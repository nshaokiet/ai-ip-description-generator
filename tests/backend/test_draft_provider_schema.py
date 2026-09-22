"""Tests for Checkpoint B draft provider schema projection."""

import copy
import json
import pytest
from pathlib import Path

from backend.app.services.draft_provider_schema import (
    build_draft_provider_schema,
    DraftProviderSchemaError,
)

def test_canonical_schema_projects_successfully():
    """21. canonical patent draft schema projects successfully"""
    schema_path = Path(__file__).resolve().parents[2] / "schemas" / "patent-draft" / "v1.0.0" / "patent-draft.schema.json"
    with schema_path.open(encoding="utf-8") as f:
        canonical = json.load(f)
    
    canonical_copy = copy.deepcopy(canonical)
    
    # 2. deterministic projection
    provider1 = build_draft_provider_schema(canonical)
    provider2 = build_draft_provider_schema(canonical)
    assert json.dumps(provider1, sort_keys=True) == json.dumps(provider2, sort_keys=True)
    
    # 1. canonical schema non-mutation
    assert canonical == canonical_copy

    # 3. recursively verify projected schema
    def walk_verify(node):
        if isinstance(node, list):
            for item in node:
                walk_verify(item)
            return
        if not isinstance(node, dict):
            return

        unsupported = {"if", "then", "else", "not", "contains", "prefixItems", "uniqueItems", "oneOf", "allOf"}
        assert not unsupported.intersection(node), f"Found unsupported keywords in node: {node}"
        if "items" in node:
            assert node["items"] is not False

        if "properties" in node:
            assert node.get("type") == "object"
            assert node.get("additionalProperties") is False
            assert set(node.get("required", [])) == set(node["properties"])

        for value in node.values():
            walk_verify(value)

    walk_verify(provider1)

    draft_sections = provider1["properties"]["draft_sections"]
    assert draft_sections["minItems"] == 6
    assert draft_sections["maxItems"] == 6
    assert "prefixItems" not in draft_sections
    assert draft_sections["items"] is not False
    assert "anyOf" in draft_sections["items"]

    section_order = provider1["properties"]["section_order"]
    assert section_order["type"] == "array"
    assert section_order["minItems"] == 11
    assert section_order["maxItems"] == 11
    assert "enum" in section_order["items"]
    assert "COVER_AND_DRAFT_NOTICE" in section_order["items"]["enum"]

    evidence_locator = provider1["$defs"]["evidence_locator"]
    assert "anyOf" not in evidence_locator
    assert "page" in evidence_locator["properties"]
    assert evidence_locator["properties"]["page"]["type"] == ["integer", "null"]
    assert "page" in evidence_locator["required"]


def test_optional_becomes_nullable_required_and_required_is_not_nullable():
    """3. all provider object properties required, 4. optional nullable, 5. required strict"""
    canonical = {
        "type": "object",
        "properties": {
            "req": {"type": "string"},
            "opt": {"type": "string"}
        },
        "required": ["req"]
    }
    provider = build_draft_provider_schema(canonical)
    assert provider["type"] == "object"
    assert provider["additionalProperties"] is False
    assert set(provider["required"]) == {"req", "opt"}
    assert provider["properties"]["req"] == {"type": "string"}
    assert provider["properties"]["opt"] == {"type": ["string", "null"]}

def test_local_ref_behavior():
    """6. local $ref behavior"""
    canonical = {
        "type": "object",
        "properties": {
            "nested": {"$ref": "#/$defs/target"}
        },
        "$defs": {
            "target": {"type": "string"}
        },
        "required": ["nested"]
    }
    provider = build_draft_provider_schema(canonical)
    assert provider["properties"]["nested"] == {"$ref": "#/$defs/target"}

def test_local_ref_fail_closed():
    """F-B01: unresolved local refs and external refs fail closed"""
    canonical_unresolved = {
        "type": "object",
        "properties": {
            "val": {"$ref": "#/$defs/missing"}
        },
        "required": ["val"]
    }
    with pytest.raises(DraftProviderSchemaError, match="unresolvable reference"):
        build_draft_provider_schema(canonical_unresolved)

    canonical_external = {
        "type": "object",
        "properties": {
            "val": {"$ref": "http://example.com/schema.json"}
        },
        "required": ["val"]
    }
    with pytest.raises(DraftProviderSchemaError, match="only local JSON Pointer references are supported"):
        build_draft_provider_schema(canonical_external)

def test_compositional_allof_compatible_merge():
    """7. compositional allOf compatible merge"""
    canonical = {
        "type": "object",
        "properties": {
            "val": {
                "allOf": [
                    {"type": "integer"},
                    {"minimum": 5}
                ]
            }
        },
        "required": ["val"]
    }
    provider = build_draft_provider_schema(canonical)
    assert provider["properties"]["val"] == {"type": "integer", "minimum": 5}

def test_incompatible_allof_fails_closed():
    """8. incompatible allOf fails closed"""
    canonical = {
        "type": "object",
        "properties": {
            "val": {
                "allOf": [
                    {"type": "integer"},
                    {"type": "string"}
                ]
            }
        },
        "required": ["val"]
    }
    with pytest.raises(DraftProviderSchemaError, match="unsafe allOf conflict for type"):
        build_draft_provider_schema(canonical)

