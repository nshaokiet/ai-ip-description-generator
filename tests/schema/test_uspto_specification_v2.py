from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = (
    REPO_ROOT
    / "schemas"
    / "uspto-specification"
    / "v2.0.0"
    / "uspto-specification.schema.json"
)
FIXTURE_DIR = (
    REPO_ROOT / "tests" / "fixtures" / "uspto-specification" / "v2.0.0"
)

CANONICAL_SECTION_ORDER = [
    "TITLE_OF_THE_INVENTION",
    "CROSS_REFERENCE_TO_RELATED_APPLICATIONS",
    "STATEMENT_REGARDING_FEDERALLY_SPONSORED_RESEARCH_OR_DEVELOPMENT",
    "NAMES_OF_PARTIES_TO_JOINT_RESEARCH_AGREEMENT",
    "INCORPORATION_BY_REFERENCE",
    "STATEMENT_REGARDING_PRIOR_DISCLOSURES",
    "BACKGROUND_OF_THE_INVENTION",
    "BRIEF_SUMMARY_OF_THE_INVENTION",
    "BRIEF_DESCRIPTION_OF_THE_DRAWINGS",
    "DETAILED_DESCRIPTION_OF_THE_INVENTION",
    "CLAIMS",
    "ABSTRACT_OF_THE_DISCLOSURE",
    "SEQUENCE_LISTING",
]

ADMINISTRATIVE_SECTION_IDS = {
    "CROSS_REFERENCE_TO_RELATED_APPLICATIONS",
    "STATEMENT_REGARDING_FEDERALLY_SPONSORED_RESEARCH_OR_DEVELOPMENT",
    "NAMES_OF_PARTIES_TO_JOINT_RESEARCH_AGREEMENT",
    "INCORPORATION_BY_REFERENCE",
    "STATEMENT_REGARDING_PRIOR_DISCLOSURES",
}

V1_IMMUTABLE_SHA256 = {
    "schemas/patent-draft/v1.0.0/patent-draft.schema.json": (
        "9f08aa2487b9bcacd3e40885899c6d7871f1df88b27cfc6d5ad85f01bbf3cb21"
    ),
    "schemas/patent-draft/v1.0.0/README.md": (
        "8449b2e2975b2661184a8e616dc5972ca773e969105fe6eb87342f1c53b869cd"
    ),
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


SCHEMA = load_json(SCHEMA_PATH)
VALIDATOR = Draft202012Validator(SCHEMA)


def load_fixture(name: str) -> dict[str, Any]:
    return load_json(FIXTURE_DIR / name)


def schema_errors(document: dict[str, Any]) -> list[Any]:
    return sorted(VALIDATOR.iter_errors(document), key=lambda error: list(error.path))


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE))


def _iter_paragraphs(document: dict[str, Any]):
    for section_index, section in enumerate(document["sections"]):
        for paragraph_index, paragraph in enumerate(section["paragraphs"]):
            yield f"/sections/{section_index}/paragraphs/{paragraph_index}", paragraph
        for subsection_index, subsection in enumerate(section["subsections"]):
            for paragraph_index, paragraph in enumerate(subsection["paragraphs"]):
                yield (
                    f"/sections/{section_index}/subsections/{subsection_index}"
                    f"/paragraphs/{paragraph_index}"
                ), paragraph


