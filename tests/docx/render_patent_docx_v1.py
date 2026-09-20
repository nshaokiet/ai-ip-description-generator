"""Deterministic offline renderer for Patent DOCX Template v1.0.0."""

from __future__ import annotations

import argparse
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Mm, Pt, RGBColor
from docxtpl import DocxTemplate
from jsonschema import Draft202012Validator


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPOSITORY_ROOT / "schemas/patent-draft/v1.0.0/patent-draft.schema.json"
TEMPLATE_PATH = REPOSITORY_ROOT / "templates/patent-docx/v1.0.0/patent-description-template.docx"
OUTPUT_ROOT = REPOSITORY_ROOT / "generated/patent-docx/v1.0.0"
MISSING_MARKER = "[AUTHOR CONFIRMATION REQUIRED]"


def _set_run_font(run: Any, size_pt: float, *, bold: bool = False, italic: bool = False) -> None:
    run.font.name = "Times New Roman"
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = RGBColor(0, 0, 0)
    run._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:ascii"), "Times New Roman")
    run._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:hAnsi"), "Times New Roman")


def _configure_style(
    style: Any,
    size_pt: float,
    *,
    bold: bool = False,
    italic: bool = False,
    alignment: Any = None,
) -> None:
    style.font.name = "Times New Roman"
    style.font.size = Pt(size_pt)
    style.font.bold = bold
    style.font.italic = italic
    style.font.color.rgb = RGBColor(0, 0, 0)
    style._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:ascii"), "Times New Roman")
    style._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:hAnsi"), "Times New Roman")
    style.paragraph_format.line_spacing = 1.15
    style.paragraph_format.space_after = Pt(6)
    if alignment is not None:
        style.paragraph_format.alignment = alignment


def _append_field(paragraph: Any, instruction: str) -> None:
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = f" {instruction} "
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    display = OxmlElement("w:t")
    display.text = "1"
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.extend([begin, instr, separate, display, end])
    _set_run_font(run, 9)


def _add_template_paragraph(document: Document, text: str, style: str = "Normal") -> None:
    document.add_paragraph(text, style=style)


def _add_block(document: Document, key: str) -> None:
    _add_template_paragraph(document, f"{{%p if {key}.status == 'MISSING' %}}")
    _add_template_paragraph(document, f"{{{{ {key}.marker }}}}")
    _add_template_paragraph(document, "{%p endif %}")
    _add_template_paragraph(document, f"{{%p for paragraph in {key}.paragraphs %}}")
    _add_template_paragraph(document, "{{ paragraph.text }}")
    _add_template_paragraph(
        document,
        "Grounding: {{ paragraph.grounding_label }} | Evidence: {{ paragraph.evidence_text }} | Source paths: {{ paragraph.source_paths_text }}",
        "Evidence Note",
    )
    _add_template_paragraph(document, "{%p endfor %}")


