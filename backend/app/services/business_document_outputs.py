"""Additive business projections delegating to the byte-frozen P2-006 renderer.

No released renderer, Claims authority or source contract is modified. Its banner
continues identifying the patent-draft context; the document title identifies the
business view. Source technical prose is unchanged; labels are not translation.
"""
from __future__ import annotations

from pathlib import Path
from tempfile import mkdtemp
from typing import Any, Mapping
import os
import shutil

from backend.app.services.uspto_document_package_validation import validate_uspto_document_package
from backend.app.services.uspto_offline_renderer import (
    Part, Section, RenderModel, CLAIMS_INCOMPLETE, MAX_FILING_CHARS,
    _build_model, _status_marker, _assert_safe_parent, _pdf, _docx,
)


def _business_docx_title(path: Path, title: str) -> None:
    """Style the added view title after the released renderer finishes."""
    from docx import Document
    from docx.shared import RGBColor
    document = Document(path)
    paragraph = document.paragraphs[0]
    if paragraph.text != title:
        raise ValueError("Business title unavailable")
    style = document.styles["Title"]
    paragraph.style = style
    style.font.name = "Crimson Text"
    style.font.color.rgb = RGBColor(0, 0, 0)
    for element in (style.element, paragraph._p):
        for border in list(element.xpath(".//w:pBdr")):
            border.getparent().remove(border)
    for run in paragraph.runs:
        run.font.name = "Crimson Text"
        run.font.color.rgb = RGBColor(0, 0, 0)
    document.core_properties.title = title
    document.save(path)


BUSINESS_OUTPUT_VERSION = "1.0.3"
BUSINESS_FILES = tuple(f"{kind}.{extension}" for kind in
    ("PATENT_DRAFT", "ANNOTATED_DRAFT", "ANALYSIS_REPORT") for extension in ("pdf", "docx"))
BUSINESS_MANIFEST = "BUSINESS_OUTPUT_MANIFEST.json"
BUSINESS_LABELS = {
    "en": {"PATENT_DRAFT": "Patent Draft", "ANNOTATED_DRAFT": "Annotated Draft",
        "ANALYSIS_REPORT": "Analysis Report", "source": "Source", "missing": "Missing information",
        "prior": "Prior Art limitations", "figures": "Figure review", "claims": "Claims support",
        "notice": "Template labels only; source technical text unchanged. Translation not assessed.",
        "prior_notice": "Prior Art evidence NOT_PROVIDED. Search completeness and Human continuation NOT_VERIFIED. No novelty or patentability conclusion.",
        "figure_notice": "REVIEW_REQUIRED: no original-asset/redraw fidelity verification is supplied."},
    "vi": {"PATENT_DRAFT": "Bản thảo sáng chế", "ANNOTATED_DRAFT": "Bản thảo có chú thích",
        "ANALYSIS_REPORT": "Báo cáo phân tích", "source": "Nguồn", "missing": "Thông tin còn thiếu",
        "prior": "Giới hạn tra cứu Prior Art", "figures": "Kiểm tra hình vẽ", "claims": "Căn cứ Claims",
        "notice": "BẢN NHÁP — CẦN CHUYÊN VIÊN KIỂM TRA. Chỉ đổi nhãn biểu mẫu; nội dung kỹ thuật nguồn giữ nguyên. Chưa kiểm chứng bản dịch.",
        "prior_notice": "Chưa có hồ sơ Prior Art trong bộ xuất này. Chưa xác minh mức độ đầy đủ và quyết định tiếp tục. Không kết luận tính mới hoặc patentability.",
        "figure_notice": "REVIEW_REQUIRED: chưa có kiểm chứng độ trung thực của hình gốc hoặc bản vẽ lại."},
}


