"""Deterministic, offline P2-004 supported draft Claims generator.

Only the released P2-002 reconstruction and P2-003 specification are semantic
inputs.  The service intentionally has no network/provider/runtime integration.
"""
from __future__ import annotations

from collections import defaultdict, deque
from copy import deepcopy
import re
from typing import Any, Iterable

from backend.app.services.uspto_specification_generation import RELATION_WORDING
from backend.app.services.uspto_specification_generation_validation import prohibited_text
from backend.app.services.supported_draft_claims_validation import (
    FAMILY_ORDER,
    GROUNDING_ELIGIBLE,
    STRUCTURAL_TYPES,
    SupportedDraftClaimsValidationError,
    canonical_json,
    claims_draft_id,
    source_identity,
    validate_inputs,
)


STRUCTURAL_ELEMENT_TYPES = {
    "DEVICE", "MODULE", "STRUCTURE", "SOFTWARE_COMPONENT", "DATA_STRUCTURE", "PROCESSING_BLOCK"
}
POSITIVE_SECTIONS = (
    "BRIEF_SUMMARY_OF_THE_INVENTION",
    "DETAILED_DESCRIPTION_OF_THE_INVENTION",
)
PARAMETER_ROLES = {"OPERATING_CONDITION", "THRESHOLD", "DIMENSION"}
CONDITION_MARKERS = re.compile(
    r"\b(if|when|while|where|under|during|upon|in response to|subject to|provided that)\b",
    re.IGNORECASE,
)
ISSUE_MESSAGES = {
    "INSUFFICIENT_INDEPENDENT_CLAIM_SUPPORT": "The selected solution lacks a complete supported structural core.",
    "METHOD_STEP_ESSENTIALITY_UNAVAILABLE": "Released upstream data does not establish method-step essentiality.",
    "COMPOSITION_SEMANTICS_UNAVAILABLE": "Released upstream data does not establish required composition semantics.",
    "PARAMETER_ESSENTIALITY_UNAVAILABLE": "Released upstream data does not establish parameter essentiality.",
    "CLAIM_ELEMENT_UNSUPPORTED": "A required claim unit is not eligible under the released support contract.",
    "CLAIM_ELEMENT_GROUNDING_INELIGIBLE": "A claim unit uses grounding that is not eligible for draft Claims.",
    "UNRESOLVED_RECONSTRUCTION_CONFLICT": "An unresolved reconstruction conflict affects this claim family.",
    "CLAIM_ELEMENT_CONFLICT_TAINTED": "A candidate claim unit is tainted by an unresolved reconstruction conflict.",
    "CLAIM_PARAMETER_BROADENING": "A parameter limitation would broaden or alter its released source semantics.",
    "CLAIM_RELATIONSHIP_STRENGTHENING": "A relationship limitation would strengthen or alter its released source semantics.",
    "CLAIM_EVIDENCE_NOT_FOUND": "Required source evidence could not be closed for this claim unit.",
    "CLAIM_SPECIFICATION_SUPPORT_NOT_FOUND": "Required positive specification disclosure could not be closed for this claim unit.",
    "DUPLICATE_LIMITATION": "A duplicate limitation candidate was excluded before numbering.",
    "CLAIM_EXAMPLE_SCOPE_INELIGIBLE": "An example-only parameter cannot become a mandatory claim limitation.",
    "CLAIM_UNKNOWN_SCOPE_INELIGIBLE": "A parameter with unknown scope cannot become a mandatory claim limitation.",
    "CLAIM_NEGATIVE_LIMITATION_UNSUPPORTED": "An unsupported negative limitation cannot be introduced.",
    "UNROUTED_UPSTREAM_GAP": "An upstream technical gap could not be safely routed and blocks this family.",
    "REQUIRED_UPSTREAM_INFORMATION_MISSING": "Required upstream technical information is missing for this family.",
    "PROHIBITED_CLAIM_CONTENT": "A technical field contains content prohibited from deterministic draft Claims.",
}
WARNING_MESSAGES = {
    "DUPLICATE_LIMITATION": "A duplicate limitation candidate was excluded before numbering.",
    "DEPENDENT_LIMIT_EXCEEDED": "Eligible dependent limitations exceeded the configured deterministic family cap.",
    "HUMAN_IP_REVIEW_REQUIRED": "Human/IP-specialist review is required before any downstream use.",
}


def _unique(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(values))


def _support(obj: dict[str, Any]) -> dict[str, Any] | None:
    value = obj.get("support")
    return value if type(value) is dict else None


def _entity_id(obj: dict[str, Any]) -> str | None:
    for key in (
        "solution_id", "element_id", "relationship_id", "step_id", "flow_id",
        "parameter_id", "effect_id", "embodiment_id", "variant_id",
    ):
        if key in obj:
            return obj[key]
    return None


def _technical_strings(obj: dict[str, Any], kind: str) -> list[str]:
    if kind == "element":
        return [obj["name"], *([obj["description"]] if "description" in obj else [])]
    if kind == "solution":
        return [obj["statement"]]
    if kind == "relationship":
        return []
    if kind in {"embodiment", "variant"}:
        return [obj["description"]]
    if kind == "parameter":
        return [obj["name"]]
    return []


def _scalar_literal(value: Any) -> str:
    if type(value) is str:
        return value
    return canonical_json(value)


def _ordered_literal(excerpt: str, values: Iterable[str]) -> bool:
    position = 0
    for value in values:
        found = excerpt.find(value, position)
        if found < 0:
            return False
        position = found + len(value)
    return True


def _parameter_literal_support(
    parameter: dict[str, Any],
    evidence_ids: list[str],
    evidence: dict[str, dict[str, Any]],
) -> bool:
    value = parameter["value"]
    kind = value["value_kind"]
    required: list[str] = [parameter["name"]]
    if kind == "EXACT":
        required.append(_scalar_literal(value["exact_value"]))
    elif kind == "RANGE":
        required.extend((_scalar_literal(value["minimum"]), _scalar_literal(value["maximum"])))
    elif kind == "SET":
        required.extend(_scalar_literal(item) for item in value["values"])
    else:
        required.append(value["qualitative_value"])
    if parameter.get("unit"):
        required.append(parameter["unit"])
    return any(
        _ordered_literal(evidence[evidence_id]["excerpt"], required)
        for evidence_id in evidence_ids
        if evidence_id in evidence
    )


def _literal_support(
    obj: dict[str, Any],
    kind: str,
    evidence_ids: list[str],
    evidence: dict[str, dict[str, Any]],
) -> bool:
    if kind == "parameter":
        return _parameter_literal_support(obj, evidence_ids, evidence)
    strings = _technical_strings(obj, kind)
    excerpts = [evidence[x]["excerpt"] for x in evidence_ids if x in evidence]
    return all(any(value in excerpt for excerpt in excerpts) for value in strings)


def _relationship_literal_support(
    relationship: dict[str, Any],
    subject: dict[str, Any],
    obj: dict[str, Any],
    evidence: dict[str, dict[str, Any]],
) -> bool:
    support = _support(relationship)
    if support is None:
        return False
    return any(
        subject["name"] in evidence[evidence_id]["excerpt"]
        and obj["name"] in evidence[evidence_id]["excerpt"]
        for evidence_id in support.get("evidence_ids", [])
        if evidence_id in evidence
    )


def _support_evidence_ids(objects: Iterable[dict[str, Any]]) -> list[str]:
    return _unique(
        evidence_id
        for obj in objects
        for evidence_id in ((_support(obj) or {}).get("evidence_ids", []))
    )


def _fingerprint_part(obj: dict[str, Any], kind: str) -> Any:
    if kind == "element":
        return [
            "ELEMENT", obj["element_id"], obj["name"], obj.get("description"),
            obj["element_type"], obj["essentiality"],
        ]
    if kind == "relationship":
        return [
            "RELATIONSHIP", obj["relationship_id"], obj["subject_id"],
            obj["relation_type"], obj["object_id"],
        ]
    if kind == "parameter":
        return [
            "PARAMETER", obj["parameter_id"], obj["name"], obj["role"],
            deepcopy(obj["value"]), obj.get("unit"), obj["scope_status"],
            deepcopy(obj["related_entity_ids"]),
        ]
    if kind == "embodiment":
        return [
            "EMBODIMENT", obj["embodiment_id"], obj["name"], obj["description"],
            deepcopy(obj["element_ids"]), deepcopy(obj["method_step_ids"]),
            deepcopy(obj["parameter_ids"]), obj["disclosure_status"],
        ]
    if kind == "variant":
        return [
            "VARIANT", obj["variant_id"], obj["description"], deepcopy(obj["base_entity_ids"]),
            obj["status"], obj["human_confirmation_required"], obj["filing_content_eligible"],
        ]
    return [kind.upper(), _entity_id(obj)]


