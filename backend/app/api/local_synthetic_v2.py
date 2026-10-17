"""Isolated synthetic-only Candidate A API v2 proof-of-contract.

This module is deliberately not imported by ``backend.app.main``.  The only
supported transport is an explicitly enabled, trusted, same-process ASGI test
harness.  It does not create a listener, expose a capability-mint route, or
alter the released v1 application.
"""

from __future__ import annotations

import base64
import hmac
import json
import re
import secrets
import time
from dataclasses import dataclass
from threading import RLock
from typing import Callable, Iterable, Sequence

from starlette.applications import Starlette

from backend.app.core.config import Settings
from backend.app.services.uspto_offline_orchestration import (
    PROVENANCE_KEYS,
    STATES,
    OfflineUSPTOOrchestrator,
)


API_VERSION = "2.0.0"
CAPABILITY_TTL_SECONDS = 900
SESSION_TTL_SECONDS = 3600
MAX_SESSIONS = 50
DEFAULT_LIMIT = 25
MAX_LIMIT = 50

_SESSION_RE = re.compile(r"^[A-Za-z0-9_-]{1,64}$")
_REVISION_RE = re.compile(r"^[1-9][0-9]{0,9}$")
_LIMIT_RE = re.compile(r"^(?:[1-9]|[1-4][0-9]|50)$")
_SAFE_ITEM_RE = re.compile(r"^[A-Za-z0-9_-]{1,128}$")
_BEARER_RE = re.compile(r"^Bearer ([A-Za-z0-9_-]{43})$")
_CURSOR_RE = re.compile(r"^[A-Za-z0-9_-]{1,512}$")
_STATUS_PATH_RE = re.compile(r"^/api/v2/sessions/([A-Za-z0-9_-]{1,64})/status$")
_EVIDENCE_PATH_RE = re.compile(
    r"^/api/v2/sessions/([A-Za-z0-9_-]{1,64})/revisions/([^/]+)/evidence-index$"
)
_V2_PREFIX = "/api/v2/sessions/"
_FORWARDED_HEADERS = {
    b"cf-connecting-ip",
    b"client-ip",
    b"forwarded",
    b"true-client-ip",
    b"x-cluster-client-ip",
    b"x-forwarded-for",
    b"x-forwarded-host",
    b"x-forwarded-proto",
    b"x-forwarded-port",
    b"x-real-ip",
}
_VERSION_HEADERS = {b"accept-version", b"x-api-version"}
_CURSOR_KEYS = {"v", "pos", "snap", "rev", "lim", "scope", "exp"}


class SyntheticV2LifecycleError(RuntimeError):
    """Typed, source-safe failure for trusted non-HTTP lifecycle operations."""

    safe_message = "Synthetic API v2 lifecycle operation failed."

    def __init__(self, code: str) -> None:
        super().__init__(self.safe_message)
        self.code = code


@dataclass(frozen=True, slots=True, order=True)
class SyntheticEvidenceItem:
    """A trusted, pre-vetted synthetic-safe evidence index entry."""

    evidence_id: str
    digest: str

    def __post_init__(self) -> None:
        if type(self.evidence_id) is not str or not _SAFE_ITEM_RE.fullmatch(
            self.evidence_id
        ):
            raise SyntheticV2LifecycleError("INVALID_SYNTHETIC_EVIDENCE")
        if type(self.digest) is not str or not _SAFE_ITEM_RE.fullmatch(self.digest):
            raise SyntheticV2LifecycleError("INVALID_SYNTHETIC_EVIDENCE")


@dataclass(frozen=True, slots=True)
class _SessionSnapshot:
    session_id: str
    revision: int
    stage: str
    claims_status: str
    review_required: bool
    document_id: str
    source_sha256: str
    evidence: tuple[SyntheticEvidenceItem, ...]
    snapshot_id: str
    expires_at: float


