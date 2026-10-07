# GOV-AGENT-001-F-PILOT-01 — Workflow V2 Synthetic Lifecycle Pilot

## 1. Metadata and provenance

| Field | Value |
|---|---|
| Program / phase / task | GOV-AGENT-001 / F / GOV-AGENT-001-F-PILOT-01 |
| Version / date | 0.1.0 / 2026-10-07 |
| Status | READY FOR HUMAN EXACT-SHA FREEZE — not committed, submitted or frozen by this authorship |
| Owner / authoring role | Human / Product Owner; distinct PLANNER |
| Planner identity / assignment | 01a1158d-800f-7923-9556-81bfc4dc8cee / 1, ACTIVE per Integration Owner/ADMIN notification of MCP readback |
| Future Implementer | Codex-Integration-Owner; separate assignment and lease required |
| Authorization reference | HUMAN-GOV-AGENT-001-F-PILOT-01-2026-10-07 |
| Activation commit / risk | 9c291325d409f74bc767f9b870e81d75c9b70802 / R3 metadata |
| Branch | feat/gov-agent-001-f-pilot-01 |
| Worktree | D:/AI IP Generator – Project Management/ai-ip-description-generator/.worktrees/gov-agent-001-f-pilot-01 |
| Verification / identity | MANUAL_EXTERNAL / PROCEDURAL_TRUST_BASED |
| Breaking change | No; synthetic governance exercise, no runtime/API/policy change |

Sources: original Human authorization attachment `C:/Users/NguyenSongHaoKiet/.codex/attachments/ba9d8ae9-a104-4b40-a040-1ccb1d4c1c07/Pasted text.txt` (sole Human authority source; §§11–13 govern specification/freeze); subsequent Codex Integration Owner/ADMIN assignment/scope notifications and coordinator freeze-source interpretation; `AGENTS.md` §§20,22,24; GOV-AGENT-001 governance spec v0.2.1 §§16–20,31 Phase F; agents role/P0 contracts; Workflow V2 activation marker and manual verification runbook.
Codex Integration Owner/ADMIN reported local registration, approval and enrollment complete and assignment 1 ACTIVE from MCP readback. Planner preserves this reported provenance without independently repeating that audit or claiming authenticated MCP truth; these notifications are not new Human decisions.
Local pilot HEAD and origin/main were observed at the activation commit; local main is stale. These observations do not replace fresh external activation/main verification before execution or merge.
Task authorization permits this bounded pilot; freeze is a separate ADMIN action. The original Human attachment §§11–13 is the authority source; Integration Owner/ADMIN interprets it as authorizing reconciliation and freeze of the committed conforming v0.1.0 artifact. Subsequent clarification is coordinator interpretation, not a new Human decision. No post-commit Human acknowledgment, future-SHA review, CI result, reviewer PASS, merge or completion is invented.

## 2. Objective, file scope and boundaries

Prove the synthetic V2 lifecycle: separate roles, exact-spec Human freeze, scoped implementation, real CI, candidate CAS/staleness, independent dual review, checkpoint/resume, manual external verification and evidence-backed closeout.
Allowed tracked files are exactly:

- `docs/tasks/GOV-AGENT-001-F-PILOT-01_SPEC.md`: Planner-authored specification only; immutable after freeze unless explicitly superseded through versioned re-planning.
- `docs/pilots/workflow-v2-pilot-01.md`: Implementer-authored synthetic record and bounded explanatory/drill documentation.
- `tests/test_workflow_v2_pilot_01.py`: narrowly necessary deterministic tests using existing Python infrastructure and no added dependency.
- `README.md`: minimum factual Phase F task row/update in Project status required by AGENTS.md §§20/22; preserve all other content, especially Phase E policy/history.