def validate_business_rules(document: dict[str, Any]) -> list[dict[str, str]]:
    """Validate cross-object v2 rules that JSON Schema cannot express safely."""

    violations: list[dict[str, str]] = []

    def add(code: str, path: str, message: str) -> None:
        violations.append({"code": code, "path": path, "message": message})

    evidence = document["review_package"]["evidence"]
    evidence_by_id = {item["evidence_id"]: item for item in evidence}
    missing_ids = {
        item["missing_id"] for item in document["review_package"]["missing_information"]
    }

    rendered_order = [item["section_id"] for item in document["sections"][:10]]
    rendered_order.extend(
        [document["claims"]["section_id"], document["abstract"]["section_id"]]
    )
    rendered_order.extend(item["section_id"] for item in document["sections"][10:])
    if document["section_order"] != CANONICAL_SECTION_ORDER:
        add("INVALID_CANONICAL_SECTION_ORDER", "/section_order", "Order is not canonical.")
    if rendered_order != CANONICAL_SECTION_ORDER:
        add("INVALID_RENDERED_SECTION_ORDER", "/sections", "Rendered order is not canonical.")

    for path, paragraph in _iter_paragraphs(document):
        for evidence_id in paragraph["support"]["evidence_ids"]:
            if evidence_id not in evidence_by_id:
                add("UNKNOWN_EVIDENCE_ID", path, f"Unknown evidence ID {evidence_id}.")

    for index, section in enumerate(document["sections"]):
        for missing_id in section["missing_information_ids"]:
            if missing_id not in missing_ids:
                add("UNKNOWN_MISSING_INFORMATION_ID", f"/sections/{index}", missing_id)
        for sub_index, subsection in enumerate(section["subsections"]):
            for missing_id in subsection["missing_information_ids"]:
                if missing_id not in missing_ids:
                    add(
                        "UNKNOWN_MISSING_INFORMATION_ID",
                        f"/sections/{index}/subsections/{sub_index}",
                        missing_id,
                    )

        if section["status"] == "NOT_APPLICABLE":
            basis = section["not_applicable_basis"]
            allowed_type = {
                "HUMAN_CONFIRMED": "HUMAN_CONFIRMATION",
                "APPROVED_DETERMINISTIC_RULE": "APPROVED_RULE",
            }[basis["decision_source"]]
            for evidence_id in basis["evidence_ids"]:
                evidence_item = evidence_by_id.get(evidence_id)
                if evidence_item is None or evidence_item["evidence_type"] != allowed_type:
                    add(
                        "INVALID_NOT_APPLICABLE_SUPPORT",
                        f"/sections/{index}/not_applicable_basis",
                        "NOT_APPLICABLE must be supported by the declared decision source.",
                    )

        if section["section_id"] in ADMINISTRATIVE_SECTION_IDS:
            if section["status"] == "PRESENT":
                for paragraph_index, paragraph in enumerate(section["paragraphs"]):
                    support = paragraph["support"]
                    valid_class = support["grounding_class"] in {
                        "HUMAN_CONFIRMED",
                        "SOURCE_FACT",
                    }
                    valid_evidence = bool(support["evidence_ids"]) and all(
                        evidence_by_id.get(evidence_id, {}).get("evidence_type")
                        in {"HUMAN_CONFIRMATION", "AUTHORIZED_EXTERNAL_SOURCE"}
                        for evidence_id in support["evidence_ids"]
                    )
                    if not (valid_class and valid_evidence):
                        add(
                            "ADMINISTRATIVE_SUPPORT_INVALID",
                            f"/sections/{index}/paragraphs/{paragraph_index}",
                            "Administrative facts require Human confirmation or an authorized external source.",
                        )

    abstract = document["abstract"]
    actual_word_count = word_count(abstract["text"])
    if abstract["status"] == "PRESENT":
        if actual_word_count > 150:
            add(
                "ABSTRACT_WORD_LIMIT_EXCEEDED",
                "/abstract/text",
                f"Abstract has {actual_word_count} words; maximum is 150.",
            )
        if abstract["word_count"] != actual_word_count:
            add(
                "ABSTRACT_WORD_COUNT_MISMATCH",
                "/abstract/word_count",
                f"Declared {abstract['word_count']}; actual {actual_word_count}.",
            )

    for missing_id in document["claims"]["missing_information_ids"]:
        if missing_id not in missing_ids:
            add("UNKNOWN_MISSING_INFORMATION_ID", "/claims", missing_id)
    for missing_id in abstract["missing_information_ids"]:
        if missing_id not in missing_ids:
            add("UNKNOWN_MISSING_INFORMATION_ID", "/abstract", missing_id)

    claims = document["claims"]["claims"]
    claim_numbers = [claim["claim_number"] for claim in claims]
    if len(claim_numbers) != len(set(claim_numbers)):
        add("DUPLICATE_CLAIM_NUMBER", "/claims/claims", "Claim numbers must be unique.")
    if claims and claim_numbers != list(range(1, len(claims) + 1)):
        add("NONCONTIGUOUS_CLAIM_NUMBER", "/claims/claims", "Claims must start at 1.")

    claim_number_set = set(claim_numbers)
    for claim_index, claim in enumerate(claims):
        claim_number = claim["claim_number"]
        for dependency in claim["depends_on"]:
            if dependency not in claim_number_set or dependency >= claim_number:
                add(
                    "INVALID_CLAIM_DEPENDENCY",
                    f"/claims/claims/{claim_index}/depends_on",
                    f"Claim {claim_number} cannot depend on claim {dependency}.",
                )
        for element_index, element in enumerate(claim["claim_elements"]):
            path = f"/claims/claims/{claim_index}/claim_elements/{element_index}"
            if element["support_status"] == "UNSUPPORTED":
                add(
                    "UNSUPPORTED_CLAIM_ELEMENT",
                    path,
                    f"Claim element {element['element_id']} has no support.",
                )
            if element["support_status"] == "SUPPORTED" and (
                not element["evidence_ids"] or not element["specification_section_ids"]
            ):
                add(
                    "SUPPORTED_CLAIM_ELEMENT_MISSING_LINKS",
                    path,
                    "Supported claim elements require evidence and specification links.",
                )
            for evidence_id in element["evidence_ids"]:
                if evidence_id not in evidence_by_id:
                    add("UNKNOWN_EVIDENCE_ID", path, f"Unknown evidence ID {evidence_id}.")

    return violations


