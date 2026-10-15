# AI-CONV-003 — Authentic source-to-Claims semantic authority: specification proposal

## 1. Metadata and status

| Field | Value |
|---|---|
| Task | AI-CONV-003 |
| Specification version | 0.1.0 |
| Status | **PROPOSED — HUMAN CLAIMS-POLICY DECISION REQUIRED; NOT APPROVED OR FROZEN** |
| GitHub issue | [#116](https://github.com/nshaokiet/ai-ip-description-generator/issues/116) |
| Task authorization | Human requested next task on 2026-10-15: **SPECIFICATION PREPARATION ONLY** |
| Baseline main | `d926e5e9f35b350aa9e6a8fe3c099e1a5386010b` |
| Parent architecture | [AI-CONV-001 v0.1.1](AI-CONV-001-source-grounded-uspto-v2-orchestration.md), accepted/frozen |
| Internal implementation input | [AI-CONV-002](AI-CONV-002-offline-orchestration-implementation.md), merged via PR #112 |
| Workflow for this proposed specification | **V1**, with standing Gemini 3.8 Flash High / Antigravity STRICT READ-ONLY independent review |
| Data / model / cost | Offline synthetic only; no provider/API, zero authorized paid runtime budget |
| Product / rollout | No public/runtime Claims activation, no Phase H/V2 enrollment, no production or Render change |

The Human request to continue to a new task authorizes *preparing this proposal*. It does not select a substantive patent-Claims semantic policy, approve schema changes or authorize implementation. The seven decisions in §6 remain mandatory Human decisions. This document is not a filing strategy or legal-opinion determination.

## 2. Problem and current evidence boundary

The released internal chain is:

1. APP-002 ExtractionInputEnvelope + validated AI-001 structured analysis.
2. P2-002 source-grounded INVENTION_RECONSTRUCTION v1.0.0.
3. P2-003 USPTO_SPECIFICATION_DRAFT v2.0.0.
4. P2-004 standalone SUPPORTED_DRAFT_CLAIMS v1.0.0.
5. P2-005 USPTO document package with seven-input full provenance validation.
6. Optional P2-006 offline DOCX/PDF renderer, through the same provenance validation.
7. AI-CONV-002 ephemeral session/orchestration, deterministic revisions, strict source/digest/cleanup checks.

The **observed documented limitation** is that authentic-style APP-002 → P2-002 reconstruction may not contain a supported statement of which elements form a *claimed solution*, which ones are *essential*, whether a method step is essential, or which materials and amounts are *mandatory parts of one composition*. An ordinary ordered list, a material mention or a natural-language inference is not a versioned authority for these predicates.

P2-004 positive **standalone** structural fixtures demonstrate safe projection when those predicates *already exist*; they do not prove that an arbitrary real paper can produce them.

The valid default outcome is **`HUMAN_CONFIRMATION_REQUIRED` plus `claims=[]`**. This indicates successful fail-closed processing, **not a pipeline exception** and not proof of a missing model call.

### 2.1 Invariants that remain released and unchanged

- P2-003 remains a disclosure draft, not a Claims generator: `claims=[]`, `review_boundary.claims_runtime_implemented=false`.
- P2-004 may emit a positive supported draft Claim only when its **existing** family-specific eligibility predicates are satisfied.
- P2-005/P2-006 require the complete retained original seven-input provenance bundle; a package, digest, UI checkbox or unattested authority receipt alone cannot authorize export.
- `UNKNOWN`, `OTHER`, unsupported `INFERENCE`, co-occurrence, optional/conditional language and missing evidence never become `ESSENTIAL`, solution membership, mandatory method steps or mandatory composition amounts automatically.
- Unsupported/contradictory source material stays unresolved. Human legal review remains required; filing-readiness is never inferred.

## 3. Semantic authority model alternatives — no selection yet

| Option | Proposed authority | Benefit | Primary failure mode | Decision |
|---|---|---|---|---|
| A — Explicit source assertions only | Versioned structured source/evidence records affirm each predicate; the authority must be independently verified | Minimal new actor/audit surface | Many authentic papers do not explicitly state patent-Claims essentiality | PENDING HUMAN |
| B — Audited Human confirmation | Qualified authorized Human explicitly confirms each scoped predicate against displayed evidence, with revocation/invalidation | May resolve legitimate author ambiguities | Actor identity, qualifications, audit/retention, consent and tamper protection are not yet approved for a product | PENDING HUMAN |
| C — Hybrid evidence + scoped Human confirmation | Require source-linked predicate plus an authenticated, revision-bound Human attestation for positive semantic promotions | Stronger control for uncertain essentiality and composition semantics | Requires both a versioned contract and an approved local/production authority model | PENDING HUMAN |

**Recommended design direction for Human consideration: C (hybrid), not an adopted policy.** The recommendation is limited to a future authorized synthetic/offline proposal. Production identity/permission, signed attestations or legal acceptance cannot be asserted under current BLK-003 restrictions. The Human may instead select A, B, a narrower family set or continue the safe no-Claims mode.

## 4. Proposed typed semantic-decision boundary (not released)

A separate, versioned *candidate* semantic-authority manifest may record a small set of affirmative/negative/unresolved predicates. Its existence is conceptual only; **do not implement or pass it into released P2-002 through P2-006 as an eighth hidden input**.

### 4.1 Proposed scoped predicate families

| Predicate | Proposed scoped target | Conservative interpretation |
|---|---|---|
| SOLUTION_MEMBERSHIP | solution_id + element_id | Belongs to the specifically identified candidate solution, not just the paper |
| ELEMENT_ESSENTIALITY | solution_id + element_id | ESSENTIAL / OPTIONAL / CONDITIONAL / UNKNOWN; only appropriately supported ESSENTIAL may meet an existing eligibility rule |
| METHOD_STEP_MEMBERSHIP | method_id + step_id | Step is part of the candidate method, not just adjacent in source |
| METHOD_STEP_ESSENTIALITY | method_id + step_id | Mandatory process step, distinct from ordering/sequence |
| COMPOSITION_MEMBERSHIP | composition_id + material_id | Material belongs to the identified composition, not mere co-occurrence |
| COMPOSITION_AMOUNT_MANDATORY | composition_id + material_id + amount_id | Exact amount/range/relationship is mandatory; mere examples and measured ranges are insufficient |
| EVIDENCE_CONFLICT | target + conflicting source IDs | Positive authority remains blocked until explicit reconciliation is versioned and independently reviewed |

These names and values are **design placeholders**, not existing enum fields or claims about released interface compatibility.

### 4.2 Minimal candidate record

A future authorized manifest should bind, at minimum:

- Unique decision ID, candidate manifest schema version, document_id and original document SHA-256.
- APP-002 source-unit evidence IDs and precise locators; references to the validated AI-001/P2-002 source identities.
- Predicate family, typed target IDs, candidate value, claimed solution/method/composition scope and explicit reason.
- Authority type **SOURCE_EXPLICIT / HUMAN_ATTESTED / HYBRID / UNRESOLVED**, never implicit from UI display/click.
- For Human confirmation *only if approved*: actor role, actor/authentication reference, timestamp, assertion and evidence snapshot hashes, decision/review revision, attestation identity, invalidation and revocation references.
- Exact AI-CONV-002 session/revision token and canonical hashes of all relevant input/configuration objects; deterministic source identity checks.
- Conflict/missing statuses and immutable relationship between the authority record and eligible or rejected draft Claims.
- No untrusted source text, unsigned boolean flag or path alone treated as authenticated authority.

### 4.3 Binding and replay prevention

- Input/source SHA, relevant evidence IDs, target set, reconstruction identity, spec and Claims configs must match. Cross-document splice, missing evidence, duplicate target, digest drift, conflicting decisions, revoked actor and stale revision **reject**.
- Changing the source/analysis invalidates **all** dependent confirmations; changing reconstruction/method/composition/Claims configuration invalidates the applicable decisions and downstream Claims/package/render identities.
- No confirmation can survive a revision if its source, target, predicate or evidentiary meaning changes. Identical-content reuse requires explicit authorized revalidation, not silent transfer.
- No authority record by itself authorizes package validation/render; a later contract design must preserve or **explicitly version** the full P2-005/P2-006 provenance boundary. A silent eighth input or validator bypass is prohibited.
- In the absence of an approved actor identity/audit design, Human confirmation can only be a **synthetic test proposal** with zero production authority.

## 5. Claim-family eligibility decision matrix (PROPOSED)

| Family | Required positive authority before future eligibility | Fail-closed cases |
|---|---|---|
| SYSTEM / APPARATUS | Exact candidate solution membership + explicitly supported structural core essentiality + grounded components/relationships | UNKNOWN or OPTIONAL core, component from unrelated solution, inference-only support, conflicting evidence |
| METHOD / PROCESS | Exact named process membership and per-step essentiality + source-grounded ordering/relations if mandatory | Sequence alone, absent step-essentiality, borrowed step across processes, contradictory relations |
| COMPOSITION | Exact composition membership and mandatory amounts/relationships with source evidence and explicit applicability | Materials merely co-mentioned, concentration listed as example, amount/range without mandatory authority, multiple compositions spliced |

All family decisions are **PENDING HUMAN**. A selected family must still pass its released P2-004 eligibility checks and approved contract rules. No positive Claims are promised for authentic sources.

## 6. Explicit Human decision register — required before implementation

| ID | Decision required | Default pending decision |
|---|---|---|
| HD-01 | What source evidence/authority establishes solution-element membership? | NO POSITIVE PROMOTION |
| HD-02 | What establishes ESSENTIAL versus OPTIONAL, CONDITIONAL and UNKNOWN? | UNKNOWN REMAINS UNKNOWN |
| HD-03 | May METHOD/PROCESS step membership and essentiality be represented, by whom and with what proof? | NO METHOD PROMOTION |
| HD-04 | May COMPOSITION membership/mandatory amount semantics be represented, by whom and with what proof? | NO COMPOSITION PROMOTION |
| HD-05 | Which Claim families (SYSTEM/APPARATUS, METHOD/PROCESS, COMPOSITION) are in scope? | NO NEW FAMILY ENABLED |
| HD-06 | Is Human confirmation an authoritative input? Who may attest, authenticate, reject, revoke and audit it? | NO HUMAN-ATTESTATION AUTHORITY |
| HD-07 | Are schema/contract version changes allowed; additive vs breaking, compatibility, migration and seven-input validation policy? | NO RELEASED CONTRACT CHANGE |

HD-01–HD-07 need a dated explicit Human choice, precise scope and acceptance. Marking a row in this proposed document is not itself approval. A later frozen spec and independent security/quality evaluation are required for any expanded semantics; use Workflow V1 reviews unless separately enrolled in V2 with its independent streams.

## 7. Compatibility / migration proposal

1. Freeze current released semantics as the compatibility baseline, including P2-003 v2 and P2-004 v1.
2. Prepare versioned candidate overlay/adapter contracts rather than mutating old JSON in place. Record exact migrations and reading/validation of older packages.
3. **No silent reinterpretation** of existing no-Claims results, `HUMAN_CONFIRMATION_REQUIRED` statuses or prior validations as eligible positive Claims.
4. If source assertions alone are proposed as authority, require field-level traceability and conflict tests; do not presume scientific-paper prose establishes patent-legal indispensability.
5. If Human attestations are proposed, define actor role authentication, anti-replay, immutable audit and rollback/revocation requirements. BLK-003 remains open, so product/tenant/persistent implementation is separately gated.
6. Keep AI-CONV-002 revision/session behavior and seven-input P2-005/P2-006 provenance; any needed change is explicitly versioned and must undergo dedicated migration/compatibility review.
7. No public v2 API route, frontend confirmation UI, release or provider call is included in this task.

## 8. Threat model and mandatory negative tests for future authorized implementation

- **Splicing:** different document, solution, method, composition or evidence ID is injected → reject.
- **Essentiality escalation:** UNKNOWN/OTHER/INFERENCE/OPTIONAL/CONDITIONAL promoted without approved authority → reject.
- **Inconsistent Claims support:** claim from different source, missing step, conflicting amount/relationship → reject.
- **Synthetic Human spoofing:** checkbox, display action, forged/stale actor, missing role or unverified actor reference → no real authority.
- **Revocation and freshness:** revoked decision, changed document hash, stale revision or changed config → invalidate affected Claims/package/render.
- **Tamper/replay:** altered authority payload/digest, reuse across sessions/documents, unsigned record, path/digest-only package → reject.
- **Privacy:** source prose/filenames, personal data, tokens, actor secrets, server paths and exception traces must not leak through status/log/error outputs.
- **Prompt injection:** source text treated as data, never instructions or new authority.
- **False success:** valid no-Claims pipeline must remain success with Human confirmation required, not be categorized as an exception.
- **Production separation:** no simulated/offline actor trusted as a real authenticated product identity.

## 9. Acceptance plan (specification gate now; executable gate later)

| ID | Specification acceptance check |
|---|---|
| SP-01 | Correct inventory of released components and current Claims fail-closed limitation, without claiming authentic positive E2E |
| SP-02 | A/B/C comparison with explicit non-adopted recommendation and Human gate |
| SP-03 | Typed predicate/target/evidence/authority metadata proposal with clear non-released status |
| SP-04 | Per-family SYSTEM/APPARATUS, METHOD/PROCESS and COMPOSITION positive/negative authority matrix |
| SP-05 | HD-01–HD-07 marked pending, no invented Human decision |
| SP-06 | Safe backward compatibility/versioning and seven-input P2-005/P2-006 integrity plan |
| SP-07 | Freshness/revocation/cross-document/stale-config/privacy/prompt-injection negative scenarios |
| SP-08 | Explicit scope excludes Claims implementation, providers, real data, deployment and V2 enrollment |
| SP-09 | V1 reviewer actual model/session, fixed SHA, findings and independent PASS/REQUEST CHANGES/BLOCKED required |
| SP-10 | Required exact-head CI + fresh Render no/off + protected merge; no closure without exact-main CI |

**Future implementation criteria, not approved now:** positive and negative authentic-style **synthetic** fixture tests under an **approved/frozen authority contract**, unchanged P2-004 regression, unchanged P2-003 fields, rejection of all unapproved semantic promotions, seven-input provenance, revision invalidation, output review/legal banner, v1 regression, negative API/runtime checks where separately authorized.

No semantic quality/fidelity metric or provider result can be declared PASS from these offline structural fixtures. A later funded EVAL-001-compatible semantic assessment requires distinct provider/data approval.

## 10. Execution and dependency gates

1. Create this proposed specification and a docs-only PR from the exact verified main baseline. Do not change the released stage code/tests or governance rules in the proposal.
2. Independent **Gemini 3.8 Flash High / Antigravity STRICT READ-ONLY** review of exact final spec SHA; actual model and session, all changed files, security/test findings, explicit verdict.
3. Required GitHub CI SUCCESS on exact head; fresh main/scope/diff/no-secret/Render no/off and protected expected-head merge preflight.
4. Documentation merge only after all gates; postmerge exact-main CI/readback. **Human approval/freeze of HD-01–HD-07 remains a separate substantive decision even if this proposal merges.**
5. Only after Human freezes the chosen policy may a new explicit implementation authorization be considered. AI-CONV-004 backend API/005 frontend/006 E2E, provider budget, production and Phase H are separate tasks; do not infer approval.

## 11. Open risks and current disposition

- **R-01 HIGH:** Scientific-paper statements may not establish patent-Claims essentiality; default no promotion.
- **R-02 HIGH:** Human identity/authorization is not product authenticated while BLK-003 remains open; no live attestation path.
- **R-03 HIGH:** Future semantic adapter could break P2-005 seven-input provenance if added implicitly; explicit versioned migration necessary.
- **R-04 MEDIUM:** Real papers may legitimately produce no Claims; UX must distinguish review-required from processing error in a separately authorized frontend task.
- **R-05 MEDIUM:** Current GOV-REVIEWER-001 Issue #113 and AI-CONV-002 Issue #111 are open for independent administrative closeout. Their unresolved exact-main CI/task-state evidence must not be labeled completed by this specification.

**Disposition: PROPOSED SPECIFICATION ONLY — HD-01–HD-07 PENDING HUMAN; NO CLAIMS SEMANTIC IMPLEMENTATION AUTHORIZED.**
