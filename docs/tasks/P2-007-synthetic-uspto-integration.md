# P2-007 — Controlled Synthetic USPTO Export Integration

| Contract field | Value |
| --- | --- |
| Task ID | P2-007 |
| Version | 0.1.0 |
| Date | 2026-10-12 |
| Status | Human-authorized implementation; independent fixed-SHA review pending |
| Source of truth | [Issue #106](https://github.com/nshaokiet/ai-ip-description-generator/issues/106) |
| Workflow / owner | V1 / Codex |
| Reviewer | Gemini 3.1 Pro High, Antigravity, strictly read-only |
| Breaking changes | No |

Provider calls: none. Render deployment/configuration: excluded.

## Controlled source and provenance

The only exposed sample identifier is `p2-005-representative-system-v1`. It binds to the checked-in synthetic file `tests/fixtures/invention-reconstruction/v1.0.0/representative-system.json` with mandatory SHA-256 `9a4be99442b39f871cb4bde7573fc9ddb47d942a6ad8fc4164c894122f18a233`. The backend never accepts user-supplied P2-005 package JSON, generation config, Claims, sample path, or document ID through these endpoints.

Seven original P2-005 inputs are reconstructed from the fixed synthetic source using the existing released pipeline:

| Validated input | Derivation |
| --- | --- |
| `source_envelope` | Trusted fixture's `source_envelope` |
| `structured_analysis` | Trusted fixture's `structured_analysis` |
| `reconstruction` | `reconstruct_invention(source_envelope, structured_analysis)` |
| `specification` | `generate_uspto_specification(reconstruction, p2_003_generation_config)` |
| `p2_003_generation_config` | Fixed `{source_document_synthetic: true}` |
| `supported_claims` | `generate_supported_draft_claims(reconstruction, specification, p2_004_generation_config)` |
| `p2_004_generation_config` | Fixed synthetic, English, U.S., `SYSTEM`, max four dependents; solution id from validated reconstruction; exact P2-003 config copy |

`assemble_uspto_document_package` assembles/validates source identity, nested relationships, digests and Claims boundary. `render_uspto_document_package` independently revalidates the full package with all seven originals before creating the four real files in a temporary directory. Only validated files are copied into an application-local, bounded in-memory cache. Every cold instance repeats source/provenance and rendering checks. Failures return a generic `503` without leaking source paths or exception details.

| Download | Origin | Status |
| --- | --- | --- |
| `B2_REFERENCE_PREVIEW.pdf` | P2-006 B2 two-column PDF reference renderer | Synthetic draft; not issued |
| `B2_REFERENCE_PREVIEW.docx` | P2-006 B2 two-column editable DOCX renderer | Synthetic draft; not issued |
| `USPTO_APPLICATION_DRAFT.pdf` | P2-006 application PDF renderer | Synthetic draft; not filing-ready |
| `USPTO_APPLICATION_DRAFT.docx` | P2-006 application editable DOCX renderer | Synthetic draft; not filing-ready |

The four files reflect **one controlled synthetic research sample**, not the current user's upload, reviewed edits, or DOCX v1 revision. Claims are explicitly `HUMAN_CONFIRMATION_REQUIRED`; output must include the renderer's incomplete-Claims marker. Neither Claims nor patentability/issuance is represented as validated. Existing editable DOCX v1 export remains on the original route and pipeline.

## API boundary

Only `backend.app.demo_staging` registers `GET /api/demo/uspto/exports` (validated manifest) and `GET /api/demo/uspto/exports/{sample_id}/{filename}` (attachment). The normal backend app does not register these routes. `sample_id` and `filename` must exactly match the fixed allowlists. No query/body, arbitrary path, or external document storage is consumed. Attachments use fixed Content-Type, Content-Disposition, `Cache-Control: no-store`, and `nosniff`. Outputs are generated provider-free. Rendering is on first request; staging free-tier cold starts may delay the initial manifest.

## Gate status

Implementation, tests, independent exact-SHA review, PR CI, merge, and closeout must each be recorded from observed evidence. No deployment or production readiness is implied by implementation PR status.
