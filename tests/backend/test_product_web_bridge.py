"""S2-A native S1 authentication + two source-bound workflows; no provider calls."""
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import threading
import time
from types import SimpleNamespace

from fastapi.testclient import TestClient
import pytest

from backend.app.local_product_web import LOGIN, PREFIX, Sessions, create_local_app
from backend.app.main import create_app
from backend.app.services import preapi_source_custody as custody
from backend.app.services.document_validation import DocumentValidator
from backend.app.services.product_synthetic_workflow import OfflineSyntheticWorkflow
from backend.app.services.product_web_bridge import ARTIFACT_LIMIT, PINS
from backend.app.services.product_web_host_control import PairingControl, create_private_dir, restrict_owned
from backend.app.services.product_web_synthetic_runtime import PinnedSyntheticRuntime, ROOT
from backend.app.services.uspto_offline_renderer import FILES
from tests.e2e.provider_tripwire import ProviderTripwire

BASE = PREFIX + "/documents"
ENTRIES = json.loads((ROOT / "tests/fixtures/api-ready/v1.0.0/manifest.json").read_bytes())["fixtures"]


@pytest.fixture
def host(tmp_path):
    restrict_owned(tmp_path)
    root = create_private_dir(tmp_path / "host")
    clock = [1000.0]
    sessions = Sessions(clock=lambda: clock[0])
    control = PairingControl(root, sessions.approve, sessions.revoke_all).start()
    wire = ProviderTripwire().install()
    app = create_local_app(enabled=True, sessions=sessions, control=control,
        proxy_secret="a" * 64, backend_port=8765, synthetic_enabled=True, state_root=root)
    def client():
        return TestClient(app, base_url="https://127.0.0.1:8765", client=("127.0.0.1", 1234))
    headers = {"Origin": "https://localhost:3443", "Sec-Fetch-Site": "same-origin",
               "X-AIIP-Proxy": "a" * 64, "Content-Type": "application/json"}
    def login(http):
        pending = http.post(PREFIX + "/session/bootstrap", content="{}",
                            headers={**headers, "X-AIIP-Bootstrap": "1"}).json()
        assert sessions.approve(pending["selector"])
        response = http.post(PREFIX + "/session", content="{}",
                            headers={**headers, "X-AIIP-CSRF": pending["csrf"]})
        assert response.status_code == 200
        return {**headers, "X-AIIP-CSRF": response.json()["csrf"]}
    with client() as http:
        h = login(http)
        value = SimpleNamespace(http=http, headers=h, client=client, login=login, app=app,
            sessions=sessions, clock=clock, bridge=app.state.synthetic_bridge, wire=wire, root=root)
        try:
            yield value
        finally:
            sessions.close()
            app.state.synthetic_bridge.close()
            control.stop()
            wire.assert_no_unexpected_activity()
            assert wire.snapshot() == {"provider_api_requests": 0, "unexpected_provider_client_attempts": 0,
                "unexpected_egress_attempts": 0, "negative_tripwire_blocked_attempts": 0}
            wire.close()


def upload(host, index=0, *, client=None, headers=None, content=None, filename=None, mime=None):
    entry = ENTRIES[index]
    return (client or host.http).post(BASE, content=(ROOT / entry["path"]).read_bytes() if content is None else content,
        headers={**(headers or host.headers), "Content-Type": mime or entry["media_type"],
                 "X-AIIP-Filename": filename or entry["filename"]})


def begin(host, index=0, **kwargs):
    result = upload(host, index, **kwargs)
    assert result.status_code == 201, result.text
    return result.json()["document"]


def review(host, document):
    result = host.http.get(f"{BASE}/{document}/review", headers=host.headers)
    assert result.status_code == 200, result.text
    return result.json()


def decision(host, document, view, action):
    return host.http.post(f"{BASE}/{document}/{action}", headers=host.headers,
        json={"revision": view["revision"], "view_id": view["view_id"],
              **({} if action == "render" else {"acknowledge": True})})


