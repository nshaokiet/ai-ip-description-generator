# AI-CONV-001 — Source-grounded USPTO v2 orchestration specification

## 1. Metadata

| Field | Value |
|---|---|
| Task ID | AI-CONV-001 |
| Version | 0.1.1 |
| Status | PROPOSED — READY FOR SPECIFICATION REVIEW |
| Canonical issue | GitHub #108 — AI-CONV-001 — Specify source-grounded USPTO v2 end-to-end pipeline (Phase H candidate) |
| Analysis baseline | `8c36b2bc662ed41b2a9b3635d5d4d29110b1d9bb` |
| Scope | Specification/readiness analysis only |
| Phase H | NOT ACTIVE / NOT ENROLLED BY THIS SPECIFICATION |
| Provider/API budget | 0; no paid/live provider call authorized |
| Real/confidential research data | NOT AUTHORIZED |
| Production/public deployment | NOT AUTHORIZED |
| Implementation authorization | NOT GRANTED |

### Revision history

| From | To | Date | Author | Change | Reason | Related finding/decision | Breaking change |
|---|---|---|---|---|---|---|---|
| 0.1.0 | 0.1.1 | 2026-10-14 | Codex | Complete pre-review task gates, reviewer-profile requirements and EVAL-001 metric-reuse boundary; no runtime/contract change | Close documentation-only gaps against Issue #108 before fixed-SHA review | AI-CONV-001 / Issue #108 readiness verification | No |

This specification proposes the next additive integration layer for converting a validated scientific-paper source into the already released offline USPTO v2 artifacts. It does not modify application code, released schemas, prompts, provider configuration, runtime behavior, Render configuration, or existing v1 public workflow.

## 2. Objective

Define a reviewable architecture for the future authorized path:

`APP-002 evidence envelope + validated structured analysis`

→ `P2-002 invention reconstruction`

→ `P2-003 USPTO specification draft v2`

→ `P2-004 supported draft Claims`

→ `P2-005 USPTO document package + strict provenance validation`

→ `P2-006 offline PDF/DOCX rendering`

The architecture must preserve source grounding, released fail-closed Claims semantics, existing v1 behavior, and the seven-input provenance trust boundary required by P2-005/P2-006.

## 3. Current-state interface inventory

### 3.1 APP-002 source contract

APP-002 accepts an already validated PDF/DOCX and creates a deterministic `ExtractionInputEnvelope` containing:

- safe document metadata including `document_id`, sanitized filename, media type and SHA-256;
- ordered source units with stable `evidence_id`, type, locator and content;
- released source-unit types limited to supported text/table evidence;
- no model/provider/network call and no OCR within APP-002.

This envelope is the source-identity root for the proposed v2 orchestration path.

### 3.2 P2-002 invention reconstruction

Released entry point:

`reconstruct_invention(envelope, analysis)`

Released output:

- `output_type = INVENTION_RECONSTRUCTION`;
- `schema_version = 1.0.0`;
- evidence-linked reconstruction derived from the APP-002 envelope and structured analysis;
- no authority to invent dependencies, variants, Human confirmation or stronger essentiality than the inputs establish.

The current APP-002 → P2-002 adapter is deliberately conservative. Authentic reconstruction may contain `UNKNOWN` essentiality and `OTHER` element classification where upstream evidence does not establish stronger semantics.

### 3.3 P2-003 USPTO specification generation

Released entry point:

`generate_uspto_specification(source, config)`

Released output:

- `output_type = USPTO_SPECIFICATION_DRAFT`;
- `schema_version = 2.0.0`;
- source-grounded USPTO-style disclosure sections;
- Claims deliberately absent from this stage;
- `claims = []` and no Claims preamble;
- `review_package.claim_support = []`;
- `review_boundary.claims_runtime_implemented = false`.

AI-CONV integration must preserve this invariant. P2-003 must not be reinterpreted as a Claims generator.

### 3.4 P2-004 supported draft Claims

Released entry point:

`generate_supported_draft_claims(reconstruction, specification, config)`

