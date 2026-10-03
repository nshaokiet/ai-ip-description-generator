"""Deterministic offline APP-002 + AI-001 to P2-002 reconstruction."""

from __future__ import annotations

import json
from copy import deepcopy
from functools import lru_cache
from typing import Any

from backend.app.schemas.analysis_input import ExtractionInputEnvelope
from backend.app.services.extraction_validation import (
    validate_canonical_output,
    validate_grounding_and_business_rules,
)
from backend.app.services.invention_reconstruction_validation import (
    REPOSITORY_ROOT,
    validate_reconstruction_business_rules,
    validate_reconstruction_schema,
)


ANALYSIS_SCHEMA_PATH = (
    REPOSITORY_ROOT / "schemas/invention-output/v1.0.0/invention-output.schema.json"
)


@lru_cache(maxsize=1)
def _load_analysis_schema() -> dict[str, Any]:
    with ANALYSIS_SCHEMA_PATH.open(encoding="utf-8") as source:
        return json.load(source)


def reconstruct_invention(
    source_envelope: ExtractionInputEnvelope | dict[str, Any],
    structured_analysis: dict[str, Any],
) -> dict[str, Any]:
    """Return a validated, deterministic INVENTION_RECONSTRUCTION v1.0.0."""

    envelope = ExtractionInputEnvelope.model_validate(
        source_envelope.model_dump(mode="json")
        if isinstance(source_envelope, ExtractionInputEnvelope)
        else source_envelope
    )
    analysis = validate_canonical_output(structured_analysis, _load_analysis_schema())
    validate_grounding_and_business_rules(analysis, envelope)

    reconstruction = _build_reconstruction(analysis)
    validate_reconstruction_schema(reconstruction)
    validate_reconstruction_business_rules(reconstruction, envelope, analysis)
    return reconstruction


