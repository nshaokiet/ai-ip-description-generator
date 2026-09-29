from __future__ import annotations

import copy
import io
import json
import os
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.app.core.config import Settings
from backend.app.main import create_app
from backend.app.services.draft_runtime import DraftRuntimeMetadata, DraftRuntimeResult
from backend.app.services.draft_validation import validate_canonical_draft
from backend.app.services.edited_draft_validation import draft_digest
from backend.app.services.extraction_runtime import ExtractionRuntimeError
from backend.app.services.patent_docx_renderer import PatentDocxRenderer
from tests.backend.test_core_pipeline_e2e_offline import ValidatingFakeExtractionRuntime
from tests.backend.test_document_parsing import synthetic_pdf


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DRAFT_SCHEMA_PATH = (
    REPOSITORY_ROOT
    / "schemas"
    / "patent-draft"
    / "v1.0.0"
    / "patent-draft.schema.json"
)
DRAFT_CASE_PATH = (
    REPOSITORY_ROOT
    / "tests"
    / "fixtures"
    / "patent-draft"
    / "v1.0.0"
    / "cases"
    / "missing-information.json"
)
REPRESENTATIVE_CASE_PATH = (
    REPOSITORY_ROOT / "tests" / "fixtures" / "patent-draft" / "v1.0.0"
    / "cases" / "representative.json"
)
PDF_MEDIA_TYPE = "application/pdf"
DOCX_MEDIA_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class RecordingDraftRuntime:
    def __init__(self) -> None:
        self.draft_template = _load_json(DRAFT_CASE_PATH)["expected_output"]
        self.draft_schema = _load_json(DRAFT_SCHEMA_PATH)
        self.invocations: list[tuple[dict, str | None]] = []

    def run_draft_generation(
        self,
        source_analysis: dict,
        selected_title_candidate_id: str | None = None,
    ) -> DraftRuntimeResult:
        self.invocations.append((source_analysis, selected_title_candidate_id))
        draft = copy.deepcopy(self.draft_template)
        draft["document_metadata"]["source_document"] = copy.deepcopy(
            source_analysis["document_metadata"]
        )
        return DraftRuntimeResult(
            draft=validate_canonical_draft(draft, self.draft_schema),
            runtime=DraftRuntimeMetadata(
                provider="offline_fake",
                model="offline_fake",
                request_id="provider-request-must-not-leak",
                status="completed",
                duration_ms=1,
                usage={"total_tokens": 1},
            ),
        )


class FailingExtractionRuntime:
    def run_extraction(self, envelope, *, correlation_id=None):
        raise ExtractionRuntimeError(
            "provider_timeout",
            "The extraction provider timed out.",
        )


class ExplodingRenderer:
    def render(self, draft: dict, output_path: Path) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(b"partial")
        raise RuntimeError("sensitive renderer detail")


