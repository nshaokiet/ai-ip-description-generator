"""Local, deterministic validation of a session-edited canonical draft."""

from __future__ import annotations

import json
import hashlib
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from jsonschema import ValidationError

from backend.app.services.draft_business_validation import (
    DraftBusinessValidationError,
    validate_draft_business_rules,
)
from backend.app.services.extraction_runtime import CANONICAL_SCHEMA_PATH
from backend.app.services.extraction_validation import (
    ExtractionValidationError,
    validate_canonical_output,
)
from backend.app.services.patent_docx_renderer import validate_payload


class EditedDraftValidationError(ValueError):
    def __init__(self, code: str, message: str, *, paths: tuple[str, ...] = ()) -> None:
        super().__init__(message)
        self.code = code
        self.safe_message = message
        self.paths = paths


def draft_digest(draft: dict[str, Any], revision_id: str) -> str:
    serialized = json.dumps(
        {"revision_id": revision_id, "draft": draft},
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    )
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _pointer(parts: tuple[str | int, ...]) -> str:
    return "/" + "/".join(str(part).replace("~", "~0").replace("/", "~1") for part in parts) if parts else "/"


def _different_paths(left: Any, right: Any, parts: tuple[str | int, ...] = ()) -> set[str]:
    if isinstance(left, dict) and isinstance(right, dict):
        paths: set[str] = set()
        for key in left.keys() | right.keys():
            if key not in left or key not in right:
                paths.add(_pointer((*parts, key)))
            else:
                paths.update(_different_paths(left[key], right[key], (*parts, key)))
        return paths
    if isinstance(left, list) and isinstance(right, list):
        if len(left) != len(right):
            return {_pointer(parts)}
        paths = set()
        for index, (old, new) in enumerate(zip(left, right)):
            paths.update(_different_paths(old, new, (*parts, index)))
        return paths
    return {_pointer(parts)} if left != right else set()


def _editable_paths(draft: Mapping[str, Any]) -> set[str]:
    paths: set[str] = set()
    if draft["abstract"]["status"] == "PRESENT":
        paths.update({"/abstract/text", "/abstract/word_count"})
    for section_index, section in enumerate(draft["draft_sections"]):
        if section["status"] != "PRESENT":
            continue
        prefix = f"/draft_sections/{section_index}"
        paths.update(
            f"{prefix}/paragraphs/{index}/text"
            for index, _ in enumerate(section["paragraphs"])
        )
        for subsection_index, subsection in enumerate(section["subsections"]):
            if subsection["status"] == "PRESENT":
                paths.update(
                    f"{prefix}/subsections/{subsection_index}/paragraphs/{index}/text"
                    for index, _ in enumerate(subsection["paragraphs"])
                )
    return paths


def _validate_one(
    draft: dict[str, Any],
    analysis: dict[str, Any],
    selected_title_candidate_id: str | None,
) -> None:
    try:
        validate_payload(draft)
    except ValidationError as exc:
        raise EditedDraftValidationError(
            "invalid_patent_draft",
            "The patent draft does not match the canonical schema.",
            paths=(_pointer(tuple(exc.absolute_path)),),
        ) from exc
    try:
        validate_draft_business_rules(
            draft, analysis, selected_title_candidate_id=selected_title_candidate_id
        )
    except DraftBusinessValidationError as exc:
        raise EditedDraftValidationError(
            "invalid_draft_grounding",
            "The patent draft failed source-linked validation.",
            paths=exc.paths,
        ) from exc


def validate_edited_draft(
    *,
    analysis: dict[str, Any],
    original_draft: dict[str, Any],
    draft: dict[str, Any],
    selected_title_candidate_id: str | None,
) -> tuple[str, ...]:
    """Validate both payloads and return edited prose paths needing Human support review.

    Deterministic rules prove reference integrity, not semantic entailment of new prose.
    Callers must surface the returned paths as unverified, never as newly grounded.
    """
    try:
        schema = json.loads(Path(CANONICAL_SCHEMA_PATH).read_text(encoding="utf-8"))
        validate_canonical_output(analysis, schema)
    except ExtractionValidationError as exc:
        raise EditedDraftValidationError(
            "invalid_source_analysis",
            "The source analysis does not match the canonical schema.",
            paths=exc.paths,
        ) from exc
    _validate_one(original_draft, analysis, selected_title_candidate_id)
    _validate_one(draft, analysis, selected_title_candidate_id)
    differences = _different_paths(original_draft, draft)
    protected = sorted(differences - _editable_paths(original_draft))
    if protected:
        raise EditedDraftValidationError(
            "protected_draft_field_changed",
            "Only existing present abstract and paragraph prose may be edited.",
            paths=tuple(protected[:10]),
        )
    return tuple(sorted(path for path in differences if path.endswith("/text")))
