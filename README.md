<p align="center">
  <img src="frontend/public/brand/vnuhcm-innovation-hub-logo.png" alt="VNUHCM Innovation Hub" width="190" />
</p>

# AI Intellectual Property Description Generator

Evidence-grounded drafting support that helps research and innovation teams turn a scientific paper into structured invention information, a reviewable USPTO-style patent-specification draft, and an editable DOCX.

The repository combines a Next.js interface, a FastAPI processing architecture, versioned data contracts, source-linked evidence, Human review controls, validation, and deterministic synthetic tests.

> **Important:** Generated content is a draft for User and qualified intellectual-property specialist review. It is not legal advice, a patentability conclusion, an inventorship determination, a filing-ready application, or a guarantee of acceptance.

## Public Demo

**Demo:** https://ai-ip-synthetic-demo-frontend.onrender.com

The public interface supports PDF/DOCX selection. Real-paper AI conversion is not enabled yet; controlled synthetic samples remain available for the working demonstration flow. Selected arbitrary files remain in the browser UI and are not connected to synthetic results.

The deployment is non-production. Do not use real, confidential, unpublished, sensitive, or regulated research data.

## Current Status

- **P2-005:** **CLOSED / COMPLETED — MERGED (effective after this final-status reconciliation PR is independently reviewed, merged, and exact-main CI succeeds)**. V1 spec PR #96 approved; implementation reviewed `731f0064a911205e9a8ddb9de64f4fa3b65b88e2` with [Human-provided external Antigravity PASS/NONE](https://github.com/nshaokiet/ai-ip-description-generator/pull/98#issuecomment-6075865959), implementation PR #98 merged `f3dfd7d1f1e559fb537256405ceaad47ba433560` and main CI #37895226175 SUCCESS. Governance reviewed `62f54c0cf04e7720dfa08f25e31b9c14ce101e36` [external PASS/NONE](https://github.com/nshaokiet/ai-ip-description-generator/pull/99#issuecomment-6076256290), PR #99 merged `d81e2e065545b37445e85fd9322ce99510a025d2`; [exact-main CI #37897744309](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/37897744309) COMPLETED/SUCCESS; [read-back evidence receipt](https://github.com/nshaokiet/ai-ip-description-generator/pull/99#issuecomment-6076332719). MCP Unknown task: P2-005 (BLOCKED BY TOOL CAPABILITY). Offline/synthetic package only; authentic APP-002→P2-002 source chain still yields no eligible supported Claims E2E; P2-004 positive fixture proves component projection only; no verified reviewer background-test results, real-paper/provider/product-runtime/production/legal filing approval.
- **P2-004:** **CLOSED / COMPLETED — MERGED**. Specification **0.1.0 — APPROVED / MERGED**; ADR-014 accepted. Standalone `SUPPORTED_DRAFT_CLAIMS` **v1.0.0 IMPLEMENTED OFFLINE**. Independent implementation review by Gemini 3.1 Pro High / Antigravity read-only: **CLOSED — PASS / findings NONE** on `eb93bf3b47682f9091bbaaf77b7bf87d7b232ee0`; PR #82 **MERGED** at `009e1320405a8d956510c4a11a73f6626acec281` (main CI `37426892194` SUCCESS). Independent governance closeout review: **CLOSED — PASS / findings NONE**, reviewed `1ee7295fea606d3e3629c1e02c62e6fa54a21aaf`; PR #84 **MERGED** at `60dad0d463eb5f48bd0b042006aab299c07fb099`; final push/main CI `37460349940` **COMPLETED / SUCCESS** on that merge. P2-001/P2-002/P2-003 unchanged; `review_boundary.claims_runtime_implemented=false`; Claims runtime integration **NOT ENABLED**; no provider/API, real/confidential data or production approval. MCP **BLOCKED BY TOOL CAPABILITY — Unknown task: P2-004**. This final-status reconciliation requires its own independent fixed-SHA governance review before its PR may merge; downstream work **NOT AUTHORIZED**.
- **P2-003:** **CLOSED / COMPLETED — MERGED**. Specification 0.1.1 APPROVED / MERGED; contract blocker RESOLVED. Human-supplied external Gemini 3.1 Pro High / Antigravity read-only implementation PASS / findings NONE, AC-01…AC-41 and provenance A–H PASS, complete diff 9/9 reviewed on `acc0ddcaa1fa533f7426133bec2963bea12aa5b2`; PR #77 merge `1702547ae06a59c990f9264223d2ff07131265cc`; main CI `37197774777` SUCCESS. Governance closeout PASS / findings NONE, 4/4 docs reviewed on `e97b5cbda4b69b7cbb8524f99b0c1a27f10e19c7`; PR #78 merge `e61b69358fba68ccc109fb5b76081d2685d96bce`; final closeout main CI `37200160782` SUCCESS. Reviews are not GitHub-native approval. MCP: BLOCKED BY TOOL CAPABILITY — Unknown task: P2-003. Arbitrary real-paper conversion NOT ENABLED, semantic acceptance NOT DETERMINED, real/confidential data NOT AUTHORIZED, P2-003 Claims output remains `MISSING` / `[]` and `review_boundary.claims_runtime_implemented = false`; production NOT APPROVED / NOT PERFORMED. P2-004 implementation is tracked separately and does not change P2-003 semantics.
- **P2-002:** CLOSED / COMPLETED — MERGED. The strict `INVENTION_RECONSTRUCTION` v1.0.0 contract and deterministic offline APP-002 + AI-001 pipeline received Human-supplied Gemini 3.1 Pro High / Antigravity implementation PASS/NONE, AC-01…AC-34 PASS, on `62a43da07fc4ccd60c9dab0da188388f6cab88e2`; PR #71 merged at `7d295165379dfa3aa16cd305eb73e7ee739f5f03`. Governance closeout reviewed `5ec0157cb5c60674421dc75b4ae90c88659524e2` PASS/NONE, 25/25; PR #72 merged at `ba8062f1c7db1506af10fdd2193ed193d31cd72d`; final closeout main CI `37168633773` SUCCESS. Public reconstruction runtime, providers, Claims, production and real/confidential data remain unauthorized; real-paper semantic acceptance is NOT DETERMINED.
- **P2-001:** CLOSED / COMPLETED — MERGED. The USPTO Patent Specification Target v2 contract, template, reference maps, fixtures, and offline tests are established.
- **P2-000:** CLOSED / COMPLETED — MERGED. The enterprise five-stage web workflow and its reviewed P2-000-R1 and P2-000-R2 interface remediations are on `main`; P2-000-R2 merged through PR #65 at `a394a98b0a86b1ce686fac4871f7e5b0c0c3c44f`, with main CI `37012025003` SUCCESS.
- **P2-000-R3:** CLOSED / COMPLETED — MERGED. Implementation SHA `5569354e7003511d2e761236395ab6a604076530` received Gemini 3.1 Pro High / Antigravity PASS with findings NONE and 15/15 requirements passing; PR #67 merged at `62a25a9ae136461924bc8047c5a6ad0f3550c68c`. Closeout SHA `7697798a7e2a84f42d22ed896c0f49af6bf773e0` received Gemini 3.1 Pro High PASS with findings NONE and 13/13 requirements passing; PR #68 merged at `a9f50adcbefe8d5725c0b5e779ae24ad7546ec51`, and final main CI `37110753273` succeeded.
- **BLK-003:** OPEN. Production authentication, tenant isolation, private storage, retention, and deletion controls are not approved.
- **EVAL-001 PRODUCT_RUNTIME:** DEFERRED / AWAITING FUNDING. Real-paper provider/runtime semantic validation has not been performed.
- **Claims runtime integration:** NOT ENABLED. P2-004 standalone `SUPPORTED_DRAFT_CLAIMS` v1.0.0 is implemented offline, implementation-reviewed PASS and merged, but it is not assembled into the P2-001/P2-003 product runtime; P2-001 target Claims structures remain unchanged and P2-003 `review_boundary.claims_runtime_implemented` remains `false`.
- **Production security and real/confidential-data use:** NOT APPROVED.

