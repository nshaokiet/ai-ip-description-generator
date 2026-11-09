"""PREAPI-E fixture inventory checks; never construct a product runtime."""

import hashlib
import json
import shutil
import sys

import pytest

from eval.semantic.v1.tools.fixture_readiness import PACKAGE, inspect_fixture, main


def copied_package(tmp_path):
    target = tmp_path / "package"
    (target / "gold").mkdir(parents=True)
    shutil.copyfile(PACKAGE / "manifest.json", target / "manifest.json")
    for source in (PACKAGE / "gold").glob("*.json"):
        shutil.copyfile(source, target / "gold" / source.name)
    return target


def test_accepted_inventory_and_runtime_separation():
    report = inspect_fixture()
    assert report["result"] == "FIXTURE_VALIDATED"
    assert (report["case_count"], report["item_count"]) == (6, 154)
    assert report["importance_counts"] == {"KEY": 102, "SECONDARY": 52}
    assert report["product_runtime"] == "NOT_DETERMINED"
    assert report["product_run_count"] == 0
    assert report["provider_execution"] == "NOT_RUN"
    assert len({row["case_id"] for row in report["gold_files"]}) == 6
    assert all(row["review_status"] == "ACCEPTED" for row in report["gold_files"])


def test_report_is_deterministic_and_does_not_mutate_gold():
    paths = [PACKAGE / "manifest.json", *(PACKAGE / "gold").glob("*.json")]
    before = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}
    assert inspect_fixture() == inspect_fixture()
    assert before == {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}


def test_missing_gold_fails_closed(tmp_path):
    package = copied_package(tmp_path)
    (package / "gold" / "eval-en-002.json").unlink()
    with pytest.raises(ValueError, match="inventory"):
        inspect_fixture(package)


def test_duplicate_gold_id_fails_closed(tmp_path):
    package = copied_package(tmp_path)
    path = package / "gold" / "eval-en-002.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["items"][1]["gold_id"] = data["items"][0]["gold_id"]
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError):
        inspect_fixture(package)


def test_unaccepted_gold_cannot_report_validated(tmp_path):
    package = copied_package(tmp_path)
    path = package / "gold" / "eval-en-002.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data.update(review_status="PENDING_HUMAN", reviewed_by=None, reviewed_at=None)
    path.write_text(json.dumps(data), encoding="utf-8")
    assert inspect_fixture(package)["result"] == "FIXTURE_FAILED"


def test_cli_cannot_overwrite_gold(tmp_path, monkeypatch):
    package = copied_package(tmp_path)
    target = package / "gold" / "eval-en-002.json"
    before = target.read_bytes()
    monkeypatch.setattr(sys, "argv", ["fixture_readiness", "--package", str(package), "--json-out", str(target)])
    with pytest.raises(SystemExit):
        main()
    assert target.read_bytes() == before
