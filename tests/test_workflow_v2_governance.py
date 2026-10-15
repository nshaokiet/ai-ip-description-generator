"""SYNTHETIC Phase E policy scenarios; no approval, enrollment or source verification."""
from copy import deepcopy
import hashlib
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/validate_workflow_v2_governance.py"
MODULE_SPEC = importlib.util.spec_from_file_location("phase_e_policy", SCRIPT)
policy_check = importlib.util.module_from_spec(MODULE_SPEC)
MODULE_SPEC.loader.exec_module(policy_check)


def policy():
    return policy_check.read_marker((ROOT / policy_check.MARKER).read_text(encoding="utf-8"))


def observed():
    # Every identity/result here is invented TEST DATA, never real project evidence.
    return dict.fromkeys((
        "source_verified", "phase_e_pr_merged", "human_activation_approved",
        "governance_review_pass", "required_ci_success", "merge_eligible",
        "reviewed_sha_contained_in_merge", "activation_merge_in_main_ancestry",
        "postmerge_verified", "postmerge_ci_success"), True) | {
        "source_branch": "main", "activation_merge_sha": "a" * 40,
        "reviewed_head_sha": "b" * 40, "review_sha": "b" * 40,
        "ci_sha": "b" * 40, "main_ci_sha": "a" * 40,
    }


def task():
    return {
        "task_id": "SYNTHETIC-TASK", "human_authorized": True,
        "authorization_ref": "SYNTHETIC:Human-authority", "activation_commit": "a" * 40,
        "explicit_enrollment_requested": True, "enrolled": True,
        "historical_v1": False, "has_execution_history": False,
        "has_v2_history": False, "required_state_exists": True,
    }


def packet():
    result = dict.fromkeys((
        "human_scope_authorized", "human_exceptions_resolved", "frozen_spec_committed",
        "human_freeze_authorized", "implementation_base_branch_verified", "ci_success",
        "fresh_pr_check", "pr_open", "pr_mergeable", "scope_safe",
        "no_secret_confidential_exposure", "no_stop_condition", "platform_controls_satisfied"), True)
    result.update({key: "SYNTHETIC:" + key for key in (
        "human_authorization_ref", "spec_artifact_ref", "human_freeze_ref", "git_ref",
        "ci_ref", "fresh_pr_ref", "repository", "branch", "pr_number",
        "implementer_id", "implementer_session_id")})
    result.update({
        "final_sha": "b" * 40, "spec_sha": "d" * 40, "base_sha": "c" * 40,
        "spec_version": "0.2.1", "ci_sha": "b" * 40, "pr_head_sha": "b" * 40,
        "mcp_provisional_used_as_permission": False, "mcp_authoritative_merge_eligible": False,
        "pilot": True, "required_reviews": {"SECURITY": True, "QUALITY": True}, "reviews": {},
    })
    for stream in ("SECURITY", "QUALITY"):
        result["reviews"][stream] = {
            "stream": stream, "verdict": "PASS", "blocking_findings": [],
            "sha": "b" * 40, "spec_sha": "d" * 40, "base_sha": "c" * 40,
            "tracked_files_modified": False, "peer_verdict_used_as_proof": False,
            "artifact_ref": "SYNTHETIC:immutable-report-" + stream,
            "reviewer_id": "SYNTHETIC:reviewer-" + stream,
            "session_id": "SYNTHETIC:session-" + stream,
            "model_profile": "SYNTHETIC:model-profile", "content_sha256": "e" * 64,
        }
    return result


