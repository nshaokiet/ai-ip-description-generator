"""Opt-in, process-local custody for synthetic offline USPTO drafts.

Only a trusted same-process caller may supply the owner context, synthetic
extraction runtime, review callback, and uploaded document identifier.  This
module exposes no transport or persistent authority.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import time
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path
from threading import RLock
from typing import Any, Callable, Protocol
from uuid import uuid4

from backend.app.schemas.analysis_input import ExtractionInputEnvelope
from backend.app.services.document_parsing import DocumentPreparationService, compute_sha256
from backend.app.services.document_registry import DocumentRegistry
from backend.app.services.document_storage import DocumentStorage
from backend.app.services.extraction_validation import (
    validate_canonical_output,
    validate_grounding_and_business_rules,
)
from backend.app.services.invention_reconstruction import reconstruct_invention
from backend.app.services.supported_draft_claims_generation import generate_supported_draft_claims
from backend.app.services.supported_draft_claims_validation import sha256_canonical
from backend.app.services.uspto_document_package import assemble_uspto_document_package
from backend.app.services.uspto_document_package_validation import (
    validate_assembly_inputs,
    validate_uspto_document_package,
)
from backend.app.services.uspto_offline_renderer import FILES, render_uspto_document_package
from backend.app.services.uspto_specification_generation import generate_uspto_specification


IDLE_SECONDS = 30 * 60
ABSOLUTE_SECONDS = 2 * 60 * 60
PROVENANCE_KEYS = (
    "source_envelope", "structured_analysis", "reconstruction", "specification",
    "p2_003_generation_config", "supported_claims", "p2_004_generation_config",
)
MIME = {
    ".pdf": "application/pdf",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


class SyntheticExtractionRuntime(Protocol):
    def run_extraction(self, envelope: ExtractionInputEnvelope, *, correlation_id: str | None = None) -> Any: ...


class CustodyError(RuntimeError):
    safe_message = "Synthetic source custody request was rejected."

    def __init__(self, code: str) -> None:
        super().__init__(self.safe_message)
        self.code = code


@dataclass(frozen=True, slots=True)
class ArtifactManifest:
    custody_id: str
    owner: str
    revision: int
    filename: str
    media_type: str
    size_bytes: int
    sha256: str


@dataclass(frozen=True, slots=True)
class ReviewAcknowledgment:
    custody_id: str
    owner: str
    actor: str
    context: str
    revision: int
    revision_token: str
    recorded_at_monotonic: float
    decision: str


@dataclass(frozen=True, slots=True)
class CustodyReceipt:
    custody_id: str
    document_id: str
    revision: int
    revision_token: str
    state: str
    source_sha256: str
    envelope_sha256: str
    analysis_sha256: str
    evidence_count: int
    claims_review_required: bool
    manifest: tuple[ArtifactManifest, ...]
    deadline_seconds: float
    synthetic_draft: bool = True
    filing_ready: bool = False


@dataclass(slots=True)
class _Record:
    custody_id: str
    owner: str
    document_id: str
    source_sha256: str
    originals: dict[str, Any]
    digests: dict[str, str]
    revision: int
    revision_token: str
    committed_at: float
    idle_deadline: float
    state: str = "REVIEW_PENDING"
    review: ReviewAcknowledgment | None = None
    claims_review: ReviewAcknowledgment | None = None
    package: dict[str, Any] | None = None
    manifest: tuple[ArtifactManifest, ...] = ()
    output_directory: Path | None = None
    lock: RLock = field(default_factory=RLock, repr=False)


class TrustedCustodyCoordinator:
    """Bounded volatile custody. Construction alone never enables execution."""

    def __init__(
        self, storage: DocumentStorage, registry: DocumentRegistry,
        preparation: DocumentPreparationService, *, output_root: Path,
        enabled: bool = False, clock: Callable[[], float] = time.monotonic,
        max_records: int = 32,
        review_authorizer: Callable[[str, str, str], bool] | None = None,
    ) -> None:
        if max_records < 1 or max_records > 256:
            raise ValueError("max_records must be between 1 and 256")
        self.storage = storage
        self.registry = registry
        self.preparation = preparation
        if output_root.is_symlink():
            raise ValueError("symlink output root is forbidden")
        self.output_root = output_root.resolve()
        self.enabled = enabled
        self.clock = clock
        self.max_records = max_records
        self.review_authorizer = review_authorizer
        self._records: dict[str, _Record] = {}
        self._intaking: set[str] = set()
        self._lock = RLock()
        self.cleanup_failures: list[str] = []  # sanitized opaque IDs only
        if enabled:
            self.output_root.mkdir(parents=True, exist_ok=True, mode=0o700)
            if self.output_root.is_symlink():
                raise ValueError("symlink output root is forbidden")

    def _enabled(self) -> None:
        if not self.enabled:
            raise CustodyError("CUSTODY_DISABLED")

    @staticmethod
    def _owner(owner: str) -> None:
        if type(owner) is not str or not owner or len(owner) > 128:
            raise CustodyError("SESSION_UNAVAILABLE")

    def commit_upload(
        self, document_id: str, *, owner: str,
        extraction_runtime: SyntheticExtractionRuntime,
        p2_003_generation_config: dict[str, Any],
        p2_004_generation_config: dict[str, Any],
    ) -> CustodyReceipt:
        """Validate actual leased APP-001 bytes and APP-002 envelope before cleanup."""
        self._enabled()
        self._owner(owner)
        if getattr(extraction_runtime, "synthetic_only", None) is not True:
            raise CustodyError("PROVIDER_BLOCKED")
        if type(document_id) is not str or not self.storage._is_document_id(document_id):
            raise CustodyError("SOURCE_MISSING")
        self.sweep_expired()
        with self._lock:
            if len(self._records) >= self.max_records:
                raise CustodyError("CUSTODY_CAPACITY")
            if document_id in self._intaking:
                raise CustodyError("INTAKE_CONFLICT")
            self._intaking.add(document_id)
        record = self.registry.get(document_id)
        if record is None:
            with self._lock:
                self._intaking.discard(document_id)
            raise CustodyError("SOURCE_MISSING")
        candidate: _Record | None = None
        try:
            with self.storage.lease(document_id) as path:
                if not path.is_file() or path.is_symlink():
                    raise CustodyError("SOURCE_MISSING")
                if compute_sha256(path) != record.sha256:
                    raise CustodyError("SOURCE_HASH_MISMATCH")
                if path.stat().st_size != record.size_bytes:
                    raise CustodyError("SOURCE_HASH_MISMATCH")
                envelope = self.preparation.prepare_extraction_input(document_id)
                metadata = envelope.document_metadata
                if (metadata.document_id != record.document_id or metadata.sha256 != record.sha256
                        or metadata.file_name != record.file_name or metadata.media_type != record.media_type):
                    raise CustodyError("SOURCE_HASH_MISMATCH")
                canonical_envelope = ExtractionInputEnvelope.model_validate(envelope.model_dump(mode="json"))
                if len({unit.evidence_id for unit in canonical_envelope.source_units}) != len(canonical_envelope.source_units):
                    raise CustodyError("EVIDENCE_INVALID")
                if compute_sha256(path) != record.sha256:
                    raise CustodyError("SOURCE_HASH_MISMATCH")
                result = extraction_runtime.run_extraction(canonical_envelope)
                analysis = deepcopy(result.analysis)
                schema = json.loads((Path(__file__).resolve().parents[3] / "schemas/invention-output/v1.0.0/invention-output.schema.json").read_text(encoding="utf-8"))
                validate_canonical_output(analysis, schema)
                validate_grounding_and_business_rules(analysis, canonical_envelope)
                # The actual upload may be replaced during a slow synthetic runtime.
                if compute_sha256(path) != record.sha256:
                    raise CustodyError("SOURCE_HASH_MISMATCH")
                source = canonical_envelope.model_dump(mode="json")
                originals = {
                    "source_envelope": source,
                    "structured_analysis": analysis,
                    "p2_003_generation_config": deepcopy(p2_003_generation_config),
                    "p2_004_generation_config": deepcopy(p2_004_generation_config),
                }
                self._derive(originals)
                digests = {key: sha256_canonical(originals[key]) for key in PROVENANCE_KEYS}
                custody_id = uuid4().hex
                now = self.clock()
                candidate = _Record(
                    custody_id=custody_id, owner=owner, document_id=record.document_id,
                    source_sha256=record.sha256, originals=deepcopy(originals),
                    digests=digests, revision=1, revision_token=uuid4().hex,
                    committed_at=now, idle_deadline=now + IDLE_SECONDS,
                )
                with self._lock:
                    if len(self._records) >= self.max_records:
                        raise CustodyError("CUSTODY_CAPACITY")
                    self._records[custody_id] = candidate
            # The envelope is already retained. A failed unlink revokes custody.
            if not self.storage.delete(document_id):
                with candidate.lock:
                    self._revoke(candidate, "ABORTED")
                raise CustodyError("CLEANUP_FAILED")
            return self._receipt(candidate)
        except CustodyError:
            if candidate is not None:
                with candidate.lock:
                    self._revoke(candidate, "ABORTED")
            if not self.storage.delete(document_id):
                self.cleanup_failures.append("upload")
            raise
        except Exception:
            if candidate is not None:
                with candidate.lock:
                    self._revoke(candidate, "ABORTED")
            if not self.storage.delete(document_id):
                self.cleanup_failures.append("upload")
            raise CustodyError("INTAKE_REJECTED") from None
        finally:
            with self._lock:
                self._intaking.discard(document_id)

    def sweep_expired(self) -> int:
        """Revoke expired records and reclaim bounded volatile capacity."""
        with self._lock:
            records = tuple(self._records.values())
        count = 0
        for record in records:
            with record.lock:
                if record.state in {"EXPIRED", "ABORTED"}:
                    expired = True
                else:
                    expired = self.clock() >= min(record.idle_deadline, record.committed_at + ABSOLUTE_SECONDS)
                    if expired:
                        self._revoke(record, "EXPIRED")
                if expired:
                    if record.output_directory is not None:
                        self._cleanup_output(record)
                    if record.output_directory is not None:
                        continue
                    with self._lock:
                        if self._records.get(record.custody_id) is record:
                            del self._records[record.custody_id]
                            count += 1
        return count

    @staticmethod
    def _derive(originals: dict[str, Any]) -> None:
        reconstruction = reconstruct_invention(originals["source_envelope"], originals["structured_analysis"])
        specification = generate_uspto_specification(reconstruction, originals["p2_003_generation_config"])
        claims = generate_supported_draft_claims(
            reconstruction, specification, originals["p2_004_generation_config"]
        )
        originals.update(reconstruction=reconstruction, specification=specification, supported_claims=claims)
        validate_assembly_inputs(**originals)

    def _find(self, custody_id: str) -> _Record:
        self._enabled()
        if type(custody_id) is not str or len(custody_id) != 32 or any(c not in "0123456789abcdef" for c in custody_id):
            raise CustodyError("SESSION_UNAVAILABLE")
        with self._lock:
            record = self._records.get(custody_id)
        if record is None:
            raise CustodyError("SESSION_UNAVAILABLE")
        return record

    def _require(self, record: _Record, owner: str, token: str) -> None:
        if record.state in {"EXPIRED", "ABORTED"}:
            raise CustodyError("SESSION_UNAVAILABLE")
        if self.clock() >= min(record.idle_deadline, record.committed_at + ABSOLUTE_SECONDS):
            self._revoke(record, "EXPIRED")
            raise CustodyError("SESSION_UNAVAILABLE")
        if owner != record.owner:
            raise CustodyError("SESSION_UNAVAILABLE")
        if type(token) is not str or token != record.revision_token:
            raise CustodyError("STALE_REVISION")
        try:
            self._validate_originals(record)
        except CustodyError:
            self._revoke(record, "ABORTED")
            raise
        if record.manifest:
            self._validate_manifest(record)
        if self.clock() >= min(record.idle_deadline, record.committed_at + ABSOLUTE_SECONDS):
            self._revoke(record, "EXPIRED")
            raise CustodyError("SESSION_UNAVAILABLE")

    def _validate_manifest(self, record: _Record) -> None:
        try:
            if (record.package is None or record.output_directory is None
                    or {item.filename for item in record.manifest} != set(FILES)):
                raise ValueError("manifest incomplete")
            directory = record.output_directory / (record.package["package_id"] + "-p2-006")
            if directory.is_symlink() or {item.name for item in directory.iterdir()} != set(FILES):
                raise ValueError("artifact directory invalid")
            for item in record.manifest:
                if item.custody_id != record.custody_id or item.owner != record.owner or item.revision != record.revision:
                    raise ValueError("manifest authority invalid")
                path = directory / item.filename
                if path.is_symlink() or not path.is_file() or path.stat().st_size != item.size_bytes:
                    raise ValueError("artifact invalid")
                if compute_sha256(path) != item.sha256:
                    raise ValueError("artifact digest invalid")
        except Exception:
            self._revoke(record, "ABORTED")
            raise CustodyError("EXPORT_UNAVAILABLE") from None

    @staticmethod
    def _validate_originals(record: _Record) -> None:
        if set(record.originals) != set(PROVENANCE_KEYS):
            raise CustodyError("PROVENANCE_MISMATCH")
        try:
            if any(sha256_canonical(record.originals[key]) != record.digests[key] for key in PROVENANCE_KEYS):
                raise CustodyError("PROVENANCE_MISMATCH")
            metadata = record.originals["source_envelope"]["document_metadata"]
            if metadata["document_id"] != record.document_id or metadata["sha256"] != record.source_sha256:
                raise CustodyError("PROVENANCE_MISMATCH")
            validate_assembly_inputs(**record.originals)
        except CustodyError:
            raise
        except Exception:
            raise CustodyError("PROVENANCE_MISMATCH") from None

    def _refresh(self, record: _Record) -> None:
        now = self.clock()
        if now >= min(record.idle_deadline, record.committed_at + ABSOLUTE_SECONDS):
            self._revoke(record, "EXPIRED")
            raise CustodyError("SESSION_UNAVAILABLE")
        record.idle_deadline = min(now + IDLE_SECONDS, record.committed_at + ABSOLUTE_SECONDS)

    def _receipt(self, record: _Record) -> CustodyReceipt:
        return CustodyReceipt(
            custody_id=record.custody_id, document_id=record.document_id,
            revision=record.revision, revision_token=record.revision_token,
            state=record.state, source_sha256=record.source_sha256,
            envelope_sha256=record.digests.get("source_envelope", ""),
            analysis_sha256=record.digests.get("structured_analysis", ""),
            evidence_count=len(record.originals.get("source_envelope", {}).get("source_units", [])),
            claims_review_required=self._claims_incomplete(record),
            manifest=record.manifest,
            deadline_seconds=min(record.idle_deadline, record.committed_at + ABSOLUTE_SECONDS),
        )

    @staticmethod
    def _claims_incomplete(record: _Record) -> bool:
        claims = record.originals.get("supported_claims", {})
        return (not claims.get("claims") or claims.get("status") != "PRESENT"
                or any(item.get("status") != "PRESENT" for item in claims.get("claim_families", ())))

    def status(self, custody_id: str, *, owner: str, revision_token: str) -> CustodyReceipt:
        record = self._find(custody_id)
        with record.lock:
            self._require(record, owner, revision_token)
            return self._receipt(record)  # read never refreshes idle TTL

    def revise(
        self, custody_id: str, *, owner: str, revision_token: str,
        structured_analysis: dict[str, Any] | None = None,
        p2_003_generation_config: dict[str, Any] | None = None,
        p2_004_generation_config: dict[str, Any] | None = None,
    ) -> CustodyReceipt:
        record = self._find(custody_id)
        with record.lock:
            self._require(record, owner, revision_token)
            candidate = deepcopy(record.originals)
            if structured_analysis is not None:
                candidate["structured_analysis"] = deepcopy(structured_analysis)
            if p2_003_generation_config is not None:
                candidate["p2_003_generation_config"] = deepcopy(p2_003_generation_config)
                candidate["p2_004_generation_config"]["p2_003_generation_config"] = deepcopy(p2_003_generation_config)
            if p2_004_generation_config is not None:
                candidate["p2_004_generation_config"] = deepcopy(p2_004_generation_config)
            if all(candidate[key] == record.originals[key] for key in ("structured_analysis", "p2_003_generation_config", "p2_004_generation_config")):
                raise CustodyError("REVISION_UNCHANGED")
            for key in ("reconstruction", "specification", "supported_claims"):
                candidate.pop(key)
            try:
                self._derive(candidate)
                digests = {key: sha256_canonical(candidate[key]) for key in PROVENANCE_KEYS}
            except Exception:
                raise CustodyError("INVALID_REVISION_INPUT") from None
            # Revoke the old manifest before touching its files.
            record.manifest = ()
            record.review = None
            record.claims_review = None
            record.package = None
            if not self._cleanup_output(record):
                self._revoke(record, "ABORTED")
                raise CustodyError("CLEANUP_FAILED")
            record.originals = candidate
            record.digests = digests
            record.revision += 1
            record.revision_token = uuid4().hex
            record.state = "REVIEW_PENDING"
            self._refresh(record)
            return self._receipt(record)

    def acknowledge_review(
        self, custody_id: str, *, owner: str, revision_token: str,
        actor: str, context: str,
    ) -> CustodyReceipt:
        record = self._find(custody_id)
        with record.lock:
            self._require(record, owner, revision_token)
            if record.state != "REVIEW_PENDING":
                raise CustodyError("INVALID_STATE")
            if not self._authorized_review(actor, context, "CONTENT_REVIEW_ACKNOWLEDGED"):
                raise CustodyError("REVIEW_REQUIRED")
            record.review = ReviewAcknowledgment(record.custody_id, owner, actor, context, record.revision, record.revision_token, self.clock(), "CONTENT_REVIEW_ACKNOWLEDGED")
            record.state = "CLAIMS_REVIEW_REQUIRED" if self._claims_incomplete(record) else "REVIEW_RECORDED"
            self._refresh(record)
            return self._receipt(record)

    def acknowledge_incomplete_claims(
        self, custody_id: str, *, owner: str, revision_token: str,
        actor: str, context: str, acknowledge: bool,
    ) -> CustodyReceipt:
        record = self._find(custody_id)
        with record.lock:
            self._require(record, owner, revision_token)
            if record.state != "CLAIMS_REVIEW_REQUIRED" or record.review is None:
                raise CustodyError("INVALID_STATE")
            if acknowledge is not True or not self._authorized_review(actor, context, "CLAIMS_INCOMPLETE_ACKNOWLEDGED"):
                raise CustodyError("CLAIMS_REVIEW_REQUIRED")
            record.claims_review = ReviewAcknowledgment(record.custody_id, owner, actor, context, record.revision, record.revision_token, self.clock(), "CLAIMS_INCOMPLETE_ACKNOWLEDGED")
            record.state = "REVIEW_RECORDED"
            self._refresh(record)
            return self._receipt(record)

    def _authorized_review(self, actor: str, context: str, decision: str) -> bool:
        if type(actor) is not str or type(context) is not str or not actor.strip() or not context.strip() or self.review_authorizer is None:
            return False
        try:
            return self.review_authorizer(actor, context, decision) is True
        except Exception:
            return False

    def render(self, custody_id: str, *, owner: str, revision_token: str) -> CustodyReceipt:
        record = self._find(custody_id)
        with record.lock:
            self._require(record, owner, revision_token)
            if record.state != "REVIEW_RECORDED" or record.review is None:
                raise CustodyError("REVIEW_REQUIRED")
            if record.review.revision != record.revision or record.review.revision_token != record.revision_token:
                raise CustodyError("STALE_REVISION")
            if self._claims_incomplete(record) and (
                record.claims_review is None or record.claims_review.revision != record.revision
                or record.claims_review.revision_token != record.revision_token
            ):
                raise CustodyError("CLAIMS_REVIEW_REQUIRED")
            self._validate_originals(record)
            try:
                package = assemble_uspto_document_package(**deepcopy(record.originals))
                validate_uspto_document_package(package, **deepcopy(record.originals))
                parent = self.output_root / record.custody_id
                parent.mkdir(mode=0o700)
                record.output_directory = parent
                outputs = render_uspto_document_package(package, **deepcopy(record.originals), output_dir=parent)
                self._validate_originals(record)
                validate_uspto_document_package(package, **deepcopy(record.originals))
                manifest = []
                for name in FILES:
                    path = outputs[name]
                    if path.is_symlink() or path.stat().st_size == 0:
                        raise CustodyError("RENDER_INCOMPLETE")
                    with path.open("rb") as stream:
                        signature = stream.read(4)
                    if signature != (b"%PDF" if name.endswith(".pdf") else b"PK\x03\x04"):
                        raise CustodyError("RENDER_INCOMPLETE")
                    manifest.append(ArtifactManifest(record.custody_id, record.owner, record.revision, name, MIME[path.suffix], path.stat().st_size, compute_sha256(path)))
                if self.clock() >= min(record.idle_deadline, record.committed_at + ABSOLUTE_SECONDS):
                    self._revoke(record, "EXPIRED")
                    raise CustodyError("SESSION_UNAVAILABLE")
                record.package = package
                record.manifest = tuple(manifest)
                record.state = "RENDERED"
                self._refresh(record)
                return self._receipt(record)
            except CustodyError:
                if record.state not in {"EXPIRED", "ABORTED"} and not self._cleanup_output(record):
                    self._revoke(record, "ABORTED")
                    raise CustodyError("CLEANUP_FAILED") from None
                raise
            except Exception:
                if not self._cleanup_output(record):
                    self._revoke(record, "ABORTED")
                    raise CustodyError("CLEANUP_FAILED") from None
                raise CustodyError("RENDER_INCOMPLETE") from None

    def download(self, custody_id: str, *, owner: str, revision_token: str, filename: str) -> bytes:
        record = self._find(custody_id)
        with record.lock:
            self._require(record, owner, revision_token)
            if record.state not in {"RENDERED", "DOWNLOADED"} or filename not in FILES:
                raise CustodyError("EXPORT_UNAVAILABLE")
            if record.package is None or len(record.manifest) != len(FILES):
                raise CustodyError("EXPORT_UNAVAILABLE")
            validate_uspto_document_package(record.package, **deepcopy(record.originals))
            entry = next((item for item in record.manifest if item.filename == filename), None)
            if entry is None or record.output_directory is None:
                raise CustodyError("EXPORT_UNAVAILABLE")
            path = record.output_directory / (record.package["package_id"] + "-p2-006") / filename
            if path.is_symlink() or not path.is_file():
                raise CustodyError("EXPORT_UNAVAILABLE")
            data = path.read_bytes()
            if len(data) != entry.size_bytes or hashlib.sha256(data).hexdigest() != entry.sha256:
                raise CustodyError("EXPORT_UNAVAILABLE")
            record.state = "DOWNLOADED"
            self._refresh(record)
            return data

    def abort(self, custody_id: str, *, owner: str, revision_token: str) -> None:
        record = self._find(custody_id)
        with record.lock:
            self._require(record, owner, revision_token)
            self._revoke(record, "ABORTED")

    def _cleanup_output(self, record: _Record) -> bool:
        directory = record.output_directory
        if directory is None:
            return True
        if directory.parent != self.output_root or directory.name != record.custody_id or directory.is_symlink():
            self.cleanup_failures.append(record.custody_id)
            return False
        try:
            shutil.rmtree(directory)
            record.output_directory = None
            return True
        except OSError:
            self.cleanup_failures.append(record.custody_id)
            return False

    def _revoke(self, record: _Record, state: str) -> None:
        record.state = state
        record.revision_token = ""
        record.review = None
        record.claims_review = None
        record.manifest = ()
        record.package = None
        record.originals.clear()
        record.digests.clear()
        self._cleanup_output(record)
