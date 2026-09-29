"""Deterministic EVAL-001 accounting; semantic labels come from Human review."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


BASELINE = "37d42fc8b07003aa2a67f2d1d32e64e69eb0ddb5"
PACKAGE = Path(__file__).resolve().parents[1]
SUPPORT_LABELS = {
    "SUPPORTED_DIRECT", "SUPPORTED_PARAPHRASE", "SUPPORTED_INFERENCE",
    "UNSUPPORTED", "CONTRADICTED", "NOT_APPLICABLE",
}
SUPPORTED = {"SUPPORTED_DIRECT", "SUPPORTED_PARAPHRASE", "SUPPORTED_INFERENCE"}
SYSTEM_LABELS = {"SOURCE_FACT", "PARAPHRASE", "INFERENCE"}
EXPECTED_LABEL = {
    "SUPPORTED_DIRECT": "SOURCE_FACT",
    "SUPPORTED_PARAPHRASE": "PARAPHRASE",
    "SUPPORTED_INFERENCE": "INFERENCE",
}
CRITICAL_CATEGORIES = {
    "numeric_value", "unit", "parameter", "experimental_outcome", "component_material",
    "process_step", "causal_technical_effect", "comparison_superiority",
    "embodiment_variant", "source_attribution", "legal_patentability_conclusion",
}
GOLD_CATEGORIES = {
    "technical_field", "technical_problem", "technical_solution", "component",
    "process_step", "distinguishing_feature", "technical_effect", "experimental_data",
    "embodiment_example", "missing_information", "ambiguity_conflict",
    "prohibited_conclusion",
}
HEX64 = re.compile(r"^[0-9a-f]{64}$")
THRESHOLDS = {
    "grounding_support_aggregate": 98,
    "grounding_support_case": 95,
    "key_coverage_aggregate": 85,
    "key_coverage_case": 75,
    "grounding_label_accuracy": 90,
    "missing_precision": 80,
    "missing_recall": 80,
    "author_question_usefulness": 80,
    "draft_support_aggregate": 97,
    "draft_support_case": 93,
}


class EvaluationInputError(ValueError):
    """Malformed or inconsistent evaluation evidence; fail closed."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise EvaluationInputError(message)


def _object(value: Any, name: str) -> dict[str, Any]:
    _require(isinstance(value, dict), f"{name} must be an object")
    return value


def _list(value: Any, name: str) -> list[Any]:
    _require(isinstance(value, list), f"{name} must be an array")
    return value


def _string(value: Any, name: str) -> str:
    _require(isinstance(value, str) and bool(value.strip()), f"{name} must be nonempty text")
    return value


def _nonnegative_int(value: Any, name: str) -> int:
    _require(type(value) is int and value >= 0, f"{name} must be a nonnegative integer")
    return value


def _boolean(value: Any, name: str) -> bool:
    _require(type(value) is bool, f"{name} must be boolean")
    return value


def _hash(value: Any, name: str) -> str:
    _require(isinstance(value, str) and bool(HEX64.fullmatch(value)), f"{name} must be lowercase SHA-256")
    return value


def _unique(items: list[dict[str, Any]], key: str, name: str) -> None:
    values = [_string(item.get(key), f"{name}.{key}") for item in items]
    _require(len(values) == len(set(values)), f"duplicate {name}.{key}")


def ratio(numerator: int, denominator: int) -> dict[str, Any]:
    _require(0 <= numerator <= denominator, "invalid metric ratio")
    return {
        "numerator": numerator,
        "denominator": denominator,
        "rate": round(numerator / denominator, 6) if denominator else None,
        "status": "MEASURED" if denominator else "NOT_APPLICABLE",
    }


def meets(metric: dict[str, Any], percent: int) -> bool:
    return metric["denominator"] > 0 and metric["numerator"] * 100 >= percent * metric["denominator"]


