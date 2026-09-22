"""Tests for Checkpoint C canonical draft validation and normalization."""

import copy
import json
from pathlib import Path

import pytest
from jsonschema.exceptions import ValidationError

from backend.app.services.draft_validation import (
    DraftValidationError,
    normalize_draft_provider_output,
    validate_canonical_draft,
)


def _load_schema() -> dict:
    schema_path = Path(__file__).resolve().parents[2] / "schemas" / "patent-draft" / "v1.0.0" / "patent-draft.schema.json"
    with schema_path.open(encoding="utf-8") as f:
        return json.load(f)


def _load_valid_fixture() -> dict:
    fixture_path = Path(__file__).resolve().parents[2] / "tests" / "fixtures" / "patent-draft" / "v1.0.0" / "cases" / "representative.json"
    with fixture_path.open(encoding="utf-8") as f:
        data = json.load(f)
        return data["expected_output"]


def test_optional_null_is_removed():
    """1. optional top-level/nested property null is removed"""
    schema = {
        "type": "object",
        "properties": {
            "req": {"type": "string"},
            "opt": {"type": "string"},
            "nested": {
                "type": "object",
                "properties": {
                    "nested_req": {"type": "string"},
                    "nested_opt": {"type": "string"}
                },
                "required": ["nested_req"]
            }
        },
        "required": ["req", "nested"]
    }
    provider_output = {
        "req": "x",
        "opt": None,
        "nested": {
            "nested_req": "y",
            "nested_opt": None
        }
    }
    normalized = normalize_draft_provider_output(provider_output, schema)
    assert normalized == {
        "req": "x",
        "nested": {
            "nested_req": "y"
        }
    }


def test_required_null_is_preserved_and_fails_validation():
    """2. canonically required null is preserved, 3. preserved required null fails canonical validation"""
    schema = {
        "type": "object",
        "properties": {
            "req": {"type": "string"},
            "opt": {"type": "string"}
        },
        "required": ["req"]
    }
    provider_output = {
        "req": None,
        "opt": "x"
    }
    normalized = normalize_draft_provider_output(provider_output, schema)
    assert normalized == {"req": None, "opt": "x"}
    
    with pytest.raises(DraftValidationError) as exc:
        validate_canonical_draft(normalized, schema)
    assert exc.value.code == "draft_canonical_validation_failed"


def test_unknown_property_behavior():
    """4. unknown property is preserved by normalization, 5. unknown property then fails canonical validation"""
    schema = {
        "type": "object",
        "properties": {
            "req": {"type": "string"}
        },
        "required": ["req"],
        "additionalProperties": False
    }
    provider_output = {
        "req": "x",
        "unknown_prop": "y"
    }
    normalized = normalize_draft_provider_output(provider_output, schema)
    assert normalized == {"req": "x", "unknown_prop": "y"}
    
    with pytest.raises(DraftValidationError) as exc:
        validate_canonical_draft(normalized, schema)
    assert exc.value.code == "draft_canonical_validation_failed"


def test_local_ref_normalization():
    """6. local $ref normalization"""
    schema = {
        "type": "object",
        "properties": {
            "nested": {"$ref": "#/$defs/Nested"}
        },
        "required": ["nested"],
        "$defs": {
            "Nested": {
                "type": "object",
                "properties": {
                    "opt": {"type": "string"}
                }
            }
        }
    }
    provider_output = {
        "nested": {
            "opt": None
        }
    }
    normalized = normalize_draft_provider_output(provider_output, schema)
    assert normalized == {"nested": {}}


def test_compositional_allof_structural_normalization():
    """7. compositional allOf structural normalization"""
    schema = {
        "type": "object",
        "properties": {
            "nested": {
                "allOf": [
                    {
                        "type": "object",
                        "properties": {"req": {"type": "string"}},
                        "required": ["req"]
                    },
                    {
                        "type": "object",
                        "properties": {"opt": {"type": "string"}}
                    }
                ]
            }
        },
        "required": ["nested"]
    }
    provider_output = {
        "nested": {
            "req": None,
            "opt": None
        }
    }
    normalized = normalize_draft_provider_output(provider_output, schema)
    assert normalized == {"nested": {"req": None}}


def test_conditional_allof_does_not_cause_unsafe_null_removal():
    """8. conditional allOf does not cause unsafe null removal"""
    schema = {
        "type": "object",
        "properties": {
            "val": {
                "allOf": [
                    {
                        "if": {"properties": {"type": {"const": "a"}}},
                        "then": {"required": ["cond_req"]}
                    }
                ],
                "properties": {
                    "type": {"type": "string"},
                    "cond_req": {"type": "string"}
                }
            }
        }
    }
    provider_output = {
        "val": {
            "type": "a",
            "cond_req": None
        }
    }
    normalized = normalize_draft_provider_output(provider_output, schema)
    # The conditional required is ignored by normalization, so it falls back to not unconditionally required
    # and therefore cond_req=None is removed.
    assert normalized == {"val": {"type": "a"}}


def test_normal_array_items_normalization():
    """9. normal array items normalization"""
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "opt": {"type": "string"}
            }
        }
    }
    provider_output = [{"opt": "x"}, {"opt": None}]
    normalized = normalize_draft_provider_output(provider_output, schema)
    assert normalized == [{"opt": "x"}, {}]


