# ADR-009 — Patent DOCX Template v1.0.0

## Metadata

| Field | Value |
|---|---|
| ADR ID | ADR-009 |
| Status | Accepted — Gemini Review Passed — Awaiting Human Merge Approval |
| Date | 20/09/2026 |
| Decision owner | Human / Product Owner |
| Implementation owner | ChatGPT/Codex |
| Reviewer | Gemini 3.1 Pro High |
| Related task | DOC-001 |

## Context

AI-003 established Patent Draft Generation Contract v1.0.0 as the stable, claim-free boundary between validated drafting content and presentation. DOC-001 needs an editable English DOCX with deterministic formatting, explicit evidence traceability, preserved missing/conflict state, and a mandatory Human-review notice.

## Decision

Adopt a versioned `docxtpl` template and deterministic offline Python renderer:

```text
Validated Patent Draft Generation Contract v1.0.0
→ Patent DOCX Template v1.0.0
→ editable DOCX requiring Human review
```

The canonical template is `templates/patent-docx/v1.0.0/patent-description-template.docx`. The renderer is `tests/docx/render_patent_docx_v1.py` and validates the payload against the canonical AI-003 schema before rendering.

The document uses A4 pages, 2.54 cm margins, Times New Roman, the approved heading hierarchy, exact header/footer notices, and PAGE/NUMPAGES fields. The eleven-part order is fixed. Claims are excluded. Missing content retains its heading and exact marker; conflict and inference labels remain visible; used evidence is rendered in the appendix.

Generated review output is restricted to `generated/patent-docx/v1.0.0/`, which remains Git-ignored. Rendering is offline, uses `autoescape=True`, and makes no API/model/network call.

## Alternatives considered

### Generate DOCX directly with `python-docx`

Rejected as the canonical runtime approach because it would combine template design and data mapping in procedural code. `python-docx` remains appropriate for deterministic construction and structural inspection of the versioned template.

### Render directly from Invention Output Schema v1.0.0

Rejected because title selection, ordered draft prose, missing/conflict rules, and evidence closure belong to the already approved Patent Draft Generation Contract.

### Produce PDF in DOC-001

Rejected because PDF export is outside the approved scope and would add platform-specific dependencies.

### Embed figures automatically

Rejected because DOC-001 has no approved figure-generation or trusted binary-image input contract.

## Consequences and trade-offs

Positive consequences include deterministic offline rendering, a reviewable mapping, strict schema rejection before output, editable DOCX delivery, and mechanical exclusion of Claims. Trade-offs include dependence on Word-compatible field refresh for PAGE/NUMPAGES display and the need for Human visual QA across Microsoft Word environments.

Automated XML/package tests do not replace visual inspection. Human Microsoft Word Visual QA and Gemini 3.1 Pro High independent review both passed with no findings or required changes; 85/85 tests passed. The implementation status is `Gemini Review Passed — Awaiting Human Merge Approval`; implementation commit, Pull Request, and merge commit do not yet exist.

## Compatibility and evolution

- Patch changes may correct documentation or formatting without changing accepted input semantics.
- Backward-compatible optional presentation capabilities require a minor version.
- Changed input contract, section order, claims boundary, or required rendering semantics require Human approval and a major version or separately versioned template.

Patent Draft Generation Contract v1.0.0 is not modified by this decision.

## Security and privacy

Fixtures are synthetic. Input strings are untrusted data and are XML-escaped. The template contains no macros, active content, embedded objects, remote images, or external relationships. The renderer logs only safe error context and never transmits data.
