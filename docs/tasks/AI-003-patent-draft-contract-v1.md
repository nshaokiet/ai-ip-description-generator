# AI-003 — Patent Draft Generation Contract v1.0.0

## Metadata

| Field | Value |
|---|---|
| Task ID | AI-003 |
| Owner | ChatGPT/Codex |
| Reviewer | Gemini 3.1 Pro High |
| Approver | Human / Product Owner |
| Status | Gemini Review Passed — Awaiting Human Merge Approval |
| Contract version | 1.0.0 |
| Base commit | `649b632bd9def72f29ad5bfbe60f9e4f5766448a` |
| Implementation branch | `ai/patent-draft-contract-v1` |
| Related ADR | ADR-008 |

## Objective

Create the strict, versioned contract and offline drafting prompt that transform a validated Invention Output Schema v1.0.0 payload into a grounded English patent-description draft suitable as the future input to DOC-001.

## In scope

- JSON Schema Draft 2020-12 output contract.
- Document metadata, notice, selected title, Abstract, ordered sections/subsections, technical paragraphs, drawings, missing information, conflicts, author questions, and used-evidence appendix.
- Relative source JSON Pointers and paragraph-level evidence traceability.
- Documented prompt input envelope without a separate input schema.
- Draft Generation Prompt v1.0.0.
- JSON Schema and downstream business validation.
- Synthetic representative, missing, conflict, prompt-injection, claims, missing-evidence, and cross-reference fixtures.
- Offline automated tests and documentation.
- AI-001 and AI-002 regression testing.

## Out of scope

- Claims or Draft Claims.
- Legal advice, novelty, inventive-step, non-obviousness, eligibility, or patentability conclusions.
- Changes to Output Schema v1.0.0 or Extraction Prompt v1.0.0.
- DOCX template/rendering or DOC-001 implementation.
- API, frontend, backend, database, storage, parsing, OCR, provider adapter, live model, deployment, or PDF output.
- Human approval/audit state in the payload.
- Real or unpublished research data.

## Deliverables

- `schemas/patent-draft/v1.0.0/patent-draft.schema.json`
- `schemas/patent-draft/v1.0.0/README.md`
- `prompts/draft-generation/v1.0.0/draft-generation-prompt.md`
- `prompts/draft-generation/v1.0.0/README.md`
- `docs/decisions/ADR-008-patent-draft-contract-v1.md`
- `tests/draft/test_patent_draft_contract_v1.py`
- Seven synthetic fixtures and fixture documentation under `tests/fixtures/patent-draft/v1.0.0/`

## Approved decisions

- Contract version `1.0.0`, Draft 2020-12, canonical schema ID and path.
- Caller/Human selects an existing title candidate; the model never invents a title.
- Status enum is only `PRESENT` and `MISSING`.
- Exact eleven-part document order, six technical sections, and seven canonical subsections.
- Required missing marker is `[AUTHOR CONFIRMATION REQUIRED]`.
- Abstract is required structurally, supports missing state, and has a 150-word maximum.
- Abstract word count uses NFKC plus Unicode `\b\w+(?:[-'’]\w+)*\b`.
- Draft-origin gaps use only four approved rule IDs.
- Conflicts have at least two evidence IDs and remain unresolved.
- Evidence appendix contains only used evidence.
- `output_notice.includes_claims` is always false.
- Minimal prohibited-assertion scanning is defense in depth only.
- No new dependency; use `jsonschema==4.26.0` and Python 3.12 standard library.
- Expected outputs are offline oracles, not live-model evidence.

## Acceptance criteria

- [x] Canonical schema exists at the approved path and self-validates as Draft 2020-12.
- [x] `$id`, schema version, and output type have the approved constants.
- [x] All schema objects use `additionalProperties: false`.
- [x] Claims, Draft Claims, and Human approval state are absent.
- [x] Notice flags mechanically exclude legal advice, filing readiness, patentability assessment, and claims.
- [x] Exact 11-part section order is enforced.
- [x] Six technical sections and seven subsections are ordered and machine-validatable.
- [x] Title and Abstract support `PRESENT` and `MISSING` with approved marker behavior.
- [x] Present Abstract includes declared word count with maximum 150.
- [x] Every technical paragraph requires source paths and grounding evidence IDs.
- [x] Drawing, missing-information, conflict, author-question, and evidence-appendix contracts are strict.
- [x] Prompt documents the exact input envelope, treats all source content as untrusted, and emits output-only JSON.
- [x] Prompt forbids tools, browsing, external knowledge, claims, and legal/patentability conclusions.
- [x] Representative, missing-information, conflicting-evidence, and prompt-injection cases use synthetic data.
- [x] Unsupported claims fixture fails JSON Schema due to root `additionalProperties`.
- [x] Missing-evidence fixture fails at the intended `minItems` path.
- [x] Invalid-cross-reference fixture passes JSON Schema and fails business validation at the intended path and target ID.
- [x] AI-001 regression is 15/15 pass.
- [x] AI-002 regression is 17/17 pass.
- [x] AI-003 automated tests pass: 25/25, zero failures/errors.
- [x] `git diff --check` passes and diff contains exactly 23 approved files.
- [x] Gemini independent read-only review is complete: `PASS`, no findings, no required changes.
- [ ] Human has decided review findings and merge.

The Gemini review criterion is satisfied by the Human-authorized review evidence dated 20/09/2026. Human merge remains unchecked. AI-003 must not be marked `Completed` before Human merge approval and post-merge governance closeout.

## Test commands

```powershell
$env:PYTHONDONTWRITEBYTECODE="1"
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip show jsonschema
.\.venv\Scripts\python.exe -m unittest discover -s tests/schema -p "test_*.py" -v
.\.venv\Scripts\python.exe -m unittest discover -s tests/prompt -p "test_*.py" -v
.\.venv\Scripts\python.exe -m unittest discover -s tests/draft -p "test_*.py" -v
git diff --check
```

## Security and privacy

Fixtures are synthetic. Tests make no network calls. No secret, PII, unpublished research input, full paper, model response, or provider data is allowed in the task artefacts.

## Handoff state

Gemini 3.1 Pro High completed independent read-only review with verdict `PASS`, no findings, and no required changes. This recommendation does not replace Human merge approval. DOC-001 must not start before AI-003 is Human-approved and merged.
