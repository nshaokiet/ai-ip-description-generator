"""S2-local pinned synthetic adapter; no provider or test-code imports."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

from backend.app.services.product_synthetic_workflow import SyntheticFixtureIdentity

ROOT = Path(__file__).resolve().parents[3]
MANIFEST = "tests/fixtures/api-ready/v1.0.0/manifest.json"
# Human 2026-11-13 / API-READY-WEB-GAP-001B-S2-A; immutable S2-local admission.
PINS = (
    ("controller.pdf", "application/pdf", 1015,
     "9bc8d4e20b2b88d2df0780294069e048b96c09a22a7012baa1efe5ba7f523975",
     "tests/fixtures/invention-reconstruction/v1.0.0/representative-system.json", 7026,
     "f453a7264e36cfbc7d71cc83ce3c5068ad360e95e56fb3896be840d1f63519c9",
     "7818a10a92b057db272ad6005f3f4daaf7372f73fc5b6a3a4f0606b9fe596704"),
    ("research-b.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", 1210,
     "dc3fb54cd9344c20c0b76b5d8e2229c6d54d253f4c2ecfba96783af3ae731eb3",
     "tests/fixtures/api-ready/v1.0.0/research-b-analysis.json", 4704,
     "b425fbf8e1f41551cbf00f51e3cff1ed2988182f0c70aff0dece54bdbf853dea",
     "54019588f7438b63955351e557268880118a12c86a5cee4d1bfd8c54fe14fac4"),
)


class PinnedSyntheticRuntime:
    synthetic_only = True

    def __init__(self):
        manifest = json.loads((ROOT / MANIFEST).read_bytes())
        entries = manifest["fixtures"]
        if (len(entries) != 2 or manifest["version"] != "1.0.0"
                or manifest["scope"] != "SYNTHETIC_TEST_ONLY" or manifest["production_admitted"] is not False
                or manifest["c2_pilot_admitted"] is not False or manifest["provider_budget_usd"] != 0):
            raise ValueError("Synthetic identity unavailable")
        self._analyses = {}
        for index, (entry, pin) in enumerate(zip(entries, PINS)):
            keys = ("filename", "media_type", "size_bytes", "sha256", "analysis_path",
                    "analysis_size_bytes", "analysis_sha256", "parsed_content_sha256")
            if tuple(entry[key] for key in keys) != pin:
                raise ValueError("Synthetic identity unavailable")
            source_path = ("tests/fixtures/product-synthetic/v1.0.0/controller.pdf" if index == 0
                           else "tests/fixtures/api-ready/v1.0.0/research-b.docx")
            if (entry["path"] != source_path or entry["analysis_media_type"] != "application/json"
                    or entry["analysis_json_pointer"] != ("/structured_analysis" if index == 0 else "")):
                raise ValueError("Synthetic identity unavailable")
            source = (ROOT / source_path).read_bytes()
            if len(source) != pin[2] or hashlib.sha256(source).hexdigest() != pin[3]:
                raise ValueError("Synthetic identity unavailable")
            scope = ("GIT_BLOB_LF: existing JSON checkout CRLF normalized to LF" if index == 0
                     else "EXACT_FILE_BYTES: UTF-8 JSON without line terminators")
            if entry["analysis_hash_scope"] != scope:
                raise ValueError("Synthetic identity unavailable")
            raw = (ROOT / entry["analysis_path"]).read_bytes()
            if index == 0:
                raw = raw.replace(b"\r\n", b"\n")
            if len(raw) != pin[5] or hashlib.sha256(raw).hexdigest() != pin[6]:
                raise ValueError("Synthetic identity unavailable")
            value = json.loads(raw)
            analysis = value["structured_analysis"] if index == 0 else value
            locator = ({"page": 1, "chunk_id": "P0001-C001"} if index == 0
                       else {"paragraph_id": "P0001", "chunk_id": "P0001-C001"})
            self._analyses[pin[3]] = (deepcopy(analysis), locator, pin)
        self.fixtures = tuple(SyntheticFixtureIdentity(p[3], p[1], p[2]) for p in PINS)

    def run_extraction(self, envelope, *, correlation_id=None):
        metadata = envelope.document_metadata
        selected = self._analyses.get(metadata.sha256)
        if selected is None or len(envelope.source_units) != 1:
            raise ValueError("Synthetic source unavailable")
        analysis, locator, pin = selected
        unit = envelope.source_units[0]
        if (metadata.file_name != pin[0] or metadata.media_type != pin[1]
                or unit.evidence_type != "TEXT" or unit.evidence_id != "EV-P0001-C001"
                or unit.locator.model_dump(exclude_none=True) != locator
                or hashlib.sha256(unit.content.encode()).hexdigest() != pin[7]):
            raise ValueError("Synthetic source unavailable")
        analysis = deepcopy(analysis)
        analysis["document_metadata"] = metadata.model_dump(exclude_none=True)
        analysis["evidence"][0].update(document_id=metadata.document_id,
                                       evidence_type=unit.evidence_type, locator=locator)
        # C1 independently performs canonical schema and source-grounding validation.
        return SimpleNamespace(analysis=analysis)
