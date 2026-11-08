# PREAPI-C2 REVISION-004 — post-PR155 specification-only recovery

| Field | Verified or bounded value |
|---|---|
| Task | PREAPI-C2-REVISION-004 / DOCS-RECOVERY-POST155 |
| Version / date | 1.0.0 / 2026-11-08 |
| Authority | Original Human Option A — Internal Synthetic Adapter First, **SPECIFICATION ONLY** (24/10/2026); continuation limited to conflict-safe documentation reconciliation |
| Accepted base | `main` `27c24f70ac1fe528e04cb2a8d59e94e8cc34f346`, tree `03bae455968afc39ce4205120346a0eac76cfccf` |
| Historical source | PR146 `29daeb208f7736a448297f699e674192c124c7da`, tree `d1f8880dad44363db4f612d76b9d709435f6089c` |
| Status | DRAFT RECOVERY / NEW FINAL-SHA REVIEW + REQUIRED PR CI PENDING / NO MERGE |

## Purpose and scope

This candidate transfers the explicitly authorized C2 REVISION-004 specification into the accepted post-PR155 documentation baseline without changing or force-pushing original PR146. The product remains the **Next.js + FastAPI website**. This recovery is NOT a C2 implementation task, new website contract approval, or PRODUCT-001B specification freeze.

Canonical [specification](PREAPI-001-C2-synthetic-adapter-contract.md), [Human authority record](../decisions/PREAPI-C2-REVISION-004-architecture-authorization.md), [historical fixed-SHA handoff](../review-handoff/PREAPI-C2-REVISION-004-fixed-sha-review.md), [historical correction receipt](../review-receipts/PREAPI-C2-REVISION-004-REVIEW-RECEIPT-CORRECTION.md) and [SHA256SUMS](../review-receipts/PREAPI-C2-REVISION-004-SHA256SUMS.txt) are included **as unchanged original Git blobs**. Old handoff SHA remains historical and must not be read as the new candidate's review.

The three common documents (README, Control Center and Review Log) derive from the currently integrated main and add a separately dated C2 status. Older B/A/CI and reviewer history is preserved. The complete changed-file inventory, exact new commit/tree and CI results belong in the post-commit Draft PR receipt.

## Exact source artifacts, immutable hashes

| Original from PR146 | Git blob | Historical SHA256, if available |
|---|---|---|
| `docs/decisions/PREAPI-C2-REVISION-004-architecture-authorization.md` | `37d1408332e3ec17ce4da3545b65cca33ba544f4` | Human authority; independently read original; no derived approval |
| `docs/review-handoff/PREAPI-C2-REVISION-004-fixed-sha-review.md` | `b4004ba171a70093ce4b9263dc6339ed1302eb04` | Historical old-SHA request only |
| `docs/review-receipts/PREAPI-C2-REVISION-004-REVIEW-RECEIPT-CORRECTION.md` | `9ed18277716c7ab71d398b1cb836982a9d7712db` | `bb0e666ff38fbbd44891e947383a1e90eb2d2df5369827baed796639500d5e80` (4993B) |
| `docs/review-receipts/PREAPI-C2-REVISION-004-SHA256SUMS.txt` | `ab308fc4324124d52a6371489fe7720fdc685b05` | Manifest preserved, no self-hash |
| `docs/tasks/PREAPI-001-C2-synthetic-adapter-contract.md` | `4d7cf5aa8016c2fd79b1f6529ed28e6eec257c11` | `1e2f5376f526e7e3176c8731deb2d49dccf1ef1de7b347643a60d4b011f8ce3f` (80892B) |

Historical external Gemini3.8 Flash High / Antigravity STRICT READ-ONLY report on old HEAD: 22626 bytes, SHA256 `a4377a60bc326771f7801898e2cd238d097ee2c43693a5da817430ba5767622f`, source-attested reviewer provenance with reused session, **PASS for SPECIFICATION only**. F01–F09 resolved in design; T01–T80 are **80 proposed unique test identities and NOT RUN**. Approved C2 fixtures **0**.

## Evidence and unresolved gates

| Gate | Status |
|---|---|
| Historical PR146 | OPEN/DRAFT/dirty vs current main; no rebase/reset/merge/force-push |
| Historical PR146 CI40078806412 | FAILURE at stale audit 1HIGH+1CRITICAL and storage quota; never retroactive SUCCESS |
| Accepted main | Post-155 push CI42449793664 SUCCESS; DEP-001 security13605153288, audits0 and security73+2PASS; applies only to accepted main |
| New spec-only candidate | Required main-target pull_request CI + mandatory downloaded security ZIP + fresh exact-final-SHA independent reviewer **PENDING** until actually run/reviewed |
| PRODUCT-001B | Documentation PR155 merged, WEB-0010.1.1 still NOT FROZEN; D01–D07/BF03/BF05 remain Human PENDING |
| C2 | Specification only, no approved fixtures; active C2 code, provider, Claims, pilot or deployment NOT AUTHORIZED |

**Independent review instructions:** Verify actual Gemini3.8 Flash High / Antigravity STRICT READ-ONLY model/session/reuse/independence. Review complete new changed-file diff, original five preserved Git blobs, Human authorization, inherited current main history, 80 test identities proposed/not run, and scope/semantic compatibility of C2 with original B0.1.1 without silently modifying either contract. Return security/quality/spec-only PASS/REQUEST CHANGES/BLOCKED on the **new final SHA**. This task does not authorize runtime security/fixture approvals.

## Safe execution / stopping conditions

- No C2 executable code/tests, A/C1 hooks, B1–B6, public browser/HTTPS/session/IPC, schema/API breaking change, fixture admission, new dependency/security gate, paid provider/real paper, deployment or local SQLite state.
- Do not edit original canonical specification/receipt/manifest/historical handoff bytes. Changes to these require a new reviewed/versioned explicit decision, not cleanup.
- No new Human architecture/production decision inferred from this documentation merge candidate.
- No automatic main merge even if review and CI later PASS; require explicit Human decision at an exact immutable HEAD.
- If the actual new diff changes an unapproved contract or leaks private data, report BLOCKED and do not merge.

**Resume:** `RESUME-AIIP-PREAPI-C2-POST155-SPEC-RECOVERY`.
