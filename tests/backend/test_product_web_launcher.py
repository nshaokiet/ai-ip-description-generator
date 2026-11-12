"""S1-RC-01/02: minimal child environment and bounded independent teardown."""
import json
import os
from pathlib import Path
import subprocess
import sys
import sysconfig
import threading
import time
from types import SimpleNamespace

import pytest

from backend.app import local_product_web as launcher
from backend.app.services.product_web_host_control import (
    SecurityError, create_private_dir, restrict_owned, write_private,
)
from tests.e2e.product_web_host import prepare


def test_real_node_receives_only_explicit_runtime_environment(tmp_path):
    parent = {name: os.environ[name] for name in launcher.NODE_RUNTIME_ENV if name in os.environ}
    forbidden = {"AWS_SECRET_ACCESS_KEY", "GITHUB_TOKEN", "ANTHROPIC_API_KEY", "AZURE_CLIENT_SECRET",
                 "AIIP_UNRELATED_TOKEN", "PYTHONPATH", "PYTHONHOME", "NODE_OPTIONS"}
    parent.update({name: "synthetic-dummy-value" for name in forbidden})
    parent.update({"NODE_ENV": "development", "NEXT_TELEMETRY_DISABLED": "0",
                   "AIIP_S1_HOST_FILE": "synthetic-wrong-path", "LD_LIBRARY_PATH": "synthetic-unsafe-loader"})
    environment = launcher._node_environment(tmp_path / "proxy.json", tmp_path / "cert", tmp_path / "key", parent=parent)
    assert not forbidden.intersection(environment)
    expected = set(launcher.NODE_RUNTIME_ENV).intersection(parent) | {
        "AIIP_S1_HOST_FILE", "AIIP_S1_CERT", "AIIP_S1_KEY", "AIIP_S1_PYTHON", "NODE_ENV", "NEXT_TELEMETRY_DISABLED"}
    if sys.platform == "linux" and sysconfig.get_config_var("Py_ENABLE_SHARED"):
        expected.add("LD_LIBRARY_PATH")
        assert environment["LD_LIBRARY_PATH"] == sysconfig.get_config_var("LIBDIR")
    assert set(environment) == expected
    assert all(environment[name] == parent[name] for name in launcher.NODE_RUNTIME_ENV if name in parent)
    if os.name == "nt":
        assert "SYSTEMROOT" in environment and "USERPROFILE" in environment
    else:
        assert "PATH" in environment and "HOME" in environment
    code = "console.log(JSON.stringify({names:Object.keys(process.env),mode:process.env.NODE_ENV,telemetry:process.env.NEXT_TELEMETRY_DISABLED}))"
    child = subprocess.run(["node", "-e", code], env=environment, capture_output=True, text=True, timeout=10, check=True)
    observed = json.loads(child.stdout)
    assert not forbidden.intersection(observed["names"])
    assert observed["mode"] == "production" and observed["telemetry"] == "1"
    assert environment["AIIP_S1_HOST_FILE"] != parent["AIIP_S1_HOST_FILE"]
    assert not child.stderr
    python = subprocess.run([sys.executable, "-c", "print('python-child-ok')"], env=environment,
                            capture_output=True, text=True, check=True, timeout=10)
    assert python.stdout.strip() == "python-child-ok"


