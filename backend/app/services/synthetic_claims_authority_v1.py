"""Versioned synthetic/offline Claims semantic-authority prototype.

This module is an internal overlay.  It does not mutate or extend any released
P2-002 through P2-006 contract, authenticate a real person, or authorize a
production Claim.  A positive result means only that a synthetic SYSTEM or
APPARATUS candidate may proceed to the existing P2-004 validation surface.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime
import hashlib
import hmac
import json
from typing import Any, Iterable, Mapping


OVERLAY_SCHEMA_VERSION = "1.0.0"
OVERLAY_TYPE = "SYNTHETIC_CLAIMS_SEMANTIC_AUTHORITY"
SUPPORTED_POSITIVE_FAMILIES = ("SYSTEM", "APPARATUS")
DISABLED_POSITIVE_FAMILIES = ("METHOD", "PROCESS", "COMPOSITION")
ALL_FAMILIES = (*SUPPORTED_POSITIVE_FAMILIES, *DISABLED_POSITIVE_FAMILIES)
SYNTHETIC_ACTORS = {
    "SYNTHETIC_REVIEWER_001": "SYNTHETIC_HUMAN_REVIEWER",
}

_NOTICE = {
    "synthetic_only": True,
    "authenticated_identity": False,
    "production_authority": False,
    "legal_authority": False,
}
_FAMILY_POLICY = {
    "eligible_for_further_validation": list(SUPPORTED_POSITIVE_FAMILIES),
    "positive_authority_disabled": list(DISABLED_POSITIVE_FAMILIES),
    "released_p2_004_modified": False,
}
_PREDICATE_VALUES = {
    "SOLUTION_MEMBERSHIP": {"MEMBER", "NOT_MEMBER", "UNKNOWN"},
    "ELEMENT_ESSENTIALITY": {"ESSENTIAL", "OPTIONAL", "CONDITIONAL", "UNKNOWN"},
    "METHOD_STEP_MEMBERSHIP": {"MEMBER", "NOT_MEMBER", "UNKNOWN"},
    "METHOD_STEP_ESSENTIALITY": {"ESSENTIAL", "OPTIONAL", "CONDITIONAL", "UNKNOWN"},
    "METHOD_STEP_RELATIONSHIP": {"ORDER_REQUIRED", "RELATED", "UNKNOWN"},
    "COMPOSITION_MEMBERSHIP": {"MEMBER", "NOT_MEMBER", "UNKNOWN"},
    "COMPOSITION_AMOUNT_MANDATORY": {"MANDATORY", "EXAMPLE", "EXPERIMENTAL", "UNKNOWN"},
    "COMPOSITION_MATERIAL_RELATIONSHIP": {"MANDATORY", "OPTIONAL", "UNKNOWN"},
}
_TARGET_KEYS = {
    "SOLUTION_MEMBERSHIP": {"solution_id", "element_id"},
    "ELEMENT_ESSENTIALITY": {"solution_id", "element_id"},
    "METHOD_STEP_MEMBERSHIP": {"method_id", "step_id"},
    "METHOD_STEP_ESSENTIALITY": {"method_id", "step_id"},
    "METHOD_STEP_RELATIONSHIP": {"method_id", "subject_step_id", "object_step_id"},
    "COMPOSITION_MEMBERSHIP": {"composition_id", "material_id"},
    "COMPOSITION_AMOUNT_MANDATORY": {"composition_id", "material_id", "amount_id"},
    "COMPOSITION_MATERIAL_RELATIONSHIP": {
        "composition_id", "subject_material_id", "object_material_id"
    },
}
_BINDING_KEYS = {
    "document_id", "source_sha256", "reconstruction_digest",
    "configuration_digest", "session_id", "revision", "revision_token",
}


class SyntheticAuthorityError(ValueError):
    """Stable source-safe diagnostic for the internal prototype."""

    safe_message = "Synthetic Claims authority validation failed."

    def __init__(self, code: str, *, paths: tuple[str, ...] = ()) -> None:
        self.code = code
        self.paths = tuple(sorted(set(paths)))
        super().__init__(self.safe_message)


@dataclass(frozen=True)
class AuthorityContext:
    document_id: str
    source_sha256: str
    reconstruction_digest: str
    configuration_digest: str
    evidence_records: Mapping[str, Any]
    solution_ids: frozenset[str]
    element_ids: frozenset[str]
    source_method_step_ids: frozenset[str]
    solution_evidence_ids: Mapping[str, frozenset[str]]
    element_evidence_ids: Mapping[str, frozenset[str]]
    method_step_evidence_ids: Mapping[str, frozenset[str]]
    session_id: str
    revision: int
    revision_token: str
    synthetic_authority_key: bytes = field(repr=False)


@dataclass(frozen=True)
class AuthorityEligibility:
    eligible: bool
    family: str
    code: str
    assertion_ids: tuple[str, ...] = ()
    positive_claims_enabled: bool = False


def canonical_json(value: Any) -> str:
    try:
        return json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
    except (TypeError, ValueError):
        raise SyntheticAuthorityError("CANONICALIZATION_FAILED") from None


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def context_from_reconstruction(
    reconstruction: Any,
    *,
    configuration_snapshot: Mapping[str, Any],
    session_id: str,
    revision: int,
    revision_token: str,
    synthetic_authority_key: bytes,
) -> AuthorityContext:
    """Create an immutable validation context without assigning membership."""
    try:
        metadata = reconstruction["document_metadata"]
        model = reconstruction["invention_model"]
        evidence = reconstruction["review_package"]["evidence"]
        evidence_records = {item["evidence_id"]: deepcopy(item) for item in evidence}
        if len(evidence_records) != len(evidence):
            raise KeyError
        context = AuthorityContext(
            document_id=metadata["document_id"],
            source_sha256=metadata["sha256"],
            reconstruction_digest=canonical_digest(reconstruction),
            configuration_digest=canonical_digest(configuration_snapshot),
            evidence_records=evidence_records,
            solution_ids=frozenset(x["solution_id"] for x in model["solution_concepts"]),
            element_ids=frozenset(x["element_id"] for x in model["elements"]),
            source_method_step_ids=frozenset(x["step_id"] for x in model["method_steps"]),
            solution_evidence_ids=_entity_evidence_map(
                model["solution_concepts"], "solution_id"
            ),
            element_evidence_ids=_entity_evidence_map(model["elements"], "element_id"),
            method_step_evidence_ids=_entity_evidence_map(
                model["method_steps"], "step_id"
            ),
            session_id=session_id,
            revision=revision,
            revision_token=revision_token,
            synthetic_authority_key=synthetic_authority_key,
        )
    except (KeyError, TypeError):
        raise SyntheticAuthorityError("INVALID_CONTEXT") from None
    _validate_context(context)
    return context


def evidence_digest(context: AuthorityContext, evidence_ids: Iterable[str]) -> str:
    ids = _evidence_ids(evidence_ids)
    missing = [item for item in ids if item not in context.evidence_records]
    if missing:
        raise SyntheticAuthorityError("EVIDENCE_NOT_FOUND", paths=("/evidence_ids",))
    return canonical_digest([[item, context.evidence_records[item]] for item in ids])


def make_synthetic_decision(
    context: AuthorityContext,
    *,
    decision_id: str,
    predicate: str,
    target: Mapping[str, str],
    value: str,
    evidence_ids: Iterable[str],
    timestamp: str,
    actor_id: str = "SYNTHETIC_REVIEWER_001",
    actor_role: str = "SYNTHETIC_HUMAN_REVIEWER",
    action: str = "CONFIRM",
    subject_decision_id: str | None = None,
    supersedes_decision_id: str | None = None,
) -> dict[str, Any]:
    """Build a digest-bound simulated decision; this is not authentication."""
    ids = _evidence_ids(evidence_ids)
    decision = {
        "decision_id": decision_id,
        "action": action,
        "actor_id": actor_id,
        "actor_role": actor_role,
        "timestamp": timestamp,
        **_binding(context),
        "predicate": predicate,
        "target": dict(target),
        "value": value,
        "evidence_ids": ids,
        "evidence_digest": evidence_digest(context, ids),
        "subject_decision_id": subject_decision_id,
        "supersedes_decision_id": supersedes_decision_id,
    }
    decision["decision_digest"] = canonical_digest(decision)
    decision["decision_seal"] = _decision_seal(
        context, decision["decision_digest"]
    )
    return decision


def make_authority_assertion(
    context: AuthorityContext,
    *,
    assertion_id: str,
    predicate: str,
    target: Mapping[str, str],
    value: str,
    evidence_ids: Iterable[str],
    authority_decision_id: str,
) -> dict[str, Any]:
    ids = _evidence_ids(evidence_ids)
    assertion = {
        "assertion_id": assertion_id,
        **_binding(context),
        "predicate": predicate,
        "target": dict(target),
        "value": value,
        "grounding": "SOURCE_EXPLICIT",
        "evidence_ids": ids,
        "evidence_digest": evidence_digest(context, ids),
        "authority_decision_id": authority_decision_id,
    }
    assertion["assertion_digest"] = canonical_digest(assertion)
    return assertion


def make_overlay(
    context: AuthorityContext,
    *,
    decisions: Iterable[Mapping[str, Any]],
    assertions: Iterable[Mapping[str, Any]],
    candidate_methods: Iterable[Mapping[str, Any]] = (),
    candidate_compositions: Iterable[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    overlay = {
        "schema_version": OVERLAY_SCHEMA_VERSION,
        "overlay_type": OVERLAY_TYPE,
        "notice": deepcopy(_NOTICE),
        "document_binding": {
            "document_id": context.document_id,
            "source_sha256": context.source_sha256,
            "reconstruction_digest": context.reconstruction_digest,
        },
        "configuration_binding": {
            "configuration_digest": context.configuration_digest,
        },
        "session_binding": {
            "session_id": context.session_id,
            "revision": context.revision,
            "revision_token": context.revision_token,
        },
        "family_policy": deepcopy(_FAMILY_POLICY),
        "candidate_methods": [deepcopy(dict(item)) for item in candidate_methods],
        "candidate_compositions": [deepcopy(dict(item)) for item in candidate_compositions],
        "decisions": [deepcopy(dict(item)) for item in decisions],
        "assertions": [deepcopy(dict(item)) for item in assertions],
    }
    overlay["overlay_digest"] = canonical_digest(overlay)
    return overlay


def validate_overlay(overlay: Any, context: AuthorityContext) -> dict[str, Any]:
    _validate_context(context)
    required = {
        "schema_version", "overlay_type", "notice", "document_binding",
        "configuration_binding", "session_binding", "family_policy", "candidate_methods",
        "candidate_compositions", "decisions", "assertions", "overlay_digest",
    }
    if type(overlay) is not dict or set(overlay) != required:
        raise SyntheticAuthorityError("INVALID_OVERLAY", paths=("/overlay",))
    if overlay["schema_version"] != OVERLAY_SCHEMA_VERSION or overlay["overlay_type"] != OVERLAY_TYPE:
        raise SyntheticAuthorityError("VERSION_UNSUPPORTED", paths=("/schema_version",))
    if overlay["notice"] != _NOTICE or overlay["family_policy"] != _FAMILY_POLICY:
        raise SyntheticAuthorityError("FAMILY_POLICY_INVALID", paths=("/family_policy", "/notice"))
    _validate_overlay_binding(overlay, context)
    unsigned = {key: deepcopy(value) for key, value in overlay.items() if key != "overlay_digest"}
    if overlay["overlay_digest"] != canonical_digest(unsigned):
        raise SyntheticAuthorityError("OVERLAY_TAMPERED", paths=("/overlay_digest",))

    methods = _validate_method_candidates(overlay["candidate_methods"], context)
    compositions = _validate_composition_candidates(overlay["candidate_compositions"])
    decisions, active_decisions = _validate_decisions(overlay["decisions"], context, methods, compositions)
    assertions = _validate_assertions(
        overlay["assertions"], context, methods, compositions, decisions, active_decisions
    )
    _validate_method_relationships(assertions)
    return deepcopy(overlay)


def evaluate_family_authority(
    overlay: Any,
    context: AuthorityContext,
    *,
    family: str,
    solution_id: str,
    required_element_ids: Iterable[str],
) -> AuthorityEligibility:
    validated = validate_overlay(overlay, context)
    if family not in ALL_FAMILIES:
        raise SyntheticAuthorityError("CLAIM_FAMILY_UNKNOWN", paths=("/family",))
    if family in DISABLED_POSITIVE_FAMILIES:
        return AuthorityEligibility(False, family, "CLAIM_FAMILY_DISABLED")
    elements = tuple(dict.fromkeys(required_element_ids))
    if not elements or any(item not in context.element_ids for item in elements):
        return AuthorityEligibility(False, family, "REQUIRED_ELEMENT_INVALID")
    if solution_id not in context.solution_ids:
        return AuthorityEligibility(False, family, "SOLUTION_NOT_FOUND")

    index = {
        (item["predicate"], _target_key(item["target"])): item
        for item in validated["assertions"]
    }
    used: list[str] = []
    for element_id in elements:
        target = _target_key({"solution_id": solution_id, "element_id": element_id})
        membership = index.get(("SOLUTION_MEMBERSHIP", target))
        essentiality = index.get(("ELEMENT_ESSENTIALITY", target))
        if membership is None or membership["value"] != "MEMBER":
            return AuthorityEligibility(False, family, "SOLUTION_MEMBERSHIP_UNRESOLVED")
        if essentiality is None or essentiality["value"] != "ESSENTIAL":
            return AuthorityEligibility(False, family, "ELEMENT_ESSENTIALITY_UNRESOLVED")
        used.extend((membership["assertion_id"], essentiality["assertion_id"]))
    return AuthorityEligibility(
        True,
        family,
        "ELIGIBLE_FOR_RELEASED_P2_004_VALIDATION",
        tuple(used),
        False,
    )


def inspect_preliminary_method(
    overlay: Any, context: AuthorityContext, *, method_id: str
) -> AuthorityEligibility:
    validated = validate_overlay(overlay, context)
    candidate = next((x for x in validated["candidate_methods"] if x["method_id"] == method_id), None)
    if candidate is None:
        return AuthorityEligibility(False, "METHOD", "METHOD_NOT_FOUND")
    assertions = validated["assertions"]
    for step_id in candidate["step_ids"]:
        scoped = [
            item
            for item in assertions
            if item["target"].get("method_id") == method_id
            and item["target"].get("step_id") == step_id
        ]
        if not any(x["predicate"] == "METHOD_STEP_MEMBERSHIP" and x["value"] == "MEMBER" for x in scoped):
            return AuthorityEligibility(False, "METHOD", "METHOD_MEMBERSHIP_UNRESOLVED")
        if not any(x["predicate"] == "METHOD_STEP_ESSENTIALITY" and x["value"] == "ESSENTIAL" for x in scoped):
            return AuthorityEligibility(False, "METHOD", "METHOD_ESSENTIALITY_UNRESOLVED")
    return AuthorityEligibility(False, "METHOD", "METHOD_POSITIVE_AUTHORITY_DISABLED")


def inspect_preliminary_composition(
    overlay: Any, context: AuthorityContext, *, composition_id: str
) -> AuthorityEligibility:
    validated = validate_overlay(overlay, context)
    candidate = next((x for x in validated["candidate_compositions"] if x["composition_id"] == composition_id), None)
    if candidate is None:
        return AuthorityEligibility(False, "COMPOSITION", "COMPOSITION_NOT_FOUND")
    assertions = validated["assertions"]
    for material in candidate["materials"]:
        scoped = [
            item
            for item in assertions
            if item["target"].get("composition_id") == composition_id
            and item["target"].get("material_id") == material["material_id"]
        ]
        if not any(x["predicate"] == "COMPOSITION_MEMBERSHIP" and x["value"] == "MEMBER" for x in scoped):
            return AuthorityEligibility(False, "COMPOSITION", "COMPOSITION_MEMBERSHIP_UNRESOLVED")
        for amount_id in material["amount_ids"]:
            if not any(
                x["predicate"] == "COMPOSITION_AMOUNT_MANDATORY"
                and x["target"].get("amount_id") == amount_id
                and x["value"] == "MANDATORY"
                for x in scoped
            ):
                return AuthorityEligibility(False, "COMPOSITION", "COMPOSITION_AMOUNT_UNRESOLVED")
    return AuthorityEligibility(False, "COMPOSITION", "COMPOSITION_POSITIVE_AUTHORITY_DISABLED")


def _binding(context: AuthorityContext) -> dict[str, Any]:
    return {
        "document_id": context.document_id,
        "source_sha256": context.source_sha256,
        "reconstruction_digest": context.reconstruction_digest,
        "configuration_digest": context.configuration_digest,
        "session_id": context.session_id,
        "revision": context.revision,
        "revision_token": context.revision_token,
    }


def _validate_context(context: AuthorityContext) -> None:
    if (
        not context.document_id
        or not _valid_sha256(context.source_sha256)
        or not _valid_sha256(context.reconstruction_digest)
        or not _valid_sha256(context.configuration_digest)
        or not context.evidence_records
        or not context.session_id
        or type(context.revision) is not int
        or context.revision < 1
        or not context.revision_token
        or type(context.synthetic_authority_key) is not bytes
        or len(context.synthetic_authority_key) < 32
    ):
        raise SyntheticAuthorityError("INVALID_CONTEXT")
    for evidence_id, record in context.evidence_records.items():
        if (
            type(evidence_id) is not str
            or not evidence_id
            or type(record) is not dict
            or record.get("evidence_id") != evidence_id
            or record.get("document_id") != context.document_id
        ):
            raise SyntheticAuthorityError("INVALID_CONTEXT")
    expected_maps = (
        (context.solution_ids, context.solution_evidence_ids),
        (context.element_ids, context.element_evidence_ids),
        (context.source_method_step_ids, context.method_step_evidence_ids),
    )
    for entity_ids, support_map in expected_maps:
        if set(support_map) != set(entity_ids):
            raise SyntheticAuthorityError("INVALID_CONTEXT")
        for evidence_ids in support_map.values():
            if (
                type(evidence_ids) is not frozenset
                or not evidence_ids
                or not evidence_ids.issubset(context.evidence_records)
            ):
                raise SyntheticAuthorityError("INVALID_CONTEXT")


def _evidence_ids(values: Iterable[str]) -> list[str]:
    if type(values) in {str, bytes}:
        raise SyntheticAuthorityError("EVIDENCE_REQUIRED", paths=("/evidence_ids",))
    try:
        ids = sorted(values)
    except TypeError:
        raise SyntheticAuthorityError("EVIDENCE_REQUIRED", paths=("/evidence_ids",)) from None
    if not ids or any(type(item) is not str or not item for item in ids) or len(ids) != len(set(ids)):
        raise SyntheticAuthorityError("EVIDENCE_REQUIRED", paths=("/evidence_ids",))
    return ids


def _validate_overlay_binding(overlay: dict[str, Any], context: AuthorityContext) -> None:
    expected_document = {
        "document_id": context.document_id,
        "source_sha256": context.source_sha256,
        "reconstruction_digest": context.reconstruction_digest,
    }
    expected_configuration = {
        "configuration_digest": context.configuration_digest,
    }
    expected_session = {
        "session_id": context.session_id,
        "revision": context.revision,
        "revision_token": context.revision_token,
    }
    if overlay["document_binding"].get("document_id") != context.document_id:
        raise SyntheticAuthorityError("DOCUMENT_MISMATCH", paths=("/document_binding/document_id",))
    if overlay["document_binding"].get("source_sha256") != context.source_sha256:
        raise SyntheticAuthorityError("SOURCE_HASH_MISMATCH", paths=("/document_binding/source_sha256",))
    if overlay["document_binding"].get("reconstruction_digest") != context.reconstruction_digest:
        raise SyntheticAuthorityError(
            "RECONSTRUCTION_MISMATCH",
            paths=("/document_binding/reconstruction_digest",),
        )
    if overlay["document_binding"] != expected_document:
        raise SyntheticAuthorityError("INVALID_OVERLAY", paths=("/document_binding",))
    if overlay["configuration_binding"] != expected_configuration:
        raise SyntheticAuthorityError(
            "CONFIGURATION_MISMATCH",
            paths=("/configuration_binding",),
        )
    if overlay["session_binding"].get("session_id") != context.session_id:
        raise SyntheticAuthorityError("SESSION_MISMATCH", paths=("/session_binding/session_id",))
    if overlay["session_binding"] != expected_session:
        raise SyntheticAuthorityError("STALE_REVISION", paths=("/session_binding",))


def _validate_method_candidates(values: Any, context: AuthorityContext) -> dict[str, set[str]]:
    if type(values) is not list:
        raise SyntheticAuthorityError("INVALID_OVERLAY", paths=("/candidate_methods",))
    result: dict[str, set[str]] = {}
    for index, item in enumerate(values):
        path = f"/candidate_methods/{index}"
        if type(item) is not dict or set(item) != {"method_id", "step_ids"}:
            raise SyntheticAuthorityError("CANDIDATE_INVALID", paths=(path,))
        method_id, step_ids = item["method_id"], item["step_ids"]
        if type(method_id) is not str or not method_id or method_id in result:
            raise SyntheticAuthorityError("CANDIDATE_DUPLICATE", paths=(path,))
        if type(step_ids) is not list or not step_ids or len(step_ids) != len(set(step_ids)):
            raise SyntheticAuthorityError("CANDIDATE_INVALID", paths=(path,))
        if any(step not in context.source_method_step_ids for step in step_ids):
            raise SyntheticAuthorityError("CANDIDATE_REFERENCE_INVALID", paths=(path,))
        result[method_id] = set(step_ids)
    return result


def _validate_composition_candidates(values: Any) -> dict[str, dict[str, set[str]]]:
    if type(values) is not list:
        raise SyntheticAuthorityError("INVALID_OVERLAY", paths=("/candidate_compositions",))
    result: dict[str, dict[str, set[str]]] = {}
    for index, item in enumerate(values):
        path = f"/candidate_compositions/{index}"
        if type(item) is not dict or set(item) != {"composition_id", "materials"}:
            raise SyntheticAuthorityError("CANDIDATE_INVALID", paths=(path,))
        composition_id, materials = item["composition_id"], item["materials"]
        if type(composition_id) is not str or not composition_id or composition_id in result:
            raise SyntheticAuthorityError("CANDIDATE_DUPLICATE", paths=(path,))
        if type(materials) is not list or not materials:
            raise SyntheticAuthorityError("CANDIDATE_INVALID", paths=(path,))
        mapped: dict[str, set[str]] = {}
        for material in materials:
            if type(material) is not dict or set(material) != {"material_id", "amount_ids"}:
                raise SyntheticAuthorityError("CANDIDATE_INVALID", paths=(path,))
            material_id, amount_ids = material["material_id"], material["amount_ids"]
            if type(material_id) is not str or not material_id or material_id in mapped:
                raise SyntheticAuthorityError("CANDIDATE_DUPLICATE", paths=(path,))
            if (
                type(amount_ids) is not list
                or len(amount_ids) != len(set(amount_ids))
                or any(type(value) is not str or not value for value in amount_ids)
            ):
                raise SyntheticAuthorityError("CANDIDATE_INVALID", paths=(path,))
            mapped[material_id] = set(amount_ids)
        result[composition_id] = mapped
    return result


def _validate_decisions(
    values: Any,
    context: AuthorityContext,
    methods: Mapping[str, set[str]],
    compositions: Mapping[str, Mapping[str, set[str]]],
) -> tuple[dict[str, dict[str, Any]], set[str]]:
    if type(values) is not list:
        raise SyntheticAuthorityError("INVALID_OVERLAY", paths=("/decisions",))
    result: dict[str, dict[str, Any]] = {}
    active: set[str] = set()
    active_targets: dict[tuple[str, str], str] = {}
    for index, decision in enumerate(values):
        path = f"/decisions/{index}"
        expected = {
            "decision_id", "action", "actor_id", "actor_role", "timestamp",
            *_BINDING_KEYS, "predicate", "target", "value", "evidence_ids",
            "evidence_digest", "subject_decision_id", "supersedes_decision_id",
            "decision_digest", "decision_seal",
        }
        if type(decision) is not dict or set(decision) != expected:
            raise SyntheticAuthorityError("DECISION_INVALID", paths=(path,))
        decision_id = decision["decision_id"]
        if type(decision_id) is not str or not decision_id or decision_id in result:
            raise SyntheticAuthorityError("DECISION_DUPLICATE", paths=(path,))
        _validate_record_binding(decision, context, path)
        _validate_actor(decision, path)
        decision_timestamp = _validate_timestamp(decision["timestamp"], path)
        _validate_semantics(decision, context, methods, compositions, path)
        _validate_evidence_binding(decision, context, path)
        unsigned = {
            key: deepcopy(value)
            for key, value in decision.items()
            if key not in {"decision_digest", "decision_seal"}
        }
        if decision["decision_digest"] != canonical_digest(unsigned):
            raise SyntheticAuthorityError("DECISION_TAMPERED", paths=(path + "/decision_digest",))
        expected_seal = _decision_seal(context, decision["decision_digest"])
        if (
            type(decision["decision_seal"]) is not str
            or not hmac.compare_digest(decision["decision_seal"], expected_seal)
        ):
            raise SyntheticAuthorityError(
                "DECISION_FORGED", paths=(path + "/decision_seal",)
            )
        key = (decision["predicate"], _target_key(decision["target"]))
        if decision["action"] == "CONFIRM":
            if decision["subject_decision_id"] is not None:
                raise SyntheticAuthorityError("DECISION_ACTION_INVALID", paths=(path,))
            prior_id = decision["supersedes_decision_id"]
            if prior_id is not None:
                prior = result.get(prior_id)
                if (
                    prior is None
                    or prior_id not in active
                    or (prior["predicate"], _target_key(prior["target"])) != key
                ):
                    raise SyntheticAuthorityError("DECISION_SUBJECT_INVALID", paths=(path,))
                if decision_timestamp <= _validate_timestamp(prior["timestamp"], path):
                    raise SyntheticAuthorityError("DECISION_TIMESTAMP_INVALID", paths=(path,))
                active.remove(prior_id)
            elif key in active_targets:
                prior = result[active_targets[key]]
                code = "DECISION_DUPLICATE" if prior["value"] == decision["value"] else "DECISION_CONFLICT"
                raise SyntheticAuthorityError(code, paths=(path,))
            active.add(decision_id)
            active_targets[key] = decision_id
        elif decision["action"] == "REVOKE":
            subject_id = decision["subject_decision_id"]
            subject = result.get(subject_id)
            if (
                decision["supersedes_decision_id"] is not None
                or subject is None
                or subject_id not in active
                or subject["predicate"] != decision["predicate"]
                or subject["target"] != decision["target"]
                or subject["value"] != decision["value"]
                or subject["evidence_ids"] != decision["evidence_ids"]
                or subject["evidence_digest"] != decision["evidence_digest"]
            ):
                raise SyntheticAuthorityError("DECISION_SUBJECT_INVALID", paths=(path,))
            if decision_timestamp <= _validate_timestamp(subject["timestamp"], path):
                raise SyntheticAuthorityError("DECISION_TIMESTAMP_INVALID", paths=(path,))
            active.remove(subject_id)
            active_targets.pop(key, None)
        else:
            raise SyntheticAuthorityError("DECISION_ACTION_INVALID", paths=(path + "/action",))
        result[decision_id] = deepcopy(decision)
    return result, active


def _validate_assertions(
    values: Any,
    context: AuthorityContext,
    methods: Mapping[str, set[str]],
    compositions: Mapping[str, Mapping[str, set[str]]],
    decisions: Mapping[str, Mapping[str, Any]],
    active_decisions: set[str],
) -> list[dict[str, Any]]:
    if type(values) is not list:
        raise SyntheticAuthorityError("INVALID_OVERLAY", paths=("/assertions",))
    ids: set[str] = set()
    targets: dict[tuple[str, str], str] = {}
    result: list[dict[str, Any]] = []
    expected = {
        "assertion_id", *_BINDING_KEYS, "predicate", "target", "value",
        "grounding", "evidence_ids", "evidence_digest", "authority_decision_id",
        "assertion_digest",
    }
    for index, assertion in enumerate(values):
        path = f"/assertions/{index}"
        if type(assertion) is not dict or set(assertion) != expected:
            raise SyntheticAuthorityError("ASSERTION_INVALID", paths=(path,))
        assertion_id = assertion["assertion_id"]
        if type(assertion_id) is not str or not assertion_id or assertion_id in ids:
            raise SyntheticAuthorityError("ASSERTION_DUPLICATE", paths=(path,))
        ids.add(assertion_id)
        _validate_record_binding(assertion, context, path)
        _validate_semantics(assertion, context, methods, compositions, path)
        _validate_evidence_binding(assertion, context, path)
        if assertion["grounding"] != "SOURCE_EXPLICIT":
            raise SyntheticAuthorityError("INFERRED_AUTHORITY_UNSUPPORTED", paths=(path + "/grounding",))
        unsigned = {key: deepcopy(value) for key, value in assertion.items() if key != "assertion_digest"}
        if assertion["assertion_digest"] != canonical_digest(unsigned):
            raise SyntheticAuthorityError("ASSERTION_TAMPERED", paths=(path + "/assertion_digest",))
        target_key = (assertion["predicate"], _target_key(assertion["target"]))
        if target_key in targets:
            code = "ASSERTION_DUPLICATE" if targets[target_key] == assertion["value"] else "ASSERTION_CONFLICT"
            raise SyntheticAuthorityError(code, paths=(path,))
        targets[target_key] = assertion["value"]
        decision_id = assertion["authority_decision_id"]
        decision = decisions.get(decision_id)
        if decision is None:
            raise SyntheticAuthorityError("CONFIRMATION_REQUIRED", paths=(path + "/authority_decision_id",))
        if decision_id not in active_decisions:
            raise SyntheticAuthorityError("CONFIRMATION_INACTIVE", paths=(path + "/authority_decision_id",))
        matching = (
            decision["predicate"] == assertion["predicate"]
            and decision["target"] == assertion["target"]
            and decision["value"] == assertion["value"]
            and decision["evidence_ids"] == assertion["evidence_ids"]
            and decision["evidence_digest"] == assertion["evidence_digest"]
        )
        if not matching:
            raise SyntheticAuthorityError("CONFIRMATION_MISMATCH", paths=(path,))
        result.append(deepcopy(assertion))
    return result


def _validate_actor(record: Mapping[str, Any], path: str) -> None:
    expected_role = SYNTHETIC_ACTORS.get(record["actor_id"])
    if expected_role is None or record["actor_role"] != expected_role:
        raise SyntheticAuthorityError("ACTOR_INVALID", paths=(path + "/actor_id",))


def _validate_timestamp(value: Any, path: str) -> datetime:
    if type(value) is not str or not value.endswith("Z"):
        raise SyntheticAuthorityError("DECISION_TIMESTAMP_INVALID", paths=(path + "/timestamp",))
    try:
        return datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        raise SyntheticAuthorityError("DECISION_TIMESTAMP_INVALID", paths=(path + "/timestamp",)) from None


def _validate_record_binding(record: Mapping[str, Any], context: AuthorityContext, path: str) -> None:
    if record["document_id"] != context.document_id:
        raise SyntheticAuthorityError("DOCUMENT_MISMATCH", paths=(path + "/document_id",))
    if record["source_sha256"] != context.source_sha256:
        raise SyntheticAuthorityError("SOURCE_HASH_MISMATCH", paths=(path + "/source_sha256",))
    if record["reconstruction_digest"] != context.reconstruction_digest:
        raise SyntheticAuthorityError(
            "RECONSTRUCTION_MISMATCH",
            paths=(path + "/reconstruction_digest",),
        )
    if record["configuration_digest"] != context.configuration_digest:
        raise SyntheticAuthorityError(
            "CONFIGURATION_MISMATCH",
            paths=(path + "/configuration_digest",),
        )
    if record["session_id"] != context.session_id:
        raise SyntheticAuthorityError("SESSION_MISMATCH", paths=(path + "/session_id",))
    if record["revision"] != context.revision or record["revision_token"] != context.revision_token:
        raise SyntheticAuthorityError("STALE_REVISION", paths=(path,))


def _validate_evidence_binding(record: Mapping[str, Any], context: AuthorityContext, path: str) -> None:
    ids = _evidence_ids(record["evidence_ids"])
    if ids != record["evidence_ids"]:
        raise SyntheticAuthorityError("EVIDENCE_REQUIRED", paths=(path + "/evidence_ids",))
    expected = evidence_digest(context, ids)
    if record["evidence_digest"] != expected:
        raise SyntheticAuthorityError("EVIDENCE_CHANGED", paths=(path + "/evidence_digest",))


def _validate_semantics(
    record: Mapping[str, Any],
    context: AuthorityContext,
    methods: Mapping[str, set[str]],
    compositions: Mapping[str, Mapping[str, set[str]]],
    path: str,
) -> None:
    predicate = record["predicate"]
    target = record["target"]
    if predicate not in _PREDICATE_VALUES or record["value"] not in _PREDICATE_VALUES[predicate]:
        raise SyntheticAuthorityError("PREDICATE_UNSUPPORTED", paths=(path + "/predicate",))
    if (
        type(target) is not dict
        or set(target) != _TARGET_KEYS[predicate]
        or any(type(value) is not str or not value for value in target.values())
    ):
        raise SyntheticAuthorityError("TARGET_INVALID", paths=(path + "/target",))
    if predicate.startswith("SOLUTION_") or predicate == "ELEMENT_ESSENTIALITY":
        if (
            target["solution_id"] not in context.solution_ids
            or target["element_id"] not in context.element_ids
        ):
            raise SyntheticAuthorityError("ENTITY_NOT_FOUND", paths=(path + "/target",))
        _validate_structural_evidence(record, context, path)
        return
    if predicate.startswith("METHOD_"):
        steps = methods.get(target["method_id"])
        used = {value for key, value in target.items() if key.endswith("step_id")}
        step_fields = [key for key in target if key.endswith("step_id")]
        if steps is None or not used.issubset(steps) or len(used) != len(step_fields):
            raise SyntheticAuthorityError("CANDIDATE_REFERENCE_INVALID", paths=(path + "/target",))
        return
    materials = compositions.get(target["composition_id"])
    if materials is None:
        raise SyntheticAuthorityError("COMPOSITION_SPLICE", paths=(path + "/target",))
    used_materials = {value for key, value in target.items() if "material_id" in key}
    if not used_materials.issubset(materials):
        raise SyntheticAuthorityError("COMPOSITION_SPLICE", paths=(path + "/target",))
    if "amount_id" in target and target["amount_id"] not in materials[target["material_id"]]:
        raise SyntheticAuthorityError("COMPOSITION_SPLICE", paths=(path + "/target",))


def _validate_method_relationships(assertions: Iterable[Mapping[str, Any]]) -> None:
    graphs: dict[str, dict[str, set[str]]] = {}
    for assertion in assertions:
        if assertion["predicate"] != "METHOD_STEP_RELATIONSHIP" or assertion["value"] != "ORDER_REQUIRED":
            continue
        target = assertion["target"]
        graph = graphs.setdefault(target["method_id"], {})
        graph.setdefault(target["subject_step_id"], set()).add(target["object_step_id"])
    for graph in graphs.values():
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(node: str) -> None:
            if node in visiting:
                raise SyntheticAuthorityError("METHOD_RELATIONSHIP_CONFLICT", paths=("/assertions",))
            if node in visited:
                return
            visiting.add(node)
            for child in graph.get(node, set()):
                visit(child)
            visiting.remove(node)
            visited.add(node)

        for node in graph:
            visit(node)


def _target_key(target: Mapping[str, str]) -> str:
    return canonical_json(dict(target))


def _valid_sha256(value: Any) -> bool:
    return (
        type(value) is str
        and len(value) == 64
        and all(char in "0123456789abcdef" for char in value)
    )


def _entity_evidence_map(
    entities: Iterable[Mapping[str, Any]], identifier: str
) -> dict[str, frozenset[str]]:
    result: dict[str, frozenset[str]] = {}
    for entity in entities:
        entity_id = entity[identifier]
        evidence_ids = entity["support"]["evidence_ids"]
        if entity_id in result or type(evidence_ids) is not list:
            raise KeyError
        result[entity_id] = frozenset(evidence_ids)
    return result


def _validate_structural_evidence(
    record: Mapping[str, Any], context: AuthorityContext, path: str
) -> None:
    target = record["target"]
    evidence_ids = set(record["evidence_ids"])
    solution_ids = context.solution_evidence_ids[target["solution_id"]]
    element_ids = context.element_evidence_ids[target["element_id"]]
    permitted = solution_ids | element_ids
    if (
        not evidence_ids.issubset(permitted)
        or not evidence_ids.intersection(solution_ids)
        or not evidence_ids.intersection(element_ids)
    ):
        raise SyntheticAuthorityError(
            "TARGET_EVIDENCE_MISMATCH", paths=(path + "/evidence_ids",)
        )


def _decision_seal(context: AuthorityContext, decision_digest: str) -> str:
    return hmac.new(
        context.synthetic_authority_key,
        decision_digest.encode("ascii"),
        hashlib.sha256,
    ).hexdigest()
