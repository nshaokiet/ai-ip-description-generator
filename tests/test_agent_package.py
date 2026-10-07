"""Phase D integrity mutations run in temporary copies, never canonical artefacts."""
import contextlib
import hashlib
import importlib.util
import io
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "agents"
SPEC = importlib.util.spec_from_file_location("phase_d_validate", ROOT / "validate_skills.py")
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def fixture_yaml(value, indent=0):
    """Serialize fixture mutations in the existing manifest's simple YAML subset."""
    def scalar(item):
        return str(item).lower() if type(item) is bool else str(item)
    lines = []
    if isinstance(value, dict):
        for key, item in value.items():
            prefix = " " * indent + key + ":"
            if isinstance(item, (dict, list)):
                lines.append(prefix)
                lines.extend(fixture_yaml(item, indent + 2).splitlines())
            else:
                lines.append(prefix + " " + scalar(item))
    else:
        lines.extend(" " * indent + "- " + scalar(item) for item in value)
    return "\n".join(lines) + "\n"


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "agents"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns("__pycache__"))
        docs = self.root.parent / "docs/tasks"
        docs.mkdir(parents=True)
        for name in ("P2-002-invention-reconstruction.md",
                     "P2-003-uspto-specification-generation-v2.md", "P2-004-supported-draft-claims.md"):
            shutil.copyfile(ROOT.parent / "docs/tasks" / name, docs / name)
        self.manifest = validator.read_manifest((self.root / "manifest.yaml").read_text(encoding="utf-8"))

    def save(self):
        (self.root / "manifest.yaml").write_text(fixture_yaml(self.manifest), encoding="utf-8")

    def blocked(self, message):
        self.save()
        with self.assertRaisesRegex(validator.ValidationError, message):
            validator.validate_package(self.root)

    def edit(self, relative, before, after):
        p = self.root / relative
        body = p.read_text(encoding="utf-8")
        self.assertIn(before, body)
        p.write_text(body.replace(before, after), encoding="utf-8")

    def version(self, version):
        self.manifest["skills"]["shared_project_context"]["version"] = version
        self.edit("skills/shared/project-context/SKILL.md", "- version: `1.0.0`",
                  f"- version: `{version}`")

    def test_valid_package_and_exact_mapping(self):
        mapping = validator.validate_package(self.root)
        self.assertEqual([len(mapping[r]) for r in validator.ROLE_GROUPS], [7, 7, 7, 8])
        self.assertEqual(len(self.manifest["skills"]), 14)

    def test_semver_digit_regression_and_compatible_stable(self):
        for version in ("1.0.0", "1.0.1", "1.9.3", "1.0.0+build.5"):
            with self.subTest(version=version):
                self.assertEqual(validator.major(version), 1)
                self.assertEqual(validator.resolve(1, version), "AVAILABLE")
        self.assertEqual(validator.major("1.0.0-rc.1"), 1)
        self.assertEqual(validator.resolve(1, "1.0.0-rc.1"), "BLOCKED")

    def test_invalid_semver_rejected_and_resolution_blocked(self):
        for version in ("1", "1.0", "01.0.0", "1.00.0", "v1.0.0", "1.0.0-01",
                        "1.0.0+", "1.0.0\n", "١.0.0", True, None):
            with self.subTest(version=version):
                with self.assertRaises(validator.ValidationError):
                    validator.major(version)
                self.assertEqual(validator.resolve(1, version), "BLOCKED")

    def test_resolution_missing_incompatible_conflict_and_unavailable(self):
        self.assertEqual(validator.resolve(1, None), "BLOCKED")
        self.assertEqual(validator.resolve(1, "2.0.0"), "BLOCKED")
        self.assertEqual(validator.resolve(1, "1.0.0", governance_conflict=True), "BLOCKED")
        self.assertEqual(validator.resolve(1, "1.0.0", unavailable=True), "BLOCKED")
        self.assertEqual(validator.resolve(True, "1.0.0"), "BLOCKED")

    def test_missing_required_disk_skill(self):
        (self.root / "skills/shared/project-context/SKILL.md").unlink()
        self.blocked("missing or unexpected on-disk skill")

    def test_missing_manifest_skill(self):
        del self.manifest["skills"]["shared_project_context"]
        self.blocked("14-skill manifest inventory")

    def test_extra_manifest_skill(self):
        self.manifest["skills"]["extra"] = dict(self.manifest["skills"]["shared_project_context"], id="shared/extra")
        self.blocked("14-skill manifest inventory")

    def test_extra_on_disk_skill(self):
        path = self.root / "skills/shared/fifteenth/SKILL.md"
        path.parent.mkdir()
        path.write_text("unexpected", encoding="utf-8")
        self.blocked("unexpected on-disk skill")

    def test_duplicate_identity(self):
        self.manifest["skills"]["extra"] = self.manifest["skills"]["shared_project_context"].copy()
        self.blocked("duplicate skill identity")

    def test_duplicate_manifest_keys(self):
        with self.assertRaisesRegex(validator.ValidationError, "duplicate manifest key"):
            validator.read_manifest("schema_version: 2\nschema_version: 2\n")

    def test_unsupported_yaml_fails_closed(self):
        for text in ("name: &anchor value\n", "name: [one, two]\n", "name: |\n  text\n",
                     "name: 'quoted'\n", "name: value # ignored?\n", "name:\n   nested: value\n", ""):
            with self.subTest(text=text), self.assertRaises(validator.ValidationError):
                validator.read_manifest(text)

    def test_duplicate_skill_metadata(self):
        self.edit("skills/shared/project-context/SKILL.md", "- name: `project-context`",
                  "- name: `project-context`\n- name: `project-context`")
        self.blocked("duplicate skill metadata")

    def test_wrong_skill_identity(self):
        self.edit("skills/shared/project-context/SKILL.md", "- name: `project-context`", "- name: `governance`")
        self.blocked("identity mismatch")

    def test_missing_contract_fields(self):
        p = self.root / "skills/shared/project-context/SKILL.md"
        original = p.read_text(encoding="utf-8")
        for field in validator.REQUIRED_HEADINGS:
            with self.subTest(field=field):
                p.write_text(original.replace("## " + field, "## Removed"), encoding="utf-8")
                self.blocked("missing/empty contract field")
        p.write_text(original, encoding="utf-8")

    def test_empty_contract_field(self):
        self.edit("skills/shared/project-context/SKILL.md",
                  "Load and reconcile the authorized project/task context before role work begins.", "")
        self.blocked("missing/empty contract field: Purpose")

    def test_duplicate_contract_field(self):
        self.edit("skills/shared/project-context/SKILL.md", "## Purpose", "## Purpose\n\nextra\n\n## Purpose")
        self.blocked("duplicate contract field")

    def test_invalid_manifest_and_skill_version(self):
        self.version("not-semver")
        self.blocked("invalid semantic version")

    def test_incompatible_major(self):
        self.version("2.0.0")
        self.blocked("incompatible version")

    def test_prerelease_not_silently_substituted(self):
        self.version("1.0.0-rc.1")
        self.blocked("incompatible version")

    def test_manifest_document_version_disagreement(self):
        self.manifest["skills"]["shared_project_context"]["version"] = "1.0.1"
        self.blocked("version mismatch")

    def test_wrong_role_mapping(self):
        self.manifest["roles"]["PLANNER"]["required_p0_skills"][-1] = "implementer/safe-code-change@^1.0"
        self.blocked("wrong role mapping")

    def test_duplicate_role_requirement(self):
        self.manifest["roles"]["PLANNER"]["required_p0_skills"].append("shared/governance@^1.0")
        self.blocked("wrong role mapping")

    def test_wrong_compatible_major_pin(self):
        self.manifest["roles"]["PLANNER"]["required_p0_skills"][0] = "shared/project-context@^2.0"
        self.blocked("compatible-major pin")

    def test_boolean_supported_major(self):
        self.manifest["skill_resolution"]["supported_major"] = True
        self.blocked("unapproved required major")

    def test_role_document_mapping_drift(self):
        self.edit("roles/planner.md", "planner/architecture-analysis@^1.0", "implementer/safe-code-change@^1.0")
        self.blocked("role document mapping mismatch")

    def test_wrong_role_contract_target(self):
        self.manifest["roles"]["PLANNER"]["contract"] = "roles/nonexistent.md"
        self.blocked("wrong role contract target")

    def test_missing_review_template(self):
        (self.root / "review-templates/security-review.md").unlink()
        self.blocked("missing/unavailable manifest target")

    def test_path_escape(self):
        self.manifest["skills"]["shared_project_context"]["path"] = "../../outside/SKILL.md"
        self.blocked("target escapes package")

    def test_noncanonical_existing_target(self):
        self.manifest["skills"]["shared_project_context"]["path"] = "skills/shared/governance/SKILL.md"
        self.blocked("noncanonical P0 target")

    def test_skill_role_authority(self):
        self.edit("skills/quality/fixed-sha-review/SKILL.md", "- role_scope: `QUALITY`", "- role_scope: `IMPLEMENTER`")
        self.blocked("skill role authority mismatch")

    def test_reviewer_write_authority(self):
        self.manifest["roles"]["SECURITY_REVIEWER"]["tracked_implementation_write"] = True
        self.blocked("role write authority expanded")

    def test_numeric_false_is_not_boolean_false(self):
        self.manifest["roles"]["SECURITY_REVIEWER"]["tracked_implementation_write"] = 0
        self.blocked("role write authority expanded")

    def test_cross_stream_and_self_review_verdict(self):
        for role in ("SECURITY_REVIEWER", "IMPLEMENTER"):
            with self.subTest(role=role):
                old = self.manifest["roles"][role]["independent_verdict"]
                self.manifest["roles"][role]["independent_verdict"] = "QUALITY_ONLY"
                self.blocked("role verdict authority expanded")
                self.manifest["roles"][role]["independent_verdict"] = old

    def test_reviewer_read_only_contract_removed(self):
        self.edit("roles/security-reviewer.md", "Do not modify tracked implementation", "Modify tracked implementation")
        self.blocked("reviewer read-only boundary")

    def test_fail_open_resolution_rules(self):
        for key in ("missing_required", "incompatible_major", "unavailable_required", "governance_conflict"):
            with self.subTest(key=key):
                self.manifest["skill_resolution"][key] = "AVAILABLE"
                self.blocked("fail-closed resolution")
                self.manifest["skill_resolution"][key] = "BLOCKED"

    def test_silent_substitution_and_authority_expansion(self):
        self.manifest["skill_resolution"]["silent_substitution_allowed"] = True
        self.blocked("substitution")
        self.manifest["skill_resolution"]["silent_substitution_allowed"] = False
        self.manifest["skill_resolution"]["task_spec_may_narrow_only"] = False
        self.blocked("governance conflict")

    def test_activation(self):
        self.manifest["package"]["workflow_v2_activation"] = "ACTIVATED"
        self.blocked("activation/model boundary")

    def test_mcp_verifier_cannot_be_invented(self):
        self.manifest["mcp_foundation"]["phase_b3"]["authoritative_merge_adapter_available"] = True
        self.blocked("verifier must remain unavailable")

    def test_evidence_trust_promotion(self):
        self.manifest["evidence_semantics"]["recorded_equals_verified"] = True
        self.blocked("evidence trust mismatch")

    def test_independence_contract_missing(self):
        del self.manifest["independence"]["stale_sha_pass_reusable"]
        self.blocked("missing independence contract")

    def test_governance_conflict_in_skill(self):
        self.edit("skills/shared/project-context/SKILL.md", "Governance takes precedence over this skill.",
                  "This skill takes precedence over governance.")
        self.blocked("skill/governance conflict")

    def test_governance_precedence_inversion(self):
        self.edit("skills/shared/governance/SKILL.md", "1. Human-authorized active governance.",
                  "1. skill procedure.")
        self.blocked("governance precedence mismatch")

    def test_ai_ip_principle_missing(self):
        self.edit("skills/shared/ai-ip-domain/SKILL.md", "INFERENCE != SOURCE_FACT", "INFERENCE == SOURCE_FACT")
        self.blocked("missing AI-IP principle")

    def test_p2_contract_reference_missing(self):
        (self.root.parent / "docs/tasks/P2-002-invention-reconstruction.md").unlink()
        self.blocked("missing P2 reference")

    def test_committed_cli_success_failure_and_canonical_unchanged(self):
        def snapshot():
            return {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in ROOT.rglob("*") if p.is_file() and "__pycache__" not in p.parts}
        original = snapshot()
        command = [sys.executable, str(ROOT / "validate_skills.py"), "--root", str(self.root)]
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        result = subprocess.run(command, text=True, capture_output=True, env=env, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS: 14/14", result.stdout)
        (self.root / "skills/shared/project-context/SKILL.md").unlink()
        result = subprocess.run(command, text=True, capture_output=True, env=env, check=False)
        self.assertEqual(result.returncode, 1)
        self.assertIn("BLOCKED:", result.stderr)
        self.assertEqual(snapshot(), original)

    def test_cli_malformed_manifest_fails_without_traceback(self):
        (self.root / "manifest.yaml").write_text("schema_version: 2\n", encoding="utf-8")
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            code = validator.main(["--root", str(self.root)])
        self.assertEqual(code, 1)
        self.assertIn("BLOCKED:", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
