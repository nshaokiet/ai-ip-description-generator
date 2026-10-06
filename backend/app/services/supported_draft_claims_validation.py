"""Validation for the standalone P2-004 supported draft Claims contract.

The module deliberately reuses the released P2-002/P2-003 validation surfaces.
It does not accept raw papers, provider output, or an assembled P2-001 document.
"""
from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from functools import lru_cache
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from backend.app.services.uspto_specification_generation_validation import (
    USPTOGenerationValidationError,
    output_schema as p2_003_output_schema,
    validate_generated_specification,
    validate_generation_config as validate_p2_003_generation_config,
    validate_generation_input,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
SCHEMA_PATH = REPOSITORY_ROOT / "schemas/supported-draft-claims/v1.0.0/supported-draft-claims.schema.json"

FAMILY_ORDER = ("SYSTEM", "APPARATUS", "METHOD", "PROCESS", "COMPOSITION")
STRUCTURAL_TYPES = ("SYSTEM", "APPARATUS")
GROUNDING_ELIGIBLE = ("SOURCE_FACT", "PARAPHRASE")


class SupportedDraftClaimsValidationError(ValueError):
    """Stable, source-safe P2-004 diagnostic."""

    def __init__(self, code: str, *, paths: tuple[str, ...] = ()) -> None:
        self.code = code
        self.safe_message = "The offline supported draft Claims request failed validation."
        self.paths = tuple(sorted(set(paths)))
        super().__init__(self.safe_message)


def canonical_json(value: Any) -> str:
    try:
        return json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
    except (TypeError, ValueError):
        raise SupportedDraftClaimsValidationError("INVALID_GENERATION_CONFIG", paths=("/generation_config",)) from None


def sha256_canonical(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


@lru_cache(maxsize=1)
def _cached_output_schema() -> dict[str, Any]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema


def output_schema() -> dict[str, Any]:
    """Return an isolated schema copy so callers cannot poison later validation."""
    return deepcopy(_cached_output_schema())


def _invalid_config(path: str = "/generation_config") -> None:
    raise SupportedDraftClaimsValidationError("INVALID_GENERATION_CONFIG", paths=(path,))


def validate_generation_config(config: Any, reconstruction: dict[str, Any] | None = None) -> dict[str, Any]:
    if config is None or (type(config) is dict and "source_document_synthetic" not in config):
        raise SupportedDraftClaimsValidationError(
            "SOURCE_DOCUMENT_PROVENANCE_REQUIRED",
            paths=("/generation_config/source_document_synthetic",),
        )
    if type(config) is not dict:
        _invalid_config()
    if type(config.get("source_document_synthetic")) is not bool:
        _invalid_config("/generation_config/source_document_synthetic")
    if config["source_document_synthetic"] is False:
        raise SupportedDraftClaimsValidationError(
            "REAL_SOURCE_NOT_AUTHORIZED",
            paths=("/generation_config/source_document_synthetic",),
        )

    required = {
        "language",
        "target_jurisdiction",
        "requested_claim_types",
        "max_dependent_claims_per_family",
        "source_document_synthetic",
        "selected_solution_id",
        "p2_003_generation_config",
    }
    if set(config) != required:
        _invalid_config()
    if config.get("language") != "en" or config.get("target_jurisdiction") != "US":
        _invalid_config()
    requested = config.get("requested_claim_types")
    if type(requested) is not list or not requested or any(type(x) is not str for x in requested):
        _invalid_config("/generation_config/requested_claim_types")
    unsupported = [x for x in requested if x not in FAMILY_ORDER]
    if unsupported:
        raise SupportedDraftClaimsValidationError(
            "REQUESTED_CLAIM_TYPE_UNSUPPORTED",
            paths=("/generation_config/requested_claim_types",),
        )
    if len(set(requested)) != len(requested):
        _invalid_config("/generation_config/requested_claim_types")
    cap = config.get("max_dependent_claims_per_family")
    if type(cap) is not int or not 0 <= cap <= 10:
        _invalid_config("/generation_config/max_dependent_claims_per_family")
    selected = config.get("selected_solution_id")
    if type(selected) is not str or not selected:
        _invalid_config("/generation_config/selected_solution_id")
    if reconstruction is not None and selected not in {
        x["solution_id"] for x in reconstruction["invention_model"]["solution_concepts"]
    }:
        _invalid_config("/generation_config/selected_solution_id")
    try:
        p2_config = validate_p2_003_generation_config(config.get("p2_003_generation_config"), reconstruction)
    except USPTOGenerationValidationError:
        _invalid_config("/generation_config/p2_003_generation_config")
    if p2_config["source_document_synthetic"] is not True:
        raise SupportedDraftClaimsValidationError(
            "REAL_SOURCE_NOT_AUTHORIZED",
            paths=("/generation_config/p2_003_generation_config/source_document_synthetic",),
        )

    return {
        "language": "en",
        "target_jurisdiction": "US",
        "requested_claim_types": [x for x in FAMILY_ORDER if x in requested],
        "max_dependent_claims_per_family": cap,
        "source_document_synthetic": True,
        "selected_solution_id": selected,
        "p2_003_generation_config": deepcopy(p2_config),
    }


def validate_inputs(
    reconstruction: Any,
    specification: Any,
    generation_config: Any,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    try:
        source = validate_generation_input(reconstruction)
    except USPTOGenerationValidationError:
        raise SupportedDraftClaimsValidationError("INVALID_RECONSTRUCTION", paths=("/reconstruction",)) from None

    config = validate_generation_config(generation_config, source)
    if type(specification) is not dict:
        raise SupportedDraftClaimsValidationError("INVALID_SPECIFICATION", paths=("/specification",))
    if list(Draft202012Validator(p2_003_output_schema()).iter_errors(specification)):
        raise SupportedDraftClaimsValidationError("INVALID_SPECIFICATION", paths=("/specification",))

    src = source["document_metadata"]
    spec_src = specification["document_metadata"]["source_document"]
    for key in ("document_id", "file_name", "media_type"):
        if src[key] != spec_src[key]:
            raise SupportedDraftClaimsValidationError(
                "UPSTREAM_DOCUMENT_IDENTITY_MISMATCH",
                paths=(f"/document_metadata/{key}",),
            )
    if ("sha256" in src) != ("sha256" in spec_src) or src.get("sha256") != spec_src.get("sha256"):
        raise SupportedDraftClaimsValidationError(
            "UPSTREAM_DOCUMENT_IDENTITY_MISMATCH",
            paths=("/document_metadata/sha256",),
        )
    metadata = specification["document_metadata"]
    if (
        metadata["language"] != "en"
        or metadata["target_jurisdiction"] != "US"
        or spec_src.get("synthetic") is not True
    ):
        raise SupportedDraftClaimsValidationError("UPSTREAM_DOCUMENT_IDENTITY_MISMATCH", paths=("/specification/document_metadata",))
    try:
        validate_generated_specification(
            specification,
            source,
            config["p2_003_generation_config"],
        )
    except USPTOGenerationValidationError:
        raise SupportedDraftClaimsValidationError("INVALID_SPECIFICATION", paths=("/specification",)) from None
    claims = specification["claims"]
    if (
        claims["status"] != "MISSING"
        or claims["claims"] != []
        or "preamble" in claims
        or specification["review_package"]["claim_support"] != []
        or specification["review_boundary"]["claims_runtime_implemented"] is not False
    ):
        raise SupportedDraftClaimsValidationError("INVALID_SPECIFICATION", paths=("/specification/claims",))
    return deepcopy(source), deepcopy(specification), config


def source_identity(
    reconstruction: dict[str, Any],
    specification: dict[str, Any],
) -> dict[str, Any]:
    metadata = reconstruction["document_metadata"]
    result = {
        "document_id": metadata["document_id"],
        "file_name": metadata["file_name"],
        "media_type": metadata["media_type"],
        "source_document_synthetic": True,
        "p2_002_identity": "p2-002-sha256-" + sha256_canonical(reconstruction),
        "p2_003_draft_id": specification["document_metadata"]["draft_id"],
        "p2_003_content_sha256": sha256_canonical(specification),
    }
    if "sha256" in metadata:
        result["source_sha256"] = metadata["sha256"]
    return result


def claims_draft_id(identity: dict[str, Any], canonical_config: dict[str, Any]) -> str:
    material = [
        identity["p2_002_identity"],
        identity["p2_003_draft_id"],
        identity["p2_003_content_sha256"],
        canonical_config,
    ]
    return "p2-004-" + hashlib.sha256(canonical_json(material).encode("utf-8")).hexdigest()[:24]


def _validate_dependency_graph(output: dict[str, Any]) -> None:
    """Validate claim-parent semantics independently of generator reprojection."""
    claims = output["claims"]
    numbers = [claim["claim_number"] for claim in claims]
    if numbers != list(range(1, len(numbers) + 1)) or len(set(numbers)) != len(numbers):
        raise SupportedDraftClaimsValidationError("CLAIM_DEPENDENCY_INVALID", paths=("/output/claims",))

    by_number = {claim["claim_number"]: claim for claim in claims}
    family_independent: dict[str, int] = {}
    for claim in claims:
        number = claim["claim_number"]
        parents = claim["depends_on"]
        if claim["independent_or_dependent"] == "INDEPENDENT":
            if parents:
                raise SupportedDraftClaimsValidationError("CLAIM_DEPENDENCY_INVALID", paths=(f"/output/claims/{number-1}/depends_on",))
            if claim["claim_family_id"] in family_independent:
                raise SupportedDraftClaimsValidationError("CLAIM_DEPENDENCY_INVALID", paths=("/output/claims",))
            family_independent[claim["claim_family_id"]] = number
            continue

        if len(parents) != 1:
            raise SupportedDraftClaimsValidationError("CLAIM_DEPENDENCY_INVALID", paths=(f"/output/claims/{number-1}/depends_on",))
        parent_number = parents[0]
        parent = by_number.get(parent_number)
        if (
            parent is None
            or parent_number >= number
            or parent_number == number
            or parent["independent_or_dependent"] != "INDEPENDENT"
            or parent["depends_on"]
            or parent["claim_family_id"] != claim["claim_family_id"]
            or parent["claim_type"] != claim["claim_type"]
        ):
            raise SupportedDraftClaimsValidationError("CLAIM_DEPENDENCY_INVALID", paths=(f"/output/claims/{number-1}/depends_on",))
        expected_parent = family_independent.get(claim["claim_family_id"])
        if expected_parent is None or parent_number != expected_parent:
            raise SupportedDraftClaimsValidationError("CLAIM_DEPENDENCY_INVALID", paths=(f"/output/claims/{number-1}/depends_on",))

    family_records = {family["claim_family_id"]: family for family in output["claim_families"]}
    if len(family_records) != len(output["claim_families"]):
        raise SupportedDraftClaimsValidationError("CLAIM_DEPENDENCY_INVALID", paths=("/output/claim_families",))
    for family_id, family in family_records.items():
        member_numbers = [claim["claim_number"] for claim in claims if claim["claim_family_id"] == family_id]
        independent = family_independent.get(family_id)
        if family["status"] == "PRESENT":
            if independent is None or family["independent_claim_number"] != independent:
                raise SupportedDraftClaimsValidationError("CLAIM_DEPENDENCY_INVALID", paths=("/output/claim_families",))
            if family["dependent_claim_numbers"] != [n for n in member_numbers if n != independent]:
                raise SupportedDraftClaimsValidationError("CLAIM_DEPENDENCY_INVALID", paths=("/output/claim_families",))
        elif member_numbers or family["independent_claim_number"] is not None or family["dependent_claim_numbers"]:
            raise SupportedDraftClaimsValidationError("CLAIM_DEPENDENCY_INVALID", paths=("/output/claim_families",))


def validate_supported_draft_claims(
    output: Any,
    reconstruction: Any,
    specification: Any,
    generation_config: Any,
) -> None:
    source, spec, config = validate_inputs(reconstruction, specification, generation_config)
    errors = sorted(
        Draft202012Validator(output_schema()).iter_errors(output),
        key=lambda error: tuple(str(x) for x in error.absolute_path),
    )
    if errors:
        paths = tuple(
            "/output" + ("/" + "/".join(str(x) for x in error.absolute_path) if error.absolute_path else "")
            for error in errors
        )
        if any("/depends_on" in path for path in paths):
            raise SupportedDraftClaimsValidationError("CLAIM_DEPENDENCY_INVALID", paths=paths)
        raise SupportedDraftClaimsValidationError("CLAIM_SUPPORT_INCOMPLETE", paths=paths or ("/output",))

    _validate_dependency_graph(output)

    from backend.app.services.supported_draft_claims_generation import _build_supported_draft_claims

    expected = _build_supported_draft_claims(source, spec, config)
    if output == expected:
        return

    if type(output) is dict and type(output.get("claims")) is list:
        expected_claims = {x["claim_number"]: x for x in expected["claims"]}
        for claim in output["claims"]:
            if type(claim) is not dict or type(claim.get("claim_number")) is not int:
                continue
            original = expected_claims.get(claim["claim_number"])
            if original is None or claim.get("depends_on") != original["depends_on"]:
                raise SupportedDraftClaimsValidationError("CLAIM_DEPENDENCY_INVALID", paths=("/output/claims",))
            actual_elements = claim.get("claim_elements")
            expected_elements = original["claim_elements"]
            if type(actual_elements) is list and len(actual_elements) == len(expected_elements):
                for actual_element, expected_element in zip(actual_elements, expected_elements):
                    if type(actual_element) is not dict:
                        continue
                    if actual_element == expected_element:
                        continue
                    role = expected_element.get("element_role")
                    if role == "PARAMETER" and actual_element.get("text") != expected_element.get("text"):
                        raise SupportedDraftClaimsValidationError("CLAIM_PARAMETER_BROADENING", paths=("/output/claims",))
                    if role == "RELATIONSHIP" and (
                        actual_element.get("text") != expected_element.get("text")
                        or actual_element.get("relationship_type") != expected_element.get("relationship_type")
                    ):
                        raise SupportedDraftClaimsValidationError("CLAIM_RELATIONSHIP_STRENGTHENING", paths=("/output/claims",))
                    actual_text = actual_element.get("text")
                    expected_text = expected_element.get("text")
                    if type(actual_text) is str and type(expected_text) is str and actual_text != expected_text:
                        lowered = actual_text.casefold()
                        expected_lowered = expected_text.casefold()
                        negative_tokens = (" no ", " not ", " without ", " excluding ", " absent ", " lacks ")
                        if any(token in f" {lowered} " and token not in f" {expected_lowered} " for token in negative_tokens):
                            raise SupportedDraftClaimsValidationError("CLAIM_NEGATIVE_LIMITATION_UNSUPPORTED", paths=("/output/claims",))
            if claim.get("claim_text") != original["claim_text"] or actual_elements != expected_elements:
                raise SupportedDraftClaimsValidationError("CANONICAL_CLAIM_TEXT_MISMATCH", paths=("/output/claims",))
    raise SupportedDraftClaimsValidationError("CLAIM_SUPPORT_INCOMPLETE", paths=("/output",))