Released output:

- `output_type = SUPPORTED_DRAFT_CLAIMS`;
- `schema_version = 1.0.0`;
- Claims only where the released eligibility rules can prove support;
- no inferred essentiality, solution membership, composition membership or fabricated claim elements.

Released limitations include:

- SYSTEM/APPARATUS require an explicitly supported ESSENTIAL structural core;
- METHOD/PROCESS fail closed when step essentiality is unavailable;
- COMPOSITION fails closed when structured composition membership/mandatory amount semantics are unavailable;
- any required core with `UNKNOWN` essentiality blocks unsupported promotion;
- zero eligible claim families is a valid `HUMAN_CONFIRMATION_REQUIRED` result with `claims = []`.

### 3.5 P2-005 package assembly and validation

Released assembly entry point:

`assemble_uspto_document_package(...)`

It requires the seven original upstream inputs:

1. `source_envelope`
2. `structured_analysis`
3. `reconstruction`
4. `specification`
5. `p2_003_generation_config`
6. `supported_claims`
7. `p2_004_generation_config`

Released validator:

`validate_uspto_document_package(package, **same_seven_inputs)`

The validator reconstructs/revalidates upstream projections and compares the complete package. A standalone package, digest, boolean flag or unsigned receipt is not sufficient proof of provenance.

P2-005 projects P2-004 Claims additively into the filing view while preserving the original P2-003 output in review evidence. Its review boundary remains draft-only, Human-review-required and filing-not-ready.

### 3.6 P2-006 offline renderer

Released entry point:

`render_uspto_document_package(package, *, same_seven_inputs, output_dir)`

Before creating output files, P2-006 invokes the full P2-005 validator with the package and all seven original upstream inputs. It then creates the mandatory four-output synthetic QA bundle:

- `B2_REFERENCE_PREVIEW.pdf`
- `B2_REFERENCE_PREVIEW.docx`
- `USPTO_APPLICATION_DRAFT.pdf`
- `USPTO_APPLICATION_DRAFT.docx`

If Claims are unavailable, it renders an explicit Human-confirmation marker rather than filler Claim text.

### 3.7 Existing public workflow

At the analysis baseline, the public/local application workflow remains v1:

- `POST /api/documents/{document_id}/process`
- `POST /api/drafts/validate`
- `POST /api/exports/docx`

The `/process` route invokes the existing v1 core pipeline and returns the v1 `{analysis, draft, metadata}` contract. P2-002 through P2-006 are not wired into this route. The frontend types and API client likewise model the v1 workflow. Existing P2-007 browser capability is a controlled synthetic demonstration and is not an arbitrary uploaded-paper → USPTO v2 path.

## 4. Readiness finding

The primary missing component is an additive v2 orchestration/session integration layer. The core offline P2-002…P2-006 components already exist.

The integration layer must:

- invoke the released stages in deterministic order;
- preserve every original upstream artifact required for later provenance validation;
- bind each stage to one source identity and immutable/canonical input digest set;
- expose explicit review-required outcomes without converting them into errors;
- prevent stale/spliced inputs from crossing stages;
- keep v1 routes/contracts unchanged;
- remain offline/provider-free until a separate provider task is authorized.

## 5. Authentic source-to-Claims provenance gap

### 5.1 Current gap

The authentic APP-002 → P2-002 path does not reliably establish the semantic predicates that P2-004 requires for positive Claims generation. In particular, released source/reconstruction data can lack authoritative evidence for:

- which elements form the claimed solution rather than merely appearing in the source;
- which solution elements are `ESSENTIAL`;
- which method/process steps are essential;
- which materials belong to one composition and which amounts/relationships are mandatory;
- the authority required to transform Human statements into audited `HUMAN_CONFIRMED` semantics.

Therefore an authentic source can validly reach P2-004/P2-005 with:

`claims.status = HUMAN_CONFIRMATION_REQUIRED`

and:

`claims = []`.

That result is a successful fail-closed pipeline outcome. It must not be treated as a processing failure and must not be “fixed” by inferred Claim text.