def test_enum_intersections():
    """9. enum intersection, 10. enum+const, 11. incompatible const"""
    canonical1 = {
        "type": "object",
        "properties": {
            "val": {
                "allOf": [
                    {"enum": ["a", "b", "c"]},
                    {"enum": ["b", "c", "d"]}
                ]
            }
        },
        "required": ["val"]
    }
    p1 = build_draft_provider_schema(canonical1)
    assert set(p1["properties"]["val"]["enum"]) == {"b", "c"}

    canonical2 = {
        "type": "object",
        "properties": {
            "val": {
                "allOf": [
                    {"enum": ["a", "b", "c"]},
                    {"const": "b"}
                ]
            }
        },
        "required": ["val"]
    }
    p2 = build_draft_provider_schema(canonical2)
    assert p2["properties"]["val"]["const"] == "b"
    assert "enum" not in p2["properties"]["val"]

    canonical3 = {
        "type": "object",
        "properties": {
            "val": {
                "allOf": [
                    {"const": "a"},
                    {"const": "b"}
                ]
            }
        },
        "required": ["val"]
    }
    with pytest.raises(DraftProviderSchemaError, match="unsafe allOf conflict for const"):
        build_draft_provider_schema(canonical3)

def test_min_max_intersections_and_impossible_ranges():
    """12. min/max intersection, 13. impossible range fails"""
    canonical = {
        "type": "object",
        "properties": {
            "val": {
                "allOf": [
                    {"minimum": 5, "maximum": 20},
                    {"minimum": 10, "maximum": 15}
                ]
            }
        },
        "required": ["val"]
    }
    p = build_draft_provider_schema(canonical)
    assert p["properties"]["val"]["minimum"] == 10
    assert p["properties"]["val"]["maximum"] == 15

    canonical2 = {
        "type": "object",
        "properties": {
            "val": {
                "allOf": [
                    {"minimum": 20},
                    {"maximum": 10}
                ]
            }
        },
        "required": ["val"]
    }
    with pytest.raises(DraftProviderSchemaError, match="impossible range for minimum/maximum"):
        build_draft_provider_schema(canonical2)

def test_conditional_allof_deferred():
    """14. conditional allOf deferred, 15. no if/then/not leakage"""
    canonical = {
        "type": "object",
        "properties": {
            "val": {
                "type": "string",
                "allOf": [
                    {"if": {"minLength": 2}, "then": {"maxLength": 5}}
                ]
            }
        },
        "required": ["val"]
    }
    p = build_draft_provider_schema(canonical)
    # The conditional allOf should be completely deferred, leaving just the base
    assert p["properties"]["val"] == {"type": "string"}
    assert "allOf" not in p["properties"]["val"]

def test_unsupported_keywords_rejected_in_assertion():
    """16. no contains leakage, 22. assertion rejects unsupported"""
    canonical = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "val": {
                "type": "array",
                "contains": {"type": "string"}
            }
        },
        "required": ["val"]
    }
    p = build_draft_provider_schema(canonical)
    assert "contains" not in p["properties"]["val"]
    
    from backend.app.services.draft_provider_schema import _assert_provider_schema
    with pytest.raises(DraftProviderSchemaError, match="unsupported keywords \\['contains'\\]"):
        _assert_provider_schema(canonical)

def test_unique_items_omitted():
    """17. uniqueItems omitted provider-side"""
    canonical = {
        "type": "object",
        "properties": {
            "val": {
                "type": "array",
                "uniqueItems": True,
                "items": {"type": "string"}
            }
        },
        "required": ["val"]
    }
    p = build_draft_provider_schema(canonical)
    assert "uniqueItems" not in p["properties"]["val"]

def test_prefix_items_tuple_projection():
    """18. prefixItems/items:false tuple projection"""
    canonical = {
        "type": "object",
        "properties": {
            "val": {
                "type": "array",
                "minItems": 2,
                "maxItems": 2,
                "prefixItems": [
                    {"type": "string"},
                    {"type": "integer"}
                ],
                "items": False
            }
        },
        "required": ["val"]
    }
    p = build_draft_provider_schema(canonical)
    assert "prefixItems" not in p["properties"]["val"]
    assert p["properties"]["val"]["items"] == {
        "anyOf": [{"type": "string"}, {"type": "integer"}]
    }
    assert p["properties"]["val"]["minItems"] == 2
    assert p["properties"]["val"]["maxItems"] == 2

def test_array_valued_const_conservative_projection():
    """19. array-valued const conservative projection"""
    canonical = {
        "type": "object",
        "properties": {
            "val": {
                "const": ["a", "b", "c"]
            }
        },
        "required": ["val"]
    }
    p = build_draft_provider_schema(canonical)
    assert p["properties"]["val"]["type"] == "array"
    assert p["properties"]["val"]["minItems"] == 3
    assert p["properties"]["val"]["maxItems"] == 3
    assert p["properties"]["val"]["items"] == {"enum": ["a", "b", "c"]}

def test_evidence_locator_presence_constraint():
    """20. evidence_locator presence constraint treatment"""
    canonical = {
        "type": "object",
        "properties": {
            "page": {"type": "integer"}
        },
        "anyOf": [
            {"required": ["page"]}
        ]
    }
    p = build_draft_provider_schema(canonical)
    # Optional properties become nullable and strictly required by provider schema rules
    assert p["type"] == "object"
    assert set(p["required"]) == {"page"}
    assert p["properties"]["page"]["type"] == ["integer", "null"]
    # anyOf presence constraint is preserved but optional properties were resolved safely
    assert "anyOf" not in p

def test_oneof_fails_closed():
    """F-B02: oneOf must fail closed"""
    canonical = {
        "type": "object",
        "properties": {
            "val": {
                "oneOf": [{"type": "string"}, {"type": "integer"}]
            }
        },
        "required": ["val"]
    }
    with pytest.raises(DraftProviderSchemaError, match="unsupported oneOf"):
        build_draft_provider_schema(canonical)
