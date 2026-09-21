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
from backend.app.services.extraction_runtime import (
    CANONICAL_PROMPT_PATH,
    ExtractionRuntimeError,
    OpenAIExtractionRuntime,
)
from backend.app.services.provider_schema import PROVIDER_SCHEMA_NAME
from tests.backend.runtime_test_support import (
    CANONICAL_SCHEMA,
    FakeClient,
    fake_response,
    minimal_analysis,
    synthetic_envelope,
)


class OpenAIExtractionRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.settings = Settings(storage_root=Path(self.temporary_directory.name))
        self.envelope = synthetic_envelope()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def runtime(self, *, response=None, error=None, **kwargs) -> tuple[OpenAIExtractionRuntime, FakeClient]:
        client = FakeClient(response=response, error=error)
        return OpenAIExtractionRuntime(self.settings, client=client, **kwargs), client

    def assert_runtime_error(self, runtime, expected_code: str) -> None:
        with self.assertRaises(ExtractionRuntimeError) as captured:
            runtime.run_extraction(self.envelope, correlation_id="corr-synthetic")
        self.assertEqual(expected_code, captured.exception.code)
        self.assertNotIn("Synthetic optical sensor", captured.exception.safe_message)

    def test_completed_valid_json_returns_validated_analysis_and_safe_metadata(self) -> None:
        analysis = minimal_analysis(with_evidence=True)
        runtime, client = self.runtime(response=fake_response(analysis))
        result = runtime.run_extraction(self.envelope)
        self.assertEqual(analysis, result.analysis)
        self.assertEqual("openai", result.runtime.provider)
        self.assertEqual("gpt-5.6-sol", result.runtime.model)
        self.assertEqual("resp_synthetic_001", result.runtime.request_id)
        self.assertEqual(
            {"input_tokens": 101, "output_tokens": 202, "total_tokens": 303},
            result.runtime.usage,
        )
        self.assertNotIn("provider", result.analysis)
        self.assertEqual(1, len(client.responses.calls))

    def test_request_uses_approved_responses_api_semantics(self) -> None:
        runtime, client = self.runtime(response=fake_response(minimal_analysis()))
        runtime.run_extraction(self.envelope)
        request = client.responses.calls[0]
        self.assertEqual("gpt-5.6-sol", request["model"])
        self.assertEqual({"effort": "high"}, request["reasoning"])
        self.assertIs(False, request["store"])
        self.assertIs(False, request["stream"])
        self.assertIs(False, request["background"])
        self.assertEqual(48_000, request["max_output_tokens"])
        self.assertNotIn("tools", request)
        self.assertNotIn("conversation", request)
        self.assertNotIn("previous_response_id", request)
        self.assertEqual(PROVIDER_SCHEMA_NAME, request["text"]["format"]["name"])
        self.assertEqual("json_schema", request["text"]["format"]["type"])
        self.assertIs(True, request["text"]["format"]["strict"])

    def test_prompt_and_untrusted_input_are_separate(self) -> None:
        runtime, client = self.runtime(response=fake_response(minimal_analysis()))
        runtime.run_extraction(self.envelope)
        request = client.responses.calls[0]
        self.assertEqual(CANONICAL_PROMPT_PATH.read_text(encoding="utf-8"), request["instructions"])
        self.assertEqual(
            self.envelope.model_dump(exclude_none=True, mode="json"),
            json.loads(request["input"]),
        )
        self.assertIn("Synthetic optical sensor source evidence", request["input"])
        self.assertNotEqual(request["instructions"], request["input"])

    def test_sdk_client_uses_timeout_and_exact_retry_policy(self) -> None:
        configured = Settings(
            storage_root=Path(self.temporary_directory.name),
            openai_api_key="synthetic-key-for-construction-only",
        )
        client = FakeClient(response=fake_response(minimal_analysis()))
        with patch("backend.app.services.extraction_runtime.OpenAI", return_value=client) as constructor:
            OpenAIExtractionRuntime(configured).run_extraction(self.envelope)
        constructor.assert_called_once_with(
            api_key="synthetic-key-for-construction-only",
            timeout=180.0,
            max_retries=2,
        )
        self.assertEqual(1, len(client.responses.calls))

    def test_missing_api_key_without_injected_client_fails_configured_boundary(self) -> None:
        runtime = OpenAIExtractionRuntime(self.settings)
        self.assert_runtime_error(runtime, "runtime_not_configured")

    def test_missing_prompt_fails_safely_before_model_call(self) -> None:
        runtime, client = self.runtime(
            response=fake_response(minimal_analysis()),
            prompt_path=Path(self.temporary_directory.name) / "missing-prompt.md",
        )
        self.assert_runtime_error(runtime, "runtime_not_configured")
        self.assertEqual([], client.responses.calls)

    def test_provider_schema_failure_occurs_before_model_call(self) -> None:
        schema_path = Path(self.temporary_directory.name) / "unsafe-schema.json"
        schema_path.write_text(
            json.dumps(
                {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {"value": {"not": {"type": "string"}}},
                    "required": ["value"],
                }
            ),
            encoding="utf-8",
        )
        runtime, client = self.runtime(
            response=fake_response(minimal_analysis()),
            schema_path=schema_path,
        )
        self.assert_runtime_error(runtime, "provider_schema_failed")
        self.assertEqual([], client.responses.calls)

    def test_invalid_canonical_schema_fails_before_model_call(self) -> None:
        schema_path = Path(self.temporary_directory.name) / "invalid-canonical-schema.json"
        schema_path.write_text(
            json.dumps({"type": 7}),
            encoding="utf-8",
        )
        runtime, client = self.runtime(
            response=fake_response(minimal_analysis()),
            schema_path=schema_path,
        )
        self.assert_runtime_error(runtime, "provider_schema_failed")
        self.assertEqual([], client.responses.calls)

    def test_malformed_and_non_object_outputs_fail_parse(self) -> None:
        for output_text in ("not-json", "[]", ""):
            with self.subTest(output_text=output_text):
                runtime, client = self.runtime(response=fake_response(output_text=output_text))
                self.assert_runtime_error(runtime, "response_parse_failed")
                self.assertEqual(1, len(client.responses.calls))

    def test_refusal_fails_closed(self) -> None:
        runtime, _ = self.runtime(response=fake_response(refusal=True, output_text="{}"))
        self.assert_runtime_error(runtime, "model_refusal")

    def test_incomplete_response_fails_closed(self) -> None:
        runtime, _ = self.runtime(response=fake_response(status="incomplete", output_text="{}"))
        self.assert_runtime_error(runtime, "model_incomplete")

    def test_noncompleted_unexpected_status_fails_provider_error(self) -> None:
        runtime, _ = self.runtime(response=fake_response(status="failed", output_text="{}"))
        self.assert_runtime_error(runtime, "provider_error")

    def test_timeout_and_connection_errors_are_mapped(self) -> None:
        request = httpx2.Request("POST", "https://api.openai.com/v1/responses")
        cases = (
            (openai.APITimeoutError(request=request), "provider_timeout"),
            (openai.APIConnectionError(request=request), "provider_connection_error"),
        )
        for error, code in cases:
            with self.subTest(code=code):
                runtime, client = self.runtime(error=error)
                self.assert_runtime_error(runtime, code)
                self.assertEqual(1, len(client.responses.calls))

    def test_rate_limit_bad_request_and_server_errors_are_mapped(self) -> None:
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
        for error, code in cases:
            with self.subTest(code=code):
                runtime, _ = self.runtime(error=error)
                self.assert_runtime_error(runtime, code)

    def test_canonical_invalid_output_is_rejected_without_second_call(self) -> None:
        invalid = minimal_analysis()
        invalid["schema_version"] = "2.0.0"
        runtime, client = self.runtime(response=fake_response(invalid))
        self.assert_runtime_error(runtime, "canonical_validation_failed")
        self.assertEqual(1, len(client.responses.calls))

    def test_grounding_invalid_output_is_rejected_without_second_call(self) -> None:
        invalid = minimal_analysis(with_evidence=True)
        invalid["evidence"][0]["excerpt"] = "not present in source"
        runtime, client = self.runtime(response=fake_response(invalid))
        self.assert_runtime_error(runtime, "grounding_validation_failed")
        self.assertEqual(1, len(client.responses.calls))

    def test_logs_exclude_source_prompt_provider_output_and_secret(self) -> None:
        analysis = minimal_analysis(with_evidence=True)
        runtime, _ = self.runtime(response=fake_response(analysis))
        with self.assertLogs("backend.app.services.extraction_runtime", level="INFO") as captured:
            runtime.run_extraction(self.envelope, correlation_id="corr-safe")
        logs = "\n".join(captured.output)
        self.assertIn("corr-safe", logs)
        self.assertIn("doc-runtime-001", logs)
        self.assertNotIn("Synthetic optical sensor source evidence", logs)
        self.assertNotIn("Return exactly one JSON object", logs)
        self.assertNotIn(json.dumps(analysis), logs)

    def test_configuration_rejects_timeout_and_output_budget_drift(self) -> None:
        for kwargs in (
            {"openai_timeout_seconds": 29},
            {"openai_timeout_seconds": 301},
            {"openai_max_output_tokens": 48_001},
            {"openai_max_output_tokens": 0},
        ):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                Settings(storage_root=Path(self.temporary_directory.name), **kwargs)

    def test_production_model_and_reasoning_policy_cannot_be_overridden(self) -> None:
        with self.assertRaises(TypeError):
            Settings(
                storage_root=Path(self.temporary_directory.name),
                openai_model="different-model",
            )
        with self.assertRaises(TypeError):
            Settings(
                storage_root=Path(self.temporary_directory.name),
                openai_reasoning_effort="low",
            )

    def test_canonical_schema_file_is_unchanged_by_runtime(self) -> None:
        before = CANONICAL_SCHEMA.read_bytes()
        runtime, _ = self.runtime(response=fake_response(minimal_analysis()))
        runtime.run_extraction(self.envelope)
        self.assertEqual(before, CANONICAL_SCHEMA.read_bytes())


if __name__ == "__main__":
    unittest.main()
