"""Tests for AI-RUNTIME-002 Checkpoint A: Config boundaries and runtime skeleton."""

import os
from unittest import mock
import pytest

from backend.app.core.config import Settings
from backend.app.services.draft_runtime import run_draft_generation


def test_extraction_config_remains_unchanged():
    """Verify existing extraction policy limits are not altered by the draft config."""
    # Ensure no environment variables are bleeding in
    with mock.patch.dict(os.environ, {}, clear=True):
        settings = Settings.from_environment()

    # 1. Extraction timeout default remains 180 seconds.
    assert settings.openai_timeout_seconds == 180
    # 2. Extraction max output remains 48,000.
    assert settings.openai_max_output_tokens == 48_000

    # 3. Draft timeout default is 240 seconds.
    assert settings.openai_draft_timeout_seconds == 240
    # 4. Draft max output is 64,000.
    assert settings.openai_draft_max_output_tokens == 64_000


def test_draft_settings_do_not_override_extraction():
    """5. Draft environment settings do not override extraction settings."""
    env = {
        "OPENAI_DRAFT_TIMEOUT_SECONDS": "300",
        "OPENAI_DRAFT_MAX_OUTPUT_TOKENS": "60000",
    }
    with mock.patch.dict(os.environ, env, clear=True):
        settings = Settings.from_environment()

    assert settings.openai_draft_timeout_seconds == 300
    assert settings.openai_draft_max_output_tokens == 60000
    
    # Extraction should be completely untouched
    assert settings.openai_timeout_seconds == 180
    assert settings.openai_max_output_tokens == 48_000


def test_extraction_settings_do_not_override_draft():
    """6. Extraction environment settings do not override Draft settings."""
    env = {
        "OPENAI_TIMEOUT_SECONDS": "90",
        "OPENAI_MAX_OUTPUT_TOKENS": "10000",
    }
    with mock.patch.dict(os.environ, env, clear=True):
        settings = Settings.from_environment()

    assert settings.openai_timeout_seconds == 90
    assert settings.openai_max_output_tokens == 10000

    # Draft should be completely untouched
    assert settings.openai_draft_timeout_seconds == 240
    assert settings.openai_draft_max_output_tokens == 64_000


def test_invalid_draft_config_rejected():
    """7. Invalid Draft timeout/token configuration is rejected according to explicit bounds."""
    # Test valid bounds first via instantiation
    # max allowed draft tokens is 64000
    _ = Settings(storage_root=".", openai_draft_max_output_tokens=64000, openai_draft_timeout_seconds=600)
    
    # Exceed max output tokens
    with pytest.raises(ValueError, match="openai_draft_max_output_tokens must be between 1 and the approved 64000"):
        Settings(storage_root=".", openai_draft_max_output_tokens=64001)
        
    # Exceed max timeout
    with pytest.raises(ValueError, match="openai_draft_timeout_seconds must be between 30 and 600"):
        Settings(storage_root=".", openai_draft_timeout_seconds=601)

    # Below min timeout
    with pytest.raises(ValueError, match="openai_draft_timeout_seconds must be between 30 and 600"):
        Settings(storage_root=".", openai_draft_timeout_seconds=29)

    # Below min tokens
    with pytest.raises(ValueError, match="openai_draft_max_output_tokens must be between 1 and the approved 64000"):
        Settings(storage_root=".", openai_draft_max_output_tokens=0)


def test_draft_runtime_skeleton_cannot_accidentally_perform_call():
    """9. Draft Runtime skeleton cannot accidentally perform an OpenAI call."""
    # It must raise NotImplementedError before doing anything else
    with pytest.raises(NotImplementedError, match="is a skeleton for Checkpoint A"):
        run_draft_generation(source_analysis={"fake": "data"})
