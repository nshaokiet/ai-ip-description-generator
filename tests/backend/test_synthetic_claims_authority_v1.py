from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import hashlib
import inspect
import json
from pathlib import Path

import pytest

from backend.app.services.supported_draft_claims_generation import generate_supported_draft_claims
from backend.app.services.synthetic_claims_authority_v1 import (
    AuthorityContext,
    SyntheticAuthorityError,
    canonical_digest,
    context_from_reconstruction,
    evaluate_family_authority,
    inspect_preliminary_composition,
    inspect_preliminary_method,
    make_authority_assertion,
    make_overlay,
    make_synthetic_decision,
    validate_overlay,
)
from backend.app.services.uspto_document_package_validation import validate_assembly_inputs
from backend.app.services.uspto_offline_orchestration import PROVENANCE_KEYS
from backend.app.services.uspto_specification_generation import generate_uspto_specification


ROOT = Path(__file__).resolve().parents[2]
RECONSTRUCTION = ROOT / "tests/fixtures/supported-draft-claims/v1.0.0/base-synthetic.json"
CANDIDATES = ROOT / "tests/fixtures/synthetic-claims-authority/v1.0.0/candidate-semantics.json"
EVIDENCE_ID = "EV-SYNTHETIC"
TIMESTAMP = "2026-10-15T09:00:00Z"


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _context(source: dict | None = None) -> AuthorityContext:
    return context_from_reconstruction(
        _json(RECONSTRUCTION) if source is None else source,
        session_id="synthetic-session-003",
        revision=7,
        revision_token="rev-7-synthetic-authority",
    )


def _candidate_data() -> dict:
    return _json(CANDIDATES)


def _overlay(
    entries: list[tuple[str, dict[str, str], str]],
    *,
    context: AuthorityContext | None = None,
    methods: bool = False,
    compositions: bool = False,
) -> dict:
    context = _context() if context is None else context
    decisions = []
    assertions = []
    for index, (predicate, target, value) in enumerate(entries, start=1):
        decision = make_synthetic_decision(
            context,
            decision_id=f"SYNTHETIC-DECISION-{index:03d}",
            predicate=predicate,
            target=target,
            value=value,
            evidence_ids=[EVIDENCE_ID],
            timestamp=TIMESTAMP,
        )
        decisions.append(decision)
        assertions.append(
            make_authority_assertion(
                context,
                assertion_id=f"SYNTHETIC-ASSERTION-{index:03d}",
                predicate=predicate,
                target=target,
                value=value,
                evidence_ids=[EVIDENCE_ID],
                authority_decision_id=decision["decision_id"],
            )
        )
    candidates = _candidate_data()
    return make_overlay(
        context,
        decisions=decisions,
        assertions=assertions,
        candidate_methods=candidates["candidate_methods"] if methods else (),
        candidate_compositions=candidates["candidate_compositions"] if compositions else (),
    )


def _positive_structural_entries() -> list[tuple[str, dict[str, str], str]]:
    entries = []
    for element_id in ("IR-ELEM-1", "IR-ELEM-2"):
        target = {"solution_id": "IR-SOL-1", "element_id": element_id}
        entries.extend(
            [
                ("SOLUTION_MEMBERSHIP", target, "MEMBER"),
                ("ELEMENT_ESSENTIALITY", target, "ESSENTIAL"),
            ]
        )
    return entries


def _resign_decision(decision: dict) -> None:
    decision["decision_digest"] = canonical_digest(
        {key: value for key, value in decision.items() if key != "decision_digest"}
    )


def _resign_assertion(assertion: dict) -> None:
    assertion["assertion_digest"] = canonical_digest(
        {key: value for key, value in assertion.items() if key != "assertion_digest"}
    )


def _resign_overlay(overlay: dict) -> None:
    overlay["overlay_digest"] = canonical_digest(
        {key: value for key, value in overlay.items() if key != "overlay_digest"}
    )


def _error(code: str, function, *args, **kwargs) -> SyntheticAuthorityError:
    with pytest.raises(SyntheticAuthorityError) as raised:
        function(*args, **kwargs)
    assert raised.value.code == code
    assert str(raised.value) == SyntheticAuthorityError.safe_message
    return raised.value


# HD-01 — explicit solution membership and source binding.


