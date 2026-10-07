# Workflow V2 — Manual / External Authoritative Verification

Version: 1.0.0 | Date: 2026-10-07 | Owner: Human / Product Owner
Status: Phase E implementation for independent governance review; effective only after the reviewed Phase E PR merges and its exact merge commit on main is verified.
Task: GOV-AGENT-001-E | Specification: GOV-AGENT-001 v0.2.1, §§18.1–20, 31 Phase E, 33.

## Human decisions and activation boundary

The Human explicitly authorized Phase E implementation with these decisions:

| Decision | Authorized initial policy |
|---|---|
| E-01 | MANUAL_EXTERNAL authoritative verification; no verifier adapters; B3 authoritative_merge_eligible remains false |
| E-02 | PROCEDURAL_TRUST_BASED identity; cryptographic identity not required for initial operation; GOV-IDENTITY-001 remains FUTURE |
| E-03 | Automatic R0–R4 routing NOT ACTIVATED; Phase F pilot requires separate Security and Quality reviews on the same final SHA |
| E-04 | Explicit Human-authorized V2 enrollment only; no historical V1 backfill |
| E-05 | The reviewed Phase E PR merge commit on main is WORKFLOW_V2_ACTIVATION_COMMIT; branch/review/open PR alone is not activation |
| E-06 | Separately reviewed disable stops new enrollment, preserves evidence and requires Human disposition for an in-progress V2 task |

These recorded decisions do not authenticate their author by themselves. Reconcile
them with the actual Human authorization channel before relying on them. This
implementation instruction is not independent review PASS or permission to merge
the Phase E PR in the current session. Phase F is NOT STARTED.

[WORKFLOW_V2_ACTIVATION.yaml](WORKFLOW_V2_ACTIVATION.yaml) is the single canonical
governance marker. Its enabled setting is a conditional policy, not a runtime
switch or an environment variable. Effective activation requires all of:

1. Read the marker from current verified main, not the implementation branch.
2. Verify explicit Human Phase E approval, independent governance review PASS on
   the final implementation SHA, required exact-SHA CI SUCCESS and merge eligibility.
3. Verify that the reviewed Phase E PR actually merged normally to main; check the
   exact merge SHA, reviewed-head ancestry and accepted post-merge state/CI.
4. Record that immutable merge SHA as WORKFLOW_V2_ACTIVATION_COMMIT in the durable
   post-merge closeout and future enrollment evidence. Keep the activation PR,
   review, Human approval and CI links with it; verify against real Git/GitHub.
5. Confirm current main's marker is still enabled and no accepted disable or
   conflicting Human decision applies. Missing/unverifiable identity means OFF.

Do not embed the future merge's own SHA into its pre-merge tree, amend reviewed
history to insert it, or use the branch implementation SHA as the activation
commit. If main later advances, the accepted activation merge remains immutable
history and must remain in main's ancestry; a later reviewed disable controls
new admission without deleting that history.

PHASE E BRANCH PRESENT != WORKFLOW V2 ACTIVATED.
PHASE E REVIEW PASS != WORKFLOW V2 ACTIVATED.
PHASE E PR OPEN != WORKFLOW V2 ACTIVATED.

## Workflow selection and enrollment preflight

Before any proposed enrollment, the Human/operator checks effective activation
from real sources as above, then separately checks task authorization, scope,
review requirements, prospective eligibility and the exact activation-commit
reference. No Phase E implementation/check runs enrollment or creates a task.

- OFF, or no explicit V2 enrollment: use the authorized V1 path.
- ON plus valid Human task authorization, explicit V2 enrollment referencing the
  accepted activation merge and the role/spec/evidence state required for the
  proposed action: the task is eligible for that V2 action.
- Missing required state blocks the proposed action. Enrollment is not permission
  to implement, self-freeze, approve, waive review/CI or merge.
- A task with existing V2 work/history must not silently fall back to V1 when
  activation is disabled or its evidence becomes invalid: checkpoint and obtain
  explicit Human disposition. Historical V1 tasks are not migrated.

Only after the external preflight succeeds may an authorized Human/operator use
the existing local command:

```text
npm run admin -- enroll-v2 /absolute/path/to/enrollment.json
```

The enrollment JSON identifies the separately authorized task, risk metadata,
authorization reference and exact activation_commit. The command does not prove
that its supplied strings are Human approval or an accepted Git commit. Existing
prospective/idempotent enrollment checks still apply. PLANNED eligibility is not
task execution authorization. There is no public automatic enrollment path.

Schema availability != activation. MCP V2 tools availability != activation.
Agent role/skill installation != activation. Activation on verified main plus
explicit task enrollment permits only the action allowed by governance and state.

## Required authoritative pre-merge procedure

The authorized integration owner performs the following checks against real
sources immediately before each proposed merge. Record a durable evidence packet
with task, actor, timestamp, repository/PR, exact spec/base/head and individual
source references/results. An unavailable source is a blocker, not an assumption.

