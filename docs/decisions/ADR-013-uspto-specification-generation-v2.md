# ADR-013 — Deterministic USPTO Specification Generation v2

| Field | Value |
|---|---|
| ADR ID / version | ADR-013 / 0.1.0 |
| Status | Implements approved specification 0.1.1; independent implementation review pending |
| Date / owner | 04/10/2026 / Human — Product Owner |
| Author / implementation owner | Codex |
| Independent reviewer | Gemini 3.1 Pro High / Antigravity, read-only; implementation decision pending |
| Authorization | HUMAN-P2-003-IMPLEMENTATION-2026-10-04 |
| Specification amendment | HUMAN-P2-003-SPECIFICATION-AMENDMENT-0.1.1-2026-10-04 |
| Baseline | `26d21feff592ff73574071887148630d44018b41` |

## Context and approved decision

This ADR implements the already reviewed/merged P2-003 specification 0.1.1;
it does not introduce a competing schema or new architecture approval.
The amendment reviewed at `1a17c87a6c42087965b7ac3fa88ae0fc17f26a4e` received
Human-supplied external Gemini 3.1 Pro High / Antigravity PASS/NONE, AC-01–41
and A–H PASS. PR #76 merged at the baseline above and main CI `37184343482`
succeeded. That specification verdict is not an implementation verdict.

The boundary is: validated P2-002 INVENTION_RECONSTRUCTION v1.0.0 → P2-003
offline templates → existing P2-001 USPTO_SPECIFICATION_DRAFT v2.0.0.
Only reconstruction and narrow caller configuration are service inputs. No
APP-002/AI-001 payload, raw file, HTTP route, provider, prompt, or runtime wiring
is introduced. Released upstream services and schemas remain immutable.

## Explicit caller provenance

`source_document_synthetic` is a required exact Python boolean with no default,
inference, fallback, or coercion. Copy the supplied value to target provenance.
Missing raises SOURCE_DOCUMENT_PROVENANCE_REQUIRED; false raises
REAL_SOURCE_NOT_AUTHORIZED before any template construction; wrong types fail
configuration validation. True is a caller assertion, not cryptographic proof
or real-data permission. Source strings never control provenance. Other narrow
controls have reviewed fixed constants; unsupported keys/values are rejected.
Draft identity remains SHA-256(document ID + `|` + file name + `|` + optional
source SHA); provenance does not participate in draft ID.

## Deterministic templates and integrity boundary

The generator uses explicit category templates and a complete controlled
relationship wording map. No natural-language ranking, semantic rewrite, synonym
expansion, randomness, UUID, timestamps, embedding, external NLP, or provider
stage exists. Exact title selection, input/category order, controlled flow,
essentiality, conditions, dependency, role, parameter value/scope, embodiment and
effect-basis semantics are preserved. Opaque scalar strings are not parsed into
ranges. Literal range pairs must occur together in individual cited excerpts;
unrelated numbers or pairs assembled across excerpts cannot justify bounds.

The caller must have validated upstream reconstruction integrity against its
original evidence/analysis. The service rechecks canonical shape, identity pairs,
unique IDs, internal references, evidence closure, dependency cycles, finite
numbers, literal generalization/range guards, and unaudited Human states, without
requesting upstream inputs. These checks do not independently verify the original
projection, scientific truth, or general semantic entailment. SAFE_GENERALIZATION
is accepted only as an upstream-validated supplied assertion; P2-003 creates none.

Output validation checks the released target schema and reconstruction-rooted
JSON pointers/evidence, then compares with the exact deterministic template
projection. This rejects tampered titles, relationships, ranges, provenance,
Claims, Abstract counts, gates, and review metadata. Independent semantic tests
also assert literal expected results; reprojection alone is not independent QA.
Errors expose fixed codes/messages and generated contract paths, never payload
text or arbitrary unknown configuration keys.

## Eligibility and conflict taint

Only SOURCE_FACT/PARAPHRASE/INFERENCE/validated SAFE_GENERALIZATION may enter
filing prose. Aggregate the most conservative used support class, including
referenced entities and explicitly rendered conditions. Proposed variants,
proposed embodiments, missing support, and unaudited Human states are not promoted.
Unresolved affected-entity taint propagates through references until stable;
unaffected eligible content alone is drafted, with Human-confirmation state when
a required solution/detail cannot remain. No conflict side is selected.
Conditional elements retain their complete supported description; without one
they are review-only rather than receiving an invented condition.

Gaps/questions preserve original review data and deterministic target routing.
Unknown routes remain explicit review warnings, not guessed filing targets.
Only used evidence or evidence explaining exclusions/warnings is copied; original
IDs and reconstruction paths remain available for a separately authorized P2-004.
Review data, original evidence excerpts, analysis paths, and audit labels do not
become filing prose. Output uses fresh nested state; cached schema constants are
copied, not shared with returned output.

## Target structure and strict boundaries

Follow USPTO-style specification content order, not issued-patent front pages.
No INID labels, official numbers, administrative inventions, reference-numeral
fabrication, Claims, legal/patentability conclusions, or filing-ready state.
Conservative phrase/number guards are defense in depth, not complete NLP/legal
classification. Administrative sections and Sequence Listing require Human
confirmation. Zero NOT_APPLICABLE or unaudited Human approval states are emitted.
P2-001 Background unconditionally requires its two subsections: it is a structural
PRESENT container; each child independently states MISSING when content is absent.

Drawings require an existing eligible source artifact and sufficiently descriptive
text copied exactly from its source reference, present in cited evidence. Opaque
IDs never become captions. Unsupported artifacts remain confirmation-required.
FIG. n is internal labeling; reference_numerals stays empty. No OCR/vision/pixels.
Claims are always MISSING/empty, no preamble, claim_support empty, and the review
boundary states claims_runtime_implemented=false. P2-004 is NOT AUTHORIZED.
Abstract uses whole sentences in fixed source priority, exact P2-001 word counting,
and at most 150 words; insufficient supported text gives an explicit missing gate.

BLK-003 OPEN; PRODUCT_RUNTIME DEFERRED — AWAITING FUNDING; semantic acceptance
NOT DETERMINED; provider NOT GRANTED / budget 0 / calls NONE; real/confidential
data NOT AUTHORIZED; arbitrary real-paper conversion NOT ENABLED; Claims NOT
IMPLEMENTED; no frontend/DOCX v2/deployment/production changes. All outputs remain
Human/IP-specialist review drafts, not legal advice or filing-ready applications.

## Version history

| Previous | New | Date | Author | Change / reason | Reference | Breaking |
|---|---|---|---|---|---|---|
| None | 0.1.0 | 04/10/2026 | Codex | Document approved deterministic drafting/provenance architecture and bounded integrity validation | P2-003 specification 0.1.1; implementation authorization | No — released contracts unchanged |
