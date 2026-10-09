# USPTO_DOCUMENT_PACKAGE v1.0.0 — P2-005

This additive, offline **synthetic-only** contract assembles the validated P2-003
USPTO disclosure and P2-004 supported draft Claims into one deterministic review
package. It does not alter the published P2-001 through P2-004 contracts, expose
an API route, render a DOCX, run an AI provider, or authorize a filing.

## Public Python entry point

`backend.app.services.uspto_document_package.assemble_uspto_document_package`
accepts **keyword-only** inputs:

| Required input | Contract |
|---|---|
| `source_envelope` | Original APP-002 validated evidence envelope |
| `structured_analysis` | AI-001 analysis associated with that envelope |
| `reconstruction` | Original P2-002 result, reproduced from the preceding two inputs |
| `specification` | P2-003 USPTO_SPECIFICATION_DRAFT v2.0.0 |
| `p2_003_generation_config` | Exact P2-003 configuration sidecar |
| `supported_claims` | P2-004 SUPPORTED_DRAFT_CLAIMS v1.0.0 |
| `p2_004_generation_config` | Exact P2-004 configuration, including selected solution and P2-003 sidecar |

The assembler validates original-source reprojection, both published generation
contracts, source identity, configs and supported Claims. Invalid/mismatched input
raises `USPTODocumentPackageValidationError` with stable `code` and safe `paths`.
`validate_uspto_document_package(package, **same_inputs)` performs a complete
schema and exact-value re-projection check. Do not call `_assemble_verified`
directly with untrusted inputs; it is an internal, prevalidated projection helper.

## Output shape and Claims mapping

- `filing_view`: P2-003 `document_metadata`, `section_order`, `sections` and
  `abstract` copied without change; standalone `claims` is projected from P2-004.
- `filing_view.claims`: `section_id=CLAIMS`, `sequence=11`, `heading=CLAIMS`.
  When supported Claims exist, `status=PRESENT`,
  `preamble="What is claimed is:"`, with consecutive `claim_number` values.
  When none exist, `status=HUMAN_CONFIRMATION_REQUIRED`, an empty Claims list,
  and nonempty `missing_information_ids`. No filler text is generated.
- Each filing Claim copies P2-004 `claim_number`, `claim_type`,
  `independent_or_dependent`, `depends_on`, `claim_text` and ClaimElements;
  ClaimElements carry only `element_id`, `sequence`, `text`, `evidence_ids`,
  `specification_section_ids`, `support_status`. Full P2-004 audit fields are
  excluded from the filing view.
- `review_package`: unchanged full P2-003 and P2-004 outputs, plus P2-004
  `claim_support` projected to `claim_number`, `element_id`, `support_status`,
  `evidence_ids`, `specification_section_ids`, and any assembly-created missing
  information linking to source issues. Review warnings, excluded candidates,
  author questions and evidence remain in the original P2-004 sidecar.
- `input_digests`, `source_identity` and `package_id`: stable canonical content
  digests/identity. Input objects are never mutated.
- `review_boundary`: always DRAFT/UNREVIEWED, requires qualified Human IP
  review, `filing_ready=false`, synthetic-only. P2-003's original Claims stay
  `MISSING` and its `claims_runtime_implemented=false` invariant is preserved.

Schema: `uspto-document-package.schema.json` (JSON Schema Draft 2020-12,
strict additional properties). Its version-pinned P2-001/P2-004 references are
embedded and local so a validator needs no network access. Rebuild only from
the released local versions with `python schemas/uspto-document-package/v1.0.0/build_schema.py`.

## Validation and limits

Run `python -m pytest tests/backend/test_uspto_document_package_v1.py -q`.
The synthetic end-to-end APP-002 -> P2-002 -> P2-003 -> P2-004 chain currently
produces no eligible supported Claims: P2-002 emits unresolved solution-element
links/essentiality that P2-004 correctly marks for Human confirmation. The
positive Claims projection is therefore tested separately with the released
P2-004 curated synthetic reconstruction fixture, and **is not represented as
passing original APP-002 source-provenance validation**. The public assembler
rejects that fixture without the original source evidence.

The offline package is the input contract proposed for the independently
authorized future P2-006 renderer. It is not a renderer, live paper-to-patent
integration, production feature, patentability determination, legal opinion or
USPTO submission.