def create_canonical_template(path: Path = TEMPLATE_PATH) -> Path:
    """Create the canonical, data-free DOCX template deterministically."""
    path = Path(path).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    document = Document()
    section = document.sections[0]
    section.start_type = WD_SECTION.NEW_PAGE
    section.page_width = Mm(210)
    section.page_height = Mm(297)
    section.top_margin = Cm(2.54)
    section.right_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(2.54)

    styles = document.styles
    _configure_style(styles["Normal"], 12)
    _configure_style(styles["Title"], 16, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER)
    _configure_style(styles["Heading 1"], 14, bold=True)
    styles["Heading 1"].paragraph_format.keep_with_next = True
    _configure_style(styles["Heading 2"], 12, bold=True)
    styles["Heading 2"].paragraph_format.keep_with_next = True
    evidence_style = styles.add_style("Evidence Note", WD_STYLE_TYPE.PARAGRAPH)
    _configure_style(evidence_style, 9, italic=True)

    header = section.header.paragraphs[0]
    header.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _set_run_font(header.add_run("AI-Generated Patent Description Draft"), 9, bold=True)

    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _set_run_font(footer.add_run("AI-generated draft — requires human review."), 9)
    page_line = section.footer.add_paragraph()
    page_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _set_run_font(page_line.add_run("Page "), 9)
    _append_field(page_line, "PAGE")
    _set_run_font(page_line.add_run(" of "), 9)
    _append_field(page_line, "NUMPAGES")

    _add_template_paragraph(document, "Cover and Draft Notice", "Heading 1")
    _add_template_paragraph(document, "{{ output_notice.notice }}")
    _add_template_paragraph(document, "Draft ID: {{ document_metadata.draft_id }}")
    _add_template_paragraph(document, "Source document: {{ document_metadata.source_document.file_name }}")
    _add_template_paragraph(document, "Template version: 1.0.0", "Evidence Note")
    document.paragraphs[-1].add_run().add_break(WD_BREAK.PAGE)

    _add_template_paragraph(document, "Title", "Heading 1")
    _add_template_paragraph(document, "{{ title_text }}", "Title")
    document.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    _add_template_paragraph(document, "Abstract", "Heading 1")
    _add_template_paragraph(document, "{{ abstract_text }}")
    _add_template_paragraph(document, "{%p if abstract_grounding %}")
    _add_template_paragraph(document, "Grounding: {{ abstract_grounding }} | Evidence: {{ abstract_evidence }} | Source paths: {{ abstract_source_paths }}", "Evidence Note")
    _add_template_paragraph(document, "{%p endif %}")

    for heading, key in (
        ("Technical Field", "technical_field"),
        ("Background", "background"),
    ):
        _add_template_paragraph(document, heading, "Heading 1")
        _add_block(document, key)

    _add_template_paragraph(document, "Summary of Technical Disclosure", "Heading 1")
    _add_template_paragraph(document, "{%p if summary.status == 'MISSING' %}")
    _add_template_paragraph(document, "{{ summary.marker }}")
    _add_template_paragraph(document, "{%p endif %}")
    for heading, key in (
        ("Technical Problems", "technical_problems"),
        ("Technical Solutions", "technical_solutions"),
        ("Potential Distinguishing Features", "potential_distinguishing_features"),
        ("Technical Effects", "technical_effects"),
    ):
        _add_template_paragraph(document, heading, "Heading 2")
        _add_block(document, key)

    _add_template_paragraph(document, "Brief Description of Drawings", "Heading 1")
    _add_block(document, "brief_description_of_drawings")
    _add_template_paragraph(document, "{%p for drawing in drawings %}")
    _add_template_paragraph(document, "{{ drawing.display_text }}")
    _add_template_paragraph(document, "Evidence: {{ drawing.evidence_text }} | Source paths: {{ drawing.source_paths_text }}", "Evidence Note")
    _add_template_paragraph(document, "{%p endfor %}")

    _add_template_paragraph(document, "Detailed Description", "Heading 1")
    _add_template_paragraph(document, "{%p if detailed_description.status == 'MISSING' %}")
    _add_template_paragraph(document, "{{ detailed_description.marker }}")
    _add_template_paragraph(document, "{%p endif %}")
    for heading, key in (
        ("Components or System", "components_or_system"),
        ("Process or Method Steps", "process_or_method_steps"),
        ("Embodiments", "embodiments"),
    ):
        _add_template_paragraph(document, heading, "Heading 2")
        _add_block(document, key)

    _add_template_paragraph(document, "Experimental Examples and Results", "Heading 1")
    _add_block(document, "experimental_examples_and_results")

    _add_template_paragraph(document, "Missing Information and Author Questions", "Heading 1")
    _add_template_paragraph(document, "{%p if no_review_items %}")
    _add_template_paragraph(document, "No missing information, unresolved conflicts, or author questions are recorded in this validated draft.")
    _add_template_paragraph(document, "{%p endif %}")
    _add_template_paragraph(document, "{%p for item in missing_information %}")
    _add_template_paragraph(document, "Missing information — {{ item.missing_id }}", "Heading 2")
    _add_template_paragraph(document, "{{ item.description }}")
    _add_template_paragraph(document, "{{ item.marker }} | Impact: {{ item.impact }} | Owner: {{ item.owner }} | Target: {{ item.target_path }}", "Evidence Note")
    _add_template_paragraph(document, "{%p endfor %}")
    _add_template_paragraph(document, "{%p for conflict in conflicts %}")
    _add_template_paragraph(document, "Unresolved conflict — {{ conflict.conflict_id }}", "Heading 2")
    _add_template_paragraph(document, "{{ conflict.summary }}")
    _add_template_paragraph(document, "Status: {{ conflict.resolution_status }} | Evidence: {{ conflict.evidence_text }} | {{ conflict.marker }}", "Evidence Note")
    _add_template_paragraph(document, "{%p endfor %}")
    _add_template_paragraph(document, "{%p for question in author_questions %}")
    _add_template_paragraph(document, "Author question — {{ question.question_id }}", "Heading 2")
    _add_template_paragraph(document, "{{ question.question }}")
    _add_template_paragraph(document, "Priority: {{ question.priority }} | Related missing information: {{ question.missing_text }} | Related conflicts: {{ question.conflict_text }}", "Evidence Note")
    _add_template_paragraph(document, "{%p endfor %}")

    _add_template_paragraph(document, "Evidence and Reference Appendix", "Heading 1")
    _add_template_paragraph(document, "{%p if no_evidence %}")
    _add_template_paragraph(document, "No evidence is used by this validated draft.")
    _add_template_paragraph(document, "{%p endif %}")
    _add_template_paragraph(document, "{%p for evidence in evidence_appendix %}")
    _add_template_paragraph(document, "Evidence {{ evidence.evidence_id }}", "Heading 2")
    _add_template_paragraph(document, "{{ evidence.excerpt }}")
    _add_template_paragraph(document, "Type: {{ evidence.evidence_type }} | Document: {{ evidence.document_id }} | Locator: {{ evidence.locator_text }}", "Evidence Note")
    _add_template_paragraph(document, "Used by: {{ evidence.usage_text }}", "Evidence Note")
    _add_template_paragraph(document, "{%p endfor %}")

    properties = document.core_properties
    properties.title = "Patent Description Draft Template"
    properties.subject = "Versioned DOCX template requiring human review"
    properties.author = "AI IP Description Generator"
    properties.keywords = "patent description draft, human review"
    document.save(path)
    return path


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("Input JSON root must be an object.")
    return value


