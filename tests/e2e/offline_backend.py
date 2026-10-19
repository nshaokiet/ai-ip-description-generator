"""Synthetic-only FastAPI process for browser tests. No provider client exists."""

from __future__ import annotations

import tempfile
from pathlib import Path

from fastapi.responses import Response
from tests.e2e.provider_tripwire import ProviderTripwire, sanitize_provider_environment

# Sanitize before importing application/provider modules or creating any runtime.
sanitize_provider_environment()

from backend.app.core.config import Settings
from backend.app.main import create_app
from backend.app.services.patent_docx_renderer import PatentDocxRenderer
from backend.app.services.synthetic_demo import (
    SyntheticDemoDraftRuntime,
    SyntheticDemoExtractionRuntime,
    paragraph_xml,
    synthetic_docx,
    synthetic_pdf,
)


TRIPWIRE = ProviderTripwire().install()

TEMP_ROOT = tempfile.TemporaryDirectory(prefix="ai-ip-p0-006-browser-")


settings = Settings(
    storage_root=Path(TEMP_ROOT.name) / "uploads",
    local_export_root=Path(TEMP_ROOT.name) / "exports",
    enable_local_orchestration_api=True,
)
app = create_app(
    settings,
    extraction_runtime=SyntheticDemoExtractionRuntime(),
    draft_runtime=SyntheticDemoDraftRuntime(),
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

@app.get("/__test/provider-activity")
def test_provider_activity() -> dict[str, int]:
    """Expose counters only, and fail if any unexpected provider activity was attempted."""
    TRIPWIRE.assert_no_unexpected_activity()
    return TRIPWIRE.snapshot()