def _limitation_fingerprint(components: list[tuple[dict[str, Any], str, str]]) -> str:
    ordered_ids = [_entity_id(obj) for obj, _, _ in components if _entity_id(obj) is not None]
    return canonical_json([
        ordered_ids,
        [_fingerprint_part(obj, kind) for obj, _, kind in components],
    ])


def _proto_fingerprint(proto: dict[str, Any]) -> str:
    """Fingerprint technical limitation content without support-witness metadata."""
    return canonical_json([
        proto.get("element_role"),
        proto.get("text"),
        proto.get("relationship_type"),
        proto.get("parameter_scope"),
        proto.get("essentiality"),
        proto.get("upstream_entity_ids", []),
    ])


def _merge_proto_support(target: dict[str, Any], source: dict[str, Any]) -> None:
    if target["text"] != source["text"] or target["element_role"] != source["element_role"]:
        return
    for key in ("source_paths", "evidence_ids", "specification_section_ids", "upstream_entity_ids"):
        target[key] = _unique([*target[key], *source[key]])
    seen = {canonical_json(item) for item in target["specification_support_refs"]}
    for item in source["specification_support_refs"]:
        key = canonical_json(item)
        if key not in seen:
            target["specification_support_refs"].append(deepcopy(item))
            seen.add(key)


def _paragraph_index(specification: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for section_index, section in enumerate(specification["sections"]):
        if section["section_id"] not in POSITIVE_SECTIONS:
            continue
        for paragraph_index, paragraph in enumerate(section["paragraphs"]):
            support = paragraph["support"]
            if support["grounding_class"] not in GROUNDING_ELIGIBLE:
                continue
            for reconstruction_path in support["source_paths"]:
                result[reconstruction_path].append({
                    "section_id": section["section_id"],
                    "paragraph_id": paragraph["paragraph_id"],
                    "specification_path": f"/sections/{section_index}/paragraphs/{paragraph_index}",
                    "reconstruction_path": reconstruction_path,
                    "evidence_ids": deepcopy(support["evidence_ids"]),
                })
    return result


def _id_and_path_indexes(model: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, str]]:
    objects: dict[str, dict[str, Any]] = {}
    paths: dict[str, str] = {}
    groups = (
        "solution_concepts", "elements", "relationships", "method_steps", "flows",
        "parameters", "technical_effects", "embodiments", "variants",
    )
    for group in groups:
        for index, obj in enumerate(model[group]):
            identifier = _entity_id(obj)
            if identifier:
                objects[identifier] = obj
                paths[identifier] = f"/invention_model/{group}/{index}"
    return objects, paths


def _reference_graph(model: dict[str, Any]) -> dict[str, set[str]]:
    graph: dict[str, set[str]] = defaultdict(set)

    def forward(owner: str, refs: Iterable[str]) -> None:
        for ref in refs:
            graph[owner].add(ref)

    def dependent(owner: str, refs: Iterable[str]) -> None:
        for ref in refs:
            graph[ref].add(owner)

    for x in model["solution_concepts"]:
        # A conflict on the selected solution taints the units it declares as
        # part of that solution. A conflict on an optional child must not flow
        # back through the solution container and contaminate required siblings.
        forward(x["solution_id"], [*x["related_element_ids"], *x["related_step_ids"]])
    for x in model["relationships"]:
        dependent(x["relationship_id"], [x["subject_id"], x["object_id"]])
    for x in model["method_steps"]:
        dependent(x["step_id"], [*x["input_element_ids"], *x["output_element_ids"], *x["dependency_step_ids"]])
    for x in model["flows"]:
        dependent(x["flow_id"], [x["source_id"], x["target_id"]])
    for x in model["parameters"]:
        dependent(x["parameter_id"], x["related_entity_ids"])
    for x in model["technical_effects"]:
        dependent(x["effect_id"], [*x["related_solution_ids"], *x["related_element_ids"]])
    for x in model["embodiments"]:
        dependent(x["embodiment_id"], [*x["element_ids"], *x["method_step_ids"], *x["parameter_ids"]])
    for x in model["variants"]:
        dependent(x["variant_id"], x["base_entity_ids"])
    return graph


def _conflict_taint(reconstruction: dict[str, Any]) -> set[str]:
    seeds = {
        identifier
        for conflict in reconstruction["review_package"]["conflicts"]
        if conflict["status"] == "UNRESOLVED"
        for identifier in conflict["affected_entity_ids"]
    }
    graph = _reference_graph(reconstruction["invention_model"])
    tainted = set(seeds)
    queue = deque(seeds)
    while queue:
        current = queue.popleft()
        for adjacent in graph.get(current, ()):
            if adjacent not in tainted:
                tainted.add(adjacent)
                queue.append(adjacent)
    return tainted


def _support_bundle(
    components: list[tuple[dict[str, Any], str, str]],
    *,
    evidence: dict[str, dict[str, Any]],
    paragraph_index: dict[str, list[dict[str, Any]]],
) -> tuple[dict[str, Any] | None, str | None]:
    source_paths: list[str] = []
    evidence_ids: list[str] = []
    entity_ids: list[str] = []
    groundings: list[str] = []
    refs: list[dict[str, Any]] = []
    technical_strings: list[str] = []
    for obj, path, kind in components:
        support = _support(obj)
        if support is None or support.get("grounding_class") not in GROUNDING_ELIGIBLE:
            return None, "CLAIM_ELEMENT_GROUNDING_INELIGIBLE"
        ids = support["evidence_ids"]
        if not ids or any(x not in evidence for x in ids):
            return None, "CLAIM_EVIDENCE_NOT_FOUND"
        strings = _technical_strings(obj, kind)
        if any(prohibited_text(x) for x in strings):
            return None, "PROHIBITED_CLAIM_CONTENT"
        if not _literal_support(obj, kind, ids, evidence):
            return None, "CLAIM_EVIDENCE_NOT_FOUND"
        witnesses = [x for x in paragraph_index.get(path, []) if set(ids).issubset(x["evidence_ids"])]
        if not witnesses:
            return None, "CLAIM_SPECIFICATION_SUPPORT_NOT_FOUND"
        source_paths.append(path)
        evidence_ids.extend(ids)
        identifier = _entity_id(obj)
        if identifier:
            entity_ids.append(identifier)
        groundings.append(support["grounding_class"])
        refs.append(deepcopy(witnesses[0]))
        technical_strings.extend(strings)
    unique_refs: list[dict[str, Any]] = []
    seen_refs: set[str] = set()
    for ref in refs:
        key = canonical_json(ref)
        if key not in seen_refs:
            seen_refs.add(key)
            unique_refs.append(ref)
    return {
        "source_paths": _unique(source_paths),
        "evidence_ids": _unique(evidence_ids),
        "specification_section_ids": _unique(x["section_id"] for x in unique_refs),
        "specification_support_refs": unique_refs,
        "grounding": "SOURCE_FACT" if groundings and all(x == "SOURCE_FACT" for x in groundings) else "PARAPHRASE",
        "upstream_entity_ids": _unique(entity_ids),
    }, None


def _source_support_code(
    obj: dict[str, Any],
    kind: str,
    evidence: dict[str, dict[str, Any]],
) -> str | None:
    """Validate source-side claim grounding without requiring a P2-003 paragraph."""
    support = _support(obj)
    if support is None or support.get("grounding_class") not in GROUNDING_ELIGIBLE:
        return "CLAIM_ELEMENT_GROUNDING_INELIGIBLE"
    ids = support["evidence_ids"]
    if not ids or any(x not in evidence for x in ids):
        return "CLAIM_EVIDENCE_NOT_FOUND"
    strings = _technical_strings(obj, kind)
    if any(prohibited_text(x) for x in strings):
        return "PROHIBITED_CLAIM_CONTENT"
    if not _literal_support(obj, kind, ids, evidence):
        return "CLAIM_EVIDENCE_NOT_FOUND"
    return None