def _business_models(package, originals, template_language):
    import json
    filing = package["filing_view"]
    labels = BUSINESS_LABELS[template_language]
    evidence = {item["evidence_id"]: item for item in originals["structured_analysis"]["evidence"]}

    def citation(ids):
        citations = []
        for identity in ids:
            item = evidence.get(identity)
            if item is None:
                raise ValueError("Evidence reference unavailable")
            locator = ", ".join(f"{key}={value}" for key, value in item["locator"].items())
            citations.append(f"{identity} ({locator})")
        return labels["source"] + ": " + ("; ".join(citations) if citations else "NOT_PROVIDED — REVIEW_REQUIRED")

    missing = package["review_package"]["original_p2_003"]["review_package"]["missing_information"]
    def annotation_parts(section):
        parts = []
        if section["status"] != "PRESENT":
            parts.append(Part("status", _status_marker(section["status"])))
        else:
            for paragraph in section["paragraphs"]:
                parts.append(Part("prose", paragraph["text"]))
                support = paragraph["support"]
                parts.append(Part("status", citation(support["evidence_ids"]) + "; " + support["grounding_class"]))
            for child in section.get("subsections", ()):
                parts.append(Part("heading", child["heading"]))
                parts.extend(annotation_parts(child))
        for item in missing:
            if item["target_section_id"] == section["section_id"]:
                parts.append(Part("status", labels["missing"] + ": " + item["missing_id"] + " — " + item["description"]))
        for figure in section.get("figures", ()):
            parts.append(Part("status", json.dumps(figure, ensure_ascii=False, sort_keys=True) + " — REVIEW_REQUIRED"))
        return tuple(parts)

    base = _build_model(filing)
    lookup = {section["section_id"]: section for section in filing["sections"]}
    annotated = []
    for section in base.sections:
        if section.section_id in lookup:
            parts = annotation_parts(lookup[section.section_id])
        elif section.section_id == "CLAIMS":
            parts = list(section.parts)
            for support in package["review_package"]["projected_claim_support"]:
                parts.append(Part("status", f"Claim {support['claim_number']} / {support['element_id']}: "
                    + citation(support["evidence_ids"]) + "; sections=" + ", ".join(support["specification_section_ids"])))
            parts = tuple(parts)
        else:
            parts = section.parts + (Part("status", citation(filing["abstract"].get("support", {}).get("evidence_ids", []))),)
        annotated.append(Section(section.section_id, section.heading, parts))

    report = []
    source = package["source_identity"]
    report.append(Section("SOURCE_PROVENANCE", labels["source"], (
        Part("prose", source["document_id"] + " — " + source["file_name"]),
        Part("prose", "SHA256: " + source["source_sha256"]),
        Part("prose", "Package: " + package["package_id"]),
        Part("prose", "Title: " + base.title),)))
    groups = (("technical_problems", "Technical problems", "Vấn đề kỹ thuật"),
        ("technical_solutions", "Technical solutions", "Giải pháp kỹ thuật"),
        ("potential_distinguishing_features", "Potential technical contributions", "Đóng góp kỹ thuật tiềm năng"),
        ("technical_effects", "Technical effects", "Hiệu quả kỹ thuật"),
        ("experimental_data", "Scientific conditions and results", "Điều kiện và kết quả khoa học"),
        ("drawing_requirements", "Drawing requirements", "Yêu cầu hình vẽ"),
        ("missing_information", "Missing disclosures", "Thông tin còn thiếu"),
        ("author_questions", "Questions for the author", "Câu hỏi cần tác giả xác nhận"))
    for key, en, vi in groups:
        parts = []
        for item in originals["structured_analysis"][key]:
            identity = next((str(v) for k, v in item.items() if k.endswith("_id")), "")
            text = next((item[k] for k in ("statement", "description", "question", "title", "name") if k in item), "")
            parts.append(Part("prose", (identity + ": " + text).strip()))
            for field in ("conditions", "results"):
                for measurement in item.get(field, []):
                    parts.append(Part("prose", str(measurement.get("parameter", measurement.get("metric", field)))
                        + ": " + ("[MISSING — HUMAN CONFIRMATION REQUIRED]" if measurement.get("value") is None
                            else json.dumps(measurement["value"], ensure_ascii=False))
                        + " " + measurement.get("unit", "")))
            grounding = item.get("grounding", {})
            if grounding:
                parts.append(Part("status", citation(grounding.get("evidence_ids", [])) + "; " + grounding["label"]))
            if key == "drawing_requirements":
                parts.append(Part("status", labels["figure_notice"]))
        if not parts:
            parts.append(Part("status", "NOT_PROVIDED — HUMAN REVIEW REQUIRED"))
        report.append(Section(key.upper(), vi if template_language == "vi" else en, tuple(parts)))
    claim_parts = [Part("status", CLAIMS_INCOMPLETE)] if not filing["claims"]["claims"] else []
    for item in package["review_package"]["projected_claim_support"]:
        claim_parts.append(Part("prose", f"Claim {item['claim_number']} / {item['element_id']}: " + citation(item["evidence_ids"])))
    report.append(Section("CLAIM_SUPPORT_REVIEW", labels["claims"], tuple(claim_parts)))
    limitations = (Section("PRIOR_ART_LIMITATIONS", labels["prior"], (Part("status", labels["prior_notice"]),)),
                   Section("FIGURE_VALIDATION", labels["figures"], (Part("status", labels["figure_notice"]),)))
    annotated.insert(0, report[0])  # Give every inline citation its actual document/hash context.
    annotated.extend(limitations)
    report.extend(limitations)
    report.append(Section("QUALITY_REVIEW", "Human review", (Part("status",
        "Canonical package and supplied-input consistency validation passed. Scientific meaning, figure fidelity, search completeness, translation and final approval remain HUMAN_REVIEW_REQUIRED."),)))
    bodies = {"PATENT_DRAFT": base.sections, "ANNOTATED_DRAFT": tuple(annotated), "ANALYSIS_REPORT": tuple(report)}
    return {kind: RenderModel(base.title, base.abstract,
        (Section("BUSINESS_DOCUMENT", labels[kind], (Part("status", "DRAFT / HUMAN REVIEW REQUIRED. " + labels["notice"]),)),) + sections,
        base.draft_id) for kind, sections in bodies.items()}