Detailed task, SHA, pull-request, CI, and review evidence remains in the [Project Control Center](docs/operations/01_PROJECT_CONTROL_CENTER.md), [review log](docs/operations/02_GEMINI_REVIEW_LOG.md), task records, and Git history.

## Project status

| Task | Status | Evidence / next gate |
|---|---|---|
| UIUX-003 | **IMPLEMENTATION — INDEPENDENT REVIEW PENDING** | Workflow V1; Human-authorized fixed-Light supersession, VIH visual polish; baseline `63d5a61235669ad7d32bb38d583789ea59ce5497`, branch `feat/uiux-003-final-visual-polish`. [Evidence and AC-01–18](docs/tasks/UIUX-003-implementation-evidence.md), [before/after provenance](docs/qa/uiux-003/README.md). Final local browser 78 PASS; Python 903 PASS / 3 SKIP. One implementation PR records final SHA, exact-head CI/artifacts and Gemini 3.1 Pro High / Antigravity STRICT READ-ONLY handoff; no review PASS, merge or deployment claimed. Existing dependency advisories unresolved; MCP Unknown task — BLOCKED BY TOOL CAPABILITY; draft-only and provider/data/Claims/production limits preserved. |
| UIUX-002 | **IMPLEMENTATION CLOSED / MERGED — POSTMERGE CI SUCCESS** | Workflow V1; [PR #103](https://github.com/nshaokiet/ai-ip-description-generator/pull/103) normal expected-head merge `e6a47c900d227e2c028156e0dad5225d721e3353`, reviewed tree matched. Human-supplied external Gemini 3.1 Pro High / Antigravity STRICT READ-ONLY **PASS, 28/28 implementation ACs** on `af5406669fcb53593184461ba0dab0c7b1ba67e4`; [review reconciliation](https://github.com/nshaokiet/ai-ip-description-generator/pull/103#issuecomment-6105421655), [eligibility](https://github.com/nshaokiet/ai-ip-description-generator/pull/103#issuecomment-6105429552). [Head CI #38109920594](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/38109920594) and [actual-merge CI #38111671791](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/38111671791) SUCCESS. Final factual documentation SHA/CI and canonical closeout are recorded in PR #103; distinct from reviewed implementation. Two non-blocking LOW observations retained; reviewer directly inspected seven images, wider synthetic matrix automated. MCP **BLOCKED BY TOOL CAPABILITY — Unknown task**; full WCAG/assistive-technology certification, authentic Claims chain and Word pagination remain unverified. Draft only; no real research, paid provider, public P2-006 integration, deployment or next task authorization. |
| UIUX-001 | **SPECIFICATION CLOSED / APPROVED / MERGED — POSTMERGE CI SUCCESS** | Workflow V1; 28/28 specification ACs reported **PASS** by Human-attributed external Gemini 3.1 Pro High / Antigravity STRICT READ-ONLY on `9c846b1d07ca825871f017ed75cd15be561f6aca` ([review reconciliation](https://github.com/nshaokiet/ai-ip-description-generator/pull/102#issuecomment-6097323015)); [merge eligibility](https://github.com/nshaokiet/ai-ip-description-generator/pull/102#issuecomment-6097329555); [PR #102](https://github.com/nshaokiet/ai-ip-description-generator/pull/102) normal merge `1908db5520cc2f4af7a9044f6c27f84c3882f89b`, reviewed tree matched; [head CI #38049956268](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/38049956268) SUCCESS and [merge/main CI #38050914819](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/38050914819) SUCCESS. Exactly 3 documentation files; reported LOW lockfile finding corrected as external review description only. MCP `Unknown task: UIUX-001` — **BLOCKED BY TOOL CAPABILITY**. **Specification only**; implementation, real-paper/provider AI, public P2-006 B2 export, Claims changes and production require separate Human authorization. |
| P2-006 | **CLOSED / COMPLETED — MERGED — POSTMERGE CI SUCCESS** | Workflow V1; frozen spec v0.2.0 `5ac9b7bcd31e8ade7f4b0861b6e7a9c14e531953`; [Human Visual QA ACCEPTED](https://github.com/nshaokiet/ai-ip-description-generator/pull/101#issuecomment-6096814511); [Gemini 3.1 Pro High / Antigravity external fixed-SHA PASS](https://github.com/nshaokiet/ai-ip-description-generator/pull/101#issuecomment-6096818474) on `4e2308dce1e1b14fcc603c9e02152f21b0a3a3c7`; [merge eligibility](https://github.com/nshaokiet/ai-ip-description-generator/pull/101#issuecomment-6096834580); PR #101 normal merge `c6b417ef0fc0ccd2714101edf8048cad3b8d94f8` (reviewed tree matched); exact-head CI [#38042598827](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/38042598827) SUCCESS; exact merge/main CI [#38047166703](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/38047166703) SUCCESS; synthetic four-file PDF/DOCX output, [measured references and pinned QA](docs/tasks/P2-006-reference-qa.md); MCP `Unknown task: P2-006` — BLOCKED BY TOOL CAPABILITY. Authentic positive Claims full-chain, authorized figures and Word pagination remain unverified; draft only, no paid API, real-paper or production authorization. |
| P2-005 | CLOSED / COMPLETED — MERGED (conditional: this final-status sync PR requires its own independent fixed-SHA review, PR CI, merge and main CI) | V1; implementation PR #98 reviewed `731f0064a911205e9a8ddb9de64f4fa3b65b88e2` external PASS/NONE, merge `f3dfd7d1f1e559fb537256405ceaad47ba433560`; governance PR #99 reviewed `62f54c0cf04e7720dfa08f25e31b9c14ce101e36` [external PASS/NONE](https://github.com/nshaokiet/ai-ip-description-generator/pull/99#issuecomment-6076256290), merge `d81e2e065545b37445e85fd9322ce99510a025d2`, [exact-main CI #37897744309](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/37897744309) SUCCESS, [canonical evidence receipt](https://github.com/nshaokiet/ai-ip-description-generator/pull/99#issuecomment-6076332719); MCP task Unknown/BLOCKED BY TOOL CAPABILITY; Claims full-source E2E gap and reviewer background-test NOT VERIFIED preserved; downstream P2-006 separately gated |
| GOV-AGENT-001-B1 | CLOSED / COMPLETED — MERGED | PR #85 merge `4e8e51b178f0f112c637b64f1472b3506ad455ba`; main CI `37468063560` SUCCESS; additive data foundation only |
| GOV-AGENT-001-B2 | IMPLEMENTATION MERGED — INDEPENDENT REVIEW PASS | PR #86 merge `b16c092491d3f0f784c82120b762a0e0064c9274`; exact main/push CI `37559518802` SUCCESS; [original Antigravity / Gemini 3.1 Pro High report](https://github.com/nshaokiet/ai-ip-description-generator/pull/86#issuecomment-6029219683) on `ff76a494ebd7c613ce0ff8ff8b25667299b516fe` |
| GOV-AGENT-001-B3 | CLOSED / COMPLETED — MERGED — INDEPENDENT SECURITY + QUALITY REVIEW PASS | PR #87 merge `a53f40731f182892edda7d76d49a616f3a54a49c`; post-merge main CI `37567450686` SUCCESS; Workflow V2 still NOT ACTIVATED |
| GOV-AGENT-001-C | CLOSED / COMPLETED — MERGED — POST-MERGE VERIFIED | PR #88 reviewed SHA `20e16d4d07f5b4b9f4d131ab6f67d42b9a4488c7`; merge `696d667c1db5d199377f367167c6302fbc2389cd`; main CI `37572087226` SUCCESS |
| GOV-AGENT-001-D | CLOSED / COMPLETED — MERGED | PR #89 reviewed `0d8a27f8599c8a1d0f9d7c3e265dcfb07e26f812`; merge `5d8d4b555b1c11407db4671b9c2af88f4baad8bb`; main CI `37586700659` SUCCESS; [original review](https://github.com/nshaokiet/ai-ip-description-generator/pull/89#issuecomment-6033009872) and [closeout](https://github.com/nshaokiet/ai-ip-description-generator/pull/89#issuecomment-6033099037) |
| GOV-AGENT-001-E | ACTIVATED — EXPLICITLY ENROLLED TASKS ONLY | Activation merge `9c291325d409f74bc767f9b870e81d75c9b70802`; [accepted Phase E closeout](https://github.com/nshaokiet/ai-ip-description-generator/pull/90#issuecomment-6034290739); unchanged [canonical marker](docs/operations/WORKFLOW_V2_ACTIVATION.yaml) v1.0.0; automatic routing OFF |
| GOV-AGENT-001-F-PILOT-01 | CLOSED / COMPLETED — CANONICAL | PR #91 reviewed B `77bd4ace72e2c050129e345dcde11206ce739303`; frozen spec v0.1.0 `fcb52eb30da03df4d1ce6bc7487bc58f7135014f`; merge `ea78c5e197d7c6ff0318d3ed2ac581c4e2f57190`; main CI [37641700885 SUCCESS](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/37641700885); [Security PASS](https://github.com/nshaokiet/ai-ip-description-generator/pull/91#issuecomment-6040682169), [Quality R2 PASS](https://github.com/nshaokiet/ai-ip-description-generator/pull/91#issuecomment-6040683645), distinct sessions; [R1 preserved / excluded from AC-11](https://github.com/nshaokiet/ai-ip-description-generator/pull/91#issuecomment-6040684709); [MANUAL_EXTERNAL PASS](https://github.com/nshaokiet/ai-ip-description-generator/pull/91#issuecomment-6040743223); PR92 documentation merge `de23dd70c28a682faa17cbd69c1ce569ecc9c35f`; main CI37720954508 SUCCESS; [canonical receipt](https://github.com/nshaokiet/ai-ip-description-generator/pull/91#issuecomment-6051437979); MCP AWAITING_REVIEW / completion BLOCKED BY TOOL CAPABILITY; automatic routing OFF |
| GOV-AGENT-001-G | IMPLEMENTATION MERGED / POSTMERGE CI VERIFIED — PHASE G CLOSEOUT PENDING | Frozen spec v0.1.1/spec3 `7c42db54909506cef5d57739072a58b3dad68943`; reviewed implementation `4d3549e0fc3c0c4f9b5fc07dc47642bea4095d90`; [Security PASS](https://github.com/nshaokiet/ai-ip-description-generator/pull/93#issuecomment-6056085370) and [Quality PASS](https://github.com/nshaokiet/ai-ip-description-generator/pull/93#issuecomment-6056086371), separate read-only Antigravity sessions; [MANUAL_EXTERNAL PASS](https://github.com/nshaokiet/ai-ip-description-generator/pull/93#issuecomment-6056148297); actual merge `1c8212971db10eb44fb0639da34f4076af6ca4eb`; [exact push/main CI 37751828515 SUCCESS](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/37751828515); [verified postmerge receipt](https://github.com/nshaokiet/ai-ip-description-generator/pull/93#issuecomment-6056276026); G-AC-24 status sync/independent review/final closeout pending; SEC-003 LOW OPEN follow-up; MCP completion unsupported; routing OFF; Phase H / AI-CONV NOT AUTHORIZED |

Workflow V2 activation `9c291325d409f74bc767f9b870e81d75c9b70802` is verified on main;
it applies only to explicitly Human-authorized V2-enrolled tasks referencing the
immutable WORKFLOW_V2_ACTIVATION_COMMIT. Historical/unenrolled tasks remain V1.
Authoritative merge verification is [MANUAL / EXTERNAL](docs/operations/WORKFLOW_V2_MANUAL_VERIFICATION.md);
accepted verifier adapters remain UNAVAILABLE and B3 authoritative_merge_eligible
stays false. Automatic R0–R4 routing is NOT ACTIVATED. Phase F is canonically
COMPLETED/PASS with its operational completion limitation preserved.
These governance milestones do not change application/provider/data/production authorization.

## Conditional project adoption (Phase G)

Human approved **ADOPT V2 WITH CONDITIONS** under
`HUMAN-GOV-AGENT-001-G-ADOPT-V2-CONDITIONAL-2026-10-08`.
[AGENTS.md §25](AGENTS.md) and the [frozen G spec](docs/tasks/GOV-AGENT-001-G_ADOPTION_SPEC.md)
define the bounded policy. PR #93 implementation merge and its exact-main CI are
verified. **G-AC-24 remains PARTIAL** until this status-reconciliation PR #94 receives
fresh Security and Quality PASS on its final SHA, required PR CI SUCCESS, fresh
MANUAL_EXTERNAL verification and normal guarded merge, followed by exact resulting
main CI SUCCESS and a published/read-back canonical Phase G closeout. Completion
requires all of those external facts; the approved conditional-adoption decision
must not be reported as project-wide ACTIVE or GOV-AGENT-001-G CLOSED / COMPLETED
while closeout evidence is incomplete. Branch/open PR/static PASS is insufficient.

| Policy field | Required value |
|---|---|
| Adoption policy | CONDITIONAL |
| Adoption effective boundary | Accepted Phase G merge/postmerge verification |
| Preferred process | V2 for eligible explicitly Human-authorized tasks |
| V2 enrollment | EXPLICIT_ONLY |
| Historical/unenrolled V1 | PRESERVED |
| MANUAL_EXTERNAL | MANDATORY |
| Phase G reviews | Security AND Quality, separate identities and actual Antigravity sessions |
| Automatic R0-R4 | NOT ACTIVATED |
| Identity | PROCEDURAL_TRUST_BASED |
| Accepted verifier adapters | UNAVAILABLE |
| B3 authoritative_merge_eligible | false |
| Evidence | RECORDED != VERIFIED; provisional_ready != authoritative_merge_eligible |
| MCP completion transition | BLOCKED BY TOOL CAPABILITY — disclosed separately |
| Rollback | Preserve evidence; separately reviewed Human disable; in-progress Human disposition |
| Product/provider/production authority | NOT GRANTED |
| Phase H / AI-CONV | NOT STARTED |
| WORKFLOW_V2_ACTIVATION_COMMIT | 9c291325d409f74bc767f9b870e81d75c9b70802 |

Every new V2 task still needs actual Human authorization, registration, approved scope,
explicit enrollment and required role/frozen-spec/evidence state. No automatic approval,
enrollment or V1 migration. Both independent read-only Antigravity reviews on the same
final SHA are mandatory for G; future requirements are explicit and unclear policy blocks.
Phase F canonical completion does not change its operational AWAITING_REVIEW status.
Unsupported MCP completion is disclosed separately and never hidden through raw SQL,
V1 transitions or task recreation. No provider/data/budget/Claims/production or
Phase H authority is granted. Original E/F decisions/reviews and V1 history remain.

## Main Features

### Currently working demo flow

- PDF/DOCX selection and client-side validation UI.
- Controlled synthetic PDF and DOCX end-to-end samples.
- Source parsing and traceable evidence architecture.
- Structured invention-analysis architecture.
- USPTO-style patent-draft workflow.
- Human review, prose revision, and immutable session revisions.
- Exact-revision backend validation before export.
- Editable DOCX export.
- Deterministic backend, frontend, and browser regression coverage.
- USPTO Patent Specification Target v2 contract and template.

### Deferred real-paper AI runtime

- Arbitrary selected papers are not currently sent through provider-backed AI conversion in the public demo.
- Live provider evaluation and semantic acceptance remain deferred pending explicit funding and authorization.
- Production use, confidential-data processing, and Claims generation require separate approved work.

## Current Workflow

```text
1. Source Upload
2. AI Extraction
3. Review & Refine
4. Validation
5. DOCX Export
```

The controlled samples exercise the complete workflow. Reached-step navigation reuses the current session without replaying processing requests, while reset and source-removal actions keep local selection, uploaded-document, and generated-result lifecycles distinct.

## Prerequisites

- Python 3.12
- Node.js 24+
- npm
- Git

Windows PowerShell is the primary documented local environment.

## Installation

```powershell
git clone https://github.com/nshaokiet/ai-ip-description-generator.git
cd ai-ip-description-generator
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt -r tests/requirements.txt
cd frontend
npm ci
cd ..
```

Do not add an `OPENAI_API_KEY` for the documented offline/synthetic workflow.

## Usage

Start the local frontend and backend from the repository root:

```powershell
.\.venv\Scripts\python.exe tools\local_dev.py
```

Open:

- Web application: http://127.0.0.1:3000
- Backend health: http://127.0.0.1:8000/health
- Frontend proxy health: http://127.0.0.1:3000/backend/health

Check prerequisites and ports without starting services:

```powershell
.\.venv\Scripts\python.exe tools\local_dev.py --check
```

Press `Ctrl+C` to stop the services owned by the launcher.

## Testing

Backend regression:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q -p no:cacheprovider
```

Frontend and standard browser workflow:

```powershell
cd frontend
npm ci
npm run lint
npm run typecheck
npm run build
npm run test:e2e
```

Static public-demo workflow:

```powershell
$env:RENDER_STATIC_EXPORT = "1"
$env:NEXT_PUBLIC_DEMO_STAGING = "1"
npm run build
npm run test:e2e:demo
```

All repository CI paths keep `RUN_OPENAI_LIVE_TESTS=0` and `RUN_OPENAI_DRAFT_LIVE_TESTS=0`.

## Project Structure

```text
backend/     FastAPI routes, parsing, orchestration, and validation
frontend/    Next.js application and Playwright browser tests
prompts/     Versioned extraction and drafting prompts
schemas/     Structured analysis and patent-specification contracts
templates/   Editable DOCX templates
tests/       Offline backend, schema, integration, and synthetic fixtures
docs/        Specifications, decisions, task records, reviews, and runbooks
tools/       Local development and project tooling
```

## Documentation

- [Project Context](PROJECT_CONTEXT.md)
- [System Specification](docs/system-specification.md)
- [P2-000 Product Workflow Specification](docs/tasks/P2-000-product-webapp-simplification.md)
- [Project Control Center](docs/operations/01_PROJECT_CONTROL_CENTER.md)
- [Independent Review Log](docs/operations/02_GEMINI_REVIEW_LOG.md)
- [MVP Handover Runbook](docs/operations/MVP_HANDOVER_RUNBOOK.md)
- [Render Demo Runbook](docs/operations/DEPLOY_001_RENDER_RUNBOOK.md)
- [AI Collaboration Rules](AGENTS.md)

## Troubleshooting

### Python 3.12 is not found

Run `py -0p`, then create `.venv` with the full path to an installed Python 3.12 interpreter if necessary.

### Port 3000 or 8000 is already in use

Run `.\.venv\Scripts\python.exe tools\local_dev.py --check`, stop the process using the required loopback port, and retry.

### Frontend dependencies are inconsistent

Run `npm ci` from `frontend/`.

### The backend is unavailable

Check http://127.0.0.1:8000/health and follow the [MVP Handover Runbook](docs/operations/MVP_HANDOVER_RUNBOOK.md).

## Contributing

1. Branch from the current `main`.
2. Keep changes within an explicitly authorized task.
3. Run relevant offline tests before opening a pull request.
4. Do not commit secrets, API keys, private research papers, or generated confidential data.
5. Include exact verification evidence and request independent fixed-SHA review.

## License / Contact

No open-source license has been published. Do not assume permission to reuse, modify, or redistribute this repository outside the authorized project scope.

- GitHub: [@nshaokiet](https://github.com/nshaokiet)
- Support: [GitHub Issues](https://github.com/nshaokiet/ai-ip-description-generator/issues)
