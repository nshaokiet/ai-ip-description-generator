"""S2-only shared publication/revocation gate; no payloads or custody secrets.

An exclusive mkdir serializes Python invalidation and Node transport handoff.
No stale-lock recovery: uncertain process/file state fails closed until host teardown.
Never acquire this gate while holding session/workflow/custody locks.
"""
from contextlib import contextmanager
import hashlib
import json
import math
import secrets
import time

from backend.app.services.product_web_host_control import SecurityError, create_private_dir, safe_path, write_private

WAIT_SECONDS = 1.0


class PublicationError(Exception):
    status, code = 503, "publication_unavailable"


class PublicationGate:
    def __init__(self, parent):
        self.root = create_private_dir(parent / "publication")
        self.path, self.latch = self.root / "state.json", self.root / "gate"
        self.instance = secrets.token_hex(32)
        self.failed = False
        write_private(self.path, {"instance": self.instance, "open": True, "receipts": {}})

    @contextmanager
    def transaction(self):
        acquired = False
        try:
            if self.failed or (self.root / "failed").exists():
                raise PublicationError()
            end = time.monotonic() + WAIT_SECONDS
            while True:
                try:
                    self.latch.mkdir(mode=0o700)
                    acquired = True
                    break
                except FileExistsError:
                    if time.monotonic() >= end:
                        raise PublicationError()
                    time.sleep(0.005)
            safe_path(self.path)
            if self.path.stat().st_size > 8192:
                raise PublicationError()
            value = json.loads(self.path.read_text(encoding="utf-8"))
            if (set(value) != {"instance", "open", "receipts"}
                    or value["instance"] != self.instance or type(value["open"]) is not bool
                    or type(value["receipts"]) is not dict or len(value["receipts"]) > 2):
                raise PublicationError()
            yield value
            # Keep the provisioned owner-only ACL. A crash/partial write is a
            # denial, never a reason to recover or reuse grants automatically.
            with self.path.open("w", encoding="utf-8") as stream:
                json.dump(value, stream, separators=(",", ":"))
        except PublicationError:
            self.failed = True
            try:
                write_private(self.root / "failed", {})
            except OSError:
                pass
            raise
        except (OSError, ValueError, KeyError, TypeError, SecurityError):
            self.failed = True
            try:
                write_private(self.root / "failed", {})
            except OSError:
                pass
            raise PublicationError() from None
        finally:
            if acquired:
                self.latch.rmdir()

    def issue(self, item, epoch, operation, action, request_path, budget_ms, response, live):
        with self.transaction() as state:
            live()
            if not state["open"]:
                raise PublicationError()
            # Replace only this owner's older, unconsumed result: bounded two
            # owners, and no accumulation of replay/tombstone records.
            state["receipts"] = {k: v for k, v in state["receipts"].items() if v["principal"] != item.owner}
            if len(state["receipts"]) >= 2:
                raise PublicationError()
            receipt = secrets.token_hex(32)
            state["receipts"][receipt] = {
                "instance": self.instance, "principal": item.owner,
                "session": hashlib.sha256(item.token.encode()).hexdigest(),
                "document": item.selector, "revision": item.ref.revision,
                "epoch": epoch, "operation": operation, "action": action,
                "path": request_path, "digest": hashlib.sha256(response.body).hexdigest(),
                "bytes": len(response.body), "status": response.status_code,
                "media_type": response.headers["content-type"],
                # Node measures from BEFORE upstream request submission. Budget
                # is floored at backend operation admission, not receipt time.
                "budget_ms": math.floor(budget_ms),
            }
        response.headers["X-AIIP-Publication"] = receipt

    def invalidate(self, owners=(), *, close=False):
        with self.transaction() as state:
            state["receipts"] = {k: v for k, v in state["receipts"].items()
                                 if not close and v["principal"] not in owners}
            if close:
                state["open"] = False

    def dispose(self):
        self.path.unlink()
        self.root.rmdir()
