"""Private deterministic orchestration for the released USPTO v2 stages.

The service keeps source material and all seven P2-005/P2-006 provenance
objects in an in-memory session.  It intentionally exposes no HTTP route and
does not call a provider, network service, database, or persistent store.
"""

from __future__ import annotations

import hashlib
import math
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from threading import RLock
from typing import Any, Callable
from uuid import uuid4

from backend.app.schemas.analysis_input import ExtractionInputEnvelope
from backend.app.services.invention_reconstruction import reconstruct_invention
from backend.app.services.supported_draft_claims_generation import (
    generate_supported_draft_claims,
)
from backend.app.services.supported_draft_claims_validation import (
    sha256_canonical,
    validate_generation_config as validate_p4_config,
)
from backend.app.services.uspto_specification_generation_validation import (
    validate_generated_specification,
    validate_generation_config as validate_p3_config,
)
from backend.app.services.uspto_document_package import (
    assemble_uspto_document_package,
)
from backend.app.services.uspto_document_package_validation import (
    validate_uspto_document_package,
)
from backend.app.services.uspto_offline_renderer import (
    FILES,
    render_uspto_document_package,
)
from backend.app.services.uspto_specification_generation import (
    generate_uspto_specification,
)


ORCHESTRATION_CONTRACT_VERSION = "1.0.1"
PROVENANCE_KEYS = (
    "source_envelope",
    "structured_analysis",
    "reconstruction",
    "specification",
    "p2_003_generation_config",
    "supported_claims",
    "p2_004_generation_config",
)
STATES = (
    "SOURCE_READY",
    "RECONSTRUCTION_READY",
    "SPECIFICATION_READY",
    "CLAIMS_READY",
    "CLAIMS_REVIEW_REQUIRED",
    "PACKAGE_VALID",
    "RENDERED",
    "FAILED",
)
_UNSET = object()


class USPTOOfflineOrchestrationError(RuntimeError):
    """Stable, source-safe orchestration failure."""

    safe_message = "Offline USPTO orchestration failed."

    def __init__(
        self,
        code: str,
        *,
        stage: str,
        paths: tuple[str, ...] = (),
        session_id: str | None = None,
        revision: int | None = None,
        upstream_code: str | None = None,
    ) -> None:
        super().__init__(self.safe_message)
        self.code = code
        self.stage = stage
        self.paths = tuple(sorted(set(paths)))
        self.session_id = session_id
        self.revision = revision
        self.upstream_code = upstream_code


@dataclass(frozen=True, slots=True)
class RenderArtifact:
    """Path-free render metadata suitable for an internal status response."""

    filename: str
    sha256: str
    size_bytes: int


@dataclass(frozen=True, slots=True)
class OrchestrationStatus:
    """Safe session status; source content and server paths are excluded."""

    session_id: str
    revision: int
    revision_token: str
    contract_version: str
    state: str
    document_id: str
    source_sha256: str
    artifact_digests: tuple[tuple[str, str], ...]
    retained_provenance_keys: tuple[str, ...]
    package_id: str | None
    render_manifest: tuple[RenderArtifact, ...]
    created_at: str
    updated_at: str
    error_code: str | None
    error_paths: tuple[str, ...]


@dataclass(slots=True)
class _SessionRecord:
    session_id: str
    revision: int
    revision_token: str
    state: str
    document_id: str
    source_sha256: str
    source_envelope: dict[str, Any]
    structured_analysis: dict[str, Any]
    p2_003_generation_config: dict[str, Any]
    p2_004_generation_config: dict[str, Any]
    reconstruction: dict[str, Any] | None = None
    specification: dict[str, Any] | None = None
    supported_claims: dict[str, Any] | None = None
    package: dict[str, Any] | None = None
    artifact_digests: dict[str, str] = field(default_factory=dict)
    render_directory: Path | None = None
    render_manifest: tuple[RenderArtifact, ...] = ()
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    error_code: str | None = None
    error_paths: tuple[str, ...] = ()


