# PRODUCT-DIRECTION-20261121 — Website-first, API-ready product strategy

| Field | Value |
|---|---|
| Document / version | PRODUCT-DIRECTION-20261121 / 0.1.0 |
| Prepared | 2026-11-21 (Asia/Ho_Chi_Minh) |
| Status | **PROPOSED FOR HUMAN REVIEW — documentation-only; not an approved implementation spec** |
| Direction | Website-first; reuse existing modules; prove end-to-end synthetic workflow before funded API pilot |
| Repository baseline | `main` at `6bb947c1cf67bcfb3ffc935b3a3fafcafb87f0af` |
| Workflow / authority | Existing V1 and AGENTS.md; Human request to reassess direction and update repository documentation, 2026-11-21 |
| Budget / provider | **USD 0; provider NOT_RUN; no paid calls** |
| Safety | No confidential/real unpublished paper, no deployment or live Claims enablement authorized |

## 1. Executive decision proposal

**Build the usable Next.js + FastAPI website, not another offline-only product or a second conversion engine.** Existing local/offline/synthetic modules are implementation and test assets. The user-facing product path is:

**Permitted scientific PDF/DOCX → upload and source evidence → invention reconstruction / USPTO-style specification draft → source-linked Human/IP review and edits → validation and missing-support decisions → draft DOCX/PDF export.**

When a source is inadequate, return missing support or `HUMAN_CONFIRMATION_REQUIRED`; do not generate an unsupported invention, embodiment, legal conclusion or claim. Keep a reviewable source trail and distinguish source statements, inferences, and author-confirmed statements.

The project target is a **draft of a U.S. nonprovisional utility-patent specification**, not a filing service, issued patent, legal opinion, or guaranteed patent application. The historical “B2-style” shorthand refers to an **issued-patent publication kind code**, not an official USPTO fill-in “Form B”. See [P2-001](../tasks/P2-001-uspto-target-specification-v2.md).

**Near-term definition of success:** one complete, repeatable, default-OFF **browser-to-export synthetic workflow** on two different admitted technical samples (a text PDF and DOCX), with evidence, review, refusals, exact expected output artifacts, negative tests, security checks, and no provider spend. This is a goal, **not a claim of current end-to-end PASS**.

## 2. Verified repository assets vs. unverified product claims

| Capability | Reuse / evidence | Remaining limitation |
|---|---|---|
| PDF/DOCX upload/parsing/source locators | APP-001/APP-002, backend; synthetic offline coverage | OCR/scanned-only not supported; real/confidential inputs prohibited |
| Extraction and structured draft runtimes | Internal OpenAI Responses API boundaries, schemas/validation | Provider NOT_RUN; semantic correctness not established |
| Invention reconstruction, specification, reference checks | P2-001/P2-002/P2-003, source-custody C1, synthetic pipeline | Arbitrary-paper and full browser flow not accepted |
| Supported draft Claims | P2-004 standalone and semantic-authority prototype | **Product Claims runtime DISABLED**; no automatic Claims enablement |
| Document validation / editable export | Existing P2-005/P2-006 assembler, validators, DOCX/PDF renderers | Static demo is fixed sample; four-artifact browser export not verified |
| Website UI/API | Next.js, FastAPI, v1 upload/process/review components | Product-001B's end-to-end session-bound browser flow not fully admitted/verified |
| Authentication/security work | S1 local transport/auth foundation plus S2-A candidate PR #164 | Production owner isolation, retention, and BLK-003 remain unresolved |
| Mock evaluation and CI | Two-content offline synthetic #161; gold 6 cases / 154 items; frontend/backend/MCP tests | Synthetic PASS does not prove live provider quality or production security |

**Do not rebuild** source extraction, reconstruction, Claims standalone, renderers, schemas, or test harnesses simply to produce a new task ID. Inspect existing contracts first; implement only missing adapters, integration points and tests.

## 3. Current blocked work and dependency order (snapshot 2026-11-21)

These are **independent PRs**, not completed milestones:

