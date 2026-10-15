# AI-CONV-003 — synthetic/offline Claims semantic authority implementation

## 1. Metadata and current status

| Field | Value |
|---|---|
| Task / issue | AI-CONV-003 / [#116](https://github.com/nshaokiet/ai-ip-description-generator/issues/116) |
| Implementation version | 0.1.1 candidate |
| Internal overlay version | 1.0.0 |
| Status | **PR A MERGED / LOCAL FINAL CANDIDATE VALIDATED — PR B EXACT-HEAD CI + INDEPENDENT REVIEW PENDING** |
| Baseline | `a14769123a5be426db2ba4b374f708a365f36f7b` (`origin/main` at branch creation) |
| Integrated main | `3e651c050be26e71a23f15aac8f6272dc7c523de` (PR A #118 merge; exact-main CI #38729181713 SUCCESS) |
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

- exact document ID, source SHA-256 and reconstruction digest binding;
- exact configuration snapshot digest binding;
- evidence snapshot IDs and canonical evidence digest;
- exact session, revision and revision-token binding;
- typed target/predicate/value assertions;
- dedicated `SYNTHETIC_REVIEWER_001` confirmation records;
- decision/assertion/overlay digests, keyed decision seals, revocation and supersession;
- preliminary method and composition candidate references;
- a fixed SYSTEM/APPARATUS-only family policy.

The overlay is not accepted by P2-002, P2-003, P2-004, P2-005, P2-006,
AI-CONV-002, any API route or frontend type. A positive SYSTEM/APPARATUS result
means only `ELIGIBLE_FOR_RELEASED_P2_004_VALIDATION`; it does not inject fields
into the released reconstruction and does not generate or package a Claim.

## 3. HD-01–HD-07 implementation matrix

| Decision | Implemented behavior | Test evidence |
|---|---|---|
| HD-01 | Explicit solution/element membership; source, reconstruction/configuration, exact-target evidence, session and revision bindings; nonexistent/cross-document/duplicate/inferred records reject | `test_hd01_*` |
| HD-02 | ESSENTIAL requires matching active Hybrid confirmation; UNKNOWN/OPTIONAL/CONDITIONAL remain non-essential; missing/conflicting/stale evidence fails closed | `test_hd02_*`, `test_hd06_*` |
| HD-03 | Versioned method/step membership, essentiality and relationship predicates; source sequence alone insufficient; cycles reject; METHOD/PROCESS positive family path fixed disabled | `test_hd03_*` |
| HD-04 | Versioned composition/material/amount/relationship predicates; co-mention, example and experimental amounts are non-mandatory; cross-composition splicing rejects; positive family fixed disabled | `test_hd04_*` |
| HD-05 | SYSTEM/APPARATUS may become eligible for further released P2-004 validation; unsupported and unknown families fail closed; policy object cannot enable disabled families | `test_hd05_*` |
| HD-06 | One allowlisted synthetic actor/role, immutable reconstruction/configuration snapshot digests, keyed decision seal, revision/source/evidence/target binding, revocation, supersession, tamper/forgery/conflict/replay rejection | `test_hd06_*` |
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
49 passed
```

Relevant P2-002…P2-006 plus AI-CONV-002 regression:

```text
python -m pytest tests/backend/test_invention_reconstruction.py tests/backend/test_uspto_specification_generation_v2.py tests/backend/test_supported_draft_claims_v1.py tests/backend/test_uspto_document_package_v1.py tests/backend/test_uspto_offline_renderer.py tests/backend/test_uspto_offline_orchestration.py tests/backend/test_synthetic_claims_authority_v1.py -q -p no:cacheprovider
417 passed
```

Full local regression with live-provider flags disabled:

```text
python -m pytest tests -q -p no:cacheprovider
1056 passed, 3 skipped, 1 existing Starlette/AnyIO deprecation warning
```

The first full Windows run failed during `tmp_path` fixture setup before affected
test bodies executed: Pytest could not enumerate the predictable shared root
`%LOCALAPPDATA%\Temp\pytest-of-NguyenSongHaoKiet`. That directory had a protected
ACL, was owned by `WEKISS\CodexSandboxOffline`, and did not grant the executing
`WEKISS\NguyenSongHaoKiet` account access. A one-case default-Temp reproduction
failed at `_pytest.pathlib.find_prefixed` / `os.scandir(root)` with WinError 5.
No active Pytest process was found, and there is no evidence attributing the
failure to application code, a fixture defect, file locking, or antivirus.

The safe remediation used the task-owned, user-writable LocalAppData root
`%LOCALAPPDATA%\AI-IP-Generator\pytest-ai-conv-003-codex-20261015-001`, set
`TEMP`, `TMP`, and `TMPDIR` before starting Python, and gave every run a fresh
`--basetemp`. A create/read/modify/remove probe and the unchanged one-case
control passed there before the 49/417/1056 suites above. No ACL, security
control, test, or unrelated Temp directory was changed.

These are local results and are not GitHub CI, independent review or final
acceptance. `python -m pip check`, Python compile, `git diff --check`, the
Workflow V2 governance structural validator, a credential/private-key marker
scan and direct P2-005 signature inspection all passed. P2-005 still accepts
the original seven named inputs and returns the seven validated projections;
no authority overlay parameter exists. Fresh exact-head PR B CI remains
required after the final candidate is committed and pushed.

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
Status: PR A MERGED / LOCAL FINAL CANDIDATE VALIDATED — PR B REVIEW/CI PENDING
Version: implementation 0.1.1 candidate; overlay 1.0.0
Work completed: Additive authority overlay, Hybrid synthetic adapter, HD-01–HD-07 matrix, hardening for exact-target evidence/reconstruction/configuration binding and keyed decision seals, and synthetic fixtures
Files affected: internal module, dedicated tests/fixtures, this task record, README and Control Center factual status
Evidence checked: PR A reviewed 3e015f2 and merged 3e651c0; exact-main CI #38729181713 SUCCESS; Issue #116 Human policy; direct Human prompt; released P2-002…006 and AI-CONV-002 boundaries; reproduced default-Temp WinError 5 at Pytest fixture setup; isolated control PASS; local 49/417/1056 test results
Findings: Seven-input package contract cannot accept enriched authority without a separately approved versioned migration
Decisions: Independent prototype; SYSTEM/APPARATUS further-validation eligibility only; other positive families disabled
Issues: PR B final commit/push, exact-head CI and fixed-SHA independent review pending
Security impact: Synthetic IDs only; safe errors; no source logging, credentials, provider, persistence, route, deployment or real data
Recommended next action: Commit/push the final PR B candidate, verify exact-head CI, then request Gemini 3.8 Flash High / Antigravity STRICT READ-ONLY review on that exact SHA
```

No merge, CI success, independent PASS, product Claims enablement or task
completion is claimed by this record.
