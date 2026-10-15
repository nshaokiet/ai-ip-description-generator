"""AI-CONV-002 deterministic orchestration and provenance-integrity tests."""

from __future__ import annotations

import inspect
import json
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path

import pytest
from docx import Document

from backend.app.services.supported_draft_claims_validation import sha256_canonical
from backend.app.services.uspto_offline_orchestration import (
    ORCHESTRATION_CONTRACT_VERSION,
    PROVENANCE_KEYS,
    OfflineUSPTOOrchestrator,
    USPTOOfflineOrchestrationError,
)
from backend.app.services.uspto_offline_renderer import CLAIMS_INCOMPLETE, FILES


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "tests/fixtures/invention-reconstruction/v1.0.0/representative-system.json"
)


def request_inputs() -> dict:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    p3_config = {"source_document_synthetic": True}
    p4_config = {
        "language": "en",
        "target_jurisdiction": "US",
        "requested_claim_types": ["SYSTEM", "METHOD", "COMPOSITION"],
        "max_dependent_claims_per_family": 4,
        "source_document_synthetic": True,
        "selected_solution_id": "IR-SOL-0001",
        "p2_003_generation_config": deepcopy(p3_config),
    }
    return {
        "source_envelope": fixture["source_envelope"],
        "structured_analysis": fixture["structured_analysis"],
        "p2_003_generation_config": p3_config,
        "p2_004_generation_config": p4_config,
    }


def alternate_document_inputs() -> dict:
    values = request_inputs()
    replacements = {
        "doc-ir-001": "doc-ir-002",
        "synthetic-optical-controller.pdf": "synthetic-optical-controller-two.pdf",
        "b" * 64: "c" * 64,
    }

    def replace(value):
        if isinstance(value, dict):
            return {key: replace(item) for key, item in value.items()}
        if isinstance(value, list):
            return [replace(item) for item in value]
        return replacements.get(value, value)

    return replace(values)


def run_package(
    orchestrator: OfflineUSPTOOrchestrator,
    values: dict | None = None,
):
    values = request_inputs() if values is None else values
    return orchestrator.run_uspto_v2_offline_pipeline(**values)


def assert_safe(error: USPTOOfflineOrchestrationError, forbidden: str) -> None:
    serialized = json.dumps(error.__dict__, sort_keys=True)
    assert str(error) == USPTOOfflineOrchestrationError.safe_message
    assert forbidden not in serialized


def test_complete_offline_pipeline_retains_all_seven_inputs_and_fails_closed_claims():
    orchestrator = OfflineUSPTOOrchestrator(session_id_factory=lambda: "session-a")
    status = run_package(orchestrator)
    package = orchestrator.get_validated_package(
        status.session_id, expected_revision_token=status.revision_token
    )

    assert status.contract_version == ORCHESTRATION_CONTRACT_VERSION == "1.0.1"
    assert status.state == "PACKAGE_VALID"
    assert status.revision == 1
    assert status.retained_provenance_keys == PROVENANCE_KEYS
    assert {
        "source_envelope",
        "structured_analysis",
        "p2_003_generation_config",
        "p2_004_generation_config",
        "reconstruction",
        "specification",
        "supported_claims",
        "package",
    } == dict(status.artifact_digests).keys()
    assert package["filing_view"]["claims"]["status"] == "HUMAN_CONFIRMATION_REQUIRED"
    assert package["filing_view"]["claims"]["claims"] == []
    assert package["review_package"]["original_p2_003"]["review_boundary"][
        "claims_runtime_implemented"
    ] is False
    reconstruction = orchestrator._sessions[status.session_id].reconstruction
    assert reconstruction is not None
    assert {item["essentiality"] for item in reconstruction["invention_model"]["elements"]} == {
        "UNKNOWN"
    }
    assert package["review_package"]["original_p2_004"]["claims"] == []


def test_repeated_inputs_have_identical_stage_outputs_and_package_identity():
    identifiers = iter(("session-a", "session-b"))
    orchestrator = OfflineUSPTOOrchestrator(session_id_factory=lambda: next(identifiers))
    first = run_package(orchestrator)
    second = run_package(orchestrator)
    first_record = orchestrator._sessions[first.session_id]
    second_record = orchestrator._sessions[second.session_id]

    assert first_record.reconstruction == second_record.reconstruction
    assert first_record.specification == second_record.specification
    assert first_record.supported_claims == second_record.supported_claims
    assert first_record.package == second_record.package
    assert first.package_id == second.package_id