@dataclass(frozen=True, slots=True)
class _CapabilityRecord:
    verifier: bytes
    session_id: str
    document_id: str
    source_sha256: str
    revision: int
    process_incarnation: bytes
    scope_id: str
    expires_at: float


class TrustedSyntheticV2Runtime:
    """Single-process, in-memory capability and immutable snapshot owner."""

    def __init__(
        self,
        *,
        monotonic: Callable[[], float] = time.monotonic,
        random_bytes: Callable[[int], bytes] = secrets.token_bytes,
    ) -> None:
        self._monotonic = monotonic
        self._random_bytes = random_bytes
        self._verifier_key = self._require_random(32)
        self._cursor_key = self._require_random(32)
        self._process_incarnation = self._require_random(16)
        self._sessions: dict[str, _SessionSnapshot] = {}
        self._capabilities: dict[str, _CapabilityRecord] = {}
        self._session_deadlines: dict[str, float] = {}
        self._lock = RLock()

    def _require_random(self, size: int) -> bytes:
        value = self._random_bytes(size)
        if type(value) is not bytes or len(value) != size:
            raise SyntheticV2LifecycleError("CSPRNG_FAILURE")
        return value

    def issue_capability(
        self,
        orchestrator: OfflineUSPTOOrchestrator,
        session_id: str,
        *,
        evidence: Sequence[SyntheticEvidenceItem],
    ) -> str:
        """Register an existing synthetic session and return one transient bearer."""

        if type(session_id) is not str or not _SESSION_RE.fullmatch(session_id):
            raise SyntheticV2LifecycleError("INVALID_SESSION")
        try:
            status = orchestrator.get_session_status(session_id)
            package = orchestrator.get_validated_package(
                session_id, expected_revision_token=status.revision_token
            )
        except Exception:
            raise SyntheticV2LifecycleError("INVALID_SESSION") from None

        if (
            status.session_id != session_id
            or status.state not in STATES
            or status.revision < 1
            or status.revision > 2_147_483_647
            or status.retained_provenance_keys != PROVENANCE_KEYS
        ):
            raise SyntheticV2LifecycleError("INVALID_SESSION")

        try:
            claims = package["filing_view"]["claims"]
            runtime_enabled = package["review_package"]["original_p2_003"][
                "review_boundary"
            ]["claims_runtime_implemented"]
        except (KeyError, TypeError):
            raise SyntheticV2LifecycleError("INVALID_SESSION") from None
        if (
            claims.get("status") != "HUMAN_CONFIRMATION_REQUIRED"
            or claims.get("claims") != []
            or runtime_enabled is not False
        ):
            raise SyntheticV2LifecycleError("CLAIMS_BOUNDARY_VIOLATION")

        if any(not isinstance(item, SyntheticEvidenceItem) for item in evidence):
            raise SyntheticV2LifecycleError("INVALID_SYNTHETIC_EVIDENCE")
        ordered = tuple(sorted(evidence, key=lambda item: (item.evidence_id, item.digest)))
        if len(ordered) > 10_000 or len({item.evidence_id for item in ordered}) != len(ordered):
            raise SyntheticV2LifecycleError("INVALID_SYNTHETIC_EVIDENCE")
        forbidden_digests = {status.source_sha256, *dict(status.artifact_digests).values()}
        if any(
            item.digest in forbidden_digests
            or item.evidence_id == status.document_id
            for item in ordered
        ):
            raise SyntheticV2LifecycleError("INVALID_SYNTHETIC_EVIDENCE")

        now = self._monotonic()
        with self._lock:
            if session_id not in self._sessions and len(self._sessions) >= MAX_SESSIONS:
                raise SyntheticV2LifecycleError("SESSION_CAPACITY_EXCEEDED")
            session_deadline = self._session_deadlines.get(session_id)
            if session_deadline is None:
                session_deadline = now + SESSION_TTL_SECONDS
                self._session_deadlines[session_id] = session_deadline
            elif now >= session_deadline:
                raise SyntheticV2LifecycleError("SESSION_EXPIRED")

            snapshot = _SessionSnapshot(
                session_id=status.session_id,
                revision=status.revision,
                stage=status.state,
                claims_status=claims["status"],
                review_required=True,
                document_id=status.document_id,
                source_sha256=status.source_sha256,
                evidence=ordered,
                snapshot_id=_b64url(self._require_random(16)),
                expires_at=session_deadline,
            )

            token = ""
            verifier = b""
            for _ in range(4):
                token = _b64url(self._require_random(32))
                if len(token) != 43:
                    raise SyntheticV2LifecycleError("CSPRNG_FAILURE")
                verifier = hmac.digest(
                    self._verifier_key, token.encode("ascii"), "sha256"
                )
                if not any(
                    hmac.compare_digest(verifier, current.verifier)
                    for current in self._capabilities.values()
                ):
                    break
            else:
                raise SyntheticV2LifecycleError("CSPRNG_FAILURE")

            scope_material = b"\0".join(
                (
                    verifier,
                    status.session_id.encode("ascii"),
                    status.document_id.encode("utf-8"),
                    status.source_sha256.encode("ascii"),
                    str(status.revision).encode("ascii"),
                    self._process_incarnation,
                )
            )
            scope_id = _b64url(
                hmac.digest(self._cursor_key, scope_material, "sha256")[:16]
            )
            capability = _CapabilityRecord(
                verifier=verifier,
                session_id=status.session_id,
                document_id=status.document_id,
                source_sha256=status.source_sha256,
                revision=status.revision,
                process_incarnation=self._process_incarnation,
                scope_id=scope_id,
                expires_at=min(now + CAPABILITY_TTL_SECONDS, session_deadline),
            )

            self.revoke_session(session_id)
            self._sessions[session_id] = snapshot
            self._capabilities[scope_id] = capability
            return token

    def revoke_session(self, session_id: str) -> None:
        """Trusted lifecycle revocation; never called by an HTTP GET."""

        with self._lock:
            self._sessions.pop(session_id, None)
            stale = [
                key
                for key, value in self._capabilities.items()
                if value.session_id == session_id
            ]
            for key in stale:
                del self._capabilities[key]

    def retire_expired(self) -> int:
        """Trusted explicit cleanup outside the request path."""

        now = self._monotonic()
        with self._lock:
            expired = [
                key for key, value in self._sessions.items() if now >= value.expires_at
            ]
            for session_id in expired:
                self.revoke_session(session_id)
            return len(expired)

    def authenticate(self, token: str) -> tuple[_SessionSnapshot, _CapabilityRecord] | None:
        """Read-only constant-time verifier lookup for one canonical bearer."""

        candidate = hmac.digest(self._verifier_key, token.encode("ascii"), "sha256")
        with self._lock:
            matched: _CapabilityRecord | None = None
            for record in tuple(self._capabilities.values()):
                if hmac.compare_digest(candidate, record.verifier):
                    matched = record
            if matched is None or matched.process_incarnation != self._process_incarnation:
                return None
            snapshot = self._sessions.get(matched.session_id)
            now = self._monotonic()
            if (
                snapshot is None
                or now >= matched.expires_at
                or now >= snapshot.expires_at
                or snapshot.document_id != matched.document_id
                or snapshot.source_sha256 != matched.source_sha256
                or snapshot.revision != matched.revision
            ):
                return None
            return snapshot, matched

    def status_payload(self, snapshot: _SessionSnapshot) -> dict[str, object]:
        return {
            "api_version": API_VERSION,
            "session_id": snapshot.session_id,
            "revision": snapshot.revision,
            "stage": snapshot.stage,
            "claims_status": snapshot.claims_status,
            "claims_count": 0,
            "review_required": snapshot.review_required,
            "product_claims_runtime_enabled": False,
        }

    def evidence_payload(
        self,
        snapshot: _SessionSnapshot,
        capability: _CapabilityRecord,
        *,
        limit: int,
        cursor: str | None,
    ) -> dict[str, object]:
        position = 0 if cursor is None else self._decode_cursor(
            cursor, snapshot=snapshot, capability=capability, limit=limit
        )
        page = snapshot.evidence[position : position + limit]
        next_position = position + len(page)
        next_cursor = None
        if next_position < len(snapshot.evidence):
            next_cursor = self._encode_cursor(
                snapshot=snapshot,
                capability=capability,
                limit=limit,
                position=next_position,
            )
        return {
            "api_version": API_VERSION,
            "session_id": snapshot.session_id,
            "revision": snapshot.revision,
            "items": [
                {"evidence_id": item.evidence_id, "digest": item.digest} for item in page
            ],
            "next_cursor": next_cursor,
        }

    def _encode_cursor(
        self,
        *,
        snapshot: _SessionSnapshot,
        capability: _CapabilityRecord,
        limit: int,
        position: int,
    ) -> str:
        payload = {
            "v": 1,
            "pos": position,
            "snap": snapshot.snapshot_id,
            "rev": snapshot.revision,
            "lim": limit,
            "scope": capability.scope_id,
            "exp": int(min(snapshot.expires_at, capability.expires_at) * 1_000_000),
        }
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("ascii")
        signature = hmac.digest(self._cursor_key, raw, "sha256")
        cursor = _b64url(raw) + _b64url(signature)
        if len(cursor) > 512:
            raise RuntimeError("cursor bound exceeded")
        return cursor

    def _decode_cursor(
        self,
        cursor: str,
        *,
        snapshot: _SessionSnapshot,
        capability: _CapabilityRecord,
        limit: int,
    ) -> int:
        if not _CURSOR_RE.fullmatch(cursor) or len(cursor) <= 43:
            raise ValueError("invalid cursor")
        payload_text, signature_text = cursor[:-43], cursor[-43:]
        try:
            raw = _b64url_decode(payload_text)
            signature = _b64url_decode(signature_text)
            payload = json.loads(raw.decode("ascii"))
        except (ValueError, UnicodeDecodeError, json.JSONDecodeError):
            raise ValueError("invalid cursor") from None
        expected = hmac.digest(self._cursor_key, raw, "sha256")
        if not hmac.compare_digest(expected, signature):
            raise ValueError("invalid cursor")
        if type(payload) is not dict or set(payload) != _CURSOR_KEYS:
            raise ValueError("invalid cursor")
        expected_expiry = int(min(snapshot.expires_at, capability.expires_at) * 1_000_000)
        if (
            payload.get("v") != 1
            or payload.get("snap") != snapshot.snapshot_id
            or payload.get("rev") != snapshot.revision
            or payload.get("lim") != limit
            or payload.get("scope") != capability.scope_id
            or payload.get("exp") != expected_expiry
            or self._monotonic() * 1_000_000 >= expected_expiry
            or type(payload.get("pos")) is not int
            or not 1 <= payload["pos"] < len(snapshot.evidence)
        ):
            raise ValueError("invalid cursor")
        return payload["pos"]


