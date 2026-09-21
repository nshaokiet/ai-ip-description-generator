from __future__ import annotations

import copy
import unittest

from backend.app.services.provider_schema import (
    PROVIDER_SCHEMA_NAME,
    ProviderSchemaError,
    build_provider_schema,
    provider_schema_fingerprint,
)
from tests.backend.runtime_test_support import CANONICAL_SCHEMA, load_json


class ProviderSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.canonical = load_json(CANONICAL_SCHEMA)

    def setUp(self) -> None:
        self.provider = build_provider_schema(self.canonical)

    def test_actual_canonical_schema_transforms(self) -> None:
        self.assertEqual("object", self.provider["type"])
        self.assertEqual(PROVIDER_SCHEMA_NAME, "invention_output_v1_0_0")

    def test_transformation_is_deterministic(self) -> None:
        second = build_provider_schema(self.canonical)
        self.assertEqual(provider_schema_fingerprint(self.provider), provider_schema_fingerprint(second))

    def test_canonical_schema_is_not_mutated(self) -> None:
        original = copy.deepcopy(self.canonical)
        build_provider_schema(self.canonical)
        self.assertEqual(original, self.canonical)

    def test_every_object_is_closed_and_all_properties_are_required(self) -> None:
        def visit(node):
            if isinstance(node, list):
                for item in node:
                    visit(item)
            elif isinstance(node, dict):
                if "properties" in node:
                    self.assertEqual("object", node.get("type"))
                    self.assertIs(False, node.get("additionalProperties"))
                    self.assertEqual(set(node["properties"]), set(node.get("required", [])))
                for item in node.values():
                    visit(item)

        visit(self.provider)

    def test_optional_string_becomes_required_nullable(self) -> None:
        metadata = self.provider["$defs"]["document_metadata"]
        self.assertIn("sha256", metadata["required"])
        self.assertEqual(
            [{"$ref": "#/$defs/non_empty_text"}, {"type": "null"}],
            self.provider["$defs"]["technical_field_item"]["properties"]["description"]["anyOf"],
        )

    def test_optional_ref_becomes_nested_nullable_anyof(self) -> None:
        item = self.provider["$defs"]["technical_field"]["properties"]["item"]
        self.assertEqual(
            [{"$ref": "#/$defs/technical_field_item"}, {"type": "null"}],
            item["anyOf"],
        )

    def test_conditional_allof_is_deferred_but_base_schema_remains(self) -> None:
        technical_field = self.provider["$defs"]["technical_field"]
        self.assertNotIn("allOf", technical_field)
        self.assertEqual({"status", "item"}, set(technical_field["properties"]))
        drawing = self.provider["$defs"]["drawing_requirement"]
        self.assertNotIn("allOf", drawing)
        self.assertIn("source_evidence_ids", drawing["properties"])

    def test_compositional_allof_is_flattened_without_losing_array_constraints(self) -> None:
        addresses = self.provider["$defs"]["technical_solution"]["properties"][
            "addresses_problem_ids"
        ]
        self.assertEqual("array", addresses["type"])
        self.assertEqual(1, addresses["minItems"])
        self.assertEqual({"$ref": "#/$defs/identifier"}, addresses["items"])
        self.assertNotIn("allOf", addresses)

    def test_scalar_oneof_becomes_nested_anyof(self) -> None:
        scalar = self.provider["$defs"]["scalar_value"]
        self.assertNotIn("oneOf", scalar)
        self.assertEqual(3, len(scalar["anyOf"]))
        self.assertEqual({"type": "number"}, scalar["anyOf"][1])

    def test_evidence_locator_uses_required_nullable_properties(self) -> None:
        locator = self.provider["$defs"]["evidence_locator"]
        self.assertNotIn("anyOf", locator)
        self.assertEqual(set(locator["properties"]), set(locator["required"]))
        self.assertEqual(["integer", "null"], locator["properties"]["page"]["type"])
        self.assertEqual(
            [{"$ref": "#/$defs/identifier"}, {"type": "null"}],
            locator["properties"]["chunk_id"]["anyOf"],
        )

    def test_uniqueitems_is_deferred_and_canonical_retains_it(self) -> None:
        self.assertTrue(self.canonical["properties"]["evidence"]["uniqueItems"])

        def assert_absent(node):
            if isinstance(node, dict):
                self.assertNotIn("uniqueItems", node)
                for value in node.values():
                    assert_absent(value)
            elif isinstance(node, list):
                for value in node:
                    assert_absent(value)

        assert_absent(self.provider)

    def test_identifier_pattern_is_preserved(self) -> None:
        self.assertEqual(
            self.canonical["$defs"]["identifier"]["pattern"],
            self.provider["$defs"]["identifier"]["pattern"],
        )

    def test_numeric_minimum_is_preserved(self) -> None:
        sequence = self.provider["$defs"]["process_step"]["properties"]["sequence"]
        self.assertEqual(1, sequence["minimum"])

    def test_array_minimum_is_preserved(self) -> None:
        results = self.provider["$defs"]["experiment"]["properties"]["results"]
        self.assertEqual(1, results["minItems"])

    def test_root_anyof_is_never_generated(self) -> None:
        self.assertNotIn("anyOf", self.provider)

    def test_no_unsupported_composition_remains(self) -> None:
        unsupported = {"allOf", "oneOf", "uniqueItems", "if", "then", "else", "not"}

        def visit(node):
            if isinstance(node, dict):
                self.assertFalse(unsupported.intersection(node))
                for value in node.values():
                    visit(value)
            elif isinstance(node, list):
                for value in node:
                    visit(value)

        visit(self.provider)

    def test_unmergeable_allof_fails_safely(self) -> None:
        unsafe = {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "value": {
                    "allOf": [{"type": "string"}, {"type": "integer"}]
                }
            },
            "required": ["value"],
        }
        with self.assertRaises(ProviderSchemaError):
            build_provider_schema(unsafe)

    def test_standalone_not_fails_safely(self) -> None:
        unsafe = {
            "type": "object",
            "additionalProperties": False,
            "properties": {"value": {"not": {"type": "string"}}},
            "required": ["value"],
        }
        with self.assertRaises(ProviderSchemaError):
            build_provider_schema(unsafe)

    def test_unapproved_presence_anyof_fails_instead_of_weakening_silently(self) -> None:
        unsafe = {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "choice": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {"a": {"type": "string"}, "b": {"type": "string"}},
                    "anyOf": [{"required": ["a"]}, {"required": ["b"]}],
                }
            },
            "required": ["choice"],
        }
        with self.assertRaises(ProviderSchemaError):
            build_provider_schema(unsafe)


if __name__ == "__main__":
    unittest.main()
