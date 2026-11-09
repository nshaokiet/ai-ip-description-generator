"""Read-only PREAPI-E inventory check. No product or provider runtime is invoked."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from eval.semantic.v1.tools import evaluator


PACKAGE = Path(__file__).resolve().parents[1]


def inspect_fixture(package: Path = PACKAGE) -> dict[str, Any]:
    """Validate accepted gold inventory and report its exact byte provenance."""
    manifest_path = package / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    cases = evaluator.validate_manifest(manifest)
    gold = evaluator.load_gold(package)
    if set(gold) != {case["case_id"] for case in cases}:
        raise ValueError("gold inventory does not match manifest")

    totals = {"KEY": 0, "SECONDARY": 0}
    files = []
    for case in sorted(cases, key=lambda row: row["case_id"]):
        case_id = case["case_id"]
        data = gold[case_id]
        items = evaluator.validate_gold(case, data)
        path = package / "gold" / f"{case_id}.json"
        counts = {kind: sum(item["importance"] == kind for item in items) for kind in totals}
        for kind in totals:
            totals[kind] += counts[kind]
        files.append({
            "case_id": case_id,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "items": len(items),
            "key": counts["KEY"],
            "secondary": counts["SECONDARY"],
            "review_status": data["review_status"],
        })

    framework = evaluator.evaluate(manifest, gold)
    accepted = all(case["selection_status"] == "HUMAN_ACCEPTED" for case in cases)
    accepted = accepted and all(row["review_status"] == "ACCEPTED" for row in files)
    return {
        "report_version": "0.1.0",
        "task_id": "PREAPI-E",
        "result": "FIXTURE_VALIDATED" if accepted else "FIXTURE_FAILED",
        "manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
        "case_count": len(cases),
        "item_count": sum(totals.values()),
        "importance_counts": totals,
        "gold_files": files,
        "product_runtime": framework["semantic_acceptance"],
        "product_run_count": framework["runtime_evidence"]["product_run_count"],
        "provider_execution": "NOT_RUN",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", type=Path, default=PACKAGE)
    parser.add_argument("--json-out", type=Path, help="Write sanitized report outside accepted gold")
    args = parser.parse_args()
    if args.json_out and (
        args.json_out.resolve() == (args.package / "manifest.json").resolve()
        or (args.package / "gold").resolve() in args.json_out.resolve().parents
    ):
        parser.error("report output cannot replace accepted evaluation input")
    try:
        report = inspect_fixture(args.package)
    except (ValueError, KeyError, TypeError, OSError, json.JSONDecodeError):
        report = {"report_version": "0.1.0", "task_id": "PREAPI-E", "result": "FIXTURE_FAILED",
                  "product_runtime": "NOT_DETERMINED", "provider_execution": "NOT_RUN"}
    output = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.json_out:
        args.json_out.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0 if report["result"] == "FIXTURE_VALIDATED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
