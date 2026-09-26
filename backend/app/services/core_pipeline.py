"""Internal core pipeline orchestration for APP-003."""

from __future__ import annotations

import logging
import time
import uuid
from dataclasses import dataclass
from typing import Any, Protocol

from backend.app.schemas.analysis_input import ExtractionInputEnvelope
from backend.app.services.document_parsing import DocumentPreparationError
from backend.app.services.document_storage import DocumentStorage
from backend.app.services.draft_runtime import DraftRuntimeError, DraftRuntimeResult
from backend.app.services.extraction_runtime import (
    ExtractionRuntimeError,
    ExtractionRuntimeResult,
)


LOGGER = logging.getLogger(__name__)


class PreparationServiceProtocol(Protocol):
    def prepare_extraction_input(self, document_id: str) -> ExtractionInputEnvelope: ...


class ExtractionRuntimeProtocol(Protocol):
    def run_extraction(
        self,
        envelope: ExtractionInputEnvelope,
        *,
        correlation_id: str | None = None,
    ) -> ExtractionRuntimeResult: ...


class DraftRuntimeProtocol(Protocol):
    def run_draft_generation(
        self,
        source_analysis: dict[str, Any],
        selected_title_candidate_id: str | None = None,
    ) -> DraftRuntimeResult: ...


@dataclass(frozen=True, slots=True)
class PipelineStageMetadata:
    stage: str
    duration_ms: int
    status: str
    provider_request_id: str | None = None
    usage: dict[str, int] | None = None


@dataclass(frozen=True, slots=True)
class PipelineMetadata:
    document_id: str
    correlation_id: str
    total_duration_ms: int
    stages: tuple[PipelineStageMetadata, ...]
    source_cleanup_performed: bool


@dataclass(frozen=True, slots=True)
class PipelineResult:
    analysis: dict[str, Any]
    draft: dict[str, Any]
    metadata: PipelineMetadata


class PipelineOrchestrationError(RuntimeError):
    """Safe failure raised when a typed downstream stage error occurs."""

    def __init__(
        self,
        stage: str,
        code: str,
        message: str,
        *,
        document_id: str,
        correlation_id: str,
        paths: tuple[str, ...] = (),
    ) -> None:
        super().__init__(message)
        self.stage = stage
        self.code = code
        self.safe_message = message
        self.document_id = document_id
        self.correlation_id = correlation_id
        self.paths = paths


