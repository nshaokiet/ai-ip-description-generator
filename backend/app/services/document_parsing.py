"""Deterministic PDF/DOCX preparation for the AI-002 input contract."""

from __future__ import annotations

import hashlib
import zipfile
from collections.abc import Iterator
from pathlib import Path
from xml.etree import ElementTree

from pypdf import PdfReader

from backend.app.schemas.analysis_input import (
    DocumentMetadata,
    ExtractionInputEnvelope,
    SourceLocator,
    SourceUnit,
)
from backend.app.services.document_registry import DocumentRecord, DocumentRegistry
from backend.app.services.document_storage import DocumentStorage
from backend.app.services.document_validation import DOCX_MEDIA_TYPE, PDF_MEDIA_TYPE


WORD_NAMESPACE = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
WORD = "{%s}" % WORD_NAMESPACE


class DocumentPreparationError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.safe_message = message


def compute_sha256(path: Path, *, block_size: int = 64 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(block_size):
            digest.update(block)
    return digest.hexdigest()


def normalize_source_text(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n").strip()


def chunk_source_text(text: str, max_chars: int) -> list[str]:
    """Split normalized text without rewriting it, preferring newline/whitespace boundaries."""

    if max_chars < 1:
        raise ValueError("max_chars must be positive")
    remaining = normalize_source_text(text)
    chunks: list[str] = []
    while remaining:
        if len(remaining) <= max_chars:
            chunks.append(remaining)
            break
        cut = remaining.rfind("\n", 0, max_chars + 1)
        if cut < 1:
            cut = max(
                remaining.rfind(" ", 0, max_chars + 1),
                remaining.rfind("\t", 0, max_chars + 1),
            )
        if cut < 1:
            cut = max_chars
        chunk = remaining[:cut].strip()
        remaining = remaining[cut:].strip()
        if chunk:
            chunks.append(chunk)
    return chunks


class DocumentPreparationService:
    def __init__(
        self,
        storage: DocumentStorage,
        registry: DocumentRegistry,
        *,
        max_source_unit_chars: int = 4_000,
    ) -> None:
        if max_source_unit_chars < 1:
            raise ValueError("max_source_unit_chars must be positive")
        self.storage = storage
        self.registry = registry
        self.max_source_unit_chars = max_source_unit_chars

    def prepare_extraction_input(self, document_id: str) -> ExtractionInputEnvelope:
        record = self.registry.get(document_id)
        if record is None:
            raise DocumentPreparationError("document_unknown", "The document is not registered.")

        with self.storage.lease(document_id) as path:
            if not path.is_file():
                self.registry.remove(document_id)
                raise DocumentPreparationError(
                    "document_expired_or_missing",
                    "The document has expired or is no longer available.",
                )
            try:
                if compute_sha256(path) != record.sha256:
                    raise DocumentPreparationError("parse_failed", "The document could not be prepared safely.")
                if record.media_type == PDF_MEDIA_TYPE:
                    source_units = self._parse_pdf(path)
                elif record.media_type == DOCX_MEDIA_TYPE:
                    source_units = self._parse_docx(path)
                else:
                    raise DocumentPreparationError("parse_failed", "The document could not be prepared safely.")
                if not source_units:
                    raise DocumentPreparationError(
                        "no_extractable_text",
                        "The document contains no extractable text or table content.",
                    )
                return ExtractionInputEnvelope(
                    document_metadata=DocumentMetadata(
                        document_id=record.document_id,
                        file_name=record.file_name,
                        media_type=record.media_type,
                        sha256=record.sha256,
                    ),
                    source_units=source_units,
                )
            except DocumentPreparationError:
                raise
            except Exception as exc:
                raise DocumentPreparationError("parse_failed", "The document could not be prepared safely.") from exc

    def _parse_pdf(self, path: Path) -> list[SourceUnit]:
        reader = PdfReader(path, strict=True)
        if reader.is_encrypted:
            raise DocumentPreparationError("parse_failed", "The document could not be prepared safely.")
        units: list[SourceUnit] = []
        for page_number, page in enumerate(reader.pages, start=1):
            chunks = chunk_source_text(page.extract_text() or "", self.max_source_unit_chars)
            for chunk_number, content in enumerate(chunks, start=1):
                chunk_id = f"P{page_number:04d}-C{chunk_number:03d}"
                units.append(
                    SourceUnit(
                        evidence_id=f"EV-{chunk_id}",
                        evidence_type="TEXT",
                        locator=SourceLocator(page=page_number, chunk_id=chunk_id),
                        content=content,
                    )
                )
        return units

    def _parse_docx(self, path: Path) -> list[SourceUnit]:
        with zipfile.ZipFile(path) as package:
            payload = package.read("word/document.xml")
        upper = payload.upper()
        if b"<!DOCTYPE" in upper or b"<!ENTITY" in upper:
            raise DocumentPreparationError("parse_failed", "The document could not be prepared safely.")
        root = ElementTree.fromstring(payload)
        body = root.find(f"{WORD}body")
        if body is None:
            raise DocumentPreparationError("parse_failed", "The document could not be prepared safely.")

        units: list[SourceUnit] = []
        paragraph_number = 0
        table_number = 0
        for element in self._iter_docx_blocks(body):
            if element.tag == f"{WORD}p":
                paragraph_number += 1
                content = self._paragraph_text(element)
                paragraph_id = f"P{paragraph_number:04d}"
                self._append_docx_chunks(units, content, "TEXT", paragraph_id=paragraph_id)
            elif element.tag == f"{WORD}tbl":
                table_number += 1
                content = self._table_text(element)
                table_id = f"T{table_number:04d}"
                self._append_docx_chunks(units, content, "TABLE", table_id=table_id)
        return units

    @classmethod
    def _iter_docx_blocks(
        cls, container: ElementTree.Element
    ) -> Iterator[ElementTree.Element]:
        """Yield supported content blocks without walking unrelated descendants."""

        for child in container:
            if child.tag in {f"{WORD}p", f"{WORD}tbl"}:
                yield child
            elif child.tag == f"{WORD}sdt":
                for content in child.findall(f"./{WORD}sdtContent"):
                    yield from cls._iter_docx_blocks(content)

    def _append_docx_chunks(
        self,
        units: list[SourceUnit],
        content: str,
        evidence_type: str,
        *,
        paragraph_id: str | None = None,
        table_id: str | None = None,
    ) -> None:
        chunks = chunk_source_text(content, self.max_source_unit_chars)
        prefix = paragraph_id or table_id
        if prefix is None:
            raise ValueError("DOCX source unit requires a paragraph or table identifier")
        for chunk_number, chunk in enumerate(chunks, start=1):
            chunk_id = f"{prefix}-C{chunk_number:03d}"
            units.append(
                SourceUnit(
                    evidence_id=f"EV-{chunk_id}",
                    evidence_type=evidence_type,
                    locator=SourceLocator(
                        paragraph_id=paragraph_id,
                        table_id=table_id,
                        chunk_id=chunk_id,
                    ),
                    content=chunk,
                )
            )

    @staticmethod
    def _paragraph_text(paragraph: ElementTree.Element) -> str:
        parts: list[str] = []
        for element in paragraph.iter():
            if element.tag == f"{WORD}t":
                parts.append(element.text or "")
            elif element.tag == f"{WORD}tab":
                parts.append("\t")
            elif element.tag in {f"{WORD}br", f"{WORD}cr"}:
                parts.append("\n")
        return normalize_source_text("".join(parts))

    @classmethod
    def _table_text(cls, table: ElementTree.Element) -> str:
        rows: list[str] = []
        for row in table.findall(f"./{WORD}tr"):
            cells: list[str] = []
            for cell in row.findall(f"./{WORD}tc"):
                blocks: list[str] = []
                for item in cls._iter_docx_blocks(cell):
                    if item.tag == f"{WORD}p":
                        content = cls._paragraph_text(item)
                    else:
                        content = cls._table_text(item)
                    if content:
                        blocks.append(content)
                cells.append("\n".join(blocks))
            rows.append("\t".join(cells))
        return normalize_source_text("\n".join(rows))