This Planner instruction authorizes writing only this specification. Implementer may write the other allowed files only after freeze, assignment and lease gates.
Review reports, CI provenance, pre-merge packets and post-merge evidence must be preserved externally with stable locators/content hashes; this allowlist does not authorize new tracked evidence files.
Exclude product/backend/frontend/provider/deployment/P2 contracts, B1/B2/B3 core, Phase E governance, database/schema redesign, authenticated identity, verifier adapters, quota/budget redesign, paid/provider API calls and real/confidential research data.
Automatic R0–R4 routing remains OFF; Phase G and AI-CONV are NOT STARTED. R3 metadata does not activate routing or reduce either review requirement.

## 3. Synthetic artifact and predefined A→B change

The pilot Markdown contains one clearly identified JSON record with `pilot_id`, `workflow_version` (integer 2), `activation_commit`, `spec_version` (0.1.0), `synthetic_value` (7), `expected_value` (15), `security_review_required` (true), `quality_review_required` (true), `rule` (`result = input * 2 + 1`) and `cases`.
Each case contains exactly integer `input`, `expected_value` and `computed_value`; booleans are not accepted as integers. Case values are synthetic and checked by arithmetic, without eval, network or provider calls.
Candidate A contains only case input 7, expected/computed 15. Candidate B adds the predefined second case input 11, expected/computed 23 while preserving the first case and all required metadata.
The test accepts these two explicitly permitted case lists, rejects missing/duplicate/unexpected cases, incorrect results/types, mismatched identity/version/activation and disabled review flags. Final B acceptance additionally requires both cases, verified from the exact B artifact.
Negative checks use in-memory variants rather than extra fixture files. Tests validate the artifact, not a mocked governance lifecycle presented as operational proof.
All arithmetic and metadata remain deterministic. The B addition is authorized upfront and does not modify the frozen specification.

## 4. Acceptance criteria and evidence contract

| ID | Required acceptance observation / evidence |
|---|---|
| AC-01 | Integration Owner supplies actual dedicated task registration/approval and explicit V2 enrollment evidence: exact task, R3, authorization reference and activation commit; no V1 execution history or unrelated enrollment. |
| AC-02 | Distinct Planner and Implementer identities/assignments; Planner assignment 1 provenance retained; Planner owns no implementation lease. |
| AC-03 | Planner does not self-freeze, approve implementation or supply independent implementation verdicts; submission and Human freeze actions have separate attribution. |
| AC-04 | Exact committed spec path/version/SHA exists; ADMIN explicitly reconciles its AC/scope conformity with original Human attachment §§11–13, records that source and exact identity as RECORDED provenance, and successfully freezes through supported mechanisms. |
| AC-05 | Implementer edits only allowed files on the named branch/worktree after validating its own assignment, current frozen spec and valid matching bounded lease. |
| AC-06 | A proves 7→15; final B proves 7→15 and 11→23; artifact tests and required applicable validation pass with commands/results/SHA evidence. |
| AC-07 | A then B selected solely by task_workflow.current_implementation_evidence_id; proper expected-pointer CAS, rejection rollback and identical winning-request idempotency demonstrated. |
| AC-08 | Real CI on A and final B independently inspected; required final checks SUCCESS and bound to exact final SHA; operational CI records retain source/run/check identity and observed result. |
| AC-09 | External independent SECURITY_REVIEWER authors Security PASS on exact final spec/base/B SHA, read-only, with zero unresolved blocking findings. |
| AC-10 | External independent QUALITY_REVIEWER authors Quality PASS on the same exact final spec/base/B SHA, read-only, with zero unresolved blocking findings. |
| AC-11 | Security and Quality have distinct identities/sessions, separate from Implementer, Planner and coordinating parent; no parent self-review or verdict borrowing; exact actual model/profile attribution retained. |
| AC-12 | A CI becomes stale after B; any permitted unsubmitted A attempts remain historical/non-current; A evidence cannot satisfy B readiness; B obtains fresh CI and both reviews. |
| AC-13 | Actual provisional_ready or specific legitimate blockers reported; B3 authoritative_merge_eligible remains false; no forced evidence, fabricated authority or interpretation of provisional readiness as merge permission. |
| AC-14 | MANUAL_EXTERNAL pre-merge source verification passes for Human authority, freeze, Git, all CI, both reports, independence, fresh PR/head/base, scope/confidentiality and platform gates; packet preserved. |
| AC-15 | Supported checkpoint/create/read/resume drill preserves candidate, spec, assignments and prior evidence; task remains V2 without deliberate BLOCKED transition, deletion/reset or silent translation. |
| AC-16 | Diff/execution evidence proves bounded synthetic non-production scope; no excluded product/provider/data/policy expansion; factual README synchronization; routing OFF and Phase G NOT STARTED. |

