"""AI-CONV-004 Candidate A acceptance tests (AC-01 through AC-29)."""

from __future__ import annotations

import asyncio
import base64
import inspect
import json
import re
import socket
import urllib.request
from dataclasses import replace
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backend.app.api.local_synthetic_v2 import (
    CAPABILITY_TTL_SECONDS,
    DEFAULT_LIMIT,
    MAX_SESSIONS,
    SESSION_TTL_SECONDS,
    SyntheticEvidenceItem,
    SyntheticV2LifecycleError,
    TrustedSyntheticV2Runtime,
    create_local_synthetic_v2_app,
)
from backend.app.core.config import Settings
from backend.app.main import create_app
from backend.app.services.uspto_document_package_validation import validate_assembly_inputs
from backend.app.services.uspto_offline_orchestration import (
    PROVENANCE_KEYS,
    OfflineUSPTOOrchestrator,
)


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests/fixtures/invention-reconstruction/v1.0.0/representative-system.json"
HOST = "127.0.0.1"
PORT = 8765
BASE_URL = f"http://{HOST}:{PORT}"


class Clock:
    def __init__(self, value: float = 1000.0) -> None:
        self.value = value

    def __call__(self) -> float:
        return self.value


def orchestration_inputs() -> dict:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    p3_config = {"source_document_synthetic": True}
    p4_config = {
        "language": "en",
        "target_jurisdiction": "US",
        "requested_claim_types": ["SYSTEM", "METHOD", "COMPOSITION"],
        "max_dependent_claims_per_family": 4,
        "source_document_synthetic": True,
        "selected_solution_id": "IR-SOL-0001",
        "p2_003_generation_config": dict(p3_config),
    }
    return {
        "source_envelope": fixture["source_envelope"],
        "structured_analysis": fixture["structured_analysis"],
        "p2_003_generation_config": p3_config,
        "p2_004_generation_config": p4_config,
    }


@pytest.fixture(scope="module")
def completed_session():
    orchestrator = OfflineUSPTOOrchestrator(
        session_id_factory=lambda: "synthetic-session-a"
    )
    status = orchestrator.run_uspto_v2_offline_pipeline(**orchestration_inputs())
    return orchestrator, status


def evidence_items(count: int = 60) -> tuple[SyntheticEvidenceItem, ...]:
    return tuple(
        SyntheticEvidenceItem(
            evidence_id=f"synthetic-evidence-{index:03d}",
            digest=f"synthetic-vetted-digest-{index:03d}",
        )
        for index in range(count, 0, -1)
    )


def make_context(completed_session, *, count: int = 60):
    orchestrator, status = completed_session
    clock = Clock()
    runtime = TrustedSyntheticV2Runtime(monotonic=clock)
    token = runtime.issue_capability(
        orchestrator, status.session_id, evidence=evidence_items(count)
    )
    settings = Settings(
        storage_root=ROOT / ".tmp-unused-v2",
        enable_local_synthetic_v2_api=True,
    )
    app = create_local_synthetic_v2_app(settings, runtime=runtime, host=HOST, port=PORT)
    client = TestClient(app, base_url=BASE_URL, client=(HOST, 51000))
    headers = {"Authorization": f"Bearer {token}"}
    return orchestrator, status, clock, runtime, token, client, headers


def assert_error(response, status: int, code: str) -> None:
    assert response.status_code == status, response.text
    payload = response.json()
    assert set(payload) == {"code", "message", "correlation_id"}
    assert payload["code"] == code
    assert re.fullmatch(r"[A-Za-z0-9_-]{1,64}", payload["correlation_id"])


