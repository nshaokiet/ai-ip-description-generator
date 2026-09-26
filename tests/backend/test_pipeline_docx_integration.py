from __future__ import annotations

import os
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from docx import Document
from fastapi.testclient import TestClient

from backend.app.core.config import Settings
from backend.app.main import create_app
from backend.app.services.core_pipeline import CorePipelineOrchestrator
from backend.app.services.document_validation import DOCX_MEDIA_TYPE, PDF_MEDIA_TYPE
from backend.app.services.patent_docx_renderer import PatentDocxRenderer
from backend.app.services.pipeline_docx import CorePipelineDocxService
from tests.backend.test_core_pipeline_e2e_offline import (
    ValidatingFakeDraftRuntime,
    ValidatingFakeExtractionRuntime,
)
from tests.backend.test_document_parsing import (
    paragraph_xml,
    synthetic_docx,
    synthetic_pdf,
)


EXPECTED_HEADINGS = [
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


class PipelineDocxIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.storage_root = self.root / "uploads"
        self.output_root = self.root / "generated"
        self.app = create_app(Settings(storage_root=self.storage_root))
        self.client_context = TestClient(self.app)
        self.client = self.client_context.__enter__()

    def tearDown(self) -> None:
        self.client_context.__exit__(None, None, None)
        self.temporary_directory.cleanup()

    def _upload(self, filename: str, payload: bytes, media_type: str) -> str:
        response = self.client.post(
            "/api/documents",
            files={"file": (filename, payload, media_type)},
        )
        self.assertEqual(201, response.status_code, response.text)
        return response.json()["document_id"]

    def _service(
        self,
    ) -> tuple[
        CorePipelineDocxService,
        ValidatingFakeExtractionRuntime,
        ValidatingFakeDraftRuntime,
    ]:
        extraction = ValidatingFakeExtractionRuntime()
        draft = ValidatingFakeDraftRuntime()
        pipeline = CorePipelineOrchestrator(
            self.app.state.document_storage,
            self.app.state.document_preparation_service,
            extraction,
            draft,
        )
        service = CorePipelineDocxService(
            pipeline,
            PatentDocxRenderer(output_root=self.output_root),
        )
        return service, extraction, draft

    def _assert_pipeline_to_docx(
        self,
        filename: str,
        payload: bytes,
        media_type: str,
    ) -> None:
        document_id = self._upload(filename, payload, media_type)
        source_path = self.app.state.document_storage.path_for(document_id)
        output_path = self.output_root / f"{document_id}.docx"
        service, extraction, draft = self._service()

        with (
            patch.dict(os.environ, {"OPENAI_API_KEY": ""}),
            patch("socket.create_connection") as connect,
            patch("urllib.request.urlopen") as urlopen,
        ):
            result = service.generate(
                document_id,
                output_path,
                correlation_id="offline-p0-003",
            )

        connect.assert_not_called()
        urlopen.assert_not_called()
        self.assertEqual(output_path.resolve(), result.output_path)
        self.assertTrue(zipfile.is_zipfile(result.output_path))
        with zipfile.ZipFile(result.output_path) as package:
            self.assertIsNone(package.testzip())
        headings = [
            paragraph.text
            for paragraph in Document(result.output_path).paragraphs
            if paragraph.style.name == "Heading 1"
        ]
        self.assertEqual(EXPECTED_HEADINGS, headings)
        self.assertEqual("PATENT_DESCRIPTION_DRAFT", result.pipeline.draft["output_type"])
        self.assertEqual(1, len(extraction.invocations))
        self.assertEqual(1, len(draft.invocations))
        self.assertIs(result.pipeline.analysis, draft.invocations[0][0])
        self.assertTrue(result.pipeline.metadata.source_cleanup_performed)
        self.assertFalse(source_path.exists())
        self.assertIsNone(self.app.state.document_registry.get(document_id))

    def test_synthetic_pdf_pipeline_renders_editable_docx_offline(self) -> None:
        self._assert_pipeline_to_docx(
            "synthetic-p0-003.pdf",
            synthetic_pdf(["Synthetic optical sensor source for DOCX integration."]),
            PDF_MEDIA_TYPE,
        )

    def test_synthetic_docx_pipeline_renders_editable_docx_offline(self) -> None:
        self._assert_pipeline_to_docx(
            "synthetic-p0-003.docx",
            synthetic_docx(
                [paragraph_xml("Synthetic DOCX source for DOCX integration.")]
            ),
            DOCX_MEDIA_TYPE,
        )


if __name__ == "__main__":
    unittest.main()