class CorePipelineOrchestrator:
    """Coordinate preparation, extraction, drafting, and mandatory cleanup."""

    def __init__(
        self,
        storage: DocumentStorage,
        preparation_service: PreparationServiceProtocol,
        extraction_runtime: ExtractionRuntimeProtocol,
        draft_runtime: DraftRuntimeProtocol,
    ) -> None:
        self.storage = storage
        self.preparation_service = preparation_service
        self.extraction_runtime = extraction_runtime
        self.draft_runtime = draft_runtime

    def run_pipeline(
        self,
        document_id: str,
        *,
        selected_title_candidate_id: str | None = None,
        correlation_id: str | None = None,
    ) -> PipelineResult:
        runtime_correlation_id = correlation_id or uuid.uuid4().hex
        pipeline_started = time.monotonic()
        stages: list[PipelineStageMetadata] = []
        cleanup_performed = False

        try:
            preparation_started = time.monotonic()
            try:
                envelope = self.preparation_service.prepare_extraction_input(document_id)
            except DocumentPreparationError as exc:
                self._log_failure(
                    document_id,
                    runtime_correlation_id,
                    stage="preparation",
                    code=exc.code,
                )
                raise PipelineOrchestrationError(
                    "preparation",
                    exc.code,
                    exc.safe_message,
                    document_id=document_id,
                    correlation_id=runtime_correlation_id,
                ) from exc
            stages.append(
                PipelineStageMetadata(
                    stage="preparation",
                    duration_ms=_elapsed_ms(preparation_started),
                    status="completed",
                )
            )

            extraction_started = time.monotonic()
            try:
                extraction_result = self.extraction_runtime.run_extraction(
                    envelope,
                    correlation_id=runtime_correlation_id,
                )
            except ExtractionRuntimeError as exc:
                self._log_failure(
                    document_id,
                    runtime_correlation_id,
                    stage="extraction",
                    code=exc.code,
                )
                raise PipelineOrchestrationError(
                    "extraction",
                    exc.code,
                    exc.safe_message,
                    document_id=document_id,
                    correlation_id=runtime_correlation_id,
                    paths=exc.paths,
                ) from exc
            stages.append(
                _runtime_stage_metadata(
                    "extraction",
                    extraction_started,
                    extraction_result.runtime,
                )
            )

            draft_started = time.monotonic()
            try:
                draft_result = self.draft_runtime.run_draft_generation(
                    extraction_result.analysis,
                    selected_title_candidate_id,
                )
            except DraftRuntimeError as exc:
                self._log_failure(
                    document_id,
                    runtime_correlation_id,
                    stage="draft_generation",
                    code=exc.code,
                )
                raise PipelineOrchestrationError(
                    "draft_generation",
                    exc.code,
                    exc.safe_message,
                    document_id=document_id,
                    correlation_id=runtime_correlation_id,
                    paths=exc.paths,
                ) from exc
            stages.append(
                _runtime_stage_metadata(
                    "draft_generation",
                    draft_started,
                    draft_result.runtime,
                )
            )
        finally:
            cleanup_performed = self._cleanup_source(document_id)

        result = PipelineResult(
            analysis=extraction_result.analysis,
            draft=draft_result.draft,
            metadata=PipelineMetadata(
                document_id=document_id,
                correlation_id=runtime_correlation_id,
                total_duration_ms=_elapsed_ms(pipeline_started),
                stages=tuple(stages),
                source_cleanup_performed=cleanup_performed,
            ),
        )
        LOGGER.info(
            "pipeline_completed correlation_id=%s document_id=%s status=completed "
            "duration_ms=%s source_cleanup_performed=%s",
            _safe_log_identifier(runtime_correlation_id),
            _safe_document_id(document_id),
            result.metadata.total_duration_ms,
            result.metadata.source_cleanup_performed,
        )
        return result

    def _cleanup_source(self, document_id: str) -> bool:
        """Delete the source best-effort without masking a primary outcome."""

        try:
            cleanup_ok = self.storage.delete(document_id)
        except Exception:
            LOGGER.warning(
                "pipeline_source_cleanup_failed document_id=%s",
                _safe_document_id(document_id),
            )
            return False

        if not cleanup_ok:
            LOGGER.warning(
                "pipeline_source_cleanup_failed document_id=%s",
                _safe_document_id(document_id),
            )
            return False
        return True

    @staticmethod
    def _log_failure(
        document_id: str,
        correlation_id: str,
        *,
        stage: str,
        code: str,
    ) -> None:
        LOGGER.warning(
            "pipeline_stage_failed correlation_id=%s document_id=%s stage=%s code=%s",
            _safe_log_identifier(correlation_id),
            _safe_document_id(document_id),
            stage,
            code,
        )


def _runtime_stage_metadata(
    stage: str,
    started: float,
    runtime: Any,
) -> PipelineStageMetadata:
    return PipelineStageMetadata(
        stage=stage,
        duration_ms=_elapsed_ms(started),
        status="completed",
        provider_request_id=runtime.request_id,
        usage=dict(runtime.usage),
    )


def _elapsed_ms(started: float) -> int:
    return max(0, round((time.monotonic() - started) * 1000))


def _safe_log_identifier(value: str) -> str:
    if value and len(value) <= 128 and all(character.isalnum() or character in "-_" for character in value):
        return value
    return "invalid"


def _safe_document_id(value: str) -> str:
    if len(value) == 32 and all(character in "0123456789abcdef" for character in value):
        return value
    return "invalid"