### 5.2 Evidence interpretation

Existing positive standalone P2-004 fixtures prove that the released Claims generator can project supported structural Claims when its required predicates are already present. They do not prove that the authentic APP-002 → P2-002 path currently creates those predicates for arbitrary research papers.

### 5.3 Permitted initial architecture decision

AI-CONV-002, if later authorized, should integrate the existing semantics unchanged. It may produce no Claims for authentic sources. This isolates orchestration correctness from a separate Claims-semantics product decision.

### 5.4 Separately scoped remediation options

Any positive authentic Claims expansion requires a separate Human-approved task. Candidate approaches for that later task include:

1. **Structured upstream authority extension:** add auditable source-grounded fields that explicitly establish solution membership, element/step essentiality and composition membership.
2. **Human-confirmation authority workflow:** define exactly who may confirm each semantic predicate, what evidence is required, how the confirmation is versioned/audited, and how stale confirmation is invalidated.
3. **Hybrid source + Human authority:** permit P2-004 eligibility only when released source evidence plus explicit Human confirmation satisfies a versioned rule set.

These options may require schema/contract changes and therefore are not authorized by AI-CONV-001.

## 6. Proposed additive offline-first architecture

### 6.1 Architectural rule

Add orchestration around released contracts; do not mutate P2-002, P2-003, P2-004, P2-005 or P2-006 schemas/semantics as part of the initial integration task.

### 6.2 Proposed internal orchestration service

Future authorized implementation should introduce an internal service conceptually equivalent to:

`run_uspto_v2_offline_pipeline(...)`

Input requirements:

- validated APP-002 `source_envelope`;
- validated structured analysis compatible with P2-002;
- version-pinned P2-003 generation config;
- version-pinned P2-004 generation config;
- caller-provided private/local render root only when export is requested.

The orchestrator should call released public service entry points only. It should not reach into private projection helpers to bypass validators.

### 6.3 Proposed orchestration session record

The implementation needs a server-side/private session record. A new public/released schema is not required for AI-CONV-002 unless Human explicitly approves one. The internal record should retain at least:

- `session_id`;
- source `document_id` and APP-002 SHA-256;
- orchestration contract version;
- current stage/state;
- canonical digest for every retained input/output artifact;
- the complete seven upstream objects required by P2-005/P2-006;
- validated P2-005 package, if created;
- render manifest containing only safe filenames/paths/metadata, not source content;
- created/updated timestamps;
- error code and safe path metadata when failed;
- revision number or equivalent optimistic-concurrency token.

The seven upstream objects are retained as the authoritative in-session provenance bundle. Digests are integrity indexes, not substitutes for those objects.

### 6.4 Source identity binding

Every stage must bind to the same APP-002 source identity:

- `document_id` must match the session root;
- source SHA-256 must match the session root;
- canonical upstream digests must be recomputed at each transition;
- a changed source, analysis, config or stage output creates a new revision/candidate and invalidates downstream artifacts;
- downstream artifacts from two source revisions must never be spliced into one package.

### 6.5 Deterministic state machine

Proposed states:

1. `SOURCE_READY`
2. `RECONSTRUCTION_READY`
3. `SPECIFICATION_READY`
4. `CLAIMS_READY` or `CLAIMS_REVIEW_REQUIRED`
5. `PACKAGE_VALID`
6. `RENDERED`
7. `FAILED`

Transitions must be monotonic within one revision. A change to any upstream artifact/config starts a new revision at the earliest affected stage and invalidates all later-stage artifacts.

`CLAIMS_REVIEW_REQUIRED` is a normal state when P2-004 returns no eligible Claims. It can still advance to a valid P2-005 package and P2-006 render containing the explicit incomplete-Claims marker.

### 6.6 Failure behavior

The orchestrator must fail closed on:

- source identity mismatch;
- stale revision/digest;
- schema/contract validation failure;
- reconstruction re-projection mismatch;
- P2-003/P2-004 config mismatch;
- package projection mismatch;
- missing one of the seven provenance inputs;
- attempt to render package-only data;
- unsafe/non-private render destination;
- timeout/cancellation/cleanup failure that makes final state uncertain.

Errors exposed outside the service must use stable machine-readable codes and safe contract paths. Raw research text must not appear in logs or error messages.

## 7. Future API integration requirements

### 7.1 Additive routing

Do not repurpose or silently change `/api/documents/{id}/process`, `/api/drafts/validate`, or `/api/exports/docx`.

Future authorized implementation should add a separate v2 namespace. Proposed shape:

| Endpoint | Purpose |
|---|---|
| `POST /api/v2/documents/{document_id}/uspto/sessions` | Start an offline v2 session from an eligible validated document/analysis |
| `GET /api/v2/uspto/sessions/{session_id}` | Return safe stage/status/revision metadata |
| `GET /api/v2/uspto/sessions/{session_id}/review` | Return review-safe v2 artifacts/evidence references allowed by the final API contract |
| `POST /api/v2/uspto/sessions/{session_id}/validate` | Re-run strict package/provenance validation for the current revision |
| `POST /api/v2/uspto/sessions/{session_id}/exports` | Render/export only after strict validation against retained seven-input provenance |

Names are proposed, not authorized contracts.

### 7.2 API invariants

Future v2 APIs must:

- require current `session_id` + revision/ETag-equivalent for mutating actions;
- reject stale revisions with `409`;
- reject source/digest mismatch with a safe deterministic validation error;
- never accept a caller-supplied P2-005 package as sufficient export authority;
- use server-side/private retained provenance for validation/export;
- never return storage filesystem paths to the browser;
- expose `HUMAN_CONFIRMATION_REQUIRED` distinctly from processing failure;
- keep legal/filing disclaimers and Human review boundary visible;
- keep v1 response contracts unchanged.

### 7.3 Session persistence boundary

Initial authorized implementation should prefer the existing local/private ephemeral operating model. Any persistent database, object store, cross-user storage, authentication or tenant model is a separate architecture/security decision requiring Human approval.

## 8. Future frontend integration requirements

The v2 user interface should be additive and should not change the v1 flow by default.

Required states/views:

- source accepted / preparing evidence;
- reconstructing invention;
- generating USPTO disclosure;
- evaluating supported Claims;
- Claims available, partially available, or Human confirmation required;
- assembling/validating document package;
- rendering/export complete;
- safe failure/retry state.

The review experience must:

- show source identity and revision so users know which paper/version is under review;
- show evidence IDs/locators without presenting unsupported assertions as facts;
- distinguish disclosure content from Claims content;
- show missing-information/issues that block Claim families;
- treat zero Claims as a valid review-required result;
- never create or suggest hidden filler Claims;
- display `P2-003 claims_runtime_implemented=false` semantics accurately where relevant;
- prevent export against a stale session revision;
- require explicit Human action for future editable/confirmed semantic fields if such a workflow is separately approved;
- preserve disclaimer that output is a draft requiring Human/IP review and is not filing-ready/legal advice.

## 9. Source-grounding and provenance requirements

1. APP-002 `evidence_id` + locator remains the root citation primitive.
2. Reconstruction must be reproducible from the exact envelope + structured analysis supplied to the session.
3. P2-003 and P2-004 inputs/configs must be version-pinned and retained.
4. P2-005 must be assembled only after upstream validation and must then pass `validate_uspto_document_package` with all seven inputs.
5. P2-006 must receive the same retained provenance set used to validate the package.
6. Digests must use the existing canonicalization rules where released helpers already define them.
7. No stage may upgrade `INFERENCE`, `UNKNOWN`, `OTHER`, optionality or missing semantics into stronger Claim authority without an explicitly authorized rule.
8. Human confirmation, if later introduced, must be separately auditable and cannot be inferred from UI interaction alone.

## 10. Security and privacy requirements

For the initial offline implementation candidate:

- no network/provider call in the v2 orchestration stages;
- no paid API call;
- synthetic/authorized fixtures only;
- no real/confidential/unpublished paper;
- no raw source text, full prompts/responses or generated confidential drafts in application logs;
- retain only the minimum private session artifacts required for provenance and rendering;
- use bounded temporary/private storage and deterministic cleanup;
- reject unsafe/symlinked output destinations using the released renderer boundary;
- preserve APP-001/APP-002 file validation, safe naming and source SHA checks;
- treat document text as untrusted data, including prompt-like/instruction-like text inside research papers;
- never execute source-provided commands, URLs, embedded relationships or file paths;
- avoid returning raw exception content when it can contain source-derived strings;
- secret scanning and dependency checks remain required in implementation review/CI.

Authentication, authorization, tenant isolation, persistent storage, retention beyond the approved local boundary and production encryption/storage policy remain blocked pending separate Human decisions.

## 11. Validation and acceptance criteria

### 11.1 Contract/orchestration acceptance

| ID | Criterion |
|---|---|
| AC-01 | A synthetic authorized APP-002 envelope + compatible structured analysis can execute P2-002 → P2-003 → P2-004 → P2-005 entirely offline. |
| AC-02 | The orchestration preserves exact released schema versions and does not modify P2-002…P2-006 contracts. |
| AC-03 | The session retains the complete seven-input provenance bundle required by P2-005/P2-006. |
| AC-04 | P2-005 validation is performed with the exact retained seven inputs before package acceptance. |
| AC-05 | P2-006 render is performed only after strict package validation and with the same seven-input provenance. |
| AC-06 | Package-only render/export attempts are rejected. |
| AC-07 | Source/revision/config/digest mismatch is rejected deterministically. |
| AC-08 | Editing/changing any upstream candidate invalidates every affected downstream artifact. |
| AC-09 | Re-running the same deterministic offline inputs yields semantically/canonically identical stage outputs and package identity where released contracts guarantee determinism. |

### 11.2 Claims safety acceptance

| ID | Criterion |
|---|---|
| AC-10 | Authentic-style input lacking eligibility semantics yields `HUMAN_CONFIRMATION_REQUIRED` with no fabricated Claims. |
| AC-11 | `UNKNOWN` essentiality is never silently promoted to `ESSENTIAL`. |
| AC-12 | METHOD/PROCESS are not generated solely from ordered/related steps when essentiality authority is absent. |
| AC-13 | COMPOSITION is not generated from material co-occurrence/ranges without released composition-membership authority. |
| AC-14 | Existing P2-004 positive structural fixture behavior remains unchanged. |
| AC-15 | P2-003 output remains unchanged and continues to declare `claims_runtime_implemented=false`. |

### 11.3 Provenance/tamper acceptance

| ID | Criterion |
|---|---|
| AC-16 | Splicing a reconstruction/specification/Claims artifact from another source is rejected. |
| AC-17 | Tampering with any package field causes package projection validation failure. |
| AC-18 | P2-003 config mismatch is rejected. |
| AC-19 | P2-004 config mismatch or supported-Claims mismatch is rejected. |
| AC-20 | Missing any one of the seven original inputs blocks validation/render. |

### 11.4 API/frontend acceptance

| ID | Criterion |
|---|---|
| AC-21 | Existing v1 routes/types/tests remain behaviorally unchanged. |
| AC-22 | New v2 routes are additive and use separate response contracts. |
| AC-23 | Mutating/export actions reject stale session revisions. |
| AC-24 | Frontend visibly distinguishes processing failure from Claims Human-confirmation-required. |
| AC-25 | Frontend never presents a no-Claims result as filing-ready. |
| AC-26 | No server filesystem path or confidential source payload is exposed through v2 status responses. |

### 11.5 Render/regression/E2E acceptance

