"""Opt-in local HTTP boundary for the existing orchestration pipeline."""

from __future__ import annotations

import logging
import uuid
from pathlib import Path
from typing import Any, Literal

from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
from jsonschema import ValidationError
from pydantic import BaseModel, ConfigDict, Field
from starlette.background import BackgroundTask

from backend.app.api.routes.documents import APIError
from backend.app.services.core_pipeline import PipelineOrchestrationError
from backend.app.services.edited_draft_validation import (
    EditedDraftValidationError,
    draft_digest,
    validate_edited_draft,
)


LOGGER = logging.getLogger(__name__)
DOCX_MEDIA_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
DOCX_DOWNLOAD_NAME = "patent-description-draft.docx"

router = APIRouter(prefix="/api")


class StrictRequest(BaseModel):
    """Reject undeclared public request fields."""

    model_config = ConfigDict(extra="forbid")


class ProcessDocumentRequest(StrictRequest):
    selected_title_candidate_id: str | None = None


class DraftRevisionRequest(StrictRequest):
    revision_id: str = Field(min_length=1, max_length=64, pattern=r"^[A-Za-z0-9_-]+$")
    analysis: dict[str, Any]
    original_draft: dict[str, Any]
    draft: dict[str, Any]
    selected_title_candidate_id: str | None = None


class ExportDocxRequest(DraftRevisionRequest):
    validated_digest: str = Field(pattern=r"^[a-f0-9]{64}$")


class DraftValidationResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    valid: Literal[True]
    revision_id: str
    draft_digest: str
    unverified_prose_paths: list[str]
    correlation_id: str


class DocumentMetadataResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    document_id: str
    original_filename: str
    media_type: str
    size_bytes: int
    page_count: int | None
    validation_status: Literal["validated"]


class ProcessMetadataResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    document_id: str
    correlation_id: str
    source_cleanup_performed: bool


class ProcessDocumentResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    analysis: dict[str, Any]
    draft: dict[str, Any]
    metadata: ProcessMetadataResponse


def _is_document_id(value: str) -> bool:
    return (
        len(value) == 32
        and value[0] in "abcdef"
        and all(character in "0123456789abcdef" for character in value)
    )


def _document_not_found() -> APIError:
    return APIError(404, "document_not_found", "The document was not found.")


def _pipeline_status(code: str) -> int:
    if code in {"document_unknown", "document_expired_or_missing"}:
        return 404
    if code in {"runtime_not_configured", "draft_runtime_not_configured"}:
        return 503
    if code == "provider_timeout":
        return 504
    if code == "provider_rate_limited":
        return 429
    if code in {
        "empty_document",
        "no_extractable_text",
        "parse_failed",
        "grounding_validation_failed",
        "schema_validation_failed",
        "draft_schema_validation_failed",
        "draft_grounding_validation_failed",
        "invalid_title_selection",
        "word_count_exceeded",
    }:
        return 422
    return 502


def _remove_export(path: Path) -> None:
    try:
        path.unlink(missing_ok=True)
    except OSError:
        LOGGER.warning("docx_export_cleanup_failed")


def _validate_revision(body: DraftRevisionRequest) -> tuple[str, ...]:
    try:
        return validate_edited_draft(
            analysis=body.analysis,
            original_draft=body.original_draft,
            draft=body.draft,
            selected_title_candidate_id=body.selected_title_candidate_id,
        )
    except EditedDraftValidationError as exc:
        raise APIError(422, exc.code, exc.safe_message, paths=exc.paths) from exc


@router.get("/documents/{document_id}", response_model=DocumentMetadataResponse)
async def get_document(document_id: str, request: Request) -> dict[str, object]:
    if not _is_document_id(document_id):
        raise _document_not_found()

    record = request.app.state.document_registry.get(document_id)
    if record is None:
        raise _document_not_found()

    return {
        "document_id": record.document_id,
        "original_filename": record.file_name,
        "media_type": record.media_type,
        "size_bytes": record.size_bytes,
        "page_count": record.page_count,
        "validation_status": "validated",
    }


@router.post("/documents/{document_id}/process", response_model=ProcessDocumentResponse)
async def process_document(
    document_id: str,
    request: Request,
    body: ProcessDocumentRequest | None = None,
) -> dict[str, object]:
    if not _is_document_id(document_id):
        raise _document_not_found()
    if request.app.state.document_registry.get(document_id) is None:
        raise _document_not_found()

    selected_title_candidate_id = body.selected_title_candidate_id if body else None
    try:
        result = request.app.state.core_pipeline.run_pipeline(
            document_id,
            selected_title_candidate_id=selected_title_candidate_id,
            correlation_id=request.state.correlation_id,
        )
    except PipelineOrchestrationError as exc:
        raise APIError(
            _pipeline_status(exc.code),
            exc.code,
            exc.safe_message,
        ) from exc

    return {
        "analysis": result.analysis,
        "draft": result.draft,
        "metadata": {
            "document_id": result.metadata.document_id,
            "correlation_id": result.metadata.correlation_id,
            "source_cleanup_performed": result.metadata.source_cleanup_performed,
        },
    }


@router.post("/drafts/validate", response_model=DraftValidationResponse)
async def validate_draft_revision(
    body: DraftRevisionRequest, request: Request
) -> DraftValidationResponse:
    unverified_paths = _validate_revision(body)
    return DraftValidationResponse(
        valid=True,
        revision_id=body.revision_id,
        draft_digest=draft_digest(body.draft, body.revision_id),
        unverified_prose_paths=list(unverified_paths),
        correlation_id=request.state.correlation_id,
    )


@router.post("/exports/docx")
async def export_docx(body: ExportDocxRequest, request: Request) -> FileResponse:
    if body.validated_digest != draft_digest(body.draft, body.revision_id):
        raise APIError(
            409,
            "stale_draft_revision",
            "The selected draft differs from the validated revision.",
        )
    _validate_revision(body)
    export_root = Path(request.app.state.local_export_root)
    output_path = export_root / f"{uuid.uuid4().hex}.docx"
    try:
        rendered_path = request.app.state.patent_docx_renderer.render(
            body.draft,
            output_path,
        )
    except ValidationError as exc:
        _remove_export(output_path)
        raise APIError(
            422,
            "invalid_patent_draft",
            "The patent draft does not match the canonical schema.",
        ) from exc
    except Exception as exc:
        _remove_export(output_path)
        LOGGER.error(
            "docx_export_failed correlation_id=%s",
            request.state.correlation_id,
        )
        raise APIError(
            500,
            "docx_render_failed",
            "The DOCX export could not be generated.",
        ) from exc

    return FileResponse(
        rendered_path,
        media_type=DOCX_MEDIA_TYPE,
        filename=DOCX_DOWNLOAD_NAME,
        background=BackgroundTask(_remove_export, Path(rendered_path)),
    )