def validate_payload(payload: dict[str, Any]) -> None:
    schema = _load_json(SCHEMA_PATH)
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
    item["paragraphs"] = [_decorate_paragraph(paragraph) for paragraph in item["paragraphs"]]
    return item


def _section_map(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {section["section_id"]: section for section in payload["draft_sections"]}


def _subsection_map(section: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {subsection["subsection_id"]: subsection for subsection in section["subsections"]}


def prepare_context(payload: dict[str, Any]) -> dict[str, Any]:
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
        item["missing_text"] = ", ".join(item["related_missing_information_ids"]) or "none"
        item["conflict_text"] = ", ".join(item["related_conflict_ids"]) or "none"
        questions.append(item)

    evidence = []
    for record in payload["evidence_appendix"]:
        item = deepcopy(record)
        item["locator_text"] = json.dumps(item["locator"], ensure_ascii=False, sort_keys=True)
        item["usage_text"] = "; ".join(
            f"{usage['target_type']}:{usage['target_id']}" for usage in item["usage_references"]
        )
        evidence.append(item)

    context = {
        "document_metadata": payload["document_metadata"],
        "output_notice": payload["output_notice"],
        "title_text": selected_title.get("text", selected_title.get("marker", MISSING_MARKER)),
        "abstract_text": abstract.get("text", abstract.get("marker", MISSING_MARKER)),
        "abstract_grounding": abstract.get("grounding", {}).get("label", ""),
        "abstract_evidence": ", ".join(abstract.get("grounding", {}).get("evidence_ids", [])),
        "abstract_source_paths": ", ".join(abstract.get("source_paths", [])),
        "technical_field": _decorate_block(sections["TECHNICAL_FIELD"]),
        "background": _decorate_block(sections["BACKGROUND"]),
        "summary": _decorate_block(summary),
        "technical_problems": _decorate_block(summary_subsections["TECHNICAL_PROBLEMS"]),
        "technical_solutions": _decorate_block(summary_subsections["TECHNICAL_SOLUTIONS"]),
        "potential_distinguishing_features": _decorate_block(summary_subsections["POTENTIAL_DISTINGUISHING_FEATURES"]),
        "technical_effects": _decorate_block(summary_subsections["TECHNICAL_EFFECTS"]),
        "brief_description_of_drawings": _decorate_block(sections["BRIEF_DESCRIPTION_OF_DRAWINGS"]),
        "detailed_description": _decorate_block(detailed),
        "components_or_system": _decorate_block(detailed_subsections["COMPONENTS_OR_SYSTEM"]),
        "process_or_method_steps": _decorate_block(detailed_subsections["PROCESS_OR_METHOD_STEPS"]),
        "embodiments": _decorate_block(detailed_subsections["EMBODIMENTS"]),
        "experimental_examples_and_results": _decorate_block(sections["EXPERIMENTAL_EXAMPLES_AND_RESULTS"]),
        "drawings": drawings,
        "missing_information": payload["missing_information"],
        "conflicts": conflicts,
        "author_questions": questions,
        "evidence_appendix": evidence,
        "no_review_items": not (payload["missing_information"] or conflicts or questions),
        "no_evidence": not evidence,
    }
    return context


def render_patent_docx(input_path: Path, output_path: Path, template_path: Path = TEMPLATE_PATH) -> Path:
    input_path = Path(input_path).resolve()
    output_path = Path(output_path).resolve()
    template_path = Path(template_path).resolve()
    approved_root = OUTPUT_ROOT.resolve()

    if not input_path.is_file():
        raise FileNotFoundError(f"Input JSON not found: {input_path}")
    if not template_path.is_file():
        raise FileNotFoundError(f"Canonical template not found: {template_path}")
    if output_path in {input_path, template_path}:
        raise ValueError("Output path must not overwrite the input or canonical template.")
    if not output_path.is_relative_to(approved_root):
        raise ValueError(f"Output path must be under {approved_root}")

    payload = _load_json(input_path)
    validate_payload(payload)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    template = DocxTemplate(template_path)
    template.render(prepare_context(payload), autoescape=True)
    template.save(output_path)
    return output_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_json", nargs="?", type=Path)
    parser.add_argument("output_docx", nargs="?", type=Path)
    parser.add_argument("--create-template", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.create_template:
            create_canonical_template()
            print(f"Created canonical template: {TEMPLATE_PATH.relative_to(REPOSITORY_ROOT)}")
            return 0
        if args.input_json is None or args.output_docx is None:
            parser.error("input_json and output_docx are required unless --create-template is used")
        rendered = render_patent_docx(args.input_json, args.output_docx)
        print(f"Rendered DOCX: {rendered.relative_to(REPOSITORY_ROOT)}")
        return 0
    except Exception as error:  # safe CLI boundary; never print payload content
        print(f"DOCX rendering failed: {type(error).__name__}: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