def violation_codes(document: dict[str, Any]) -> set[str]:
    return {item["code"] for item in validate_business_rules(document)}


def test_schema_self_validates_under_draft_2020_12() -> None:
    Draft202012Validator.check_schema(SCHEMA)


def test_representative_fixture_passes_schema_and_business_rules() -> None:
    document = load_fixture("representative.json")
    assert schema_errors(document) == []
    assert validate_business_rules(document) == []


@pytest.mark.parametrize(
    "fixture_name",
    [
        "representative.json",
        "missing-administrative-information.json",
        "unsupported-claim-element.json",
    ],
)
def test_all_fixtures_are_synthetic(fixture_name: str) -> None:
    document = load_fixture(fixture_name)
    assert document["document_metadata"]["source_document"]["synthetic"] is True


def test_target_contract_does_not_hard_code_future_sources_as_synthetic() -> None:
    document = load_fixture("representative.json")
    document["document_metadata"]["source_document"]["synthetic"] = False
    assert schema_errors(document) == []


def test_wrong_section_order_fails_schema_validation() -> None:
    document = load_fixture("representative.json")
    document["sections"][0], document["sections"][1] = (
        document["sections"][1],
        document["sections"][0],
    )
    assert schema_errors(document)


@pytest.mark.parametrize(
    ("path", "key"),
    [
        ([], "unexpected_root_property"),
        (["document_metadata"], "unexpected_metadata_property"),
        (["sections", 0, "paragraphs", 0], "unexpected_paragraph_property"),
        (["claims", "claims", 0], "unexpected_claim_property"),
    ],
)
def test_extra_properties_fail_schema_validation(path: list[Any], key: str) -> None:
    document = load_fixture("representative.json")
    target: Any = document
    for part in path:
        target = target[part]
    target[key] = "not allowed"
    assert schema_errors(document)


