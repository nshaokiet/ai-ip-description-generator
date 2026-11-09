"""PRODUCT-001A: real registered bytes, retained provenance, review and export."""

from __future__ import annotations

import hashlib
import io
import json
import zipfile
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
from types import SimpleNamespace
from threading import Event
from xml.etree import ElementTree

import pytest
from fastapi.testclient import TestClient
from pypdf import PdfReader

from backend.app.core.config import Settings
from backend.app.main import create_app
from backend.app.services.custody_review import (
    C1ReviewTarget, ReviewProjectionError, freeze_originals, review_documents,
)
from backend.app.services.preapi_source_custody import CustodyError, IDLE_SECONDS
from backend.app.services.product_synthetic_workflow import (
    OfflineSyntheticWorkflow, ProductWorkflowError, SyntheticFixtureIdentity,
)
from backend.app.services.supported_draft_claims_validation import sha256_canonical
from backend.app.services.uspto_offline_renderer import FILES
from tests.e2e.provider_tripwire import ProviderTripwire


ROOT = Path(__file__).resolve().parents[2]
INPUTS = ROOT / "tests/fixtures/product-synthetic/v1.0.0"
MANIFEST = json.loads((INPUTS / "manifest.json").read_text())
TEMPLATE = json.loads((ROOT / "tests/fixtures/invention-reconstruction/v1.0.0/representative-system.json").read_text())
IDENTITIES = tuple(SyntheticFixtureIdentity(item["sha256"], item["media_type"], item["size_bytes"])
                   for item in MANIFEST["fixtures"])


API_INPUTS = ROOT / "tests/fixtures/api-ready/v1.0.0"
API_MANIFEST = json.loads((API_INPUTS / "manifest.json").read_text())
RESEARCH_B = API_MANIFEST["fixtures"][1]
TWO_SOURCES = ["controller.pdf", "research-b.docx"]
B_IDENTITY = SyntheticFixtureIdentity(
    RESEARCH_B["sha256"], RESEARCH_B["media_type"], RESEARCH_B["size_bytes"],
)


def source_template(entry):
    payload = (ROOT / entry["analysis_path"]).read_bytes()
    if entry["source_id"] == "controller-a":
        payload = payload.replace(b"\r\n", b"\n")  # Hash the existing Git blob, not checkout EOLs.
    if len(payload) != entry["analysis_size_bytes"] or hashlib.sha256(payload).hexdigest() != entry["analysis_sha256"]:
        raise ValueError("Synthetic analysis identity mismatch")
    value = json.loads(payload)
    return value["structured_analysis"] if entry["analysis_json_pointer"] else value


class SourceCheckingRuntime:
    synthetic_only = True

    def __init__(self, mutate=None):
        self.mutate = mutate
        self.envelopes = []

    def run_extraction(self, envelope, *, correlation_id=None):
        # This is a deliberately narrow test runtime, not semantic AI extraction.
        # Reusing expected analysis is safe only after the actual parsed source matches.
        assert len(envelope.source_units) == 1
        unit = envelope.source_units[0]
        metadata = envelope.document_metadata
        if (metadata.sha256, metadata.media_type) == (RESEARCH_B["sha256"], RESEARCH_B["media_type"]):
            if hashlib.sha256(unit.content.encode()).hexdigest() != RESEARCH_B["parsed_content_sha256"]:
                raise ValueError("Unsupported synthetic technical content")
            analysis = source_template(RESEARCH_B)
        else:
            known = any(metadata.sha256 == item["sha256"] and metadata.media_type == item["media_type"]
                        for item in MANIFEST["fixtures"] if item["filename"].startswith("controller."))
            if not known or unit.content != TEMPLATE["source_envelope"]["source_units"][0]["content"]:
                raise ValueError("Unsupported synthetic technical content")
            analysis = deepcopy(source_template(API_MANIFEST["fixtures"][0]))
        self.envelopes.append(envelope)
        analysis["document_metadata"] = envelope.document_metadata.model_dump(exclude_none=True)
        old_id = analysis["evidence"][0]["evidence_id"]

        def rebind(value):
            if isinstance(value, dict):
                return {key: rebind(child) for key, child in value.items()}
            if isinstance(value, list):
                return [rebind(child) for child in value]
            return unit.evidence_id if value == old_id else value

        analysis = rebind(analysis)
        analysis["evidence"][0].update(
            document_id=envelope.document_metadata.document_id,
            evidence_type=unit.evidence_type, locator=unit.locator.model_dump(exclude_none=True),
        )
        if self.mutate:
            self.mutate(analysis)
        return SimpleNamespace(analysis=analysis)