def test_hd01_valid_solution_membership_is_explicit_and_source_bound():
    context = _context()
    overlay = _overlay(_positive_structural_entries(), context=context)
    validated = validate_overlay(overlay, context)
    assert validated == overlay
    assert validated is not overlay


def test_hd01_missing_or_unknown_evidence_fails_closed():
    context = _context()
    target = {"solution_id": "IR-SOL-1", "element_id": "IR-ELEM-1"}
    _error(
        "EVIDENCE_REQUIRED",
        make_synthetic_decision,
        context,
        decision_id="D-1",
        predicate="SOLUTION_MEMBERSHIP",
        target=target,
        value="MEMBER",
        evidence_ids=[],
        timestamp=TIMESTAMP,
    )
    _error(
        "EVIDENCE_NOT_FOUND",
        make_synthetic_decision,
        context,
        decision_id="D-2",
        predicate="SOLUTION_MEMBERSHIP",
        target=target,
        value="MEMBER",
        evidence_ids=["EV-NOT-FOUND"],
        timestamp=TIMESTAMP,
    )


@pytest.mark.parametrize(
    "target",
    [
        {"solution_id": "IR-SOL-NOT-FOUND", "element_id": "IR-ELEM-1"},
        {"solution_id": "IR-SOL-1", "element_id": "IR-ELEM-NOT-FOUND"},
    ],
)
def test_hd01_nonexistent_solution_or_element_is_rejected(target):
    context = _context()
    overlay = _overlay([("SOLUTION_MEMBERSHIP", target, "MEMBER")], context=context)
    _error("ENTITY_NOT_FOUND", validate_overlay, overlay, context)


def test_hd01_cross_document_confirmation_reuse_is_rejected():
    context = _context()
    overlay = _overlay(_positive_structural_entries(), context=context)
    overlay["decisions"][0]["document_id"] = "another-document"
    _resign_decision(overlay["decisions"][0])
    _resign_overlay(overlay)
    _error("DOCUMENT_MISMATCH", validate_overlay, overlay, context)


def test_hd01_duplicate_assertions_are_rejected():
    context = _context()
    overlay = _overlay([_positive_structural_entries()[0]], context=context)
    duplicate = deepcopy(overlay["assertions"][0])
    duplicate["assertion_id"] = "SYNTHETIC-ASSERTION-REPLAY"
    _resign_assertion(duplicate)
    overlay["assertions"].append(duplicate)
    _resign_overlay(overlay)
    _error("ASSERTION_DUPLICATE", validate_overlay, overlay, context)


def test_hd01_contradictory_assertions_are_rejected():
    context = _context()
    overlay = _overlay([_positive_structural_entries()[0]], context=context)
    contradiction = deepcopy(overlay["assertions"][0])
    contradiction["assertion_id"] = "SYNTHETIC-ASSERTION-CONFLICT"
    contradiction["value"] = "NOT_MEMBER"
    _resign_assertion(contradiction)
    overlay["assertions"].append(contradiction)
    _resign_overlay(overlay)
    _error("ASSERTION_CONFLICT", validate_overlay, overlay, context)


def test_hd01_changed_source_hash_invalidates_overlay():
    context = _context()
    overlay = _overlay([_positive_structural_entries()[0]], context=context)
    changed = replace(context, source_sha256="c" * 64)
    _error("SOURCE_HASH_MISMATCH", validate_overlay, overlay, changed)


def test_hd01_inferred_membership_is_never_authority():
    context = _context()
    overlay = _overlay([_positive_structural_entries()[0]], context=context)
    overlay["assertions"][0]["grounding"] = "INFERENCE"
    _resign_assertion(overlay["assertions"][0])
    _resign_overlay(overlay)
    _error("INFERRED_AUTHORITY_UNSUPPORTED", validate_overlay, overlay, context)


# HD-02 — conservative essentiality.


@pytest.mark.parametrize("state", ["UNKNOWN", "OPTIONAL", "CONDITIONAL"])
def test_hd02_nonessential_states_never_promote_to_essential(state):
    context = _context()
    target = {"solution_id": "IR-SOL-1", "element_id": "IR-ELEM-1"}
    overlay = _overlay(
        [
            ("SOLUTION_MEMBERSHIP", target, "MEMBER"),
            ("ELEMENT_ESSENTIALITY", target, state),
        ],
        context=context,
    )
    result = evaluate_family_authority(
        overlay,
        context,
        family="SYSTEM",
        solution_id="IR-SOL-1",
        required_element_ids=["IR-ELEM-1"],
    )
    assert result.eligible is False
    assert result.code == "ELEMENT_ESSENTIALITY_UNRESOLVED"


