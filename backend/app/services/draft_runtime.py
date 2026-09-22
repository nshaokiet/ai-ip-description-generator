"""Minimal internal skeleton for Draft Generation Runtime."""

from __future__ import annotations

from typing import Any


class DraftRuntimeError(Exception):
    """Base exception for the Draft Runtime."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


# Anticipated error codes for future checkpoints
_ERROR_CODES = {
    "draft_runtime_not_configured",
    "draft_input_invalid",
    "provider_schema_failed",
    "provider_timeout",
    "provider_connection_error",
    "provider_rate_limited",
    "provider_request_rejected",
    "provider_error",
    "model_refusal",
    "model_incomplete",
    "response_parse_failed",
    "draft_canonical_validation_failed",
    "draft_business_validation_failed",
}


def run_draft_generation(
    source_analysis: dict[str, Any],
    selected_title_candidate_id: str | None = None,
) -> dict[str, Any]:
    """
    Transform a validated structured invention analysis into a grounded English
    patent-description draft.

    This function represents the future AI-RUNTIME-002 boundary.
    It does not currently invoke the provider.
    """
    # Checkpoint A: explicitly not implemented yet.
    raise NotImplementedError(
        "run_draft_generation is a skeleton for Checkpoint A and is not yet implemented"
    )