@pytest.fixture
def host(tmp_path):
    app = create_app(Settings(storage_root=tmp_path / "uploads"))
    clock, authorized = [1000.0], [True]
    runtime = SourceCheckingRuntime()
    workflow = OfflineSyntheticWorkflow(
        app.state.document_storage, app.state.document_registry,
        app.state.document_preparation_service, output_root=tmp_path / "exports",
        extraction_runtime=runtime, fixtures=IDENTITIES + (B_IDENTITY,),
        authorize_invocation=lambda: authorized[0],
        review_authorizer=lambda actor, context, decision: (
            actor == "test-human" and context == "trusted-local-review"
            and decision in {"CONTENT_REVIEW_ACKNOWLEDGED", "CLAIMS_INCOMPLETE_ACKNOWLEDGED"}
        ), enabled=True, clock=lambda: clock[0],
    )
    with TestClient(app) as client:
        yield SimpleNamespace(app=app, client=client, workflow=workflow, runtime=runtime,
                              clock=clock, authorized=authorized, tmp=tmp_path)


def register(host, name="controller.pdf"):
    entry = (RESEARCH_B if name == "research-b.docx" else
             next(item for item in MANIFEST["fixtures"] if item["filename"] == name))
    payload = (ROOT / entry["path"] if name == "research-b.docx" else INPUTS / name).read_bytes()
    assert hashlib.sha256(payload).hexdigest() == entry["sha256"]
    assert len(payload) == entry["size_bytes"]
    response = host.client.post("/api/documents", files={"file": (name, payload, entry["media_type"])})
    assert response.status_code == 201, response.text
    return response.json()["document_id"], payload


def start(host, name="controller.pdf"):
    document_id, payload = register(host, name)
    ref = host.workflow.start(document_id)
    assert ref.document_id == document_id != "doc-ir-001"
    assert host.app.state.document_registry.get(document_id) is None
    assert not host.app.state.document_storage.path_for(document_id).exists()
    return ref, payload


def acknowledge(host, ref, *, claims=False, digest=None, actor="test-human"):
    projection = host.workflow.review(ref)
    return host.workflow.acknowledge(
        ref, review_snapshot_sha256=digest or projection.review_snapshot_sha256,
        actor=actor, context="trusted-local-review", acknowledge=True, incomplete_claims=claims,
    )


def export(host, ref):
    snapshot = acknowledge(host, ref)
    if snapshot.claims_review_required:
        acknowledge(host, ref, claims=True)
    return host.workflow.render(ref)


