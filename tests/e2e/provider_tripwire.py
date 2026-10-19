"""Test-process-only provider and network tripwire. Never import in product code."""

from __future__ import annotations

import asyncio
import ipaddress
import os
import socket
from contextlib import ExitStack, contextmanager
from unittest.mock import patch


class ProviderTripwireViolation(RuntimeError):
    """Intentionally non-disclosing denial of a forbidden test operation."""

    def __init__(self) -> None:
        super().__init__("preapi_tripwire_blocked")


def sanitize_provider_environment() -> None:
    """Remove credentials inside the isolated backend subprocess without logging values."""
    for name in tuple(os.environ):
        if name.startswith("OPENAI_") and any(
            marker in name for marker in ("KEY", "TOKEN", "SECRET", "CREDENTIAL")
        ):
            os.environ.pop(name, None)
    os.environ["RUN_OPENAI_LIVE_TESTS"] = "0"
    os.environ["RUN_OPENAI_DRAFT_LIVE_TESTS"] = "0"


def _loopback(destination: object, family: int | None = None) -> bool:
    if hasattr(socket, "AF_UNIX") and family == socket.AF_UNIX:
        return True
    host = destination[0] if isinstance(destination, tuple) and destination else destination
    if not isinstance(host, str):
        return False
    if host.lower().rstrip(".") == "localhost":
        return True
    try:
        return ipaddress.ip_address(host.split("%", 1)[0]).is_loopback
    except ValueError:
        return False


class ProviderTripwire:
    """Deny actual adapter/SDK creation and non-loopback transport before I/O.

    Install only inside isolated test processes. The normal and deliberate
    negative-probe accounting streams are distinct. No destination is logged.
    """

    def __init__(self) -> None:
        self.unexpected_provider_client_attempts = 0
        self.unexpected_egress_attempts = 0
        self.negative_tripwire_blocked_attempts = 0
        self.provider_api_requests = 0
        self._negative_probe = False
        self._patches: ExitStack | None = None

    def _deny(self, kind: str) -> None:
        if self._negative_probe:
            self.negative_tripwire_blocked_attempts += 1
        elif kind == "client":
            self.unexpected_provider_client_attempts += 1
        else:
            self.unexpected_egress_attempts += 1
        raise ProviderTripwireViolation()

    @contextmanager
    def negative_probe(self):
        if self._negative_probe:
            raise AssertionError("nested negative probe")
        self._negative_probe = True
        try:
            yield
        finally:
            self._negative_probe = False

    def snapshot(self) -> dict[str, int]:
        return {
            "provider_api_requests": self.provider_api_requests,
            "unexpected_provider_client_attempts": self.unexpected_provider_client_attempts,
            "unexpected_egress_attempts": self.unexpected_egress_attempts,
            "negative_tripwire_blocked_attempts": self.negative_tripwire_blocked_attempts,
        }

    def assert_no_unexpected_activity(self) -> None:
        if (self.unexpected_provider_client_attempts or self.unexpected_egress_attempts
                or self.provider_api_requests):
            raise AssertionError("preapi_unexpected_provider_activity")

    def install(self) -> "ProviderTripwire":
        if self._patches is not None:
            raise RuntimeError("tripwire_already_installed")

        # Import first, then replace the exact names resolved by create_app and
        # both real runtimes; never build a real SDK client as part of the patch.
        import openai
        from backend.app import main
        from backend.app.services import draft_runtime, extraction_runtime

        original_connect = socket.socket.connect
        original_connect_ex = socket.socket.connect_ex
        original_sendto = socket.socket.sendto
        original_getaddrinfo = socket.getaddrinfo
        original_async_connection = asyncio.BaseEventLoop.create_connection
        original_async_datagram = asyncio.BaseEventLoop.create_datagram_endpoint

        def connect(sock, address):
            if not _loopback(address, sock.family):
                self._deny("egress")
            return original_connect(sock, address)

        def connect_ex(sock, address):
            if not _loopback(address, sock.family):
                self._deny("egress")
            return original_connect_ex(sock, address)

        def sendto(sock, data, *args):
            if args and not _loopback(args[-1], sock.family):
                self._deny("egress")
            return original_sendto(sock, data, *args)

        def getaddrinfo(host, *args, **kwargs):
            if not _loopback(host):
                self._deny("egress")
            return original_getaddrinfo(host, *args, **kwargs)

        async def async_connection(loop, protocol_factory, host=None, port=None, *args, **kwargs):
            # Windows Proactor bypasses Python socket.connect for async I/O.
            if host is not None and not _loopback(host):
                self._deny("egress")
            return await original_async_connection(
                loop, protocol_factory, host, port, *args, **kwargs
            )

        async def async_datagram(loop, protocol_factory, *args, **kwargs):
            remote = kwargs.get("remote_addr")
            if remote is not None and not _loopback(remote):
                self._deny("egress")
            return await original_async_datagram(loop, protocol_factory, *args, **kwargs)

        def blocked_client(*_args, **_kwargs):
            self._deny("client")

        stack = ExitStack()
        try:
            for module, name in (
                (main, "OpenAIExtractionRuntime"),
                (main, "OpenAIDraftRuntime"),
                (extraction_runtime, "OpenAIExtractionRuntime"),
                (draft_runtime, "OpenAIDraftRuntime"),
                (extraction_runtime, "OpenAI"),
                (draft_runtime, "OpenAI"),
                (openai, "OpenAI"),
                (openai, "AsyncOpenAI"),
            ):
                stack.enter_context(patch.object(module, name, blocked_client))
            stack.enter_context(patch.object(socket.socket, "connect", connect))
            stack.enter_context(patch.object(socket.socket, "connect_ex", connect_ex))
            stack.enter_context(patch.object(socket.socket, "sendto", sendto))
            stack.enter_context(patch.object(socket, "getaddrinfo", getaddrinfo))
            stack.enter_context(patch.object(asyncio.BaseEventLoop, "create_connection", async_connection))
            stack.enter_context(patch.object(asyncio.BaseEventLoop, "create_datagram_endpoint", async_datagram))
            if os.name == "nt":
                from asyncio.proactor_events import BaseProactorEventLoop
                original_proactor_sock_connect = BaseProactorEventLoop.sock_connect

                async def proactor_sock_connect(loop, sock, address):
                    if not _loopback(address, sock.family):
                        self._deny("egress")
                    return await original_proactor_sock_connect(loop, sock, address)

                stack.enter_context(
                    patch.object(BaseProactorEventLoop, "sock_connect", proactor_sock_connect)
                )
        except BaseException:
            stack.close()
            raise
        self._patches = stack
        return self

    def close(self) -> None:
        if self._patches is not None:
            self._patches.close()
            self._patches = None

    def __enter__(self) -> "ProviderTripwire":
        return self.install()

    def __exit__(self, *_exc_info) -> None:
        self.close()