def test_package_copy_is_mutation_isolated_and_revalidated_on_every_read():
    orchestrator = OfflineUSPTOOrchestrator(session_id_factory=lambda: "session-a")
    status = run_package(orchestrator)
    package = orchestrator.get_validated_package(
        status.session_id, expected_revision_token=status.revision_token
    )
    package["review_boundary"]["filing_ready"] = True

    fresh = orchestrator.get_validated_package(
        status.session_id, expected_revision_token=status.revision_token
    )
    assert fresh["review_boundary"]["filing_ready"] is False


def test_render_uses_retained_bundle_returns_path_free_manifest_and_cleans_up(tmp_path):
    orchestrator = OfflineUSPTOOrchestrator(session_id_factory=lambda: "session-render")
    status = orchestrator.run_uspto_v2_offline_pipeline(
        **request_inputs(), output_dir=tmp_path
    )
    rendered = tmp_path / f"{status.package_id}-p2-006"

    assert status.state == "RENDERED"
    assert tuple(item.filename for item in status.render_manifest) == FILES
    assert all(item.size_bytes > 1000 for item in status.render_manifest)
    assert set(path.name for path in rendered.iterdir()) == set(FILES)
    assert str(tmp_path) not in json.dumps(asdict(status), sort_keys=True)
    document = Document(rendered / FILES[1])
    document_text = "\n".join(paragraph.text for paragraph in document.paragraphs)
    assert CLAIMS_INCOMPLETE in document_text

    orchestrator.cleanup_session(
        status.session_id, expected_revision_token=status.revision_token
    )
    assert not rendered.exists()
    with pytest.raises(USPTOOfflineOrchestrationError) as captured:
        orchestrator.get_session_status(status.session_id)
    assert captured.value.code == "SESSION_NOT_FOUND"


def test_unsafe_render_destination_fails_with_safe_error(tmp_path):
    orchestrator = OfflineUSPTOOrchestrator(session_id_factory=lambda: "session-a")
    status = run_package(orchestrator)
    relative = Path("relative-output")
    with pytest.raises(USPTOOfflineOrchestrationError) as captured:
        orchestrator.render_session(
            status.session_id,
            expected_revision_token=status.revision_token,
            output_dir=relative,
        )
    assert captured.value.code == "UNSAFE_RENDER_DESTINATION"
    assert captured.value.paths == ("/output_dir",)
    assert not tmp_path.joinpath(relative).exists()


def test_render_manifest_tampering_fails_closed_and_cleanup_never_deletes_unknown_file(
    tmp_path,
):
    orchestrator = OfflineUSPTOOrchestrator(session_id_factory=lambda: "session-render")
    status = orchestrator.run_uspto_v2_offline_pipeline(
        **request_inputs(), output_dir=tmp_path
    )
    rendered = tmp_path / f"{status.package_id}-p2-006"
    unknown = rendered / "unknown.txt"
    unknown.write_text("synthetic unexpected file", encoding="utf-8")

    with pytest.raises(USPTOOfflineOrchestrationError) as captured:
        orchestrator.get_session_status(status.session_id)
    assert captured.value.code == "SESSION_INTEGRITY_MISMATCH"
    assert orchestrator._sessions[status.session_id].state == "FAILED"
    assert unknown.exists()
    assert all((rendered / name).exists() for name in FILES)

    unknown.unlink()
    orchestrator.cleanup_session(
        status.session_id, expected_revision_token=status.revision_token
    )
    assert not rendered.exists()


