"""Validation layers for the P2-002 invention reconstruction contract."""

from __future__ import annotations

import json
import re
import unicodedata
from collections.abc import Iterable, Mapping
from copy import deepcopy
from functools import lru_cache
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from backend.app.schemas.analysis_input import ExtractionInputEnvelope


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
RECONSTRUCTION_SCHEMA_PATH = (
    REPOSITORY_ROOT
    / "schemas/invention-reconstruction/v1.0.0/invention-reconstruction.schema.json"
)
APPROVED_GENERALIZATION_RULE = "SG-01_EXPLICIT_SOURCE_CATEGORY"


class InventionReconstructionValidationError(ValueError):
    """Fail-closed reconstruction error with content-safe diagnostics."""

    def __init__(self, code: str, message: str, *, paths: Iterable[str] = ()) -> None:
        super().__init__(message)
        self.code = code
        self.safe_message = message
        self.paths = tuple(sorted(set(paths)))


@lru_cache(maxsize=1)
def load_reconstruction_schema() -> dict[str, Any]:
    with RECONSTRUCTION_SCHEMA_PATH.open(encoding="utf-8") as source:
        schema = json.load(source)
    Draft202012Validator.check_schema(schema)
    return schema


def validate_reconstruction_schema(reconstruction: Any) -> dict[str, Any]:
    """Validate local shape with the canonical Draft 2020-12 schema."""

    validator = Draft202012Validator(load_reconstruction_schema())
    errors = sorted(
        validator.iter_errors(reconstruction),
        key=lambda error: (_json_path(error.absolute_path), _json_path(error.absolute_schema_path)),
    )
    if errors:
        raise InventionReconstructionValidationError(
            "reconstruction_schema_validation_failed",
            "The reconstruction did not satisfy the canonical P2-002 contract.",
            paths=(_json_path(error.absolute_path) for error in errors[:20]),
        )
    if not isinstance(reconstruction, dict):
        raise InventionReconstructionValidationError(
            "reconstruction_schema_validation_failed",
            "The reconstruction did not satisfy the canonical P2-002 contract.",
        )
    return reconstruction


def validate_reconstruction_business_rules(
    reconstruction: Mapping[str, Any],
    source_envelope: ExtractionInputEnvelope,
    structured_analysis: Mapping[str, Any],
    *,
    allow_review_candidates: bool = False,
) -> None:
    """Validate source integrity, deterministic mappings, and cross-object rules."""

    # Revalidate public entry-point inputs, including Pydantic instances created
    # with model_construct/model_copy, before dereferencing any fields.
    from backend.app.services.invention_reconstruction import (
        _build_reconstruction,
        _load_analysis_schema,
    )
    from backend.app.services.extraction_validation import (
        validate_canonical_output,
        validate_grounding_and_business_rules,
    )

    validate_reconstruction_schema(reconstruction)
    source_envelope = ExtractionInputEnvelope.model_validate(source_envelope.model_dump(mode="json"))
    structured_analysis = validate_canonical_output(structured_analysis, _load_analysis_schema())
    validate_grounding_and_business_rules(structured_analysis, source_envelope)

    failures: list[str] = []
    model = reconstruction["invention_model"]
    review = reconstruction["review_package"]

    _validate_document_identity(reconstruction, source_envelope, structured_analysis, failures)
    evidence_index = _validate_evidence(review, source_envelope, failures)
    _validate_support_objects(reconstruction, structured_analysis, evidence_index, failures)
    identifiers = _collect_identifiers(reconstruction, failures)
    _validate_references(model, review, identifiers, failures)
    expected = _build_reconstruction(structured_analysis)
    comparable = deepcopy(reconstruction)
    _validate_projection(comparable, expected, failures)
    if allow_review_candidates:
        comparable["invention_model"]["variants"] = []
    _compare_projection(comparable, expected, "", failures)
    _validate_relationships_and_flows(model, structured_analysis, failures)
    _validate_step_dependencies(model, failures)
    _validate_generalizations(reconstruction, source_envelope, failures)
    _validate_parameter_ranges(model, source_envelope, failures)
    _validate_review_gates(reconstruction, failures)
    _validate_prohibited_content(reconstruction, failures)

    if failures:
        raise InventionReconstructionValidationError(
            "reconstruction_business_validation_failed",
            "The reconstruction failed deterministic source or business validation.",
            paths=failures,
        )