def run_raw(app, *, method="GET", path, headers, query=b"", client=(HOST, 51000)):
    messages = []
    received = False

    async def receive():
        nonlocal received
        if not received:
            received = True
            return {"type": "http.request", "body": b"", "more_body": False}
        return {"type": "http.disconnect"}

    async def send(message):
        messages.append(message)

    scope = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": method,
        "scheme": "http",
        "path": path,
        "raw_path": path.encode("ascii", "ignore"),
        "query_string": query,
        "headers": headers,
        "client": client,
        "server": (HOST, PORT),
    }
    asyncio.run(app(scope, receive, send))
    start = next(message for message in messages if message["type"] == "http.response.start")
    body = b"".join(
        message.get("body", b"")
        for message in messages
        if message["type"] == "http.response.body"
    )
    return start["status"], json.loads(body)


def test_ac_01_v1_inventory_and_default_app_never_registers_v2(tmp_path):
    app = create_app(Settings(storage_root=tmp_path))
    paths = set(app.openapi()["paths"])
    assert paths == {"/health", "/api/documents"}
    assert not any(path.startswith("/api/v2") for path in paths)
    with TestClient(app) as client:
        assert client.get("/api/v2/sessions/x/status").status_code == 404


def test_ac_02_versioned_strict_status_and_unknown_input_rejected(completed_session):
    *_, client, headers = make_context(completed_session)
    session_id = completed_session[1].session_id
    response = client.get(f"/api/v2/sessions/{session_id}/status", headers=headers)
    assert response.status_code == 200
    assert set(response.json()) == {
        "api_version",
        "session_id",
        "revision",
        "stage",
        "claims_status",
        "claims_count",
        "review_required",
        "product_claims_runtime_enabled",
    }
    assert response.json()["api_version"] == "2.0.0"
    assert_error(
        client.get(f"/api/v2/sessions/{session_id}/status?extra=x", headers=headers),
        422,
        "invalid_request",
    )


def test_ac_03_exact_session_revision_and_capability_scope(completed_session):
    *_, client, headers = make_context(completed_session)
    response = client.get(
        "/api/v2/sessions/another-session/revisions/1/evidence-index", headers=headers
    )
    assert_error(response, 404, "session_unavailable")
    response = client.get(
        "/api/v2/sessions/synthetic-session-a/revisions/2/evidence-index", headers=headers
    )
    assert_error(response, 409, "stale_revision")


def test_ac_04_evidence_bootstrap_rejects_foreign_or_raw_source_identity(completed_session):
    orchestrator, status = completed_session
    runtime = TrustedSyntheticV2Runtime()
    with pytest.raises(SyntheticV2LifecycleError) as captured:
        runtime.issue_capability(
            orchestrator,
            status.session_id,
            evidence=(SyntheticEvidenceItem("safe-id", status.source_sha256),),
        )
    assert captured.value.code == "INVALID_SYNTHETIC_EVIDENCE"
    with pytest.raises(SyntheticV2LifecycleError):
        runtime.issue_capability(
            orchestrator,
            status.session_id,
            evidence=(
                SyntheticEvidenceItem("duplicate", "synthetic-a"),
                SyntheticEvidenceItem("duplicate", "synthetic-b"),
            ),
        )


def test_ac_05_zero_claims_review_required_is_success(completed_session):
    *_, client, headers = make_context(completed_session)
    payload = client.get(
        "/api/v2/sessions/synthetic-session-a/status", headers=headers
    ).json()
    assert payload["claims_status"] == "HUMAN_CONFIRMATION_REQUIRED"
    assert payload["claims_count"] == 0
    assert payload["review_required"] is True
    assert payload["product_claims_runtime_enabled"] is False
    assert "claims" not in payload


def test_ac_06_human_review_remains_fail_closed_and_read_only(completed_session):
    *_, client, headers = make_context(completed_session)
    for method, path in (
        ("POST", "/api/v2/sessions/synthetic-session-a/review"),
        ("PATCH", "/api/v2/sessions/synthetic-session-a/status"),
        ("POST", "/api/v2/sessions/synthetic-session-a/status?confirmed=true"),
    ):
        assert client.request(method, path, headers=headers).status_code == 404