def _entity_fragment(element: dict[str, Any]) -> str:
    return element["name"] + (": " + element["description"] if "description" in element else "")


def _parameter_fragment(parameter: dict[str, Any]) -> str:
    value = parameter["value"]
    unit = (" " + parameter["unit"]) if parameter.get("unit") else ""
    if value["value_kind"] == "EXACT":
        rendered = canonical_json(value["exact_value"])
        return f"{parameter['name']} has value {rendered}{unit}"
    if value["value_kind"] == "RANGE":
        return f"{parameter['name']} has value from {canonical_json(value['minimum'])} to {canonical_json(value['maximum'])}{unit}"
    if value["value_kind"] == "SET":
        return f"{parameter['name']} has values {canonical_json(value['values'])}{unit}"
    return f"{parameter['name']} has value {parameter['value']['qualitative_value']}{unit}"


def _element_proto(
    text: str,
    role: str,
    bundle: dict[str, Any],
    essentiality: str,
    *,
    parameter_scope: str | None = None,
    relationship_type: str | None = None,
) -> dict[str, Any]:
    result = {
        "text": text,
        "element_role": role,
        **deepcopy(bundle),
        "support_status": "SUPPORTED",
        "essentiality": essentiality,
    }
    if parameter_scope is not None:
        result["parameter_scope"] = parameter_scope
    if relationship_type is not None:
        result["relationship_type"] = relationship_type
    return result


def _issue(
    family_id: str,
    code: str,
    *,
    entity_ids: Iterable[str] = (),
    source_paths: Iterable[str] = (),
    specification_paths: Iterable[str] = (),
    evidence_ids: Iterable[str] = (),
    missing_ids: Iterable[str] = (),
    author_question_ids: Iterable[str] = (),
) -> dict[str, Any]:
    return {
        "code": code,
        "family_id": family_id,
        "entity_ids": _unique(entity_ids),
        "source_paths": _unique(source_paths),
        "specification_paths": _unique(specification_paths),
        "evidence_ids": _unique(evidence_ids),
        "missing_ids": _unique(missing_ids),
        "author_question_ids": _unique(author_question_ids),
        "support_status": "HUMAN_CONFIRMATION_REQUIRED" if code in {
            "INSUFFICIENT_INDEPENDENT_CLAIM_SUPPORT", "METHOD_STEP_ESSENTIALITY_UNAVAILABLE",
            "COMPOSITION_SEMANTICS_UNAVAILABLE", "PARAMETER_ESSENTIALITY_UNAVAILABLE",
            "UNRESOLVED_RECONSTRUCTION_CONFLICT", "UNROUTED_UPSTREAM_GAP",
            "REQUIRED_UPSTREAM_INFORMATION_MISSING",
        } else "UNSUPPORTED",
        "message": ISSUE_MESSAGES[code],
    }


def _claim_text(claim_type: str, number: int, dependent: bool, local: list[dict[str, Any]]) -> str:
    noun = "system" if claim_type == "SYSTEM" else "apparatus"
    if dependent:
        text = f"The {noun} of claim {number}, wherein " + "; ".join(x["text"] for x in local)
    else:
        article = "A" if claim_type == "SYSTEM" else "An"
        text = f"{article} {noun} comprising: " + "; ".join(x["text"] for x in local)
    if not text.endswith((".", "!", "?")):
        text += "."
    return text


def _allocate_claim(
    claim_number: int,
    claim_type: str,
    family_id: str,
    local_protos: list[dict[str, Any]],
    element_counter: list[int],
    *,
    parent: dict[str, Any] | None = None,
) -> dict[str, Any]:
    elements: list[dict[str, Any]] = []
    if parent is not None:
        for parent_element in parent["claim_elements"]:
            element_counter[0] += 1
            clone = deepcopy(parent_element)
            clone["element_id"] = f"CE-P2-004-{element_counter[0]:04d}"
            clone["sequence"] = len(elements) + 1
            clone["inherited_from_element_id"] = parent_element["element_id"]
            elements.append(clone)
    local_elements: list[dict[str, Any]] = []
    for proto in local_protos:
        element_counter[0] += 1
        element = deepcopy(proto)
        element["element_id"] = f"CE-P2-004-{element_counter[0]:04d}"
        element["sequence"] = len(elements) + 1
        element["inherited_from_element_id"] = None
        elements.append(element)
        local_elements.append(element)
    dependent = parent is not None
    parent_number = parent["claim_number"] if parent is not None else claim_number
    return {
        "claim_number": claim_number,
        "claim_type": claim_type,
        "independent_or_dependent": "DEPENDENT" if dependent else "INDEPENDENT",
        "depends_on": [parent_number] if dependent else [],
        "claim_text": _claim_text(claim_type, parent_number, dependent, local_elements),
        "claim_elements": elements,
        "claim_family_id": family_id,
        "review_status": "UNREVIEWED",
    }


def _blocking_gaps(
    reconstruction: dict[str, Any],
    relevant_paths: set[str],
) -> tuple[list[dict[str, Any]], bool]:
    routed: list[dict[str, Any]] = []
    unrouted = False
    known_entity_paths = {
        f"/invention_model/{group}/{index}"
        for group in (
            "solution_concepts", "elements", "relationships", "method_steps", "flows",
            "parameters", "technical_effects", "embodiments", "variants",
        )
        for index, _ in enumerate(reconstruction["invention_model"][group])
    }
    for missing in reconstruction["review_package"]["missing_information"]:
        if missing["impact"] not in {"BLOCKING", "HIGH"}:
            continue
        target = missing["target_path"]
        if not target.startswith("/invention_model/"):
            continue
        if any(target == path or target.startswith(path + "/") for path in relevant_paths):
            routed.append(missing)
            continue
        # A technical path which cannot be resolved to a known model unit is
        # deliberately treated as unrouted rather than guessed irrelevant.
        if not any(target == path or target.startswith(path + "/") for path in known_entity_paths):
            unrouted = True
    return routed, unrouted


