# README-REFRESH-001 — Professional Project README

| Field | Value |
|---|---|
| Version / date / author | 1.0.0 / 2026-10-21 Asia/Saigon / Codex |
| Status | IN PROGRESS — documentation candidate; independent review, CI and merge pending |
| Owner / reviewer | Human Product Owner / Gemini 3.8 Flash High, Antigravity STRICT READ-ONLY |
| Authorization | Human task attachment “README-REFRESH-001 — Professional Project README”, 2026-10-21; later instruction: names in English, functional descriptions in Vietnamese |
| Workflow | V1; no V2 enrollment or MCP state invented |
| Baseline | `7abc63e12e18a8027de1d4be4c71ad7aa182cb91` |
| Branch | `docs/readme-professional-refresh` |
| Scope | README.md and this governance-required task record only |
| Resume | `RESUME-AIIP-README-001` |

History: none → 1.0.0, 2026-10-21, Codex: replace lengthy README presentation
with an executive overview, preserve evidence and record editorial maintenance.
Breaking change: **No**; application, CI, tests, policy and releases unchanged.

## Editorial result

README keeps the original VNUHCM Innovation Hub image, English project/component
names, headings and status labels. Explanatory prose is Vietnamese, following the
Human's later instruction overriding the original English-primary request.
The overview separates implemented offline components, mocked provider adapters,
public synthetic demonstration, Draft development and unfunded live validation.
It retains a compact Project status table, funding table, production requirements,
working local setup commands, documentation and maintenance guidance.