def test_ac_07_disabled_claim_types_cannot_be_enabled_by_request(completed_session):
    *_, client, headers = make_context(completed_session)
    response = client.get(
        "/api/v2/sessions/synthetic-session-a/status?claim_type=METHOD", headers=headers
    )
    assert_error(response, 422, "invalid_request")
    for path in ("/claims", "/method-claims", "/composition-claims"):
        assert client.get(f"/api/v2/sessions/synthetic-session-a{path}", headers=headers).status_code == 404


def test_ac_08_exact_seven_input_projector_is_unchanged():
    assert PROVENANCE_KEYS == (
        "source_envelope",
        "structured_analysis",
        "reconstruction",
        "specification",
        "p2_003_generation_config",
        "supported_claims",
        "p2_004_generation_config",
    )
    assert tuple(inspect.signature(validate_assembly_inputs).parameters) == PROVENANCE_KEYS


def test_ac_09_errors_and_state_do_not_leak_source_or_token(completed_session, caplog):
    _, status, _, runtime, token, client, _ = make_context(completed_session)
    response = client.get(
        "/api/v2/sessions/synthetic-session-a/status",
        headers={"Authorization": "Bearer " + "A" * 43},
    )
    assert_error(response, 404, "session_unavailable")
    serialized = response.text + repr(runtime._sessions) + repr(runtime._capabilities) + caplog.text
    assert token not in serialized
    assert status.source_sha256 not in response.text
    assert status.document_id not in response.text
    assert str(ROOT) not in response.text


def test_ac_10_existing_v1_routes_and_feature_gate_are_unchanged(tmp_path):
    default = create_app(Settings(storage_root=tmp_path / "default"))
    enabled = create_app(
        Settings(storage_root=tmp_path / "enabled", enable_local_orchestration_api=True),
        extraction_runtime=object(),
        draft_runtime=object(),
        docx_renderer=object(),
    )
    assert set(default.openapi()["paths"]) == {"/health", "/api/documents"}
    assert set(enabled.openapi()["paths"]) == {
        "/health",
        "/api/documents",
        "/api/documents/{document_id}",
        "/api/documents/{document_id}/process",
        "/api/drafts/validate",
        "/api/exports/docx",
    }


def test_ac_11_get_does_not_call_network_provider_or_renderer(completed_session, monkeypatch):
    orchestrator, _, _, _, _, client, headers = make_context(completed_session)
    monkeypatch.setattr(socket, "create_connection", lambda *a, **k: pytest.fail("network"))
    monkeypatch.setattr(urllib.request, "urlopen", lambda *a, **k: pytest.fail("network"))
    monkeypatch.setattr(orchestrator, "get_session_status", lambda *a, **k: pytest.fail("pipeline"))
    monkeypatch.setattr(orchestrator, "get_validated_package", lambda *a, **k: pytest.fail("package"))
    assert client.get(
        "/api/v2/sessions/synthetic-session-a/status", headers=headers
    ).status_code == 200


def test_ac_12_dedicated_flag_cannot_activate_released_app(tmp_path, monkeypatch):
    settings = Settings(
        storage_root=tmp_path,
        enable_local_synthetic_v2_api=True,
    )
    released = create_app(settings)
    assert not any(path.startswith("/api/v2") for path in released.openapi()["paths"])
    monkeypatch.setenv("AI_IP_ENABLE_LOCAL_SYNTHETIC_V2_API", "1")
    assert Settings.from_environment().enable_local_synthetic_v2_api is True
    assert not any(
        path.startswith("/api/v2")
        for path in create_app(Settings.from_environment()).openapi()["paths"]
    )
    with pytest.raises(ValueError, match="trusted in-process runtime required"):
        create_local_synthetic_v2_app(settings)


