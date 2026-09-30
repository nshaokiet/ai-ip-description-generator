from __future__ import annotations

import asyncio
import io
import logging
import os
import tempfile
import time
import unittest
import uuid
import warnings
import zipfile
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient
from pypdf import PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject

from backend.app.core.config import MEBIBYTE, Settings
from backend.app.main import create_app
from backend.app.services.document_storage import DocumentStorage
from backend.app.services.document_validation import DOCX_MEDIA_TYPE, PDF_MEDIA_TYPE


CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="{main_type}"/>
</Types>"""
DOCUMENT_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body><w:p><w:r><w:t>Synthetic document text</w:t></w:r></w:p></w:body>
</w:document>"""
INTERNAL_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="officeDocument" Target="word/document.xml"/>
</Relationships>"""
EXTERNAL_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId9" Type="hyperlink" Target="https://example.invalid" TargetMode="External"/>
</Relationships>"""
MAIN_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"
MACRO_TYPE = "application/vnd.ms-word.document.macroEnabled.main+xml"


def synthetic_pdf(*, pages: int = 1, text_page: int | None = 0, encrypted: bool = False) -> bytes:
    writer = PdfWriter()
    for index in range(pages):
        page = writer.add_blank_page(width=612, height=792)
        if text_page == index:
            font = DictionaryObject(
                {
                    NameObject("/Type"): NameObject("/Font"),
                    NameObject("/Subtype"): NameObject("/Type1"),
                    NameObject("/BaseFont"): NameObject("/Helvetica"),
                }
            )
            font_ref = writer._add_object(font)
            resources = DictionaryObject(
                {NameObject("/Font"): DictionaryObject({NameObject("/F1"): font_ref})}
            )
            stream = DecodedStreamObject()
            stream.set_data(b"BT /F1 12 Tf 72 720 Td (Synthetic PDF text) Tj ET")
            page[NameObject("/Resources")] = resources
            page[NameObject("/Contents")] = writer._add_object(stream)
    if encrypted:
        writer.encrypt("synthetic-password")
    output = io.BytesIO()
    writer.write(output)
    return output.getvalue()


def synthetic_docx(
    *,
    macro: bool = False,
    embedded: bool = False,
    external: bool = False,
    traversal: bool = False,
    compression_bomb: bool = False,
) -> bytes:
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as package:
        package.writestr(
            "[Content_Types].xml",
            CONTENT_TYPES.format(main_type=MACRO_TYPE if macro else MAIN_TYPE),
        )
        package.writestr(
            "word/document.xml",
            ("A" * (2 * MEBIBYTE)) if compression_bomb else DOCUMENT_XML,
        )
        package.writestr("_rels/.rels", INTERNAL_RELS)
        if macro:
            package.writestr("word/vbaProject.bin", b"synthetic macro marker")
        if embedded:
            package.writestr("word/embeddings/oleObject1.bin", b"synthetic object")
        if external:
            package.writestr("word/_rels/document.xml.rels", EXTERNAL_RELS)
        if traversal:
            package.writestr("../outside.xml", b"synthetic traversal marker")
    return output.getvalue()


class DocumentUploadTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.storage_root = Path(self.temporary_directory.name)
        self.settings = Settings(storage_root=self.storage_root)
        self.app = create_app(self.settings)
        self.client_context = TestClient(self.app)
        self.client = self.client_context.__enter__()

    def tearDown(self) -> None:
        self.client_context.__exit__(None, None, None)
        self.temporary_directory.cleanup()

    def upload(self, filename: str, payload: bytes, media_type: str):
        return self.client.post("/api/documents", files={"file": (filename, payload, media_type)})

    def assert_error(self, response, status: int, code: str) -> None:
        self.assertEqual(status, response.status_code, response.text)
        body = response.json()
        self.assertEqual(code, body["error"]["code"])
        self.assertRegex(body["error"]["correlation_id"], r"^[0-9a-f]{32}$")
        self.assertNotIn(str(self.storage_root), response.text)
        self.assertNotIn("Traceback", response.text)

    def assert_storage_empty(self) -> None:
        self.assertEqual([], list(self.storage_root.iterdir()))

    def test_valid_text_pdf_is_accepted_with_safe_metadata(self) -> None:
        payload = synthetic_pdf()
        response = self.upload("paper.pdf", payload, PDF_MEDIA_TYPE)
        self.assertEqual(201, response.status_code, response.text)
        body = response.json()
        self.assertEqual("paper.pdf", body["original_filename"])
        self.assertEqual(PDF_MEDIA_TYPE, body["media_type"])
        self.assertEqual(len(payload), body["size_bytes"])
        self.assertEqual(1, body["page_count"])
        self.assertEqual("validated", body["validation_status"])
        self.assertRegex(body["document_id"], r"^[a-f][0-9a-f]{31}$")
        self.assertTrue((self.storage_root / body["document_id"]).is_file())

    def test_allocate_id_rejects_digit_leading_uuid4_candidates(self) -> None:
        rejected = uuid.UUID(hex="1" * 32)
        accepted = uuid.UUID(hex="a" * 32)
        with patch(
            "backend.app.services.document_storage.uuid.uuid4",
            side_effect=[rejected, accepted],
        ) as uuid4:
            document_id = self.app.state.document_storage.allocate_id()
        self.assertEqual(accepted.hex, document_id)
        self.assertEqual(2, uuid4.call_count)

    def test_allocated_ids_are_schema_compatible_uuid4_hex_and_unique(self) -> None:
        document_ids = {
            self.app.state.document_storage.allocate_id()
            for _ in range(64)
        }
        self.assertEqual(64, len(document_ids))
        for document_id in document_ids:
            self.assertRegex(document_id, r"^[a-f][0-9a-f]{31}$")
            self.assertEqual(document_id, uuid.UUID(hex=document_id).hex)
            self.assertEqual(4, uuid.UUID(hex=document_id).version)

    def test_document_ids_are_unique_within_a_run(self) -> None:
        first = self.upload("one.pdf", synthetic_pdf(), PDF_MEDIA_TYPE)
        second = self.upload("two.pdf", synthetic_pdf(), PDF_MEDIA_TYPE)
        self.assertEqual(201, first.status_code, first.text)
        self.assertEqual(201, second.status_code, second.text)
        self.assertNotEqual(first.json()["document_id"], second.json()["document_id"])

    def test_mixed_pdf_with_blank_page_is_accepted(self) -> None:
        response = self.upload("mixed.pdf", synthetic_pdf(pages=2, text_page=1), PDF_MEDIA_TYPE)
        self.assertEqual(201, response.status_code, response.text)
        self.assertEqual(2, response.json()["page_count"])

    def test_valid_docx_is_accepted_without_page_count(self) -> None:
        payload = synthetic_docx()
        response = self.upload("paper.docx", payload, DOCX_MEDIA_TYPE)
        self.assertEqual(201, response.status_code, response.text)
        body = response.json()
        self.assertEqual(DOCX_MEDIA_TYPE, body["media_type"])
        self.assertNotIn("page_count", body)

    def test_zero_byte_is_rejected_and_deleted(self) -> None:
        response = self.upload("empty.pdf", b"", PDF_MEDIA_TYPE)
        self.assert_error(response, 400, "empty_file")
        self.assert_storage_empty()

    def test_missing_and_multiple_files_are_rejected(self) -> None:
        missing = self.client.post("/api/documents", data={"note": "synthetic"})
        self.assert_error(missing, 400, "single_file_required")
        multiple = self.client.post(
            "/api/documents",
            files=[
                ("file", ("one.pdf", synthetic_pdf(), PDF_MEDIA_TYPE)),
                ("file", ("two.pdf", synthetic_pdf(), PDF_MEDIA_TYPE)),
            ],
        )
        self.assert_error(multiple, 400, "single_file_required")
        self.assert_storage_empty()

    def test_file_over_exact_ten_mib_limit_is_rejected(self) -> None:
        response = self.upload("large.pdf", b"%PDF-" + b"A" * (10 * MEBIBYTE), PDF_MEDIA_TYPE)
        self.assert_error(response, 413, "file_too_large")
        self.assert_storage_empty()

    def test_storage_accepts_exact_upload_limit_without_off_by_one_rejection(self) -> None:
        class ExactLimitUpload:
            def __init__(self, size: int) -> None:
                self.remaining = size

            async def read(self, size: int) -> bytes:
                count = min(size, self.remaining)
                self.remaining -= count
                return b"A" * count

        storage = DocumentStorage(
            self.storage_root,
            ttl_seconds=60,
            max_upload_bytes=10 * MEBIBYTE,
            read_chunk_bytes=64 * 1024,
        )
        document_id = storage.allocate_id()
        path, size = asyncio.run(
            storage.stream_to_disk(ExactLimitUpload(10 * MEBIBYTE), document_id)
        )
        self.assertEqual(10 * MEBIBYTE, size)
        self.assertEqual(size, path.stat().st_size)
        self.assertTrue(storage.delete(document_id))
        self.assert_storage_empty()

    def test_pdf_over_fifty_pages_is_rejected(self) -> None:
        response = self.upload("long.pdf", synthetic_pdf(pages=51, text_page=None), PDF_MEDIA_TYPE)
        self.assert_error(response, 422, "pdf_page_limit_exceeded")
        self.assert_storage_empty()

    def test_pdf_at_exact_fifty_page_limit_is_accepted(self) -> None:
        response = self.upload(
            "boundary.pdf",
            synthetic_pdf(pages=50, text_page=49),
            PDF_MEDIA_TYPE,
        )
        self.assertEqual(201, response.status_code, response.text)
        self.assertEqual(50, response.json()["page_count"])

    def test_scanned_only_pdf_is_rejected(self) -> None:
        response = self.upload("scan.pdf", synthetic_pdf(text_page=None), PDF_MEDIA_TYPE)
        self.assert_error(response, 422, "pdf_text_layer_required")
        self.assert_storage_empty()

    def test_corrupt_and_encrypted_pdfs_are_rejected(self) -> None:
        corrupt = self.upload("broken.pdf", b"%PDF-not-a-document", PDF_MEDIA_TYPE)
        self.assert_error(corrupt, 422, "corrupt_pdf")
        encrypted = self.upload("locked.pdf", synthetic_pdf(encrypted=True), PDF_MEDIA_TYPE)
        self.assert_error(encrypted, 422, "encrypted_document")
        self.assert_storage_empty()

    def test_extension_mime_and_signature_mismatches_are_rejected(self) -> None:
        wrong_mime = self.upload("paper.pdf", synthetic_pdf(), DOCX_MEDIA_TYPE)
        self.assert_error(wrong_mime, 415, "format_mismatch")
        fake_pdf = self.upload("paper.pdf", synthetic_docx(), PDF_MEDIA_TYPE)
        self.assert_error(fake_pdf, 415, "format_mismatch")
        unsupported = self.upload("paper.txt", b"synthetic", "text/plain")
        self.assert_error(unsupported, 415, "unsupported_extension")
        self.assert_storage_empty()

    def test_disguised_double_extension_is_rejected_without_parsing(self) -> None:
        with patch("backend.app.services.document_validation.PdfReader") as reader:
            response = self.upload(
                "paper.pdf.exe",
                synthetic_pdf(),
                PDF_MEDIA_TYPE,
            )
        reader.assert_not_called()
        self.assert_error(response, 415, "unsupported_extension")
        self.assert_storage_empty()

    def test_macro_docm_and_renamed_macro_are_rejected(self) -> None:
        docm = self.upload("paper.docm", synthetic_docx(macro=True), DOCX_MEDIA_TYPE)
        self.assert_error(docm, 422, "macro_enabled_document")
        renamed = self.upload("paper.docx", synthetic_docx(macro=True), DOCX_MEDIA_TYPE)
        self.assert_error(renamed, 422, "macro_enabled_document")
        self.assert_storage_empty()

    def test_encrypted_docx_signature_is_rejected(self) -> None:
        payload = bytes.fromhex("D0CF11E0A1B11AE1") + b"synthetic encrypted OOXML"
        response = self.upload("locked.docx", payload, DOCX_MEDIA_TYPE)
        self.assert_error(response, 422, "encrypted_document")
        self.assert_storage_empty()

    def test_unsafe_docx_content_is_rejected(self) -> None:
        cases = [
            (synthetic_docx(embedded=True), "embedded_object_not_allowed"),
            (synthetic_docx(external=True), "external_relationship_not_allowed"),
            (synthetic_docx(traversal=True), "unsafe_docx_package"),
            (synthetic_docx(compression_bomb=True), "unsafe_docx_package"),
        ]
        for payload, expected_code in cases:
            with self.subTest(expected_code=expected_code):
                response = self.upload("unsafe.docx", payload, DOCX_MEDIA_TYPE)
                self.assert_error(response, 422, expected_code)
                self.assert_storage_empty()

    def test_duplicate_and_case_colliding_docx_members_are_rejected_before_parse(self) -> None:
        cases = [
            ("word/document.xml", b"<duplicate/>"),
            ("WORD/DOCUMENT.XML", b"<case-collision/>"),
            ("word//document.xml", b"<separator-collision/>"),
        ]
        for duplicate_name, duplicate_payload in cases:
            with self.subTest(duplicate_name=duplicate_name):
                payload = io.BytesIO()
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", UserWarning)
                    with zipfile.ZipFile(payload, "w", zipfile.ZIP_DEFLATED) as package:
                        package.writestr(
                            "[Content_Types].xml",
                            CONTENT_TYPES.format(main_type=MAIN_TYPE),
                        )
                        package.writestr("word/document.xml", DOCUMENT_XML)
                        package.writestr(duplicate_name, duplicate_payload)
                response = self.upload("ambiguous.docx", payload.getvalue(), DOCX_MEDIA_TYPE)
                self.assert_error(response, 422, "unsafe_docx_package")
                self.assert_storage_empty()

    def test_corrupt_docx_is_rejected(self) -> None:
        response = self.upload("broken.docx", b"PK\x03\x04not-a-zip", DOCX_MEDIA_TYPE)
        self.assert_error(response, 422, "corrupt_docx")
        self.assert_storage_empty()

    def test_docx_missing_parts_or_with_malformed_document_xml_is_rejected(self) -> None:
        missing = io.BytesIO()
        with zipfile.ZipFile(missing, "w", zipfile.ZIP_DEFLATED) as package:
            package.writestr("[Content_Types].xml", CONTENT_TYPES.format(main_type=MAIN_TYPE))
        response = self.upload("missing.docx", missing.getvalue(), DOCX_MEDIA_TYPE)
        self.assert_error(response, 422, "invalid_docx_package")

        malformed = io.BytesIO()
        with zipfile.ZipFile(malformed, "w", zipfile.ZIP_DEFLATED) as package:
            package.writestr("[Content_Types].xml", CONTENT_TYPES.format(main_type=MAIN_TYPE))
            package.writestr("word/document.xml", b"<not-closed")
        response = self.upload("malformed.docx", malformed.getvalue(), DOCX_MEDIA_TYPE)
        self.assert_error(response, 422, "corrupt_docx")

        entity = io.BytesIO()
        with zipfile.ZipFile(entity, "w", zipfile.ZIP_DEFLATED) as package:
            package.writestr("[Content_Types].xml", CONTENT_TYPES.format(main_type=MAIN_TYPE))
            package.writestr(
                "word/document.xml",
                b'<!DOCTYPE x [<!ENTITY data "unsafe">]><x>&data;</x>',
            )
        response = self.upload("entity.docx", entity.getvalue(), DOCX_MEDIA_TYPE)
        self.assert_error(response, 422, "unsafe_docx_package")
        self.assert_storage_empty()

    def test_path_traversal_filename_never_controls_storage_path(self) -> None:
        response = self.upload("../../private/paper.pdf", synthetic_pdf(), PDF_MEDIA_TYPE)
        self.assertEqual(201, response.status_code, response.text)
        body = response.json()
        self.assertEqual("paper.pdf", body["original_filename"])
        self.assertEqual([body["document_id"]], [path.name for path in self.storage_root.iterdir()])

    def test_platform_paths_and_unicode_filename_never_control_storage_path(self) -> None:
        cases = [
            (r"C:\private\paper.pdf", "paper.pdf"),
            (r"\\server\share/mixed\paper.pdf", "paper.pdf"),
            ("研究資料.pdf", "_.pdf"),
        ]
        for filename, expected_display_name in cases:
            with self.subTest(filename=filename):
                response = self.upload(filename, synthetic_pdf(), PDF_MEDIA_TYPE)
                self.assertEqual(201, response.status_code, response.text)
                body = response.json()
                self.assertEqual(expected_display_name, body["original_filename"])
                stored = self.storage_root / body["document_id"]
                self.assertTrue(stored.is_file())
                self.assertNotIn("paper.pdf", stored.name)
                self.assertTrue(self.app.state.document_storage.delete(body["document_id"]))

    def test_success_cleanup_ttl_and_active_lease_are_idempotent(self) -> None:
        response = self.upload("paper.pdf", synthetic_pdf(), PDF_MEDIA_TYPE)
        document_id = response.json()["document_id"]
        stored_path = self.storage_root / document_id
        expired_time = time.time() - self.settings.upload_ttl_seconds
        os.utime(stored_path, (expired_time, expired_time))
        with self.app.state.document_storage.lease(document_id):
            self.assertEqual([], self.app.state.document_storage.sweep_expired())
            self.assertTrue(stored_path.exists())
            self.assertFalse(self.app.state.document_storage.delete(document_id))
        self.assertEqual([document_id], self.app.state.document_storage.sweep_expired())
        self.assertFalse(stored_path.exists())
        self.assertTrue(self.app.state.document_storage.delete(document_id))

    def test_ttl_timestamp_begins_when_receipt_starts(self) -> None:
        class DelayedUpload:
            def __init__(self) -> None:
                self.calls = 0

            async def read(self, _: int) -> bytes:
                self.calls += 1
                if self.calls == 1:
                    return b"synthetic"
                await asyncio.sleep(0.03)
                return b""

        storage = DocumentStorage(
            self.storage_root,
            ttl_seconds=60,
            max_upload_bytes=1024,
            read_chunk_bytes=64,
        )
        document_id = storage.allocate_id()
        started = time.time()
        path, _ = asyncio.run(storage.stream_to_disk(DelayedUpload(), document_id))
        finished = time.time()
        self.assertGreaterEqual(path.stat().st_mtime, started)
        self.assertLess(path.stat().st_mtime, finished - 0.01)

    def test_success_file_can_be_deleted_immediately_after_downstream_completion(self) -> None:
        response = self.upload("paper.pdf", synthetic_pdf(), PDF_MEDIA_TYPE)
        document_id = response.json()["document_id"]
        self.assertTrue(self.app.state.document_storage.delete(document_id))
        self.assert_storage_empty()
        self.assertTrue(self.app.state.document_storage.delete(document_id))

    def test_startup_removes_expired_opaque_file(self) -> None:
        self.client_context.__exit__(None, None, None)
        stale_id = "a" * 32
        stale_path = self.storage_root / stale_id
        stale_path.write_bytes(b"synthetic")
        expired_time = time.time() - self.settings.upload_ttl_seconds
        os.utime(stale_path, (expired_time, expired_time))
        self.client_context = TestClient(create_app(self.settings))
        self.client = self.client_context.__enter__()
        self.assertFalse(stale_path.exists())

    def test_expiry_sweep_preserves_non_identifier_and_symlink_entries(self) -> None:
        expired_time = time.time() - self.settings.upload_ttl_seconds
        sentinel = self.storage_root / ("z" * 32)
        sentinel.write_bytes(b"unmanaged synthetic sentinel")
        os.utime(sentinel, (expired_time, expired_time))

        target = self.storage_root / "unmanaged-target"
        target.write_bytes(b"unmanaged synthetic target")
        symlink = self.storage_root / ("b" * 32)
        try:
            symlink.symlink_to(target)
        except (OSError, NotImplementedError):
            symlink = None

        stale_id = "a" * 32
        stale_path = self.storage_root / stale_id
        stale_path.write_bytes(b"managed synthetic stale upload")
        os.utime(stale_path, (expired_time, expired_time))

        self.assertEqual([stale_id], self.app.state.document_storage.sweep_expired())
        self.assertTrue(sentinel.exists())
        self.assertTrue(target.exists())
        if symlink is not None:
            self.assertTrue(symlink.is_symlink())

    def test_malformed_multipart_is_rejected_without_parser_detail_or_trace(self) -> None:
        marker = "DO_NOT_REFLECT_MULTIPART_SECRET"
        response = self.client.post(
            "/api/documents",
            content=(f"--broken\r\n{marker}").encode(),
            headers={"Content-Type": "multipart/form-data; boundary=broken"},
        )
        self.assert_error(response, 400, "single_file_required")
        self.assertNotIn(marker, response.text)

    def test_backend_responses_include_local_security_headers(self) -> None:
        for response in (
            self.client.get("/health"),
            self.upload("unsupported.txt", b"synthetic", "text/plain"),
        ):
            with self.subTest(status=response.status_code):
                self.assertEqual("no-store", response.headers["cache-control"])
                self.assertEqual("nosniff", response.headers["x-content-type-options"])
                self.assertEqual("no-referrer", response.headers["referrer-policy"])
                self.assertEqual("DENY", response.headers["x-frame-options"])
                self.assertEqual(
                    "camera=(), geolocation=(), microphone=()",
                    response.headers["permissions-policy"],
                )

    def test_logs_and_errors_do_not_disclose_content_filename_or_path(self) -> None:
        marker = "DO_NOT_LOG_SYNTHETIC_SECRET"
        with self.assertLogs("backend.app.main", level=logging.INFO) as captured:
            response = self.upload("../../%s.txt" % marker, marker.encode(), "text/plain")
        self.assert_error(response, 415, "unsupported_extension")
        combined = "\n".join(captured.output) + response.text
        self.assertNotIn(marker, combined)
        self.assertNotIn(str(self.storage_root), combined)

    @unittest.skipIf(os.name == "nt", "POSIX permission bits are not reliable on Windows")
    def test_stored_file_permissions_are_restrictive(self) -> None:
        response = self.upload("paper.pdf", synthetic_pdf(), PDF_MEDIA_TYPE)
        path = self.storage_root / response.json()["document_id"]
        self.assertEqual(0o600, path.stat().st_mode & 0o777)


if __name__ == "__main__":
    unittest.main()
