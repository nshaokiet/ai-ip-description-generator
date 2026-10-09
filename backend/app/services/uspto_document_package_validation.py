"""Offline integrity and strict business validation for P2-005 packages.

Only released upstream validators and synthetic APP-002/AI-001 inputs are
accepted. Errors deliberately never include source text or unknown field names.
"""
from __future__ import annotations

import json
from copy import deepcopy
from functools import lru_cache
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from backend.app.schemas.analysis_input import ExtractionInputEnvelope
from backend.app.services.invention_reconstruction import reconstruct_invention
from backend.app.services.supported_draft_claims_validation import (
    SupportedDraftClaimsValidationError,
    canonical_json,
    validate_inputs as validate_claims_inputs,
    validate_supported_draft_claims,
)
from backend.app.services.uspto_specification_generation_validation import (
    USPTOGenerationValidationError,
    validate_generation_config as validate_p2_003_config,
)


SCHEMA_PATH = (
    Path(__file__).resolve().parents[3]
    / "schemas/uspto-document-package/v1.0.0/uspto-document-package.schema.json"
)


class USPTODocumentPackageValidationError(ValueError):
    """Content-safe, stable validation error with contract paths only."""

    def __init__(self, code: str, *, paths: tuple[str, ...] = ()) -> None:
        self.code = code
        self.paths = tuple(sorted(set(paths)))
        self.safe_message = "Offline USPTO document package validation failed."
        super().__init__(self.safe_message)


@lru_cache(maxsize=1)
def _schema() -> dict[str, Any]:
    value = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(value)
    return value


def output_schema() -> dict[str, Any]:
    """Provide a mutation-isolated copy of the version-pinned contract."""
    return deepcopy(_schema())


def validate_assembly_inputs(
    *,
    source_envelope: Any,
    structured_analysis: Any,
    reconstruction: Any,
    specification: Any,
    p2_003_generation_config: Any,
    supported_claims: Any,
    p2_004_generation_config: Any,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any],
           dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Validate exact original source projection and both released draft stages."""
    try:
        envelope = ExtractionInputEnvelope.model_validate(source_envelope)
        canonical_envelope = envelope.model_dump(mode="json")
        canonical_analysis = deepcopy(structured_analysis)
        expected_reconstruction = reconstruct_invention(envelope, canonical_analysis)
    except Exception:
        raise USPTODocumentPackageValidationError(
            "INVALID_SOURCE_PROVENANCE", paths=("/source_envelope", "/structured_analysis")
        ) from None
    if reconstruction != expected_reconstruction:
        raise USPTODocumentPackageValidationError(
            "RECONSTRUCTION_PROJECTION_MISMATCH", paths=("/reconstruction",)
        )
    try:
        source, spec, canonical_config = validate_claims_inputs(
            reconstruction, specification, p2_004_generation_config
        )
        p2_config = validate_p2_003_config(p2_003_generation_config, source)
        if p2_config != canonical_config["p2_003_generation_config"]:
            raise USPTODocumentPackageValidationError(
                "P2_003_CONFIG_MISMATCH", paths=("/p2_003_generation_config",)
            )
        validate_supported_draft_claims(supported_claims, source, spec, canonical_config)
    except USPTODocumentPackageValidationError:
        raise
    except (SupportedDraftClaimsValidationError, USPTOGenerationValidationError):
        raise USPTODocumentPackageValidationError(
            "UPSTREAM_CONTRACT_INVALID", paths=("/reconstruction", "/specification", "/supported_claims")
        ) from None
    return (
        canonical_envelope,
        canonical_analysis,
        source,
        spec,
        deepcopy(p2_config),
        deepcopy(supported_claims),
        deepcopy(canonical_config),
    )


def validate_uspto_document_package(
    package: Any,
    *,
    source_envelope: Any,
    structured_analysis: Any,
    reconstruction: Any,
    specification: Any,
    p2_003_generation_config: Any,
    supported_claims: Any,
    p2_004_generation_config: Any,
) -> None:
    """Independently reproject the supplied inputs and compare the whole package."""
    from backend.app.services.uspto_document_package import _assemble_verified

    verified = validate_assembly_inputs(
        source_envelope=source_envelope,
        structured_analysis=structured_analysis,
        reconstruction=reconstruction,
        specification=specification,
        p2_003_generation_config=p2_003_generation_config,
        supported_claims=supported_claims,
        p2_004_generation_config=p2_004_generation_config,
    )
    try:
        errors = list(Draft202012Validator(_schema()).iter_errors(package))
    except Exception:
        raise USPTODocumentPackageValidationError("INVALID_PACKAGE_SCHEMA", paths=("/package",)) from None
    if errors:
        # Keep paths fixed, independent of source content or injected keys.
        raise USPTODocumentPackageValidationError("INVALID_PACKAGE_SCHEMA", paths=("/package",))
    expected = _assemble_verified(*verified)
    if package != expected:
        raise USPTODocumentPackageValidationError("PACKAGE_PROJECTION_MISMATCH", paths=("/package",))
    # Canonical JSON also rejects NaN/Infinity and non-JSON values.
    try:
        canonical_json(package)
    except SupportedDraftClaimsValidationError:
        raise USPTODocumentPackageValidationError("INVALID_PACKAGE_SCHEMA", paths=("/package",)) from None
