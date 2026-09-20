# ADR-008 — Patent Draft Generation Contract v1.0.0

## Metadata

| Field | Value |
|---|---|
| ADR ID | ADR-008 |
| Status | Accepted — Gemini Review Passed — Awaiting Human Merge Approval |
| Date | 19/09/2026 |
| Decision owner | Human / Product Owner |
| Implementation owner | ChatGPT/Codex |
| Reviewer | Gemini 3.1 Pro High |
| Related task | AI-003 |

## Context

Invention Output Schema v1.0.0 is a strict structured-analysis contract. It contains technical facts, relationships, missing information, author questions, drawing requirements, and evidence, but it does not select a final title or define ordered patent-description prose.

DOC-001 requires a stable rendering input. Rendering the structured analysis directly would put title selection, prose generation, missing-data decisions, and evidence mapping inside a DOCX template. That would make presentation logic responsible for technical drafting and weaken traceability.

Claims remain outside the approved scope. Human approved an intermediate, claim-free draft contract before DOCX implementation.

## Decision

Introduce Patent Draft Generation Contract v1.0.0 as the boundary:

```text
Validated Invention Output Schema v1.0.0
→ Patent Draft Generation Contract v1.0.0
→ Patent DOCX Template v1.0.0
→ DOCX output
```

The canonical schema is `schemas/patent-draft/v1.0.0/patent-draft.schema.json`, uses JSON Schema Draft 2020-12, and has ID `urn:ai-ip-description-generator:patent-draft:1.0.0`.

The contract:

- produces English technical drafting;
- uses the exact eleven-part document order approved for DOC-001;
- represents six technical sections and seven ordered subsections;
- allows only `PRESENT` and `MISSING` section status;
- uses `[AUTHOR CONFIRMATION REQUIRED]` when required content is unavailable;
- requires paragraph-level source paths and evidence IDs;
- keeps conflicts unresolved and preserves both sides;
- includes only used evidence in its appendix;
- excludes claims, legal advice, patentability conclusions, filing-ready assertions, and Human approval/audit state.

The caller/Human selects an existing title candidate. The model may not invent or independently choose a title. Missing or invalid selection produces a missing-title state.

No separate schema is introduced for the prompt input envelope in v1.0.0. The envelope is documented in the prompt and tested offline; its `source_analysis` is validated with the canonical input schema.

## Validation decision

JSON Schema validates shape, required fields, types, enums, constants, strict objects, fixed section order, local array constraints, and status conditionals.

A downstream Python business validator checks:

- global logical-ID uniqueness;
- source and draft cross-references;
- relative JSON Pointer resolution;
- title selection and metadata equality;
- paragraph ordering;
- Abstract word count after NFKC normalization;
- evidence closure, exact evidence copy, and reverse usage;
- conflict and missing-information rules;
- minimal prohibited legal/patentability assertion patterns.

`uniqueItems` does not guarantee uniqueness of logical IDs inside objects. Semantic evidence entailment and legal classification cannot be proven completely by these validators; independent and Human review remain mandatory.

## Alternatives considered

### Render Output Schema directly into DOCX

Rejected because Output Schema has no selected title or patent-description prose contract. It would move drafting decisions into the template and couple content generation to presentation.

### Add draft fields to Invention Output Schema v1.0.0

Rejected because it would change a released contract, mix extraction with drafting, and violate the approved AI-001 boundary.

### Use unstructured Markdown or free-form prose

Rejected because it weakens machine validation, evidence traceability, missing-data handling, and deterministic DOCX mapping.

### Add a provider-specific generation schema now

Rejected because live model integration and provider compatibility are outside AI-003. They require a separately approved runtime task.

## Consequences

### Positive

- Extraction, drafting, and presentation are independently versioned.
- DOCX rendering receives a stable, validated input.
- Every technical paragraph has explicit source and evidence links.
- Missing and conflicting inputs remain visible instead of being silently completed.
- Claims and legal conclusions are excluded mechanically and procedurally.
- Offline fixtures and tests can review the contract without external services.

### Trade-offs

- Adds another schema and validation stage.
- Requires business validation beyond JSON Schema.
- Array-based JSON Pointers are bound to a particular validated source payload instance.
- Offline oracle fixtures do not prove model behavior.
- The minimal prohibited-phrase scanner is defense in depth, not a complete semantic classifier.

## Compatibility and evolution

- Patch: documentation or non-contract correction that does not alter accepted payloads.
- Minor: backward-compatible optional capability.
- Major: changed required fields, enums, semantics, order, or claims boundary.

Released `1.0.0` must not be overwritten with breaking semantics. A future claims contract, Human approval state, provider adapter, or different section structure requires a separate Human decision and compatible versioning/migration plan.

## Security and privacy

All source strings are untrusted data. The prompt ignores embedded instructions, does not browse or call tools, and uses only synthetic fixtures in AI-003. No real paper, PII, secret, provider request, or generated confidential document is stored.

## Follow-up

1. Gemini independent read-only review completed with verdict `PASS`, no findings, and no required changes on 20/09/2026.
2. Human decides whether to approve and merge AI-003.
3. DOC-001 may begin only after AI-003 is Human-approved and merged.
