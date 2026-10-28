# CI-V2-003 — Artifact storage optimization specification

| Field | Current revision |
| --- | --- |
| Version / previous version | 0.2.0 / 0.1.0 |
| Date / task / author | 2026-10-28 / AIIP-CI-STORAGE-ROADMAP-20261028 REVISION 2 / Codex |
| Authorization | Human attachment AIIP-CI-STORAGE-ROADMAP-20261028 REVISION 2, planning and documentation only |
| Implementation status | PLANNED / NOT AUTHORIZED; this revision changes documentation only |
| Dependencies | Verified storage recovery; review of this specification; separate Human implementation authorization; existing required CI and governance |
| Security / compatibility | Preserve mandatory security evidence, exact-head reviews and existing required CI contract; no runtime or workflow change |
| Breaking change | No — documentation only; any future status-contract migration needs separate authorization |
| Provenance | Original 0.1.0 from planning commit `88be84bdcf900c48adc2323a7e34d9095ae833c1`, reproduced below without editing |

Revision summary: Clarify artifact budgets, provenance, account metrics and warning thresholds.

## Revision 0.2.0 — 2026-10-28: budgets, evidence and account monitoring

The ordinary success goal is **below 1 MB uploaded per run** and ordinary functional failure **below 5 MB**. These are aspirational measurements, not gates that truncate required evidence. Preserve full required security audit/tree/lint archives and every required acceptance/review artifact. Upload optional visual diagnostics only when required; an explicitly justified full-visual mode retains the complete evidence required for review, even above the target. Capture functional results before tail uploads; an upload-only failure stays blocking when mandatory and must not itself cause optional diagnostic uploads. Missing mandatory evidence fails closed. Two-day retention is proposed only when compatible with review and custody; preserve longer-required and protected evidence. No automatic protected deletion or paid storage is authorized.

A future evidence manifest should identify repository, exact commit/tree, workflow, run ID, attempt, producer, selection reason, artifact name/ID, SHA-256 over explicitly identified archive and/or payload bytes, retention, functional and upload outcome, and measured raw and actual uploaded bytes. Differentiate GitHub artifact digests from independently computed SHA-256 and state precisely which bytes were hashed. If a value is unavailable, mark UNKNOWN rather than infer it. Verify delivered bytes against the recorded digest and exact run. Preserve required archives if compacting cannot meet a target.

### Proposed account-aware monitoring

Use verified, appropriately scoped account/billing metrics, timestamp and measurement period; repo artifact lists alone cannot establish account allowance or recoverability. Report separately: current retained artifact bytes; cumulative billed GB-hours (and billing-period average/allowance if supplied by GitHub); Actions cache; workflow logs; GitHub Packages; and any account-level usage or inaccessible categories. Confirm each service's actual allowance/billing relationship from current authoritative GitHub account evidence; do not assume all categories share one quota. Treat stale, incomplete or inaccessible metrics as UNKNOWN, not zero or recovered.

| Verified applicable account utilization | Proposed response |
| --- | --- |
| 60% | Early warning and record trend/source. |
| 80% | Restrict discretionary QA uploads; do not suppress mandatory visual or security evidence. |
| 90% | Freeze nonessential runs and assess capacity; required gates remain required, not waived. |

Thresholds are a proposed operational policy, not an implemented monitor, automatic deletion, billing change or CI exception. Capacity recovery requires positive account-side and/or authorized successful upload evidence as appropriate; nominal retained-byte reductions or elapsed time alone do not prove it. See [roadmap](../operations/CI_STORAGE_PREVENTION_ROADMAP.md).

## Preserved original specification 0.1.0

The following historical text is preserved verbatim; its metadata and handoff describe the 2026-10-21 revision, not the current revision.

# CI-V2-003 — Artifact storage optimization specification

| Field | Value |
| --- | --- |
| Version / date / author | 0.1.0 / 2026-10-21 Asia/Saigon / Codex |
| Status | DRAFT SPECIFICATION ONLY — no deletion or retention-policy change executed |
| Owner / reviewer | Human Product Owner / Gemini 3.8 Flash High, Antigravity STRICT READ-ONLY, pending |
| Authorization | Human “TASK: AI-IP CI-V2 — GitHub Actions Optimization”, 2026-10-21, specification/planning scope |
| Baseline | `7abc63e12e18a8027de1d4be4c71ad7aa182cb91` |
| Relationship | Separate from CI-V2-001 PR #144; coordinate future tier selection with CI-V2-002 |

History: none → 0.1.0, 2026-10-21, Codex, proposed storage design. Breaking
change: **No implementation**. Targets cannot delete or truncate mandatory evidence.

## Artifact policy

| Run/evidence class | Proposed policy | Design target |
| --- | --- | --- |
| Ordinary success | Mandatory `dep-001-security` audit/tree/lint evidence plus compact provenance/result manifest; omit optional screenshots, documents and traces | Prefer <1 MB total uploaded |
| Ordinary functional failure | Small allowlisted diagnostics from affected producers; logs, error metadata and relevant failed-test captures; keep mandatory security evidence complete | Prefer <5 MB total uploaded |
| Artifact upload failure only | Preserve blocking upload result and summary; no extra optional uploads triggered solely by that failure | No diagnostic cascade |
| Full visual/review evidence | Required synthetic PDF/DOCX, layout pages and browser captures when rendering risk, review or AC requires them; record justification and expected files | Explicitly exempt justified full evidence from ordinary targets |