def test_ac_13_off_host_origin_forwarded_and_peer_guards(completed_session, tmp_path):
    off = create_local_synthetic_v2_app(Settings(storage_root=tmp_path))
    with TestClient(off, base_url=BASE_URL, client=(HOST, 51000)) as client:
        response = client.get("/api/v2/sessions/synthetic-session-a/status")
    assert response.status_code == 404
    assert response.text == "Not Found"

    *_, client, headers = make_context(completed_session)
    assert_error(
        client.get(
            "/api/v2/sessions/synthetic-session-a/status",
            headers={**headers, "Host": "localhost:8765"},
        ),
        404,
        "session_unavailable",
    )
    for name in (
        "Origin",
        "Forwarded",
        "X-Forwarded-For",
        "X-Real-IP",
        "CF-Connecting-IP",
        "True-Client-IP",
    ):
        assert_error(
            client.get(
                "/api/v2/sessions/synthetic-session-a/status",
                headers={**headers, name: "http://127.0.0.1"},
            ),
            404,
            "session_unavailable",
        )
    _, _, _, runtime, _, _, _ = make_context(completed_session)
    app = create_local_synthetic_v2_app(
        Settings(storage_root=tmp_path, enable_local_synthetic_v2_api=True),
        runtime=runtime,
        host=HOST,
        port=PORT,
    )
    status, body = run_raw(
        app,
        path="/api/v2/sessions/synthetic-session-a/status",
        headers=[(b"host", f"{HOST}:{PORT}".encode()), (b"authorization", b"Bearer " + b"A" * 43)],
        client=("10.0.0.2", 51000),
    )
    assert status == 404 and body["code"] == "session_unavailable"


def test_ac_14_capability_absent_malformed_expired_and_cross_session(completed_session):
    _, _, clock, _, token, client, _ = make_context(completed_session)
    path = "/api/v2/sessions/synthetic-session-a/status"
    for headers in ({}, {"Authorization": "Basic no"}, {"Authorization": "Bearer short"}):
        assert_error(client.get(path, headers=headers), 404, "session_unavailable")
    assert_error(
        client.get(path, headers={"Authorization": "Bearer " + "B" * 43}),
        404,
        "session_unavailable",
    )
    clock.value += CAPABILITY_TTL_SECONDS
    assert_error(
        client.get(path, headers={"Authorization": f"Bearer {token}"}),
        404,
        "session_unavailable",
    )


def test_ac_15_bounded_deterministic_evidence_without_total_or_source(completed_session):
    _, status, _, _, token, client, headers = make_context(completed_session)
    first = client.get(
        "/api/v2/sessions/synthetic-session-a/revisions/1/evidence-index", headers=headers
    )
    assert first.status_code == 200
    payload = first.json()
    assert set(payload) == {"api_version", "session_id", "revision", "items", "next_cursor"}
    assert len(payload["items"]) == DEFAULT_LIMIT
    assert payload["items"] == sorted(payload["items"], key=lambda item: item["evidence_id"])
    assert all(set(item) == {"evidence_id", "digest"} for item in payload["items"])
    serialized = first.text
    assert "total" not in serialized
    assert status.source_sha256 not in serialized
    assert status.document_id not in serialized
    assert token not in serialized


def test_ac_16_get_is_state_immutable_and_cursor_is_stateless(completed_session):
    _, _, _, runtime, _, client, headers = make_context(completed_session)
    before_sessions = repr(runtime._sessions)
    before_capabilities = repr(runtime._capabilities)
    first = client.get(
        "/api/v2/sessions/synthetic-session-a/revisions/1/evidence-index?limit=10",
        headers=headers,
    ).json()
    client.get(
        "/api/v2/sessions/synthetic-session-a/revisions/1/evidence-index",
        params={"limit": "10", "cursor": first["next_cursor"]},
        headers=headers,
    )
    assert repr(runtime._sessions) == before_sessions
    assert repr(runtime._capabilities) == before_capabilities


