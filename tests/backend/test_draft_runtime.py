from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import httpx2
import openai

from backend.app.core.config import Settings
from backend.app.services.draft_provider_schema import PATENT_DRAFT_PROVIDER_SCHEMA_NAME
from backend.app.services.draft_runtime import (
    DRAFT_SCHEMA_PATH,
    DRAFT_PROMPT_PATH,
    DraftRuntimeError,
    OpenAIDraftRuntime,
    build_draft_input_envelope,
)
from backend.app.services.draft_validation import (
    normalize_draft_provider_output,
    validate_canonical_draft,
)
from backend.app.services.draft_business_validation import validate_draft_business_rules
from tests.backend.runtime_test_support import FakeClient, fake_response, load_json


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
REPRESENTATIVE_FIXTURE = (
    REPOSITORY_ROOT / "tests" / "fixtures" / "patent-draft" / "v1.0.0"
    / "cases" / "representative.json"
)
MISSING_INFORMATION_FIXTURE = (
    REPOSITORY_ROOT / "tests" / "fixtures" / "patent-draft" / "v1.0.0"
    / "cases" / "missing-information.json"
)


class OpenAIDraftRuntimePlumbingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.settings = Settings(storage_root=Path(self.temporary_directory.name))
        fixture = load_json(REPRESENTATIVE_FIXTURE)
        self.source_analysis = fixture["input"]["source_analysis"]
        self.expected_draft = fixture["expected_output"]
        self.selected_title_candidate_id = fixture["input"]["generation_config"][
            "selected_title_candidate_id"
        ]
        self.missing_information_fixture = load_json(MISSING_INFORMATION_FIXTURE)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def runtime(
        self,
        *,
        response=None,
        error=None,
        **kwargs,
    ) -> tuple[OpenAIDraftRuntime, FakeClient]:
        client = FakeClient(response=response, error=error)
        return OpenAIDraftRuntime(self.settings, client=client, **kwargs), client

    def assert_runtime_error(
        self,
        runtime: OpenAIDraftRuntime,
        expected_code: str,
        *,
        selected_title_candidate_id: str | None = None,
    ) -> DraftRuntimeError:
        with self.assertRaises(DraftRuntimeError) as captured:
            runtime.run_draft_generation(
                self.source_analysis,
                selected_title_candidate_id,
            )
        self.assertEqual(expected_code, captured.exception.code)
        self.assertNotIn("Temperature-dependent drift", captured.exception.safe_message)
        return captured.exception

    def test_valid_source_reaches_provider_exactly_once(self) -> None:
        runtime, client = self.runtime(response=fake_response(self.expected_draft))
        result = runtime.run_draft_generation(
            self.source_analysis,
            self.selected_title_candidate_id,
        )
        self.assertEqual(self.expected_draft, result.draft)
        self.assertEqual(1, len(client.responses.calls))

    def test_invalid_source_schema_fails_before_provider_call(self) -> None:
        self.source_analysis["schema_version"] = "2.0.0"
        runtime, client = self.runtime(response=fake_response(self.expected_draft))
        error = self.assert_runtime_error(runtime, "draft_input_invalid")
        self.assertIn("/schema_version", error.paths)
        self.assertEqual([], client.responses.calls)

    def test_duplicate_source_logical_id_fails_before_provider_call(self) -> None:
        self.source_analysis["components"][1]["component_id"] = self.source_analysis[
            "components"
        ][0]["component_id"]
        runtime, client = self.runtime(response=fake_response(self.expected_draft))
        error = self.assert_runtime_error(runtime, "draft_input_invalid")
        self.assertIn("source_analysis/components/1/component_id", error.paths)
        self.assertEqual([], client.responses.calls)

    def test_invalid_source_cross_reference_fails_before_provider_call(self) -> None:
        self.source_analysis["technical_solutions"][0]["addresses_problem_ids"] = [
            "missing-problem"
        ]
        runtime, client = self.runtime(response=fake_response(self.expected_draft))
        error = self.assert_runtime_error(runtime, "draft_input_invalid")
        self.assertIn(
            "/source_analysis/technical_solutions/0/addresses_problem_ids/0",
            error.paths,
        )
        self.assertEqual([], client.responses.calls)

    def test_missing_provider_configuration_is_safe(self) -> None:
        runtime = OpenAIDraftRuntime(self.settings)
        self.assert_runtime_error(runtime, "draft_runtime_not_configured")

    def test_provider_schema_error_is_mapped_before_provider_call(self) -> None:
        from backend.app.services.draft_provider_schema import DraftProviderSchemaError

        runtime, client = self.runtime(response=fake_response(self.expected_draft))
        with patch(
            "backend.app.services.draft_runtime.build_draft_provider_schema",
            side_effect=DraftProviderSchemaError("unsafe synthetic schema"),
        ):
            self.assert_runtime_error(runtime, "provider_schema_failed")
        self.assertEqual([], client.responses.calls)

    def test_request_uses_locked_responses_api_policy(self) -> None:
        runtime, client = self.runtime(response=fake_response(self.expected_draft))
        runtime.run_draft_generation(
            self.source_analysis,
            self.selected_title_candidate_id,
        )
        request = client.responses.calls[0]
        self.assertEqual("gpt-5.6-sol", request["model"])
        self.assertEqual({"effort": "high"}, request["reasoning"])
        self.assertIs(False, request["store"])
        self.assertIs(False, request["stream"])
        self.assertIs(False, request["background"])
        self.assertEqual(64_000, request["max_output_tokens"])
        self.assertNotIn("tools", request)
        self.assertNotIn("conversation", request)
        self.assertNotIn("previous_response_id", request)
        self.assertEqual(
            PATENT_DRAFT_PROVIDER_SCHEMA_NAME,
            request["text"]["format"]["name"],
        )
        self.assertEqual("json_schema", request["text"]["format"]["type"])
        self.assertIs(True, request["text"]["format"]["strict"])

    def test_valid_title_selection_is_represented_exactly(self) -> None:
        runtime, client = self.runtime(response=fake_response(self.expected_draft))
        runtime.run_draft_generation(
            self.source_analysis,
            self.selected_title_candidate_id,
        )
        envelope = json.loads(client.responses.calls[0]["input"])
        self.assertEqual(
            self.selected_title_candidate_id,
            envelope["generation_config"]["selected_title_candidate_id"],
        )
        self.assertEqual(self.source_analysis, envelope["source_analysis"])

    def test_absent_or_invalid_title_selection_is_omitted(self) -> None:
        for selected_title_candidate_id in (None, "unknown-title"):
            with self.subTest(selected_title_candidate_id=selected_title_candidate_id):
                envelope = build_draft_input_envelope(
                    self.source_analysis,
                    selected_title_candidate_id,
                )
                self.assertNotIn(
                    "selected_title_candidate_id",
                    envelope["generation_config"],
                )
                self.assertEqual("1.0.0", envelope["input_contract_version"])
                self.assertEqual(
                    "GENERATE_PATENT_DESCRIPTION_DRAFT",
                    envelope["task"],
                )
                self.assertEqual(
                    "[AUTHOR CONFIRMATION REQUIRED]",
                    envelope["generation_config"]["missing_marker"],
                )

    def test_prompt_and_untrusted_source_are_separate(self) -> None:
        runtime, client = self.runtime(response=fake_response(self.expected_draft))
        runtime.run_draft_generation(
            self.source_analysis,
            self.selected_title_candidate_id,
        )
        request = client.responses.calls[0]
        self.assertEqual(DRAFT_PROMPT_PATH.read_text(encoding="utf-8"), request["instructions"])
        self.assertIn("Temperature-dependent drift", request["input"])
        self.assertNotIn("Temperature-dependent drift", request["instructions"])

    def test_sdk_client_uses_draft_timeout_and_retry_policy(self) -> None:
        configured = Settings(
            storage_root=Path(self.temporary_directory.name),
            openai_api_key="synthetic-key-for-construction-only",
        )
        client = FakeClient(response=fake_response(self.expected_draft))
        with patch("backend.app.services.draft_runtime.OpenAI", return_value=client) as constructor:
            OpenAIDraftRuntime(configured).run_draft_generation(
                self.source_analysis,
                self.selected_title_candidate_id,
            )
        constructor.assert_called_once_with(
            api_key="synthetic-key-for-construction-only",
            timeout=240.0,
            max_retries=2,
        )
        self.assertEqual(1, len(client.responses.calls))

    def test_timeout_and_connection_errors_are_mapped(self) -> None:
        request = httpx2.Request("POST", "https://api.openai.com/v1/responses")
        cases = (
            (openai.APITimeoutError(request=request), "provider_timeout"),
            (openai.APIConnectionError(request=request), "provider_connection"),
        )
        for provider_error, code in cases:
            with self.subTest(code=code):
                runtime, client = self.runtime(error=provider_error)
                self.assert_runtime_error(runtime, code)
                self.assertEqual(1, len(client.responses.calls))

    def test_rate_limit_rejection_and_generic_errors_are_mapped(self) -> None:
        request = httpx2.Request("POST", "https://api.openai.com/v1/responses")
        cases = (
            (
                openai.RateLimitError(
                    "synthetic rate limit",
                    response=httpx2.Response(429, request=request),
                    body=None,
                ),
                "provider_rate_limited",
            ),
            (
                openai.BadRequestError(
                    "synthetic rejection",
                    response=httpx2.Response(400, request=request),
                    body=None,
                ),
                "provider_request_rejected",
            ),
            (
                openai.InternalServerError(
                    "synthetic provider failure",
                    response=httpx2.Response(500, request=request),
                    body=None,
                ),
                "provider_error",
            ),
        )
        for provider_error, code in cases:
            with self.subTest(code=code):
                runtime, client = self.runtime(error=provider_error)
                self.assert_runtime_error(runtime, code)
                self.assertEqual(1, len(client.responses.calls))

    def test_refusal_incomplete_and_failed_statuses_fail_closed(self) -> None:
        cases = (
            (fake_response(refusal=True, output_text="{}"), "model_refusal"),
            (fake_response(status="incomplete", output_text="{}"), "model_incomplete"),
            (fake_response(status="failed", output_text="{}"), "provider_error"),
        )
        for response, code in cases:
            with self.subTest(code=code):
                runtime, client = self.runtime(response=response)
                self.assert_runtime_error(runtime, code)
                self.assertEqual(1, len(client.responses.calls))

    def test_unparseable_outputs_fail_without_repair_call(self) -> None:
        for output_text in ("not-json", "[]", ""):
            with self.subTest(output_text=output_text):
                runtime, client = self.runtime(response=fake_response(output_text=output_text))
                self.assert_runtime_error(runtime, "response_parse_failed")
                self.assertEqual(1, len(client.responses.calls))

    def test_source_and_draft_limits_remain_independent(self) -> None:
        self.assertEqual(180, self.settings.openai_timeout_seconds)
        self.assertEqual(48_000, self.settings.openai_max_output_tokens)
        self.assertEqual(240, self.settings.openai_draft_timeout_seconds)
        self.assertEqual(64_000, self.settings.openai_draft_max_output_tokens)
        self.assertEqual(2, self.settings.openai_draft_max_retries)

    def test_caller_source_is_not_mutated(self) -> None:
        before = copy.deepcopy(self.source_analysis)
        runtime, _ = self.runtime(response=fake_response(self.expected_draft))
        runtime.run_draft_generation(
            self.source_analysis,
            self.selected_title_candidate_id,
        )
        self.assertEqual(before, self.source_analysis)

    def test_provider_valid_but_canonical_invalid_draft_is_rejected(self) -> None:
        invalid = copy.deepcopy(self.expected_draft)
        invalid["schema_version"] = "2.0.0"
        runtime, client = self.runtime(response=fake_response(invalid))
        error = self.assert_runtime_error(
            runtime,
            "draft_canonical_validation_failed",
            selected_title_candidate_id=self.selected_title_candidate_id,
        )
        self.assertIn("/schema_version", error.paths)
        self.assertEqual(1, len(client.responses.calls))

    def test_canonical_valid_but_business_invalid_draft_is_rejected(self) -> None:
        invalid = copy.deepcopy(self.expected_draft)
        invalid["document_metadata"]["source_document"]["file_name"] = "different.pdf"
        runtime, client = self.runtime(response=fake_response(invalid))
        error = self.assert_runtime_error(
            runtime,
            "draft_business_validation_failed",
            selected_title_candidate_id=self.selected_title_candidate_id,
        )
        self.assertIn("/document_metadata", error.paths)
        self.assertEqual(1, len(client.responses.calls))

    def test_provider_null_for_optional_property_is_normalized_before_validation(self) -> None:
        provider_output = copy.deepcopy(self.expected_draft)
        provider_output["selected_title"]["marker"] = None
        runtime, client = self.runtime(response=fake_response(provider_output))
        result = runtime.run_draft_generation(
            self.source_analysis,
            self.selected_title_candidate_id,
        )
        self.assertNotIn("marker", result.draft["selected_title"])
        self.assertEqual(1, len(client.responses.calls))

    def test_absent_and_invalid_title_selection_preserve_missing_title_policy(self) -> None:
        fixture = self.missing_information_fixture
        source_analysis = fixture["input"]["source_analysis"]
        expected_draft = fixture["expected_output"]
        for selected_title_candidate_id in (None, "unknown-title"):
            with self.subTest(selected_title_candidate_id=selected_title_candidate_id):
                runtime, client = self.runtime(response=fake_response(expected_draft))
                result = runtime.run_draft_generation(
                    source_analysis,
                    selected_title_candidate_id,
                )
                self.assertEqual("MISSING", result.draft["selected_title"]["status"])
                self.assertEqual(
                    "[AUTHOR CONFIRMATION REQUIRED]",
                    result.draft["selected_title"]["marker"],
                )
                linked = [
                    item
                    for item in result.draft["missing_information"]
                    if item.get("rule_id") == "TITLE_SELECTION_REQUIRED"
                ]
                self.assertEqual(1, len(linked))
                self.assertEqual(1, len(client.responses.calls))

    def test_validation_order_is_normalize_then_canonical_then_business(self) -> None:
        calls: list[str] = []

        def normalize(output, schema):
            calls.append("normalize")
            return normalize_draft_provider_output(output, schema)

        def canonical(output, schema):
            calls.append("canonical")
            return validate_canonical_draft(output, schema)

        def business(draft, source_analysis, *, selected_title_candidate_id):
            calls.append("business")
            return validate_draft_business_rules(
                draft,
                source_analysis,
                selected_title_candidate_id=selected_title_candidate_id,
            )

        runtime, _ = self.runtime(response=fake_response(self.expected_draft))
        with (
            patch(
                "backend.app.services.draft_runtime.normalize_draft_provider_output",
                side_effect=normalize,
            ),
            patch(
                "backend.app.services.draft_runtime.validate_canonical_draft",
                side_effect=canonical,
            ),
            patch(
                "backend.app.services.draft_runtime.validate_draft_business_rules",
                side_effect=business,
            ),
        ):
            runtime.run_draft_generation(
                self.source_analysis,
                self.selected_title_candidate_id,
            )
        self.assertEqual(["normalize", "canonical", "business"], calls)

    def test_success_returns_validated_draft_and_safe_metadata(self) -> None:
        runtime, client = self.runtime(response=fake_response(self.expected_draft))
        result = runtime.run_draft_generation(
            self.source_analysis,
            self.selected_title_candidate_id,
        )
        self.assertEqual(self.expected_draft, result.draft)
        self.assertEqual("openai", result.runtime.provider)
        self.assertEqual("gpt-5.6-sol", result.runtime.model)
        self.assertEqual("resp_synthetic_001", result.runtime.request_id)
        self.assertEqual("completed", result.runtime.status)
        self.assertGreaterEqual(result.runtime.duration_ms, 0)
        self.assertEqual(
            {"input_tokens": 101, "output_tokens": 202, "total_tokens": 303},
            result.runtime.usage,
        )
        self.assertEqual(1, len(client.responses.calls))

    def test_logs_contain_only_safe_operational_metadata(self) -> None:
        configured = Settings(
            storage_root=Path(self.temporary_directory.name),
            openai_api_key="synthetic-secret-that-must-not-be-logged",
        )
        client = FakeClient(response=fake_response(self.expected_draft))
        runtime = OpenAIDraftRuntime(configured, client=client)
        with self.assertLogs("backend.app.services.draft_runtime", level="INFO") as captured:
            runtime.run_draft_generation(
                self.source_analysis,
                self.selected_title_candidate_id,
            )
        logs = "\n".join(captured.output)
        self.assertIn("doc-draft-representative", logs)
        self.assertIn("resp_synthetic_001", logs)
        self.assertIn("gpt-5.6-sol", logs)
        self.assertNotIn("Temperature-dependent drift", logs)
        self.assertNotIn("synthetic-secret-that-must-not-be-logged", logs)
        self.assertNotIn(str(DRAFT_PROMPT_PATH), logs)
        self.assertNotIn(json.dumps(self.expected_draft), logs)

    def test_canonical_schema_is_not_modified_by_runtime(self) -> None:
        before = DRAFT_SCHEMA_PATH.read_bytes()
        runtime, _ = self.runtime(response=fake_response(self.expected_draft))
        runtime.run_draft_generation(
            self.source_analysis,
            self.selected_title_candidate_id,
        )
        self.assertEqual(before, DRAFT_SCHEMA_PATH.read_bytes())


if __name__ == "__main__":
    unittest.main()