@pytest.mark.parametrize("name", ["controller.pdf", "controller.docx", "research-b.docx"])
def test_new_upload_to_complete_review_and_four_valid_artifacts(host, name):
    tripwire = ProviderTripwire().install()
    try:
        ref, source = start(host, name)
        snapshot = host.workflow.review(ref)
        documents = review_documents(snapshot.originals)
        assert set(documents) == {
            "source_envelope", "structured_analysis", "reconstruction", "specification",
            "p2_003_generation_config", "supported_claims", "p2_004_generation_config",
        }
        assert documents["specification"]["review_boundary"]["claims_runtime_implemented"] is False
        claims = documents["supported_claims"]
        assert claims["status"] == "HUMAN_CONFIRMATION_REQUIRED" and claims["claims"] == []
        assert snapshot.claims_review_required
        expected = source_template(RESEARCH_B if name == "research-b.docx" else API_MANIFEST["fixtures"][0])
        assert documents["structured_analysis"]["technical_problems"] == expected["technical_problems"]
        assert documents["structured_analysis"]["technical_solutions"] == expected["technical_solutions"]
        assert all(item["essentiality"] == "UNKNOWN" for item in documents["reconstruction"]["invention_model"]["elements"])
        marker, foreign = (("perforated membrane", "calibration coefficient") if name == "research-b.docx"
                           else ("calibration coefficient", "perforated membrane"))
        assert snapshot.source_sha256 == hashlib.sha256(source).hexdigest()
        assert documents["source_envelope"]["document_metadata"]["document_id"] == ref.document_id
        assert documents["structured_analysis"]["document_metadata"] == documents["source_envelope"]["document_metadata"]
        assert documents["source_envelope"]["source_units"] == [
            host.runtime.envelopes[0].source_units[0].model_dump()
        ]
        assert dict(snapshot.originals_sha256) == {key: sha256_canonical(value) for key, value in documents.items()}
        assert documents["specification"]["review_package"]
        assert documents["supported_claims"]["review_package"]
        assert snapshot.synthetic_draft and not snapshot.filing_ready
        assert "revision_token" not in repr(snapshot)
        result = export(host, ref)
        assert result.review_snapshot_sha256 == snapshot.review_snapshot_sha256
        assert tuple(item.filename for item in result.artifacts) == FILES
        for item in result.artifacts:
            payload = host.workflow.download(ref, filename=item.filename, manifest_sha256=result.manifest_sha256)
            assert hashlib.sha256(payload).hexdigest() == item.sha256
            assert len(payload) == item.size_bytes
            if item.filename.endswith(".pdf"):
                pages = PdfReader(io.BytesIO(payload)).pages
                assert len(pages) > 0
                rendered_text = " ".join(page.extract_text() for page in pages)
            else:
                with zipfile.ZipFile(io.BytesIO(payload)) as docx:
                    assert docx.testzip() is None
                    rendered_text = " ".join(
                        text for member in docx.namelist()
                        if member.startswith("word/") and member.endswith(".xml")
                        for text in ElementTree.fromstring(docx.read(member)).itertext()
                    )
            normalized = " ".join(rendered_text.lower().split())
            assert marker in normalized and foreign not in normalized
            assert "draft" in normalized and "claims incomplete" in normalized
        assert result.synthetic_draft and not result.filing_ready
        host.workflow.abort(ref)
        assert not (host.tmp / "exports" / result.custody_id).exists()
        tripwire.assert_no_unexpected_activity()
        assert tripwire.snapshot()["provider_api_requests"] == 0
    finally:
        tripwire.close()


@pytest.mark.parametrize("name", TWO_SOURCES)
def test_projection_is_complete_detached_and_recursively_immutable(host, name):
    ref, _ = start(host, name)
    snapshot = host.workflow.review(ref)
    with pytest.raises(FrozenInstanceError):
        snapshot.originals.members = ()
    detached = review_documents(snapshot.originals)
    for document in detached.values():
        document.clear()
        document["forged"] = True
    assert host.workflow.review(ref) == snapshot
    assert "forged" not in repr(host.workflow.review(ref))


@pytest.mark.parametrize("name", TWO_SOURCES)
def test_human_and_separate_incomplete_claims_gates(host, name):
    ref, _ = start(host, name)
    with pytest.raises(CustodyError, match="Synthetic"):
        host.workflow.render(ref)
    with pytest.raises(CustodyError) as denied:
        acknowledge(host, ref, actor="unauthorized")
    assert denied.value.code == "REVIEW_REQUIRED"
    with pytest.raises(ProductWorkflowError):
        acknowledge(host, ref, digest="0" * 64)
    assert acknowledge(host, ref).state == "CLAIMS_REVIEW_REQUIRED"
    with pytest.raises(CustodyError):
        host.workflow.render(ref)
    assert acknowledge(host, ref, claims=True).state == "REVIEW_RECORDED"
    assert host.workflow.render(ref).artifacts


