"""PREAPI-C1 synthetic, provider-free custody acceptance checks."""

from __future__ import annotations

import json
import threading
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from backend.app.core.config import Settings
from backend.app.main import create_app
from backend.app.services.core_pipeline import CorePipelineOrchestrator
from backend.app.services.preapi_source_custody import (
    ABSOLUTE_SECONDS, IDLE_SECONDS, CustodyError, TrustedCustodyCoordinator,
)
from backend.app.services.uspto_offline_renderer import FILES
from tests.backend.test_document_parsing import (
    paragraph_xml, synthetic_docx, synthetic_pdf, table_xml,
)
from tests.e2e.provider_tripwire import ProviderTripwire
from backend.app.schemas.analysis_input import ExtractionInputEnvelope
from tests.backend.test_core_pipeline_e2e_offline import (
    ValidatingFakeDraftRuntime, ValidatingFakeExtractionRuntime,
)


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = json.loads((ROOT / "tests/fixtures/invention-reconstruction/v1.0.0/representative-system.json").read_text(encoding="utf-8"))
SOURCE_TEXT = FIXTURE["source_envelope"]["source_units"][0]["content"]


class SyntheticRuntime:
    synthetic_only = True
    def __init__(self, mutate=None):
        self.mutate = mutate

    def run_extraction(self, envelope, *, correlation_id=None):
        analysis = deepcopy(FIXTURE["structured_analysis"])
        analysis["document_metadata"] = envelope.document_metadata.model_dump(exclude_none=True)
        evidence = analysis["evidence"][0]
        evidence["evidence_id"] = envelope.source_units[0].evidence_id
        evidence["document_id"] = envelope.document_metadata.document_id
        evidence["evidence_type"] = envelope.source_units[0].evidence_type
        evidence["locator"] = envelope.source_units[0].locator.model_dump(exclude_none=True)
        if self.mutate:
            self.mutate(analysis)
        return SimpleNamespace(analysis=analysis)


@pytest.fixture
def setup(tmp_path):
    app = create_app(Settings(storage_root=tmp_path / "uploads"))
    clock = [1000.0]
    custody = TrustedCustodyCoordinator(
        app.state.document_storage, app.state.document_registry,
        app.state.document_preparation_service, output_root=tmp_path / "outputs",
        enabled=True, clock=lambda: clock[0],
        review_authorizer=lambda actor, context, decision: (actor, context) in {
            ("synthetic-human", "offline-fixture"), ("human", "fixture"),
        } and decision in {"CONTENT_REVIEW_ACKNOWLEDGED", "CLAIMS_INCOMPLETE_ACKNOWLEDGED"},
    )
    with TestClient(app) as client:
        yield client, app, custody, clock


def upload(client, kind="pdf", text=SOURCE_TEXT):
    if kind == "pdf":
        payload = synthetic_pdf([text])
        name, media = "synthetic-optical-controller.pdf", "application/pdf"
    else:
        payload = synthetic_docx([paragraph_xml(text), table_xml([["Synthetic table entry"]])])
        name = "synthetic-optical-controller.docx"
        media = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    response = client.post("/api/documents", files={"file": (name, payload, media)})
    assert response.status_code == 201, response.text
    return response.json()["document_id"]


def configs():
    p3 = {"source_document_synthetic": True}
    p4 = {
        "language": "en", "target_jurisdiction": "US",
        "requested_claim_types": ["SYSTEM", "METHOD", "COMPOSITION"],
        "max_dependent_claims_per_family": 4,
        "source_document_synthetic": True,
        "selected_solution_id": "IR-SOL-0001",
        "p2_003_generation_config": deepcopy(p3),
    }
    return p3, p4


def commit(env, *, kind="pdf", runtime=None, owner="trusted-owner", text=SOURCE_TEXT):
    client, app, custody, _ = env
    document_id = upload(client, kind, text)
    p3, p4 = configs()
    receipt = custody.commit_upload(
        document_id, owner=owner, extraction_runtime=runtime or SyntheticRuntime(),
        p2_003_generation_config=p3, p2_004_generation_config=p4,
    )
    assert app.state.document_registry.get(document_id) is None
    assert not app.state.document_storage.path_for(document_id).exists()
    return receipt


