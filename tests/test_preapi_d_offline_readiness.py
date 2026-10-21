"""PREAPI-D static preflight regression; no provider execution."""

import json
import socket
from unittest.mock import patch

from tools import preapi_d_offline_readiness as readiness


def test_default_offline_report_and_no_client_or_transport():
    with patch("openai.OpenAI", side_effect=AssertionError("client constructed")) as client:
        with patch.object(socket.socket, "connect", side_effect=AssertionError("network")) as network:
            report = readiness.inspect_offline({})
    client.assert_not_called()
    network.assert_not_called()
    assert report["mode"] == "OFFLINE_ONLY"
    assert report["credential_status"] == "ABSENT"
    assert report["provider_execution"] == "NOT_RUN"
    assert report["model_entitlement"] == "UNVERIFIED"
    assert report["product_runtime"] == "NOT_DETERMINED"
    assert report["provider_budget_usd"] == 0
    assert report["future_live_budget_enforcement"] == "NOT_IMPLEMENTED"


def test_credential_presence_is_non_disclosing():
    marker = "secret-canary-do-not-print-123456"
    report = readiness.inspect_offline({"OPENAI_API_KEY": marker})
    assert report["credential_status"] == "PRESENT"
    assert marker not in json.dumps(report)
    assert marker[:8] not in json.dumps(report)
    assert readiness.inspect_offline({"OPENAI_API_KEY": "   "})["credential_status"] == "ABSENT"


def test_invalid_timeout_and_token_limit_block():
    for field, value in (("OPENAI_TIMEOUT_SECONDS", "29"),
                         ("OPENAI_DRAFT_TIMEOUT_SECONDS", "601"),
                         ("OPENAI_MAX_OUTPUT_TOKENS", "48001"),
                         ("OPENAI_DRAFT_MAX_OUTPUT_TOKENS", "not-a-number")):
        report = readiness.inspect_offline({field: value})
        assert report["checks"]["timeouts_and_token_caps"] == "BLOCKED"
        assert report["readiness"] == "BLOCKED"


def test_live_flags_block_and_report_is_deterministic():
    environment = {"RUN_OPENAI_LIVE_TESTS": "1"}
    report = readiness.inspect_offline(environment)
    assert report["checks"]["live_flags_off"] == "BLOCKED"
    assert report == readiness.inspect_offline(environment)
    assert readiness.inspect_offline({"RUN_OPENAI_DRAFT_LIVE_TESTS": "1"})["readiness"] == "BLOCKED"


def test_missing_prompt_and_invalid_schema_block(tmp_path, monkeypatch):
    monkeypatch.setattr(readiness, "CANONICAL_PROMPT_PATH", tmp_path / "missing.md")
    assert readiness.inspect_offline({})["checks"]["extraction_prompt"] == "BLOCKED"
    bad_schema = tmp_path / "bad.json"
    bad_schema.write_text('{"type": "not-a-json-schema-type"}', encoding="utf-8")
    monkeypatch.setattr(readiness, "DRAFT_SCHEMA_PATH", bad_schema)
    assert readiness.inspect_offline({})["checks"]["draft_schema"] == "BLOCKED"


def test_invalid_model_and_retry_policy_block(monkeypatch):
    monkeypatch.setattr(readiness, "OPENAI_EXTRACTION_MODEL", "bad model with spaces")
    monkeypatch.setattr(readiness, "OPENAI_MAX_RETRIES", 3)
    checks = readiness.inspect_offline({})["checks"]
    assert checks["model_identifier_syntax"] == "BLOCKED"
    assert checks["retry_ceiling"] == "BLOCKED"


def test_sdk_pin_mismatch_blocks(monkeypatch):
    monkeypatch.setattr(readiness.importlib.metadata, "version", lambda _name: "0.0.0")
    report = readiness.inspect_offline({})
    assert report["checks"]["sdk_pin"] == "BLOCKED"
    assert report["readiness"] == "BLOCKED"