class ActivationAndEnrollmentTests(unittest.TestCase):
    def test_enabled_policy_without_main_merge_is_not_activation(self):
        facts = observed()
        facts.update(source_branch="feat/SYNTHETIC", phase_e_pr_merged=False)
        self.assertFalse(policy_check.effective_activation(policy(), facts))
        self.assertFalse(policy_check.enrollment_preflight(policy(), facts, task()))
        self.assertEqual(policy_check.workflow_selection(policy(), facts, task()), "V1")

    def test_review_and_ci_pass_on_open_pr_are_insufficient(self):
        facts = observed() | {"phase_e_pr_merged": False}
        self.assertFalse(policy_check.effective_activation(policy(), facts))

    def test_each_missing_or_unverified_activation_fact_blocks(self):
        for key, value in observed().items():
            if type(value) is not bool:
                continue
            for invalid in (False, None, 1, "true"):
                with self.subTest(key=key, invalid=invalid):
                    self.assertFalse(policy_check.effective_activation(policy(), observed() | {key: invalid}))

    def test_activation_uses_distinct_merge_and_exact_ci_review_identities(self):
        for key in ("activation_merge_sha", "reviewed_head_sha", "review_sha", "ci_sha", "main_ci_sha"):
            with self.subTest(key=key):
                self.assertFalse(policy_check.effective_activation(policy(), observed() | {key: "f" * 40}))
        same = observed() | {key: "b" * 40 for key in ("activation_merge_sha", "main_ci_sha")}
        self.assertFalse(policy_check.effective_activation(policy(), same))

    def test_valid_synthetic_main_merge_allows_explicit_authorized_enrollment(self):
        self.assertTrue(policy_check.effective_activation(policy(), observed()))
        self.assertTrue(policy_check.enrollment_preflight(policy(), observed(), task()))
        self.assertEqual(policy_check.workflow_selection(policy(), observed(), task()), "V2")

    def test_off_and_unenrolled_tasks_keep_v1(self):
        disabled = policy() | {"enabled": False}
        for config, candidate in ((disabled, task()), (policy(), task() | {"enrolled": False})):
            self.assertEqual(policy_check.workflow_selection(config, observed(), candidate), "V1")
        self.assertFalse(policy_check.enrollment_preflight(disabled, observed(), task()))

    def test_admission_requires_authority_explicit_request_and_immutable_reference(self):
        for key, value in {
            "human_authorized": False, "authorization_ref": "", "task_id": "",
            "explicit_enrollment_requested": False, "activation_commit": "b" * 40,
            "historical_v1": True, "has_execution_history": True, "has_v2_history": True,
        }.items():
            with self.subTest(key=key):
                self.assertFalse(policy_check.enrollment_preflight(policy(), observed(), task() | {key: value}))

    def test_required_authority_enrollment_reference_state_for_v2_selection(self):
        for key, value in {
            "human_authorized": False, "authorization_ref": " ", "enrolled": False,
            "historical_v1": True, "activation_commit": "b" * 40, "required_state_exists": False,
        }.items():
            with self.subTest(key=key):
                self.assertEqual(policy_check.workflow_selection(policy(), observed(), task() | {key: value}), "V1")

    def test_historical_v1_evidence_cannot_be_backfilled(self):
        historical = task() | {"historical_v1": True, "has_execution_history": True,
                               "evidence": ["SYNTHETIC:original-v1-checkpoint"]}
        before = deepcopy(historical)
        self.assertFalse(policy_check.enrollment_preflight(policy(), observed(), historical))
        self.assertEqual(policy_check.workflow_selection(policy(), observed(), historical), "V1")
        self.assertEqual(historical, before)

    def test_disable_preserves_active_v2_history_and_requires_human_disposition(self):
        active = task() | {"has_v2_history": True, "has_execution_history": True,
                           "evidence": ["SYNTHETIC:spec", "SYNTHETIC:review", "SYNTHETIC:ci"]}
        before = deepcopy(active)
        self.assertEqual(policy_check.workflow_selection(policy() | {"enabled": False}, observed(), active),
                         "BLOCKED_HUMAN_DISPOSITION")
        self.assertFalse(policy_check.enrollment_preflight(policy() | {"enabled": False}, observed(), active))
        self.assertEqual(active, before)

    def test_invalid_existing_v2_evidence_never_silently_falls_back(self):
        for key, value in (("activation_commit", "f" * 40), ("required_state_exists", False),
                           ("human_authorized", False)):
            with self.subTest(key=key):
                self.assertEqual(policy_check.workflow_selection(policy(), observed(),
                    task() | {"has_v2_history": True, key: value}), "BLOCKED_HUMAN_DISPOSITION")


