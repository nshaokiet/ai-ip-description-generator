"""P2-005 deterministic synthetic-only USPTO v2 disclosure + Claims assembly.

This package is an additive contract. P2-003's original output and its runtime
claims=false invariant are preserved verbatim as review evidence.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any

from backend.app.services.supported_draft_claims_validation import (
    sha256_canonical,
)
from backend.app.services.uspto_document_package_validation import (
    validate_assembly_inputs,
    validate_uspto_document_package,
)


CLAIM_FIELDS = (
    "claim_number", "claim_type", "independent_or_dependent",
    "depends_on", "claim_text",
)
ELEMENT_FIELDS = (
    "element_id", "sequence", "text", "evidence_ids",
    "specification_section_ids", "support_status",
)
SUPPORT_FIELDS = (
    "claim_number", "element_id", "support_status", "evidence_ids",
    "specification_section_ids",
)


def _project_fields(value: dict[str, Any], keys: tuple[str, ...]) -> dict[str, Any]:
    return {key: deepcopy(value[key]) for key in keys}


def _assemble_verified(
    envelope: dict[str, Any],
    analysis: dict[str, Any],
    reconstruction: dict[str, Any],
    specification: dict[str, Any],
    p2_config: dict[str, Any],
    supported_claims: dict[str, Any],
    p4_config: dict[str, Any],
) -> dict[str, Any]:
    """Pure projection; caller must validate the full upstream provenance first."""
    projected = []
    for claim in supported_claims["claims"]:
        item = _project_fields(claim, CLAIM_FIELDS)
        item["claim_elements"] = [
            _project_fields(element, ELEMENT_FIELDS)
            for element in claim["claim_elements"]
        ]
        projected.append(item)

    review = supported_claims["review_package"]
    missing = []
    extra_missing = []
    if not projected:
        missing = [item["missing_id"] for item in review["missing_information"]]
        if not missing:
            missing = ["MI-P2-005-0001"]
            extra_missing = [{
                "missing_id": "MI-P2-005-0001",
                "reason_code": "NO_ELIGIBLE_SUPPORTED_CLAIMS",
                "source_issue_ids": sorted({x["issue_id"] for x in review["issues"]}),
            }]
    claims_section: dict[str, Any] = {
        "section_id": "CLAIMS",
        "sequence": 11,
        "heading": "CLAIMS",
        "status": "PRESENT" if projected else "HUMAN_CONFIRMATION_REQUIRED",
        "claims": projected,
        "missing_information_ids": missing,
    }
    if projected:
        claims_section["preamble"] = "What is claimed is:"

    filing = {
        "document_metadata": deepcopy(specification["document_metadata"]),
        "section_order": deepcopy(specification["section_order"]),
        "sections": deepcopy(specification["sections"]),
        "claims": claims_section,
        "abstract": deepcopy(specification["abstract"]),
    }
    package: dict[str, Any] = {
        "schema_version": "1.0.0",
        "output_type": "USPTO_DOCUMENT_PACKAGE",
        "source_identity": deepcopy(supported_claims["source_identity"]),
        "input_digests": {
            "source_envelope": sha256_canonical(envelope),
            "structured_analysis": sha256_canonical(analysis),
            "reconstruction": sha256_canonical(reconstruction),
            "specification": sha256_canonical(specification),
            "supported_claims": sha256_canonical(supported_claims),
        },
        "generation_config": deepcopy(p4_config),
        "filing_view": filing,
        "review_package": {
            "original_p2_003": deepcopy(specification),
            "original_p2_004": deepcopy(supported_claims),
            "projected_claim_support": [
                _project_fields(x, SUPPORT_FIELDS) for x in review["claim_support"]
            ],
            "assembly_missing_information": extra_missing,
        },
        "review_boundary": {
            "status": "DRAFT",
            "review_status": "UNREVIEWED",
            "human_ip_review_required": True,
            "filing_ready": False,
            "legal_advice": False,
            "patentability_assessment_included": False,
            "source_document_synthetic": True,
            "render_review_metadata_as_filing_content": False,
            "p2_003_claims_runtime_implemented": False,
        },
    }
    package["package_id"] = "p2-005-" + sha256_canonical(package)[:24]
    return package


def assemble_uspto_document_package(
    *,
    source_envelope: Any,
    structured_analysis: Any,
    reconstruction: Any,
    specification: Any,
    p2_003_generation_config: Any,
    supported_claims: Any,
    p2_004_generation_config: Any,
) -> dict[str, Any]:
    """Assemble only fully matched, validated synthetic upstream artifacts."""
    arguments = {
        "source_envelope": source_envelope,
        "structured_analysis": structured_analysis,
        "reconstruction": reconstruction,
        "specification": specification,
        "p2_003_generation_config": p2_003_generation_config,
        "supported_claims": supported_claims,
        "p2_004_generation_config": p2_004_generation_config,
    }
    verified = validate_assembly_inputs(**arguments)
    result = _assemble_verified(*verified)
    validate_uspto_document_package(result, **arguments)
    return result