def test_ac_17_exactly_two_get_routes_are_reachable(completed_session):
    *_, client, headers = make_context(completed_session)
    assert client.get("/api/v2/sessions/synthetic-session-a/status", headers=headers).status_code == 200
    assert client.get(
        "/api/v2/sessions/synthetic-session-a/revisions/1/evidence-index", headers=headers
    ).status_code == 200
    for path in (
        "/api/v2/sessions/synthetic-session-a/package-status",
        "/api/v2/sessions/synthetic-session-a/export",
        "/api/v2/sessions/synthetic-session-a/capabilities",
        "/api/v2/sessions",
    ):
        assert client.get(path, headers=headers).status_code == 404
    unknown = client.get(
        "/api/v2/sessions/synthetic-session-a/not-a-route",
        headers={**headers, "X-API-Version": "9"},
    )
    assert unknown.status_code == 404
    assert unknown.json() == {"detail": "Not Found"}


def test_ac_18_no_http_bootstrap_or_secret_transport(completed_session):
    *_, token, client, headers = make_context(completed_session)[1:]
    for path in (
        "/api/v2/capabilities",
        "/api/v2/sessions/synthetic-session-a/capabilities",
        f"/api/v2/sessions/synthetic-session-a/status?token={token}",
    ):
        response = client.get(path, headers=headers if "token=" not in path else {})
        assert response.status_code == 404
        assert token not in response.text
    assert_error(
        client.get(
            "/api/v2/sessions/synthetic-session-a/status",
            headers={**headers, "Cookie": f"capability={token}"},
        ),
        422,
        "invalid_request",
    )


def test_ac_19_absolute_ttls_capacity_and_no_get_eviction(completed_session):
    orchestrator, status, clock, runtime, token, client, headers = make_context(completed_session)
    assert CAPABILITY_TTL_SECONDS == 900 and SESSION_TTL_SECONDS == 3600 and MAX_SESSIONS == 50
    clock.value += CAPABILITY_TTL_SECONDS - 0.001
    assert client.get(f"/api/v2/sessions/{status.session_id}/status", headers=headers).status_code == 200
    clock.value += 0.001
    assert_error(
        client.get(f"/api/v2/sessions/{status.session_id}/status", headers=headers),
        404,
        "session_unavailable",
    )
    assert status.session_id in runtime._sessions
    snapshot = runtime._sessions[status.session_id]
    runtime._sessions.clear()
    runtime._capabilities.clear()
    runtime._sessions.update(
        {f"synthetic-fill-{index}": replace(snapshot, session_id=f"synthetic-fill-{index}") for index in range(MAX_SESSIONS)}
    )
    with pytest.raises(SyntheticV2LifecycleError) as captured:
        runtime.issue_capability(orchestrator, status.session_id, evidence=evidence_items(1))
    assert captured.value.code == "SESSION_CAPACITY_EXCEEDED"
    assert token not in repr(runtime._capabilities)


@pytest.mark.parametrize("limit", ["0", "00", "01", "51", "1.0", "1e1", " 1", "999999999"])
def test_ac_20_pagination_bounds_duplicate_and_cursor_tamper(completed_session, limit):
    *_, client, headers = make_context(completed_session)
    base = "/api/v2/sessions/synthetic-session-a/revisions/1/evidence-index"
    assert_error(client.get(base, params={"limit": limit}, headers=headers), 422, "invalid_request")
    assert_error(
        client.get(base, params=[("limit", "1"), ("limit", "2")], headers=headers),
        422,
        "invalid_request",
    )
    cursor = client.get(base, params={"limit": "10"}, headers=headers).json()["next_cursor"]
    tampered = ("A" if cursor[0] != "A" else "B") + cursor[1:]
    assert_error(
        client.get(base, params={"limit": "10", "cursor": tampered}, headers=headers),
        422,
        "invalid_request",
    )
    assert_error(
        client.get(base, params={"limit": "11", "cursor": cursor}, headers=headers),
        422,
        "invalid_request",
    )