def rendered(host, index=0):
    doc = begin(host, index)
    view = review(host, doc)
    assert decision(host, doc, view, "ack-content").status_code == 200
    assert decision(host, doc, view, "ack-claims").status_code == 200
    response = decision(host, doc, view, "render")
    assert response.status_code == 200, response.text
    return doc, view, response.json()


@pytest.mark.parametrize("index", [0, 1])
def test_two_sources_complete_seven_originals_and_four_verified_downloads(host, index):
    doc, view, export = rendered(host, index)
    assert set(view["originals"]) == {"source_envelope", "structured_analysis", "reconstruction", "specification",
        "p2_003_generation_config", "supported_claims", "p2_004_generation_config"}
    claims = view["originals"]["supported_claims"]
    assert claims["status"] == "HUMAN_CONFIRMATION_REQUIRED" and claims["claims"] == []
    entry = ENTRIES[index]
    source = view["originals"]["source_envelope"]
    assert source["document_metadata"]["sha256"] == entry["sha256"]
    assert hashlib.sha256(source["source_units"][0]["content"].encode()).hexdigest() == entry["parsed_content_sha256"]
    assert view["originals"]["structured_analysis"]["document_metadata"] == source["document_metadata"]
    for forbidden in ("revision_token", "custody_id", "coordinator_instance_id", '"token"'):
        assert forbidden not in json.dumps(view)
    assert next(iter(host.bridge.documents.values())).owner not in json.dumps(view)
    assert [a["filename"] for a in export["artifacts"]] == list(FILES)
    for artifact in export["artifacts"]:
        response = host.http.get(f'{BASE}/{doc}/revisions/1/artifacts/{artifact["filename"]}', headers=host.headers)
        assert response.status_code == 200
        assert response.headers["content-type"] == artifact["media_type"]
        assert response.headers["cache-control"] == "no-store"
        assert len(response.content) == artifact["size_bytes"] <= ARTIFACT_LIMIT
        assert hashlib.sha256(response.content).hexdigest() == artifact["sha256"]


@pytest.mark.parametrize("index", [0, 1])
@pytest.mark.parametrize("bad", ["bytes", "size", "filename", "mime", "oversize"])
def test_unknown_bytes_and_metadata_rejected_before_any_parser(host, monkeypatch, index, bad):
    def forbidden(*args, **kwargs):
        pytest.fail("Unadmitted source reached parser")
    monkeypatch.setattr(DocumentValidator, "validate", forbidden)
    entry = ENTRIES[index]
    data = (ROOT / entry["path"]).read_bytes()
    kwargs = {"content": data}
    if bad == "bytes":
        kwargs["content"] = data[:-1] + bytes([data[-1] ^ 1])
    elif bad == "size":
        kwargs["content"] = data[:-1]
    elif bad == "oversize":
        kwargs["content"] = b"x" * 2049
    elif bad == "filename":
        kwargs["filename"] = "../" + entry["filename"]
    else:
        kwargs["mime"] = "application/octet-stream"
    assert upload(host, index, **kwargs).status_code in {413, 415}
    assert not host.bridge.documents


@pytest.mark.parametrize("extra", [
    [("content-length", "1"), ("content-length", "2")],
    [("transfer-encoding", "chunked")], [("content-encoding", "gzip")],
    [("x-aiip-filename", "controller.pdf"), ("x-aiip-filename", "controller.pdf")],
])
def test_suspicious_framing_never_reaches_parser(host, monkeypatch, extra):
    monkeypatch.setattr(DocumentValidator, "validate", lambda *a, **k: pytest.fail("Parser invoked"))
    headers = [(k, v) for k, v in host.headers.items() if k.lower() not in {"content-type"}]
    headers += [("content-type", "application/pdf"), *extra]
    assert host.http.post(BASE, content=b"x", headers=headers).status_code in {400, 415}


