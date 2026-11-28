"""Controlled manual evidence on actual registered uploads; no search or egress.

Native trusted-host API only. Callback identity/actual Human decisions must be
verified by the host. Audit hashes show consistency, not authenticated identity.
No provider/drafting route is wired here; evidence and audit are process-local.
"""
from __future__ import annotations

from contextlib import contextmanager
from dataclasses import asdict, dataclass, replace
from datetime import date, datetime, timezone
import re
from threading import RLock
from typing import Callable
from urllib.parse import unquote, urlsplit

from backend.app.services.custody_review import FrozenObject, freeze_originals, review_documents
from backend.app.services.document_parsing import compute_sha256
from backend.app.services.document_registry import DocumentRecord, DocumentRegistry
from backend.app.services.document_storage import DocumentStorage
from backend.app.services.supported_draft_claims_validation import sha256_canonical

CONTRACT_VERSION = "1.0.0"
INCOMPLETE_WARNING = "Prior Art Search Incomplete"
UNVERIFIED_WARNING = "Manual references are user-recorded, not independently verified; no novelty or patentability assessment."
ID = re.compile(r"[A-Za-z0-9_-]{1,128}\Z")
DOCUMENT_ID = re.compile(r"[a-f0-9]{32}\Z")


class PriorArtError(ValueError):
    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


def _text(value: str, *, limit: int = 4096, empty: bool = False) -> None:
    if type(value) is not str:
        raise PriorArtError("INVALID_TEXT")
    try:
        valid = len(value.encode("utf-8")) <= limit
    except UnicodeError:
        valid = False
    if not valid or (not empty and not value.strip()):
        raise PriorArtError("INVALID_TEXT")
    if any(ord(c) < 32 and c not in "\n\t" or ord(c) == 127 for c in value):
        raise PriorArtError("INVALID_TEXT")


def _identifier(value: str) -> None:
    if type(value) is not str or ID.fullmatch(value) is None:
        raise PriorArtError("INVALID_IDENTIFIER")


def _date(value: str) -> date:
    if type(value) is not str or re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value) is None:
        raise PriorArtError("INVALID_RETRIEVAL_DATE")
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise PriorArtError("INVALID_RETRIEVAL_DATE") from None


def _url(value: str) -> None:
    if value == "":
        return
    _text(value, limit=2048)
    try:
        parts = urlsplit(value)
        valid = (parts.scheme == "https" and parts.hostname is not None
                 and parts.username is None and parts.password is None
                 and parts.port in (None, 443)
                 and not any(c.isspace() or ord(c) < 32 or c == "\\" for c in unquote(value)))
    except ValueError:
        valid = False
    if not valid:
        raise PriorArtError("INVALID_SOURCE_URL")


@dataclass(frozen=True, slots=True)
class PriorArtReference:
    reference_id: str
    kind: str
    citation: str
    source: str
    retrieved_on: str
    source_url: str = ""
    relevant_passage: str = ""
    similarities: str = ""
    differences: str = ""

    def __post_init__(self) -> None:
        _identifier(self.reference_id)
        if type(self.kind) is not str or self.kind not in ("PATENT", "NON_PATENT"):
            raise PriorArtError("INVALID_REFERENCE_KIND")
        _text(self.citation, limit=1024)
        _text(self.source, limit=512)
        _date(self.retrieved_on)
        _url(self.source_url)
        for value in (self.relevant_passage, self.similarities, self.differences):
            _text(value, empty=True)


