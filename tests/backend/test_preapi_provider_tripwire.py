"""PREAPI-001-B: isolated provider tripwire negative probes and safe accounting."""

from __future__ import annotations

import asyncio
import os
import socket
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.app.core.config import Settings
from backend.app.main import create_app
from tests.e2e.provider_tripwire import (
    ProviderTripwire,
    ProviderTripwireViolation,
    sanitize_provider_environment,
)


class ProviderTripwireTests(unittest.TestCase):
    def test_missing_fakes_are_denied_before_actual_adapter_construction(self) -> None:
        with tempfile.TemporaryDirectory() as root, ProviderTripwire() as guard:
            settings = Settings(
                storage_root=Path(root) / "uploads",
                enable_local_orchestration_api=True,
                openai_api_key="synthetic-not-a-secret",
            )
            # Each missing fake would enter a real fallback without the guard.
            with guard.negative_probe():
                with self.assertRaisesRegex(ProviderTripwireViolation, "^preapi_tripwire_blocked$"):
                    create_app(settings, draft_runtime=object())
                with self.assertRaises(ProviderTripwireViolation):
                    create_app(settings, extraction_runtime=object())
            self.assertEqual(2, guard.negative_tripwire_blocked_attempts)
            guard.assert_no_unexpected_activity()
            self.assertEqual(0, guard.snapshot()["provider_api_requests"])

    def test_direct_sync_and_async_sdk_constructors_are_denied(self) -> None:
        from backend.app.services import draft_runtime, extraction_runtime
        import openai

        with ProviderTripwire() as guard:
            with guard.negative_probe():
                for constructor in (
                    extraction_runtime.OpenAI,
                    draft_runtime.OpenAI,
                    openai.OpenAI,
                    openai.AsyncOpenAI,
                ):
                    with self.assertRaises(ProviderTripwireViolation):
                        constructor(api_key="synthetic-not-a-secret")
            self.assertEqual(4, guard.negative_tripwire_blocked_attempts)
            guard.assert_no_unexpected_activity()

    def test_normal_fake_injection_has_zero_provider_activity(self) -> None:
        with tempfile.TemporaryDirectory() as root, ProviderTripwire() as guard:
            settings = Settings(
                storage_root=Path(root) / "uploads",
                enable_local_orchestration_api=True,
                openai_api_key="synthetic-not-a-secret",
            )
            app = create_app(
                settings, extraction_runtime=object(), draft_runtime=object()
            )
            with TestClient(app) as client:
                self.assertEqual(200, client.get("/health").status_code)
            self.assertEqual(
                {
                    "provider_api_requests": 0,
                    "unexpected_provider_client_attempts": 0,
                    "unexpected_egress_attempts": 0,
                    "negative_tripwire_blocked_attempts": 0,
                },
                guard.snapshot(),
            )

    def test_external_socket_dns_udp_and_async_paths_fail_closed(self) -> None:
        with ProviderTripwire() as guard, guard.negative_probe():
            with socket.socket() as stream:
                with self.assertRaises(ProviderTripwireViolation):
                    stream.connect(("203.0.113.10", 443))
                with self.assertRaises(ProviderTripwireViolation):
                    stream.connect_ex(("203.0.113.10", 443))
            with self.assertRaises(ProviderTripwireViolation):
                socket.getaddrinfo("api.openai.com", 443)
            with socket.socket(type=socket.SOCK_DGRAM) as udp:
                with self.assertRaises(ProviderTripwireViolation):
                    udp.sendto(b"probe", ("203.0.113.10", 53))

            async def probe() -> None:
                await asyncio.open_connection("203.0.113.10", 443)

            with self.assertRaises(ProviderTripwireViolation):
                asyncio.run(probe())
        self.assertEqual(5, guard.negative_tripwire_blocked_attempts)
        guard.assert_no_unexpected_activity()

    def test_loopback_transport_is_allowed_and_patches_are_scoped(self) -> None:
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            listener.listen(1)
            address = listener.getsockname()
            with ProviderTripwire() as guard:
                with socket.create_connection(address, timeout=2) as client:
                    accepted, _ = listener.accept()
                    accepted.close()
                    self.assertTrue(client.getpeername())
                guard.assert_no_unexpected_activity()
            self.assertEqual(0, guard.snapshot()["negative_tripwire_blocked_attempts"])

    def test_unexpected_attempts_are_fatal_even_when_caught(self) -> None:
        with ProviderTripwire() as guard:
            with self.assertRaises(ProviderTripwireViolation):
                socket.getaddrinfo("not-a-loopback.example", 443)
            self.assertEqual(1, guard.unexpected_egress_attempts)
            with self.assertRaisesRegex(AssertionError, "preapi_unexpected_provider_activity"):
                guard.assert_no_unexpected_activity()

    def test_subprocess_sanitization_and_safe_redacted_counters(self) -> None:
        with patch.dict(os.environ, {
            "OPENAI_API_KEY": "synthetic-not-a-secret",
            "OPENAI_TEST_TOKEN": "synthetic-not-a-secret",
            "RUN_OPENAI_LIVE_TESTS": "1",
            "RUN_OPENAI_DRAFT_LIVE_TESTS": "1",
        }):
            sanitize_provider_environment()
            self.assertNotIn("OPENAI_API_KEY", os.environ)
            self.assertNotIn("OPENAI_TEST_TOKEN", os.environ)
            self.assertEqual("0", os.environ["RUN_OPENAI_LIVE_TESTS"])
            self.assertEqual("0", os.environ["RUN_OPENAI_DRAFT_LIVE_TESTS"])

        guard = ProviderTripwire()
        self.assertEqual(
            {
                "provider_api_requests",
                "unexpected_provider_client_attempts",
                "unexpected_egress_attempts",
                "negative_tripwire_blocked_attempts",
            },
            set(guard.snapshot()),
        )
        self.assertEqual("preapi_tripwire_blocked", str(ProviderTripwireViolation()))


if __name__ == "__main__":
    unittest.main()