def review_and_render(custody, receipt, owner="trusted-owner"):
    custody.acknowledge_review(
        receipt.custody_id, owner=owner, revision_token=receipt.revision_token,
        actor="synthetic-human", context="offline-fixture",
    )
    if receipt.claims_review_required:
        custody.acknowledge_incomplete_claims(
            receipt.custody_id, owner=owner, revision_token=receipt.revision_token,
            actor="synthetic-human", context="offline-fixture", acknowledge=True,
        )
    return custody.render(receipt.custody_id, owner=owner, revision_token=receipt.revision_token)


def assert_code(code, function, *args, **kwargs):
    with pytest.raises(CustodyError) as captured:
        function(*args, **kwargs)
    assert captured.value.code == code


def test_v2_01_pdf_trusted_intake_to_four_artifacts_with_tripwire(setup):
    _, _, custody, _ = setup
    tripwire = ProviderTripwire().install()
    try:
        receipt = commit(setup)
        assert receipt.evidence_count == 1
        record = custody._records[receipt.custody_id]
        assert len(record.originals) == 7
        assert receipt.envelope_sha256 == record.digests["source_envelope"]
        result = review_and_render(custody, receipt)
        assert result.state == "RENDERED"
        assert tuple(item.filename for item in result.manifest) == FILES
        assert all(item.size_bytes > 1000 for item in result.manifest)
        for item in result.manifest:
            assert custody.download(result.custody_id, owner="trusted-owner", revision_token=result.revision_token, filename=item.filename)
        tripwire.assert_no_unexpected_activity()
        assert tripwire.snapshot()["provider_api_requests"] == 0
    finally:
        tripwire.close()


def test_v2_02_docx_locator_and_expiry(setup):
    _, _, custody, clock = setup
    receipt = commit(setup, kind="docx")
    units = custody._records[receipt.custody_id].originals["source_envelope"]["source_units"]
    assert [item["evidence_type"] for item in units] == ["TEXT", "TABLE"]
    assert len({item["evidence_id"] for item in units}) == 2
    result = review_and_render(custody, receipt)
    clock[0] += IDLE_SECONDS
    assert_code("SESSION_UNAVAILABLE", custody.status, result.custody_id, owner="trusted-owner", revision_token=result.revision_token)
    assert not (custody.output_root / receipt.custody_id).exists()


def test_v2_03_foreign_analysis_and_self_consistent_pair_rejected(setup):
    client, _, custody, _ = setup
    first = upload(client, text=SOURCE_TEXT)
    other = commit(setup, text=SOURCE_TEXT + " Other source.")
    foreign = deepcopy(custody._records[other.custody_id].originals["structured_analysis"])
    class ForeignRuntime:
        synthetic_only = True
        def run_extraction(self, *_args, **_kwargs):
            return SimpleNamespace(analysis=foreign)
    p3, p4 = configs()
    assert_code("INTAKE_REJECTED", custody.commit_upload, first, owner="trusted-owner", extraction_runtime=ForeignRuntime(), p2_003_generation_config=p3, p2_004_generation_config=p4)
    assert custody._records[other.custody_id].manifest == ()


def test_v2_04_pipeline_result_cannot_create_custody(setup):
    client, app, custody, _ = setup
    document_id = upload(client)
    pipeline = CorePipelineOrchestrator(
        app.state.document_storage, app.state.document_preparation_service,
        ValidatingFakeExtractionRuntime(), ValidatingFakeDraftRuntime(),
    )
    result = pipeline.run_pipeline(document_id)
    assert result.analysis and result.draft
    assert not hasattr(result, "source_envelope")
    assert not app.state.document_storage.path_for(document_id).exists()
    assert_code("SOURCE_MISSING", custody.commit_upload, document_id, owner="trusted-owner", extraction_runtime=SyntheticRuntime(), p2_003_generation_config=configs()[0], p2_004_generation_config=configs()[1])


