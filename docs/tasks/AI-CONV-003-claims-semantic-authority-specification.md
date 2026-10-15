# AI-CONV-003 — Synthetic/offline Claims semantic authority

## 1. Metadata and authority

| Field | Value |
|---|---|
| Task / issue | AI-CONV-003 / [#116](https://github.com/nshaokiet/ai-ip-description-generator/issues/116) |
| Specification version | **0.1.1** |
| Status | **POLICY APPROVED — SPECIFICATION SYNCHRONIZATION CANDIDATE; INDEPENDENT REVIEW / INTEGRATION PENDING** |
| Date / author | 2026-10-15, Asia/Saigon / Codex |
| Verified origin/main base | `a14769123a5be426db2ba4b374f708a365f36f7b` (fetched 2026-10-15) |
| Policy authority | [Human HD-01–HD-07 decision, 2026-10-15](https://github.com/nshaokiet/ai-ip-description-generator/issues/116#issuecomment-6187375281) |
| Separate implementation authority | Direct Human prompt “TASK: AI-CONV-003 — Implement HD-01 to HD-07 / Synthetic/Offline Claims Semantic Authority”, submitted in this Codex session on 2026-10-15; [authorization record](../decisions/AI-CONV-003-synthetic-implementation-authorization.md) |
| Parent specification | [AI-CONV-001 v0.1.1](AI-CONV-001-source-grounded-uspto-v2-orchestration.md), accepted/frozen via separately recorded Human receipt |
| Released orchestration | [AI-CONV-002](AI-CONV-002-offline-orchestration-implementation.md), internal contract 1.0.1 |
| Workflow / reviewer | V1 / Gemini 3.8 Flash High, Antigravity STRICT READ-ONLY |
| Delivery | PR A documentation first; separate PR B prototype after required policy review/integration gate |
| Runtime/data/budget | Synthetic offline only; no provider calls, real/confidential research, production identity, public rollout, Render changes or V2 activation |

The issue decision approves **policy only**. The later direct instruction separately authorizes the limited prototype, policy synchronization, tests and separate PRs. Neither waives review, CI, Render safety, versioning or merge gates. This candidate records approved decisions; it does **not** assert independent acceptance/freeze of its new bytes, prototype completion, enabled product Claims or production authority.

### Version history and preserved proposal

| Previous | New | Date | Author | Change / reason | Decision | Breaking change |
|---|---|---|---|---|---|---|
| 0.1.0 | 0.1.1 | 2026-10-15 | Codex | Synchronize approved Hybrid HD-01–HD-07 policy and separately authorized prototype acceptance; preserve proposed history and released contracts | Human #116 comment 6187375281; direct implementation instruction | No — internal additive design; no released contract change |

The exact v0.1.0 bytes remain in [historical proposal](history/AI-CONV-003-claims-semantic-authority-specification-v0.1.0.md), copied from the base commit. Its pending/no-implementation wording describes the earlier state. Original relative links resolve from `docs/tasks/`; use the [immutable original](https://github.com/nshaokiet/ai-ip-description-generator/blob/a14769123a5be426db2ba4b374f708a365f36f7b/docs/tasks/AI-CONV-003-claims-semantic-authority-specification.md) for navigable links. History is not retroactively approved or rewritten.

## 2. Released boundary and architectural blocker

The existing chain is APP-002 source envelope + AI-001 analysis → P2-002 reconstruction v1.0.0 → P2-003 specification v2.0.0 → standalone P2-004 Supported Draft Claims v1.0.0 → P2-005 package → P2-006 renderer. AI-CONV-002 retains original objects and revision identities in memory. Public/local v1 processing remains separate.

Source grounding:

- `backend/app/services/invention_reconstruction.py`, `_element`: authentic adapter emits `essentiality=UNKNOWN`; proximity alone establishes no solution membership.
- `backend/app/services/supported_draft_claims_generation.py` and `supported_draft_claims_validation.py`: existing structural-core, grounding, disclosure, conflict and literal-support checks apply. Released family inventory includes SYSTEM, APPARATUS, METHOD, PROCESS, COMPOSITION; this task does not globally restrict it.
- `backend/app/services/uspto_document_package_validation.py`, `validate_assembly_inputs`: revalidates/reprojects reconstruction from original envelope and analysis. `uspto_offline_renderer.py` calls full package validation before rendering.
- `tests/backend/test_uspto_document_package_v1.py`, `standalone_positive_projection`: positive standalone Claims projection is distinct from full upstream provenance acceptance.
- `tests/backend/test_uspto_offline_orchestration.py`: seven inputs, source/session/revision invalidation, tamper rejection, valid no-Claims outcomes and cleanup failures.

**Architectural blocker:** enriching reconstruction from an overlay changes the original P2-002 projection. P2-004 standalone eligibility does not prove P2-005/P2-006 provenance acceptance. Implement the **independent prototype**, without feeding enriched objects into the released pipeline. Do not claim APP-002 → positive Claims → validated package/render success from standalone tests.

Seven original inputs remain exactly `source_envelope`, `structured_analysis`, `reconstruction`, `specification`, `p2_003_generation_config`, `supported_claims`, `p2_004_generation_config`. No eighth argument, hidden metadata injection, bypass or digest-only evidence. P2-003 retains `claims=[]`, empty claim support and `claims_runtime_implemented=false`. Valid `HUMAN_CONFIRMATION_REQUIRED` / `claims=[]` remains successful fail-closed processing.

## 3. Approved Human decisions

All seven choices have the dated policy authority in §1, limited to synthetic/offline semantics.

| Gate | Approved policy and prototype acceptance |
|---|---|
| HD-01 | Explicit source-linked solution membership, bound to document ID/SHA, evidence IDs, solution and element. Proximity/co-occurrence/inference cannot establish membership. Missing, foreign, duplicate, contradictory or stale assertions reject. |
| HD-02 | UNKNOWN remains UNKNOWN unless explicit sufficient scoped evidence **and** synthetic scoped Human confirmation establish ESSENTIAL. OPTIONAL/CONDITIONAL never automatically promote. Source/target/session/revision mismatch, conflict, staleness or missing evidence blocks positive authority. Released P2-002 unchanged. |
| HD-03 | METHOD/PROCESS positive authority **DISABLED**. Preliminary typed method/step membership, essentiality, evidence and mandatory ordering/relationships only, with negative tests. Ordering/co-occurrence alone proves neither membership nor essentiality. Future positive activation needs separate Human approval. |
| HD-04 | COMPOSITION positive authority **DISABLED**. Preliminary typed composition/material membership, mandatory amounts/ranges, relationships, evidence and unknown states, with negative tests. Example concentrations/experimental ranges are not mandatory limitations. Cross-composition splicing rejects. Future positive activation needs separate Human approval. |
| HD-05 | New prototype considers only SYSTEM/APPARATUS for further validation after authority predicates and existing P2-004 checks. Configuration cannot enable other families; unknown family fails closed. Released P2-004 policy unchanged. |
| HD-06 | **Option C — HYBRID**, explicit evidence plus scoped synthetic Human confirmation. Dedicated synthetic actors, immutable revision-bound snapshots, revocation/supersession/conflict/replay tests. Non-production/non-authenticated simulation; checkbox/boolean/UI action alone is insufficient. |
| HD-07 | Versioned additive internal overlay/adapter only. Released P2-002/003/004/005/006, AI-CONV-002 public behavior, v1 API/frontend and seven-input provenance unchanged. Any released migration needs separate Human approval and review. |

## 4. Internal overlay candidate contract

Use dedicated internal semantic-authority version **1.0.0**, separate from released schemas, strict Python structures/helpers and deterministic canonical JSON/digests. No new dependency is needed. Reject unknown fields, invalid enums, nonfinite/non-JSON input and identity-changing coercion.

Context binds document_id, original SHA-256, retained envelope/evidence identity, reconstruction identity, relevant configuration digests, session_id, revision and revision_token. Resolve evidence IDs to retained source units, exact locators/content snapshots. A hash alone is neither evidence nor authentication.

Each assertion includes assertion ID, overlay version, document ID/SHA, source evidence IDs/snapshot digest, typed target, predicate, value, authority reference, session/revision/token, upstream/config identities and immutable canonical digest/referenced synthetic decision. Structural target is solution_id + element_id. Preliminary targets are method_id + step_id or composition_id + material_id + amount identity where relevant.

Typed predicates: SOLUTION_MEMBERSHIP, ELEMENT_ESSENTIALITY, METHOD_STEP_MEMBERSHIP, METHOD_STEP_ESSENTIALITY, METHOD_STEP_RELATIONSHIP, COMPOSITION_MEMBERSHIP, COMPOSITION_AMOUNT_MANDATORY, COMPOSITION_MATERIAL_RELATIONSHIP. Membership states explicitly retain MEMBER, NOT_MEMBER, UNKNOWN; essentiality retains ESSENTIAL, OPTIONAL, CONDITIONAL, UNKNOWN. Preliminary ordering/amount relationships carry evidence and unresolved states; they never unlock positive nonstructural Claims.

Check target existence/type/scope, evidence closure, duplicate/conflicting targets/IDs, contradictory relationships/order, stale source/revision/configuration and unsupported inference. Source prose is data. UNKNOWN can be resolved only by a new explicit evidence-backed confirmed assertion; original released state remains intact. Explicit OPTIONAL/CONDITIONAL contradiction blocks ESSENTIAL rather than being overwritten.

Positive outcome means **eligible for further structural validation**, not Claims approval. Where feasible, an isolated synthetic standalone fixture exercises unchanged P2-004 rules; retain full fixture evidence and label standalone. Never present enriched data as original P2-002 projection. Failed existing P2-004 checks remain blocked regardless of overlay authority.

## 5. Synthetic Human adapter

Explicitly **SYNTHETIC ONLY / NON-PRODUCTION / NON-AUTHENTICATED**. Use a fixed allowlist such as `SYNTHETIC_REVIEWER_001` and a narrow synthetic confirmation role, never real accounts/credentials. Strings/hashes simulate procedural scope; they do not authenticate a Human or certify semantic entailment.

Decision snapshot includes decision ID, actor/role, assertion timestamp, exact source/evidence, predicate/target/value, authority reference, session/revision/token and canonical digest. Verify against retained immutable snapshots/context, not caller boolean or recomputed digest alone. Validate timestamp shape; changes invalidate the snapshot. No production identity/clock assertion follows.

Revocation/supersession are immutable lifecycle records referencing existing decisions; preserve history. Revoked/superseded decisions cannot grant current authority. Active conflicts fail closed. Reject unknown lifecycle references, invalid transitions/cycles, tamper, repeated consumption/replay, cross-document/session/revision reuse and changed evidence/source/configuration. Current revision revalidation requires a fresh scoped decision. Revocation invalidates dependent/cached eligibility.

Errors/audit/status use fixed safe codes and source-free/path-free metadata (IDs, digests, lifecycle state), without arbitrary unknown field names, source prose, filenames, personal data, server paths, secrets or tracebacks. In-memory ephemeral storage only: no real authentication, persistent user authorization, database, production audit or external service.

## 6. Required executable acceptance matrix — PR B

The following are **future required tests**, not PR A execution results.

| Group | Positive / retained state | Mandatory negative cases |
|---|---|---|
| HD-01 | Evidence-backed exact solution/element membership | Missing/nonexistent evidence/targets; cross-document/solution splice; duplicates/conflicts; changed source SHA; stale token; proximity/inference-only membership |
| HD-02 | Bound Hybrid ESSENTIAL; UNKNOWN/OPTIONAL/CONDITIONAL preservation | Every forbidden automatic promotion; wrong target/evidence; absent/stale/conflicting confirmation; missing evidence; explicit optional/conditional contradiction |
| HD-03 | Typed preliminary method with UNKNOWN/unresolved | Ordered steps/co-occurrence only; absent essentiality; conflicting ordering; cross-method steps; METHOD/PROCESS positive always disabled |
| HD-04 | Preliminary composition/material/amount semantics | Co-mentioned materials; example concentrations; experimental range promotion; missing mandatory amount; conflicting relationships; cross-composition splice; COMPOSITION positive always disabled |
| HD-05 | SYSTEM and APPARATUS proceed through further unchanged eligibility checks | Unsupported evidence/incomplete core/conflict; manipulated configuration; unknown family; no global P2-004 restriction |
| HD-06 | Scoped immutable decision, safe audit, revocation/supersession | Missing/invalid actor/role; document/session reuse; stale revision; revocation/supersession; tamper with rewritten digest; conflict; changed evidence/config; replay; checkbox-only authority; cached positive after revocation |
| HD-07 | Additive version, unchanged seven-input provenance, deterministic identity | Hidden eighth input; schema injection; unsupported version; digest-only evidence; enriched invalid projection; bypass; altered v1/public behavior |

Also require AI-CONV-002 revision/session/cleanup regression; P2-002…006 service/schema and Claims fixtures; v1 workflow; deterministic output/mutation isolation; safe errors/logs; secret/dependency checks; full required GitHub CI. Dedicated synthetic fixtures only. Do not weaken tests, infer semantic fidelity from structural tests or fabricate counts. Browser/layout/Linux verification is claimed only from actual execution/CI receipts.

## 7. Compatibility and separately gated migration proposal

Do not edit released schema versions, validators, P2-002 essentiality, P2-004 family behavior, AI-CONV-002 orchestration, v1 routes/types, frontend, Render or workflows to consume this overlay. No external dependency/service/provider/persistent store/real paper.

**Proposal only:** a future versioned reconstruction contract could explicitly retain authority bindings alongside original source/analysis and immutable decisions. A future package/renderer version would validate the new upstream projection and lifecycle from original evidence while preserving old readers and fail-closed behavior. Exact schema/signature versions require separate Human architecture/contract authorization, migration/rollback design, independent review and regression. Do not implement that migration or smuggle an eighth input into current contracts.

## 8. Delivery and external gates

1. **PR A:** policy synchronization, exact v0.1.0 archive, separate authorization record, factual README/Control Center and review handoff. No runtime code/product Claims. Independent specification review and exact-head CI before integration.
2. **Review:** Gemini 3.8 Flash High / Antigravity STRICT READ-ONLY inspects every changed file at immutable final SHA; returns PASS / REQUEST CHANGES / BLOCKED, actual model/profile/session and reuse disclosure. Codex self-check is not independent PASS. Unavailable/mismatched model stops review; no implicit substitute.
3. **PR B:** after PR A review/integration gate, implement independent overlay/adapter, fixtures, explicit matrix and handoff in separate branch/worktree/PR. New exact-SHA independent review and CI; changed implementation requires re-review.
4. **Each merge:** authorized scope, exact current head/base/OPEN mergeable PR, actual required CI SUCCESS, final-SHA independent PASS, zero blockers, no secrets/real research/conflict, both Render services `autoDeploy=no` / `autoDeployTrigger=off`. Normal expected-head-protected merge only; no bypass/history rewrite.
5. **Postmerge:** verify main/merge tree/ancestry, exact-main push CI, Render and readback; factual README/Control Center/MCP synchronization. Keep #116 open pending substantive acceptance/postmerge evidence. #111/#113 closeout is separate; unknown main CI is not success.

## 9. Risks and present checkpoint

- Scientific-paper evidence may not establish essentiality: unresolved by default; no legal necessity, filing-readiness or semantic fidelity certification.
- Synthetic actors are not authenticated; BLK-003 OPEN, no production authority/security acceptance.
- Released package consumption is architecturally blocked (§2/§7); independent prototype is the safe authorized deliverable.
- PR #117 merged at the stated base; exact-main push CI is not verified by the connected PR-only workflow listing. #111/#113 closeout remains separate and is not marked complete here.
- MCP read 2026-10-15: `Unknown task: AI-CONV-003`. Claim/state **BLOCKED BY TOOL CAPABILITY**; no fabricated lease/transition.

**Disposition:** HD-01–HD-07 policy approved; limited implementation separately authorized; PR A candidate for independent review. PR B not implemented/tested/reviewed/merged. Product Claims, real-data/provider use, deployment, Phase H/V2 and released-contract migration remain unauthorized.
