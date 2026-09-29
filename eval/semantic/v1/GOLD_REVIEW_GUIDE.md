# EVAL-001 candidate gold review guide

Corpus selection: **6/6 HUMAN_ACCEPTED** (Human / Product Owner, 2026-09-29). Candidate annotation inventories: **6/6 complete**. Gold acceptance: **0/6**; every package remains `PENDING_HUMAN` with null reviewer/date. Completion here means an implementation-agent inventory of the full single-PDF input, not Human validation or semantic acceptance.

| Case | Paper / domain | Items | KEY | SECONDARY | Missing-information target(s) |
|---|---|---:|---:|---:|---|
| eval-en-002 | Multi-objective numerical optimization of 3D-printed PLA bio-metamaterial / additive manufacturing and materials | 28 | 20 | 8 | `EN002-GAP-01`: optimized-sample fatigue life modeled; experimental fatigue validation deferred |
| eval-en-003 | Recognition of mulberry leaf diseases based on multi-scale residual network fusion SENet / agricultural computer vision | 25 | 15 | 10 | `EN003-GAP-01`: 100-versus-50 training-iteration description requires Human materiality decision |
| eval-en-004 | Growth and nutrient removal efficiency of duckweed from leachate / environmental biotechnology | 25 | 17 | 8 | `EN004-AMBIGUITY-01`: synthetic COD prose/Table 1 conflict |
| eval-en-005 | Field pea leaf disease classification using a deep learning approach / agricultural computer vision | 26 | 16 | 10 | `EN005-AMBIGUITY-01`: DenseNet201-versus-DenseNet121 architecture conflict |
| eval-en-007 | Osmosis-Based Pressure Generation: Dynamics and Application / fluidic mechanical engineering | 24 | 18 | 6 | `EN007-GAP-01`: standalone PDF lacks referenced Appendix S3 calibration detail |
| eval-vi-001 | HỆ KHUYẾN NGHỊ CỘNG TÁC ĐỒNG TÁC GIẢ / scholarly recommendation software | 26 | 16 | 10 | `VI001-GAP-01`: classifier split and SVM hyperparameters unspecified |
| **Total** | Five English, one Vietnamese | **154** | **102** | **52** | Six candidate targets |

Categories represented:

- `eval-en-002`: technical_field, technical_problem, technical_solution, component, process_step, distinguishing_feature, technical_effect, experimental_data, embodiment_example, missing_information, prohibited_conclusion.
- `eval-en-003`: technical_field, technical_problem, technical_solution, component, process_step, distinguishing_feature, technical_effect, experimental_data, missing_information, prohibited_conclusion.
- `eval-en-004`: technical_field, technical_problem, technical_solution, component, process_step, distinguishing_feature, technical_effect, experimental_data, ambiguity_conflict, prohibited_conclusion.
- `eval-en-005`: technical_field, technical_problem, technical_solution, component, process_step, distinguishing_feature, experimental_data, embodiment_example, ambiguity_conflict, prohibited_conclusion.
- `eval-en-007`: technical_field, technical_problem, technical_solution, component, process_step, distinguishing_feature, technical_effect, experimental_data, embodiment_example, missing_information, prohibited_conclusion.
- `eval-vi-001`: technical_field, technical_problem, technical_solution, component, process_step, distinguishing_feature, experimental_data, embodiment_example, missing_information, prohibited_conclusion.

## Human review

Open each local-only source PDF alongside its `gold/<case-id>.json`. For **each** item, verify the atomic normalized proposition, KEY/SECONDARY importance, precise page/section/table locator, and short source-language excerpt. Check that numerical values, units and comparison baselines are exact; decide whether each gap/conflict is material and warrants an author question. Review prohibited-conclusion items as **evaluator safety expectations**, not assertions made by the paper. Resolve any omission, overreach or combined proposition before marking a package `ACCEPTED` with a real Human reviewer and date. Corpus acceptance does not imply gold acceptance.

No provider call or product-runtime evaluation is authorized (budget 0). Product-runtime evidence is absent; semantic acceptance is NOT DETERMINED; EVAL-001 is not Completed; BLK-003 remains OPEN. Do not commit the local PDFs.
