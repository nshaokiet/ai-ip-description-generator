"""Ephemeral, path-isolated storage for validated uploads."""

from __future__ import annotations

import logging
import os
import threading
import time
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


LOGGER = logging.getLogger(__name__)


class UploadTooLargeError(ValueError):
    """Raised while streaming when an upload exceeds the configured limit."""


class EmptyUploadError(ValueError):
    """Raised when an upload contains no bytes."""


class DocumentStorage:
    """Store uploads under opaque IDs and remove them on failure or expiry."""

    def __init__(self, root: Path, *, ttl_seconds: int, max_upload_bytes: int, read_chunk_bytes: int) -> None:
        self.root = root.resolve()
        self.ttl_seconds = ttl_seconds
        self.max_upload_bytes = max_upload_bytes
        self.read_chunk_bytes = read_chunk_bytes
        self._active_ids: set[str] = set()
        self._lock = threading.RLock()
        self.root.mkdir(mode=0o700, parents=True, exist_ok=True)
        try:
            self.root.chmod(0o700)
        except OSError:
            pass

    def allocate_id(self) -> str:
        return uuid.uuid4().hex

    def path_for(self, document_id: str) -> Path:
        if len(document_id) != 32 or any(ch not in "0123456789abcdef" for ch in document_id):
            raise ValueError("Invalid opaque document identifier")
        candidate = (self.root / document_id).resolve()
        if candidate.parent != self.root:
            raise ValueError("Document path escaped storage root")
        return candidate

    async def stream_to_disk(self, upload: object, document_id: str) -> tuple[Path, int]:
        """Copy an UploadFile-like object in bounded chunks using exclusive creation."""

        path = self.path_for(document_id)
        total = 0
        try:
            descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(descriptor, "wb") as destination:
                while True:
                    chunk = await upload.read(self.read_chunk_bytes)
                    if not chunk:
                        break
                    total += len(chunk)
                    if total > self.max_upload_bytes:
                        raise UploadTooLargeError
                    destination.write(chunk)
                destination.flush()
                os.fsync(destination.fileno())
            if total == 0:
                raise EmptyUploadError
            return path, total
        except BaseException:
            self._unlink_path(path, document_id)
            raise

    def delete(self, document_id: str) -> bool:
        return self._unlink_path(self.path_for(document_id), document_id)

    def _unlink_path(self, path: Path, document_id: str) -> bool:
        try:
            path.unlink(missing_ok=True)
            return True
        except OSError:
            LOGGER.warning("document_cleanup_failed document_id=%s", document_id)
            return False

    @contextmanager
    def lease(self, document_id: str) -> Iterator[Path]:
        """Prevent an in-process TTL sweep from racing active downstream work."""

        with self._lock:
            self._active_ids.add(document_id)
        try:
            yield self.path_for(document_id)
        finally:
            with self._lock:
                self._active_ids.discard(document_id)

    def sweep_expired(self, *, now: float | None = None) -> list[str]:
        """Best-effort idempotent cleanup of opaque files at or beyond the TTL."""

        current_time = time.time() if now is None else now
        removed: list[str] = []
        try:
            candidates = list(self.root.iterdir())
        except OSError:
            LOGGER.warning("document_sweep_failed")
            return removed
        for path in candidates:
            document_id = path.name
            if not path.is_file() or len(document_id) != 32:
                continue
            with self._lock:
                if document_id in self._active_ids:
                    continue
            try:
                expired = current_time - path.stat().st_mtime >= self.ttl_seconds
            except OSError:
                continue
            if expired and self._unlink_path(path, document_id):
                removed.append(document_id)
        return removed

