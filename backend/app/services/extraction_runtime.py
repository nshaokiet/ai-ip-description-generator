"""Internal OpenAI Responses API extraction runtime for AI-RUNTIME-001."""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import openai
from openai import OpenAI
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

from backend.app.core.config import Settings
from backend.app.schemas.analysis_input import ExtractionInputEnvelope
from backend.app.services.extraction_validation import (
    ExtractionValidationError,
    normalize_provider_output,
    validate_canonical_output,
    validate_grounding_and_business_rules,
)
from backend.app.services.provider_schema import (
    PROVIDER_SCHEMA_NAME,
    ProviderSchemaError,
    build_provider_schema,
)


LOGGER = logging.getLogger(__name__)
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
CANONICAL_SCHEMA_PATH = (
    REPOSITORY_ROOT / "schemas" / "invention-output" / "v1.0.0" / "invention-output.schema.json"
)
CANONICAL_PROMPT_PATH = (
    REPOSITORY_ROOT / "prompts" / "extraction" / "v1.0.0" / "extraction-prompt.md"
)


class ExtractionRuntimeError(RuntimeError):
    """Safe, stable runtime failure exposed to internal callers."""

    def __init__(self, code: str, message: str, *, paths: tuple[str, ...] = ()) -> None:
        super().__init__(message)
        self.code = code
        self.safe_message = message
        self.paths = paths


@dataclass(frozen=True, slots=True)
class ExtractionRuntimeMetadata:
    provider: str
    model: str
    request_id: str | None
    status: str
    duration_ms: int
    usage: dict[str, int]


@dataclass(frozen=True, slots=True)
class ExtractionRuntimeResult:
    analysis: dict[str, Any]
    runtime: ExtractionRuntimeMetadata


