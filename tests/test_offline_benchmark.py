from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from tools import offline_benchmark as benchmark


def minimal_report() -> dict:
    return {
        "schema_version": "1.0.0",
        "task_id": "P1-005",
        "authorization": benchmark.AUTHORIZATION,
        "generated_at": "2026-10-01T00:00:00+00:00",
        "environment": {"provider_api_calls": "NONE"},
        "config": {"warmups": 0, "samples": 1},
        "cases": [{
            "name": "case",
            "status": "MEASURED",
            "workload": {},
            "observed": {},
            "timing": benchmark.calculate_statistics([10.0]),
        }],
    }


def test_synthetic_fixtures_are_byte_reproducible_and_within_limits():
    pdf_a = benchmark.synthetic_pdf(2)
    pdf_b = benchmark.synthetic_pdf(2)
    docx_a = benchmark.synthetic_docx(3)
    docx_b = benchmark.synthetic_docx(3)
    assert pdf_a == pdf_b
    assert docx_a == docx_b
    assert len(pdf_a) < 10 * 1024 * 1024
    assert len(docx_a) < 10 * 1024 * 1024


def test_statistics_use_median_and_nearest_rank_p95():
    result = benchmark.calculate_statistics([1, 2, 3, 4, 100])
    assert result["median_ms"] == 3
    assert result["p95_ms"] == 100
    assert result["sample_count"] == 5


def test_measure_excludes_warmups_and_collects_observed_metadata():
    calls = []
    result = benchmark.measure(
        "unit", lambda: calls.append(1) or {"count": 1}, warmups=2, samples=3, workload={"size": 1}
    )
    assert len(calls) == 5
    assert result["timing"]["sample_count"] == 3
    assert result["observed"] == {"count": 1}


@pytest.mark.parametrize(
    "kwargs",
    ({"warmups": -1}, {"samples": 0}, {"profile": "unknown"}),
)
def test_invalid_configuration_is_rejected(kwargs):
    with pytest.raises(ValueError):
        benchmark.BenchmarkConfig(**kwargs)


def test_report_schema_and_json_serialization_are_stable():
    report = minimal_report()
    benchmark.validate_report(report)
    restored = json.loads(json.dumps(report))
    benchmark.validate_report(restored)


def test_threshold_evaluation_reports_pass_and_fail():
    report = minimal_report()
    assert benchmark.evaluate_thresholds(report, {"case": {"median_ms_max": 11}})["status"] == "PASS"
    failure = benchmark.evaluate_thresholds(report, {"case": {"p95_ms_max": 9}})
    assert failure["status"] == "FAIL"
    assert failure["failures"][0]["actual"] == 10


def test_ci_profile_executes_all_backend_stage_categories():
    report = benchmark.run_benchmark(benchmark.BenchmarkConfig(warmups=0, samples=1, profile="ci", include_browser=False))
    names = {case["name"] for case in report["cases"]}
    assert names == {
        "upload_document_validation_pdf_ci",
        "pdf_parsing_ci",
        "docx_parsing_ci",
        "structured_draft_validation",
        "docx_render_export",
        "representative_offline_backend_e2e",
    }
    assert report["environment"]["provider_api_calls"] == "NONE"
    assert report["environment"]["live_flags"] == {
        "RUN_OPENAI_LIVE_TESTS": "0",
        "RUN_OPENAI_DRAFT_LIVE_TESTS": "0",
    }


def test_browser_command_forces_live_flags_off_and_removes_api_key(tmp_path: Path):
    completed = Mock(returncode=0)
    result_path = tmp_path / "browser.json"

    def fake_run(_npm, env):
        assert env["RUN_OPENAI_LIVE_TESTS"] == "0"
        assert env["RUN_OPENAI_DRAFT_LIVE_TESTS"] == "0"
        assert "OPENAI_API_KEY" not in env
        assert env["P1_005_EXTERNAL_SERVERS"] == "1"
        result_path.write_text(json.dumps({"workload": {}, "observed": {}, "samples_ms": [1.0]}), encoding="utf-8")
        return completed

    with patch.object(benchmark.shutil, "which", return_value="npm"), patch.object(
        benchmark, "_run_browser_processes", side_effect=fake_run
    ):
        case = benchmark.run_browser_benchmark(benchmark.BenchmarkConfig(warmups=0, samples=1), result_path)
    assert case["timing"]["sample_count"] == 1


def test_command_exit_behavior_writes_json_and_propagates_threshold_failure(tmp_path: Path):
    output = tmp_path / "report.json"
    thresholds = tmp_path / "thresholds.json"
    thresholds.write_text(json.dumps({"case": {"median_ms_max": 9}}), encoding="utf-8")
    with patch.object(benchmark, "run_benchmark", return_value=minimal_report()):
        assert benchmark.main(["--output", str(output), "--skip-browser"]) == 0
        assert json.loads(output.read_text(encoding="utf-8"))["task_id"] == "P1-005"
        assert benchmark.main(["--output", str(output), "--skip-browser", "--thresholds", str(thresholds)]) == 2


def test_command_returns_one_for_execution_error():
    with patch.object(benchmark, "run_benchmark", side_effect=RuntimeError("synthetic failure")):
        assert benchmark.main(["--skip-browser"]) == 1