def _validate_document_identity(
    reconstruction: Mapping[str, Any],
    envelope: ExtractionInputEnvelope,
    analysis: Mapping[str, Any],
    failures: list[str],
) -> None:
    output = reconstruction["document_metadata"]
    source = envelope.document_metadata.model_dump(exclude_none=True)
    upstream = analysis["document_metadata"]
    for field in ("document_id", "file_name", "media_type"):
        if output.get(field) != source.get(field) or output.get(field) != upstream.get(field):
            failures.append(f"/document_metadata/{field}")
    represented_sha = [
        item["sha256"]
        for item in (output, source, upstream)
        if "sha256" in item
    ]
    if represented_sha and any(value != represented_sha[0] for value in represented_sha[1:]):
        failures.append("/document_metadata/sha256")


def _validate_evidence(
    review: Mapping[str, Any],
    envelope: ExtractionInputEnvelope,
    failures: list[str],
) -> dict[str, Mapping[str, Any]]:
    source_index = {unit.evidence_id: unit for unit in envelope.source_units}
    output_index: dict[str, Mapping[str, Any]] = {}
    for index, evidence in enumerate(review["evidence"]):
        path = f"/review_package/evidence/{index}"
        evidence_id = evidence["evidence_id"]
        source = source_index.get(evidence_id)
        if source is None or evidence_id in output_index:
            failures.append(f"{path}/evidence_id")
            continue
        output_index[evidence_id] = evidence
        if evidence["document_id"] != envelope.document_metadata.document_id:
            failures.append(f"{path}/document_id")
        if evidence["evidence_type"] != source.evidence_type:
            failures.append(f"{path}/evidence_type")
        if evidence["locator"] != source.locator.model_dump(exclude_none=True):
            failures.append(f"{path}/locator")
        if evidence["excerpt"] not in source.content:
            failures.append(f"{path}/excerpt")
    return output_index


def _validate_projection(actual: Any, expected: Any, failures: list[str], path: str = "") -> None:
    """Allow only explicit SG-01 category substitution, never structural additions.

    Replacing the SG support in the comparison copy is safe only after retaining
    the exact upstream paths/evidence and checking its source terms separately.
    All other fields, including parameter scopes/units and prose, compare exactly.
    """
    if isinstance(actual, dict) and isinstance(expected, dict):
        support = actual.get("support", {})
        original_support = expected.get("support", {})
        if support.get("grounding_class") == "SAFE_GENERALIZATION" and original_support:
            for key in ("analysis_paths", "evidence_ids"):
                if support[key] != original_support[key]:
                    failures.append(f"{path}/support/{key}")
            if original_support["grounding_class"] == "INFERENCE":
                failures.append(f"{path}/support/grounding_class")
            metadata = support["generalization"]
            category = metadata["generalized_term"]
            members = metadata["member_terms"]
            if any(re.search(r"\d", term) for term in [category, *members]):
                failures.append(f"{path}/support/generalization")
            for key in ("name", "title", "statement", "description", "action"):
                if key not in actual or key not in expected or actual[key] == expected[key]:
                    continue
                candidates = {
                    re.sub(rf"(?<!\w){re.escape(member)}(?!\w)", lambda _: category,
                           expected[key], flags=re.IGNORECASE)
                    for member in members
                }
                if actual[key] in candidates:
                    actual[key] = expected[key]
            actual["support"] = deepcopy(original_support)
        for key in actual.keys() & expected.keys():
            _validate_projection(actual[key], expected[key], failures, f"{path}/{key}")
    elif isinstance(actual, list) and isinstance(expected, list):
        for index, (left, right) in enumerate(zip(actual, expected)):
            _validate_projection(left, right, failures, f"{path}/{index}")


