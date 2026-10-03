# Executable synthetic reconstruction corpus v1.0.0

All content is invented test data, not a real paper or confidential research.

`representative-system.json` contains both canonical upstream payloads. The other
15 cases extend it using explicit JSON Patch operations (`add`, `replace`, `copy`,
`remove`) implemented by `tests/reconstruction_fixture_support.py` without a new
dependency. `input_patches` change synthetic upstream inputs; `output_patches`
exercise contract/business rejection or explicitly supplied review candidates.
`assertions` check emitted values; `expected_error` checks a safe failure code.

Every JSON case is executed by the parametrized backend corpus test, including
deterministic regeneration. Schema tests also verify the exact 16-case inventory.

The SAFE_GENERALIZATION and proposed-variant cases are validator fixtures, not
producer output. Only the proposed-variant fixture opts into
`allow_review_candidates=True`; the production adapter uses the default `False`,
always emits an empty variant array, and cannot generate Human confirmation.
The candidate has `human_confirmation_required=true` and
`filing_content_eligible=false`; no candidate is promoted or drafted for filing.
