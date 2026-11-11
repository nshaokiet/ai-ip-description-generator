"""S1 boundary tests. State tests supplement, never replace, real IPC tests."""
from __future__ import annotations

from types import SimpleNamespace
from concurrent.futures import ThreadPoolExecutor

from fastapi.testclient import TestClient
import pytest

from backend.app.local_product_web import LOGIN, PREFIX, PRELOGIN, Sessions, create_local_app
from backend.app.services.product_web_host_control import (
    PairingControl, create_private_dir, request_control, restrict_owned,
)


@pytest.fixture
def shell(tmp_path):
    restrict_owned(tmp_path)
    root = create_private_dir(tmp_path / "control")
    clock = [1000.0]
    sessions = Sessions(clock=lambda: clock[0])
    control = PairingControl(root, sessions.approve, sessions.revoke_all).start()
    secret = "a" * 64
    app = create_local_app(enabled=True, sessions=sessions, control=control,
                           proxy_secret=secret, backend_port=8765)
    headers = {"Origin": "https://localhost:3443", "Sec-Fetch-Site": "same-origin",
               "X-AIIP-Proxy": secret, "Content-Type": "application/json"}
    def client():
        return TestClient(app, base_url="https://127.0.0.1:8765", client=("127.0.0.1", 12345))
    config = {"instance": control.instance, "control_key": control.key, "address": control.address}
    try:
        with client() as http:
            yield SimpleNamespace(http=http, client=client, headers=headers, app=app, clock=clock,
                                  sessions=sessions, control=control, config=config)
    finally:
        control.stop()


def bootstrap(shell, client=None):
    return (client or shell.http).post(PREFIX + "/session/bootstrap", content="{}",
                                      headers={**shell.headers, "X-AIIP-Bootstrap": "1"})


def login(shell, client=None):
    client = client or shell.http
    pending = bootstrap(shell, client).json()
    assert request_control(shell.config, pending["selector"])
    return client.post(PREFIX + "/session", content="{}",
                       headers={**shell.headers, "X-AIIP-CSRF": pending["csrf"]})


def test_real_pairing_rotates_cookies_csrf_and_does_not_authenticate_on_approval(shell):
    result = bootstrap(shell)
    assert result.status_code == 200
    old = shell.http.cookies.get(PRELOGIN)
    pending = result.json()
    repeated = bootstrap(shell)
    assert repeated.json() == pending and shell.http.cookies.get(PRELOGIN) == old
    denied = shell.http.post(PREFIX + "/session", content="{}",
                             headers={**shell.headers, "X-AIIP-CSRF": pending["csrf"]})
    assert denied.status_code == 403
    assert request_control(shell.config, pending["selector"])
    assert shell.http.get(PREFIX + "/session", headers=shell.headers).json()["state"] == "pending"
    accepted = shell.http.post(PREFIX + "/session", content="{}",
                               headers={**shell.headers, "X-AIIP-CSRF": pending["csrf"]})
    assert accepted.status_code == 200 and accepted.json()["state"] == "authenticated"
    assert shell.http.cookies.get(LOGIN) != old
    assert accepted.json()["csrf"] != pending["csrf"]
    assert not shell.http.cookies.get(PRELOGIN)
    cookie = accepted.headers.get_list("set-cookie")[-1].lower()
    for attribute in ("secure", "httponly", "samesite=strict", "path=/"):
        assert attribute in cookie
    assert "domain=" not in cookie
    assert shell.http.post(PREFIX + "/session", content="{}", headers={
        **shell.headers, "X-AIIP-CSRF": pending["csrf"], "Cookie": f"{PRELOGIN}={old}"
    }).status_code == 401


@pytest.mark.parametrize("name,value", [
    ("Origin", None), ("Origin", "null"), ("Origin", "https://evil.invalid"),
    ("Host", "localhost:3443"), ("Host", "attacker.invalid:8765"),
    ("Sec-Fetch-Site", None), ("Sec-Fetch-Site", "cross-site"),
    ("X-AIIP-Proxy", None), ("X-AIIP-Proxy", "wrong"),
    ("Forwarded", "host=localhost"), ("X-Forwarded-Host", "localhost"),
    ("X-Internal-Control", "1"),
])
def test_authentication_guard_precedes_allocation(shell, name, value):
    headers = {**shell.headers, "X-AIIP-Bootstrap": "1"}
    headers.pop(name, None)
    if value is not None:
        headers[name] = value
    result = shell.http.post(PREFIX + "/session/bootstrap", content="{}", headers=headers)
    assert result.status_code == 403
    assert not shell.sessions.pending


def test_duplicate_origin_cookie_and_unexpected_body_or_query_fail(shell):
    headers = list(shell.headers.items()) + [("Origin", "https://localhost:3443")]
    assert shell.http.post(PREFIX + "/session/bootstrap", content="{}", headers=headers).status_code == 400
    assert shell.http.get(PREFIX + "/session?owner=forged", headers=shell.headers).status_code == 403
    assert shell.http.get(PREFIX + "/session", headers={**shell.headers, "Cookie":
        f"{LOGIN}={'x'*43}; {LOGIN}={'x'*43}"}).status_code == 400
    assert shell.http.post(PREFIX + "/session/bootstrap", content='{"actor":"operator"}',
                           headers={**shell.headers, "X-AIIP-Bootstrap": "1"}).status_code == 400
    assert shell.http.post(PREFIX + "/session/bootstrap", content="x" * 4097,
                           headers={**shell.headers, "X-AIIP-Bootstrap": "1"}).status_code == 413


