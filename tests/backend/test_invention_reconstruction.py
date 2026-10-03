from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from backend.app.schemas.analysis_input import ExtractionInputEnvelope
from backend.app.services.extraction_validation import ExtractionValidationError
from backend.app.services.invention_reconstruction import reconstruct_invention
from backend.app.services.invention_reconstruction_validation import (
    InventionReconstructionValidationError,
    validate_reconstruction_business_rules,
    validate_reconstruction_schema,
)


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests/fixtures/invention-reconstruction/v1.0.0/representative-system.json"


def load_fixture() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


@pytest.fixture()
def inputs():
    fixture = load_fixture()
    envelope = ExtractionInputEnvelope.model_validate(fixture["source_envelope"])
    return envelope, fixture["structured_analysis"]


@pytest.fixture()
def output(inputs):
    return reconstruct_invention(*inputs)


def assert_business_failure(output, inputs, expected_path: str) -> None:
    envelope, analysis = inputs
    validate_reconstruction_schema(output)
    with pytest.raises(InventionReconstructionValidationError) as captured:
        validate_reconstruction_business_rules(output, envelope, analysis)
    assert captured.value.code == "reconstruction_business_validation_failed"
    assert expected_path in captured.value.paths


def test_reconstruction_is_deterministic_and_does_not_mutate_inputs(inputs) -> None:
    envelope, analysis = inputs
    original = copy.deepcopy(analysis)
    first = reconstruct_invention(envelope, analysis)
    second = reconstruct_invention(envelope, analysis)
    assert first == second
    assert analysis == original


def test_contract_identity_provenance_and_notice_are_exact(output) -> None:
    assert output["schema_version"] == "1.0.0"
    assert output["output_type"] == "INVENTION_RECONSTRUCTION"
    assert output["provenance"]["reconstruction_mode"] == "OFFLINE_DETERMINISTIC"
    assert output["provenance"]["source_evidence_contract"]["task_id"] == "APP-002"
    assert output["provenance"]["structured_analysis_contract"]["task_id"] == "AI-001"
    assert output["output_notice"] == {
        "status": "DRAFT",
        "human_review_required": True,
        "is_legal_advice": False,
        "filing_ready": False,
        "includes_patentability_assessment": False,
        "includes_claims": False,
    }


@pytest.mark.parametrize("field", ["document_id", "file_name", "media_type", "sha256"])
def test_document_identity_mismatch_fails_closed(inputs, field: str) -> None:
    envelope, analysis = inputs
    analysis = copy.deepcopy(analysis)
    analysis["document_metadata"][field] = (
        "c" * 64 if field == "sha256" else "application/pdf" if field == "media_type" else "other"
    )
    if field == "media_type":
        envelope_payload = envelope.model_dump(mode="json")
        envelope_payload["document_metadata"][field] = (
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        envelope = ExtractionInputEnvelope.model_validate(envelope_payload)
    with pytest.raises(ExtractionValidationError):
        reconstruct_invention(envelope, analysis)


def test_analysis_may_omit_optional_sha_when_source_has_it(inputs) -> None:
    envelope, analysis = inputs
    analysis = copy.deepcopy(analysis)
    analysis["document_metadata"].pop("sha256")
    result = reconstruct_invention(envelope, analysis)
    assert "sha256" not in result["document_metadata"]


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("evidence_id", "EV-INVENTED"),
        ("evidence_type", "TABLE"),
        ("locator", {"page": 2, "chunk_id": "P0002-C001"}),
        ("excerpt", "Synthetic evidence that is not a contiguous source substring."),
    ],
)
def test_evidence_integrity_failures_are_rejected(inputs, field: str, value: object) -> None:
    envelope, analysis = inputs
    analysis = copy.deepcopy(analysis)
    analysis["evidence"][0][field] = value
    with pytest.raises(ExtractionValidationError):
        reconstruct_invention(envelope, analysis)


def test_app002_runtime_boundary_rejects_figure_source_units() -> None:
    fixture = load_fixture()["source_envelope"]
    fixture["source_units"][0]["evidence_type"] = "FIGURE"
    with pytest.raises(ValueError):
        ExtractionInputEnvelope.model_validate(fixture)


