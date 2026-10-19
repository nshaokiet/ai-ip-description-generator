# PREAPI-001 — Zero-cost API Readiness and Offline Product Integration

| Field | Value |
|---|---|
| Task | PREAPI-001 / Issue #131 |
| Specification | v0.1.0 DRAFT — independent review and Human freeze pending |
| Initial baseline | f3e9994ffa255600ceeaffc1d4d7640140aba1fb (PR #130 merged) |
| Workflow | V1; Codex implementation, Gemini 3.8 Flash High/Antigravity STRICT READ-ONLY review |
| Authorization | HUMAN-PREAPI-001-ZERO-COST-PREPARATION-2026-10-19; preparation and Draft PR only |
| Allowed cost | USD 0 provider spend; live-provider calls 0 |
| Data | Synthetic and provenance-verified public/open-license test material only; no confidential/unpublished inputs |
| Merge | NOT AUTHORIZED for this Draft or any subsequent implementation |

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
- Preserve released seven-input P2-005/P2-006 validation: source_envelope, structured_analysis, reconstruction, specification, claims, P2-003 config and P2-004 config. The validator must re-read all seven originals; package digest alone is not rendering authority.
- Produce docs-only spec; no changes to application, runtime, workflows or flags. Independent fixed-SHA review and Human freeze/merge remain separate.

### PREAPI-001-B — Mock-backed full v1 E2E (future implementation authorization)

- Reuse existing APP-003 and local-orchestration API with explicit fake Extraction and Draft runtimes. Synthetic PDF and DOCX fixtures only.
- Assert local upload/parse → AI-001-compatible structured analysis → draft → source/grounding validation → DOCX v1 generation and download, actual bytes, no provider/network calls.
- Cover wrong document ID, expired/invalid sources, refused/incomplete fake provider, schema mismatch, unsafe path, cleanup failure, missing evidence, cross-document mixup and safe/log-redacted errors.
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