def test_ac_21_auth_precedes_typed_path_and_query_validation(completed_session):
    *_, client, _ = make_context(completed_session)
    absent = {"Authorization": "Bearer " + "Z" * 43}
    paths = (
        "/api/v2/sessions/synthetic-session-a/revisions/00/evidence-index?limit=bad",
        "/api/v2/sessions/synthetic-session-a/revisions/2147483648/evidence-index?version=9",
        "/api/v2/sessions/other/revisions/2/evidence-index",
    )
    for path in paths:
        response = client.get(path, headers=absent)
        assert_error(response, 404, "session_unavailable")


def test_ac_22_exact_allowlisted_success_and_error_shapes(completed_session):
    *_, client, headers = make_context(completed_session)
    status = client.get("/api/v2/sessions/synthetic-session-a/status", headers=headers).json()
    evidence = client.get(
        "/api/v2/sessions/synthetic-session-a/revisions/1/evidence-index?limit=1",
        headers=headers,
    ).json()
    assert len(status) == 8
    assert len(evidence) == 5
    assert len(evidence["items"][0]) == 2
    error = client.get(
        "/api/v2/sessions/synthetic-session-a/status?bad=1", headers=headers
    )
    assert_error(error, 422, "invalid_request")
    for forbidden in ("source_identity", "filename", "revision_token", "seal", "claim_text"):
        assert forbidden not in json.dumps([status, evidence, error.json()])


def test_ac_23_no_client_version_negotiation_or_unsupported_code(completed_session):
    *_, client, headers = make_context(completed_session)
    path = "/api/v2/sessions/synthetic-session-a/status"
    for mutated in (
        client.get(path + "?version=2.0.0", headers=headers),
        client.get(path, headers={**headers, "X-API-Version": "2.0.0"}),
        client.get(path, headers={**headers, "Accept-Version": "2.0.0"}),
    ):
        assert_error(mutated, 422, "invalid_request")
        assert "unsupported_api_version" not in mutated.text
    preauth = client.get(path + "?version=2.0.0")
    assert_error(preauth, 404, "session_unavailable")


def test_ac_24_bearer_is_32_random_bytes_canonical_and_header_only(completed_session):
    orchestrator, status = completed_session
    runtime = TrustedSyntheticV2Runtime()
    first = runtime.issue_capability(orchestrator, status.session_id, evidence=evidence_items(1))
    second = runtime.issue_capability(orchestrator, status.session_id, evidence=evidence_items(1))
    assert first != second
    assert re.fullmatch(r"[A-Za-z0-9_-]{43}", second)
    assert len(base64.urlsafe_b64decode(second + "=")) == 32
    assert runtime.authenticate(first) is None
    assert runtime.authenticate(second) is not None


def test_ac_25_ephemeral_distinct_keys_hmac_restart_and_revocation(completed_session, monkeypatch):
    orchestrator, status = completed_session
    runtime = TrustedSyntheticV2Runtime()
    assert len(runtime._verifier_key) == len(runtime._cursor_key) == 32
    assert runtime._verifier_key != runtime._cursor_key
    token = runtime.issue_capability(orchestrator, status.session_id, evidence=evidence_items(1))
    assert token not in repr(runtime._capabilities)
    assert TrustedSyntheticV2Runtime().authenticate(token) is None
    calls = 0
    original = __import__("hmac").compare_digest

    def counted(left, right):
        nonlocal calls
        calls += 1
        return original(left, right)

    monkeypatch.setattr("backend.app.api.local_synthetic_v2.hmac.compare_digest", counted)
    assert runtime.authenticate(token) is not None
    assert calls >= 1
    runtime.revoke_session(status.session_id)
    assert runtime.authenticate(token) is None


