# CI-V2-001 — document layout installer recovery plan

| Field | Value |
|---|---|
| Document ID | CI-V2-001-QA-INSTALLER-PLAN |
| Version / date / author | 1.0.0 / 2026-11-05 Asia/Saigon / Codex |
| Status | PLAN ONLY — no installer/workflow implementation in foundation |
| Authority | Human CONTINUE REVIEW CLOSEOUT: prepare HTTP503 recovery plan; no automatic workflow/gate change |
| Related work | [PR144](https://github.com/nshaokiet/ai-ip-description-generator/pull/144), CI-V2-001 upload hardening |

## Actual failure and authorized boundary

[Run42034588440](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/42034588440)
on foundation `31d9fce57681e4e21fe552e894898f29d84d23c8` failed at
**Install offline document layout QA tools**: signed Ubuntu snapshot InRelease
requests returned HTTP503; installer exit100. Required security archive also
failed because the producer directory was never created. MCP SUCCESS;
backend1127 PASS/2 SKIP. Frontend/audit/build/browser SKIPPED is not PASS.

CI-V2-001's existing task record authorizes upload-tail hardening and retained
gates; it records earlier HTTP503 without claiming a fix. Foundation spec A3
labels installer recovery a proposed extension. This Human instruction authorizes
preparing the plan, not implementing the extension or editing workflow. Before
implementation, reconcile the concrete extension authorization with task/owner.
PR144 remains Draft/CONFLICTING at `43e07dfa36b217066647af23f2dda2c6c715bd0c`;
do not overwrite its worktree or reuse its old review for a changed head.

## Proposed bounded patch, separate from foundation

1. Use a new isolated branch/worktree from the verified appropriate CI baseline.
   Preserve PR144's existing commits and reconcile its main conflicts separately.
   Proposed changed paths: `tests/backend/install_p2_006_qa.sh`, a focused installer
   regression test, CI-V2 task/evidence/status docs. No workflow edit is needed
   merely to invoke the already-used installer; any additional workflow change
   requires its own concrete scope check and review.
2. Keep Ubuntu24.04/amd64, signed snapshot `20261009T000000Z`, all exact package
   revisions, fonts, runtime verification and isolated apt lists/sources unchanged.
   No live mirror/PPA fallback, snapshot refresh, unauthenticated install or
   signature/hash bypass. Existing historical-metadata handling stays unchanged.
3. Proposed retry policy: at most3 attempts, bounded per-attempt acquisition
   timeouts, delays2s then5s. Apply only to recognized transient acquisition
   failures (HTTP503 first; expand classification only with approved evidence).
   Preserve diagnostic exit/status output; do not treat a successful apt-update
   exit alone as proof of complete fresh indexes. Fail if required index fetches
   remain incomplete. Use strict apt update error handling compatible with the
   pinned Ubuntu version and verify its real behavior before choosing options.
4. Never proceed to install after exhausted/incomplete update. A recognized
   transient package-download failure may receive the same bounded retry only
   if explicitly included in the implemented scope. Permanent signature/hash,
   missing pinned version, unsupported OS/architecture or package configuration
   errors fail immediately; no generic retry of arbitrary install failures.
5. Keep mandatory security artifact, missing-files error, retention, test counts,
   provider-free flags and CI status contracts. Do not use continue-on-error,
   optionalize QA/audit, suppress upload failure or manufacture an empty archive.

## Acceptance and test plan — not executed by this document

| Scenario | Required evidence |
|---|---|
| Immediate success | One attempt, exact sources/pins preserved, verification/layout gates execute |
| Transient503 then success | Retry bound/delays observed; install only after complete successful indexes |
| Persistent503 / update returns0 with failed index warning | Nonzero final failure before install; no stale-index acceptance |
| Signature/hash/version/OS/architecture failure | Immediate fail-closed behavior; no fallback or unrelated retry |
| Install transient failure, if separately included | Bounded acquisition-only retry; permanent package configuration failure not retried |
| Existing CI upload hardening | Original25 focused checks, cleanup checks and YAML/actionlint appropriate to actual final diff; no reduction of mandatory evidence |
| Real Ubuntu pinned environment | Actual installer, runtime verifier and document/reference layout QA PASS on supported Ubuntu24.04amd64, not mocked-only acceptance |
| Final hosted candidate | Exact final SHA required CI SUCCESS and mandatory security artifact present, digest/content checked; new independent Gemini/Antigravity review |

Mocked apt/fake-clock tests are appropriate for retry semantics; they do not prove
real snapshot availability or replace hosted/layout tests. Preserve failed logs.
One successful rerun alone does not demonstrate persistent503 fail-closed behavior.
No global workflow rerun loop is proposed.

## Integration order and decisions

PR147's dependency fix and this installer failure are independent. After a Human-
authorized147 merge, verify exact-main ancestry/tree/CI/artifacts. If exact-main
CI fails at installer503, record the blocker and do not claim accepted closeout
or proceed with the conditional151 integration. A separately authorized CI fix
must meet its own review/CI/merge/postmerge gates. Once the verified main baseline
is accepted, normal merge it into151 without force-push, preserve150 and other
agents' changes, freeze final HEAD/tree and run applicable CI/fresh review.

Human decision needed before implementation: accept the concrete bounded installer
extension, target CI task/PR and test criteria above, or supply a narrower scope.
No implementation, workflow edit, merge, deploy or gate exception is executed here.

Task ID: CI-V2-001 / RESUME-FOUNDATION-001-WEB planning
Agent: Codex — planner of bounded recovery proposal
Reviewer: Independent final implementation review PENDING; no implementation SHA exists for this plan
Status: PLAN PREPARED / implementation authorization and CI acceptance PENDING
Version: 1.0.0
Work completed: Identified actual503/bootstrap/archive cascade and prepared bounded patch/test/integration plan
Files affected: This document only; installer/workflow unchanged
Evidence checked: CI42034588440 logs/jobs/artifacts; current installer/environment pins; existing CI-V2 task and foundation A3 scope
Findings: Bootstrap failure prevents audit/security evidence; PR144 conflicts; existing upload authorization is not implicit installer-extension approval
Decisions: No live fallback, pin/gate weakening or automatic workflow modification
Issues: Concrete extension authorization, implementation, independent review and real hosted acceptance outstanding
Security impact: Planning only, preserves signed immutable inputs and mandatory security evidence
Recommended next action: Human disposition of bounded extension; implement separately only within authorized CI scope

1.0.0 created 2026-11-05 by Codex. Breaking change: No — proposal only.
