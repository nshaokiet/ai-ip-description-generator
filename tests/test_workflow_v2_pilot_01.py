"""Validate the real synthetic artifact; no operational lifecycle is mocked."""
from copy import deepcopy
import json
from pathlib import Path
import re

import pytest

ARTIFACT = Path(__file__).resolve().parents[1] / "docs/pilots/workflow-v2-pilot-01.md"
METADATA = {
    "pilot_id": "GOV-AGENT-001-F-PILOT-01",
    "workflow_version": 2,
    "activation_commit": "9c291325d409f74bc767f9b870e81d75c9b70802",
    "spec_version": "0.1.0",
    "synthetic_value": 7,
    "expected_value": 15,
    "security_review_required": True,
    "quality_review_required": True,
    "rule": "result = input * 2 + 1",
}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: " + key)
        result[key] = value
    return result


def read_record(text):
    blocks = re.findall(r"^```json\s*\n(.*?)^```[ \t]*$", text, re.M | re.S)
    if len(blocks) != 1:
        raise ValueError("exactly one JSON record required")
    return json.loads(blocks[0], object_pairs_hook=unique_object)


def validate_record(record):
    if type(record) is not dict or set(record) != set(METADATA) | {"cases"}:
        raise ValueError("record fields mismatch")
    for key, expected in METADATA.items():
        if type(record[key]) is not type(expected) or record[key] != expected:
            raise ValueError("metadata mismatch: " + key)
    cases = record["cases"]
    if type(cases) is not list:
        raise ValueError("cases must be a list")
    inputs = []
    for case in cases:
        if type(case) is not dict or set(case) != {"input", "expected_value", "computed_value"}:
            raise ValueError("case fields mismatch")
        if any(type(value) is not int for value in case.values()):
            raise ValueError("case values must be integers, excluding booleans")
        result = case["input"] * 2 + 1
        if case["expected_value"] != result or case["computed_value"] != result:
            raise ValueError("incorrect arithmetic")
        inputs.append(case["input"])
    if inputs not in ([7], [7, 11]):
        raise ValueError("only predefined A or B cases permitted")
    return record


def record_for(inputs):
    return deepcopy(METADATA) | {"cases": [
        {"input": value, "expected_value": value * 2 + 1, "computed_value": value * 2 + 1}
        for value in inputs
    ]}


def test_committed_pilot_record():
    validate_record(read_record(ARTIFACT.read_text(encoding="utf-8")))


@pytest.mark.parametrize("inputs", [[7], [7, 11]])
def test_permitted_stages(inputs):
    validate_record(record_for(inputs))


@pytest.mark.parametrize("inputs", [[], [11], [7, 7], [11, 7], [7, 13], [7, 11, 13]])
def test_reject_missing_duplicate_unexpected_or_reordered_cases(inputs):
    with pytest.raises(ValueError):
        validate_record(record_for(inputs))


@pytest.mark.parametrize("key", list(METADATA))
def test_reject_missing_metadata(key):
    record = record_for([7])
    del record[key]
    with pytest.raises(ValueError):
        validate_record(record)


@pytest.mark.parametrize("key,bad", [
    ("pilot_id", "OTHER"), ("workflow_version", True), ("workflow_version", "2"),
    ("activation_commit", "0" * 40), ("spec_version", "0.1.1"),
    ("synthetic_value", True), ("synthetic_value", 11), ("expected_value", 23),
    ("security_review_required", False), ("security_review_required", 1),
    ("quality_review_required", False), ("quality_review_required", 1),
    ("rule", "result = input * 2"),
])
def test_reject_changed_metadata_or_disabled_review(key, bad):
    record = record_for([7])
    record[key] = bad
    with pytest.raises(ValueError):
        validate_record(record)


@pytest.mark.parametrize("key,bad", [
    ("input", True), ("input", 7.0), ("expected_value", "15"),
    ("expected_value", 14), ("computed_value", 16), ("computed_value", False),
])
def test_reject_bad_case_types_and_results(key, bad):
    record = record_for([7, 11])
    record["cases"][0][key] = bad
    with pytest.raises(ValueError):
        validate_record(record)


def test_reject_missing_and_extra_case_fields():
    for key in ("input", "expected_value", "computed_value"):
        record = record_for([7])
        del record["cases"][0][key]
        with pytest.raises(ValueError):
            validate_record(record)
    record = record_for([7])
    record["cases"][0]["extra"] = 1
    with pytest.raises(ValueError):
        validate_record(record)


@pytest.mark.parametrize("bad", [None, [], "record", {"cases": []}])
def test_reject_invalid_top_level(bad):
    with pytest.raises(ValueError):
        validate_record(bad)


def test_reject_extra_fields_or_non_list_cases():
    for patch in ({"extra": 1}, {"cases": {"input": 7}}):
        with pytest.raises(ValueError):
            validate_record(record_for([7]) | patch)


def test_reject_ambiguous_or_missing_record():
    block = "```json\n" + json.dumps(record_for([7])) + "\n```"
    for text in ("no record", block + "\n" + block):
        with pytest.raises(ValueError):
            read_record(text)


def test_reject_duplicate_json_keys():
    for text in ('{"pilot_id":"A","pilot_id":"B"}', '{"cases":[{"input":7,"input":11}]}'):
        with pytest.raises(ValueError, match="duplicate JSON key"):
            read_record("```json\n" + text + "\n```")


def test_reject_malformed_json():
    with pytest.raises(ValueError):
        read_record("```json\n{invalid}\n```")
