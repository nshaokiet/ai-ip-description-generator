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
    DRAFT_PROMPT_PATH,
    DraftRuntimeError,
    OpenAIDraftRuntime,
)
from tests.backend.runtime_test_support import FakeClient, fake_response, load_json


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
REPRESENTATIVE_FIXTURE = (
    REPOSITORY_ROOT / "tests" / "fixtures" / "patent-draft" / "v1.0.0"
    / "cases" / "representative.json"
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
                runtime, client = self.runtime(response=fake_response(self.expected_draft))
                runtime.run_draft_generation(
                    self.source_analysis,
                    selected_title_candidate_id,
                )
                envelope = json.loads(client.responses.calls[0]["input"])
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
        runtime.run_draft_generation(self.source_analysis)
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
            OpenAIDraftRuntime(configured).run_draft_generation(self.source_analysis)
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
        runtime.run_draft_generation(self.source_analysis, "unknown-title")
        self.assertEqual(before, self.source_analysis)


if __name__ == "__main__":
    unittest.main()
