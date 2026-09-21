"""Thread-safe in-memory metadata registry for validated local documents."""

from __future__ import annotations

import threading
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DocumentRecord:
    document_id: str
    file_name: str
    media_type: str
    size_bytes: int
    page_count: int | None
    sha256: str


class DocumentRegistry:
    """Keep safe metadata only; source bytes, content, and paths are never stored."""

    def __init__(self) -> None:
        self._records: dict[str, DocumentRecord] = {}
        self._lock = threading.RLock()

    def register(self, record: DocumentRecord) -> None:
        with self._lock:
            if record.document_id in self._records:
                raise ValueError("document identifier is already registered")
            self._records[record.document_id] = record

    def get(self, document_id: str) -> DocumentRecord | None:
        with self._lock:
            return self._records.get(document_id)

    def remove(self, document_id: str) -> bool:
        with self._lock:
            return self._records.pop(document_id, None) is not None

    def __len__(self) -> int:
        with self._lock:
            return len(self._records)