@pytest.mark.parametrize("name", TWO_SOURCES)
def test_cross_document_review_export_and_stale_revision_rejected(host, name):
    first, _ = start(host, name)
    other = next(item for item in TWO_SOURCES if item != name)
    second, _ = start(host, other)
    a, b = host.workflow.review(first), host.workflow.review(second)
    assert a.review_snapshot_sha256 != b.review_snapshot_sha256
    with pytest.raises(ProductWorkflowError):
        acknowledge(host, second, digest=a.review_snapshot_sha256)
    with pytest.raises(ProductWorkflowError):
        host.workflow.review(replace(first, document_id=second.document_id))
    old_export = export(host, first)
    other_export = export(host, second)
    with pytest.raises(ProductWorkflowError):
        host.workflow.download(second, filename=FILES[0], manifest_sha256=old_export.manifest_sha256)
    assert old_export.manifest_sha256 != other_export.manifest_sha256
    analysis = review_documents(a.originals)["structured_analysis"]
    analysis["title_candidates"][0]["rationale"] = "Updated synthetic review rationale."
    new = host.workflow.revise(first, structured_analysis=analysis)
    assert new.revision == 2
    assert not (host.tmp / "exports" / old_export.custody_id).exists()
    with pytest.raises(ProductWorkflowError):
        host.workflow.download(first, filename=FILES[0], manifest_sha256=old_export.manifest_sha256)
    with pytest.raises(ProductWorkflowError):
        acknowledge(host, new, digest=a.review_snapshot_sha256)
    with pytest.raises(CustodyError):
        host.workflow.render(new)
    fresh = export(host, new)
    with pytest.raises(ProductWorkflowError):
        host.workflow.download(new, filename=FILES[0], manifest_sha256=old_export.manifest_sha256)
    assert fresh.manifest_sha256 != old_export.manifest_sha256


def test_mixed_document_revision_input_rejected_without_replacing_current(host):
    first, _ = start(host)
    second, _ = start(host, "research-b.docx")
    foreign = review_documents(host.workflow.review(second).originals)["structured_analysis"]
    with pytest.raises(CustodyError) as error:
        host.workflow.revise(first, structured_analysis=foreign)
    assert error.value.code == "INVALID_REVISION_INPUT"
    assert host.workflow.review(first).revision == 1


@pytest.mark.parametrize("mutation", [
    lambda analysis: analysis.update(evidence=[]),
    lambda analysis: analysis["evidence"][0].update(excerpt="Not in the uploaded source"),
    lambda analysis: analysis["evidence"][0].update(document_id="doc-foreign"),
])
@pytest.mark.parametrize("name", TWO_SOURCES)
def test_missing_or_forged_evidence_cleans_uploaded_source(host, mutation, name):
    document_id, _ = register(host, name)
    host.runtime.mutate = mutation
    with pytest.raises(CustodyError) as error:
        host.workflow.start(document_id)
    assert error.value.code == "INTAKE_REJECTED"
    assert host.app.state.document_registry.get(document_id) is None
    assert not host.app.state.document_storage.path_for(document_id).exists()
    assert not host.workflow._handles


@pytest.mark.parametrize("name", ["unsupported.pdf", "empty.pdf"])
def test_unsupported_or_missing_technical_content_is_not_fabricated(host, name):
    if name == "empty.pdf":
        response = host.client.post("/api/documents", files={
            "file": (name, (INPUTS / name).read_bytes(), "application/pdf"),
        })
        assert response.status_code == 422
        assert response.json()["error"]["code"] == "pdf_text_layer_required"
        assert not host.runtime.envelopes and not host.workflow._handles
        assert len(host.app.state.document_registry) == 0
        assert not list(host.app.state.document_storage.root.iterdir())
        return
    document_id, _ = register(host, name)
    with pytest.raises(CustodyError):
        host.workflow.start(document_id)
    assert not host.workflow._handles
    assert host.app.state.document_registry.get(document_id) is None
    assert not host.app.state.document_storage.path_for(document_id).exists()