class OfflineUSPTOOrchestrator:
    """Bounded, ephemeral session manager for the released offline pipeline."""

    def __init__(
        self,
        *,
        max_sessions: int = 32,
        session_id_factory: Callable[[], str] | None = None,
    ) -> None:
        if type(max_sessions) is not int or max_sessions < 1 or max_sessions > 256:
            raise ValueError("max_sessions must be an integer from 1 through 256")
        self._max_sessions = max_sessions
        self._session_id_factory = session_id_factory or (lambda: uuid4().hex)
        self._sessions: dict[str, _SessionRecord] = {}
        self._lock = RLock()

    def start_session(
        self,
        *,
        source_envelope: ExtractionInputEnvelope | dict[str, Any],
        structured_analysis: dict[str, Any],
        p2_003_generation_config: dict[str, Any],
        p2_004_generation_config: dict[str, Any],
    ) -> OrchestrationStatus:
        """Create a SOURCE_READY revision without executing downstream stages."""

        envelope = _canonical_envelope(source_envelope)
        analysis = _require_dict(structured_analysis, "/structured_analysis")
        p3_config = _require_dict(
            p2_003_generation_config, "/p2_003_generation_config"
        )
        p4_config = _require_dict(
            p2_004_generation_config, "/p2_004_generation_config"
        )
        initial = {
            "source_envelope": envelope,
            "structured_analysis": analysis,
            "p2_003_generation_config": p3_config,
            "p2_004_generation_config": p4_config,
        }
        try:
            digests = {name: sha256_canonical(value) for name, value in initial.items()}
        except Exception:
            raise USPTOOfflineOrchestrationError(
                "INVALID_CANONICAL_INPUT",
                stage="session",
                paths=("/source_envelope", "/structured_analysis", "/generation_config"),
            ) from None

        with self._lock:
            if len(self._sessions) >= self._max_sessions:
                raise USPTOOfflineOrchestrationError(
                    "SESSION_CAPACITY_EXCEEDED", stage="session"
                )
            session_id = self._new_session_id()
            metadata = envelope["document_metadata"]
            token = _revision_token(session_id, 1, digests)
            now = datetime.now(timezone.utc)
            record = _SessionRecord(
                session_id=session_id,
                revision=1,
                revision_token=token,
                state="SOURCE_READY",
                document_id=metadata["document_id"],
                source_sha256=metadata["sha256"],
                source_envelope=envelope,
                structured_analysis=analysis,
                p2_003_generation_config=p3_config,
                p2_004_generation_config=p4_config,
                artifact_digests=digests,
                created_at=now,
                updated_at=now,
            )
            self._sessions[session_id] = record
            return _status(record)

    def run_uspto_v2_offline_pipeline(
        self,
        *,
        source_envelope: ExtractionInputEnvelope | dict[str, Any],
        structured_analysis: dict[str, Any],
        p2_003_generation_config: dict[str, Any],
        p2_004_generation_config: dict[str, Any],
        output_dir: Path | str | None = None,
    ) -> OrchestrationStatus:
        """Create and advance one session through P2-005 and optional P2-006."""

        status = self.start_session(
            source_envelope=source_envelope,
            structured_analysis=structured_analysis,
            p2_003_generation_config=p2_003_generation_config,
            p2_004_generation_config=p2_004_generation_config,
        )
        return self.advance_session(
            status.session_id,
            expected_revision_token=status.revision_token,
            output_dir=output_dir,
        )

    def advance_session(
        self,
        session_id: str,
        *,
        expected_revision_token: str,
        output_dir: Path | str | None = None,
    ) -> OrchestrationStatus:
        """Advance monotonically to PACKAGE_VALID, then optionally RENDERED."""

        with self._lock:
            record = self._require_current(session_id, expected_revision_token)
            self._verify_integrity(record)
            if record.state == "FAILED":
                raise USPTOOfflineOrchestrationError(
                    "SESSION_FAILED",
                    stage="session",
                    session_id=record.session_id,
                    revision=record.revision,
                )

            if record.state == "SOURCE_READY":
                reconstruction = self._execute(
                    record,
                    stage="P2_002",
                    code="P2_002_REJECTED",
                    action=lambda: reconstruct_invention(
                        record.source_envelope, record.structured_analysis
                    ),
                )
                record.reconstruction = deepcopy(reconstruction)
                self._record_json_digest(record, "reconstruction", reconstruction)
                self._transition(record, "RECONSTRUCTION_READY")

            if record.state == "RECONSTRUCTION_READY":
                specification = self._execute(
                    record,
                    stage="P2_003",
                    code="P2_003_REJECTED",
                    action=lambda: generate_uspto_specification(
                        record.reconstruction,
                        record.p2_003_generation_config,
                    ),
                )
                record.specification = deepcopy(specification)
                self._record_json_digest(record, "specification", specification)
                self._transition(record, "SPECIFICATION_READY")

            if record.state == "SPECIFICATION_READY":
                supported_claims = self._execute(
                    record,
                    stage="P2_004",
                    code="P2_004_REJECTED",
                    action=lambda: generate_supported_draft_claims(
                        record.reconstruction,
                        record.specification,
                        record.p2_004_generation_config,
                    ),
                )
                record.supported_claims = deepcopy(supported_claims)
                self._record_json_digest(record, "supported_claims", supported_claims)
                claims_state = (
                    "CLAIMS_READY"
                    if supported_claims["claims"]
                    else "CLAIMS_REVIEW_REQUIRED"
                )
                self._transition(record, claims_state)

            if record.state in {"CLAIMS_READY", "CLAIMS_REVIEW_REQUIRED"}:
                bundle = self._provenance_bundle(record)
                package = self._execute(
                    record,
                    stage="P2_005",
                    code="P2_005_REJECTED",
                    action=lambda: assemble_uspto_document_package(**bundle),
                )
                self._execute(
                    record,
                    stage="P2_005_VALIDATION",
                    code="P2_005_VALIDATION_REJECTED",
                    action=lambda: validate_uspto_document_package(
                        package, **bundle
                    ),
                )
                record.package = deepcopy(package)
                self._record_json_digest(record, "package", package)
                self._transition(record, "PACKAGE_VALID")

            if output_dir is not None and record.state == "PACKAGE_VALID":
                self._render(record, output_dir)
            elif output_dir is not None and record.state == "RENDERED":
                raise USPTOOfflineOrchestrationError(
                    "RENDER_ALREADY_COMPLETED",
                    stage="P2_006",
                    paths=("/output_dir",),
                    session_id=record.session_id,
                    revision=record.revision,
                )
            return _status(record)

    def validate_session(
        self, session_id: str, *, expected_revision_token: str
    ) -> OrchestrationStatus:
        """Revalidate the package using the retained seven-input bundle."""

        with self._lock:
            record = self._require_current(session_id, expected_revision_token)
            self._verify_integrity(record)
            if record.package is None:
                raise USPTOOfflineOrchestrationError(
                    "PACKAGE_NOT_READY",
                    stage="P2_005_VALIDATION",
                    paths=("/package",),
                    session_id=record.session_id,
                    revision=record.revision,
                )
            bundle = self._provenance_bundle(record)
            self._execute(
                record,
                stage="P2_005_VALIDATION",
                code="P2_005_VALIDATION_REJECTED",
                action=lambda: validate_uspto_document_package(
                    record.package, **bundle
                ),
            )
            return _status(record)

    def render_session(
        self,
        session_id: str,
        *,
        expected_revision_token: str,
        output_dir: Path | str,
    ) -> OrchestrationStatus:
        """Render only from a current validated session, never from package alone."""

        with self._lock:
            record = self._require_current(session_id, expected_revision_token)
            self._verify_integrity(record)
            if record.state != "PACKAGE_VALID" or record.package is None:
                raise USPTOOfflineOrchestrationError(
                    "PACKAGE_NOT_READY",
                    stage="P2_006",
                    paths=("/package",),
                    session_id=record.session_id,
                    revision=record.revision,
                )
            self._render(record, output_dir)
            return _status(record)

    def revise_session(
        self,
        session_id: str,
        *,
        expected_revision_token: str,
        source_envelope: ExtractionInputEnvelope | dict[str, Any] | object = _UNSET,
        structured_analysis: dict[str, Any] | object = _UNSET,
        p2_003_generation_config: dict[str, Any] | object = _UNSET,
        p2_004_generation_config: dict[str, Any] | object = _UNSET,
    ) -> OrchestrationStatus:
        """Create a new revision and invalidate every affected downstream stage."""

        with self._lock:
            record = self._require_current(session_id, expected_revision_token)
            self._verify_integrity(record)
            # Reject non-JSON values before copying or model coercion. Preparing
            # a rejected revision must never mutate the live record or files.
            for value in (
                source_envelope, structured_analysis,
                p2_003_generation_config, p2_004_generation_config,
            ):
                if value is not _UNSET:
                    _validate_revision_json(
                        value.model_dump(mode="python")
                        if isinstance(value, ExtractionInputEnvelope) else value
                    )
            next_envelope = (
                record.source_envelope
                if source_envelope is _UNSET
                else _canonical_envelope(source_envelope)
            )
            next_analysis = (
                record.structured_analysis
                if structured_analysis is _UNSET
                else _require_dict(structured_analysis, "/structured_analysis")
            )
            next_p3 = (
                record.p2_003_generation_config
                if p2_003_generation_config is _UNSET
                else _require_dict(
                    p2_003_generation_config, "/p2_003_generation_config"
                )
            )
            next_p4 = (
                record.p2_004_generation_config
                if p2_004_generation_config is _UNSET
                else _require_dict(
                    p2_004_generation_config, "/p2_004_generation_config"
                )
            )
            source_changed = (
                next_envelope != record.source_envelope
                or next_analysis != record.structured_analysis
            )
            p3_changed = next_p3 != record.p2_003_generation_config
            p4_changed = next_p4 != record.p2_004_generation_config
            if not (source_changed or p3_changed or p4_changed):
                return _status(record)

            candidate = deepcopy(record)
            candidate.source_envelope = deepcopy(next_envelope)
            candidate.structured_analysis = deepcopy(next_analysis)
            candidate.p2_003_generation_config = deepcopy(next_p3)
            candidate.p2_004_generation_config = deepcopy(next_p4)
            if source_changed:
                metadata = next_envelope["document_metadata"]
                candidate.document_id = metadata["document_id"]
                candidate.source_sha256 = metadata["sha256"]
                candidate.reconstruction = None
                candidate.specification = None
            elif p3_changed:
                candidate.specification = None
            candidate.supported_claims = None
            candidate.package = None
            if candidate.reconstruction is None:
                candidate.specification = None
                candidate.state = "SOURCE_READY"
            elif candidate.specification is None:
                candidate.state = "RECONSTRUCTION_READY"
            else:
                candidate.state = "SPECIFICATION_READY"
            candidate.revision += 1
            candidate.error_code = None
            candidate.error_paths = ()
            candidate.render_directory = None
            candidate.render_manifest = ()
            try:
                for key in (
                    "source_envelope", "structured_analysis",
                    "p2_003_generation_config", "p2_004_generation_config",
                ):
                    _validate_revision_json(getattr(candidate, key))
                # Validate all root inputs using released contracts, including
                # selections when upstream stages have not yet been executed.
                expected = reconstruct_invention(
                    candidate.source_envelope, candidate.structured_analysis
                )
                p3 = validate_p3_config(candidate.p2_003_generation_config, expected)
                p4 = validate_p4_config(candidate.p2_004_generation_config, expected)
                if p3 != p4["p2_003_generation_config"]:
                    raise ValueError("inconsistent configs")
                if candidate.reconstruction is not None:
                    if candidate.reconstruction != expected:
                        raise ValueError("invalid retained reconstruction")
                if candidate.specification is not None:
                    validate_generated_specification(candidate.specification, expected, p3)
                candidate.artifact_digests = self._current_json_digests(candidate)
                candidate.revision_token = _revision_token(
                    candidate.session_id, candidate.revision, candidate.artifact_digests
                )
                candidate.updated_at = datetime.now(timezone.utc)
                prepared_status = _status(candidate)
            except Exception:
                raise USPTOOfflineOrchestrationError(
                    "INVALID_REVISION_INPUT", stage="session", paths=("/revision",),
                    session_id=record.session_id, revision=record.revision,
                ) from None

            # Cleanup may fail after some files were removed. The existing
            # helper explicitly marks the old revision FAILED/CLEANUP_FAILED;
            # never publish a candidate or claim rollback of filesystem writes.
            self._remove_render_output(record)
            self._sessions[session_id] = candidate
            return prepared_status

    def get_session_status(self, session_id: str) -> OrchestrationStatus:
        """Return path-free status metadata without source or generated prose."""

        with self._lock:
            record = self._require_session(session_id)
            self._verify_integrity(record)
            return _status(record)

    def get_validated_package(
        self, session_id: str, *, expected_revision_token: str
    ) -> dict[str, Any]:
        """Return a mutation-isolated package after complete seven-input validation."""

        with self._lock:
            record = self._require_current(session_id, expected_revision_token)
            self._verify_integrity(record)
            if record.package is None:
                raise USPTOOfflineOrchestrationError(
                    "PACKAGE_NOT_READY",
                    stage="P2_005_VALIDATION",
                    paths=("/package",),
                    session_id=record.session_id,
                    revision=record.revision,
                )
            bundle = self._provenance_bundle(record)
            self._execute(
                record,
                stage="P2_005_VALIDATION",
                code="P2_005_VALIDATION_REJECTED",
                action=lambda: validate_uspto_document_package(
                    record.package, **bundle
                ),
            )
            return deepcopy(record.package)

    def cleanup_session(
        self, session_id: str, *, expected_revision_token: str
    ) -> None:
        """Delete bounded render artifacts and forget the ephemeral session."""

        with self._lock:
            record = self._require_current(session_id, expected_revision_token)
            self._verify_integrity(record)
            self._remove_render_output(record)
            del self._sessions[session_id]

    def _new_session_id(self) -> str:
        for _ in range(4):
            candidate = self._session_id_factory()
            if (
                type(candidate) is str
                and candidate
                and len(candidate) <= 128
                and candidate not in self._sessions
            ):
                return candidate
        raise USPTOOfflineOrchestrationError(
            "SESSION_ID_GENERATION_FAILED", stage="session"
        )

    def _require_session(self, session_id: str) -> _SessionRecord:
        if type(session_id) is not str or session_id not in self._sessions:
            raise USPTOOfflineOrchestrationError(
                "SESSION_NOT_FOUND", stage="session", paths=("/session_id",)
            )
        return self._sessions[session_id]

    def _require_current(
        self, session_id: str, expected_revision_token: str
    ) -> _SessionRecord:
        record = self._require_session(session_id)
        if (
            type(expected_revision_token) is not str
            or expected_revision_token != record.revision_token
        ):
            raise USPTOOfflineOrchestrationError(
                "STALE_REVISION",
                stage="session",
                paths=("/revision_token",),
                session_id=record.session_id,
                revision=record.revision,
            )
        return record

    def _verify_integrity(self, record: _SessionRecord) -> None:
        if type(record.source_envelope) is not dict:
            self._fail(
                record,
                "SOURCE_IDENTITY_MISMATCH",
                stage="session",
                paths=("/source_envelope/document_metadata",),
            )
        metadata = record.source_envelope.get("document_metadata", {})
        if (
            metadata.get("document_id") != record.document_id
            or metadata.get("sha256") != record.source_sha256
        ):
            self._fail(
                record,
                "SOURCE_IDENTITY_MISMATCH",
                stage="session",
                paths=("/source_envelope/document_metadata",),
            )
        try:
            current = self._current_json_digests(record)
            if record.render_directory is not None:
                current.update(self._render_digests(record))
        except USPTOOfflineOrchestrationError as exc:
            self._fail(
                record,
                exc.code,
                stage=exc.stage,
                paths=exc.paths,
                upstream_code=exc.upstream_code,
            )
        except Exception:
            self._fail(
                record,
                "SESSION_INTEGRITY_MISMATCH",
                stage="session",
                paths=("/artifact_digests",),
            )
        if current != record.artifact_digests:
            self._fail(
                record,
                "SESSION_INTEGRITY_MISMATCH",
                stage="session",
                paths=("/artifact_digests",),
            )

    def _current_json_digests(self, record: _SessionRecord) -> dict[str, str]:
        values = {
            "source_envelope": record.source_envelope,
            "structured_analysis": record.structured_analysis,
            "p2_003_generation_config": record.p2_003_generation_config,
            "p2_004_generation_config": record.p2_004_generation_config,
            "reconstruction": record.reconstruction,
            "specification": record.specification,
            "supported_claims": record.supported_claims,
            "package": record.package,
        }
        return {
            name: sha256_canonical(value)
            for name, value in values.items()
            if value is not None
        }

    def _record_json_digest(
        self, record: _SessionRecord, name: str, value: dict[str, Any]
    ) -> None:
        record.artifact_digests[name] = sha256_canonical(value)

    def _transition(self, record: _SessionRecord, target: str) -> None:
        allowed = {
            "SOURCE_READY": {"RECONSTRUCTION_READY"},
            "RECONSTRUCTION_READY": {"SPECIFICATION_READY"},
            "SPECIFICATION_READY": {"CLAIMS_READY", "CLAIMS_REVIEW_REQUIRED"},
            "CLAIMS_READY": {"PACKAGE_VALID"},
            "CLAIMS_REVIEW_REQUIRED": {"PACKAGE_VALID"},
            "PACKAGE_VALID": {"RENDERED"},
        }
        if target not in allowed.get(record.state, set()):
            self._fail(
                record,
                "INVALID_STATE_TRANSITION",
                stage="session",
                paths=("/state",),
            )
        record.state = target
        record.updated_at = datetime.now(timezone.utc)

    def _provenance_bundle(self, record: _SessionRecord) -> dict[str, Any]:
        values = {
            "source_envelope": record.source_envelope,
            "structured_analysis": record.structured_analysis,
            "reconstruction": record.reconstruction,
            "specification": record.specification,
            "p2_003_generation_config": record.p2_003_generation_config,
            "supported_claims": record.supported_claims,
            "p2_004_generation_config": record.p2_004_generation_config,
        }
        missing = tuple(f"/{name}" for name, value in values.items() if value is None)
        if missing:
            self._fail(
                record,
                "MISSING_PROVENANCE_INPUT",
                stage="session",
                paths=missing,
            )
        return deepcopy(values)

    def _execute(
        self,
        record: _SessionRecord,
        *,
        stage: str,
        code: str,
        action: Callable[[], Any],
    ) -> Any:
        try:
            return action()
        except USPTOOfflineOrchestrationError:
            raise
        except Exception as exc:
            paths = getattr(exc, "paths", ())
            safe_paths = tuple(
                value
                for value in paths
                if type(value) is str and value.startswith("/") and len(value) <= 256
            )[:20]
            upstream_code = getattr(exc, "code", None)
            self._fail(
                record,
                code,
                stage=stage,
                paths=safe_paths,
                upstream_code=(
                    upstream_code if type(upstream_code) is str else None
                ),
            )

    def _render(self, record: _SessionRecord, output_dir: Path | str) -> None:
        bundle = self._provenance_bundle(record)
        self._execute(
            record,
            stage="P2_005_VALIDATION",
            code="P2_005_VALIDATION_REJECTED",
            action=lambda: validate_uspto_document_package(record.package, **bundle),
        )
        try:
            outputs = render_uspto_document_package(
                record.package,
                **bundle,
                output_dir=output_dir,
            )
        except FileExistsError:
            self._fail(
                record,
                "RENDER_DESTINATION_EXISTS",
                stage="P2_006",
                paths=("/output_dir",),
            )
        except ValueError:
            self._fail(
                record,
                "UNSAFE_RENDER_DESTINATION",
                stage="P2_006",
                paths=("/output_dir",),
            )
        except Exception:
            self._fail(record, "P2_006_REJECTED", stage="P2_006")
        if tuple(outputs) != FILES or any(not path.is_file() for path in outputs.values()):
            self._fail(record, "P2_006_OUTPUT_INCOMPLETE", stage="P2_006")
        directories = {path.parent.resolve(strict=True) for path in outputs.values()}
        if len(directories) != 1:
            self._fail(record, "P2_006_OUTPUT_INCOMPLETE", stage="P2_006")
        record.render_directory = directories.pop()
        record.render_manifest = tuple(
            RenderArtifact(
                filename=name,
                sha256=_sha256_file(outputs[name]),
                size_bytes=outputs[name].stat().st_size,
            )
            for name in FILES
        )
        record.artifact_digests.update(self._render_digests(record))
        self._transition(record, "RENDERED")

    def _render_digests(self, record: _SessionRecord) -> dict[str, str]:
        directory = record.render_directory
        if directory is None or directory.is_symlink() or not directory.is_dir():
            raise USPTOOfflineOrchestrationError(
                "SESSION_INTEGRITY_MISMATCH",
                stage="session",
                paths=("/render_manifest",),
                session_id=record.session_id,
                revision=record.revision,
            )
        expected = {item.filename: item for item in record.render_manifest}
        if set(expected) != set(FILES) or {item.name for item in directory.iterdir()} != set(FILES):
            raise USPTOOfflineOrchestrationError(
                "SESSION_INTEGRITY_MISMATCH",
                stage="session",
                paths=("/render_manifest",),
                session_id=record.session_id,
                revision=record.revision,
            )
        result: dict[str, str] = {}
        for name in FILES:
            path = directory / name
            if path.is_symlink() or not path.is_file():
                raise USPTOOfflineOrchestrationError(
                    "SESSION_INTEGRITY_MISMATCH",
                    stage="session",
                    paths=("/render_manifest",),
                    session_id=record.session_id,
                    revision=record.revision,
                )
            digest = _sha256_file(path)
            item = expected[name]
            if digest != item.sha256 or path.stat().st_size != item.size_bytes:
                raise USPTOOfflineOrchestrationError(
                    "SESSION_INTEGRITY_MISMATCH",
                    stage="session",
                    paths=("/render_manifest",),
                    session_id=record.session_id,
                    revision=record.revision,
                )
            result[f"render/{name}"] = digest
        return result

    def _remove_render_output(self, record: _SessionRecord) -> None:
        if record.render_directory is None:
            return
        try:
            self._render_digests(record)
            directory = record.render_directory
            for name in FILES:
                (directory / name).unlink()
            directory.rmdir()
        except Exception:
            self._fail(
                record,
                "CLEANUP_FAILED",
                stage="cleanup",
                paths=("/render_manifest",),
            )
        record.render_directory = None
        record.render_manifest = ()
        for name in FILES:
            record.artifact_digests.pop(f"render/{name}", None)

    def _fail(
        self,
        record: _SessionRecord,
        code: str,
        *,
        stage: str,
        paths: tuple[str, ...] = (),
        upstream_code: str | None = None,
    ) -> None:
        record.state = "FAILED"
        record.error_code = code
        record.error_paths = tuple(sorted(set(paths)))
        record.updated_at = datetime.now(timezone.utc)
        raise USPTOOfflineOrchestrationError(
            code,
            stage=stage,
            paths=record.error_paths,
            session_id=record.session_id,
            revision=record.revision,
            upstream_code=upstream_code,
        ) from None