def _family_structural(
    claim_type: str,
    family_id: str,
    reconstruction: dict[str, Any],
    specification: dict[str, Any],
    config: dict[str, Any],
    objects: dict[str, dict[str, Any]],
    paths: dict[str, str],
    tainted: set[str],
    paragraph_index: dict[str, list[dict[str, Any]]],
    evidence: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]] | None, list[list[dict[str, Any]]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], str]:
    issues: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    missing_out: list[dict[str, Any]] = []
    questions_out: list[dict[str, Any]] = []
    model = reconstruction["invention_model"]
    solution = objects[config["selected_solution_id"]]
    related = [objects[x] for x in solution["related_element_ids"]]
    related_paths = {paths[x["element_id"]] for x in related} | {paths[solution["solution_id"]]}

    direct_conflicts = {
        identifier
        for conflict in reconstruction["review_package"]["conflicts"]
        if conflict["status"] == "UNRESOLVED"
        for identifier in conflict["affected_entity_ids"]
    }
    if solution["solution_id"] in direct_conflicts or any(x["element_id"] in tainted and x["essentiality"] == "ESSENTIAL" for x in related):
        issues.append(_issue(family_id, "UNRESOLVED_RECONSTRUCTION_CONFLICT", entity_ids=[solution["solution_id"]], source_paths=[paths[solution["solution_id"]]]))
        return None, [], issues, warnings, missing_out, questions_out, "HUMAN_CONFIRMATION_REQUIRED"
    if any(x["essentiality"] == "UNKNOWN" for x in related):
        unknown = [x for x in related if x["essentiality"] == "UNKNOWN"]
        issues.append(_issue(family_id, "INSUFFICIENT_INDEPENDENT_CLAIM_SUPPORT", entity_ids=[x["element_id"] for x in unknown], source_paths=[paths[x["element_id"]] for x in unknown]))
        return None, [], issues, warnings, missing_out, questions_out, "HUMAN_CONFIRMATION_REQUIRED"

    core = [x for x in related if x["essentiality"] == "ESSENTIAL"]
    if not core:
        issues.append(_issue(family_id, "INSUFFICIENT_INDEPENDENT_CLAIM_SUPPORT", entity_ids=[x["element_id"] for x in core], source_paths=[paths[x["element_id"]] for x in core]))
        return None, [], issues, warnings, missing_out, questions_out, "HUMAN_CONFIRMATION_REQUIRED"

    nonstructural = [x for x in core if x["element_type"] not in STRUCTURAL_ELEMENT_TYPES]
    if nonstructural:
        # NOT_GENERATED is intentionally narrow: only a fully supported ESSENTIAL
        # core that is wholly and demonstrably outside the released structural
        # taxonomy qualifies. Mixed or unsupported cores still require Human
        # confirmation rather than a type inference.
        demonstrably_nonstructural = len(nonstructural) == len(core)
        if demonstrably_nonstructural:
            solution_probe, solution_code = _support_bundle(
                [(solution, paths[solution["solution_id"]], "solution")],
                evidence=evidence,
                paragraph_index=paragraph_index,
            )
            if solution_code:
                demonstrably_nonstructural = False
            else:
                for element in core:
                    _, element_code = _support_bundle(
                        [(element, paths[element["element_id"]], "element")],
                        evidence=evidence,
                        paragraph_index=paragraph_index,
                    )
                    if element_code:
                        demonstrably_nonstructural = False
                        break
        issues.append(_issue(
            family_id,
            "CLAIM_ELEMENT_UNSUPPORTED" if demonstrably_nonstructural else "INSUFFICIENT_INDEPENDENT_CLAIM_SUPPORT",
            entity_ids=[x["element_id"] for x in nonstructural],
            source_paths=[paths[x["element_id"]] for x in nonstructural],
            evidence_ids=_support_evidence_ids(nonstructural),
        ))
        return (
            None, [], issues, warnings, missing_out, questions_out,
            "NOT_GENERATED" if demonstrably_nonstructural else "HUMAN_CONFIRMATION_REQUIRED",
        )

    core_ids = {x["element_id"] for x in core}
    core_relationships = [
        x for x in model["relationships"]
        if x["subject_id"] in core_ids and x["object_id"] in core_ids
    ]
    core_rel_ids = {x["relationship_id"] for x in core_relationships}
    tainted_core_relationships = [x for x in core_relationships if x["relationship_id"] in tainted]
    if tainted_core_relationships:
        issues.append(_issue(
            family_id,
            "UNRESOLVED_RECONSTRUCTION_CONFLICT",
            entity_ids=[x["relationship_id"] for x in tainted_core_relationships],
            source_paths=[paths[x["relationship_id"]] for x in tainted_core_relationships],
            evidence_ids=_support_evidence_ids(tainted_core_relationships),
        ))
        return None, [], issues, warnings, missing_out, questions_out, "HUMAN_CONFIRMATION_REQUIRED"
    for parameter in model["parameters"]:
        if set(parameter["related_entity_ids"]) & (core_ids | core_rel_ids | {solution["solution_id"]}):
            issues.append(_issue(
                family_id,
                "PARAMETER_ESSENTIALITY_UNAVAILABLE",
                entity_ids=[parameter["parameter_id"]],
                source_paths=[paths[parameter["parameter_id"]]],
                evidence_ids=_support_evidence_ids([parameter]),
            ))
            return None, [], issues, warnings, missing_out, questions_out, "HUMAN_CONFIRMATION_REQUIRED"

    routed_gaps, unrouted = _blocking_gaps(reconstruction, related_paths | {paths[x["relationship_id"]] for x in core_relationships})
    if routed_gaps or unrouted:
        question_by_missing = {
            q["missing_information_id"]: q for q in reconstruction["review_package"]["author_questions"]
        }
        for gap in routed_gaps:
            mi_id = f"MI-P2-004-{len(missing_out)+1:04d}"
            q_id = f"AQ-P2-004-{len(questions_out)+1:04d}"
            missing_out.append({"missing_id": mi_id, "family_id": family_id, "source_paths": [gap["target_path"]], "reason": "Required upstream technical information is missing.", "question_ids": [q_id]})
            questions_out.append({"question_id": q_id, "family_id": family_id, "missing_id": mi_id, "question": "Please confirm the upstream technical information required for this claim family.", "status": "OPEN"})
            upstream_q = question_by_missing.get(gap["missing_id"])
            issues.append(_issue(family_id, "REQUIRED_UPSTREAM_INFORMATION_MISSING", source_paths=[gap["target_path"]], missing_ids=[mi_id], author_question_ids=[q_id, *([upstream_q["question_id"]] if upstream_q else [])]))
        if unrouted:
            issues.append(_issue(family_id, "UNROUTED_UPSTREAM_GAP", source_paths=[paths[solution["solution_id"]]]))
        return None, [], issues, warnings, missing_out, questions_out, "HUMAN_CONFIRMATION_REQUIRED"

    independent: list[dict[str, Any]] = []
    for element in core:
        path = paths[element["element_id"]]
        bundle, code = _support_bundle([(element, path, "element")], evidence=evidence, paragraph_index=paragraph_index)
        if code:
            issues.append(_issue(family_id, code, entity_ids=[element["element_id"]], source_paths=[path]))
            return None, [], issues, warnings, missing_out, questions_out, "HUMAN_CONFIRMATION_REQUIRED"
        independent.append(_element_proto(_entity_fragment(element), "ENTITY", bundle, "ESSENTIAL"))

    _, code = _support_bundle(
        [(solution, paths[solution["solution_id"]], "solution")],
        evidence=evidence,
        paragraph_index=paragraph_index,
    )
    if code:
        # P2-003 suppresses a solution paragraph when any referenced child is
        # blocked. P2-004 may retain a structurally complete core only when the
        # solution itself is source-eligible and an excluded optional/conditional
        # child explains that suppression. Required core disclosure was already
        # verified above, so this cannot rescue a bad core or invent disclosure.
        optional_exclusion_explains_missing_solution = False
        if code == "CLAIM_SPECIFICATION_SUPPORT_NOT_FOUND" and _source_support_code(solution, "solution", evidence) is None:
            for candidate in related:
                if candidate["essentiality"] not in {"OPTIONAL", "CONDITIONAL"}:
                    continue
                candidate_code = _source_support_code(candidate, "element", evidence)
                if candidate["element_id"] in tainted or candidate_code is not None:
                    optional_exclusion_explains_missing_solution = True
                    break
        if not optional_exclusion_explains_missing_solution:
            issues.append(_issue(family_id, code, entity_ids=[solution["solution_id"]], source_paths=[paths[solution["solution_id"]]]))
            return None, [], issues, warnings, missing_out, questions_out, "HUMAN_CONFIRMATION_REQUIRED"

    graph: dict[str, set[str]] = defaultdict(set)
    for relation in core_relationships:
        subject, obj = objects[relation["subject_id"]], objects[relation["object_id"]]
        relation_path = paths[relation["relationship_id"]]
        if not _relationship_literal_support(relation, subject, obj, evidence):
            issues.append(_issue(
                family_id,
                "CLAIM_EVIDENCE_NOT_FOUND",
                entity_ids=[relation["relationship_id"]],
                source_paths=[relation_path],
                evidence_ids=_support_evidence_ids([relation]),
            ))
            return None, [], issues, warnings, missing_out, questions_out, "HUMAN_CONFIRMATION_REQUIRED"
        components = [
            (relation, relation_path, "relationship"),
            (subject, paths[subject["element_id"]], "element"),
            (obj, paths[obj["element_id"]], "element"),
        ]
        bundle, code = _support_bundle(components, evidence=evidence, paragraph_index=paragraph_index)
        if code:
            issues.append(_issue(family_id, code, entity_ids=[relation["relationship_id"]], source_paths=[relation_path]))
            return None, [], issues, warnings, missing_out, questions_out, "HUMAN_CONFIRMATION_REQUIRED"
        graph[relation["subject_id"]].add(relation["object_id"])
        graph[relation["object_id"]].add(relation["subject_id"])
        independent.append(_element_proto(
            f"{subject['name']} {RELATION_WORDING[relation['relation_type']]} {obj['name']}",
            "RELATIONSHIP", bundle, "NOT_APPLICABLE", relationship_type=relation["relation_type"],
        ))
    if len(core_ids) > 1:
        seen = {next(iter(core_ids))}
        queue = deque(seen)
        while queue:
            current = queue.popleft()
            for adjacent in graph[current]:
                if adjacent not in seen:
                    seen.add(adjacent)
                    queue.append(adjacent)
        if seen != core_ids:
            issues.append(_issue(family_id, "INSUFFICIENT_INDEPENDENT_CLAIM_SUPPORT", entity_ids=sorted(core_ids), source_paths=[paths[x] for x in sorted(core_ids)]))
            return None, [], issues, warnings, missing_out, questions_out, "HUMAN_CONFIRMATION_REQUIRED"

    candidates: list[dict[str, Any]] = []

    def add_candidate(
        priority: int,
        order: int,
        logical_id: str,
        components: list[tuple[dict[str, Any], str, str]],
        delta: list[dict[str, Any]],
        identifiers: list[str],
    ) -> None:
        candidates.append({
            "priority": priority,
            "order": order,
            "logical_id": logical_id,
            "path": paths[logical_id],
            "fingerprint": _limitation_fingerprint(components),
            "delta": delta,
            "identifiers": identifiers,
            "evidence_ids": _support_evidence_ids(obj for obj, _, _ in components),
        })

    for element in related:
        if element["essentiality"] not in {"OPTIONAL", "CONDITIONAL"}:
            continue
        eid = element["element_id"]
        path = paths[eid]
        if eid in tainted:
            issues.append(_issue(
                family_id, "CLAIM_ELEMENT_CONFLICT_TAINTED",
                entity_ids=[eid], source_paths=[path], evidence_ids=_support_evidence_ids([element]),
            ))
            continue
        if element["element_type"] not in STRUCTURAL_ELEMENT_TYPES:
            issues.append(_issue(
                family_id, "CLAIM_ELEMENT_UNSUPPORTED",
                entity_ids=[eid], source_paths=[path], evidence_ids=_support_evidence_ids([element]),
            ))
            continue
        if element["essentiality"] == "CONDITIONAL" and (
            "description" not in element or CONDITION_MARKERS.search(element["description"]) is None
        ):
            issues.append(_issue(
                family_id, "CLAIM_ELEMENT_UNSUPPORTED",
                entity_ids=[eid], source_paths=[path], evidence_ids=_support_evidence_ids([element]),
            ))
            continue
        linked_parameters = [x for x in model["parameters"] if eid in x["related_entity_ids"]]
        parameter_code = None
        for parameter in linked_parameters:
            if parameter["scope_status"] == "EXAMPLE_ONLY":
                parameter_code = "CLAIM_EXAMPLE_SCOPE_INELIGIBLE"
                break
            if parameter["scope_status"] == "UNKNOWN_SCOPE":
                parameter_code = "CLAIM_UNKNOWN_SCOPE_INELIGIBLE"
                break
            if parameter["role"] not in PARAMETER_ROLES:
                parameter_code = "CLAIM_ELEMENT_UNSUPPORTED"
                break
        if parameter_code:
            issues.append(_issue(
                family_id,
                parameter_code,
                entity_ids=[eid, *[x["parameter_id"] for x in linked_parameters]],
                source_paths=[path, *[paths[x["parameter_id"]] for x in linked_parameters]],
                evidence_ids=_support_evidence_ids([element, *linked_parameters]),
            ))
            continue

        components = [(element, path, "element")]
        relation_group = [
            x for x in model["relationships"]
            if (x["subject_id"] == eid and x["object_id"] in core_ids)
            or (x["object_id"] == eid and x["subject_id"] in core_ids)
        ]
        components.extend((x, paths[x["relationship_id"]], "relationship") for x in relation_group)
        components.extend((x, paths[x["parameter_id"]], "parameter") for x in linked_parameters)
        bundle, code = _support_bundle(components, evidence=evidence, paragraph_index=paragraph_index)
        if code:
            issues.append(_issue(
                family_id, code, entity_ids=[eid], source_paths=[path],
                evidence_ids=_support_evidence_ids(obj for obj, _, _ in components),
            ))
            continue
        role = "CONDITIONAL_UNIT" if element["essentiality"] == "CONDITIONAL" else "ENTITY"
        text = element["description"] if role == "CONDITIONAL_UNIT" and "description" in element else _entity_fragment(element)
        delta = [_element_proto(text, role, bundle, element["essentiality"])]
        for relation in relation_group:
            subject, obj = objects[relation["subject_id"]], objects[relation["object_id"]]
            if not _relationship_literal_support(relation, subject, obj, evidence):
                delta = []
                issues.append(_issue(
                    family_id, "CLAIM_EVIDENCE_NOT_FOUND",
                    entity_ids=[relation["relationship_id"]],
                    source_paths=[paths[relation["relationship_id"]]],
                    evidence_ids=_support_evidence_ids([relation]),
                ))
                break
            r_bundle, r_code = _support_bundle([
                (relation, paths[relation["relationship_id"]], "relationship"),
                (subject, paths[subject["element_id"]], "element"),
                (obj, paths[obj["element_id"]], "element"),
            ], evidence=evidence, paragraph_index=paragraph_index)
            if r_code:
                delta = []
                issues.append(_issue(
                    family_id, r_code, entity_ids=[relation["relationship_id"]],
                    source_paths=[paths[relation["relationship_id"]]], evidence_ids=_support_evidence_ids([relation]),
                ))
                break
            delta.append(_element_proto(
                f"{subject['name']} {RELATION_WORDING[relation['relation_type']]} {obj['name']}",
                "RELATIONSHIP", r_bundle, "NOT_APPLICABLE", relationship_type=relation["relation_type"],
            ))
        if not delta:
            continue
        for parameter in linked_parameters:
            p_bundle, p_code = _support_bundle([(parameter, paths[parameter["parameter_id"]], "parameter")], evidence=evidence, paragraph_index=paragraph_index)
            if p_code:
                delta = []
                issues.append(_issue(
                    family_id, p_code, entity_ids=[parameter["parameter_id"]],
                    source_paths=[paths[parameter["parameter_id"]]], evidence_ids=_support_evidence_ids([parameter]),
                ))
                break
            delta.append(_element_proto(_parameter_fragment(parameter), "PARAMETER", p_bundle, "NOT_APPLICABLE", parameter_scope=parameter["scope_status"]))
        if delta:
            priority = 1 if element["essentiality"] == "OPTIONAL" else 2
            element_order = next(index for index, item in enumerate(model["elements"]) if item["element_id"] == eid)
            add_candidate(priority, element_order, eid, components, delta, [eid, *[x["parameter_id"] for x in linked_parameters]])

            # Category 4 is the same complete entity/parameter closure.  It is
            # retained as an explicit candidate so canonical fingerprinting,
            # rather than ad-hoc text comparison, owns duplicate elimination.
            if linked_parameters:
                parameter_order = min(
                    index for index, item in enumerate(model["parameters"])
                    if item["parameter_id"] in {x["parameter_id"] for x in linked_parameters}
                )
                add_candidate(4, parameter_order, eid, components, deepcopy(delta), [eid, *[x["parameter_id"] for x in linked_parameters]])

    # Priority 3: a relationship may form one indivisible structural delta when
    # both non-parent endpoints are introduced together.  Core-to-core
    # relationships are already mandatory independent content; optional-to-core
    # links are already carried by the priority-1/2 entity closure above.
    related_by_id = {x["element_id"]: x for x in related}
    for relationship_order, relation in enumerate(model["relationships"]):
        rid = relation["relationship_id"]
        if rid in core_rel_ids:
            continue
        endpoint_ids = {relation["subject_id"], relation["object_id"]}
        if not endpoint_ids.issubset(related_by_id):
            continue
        if endpoint_ids & core_ids:
            continue
        endpoints = [related_by_id[relation["subject_id"]], related_by_id[relation["object_id"]]]
        if any(
            x["essentiality"] not in {"OPTIONAL", "CONDITIONAL"}
            or x["element_type"] not in STRUCTURAL_ELEMENT_TYPES
            or x["element_id"] in tainted
            for x in endpoints
        ):
            continue
        if any(
            x["essentiality"] == "CONDITIONAL"
            and ("description" not in x or CONDITION_MARKERS.search(x["description"]) is None)
            for x in endpoints
        ):
            continue

        delta_ids = {x["element_id"] for x in endpoints}
        relation_group = [
            x for x in model["relationships"]
            if (
                x["subject_id"] in delta_ids and x["object_id"] in (delta_ids | core_ids)
            ) or (
                x["object_id"] in delta_ids and x["subject_id"] in (delta_ids | core_ids)
            )
        ]
        linked_parameters = [
            x for x in model["parameters"]
            if set(x["related_entity_ids"]) & delta_ids
        ]
        if any(
            p["scope_status"] != "SUPPORTED_RANGE" or p["role"] not in PARAMETER_ROLES
            for p in linked_parameters
        ):
            continue

        components: list[tuple[dict[str, Any], str, str]] = []
        components.extend((x, paths[x["element_id"]], "element") for x in endpoints)
        components.extend((x, paths[x["relationship_id"]], "relationship") for x in relation_group)
        components.extend((x, paths[x["parameter_id"]], "parameter") for x in linked_parameters)
        bundle, code = _support_bundle(components, evidence=evidence, paragraph_index=paragraph_index)
        if code:
            issues.append(_issue(
                family_id, code,
                entity_ids=[rid, *sorted(delta_ids)],
                source_paths=[paths[rid]],
                evidence_ids=_support_evidence_ids(obj for obj, _, _ in components),
            ))
            continue
        if any(
            not _relationship_literal_support(x, objects[x["subject_id"]], objects[x["object_id"]], evidence)
            for x in relation_group
        ):
            issues.append(_issue(
                family_id, "CLAIM_EVIDENCE_NOT_FOUND",
                entity_ids=[rid, *sorted(delta_ids)],
                source_paths=[paths[rid]],
                evidence_ids=_support_evidence_ids(relation_group),
            ))
            continue

        delta: list[dict[str, Any]] = []
        for endpoint in endpoints:
            role = "CONDITIONAL_UNIT" if endpoint["essentiality"] == "CONDITIONAL" else "ENTITY"
            text = endpoint["description"] if role == "CONDITIONAL_UNIT" else _entity_fragment(endpoint)
            endpoint_bundle, endpoint_code = _support_bundle(
                [(endpoint, paths[endpoint["element_id"]], "element")],
                evidence=evidence,
                paragraph_index=paragraph_index,
            )
            if endpoint_code:
                delta = []
                break
            delta.append(_element_proto(text, role, endpoint_bundle, endpoint["essentiality"]))
        if not delta:
            continue
        for linked_relation in relation_group:
            subject = objects[linked_relation["subject_id"]]
            obj = objects[linked_relation["object_id"]]
            r_bundle, r_code = _support_bundle([
                (linked_relation, paths[linked_relation["relationship_id"]], "relationship"),
                (subject, paths[subject["element_id"]], "element"),
                (obj, paths[obj["element_id"]], "element"),
            ], evidence=evidence, paragraph_index=paragraph_index)
            if r_code:
                delta = []
                break
            delta.append(_element_proto(
                f"{subject['name']} {RELATION_WORDING[linked_relation['relation_type']]} {obj['name']}",
                "RELATIONSHIP", r_bundle, "NOT_APPLICABLE",
                relationship_type=linked_relation["relation_type"],
            ))
        if not delta:
            continue
        for parameter in linked_parameters:
            p_bundle, p_code = _support_bundle(
                [(parameter, paths[parameter["parameter_id"]], "parameter")],
                evidence=evidence,
                paragraph_index=paragraph_index,
            )
            if p_code:
                delta = []
                break
            delta.append(_element_proto(
                _parameter_fragment(parameter), "PARAMETER", p_bundle, "NOT_APPLICABLE",
                parameter_scope=parameter["scope_status"],
            ))
        if delta:
            add_candidate(
                3, relationship_order, rid, components, delta,
                [rid, *[x["element_id"] for x in endpoints], *[x["parameter_id"] for x in linked_parameters]],
            )

    # Priority 5: explicit embodiments.  A v1 embodiment may reference the
    # structural parent plus a supported optional/conditional delta, but never a
    # method step or an unsupported quantitative qualifier.
    for embodiment_order, embodiment in enumerate(model["embodiments"]):
        emb_id = embodiment["embodiment_id"]
        emb_path = paths[emb_id]
        if embodiment["disclosure_status"] != "EXPLICIT":
            issues.append(_issue(
                family_id, "CLAIM_ELEMENT_GROUNDING_INELIGIBLE",
                entity_ids=[emb_id], source_paths=[emb_path], evidence_ids=_support_evidence_ids([embodiment]),
            ))
            continue
        if emb_id in tainted or embodiment["method_step_ids"]:
            code = "CLAIM_ELEMENT_CONFLICT_TAINTED" if emb_id in tainted else "CLAIM_ELEMENT_UNSUPPORTED"
            issues.append(_issue(
                family_id, code, entity_ids=[emb_id], source_paths=[emb_path], evidence_ids=_support_evidence_ids([embodiment]),
            ))
            continue
        extra_elements: list[dict[str, Any]] = []
        eligible = True
        for element_id in embodiment["element_ids"]:
            if element_id in core_ids:
                continue
            candidate_element = objects.get(element_id)
            if (
                candidate_element is None
                or candidate_element not in related
                or candidate_element.get("essentiality") not in {"OPTIONAL", "CONDITIONAL"}
                or candidate_element.get("element_type") not in STRUCTURAL_ELEMENT_TYPES
                or element_id in tainted
            ):
                eligible = False
                break
            if candidate_element["essentiality"] == "CONDITIONAL" and (
                "description" not in candidate_element
                or CONDITION_MARKERS.search(candidate_element["description"]) is None
            ):
                eligible = False
                break
            extra_elements.append(candidate_element)
        referenced_parameters = [objects[x] for x in embodiment["parameter_ids"] if x in objects]
        if len(referenced_parameters) != len(embodiment["parameter_ids"]):
            eligible = False
        if any(
            parameter["scope_status"] != "SUPPORTED_RANGE" or parameter["role"] not in PARAMETER_ROLES
            for parameter in referenced_parameters
        ):
            eligible = False
        if not eligible:
            issues.append(_issue(
                family_id, "CLAIM_ELEMENT_UNSUPPORTED",
                entity_ids=[emb_id, *embodiment["element_ids"], *embodiment["parameter_ids"]],
                source_paths=[emb_path], evidence_ids=_support_evidence_ids([embodiment, *extra_elements, *referenced_parameters]),
            ))
            continue
        extra_ids = {x["element_id"] for x in extra_elements}
        relationship_group = [
            x for x in model["relationships"]
            if (
                x["subject_id"] in extra_ids and x["object_id"] in (extra_ids | core_ids)
            ) or (
                x["object_id"] in extra_ids and x["subject_id"] in (extra_ids | core_ids)
            )
        ]
        referenced_parameter_ids = set(embodiment["parameter_ids"])
        referenced_parameter_ids.update(
            parameter["parameter_id"]
            for parameter in model["parameters"]
            if set(parameter["related_entity_ids"]) & extra_ids
        )
        referenced_parameters = [
            parameter for parameter in model["parameters"]
            if parameter["parameter_id"] in referenced_parameter_ids
        ]
        closure_ids = core_ids | extra_ids | {x["relationship_id"] for x in relationship_group} | {emb_id}
        if (
            len(referenced_parameters) != len(referenced_parameter_ids)
            or any(
                parameter["scope_status"] != "SUPPORTED_RANGE"
                or parameter["role"] not in PARAMETER_ROLES
                or not set(parameter["related_entity_ids"]).issubset(closure_ids)
                for parameter in referenced_parameters
            )
            or any(x["relationship_id"] in tainted for x in relationship_group)
        ):
            issues.append(_issue(
                family_id, "CLAIM_ELEMENT_UNSUPPORTED",
                entity_ids=[emb_id, *sorted(extra_ids), *sorted(referenced_parameter_ids)],
                source_paths=[emb_path],
                evidence_ids=_support_evidence_ids([embodiment, *extra_elements, *relationship_group, *referenced_parameters]),
            ))
            continue

        emb_components: list[tuple[dict[str, Any], str, str]] = [(embodiment, emb_path, "embodiment")]
        emb_components.extend((x, paths[x["element_id"]], "element") for x in extra_elements)
        emb_components.extend((x, paths[x["relationship_id"]], "relationship") for x in relationship_group)
        emb_components.extend((x, paths[x["parameter_id"]], "parameter") for x in referenced_parameters)
        emb_bundle, emb_code = _support_bundle(emb_components, evidence=evidence, paragraph_index=paragraph_index)
        if emb_code:
            issues.append(_issue(
                family_id, emb_code, entity_ids=[emb_id], source_paths=[emb_path],
                evidence_ids=_support_evidence_ids(obj for obj, _, _ in emb_components),
            ))
            continue
        if any(
            not _relationship_literal_support(x, objects[x["subject_id"]], objects[x["object_id"]], evidence)
            for x in relationship_group
        ):
            issues.append(_issue(
                family_id, "CLAIM_EVIDENCE_NOT_FOUND",
                entity_ids=[emb_id, *[x["relationship_id"] for x in relationship_group]],
                source_paths=[emb_path], evidence_ids=_support_evidence_ids(relationship_group),
            ))
            continue

        delta: list[dict[str, Any]] = []
        embodiment_only_bundle, embodiment_only_code = _support_bundle(
            [(embodiment, emb_path, "embodiment")], evidence=evidence, paragraph_index=paragraph_index,
        )
        if embodiment_only_code:
            continue
        delta.append(_element_proto(embodiment["description"], "EMBODIMENT", embodiment_only_bundle, "NOT_APPLICABLE"))
        closure_failed = False
        for element in extra_elements:
            bundle, code = _support_bundle(
                [(element, paths[element["element_id"]], "element")],
                evidence=evidence, paragraph_index=paragraph_index,
            )
            if code:
                closure_failed = True
                break
            role = "CONDITIONAL_UNIT" if element["essentiality"] == "CONDITIONAL" else "ENTITY"
            text = element["description"] if role == "CONDITIONAL_UNIT" else _entity_fragment(element)
            delta.append(_element_proto(text, role, bundle, element["essentiality"]))
        if closure_failed:
            continue
        for relation in relationship_group:
            subject, obj = objects[relation["subject_id"]], objects[relation["object_id"]]
            bundle, code = _support_bundle([
                (relation, paths[relation["relationship_id"]], "relationship"),
                (subject, paths[subject["element_id"]], "element"),
                (obj, paths[obj["element_id"]], "element"),
            ], evidence=evidence, paragraph_index=paragraph_index)
            if code:
                closure_failed = True
                break
            delta.append(_element_proto(
                f"{subject['name']} {RELATION_WORDING[relation['relation_type']]} {obj['name']}",
                "RELATIONSHIP", bundle, "NOT_APPLICABLE", relationship_type=relation["relation_type"],
            ))
        if closure_failed:
            continue
        for parameter in referenced_parameters:
            bundle, code = _support_bundle(
                [(parameter, paths[parameter["parameter_id"]], "parameter")],
                evidence=evidence, paragraph_index=paragraph_index,
            )
            if code:
                closure_failed = True
                break
            delta.append(_element_proto(
                _parameter_fragment(parameter), "PARAMETER", bundle, "NOT_APPLICABLE",
                parameter_scope=parameter["scope_status"],
            ))
        if closure_failed:
            continue
        add_candidate(
            5, embodiment_order, emb_id, emb_components, delta,
            [emb_id, *[x["element_id"] for x in extra_elements],
             *[x["relationship_id"] for x in relationship_group],
             *[x["parameter_id"] for x in referenced_parameters]],
        )

    # Priority 6: released source-supported variants only.  A variant can narrow
    # the structural parent only when every base entity already belongs to it.
    for variant_order, variant in enumerate(model["variants"]):
        variant_id = variant["variant_id"]
        variant_path = paths[variant_id]
        if not (
            variant["status"] == "SOURCE_SUPPORTED"
            and variant["filing_content_eligible"] is True
            and variant["human_confirmation_required"] is False
            and set(variant["base_entity_ids"]).issubset(core_ids)
            and variant_id not in tainted
        ):
            issues.append(_issue(
                family_id, "CLAIM_ELEMENT_GROUNDING_INELIGIBLE",
                entity_ids=[variant_id], source_paths=[variant_path], evidence_ids=_support_evidence_ids([variant]),
            ))
            continue
        variant_components = [(variant, variant_path, "variant")]
        variant_components.extend((objects[x], paths[x], "element") for x in variant["base_entity_ids"])
        variant_bundle, variant_code = _support_bundle(variant_components, evidence=evidence, paragraph_index=paragraph_index)
        if variant_code:
            issues.append(_issue(
                family_id, variant_code, entity_ids=[variant_id], source_paths=[variant_path],
                evidence_ids=_support_evidence_ids(obj for obj, _, _ in variant_components),
            ))
            continue
        add_candidate(
            6, variant_order, variant_id, variant_components,
            [_element_proto(variant["description"], "VARIANT", variant_bundle, "NOT_APPLICABLE")],
            [variant_id],
        )

    candidates.sort(key=lambda x: (x["priority"], x["order"], x["logical_id"], x["path"]))
    seen: dict[str, list[dict[str, Any]]] = {}
    parent_by_proto = {_proto_fingerprint(proto): proto for proto in independent}
    dependents: list[list[dict[str, Any]]] = []
    retained_candidates: list[dict[str, Any]] = []
    for candidate in candidates:
        fingerprint = candidate["fingerprint"]
        delta = candidate["delta"]
        delta_proto_keys = [_proto_fingerprint(proto) for proto in delta]
        if delta_proto_keys and all(key in parent_by_proto for key in delta_proto_keys):
            for proto in delta:
                _merge_proto_support(parent_by_proto[_proto_fingerprint(proto)], proto)
            warnings.append({
                "code": "DUPLICATE_LIMITATION",
                "family_id": family_id,
                "affected_ids": deepcopy(candidate["identifiers"]),
                "source_paths": [candidate["path"]],
                "message": WARNING_MESSAGES["DUPLICATE_LIMITATION"],
                "_evidence_ids": deepcopy(candidate["evidence_ids"]),
                "_sort_priority": candidate["priority"],
                "_sort_order": candidate["order"],
            })
            continue
        if fingerprint in seen:
            retained = seen[fingerprint]
            for target, source in zip(retained, delta):
                _merge_proto_support(target, source)
            warnings.append({
                "code": "DUPLICATE_LIMITATION",
                "family_id": family_id,
                "affected_ids": deepcopy(candidate["identifiers"]),
                "source_paths": [candidate["path"]],
                "message": WARNING_MESSAGES["DUPLICATE_LIMITATION"],
                "_evidence_ids": deepcopy(candidate["evidence_ids"]),
                "_sort_priority": candidate["priority"],
                "_sort_order": candidate["order"],
            })
            continue
        seen[fingerprint] = delta
        dependents.append(delta)
        retained_candidates.append(candidate)
    cap = config["max_dependent_claims_per_family"]
    if len(dependents) > cap:
        warnings.append({
            "code": "DEPENDENT_LIMIT_EXCEEDED",
            "family_id": family_id,
            "affected_ids": _unique(x for candidate in retained_candidates[cap:] for x in candidate["identifiers"]),
            "source_paths": _unique(candidate["path"] for candidate in retained_candidates[cap:]),
            "message": WARNING_MESSAGES["DEPENDENT_LIMIT_EXCEEDED"],
            "_evidence_ids": _unique(e for candidate in retained_candidates[cap:] for e in candidate["evidence_ids"]),
            "_sort_priority": retained_candidates[cap]["priority"],
            "_sort_order": retained_candidates[cap]["order"],
        })
        dependents = dependents[:cap]
    return independent, dependents, issues, warnings, missing_out, questions_out, "PRESENT"


