"""Contract tests for the dry-run-first, allowlisted Actions QA artifact pruner."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "maintenance" / "prune_actions_qa_artifacts.py"
spec = importlib.util.spec_from_file_location("prune_actions_qa_artifacts", SCRIPT)
assert spec is not None and spec.loader is not None
prune = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prune)


def _run(run_id: int, *, branch: str, event: str = "pull_request", conclusion: str = "success") -> dict:
    return {
        "id": run_id, "head_branch": branch, "event": event,
        "conclusion": conclusion, "created_at": f"2020-01-{min(run_id, 28):02d}T00:00:00Z",
    }


def _artifact(artifact_id: int, run_id: int, name: str, *, expired: bool = False) -> dict:
    return {
        "id": artifact_id, "name": name, "size_in_bytes": 1_000_000,
        "created_at": "2020-01-01T00:00:00Z", "expired": expired,
        "workflow_run": {"id": run_id},
    }


def _fixtures() -> tuple[list[dict], list[dict]]:
    runs = [
        _run(13, branch="main", event="push"),
        _run(12, branch="main", event="push"),
        _run(11, branch="main", event="push"),
        _run(20, branch="review-new"),
        _run(10, branch="review-old"),
        _run(9, branch="failed", conclusion="failure"),
    ]
    artifacts = [
        _artifact(101, 13, "uiux-003-synthetic-browser-qa"),  # protected newest main
        _artifact(102, 12, "uiux-003-synthetic-browser-qa"),  # protected second main
        _artifact(103, 20, "uiux-003-synthetic-browser-qa"),  # protected latest PR
        _artifact(104, 9, "uiux-003-synthetic-browser-qa"),   # failed run preserved
        _artifact(105, 11, "dep-001-security"),               # unknown-name/small evidence
        _artifact(106, 10, "p2-006-synthetic-layout-qa", expired=True),
        _artifact(107, 10, "p2-006-public-reference-calibration"),  # deletable
        _artifact(108, 11, "uiux-003-synthetic-browser-qa"),  # deletable
        _artifact(109, 10, "unexpected-artifact"),           # not allowlisted
    ]
    return runs, artifacts


def test_dry_run_preserves_protected_runs_and_does_not_delete(capsys) -> None:
    runs, artifacts = _fixtures()
    with patch.object(prune, "get_all", side_effect=[runs, artifacts]), \
         patch.object(prune.shutil, "which", return_value="/usr/bin/gh"), \
         patch.object(prune, "gh_api") as delete, \
         patch.object(sys, "argv", [str(SCRIPT)]):
        assert prune.main() == 0
    delete.assert_not_called()
    output = capsys.readouterr().out
    assert "selected: 2" in output
    assert "DRY-RUN" in output
    assert "107" in output and "108" in output


def test_apply_deletes_only_explicitly_allowlisted_old_success_artifacts(capsys) -> None:
    runs, artifacts = _fixtures()
    deleted = []
    def fake_delete(path: str, *, delete: bool = False) -> dict:
        assert delete
        deleted.append(path)
        return {}
    with patch.object(prune, "get_all", side_effect=[runs, artifacts]), \
         patch.object(prune.shutil, "which", return_value="/usr/bin/gh"), \
         patch.object(prune, "gh_api", side_effect=fake_delete), \
         patch.object(sys, "argv", [str(SCRIPT), "--apply"]):
        assert prune.main() == 0
    assert deleted == ["actions/artifacts/107", "actions/artifacts/108"]
    assert "Deleted 2 artifact(s)" in capsys.readouterr().out