def _validate_revision_json(value: Any) -> None:
    """Require JSON-native values; do not coerce tuples, keys or NaN/Infinity."""

    def visit(item: Any) -> None:
        if item is None or type(item) in (str, bool, int):
            return
        if type(item) is float and math.isfinite(item):
            return
        if type(item) is list:
            for child in item:
                visit(child)
            return
        if type(item) is dict and all(type(key) is str for key in item):
            for child in item.values():
                visit(child)
            return
        raise ValueError("non-JSON value")

    try:
        visit(value)
        sha256_canonical(value)
    except Exception:
        raise USPTOOfflineOrchestrationError(
            "INVALID_CANONICAL_INPUT", stage="session", paths=("/revision",)
        ) from None


def _canonical_envelope(
    source_envelope: ExtractionInputEnvelope | dict[str, Any] | object,
) -> dict[str, Any]:
    try:
        envelope = ExtractionInputEnvelope.model_validate(
            source_envelope.model_dump(mode="json")
            if isinstance(source_envelope, ExtractionInputEnvelope)
            else source_envelope
        )
    except Exception:
        raise USPTOOfflineOrchestrationError(
            "INVALID_SOURCE_ENVELOPE",
            stage="session",
            paths=("/source_envelope",),
        ) from None
    return envelope.model_dump(mode="json")