Evidence records identify task, actor/assignment/session, timestamp, source locator/hash, spec version/commit SHA, base SHA, implementation SHA, observed result and limitations as applicable. Unknown fields remain pending, never invented.
MCP/registry claims are RECORDED operational evidence, not authenticated external truth. Hashes bind bytes, not author identity; locally repeated claims do not establish verification.

## 5. Exact-spec Human freeze gate

Integration Owner commits this exact artifact and captures `SPEC_SHA` (specification commit SHA, not a file hash); Planner submission uses task, assignment_id=1, spec_version=0.1.0, spec_sha=SPEC_SHA, artifact_path, actual authorization_ref and status READY.
This document must not embed its own future commit SHA or be edited to insert it after freeze. Preserve committed identity and artifact content hash in external evidence.
The original Human attachment §§11–13 is the sole Human freeze authorization source. Integration Owner/ADMIN's subsequent clarification is a coordinator interpretation of that source: once the committed v0.1.0 artifact conforms to every stated AC/scope, ADMIN must inspect it, reconcile its concrete task/path/version/SPEC_SHA and conformity against that actual source/reference, and preserve the reconciliation. No new post-commit Human acknowledgment or claim that Human reviewed a future SHA is required or permitted.
Proposed `record-verification` fields, to be populated only with real evidence: task_id; actual ADMIN actor_id and actor_type=ADMIN; subject_type=HUMAN_AUTHORIZATION; subject_key=actual freeze approval_ref identifying the current Human source; decision=ATTEST; verification_level=RECORDED; expected_effective_verification_id from actual state; recorded_by; actual source/reference and optional truthful verifier attribution/time.
Its metadata_json must cover `human_authorized=true`, `committed_artifact_exists=true`, exact `spec_sha`, `spec_version=0.1.0` and `artifact_path=docs/tasks/GOV-AGENT-001-F-PILOT-01_SPEC.md`, only after external reconciliation proves them.
Authorized non-Planner ADMIN then uses `project.freeze_spec` with exact task/version/SHA, actual ADMIN attribution, approval_ref, returned approval_verification_id and actual expected_frozen_spec_id; read back successful FROZEN identity and current authorization evidence before any implementation. Existing admin/MCP records remain RECORDED, not authenticated proof of Human identity.
Planner must not record approval, execute freeze, claim a lease or start implementation. Missing/revoked/conflicting authorization, nonconformity or unsupported/failed freeze blocks affected work; frozen requirement changes require explicit supersession/re-planning and applicable new validation/reviews.

## 6. Implementation, real CI and candidate staleness drill

