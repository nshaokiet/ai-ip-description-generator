"""Provider-free FastAPI entrypoint for the public synthetic demo/staging site."""

from __future__ import annotations

import tempfile
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import Response

from backend.app.core.config import Settings
from backend.app.main import create_app
from backend.app.services.patent_docx_renderer import PatentDocxRenderer
from backend.app.services.synthetic_demo import (
    DEMO_SAMPLES,
    SyntheticDemoDraftRuntime,
    SyntheticDemoExtractionRuntime,
    SyntheticDemoUploadGuard,
)


demo_router = APIRouter(prefix="/api/demo")


@demo_router.get("/samples/{sample_id}")
def get_synthetic_demo_sample(sample_id: str) -> Response:
    sample = DEMO_SAMPLES.get(sample_id)
    if sample is None:
        return Response(status_code=404)
    return Response(
        sample.content,
        media_type=sample.media_type,
        headers={
            "Cache-Control": "no-store",
            "Content-Disposition": f'attachment; filename="{sample.filename}"',
            "X-AI-IP-Demo-Sample": sample.sample_id,
        },
    )


def create_demo_staging_app(*, temporary_root: Path | None = None):
    """Create the isolated staging app with deterministic synthetic runtimes."""
    root = temporary_root or Path(tempfile.gettempdir()) / "ai-ip-demo-staging"
    settings = Settings(
        storage_root=root / "uploads",
        local_export_root=root / "exports",
        enable_local_orchestration_api=True,
        openai_api_key=None,
        run_openai_live_tests=False,
        run_openai_draft_live_tests=False,
    )
    extraction_runtime = SyntheticDemoExtractionRuntime()
    draft_runtime = SyntheticDemoDraftRuntime()
    application = create_app(
        settings,
        extraction_runtime=extraction_runtime,
        draft_runtime=draft_runtime,
        docx_renderer=PatentDocxRenderer(output_root=settings.local_export_root),
    )
    application.title = "AI IP Generator Synthetic Demo/Staging Backend"
    application.state.document_upload_guard = SyntheticDemoUploadGuard()
    application.state.synthetic_demo_only = True
    application.state.synthetic_extraction_runtime = extraction_runtime
    application.state.synthetic_draft_runtime = draft_runtime
    application.include_router(demo_router)
    return application


app = create_demo_staging_app()