The original presentation is preserved in the
[immutable baseline README](https://github.com/nshaokiet/ai-ip-description-generator/blob/7abc63e12e18a8027de1d4be4c71ad7aa182cb91/README.md).
Existing task records, decision logs, Control Center and Review Log remain
byte-identical to baseline. Removing repeated timelines from README neither
deletes those records nor declares old open closeouts completed.

## Evidence audit

| README subject | Source and observed boundary |
|---|---|
| Local/synthetic MVP | PROJECT_CONTEXT.md; docs/system-specification.md; existing parsing, provider adapters, Human review, offline test and rendering records. Adapter code exists; live-model behavior remains unverified. |
| Invention/USPTO/Claims/rendering | PREAPI-001-zero-cost-readiness.md inventory; P2-002…P2-007 and AI-CONV task records; components are merged, product v2 integration and product Claims remain disabled. |
| PREAPI-A/B | Merged main records; Issue #133 is actually CLOSED despite stale planning wording in its body/old README. No open implementation blocker invented. Parent #131 remains OPEN. |
| PREAPI-C1 | PR #139 MERGED at current main; source custody default-off, same-process and synthetic-only. Postmerge CI #39555439292 failed at artifact upload; closeout not completed. |
| PREAPI-C2 | PR #140 OPEN/DRAFT, head 0b46eea63679380cff0d93d2864f04238738a7fd; specification only. CI #39545978861 FAILURE. PR #143 decision package proposes options; no frozen architecture/implementation acceptance inferred. |
| PREAPI-D | PR #141 OPEN/DRAFT, head 91cfdeeb49f7ba341e7700ad967e2646940430fd; no-client/no-egress checker candidate, local results separately reported; CI #39546171580 FAILURE. Not on main or live entitlement proof. |
| PREAPI-E | PR #142 OPEN/DRAFT, head 03f696b77b6cbbed3c03f584846653eae9f4b5c1; fixture readiness checker only; CI #39546255007 FAILURE. Fixture evaluation is not model semantic acceptance. |
| CI-V2-001 | PR #144 stays OPEN/DRAFT at 43e07dfa36b217066647af23f2dda2c6c715bd0c. Human-supplied Gemini code/architecture PASS recorded; CI #39595590479 FAILURE due to mandatory security upload quota after functional SUCCESS. No #144 change is part of this task. |
| CI-V2-002/003 | Separate planning branch docs/ci-v2-002-003-planning, commit 88be84bdcf900c48adc2323a7e34d9095ae833c1; two specifications, no architecture/storage implementation approval. |
| Governance/integration | PR #143 OPEN/DRAFT at df2eacba73ad8d0ce580e7ed83933af4f0484fe8; exact-head CI #39558639521 FAILURE. Older Control Center/README lifecycle text is not a current completion verdict. |
| Latest roadmap/pilot preparation | Inspected PR #143 roadmap v0.1.3, C2 decision package v0.1.0 and funded-pilot checklist v0.1.0. These remain unmerged proposals; README links #143 as Draft alongside the existing main roadmap. |
| Funding/production | Issue #131, EVAL-001 and BLK-003: AI budget USD 0, no accepted live product results, model entitlement/prices unverified; separate provider/model/budget/data/pilot approval required. No exact cost or mandatory paid hosting inferred. |
| Local development | tools/local_dev.py and P1-004 runbook: launcher does not call provider or enable the orchestration API; existing Python 3.12/Node 24+/npm setup commands retained. Not a fresh install verification. |

## Governance compatibility

The existing validator `tools/validate_workflow_v2_governance.py` requires the exact
README heading `Conditional project adoption (Phase G)`, 17 policy rows, historical
D/E milestone phrases, `MANUAL / EXTERNAL` and the V1 preservation declaration.
Removing or translating those machine-checked values would change governance or
fail existing tests, outside this documentation-only scope.

Keep that contract unchanged in a collapsed `Governance Compatibility` section.
The English policy values and one immutable activation SHA are intentional narrow
exceptions to Vietnamese explanatory prose and removal of verbose SHA lists.
The wrapper explicitly distinguishes the retained Phase G declarations from the
current product status. No Phase G closure, routing, enrollment or identity claim
is added. No policy validator, test or other canonical file is modified.

## Acceptance and validation

| AC | Evidence / remaining gate |
|---|---|
| 01 | Concise overview, small tables, collapsed compatibility detail; exact final line/byte counts in PR checkpoint. |
| 02–03 | Source audit above separates merged components, Draft candidates, planned specifications and pending closeout; no Draft implementation counted completed. |
| 04–05 | USD 0 and unknown entitlement/prices, no accepted live/semantic evidence, separate GitHub storage blocker, production/data/Claims limits explicit. |
| 06 | Original logo and demo URL, repository-relative links and existing setup retained; link/Markdown results and limitations in checkpoint. |
| 07 | Existing canonical docs unchanged; prior README available at immutable Git baseline. |
| 08 | Exactly README.md plus this task record; source/tests/workflows untouched. |
| 09 | Independent exact-final-SHA Gemini review and required CI remain mandatory; no automatic merge or CI waiver from this document. |
| 10 | Maintenance policy below; detailed histories stay in canonical records. |

Run read-only Markdown structure/link/UTF-8 checks and the real governance validator
and relevant existing governance regression tests. No new test dependencies or
tests are introduced for prose. Do not claim a fresh application install, live
provider smoke, model entitlement, full rendered visual certification or complete
CI success from document checks. Publish actual results against immutable head.

Final local verification: README **284 → 143 lines**, UTF-8 bytes **41,555 →
10,567** (about 75% smaller); 11 unique English headings, consistent tables,
balanced code fences/details, valid UTF-8 and all **9 relative links/image** PASS.
Original logo path/alt retained; public demo HTTP HEAD **200**. GitHub PR/tree
targets were inspected through authenticated repository tools; localhost setup
URLs were not probed and no new install/server or provider run is claimed.
`git diff --check` PASS. Governance validator PASS and existing
`tests/test_workflow_v2_governance.py` **38 passed** under Python 3.12.10.
The initial governance test run had **37 passed / 1 failed** because Phase E
markers were inside the removable Phase G section; moving those unchanged
markers before that heading resolved the regression without source/test changes.
These are static Markdown checks, not a markdownlint or browser-render claim.

MCP returns `Unknown task: README-REFRESH-001` — **BLOCKED BY TOOL CAPABILITY**;
no registration, lease or approval is fabricated. No connected tool to execute
the specified Gemini/Antigravity review is available in this session; publish an
exact-SHA review handoff for the external environment. Earlier CI task review
does not cover this documentation commit.

## Maintenance policy

- Update README when an accepted feature completes, an active workstream changes
  materially, a planned task receives authorization, a major blocker is resolved,
  AI funding is approved or a provider pilot completes.
- Keep English names/headings/status labels and Vietnamese descriptions unless
  Human gives a later preference. Keep the required Project status summary.
- Put minor commits, reruns, review comments, exact hashes and interim checkpoints
  in task records, PR receipts or Control Center; do not append README timelines.
- Preserve the machine-checked governance declaration until a separately approved
  policy/validator migration. Inspect README edits in open PRs #143/#144 before
  future integration; reconcile overlapping rows without dropping current status.
- The next steps are proposed priorities; they do not authorize implementation,
  provider spend, public API, Claims, confidential data, SQLite migration or deploy.

## Review, merge and rollback

Gemini 3.8 Flash High / Antigravity STRICT READ-ONLY must review the exact final
head and both changed files against this source audit and Human language update.
Verify policy equivalence, current status, Draft/merged distinctions, funding and
legal limits, setup and valid links. Return actual model/profile/session and reuse,
inspected SHA/files, commands/results, findings and PASS/REQUEST CHANGES/BLOCKED.
Never transfer #144's PASS or confuse author document checks with independent review.

Keep the dedicated PR Draft while review or required CI is missing/failed. The
unchanged baseline CI may still fail at artifact quota; no workflow change, repeated
rerun, exception or merge is authorized to bypass that gate. Only all AGENTS.md
conditions permit normal expected-head merge, exact-main CI verification and
evidence-backed task closeout. Reconcile this README with any later overlapping PR
before merge; changed final content requires applicable fresh review and CI.

Rollback via a normal reviewed revert PR from current main, reverting the actual
verified documentation merge while preserving unrelated later changes and history.
Do not force/reset main or overwrite the README from an old tree blindly.

## Handoff

```text
Task ID: README-REFRESH-001
Agent: Codex — documentation implementer, Workflow V1
Reviewer: Gemini 3.8 Flash High / Antigravity STRICT READ-ONLY, pending
Status: IN PROGRESS — Draft candidate, not merged or completed
Version: 1.0.0; immutable head and PR in external checkpoint
Work completed: README overview, scoped evidence audit and maintenance policy.
Files affected: README.md; docs/tasks/README-REFRESH-001-professional-readme.md.
Evidence checked: Current main, complete prior README, AGENTS/context/system spec, task/control records, live PR/CI states, latest Draft roadmap/pilot checklist and local launcher.
Findings: Artifact quota blocks related CI; canonical roadmap/Control Center contain historical states; governance text contract must remain.
Decisions: Human authorizes documentation only; later instruction selects English names and Vietnamese descriptions.
Issues: Independent final-head review, required CI and postmerge verification pending; MCP task unknown.
Security impact: No code, CI, provider, data, billing, deployment or policy changes.
Recommended next action: Review both files on final SHA; inspect required CI without quota retry loops; merge/closeout only after all gates pass.
```
