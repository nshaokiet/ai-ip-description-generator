"""Offline, reconstruction-only USPTO content generation; no runtime wiring."""
from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any

from backend.app.services.uspto_specification_generation_validation import (
    ELIGIBLE, USPTOGenerationValidationError, normalize, output_schema,
    prohibited_text, validate_generated_specification, validate_generation_config,
    validate_generation_input, word_count,
)

RELATION_WORDING = {
    "RELATED_TO": "is related to", "PART_OF": "is part of", "CONTAINS": "contains",
    "CONNECTED_TO": "is connected to", "COUPLED_TO": "is coupled to",
    "COMMUNICATES_WITH": "communicates with", "RECEIVES_FROM": "receives from",
    "OUTPUTS_TO": "outputs to", "CONTROLS": "controls", "TRANSFORMS": "transforms",
    "MEASURES": "measures", "STORES": "stores", "EXECUTES": "executes",
    "INPUT_TO_STEP": "is an input to step", "OUTPUT_FROM_STEP": "is an output from step",
    "DEPENDS_ON": "depends on",
}
REF_FIELDS = {
    "subject_id", "object_id", "source_id", "target_id", "addresses_problem_ids",
    "related_element_ids", "related_step_ids", "input_element_ids", "output_element_ids",
    "dependency_step_ids", "related_entity_ids", "related_solution_ids", "element_ids",
    "method_step_ids", "parameter_ids", "base_entity_ids",
}
ROUTES = {
    "title_candidates": "TITLE_OF_THE_INVENTION", "technical_field": "FIELD_OF_THE_INVENTION",
    "technical_context": "DESCRIPTION_OF_RELATED_ART", "background": "DESCRIPTION_OF_RELATED_ART",
    "technical_problems": "BRIEF_SUMMARY_OF_THE_INVENTION", "problems": "BRIEF_SUMMARY_OF_THE_INVENTION",
    "technical_solutions": "BRIEF_SUMMARY_OF_THE_INVENTION", "solution_concepts": "BRIEF_SUMMARY_OF_THE_INVENTION",
    "components": "DETAILED_DESCRIPTION_OF_THE_INVENTION", "elements": "DETAILED_DESCRIPTION_OF_THE_INVENTION",
    "relationships": "DETAILED_DESCRIPTION_OF_THE_INVENTION", "flows": "DETAILED_DESCRIPTION_OF_THE_INVENTION",
    "process_steps": "DETAILED_DESCRIPTION_OF_THE_INVENTION", "method_steps": "DETAILED_DESCRIPTION_OF_THE_INVENTION",
    "experimental_data": "DETAILED_DESCRIPTION_OF_THE_INVENTION", "parameters": "DETAILED_DESCRIPTION_OF_THE_INVENTION",
    "technical_effects": "DETAILED_DESCRIPTION_OF_THE_INVENTION", "embodiments": "DETAILED_DESCRIPTION_OF_THE_INVENTION",
    "variants": "DETAILED_DESCRIPTION_OF_THE_INVENTION", "source_artifacts": "BRIEF_DESCRIPTION_OF_THE_DRAWINGS",
    "drawing_requirements": "BRIEF_DESCRIPTION_OF_THE_DRAWINGS",
}


