"""Synthetic-only FastAPI process for browser tests. No provider client exists."""

from __future__ import annotations

import copy
import json
import tempfile
from pathlib import Path

from fastapi.responses import Response

from backend.app.core.config import Settings
from backend.app.main import create_app
from backend.app.services.draft_business_validation import validate_draft_business_rules
from backend.app.services.draft_runtime import DraftRuntimeMetadata, DraftRuntimeResult
from backend.app.services.extraction_runtime import ExtractionRuntimeMetadata, ExtractionRuntimeResult
from backend.app.services.patent_docx_renderer import PatentDocxRenderer
from tests.backend.test_document_parsing import paragraph_xml, synthetic_docx, synthetic_pdf


ROOT = Path(__file__).resolve().parents[2]
CASE = json.loads((ROOT / "tests/fixtures/patent-draft/v1.0.0/cases/representative.json").read_text(encoding="utf-8"))
MISSING = json.loads((ROOT / "tests/fixtures/patent-draft/v1.0.0/cases/missing-information.json").read_text(encoding="utf-8"))
TEMP_ROOT = tempfile.TemporaryDirectory(prefix="ai-ip-p0-006-browser-")


class SyntheticExtractionRuntime:
    def run_extraction(self, envelope, *, correlation_id=None):
        metadata = envelope.document_metadata.model_dump(exclude_none=True)
        fixture = MISSING if metadata["file_name"] == "synthetic-missing.pdf" else CASE
        analysis = copy.deepcopy(fixture["input"]["source_analysis"])
        analysis["document_metadata"] = metadata
        for evidence in analysis["evidence"]:
            evidence["document_id"] = metadata["document_id"]
        return ExtractionRuntimeResult(
            analysis=analysis,
            runtime=ExtractionRuntimeMetadata(
                provider="offline_fake", model="offline_fake", request_id="offline-extraction",
                status="completed", duration_ms=1, usage={},
            ),
        )


class SyntheticDraftRuntime:
    def run_draft_generation(self, source_analysis, selected_title_candidate_id=None):
        missing_case = source_analysis["document_metadata"]["file_name"] == "synthetic-missing.pdf"
        draft = copy.deepcopy((MISSING if missing_case else CASE)["expected_output"])
        draft["document_metadata"]["source_document"] = copy.deepcopy(source_analysis["document_metadata"])
        for evidence in draft["evidence_appendix"]:
            evidence["document_id"] = source_analysis["document_metadata"]["document_id"]
        if selected_title_candidate_id is None and not missing_case:
            draft["selected_title"] = copy.deepcopy(MISSING["expected_output"]["selected_title"])
            draft["missing_information"].append(
                copy.deepcopy(next(item for item in MISSING["expected_output"]["missing_information"] if item["missing_id"] == "missing-title"))
            )
            for evidence in draft["evidence_appendix"]:
                evidence["usage_references"] = [
                    usage for usage in evidence["usage_references"]
                    if usage["target_type"] != "SELECTED_TITLE"
                ]
        validate_draft_business_rules(
            draft, source_analysis, selected_title_candidate_id=selected_title_candidate_id
        )
        return DraftRuntimeResult(
            draft=draft,
            runtime=DraftRuntimeMetadata(
                provider="offline_fake", model="offline_fake", request_id="offline-draft",
                status="completed", duration_ms=1, usage={},
            ),
        )


settings = Settings(
    storage_root=Path(TEMP_ROOT.name) / "uploads",
    local_export_root=Path(TEMP_ROOT.name) / "exports",
    enable_local_orchestration_api=True,
)
app = create_app(
    settings,
    extraction_runtime=SyntheticExtractionRuntime(),
    draft_runtime=SyntheticDraftRuntime(),
    docx_renderer=PatentDocxRenderer(output_root=settings.local_export_root),
)


@app.get("/__test/storage")
def test_storage() -> dict[str, int]:
    """Expose file counts, never paths or content, for synthetic cleanup checks."""
    return {
        "source_files": sum(path.is_file() for path in settings.storage_root.rglob("*")),
        "export_files": sum(path.is_file() for path in settings.local_export_root.rglob("*")),
    }


@app.get("/__test/pdf")
def test_pdf() -> Response:
    return Response(
        synthetic_pdf(["Synthetic optical sensor calibration and temperature coefficient for offline browser testing."]),
        media_type="application/pdf",
    )


@app.get("/__test/docx")
def test_docx() -> Response:
    return Response(
        synthetic_docx([paragraph_xml("Synthetic optical sensor calibration and temperature coefficient for offline browser testing.")]),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