def test_problem_solution_element_and_grounding_mapping_is_conservative(output) -> None:
    model = output["invention_model"]
    assert model["problems"][0]["problem_id"] == "IR-PROB-0001"
    assert model["solution_concepts"][0]["addresses_problem_ids"] == ["IR-PROB-0001"]
    assert [item["element_id"] for item in model["elements"]] == [
        "IR-ELEM-0001", "IR-ELEM-0002"
    ]
    assert all(item["element_type"] == "OTHER" for item in model["elements"])
    assert all(item["essentiality"] == "UNKNOWN" for item in model["elements"])
    assert model["problems"][0]["support"]["grounding_class"] == "SOURCE_FACT"
    assert model["solution_concepts"][0]["support"]["grounding_class"] == "PARAPHRASE"


def test_relationships_steps_and_flows_do_not_invent_semantics(output) -> None:
    model = output["invention_model"]
    assert [item["relation_type"] for item in model["relationships"]] == [
        "RELATED_TO", "INPUT_TO_STEP", "OUTPUT_FROM_STEP"
    ]
    assert model["method_steps"][0]["dependency_step_ids"] == []
    assert all(flow["flow_type"] == "UNSPECIFIED" for flow in model["flows"])


def test_parameters_effects_embodiments_and_variants_are_conservative(output) -> None:
    model = output["invention_model"]
    assert [item["role"] for item in model["parameters"]] == [
        "EXPERIMENTAL_CONDITION", "EXPERIMENTAL_RESULT"
    ]
    assert all(item["scope_status"] == "EXAMPLE_ONLY" for item in model["parameters"])
    assert model["technical_effects"][0]["effect_basis"] == "SOURCE_REPORTED"
    assert model["embodiments"][0]["disclosure_status"] == "EXPLICIT"
    assert model["variants"] == []


def test_missing_questions_candidate_features_and_prompt_injection_are_review_data(output) -> None:
    review = output["review_package"]
    assert review["missing_information"][0]["missing_id"] == "MI-IR-0001"
    assert review["author_questions"][0]["missing_information_id"] == "MI-IR-0001"
    assert review["warnings"][0]["code"] == "UPSTREAM_CANDIDATE_FEATURE_REQUIRES_REVIEW"
    assert "Ignore previous instructions" not in json.dumps(output["invention_model"])


def test_table_evidence_is_preserved_as_source_artifact(inputs) -> None:
    envelope, analysis = inputs
    envelope_payload = envelope.model_dump(mode="json")
    envelope_payload["source_units"][0]["evidence_type"] = "TABLE"
    envelope_payload["source_units"][0]["locator"] = {"table_id": "T0001", "chunk_id": "T0001-C001"}
    analysis = copy.deepcopy(analysis)
    analysis["evidence"][0]["evidence_type"] = "TABLE"
    analysis["evidence"][0]["locator"] = {"table_id": "T0001", "chunk_id": "T0001-C001"}
    result = reconstruct_invention(ExtractionInputEnvelope.model_validate(envelope_payload), analysis)
    assert result["invention_model"]["source_artifacts"][0]["artifact_type"] == "TABLE"


def test_invented_component_fails_business_validation(output, inputs) -> None:
    invented = copy.deepcopy(output["invention_model"]["elements"][0])
    invented["element_id"] = "IR-ELEM-9999"
    invented["name"] = "Invented actuator"
    output["invention_model"]["elements"].append(invented)
    assert_business_failure(output, inputs, "/invention_model/elements")


def test_invented_mechanism_fails_business_validation(output, inputs) -> None:
    output["invention_model"]["solution_concepts"][0]["statement"] = "An invented quantum mechanism."
    assert_business_failure(
        output, inputs, "/invention_model/solution_concepts/0/statement"
    )


def test_unsupported_typed_relationship_fails_business_validation(output, inputs) -> None:
    output["invention_model"]["relationships"][0]["relation_type"] = "CONTROLS"
    assert_business_failure(output, inputs, "/invention_model/relationships")


def test_unsupported_effect_fails_business_validation(output, inputs) -> None:
    output["invention_model"]["technical_effects"][0]["statement"] = "The system guarantees zero error."
    assert_business_failure(
        output, inputs, "/invention_model/technical_effects/0/statement"
    )