def render_business_document_set(package: Mapping[str, Any], *, source_envelope: Any,
        structured_analysis: Any, reconstruction: Any, specification: Any,
        p2_003_generation_config: Any, supported_claims: Any, p2_004_generation_config: Any,
        output_dir: Path | str, template_language: str = "en") -> dict[str, Path]:
    """Atomic three-document DOCX/PDF set from the existing synthetic trust boundary.

    Template language changes labels only; technical content is never translated.
    The existing four-format API and its filing/review separation remain intact.
    """
    from copy import deepcopy
    import hashlib
    import json
    from backend.app.services.supported_draft_claims_validation import sha256_canonical

    if type(template_language) is not str or template_language not in BUSINESS_LABELS:
        raise ValueError("Unsupported template language")
    candidate = deepcopy(package)
    originals = deepcopy(dict(source_envelope=source_envelope, structured_analysis=structured_analysis,
        reconstruction=reconstruction, specification=specification,
        p2_003_generation_config=p2_003_generation_config, supported_claims=supported_claims,
        p2_004_generation_config=p2_004_generation_config))
    validate_uspto_document_package(candidate, **originals)
    models = _business_models(candidate, originals, template_language)
    for model in models.values():
        if sum(len(part.text) for section in model.sections for part in section.parts) > MAX_FILING_CHARS:
            raise ValueError("Validated business content exceeds renderer limit")
    parent = _assert_safe_parent(Path(output_dir))
    destination = parent / (candidate["package_id"] + "-business-v1-" + template_language)
    if destination.exists():
        raise FileExistsError("Business output directory already exists")
    staging = Path(mkdtemp(prefix=".business-", dir=parent))
    try:
        for kind, model in models.items():
            _pdf(model, staging / (kind + ".pdf"), b2=False)
            _docx(model, staging / (kind + ".docx"), b2=False)
            _business_docx_title(staging / (kind + ".docx"), BUSINESS_LABELS[template_language][kind])
        manifest = {"contract_version": BUSINESS_OUTPUT_VERSION, "status": "DRAFT",
            "review_status": "UNREVIEWED", "filing_ready": False,
            "human_review_required": True, "source_identity": candidate["source_identity"],
            "package_id": candidate["package_id"], "package_sha256": sha256_canonical(candidate),
            "input_digests": candidate["input_digests"], "template_language": template_language,
            "translation_status": "SOURCE_TECHNICAL_TEXT_UNCHANGED_NOT_VALIDATED",
            "prior_art": "NOT_PROVIDED", "figure_fidelity": "REVIEW_REQUIRED",
            "claims_product_runtime_enabled": False,
            "outputs": {name: hashlib.sha256((staging / name).read_bytes()).hexdigest() for name in BUSINESS_FILES}}
        (staging / BUSINESS_MANIFEST).write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if set(item.name for item in staging.iterdir()) != set(BUSINESS_FILES) | {BUSINESS_MANIFEST}:
            raise RuntimeError("Business output set incomplete")
        os.rename(staging, destination)
    finally:
        if staging.exists():
            if not staging.resolve().is_relative_to(parent) or not staging.name.startswith(".business-"):
                raise RuntimeError("Unsafe renderer cleanup path")
            shutil.rmtree(staging)
    return {name: destination / name for name in BUSINESS_FILES + (BUSINESS_MANIFEST,)}
