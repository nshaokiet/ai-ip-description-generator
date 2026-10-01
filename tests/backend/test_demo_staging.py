from __future__ import annotations

import copy
import tempfile
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.app.demo_staging import create_demo_staging_app
from backend.app.main import create_app
from backend.app.services.synthetic_demo import (
    DEMO_SAMPLE_HEADER,
    DEMO_SAMPLES,
    PDF_SAMPLE_ID,
    synthetic_pdf,
)


def _upload_sample(client: TestClient, sample_id: str):
    sample = DEMO_SAMPLES[sample_id]
    return client.post(
        "/api/documents",
        headers={DEMO_SAMPLE_HEADER: sample_id},
        files={"file": (sample.filename, sample.content, sample.media_type)},
    )


def test_normal_local_backend_still_accepts_ordinary_valid_upload() -> None:
    with tempfile.TemporaryDirectory() as temporary_directory:
        app = create_app()
        app.state.document_storage.root = Path(temporary_directory)
        with TestClient(app) as client:
            response = client.post(
                "/api/documents",
                files={
                    "file": (
                        "ordinary-synthetic.pdf",
                        synthetic_pdf(["Ordinary local synthetic upload."]),
                        "application/pdf",
                    )
                },
            )
    assert response.status_code == 201, response.text


def test_demo_app_starts_without_key_and_never_constructs_provider_runtimes() -> None:
    with tempfile.TemporaryDirectory() as temporary_directory:
        with (
            patch("backend.app.main.OpenAIExtractionRuntime") as extraction_runtime,
            patch("backend.app.main.OpenAIDraftRuntime") as draft_runtime,
        ):
            app = create_demo_staging_app(temporary_root=Path(temporary_directory))
        extraction_runtime.assert_not_called()
        draft_runtime.assert_not_called()
        assert app.state.settings.openai_api_key is None
        assert app.state.settings.run_openai_live_tests is False
        assert app.state.settings.run_openai_draft_live_tests is False
        with TestClient(app) as client:
            assert client.get("/health").json() == {"status": "ok"}


def test_demo_backend_rejects_missing_or_mismatched_sample_contract() -> None:
    with tempfile.TemporaryDirectory() as temporary_directory:
        app = create_demo_staging_app(temporary_root=Path(temporary_directory))
        with TestClient(app) as client:
            missing_header = client.post(
                "/api/documents",
                files={
                    "file": (
                        "ordinary.pdf",
                        synthetic_pdf(["Ordinary arbitrary research-like upload."]),
                        "application/pdf",
                    )
                },
            )
            assert missing_header.status_code == 403
            assert missing_header.json()["error"]["code"] == "synthetic_demo_sample_required"

            expected = DEMO_SAMPLES[PDF_SAMPLE_ID]
            mismatched = client.post(
                "/api/documents",
                headers={DEMO_SAMPLE_HEADER: PDF_SAMPLE_ID},
                files={
                    "file": (
                        expected.filename,
                        synthetic_pdf(["Different synthetic bytes."]),
                        expected.media_type,
                    )
                },
            )
            assert mismatched.status_code == 422
            assert mismatched.json()["error"]["code"] == "invalid_synthetic_demo_sample"


def test_demo_pdf_upload_process_validate_and_docx_export_is_provider_free() -> None:
    with tempfile.TemporaryDirectory() as temporary_directory:
        app = create_demo_staging_app(temporary_root=Path(temporary_directory))
        with TestClient(app) as client:
            sample_response = client.get(f"/api/demo/samples/{PDF_SAMPLE_ID}")
            assert sample_response.status_code == 200
            assert sample_response.content == DEMO_SAMPLES[PDF_SAMPLE_ID].content

            upload = _upload_sample(client, PDF_SAMPLE_ID)
            assert upload.status_code == 201, upload.text
            document_id = upload.json()["document_id"]

            process = client.post(f"/api/documents/{document_id}/process")
            assert process.status_code == 200, process.text
            result = process.json()
            assert result["metadata"]["source_cleanup_performed"] is True

            revision = {
                "revision_id": "revision-1",
                "analysis": result["analysis"],
                "original_draft": result["draft"],
                "draft": copy.deepcopy(result["draft"]),
                "selected_title_candidate_id": None,
            }
            validation = client.post("/api/drafts/validate", json=revision)
            assert validation.status_code == 200, validation.text

            export = client.post(
                "/api/exports/docx",
                json={**revision, "validated_digest": validation.json()["draft_digest"]},
            )
            assert export.status_code == 200, export.text
            assert export.content.startswith(b"PK")

        assert app.state.synthetic_extraction_runtime.provider_call_count == 0
        assert app.state.synthetic_draft_runtime.provider_call_count == 0


def test_render_blueprint_is_free_synthetic_and_contains_no_secret() -> None:
    blueprint = (Path(__file__).resolve().parents[2] / "render.yaml").read_text(
        encoding="utf-8"
    )
    required_fragments = (
        "runtime: static",
        "staticPublishPath: frontend/out",
        "RENDER_STATIC_EXPORT",
        "NEXT_PUBLIC_DEMO_STAGING",
        "runtime: python",
        "plan: free",
        "region: singapore",
        "healthCheckPath: /health",
        "backend.app.demo_staging:app",
        "RUN_OPENAI_LIVE_TESTS",
        "RUN_OPENAI_DRAFT_LIVE_TESTS",
        "Cache-Control",
        "Permissions-Policy",
        "Referrer-Policy",
        "X-Content-Type-Options",
        "X-Frame-Options",
    )
    for fragment in required_fragments:
        assert fragment in blueprint
    assert "OPENAI_API_KEY" not in blueprint
    assert "allow_origins" not in blueprint
    assert "type: worker" not in blueprint
    assert "disk:" not in blueprint
