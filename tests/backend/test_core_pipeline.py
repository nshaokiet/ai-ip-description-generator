from __future__ import annotations

import inspect
import unittest
from typing import Any

from backend.app.schemas.analysis_input import ExtractionInputEnvelope
from backend.app.services.core_pipeline import (
    CorePipelineOrchestrator,
    PipelineOrchestrationError,
)
from backend.app.services.document_parsing import DocumentPreparationError
from backend.app.services.draft_runtime import (
    DraftRuntimeError,
    DraftRuntimeMetadata,
    DraftRuntimeResult,
)
from backend.app.services.extraction_runtime import (
    ExtractionRuntimeError,
    ExtractionRuntimeMetadata,
    ExtractionRuntimeResult,
)


class FakeStorage:
    def __init__(
        self,
        events: list[str],
        *,
        delete_result: bool = True,
        delete_error: Exception | None = None,
    ) -> None:
        self.events = events
        self.delete_result = delete_result
        self.delete_error = delete_error
        self.deleted_ids: list[str] = []

    def delete(self, document_id: str) -> bool:
        self.events.append("cleanup")
        self.deleted_ids.append(document_id)
        if self.delete_error is not None:
            raise self.delete_error
        return self.delete_result


class FakePreparationService:
    def __init__(
        self,
        envelope: ExtractionInputEnvelope,
        events: list[str],
        *,
        error: Exception | None = None,
    ) -> None:
        self.envelope = envelope
        self.events = events
        self.error = error
        self.document_ids: list[str] = []

    def prepare_extraction_input(self, document_id: str) -> ExtractionInputEnvelope:
        self.events.append("preparation")
        self.document_ids.append(document_id)
        if self.error is not None:
            raise self.error
        return self.envelope


class FakeExtractionRuntime:
    def __init__(
        self,
        analysis: dict[str, Any],
        events: list[str],
        *,
        error: Exception | None = None,
    ) -> None:
        self.analysis = analysis
        self.events = events
        self.error = error
        self.invocations: list[tuple[ExtractionInputEnvelope, str | None]] = []

    def run_extraction(
        self,
        envelope: ExtractionInputEnvelope,
        *,
        correlation_id: str | None = None,
    ) -> ExtractionRuntimeResult:
        self.events.append("extraction")
        self.invocations.append((envelope, correlation_id))
        if self.error is not None:
            raise self.error
        return ExtractionRuntimeResult(
            analysis=self.analysis,
            runtime=ExtractionRuntimeMetadata(
                provider="fake_openai",
                model="gpt-5.6-sol",
                request_id="fake_extract_request",
                status="completed",
                duration_ms=10,
                usage={"input_tokens": 10, "output_tokens": 20, "total_tokens": 30},
            ),
        )


class FakeDraftRuntime:
    def __init__(
        self,
        draft: dict[str, Any],
        events: list[str],
        *,
        error: Exception | None = None,
    ) -> None:
        self.draft = draft
        self.events = events
        self.error = error
        self.invocations: list[tuple[dict[str, Any], str | None]] = []

    def run_draft_generation(
        self,
        source_analysis: dict[str, Any],
        selected_title_candidate_id: str | None = None,
    ) -> DraftRuntimeResult:
        self.events.append("draft_generation")
        self.invocations.append((source_analysis, selected_title_candidate_id))
        if self.error is not None:
            raise self.error
        return DraftRuntimeResult(
            draft=self.draft,
            runtime=DraftRuntimeMetadata(
                provider="fake_openai",
                model="gpt-5.6-sol",
                request_id="fake_draft_request",
                status="completed",
                duration_ms=12,
                usage={"input_tokens": 20, "output_tokens": 40, "total_tokens": 60},
            ),
        )


class CorePipelineOrchestratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.document_id = "a" * 32
        self.events: list[str] = []
        self.envelope = ExtractionInputEnvelope.model_validate(
            {
                "document_metadata": {
                    "document_id": self.document_id,
                    "file_name": "synthetic.pdf",
                    "media_type": "application/pdf",
                    "sha256": "b" * 64,
                },
                "source_units": [
                    {
                        "evidence_id": "EV-P0001-C001",
                        "evidence_type": "TEXT",
                        "locator": {"page": 1, "chunk_id": "P0001-C001"},
                        "content": "Synthetic source content that must never appear in logs.",
                    }
                ],
            }
        )
        self.analysis = {
            "output_type": "STRUCTURED_INVENTION_ANALYSIS",
            "document_metadata": self.envelope.document_metadata.model_dump(exclude_none=True),
        }
        self.draft = {"output_type": "PATENT_DESCRIPTION_DRAFT"}

    def orchestrator(
        self,
        *,
        storage: FakeStorage | None = None,
        preparation_error: Exception | None = None,
        extraction_error: Exception | None = None,
        draft_error: Exception | None = None,
    ) -> tuple[
        CorePipelineOrchestrator,
        FakeStorage,
        FakePreparationService,
        FakeExtractionRuntime,
        FakeDraftRuntime,
    ]:
        actual_storage = storage or FakeStorage(self.events)
        preparation = FakePreparationService(
            self.envelope,
            self.events,
            error=preparation_error,
        )
        extraction = FakeExtractionRuntime(
            self.analysis,
            self.events,
            error=extraction_error,
        )
        draft = FakeDraftRuntime(self.draft, self.events, error=draft_error)
        pipeline = CorePipelineOrchestrator(
            actual_storage,  # type: ignore[arg-type]
            preparation,
            extraction,
            draft,
        )
        return pipeline, actual_storage, preparation, extraction, draft

    def test_initializes_without_document_registry_dependency(self) -> None:
        pipeline, _, preparation, extraction, draft = self.orchestrator()
        self.assertIs(preparation, pipeline.preparation_service)
        self.assertIs(extraction, pipeline.extraction_runtime)
        self.assertIs(draft, pipeline.draft_runtime)
        self.assertFalse(hasattr(pipeline, "registry"))

    def test_success_runs_stages_in_order_and_cleans_up_once(self) -> None:
        pipeline, storage, _, extraction, draft = self.orchestrator()
        result = pipeline.run_pipeline(
            self.document_id,
            selected_title_candidate_id="title-001",
            correlation_id="correlation-001",
        )
        self.assertEqual(
            ["preparation", "extraction", "draft_generation", "cleanup"],
            self.events,
        )
        self.assertEqual([self.document_id], storage.deleted_ids)
        self.assertEqual(self.analysis, result.analysis)
        self.assertEqual(self.draft, result.draft)
        self.assertEqual("correlation-001", result.metadata.correlation_id)
        self.assertTrue(result.metadata.source_cleanup_performed)
        self.assertEqual(1, len(extraction.invocations))
        self.assertEqual(1, len(draft.invocations))

    def test_success_metadata_has_exact_stage_names_and_runtime_fields(self) -> None:
        pipeline, *_ = self.orchestrator()
        result = pipeline.run_pipeline(self.document_id, correlation_id="correlation-002")
        self.assertEqual(
            ["preparation", "extraction", "draft_generation"],
            [stage.stage for stage in result.metadata.stages],
        )
        self.assertTrue(all(stage.status == "completed" for stage in result.metadata.stages))
        self.assertEqual("fake_extract_request", result.metadata.stages[1].provider_request_id)
        self.assertEqual("fake_draft_request", result.metadata.stages[2].provider_request_id)
        self.assertEqual(30, result.metadata.stages[1].usage["total_tokens"])
        self.assertEqual(60, result.metadata.stages[2].usage["total_tokens"])
        self.assertTrue(all(stage.duration_ms >= 0 for stage in result.metadata.stages))
        self.assertGreaterEqual(result.metadata.total_duration_ms, 0)

    def test_exact_envelope_analysis_title_and_correlation_are_forwarded(self) -> None:
        pipeline, _, _, extraction, draft = self.orchestrator()
        pipeline.run_pipeline(
            self.document_id,
            selected_title_candidate_id="title-001",
            correlation_id="correlation-003",
        )
        self.assertIs(self.envelope, extraction.invocations[0][0])
        self.assertEqual("correlation-003", extraction.invocations[0][1])
        self.assertIs(self.analysis, draft.invocations[0][0])
        self.assertEqual("title-001", draft.invocations[0][1])

    def test_generated_correlation_id_is_uuid4_hex(self) -> None:
        pipeline, *_ = self.orchestrator()
        result = pipeline.run_pipeline(self.document_id)
        self.assertEqual(32, len(result.metadata.correlation_id))
        self.assertTrue(all(character in "0123456789abcdef" for character in result.metadata.correlation_id))

    def test_preparation_error_is_mapped_and_ai_runtimes_are_not_called(self) -> None:
        source = DocumentPreparationError("document_unknown", "The document is not registered.")
        pipeline, storage, _, extraction, draft = self.orchestrator(preparation_error=source)
        with self.assertRaises(PipelineOrchestrationError) as captured:
            pipeline.run_pipeline(self.document_id, correlation_id="correlation-004")
        error = captured.exception
        self.assertEqual(("preparation", "document_unknown"), (error.stage, error.code))
        self.assertEqual("The document is not registered.", error.safe_message)
        self.assertIs(source, error.__cause__)
        self.assertEqual([], extraction.invocations)
        self.assertEqual([], draft.invocations)
        self.assertEqual([self.document_id], storage.deleted_ids)

    def test_extraction_error_is_mapped_and_draft_is_not_called(self) -> None:
        source = ExtractionRuntimeError(
            "grounding_validation_failed",
            "The extraction output failed grounding validation.",
            paths=("/evidence/0",),
        )
        pipeline, storage, _, extraction, draft = self.orchestrator(extraction_error=source)
        with self.assertRaises(PipelineOrchestrationError) as captured:
            pipeline.run_pipeline(self.document_id, correlation_id="correlation-005")
        error = captured.exception
        self.assertEqual(("extraction", "grounding_validation_failed"), (error.stage, error.code))
        self.assertEqual(("/evidence/0",), error.paths)
        self.assertIs(source, error.__cause__)
        self.assertEqual(1, len(extraction.invocations))
        self.assertEqual([], draft.invocations)
        self.assertEqual([self.document_id], storage.deleted_ids)

    def test_draft_error_is_mapped_with_paths(self) -> None:
        source = DraftRuntimeError(
            "word_count_exceeded",
            "The Draft failed deterministic validation.",
            paths=("/abstract/word_count",),
        )
        pipeline, storage, _, extraction, draft = self.orchestrator(draft_error=source)
        with self.assertRaises(PipelineOrchestrationError) as captured:
            pipeline.run_pipeline(self.document_id, correlation_id="correlation-006")
        error = captured.exception
        self.assertEqual(("draft_generation", "word_count_exceeded"), (error.stage, error.code))
        self.assertEqual(("/abstract/word_count",), error.paths)
        self.assertIs(source, error.__cause__)
        self.assertEqual(1, len(extraction.invocations))
        self.assertEqual(1, len(draft.invocations))
        self.assertEqual([self.document_id], storage.deleted_ids)

    def test_cleanup_false_preserves_success_and_reports_unconfirmed_cleanup(self) -> None:
        storage = FakeStorage(self.events, delete_result=False)
        pipeline, *_ = self.orchestrator(storage=storage)
        with self.assertLogs("backend.app.services.core_pipeline", level="WARNING") as captured:
            result = pipeline.run_pipeline(self.document_id, correlation_id="correlation-007")
        self.assertEqual(self.analysis, result.analysis)
        self.assertEqual(self.draft, result.draft)
        self.assertFalse(result.metadata.source_cleanup_performed)
        self.assertIn("pipeline_source_cleanup_failed", "\n".join(captured.output))

    def test_cleanup_exception_preserves_success(self) -> None:
        storage = FakeStorage(self.events, delete_error=OSError("synthetic cleanup failure"))
        pipeline, *_ = self.orchestrator(storage=storage)
        with self.assertLogs("backend.app.services.core_pipeline", level="WARNING") as captured:
            result = pipeline.run_pipeline(self.document_id, correlation_id="correlation-008")
        self.assertEqual(self.draft, result.draft)
        self.assertFalse(result.metadata.source_cleanup_performed)
        self.assertNotIn("synthetic cleanup failure", "\n".join(captured.output))

    def test_cleanup_exception_does_not_mask_primary_error(self) -> None:
        source = ExtractionRuntimeError("provider_timeout", "The extraction provider timed out.")
        storage = FakeStorage(self.events, delete_error=ValueError("invalid identifier"))
        pipeline, *_ = self.orchestrator(storage=storage, extraction_error=source)
        with self.assertLogs("backend.app.services.core_pipeline", level="WARNING"):
            with self.assertRaises(PipelineOrchestrationError) as captured:
                pipeline.run_pipeline(self.document_id, correlation_id="correlation-009")
        self.assertEqual("provider_timeout", captured.exception.code)
        self.assertIs(source, captured.exception.__cause__)

    def test_malformed_document_id_cleanup_value_error_is_contained(self) -> None:
        malformed_id = "not-a-valid-document-id"
        source = DocumentPreparationError("document_unknown", "The document is not registered.")
        storage = FakeStorage(self.events, delete_error=ValueError("invalid opaque identifier"))
        pipeline, *_ = self.orchestrator(storage=storage, preparation_error=source)
        with self.assertLogs("backend.app.services.core_pipeline", level="WARNING") as captured:
            with self.assertRaises(PipelineOrchestrationError) as error:
                pipeline.run_pipeline(malformed_id, correlation_id="correlation-010")
        self.assertEqual("document_unknown", error.exception.code)
        logs = "\n".join(captured.output)
        self.assertIn("document_id=invalid", logs)
        self.assertNotIn(malformed_id, logs)

    def test_unexpected_exception_still_triggers_cleanup_without_reclassification(self) -> None:
        source = RuntimeError("synthetic unexpected preparation failure")
        pipeline, storage, *_ = self.orchestrator(preparation_error=source)
        with self.assertRaisesRegex(RuntimeError, "synthetic unexpected preparation failure"):
            pipeline.run_pipeline(self.document_id, correlation_id="correlation-011")
        self.assertEqual([self.document_id], storage.deleted_ids)

    def test_no_caller_cleanup_switch_exists(self) -> None:
        parameters = inspect.signature(CorePipelineOrchestrator.run_pipeline).parameters
        self.assertNotIn("cleanup_source", parameters)
        self.assertEqual(
            {"self", "document_id", "selected_title_candidate_id", "correlation_id"},
            set(parameters),
        )

    def test_repeated_fixed_input_has_deterministic_business_handoff(self) -> None:
        business_results: list[tuple[Any, ...]] = []
        for _ in range(2):
            self.events = []
            pipeline, _, _, extraction, draft = self.orchestrator()
            result = pipeline.run_pipeline(self.document_id, correlation_id="fixed-correlation")
            business_results.append(
                (
                    extraction.invocations[0][0].model_dump(mode="json"),
                    draft.invocations[0],
                    result.analysis,
                    result.draft,
                    tuple(stage.stage for stage in result.metadata.stages),
                )
            )
        self.assertEqual(business_results[0], business_results[1])

    def test_typed_stage_failure_is_not_retried(self) -> None:
        source = ExtractionRuntimeError("provider_timeout", "The extraction provider timed out.")
        pipeline, _, preparation, extraction, draft = self.orchestrator(extraction_error=source)
        with self.assertRaises(PipelineOrchestrationError):
            pipeline.run_pipeline(self.document_id, correlation_id="correlation-012")
        self.assertEqual([self.document_id], preparation.document_ids)
        self.assertEqual(1, len(extraction.invocations))
        self.assertEqual([], draft.invocations)

    def test_logs_exclude_source_analysis_draft_and_error_details(self) -> None:
        storage = FakeStorage(self.events, delete_result=False)
        pipeline, *_ = self.orchestrator(storage=storage)
        with self.assertLogs("backend.app.services.core_pipeline", level="INFO") as captured:
            pipeline.run_pipeline(self.document_id, correlation_id="correlation-013")
        logs = "\n".join(captured.output)
        self.assertNotIn("Synthetic source content", logs)
        self.assertNotIn("STRUCTURED_INVENTION_ANALYSIS", logs)
        self.assertNotIn("PATENT_DESCRIPTION_DRAFT", logs)
        self.assertNotIn(".pdf", logs)


if __name__ == "__main__":
    unittest.main()
