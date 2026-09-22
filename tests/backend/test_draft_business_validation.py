"""Tests for deterministic business validation of drafts."""

import json
from pathlib import Path
import pytest

from backend.app.services.draft_business_validation import (
    validate_draft_business_rules,
    DraftBusinessValidationError,
)

FIXTURE_DIR = Path(__file__).resolve().parents[2] / "tests" / "fixtures" / "patent-draft" / "v1.0.0" / "cases"

FIXTURE_FILES = [
    "representative.json",
    "missing-information.json",
    "conflicting-evidence.json",
    "prompt-injection.json"
]

def load_fixture(name: str) -> dict:
    with (FIXTURE_DIR / name).open(encoding="utf-8") as f:
        return json.load(f)

@pytest.mark.parametrize("fixture_name", FIXTURE_FILES)
def test_all_fixtures_pass(fixture_name):
    data = load_fixture(fixture_name)
    source_analysis = data["input"]["source_analysis"]
    draft = data["expected_output"]
    title_id = data["input"]["generation_config"].get("selected_title_candidate_id")
@pytest.mark.parametrize("fixture_name", FIXTURE_FILES)
def test_all_fixtures_pass(fixture_name):
    data = load_fixture(fixture_name)
    source_analysis = data["input"]["source_analysis"]
    draft = data["expected_output"]
    title_id = data["input"]["generation_config"].get("selected_title_candidate_id")
    try:
        validate_draft_business_rules(draft, source_analysis, selected_title_candidate_id=title_id)
    except DraftBusinessValidationError as e:
        print("FAILED PATHS:", e.paths)
        raise

import copy

def run_failure_test(modifier_func, expected_paths, title_id="title-calibration"):
    data = load_fixture("representative.json")
    draft = copy.deepcopy(data["expected_output"])
    source = copy.deepcopy(data["input"]["source_analysis"])
    
    modifier_func(draft, source)
    
    with pytest.raises(DraftBusinessValidationError) as exc_info:
        validate_draft_business_rules(draft, source, selected_title_candidate_id=title_id)
        
    actual_paths = exc_info.value.paths
    for ep in expected_paths:
        assert ep in actual_paths, f"Expected {ep} in {actual_paths}"

def test_metadata_mismatch():
    def mod(d, s): d["document_metadata"]["source_document"]["file_name"] = "wrong.pdf"
    run_failure_test(mod, ["/document_metadata"])

def test_invalid_json_pointer():
    def mod(d, s): d["selected_title"]["source_paths"].append("/invalid/path")
    run_failure_test(mod, ["/selected_title/source_paths/1"])

def test_technical_paragraph_restricted_source_path():
    def mod(d, s): d["draft_sections"][0]["paragraphs"][0]["source_paths"].append("/document_metadata")
    run_failure_test(mod, ["/draft_sections/0/paragraphs/0/source_paths/1"])

def test_selected_title_status_missing_when_candidate_provided():
    def mod(d, s): d["selected_title"]["status"] = "MISSING"
    run_failure_test(mod, ["/selected_title/status"])

def test_selected_title_wrong_candidate_id():
    def mod(d, s): d["selected_title"]["source_title_candidate_id"] = "wrong-id"
    run_failure_test(mod, ["/selected_title/source_title_candidate_id"])

def test_selected_title_text_mismatch():
    def mod(d, s): d["selected_title"]["text"] = "Wrong Text"
    run_failure_test(mod, ["/selected_title/text"])

def test_selected_title_grounding_mismatch():
    def mod(d, s): d["selected_title"]["grounding"]["evidence_ids"].append("ev-wrong")
    run_failure_test(mod, ["/selected_title/grounding/evidence_ids"])

def test_selected_title_status_present_when_no_candidate():
    def mod(d, s): pass
    run_failure_test(mod, ["/selected_title/status"], title_id=None)

def test_selected_title_missing_linkage_fail():
    def mod(d, s): 
        d["selected_title"]["status"] = "MISSING"
        d["selected_title"]["marker"] = "[AUTHOR CONFIRMATION REQUIRED]"
        d["selected_title"]["missing_information_ids"] = []
    run_failure_test(mod, ["/selected_title/missing_information_ids"], title_id=None)

def test_section_order_wrong():
    def mod(d, s): d["section_order"][0] = "TITLE"
    run_failure_test(mod, ["/section_order"])

def test_draft_sections_length():
    def mod(d, s): d["draft_sections"].pop()
    run_failure_test(mod, ["/draft_sections"])

