"""Manual Prior Art: real registered source bytes, immutable evidence, no network."""
from dataclasses import FrozenInstanceError, replace
from datetime import datetime, timezone, timedelta
import os
from types import SimpleNamespace

from fastapi.testclient import TestClient
import pytest

from backend.app.core.config import Settings
from backend.app.main import create_app
from backend.app.services.custody_review import review_documents
from backend.app.services.manual_prior_art import (
    ManualPriorArtWorkflow, PriorArtReference, ManualSearchRecord, PriorArtError,
    INCOMPLETE_WARNING,
)
from tests.backend.test_document_upload import synthetic_docx, synthetic_pdf
from tests.e2e.provider_tripwire import ProviderTripwire

PRINCIPAL = {"owner": "owner_a", "actor": "specialist_a", "context": "human_scope_a"}
REF = PriorArtReference("ref_a", "PATENT", "Synthetic patent citation, not a real patent",
    "Synthetic manual source", "2026-11-21", "https://example.invalid/patent-a",
    "Synthetic passage only", "Sensor component described", "Control path differs")
INCOMPLETE = ManualSearchRecord("Bounded manual search", "Coverage incomplete", (REF,))
RECORDED = replace(INCOMPLETE, status="MANUAL_SEARCH_RECORDED")


@pytest.fixture(autouse=True)
def offline_guard():
    with ProviderTripwire() as guard:
        yield guard
        guard.assert_no_unexpected_activity()
        assert all(value == 0 for value in guard.snapshot().values())