def test_config_change_creates_revision_invalidates_downstream_and_rejects_stale_token():
    orchestrator = OfflineUSPTOOrchestrator(session_id_factory=lambda: "session-a")
    first = run_package(orchestrator)
    values = request_inputs()
    p3 = {
        "source_document_synthetic": True,
        "selected_title_candidate_id": "IR-TITLE-0001",
    }
    p4 = deepcopy(values["p2_004_generation_config"])
    p4["p2_003_generation_config"] = deepcopy(p3)

    revised = orchestrator.revise_session(
        first.session_id,
        expected_revision_token=first.revision_token,
        p2_003_generation_config=p3,
        p2_004_generation_config=p4,
    )
    assert revised.revision == 2
    assert revised.state == "RECONSTRUCTION_READY"
    assert revised.package_id is None
    assert "reconstruction" in dict(revised.artifact_digests)
    assert "specification" not in dict(revised.artifact_digests)

    with pytest.raises(USPTOOfflineOrchestrationError) as captured:
        orchestrator.advance_session(
            first.session_id, expected_revision_token=first.revision_token
        )
    assert captured.value.code == "STALE_REVISION"

    completed = orchestrator.advance_session(
        revised.session_id, expected_revision_token=revised.revision_token
    )
    assert completed.state == "PACKAGE_VALID"
    assert completed.revision == 2


def test_source_identity_change_starts_at_source_and_invalidates_all_outputs():
    orchestrator = OfflineUSPTOOrchestrator(session_id_factory=lambda: "session-a")
    first = run_package(orchestrator)
    changed = alternate_document_inputs()

    revised = orchestrator.revise_session(
        first.session_id,
        expected_revision_token=first.revision_token,
        source_envelope=changed["source_envelope"],
        structured_analysis=changed["structured_analysis"],
    )
    assert revised.state == "SOURCE_READY"
    assert revised.document_id == "doc-ir-002"
    assert revised.source_sha256 == "c" * 64
    assert set(revised.retained_provenance_keys) == {
        "source_envelope",
        "structured_analysis",
        "p2_003_generation_config",
        "p2_004_generation_config",
    }
    completed = orchestrator.advance_session(
        revised.session_id, expected_revision_token=revised.revision_token
    )
    assert completed.state == "PACKAGE_VALID"
    assert completed.package_id != first.package_id


def test_digest_mismatch_is_rejected_before_downstream_validation():
    secret_source_text = "SYNTHETIC PRIVATE SENTENCE MUST NOT LEAK"
    orchestrator = OfflineUSPTOOrchestrator(session_id_factory=lambda: "session-a")
    status = run_package(orchestrator)
    record = orchestrator._sessions[status.session_id]
    record.structured_analysis["background"][0]["text"] = secret_source_text

    with pytest.raises(USPTOOfflineOrchestrationError) as captured:
        orchestrator.validate_session(
            status.session_id, expected_revision_token=status.revision_token
        )
    assert captured.value.code == "SESSION_INTEGRITY_MISMATCH"
    assert_safe(captured.value, secret_source_text)


def test_cross_document_splicing_is_rejected_even_if_digest_index_is_rewritten():
    identifiers = iter(("session-a", "session-b"))
    orchestrator = OfflineUSPTOOrchestrator(session_id_factory=lambda: next(identifiers))
    first = run_package(orchestrator, request_inputs())
    second = run_package(orchestrator, alternate_document_inputs())
    first_record = orchestrator._sessions[first.session_id]
    second_record = orchestrator._sessions[second.session_id]
    second_record.specification = deepcopy(first_record.specification)
    second_record.artifact_digests["specification"] = sha256_canonical(
        second_record.specification
    )

    with pytest.raises(USPTOOfflineOrchestrationError) as captured:
        orchestrator.validate_session(
            second.session_id, expected_revision_token=second.revision_token
        )
    assert captured.value.code == "P2_005_VALIDATION_REJECTED"
    assert captured.value.upstream_code == "UPSTREAM_CONTRACT_INVALID"


def test_package_tampering_is_rejected_even_if_digest_index_is_rewritten():
    orchestrator = OfflineUSPTOOrchestrator(session_id_factory=lambda: "session-a")
    status = run_package(orchestrator)
    record = orchestrator._sessions[status.session_id]
    record.package["review_boundary"]["filing_ready"] = True
    record.artifact_digests["package"] = sha256_canonical(record.package)

    with pytest.raises(USPTOOfflineOrchestrationError) as captured:
        orchestrator.validate_session(
            status.session_id, expected_revision_token=status.revision_token
        )
    assert captured.value.code == "P2_005_VALIDATION_REJECTED"
    assert captured.value.upstream_code == "INVALID_PACKAGE_SCHEMA"