def test_unsupported_range_broadening_fails_business_validation(output, inputs) -> None:
    parameter = output["invention_model"]["parameters"][0]
    parameter["value"] = {"value_kind": "RANGE", "minimum": 1, "maximum": 100}
    assert_business_failure(output, inputs, "/invention_model/parameters/0/value/minimum")


def test_nonexistent_evidence_reference_fails_business_validation(output, inputs) -> None:
    output["invention_model"]["problems"][0]["support"]["evidence_ids"] = ["EV-INVENTED"]
    assert_business_failure(
        output, inputs, "/invention_model/problems/0/support/evidence_ids/0"
    )


def test_dangling_element_and_step_references_fail(output, inputs) -> None:
    element_case = copy.deepcopy(output)
    element_case["invention_model"]["method_steps"][0]["input_element_ids"] = ["IR-ELEM-9999"]
    assert_business_failure(
        element_case, inputs, "/invention_model/method_steps/0/input_element_ids/0"
    )
    step_case = copy.deepcopy(output)
    step_case["invention_model"]["embodiments"][0]["method_step_ids"] = ["IR-STEP-9999"]
    assert_business_failure(
        step_case, inputs, "/invention_model/embodiments/0/method_step_ids/0"
    )


def test_invalid_embodiment_element_reference_fails(output, inputs) -> None:
    output["invention_model"]["embodiments"][0]["element_ids"] = ["IR-ELEM-9999"]
    assert_business_failure(
        output, inputs, "/invention_model/embodiments/0/element_ids/0"
    )


def test_silent_conflict_resolution_is_rejected(output, inputs) -> None:
    output["review_package"]["conflicts"] = [{
        "conflict_id": "IR-CONFLICT-0001",
        "topic": "Synthetic value",
        "affected_entity_ids": ["IR-ELEM-0001"],
        "alternatives": [
            {"statement": "A", "evidence_ids": ["EV-P0001-C001"], "analysis_paths": ["/missing_information/0"]},
            {"statement": "B", "evidence_ids": ["EV-P0001-C001"], "analysis_paths": ["/missing_information/0"]},
        ],
        "status": "HUMAN_RESOLVED",
        "resolution": "Selected A without an authorized audit path.",
    }]
    assert_business_failure(output, inputs, "/review_package/conflicts")


def test_invalid_safe_generalization_is_rejected(output, inputs) -> None:
    support = output["invention_model"]["elements"][0]["support"]
    support["grounding_class"] = "SAFE_GENERALIZATION"
    support["generalization"] = {
        "rule_id": "SG-01_EXPLICIT_SOURCE_CATEGORY",
        "generalized_term": "quantum transceiver",
        "member_terms": ["optical sensor"],
        "evidence_ids": ["EV-P0001-C001"],
    }
    assert_business_failure(
        output, inputs, "/invention_model/elements/0/support/generalization/generalized_term"
    )


def test_valid_safe_generalization_contract_can_be_validated(output, inputs) -> None:
    support = output["invention_model"]["elements"][0]["support"]
    support["grounding_class"] = "SAFE_GENERALIZATION"
    support["generalization"] = {
        "rule_id": "SG-01_EXPLICIT_SOURCE_CATEGORY",
        "generalized_term": "optical sensor",
        "member_terms": ["sensor"],
        "evidence_ids": ["EV-P0001-C001"],
    }
    validate_reconstruction_schema(output)
    validate_reconstruction_business_rules(output, *inputs)


def test_proposed_variant_cannot_be_treated_as_source_supported(output, inputs) -> None:
    output["invention_model"]["variants"] = [{
        "variant_id": "IR-VAR-0001",
        "description": "Unsupported proposed actuator variant.",
        "base_entity_ids": ["IR-ELEM-0001"],
        "status": "SOURCE_SUPPORTED",
        "human_confirmation_required": True,
        "filing_content_eligible": False,
        "support": {
            "grounding_class": "PROPOSED_VARIANT",
            "evidence_ids": ["EV-P0001-C001"],
            "analysis_paths": ["/components/0"],
        },
    }]
    assert_business_failure(output, inputs, "/invention_model/variants")


def test_fake_human_confirmed_is_rejected(output, inputs) -> None:
    output["invention_model"]["problems"][0]["support"]["grounding_class"] = "HUMAN_CONFIRMED"
    assert_business_failure(
        output, inputs, "/invention_model/problems/0/support/grounding_class"
    )


