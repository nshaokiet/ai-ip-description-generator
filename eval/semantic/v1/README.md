# EVAL-001 semantic quality framework v1

This package implements evaluation accounting for frozen product baseline `37d42fc8b07003aa2a67f2d1d32e64e69eb0ddb5` and approved specification v0.1.0. It does **not** run the product, call a provider, or establish semantic quality. The six manifest entries and their draft gold items are candidates pending individual Human acceptance. Only public/open-access papers were considered; all full PDFs are local-only under ignored `sources/`.

## Contents

- `manifest.json`: source provenance, license evidence, exact local file hashes, selection rationale and objective exclusion log.
- `gold/*.json`: short, atomic AI-assisted draft annotations, each `PENDING_HUMAN`. These are illustrative starting points, **not complete gold sets**.
- `rubric.md`: Human-approved thresholds, atomic semantic labels and deterministic formulas.
- `tools/evaluator.py`: strict input validation, arithmetic, non-averagable safety gates and JSON/Markdown reports.
- `reports/framework-status.*`: reproducible blocked-state report with no product-run evidence.
- `runs/local/`: ignored location for any *future separately authorized* product outputs; currently empty.

## Corpus preparation

Obtain public papers from the manifest URLs into `sources/<case_id>.pdf` only after checking provenance/license. No source PDF may be staged. Optional local integrity check:

```powershell
.\.venv\Scripts\python.exe eval/semantic/v1/tools/evaluator.py --verify-local-sources
```

The source verifier checks SHA-256 and bytes. Local PDFs were inspected as text-based and <=50 pages; this is a candidate-source check, not Human corpus approval. CI need not download copyrighted papers.

## Framework report

```powershell
.\.venv\Scripts\python.exe eval/semantic/v1/tools/evaluator.py
```

This writes `reports/framework-status.json` and `.md` and must show `BLOCKED_FOR_PRODUCT_RUNTIME_EVIDENCE`. The metric engine can be exercised with synthetic test fixtures in `tests/eval/`; those fixtures never count as product evidence.

For a future authorized run, pass `--evidence <local JSON path>`. Evidence format is an object with `runs: [{metadata, judgments}]`. Run metadata includes run/case/source/baseline IDs and hashes, prompt/schema/draft-contract versions, exact model/config/timestamp, `run_source`, provider authorization reference, and for `PRODUCT_RUNTIME` local output paths under ignored `runs/local/`. The evaluator verifies output bytes against the supplied SHA-256. Human judgments must enumerate all substantive extraction/draft assertions, applicable gold coverage, system gaps, author questions, and contract safety counts. See `schemas/` and evaluator tests for the field-level example. Do **not** create a product run or spend budget under the current approval.

The CLI refuses malformed inputs. It cannot independently establish whether a Human annotation is complete or whether a purported authorization is valid; these require external governance review. Preserve source/output files and provenance privately and follow a separate Human approval for provider credentials, budget and number of runs. No credential, private path or full source text belongs in Git or a report.

## Limitations / next gates

1. Human reviews each source/license and accepts or rejects the candidate corpus.
2. Human expands the deliberately sparse draft gold items into a complete atomic set and records acceptance; no final scoring before this gate.
3. Gemini 3.1 Pro High independently reviews the fixed framework implementation SHA; reviewer makes no production edits.
4. A separate Human decision may authorize product-runtime provider use and a budget; until then, product-runtime evidence is absent and semantic acceptance is not determined.

BLK-003 remains OPEN; live-provider smoke remains unvalidated/deferred. Neither this framework nor future bounded quality results establish production or legal readiness.
