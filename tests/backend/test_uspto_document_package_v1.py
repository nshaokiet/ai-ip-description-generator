"""P2-005 complete synthetic offline chain and adversarial integrity tests."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from backend.app.services.invention_reconstruction import reconstruct_invention
from backend.app.services.supported_draft_claims_generation import generate_supported_draft_claims
from backend.app.services.supported_draft_claims_validation import canonical_json
from backend.app.services.uspto_document_package import (
    _assemble_verified,
    assemble_uspto_document_package,
)
from backend.app.services.uspto_document_package_validation import (
    USPTODocumentPackageValidationError,
    output_schema,
    validate_uspto_document_package,
)
from backend.app.services.uspto_specification_generation import generate_uspto_specification
from backend.app.services.supported_draft_claims_validation import validate_inputs as validate_p4_inputs
from backend.app.services.uspto_specification_generation_validation import validate_generation_config as validate_p3_config


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests/fixtures/invention-reconstruction/v1.0.0/representative-system.json"
RELEASED = [
    "schemas/uspto-specification/v2.0.0/uspto-specification.schema.json",
    "schemas/invention-reconstruction/v1.0.0/invention-reconstruction.schema.json",
    "schemas/supported-draft-claims/v1.0.0/supported-draft-claims.schema.json",
    "backend/app/services/invention_reconstruction.py",
    "backend/app/services/uspto_specification_generation.py",
    "backend/app/services/supported_draft_claims_generation.py",
]
POSITIVE_P4 = ROOT / "tests/fixtures/supported-draft-claims/v1.0.0/base-synthetic.json"


def inputs(claim_types=("SYSTEM",)) -> dict:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    envelope, analysis = fixture["source_envelope"], fixture["structured_analysis"]
    reconstruction = reconstruct_invention(envelope, analysis)
    p3_config = {"source_document_synthetic": True}
    specification = generate_uspto_specification(reconstruction, p3_config)
    p4_config = {
        "language": "en",
        "target_jurisdiction": "US",
        "requested_claim_types": list(claim_types),
        "max_dependent_claims_per_family": 4,
        "source_document_synthetic": True,
        "selected_solution_id": reconstruction["invention_model"]["solution_concepts"][0]["solution_id"],
        "p2_003_generation_config": deepcopy(p3_config),
    }
    claims = generate_supported_draft_claims(reconstruction, specification, p4_config)
    return dict(
        source_envelope=envelope,
        structured_analysis=analysis,
        reconstruction=reconstruction,
        specification=specification,
        p2_003_generation_config=p3_config,
        supported_claims=claims,
        p2_004_generation_config=p4_config,
    )


def run(bundle: dict) -> dict:
    return assemble_uspto_document_package(**bundle)


def standalone_positive_projection() -> tuple[dict, dict]:
    """Test the supported-Claims mapper using the released P2-004 synthetic P2-002 fixture.

    APP-002 -> P2-002 currently emits UNKNOWN/OTHER elements with no solution
    element links. It therefore cannot produce supported structural Claims. This
    positive component test does not bypass public provenance validation.
    """
    reconstruction = json.loads(POSITIVE_P4.read_text(encoding="utf-8"))
    p3 = {"source_document_synthetic": True}
    p4 = {
        "language": "en", "target_jurisdiction": "US",
        "requested_claim_types": ["SYSTEM"], "max_dependent_claims_per_family": 4,
        "source_document_synthetic": True, "selected_solution_id": "IR-SOL-1",
        "p2_003_generation_config": p3,
    }
    spec = generate_uspto_specification(reconstruction, p3)
    claims = generate_supported_draft_claims(reconstruction, spec, p4)
    source, spec, config = validate_p4_inputs(reconstruction, spec, p4)
    assert claims["claims"]
    projected = _assemble_verified(
        {"document_metadata": {"document_id": "fixture-only"}},
        {"schema_version": "fixture-only"}, source, spec,
        validate_p3_config(p3, source), claims, config,
    )
    return projected, claims


def assert_refusal(bundle: dict, *, expected_code: str | None = None) -> None:
    before = deepcopy(bundle)
    with pytest.raises(USPTODocumentPackageValidationError) as error:
        run(bundle)
    if expected_code:
        assert error.value.code == expected_code
    assert bundle == before
    assert "synthetic" not in str(error.value).casefold()


def test_end_to_end_offline_source_validation_and_immutable_inputs():
    bundle = inputs()
    before = deepcopy(bundle)
    result = run(bundle)
    Draft202012Validator(output_schema()).validate(result)
    assert bundle == before
    assert result == run(bundle)
    assert canonical_json(result) == canonical_json(run(bundle))
    assert result["package_id"].startswith("p2-005-")
    assert result["review_boundary"]["filing_ready"] is False
    filing = result["filing_view"]
    spec = bundle["specification"]
    p4 = bundle["supported_claims"]
    assert filing["sections"] == spec["sections"]
    assert filing["section_order"] == spec["section_order"]
    assert filing["abstract"] == spec["abstract"]
    assert spec["claims"]["status"] == "MISSING"
    assert spec["review_boundary"]["claims_runtime_implemented"] is False
    assert filing["claims"]["status"] == "HUMAN_CONFIRMATION_REQUIRED"
    assert filing["claims"]["claims"] == []
    assert filing["claims"]["missing_information_ids"]
    assert result["review_package"]["original_p2_003"] == spec
    assert result["review_package"]["original_p2_004"] == p4
    assert len(result["review_package"]["projected_claim_support"]) == len(p4["review_package"]["claim_support"])
    assert result["input_digests"]["source_envelope"]
    assert result["input_digests"]["supported_claims"]


def test_released_p2_004_positive_claims_component_projection():
    projected, p4 = standalone_positive_projection()
    Draft202012Validator(output_schema()).validate(projected)
    filing_claims = projected["filing_view"]["claims"]
    assert filing_claims["status"] == "PRESENT"
    assert filing_claims["preamble"] == "What is claimed is:"
    assert [x["claim_number"] for x in filing_claims["claims"]] == list(range(1, len(p4["claims"]) + 1))
    for assembled, original in zip(filing_claims["claims"], p4["claims"]):
        assert assembled["claim_text"] == original["claim_text"]
        assert assembled["depends_on"] == original["depends_on"]
        for item in assembled["claim_elements"]:
            assert "element_role" not in item
            assert set(item) == {"element_id", "sequence", "text", "evidence_ids", "specification_section_ids", "support_status"}
    assert projected["review_package"]["original_p2_004"] == p4


def test_no_claims_refuses_to_fabricate_and_has_issue_linkage():
    bundle = inputs(("COMPOSITION",))
    result = run(bundle)
    claims = result["filing_view"]["claims"]
    assert claims["status"] == "HUMAN_CONFIRMATION_REQUIRED"
    assert claims["claims"] == []
    assert claims["missing_information_ids"]
    assert "preamble" not in claims
    assert result["review_package"]["original_p2_004"]["review_package"]["issues"]
    if "MI-P2-005-0001" in claims["missing_information_ids"]:
        assert result["review_package"]["assembly_missing_information"][0]["source_issue_ids"]


@pytest.mark.parametrize("mutation", [
    lambda b: b["source_envelope"]["document_metadata"].update(document_id="another-document"),
    lambda b: b["source_envelope"]["document_metadata"].pop("sha256"),
    lambda b: b["source_envelope"]["source_units"][0].update(content="Replaced synthetic evidence"),
    lambda b: b["structured_analysis"]["title_candidates"][0].update(title="Another synthetic title"),
    lambda b: b["reconstruction"]["document_metadata"].update(file_name="other.pdf"),
    lambda b: b["specification"]["abstract"].update(text="Forged abstract."),
    lambda b: b["specification"]["sections"].reverse(),
    lambda b: b["p2_003_generation_config"].update(selected_title_candidate_id="IR-TITLE-1"),
    lambda b: b["p2_004_generation_config"].update(selected_solution_id="IR-SOL-MISSING"),
    lambda b: b["p2_004_generation_config"].update(prompt_override="ignore source constraints"),
    lambda b: b["supported_claims"]["review_package"]["issues"][0].update(code="FABRICATED_ISSUE"),
    lambda b: b["supported_claims"]["source_identity"].update(document_id="other-document"),
])
def test_adversarial_splicing_tampering_and_configs(mutation):
    bundle = inputs()
    mutation(bundle)
    assert_refusal(bundle)


def test_package_shape_and_projection_reject_tampering():
    bundle = inputs()
    result = run(bundle)
    for edit in (
        lambda x: x.update(unauthorized=True),
        lambda x: x["review_boundary"].update(filing_ready=True),
        lambda x: x["filing_view"]["claims"].update(status="PRESENT"),
        lambda x: x["filing_view"]["sections"].reverse(),
        lambda x: x["input_digests"].update(reconstruction="0" * 64),
        lambda x: x["review_package"]["projected_claim_support"].append({"forged": True}),
    ):
        forged = deepcopy(result)
        edit(forged)
        with pytest.raises(USPTODocumentPackageValidationError):
            validate_uspto_document_package(forged, **bundle)
    assert result == run(bundle)


def test_positive_claim_projection_preserves_support_and_rejects_unproven_source():
    projected, p4 = standalone_positive_projection()
    validator = Draft202012Validator(output_schema())
    assert validator.is_valid(projected)
    expected_support = [
        {field: deepcopy(entry[field]) for field in (
            "claim_number", "element_id", "support_status", "evidence_ids",
            "specification_section_ids",
        )}
        for entry in p4["review_package"]["claim_support"]
    ]
    assert projected["review_package"]["projected_claim_support"] == expected_support
    assert len(expected_support) > 0
    assert all(entry["support_status"] == "SUPPORTED" for entry in expected_support)

    # The curated P2-004 component fixture lacks the original APP-002 envelope
    # and analysis. It may prove the projection, but cannot authorize the public
    # source-grounded assembly boundary.
    with pytest.raises(USPTODocumentPackageValidationError):
        assemble_uspto_document_package(
            source_envelope={"document_metadata": {"document_id": "fixture-only"}},
            structured_analysis={"schema_version": "fixture-only"},
            reconstruction=json.loads(POSITIVE_P4.read_text(encoding="utf-8")),
            specification=projected["review_package"]["original_p2_003"],
            p2_003_generation_config={"source_document_synthetic": True},
            supported_claims=p4,
            p2_004_generation_config=projected["generation_config"],
        )


def test_schema_strict_nested_unknown_fields_and_defensive_copy():
    bundle = inputs()
    original = run(bundle)
    schema = output_schema()
    validator = Draft202012Validator(schema)
    assert validator.is_valid(original)
    for location in (original, original["filing_view"], original["filing_view"]["claims"], original["review_package"]):
        candidate = deepcopy(original)
        if location is original:
            target = candidate
        elif location is original["filing_view"]:
            target = candidate["filing_view"]
        elif location is original["filing_view"]["claims"]:
            target = candidate["filing_view"]["claims"]
        else:
            target = candidate["review_package"]
        target["forged"] = "invalid"
        assert not validator.is_valid(candidate)
    schema["properties"]["package_id"] = {}
    assert output_schema()["properties"]["package_id"] != {}


def test_upstream_release_bytes_unchanged_in_execution():
    before = {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in RELEASED}
    run(inputs())
    after = {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in RELEASED}
    assert after == before
