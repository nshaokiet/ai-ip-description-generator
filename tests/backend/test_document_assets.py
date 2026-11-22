"""Registered DOCX asset bytes and provenance, never decoded or redrawn."""
from dataclasses import FrozenInstanceError
import hashlib
import io
import os
from types import SimpleNamespace
from zipfile import ZipFile, ZIP_DEFLATED

from docx import Document
from PIL import Image
from fastapi.testclient import TestClient
import pytest

from backend.app.core.config import Settings
from backend.app.main import create_app
from backend.app.services import document_assets as assets
from tests.backend.test_document_upload import synthetic_pdf
from tests.e2e.provider_tripwire import ProviderTripwire

PRINCIPAL = {"owner": "owner_a", "actor": "specialist_a", "context": "local_inspection"}


@pytest.fixture(autouse=True)
def offline():
    with ProviderTripwire() as guard:
        yield guard
        guard.assert_no_unexpected_activity()
        assert all(value == 0 for value in guard.snapshot().values())


def docx_bytes(format="PNG"):
    buffer = io.BytesIO();Image.new("RGB", (16, 16), "white").save(buffer, format=format)
    data = buffer.getvalue();document = Document()
    document.add_paragraph("See Fig. 1 for the synthetic controller.")
    document.add_picture(io.BytesIO(data))
    document.add_paragraph("Fig. 1 Synthetic controller", style="Caption")
    table = document.add_table(rows=1, cols=2)
    table.cell(0, 0).text = "Synthetic parameter";table.cell(0, 1).text = "12 percent"
    output = io.BytesIO();document.save(output)
    return output.getvalue(), data


def replace_member(data, name, value):
    output = io.BytesIO()
    with ZipFile(io.BytesIO(data)) as original, ZipFile(output, "w", ZIP_DEFLATED) as result:
        for member in original.namelist():
            result.writestr(member, value if member == name else original.read(member))
    return output.getvalue()


@pytest.fixture
def host(tmp_path):
    app = create_app(Settings(storage_root=tmp_path / "uploads"))
    calls = []
    def authority(request):
        calls.append(request)
        return request.owner == "owner_a" and request.actor == "specialist_a" and request.context == "local_inspection"
    inspector = assets.DocumentAssetInspector(app.state.document_storage, app.state.document_registry,
        app.state.document_preparation_service, app.state.document_validator, authorizer=authority)
    with TestClient(app) as client:
        yield SimpleNamespace(app=app, inspector=inspector, client=client, calls=calls)