def test_draft_sections_wrong_id():
    def mod(d, s): d["draft_sections"][0]["section_id"] = "BACKGROUND"
    run_failure_test(mod, ["/draft_sections/0/section_id"])

def test_draft_subsections_length():
    def mod(d, s): d["draft_sections"][2]["subsections"].pop()
    run_failure_test(mod, ["/draft_sections/2/subsections"])

def test_paragraph_sequence_gap():
    def mod(d, s): d["draft_sections"][0]["paragraphs"][0]["sequence"] = 2
    run_failure_test(mod, ["/draft_sections/0/paragraphs/0/sequence"])

def test_paragraph_prohibited_content():
    def mod(d, s): d["draft_sections"][0]["paragraphs"][0]["text"] += " This is patentable."
    run_failure_test(mod, ["/draft_sections/0/paragraphs/0/text"])

def test_abstract_prohibited_content():
    def mod(d, s): d["abstract"]["text"] += " It satisfies novelty."
    run_failure_test(mod, ["/abstract/text"])

def test_abstract_word_count_mismatch():
    def mod(d, s): d["abstract"]["word_count"] = 999
    run_failure_test(mod, ["/abstract/word_count"])

def test_abstract_missing_linkage_fail():
    def mod(d, s):
        d["abstract"] = {"status": "MISSING", "marker": "[AUTHOR CONFIRMATION REQUIRED]", "missing_information_ids": []}
    run_failure_test(mod, ["/abstract/missing_information_ids"])

def test_global_logical_id_uniqueness_draft():
    def mod(d, s): d["draft_sections"][0]["paragraphs"][0]["paragraph_id"] = d["draft_sections"][1]["paragraphs"][0]["paragraph_id"]
    run_failure_test(mod, ["/draft_sections/0/paragraphs/0/paragraph_id"])

def test_global_logical_id_uniqueness_source():
    def mod(d, s): s["technical_problems"][0]["problem_id"] = s["technical_solutions"][0]["solution_id"]
    run_failure_test(mod, ["source_analysis/technical_problems/0/problem_id"])

def test_source_cross_reference_defensive_check():
    def mod(d, s): s["technical_solutions"][0]["addresses_problem_ids"].append("wrong-id")
    run_failure_test(mod, ["source_analysis/technical_solutions/0/addresses_problem_ids/1"])

def test_draft_reference_integrity():
    def mod(d, s): d["missing_information"].append({
        "missing_id": "m2", "origin": "DRAFT_VALIDATION", "rule_id": "TITLE_SELECTION_REQUIRED", 
        "target_path": "/", "description": "", "reason": "NOT_FOUND", "impact": "HIGH", "owner": "AUTHOR", 
        "grounding_label": "MISSING", "affected_section_ids": ["TITLE"], 
        "related_missing_information_ids": ["invalid-id"]
    })
    run_failure_test(mod, ["/missing_information/0/related_missing_information_ids/0"])

def test_source_missing_information_propagation_id():
    def mod(d, s):
        d["missing_information"].append({
            "missing_id": "m3", "origin": "SOURCE_ANALYSIS", "source_missing_information_id": "invalid-src",
            "target_path": "/", "description": "", "reason": "NOT_FOUND", "impact": "HIGH", "owner": "AUTHOR", 
            "grounding_label": "MISSING", "affected_section_ids": ["TITLE"]
        })
    run_failure_test(mod, ["/missing_information/0/source_missing_information_id"])

def test_source_missing_information_propagation_mismatch():
    def mod(d, s):
        s["missing_information"] = [{
            "missing_id": "sm1", "target_path": "/", "description": "desc", "reason": "NOT_FOUND", "impact": "HIGH", "owner": "AUTHOR"
        }]
        d["missing_information"].append({
            "missing_id": "m4", "origin": "SOURCE_ANALYSIS", "source_missing_information_id": "sm1",
            "target_path": "/", "description": "wrong desc", "reason": "NOT_FOUND", "impact": "HIGH", "owner": "AUTHOR", 
            "grounding_label": "MISSING", "affected_section_ids": ["TITLE"]
        })
    run_failure_test(mod, ["/missing_information/0/description"])

def test_source_author_question_propagation_id():
    def mod(d, s):
        d["author_questions"].append({
            "question_id": "q1", "origin": "SOURCE_ANALYSIS", "source_question_id": "invalid-sq",
            "question": "?", "priority": "HIGH", "source_paths": []
        })
    run_failure_test(mod, ["/author_questions/0/source_question_id"])

