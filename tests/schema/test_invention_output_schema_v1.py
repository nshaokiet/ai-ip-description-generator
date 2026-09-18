import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPOSITORY_ROOT / "schemas/invention-output/v1.0.0/invention-output.schema.json"
FIXTURE_ROOT = REPOSITORY_ROOT / "tests/fixtures/invention-output/v1.0.0"


def load_json(path: Path):
    with path.open(encoding="utf-8") as source:
        return json.load(source)


class InventionOutputSchemaV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = load_json(SCHEMA_PATH)
        cls.validator = Draft202012Validator(cls.schema)
        cls.minimal = load_json(FIXTURE_ROOT / "valid/minimal.json")
        cls.representative = load_json(FIXTURE_ROOT / "valid/representative.json")

    def assert_valid(self, instance):
        errors = sorted(self.validator.iter_errors(instance), key=lambda error: list(error.absolute_path))
        self.assertEqual([], errors, "\n".join(error.message for error in errors))

    def errors_for(self, instance):
        return list(self.validator.iter_errors(instance))

    def test_schema_is_valid_draft_2020_12(self):
        Draft202012Validator.check_schema(self.schema)

    def test_minimal_fixture_is_valid(self):
        self.assert_valid(self.minimal)

    def test_representative_fixture_is_valid(self):
        self.assert_valid(self.representative)

    def test_missing_evidence_fixture_fails_at_exact_path(self):
        instance = load_json(FIXTURE_ROOT / "invalid/missing-evidence.json")
        errors = self.errors_for(instance)
        self.assertEqual(1, len(errors))
        self.assertEqual("minItems", errors[0].validator)
        self.assertEqual(
            ["technical_problems", 0, "grounding", "evidence_ids"],
            list(errors[0].absolute_path),
        )

    def test_unsupported_claims_fixture_fails_at_root(self):
        instance = load_json(FIXTURE_ROOT / "invalid/unsupported-claims-field.json")
        errors = self.errors_for(instance)
        self.assertEqual(1, len(errors))
        self.assertEqual("additionalProperties", errors[0].validator)
        self.assertEqual([], list(errors[0].absolute_path))
        self.assertIn("claims", errors[0].message)

    def test_missing_required_root_field_is_rejected(self):
        instance = copy.deepcopy(self.minimal)
        del instance["evidence"]
        errors = self.errors_for(instance)
        self.assertTrue(any(error.validator == "required" for error in errors))

    def test_wrong_schema_version_is_rejected(self):
        instance = copy.deepcopy(self.minimal)
        instance["schema_version"] = "2.0.0"
        errors = self.errors_for(instance)
        self.assertTrue(any(error.validator == "const" for error in errors))

    def test_unknown_nested_field_is_rejected(self):
        instance = copy.deepcopy(self.minimal)
        instance["output_notice"]["unknown"] = True
        errors = self.errors_for(instance)
        self.assertTrue(any(error.validator == "additionalProperties" for error in errors))

    def test_legacy_notice_field_names_are_rejected(self):
        instance = copy.deepcopy(self.minimal)
        instance["output_notice"]["legal_advice"] = instance["output_notice"].pop("is_legal_advice")
        instance["output_notice"]["patentability_assessment"] = instance["output_notice"].pop(
            "includes_patentability_assessment"
        )
        errors = self.errors_for(instance)
        self.assertTrue(any(error.validator == "required" for error in errors))
        self.assertTrue(any(error.validator == "additionalProperties" for error in errors))

    def test_legal_notice_flags_must_be_false(self):
        for field in ("is_legal_advice", "includes_patentability_assessment"):
            with self.subTest(field=field):
                instance = copy.deepcopy(self.minimal)
                instance["output_notice"][field] = True
                errors = self.errors_for(instance)
                self.assertTrue(any(error.validator == "const" for error in errors))

    def test_each_grounding_label_requires_evidence(self):
        for label in ("SOURCE_FACT", "PARAPHRASE", "INFERENCE"):
            with self.subTest(label=label):
                instance = copy.deepcopy(self.representative)
                grounding = instance["technical_problems"][0]["grounding"]
                grounding["label"] = label
                grounding["evidence_ids"] = []
                errors = self.errors_for(instance)
                self.assertTrue(any(error.validator == "minItems" for error in errors))

    def test_invalid_identifier_media_type_and_checksum_are_rejected(self):
        mutations = (
            ("document_id", "1-invalid"),
            ("media_type", "text/plain"),
            ("sha256", "ABC"),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                instance = copy.deepcopy(self.representative)
                instance["document_metadata"][field] = value
                self.assertTrue(self.errors_for(instance))

    def test_empty_evidence_locator_is_rejected(self):
        instance = copy.deepcopy(self.representative)
        instance["evidence"][0]["locator"] = {}
        errors = self.errors_for(instance)
        self.assertTrue(any(error.validator == "anyOf" for error in errors))

    def test_experiment_requires_at_least_one_result(self):
        instance = copy.deepcopy(self.representative)
        instance["experimental_data"][0]["results"] = []
        errors = self.errors_for(instance)
        self.assertTrue(any(error.validator == "minItems" for error in errors))

    def test_drawing_conditionals_are_enforced(self):
        source_figure = copy.deepcopy(self.representative)
        source_figure["drawing_requirements"][0]["source_evidence_ids"] = []
        self.assertTrue(any(error.validator == "minItems" for error in self.errors_for(source_figure)))

        proposed = copy.deepcopy(self.representative)
        proposed["drawing_requirements"][1]["human_confirmation_required"] = False
        self.assertTrue(any(error.validator == "const" for error in self.errors_for(proposed)))


if __name__ == "__main__":
    unittest.main()
