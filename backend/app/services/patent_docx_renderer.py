"""Production DOCX renderer for Patent DOCX Template v1.0.0."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from docxtpl import DocxTemplate
from jsonschema import Draft202012Validator


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
SCHEMA_PATH = (
    REPOSITORY_ROOT
    / "schemas"
    / "patent-draft"
    / "v1.0.0"
    / "patent-draft.schema.json"
)
TEMPLATE_PATH = (
    REPOSITORY_ROOT
    / "templates"
    / "patent-docx"
    / "v1.0.0"
    / "patent-description-template.docx"
)
OUTPUT_ROOT = REPOSITORY_ROOT / "generated" / "patent-docx" / "v1.0.0"
MISSING_MARKER = "[AUTHOR CONFIRMATION REQUIRED]"


def _load_json_object(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as source:
        value = json.load(source)
    if not isinstance(value, dict):
        raise ValueError("Canonical schema root must be an object.")
    return value


def validate_payload(payload: dict[str, Any]) -> None:
    """Validate a draft against the canonical Patent Draft v1.0.0 schema."""

    if not isinstance(payload, dict):
        raise ValueError("Patent draft payload must be an object.")
    schema = _load_json_object(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(payload)


def _decorate_paragraph(paragraph: dict[str, Any]) -> dict[str, Any]:
    item = deepcopy(paragraph)
    grounding = item["grounding"]
    item["grounding_label"] = grounding["label"]
    item["evidence_text"] = ", ".join(grounding["evidence_ids"])
    item["source_paths_text"] = ", ".join(item["source_paths"])
    return item


def _decorate_block(block: dict[str, Any]) -> dict[str, Any]:
    item = deepcopy(block)
    item.setdefault("marker", "")
    item["paragraphs"] = [
        _decorate_paragraph(paragraph) for paragraph in item["paragraphs"]
    ]
    return item


def _section_map(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {section["section_id"]: section for section in payload["draft_sections"]}


def _subsection_map(section: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        subsection["subsection_id"]: subsection
        for subsection in section["subsections"]
    }


def prepare_context(payload: dict[str, Any]) -> dict[str, Any]:
    """Map a validated canonical draft to the approved DOC-001 template context."""

    sections = _section_map(payload)
    summary = sections["SUMMARY_OF_TECHNICAL_DISCLOSURE"]
    detailed = sections["DETAILED_DESCRIPTION"]
    summary_subsections = _subsection_map(summary)
    detailed_subsections = _subsection_map(detailed)
    selected_title = payload["selected_title"]
    abstract = payload["abstract"]

    drawings = []
    for drawing in payload["drawings"]:
        item = deepcopy(drawing)
        if item["kind"] == "PROPOSED_DRAWING":
            prefix = "Proposed drawing — not supplied"
        elif item["status"] == "MISSING":
            prefix = "Drawing not supplied"
        else:
            prefix = "Source drawing available (not embedded)"
        item["display_text"] = f"{prefix}: {item['title']}"
        item["evidence_text"] = ", ".join(item["evidence_ids"]) or "none"
        item["source_paths_text"] = ", ".join(item["source_paths"])
        drawings.append(item)

    conflicts = []
    for conflict in payload["conflicts"]:
        item = deepcopy(conflict)
        item["evidence_text"] = ", ".join(item["evidence_ids"])
        conflicts.append(item)

    questions = []
    for question in payload["author_questions"]:
        item = deepcopy(question)
        item["missing_text"] = (
            ", ".join(item["related_missing_information_ids"]) or "none"
        )
        item["conflict_text"] = ", ".join(item["related_conflict_ids"]) or "none"
        questions.append(item)

    evidence = []
    for record in payload["evidence_appendix"]:
        item = deepcopy(record)
        item["locator_text"] = json.dumps(
            item["locator"], ensure_ascii=False, sort_keys=True
        )
        item["usage_text"] = "; ".join(
            f"{usage['target_type']}:{usage['target_id']}"
            for usage in item["usage_references"]
        )
        evidence.append(item)

    return {
        "document_metadata": payload["document_metadata"],
        "output_notice": payload["output_notice"],
        "title_text": selected_title.get(
            "text", selected_title.get("marker", MISSING_MARKER)
        ),
        "abstract_text": abstract.get("text", abstract.get("marker", MISSING_MARKER)),
        "abstract_grounding": abstract.get("grounding", {}).get("label", ""),
        "abstract_evidence": ", ".join(
            abstract.get("grounding", {}).get("evidence_ids", [])
        ),
        "abstract_source_paths": ", ".join(abstract.get("source_paths", [])),
        "technical_field": _decorate_block(sections["TECHNICAL_FIELD"]),
        "background": _decorate_block(sections["BACKGROUND"]),
        "summary": _decorate_block(summary),
        "technical_problems": _decorate_block(
            summary_subsections["TECHNICAL_PROBLEMS"]
        ),
        "technical_solutions": _decorate_block(
            summary_subsections["TECHNICAL_SOLUTIONS"]
        ),
        "potential_distinguishing_features": _decorate_block(
            summary_subsections["POTENTIAL_DISTINGUISHING_FEATURES"]
        ),
        "technical_effects": _decorate_block(
            summary_subsections["TECHNICAL_EFFECTS"]
        ),
        "brief_description_of_drawings": _decorate_block(
            sections["BRIEF_DESCRIPTION_OF_DRAWINGS"]
        ),
        "detailed_description": _decorate_block(detailed),
        "components_or_system": _decorate_block(
            detailed_subsections["COMPONENTS_OR_SYSTEM"]
        ),
        "process_or_method_steps": _decorate_block(
            detailed_subsections["PROCESS_OR_METHOD_STEPS"]
        ),
        "embodiments": _decorate_block(detailed_subsections["EMBODIMENTS"]),
        "experimental_examples_and_results": _decorate_block(
            sections["EXPERIMENTAL_EXAMPLES_AND_RESULTS"]
        ),
        "drawings": drawings,
        "missing_information": payload["missing_information"],
        "conflicts": conflicts,
        "author_questions": questions,
        "evidence_appendix": evidence,
        "no_review_items": not (
            payload["missing_information"] or conflicts or questions
        ),
        "no_evidence": not evidence,
    }


class PatentDocxRenderer:
    """Render validated patent draft dictionaries within a configured safe root."""

    def __init__(self, *, output_root: Path = OUTPUT_ROOT) -> None:
        self.output_root = Path(output_root).resolve()

    def render(self, draft: dict[str, Any], output_path: Path) -> Path:
        output_path = Path(output_path).resolve()
        template_path = TEMPLATE_PATH.resolve()

        if not template_path.is_file():
            raise FileNotFoundError("Canonical DOCX template is unavailable.")
        if output_path.suffix.lower() != ".docx":
            raise ValueError("Output path must use the .docx extension.")
        if output_path == template_path:
            raise ValueError("Output path must not overwrite the canonical template.")
        if not output_path.is_relative_to(self.output_root):
            raise ValueError("Output path must be under the configured output root.")

        validate_payload(draft)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        template = DocxTemplate(template_path)
        template.render(prepare_context(draft), autoescape=True)
        template.save(output_path)
        return output_path


def render_patent_docx(
    draft: dict[str, Any],
    output_path: Path,
    *,
    output_root: Path = OUTPUT_ROOT,
) -> Path:
    """Convenience API for direct canonical draft-to-DOCX rendering."""

    return PatentDocxRenderer(output_root=output_root).render(draft, output_path)
