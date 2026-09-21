"""Canonical and deterministic business validation for extraction output."""

from __future__ import annotations

import copy
from collections.abc import Iterable, Mapping
from typing import Any

from jsonschema import Draft202012Validator

from backend.app.schemas.analysis_input import ExtractionInputEnvelope


class ExtractionValidationError(ValueError):
    """A fail-closed validation result with content-safe diagnostics."""

    def __init__(self, code: str, message: str, *, paths: Iterable[str] = ()) -> None:
        super().__init__(message)
        self.code = code
        self.safe_message = message
        self.paths = tuple(paths)


def normalize_provider_output(
    provider_output: Any,
    canonical_schema: Mapping[str, Any],
) -> Any:
    """Remove only nulls that represent canonically optional properties."""

    return _normalize(copy.deepcopy(provider_output), canonical_schema, canonical_schema)


def validate_canonical_output(
    analysis: Any,
    canonical_schema: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate with the canonical Draft 2020-12 schema and fail closed."""

    Draft202012Validator.check_schema(canonical_schema)
    validator = Draft202012Validator(canonical_schema)
    errors = sorted(
        validator.iter_errors(analysis),
        key=lambda error: (list(error.absolute_path), list(error.absolute_schema_path)),
    )
    if errors:
        paths = (_json_path(error.absolute_path) for error in errors[:10])
        raise ExtractionValidationError(
            "canonical_validation_failed",
            "The model output did not satisfy the canonical analysis contract.",
            paths=paths,
        )
    if not isinstance(analysis, dict):
        raise ExtractionValidationError(
            "canonical_validation_failed",
            "The model output did not satisfy the canonical analysis contract.",
        )
    return analysis


def validate_grounding_and_business_rules(
    analysis: Mapping[str, Any],
    envelope: ExtractionInputEnvelope,
) -> None:
    """Validate provenance, exact excerpts, logical IDs, and cross-references."""

    failures: list[str] = []
    input_metadata = envelope.document_metadata.model_dump(exclude_none=True)
    output_metadata = analysis["document_metadata"]
    for field in ("document_id", "file_name", "media_type"):
        if output_metadata.get(field) != input_metadata[field]:
            failures.append(f"/document_metadata/{field}")
    if (
        "sha256" in output_metadata
        and output_metadata["sha256"] != input_metadata.get("sha256")
    ):
        failures.append("/document_metadata/sha256")

    source_units = {unit.evidence_id: unit for unit in envelope.source_units}
    output_evidence: dict[str, Mapping[str, Any]] = {}
    for index, evidence in enumerate(analysis["evidence"]):
        path = f"/evidence/{index}"
        evidence_id = evidence["evidence_id"]
        source = source_units.get(evidence_id)
        if source is None:
            failures.append(f"{path}/evidence_id")
            continue
        if evidence_id in output_evidence:
            failures.append(f"{path}/evidence_id")
        output_evidence[evidence_id] = evidence
        if evidence["document_id"] != input_metadata["document_id"]:
            failures.append(f"{path}/document_id")
        if evidence["evidence_type"] != source.evidence_type:
            failures.append(f"{path}/evidence_type")
        if evidence["locator"] != source.locator.model_dump(exclude_none=True):
            failures.append(f"{path}/locator")
        if evidence["excerpt"] not in source.content:
            failures.append(f"{path}/excerpt")

    emitted_evidence_ids = set(output_evidence)
    input_evidence_ids = set(source_units)
    for path, grounding in _iter_grounding_objects(analysis):
        for index, evidence_id in enumerate(grounding.get("evidence_ids", [])):
            reference_path = f"{path}/evidence_ids/{index}"
            if evidence_id not in input_evidence_ids or evidence_id not in emitted_evidence_ids:
                failures.append(reference_path)

    logical_ids = _collect_and_check_logical_ids(analysis, failures)
    _check_references(
        analysis,
        logical_ids,
        input_evidence_ids,
        emitted_evidence_ids,
        failures,
    )

    if failures:
        raise ExtractionValidationError(
            "grounding_validation_failed",
            "The model output failed deterministic grounding or reference validation.",
            paths=sorted(set(failures)),
        )


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
        item_schema = effective.get("items")
        if item_schema is None:
            return copy.deepcopy(value)
        return [_normalize(item, item_schema, root) for item in value]
    return copy.deepcopy(value)


def _effective_schema(schema: Any, root: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(schema, dict):
        return {}
    effective = copy.deepcopy(schema)
    if "$ref" in effective:
        target = _resolve_reference(effective.pop("$ref"), root)
        target.update(effective)
        effective = target
    compositions = effective.pop("allOf", [])
    for composition in compositions:
        if _contains_conditional(composition):
            continue
        part = _effective_schema(composition, root)
        for key, value in part.items():
            if key not in effective:
                effective[key] = value
            elif key == "required" and isinstance(value, list):
                effective[key] = list(dict.fromkeys([*effective[key], *value]))
            elif effective[key] != value:
                # Normalization needs structural metadata only; canonical validation
                # remains authoritative for incompatible constraint combinations.
                continue
    return effective


def _resolve_reference(reference: str, root: Mapping[str, Any]) -> dict[str, Any]:
    if not reference.startswith("#/"):
        return {}
    target: Any = root
    for token in reference[2:].split("/"):
        decoded = token.replace("~1", "/").replace("~0", "~")
        if not isinstance(target, Mapping) or decoded not in target:
            return {}
        target = target[decoded]
    return copy.deepcopy(target) if isinstance(target, dict) else {}


def _contains_conditional(node: Any) -> bool:
    if isinstance(node, dict):
        return any(key in node for key in ("if", "then", "else", "not")) or any(
            _contains_conditional(value) for value in node.values()
        )
    if isinstance(node, list):
        return any(_contains_conditional(item) for item in node)
    return False


def _iter_grounding_objects(value: Any, path: str = ""):
    if isinstance(value, dict):
        for key, item in value.items():
            child_path = f"{path}/{key}"
            if key == "grounding" and isinstance(item, dict):
                yield child_path, item
            yield from _iter_grounding_objects(item, child_path)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from _iter_grounding_objects(item, f"{path}/{index}")


def _collect_and_check_logical_ids(
    analysis: Mapping[str, Any],
    failures: list[str],
) -> dict[str, set[str]]:
    collection_specs = {
        "title_candidates": "title_id",
        "background": "statement_id",
        "technical_problems": "problem_id",
        "technical_solutions": "solution_id",
        "components": "component_id",
        "process_steps": "step_id",
        "potential_distinguishing_features": "feature_id",
        "technical_effects": "effect_id",
        "embodiments": "embodiment_id",
        "experimental_data": "experiment_id",
        "drawing_requirements": "drawing_id",
        "missing_information": "missing_id",
        "author_questions": "question_id",
    }
    identifiers: dict[str, set[str]] = {}
    globally_seen: set[str] = set()
    for collection, id_field in collection_specs.items():
        values: set[str] = set()
        for index, item in enumerate(analysis[collection]):
            identifier = item[id_field]
            if identifier in values or identifier in globally_seen:
                failures.append(f"/{collection}/{index}/{id_field}")
            values.add(identifier)
            globally_seen.add(identifier)
        identifiers[collection] = values

    technical_item = analysis["technical_field"].get("item")
    if technical_item is not None:
        field_id = technical_item["field_id"]
        if field_id in globally_seen:
            failures.append("/technical_field/item/field_id")
        globally_seen.add(field_id)

    for collection in ("process_steps", "technical_effects"):
        for parent_index, parent in enumerate(analysis[collection]):
            for condition_index, condition in enumerate(parent["conditions"]):
                statement_id = condition["statement_id"]
                if statement_id in globally_seen:
                    failures.append(
                        f"/{collection}/{parent_index}/conditions/{condition_index}/statement_id"
                    )
                globally_seen.add(statement_id)
    return identifiers


def _check_references(
    analysis: Mapping[str, Any],
    identifiers: Mapping[str, set[str]],
    input_evidence_ids: set[str],
    emitted_evidence_ids: set[str],
    failures: list[str],
) -> None:
    rules = (
        ("technical_solutions", "addresses_problem_ids", "technical_problems"),
        ("components", "related_component_ids", "components"),
        ("process_steps", "input_component_ids", "components"),
        ("process_steps", "output_component_ids", "components"),
        ("potential_distinguishing_features", "related_component_ids", "components"),
        ("potential_distinguishing_features", "related_step_ids", "process_steps"),
        ("technical_effects", "related_solution_ids", "technical_solutions"),
        ("embodiments", "component_ids", "components"),
        ("embodiments", "process_step_ids", "process_steps"),
    )
    for collection, field, target_collection in rules:
        valid_targets = identifiers[target_collection]
        for item_index, item in enumerate(analysis[collection]):
            for reference_index, reference in enumerate(item[field]):
                if reference not in valid_targets:
                    failures.append(f"/{collection}/{item_index}/{field}/{reference_index}")

    valid_missing_ids = identifiers["missing_information"]
    for index, question in enumerate(analysis["author_questions"]):
        if question["missing_information_id"] not in valid_missing_ids:
            failures.append(f"/author_questions/{index}/missing_information_id")

    for item_index, drawing in enumerate(analysis["drawing_requirements"]):
        for reference_index, evidence_id in enumerate(drawing["source_evidence_ids"]):
            if evidence_id not in input_evidence_ids or evidence_id not in emitted_evidence_ids:
                failures.append(
                    f"/drawing_requirements/{item_index}/source_evidence_ids/{reference_index}"
                )


def _json_path(path: Iterable[Any]) -> str:
    tokens = [str(token).replace("~", "~0").replace("/", "~1") for token in path]
    return "/" + "/".join(tokens) if tokens else "/"