def test_cross_session_csrf_logout_revocation_and_restart(shell):
    first = login(shell).json()
    with shell.client() as other:
        second = login(shell, other).json()
        assert first["csrf"] != second["csrf"]
        assert shell.http.cookies.get(LOGIN) != other.cookies.get(LOGIN)
        for csrf in ("wrong", second["csrf"], ""):
            assert shell.http.request("DELETE", PREFIX + "/session", content="{}", headers={
                **shell.headers, "X-AIIP-CSRF": csrf}).status_code == 403
        assert shell.http.request("DELETE", PREFIX + "/session", content="{}", headers={
            **shell.headers, "X-AIIP-CSRF": first["csrf"]}).status_code == 200
        assert other.get(PREFIX + "/session", headers=shell.headers).json()["state"] == "authenticated"
        assert shell.http.request("DELETE", PREFIX + "/session", content="{}", headers={
            **shell.headers, "X-AIIP-CSRF": first["csrf"]}).status_code == 401
        assert request_control(shell.config, action="revoke-all")
        assert other.get(PREFIX + "/session", headers=shell.headers).json()["state"] == "anonymous"
        assert Sessions().status(None, other.cookies.get(LOGIN))["state"] == "anonymous"


def test_absolute_lifetimes_and_capacities_do_not_renew_on_reads(shell):
    pending = bootstrap(shell).json()
    shell.clock[0] += 59
    assert bootstrap(shell).json()["expires_in"] == 1
    shell.clock[0] += 1
    assert not request_control(shell.config, pending["selector"])
    assert shell.http.get(PREFIX + "/session", headers=shell.headers).json()["state"] == "anonymous"
    # Capacity is a global server bound, independent of browser cookie selection.
    shell.sessions.allocations.clear()
    for _ in range(8):
        shell.sessions.bootstrap(None, None)
    with pytest.raises(Exception):
        shell.sessions.bootstrap(None, None)
    shell.sessions.revoke_all()
    shell.sessions.allocations.clear()
    first = login(shell).json()
    with shell.client() as other, shell.client() as third:
        login(shell, other)
        pending = bootstrap(shell, third).json()
        assert request_control(shell.config, pending["selector"])
        assert third.post(PREFIX + "/session", content="{}", headers={
            **shell.headers, "X-AIIP-CSRF": pending["csrf"]}).status_code == 429
    shell.clock[0] += 1799
    assert shell.http.get(PREFIX + "/session", headers=shell.headers).json()["expires_in"] == 1
    shell.clock[0] += 1
    assert shell.http.get(PREFIX + "/session", headers=shell.headers).json()["state"] == "anonymous"
    assert first["state"] == "authenticated"


def test_default_apps_no_document_routes_or_provider_activity(shell):
    from tests.e2e.provider_tripwire import ProviderTripwire
    guard = ProviderTripwire().install()
    try:
        from backend.app.main import create_app
        from backend.app.demo_staging import create_demo_staging_app
        app = create_local_app(enabled=True, sessions=shell.sessions, control=shell.control,
                               proxy_secret="b" * 64, backend_port=8765)
        assert {route.path for route in app.routes} == {PREFIX + "/session", PREFIX + "/session/bootstrap"}
        assert not create_local_app().routes
        for released in (create_app(), create_demo_staging_app()):
            with TestClient(released) as client:
                assert client.get(PREFIX + "/session").status_code == 404
                assert client.post(PREFIX + "/session/bootstrap", json={}).status_code == 404
        for path in ("/api/documents", "/api/process", "/review", "/render", "/download", "/docs"):
            assert shell.http.get(path, headers=shell.headers).status_code == 404
        guard.assert_no_unexpected_activity()
    finally:
        guard.close()


def test_dead_control_channel_revokes_sessions(shell):
    login(shell)
    shell.control.error = True
    assert shell.http.get(PREFIX + "/session", headers=shell.headers).status_code == 503
    assert not shell.sessions.authenticated


def test_concurrent_bootstrap_and_login_consume_one_approval(shell):
    def allocate(_):
        with shell.client() as client:
            response = bootstrap(shell, client)
            return response.json(), client.cookies.get(PRELOGIN)
    with ThreadPoolExecutor(max_workers=2) as pool:
        allocations = list(pool.map(allocate, range(2)))
    assert len(shell.sessions.pending) == 2
    assert allocations[0][0]["selector"] != allocations[1][0]["selector"]
    pending, cookie = allocations[0]
    assert request_control(shell.config, pending["selector"])
    def complete(_):
        with shell.client() as client:
            return client.post(PREFIX + "/session", content="{}", headers={
                **shell.headers, "Cookie": f"{PRELOGIN}={cookie}", "X-AIIP-CSRF": pending["csrf"]
            }).status_code
    with ThreadPoolExecutor(max_workers=2) as pool:
        assert sorted(pool.map(complete, range(2))) == [200, 401]
    assert len(shell.sessions.authenticated) == 1


def test_allocation_rate_limit_survives_host_revocation(shell):
    for _ in range(12):
        assert bootstrap(shell).status_code == 200
        assert request_control(shell.config, action="revoke-all")
    assert bootstrap(shell).status_code == 429
    shell.clock[0] += 60
    assert bootstrap(shell).status_code == 200