def test_hd02_missing_confirmation_cannot_establish_essentiality():
    context = _context()
    overlay = _overlay([_positive_structural_entries()[1]], context=context)
    overlay["assertions"][0]["authority_decision_id"] = "MISSING-DECISION"
    _resign_assertion(overlay["assertions"][0])
    _resign_overlay(overlay)
    _error("CONFIRMATION_REQUIRED", validate_overlay, overlay, context)


def test_hd02_mismatched_confirmation_target_fails_closed():
    context = _context()
    overlay = _overlay([_positive_structural_entries()[1]], context=context)
    overlay["assertions"][0]["target"]["element_id"] = "IR-ELEM-2"
    _resign_assertion(overlay["assertions"][0])
    _resign_overlay(overlay)
    _error("CONFIRMATION_MISMATCH", validate_overlay, overlay, context)


def test_hd02_conflicting_confirmation_requires_explicit_supersession():
    context = _context()
    target = {"solution_id": "IR-SOL-1", "element_id": "IR-ELEM-1"}
    first = make_synthetic_decision(
        context,
        decision_id="D-ESSENTIAL",
        predicate="ELEMENT_ESSENTIALITY",
        target=target,
        value="ESSENTIAL",
        evidence_ids=[EVIDENCE_ID],
        timestamp=TIMESTAMP,
    )
    conflict = make_synthetic_decision(
        context,
        decision_id="D-OPTIONAL",
        predicate="ELEMENT_ESSENTIALITY",
        target=target,
        value="OPTIONAL",
        evidence_ids=[EVIDENCE_ID],
        timestamp="2026-10-15T09:01:00Z",
    )
    overlay = make_overlay(context, decisions=[first, conflict], assertions=[])
    _error("DECISION_CONFLICT", validate_overlay, overlay, context)


# HD-03 — preliminary method semantics, with positive Claims disabled.


def test_hd03_ordered_steps_alone_do_not_establish_method_membership():
    context = _context()
    target = {
        "method_id": "SYNTHETIC-METHOD-001",
        "subject_step_id": "IR-STEP-1",
        "object_step_id": "IR-STEP-2",
    }
    overlay = _overlay(
        [("METHOD_STEP_RELATIONSHIP", target, "ORDER_REQUIRED")],
        context=context,
        methods=True,
    )
    result = inspect_preliminary_method(overlay, context, method_id="SYNTHETIC-METHOD-001")
    assert (result.eligible, result.code) == (False, "METHOD_MEMBERSHIP_UNRESOLVED")


def test_hd03_missing_step_essentiality_blocks_preliminary_model():
    context = _context()
    entries = [
        (
            "METHOD_STEP_MEMBERSHIP",
            {"method_id": "SYNTHETIC-METHOD-001", "step_id": step_id},
            "MEMBER",
        )
        for step_id in ("IR-STEP-1", "IR-STEP-2")
    ]
    overlay = _overlay(entries, context=context, methods=True)
    result = inspect_preliminary_method(overlay, context, method_id="SYNTHETIC-METHOD-001")
    assert (result.eligible, result.code) == (False, "METHOD_ESSENTIALITY_UNRESOLVED")


def test_hd03_conflicting_step_relationships_are_rejected():
    context = _context()
    entries = [
        (
            "METHOD_STEP_RELATIONSHIP",
            {
                "method_id": "SYNTHETIC-METHOD-001",
                "subject_step_id": subject,
                "object_step_id": obj,
            },
            "ORDER_REQUIRED",
        )
        for subject, obj in (("IR-STEP-1", "IR-STEP-2"), ("IR-STEP-2", "IR-STEP-1"))
    ]
    overlay = _overlay(entries, context=context, methods=True)
    _error("METHOD_RELATIONSHIP_CONFLICT", validate_overlay, overlay, context)


@pytest.mark.parametrize("family", ["METHOD", "PROCESS"])
def test_hd03_method_and_process_positive_authority_cannot_be_enabled(family):
    context = _context()
    overlay = _overlay([], context=context, methods=True)
    result = evaluate_family_authority(
        overlay,
        context,
        family=family,
        solution_id="IR-SOL-1",
        required_element_ids=["IR-ELEM-1"],
    )
    assert (result.eligible, result.code, result.positive_claims_enabled) == (
        False,
        "CLAIM_FAMILY_DISABLED",
        False,
    )