@pytest.mark.parametrize("change", ["analysis", "p3", "p4"])
def test_v2_05_revision_invalidates_review_and_export(setup, change):
    _, _, custody, _ = setup
    old = commit(setup)
    review_and_render(custody, old)
    if change == "analysis":
        analysis = deepcopy(custody._records[old.custody_id].originals["structured_analysis"])
        analysis["title_candidates"][0]["rationale"] = "Describes the synthetic optical controller system."
        kwargs = {"structured_analysis": analysis}
    elif change == "p3":
        p3 = deepcopy(custody._records[old.custody_id].originals["p2_003_generation_config"])
        p3["selected_title_candidate_id"] = "IR-TITLE-0001"
        kwargs = {"p2_003_generation_config": p3}
    else:
        p4 = deepcopy(custody._records[old.custody_id].originals["p2_004_generation_config"])
        p4["max_dependent_claims_per_family"] = 3
        kwargs = {"p2_004_generation_config": p4}
    result = custody.revise(old.custody_id, owner="trusted-owner", revision_token=old.revision_token, **kwargs)
    assert result.revision == 2 and result.state == "REVIEW_PENDING" and result.manifest == ()
    assert_code("STALE_REVISION", custody.download, old.custody_id, owner="trusted-owner", revision_token=old.revision_token, filename=FILES[0])


@pytest.mark.parametrize("mutation", [
    lambda a: a["evidence"][0].update(evidence_id="EV-FOREIGN"),
    lambda a: a["evidence"][0].update(locator={"page": 99}),
    lambda a: a["evidence"][0].update(excerpt="Forged source excerpt"),
    lambda a: a["evidence"].append(deepcopy(a["evidence"][0])),
])
def test_v2_06_invalid_evidence_rejected_and_upload_cleaned(setup, mutation):
    client, app, custody, _ = setup
    document_id = upload(client)
    p3, p4 = configs()
    assert_code("INTAKE_REJECTED", custody.commit_upload, document_id, owner="trusted-owner", extraction_runtime=SyntheticRuntime(mutation), p2_003_generation_config=p3, p2_004_generation_config=p4)
    assert app.state.document_registry.get(document_id) is None
    assert not app.state.document_storage.path_for(document_id).exists()


def test_v2_07_claims_require_separate_acknowledgment(setup):
    _, _, custody, _ = setup
    receipt = commit(setup)
    assert receipt.claims_review_required
    assert_code("REVIEW_REQUIRED", custody.render, receipt.custody_id, owner="trusted-owner", revision_token=receipt.revision_token)
    content = custody.acknowledge_review(receipt.custody_id, owner="trusted-owner", revision_token=receipt.revision_token, actor="human", context="fixture")
    assert content.state == "CLAIMS_REVIEW_REQUIRED" and content.manifest == ()
    assert_code("REVIEW_REQUIRED", custody.render, receipt.custody_id, owner="trusted-owner", revision_token=receipt.revision_token)
    assert_code("CLAIMS_REVIEW_REQUIRED", custody.acknowledge_incomplete_claims, receipt.custody_id, owner="trusted-owner", revision_token=receipt.revision_token, actor="human", context="fixture", acknowledge=False)
    custody.acknowledge_incomplete_claims(receipt.custody_id, owner="trusted-owner", revision_token=receipt.revision_token, actor="human", context="fixture", acknowledge=True)
    result = custody.render(receipt.custody_id, owner="trusted-owner", revision_token=receipt.revision_token)
    assert result.manifest
    assert custody._records[receipt.custody_id].package["review_boundary"]["filing_ready"] is False


def test_v2_08_package_without_originals_cannot_render(setup):
    _, _, custody, _ = setup
    receipt = commit(setup)
    review_and_render(custody, receipt)
    custody._records[receipt.custody_id].originals.pop("source_envelope")
    assert_code("PROVENANCE_MISMATCH", custody.download, receipt.custody_id, owner="trusted-owner", revision_token=receipt.revision_token, filename=FILES[0])


def test_v2_09_wrong_owner_paths_and_stale_token(setup):
    _, _, custody, _ = setup
    first = commit(setup)
    second = commit(setup, owner="second-owner")
    rendered = review_and_render(custody, first)
    assert_code("SESSION_UNAVAILABLE", custody.download, first.custody_id, owner="second-owner", revision_token=rendered.revision_token, filename=FILES[0])
    assert_code("EXPORT_UNAVAILABLE", custody.download, first.custody_id, owner="trusted-owner", revision_token=rendered.revision_token, filename="../" + FILES[0])
    assert custody.status(second.custody_id, owner="second-owner", revision_token=second.revision_token).state == "REVIEW_PENDING"