def test_ac_26_duplicate_headers_options_and_dns_rebinding_fail_closed(completed_session):
    _, _, _, runtime, token, _, _ = make_context(completed_session)
    app = create_local_synthetic_v2_app(
        Settings(storage_root=ROOT / ".tmp-unused", enable_local_synthetic_v2_api=True),
        runtime=runtime,
        host=HOST,
        port=PORT,
    )
    path = "/api/v2/sessions/synthetic-session-a/status"
    auth = f"Bearer {token}".encode()
    for headers in (
        [(b"host", b"127.0.0.1:8765"), (b"host", b"localhost:8765"), (b"authorization", auth)],
        [(b"host", b"127.0.0.1:8765"), (b"authorization", auth), (b"authorization", auth)],
    ):
        status, body = run_raw(app, path=path, headers=headers)
        assert status == 404 and body["code"] == "session_unavailable"
    status, body = run_raw(
        app,
        method="OPTIONS",
        path=path,
        headers=[(b"host", b"127.0.0.1:8765"), (b"authorization", auth)],
    )
    assert status == 404 and body == {"detail": "Not Found"}


def test_ac_27_strict_path_query_grammar_and_no_authority_promotion(completed_session):
    *_, client, headers = make_context(completed_session)
    for path in (
        "/api/v2/sessions/bad.id/status",
        "/api/v2/sessions/synthetic-session-a/revisions/01/evidence-index",
        "/api/v2/sessions/synthetic-session-a/revisions/0/evidence-index",
        "/api/v2/sessions/synthetic-session-a/revisions/2147483648/evidence-index",
    ):
        response = client.get(path, headers=headers)
        assert response.status_code in {404, 422}
    response = client.get(
        "/api/v2/sessions/synthetic-session-a/status?essentiality=ESSENTIAL",
        headers=headers,
    )
    assert_error(response, 422, "invalid_request")


def test_ac_28_cursor_has_integrity_not_secrecy_and_bearer_stays_independent(completed_session):
    _, status, _, _, token, client, headers = make_context(completed_session)
    base = "/api/v2/sessions/synthetic-session-a/revisions/1/evidence-index"
    cursor = client.get(base, params={"limit": "10"}, headers=headers).json()["next_cursor"]
    raw = base64.urlsafe_b64decode(cursor[:-43] + "=" * ((4 - len(cursor[:-43]) % 4) % 4))
    decoded = raw.decode("ascii")
    payload = json.loads(decoded)
    assert set(payload) == {"v", "pos", "snap", "rev", "lim", "scope", "exp"}
    for forbidden in (token, status.document_id, status.source_sha256, "synthetic-evidence"):
        assert forbidden not in decoded
    response = client.get(base, params={"limit": "10", "cursor": cursor})
    assert_error(response, 404, "session_unavailable")


def test_ac_29_monotonic_boundary_and_cleanup_only_by_trusted_lifecycle(completed_session):
    orchestrator, status, clock, runtime, _, client, headers = make_context(completed_session)
    clock.value += CAPABILITY_TTL_SECONDS
    response = client.get(f"/api/v2/sessions/{status.session_id}/status", headers=headers)
    assert_error(response, 404, "session_unavailable")
    assert status.session_id in runtime._sessions
    assert runtime.retire_expired() == 0
    clock.value += SESSION_TTL_SECONDS - CAPABILITY_TTL_SECONDS
    assert status.session_id in runtime._sessions
    assert runtime.retire_expired() == 1
    assert status.session_id not in runtime._sessions
    with pytest.raises(SyntheticV2LifecycleError) as captured:
        runtime.issue_capability(orchestrator, status.session_id, evidence=evidence_items(1))
    assert captured.value.code == "SESSION_EXPIRED"


def test_internal_failure_is_sanitized(completed_session, monkeypatch):
    *_, runtime, _, client, headers = make_context(completed_session)[2:]

    def explode(_snapshot):
        raise RuntimeError(f"sensitive path {ROOT}")

    monkeypatch.setattr(runtime, "status_payload", explode)
    response = client.get("/api/v2/sessions/synthetic-session-a/status", headers=headers)
    assert_error(response, 500, "internal_error")
    assert str(ROOT) not in response.text
