"""Reproduce the frozen additive P2-005 schema from released local contracts.

No network access; the embedded P2-001/P2-004 definitions are version-pinned
in the generated JSON. This script never changes either released source.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent


def _embedded(relative: str, namespace: str) -> dict:
    value = json.loads((ROOT / relative).read_text(encoding="utf-8"))
    # These contracts become subschemas of the package. Their original absolute
    # $id would otherwise redirect rewritten local $refs away from the package.
    value.pop("$id", None)
    value.pop("$schema", None)

    def visit(node: object) -> None:
        if isinstance(node, dict):
            for key, item in node.items():
                if key == "$ref" and isinstance(item, str) and item.startswith("#/"):
                    node[key] = f"#/$defs/{namespace}/{item[2:]}"
                else:
                    visit(item)
        elif isinstance(node, list):
            for item in node:
                visit(item)

    visit(value)
    return value


def build() -> dict:
    p1 = _embedded("schemas/uspto-specification/v2.0.0/uspto-specification.schema.json", "p2_001")
    p4 = _embedded("schemas/supported-draft-claims/v1.0.0/supported-draft-claims.schema.json", "p2_004")
    digest = {"type": "string", "pattern": "^[a-f0-9]{64}$"}
    ref = lambda name: {"$ref": f"#/$defs/p2_001/properties/{name}"}
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://github.com/nshaokiet/ai-ip-description-generator/schemas/uspto-document-package/v1.0.0/uspto-document-package.schema.json",
        "title": "USPTO_DOCUMENT_PACKAGE v1.0.0 — synthetic offline draft assembly",
        "type": "object", "additionalProperties": False,
        "required": ["schema_version", "output_type", "package_id", "source_identity", "input_digests", "generation_config", "filing_view", "review_package", "review_boundary"],
        "properties": {
            "schema_version": {"const": "1.0.0"},
            "output_type": {"const": "USPTO_DOCUMENT_PACKAGE"},
            "package_id": {"type": "string", "pattern": "^p2-005-[a-f0-9]{24}$"},
            "source_identity": {"$ref": "#/$defs/p2_004/$defs/source_identity"},
            "input_digests": {
                "type": "object", "additionalProperties": False,
                "required": ["source_envelope", "structured_analysis", "reconstruction", "specification", "supported_claims"],
                "properties": {key: digest for key in ("source_envelope", "structured_analysis", "reconstruction", "specification", "supported_claims")},
            },
            "generation_config": {"$ref": "#/$defs/p2_004/$defs/generation_config"},
            "filing_view": {
                "type": "object", "additionalProperties": False,
                "required": ["document_metadata", "section_order", "sections", "claims", "abstract"],
                "properties": {key: ref(key) for key in ("document_metadata", "section_order", "sections", "claims", "abstract")},
            },
            "review_package": {
                "type": "object", "additionalProperties": False,
                "required": ["original_p2_003", "original_p2_004", "projected_claim_support", "assembly_missing_information"],
                "properties": {
                    "original_p2_003": {"$ref": "#/$defs/p2_001"},
                    "original_p2_004": {"$ref": "#/$defs/p2_004"},
                    "projected_claim_support": {"type": "array", "items": {"$ref": "#/$defs/p2_001/$defs/claim_support"}},
                    "assembly_missing_information": {
                        "type": "array", "maxItems": 1,
                        "items": {
                            "type": "object", "additionalProperties": False,
                            "required": ["missing_id", "reason_code", "source_issue_ids"],
                            "properties": {
                                "missing_id": {"const": "MI-P2-005-0001"},
                                "reason_code": {"const": "NO_ELIGIBLE_SUPPORTED_CLAIMS"},
                                "source_issue_ids": {"type": "array", "uniqueItems": True, "items": {"type": "string", "pattern": "^ISS-P2-004-[0-9]{4,}$"}},
                            },
                        },
                    },
                },
            },
            "review_boundary": {
                "type": "object", "additionalProperties": False,
                "required": ["status", "review_status", "human_ip_review_required", "filing_ready", "legal_advice", "patentability_assessment_included", "source_document_synthetic", "render_review_metadata_as_filing_content", "p2_003_claims_runtime_implemented"],
                "properties": {
                    "status": {"const": "DRAFT"},
                    "review_status": {"const": "UNREVIEWED"},
                    "human_ip_review_required": {"const": True},
                    "filing_ready": {"const": False},
                    "legal_advice": {"const": False},
                    "patentability_assessment_included": {"const": False},
                    "source_document_synthetic": {"const": True},
                    "render_review_metadata_as_filing_content": {"const": False},
                    "p2_003_claims_runtime_implemented": {"const": False},
                },
            },
        },
        "$defs": {"p2_001": p1, "p2_004": p4},
    }


if __name__ == "__main__":
    destination = HERE / "uspto-document-package.schema.json"
    destination.write_text(json.dumps(build(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
