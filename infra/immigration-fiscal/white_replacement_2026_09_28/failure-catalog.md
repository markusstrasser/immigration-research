**Verdict:** Comparator survivor adjustments are admitted only at publication, after the evaluator used for M5 calibration.

## R2C40 — 2026-10-15

- A changed/missing own-mask summary or paired-SE file stops `[BLOCKED]` at its SHA256 pin. Regression: `test_source_drift_blocks_and_live_scaling_uses_paired_vectors`.
- An unsupported population stops rather than borrowing another frame's paired SE. The White own-count contrast holds the lineage fixed, as source `finalize.py` does; it scales only the comparator. Regression: actual population tables and source SE checks.
- A second publication pass stops rather than adding item11 twice. The evaluator/control columns retain the prior amounts. Regression: `test_base_publication_keeps_dimensionless_ratio_and_budget_identity`.
- Per-member comparator/lineage ratios remain dimensionless. Allocated member balances retain `receipts - spending` and exclude staying-nonmember effects, matching the lineage evaluator; responsive budget and net-cost fields include the explicitly separated survivor term. Regression: the same base-publication test.
- Income-tax fragility used to add every field ending in `_bn`, admitting post-evaluator metadata as a tax part. It now loads the producer's authoritative `PARTS` registry, gates every declared column, and retains the original closure tolerances. Regression: `test_tax_parts_exclude_post_evaluator_metadata_from_decomposition` and the executed local fragility gates.

These controls verify implementation and accounting, not the whole-person static-removal counterfactual. [FRAMING-SENSITIVE] [CALCULATION: comparison_contract.py; test_comparison_contract.py; source derived/gaps.csv]