@pytest.mark.parametrize("name", TWO_SOURCES)
def test_unknown_bytes_and_modified_registered_bytes_are_not_admitted(host, name):
    document_id, _ = register(host, name)
    path = host.app.state.document_storage.path_for(document_id)
    path.write_bytes(path.read_bytes() + b"tampered")
    with pytest.raises(ProductWorkflowError) as error:
        host.workflow.start(document_id)
    assert error.value.code == "SOURCE_NOT_ADMITTED"
    assert not host.runtime.envelopes
    assert path.exists()  # admission doesn't delete an unowned upload
    with pytest.raises(ProductWorkflowError):
        host.workflow.start("a" * 32)


def test_unauthorized_invocations_cannot_read_acknowledge_or_export(host):
    ref, _ = start(host)
    snapshot = host.workflow.review(ref)
    host.authorized[0] = False
    for operation in (
        lambda: host.workflow.review(ref), lambda: host.workflow.render(ref),
        lambda: host.workflow.abort(ref),
        lambda: host.workflow.acknowledge(ref, review_snapshot_sha256=snapshot.review_snapshot_sha256,
                                          actor="test-human", context="trusted-local-review", acknowledge=True),
        lambda: host.workflow.download(ref, filename=FILES[0], manifest_sha256="0" * 64),
        lambda: host.workflow.start("a" * 32),
    ):
        with pytest.raises(ProductWorkflowError) as error:
            operation()
        assert error.value.code == "UNAUTHORIZED"


@pytest.mark.parametrize("name", TWO_SOURCES)
def test_reads_do_not_refresh_expiry_and_export_is_removed(host, name):
    ref, _ = start(host, name)
    result = export(host, ref)
    host.clock[0] += IDLE_SECONDS - 1
    host.workflow.review(ref)
    host.clock[0] += 1
    with pytest.raises(CustodyError):
        host.workflow.download(ref, filename=FILES[0], manifest_sha256=result.manifest_sha256)
    assert not (host.tmp / "exports" / result.custody_id).exists()
    assert not host.workflow._handles


@pytest.mark.parametrize("tamper", ["file", "mime", "revision", "digest"])
@pytest.mark.parametrize("name", TWO_SOURCES)
def test_tampered_manifest_or_artifact_never_returns_bytes(host, tamper, name):
    ref, _ = start(host, name)
    result = export(host, ref)
    record = host.workflow._custody._records[result.custody_id]  # adversarial test only
    if tamper == "file":
        next(record.output_directory.rglob(FILES[0])).write_bytes(b"%PDF-forged")
    else:
        item = record.manifest[0]
        changes = {"mime": {"media_type": "text/plain"}, "revision": {"revision": 99},
                   "digest": {"sha256": "0" * 64}}[tamper]
        record.manifest = (replace(item, **changes),) + record.manifest[1:]
    with pytest.raises((CustodyError, ProductWorkflowError)):
        host.workflow.download(ref, filename=FILES[0], manifest_sha256=result.manifest_sha256)


def test_bound_c1_review_cannot_be_bypassed_by_direct_acknowledgment(host):
    ref, _ = start(host)
    receipt = host.workflow._handles[ref.session_id]
    with pytest.raises(CustodyError) as error:
        host.workflow._custody.acknowledge_review(
            receipt.custody_id, owner=host.workflow._owner, revision_token=receipt.revision_token,
            actor="test-human", context="trusted-local-review",
        )
    assert error.value.code == "REVIEW_REQUIRED"


