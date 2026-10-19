from __future__ import annotations

import copy
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.app.core.config import Settings
from backend.app.main import create_app
from backend.app.schemas.analysis_input import ExtractionInputEnvelope
from backend.app.services.core_pipeline import (
    CorePipelineOrchestrator,
    PipelineOrchestrationError,
)
from backend.app.services.draft_business_validation import validate_draft_business_rules
from backend.app.services.draft_runtime import DraftRuntimeError, DraftRuntimeMetadata, DraftRuntimeResult
from backend.app.services.draft_validation import validate_canonical_draft
from backend.app.services.document_validation import DOCX_MEDIA_TYPE, PDF_MEDIA_TYPE
from backend.app.services.extraction_runtime import (
    ExtractionRuntimeError,
    ExtractionRuntimeMetadata,
    ExtractionRuntimeResult,
)
from backend.app.services.extraction_validation import (
    validate_canonical_output,
    validate_grounding_and_business_rules,
)
from tests.backend.test_document_parsing import paragraph_xml, synthetic_docx, synthetic_pdf


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
ANALYSIS_SCHEMA_PATH = (
    REPOSITORY_ROOT / "schemas" / "invention-output" / "v1.0.0"
    / "invention-output.schema.json"
)
DRAFT_SCHEMA_PATH = (
    REPOSITORY_ROOT / "schemas" / "patent-draft" / "v1.0.0"
    / "patent-draft.schema.json"
)
MINIMAL_ANALYSIS_PATH = (
    REPOSITORY_ROOT / "tests" / "fixtures" / "invention-output" / "v1.0.0"
    / "valid" / "minimal.json"
)
MISSING_DRAFT_CASE_PATH = (
    REPOSITORY_ROOT / "tests" / "fixtures" / "patent-draft" / "v1.0.0"
    / "cases" / "missing-information.json"
)


def _load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as source:
        return json.load(source)


class ValidatingFakeExtractionRuntime:
    def __init__(self) -> None:
        self.analysis_schema = _load_json(ANALYSIS_SCHEMA_PATH)
        self.analysis_template = _load_json(MINIMAL_ANALYSIS_PATH)
        self.invocations: list[tuple[ExtractionInputEnvelope, str | None]] = []

    def run_extraction(
        self,
        envelope: ExtractionInputEnvelope,
        *,
        correlation_id: str | None = None,
    ) -> ExtractionRuntimeResult:
        self.invocations.append((envelope, correlation_id))
        analysis = copy.deepcopy(self.analysis_template)
        analysis["document_metadata"] = envelope.document_metadata.model_dump(exclude_none=True)
        validated = validate_canonical_output(analysis, self.analysis_schema)
        validate_grounding_and_business_rules(validated, envelope)
        return ExtractionRuntimeResult(
            analysis=validated,
            runtime=ExtractionRuntimeMetadata(
                provider="fake_openai",
                model="gpt-5.6-sol",
                request_id="fake_req_extract_e2e",
                status="completed",
                duration_ms=15,
                usage={"input_tokens": 100, "output_tokens": 200, "total_tokens": 300},
            ),
        )


class ValidatingFakeDraftRuntime:
    def __init__(self) -> None:
        fixture = _load_json(MISSING_DRAFT_CASE_PATH)
        self.draft_template = fixture["expected_output"]
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
        validated = validate_canonical_draft(draft, self.draft_schema)
        validate_draft_business_rules(
            validated,
            source_analysis,
            selected_title_candidate_id=selected_title_candidate_id,
        )
        return DraftRuntimeResult(
            draft=validated,
            runtime=DraftRuntimeMetadata(
                provider="fake_openai",
                model="gpt-5.6-sol",
                request_id="fake_req_draft_e2e",
                status="completed",
                duration_ms=25,
                usage={"input_tokens": 200, "output_tokens": 400, "total_tokens": 600},
            ),
        )


