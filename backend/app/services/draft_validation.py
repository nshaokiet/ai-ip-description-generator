"""Canonical validation and normalization for AI-RUNTIME-002 Draft schema."""

from __future__ import annotations

import copy
from collections.abc import Iterable, Mapping
from typing import Any

from jsonschema import Draft202012Validator


class DraftValidationError(ValueError):
    """A fail-closed validation result with content-safe diagnostics for drafts."""

    def __init__(self, code: str, message: str, *, paths: Iterable[str] = ()) -> None:
        super().__init__(message)
        self.code = code
        self.safe_message = message
        self.paths = tuple(paths)


def normalize_draft_provider_output(
    provider_output: Any,
    canonical_schema: Mapping[str, Any],
) -> Any:
    """Remove only nulls that represent canonically optional properties."""
    return _normalize(copy.deepcopy(provider_output), canonical_schema, canonical_schema)


def validate_canonical_draft(
    draft: Any,
    canonical_schema: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate with the canonical Draft 2020-12 schema and fail closed."""
    Draft202012Validator.check_schema(canonical_schema)
    validator = Draft202012Validator(canonical_schema)
    errors = sorted(
        validator.iter_errors(draft),
        key=lambda error: (list(error.absolute_path), list(error.absolute_schema_path)),
    )
    if errors:
        paths = (_json_path(error.absolute_path) for error in errors[:10])
        raise DraftValidationError(
            code="draft_canonical_validation_failed",
            message="The model output did not satisfy the canonical draft contract.",
            paths=paths,
        )
    if not isinstance(draft, dict):
        raise DraftValidationError(
            code="draft_canonical_validation_failed",
            message="The model output did not satisfy the canonical draft contract.",
        )
    return draft


def _normalize(value: Any, schema: Any, root: Mapping[str, Any]) -> Any:
    effective = _effective_schema(schema, root)
    if isinstance(value, dict):
        properties = effective.get("properties", {})
        required = set(effective.get("required", []))
        normalized: dict[str, Any] = {}
        for key, item in value.items():
            property_schema = properties.get(key)
            if item is None and property_schema is not None and key not in required:
                continue
            normalized[key] = (
                _normalize(item, property_schema, root)
                if property_schema is not None
                else copy.deepcopy(item)
            )
        return normalized
    if isinstance(value, list):
        prefix_items = effective.get("prefixItems", [])
        items_schema = effective.get("items")
        normalized_list = []
        for index, item in enumerate(value):
            if index < len(prefix_items):
                item_schema = prefix_items[index]
                normalized_list.append(_normalize(item, item_schema, root))
            else:
                if isinstance(items_schema, dict):
                    normalized_list.append(_normalize(item, items_schema, root))
                else:
                    normalized_list.append(copy.deepcopy(item))
        return normalized_list
    return copy.deepcopy(value)


def _effective_schema(schema: Any, root: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(schema, dict):
        return {}
    effective = copy.deepcopy(schema)
    if "$ref" in effective:
        reference = effective.pop("$ref")
        target = _resolve_reference(reference, root)
        resolved = copy.deepcopy(target)
        resolved.update(effective)
        effective = resolved
    compositions = effective.pop("allOf", [])
    for composition in compositions:
        if _contains_conditional(composition):
            continue
        part = _effective_schema(composition, root)
        for key, value in part.items():
            if key not in effective:
                effective[key] = value
            elif key == "required" and isinstance(value, list):
                effective[key] = list(dict.fromkeys([*effective.get("required", []), *value]))
            elif key == "properties" and isinstance(value, dict):
                effective["properties"].update(value)
            elif key == "prefixItems" and isinstance(value, list):
                effective["prefixItems"] = value
            elif key == "items":
                effective["items"] = value
    return effective


def _resolve_reference(reference: str, root: Mapping[str, Any]) -> dict[str, Any]:
    if not reference.startswith("#/"):
        raise DraftValidationError(
            code="draft_canonical_validation_failed",
            message=f"unresolvable reference: {reference}"
        )
    target: Any = root
    for token in reference[2:].split("/"):
        decoded = token.replace("~1", "/").replace("~0", "~")
        if not isinstance(target, Mapping) or decoded not in target:
            raise DraftValidationError(
                code="draft_canonical_validation_failed",
                message=f"unresolvable reference: {reference}"
            )
        target = target[decoded]
    if not isinstance(target, dict):
        raise DraftValidationError(
            code="draft_canonical_validation_failed",
            message=f"unresolvable reference: {reference}"
        )
    return target


def _contains_conditional(node: Any) -> bool:
    if isinstance(node, dict):
        return any(key in node for key in ("if", "then", "else", "not", "contains")) or any(
            _contains_conditional(value) for value in node.values()
        )
    if isinstance(node, list):
        return any(_contains_conditional(item) for item in node)
    return False


def _json_path(path: Iterable[Any]) -> str:
    tokens = [str(token).replace("~", "~0").replace("/", "~1") for token in path]
    return "/" + "/".join(tokens) if tokens else "/"