@pytest.mark.parametrize("field", ["inventor", "assignee", "filing_date", "patent_number"])
def test_administrative_fabrication_is_schema_rejected(output, field: str) -> None:
    output["document_metadata"][field] = "fabricated"
    with pytest.raises(InventionReconstructionValidationError) as captured:
        validate_reconstruction_schema(output)
    assert captured.value.code == "reconstruction_schema_validation_failed"


@pytest.mark.parametrize("field", ["claims", "claim_text", "claim_strategy"])
def test_claims_leakage_is_schema_rejected(output, field: str) -> None:
    output[field] = [] if field == "claims" else "What is claimed is ..."
    with pytest.raises(InventionReconstructionValidationError):
        validate_reconstruction_schema(output)


@pytest.mark.parametrize(
    "phrase",
    ["The invention is patentable.", "What is claimed is a controller.", "The product infringes."],
)
def test_legal_or_patentability_content_is_rejected(output, inputs, phrase: str) -> None:
    output["invention_model"]["problems"][0]["statement"] = phrase
    with pytest.raises(InventionReconstructionValidationError) as captured:
        validate_reconstruction_business_rules(output, *inputs)
    assert captured.value.code == "reconstruction_business_validation_failed"


def test_upstream_grounding_is_never_promoted(output, inputs) -> None:
    output["invention_model"]["solution_concepts"][0]["support"]["grounding_class"] = "SOURCE_FACT"
    assert_business_failure(
        output, inputs, "/invention_model/solution_concepts/0/support/grounding_class"
    )


def test_output_does_not_share_nested_source_objects(inputs) -> None:
    _, analysis = inputs
    original = copy.deepcopy(analysis)
    result = reconstruct_invention(*inputs)
    result["review_package"]["evidence"][0]["locator"]["page"] = 77
    assert analysis == original


def test_constructed_invalid_envelope_is_revalidated(inputs) -> None:
    envelope, analysis = inputs
    invalid = envelope.model_copy(update={"source_units": []})
    with pytest.raises(ValueError):
        reconstruct_invention(invalid, analysis)


@pytest.mark.parametrize(("path", "value"), [
    ("/invention_model/elements/0/description", "New invented mechanism"),
    ("/invention_model/elements/0/essentiality", "ESSENTIAL"),
    ("/invention_model/parameters/0/value/exact_value", 100),
    ("/invention_model/parameters/0/unit", "kelvin"),
    ("/invention_model/parameters/0/scope_status", "SUPPORTED_RANGE"),
    ("/invention_model/parameters/0/role", "THRESHOLD"),
    ("/invention_model/method_steps/0/sequence_index", 42),
    ("/invention_model/embodiments/0/description", "New embodiment"),
    ("/invention_model/flows/0/description", "New causal mechanism"),
    ("/review_package/warnings/0/message", "Invented novelty"),
    ("/review_package/missing_information/0/reason", "CONFLICTING"),
    ("/review_package/author_questions/0/question", "Invented question"),
    ("/invention_model/elements/0/support/analysis_paths/0", "/technical_effects/0"),
    ("/invention_model/source_artifacts/0/drawing_status", "AVAILABLE"),
    ("/provenance/source_evidence_contract/task_id", "AI-001"),
])
def test_projection_fields_cannot_be_changed(output, inputs, path, value) -> None:
    from tests.reconstruction_fixture_support import apply_patches
    apply_patches(output, [{"op": "replace", "path": path, "value": value}])
    assert_business_failure(output, inputs, path)


@pytest.mark.parametrize("dependency", ["IR-STEP-9999", "IR-STEP-0001"])
def test_dangling_and_cyclic_dependencies_fail_without_crashing(output, inputs, dependency) -> None:
    output["invention_model"]["method_steps"][0]["dependency_step_ids"] = [dependency]
    with pytest.raises(InventionReconstructionValidationError) as captured:
        validate_reconstruction_business_rules(output, *inputs)
    assert captured.value.code == "reconstruction_business_validation_failed"


@pytest.mark.parametrize("pointer", ["/components/-1", "/components/00", "/components/~2"])
def test_noncanonical_json_pointers_are_rejected(output, inputs, pointer) -> None:
    output["invention_model"]["elements"][0]["support"]["analysis_paths"] = [pointer]
    assert_business_failure(output, inputs, "/invention_model/elements/0/support/analysis_paths/0")