| ID | Criterion |
|---|---|
| AC-27 | P2-006 still emits exactly the four required files for a valid synthetic package. |
| AC-28 | Missing Claims render the released incomplete/Human-confirmation marker. |
| AC-29 | Existing P2-002…P2-006 unit/regression suites pass unchanged. |
| AC-30 | Existing v1 backend/frontend regression and E2E suites pass. |
| AC-31 | A new synthetic offline E2E test covers APP-002 → P2-006, including provenance validation. |
| AC-32 | Visual QA reuses the released P2-006 reference/measurement procedure when rendered layout changes are actually in scope. |
| AC-33 | Performance/latency may be measured offline but cannot be reported as semantic quality or product-runtime acceptance. |

### 11.6 EVAL-001 metric reuse boundary

Any later funded semantic/product-runtime evaluation should reuse the applicable released EVAL-001 measures rather than inventing a parallel quality vocabulary: grounding support precision, critical hallucination count, KEY/SECONDARY coverage, grounding-label accuracy, evidence fidelity, missing-information precision/recall, author-question usefulness and draft faithfulness. The zero-tolerance principles for contradiction, falsified evidence and unsupported legal conclusions remain applicable.

The historical EVAL-001 contract-safety gate requiring Claims count `0` belongs to the earlier no-Claims MVP contract and must not be transplanted unchanged into a future authorized USPTO v2 Claims evaluation. For v2, Claims safety remains governed by P2-004 eligibility/provenance rules and the AI-CONV-003 decisions, if that task is ever separately authorized. AI-CONV-001 does not authorize product-runtime evaluation, provider calls, threshold changes or semantic PASS.

## 12. Risk register

| Risk | Impact | Required mitigation |
|---|---|---|
| Authentic source lacks Claim-eligibility semantics | High | Preserve fail-closed no-Claims outcome; separate Human-approved semantics task |
| Provenance objects discarded too early | Critical | Session retains all seven inputs; package/digest alone never authorizes render |
| v2 accidentally changes v1 user workflow | High | Separate namespace/contracts + mandatory v1 regression |
| Stale edited artifacts are mixed | High | Revision/digest binding and downstream invalidation |
| Research text leaks through logs/errors | Critical | Safe error codes/paths, no raw content logging, synthetic-only implementation tests |
| UI implies legal/filing readiness | High | Persistent draft/Human-review boundary and explicit Claims status |
| Schema changes hidden inside integration task | High | AI-CONV-002 must consume released contracts unchanged; schema work moved to separately authorized task |
| Provider/runtime introduced implicitly | High | Offline-only architecture until funded/provider authorization exists |
| Persistent storage/auth assumptions exceed local boundary | High | Keep initial integration ephemeral/private; separate production/security decision |

## 13. Recommended implementation task breakdown

No task below is authorized by this specification. Each requires explicit Human scope, acceptance criteria and authorization reference.

### AI-CONV-002 — Offline v2 orchestrator + provenance/session integration

Scope:

- internal additive orchestration service;
- session/revision integrity model;
- deterministic P2-002 → P2-005 execution;
- optional P2-006 invocation through its released validator boundary;
- synthetic/offline tests only;
- no Claims semantic/schema expansion.

### AI-CONV-003 — Authentic source-to-Claims semantic authority

Scope only after explicit Human Claims decision:

- define solution membership and essentiality authority;
- define METHOD/PROCESS step-essentiality semantics;
- define COMPOSITION membership/mandatory-amount semantics if required;
- define Human confirmation audit semantics if used;
- version/schema/migration impact analysis;
- positive authentic-style provenance E2E only after contract approval.

### AI-CONV-004 — Additive v2 backend API integration

Scope:

- versioned v2 session/status/review/validate/export routes;
- stale revision handling;
- safe error model;
- local/private session lifecycle;
- preserve v1 routes.

### AI-CONV-005 — Frontend v2 review/export UX

Scope:

- additive v2 workflow;
- evidence/revision visibility;
- Claims available/partial/review-required UX;
- safe validation/export controls;
- explicit draft/legal boundary;
- v1 UX non-regression.

### AI-CONV-006 — Offline E2E/regression/security QA

Scope:

- APP-002 → P2-006 synthetic E2E;
- splicing/tamper/config mismatch tests;
- cleanup/logging/security regression;
- v1 non-regression;
- P2-006 output/visual QA when applicable.

### Later, separately authorized gates

- funded provider/product-runtime semantic evaluation under EVAL-001 or a new approved task;
- real/confidential research-data evaluation only after data/privacy authorization;
- BLK-003 production security/auth/storage/retention work;
- production/public deployment and release authorization.

### 13.1 Proposed execution-gate matrix

This matrix completes planning only. It does not authorize any listed task, select a reviewer model, enroll Workflow V2 or grant merge/deployment authority.

| Task | Required inputs | Expected outputs | Minimum evidence before review | Reviewer profile requirement | Stop conditions |
|---|---|---|---|---|---|
| AI-CONV-002 | Valid APP-002 envelope, compatible structured analysis, released P2-002…P2-006 contracts/configs, explicit Human task authorization | Internal offline orchestrator/session revision model; deterministic synthetic P2-002→P2-005 flow; optional P2-006 call through released validator | Focused orchestration/provenance tests; existing P2-002…P2-006 regressions; v1 non-regression; diff proves no schema/Claims-semantic change | Current authorized workflow only: V1 Antigravity read-only fixed-SHA reviewer with exact Human-authorized model/profile, or explicitly enrolled V2 reviewers if separately authorized | Any released schema/Claims semantic change, provider/network use, real/confidential data, persistent production storage/auth change, failed required CI/review |
| AI-CONV-003 | Explicit Human Claims-semantics decision; approved authority/evidence model; compatibility/migration decision | Versioned proposal/implementation for solution membership, essentiality, method/process and composition authority; audited Human-confirmation semantics if approved | Positive and negative authentic-style synthetic provenance cases; migration/compatibility evidence; no inferred authority | Reviewer/model must be explicitly authorized for this task; if V2-enrolled, required Security/Quality streams and MANUAL_EXTERNAL gates apply | Missing Human Claims decision, breaking schema/contract without approval, unsupported semantic promotion, real/confidential data or provider use without separate authorization |
| AI-CONV-004 | Authorized AI-CONV-002 output and frozen additive API contract | Separate v2 session/status/review/validate/export endpoints; stale revision/error model; v1 routes unchanged | API contract tests, stale/digest/source-mismatch tests, v1 backend regression, security/logging checks | Current task-authorized independent fixed-SHA reviewer(s); exact model/profile recorded | Reusing/changing v1 response contract, accepting package-only export authority, auth/storage/tenant design beyond approved local boundary, unresolved security finding |
| AI-CONV-005 | Authorized v2 API/review contract and approved UI states | Additive v2 review/export UX with evidence/revision/Claims status and draft boundary | Frontend type/unit/E2E coverage; v1 UX regression; stale-session/export-block tests; accessibility checks | Current task-authorized independent fixed-SHA reviewer(s); exact model/profile recorded | UI fabricates/suggests unsupported Claims, hides Human-review requirement, changes v1 by default, exposes confidential paths/content |
| AI-CONV-006 | Frozen authorized offline v2 integration candidate | Synthetic APP-002→P2-006 E2E/regression/security report; tamper/splice/config/cleanup evidence; P2-006 visual QA when applicable | Exact-SHA CI plus negative provenance suite, v1 regression, output count/content markers, safe logging/cleanup evidence | Independent review under the workflow explicitly selected for AI-CONV-006; exact model/profile recorded | Any unresolved CRITICAL/HIGH finding, failed CI, secret/data exposure, package-only validation bypass, real/provider/production scope creep |
| Later funded runtime evaluation | Separate provider/model/budget authorization plus permitted corpus/data route | EVAL-001-compatible runtime evidence and Human semantic decision | Exact model/config/prompt/schema/source/output hashes; applicable EVAL-001 metrics; provider-cost evidence | Separately authorized semantic/review profile; Human remains final semantic acceptance authority | Budget/provider not approved, real/confidential data rights unresolved, BLK-003/security gate unmet, attempt to infer production/legal readiness |

