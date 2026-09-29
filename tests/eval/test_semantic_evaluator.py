"""Synthetic-only arithmetic and provenance tests; no product/provider execution."""

import copy
import hashlib
import json
from pathlib import Path

import pytest

from eval.semantic.v1.tools import evaluator as ev


PACKAGE = Path(__file__).resolve().parents[2] / "eval" / "semantic" / "v1"


def item(gold_id, importance="KEY", category="technical_solution", applicable=True, missing=False):
    return {
        "gold_id": gold_id,
        "category": category,
        "normalized_proposition": gold_id,
        "importance": importance,
        "source_locators": ["PDF p. 1"],
        "supporting_excerpts": [],
        "evaluator_note": "Synthetic test item",
        "coverage_applicable": applicable,
        "missing_information_target": missing,
    }


GOLD_ITEMS = [item("key"), item("secondary", "SECONDARY"),
              item("gap", "SECONDARY", "missing_information", False, True)]


def assertion(assertion_id="a1", support="SUPPORTED_DIRECT", label="SOURCE_FACT", critical=None):
    return {
        "assertion_id": assertion_id,
        "support": support,
        "system_grounding_label": label,
        "expected_grounding_label": ev.EXPECTED_LABEL.get(support) if label is not None else None,
        "critical_categories": critical or [],
        "cited_evidence_ids": ["e1"],
        "evidence_ids_exist": True,
        "cited_evidence_supports": support in ev.SUPPORTED,
    }


def judgments(items=None):
    items = items or GOLD_ITEMS
    gaps = [i["gold_id"] for i in items if i["missing_information_target"]]
    return {
        "review_status": "ACCEPTED",
        "reviewed_by": "Synthetic test evaluator",
        "reviewed_at": "2026-09-28T00:00:00Z",
        "assertion_inventory_complete": True,
        "extraction_assertions": [assertion()],
        "draft_assertions": [assertion("d1", label=None)],
        "gold_coverage": [{"gold_id": i["gold_id"], "covered": True} for i in items if i["coverage_applicable"]],
        "system_gaps": [{"gap_id": "gap-1", "relevant": True, "gold_ids": gaps}] if gaps else [],
        "author_questions": [{"question_id": "q1", "relevant_to_gap": True, "specific_actionable": True,
                              "answerable_by_author": True, "no_unsupported_presupposition": True}] if gaps else [],
        "conflict_handling": [
            {"gold_id": i["gold_id"], "handled_accurately": True}
            for i in items if i["category"] == "ambiguity_conflict"
        ],
        "claims_violations": 0,
        "legal_conclusion_violations": 0,
        "abstract_word_count": 150,
        "schema_business_rule_failures": 0,
    }


def scored(j=None, items=None):
    return ev.score_case("synthetic", items or GOLD_ITEMS, j or judgments(items))


def manifest_and_gold(accepted=False):
    manifest = json.loads((PACKAGE / "manifest.json").read_text(encoding="utf-8"))
    gold = ev.load_gold(PACKAGE)
    if accepted:
        for case in manifest["cases"]:
            case["selection_status"] = "HUMAN_ACCEPTED"
            case["accepted_by"] = "Synthetic test evaluator"
            case["accepted_at"] = "2026-09-28T00:00:00Z"
        for data in gold.values():
            data["review_status"] = "ACCEPTED"
            data["annotation_inventory_complete"] = True
            data["reviewed_by"] = "Synthetic test evaluator"
            data["reviewed_at"] = "2026-09-28T00:00:00Z"
    return manifest, gold


def run_for(case, gold, tmp_path, source="PRODUCT_RUNTIME"):
    local = tmp_path / "runs" / "local"
    local.mkdir(parents=True, exist_ok=True)
    names = {}
    for kind in ("extraction", "draft"):
        name = f"{case['case_id']}-{kind}.json"
        (local / name).write_bytes(b"{}")
        names[kind] = name
    metadata = {
        "run_id": f"synthetic-fixture-{case['case_id']}",
        "case_id": case["case_id"], "source_sha256": case["source_sha256"],
        "repository_baseline_sha": ev.BASELINE,
        "prompt_version": "1.0.0", "schema_version": "1.0.0", "draft_contract_version": "1.0.0",
        "model_identifier": "synthetic-fixture-not-a-provider", "reasoning_config": {"mode": "fixture"},
        "timestamp": "2026-09-28T00:00:00Z",
        "extraction_output_sha256": hashlib.sha256(b"{}").hexdigest(),
        "draft_output_sha256": hashlib.sha256(b"{}").hexdigest(),
        "extraction_output_path": f"runs/local/{names['extraction']}",
        "draft_output_path": f"runs/local/{names['draft']}",
        "run_source": source,
        "provider_authorization_reference": "SYNTHETIC_TEST_ONLY_NOT_REAL_APPROVAL" if source == "PRODUCT_RUNTIME" else None,
    }
    return {"metadata": metadata, "judgments": judgments(gold["items"])}


