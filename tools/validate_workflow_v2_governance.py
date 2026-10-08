"""Read-only Phase E/G governance checks, not activation or a source verifier."""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

MARKER = "docs/operations/WORKFLOW_V2_ACTIVATION.yaml"
EXPECTED = {
    "schema_version": 1, "version": "1.0.0", "workflow": "V2", "enabled": True,
    "activation": {"phase": "GOV-AGENT-001-E",
        "activation_commit_semantics": "PHASE_E_REVIEWED_PR_MERGE_COMMIT",
        "explicit_human_approval_required": True, "accepted_merge_on_main_required": True,
        "independent_governance_review_required": True, "required_ci_success": True,
        "postmerge_verification_required": True, "implementation_sha_is_activation_commit": False},
    "enrollment": {"mode": "EXPLICIT_ONLY", "human_task_authorization_required": True,
        "historical_v1_backfill": False, "unenrolled_tasks_use": "V1",
        "activation_commit_reference_required": True, "required_role_spec_evidence_state_required": True},
    "identity": {"mode": "PROCEDURAL_TRUST_BASED", "cryptographically_authenticated": False},
    "merge_verification": {"mode": "MANUAL_EXTERNAL", "mcp_authoritative_merge_eligible_required": False,
        "mcp_provisional_ready_is_merge_permission": False, "authoritative_verifier_adapter_available": False,
        "fresh_external_premerge_check_required": True},
    "risk_routing": {"automatic_r0_r4": False, "pilot_security_review_required": True,
        "pilot_quality_review_required": True, "other_tasks_explicit_review_policy_required": True},
    "rollback": {"separately_reviewed_disable_required": True, "preserve_v2_evidence": True,
        "silent_v2_to_v1_translation": False, "disable_stops_new_enrollment": True,
        "active_v2_task_human_disposition_required": True},
}


class ValidationError(ValueError):
    """Policy declaration invalid; structural validation is BLOCKED."""


def require(condition: bool, message: str):
    if not condition:
        raise ValidationError(message)


def read_marker(text: str) -> dict:
    """Only this marker's indented scalar mappings; unsupported YAML fails closed."""
    root = {}
    stack = [(-2, root)]
    previous_indent = -2
    previous_child = root
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        require("\t" not in raw, "tabs unsupported in marker")
        indent = len(raw) - len(raw.lstrip(" "))
        require(indent % 2 == 0, "invalid marker indentation")
        if indent > previous_indent:
            require(indent == previous_indent + 2 and previous_child is not None,
                    "unsupported marker nesting")
            stack.append((indent, previous_child))
        else:
            while stack and stack[-1][0] > indent:
                stack.pop()
            require(stack and stack[-1][0] == indent, "invalid marker nesting")
        match = re.fullmatch(r"([a-z_][a-z0-9_]*):(?: ([A-Za-z0-9_.-]+))?", raw.strip())
        require(match is not None, "unsupported YAML syntax in marker")
        key, value = match.groups()
        parent = stack[-1][1]
        require(key not in parent, f"duplicate marker key: {key}")
        previous_child = {} if value is None else None
        if value is None:
            parent[key] = previous_child
        elif value in ("true", "false"):
            parent[key] = value == "true"
        elif re.fullmatch(r"0|[1-9][0-9]*", value):
            parent[key] = int(value)
        else:
            parent[key] = value
        previous_indent = indent
    require(bool(root), "empty marker")
    return root


def validate_policy(policy: dict):
    def check(observed, expected, path):
        require(type(observed) is type(expected), f"wrong type: {path}")
        if isinstance(expected, dict):
            require(set(observed) == set(expected), f"missing/unexpected field: {path}")
            for key, value in expected.items():
                if path == "policy" and key == "enabled":
                    require(type(observed[key]) is bool, "enabled must be boolean")
                else:
                    check(observed[key], value, path + "." + key)
        else:
            require(observed == expected, f"governance boundary changed: {path}")
    check(policy, EXPECTED, "policy")


