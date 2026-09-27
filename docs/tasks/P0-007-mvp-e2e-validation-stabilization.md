# P0-007 — MVP End-to-End Validation & Stabilization Specification

## Metadata and change history

| Field | Value |
|---|---|
| Task ID | P0-007 |
| Specification version | 0.1.0 |
| Status | Approved specification v0.1.0; implementation READY FOR INDEPENDENT IMPLEMENTATION REVIEW — not merged or closed |
| Implementation evidence revision | 0.1.1; technical specification remains v0.1.0 |
| Owner / decision authority | Human / Product Owner |
| Author | Codex |
| Proposed independent reviewer | Antigravity Reviewer Agent; record the exact model/profile actually used when review occurs |
| Date | 27/09/2026 |
| Baseline | `main` at `403deba9d33d1cc20c3d231bc08fa473420505ed` |
| Source of truth | This Git specification, subject to independent review and Human approval |
| Confidentiality | Internal; fixtures synthetic only |

| From | To | Date | Author | Change | Reason | Related task/decision | Breaking change |
|---|---|---|---|---|---|---|---|
| None | 0.1.0 | 27/09/2026 | Codex | Define evidence-based MVP E2E validation and stabilization gates | Specify the next task without implementing it or expanding product scope | P0-007; APP-003, P0-003, P0-004, P0-005, P0-006; BLK-003 | No |
| 0.1.0 | 0.1.1 evidence addendum | 27/09/2026 | Codex | Record approved specification review, Human implementation approval, offline test results and AC-01…AC-16 implementation evidence | Handoff for independent implementation review; no technical requirement change | P0-007; specification `f98cf600f47a6559175c10dc3498846a7ae4395b`; implementation `2638c620a36e6fb4016ed2efaeb788446a5b2eff` | No |

## 1. Purpose and current-state baseline

Validate the **already-merged local MVP path** from one synthetic text PDF or DOCX through upload, parsing/evidence, offline extraction, validated analysis, draft generation, browser review/revision, authoritative backend validation and DOCX export. Stabilization means repairing defects found against approved contracts and protecting the path with proportionate regression evidence. This is a validation specification, not permission to implement P0-007, release the MVP or process real research data.

APP-003, P0-005 and P0-006 are Completed/CLOSED; GOV-P0-006-01 is RESOLVED. BLK-003 remains OPEN. The runtime model/provider remains the existing approved configuration, but P0-007 acceptance needs **no paid/provider call**: synthetic fixtures and injected offline/fake extraction and draft runtimes exercise the real local application boundaries. Such a run verifies wiring and deterministic contracts, **not** the semantic quality or availability of a live model. Human review remains required; session `REVIEWED` is not formal approval.

## 2. Scope

In scope: verify PDF and DOCX flows; cross-layer canonical data preservation; edit/revision/validation/export binding; safe negative paths; cleanup; keyboard and narrow-screen usability; deterministic offline regression; reproducible local commands; redacted defect triage and known-limitations handoff. Reuse the existing tests first. Add or strengthen a test only where section 5 identifies a material integration/regression gap. Fixes, if later approved, must be limited to defects in this existing workflow and must preserve released contracts.

Out of scope: authentication, database or durable persistence, cloud/private production storage, deployment infrastructure, OCR/scanned-PDF support, Claims, prior-art work, patentability scoring, new schema/prompt/template versions, new AI model/provider policy, post-analysis title generation/selection, unrelated frontend redesign, formal Human approval/audit state, and real/confidential research data. Do not turn P0-007 into a feature task. Any needed change across these boundaries requires a separate Human decision and versioned plan.

## 3. Dependencies and fixed merged baselines