1. [PR #165 — dependency remediation](https://github.com/nshaokiet/ai-ip-description-generator/pull/165), HEAD `b4e7db7b123dc41e169483a50ca36d6f7821a9d4`: hosted CI `44263429631` SUCCESS, but independent Quality addendum identifies a **MEDIUM dynamic-directory/tsconfig include compatibility regression** (finding `DEP-RECON-QUAL-001`, `REQUEST CHANGES`). Remediation + new-head CI and independent review are required; historical task-initiation authorization is `AUTHORIZATION_PROVENANCE_NOT_VERIFIED` and requires actual-date Human disposition. **NOT MERGE ELIGIBLE**.
2. [PR #166 — standing Argon reviewer policy](https://github.com/nshaokiet/ai-ip-description-generator/pull/166), HEAD `37e9344465e5bc052bb02e9da60c23d67e7f62de`: validator alignment done, targeted/back-end tests reported PASS; CI `44889601897` FAILURE at inherited Next.js audit gate. Do not disable audit or reuse its failed CI.
3. [PR #164 — default-OFF S2-A bridge](https://github.com/nshaokiet/ai-ip-description-generator/pull/164), HEAD `f08b071ee76468f01ad20bfa917d1b6360e5b453`: OPEN/DRAFT, security and independent review/integration still gated. Do not assume an unmerged S2-A implementation exists on main.

**Proposed integration sequence:** finish #165 correctly → reassess #166 on updated main → reassess #164 and applicable S2-A dependencies → begin a narrowly approved PRODUCT-001B browser integration. Ordering is conditional on actual dependency and accepted-main checks, not a blanket permission to merge or rebase.

Security remediation and product gap analysis may proceed **in parallel as separate workstreams**, but implementation code that depends on unmerged branches must wait for accepted dependencies.

## 4. Thin product roadmap — no parallel backend

### Stage A — Reconcile and unblock (in flight)

- Resolve `DEP-RECON-QUAL-001` with a bounded adapter fix/tests on #165, new SHA, CI, independent Security/Quality and Human provenance/merge decisions.
- Integrate #166/#164 only after their own exact-head/rebase, security, reviews and Human merge gates.
- Preserve branch and report history; no “CI green means safe to merge” shortcut.

**Exit:** required accepted-main dependencies are verified, or gaps are explicitly listed as blocked with no fake green status.

### Stage B — Single-operator secure browser flow (next proposed build)

Reuse [PRODUCT-001B-WEB-001](../tasks/PRODUCT-001B-WEB-001.md), [PRODUCT-001B v0.2.0](../tasks/PRODUCT-001B-trusted-local-review-presenter.md), and existing C1/P2 contracts. **Do not duplicate them as PRODUCT-002.** Confirm design/security decisions `D01–D07`, fixtures/admission and the B1–B6 implementation boundary before authorization. Reuse local operator-controlled HTTPS/session model rather than inventing SaaS/multi-tenant production.

Required user capabilities: select admitted synthetic file, upload, start mock processing, read cited evidence, review/answer missing information, edit supported draft, validate revision/digest, and export existing expected USPTO v2 draft artifacts. Browser displays **review metadata separately from filing-style prose**, and refuses unsupported Claims. Use existing server-controlled custody/manifest; browser never owns source or approval authority.

**Exit:** user can complete the same flow in the browser with no CLI interaction for normal review, while local operator setup/security remains a separate trusted administration boundary.

### Stage C — Reproducible mock E2E and product acceptance

Accept **two distinct technical contents** (one text PDF, one DOCX) through explicit permitted fixture admission. Do not treat two file encodings of the same controller as two sources.

Demonstrate:
- source locator/evidence correctness and distinct source fingerprints;
- end-to-end upload → processing → source-grounded review → revision validation → export with proper filenames, MIME and integrity;
- controlled Claims behavior: supported standalone capability is not silently used in product; `claims_runtime_implemented=false` and explicit missing/refusal states remain true;
- negative paths: unsupported or too-large/scanned input, missing support, cross-session misuse, expired session, stale revision/digest, unapproved file/fixture, wrong export authorization, provider/network egress attempt;
- frontend lint/typecheck/build, backend/MCP, Playwright/browser E2E, security/audit, DOCX/PDF layout QA and exact-HEAD hosted CI.

**Exit:** all scoped mock-E2E acceptance tests PASS with no paid provider, verified artifacts and independent review. Declare `API_READY_SYNTHETIC` only with documented criteria; do not equate it to live semantic acceptance or production.

### Stage D — Paid-provider pilot (future, separately authorized)

Prepare provider smoke scripts/default-OFF configs and offline preflight now. Actual provider/model entitlement, cost controls, backend-only secrets, budget enforcement, source permissions, Human/IP evaluation and explicit paid-call authorization remain future gates. **Budget enforcement is NOT_IMPLEMENTED**; a configuration flag or `USD 0` intention is not a runtime cost guard.

With approved budget and lawful data, run a bounded live pilot against the accepted evaluation framework, measure grounding/hallucination, disclosure quality, source support, Claims conservatism, error rate, latency and cost. A pilot result is not permission to make filing, novelty or patentability claims.

## 5. Explicitly defer

Defer multi-user SaaS, account/billing, collaboration platform, cloud databases/vector DB/RAG, prior-art/novelty/FTO automation, OCR/vision, generalized agent orchestration, large UI redesign, automatic product Claims enablement and production/public upload. These are **not prerequisites for the synthetic API-ready milestone**, and would need their own scoped Human decisions if later necessary.

Continue maintaining existing MCP as a development coordination tool. Do not make it the user-document database.

## 6. Recommended next task and authorization boundary

**Next task candidate: `PRODUCT-001B-WEB-001-GAP-AUDIT` (PROPOSED / NOT AUTHORIZED FOR RUNTIME).** Read-only, no code or fixture mutation:

1. Map every required browser action and API route to the *actual accepted-main* backend/frontend implementation, including #164 as a separate unmerged candidate.
2. Produce a B1–B6 acceptance matrix of `IMPLEMENTED / TESTED / MISSING / BLOCKED` with exact code references.
3. Reconcile D01–D07 security decisions, session/owner/content lifecycle, two-content fixture admission and output contracts; propose the **smallest next executable increment**, not a complete rewrite.
4. State all prerequisites and negative security tests, the independent review plan, CI checks, and exact implementation files.
5. Request a separately scoped Human implementation authorization for the identified gap. No new runtime, provider/Claims activation or production assumption follows from this roadmap.

The Human's request to reassess direction and update repository documentation authorizes this **documentation candidate only**, not Stage B–D implementation, PR merging, data-security policy changes or reviewer bypass.

## 7. Product scorecard and stop rules

| Metric | Near-term acceptance |
|---|---|
| Complete browser workflow | Two distinct admitted synthetic sources complete upload-to-export |
| Grounding | Every represented technical claim/disclosure is linked to source or explicitly flagged for Human confirmation |
| Document output | Existing v2 export contract and file integrity satisfied; separate review package |
| Claims | Runtime stays OFF unless separately authorized; unsupported Claims empty/refused |
| Safety | Auth/session/CSRF/owner/revision gates pass negative tests; no secrets, no provider egress |
| Reproducibility | Required hosted CI, security artifacts, tests, independent reviews and Human decisions on exact final SHA |
| Spend | 0 paid provider calls prior to later explicit funding authorization |
| Semantic quality | NOT DETERMINED until actual authorized model evaluation |
| Deployment | NOT APPROVED; BLK-003 remains OPEN |

**Stop development expansion** at the verified `API_READY_SYNTHETIC` milestone until real pilot funding/authority exists. Maintain only needed dependency/security fixes and the documented pilot readiness checklist. Never claim that inserting an API key instantly produces a legally complete or filing-ready patent.

## 8. Sources of truth and review request

- [README](../../README.md), [Project Context](../../PROJECT_CONTEXT.md), [system specification](../system-specification.md), [Workflow](../workflow.md)
- [Website direction decision](../decisions/RESUME-FOUNDATION-001-web-direction.md)
- [PRODUCT-001B web contract](../tasks/PRODUCT-001B-WEB-001.md) and [API-ready S1 foundation](../tasks/API-READY-WEB-GAP-001B-S1.md)
- [USPTO target v2](../tasks/P2-001-uspto-target-specification-v2.md), [Claims standalone boundary](../tasks/P2-004-supported-draft-claims.md), [MVP closeout](../operations/FINAL_MVP_CLOSEOUT.md)
- [Governance AGENTS.md](../../AGENTS.md); [PR #165](https://github.com/nshaokiet/ai-ip-description-generator/pull/165), [#166](https://github.com/nshaokiet/ai-ip-description-generator/pull/166), [#164](https://github.com/nshaokiet/ai-ip-description-generator/pull/164)

**Human review questions:** Approve the website-first priority and the no-rewrite / no-extra-features stop rule? Authorize a separate read-only B-gap audit? After the audit, approve a narrow B implementation slice only with D01–D07 decisions and admitted fixture evidence. Do not merge this docs PR until its own required review/CI and Human approval.