def test_streaming_limit_and_declared_length_mismatch(host, monkeypatch):
    monkeypatch.setattr(DocumentValidator, "validate", lambda *a, **k: pytest.fail("Parser invoked"))
    for parts, declared in [([b"x" * 1024, b"x" * 1025], "2048"), ([b"x"], "2")]:
        response = host.http.post(BASE, content=iter(parts), headers={**host.headers,
            "Content-Type": "application/pdf", "X-AIIP-Filename": "controller.pdf", "Content-Length": declared})
        assert response.status_code in {400, 413}


def test_forged_expired_and_missing_csrf_rejected(host):
    for overrides in [{"Cookie": f"{LOGIN}=" + "z" * 43}, {"X-AIIP-CSRF": "bad"}]:
        assert upload(host, headers={**host.headers, **overrides}).status_code in {401, 403}
    host.clock[0] += 1800
    assert upload(host).status_code == 401


def test_two_owners_cross_source_views_and_selectors(host):
    first = begin(host)
    view = review(host, first)
    assert upload(host).status_code == 409
    with host.client() as other:
        h = host.login(other)
        second = begin(host, 1, client=other, headers=h)
        assert second != first
        assert other.get(f"{BASE}/{first}/review", headers=h).status_code == 404
        assert host.http.get(f"{BASE}/{second}/review", headers=host.headers).status_code == 404
        assert other.post(f"{BASE}/{second}/ack-content", headers=h,
            json={"revision": 1, "view_id": view["view_id"], "acknowledge": True}).status_code == 409


def test_separate_affirmations_stale_view_revision_and_no_generic_edit(host):
    doc = begin(host)
    view = review(host, doc)
    assert decision(host, doc, view, "render").status_code == 409
    assert decision(host, doc, view, "ack-claims").status_code == 409
    current = review(host, doc)
    assert current["view_id"] != view["view_id"]
    assert decision(host, doc, view, "ack-content").status_code == 409
    for bad in [{**current, "revision": 2}, {**current, "revision": True}]:
        assert decision(host, doc, bad, "ack-content").status_code == 409
    assert decision(host, doc, current, "ack-content").status_code == 200
    assert decision(host, doc, current, "render").status_code == 409
    assert host.http.post(f"{BASE}/{doc}/ack-claims", headers=host.headers,
        json={"revision": 1, "view_id": current["view_id"], "acknowledge": False}).status_code == 409
    assert host.http.put(f"{BASE}/{doc}/analysis", headers=host.headers, json={}).status_code == 405
    assert decision(host, doc, current, "ack-claims").status_code == 200
    assert decision(host, doc, current, "render").status_code == 200


@pytest.mark.parametrize("invalidate", ["logout", "expiry", "cancel", "host-revoke"])
def test_revoke_during_render_is_immediate_and_late_result_disposed(host, monkeypatch, invalidate):
    doc = begin(host)
    view = review(host, doc)
    decision(host, doc, view, "ack-content")
    decision(host, doc, view, "ack-claims")
    entered, release = threading.Event(), threading.Event()
    original = custody.render_uspto_document_package
    def slow(*args, **kwargs):
        entered.set()
        assert release.wait(10)
        return original(*args, **kwargs)
    monkeypatch.setattr(custody, "render_uspto_document_package", slow)
    with ThreadPoolExecutor(max_workers=1) as pool:
        pending = pool.submit(decision, host, doc, view, "render")
        assert entered.wait(5)
        try:
            assert host.http.get(f"{BASE}/{doc}/review", headers=host.headers).status_code == 429
            started = time.monotonic()
            if invalidate == "logout":
                assert host.http.request("DELETE", PREFIX + "/session", headers=host.headers, json={}).status_code == 200
            elif invalidate == "expiry":
                host.clock[0] += 1801
                host.sessions.status(None, None)
            elif invalidate == "host-revoke":
                host.sessions.revoke_all()
            else:
                assert host.http.request("DELETE", f"{BASE}/{doc}", headers=host.headers, json={}).status_code == 200
            assert time.monotonic() - started < 1
            assert not pending.done()  # Revocation has NOT stopped computation.
            item = next(iter(host.bridge.documents.values()))
            assert item.retired and item.export is None
            assert host.http.get(f"{BASE}/{doc}/revisions/1/artifacts/{FILES[0]}", headers=host.headers).status_code in {401, 404}
        finally:
            release.set()
        assert pending.result(timeout=15).status_code in {401, 503}
    assert not host.bridge.documents
    assert list(host.bridge.root.iterdir()) == []


