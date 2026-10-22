"""PREAPI-D offline preflight. It never creates a provider client or request."""

from __future__ import annotations

import argparse
import importlib
import importlib.metadata
import json
import re
from pathlib import Path
from typing import Mapping

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

from backend.app.core.config import (
    OPENAI_DRAFT_MAX_RETRIES, OPENAI_DRAFT_MODEL, OPENAI_MAX_RETRIES,
    OPENAI_EXTRACTION_MODEL, Settings,
)
from backend.app.services.draft_runtime import DRAFT_PROMPT_PATH, DRAFT_SCHEMA_PATH, SOURCE_SCHEMA_PATH
from backend.app.services.extraction_runtime import CANONICAL_PROMPT_PATH, CANONICAL_SCHEMA_PATH


ROOT = Path(__file__).resolve().parents[1]
MODEL_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
CONFIG_FIELDS = (
    ("OPENAI_TIMEOUT_SECONDS", "openai_timeout_seconds", 180),
    ("OPENAI_MAX_OUTPUT_TOKENS", "openai_max_output_tokens", 48_000),
    ("OPENAI_DRAFT_TIMEOUT_SECONDS", "openai_draft_timeout_seconds", 240),
    ("OPENAI_DRAFT_MAX_OUTPUT_TOKENS", "openai_draft_max_output_tokens", 64_000),
)


def inspect_offline(environment: Mapping[str, str], *, root: Path = ROOT) -> dict:
    """Inspect local static prerequisites without reading credential contents into output."""
    checks: dict[str, str] = {}
    try:
        required = next(
            line.strip().split("==", 1)[1]
            for line in (root / "backend" / "requirements.txt").read_text(encoding="utf-8").splitlines()
            if line.strip().startswith("openai==")
        )
        installed = importlib.metadata.version("openai")
        checks["sdk_pin"] = "PASS" if installed == required else "BLOCKED"
    except (OSError, StopIteration, importlib.metadata.PackageNotFoundError):
        installed = "NOT_INSTALLED"
        checks["sdk_pin"] = "BLOCKED"
    try:
        sdk = importlib.import_module("openai")
        checks["sdk_import"] = "PASS" if hasattr(sdk, "OpenAI") else "BLOCKED"
    except ImportError:
        checks["sdk_import"] = "BLOCKED"

    for label, path in (
        ("extraction_prompt", CANONICAL_PROMPT_PATH),
        ("draft_prompt", DRAFT_PROMPT_PATH),
    ):
        try:
            checks[label] = "PASS" if path.read_text(encoding="utf-8").strip() else "BLOCKED"
        except OSError:
            checks[label] = "BLOCKED"
    for label, path in (
        ("analysis_schema", CANONICAL_SCHEMA_PATH),
        ("draft_source_schema", SOURCE_SCHEMA_PATH),
        ("draft_schema", DRAFT_SCHEMA_PATH),
    ):
        try:
            Draft202012Validator.check_schema(json.loads(path.read_text(encoding="utf-8")))
            checks[label] = "PASS"
        except (OSError, ValueError, TypeError, SchemaError):
            checks[label] = "BLOCKED"

    checks["model_identifier_syntax"] = (
        "PASS" if all(MODEL_ID.fullmatch(model) for model in
                      (OPENAI_EXTRACTION_MODEL, OPENAI_DRAFT_MODEL)) else "BLOCKED"
    )
    checks["retry_ceiling"] = (
        "PASS" if 0 <= OPENAI_MAX_RETRIES <= 2 and 0 <= OPENAI_DRAFT_MAX_RETRIES <= 2 else "BLOCKED"
    )
    try:
        values = {field: int(environment.get(name, str(default))) for name, field, default in CONFIG_FIELDS}
        Settings(storage_root=root / "_offline_preflight_unused", **values)
        checks["timeouts_and_token_caps"] = "PASS"
    except (TypeError, ValueError):
        checks["timeouts_and_token_caps"] = "BLOCKED"
    checks["live_flags_off"] = (
        "PASS" if environment.get("RUN_OPENAI_LIVE_TESTS", "0") == "0"
        and environment.get("RUN_OPENAI_DRAFT_LIVE_TESTS", "0") == "0" else "BLOCKED"
    )

    # Do not include, hash, truncate, log or interpolate the credential value.
    credential_status = "PRESENT" if bool(environment.get("OPENAI_API_KEY", "").strip()) else "ABSENT"
    return {
        "report_version": "0.1.0", "task_id": "PREAPI-D", "mode": "OFFLINE_ONLY",
        "checks": checks, "sdk_version": installed,
        "credential_status": credential_status,
        "readiness": "READY_FOR_AUTHORIZED_PROVIDER_SMOKE" if all(
            value == "PASS" for value in checks.values()
        ) else "BLOCKED",
        "provider_execution": "NOT_RUN", "model_entitlement": "UNVERIFIED",
        "tripwire_verification": "TEST_SUITE_ONLY",
        "product_runtime": "NOT_DETERMINED", "provider_authorization": "NOT_GRANTED",
        "provider_budget_usd": 0,
        "future_live_budget_enforcement": "NOT_IMPLEMENTED",
    }


def main() -> int:
    import os

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-out", type=Path, help="Optional report path")
    args = parser.parse_args()
    report = inspect_offline(os.environ)
    output = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.json_out:
        args.json_out.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0 if report["readiness"] == "READY_FOR_AUTHORIZED_PROVIDER_SMOKE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
