import re
import unicodedata
from collections.abc import Iterable, Mapping
from typing import Any


class DraftBusinessValidationError(ValueError):
    def __init__(self, code: str, message: str, *, paths: Iterable[str] = ()) -> None:
        super().__init__(message)
        self.code = code
        self.safe_message = message
        self.paths = tuple(paths)


def _resolve_json_pointer(doc: Mapping[str, Any], pointer: str) -> Any:
    # F-D08: JSON POINTER STRICTNESS
    if not isinstance(pointer, str):
        raise TypeError("Pointer must be a string")
    if not pointer.startswith("/"):
        raise ValueError("Pointer must start with /")

    parts = pointer.split("/")[1:]

    current = doc
    for part in parts:
        if "~" in part:
            # Check for invalid escapes like ~2
            if re.search(r"~[^01]", part) or part.endswith("~"):
                raise ValueError(f"Invalid escape in pointer: {part}")
        part = part.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict):
            if part not in current:
                raise KeyError(f"Key '{part}' not found")
            current = current[part]
        elif isinstance(current, list):
            # strict integer parsing
            if not re.match(r"^(0|[1-9][0-9]*)$", part):
                raise ValueError(f"Invalid list index '{part}'")
            idx = int(part)
            if idx < 0 or idx >= len(current):
                raise IndexError(f"Index {idx} out of range")
            current = current[idx]
        else:
            raise TypeError("Cannot traverse scalar")
    return current


def _collect_typed_ids(doc: Any, id_keys: set[str], path: str = "") -> dict[str, dict[str, list[str]]]:
    found = {k: {} for k in id_keys}
    def _visit(node: Any, current_path: str):
        if isinstance(node, dict):
            for k, v in node.items():
                if k in id_keys and isinstance(v, str):
                    found[k].setdefault(v, []).append(f"{current_path}/{k}")
                _visit(v, f"{current_path}/{k}")
        elif isinstance(node, list):
            for i, v in enumerate(node):
                _visit(v, f"{current_path}/{i}")
    _visit(doc, path)
    return found




def _is_prohibited(text: str) -> bool:
    if not isinstance(text, str):
        return False
    normalized = unicodedata.normalize("NFKC", text).casefold()
    prohibited = [
        "is patentable", "is novel", "satisfies novelty", "has an inventive step",
        "is non-obvious", "should be granted", "is eligible for patent protection"
    ]
    return any(p in normalized for p in prohibited)


_SOURCE_ID_KEYS = {
    "field_id", "title_id", "statement_id", "problem_id",
    "solution_id", "component_id", "step_id", "feature_id", "effect_id",
    "embodiment_id", "experiment_id", "drawing_id", "missing_id",
    "question_id", "evidence_id", "draft_id"
}


def _check_source_analysis_rules(
    source_analysis: Mapping[str, Any],
    errors: set[str],
) -> dict[str, dict[str, list[str]]]:
    """Apply the source-side ID and typed-reference rules used by Draft validation."""
    typed_src_ids = _collect_typed_ids(source_analysis, _SOURCE_ID_KEYS)

    all_src_id_values: dict[str, list[str]] = {}
    for ids_dict in typed_src_ids.values():
        for id_val, paths in ids_dict.items():
            all_src_id_values.setdefault(id_val, []).extend(paths)
    for paths in all_src_id_values.values():
        if len(paths) > 1:
            for path in paths:
                errors.add(f"source_analysis{path}")

    def _check_source_typed_refs(node: Any, current_path: str) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "addresses_problem_ids" and isinstance(value, list):
                    for index, reference in enumerate(value):
                        if reference not in typed_src_ids["problem_id"]:
                            errors.add(f"{current_path}/{key}/{index}")
                elif key == "related_component_ids" and isinstance(value, list):
                    for index, reference in enumerate(value):
                        if reference not in typed_src_ids["component_id"]:
                            errors.add(f"{current_path}/{key}/{index}")
                elif key in ("input_component_ids", "output_component_ids", "component_ids") and isinstance(value, list):
                    for index, reference in enumerate(value):
                        if reference not in typed_src_ids["component_id"]:
                            errors.add(f"{current_path}/{key}/{index}")
                elif key in ("related_step_ids", "process_step_ids") and isinstance(value, list):
                    for index, reference in enumerate(value):
                        if reference not in typed_src_ids["step_id"]:
                            errors.add(f"{current_path}/{key}/{index}")
                elif key == "related_solution_ids" and isinstance(value, list):
                    for index, reference in enumerate(value):
                        if reference not in typed_src_ids["solution_id"]:
                            errors.add(f"{current_path}/{key}/{index}")
                elif key == "source_evidence_ids" and isinstance(value, list):
                    for index, reference in enumerate(value):
                        if reference not in typed_src_ids["evidence_id"]:
                            errors.add(f"{current_path}/{key}/{index}")
                elif key == "missing_information_id" and isinstance(value, str):
                    if value not in typed_src_ids["missing_id"]:
                        errors.add(f"{current_path}/{key}")
                elif key == "evidence_ids" and isinstance(value, list):
                    for index, reference in enumerate(value):
                        if reference not in typed_src_ids["evidence_id"]:
                            errors.add(f"{current_path}/{key}/{index}")
                _check_source_typed_refs(value, f"{current_path}/{key}")
        elif isinstance(node, list):
            for index, value in enumerate(node):
                _check_source_typed_refs(value, f"{current_path}/{index}")

    _check_source_typed_refs(source_analysis, "/source_analysis")
    return typed_src_ids


