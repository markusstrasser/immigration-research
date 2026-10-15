**Verdict:** Comparator survivor adjustments are admitted only at publication, after the evaluator used for M5 calibration.

## R2C40 — 2026-10-15

- A changed/missing own-mask summary or paired-SE file stops `[BLOCKED]` at its SHA256 pin. Regression: `test_source_drift_blocks_and_live_scaling_uses_paired_vectors`.
- An unsupported population stops rather than borrowing another frame's paired SE. The White own-count contrast holds the lineage fixed, as source `finalize.py` does; it scales only the comparator. Regression: actual population tables and source SE checks.
- A second publication pass stops rather than adding item11 twice. The evaluator/control columns retain the prior amounts. Regression: `test_base_publication_keeps_dimensionless_ratio_and_budget_identity`.
- Per-member comparator/lineage ratios remain dimensionless. Allocated member balances retain `receipts - spending` and exclude staying-nonmember effects, matching the lineage evaluator; responsive budget and net-cost fields include the explicitly separated survivor term. Regression: the same base-publication test.
- Income-tax fragility used to add every field ending in `_bn`, admitting post-evaluator metadata as a tax part. It now loads the producer's authoritative `PARTS` registry, gates every declared column, and retains the original closure tolerances. Regression: `test_tax_parts_exclude_post_evaluator_metadata_from_decomposition` and the executed local fragility gates.

These controls verify implementation and accounting, not the whole-person static-removal counterfactual. [FRAMING-SENSITIVE] [CALCULATION: comparison_contract.py; test_comparison_contract.py; source derived/gaps.csv]

## R4C4 — 2026-10-15

- A zero-production diagnostic changes the case's policy level as well as the comparison. Omitting that change from the new headline decomposition stopped 16 actual-data identities. The producer now emits `lineage_policy_delta_bn`; every published decomposition closes at 1e-9bn. Central policy delta is zero within floating precision. Regressions: `test_published_lineage_decomposition_and_complete_cost_identity`, `test_optional_policy_delta_is_printed_only_for_changed_policy`.
- A test cache keyed only by basis/end/half conflated source-current and expanded-children signed vectors. Its key now includes membership rule; actual current/children/half signed-vector identities are checked independently. Regression: `test_actual_comparator_publications_match_pinned_terms_and_paired_se`.
- The old positive-child-block assumption was invalid for a half-overlap reading that removes half of the overlap from the lineage. The transport gate now checks each reading's exact population identity; complete non-half additions still must be positive. No accounting or source tolerance was loosened. Regression: `test_completed_population_and_comparator_asymmetry`.
- The district-dollar adapter rejects mismatched principal school nationals and empty full-frame pupil exposure rather than substituting an average. Source charged Hispanic/white values and all 51 state controls reproduce independently. Regressions: `test_district_prices_oct15.py`, `test_r4_adjustments.py`.

- Literal O-F8 review found A3/A4 own-count item11 SEs missing from the report although matched-count SEs were correct. The producer now exports own-count amount, comparator SE and paired SE, with a fixed lineage vector; both counts are printed. Regressions: `test_a3_a4_derived_publications_use_reconstructed_own_counts_and_factors`, `test_round4_render_preserves_prefix_and_se_distinctions`.
