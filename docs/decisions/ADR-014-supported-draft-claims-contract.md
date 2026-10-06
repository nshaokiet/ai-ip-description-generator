# ADR-014 — Standalone Supported Draft Claims Contract

| Field | Value |
|---|---|
| ADR ID / version | ADR-014 / **0.1.0** |
| Status | **ACCEPTED — P2-004 SPECIFICATION ARCHITECTURE BASELINE; IMPLEMENTATION NOT AUTHORIZED** |
| Date / owner / author | 05/10/2026 GMT+7 / Human — Product Owner / Codex |
| Authorization | `HUMAN-P2-004-CLAIMS-SPECIFICATION-2026-10-05` — specification only |
| Baseline | `60b0fdb4ed68cd8c701576cf49a8b620052bb14b` |
| Task / normative contract | [P2-004 specification 0.1.0](../tasks/P2-004-supported-draft-claims.md); standalone SUPPORTED_DRAFT_CLAIMS v1.0.0 |
| Independent reviewer | Gemini 3.1 Pro High / Antigravity read-only; **PASS / findings NONE** |
| Implementation | **NOT AUTHORIZED**; no code or production JSON Schema |
| Review attribution / reviewed SHA | Human-supplied external fixed-SHA review, not GitHub-native approval; `89eef2af3fcc4105b66acf02f9504b2887c222ac` |
| Acceptance criteria / fixture plan | AC-01…AC-48 **PASS**; 54-case future synthetic fixture plan **ADEQUATE** |
| PR / merge SHA | #80 — **MERGED**; `9ac1889e44bca080e21efb5bbbd2ebf5c3140293` |
| Exact-head PR CI / main CI | `37255116233` / `37262324108` — **SUCCESS** |
| Status reconciliation / date | `HUMAN-P2-004-SPECIFICATION-STATUS-RECONCILIATION-2026-10-06` / 06/10/2026 GMT+7 |

## Context and source evidence

P2-003 is CLOSED / COMPLETED — MERGED after reviewed implementation/closeout and
successful main CI; its deterministic generator produces a P2-001 v2 draft with
Claims MISSING/empty, no preamble, empty claim_support and runtime-false boundary.
The source baseline is the P2-003 final reconciliation merge above; no existing
P2-004 contract or ADR-014 exists at that baseline.

P2-001 `schemas/uspto-specification/v2.0.0/uspto-specification.schema.json` already
defines claims_section, claim, claim_element and claim_support. It simultaneously
fixes `$defs.review_boundary.properties.claims_runtime_implemented.const=false`.
Claims-shaped components are not an implemented integrated Claims runtime.
Mutating that schema or assembling a runtime-true replacement would exceed this
Human authorization. The specification must expose the distinction explicitly.

Technical authority is P2-002 `INVENTION_RECONSTRUCTION` v1.0.0; disclosure
authority is P2-003 `USPTO_SPECIFICATION_DRAFT` v2.0.0. Released P2-003 validator
requires reconstruction and the actual generation config for exact projection
validation. Its output does not persist that config. Its source document ID is
not a content hash of all reconstruction/draft text, so P2-004 also binds content.

## Proposed decision

1. Define a **standalone SUPPORTED_DRAFT_CLAIMS v1.0.0** package, strict shapes,
   families, claims, effective elements, source identity, review audit and immutable
   Human/IP boundary. Document the contract, not a production JSON Schema.
2. Keep P2-001/P2-002/P2-003 unchanged. Specify a pure future component projection
   to P2-001 claim/element/support shapes; keep richer audit and identity in a
   standalone sidecar. Do not emit or claim an assembled replacement P2-001 draft.
3. Require dual closure: eligible P2-002 entities/evidence/fields AND exact
   P2-003 PRESENT invention-disclosure paragraphs with matching pointers/evidence.
   Background/Field/Related Art alone cannot justify invention Claims.
4. Initial emitted grounding is **SOURCE_FACT/PARAPHRASE only**, with literal
   field integrity. Reject inference/generalization/proposed/unaudited Human
   states, unresolved conflict taint and incomplete required core. This is more
   conservative than P2-003 prose eligibility, not semantic/legal acceptance.
5. Explicit caller claim-type requests and selected existing solution prevent
   invisible strategy inference. Required actual P2-003 config sidecar verifies
   the immutable upstream draft; it supplies no extra technical authority.
6. Use closed deterministic templates, exact technical terms/values/relationships,
   ordered candidates, numbering, content-bound SHA identity and upstream-based
   canonical-render validation. No LLM/synonym/claim-breadth optimizer.
7. One independent per family, single-parent depth-one dependents; one supported
   narrowing unit/group per dependent. No multiple dependencies or claim chains.
8. Require UNREVIEWED draft and human_ip_review_required=true, filing_ready=false,
   legal_advice=false, patentability/novelty assessments=false and
   claim_scope_optimized=false. No auto-Human/attorney approval or filing state.
9. No provider/API, real data, raw-paper reinterpretation, legal/patentability
   conclusions, frontend/DOCX/runtime/deployment/production or downstream authority.
