#!/usr/bin/env python3
"""Static validation for GOV-AGENT-001 Phase D P0 skill contracts."""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKILL_ROOT = ROOT / "skills"
MANIFEST = ROOT / "manifest.yaml"
EXPECTED = {
    "shared/project-context","shared/governance","shared/git-safety","shared/testing-policy","shared/ai-ip-domain",
    "planner/task-specification","planner/architecture-analysis",
    "implementer/specification-execution","implementer/safe-code-change",
    "security/threat-modeling","security/ai-security",
    "quality/fixed-sha-review","quality/spec-compliance","quality/patent-conversion-review",
}
REQUIRED_HEADINGS = (
    "## Purpose","## Applies when","## Required inputs","## Allowed actions","## Forbidden actions",
    "## Procedure","## Required checks","## Output contract","## Failure conditions","## Handoff",
)
def major(version: str) -> int:
    match = re.fullmatch(r"(\\d+)\\.(\\d+)\\.(\\d+)", version)
    if not match:
        raise ValueError(f"invalid semantic version: {version}")
    return int(match.group(1))
def resolve(required_major: int, available_version: str | None, governance_conflict: bool = False) -> str:
    if governance_conflict or available_version is None:
        return "BLOCKED"
    return "AVAILABLE" if major(available_version) == required_major else "BLOCKED"
def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)

manifest = MANIFEST.read_text(encoding="utf-8")
for needle in (
    "workflow_v2_activation: NOT_ACTIVATED","missing_required: BLOCKED","incompatible_major: BLOCKED",
    "governance_conflict: BLOCKED","task_spec_may_narrow_only: true","silent_substitution_allowed: false",
):
    if needle not in manifest:
        fail(f"manifest missing {needle}")

found: set[str] = set()
for path in sorted(SKILL_ROOT.glob("*/*/SKILL.md")):
    rel = path.relative_to(SKILL_ROOT)
    skill_id = f"{rel.parts[0]}/{rel.parts[1]}"
    found.add(skill_id)
    body = path.read_text(encoding="utf-8")
    for heading in REQUIRED_HEADINGS:
        if heading not in body:
            fail(f"{skill_id} missing {heading}")
    name_match = re.search(r"^- name: \`([^\`]+)\`$", body, flags=re.MULTILINE)
    version_match = re.search(r"^- version: \`([^\`]+)\`$", body, flags=re.MULTILINE)
    if not name_match or name_match.group(1) != rel.parts[1]:
        fail(f"{skill_id} has invalid name metadata")
    if not version_match or version_match.group(1) != "1.0.0":
        fail(f"{skill_id} must be version 1.0.0")
    if "Governance takes precedence over this skill." not in body:
        fail(f"{skill_id} missing governance precedence")
    if f"path: skills/{skill_id}/SKILL.md" not in manifest or f"id: {skill_id}" not in manifest:
        fail(f"{skill_id} missing manifest reference")
    if f"{skill_id}@^1.0" not in manifest:
        fail(f"{skill_id} is not required by a role")

if found != EXPECTED:
    fail(f"skill inventory mismatch; missing={sorted(EXPECTED-found)} extra={sorted(found-EXPECTED)}")

assert resolve(1, "1.0.0") == "AVAILABLE"
assert resolve(1, None) == "BLOCKED"
assert resolve(1, "2.0.0") == "BLOCKED"
assert resolve(1, "1.9.3", governance_conflict=True) == "BLOCKED"

for role_file in (ROOT / "roles").glob("*.md"):
    body = role_file.read_text(encoding="utf-8")
    if "## Required P0 skills" not in body:
        fail(f"{role_file.name} missing Phase D skill requirements")
    if "missing or incompatible required skill" not in body.lower():
        fail(f"{role_file.name} missing fail-closed resolution rule")

print("PASS: GOV-AGENT-001 Phase D static validation")
print(f"PASS: {len(EXPECTED)} P0 skills; contract headings, role references, and fail-closed fixtures valid")