def test_logout_during_intake_rejects_and_cleans_late_work(host, monkeypatch):
    entered, release = threading.Event(), threading.Event()
    original = PinnedSyntheticRuntime.run_extraction
    def slow(self, *args, **kwargs):
        entered.set()
        assert release.wait(10)
        return original(self, *args, **kwargs)
    monkeypatch.setattr(PinnedSyntheticRuntime, "run_extraction", slow)
    with ThreadPoolExecutor(max_workers=1) as pool:
        pending = pool.submit(upload, host)
        assert entered.wait(5)
        try:
            assert host.http.request("DELETE", PREFIX + "/session", headers=host.headers, json={}).status_code == 200
            assert not pending.done()
        finally:
            release.set()
        assert pending.result(timeout=10).status_code == 401
    assert list(host.bridge.root.iterdir()) == []


@pytest.mark.parametrize("tamper", ["artifact", "manifest"])
def test_corrupt_artifact_revokes_whole_bundle(host, tamper):
    doc, view, export = rendered(host)
    if tamper == "artifact":
        target = next(host.bridge.root.rglob(FILES[-1]))
        target.write_bytes(b"corrupt")
    else:
        item = next(iter(host.bridge.documents.values()))
        item.export = replace(item.export, manifest_sha256="0" * 64)
    for name in FILES:
        assert host.http.get(f"{BASE}/{doc}/revisions/1/artifacts/{name}", headers=host.headers).status_code != 200


def test_oversized_response_is_fail_closed(host, monkeypatch):
    import backend.app.services.product_web_bridge as module
    doc = begin(host)
    monkeypatch.setattr(module, "REVIEW_LIMIT", 32)
    assert host.http.get(f"{BASE}/{doc}/review", headers=host.headers).status_code != 200


def test_source_analysis_substitution_and_line_ending_scope(host, monkeypatch):
    runtime = PinnedSyntheticRuntime()
    first = runtime._analyses[PINS[0][3]]
    second = runtime._analyses[PINS[1][3]]
    # Simulate an adapter regression: C1 still rejects cross-source evidence.
    host.bridge.runtime._analyses[PINS[0][3]] = (deepcopy(second[0]), first[1], first[2])
    assert upload(host).status_code != 201
    assert not host.bridge.documents
    original = Path.read_bytes
    def changed(path):
        raw = original(path)
        if str(path).replace("\\", "/").endswith("research-b-analysis.json"):
            return raw + b"\r\n"
        return raw
    monkeypatch.setattr(Path, "read_bytes", changed)
    with pytest.raises(ValueError, match="identity"):
        PinnedSyntheticRuntime()


def test_default_apps_and_s1_only_expose_zero_document_routes():
    for app in (create_local_app(), create_app()):
        assert not any(getattr(route, "path", "").startswith(BASE) for route in app.routes)


def test_projection_preserves_null_absence_order_and_rejects_arbitrary_json(host):
    doc = begin(host)
    value = review(host, doc)
    item = next(iter(host.bridge.documents.values()))
    from backend.app.services.custody_review import review_documents
    assert value["originals"] == review_documents(item.workflow.review(item.ref).originals)
    assert host.http.post(f"{BASE}/{doc}/ack-content", headers=host.headers,
        json={"revision": 1, "view_id": value["view_id"], "acknowledge": True, "actor": "forged"}).status_code == 409


