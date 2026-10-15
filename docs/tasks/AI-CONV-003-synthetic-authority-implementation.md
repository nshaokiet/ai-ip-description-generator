# AI-CONV-003 — synthetic/offline Claims semantic authority implementation

## 1. Metadata and current status

| Field | Value |
|---|---|
| Task / issue | AI-CONV-003 / [#116](https://github.com/nshaokiet/ai-ip-description-generator/issues/116) |
| Implementation version | 0.1.0 candidate |
| Internal overlay version | 1.0.0 |
| Status | **IMPLEMENTED LOCALLY / TARGETED TESTS PASS — PR B REVIEW, CI AND INTEGRATION PENDING** |
| Baseline | `a14769123a5be426db2ba4b374f708a365f36f7b` (`origin/main` at branch creation) |
| Branch | `feat/ai-conv-003-synthetic-authority` |
| Human policy | [HD-01–HD-07 approved for limited offline/synthetic policy](https://github.com/nshaokiet/ai-ip-description-generator/issues/116#issuecomment-6187375281) |
| Separate implementation authority | Direct Human prompt, 15/10/2026; recorded by PR A as `HUMAN-AI-CONV-003-SYNTHETIC-IMPLEMENTATION-2026-10-15` |
| Workflow | V1; PR B is separate from policy synchronization PR A #118 |
| Required reviewer | Gemini 3.8 Flash High / Antigravity STRICT READ-ONLY on exact final SHA |

This is a non-production, non-authenticated prototype. It does not determine
patentability, authorize filing, or make output legally reliable. Any draft
Claim still requires Human and qualified IP review.

## 2. Architecture and released boundary

`backend/app/services/synthetic_claims_authority_v1.py` is an additive internal
module. It defines a deterministic overlay with:

- exact document ID and source SHA-256 binding;
- evidence snapshot IDs and canonical evidence digest;
- exact session, revision and revision-token binding;
- typed target/predicate/value assertions;
- dedicated `SYNTHETIC_REVIEWER_001` confirmation records;
- decision/assertion/overlay digests, revocation and supersession;
- preliminary method and composition candidate references;
- a fixed SYSTEM/APPARATUS-only family policy.

The overlay is not accepted by P2-002, P2-003, P2-004, P2-005, P2-006,
AI-CONV-002, any API route or frontend type. A positive SYSTEM/APPARATUS result
means only `ELIGIBLE_FOR_RELEASED_P2_004_VALIDATION`; it does not inject fields
into the released reconstruction and does not generate or package a Claim.

## 3. HD-01–HD-07 implementation matrix

| Decision | Implemented behavior | Test evidence |
|---|---|---|
| HD-01 | Explicit solution/element membership; source, evidence, session and revision bindings; nonexistent/cross-document/duplicate/inferred records reject | `test_hd01_*` |
| HD-02 | ESSENTIAL requires matching active Hybrid confirmation; UNKNOWN/OPTIONAL/CONDITIONAL remain non-essential; missing/conflicting/stale evidence fails closed | `test_hd02_*`, `test_hd06_*` |
| HD-03 | Versioned method/step membership, essentiality and relationship predicates; source sequence alone insufficient; cycles reject; METHOD/PROCESS positive family path fixed disabled | `test_hd03_*` |
| HD-04 | Versioned composition/material/amount/relationship predicates; co-mention, example and experimental amounts are non-mandatory; cross-composition splicing rejects; positive family fixed disabled | `test_hd04_*` |
| HD-05 | SYSTEM/APPARATUS may become eligible for further released P2-004 validation; unsupported and unknown families fail closed; policy object cannot enable disabled families | `test_hd05_*` |
| HD-06 | One allowlisted synthetic actor/role, immutable digest snapshot, revision/source/evidence/target binding, revocation, supersession, tamper/conflict/replay rejection | `test_hd06_*` |
| HD-07 | Additive overlay only; deterministic identity; exact original seven-input P2-005 signature asserted; released implementation hashes pinned | `test_hd07_*` |

## 4. Compatibility and provenance blocker

P2-005 reprojects P2-002 from the original APP-002 envelope and AI-001 analysis,
then validates the original seven inputs. An overlay-enriched reconstruction
would fail that projection check. Passing the overlay as an undeclared eighth
input, weakening reprojection, or treating its digest as source evidence would
bypass the released provenance contract and is prohibited.

The implemented safe path therefore remains independent. A future migration
proposal would require a separately Human-approved P2-005/P2-006 v2 contract
that explicitly names the new authority input, authenticates real actors,
retains all seven original inputs, pins all snapshots and adds migration plus
renderer/package regression tests. No part of that migration is implemented or
authorized here.

## 5. Tests and limitations

Targeted result on the current working tree:

```text
python -m pytest tests/backend/test_synthetic_claims_authority_v1.py -q -p no:cacheprovider
44 passed
```

Relevant P2-002…P2-006 plus AI-CONV-002 regression:

```text
python -m pytest tests/backend/test_invention_reconstruction.py tests/backend/test_uspto_specification_generation_v2.py tests/backend/test_supported_draft_claims_v1.py tests/backend/test_uspto_document_package_v1.py tests/backend/test_uspto_offline_renderer.py tests/backend/test_uspto_offline_orchestration.py tests/backend/test_synthetic_claims_authority_v1.py -q -p no:cacheprovider
412 passed
```

Full local regression with live-provider flags disabled:

```text
python -m pytest tests -q -p no:cacheprovider
1051 passed, 3 skipped, 1 existing Starlette/AnyIO deprecation warning
```

These are local results and are not GitHub CI, independent review or final
acceptance. Dependency/secret checks and exact-head CI remain required after
the implementation candidate is finalized.

Known limitations are intentional: actor identity is simulated; timestamps are
syntax-checked rather than backed by a trusted clock; storage is caller-owned
and ephemeral; no API/UI/database/authentication/provider integration exists;
no real/confidential document is accepted; no production audit guarantee is
claimed. METHOD/PROCESS and COMPOSITION positive authority remains disabled.

## 6. Handoff

```text
Task ID: AI-CONV-003
Agent: Codex implementation/integration session
Reviewer: Gemini 3.8 Flash High / Antigravity STRICT READ-ONLY required; pending
Status: IMPLEMENTED LOCALLY / TARGETED TESTS PASS — PR B REVIEW/CI PENDING
Version: implementation 0.1.0 candidate; overlay 1.0.0
Work completed: Additive authority overlay, Hybrid synthetic adapter, HD-01–HD-07 matrix and synthetic fixtures
Files affected: internal module, dedicated tests/fixtures, this task record, factual README status
Evidence checked: main a147691; Issue #116 Human policy; direct Human prompt; released P2-002…006 and AI-CONV-002 boundaries
Findings: Seven-input package contract cannot accept enriched authority without a separately approved versioned migration
Decisions: Independent prototype; SYSTEM/APPARATUS further-validation eligibility only; other positive families disabled
Issues: PR A #118 external review/CI/integration pending; PR B full regression, fixed-SHA review and CI pending
Security impact: Synthetic IDs only; safe errors; no source logging, credentials, provider, persistence, route, deployment or real data
Recommended next action: Complete local/full validation; commit/push PR B candidate; after PR A integration, rebase/finalize and request exact-SHA independent review
```

No merge, CI success, independent PASS, product Claims enablement or task
completion is claimed by this record.
