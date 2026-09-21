import copy
import hashlib
import importlib.util
import json
import re
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from jsonschema import Draft202012Validator, ValidationError


ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "templates/patent-docx/v1.0.0/patent-description-template.docx"
MANIFEST = ROOT / "templates/patent-docx/v1.0.0/template-manifest.json"
SCHEMA = ROOT / "schemas/patent-draft/v1.0.0/patent-draft.schema.json"
FIXTURE_ROOT = ROOT / "tests/fixtures/patent-docx/v1.0.0"
RENDERER = ROOT / "tests/docx/render_patent_docx_v1.py"
AI003_CONFLICT = ROOT / "tests/fixtures/patent-draft/v1.0.0/cases/conflicting-evidence.json"
EXPECTED_FIXTURES = {
    "representative-context.json",
    "missing-information-context.json",
    "special-characters-context.json",
}
SECTION_HEADINGS = [
    "Cover and Draft Notice",
    "Title",
    "Abstract",
    "Technical Field",
    "Background",
    "Summary of Technical Disclosure",
    "Brief Description of Drawings",
    "Detailed Description",
    "Experimental Examples and Results",
    "Missing Information and Author Questions",
    "Evidence and Reference Appendix",
]


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_renderer():
    spec = importlib.util.spec_from_file_location("render_patent_docx_v1", RENDERER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def all_text(document):
    values = [paragraph.text for paragraph in document.paragraphs]
    for section in document.sections:
        values.extend(paragraph.text for paragraph in section.header.paragraphs)
        values.extend(paragraph.text for paragraph in section.footer.paragraphs)
    return "\n".join(values)


def package_text(path):
    with zipfile.ZipFile(path) as archive:
        return "\n".join(
            archive.read(name).decode("utf-8", errors="replace")
            for name in archive.namelist()
            if name.endswith((".xml", ".rels"))
        )


class PatentDocxTemplateV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.renderer = load_renderer()
        cls.schema = load_json(SCHEMA)
        cls.validator = Draft202012Validator(cls.schema)
        cls.manifest = load_json(MANIFEST)
        cls.fixtures = {path.name: load_json(path) for path in FIXTURE_ROOT.glob("*.json")}
        cls.temp = tempfile.TemporaryDirectory()
        cls.output_dir = cls.renderer.OUTPUT_ROOT / "automated-tests"
        cls.output_dir.mkdir(parents=True, exist_ok=True)
        cls.outputs = {}
        for name, payload in cls.fixtures.items():
            output = cls.output_dir / f"{Path(name).stem}.docx"
            cls.renderer.render_patent_docx(FIXTURE_ROOT / name, output)
            cls.outputs[name] = output

    @classmethod
    def tearDownClass(cls):
        for output in cls.outputs.values():
            output.unlink(missing_ok=True)
        cls.output_dir.rmdir()
        cls.temp.cleanup()

    def test_template_and_supporting_files_exist(self):
        for path in (TEMPLATE, MANIFEST, RENDERER):
            self.assertTrue(path.is_file(), path)

    def test_manifest_identity_paths_and_compatibility(self):
        self.assertEqual("patent-description-template-v1", self.manifest["template_id"])
        self.assertEqual("1.0.0", self.manifest["template_version"])
        self.assertEqual("1.0.0", self.manifest["compatible_patent_draft_contract_version"])
        self.assertEqual(TEMPLATE.relative_to(ROOT).as_posix(), self.manifest["canonical_template_path"])
        self.assertEqual(RENDERER.relative_to(ROOT).as_posix(), self.manifest["renderer_path"])
        self.assertEqual("en", self.manifest["language"])
        self.assertTrue(self.manifest["claims_excluded"])
        self.assertTrue(self.manifest["human_review_required"])

    def test_exact_fixture_inventory_and_schema_validity(self):
        self.assertEqual(EXPECTED_FIXTURES, set(self.fixtures))
        for name, payload in self.fixtures.items():
            with self.subTest(name=name):
                self.assertEqual([], list(self.validator.iter_errors(payload)))

    def test_fixtures_are_synthetic_and_have_no_secret_or_pii(self):
        forbidden = re.compile(r"(?:sk-[A-Za-z0-9]{12,}|api[_-]?key|password|token|@(?:gmail|outlook)\.)", re.I)
        for name, payload in self.fixtures.items():
            serialized = json.dumps(payload, ensure_ascii=False)
            with self.subTest(name=name):
                self.assertIn("synthetic", serialized.lower())
                self.assertIsNone(forbidden.search(serialized))

    def test_template_is_valid_docx_zip_package(self):
        self.assertTrue(zipfile.is_zipfile(TEMPLATE))
        with zipfile.ZipFile(TEMPLATE) as archive:
            self.assertIsNone(archive.testzip())
            self.assertIn("word/document.xml", archive.namelist())

    def test_template_has_no_macro_or_embedded_active_content(self):
        with zipfile.ZipFile(TEMPLATE) as archive:
            lower_names = [name.lower() for name in archive.namelist()]
            self.assertFalse(any("vbaproject" in name or "activex" in name or "/embeddings/" in name for name in lower_names))
            content_types = archive.read("[Content_Types].xml").decode("utf-8")
            self.assertNotIn("macroEnabled", content_types)

    def test_template_has_no_remote_image_or_external_relationship(self):
        with zipfile.ZipFile(TEMPLATE) as archive:
            for name in archive.namelist():
                if not name.endswith(".rels"):
                    continue
                relationships = archive.read(name).decode("utf-8")
                with self.subTest(name=name):
                    self.assertNotIn('TargetMode="External"', relationships)

    def test_renderer_rejects_schema_invalid_input_without_output(self):
        invalid = copy.deepcopy(self.fixtures["representative-context.json"])
        invalid["claims"] = []
        temp_root = Path(self.temp.name)
        invalid_path = temp_root / "invalid.json"
        invalid_path.write_text(json.dumps(invalid), encoding="utf-8")
        output = self.renderer.OUTPUT_ROOT / "automated-tests-invalid.docx"
        output.unlink(missing_ok=True)
        with self.assertRaises(ValidationError):
            self.renderer.render_patent_docx(invalid_path, output)
        self.assertFalse(output.exists())

    def test_renderer_refuses_output_outside_approved_generated_root(self):
        outside = Path(self.temp.name) / "outside.docx"
        with self.assertRaisesRegex(ValueError, "must be under"):
            self.renderer.render_patent_docx(FIXTURE_ROOT / "representative-context.json", outside)

    def test_renderer_refuses_to_overwrite_input_or_template(self):
        with self.assertRaisesRegex(ValueError, "must not overwrite"):
            self.renderer.render_patent_docx(FIXTURE_ROOT / "representative-context.json", TEMPLATE, TEMPLATE)

    def test_all_three_contexts_render_and_open(self):
        for name, output in self.outputs.items():
            with self.subTest(name=name):
                self.assertTrue(zipfile.is_zipfile(output))
                self.assertTrue(Document(output).paragraphs)

    def test_page_size_and_margins_are_exact(self):
        document = Document(TEMPLATE)
        section = document.sections[0]
        self.assertAlmostEqual(210, section.page_width.mm, places=1)
        self.assertAlmostEqual(297, section.page_height.mm, places=1)
        for margin in (section.top_margin, section.right_margin, section.bottom_margin, section.left_margin):
            self.assertAlmostEqual(25.4, margin.mm, places=1)

    def test_approved_styles_are_exact(self):
        styles = Document(TEMPLATE).styles
        expected = {
            "Normal": ("Times New Roman", 12, False),
            "Title": ("Times New Roman", 16, True),
            "Heading 1": ("Times New Roman", 14, True),
            "Heading 2": ("Times New Roman", 12, True),
        }
        for name, (font, size, bold) in expected.items():
            with self.subTest(style=name):
                self.assertEqual(font, styles[name].font.name)
                self.assertEqual(size, styles[name].font.size.pt)
                self.assertEqual(bold, styles[name].font.bold)
        self.assertEqual(WD_ALIGN_PARAGRAPH.CENTER, styles["Title"].paragraph_format.alignment)

    def test_body_spacing_is_exact(self):
        normal = Document(TEMPLATE).styles["Normal"].paragraph_format
        self.assertAlmostEqual(1.15, normal.line_spacing, places=2)
        self.assertAlmostEqual(6, normal.space_after.pt, places=1)

    def test_header_footer_and_page_fields_are_exact(self):
        document = Document(TEMPLATE)
        section = document.sections[0]
        self.assertIn("AI-Generated Patent Description Draft", "\n".join(p.text for p in section.header.paragraphs))
        self.assertIn("AI-generated draft — requires human review.", "\n".join(p.text for p in section.footer.paragraphs))
        xml = package_text(TEMPLATE)
        self.assertRegex(xml, r">\s*PAGE\s*<")
        self.assertRegex(xml, r">\s*NUMPAGES\s*<")

    def test_representative_heading_order_is_exact(self):
        document = Document(self.outputs["representative-context.json"])
        headings = [p.text for p in document.paragraphs if p.style.name == "Heading 1"]
        self.assertEqual(SECTION_HEADINGS, headings)
        heading_twos = [p.text for p in document.paragraphs if p.style.name == "Heading 2"]
        self.assertEqual(
            ["Technical Problems", "Technical Solutions", "Potential Distinguishing Features", "Technical Effects", "Components or System", "Process or Method Steps", "Embodiments", "Evidence ev-core", "Evidence ev-result", "Evidence ev-figure"],
            heading_twos,
        )

    def test_title_style_is_approved(self):
        document = Document(self.outputs["representative-context.json"])
        title = next(p for p in document.paragraphs if p.style.name == "Title")
        self.assertEqual("Temperature-Aware Calibration of an Optical Sensor", title.text)
        self.assertEqual(WD_ALIGN_PARAGRAPH.CENTER, title.alignment)

    def test_abstract_is_not_over_150_words(self):
        payload = self.fixtures["representative-context.json"]
        words = re.findall(r"\b\w+(?:[-'’]\w+)*\b", payload["abstract"]["text"], flags=re.UNICODE)
        self.assertEqual(payload["abstract"]["word_count"], len(words))
        self.assertLessEqual(len(words), 150)

    def test_missing_sections_keep_headings_and_exact_marker(self):
        text = all_text(Document(self.outputs["missing-information-context.json"]))
        for heading in SECTION_HEADINGS:
            self.assertIn(heading, text)
        self.assertGreaterEqual(text.count("[AUTHOR CONFIRMATION REQUIRED]"), 10)

    def test_inference_label_and_evidence_traceability_are_visible(self):
        text = all_text(Document(self.outputs["representative-context.json"]))
        self.assertIn("Grounding: INFERENCE | Evidence: ev-core", text)
        self.assertIn("Source paths: /potential_distinguishing_features/0", text)
        for evidence_id in ("ev-core", "ev-result", "ev-figure"):
            self.assertIn(f"Evidence {evidence_id}", text)

    def test_drawing_state_is_descriptive_and_no_figure_is_generated(self):
        representative = all_text(Document(self.outputs["representative-context.json"]))
        missing = all_text(Document(self.outputs["missing-information-context.json"]))
        self.assertIn("Source drawing available (not embedded)", representative)
        self.assertIn("Proposed drawing — not supplied", missing)
        with zipfile.ZipFile(self.outputs["representative-context.json"]) as archive:
            self.assertFalse(any(name.startswith("word/media/") for name in archive.namelist()))

    def test_author_questions_and_evidence_appendix_render(self):
        missing = all_text(Document(self.outputs["missing-information-context.json"]))
        representative = all_text(Document(self.outputs["representative-context.json"]))
        self.assertIn("Which existing title candidate should be selected?", missing)
        self.assertIn("Evidence and Reference Appendix", representative)
        self.assertIn("PARAGRAPH:docx-paragraph-feature", representative)

    def test_conflict_remains_unresolved(self):
        payload = load_json(AI003_CONFLICT)["expected_output"]
        temp_input = Path(self.temp.name) / "conflict.json"
        temp_input.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        output = self.renderer.OUTPUT_ROOT / "automated-tests-conflict.docx"
        try:
            self.renderer.render_patent_docx(temp_input, output)
            text = all_text(Document(output))
            self.assertIn("UNRESOLVED", text)
            self.assertIn("ev-conflict-a, ev-conflict-b", text)
            self.assertIn("Which operating temperature is intended?", text)
        finally:
            output.unlink(missing_ok=True)

    def test_claims_and_legal_conclusions_are_absent(self):
        output = self.outputs["representative-context.json"]
        text = all_text(Document(output))
        self.assertIsNone(re.search(r"\b(?:draft\s+)?claims?\b", package_text(output), re.I))
        for prohibited in ("is patentable", "is novel", "has an inventive step", "ready for filing"):
            self.assertNotIn(prohibited, text.lower())

    def test_rendered_packages_have_no_unresolved_template_markers(self):
        for name, output in self.outputs.items():
            xml = package_text(output)
            with self.subTest(name=name):
                for template_marker in (
                    "{%p", "{{ output_notice", "{{ document_metadata", "{{ paragraph.",
                    "{{ evidence.", "{{ item.", "{{ conflict.", "{{ question.",
                ):
                    self.assertNotIn(template_marker, xml)

    def test_special_characters_and_jinja_like_input_are_literal_data(self):
        text = all_text(Document(self.outputs["special-characters-context.json"]))
        self.assertIn("<sensor & controller>", text)
        self.assertIn("{{ do_not_execute }}", text)
        self.assertIn("{% raw_instruction %}", text)
        self.assertIn("{# literal_comment #}", text)
        self.assertIn("{{ braces }}", text)
        with zipfile.ZipFile(self.outputs["special-characters-context.json"]) as archive:
            self.assertIsNone(archive.testzip())

    def test_generated_representative_output_is_not_git_tracked(self):
        target = ROOT / "generated/patent-docx/v1.0.0/representative-patent-draft.docx"
        result = subprocess.run(
            ["git", "ls-files", "--error-unmatch", str(target.relative_to(ROOT))],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(0, result.returncode)

    def test_ai_technical_artefacts_are_not_modified(self):
        protected_roots = (
            ROOT / "schemas/invention-output",
            ROOT / "schemas/patent-draft",
            ROOT / "prompts/extraction",
            ROOT / "prompts/draft-generation",
            ROOT / "tests/schema",
            ROOT / "tests/prompt",
            ROOT / "tests/draft",
            ROOT / "tests/fixtures/invention-output",
            ROOT / "tests/fixtures/extraction-prompt",
            ROOT / "tests/fixtures/patent-draft",
        )

        def snapshot():
            return {
                path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                for root in protected_roots
                for path in root.rglob("*")
                if path.is_file()
            }

        before = snapshot()
        output = self.output_dir / "technical-artefact-mutation-check.docx"
        try:
            self.renderer.render_patent_docx(
                FIXTURE_ROOT / "representative-context.json",
                output,
            )
            self.assertEqual(before, snapshot())
        finally:
            output.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
