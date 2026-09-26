"""Validated runtime configuration for local backend and extraction services."""

from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass, field
from pathlib import Path


MEBIBYTE = 1024 * 1024
OPENAI_EXTRACTION_MODEL = "gpt-5.6-sol"
OPENAI_REASONING_EFFORT = "high"
OPENAI_MAX_RETRIES = 2
OPENAI_DEFAULT_TIMEOUT_SECONDS = 180
OPENAI_DEFAULT_MAX_OUTPUT_TOKENS = 48_000
OPENAI_DRAFT_MODEL = "gpt-5.6-sol"
OPENAI_DRAFT_REASONING_EFFORT = "high"
OPENAI_DRAFT_MAX_RETRIES = 2
OPENAI_DRAFT_TIMEOUT_SECONDS = 240
OPENAI_DRAFT_MAX_OUTPUT_TOKENS = 64_000


def _environment_integer(name: str, default: int, *, minimum: int, maximum: int) -> int:
    raw_value = os.environ.get(name)
    if raw_value is None:
        return default
    try:
        value = int(raw_value)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if not minimum <= value <= maximum:
        raise ValueError(f"{name} must be between {minimum} and {maximum}")
    return value


def _environment_flag(name: str, default: bool = False) -> bool:
    raw_value = os.environ.get(name)
    if raw_value is None:
        return default
    if raw_value not in {"0", "1"}:
        raise ValueError(f"{name} must be 0 or 1")
    return raw_value == "1"


@dataclass(frozen=True, slots=True)
class Settings:
    """Small, explicit configuration surface with fixed extraction policy."""

    storage_root: Path
    local_export_root: Path = field(
        default_factory=lambda: Path(tempfile.gettempdir()) / "ai-ip-generator" / "exports"
    )
    enable_local_orchestration_api: bool = False
    max_upload_bytes: int = 10 * MEBIBYTE
    max_pdf_pages: int = 50
    upload_ttl_seconds: int = 60 * 60
    read_chunk_bytes: int = 64 * 1024
    max_docx_entries: int = 2_048
    max_docx_uncompressed_bytes: int = 100 * MEBIBYTE
    max_docx_entry_bytes: int = 50 * MEBIBYTE
    max_docx_compression_ratio: int = 1_000
    max_source_unit_chars: int = 4_000
    openai_api_key: str | None = None
    openai_timeout_seconds: int = OPENAI_DEFAULT_TIMEOUT_SECONDS
    openai_max_output_tokens: int = OPENAI_DEFAULT_MAX_OUTPUT_TOKENS
    run_openai_live_tests: bool = False
    openai_draft_timeout_seconds: int = OPENAI_DRAFT_TIMEOUT_SECONDS
    openai_draft_max_output_tokens: int = OPENAI_DRAFT_MAX_OUTPUT_TOKENS
    run_openai_draft_live_tests: bool = False
    openai_model: str = field(default=OPENAI_EXTRACTION_MODEL, init=False)
    openai_reasoning_effort: str = field(default=OPENAI_REASONING_EFFORT, init=False)
    openai_max_retries: int = field(default=OPENAI_MAX_RETRIES, init=False)
    openai_draft_model: str = field(default=OPENAI_DRAFT_MODEL, init=False)
    openai_draft_reasoning_effort: str = field(
        default=OPENAI_DRAFT_REASONING_EFFORT,
        init=False,
    )
    openai_draft_max_retries: int = field(default=OPENAI_DRAFT_MAX_RETRIES, init=False)

    def __post_init__(self) -> None:
        if not 30 <= self.openai_timeout_seconds <= 300:
            raise ValueError("openai_timeout_seconds must be between 30 and 300")
        if not 1 <= self.openai_max_output_tokens <= OPENAI_DEFAULT_MAX_OUTPUT_TOKENS:
            raise ValueError(
                "openai_max_output_tokens must be between 1 and the approved 48000-token limit"
            )
        if not 30 <= self.openai_draft_timeout_seconds <= 600:
            raise ValueError("openai_draft_timeout_seconds must be between 30 and 600")
        if not 1 <= self.openai_draft_max_output_tokens <= OPENAI_DRAFT_MAX_OUTPUT_TOKENS:
            raise ValueError(
                "openai_draft_max_output_tokens must be between 1 and the approved 64000-token limit"
            )

    @classmethod
    def from_environment(cls) -> "Settings":
        configured_root = os.environ.get("AI_IP_UPLOAD_ROOT")
        root = (
            Path(configured_root)
            if configured_root
            else Path(tempfile.gettempdir()) / "ai-ip-generator" / "uploads"
        )
        configured_api_key = os.environ.get("OPENAI_API_KEY")
        api_key = configured_api_key if configured_api_key and configured_api_key.strip() else None
        return cls(
            storage_root=root,
            enable_local_orchestration_api=_environment_flag(
                "AI_IP_ENABLE_LOCAL_ORCHESTRATION_API"
            ),
            openai_api_key=api_key,
            openai_timeout_seconds=_environment_integer(
                "OPENAI_TIMEOUT_SECONDS",
                OPENAI_DEFAULT_TIMEOUT_SECONDS,
                minimum=30,
                maximum=300,
            ),
            openai_max_output_tokens=_environment_integer(
                "OPENAI_MAX_OUTPUT_TOKENS",
                OPENAI_DEFAULT_MAX_OUTPUT_TOKENS,
                minimum=1,
                maximum=OPENAI_DEFAULT_MAX_OUTPUT_TOKENS,
            ),
            run_openai_live_tests=_environment_flag("RUN_OPENAI_LIVE_TESTS"),
            openai_draft_timeout_seconds=_environment_integer(
                "OPENAI_DRAFT_TIMEOUT_SECONDS",
                OPENAI_DRAFT_TIMEOUT_SECONDS,
                minimum=30,
                maximum=600,
            ),
            openai_draft_max_output_tokens=_environment_integer(
                "OPENAI_DRAFT_MAX_OUTPUT_TOKENS",
                OPENAI_DRAFT_MAX_OUTPUT_TOKENS,
                minimum=1,
                maximum=OPENAI_DRAFT_MAX_OUTPUT_TOKENS,
            ),
            run_openai_draft_live_tests=_environment_flag("RUN_OPENAI_DRAFT_LIVE_TESTS"),
        )
