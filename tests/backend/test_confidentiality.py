"""P0-CONF: offline, exact-payload consent with no implicit egress authority."""
from dataclasses import FrozenInstanceError, replace
from datetime import datetime, timedelta, timezone
from copy import deepcopy

import pytest

from backend.app.services.confidentiality import (
    ConsentError, OfflineConfidentialityGate, SourceRevision,
)
from backend.app.services.supported_draft_claims_validation import sha256_canonical
from tests.e2e.provider_tripwire import ProviderTripwire

SOURCE = SourceRevision("doc_a", "a" * 64, 1)
PAYLOAD = {"source_units": [{"text": "Synthetic sensor value 12", "page": 1}]}
SCOPE = {"owner": "owner_a", "destination": "approved_provider", "purpose": "SCIENTIFIC_ANALYSIS"}
PRINCIPAL = {"owner": "owner_a", "actor": "reviewer_a", "context": "human_decision_a"}


@pytest.fixture
def setup_gate():
    now = [datetime(2026, 11, 22, 0, 0, tzinfo=timezone.utc)]
    requests = []
    def authority(request):
        requests.append(request)
        return request.actor == "reviewer_a" and request.context == "human_decision_a"
    gate = OfflineConfidentialityGate(authorizer=authority, clock=lambda: now[0])
    return gate, now, requests


def classify(gate, source=SOURCE, classification="CONFIDENTIAL"):
    return gate.classify(source, classification=classification, **PRINCIPAL)


def grant(gate, now, source=SOURCE, payload=None, **extra):
    args = {**SCOPE, "actor": PRINCIPAL["actor"], "context": PRINCIPAL["context"],
            "expires_at": now[0] + timedelta(minutes=10), **extra}
    return gate.grant(source, deepcopy(PAYLOAD) if payload is None else payload, **args)


def test_missing_classification_or_authority_never_grants():
    gate = OfflineConfidentialityGate()
    assert not gate.check(SOURCE, PAYLOAD, **SCOPE).allowed
    with pytest.raises(ConsentError, match="AUTHORIZATION_REQUIRED"):
        classify(gate)


@pytest.mark.parametrize("classification", ["PUBLIC", "CONFIDENTIAL", "UNPUBLISHED"])
def test_classification_alone_is_not_egress_consent(setup_gate, classification):
    gate, _, _ = setup_gate
    classify(gate, classification=classification)
    assert gate.check(SOURCE, PAYLOAD, **SCOPE).code == "CONSENT_REQUIRED"


def test_success_records_actual_actor_utc_scope_digest_without_payload(setup_gate):
    gate, now, requests = setup_gate
    with ProviderTripwire() as tripwire:
        classification = classify(gate)
        receipt = grant(gate, now)
        result = gate.check(SOURCE, PAYLOAD, **SCOPE)
        assert result.allowed and result.code == "EXPLICIT_CONSENT"
        assert result.consent == receipt
        assert receipt.recorded_at == now[0] == classification.recorded_at
        assert receipt.request.actor == "reviewer_a"
        assert receipt.request.payload_sha256 == sha256_canonical(PAYLOAD)
        assert receipt.request.destination == "approved_provider"
        assert receipt.request.purpose == "SCIENTIFIC_ANALYSIS"
        assert requests[-1] == receipt.request
        assert "Synthetic sensor" not in repr(receipt)
        with pytest.raises(FrozenInstanceError):
            receipt.request.actor = "forged"
        tripwire.assert_no_unexpected_activity()
        assert all(value == 0 for value in tripwire.snapshot().values())


@pytest.mark.parametrize("change", [
    {"owner": "owner_b"}, {"destination": "other_provider"},
    {"purpose": "PRIOR_ART_SEARCH"}, {"purpose": "DISPLAY_ONLY"},
])
def test_consent_cannot_cross_owner_destination_or_purpose(setup_gate, change):
    gate, now, _ = setup_gate
    classify(gate); grant(gate, now)
    assert not gate.check(SOURCE, PAYLOAD, **{**SCOPE, **change}).allowed


