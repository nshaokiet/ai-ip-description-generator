# P2-004 — Supported Draft Claims Contract & Offline Claims Generation Pipeline

## Metadata

| Field | Value |
|---|---|
| Task ID / specification version | P2-004 / **0.1.0** |
| Status | **IMPLEMENTATION — INDEPENDENT REVIEW PENDING** |
| Human authorization | `HUMAN-P2-004-IMPLEMENTATION-2026-10-06` |
| Authorized baseline | `b1085337c8f16c4bb72574bfb45e27741290ca90` |
| Specification authorization / baseline | `HUMAN-P2-004-CLAIMS-SPECIFICATION-2026-10-05` / `60b0fdb4ed68cd8c701576cf49a8b620052bb14b` — historical specification evidence |
| Implementation branch / PR | `feat/p2-004-supported-draft-claims` / #82 — **OPEN / UNMERGED** |
| Executable SHA / exact-head CI before governance handoff | `411b17a6ed39885b47af9932c9cf44d4b498db9e` / `37423007016` — **SUCCESS** |
| Date / owner / author | 06/10/2026 GMT+7 / Human — Product Owner / Codex |
| Independent reviewer | Specification: Gemini 3.1 Pro High / Antigravity read-only **PASS / findings NONE**; implementation: **PENDING** |
| Phase / implementation | **IMPLEMENTED ON BRANCH — INDEPENDENT FIXED-SHA REVIEW PENDING; PR OPEN / UNMERGED** |
| Input | Validated P2-002 `INVENTION_RECONSTRUCTION` v1.0.0 AND validated P2-003 `USPTO_SPECIFICATION_DRAFT` v2.0.0 |
| Output contract identity | Standalone `SUPPORTED_DRAFT_CLAIMS` **v1.0.0**; production JSON Schema created at `schemas/supported-draft-claims/v1.0.0/supported-draft-claims.schema.json` |
| Architecture record | [ADR-014](../decisions/ADR-014-supported-draft-claims-contract.md) — **ACCEPTED as specification architecture baseline** |
| MCP | **BLOCKED BY TOOL CAPABILITY — Unknown task: P2-004**; actual read-only tool result, no state/lease/checkpoint fabricated |
| Existing P2-003 | **CLOSED / COMPLETED — MERGED**; unchanged |
| Review attribution | Human-supplied external independent fixed-SHA review; **not GitHub-native approval** |
| Reviewed SHA | `89eef2af3fcc4105b66acf02f9504b2887c222ac` |
| PR / exact-head CI | #80 — **MERGED**; `37255116233` — **SUCCESS** |
| Specification merge / main CI | `9ac1889e44bca080e21efb5bbbd2ebf5c3140293`; `37262324108` — **SUCCESS** |
| Reconciliation authorization / date | `HUMAN-P2-004-SPECIFICATION-STATUS-RECONCILIATION-2026-10-06` / 06/10/2026 GMT+7 |

## 1. Purpose, authority and non-goals

This specification proposes a conservative, source-grounded **draft** Claims
package and a deterministic synthetic/offline producer/validator design. It is
not runtime implementation, claim-scope optimization, prosecution strategy,
novelty/prior-art/patentability analysis, freedom-to-operate analysis, legal advice,
filing-ready preparation, or authorization to use actual research papers.

Every output remains **DRAFT — SOURCE-GROUNDED — HUMAN/IP-REVIEW REQUIRED**.
Support validation checks structured integrity and exact reviewed projection;
it does not prove scientific truth, semantic entailment, legal sufficiency or
appropriate protection scope. Human/IP-specialist review is mandatory.

Normative words MUST/MUST NOT below govern a **future separately authorized**
implementation. No production schema, service, validator, fixture or runtime
configuration is delivered by this specification task.

## 2. Canonical inputs and immutable compatibility boundary

P2-002 is the sole structured technical/evidence authority. P2-003 is the
filing-style specification-disclosure authority. Neither substitutes for the
other. No raw PDF/DOCX, APP-002 envelope or AI-001 analysis is a P2-004 semantic
input. Original upstream validation against those sources is a caller obligation;
P2-004 rechecks available integrity, not the original reconstruction projection.

P2-003's expected input state is valid and intentional:

```text
claims.status = MISSING
claims.claims = []
claims.preamble is absent
review_package.claim_support = []
review_boundary.claims_runtime_implemented = false
```

The released P2-001 schema at
`schemas/uspto-specification/v2.0.0/uspto-specification.schema.json` defines
`$defs.claims_section`, `$defs.claim`, `$defs.claim_element`, `$defs.claim_support`,
but its `$defs.review_boundary` fixes `claims_runtime_implemented` to **false**.
P2-004 MUST NOT modify or produce an assembled replacement P2-001 object, change
that constant, write into the P2-003 input, or advertise a specification-with-
claims integration. Component-level mapping in Section 19 is a handoff contract,
not authorization to assemble or render it. P2-001/P2-002/P2-003, current prompts,
frontend, DOCX, dependencies and deployment remain unchanged.

## 3. Released-model feasibility and fail-closed capability table

Read the actual released fields; do not invent `reconstruction_id`, method-step
`essentiality`, parameter `essentiality`, composition membership or condition
AST fields. P2-002 `method_step` has action, sequence, input/output IDs, explicit
dependency IDs and conditions, **but no essentiality**. `parameter` has role,
value, scope and related entity IDs, **but no essentiality**. `element` has
essentiality and an optional opaque description, **but no structured condition**.

| Requested type | v1 deterministic eligibility under unchanged released inputs |
|---|---|
| SYSTEM / APPARATUS | Selected solution has a nonempty, strictly supported ESSENTIAL structural core; all required dual support and integrity gates pass |
| METHOD / PROCESS | **HUMAN_CONFIRMATION_REQUIRED**, no claims: released steps cannot establish the required ESSENTIAL-step predicate. Sequence, `related_step_ids`, action wording or caller preference are not essentiality evidence |
| COMPOSITION | **HUMAN_CONFIRMATION_REQUIRED**, no claims: released types MATERIAL/CHEMICAL_ELEMENT/BIOLOGICAL_ELEMENT and co-occurrence do not establish structured composition membership, mandatory amounts and formulation scope |
| NON_TRANSITORY_COMPUTER_READABLE_MEDIUM / OTHER | Not allowed in configuration; reject `REQUESTED_CLAIM_TYPE_UNSUPPORTED` |

This is a deliberate fail-closed v1 limitation, not a whole-task contract blocker:
SYSTEM/APPARATUS generation and review-only entries for unavailable types are
possible without changing P2-001. A future essentiality/composition authority
extension needs separate Human authorization and independent review; this task
does not propose adding fields to the released schemas or secretly granting that
extension. A caller MUST NOT manufacture missing authority through configuration.
Review must explicitly challenge these capability limits before implementation.

## 4. Strict standalone output shape

All objects below are closed: unknown properties rejected. Required fields are
exactly those named unless explicitly marked optional. Arrays preserve defined
order and are fresh nested state. Integers exclude booleans; numbers are finite.
Nonempty technical strings are copied intact, never silently trimmed, normalized,
translated or corrected. Optional properties are absent, not invented defaults.

```text
SUPPORTED_DRAFT_CLAIMS {
  schema_version: "1.0.0",
  output_type: "SUPPORTED_DRAFT_CLAIMS",
  claims_draft_id: string,
  status: PRESENT | PARTIAL_REVIEW_REQUIRED | HUMAN_CONFIRMATION_REQUIRED,
  source_identity: SourceIdentity,
  generation_config: CanonicalGenerationConfig,
  claim_families: Family[],
  claims: Claim[],
  review_package: ReviewPackage,
  review_boundary: ReviewBoundary
}
```