def validate_manifest(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    _object(manifest, "manifest")
    _require(manifest.get("product_baseline_sha") == BASELINE, "wrong product baseline")
    cases = _list(manifest.get("cases"), "manifest.cases")
    _require(len(cases) >= 6, "corpus needs at least six cases")
    for raw in cases:
        case = _object(raw, "case")
        for key in ("case_id", "title", "publication", "source_page_url", "source_file_url",
                    "technical_domain", "document_format", "access_license_status",
                    "license_evidence_url", "local_acquisition_date", "selection_rationale"):
            _string(case.get(key), f"case.{key}")
        _require(case.get("language") in {"en", "vi"}, "unsupported corpus language")
        _require(case.get("document_format") in {"PDF", "DOCX"}, "unsupported source format")
        _require(case.get("selection_status") in {"CANDIDATE", "HUMAN_ACCEPTED"}, "invalid selection status")
        if case["selection_status"] == "HUMAN_ACCEPTED":
            _string(case.get("accepted_by"), "case.accepted_by")
            _string(case.get("accepted_at"), "case.accepted_at")
        else:
            _require(case.get("accepted_by") is None and case.get("accepted_at") is None, "candidate cannot claim Human acceptance")
        _require(case.get("local_source_path") == f"sources/{case['case_id']}.{case['document_format'].lower()}", "unsafe or inconsistent local source path")
        authors = _list(case.get("authors"), "case.authors")
        _require(bool(authors) and all(isinstance(author, str) and author.strip() for author in authors), "case needs named authors")
        _hash(case.get("source_sha256"), "case.source_sha256")
        _require(0 < _nonnegative_int(case.get("source_size_bytes"), "case.source_size_bytes") <= 10485760, "source exceeds 10 MiB")
        if case["document_format"] == "PDF":
            _require(0 < _nonnegative_int(case.get("page_count"), "case.page_count") <= 50, "PDF page limit exceeded")
        tags = _list(case.get("coverage_tags"), "case.coverage_tags")
        _require(all(isinstance(tag, str) for tag in tags), "coverage tags must be text")
    _unique(cases, "case_id", "case")
    _require(sum(c["language"] == "en" for c in cases) >= 4, "corpus needs four English cases")
    _require(sum(c["language"] == "vi" for c in cases) >= 1, "corpus needs a Vietnamese case")
    _require(len({c["technical_domain"] for c in cases}) >= 2, "corpus needs two domains")
    _require(any({"experimental", "table_heavy"} & set(c["coverage_tags"]) for c in cases), "corpus needs experimental/table-heavy case")
    _require(any({"ambiguous", "incomplete_disclosure"} & set(c["coverage_tags"]) for c in cases), "corpus needs ambiguous/incomplete case")
    return cases


def verify_local_sources(cases: list[dict[str, Any]], package: Path = PACKAGE) -> None:
    """Optional local audit; CI intentionally does not contain copyrighted PDFs."""
    for case in cases:
        path = package / case["local_source_path"]
        _require(path.is_file(), f"missing local source: {case['case_id']}")
        _require(path.stat().st_size == case["source_size_bytes"], f"source size mismatch: {case['case_id']}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        _require(digest == case["source_sha256"], f"source SHA-256 mismatch: {case['case_id']}")


def validate_gold(case: dict[str, Any], gold: dict[str, Any]) -> list[dict[str, Any]]:
    _object(gold, "gold")
    _require(gold.get("case_id") == case["case_id"], "gold case mismatch")
    _require(gold.get("source_sha256") == case["source_sha256"], "gold source mismatch")
    _require(gold.get("review_status") in {"PENDING_HUMAN", "ACCEPTED"}, "invalid gold review status")
    _boolean(gold.get("annotation_inventory_complete"), "annotation_inventory_complete")
    if gold["review_status"] == "ACCEPTED":
        _string(gold.get("reviewed_by"), "gold.reviewed_by")
        _string(gold.get("reviewed_at"), "gold.reviewed_at")
        _require(gold["annotation_inventory_complete"], "accepted gold needs complete annotation inventory")
    else:
        _require(gold.get("reviewed_by") is None and gold.get("reviewed_at") is None, "pending gold cannot claim review")
    items = _list(gold.get("items"), "gold.items")
    for raw in items:
        item = _object(raw, "gold item")
        _string(item.get("gold_id"), "gold_id")
        _require(item.get("category") in GOLD_CATEGORIES, "invalid gold category")
        _string(item.get("normalized_proposition"), "normalized_proposition")
        _require(item.get("importance") in {"KEY", "SECONDARY"}, "invalid gold importance")
        locators = _list(item.get("source_locators"), "source_locators")
        _require(bool(locators) and all(isinstance(locator, str) and locator.strip() for locator in locators), "gold item needs text source locator")
        excerpts = _list(item.get("supporting_excerpts"), "supporting_excerpts")
        _require(all(isinstance(excerpt, str) for excerpt in excerpts), "supporting excerpts must be text")
        _string(item.get("evaluator_note"), "evaluator_note")
        _boolean(item.get("coverage_applicable"), "coverage_applicable")
        _boolean(item.get("missing_information_target"), "missing_information_target")
        if item["missing_information_target"]:
            _require(item["category"] in {"missing_information", "ambiguity_conflict"}, "missing target must be gap category")
    _unique(items, "gold_id", "gold item")
    return items


def validate_metadata(metadata: dict[str, Any], case: dict[str, Any], package: Path = PACKAGE) -> None:
    _object(metadata, "run metadata")
    for key in ("run_id", "prompt_version", "schema_version", "draft_contract_version",
                "model_identifier", "timestamp"):
        _string(metadata.get(key), f"metadata.{key}")
    _require(metadata.get("case_id") == case["case_id"], "run case mismatch")
    _require(metadata.get("source_sha256") == case["source_sha256"], "run source hash mismatch")
    _require(metadata.get("repository_baseline_sha") == BASELINE, "run baseline mismatch")
    _hash(metadata.get("extraction_output_sha256"), "extraction_output_sha256")
    _hash(metadata.get("draft_output_sha256"), "draft_output_sha256")
    _object(metadata.get("reasoning_config"), "reasoning_config")
    _require(metadata.get("run_source") in {"PRODUCT_RUNTIME", "SYNTHETIC_HARNESS", "MANUAL_UI"}, "invalid run source")
    if metadata["run_source"] == "PRODUCT_RUNTIME":
        _string(metadata.get("provider_authorization_reference"), "provider_authorization_reference")
        for kind in ("extraction", "draft"):
            rel = _string(metadata.get(f"{kind}_output_path"), f"{kind}_output_path")
            path = (package / rel).resolve()
            local = (package / "runs" / "local").resolve()
            _require(path.is_relative_to(local) and path.is_file(), "product output must be an existing local-only file")
            _require(hashlib.sha256(path.read_bytes()).hexdigest() == metadata[f"{kind}_output_sha256"], f"{kind} output hash mismatch")


def _validate_assertions(rows: Any, name: str) -> list[dict[str, Any]]:
    assertions = _list(rows, name)
    for raw in assertions:
        item = _object(raw, name + " item")
        _string(item.get("assertion_id"), "assertion_id")
        _require(item.get("support") in SUPPORT_LABELS, "invalid support judgment")
        categories = _list(item.get("critical_categories"), "critical_categories")
        _require(all(isinstance(category, str) for category in categories) and set(categories) <= CRITICAL_CATEGORIES, "invalid critical category")
        if categories:
            _require(item["support"] in {"UNSUPPORTED", "CONTRADICTED"}, "critical categories require unsupported or contradicted judgment")
        if item.get("system_grounding_label") is not None:
            _require(item["system_grounding_label"] in SYSTEM_LABELS, "invalid system grounding label")
            _require(item["support"] != "NOT_APPLICABLE", "non-substantive assertion cannot carry grounding label")
        if item.get("expected_grounding_label") is not None:
            _require(item["expected_grounding_label"] in SYSTEM_LABELS, "invalid expected grounding label")
            _require(item["support"] in EXPECTED_LABEL, "expected grounding label requires supported judgment")
            _require(item["expected_grounding_label"] == EXPECTED_LABEL[item["support"]], "expected grounding label conflicts with semantic support")
        if item["support"] in EXPECTED_LABEL:
            _require((item.get("system_grounding_label") is None) == (item.get("expected_grounding_label") is None), "supported assertion grounding labels must be paired")
        else:
            _require(item.get("expected_grounding_label") is None, "unsupported assertion has no correct grounding label")
        ids = _list(item.get("cited_evidence_ids"), "cited_evidence_ids")
        for evidence_id in ids:
            _string(evidence_id, "cited_evidence_id")
        _boolean(item.get("evidence_ids_exist"), "evidence_ids_exist")
        _boolean(item.get("cited_evidence_supports"), "cited_evidence_supports")
    _unique(assertions, "assertion_id", name)
    return assertions


def validate_judgments(judgments: dict[str, Any], items: list[dict[str, Any]]) -> None:
    _object(judgments, "judgments")
    _require(judgments.get("review_status") in {"PENDING_HUMAN", "ACCEPTED"}, "invalid judgment review status")
    if judgments["review_status"] == "ACCEPTED":
        _string(judgments.get("reviewed_by"), "judgments.reviewed_by")
        _string(judgments.get("reviewed_at"), "judgments.reviewed_at")
    _boolean(judgments.get("assertion_inventory_complete"), "assertion_inventory_complete")
    _validate_assertions(judgments.get("extraction_assertions"), "extraction_assertions")
    _validate_assertions(judgments.get("draft_assertions"), "draft_assertions")
    coverage = _list(judgments.get("gold_coverage"), "gold_coverage")
    for row in coverage:
        _object(row, "gold coverage")
        _string(row.get("gold_id"), "gold_coverage.gold_id")
        _boolean(row.get("covered"), "gold_coverage.covered")
    _unique(coverage, "gold_id", "gold coverage")
    _require({r["gold_id"] for r in coverage} == {i["gold_id"] for i in items if i["coverage_applicable"]}, "gold coverage must enumerate every applicable item exactly once")
    gaps = _list(judgments.get("system_gaps"), "system_gaps")
    gold_gap_ids = {i["gold_id"] for i in items if i["missing_information_target"]}
    for row in gaps:
        _object(row, "system gap")
        _string(row.get("gap_id"), "system gap ID")
        _boolean(row.get("relevant"), "system gap relevance")
        ids = _list(row.get("gold_ids"), "system gap gold IDs")
        _require(all(isinstance(gold_id, str) for gold_id in ids) and set(ids) <= gold_gap_ids, "system gap refers to non-gap gold item")
    _unique(gaps, "gap_id", "system gap")
    questions = _list(judgments.get("author_questions"), "author_questions")
    for row in questions:
        _object(row, "author question")
        _string(row.get("question_id"), "author question ID")
        for key in ("relevant_to_gap", "specific_actionable", "answerable_by_author", "no_unsupported_presupposition"):
            _boolean(row.get(key), f"author question.{key}")
    _unique(questions, "question_id", "author question")
    conflicts = _list(judgments.get("conflict_handling", []), "conflict_handling")
    conflict_ids = {i["gold_id"] for i in items if i["category"] == "ambiguity_conflict"}
    for row in conflicts:
        _object(row, "conflict handling")
        _string(row.get("gold_id"), "conflict handling gold ID")
        _boolean(row.get("handled_accurately"), "conflict handling accuracy")
    _unique(conflicts, "gold_id", "conflict handling")
    _require({r["gold_id"] for r in conflicts} == conflict_ids, "conflict handling must enumerate each ambiguity/conflict gold item")
    for key in ("claims_violations", "legal_conclusion_violations", "abstract_word_count", "schema_business_rule_failures"):
        _nonnegative_int(judgments.get(key), key)


def _assertion_counts(rows: list[dict[str, Any]]) -> dict[str, Any]:
    substantive = [r for r in rows if r["support"] != "NOT_APPLICABLE"]
    supported = sum(r["support"] in SUPPORTED for r in substantive)
    unsupported = [r["assertion_id"] for r in substantive if r["support"] == "UNSUPPORTED"]
    contradicted = [r["assertion_id"] for r in substantive if r["support"] == "CONTRADICTED"]
    critical = [r["assertion_id"] for r in substantive if r["critical_categories"]]
    return {
        "support": ratio(supported, len(substantive)),
        "unsupported_assertion_ids": unsupported,
        "contradicted_assertion_ids": contradicted,
        "critical_assertion_ids": critical,
        "evidence_id_failures": [r["assertion_id"] for r in substantive if not r["evidence_ids_exist"]],
        "evidence_semantic_failures": [r["assertion_id"] for r in substantive if not r["cited_evidence_supports"]],
    }


def score_case(case_id: str, items: list[dict[str, Any]], judgments: dict[str, Any]) -> dict[str, Any]:
    validate_judgments(judgments, items)
    extraction = _assertion_counts(judgments["extraction_assertions"])
    draft = _assertion_counts(judgments["draft_assertions"])
    covered = {r["gold_id"] for r in judgments["gold_coverage"] if r["covered"]}
    key = [i for i in items if i["coverage_applicable"] and i["importance"] == "KEY"]
    secondary = [i for i in items if i["coverage_applicable"] and i["importance"] == "SECONDARY"]
    labels = [r for r in judgments["extraction_assertions"] if r.get("system_grounding_label") is not None]
    gaps = judgments["system_gaps"]
    gold_gaps = {i["gold_id"] for i in items if i["missing_information_target"]}
    surfaced = set().union(*(set(r["gold_ids"]) for r in gaps if r["relevant"])) if gaps else set()
    questions = judgments["author_questions"]
    conflicts = judgments.get("conflict_handling", [])
    useful = sum(all(r[k] for k in ("relevant_to_gap", "specific_actionable", "answerable_by_author", "no_unsupported_presupposition")) for r in questions)
    metrics = {
        "grounding_support_precision": extraction["support"],
        "draft_supported_assertion_rate": draft["support"],
        "key_coverage": ratio(sum(i["gold_id"] in covered for i in key), len(key)),
        "secondary_coverage": ratio(sum(i["gold_id"] in covered for i in secondary), len(secondary)),
        "grounding_label_accuracy": ratio(sum(r["system_grounding_label"] == r["expected_grounding_label"] for r in labels), len(labels)),
        "missing_information_precision": ratio(sum(r["relevant"] for r in gaps), len(gaps)),
        "missing_information_recall": ratio(len(surfaced), len(gold_gaps)),
        "author_question_usefulness": ratio(useful, len(questions)),
        "conflict_handling_accuracy": ratio(sum(r["handled_accurately"] for r in conflicts), len(conflicts)),
    }
    failures = {
        "unsupported_extraction_assertion_ids": extraction["unsupported_assertion_ids"],
        "unsupported_draft_assertion_ids": draft["unsupported_assertion_ids"],
        "contradicted_extraction_assertion_ids": extraction["contradicted_assertion_ids"],
        "contradicted_draft_assertion_ids": draft["contradicted_assertion_ids"],
        "critical_extraction_assertion_ids": extraction["critical_assertion_ids"],
        "critical_draft_assertion_ids": draft["critical_assertion_ids"],
        "evidence_id_failure_ids": extraction["evidence_id_failures"] + draft["evidence_id_failures"],
        "evidence_semantic_failure_ids": extraction["evidence_semantic_failures"] + draft["evidence_semantic_failures"],
        "missed_key_gold_ids": [i["gold_id"] for i in key if i["gold_id"] not in covered],
        "missed_gap_gold_ids": sorted(gold_gaps - surfaced),
    }
    safety = {k: judgments[k] for k in ("claims_violations", "legal_conclusion_violations", "schema_business_rule_failures")}
    safety["abstract_over_150"] = int(judgments["abstract_word_count"] > 150)
    return {"case_id": case_id, "metrics": metrics, "failures": failures, "safety": safety,
            "judgment_review_status": judgments["review_status"],
            "assertion_inventory_complete": judgments["assertion_inventory_complete"]}


def _aggregate(per_case: list[dict[str, Any]]) -> dict[str, Any]:
    if not per_case:
        return {}
    names = list(per_case[0]["metrics"])
    metrics = {}
    for name in names:
        parts = [case["metrics"][name] for case in per_case]
        metrics[name] = ratio(sum(p["numerator"] for p in parts), sum(p["denominator"] for p in parts))
    safety = {name: sum(c["safety"][name] for c in per_case) for name in per_case[0]["safety"]}
    return {"metrics": metrics, "safety": safety,
            "critical_hallucination_count": sum(len(c["failures"][f"critical_{kind}_assertion_ids"]) for c in per_case for kind in ("extraction", "draft")),
            "contradicted_substantive_assertion_count": sum(len(c["failures"][f"contradicted_{kind}_assertion_ids"]) for c in per_case for kind in ("extraction", "draft")),
            "critical_affected_case_ids": [c["case_id"] for c in per_case if c["failures"]["critical_extraction_assertion_ids"] or c["failures"]["critical_draft_assertion_ids"]]}


def threshold_results(per_case: list[dict[str, Any]], aggregate: dict[str, Any]) -> dict[str, str]:
    zero_names = ("critical_hallucinations", "contradictions", "claims", "legal_conclusions",
                  "abstract_length", "schema_business_rules", "falsified_evidence_ids", "zero_tolerance")
    if not per_case:
        return {name: "NOT_EVALUATED" for name in (*THRESHOLDS, *zero_names)}
    a = aggregate["metrics"]
    checks = {
        "grounding_support_aggregate": meets(a["grounding_support_precision"], 98),
        "grounding_support_case": all(meets(c["metrics"]["grounding_support_precision"], 95) for c in per_case),
        "key_coverage_aggregate": meets(a["key_coverage"], 85),
        "key_coverage_case": all(meets(c["metrics"]["key_coverage"], 75) for c in per_case),
        "grounding_label_accuracy": meets(a["grounding_label_accuracy"], 90),
        "missing_precision": meets(a["missing_information_precision"], 80),
        "missing_recall": meets(a["missing_information_recall"], 80),
        "author_question_usefulness": meets(a["author_question_usefulness"], 80),
        "draft_support_aggregate": meets(a["draft_supported_assertion_rate"], 97),
        "draft_support_case": all(meets(c["metrics"]["draft_supported_assertion_rate"], 93) for c in per_case),
        "critical_hallucinations": aggregate["critical_hallucination_count"] == 0,
        "contradictions": aggregate["contradicted_substantive_assertion_count"] == 0,
        "claims": aggregate["safety"]["claims_violations"] == 0,
        "legal_conclusions": aggregate["safety"]["legal_conclusion_violations"] == 0,
        "abstract_length": aggregate["safety"]["abstract_over_150"] == 0,
        "schema_business_rules": aggregate["safety"]["schema_business_rule_failures"] == 0,
        "falsified_evidence_ids": all(not c["failures"]["evidence_id_failure_ids"] for c in per_case),
    }
    checks["zero_tolerance"] = all(checks[name] for name in zero_names if name != "zero_tolerance")
    return {name: "PASS" if value else "FAIL" for name, value in checks.items()}


def evaluate(manifest: dict[str, Any], gold_by_case: dict[str, dict[str, Any]], evidence: dict[str, Any] | None = None,
             package: Path = PACKAGE) -> dict[str, Any]:
    cases = validate_manifest(manifest)
    by_id = {c["case_id"]: c for c in cases}
    _require(set(gold_by_case) == set(by_id), "one gold file required per corpus case")
    gold_items = {case_id: validate_gold(by_id[case_id], gold) for case_id, gold in gold_by_case.items()}
    evidence = evidence if evidence is not None else {"runs": []}
    runs = _list(_object(evidence, "evidence").get("runs"), "evidence.runs")
    product = []
    excluded = []
    for raw in runs:
        run = _object(raw, "run")
        metadata = _object(run.get("metadata"), "metadata")
        case_id = _string(metadata.get("case_id"), "metadata.case_id")
        _require(case_id in by_id, "unknown run case")
        validate_metadata(metadata, by_id[case_id], package)
        judgments = _object(run.get("judgments"), "judgments")
        validate_judgments(judgments, gold_items[case_id])
        if metadata["run_source"] == "PRODUCT_RUNTIME":
            product.append(run)
        else:
            excluded.append({"run_id": metadata["run_id"], "case_id": case_id, "run_source": metadata["run_source"], "reason": "Non-product output excluded from semantic acceptance"})
    _unique([r["metadata"] for r in runs], "run_id", "run")
    _require(len({r["metadata"]["case_id"] for r in product}) == len(product), "repeat product runs need separate Human authorization")
    per_case = [score_case(r["metadata"]["case_id"], gold_items[r["metadata"]["case_id"]], r["judgments"]) for r in product]
    aggregate = _aggregate(per_case)
    thresholds = threshold_results(per_case, aggregate)
    missing = sorted(set(by_id) - {r["metadata"]["case_id"] for r in product})
    pending_corpus = sorted(c["case_id"] for c in cases if c["selection_status"] != "HUMAN_ACCEPTED")
    pending_gold = sorted(cid for cid, g in gold_by_case.items() if g["review_status"] != "ACCEPTED")
    pending_judgments = sorted(r["metadata"]["case_id"] for r in product if r["judgments"]["review_status"] != "ACCEPTED" or not r["judgments"]["assertion_inventory_complete"])
    if not product:
        status = "BLOCKED_FOR_PRODUCT_RUNTIME_EVIDENCE"
    elif missing:
        status = "BLOCKED_FOR_INCOMPLETE_PRODUCT_RUNTIME_CORPUS"
    elif pending_corpus or pending_gold or pending_judgments:
        status = "BLOCKED_FOR_HUMAN_ACCEPTANCE"
    elif any(v == "FAIL" for v in thresholds.values()):
        status = "THRESHOLD_FAILURE_REQUIRES_HUMAN_DECISION"
    else:
        status = "READY_FOR_HUMAN_SEMANTIC_DECISION"
    return {
        "report_version": "1.0.0", "product_baseline_sha": BASELINE,
        "specification_version": manifest.get("specification_version"),
        "status": status, "semantic_acceptance": "NOT_DETERMINED",
        "corpus": {"case_count": len(cases), "human_accepted_count": len(cases) - len(pending_corpus), "pending_case_ids": pending_corpus},
        "gold": {"human_accepted_count": len(cases) - len(pending_gold), "pending_case_ids": pending_gold},
        "runtime_evidence": {"product_run_count": len(product), "missing_case_ids": missing, "excluded_non_product_runs": excluded,
                             "product_runs": [{key: r["metadata"][key] for key in (
                                 "run_id", "case_id", "source_sha256", "repository_baseline_sha", "prompt_version",
                                 "schema_version", "draft_contract_version", "model_identifier", "reasoning_config",
                                 "timestamp", "extraction_output_sha256", "draft_output_sha256", "run_source",
                                 "provider_authorization_reference")} for r in product],
                             "pending_human_judgment_case_ids": pending_judgments},
        "per_case": per_case, "aggregate": aggregate, "threshold_results": thresholds,
        "provider_authorization": "NOT_GRANTED_FOR_THIS_FRAMEWORK_PHASE",
        "provider_budget": 0,
        "blocking_conditions": [x for x, active in (
            ("PRODUCT_RUNTIME_EVIDENCE_ABSENT", not product),
            ("PRODUCT_RUNTIME_CASES_MISSING", bool(missing)),
            ("CORPUS_HUMAN_ACCEPTANCE_PENDING", bool(pending_corpus)),
            ("GOLD_HUMAN_ACCEPTANCE_PENDING", bool(pending_gold)),
            ("JUDGMENT_HUMAN_ACCEPTANCE_PENDING", bool(pending_judgments)),
        ) if active],
    }


def markdown_report(report: dict[str, Any]) -> str:
    lines = ["# EVAL-001 semantic quality report", "", f"Status: **{report['status'].replace('_', ' ')}**", "",
             "Semantic acceptance: **NOT DETERMINED**", "", f"Frozen product baseline: `{report['product_baseline_sha']}`", "",
             f"Corpus candidates: {report['corpus']['case_count']}; Human-accepted: {report['corpus']['human_accepted_count']}",
             f"Human-accepted gold packages: {report['gold']['human_accepted_count']}",
             f"Actual product-runtime runs: {report['runtime_evidence']['product_run_count']}",
             f"Excluded manual/synthetic runs: {len(report['runtime_evidence']['excluded_non_product_runs'])}", "",
             "Provider access: NOT AUTHORIZED; budget: 0; BLK-003: OPEN.", "",
             "## Blocking conditions", ""]
    lines += [f"- {item}" for item in report["blocking_conditions"]] or ["- None recorded; Human semantic decision still required."]
    lines += ["", "## Threshold results", "", "| Gate | State |", "|---|---|"]
    lines += [f"| {name} | {state} |" for name, state in report["threshold_results"].items()]
    lines += ["", "## Per-case evidence", "", "| Case | Extraction support | KEY coverage | Draft support | Critical IDs |", "|---|---:|---:|---:|---|"]
    for case in report["per_case"]:
        m = case["metrics"]
        def display(name: str) -> str:
            value = m[name]["rate"]
            return "N/A" if value is None else f"{value:.1%}"
        critical = case["failures"]["critical_extraction_assertion_ids"] + case["failures"]["critical_draft_assertion_ids"]
        lines.append(f"| {case['case_id']} | {display('grounding_support_precision')} | {display('key_coverage')} | {display('draft_supported_assertion_rate')} | {', '.join(critical) or 'none'} |")
    if not report["per_case"]:
        lines.append("| No authorized product-runtime evidence | N/A | N/A | N/A | N/A |")
    lines += ["", "Deterministic arithmetic uses Human-labelled assertion and gold judgments. No automatic semantic PASS is issued.", ""]
    return "\n".join(lines)


def load_gold(package: Path = PACKAGE) -> dict[str, dict[str, Any]]:
    result = {}
    for path in sorted((package / "gold").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        case_id = _string(data.get("case_id"), "gold.case_id")
        _require(case_id not in result and path.stem == case_id, "gold filename/case mismatch")
        result[case_id] = data
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, help="Local-only run metadata and Human judgments; omit for framework blocked report")
    parser.add_argument("--verify-local-sources", action="store_true")
    parser.add_argument("--json-out", type=Path, default=PACKAGE / "reports" / "framework-status.json")
    parser.add_argument("--markdown-out", type=Path, default=PACKAGE / "reports" / "framework-status.md")
    args = parser.parse_args()
    try:
        manifest = json.loads((PACKAGE / "manifest.json").read_text(encoding="utf-8"))
        cases = validate_manifest(manifest)
        if args.verify_local_sources:
            verify_local_sources(cases)
        evidence = json.loads(args.evidence.read_text(encoding="utf-8")) if args.evidence else None
        report = evaluate(manifest, load_gold(), evidence)
    except (EvaluationInputError, OSError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.markdown_out.write_text(markdown_report(report), encoding="utf-8")
    print(report["status"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
