from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from backend.app.core.config import Settings
from backend.app.main import create_app


class HealthEndpointTests(unittest.TestCase):
    def test_health_returns_exact_contract(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            app = create_app(Settings(storage_root=Path(directory)))
            with TestClient(app) as client:
                response = client.get("/health")
        self.assertEqual(200, response.status_code)
        self.assertEqual({"status": "ok"}, response.json())
        self.assertNotIn("access-control-allow-origin", response.headers)


if __name__ == "__main__":
    unittest.main()

