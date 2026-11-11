"""S1 host-only pairing. No HTTP approval, document or provider imports.

The current OS account is the trust boundary. Same-account malware and OS
administrators are not isolated by this channel. Unsupported controls deny startup.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import ctypes as C
import hashlib
import hmac
import json
import os
from pathlib import Path
import secrets
import socket
import stat
import struct
import threading
import time


class SecurityError(RuntimeError):
    def __init__(self):
        super().__init__("Local security prerequisite unavailable.")


def _require(value):
    if not value:
        raise SecurityError()
    return value


class Windows:
    """Explicit ctypes signatures; no default DACL or anonymous pipe fallback."""
    def __init__(self):
        self.k = C.WinDLL("kernel32", use_last_error=True)
        self.a = C.WinDLL("advapi32", use_last_error=True)
        p, d, b = C.c_void_p, C.c_ulong, C.c_int
        self.SA = type("SA", (C.Structure,), {"_fields_": [
            ("length", d), ("descriptor", p), ("inherit", b)]})
        specs = [
            (self.k, "GetCurrentProcess", p, []), (self.k, "GetCurrentThread", p, []),
            (self.k, "CloseHandle", b, [p]), (self.k, "LocalFree", p, [p]),
            (self.a, "OpenProcessToken", b, [p, d, C.POINTER(p)]),
            (self.a, "OpenThreadToken", b, [p, d, b, C.POINTER(p)]),
            (self.a, "GetTokenInformation", b, [p, b, p, d, C.POINTER(d)]),
            (self.a, "ConvertSidToStringSidW", b, [p, C.POINTER(p)]),
            (self.a, "ConvertStringSecurityDescriptorToSecurityDescriptorW", b,
             [C.c_wchar_p, d, C.POINTER(p), C.POINTER(d)]),
            (self.a, "GetNamedSecurityInfoW", d,
             [C.c_wchar_p, b, d, C.POINTER(p), p, C.POINTER(p), p, C.POINTER(p)]),
            (self.a, "GetSecurityInfo", d,
             [p, b, d, C.POINTER(p), p, C.POINTER(p), p, C.POINTER(p)]),
            (self.a, "SetFileSecurityW", b, [C.c_wchar_p, d, p]),
            (self.a, "GetSecurityDescriptorControl", b, [p, C.POINTER(C.c_ushort), C.POINTER(d)]),
            (self.a, "GetAclInformation", b, [p, p, d, b]),
            (self.a, "GetAce", b, [p, d, C.POINTER(p)]),
            (self.k, "CreateDirectoryW", b, [C.c_wchar_p, p]),
            (self.k, "CreateNamedPipeW", p, [C.c_wchar_p, d, d, d, d, d, d, p]),
            (self.k, "ConnectNamedPipe", b, [p, p]),
            (self.k, "DisconnectNamedPipe", b, [p]),
            (self.k, "CreateFileW", p, [C.c_wchar_p, d, d, p, d, d, p]),
            (self.k, "SetNamedPipeHandleState", b, [p, C.POINTER(d), p, p]),
            (self.k, "ReadFile", b, [p, p, d, C.POINTER(d), p]),
            (self.k, "WriteFile", b, [p, p, d, C.POINTER(d), p]),
            (self.a, "ImpersonateNamedPipeClient", b, [p]),
            (self.a, "RevertToSelf", b, []),
        ]
        for dll, name, result, args in specs:
            function = getattr(dll, name)
            function.restype, function.argtypes = result, args
        self.sid = self.token_sid()

    def sid_string(self, pointer):
        text = C.c_void_p()
        _require(self.a.ConvertSidToStringSidW(pointer, C.byref(text)))
        try:
            return C.wstring_at(text)
        finally:
            self.k.LocalFree(text)

    def token_sid(self, thread=False):
        handle, size = C.c_void_p(), C.c_ulong()
        if thread:
            _require(self.a.OpenThreadToken(self.k.GetCurrentThread(), 8, True, C.byref(handle)))
        else:
            _require(self.a.OpenProcessToken(self.k.GetCurrentProcess(), 8, C.byref(handle)))
        try:
            self.a.GetTokenInformation(handle, 1, None, 0, C.byref(size))
            buffer = C.create_string_buffer(size.value)
            _require(self.a.GetTokenInformation(handle, 1, buffer, size, C.byref(size)))
            return self.sid_string(C.cast(buffer, C.POINTER(C.c_void_p))[0])
        finally:
            self.k.CloseHandle(handle)

    def descriptor(self):
        descriptor = C.c_void_p()
        _require(self.a.ConvertStringSecurityDescriptorToSecurityDescriptorW(
            f"O:{self.sid}D:P(A;;GA;;;{self.sid})", 1, C.byref(descriptor), None))
        return descriptor

    def verify_owner(self, path):
        owner, descriptor = C.c_void_p(), C.c_void_p()
        _require(self.a.GetNamedSecurityInfoW(str(path), 1, 1, C.byref(owner), None,
                                            None, None, C.byref(descriptor)) == 0)
        try:
            _require(owner.value and self.sid_string(owner) == self.sid)
        finally:
            self.k.LocalFree(descriptor)

    def verify_acl(self, path=None, handle=None):
        owner, acl, descriptor = C.c_void_p(), C.c_void_p(), C.c_void_p()
        if path is not None:
            error = self.a.GetNamedSecurityInfoW(str(path), 1, 5, C.byref(owner), None,
                                                C.byref(acl), None, C.byref(descriptor))
        else:
            error = self.a.GetSecurityInfo(handle, 1, 5, C.byref(owner), None,
                                           C.byref(acl), None, C.byref(descriptor))
        _require(error == 0)
        try:
            _require(owner.value and acl.value and self.sid_string(owner) == self.sid)
            info = (C.c_ulong * 3)()
            _require(self.a.GetAclInformation(acl, info, C.sizeof(info), 2) and info[0] == 1)
            ace = C.c_void_p()
            _require(self.a.GetAce(acl, 0, C.byref(ace)))
            _require(C.c_ubyte.from_address(ace.value).value == 0)
            _require(self.sid_string(ace.value + 8) == self.sid)
            mask = C.c_ulong.from_address(ace.value + 4).value
            _require(mask & 0x10000000 or mask & 0x1F01FF == 0x1F01FF)
        finally:
            self.k.LocalFree(descriptor)


def _windows():
    _require(os.name == "nt")
    return Windows()


def safe_path(path: Path, *, directory=False):
    path = Path(path).absolute()
    for part in (path, *path.parents):
        item = part.lstat()
        _require(not stat.S_ISLNK(item.st_mode) and not getattr(item, "st_file_attributes", 0) & 0x400)
    item = path.stat()
    _require(stat.S_ISDIR(item.st_mode) if directory else stat.S_ISREG(item.st_mode))
    if not directory:
        safe_path(path.parent, directory=True)
    if os.name == "nt":
        _windows().verify_acl(path=path)
    else:
        _require(item.st_uid == os.getuid() and item.st_mode & 0o077 == 0)
    return path


def restrict_owned(path: Path):
    """Provision permissions only on an already owned path; never follow a link."""
    path = Path(path).absolute()
    _require(not path.is_symlink() and not getattr(path.lstat(), "st_file_attributes", 0) & 0x400)
    if os.name == "nt":
        win = _windows()
        win.verify_owner(path)
        descriptor = win.descriptor()
        try:
            _require(win.a.SetFileSecurityW(str(path), 0x80000004, descriptor))
        finally:
            win.k.LocalFree(descriptor)
    else:
        _require(path.stat().st_uid == os.getuid())
        path.chmod(0o700 if path.is_dir() else 0o600)
    return safe_path(path, directory=path.is_dir())


def create_private_dir(path: Path):
    path = Path(path).absolute()
    safe_path(path.parent, directory=True)
    if os.name == "nt":
        win = _windows()
        descriptor = win.descriptor()
        attributes = win.SA(C.sizeof(win.SA), descriptor, False)
        try:
            _require(win.k.CreateDirectoryW(str(path), C.byref(attributes)))
        finally:
            win.k.LocalFree(descriptor)
    else:
        path.mkdir(mode=0o700)
    return safe_path(path, directory=True)


def write_private(path: Path, value: dict):
    safe_path(path.parent, directory=True)
    descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
        json.dump(value, stream)
    restrict_owned(path)


def read_private(path: Path):
    safe_path(path.parent, directory=True)
    safe_path(path)
    _require(path.stat().st_size <= 4096)
    return json.loads(path.read_text(encoding="utf-8"))


def _encode(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _mac(key, value):
    return hmac.new(bytes.fromhex(key), _encode(value), hashlib.sha256).hexdigest()


class PairingControl:
    def __init__(self, root: Path, approve, revoke, *, clock=time.monotonic):
        safe_path(root, directory=True)
        self.root, self.approve, self.revoke, self.clock = root, approve, revoke, clock
        self.instance, self.key = secrets.token_hex(32), secrets.token_hex(32)
        self.address = (rf"\\.\pipe\aiip-s1-{self.instance}" if os.name == "nt"
                        else str(root / "pair.sock"))
        self.stopping, self.ready = threading.Event(), threading.Event()
        self.shutdown_requested = threading.Event()
        self.error = False

    def start(self):
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        _require(self.ready.wait(5) and not self.error)
        return self

    def stop(self):
        self.stopping.set()
        self.thread.join(6)
        _require(not self.thread.is_alive())

    def _exchange(self, read, write, peer):
        nonce, deadline = secrets.token_hex(32), self.clock() + 5
        write(_encode({"instance": self.instance, "nonce": nonce}) + b"\n")
        raw = read()
        _require(peer() and self.clock() < deadline and len(raw) <= 4096)
        value = json.loads(raw)
        _require(set(value) == {"instance", "nonce", "action", "selector", "mac"})
        signature = value.pop("mac")
        _require(value["instance"] == self.instance and value["nonce"] == nonce
                 and type(signature) is str and hmac.compare_digest(signature, _mac(self.key, value)))
        _require(value["action"] in {"approve", "revoke-all", "shutdown"} and type(value["selector"]) is str)
        _require(len(value["selector"]) <= 64)
        _require(value["action"] == "approve" or value["selector"] == "")
        accepted = self.approve(value["selector"]) if value["action"] == "approve" else self.revoke()
        write(_encode({"accepted": bool(accepted)}) + b"\n")
        _require(read() == b"done")  # Do not discard an unread Windows pipe response.
        if value["action"] == "shutdown":
            self.shutdown_requested.set()

    def _run(self):
        try:
            if os.name == "nt":
                self._pipe_server()
            else:
                self._unix_server()
        except Exception:
            self.error = True
            self.ready.set()

    def _unix_server(self):
        _require(hasattr(socket, "SO_PEERCRED"))
        listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        inode = None
        try:
            listener.bind(self.address)
            os.chmod(self.address, 0o600)
            item = Path(self.address).lstat()
            _require(stat.S_ISSOCK(item.st_mode) and item.st_uid == os.getuid() and item.st_mode & 0o077 == 0)
            inode = item.st_ino
            listener.listen(2)
            listener.settimeout(0.1)
            self.ready.set()
            while not self.stopping.is_set():
                try:
                    connection, _ = listener.accept()
                except socket.timeout:
                    continue
                with connection:
                    connection.settimeout(0.2)
                    try:
                        peer = lambda: struct.unpack("3i", connection.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, 12))[1] == os.getuid()
                        _require(peer())
                        self._exchange(lambda: _socket_read(connection, self.stopping), connection.sendall, peer)
                    except Exception:
                        pass  # No client data, credential, path or exception logged.
        finally:
            listener.close()
            path = Path(self.address)
            if inode is not None and path.exists() and path.lstat().st_ino == inode:
                path.unlink()

    def _pipe_server(self):
        win = _windows()
        descriptor = win.descriptor()
        attributes = win.SA(C.sizeof(win.SA), descriptor, False)
        handle = win.k.CreateNamedPipeW(self.address, 3 | 0x80000, 1 | 8, 1, 4096, 4096, 0, C.byref(attributes))
        win.k.LocalFree(descriptor)
        _require(handle not in {None, C.c_void_p(-1).value})
        try:
            win.verify_acl(handle=handle)
            self.ready.set()
            while not self.stopping.is_set():
                ok = win.k.ConnectNamedPipe(handle, None)
                error = C.get_last_error()
                if not ok and error not in {535}:
                    _require(error in {536, 232})
                    if error == 232:
                        win.k.DisconnectNamedPipe(handle)
                    time.sleep(0.01)
                    continue
                try:
                    def peer():
                        _require(win.a.ImpersonateNamedPipeClient(handle))
                        try:
                            return win.token_sid(thread=True) == win.sid
                        finally:
                            _require(win.a.RevertToSelf())
                    self._exchange(lambda: _pipe_read(win, handle, self.stopping),
                                   lambda value: _pipe_write(win, handle, value), peer)
                except Exception:
                    pass
                finally:
                    win.k.DisconnectNamedPipe(handle)
        finally:
            win.k.CloseHandle(handle)


def _socket_read(connection, stopping):
    result, deadline = bytearray(), time.monotonic() + 5
    while not stopping.is_set() and time.monotonic() < deadline:
        try:
            part = connection.recv(4097 - len(result))
        except socket.timeout:
            continue
        _require(part)
        result.extend(part)
        _require(len(result) <= 4096)
        if b"\n" in result:
            _require(result.endswith(b"\n") and result.count(b"\n") == 1)
            return bytes(result[:-1])
    raise SecurityError()


def _pipe_read(win, handle, stopping):
    result, deadline = bytearray(), time.monotonic() + 5
    while not stopping.is_set() and time.monotonic() < deadline:
        buffer, count = C.create_string_buffer(4097 - len(result)), C.c_ulong()
        ok = win.k.ReadFile(handle, buffer, len(buffer), C.byref(count), None)
        if not ok:
            _require(C.get_last_error() in {232, 536})
        result.extend(buffer.raw[:count.value])
        _require(len(result) <= 4096)
        if b"\n" in result:
            _require(result.endswith(b"\n") and result.count(b"\n") == 1)
            return bytes(result[:-1])
        time.sleep(0.01)
    raise SecurityError()


def _pipe_write(win, handle, value):
    count = C.c_ulong()
    _require(len(value) <= 4096 and win.k.WriteFile(handle, value, len(value), C.byref(count), None)
             and count.value == len(value))


@contextmanager
def _connection(config):
    if os.name == "nt":
        win = _windows()
        deadline = time.monotonic() + 5
        while True:
            handle = win.k.CreateFileW(config["address"], 0xC0000000, 0, None, 3, 0, None)
            if handle not in {None, C.c_void_p(-1).value}:
                break
            _require(C.get_last_error() == 231 and time.monotonic() < deadline)
            time.sleep(0.01)
        _require(handle not in {None, C.c_void_p(-1).value})
        try:
            win.verify_acl(handle=handle)
            mode = C.c_ulong(1)
            _require(win.k.SetNamedPipeHandleState(handle, C.byref(mode), None, None))
            yield (lambda: _pipe_read(win, handle, threading.Event()),
                   lambda value: _pipe_write(win, handle, value))
        finally:
            win.k.CloseHandle(handle)
    else:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
            connection.settimeout(0.2)
            connection.connect(config["address"])
            _require(struct.unpack("3i", connection.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, 12))[1] == os.getuid())
            yield (lambda: _socket_read(connection, threading.Event()), connection.sendall)


def request_control(config, selector="", action="approve", *, key=None, instance=None):
    """Used by the actual operator CLI and trusted host tests, never by HTTP."""
    with _connection(config) as (read, write):
        challenge = json.loads(read())
        _require(challenge["instance"] == config["instance"])
        message = {"instance": instance or config["instance"], "nonce": challenge["nonce"],
                   "action": action, "selector": selector}
        write(_encode({**message, "mac": _mac(key or config["control_key"], message)}) + b"\n")
        accepted = json.loads(read())["accepted"] is True
        write(b"done\n")
        return accepted


def main():
    parser = argparse.ArgumentParser(description="S1 protected local operator control")
    parser.add_argument("action", choices=["approve", "revoke-all", "shutdown", "check-private"])
    parser.add_argument("paths", nargs="+")
    args = parser.parse_args()
    try:
        if args.action == "check-private":
            for value in args.paths:
                safe_path(Path(value))
            return 0
        _require(len(args.paths) == (2 if args.action == "approve" else 1))
        config = read_private(Path(args.paths[0]))
        _require(request_control(config, args.paths[1] if args.action == "approve" else "", args.action))
        print("Operator action accepted.")
        return 0
    except Exception:
        print("Operator action unavailable.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