def _compare_projection(actual: Any, expected: Any, path: str, failures: list[str]) -> None:
    if isinstance(actual, Mapping) and isinstance(expected, Mapping):
        for key in actual.keys() | expected.keys():
            child = f"{path}/{key}"
            if key not in actual or key not in expected:
                failures.append(child)
            else:
                _compare_projection(actual[key], expected[key], child, failures)
    elif isinstance(actual, list) and isinstance(expected, list):
        if len(actual) != len(expected):
            failures.append(path)
        for index, (left, right) in enumerate(zip(actual, expected)):
            _compare_projection(left, right, f"{path}/{index}", failures)
    elif type(actual) is not type(expected) or actual != expected:
        failures.append(path or "/")


def _validate_support_objects(
    reconstruction: Any,
    analysis: Mapping[str, Any],
    evidence_index: Mapping[str, Mapping[str, Any]],
    failures: list[str],
) -> None:
    for path, support in _iter_named_objects(reconstruction, "support"):
        for index, evidence_id in enumerate(support["evidence_ids"]):
            if evidence_id not in evidence_index:
                failures.append(f"{path}/evidence_ids/{index}")
        resolved: list[Any] = []
        for index, pointer in enumerate(support["analysis_paths"]):
            try:
                resolved.append(_resolve_pointer(analysis, pointer))
            except (KeyError, IndexError, TypeError, ValueError):
                failures.append(f"{path}/analysis_paths/{index}")
        if support["grounding_class"] in {"SOURCE_FACT", "PARAPHRASE", "INFERENCE"}:
            grounding = next(
                (
                    item.get("grounding")
                    for item in resolved
                    if isinstance(item, Mapping) and isinstance(item.get("grounding"), Mapping)
                ),
                None,
            )
            if grounding is None:
                failures.append(f"{path}/analysis_paths")
            else:
                if support["grounding_class"] != grounding.get("label"):
                    failures.append(f"{path}/grounding_class")
                if support["evidence_ids"] != grounding.get("evidence_ids"):
                    failures.append(f"{path}/evidence_ids")


def _collect_identifiers(
    reconstruction: Mapping[str, Any], failures: list[str]
) -> dict[str, set[str]]:
    model = reconstruction["invention_model"]
    review = reconstruction["review_package"]
    specs = (
        ("title_candidates", model["title_candidates"], "title_id"),
        ("technical_context", model["technical_context"], "context_id"),
        ("problems", model["problems"], "problem_id"),
        ("solution_concepts", model["solution_concepts"], "solution_id"),
        ("elements", model["elements"], "element_id"),
        ("relationships", model["relationships"], "relationship_id"),
        ("method_steps", model["method_steps"], "step_id"),
        ("flows", model["flows"], "flow_id"),
        ("parameters", model["parameters"], "parameter_id"),
        ("technical_effects", model["technical_effects"], "effect_id"),
        ("embodiments", model["embodiments"], "embodiment_id"),
        ("variants", model["variants"], "variant_id"),
        ("source_artifacts", model["source_artifacts"], "artifact_id"),
        ("conflicts", review["conflicts"], "conflict_id"),
        ("missing_information", review["missing_information"], "missing_id"),
        ("author_questions", review["author_questions"], "question_id"),
        ("warnings", review["warnings"], "warning_id"),
    )
    identifiers: dict[str, set[str]] = {}
    seen: set[str] = set()
    for collection, values, id_field in specs:
        current: set[str] = set()
        for index, item in enumerate(values):
            identifier = item[id_field]
            if identifier in current or identifier in seen:
                failures.append(f"/{collection}/{index}/{id_field}")
            current.add(identifier)
            seen.add(identifier)
        identifiers[collection] = current
    field_id = model["technical_field"].get("field_id")
    if field_id:
        if field_id in seen:
            failures.append("/invention_model/technical_field/field_id")
        identifiers["technical_field"] = {field_id}
        seen.add(field_id)
    else:
        identifiers["technical_field"] = set()
    for collection in ("method_steps", "technical_effects"):
        for item_index, item in enumerate(model[collection]):
            for condition_index, condition in enumerate(item["conditions"]):
                identifier = condition["condition_id"]
                if identifier in seen:
                    failures.append(
                        f"/invention_model/{collection}/{item_index}/conditions/{condition_index}/condition_id"
                    )
                seen.add(identifier)
    return identifiers


