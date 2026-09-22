"""Internal OpenAI Responses API runtime for AI-RUNTIME-002 Draft generation."""

from __future__ import annotations

import copy
import json
import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

import openai
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError
from openai import OpenAI

from backend.app.core.config import Settings
from backend.app.services.draft_business_validation import (
    DraftBusinessValidationError,
    validate_draft_business_rules,
    validate_draft_source_analysis,
)
from backend.app.services.draft_provider_schema import (
    PATENT_DRAFT_PROVIDER_SCHEMA_NAME,
    DraftProviderSchemaError,
    build_draft_provider_schema,
)
from backend.app.services.draft_validation import (
    DraftValidationError,
    normalize_draft_provider_output,
    validate_canonical_draft,
)


LOGGER = logging.getLogger(__name__)
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
SOURCE_SCHEMA_PATH = (
    REPOSITORY_ROOT / "schemas" / "invention-output" / "v1.0.0" / "invention-output.schema.json"
)
DRAFT_SCHEMA_PATH = (
    REPOSITORY_ROOT / "schemas" / "patent-draft" / "v1.0.0" / "patent-draft.schema.json"
)
DRAFT_PROMPT_PATH = (
    REPOSITORY_ROOT / "prompts" / "draft-generation" / "v1.0.0" / "draft-generation-prompt.md"
)

INPUT_CONTRACT_VERSION = "1.0.0"
DRAFT_TASK = "GENERATE_PATENT_DESCRIPTION_DRAFT"
MISSING_MARKER = "[AUTHOR CONFIRMATION REQUIRED]"
ABSTRACT_MAX_WORDS = 150


class DraftRuntimeError(RuntimeError):
    """Safe, stable runtime failure exposed to internal callers."""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        paths: tuple[str, ...] = (),
    ) -> None:
        super().__init__(message)
        self.code = code
        self.safe_message = message
        self.paths = paths


@dataclass(frozen=True, slots=True)
class DraftRuntimeMetadata:
    provider: str
    model: str
    request_id: str | None
    status: str
    duration_ms: int
    usage: dict[str, int]


@dataclass(frozen=True, slots=True)
class DraftRuntimeResult:
    draft: dict[str, Any]
    runtime: DraftRuntimeMetadata


def build_draft_input_envelope(
    source_analysis: Mapping[str, Any],
    selected_title_candidate_id: str | None,
) -> dict[str, Any]:
    """Build the fixed AI-003 input envelope without mutating caller data."""
    generation_config: dict[str, Any] = {
        "language": "en",
        "abstract_max_words": ABSTRACT_MAX_WORDS,
        "missing_marker": MISSING_MARKER,
        "include_claims": False,
        "include_legal_advice": False,
        "include_patentability_assessment": False,
    }
    candidate_ids = {
        candidate.get("title_id")
        for candidate in source_analysis.get("title_candidates", [])
        if isinstance(candidate, Mapping)
    }
    if selected_title_candidate_id is not None and selected_title_candidate_id in candidate_ids:
        generation_config["selected_title_candidate_id"] = selected_title_candidate_id

    return {
        "input_contract_version": INPUT_CONTRACT_VERSION,
        "task": DRAFT_TASK,
        "source_analysis": copy.deepcopy(dict(source_analysis)),
        "generation_config": generation_config,
    }


