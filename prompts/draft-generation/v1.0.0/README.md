# Draft Generation Prompt v1.0.0

Canonical prompt: `prompts/draft-generation/v1.0.0/draft-generation-prompt.md`

Output contract: `schemas/patent-draft/v1.0.0/patent-draft.schema.json`

Status: **Completed — Merged via PR #5**

## Boundary

The prompt transforms a validated Invention Output Schema v1.0.0 payload into a Patent Draft Generation Contract v1.0.0 payload. It drafts English technical prose only from the supplied structured analysis.

The prompt does not call a live model in AI-003. It does not define a provider adapter, modify the input schema, render DOCX, create claims, provide legal advice, or assess patentability.

## Input envelope

The caller supplies one JSON object containing `input_contract_version`, `task`, `source_analysis`, and `generation_config`. No separate input-envelope schema file exists in v1.0.0. Tests verify the envelope and validate `source_analysis` with the canonical Invention Output Schema.

The caller/Human controls `selected_title_candidate_id`. The prompt may copy only that candidate. Missing or invalid selection produces an explicit missing title; it never produces an invented title.

## Offline validation

Synthetic fixtures cover representative content, missing information, conflicting evidence, and prompt injection. Their expected outputs are deterministic offline oracles; they do not prove live-model compliance.

Automated tests verify prompt clauses, output schema validation, logical IDs, cross-references, source paths, ordering, word count, evidence closure, reverse usage, claims exclusion, and the minimal legal-assertion scanner.

## Integration limit

Before any future model invocation, a separately approved runtime task must define provider-specific schema compatibility, request construction, timeout/retry/cost policy, logging/redaction, and live evaluation. AI-003 supplies no such integration.