def _validate_references(
    model: Mapping[str, Any],
    review: Mapping[str, Any],
    identifiers: Mapping[str, set[str]],
    failures: list[str],
) -> None:
    rules = (
        ("solution_concepts", "addresses_problem_ids", "problems"),
        ("solution_concepts", "related_element_ids", "elements"),
        ("solution_concepts", "related_step_ids", "method_steps"),
        ("method_steps", "input_element_ids", "elements"),
        ("method_steps", "output_element_ids", "elements"),
        ("method_steps", "dependency_step_ids", "method_steps"),
        ("technical_effects", "related_solution_ids", "solution_concepts"),
        ("technical_effects", "related_element_ids", "elements"),
        ("embodiments", "element_ids", "elements"),
        ("embodiments", "method_step_ids", "method_steps"),
        ("embodiments", "parameter_ids", "parameters"),
    )
    for collection, field, target in rules:
        for item_index, item in enumerate(model[collection]):
            for ref_index, reference in enumerate(item[field]):
                if reference not in identifiers[target]:
                    failures.append(
                        f"/invention_model/{collection}/{item_index}/{field}/{ref_index}"
                    )
    entity_ids = set().union(
        identifiers["elements"],
        identifiers["method_steps"],
        identifiers["solution_concepts"],
        identifiers["problems"],
        identifiers["parameters"],
        identifiers["technical_effects"],
        identifiers["embodiments"],
    )
    for index, relation in enumerate(model["relationships"]):
        if relation["subject_id"] not in entity_ids:
            failures.append(f"/invention_model/relationships/{index}/subject_id")
        if relation["object_id"] not in entity_ids:
            failures.append(f"/invention_model/relationships/{index}/object_id")
    flow_ids = identifiers["elements"] | identifiers["method_steps"]
    for index, flow in enumerate(model["flows"]):
        if flow["source_id"] not in flow_ids:
            failures.append(f"/invention_model/flows/{index}/source_id")
        if flow["target_id"] not in flow_ids:
            failures.append(f"/invention_model/flows/{index}/target_id")
    for index, variant in enumerate(model["variants"]):
        for ref_index, reference in enumerate(variant["base_entity_ids"]):
            if reference not in entity_ids:
                failures.append(
                    f"/invention_model/variants/{index}/base_entity_ids/{ref_index}"
                )
    for index, parameter in enumerate(model["parameters"]):
        for ref_index, reference in enumerate(parameter["related_entity_ids"]):
            if reference not in entity_ids:
                failures.append(f"/invention_model/parameters/{index}/related_entity_ids/{ref_index}")
    missing_ids = identifiers["missing_information"]
    for index, question in enumerate(review["author_questions"]):
        if question["missing_information_id"] not in missing_ids:
            failures.append(f"/review_package/author_questions/{index}/missing_information_id")
    for index, conflict in enumerate(review["conflicts"]):
        for ref_index, reference in enumerate(conflict["affected_entity_ids"]):
            if reference not in entity_ids:
                failures.append(
                    f"/review_package/conflicts/{index}/affected_entity_ids/{ref_index}"
                )