def test_01_supported_assertion_scoring():
    assert scored()["metrics"]["grounding_support_precision"]["rate"] == 1


def test_02_unsupported_assertion_scoring():
    j = judgments()
    j["extraction_assertions"].append(assertion("a2", "UNSUPPORTED", "SOURCE_FACT"))
    result = scored(j)
    assert result["metrics"]["grounding_support_precision"]["rate"] == 0.5
    assert result["failures"]["unsupported_extraction_assertion_ids"] == ["a2"]


def test_03_contradiction_scoring():
    j = judgments()
    j["extraction_assertions"] = [assertion("a1", "CONTRADICTED", "SOURCE_FACT")]
    assert scored(j)["failures"]["contradicted_extraction_assertion_ids"] == ["a1"]


def test_04_critical_hallucination_non_averagable():
    j = judgments()
    j["draft_assertions"] = [assertion("d1", "UNSUPPORTED", None, ["numeric_value"])]
    cases = [scored(j), scored()]
    aggregate = ev._aggregate(cases)
    assert aggregate["critical_hallucination_count"] == 1
    assert ev.threshold_results(cases, aggregate)["zero_tolerance"] == "FAIL"


def test_05_key_coverage():
    j = judgments()
    j["gold_coverage"][0]["covered"] = False
    assert scored(j)["metrics"]["key_coverage"]["rate"] == 0


def test_06_sparse_output_cannot_game_precision():
    j = judgments()
    j["extraction_assertions"] = []
    j["gold_coverage"][0]["covered"] = False
    result = scored(j)
    gates = ev.threshold_results([result], ev._aggregate([result]))
    assert gates["grounding_support_case"] == "FAIL"
    assert gates["key_coverage_case"] == "FAIL"


def test_07_zero_denominator_is_not_applicable():
    assert ev.ratio(0, 0) == {"numerator": 0, "denominator": 0, "rate": None, "status": "NOT_APPLICABLE"}
    assert ev.meets(ev.ratio(0, 0), 80) is False


def test_08_grounding_label_accuracy():
    j = judgments()
    j["extraction_assertions"].append(assertion("a2", "SUPPORTED_INFERENCE", "SOURCE_FACT"))
    assert scored(j)["metrics"]["grounding_label_accuracy"]["rate"] == 0.5


def test_09_missing_information_precision():
    j = judgments()
    j["system_gaps"].append({"gap_id": "gap-2", "relevant": False, "gold_ids": []})
    assert scored(j)["metrics"]["missing_information_precision"]["rate"] == 0.5


def test_10_missing_information_recall():
    j = judgments()
    j["system_gaps"] = []
    assert scored(j)["metrics"]["missing_information_recall"]["rate"] == 0


def test_11_author_question_usefulness():
    j = judgments()
    j["author_questions"][0]["answerable_by_author"] = False
    assert scored(j)["metrics"]["author_question_usefulness"]["rate"] == 0


def test_12_draft_faithfulness_independent_of_extraction():
    j = judgments()
    j["draft_assertions"] = [assertion("d1", "UNSUPPORTED", None)]
    result = scored(j)
    assert result["metrics"]["grounding_support_precision"]["rate"] == 1
    assert result["metrics"]["draft_supported_assertion_rate"]["rate"] == 0


def test_13_claims_violation():
    j = judgments()
    j["claims_violations"] = 1
    result = scored(j)
    assert ev.threshold_results([result], ev._aggregate([result]))["zero_tolerance"] == "FAIL"


def test_14_legal_conclusion_violation():
    j = judgments()
    j["legal_conclusion_violations"] = 1
    result = scored(j)
    assert ev.threshold_results([result], ev._aggregate([result]))["zero_tolerance"] == "FAIL"


def test_15_abstract_over_150_words():
    j = judgments()
    j["abstract_word_count"] = 151
    assert scored(j)["safety"]["abstract_over_150"] == 1


def test_16_aggregate_uses_micro_average():
    full = scored()
    j = judgments()
    j["extraction_assertions"] = [assertion(f"a{i}", "UNSUPPORTED", "SOURCE_FACT") for i in range(9)]
    poor = scored(j)
    aggregate = ev._aggregate([full, poor])
    assert aggregate["metrics"]["grounding_support_precision"] == ev.ratio(1, 10)


def test_17_per_case_threshold_failure():
    good = scored()
    j = judgments()
    j["gold_coverage"][0]["covered"] = False
    poor = scored(j)
    gates = ev.threshold_results([good, poor], ev._aggregate([good, poor]))
    assert gates["key_coverage_case"] == "FAIL"


def test_18_aggregate_threshold_failure():
    cases = [scored()]
    for _ in range(5):
        j = judgments()
        j["extraction_assertions"] = [assertion("a1", "UNSUPPORTED", "SOURCE_FACT")]
        cases.append(scored(j))
    assert ev.threshold_results(cases, ev._aggregate(cases))["grounding_support_aggregate"] == "FAIL"


