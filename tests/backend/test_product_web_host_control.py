"""Real OS channel/ACL tests on the executing platform; no mocked peers."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import socket
import stat
import threading

import pytest

from backend.app.services import product_web_host_control as control


@pytest.fixture
def private(tmp_path):
    return control.restrict_owned(tmp_path)


def test_native_channel_owner_checks_and_approval_are_real(private):
    seen = []
    host = control.PairingControl(private, lambda selector: seen.append(selector) or True, lambda: True).start()
    config = {"instance": host.instance, "control_key": host.key, "address": host.address}
    try:
        with ThreadPoolExecutor(max_workers=2) as pool:
            assert all(pool.map(lambda s: control.request_control(config, s), ["one", "two"]))
        assert sorted(seen) == ["one", "two"]
        if os.name == "nt":
            # Server and client perform actual descriptor readback and TokenUser
            # impersonation in production code. A Windows pipe is not a file.
            assert host.address.startswith("\\\\.\\pipe\\aiip-s1-")
        else:
            item = Path(host.address).lstat()
            assert stat.S_ISSOCK(item.st_mode) and item.st_uid == os.getuid()
            assert item.st_mode & 0o077 == 0
    finally:
        host.stop()
    if os.name != "nt":
        assert not Path(host.address).exists()
    with pytest.raises((OSError, control.SecurityError)):
        control.request_control(config, "after-stop")


@pytest.mark.parametrize("alteration", ["key", "instance", "selector"])
def test_bad_approval_does_not_bypass_real_control(private, alteration):
    host = control.PairingControl(private, lambda value: value == "allowed", lambda: True).start()
    config = {"instance": host.instance, "control_key": host.key, "address": host.address}
    try:
        kwargs = {"key": "0" * 64} if alteration == "key" else (
            {"instance": "0" * 64} if alteration == "instance" else {})
        try:
            accepted = control.request_control(config, "foreign" if alteration == "selector" else "allowed", **kwargs)
        except control.SecurityError:
            accepted = False
        assert not accepted
        assert control.request_control(config, "allowed")
    finally:
        host.stop()


def test_expired_challenge_and_replayed_approval_denied(private):
    calls = []
    times = iter([0, 6])
    host = control.PairingControl(private, lambda value: calls.append(value), lambda: True,
                                  clock=lambda: next(times)).start()
    config = {"instance": host.instance, "control_key": host.key, "address": host.address}
    try:
        with pytest.raises(control.SecurityError):
            control.request_control(config, "expired")
        assert not calls
    finally:
        host.stop()


def test_exact_wire_message_cannot_be_replayed_on_a_new_challenge(private):
    seen = []
    host = control.PairingControl(private, lambda value: seen.append(value) or True, lambda: True).start()
    config = {"instance": host.instance, "control_key": host.key, "address": host.address}
    try:
        with control._connection(config) as (read, write):
            challenge = json.loads(read())
            value = {**challenge, "action": "approve", "selector": "once"}
            wire = control._encode({**value, "mac": control._mac(host.key, value)}) + b"\n"
            write(wire)
            assert json.loads(read())["accepted"]
            write(b"done\n")
        with control._connection(config) as (read, write):
            assert json.loads(read())["nonce"] != challenge["nonce"]
            write(wire)
            with pytest.raises((OSError, control.SecurityError)):
                read()
        assert seen == ["once"]
    finally:
        host.stop()


def test_private_files_wrong_permissions_links_and_atomic_creation(private):
    directory = control.create_private_dir(private / "owned")
    target = directory / "state.json"
    control.write_private(target, {"nonsecret": True})
    assert control.read_private(target) == {"nonsecret": True}
    with pytest.raises(FileExistsError):
        control.write_private(target, {"replace": True})
    with pytest.raises((FileExistsError, control.SecurityError)):
        control.create_private_dir(directory)
    if os.name == "nt":
        win = control._windows()
        descriptor = control.C.c_void_p()
        assert win.a.ConvertStringSecurityDescriptorToSecurityDescriptorW(
            f"D:P(A;;GA;;;{win.sid})(A;;GR;;;WD)", 1, control.C.byref(descriptor), None)
        try:
            assert win.a.SetFileSecurityW(str(target), 0x80000004, descriptor)
        finally:
            win.k.LocalFree(descriptor)
        with pytest.raises(control.SecurityError):
            control.safe_path(target)
    else:
        target.chmod(0o644)
        with pytest.raises(control.SecurityError):
            control.safe_path(target)
        target.chmod(0o600)
        link = directory / "alias"
        link.symlink_to(target)
        with pytest.raises(control.SecurityError):
            control.safe_path(link)


def test_unavailable_channel_has_no_authentication_fallback(private):
    config = {"instance": "a" * 64, "control_key": "b" * 64,
              "address": r"\\.\pipe\aiip-s1-missing" if os.name == "nt" else str(private / "missing.sock")}
    with pytest.raises((OSError, control.SecurityError)):
        control.request_control(config, "missing")
    assert not threading.current_thread().daemon