def _build_supported_draft_claims(
    reconstruction: dict[str, Any],
    specification: dict[str, Any],
    config: dict[str, Any],
) -> dict[str, Any]:
    identity = source_identity(reconstruction, specification)
    model = reconstruction["invention_model"]
    objects, paths = _id_and_path_indexes(model)
    tainted = _conflict_taint(reconstruction)
    paragraphs = _paragraph_index(specification)
    evidence_index = {x["evidence_id"]: x for x in reconstruction["review_package"]["evidence"]}
    claims: list[dict[str, Any]] = []
    families: list[dict[str, Any]] = []
    raw_issues: list[dict[str, Any]] = []
    raw_warnings: list[dict[str, Any]] = []
    missing_information: list[dict[str, Any]] = []
    author_questions: list[dict[str, Any]] = []
    warning_evidence_ids: list[str] = []
    element_counter = [0]
    next_claim = 1

    for claim_type in config["requested_claim_types"]:
        family_id = f"CF-P2-004-{claim_type}"
        family_claims: list[dict[str, Any]] = []
        if claim_type in {"METHOD", "PROCESS"}:
            raw_issues.append(_issue(family_id, "METHOD_STEP_ESSENTIALITY_UNAVAILABLE", entity_ids=[config["selected_solution_id"]], source_paths=[paths[config["selected_solution_id"]]]))
        elif claim_type == "COMPOSITION":
            raw_issues.append(_issue(family_id, "COMPOSITION_SEMANTICS_UNAVAILABLE", entity_ids=[config["selected_solution_id"]], source_paths=[paths[config["selected_solution_id"]]]))
        else:
            independent, dependents, issues, warnings, missing, questions, family_status = _family_structural(
                claim_type, family_id, reconstruction, specification, config, objects, paths, tainted, paragraphs, evidence_index,
            )
            raw_issues.extend(issues)
            raw_warnings.extend(warnings)
            missing_information.extend(missing)
            author_questions.extend(questions)
            if independent is not None:
                parent = _allocate_claim(next_claim, claim_type, family_id, independent, element_counter)
                claims.append(parent)
                family_claims.append(parent)
                next_claim += 1
                for delta in dependents:
                    dependent = _allocate_claim(next_claim, claim_type, family_id, delta, element_counter, parent=parent)
                    claims.append(dependent)
                    family_claims.append(dependent)
                    next_claim += 1
        if claim_type in {"METHOD", "PROCESS", "COMPOSITION"}:
            family_status = "HUMAN_CONFIRMATION_REQUIRED"
        families.append({
            "claim_family_id": family_id,
            "claim_type": claim_type,
            "selected_solution_id": config["selected_solution_id"],
            "independent_claim_number": family_claims[0]["claim_number"] if family_claims else None,
            "dependent_claim_numbers": [x["claim_number"] for x in family_claims[1:]],
            "status": "PRESENT" if family_claims else family_status,
            "support_summary": {"source_paths": [], "evidence_ids": [], "specification_section_ids": [], "issue_ids": []},
            "review_status": "UNREVIEWED",
        })
        raw_warnings.append({
            "code": "HUMAN_IP_REVIEW_REQUIRED",
            "family_id": family_id,
            "affected_ids": [],
            "source_paths": [],
            "message": WARNING_MESSAGES["HUMAN_IP_REVIEW_REQUIRED"],
            "_sort_priority": 99,
            "_sort_order": 0,
        })

    family_rank = {f"CF-P2-004-{name}": i for i, name in enumerate(FAMILY_ORDER)}

    def audit_position(item: dict[str, Any]) -> tuple[int, int]:
        if "_sort_priority" in item:
            return int(item["_sort_priority"]), int(item.get("_sort_order", 0))
        if not item.get("source_paths"):
            return 0, 0
        first = item["source_paths"][0]
        parts = first.split("/")
        if len(parts) < 4 or parts[1] != "invention_model":
            return 0, 0
        group = parts[2]
        try:
            index = int(parts[3])
        except (ValueError, IndexError):
            return 0, 0
        if group == "elements" and 0 <= index < len(model["elements"]):
            essentiality = model["elements"][index]["essentiality"]
            if essentiality == "OPTIONAL":
                return 1, index
            if essentiality == "CONDITIONAL":
                return 2, index
            return 0, index
        category = {"relationships": 3, "parameters": 4, "embodiments": 5, "variants": 6}.get(group, 0)
        return category, index

    raw_issues.sort(key=lambda x: (
        family_rank[x["family_id"]], *audit_position(x), x["code"], tuple(x["source_paths"])
    ))
    issues: list[dict[str, Any]] = []
    seen_issue: set[str] = set()
    for raw in raw_issues:
        key = canonical_json([raw["code"], raw["family_id"], raw["source_paths"]])
        if key in seen_issue:
            continue
        seen_issue.add(key)
        item = deepcopy(raw)
        item.pop("_evidence_ids", None)
        item.pop("_sort_priority", None)
        item.pop("_sort_order", None)
        item["issue_id"] = f"ISS-P2-004-{len(issues)+1:04d}"
        issues.append(item)

    raw_warnings.sort(key=lambda x: (
        family_rank[x["family_id"]], *audit_position(x), x["code"], tuple(x["source_paths"])
    ))
    warnings = []
    seen_warning: set[str] = set()
    for raw in raw_warnings:
        key = canonical_json([raw["code"], raw["family_id"], raw["source_paths"]])
        if key in seen_warning:
            continue
        seen_warning.add(key)
        item = deepcopy(raw)
        warning_evidence_ids.extend(item.pop("_evidence_ids", []))
        item.pop("_sort_priority", None)
        item.pop("_sort_order", None)
        item["warning_id"] = f"W-P2-004-{len(warnings)+1:04d}"
        warnings.append(item)

    claim_support: list[dict[str, Any]] = []
    for claim in claims:
        for element in claim["claim_elements"]:
            audit = {
                "claim_number": claim["claim_number"],
                "element_id": element["element_id"],
                "support_status": "SUPPORTED",
                "source_paths": deepcopy(element["source_paths"]),
                "evidence_ids": deepcopy(element["evidence_ids"]),
                "specification_section_ids": deepcopy(element["specification_section_ids"]),
                "specification_support_refs": deepcopy(element["specification_support_refs"]),
                "upstream_entity_ids": deepcopy(element["upstream_entity_ids"]),
                "grounding": element["grounding"],
                "conflict_status": "CLEAR",
            }
            if "parameter_scope" in element:
                audit["parameter_scope"] = element["parameter_scope"]
            claim_support.append(audit)

    for family in families:
        family_claim_numbers = {x["claim_number"] for x in claims if x["claim_family_id"] == family["claim_family_id"]}
        audits = [x for x in claim_support if x["claim_number"] in family_claim_numbers]
        family_issues = [x for x in issues if x["family_id"] == family["claim_family_id"]]
        family["support_summary"] = {
            "source_paths": _unique(p for x in audits for p in x["source_paths"]),
            "evidence_ids": _unique(e for x in audits for e in x["evidence_ids"]),
            "specification_section_ids": _unique(s for x in audits for s in x["specification_section_ids"]),
            "issue_ids": [x["issue_id"] for x in family_issues],
        }

    used_evidence = _unique(
        [e for x in claim_support for e in x["evidence_ids"]]
        + [e for x in issues for e in x["evidence_ids"]]
        + warning_evidence_ids
    )
    evidence = [deepcopy(x) for x in reconstruction["review_package"]["evidence"] if x["evidence_id"] in used_evidence]
    present = sum(1 for x in families if x["status"] == "PRESENT")
    support_exclusion = bool(issues)
    status = (
        "HUMAN_CONFIRMATION_REQUIRED" if present == 0
        else "PRESENT" if present == len(families) and not support_exclusion
        else "PARTIAL_REVIEW_REQUIRED"
    )
    return {
        "schema_version": "1.0.0",
        "output_type": "SUPPORTED_DRAFT_CLAIMS",
        "claims_draft_id": claims_draft_id(identity, config),
        "status": status,
        "source_identity": identity,
        "generation_config": deepcopy(config),
        "claim_families": families,
        "claims": claims,
        "review_package": {
            "evidence": evidence,
            "claim_support": claim_support,
            "issues": issues,
            "warnings": warnings,
            "missing_information": missing_information,
            "author_questions": author_questions,
        },
        "review_boundary": {
            "status": "DRAFT",
            "source_grounded": True,
            "human_ip_review_required": True,
            "review_status": "UNREVIEWED",
            "filing_ready": False,
            "legal_advice": False,
            "patentability_assessment_included": False,
            "novelty_assessment_included": False,
            "claim_scope_optimized": False,
            "assembled_p2_001_document": False,
            "render_review_metadata_as_claim_text": False,
        },
    }


def generate_supported_draft_claims(
    reconstruction: Any,
    specification: Any,
    generation_config: Any,
) -> dict[str, Any]:
    """Generate a fresh deterministic standalone P2-004 package."""
    source, spec, config = validate_inputs(reconstruction, specification, generation_config)
    result = _build_supported_draft_claims(source, spec, config)
    # Schema validation here catches implementation/schema drift before return.
    from backend.app.services.supported_draft_claims_validation import output_schema
    from jsonschema import Draft202012Validator
    if list(Draft202012Validator(output_schema()).iter_errors(result)):
        raise SupportedDraftClaimsValidationError("CLAIM_SUPPORT_INCOMPLETE", paths=("/output",))
    return deepcopy(result)
