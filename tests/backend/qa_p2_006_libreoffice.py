"""CI-only headless LibreOffice visual/semantic smoke test for synthetic P2-006.

Usage: python tests/backend/qa_p2_006_libreoffice.py EXISTING_QA_ROOT
Requires libreoffice-writer, licensed Crimson Text fonts, and pdftoppm.
This is a separate presentation-engine test, not a signed source validator.
"""
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from test_uspto_document_package_v1 import inputs, run
from backend.app.services.uspto_offline_renderer import (
    BANNER, CLAIMS_INCOMPLETE, FILES, render_uspto_document_package,
    _build_model,
)
from verify_p2_006_qa_environment import verify


def check(program: list[str]) -> None:
    result = subprocess.run(program, capture_output=True, text=True, timeout=120)
    if result.returncode:
        # Only tools' safe diagnostics; never dump the source paper/filing.
        raise RuntimeError(f"{program[0]} exited {result.returncode}: {result.stderr[:500]}")


def normalized_pdf(pdf: Path) -> tuple[list[str], str]:
    pages = [re.sub(r"\s+", " ", p.extract_text() or "") for p in PdfReader(str(pdf)).pages]
    return pages, " ".join(pages)


def synthetic_figure_layout(qa_root: Path) -> None:
    """Produce rights-cleared geometric QA artwork, outside all filing outputs."""
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    path = qa_root / "SYNTHETIC_DRAWING_LAYOUT_QA.pdf"
    page = canvas.Canvas(str(path), pagesize=letter, invariant=1)
    page.setFont("Helvetica-Bold", 11)
    page.drawCentredString(306, 755, "SYNTHETIC FIGURE LAYOUT QA — NO SOURCE DRAWING")
    page.setLineWidth(1)
    # Fixed-aspect synthetic geometry tests centering and available draw area.
    box_w, box_h = 360, 210
    origin_x, origin_y = (612 - box_w) / 2, (792 - box_h) / 2
    page.rect(origin_x, origin_y, box_w, box_h)
    page.line(origin_x + 35, origin_y + 70, origin_x + 170, origin_y + 145)
    page.line(origin_x + 170, origin_y + 145, origin_x + 325, origin_y + 70)
    page.drawCentredString(306, origin_y - 30, "FIG. 1 (SYNTHETIC QA ONLY)")
    page.showPage()
    page.save()
    assert len(PdfReader(str(path)).pages) == 1
    check([
        "pdftoppm", "-f", "1", "-l", "1", "-r", "200", "-singlefile",
        "-png", str(path), str(qa_root / "SYNTHETIC_DRAWING_LAYOUT_QA"),
    ])


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: qa_p2_006_libreoffice.py EXISTING_QA_ROOT")
    qa_root = Path(sys.argv[1]).resolve(strict=True)
    if not qa_root.is_dir():
        raise ValueError("QA directory required")

    # Enforce the source-controlled package and runtime pins in this process too.
    environment = verify()
    (qa_root / "qa-environment.json").write_text(json.dumps(environment, indent=2)+"\n")

    originals = inputs()
    package = run(originals)
    outputs = render_uspto_document_package(package, **originals, output_dir=qa_root)
    assert tuple(outputs) == FILES
    model = _build_model(package["filing_view"])
    expected_text = [model.title, model.abstract]
    expected_text.extend(part.text for section in model.sections for part in section.parts)
    evidence = {"environment": environment, "outputs": {}}

    for profile in ("B2_REFERENCE_PREVIEW", "USPTO_APPLICATION_DRAFT"):
        source_pdf = outputs[profile + ".pdf"]
        pages, text = normalized_pdf(source_pdf)
        assert all(re.sub(r"\s+", " ", fragment) in text for fragment in expected_text)
        for number in range(1, len(pages)+1):
            suffix = "cover" if number == 1 else f"p{number:02}"
            check([
                "pdftoppm", "-f", str(number), "-l", str(number),
                "-r", "300", "-singlefile", "-png", str(source_pdf),
                str(qa_root / f"{profile}-NATIVE-{suffix}"),
            ])
    synthetic_figure_layout(qa_root)

    for profile in ("B2_REFERENCE_PREVIEW", "USPTO_APPLICATION_DRAFT"):
        source = outputs[profile + ".docx"]
        # A private, per-run LibreOffice profile avoids shared state.
        office_profile = qa_root / (".lo-" + profile)
        command = [
            "soffice", "-env:UserInstallation=" + office_profile.as_uri(),
            "--headless", "--convert-to", "pdf", "--outdir", str(qa_root), str(source),
        ]
        check(command)
        converted = qa_root / (profile + ".pdf")
        if not converted.is_file():
            raise AssertionError("LibreOffice did not render the expected PDF")
        pages, text = normalized_pdf(converted)
        assert len(pages) >= 2
        assert BANNER in text
        assert CLAIMS_INCOMPLETE in text
        assert "What is claimed is:" not in text
        assert all(BANNER in page for page in pages)
        assert all(re.sub(r"\s+", " ", fragment) in text for fragment in expected_text)
        assert text.index("TITLE OF THE INVENTION") < text.index("BACKGROUND OF THE INVENTION")
        if profile == "USPTO_APPLICATION_DRAFT":
            claims_pages = [i for i, p in enumerate(pages) if CLAIMS_INCOMPLETE in p]
            abstract_pages = [i for i, p in enumerate(pages) if "ABSTRACT OF THE DISCLOSURE" in p]
            assert claims_pages and abstract_pages and claims_pages[0] < abstract_pages[0]
            assert "CLAIMS" in pages[claims_pages[0]]

        evidence["outputs"][profile] = {
            "native_pages": len(PdfReader(str(outputs[profile+".pdf"])).pages),
            "libreoffice_pages": len(pages), "all_filing_fragments_preserved": True,
            "missing_claims_marker": True, "claims_preamble_absent": True,
            "sha256": {name: hashlib.sha256(outputs[name].read_bytes()).hexdigest()
                       for name in (profile+".pdf",profile+".docx")},
            "converted_pdf_sha256": hashlib.sha256(converted.read_bytes()).hexdigest(),
        }
        for number in range(1, len(pages)+1):
            suffix = "cover" if number == 1 else f"p{number:02}"
            check([
                "pdftoppm", "-f", str(number), "-l", str(number), "-r", "300",
                "-singlefile", "-png", str(converted),
                str(qa_root / f"{profile}-LO-{suffix}"),
            ])
        print(f"LO_QA {profile}: {len(pages)} pages, editable DOCX converted, text markers verified")

    (qa_root / "synthetic-qa-evidence.json").write_text(json.dumps(evidence, indent=2)+"\n")


if __name__ == "__main__":
    main()