@pytest.mark.parametrize("source", [replace(SOURCE, document_id="other_doc"),
    replace(SOURCE, source_sha256="b" * 64), replace(SOURCE, revision=2)])
def test_consent_cannot_cross_document_source_or_revision(setup_gate, source):
    gate, now, _ = setup_gate
    classify(gate); grant(gate, now)
    assert not gate.check(source, PAYLOAD, **SCOPE).allowed


def test_payload_mutation_and_canonical_equivalence(setup_gate):
    gate, now, _ = setup_gate
    classify(gate); grant(gate, now, payload={"a": 1, "b": 2})
    assert gate.check(SOURCE, {"b": 2, "a": 1}, **SCOPE).allowed
    assert gate.check(SOURCE, {"a": 2, "b": 2}, **SCOPE).code == "PAYLOAD_CHANGED"


def test_revocation_reclassification_and_new_revision_invalidate(setup_gate):
    gate, now, _ = setup_gate
    classify(gate); grant(gate, now)
    receipt = gate.revoke(SOURCE, **PRINCIPAL)
    assert receipt.request.action == "REVOKE_EGRESS"
    assert not gate.check(SOURCE, PAYLOAD, **SCOPE).allowed
    grant(gate, now)
    classify(gate, classification="PUBLIC")
    assert not gate.check(SOURCE, PAYLOAD, **SCOPE).allowed
    grant(gate, now)
    newer = replace(SOURCE, revision=2)
    classify(gate, source=newer)
    assert gate.check(SOURCE, PAYLOAD, **SCOPE).code == "STALE_SOURCE_REVISION"
    assert not gate.check(newer, PAYLOAD, **SCOPE).allowed
    with pytest.raises(ConsentError, match="STALE_SOURCE_REVISION"):
        classify(gate)


def test_same_revision_cannot_change_source_hash_or_owner(setup_gate):
    gate, _, _ = setup_gate
    classify(gate)
    with pytest.raises(ConsentError, match="SOURCE_REVISION_CONFLICT"):
        classify(gate, replace(SOURCE, source_sha256="b" * 64))
    with pytest.raises(ConsentError, match="OWNER_MISMATCH"):
        gate.classify(SOURCE, classification="PUBLIC", **{**PRINCIPAL, "owner": "owner_b"})


def test_expiry_and_naive_time_fail_closed(setup_gate):
    gate, now, _ = setup_gate
    classify(gate); grant(gate, now)
    now[0] += timedelta(minutes=10)
    assert gate.check(SOURCE, PAYLOAD, **SCOPE).code == "CONSENT_EXPIRED"
    with pytest.raises(ConsentError, match="CONSENT_EXPIRED"):
        grant(gate, now, expires_at=now[0])
    with pytest.raises(ConsentError, match="INVALID_TIME"):
        grant(gate, now, expires_at=datetime(2026, 11, 22))


def test_actor_context_and_callback_errors_do_not_create_consent(setup_gate):
    gate, now, _ = setup_gate
    classify(gate)
    for change in [{"actor": "untrusted"}, {"context": "display_only"}]:
        with pytest.raises(ConsentError, match="AUTHORIZATION_REQUIRED"):
            grant(gate, now, **change)
        assert not gate.check(SOURCE, PAYLOAD, **SCOPE).allowed
    def broken(_):
        raise RuntimeError("private callback content")
    broken_gate = OfflineConfidentialityGate(authorizer=broken)
    with pytest.raises(ConsentError, match="^AUTHORIZATION_REQUIRED$"):
        classify(broken_gate)


@pytest.mark.parametrize("payload", [[], {"v": float("nan")}, {"v": object()},
    {"v": "x" * 1_048_577}, {"v": (1, 2)}])
def test_invalid_or_oversize_payload_is_denied_without_leaking(setup_gate, payload):
    gate, now, _ = setup_gate
    classify(gate)
    assert gate.check(SOURCE, payload, **SCOPE).code == "INVALID_PAYLOAD"
    with pytest.raises(ConsentError, match="^INVALID_PAYLOAD$"):
        grant(gate, now, payload=payload)


