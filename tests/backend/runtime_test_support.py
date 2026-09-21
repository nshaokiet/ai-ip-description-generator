"""Synthetic-only helpers for AI-RUNTIME-001 offline tests."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from backend.app.schemas.analysis_input import ExtractionInputEnvelope


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
MINIMAL_FIXTURE = (
    REPOSITORY_ROOT / "tests/fixtures/invention-output/v1.0.0/valid/minimal.json"
)
CANONICAL_SCHEMA = (
    REPOSITORY_ROOT / "schemas/invention-output/v1.0.0/invention-output.schema.json"
)


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as source:
        return json.load(source)


def synthetic_envelope() -> ExtractionInputEnvelope:
    return ExtractionInputEnvelope.model_validate(
        {
            "document_metadata": {
                "document_id": "doc-runtime-001",
                "file_name": "synthetic-runtime.pdf",
                "media_type": "application/pdf",
                "sha256": "b" * 64,
            },
            "source_units": [
                {
                    "evidence_id": "EV-P0001-C001",
                    "evidence_type": "TEXT",
                    "locator": {"page": 1, "chunk_id": "P0001-C001"},
                    "content": "Synthetic optical sensor source evidence for deterministic testing.",
                }
            ],
        }
    )


def minimal_analysis(*, with_evidence: bool = False) -> dict[str, Any]:
    envelope = synthetic_envelope()
    analysis = copy.deepcopy(load_json(MINIMAL_FIXTURE))
    analysis["document_metadata"] = envelope.document_metadata.model_dump(exclude_none=True)
    if with_evidence:
        analysis["technical_problems"] = [
            {
                "problem_id": "problem-001",
                "statement": "A synthetic sensor requires deterministic testing.",
                "grounding": {
                    "label": "PARAPHRASE",
                    "evidence_ids": ["EV-P0001-C001"],
                },
            }
        ]
        analysis["evidence"] = [
            {
                "evidence_id": "EV-P0001-C001",
                "document_id": envelope.document_metadata.document_id,
                "evidence_type": "TEXT",
                "locator": {"page": 1, "chunk_id": "P0001-C001"},
                "excerpt": "Synthetic optical sensor source evidence",
            }
        ]
    return analysis


class FakeResponses:
    def __init__(self, response: Any = None, error: Exception | None = None) -> None:
        self.response = response
        self.error = error
        self.calls: list[dict[str, Any]] = []

    def create(self, **kwargs: Any) -> Any:
        self.calls.append(kwargs)
        if self.error is not None:
            raise self.error
        return self.response


class FakeClient:
    def __init__(self, response: Any = None, error: Exception | None = None) -> None:
        self.responses = FakeResponses(response, error)


def fake_response(
    analysis: dict[str, Any] | None = None,
    *,
    status: str = "completed",
    output_text: str | None = None,
    refusal: bool = False,
) -> SimpleNamespace:
    content = [SimpleNamespace(type="refusal", refusal="Declined")] if refusal else []
    return SimpleNamespace(
        id="resp_synthetic_001",
        status=status,
        output=[SimpleNamespace(type="message", content=content)],
        output_text=(json.dumps(analysis) if output_text is None and analysis is not None else output_text),
        usage={"input_tokens": 101, "output_tokens": 202, "total_tokens": 303},
    )