def test_failed_initial_projection_aborts_without_publishing_session(host, monkeypatch):
    document_id, _ = register(host)
    def reject(*args, **kwargs):
        raise ReviewProjectionError()
    monkeypatch.setattr(host.workflow._custody, "get_review_projection", reject)
    with pytest.raises(ReviewProjectionError):
        host.workflow.start(document_id)
    assert not host.workflow._handles
    assert all(record.state == "ABORTED" and not record.originals
               for record in host.workflow._custody._records.values())
    assert not host.app.state.document_storage.path_for(document_id).exists()


def test_partial_render_failure_cleans_outputs_and_allows_explicit_retry(host, monkeypatch):
    from backend.app.services import preapi_source_custody as c1
    ref, _ = start(host)
    acknowledge(host, ref)
    acknowledge(host, ref, claims=True)
    real_renderer = c1.render_uspto_document_package
    def fail(*args, **kwargs):
        real_renderer(*args, **kwargs)
        raise RuntimeError("synthetic interrupted renderer")
    monkeypatch.setattr(c1, "render_uspto_document_package", fail)
    with pytest.raises(CustodyError):
        host.workflow.render(ref)
    assert not list((host.tmp / "exports").iterdir())
    assert host.workflow.review(ref).state == "REVIEW_RECORDED"
    monkeypatch.setattr(c1, "render_uspto_document_package", real_renderer)
    assert host.workflow.render(ref).artifacts


@pytest.mark.parametrize("payload", [
    {"bad": float("nan")}, {"bad": object()}, {1: "not a string key"},
    {"large": "a" * 1_048_577}, {"many": [None] * 100_001},
])
def test_projection_limits_fail_without_partial_data(payload):
    with pytest.raises(ReviewProjectionError):
        freeze_originals(payload)


def test_absence_null_and_array_order_survive_projection():
    value = {"array": [None, False, 1, "x"], "null": None, "empty": {}}
    assert review_documents(freeze_originals(value)) == value
    nested = value
    for _ in range(66):
        nested = {"child": nested}
    with pytest.raises(ReviewProjectionError):
        freeze_originals(nested)


def test_live_authority_revocation_and_expiry_during_acknowledgment(host):
    ref, _ = start(host)
    def expire(actor, context, decision):
        host.clock[0] += IDLE_SECONDS
        return True
    host.workflow._custody.review_authorizer = expire  # adversarial callback timing
    with pytest.raises(CustodyError):
        acknowledge(host, ref)
    record = next(iter(host.workflow._custody._records.values()))
    assert record.state == "EXPIRED" and record.review is None


def test_expiry_during_projection_returns_no_valid_snapshot(host, monkeypatch):
    from backend.app.services import preapi_source_custody as c1
    ref, _ = start(host)
    original = c1.freeze_originals
    def expire(originals):
        frozen = original(originals)
        host.clock[0] += IDLE_SECONDS
        return frozen
    monkeypatch.setattr(c1, "freeze_originals", expire)
    with pytest.raises(CustodyError):
        host.workflow.review(ref)


def test_actual_c1_target_prevents_cross_custody_acknowledgment(host):
    first, _ = start(host)
    second, _ = start(host)
    receipt = host.workflow._handles[first.session_id]
    snapshot = host.workflow.review(first)
    other = host.workflow._handles[second.session_id]
    host.workflow._pending_target = C1ReviewTarget(
        snapshot.coordinator_instance_id, receipt.custody_id, receipt.document_id,
        host.workflow._owner, receipt.revision,
        hashlib.sha256(receipt.revision_token.encode()).hexdigest(),
        snapshot.review_snapshot_sha256, "test-human", "trusted-local-review",
        "CONTENT_REVIEW_ACKNOWLEDGED",
    )
    try:
        with pytest.raises(CustodyError) as error:
            host.workflow._custody.acknowledge_review(
                other.custody_id, owner=host.workflow._owner, revision_token=other.revision_token,
                actor="test-human", context="trusted-local-review",
            )
        assert error.value.code == "REVIEW_REQUIRED"
        assert host.workflow.review(second).state == "REVIEW_PENDING"
    finally:
        host.workflow._pending_target = None


