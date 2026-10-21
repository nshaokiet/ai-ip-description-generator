"""Regression guards for CI-V2-001; no provider, network or new test dependency.

These deliberately inspect the workflow's step-level text contract. Full YAML
and Actions expression validation is performed separately with actionlint.
"""
from __future__ import annotations

import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import textwrap

import pytest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
BUILD = WORKFLOW.split("  build-and-test:\n", 1)[1]
STEPS = re.findall(r"^      - .+?(?=^      - |\Z)", BUILD, re.M | re.S)
UPLOADS = [step for step in STEPS if "uses: actions/upload-artifact@" in step]
SNAPSHOT = next(step for step in STEPS if "id: functional_test_status\n" in step)


def named_step(name: str) -> str:
    matches = [step for step in STEPS if step.startswith(f"      - name: {name}\n")]
    assert len(matches) == 1, f"required step missing or duplicated: {name}"
    return matches[0]


def test_uploads_cannot_interrupt_any_functional_step() -> None:
    assert len(UPLOADS) == 5
    first_upload = STEPS.index(UPLOADS[0])
    assert STEPS[first_upload:] == UPLOADS, "all archives must be at the job tail"
    assert STEPS[first_upload - 1] == SNAPSHOT
    assert STEPS[first_upload - 2] == named_step("Run Render synthetic demo browser E2E")


@pytest.mark.parametrize("name, command", [
    ("Run offline backend regression", "python -m pytest tests -q -p no:cacheprovider"),
    ("Validate synthetic editable DOCX layout using headless LibreOffice", "qa_p2_006_libreoffice.py"),
    ("Reproduce both public patent reference measurements", "--verify docs/tasks/P2-006-reference-measurements.json"),
    ("Lint frontend", "npm run lint"),
    ("Verify DEP-001 full and production security graphs", "npm run test:lint-security"),
    ("Typecheck frontend", "npm run typecheck"),
    ("Build frontend", "npm run build"),
    ("Run synthetic browser E2E", "npm run test:e2e"),
    ("Verify isolated fixed UIUX-003 compatibility without changing PR 104", "npx playwright test e2e/integration.spec.ts e2e/uiux-003.spec.ts"),
    ("Build Render static demo export", "npm run build"),
    ("Verify static demo output contains no provider secret markers", "! grep -R -E"),
    ("Run Render synthetic demo browser E2E", "npm run test:e2e:demo"),
])
def test_required_functional_gates_are_unconditional_and_before_uploads(name, command) -> None:
    step = named_step(name)
    assert command in step
    assert STEPS.index(step) < STEPS.index(SNAPSHOT)
    assert not re.search(r"^        if:", step, re.M)


def test_security_evidence_stays_required_even_after_test_or_upload_failure() -> None:
    security = named_step("Archive DEP-001 security evidence")
    assert UPLOADS[0] == security
    assert "        if: always()\n" in security
    assert "          if-no-files-found: error\n" in security
    assert "          path: ${{ runner.temp }}/dep-001-security/\n" in security
    producer = named_step("Verify DEP-001 full and production security graphs")
    for command in ("npm audit --json", "npm audit --omit=dev --json", "npm ls --all --json"):
        assert command in producer


@pytest.mark.parametrize("upload_index", range(1, 5))
def test_optional_archives_use_only_preupload_failure_or_explicit_request(upload_index) -> None:
    # In particular, failure() here would turn a storage failure into more uploads.
    step = UPLOADS[upload_index]
    assert "if: ${{ always() && (steps.functional_test_status.outputs.failed == 'true' || inputs.upload_qa_artifacts) }}" in step
    assert "failure()" not in step
    assert "job.status" not in step


@pytest.mark.parametrize("status, expected", [
    ("success", "false"), ("failure", "true"), ("cancelled", "false"),
])
def test_real_snapshot_shell_records_status_before_artifact_failures(tmp_path, status, expected) -> None:
    bash = shutil.which("bash")
    if sys.platform == "win32":
        git = shutil.which("git")
        git_bash = Path(git).parent.parent / "bin/bash.exe" if git else None
        bash = str(git_bash) if git_bash and git_bash.is_file() else None
    if not bash:
        pytest.skip("Bash is required to execute the workflow snapshot")
    assert "        if: always()\n" in SNAPSHOT
    assert "        shell: bash\n" in SNAPSHOT
    script = textwrap.dedent(SNAPSHOT.split("        run: |\n", 1)[1])
    script = script.replace("${{ job.status }}", status)
    output = tmp_path / "output"
    env = {**os.environ, "GITHUB_OUTPUT": output.as_posix()}
    subprocess.run([bash, "--noprofile", "--norc", "-e", "-o", "pipefail", "-c", script],
                   check=True, env=env, capture_output=True, text=True, timeout=15)
    assert output.read_text(encoding="utf-8") == f"failed={expected}\n"


def test_failure_suppression_is_forbidden_and_retention_stays_bounded() -> None:
    assert "continue-on-error" not in WORKFLOW
    assert not re.search(r"\|\|\s*(?:true|:)(?:\s|$)", WORKFLOW)
    for step in UPLOADS:
        assert "          retention-days: 2\n" in step


def test_provider_flags_exact_head_and_required_status_contracts_are_preserved() -> None:
    assert re.findall(r"^  ([\w-]+):\n    runs-on:", WORKFLOW, re.M) == ["mcp-tests", "build-and-test"]
    for flag in ("RUN_OPENAI_LIVE_TESTS", "RUN_OPENAI_DRAFT_LIVE_TESTS"):
        assert f'      {flag}: "0"\n' in WORKFLOW
    assert "permissions:\n  contents: read\n" in WORKFLOW
    assert "secrets." not in WORKFLOW
    assert WORKFLOW.count("ref: ${{ github.event.pull_request.head.sha || github.sha }}") == 2
    assert "test \"$(git rev-parse HEAD)\" = \"$MCP_EXPECTED_SHA\"" in WORKFLOW
    mcp = WORKFLOW.split("  build-and-test:\n", 1)[0]
    for command in ("npm ci", "npm run typecheck", "npm run build", "npm test"):
        assert command in mcp
    assert "  pull_request:\n    branches:\n      - main\n" in WORKFLOW
    assert "  push:\n    branches:\n      - main\n" in WORKFLOW
    assert "paths:" not in WORKFLOW and "paths-ignore:" not in WORKFLOW
    assert "        type: boolean\n        default: false\n" in WORKFLOW