@pytest.mark.parametrize("missing", PROVENANCE_KEYS)
def test_missing_any_of_seven_retained_inputs_blocks_validation(missing):
    orchestrator = OfflineUSPTOOrchestrator(session_id_factory=lambda: "session-a")
    status = run_package(orchestrator)
    record = orchestrator._sessions[status.session_id]
    if missing == "source_envelope":
        record.source_envelope = None
    else:
        setattr(record, missing, None)
    record.artifact_digests.pop(missing, None)

    with pytest.raises(USPTOOfflineOrchestrationError) as captured:
        orchestrator.validate_session(
            status.session_id, expected_revision_token=status.revision_token
        )
    assert captured.value.code in {
        "MISSING_PROVENANCE_INPUT",
        "SOURCE_IDENTITY_MISMATCH",
    }


def test_invalid_configuration_marks_actual_revision_failed_without_leaking_input():
    source_text = "do not expose this synthetic source value"
    values = request_inputs()
    values["p2_003_generation_config"] = {
        "source_document_synthetic": True,
        "source_note": source_text,
    }
    values["p2_004_generation_config"]["p2_003_generation_config"] = deepcopy(
        values["p2_003_generation_config"]
    )
    orchestrator = OfflineUSPTOOrchestrator(session_id_factory=lambda: "session-a")

    with pytest.raises(USPTOOfflineOrchestrationError) as captured:
        run_package(orchestrator, values)
    assert captured.value.code == "P2_003_REJECTED"
    assert captured.value.upstream_code == "INVALID_GENERATION_CONFIG"
    assert_safe(captured.value, source_text)
    assert orchestrator._sessions["session-a"].state == "FAILED"


def test_status_excludes_source_content_file_name_and_server_paths():
    source_phrase = request_inputs()["source_envelope"]["source_units"][0]["content"]
    orchestrator = OfflineUSPTOOrchestrator(session_id_factory=lambda: "session-a")
    status = run_package(orchestrator)
    serialized = json.dumps(asdict(status), sort_keys=True)

    assert source_phrase not in serialized
    assert "synthetic-optical-controller.pdf" not in serialized
    assert "server_path" not in serialized
    assert "output_dir" not in serialized


def test_session_capacity_is_bounded_and_cleanup_releases_slot():
    identifiers = iter(("session-a", "session-b"))
    orchestrator = OfflineUSPTOOrchestrator(
        max_sessions=1, session_id_factory=lambda: next(identifiers)
    )
    first = orchestrator.start_session(**request_inputs())
    with pytest.raises(USPTOOfflineOrchestrationError) as captured:
        orchestrator.start_session(**request_inputs())
    assert captured.value.code == "SESSION_CAPACITY_EXCEEDED"
    orchestrator.cleanup_session(
        first.session_id, expected_revision_token=first.revision_token
    )
    second = orchestrator.start_session(**request_inputs())
    assert second.session_id == "session-b"


def test_orchestrator_has_no_package_only_render_or_public_api_contract():
    signature = inspect.signature(OfflineUSPTOOrchestrator.render_session)
    assert "package" not in signature.parameters
    assert set(signature.parameters) == {
        "self",
        "session_id",
        "expected_revision_token",
        "output_dir",
    }


class _PauseAfterStage(BaseException):
    """Test-only interruption after a real completed stage transition."""


def session_at_stage(orchestrator, stage, monkeypatch):
    status = orchestrator.start_session(**request_inputs())
    if stage == "SOURCE_READY":
        return status
    transition = orchestrator._transition

    def pause(record, target):
        transition(record, target)
        if target == stage:
            raise _PauseAfterStage()

    with monkeypatch.context() as patch:
        patch.setattr(orchestrator, "_transition", pause)
        with pytest.raises(_PauseAfterStage):
            orchestrator.advance_session(
                status.session_id, expected_revision_token=status.revision_token
            )
    return orchestrator.get_session_status(status.session_id)


