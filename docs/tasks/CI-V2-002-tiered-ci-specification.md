# CI-V2-002 — Tiered CI architecture specification

| Field | Value |
| --- | --- |
| Version / date / author | 0.1.0 / 2026-10-21 Asia/Saigon / Codex |
| Status | DRAFT SPECIFICATION ONLY — implementation not authorized by this document |
| Owner / reviewer | Human Product Owner / Gemini 3.8 Flash High, Antigravity STRICT READ-ONLY, pending |
| Authorization | Human “TASK: AI-IP CI-V2 — GitHub Actions Optimization”, 2026-10-21, specification/planning scope |
| Baseline | `7abc63e12e18a8027de1d4be4c71ad7aa182cb91` |
| Relationship | Separate from CI-V2-001 PR #144; no workflow changes on this planning branch |

History: none → 0.1.0, 2026-10-21, Codex, proposed architecture under Human
planning authorization. Breaking change: **No implementation**. Any future
required-status contract migration requires separate explicit authorization.

## Required lanes

| Lane | Required behavior |
| --- | --- |
| Fast CI | Every PR: dependency consistency, lint/typecheck, unit/contract tests and provider tripwire; fast feedback must never replace required full regression |
| Full CI | Existing full backend/security/MCP/frontend/browser/compatibility regression, document layout and public-reference verification for integration and high-risk changes; premerge, exact PR head |
| Visual QA | Synthetic PDF/DOCX/LibreOffice layout, patent-reference calibration, Playwright screenshots/traces when required by rendering/UI risk or acceptance/review; full evidence only by justified selection |
| Governance CI | Always evaluate versioned schema/contracts, role/skill/activation rules, documentation links/status consistency and workflow checks; no automatic project acceptance or authenticated-identity claim |
| Required Gate | Always scheduled, validates exact-head selection manifest and every mandatory result; missing, failed, cancelled or unexpectedly skipped required work fails closed |

Until a separately approved migration, retain workflow `CI` and existing required
statuses `build-and-test` and `mcp-tests`. A new aggregate gate must not silently
replace them. Do not introduce workflow-level `paths`/`paths-ignore` that leaves
required checks pending. Preserve PR/main/manual triggers and normal branch gates.

## Selection and risk

An always-run selector computes a merge-base-to-exact-head changed-file set with
rename/delete coverage and sufficient Git history. Persist head/base/merge-base,
selector version, changed paths, reasons, required lanes and expected job matrix.
Use conservative defaults: unknown paths, diff/API/pagination/truncation errors,
missing history or invalid policy select **full regression**, or fail selection;
they cannot select fewer checks. CI/job names are not authorization or review.

| Change class | Premerge requirement |
| --- | --- |
| Custody/provenance, Claims authority, backend/API, security/auth, dependency/lock/install scripts | Full existing regression + security + MCP + applicable governance |
| USPTO assembly, templates, PDF/DOCX renderer, source evidence/contracts | Full regression + full applicable rendering/reference visual verification |
| CI/selection/gates/governance enforcement, selector tests | Full regression + governance + selection-negative tests; no self-exemption |
| Frontend/UI/browser/config | Frontend/unit/security/browser/static/demo and compatibility; relevant backend integration; full where boundary/risk uncertain |
| Demonstrably isolated prose-only documentation | Fast + governance, only after independent review of a precise allowlist and separate Human acceptance; until then full |
| Unclassified, deleted/renamed or mixed change | Union of requirements; uncertainty selects full |

Risk is explicit metadata, never permission to skip independent review. Policy
is evaluated from trusted approved policy; PR policy changes cannot reduce their
own checks. Baseline test inventory must be mapped file-by-file before changing
execution, including all currently collected tests and pinned compatibility SHA.
No implementation of selective skipping is approved by this specification.

The aggregate uses an explicit planned matrix and exact-head results. A lane
may be intentionally not applicable only if the trusted plan explains why and
the gate verifies that plan. `needs.*.result == success` is required for every
planned lane, including mandatory evidence delivery. A green gate cannot conceal
cancelled, empty, partial, stale-SHA or absent jobs. CI result and reviewer verdict
remain separate evidence. Never use `continue-on-error` to neutralize required work.

## Verification before implementation acceptance

1. Inventory existing commands/test coverage/status contracts; replay representative
   historical paths plus high-risk, rename, delete, unknown and mixed fixtures.
2. Exercise selector failure, forged reduced plan, missing/empty matrix, cancellation,
   stale SHA, skipped required job, test failure and security upload failure;
   aggregate must fail. Gate must be scheduled even after upstream failure.
3. Demonstrate no upload failure blocks later functional work and no lost security
   evidence requirement; exact checkout and provider-free flags remain enforced.
4. Measure wall-clock/runner minutes/upload bytes against equivalent baseline
   runs; no claimed savings from skipped mandatory work or failed uploads.
5. Independent exact-final-SHA review and complete required CI; normal protected
   merge, postmerge exact-main CI and README/Control Center evidence closeout.

Budget remains USD 0 for AI; no real/confidential research, deployment/Render,
Claims activation, active SQLite migration, billing increase or new external
service. Phase CI-V2-001 must not be expanded to implement this architecture.
Rollback future implementation by a reviewed ordinary revert of its verified
merge, preserving evidence/status compatibility; no force/reset or policy bypass.

## Handoff

Task ID: CI-V2-002. Agent: Codex, specification author. Reviewer: Gemini 3.8
Flash High / Antigravity STRICT READ-ONLY, pending. Status: DRAFT SPECIFICATION.
Version: 0.1.0. Work completed: lane, selection, required-gate and validation
design. Files affected: this specification only. Evidence checked: baseline CI,
AGENTS.md, CI-V2-001 known failure and existing status contracts. Findings:
selection/matrix implementation and performance not validated. Decisions: planning
only under Human instruction. Issues: separate implementation authorization and
spec review pending. Security impact: proposal preserves existing boundaries.
Recommended next action: review specification; authorize a separate implementation
scope only after decisions and CI-V2-001 evidence are reconciled.