| Dependency | Fixed evidence | Boundary for P0-007 |
|---|---|---|
| APP-003 internal pipeline | Implementation `3e7c2910695eed9e5ef1d7d0ff11f8f0e3ac6c38`; merge `b5a47f6030441b438e7e1745b75b05d8b345d6c0` | Offline PDF/DOCX to validated draft JSON; source cleanup. Merge message reports 32/32 AC and independent Antigravity PASS; exact underlying profile not evidenced. |
| P0-003 DOCX integration | Merge `5cfb1b5d0377fcb4538a2bba0bbb48232001b123` | Existing backend pipeline-to-DOCX integration; no new renderer contract. |
| P0-004 local HTTP boundary | Merge `43737a79fcdb634a12a92752c767df9fbf98d1f3` | Existing opt-in local metadata/process/export API, not production auth. |
| P0-005 frontend MVP | Final accepted SHA `43907213f14c8c55294f55af34afcc0cbcc9dc66`; CLOSED | Existing upload/results/responsive foundation. |
| P0-006 frontend/backend integration | Accepted implementation `0f1e94db438869a980db8a1cb1e06956de2d8d3e`; merge `3207479e5cca73da3e7facbc7c482d2ce5eba2b9`; CLOSED | Session-only revisions, backend validation, exact-revision export, six offline Playwright tests. |
| Governance baseline | `403deba9d33d1cc20c3d231bc08fa473420505ed` | APP-003 reconciliation merged; GOV-P0-006-01 RESOLVED; BLK-003 OPEN. |
| Released contracts | AI-001 Output Schema v1.0.0, AI-003 Patent Draft Contract v1.0.0, DOC-001 template v1.0.0; APP-001/002 and AI-RUNTIME-001/002 | No contract, provider, security-policy or technical requirement revision in this specification. |

`docs/system-specification.md` contains older implementation-state prose; current merged code and the task/governance evidence above take precedence for this P0-007 baseline. P0-007 must not silently treat that historical prose as proof the current workflow is absent, nor broaden this task into a system-specification rewrite.

## 4. End-to-end workflow under test

```text
Synthetic text PDF/DOCX
  -> APP-001 secure local upload and safe metadata
  -> APP-002 deterministic parsing, source units, locators and evidence IDs
  -> APP-003 orchestration using injected offline extraction/draft runtimes
  -> canonical validated structured analysis and Patent Draft JSON
  -> P0-006 browser display, immutable in-memory revision and local review status
  -> backend-authoritative validation of exact revision against original analysis
  -> backend revalidation, existing DOCX rendering and browser download
  -> source and temporary export cleanup
```

The offline runtimes return synthetic oracle payloads; they do not demonstrate that a real provider extracted the facts from the PDF/DOCX. Verify actual parser locators and document identity separately from fixture-provided semantic content. A generated draft without a selected title remains visibly `MISSING`; no title-selection feature is implied.

## 5. Existing coverage and incremental test matrix

“Reuse” denotes an existing test to retain in the P0-007 evidence pack, not a claim that it has been rerun in this specification task. “Gap” is a proposed P0-007 validation delta; do not duplicate existing assertions merely to increase test count.

| Scenario | Existing coverage to reuse | Material P0-007 gap / required oracle |
|---|---|---|
| PDF happy path | `test_core_pipeline_e2e_offline.py::test_pdf_document_reaches_validated_draft_json_offline`, `test_pipeline_docx_integration.py::test_synthetic_pdf_pipeline_renders_editable_docx_offline`, PDF Playwright case in `frontend/e2e/integration.spec.ts` | Cross-layer downloaded DOCX content must be checked against the UI-selected edited revision, not only request JSON/filename or a separate backend fixture. |
| DOCX happy path | Corresponding DOCX tests in the two backend modules and the DOCX Playwright case | Strengthen browser-level downloaded DOCX content/notice verification for edited DOCX input; reuse existing upload/process/validate assertions. |
| Invalid/corrupt input | `test_document_upload.py` covers zero/multiple, oversize, scanned, encrypted, corrupt PDF/DOCX and type mismatch | One representative browser upload rejection and recovery check, without replaying every backend validation case. No fake successful process/export. |
| Missing-information draft | `test_draft_business_validation.py`, `test_patent_docx_renderer.py::test_missing_marker_and_author_questions_are_preserved`, Playwright missing-title display | One synthetic non-title MISSING case through browser result and downloaded DOCX; retain marker, related author question and no invented prose. Cover unresolved conflict/inference as an invariant using existing fixtures where possible. |
| Edited draft validation | `test_local_orchestration_api.py::test_validate_edited_revision_returns_exact_digest_and_unverified_paths`, PDF/DOCX Playwright cases | Reuse; verify selected revision/digest and unverified prose warning are in the final evidence pack. |
| Invalid edited draft rejection | `test_validate_rejects_schema_business_source_and_pointer_failures`, `test_validate_rejects_protected_change_and_abstract_count_errors`, invalid-edit Playwright case | Reuse; no new negative test unless a discovered defect lacks an existing oracle. |
| Exact-revision DOCX export | `test_export_requires_exact_validated_revision_and_revalidates`, `test_export_returns_editable_docx_and_removes_temporary_file`, PDF browser request-body check | Inspect the downloaded DOCX from the browser run for selected revision prose, absence of older/unsaved text, and unchanged disclaimer/required markers. |
| Network/backend-safe errors | Backend 404/422/409/500/504 tests; Playwright non-JSON and aborted-network validation case | Add a small browser failure/retry matrix for upload or process and export, because existing browser fault injection targets validation only. Preserve revision and avoid raw payload/path/false download. |
| Source cleanup | `test_core_pipeline.py` success/failure/exception cases, `test_core_pipeline_e2e_offline.py` source deletion, local API process failure test | Reuse with both formats and failure paths; only add case if a discovered cross-layer path escapes these checks. |
| Temporary DOCX cleanup | `test_export_returns_editable_docx_and_removes_temporary_file`, `test_export_internal_failure_is_generic_and_cleans_partial_output` | Reuse; verify clean export directory after browser-download/failure run if not already observable through existing backend tests. |
| Keyboard flow | Playwright keyboard-only edit/validate/review/export case | Reuse; add a keyboard-operated upload entry check and verify focus remains discoverable after injected failure/retry, because the existing test sets the file programmatically. |
| Narrow viewport | Playwright 390×844 case, width and warning/validation/export assertions | Reuse; check any changed error/missing-information view at the same viewport. |
| Session-only revision behavior | PDF Playwright cancel, immutable history, review reset and reload loss; `draftRevisions.ts` | Reuse; regression-check that no localStorage/IndexedDB or server-side revision persistence is introduced. |