def _build_reconstruction(analysis: dict[str, Any]) -> dict[str, Any]:
    """Pure projection of validated AI-001 data; not a validation entry point."""

    problem_ids = _id_map(analysis["technical_problems"], "problem_id", "IR-PROB")
    solution_ids = _id_map(analysis["technical_solutions"], "solution_id", "IR-SOL")
    element_ids = _id_map(analysis["components"], "component_id", "IR-ELEM")
    step_ids = _id_map(analysis["process_steps"], "step_id", "IR-STEP")
    parameter_ids = _parameter_id_map(analysis["experimental_data"])

    relationships, flows = _build_relations_and_flows(
        analysis, element_ids=element_ids, step_ids=step_ids
    )
    missing_ids = _id_map(analysis["missing_information"], "missing_id", "MI-IR")

    reconstruction: dict[str, Any] = {
        "schema_version": "1.0.0",
        "output_type": "INVENTION_RECONSTRUCTION",
        "output_notice": {
            "status": "DRAFT",
            "human_review_required": True,
            "is_legal_advice": False,
            "filing_ready": False,
            "includes_patentability_assessment": False,
            "includes_claims": False,
        },
        "document_metadata": dict(analysis["document_metadata"]),
        "provenance": {
            "source_evidence_contract": {
                "task_id": "APP-002",
                "contract_name": "ExtractionInputEnvelope",
                "schema_version": "1.0.0",
            },
            "structured_analysis_contract": {
                "task_id": "AI-001",
                "contract_name": "STRUCTURED_INVENTION_ANALYSIS",
                "schema_version": "1.0.0",
            },
            "reconstruction_mode": "OFFLINE_DETERMINISTIC",
        },
        "invention_model": {
            "title_candidates": [
                {
                    "title_id": f"IR-TITLE-{index + 1:04d}",
                    "title": item["title"],
                    "rationale": item["rationale"],
                    "support": _support(item, f"/title_candidates/{index}"),
                }
                for index, item in enumerate(analysis["title_candidates"])
            ],
            "technical_field": _technical_field(analysis),
            "technical_context": [
                {
                    "context_id": f"IR-CONTEXT-{index + 1:04d}",
                    "statement": item["text"],
                    "support": _support(item, f"/background/{index}"),
                }
                for index, item in enumerate(analysis["background"])
            ],
            "problems": [
                {
                    "problem_id": problem_ids[item["problem_id"]],
                    "statement": item["statement"],
                    "support": _support(item, f"/technical_problems/{index}"),
                }
                for index, item in enumerate(analysis["technical_problems"])
            ],
            "solution_concepts": [
                {
                    "solution_id": solution_ids[item["solution_id"]],
                    "statement": item["statement"],
                    "addresses_problem_ids": [
                        problem_ids[problem_id]
                        for problem_id in item["addresses_problem_ids"]
                    ],
                    "related_element_ids": [],
                    "related_step_ids": [],
                    "support": _support(item, f"/technical_solutions/{index}"),
                }
                for index, item in enumerate(analysis["technical_solutions"])
            ],
            "elements": [
                _element(item, index, element_ids[item["component_id"]])
                for index, item in enumerate(analysis["components"])
            ],
            "relationships": relationships,
            "method_steps": [
                _method_step(item, index, element_ids, step_ids[item["step_id"]])
                for index, item in enumerate(analysis["process_steps"])
            ],
            "flows": flows,
            "parameters": _parameters(analysis, parameter_ids),
            "technical_effects": [
                _technical_effect(item, index, solution_ids)
                for index, item in enumerate(analysis["technical_effects"])
            ],
            "embodiments": [
                _embodiment(item, index, element_ids, step_ids)
                for index, item in enumerate(analysis["embodiments"])
            ],
            "variants": [],
            "source_artifacts": _source_artifacts(analysis),
        },
        "review_package": {
            "evidence": deepcopy(analysis["evidence"]),
            "conflicts": [],
            "missing_information": [
                {
                    "missing_id": missing_ids[item["missing_id"]],
                    "target_path": item["target_path"],
                    "description": item["description"],
                    "reason": item["reason"],
                    "impact": item["impact"],
                    "owner": item["owner"],
                    "analysis_paths": [f"/missing_information/{index}"],
                }
                for index, item in enumerate(analysis["missing_information"])
            ],
            "author_questions": [
                {
                    "question_id": f"AQ-IR-{index + 1:04d}",
                    "missing_information_id": missing_ids[item["missing_information_id"]],
                    "question": item["question"],
                    "priority": item["priority"],
                    "analysis_paths": [f"/author_questions/{index}"],
                }
                for index, item in enumerate(analysis["author_questions"])
            ],
            "warnings": [
                {
                    "warning_id": f"W-IR-{index + 1:04d}",
                    "code": "UPSTREAM_CANDIDATE_FEATURE_REQUIRES_REVIEW",
                    "message": item["statement"],
                    "analysis_paths": [f"/potential_distinguishing_features/{index}"],
                    "support": _support(item, f"/potential_distinguishing_features/{index}"),
                }
                for index, item in enumerate(analysis["potential_distinguishing_features"])
            ],
        },
    }
    return reconstruction


def _id_map(items: list[dict[str, Any]], source_key: str, prefix: str) -> dict[str, str]:
    return {
        item[source_key]: f"{prefix}-{index + 1:04d}"
        for index, item in enumerate(items)
    }


def _support(item: dict[str, Any], analysis_path: str) -> dict[str, Any]:
    grounding = item["grounding"]
    return {
        "grounding_class": grounding["label"],
        "evidence_ids": list(grounding["evidence_ids"]),
        "analysis_paths": [analysis_path],
    }


def _technical_field(analysis: dict[str, Any]) -> dict[str, Any]:
    field = analysis["technical_field"]
    if field["status"] == "MISSING":
        return {"status": "MISSING"}
    item = field["item"]
    output: dict[str, Any] = {
        "status": "PRESENT",
        "field_id": "IR-FIELD-0001",
        "name": item["name"],
        "support": _support(item, "/technical_field/item"),
    }
    if "description" in item:
        output["description"] = item["description"]
    return output


def _element(item: dict[str, Any], index: int, element_id: str) -> dict[str, Any]:
    output: dict[str, Any] = {
        "element_id": element_id,
        "name": item["name"],
        "element_type": "OTHER",
        "essentiality": "UNKNOWN",
        "support": _support(item, f"/components/{index}"),
    }
    if "description" in item:
        output["description"] = item["description"]
    return output