1. Integration Owner validates current external activation, supplied enrollment/authorization evidence and frozen spec; assigns distinct Implementer and starts its matching bounded lease through existing tools. Capture actual authorized base SHA.
2. Implementer creates A artifact/test and a minimal factual README Phase F row, runs validation, commits A and records it with expected_current_implementation_evidence_id=null only if actual pointer is null; read back A's evidence ID.
3. Open a draft PR on A to trigger existing PR CI (branch pushes alone do not trigger the current workflow). Inspect real provider results before moving head to B; preserve run/check links, head binding, execution revision and timestamps. Do not mislabel a synthetic PR merge checkout SHA as A.
4. Record actual A CI observations with unique references. Pending/failure/cancelled/unknown results remain explicit; do not invent SUCCESS. Required exact-head binding must be externally reconciled.
5. If separate authorized external reviewers and supported tools permit, each reviewer starts a SECURITY/QUALITY attempt on exact current A/spec/base. No verdict is submitted for the drill. Preserve IDs/identities; MCP unsubmitted attempts are IN_PROGRESS, described as pending work, not a PENDING/PASS verdict.
6. If attempts cannot legitimately start, preserve the capability/independence reason; prove real A CI staleness and report review-attempt demonstration unavailable. Do not bypass role checks or claim the omitted demonstration succeeded.
7. Implementer adds only the predefined 11→23 case to produce committed B; all remaining final tracked edits, including factual README updates, must precede final review. Keep spec unchanged.
8. While A is current, try recording actual B with expected pointer null: require explicit CAS conflict and pointer/history rollback. Record B with expected A evidence ID: require successful atomic transition. Retry identical winning B request with original expected A: require same row/pointer without duplicate history.
9. Read state/review status/gate: B is sole current pointer, A CI stale, A attempts retained with current=false when present. B streams have no satisfying PASS. Do not submit fabricated stale PASS payloads or delete/retarget A evidence.
10. Obtain and externally inspect real final B CI, record it honestly, and initiate new independent final B attempts. Preserve A/B immutable history and every real failed/pending observation.

## 7. Checkpoint/resume and validation

During IN_PROGRESS with a valid Implementer lease, capture current task/workflow/spec/candidate/assignment/history identifiers and last safe committed SHA; avoid dirty tracked files at the checkpoint.
Use `checkpoint.create` with actual task, owner matching Implementer, role=IMPLEMENTER, assignment_id, last_safe_commit, completed_work, tests, remaining_work, blockers, stop_reason and exact_next_action. Use a bounded planned pause reason and truthful blockers.
Read `checkpoint.get_latest` with task_id and role=IMPLEMENTER, then reload project state, assignments, frozen spec, Git head/status and candidate pointer before continuing. Resume through the existing valid lease; no invented resume command or status transition is required.
Require unchanged V2 enrollment, preserved checkpoint/history and correct current pointer. Do not use project.stop_and_handoff for this planned drill because it marks the task BLOCKED; do not expire leases, stop the shared server, mutate SQLite or alter activation to manufacture rollback.
An actual invalid lease/stop condition blocks affected execution and requires legitimate recovery; it is not hidden as a successful drill.
Required checks: git diff --check; focused pilot test; python agents/validate_skills.py; python tools/validate_workflow_v2_governance.py; relevant agent/governance regression and existing offline repository CI.
In tools/project-orchestrator-mcp run existing npm run typecheck, npm test and npm run build against the candidate checkout; isolate generated output and temporary test databases, never point synthetic fixtures at the operational DB.
Record actual commands/results/revision; required unavailable/failing checks block progress unless specifically excepted by Human. No tests are run or PASS claimed by this specification authorship.

## 8. Final independent reviews, external merge and closeout

