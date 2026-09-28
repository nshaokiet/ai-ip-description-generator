# Evaluation-local schemas

`gold.schema.json` and `run-evidence.schema.json` document evaluation-local structures. Cross-record checks (case IDs, source hashes, unique IDs, complete coverage, local product-output hashes) are implemented in `../tools/evaluator.py`, with malformed-input regression cases in `tests/eval/`. These are **not** canonical product schemas and do not change the product contract. Semantic validity (actual support) is a Human judgment, never a JSON-schema inference.
