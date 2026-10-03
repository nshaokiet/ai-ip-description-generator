from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from backend.app.services.invention_reconstruction import reconstruct_invention
from backend.app.services.invention_reconstruction_validation import (
    RECONSTRUCTION_SCHEMA_PATH,
    load_reconstruction_schema,
)


ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "tests/fixtures/invention-reconstruction/v1.0.0"
REPRESENTATIVE = FIXTURES / "representative-system.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def schema() -> dict:
    return load_reconstruction_schema()


@pytest.fixture()
def reconstruction() -> dict:
    fixture = load(REPRESENTATIVE)
    return reconstruct_invention(fixture["source_envelope"], fixture["structured_analysis"])


def errors(schema: dict, payload: dict):
    return list(Draft202012Validator(schema).iter_errors(payload))


def test_schema_exists_at_canonical_path() -> None:
    assert RECONSTRUCTION_SCHEMA_PATH.is_file()


def test_schema_is_draft_2020_12_and_self_validates(schema: dict) -> None:
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["$id"] == "urn:ai-ip-description-generator:invention-reconstruction:1.0.0"
    Draft202012Validator.check_schema(schema)


def test_representative_service_output_validates(schema: dict, reconstruction: dict) -> None:
    assert not errors(schema, reconstruction)


def test_root_identity_is_fixed(schema: dict, reconstruction: dict) -> None:
    wrong_version = copy.deepcopy(reconstruction)
    wrong_version["schema_version"] = "2.0.0"
    assert errors(schema, wrong_version)
    wrong_type = copy.deepcopy(reconstruction)
    wrong_type["output_type"] = "USPTO_SPECIFICATION_DRAFT"
    assert errors(schema, wrong_type)


@pytest.mark.parametrize(
    ("field", "invalid"),
    [
        ("status", "FINAL"),
        ("human_review_required", False),
        ("is_legal_advice", True),
        ("filing_ready", True),
        ("includes_patentability_assessment", True),
        ("includes_claims", True),
    ],
)
def test_output_notice_boundaries_are_mechanical(
    schema: dict, reconstruction: dict, field: str, invalid: object
) -> None:
    reconstruction["output_notice"][field] = invalid
    assert errors(schema, reconstruction)


def test_root_and_nested_unknown_fields_are_rejected(schema: dict, reconstruction: dict) -> None:
    root = copy.deepcopy(reconstruction)
    root["claims"] = []
    assert errors(schema, root)
    nested = copy.deepcopy(reconstruction)
    nested["invention_model"]["elements"][0]["inventor"] = "Synthetic Person"
    assert errors(schema, nested)


def test_contract_enums_cover_reviewed_vocabularies(schema: dict) -> None:
    defs = schema["$defs"]
    assert defs["element"]["properties"]["element_type"]["enum"] == [
        "DEVICE", "MODULE", "STRUCTURE", "MATERIAL", "SOFTWARE_COMPONENT",
        "DATA_STRUCTURE", "PROCESSING_BLOCK", "CHEMICAL_ELEMENT",
        "BIOLOGICAL_ELEMENT", "OTHER",
    ]
    assert "DEPENDS_ON" in defs["relationship"]["properties"]["relation_type"]["enum"]
    assert defs["flow"]["properties"]["flow_type"]["enum"][-1] == "UNSPECIFIED"
    assert defs["parameter_value"]["properties"]["value_kind"]["enum"] == [
        "EXACT", "RANGE", "SET", "QUALITATIVE"
    ]


def test_safe_generalization_requires_metadata(schema: dict, reconstruction: dict) -> None:
    support = reconstruction["invention_model"]["elements"][0]["support"]
    support["grounding_class"] = "SAFE_GENERALIZATION"
    assert errors(schema, reconstruction)
    support["generalization"] = {
        "rule_id": "SG-01_EXPLICIT_SOURCE_CATEGORY",
        "generalized_term": "optical sensor",
        "member_terms": ["sensor"],
        "evidence_ids": ["EV-P0001-C001"],
    }
    assert not errors(schema, reconstruction)


def test_generalization_metadata_is_forbidden_for_other_grounding(schema: dict, reconstruction: dict) -> None:
    reconstruction["invention_model"]["elements"][0]["support"]["generalization"] = {
        "rule_id": "SG-01_EXPLICIT_SOURCE_CATEGORY",
        "generalized_term": "optical sensor",
        "member_terms": ["sensor"],
        "evidence_ids": ["EV-P0001-C001"],
    }
    assert errors(schema, reconstruction)


def test_missing_technical_field_cannot_carry_invented_content(schema: dict, reconstruction: dict) -> None:
    reconstruction["invention_model"]["technical_field"] = {
        "status": "MISSING",
        "name": "Invented field",
    }
    assert errors(schema, reconstruction)


def test_conflict_requires_two_supported_alternatives(schema: dict, reconstruction: dict) -> None:
    reconstruction["review_package"]["conflicts"] = [{
        "conflict_id": "IR-CONFLICT-0001",
        "topic": "Synthetic conflict",
        "affected_entity_ids": ["IR-ELEM-0001"],
        "alternatives": [{
            "statement": "One side",
            "evidence_ids": ["EV-P0001-C001"],
            "analysis_paths": ["/missing_information/0"],
        }],
        "status": "UNRESOLVED",
    }]
    assert errors(schema, reconstruction)


def test_fixture_corpus_contains_all_sixteen_reviewed_cases() -> None:
    fixtures = sorted(FIXTURES.glob("*.json"))
    assert len(fixtures) == 16
    cases = {load(path)["case"] for path in fixtures}
    assert cases == {
        "representative_system", "multi_component_system", "method_process",
        "parameter_heavy", "multiple_embodiments", "table_evidence",
        "missing_information", "conflict", "valid_safe_generalization",
        "invalid_safe_generalization", "proposed_variant",
        "prompt_injection_source", "dangling_reference",
        "unsupported_range_broadening", "administrative_fabrication",
        "claims_leakage",
    }


def test_released_upstream_schema_is_not_redefined(schema: dict) -> None:
    serialized = json.dumps(schema)
    assert "source_units" not in schema["properties"]
    assert "STRUCTURED_INVENTION_ANALYSIS" not in schema["properties"]
    assert '"source_envelope"' not in serialized


@pytest.mark.parametrize("extra", ["minimum", "maximum", "values", "qualitative_value"])
def test_exact_parameter_cannot_carry_other_value_kinds(schema, reconstruction, extra) -> None:
    reconstruction["invention_model"]["parameters"][0]["value"][extra] = (
        [25] if extra == "values" else "stable" if extra == "qualitative_value" else 25
    )
    assert errors(schema, reconstruction)


def test_each_object_definition_is_strict(schema) -> None:
    for name, definition in schema["$defs"].items():
        if definition.get("type") == "object":
            assert definition["additionalProperties"] is False, name