def test_abstract_over_150_words_fails_validation() -> None:
    document = load_fixture("representative.json")
    document["abstract"]["text"] = " ".join(["word"] * 151)
    document["abstract"]["word_count"] = 151
    assert schema_errors(document)
    assert "ABSTRACT_WORD_LIMIT_EXCEEDED" in violation_codes(document)


def test_invalid_claim_dependency_is_detected() -> None:
    document = load_fixture("representative.json")
    document["claims"]["claims"][1]["depends_on"] = [99]
    assert schema_errors(document) == []
    assert "INVALID_CLAIM_DEPENDENCY" in violation_codes(document)


def test_unsupported_claim_element_fixture_is_detected() -> None:
    document = load_fixture("unsupported-claim-element.json")
    assert schema_errors(document) == []
    assert "UNSUPPORTED_CLAIM_ELEMENT" in violation_codes(document)


def test_missing_administrative_information_stays_explicit() -> None:
    document = load_fixture("missing-administrative-information.json")
    assert schema_errors(document) == []
    assert validate_business_rules(document) == []
    assert all(
        section["status"] in {"MISSING", "HUMAN_CONFIRMATION_REQUIRED"}
        for section in document["sections"]
        if section["section_id"] in ADMINISTRATIVE_SECTION_IDS
    )

    silent_fact = copy.deepcopy(document)
    silent_fact["sections"][1].update(
        {
            "status": "PRESENT",
            "missing_information_ids": [],
            "paragraphs": [
                {
                    "paragraph_id": "P-ADMIN-UNSUPPORTED",
                    "sequence": 1,
                    "text": "This application claims priority to an unspecified application.",
                    "support": {
                        "source_paths": ["/title"],
                        "evidence_ids": ["EV-SOURCE-TITLE"],
                        "grounding_class": "INFERENCE",
                    },
                }
            ],
        }
    )
    assert schema_errors(silent_fact) == []
    assert "ADMINISTRATIVE_SUPPORT_INVALID" in violation_codes(silent_fact)


def test_claims_section_is_required_and_modeled_separately() -> None:
    assert "claims" in SCHEMA["required"]
    assert SCHEMA["properties"]["claims"]["$ref"] == "#/$defs/claims_section"
    assert SCHEMA["properties"]["section_order"]["const"] == CANONICAL_SECTION_ORDER


def test_v1_contract_files_are_immutable() -> None:
    for relative_path, expected_hash in V1_IMMUTABLE_SHA256.items():
        actual_hash = hashlib.sha256((REPO_ROOT / relative_path).read_bytes()).hexdigest()
        assert actual_hash == expected_hash, relative_path

    v1_schema = load_json(
        REPO_ROOT / "schemas" / "patent-draft" / "v1.0.0" / "patent-draft.schema.json"
    )
    serialized = json.dumps(v1_schema, sort_keys=True)
    assert "SAFE_GENERALIZATION" not in serialized
    assert "PROPOSED_VARIANT" not in serialized


@pytest.mark.parametrize(
    ("file_name", "expected_number", "expected_independent_claims"),
    [
        ("US11367264B2-section-map.json", "US11367264", [1, 18, 19]),
        ("US11044591B2-section-map.json", "US11044591", [1, 10, 15]),
    ],
)
def test_reference_maps_are_structural_and_cover_canonical_sections(
    file_name: str,
    expected_number: str,
    expected_independent_claims: list[int],
) -> None:
    section_map = load_json(REPO_ROOT / "docs" / "references" / file_name)
    assert section_map["patent_number"] == expected_number
    assert section_map["kind_code"] == "B2"
    assert section_map["structural_reference_only"] is True
    assert [item["canonical_section"] for item in section_map["sections"]] == (
        CANONICAL_SECTION_ORDER
    )
    assert section_map["claims_summary"]["count"] == 21
    assert section_map["claims_summary"]["independent_claim_numbers"] == (
        expected_independent_claims
    )
    assert "substantive_text" not in section_map
