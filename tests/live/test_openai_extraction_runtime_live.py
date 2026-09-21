from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from backend.app.core.config import Settings
from backend.app.services.extraction_runtime import OpenAIExtractionRuntime
from tests.backend.runtime_test_support import synthetic_envelope


@unittest.skipUnless(
    os.environ.get("RUN_OPENAI_LIVE_TESTS") == "1",
    "RUN_OPENAI_LIVE_TESTS is not enabled",
)
class OpenAIExtractionRuntimeLiveTests(unittest.TestCase):
    def test_synthetic_structured_extraction(self) -> None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            self.skipTest("OPENAI_API_KEY is not available")
        with tempfile.TemporaryDirectory() as directory:
            settings = Settings(
                storage_root=Path(directory),
                openai_api_key=api_key,
                openai_timeout_seconds=180,
                openai_max_output_tokens=48_000,
                run_openai_live_tests=True,
            )
            result = OpenAIExtractionRuntime(settings).run_extraction(synthetic_envelope())
        self.assertEqual("1.0.0", result.analysis["schema_version"])
        self.assertEqual("STRUCTURED_INVENTION_ANALYSIS", result.analysis["output_type"])
        self.assertEqual("completed", result.runtime.status)
        self.assertEqual("gpt-5.6-sol", result.runtime.model)


if __name__ == "__main__":
    unittest.main()