# HD-04 — preliminary composition semantics, with positive Claims disabled.


def test_hd04_co_mentioned_materials_do_not_establish_composition():
    context = _context()
    overlay = _overlay([], context=context, compositions=True)
    result = inspect_preliminary_composition(
        overlay, context, composition_id="SYNTHETIC-COMPOSITION-001"
    )
    assert (result.eligible, result.code) == (False, "COMPOSITION_MEMBERSHIP_UNRESOLVED")


@pytest.mark.parametrize("amount_state", ["EXAMPLE", "EXPERIMENTAL"])
def test_hd04_nonmandatory_amounts_do_not_become_claim_limitations(amount_state):
    context = _context()
    entries = [
        (
            "COMPOSITION_MEMBERSHIP",
            {
                "composition_id": "SYNTHETIC-COMPOSITION-001",
                "material_id": "SYNTHETIC-MATERIAL-A",
            },
            "MEMBER",
        ),
        (
            "COMPOSITION_AMOUNT_MANDATORY",
            {
                "composition_id": "SYNTHETIC-COMPOSITION-001",
                "material_id": "SYNTHETIC-MATERIAL-A",
                "amount_id": "SYNTHETIC-AMOUNT-A",
            },
            amount_state,
        ),
    ]
    overlay = _overlay(entries, context=context, compositions=True)
    result = inspect_preliminary_composition(
        overlay, context, composition_id="SYNTHETIC-COMPOSITION-001"
    )
    assert (result.eligible, result.code) == (False, "COMPOSITION_AMOUNT_UNRESOLVED")


def test_hd04_cross_composition_material_splicing_fails():
    context = _context()
    overlay = _overlay(
        [
            (
                "COMPOSITION_MEMBERSHIP",
                {
                    "composition_id": "SYNTHETIC-COMPOSITION-001",
                    "material_id": "SYNTHETIC-MATERIAL-C",
                },
                "MEMBER",
            )
        ],
        context=context,
        compositions=True,
    )
    _error("COMPOSITION_SPLICE", validate_overlay, overlay, context)


def test_hd04_composition_positive_authority_is_disabled():
    context = _context()
    overlay = _overlay([], context=context, compositions=True)
    result = evaluate_family_authority(
        overlay,
        context,
        family="COMPOSITION",
        solution_id="IR-SOL-1",
        required_element_ids=["IR-ELEM-1"],
    )
    assert (result.eligible, result.code) == (False, "CLAIM_FAMILY_DISABLED")


# HD-05 — SYSTEM/APPARATUS-only prototype family policy.


@pytest.mark.parametrize("family", ["SYSTEM", "APPARATUS"])
def test_hd05_supported_structural_authority_is_eligible_for_further_validation(family):
    context = _context()
    overlay = _overlay(_positive_structural_entries(), context=context)
    result = evaluate_family_authority(
        overlay,
        context,
        family=family,
        solution_id="IR-SOL-1",
        required_element_ids=["IR-ELEM-1", "IR-ELEM-2"],
    )
    assert result.eligible is True
    assert result.code == "ELIGIBLE_FOR_RELEASED_P2_004_VALIDATION"
    assert result.positive_claims_enabled is False
    assert len(result.assertion_ids) == 4


def test_hd05_unsupported_structural_candidate_remains_blocked():
    context = _context()
    entries = _positive_structural_entries()[:-1]
    overlay = _overlay(entries, context=context)
    result = evaluate_family_authority(
        overlay,
        context,
        family="SYSTEM",
        solution_id="IR-SOL-1",
        required_element_ids=["IR-ELEM-1", "IR-ELEM-2"],
    )
    assert (result.eligible, result.code) == (False, "ELEMENT_ESSENTIALITY_UNRESOLVED")


def test_hd05_configuration_cannot_enable_disabled_families():
    context = _context()
    overlay = _overlay([], context=context)
    overlay["family_policy"]["eligible_for_further_validation"].append("METHOD")
    _resign_overlay(overlay)
    _error("FAMILY_POLICY_INVALID", validate_overlay, overlay, context)


def test_hd05_unrecognized_family_fails_closed():
    context = _context()
    overlay = _overlay([], context=context)
    _error(
        "CLAIM_FAMILY_UNKNOWN",
        evaluate_family_authority,
        overlay,
        context,
        family="SOFTWARE_WIDGET",
        solution_id="IR-SOL-1",
        required_element_ids=["IR-ELEM-1"],
    )