| Check | Required observation and evidence |
|---|---|
| Human authorization | Actual explicit task/scope authorization; exception decisions resolved; no revoked or conflicting authority; canonical reference |
| Specification | Committed frozen artifact, exact version/SHA/path; actual Human freeze authorization for that identity |
| Implementation | Real Git final SHA, correct authorized base, branch/PR/repository; inspect complete diff and file scope |
| CI | Actual provider run/check identity and SUCCESS on that exact final SHA for every required check; pending/failing/cancelled/unknown blocks |
| Review policy | Explicit Human/task-spec required streams; no risk-class shortcut; unclear policy blocks; Phase F pilot always requires both streams |
| Security, when required | Canonical immutable Security artifact; independent reviewer/session/model attribution, exact spec/base/final SHA, read-only declaration, PASS and no unresolved blocking finding |
| Quality, when required | Canonical immutable Quality artifact with the same identities/checks; independently authored from Security; PASS and no unresolved blocking finding |
| Independence | Reviewer not Implementer; Security and Quality use independent identities/sessions and do not consume each other's verdict as proof; tracked reviewer implementation writes block PASS |
| Fresh PR/branch state | Correct repository/PR, OPEN and mergeable, exact reviewed head and base, no newer implementation commit/conflict; perform fresh remote fetch/API check immediately before merge |
| Scope / confidentiality | No unauthorized diff, secret/confidential exposure, unresolved blocker or AGENTS.md §19 stop condition |
| Platform | Required repository controls satisfied; a denied operation is not bypassed through another tool/API/CLI |

Use content hashes and stable source locators where applicable. A hash checks
bytes, not author identity. Preserve original report content and attribution.
If external review storage is mutable (for example PR comments), preserve the
original hash-bound report and recheck its content/current applicability; a
comment is not a cryptographic signature or immutable-by-platform assertion.
Do not invent a GitHub-native APPROVE under the Implementer identity.

An independent PASS and CI SUCCESS are necessary evidence, not automatic merge
permission. The external procedure must satisfy every current governance and
platform gate. Normal merge may use the exact expected head as a concurrency
guard. If head/spec changes, do not merge: obtain new applicable CI/reviews and
repeat the full preflight. Never force/rewrite history or substitute an older PASS.

## B3 boundary and terminology

This external/manual strategy is outside B3's trusted-adapter computation. MCP
remains an operational index of recorded claims. B3 authoritative_merge_eligible
remains false; accepted authoritative verifier adapters remain unavailable.
The integration owner can exercise current governance's conditional merge
authority only after the external checks, even though that MCP field stays false.
Neither provisional_ready nor a caller-supplied VERIFIED field grants permission.
No B1/B2/B3 runtime/schema or source-policy change is made by Phase E.

Existing MCP state/merge-gate responses may retain their installation-era
workflow_v2_governance: NOT ACTIVATED diagnostic. That hardcoded field is not a
global activation verifier or the source of workflow selection. Operators must
report the canonical marker/main/activation record separately and expose this
limitation. Do not rewrite the B3 result or claim the server enforces this marker.
The existing admin command does not automatically read/enforce the marker;
the procedural preflight is mandatory. Any future runtime wiring needs separate
authorization and review; it is not a prerequisite silently added to this task.

RECORDED != VERIFIED.
provisional_ready != authoritative_merge_eligible.
MCP state != authenticated external truth.
model_profile != authenticated identity.
review PASS != CI PASS.
CI PASS != review PASS.
review PASS + CI PASS != automatic merge permission.

## Post-merge verification and closeout

After a real merge, fetch and verify merged=true, exact merge SHA/main, reviewed
SHA ancestry and the expected diff/tree. Inspect CI generated for the exact main
merge SHA and wait for any required run. Do not invent a run or reuse branch CI as
main CI. A missing run must be reported/evaluated against active governance; a
required failure stops closeout. For Phase E activation closeout, verify the
exact resulting main merge SHA and record it durably as the activation commit,
with review, approval, PR/main CI and observed enabled state. Do not claim active
V2 before these accepted checks. Synchronize README/operational status honestly.

## Rollback / disable

1. Obtain a separately reviewed Human-authorized governance change setting this
   marker enabled=false; verify the disable commit on main before new admission.
2. Stop NEW V2 enrollment. Do not assign/start new V2 work through a stale policy
   observation; rerun external preflight for each proposed admission/action.
3. Preserve all V2 rows, specs, assignments, reviews, CI, verification chains and
   Git artifacts. No database deletion/reset/restore-over-history or fake backfill.
4. Checkpoint in-progress V2 work. Human decides whether it finishes under V2 or
   is stopped and explicitly reauthorized/restarted under V1. No silent translation.
5. Unenrolled/new tasks use the approved V1 path if their authorization permits;
   historical V1 evidence remains unchanged. Safe reads/checkpoints/handoffs remain.
6. Preserve the immutable activation commit and disable history. Re-enable requires
   a separately reviewed governance decision; toggling policy does not refresh
   stale CI/reviews or migrate history.

## Focused validation and limits

```text
python tools/validate_workflow_v2_governance.py
python -m unittest discover -s tests -p test_workflow_v2_governance.py -v
```

The validator reads the bounded YAML marker and governance text. Its pure scenario
helpers test explicitly SYNTHETIC policy/activation/enrollment/evidence packets.
Checklist completeness is not authoritative verification, approval, enrollment,
activation or merge permission. It makes no API/Git network/provider call, writes
no operational state and does not run the admin command. Real preflight remains
the external/manual procedure above. Existing CI collects the focused tests.

## Version history

| Old | New | Date | Author | Change / reason | Breaking change |
|---|---|---|---|---|---|
| None | 1.0.0 | 2026-10-07 | Codex | Human E-01–E-06; initial external/manual authority, admission and rollback procedure | Yes — conditional governance activation; no runtime/API change |
