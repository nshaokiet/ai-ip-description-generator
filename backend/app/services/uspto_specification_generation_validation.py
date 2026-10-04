"""Reconstruction-only integrity gate and deterministic P2-003 validation.

The caller must supply an upstream-validated reconstruction. This gate checks
internal integrity, not the original APP-002/AI-001 projection or scientific
entailment. Neither upstream payload is a service input.
"""
from __future__ import annotations

import json
import math
import re
import unicodedata
from copy import deepcopy
from functools import lru_cache
from typing import Any

from jsonschema import Draft202012Validator

from backend.app.services.invention_reconstruction_validation import (
    REPOSITORY_ROOT, InventionReconstructionValidationError,
    _collect_identifiers, _validate_references, _validate_step_dependencies,
    _resolve_pointer, _walk, validate_reconstruction_schema,
)

ELIGIBLE = ("SOURCE_FACT", "PARAPHRASE", "INFERENCE", "SAFE_GENERALIZATION")
SCHEMA_PATH = REPOSITORY_ROOT / "schemas/uspto-specification/v2.0.0/uspto-specification.schema.json"


class USPTOGenerationValidationError(ValueError):
    """Fixed diagnostic messages; never include rejected source/config text."""

    def __init__(self, code: str, *, paths: tuple[str, ...] = ()) -> None:
        self.code = code
        self.safe_message = "The offline specification request failed validation."
        # Paths are generated from known contract fields, not arbitrary keys.
        self.paths = tuple(sorted(set(paths)))
        super().__init__(self.safe_message)


@lru_cache(maxsize=1)
def output_schema() -> dict[str, Any]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema


def word_count(text: str) -> int:
    """Exactly the released P2-001 counting behavior (no normalization)."""
    return len(re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE))


