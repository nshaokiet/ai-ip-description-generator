"""Controlled P2-005 to P2-006 offline export for the synthetic staging app only.

The only accepted source is the pinned, repository-owned synthetic reconstruction
fixture. No externally supplied package, path, claims, or configuration is used.
"""
from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Lock
import json

from backend.app.services.invention_reconstruction import reconstruct_invention
from backend.app.services.supported_draft_claims_generation import generate_supported_draft_claims
from backend.app.services.uspto_document_package import assemble_uspto_document_package
from backend.app.services.uspto_offline_renderer import FILES, render_uspto_document_package
from backend.app.services.uspto_specification_generation import generate_uspto_specification

SAMPLE_ID = "p2-005-representative-system-v1"
FIXTURE = Path(__file__).resolve().parents[3] / "tests/fixtures/invention-reconstruction/v1.0.0/representative-system.json"
FIXTURE_SHA256 = "9a4be99442b39f871cb4bde7573fc9ddb47d942a6ad8fc4164c894122f18a233"
PDF_MIME = "application/pdf"
DOCX_MIME = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
MIME_TYPES = {filename: PDF_MIME if filename.endswith(".pdf") else DOCX_MIME for filename in FILES}
MAX_FILE_BYTES = 8 * 1024 * 1024
MAX_TOTAL_BYTES = 24 * 1024 * 1024


class SyntheticUSPTOUnavailable(RuntimeError):
    """Raised for any failed source/provenance/rendering validation, without details."""


class SyntheticUSPTOExports:
    def __init__(self):
        self._lock = Lock()
        self._files: dict[str, bytes] | None = None

    def _generate(self) -> dict[str, bytes]:
        fixture_bytes = FIXTURE.read_bytes()
        if sha256(fixture_bytes).hexdigest() != FIXTURE_SHA256:
            raise ValueError("Unrecognized synthetic sample")
        fixture = json.loads(fixture_bytes)
        envelope = fixture["source_envelope"]
        analysis = fixture["structured_analysis"]
        reconstruction = reconstruct_invention(envelope, analysis)
        p3 = {"source_document_synthetic": True}
        specification = generate_uspto_specification(reconstruction, p3)
        p4 = {
            "language": "en", "target_jurisdiction": "US",
            "requested_claim_types": ["SYSTEM"], "max_dependent_claims_per_family": 4,
            "source_document_synthetic": True,
            "selected_solution_id": reconstruction["invention_model"]["solution_concepts"][0]["solution_id"],
            "p2_003_generation_config": deepcopy(p3),
        }
        supported_claims = generate_supported_draft_claims(reconstruction, specification, p4)
        originals = dict(
            source_envelope=envelope,
            structured_analysis=analysis,
            reconstruction=reconstruction,
            specification=specification,
            p2_003_generation_config=p3,
            supported_claims=supported_claims,
            p2_004_generation_config=p4,
        )
        package = assemble_uspto_document_package(**originals)
        if package["review_boundary"]["filing_ready"] is not False:
            raise ValueError("Unexpected review boundary")
        claims = package["filing_view"]["claims"]
        if claims["status"] != "HUMAN_CONFIRMATION_REQUIRED" or claims["claims"]:
            raise ValueError("Unexpected claim projection")
        with TemporaryDirectory(prefix="p2-007-synthetic-") as tmp:
            outputs = render_uspto_document_package(package, **originals, output_dir=Path(tmp))
            if set(outputs) != set(FILES):
                raise ValueError("Renderer output mismatch")
            result: dict[str, bytes] = {}
            for filename in FILES:
                content = outputs[filename].read_bytes()
                if not content or len(content) > MAX_FILE_BYTES:
                    raise ValueError("Invalid output size")
                if filename.endswith(".pdf") and not content.startswith(b"%PDF-"):
                    raise ValueError("Invalid PDF signature")
                if filename.endswith(".docx") and not content.startswith(b"PK\x03\x04"):
                    raise ValueError("Invalid DOCX signature")
                result[filename] = content
            if sum(map(len, result.values())) > MAX_TOTAL_BYTES:
                raise ValueError("Export set exceeds budget")
            return result

    def get_files(self) -> dict[str, bytes]:
        with self._lock:
            if self._files is None:
                try:
                    self._files = self._generate()
                except Exception as exc:
                    raise SyntheticUSPTOUnavailable("Synthetic reference unavailable") from exc
            return self._files