def test_prefixitems_positional_normalization():
    """10. prefixItems positional normalization"""
    schema = {
        "type": "array",
        "prefixItems": [
            {
                "type": "object",
                "properties": {"opt1": {"type": "string"}}
            },
            {
                "type": "object",
                "properties": {"opt2": {"type": "string"}}
            }
        ],
        "items": False
    }
    provider_output = [{"opt1": None}, {"opt2": None}, {"opt3": None}]
    normalized = normalize_draft_provider_output(provider_output, schema)
    assert normalized == [{}, {}, {"opt3": None}]


def test_actual_draft_sections_tuple_normalization():
    """11. actual draft_sections tuple normalization"""
    schema = _load_schema()
    # We use 'marker' which is an optional property in draft_section
    provider_output = {
        "draft_sections": [
            {"section_type": "technical_field", "marker": None},
            {"section_type": "background", "marker": None},
            {"section_type": "summary", "marker": None},
            {"section_type": "drawings", "marker": None},
            {"section_type": "detailed_description", "marker": None},
            {"section_type": "experimental", "marker": None},
        ]
    }
    normalized = normalize_draft_provider_output(provider_output, schema)
    assert "marker" not in normalized["draft_sections"][0]
    assert "marker" not in normalized["draft_sections"][4]


def test_specialized_subsection_tuple_normalization():
    """12. specialized subsection tuple normalization"""
    schema = _load_schema()
    # subsections has marker which is optional
    provider_output = {
        "draft_sections": [
            {"section_type": "technical_field", "paragraphs": []},
            {"section_type": "background", "paragraphs": []},
            {"section_type": "summary", "paragraphs": []},
            {"section_type": "drawings", "paragraphs": []},
            {
                "section_type": "detailed_description",
                "subsections": [
                    {
                        "heading": "Embodiments",
                        "marker": None
                    }
                ]
            },
            {"section_type": "experimental", "paragraphs": []}
        ]
    }
    normalized = normalize_draft_provider_output(provider_output, schema)
    assert "marker" not in normalized["draft_sections"][4]["subsections"][0]


def test_evidence_locator_normalization():
    """13. evidence_locator nullable optional fields normalize correctly"""
    schema = _load_schema()
    locator_output = {
        "page": 1,
        "section": None,
        "paragraph_id": None,
        "chunk_id": None,
        "table_id": None,
        "figure_id": None
    }
    container_schema = {
        "type": "object",
        "properties": {
            "locator": {"$ref": "#/$defs/evidence_locator"}
        },
        "$defs": schema["$defs"]
    }
    provider_output = {"locator": locator_output}
    normalized = normalize_draft_provider_output(provider_output, container_schema)
    assert normalized["locator"] == {"page": 1}


def test_input_mutation_safety():
    """14. input provider output not mutated, 15. canonical schema not mutated"""
    schema = {
        "type": "object",
        "properties": {
            "opt": {"type": "string"}
        }
    }
    provider_output = {"opt": None}
    
    schema_copy = copy.deepcopy(schema)
    output_copy = copy.deepcopy(provider_output)
    
    normalize_draft_provider_output(provider_output, schema)
    
    assert schema == schema_copy
    assert provider_output == output_copy


def test_valid_fixture_passes_validation():
    """16. valid canonical Patent Draft fixture passes validation"""
    schema = _load_schema()
    fixture = _load_valid_fixture()
    
    # We must first normalize it in case the fixture has optional nulls, though valid fixtures shouldn't.
    normalized = normalize_draft_provider_output(fixture, schema)
    validated = validate_canonical_draft(normalized, schema)
    
    assert validated == normalized


def test_invalid_fixture_fails_validation():
    """17. invalid canonical Draft fixture fails with: draft_canonical_validation_failed"""
    schema = _load_schema()
    fixture = _load_valid_fixture()
    
    # Mutate to make it invalid
    del fixture["section_order"]
    
    with pytest.raises(DraftValidationError) as exc:
        validate_canonical_draft(fixture, schema)
    assert exc.value.code == "draft_canonical_validation_failed"


def test_validation_paths_stable_and_safe():
    """18. validation paths are stable and content-safe"""
    schema = _load_schema()
    fixture = _load_valid_fixture()
    
    # Create deterministic errors at known paths
    fixture["draft_sections"][0]["sequence"] = "not an int"  # Expected int
    del fixture["draft_sections"][1]["paragraphs"]  # Required field missing

    with pytest.raises(DraftValidationError) as exc:
        validate_canonical_draft(fixture, schema)

    assert "/draft_sections/0/sequence" in exc.value.paths
    assert "/draft_sections/1" in exc.value.paths
    
    # Ensure it doesn't leak full objects or prompt contents
    for path in exc.value.paths:
        assert "{" not in path
        assert "}" not in path
        assert "\n" not in path


def test_non_dict_root_fails():
    """19. non-dict root fails canonical validation"""
    schema = {"type": "object"}
    with pytest.raises(DraftValidationError) as exc:
        validate_canonical_draft(["list", "not", "dict"], schema)
    assert exc.value.code == "draft_canonical_validation_failed"


def test_no_content_repair_occurs():
    """20. no content repair occurs"""
    schema = {
        "type": "object",
        "properties": {
            "req_int": {"type": "integer"}
        },
        "required": ["req_int"]
    }
    provider_output = {"req_int": "123"}  # String instead of int
    normalized = normalize_draft_provider_output(provider_output, schema)
    
    # It must not change "123" to 123
    assert normalized["req_int"] == "123"
    
    with pytest.raises(DraftValidationError) as exc:
        validate_canonical_draft(normalized, schema)
    assert exc.value.code == "draft_canonical_validation_failed"