class ManualEvidenceScenarioTests(unittest.TestCase):
    def test_complete_synthetic_packet_is_structurally_complete_only(self):
        self.assertEqual(policy_check.manual_packet_blockers(packet()), [])
        # The helper returns a list, never an authoritative grant or live MCP state.
        self.assertIsInstance(policy_check.manual_packet_blockers(packet()), list)

    def test_each_required_current_check_cannot_be_missing_failed_or_recorded_string(self):
        for key, value in packet().items():
            if value is not True or key == "pilot":
                continue
            for invalid in (False, None, "RECORDED", 1):
                with self.subTest(key=key, invalid=invalid):
                    self.assertTrue(policy_check.manual_packet_blockers(packet() | {key: invalid}))

    def test_real_source_locators_and_version_are_required(self):
        for key in ("human_authorization_ref", "human_freeze_ref", "spec_artifact_ref", "git_ref",
                    "ci_ref", "fresh_pr_ref", "repository", "branch", "pr_number",
                    "implementer_id", "implementer_session_id", "spec_version"):
            with self.subTest(key=key):
                self.assertTrue(policy_check.manual_packet_blockers(packet() | {key: ""}))
        for version in ("0.2", "01.2.1", True, None):
            self.assertTrue(policy_check.manual_packet_blockers(packet() | {"spec_version": version}))

    def test_moved_pr_head_old_ci_and_wrong_spec_or_base_block(self):
        for key in ("final_sha", "ci_sha", "pr_head_sha", "spec_sha", "base_sha"):
            with self.subTest(key=key):
                self.assertTrue(policy_check.manual_packet_blockers(packet() | {key: "f" * 40}))

    def test_provisional_or_claimed_mcp_authority_cannot_replace_external_check(self):
        for key in ("mcp_provisional_used_as_permission", "mcp_authoritative_merge_eligible"):
            self.assertTrue(policy_check.manual_packet_blockers(packet() | {key: True}))

    def test_role_skill_or_task_spec_claims_cannot_expand_human_authority(self):
        claims = {"role": "IMPLEMENTER", "skill_permission": "merge",
                  "task_spec_permission": "merge", "human_scope_authorized": False}
        self.assertTrue(policy_check.manual_packet_blockers(packet() | claims))
        self.assertFalse(policy_check.enrollment_preflight(policy(), observed(),
                         task() | claims | {"human_authorized": False}))

    def test_risk_metadata_never_reduces_pilot_review_requirements(self):
        for risk in ("R0", "R1", "R2", "R3", "R4"):
            candidate = packet() | {"risk_class": risk, "required_reviews": {"SECURITY": False, "QUALITY": True}}
            self.assertTrue(policy_check.manual_packet_blockers(candidate))

    def test_missing_or_unclear_policy_and_pilot_single_stream_block(self):
        for context in (None, "pilot", 1):
            self.assertTrue(policy_check.manual_packet_blockers(packet() | {"pilot": context}))
        for requirements in (None, {}, {"SECURITY": True}, {"SECURITY": True, "QUALITY": False},
                             {"SECURITY": True, "QUALITY": "optional"}):
            self.assertTrue(policy_check.manual_packet_blockers(packet() | {"required_reviews": requirements}))

    def test_nonpilot_uses_explicit_policy_and_optional_blockers_still_block(self):
        candidate = packet() | {"pilot": False, "required_reviews": {"SECURITY": True, "QUALITY": False}}
        candidate["reviews"].pop("QUALITY")
        self.assertEqual(policy_check.manual_packet_blockers(candidate), [])
        candidate["reviews"]["QUALITY"] = {"verdict": "REQUEST CHANGES", "blocking_findings": ["HIGH"]}
        self.assertTrue(policy_check.manual_packet_blockers(candidate))

    def test_required_reviews_must_be_same_sha_independent_readonly_hash_bound_pass(self):
        invalid_fields = {
            "stream": "OTHER", "verdict": "REQUEST CHANGES", "blocking_findings": ["HIGH"],
            "sha": "f" * 40, "spec_sha": "f" * 40, "base_sha": "f" * 40,
            "tracked_files_modified": True, "peer_verdict_used_as_proof": True,
            "artifact_ref": "", "reviewer_id": "SYNTHETIC:implementer_id",
            "session_id": "SYNTHETIC:implementer_session_id", "model_profile": "",
            "content_sha256": "not-a-hash",
        }
        for stream in ("SECURITY", "QUALITY"):
            missing = packet()
            missing["reviews"].pop(stream)
            self.assertTrue(policy_check.manual_packet_blockers(missing))
            for key, value in invalid_fields.items():
                with self.subTest(stream=stream, key=key):
                    candidate = packet()
                    candidate["reviews"][stream][key] = value
                    self.assertTrue(policy_check.manual_packet_blockers(candidate))

    def test_security_quality_must_use_separate_reviewers_and_sessions(self):
        for key in ("reviewer_id", "session_id"):
            candidate = packet()
            candidate["reviews"]["QUALITY"][key] = candidate["reviews"]["SECURITY"][key]
            self.assertTrue(policy_check.manual_packet_blockers(candidate))

    def test_malformed_review_artifacts_fail_closed(self):
        for reviews in ([], {"SECURITY": "PASS", "QUALITY": None}, {"UNKNOWN": {}}):
            self.assertTrue(policy_check.manual_packet_blockers(packet() | {"reviews": reviews}))
        candidate = packet() | {"pilot": False, "required_reviews": {"SECURITY": True, "QUALITY": False}}
        candidate["reviews"]["QUALITY"] = "PASS"
        self.assertTrue(policy_check.manual_packet_blockers(candidate))