def normalize(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def prohibited_text(text: str) -> bool:
    """Defense in depth, not a complete NLP/legal classifier."""
    value = normalize(text)
    phrases = (
        "ignore previous instructions", "generate claims", "what is claimed is",
        "independent claim", "dependent claim", "human_confirmed", "human_resolved",
        "is patentable", "patentability", "non-obvious", "nonobvious",
        "inventive step", "novel over", "novelty", "infring", "enforceability",
        "freedom to operate", "likelihood of allowance", "claim scope",
        "inventorship", "filing-ready", "filing ready", "subject-matter eligibility",
        "patent validity", "patent no.", "application no.", "publication no.",
        "examiner", "art unit", "assignee", "inventor:", "filing date",
        "priority date", "publication date", "issue date", "classification code",
        "patent number", "application number", "publication number", "is novel",
        "guarantee", "is valid", "is eligible", "allowance probability",
    )
    return any(x in value for x in phrases) or bool(re.search(
        r"\((?:10|21|22|43|45|54|57|71|72|73|74)\)|\b(?:us|wo|ep)\s*\d[\d, /.-]*(?:\s*(?:a1|b1|b2))?\b",
        value,
    ))


def validate_generation_config(config: Any, reconstruction: dict[str, Any] | None = None) -> dict[str, Any]:
    if config is None or (type(config) is dict and "source_document_synthetic" not in config):
        raise USPTOGenerationValidationError("SOURCE_DOCUMENT_PROVENANCE_REQUIRED", paths=("/generation_config/source_document_synthetic",))
    if type(config) is not dict or type(config.get("source_document_synthetic")) is not bool:
        raise USPTOGenerationValidationError("INVALID_GENERATION_CONFIG", paths=("/generation_config",))
    if config["source_document_synthetic"] is False:
        raise USPTOGenerationValidationError("REAL_SOURCE_NOT_AUTHORIZED", paths=("/generation_config/source_document_synthetic",))
    defaults = {"language": "en", "abstract_max_words": 150, "include_claims": False, "target_jurisdiction": "US"}
    allowed = set(defaults) | {"source_document_synthetic", "selected_title_candidate_id"}
    if set(config) - allowed or any(
        key in config and (type(config[key]) is not type(value) or config[key] != value)
        for key, value in defaults.items()
    ):
        raise USPTOGenerationValidationError("INVALID_GENERATION_CONFIG", paths=("/generation_config",))
    if "selected_title_candidate_id" in config:
        selected = config["selected_title_candidate_id"]
        if type(selected) is not str or (reconstruction is not None and selected not in {
            x["title_id"] for x in reconstruction["invention_model"]["title_candidates"]
        }):
            raise USPTOGenerationValidationError("INVALID_TITLE_SELECTION", paths=("/generation_config/selected_title_candidate_id",))
    return deepcopy(defaults | config)


def validate_generation_input(reconstruction: Any) -> dict[str, Any]:
    try:
        validate_reconstruction_schema(reconstruction)
    except InventionReconstructionValidationError:
        raise USPTOGenerationValidationError("INVALID_RECONSTRUCTION", paths=("/reconstruction",)) from None
    failures: list[str] = []
    identifiers = _collect_identifiers(reconstruction, failures)
    model, review = reconstruction["invention_model"], reconstruction["review_package"]
    _validate_references(model, review, identifiers, failures)
    _validate_step_dependencies(model, failures)
    expected = {"source_evidence_contract": ("APP-002", "ExtractionInputEnvelope"),
                "structured_analysis_contract": ("AI-001", "STRUCTURED_INVENTION_ANALYSIS")}
    for key, (task, name) in expected.items():
        ref = reconstruction["provenance"][key]
        if ref["task_id"] != task or ref["contract_name"] != name:
            failures.append("/provenance/" + key)
    evidence = {x["evidence_id"]: x for x in review["evidence"]}
    if len(evidence) != len(review["evidence"]):
        failures.append("/review_package/evidence")
    for index, item in enumerate(review["evidence"]):
        if item["document_id"] != reconstruction["document_metadata"]["document_id"] or not re.fullmatch(r"EV-[A-Z0-9_-]+", item["evidence_id"]):
            failures.append(f"/review_package/evidence/{index}")
    for path, obj in _walk(reconstruction):
        if not isinstance(obj, dict):
            if isinstance(obj, float) and not math.isfinite(obj):
                failures.append(path)
            continue
        if obj.get("grounding_class") == "HUMAN_CONFIRMED" or obj.get("status") in {"HUMAN_CONFIRMED", "HUMAN_RESOLVED"}:
            failures.append(path)
        if "evidence_ids" in obj and any(x not in evidence for x in obj["evidence_ids"]):
            failures.append(path)
        if obj.get("grounding_class") == "SAFE_GENERALIZATION":
            metadata = obj["generalization"]
            cited = [normalize(evidence[x]["excerpt"]) for x in obj["evidence_ids"] if x in evidence]
            terms = [metadata["generalized_term"], *metadata["member_terms"]]
            if metadata["evidence_ids"] != obj["evidence_ids"] or any(
                not any(re.search(rf"(?<!\w){re.escape(normalize(term))}(?!\w)", excerpt) for excerpt in cited)
                for term in terms
            ):
                failures.append(path)
    for index, item in enumerate(model["parameters"]):
        value = item["value"]
        if value["value_kind"] == "RANGE":
            cited = [evidence[x]["excerpt"] for x in item["support"]["evidence_ids"] if x in evidence]
            def tokens(number: int | float) -> str:
                values = [str(number)]
                if isinstance(number, float) and number.is_integer():
                    values.append(str(int(number)))
                return "(?:" + "|".join(re.escape(x) for x in values) + ")"
            # Refuse coincidental numbers elsewhere in an excerpt or across units.
            # A literal supported pair is an integrity guard, not scientific NLP.
            pair = rf"(?<![\d.]){tokens(value['minimum'])}\s*(?:to|[-–—])\s*{tokens(value['maximum'])}(?![\d.])"
            if value["minimum"] > value["maximum"] or not any(re.search(pair, text) for text in cited):
                failures.append(f"/invention_model/parameters/{index}/value")
    sequences = [x["sequence_index"] for x in model["method_steps"]]
    for index, effect in enumerate(model["technical_effects"]):
        grounding = effect["support"]["grounding_class"]
        if grounding in ELIGIBLE and (
            (effect["effect_basis"] == "SUPPORTED_CONSEQUENCE" and grounding != "INFERENCE")
            or (effect["effect_basis"] == "SOURCE_REPORTED" and grounding == "INFERENCE")
        ):
            failures.append(f"/invention_model/technical_effects/{index}/support")
    if len(sequences) != len(set(sequences)):
        failures.append("/invention_model/method_steps")
    if failures:
        raise USPTOGenerationValidationError("INVALID_RECONSTRUCTION_INTEGRITY", paths=tuple(failures[:20]))
    return deepcopy(reconstruction)


def validate_generated_specification(output: Any, reconstruction: Any, generation_config: Any) -> None:
    """Validate target schema, pointer/evidence closure and exact template projection.

    Reprojection enforces non-broadening and rejects all output tampering,
    including identities, gates, provenance and internal review metadata.
    """
    source = validate_generation_input(reconstruction)
    config = validate_generation_config(generation_config, source)
    errors = list(Draft202012Validator(output_schema()).iter_errors(output))
    if errors:
        raise USPTOGenerationValidationError("INVALID_SPECIFICATION_SCHEMA", paths=("/output",))
    evidence_ids = {x["evidence_id"] for x in output["review_package"]["evidence"]}
    for section in output["sections"]:
        for area in [section, *section["subsections"]]:
            if any(prohibited_text(x["text"]) for x in area["paragraphs"]):
                raise USPTOGenerationValidationError("PROHIBITED_FILING_CONTENT", paths=("/output",))
        if any(prohibited_text(x["title"]) or prohibited_text(x["description"]) for x in section["figures"]):
            raise USPTOGenerationValidationError("PROHIBITED_FILING_CONTENT", paths=("/output",))
    if prohibited_text(output["abstract"]["text"]):
        raise USPTOGenerationValidationError("PROHIBITED_FILING_CONTENT", paths=("/output/abstract",))
    for _, obj in _walk(output):
        if not isinstance(obj, dict):
            continue
        if "source_paths" in obj:
            for pointer in obj["source_paths"]:
                try:
                    _resolve_pointer(source, pointer)
                except (KeyError, IndexError, TypeError, ValueError):
                    raise USPTOGenerationValidationError("INVALID_SOURCE_PATH", paths=("/output",)) from None
        if "support" in obj and any(x not in evidence_ids for x in obj["support"]["evidence_ids"]):
            raise USPTOGenerationValidationError("UNKNOWN_EVIDENCE_ID", paths=("/output",))
    from backend.app.services.uspto_specification_generation import _build_specification
    if output != _build_specification(source, config):
        raise USPTOGenerationValidationError("SPECIFICATION_MAPPING_MISMATCH", paths=("/output",))