class CorePipelineOfflineE2ETests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.storage_root = Path(self.temporary_directory.name)
        self.settings = Settings(storage_root=self.storage_root)
        self.app = create_app(self.settings)
        self.client_context = TestClient(self.app)
        self.client = self.client_context.__enter__()

    def tearDown(self) -> None:
        self.client_context.__exit__(None, None, None)
        self.temporary_directory.cleanup()

    def upload(self, filename: str, payload: bytes, media_type: str) -> str:
        response = self.client.post(
            "/api/documents",
            files={"file": (filename, payload, media_type)},
        )
        self.assertEqual(201, response.status_code, response.text)
        document_id = response.json()["document_id"]
        self.assertRegex(document_id, r"^[a-f][0-9a-f]{31}$")
        return document_id

    def pipeline(
        self,
    ) -> tuple[
        CorePipelineOrchestrator,
        ValidatingFakeExtractionRuntime,
        ValidatingFakeDraftRuntime,
    ]:
        extraction = ValidatingFakeExtractionRuntime()
        draft = ValidatingFakeDraftRuntime()
        pipeline = CorePipelineOrchestrator(
            self.app.state.document_storage,
            self.app.state.document_preparation_service,
            extraction,
            draft,
        )
        return pipeline, extraction, draft

    def assert_successful_offline_pipeline(
        self,
        filename: str,
        payload: bytes,
        media_type: str,
    ) -> None:
        document_id = self.upload(filename, payload, media_type)
        source_path = self.app.state.document_storage.path_for(document_id)
        self.assertTrue(source_path.exists())
        pipeline, extraction, draft = self.pipeline()

        with (
            patch.dict(os.environ, {"OPENAI_API_KEY": ""}),
            patch("socket.create_connection") as connect,
            patch("urllib.request.urlopen") as urlopen,
        ):
            result = pipeline.run_pipeline(
                document_id,
                correlation_id="offline-e2e-correlation",
            )

        connect.assert_not_called()
        urlopen.assert_not_called()
        self.assertEqual("STRUCTURED_INVENTION_ANALYSIS", result.analysis["output_type"])
        self.assertEqual("PATENT_DESCRIPTION_DRAFT", result.draft["output_type"])
        self.assertEqual(document_id, result.analysis["document_metadata"]["document_id"])
        self.assertEqual(
            result.analysis["document_metadata"],
            result.draft["document_metadata"]["source_document"],
        )
        self.assertEqual(1, len(extraction.invocations))
        self.assertEqual(1, len(draft.invocations))
        self.assertIs(result.analysis, draft.invocations[0][0])
        self.assertEqual(
            ["preparation", "extraction", "draft_generation"],
            [stage.stage for stage in result.metadata.stages],
        )
        self.assertTrue(result.metadata.source_cleanup_performed)
        self.assertFalse(source_path.exists())
        self.assertIsNone(self.app.state.document_registry.get(document_id))

    def test_pdf_document_reaches_validated_draft_json_offline(self) -> None:
        self.assert_successful_offline_pipeline(
            "synthetic.pdf",
            synthetic_pdf(["Synthetic optical sensor source for offline orchestration."]),
            PDF_MEDIA_TYPE,
        )

    def test_docx_document_reaches_validated_draft_json_offline(self) -> None:
        self.assert_successful_offline_pipeline(
            "synthetic.docx",
            synthetic_docx([paragraph_xml("Synthetic DOCX source for offline orchestration.")]),
            DOCX_MEDIA_TYPE,
        )

    def test_integrity_failure_maps_to_preparation_and_cleans_source(self) -> None:
        document_id = self.upload(
            "integrity.pdf",
            synthetic_pdf(["Original synthetic source."]),
            PDF_MEDIA_TYPE,
        )
        source_path = self.app.state.document_storage.path_for(document_id)
        source_path.write_bytes(b"tampered synthetic bytes")
        pipeline, extraction, draft = self.pipeline()
        with self.assertRaises(PipelineOrchestrationError) as captured:
            pipeline.run_pipeline(document_id, correlation_id="offline-integrity")
        self.assertEqual(("preparation", "parse_failed"), (captured.exception.stage, captured.exception.code))
        self.assertEqual([], extraction.invocations)
        self.assertEqual([], draft.invocations)
        self.assertFalse(source_path.exists())
        self.assertIsNone(self.app.state.document_registry.get(document_id))

    def test_unknown_document_fails_without_runtime_calls(self) -> None:
        pipeline, extraction, draft = self.pipeline()
        with self.assertRaises(PipelineOrchestrationError) as captured:
            pipeline.run_pipeline("f" * 32, correlation_id="offline-unknown")
        self.assertEqual(("preparation", "document_unknown"), (captured.exception.stage, captured.exception.code))
        self.assertEqual([], extraction.invocations)
        self.assertEqual([], draft.invocations)

    def test_deleted_source_is_rejected_without_provider_or_source_remnants(self) -> None:
        document_id = self.upload(
            "deleted.pdf", synthetic_pdf(["Synthetic deleted source."]), PDF_MEDIA_TYPE
        )
        self.assertTrue(self.app.state.document_storage.delete(document_id))
        pipeline, extraction, draft = self.pipeline()
        with self.assertRaises(PipelineOrchestrationError) as captured:
            pipeline.run_pipeline(document_id)
        self.assertEqual("document_unknown", captured.exception.code)
        self.assertEqual([], extraction.invocations)
        self.assertEqual([], draft.invocations)
        self.assertFalse(self.app.state.document_storage.path_for(document_id).exists())

    def test_extraction_refusal_and_draft_incomplete_clean_source(self) -> None:
        for stage, failure in (
            ("extraction", ExtractionRuntimeError("model_refusal", "Safe extraction refusal")),
            ("draft_generation", DraftRuntimeError("model_incomplete", "Safe incomplete draft")),
        ):
            with self.subTest(stage=stage):
                document_id = self.upload(
                    f"{stage}.pdf",
                    synthetic_pdf(["Synthetic isolated failure case."]),
                    PDF_MEDIA_TYPE,
                )
                pipeline, extraction, draft = self.pipeline()
                target = extraction if stage == "extraction" else draft
                method = "run_extraction" if stage == "extraction" else "run_draft_generation"
                with patch.object(target, method, side_effect=failure):
                    with self.assertRaises(PipelineOrchestrationError) as captured:
                        pipeline.run_pipeline(document_id)
                self.assertEqual(stage, captured.exception.stage)
                self.assertEqual(failure.code, captured.exception.code)
                self.assertNotIn(str(self.storage_root), str(captured.exception))
                self.assertFalse(self.app.state.document_storage.path_for(document_id).exists())
                self.assertIsNone(self.app.state.document_registry.get(document_id))
                if stage == "extraction":
                    self.assertEqual([], draft.invocations)

    def test_registry_lookup_occurs_only_inside_preparation_service(self) -> None:
        document_id = self.upload(
            "lookup.pdf",
            synthetic_pdf(["Synthetic registry lookup source."]),
            PDF_MEDIA_TYPE,
        )
        pipeline, _, _ = self.pipeline()
        registry = self.app.state.document_registry
        with patch.object(registry, "get", wraps=registry.get) as lookup:
            pipeline.run_pipeline(document_id, correlation_id="offline-lookup")
        self.assertEqual(1, lookup.call_count)

    def test_public_business_routes_are_unchanged(self) -> None:
        business_routes = {
            (method.upper(), path)
            for path, operation in self.app.openapi()["paths"].items()
            for method in operation
        }
        self.assertEqual(
            {("GET", "/health"), ("POST", "/api/documents")},
            business_routes,
        )
        route_paths = set(self.app.openapi()["paths"])
        self.assertNotIn("/api/pipeline", route_paths)
        self.assertNotIn("/api/documents/{id}/analyze", route_paths)
        self.assertNotIn("/api/documents/{id}/generate-draft", route_paths)

    def test_framework_documentation_routes_remain_available(self) -> None:
        for path in ("/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"):
            response = self.client.get(path)
            self.assertNotEqual(404, response.status_code, path)

    def test_real_app001_id_satisfies_ai001_canonical_identifier(self) -> None:
        document_id = self.upload(
            "identifier-contract.pdf",
            synthetic_pdf(["Synthetic identifier-contract evidence."]),
            PDF_MEDIA_TYPE,
        )
        envelope = self.app.state.document_preparation_service.prepare_extraction_input(
            document_id
        )
        analysis = _load_json(MINIMAL_ANALYSIS_PATH)
        analysis["document_metadata"] = envelope.document_metadata.model_dump(exclude_none=True)
        validated = validate_canonical_output(
            analysis,
            _load_json(ANALYSIS_SCHEMA_PATH),
        )
        self.assertEqual(document_id, validated["document_metadata"]["document_id"])
        self.app.state.document_storage.delete(document_id)

    def test_repeated_synthetic_inputs_have_deterministic_business_shape(self) -> None:
        payload = synthetic_docx([paragraph_xml("Deterministic synthetic source.")])
        normalized_outputs: list[tuple[dict, dict, tuple[str, ...]]] = []
        for index in range(2):
            document_id = self.upload(f"deterministic-{index}.docx", payload, DOCX_MEDIA_TYPE)
            pipeline, _, _ = self.pipeline()
            result = pipeline.run_pipeline(document_id, correlation_id="fixed-e2e-correlation")
            analysis = copy.deepcopy(result.analysis)
            draft = copy.deepcopy(result.draft)
            analysis["document_metadata"]["document_id"] = "<document-id>"
            analysis["document_metadata"]["file_name"] = "<file-name>"
            draft["document_metadata"]["source_document"]["document_id"] = "<document-id>"
            draft["document_metadata"]["source_document"]["file_name"] = "<file-name>"
            normalized_outputs.append(
                (analysis, draft, tuple(stage.stage for stage in result.metadata.stages))
            )
        self.assertEqual(normalized_outputs[0], normalized_outputs[1])


if __name__ == "__main__":
    unittest.main()
