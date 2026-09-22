"""Opt-in synthetic live check for the AI-RUNTIME-002 Draft provider boundary."""

from __future__ import annotations

import copy
import json
import os
from pathlib import Path

import pytest

from backend.app.services.draft_runtime import DraftRuntimeResult, run_draft_generation


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
MINIMAL_SOURCE_FIXTURE = (
    REPOSITORY_ROOT / "tests" / "fixtures" / "invention-output" / "v1.0.0"
    / "valid" / "minimal.json"
)
LIVE_ENABLED = (
    os.environ.get("RUN_OPENAI_DRAFT_LIVE_TESTS") == "1"
    and bool(os.environ.get("OPENAI_API_KEY", "").strip())
)


@pytest.mark.skipif(
    not LIVE_ENABLED,
    reason="requires RUN_OPENAI_DRAFT_LIVE_TESTS=1 and OPENAI_API_KEY",
)
def test_one_synthetic_live_draft_call() -> None:
    source_analysis = json.loads(MINIMAL_SOURCE_FIXTURE.read_text(encoding="utf-8"))
    source_analysis = copy.deepcopy(source_analysis)
    source_analysis["document_metadata"] = {
        "document_id": "doc-synthetic-draft-live",
        "file_name": "synthetic-draft-live.pdf",
        "media_type": "application/pdf",
        "sha256": "d" * 64,
    }

    result = run_draft_generation(source_analysis)

    assert isinstance(result, DraftRuntimeResult)
    assert result.runtime.provider == "openai"
    assert result.runtime.model == "gpt-5.6-sol"
    assert result.runtime.status == "completed"