All upload steps follow functional execution. Required security delivery failures
remain blocking and missing required files remain errors. Optional absence is
distinct from producer failure; it cannot become false acceptance. Capture the
functional result before uploads; classify functional failure and upload failure
separately. No blanket suppression, automatic quota retry loop or required-evidence
deletion. Size targets are monitoring goals, not acceptance/security waivers.

Playwright should retain failed-test screenshots and failure/retry traces only
where applicable, with an explicit manual/full-visual override. Reporters must
keep exact failed test, project and retry identity; conditional retention must
not drop captures required by review. LibreOffice/PDF/DOCX QA still executes
when required; ordinary success uploads compact measurement JSON rather than
repeated full-page PNGs or all generated binaries. Retain full originals when AC
or review needs visual inspection. Synthetic content only; no source research.

Public patent reference calibration keeps its required measurements/checks.
Consider immutable content-addressed reuse of the two approved public PDFs and
derived measurement outputs keyed by reference hashes, pinned QA tools, script
version and expected measurement contract. Validate hashes before reuse; on a
miss fetch only approved URLs and validate, failing closed on mismatch. A cache
must not substitute stale measurements or trust PR-writable evidence. Do not
upload PDFs/repeated page images on ordinary successful runs. No new service is
approved; exact cache/integrity implementation requires separate review.

Two-day retention is the default only where compatible with existing evidence
requirements (baseline archives already use it). Evidence needing durable review
must remain available through the accepted review/closeout process; document
exceptions and acceptance before changing retention. This spec cannot shorten
protected historical evidence or infer that Git receipts contain artifact bytes.

## Cleanup and reporting

Keep `.github/workflows/qa-artifact-cleanup.yml` manually dispatched on main,
dry-run by default, explicitly allowlisted, age-bounded and serialized. Preserve
the pruner's protected main/PR successful-run evidence, failed-run artifacts,
security/unknown-name artifacts and incomplete/unverifiable metadata. Inspect
the current reviewed script before execution; do not broaden allowlists or run
deletion under this planning authorization. Existing cleanup tests must pass.

Produce a job summary containing exact SHA/run/attempt, functional and upload
results, artifact name/ID/size/digest/retention, selection reason and local raw
versus uploaded compressed bytes. Required evidence missing must be obvious.
Report nominal nonexpired artifact totals through paginated read-only Actions
metadata; distinguish repository totals from account billing, caches and logs.
Alert in the run summary/check output when targets exceed budget or uploads hit
quota; external messaging/schedules/billing changes require separate approval.
Do not claim quota recovery from deleted nominal bytes or elapsed time alone.

Historical preparation references (~46.6 MB successful QA artifacts, 193 deleted
allowlisted artifacts/~2.98 GB) are not new measurements. Predecessor CI-V2-001
run 39594108615 still reported storage quota failure. Fresh successful uploads,
exact artifact metadata and, where needed, actual billing/storage observations
are required to establish recovery. No current success-size saving is claimed.

## Verification and rollout gates

1. Record comparable successful/failed/manual-visual baseline manifests and bytes.
2. Verify success omits optional heavy outputs; functional failure selects only
   relevant diagnostics; upload-only failure selects none; full review mode keeps
   required visual files. Exercise cancellation/missing producer/missing evidence.
3. Prove full/prod security audits, tree and lint evidence remain complete and
   blocking; exact SHA provenance retained, no secret/source content uploaded.
4. Re-run cleanup safety tests and read-only dry-run planning; no protected deletion.
5. Independently review exact implementation SHA; full required CI and fresh
   uploaded artifact inspection; normal merge/postmerge verification and status
   closeout. No repeated CI reruns while quota remains blocked.

Rollback any later implementation through a reviewed ordinary revert, restoring
prior upload payload/retention without history rewrite. Deleted bytes cannot be
recovered by Git revert; this is why cleanup is separately controlled. AI budget
USD 0, no real research, Render/deploy/public API, Claims runtime, active SQLite,
billing increase or automatic maintenance execution.

## Handoff

Task ID: CI-V2-003. Agent: Codex, specification author. Reviewer: Gemini 3.8
Flash High / Antigravity STRICT READ-ONLY, pending. Status: DRAFT SPECIFICATION.
Version: 0.1.0. Work completed: retention, evidence, diagnostics, reference reuse,
cleanup and measurement design. Files affected: this specification only. Evidence
checked: baseline archives/pruner/tests and quota failure logs. Findings: targets
unmeasured; quota recovery unverified. Decisions: planning only. Issues: separate
implementation review/authorization, evidence-retention exceptions if necessary.
Security impact: mandatory audit/review evidence preserved; no deletion executed.
Recommended next action: review this policy before separately scoped implementation.