def _method_step(
    item: dict[str, Any],
    index: int,
    element_ids: dict[str, str],
    step_id: str,
) -> dict[str, Any]:
    return {
        "step_id": step_id,
        "sequence_index": item["sequence"],
        "action": item["action"],
        "input_element_ids": [element_ids[value] for value in item["input_component_ids"]],
        "output_element_ids": [element_ids[value] for value in item["output_component_ids"]],
        "dependency_step_ids": [],
        "conditions": [
            {
                "condition_id": f"IR-STEP-COND-{index + 1:04d}-{condition_index + 1:03d}",
                "statement": condition["text"],
                "support": _support(
                    condition,
                    f"/process_steps/{index}/conditions/{condition_index}",
                ),
            }
            for condition_index, condition in enumerate(item["conditions"])
        ],
        "support": _support(item, f"/process_steps/{index}"),
    }


def _build_relations_and_flows(
    analysis: dict[str, Any],
    *,
    element_ids: dict[str, str],
    step_ids: dict[str, str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    relationships: list[dict[str, Any]] = []
    flows: list[dict[str, Any]] = []

    def add_relation(
        subject_id: str,
        relation_type: str,
        object_id: str,
        source_item: dict[str, Any],
        analysis_path: str,
    ) -> None:
        relationships.append(
            {
                "relationship_id": f"IR-REL-{len(relationships) + 1:04d}",
                "subject_id": subject_id,
                "relation_type": relation_type,
                "object_id": object_id,
                "support": _support(source_item, analysis_path),
            }
        )

    def add_flow(
        source_id: str,
        target_id: str,
        description: str,
        source_item: dict[str, Any],
        analysis_path: str,
    ) -> None:
        flows.append(
            {
                "flow_id": f"IR-FLOW-{len(flows) + 1:04d}",
                "flow_type": "UNSPECIFIED",
                "source_id": source_id,
                "target_id": target_id,
                "description": description,
                "support": _support(source_item, analysis_path),
            }
        )

    for index, component in enumerate(analysis["components"]):
        for related in component["related_component_ids"]:
            add_relation(
                element_ids[component["component_id"]],
                "RELATED_TO",
                element_ids[related],
                component,
                f"/components/{index}",
            )
    for index, step in enumerate(analysis["process_steps"]):
        step_id = step_ids[step["step_id"]]
        for component_id in step["input_component_ids"]:
            element_id = element_ids[component_id]
            add_relation(element_id, "INPUT_TO_STEP", step_id, step, f"/process_steps/{index}")
            add_flow(
                element_id,
                step_id,
                f"Input to step: {step['action']}",
                step,
                f"/process_steps/{index}",
            )
        for component_id in step["output_component_ids"]:
            element_id = element_ids[component_id]
            add_relation(step_id, "OUTPUT_FROM_STEP", element_id, step, f"/process_steps/{index}")
            add_flow(
                step_id,
                element_id,
                f"Output from step: {step['action']}",
                step,
                f"/process_steps/{index}",
            )
    return relationships, flows


def _parameter_id_map(experiments: list[dict[str, Any]]) -> dict[tuple[int, str, int], str]:
    mapping: dict[tuple[int, str, int], str] = {}
    counter = 1
    for experiment_index, experiment in enumerate(experiments):
        for kind in ("conditions", "results"):
            for item_index, _ in enumerate(experiment[kind]):
                mapping[(experiment_index, kind, item_index)] = f"IR-PARAM-{counter:04d}"
                counter += 1
    return mapping


def _parameters(
    analysis: dict[str, Any],
    parameter_ids: dict[tuple[int, str, int], str],
) -> list[dict[str, Any]]:
    parameters: list[dict[str, Any]] = []
    for experiment_index, experiment in enumerate(analysis["experimental_data"]):
        for kind, role, name_key in (
            ("conditions", "EXPERIMENTAL_CONDITION", "parameter"),
            ("results", "EXPERIMENTAL_RESULT", "metric"),
        ):
            for item_index, item in enumerate(experiment[kind]):
                path = f"/experimental_data/{experiment_index}"
                parameter: dict[str, Any] = {
                    "parameter_id": parameter_ids[(experiment_index, kind, item_index)],
                    "name": item[name_key],
                    "role": role,
                    "value": {"value_kind": "EXACT", "exact_value": item["value"]},
                    "scope_status": "EXAMPLE_ONLY",
                    "related_entity_ids": [],
                    "support": _support(experiment, path),
                }
                if "unit" in item:
                    parameter["unit"] = item["unit"]
                parameter["support"]["analysis_paths"].append(f"{path}/{kind}/{item_index}")
                parameters.append(parameter)
    return parameters


def _technical_effect(
    item: dict[str, Any], index: int, solution_ids: dict[str, str]
) -> dict[str, Any]:
    return {
        "effect_id": f"IR-EFFECT-{index + 1:04d}",
        "statement": item["statement"],
        "related_solution_ids": [solution_ids[value] for value in item["related_solution_ids"]],
        "related_element_ids": [],
        "conditions": [
            {
                "condition_id": f"IR-EFFECT-COND-{index + 1:04d}-{condition_index + 1:03d}",
                "statement": condition["text"],
                "support": _support(
                    condition,
                    f"/technical_effects/{index}/conditions/{condition_index}",
                ),
            }
            for condition_index, condition in enumerate(item["conditions"])
        ],
        "effect_basis": (
            "SUPPORTED_CONSEQUENCE"
            if item["grounding"]["label"] == "INFERENCE"
            else "SOURCE_REPORTED"
        ),
        "support": _support(item, f"/technical_effects/{index}"),
    }


def _embodiment(
    item: dict[str, Any],
    index: int,
    element_ids: dict[str, str],
    step_ids: dict[str, str],
) -> dict[str, Any]:
    return {
        "embodiment_id": f"IR-EMB-{index + 1:04d}",
        "name": item["name"],
        "description": item["description"],
        "element_ids": [element_ids[value] for value in item["component_ids"]],
        "method_step_ids": [step_ids[value] for value in item["process_step_ids"]],
        "parameter_ids": [],
        "disclosure_status": (
            "SYNTHESIZED"
            if item["grounding"]["label"] == "INFERENCE"
            else "EXPLICIT"
        ),
        "support": _support(item, f"/embodiments/{index}"),
    }


def _source_artifacts(analysis: dict[str, Any]) -> list[dict[str, Any]]:
    artifacts: list[dict[str, Any]] = []
    for index, evidence in enumerate(analysis["evidence"]):
        if evidence["evidence_type"] == "TABLE":
            artifacts.append(
                {
                    "artifact_id": f"IR-ART-{len(artifacts) + 1:04d}",
                    "artifact_type": "TABLE",
                    "source_reference": evidence["locator"].get(
                        "table_id", evidence["evidence_id"]
                    ),
                    "evidence_ids": [evidence["evidence_id"]],
                    "human_confirmation_required": False,
                    "analysis_paths": [f"/evidence/{index}"],
                }
            )
        if "figure_id" in evidence["locator"]:
            artifacts.append({
                "artifact_id": f"IR-ART-{len(artifacts) + 1:04d}",
                "artifact_type": "FIGURE_REFERENCE",
                "source_reference": evidence["locator"]["figure_id"],
                "evidence_ids": [evidence["evidence_id"]],
                "human_confirmation_required": False,
                "analysis_paths": [f"/evidence/{index}"],
            })
    for index, drawing in enumerate(analysis["drawing_requirements"]):
        artifacts.append(
            {
                "artifact_id": f"IR-ART-{len(artifacts) + 1:04d}",
                "artifact_type": "DRAWING_REQUIREMENT",
                "source_reference": drawing["title"],
                "evidence_ids": list(drawing["source_evidence_ids"]),
                "human_confirmation_required": drawing["human_confirmation_required"],
                "analysis_paths": [f"/drawing_requirements/{index}"],
                "drawing_id": drawing["drawing_id"],
                "drawing_kind": drawing["kind"],
                "drawing_status": drawing["status"],
            }
        )
    return artifacts