def test_projection_and_revision_are_serialized_without_mixed_data(host, monkeypatch):
    from backend.app.services import preapi_source_custody as c1
    ref, _ = start(host)
    analysis = review_documents(host.workflow.review(ref).originals)["structured_analysis"]
    analysis["title_candidates"][0]["rationale"] = "Changed revision rationale."
    entered, release = Event(), Event()
    original = c1.freeze_originals
    def pause(originals):
        entered.set()
        assert release.wait(timeout=10)
        return original(originals)
    monkeypatch.setattr(c1, "freeze_originals", pause)
    with ThreadPoolExecutor(max_workers=2) as pool:
        reading = pool.submit(host.workflow.review, ref)
        try:
            assert entered.wait(timeout=10)
            revising = pool.submit(host.workflow.revise, ref, structured_analysis=analysis)
            assert not revising.done()
        finally:
            release.set()
        old_snapshot, new_ref = reading.result(timeout=20), revising.result(timeout=20)
    assert old_snapshot.revision == 1 and new_ref.revision == 2
    assert old_snapshot.review_snapshot_sha256 != host.workflow.review(new_ref).review_snapshot_sha256


def test_source_policy_is_pinned_empty_by_default_and_execution_is_opt_in(host):
    from tests.backend.test_document_parsing import synthetic_pdf
    payload = synthetic_pdf(["An unapproved synthetic upload with a familiar filename."])
    response = host.client.post("/api/documents", files={"file": ("controller.pdf", payload, "application/pdf")})
    document_id = response.json()["document_id"]
    with pytest.raises(ProductWorkflowError):
        host.workflow.start(document_id)
    assert host.app.state.document_storage.path_for(document_id).exists()
    kwargs = dict(output_root=host.tmp / "other", extraction_runtime=SourceCheckingRuntime(),
                  authorize_invocation=lambda: True, review_authorizer=lambda *args: True)
    for enabled, fixtures in [(True, ()), (False, IDENTITIES)]:
        workflow = OfflineSyntheticWorkflow(
            host.app.state.document_storage, host.app.state.document_registry,
            host.app.state.document_preparation_service, enabled=enabled, fixtures=fixtures, **kwargs,
        )
        registered, _ = register(host)
        with pytest.raises((ProductWorkflowError, CustodyError)):
            workflow.start(registered)
    with pytest.raises(ProductWorkflowError):
        OfflineSyntheticWorkflow(
            host.app.state.document_storage, host.app.state.document_registry,
            host.app.state.document_preparation_service,
            **dict(kwargs, extraction_runtime=SimpleNamespace(synthetic_only=False)),
        )


def test_capacity_is_bounded_and_abort_releases_a_slot(host):
    refs = [start(host)[0] for _ in range(4)]
    pending, _ = register(host)
    with pytest.raises(ProductWorkflowError) as error:
        host.workflow.start(pending)
    assert error.value.code == "CAPACITY"
    assert host.app.state.document_registry.get(pending)
    host.workflow.abort(refs[0])
    replacement = host.workflow.start(pending)
    assert replacement.document_id == pending
    assert len(host.workflow._handles) == 4


@pytest.fixture(autouse=True)
def offline_provider_guard():
    guard = ProviderTripwire().install()
    try:
        yield guard
        guard.assert_no_unexpected_activity()
    finally:
        guard.close()


