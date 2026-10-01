"""Deterministic synthetic-only samples and runtimes for demo/staging.

This module deliberately contains no provider client and performs no network calls.
The fixture outputs are offline oracles; they do not represent analysis of an
arbitrary uploaded paper and do not establish model quality or patentability.
"""

from __future__ import annotations

import copy
import hashlib
import hmac
import io
import json
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping
from xml.sax.saxutils import escape

from pypdf import PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject

from backend.app.api.routes.documents import APIError
from backend.app.services.draft_business_validation import validate_draft_business_rules
from backend.app.services.draft_runtime import DraftRuntimeMetadata, DraftRuntimeResult
from backend.app.services.extraction_runtime import (
    ExtractionRuntimeMetadata,
    ExtractionRuntimeResult,
)


DEMO_SAMPLE_HEADER = "X-AI-IP-Demo-Sample"
PDF_SAMPLE_ID = "synthetic-pdf-v1"
DOCX_SAMPLE_ID = "synthetic-docx-v1"
SYNTHETIC_SOURCE_TEXT = (
    "Synthetic optical sensor calibration and temperature coefficient for "
    "deterministic AI IP demo testing."
)

_ROOT = Path(__file__).resolve().parents[3]
_FIXTURE_ROOT = _ROOT / "tests" / "fixtures" / "patent-draft" / "v1.0.0" / "cases"
_REPRESENTATIVE = json.loads(
    (_FIXTURE_ROOT / "representative.json").read_text(encoding="utf-8")
)
_MISSING = json.loads(
    (_FIXTURE_ROOT / "missing-information.json").read_text(encoding="utf-8")
)

_CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>"""
_INTERNAL_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="officeDocument" Target="word/document.xml"/>
</Relationships>"""


def _pdf_literal(text: str) -> bytes:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)").encode("latin-1")


def synthetic_pdf(page_texts: list[str]) -> bytes:
    """Build a deterministic text-layer PDF for the controlled demo contract."""
    writer = PdfWriter()
    for text in page_texts:
        page = writer.add_blank_page(width=612, height=792)
        font = DictionaryObject(
            {
                NameObject("/Type"): NameObject("/Font"),
                NameObject("/Subtype"): NameObject("/Type1"),
                NameObject("/BaseFont"): NameObject("/Helvetica"),
            }
        )
        font_ref = writer._add_object(font)
        page[NameObject("/Resources")] = DictionaryObject(
            {NameObject("/Font"): DictionaryObject({NameObject("/F1"): font_ref})}
        )
        stream = DecodedStreamObject()
        stream.set_data(b"BT /F1 12 Tf 72 720 Td (" + _pdf_literal(text) + b") Tj ET")
        page[NameObject("/Contents")] = writer._add_object(stream)
    output = io.BytesIO()
    writer.write(output)
    return output.getvalue()


def paragraph_xml(text: str) -> str:
    return '<w:p><w:r><w:t xml:space="preserve">%s</w:t></w:r></w:p>' % escape(text)


def synthetic_docx(body_elements: list[str]) -> bytes:
    """Build a deterministic minimal DOCX for the controlled demo contract."""
    document_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        "<w:body>%s</w:body></w:document>" % "".join(body_elements)
    )
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as package:
        package.writestr("[Content_Types].xml", _CONTENT_TYPES)
        package.writestr("_rels/.rels", _INTERNAL_RELS)
        package.writestr("word/document.xml", document_xml)
    return output.getvalue()


@dataclass(frozen=True, slots=True)
class SyntheticDemoSample:
    sample_id: str
    filename: str
    media_type: str
    content: bytes
    sha256: str


def _sample(sample_id: str, filename: str, media_type: str, content: bytes) -> SyntheticDemoSample:
    return SyntheticDemoSample(
        sample_id=sample_id,
        filename=filename,
        media_type=media_type,
        content=content,
        sha256=hashlib.sha256(content).hexdigest(),
    )