@pytest.mark.parametrize("stage", [
    "SOURCE_READY", "RECONSTRUCTION_READY", "SPECIFICATION_READY",
    "CLAIMS_REVIEW_REQUIRED", "PACKAGE_VALID",
])
@pytest.mark.parametrize("edit", ["p3", "p4", "both"])
def test_revision_readiness_uses_retained_prerequisites(stage, edit, monkeypatch):
    orchestrator = OfflineUSPTOOrchestrator()
    status = session_at_stage(orchestrator, stage, monkeypatch)
    before = deepcopy(orchestrator._sessions[status.session_id])
    values = request_inputs()
    edits = {}
    if edit in {"p3", "both"}:
        # Explicit released default is semantically equal to the nested P3
        # config, while changing the original retained config representation.
        p3 = deepcopy(values["p2_003_generation_config"])
        p3["language"] = "en"
        edits["p2_003_generation_config"] = p3
    if edit in {"p4", "both"}:
        p4 = deepcopy(values["p2_004_generation_config"])
        p4["max_dependent_claims_per_family"] = 3
        edits["p2_004_generation_config"] = p4
    revised = orchestrator.revise_session(
        status.session_id, expected_revision_token=status.revision_token, **edits
    )
    after = orchestrator._sessions[status.session_id]
    expected = (
        "SOURCE_READY" if before.reconstruction is None else
        "RECONSTRUCTION_READY" if edit != "p4" or before.specification is None else
        "SPECIFICATION_READY"
    )
    assert revised.state == expected
    assert after.reconstruction == before.reconstruction
    assert after.specification == (before.specification if edit == "p4" else None)
    assert after.supported_claims is None and after.package is None
    assert revised.revision == status.revision + 1
    assert revised.revision_token != status.revision_token
    with pytest.raises(USPTOOfflineOrchestrationError, match="Offline USPTO") as stale:
        orchestrator.advance_session(status.session_id, expected_revision_token=status.revision_token)
    assert stale.value.code == "STALE_REVISION"
    completed = orchestrator.advance_session(
        revised.session_id, expected_revision_token=revised.revision_token
    )
    same_inputs = request_inputs() | edits
    fresh = OfflineUSPTOOrchestrator()
    reference = fresh.run_uspto_v2_offline_pipeline(**same_inputs)
    assert completed.state == "PACKAGE_VALID"
    assert orchestrator.get_validated_package(
        completed.session_id, expected_revision_token=completed.revision_token
    ) == fresh.get_validated_package(
        reference.session_id, expected_revision_token=reference.revision_token
    )


@pytest.mark.parametrize("bad", [
    float("nan"), float("inf"), float("-inf"), object(), {1, 2},
    ("silently coercible tuple",), {1: "non-string key"},
], ids=["nan", "inf", "negative-inf", "object", "set", "tuple", "non-string-key"])
@pytest.mark.parametrize("root", [
    "source_envelope", "structured_analysis", "p2_003_generation_config",
    "p2_004_generation_config",
])
def test_revision_rejects_nested_non_json_without_any_mutation(bad, root):
    orchestrator = OfflineUSPTOOrchestrator()
    status = orchestrator.start_session(**request_inputs())
    before = deepcopy(orchestrator._sessions[status.session_id])
    invalid = deepcopy(request_inputs()[root])
    invalid["nested"] = {"items": [bad]}
    with pytest.raises(USPTOOfflineOrchestrationError) as captured:
        orchestrator.revise_session(
            status.session_id, expected_revision_token=status.revision_token,
            **{root: invalid},
        )
    assert captured.value.code == "INVALID_CANONICAL_INPUT"
    assert orchestrator._sessions[status.session_id] == before
    assert orchestrator.get_session_status(status.session_id) == status
    orchestrator.cleanup_session(status.session_id, expected_revision_token=status.revision_token)