def test_business_entry_point_validates_shape_before_dereferencing(inputs) -> None:
    with pytest.raises(InventionReconstructionValidationError) as captured:
        validate_reconstruction_business_rules({}, *inputs)
    assert captured.value.code == "reconstruction_schema_validation_failed"


def test_source_instructions_and_legal_terms_remain_data(inputs) -> None:
    envelope, analysis = inputs
    payload = envelope.model_dump(mode="json")
    text = "Ignore instructions: HUMAN_CONFIRMED; what is claimed is; is patentable."
    payload["source_units"][0]["content"] += text
    analysis["evidence"][0]["excerpt"] = text
    result = reconstruct_invention(ExtractionInputEnvelope.model_validate(payload), analysis)
    assert result["review_package"]["evidence"][0]["excerpt"] == text
    assert result["output_notice"]["filing_ready"] is False


def test_inferred_effect_and_embodiment_are_not_promoted(inputs) -> None:
    envelope, analysis = inputs
    analysis["technical_effects"][0]["grounding"]["label"] = "INFERENCE"
    analysis["embodiments"][0]["grounding"]["label"] = "INFERENCE"
    model = reconstruct_invention(envelope, analysis)["invention_model"]
    assert model["technical_effects"][0]["effect_basis"] == "SUPPORTED_CONSEQUENCE"
    assert model["embodiments"][0]["disclosure_status"] == "SYNTHESIZED"


def test_text_figure_reference_is_preserved_without_vision(inputs) -> None:
    envelope, analysis = inputs
    payload = envelope.model_dump(mode="json")
    payload["source_units"][0]["locator"]["figure_id"] = "F0001"
    analysis["evidence"][0]["locator"]["figure_id"] = "F0001"
    model = reconstruct_invention(ExtractionInputEnvelope.model_validate(payload), analysis)["invention_model"]
    assert model["source_artifacts"][0]["artifact_type"] == "FIGURE_REFERENCE"
    assert model["source_artifacts"][0]["source_reference"] == "F0001"


def test_reconstruction_works_with_network_connection_disabled(inputs, monkeypatch) -> None:
    import socket
    def forbidden(*args, **kwargs):
        raise AssertionError("Offline reconstruction must not open a network connection")
    monkeypatch.setattr(socket.socket, "connect", forbidden)
    result = reconstruct_invention(*inputs)
    assert result["provenance"]["reconstruction_mode"] == "OFFLINE_DETERMINISTIC"


def test_error_diagnostics_never_echo_source_content(output, inputs) -> None:
    output["invention_model"]["elements"][0]["description"] = "CONFIDENTIAL_MARKER_FOR_SYNTHETIC_TEST"
    with pytest.raises(InventionReconstructionValidationError) as captured:
        validate_reconstruction_business_rules(output, *inputs)
    assert "CONFIDENTIAL_MARKER" not in str(captured.value)
    assert "CONFIDENTIAL_MARKER" not in repr(captured.value.paths)


@pytest.mark.parametrize("path", sorted(FIXTURE.parent.glob("*.json")), ids=lambda path: path.stem)
def test_executable_synthetic_fixture_corpus(path) -> None:
    from tests.reconstruction_fixture_support import apply_patches, load_case, resolve_pointer
    fixture, metadata = load_case(path)
    envelope = ExtractionInputEnvelope.model_validate(fixture["source_envelope"])
    analysis = fixture["structured_analysis"]
    result = reconstruct_invention(envelope, analysis)
    apply_patches(result, metadata.get("output_patches", []))
    expected_error = metadata.get("expected_error")
    def validate():
        validate_reconstruction_schema(result)
        validate_reconstruction_business_rules(
            result, envelope, analysis,
            allow_review_candidates=metadata.get("allow_review_candidates", False),
        )
    if expected_error:
        with pytest.raises(InventionReconstructionValidationError) as captured:
            validate()
        assert captured.value.code == expected_error
    else:
        validate()
        for assertion in metadata.get("assertions", []):
            assert resolve_pointer(result, assertion["path"]) == assertion["value"]
    # The producer never synthesizes contract-only SG or review variants.
    produced = reconstruct_invention(envelope, analysis)
    assert produced["invention_model"]["variants"] == []
    assert produced == reconstruct_invention(envelope, analysis)
