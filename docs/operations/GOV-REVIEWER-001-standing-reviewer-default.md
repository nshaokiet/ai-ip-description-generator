# GOV-REVIEWER-001 — Standing independent reviewer default

| Field | Value |
|---|---|
| Document ID | GOV-REVIEWER-001 |
| Version | 0.2.0 |
| Status | Permanent Human model-selection decision effective 2026-11-18; documentation sync pending independent review/CI and explicit Human merge authorization |
| Owner | Human / Product Owner |
| Author | ChatGPT/Codex |
| Date | 2026-11-18 |
| Task | GOV-REVIEWER-002; historical selection task [Issue #113](https://github.com/nshaokiet/ai-ip-description-generator/issues/113) preserved |
| Authority | [Permanent Human decision 2026-11-18](../decisions/GOV-REVIEWER-002-permanent-reviewer-model.md), superseding the [2026-10-14 selection](https://github.com/nshaokiet/ai-ip-description-generator/pull/112#issuecomment-6164405254) |
| Scope | Standing reviewer selection for all current/future independent Security and Quality reviews; no role/activation/merge authority expansion |

## Prospective selection

1. For each **separately Human-authorized** current/future independent Security or Quality review, select **Gemini 4 Argon (High) / Antigravity STRICT READ-ONLY**. This permanent Human choice is effective **2026-11-18**, including DEP-SEC-20261118-001 / PR #165, until explicitly superseded by a subsequent Human decision. Do not solicit repeat selection. Only the prior model-authorization blocker is resolved; review/CI/security/merge gates remain.
2. Before review, confirm the **actual runtime model and High profile**; do not infer aliases, substitutes, identities, availability or approval. If Gemini 4 Argon (High) is unavailable, mismatched or cannot be verified, **STOP the affected review and obtain explicit Human authorization before any substitute**.
3. Run each review genuinely independently and STRICT READ-ONLY against an **immutable final candidate SHA**. Record task, repository, base/head, changed files, specification/acceptance criteria, relevant executed test/CI evidence, security/privacy findings by severity, reviewer identity, actual model/profile, actual session ID, fresh-session YES/NO/UNKNOWN, reuse YES/NO/UNKNOWN and prior task/role context if reused. Missing/unverifiable identity or independence blocks the affected gate; never label an unknown/reused session fresh. Security and Quality use separate actual reviewer identities/sessions and separately authored evidence; neither borrows the other's verdict as proof. Publish an attributed **PASS / REQUEST CHANGES / BLOCKED** with supporting evidence.
4. A changed reviewed implementation/doc SHA invalidates earlier approval for the new SHA. Re-review and rerun applicable exact-head CI; before merge check current PR/base/head, conflicts, scope, secrets, all required reviews, branch permissions, Render safety and expected-head protection. After merge independently verify exact-main CI/readback and closeout without inventing state.
5. Never treat Codex self-review, external Human-provided attribution, a past model choice or a GitHub comment as proof of authenticated independent identity or a native GitHub approval unless directly evidenced.

## Historical boundary

The 2026-10-14 Gemini 3.8 Flash High standing selection is superseded for reviews
from 2026-11-18. Preserve historical reports, actual model attribution, sessions,
verdicts and prior limitations unchanged. The new authorization does not
retroactively validate an older mismatched-model report or stale SHA.

The **Gemini 3.8 Flash High** report on AI-CONV-002 candidate `beb69bf9ff0972b27147c62a938323a74f3a0193` existed **before** the Human standing decision on **2026-10-14** and was not made gate-eligible retroactively. The actual later remediation/re-review and PR #112/#114 merge records remain authoritative for those individual SHAs. Earlier Gemini 3.1 Pro High entries are historical and must not be rewritten. Neither this guide nor Issue #113 backfills any review, test, signature or task-state transition.

## Authority separation and stop conditions

- **Workflow V1**: selection defaults do not authorize tasks, exceptions, implementation, merge without evidence/applicable Human authorization, release, or deployment. This documentation PR must not merge without explicit Human authorization.
- **Workflow V2 / Phase H**: requires separate explicit activation/enrollment, assigned roles and actual independent **Security + Quality** identity/session/verdict evidence where specified; one session/report cannot satisfy multiple independent reviewer streams or bypass MANUAL_EXTERNAL. The same authorized model may be used in distinct genuinely independent sessions.
- **Product/runtime AI**: no change to provider selection, API budget (still zero until authorized), Claims policy, real/confidential research, tenant/security/retention, USPTO filing-readiness or Render deployment.
- **Preserve** all source-attributed findings and historical model availability context. When actual review model is unavailable, a session's identity is unverifiable, or a required gate is missing: **STOP the affected operation** and record what is missing.

## Publication checklist for the current documentation-only update

- [ ] Review the entire documentation-only final SHA using actual Gemini 4 Argon (High) / Antigravity STRICT READ-ONLY; preserve separate Security/Quality evidence, actual model/profile/session/freshness, SHA/verdict and findings. No validator/test source change is included.
- [ ] Verify required PR exact-head CI SUCCESS and clean scope/diff/secret checks.
- [ ] Verify updated base/head, separate Render no/off controls and applicable AGENTS.md §8/19 gates.
- [ ] Obtain explicit Human authorization before any normal expected-head-protected merge; no forced merge or invented PASS.
- [ ] Verify exact-main postmerge CI/readback and update honest status/README only after actual authorized merge; this change does not close historical Issue #113.

This checklist represents **requirements**, not assertions that they have been satisfied.

## Version history

| Old | New | Date | Author | Change/reason/authority | Breaking change |
|---|---|---|---|---|---|
| 0.1.0 | 0.2.0 | 2026-11-18 | Codex | Permanent Human reviewer-model update, separate stream/session/freshness evidence and unavailable-model stop; GOV-REVIEWER-002 | No product/runtime or role-authority change; selection policy explicitly superseded |