def sha(value, length=40):
    return isinstance(value, str) and re.fullmatch(r"[a-f0-9]{" + str(length) + r"}", value) is not None


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def effective_activation(policy: dict, observed: dict) -> bool:
    """Pure supplied-evidence model only; cannot authenticate/observe Git or approval."""
    validate_policy(policy)
    required = ("source_verified", "phase_e_pr_merged", "human_activation_approved",
                "governance_review_pass", "required_ci_success", "merge_eligible",
                "reviewed_sha_contained_in_merge", "activation_merge_in_main_ancestry",
                "postmerge_verified", "postmerge_ci_success")
    return (policy["enabled"] is True and observed.get("source_branch") == "main"
            and all(observed.get(key) is True for key in required)
            and sha(observed.get("activation_merge_sha")) and sha(observed.get("reviewed_head_sha"))
            and observed["activation_merge_sha"] != observed["reviewed_head_sha"]
            and observed.get("review_sha") == observed["reviewed_head_sha"]
            and observed.get("ci_sha") == observed["reviewed_head_sha"]
            and observed.get("main_ci_sha") == observed["activation_merge_sha"])


def enrollment_preflight(policy: dict, observed: dict, task: dict) -> bool:
    """Model new admission, without writing an enrollment or changing task state."""
    return (effective_activation(policy, observed)
            and task.get("human_authorized") is True and nonempty(task.get("authorization_ref"))
            and nonempty(task.get("task_id")) and task.get("explicit_enrollment_requested") is True
            and task.get("historical_v1") is False and task.get("has_execution_history") is False
            and task.get("has_v2_history") is False
            and task.get("activation_commit") == observed["activation_merge_sha"])


def workflow_selection(policy: dict, observed: dict, task: dict) -> str:
    """Model eligible workflow, not execution permission; no silent V2-history fallback."""
    active = effective_activation(policy, observed)
    eligible = (active and task.get("human_authorized") is True
                and nonempty(task.get("authorization_ref")) and nonempty(task.get("task_id"))
                and task.get("enrolled") is True and task.get("historical_v1") is False
                and task.get("activation_commit") == observed["activation_merge_sha"]
                and task.get("required_state_exists") is True)
    if task.get("has_v2_history") is True and not eligible:
        return "BLOCKED_HUMAN_DISPOSITION"
    return "V2" if eligible else "V1"


def manual_packet_blockers(packet: dict) -> list[str]:
    """Structural checklist completeness only, NEVER authoritative merge permission."""
    blockers = []
    def gate(ok, reason):
        if not ok:
            blockers.append(reason)
    for key in ("human_scope_authorized", "human_exceptions_resolved", "frozen_spec_committed",
                "human_freeze_authorized", "implementation_base_branch_verified", "ci_success",
                "fresh_pr_check", "pr_open", "pr_mergeable", "scope_safe",
                "no_secret_confidential_exposure", "no_stop_condition", "platform_controls_satisfied"):
        gate(packet.get(key) is True, key)
    for key in ("human_authorization_ref", "spec_artifact_ref", "human_freeze_ref",
                "git_ref", "ci_ref", "fresh_pr_ref", "repository", "branch", "pr_number"):
        gate(nonempty(packet.get(key)), key)
    final = packet.get("final_sha")
    spec = packet.get("spec_sha")
    base = packet.get("base_sha")
    gate(sha(final) and sha(spec) and sha(base), "exact_git_identities")
    gate(isinstance(packet.get("spec_version"), str)
         and re.fullmatch(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)",
                          packet["spec_version"]) is not None, "spec_version")
    gate(packet.get("ci_sha") == final and sha(final), "exact_head_ci")
    gate(packet.get("pr_head_sha") == final and sha(final), "fresh_exact_pr_head")
    gate(packet.get("mcp_provisional_used_as_permission") is False, "provisional_not_permission")
    gate(packet.get("mcp_authoritative_merge_eligible") is False, "unchanged_b3_authority")
    gate(nonempty(packet.get("implementer_id")), "implementer_identity")
    gate(nonempty(packet.get("implementer_session_id")), "implementer_session")
    requirements = packet.get("required_reviews")
    known = isinstance(requirements, dict) and set(requirements) == {"SECURITY", "QUALITY"}
    gate(known, "explicit_review_policy")
    if not known:
        return blockers
    gate(type(packet.get("pilot")) is bool, "explicit_pilot_context")
    if packet.get("pilot") is True:
        gate(requirements["SECURITY"] is True and requirements["QUALITY"] is True, "pilot_dual_review")
    valid = []
    reviews = packet.get("reviews", {})
    if not isinstance(reviews, dict):
        blockers.append("review_artifacts")
        return blockers
    gate(set(reviews) <= {"SECURITY", "QUALITY"}, "known_review_streams")
    for stream in ("SECURITY", "QUALITY"):
        gate(type(requirements[stream]) is bool, "explicit_" + stream + "_requirement")
        review = reviews.get(stream)
        if requirements[stream] is not True:
            gate(review is None or isinstance(review, dict), "optional_review_artifact")
            if isinstance(review, dict):
                gate(review.get("blocking_findings") == [], "optional_review_blocker")
                gate(review.get("verdict") == "PASS", "optional_review_not_pass")
            continue
        if not isinstance(review, dict):
            blockers.append(stream + "_missing")
            continue
        gate(review.get("stream") == stream, stream + "_stream")
        gate(review.get("verdict") == "PASS" and review.get("blocking_findings") == [], stream + "_PASS")
        gate(review.get("sha") == final and review.get("spec_sha") == spec
             and review.get("base_sha") == base and sha(final), stream + "_exact_identity")
        gate(review.get("tracked_files_modified") is False, stream + "_read_only")
        for key in ("artifact_ref", "reviewer_id", "session_id", "model_profile"):
            gate(nonempty(review.get(key)), stream + "_" + key)
        gate(sha(review.get("content_sha256"), 64), stream + "_artifact_hash")
        gate(review.get("reviewer_id") != packet.get("implementer_id"), stream + "_not_self_review")
        gate(review.get("session_id") != packet.get("implementer_session_id"), stream + "_separate_implementer_session")
        gate(review.get("peer_verdict_used_as_proof") is False, stream + "_independent_verdict")
        valid.append(review)
    if len(valid) == 2:
        gate(valid[0].get("reviewer_id") != valid[1].get("reviewer_id")
             and valid[0].get("session_id") != valid[1].get("session_id"), "separate_reviewer_sessions")
    return blockers