DEMO_SAMPLES: Mapping[str, SyntheticDemoSample] = {
    PDF_SAMPLE_ID: _sample(
        PDF_SAMPLE_ID,
        "ai-ip-synthetic-demo.pdf",
        "application/pdf",
        synthetic_pdf([SYNTHETIC_SOURCE_TEXT]),
    ),
    DOCX_SAMPLE_ID: _sample(
        DOCX_SAMPLE_ID,
        "ai-ip-synthetic-demo.docx",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        synthetic_docx([paragraph_xml(SYNTHETIC_SOURCE_TEXT)]),
    ),
}


class SyntheticDemoUploadGuard:
    """Allow only the exact public samples issued by the demo backend."""

    header_name = DEMO_SAMPLE_HEADER

    def validate_request(self, headers) -> None:
        sample_id = headers.get(self.header_name)
        if sample_id not in DEMO_SAMPLES:
            raise APIError(
                403,
                "synthetic_demo_sample_required",
                "This staging service accepts only its controlled synthetic demo samples.",
            )

    def validate_document(
        self,
        *,
        sample_id: str | None,
        filename: str,
        media_type: str,
        sha256: str,
    ) -> None:
        sample = DEMO_SAMPLES.get(sample_id or "")
        if (
            sample is None
            or filename != sample.filename
            or media_type != sample.media_type
            or not hmac.compare_digest(sha256, sample.sha256)
        ):
            raise APIError(
                422,
                "invalid_synthetic_demo_sample",
                "The upload does not match a controlled synthetic demo sample.",
            )


class SyntheticDemoExtractionRuntime:
    """Return canonical deterministic analysis; never instantiate a provider client."""

    provider_call_count = 0

    def run_extraction(self, envelope, *, correlation_id=None):
        metadata = envelope.document_metadata.model_dump(exclude_none=True)
        fixture = _MISSING if metadata["file_name"] == "synthetic-missing.pdf" else _REPRESENTATIVE
        analysis = copy.deepcopy(fixture["input"]["source_analysis"])
        analysis["document_metadata"] = metadata
        for evidence in analysis["evidence"]:
            evidence["document_id"] = metadata["document_id"]
        return ExtractionRuntimeResult(
            analysis=analysis,
            runtime=ExtractionRuntimeMetadata(
                provider="synthetic_demo",
                model="deterministic_fixture_v1",
                request_id="synthetic-demo-extraction",
                status="completed",
                duration_ms=1,
                usage={},
            ),
        )


class SyntheticDemoDraftRuntime:
    """Return a canonical deterministic draft; never instantiate a provider client."""

    provider_call_count = 0

    def run_draft_generation(self, source_analysis, selected_title_candidate_id=None):
        missing_case = source_analysis["document_metadata"]["file_name"] == "synthetic-missing.pdf"
        fixture = _MISSING if missing_case else _REPRESENTATIVE
        draft = copy.deepcopy(fixture["expected_output"])
        draft["document_metadata"]["source_document"] = copy.deepcopy(
            source_analysis["document_metadata"]
        )
        for evidence in draft["evidence_appendix"]:
            evidence["document_id"] = source_analysis["document_metadata"]["document_id"]
        if selected_title_candidate_id is None and not missing_case:
            draft["selected_title"] = copy.deepcopy(_MISSING["expected_output"]["selected_title"])
            draft["missing_information"].append(
                copy.deepcopy(
                    next(
                        item
                        for item in _MISSING["expected_output"]["missing_information"]
                        if item["missing_id"] == "missing-title"
                    )
                )
            )
            for evidence in draft["evidence_appendix"]:
                evidence["usage_references"] = [
                    usage
                    for usage in evidence["usage_references"]
                    if usage["target_type"] != "SELECTED_TITLE"
                ]
        validate_draft_business_rules(
            draft,
            source_analysis,
            selected_title_candidate_id=selected_title_candidate_id,
        )
        return DraftRuntimeResult(
            draft=draft,
            runtime=DraftRuntimeMetadata(
                provider="synthetic_demo",
                model="deterministic_fixture_v1",
                request_id="synthetic-demo-draft",
                status="completed",
                duration_ms=1,
                usage={},
            ),
        )