class LocalOrchestrationAPITests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.storage_root = self.root / "uploads"
        self.export_root = self.root / "exports"
        self.extraction_runtime = ValidatingFakeExtractionRuntime()
        self.draft_runtime = RecordingDraftRuntime()
        self.settings = Settings(
            storage_root=self.storage_root,
            local_export_root=self.export_root,
            enable_local_orchestration_api=True,
        )
        self.app = create_app(
            self.settings,
            extraction_runtime=self.extraction_runtime,
            draft_runtime=self.draft_runtime,
            docx_renderer=PatentDocxRenderer(output_root=self.export_root),
        )
        self.client_context = TestClient(self.app)
        self.client = self.client_context.__enter__()

    def tearDown(self) -> None:
        self.client_context.__exit__(None, None, None)
        self.temporary_directory.cleanup()

    def upload(self) -> tuple[str, dict]:
        payload = synthetic_pdf(["Synthetic optical apparatus for local API testing."])
        response = self.client.post(
            "/api/documents",
            files={"file": ("synthetic.pdf", payload, PDF_MEDIA_TYPE)},
        )
        self.assertEqual(201, response.status_code, response.text)
        return response.json()["document_id"], response.json()

    def draft_context(self) -> dict:
        fixture = _load_json(REPRESENTATIVE_CASE_PATH)
        draft = fixture["expected_output"]
        return {
            "revision_id": "revision-1",
            "analysis": fixture["input"]["source_analysis"],
            "original_draft": copy.deepcopy(draft),
            "draft": copy.deepcopy(draft),
            "selected_title_candidate_id": "title-calibration",
        }

    def validated_export_context(self, context: dict) -> dict:
        response = self.client.post("/api/drafts/validate", json=context)
        self.assertEqual(200, response.status_code, response.text)
        return {**context, "validated_digest": response.json()["draft_digest"]}

    def test_feature_flag_is_strict_and_opt_in(self) -> None:
        with patch.dict(os.environ, {"AI_IP_ENABLE_LOCAL_ORCHESTRATION_API": "1"}):
            self.assertTrue(Settings.from_environment().enable_local_orchestration_api)
        with patch.dict(os.environ, {"AI_IP_ENABLE_LOCAL_ORCHESTRATION_API": "0"}):
            self.assertFalse(Settings.from_environment().enable_local_orchestration_api)
        with patch.dict(os.environ, {"AI_IP_ENABLE_LOCAL_ORCHESTRATION_API": "true"}):
            with self.assertRaisesRegex(ValueError, "must be 0 or 1"):
                Settings.from_environment()

    def test_disabled_flag_preserves_existing_routes_and_hides_local_routes(self) -> None:
        disabled_settings = Settings(
            storage_root=self.root / "disabled-uploads",
            local_export_root=self.root / "disabled-exports",
        )
        with TestClient(create_app(disabled_settings)) as client:
            self.assertEqual({"status": "ok"}, client.get("/health").json())
            _, upload = self._upload_with(client)
            for method, path in (
                ("get", f"/api/documents/{upload['document_id']}"),
                ("post", f"/api/documents/{upload['document_id']}/process"),
                ("post", "/api/exports/docx"),
                ("post", "/api/drafts/validate"),
            ):
                response = getattr(client, method)(path)
                self.assertEqual(404, response.status_code, response.text)
                self.assertIn("correlation_id", response.json()["error"])

    def _upload_with(self, client: TestClient) -> tuple[bytes, dict]:
        payload = synthetic_pdf(["Synthetic source for disabled-route testing."])
        response = client.post(
            "/api/documents",
            files={"file": ("synthetic.pdf", payload, PDF_MEDIA_TYPE)},
        )
        self.assertEqual(201, response.status_code, response.text)
        return payload, response.json()

    def test_get_document_returns_safe_registry_metadata_only(self) -> None:
        document_id, upload = self.upload()
        response = self.client.get(f"/api/documents/{document_id}")
        self.assertEqual(200, response.status_code, response.text)
        self.assertEqual(
            {
                "document_id",
                "original_filename",
                "media_type",
                "size_bytes",
                "page_count",
                "validation_status",
            },
            set(response.json()),
        )
        self.assertEqual(upload["original_filename"], response.json()["original_filename"])
        self.assertNotIn("sha256", response.text)
        self.assertNotIn(str(self.storage_root), response.text)

    def test_malformed_and_unknown_document_ids_are_safe_404(self) -> None:
        with patch.object(self.app.state.document_storage, "path_for") as path_for:
            malformed = self.client.get("/api/documents/not-an-opaque-id")
        path_for.assert_not_called()
        unknown = self.client.get(f"/api/documents/{'a' * 32}")
        for response in (malformed, unknown):
            self.assertEqual(404, response.status_code, response.text)
            self.assertEqual("document_not_found", response.json()["error"]["code"])
            self.assertIn("correlation_id", response.json()["error"])

    def test_process_runs_existing_pipeline_and_returns_minimal_metadata(self) -> None:
        document_id, _ = self.upload()
        source_path = self.app.state.document_storage.path_for(document_id)
        with (
            patch("socket.create_connection") as connect,
            patch("urllib.request.urlopen") as urlopen,
        ):
            response = self.client.post(
                f"/api/documents/{document_id}/process",
                json={"selected_title_candidate_id": "candidate-from-client"},
            )
        connect.assert_not_called()
        urlopen.assert_not_called()
        self.assertEqual(200, response.status_code, response.text)
        body = response.json()
        self.assertEqual({"analysis", "draft", "metadata"}, set(body))
        self.assertEqual(
            {"document_id", "correlation_id", "source_cleanup_performed"},
            set(body["metadata"]),
        )
        self.assertEqual(document_id, body["metadata"]["document_id"])
        self.assertTrue(body["metadata"]["source_cleanup_performed"])
        self.assertEqual("candidate-from-client", self.draft_runtime.invocations[0][1])
        self.assertNotIn("provider-request-must-not-leak", response.text)
        self.assertNotIn("total_tokens", response.text)
        self.assertFalse(source_path.exists())
        self.assertIsNone(self.app.state.document_registry.get(document_id))

    def test_process_accepts_no_body(self) -> None:
        document_id, _ = self.upload()
        response = self.client.post(f"/api/documents/{document_id}/process")
        self.assertEqual(200, response.status_code, response.text)
        self.assertIsNone(self.draft_runtime.invocations[0][1])

    def test_process_rejects_extra_request_fields(self) -> None:
        document_id, _ = self.upload()
        response = self.client.post(
            f"/api/documents/{document_id}/process",
            json={"output_path": "C:/sensitive/output.docx"},
        )
        self.assertEqual(422, response.status_code, response.text)
        self.assertEqual("invalid_request", response.json()["error"]["code"])
        self.assertNotIn("sensitive", response.text)
        self.assertTrue(self.app.state.document_storage.path_for(document_id).exists())

    def test_process_maps_typed_error_and_preserves_cleanup(self) -> None:
        failing_app = create_app(
            Settings(
                storage_root=self.root / "failing-uploads",
                local_export_root=self.root / "failing-exports",
                enable_local_orchestration_api=True,
            ),
            extraction_runtime=FailingExtractionRuntime(),
            draft_runtime=RecordingDraftRuntime(),
            docx_renderer=PatentDocxRenderer(output_root=self.root / "failing-exports"),
        )
        with TestClient(failing_app) as client:
            _, upload = self._upload_with(client)
            document_id = upload["document_id"]
            source_path = failing_app.state.document_storage.path_for(document_id)
            response = client.post(f"/api/documents/{document_id}/process")
        self.assertEqual(504, response.status_code, response.text)
        self.assertEqual("provider_timeout", response.json()["error"]["code"])
        self.assertIn("correlation_id", response.json()["error"])
        self.assertFalse(source_path.exists())

    def test_validate_edited_revision_returns_exact_digest_and_unverified_paths(self) -> None:
        context = self.draft_context()
        context["revision_id"] = "revision-2"
        context["draft"]["draft_sections"][0]["paragraphs"][0]["text"] += " The coefficient remains source-linked."
        with (
            patch("socket.create_connection") as connect,
            patch("urllib.request.urlopen") as urlopen,
        ):
            response = self.client.post("/api/drafts/validate", json=context)
        connect.assert_not_called()
        urlopen.assert_not_called()
        self.assertEqual(200, response.status_code, response.text)
        self.assertEqual("revision-2", response.json()["revision_id"])
        self.assertTrue(response.json()["valid"])
        self.assertEqual(draft_digest(context["draft"], "revision-2"), response.json()["draft_digest"])
        self.assertEqual(
            ["/draft_sections/0/paragraphs/0/text"], response.json()["unverified_prose_paths"]
        )
        self.assertEqual(response.headers["x-correlation-id"], response.json()["correlation_id"])

    def test_validate_rejects_schema_business_source_and_pointer_failures(self) -> None:
        cases = (
            ("schema", lambda body: body["draft"].update({"claims": []}), "invalid_patent_draft"),
            ("source", lambda body: body["analysis"]["document_metadata"].update({"document_id": "other-id"}), "invalid_draft_grounding"),
            ("pointer", lambda body: body["draft"]["draft_sections"][0]["paragraphs"][0]["source_paths"].__setitem__(0, "/no-such-source"), "invalid_draft_grounding"),
            ("evidence", lambda body: body["draft"]["draft_sections"][0]["paragraphs"][0]["grounding"]["evidence_ids"].__setitem__(0, "unknown-evidence"), "invalid_draft_grounding"),
        )
        for name, change, expected_code in cases:
            with self.subTest(name=name):
                context = self.draft_context()
                change(context)
                response = self.client.post("/api/drafts/validate", json=context)
                self.assertEqual(422, response.status_code, response.text)
                self.assertEqual(expected_code, response.json()["error"]["code"])
                self.assertTrue(response.json()["error"].get("paths"))
                self.assertEqual(response.headers["x-correlation-id"], response.json()["error"]["correlation_id"])
                self.assertNotIn("no-such-source", response.text)
                self.assertNotIn(str(self.root), response.text)

        malformed_analysis = self.draft_context()
        malformed_analysis["analysis"]["unapproved_field"] = "must not leak"
        response = self.client.post("/api/drafts/validate", json=malformed_analysis)
        self.assertEqual(422, response.status_code, response.text)
        self.assertEqual("invalid_source_analysis", response.json()["error"]["code"])
        self.assertNotIn("must not leak", response.text)

    def test_validate_rejects_protected_change_and_abstract_count_errors(self) -> None:
        protected = self.draft_context()
        protected["draft"]["document_metadata"]["draft_id"] = "changed-draft-id"
        response = self.client.post("/api/drafts/validate", json=protected)
        self.assertEqual("protected_draft_field_changed", response.json()["error"]["code"])
        self.assertIn("/document_metadata/draft_id", response.json()["error"]["paths"])

        valid = self.draft_context()
        valid["draft"]["abstract"]["text"] = "A calibrated optical sensor uses a measured temperature coefficient."
        valid["draft"]["abstract"]["word_count"] = 9
        response = self.client.post("/api/drafts/validate", json=valid)
        self.assertEqual(200, response.status_code, response.text)

        invalid_count = copy.deepcopy(valid)
        invalid_count["draft"]["abstract"]["word_count"] = 8
        response = self.client.post("/api/drafts/validate", json=invalid_count)
        self.assertEqual(422, response.status_code, response.text)
        self.assertIn("/abstract/word_count", response.json()["error"]["paths"])

        over_limit = self.draft_context()
        over_limit["draft"]["abstract"]["text"] = "word " * 151
        over_limit["draft"]["abstract"]["word_count"] = 151
        response = self.client.post("/api/drafts/validate", json=over_limit)
        self.assertEqual(422, response.status_code, response.text)

    def test_malformed_json_validation_and_export_requests_fail_safely(self) -> None:
        for path in ("/api/drafts/validate", "/api/exports/docx"):
            with self.subTest(path=path):
                response = self.client.post(
                    path,
                    content=b'{"revision_id":"synthetic",',
                    headers={"content-type": "application/json"},
                )
                self.assertEqual(422, response.status_code, response.text)
                self.assertEqual("invalid_request", response.json()["error"]["code"])
                self.assertEqual(
                    response.headers["x-correlation-id"],
                    response.json()["error"]["correlation_id"],
                )
                self.assertNotIn("Traceback", response.text)
                self.assertNotIn(str(self.root), response.text)
        self.assertEqual([], self.draft_runtime.invocations)
        self.assertEqual([], list(self.export_root.glob("*.docx")))

    def test_export_requires_exact_validated_revision_and_revalidates(self) -> None:
        body = self.validated_export_context(self.draft_context())
        stale = copy.deepcopy(body)
        stale["draft"]["draft_sections"][0]["paragraphs"][0]["text"] += " Changed after validation."
        response = self.client.post("/api/exports/docx", json=stale)
        self.assertEqual(409, response.status_code, response.text)
        self.assertEqual("stale_draft_revision", response.json()["error"]["code"])
        self.assertEqual([], list(self.export_root.glob("*.docx")))

        invalid = copy.deepcopy(body)
        invalid["draft"]["draft_sections"][0]["paragraphs"][0]["source_paths"][0] = "/bad"
        invalid["validated_digest"] = draft_digest(invalid["draft"], invalid["revision_id"])
        with patch.object(self.app.state.patent_docx_renderer, "render") as render:
            response = self.client.post("/api/exports/docx", json=invalid)
        render.assert_not_called()
        self.assertEqual(422, response.status_code, response.text)
        self.assertEqual("invalid_draft_grounding", response.json()["error"]["code"])

        wrong_source = copy.deepcopy(body)
        wrong_source["analysis"]["document_metadata"]["document_id"] = "different"
        response = self.client.post("/api/exports/docx", json=wrong_source)
        self.assertEqual(422, response.status_code, response.text)
        self.assertEqual([], list(self.export_root.glob("*.docx")))

        over_limit = copy.deepcopy(body)
        over_limit["draft"]["abstract"]["text"] = "word " * 151
        over_limit["draft"]["abstract"]["word_count"] = 151
        over_limit["validated_digest"] = draft_digest(over_limit["draft"], over_limit["revision_id"])
        response = self.client.post("/api/exports/docx", json=over_limit)
        self.assertEqual(422, response.status_code, response.text)
        self.assertEqual([], list(self.export_root.glob("*.docx")))

    def test_revision_id_change_invalidates_previously_validated_digest(self) -> None:
        body = self.validated_export_context(self.draft_context())
        body["revision_id"] = "revision-2"
        with patch.object(self.app.state.patent_docx_renderer, "render") as render:
            response = self.client.post("/api/exports/docx", json=body)
        render.assert_not_called()
        self.assertEqual(409, response.status_code, response.text)
        self.assertEqual("stale_draft_revision", response.json()["error"]["code"])
        self.assertEqual([], list(self.export_root.glob("*.docx")))

    def test_export_returns_editable_docx_and_removes_temporary_file(self) -> None:
        context = self.draft_context()
        context["revision_id"] = "revision-2"
        context["draft"]["draft_sections"][0]["paragraphs"][0]["text"] += " Calibration remains temperature-aware."
        body = self.validated_export_context(context)
        with (
            patch("socket.create_connection") as connect,
            patch("urllib.request.urlopen") as urlopen,
        ):
            response = self.client.post("/api/exports/docx", json=body)
        connect.assert_not_called()
        urlopen.assert_not_called()
        self.assertEqual(200, response.status_code, response.text)
        self.assertEqual(DOCX_MEDIA_TYPE, response.headers["content-type"])
        self.assertIn(
            'filename="patent-description-draft.docx"',
            response.headers["content-disposition"],
        )
        with zipfile.ZipFile(io.BytesIO(response.content)) as package:
            self.assertIsNone(package.testzip())
            self.assertIn("word/document.xml", package.namelist())
            self.assertIn(b"Calibration remains temperature-aware.", package.read("word/document.xml"))
        self.assertEqual([], list(self.export_root.glob("*.docx")))

    def test_export_rejects_invalid_draft_without_output_or_path_disclosure(self) -> None:
        context = self.draft_context()
        context["draft"]["claims"] = []
        response = self.client.post("/api/exports/docx", json={
            **context, "validated_digest": draft_digest(context["draft"], context["revision_id"])
        })
        self.assertEqual(422, response.status_code, response.text)
        self.assertEqual("invalid_patent_draft", response.json()["error"]["code"])
        self.assertIn("correlation_id", response.json()["error"])
        self.assertNotIn(str(self.export_root), response.text)
        self.assertEqual([], list(self.export_root.glob("*.docx")))

    def test_export_rejects_client_output_path(self) -> None:
        response = self.client.post(
            "/api/exports/docx",
            json={
                **self.validated_export_context(self.draft_context()),
                "output_path": "C:/client-selected.docx",
            },
        )
        self.assertEqual(422, response.status_code, response.text)
        self.assertEqual("invalid_request", response.json()["error"]["code"])
        self.assertNotIn("client-selected", response.text)

    def test_export_internal_failure_is_generic_and_cleans_partial_output(self) -> None:
        failing_app = create_app(
            Settings(
                storage_root=self.root / "render-failure-uploads",
                local_export_root=self.root / "render-failure-exports",
                enable_local_orchestration_api=True,
            ),
            extraction_runtime=self.extraction_runtime,
            draft_runtime=self.draft_runtime,
            docx_renderer=ExplodingRenderer(),
        )
        context = self.draft_context()
        with TestClient(failing_app, raise_server_exceptions=False) as client:
            response = client.post(
                "/api/exports/docx",
                json={**context, "validated_digest": draft_digest(context["draft"], context["revision_id"])},
            )
        self.assertEqual(500, response.status_code, response.text)
        self.assertEqual("docx_render_failed", response.json()["error"]["code"])
        self.assertNotIn("sensitive renderer detail", response.text)
        self.assertNotIn(str(self.root), response.text)
        self.assertEqual([], list((self.root / "render-failure-exports").glob("*.docx")))

    def test_enabled_openapi_adds_only_approved_public_business_routes(self) -> None:
        paths = {
            (method.upper(), path)
            for path, operations in self.app.openapi()["paths"].items()
            for method in operations
        }
        self.assertEqual(
            {
                ("GET", "/health"),
                ("POST", "/api/documents"),
                ("GET", "/api/documents/{document_id}"),
                ("POST", "/api/documents/{document_id}/process"),
                ("POST", "/api/exports/docx"),
                ("POST", "/api/drafts/validate"),
            },
            paths,
        )


if __name__ == "__main__":
    unittest.main()
