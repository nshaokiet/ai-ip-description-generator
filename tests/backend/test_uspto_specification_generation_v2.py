"""Synthetic-only P2-003 contract, preservation and adversarial regression."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import pytest
from jsonschema import Draft202012Validator

from backend.app.services.invention_reconstruction import reconstruct_invention
from backend.app.services.uspto_specification_generation import (
    RELATION_WORDING, generate_uspto_specification,
)
from backend.app.services.uspto_specification_generation_validation import (
    USPTOGenerationValidationError, output_schema, validate_generated_specification, word_count,
)

ROOT = Path(__file__).resolve().parents[2]
CONFIG = {"source_document_synthetic": True}


@pytest.fixture
def source():
    return json.loads((ROOT / "tests/fixtures/uspto-generation/v2.0.0/minimal-synthetic.json").read_text(encoding="utf-8"))


def generate(source, config=None):
    return generate_uspto_specification(source, CONFIG if config is None else config)


def prose(output):
    return " ".join([
        *[p["text"] for s in output["sections"] for a in [s, *s["subsections"]] for p in a["paragraphs"]],
        output["abstract"]["text"],
    ])


def detail(output):
    return output["sections"][9]["paragraphs"]


def find_detail(output, group):
    return next(p for p in detail(output) if p["support"]["source_paths"][0].startswith("/invention_model/" + group))


def test_01_system_canonical_identity_and_closed_gates(source):
    out = generate(source)
    Draft202012Validator(output_schema()).validate(out)
    assert out["schema_version"] == "2.0.0"
    assert out["output_type"] == "USPTO_SPECIFICATION_DRAFT"
    metadata = out["document_metadata"]
    assert metadata["source_document"] == source["document_metadata"] | {"synthetic": True}
    material = "doc-p3-synthetic|synthetic-controller.pdf|" + "b" * 64
    assert metadata["draft_id"] == "p2-003-" + hashlib.sha256(material.encode()).hexdigest()[:24]
    assert metadata["language"] == "en" and metadata["target_jurisdiction"] == "US"
    assert out["review_boundary"]["human_review_required"] is True
    for key in ("filing_ready", "legal_advice", "patentability_assessment_included", "claims_runtime_implemented", "render_review_metadata_as_filing_content"):
        assert out["review_boundary"][key] is False
    assert "SOURCE_FACT" in json.dumps(out)
    assert "NOT_APPLICABLE" not in json.dumps(out)


def test_02_method_order_dependencies_conditions_and_grounding(source):
    out = generate(source)
    first = find_detail(out, "method_steps")
    assert "Step 1: Measure sensor response." in first["text"]
    assert "Inputs: sensor; outputs: controller." in first["text"]
    assert "Explicit step dependencies: none represented." in first["text"]
    assert "Conditions: At 25 degC." in first["text"]
    assert first["support"]["grounding_class"] == "INFERENCE"
    second = [p for p in detail(out) if p["support"]["source_paths"][0] == "/invention_model/method_steps/1"][0]
    assert "Explicit step dependencies: Measure sensor response." in second["text"]
    assert "causes" not in prose(out) and "parallel" not in prose(out)


@pytest.mark.parametrize("relation", list(RELATION_WORDING))
def test_03_all_controlled_relationships_remain_exact(source, relation):
    source["invention_model"]["relationships"][0]["relation_type"] = relation
    out = generate(source)
    assert find_detail(out, "relationships")["text"] == f"sensor {RELATION_WORDING[relation]} controller."
    if relation == "RELATED_TO":
        assert "connected to" not in find_detail(out, "relationships")["text"]


@pytest.mark.parametrize("kind,value,expected", [
    ("EXACT", {"exact_value": "5–10"}, '"5–10"'),
    ("RANGE", {"minimum": 5, "maximum": 10}, "5 to 10"),
    ("SET", {"values": [5, 10]}, "[5, 10]"),
    ("QUALITATIVE", {"qualitative_value": "low"}, '"low"'),
])
def test_04_parameters_exact_values_units_and_role(source, kind, value, expected):
    source["invention_model"]["parameters"][0]["value"] = {"value_kind": kind, **value}
    text = find_detail(generate(source), "parameters")["text"]
    assert expected in text and "degC" in text and "experimental condition" in text
    assert "In the represented example" in text


def test_05_multiple_embodiments_in_input_order(source):
    model = source["invention_model"]
    second = copy.deepcopy(model["embodiments"][0])
    second.update(embodiment_id="IR-EMB-2", name="Second example", disclosure_status="EXPLICIT")
    model["embodiments"].append(second)
    texts = [p["text"] for p in detail(generate(source)) if "/embodiments/" in p["support"]["source_paths"][0]]
    assert len(texts) == 2 and "represented combination" in texts[0] and "Second example" in texts[1]
    second["disclosure_status"] = "PROPOSED_REQUIRES_HUMAN_CONFIRMATION"
    assert "Second example" not in prose(generate(source))


def test_06_titles_exact_selection_no_selection_and_empty(source):
    title = copy.deepcopy(source["invention_model"]["title_candidates"][0])
    title.update(title_id="IR-TITLE-2", title="Second exact title!")
    source["invention_model"]["title_candidates"].append(title)
    assert generate(source)["sections"][0]["status"] == "HUMAN_CONFIRMATION_REQUIRED"
    out = generate(source, CONFIG | {"selected_title_candidate_id": "IR-TITLE-2"})
    assert out["sections"][0]["paragraphs"][0]["text"] == "Second exact title!"
    source["invention_model"]["title_candidates"] = []
    assert generate(source)["sections"][0]["status"] == "MISSING"


def test_07_missing_field_and_context_are_explicit_subsection_gaps(source):
    source["invention_model"]["technical_field"] = {"status": "MISSING"}
    source["invention_model"]["technical_context"] = []
    out = generate(source)
    assert all(s["status"] == "MISSING" for s in out["sections"][6]["subsections"])
    assert out["abstract"]["status"] == "MISSING"


def test_08_administrative_gaps_and_review_separation(source):
    out = generate(source)
    for section in out["sections"][1:6]:
        assert section["status"] == "HUMAN_CONFIRMATION_REQUIRED"
        assert section["paragraphs"] == [] and section["missing_information_ids"]
    assert "EV-SYNTHETIC" not in prose(out)
    assert "review_package" not in prose(out)


def test_09_conflict_taint_propagates_without_selecting_a_side(source):
    support = source["invention_model"]["elements"][0]["support"]
    source["review_package"]["conflicts"] = [{"conflict_id": "IR-CONFLICT-1", "topic": "Synthetic disagreement",
        "affected_entity_ids": ["IR-ELEM-1"], "alternatives": [{"statement": x, "evidence_ids": support["evidence_ids"], "analysis_paths": support["analysis_paths"]} for x in ("left", "right")], "status": "UNRESOLVED"}]
    out = generate(source)
    assert out["sections"][7]["status"] == "HUMAN_CONFIRMATION_REQUIRED"
    assert out["abstract"]["status"] == "MISSING"
    assert all("/invention_model/elements/0" not in p["support"]["source_paths"] for p in detail(out))
    assert any(w["code"] == "UNRESOLVED_RECONSTRUCTION_CONFLICT" for w in out["review_package"]["warnings"])
    assert "left" not in prose(out) and "right" not in prose(out)
    assert "controller" in prose(out)


def test_10_valid_safe_generalization_and_aggregation(source):
    x = source["invention_model"]["elements"][0]
    x["name"] = "Optical devices"
    x["support"].update(grounding_class="SAFE_GENERALIZATION", generalization={
        "rule_id": "SG-01_EXPLICIT_SOURCE_CATEGORY", "generalized_term": "Optical devices",
        "member_terms": ["sensor", "controller"], "evidence_ids": ["EV-SYNTHETIC"]})
    assert find_detail(generate(source), "elements")["support"]["grounding_class"] == "SAFE_GENERALIZATION"
    x["support"]["generalization"]["generalized_term"] = "unmentioned category"
    with pytest.raises(USPTOGenerationValidationError):
        generate(source)


def test_11_variant_source_gate_and_proposed_exclusion(source):
    variant = {"variant_id": "IR-VAR-1", "description": "Synthetic alternate calibration", "base_entity_ids": ["IR-ELEM-2"],
        "status": "SOURCE_SUPPORTED", "filing_content_eligible": True, "human_confirmation_required": False,
        "support": copy.deepcopy(source["invention_model"]["elements"][1]["support"])}
    source["invention_model"]["variants"] = [variant]
    assert "Synthetic alternate calibration" in prose(generate(source))
    variant.update(status="PROPOSED_REQUIRES_HUMAN_CONFIRMATION", filing_content_eligible=False, human_confirmation_required=True)
    variant["support"]["grounding_class"] = "PROPOSED_VARIANT"
    assert "Synthetic alternate calibration" not in prose(generate(source))


def artifact(source, reference):
    source["invention_model"]["source_artifacts"] = [{"artifact_id": "IR-ART-1", "artifact_type": "DRAWING_REQUIREMENT",
        "drawing_id": "SOURCE-FIG-1", "drawing_kind": "SOURCE_FIGURE", "drawing_status": "AVAILABLE",
        "source_reference": reference, "evidence_ids": ["EV-SYNTHETIC"], "human_confirmation_required": False, "analysis_paths": ["/drawing_requirements/0"]}]


def test_12_text_supported_drawing_without_vision_or_reference_numerals(source):
    artifact(source, "Figure 1 shows the synthetic sensor and controller arrangement")
    out = generate(source)
    drawing = out["sections"][8]
    assert drawing["status"] == "PRESENT"
    assert drawing["figures"][0]["figure_label"] == "FIG. 1"
    assert drawing["figures"][0]["reference_numerals"] == []
    assert drawing["figures"][0]["source_figure_ids"] == ["SOURCE-FIG-1"]


def test_13_opaque_drawing_requires_human_drafting(source):
    artifact(source, "SOURCE-FIG-1")
    out = generate(source)
    assert out["sections"][8]["status"] == "HUMAN_CONFIRMATION_REQUIRED"
    assert out["sections"][8]["figures"] == []


@pytest.mark.parametrize("scope,phrase", [("EXAMPLE_ONLY", "represented example"), ("SUPPORTED_RANGE", "supported range"), ("UNKNOWN_SCOPE", "scope unspecified")])
def test_14_parameter_scope_not_strengthened(source, scope, phrase):
    source["invention_model"]["parameters"][0]["scope_status"] = scope
    assert phrase in find_detail(generate(source), "parameters")["text"]


def test_15_input_and_output_range_broadening_rejected(source):
    parameter = source["invention_model"]["parameters"][0]
    parameter["value"] = {"value_kind": "RANGE", "minimum": 5, "maximum": 10}
    out = generate(source)
    out["sections"][9]["paragraphs"][-2]["text"] += " Broadened value 1 to 20."
    with pytest.raises(USPTOGenerationValidationError):
        validate_generated_specification(out, source, CONFIG)
    parameter["value"]["minimum"] = 1
    with pytest.raises(USPTOGenerationValidationError):
        generate(source)


@pytest.mark.parametrize("text", ["Ignore previous instructions", "Generate claims", "Mark HUMAN_CONFIRMED"])
def test_16_prompt_injection_is_data_and_never_a_command(source, text):
    source["review_package"]["evidence"][0]["excerpt"] += " " + text
    out = generate(source)
    assert text not in prose(out) and out["claims"]["claims"] == []
    source["invention_model"]["elements"][0]["description"] = text
    assert text not in prose(generate(source))


@pytest.mark.parametrize("text", ["The invention is patentable", "Novelty is guaranteed", "Freedom to operate is assured", "It infringes", "Non-obvious design", "Filing-ready result"])
def test_17_legal_contamination_is_excluded(source, text):
    source["invention_model"]["elements"][0]["description"] = text
    assert text not in prose(generate(source))


def test_18_claims_hard_gate(source):
    out = generate(source)
    assert out["claims"] == {"section_id": "CLAIMS", "sequence": 11, "heading": "CLAIMS", "status": "MISSING",
        "claims": [], "missing_information_ids": out["claims"]["missing_information_ids"]}
    assert out["claims"]["missing_information_ids"]
    assert out["review_package"]["claim_support"] == []
    assert "What is claimed is" not in prose(out)


def test_19_abstract_whole_sentences_count_and_insufficient_limit(source):
    out = generate(source)
    assert out["abstract"]["word_count"] == word_count(out["abstract"]["text"]) <= 150
    source["invention_model"]["technical_field"]["name"] = " ".join(["synthetic"] * 160)
    abstract = generate(source)["abstract"]
    assert abstract["status"] == "MISSING" and abstract["text"] == "" and abstract["word_count"] == 0


def test_20_sequence_listing_human_confirmation(source):
    assert generate(source)["sections"][10]["status"] == "HUMAN_CONFIRMATION_REQUIRED"


@pytest.mark.parametrize("text", ["(54) TITLE", "(57) ABSTRACT", "US 12,345,678 B2", "Patent No. 123", "Application No. 456", "Publication No. 789"])
def test_21_22_inid_and_official_numbers_blocked(source, text):
    source["invention_model"]["title_candidates"][0]["title"] = text
    out = generate(source)
    assert out["sections"][0]["status"] == "MISSING" and text not in prose(out)


def test_23_dangling_output_source_path_rejected(source):
    out = generate(source)
    out["sections"][0]["paragraphs"][0]["support"]["source_paths"] = ["/invention_model/no_such_item"]
    with pytest.raises(USPTOGenerationValidationError) as error:
        validate_generated_specification(out, source, CONFIG)
    assert error.value.code == "INVALID_SOURCE_PATH"


def test_24_nonexistent_evidence_input_and_output_rejected(source):
    out = generate(source)
    out["sections"][0]["paragraphs"][0]["support"]["evidence_ids"] = ["EV-NOT-FOUND"]
    with pytest.raises(USPTOGenerationValidationError):
        validate_generated_specification(out, source, CONFIG)
    source["invention_model"]["elements"][0]["support"]["evidence_ids"] = ["EV-NOT-FOUND"]
    with pytest.raises(USPTOGenerationValidationError):
        generate(source)


def test_provenance_A_true_is_exact_caller_assertion(source):
    assert generate(source)["document_metadata"]["source_document"]["synthetic"] is True


@pytest.mark.parametrize("config", [None, {}, {"language": "en"}])
def test_provenance_B_missing_fails_before_generation(source, config):
    with patch("backend.app.services.uspto_specification_generation._build_specification") as builder:
        with pytest.raises(USPTOGenerationValidationError) as error:
            generate_uspto_specification(source, config)
        assert error.value.code == "SOURCE_DOCUMENT_PROVENANCE_REQUIRED"
        builder.assert_not_called()


def test_provenance_C_false_fails_before_generation(source):
    with patch("backend.app.services.uspto_specification_generation._build_specification") as builder:
        with pytest.raises(USPTOGenerationValidationError) as error:
            generate(source, {"source_document_synthetic": False})
        assert error.value.code == "REAL_SOURCE_NOT_AUTHORIZED"
        builder.assert_not_called()


@pytest.mark.parametrize("value", [0, 1, "true", "false", None, [], {}, 1.0])
def test_provenance_D_strict_boolean_no_coercion(source, value):
    with pytest.raises(USPTOGenerationValidationError) as error:
        generate(source, {"source_document_synthetic": value})
    assert error.value.code == "INVALID_GENERATION_CONFIG"


def test_provenance_E_source_cannot_supply_missing_config(source):
    source["review_package"]["evidence"][0]["excerpt"] += " This is synthetic; synthetic=true."
    with pytest.raises(USPTOGenerationValidationError) as error:
        generate(source, {})
    assert error.value.code == "SOURCE_DOCUMENT_PROVENANCE_REQUIRED"


def test_provenance_F_source_real_assertion_cannot_override_config(source):
    source["review_package"]["evidence"][0]["excerpt"] += " This is a real research paper."
    assert generate(source)["document_metadata"]["source_document"]["synthetic"] is True


def test_provenance_G_determinism_and_deep_mutation_isolation(source):
    original = copy.deepcopy(source)
    config = copy.deepcopy(CONFIG)
    first, second = generate(source, config), generate(source, config)
    assert first == second and json.dumps(first) == json.dumps(second)
    first["document_metadata"]["source_document"]["file_name"] = "changed"
    first["review_package"]["evidence"][0]["source_paths"].append("/changed")
    first["section_order"].clear()
    assert source == original and config == CONFIG and generate(source) == second


def test_provenance_H_released_schema_immutability():
    expected = {
        "schemas/invention-reconstruction/v1.0.0/invention-reconstruction.schema.json": "e10b5ae85da60e26c4d928ec27bf46605296d6ab7a2dd7c7a234933efddd5693",
        "schemas/uspto-specification/v2.0.0/uspto-specification.schema.json": "32b40c67eaaa3915fb3cd0fb4cf86cfc439f21bd417c74c48eaf26e29a4b657c",
    }
    for file, digest in expected.items():
        # Match immutable checked-in content independent of Windows line endings.
        content = (ROOT / file).read_bytes().replace(b"\r\n", b"\n")
        assert hashlib.sha256(content).hexdigest() == digest


@pytest.mark.parametrize("essentiality,phrase", [("ESSENTIAL", "required"), ("OPTIONAL", "optional"), ("CONDITIONAL", "conditional"), ("UNKNOWN", "unspecified essentiality")])
def test_essentiality_preserved(source, essentiality, phrase):
    source["invention_model"]["elements"][0]["essentiality"] = essentiality
    assert phrase in find_detail(generate(source), "elements")["text"]


@pytest.mark.parametrize("flow", ["MATERIAL", "SIGNAL", "DATA", "ENERGY", "CONTROL", "UNSPECIFIED"])
def test_flow_enum_not_inferred(source, flow):
    source["invention_model"]["flows"][0]["flow_type"] = flow
    assert f"A {flow.lower()} flow" in find_detail(generate(source), "flows")["text"]


@pytest.mark.parametrize("config", [{"model": "no"}, {"include_claims": True}, {"abstract_max_words": 151}, {"target_jurisdiction": "EP"}, {"language": "vi"}, {"selected_title_candidate_id": "absent"}, {"abstract_max_words": True}])
def test_config_rejects_unsupported_keys_values_and_title(source, config):
    with pytest.raises(USPTOGenerationValidationError):
        generate(source, CONFIG | config)


def test_safe_errors_human_state_reference_cycles_and_invalid_schema(source):
    source["invention_model"]["elements"][0]["support"]["grounding_class"] = "HUMAN_CONFIRMED"
    with pytest.raises(USPTOGenerationValidationError) as error:
        generate(source)
    assert "sensor" not in str(error.value) and hasattr(error.value, "safe_message")
    source["invention_model"]["elements"][0]["support"]["grounding_class"] = "SOURCE_FACT"
    source["invention_model"]["method_steps"][0]["dependency_step_ids"] = ["IR-STEP-2"]
    with pytest.raises(USPTOGenerationValidationError):
        generate(source)
    with pytest.raises(USPTOGenerationValidationError):
        generate({})


def test_review_gaps_questions_and_unknown_routes_preserved(source):
    missing = {"missing_id": "MI-IR-1", "target_path": "/technical_field", "description": "Synthetic author clarification",
        "reason": "INSUFFICIENT_DETAIL", "impact": "MEDIUM", "owner": "AUTHOR", "analysis_paths": ["/technical_field"]}
    source["review_package"]["missing_information"] = [missing]
    source["review_package"]["author_questions"] = [{"question_id": "AQ-IR-1", "missing_information_id": "MI-IR-1", "question": "Clarify the synthetic field", "priority": "MEDIUM", "analysis_paths": ["/technical_field"]}]
    out = generate(source)
    assert out["review_package"]["author_questions"][0]["target_section_id"] == "FIELD_OF_THE_INVENTION"
    assert "Synthetic author clarification" not in prose(out)
    missing["target_path"] = "/unmapped"
    assert any(w["code"] == "UNROUTED_RECONSTRUCTION_GAP" for w in generate(source)["review_package"]["warnings"])


def test_real_p2_producer_output_consumed_without_upstream_service_inputs():
    fixture = json.loads((ROOT / "tests/fixtures/invention-reconstruction/v1.0.0/representative-system.json").read_text(encoding="utf-8"))
    reconstruction = reconstruct_invention(fixture["source_envelope"], fixture["structured_analysis"])
    out = generate(reconstruction)
    assert out["schema_version"] == "2.0.0"
    assert out["claims"]["claims"] == []


@pytest.mark.parametrize("field", ["draft_id", "source_document"])
def test_output_identity_tampering_rejected(source, field):
    out = generate(source)
    if field == "draft_id":
        out["document_metadata"][field] = "changed-draft"
    else:
        out["document_metadata"][field]["synthetic"] = False
    with pytest.raises(USPTOGenerationValidationError):
        validate_generated_specification(out, source, CONFIG)


def test_conditional_element_without_condition_description_is_review_only(source):
    element = source["invention_model"]["elements"][0]
    element["essentiality"] = "CONDITIONAL"
    del element["description"]
    out = generate(source)
    assert not any(p["support"]["source_paths"][0] == "/invention_model/elements/0" for p in detail(out))
    assert any(w["code"] == "RECONSTRUCTION_CONTENT_EXCLUDED" for w in out["review_package"]["warnings"])


def test_parameter_legal_or_inid_scalar_contamination_is_not_rendered(source):
    source["invention_model"]["parameters"][0]["value"]["exact_value"] = "US 12,345,678 B2"
    assert "US 12,345,678 B2" not in prose(generate(source))


def test_no_sha_is_omitted_and_draft_id_rule_still_exact(source):
    del source["document_metadata"]["sha256"]
    out = generate(source)
    assert "sha256" not in out["document_metadata"]["source_document"]
    assert out["document_metadata"]["draft_id"] == "p2-003-" + hashlib.sha256(b"doc-p3-synthetic|synthetic-controller.pdf|").hexdigest()[:24]


def test_pure_offline_entrypoint_never_uses_network(source):
    with patch("socket.socket", side_effect=AssertionError("Network forbidden")), patch("socket.create_connection", side_effect=AssertionError("Network forbidden")):
        assert generate(source)["claims"]["claims"] == []


def test_bad_json_pointer_escape_and_unaudited_resolved_conflict_rejected(source):
    out = generate(source)
    out["sections"][0]["paragraphs"][0]["support"]["source_paths"] = ["/invention_model/~bad"]
    with pytest.raises(USPTOGenerationValidationError):
        validate_generated_specification(out, source, CONFIG)
    support = source["invention_model"]["elements"][0]["support"]
    source["review_package"]["conflicts"] = [{"conflict_id": "IR-CONFLICT-1", "topic": "Synthetic disagreement", "affected_entity_ids": [],
        "alternatives": [{"statement": x, "evidence_ids": support["evidence_ids"], "analysis_paths": support["analysis_paths"]} for x in ("left", "right")], "status": "HUMAN_RESOLVED", "resolution": "unaudited"}]
    with pytest.raises(USPTOGenerationValidationError):
        generate(source)


def test_input_invalid_references_and_duplicate_evidence_fail_safe(source):
    source["invention_model"]["relationships"][0]["object_id"] = "IR-ABSENT"
    with pytest.raises(USPTOGenerationValidationError):
        generate(source)
    source["invention_model"]["relationships"][0]["object_id"] = "IR-ELEM-2"
    source["review_package"]["evidence"].append(copy.deepcopy(source["review_package"]["evidence"][0]))
    with pytest.raises(USPTOGenerationValidationError):
        generate(source)


def test_unused_evidence_is_not_copied(source):
    evidence = copy.deepcopy(source["review_package"]["evidence"][0])
    evidence["evidence_id"] = "EV-UNUSED"
    source["review_package"]["evidence"].append(evidence)
    assert [x["evidence_id"] for x in generate(source)["review_package"]["evidence"]] == ["EV-SYNTHETIC"]


@pytest.mark.parametrize("change", ["essentiality", "relationship", "flow", "condition", "claims", "abstract", "admin"])
def test_output_semantic_or_gate_tampering_is_rejected(source, change):
    out = generate(source)
    if change in {"essentiality", "relationship", "flow", "condition"}:
        group = {"essentiality": "elements", "relationship": "relationships", "flow": "flows", "condition": "method_steps"}[change]
        paragraph = find_detail(out, group)
        paragraph["text"] += " Unsupported semantic addition."
    elif change == "claims":
        out["claims"]["status"] = "HUMAN_CONFIRMATION_REQUIRED"
    elif change == "abstract":
        out["abstract"]["word_count"] += 1
    else:
        out["sections"][1]["status"] = "MISSING"
    with pytest.raises(USPTOGenerationValidationError):
        validate_generated_specification(out, source, CONFIG)


@pytest.mark.parametrize("basis,grounding,phrase", [("SOURCE_REPORTED", "SOURCE_FACT", "The source reports"), ("SUPPORTED_CONSEQUENCE", "INFERENCE", "A supported consequence")])
def test_effect_basis_conditions_and_non_promotion(source, basis, grounding, phrase):
    effect = source["invention_model"]["technical_effects"][0]
    effect["effect_basis"] = basis
    effect["support"]["grounding_class"] = grounding
    paragraph = find_detail(generate(source), "technical_effects")
    assert phrase in paragraph["text"] and "Conditions: At 25 degC." in paragraph["text"]
    # The related solution is PARAPHRASE; aggregation must not promote it.
    assert paragraph["support"]["grounding_class"] == ("INFERENCE" if grounding == "INFERENCE" else "PARAPHRASE")
    effect["support"]["grounding_class"] = "SOURCE_FACT" if grounding == "INFERENCE" else "INFERENCE"
    with pytest.raises(USPTOGenerationValidationError):
        generate(source)