No fields encode HUMAN_APPROVED, ATTORNEY_APPROVED, FILING_READY or PROSECUTION_READY.
`PRESENT` means only that all requested families emitted supported drafts with
no skipped support-bearing candidates; it does not mean review completion.

## 5. Source identity, hashing and cross-input equality

`SourceIdentity` requires `document_id`, `file_name`, `media_type`,
`source_document_synthetic` (true), `p2_002_identity`, `p2_003_draft_id`,
`p2_003_content_sha256`; optional `source_sha256` exists iff present upstream.

Compare P2-002 `document_metadata` with P2-003
`document_metadata.source_document`: document_id/file_name/media_type MUST be
exact equal strings, with no case folding or Unicode normalization. SHA presence
MUST match; if present, the lowercase 64-hex values MUST match. This is stricter
than comparing only when both exist, and is compatible with P2-003's exact copy.
P2-003 language/jurisdiction MUST be en/US, synthetic MUST equal the required
caller true value. Validate P2-003's draft ID through its released business gate.
Any mismatch fails the entire request; do not combine documents or mask differing
checksums. A missing checksum on both inputs is recorded as absent, not guessed.

Canonical serialization `C(x)` for identity only: JSON, UTF-8, sorted object keys
by Unicode code point, no insignificant spaces, `ensure_ascii=false`, finite
numbers, preserve array order and exact strings. Use Python's reviewed JSON
serialization convention (`sort_keys=True`, `separators=(",", ":")`,
`ensure_ascii=False`, `allow_nan=False`); no host-dependent encodings. No hashes
are evidence of authenticity or scientific correctness.

```text
p2_002_identity = "p2-002-sha256-" + SHA256(C(entire validated reconstruction))
p2_003_content_sha256 = SHA256(C(entire validated specification))
material = C([p2_002_identity, p2_003_draft_id,
              p2_003_content_sha256, canonical_generation_config])
claims_draft_id = "p2-004-" + first 24 lowercase hex SHA256(material)
```

Length-delimited JSON array material avoids ambiguous pipe concatenation; content
hashes bind different reconstruction/specification content sharing a document ID.
No timestamps, UUID, randomness, provider IDs, environment or host state.

## 6. Narrow caller configuration and provenance

All fields are required; unknown keys fail. This is caller selection/control,
never new technical support, legal strategy approval or Human/IP confirmation.

| Field | Constraint / purpose |
|---|---|
| `language` | Exact `en` |
| `target_jurisdiction` | Exact `US` |
| `requested_claim_types` | Nonempty unique list of SYSTEM, APPARATUS, METHOD, PROCESS, COMPOSITION; canonicalize to fixed order in Section 15, never optimize/rank |
| `max_dependent_claims_per_family` | Exact integer 0…10 inclusive; no coercion, no default |
| `source_document_synthetic` | Required strict boolean; **true only** at current future runtime boundary; no default/inference/coercion |
| `selected_solution_id` | Exact existing P2-002 solution_concept ID; explicit caller choice, no first/best-solution heuristic or combination of unrelated solutions |
| `p2_003_generation_config` | Required verification sidecar: the actual narrow config used to generate supplied P2-003; validate/canonicalize with released P2-003 config gate, then validate supplied draft against reconstruction and that config |

The sidecar is necessary because P2-003 does not persist generation config and
optional `selected_title_candidate_id` can affect its exact projection. Do not
infer that selection from arbitrary source prose. This sidecar is solely for
input verification; it cannot insert Claims or loosen P2-003's existing rules.
Store the validated/canonicalized copy in canonical_generation_config.

Missing top-level provenance (including null/absent config) yields
`SOURCE_DOCUMENT_PROVENANCE_REQUIRED`; wrong provenance type yields
`INVALID_GENERATION_CONFIG`; false yields `REAL_SOURCE_NOT_AUTHORIZED` before
candidate construction. Source strings such as "synthetic=true" cannot supply
provenance. True is a caller assertion, not proof of permission. The same true
must be used in the sidecar and P2-003 source metadata. Missing/invalid sidecar
or solution selection fails input verification; there is no fallback generation.

## 7. Families and status semantics

One Family entry per requested allowed type, including blocked types; entries
are in fixed order. Required fields:

```text
claim_family_id: "CF-P2-004-" + claim_type
claim_type: allowed configured enum
selected_solution_id: exact config value
independent_claim_number: positive integer | null
dependent_claim_numbers: unique positive integer[]
status: PRESENT | HUMAN_CONFIRMATION_REQUIRED | NOT_GENERATED
support_summary: {source_paths: string[], evidence_ids: string[],
                  specification_section_ids: string[], issue_ids: string[]}
review_status: UNREVIEWED
```

PRESENT family has exactly one independent claim and 0…configured-limit
dependents. HUMAN_CONFIRMATION_REQUIRED/NOT_GENERATED has null independent,
empty dependents and **no claims**. Missing required authority/support/conflict
gives HUMAN_CONFIRMATION_REQUIRED; a supported structure demonstrably outside
the requested structural type gives NOT_GENERATED with reason. A family with a
valid core but excluded dependent candidates remains PRESENT; record its issues.

Output PRESENT iff every requested family is PRESENT and no support-exclusion
issue exists. PARTIAL_REVIEW_REQUIRED iff at least one family is PRESENT but
another is blocked/not-generated or a candidate exclusion issue exists.
HUMAN_CONFIRMATION_REQUIRED iff zero families emitted. Count-limit truncation
alone is an informational warning, not a support-exclusion issue. No empty-success
PRESENT output. Family numbering allocates only emitted claims; rejected families
never leave number gaps. All statuses remain UNREVIEWED drafts.

## 8. Claims and effective elements

