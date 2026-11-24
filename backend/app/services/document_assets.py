"""Read-only DOCX byte/locator capture from registered source; never decode/redraw.

Source metadata and bytes are private native results, not browser/provider output.
The host authenticates the supplied inspection callback. Page/figure association
and scientific fidelity are deliberately REVIEW_REQUIRED, even for retained bytes.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
from pathlib import PurePosixPath
import re
from typing import Callable
from xml.etree import ElementTree
from zipfile import ZipFile

from backend.app.services.document_parsing import DocumentPreparationService, compute_sha256
from backend.app.services.document_registry import DocumentRegistry
from backend.app.services.document_storage import DocumentStorage
from backend.app.services.document_validation import DocumentValidator, DOCX_MEDIA_TYPE

WORD = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
DRAWING = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
REL = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
IMAGE_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"
MAX_ASSETS, MAX_ASSET_BYTES, MAX_TOTAL_BYTES, MAX_XML_BYTES = 32, 4*1024*1024, 16*1024*1024, 2*1024*1024


class AssetInspectionError(ValueError):
    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


@dataclass(frozen=True, slots=True)
class AssetInspectionAction:
    document_id: str
    source_sha256: str
    owner: str
    actor: str
    context: str
    purpose: str = "INSPECT_SOURCE_ASSETS"


@dataclass(frozen=True, slots=True)
class AssetLocator:
    part: str
    xml_paragraph_index: int
    relationship_id: str


@dataclass(frozen=True, slots=True)
class SourceAsset:
    media_member: str
    sha256: str
    format_hint: str
    data: bytes = field(repr=False)
    locators: tuple[AssetLocator, ...] = ()
    source_page: None = None
    caption: None = None
    related_specification_section: None = None
    status: str = "REVIEW_REQUIRED"
    byte_validation: str = "SOURCE_BYTES_ONLY_PIXELS_NOT_VALIDATED"


@dataclass(frozen=True, slots=True)
class CaptionCandidate:
    part: str
    xml_paragraph_index: int
    text: str = field(repr=False)
    status: str = "ASSOCIATION_REVIEW_REQUIRED"


@dataclass(frozen=True, slots=True)
class TextFigureReference:
    evidence_id: str
    locator: tuple[tuple[str, object], ...]
    literal: str = field(repr=False)
    status: str = "ASSOCIATION_REVIEW_REQUIRED"


@dataclass(frozen=True, slots=True)
class TableProvenance:
    evidence_id: str
    locator: tuple[tuple[str, object], ...]
    normalized_content_sha256: str


@dataclass(frozen=True, slots=True)
class DocumentAssetManifest:
    document_id: str
    source_sha256: str
    assets: tuple[SourceAsset, ...]
    captions: tuple[CaptionCandidate, ...]
    text_references: tuple[TextFigureReference, ...]
    tables: tuple[TableProvenance, ...]
    warnings: tuple[str, ...]
    inspection: AssetInspectionAction
    inspected_at: datetime
    contract_version: str = "1.0.0"
    status: str = "REVIEW_REQUIRED"
    redraw_implemented: bool = False


def _xml(package, name):
    info = package.getinfo(name)
    if info.file_size > MAX_XML_BYTES:
        raise AssetInspectionError("XML_LIMIT_EXCEEDED")
    raw = package.read(name)
    if b"\x00" in raw or b"<!DOCTYPE" in raw.upper() or b"<!ENTITY" in raw.upper():
        raise AssetInspectionError("UNSAFE_XML")
    return ElementTree.fromstring(raw)


class DocumentAssetInspector:
    def __init__(self, storage: DocumentStorage, registry: DocumentRegistry,
                 preparation: DocumentPreparationService, validator: DocumentValidator, *,
                 authorizer: Callable[[AssetInspectionAction], bool] | None = None):
        self._storage, self._registry = storage, registry
        self._preparation, self._validator, self._authorizer = preparation, validator, authorizer

    def _verify(self, record, path):
        if (self._registry.get(record.document_id) != record or path.is_symlink()
                or not path.is_file() or path.stat().st_size != record.size_bytes
                or compute_sha256(path) != record.sha256):
            raise AssetInspectionError("SOURCE_UNAVAILABLE_OR_CHANGED")

    def inspect(self, document_id: str, *, owner: str, actor: str, context: str) -> DocumentAssetManifest:
        if type(document_id) is not str or re.fullmatch(r"[a-f0-9]{32}", document_id) is None:
            raise AssetInspectionError("INVALID_DOCUMENT_ID")
        for value in (owner, actor, context):
            if type(value) is not str or re.fullmatch(r"[A-Za-z0-9_-]{1,128}", value) is None:
                raise AssetInspectionError("INVALID_PRINCIPAL")
        self._storage.sweep_expired()
        record = self._registry.get(document_id)
        if record is None:
            raise AssetInspectionError("SOURCE_UNAVAILABLE_OR_CHANGED")
        try:
            with self._storage.lease(document_id) as path:
                self._verify(record, path)
                request = AssetInspectionAction(document_id, record.sha256, owner, actor, context)
                try:
                    allowed = self._authorizer is not None and self._authorizer(request) is True
                except Exception:
                    allowed = False
                if not allowed:
                    raise AssetInspectionError("AUTHORIZATION_REQUIRED")
                self._verify(record, path)
                self._validator.validate(path, filename=record.file_name, declared_mime=record.media_type)
                if record.media_type != DOCX_MEDIA_TYPE:
                    self._verify(record, path)
                    return DocumentAssetManifest(document_id, record.sha256, (), (), (), (),
                        ("PDF_IMAGE_EXTRACTION_NOT_IMPLEMENTED", "REDRAW_NOT_IMPLEMENTED"), request, datetime.now(timezone.utc))
            # Reuse source-unit extraction before taking a fresh outer lease, avoiding nested leases.
            envelope = self._preparation.prepare_extraction_input(document_id)
            if envelope.document_metadata.sha256 != record.sha256:
                raise AssetInspectionError("SOURCE_UNAVAILABLE_OR_CHANGED")
            with self._storage.lease(document_id) as path:
                self._verify(record, path)
                assets, captions, warnings = self._docx(path)
                tables, references = [], []
                for unit in envelope.source_units:
                    locator = tuple(sorted(unit.locator.model_dump(exclude_none=True).items()))
                    if unit.evidence_type == "TABLE":
                        tables.append(TableProvenance(unit.evidence_id, locator,
                            hashlib.sha256(unit.content.encode("utf-8")).hexdigest()))
                    for match in re.finditer(r"\b(?:Fig(?:ure)?\.?|Hình)\s+[0-9A-Za-z]+", unit.content, re.IGNORECASE):
                        references.append(TextFigureReference(unit.evidence_id, locator, match.group()))
                self._verify(record, path)
                return DocumentAssetManifest(document_id, record.sha256, tuple(assets), tuple(captions),
                    tuple(references), tuple(tables), tuple(warnings), request, datetime.now(timezone.utc))
        except AssetInspectionError:
            raise
        except Exception:
            raise AssetInspectionError("SOURCE_OR_PACKAGE_INVALID") from None

    @staticmethod
    def _docx(path):
        warnings = ["DOCX_PAGE_NOT_DETERMINED", "CAPTION_ASSOCIATION_NOT_VERIFIED", "REDRAW_NOT_IMPLEMENTED"]
        with ZipFile(path) as package:
            root = _xml(package, "word/document.xml")
            names = set(package.namelist())
            relationships = {}
            if "word/_rels/document.xml.rels" in names:
                for rel in _xml(package, "word/_rels/document.xml.rels"):
                    if rel.get("Type") != IMAGE_REL:
                        continue
                    rid = rel.get("Id", "")
                    if not rid or rid in relationships or rel.get("TargetMode") == "External":
                        raise AssetInspectionError("UNSAFE_IMAGE_RELATIONSHIP")
                    relationships[rid] = rel.get("Target", "")
            if len(relationships) > MAX_ASSETS:
                raise AssetInspectionError("ASSET_COUNT_EXCEEDED")
            locations = {rid: [] for rid in relationships}
            captions = []
            for index, paragraph in enumerate(root.iter(WORD + "p"), 1):
                style = paragraph.find(WORD + "pPr/" + WORD + "pStyle")
                if style is not None and style.get(WORD + "val") == "Caption":
                    captions.append(CaptionCandidate("word/document.xml", index,
                        DocumentPreparationService._paragraph_text(paragraph)))
                for image in paragraph.iter(DRAWING + "blip"):
                    rid = image.get(REL + "embed")
                    if rid in locations:
                        locations[rid].append(AssetLocator("word/document.xml", index, rid))
                    else:
                        warnings.append("UNRESOLVED_IMAGE_REFERENCE_REVIEW_REQUIRED")
            captured, total = {}, 0
            for rid, target in relationships.items():
                if target.startswith("/word/"):
                    target = target[len("/word/"):]
                if re.fullmatch(r"media/[A-Za-z0-9_.-]+\.(?:png|jpe?g)", target, re.IGNORECASE) is None:
                    warnings.append("UNSUPPORTED_IMAGE_TARGET_REVIEW_REQUIRED")
                    continue
                member = str(PurePosixPath("word") / target)
                if member not in names:
                    raise AssetInspectionError("MISSING_IMAGE_MEMBER")
                if member in captured:
                    captured[member] = (captured[member][0], captured[member][1] + tuple(locations[rid]))
                    continue
                info = package.getinfo(member)
                if info.file_size > MAX_ASSET_BYTES:
                    raise AssetInspectionError("ASSET_SIZE_EXCEEDED")
                with package.open(member) as stream:
                    data = stream.read(MAX_ASSET_BYTES + 1)
                if len(data) > MAX_ASSET_BYTES:
                    raise AssetInspectionError("ASSET_SIZE_EXCEEDED")
                total += len(data)
                if total > MAX_TOTAL_BYTES:
                    raise AssetInspectionError("TOTAL_ASSET_SIZE_EXCEEDED")
                hint = ("PNG" if data.startswith(b"\x89PNG\r\n\x1a\n") else
                        "JPEG" if data.startswith(b"\xff\xd8\xff") else None)
                if hint is None:
                    warnings.append("IMAGE_SIGNATURE_UNSUPPORTED_REVIEW_REQUIRED")
                    continue
                asset = SourceAsset(member, hashlib.sha256(data).hexdigest(), hint, data)
                captured[member] = (asset, tuple(locations[rid]))
            from dataclasses import replace
            assets = [replace(asset, locators=locators) for asset, locators in captured.values()]
            if any(not asset.locators for asset in assets):
                warnings.append("UNREFERENCED_OR_LEGACY_IMAGE_REVIEW_REQUIRED")
            return assets, captions, sorted(set(warnings))