@pytest.mark.parametrize("ignore_terminate", [False, True])
def test_owned_real_child_is_terminated_or_killed_and_reaped(tmp_path, ignore_terminate):
    ready = tmp_path / "ready"
    code = ("import sys,time,signal;from pathlib import Path;"
            + ("signal.signal(signal.SIGTERM,signal.SIG_IGN);" if ignore_terminate and os.name != "nt" else "")
            + "Path(sys.argv[1]).write_text('ready');time.sleep(60)")
    process = subprocess.Popen([sys.executable, "-c", code, str(ready)], stdin=subprocess.DEVNULL,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    killed = []
    class OwnedChild:
        poll = process.poll
        wait = process.wait
        def terminate(self):
            # Windows TerminateProcess cannot be ignored; inject that failure
            # while still using real bounded wait, native kill and OS reaping.
            if not (ignore_terminate and os.name == "nt"):
                process.terminate()
        def kill(self):
            killed.append(True)
            process.kill()
    try:
        deadline = time.monotonic() + 5
        while not ready.exists() and time.monotonic() < deadline and process.poll() is None:
            time.sleep(0.01)
        assert ready.exists()
        launcher._stop_child(OwnedChild(), timeout=0.2 if ignore_terminate else 1)
        assert process.poll() is not None
        assert bool(killed) is ignore_terminate
    finally:
        if process.poll() is None:
            process.kill()
        process.wait(timeout=5)


class FakeChild:
    def __init__(self, sessions, stuck=False):
        self.sessions, self.stuck, self.alive, self.killed = sessions, stuck, True, False
    def poll(self):
        return None if self.alive else -9
    def terminate(self):
        assert self.sessions.closed and not self.sessions.authenticated
    def wait(self, timeout):
        if self.alive:
            raise subprocess.TimeoutExpired("synthetic-child", timeout)
        return -9
    def kill(self):
        self.killed = True
        self.alive = self.stuck


def resources(tmp_path, fault=None):
    restrict_owned(tmp_path)
    root = create_private_dir(tmp_path / "state")
    for name in ("host.json", "proxy.json"):
        write_private(root / name, {"synthetic": True})
    sessions = launcher.Sessions()
    pending, token = sessions.bootstrap(None, None)
    assert sessions.approve(pending["selector"])
    sessions.login(token, pending["csrf"])
    flags = set()
    def action(name):
        flags.add(name)
        if name == fault:
            raise OSError("synthetic-cleanup-failure")
    control = SimpleNamespace(stopping=threading.Event(), thread=object(), stop=lambda: action("ipc"))
    thread = SimpleNamespace(join=lambda timeout: action("join"), is_alive=lambda: fault == "backend")
    return SimpleNamespace(sessions=sessions, child=FakeChild(sessions, fault == "child"),
                           server=SimpleNamespace(should_exit=False), thread=thread,
                           listener=SimpleNamespace(close=lambda: action("listener")),
                           control=control, root=root, flags=flags)


def clean(value):
    return launcher._cleanup(value.sessions, value.child, value.server, value.thread,
                             value.listener, value.control, value.root)


def test_successful_cleanup_seals_sessions_before_forced_child_teardown(tmp_path):
    value = resources(tmp_path)
    assert clean(value) == ()
    assert value.child.killed and not value.child.alive
    assert value.flags == {"join", "listener", "ipc"}
    assert value.server.should_exit and value.control.stopping.is_set()
    assert not value.root.exists()
    with pytest.raises(launcher.AuthError) as error:
        value.sessions.bootstrap(None, None)
    assert error.value.status == 503


@pytest.mark.parametrize("fault,stage", [("child", "child"), ("ipc", "control"),
                                        ("backend", "backend_thread"), ("listener", "listener")])
def test_cleanup_failure_does_not_skip_independent_teardown_or_delete_state(tmp_path, fault, stage):
    value = resources(tmp_path, fault)
    assert stage in clean(value)
    assert value.sessions.closed and not value.sessions.authenticated
    assert value.flags == {"join", "listener", "ipc"}
    assert value.server.should_exit and value.control.stopping.is_set()
    assert value.root.exists()  # Fail closed: retain private state for inspection.
    assert (value.root / "host.json").exists() and (value.root / "proxy.json").exists()


def test_one_file_unlink_error_does_not_skip_other_owned_file(tmp_path, monkeypatch):
    value = resources(tmp_path)
    unlink = Path.unlink
    def fail_one(path, *args, **kwargs):
        if path == value.root / "host.json":
            raise OSError("synthetic-unlink-failure")
        return unlink(path, *args, **kwargs)
    monkeypatch.setattr(Path, "unlink", fail_one)
    assert clean(value) == ("state_file",)
    assert (value.root / "host.json").exists()
    assert not (value.root / "proxy.json").exists()


def test_partial_startup_stops_real_ipc_and_cleans_owned_state(tmp_path, monkeypatch):
    state, certificate, key = prepare(tmp_path)
    actual_write, actual_control = launcher.write_private, launcher.PairingControl
    actual_socket = launcher.socket.socket
    controls, writes, sockets = [], [], []
    def observe_socket(*args, **kwargs):
        value = actual_socket(*args, **kwargs)
        sockets.append(value)
        return value
    class ObservedControl(actual_control):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            controls.append(self)
    def fail_second(path, value):
        writes.append(path)
        if len(writes) == 2:
            raise OSError("synthetic-second-file-failure")
        return actual_write(path, value)
    monkeypatch.setattr(launcher, "PairingControl", ObservedControl)
    monkeypatch.setattr(launcher, "write_private", fail_second)
    monkeypatch.setattr(launcher.socket, "socket", observe_socket)
    with pytest.raises(OSError):
        launcher.run(state, certificate, key)
    assert len(controls) == 1 and not controls[0].thread.is_alive()
    assert sockets and all(value.fileno() == -1 for value in sockets)
    assert list(state.iterdir()) == []


def test_failed_directory_verification_quarantines_instead_of_blind_deletion(tmp_path, monkeypatch):
    state, certificate, key = prepare(tmp_path)
    actual_create = launcher.create_private_dir
    def fail_after_create(path):
        actual_create(path)
        raise SecurityError()
    monkeypatch.setattr(launcher, "create_private_dir", fail_after_create)
    with pytest.raises(SecurityError):
        launcher.run(state, certificate, key)
    assert len(list(state.iterdir())) == 1
