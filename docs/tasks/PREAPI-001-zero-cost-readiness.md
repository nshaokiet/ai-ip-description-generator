# PREAPI-001 — Zero-cost API Readiness and Offline Product Integration

| Field | Value |
|---|---|
| Task | PREAPI-001 / Issue #131 |
| Specification | v0.1.1 DRAFT — independent review and Human freeze pending |
| Initial baseline | f3e9994ffa255600ceeaffc1d4d7640140aba1fb (PR #130 merged) |
| Workflow | V1; Codex implementation, Gemini 3.8 Flash High/Antigravity STRICT READ-ONLY review |
| Authorization | HUMAN-PREAPI-001-ZERO-COST-PREPARATION-2026-10-19; preparation and Draft PR only |
| Allowed cost | USD 0 provider spend; live-provider calls 0 |
| Data | Synthetic and provenance-verified public/open-license test material only; no confidential/unpublished inputs |
| Merge | NOT AUTHORIZED for this Draft or any subsequent implementation |

Version note: v0.1.1 (2026-10-19, Codex) corrects the v1 client-supplied revision/source-binding limitation in the proposed offline tests; v0.1.0 remains in Git history. No runtime contract or authorization changes.

## 1. Product objective and non-claims

Prepare the current repo to be one independently approved, budget-capped provider smoke away from initial **AI API validation**, without enabling real-paper usage or treating offline mock output as model-quality evidence. Actual production readiness, legal filing readiness and full public v2 access are separate decisions.

**Do not conflate:** (A) API adapter tests with mock output, (B) local v1 pipeline integration, (C) offline source-grounded USPTO v2 generation, (D) isolated Candidate A v2 proof-of-contract, (E) public synthetic demo, and (F) a live-provider, real-paper product workflow. Completion of A–E does not prove F.

## 2. Verified source inventory

| Capability | Current location/evidence | Runtime boundary / gap |
|---|---|---|
| PDF/DOCX upload, parsing and source units | backend/app/main.py, backend/app/api/routes/documents.py, backend/app/services/document_parsing.py | App routes available; does not imply live provider conversion |
| AI extraction | backend/app/services/extraction_runtime.py, tests/backend/test_extraction_runtime.py | OpenAI Responses client exists; no verified funded live smoke |
| AI draft | backend/app/services/draft_runtime.py, tests/backend/test_draft_runtime.py | Provider integration mocked; real model validation unproven |
| Internal v1 pipeline | backend/app/services/core_pipeline.py and tests/backend/test_core_pipeline_e2e_offline.py | Local HTTP router in main.py only if AI_IP_ENABLE_LOCAL_ORCHESTRATION_API is explicitly enabled; default OFF |
| USPTO v2 components | invention_reconstruction.py; uspto_specification_generation.py; supported_draft_claims_generation.py; uspto_document_package.py; uspto_offline_renderer.py | Standalone deterministic offline modules validated with synthetic data, not fully wired to product v1 API |
| Offline v2 session/revision | uspto_offline_orchestration.py, tests/backend/test_uspto_offline_orchestration.py | Internal service, not registered as public FastAPI route |
| Claims semantic authority | synthetic_claims_authority_v1.py | Additive synthetic-only authority overlay, not product Claims enablement; positive METHOD/PROCESS/COMPOSITION disabled |
| Candidate A v2 API | backend/app/api/local_synthetic_v2.py, tests/backend/test_local_synthetic_v2_api.py | Exactly isolated, trusted same-process GET contract; default OFF, not a public browser/proxy API |
| Synthetic export demo | backend/app/demo_staging.py; uspto_synthetic_delivery.py; frontend/src/components/SyntheticUSPTOExports.tsx | Fixed demo fixture and four synthetic files; arbitrary user upload is unrelated |
| EVAL-001 corpus and scorer | eval/semantic/v1/gold (six Human-accepted cases), eval/semantic/v1/tools | 154 gold items, 102 KEY/52 SECONDARY; zero accepted product-runtime runs; semantic quality NOT_DETERMINED |
| CI | .github/workflows/ci.yml, PR #130 postmerge run #39186953039 | At baseline, exact-main push run SUCCESS: both mcp-tests (152/152) and build-and-test |

## 3. Feature flags and hard defaults

| Flag / setting | Safe value until separate approval |
|---|---|
| RUN_OPENAI_LIVE_TESTS | 0 |
| RUN_OPENAI_DRAFT_LIVE_TESTS | 0 |
| AI_IP_ENABLE_LOCAL_ORCHESTRATION_API | 0 by default; local isolated synthetic test may explicitly use fake runtimes when approved |
| AI_IP_ENABLE_LOCAL_SYNTHETIC_V2_API | 0 by default; not an externally available endpoint |
| OPENAI_API_KEY | Empty/not required for free mock tests; never log or commit keys |
| Provider model | Current backend/app/core/config.py selects gpt-5.6-sol/high; actual API account/model availability UNVERIFIED |
| Render backend and frontend | Auto-Deploy OFF, preview OFF; no deployment is authorized |
| MCP PROJECT_ORCH_DB | Never point an upgraded Store at active state without separate Human-approved backup/migration |

## 4. No-cost work packages (each code package requires separately scoped Human approval)

### PREAPI-001-A — Documentation and contract audit (authorized for a Draft PR)

- Trace the real schema/contract edges from the parser envelope through AI-001, v1 draft, v2 reconstruction/specification/Claims/package and renderer. Specify exact inputs and evidence indices; do not assume synthetic demo samples represent arbitrary uploads.
- Build source-file-to-test-case coverage matrix. Mark unimplemented/unsupported transitions, schemas, Human confirmation boundaries, absent provider metadata and proof-of-provenance requirements.
- Preserve released seven-input P2-005/P2-006 validation: source_envelope, structured_analysis, reconstruction, specification, p2_003_generation_config, supported_claims and p2_004_generation_config. The validator must re-read all seven originals; package digest alone is not rendering authority.
- Produce docs-only spec; no changes to application, runtime, workflows or flags. Independent fixed-SHA review and Human freeze/merge remain separate.

### PREAPI-001-B — Mock-backed full v1 E2E (future implementation authorization)

- Reuse existing APP-003 and local-orchestration API with explicit fake Extraction and Draft runtimes. Synthetic PDF and DOCX fixtures only.
- Assert local upload/parse → AI-001-compatible structured analysis → draft → source/grounding validation → DOCX v1 generation and download, actual bytes, no provider/network calls.
- Cover wrong document ID, expired/invalid sources, refused/incomplete fake provider, schema mismatch, unsafe path, cleanup failure, missing evidence, **mismatched** cross-document analysis/draft and safe/log-redacted errors. Do not claim v1 rejects a self-consistent foreign analysis/draft pair: its validate/export requests are client-supplied and have no server-held upload/session binding. Record that residual gap for PREAPI-C1, not a test-only v1 fix.
- CI must prove strict defaults and v1 regression. No live provider, no background export, no schema mutation.

### PREAPI-001-C — Offline USPTO v2 product adapter and UI (future contract + implementation approvals)

- Split first into frozen v2 API/UI contract and then implementation; identify exact gap between internal OfflineUSPTOOrchestrator, Candidate A synthetic-only GETs and product-facing review/export.
- Add only Human-approved, local, opt-in, synthetic-offline flow; preserve existing v1 endpoints and default flag OFF. No public v2 route or browser activation without a separate access/security decision.
- Exercise synthetic APP-002 envelope+validated analysis → P2-002 → P2-003 → P2-004 → P2-005 → P2-006 via retained seven originals. Assert immutable source binding, revisions/digests, Human confirmation and four expected PDF/DOCX files.
- Frontend review must distinguish missing/unsupported Claims from valid, and never claim filing-ready status. No unsupported Claims promotion.

### PREAPI-001-D — Provider API dry-run readiness harness (future implementation authorization)

- Default mode must be PURE OFFLINE and fail closed: no OpenAI client instantiation with transport, no network request, even if an API key happens to exist in the developer environment.
- Check installed SDK/schema compatibility, prompt/schema determinism, typed request envelope, model ID syntax and configured output/token/time limits. Model API entitlement and response capability must be labelled UNVERIFIED until paid/authorized live run.
- Check only whether key is PRESENT/ABSENT without printing value, length, prefix or fingerprint; redact prompts/source/provider response/absolute paths from public logs.
- Define an explicit opt-in, separately authorized future live smoke command with a strict case count, hard per-run and aggregate USD budget, max token use, timeout, refusal/error taxonomy and STOP switch. Merely setting OPENAI_API_KEY must never enable live testing.
- Emit machine-readable readiness report with explicit READY_FOR_AUTHORIZED_PROVIDER_SMOKE vs BLOCKED statuses and evidence references. A READY status cannot mean live-provider smoke passed.

### PREAPI-001-E — EVAL-001 and operational dry-run (future implementation authorization)

- Wire pre-existing six Human-accepted EVAL-001 gold packages to mock/fixture scoring to verify scoring/report pipelines without falsely introducing PRODUCT_RUNTIME evidence.
- Assert simulated outputs never count toward product-runtime acceptance and semantic quality remains NOT_DETERMINED / DEFERRED until real authorized provider execution.
- Prepare separate MCP schema-v4 active-db rollout plan only (backup consistency, restore rehearsal on disposable copy, rollback, writer-stop and explicit Human gate). No live DB access or migration.

## 5. Acceptance criteria for readiness specification

| AC | Acceptance |
|---|---|
| PRE-01 | Two distinct documented pipelines (v1 provider adapter and offline USPTO v2), with actual source-file and test links |
| PRE-02 | Every model/provider call currently deferred and every offline/mock path explicitly distinguished |
| PRE-03 | Current default-off flags and zero-cost/zero-live-call controls preserved |
| PRE-04 | All missing API/frontend/Claims integration seams and separately gated authorization decisions enumerated |
| PRE-05 | Strict seven-input provenance and unsupported Claims fail-closed gates identified |
| PRE-06 | Mock E2E and six-gold-score integration test plans include negative tests and pass/fail evidence without API spend |
| PRE-07 | Future smoke runbook specifies model entitlement check, safe API key handling, spending cap, input licensing, refusal/failure reporting and stop controls |
| PRE-08 | Dependencies, exact commands and no-fee go/no-go exit checklist allow repeatable follow-up Codex Draft PRs |

## 6. Planned test inventory and repeatable checks

Targeted backend suites include: tests/backend/test_extraction_runtime.py, test_draft_runtime.py, test_core_pipeline_e2e_offline.py, test_local_orchestration_api.py, test_uspto_offline_orchestration.py, test_local_synthetic_v2_api.py, test_supported_draft_claims_v1.py, test_uspto_offline_renderer.py. Repo-wide: python -m pytest tests -q -p no:cacheprovider, frontend lint/typecheck/build/E2E in CI; MCP npm test runs in dedicated main/PR CI. Exact commands should be refined against scripts and runtime environment before execution.

All tests run with live flags 0, mock provider transport and disposable DBs only; test failures must not be masked. At handoff, report actual test counts, hashes and skipped tests. The presence of tests is not evidence they all passed in a new run.

## 7. Future funded pilot gate (NOT authorized now)

Human separately decides provider/platform, actual API model ID, OpenAI API billing account, max USD spend and max calls, allowed open-access/synthetic inputs, API key injection, whether APP-003 v1 and/or USPTO v2 are in scope, and reviewer/evaluation acceptance criteria. First run minimal synthetic Extraction+Draft smoke, then one full E2E, then the six EVAL-001 cases if budget permits. Record exact model/config/prompt/source/output hashes, errors/usage, latency and source licensing. Provider failures or quality findings require mitigation and another decision; do not infer general validity.

## 8. Explicit STOP boundaries

No paid provider/network calls; no use of user's real/confidential/unpublished papers; no Render rollout; no public endpoint; no production auth/tenant/storage change; no Claims product activation; no MCP active database migration; no fabricated MCP leases/tasks; no changes to AGENTS.md, frozen contracts or branch protection. Every new code change remains a separate Draft PR under Workflow V1 fixed-SHA Gemini independent review followed by explicit Human merge approval.

**Current task status:** SPECIFICATION DRAFT / ZERO COST / CODE IMPLEMENTATION NOT STARTED / NO MERGE AUTHORIZATION. This is a roadmap specification, not a verified live AI test.


## 9. Source-verified acceptance matrix (audit addendum, 2026-10-19)

This audit is based on existing source/test paths. **Presence of regression tests is not new test execution or proof that this PR has passed.** Target missing integration seams instead of implementing the existing positive cases again.

| Boundary | Existing code/tests | Already covered | Incremental gap |
|---|---|---|---|
| PDF/DOCX → evidence | backend/app/api/routes/documents.py; backend/app/services/document_parsing.py; tests/backend/test_document_upload.py; test_document_parsing.py | Validation, source-unit preparation | Explicit no-provider, cross-document and expiry/replay negative integration evidence |
| Evidence → AI-001 extraction | backend/app/services/extraction_runtime.py; tests/backend/test_extraction_runtime.py | Mock Responses client, schema/grounding errors, refusal, timeout, safe logs | Explicit forbidden-provider transport tripwire across full E2E |
| AI-001 → draft | backend/app/services/draft_runtime.py; tests/backend/test_draft_runtime.py | Mocked provider contract, business validation, refusal, incomplete | Assert metadata consistency and zero provider invocation; server-side identity for a self-consistent foreign pair is absent in v1 |
| Upload → v1 draft → DOCX | tests/backend/test_core_pipeline_e2e_offline.py; test_local_orchestration_api.py; tests/e2e/offline_backend.py; frontend/e2e/integration.spec.ts | Existing real HTTP PDF/DOCX, review, revision digest, export, cleanup, retry and errors | Add only missing failures and provider-egress proof; v1 revision digest is not server-side source/session custody |
| v2 source → P2-002 through P2-006 | backend/app/services/uspto_offline_orchestration.py; tests/backend/test_uspto_offline_orchestration.py | Seven retained originals, revision/digest tamper, document splice rejection and cleanup | Product integration of arbitrary newly uploaded *synthetic* source, Human review and gated exports |
| Candidate A v2 API | backend/app/api/local_synthetic_v2.py; tests/backend/test_local_synthetic_v2_api.py | In-process two-GET, capability scopes, strict default OFF | No released public/product upload API; must freeze separate API/UX contract |
| Four USPTO files/demo | backend/app/services/uspto_offline_renderer.py; tests/backend/test_uspto_offline_renderer.py; backend/app/services/uspto_synthetic_delivery.py; tests/backend/test_uspto_synthetic_delivery.py; frontend/e2e-demo/uspto-exports.spec.ts | Four files from verified synthetic sources or fixed demo | Upload-linked provenance-based export and authorization boundary absent |
| EVAL-001 | eval/semantic/v1/tools/evaluator.py; tests/eval/test_semantic_evaluator.py; eval/semantic/v1/reports/framework-status.json | Scoring engine and blocked framework status | Fixture harness only, never substitute for PRODUCT_RUNTIME results |

### 9.1 Critical safety correction: live-test flags do not prevent all runtime calls

The two RUN_OPENAI_*_LIVE_TESTS flags in backend/app/core/config.py default to OFF, but backend/app/main.py wires real OpenAIExtractionRuntime and OpenAIDraftRuntime into the opt-in local processing router when the caller does not explicitly inject fakes. Thus **setting live-test flags to 0 does not make an arbitrary running local processing application provider-safe**.

PREAPI-B/D must require all of the following:

1. Create only a test application with explicit fake Extraction and Draft runtimes (see tests/e2e/offline_backend.py); unset OPENAI_API_KEY in the isolated test process, including when the host had a key.
2. Prove an unexpected provider-client construction, SDK request or non-loopback product network access fails the test. Local loopback connections used by Playwright are allowed; external package installs/CI fixture downloads are unrelated to product provider calls.
3. Assert provider-call count = **0** across success, malformed input, refusal, retry, cleanup and browser flow. Mark all outputs as MOCK/SYNTHETIC; mock results do not establish semantic quality.
4. Never use logging-only detection or a hidden environment toggle as a safety control. Fail the test/job on an unapproved request.

Current configuration limits are **48,000 extraction** and **64,000 draft output tokens**, with **2 retries per stage**; these maxima are *not* a USD budget cap. Future paid pilot must derive and enforce a worst-case cap including both stages, retry policy and exact provider pricing. The actual availability of configured model gpt-5.6-sol is unverified. Do not silently modify frozen production settings to claim readiness.

### 9.2 Repeatable targeted offline commands

Run from repo root after installing Python 3.12 and pinned requirements. These invoke existing unit/offline suites, **not** the live tests; commands are source-observed but have NOT been executed in this audit.

~~~bash
export RUN_OPENAI_LIVE_TESTS=0 RUN_OPENAI_DRAFT_LIVE_TESTS=0
unset OPENAI_API_KEY
python -m pytest tests/backend/test_extraction_runtime.py \
  tests/backend/test_draft_runtime.py \
  tests/backend/test_core_pipeline_e2e_offline.py \
  tests/backend/test_local_orchestration_api.py \
  tests/backend/test_uspto_offline_orchestration.py \
  tests/backend/test_local_synthetic_v2_api.py \
  tests/backend/test_uspto_offline_renderer.py \
  tests/backend/test_uspto_synthetic_delivery.py \
  tests/eval/test_semantic_evaluator.py \
  -q -p no:cacheprovider
~~~

Existing full CI uses python -m pytest tests -q -p no:cacheprovider. MCP CI independently runs npm ci, npm run typecheck, npm run build, npm test with a disposable absolute PROJECT_ORCH_DB below RUNNER_TEMP; frontend scripts include lint, typecheck, build, test:e2e. For frontend Playwright, use its configured test servers/dependencies: merely typing npm run test:e2e does not guarantee a test server is running.

The existing framework command python eval/semantic/v1/tools/evaluator.py may rewrite tracked reports. Run it in a disposable checkout and inspect the diff. Correct no-provider outcome is BLOCKED_FOR_PRODUCT_RUNTIME_EVIDENCE / NOT_DETERMINED with 6 accepted gold cases and zero accepted product runs.

## 10. Bounded next task sequence / stop conditions

| Stage | Separate Human approval required before source code | Deliverable | STOP if |
|---|---|---|---|
| PREAPI-B incremental mock v1 E2E | Yes | Provider tripwire and only uncovered negative cases, actual test logs and no-live-call proof | Real client request, secrets, unexpected source/schema mutation |
| PREAPI-C1 v2 product API and UI contract | Contract review and freeze | Local auth/session/data-flow boundary distinct from Candidate A; HTTP route/UX specification | Any unapproved public route, browser bearer transport, Claims promotion |
| PREAPI-C2 v2 synthetic product adapter/UI | Yes, after C1 freeze | Synthetic uploaded source linked to all seven originals, immutable revision/Human gate, four exports and cleanup | Package-only renderer, foreign evidence, unsupported Claims, deployment |
| PREAPI-D dry-run harness | Yes | Default-fail-closed CLI/readiness report, key PRESENT/ABSENT only, no provider network and budget-cap design | Real model discovery/call, model entitlement asserted without evidence, leaked key/source |
| PREAPI-E EVAL-001 audit | Yes | Synthetic fixture scoring validation with unchanged product-runtime NOT_DETERMINED status | Mock outputs labelled as product runtime, altered gold, actual DB migration |

**Future funded gate, not part of this authorization:** approve real API provider/model availability, billed account, licensed test corpus, explicit max USD/call/token/retry budgets, secure key injection, response safety and provider kill switch. ChatGPT/Codex subscription access is not API billing proof. Keep BLK-003 and confidential-source restrictions. Distinguish OFFLINE_READY after separate approved workstreams from LIVE_PROVIDER_VALIDATED only after a later authorized live run.

## 11. Postmerge-governance and exact-head CI checkpoint (2026-10-19)

- GOV-MCP-CI-001 [Issue #129](https://github.com/nshaokiet/ai-ip-description-generator/issues/129) is **CLOSED / COMPLETED** after successful guarded merge and direct final-main CI verification; it is not an active-database rollout. [Issue #126](https://github.com/nshaokiet/ai-ip-description-generator/issues/126) remains **OPEN**.
- PREAPI-001 Draft [PR #132](https://github.com/nshaokiet/ai-ip-description-generator/pull/132) was independently read back at prior HEAD `3d695ea08bcee006d187e6bfb227486af2240dce`. [Exact-HEAD PR CI #39189309087](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/39189309087) **COMPLETED/SUCCESS**: `mcp-tests` 7/7 steps; `build-and-test` 34/34 steps. These are CI results, **not** external Gemini spec approval.
- **After this documentation addendum, review and CI must use its new HEAD**; no stale reviewed-head or old-CI success may substitute. As of this checkpoint, **no PR #132 independent review submission or thread was found**. Status remains Draft/unmerged, no Human freeze/merge permission.

## 12. Critical v1-to-v2 boundary contract — preliminary, NOT FROZEN

**Source observation:** `backend/app/services/core_pipeline.py` constructs its validated extraction envelope inside `run_pipeline` and calls `_cleanup_source(document_id)` in `finally`; its public `PipelineResult` exposes `analysis`, `draft` and `metadata`, **not the original full validated envelope**. The opt-in `/api/documents/{document_id}/process` response similarly returns analysis/draft/metadata. Therefore **do not infer that a v1 processing response is sufficient for a later USPTO v2 run**. Re-reading a cleaned-up upload or synthesizing a lookalike envelope from `analysis` is forbidden.

PREAPI-C1 must design a new **trusted, local, opt-in, synthetic-only** orchestration boundary with these invariants, subject to independent contract review and later Human approval:

1. **Atomic intake / evidence custody:** within one trusted process, validate the uploaded synthetic PDF/DOCX into `ExtractionInputEnvelope`; bind immutable document ID, source SHA-256, evidence units/IDs and canonical envelope digest. Preserve the canonical envelope alongside matching validated `structured_analysis` **before** cleanup. If any stage fails, discard retained state and clean original/output files.
2. **Provenance consistency:** prove analysis belongs to the same source and that citations/evidence IDs resolve against that saved envelope. Foreign, missing or duplicated evidence, changed document ID/hash, missing originals or noncanonical JSON must fail closed; do not substitute a fixed demo fixture for a newly uploaded source. The current v1 `/api/drafts/validate` and `/api/exports/docx` accept client-supplied analysis/draft/revision data; their `draft_digest` hashes only revision ID and draft, not a retained server-side source/session. A self-consistent foreign pair can therefore satisfy internal validation without proving custody of the uploaded source. C1 must specify a distinct trusted server-side binding before product v2 export; PREAPI-B must report this as an unclosed v1 boundary, not claim to fix it with tests alone.
3. **Offline stages:** pass saved envelope and analysis plus separately validated P2-003 and P2-004 configs into `OfflineUSPTOOrchestrator.start_session`; advance through reconstruction, specification, supported-draft-Claims authority, package and optional render. Revalidate all `PROVENANCE_KEYS` (`source_envelope`, `structured_analysis`, `reconstruction`, `specification`, `p2_003_generation_config`, `supported_claims`, `p2_004_generation_config`) before download. Do not use a package digest as standalone authority.
4. **Review and revision:** bind session ID, revision and opaque revision token to source digest and all seven originals. Any changed source, analysis, configs or draft invalidates downstream package and export, requiring recomputation and an explicit Human review checkpoint. A claims-empty result stays `CLAIMS_REVIEW_REQUIRED`/Human confirmation; never infer patentability or promote unsupported positive Claims.
5. **Transport/security:** the existing `backend/app/api/local_synthetic_v2.py` provides two isolated trusted same-process GET operations and capabilities, and `backend/app/main.py` does **not** import or mount it. PREAPI-C1 must **not** silently expose that bearer capability or any new browser/public endpoint. First define an independent trust boundary, authentication, retention/expiry, safe error mapping and session ownership before any route/UI implementation.
6. **Artifacts:** successful synthetic v2 render must deliver **four** manifest-bound output files (PDF/DOCX pairs) with sizes and SHA-256; downloads must be current-revision and session-bound, returned with safe filenames, appropriate media types, `no-store`, and post-download/expiry cleanup. Filename/path must never select arbitrary host files.

**C1 proposed check cases (implementation NOT AUTHORIZED):** V2-01 synthetic PDF; V2-02 synthetic DOCX; V2-03 foreign document or evidence splice; V2-04 original envelope absent after cleanup; V2-05 tampered config or stale revision; V2-06 ungrounded analysis; V2-07 unsupported Claims state; V2-08 package-only render attempt; V2-09 cross-session/export path traversal; V2-10 interrupted render/cleanup. For each case capture the source digest, outcome code, seven-key verification verdict, number of outputs (0 or 4), and **provider calls = 0**, without recording raw source or private paths.

## 13. Provider-free PREAPI-B/D executable-test specification

Existing `tests/e2e/offline_backend.py` already builds `create_app(..., extraction_runtime=SyntheticDemoExtractionRuntime(), draft_runtime=SyntheticDemoDraftRuntime())`; `frontend/playwright.config.ts` launches its local test backend and Next server via Playwright `webServer`. PREAPI-B should reuse this composition and strengthen **negative coverage**, not replace functioning positive E2E tests.

A new test-only isolation harness must: (a) clear provider credential from the subprocess environment; (b) inject explicit fake runtimes into every processing test app; (c) intercept/deny unexpected provider SDK construction and outbound network access during actual product test execution, allowing only loopback as required; (d) count attempted calls and fail the test if nonzero; (e) verify the test process cannot silently fall back to real runtime when a fake is absent; (f) reuse PDF and DOCX success and target uncovered schema/refusal/error/retry, **mismatched** cross-document substitution, no-source cleanup and output cleanup; (g) emit redacted machine evidence with immutable test SHA and exact counts. A self-consistent foreign analysis/draft pair is a documented v1 custody gap, not a PREAPI-B pass assertion or authorization to change production behavior.

**Explicit risk:** the two `RUN_OPENAI_*_LIVE_TESTS=0` switches control opt-in live tests only. Merely unsetting `OPENAI_API_KEY` or hiding errors is **not** a complete network-deny mechanism. Interception must cover all actual product execution paths. CI dependencies and public patent-reference downloads in the existing workflow are **external connections** but are not paid model/provider calls; therefore report `provider_api_requests=0` separately from broad `total_network_requests`.

Proposed PREAPI-D default-off report fields (schema design only, no generated result yet):

~~~json
{
  "report_version": "preapi-1",
  "mode": "OFFLINE_ONLY",
  "candidate_git_sha": "<exact test commit>",
  "provider_api_requests": 0,
  "provider_client_attempts": 0,
  "synthetic_v1_e2e": "NOT_RUN",
  "synthetic_v2_e2e": "NOT_IMPLEMENTED",
  "source_binding": "NOT_VERIFIED",
  "seven_input_validation": "NOT_VERIFIED",
  "evaluator_product_runtime": "NOT_DETERMINED",
  "model_entitlement": "UNVERIFIED",
  "credential_status": "ABSENT_OR_NOT_INSPECTED",
  "readiness": "BLOCKED_PENDING_IMPLEMENTATION"
}
~~~

An offline harness may become `READY_FOR_AUTHORIZED_PROVIDER_SMOKE` only once its **own** offline criteria truly pass; it must never assert `LIVE_PROVIDER_VALIDATED` or `EVAL_ACCEPTED`. Real provider capability and access cannot be inferred from an SDK import, a model-like string or a ChatGPT subscription. The future live opt-in must require a **separate Human decision plus a bounded request count, token budget, timeout/retry policy and enforced USD cap**, with a fail-closed STOP switch; amount and model pricing require current verification at authorization time.

## 14. Remaining readiness gates and implementation ownership

| Gate | Required evidence | Status on this Draft |
|---|---|---|
| A specification | Source inventory, v1/v2 provenance and reviewable offline plan | **DRAFT**, not frozen or merged |
| A exact-head CI | Both jobs green for final doc HEAD | **MUST RECHECK AFTER THIS COMMIT** |
| A independent review | Gemini fixed-SHA strict read-only report including actual session/model/findings | **PENDING**, cannot self-certify |
| A Human freeze/merge | Separate explicit approval | **NOT AUTHORIZED** |
| B code | Offline network/provider tripwire and incremental v1 E2E | **NOT STARTED; independent approval required** |
| C1 then C2 | Frozen trusted synthetic-v2 product contract; gated adapter/UI and four-file export | **NOT STARTED; independent approvals required** |
| D code | Fail-closed offline readiness CLI and machine report | **NOT STARTED; independent approval required** |
| E code | Six accepted-gold fixture validation without product-runtime claims | **NOT STARTED; independent approval required** |
| Future paid pilot | Separate provider/account/model, lawful sources, USD/call/token cap, key handling and rollback approval | **BLOCKED / SPEND USD 0** |

When handing off to Antigravity for independent PREAPI-A review, ask the reviewer to examine Sections 9–14 against **actual main source**, challenge the mandatory source-envelope custody issue, verify safety boundaries, exact PR diff and fresh CI head. No edits, approvals by inference, paid API calls, deployment or active SQLite access during review.
