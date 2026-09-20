"""Runtime configuration for the local APP-001 backend skeleton."""

from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass
from pathlib import Path


MEBIBYTE = 1024 * 1024


@dataclass(frozen=True, slots=True)
class Settings:
    """Small, explicit configuration surface for APP-001."""

    storage_root: Path
    max_upload_bytes: int = 10 * MEBIBYTE
    max_pdf_pages: int = 50
    upload_ttl_seconds: int = 60 * 60
    read_chunk_bytes: int = 64 * 1024
    max_docx_entries: int = 2_048
    max_docx_uncompressed_bytes: int = 100 * MEBIBYTE
    max_docx_entry_bytes: int = 50 * MEBIBYTE
    max_docx_compression_ratio: int = 1_000

    @classmethod
    def from_environment(cls) -> "Settings":
        configured_root = os.environ.get("AI_IP_UPLOAD_ROOT")
        root = (
            Path(configured_root)
            if configured_root
            else Path(tempfile.gettempdir()) / "ai-ip-generator" / "uploads"
        )
        return cls(storage_root=root)
