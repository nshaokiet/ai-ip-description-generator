# PREAPI-E — Fixture-only evaluation readiness

| Field | Value |
|---|---|
| Version | 0.1.0, review candidate |
| Status | Draft implementation; independent review pending; no merge or semantic acceptance |
| Task / authority | PREAPI-E; Human zero-cost development instruction, 21/10/2026 |
| Base | `d7516d4322f828c5802ec6d9e5ef5f8dffa5721d` |
| Dependency | Existing Human-accepted EVAL-001 gold and evaluator; no C1/C2 runtime dependency for this inventory check |

## Contract

`python -m eval.semantic.v1.tools.fixture_readiness` reads only the existing
`eval/semantic/v1/manifest.json` and six `gold/*.json` files. It applies the
released evaluator's manifest and gold validators, verifies one matching gold
file per manifest case, computes KEY/SECONDARY totals, and records SHA-256 of
each file's current bytes. It invokes the evaluator with **no run evidence**
to confirm `semantic_acceptance=NOT_DETERMINED` and product run count zero.
It never loads source PDFs, constructs a model client or writes accepted gold.

The report has `result=FIXTURE_VALIDATED` only if the existing validators pass
and every corpus/gold record is Human-accepted. This means the offline fixture
inventory is internally consistent. It does not say any assertion is true,
any Claims are supported, or any product output meets the rubric. Malformed,
missing, duplicated or unaccepted gold fails closed; the CLI exits nonzero.
The optional `--json-out` must point outside the accepted gold directory.

Current accepted inventory, checked from repository files: **6 cases, 154
items, 102 KEY and 52 SECONDARY**. These values are test expectations for the
frozen corpus; the report itself derives counts from files. Each report embeds
the manifest and gold byte hashes so a later reviewer can identify the exact
fixture snapshot. `provider_execution=NOT_RUN` and `product_runtime=NOT_DETERMINED`
remain explicit.

## Source and acceptance matrix

| Check | Source | Failure behavior |
|---|---|---|
| Case identity and accepted selection | `manifest.json`, `evaluator.validate_manifest` | Fail on malformed, duplicate or unaccepted selection |
| Gold identity, source digest, category, locator and duplicate item ID | `gold/*.json`, `evaluator.validate_gold` | Fail on mismatched or malformed gold |
| Item and importance totals | Validated gold items | Derive actual values; regression test pins accepted 6/154/102/52 |
| Fixture provenance | Raw manifest/gold bytes | SHA-256 per file, no source-paper content in report |
| Product separation | `evaluator.evaluate(..., evidence=None)` | Zero product runs; semantic acceptance stays `NOT_DETERMINED` |

The existing `tests/eval/test_semantic_evaluator.py` checks scoring arithmetic,
unsupported/contradicted assertions, missing evidence, Claims violations,
refusals, malformed evidence and synthetic-run exclusion. New
`tests/eval/test_preapi_e_fixture_readiness.py` checks actual inventory,
determinism, gold byte immutability, missing file, duplicate item ID and
unaccepted gold. No synthetic score is represented as model output.

## Review and later gates

Reviewers should verify the checker cannot consume or promote product runtime
evidence, validate reported file hashes against the candidate tree and inspect
the negative tests. The exact implementation SHA requires independent Gemini
read-only review and CI before any merge. A funded provider/model/budget and
lawful-source decision is separate. EVAL-001 PRODUCT_RUNTIME stays
`NOT_DETERMINED` and BLK-003 remains open.