def test_hd05_positive_overlay_can_precede_unchanged_released_p2_004_validation():
    source = _json(RECONSTRUCTION)
    context = _context(source)
    overlay = _overlay(_positive_structural_entries(), context=context)
    authority = evaluate_family_authority(
        overlay,
        context,
        family="SYSTEM",
        solution_id="IR-SOL-1",
        required_element_ids=["IR-ELEM-1", "IR-ELEM-2"],
    )
    p2_config = {"source_document_synthetic": True}
    claims_config = {
        "language": "en",
        "target_jurisdiction": "US",
        "requested_claim_types": ["SYSTEM"],
        "max_dependent_claims_per_family": 4,
        "source_document_synthetic": True,
        "selected_solution_id": "IR-SOL-1",
        "p2_003_generation_config": p2_config,
    }
    specification = generate_uspto_specification(source, p2_config)
    released_result = generate_supported_draft_claims(source, specification, claims_config)
    assert authority.eligible is True
    assert released_result["claim_families"][0]["status"] == "PRESENT"
    assert released_result["claims"]
    assert "authority" not in released_result


# HD-06 — synthetic actor, lifecycle, freshness and replay protection.


def test_hd06_invalid_synthetic_actor_is_rejected():
    context = _context()
    overlay = _overlay([_positive_structural_entries()[0]], context=context)
    overlay["decisions"][0]["actor_id"] = "REAL-USER-001"
    _resign_decision(overlay["decisions"][0])
    _resign_overlay(overlay)
    _error("ACTOR_INVALID", validate_overlay, overlay, context)


def test_hd06_checkbox_or_boolean_cannot_replace_a_decision_record():
    context = _context()
    overlay = _overlay([_positive_structural_entries()[0]], context=context)
    overlay["decisions"] = [True]
    _resign_overlay(overlay)
    _error("DECISION_INVALID", validate_overlay, overlay, context)


def test_hd06_stale_revision_is_rejected():
    context = _context()
    overlay = _overlay([_positive_structural_entries()[0]], context=context)
    overlay["decisions"][0]["revision_token"] = "rev-6-stale"
    _resign_decision(overlay["decisions"][0])
    _resign_overlay(overlay)
    _error("STALE_REVISION", validate_overlay, overlay, context)


def test_hd06_revoked_confirmation_is_inactive():
    context = _context()
    predicate, target, value = _positive_structural_entries()[0]
    confirm = make_synthetic_decision(
        context,
        decision_id="D-CONFIRM",
        predicate=predicate,
        target=target,
        value=value,
        evidence_ids=[EVIDENCE_ID],
        timestamp=TIMESTAMP,
    )
    revoke = make_synthetic_decision(
        context,
        decision_id="D-REVOKE",
        predicate=predicate,
        target=target,
        value=value,
        evidence_ids=[EVIDENCE_ID],
        timestamp="2026-10-15T09:02:00Z",
        action="REVOKE",
        subject_decision_id="D-CONFIRM",
    )
    assertion = make_authority_assertion(
        context,
        assertion_id="A-MEMBER",
        predicate=predicate,
        target=target,
        value=value,
        evidence_ids=[EVIDENCE_ID],
        authority_decision_id="D-CONFIRM",
    )
    overlay = make_overlay(context, decisions=[confirm, revoke], assertions=[assertion])
    _error("CONFIRMATION_INACTIVE", validate_overlay, overlay, context)


def test_hd06_explicit_supersession_invalidates_old_confirmation():
    context = _context()
    target = {"solution_id": "IR-SOL-1", "element_id": "IR-ELEM-1"}
    old = make_synthetic_decision(
        context,
        decision_id="D-OLD",
        predicate="ELEMENT_ESSENTIALITY",
        target=target,
        value="ESSENTIAL",
        evidence_ids=[EVIDENCE_ID],
        timestamp=TIMESTAMP,
    )
    new = make_synthetic_decision(
        context,
        decision_id="D-NEW",
        predicate="ELEMENT_ESSENTIALITY",
        target=target,
        value="UNKNOWN",
        evidence_ids=[EVIDENCE_ID],
        timestamp="2026-10-15T09:03:00Z",
        supersedes_decision_id="D-OLD",
    )
    assertion = make_authority_assertion(
        context,
        assertion_id="A-NEW",
        predicate="ELEMENT_ESSENTIALITY",
        target=target,
        value="UNKNOWN",
        evidence_ids=[EVIDENCE_ID],
        authority_decision_id="D-NEW",
    )
    overlay = make_overlay(context, decisions=[old, new], assertions=[assertion])
    validate_overlay(overlay, context)


