#!/usr/bin/env python3
"""Prune superseded SUCCESS-only GitHub Actions QA artifacts; safe dry-run by default.

Requires an authenticated GitHub CLI (`gh auth status`). No tokens are read or printed
by this script. Deletes artifacts only, not CI workflow runs, logs, caches or releases.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import json
import shutil
import subprocess
import sys

REPOSITORY = "nshaokiet/ai-ip-description-generator"
QA_ARTIFACT_NAMES = frozenset({
    "p2-006-public-reference-calibration",
    "p2-006-synthetic-layout-qa",
    "uiux-003-synthetic-browser-qa",
    "dep-001-uiux003-compatibility",
})
# Keep the small "dep-001-security" artifact and all non-QA/unknown artifacts.


def gh_api(path: str, *, delete: bool = False) -> dict:
    cmd = ["gh", "api", "--hostname", "github.com"]
    if delete:
        cmd += ["--method", "DELETE"]
    cmd.append(f"repos/{REPOSITORY}/{path}")
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode:
        # GitHub CLI diagnostics may include the endpoint; never show credentials.
        raise RuntimeError(f"GitHub API request failed: {path} (exit {result.returncode})")
    if delete:
        return {}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Unexpected JSON for {path}") from exc


def get_all(endpoint: str, key: str, *, max_pages: int = 20) -> list[dict]:
    items: list[dict] = []
    for page in range(1, max_pages + 1):
        data = gh_api(f"{endpoint}?per_page=100&page={page}")
        if not isinstance(data, dict) or not isinstance(data.get(key), list):
            raise RuntimeError(f"Unexpected list response for {endpoint}")
        rows = data[key]
        items.extend(rows)
        if len(rows) < 100:
            return items
    raise RuntimeError(f"{endpoint} exceeded {max_pages} pages: refusing partial inventory")


def utc_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true",
                        help="Actually delete selected artifacts (default: dry-run only).")
    parser.add_argument("--min-age-hours", type=int, default=24,
                        help="Do not remove artifacts newer than this many hours (default: 24).")
    parser.add_argument("--keep-main-runs", type=int, default=2,
                        help="Protect latest successful main runs (default: 2).")
    parser.add_argument("--keep-pr-runs", type=int, default=1,
                        help="Protect latest successful PR runs (default: 1).")
    parser.add_argument("--keep-run", type=int, action="append", default=[],
                        help="Explicitly protect a workflow run ID; repeat as needed.")
    parser.add_argument("--max-delete", type=int, default=100,
                        help="Hard cap on artifact deletions per invocation (default: 100).")
    args = parser.parse_args()

    if not shutil.which("gh"):
        parser.error("GitHub CLI 'gh' is required. Install and authenticate it first.")
    if args.min_age_hours < 1 or args.keep_main_runs < 1 or args.keep_pr_runs < 1 or args.max_delete < 1:
        parser.error("All numeric limits must be positive.")

    runs = get_all("actions/runs", "workflow_runs")
    artifacts = get_all("actions/artifacts", "artifacts")
    run_by_id = {int(run["id"]): run for run in runs}
    successes = sorted(
        (r for r in runs if r.get("conclusion") == "success"),
        key=lambda r: r.get("created_at", ""), reverse=True,
    )
    protected = set(args.keep_run)
    protected.update(int(r["id"]) for r in
                     (r for r in successes if r.get("head_branch") == "main")[:args.keep_main_runs])
    protected.update(int(r["id"]) for r in
                     (r for r in successes if r.get("event") == "pull_request")[:args.keep_pr_runs])
    threshold = datetime.now(timezone.utc) - timedelta(hours=args.min_age_hours)

    candidates = []
    for artifact in artifacts:
        if artifact.get("expired") or artifact.get("name") not in QA_ARTIFACT_NAMES:
            continue
        run_id = int((artifact.get("workflow_run") or {}).get("id") or 0)
        run = run_by_id.get(run_id)
        if not run or run.get("conclusion") != "success" or run_id in protected:
            continue
        if utc_time(artifact["created_at"]) >= threshold:
            continue
        candidates.append(artifact)

    candidates.sort(key=lambda a: (a["created_at"], a["id"]))
    selected = candidates[:args.max_delete]
    total = sum(int(a["size_in_bytes"]) for a in selected)
    print(f"Repository: {REPOSITORY}")
    print(f"Protected run IDs: {sorted(protected)}")
    print(f"Inventory: {len(runs)} workflow runs, {len(artifacts)} artifacts")
    print(f"QA candidates: {len(candidates)}; selected: {len(selected)}")
    print(f"Selected artifact bytes: {total:,} ({total/1_000_000:.1f} MB)")
    print(f"Mode: {'APPLY (DELETE)' if args.apply else 'DRY-RUN (NO DELETION)'}")
    for a in selected:
        rid = int((a.get("workflow_run") or {})["id"])
        print(f"  {a['id']}  run={rid}  {a['name']}  {a['size_in_bytes']/1_000_000:.1f} MB")
    if not args.apply:
        print("Nothing deleted. Review candidates, then rerun with --apply.")
        return 0

    deleted = 0
    for a in selected:
        try:
            gh_api(f"actions/artifacts/{int(a['id'])}", delete=True)
            deleted += 1
        except RuntimeError as exc:
            print(f"STOP after {deleted} deletions: {exc}", file=sys.stderr)
            return 1
    print(f"Deleted {deleted} artifact(s), nominally {total/1_000_000:.1f} MB.")
    print("GitHub billing/storage dashboards may lag; caches and workflow logs were untouched.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