def test_19_pending_human_gold_blocks_final_acceptance(tmp_path):
    manifest, gold = manifest_and_gold(accepted=True)
    gold[manifest["cases"][0]["case_id"]]["review_status"] = "PENDING_HUMAN"
    gold[manifest["cases"][0]["case_id"]]["reviewed_by"] = None
    gold[manifest["cases"][0]["case_id"]]["reviewed_at"] = None
    runs = [run_for(c, gold[c["case_id"]], tmp_path) for c in manifest["cases"]]
    report = ev.evaluate(manifest, gold, {"runs": runs}, tmp_path)
    assert report["status"] == "BLOCKED_FOR_HUMAN_ACCEPTANCE"
    assert report["semantic_acceptance"] == "NOT_DETERMINED"


def test_20_no_product_runtime_evidence_is_blocked():
    manifest, gold = manifest_and_gold()
    report = ev.evaluate(manifest, gold)
    assert report["status"] == "BLOCKED_FOR_PRODUCT_RUNTIME_EVIDENCE"
    assert all(v == "NOT_EVALUATED" for v in report["threshold_results"].values())


def test_21_manual_ui_cannot_count(tmp_path):
    manifest, gold = manifest_and_gold()
    case = manifest["cases"][0]
    report = ev.evaluate(manifest, gold, {"runs": [run_for(case, gold[case["case_id"]], tmp_path, "MANUAL_UI")]}, tmp_path)
    assert report["runtime_evidence"]["product_run_count"] == 0
    assert report["status"] == "BLOCKED_FOR_PRODUCT_RUNTIME_EVIDENCE"


def test_22_synthetic_harness_cannot_count(tmp_path):
    manifest, gold = manifest_and_gold()
    case = manifest["cases"][0]
    report = ev.evaluate(manifest, gold, {"runs": [run_for(case, gold[case["case_id"]], tmp_path, "SYNTHETIC_HARNESS")]}, tmp_path)
    assert report["runtime_evidence"]["product_run_count"] == 0
    assert report["runtime_evidence"]["excluded_non_product_runs"][0]["run_source"] == "SYNTHETIC_HARNESS"


def test_23_malformed_input_fails_closed():
    j = judgments()
    del j["gold_coverage"][0]
    with pytest.raises(ev.EvaluationInputError, match="enumerate every applicable"):
        scored(j)


def test_24_run_provenance_and_hash_validation(tmp_path):
    manifest, gold = manifest_and_gold()
    case = manifest["cases"][0]
    metadata = run_for(case, gold[case["case_id"]], tmp_path)["metadata"]
    ev.validate_metadata(metadata, case, tmp_path)
    metadata["draft_output_sha256"] = "0" * 64
    with pytest.raises(ev.EvaluationInputError, match="draft output hash mismatch"):
        ev.validate_metadata(metadata, case, tmp_path)


def test_25_no_human_authorization_reference_fails_closed(tmp_path):
    manifest, gold = manifest_and_gold()
    case = manifest["cases"][0]
    metadata = run_for(case, gold[case["case_id"]], tmp_path)["metadata"]
    metadata["provider_authorization_reference"] = None
    with pytest.raises(ev.EvaluationInputError, match="provider_authorization_reference"):
        ev.validate_metadata(metadata, case, tmp_path)


def test_26_local_source_tampering_detected(tmp_path):
    manifest, _ = manifest_and_gold()
    case = copy.deepcopy(manifest["cases"][0])
    source = tmp_path / case["local_source_path"]
    source.parent.mkdir(parents=True)
    source.write_bytes(b"not the approved paper")
    with pytest.raises(ev.EvaluationInputError, match="source size mismatch"):
        ev.verify_local_sources([case], tmp_path)


def test_27_human_accepted_corpus_does_not_accept_candidate_gold():
    manifest, gold = manifest_and_gold()
    assert {c["case_id"] for c in manifest["cases"]} == {
        "eval-en-002", "eval-en-003", "eval-en-004",
        "eval-en-005", "eval-en-007", "eval-vi-001",
    }
    assert all(c["selection_status"] == "HUMAN_ACCEPTED" for c in manifest["cases"])
    assert all(g["annotation_inventory_complete"] for g in gold.values())
    assert all(g["review_status"] == "PENDING_HUMAN" for g in gold.values())
    assert all(g["reviewed_by"] is None and g["reviewed_at"] is None for g in gold.values())

    report = ev.evaluate(manifest, gold)
    assert report["corpus"]["human_accepted_count"] == 6
    assert report["gold"]["human_accepted_count"] == 0
    assert report["runtime_evidence"]["product_run_count"] == 0
    assert report["semantic_acceptance"] == "NOT_DETERMINED"
    assert "CORPUS_HUMAN_ACCEPTANCE_PENDING" not in report["blocking_conditions"]
    assert {"GOLD_HUMAN_ACCEPTANCE_PENDING", "PRODUCT_RUNTIME_EVIDENCE_ABSENT",
            "PRODUCT_RUNTIME_CASES_MISSING"} <= set(report["blocking_conditions"])