class CandidateASyntheticV2App:
    """Minimal ASGI app with an authorization-first raw protocol guard."""

    def __init__(
        self,
        runtime: TrustedSyntheticV2Runtime,
        *,
        host: str = "127.0.0.1",
        port: int = 8765,
    ) -> None:
        if host not in {"127.0.0.1", "::1"} or not 1 <= port <= 65535:
            raise ValueError("literal loopback host and valid port required")
        self.runtime = runtime
        self.host = host
        self.port = port
        self.host_header = f"[{host}]:{port}" if host == "::1" else f"{host}:{port}"

    async def __call__(self, scope, receive, send) -> None:
        if scope["type"] == "lifespan":
            while True:
                message = await receive()
                if message["type"] == "lifespan.startup":
                    await send({"type": "lifespan.startup.complete"})
                elif message["type"] == "lifespan.shutdown":
                    await send({"type": "lifespan.shutdown.complete"})
                    return
            return
        if scope["type"] != "http":
            return

        path = scope.get("path", "")
        is_candidate = isinstance(path, str) and path.startswith(_V2_PREFIX)
        if not is_candidate:
            await _generic_not_found(send)
            return
        if not self._transport_is_trusted(scope):
            await _safe_error(send, 404, "session_unavailable", "The session is unavailable.")
            return
        if scope.get("method") != "GET":
            await _generic_not_found(send)
            return

        headers = tuple(scope.get("headers", ()))
        authorization = [value for name, value in headers if name.lower() == b"authorization"]
        if len(authorization) != 1:
            await _safe_error(send, 404, "session_unavailable", "The session is unavailable.")
            return
        try:
            authorization_text = authorization[0].decode("ascii")
        except UnicodeDecodeError:
            authorization_text = ""
        match = _BEARER_RE.fullmatch(authorization_text)
        if match is None:
            await _safe_error(send, 404, "session_unavailable", "The session is unavailable.")
            return
        token = match.group(1)
        try:
            if len(_b64url_decode(token)) != 32:
                raise ValueError
        except ValueError:
            await _safe_error(send, 404, "session_unavailable", "The session is unavailable.")
            return
        authenticated = self.runtime.authenticate(token)
        if authenticated is None:
            await _safe_error(send, 404, "session_unavailable", "The session is unavailable.")
            return
        snapshot, capability = authenticated

        try:
            raw_path = scope.get("raw_path", path.encode("ascii", "ignore"))
            if b"%" in raw_path or len(raw_path) > 512:
                await _generic_not_found(send)
                return

            status_match = _STATUS_PATH_RE.fullmatch(path)
            evidence_match = _EVIDENCE_PATH_RE.fullmatch(path)
            if status_match is not None:
                if status_match.group(1) != snapshot.session_id:
                    await _safe_error(
                        send, 404, "session_unavailable", "The session is unavailable."
                    )
                    return
                if self._has_post_auth_protocol_error(scope, headers):
                    await _safe_error(
                        send, 422, "invalid_request", "The request is invalid."
                    )
                    return
                if scope.get("query_string", b""):
                    await _safe_error(send, 422, "invalid_request", "The request is invalid.")
                    return
                await _json_response(send, 200, self.runtime.status_payload(snapshot))
                return

            if evidence_match is None:
                await _generic_not_found(send)
                return
            if evidence_match.group(1) != snapshot.session_id:
                await _safe_error(send, 404, "session_unavailable", "The session is unavailable.")
                return
            if self._has_post_auth_protocol_error(scope, headers):
                await _safe_error(send, 422, "invalid_request", "The request is invalid.")
                return
            revision_text = evidence_match.group(2)
            if not _REVISION_RE.fullmatch(revision_text):
                await _safe_error(send, 422, "invalid_request", "The request is invalid.")
                return
            revision = int(revision_text)
            if revision > 2_147_483_647:
                await _safe_error(send, 422, "invalid_request", "The request is invalid.")
                return
            if revision != snapshot.revision:
                await _safe_error(send, 409, "stale_revision", "The revision is stale.")
                return
            try:
                limit, cursor = _parse_query(scope.get("query_string", b""))
                payload = self.runtime.evidence_payload(
                    snapshot, capability, limit=limit, cursor=cursor
                )
            except ValueError:
                await _safe_error(send, 422, "invalid_request", "The request is invalid.")
                return
            await _json_response(send, 200, payload)
        except Exception:
            await _safe_error(send, 500, "internal_error", "The request could not be completed.")

    def _transport_is_trusted(self, scope) -> bool:
        headers = tuple(scope.get("headers", ()))
        if len(headers) > 64 or sum(len(name) + len(value) for name, value in headers) > 16_384:
            return False
        host_values = [value for name, value in headers if name.lower() == b"host"]
        if len(host_values) != 1 or host_values[0] != self.host_header.encode("ascii"):
            return False
        names = [name.lower() for name, _ in headers]
        if b"origin" in names or any(
            name in _FORWARDED_HEADERS or name.startswith(b"x-forwarded-") for name in names
        ):
            return False
        client = scope.get("client")
        server = scope.get("server")
        if not client or client[0] != self.host:
            return False
        if not server or server[0] != self.host or server[1] != self.port:
            return False
        query = scope.get("query_string", b"")
        raw_path = scope.get("raw_path", b"")
        return (
            isinstance(query, bytes)
            and len(query) <= 2_048
            and isinstance(raw_path, bytes)
            and len(raw_path) <= 512
        )

    @staticmethod
    def _has_post_auth_protocol_error(scope, headers: Iterable[tuple[bytes, bytes]]) -> bool:
        names = [name.lower() for name, _ in headers]
        if any(name in _VERSION_HEADERS for name in names) or b"cookie" in names:
            return True
        content_lengths = [value for name, value in headers if name.lower() == b"content-length"]
        transfer_encodings = [value for name, value in headers if name.lower() == b"transfer-encoding"]
        if len(content_lengths) > 1 or transfer_encodings:
            return True
        if content_lengths:
            try:
                if int(content_lengths[0]) != 0:
                    return True
            except ValueError:
                return True
        return False