def validate_draft_source_analysis(source_analysis: Mapping[str, Any]) -> None:
    """Fail closed on source-side rules that must hold before a Draft model call."""
    errors: set[str] = set()
    _check_source_analysis_rules(source_analysis, errors)
    if errors:
        raise DraftBusinessValidationError(
            code="draft_input_invalid",
            message="The source analysis failed deterministic Draft input validation.",
            paths=sorted(errors)[:10],
        )


def validate_draft_business_rules(
    draft: Mapping[str, Any],
    source_analysis: Mapping[str, Any],
    *,
    selected_title_candidate_id: str | None,
) -> None:
    errors = set()

    def _err(path: str):
        errors.add(path)

    # 4. SOURCE METADATA EXACT MATCH
    dm_draft = draft.get("document_metadata", {})
    if dm_draft.get("source_document") != source_analysis.get("document_metadata"):
        _err("/document_metadata")

    # 11. GLOBAL LOGICAL ID UNIQUENESS
    draft_id_keys = {
        "paragraph_id", "drawing_id", "missing_id",
        "conflict_id", "question_id", "evidence_id", "draft_id"
    }

    typed_src_ids = _check_source_analysis_rules(source_analysis, errors)
    typed_draft_ids = _collect_typed_ids(draft, draft_id_keys)

    all_draft_id_values = {}
    for k, ids_dict in typed_draft_ids.items():
        for id_val, paths in ids_dict.items():
            all_draft_id_values.setdefault(id_val, []).extend(paths)
    for id_val, paths in all_draft_id_values.items():
        if len(paths) > 1:
            for p in paths:
                _err(p)

    # 5. SOURCE JSON POINTERS & 6. TECHNICAL PARAGRAPH SOURCE PATH RESTRICTIONS
    def _check_source_paths(node: Any, current_path: str):
        if isinstance(node, dict):
            for k, v in node.items():
                if k == "source_paths" and isinstance(v, list):
                    for i, p in enumerate(v):
                        try:
                            _resolve_json_pointer(source_analysis, p)
                            if "paragraph" in current_path:
                                if p == "/document_metadata" or p == "/evidence" or \
                                   p.startswith("/document_metadata/") or p.startswith("/evidence/"):
                                    _err(f"{current_path}/{k}/{i}")
                        except Exception:
                            _err(f"{current_path}/{k}/{i}")
                elif k == "target_path" and isinstance(v, str):
                    try:
                        _resolve_json_pointer(source_analysis, v)
                    except Exception:
                        _err(f"{current_path}/{k}")
                _check_source_paths(v, f"{current_path}/{k}")
        elif isinstance(node, list):
            for i, v in enumerate(node):
                _check_source_paths(v, f"{current_path}/{i}")

    _check_source_paths(draft, "")

    # F-D01: SELECTED TITLE — EXACT IDENTITY & 22. TITLE MISSING LINKAGE
    title_node = draft.get("selected_title", {})
    if _is_prohibited(title_node.get("text", "")):
        _err("/selected_title/text")

    cands = source_analysis.get("title_candidates", [])
    found_cand = None
    if selected_title_candidate_id:
        for c in cands:
            if c.get("title_id") == selected_title_candidate_id:
                found_cand = c
                break

    if found_cand:
        if title_node.get("status") != "PRESENT":
            _err("/selected_title/status")
        if title_node.get("source_title_candidate_id") != selected_title_candidate_id:
            _err("/selected_title/source_title_candidate_id")
        if title_node.get("text") != found_cand.get("title"):
            _err("/selected_title/text")
        draft_ev = title_node.get("grounding", {}).get("evidence_ids", [])
        src_ev = found_cand.get("grounding", {}).get("evidence_ids", [])
        if sorted(draft_ev) != sorted(src_ev):
            _err("/selected_title/grounding/evidence_ids")
        for i, sp in enumerate(title_node.get("source_paths", [])):
            try:
                resolved = _resolve_json_pointer(source_analysis, sp)
                if resolved != found_cand:
                    _err(f"/selected_title/source_paths/{i}")
            except Exception:
                _err(f"/selected_title/source_paths/{i}")
    else:
        # Invalid or absent candidate ID
        if title_node.get("status") != "MISSING":
            _err("/selected_title/status")
        if title_node.get("marker") != "[AUTHOR CONFIRMATION REQUIRED]":
            _err("/selected_title/marker")

        title_miss_ids = title_node.get("missing_information_ids", [])
        found_rule = False
        for mid in title_miss_ids:
            for m in draft.get("missing_information", []):
                if m.get("missing_id") == mid and m.get("rule_id") == "TITLE_SELECTION_REQUIRED":
                    found_rule = True
                    break
        if not found_rule:
            _err("/selected_title/missing_information_ids")

    # 8. SECTION ORDER
    expected_root = [
        "COVER_AND_DRAFT_NOTICE", "TITLE", "ABSTRACT", "TECHNICAL_FIELD", "BACKGROUND",
        "SUMMARY_OF_TECHNICAL_DISCLOSURE", "BRIEF_DESCRIPTION_OF_DRAWINGS", "DETAILED_DESCRIPTION",
        "EXPERIMENTAL_EXAMPLES_AND_RESULTS", "MISSING_INFORMATION_AND_AUTHOR_QUESTIONS",
        "EVIDENCE_AND_REFERENCE_APPENDIX"
    ]
    if draft.get("section_order") != expected_root:
        _err("/section_order")

    draft_secs = draft.get("draft_sections", [])
    expected_secs = [
        "TECHNICAL_FIELD", "BACKGROUND", "SUMMARY_OF_TECHNICAL_DISCLOSURE",
        "BRIEF_DESCRIPTION_OF_DRAWINGS", "DETAILED_DESCRIPTION", "EXPERIMENTAL_EXAMPLES_AND_RESULTS"
    ]
    if len(draft_secs) != len(expected_secs):
        _err("/draft_sections")
    else:
        for i, expected in enumerate(expected_secs):
            if draft_secs[i].get("section_id") != expected:
                _err(f"/draft_sections/{i}/section_id")

        if len(draft_secs) > 2:
            sum_subsec = draft_secs[2].get("subsections", [])
            expected_sum_subsec = ["TECHNICAL_PROBLEMS", "TECHNICAL_SOLUTIONS", "POTENTIAL_DISTINGUISHING_FEATURES", "TECHNICAL_EFFECTS"]
            if len(sum_subsec) != len(expected_sum_subsec):
                _err("/draft_sections/2/subsections")
            else:
                for i, expected in enumerate(expected_sum_subsec):
                    if sum_subsec[i].get("subsection_id") != expected:
                        _err(f"/draft_sections/2/subsections/{i}/subsection_id")

        if len(draft_secs) > 4:
            dd_subsec = draft_secs[4].get("subsections", [])
            expected_dd_subsec = ["COMPONENTS_OR_SYSTEM", "PROCESS_OR_METHOD_STEPS", "EMBODIMENTS"]
            if len(dd_subsec) != len(expected_dd_subsec):
                _err("/draft_sections/4/subsections")
            else:
                for i, expected in enumerate(expected_dd_subsec):
                    if dd_subsec[i].get("subsection_id") != expected:
                        _err(f"/draft_sections/4/subsections/{i}/subsection_id")

    # 9. PARAGRAPH SEQUENCE & 21. MISSING SECTION INVARIANTS & 25. PROHIBITED CONTENT SCANNER
    def _check_paragraphs(paras: list, path: str):
        for i, p in enumerate(paras):
            if p.get("sequence") != i + 1:
                _err(f"{path}/{i}/sequence")
            if _is_prohibited(p.get("text", "")):
                _err(f"{path}/{i}/text")

    for i, sec in enumerate(draft_secs):
        if sec.get("status") == "PRESENT":
            _check_paragraphs(sec.get("paragraphs", []), f"/draft_sections/{i}/paragraphs")
            if "marker" in sec:
                _err(f"/draft_sections/{i}/marker")
        else:
            if sec.get("paragraphs"):
                _err(f"/draft_sections/{i}/paragraphs")
            if sec.get("marker") != "[AUTHOR CONFIRMATION REQUIRED]":
                _err(f"/draft_sections/{i}/marker")
            if not sec.get("missing_information_ids"):
                _err(f"/draft_sections/{i}/missing_information_ids")

        for j, subsec in enumerate(sec.get("subsections", [])):
            if subsec.get("status") == "PRESENT":
                _check_paragraphs(subsec.get("paragraphs", []), f"/draft_sections/{i}/subsections/{j}/paragraphs")
                if "marker" in subsec:
                    _err(f"/draft_sections/{i}/subsections/{j}/marker")
            else:
                if subsec.get("paragraphs"):
                    _err(f"/draft_sections/{i}/subsections/{j}/paragraphs")
                if subsec.get("marker") != "[AUTHOR CONFIRMATION REQUIRED]":
                    _err(f"/draft_sections/{i}/subsections/{j}/marker")
                if not subsec.get("missing_information_ids"):
                    _err(f"/draft_sections/{i}/subsections/{j}/missing_information_ids")

    # 10. ABSTRACT WORD COUNT & 23. ABSTRACT MISSING LINKAGE & 25
    abs_node = draft.get("abstract", {})
    if abs_node.get("status") == "PRESENT":
        text = abs_node.get("text", "")
        if _is_prohibited(text):
            _err("/abstract/text")
        text_norm = unicodedata.normalize("NFKC", text)
        words = re.findall(r"\b\w+(?:[-'’]\w+)*\b", text_norm, flags=re.UNICODE)
        if abs_node.get("word_count") != len(words):
            _err("/abstract/word_count")
        if len(words) > 150:
            _err("/abstract/word_count")
    else:
        found_rule = False
        for mid in abs_node.get("missing_information_ids", []):
            for m in draft.get("missing_information", []):
                if m.get("missing_id") == mid:
                    if m.get("origin") == "DRAFT_VALIDATION" and m.get("rule_id") == "ABSTRACT_SOURCE_INSUFFICIENT":
                        found_rule = True
                        break
            if found_rule:
                break
        if not found_rule:
            _err("/abstract/missing_information_ids")

    # 13. SOURCE MISSING INFORMATION PROPAGATION
    for i, m in enumerate(draft.get("missing_information", [])):
        if m.get("origin") == "SOURCE_ANALYSIS":
            smid = m.get("source_missing_information_id")
            if not smid or smid not in typed_src_ids["missing_id"]:
                _err(f"/missing_information/{i}/source_missing_information_id")
            else:
                found_src = None
                for sm in source_analysis.get("missing_information", []):
                    if sm.get("missing_id") == smid:
                        found_src = sm
                        break
                if found_src:
                    if m.get("description") != found_src.get("description"): _err(f"/missing_information/{i}/description")
                    if m.get("reason") != found_src.get("reason"): _err(f"/missing_information/{i}/reason")
                    if m.get("impact") != found_src.get("impact"): _err(f"/missing_information/{i}/impact")
                    if m.get("owner") != found_src.get("owner"): _err(f"/missing_information/{i}/owner")
                    try:
                        _resolve_json_pointer(source_analysis, m.get("target_path", ""))
                    except Exception:
                        _err(f"/missing_information/{i}/target_path")

    # F-D04: AUTHOR QUESTION SOURCE-MISSING LINKAGE
    for i, q in enumerate(draft.get("author_questions", [])):
        if q.get("origin") == "SOURCE_ANALYSIS":
            sqid = q.get("source_question_id")
            if not sqid or sqid not in typed_src_ids["question_id"]:
                _err(f"/author_questions/{i}/source_question_id")
            else:
                found_sq = None
                for sq in source_analysis.get("author_questions", []):
                    if sq.get("question_id") == sqid:
                        found_sq = sq
                        break
                if found_sq:
                    if q.get("question") != found_sq.get("question"): _err(f"/author_questions/{i}/question")
                    if q.get("priority") != found_sq.get("priority"): _err(f"/author_questions/{i}/priority")
                    for j, sp in enumerate(q.get("source_paths", [])):
                        if sp != f"/author_questions/{source_analysis.get('author_questions', []).index(found_sq)}":
                            _err(f"/author_questions/{i}/source_paths/{j}")

                    smid = found_sq.get("missing_information_id")
                    if smid:
                        draft_mid = None
                        for m in draft.get("missing_information", []):
                            if m.get("origin") == "SOURCE_ANALYSIS" and m.get("source_missing_information_id") == smid:
                                draft_mid = m.get("missing_id")
                                break
                        if not draft_mid or draft_mid not in q.get("related_missing_information_ids", []):
                            _err(f"/author_questions/{i}/related_missing_information_ids")

    # F-D03: TYPED DRAFT REFERENCE INTEGRITY
    def _check_draft_typed_refs(node: Any, current_path: str):
        if isinstance(node, dict):
            for k, v in node.items():
                if k in ("missing_information_ids", "related_missing_information_ids") and isinstance(v, list):
                    for i, ref in enumerate(v):
                        if ref not in typed_draft_ids["missing_id"]: _err(f"{current_path}/{k}/{i}")
                elif k == "author_question_ids" and isinstance(v, list):
                    for i, ref in enumerate(v):
                        if ref not in typed_draft_ids["question_id"]: _err(f"{current_path}/{k}/{i}")
                elif k == "related_conflict_ids" and isinstance(v, list):
                    for i, ref in enumerate(v):
                        if ref not in typed_draft_ids["conflict_id"]: _err(f"{current_path}/{k}/{i}")
                elif k == "source_question_id" and isinstance(v, str):
                    if v not in typed_src_ids["question_id"]: _err(f"{current_path}/{k}")
                elif k == "source_missing_information_id" and isinstance(v, str):
                    if v not in typed_src_ids["missing_id"]: _err(f"{current_path}/{k}")
                elif k == "source_drawing_id" and isinstance(v, str):
                    if v not in typed_src_ids["drawing_id"]: _err(f"{current_path}/{k}")
                _check_draft_typed_refs(v, f"{current_path}/{k}")
        elif isinstance(node, list):
            for i, v in enumerate(node):
                _check_draft_typed_refs(v, f"{current_path}/{i}")

    _check_draft_typed_refs(draft, "")

    # 16. CONFLICTS & 24. CONFLICT MISSING LINKAGE
    for i, conflict in enumerate(draft.get("conflicts", [])):
        if conflict.get("resolution_status") != "UNRESOLVED":
            _err(f"/conflicts/{i}/resolution_status")
        ev_ids = conflict.get("evidence_ids", [])
        if len(set(ev_ids)) < 2:
            _err(f"/conflicts/{i}/evidence_ids")
        for ev in ev_ids:
            if ev not in typed_src_ids["evidence_id"]:
                _err(f"/conflicts/{i}/evidence_ids")
        if not conflict.get("author_question_ids"):
            _err(f"/conflicts/{i}/author_question_ids")
        if _is_prohibited(conflict.get("summary", "")):
            _err(f"/conflicts/{i}/summary")

    # F-D05: DRAWING INVARIANTS
    for i, d in enumerate(draft.get("drawings", [])):
        sdid = d.get("source_drawing_id")
        if sdid:
            found_sd = None
            for sd in source_analysis.get("drawing_requirements", []):
                if sd.get("drawing_id") == sdid:
                    found_sd = sd
                    break
            if not found_sd:
                _err(f"/drawings/{i}/source_drawing_id")
            else:
                if d.get("kind") != found_sd.get("kind"): _err(f"/drawings/{i}/kind")
                if d.get("status") != found_sd.get("status"): _err(f"/drawings/{i}/status")
                if d.get("title") != found_sd.get("title"): _err(f"/drawings/{i}/title")

                # Check human_confirmation_required deterministic copy
                if d.get("human_confirmation_required") != found_sd.get("human_confirmation_required"):
                    _err(f"/drawings/{i}/human_confirmation_required")

                if found_sd.get("status") in ("PROPOSED", "MISSING") or found_sd.get("kind") == "PROPOSED_DRAWING":
                    if not found_sd.get("human_confirmation_required"):
                        # Ensure we validate source requirement correctness too if needed,
                        # but mainly check draft consistency. Wait, prompt says:
                        # "For source kind PROPOSED_DRAWING or status MISSING: human_confirmation_required must remain true."
                        if not d.get("human_confirmation_required"):
                            _err(f"/drawings/{i}/human_confirmation_required")

                if found_sd.get("kind") == "SOURCE_FIGURE":
                    src_ev_ids = found_sd.get("source_evidence_ids", [])
                    draft_ev_ids = d.get("evidence_ids", [])
                    if sorted(src_ev_ids) != sorted(draft_ev_ids):
                        _err(f"/drawings/{i}/evidence_ids")

    # F-D06: EVIDENCE SOURCE CLOSURE
    src_ev_dict = {e.get("evidence_id"): e for e in source_analysis.get("evidence", []) if e.get("evidence_id")}

    used_evidence = set()
    used_evidence.update(title_node.get("grounding", {}).get("evidence_ids", []))
    used_evidence.update(abs_node.get("grounding", {}).get("evidence_ids", []))
    for sec in draft_secs:
        for p in sec.get("paragraphs", []):
            used_evidence.update(p.get("grounding", {}).get("evidence_ids", []))
        for subsec in sec.get("subsections", []):
            for p in subsec.get("paragraphs", []):
                used_evidence.update(p.get("grounding", {}).get("evidence_ids", []))
    for d in draft.get("drawings", []):
        used_evidence.update(d.get("evidence_ids", []))
    for c in draft.get("conflicts", []):
        used_evidence.update(c.get("evidence_ids", []))

    # All used evidence MUST exist in source_analysis["evidence"] specifically
    for eid in used_evidence:
        if eid not in src_ev_dict:
            _err(f"/evidence_appendix") # or a specific grounding path

    appendix_ev = draft.get("evidence_appendix", [])
    appendix_ids = {e.get("evidence_id") for e in appendix_ev if e.get("evidence_id")}

    for eid in appendix_ids:
        if eid not in src_ev_dict:
            _err("/evidence_appendix")

    if used_evidence != appendix_ids:
        _err("/evidence_appendix")

    for i, e in enumerate(appendix_ev):
        eid = e.get("evidence_id")
        if eid in src_ev_dict:
            src_e = src_ev_dict[eid]
            if e.get("document_id") != src_e.get("document_id"): _err(f"/evidence_appendix/{i}/document_id")
            if e.get("evidence_type") != src_e.get("evidence_type"): _err(f"/evidence_appendix/{i}/evidence_type")
            if e.get("locator") != src_e.get("locator"): _err(f"/evidence_appendix/{i}/locator")
            if e.get("excerpt") != src_e.get("excerpt"): _err(f"/evidence_appendix/{i}/excerpt")

    # 20. REVERSE USAGE
    expected_usage = {eid: set() for eid in used_evidence}

    for eid in title_node.get("grounding", {}).get("evidence_ids", []):
        if eid in expected_usage:
            expected_usage[eid].add(("SELECTED_TITLE", selected_title_candidate_id))
    for eid in abs_node.get("grounding", {}).get("evidence_ids", []):
        if eid in expected_usage:
            expected_usage[eid].add(("ABSTRACT", "abstract"))
    for sec in draft_secs:
        for p in sec.get("paragraphs", []):
            for eid in p.get("grounding", {}).get("evidence_ids", []):
                if eid in expected_usage:
                    expected_usage[eid].add(("PARAGRAPH", p.get("paragraph_id")))
        for subsec in sec.get("subsections", []):
            for p in subsec.get("paragraphs", []):
                for eid in p.get("grounding", {}).get("evidence_ids", []):
                    if eid in expected_usage:
                        expected_usage[eid].add(("PARAGRAPH", p.get("paragraph_id")))
    for d in draft.get("drawings", []):
        for eid in d.get("evidence_ids", []):
            if eid in expected_usage:
                expected_usage[eid].add(("DRAWING", d.get("drawing_id")))
    for c in draft.get("conflicts", []):
        for eid in c.get("evidence_ids", []):
            if eid in expected_usage:
                expected_usage[eid].add(("CONFLICT", c.get("conflict_id")))

    for i, e in enumerate(appendix_ev):
        eid = e.get("evidence_id")
        if eid in expected_usage:
            actual = set()
            for ref in e.get("usage_references", []):
                actual.add((ref.get("target_type"), ref.get("target_id")))
            if actual != expected_usage[eid]:
                _err(f"/evidence_appendix/{i}/usage_references")

    if errors:
        sorted_errors = sorted(list(errors))
        raise DraftBusinessValidationError(
            code="draft_business_validation_failed",
            message="The model output failed deterministic business validation.",
            paths=sorted_errors[:10],
        )
