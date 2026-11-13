"""Explicit S1 local authentication shell. No product or provider routes/imports."""
from __future__ import annotations

import argparse
from collections import deque
import hmac
import json
import os
from pathlib import Path
import re
import secrets
import socket
import ssl
import subprocess
import sys
import sysconfig
import threading
import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.app.services.product_web_host_control import (
    PairingControl, SecurityError, create_private_dir, safe_path, write_private,
)

ORIGIN = "https://localhost:3443"
PREFIX = "/api/product-web/v1"
PRELOGIN, LOGIN = "__Host-aiip_prelogin", "__Host-aiip_web"
TOKEN = re.compile(r"^[A-Za-z0-9_-]{43}$")
HEADERS = {"Cache-Control": "no-store", "X-Content-Type-Options": "nosniff",
           "Referrer-Policy": "no-referrer", "X-Frame-Options": "DENY"}
NODE_RUNTIME_ENV = ("PATH", "SYSTEMROOT", "WINDIR", "TEMP", "TMP", "TMPDIR", "HOME", "USERPROFILE")


class AuthError(Exception):
    def __init__(self, status, code):
        self.status, self.code = status, code


def _deny_unless(condition, status=403, code="request_rejected"):
    if not condition:
        raise AuthError(status, code)


class Sessions:
    """One local operator; independent browser principals; no persistent state."""
    def __init__(self, *, clock=time.monotonic):
        self.clock, self.lock = clock, threading.RLock()
        self.pending, self.authenticated, self.allocations = {}, {}, deque()
        self.closed = False

    def _sweep(self):
        _deny_unless(not self.closed, 503, "session_unavailable")
        now = self.clock()
        for records in (self.pending, self.authenticated):
            for key in tuple(records):
                if now >= records[key]["deadline"]:
                    del records[key]
        while self.allocations and self.allocations[0] <= now - 60:
            self.allocations.popleft()

    def _info(self, record, state):
        value = {"state": state, "csrf": record["csrf"],
                 "expires_in": max(0, int(record["deadline"] - self.clock()))}
        if state == "pending":
            value["selector"] = record["selector"]
        return value

    def status(self, prelogin, session):
        with self.lock:
            self._sweep()
            if session in self.authenticated:
                return self._info(self.authenticated[session], "authenticated")
            if prelogin in self.pending:
                return self._info(self.pending[prelogin], "pending")
            return {"state": "anonymous"}

    def bootstrap(self, prelogin, session):
        with self.lock:
            info = self.status(prelogin, session)
            if info["state"] != "anonymous":
                return info, None
            _deny_unless(len(self.pending) < 8 and len(self.allocations) < 12, 429, "capacity")
            value = {"csrf": secrets.token_urlsafe(32), "selector": secrets.token_urlsafe(32),
                     "deadline": self.clock() + 60, "approved": False}
            token = secrets.token_urlsafe(32)
            self.pending[token] = value
            self.allocations.append(self.clock())
            return self._info(value, "pending"), token

    def approve(self, selector):
        with self.lock:
            self._sweep()
            for record in self.pending.values():
                if hmac.compare_digest(record["selector"], selector) and not record["approved"]:
                    record["approved"] = True
                    return True
            return False

    def login(self, token, csrf):
        with self.lock:
            self._sweep()
            record = self.pending.get(token)
            _deny_unless(record is not None, 401, "session_unavailable")
            _deny_unless(csrf and hmac.compare_digest(record["csrf"], csrf), 403, "csrf_rejected")
            _deny_unless(record["approved"], 403, "pairing_required")
            _deny_unless(len(self.authenticated) < 2, 429, "capacity")
            # Consume approval and retire both prelogin credentials atomically.
            del self.pending[token]
            value = {"csrf": secrets.token_urlsafe(32), "owner": secrets.token_hex(32),
                     "deadline": self.clock() + 1800}
            session = secrets.token_urlsafe(32)
            self.authenticated[session] = value
            return self._info(value, "authenticated"), session

    def logout(self, token, csrf):
        with self.lock:
            self._sweep()
            record = self.authenticated.get(token)
            _deny_unless(record is not None, 401, "session_unavailable")
            _deny_unless(csrf and hmac.compare_digest(record["csrf"], csrf), 403, "csrf_rejected")
            del self.authenticated[token]
            return {"state": "anonymous"}

    def revoke_all(self):
        with self.lock:
            self.pending.clear()
            self.authenticated.clear()
            return True

    def close(self):
        with self.lock:
            self.closed = True  # No new allocation or approval while teardown runs.
            self.pending.clear()
            self.authenticated.clear()