10. Future P2-001 amendment, specification-with-claims assembly, runtime-true
    transition, Human/IP review workflow or DOCX Claims integration requires
    separate Human authorization, versioning, independent review and tests.

## Released-model feasibility and consequences

P2-002 element has essentiality; method_step and parameter do not. Composition
membership and structured amounts/mandatory component semantics are not defined.
The specification therefore permits eligible SYSTEM/APPARATUS cores but makes
METHOD/PROCESS/COMPOSITION requests explicit confirmation-required entries with
no generated claims under current released authority. Parameters cannot silently
be declared essential; potentially necessary quantities gate a core rather than
being omitted. Conditional element descriptions remain complete opaque supported
units; no missing structured condition is invented.

This is a deterministic, implementable refusal policy, not a reason to amend
P2-001 now. Independent review must challenge the deliberately limited capability
and conditional future-positive fixture cases. Any future upstream authority
extension is separate, not approved here. Typed requests alone never prove support.

Benefits: compatibility honesty, auditable support and deterministic projection,
no legal-value ranking, no unsupported assembled runtime claim. Costs: substantial
conservative refusals, awkward exact-source draft grammar, no current positive
method/composition generation, preserved sidecar required for rich provenance.
These limits cannot be hidden by marking the review package PRESENT/approved.

## Alternatives not selected

- Flip P2-001 runtime-false constant or embed generated Claims into supplied
  P2-003: exceeds authorization and contradicts its reviewed exact projection.
- Use P2-003 prose alone: can launder upstream inference/unsupported content.
- Reopen raw source/APP-002/AI-001 or use a provider: outside this specification
  boundary; introduces a second semantic authority and unapproved data/cost path.
- Infer step essentiality/composition strategy or optimize legal breadth: absent
  structured authority, non-auditable strategy and unsafe silent promotion.
- Reject standalone design altogether: unnecessary; structural families and
  explicit refusal packages are possible without changing existing contracts.

## Review and adoption gates

### Current adoption status — 06/10/2026

Independent specification review: **Gemini 3.1 Pro High / Antigravity read-only**,
**PASS / findings NONE** on reviewed SHA `89eef2af3fcc4105b66acf02f9504b2887c222ac`.
Evidence attribution: **Human-supplied external independent fixed-SHA review;
not GitHub-native approval**. AC-01…AC-48 **PASS**; **54-case future synthetic
fixture plan ADEQUATE** (plan review, not executed runtime tests).
Exact-head specification PR CI [`37255116233`](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/37255116233)
**SUCCESS**; [PR #80](https://github.com/nshaokiet/ai-ip-description-generator/pull/80)
**MERGED** at `9ac1889e44bca080e21efb5bbbd2ebf5c3140293`; post-merge push/main CI
[`37262324108`](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/37262324108)
**SUCCESS** on that exact merge.
ADR-014 is **ACCEPTED — P2-004 specification architecture baseline** only.
Specification review + merge + main CI gates **SATISFIED**.
P2-004 implementation **NOT AUTHORIZED**; Claims runtime **NOT IMPLEMENTED**.
Next gate: **SEPARATE HUMAN IMPLEMENTATION AUTHORIZATION REQUIRED**.

ACCEPTED applies only at specification level: no runtime implementation, released
schema, generated Claims, P2-001 change, filing-ready state or production approval.
The decision narrative and technical semantics remain version 0.1.0 unchanged.

### Historical pre-review gates — preserved

The following passage records the original proposed/pre-review state and is
superseded only for current status by the accepted specification evidence above.

This ADR is **proposed**, not independent approval. P2-004 AC-01…AC-48, the
54-case synthetic future plan and especially standalone compatibility, strict
support/essentiality feasibility, canonical rendering and legal exclusions require
fixed-SHA Gemini 3.1 Pro High / Antigravity read-only review. No decision is
fabricated. Exact-head PR CI SUCCESS is required before handoff. **Do not merge
in this task**. Specification PASS, later authorized merge and main CI still
require separate Human implementation authorization before any runtime work.

MCP: BLOCKED BY TOOL CAPABILITY — Unknown task: P2-004 (observed); no state/lease
fabricated. BLK-003 OPEN; PRODUCT_RUNTIME DEFERRED — AWAITING FUNDING; semantic
acceptance NOT DETERMINED; provider NOT GRANTED/budget 0/calls NONE; real/confidential
data NOT AUTHORIZED; arbitrary real-paper conversion NOT ENABLED; Claims runtime
NOT IMPLEMENTED; production NOT APPROVED / NOT PERFORMED.

## Version history

| Previous | New | Date | Author | Change / reason | Reference | Breaking |
|---|---|---|---|---|---|---|
| None | 0.1.0 | 05/10/2026 | Codex | Propose standalone supported draft Claims and component-only handoff without altering released runtime-false/schema boundaries | HUMAN-P2-004-CLAIMS-SPECIFICATION-2026-10-05; P2-004 specification 0.1.0 | No — existing contracts unchanged |
