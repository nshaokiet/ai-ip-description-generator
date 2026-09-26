"""Internal APP-003-to-DOCX composition service for P0-003."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from backend.app.services.core_pipeline import PipelineResult
from backend.app.services.patent_docx_renderer import PatentDocxRenderer


class CorePipelineProtocol(Protocol):
    def run_pipeline(
        self,
        document_id: str,
        *,
        selected_title_candidate_id: str | None = None,
        correlation_id: str | None = None,
    ) -> PipelineResult: ...


class PatentDocxRendererProtocol(Protocol):
    def render(self, draft: dict[str, Any], output_path: Path) -> Path: ...


@dataclass(frozen=True, slots=True)
class PipelineDocxResult:
    pipeline: PipelineResult
    output_path: Path


class CorePipelineDocxService:
    """Compose the internal core pipeline with canonical DOCX rendering."""

    def __init__(
        self,
        pipeline: CorePipelineProtocol,
        renderer: PatentDocxRendererProtocol | None = None,
    ) -> None:
        self.pipeline = pipeline
        self.renderer = renderer or PatentDocxRenderer()

    def generate(
        self,
        document_id: str,
        output_path: Path,
        *,
        selected_title_candidate_id: str | None = None,
        correlation_id: str | None = None,
    ) -> PipelineDocxResult:
        """Run APP-003 and render its in-memory validated draft directly."""

        pipeline_result = self.pipeline.run_pipeline(
            document_id,
            selected_title_candidate_id=selected_title_candidate_id,
            correlation_id=correlation_id,
        )
        rendered_path = self.renderer.render(pipeline_result.draft, output_path)
        return PipelineDocxResult(
            pipeline=pipeline_result,
            output_path=rendered_path,
        )
