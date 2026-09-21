"""Strict AI-002 extraction-input envelope models for APP-002."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from backend.app.services.document_validation import DOCX_MEDIA_TYPE, PDF_MEDIA_TYPE


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class DocumentMetadata(StrictModel):
    document_id: str = Field(min_length=1)
    file_name: str = Field(min_length=1)
    media_type: Literal[PDF_MEDIA_TYPE, DOCX_MEDIA_TYPE]
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")

    @model_validator(mode="after")
    def reject_blank_identifiers(self) -> "DocumentMetadata":
        if not self.document_id.strip() or not self.file_name.strip():
            raise ValueError("document identifiers must contain non-whitespace characters")
        return self

class SourceLocator(StrictModel):
    page: int | None = Field(default=None, ge=1)
    section: str | None = None
    paragraph_id: str | None = None
    chunk_id: str | None = None
    table_id: str | None = None
    figure_id: str | None = None

    @model_validator(mode="after")
    def require_supported_locator(self) -> "SourceLocator":
        values = (
            self.page,
            self.section,
            self.paragraph_id,
            self.chunk_id,
            self.table_id,
            self.figure_id,
        )
        if not any(value is not None for value in values):
            raise ValueError("locator must contain at least one supported field")
        for value in values[1:]:
            if value is not None and not value.strip():
                raise ValueError("locator string fields must not be blank")
        return self


class SourceUnit(StrictModel):
    evidence_id: str = Field(min_length=1, pattern=r"^[A-Za-z0-9._:-]+$")
    evidence_type: Literal["TEXT", "TABLE"]
    locator: SourceLocator
    content: str = Field(min_length=1)

    @model_validator(mode="after")
    def require_non_whitespace_content(self) -> "SourceUnit":
        if not self.content.strip():
            raise ValueError("source-unit content must not be blank")
        return self


class ExtractionInputEnvelope(StrictModel):
    document_metadata: DocumentMetadata
    source_units: list[SourceUnit] = Field(min_length=1)

    @model_validator(mode="after")
    def require_unique_evidence_ids(self) -> "ExtractionInputEnvelope":
        evidence_ids = [unit.evidence_id for unit in self.source_units]
        if len(evidence_ids) != len(set(evidence_ids)):
            raise ValueError("evidence_id values must be unique within a document")
        return self
