"""PRODUCT-001A: opt-in internal synthetic upload -> review -> draft export.

The host supplies live invocation authorization, pinned fixture byte identities,
one offline runtime and a Human-review authorizer at construction. None of these
are request parameters. This is not an HTTP API, public upload bridge or provider.
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from threading import RLock
from typing import Any, Callable
from uuid import uuid4

from backend.app.services.custody_review import C1ReviewProjection, C1ReviewTarget
from backend.app.services.document_parsing import DocumentPreparationService, compute_sha256
from backend.app.services.document_registry import DocumentRegistry
from backend.app.services.document_storage import DocumentStorage
from backend.app.services.preapi_source_custody import (
    MIME, CustodyError, CustodyReceipt, SyntheticExtractionRuntime, TrustedCustodyCoordinator,
)
from backend.app.services.supported_draft_claims_validation import sha256_canonical
from backend.app.services.uspto_offline_renderer import FILES


class ProductWorkflowError(RuntimeError):
    def __init__(self, code: str) -> None:
        super().__init__("Offline synthetic workflow request was rejected.")
        self.code = code


@dataclass(frozen=True, slots=True)
class SyntheticFixtureIdentity:
    """Host-pinned test fixture bytes; not a claim of Human/production approval."""
    sha256: str
    media_type: str
    size_bytes: int


@dataclass(frozen=True, slots=True)
class ProductSessionRef:
    session_id: str
    document_id: str
    revision: int


@dataclass(frozen=True, slots=True)
class ProductArtifact:
    filename: str
    media_type: str
    size_bytes: int
    sha256: str


@dataclass(frozen=True, slots=True)
class ProductExport:
    session: ProductSessionRef
    custody_id: str
    review_snapshot_sha256: str
    manifest_sha256: str
    artifacts: tuple[ProductArtifact, ...]
    synthetic_draft: bool = True
    filing_ready: bool = False


class OfflineSyntheticWorkflow:
    """One trusted host, at most four sessions, serialized operations, no cache.

    A host instance serves one principal; its callback must verify that exact
    principal in the current invocation, not merely any logged-in caller.
    References select a host-private handle. Every invocation additionally needs
    the host's current authorization callback. Do not expose this object or its
    constructor to an untrusted caller. A restart invalidates all references.
    """

    def __init__(
        self, storage: DocumentStorage, registry: DocumentRegistry,
        preparation: DocumentPreparationService, *, output_root: Path,
        extraction_runtime: SyntheticExtractionRuntime,
        fixtures: tuple[SyntheticFixtureIdentity, ...] = (),
        authorize_invocation: Callable[[], bool],
        review_authorizer: Callable[[str, str, str], bool],
        enabled: bool = False, clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if getattr(extraction_runtime, "synthetic_only", False) is not True:
            raise ProductWorkflowError("PROVIDER_BLOCKED")
        self._fixtures = tuple(fixtures)
        hashes = set()
        for item in self._fixtures:
            if (type(item) is not SyntheticFixtureIdentity or type(item.sha256) is not str
                    or type(item.media_type) is not str or item.sha256 in hashes
                    or len(item.sha256) != 64 or any(c not in "0123456789abcdef" for c in item.sha256)
                    or item.media_type not in MIME.values()
                    or type(item.size_bytes) is not int or not 0 < item.size_bytes <= 20 * 1024 * 1024):
                raise ProductWorkflowError("INVALID_FIXTURE_POLICY")
            hashes.add(item.sha256)
        self._runtime = extraction_runtime
        self._authorize_invocation = authorize_invocation
        self._owner = uuid4().hex
        self._pending_target: C1ReviewTarget | None = None
        self._handles: dict[str, CustodyReceipt] = {}
        self._lock = RLock()
        self._custody = TrustedCustodyCoordinator(
            storage, registry, preparation, output_root=output_root,
            enabled=enabled, clock=clock, max_records=4,
            review_authorizer=review_authorizer, require_bound_review=True,
            review_binding_authorizer=self._authorize_target,
        )

    def _authorized(self) -> None:
        try:
            allowed = self._authorize_invocation() is True
        except Exception:
            allowed = False
        if not allowed:
            raise ProductWorkflowError("UNAUTHORIZED")

    def _authorize_target(self, target: C1ReviewTarget) -> bool:
        self._authorized()
        if self._pending_target is None or target != self._pending_target:
            return False
        self._pending_target = None  # consumed once, even if the operation later fails
        return True

    @staticmethod
    def _ref(session_id: str, receipt: CustodyReceipt) -> ProductSessionRef:
        return ProductSessionRef(session_id, receipt.document_id, receipt.revision)

    def _get(self, ref: ProductSessionRef) -> CustodyReceipt:
        self._authorized()
        if (type(ref) is not ProductSessionRef or type(ref.session_id) is not str
                or type(ref.document_id) is not str or type(ref.revision) is not int):
            raise ProductWorkflowError("SESSION_MISMATCH")
        receipt = self._handles.get(ref.session_id)
        if receipt is None or ref != self._ref(ref.session_id, receipt):
            raise ProductWorkflowError("SESSION_MISMATCH")
        try:
            return self._custody.status(receipt.custody_id, owner=self._owner,
                                        revision_token=receipt.revision_token)
        except CustodyError as exc:
            if exc.code == "SESSION_UNAVAILABLE":
                self._handles.pop(ref.session_id, None)
            raise

    def _projection(self, receipt: CustodyReceipt) -> C1ReviewProjection:
        return self._custody.get_review_projection(
            receipt.custody_id, owner=self._owner, revision_token=receipt.revision_token,
        )

    def start(self, document_id: str) -> ProductSessionRef:
        """Consume a host-registered, byte-pinned synthetic PDF/DOCX, never a demo ID."""
        with self._lock:
            self._authorized()
            if type(document_id) is not str:
                raise ProductWorkflowError("SOURCE_NOT_ADMITTED")
            self._custody.sweep_expired()
            for session_id, old in tuple(self._handles.items()):
                try:
                    self._custody.status(old.custody_id, owner=self._owner,
                                         revision_token=old.revision_token)
                except CustodyError as exc:
                    if exc.code != "SESSION_UNAVAILABLE":
                        raise
                    self._handles.pop(session_id)
            if len(self._handles) >= 4:
                raise ProductWorkflowError("CAPACITY")
            record = self._custody.registry.get(document_id)
            if record is None or not any(
                (record.sha256, record.media_type, record.size_bytes)
                == (entry.sha256, entry.media_type, entry.size_bytes) for entry in self._fixtures
            ):
                raise ProductWorkflowError("SOURCE_NOT_ADMITTED")
            with self._custody.storage.lease(document_id) as path:
                if (path.is_symlink() or not path.is_file()
                        or path.stat().st_size != record.size_bytes
                        or compute_sha256(path) != record.sha256):
                    raise ProductWorkflowError("SOURCE_NOT_ADMITTED")
            p3 = {"source_document_synthetic": True}
            p4 = {
                "language": "en", "target_jurisdiction": "US",
                "requested_claim_types": ["SYSTEM", "METHOD", "COMPOSITION"],
                "max_dependent_claims_per_family": 4, "source_document_synthetic": True,
                "selected_solution_id": "IR-SOL-0001", "p2_003_generation_config": dict(p3),
            }
            receipt = self._custody.commit_upload(
                document_id, owner=self._owner, extraction_runtime=self._runtime,
                p2_003_generation_config=p3, p2_004_generation_config=p4,
            )
            try:
                self._projection(receipt)  # don't publish a partial/unreviewable session
            except Exception:
                self._custody.abort(receipt.custody_id, owner=self._owner,
                                    revision_token=receipt.revision_token)
                raise
            session_id = uuid4().hex
            self._handles[session_id] = receipt
            return self._ref(session_id, receipt)

    def review(self, ref: ProductSessionRef) -> C1ReviewProjection:
        with self._lock:
            return self._projection(self._get(ref))

    def acknowledge(
        self, ref: ProductSessionRef, *, review_snapshot_sha256: str,
        actor: str, context: str, acknowledge: bool,
        incomplete_claims: bool = False,
    ) -> C1ReviewProjection:
        """Trusted presenter must expose the complete snapshot before this call.

        Incomplete Claims require a distinct subsequent affirmative invocation.
        This records a local draft review, never legal or semantic acceptance.
        """
        with self._lock:
            receipt = self._get(ref)
            projection = self._projection(receipt)
            if (acknowledge is not True or type(incomplete_claims) is not bool
                    or review_snapshot_sha256 != projection.review_snapshot_sha256):
                raise ProductWorkflowError("REVIEW_MISMATCH")
            decision = ("CLAIMS_INCOMPLETE_ACKNOWLEDGED" if incomplete_claims
                        else "CONTENT_REVIEW_ACKNOWLEDGED")
            self._pending_target = C1ReviewTarget(
                projection.coordinator_instance_id, receipt.custody_id, receipt.document_id,
                self._owner, receipt.revision,
                hashlib.sha256(receipt.revision_token.encode()).hexdigest(),
                projection.review_snapshot_sha256, actor, context, decision,
            )
            try:
                kwargs = dict(owner=self._owner, revision_token=receipt.revision_token,
                              actor=actor, context=context)
                if incomplete_claims:
                    self._custody.acknowledge_incomplete_claims(
                        receipt.custody_id, acknowledge=True, **kwargs,
                    )
                else:
                    self._custody.acknowledge_review(receipt.custody_id, **kwargs)
            finally:
                self._pending_target = None
            return self._projection(self._get(ref))

    def revise(self, ref: ProductSessionRef, *, structured_analysis: dict[str, Any]) -> ProductSessionRef:
        with self._lock:
            receipt = self._get(ref)
            updated = self._custody.revise(
                receipt.custody_id, owner=self._owner, revision_token=receipt.revision_token,
                structured_analysis=structured_analysis,
            )
            self._handles[ref.session_id] = updated
            try:
                self._projection(updated)
            except Exception:
                self._custody.abort(updated.custody_id, owner=self._owner,
                                    revision_token=updated.revision_token)
                self._handles.pop(ref.session_id, None)
                raise
            return self._ref(ref.session_id, updated)

    def _export(self, ref: ProductSessionRef, receipt: CustodyReceipt) -> ProductExport:
        projection = self._projection(receipt)
        if (receipt.state not in {"RENDERED", "DOWNLOADED"}
                or len(receipt.manifest) != len(FILES)
                or {item.filename for item in receipt.manifest} != set(FILES)):
            raise ProductWorkflowError("EXPORT_UNAVAILABLE")
        for item in receipt.manifest:
            if (item.custody_id != receipt.custody_id or item.revision != receipt.revision
                    or item.owner != self._owner
                    or item.media_type != MIME[Path(item.filename).suffix]):
                raise ProductWorkflowError("EXPORT_UNAVAILABLE")
        digest = sha256_canonical({
            "domain": "PRODUCT-001A-MANIFEST-1.0.0",
            "custody_id": receipt.custody_id, "document_id": receipt.document_id,
            "revision": receipt.revision, "source_sha256": receipt.source_sha256,
            "review_snapshot_sha256": projection.review_snapshot_sha256,
            "artifacts": [asdict(item) for item in receipt.manifest],
        })
        return ProductExport(ref, receipt.custody_id, projection.review_snapshot_sha256,
                             digest, tuple(ProductArtifact(item.filename, item.media_type,
                                                          item.size_bytes, item.sha256)
                                           for item in receipt.manifest))

    def render(self, ref: ProductSessionRef) -> ProductExport:
        with self._lock:
            receipt = self._get(ref)
            result = self._custody.render(receipt.custody_id, owner=self._owner,
                                          revision_token=receipt.revision_token)
            return self._export(ref, result)

    def download(self, ref: ProductSessionRef, *, filename: str, manifest_sha256: str) -> bytes:
        with self._lock:
            receipt = self._get(ref)
            export = self._export(ref, receipt)
            if manifest_sha256 != export.manifest_sha256 or filename not in FILES:
                raise ProductWorkflowError("MANIFEST_MISMATCH")
            payload = self._custody.download(receipt.custody_id, owner=self._owner,
                                             revision_token=receipt.revision_token, filename=filename)
            artifact = next(item for item in export.artifacts if item.filename == filename)
            if len(payload) != artifact.size_bytes or hashlib.sha256(payload).hexdigest() != artifact.sha256:
                raise ProductWorkflowError("EXPORT_UNAVAILABLE")
            return payload

    def abort(self, ref: ProductSessionRef) -> None:
        with self._lock:
            receipt = self._get(ref)
            self._custody.abort(receipt.custody_id, owner=self._owner,
                                revision_token=receipt.revision_token)
            self._handles.pop(ref.session_id, None)

    def close(self) -> None:
        """Trusted host retirement, never a browser operation.

        The host has already revoked publication outside our locks. Wait for
        in-process work, then use retained custody credentials solely to revoke
        and dispose. No invocation authorization or result is reissued here.
        """
        with self._lock:
            for receipt in tuple(self._handles.values()):
                try:
                    self._custody.abort(receipt.custody_id, owner=self._owner,
                                        revision_token=receipt.revision_token)
                except CustodyError as exc:
                    if exc.code != "SESSION_UNAVAILABLE":
                        raise
            self._handles.clear()
            self._custody.sweep_expired()
            if self._custody.cleanup_failures:
                raise ProductWorkflowError("CLEANUP_FAILED")