def test_v2_10_interrupted_render_and_cleanup_failure_fail_closed(setup):
    _, _, custody, clock = setup
    receipt = commit(setup)
    custody.acknowledge_review(receipt.custody_id, owner="trusted-owner", revision_token=receipt.revision_token, actor="human", context="fixture")
    custody.acknowledge_incomplete_claims(receipt.custody_id, owner="trusted-owner", revision_token=receipt.revision_token, actor="human", context="fixture", acknowledge=True)
    def interrupted_render(*_args, **kwargs):
        staged = kwargs["output_dir"] / ".partial-render"
        staged.mkdir()
        for name in FILES[:2]:
            (staged / name).write_bytes(b"incomplete synthetic artifact")
        raise RuntimeError("interrupted")
    with patch("backend.app.services.preapi_source_custody.render_uspto_document_package", side_effect=interrupted_render):
        assert_code("RENDER_INCOMPLETE", custody.render, receipt.custody_id, owner="trusted-owner", revision_token=receipt.revision_token)
    assert custody.status(receipt.custody_id, owner="trusted-owner", revision_token=receipt.revision_token).manifest == ()
    assert not (custody.output_root / receipt.custody_id).exists()
    result = custody.render(receipt.custody_id, owner="trusted-owner", revision_token=receipt.revision_token)
    with patch("backend.app.services.preapi_source_custody.shutil.rmtree", side_effect=OSError("denied")):
        clock[0] += IDLE_SECONDS
        assert_code("SESSION_UNAVAILABLE", custody.download, result.custody_id, owner="trusted-owner", revision_token=result.revision_token, filename=FILES[0])
    assert custody.cleanup_failures == [receipt.custody_id]
    assert custody._records[receipt.custody_id].manifest == ()


def test_source_hash_mismatch_and_duplicate_evidence_fail_before_publication(setup):
    client, app, custody, _ = setup
    document_id = upload(client)
    app.state.document_storage.path_for(document_id).write_bytes(b"tampered")
    p3, p4 = configs()
    assert_code("SOURCE_HASH_MISMATCH", custody.commit_upload, document_id, owner="trusted-owner", extraction_runtime=SyntheticRuntime(), p2_003_generation_config=p3, p2_004_generation_config=p4)
    assert not custody._records
    duplicate_id = upload(client)
    original_prepare = custody.preparation.prepare_extraction_input

    def duplicate_envelope(value):
        envelope = original_prepare(value)
        return ExtractionInputEnvelope.model_construct(
            document_metadata=envelope.document_metadata,
            source_units=[envelope.source_units[0], envelope.source_units[0]],
        )

    with patch.object(custody.preparation, "prepare_extraction_input", side_effect=duplicate_envelope):
        assert_code("INTAKE_REJECTED", custody.commit_upload, duplicate_id, owner="trusted-owner", extraction_runtime=SyntheticRuntime(), p2_003_generation_config=p3, p2_004_generation_config=p4)
    assert app.state.document_registry.get(duplicate_id) is None
    assert not custody._records


def test_failed_reads_do_not_refresh_idle_and_absolute_lifetime_is_hard(setup):
    _, _, custody, clock = setup
    receipt = commit(setup)
    clock[0] += IDLE_SECONDS - 1
    custody.status(receipt.custody_id, owner="trusted-owner", revision_token=receipt.revision_token)
    assert_code("SESSION_UNAVAILABLE", custody.status, receipt.custody_id, owner="wrong-owner", revision_token=receipt.revision_token)
    clock[0] += 1
    assert_code("SESSION_UNAVAILABLE", custody.status, receipt.custody_id, owner="trusted-owner", revision_token=receipt.revision_token)

    second = commit(setup)
    for index in range(4):
        clock[0] += 1700
        if index % 2 == 0:
            custody.acknowledge_review(second.custody_id, owner="trusted-owner", revision_token=second.revision_token, actor="human", context="fixture")
            second = custody.acknowledge_incomplete_claims(second.custody_id, owner="trusted-owner", revision_token=second.revision_token, actor="human", context="fixture", acknowledge=True)
        else:
            p4 = deepcopy(custody._records[second.custody_id].originals["p2_004_generation_config"])
            p4["max_dependent_claims_per_family"] = 3 if index == 1 else 4
            second = custody.revise(second.custody_id, owner="trusted-owner", revision_token=second.revision_token, p2_004_generation_config=p4)
    clock[0] += ABSOLUTE_SECONDS - 6800
    assert_code("SESSION_UNAVAILABLE", custody.status, second.custody_id, owner="trusted-owner", revision_token=second.revision_token)