ADOPTION_SECTIONS = {
    "AGENTS.md": "## 25. Conditional project adoption (Phase G)",
    "docs/operations/AUTONOMOUS_AGENT_PROTOCOL.md": "## Conditional project adoption (Phase G)",
    "docs/operations/01_PROJECT_CONTROL_CENTER.md": "### GOV-AGENT-001-G — current adoption status",
    "README.md": "## Conditional project adoption (Phase G)",
}
ADOPTION_FIELDS = {
    "Adoption policy": "CONDITIONAL",
    "Adoption effective boundary": "Accepted Phase G merge/postmerge verification",
    "Preferred process": "V2 for eligible explicitly Human-authorized tasks",
    "V2 enrollment": "EXPLICIT_ONLY",
    "Historical/unenrolled V1": "PRESERVED",
    "MANUAL_EXTERNAL": "MANDATORY",
    "Phase G reviews": "Security AND Quality, separate identities and actual Antigravity sessions",
    "Automatic R0-R4": "NOT ACTIVATED",
    "Identity": "PROCEDURAL_TRUST_BASED",
    "Accepted verifier adapters": "UNAVAILABLE",
    "B3 authoritative_merge_eligible": "false",
    "Evidence": "RECORDED != VERIFIED; provisional_ready != authoritative_merge_eligible",
    "MCP completion transition": "BLOCKED BY TOOL CAPABILITY — disclosed separately",
    "Rollback": "Preserve evidence; separately reviewed Human disable; in-progress Human disposition",
    "Product/provider/production authority": "NOT GRANTED",
    "Phase H / AI-CONV": "NOT STARTED",
    "WORKFLOW_V2_ACTIVATION_COMMIT": "9c291325d409f74bc767f9b870e81d75c9b70802"
}
ADOPTION_SPEC = "docs/tasks/GOV-AGENT-001-G_ADOPTION_SPEC.md"
DECLARATION_FILES = (MARKER, *ADOPTION_SECTIONS,
                     "docs/operations/WORKFLOW_V2_MANUAL_VERIFICATION.md", ADOPTION_SPEC)


def current_section(body: str, heading: str) -> str:
    """Inspect a single designated current section; history cannot satisfy it."""
    headers = list(re.finditer(r"^" + re.escape(heading) + r"$", body, re.MULTILINE))
    require(len(headers) == 1, f"missing/ambiguous current section: {heading}")
    start = headers[0].end()
    following = re.search(r"^#{1,3} ", body[start:], re.MULTILINE)
    return body[start:start + following.start()] if following else body[start:]