def _guard(request: Request, proxy_secret: str, backend_host: str):
    pairs = request.scope["headers"]
    _deny_unless(len(pairs) <= 64 and sum(len(k) + len(v) for k, v in pairs) <= 16384)
    values = {}
    for key, value in pairs:
        key = key.decode("ascii").lower()
        _deny_unless(key not in values, 400)
        values[key] = value.decode("latin-1")
        _deny_unless(key != "forwarded" and not key.startswith(("x-forwarded-", "x-internal-")))
    _deny_unless(request.client and request.client.host == "127.0.0.1")
    _deny_unless(values.get("host") == backend_host and not request.scope["query_string"])
    _deny_unless(hmac.compare_digest(values.get("x-aiip-proxy", ""), proxy_secret))
    _deny_unless(values.get("sec-fetch-site") == "same-origin")
    origin = values.get("origin")
    _deny_unless(origin == ORIGIN if request.method != "GET" else origin in {None, ORIGIN})
    if request.method != "GET":
        _deny_unless(values.get("content-type", "").lower() == "application/json")
    cookies = {}
    for item in values.get("cookie", "").split(";"):
        name, separator, value = item.strip().partition("=")
        if name in {PRELOGIN, LOGIN}:
            _deny_unless(separator and name not in cookies and TOKEN.fullmatch(value), 400)
            cookies[name] = value
    return values, cookies


def _cookie(response, name, token, age):
    response.set_cookie(name, token, max_age=age, secure=True, httponly=True,
                        samesite="strict", path="/")


def create_local_app(*, enabled=False, sessions=None, proxy_secret=None, backend_port=None, control=None):
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None, redirect_slashes=False)
    if not enabled:
        return app
    if (not isinstance(sessions, Sessions) or not isinstance(control, PairingControl)
            or getattr(control.approve, "__self__", None) is not sessions
            or not control.ready.is_set() or control.error or not control.thread.is_alive()
            or not isinstance(proxy_secret, str)
            or not re.fullmatch(r"[0-9a-f]{64}", proxy_secret)
            or type(backend_port) is not int or not 1 <= backend_port <= 65535):
        raise SecurityError()

    @app.middleware("http")
    async def boundary(request, call_next):
        try:
            if control.error or not control.thread.is_alive():
                sessions.revoke_all()
                raise AuthError(503, "operator_control_unavailable")
            headers, cookies = _guard(request, proxy_secret, f"127.0.0.1:{backend_port}")
            request.state.s1_headers, request.state.s1_cookies = headers, cookies
            response = await call_next(request)
        except AuthError as exc:
            response = JSONResponse({"error": {"code": exc.code}}, status_code=exc.status)
        except Exception:
            response = JSONResponse({"error": {"code": "session_unavailable"}}, status_code=503)
        response.headers.update(HEADERS)
        return response

    @app.api_route(PREFIX + "/session", methods=["GET", "POST", "DELETE"])
    @app.post(PREFIX + "/session/bootstrap")
    async def authentication(request: Request):
        try:
            _deny_unless(request.scope.get("raw_path") == request.url.path.encode(), 404)
            headers, cookies = request.state.s1_headers, request.state.s1_cookies
            prelogin, session = cookies.get(PRELOGIN), cookies.get(LOGIN)
            if request.method != "GET":
                data = bytearray()
                async for part in request.stream():
                    data.extend(part)
                    _deny_unless(len(data) <= 4096, 413, "body_limit")
                _deny_unless(json.loads(data) == {}, 400)
            if request.method == "GET":
                return JSONResponse(sessions.status(prelogin, session))
            if request.url.path.endswith("/bootstrap"):
                _deny_unless(headers.get("x-aiip-bootstrap") == "1")
                value, token = sessions.bootstrap(prelogin, session)
                response = JSONResponse(value)
                if token:
                    _cookie(response, PRELOGIN, token, 60)
                return response
            if request.method == "POST":
                value, token = sessions.login(prelogin, headers.get("x-aiip-csrf"))
                response = JSONResponse(value)
                _cookie(response, PRELOGIN, "", 0)
                _cookie(response, LOGIN, token, 1800)
                return response
            value = sessions.logout(session, headers.get("x-aiip-csrf"))
            response = JSONResponse(value)
            _cookie(response, LOGIN, "", 0)
            _cookie(response, PRELOGIN, "", 0)
            return response
        except AuthError as exc:
            return JSONResponse({"error": {"code": exc.code}}, status_code=exc.status)
        except (ValueError, UnicodeError):
            return JSONResponse({"error": {"code": "request_rejected"}}, status_code=400)
    return app


