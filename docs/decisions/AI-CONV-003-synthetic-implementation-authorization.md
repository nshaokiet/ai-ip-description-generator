# AI-CONV-003 — separate limited implementation authorization

| Field | Value |
|---|---|
| Record / version | HUMAN-AI-CONV-003-SYNTHETIC-IMPLEMENTATION-2026-10-15 / 1.0.0 |
| Date / recorder | 2026-10-15, Asia/Saigon / Codex |
| Authority | Human / Product Owner direct instruction in this Codex conversation |
| Source title | TASK: AI-CONV-003 — Implement HD-01 to HD-07 / Synthetic/Offline Claims Semantic Authority |
| Earlier policy-only authority | [Issue #116 comment 6187375281](https://github.com/nshaokiet/ai-ip-description-generator/issues/116#issuecomment-6187375281) |
| Scope specification | [AI-CONV-003 v0.1.1 candidate](../tasks/AI-CONV-003-claims-semantic-authority-specification.md) |
| Workflow | V1 standing delegation; separate PR A / PR B |

The direct instruction explicitly states:

> When Human submits this prompt directly to Codex, treat it as a new, limited instruction to prepare and implement the approved synthetic/offline prototype. Record that instruction separately from the earlier policy-only approval.

Human submitted that prompt directly on 2026-10-15. This record identifies the instruction; it does not claim a new GitHub Human comment, authenticated identity, independent approval or MCP task state. The earlier policy-only decision remains historically unchanged.

Authorized outputs: policy synchronization preserving v0.1.0 and assigning a new version; internal overlay and synthetic Human adapter; HD-01–HD-07 tests; positive SYSTEM/APPARATUS eligibility where released P2-004 permits; negative METHOD/PROCESS/COMPOSITION authority; regression/security checks; separate PRs, fixed-SHA handoffs and conditional integration/closeout.

Required order: repository verification → documentation PR A → independent specification review and exact-head CI before integration → separate prototype PR B → its own independent review/CI → conditional merges/postmerge verification. The direct instruction says to stop at required external review or Human-only architectural decisions. No implementation is inferred from the earlier policy-only approval.

Excluded: released-contract breaking change or silent schema/validator mutation; hidden eighth provenance input/package-validation bypass; public routes/frontend; real/confidential research; real authentication/persistent authorization; database/external dependency/service; paid provider calls; Render/deployment; production/legal/filing acceptance; Workflow V2/Phase H; AI-CONV-004/005/006 authorization.

Required reviewer: Gemini 3.8 Flash High / Antigravity STRICT READ-ONLY, actual model/profile/session and reuse disclosure, exact final SHA, independent verdict. No Codex self-review substitute. Merge requires scope safety, PASS, actual required CI SUCCESS, zero blockers, fresh Git/PR/main, both Render services Auto-Deploy OFF and normal expected-head protection. Postmerge exact-main CI/readback/Render required before closeout; keep #116 open while gates remain.

## Version history

| Previous | New | Date | Author | Change / reason | Reference | Breaking |
|---|---|---|---|---|---|---|
| None | 1.0.0 | 2026-10-15 | Codex | Record direct limited implementation instruction separately from policy approval | Direct Human prompt above; Issue #116 | No |