def upload(host, data=None):
    if data is None:data = docx_bytes()[0]
    response = host.client.post("/api/documents", files={"file": ("synthetic.docx", data,
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document")})
    assert response.status_code == 201,response.text
    return response.json()["document_id"]


@pytest.mark.parametrize("format", ["PNG", "JPEG"])
def test_registered_docx_original_bytes_locators_table_caption_and_reference(host, format):
    data, original_image = docx_bytes(format)
    identity = upload(host, data)
    result = host.inspector.inspect(identity, **PRINCIPAL)
    assert result.source_sha256 == hashlib.sha256(data).hexdigest()
    assert result.inspection == host.calls[-1] and result.inspected_at.tzinfo is not None
    assert result.status == "REVIEW_REQUIRED" and not result.redraw_implemented
    assert len(result.assets) == 1
    image = result.assets[0]
    assert image.data == original_image and image.sha256 == hashlib.sha256(original_image).hexdigest()
    assert image.format_hint == format and image.source_page is None
    assert image.caption is None and image.related_specification_section is None
    assert image.byte_validation == "SOURCE_BYTES_ONLY_PIXELS_NOT_VALIDATED"
    assert image.locators[0].part == "word/document.xml"
    assert image.locators[0].xml_paragraph_index == 2
    assert result.captions[0].text == "Fig. 1 Synthetic controller"
    assert result.captions[0].xml_paragraph_index == 3
    assert result.text_references[0].literal == "Fig. 1"
    assert result.tables and result.tables[0].evidence_id.startswith("EV-T")
    assert "CAPTION_ASSOCIATION_NOT_VERIFIED" in result.warnings
    assert "Synthetic controller" not in repr(result)
    with pytest.raises(FrozenInstanceError):image.caption = "invented association"


def test_pdf_asset_extraction_is_explicitly_unsupported(host):
    response = host.client.post("/api/documents", files={"file": ("sample.pdf", synthetic_pdf(), "application/pdf")})
    assert response.status_code == 201
    result = host.inspector.inspect(response.json()["document_id"], **PRINCIPAL)
    assert result.assets == () and "PDF_IMAGE_EXTRACTION_NOT_IMPLEMENTED" in result.warnings
    assert result.status == "REVIEW_REQUIRED"


def test_other_format_is_flagged_not_decoded(host):
    identity = upload(host, docx_bytes("GIF")[0])
    result = host.inspector.inspect(identity, **PRINCIPAL)
    assert not result.assets and "UNSUPPORTED_IMAGE_TARGET_REVIEW_REQUIRED" in result.warnings


def test_no_image_decoding_occurs(host, monkeypatch):
    identity = upload(host)
    def forbidden(*args, **kwargs):raise AssertionError("unexpected image decode")
    monkeypatch.setattr(Image, "open", forbidden)
    assert host.inspector.inspect(identity, **PRINCIPAL).assets


@pytest.mark.parametrize("mode", ["tamper", "delete", "expire"])
def test_missing_changed_or_expired_source_denied(host, mode):
    identity = upload(host);storage = host.app.state.document_storage;path = storage.path_for(identity)
    if mode == "tamper":path.write_bytes(b"x" * path.stat().st_size)
    elif mode == "delete":storage.delete(identity)
    else:os.utime(path, (1, 1))
    with pytest.raises(assets.AssetInspectionError, match="SOURCE_UNAVAILABLE_OR_CHANGED"):
        host.inspector.inspect(identity, **PRINCIPAL)


def test_default_missing_authority_and_wrong_scope_deny(host):
    identity = upload(host)
    with pytest.raises(assets.AssetInspectionError, match="AUTHORIZATION_REQUIRED"):
        host.inspector.inspect(identity, **{**PRINCIPAL, "actor": "untrusted"})
    with pytest.raises(assets.AssetInspectionError, match="AUTHORIZATION_REQUIRED"):
        host.inspector.inspect(identity, **{**PRINCIPAL, "owner": "owner_b"})
    host.inspector._authorizer = None
    with pytest.raises(assets.AssetInspectionError, match="AUTHORIZATION_REQUIRED"):
        host.inspector.inspect(identity, **PRINCIPAL)


def test_callback_source_change_cannot_return_assets(host):
    identity = upload(host)
    def mutate(_):
        path = host.app.state.document_storage.path_for(identity)
        path.write_bytes(b"x" * path.stat().st_size)
        return True
    host.inspector._authorizer = mutate
    with pytest.raises(assets.AssetInspectionError, match="SOURCE_UNAVAILABLE_OR_CHANGED"):
        host.inspector.inspect(identity, **PRINCIPAL)


@pytest.mark.parametrize("limit_name", ["MAX_ASSET_BYTES", "MAX_TOTAL_BYTES", "MAX_ASSETS", "MAX_XML_BYTES"])
def test_bounds_fail_closed_before_returning_partial_manifest(host, monkeypatch, limit_name):
    identity = upload(host)
    monkeypatch.setattr(assets, limit_name, 0)  # Lower a local test limit to exercise denial, never bypass a guard.
    with pytest.raises(assets.AssetInspectionError):
        host.inspector.inspect(identity, **PRINCIPAL)


def test_xml_dtd_and_utf16_entity_patterns_rejected_without_expansion(tmp_path):
    for index, raw in enumerate([b'<!DOCTYPE x [<!ENTITY s "secret">]><x>&s;</x>',
                                '<!DOCTYPE x [<!ENTITY s "secret">]><x>&s;</x>'.encode("utf-16")]):
        path = tmp_path / f"fixture-{index}.zip"
        with ZipFile(path, "w") as z:z.writestr("word/document.xml", raw)
        with ZipFile(path) as z, pytest.raises(assets.AssetInspectionError, match="UNSAFE_XML"):
            assets._xml(z, "word/document.xml")


def test_callback_errors_are_sanitized(host):
    identity = upload(host)
    def broken(_):raise RuntimeError("private figure content")
    host.inspector._authorizer = broken
    with pytest.raises(assets.AssetInspectionError, match="^AUTHORIZATION_REQUIRED$"):
        host.inspector.inspect(identity, **PRINCIPAL)


def test_unsupported_member_path_is_not_opened_or_extracted(tmp_path):
    data, _ = docx_bytes()
    with ZipFile(io.BytesIO(data)) as z:
        raw = z.read("word/_rels/document.xml.rels")
    changed = raw.replace(b'Target="media/image1.png"', b'Target="../../outside.png"')
    assert changed != raw
    path = tmp_path / "unsupported.docx"
    path.write_bytes(replace_member(data, "word/_rels/document.xml.rels", changed))
    images, _, warnings = assets.DocumentAssetInspector._docx(path)
    assert not images and "UNSUPPORTED_IMAGE_TARGET_REVIEW_REQUIRED" in warnings
    assert not (tmp_path / "outside.png").exists()


def test_external_image_relationship_is_denied_even_in_parser_subset(tmp_path):
    data, _ = docx_bytes()
    with ZipFile(io.BytesIO(data)) as z:
        raw = z.read("word/_rels/document.xml.rels")
    changed = raw.replace(b'Target="media/image1.png"', b'Target="https://example.invalid/image.png" TargetMode="External"')
    assert changed != raw
    path = tmp_path / "external.docx"
    path.write_bytes(replace_member(data, "word/_rels/document.xml.rels", changed))
    with pytest.raises(assets.AssetInspectionError, match="UNSAFE_IMAGE_RELATIONSHIP"):
        assets.DocumentAssetInspector._docx(path)