def test_source_author_question_propagation_mismatch():
    def mod(d, s):
        s["author_questions"] = [{
            "question_id": "sq1", "question": "?", "priority": "HIGH"
        }]
        d["author_questions"].append({
            "question_id": "q2", "origin": "SOURCE_ANALYSIS", "source_question_id": "sq1",
            "question": "wrong?", "priority": "HIGH", "source_paths": ["/author_questions/0"]
        })
    run_failure_test(mod, ["/author_questions/0/question"])

def test_conflict_resolution_status():
    def mod(d, s):
        d["conflicts"].append({
            "conflict_id": "c1", "resolution_status": "RESOLVED", "evidence_ids": ["ev-1", "ev-2"], 
            "author_question_ids": ["q1"], "summary": "c"
        })
    run_failure_test(mod, ["/conflicts/0/resolution_status"])

def test_conflict_evidence_ids_length():
    def mod(d, s):
        ev = s["evidence"][0]["evidence_id"]
        d["conflicts"].append({
            "conflict_id": "c1", "resolution_status": "UNRESOLVED", "evidence_ids": [ev], 
            "author_question_ids": ["q1"], "summary": "c"
        })
    run_failure_test(mod, ["/conflicts/0/evidence_ids"])

def test_conflict_evidence_ids_invalid():
    def mod(d, s):
        ev = s["evidence"][0]["evidence_id"]
        d["conflicts"].append({
            "conflict_id": "c1", "resolution_status": "UNRESOLVED", "evidence_ids": [ev, "invalid-ev"], 
            "author_question_ids": ["q1"], "summary": "c"
        })
    run_failure_test(mod, ["/conflicts/0/evidence_ids"])

def test_conflict_prohibited_summary():
    def mod(d, s):
        ev = s["evidence"][0]["evidence_id"]
        ev2 = s["evidence"][1]["evidence_id"]
        d["conflicts"].append({
            "conflict_id": "c1", "resolution_status": "UNRESOLVED", "evidence_ids": [ev, ev2], 
            "author_question_ids": ["q1"], "summary": "is patentable"
        })
        d["author_questions"].append({"question_id": "q1", "origin": "DRAFT_VALIDATION", "question": "", "priority": "HIGH"})
    run_failure_test(mod, ["/conflicts/0/summary"])

def test_drawing_source_drawing_id_invalid():
    def mod(d, s):
        d["drawings"].append({"drawing_id": "dr1", "source_drawing_id": "invalid-sd", "kind": "BLOCK_DIAGRAM", "status": "PRESENT", "title": "t", "evidence_ids": []})
    run_failure_test(mod, ["/drawings/1/source_drawing_id"])

def test_drawing_source_drawing_mismatch():
    def mod(d, s):
        s["drawing_requirements"][0] = {"drawing_id": "sd1", "kind": "BLOCK_DIAGRAM", "status": "PRESENT", "title": "t"}
        d["drawings"][0] = {"drawing_id": "dr1", "source_drawing_id": "sd1", "kind": "FLOWCHART", "status": "PRESENT", "title": "t", "evidence_ids": []}
    run_failure_test(mod, ["/drawings/0/kind"])

def test_evidence_appendix_closed_set():
    def mod(d, s):
        d["evidence_appendix"].append({"evidence_id": "ev-extra", "document_id": "d", "evidence_type": "TEXT", "locator": "l", "excerpt": "e", "usage_references": []})
    run_failure_test(mod, ["/evidence_appendix"])

def test_evidence_appendix_exact_copy():
    def mod(d, s):
        d["evidence_appendix"][0]["excerpt"] = "wrong"
    run_failure_test(mod, ["/evidence_appendix/0/excerpt"])

def test_reverse_usage():
    def mod(d, s):
        d["evidence_appendix"][0]["usage_references"].append({"target_type": "PARAGRAPH", "target_id": "wrong-para"})
    run_failure_test(mod, ["/evidence_appendix/0/usage_references"])

def test_missing_section_paragraphs_present():
    def mod(d, s):
        d["draft_sections"][1]["status"] = "MISSING"
        d["draft_sections"][1]["marker"] = "[AUTHOR CONFIRMATION REQUIRED]"
        d["draft_sections"][1]["missing_information_ids"] = ["m1"]
    run_failure_test(mod, ["/draft_sections/1/paragraphs"])

def test_missing_section_missing_marker():
    def mod(d, s):
        d["draft_sections"][1]["status"] = "MISSING"
        d["draft_sections"][1]["paragraphs"] = []
        d["draft_sections"][1]["missing_information_ids"] = ["m1"]
    run_failure_test(mod, ["/draft_sections/1/marker"])