class OpenAIExtractionRuntime:
    """One-call, fail-closed internal extraction boundary."""

    def __init__(
        self,
        settings: Settings,
        *,
        client: Any | None = None,
        schema_path: Path = CANONICAL_SCHEMA_PATH,
        prompt_path: Path = CANONICAL_PROMPT_PATH,
    ) -> None:
        self.settings = settings
        self._client = client
        self.schema_path = schema_path
        self.prompt_path = prompt_path

    def run_extraction(
        self,
        envelope: ExtractionInputEnvelope,
        *,
        correlation_id: str | None = None,
    ) -> ExtractionRuntimeResult:
        canonical_schema = self._load_canonical_schema()
        try:
            provider_schema = build_provider_schema(canonical_schema)
        except ProviderSchemaError as exc:
            self._log_failure("provider_schema_failed", envelope, correlation_id)
            raise ExtractionRuntimeError(
                "provider_schema_failed",
                "The provider schema could not be generated safely.",
            ) from exc

        prompt = self._load_canonical_prompt()
        client = self._get_client()
        serialized_input = json.dumps(
            envelope.model_dump(exclude_none=True, mode="json"),
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        request = {
            "model": self.settings.openai_model,
            "instructions": prompt,
            "input": serialized_input,
            "reasoning": {"effort": self.settings.openai_reasoning_effort},
            "store": False,
            "stream": False,
            "background": False,
            "max_output_tokens": self.settings.openai_max_output_tokens,
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": PROVIDER_SCHEMA_NAME,
                    "strict": True,
                    "schema": provider_schema,
                }
            },
        }

        started = time.monotonic()
        try:
            response = client.responses.create(**request)
        except openai.APITimeoutError as exc:
            self._raise_provider_error("provider_timeout", envelope, correlation_id, exc)
        except openai.APIConnectionError as exc:
            self._raise_provider_error("provider_connection_error", envelope, correlation_id, exc)
        except openai.RateLimitError as exc:
            self._raise_provider_error("provider_rate_limited", envelope, correlation_id, exc)
        except openai.APIStatusError as exc:
            code = "provider_request_rejected" if 400 <= exc.status_code < 500 else "provider_error"
            self._raise_provider_error(code, envelope, correlation_id, exc)
        except openai.OpenAIError as exc:
            self._raise_provider_error("provider_error", envelope, correlation_id, exc)
        except Exception as exc:
            self._raise_provider_error("provider_error", envelope, correlation_id, exc)

        duration_ms = round((time.monotonic() - started) * 1000)
        status = str(_field(response, "status") or "")
        request_id = _optional_string(_field(response, "id"))
        if _contains_refusal(response):
            self._log_failure("model_refusal", envelope, correlation_id, request_id=request_id)
            raise ExtractionRuntimeError("model_refusal", "The model declined the extraction request.")
        if status == "incomplete":
            self._log_failure("model_incomplete", envelope, correlation_id, request_id=request_id)
            raise ExtractionRuntimeError("model_incomplete", "The model response was incomplete.")
        if status != "completed":
            self._log_failure("provider_error", envelope, correlation_id, request_id=request_id)
            raise ExtractionRuntimeError("provider_error", "The provider did not complete the request.")

        output_text = _field(response, "output_text")
        if not isinstance(output_text, str) or not output_text.strip():
            self._log_failure("response_parse_failed", envelope, correlation_id, request_id=request_id)
            raise ExtractionRuntimeError(
                "response_parse_failed",
                "The completed provider response contained no parseable structured output.",
            )
        try:
            provider_output = json.loads(output_text)
        except (json.JSONDecodeError, TypeError) as exc:
            self._log_failure("response_parse_failed", envelope, correlation_id, request_id=request_id)
            raise ExtractionRuntimeError(
                "response_parse_failed",
                "The completed provider response contained no parseable structured output.",
            ) from exc
        if not isinstance(provider_output, dict):
            self._log_failure("response_parse_failed", envelope, correlation_id, request_id=request_id)
            raise ExtractionRuntimeError(
                "response_parse_failed",
                "The completed provider response contained no parseable structured output.",
            )

        normalized = normalize_provider_output(provider_output, canonical_schema)
        try:
            analysis = validate_canonical_output(normalized, canonical_schema)
            validate_grounding_and_business_rules(analysis, envelope)
        except ExtractionValidationError as exc:
            self._log_failure(exc.code, envelope, correlation_id, request_id=request_id)
            raise ExtractionRuntimeError(exc.code, exc.safe_message, paths=exc.paths) from exc

        runtime_metadata = ExtractionRuntimeMetadata(
            provider="openai",
            model=self.settings.openai_model,
            request_id=request_id,
            status=status,
            duration_ms=duration_ms,
            usage=_safe_usage(_field(response, "usage")),
        )
        LOGGER.info(
            "extraction_runtime_completed correlation_id=%s document_id=%s provider_request_id=%s "
            "model=%s status=%s duration_ms=%s",
            correlation_id or "none",
            envelope.document_metadata.document_id,
            request_id or "none",
            self.settings.openai_model,
            status,
            duration_ms,
        )
        return ExtractionRuntimeResult(analysis=analysis, runtime=runtime_metadata)

    def _get_client(self) -> Any:
        if self._client is not None:
            return self._client
        if not self.settings.openai_api_key:
            raise ExtractionRuntimeError(
                "runtime_not_configured",
                "The OpenAI extraction runtime is not configured.",
            )
        self._client = OpenAI(
            api_key=self.settings.openai_api_key,
            timeout=float(self.settings.openai_timeout_seconds),
            max_retries=self.settings.openai_max_retries,
        )
        return self._client

    def _load_canonical_prompt(self) -> str:
        try:
            prompt = self.prompt_path.read_text(encoding="utf-8")
        except OSError as exc:
            raise ExtractionRuntimeError(
                "runtime_not_configured",
                "The canonical extraction prompt is unavailable.",
            ) from exc
        if not prompt.strip():
            raise ExtractionRuntimeError(
                "runtime_not_configured",
                "The canonical extraction prompt is unavailable.",
            )
        return prompt

    def _load_canonical_schema(self) -> dict[str, Any]:
        try:
            with self.schema_path.open(encoding="utf-8") as source:
                schema = json.load(source)
        except (OSError, json.JSONDecodeError) as exc:
            raise ExtractionRuntimeError(
                "provider_schema_failed",
                "The canonical analysis schema is unavailable or invalid.",
            ) from exc
        if not isinstance(schema, dict):
            raise ExtractionRuntimeError(
                "provider_schema_failed",
                "The canonical analysis schema is unavailable or invalid.",
            )
        try:
            Draft202012Validator.check_schema(schema)
        except SchemaError as exc:
            raise ExtractionRuntimeError(
                "provider_schema_failed",
                "The canonical analysis schema is unavailable or invalid.",
            ) from exc
        return schema

    def _raise_provider_error(
        self,
        code: str,
        envelope: ExtractionInputEnvelope,
        correlation_id: str | None,
        cause: Exception,
    ) -> None:
        self._log_failure(code, envelope, correlation_id)
        messages = {
            "provider_timeout": "The extraction provider timed out.",
            "provider_connection_error": "The extraction provider could not be reached.",
            "provider_rate_limited": "The extraction provider rate limit was reached.",
            "provider_request_rejected": "The extraction provider rejected the request.",
            "provider_error": "The extraction provider request failed.",
        }
        raise ExtractionRuntimeError(code, messages[code]) from cause

    def _log_failure(
        self,
        code: str,
        envelope: ExtractionInputEnvelope,
        correlation_id: str | None,
        *,
        request_id: str | None = None,
    ) -> None:
        LOGGER.warning(
            "extraction_runtime_failed correlation_id=%s document_id=%s provider_request_id=%s "
            "model=%s code=%s",
            correlation_id or "none",
            envelope.document_metadata.document_id,
            request_id or "none",
            self.settings.openai_model,
            code,
        )


def run_extraction(
    envelope: ExtractionInputEnvelope,
    *,
    settings: Settings | None = None,
    client: Any | None = None,
    correlation_id: str | None = None,
) -> ExtractionRuntimeResult:
    """Convenience entrypoint for the internal extraction service."""

    runtime = OpenAIExtractionRuntime(settings or Settings.from_environment(), client=client)
    return runtime.run_extraction(envelope, correlation_id=correlation_id)


def _field(value: Any, name: str) -> Any:
    if isinstance(value, dict):
        return value.get(name)
    return getattr(value, name, None)


def _contains_refusal(response: Any) -> bool:
    for item in _field(response, "output") or []:
        for content in _field(item, "content") or []:
            if _field(content, "type") == "refusal":
                return True
    return False


def _optional_string(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None


def _safe_usage(usage: Any) -> dict[str, int]:
    if usage is None:
        return {}
    if hasattr(usage, "model_dump"):
        usage = usage.model_dump()
    if not isinstance(usage, dict):
        return {}
    safe_fields = ("input_tokens", "output_tokens", "total_tokens")
    return {
        field: value
        for field in safe_fields
        if isinstance((value := usage.get(field)), int) and not isinstance(value, bool)
    }