@pytest.fixture
def host(tmp_path, offline_guard):
    app = create_app(Settings(storage_root=tmp_path / "uploads"))
    clock = [datetime(2026, 11, 22, 8, tzinfo=timezone.utc)]
    requests = []
    def authority(request):
        requests.append(request)
        return request.actor == "specialist_a" and request.context == "human_scope_a"
    workflow = ManualPriorArtWorkflow(app.state.document_storage, app.state.document_registry,
        authorizer=authority, clock=lambda: clock[0])
    with TestClient(app) as client:
        docs = []
        for name, data, mime in [("sample.pdf", synthetic_pdf(), "application/pdf"),
            ("sample.docx", synthetic_docx(), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")]:
            response = client.post("/api/documents", files={"file": (name, data, mime)})
            assert response.status_code == 201
            docs.append(response.json()["document_id"])
        yield SimpleNamespace(app=app, client=client, wf=workflow, clock=clock,
                              requests=requests, docs=docs, authority=authority)


def save(host, search=INCOMPLETE, doc=None, revision=0, **extra):
    return host.wf.save(doc or host.docs[0], search, expected_revision=revision,
        reason="Manual evidence entered", **{**PRINCIPAL, **extra})


def decide(host, choice="CONTINUE", revision=1, doc=None, **extra):
    return host.wf.decide(doc or host.docs[0], choice=choice, expected_revision=revision,
        reason="Specialist explicitly decided after reviewing limits", **{**PRINCIPAL, **extra})


def assess(host, revision=1, doc=None, **extra):
    return host.wf.assess_drafting(doc or host.docs[0], expected_revision=revision,
                                  **{**PRINCIPAL, **extra})


@pytest.mark.parametrize("index", [0, 1])
def test_actual_pdf_docx_upload_to_incomplete_continue_audit(host, index):
    document_id = host.docs[index]
    snapshot = save(host, doc=document_id)
    registry = host.app.state.document_registry.get(document_id)
    assert snapshot.source_sha256 == registry.sha256
    assert snapshot.dossier_revision == 1
    assert assess(host, doc=document_id).code == "HUMAN_DECISION_REQUIRED"
    decision = decide(host, doc=document_id)
    result = assess(host, doc=document_id)
    assert result.allowed and result.code == "EXPLICIT_CONTINUATION"
    assert INCOMPLETE_WARNING in result.warnings
    assert result.source_sha256 == registry.sha256
    assert result.decision_sha256 == decision.audit[-1].sha256
    body = review_documents(snapshot.content)
    assert body["reference_verification"] == "USER_RECORDED_NOT_VERIFIED"
    assert body["novelty_assessed"] is False and body["patentability_assessed"] is False
    assert body["manual_search"]["references"][0]["citation"] == REF.citation
    assert [event.sequence for event in decision.audit] == [1, 2]
    assert decision.audit[1].previous_sha256 == decision.audit[0].sha256
    assert decision.audit[-1].request.actor == PRINCIPAL["actor"]
    assert decision.audit[-1].recorded_at == host.clock[0]
    assert host.requests[-1].dossier_sha256 == result.dossier_sha256


def test_recorded_search_still_needs_human_and_never_asserts_novelty(host):
    save(host, RECORDED)
    assert not assess(host).allowed
    decide(host)
    result = assess(host)
    assert result.allowed and INCOMPLETE_WARNING not in result.warnings
    assert "not independently verified" in result.warnings[0]


def test_explicit_incomplete_with_no_citations_can_continue_with_warning(host):
    record = ManualSearchRecord("No sources searched yet", "Specialist records absent coverage")
    save(host, record); decide(host)
    assert INCOMPLETE_WARNING in assess(host).warnings


def test_no_record_cannot_skip_mandatory_manual_step(host):
    with pytest.raises(PriorArtError, match="PRIOR_ART_RECORD_NOT_FOUND"):
        assess(host)


def test_last_stop_then_continue_decision_controls_same_revision(host):
    save(host); decide(host)
    decide(host, "STOP")
    assert assess(host).code == "HUMAN_STOPPED" and not assess(host).allowed
    decide(host)
    assert assess(host).allowed


def test_content_revision_invalidates_decision_and_stale_consumers(host):
    save(host); decide(host)
    newer = save(host, replace(INCOMPLETE, limitations="Additional unresolved source"), revision=1)
    assert newer.dossier_revision == 2
    assert not assess(host, revision=2).allowed
    for operation in [lambda: save(host, revision=1), lambda: decide(host, revision=1), lambda: assess(host)]:
        with pytest.raises(PriorArtError, match="STALE_DOSSIER_REVISION"):
            operation()


@pytest.mark.parametrize("bad", [None, True, 0, -1, "1"])
def test_expected_revision_cannot_be_omitted_or_coerced(host, bad):
    save(host)
    for operation in [lambda: decide(host, revision=bad), lambda: assess(host, revision=bad)]:
        with pytest.raises(PriorArtError, match="STALE_DOSSIER_REVISION"):
            operation()


def test_foreign_owner_cannot_read_edit_or_decide(host):
    save(host)
    for operation in [lambda: save(host, revision=1, owner="owner_b"),
        lambda: decide(host, owner="owner_b"), lambda: assess(host, owner="owner_b"),
        lambda: host.wf.snapshot(host.docs[0], **{**PRINCIPAL, "owner": "owner_b"})]:
        with pytest.raises(PriorArtError, match="PRIOR_ART_RECORD_NOT_FOUND"):
            operation()


def test_authority_is_required_for_save_read_and_decision(host):
    with pytest.raises(PriorArtError, match="AUTHORIZATION_REQUIRED"):
        save(host, actor="untrusted")
    save(host)
    with pytest.raises(PriorArtError, match="AUTHORIZATION_REQUIRED"):
        decide(host, context="display_only")
    with pytest.raises(PriorArtError, match="AUTHORIZATION_REQUIRED"):
        assess(host, actor="untrusted")
    denied = ManualPriorArtWorkflow(host.app.state.document_storage, host.app.state.document_registry)
    with pytest.raises(PriorArtError, match="AUTHORIZATION_REQUIRED"):
        denied.save(host.docs[1], INCOMPLETE, expected_revision=0, reason="No authority", **PRINCIPAL)


@pytest.mark.parametrize("mode", ["tamper", "delete", "expire"])
def test_actual_source_integrity_removal_and_ttl_invalidate_assessment(host, mode):
    save(host); decide(host)
    storage = host.app.state.document_storage
    path = storage.path_for(host.docs[0])
    if mode == "tamper":
        path.write_bytes(b"x" * path.stat().st_size)
    elif mode == "delete":
        storage.delete(host.docs[0])
    else:
        os.utime(path, (1, 1))
    with pytest.raises(PriorArtError, match="SOURCE_UNAVAILABLE_OR_CHANGED"):
        assess(host)


def test_returned_frozen_snapshot_and_detached_view_cannot_change_store(host):
    snapshot = save(host)
    detached = review_documents(snapshot.content)
    detached["manual_search"]["limitations"] = "forged coverage"
    assert review_documents(host.wf.snapshot(host.docs[0], **PRINCIPAL).content)["manual_search"]["limitations"] == INCOMPLETE.limitations
    with pytest.raises(FrozenInstanceError):
        snapshot.dossier_revision = 9


def test_corrupt_audit_chain_is_rejected(host):
    snapshot = save(host)
    event = replace(snapshot.audit[0], sha256="f" * 64)
    record = host.wf._records[host.docs[0]]
    host.wf._records[host.docs[0]] = replace(record, snapshot=replace(snapshot, audit=(event,)))
    with pytest.raises(PriorArtError, match="AUDIT_INTEGRITY_FAILED"):
        host.wf.snapshot(host.docs[0], **PRINCIPAL)


@pytest.mark.parametrize("url", ["javascript:alert(1)", "file:///private", "http://example.invalid",
    "https://user:secret@example.invalid", "https://example.invalid/%0A", "https://"])
def test_unsafe_urls_are_rejected_without_fetch(url):
    with pytest.raises(PriorArtError):
        replace(REF, source_url=url)


@pytest.mark.parametrize("change", [{"citation": ""}, {"source": " "},
    {"retrieved_on": "2026-02-30"}, {"retrieved_on": "20261122"},
    {"kind": "UNKNOWN"}, {"reference_id": "../source"}, {"citation": "x" * 1025},
    {"source": "private\x00content"}])
def test_invalid_reference_fields_are_sanitized(change):
    with pytest.raises(PriorArtError) as exc:
        replace(REF, **change)
    assert "private" not in str(exc.value)


@pytest.mark.parametrize("change", [{"references": (REF, REF)}, {"references": [REF]},
    {"references": (object(),)}, {"search_scope": ""}, {"limitations": ""},
    {"status": "COMPLETE_PATENTABLE"}, {"status": "MANUAL_SEARCH_RECORDED", "references": ()}])
def test_invalid_manual_record_rejected(change):
    with pytest.raises(PriorArtError):
        replace(INCOMPLETE, **change)


def test_future_retrieval_date_not_treated_as_actual_evidence(host):
    future = replace(INCOMPLETE, references=(replace(REF, retrieved_on="2999-01-01"),))
    with pytest.raises(PriorArtError, match="FUTURE_RETRIEVAL_DATE"):
        save(host, future)


def test_clock_failure_and_rollback_fail_closed(host):
    save(host); decide(host)
    host.clock[0] -= timedelta(days=1)
    with pytest.raises(PriorArtError, match="CLOCK_ROLLBACK"):
        assess(host)
    host.clock[0] = datetime(2026, 11, 22)
    with pytest.raises(PriorArtError, match="CLOCK_UNAVAILABLE"):
        assess(host)


def test_audit_capacity_preserves_history_and_rejects_further_writes(host):
    host.wf = ManualPriorArtWorkflow(host.app.state.document_storage, host.app.state.document_registry,
        authorizer=host.authority, clock=lambda: host.clock[0], max_audit_events=2)
    save(host); decide(host)
    with pytest.raises(PriorArtError, match="AUDIT_CAPACITY_REACHED"):
        save(host, revision=1)
    assert assess(host).allowed
    assert len(host.wf.snapshot(host.docs[0], **PRINCIPAL).audit) == 2


def test_callback_reentrancy_cannot_overwrite_a_new_decision(host):
    save(host)
    active = [False]
    def authority(request):
        if request.action == "CONTINUE_DRAFT" and not active[0]:
            active[0] = True
            decide(host, "STOP")
        return True
    host.wf._authorizer = authority
    with pytest.raises(PriorArtError, match="STALE_DOSSIER_REVISION"):
        decide(host)
    assert assess(host).code == "HUMAN_STOPPED"


def test_callback_record_capacity_rechecked_before_commit(host):
    first, second = host.docs
    def authority(request):
        if request.document_id == first:
            save(host, doc=second)
        return True
    host.wf = ManualPriorArtWorkflow(host.app.state.document_storage, host.app.state.document_registry,
        authorizer=authority, clock=lambda: host.clock[0], max_records=1)
    with pytest.raises(PriorArtError, match="CAPACITY_REACHED"):
        save(host, doc=first)
    assert host.wf.snapshot(second, **PRINCIPAL).dossier_revision == 1


@pytest.mark.parametrize("bad", ["../file", "not-an-id", {}, None])
def test_malformed_document_identity_fails_closed(host, bad):
    with pytest.raises(PriorArtError, match="INVALID_DOCUMENT_ID"):
        host.wf.snapshot(bad, **PRINCIPAL)


def test_callback_source_mutation_is_denied_before_record_commit(host):
    def authority(request):
        path = host.app.state.document_storage.path_for(request.document_id)
        path.write_bytes(b"x" * path.stat().st_size)
        return True
    host.wf._authorizer = authority
    with pytest.raises(PriorArtError, match="SOURCE_UNAVAILABLE_OR_CHANGED"):
        save(host)
    assert host.docs[0] not in host.wf._records


def test_callback_exception_never_leaks_manual_content(host):
    def authority(_):
        raise RuntimeError("sensitive manual search content")
    host.wf._authorizer = authority
    with pytest.raises(PriorArtError, match="^AUTHORIZATION_REQUIRED$"):
        save(host)
    assert host.docs[0] not in host.wf._records
