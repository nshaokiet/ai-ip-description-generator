"""Deterministic validation for PDF and DOCX uploads."""

from __future__ import annotations

import re
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from xml.etree import ElementTree

from pypdf import PdfReader
from pypdf.errors import PdfReadError

from backend.app.core.config import Settings


PDF_MEDIA_TYPE = "application/pdf"
DOCX_MEDIA_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
OLE_COMPOUND_SIGNATURE = bytes.fromhex("D0CF11E0A1B11AE1")
PDF_SIGNATURE = b"%PDF-"
ZIP_SIGNATURES = (b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08")
SAFE_FILENAME_CHARACTER = re.compile(r"[^A-Za-z0-9._ -]+")
MAIN_DOCUMENT_CONTENT_TYPE = (
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"
)


class DocumentValidationError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.safe_message = message


@dataclass(frozen=True, slots=True)
class ValidationResult:
    media_type: str
    page_count: int | None


def sanitize_filename(filename: str | None) -> str:
    """Return display-only metadata; this value is never used as a server path."""

    candidate = (filename or "document").replace("\\", "/").split("/")[-1]
    candidate = "".join(ch for ch in candidate if ch.isprintable() and ch not in "\x00\r\n\t")
    candidate = SAFE_FILENAME_CHARACTER.sub("_", candidate).strip(" .")
    if not candidate or candidate in {".", ".."}:
        return "document"
    return candidate[:255]


class DocumentValidator:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def validate(self, path: Path, *, filename: str | None, declared_mime: str | None) -> ValidationResult:
        suffix = Path(filename or "").suffix.lower()
        header = self._read_header(path)
        if header.startswith(OLE_COMPOUND_SIGNATURE) and suffix in {".docx", ".docm"}:
            raise DocumentValidationError(
                "encrypted_document", "Encrypted or password-protected documents are not supported."
            )
        if suffix == ".docm":
            raise DocumentValidationError("macro_enabled_document", "Macro-enabled documents are not supported.")
        if suffix not in {".pdf", ".docx"}:
            raise DocumentValidationError("unsupported_extension", "Only PDF and DOCX files are supported.")
        if suffix == ".pdf":
            if declared_mime != PDF_MEDIA_TYPE or not header.startswith(PDF_SIGNATURE):
                raise DocumentValidationError(
                    "format_mismatch", "The filename, media type, and file signature do not match."
                )
            return self._validate_pdf(path)
        if declared_mime != DOCX_MEDIA_TYPE or not header.startswith(ZIP_SIGNATURES):
            raise DocumentValidationError(
                "format_mismatch", "The filename, media type, and file signature do not match."
            )
        return self._validate_docx(path)

    @staticmethod
    def _read_header(path: Path) -> bytes:
        with path.open("rb") as source:
            return source.read(8)

    def _validate_pdf(self, path: Path) -> ValidationResult:
        try:
            reader = PdfReader(path, strict=True)
            if reader.is_encrypted:
                raise DocumentValidationError(
                    "encrypted_document", "Encrypted or password-protected documents are not supported."
                )
            page_count = len(reader.pages)
            if page_count < 1:
                raise DocumentValidationError("corrupt_pdf", "The PDF contains no pages.")
            if page_count > self.settings.max_pdf_pages:
                raise DocumentValidationError(
                    "pdf_page_limit_exceeded",
                    "PDF files may contain at most %d pages." % self.settings.max_pdf_pages,
                )
            has_text = False
            for page in reader.pages:
                extracted = page.extract_text() or ""
                if extracted.strip():
                    has_text = True
            if not has_text:
                raise DocumentValidationError(
                    "pdf_text_layer_required",
                    "The PDF must contain extractable text; scanned-only PDFs are not supported.",
                )
            return ValidationResult(media_type=PDF_MEDIA_TYPE, page_count=page_count)
        except DocumentValidationError:
            raise
        except (PdfReadError, OSError, ValueError, TypeError, KeyError) as exc:
            raise DocumentValidationError("corrupt_pdf", "The PDF could not be parsed safely.") from exc

    def _validate_docx(self, path: Path) -> ValidationResult:
        try:
            if not zipfile.is_zipfile(path):
                raise DocumentValidationError("corrupt_docx", "The DOCX package is not a valid ZIP archive.")
            with zipfile.ZipFile(path) as package:
                infos = package.infolist()
                self._validate_zip_limits(infos)
                names = {info.filename for info in infos}
                required = {"[Content_Types].xml", "word/document.xml"}
                if not required.issubset(names):
                    raise DocumentValidationError(
                        "invalid_docx_package", "The DOCX package is missing required OOXML parts."
                    )
                if any(info.flag_bits & 0x1 for info in infos):
                    raise DocumentValidationError(
                        "encrypted_document", "Encrypted or password-protected documents are not supported."
                    )
                lowered = {name.lower() for name in names}
                if "word/vbaproject.bin" in lowered:
                    raise DocumentValidationError(
                        "macro_enabled_document", "Macro-enabled documents are not supported."
                    )
                if any(
                    name.startswith(("word/embeddings/", "word/activex/", "word/controls/"))
                    for name in lowered
                ):
                    raise DocumentValidationError(
                        "embedded_object_not_allowed", "Embedded or active objects are not supported."
                    )
                self._validate_content_types(package.read("[Content_Types].xml"))
                self._parse_xml(package.read("word/document.xml"))
                self._validate_relationships(package, names)
            return ValidationResult(media_type=DOCX_MEDIA_TYPE, page_count=None)
        except DocumentValidationError:
            raise
        except (zipfile.BadZipFile, OSError, ValueError, KeyError, ElementTree.ParseError) as exc:
            raise DocumentValidationError("corrupt_docx", "The DOCX package could not be parsed safely.") from exc

    def _validate_zip_limits(self, infos: list[zipfile.ZipInfo]) -> None:
        if len(infos) > self.settings.max_docx_entries:
            raise DocumentValidationError("unsafe_docx_package", "The DOCX package contains too many entries.")
        total_uncompressed = 0
        normalized_names: set[str] = set()
        for info in infos:
            name = info.filename
            normalized_name = name.replace("\\", "/")
            path = PurePosixPath(normalized_name)
            if path.is_absolute() or ".." in path.parts or ":" in name:
                raise DocumentValidationError(
                    "unsafe_docx_package", "The DOCX package contains an unsafe entry path."
                )
            canonical_name = path.as_posix().casefold()
            if canonical_name in normalized_names:
                raise DocumentValidationError(
                    "unsafe_docx_package",
                    "The DOCX package contains duplicate or ambiguous entry names.",
                )
            normalized_names.add(canonical_name)
            if info.file_size > self.settings.max_docx_entry_bytes:
                raise DocumentValidationError("unsafe_docx_package", "A DOCX package entry is too large.")
            total_uncompressed += info.file_size
            if total_uncompressed > self.settings.max_docx_uncompressed_bytes:
                raise DocumentValidationError(
                    "unsafe_docx_package", "The DOCX package expands beyond the safe limit."
                )
            if info.file_size and info.compress_size == 0:
                raise DocumentValidationError(
                    "unsafe_docx_package", "The DOCX package has an unsafe compression ratio."
                )
            if info.compress_size and info.file_size / info.compress_size > self.settings.max_docx_compression_ratio:
                raise DocumentValidationError(
                    "unsafe_docx_package", "The DOCX package has an unsafe compression ratio."
                )

    @staticmethod
    def _validate_content_types(payload: bytes) -> None:
        root = DocumentValidator._parse_xml(payload)
        all_content_types = {
            element.attrib.get("ContentType", "")
            for element in root
        }
        content_types = {
            element.attrib.get("ContentType", "")
            for element in root
            if element.attrib.get("PartName") == "/word/document.xml"
        }
        if any(
            "macroEnabled" in value or "vbaProject" in value or "oleObject" in value
            for value in all_content_types
        ):
            code = "macro_enabled_document" if any(
                "macroEnabled" in value or "vbaProject" in value for value in all_content_types
            ) else "embedded_object_not_allowed"
            message = (
                "Macro-enabled documents are not supported."
                if code == "macro_enabled_document"
                else "Embedded or active objects are not supported."
            )
            raise DocumentValidationError(code, message)
        if MAIN_DOCUMENT_CONTENT_TYPE not in content_types:
            raise DocumentValidationError(
                "invalid_docx_package", "The OOXML main document content type is invalid."
            )

    @staticmethod
    def _validate_relationships(package: zipfile.ZipFile, names: set[str]) -> None:
        for name in names:
            if not name.lower().endswith(".rels"):
                continue
            root = DocumentValidator._parse_xml(package.read(name))
            for relationship in root:
                if relationship.attrib.get("TargetMode", "").lower() == "external":
                    raise DocumentValidationError(
                        "external_relationship_not_allowed",
                        "External OOXML relationships are not supported.",
                    )

    @staticmethod
    def _parse_xml(payload: bytes) -> ElementTree.Element:
        upper = payload.upper()
        if b"<!DOCTYPE" in upper or b"<!ENTITY" in upper:
            raise DocumentValidationError(
                "unsafe_docx_package", "DTD and entity declarations are not supported in DOCX XML."
            )
        return ElementTree.fromstring(payload)