@dataclass(frozen=True, slots=True)
class ManualSearchRecord:
    search_scope: str
    limitations: str
    references: tuple[PriorArtReference, ...] = ()
    search_terms: str = ""
    status: str = "INCOMPLETE"

    def __post_init__(self) -> None:
        _text(self.search_scope)
        _text(self.limitations)
        _text(self.search_terms, empty=True)
        if type(self.references) is not tuple or len(self.references) > 32:
            raise PriorArtError("INVALID_REFERENCES")
        if any(type(item) is not PriorArtReference for item in self.references):
            raise PriorArtError("INVALID_REFERENCES")
        if len({item.reference_id for item in self.references}) != len(self.references):
            raise PriorArtError("DUPLICATE_REFERENCE_ID")
        if type(self.status) is not str or self.status not in ("INCOMPLETE", "MANUAL_SEARCH_RECORDED"):
            raise PriorArtError("INVALID_SEARCH_STATUS")
        if self.status == "MANUAL_SEARCH_RECORDED" and not self.references:
            raise PriorArtError("REFERENCES_REQUIRED")


@dataclass(frozen=True, slots=True)
class PriorArtAction:
    action: str
    document_id: str
    source_sha256: str
    dossier_revision: int
    dossier_sha256: str
    owner: str
    actor: str
    context: str
    reason: str


@dataclass(frozen=True, slots=True)
class PriorArtAuditEvent:
    sequence: int
    request: PriorArtAction
    recorded_at: datetime
    previous_sha256: str
    sha256: str


@dataclass(frozen=True, slots=True)
class PriorArtSnapshot:
    document_id: str
    source_sha256: str
    dossier_revision: int
    dossier_sha256: str
    content: FrozenObject
    audit: tuple[PriorArtAuditEvent, ...]


@dataclass(frozen=True, slots=True)
class DraftingAssessment:
    allowed: bool
    code: str
    warnings: tuple[str, ...]
    source_sha256: str
    dossier_revision: int
    dossier_sha256: str
    decision_sha256: str | None = None


@dataclass(frozen=True, slots=True)
class _Record:
    owner: str
    snapshot: PriorArtSnapshot


def _event_digest(sequence, request, recorded_at, previous):
    return sha256_canonical({"sequence": sequence, "request": asdict(request),
                             "recorded_at": recorded_at.isoformat(), "previous_sha256": previous})