def create_local_synthetic_v2_app(
    settings: Settings,
    *,
    runtime: TrustedSyntheticV2Runtime | None = None,
    host: str = "127.0.0.1",
    port: int = 8765,
):
    """Return an unregistered app when OFF, or the isolated trusted ASGI app."""

    if not settings.enable_local_synthetic_v2_api:
        return Starlette(routes=[])
    if runtime is None:
        raise ValueError("trusted in-process runtime required")
    return CandidateASyntheticV2App(runtime, host=host, port=port)


def _parse_query(query: bytes) -> tuple[int, str | None]:
    if not query:
        return DEFAULT_LIMIT, None
    if any(value > 127 for value in query) or b"%" in query or b"+" in query:
        raise ValueError("invalid query")
    values: dict[str, str] = {}
    for part in query.split(b"&"):
        if part.count(b"=") != 1:
            raise ValueError("invalid query")
        raw_name, raw_value = part.split(b"=", 1)
        name = raw_name.decode("ascii")
        value = raw_value.decode("ascii")
        if name not in {"limit", "cursor"} or name in values or not value:
            raise ValueError("invalid query")
        values[name] = value
    limit_text = values.get("limit", str(DEFAULT_LIMIT))
    if not _LIMIT_RE.fullmatch(limit_text):
        raise ValueError("invalid limit")
    cursor = values.get("cursor")
    if cursor is not None and not _CURSOR_RE.fullmatch(cursor):
        raise ValueError("invalid cursor")
    return int(limit_text), cursor


def _b64url(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def _b64url_decode(value: str) -> bytes:
    if not value or not re.fullmatch(r"[A-Za-z0-9_-]+", value):
        raise ValueError("invalid base64url")
    padding = "=" * ((4 - len(value) % 4) % 4)
    decoded = base64.b64decode(value + padding, altchars=b"-_", validate=True)
    if _b64url(decoded) != value:
        raise ValueError("noncanonical base64url")
    return decoded


async def _safe_error(send, status: int, code: str, message: str) -> None:
    await _json_response(
        send,
        status,
        {
            "code": code,
            "message": message,
            "correlation_id": secrets.token_hex(16),
        },
    )


async def _generic_not_found(send) -> None:
    await _json_response(send, 404, {"detail": "Not Found"})


async def _json_response(send, status: int, content: dict[str, object]) -> None:
    body = json.dumps(content, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    headers = [
        (b"content-type", b"application/json"),
        (b"content-length", str(len(body)).encode("ascii")),
        (b"cache-control", b"no-store"),
        (b"x-content-type-options", b"nosniff"),
    ]
    await send({"type": "http.response.start", "status": status, "headers": headers})
    await send({"type": "http.response.body", "body": body})