class MarkerAndReadOnlyCliTests(unittest.TestCase):
    def test_canonical_declarations_validate(self):
        policy_check.validate_repository(ROOT)

    def test_disable_is_valid_policy_without_erasing_other_boundaries(self):
        disabled = policy() | {"enabled": False}
        policy_check.validate_policy(disabled)
        self.assertFalse(policy_check.effective_activation(disabled, observed()))

    def test_policy_cannot_enable_adapters_crypto_routing_backfill_or_evidence_deletion(self):
        for section, key, value in (
            ("identity", "cryptographically_authenticated", True),
            ("enrollment", "historical_v1_backfill", True),
            ("enrollment", "human_task_authorization_required", False),
            ("merge_verification", "authoritative_verifier_adapter_available", True),
            ("merge_verification", "mcp_provisional_ready_is_merge_permission", True),
            ("merge_verification", "fresh_external_premerge_check_required", False),
            ("risk_routing", "automatic_r0_r4", True),
            ("risk_routing", "pilot_security_review_required", False),
            ("risk_routing", "pilot_quality_review_required", False),
            ("rollback", "preserve_v2_evidence", False),
            ("rollback", "silent_v2_to_v1_translation", True),
            ("rollback", "disable_stops_new_enrollment", False),
            ("activation", "implementation_sha_is_activation_commit", True),
        ):
            with self.subTest(section=section, key=key):
                candidate = policy()
                candidate[section][key] = value
                with self.assertRaises(policy_check.ValidationError):
                    policy_check.validate_policy(candidate)

    def test_missing_unknown_wrong_type_and_self_referential_sha_rejected(self):
        for mutate in (
            lambda value: value.pop("rollback"),
            lambda value: value.update(enabled=1),
            lambda value: value.update(activation_commit="a" * 40),
            lambda value: value.update(schema_version=True),
        ):
            candidate = policy()
            mutate(candidate)
            with self.assertRaises(policy_check.ValidationError):
                policy_check.validate_policy(candidate)

    def test_duplicate_or_unsupported_yaml_rejected(self):
        for raw in ("enabled: true\nenabled: false", "activation:\n\tphase: E", "enabled: [true]",
                    "enabled: &on true", "enabled: 'true'", "activation:\n    phase: E", ""):
            with self.subTest(raw=raw), self.assertRaises(policy_check.ValidationError):
                policy_check.read_marker(raw)

    def test_cli_checks_real_declarations_without_mutating_files(self):
        files = policy_check.DECLARATION_FILES
        with tempfile.TemporaryDirectory(prefix="SYNTHETIC-phase-e-") as folder:
            root = Path(folder)
            for relative in files:
                destination = root / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / relative, destination)
            before = {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in files}
            result = subprocess.run([sys.executable, str(SCRIPT), "--root", str(root)],
                                    capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("do not establish activation", result.stdout)
            self.assertEqual(before, {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in files})
            (root / policy_check.MARKER).unlink()
            missing = subprocess.run([sys.executable, str(SCRIPT), "--root", str(root)],
                                     capture_output=True, text=True, encoding="utf-8")
            self.assertNotEqual(missing.returncode, 0)
            self.assertIn("BLOCKED", missing.stderr)



class ConditionalAdoptionDeclarationTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory(prefix="SYNTHETIC-phase-g-declarations-")
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        for relative in policy_check.DECLARATION_FILES:
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, destination)

    def change_field(self, relative, field, value):
        path = self.root / relative
        original = (ROOT / relative).read_text(encoding="utf-8")
        before = f"| {field} | {policy_check.ADOPTION_FIELDS[field]} |"
        self.assertEqual(original.count(before), 1)
        path.write_text(original.replace(before, f"| {field} | {value} |"), encoding="utf-8")

    def test_canonical_adoption_declarations_are_static_only(self):
        before = {name: (self.root / name).read_bytes()
                  for name in policy_check.DECLARATION_FILES}
        self.assertEqual(policy_check.validate_repository(self.root), policy())
        policy_check.validate_adoption_declarations(self.root)
        self.assertEqual(before, {name: (self.root / name).read_bytes() for name in before})

    def test_each_current_document_requires_its_unique_adoption_section(self):
        for relative, heading in policy_check.ADOPTION_SECTIONS.items():
            path = self.root / relative
            original = (ROOT / relative).read_text(encoding="utf-8")
            for candidate in (original.replace(heading, heading + " HISTORICAL", 1),
                              original + "\n" + heading + "\n"):
                with self.subTest(relative=relative), self.assertRaises(policy_check.ValidationError):
                    path.write_text(candidate, encoding="utf-8")
                    policy_check.validate_repository(self.root)
            path.write_text(original, encoding="utf-8")

    def test_historical_policy_cannot_mask_a_missing_current_obligation(self):
        path = self.root / "AGENTS.md"
        original = path.read_text(encoding="utf-8")
        row = "| MANUAL_EXTERNAL | MANDATORY |"
        path.write_text(original.replace(row, "", 1) +
                        "\n## Historical declaration\n" + row + "\n", encoding="utf-8")
        with self.assertRaises(policy_check.ValidationError):
            policy_check.validate_repository(self.root)

    def test_duplicate_policy_fields_and_missing_human_conditions_block(self):
        path = self.root / "AGENTS.md"
        original = path.read_text(encoding="utf-8")
        row = "| V2 enrollment | EXPLICIT_ONLY |"
        path.write_text(original.replace(row, row + "\n" + row, 1), encoding="utf-8")
        with self.assertRaises(policy_check.ValidationError):
            policy_check.validate_repository(self.root)
        for number in range(1, 10):
            lines = original.splitlines()
            condition = next(line for line in lines if line.startswith(f"| G-{number:02} |"))
            with self.subTest(condition=number), self.assertRaises(policy_check.ValidationError):
                path.write_text(original.replace(condition, "", 1) +
                                "\n## Historical condition\n" + condition + "\n", encoding="utf-8")
                policy_check.validate_repository(self.root)

    def test_no_admission_migration_routing_trust_or_product_promotion(self):
        prohibited = {
            "V2 enrollment": "AUTOMATIC",
            "Historical/unenrolled V1": "AUTO_MIGRATE_TO_V2",
            "MANUAL_EXTERNAL": "OPTIONAL",
            "Phase G reviews": "Security OR Quality",
            "Automatic R0-R4": "ACTIVATED",
            "Identity": "AUTHENTICATED",
            "Accepted verifier adapters": "AVAILABLE",
            "B3 authoritative_merge_eligible": "true",
            "Evidence": "RECORDED == VERIFIED",
            "MCP completion transition": "COMPLETED via V1 transition",
            "Rollback": "Delete history; silently translate V2 to V1",
            "Product/provider/production authority": "GRANTED",
            "Phase H / AI-CONV": "STARTED",
            "WORKFLOW_V2_ACTIVATION_COMMIT": "a" * 40,
        }
        for relative in policy_check.ADOPTION_SECTIONS:
            for field, value in prohibited.items():
                with self.subTest(relative=relative, field=field), self.assertRaises(policy_check.ValidationError):
                    self.change_field(relative, field, value)
                    policy_check.validate_repository(self.root)
            shutil.copyfile(ROOT / relative, self.root / relative)

    def test_review_pass_open_pr_and_branch_do_not_declare_adoption_active(self):
        for value in ("Branch exists", "PR OPEN", "Review PASS", "STATIC PASS"):
            with self.subTest(value=value), self.assertRaises(policy_check.ValidationError):
                self.change_field("README.md", "Adoption effective boundary", value)
                policy_check.validate_repository(self.root)
        self.change_field("README.md", "Adoption policy", "ACTIVE")
        with self.assertRaises(policy_check.ValidationError):
            policy_check.validate_repository(self.root)
        shutil.copyfile(ROOT / "README.md", self.root / "README.md")
        body = (self.root / "README.md").read_text(encoding="utf-8")
        heading = policy_check.ADOPTION_SECTIONS["README.md"]
        (self.root / "README.md").write_text(
            body.replace(heading, heading + "\n\nAdoption policy: ACTIVE", 1), encoding="utf-8")
        with self.assertRaises(policy_check.ValidationError):
            policy_check.validate_repository(self.root)

    def test_current_document_versions_and_spec_provenance_are_required(self):
        for relative, before, after in (
            ("AGENTS.md", "| Version | 0.6.2 |", "| Version | 0.5.0 |"),
            ("docs/operations/AUTONOMOUS_AGENT_PROTOCOL.md", "Version: 0.3.1", "Version: 0.2.0"),
            (policy_check.ADOPTION_SPEC, "## 6. Committed-spec ADMIN reconciliation and freeze gate", "No freeze gate"),
            (policy_check.ADOPTION_SPEC, "19C98EDB6C1EEAC33374C293BF22DCBCFD288363FDF54329DDEE62EF3B980D60", "missing"),
        ):
            path = self.root / relative
            original = (ROOT / relative).read_text(encoding="utf-8")
            with self.subTest(relative=relative), self.assertRaises(policy_check.ValidationError):
                path.write_text(original.replace(before, after, 1), encoding="utf-8")
                policy_check.validate_repository(self.root)
            path.write_text(original, encoding="utf-8")
        (self.root / policy_check.ADOPTION_SPEC).unlink()
        with self.assertRaises(OSError):
            policy_check.validate_repository(self.root)

    def test_superseded_spec_version_and_private_metadata_paths_block(self):
        path = self.root / policy_check.ADOPTION_SPEC
        original = path.read_text(encoding="utf-8")
        for candidate in (
            original.replace("| Version / date | 0.1.1 /", "| Version / date | 0.1.0 /", 1),
            original + "\nSynthetic attachment: C:/Users/SYNTHETIC/.codex/attachments/example\n",
            original + "\nSynthetic worktree: D:\\SYNTHETIC\\repo\\worktree\n",
        ):
            with self.subTest(candidate=candidate[-90:]), self.assertRaises(policy_check.ValidationError):
                path.write_text(candidate, encoding="utf-8")
                policy_check.validate_repository(self.root)
        path.write_text(original, encoding="utf-8")

    def test_phase_e_declarations_remain_compatible_without_adoption(self):
        for relative, heading in policy_check.ADOPTION_SECTIONS.items():
            path = self.root / relative
            body = path.read_text(encoding="utf-8")
            body = body.replace(heading + policy_check.current_section(body, heading), "", 1)
            body = body.replace("| Version | 0.6.2 |", "| Version | 0.5.0 |")
            body = body.replace("Version: 0.3.1", "Version: 0.2.0")
            path.write_text(body, encoding="utf-8")
        self.assertEqual(policy_check.validate_repository(self.root), policy())

if __name__ == "__main__":
    unittest.main()