For AI-CONV-001 specification review itself, Issue #108 leaves the independent reviewer/model to be explicitly agreed. Therefore the immutable handoff must record the reviewer profile as `PENDING_HUMAN_SELECTION` until a specific authorized Antigravity model/profile is chosen. Availability of Gemini 3.8 Flash High does not by itself grant that authorization, and a P2-007-specific substitution cannot be generalized to AI-CONV-001.

## 14. Explicit Human decisions required before implementation or later rollout

### 14.1 Immediate specification decision

Human must explicitly accept/freeze or request changes to AI-CONV-001 v0.1.1 before any implementation task begins.

### 14.2 Implementation authorization

Human must explicitly authorize each implementation task ID and its scope/acceptance criteria. Issue #108/AI-CONV-001 does not authorize AI-CONV-002+ implementation.

### 14.3 Claims semantics

Before AI-CONV-003 or any semantic expansion, Human must decide:

- what evidence establishes solution-element membership;
- what establishes `ESSENTIAL` versus optional/conditional/unknown;
- whether and how method/process step essentiality can be represented;
- whether and how composition membership/mandatory amounts can be represented;
- which Claim families are desired/allowed;
- whether Human confirmation is an authoritative input and what audit evidence makes it valid;
- whether schema/contract changes are permitted and what compatibility/migration policy applies.

### 14.4 Workflow governance

Human must choose whether each future AI-CONV implementation task uses the current authorized V1 governance path or is explicitly enrolled in Workflow V2 under the accepted activation record. AI-CONV-001 does not enroll or activate Phase H/V2.

### 14.5 Provider/model/budget

Any live model/provider usage, provider configuration change, external retrieval, paid call or budget increase requires separate authorization. Current budget remains 0 and EVAL-001 PRODUCT_RUNTIME remains outside this specification.

### 14.6 Real/confidential data

Before using real, confidential or unpublished research, Human must approve legal right to process, provider/data route if any, storage, access control, retention/deletion, backup/legal-hold policy and permitted test/evaluation use.

### 14.7 Production

Authentication, authorization, tenant isolation, private persistent storage, production retention, security acceptance, public deployment and production release each require separate approval. BLK-003 is not resolved by this specification.

### 14.8 Rendering/assets/dependencies

Any renderer architecture change, new external dependency/service, or use of authentic source figures/assets requires separate approval including rights/manifest requirements where applicable.

## 15. Blockers and current disposition

| Blocker | Current disposition |
|---|---|
| Authentic source → positive Claims eligibility not established | OPEN; fail closed to `HUMAN_CONFIRMATION_REQUIRED`; resolve only in separately authorized AI-CONV-003 |
| Workflow V2/Phase H enrollment | NOT AUTHORIZED / NOT ACTIVE |
| Provider/API budget | 0 / NOT AUTHORIZED |
| Product-runtime semantic acceptance | NOT DETERMINED; outside AI-CONV-001 |
| Real/confidential research data | NOT AUTHORIZED |
| Production security/auth/storage/retention | BLK-003 OPEN |
| Production/public release | NOT AUTHORIZED |

## 16. Specification review checklist

Reviewers should verify that this proposal:

1. matches the exact baseline interfaces and current public v1 separation;
2. preserves all released P2-003 and P2-004 Claims semantics;
3. retains the P2-005/P2-006 seven-input provenance trust boundary;
4. treats authentic no-Claims as a valid fail-closed result;
5. introduces only additive future integration requirements;
6. does not imply implementation, V2 enrollment, provider funding, real-data use or production approval;
7. clearly separates orchestration implementation from future Claims semantic expansion.

## 17. Readiness conclusion

AI-CONV-001 v0.1.1 is **READY FOR SPECIFICATION REVIEW**.

The recommended next step is Human review/freeze of this specification. Implementation remains **NOT AUTHORIZED**. Phase H remains **NOT ACTIVE**. No provider budget, real/confidential data use, production readiness or public release authority is granted by this document.
