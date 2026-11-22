"""Offline consent decisions for a trusted host; no routes, transport or identity service.

A decision is explanatory metadata, never a bearer token. The host must authenticate
actors, obtain actual Human consent, derive source/revision from custody, and check
the exact outgoing payload/destination immediately before any future transmission.
Existing provider paths are deliberately not wired here. State is process-local.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import re
from threading import RLock
from typing import Callable

from backend.app.services.custody_review import ReviewProjectionError, freeze_originals, review_documents
from backend.app.services.supported_draft_claims_validation import sha256_canonical

CLASSIFICATIONS = frozenset({"PUBLIC", "CONFIDENTIAL", "UNPUBLISHED"})
PURPOSES = frozenset({"SCIENTIFIC_ANALYSIS", "PRIOR_ART_SEARCH", "DRAFT_GENERATION",
                      "TRANSLATION", "FIGURE_PROCESSING"})
IDENTIFIER = re.compile(r"[A-Za-z0-9_-]{1,128}\Z")
DIGEST = re.compile(r"[a-f0-9]{64}\Z")


class ConsentError(ValueError):
    """Sanitized diagnostic: never include source, query, payload or credentials."""
    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


def _identifier(value: str) -> None:
    if type(value) is not str or IDENTIFIER.fullmatch(value) is None:
        raise ConsentError("INVALID_IDENTIFIER")


def _aware(value: datetime) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ConsentError("INVALID_TIME")
    return value.astimezone(timezone.utc)


def _payload_digest(payload: dict) -> str:
    if type(payload) is not dict:
        raise ConsentError("INVALID_PAYLOAD")
    try:
        snapshot = freeze_originals(payload)  # Reuse bounded immutable review snapshot.
        return sha256_canonical(review_documents(snapshot))
    except (ReviewProjectionError, ValueError, TypeError, RecursionError):
        raise ConsentError("INVALID_PAYLOAD") from None


@dataclass(frozen=True, slots=True)
class SourceRevision:
    document_id: str
    source_sha256: str
    revision: int

    def __post_init__(self) -> None:
        _identifier(self.document_id)
        if type(self.source_sha256) is not str or DIGEST.fullmatch(self.source_sha256) is None:
            raise ConsentError("INVALID_SOURCE_DIGEST")
        if type(self.revision) is not int or not 1 <= self.revision <= 2**53 - 1:
            raise ConsentError("INVALID_REVISION")


@dataclass(frozen=True, slots=True)
class ConsentAction:
    action: str
    source: SourceRevision
    owner: str
    actor: str
    context: str
    classification: str
    destination: str | None = None
    purpose: str | None = None
    payload_sha256: str | None = None
    expires_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class ConsentReceipt:
    request: ConsentAction
    recorded_at: datetime


@dataclass(frozen=True, slots=True)
class EgressDecision:
    allowed: bool
    code: str
    consent: ConsentReceipt | None = None


@dataclass(slots=True)
class _Record:
    source: SourceRevision
    owner: str
    classification: str
    classification_receipt: ConsentReceipt
    generation: int = 0
    grants: dict[tuple[str, str], ConsentReceipt] = field(default_factory=dict)


class OfflineConfidentialityGate:
    """Bounded local decision store. No authority callback means no consent writes.

    Callback receives the complete immutable requested action, including source,
    owner, payload hash, scope and expiry. A caller-supplied actor string or receipt
    alone does not grant authority. Public classification still requires consent.
    """
    def __init__(self, *, authorizer: Callable[[ConsentAction], bool] | None = None,
                 clock: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
                 max_records: int = 32, max_scopes: int = 16) -> None:
        if type(max_records) is not int or not 1 <= max_records <= 256:
            raise ConsentError("INVALID_CAPACITY")
        if type(max_scopes) is not int or not 1 <= max_scopes <= 64:
            raise ConsentError("INVALID_CAPACITY")
        self._authorizer, self._clock = authorizer, clock
        self._max_records, self._max_scopes = max_records, max_scopes
        self._records: dict[str, _Record] = {}
        self._lock = RLock()

    def _now(self) -> datetime:
        try:
            return _aware(self._clock())
        except Exception:
            raise ConsentError("CLOCK_UNAVAILABLE") from None

    def _authorize(self, request: ConsentAction) -> None:
        try:
            allowed = self._authorizer is not None and self._authorizer(request) is True
        except Exception:
            allowed = False
        if not allowed:
            raise ConsentError("AUTHORIZATION_REQUIRED")

    @staticmethod
    def _principal(owner: str, actor: str, context: str) -> None:
        for value in (owner, actor, context):
            _identifier(value)

    def _record(self, source: SourceRevision, owner: str) -> _Record:
        if type(source) is not SourceRevision:
            raise ConsentError("INVALID_SOURCE")
        _identifier(owner)
        record = self._records.get(source.document_id)
        if record is None:
            raise ConsentError("CLASSIFICATION_REQUIRED")
        if record.owner != owner:
            raise ConsentError("OWNER_MISMATCH")
        if record.source != source:
            raise ConsentError("STALE_SOURCE_REVISION")
        return record

    @staticmethod
    def _scope(destination: str, purpose: str) -> None:
        _identifier(destination)  # Opaque host-registered destination, never a URL to fetch.
        if type(purpose) is not str or purpose not in PURPOSES:
            raise ConsentError("INVALID_PURPOSE")

    def classify(self, source: SourceRevision, *, owner: str, classification: str,
                 actor: str, context: str) -> ConsentReceipt:
        if type(source) is not SourceRevision:
            raise ConsentError("INVALID_SOURCE")
        self._principal(owner, actor, context)
        if type(classification) is not str or classification not in CLASSIFICATIONS:
            raise ConsentError("INVALID_CLASSIFICATION")
        request = ConsentAction("CLASSIFY", source, owner, actor, context, classification)
        with self._lock:
            previous = self._records.get(source.document_id)
            generation = previous.generation if previous is not None else None
            if previous is not None:
                if previous.owner != owner:
                    raise ConsentError("OWNER_MISMATCH")
                if source.revision < previous.source.revision:
                    raise ConsentError("STALE_SOURCE_REVISION")
                if source.revision == previous.source.revision and source != previous.source:
                    raise ConsentError("SOURCE_REVISION_CONFLICT")
            elif len(self._records) >= self._max_records:
                raise ConsentError("CAPACITY_REACHED")
            self._authorize(request)
            if (self._records.get(source.document_id) is not previous
                    or (previous is not None and previous.generation != generation)):
                raise ConsentError("STALE_SOURCE_REVISION")
            if previous is None and len(self._records) >= self._max_records:
                raise ConsentError("CAPACITY_REACHED")
            receipt = ConsentReceipt(request, self._now())
            self._records[source.document_id] = _Record(source, owner, classification, receipt)
            return receipt  # Reclassification always invalidates all prior grants.

    def grant(self, source: SourceRevision, payload: dict, *, owner: str,
              destination: str, purpose: str, actor: str, context: str,
              expires_at: datetime) -> ConsentReceipt:
        self._principal(owner, actor, context)
        self._scope(destination, purpose)
        digest = _payload_digest(payload)
        expiry = _aware(expires_at)
        with self._lock:
            record = self._record(source, owner)
            generation = record.generation
            now = self._now()
            if expiry <= now:
                raise ConsentError("CONSENT_EXPIRED")
            key = (destination, purpose)
            if key not in record.grants and len(record.grants) >= self._max_scopes:
                raise ConsentError("CAPACITY_REACHED")
            request = ConsentAction("ALLOW_EGRESS", source, owner, actor, context,
                                    record.classification, destination, purpose, digest, expiry)
            self._authorize(request)
            if (self._records.get(source.document_id) is not record
                    or record.generation != generation):
                raise ConsentError("STALE_SOURCE_REVISION")
            now = self._now()
            if expiry <= now:
                raise ConsentError("CONSENT_EXPIRED")
            receipt = ConsentReceipt(request, now)
            record.grants[key] = receipt
            record.generation += 1
            return receipt

    def revoke(self, source: SourceRevision, *, owner: str, actor: str,
               context: str) -> ConsentReceipt:
        self._principal(owner, actor, context)
        with self._lock:
            record = self._record(source, owner)
            generation = record.generation
            request = ConsentAction("REVOKE_EGRESS", source, owner, actor, context,
                                    record.classification)
            self._authorize(request)
            if (self._records.get(source.document_id) is not record
                    or record.generation != generation):
                raise ConsentError("STALE_SOURCE_REVISION")
            receipt = ConsentReceipt(request, self._now())
            record.grants.clear()
            record.generation += 1
            return receipt

    def check(self, source: SourceRevision, payload: dict, *, owner: str,
              destination: str, purpose: str) -> EgressDecision:
        """Check actual payload; exceptions, missing state and expired consent deny.

        Does not perform egress, authenticate the host, persist state, or activate
        any existing provider route. Host integration needs separate review.
        """
        try:
            self._scope(destination, purpose)
            digest = _payload_digest(payload)
            with self._lock:
                record = self._record(source, owner)
                receipt = record.grants.get((destination, purpose))
                if receipt is None:
                    return EgressDecision(False, "CONSENT_REQUIRED")
                if receipt.request.payload_sha256 != digest:
                    return EgressDecision(False, "PAYLOAD_CHANGED")
                if receipt.request.expires_at <= self._now():
                    return EgressDecision(False, "CONSENT_EXPIRED")
                return EgressDecision(True, "EXPLICIT_CONSENT", receipt)
        except ConsentError as exc:
            return EgressDecision(False, exc.code)
