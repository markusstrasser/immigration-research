# Immigration public MVP SIPP–MEPS bridge — 2026-04-11

## Purpose

This memo records the completed bridge between the new `SIPP 2024` transition cell module and the existing `MEPS HC-251` health-cost module.

## Why this bridge exists

The public MVP needs one consistent health-cost input per SIPP profile cell.
Before this pass, the repo had:

1. [sipp_public_mvp_cells_2024.csv](sources/immigration-fiscal/data/derived/stage3_proto/sipp_public_mvp_cells_2024.csv) (`SIPP` transition / transfer / earnings cells)
2. [meps_health_cost_module_2023.csv](sources/immigration-fiscal/data/derived/stage3_proto/meps_health_cost_module_2023.csv) (age × nativity × insurance payer-incidence cells)

What was missing was the explicit join layer mapping those two profiles before scenario assembly.

## What was built

Builder:
- [build_public_mvp_sipp_meps_bridge_2024.py](sources/immigration-fiscal/data/derived/build_public_mvp_sipp_meps_bridge_2024.py)

Primary outputs:
- [sipp_meps_bridge_cells_2024.csv](sources/immigration-fiscal/data/derived/stage3_proto/sipp_meps_bridge_cells_2024.csv)
- [sipp_meps_expected_health_cost_cells_2024.csv](sources/immigration-fiscal/data/derived/stage3_proto/sipp_meps_expected_health_cost_cells_2024.csv)
- [sipp_meps_bridge_cells_2024.meta.json](sources/immigration-fiscal/data/derived/stage3_proto/sipp_meps_bridge_cells_2024.meta.json)

## Quantitative status

From the bridge meta:

- `sipp_rows_input`: `98`
- `meps_rows_input`: `81`
- `sipp_rows_matched_exact`: `98`
- `sipp_rows_matched_group_fallback`: `0`
- `sipp_rows_unmatched`: `0`
- `bridge_rows_written`: `294`
- `expected_rows_written`: `98`

Interpretation:
- `sipp_rows_matched_exact` == `98` means every SIPP cell has a direct nativity-age match in MEPS; no fallback was needed in current artifacts.
- `bridge_rows_written = 294` means an average of `3` MEPS insurance branches per matched SIPP cell.
- `expected_rows_written` gives one collapsed expected health-cost profile per SIPP cell for scenario use.

## Match and expectation logic

1. Exact match on `(age_band, nativity_code)` first.
2. Fallback to `(age_band, nativity_group)` only when exact code is missing.
3. Within-match branch shares are the MEPS insurance shares implied by `person_weight_sum`.
4. Branch shares are scaled by SIPP cell weight (`sipp_person_weight_sum`) to produce bridge rows.
5. Expected rows are payer-spend means for each SIPP cell by re-aggregating branch rows with those bridge weights.

## Constraint note

No undocumented-status inference is introduced by this bridge.
`citizenship` and `nativity` remain at their public-code levels only.

## What this unlocks

The public MVP has:

1. `SIPP 2024` transition module (`sipp_public_mvp_cells_2024.csv`)
2. `MEPS` health-cost module (`meps_health_cost_module_2023.csv`)
3. explicit `SIPP`-`MEPS` join layer with expected health-cost profiles (`sipp_meps_*_2024.csv`)

Next step is model-level consumption, not additional join construction.