def _validate_relationships_and_flows(
    model: Mapping[str, Any], analysis: Mapping[str, Any], failures: list[str]
) -> None:
    component_ids = {
        component["component_id"]: f"IR-ELEM-{index + 1:04d}"
        for index, component in enumerate(analysis["components"])
    }
    step_ids = {
        step["step_id"]: f"IR-STEP-{index + 1:04d}"
        for index, step in enumerate(analysis["process_steps"])
    }
    expected_relations: list[tuple[str, str, str]] = []
    expected_flows: list[tuple[str, str]] = []
    for component in analysis["components"]:
        for related in component["related_component_ids"]:
            expected_relations.append(
                (component_ids[component["component_id"]], "RELATED_TO", component_ids[related])
            )
    for step in analysis["process_steps"]:
        step_id = step_ids[step["step_id"]]
        for component in step["input_component_ids"]:
            expected_relations.append((component_ids[component], "INPUT_TO_STEP", step_id))
            expected_flows.append((component_ids[component], step_id))
        for component in step["output_component_ids"]:
            expected_relations.append((step_id, "OUTPUT_FROM_STEP", component_ids[component]))
            expected_flows.append((step_id, component_ids[component]))
    actual_relations = [
        (item["subject_id"], item["relation_type"], item["object_id"])
        for item in model["relationships"]
    ]
    if actual_relations != expected_relations:
        failures.append("/invention_model/relationships")
    actual_flows = [(item["source_id"], item["target_id"]) for item in model["flows"]]
    if actual_flows != expected_flows:
        failures.append("/invention_model/flows")
    for index, flow in enumerate(model["flows"]):
        if flow["flow_type"] != "UNSPECIFIED":
            failures.append(f"/invention_model/flows/{index}/flow_type")


def _validate_step_dependencies(model: Mapping[str, Any], failures: list[str]) -> None:
    graph = {
        step["step_id"]: tuple(step["dependency_step_ids"])
        for step in model["method_steps"]
    }
    # Iterative topological traversal: dangling IDs are already reported by the
    # reference validator and must not raise KeyError or exhaust recursion here.
    incoming = {node: 0 for node in graph}
    for dependencies in graph.values():
        for dependency in dependencies:
            if dependency in incoming:
                incoming[dependency] += 1
    ready = [node for node, degree in incoming.items() if degree == 0]
    visited = 0
    while ready:
        node = ready.pop()
        visited += 1
        for dependency in graph[node]:
            if dependency in incoming:
                incoming[dependency] -= 1
                if incoming[dependency] == 0:
                    ready.append(dependency)
    if visited != len(graph):
        for index, step in enumerate(model["method_steps"]):
            if incoming[step["step_id"]]:
                failures.append(f"/invention_model/method_steps/{index}/dependency_step_ids")


def _validate_generalizations(
    reconstruction: Any,
    envelope: ExtractionInputEnvelope,
    failures: list[str],
) -> None:
    source_index = {unit.evidence_id: unit.content for unit in envelope.source_units}
    for path, support in _iter_named_objects(reconstruction, "support"):
        if support["grounding_class"] != "SAFE_GENERALIZATION":
            continue
        metadata = support.get("generalization", {})
        if metadata.get("rule_id") != APPROVED_GENERALIZATION_RULE:
            failures.append(f"{path}/generalization/rule_id")
            continue
        evidence_ids = metadata.get("evidence_ids", [])
        if evidence_ids != support["evidence_ids"]:
            failures.append(f"{path}/generalization/evidence_ids")
        cited = [_normalize_text(source_index.get(evidence_id, "")) for evidence_id in evidence_ids]
        def contains(term: str) -> bool:
            pattern = rf"(?<!\w){re.escape(_normalize_text(term))}(?!\w)"
            return any(re.search(pattern, unit) is not None for unit in cited)

        if not contains(metadata.get("generalized_term", "")):
            failures.append(f"{path}/generalization/generalized_term")
        for index, member in enumerate(metadata.get("member_terms", [])):
            if not contains(member):
                failures.append(f"{path}/generalization/member_terms/{index}")


def _validate_parameter_ranges(
    model: Mapping[str, Any],
    envelope: ExtractionInputEnvelope,
    failures: list[str],
) -> None:
    source_index = {unit.evidence_id: unit.content for unit in envelope.source_units}
    for index, parameter in enumerate(model["parameters"]):
        value = parameter["value"]
        if value["value_kind"] != "RANGE":
            continue
        cited = " ".join(source_index.get(item, "") for item in parameter["support"]["evidence_ids"])
        for key in ("minimum", "maximum"):
            if not any(_contains_number_token(cited, token) for token in _number_tokens(value[key])):
                failures.append(f"/invention_model/parameters/{index}/value/{key}")
        if value["minimum"] > value["maximum"]:
            failures.append(f"/invention_model/parameters/{index}/value")


