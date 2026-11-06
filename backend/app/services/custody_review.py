"""Bounded immutable review snapshots; no transport or authorization by possession."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from typing import Any


class ReviewProjectionError(RuntimeError):
    def __init__(self) -> None:
        super().__init__("Complete synthetic review data is unavailable within review limits.")


@dataclass(frozen=True, slots=True)
class FrozenObject:
    members: tuple[tuple[str, Any], ...]


@dataclass(frozen=True, slots=True)
class FrozenArray:
    values: tuple[Any, ...]


def freeze_originals(originals: dict[str, Any]) -> FrozenObject:
    """Check limits before copying. Never truncate a source or draft for approval."""
    nodes = 0

    def check(value: Any, depth: int = 0) -> None:
        nonlocal nodes
        nodes += 1
        if nodes > 100_000 or depth > 64:
            raise ReviewProjectionError()
        if type(value) is str:
            if len(value) > 1_048_576 or len(value.encode("utf-8")) > 1_048_576:
                raise ReviewProjectionError()
        elif type(value) is dict:
            for key, child in value.items():
                if type(key) is not str:
                    raise ReviewProjectionError()
                check(key, depth + 1)
                check(child, depth + 1)
        elif type(value) is list:
            for child in value:
                check(child, depth + 1)
        elif value is None or type(value) in (bool, int):
            return
        elif type(value) is float and math.isfinite(value):
            return
        else:
            raise ReviewProjectionError()

    check(originals)
    total = 0
    for chunk in json.JSONEncoder(ensure_ascii=False, allow_nan=False).iterencode(originals):
        total += len(chunk.encode("utf-8"))
        if total > 8 * 1_048_576:
            raise ReviewProjectionError()

    def freeze(value: Any) -> Any:
        if type(value) is dict:
            return FrozenObject(tuple((key, freeze(child)) for key, child in value.items()))
        if type(value) is list:
            return FrozenArray(tuple(freeze(child) for child in value))
        return value

    return freeze(originals)


def review_documents(value: FrozenObject | FrozenArray | Any) -> Any:
    """Return a detached JSON copy for a trusted presenter, without losing fields."""
    if isinstance(value, FrozenObject):
        return {key: review_documents(child) for key, child in value.members}
    if isinstance(value, FrozenArray):
        return [review_documents(child) for child in value.values]
    return value


@dataclass(frozen=True, slots=True)
class C1ReviewProjection:
    projection_version: str
    coordinator_instance_id: str
    custody_id: str
    document_id: str
    revision: int
    state: str
    source_sha256: str
    originals_sha256: tuple[tuple[str, str], ...]
    originals: FrozenObject
    claims_review_required: bool
    review_snapshot_sha256: str
    render_policy_baseline: str
    synthetic_draft: bool = True
    filing_ready: bool = False


@dataclass(frozen=True, slots=True)
class C1ReviewTarget:
    coordinator_instance_id: str
    custody_id: str
    document_id: str
    owner: str
    revision: int
    revision_token_sha256: str
    review_snapshot_sha256: str
    actor: str
    context: str
    decision: str