class ManualPriorArtWorkflow:
    """Bounded ephemeral evidence with real source-custody checks and explicit decisions."""
    def __init__(self, storage: DocumentStorage, registry: DocumentRegistry, *,
                 authorizer: Callable[[PriorArtAction], bool] | None = None,
                 clock: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
                 max_records: int = 32, max_audit_events: int = 128) -> None:
        if (type(max_records) is not int or not 1 <= max_records <= 256
                or type(max_audit_events) is not int or not 2 <= max_audit_events <= 1024):
            raise PriorArtError("INVALID_CAPACITY")
        self._storage, self._registry = storage, registry
        self._authorizer, self._clock = authorizer, clock
        self._max_records, self._max_events = max_records, max_audit_events
        self._records: dict[str, _Record] = {}
        self._lock = RLock()

    def _now(self) -> datetime:
        try:
            now = self._clock()
            if not isinstance(now, datetime) or now.tzinfo is None or now.utcoffset() is None:
                raise ValueError
            return now.astimezone(timezone.utc)
        except Exception:
            raise PriorArtError("CLOCK_UNAVAILABLE") from None

    @staticmethod
    def _principal(owner, actor, context) -> None:
        for value in (owner, actor, context):
            _identifier(value)

    def _authorize(self, request: PriorArtAction) -> None:
        try:
            allowed = self._authorizer is not None and self._authorizer(request) is True
        except Exception:
            allowed = False
        if not allowed:
            raise PriorArtError("AUTHORIZATION_REQUIRED")

    def _verify_source(self, record: DocumentRecord, path) -> None:
        try:
            valid = (self._registry.get(record.document_id) == record and not path.is_symlink()
                     and path.is_file() and path.stat().st_size == record.size_bytes
                     and record.size_bytes <= self._storage.max_upload_bytes
                     and compute_sha256(path) == record.sha256)
        except (OSError, ValueError):
            valid = False
        if not valid:
            raise PriorArtError("SOURCE_UNAVAILABLE_OR_CHANGED")

    @contextmanager
    def _source(self, document_id):
        if type(document_id) is not str or DOCUMENT_ID.fullmatch(document_id) is None:
            raise PriorArtError("INVALID_DOCUMENT_ID")
        self._storage.sweep_expired()
        record = self._registry.get(document_id)
        if record is None:
            raise PriorArtError("SOURCE_UNAVAILABLE_OR_CHANGED")
        with self._storage.lease(document_id) as path:
            self._verify_source(record, path)
            yield record, path

    def _current(self, document_id, owner) -> _Record:
        if type(document_id) is not str or DOCUMENT_ID.fullmatch(document_id) is None:
            raise PriorArtError("INVALID_DOCUMENT_ID")
        record = self._records.get(document_id)
        if record is None or record.owner != owner:
            raise PriorArtError("PRIOR_ART_RECORD_NOT_FOUND")
        snapshot = record.snapshot
        if sha256_canonical(review_documents(snapshot.content)) != snapshot.dossier_sha256:
            raise PriorArtError("AUDIT_INTEGRITY_FAILED")
        previous = "0" * 64
        for index, event in enumerate(snapshot.audit, 1):
            if (event.sequence != index or event.previous_sha256 != previous
                    or event.sha256 != _event_digest(index, event.request, event.recorded_at, previous)):
                raise PriorArtError("AUDIT_INTEGRITY_FAILED")
            previous = event.sha256
        if (not snapshot.audit or snapshot.audit[-1].request.dossier_sha256 != snapshot.dossier_sha256
                or snapshot.audit[-1].request.dossier_revision != snapshot.dossier_revision):
            raise PriorArtError("AUDIT_INTEGRITY_FAILED")
        return record

    @staticmethod
    def _expected(record: _Record | None, expected_revision) -> None:
        version = 0 if record is None else record.snapshot.dossier_revision
        if type(expected_revision) is not int or expected_revision != version:
            raise PriorArtError("STALE_DOSSIER_REVISION")

    def _event(self, request, audit) -> PriorArtAuditEvent:
        if len(audit) >= self._max_events:
            raise PriorArtError("AUDIT_CAPACITY_REACHED")
        now = self._now()
        if audit and now < audit[-1].recorded_at:
            raise PriorArtError("CLOCK_ROLLBACK")
        previous = audit[-1].sha256 if audit else "0" * 64
        sequence = len(audit) + 1
        return PriorArtAuditEvent(sequence, request, now, previous,
                                 _event_digest(sequence, request, now, previous))

    def save(self, document_id: str, search: ManualSearchRecord, *, owner: str,
             expected_revision: int, actor: str, context: str, reason: str) -> PriorArtSnapshot:
        self._principal(owner, actor, context)
        _text(reason, limit=1024)
        if type(search) is not ManualSearchRecord:
            raise PriorArtError("INVALID_MANUAL_RECORD")
        with self._lock, self._source(document_id) as (source, path):
            previous = self._records.get(document_id)
            if previous is not None:
                previous = self._current(document_id, owner)
                if previous.snapshot.source_sha256 != source.sha256:
                    raise PriorArtError("SOURCE_UNAVAILABLE_OR_CHANGED")
            self._expected(previous, expected_revision)
            if previous is None and len(self._records) >= self._max_records:
                raise PriorArtError("CAPACITY_REACHED")
            if any(_date(r.retrieved_on) > self._now().date() for r in search.references):
                raise PriorArtError("FUTURE_RETRIEVAL_DATE")
            version = expected_revision + 1
            content = freeze_originals({"contract_version": CONTRACT_VERSION,
                "document_id": document_id, "source_sha256": source.sha256,
                "dossier_revision": version, "manual_search": {**asdict(search),
                    "references": [asdict(ref) for ref in search.references]},
                "reference_verification": "USER_RECORDED_NOT_VERIFIED",
                "search_exhaustiveness": "NOT_DETERMINED",
                "novelty_assessed": False, "patentability_assessed": False})
            digest = sha256_canonical(review_documents(content))
            request = PriorArtAction("SAVE_MANUAL_SEARCH", document_id, source.sha256,
                                    version, digest, owner, actor, context, reason)
            self._authorize(request)
            if self._records.get(document_id) is not previous:
                raise PriorArtError("STALE_DOSSIER_REVISION")
            if previous is None and len(self._records) >= self._max_records:
                raise PriorArtError("CAPACITY_REACHED")
            self._verify_source(source, path)
            audit = previous.snapshot.audit if previous else ()
            event = self._event(request, audit)
            snapshot = PriorArtSnapshot(document_id, source.sha256, version, digest, content, audit + (event,))
            self._records[document_id] = _Record(owner, snapshot)
            return snapshot

    def _read(self, document_id, owner, actor, context, action, expected_revision=None, reason="Read current manual evidence"):
        self._principal(owner, actor, context)
        _text(reason, limit=1024)
        record = self._current(document_id, owner)
        if expected_revision is not None:
            self._expected(record, expected_revision)
        with self._source(document_id) as (source, path):
            snapshot = record.snapshot
            if source.sha256 != snapshot.source_sha256:
                raise PriorArtError("SOURCE_UNAVAILABLE_OR_CHANGED")
            request = PriorArtAction(action, document_id, source.sha256, snapshot.dossier_revision,
                                    snapshot.dossier_sha256, owner, actor, context, reason)
            self._authorize(request)
            if self._records.get(document_id) is not record:
                raise PriorArtError("STALE_DOSSIER_REVISION")
            self._verify_source(source, path)
            if self._now() < snapshot.audit[-1].recorded_at:
                raise PriorArtError("CLOCK_ROLLBACK")
            return record, request

    def snapshot(self, document_id: str, *, owner: str, actor: str, context: str) -> PriorArtSnapshot:
        with self._lock:
            record, _ = self._read(document_id, owner, actor, context, "READ_MANUAL_SEARCH")
            return record.snapshot

    def decide(self, document_id: str, *, owner: str, expected_revision: int,
               choice: str, actor: str, context: str, reason: str) -> PriorArtSnapshot:
        if type(expected_revision) is not int or expected_revision < 1:
            raise PriorArtError("STALE_DOSSIER_REVISION")
        if type(choice) is not str or choice not in ("CONTINUE", "STOP"):
            raise PriorArtError("INVALID_DECISION")
        with self._lock:
            record, request = self._read(document_id, owner, actor, context,
                choice + "_DRAFT", expected_revision, reason)
            event = self._event(request, record.snapshot.audit)
            snapshot = replace(record.snapshot, audit=record.snapshot.audit + (event,))
            self._records[document_id] = _Record(owner, snapshot)
            return snapshot

    def assess_drafting(self, document_id: str, *, owner: str, expected_revision: int,
                        actor: str, context: str) -> DraftingAssessment:
        if type(expected_revision) is not int or expected_revision < 1:
            raise PriorArtError("STALE_DOSSIER_REVISION")
        with self._lock:
            record, _ = self._read(document_id, owner, actor, context,
                "ASSESS_DRAFTING", expected_revision)
            snapshot = record.snapshot
            search = review_documents(snapshot.content)["manual_search"]
            warnings = (UNVERIFIED_WARNING,)
            if search["status"] == "INCOMPLETE":
                warnings += (INCOMPLETE_WARNING,)
            decision = next((event for event in reversed(snapshot.audit)
                if event.request.dossier_revision == snapshot.dossier_revision
                and event.request.action in ("CONTINUE_DRAFT", "STOP_DRAFT")), None)
            allowed = decision is not None and decision.request.action == "CONTINUE_DRAFT"
            code = ("EXPLICIT_CONTINUATION" if allowed else
                    "HUMAN_STOPPED" if decision else "HUMAN_DECISION_REQUIRED")
            return DraftingAssessment(allowed, code, warnings, snapshot.source_sha256,
                snapshot.dossier_revision, snapshot.dossier_sha256,
                decision.sha256 if decision else None)
