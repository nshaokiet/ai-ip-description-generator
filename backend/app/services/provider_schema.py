"""Deterministic OpenAI Structured Outputs adapter for AI-001 schema v1.0.0."""

from __future__ import annotations

import copy
import json
from collections.abc import Mapping
from typing import Any


PROVIDER_SCHEMA_NAME = "invention_output_v1_0_0"
_UNSUPPORTED_KEYWORDS = {"allOf", "oneOf", "uniqueItems", "if", "then", "else", "not"}


class ProviderSchemaError(ValueError):
    """Raised when a canonical schema cannot be adapted without unsafe weakening."""


def build_provider_schema(canonical_schema: Mapping[str, Any]) -> dict[str, Any]:
    """Return a strict provider schema without mutating the canonical input."""

    original = copy.deepcopy(dict(canonical_schema))
    provider_schema = _transform_node(original, original, ())
    if original != canonical_schema:
        raise ProviderSchemaError("canonical schema was mutated during provider adaptation")
    _assert_provider_schema(provider_schema)
    return provider_schema


def provider_schema_fingerprint(schema: Mapping[str, Any]) -> str:
    """Return a stable serialization useful for deterministic comparison and review."""

    return json.dumps(schema, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def _transform_node(
    node: Any,
    root: Mapping[str, Any],
    path: tuple[str, ...],
) -> Any:
    if isinstance(node, list):
        return [_transform_node(item, root, path + (str(index),)) for index, item in enumerate(node)]
    if not isinstance(node, dict):
        return copy.deepcopy(node)

    if "allOf" in node:
        compositions = node["allOf"]
        if not isinstance(compositions, list) or not compositions:
            raise ProviderSchemaError(f"invalid allOf at {_display_path(path)}")
        base = {key: value for key, value in node.items() if key != "allOf"}
        if any(_contains_conditional_keyword(item) for item in compositions):
            return _transform_node(base, root, path)
        merged = copy.deepcopy(base)
        for index, item in enumerate(compositions):
            resolved = _resolve_schema(item, root, set())
            merged = _merge_schema(merged, resolved, path + ("allOf", str(index)))
        return _transform_node(merged, root, path)

    for keyword in ("if", "then", "else", "not"):
        if keyword in node:
            raise ProviderSchemaError(
                f"unsupported standalone {keyword} at {_display_path(path)}"
            )

    transformed: dict[str, Any] = {}
    for key, value in node.items():
        if key in {"$schema", "$id", "uniqueItems"}:
            continue
        if key == "oneOf":
            if "anyOf" in node:
                raise ProviderSchemaError(f"combined oneOf/anyOf at {_display_path(path)}")
            transformed["anyOf"] = _transform_node(value, root, path + ("anyOf",))
            continue
        if key == "anyOf" and _is_presence_constraint(value):
            if path[-2:] != ("$defs", "evidence_locator"):
                raise ProviderSchemaError(
                    f"unsupported presence anyOf at {_display_path(path)}"
                )
            continue
        transformed[key] = _transform_node(value, root, path + (key,))

    properties = node.get("properties")
    if isinstance(properties, dict):
        canonical_required = set(node.get("required", []))
        provider_properties: dict[str, Any] = {}
        for property_name, property_schema in properties.items():
            adapted = _transform_node(
                property_schema,
                root,
                path + ("properties", property_name),
            )
            if property_name not in canonical_required:
                adapted = _make_nullable(adapted)
            provider_properties[property_name] = adapted
        transformed["type"] = "object"
        transformed["properties"] = provider_properties
        transformed["additionalProperties"] = False
        transformed["required"] = list(properties)

    return transformed


def _resolve_schema(
    schema: Any,
    root: Mapping[str, Any],
    seen_refs: set[str],
) -> dict[str, Any]:
    if not isinstance(schema, dict):
        raise ProviderSchemaError("allOf member must be a schema object")
    if "$ref" not in schema:
        return copy.deepcopy(schema)
    reference = schema["$ref"]
    if not isinstance(reference, str) or not reference.startswith("#/"):
        raise ProviderSchemaError("only local JSON Pointer references are supported")
    if reference in seen_refs:
        raise ProviderSchemaError(f"cyclic reference cannot be flattened: {reference}")
    target: Any = root
    for token in reference[2:].split("/"):
        decoded = token.replace("~1", "/").replace("~0", "~")
        if not isinstance(target, Mapping) or decoded not in target:
            raise ProviderSchemaError(f"unresolvable reference: {reference}")
        target = target[decoded]
    resolved = _resolve_schema(target, root, seen_refs | {reference})
    siblings = {key: value for key, value in schema.items() if key != "$ref"}
    return _merge_schema(resolved, siblings, ("$ref", reference))


def _merge_schema(
    left: Mapping[str, Any],
    right: Mapping[str, Any],
    path: tuple[str, ...],
) -> dict[str, Any]:
    merged = copy.deepcopy(dict(left))
    for key, value in right.items():
        if key not in merged:
            merged[key] = copy.deepcopy(value)
        elif merged[key] == value:
            continue
        elif key == "required" and isinstance(merged[key], list) and isinstance(value, list):
            merged[key] = list(dict.fromkeys([*merged[key], *value]))
        elif key == "properties" and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = _merge_schema(merged[key], value, path + (key,))
        else:
            raise ProviderSchemaError(
                f"unsafe allOf conflict for {key} at {_display_path(path)}"
            )
    return merged


def _make_nullable(schema: dict[str, Any]) -> dict[str, Any]:
    nullable = copy.deepcopy(schema)
    schema_type = nullable.get("type")
    if isinstance(schema_type, str):
        nullable["type"] = [schema_type, "null"]
        return nullable
    if isinstance(schema_type, list):
        if "null" not in schema_type:
            nullable["type"] = [*schema_type, "null"]
        return nullable
    if "anyOf" in nullable and isinstance(nullable["anyOf"], list):
        if not any(branch == {"type": "null"} for branch in nullable["anyOf"]):
            nullable["anyOf"].append({"type": "null"})
        return nullable
    return {"anyOf": [nullable, {"type": "null"}]}


def _contains_conditional_keyword(node: Any) -> bool:
    if isinstance(node, dict):
        if any(keyword in node for keyword in ("if", "then", "else", "not")):
            return True
        return any(_contains_conditional_keyword(value) for value in node.values())
    if isinstance(node, list):
        return any(_contains_conditional_keyword(item) for item in node)
    return False


def _is_presence_constraint(branches: Any) -> bool:
    if not isinstance(branches, list) or not branches:
        return False
    return all(
        isinstance(branch, dict)
        and set(branch) == {"required"}
        and isinstance(branch["required"], list)
        for branch in branches
    )


def _assert_provider_schema(schema: Mapping[str, Any]) -> None:
    if schema.get("type") != "object":
        raise ProviderSchemaError("provider schema root must be an object")
    if "anyOf" in schema:
        raise ProviderSchemaError("provider schema root must not contain anyOf")

    def visit(node: Any, path: tuple[str, ...]) -> None:
        if isinstance(node, list):
            for index, item in enumerate(node):
                visit(item, path + (str(index),))
            return
        if not isinstance(node, dict):
            return
        unsupported = _UNSUPPORTED_KEYWORDS.intersection(node)
        if unsupported:
            raise ProviderSchemaError(
                f"unsupported keywords {sorted(unsupported)} at {_display_path(path)}"
            )
        properties = node.get("properties")
        if isinstance(properties, dict):
            if node.get("type") != "object":
                raise ProviderSchemaError(f"object type missing at {_display_path(path)}")
            if node.get("additionalProperties") is not False:
                raise ProviderSchemaError(
                    f"additionalProperties must be false at {_display_path(path)}"
                )
            required = node.get("required")
            if not isinstance(required, list) or set(required) != set(properties):
                raise ProviderSchemaError(
                    f"all provider object properties must be required at {_display_path(path)}"
                )
        for key, value in node.items():
            visit(value, path + (key,))

    visit(schema, ())


def _display_path(path: tuple[str, ...]) -> str:
    return "/" + "/".join(path) if path else "/"
