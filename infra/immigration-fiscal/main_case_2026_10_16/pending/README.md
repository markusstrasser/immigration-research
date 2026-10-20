# Corrections held for the next main case

Adopted case v9 (key `oct16`) stays byte-identical. Each correction below is confirmed, sized below one-decimal
printing, and deferred because applying it now would re-pin about 20 consumer lanes that hash this case's
package (and about 50 files that hash `main_case_2026_09_24/package.cjs`). Apply all of them when the next main
case is built, then delete this directory.

| # | Correction | Where | Effect on v9 | Patch |
|---|---|---|---|---|
| 1 | NIBRS stores unknown age as `00`/`NS` (age_id 103/104); the restage parsed it as age 0. Fixed in commit 5bcb5d8e; held out of the adopted chain, so `offender_ethnicity_nibrs_2026_09_23`, `crime_ratio_direction_2026_09_24` and `crime_victim_cost_2026_09_23` were restored to their pre-fix state (crime_victim_cost's mortality receipt pins the first two lanes' sources and ignored caches). `business_crime_2026_10_21` keeps its own fixed age parse. | `offender_ethnicity_nibrs_2026_09_23/nibrs_stage.py`; `crime_ratio_direction_2026_09_24/nibrs_restage.py` and gates; `crime_victim_cost_2026_09_23` pins and test tolerance; rebuild both lanes' `_cache` stages | Booking delta 0.868803 → 0.866191: justice line about −$0.0027bn. Lineage victims +$0.000036 / +$0.000040bn. Murder ratio 2.303 → 2.311; mean recorded-offender age 31.17 → 33.42. | `nibrs_age_fix_offender_lane.patch`, `nibrs_age_fix_crime_chain.patch` (code and pins only; rerun the lanes' documented commands for derived files) |
| 2 | Booking rows are looked up by exact label text, so a relabel (`RR x 1.0401` → `1.0400`) throws. Match by scope text and fail on zero or several matches. | `main_case_2026_09_24/package.cjs:313-319`; `outside_checks_combined_2026_09_24/combine.cjs:105-106` | none | write with #1 |
| 3 | Item 13's variant branch tested `base !== V8` by object identity, so the uncached route repriced the canonical case as a variant and took per-line amounts from the first method only; real variants kept v8 block/part metadata. No cost reads those fields (`postAdditions` recomputes deltas). | `package.cjs` item 13 branch; `run_all.sh` | none: corrections.json, bands and totals unchanged; `break_conditions_2026_09_29` refuses `V9_CASE_CACHE=0` meanwhile | `item13_routes.patch` (adds `test_routes.cjs`, which fails on the unpatched package) |

Recorded 2026-10-21. Found by the business-crime and within-group lanes (#1, #2) and the v9 consumer
reruns (#3); see `failure-catalog.md`.