class OpenAIDraftRuntime:
    """One-call, stateless Draft provider boundary."""

    def __init__(
        self,
        settings: Settings,
        *,
        client: Any | None = None,
        source_schema_path: Path = SOURCE_SCHEMA_PATH,
        draft_schema_path: Path = DRAFT_SCHEMA_PATH,
        prompt_path: Path = DRAFT_PROMPT_PATH,
    ) -> None:
        self.settings = settings
        self._client = client
        self.source_schema_path = source_schema_path
        self.draft_schema_path = draft_schema_path
        self.prompt_path = prompt_path

    def run_draft_generation(
        self,
        source_analysis: dict[str, Any],
        selected_title_candidate_id: str | None = None,
    ) -> DraftRuntimeResult:
        source_schema = self._load_source_schema()
        self._validate_source_analysis(source_analysis, source_schema)
        envelope = build_draft_input_envelope(source_analysis, selected_title_candidate_id)

        canonical_draft_schema = self._load_draft_schema()
        try:
            provider_schema = build_draft_provider_schema(canonical_draft_schema)
        except DraftProviderSchemaError as exc:
            self._log_failure("provider_schema_failed", source_analysis)
            raise DraftRuntimeError(
                "provider_schema_failed",
                "The Draft provider schema could not be generated safely.",
            ) from exc

        prompt = self._load_prompt()
        client = self._get_client()
        serialized_input = json.dumps(
            envelope,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        request = {
            "model": self.settings.openai_draft_model,
            "instructions": prompt,
            "input": serialized_input,
            "reasoning": {"effort": self.settings.openai_draft_reasoning_effort},
            "store": False,
            "stream": False,
            "background": False,
            "max_output_tokens": self.settings.openai_draft_max_output_tokens,
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": PATENT_DRAFT_PROVIDER_SCHEMA_NAME,
                    "strict": True,
                    "schema": provider_schema,
                }
            },
        }

        started = time.monotonic()
        try:
            response = client.responses.create(**request)
        except openai.APITimeoutError as exc:
            self._raise_provider_error("provider_timeout", source_analysis, exc)
        except openai.APIConnectionError as exc:
            self._raise_provider_error("provider_connection", source_analysis, exc)
        except openai.RateLimitError as exc:
            self._raise_provider_error("provider_rate_limited", source_analysis, exc)
        except openai.APIStatusError as exc:
            code = "provider_request_rejected" if 400 <= exc.status_code < 500 else "provider_error"
            self._raise_provider_error(code, source_analysis, exc)
        except openai.OpenAIError as exc:
            self._raise_provider_error("provider_error", source_analysis, exc)
        except Exception as exc:
            self._raise_provider_error("provider_error", source_analysis, exc)

        duration_ms = round((time.monotonic() - started) * 1000)
        status = str(_field(response, "status") or "")
        request_id = _optional_string(_field(response, "id"))
        if _contains_refusal(response):
            self._log_failure("model_refusal", source_analysis, request_id=request_id)
            raise DraftRuntimeError("model_refusal", "The model declined the Draft request.")
        if status == "incomplete":
            self._log_failure("model_incomplete", source_analysis, request_id=request_id)
            raise DraftRuntimeError("model_incomplete", "The model response was incomplete.")
        if status != "completed":
            self._log_failure("provider_error", source_analysis, request_id=request_id)
            raise DraftRuntimeError("provider_error", "The provider did not complete the Draft request.")

        output_text = _field(response, "output_text")
        if not isinstance(output_text, str) or not output_text.strip():
            self._raise_parse_error(source_analysis, request_id)
        try:
            provider_output = json.loads(output_text)
        except (json.JSONDecodeError, TypeError) as exc:
            self._raise_parse_error(source_analysis, request_id, exc)
        if not isinstance(provider_output, dict):
            self._raise_parse_error(source_analysis, request_id)

        normalized = normalize_draft_provider_output(
            provider_output,
            canonical_draft_schema,
        )
        try:
            draft = validate_canonical_draft(normalized, canonical_draft_schema)
        except DraftValidationError as exc:
            self._log_failure(exc.code, source_analysis, request_id=request_id)
            raise DraftRuntimeError(exc.code, exc.safe_message, paths=exc.paths) from exc
        try:
            validate_draft_business_rules(
                draft,
                source_analysis,
                selected_title_candidate_id=selected_title_candidate_id,
            )
        except DraftBusinessValidationError as exc:
            self._log_failure(exc.code, source_analysis, request_id=request_id)
            raise DraftRuntimeError(exc.code, exc.safe_message, paths=exc.paths) from exc

        runtime_metadata = DraftRuntimeMetadata(
            provider="openai",
            model=self.settings.openai_draft_model,
            request_id=request_id,
            status=status,
            duration_ms=duration_ms,
            usage=_safe_usage(_field(response, "usage")),
        )
        self._log_completion(source_analysis, runtime_metadata)
        return DraftRuntimeResult(draft=draft, runtime=runtime_metadata)

    def _load_source_schema(self) -> dict[str, Any]:
        return self._load_schema(
            self.source_schema_path,
            code="draft_runtime_not_configured",
            message="The canonical source-analysis schema is unavailable or invalid.",
        )

    def _load_draft_schema(self) -> dict[str, Any]:
        return self._load_schema(
            self.draft_schema_path,
            code="provider_schema_failed",
            message="The canonical Draft schema is unavailable or invalid.",
        )

    @staticmethod
    def _load_schema(path: Path, *, code: str, message: str) -> dict[str, Any]:
        try:
            with path.open(encoding="utf-8") as source:
                schema = json.load(source)
        except (OSError, json.JSONDecodeError) as exc:
            raise DraftRuntimeError(code, message) from exc
        if not isinstance(schema, dict):
            raise DraftRuntimeError(code, message)
        try:
            Draft202012Validator.check_schema(schema)
        except SchemaError as exc:
            raise DraftRuntimeError(code, message) from exc
        return schema

    def _validate_source_analysis(
        self,
        source_analysis: Any,
        source_schema: Mapping[str, Any],
    ) -> None:
        errors = sorted(
            Draft202012Validator(source_schema).iter_errors(source_analysis),
            key=lambda error: (list(error.absolute_path), list(error.absolute_schema_path)),
        )
        if errors:
            paths = tuple(_json_path(error.absolute_path) for error in errors[:10])
            self._log_failure("draft_input_invalid", source_analysis)
            raise DraftRuntimeError(
                "draft_input_invalid",
                "The source analysis did not satisfy the canonical input contract.",
                paths=paths,
            )
        if not isinstance(source_analysis, Mapping):
            self._log_failure("draft_input_invalid", source_analysis)
            raise DraftRuntimeError(
                "draft_input_invalid",
                "The source analysis did not satisfy the canonical input contract.",
            )
        try:
            validate_draft_source_analysis(source_analysis)
        except DraftBusinessValidationError as exc:
            self._log_failure("draft_input_invalid", source_analysis)
            raise DraftRuntimeError(
                "draft_input_invalid",
                "The source analysis failed deterministic Draft input validation.",
                paths=exc.paths,
            ) from exc

    def _load_prompt(self) -> str:
        try:
            prompt = self.prompt_path.read_text(encoding="utf-8")
        except OSError as exc:
            raise DraftRuntimeError(
                "draft_runtime_not_configured",
                "The canonical Draft prompt is unavailable.",
            ) from exc
        if not prompt.strip():
            raise DraftRuntimeError(
                "draft_runtime_not_configured",
                "The canonical Draft prompt is unavailable.",
            )
        return prompt

    def _get_client(self) -> Any:
        if self._client is not None:
            return self._client
        if not self.settings.openai_api_key:
            raise DraftRuntimeError(
                "draft_runtime_not_configured",
                "The OpenAI Draft runtime is not configured.",
            )
        self._client = OpenAI(
            api_key=self.settings.openai_api_key,
            timeout=float(self.settings.openai_draft_timeout_seconds),
            max_retries=self.settings.openai_draft_max_retries,
        )
        return self._client

    def _raise_provider_error(
        self,
        code: str,
        source_analysis: Any,
        cause: Exception,
    ) -> None:
        self._log_failure(code, source_analysis)
        messages = {
            "provider_timeout": "The Draft provider timed out.",
            "provider_connection": "The Draft provider could not be reached.",
            "provider_rate_limited": "The Draft provider rate limit was reached.",
            "provider_request_rejected": "The Draft provider rejected the request.",
            "provider_error": "The Draft provider request failed.",
        }
        raise DraftRuntimeError(code, messages[code]) from cause

    def _raise_parse_error(
        self,
        source_analysis: Any,
        request_id: str | None,
        cause: Exception | None = None,
    ) -> None:
        self._log_failure("response_parse_failed", source_analysis, request_id=request_id)
        error = DraftRuntimeError(
            "response_parse_failed",
            "The completed provider response contained no parseable structured Draft output.",
        )
        if cause is None:
            raise error
        raise error from cause

    def _log_failure(
        self,
        code: str,
        source_analysis: Any,
        *,
        request_id: str | None = None,
    ) -> None:
        LOGGER.warning(
            "draft_runtime_failed document_id=%s provider_request_id=%s model=%s code=%s",
            _safe_document_id(source_analysis),
            request_id or "none",
            self.settings.openai_draft_model,
            code,
        )

    @staticmethod
    def _log_completion(
        source_analysis: Any,
        runtime: DraftRuntimeMetadata,
    ) -> None:
        LOGGER.info(
            "draft_runtime_completed document_id=%s provider_request_id=%s model=%s "
            "status=%s duration_ms=%s input_tokens=%s output_tokens=%s total_tokens=%s",
            _safe_document_id(source_analysis),
            runtime.request_id or "none",
            runtime.model,
            runtime.status,
            runtime.duration_ms,
            runtime.usage.get("input_tokens", "none"),
            runtime.usage.get("output_tokens", "none"),
            runtime.usage.get("total_tokens", "none"),
        )


def run_draft_generation(
    source_analysis: dict[str, Any],
    selected_title_candidate_id: str | None = None,
) -> DraftRuntimeResult:
    """Run the fixed-policy Draft generation runtime."""
    runtime = OpenAIDraftRuntime(Settings.from_environment())
    return runtime.run_draft_generation(source_analysis, selected_title_candidate_id)


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


def _safe_document_id(source_analysis: Any) -> str:
    if not isinstance(source_analysis, Mapping):
        return "none"
    metadata = source_analysis.get("document_metadata")
    if not isinstance(metadata, Mapping):
        return "none"
    document_id = metadata.get("document_id")
    return document_id if isinstance(document_id, str) and document_id else "none"


def _json_path(path: Any) -> str:
    tokens = [str(token).replace("~", "~0").replace("/", "~1") for token in path]
    return "/" + "/".join(tokens) if tokens else "/"