def _require_dict(value: object, path: str) -> dict[str, Any]:
    if type(value) is not dict:
        raise USPTOOfflineOrchestrationError(
            "INVALID_SESSION_INPUT", stage="session", paths=(path,)
        )
    return deepcopy(value)


def _revision_token(
    session_id: str, revision: int, digests: dict[str, str]
) -> str:
    material = {
        "contract_version": ORCHESTRATION_CONTRACT_VERSION,
        "session_id": session_id,
        "revision": revision,
        "root_digests": {
            key: digests[key]
            for key in (
                "source_envelope",
                "structured_analysis",
                "p2_003_generation_config",
                "p2_004_generation_config",
            )
        },
    }
    return f"rev-{revision}-" + sha256_canonical(material)[:24]


def _status(record: _SessionRecord) -> OrchestrationStatus:
    retained = tuple(
        key
        for key, value in (
            ("source_envelope", record.source_envelope),
            ("structured_analysis", record.structured_analysis),
            ("reconstruction", record.reconstruction),
            ("specification", record.specification),
            ("p2_003_generation_config", record.p2_003_generation_config),
            ("supported_claims", record.supported_claims),
            ("p2_004_generation_config", record.p2_004_generation_config),
        )
        if value is not None
    )
    return OrchestrationStatus(
        session_id=record.session_id,
        revision=record.revision,
        revision_token=record.revision_token,
        contract_version=ORCHESTRATION_CONTRACT_VERSION,
        state=record.state,
        document_id=record.document_id,
        source_sha256=record.source_sha256,
        artifact_digests=tuple(sorted(record.artifact_digests.items())),
        retained_provenance_keys=retained,
        package_id=(record.package or {}).get("package_id"),
        render_manifest=record.render_manifest,
        created_at=record.created_at.isoformat(),
        updated_at=record.updated_at.isoformat(),
        error_code=record.error_code,
        error_paths=record.error_paths,
    )


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(64 * 1024):
            digest.update(block)
    return digest.hexdigest()