@pytest.mark.parametrize("change", [{"revision": True}, {"revision": 0},
    {"source_sha256": "raw-source-content"}, {"document_id": "../unsafe"}])
def test_invalid_source_identity_is_rejected(change):
    with pytest.raises(ConsentError):
        replace(SOURCE, **change)


def test_bounded_capacity_and_clock_failure(setup_gate):
    _, now, _ = setup_gate
    gate = OfflineConfidentialityGate(authorizer=lambda _: True, clock=lambda: now[0],
                                     max_records=1, max_scopes=1)
    classify(gate); grant(gate, now)
    with pytest.raises(ConsentError, match="CAPACITY_REACHED"):
        classify(gate, replace(SOURCE, document_id="doc_b"))
    with pytest.raises(ConsentError, match="CAPACITY_REACHED"):
        grant(gate, now, destination="provider_b")
    now[0] = datetime(2026, 11, 22)  # Invalid host clock: even existing consent cannot pass.
    assert gate.check(SOURCE, PAYLOAD, **SCOPE).code == "CLOCK_UNAVAILABLE"


def test_callback_revocation_cannot_be_overwritten_by_pending_grant(setup_gate):
    _, now, _ = setup_gate
    gate = None
    def authority(request):
        if request.action == "ALLOW_EGRESS":
            gate.revoke(SOURCE, **PRINCIPAL)
        return True
    gate = OfflineConfidentialityGate(authorizer=authority, clock=lambda: now[0])
    classify(gate)
    with pytest.raises(ConsentError, match="STALE_SOURCE_REVISION"):
        grant(gate, now)
    assert not gate.check(SOURCE, PAYLOAD, **SCOPE).allowed


def test_new_process_store_does_not_accept_prior_receipts_as_authority(setup_gate):
    gate, now, _ = setup_gate
    classify(gate); receipt = grant(gate, now)
    fresh = OfflineConfidentialityGate()
    assert receipt.request.action == "ALLOW_EGRESS"
    assert not fresh.check(SOURCE, PAYLOAD, **SCOPE).allowed


@pytest.mark.parametrize("destination", ["*", "https://external.invalid", "", "provider\nheader"])
def test_invalid_destination_cannot_widen_scope_or_trigger_fetch(setup_gate, destination):
    gate, now, _ = setup_gate
    classify(gate)
    with ProviderTripwire() as guard:
        assert not gate.check(SOURCE, PAYLOAD, **{**SCOPE, "destination": destination}).allowed
        with pytest.raises(ConsentError, match="INVALID_IDENTIFIER"):
            grant(gate, now, destination=destination)
        guard.assert_no_unexpected_activity()


def test_grant_requires_classification_even_with_trusted_authorizer(setup_gate):
    gate, now, _ = setup_gate
    with pytest.raises(ConsentError, match="CLASSIFICATION_REQUIRED"):
        grant(gate, now)


def test_consent_that_expires_during_authorization_is_not_recorded(setup_gate):
    _, now, _ = setup_gate
    def authority(request):
        if request.action == "ALLOW_EGRESS":
            now[0] += timedelta(minutes=11)
        return True
    gate = OfflineConfidentialityGate(authorizer=authority, clock=lambda: now[0])
    classify(gate)
    with pytest.raises(ConsentError, match="CONSENT_EXPIRED"):
        grant(gate, now)
    assert not gate.check(SOURCE, PAYLOAD, **SCOPE).allowed


def test_callback_cannot_overallocate_record_capacity(setup_gate):
    _, now, _ = setup_gate
    second = replace(SOURCE, document_id="doc_b")
    gate = None
    def authority(request):
        if request.action == "CLASSIFY" and request.source == SOURCE:
            classify(gate, source=second)
        return True
    gate = OfflineConfidentialityGate(authorizer=authority, clock=lambda: now[0], max_records=1)
    with pytest.raises(ConsentError, match="CAPACITY_REACHED"):
        classify(gate)
    assert gate.check(SOURCE, PAYLOAD, **SCOPE).code == "CLASSIFICATION_REQUIRED"
    assert gate.check(second, PAYLOAD, **SCOPE).code == "CONSENT_REQUIRED"
