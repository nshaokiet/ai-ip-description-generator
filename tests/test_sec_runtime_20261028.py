"""Offline regression checks for SEC-RUNTIME-20261028."""
import json
from pathlib import Path
import re
import ssl
import unittest

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ">=24.22.1 <25"


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class RuntimeSecurityTests(unittest.TestCase):
    def test_both_ci_node_installations_are_pinned(self):
        workflow = read(".github/workflows/ci.yml")
        self.assertEqual(workflow.count("uses: actions/setup-node@v7"), 2)
        self.assertEqual(workflow.count('node-version: "24.22.1"'), 2)
        self.assertNotIn('node-version: "24.18.0"', workflow)
        # Required security evidence remains mandatory and blocking.
        self.assertRegex(workflow, r"(?s)name: Archive DEP-001 security evidence.*?if-no-files-found: error")

    def test_render_frontend_pin_is_scoped_and_preserves_triggers(self):
        blueprint = read("render.yaml")
        frontend, backend = blueprint.split("  - type: web", 2)[1:]
        self.assertIn("name: ai-ip-synthetic-demo-frontend", frontend)
        self.assertIn('key: NODE_VERSION\n        value: "24.22.1"', frontend)
        self.assertNotIn("key: NODE_VERSION", backend)
        self.assertEqual(blueprint.count("autoDeployTrigger: checksPass"), 2)

    def test_engine_and_lockfile_metadata_agree(self):
        frontend = json.loads(read("frontend/package.json"))
        front_lock = json.loads(read("frontend/package-lock.json"))
        adapter = json.loads(read("frontend/tools/next-root-glob-adapter/package.json"))
        mcp = json.loads(read("tools/project-orchestrator-mcp/package.json"))
        mcp_lock = json.loads(read("tools/project-orchestrator-mcp/package-lock.json"))
        for value in (frontend["engines"]["node"], front_lock["packages"][""]["engines"]["node"],
                      adapter["engines"]["node"], front_lock["packages"]["node_modules/fast-glob"]["engines"]["node"],
                      mcp["engines"]["node"], mcp_lock["packages"][""]["engines"]["node"]):
            self.assertEqual(value, ENGINE)

    def test_certifi_requirement_is_exact_and_unique(self):
        lines = read("backend/requirements.txt").splitlines()
        self.assertEqual([x for x in lines if re.match(r"(?i)^certifi\s*[<=>]", x)], ["certifi==2026.10.19"])

    def test_default_tls_context_requires_trust_and_hostname(self):
        context = ssl.create_default_context()
        self.assertEqual(context.verify_mode, ssl.CERT_REQUIRED)
        self.assertTrue(context.check_hostname)

    def test_blueprint_and_workflow_do_not_disable_tls(self):
        for path in ("render.yaml", ".github/workflows/ci.yml"):
            text = read(path)
            self.assertNotRegex(text, r"(?i)NODE_TLS_REJECT_UNAUTHORIZED\s*[:=]\s*[\"']?0")
            self.assertNotRegex(text, r"(?i)PYTHONHTTPSVERIFY\s*[:=]\s*[\"']?0")

    def test_patched_installed_certifi_bundle(self):
        import certifi
        self.assertGreaterEqual(tuple(map(int, certifi.__version__.split("."))), (2026, 10, 19))
        context = ssl.create_default_context(cafile=certifi.where())
        self.assertEqual(context.verify_mode, ssl.CERT_REQUIRED)
        self.assertTrue(context.check_hostname)


if __name__ == "__main__":
    unittest.main()