def invalid_revision_edits(case):
    values = request_inputs()
    if case in {"nan", "infinity", "object"}:
        values["structured_analysis"]["background"][0]["text"] = (
            object() if case == "object" else float("inf" if case == "infinity" else "nan")
        )
        return {"structured_analysis": values["structured_analysis"]}
    if case == "nested-invalid-analysis":
        values["structured_analysis"]["background"][0]["grounding"]["label"] = "INVALID"
        return {"structured_analysis": values["structured_analysis"]}
    if case == "p3-selection":
        values["p2_003_generation_config"]["selected_title_candidate_id"] = "missing-title"
        return {"p2_003_generation_config": values["p2_003_generation_config"]}
    if case == "p4-selection":
        values["p2_004_generation_config"]["selected_solution_id"] = "missing-solution"
        return {"p2_004_generation_config": values["p2_004_generation_config"]}
    if case == "config-mismatch":
        values["p2_003_generation_config"]["selected_title_candidate_id"] = "IR-TITLE-0001"
        return {"p2_003_generation_config": values["p2_003_generation_config"]}
    if case == "source-mismatch":
        values["source_envelope"]["document_metadata"]["sha256"] = "c" * 64
        return {"source_envelope": values["source_envelope"]}
    raise AssertionError(case)


@pytest.mark.parametrize("rendered", [False, True])
@pytest.mark.parametrize("case", [
    "nan", "infinity", "object", "nested-invalid-analysis", "p3-selection", "p4-selection",
    "config-mismatch", "source-mismatch",
])
def test_rejected_revision_preserves_usable_package_and_render(case, rendered, tmp_path):
    orchestrator = OfflineUSPTOOrchestrator()
    status = orchestrator.run_uspto_v2_offline_pipeline(
        **request_inputs(), output_dir=tmp_path if rendered else None
    )
    before = deepcopy(orchestrator._sessions[status.session_id])
    files = {p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    with pytest.raises(USPTOOfflineOrchestrationError) as captured:
        orchestrator.revise_session(
            status.session_id, expected_revision_token=status.revision_token,
            **invalid_revision_edits(case),
        )
    assert captured.value.code in {"INVALID_CANONICAL_INPUT", "INVALID_REVISION_INPUT"}
    assert orchestrator._sessions[status.session_id] == before
    assert orchestrator.get_session_status(status.session_id) == status
    assert orchestrator.validate_session(
        status.session_id, expected_revision_token=status.revision_token
    ) == status
    assert orchestrator.get_validated_package(
        status.session_id, expected_revision_token=status.revision_token
    ) == before.package
    assert {p: p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()} == files
    assert status.render_manifest == before.render_manifest
    p4 = deepcopy(request_inputs()["p2_004_generation_config"])
    p4["max_dependent_claims_per_family"] = 2
    revised = orchestrator.revise_session(
        status.session_id, expected_revision_token=status.revision_token,
        p2_004_generation_config=p4,
    )
    assert revised.state == "SPECIFICATION_READY"
    assert revised.render_manifest == ()
    assert not list(tmp_path.iterdir())
    completed = orchestrator.advance_session(status.session_id, expected_revision_token=revised.revision_token)
    assert completed.state == "PACKAGE_VALID"
    orchestrator.cleanup_session(status.session_id, expected_revision_token=revised.revision_token)


def test_rejected_rendered_revision_can_be_cleaned_up_directly(tmp_path):
    orchestrator = OfflineUSPTOOrchestrator()
    status = orchestrator.run_uspto_v2_offline_pipeline(**request_inputs(), output_dir=tmp_path)
    with pytest.raises(USPTOOfflineOrchestrationError):
        orchestrator.revise_session(
            status.session_id, expected_revision_token=status.revision_token,
            **invalid_revision_edits("nan"),
        )
    orchestrator.cleanup_session(status.session_id, expected_revision_token=status.revision_token)
    assert not list(tmp_path.iterdir())


def test_revision_token_preparation_failure_preserves_rendered_session(tmp_path, monkeypatch):
    import backend.app.services.uspto_offline_orchestration as module

    orchestrator = OfflineUSPTOOrchestrator()
    status = orchestrator.run_uspto_v2_offline_pipeline(**request_inputs(), output_dir=tmp_path)
    before = deepcopy(orchestrator._sessions[status.session_id])
    p4 = deepcopy(request_inputs()["p2_004_generation_config"])
    p4["max_dependent_claims_per_family"] = 2

    def fail_token(*args):
        raise ValueError("synthetic private error must not escape")

    with monkeypatch.context() as patch:
        patch.setattr(module, "_revision_token", fail_token)
        with pytest.raises(USPTOOfflineOrchestrationError) as captured:
            orchestrator.revise_session(
                status.session_id, expected_revision_token=status.revision_token,
                p2_004_generation_config=p4,
            )
    assert captured.value.code == "INVALID_REVISION_INPUT"
    assert_safe(captured.value, "synthetic private error")
    assert orchestrator._sessions[status.session_id] == before
    assert orchestrator.get_session_status(status.session_id) == status
    orchestrator.cleanup_session(status.session_id, expected_revision_token=status.revision_token)


@pytest.mark.parametrize("deleted_before_failure", [0, 1, 3])
def test_revision_cleanup_failure_never_commits_candidate(deleted_before_failure, tmp_path, monkeypatch):
    orchestrator = OfflineUSPTOOrchestrator()
    status = orchestrator.run_uspto_v2_offline_pipeline(**request_inputs(), output_dir=tmp_path)
    before = deepcopy(orchestrator._sessions[status.session_id])
    p4 = deepcopy(request_inputs()["p2_004_generation_config"])
    p4["max_dependent_claims_per_family"] = 2
    unlink = Path.unlink
    removed = []

    def fail_unlink(path, *args, **kwargs):
        if path.parent == before.render_directory:
            if len(removed) == deleted_before_failure:
                raise PermissionError("synthetic sensitive path")
            removed.append(path.name)
        return unlink(path, *args, **kwargs)

    with monkeypatch.context() as patch:
        patch.setattr(Path, "unlink", fail_unlink)
        with pytest.raises(USPTOOfflineOrchestrationError) as captured:
            orchestrator.revise_session(
                status.session_id, expected_revision_token=status.revision_token,
                p2_004_generation_config=p4,
            )
    assert captured.value.code == "CLEANUP_FAILED"
    assert_safe(captured.value, "synthetic sensitive path")
    failed = orchestrator._sessions[status.session_id]
    assert failed.state == "FAILED" and failed.error_code == "CLEANUP_FAILED"
    assert failed.revision == before.revision and failed.revision_token == before.revision_token
    assert failed.package == before.package
    assert failed.p2_004_generation_config == before.p2_004_generation_config
    assert failed.render_manifest == before.render_manifest
    assert len(list(before.render_directory.iterdir())) == 4 - deleted_before_failure
    if deleted_before_failure:
        with pytest.raises(USPTOOfflineOrchestrationError) as integrity:
            orchestrator.get_session_status(status.session_id)
        assert integrity.value.code == "SESSION_INTEGRITY_MISMATCH"
    else:
        assert orchestrator.get_session_status(status.session_id).state == "FAILED"
        orchestrator.cleanup_session(status.session_id, expected_revision_token=status.revision_token)


def test_failed_intermediate_session_can_revise_and_recover():
    orchestrator = OfflineUSPTOOrchestrator()
    values = request_inputs()
    values["p2_003_generation_config"]["unsupported"] = True
    status = orchestrator.start_session(**values)
    with pytest.raises(USPTOOfflineOrchestrationError):
        orchestrator.advance_session(status.session_id, expected_revision_token=status.revision_token)
    before = deepcopy(orchestrator._sessions[status.session_id].reconstruction)
    assert before is not None
    revised = orchestrator.revise_session(
        status.session_id, expected_revision_token=status.revision_token,
        p2_003_generation_config=request_inputs()["p2_003_generation_config"],
    )
    assert revised.state == "RECONSTRUCTION_READY"
    assert revised.error_code is None
    assert orchestrator._sessions[status.session_id].reconstruction == before
    assert orchestrator.advance_session(
        status.session_id, expected_revision_token=revised.revision_token
    ).state == "PACKAGE_VALID"


def test_cyclic_revision_is_rejected_without_live_mutation():
    orchestrator = OfflineUSPTOOrchestrator()
    status = orchestrator.start_session(**request_inputs())
    cyclic = {}
    cyclic["self"] = cyclic
    with pytest.raises(USPTOOfflineOrchestrationError) as captured:
        orchestrator.revise_session(
            status.session_id, expected_revision_token=status.revision_token,
            structured_analysis=cyclic,
        )
    assert captured.value.code == "INVALID_CANONICAL_INPUT"
    assert orchestrator.get_session_status(status.session_id) == status
    orchestrator.cleanup_session(status.session_id, expected_revision_token=status.revision_token)
