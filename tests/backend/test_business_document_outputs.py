"""P0-OUTPUT reuses canonical renderer: three document types, six artifacts."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
from zipfile import ZipFile

from docx import Document
from pypdf import PdfReader
import pytest

from backend.app.services import business_document_outputs as renderer
from backend.app.services.uspto_document_package_validation import USPTODocumentPackageValidationError
from tests.backend.test_uspto_document_package_v1 import inputs, run
from tests.backend.test_uspto_offline_renderer import _docx_text, _pdf_text
from tests.e2e.provider_tripwire import ProviderTripwire


@pytest.fixture(autouse=True)
def no_egress():
    with ProviderTripwire() as guard:
        yield guard
        guard.assert_no_unexpected_activity()
        assert all(value == 0 for value in guard.snapshot().values())


def render(tmp_path, language="en"):
    original = inputs();package = run(original)
    files = renderer.render_business_document_set(package, **original,
        output_dir=tmp_path, template_language=language)
    return original, package, files


@pytest.mark.parametrize("language", ["en", "vi"])
def test_canonical_package_to_three_document_types_docx_pdf_and_provenance(tmp_path, language):
    original, package, files = render(tmp_path, language)
    assert tuple(files) == renderer.BUSINESS_FILES + (renderer.BUSINESS_MANIFEST,)
    manifest = json.loads(files[renderer.BUSINESS_MANIFEST].read_text(encoding="utf-8"))
    assert manifest["source_identity"] == package["source_identity"]
    assert manifest["input_digests"] == package["input_digests"]
    assert manifest["status"] == "DRAFT" and manifest["review_status"] == "UNREVIEWED"
    assert not manifest["filing_ready"] and not manifest["claims_product_runtime_enabled"]
    assert manifest["translation_status"] == "SOURCE_TECHNICAL_TEXT_UNCHANGED_NOT_VALIDATED"
    assert manifest["prior_art"] == "NOT_PROVIDED" and manifest["figure_fidelity"] == "REVIEW_REQUIRED"
    for name in renderer.BUSINESS_FILES:
        path = files[name]
        assert manifest["outputs"][name] == hashlib.sha256(path.read_bytes()).hexdigest()
        text = _pdf_text(path) if path.suffix == ".pdf" else _docx_text(path)
        assert "DRAFT" in text and "HUMAN REVIEW REQUIRED" in text
        assert "Synthetic Optical Controller Calibration" in text
        if path.suffix == ".pdf":
            assert all("DRAFT" in (page.extract_text() or "") for page in PdfReader(str(path)).pages)
        else:
            document = Document(path)
            assert any(p.style.name == "Title" for p in document.paragraphs)
            assert not document.styles["Title"].element.xpath(".//w:pBdr")
            assert not document.paragraphs[0]._p.xpath(".//w:pBdr")
            with ZipFile(path) as archive:
                assert not any("vbaProject" in entry or "embeddings/" in entry for entry in archive.namelist())
                for entry in archive.namelist():
                    if entry.endswith(".rels"):
                        assert b'TargetMode="External"' not in archive.read(entry)
    patent = _docx_text(files["PATENT_DRAFT.docx"])
    annotated = _docx_text(files["ANNOTATED_DRAFT.docx"])
    report = _docx_text(files["ANALYSIS_REPORT.docx"])
    assert "EV-P0001-C001" not in patent and "MI-P2-003" not in patent
    assert "EV-P0001-C001 (page=1, chunk_id=P0001-C001)" in annotated
    assert package["source_identity"]["source_sha256"] in annotated
    assert package["source_identity"]["file_name"] in annotated
    paragraphs = [p.text for p in Document(files["ANNOTATED_DRAFT.docx"]).paragraphs]
    position = paragraphs.index("Synthetic Optical Controller Calibration")
    assert "EV-P0001-C001" in paragraphs[position+1]
    assert "MI-P2-003" in annotated and "REVIEW_REQUIRED" in annotated
    assert renderer.CLAIMS_INCOMPLETE in patent and renderer.CLAIMS_INCOMPLETE in annotated
    assert "12 percent" in report and "25 degC" in report
    assert original["structured_analysis"]["technical_problems"][0]["statement"] in report
    assert "controller model is not specified" in report
    assert "NOT_PROVIDED" in manifest["prior_art"]
    for kind in ["ANNOTATED_DRAFT", "ANALYSIS_REPORT"]:
        pdf = _pdf_text(files[kind+".pdf"])
        assert "REVIEW_REQUIRED" in pdf
        assert re.sub(r"\s+", " ", renderer.BUSINESS_LABELS[language][kind]) in pdf


@pytest.mark.parametrize("mutation", ["package", "source", "claims", "config"])
def test_invalid_canonical_inputs_fail_before_any_output(tmp_path, mutation):
    original = inputs();package = run(original)
    if mutation == "package":package["package_id"] = "p2-005-" + "0" * 24
    elif mutation == "source":original["structured_analysis"]["unapproved_key"] = "mutation"
    elif mutation == "claims":package["filing_view"]["claims"]["claims"] = [{"claim_text": "fabricated"}]
    else:original["p2_004_generation_config"]["max_dependent_claims_per_family"] = 99
    with pytest.raises(USPTODocumentPackageValidationError):
        renderer.render_business_document_set(package, **original, output_dir=tmp_path)
    assert list(tmp_path.iterdir()) == []


def test_missing_original_and_unsupported_language_cannot_create_files(tmp_path):
    original = inputs();package = run(original);arguments = deepcopy(original);arguments.pop("source_envelope")
    with pytest.raises(TypeError):renderer.render_business_document_set(package, **arguments, output_dir=tmp_path)
    with pytest.raises(ValueError, match="Unsupported template language"):
        renderer.render_business_document_set(package, **original, output_dir=tmp_path, template_language="unknown")
    assert list(tmp_path.iterdir()) == []


def test_existing_destination_is_not_overwritten(tmp_path):
    original, package, files = render(tmp_path)
    before = {name: path.read_bytes() for name, path in files.items()}
    with pytest.raises(FileExistsError):
        renderer.render_business_document_set(package, **original, output_dir=tmp_path)
    assert all(path.read_bytes() == before[name] for name, path in files.items())


def test_renderer_failure_does_not_publish_partial_set(tmp_path, monkeypatch):
    original = inputs();package = run(original)
    def fail(*args, **kwargs):raise RuntimeError("synthetic renderer failure")
    monkeypatch.setattr(renderer, "_docx", fail)
    with pytest.raises(RuntimeError, match="synthetic renderer failure"):
        renderer.render_business_document_set(package, **original, output_dir=tmp_path)
    assert list(tmp_path.iterdir()) == []


def test_input_objects_are_not_modified(tmp_path):
    original = inputs();package = run(original);before = deepcopy((original, package))
    renderer.render_business_document_set(package, **original, output_dir=tmp_path)
    assert (original, package) == before


def test_pdf_qa_decodes_ligatures_without_erasing_scientific_content():
    from tests.backend.qa_p2_006_libreoffice import semantic_pdf_text
    assert semantic_pdf_text("oﬀ conﬁrmation ﬂow coeﬃcient") == "off confirmation flow coefficient"
    assert semantic_pdf_text("12 percent") != semantic_pdf_text("21 percent")
    assert semantic_pdf_text("not supported") != semantic_pdf_text("supported")
    assert semantic_pdf_text("µm") != semantic_pdf_text("μm")
    assert semantic_pdf_text("SOURCE_FACT") != semantic_pdf_text("MISSING")