## 6. Cross-layer contract and invariant checks

Trace the same synthetic document through response, selected revision, validation request/result, export request and rendered DOCX where the field is renderable. Assert identity or intentional projection, not byte equality across unrelated representations.

| Invariant | Required check |
|---|---|
| Document metadata | Opaque document ID, file type/name and checksum-related safe metadata remain consistent across upload, analysis and draft `source_document`; no local path or secret reaches browser/logs. |
| Evidence IDs and locators | APP-002 source units/evidence IDs remain stable, unique and resolvable in analysis and draft grounding/appendix; no ID is invented by UI edit. |
| Source paths | Technical paragraph paths resolve against the original analysis; edit only changes allowed prose. Bad pointer/evidence closure fails backend validation and export. |
| `output_notice` | Full canonical notice survives process -> revision -> export; draft/renderer retain draft/Human-review/non-legal/non-filing semantics. |
| Drawings | Canonical `drawings` state survives the frontend round trip and existing DOCX mapping; no generated figure or approval is invented. |
| `MISSING`, conflict, inference | Missing marker and author-question links remain; conflict stays `UNRESOLVED` with both sides/evidence; inference is visibly labeled, never promoted to `SOURCE_FACT`. |
| Title behavior | No selected candidate means canonical `MISSING` title and `[AUTHOR CONFIRMATION REQUIRED]`; no arbitrary UI title edit or generated title. |
| Revision/review boundary | New prose revision invalidates its own validation and starts `UNREVIEWED`; review records are session-only and outside canonical AI JSON. Export binds exact selected revision ID and digest; `REVIEWED` is not legal/technical approval. |

Reuse `test_document_parsing.py`, `test_draft_business_validation.py`, `test_patent_docx_renderer.py`, `test_local_orchestration_api.py` and existing Playwright checks as the field-level oracles. Add a cross-layer assertion only where these independent tests do not prove preservation end-to-end.

## 7. Regression strategy and reproducible commands

Run targeted affected tests during stabilization, then one full offline backend regression and the complete six-case-or-expanded browser suite at the final implementation SHA. Do not quote historical counts as new results. Record command, OS/Python/Node versions, SHA, pass/skip/fail totals, duration, and approved exceptions. Keep old tests; change them only for a justified oracle gap. No dependency or test framework addition is approved here.