def test_hd06_tampered_decision_and_overlay_are_rejected():
    context = _context()
    overlay = _overlay([_positive_structural_entries()[0]], context=context)
    overlay["decisions"][0]["value"] = "NOT_MEMBER"
    _resign_overlay(overlay)
    _error("DECISION_TAMPERED", validate_overlay, overlay, context)


def test_hd06_changed_evidence_invalidates_confirmation():
    context = _context()
    overlay = _overlay([_positive_structural_entries()[0]], context=context)
    evidence = deepcopy(dict(context.evidence_records))
    evidence[EVIDENCE_ID]["excerpt"] = "Changed synthetic evidence."
    changed = replace(context, evidence_records=evidence)
    _error("EVIDENCE_CHANGED", validate_overlay, overlay, changed)


def test_hd06_replayed_decision_is_rejected():
    context = _context()
    overlay = _overlay([_positive_structural_entries()[0]], context=context)
    overlay["decisions"].append(deepcopy(overlay["decisions"][0]))
    _resign_overlay(overlay)
    _error("DECISION_DUPLICATE", validate_overlay, overlay, context)


# HD-07 — additive compatibility and deterministic identity.


def test_hd07_overlay_identity_is_deterministic_and_versioned():
    context = _context()
    first = _overlay(_positive_structural_entries(), context=context)
    second = _overlay(_positive_structural_entries(), context=context)
    assert first == second
    assert first["schema_version"] == "1.0.0"
    assert first["overlay_digest"] == second["overlay_digest"]
    assert first["notice"] == {
        "synthetic_only": True,
        "authenticated_identity": False,
        "production_authority": False,
        "legal_authority": False,
    }


def test_hd07_released_package_keeps_exact_original_seven_inputs():
    parameters = inspect.signature(validate_assembly_inputs).parameters
    assert tuple(parameters) == PROVENANCE_KEYS
    assert len(PROVENANCE_KEYS) == 7
    assert "authority_overlay" not in parameters


def test_hd07_released_contract_files_remain_byte_identical_to_baseline():
    expected = {
        "backend/app/services/supported_draft_claims_generation.py": (
            "15cd37f00966a9a78165989fa7405465b4280e9c913b2e43fbc1634a3f5b28db"
        ),
        "backend/app/services/supported_draft_claims_validation.py": (
            "ccb4837a6dc434cd58c03717dfe2b71b9b2667616dba48d64e14b6b25ffe1414"
        ),
        "backend/app/services/uspto_document_package_validation.py": (
            "1c35bcf63333a7b8774050248674e8009f22fa4758ade688571eaac50210e2b2"
        ),
        "backend/app/services/uspto_offline_renderer.py": (
            "cc613ad7ecbeabd2049d6f565933182dc78a1503b8b0ac252fbbc1fd00b10250"
        ),
        "backend/app/services/uspto_offline_orchestration.py": (
            "b8f2fb9697f8ad5b4bb94895a2dae7112977d378a64f0a1a05e82380251f5955"
        ),
    }
    for relative, digest in expected.items():
        content = (ROOT / relative).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        assert hashlib.sha256(content).hexdigest() == digest


def test_hd07_errors_do_not_disclose_source_content():
    source = _json(RECONSTRUCTION)
    secret_excerpt = source["review_package"]["evidence"][0]["excerpt"]
    context = _context(source)
    overlay = _overlay([_positive_structural_entries()[0]], context=context)
    overlay["decisions"][0]["actor_id"] = "INVALID"
    _resign_decision(overlay["decisions"][0])
    _resign_overlay(overlay)
    error = _error("ACTOR_INVALID", validate_overlay, overlay, context)
    assert secret_excerpt not in str(error)
    assert secret_excerpt not in repr(error.paths)


def test_hd07_overlay_is_not_wired_to_public_routes():
    route_sources = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (ROOT / "backend/app/api/routes").glob("*.py")
    )
    assert "synthetic_claims_authority_v1" not in route_sources
