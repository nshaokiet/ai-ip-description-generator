# GOV-REVIEWER-001 — Standing independent reviewer default

| Field | Value |
|---|---|
| Document ID | GOV-REVIEWER-001 |
| Version | 0.1.0 |
| Status | Human model-selection decision effective 2026-10-14; this documentation sync remains pending its own review/CI/merge |
| Owner | Human / Product Owner |
| Author | ChatGPT/Codex |
| Date | 2026-10-15 |
| Task | [Issue #113](https://github.com/nshaokiet/ai-ip-description-generator/issues/113) |
| Authority | [Human standing decision on PR #112](https://github.com/nshaokiet/ai-ip-description-generator/pull/112#issuecomment-6164405254) |
| Scope | Workflow V1 independent reviewer **selection only** |

## Prospective selection

1. For each **separately Human-authorized** new Workflow V1 task requiring independent review, select **Gemini 3.8 Flash High / Antigravity STRICT READ-ONLY** by default; do not solicit repeat selection if nothing changes. A later explicit task-specific Human selection overrides the standing default.
2. Before review, confirm the **actual runtime model and profile**; do not infer aliases, substitutes, identities, availability or approval. If the model cannot be selected/verified, record a blocker and ask Human for a replacement decision.
3. Run review genuinely independently and read-only against an **immutable final candidate SHA**. Record task, repository, base/head, changed files, specification/acceptance criteria, relevant executed test/CI evidence, security/privacy findings by severity, reviewer identity and actual session ID (identify session reuse). Publish an attributed **PASS / REQUEST CHANGES / BLOCKED** with supporting evidence.
4. A changed reviewed implementation/doc SHA invalidates earlier approval for the new SHA. Re-review and rerun applicable exact-head CI; before merge check current PR/base/head, conflicts, scope, secrets, all required reviews, branch permissions, Render safety and expected-head protection. After merge independently verify exact-main CI/readback and closeout without inventing state.
5. Never treat Codex self-review, external Human-provided attribution, a past model choice or a GitHub comment as proof of authenticated independent identity or a native GitHub approval unless directly evidenced.

## Historical boundary

The **Gemini 3.8 Flash High** report on AI-CONV-002 candidate `beb69bf9ff0972b27147c62a938323a74f3a0193` existed **before** the Human standing decision on **2026-10-14** and was not made gate-eligible retroactively. The actual later remediation/re-review and PR #112/#114 merge records remain authoritative for those individual SHAs. Earlier Gemini 3.1 Pro High entries are historical and must not be rewritten. Neither this guide nor Issue #113 backfills any review, test, signature or task-state transition.

## Authority separation and stop conditions

- **Workflow V1**: selection defaults do not authorize tasks, exceptions, implementation, merge without evidence, release, or deployment.
- **Workflow V2 / Phase H**: requires separate explicit activation/enrollment, assigned roles and actual independent **Security + Quality** identity/session/verdict evidence where specified; one default model cannot satisfy multiple independent reviewer streams or bypass MANUAL_EXTERNAL.
- **Product/runtime AI**: no change to provider selection, API budget (still zero until authorized), Claims policy, real/confidential research, tenant/security/retention, USPTO filing-readiness or Render deployment.
- **Preserve** all source-attributed findings and historical model availability context. When actual review model is unavailable, a session's identity is unverifiable, or a required gate is missing: **STOP the affected operation** and record what is missing.

## Publication checklist for this docs-only task

- [ ] Review exactly this docs-only final SHA using actual Gemini 3.8 Flash High / Antigravity STRICT READ-ONLY; preserve model/session/SHA/verdict and findings.
- [ ] Verify required PR exact-head CI SUCCESS and clean scope/diff/secret checks.
- [ ] Verify updated base/head, separate Render no/off controls and applicable AGENTS.md §8/19 gates.
- [ ] Perform only an authorized normal expected-head-protected merge; no forced merge or invented PASS.
- [ ] Verify exact-main postmerge CI/readback, update honest status/README if task state changes, then close Issue #113 only after evidence.

This checklist represents **requirements**, not assertions that they have been satisfied.