def test_two_source_manifest_and_analysis_identities():
    assert API_MANIFEST["scope"] == "SYNTHETIC_TEST_ONLY"
    assert API_MANIFEST["production_admitted"] is False
    assert API_MANIFEST["c2_pilot_admitted"] is False
    assert API_MANIFEST["provider_budget_usd"] == 0
    assert len(API_MANIFEST["fixtures"]) == 2
    assert {entry["filename"] for entry in API_MANIFEST["fixtures"]} == set(TWO_SOURCES)
    assert len({entry["sha256"] for entry in API_MANIFEST["fixtures"]}) == 2
    assert len({entry["parsed_content_sha256"] for entry in API_MANIFEST["fixtures"]}) == 2
    for entry in API_MANIFEST["fixtures"]:
        payload = (ROOT / entry["path"]).read_bytes()
        assert len(payload) == entry["size_bytes"]
        assert hashlib.sha256(payload).hexdigest() == entry["sha256"]
        assert entry["provenance"]
        assert entry["analysis_media_type"] == "application/json"
        source_template(entry)  # Verify analysis bytes independently of source bytes.
    b = source_template(RESEARCH_B)
    assert b["document_metadata"]["sha256"] == RESEARCH_B["sha256"]
    assert b["document_metadata"]["media_type"] == RESEARCH_B["media_type"]
    assert b["document_metadata"]["file_name"] == RESEARCH_B["filename"]
    assert b["technical_problems"] != TEMPLATE["structured_analysis"]["technical_problems"]


@pytest.mark.parametrize("name", TWO_SOURCES)
def test_parsed_source_identity_and_cross_source_fake_analysis_rejected(host, name):
    ref, _ = start(host, name)
    envelope = host.runtime.envelopes[-1]
    entry = next(item for item in API_MANIFEST["fixtures"] if item["filename"] == name)
    unit = envelope.source_units[0]
    assert hashlib.sha256(unit.content.encode()).hexdigest() == entry["parsed_content_sha256"]
    actual = review_documents(host.workflow.review(ref).originals)["structured_analysis"]
    assert actual["evidence"][0]["locator"] == unit.locator.model_dump(exclude_none=True)
    assert actual["evidence"][0]["excerpt"] in unit.content
    if name == "research-b.docx":
        assert actual["evidence"][0]["locator"] == source_template(RESEARCH_B)["evidence"][0]["locator"]
    other = next(item for item in API_MANIFEST["fixtures"] if item["filename"] != name)
    foreign = source_template(other)
    # Even with metadata/locator rebound by the fake, foreign evidence must fail grounding.
    def swap(analysis):
        metadata = analysis["document_metadata"]
        evidence = analysis["evidence"][0]
        analysis.clear()
        analysis.update(deepcopy(foreign))
        old = analysis["evidence"][0]["evidence_id"]
        def rebind(value):
            if isinstance(value, dict):
                return {key: rebind(child) for key, child in value.items()}
            if isinstance(value, list):
                return [rebind(child) for child in value]
            return evidence["evidence_id"] if value == old else value
        bound = rebind(analysis)
        analysis.clear()
        analysis.update(bound)
        analysis["document_metadata"] = metadata
        analysis["evidence"][0].update({key: value for key, value in evidence.items() if key != "excerpt"})
    host.runtime.mutate = swap
    document_id, _ = register(host, name)
    with pytest.raises(CustodyError) as error:
        host.workflow.start(document_id)
    assert error.value.code == "INTAKE_REJECTED"
    assert host.app.state.document_registry.get(document_id) is None
    assert not host.app.state.document_storage.path_for(document_id).exists()
    assert host.workflow.review(ref).revision == 1
    host.workflow.abort(ref)


@pytest.mark.parametrize("name", TWO_SOURCES)
@pytest.mark.parametrize("tamper", ["sha256", "media_type", "content"])
def test_fake_extractor_rejects_mismatched_source_identity(host, name, tamper):
    ref, _ = start(host, name)
    envelope = host.runtime.envelopes[-1].model_copy(deep=True)
    if tamper == "content":
        other = next(item for item in API_MANIFEST["fixtures"] if item["filename"] != name)
        foreign = source_template(other)["evidence"][0]["excerpt"]
        envelope.source_units[0].content = foreign
    else:
        setattr(envelope.document_metadata, tamper, "0" * 64 if tamper == "sha256" else "text/plain")
    before = len(host.runtime.envelopes)
    with pytest.raises(ValueError, match="Unsupported synthetic technical content"):
        host.runtime.run_extraction(envelope)
    assert len(host.runtime.envelopes) == before
    host.workflow.abort(ref)
