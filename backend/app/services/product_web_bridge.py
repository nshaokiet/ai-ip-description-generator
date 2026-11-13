"""Bounded S2-local owner gateway. Revocation never takes workflow/custody locks."""
from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path
import secrets
import threading

from fastapi.responses import JSONResponse, Response
from starlette.concurrency import run_in_threadpool

from backend.app.core.config import Settings
from backend.app.services.custody_review import review_documents
from backend.app.services.document_parsing import DocumentPreparationService
from backend.app.services.document_registry import DocumentRecord, DocumentRegistry
from backend.app.services.document_storage import DocumentStorage
from backend.app.services.document_validation import DocumentValidator
from backend.app.services.product_synthetic_workflow import OfflineSyntheticWorkflow
from backend.app.services.product_web_host_control import create_private_dir, safe_path, SecurityError
from backend.app.services.product_web_synthetic_runtime import PINS, PinnedSyntheticRuntime
from backend.app.services.uspto_offline_renderer import FILES

BODY_LIMIT = 2048
REVIEW_LIMIT = 8 * 1024 * 1024
ARTIFACT_LIMIT = 8 * 1024 * 1024
OP_SECONDS = 120


class BridgeError(Exception):
    def __init__(self, status=409, code="document_unavailable"):
        self.status, self.code = status, code


def require(value, status=409, code="document_unavailable"):
    if not value:
        raise BridgeError(status, code)


@dataclass
class Document:
    owner: str
    token: str = field(repr=False)
    selector: str = field(default_factory=lambda: secrets.token_hex(16))
    epoch: int = 0
    retired: bool = False
    ref: object = None
    workflow: object = None
    view: str | None = None
    digest: str | None = None
    export: object = None
    root: Path | None = None
    upload_id: str | None = None
    storage: object = None
    deadline: float = 0