def test_operation_timeout_keeps_capacity_until_late_work_returns(host, monkeypatch):
    import backend.app.services.product_web_bridge as module
    entered, release = threading.Event(), threading.Event()
    original = PinnedSyntheticRuntime.run_extraction
    def slow(self, *args, **kwargs):
        entered.set()
        assert release.wait(10)
        return original(self, *args, **kwargs)
    monkeypatch.setattr(PinnedSyntheticRuntime, "run_extraction", slow)
    monkeypatch.setattr(module, "OP_SECONDS", 0.2)
    with ThreadPoolExecutor(max_workers=1) as pool:
        pending = pool.submit(upload, host)
        assert entered.wait(5)
        try:
            assert pending.result(timeout=3).status_code == 504
            assert host.bridge.capacity.locked()
            assert next(iter(host.bridge.documents.values())).retired
            assert upload(host).status_code == 429
        finally:
            release.set()
    deadline = time.monotonic() + 10
    while host.bridge.capacity.locked() and time.monotonic() < deadline:
        time.sleep(0.01)
    assert not host.bridge.capacity.locked() and not host.bridge.documents


def test_adapter_rejects_wrong_locator_and_missing_provider_isolation(host):
    from backend.app.schemas.analysis_input import ExtractionInputEnvelope
    doc = begin(host)
    source = review(host, doc)["originals"]["source_envelope"]
    source["source_units"][0]["locator"]["page"] = 2
    with pytest.raises(ValueError, match="source"):
        PinnedSyntheticRuntime().run_extraction(ExtractionInputEnvelope.model_validate(source))
    from backend.app.services.product_synthetic_workflow import ProductWorkflowError
    with pytest.raises(ProductWorkflowError) as error:
        OfflineSyntheticWorkflow(None, None, None, output_root=host.root / "never-created",
            extraction_runtime=SimpleNamespace(synthetic_only=False), authorize_invocation=lambda: True,
            review_authorizer=lambda *a: True, enabled=True)
    assert error.value.code == "PROVIDER_BLOCKED"


def test_publication_fence_rechecks_after_response_buffering():
    import asyncio
    from backend.app.api.product_web_synthetic import PublicationFence
    from backend.app.services.product_web_bridge import BridgeError
    sent = []
    async def source(scope, receive, send):
        def denied():
            raise BridgeError(401, "authority_revoked")
        scope["state"]["s2_fence"] = denied
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b"LATE_PRIVATE_RESULT"})
    async def collect(message):
        sent.append(message)
    async def receive():
        return {"type": "http.disconnect"}
    asyncio.run(PublicationFence(source)({"type": "http", "path": BASE, "state": {}}, receive, collect))
    assert sent[0]["status"] == 401
    assert b"LATE_PRIVATE_RESULT" not in b"".join(message.get("body", b"") for message in sent)


def test_cleanup_failure_quarantines_and_denies_reuse(host, monkeypatch):
    from backend.app.services.product_web_host_control import SecurityError
    doc = begin(host)
    item = next(iter(host.bridge.documents.values()))
    original = item.workflow.close
    def fail():
        raise OSError("synthetic cleanup failure")
    # Hold the sole slot so maintenance cannot race fault injection/assertions.
    assert host.bridge.capacity.acquire(blocking=False)
    try:
        monkeypatch.setattr(item.workflow, "close", fail)
        host.bridge.cancel(item.token, doc)
        host.bridge._reap()
        assert host.bridge.quarantined and item.retired and item.root.exists()
    finally:
        host.bridge.capacity.release()
    assert upload(host).status_code == 503
    with pytest.raises(SecurityError):
        host.bridge.close()
    # Test-only repair for fixture disposal; no application reset API exists.
    monkeypatch.setattr(item.workflow, "close", original)
    host.bridge._dispose(item)
    host.bridge.quarantined = False
