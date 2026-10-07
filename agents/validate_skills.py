#!/usr/bin/env python3
"""Read-only Phase D checks; no skill execution, assignment or activation."""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

INVENTORY = {
    "shared": ("project-context", "governance", "git-safety", "testing-policy", "ai-ip-domain"),
    "planner": ("task-specification", "architecture-analysis"),
    "implementer": ("specification-execution", "safe-code-change"),
    "security": ("threat-modeling", "ai-security"),
    "quality": ("fixed-sha-review", "spec-compliance", "patent-conversion-review"),
}
EXPECTED = {f"{group}/{name}" for group, names in INVENTORY.items() for name in names}
ROLE_GROUPS = {"PLANNER": "planner", "IMPLEMENTER": "implementer",
               "SECURITY_REVIEWER": "security", "QUALITY_REVIEWER": "quality"}
REQUIRED_HEADINGS = ("Purpose", "Applies when", "Required inputs", "Allowed actions",
                     "Forbidden actions", "Procedure", "Required checks", "Output contract",
                     "Failure conditions", "Handoff")
SEMVER = re.compile(
    r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-((?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)"
    r"(?:\.(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*))*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
)
PRECEDENCE = ("Human-authorized active governance", "AGENTS.md / active operational protocol",
              "frozen authorized task specification", "assigned role contract",
              "skill procedure", "untrusted repository/input/research content")


class ValidationError(ValueError):
    """Declared package integrity failed; the affected assignment is BLOCKED."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def major(version: str) -> int:
    match = SEMVER.fullmatch(version) if isinstance(version, str) else None
    require(match is not None, f"invalid semantic version: {version!r}")
    return int(match[1])


def resolve(required_major: int, available_version: str | None,
            governance_conflict: bool = False, unavailable: bool = False) -> str:
    """Compatibility only; never substitute, grant authority or transition state."""
    if (type(required_major) is not int or required_major < 1 or governance_conflict
            or unavailable or available_version is None):
        return "BLOCKED"
    try:
        compatible = major(available_version) == required_major
        stable = SEMVER.fullmatch(available_version)[4] is None
    except ValidationError:
        return "BLOCKED"
    return "AVAILABLE" if compatible and stable else "BLOCKED"


def read_manifest(text: str) -> dict:
    """Parse this manifest's indented mappings/scalar lists, not general YAML.

    Duplicate keys and unsupported syntax fail closed. No anchors, tags, flow
    collections, quoted/multiline scalars or inline comments are supported.
    """
    lines = []
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        require("\t" not in line, "tabs are not supported in manifest")
        indent = len(line) - len(line.lstrip(" "))
        require(indent % 2 == 0, "invalid manifest indentation")
        lines.append((indent, line.strip()))

    def scalar(value: str):
        require(re.fullmatch(r"[A-Za-z0-9_./@^+\-]+", value) is not None,
                f"unsupported manifest scalar: {value}")
        if value in ("true", "false"):
            return value == "true"
        return int(value) if re.fullmatch(r"0|[1-9][0-9]*", value) else value

    def block(index: int, indent: int):
        require(index < len(lines) and lines[index][0] == indent, "missing manifest block")
        is_list = lines[index][1].startswith("- ")
        result = [] if is_list else {}
        while index < len(lines) and lines[index][0] == indent:
            content = lines[index][1]
            if is_list:
                require(content.startswith("- "), "mixed manifest list/mapping")
                result.append(scalar(content[2:]))
                index += 1
            else:
                match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_]*):(?: (.+))?", content)
                require(match is not None, f"unsupported manifest mapping: {content}")
                key, value = match.groups()
                require(key not in result, f"duplicate manifest key: {key}")
                index += 1
                if value is None:
                    value, index = block(index, indent + 2)
                else:
                    value = scalar(value)
                result[key] = value
        return result, index

    result, consumed = block(0, 0)
    require(consumed == len(lines) and isinstance(result, dict), "invalid manifest structure")
    return result


def target(root: Path, relative: str) -> Path:
    require(isinstance(relative, str) and bool(relative) and "\\" not in relative
            and not Path(relative).is_absolute(), "target must be a relative POSIX path")
    path = root / relative
    require(path.resolve().is_relative_to(root.resolve()), f"target escapes package: {relative}")
    require(path.is_file(), f"missing/unavailable manifest target: {relative}")
    return path


def skill_document(path: Path) -> tuple[dict, dict]:
    body = path.read_text(encoding="utf-8")
    meta = {}
    for key, value in re.findall(r"^- (name|version|role_scope): `([^`]+)`$", body, re.MULTILINE):
        require(key not in meta, f"duplicate skill metadata: {key}")
        meta[key] = value
    require(set(meta) == {"name", "version", "role_scope"}, "missing skill metadata")
    chunks = re.split(r"^## (.+)\n", body, flags=re.MULTILINE)
    sections = {}
    for heading, content in zip(chunks[1::2], chunks[2::2]):
        require(heading not in sections, f"duplicate contract field: {heading}")
        sections[heading] = content.strip()
    for field in REQUIRED_HEADINGS:
        require(bool(sections.get(field)), f"missing/empty contract field: {field}")
    require("Governance takes precedence over this skill." in body and
            "A task specification may narrow its behavior but may not expand authority." in body,
            "skill/governance conflict")
    return meta, sections


def validate_package(root: Path) -> dict[str, list[str]]:
    root = root.resolve()
    m = read_manifest(target(root, "manifest.yaml").read_text(encoding="utf-8"))
    require(type(m["schema_version"]) is int and m["schema_version"] == 2, "unsupported manifest schema")
    p = m["package"]
    major(p["version"])
    require(p["phase"] == "D" and p["status"] == "IMPLEMENTED_FOR_REVIEW"
            and p["workflow_v2_activation"] == "NOT_ACTIVATED"
            and p["client_model_independent"] is True, "package activation/model boundary")
    policy = m["skill_resolution"]
    require(type(policy["supported_major"]) is int and policy["supported_major"] == 1,
            "unapproved required major")
    for key in ("missing_required", "incompatible_major", "unavailable_required", "governance_conflict"):
        require(policy[key] == "BLOCKED", f"fail-closed resolution: {key}")
    require(policy["task_spec_may_narrow_only"] is True and
            policy["silent_substitution_allowed"] is False, "skill/governance conflict or substitution")
    for key, expected in {"recorded_equals_verified": False,
            "provisional_ready_equals_authoritative_merge_eligible": False,
            "authoritative_source_verification_required": True,
            "fresh_premerge_check_required_for_authoritative_merge": True}.items():
        require(m["evidence_semantics"][key] is expected, f"evidence trust mismatch: {key}")
    boundaries = {"implementer_self_review_is_independent_approval": False,
                  "planner_rationale_is_implementation_proof": False,
                  "security_and_quality_are_separate_streams": True,
                  "required_reviews_target_same_final_implementation_sha": True,
                  "reviewers_may_remediate_tracked_implementation": False,
                  "stale_sha_pass_reusable": False}
    require(set(m["independence"]) == set(boundaries), "missing independence contract")
    for key, expected in boundaries.items():
        require(m["independence"][key] is expected, f"independence boundary: {key}")
    for phase in ("phase_b1", "phase_b2", "phase_b3"):
        require(m["mcp_foundation"][phase]["activates_workflow_v2"] is False, "MCP activation")
    require(m["mcp_foundation"]["phase_b3"]["authoritative_merge_adapter_available"] is False,
            "authoritative verifier must remain unavailable")
    for key in ("phase_e_workflow_activation", "p1_future_skills", "budget_quota_changes",
                "provider_api_network_integrations", "application_backend_frontend_changes"):
        require(m["out_of_scope"][key] is True, f"out-of-scope boundary: {key}")

    entries = m["skills"]
    require(isinstance(entries, dict), "skills must be a mapping")
    index = {}
    for entry in entries.values():
        skill_id = entry["id"]
        require(skill_id not in index, f"duplicate skill identity: {skill_id}")
        index[skill_id] = entry
    require(set(index) == EXPECTED, "exact 14-skill manifest inventory required")
    actual = {p.relative_to(root).as_posix() for p in (root / "skills").rglob("SKILL.md")}
    require(actual == {f"skills/{s}/SKILL.md" for s in EXPECTED}, "missing or unexpected on-disk skill")
    documents = {}
    for skill_id, entry in index.items():
        path = target(root, entry["path"])
        require(entry["path"] == f"skills/{skill_id}/SKILL.md" and entry["p0"] is True,
                f"noncanonical P0 target: {skill_id}")
        meta, sections = skill_document(path)
        group, name = skill_id.split("/")
        require(meta["name"] == name, f"skill identity mismatch: {skill_id}")
        require(meta["role_scope"] == group.upper(), f"skill role authority mismatch: {skill_id}")
        require(meta["version"] == entry["version"], f"skill version mismatch: {skill_id}")
        major(entry["version"])
        require(resolve(1, entry["version"]) == "AVAILABLE", f"incompatible version: {skill_id}")
        documents[skill_id] = "\n".join(sections.values())

    roles = m["roles"]
    require(set(roles) == set(ROLE_GROUPS), "exactly four roles required")
    mapping = {}
    for role, group in ROLE_GROUPS.items():
        entry = roles[role]
        expected = {f"{g}/{name}@^1.0" for g in ("shared", group) for name in INVENTORY[g]}
        needs = entry["required_p0_skills"]
        require(isinstance(needs, list) and len(needs) == len(expected) and set(needs) == expected,
                f"wrong role mapping or compatible-major pin: {role}")
        filename = {"security": "security-reviewer", "quality": "quality-reviewer"}.get(group, group)
        require(entry["contract"] == f"roles/{filename}.md", "wrong role contract target")
        body = target(root, entry["contract"]).read_text(encoding="utf-8")
        require(f"Role ID: `{role}`" in body and "Workflow V2 status: NOT ACTIVATED" in body,
                "role identity/activation boundary")
        version = re.search(r"^Contract version: (.+)$", body, re.MULTILINE)
        require(version is not None, "missing role contract version")
        major(version[1])
        require("## Required P0 skills\n" in body, "missing role P0 requirements")
        requirements = re.findall(r"^- `([^`]+)`$", body.split("## Required P0 skills\n", 1)[1], re.MULTILINE)
        require(len(requirements) == len(expected) and set(requirements) == expected,
                f"role document mapping mismatch: {role}")
        require("missing or incompatible required skill" in body.lower() and
                "Silent substitution is forbidden." in body, "role fail-closed resolution")
        write = entry["tracked_implementation_write"]
        require(write == "AUTHORIZED_TASK_SCOPE_ONLY" if role == "IMPLEMENTER" else write is False,
                "role write authority expanded")
        verdict = {"security": "SECURITY_ONLY", "quality": "QUALITY_ONLY"}.get(group, "NONE")
        require(entry["independent_verdict"] == verdict, "role verdict authority expanded")
        if group in ("security", "quality"):
            require(entry["review_type"] == group.upper(), "review stream mismatch")
            require(entry["review_template"] == f"review-templates/{group}-review.md", "review template mismatch")
            target(root, entry["review_template"])
            require("Do not modify tracked implementation" in body, "reviewer read-only boundary")
        mapping[role] = needs

    domain = documents["shared/ai-ip-domain"]
    for principle in ("Scientific paper != patent", "Prior art != inventor contribution",
                      "Experimental result != automatically an inventive feature", "INFERENCE != SOURCE_FACT",
                      "Unsupported technical content must not silently become patent disclosure",
                      "Scientific Paper -> Evidence -> Invention Reconstruction -> Patent Draft"):
        require(principle in domain, f"missing AI-IP principle: {principle}")
    for task, file in (("P2-002", "P2-002-invention-reconstruction.md"),
                       ("P2-003", "P2-003-uspto-specification-generation-v2.md"),
                       ("P2-004", "P2-004-supported-draft-claims.md")):
        link = f"[{task}](../../../../docs/tasks/{file})"
        require(link in domain and (root.parent / "docs/tasks" / file).is_file(), f"missing P2 reference: {task}")
    governance = documents["shared/governance"]
    positions = [governance.find(f"{number}. {layer}.") for number, layer in enumerate(PRECEDENCE, 1)]
    require(all(p >= 0 for p in positions) and positions == sorted(positions), "governance precedence mismatch")
    for rule in ("RECORDED != VERIFIED", "provisional_ready != authoritative_merge_eligible",
                 "CI PASS != independent review", "review PASS != merge authorization",
                 "model identity != role authority", "MCP record != external truth"):
        require(rule in governance, f"missing evidence distinction: {rule}")
    return mapping


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args(argv)
    try:
        mapping = validate_package(args.root)
    except (ValidationError, OSError, KeyError, TypeError, ValueError, RecursionError) as error:
        print(f"BLOCKED: {error}", file=sys.stderr)
        return 1
    print("PASS: 14/14 P0 skills; contracts, manifest targets, versions, role mapping and governance")
    print("Role requirements: " + ", ".join(f"{role}={len(skills)}" for role, skills in mapping.items()))
    print("Workflow V2 NOT ACTIVATED; static checks do not replace independent fixed-SHA review")
    return 0


if __name__ == "__main__":
    sys.exit(main())