Final F_FINAL_SHA is B only while no later tracked commit exists. Remediation creates a new final candidate and requires applicable fresh CI and both independent reviews; never reuse old PASS on a changed SHA.
Security reviews authority/scope, enrollment/freeze provenance, secrets/confidentiality, instruction/data boundaries, independence and exact-SHA/stale evidence handling. Quality reviews all ACs, both arithmetic cases, meaningful tests/regression, pointer/CAS, checkpoint/history and auditability.
Both external reviewers inspect the frozen spec and exact base/final Git diff in independent read-only sessions; preserve original separately authored reports and exact model/profile/session attribution externally, with hashes and canonical locators.
Neither Planner, Implementer nor coordinating parent provides these verdicts. Reviewer tracked implementation writes invalidate independent PASS. Do not add review reports to the implementation branch merely to publish evidence after review.
Inspect project.get_merge_gate after genuine final CI/reviews/policy evidence: target provisional_ready=true or report legitimate blockers. Keep authoritative_merge_eligible=false because accepted adapters are unavailable; manual external eligibility is separate.
Immediately before merge, Integration Owner follows WORKFLOW_V2_MANUAL_VERIFICATION.md against actual Human approval/freeze sources, Git, CI provider, canonical independent reports and fresh remote PR state; preserve each check's result/source/time in a durable external pre-merge packet.
Require correct repository, OPEN/mergeable PR, exact reviewed head/base, no newer commit/conflict/blocking finding/secret/scope violation, every required CI SUCCESS and both PASS on that same final SHA; perform normal expected-head-protected merge only when all governance/platform gates pass.
Platform denial is not bypassed through another tool/API/CLI. Head/spec movement invalidates readiness and requires reconciliation/new applicable checks; no force push, history rewrite or local-merge bypass.
After actual merge verify merged=true, exact merge/main SHA, reviewed-final ancestry, expected tree and required exact post-merge CI SUCCESS; preserve source-backed merge and CI evidence, not merely MCP claims.
README Project status must accurately reflect the phase reached. Future post-merge factual updates are limited to the same row and follow applicable review/CI/merge gates; do not mark Completed before all acceptance/closeout evidence exists or silently append unreviewed changes to final B.
Closeout records activation/enrollment, assignments/freeze/lease, A/B and stale behavior, CI/reviews/gates, checkpoint/history, manual packet, merge/post-merge CI and findings/resolutions; report pilot PASS/FAIL with any unproven checks.
Provide a Human adoption decision packet covering weaknesses, identity limits, manual burden, B3 adapter limits, independence, rollback and recommendation. This is advice only: Phase G remains NOT STARTED and automatic routing OFF.

## 9. Stops, revision history and Planner handoff

Stop affected work for missing exact freeze authority, role/lease conflict, incapable CAS/checkpoint behavior, evidence contradiction, unavailable required CI/review, unauthorized scope/data/provider/production demand or any AGENTS.md §19 condition. Preserve history and report the concrete blocker; do not silently redesign MCP or widen this spec.
Revision: none → 0.1.0, 2026-10-07, distinct PLANNER; Human-authorized bounded Phase F specification and AC01–16; no breaking change, implementation, freeze or Phase G action.

```text
Task ID: GOV-AGENT-001-F-PILOT-01
Agent: PLANNER 01a1158d-800f-7923-9556-81bfc4dc8cee; assignment 1 ACTIVE per Integration Owner/ADMIN notification of MCP readback
Reviewer: Future external independent Security and Quality reviewers; pending
Status: READY FOR HUMAN EXACT-SHA FREEZE; authorship only, not task completion
Version: 0.1.0
Work completed: Defined bounded scope, AC01–16, freeze/evidence contract and lifecycle drills
Files affected: docs/tasks/GOV-AGENT-001-F-PILOT-01_SPEC.md only
Evidence checked: Original Human attachment; Integration Owner/ADMIN notifications and coordinator interpretation; governance/roles/P0; local Git; existing MCP/CI contracts
Findings: Task approval and ADMIN exact-spec freeze are separate; original Human §§11–13 is sole authority source, subsequent clarification is coordinator interpretation; local main is stale
Decisions: Predefined A 7→15 and B additional 11→23; dual external independent final reviews
Issues: Committed SPEC_SHA, ADMIN exact-spec reconciliation/supported freeze, CI/reviews/implementation remain future
Security impact: Specification only; no operational state, runtime, provider or data-policy change
Recommended next action: Integration Owner commits exact spec; ADMIN reconciles original Human attachment §§11–13 and conforming committed identity, records RECORDED provenance and successfully freezes before implementation
```
