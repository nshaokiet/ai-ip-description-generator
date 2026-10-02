# ADR-011 — USPTO Patent Specification Target v2.0.0

## Metadata

| Field | Value |
| --- | --- |
| ADR ID | ADR-011 |
| Status | Proposed — P2-001 fixed-SHA review pending |
| Date | 02/10/2026 |
| Decision owner | Human / Product Owner |
| Implementation owner | ChatGPT/Codex |
| Reviewer | Gemini 3.1 Pro High / Antigravity read-only |
| Related task | P2-001 |
| Authorization | `HUMAN-P2-001-USPTO-TARGET-2026-10-02` |

## Context

The existing MVP validates an evidence-grounded, claim-free Patent Description Draft v1.0.0 and synthetic public workflow. The Human / Product Owner clarified the actual product objective as:

`one scientific research paper → one USPTO-style patent specification draft`

with issued patents `US11367264B2` and `US11044591B2` supplied as structural examples.

The existing v1 contract intentionally excludes Claims and includes internal review sections that are useful for drafting support but are not part of a filing-style specification body.

## Decision

Adopt **USPTO Patent Specification Target v2.0.0** as the future product target.

The target is a **draft nonprovisional utility patent specification for Human/IP-specialist review**, not an issued patent facsimile, not legal advice, and not a filing-ready guarantee.

Record the target as a strict JSON Schema Draft 2020-12 contract at `schemas/uspto-specification/v2.0.0/uspto-specification.schema.json`, accompanied by a neutral Human-readable template, synthetic fixtures, structural reference maps, and offline contract tests. This contract is not wired into runtime by P2-001.

Use USPTO current guidance and MPEP § 608 / 37 CFR 1.77(b) as normative structural references. The Human-supplied B2 patents are example corpora only.

### Target structure

The v2 target models, where applicable:

1. TITLE OF THE INVENTION
2. CROSS-REFERENCE TO RELATED APPLICATIONS
3. STATEMENT REGARDING FEDERALLY SPONSORED RESEARCH OR DEVELOPMENT
4. NAMES OF PARTIES TO A JOINT RESEARCH AGREEMENT
5. INCORPORATION BY REFERENCE
6. STATEMENT REGARDING PRIOR DISCLOSURES
7. BACKGROUND OF THE INVENTION
8. BRIEF SUMMARY OF THE INVENTION
9. BRIEF DESCRIPTION OF THE DRAWINGS
10. DETAILED DESCRIPTION OF THE INVENTION
11. CLAIM OR CLAIMS
12. ABSTRACT OF THE DISCLOSURE
13. SEQUENCE LISTING when applicable.

Background may include Field of the Invention and Description of Related Art.

### Output separation

Future implementation will separate:

- **USPTO-style specification draft** — filing-style prose/claims/abstract only; and
- **Review package** — source evidence, grounding labels, missing information, author questions, claim support and QA metadata.

### Administrative facts

Administrative/legal metadata that does not arise safely from the scientific paper must never be invented. It requires Human-supplied or separately authorized evidence.

### Claims

Claims are restored as a **future v2 product requirement**, reversing the v1 product-target limitation, but P2-001 itself does not implement Claims generation. A separately authorized P2-004 (or equivalent) must define and implement Claims behavior, validation and review requirements.

### Compatibility

Do not mutate released v1 artefacts in place. v2 must be introduced through new versioned contracts/prompts/templates/adapters.

## Consequences

### Positive

- Product target now matches the Human-requested paper-to-USPTO-specification objective.
- UI, AI pipeline, Claims work and DOCX v2 can converge on one canonical structure.
- Administrative hallucinations are explicitly blocked.
- Internal grounding remains available without contaminating the filing-style draft.
- Existing engineering infrastructure can be reused rather than rewritten.

### Trade-offs

- v2 is a major semantic evolution from the claim-free v1 contract.
- Claims require separate legal/technical quality controls.
- A scientific paper may not contain enough administrative, enablement, embodiment or claim-support information; Human confirmation remains necessary.
- A specification structurally resembling USPTO practice does not establish patentability or filing readiness.

## Sources

- USPTO Nonprovisional (Utility) Patent Application Filing Guide: https://www.uspto.gov/patents/basics/apply/utility-patent
- USPTO MPEP § 608: https://www.uspto.gov/web/offices/pac/mpep/s608.html
- Reference patent `US11367264B2`: https://patentimages.storage.googleapis.com/91/f6/9b/18dc2af29220c8/US11367264.pdf
- Reference patent `US11044591B2`: https://patentimages.storage.googleapis.com/42/19/af/1c5089854ab9d4/US11044591.pdf

## Boundaries

This decision does not authorize:

- provider/API spend;
- real/confidential research data;
- production;
- filing;
- prior-art/patentability conclusions;
- Claims runtime implementation;
- modification of released v1 semantics.

BLK-003 remains OPEN. EVAL-001 PRODUCT_RUNTIME remains DEFERRED — AWAITING FUNDING.