def _node_environment(proxy_path, certificate, key, *, parent=None):
    parent = os.environ if parent is None else parent
    environment = {name: parent[name] for name in NODE_RUNTIME_ENV if name in parent}
    # Never inherit NODE_OPTIONS, arbitrary AIIP_* or unrelated credentials.
    environment.update({"AIIP_S1_HOST_FILE": str(proxy_path), "AIIP_S1_CERT": str(certificate),
                        "AIIP_S1_KEY": str(key), "AIIP_S1_PYTHON": sys.executable,
                        "NODE_ENV": "production", "NEXT_TELEMETRY_DISABLED": "1"})
    if sys.platform == "linux" and sysconfig.get_config_var("Py_ENABLE_SHARED"):
        # The Node checker re-executes this Python. Hosted shared-Python builds
        # need their compiled LIBDIR; never copy an ambient loader search path.
        library = sysconfig.get_config_var("LIBDIR")
        if not isinstance(library, str) or not Path(library).is_absolute() or not Path(library).is_dir():
            raise SecurityError()
        environment["LD_LIBRARY_PATH"] = library
    return environment


def _stop_child(process, timeout=5):
    if process is None:
        return
    try:
        if process.poll() is None:
            process.terminate()
        process.wait(timeout=timeout)
    except Exception:
        # wait(timeout) never kills a process. Reap after a bounded kill fallback.
        try:
            if process.poll() is None:
                process.kill()
        finally:
            process.wait(timeout=timeout)
    if process.poll() is None:
        raise SecurityError()


def _cleanup(sessions, process, server, thread, listener, control, root):
    """Attempt independent teardown; quarantine state if any resource is unconfirmed."""
    failures = []

    def attempt(stage, action):
        try:
            action()
        except Exception:
            failures.append(stage)  # Codes only, never exception/credential contents.

    attempt("sessions", sessions.close)
    if control is not None:
        attempt("control_signal", control.stopping.set)
    if server is not None:
        attempt("backend_signal", lambda: setattr(server, "should_exit", True))
    attempt("child", lambda: _stop_child(process))
    if thread is not None:
        def join_backend():
            thread.join(5)
            if thread.is_alive():
                raise SecurityError()
        attempt("backend_thread", join_backend)
    if listener is not None:
        attempt("listener", listener.close)
    if control is not None and hasattr(control, "thread"):
        attempt("control", control.stop)
    if failures or root is None:
        return tuple(failures)
    try:
        safe_path(root, directory=True)
    except Exception:
        return ("state_directory",)
    for name in ("host.json", "proxy.json"):
        def remove_owned(name=name):
            path = root / name
            if path.exists() or path.is_symlink():
                safe_path(path)
                path.unlink()
        attempt("state_file", remove_owned)
    if not failures:
        attempt("state_directory", root.rmdir)  # Never recursively delete unknown files.
    return tuple(failures)


def run(state_parent: Path, certificate: Path, key: Path):
    """Explicit launcher. Parent must already be provisioned as owner-private."""
    safe_path(state_parent, directory=True)
    safe_path(certificate)
    safe_path(key)
    ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER).load_cert_chain(certificate, key, password=b"")
    if any(state_parent.iterdir()):
        raise SecurityError()  # Never delete another/live or crash-left host directory.
    sessions = Sessions()
    root = listener = control = process = server = thread = None
    try:
        root = create_private_dir(state_parent / ("s1-" + secrets.token_hex(16)))
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.bind(("127.0.0.1", 0))
        listener.listen(16)
        port = listener.getsockname()[1]
        control = PairingControl(root, sessions.approve, sessions.revoke_all)
        config_path, proxy_path = root / "host.json", root / "proxy.json"
        control.start()
        credential = secrets.token_hex(32)
        write_private(config_path, {"instance": control.instance, "control_key": control.key,
                                   "address": control.address})
        write_private(proxy_path, {"port": port, "proxy": credential})
        import uvicorn
        server = uvicorn.Server(uvicorn.Config(
            create_local_app(enabled=True, sessions=sessions, proxy_secret=credential, backend_port=port, control=control),
            proxy_headers=False, access_log=False, log_level="error"))
        thread = threading.Thread(target=lambda: server.run(sockets=[listener]), daemon=True)
        thread.start()
        environment = _node_environment(proxy_path, certificate, key)
        repo = Path(__file__).resolve().parents[2]
        process = subprocess.Popen(["node", str(repo / "frontend/tools/product-web-local-https.mjs")],
                                   cwd=repo / "frontend", env=environment)
        while process.poll() is None and not control.shutdown_requested.wait(0.1):
            if control.error or not control.thread.is_alive():
                raise SecurityError()
        if process.poll() is not None and process.returncode:
            raise SecurityError()
    finally:
        if _cleanup(sessions, process, server, thread, listener, control, root):
            raise SecurityError() from None


def main():
    parser = argparse.ArgumentParser(description="Explicit local S1 auth launcher")
    parser.add_argument("--enable", action="store_true", required=True)
    parser.add_argument("--state-parent", type=Path, required=True)
    parser.add_argument("--cert", type=Path, required=True)
    parser.add_argument("--key", type=Path, required=True)
    args = parser.parse_args()
    try:
        run(args.state_parent.absolute(), args.cert.absolute(), args.key.absolute())
    except (Exception, KeyboardInterrupt):
        print("S1 local authentication unavailable.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