def test_parallel_duplicate_intake_conflicts_without_second_record(setup):
    client, _, custody, _ = setup
    document_id = upload(client)
    entered, release = threading.Event(), threading.Event()
    class WaitingRuntime(SyntheticRuntime):
        def run_extraction(self, envelope, *, correlation_id=None):
            entered.set()
            assert release.wait(10)
            return super().run_extraction(envelope, correlation_id=correlation_id)
    result = []
    p3, p4 = configs()
    def run():
        result.append(custody.commit_upload(document_id, owner="trusted-owner", extraction_runtime=WaitingRuntime(), p2_003_generation_config=p3, p2_004_generation_config=p4))
    worker = threading.Thread(target=run)
    worker.start()
    try:
        assert entered.wait(10)
        assert_code("INTAKE_CONFLICT", custody.commit_upload, document_id, owner="trusted-owner", extraction_runtime=SyntheticRuntime(), p2_003_generation_config=p3, p2_004_generation_config=p4)
    finally:
        release.set()
        worker.join(10)
    assert len(result) == len(custody._records) == 1


def test_expiry_during_render_never_publishes_manifest(setup):
    _, _, custody, clock = setup
    receipt = commit(setup)
    custody.acknowledge_review(receipt.custody_id, owner="trusted-owner", revision_token=receipt.revision_token, actor="human", context="fixture")
    custody.acknowledge_incomplete_claims(receipt.custody_id, owner="trusted-owner", revision_token=receipt.revision_token, actor="human", context="fixture", acknowledge=True)
    from backend.app.services import preapi_source_custody as module
    original = module.render_uspto_document_package
    def slow_render(*args, **kwargs):
        result = original(*args, **kwargs)
        clock[0] += IDLE_SECONDS
        return result
    with patch.object(module, "render_uspto_document_package", side_effect=slow_render):
        assert_code("SESSION_UNAVAILABLE", custody.render, receipt.custody_id, owner="trusted-owner", revision_token=receipt.revision_token)
    assert custody._records[receipt.custody_id].manifest == ()
    assert not (custody.output_root / receipt.custody_id).exists()


def test_disabled_restart_and_untrusted_review_context_fail_closed(setup, tmp_path):
    _, app, custody, _ = setup
    receipt = commit(setup)
    assert_code("REVIEW_REQUIRED", custody.acknowledge_review, receipt.custody_id, owner="trusted-owner", revision_token=receipt.revision_token, actor="forged", context="fixture")
    restarted = TrustedCustodyCoordinator(
        app.state.document_storage, app.state.document_registry,
        app.state.document_preparation_service, output_root=tmp_path / "restart",
        enabled=True,
    )
    assert_code("SESSION_UNAVAILABLE", restarted.status, receipt.custody_id, owner="trusted-owner", revision_token=receipt.revision_token)
    disabled = TrustedCustodyCoordinator(
        app.state.document_storage, app.state.document_registry,
        app.state.document_preparation_service, output_root=tmp_path / "disabled",
    )
    assert_code("CUSTODY_DISABLED", disabled.status, receipt.custody_id, owner="trusted-owner", revision_token=receipt.revision_token)


def test_modified_artifact_revokes_entire_bundle(setup):
    _, _, custody, _ = setup
    receipt = commit(setup)
    result = review_and_render(custody, receipt)
    record = custody._records[receipt.custody_id]
    path = record.output_directory / (record.package["package_id"] + "-p2-006") / FILES[0]
    path.write_bytes(b"corrupted synthetic output")
    assert_code("EXPORT_UNAVAILABLE", custody.status, result.custody_id, owner="trusted-owner", revision_token=result.revision_token)
    assert record.manifest == () and record.state == "ABORTED"
    assert_code("SESSION_UNAVAILABLE", custody.download, result.custody_id, owner="trusted-owner", revision_token=result.revision_token, filename=FILES[1])
