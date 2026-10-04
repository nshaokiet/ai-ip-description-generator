# P2-003 synthetic fixture corpus and acceptance matrix

`minimal-synthetic.json` is wholly invented engineering test data, not a paper,
real patent, scientific gold label, or proof of semantic acceptance. It exercises
schema-representable states beyond the current P2-002 producer's conservative
defaults. The separate producer-compatibility test consumes its genuinely
upstream-validated synthetic output. Production callers must supply a reconstruction
already validated by the upstream P2-002 pipeline; P2-003's reconstruction-only
gate checks internal integrity and does not replace original source validation.

The explicitly numbered tests in
`tests/backend/test_uspto_specification_generation_v2.py` cover categories 01–24
from specification Section 35 using this canonical fixture and auditable mutations.
They cover system/method/relationships/parameters/multiple embodiments/multiple
titles/missing field/admin gaps/conflicts/SAFE_GENERALIZATION/proposed variants/
supported and insufficient drawing text/example scope/range attack/injection/
legal contamination/Claims/Abstract/Sequence Listing/INID/official numbers/
dangling source pointers/nonexistent evidence. Tests named `test_provenance_A`
through `test_provenance_H` implement amendment cases A–H explicitly.

## Implementation self-check matrix

This matrix is Codex self-check evidence, not independent implementation approval.
The historical specification review PASS does not approve this implementation.
The test names below are stable search keys; inspect their assertions and CI logs.

| AC | Test/evidence |
|---|---|
| 01 | `test_real_p2_producer_output_consumed_without_upstream_service_inputs`; no route/frontend wiring in diff |
| 02 | producer compatibility; `test_safe_errors_human_state_reference_cycles_and_invalid_schema` |
| 03 | `test_01_system_canonical_identity_and_closed_gates` and canonical Draft202012Validator |
| 04 | canonical output schema and `test_01`; sections/order constants copied from released target |
| 05 | `test_21_22_inid_and_official_numbers_blocked` |
| 06 | `test_08_administrative_gaps_and_review_separation` |
| 07 | `test_01` (zero NOT_APPLICABLE), admin/sequence-listing tests |
| 08 | `test_06_titles_exact_selection_no_selection_and_empty` |
| 09 | `test_07_missing_field_and_context_are_explicit_subsection_gaps`; `test_01` |
| 10 | numbered 01/07/17; related-art template copies context only |
| 11 | numbered 01/09/18; summary requires an eligible solution |
| 12 | numbered 12/13; drawing text exact cited-source match, no pixels/vision |
| 13 | numbered 02–05; stable input/category ordering in `_build_specification` |
| 14 | `test_essentiality_preserved`; conditional gap test; output tampering test |
| 15 | `test_03_all_controlled_relationships_remain_exact` (all 16 enums) |
| 16 | `test_02_method_order_dependencies_conditions_and_grounding`; cycle rejection |
| 17 | `test_flow_enum_not_inferred` (all six enums) |
| 18 | numbered 04/15; input literal range-pair check; exact output reprojection |
| 19 | `test_14_parameter_scope_not_strengthened` (all three states) |
| 20 | numbered 02/01; `test_effect_basis_conditions_and_non_promotion`; effect basis and conditions copied; aggregation includes condition support |
| 21 | `test_05_multiple_embodiments_in_input_order` |
| 22 | `test_11_variant_source_gate_and_proposed_exclusion` |
| 23 | numbered 02/10; aggregation preserves most conservative eligible class |
| 24 | numbered 23/24; input integrity and output pointer/evidence closure |
| 25 | `test_09_conflict_taint_propagates_without_selecting_a_side` |
| 26 | `test_review_gaps_questions_and_unknown_routes_preserved` |
| 27 | `test_18_claims_hard_gate`; output gate tampering test |
| 28 | `test_19_abstract_whole_sentences_count_and_insufficient_limit` |
| 29 | `test_20_sequence_listing_human_confirmation` |
| 30 | safe-error and unaudited resolved-conflict tests |
| 31 | numbered 08/26; only source technical fields enter paragraph templates |
| 32 | `test_17_legal_contamination_is_excluded`; parameter contamination test |
| 33 | numbered 16; provenance E/F; no eval/exec or commands derived from text |
| 34 | `test_provenance_G_determinism_and_deep_mutation_isolation` |
| 35 | provenance G, no-SHA mapping test, fresh deep-copied output |
| 36 | `test_pure_offline_entrypoint_never_uses_network`; no provider/service dependency added |
| 37 | provenance H plus baseline Git diff/hashes and existing regressions |
| 38 | numbered 23/24; source paths/evidence remain available; Claims never generated |
| 39 | explicit numbered categories 01–24 plus additional adversarial mutations |
| 40 | **PENDING INDEPENDENT IMPLEMENTATION REVIEW** — no self-approved PASS |
| 41 | explicit provenance tests A–H |

## Boundaries

No provider/model use, real/confidential data, Claims, P2-004, frontend/runtime
integration, DOCX v2, deployment, or production change. BLK-003 OPEN;
PRODUCT_RUNTIME DEFERRED — AWAITING FUNDING; semantic acceptance NOT DETERMINED.