Claim requires `claim_number`, `claim_type`, `independent_or_dependent`,
`depends_on`, `claim_text`, `claim_elements`, `claim_family_id`, `review_status`.
Review_status is UNREVIEWED. Claim numbers are positive, globally unique and
contiguous starting at 1. Independent depends_on=[]; dependent depends_on=[the
same family's independent number]. Only depth 1, no multiple dependencies,
chains, alternatives, self-reference, cycles or cross-family reference.

Each ClaimElement requires:

```text
element_id: "CE-P2-004-" + global 1-based zero-padded index (at least 4 digits)
sequence: 1-based contiguous within claim
text: canonical technical fragment (Section 16)
element_role: ENTITY | RELATIONSHIP | PARAMETER | CONDITIONAL_UNIT | EMBODIMENT | VARIANT
source_paths: nonempty unique P2-002-rooted JSON Pointer[]
evidence_ids: nonempty unique original evidence ID[]
specification_section_ids: nonempty positive support section ID[]
specification_support_refs: nonempty DisclosureRef[]
grounding: SOURCE_FACT | PARAPHRASE
support_status: SUPPORTED
upstream_entity_ids: nonempty unique reconstruction logical ID[]
essentiality: ESSENTIAL | OPTIONAL | CONDITIONAL | NOT_APPLICABLE
inherited_from_element_id: parent independent element ID | null
parameter_scope: EXAMPLE_ONLY | SUPPORTED_RANGE | UNKNOWN_SCOPE (optional iff PARAMETER)
relationship_type: exact released P2-002 enum (optional iff RELATIONSHIP)
```

NOT_APPLICABLE means the released entity has no essentiality field; it is not
an inferred ESSENTIAL status or a claim-eligibility grant. ENTITY preserves the
actual element essentiality; relational/parameter/embodiment/variant units use
NOT_APPLICABLE. Blocked elements never appear in emitted ClaimElement arrays;
their IDs/paths/statuses live in review issues, not phantom numbered claims.

Independent elements have inherited_from_element_id=null. A dependent's effective
model first clones all parent elements, with fresh global element IDs, unchanged
technical content/support, and inherited_from_element_id pointing to the parent's
element. Its appended local delta elements have null inheritance. Only this
delta is rendered in dependent claim_text; the dependency sentence incorporates
the parent. Support audit includes **every effective element**, including clones.
No mutable input/parent/output aliases. The pair (claim_number, element_id) is unique.

## 9. Dual-support closure and strict grounding

Every emitted element needs all of the following; mere section presence is not
support. Source paths are RFC 6901 JSON Pointers relative to the reconstruction,
resolve to known invention_model entities/conditions, and include the entity that
supplies each technical field and required reference/condition. Review-only
analysis_paths may be preserved but are not independently resolved as AI-001 input.

1. All used P2-002 entities, referenced labels, values and conditions have
   SOURCE_FACT/PARAPHRASE support and evidence IDs resolving uniquely to that
   reconstruction's review_package.evidence, same document ID. Preserve original
   IDs/locators/excerpts; no fresh evidence is invented.
2. Every copied technical string has a literal match in at least one cited
   source excerpt (exact code points; no synonym/fuzzy matching). A range pair
   must occur together with its exact units in one cited excerpt. This deliberately
   rejects non-literal paraphrases that cannot meet v1's conservative integrity
   check; PARAPHRASE labels alone do not override it.
3. `DisclosureRef` requires `section_id`, `paragraph_id`, `specification_path`
   (P2-003-rooted pointer), `reconstruction_path`, `evidence_ids`. It resolves to a
   PRESENT P2-003 paragraph whose support includes the exact reconstruction entity
   or condition path, includes the used evidence IDs, and is SOURCE_FACT/PARAPHRASE.
   Validate that paragraph as part of P2-003's exact projection; a manually inserted
   path or similar prose cannot counterfeit disclosure. One paragraph may witness
   several fields, but the closure is per field and cannot rely on an unrelated path.
4. At least one positive disclosure witness per contributing entity/condition:
   BRIEF_SUMMARY_OF_THE_INVENTION or DETAILED_DESCRIPTION_OF_THE_INVENTION.
   BRIEF_DESCRIPTION_OF_THE_DRAWINGS may supplement only for an actually textually
   disclosed unit, never infer from pixels; it is not a replacement for absent
   invention-model support. Background/Field/Related Art alone never qualifies.

Aggregate grounding is the more conservative class of all used supports:
SOURCE_FACT only if all are SOURCE_FACT; otherwise PARAPHRASE. Reject INFERENCE,
SAFE_GENERALIZATION, PROPOSED_VARIANT, MISSING, unaudited HUMAN_CONFIRMED,
unsupported/tainted supports. A P2-003 paragraph containing a stricter-ineligible
support aggregate is ineligible even if its prose looks plausible. Never upgrade.
If a required core unit fails, emit no claim for that family; optional candidate
failure excludes the whole candidate and yields a deterministic review issue.

## 10. Conflicts, gaps and taint

Start with every UNRESOLVED P2-002 conflict's affected_entity_ids; compute a
fixed-point taint closure through typed references (solution references, relation
endpoints, step inputs/outputs/dependencies, flow endpoints, parameter related IDs,
embodiment members, variant base IDs, effect references). Conditions are part of
their owning unit. Required-core taint blocks the entire family. Optional-unit
taint excludes that candidate, never selects a side, averages values or repairs
using P2-003 prose. Reject unaudited HUMAN_RESOLVED/HUMAN_CONFIRMED input through
the released P2-003 integrity gate; there is no new approval workflow here.

Missing records are routed by resolvable target_path into entity/family closure.
BLOCKING/HIGH gaps affecting a required unit block its family; other relevant
gaps/issues remain in review metadata. Unresolvable technical target paths create
an explicit unrouted issue and conservatively block the selected solution's
families rather than guessing irrelevance. P2-003's expected administrative/
Claims/sequence-listing gaps are not false technical blockers; known section IDs
route them as upstream context only. Do not suppress upstream questions/history.
Issues record missing IDs, affected family, entity IDs, both sets of source paths
and related author questions where available. No partial core is emitted as complete.

## 11. Structural independent claims

Select exactly the configured solution, not all alternatives. SYSTEM/APPARATUS
core = **all** its related_element_ids whose actual essentiality is ESSENTIAL,
ordered by upstream element-array index. No eligible ESSENTIAL core means
INSUFFICIENT_INDEPENDENT_CLAIM_SUPPORT. Require selected solution support and
disclosure; it anchors family coherence but is not free-form extra claim prose.

Structural element types allowed: DEVICE, MODULE, STRUCTURE, SOFTWARE_COMPONENT,
DATA_STRUCTURE, PROCESSING_BLOCK. OTHER/chemical/biological/material classification
alone cannot be reinterpreted as a structural family. If any required core element
is outside that closed list or fails any strict support gate, no family claim.
If any selected solution related_element_id has UNKNOWN essentiality, block the
family for confirmation rather than guess that omitting it preserves the core.
Render exact name plus complete supported description when present; do not
extract, omit or rewrite qualifiers inside descriptions.

Include every supported P2-002 relationship with both endpoints in this core,
using the exact controlled type. A disconnected multi-element core with no
represented connections is confirmation-required; graph connectivity ignores
direction only for this coherence check, never for rendering. Each relationship
unit must close support itself, including endpoints. This is a conservative
represented-core convention, **not** a finding of legal necessity or optimal scope.
Optional/conditional/unknown elements do not become mandatory by name order.

P2-002 has no parameter-essentiality field. Therefore no independent parameter
is classified ESSENTIAL by role or numeric presence. Deterministic predicate:
if any parameter.related_entity_ids intersects the core element/relationship IDs
or contains the selected_solution_id, gate the family for confirmation
(`PARAMETER_ESSENTIALITY_UNAVAILABLE`) rather than omit a possibly required
quantitative constraint and silently broaden. Parameters tied only to optional
dependent candidates follow Section 13. Exact parameters embedded in a copied
description retain full scope; EXAMPLE_ONLY/UNKNOWN_SCOPE references still gate
that unit. No parsing around an unsupported qualifier to salvage a claim.

## 12. Procedural and composition rules

Normative independent METHOD/PROCESS rule: only explicitly supported ESSENTIAL
steps, whole actions/conditions, actual input/output entities, original
sequence_index and dependency_step_ids; no prerequisites invented from sequence.
The released step schema cannot prove the ESSENTIAL predicate, so the v1 selector
returns HUMAN_CONFIRMATION_REQUIRED / no claims, with
`METHOD_STEP_ESSENTIALITY_UNAVAILABLE`. A synthetic action saying "required" or
config selecting a step is not a replacement for structured authority.

Composition rule: explicit composition/component membership, required/optional
status and exact amount/concentration/range, units, conditions and scope must be
available as eligible structured authority. The released reconstruction does not
define that complete relation. v1 returns HUMAN_CONFIRMATION_REQUIRED / no claims,
with `COMPOSITION_SEMANTICS_UNAVAILABLE`, even if individual material names/ranges
are supported. Do not synthesize formulation semantics from arbitrary elements.

These rules define safe refusal cases, not permission to add missing upstream
fields now. Positive generation cases for these types require a future separately
authorized contract extension; Section 22 distinguishes those conditional tests
from tests feasible against today's schemas.

## 13. Dependent limitation units

Each dependent adds exactly one source-supported limitation unit; an inseparable
upstream reference/condition group counts as one unit. All its members require
strict dual support and must further specify/add to the parent. No dependent
repeats only existing parent content, removes constraints, substitutes an optional
entity for a required one or generalizes a value. It inherits the complete core.

| Priority / unit | Conservative eligibility and grouping |
|---|---|
| 1 OPTIONAL element | In selected solution, compatible structural type; full name/description; include all represented links to core. Unrepresented necessary linkage is not invented |
| 2 CONDITIONAL element | Entire supported description must carry its explicit condition; emit that complete opaque description intact. If absent or condition cannot be supported as part of that exact unit, exclude with confirmation issue; no invented `when` clause |
| 3 Relationship | Both endpoints already in the core, or in the same indivisible delta group; exact type, no duplicate existing relationship |
| 4 Parameter | Linked only to an introduced optional unit, supported scope/value/units/conditions; no legal importance or mandatory status inferred from role |
| 5 Explicit embodiment | EXPLICIT only, strict grounding, references within the core plus same delta closure, no unsupported member; SYNTHESIZED/proposed excluded |
| 6 Variant | SOURCE_SUPPORTED, filing_content_eligible=true, human_confirmation_required=false; all base_entity_ids already in core; exact full description and qualifiers, no replacement/broadening |

For an OPTIONAL/CONDITIONAL entity candidate, include **all** parameters whose
related_entity_ids include that introduced entity in the same indivisible unit,
using upstream parameter order. If any linked constraint is ineligible by scope,
role, support or reference closure, exclude the whole entity unit; do not emit
the entity while silently dropping its disclosed quantitative qualifiers. The
category-4 parameter candidate uses that same complete entity/parameter closure;
if already emitted at priority 1/2, fingerprint deduplication removes it.

All transitive references needed to render a delta must either be in the parent
or be included together in the same supported indivisible unit. If that closure
needs an UNKNOWN/unsupported member, another claim, or an invented relationship,
exclude the whole unit. No recursive claim chains. Standalone supported method
steps are not dependent structural limitations in v1 because required procedural
authority is unavailable. Effects alone never form limitation units.

A parameter unit necessarily groups its linked optional entity and exact parameter
constraint; do not render a numeric limitation without introducing its subject.
Only SUPPORTED_RANGE and non-experimental roles OPERATING_CONDITION/THRESHOLD/
DIMENSION qualify. EXAMPLE_ONLY or UNKNOWN_SCOPE never becomes a mandatory claim
constraint in v1, even in a dependent. EXPERIMENTAL_RESULT/EXPERIMENTAL_CONDITION/
OTHER cannot become general operating requirements. Later Human/IP approval is
not auto-generated by this producer; an exception needs separately authorized
review/contract work. All source value_kind EXACT/RANGE/SET/QUALITATIVE semantics
must remain exact; no rounding, unit conversion, approximation or set selection.

Technical effects, commercial advantages and guarantees are excluded from v1
limitations entirely. A future explicit result/condition mapping needs separately
reviewed rules; source effects cannot become claim requirements automatically.
Negative limitations are never inferred from omission: an explicit negative
phrase can only be copied intact inside an otherwise eligible exact source unit
with a literal cited disclosure; no negation token is added by a template.

## 14. Anti-broadening and relationship/dependency preservation

Never broaden `5–10 μm` to `1–20 μm`, `up to 10 μm`, `at least 5 μm`, or
`approximately 5–10 μm`. Preserve numeric JSON scalar types, endpoints, set order,
units, conditions and scope. An opaque numeric string stays opaque; do not parse
it to synthesize an independent range. No conversion, rounding or inferred bounds.

Use the following closed, non-strengthening relationship map, identical in meaning
to released P2-003; `subject`/`object` are exact upstream names/actions, not synonyms:

| Type | Wording |
|---|---|
| RELATED_TO / PART_OF / CONTAINS | is related to / is part of / contains |
| CONNECTED_TO / COUPLED_TO | is connected to / is coupled to |
| COMMUNICATES_WITH / RECEIVES_FROM / OUTPUTS_TO | communicates with / receives from / outputs to |
| CONTROLS / TRANSFORMS / MEASURES / STORES / EXECUTES | controls / transforms / measures / stores / executes |
| INPUT_TO_STEP / OUTPUT_FROM_STEP / DEPENDS_ON | is an input to step / is an output from step / depends on |

CONNECTED_TO does not become COUPLED_TO/CONTROLS; RELATED_TO does not become
CONNECTED_TO; no new spatial/causal relation. A directed edge keeps its subject/
object, even if coherence validation uses an undirected view. Flow descriptions
never generate branches, feedback, parallelism, causality or unspecified flow type.
No flow-only claim unit in initial v1. sequence_index is not dependency; preserve
explicit dependency_step_ids and conditions in review data even when steps cannot
be claimed. No method-family generation shortcut around Section 12.

## 15. Deterministic ordering, IDs and duplicate elimination

Fixed family order: SYSTEM, APPARATUS, METHOD, PROCESS, COMPOSITION, filtered
by requests, not caller list order or perceived patent value. Within structural
core: entities by element-array index, then relationships by relationship-array
index. Claim order: each emitted independent, then its selected dependents, then
next family. Element global IDs allocate in final claim order, effective element
sequence; padding is at least four digits, not a 9,999-item collision limit.

Dependent candidates use Section 13 priority, upstream array index within a
category, then logical ID and escaped source-path Unicode lexical order as
tie-breaks. Preserve all member conditions and parameter value-array order.
Build candidate closure and validate before sorting/deduplication/count limiting.

Fingerprint a limitation using C([ordered upstream entity IDs, complete technical
field values, relation endpoints/types, parameter value/unit/scope, conditions]).
Exclude a fingerprint already present in the parent or emitted delta, retaining
first canonical candidate and merging its support witnesses deterministically.
No near-duplicate semantic scoring. Apply configured cap only after eligibility
and deduplication; warn `DEPENDENT_LIMIT_EXCEEDED`, keeping truncated candidate
IDs for audit. No rejected candidate consumes a claim/element number.

## 16. Canonical rendering and no new terminology

No provider or free-form drafting stage. Rendering consumes validated structured
units only. Closed boilerplate templates below are grammatical draft conventions,
including `comprising`; none represents optimal breadth or legal acceptance.

| Unit / claim | Exact template |
|---|---|
| ENTITY | exact `name`; if description exists, append `: ` + entire exact description |
| CONDITIONAL_UNIT | entire exact description (including condition); no name-only shortening |
| RELATIONSHIP | exact subject label + one space + mapped wording + one space + exact object label |
| PARAMETER EXACT | exact name + ` has value ` + canonical scalar + optional ` ` + exact unit |
| PARAMETER RANGE | exact name + ` has value from ` + canonical minimum + ` to ` + canonical maximum + optional ` ` + exact unit |
| PARAMETER SET | exact name + ` has values ` + C(values) + optional ` ` + exact unit; no subset choice |
| PARAMETER QUALITATIVE | exact name + ` has value ` + exact qualitative_value + optional ` ` + exact unit |
| EMBODIMENT / VARIANT | complete exact supported description; no summary/paraphrase generator |
| Independent SYSTEM / APPARATUS | `A system comprising: ` / `An apparatus comprising: ` + local fragment list separated by `; ` + final `.` |
| Dependent SYSTEM / APPARATUS | `The system of claim N, wherein ` / `The apparatus of claim N, wherein ` + delta fragment list separated by `; ` + final `.` |

Parameter values use C(value) for numeric/string EXACT values and numbers for
RANGE; QUALITATIVE copies the full string. JSON quoting of a scalar is serialization,
not a new technical term. Source punctuation is preserved, even if draft prose
is awkward; append final period only if final fragment lacks `.`, `!`, `?`.
No article/plural correction, abbreviation expansion, synonym generation,
translation, sentence reordering, stylistic repair or invented technical nouns.

METHOD `A method comprising: `, PROCESS `A process comprising: `, COMPOSITION
`A composition comprising: ` and their corresponding dependency wrappers are
reserved conventions, **disabled** by Section 3. Their presence in this document
does not enable a claim-generation path without a reviewed authority extension.

Allowed boilerplate is exactly the fixed template text, closed relationship-map
wording, separators, `from`, `to`, and decimal parent numbers/serialization tokens.
All other characters in rendered technical fragments must come from specific
supported upstream fields identified in audit records. This is field provenance,
not a word-frequency whitelist that can recombine source tokens into new facts.

`canonical_render(claim_struct)` uses independent local elements or dependent
non-inherited delta only; number prefix is metadata, not included in claim_text.
Validator reconstructs units from upstream fields and checks exact text equality,
not merely agreement between attacker-controlled element.text and claim_text.
Parent clones must exactly match the parent's content/support. Unknown role,
unsupported fragment, hidden suffix or reordered condition fails validation.

## 17. Review package and support audit

ReviewPackage requires `evidence`, `claim_support`, `issues`, `warnings`,
`missing_information`, `author_questions`. Only used/excluded-unit evidence is
copied as original P2-002 records; sorted by upstream evidence-array order.
Preserve P2-003 evidence references as pointers, never parse its serialized
`description` into a new authority or import unrelated evidence.

One ClaimSupport record per effective emitted claim_number + element_id:
`support_status=SUPPORTED`, source_paths, evidence_ids, specification_section_ids,
specification_support_refs, upstream_entity_ids, grounding, `conflict_status=CLEAR`,
optional parameter_scope iff relevant. Exact equality with the corresponding
element's support is required; no orphan, missing, duplicated or mismatched record.
Review-only failures use issues with support_status UNSUPPORTED or
HUMAN_CONFIRMATION_REQUIRED, not fake claim numbers/support records.

Issue requires issue_id (`ISS-P2-004-0001…`), stable code, family_id, entity_ids,
source_paths, specification_paths, evidence_ids, missing_ids, author_question_ids,
support_status and fixed safe message. Warning has warning_id (`W-P2-004-0001…`),
code, family_id, affected IDs/known paths and fixed safe message. MissingInformation
requires missing_id (`MI-P2-004-0001…`), family_id, source_paths, reason, question_ids;
AuthorQuestion requires question_id (`AQ-P2-004-0001…`), family_id, missing_id,
fixed question text, status OPEN. Original upstream IDs/records are linked/copied
in optional `upstream_record` on missing/question entries with a typed root pointer;
never claim their authors supplied new approval. No source content goes in logs.

Issue/warning order: family order, candidate category/order, fixed error-code order
(Section 21 lexical code order for simultaneous codes), then source path; allocate
IDs only after this order is fixed. Deduplicate exact code/family/path tuples.
This ensures stable failures and preserves historical conflicts/questions.
Each requested family also gets one informational HUMAN_IP_REVIEW_REQUIRED
warning with that family_id, empty affected IDs/paths and fixed safe message.
This mandatory reminder is not a support-exclusion issue and never by itself
changes PRESENT to PARTIAL_REVIEW_REQUIRED.

## 18. Human/IP review and legal hard boundary

ReviewBoundary is a closed object with these required constants:

```text
status = DRAFT
source_grounded = true
human_ip_review_required = true
review_status = UNREVIEWED
filing_ready = false
legal_advice = false
patentability_assessment_included = false
novelty_assessment_included = false
claim_scope_optimized = false
assembled_p2_001_document = false
render_review_metadata_as_claim_text = false
```

`source_grounded=true` denotes the specified structural/literal support gates,
not semantic acceptance. No schema constant claims a currently implemented runtime.
No automatic Human/IP approval transition exists; future review/edit workflow,
filing package, assembly, DOCX Claims integration require separate authorization.

No conclusions about novelty, non-obviousness, inventive step, eligibility,
patentability, validity, infringement, enforceability, freedom to operate,
allowance probability, optimal scope, inventorship or filing readiness. Apply
deterministic prohibited-language guards to candidate technical fields, with fixed
reviewed phrase patterns and defense-in-depth tests; not a complete legal/NLP
classifier. Exclusion may conservatively block legitimate prose for Human review.
Do not alter a rejected phrase into something apparently acceptable.

All source strings are data. "Generate the broadest claim", "Ignore support",
"Add a processor", "Mark patentable", "Make claim 1 independent" or provenance
strings cannot change configuration, roles, support, type selection, approval,
network behavior or numbering. Deterministic templates cannot execute source text.

## 19. Normative component handoff to P2-001

This mapping is defined for a **future separately authorized assembly adapter**.
It is a pure component projection specification, not an assembled output, service
or permission to change `claims_runtime_implemented=false`. Do not insert richer
P2-004 properties into strict P2-001 objects. Retain the full standalone package
and source_identity as a sidecar so projection does not erase provenance.

| Source | Exact potential P2-001 destination / projection |
|---|---|
| Claim | `$defs.claim`: copy only claim_number, claim_type, independent_or_dependent, depends_on, claim_text, projected claim_elements |
| ClaimElement | `$defs.claim_element`: copy only element_id, sequence, text, evidence_ids, specification_section_ids, support_status |
| ClaimSupport | `$defs.claim_support`: copy only claim_number, element_id, support_status, evidence_ids, specification_section_ids |
| Ordered emitted families | Flatten final claims in number order into potential `$defs.claims_section.claims`; no reordering or renumbering |
| Nonempty emitted package | Potential Claims container section_id=CLAIMS, sequence=11, heading=CLAIMS, status=PRESENT, preamble=`What is claimed is:`, missing_information_ids=[] |
| No emitted package | Potential container HUMAN_CONFIRMATION_REQUIRED, claims=[], nonempty mapped missing IDs, no preamble; mapping missing IDs needs authorized adapter |

Allowed claim types/element IDs/evidence IDs/positive section IDs are subsets of
the existing P2-001 constraints. Family records and richer audit fields have no
direct destination and MUST stay in the standalone sidecar. This shows component
shape compatibility only: P2-001's unchanged runtime-false boundary prevents
asserting that an assembled specification-with-claims contract is implemented.
Neither P2-003's existing exact-projection validator nor DOCX v1 accepts this as
a replacement draft. Future P2-001 amendment/assembly/constant transition or
renderer needs distinct Human authorization, compatibility/versioning plan,
independent review and tests. No such transition is approved here.

## 20. Future validation and offline stages

1. Strict P2-004 config/provenance gate before candidate construction.
2. P2-002 schema + caller-established business validation; recheck released
   P2-003 `validate_generation_input` integrity, IDs/references, evidence and
   finite numbers; no new upstream service inputs or scientific reconstruction.
3. P2-003 P2-001-schema validation, exact expected no-Claims handoff shape,
   `validate_generated_specification(draft, reconstruction, sidecar_config)`;
   use its existing config gate, including optional actual title selection.
4. Cross-input identity/content hashing; validate selected solution and indexes.
5. Conflict/gap taint, strict grounding/literal and specification-support closure.
6. Fixed requested-type capability gate, complete independent-core eligibility.
7. Dependent-unit construction, support, scope, grouping, dedupe/cap ordering.
8. Allocate family/claim/element IDs; canonical text and complete effective audit.
9. Review issues/status calculation and immutable boundaries.
10. Future standalone JSON Schema plus business validation, exact upstream
    reprojection comparison, repeat determinism and mutation-isolation checks.

Business checks include positive/contiguous unique numbering, complete inherited
support, same-family single parent, depth=1 graph, exact rendered text/fields,
no range broadening, scope/condition/relationship preservation, evidence references,
exact dual support, all Human-review constants and absence of legal conclusions.
Shape validation alone cannot prove logical IDs or evidence closure. Exact
reprojection alone is not independent semantic QA; fixtures also assert literal
expected fragments/exclusions and deliberate output tampering independently.

No network, provider, retrieval, model repair, embeddings, storage service,
external NLP or environment-dependent stage. Future service/validator may use
existing dependencies only if separately authorized; no dependency added here.
Neither generation nor validation mutates reconstruction, specification, config,
cached definitions or another returned output. Invalid input returns no package;
valid input with no eligible family returns an explicit review-required package.

## 21. Stable failure and warning codes

Fatal errors have fixed safe messages and generated known contract paths only;
never interpolate source text, unknown keys or secrets into logs/errors. Multiple
validation failures use phase order above, then lexical code/path order. Candidate
exclusions/blocks are deterministic issues, not successful unsupported claims.

| Code | Disposition |
|---|---|
| SOURCE_DOCUMENT_PROVENANCE_REQUIRED | Fatal missing provenance |
| REAL_SOURCE_NOT_AUTHORIZED | Fatal false provenance |
| INVALID_GENERATION_CONFIG | Fatal wrong type/value/key/selection/sidecar shape |
| INVALID_RECONSTRUCTION / INVALID_SPECIFICATION | Fatal upstream schema/business failure |
| UPSTREAM_DOCUMENT_IDENTITY_MISMATCH | Fatal identity/SHA/synthetic mismatch |
| REQUESTED_CLAIM_TYPE_UNSUPPORTED | Fatal prohibited enum |
| INSUFFICIENT_INDEPENDENT_CLAIM_SUPPORT | Family confirmation; no partial core |
| METHOD_STEP_ESSENTIALITY_UNAVAILABLE / COMPOSITION_SEMANTICS_UNAVAILABLE / PARAMETER_ESSENTIALITY_UNAVAILABLE | Family confirmation under released-model capability limits |
| CLAIM_ELEMENT_UNSUPPORTED / CLAIM_ELEMENT_GROUNDING_INELIGIBLE | Core block or dependent exclusion |
| UNRESOLVED_RECONSTRUCTION_CONFLICT / CLAIM_ELEMENT_CONFLICT_TAINTED | Core block or dependent exclusion, no side chosen |
| CLAIM_PARAMETER_BROADENING / CLAIM_RELATIONSHIP_STRENGTHENING | Exclude candidate; fatal if present in purported output |
| CLAIM_EVIDENCE_NOT_FOUND / CLAIM_SPECIFICATION_SUPPORT_NOT_FOUND | Core block or dependent exclusion |
| CLAIM_DEPENDENCY_INVALID / CANONICAL_CLAIM_TEXT_MISMATCH / CLAIM_SUPPORT_INCOMPLETE | Fatal output validation |
| DUPLICATE_LIMITATION / DEPENDENT_LIMIT_EXCEEDED | Deterministic audit warning; do not consume numbering |
| CLAIM_EXAMPLE_SCOPE_INELIGIBLE / CLAIM_UNKNOWN_SCOPE_INELIGIBLE / CLAIM_NEGATIVE_LIMITATION_UNSUPPORTED | Exclude unsupported unit |
| UNROUTED_UPSTREAM_GAP / REQUIRED_UPSTREAM_INFORMATION_MISSING | Family confirmation plus linked question |
| PROHIBITED_CLAIM_CONTENT | Core block/dependent exclusion; fatal output if bypassed |
| HUMAN_IP_REVIEW_REQUIRED | Always-present review-boundary notice; not an approval or generation failure |

## 22. Synthetic/adversarial future fixture plan

No fixtures/tests are created or run by this task. Future fixtures must be
synthetic, privacy-safe, upstream-schema-valid and paired with independently
asserted expected outcomes; mutation fixtures may intentionally fail validation.
The following are **test requirements, not PASS evidence**.

| Case | Fixture / required assertion |
|---|---|
| 01 | Supported SYSTEM essential connected core; exact fragments and dual-support audit |
| 02 | METHOD request with supported actions: current schema lacks step essentiality, so confirmation/no claims; positive essential-method generation reserved for separately authorized upstream authority extension |
| 03 | SYSTEM + METHOD request: structural family emitted, method blocked, PARTIAL_REVIEW_REQUIRED, numbering no gaps |
| 04 | APPARATUS supported structural core; exact independent wrapper |
| 05 | PROCESS supported steps: current essentiality gate refusal; future positive extension case remains unauthorized |
| 06 | Composition-looking materials/amounts with support: current membership/essentiality gap refusal; positive structured-composition fixture needs a separately authorized extension, not a fabricated released-schema field |
| 07 | Requested structural family lacks eligible connected core; confirmation, empty family |
| 08 | OPTIONAL supported element forms one dependent unit; parent stays unchanged |
| 09 | CONDITIONAL complete supported description preserved; absent/unsupported condition excludes unit |
| 10 | UNKNOWN essentiality in required core cannot be promoted; issue/no partial independent |
| 11 | INFERENCE blocked, including referenced labels/conditions |
| 12 | SAFE_GENERALIZATION blocked despite P2-003's broader prose eligibility |
| 13 | PROPOSED_VARIANT / unaudited HUMAN_CONFIRMED blocked |
| 14 | Unresolved core conflict blocks family; optional taint excludes whole delta |
| 15 | Numeric-range endpoints broadened/tampered; rejected, no rounding/conversion |
| 16 | EXAMPLE_ONLY remains review-only, never mandatory general claim constraint |
| 17 | UNKNOWN_SCOPE never becomes mandatory independent/dependent constraint |
| 18 | RELATED_TO changed to CONNECTED_TO/CONTROLS rejected |
| 19 | Sequence index alone cannot introduce step dependency or essentiality |
| 20 | UNSPECIFIED flow cannot become material/causal/feedback limitation |
| 21 | Missing/dangling evidence ID blocks unit; orphan audit record rejected |
| 22 | Missing/wrong paragraph/path specification support blocks unit |
| 23 | Field/background/related-art-only support rejected as sole invention disclosure |
| 24 | Document_id/file_name/media_type/checksum or checksum-presence mismatch fatal |
| 25 | Dependent wrong/cross-family/forward/self parent rejected |
| 26 | Multiple-dependent parent list rejected |
| 27 | Depth >1/cycle/claim chain rejected |
| 28 | Duplicate local or already-inherited limitation excluded before cap; stable IDs |
| 29 | Absence of X cannot add excludes-X; explicit negative unit needs literal source disclosure |
| 30 | Unsupported technical synonym or source-token recombination rejected |
| 31 | Effect/benefit alone does not become limitation; no guarantees |
| 32 | Source command-like strings cannot alter selection/templates/numbering; excluded safely where prohibited |
| 33 | Source says synthetic but caller provenance missing: required-provenance error |
| 34 | Source says real while caller true: source text is data; no provenance control change or real-data authorization |
| 35 | False provenance fatal before candidate construction |
| 36 | String/number/null/container provenance or bool-as-integer cap rejected |
| 37 | Repeated identical input/config produces identical full package and IDs |
| 38 | Input/config/output mutation isolation, repeated result not aliased |
| 39 | Claim and global element numbering stable across blocked candidates/families |
| 40 | Requested-list permutation yields canonical fixed family/config order |
| 41 | Hidden suffix/element.text tampering fails upstream-based canonical-render equality |
| 42 | Every claim/family UNREVIEWED; Human/IP hard boundary immutable |
| 43 | Legal/patentability/conclusion language in candidate/output refused |
| 44 | P2-001 schema bytes unchanged; projected component keys exact subset, no assembled runtime-true object |
| 45 | P2-003 schema/service/contract bytes unchanged; expected empty Claims input accepted |
| 46 | No provider/network/retrieval path; no environment/runtime integration |
| 47 | All fixtures synthetic; no real/confidential excerpt or paper committed |
| 48 | No filing-ready/attorney-approved/Human-approved state |
| 49 | Actual P2-003 config sidecar validates selected title; absent/wrong sidecar rejected |
| 50 | Same document/draft ID but changed content changes Claims ID; canonical hash material unambiguous |
| 51 | Inherited effective elements all have fresh IDs and complete matching audit |
| 52 | Required parameter with no essentiality blocks family; no silent numeric omission |
| 53 | Selected solution cannot silently mix disjoint alternatives; absent selection rejected |
| 54 | Conservative P2-003 paragraph grounding aggregate cannot be bypassed by prose similarity |

## 23. Acceptance criteria matrix

**Historical pre-review state at original authorship — preserved:**

These criteria describe specification requirements and future implementation
oracles. Codex self-checks are not independent approval; **AC-45 is PENDING**.

**Current specification review:** AC-01…AC-48 PASS; 54-case future synthetic
fixture plan ADEQUATE. This records specification review, not implementation
or execution of future tests.

| AC | Required rule / verification reference |
|---|---|
| AC-01 | Specification-only authorized scope and draft/non-legal boundary; Sections 1–2 |
| AC-02 | Validated P2-002 canonical technical/evidence input only; Sections 2, 20 |
| AC-03 | Validated immutable P2-003 canonical specification input, expected empty Claims; Sections 2, 20 |
| AC-04 | Strict standalone SUPPORTED_DRAFT_CLAIMS v1.0.0 documented, no production schema yet; Sections 4–8 |
| AC-05 | P2-001 schema/runtime-false constant immutable; Sections 2, 19; case 44 |
| AC-06 | P2-003 contract/runtime unchanged; Sections 2, 19; case 45 |
| AC-07 | Exact cross-input document/checksum presence/value identity; Section 5; case 24 |
| AC-08 | Required strict true-only caller provenance, no inference/coercion; Section 6; cases 33–36 |
| AC-09 | Explicit unique requested-type controls, no silent claim-strategy optimization; Section 6 |
| AC-10 | Deterministic type capability/refusal predicates; Sections 3, 11–12; cases 01–07 |
| AC-11 | Complete supported independent core, no partial apparent completeness; Section 11 |
| AC-12 | Exactly one supported delta/indivisible group per dependent; Section 13 |
| AC-13 | ESSENTIAL only in independent structural core; missing step/parameter essentiality cannot be invented; Sections 3, 11–12 |
| AC-14 | OPTIONAL/CONDITIONAL preserved, complete supported conditions retained; Sections 11, 13; cases 08–10 |
| AC-15 | SOURCE_FACT/PARAPHRASE only, all referenced supports and paragraph aggregate checked; Section 9 |
| AC-16 | P2-002 entity/path/evidence and exact-literal integrity closure; Section 9; case 21 |
| AC-17 | P2-003 positive paragraph-level disclosure witnesses, not section-name presence; Section 9; case 22 |
| AC-18 | Field/background/related-art cannot be sole positive invention support; Section 9; case 23 |
| AC-19 | Fixed-point conflict taint, no side chosen; Section 10; case 14 |
| AC-20 | Required/unrouted technical gaps block with traceable questions; Section 10 |
| AC-21 | No numeric broadening/conversion/rounding; Section 14; case 15 |
| AC-22 | EXAMPLE_ONLY/UNKNOWN_SCOPE cannot become universal claim constraints; Section 13; cases 16–17 |
| AC-23 | Exact relationship enum/endpoints/non-strengthening map; Section 14; case 18 |
| AC-24 | Explicit step dependencies, not sequence, and no new flow semantics; Sections 12, 14; cases 19–20 |
| AC-25 | Composition membership gate under released-model limitations; Sections 3, 12; case 06 |
| AC-26 | Effects not automatically claimed, no guaranteed benefits; Section 13; case 31 |
| AC-27 | Only strict SOURCE_SUPPORTED eligible variants, no inferred/proposed variants; Section 13 |
| AC-28 | No negative limitation inferred from omission; Section 13; case 29 |
| AC-29 | Exact source technical fields and closed boilerplate, no synonyms; Section 16; case 30 |
| AC-30 | Fixed family/limitation category and tie-break ordering; Section 15; case 40 |
| AC-31 | Positive unique contiguous claims/elements and stable IDs; Sections 5, 8, 15; case 39 |
| AC-32 | Same-family single independent parent, depth 1, no multiple dependencies; Section 8; cases 25–27 |
| AC-33 | Upstream-reconstructed canonical text equality, no hidden prose; Section 16; case 41 |
| AC-34 | Complete first-class effective-element support audit, no orphan records; Section 17; case 51 |
| AC-35 | Required Human/IP review and UNREVIEWED constants; Section 18; case 42 |
| AC-36 | No filing-ready/automatic approval state; Section 18; case 48 |
| AC-37 | Legal/patentability/novelty/claim-value conclusions excluded; Sections 1, 18; case 43 |
| AC-38 | Untrusted source cannot alter any control/gate; Section 18; cases 32–34 |
| AC-39 | Full package determinism and content-bound identity; Sections 5, 15, 20; cases 37, 50 |
| AC-40 | Input/config/cache/output mutation isolation; Section 20; case 38 |
| AC-41 | Offline/provider-free design, no network/runtime integration; Section 20; case 46 |
| AC-42 | Real/confidential data not authorized; provenance assertion not permission; Sections 6, 24; case 47 |
| AC-43 | Explicit component-only P2-001 projection, no assembled schema contradiction; Section 19 |
| AC-44 | At least 48 adversarial synthetic cases with exact expected outcomes, positive/refusal limitations distinguished; Section 22 |
| AC-45 | **PASS** — independent fixed-SHA Gemini 3.1 Pro High / Antigravity read-only specification review **PASS / findings NONE** on `89eef2af3fcc4105b66acf02f9504b2887c222ac`; Human-supplied external review evidence, not self-approval |
| AC-46 | Actual P2-003 generation-config sidecar for reusable exact business validation; Sections 6, 20; case 49 |
| AC-47 | Explicit selected solution and no combination of unrelated solutions; Sections 6, 11; case 53 |
| AC-48 | Released-model feasibility limits are explicit and do not authorize upstream amendment; Sections 3, 12; cases 02, 05, 06, 52 |

## 24. Governance gates, boundaries and fixed-SHA handoff

### Current implementation gate — 06/10/2026

Specification 0.1.0 remains **APPROVED / MERGED**. Independent specification
review was **Gemini 3.1 Pro High / Antigravity read-only**, **PASS / findings NONE**
on reviewed SHA `89eef2af3fcc4105b66acf02f9504b2887c222ac`; AC-01…AC-48 **PASS** and the
54-case future synthetic fixture plan was **ADEQUATE**. [PR #80](https://github.com/nshaokiet/ai-ip-description-generator/pull/80)
merged at `9ac1889e44bca080e21efb5bbbd2ebf5c3140293`; post-merge main CI
[`37262324108`](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/37262324108)
was **SUCCESS**. ADR-014 remains the **ACCEPTED P2-004 specification architecture baseline**.

Implementation is authorized by `HUMAN-P2-004-IMPLEMENTATION-2026-10-06` from
baseline `b1085337c8f16c4bb72574bfb45e27741290ca90` on branch
`feat/p2-004-supported-draft-claims`. [PR #82](https://github.com/nshaokiet/ai-ip-description-generator/pull/82)
is **OPEN / UNMERGED**. Executable implementation SHA before this governance
handoff is `411b17a6ed39885b47af9932c9cf44d4b498db9e`; exact-head CI
[`37423007016`](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/37423007016)
is **SUCCESS**. Local verification: P2-004 oracle **54/54 passed**; targeted
P2-002/P2-003 regression **237/237 passed**; full Python **738 passed / 3 skipped**;
frontend lint/typecheck/build **PASS**; local Playwright **26/26 cases completed**
with a Windows teardown hang caveat; static Render export **PASS**; demo E2E
**5/5 passed**.

The executable implementation touched six files before this governance handoff:
`backend/app/services/supported_draft_claims_generation.py`,
`backend/app/services/supported_draft_claims_validation.py`,
`schemas/supported-draft-claims/v1.0.0/supported-draft-claims.schema.json`,
`tests/backend/test_supported_draft_claims_v1.py`,
`tests/fixtures/supported-draft-claims/README.md`, and
`tests/fixtures/supported-draft-claims/v1.0.0/base-synthetic.json`. This handoff
adds only README, PROJECT_CONTEXT, this task record and Project Control Center.
Git comparison to the authorized baseline confirms **10 distinct changed files**.

Independent implementation review is **PENDING**. No implementation PASS or
merge eligibility is claimed. P2-001/P2-002/P2-003 semantics remain unchanged:
P2-003 Claims stays `status = MISSING`, `claims = []`, has no Claims preamble,
`review_package.claim_support = []`, and
`review_boundary.claims_runtime_implemented = false`. The standalone P2-004
generator/validator is not integrated into the product Claims runtime.

Provider/API calls **NONE**; real/confidential data **NONE / NOT AUTHORIZED**;
frontend/DOCX/deployment implementation changes **NONE**; BLK-003 **OPEN**;
EVAL-001 PRODUCT_RUNTIME **DEFERRED — AWAITING FUNDING**; semantic acceptance
**NOT DETERMINED**; production **NOT APPROVED / NOT PERFORMED**. MCP remains
**BLOCKED BY TOOL CAPABILITY — Unknown task: P2-004**; no task state, owner,
lease or checkpoint is fabricated.

Required stop: **READY FOR INDEPENDENT FIXED-SHA REVIEW**. Freeze the final SHA,
obtain Gemini 3.1 Pro High / Antigravity read-only fixed-SHA implementation review,
and **DO NOT MERGE or start downstream work** in this phase.

### Historical pre-review authorization and handoff — preserved

The following passage records the original 05/10/2026 specification-only
authorization and pre-review/pre-merge gates. Pending/DO NOT MERGE wording is
historical and superseded by the current specification evidence above.

Authorization permits exactly two new docs (this task and ADR-014) plus bounded
README/PROJECT_CONTEXT/Control Center registration: maximum five documentation
files. Review Log is read-only; no fabricated review result. Register P2-004 as
SPECIFICATION — INDEPENDENT REVIEW PENDING, implementation NOT AUTHORIZED;
preserve P2-003 CLOSED / COMPLETED — MERGED. Prior P2-003 "P2-004 not authorized"
statements describe its earlier gate; newer Human authorization grants **only
this specification task**, not runtime implementation or downstream work.

Commit/push, open PR against main, require exact-head PR CI SUCCESS, then STOP
edits and hand off that fixed SHA to Gemini 3.1 Pro High / Antigravity read-only.
Reviewer MUST challenge standalone/P2-001-runtime-false compatibility, dual-support
closure, released-model refusal limits, essentiality/optionality, conflict/range
gates, caller selection, config sidecar, canonical rendering, Human/IP boundary,
legal exclusions, deterministic feasibility and all 48 ACs. No PASS is supplied
yet. **DO NOT MERGE in this task. DO NOT IMPLEMENT P2-004.**

Even later specification PASS + authorized merge + successful post-merge main CI
does not itself authorize implementation: a separate explicit Human implementation
authorization is still required. No downstream-task authorization follows.

MCP observed: **BLOCKED BY TOOL CAPABILITY — Unknown task: P2-004**. No task,
approval, owner, lease or checkpoint transition is invented. Git docs/PR/handoff
are the evidence surface. Own future PR/CI identifiers belong in PR/final handoff,
not speculative metadata or recursively self-referential commits.

BLK-003 **OPEN**; EVAL-001 PRODUCT_RUNTIME **DEFERRED — AWAITING FUNDING**;
semantic acceptance **NOT DETERMINED**; provider authorization **NOT GRANTED**,
budget **0**, provider/API calls **NONE**; real/confidential data **NOT AUTHORIZED**;
arbitrary real-paper conversion **NOT ENABLED**; Claims runtime **NOT IMPLEMENTED**;
frontend/DOCX/deployment **NO CHANGE**; production **NOT APPROVED / NOT PERFORMED**.

STOP if work requires changing released schemas/P2-003, implementing code,
providers, real data, prior-art retrieval, legal decisions, frontend/DOCX,
deployment/production or a claim-strategy decision that cannot safely remain
explicit caller selection/confirmation metadata. Do not remediate outside scope.

## 25. Version history

| Previous | New | Date | Author | Change / reason | Reference | Breaking |
|---|---|---|---|---|---|---|
| None | Specification 0.1.0; proposed standalone contract 1.0.0 | 05/10/2026 | Codex | Define standalone supported draft Claims, strict dual support, fail-closed released-model capability gates, deterministic generation/audit and future tests; independent review pending | HUMAN-P2-004-CLAIMS-SPECIFICATION-2026-10-05; baseline `60b0fdb4ed68cd8c701576cf49a8b620052bb14b`; ADR-014 | No — existing contracts unchanged; new standalone contract not implemented |
| Specification 0.1.0; standalone contract 1.0.0 proposed | Specification 0.1.0 unchanged; standalone contract 1.0.0 implemented on review branch | 06/10/2026 | Codex | Implement production JSON Schema, deterministic offline generator/validator, strict dual-support/business gates, canonical rendering and reviewed 54-case synthetic/adversarial suite; implementation review pending | `HUMAN-P2-004-IMPLEMENTATION-2026-10-06`; baseline `b1085337c8f16c4bb72574bfb45e27741290ca90`; executable `411b17a6ed39885b47af9932c9cf44d4b498db9e`; PR #82; CI `37423007016` SUCCESS | No — standalone additive contract; P2-001/P2-002/P2-003 semantics unchanged |