def _validate_review_gates(reconstruction: Any, failures: list[str]) -> None:
    for path, value in _walk(reconstruction):
        if path.startswith("/review_package/evidence/"):
            continue
        if path.rsplit("/", 1)[-1] in {"grounding_class", "status"} and value == "HUMAN_CONFIRMED":
            failures.append(path)
        if isinstance(value, Mapping) and value.get("status") == "HUMAN_RESOLVED":
            failures.append(f"{path}/status")
    for index, variant in enumerate(reconstruction["invention_model"]["variants"]):
        status = variant["status"]
        grounding = variant["support"]["grounding_class"]
        if status != "PROPOSED_REQUIRES_HUMAN_CONFIRMATION":
            failures.append("/invention_model/variants")
        if status == "PROPOSED_REQUIRES_HUMAN_CONFIRMATION" and grounding != "PROPOSED_VARIANT":
            failures.append(f"/invention_model/variants/{index}/support/grounding_class")
        if status == "SOURCE_SUPPORTED" and grounding == "PROPOSED_VARIANT":
            failures.append(f"/invention_model/variants/{index}/status")


def _validate_prohibited_content(reconstruction: Any, failures: list[str]) -> None:
    prohibited_keys = {
        "claims",
        "claim_text",
        "independent_claim",
        "dependent_claim",
        "claim_strategy",
        "inventor",
        "assignee",
        "filing_date",
        "priority_number",
        "patent_number",
        "examiner",
        "classification",
    }
    prohibited_phrases = (
        "is patentable",
        "is non-obvious",
        "is novel over prior art",
        "what is claimed is",
        "independent claim",
        "dependent claim",
        "infringes",
        "filing-ready",
    )
    for path, value in _walk(reconstruction):
        if path.rsplit("/", 1)[-1].casefold() in prohibited_keys:
            failures.append(path)
        # Source excerpts, filenames, locators and JSON pointers are untrusted
        # data, not generated legal assertions or executable instructions.
        if path.startswith("/review_package/evidence/"):
            continue
        if isinstance(value, str) and path.rsplit("/", 1)[-1] in {
            "name", "title", "statement", "action", "description", "rationale",
            "message", "question", "topic", "resolution", "source_reference",
        }:
            normalized = _normalize_text(value)
            if any(phrase in normalized for phrase in prohibited_phrases):
                failures.append(path)


def _resolve_pointer(document: Any, pointer: str) -> Any:
    if not pointer.startswith("/"):
        raise ValueError(pointer)
    current = document
    for token in pointer[1:].split("/"):
        if re.search(r"~(?![01])", token):
            raise ValueError("Invalid JSON Pointer escape")
        decoded = token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, list):
            if re.fullmatch(r"0|[1-9][0-9]*", decoded) is None:
                raise ValueError("Invalid JSON Pointer array index")
            current = current[int(decoded)]
        else:
            current = current[decoded]
    return current


def _iter_named_objects(value: Any, name: str, path: str = ""):
    if isinstance(value, Mapping):
        for key, item in value.items():
            child = f"{path}/{key}"
            if key == name and isinstance(item, Mapping):
                yield child, item
            yield from _iter_named_objects(item, name, child)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from _iter_named_objects(item, name, f"{path}/{index}")


def _walk(value: Any, path: str = ""):
    yield path or "/", value
    if isinstance(value, Mapping):
        for key, item in value.items():
            yield from _walk(item, f"{path}/{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from _walk(item, f"{path}/{index}")


def _normalize_text(value: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def _number_tokens(value: int | float) -> set[str]:
    tokens = {str(value)}
    if isinstance(value, float) and value.is_integer():
        tokens.add(str(int(value)))
    return tokens


def _contains_number_token(text: str, token: str) -> bool:
    return re.search(rf"(?<![0-9.]){re.escape(token)}(?![0-9.])", text) is not None


def _json_path(path: Iterable[Any]) -> str:
    tokens = [str(token).replace("~", "~0").replace("/", "~1") for token in path]
    return "/" + "/".join(tokens) if tokens else "/"