def validate_adoption_declarations(root: Path):
    """Read-only text/schema consistency, not adoption activation or authority."""
    for relative, heading in ADOPTION_SECTIONS.items():
        section = current_section((root / relative).read_text(encoding="utf-8"), heading)
        values = {}
        for line in section.splitlines():
            match = re.fullmatch(r"\| ([^|]+) \| ([^|]+) \|", line)
            if match and match[1] in ADOPTION_FIELDS:
                require(match[1] not in values, f"duplicate adoption field: {relative}: {match[1]}")
                values[match[1]] = match[2]
        require(values == ADOPTION_FIELDS, f"conditional adoption boundary changed/missing: {relative}")
        require(not re.search(r"^Adoption policy:\s*ACTIVE\b", section, re.MULTILINE),
                f"premature adoption declaration: {relative}")
    agents = current_section((root / "AGENTS.md").read_text(encoding="utf-8"),
                             ADOPTION_SECTIONS["AGENTS.md"])
    for number in range(1, 10):
        require(len(re.findall(r"^\| G-" + f"{number:02}" + r" \|", agents, re.MULTILINE)) == 1,
                f"missing/ambiguous Human condition G-{number:02}")
    spec = (root / ADOPTION_SPEC).read_text(encoding="utf-8")
    for phrase in ("| Version / date | 0.1.1 / 2026-10-08 |",
                   "HUMAN-GOV-AGENT-001-G-ADOPT-V2-CONDITIONAL-2026-10-08",
                   "19C98EDB6C1EEAC33374C293BF22DCBCFD288363FDF54329DDEE62EF3B980D60",
                   "de23dd70c28a682faa17cbd69c1ce569ecc9c35f",
                   ADOPTION_FIELDS["WORKFLOW_V2_ACTIVATION_COMMIT"],
                   "## 6. Committed-spec ADMIN reconciliation and freeze gate",
                   "## 7. Measurable acceptance criteria"):
        require(phrase in spec, f"missing adoption spec identity/authority: {phrase}")
    require(not re.search(r"(?<![A-Za-z])[A-Za-z]:[/\\]", spec),
            "private absolute Windows path in adoption specification")
    require(".codex/attachments/" not in spec and ".codex\\attachments\\" not in spec,
            "private Codex attachment path in adoption specification")


def validate_repository(root: Path):
    policy = read_marker((root / MARKER).read_text(encoding="utf-8"))
    validate_policy(policy)
    agents = (root / "AGENTS.md").read_text(encoding="utf-8")
    adoption = "| Version | 0.6.1 |" in agents or any(
        (root / relative).exists() and heading in (root / relative).read_text(encoding="utf-8")
        for relative, heading in ADOPTION_SECTIONS.items())
    agent_version = "0.6.1" if adoption else "0.5.0"
    protocol_version = "0.3.1" if adoption else "0.2.0"
    for relative, phrases in {
        "AGENTS.md": (f"| Version | {agent_version} |", "## 24. Conditional Workflow V2 governance",
            "WORKFLOW_V2_ACTIVATION_COMMIT", "MANUAL_EXTERNAL", "PROCEDURAL_TRUST_BASED",
            "SECURITY_REVIEWER", "QUALITY_REVIEWER", "Historical V1", "Section 19 stop condition"),
        "docs/operations/AUTONOMOUS_AGENT_PROTOCOL.md": (f"Version: {protocol_version}", "APPROVED -> CLAIMED",
            "WORKFLOW_V2_ACTIVATION_COMMIT", "Remaining <=8", "external", "never"),
        "docs/operations/WORKFLOW_V2_MANUAL_VERIFICATION.md": ("Version: 1.0.0",
            "E-01", "E-02", "E-03", "E-04", "E-05", "E-06", "Required authoritative pre-merge procedure",
            "PHASE E BRANCH PRESENT != WORKFLOW V2 ACTIVATED", "provisional_ready != authoritative_merge_eligible",
            "RECORDED != VERIFIED", "fresh", "rollback", "not a cryptographic", "Phase F is NOT STARTED"),
        "README.md": ("GOV-AGENT-001-D | CLOSED / COMPLETED", "GOV-AGENT-001-E |",
            "MANUAL / EXTERNAL", "Historical/unenrolled tasks remain V1"),
    }.items():
        body = (root / relative).read_text(encoding="utf-8")
        for phrase in phrases:
            require(phrase in body, f"missing governance declaration: {relative}: {phrase}")
    if adoption:
        validate_adoption_declarations(root)
    return policy


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    try:
        validate_repository(args.root)
    except (ValidationError, OSError, ValueError, TypeError, KeyError) as error:
        print(f"BLOCKED: {error}", file=sys.stderr)
        return 1
    print("PASS: Phase E marker, E-01–E-06, V1/V2 and applicable conditional Phase G declarations")
    print("Structural checks do not establish activation, verify sources, enroll tasks or authorize a merge")
    print("Branch/open PR does not establish activation/adoption; accepted merge/postmerge verification is required")
    return 0


if __name__ == "__main__":
    sys.exit(main())