class SyntheticBridge:
    def __init__(self, sessions, root):
        safe_path(root, directory=True)
        self.root = create_private_dir(root / "s2")
        self.sessions = sessions
        self.runtime = PinnedSyntheticRuntime()
        self.lock, self.capacity = threading.RLock(), threading.Lock()
        self.documents = {}
        self.closed = self.quarantined = False
        self.stopping = threading.Event()
        # Session notifications only touch our small metadata lock, never custody.
        sessions.on_invalidate = self.revoke
        self.maintenance = threading.Thread(target=self._maintenance, daemon=True)
        self.maintenance.start()

    def revoke(self, owner):
        with self.lock:
            item = self.documents.get(owner)
            if item is not None:
                item.retired = True
                item.epoch += 1
                item.view = item.export = None

    def _live(self, item, epoch, deadline):
        # Lock order is always Sessions -> gateway; never acquire workflow here.
        with self.sessions.lock:
            record = self.sessions.authority(item.token)
            with self.lock:
                require(not self.closed and not self.quarantined and record["owner"] == item.owner
                        and self.documents.get(item.owner) is item and not item.retired
                        and item.epoch == epoch and self.sessions.clock() < deadline, 401,
                        "authority_revoked")

    def _dispose(self, item):
        try:
            if item.workflow is not None:
                item.workflow.close()
            if item.storage is not None and item.upload_id:
                require(item.storage.delete(item.upload_id), 503, "cleanup_failed")
            if item.root is not None:
                safe_path(item.root, directory=True)
                for name in ("exports", "uploads"):
                    path = item.root / name
                    if path.exists():
                        safe_path(path, directory=True)
                        path.rmdir()  # Only known, now-empty owned directories.
                item.root.rmdir()
            with self.lock:
                if self.documents.get(item.owner) is item:
                    del self.documents[item.owner]
        except Exception:
            with self.lock:
                self.quarantined = True  # Never reuse failed-cleanup state/capacity.

    def _reap(self):
        with self.lock:
            retired = tuple(item for item in self.documents.values() if item.retired)
        for item in retired:
            self._dispose(item)

    def _maintenance(self):
        while not self.stopping.wait(0.1):
            with self.sessions.lock:
                if not self.sessions.closed:
                    self.sessions._sweep()
            if self.capacity.acquire(blocking=False):
                try:
                    self._reap()
                finally:
                    self.capacity.release()

    def close(self):
        with self.lock:
            self.closed = True
            for item in self.documents.values():
                item.retired = True
                item.epoch += 1
        self.stopping.set()
        self.maintenance.join(1)
        # This is a bounded wait, not forced thread termination.
        if not self.capacity.acquire(timeout=5):
            raise SecurityError()
        try:
            self._reap()
            if self.quarantined or self.maintenance.is_alive():
                raise SecurityError()
            self.root.rmdir()
        finally:
            self.capacity.release()

    def cancel(self, token, selector):
        with self.sessions.lock:
            record = self.sessions.authority(token)
            with self.lock:
                item = self.documents.get(record["owner"])
                require(item is not None and item.selector == selector and not item.retired, 404)
                self.revoke(item.owner)

    async def execute(self, token, selector, action, data, *, source=None):
        # Reserve before submitting to a thread pool. At most one task, no work queue.
        with self.sessions.lock:
            owner = self.sessions.authority(token)["owner"]
            with self.lock:
                existing = self.documents.get(owner)
                if action != "intake":
                    require(existing is not None and not existing.retired and existing.selector == selector, 404)
            require(self.capacity.acquire(blocking=False), 429, "capacity")
            try:
                with self.lock:
                    require(not self.closed and not self.quarantined, 503)
                    item = self.documents.get(owner)
                    if action == "intake":
                        require(item is None, 409, "document_capacity")
                        require(len(self.documents) < 2, 429, "capacity")
                        item = Document(owner, token)
                        self.documents[owner] = item
                    require(item is not None and not item.retired
                            and (action == "intake" or item.selector == selector), 404)
                    epoch = item.epoch
                    deadline = min(self.sessions.authority(token)["deadline"], self.sessions.clock() + OP_SECONDS)
                    item.deadline = deadline
            except BaseException:
                self.capacity.release()
                raise
        future = asyncio.create_task(run_in_threadpool(self._work, item, epoch, deadline, action, data, source))
        try:
            result = await asyncio.wait_for(asyncio.shield(future), OP_SECONDS)
            self._live(item, epoch, deadline)
            return result, lambda: self._live(item, epoch, deadline)
        except TimeoutError:
            self.revoke(owner)
            future.add_done_callback(lambda task: task.exception() if not task.cancelled() else None)
            raise BridgeError(504, "operation_expired") from None
        except BaseException:
            # Thread may still compute. Fence it immediately, then its finally reaps.
            self.revoke(owner)
            # Retrieve late exceptions without exposing content to event-loop logging.
            future.add_done_callback(lambda task: task.exception() if not task.cancelled() else None)
            raise

    def _work(self, item, epoch, deadline, action, data, source):
        try:
            self._live(item, epoch, deadline)
            if action == "intake":
                filename, media_type, raw = source
                item.root = create_private_dir(self.root / item.selector)
                registry = DocumentRegistry()
                item.storage = DocumentStorage(create_private_dir(item.root / "uploads"),
                    ttl_seconds=1800, max_upload_bytes=BODY_LIMIT, read_chunk_bytes=BODY_LIMIT,
                    on_removed=registry.remove)
                item.upload_id = item.storage.allocate_id()
                path = item.storage.path_for(item.upload_id)
                with path.open("xb") as stream:
                    stream.write(raw)
                result = DocumentValidator(Settings(storage_root=item.storage.root)).validate(
                    path, filename=filename, declared_mime=media_type)
                registry.register(DocumentRecord(item.upload_id, filename, media_type, len(raw),
                                                  result.page_count, hashlib.sha256(raw).hexdigest()))
                def authorized():
                    try:
                        self._live(item, epoch, item.deadline)
                        return True
                    except Exception:
                        return False
                item.workflow = OfflineSyntheticWorkflow(item.storage, registry,
                    DocumentPreparationService(item.storage, registry),
                    output_root=create_private_dir(item.root / "exports"), extraction_runtime=self.runtime,
                    fixtures=self.runtime.fixtures, authorize_invocation=authorized,
                    review_authorizer=lambda actor, context, decision: (
                        actor == item.owner and context == "S2_LOCAL_CONTENT_REVIEW"
                        and decision in {"CONTENT_REVIEW_ACKNOWLEDGED", "CLAIMS_INCOMPLETE_ACKNOWLEDGED"}),
                    enabled=True, clock=self.sessions.clock)
                item.ref = item.workflow.start(item.upload_id)
            else:
                if action != "review" and action != "download":
                    require(type(data.get("revision")) is int and data["revision"] == item.ref.revision
                            and item.view is not None and data.get("view_id") == item.view)
                if action in {"ack-content", "ack-claims"}:
                    require(set(data) == {"revision", "view_id", "acknowledge"}
                            and data["acknowledge"] is True, 400)
                    item.workflow.acknowledge(item.ref, review_snapshot_sha256=item.digest,
                        actor=item.owner, context="S2_LOCAL_CONTENT_REVIEW", acknowledge=True,
                        incomplete_claims=action == "ack-claims")
                elif action == "render":
                    require(set(data) == {"revision", "view_id"}, 400)
                    item.export = item.workflow.render(item.ref)
                    require(len(item.export.artifacts) == 4)
                    for artifact in item.export.artifacts:
                        require(0 < artifact.size_bytes <= ARTIFACT_LIMIT, 503, "response_limit")
                        # Verify every file before exposing ANY part of the bundle.
                        item.workflow.download(item.ref, filename=artifact.filename,
                                               manifest_sha256=item.export.manifest_sha256)
                elif action == "download":
                    require(item.export is not None and data["revision"] == item.ref.revision, 409)
                    require(data["filename"] in FILES, 404)
                    payload = item.workflow.download(item.ref, filename=data["filename"],
                                                    manifest_sha256=item.export.manifest_sha256)
                    require(0 < len(payload) <= ARTIFACT_LIMIT, 503, "response_limit")
                    artifact = next(a for a in item.export.artifacts if a.filename == data["filename"])
                    self._live(item, epoch, deadline)
                    return Response(payload, media_type=artifact.media_type,
                        headers={"Content-Disposition": 'attachment; filename="' + artifact.filename + '"'})
                else:
                    require(action == "review", 404)
            projection = item.workflow.review(item.ref)
            if action == "review":
                item.view, item.digest = secrets.token_hex(16), projection.review_snapshot_sha256
            value = {"document": item.selector, "revision": item.ref.revision, "state": projection.state,
                     "synthetic_draft": True, "filing_ready": False, "claims_runtime_enabled": False}
            if action == "review":
                value.update(view_id=item.view, originals=review_documents(projection.originals),
                             claims_review_required=projection.claims_review_required)
            if action == "render":
                value["artifacts"] = [{"filename": a.filename, "media_type": a.media_type,
                    "size_bytes": a.size_bytes, "sha256": a.sha256} for a in item.export.artifacts]
            body = json.dumps(value, ensure_ascii=False, allow_nan=False).encode()
            require(len(body) <= (REVIEW_LIMIT if action == "review" else 8192), 503, "response_limit")
            self._live(item, epoch, deadline)
            return Response(body, media_type="application/json", status_code=201 if action == "intake" else 200)
        except Exception as exc:
            # Expected review gating is retryable. Other failures retire the document.
            code = getattr(exc, "code", "document_unavailable")
            if action == "intake" or code not in {"REVIEW_REQUIRED", "CLAIMS_REVIEW_REQUIRED", "INVALID_STATE", "document_unavailable"}:
                self.revoke(item.owner)
            return JSONResponse({"error": {"code": "document_unavailable"}}, status_code=409)
        finally:
            try:
                if not self._allowed(item, epoch, deadline):
                    self.revoke(item.owner)
                self._reap()
            finally:
                self.capacity.release()

    def _allowed(self, item, epoch, deadline):
        try:
            self._live(item, epoch, deadline)
            return True
        except Exception:
            return False


def admit(filename, media_type, body):
    identity = (filename, media_type, len(body), hashlib.sha256(body).hexdigest())
    require(any(identity == pin[:4] for pin in PINS), 415, "source_not_admitted")