def generate_uspto_specification(
    reconstruction: dict[str, Any], generation_config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Generate a draft from an already upstream-validated P2-002 payload.

    Explicit caller provenance is required even with the optional API argument.
    No source text is interpreted as configuration, a command, or new evidence.
    """
    # Provenance refusal precedes even template/index construction.
    config = validate_generation_config(generation_config)
    source = validate_generation_input(reconstruction)
    config = validate_generation_config(config, source)
    result = _build_specification(source, config)
    validate_generated_specification(result, source, config)
    return result


def _sentence(text: str) -> str:
    return text if text.endswith((".", "!", "?")) else text + "."


def _references(item: dict[str, Any]) -> list[str]:
    result: list[str] = []
    for key, value in item.items():
        if key in REF_FIELDS:
            result.extend(value if isinstance(value, list) else [value])
    return list(dict.fromkeys(result))


class _Projection:
    def __init__(self, source: dict[str, Any]) -> None:
        self.source = source
        self.model = source["invention_model"]
        self.items: dict[str, tuple[str, dict[str, Any]]] = {}
        self.by_id: dict[str, str] = {}
        for group, values in self.model.items():
            values = [values] if isinstance(values, dict) else values
            for index, item in enumerate(values):
                path = f"/invention_model/{group}" + ("" if group == "technical_field" else f"/{index}")
                self.items[path] = (group, item)
                id_key = next((k for k in item if k.endswith("_id") and k not in REF_FIELDS), None)
                if id_key:
                    self.by_id[item[id_key]] = path
        self.blocked: set[str] = set()
        for path, (group, item) in self.items.items():
            support = item.get("support")
            if group != "source_artifacts" and (not support or support["grounding_class"] not in ELIGIBLE):
                self.blocked.add(path)
            if group == "variants" and (item["status"] != "SOURCE_SUPPORTED" or not item["filing_content_eligible"] or item["human_confirmation_required"]):
                self.blocked.add(path)
            if group == "embodiments" and item["disclosure_status"] == "PROPOSED_REQUIRES_HUMAN_CONFIRMATION":
                self.blocked.add(path)
            if group == "elements" and item["essentiality"] == "CONDITIONAL" and not item.get("description"):
                # The released schema has no separate element-condition field.
                # Preserve a supported description whole, or require Human input.
                self.blocked.add(path)
            if any(c["support"]["grounding_class"] not in ELIGIBLE for c in item.get("conditions", [])):
                self.blocked.add(path)
            for key, value in item.items():
                if key in {"title", "name", "description", "statement", "action", "source_reference"} and prohibited_text(value):
                    self.blocked.add(path)
            if any(prohibited_text(c["statement"]) for c in item.get("conditions", [])):
                self.blocked.add(path)
            if group == "parameters":
                from backend.app.services.invention_reconstruction_validation import _walk
                if any(isinstance(v, str) and prohibited_text(v) for _, v in _walk(item["value"])) or prohibited_text(item.get("unit", "")):
                    self.blocked.add(path)
        self.tainted: set[str] = set()
        for conflict in source["review_package"]["conflicts"]:
            self.tainted.update(self.by_id[x] for x in conflict["affected_entity_ids"] if x in self.by_id)
        self.blocked.update(self.tainted)
        while True:
            previous = set(self.blocked)
            for path, (_, item) in self.items.items():
                if any(self.by_id.get(x) in self.blocked for x in _references(item)):
                    self.blocked.add(path)
                if any(self.by_id.get(x) in self.tainted for x in _references(item)):
                    self.tainted.add(path)
            if previous == self.blocked:
                break
        self.review: dict[str, list] = {k: [] for k in ("evidence", "missing_information", "author_questions", "claim_support", "warnings")}
        self.used: set[str] = set()

    def paths(self, group: str) -> list[str]:
        return [p for p, (g, _) in self.items.items() if g == group and p not in self.blocked]

    def sources(self, path: str) -> list[str]:
        item = self.items[path][1]
        return list(dict.fromkeys([path, *[self.by_id[x] for x in _references(item)],
            *[f"{path}/conditions/{i}" for i in range(len(item.get("conditions", [])))]]))

    def support(self, paths: list[str]) -> dict[str, Any]:
        from backend.app.services.invention_reconstruction_validation import _resolve_pointer
        ids: list[str] = []
        classes: list[str] = []
        for path in paths:
            item = _resolve_pointer(self.source, path)
            support = item.get("support", {"evidence_ids": item.get("evidence_ids", []), "grounding_class": "PARAPHRASE"})
            ids.extend(support["evidence_ids"])
            classes.append(support["grounding_class"])
        self.used.update(ids)
        return {"source_paths": list(dict.fromkeys(paths)), "evidence_ids": list(dict.fromkeys(ids)),
                "grounding_class": max(classes, key=ELIGIBLE.index) if classes else "MISSING"}

    def label(self, identifier: str) -> str:
        item = self.items[self.by_id[identifier]][1]
        return next(item[k] for k in ("name", "action", "statement", "description", "title") if k in item)

    def names(self, ids: list[str]) -> str:
        return "; ".join(self.label(x) for x in ids) or "none represented"

    def text(self, path: str) -> str:
        group, x = self.items[path]
        if group in {"solution_concepts", "problems", "technical_context"}:
            prefix = {"solution_concepts": "The disclosed solution is", "problems": "The represented technical problem is", "technical_context": "The technical context is"}[group]
            return _sentence(f"{prefix}: {x['statement']}")
        if group == "technical_field":
            return _sentence("The technical field is " + x["name"]) + (" " + _sentence(x["description"]) if "description" in x else "")
        if group == "elements":
            qualifier = {"ESSENTIAL": "required", "OPTIONAL": "optional", "CONDITIONAL": "conditional", "UNKNOWN": "of unspecified essentiality"}[x["essentiality"]]
            return _sentence(f"The element {x['name']} is {qualifier} (type: {x['element_type'].lower().replace('_', ' ')})") + (" " + _sentence(x["description"]) if "description" in x else "")
        if group == "relationships":
            return _sentence(f"{self.label(x['subject_id'])} {RELATION_WORDING[x['relation_type']]} {self.label(x['object_id'])}")
        if group == "flows":
            return _sentence(f"A {x['flow_type'].lower()} flow is represented from {self.label(x['source_id'])} to {self.label(x['target_id'])}: {x['description']}")
        if group == "method_steps":
            text = _sentence(f"Step {x['sequence_index']}: {x['action']}")
            text += " " + _sentence(f"Inputs: {self.names(x['input_element_ids'])}; outputs: {self.names(x['output_element_ids'])}")
            text += " " + _sentence(f"Explicit step dependencies: {self.names(x['dependency_step_ids'])}")
        elif group == "parameters":
            v = x["value"]
            if v["value_kind"] == "RANGE":
                value = f"{v['minimum']} to {v['maximum']}"
            else:
                value = json.dumps(v.get("exact_value", v.get("values", v.get("qualitative_value"))), ensure_ascii=False)
            qualifier = {"EXAMPLE_ONLY": "In the represented example", "SUPPORTED_RANGE": "Within the supported range", "UNKNOWN_SCOPE": "With scope unspecified"}[x["scope_status"]]
            text = _sentence(f"{qualifier}, {x['name']} has {v['value_kind'].lower()} value {value}" + (f" {x['unit']}" if "unit" in x else "") + f" (role: {x['role'].lower().replace('_', ' ')})")
        elif group == "embodiments":
            wording = {"EXPLICIT": "explicitly disclosed", "SYNTHESIZED": "represented combination"}[x["disclosure_status"]]
            text = _sentence(f"The {wording} embodiment {x['name']} is described as follows: {x['description']}")
            text += " " + _sentence(f"Elements: {self.names(x['element_ids'])}; method steps: {self.names(x['method_step_ids'])}; parameters: {self.names(x['parameter_ids'])}")
        elif group == "technical_effects":
            wording = {"SOURCE_REPORTED": "The source reports the technical effect", "SUPPORTED_CONSEQUENCE": "A supported consequence is"}[x["effect_basis"]]
            text = _sentence(f"{wording}: {x['statement']}")
        elif group == "variants":
            text = _sentence("The source-supported variant is: " + x["description"])
        else:
            raise USPTOGenerationValidationError("UNSUPPORTED_MAPPING")
        if x.get("conditions"):
            text += " " + _sentence("Conditions: " + "; ".join(c["statement"] for c in x["conditions"]))
        return text

    def paragraphs(self, paths: list[str], family: str) -> list[dict[str, Any]]:
        return [{"paragraph_id": f"P-{family}-{i+1:04d}", "sequence": i+1,
                 "text": self.text(p), "support": self.support(self.sources(p))} for i, p in enumerate(paths)]

    def gap(self, section: str, description: str) -> str:
        identifier = f"MI-P2-003-{len(self.review['missing_information'])+1:04d}"
        self.review["missing_information"].append({"missing_id": identifier, "target_section_id": section,
            "description": description, "author_question_ids": []})
        return identifier

    def warning(self, code: str, message: str, paths: list[str]) -> None:
        self.review["warnings"].append({"warning_id": f"W-P2-003-{len(self.review['warnings'])+1:04d}",
            "code": code, "message": message, "affected_paths": paths})


def _build_specification(source: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    p = _Projection(source)
    schema = output_schema()
    order = deepcopy(schema["properties"]["section_order"]["const"])
    sections: list[dict[str, Any]] = []
    for ref in schema["properties"]["sections"]["prefixItems"]:
        props = schema["$defs"][ref["$ref"].rsplit("/", 1)[1]]["allOf"][1]["properties"]
        sections.append({"section_id": props["section_id"]["const"], "sequence": props["sequence"]["const"],
                         "heading": props["heading"]["const"], "status": "PRESENT", "paragraphs": [],
                         "subsections": [], "figures": [], "missing_information_ids": []})

    def empty(section: dict[str, Any], state: str, reason: str) -> None:
        section["status"] = state
        section["missing_information_ids"] = [p.gap(section["section_id"], reason)]

    title = p.paths("title_candidates")
    selected = config.get("selected_title_candidate_id")
    if selected:
        title = [path for path in title if p.items[path][1]["title_id"] == selected]
    if len(title) == 1:
        path = title[0]
        sections[0]["paragraphs"] = [{"paragraph_id": "P-TITLE-0001", "sequence": 1,
            "text": p.items[path][1]["title"], "support": p.support([path])}]
    else:
        empty(sections[0], "HUMAN_CONFIRMATION_REQUIRED" if len(title) > 1 else "MISSING", "An eligible existing title requires selection or confirmation.")
    for section in sections[1:6]:
        empty(section, "HUMAN_CONFIRMATION_REQUIRED", "Administrative content requires separately authorized Human input; it cannot be inferred from reconstruction.")
    for i, (group, identifier, family) in enumerate([
        ("technical_field", "FIELD_OF_THE_INVENTION", "FIELD"),
        ("technical_context", "DESCRIPTION_OF_RELATED_ART", "RELATED"),
    ]):
        subsection = {"section_id": identifier, "sequence": i+1, "heading": identifier.replace("_", " "),
            "status": "PRESENT", "paragraphs": p.paragraphs(p.paths(group), family), "missing_information_ids": []}
        if not subsection["paragraphs"]:
            empty(subsection, "MISSING", "No eligible technical content is represented for this subsection.")
        sections[6]["subsections"].append(subsection)
    # P2-001 requires both subsections. Background is their structural container;
    # each subsection independently states whether supported content is missing.
    summary_paths = [path for group in ("problems", "solution_concepts", "elements", "method_steps", "technical_effects", "embodiments") for path in p.paths(group)]
    if p.paths("solution_concepts"):
        sections[7]["paragraphs"] = p.paragraphs(summary_paths, "SUMMARY")
    else:
        empty(sections[7], "HUMAN_CONFIRMATION_REQUIRED" if any(g == "solution_concepts" and path in p.tainted for path, (g, _) in p.items.items()) else "MISSING", "A supported, unconflicted solution is needed for the summary.")
    detail_paths = [path for group in ("solution_concepts", "elements", "relationships", "flows", "method_steps", "parameters", "embodiments", "technical_effects", "variants") for path in p.paths(group)]
    if detail_paths:
        sections[9]["paragraphs"] = p.paragraphs(detail_paths, "DETAIL")
    else:
        empty(sections[9], "HUMAN_CONFIRMATION_REQUIRED" if p.tainted else "MISSING", "No sufficient eligible detailed-description content remains.")
    drawings = [path for path, (group, _) in p.items.items() if group == "source_artifacts"]
    eligible_drawings: list[str] = []
    for path in drawings:
        x = p.items[path][1]
        description = x["source_reference"]
        supported_text = any(normalize(description) in normalize(e["excerpt"]) for e in source["review_package"]["evidence"] if e["evidence_id"] in x["evidence_ids"])
        if path not in p.blocked and x["artifact_type"] != "TABLE" and not x["human_confirmation_required"] and word_count(description) >= 5 and supported_text and (
            x["artifact_type"] == "FIGURE_REFERENCE" or (x["drawing_kind"] == "SOURCE_FIGURE" and x["drawing_status"] == "AVAILABLE")
        ):
            eligible_drawings.append(path)
    if eligible_drawings and len(eligible_drawings) == len(drawings):
        for i, path in enumerate(eligible_drawings):
            x = p.items[path][1]
            label = f"FIG. {i+1}"
            sections[8]["figures"].append({"figure_id": f"FIG-P2-003-{i+1:04d}", "figure_label": label,
                "title": x["source_reference"], "description": x["source_reference"],
                "source_figure_ids": [x.get("drawing_id", x["source_reference"])], "reference_numerals": []})
            sections[8]["paragraphs"].append({"paragraph_id": f"P-DRAWINGS-{i+1:04d}", "sequence": i+1,
                "text": _sentence(label + ": " + x["source_reference"]), "support": p.support([path])})
    else:
        empty(sections[8], "HUMAN_CONFIRMATION_REQUIRED", "Supported textual figure descriptions require Human confirmation; no image inference is performed.")
        if drawings:
            p.warning("DRAWING_DESCRIPTION_REQUIRES_REVIEW", "Source artifacts lack sufficient eligible textual drawing descriptions.", drawings)
    empty(sections[10], "HUMAN_CONFIRMATION_REQUIRED", "Sequence-listing applicability/data requires separately authorized Human input.")
    claims = {"section_id": "CLAIMS", "sequence": 11, "heading": "CLAIMS", "status": "MISSING", "claims": [],
        "missing_information_ids": [p.gap("CLAIMS", "Claims are intentionally not generated by P2-003; P2-004 / separately authorized Claims work owns this gate.")]}
    abstract = {"section_id": "ABSTRACT_OF_THE_DISCLOSURE", "sequence": 12, "heading": "ABSTRACT OF THE DISCLOSURE",
        "status": "MISSING", "text": "", "word_count": 0, "support": {"source_paths": [], "evidence_ids": [], "grounding_class": "MISSING"}, "missing_information_ids": []}
    context = p.paths("technical_field") or p.paths("technical_context")
    solution = p.paths("solution_concepts")
    aspect = p.paths("elements") or p.paths("method_steps")
    if context and solution and aspect:
        chosen = [context[0], solution[0], aspect[0]]
        sentences = [p.text(x) for x in chosen]
        if word_count(" ".join(sentences)) <= 150:
            effects = p.paths("technical_effects")
            if effects and word_count(" ".join([*sentences, p.text(effects[0])])) <= 150:
                chosen.append(effects[0])
                sentences.append(p.text(effects[0]))
            abstract.update(status="PRESENT", text=" ".join(sentences), word_count=word_count(" ".join(sentences)),
                            support=p.support([s for path in chosen for s in p.sources(path)]))
    if abstract["status"] == "MISSING":
        abstract["missing_information_ids"] = [p.gap("ABSTRACT_OF_THE_DISCLOSURE", "Insufficient supported whole sentences fit the 150-word abstract limit.")]
    for index, conflict in enumerate(source["review_package"]["conflicts"]):
        p.warning("UNRESOLVED_RECONSTRUCTION_CONFLICT", json.dumps(conflict, ensure_ascii=False, sort_keys=True), [f"/review_package/conflicts/{index}"])
        for alternative in conflict["alternatives"]:
            p.used.update(alternative["evidence_ids"])
    for path in p.items:
        if path in p.blocked and p.items[path][0] != "technical_field":
            p.warning("RECONSTRUCTION_CONTENT_EXCLUDED", "Content or its references are not eligible for filing prose; Human review required.", [path])
            item = p.items[path][1]
            p.used.update(item.get("support", item).get("evidence_ids", []))
    for path in drawings:
        p.used.update(p.items[path][1]["evidence_ids"])
    review = source["review_package"]
    for index, missing in enumerate(review["missing_information"]):
        tokens = missing["target_path"].strip("/").split("/")
        if tokens[0] == "invention_model":
            tokens = tokens[1:]
        target = ROUTES.get(tokens[0]) if tokens else None
        questions = [q for q in review["author_questions"] if q["missing_information_id"] == missing["missing_id"]]
        if target:
            p.gap(target, json.dumps(missing, ensure_ascii=False, sort_keys=True))
            record = p.review["missing_information"][-1]
            for question in questions:
                qid = f"AQ-P2-003-{len(p.review['author_questions'])+1:04d}"
                record["author_question_ids"].append(qid)
                p.review["author_questions"].append({"question_id": qid, "target_section_id": target,
                    "question": json.dumps(question, ensure_ascii=False, sort_keys=True), "status": "OPEN"})
        else:
            p.warning("UNROUTED_RECONSTRUCTION_GAP", json.dumps({"missing": missing, "questions": questions}, ensure_ascii=False, sort_keys=True), [f"/review_package/missing_information/{index}"])
    for index, warning in enumerate(review["warnings"]):
        p.warning(warning["code"], json.dumps(warning, ensure_ascii=False, sort_keys=True), [f"/review_package/warnings/{index}"])
        p.used.update(warning["support"]["evidence_ids"])
    for index, evidence in enumerate(review["evidence"]):
        if evidence["evidence_id"] in p.used:
            p.review["evidence"].append({"evidence_id": evidence["evidence_id"], "evidence_type": "SOURCE_DOCUMENT",
                "source_paths": [f"/review_package/evidence/{index}"], "description": json.dumps(evidence, ensure_ascii=False, sort_keys=True)})
    metadata = deepcopy(source["document_metadata"])
    material = metadata["document_id"] + "|" + metadata["file_name"] + "|" + metadata.get("sha256", "")
    metadata["synthetic"] = config["source_document_synthetic"]
    boundary = {key: deepcopy(value["const"]) for key, value in schema["$defs"]["review_boundary"]["properties"].items()}
    return {"schema_version": "2.0.0", "output_type": "USPTO_SPECIFICATION_DRAFT",
        "document_metadata": {"draft_id": "p2-003-" + hashlib.sha256(material.encode("utf-8")).hexdigest()[:24],
            "language": "en", "target_jurisdiction": "US", "specification_kind": "NONPROVISIONAL_UTILITY_PATENT_SPECIFICATION_DRAFT", "source_document": metadata},
        "section_order": order, "sections": sections, "claims": claims, "abstract": abstract,
        "review_boundary": boundary, "review_package": p.review}