From the repository root, with the existing Python 3.12 environment and test dependencies installed:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/backend/test_document_upload.py tests/backend/test_document_parsing.py tests/backend/test_core_pipeline.py tests/backend/test_core_pipeline_e2e_offline.py tests/backend/test_pipeline_docx_integration.py tests/backend/test_local_orchestration_api.py tests/backend/test_patent_docx_renderer.py tests/backend/test_draft_business_validation.py tests/docx/test_patent_docx_template_v1.py -q -p no:cacheprovider
.\.venv\Scripts\python.exe -m pytest tests -q -p no:cacheprovider
```

From `frontend/`, with installed pinned dependencies, Chromium and a built Next.js app:

```powershell
npm run lint
npm run build
npm run test:e2e
```

Before Playwright, verify ports **8000** and **3106** are free or demonstrably owned by this run's synthetic backend and frontend. `frontend/playwright.config.ts` currently has `reuseExistingServer: true`; a generic pre-existing backend on 8000 must **not** be reused. The P0-007 implementation must enforce this precondition or fail closed. Do not point this suite at a real-provider backend. Do not set `RUN_OPENAI_LIVE_TESTS=1`; do not use an API credential for acceptance.

## 8. Security and privacy checks

- Synthetic fixtures only. Verify no real paper, PII, credential, full prompt/response, local path or generated sensitive document is committed or exposed in error/log/browser artifacts. Use existing synthetic fixture inventory and `test_patent_docx_template_v1.py::test_fixtures_are_synthetic_and_have_no_secret_or_pii` as one oracle, not the sole privacy proof.
- The local opt-in API flag is **not** authentication. BLK-003 still blocks real/unpublished data and production use. Confirm disabled-flag route absence and no browser-visible API key or backend configuration.
- Fail closed on invalid upload, source mismatch, invalid pointer/evidence, stale digest, renderer error and non-JSON/network failure; correlation ID may be shown when available, never raw server detail.
- Verify uploaded source and temporary DOCX files are removed on success/failure according to existing local lifecycle; report an unconfirmed cleanup result honestly, without promising deletion when it failed.
- The browser E2E harness must prove it uses injected fake runtimes and no provider client/call. Network blocking in a browser page alone does not prove the backend made no provider call.

## 9. Local performance and stability checks

At the final P0-007 implementation SHA, repeat both synthetic PDF and DOCX offline flows at least three times in a fresh local test environment. Each run must finish under the existing explicit test timeouts, produce one valid response/download or a classified safe failure, and leave no unexpected source/temporary export file. Record per-stage and total duration from safe operational metadata, plus max/median observed time; this is a local regression baseline, **not** a production SLA. A timeout, hang, nondeterministic contract change or accumulated temporary file is a defect to triage. Do not add paid calls, performance infrastructure, or arbitrary throughput targets.

## 10. Offline/synthetic test requirements

Reuse `tests/e2e/offline_backend.py`, `tests/backend/test_document_parsing.py` synthetic file builders and existing canonical fixtures. Inject `SyntheticExtractionRuntime` and `SyntheticDraftRuntime` or equivalent approved fakes into the real FastAPI app. Keep real upload, parser, validation, session UI and DOCX renderer boundaries; do not stub the entire HTTP response in the happy path. Browser routing may inject specific network/proxy failures for negative cases. Explicitly report what the fake runtime cannot establish: semantic source entailment, live provider availability, cost, latency and model conformance. Fixture text must remain synthetic and unidentifiable.

## 11. Failure triage and stabilization rules

For each failure capture task ID, fixed SHA, synthetic fixture ID, command, environment, stage, expected/actual safe result, redacted correlation ID, reproduction rate and proposed minimal fix. Classify as: **blocking** if an approved flow fails, contracts/evidence are corrupted, backend validation is bypassed, wrong revision is exported, sensitive data leaks, cleanup fails without honest state, a provider is called, or keyboard/narrow flow becomes unusable; **non-blocking** only for defects that do not affect those gates and have a documented Human disposition. Do not mark a failed/untested AC PASS. Fix within the current contracts, rerun affected targets, then final regression. Escalate any schema/prompt/template/model/security/scope change to Human before implementation. Preserve findings and review history rather than rewriting them.

## 12. Objective acceptance criteria

| ID | Pass oracle |
|---|---|
| AC-01 | The test harness is proven synthetic/offline, refuses an unidentified pre-existing backend on ports 8000/3106, makes zero provider/API calls, and uses no confidential fixture. |
| AC-02 | A synthetic text PDF completes upload -> parse/evidence -> validated analysis -> draft -> browser edit/review -> backend validation -> DOCX download; response, selected revision and downloaded file are checked. |
| AC-03 | The same complete flow passes for synthetic DOCX input, including edited downloaded DOCX content. |
| AC-04 | Invalid/corrupt/unsupported input is rejected by existing backend validation and a representative browser case shows a safe recoverable error with no process/export success. |
| AC-05 | Document metadata, evidence IDs, source paths, `output_notice`, drawings and canonical notices survive all applicable layer boundaries or fail authoritative validation if tampered. |
| AC-06 | A missing-information draft keeps non-title missing marker/question links, unresolved conflict/inference labels where present, and a missing title remains missing without invented prose/title. |
| AC-07 | Saving/editing creates distinct immutable session revisions; a new revision is unvalidated and `UNREVIEWED`, old revision remains selectable, and reload discards state without durable persistence. |
| AC-08 | Backend canonical/business/grounding and abstract-count validation is authoritative; invalid or unsupported edited draft and protected-field/source changes cannot pass by client assertion. |
| AC-09 | DOCX export binds the exact selected revision ID, digest and content, revalidates before rendering, rejects stale/invalid/unsaved substitutions, and downloaded content excludes older text. |
| AC-10 | Upload/process/validation/export failures produce safe classified UX or HTTP errors, preserve retryable session state, expose correlation ID when available, and create no false success/download or sensitive disclosure. |
| AC-11 | Existing tests and any necessary incremental check prove source cleanup and temporary DOCX cleanup on success/failure for the covered local paths; unconfirmed cleanup is reported honestly. |
| AC-12 | Keyboard-only user can upload, inspect, edit, validate, set local review status and export, with visible focus and comprehensible error/recovery state. |
| AC-13 | At 390×844 viewport, upload/results, warnings/missing state, edit/validation/review/export and representative error remain usable without horizontal page overflow. |
| AC-14 | Three repeated offline runs per input format finish under existing test timeouts, preserve deterministic business shape, and leave no unexpected source/export files; durations and environment are recorded without claiming an SLA. |
| AC-15 | Targeted affected tests, one final full offline backend regression, frontend lint/build and complete Playwright suite pass at the fixed implementation SHA; commands, totals/skips and any exceptions are reproducible and reported. |
| AC-16 | Handoff lists known limitations, any unresolved findings, fixed SHAs, exact test evidence and independent reviewer identity/profile when evidenced; BLK-003 stays OPEN and no production/live-provider/MVP-release claim is made. |

At the specification baseline these were proposed criteria, not verified results. The separately authorized implementation evidence is recorded in section 15; the AC definitions above are unchanged. An AC count of 16 follows the distinct gates above; it is not copied from P0-006. Independent implementation review and Human merge decision are still pending.

## 13. Explicit blockers and limitations

BLK-003 is **OPEN**: production authentication, private storage and retention are undecided. No real/confidential inputs or production deployment. Live provider smoke remains **NOT RUN / DEFERRED** and is not required for P0-007 offline acceptance; therefore provider behavior, semantic grounding quality and production performance remain unvalidated. Claims and title-generation workflow remain out of scope. The existing session-only UI can lose edits/review on reload or session loss; it is not audited Human approval. Synthetic oracle outputs do not prove real-paper extraction accuracy. `GOV-P0-006-01` remains RESOLVED; P0-006 remains CLOSED. This specification does not reopen either.

## 14. Historical specification-review handoff and next gate

The independent reviewer should inspect this specification against the fixed merged code/tests, check that reused coverage and proposed gaps are accurately distinguished, verify the 16 AC are objective, and report `PASS`, `REQUEST CHANGES` or Human decisions required with evidence. Record the actual Antigravity model/profile and reviewed specification SHA in the review log **only after** review occurs. No review result, implementation approval, test execution or release decision is asserted here.

```text
Task ID: P0-007
Agent: Codex (specification author)
Reviewer: Antigravity independent specification reviewer — exact model/profile to be recorded after review
Status: Draft — ready for independent specification review; implementation not started
Version: Specification 0.1.0
Work completed: Defined evidence-based validation/stabilization scope, reused coverage, incremental gaps and 16 proposed acceptance criteria.
Files affected: docs/tasks/P0-007-mvp-e2e-validation-stabilization.md; docs/operations/01_PROJECT_CONTROL_CENTER.md; PROJECT_CONTEXT.md.
Evidence checked: Merged APP-003/P0-003/P0-004/P0-005/P0-006 baselines; existing backend and Playwright test sources; no tests run for this specification.
Findings: Potential coverage gaps are proposals in section 5, not confirmed implementation defects.
Decisions: No new product, provider, schema, security or release decision made.
Issues: BLK-003 OPEN; live provider smoke deferred; synthetic-only limitations as section 13.
Security impact: No real data, provider call or code change in this specification task.
Recommended next action: ANTIGRAVITY INDEPENDENT SPECIFICATION REVIEW.
```

## 15. P0-007 implementation evidence and current handoff — 27/09/2026

This section supersedes the **lifecycle status only** in the original specification handoff. Specification v0.1.0 remains fixed at `f98cf600f47a6559175c10dc3498846a7ae4395b`. Human-supplied independent **specification** review by Google Antigravity (Advanced Agentic Coding) returned `PASS` for specification AC-01…AC-16, findings `NONE`, Human decisions required `NONE`; Human / Product Owner then approved implementation. The exact underlying model is not evidenced. This was not an independent **implementation** review.

Implementation branch: `feat/p0-007-mvp-e2e-validation-stabilization`. Pushed checkpoint `05ec10a90f11560a74e3cb2f3e7b2b33089314e1` adds browser downloaded-DOCX inspection, missing-information and failure/retry cases, keyboard upload, and fail-closed Playwright server startup. `560c41288c41786817724d12dc966fb82c87975f` adds repeated stability/cleanup evidence; `2638c620a36e6fb4016ed2efaeb788446a5b2eff` adds narrow failure, keyboard recovery and correlation-ID assertions. **Fixed implementation code SHA:** `2638c620a36e6fb4016ed2efaeb788446a5b2eff`. No production application code or released contract changed; no product defect fix was required.

Validation environment: Windows NT 10.0.26200.0, Python 3.12.10, Node v24.18.0, npm 11.16.0. Backend regression and build ran at `560c41288c41786817724d12dc966fb82c87975f`; only browser-test assertions changed afterward. Final Playwright and lint ran at code SHA `2638c620a36e6fb4016ed2efaeb788446a5b2eff`:

| Command | Actual result |
|---|---|
| Specification section 7 targeted `pytest` command | **194 passed, 1 skipped, 1 warning** in 11.39s at `560c412` |
| `.\.venv\Scripts\python.exe -m pytest tests -q -p no:cacheprovider` | **380 passed, 3 skipped, 1 warning** in 19.81s at `560c412`; no live-provider flag or API credential used |
| `frontend/`: `npm run lint` | **PASS** |
| `frontend/`: `npm run build` | **PASS** at `560c412`; no production frontend changes followed this build |
| `frontend/`: `npm run test:e2e` | **11 passed** in 56.5s at the fixed code SHA; Playwright-owned backend/frontend were started with `reuseExistingServer: false` |

The single pytest warning is Starlette's third-party `anyio.abc.BlockingPortal` deprecation. Three skips were reported in the full suite; no failed/error tests. Playwright ran outside the filesystem sandbox on Windows so it could terminate its own test server processes; the same test cases had completed inside the sandbox but teardown could not exit there. No provider client exists in the injected `tests/e2e/offline_backend.py` harness; synthetic fixture bytes only were used. This proves local wiring and contracts, not real-provider behavior or semantic source entailment.

| Criterion | Implementation evidence at fixed code SHA | Self-check |
|---|---|---|
| AC-01 | `playwright.config.ts` sets both `reuseExistingServer: false`, so occupied ports fail instead of silently reusing unidentified servers; `offline_backend.py` injects fake extraction/draft runtimes with no provider client; fixtures are synthetic. | PASS |
| AC-02 | PDF Playwright case traverses upload, process, revision edit/review, backend validation and actual downloaded DOCX; selected prose present and old/unsaved prose absent. Offline pipeline/DOCX backend tests also pass. | PASS |
| AC-03 | DOCX Playwright case exercises the same local boundary and inspects actual downloaded edited DOCX and notice. Offline DOCX pipeline tests also pass. | PASS |
| AC-04 | Existing upload regression rejects invalid/corrupt/unsupported files; browser corrupt-PDF case shows safe error, no false process/result, then valid-file retry. | PASS |
| AC-05 | PDF browser case compares canonical `output_notice` and `drawings` through export request and checks grounding/source path; backend validation and renderer tests cover document identity, evidence IDs, pointer closure and notices. | PASS |
| AC-06 | `missing-information.json` flows through browser and downloaded DOCX: non-title `missing-abstract` marker and linked author question survive, title remains `MISSING`; existing renderer tests preserve `UNRESOLVED` conflict and `INFERENCE` labels. | PASS |
| AC-07 | PDF session test checks cancel, immutable revision-1/revision-2 selection, validation reset, `UNREVIEWED` reset, local review status and reload loss. | PASS |
| AC-08 | Backend canonical/business/source/abstract validation tests pass; browser invalid edited prose fails validation and disables export. | PASS |
| AC-09 | Backend export tests reject stale digest/revision and revalidate; PDF browser export request binds revision-2 and downloaded DOCX contains only selected saved prose, not old or unsaved text. | PASS |
| AC-10 | Browser corrupt-upload, process-proxy and export failures show safe errors and recovery; failed export produces no download, preserves selected validated revision, exposes safe correlation ID; existing validation network tests cover non-JSON/abort. | PASS |
| AC-11 | Backend source/export success and failure cleanup tests pass; six browser stability runs query test-only file counts after export, each returning `source_files=0`, `export_files=0`. | PASS |
| AC-12 | Keyboard test activates file chooser using focus/Enter, supplies synthetic file without native-dialog automation, then edits, validates, reviews and exports by keyboard; corrupt-upload retry also checks keyboard-focused selection. | PASS |
| AC-13 | 390×844 browser case covers missing title/marker, edit warning, validation, export and injected error/recovery; page width stays within viewport before and during error. | PASS |
| AC-14 | Three PDF and three DOCX fresh synthetic runs each validate, download, retain deterministic section/missing/notice shape, and leave zero source/export files; stage and total durations below. | PASS |
| AC-15 | Targeted backend 194/1, full offline backend 380/3, lint/build PASS and final Playwright 11/11; commands and environment above. | PASS |
| AC-16 | This handoff records fixed SHAs, exact evidence and limitations; independent implementation review is still pending, BLK-003 OPEN, live provider smoke unvalidated, no release/production claim. | PASS |

AC-14 local total durations (milliseconds): PDF **2219, 1300, 1160** — median **1300**, max **2219**; DOCX **2066, 2155, 2120** — median **2120**, max **2155**. Per-stage `upload/process/validation/export` measurements are emitted as safe `P0-007 stability` JSON lines by the browser test. All six runs remained within existing 60-second Playwright test boundary (combined stability case 11.2s); this is not a production SLA. The test-only storage endpoint returns counts, never paths or content.

Limitations: synthetic oracle outputs do not prove real-paper extraction accuracy, semantic support of edited prose, live provider/model behavior, cost or production latency. Session edits and review status disappear on reload; `REVIEWED` is not formal Human approval. BLK-003 stays **OPEN** for production auth/private storage/retention; live-provider smoke remains **NOT RUN / DEFERRED**. No real/confidential research data or provider API call was used. P0-007 is **READY FOR INDEPENDENT IMPLEMENTATION REVIEW**, not CLOSED, merged, production-ready or MVP-released.

```text
Task ID: P0-007
Agent: Codex
Reviewer: Independent implementation review pending; specification reviewer was Google Antigravity (Advanced Agentic Coding), underlying model not evidenced.
Status: READY FOR INDEPENDENT IMPLEMENTATION REVIEW
Version: Specification v0.1.0 at f98cf600f47a6559175c10dc3498846a7ae4395b; implementation code 2638c620a36e6fb4016ed2efaeb788446a5b2eff; evidence addendum 0.1.1.
Work completed: Added only test/harness coverage for five approved gaps and six-run local stability evidence; no production code change.
Files affected: frontend/e2e/integration.spec.ts; frontend/playwright.config.ts; tests/e2e/inspect_docx.py; tests/e2e/offline_backend.py; docs/tasks/P0-007-mvp-e2e-validation-stabilization.md; docs/operations/01_PROJECT_CONTROL_CENTER.md; docs/operations/02_GEMINI_REVIEW_LOG.md; PROJECT_CONTEXT.md.
Evidence checked: Targeted backend 194 passed/1 skipped; full offline backend 380 passed/3 skipped; frontend lint/build PASS; Playwright 11 passed; PDF and DOCX stability 3/3 each with zero source/export files.
Findings: No production defect found by this implementation self-check; independent implementation review pending.
Decisions: Human approved implementation after independent specification PASS; no Human merge/release/production decision inferred.
Issues: BLK-003 OPEN; live-provider smoke NOT RUN; synthetic-only and session-only limitations as above.
Security impact: No provider API call or real/confidential input; no application, schema, prompt, template, dependency or security-policy change.
Recommended next action: ANTIGRAVITY INDEPENDENT IMPLEMENTATION REVIEW.
```
