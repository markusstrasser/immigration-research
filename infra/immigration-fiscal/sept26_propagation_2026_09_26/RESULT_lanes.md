claude-opus-5-5

# W1 `lanes`: schools at full average cost as the default case

**Verdict:** Done. The back-cast, distribution, uncertainty and debt-legacy lanes now run `sept26_schools`
(`main_case_schools_full_2026_09_26`, $258.4885–291.9548bn) by default. `--case sept26` and `--case sept24`
rebuild the committed files byte for byte, as does `--case sept23` where a lane has it. Every gate the lead
listed reproduces, two default runs are byte-identical, and all 23 tests pass. One premise in the brief does
not hold in the debt lane: the school step is 1.0–12.9% federal, depending on the payer convention (8.2% under
the central one), so it is not all state and local. Nothing is committed or staged.

Model self-report: claude-opus-5-5 (Opus 5.5), 2026-09-26. Numbers are [CALCULATION] from the files named.
I re-verified everything after f1e4f5b changed the schools lane's `summary.json`. That commit changed the
school line and the unfunded parts, and none of these lanes reads either field.

## Case switch

Each lane has one case table, and its default is the last entry. Adding a case takes one line.

| Lane | Switch | `sept26_schools` entry |
|---|---|---|
| back-cast | `backcast.py` `LATER_CASES` | `("main_case_schools_full_2026_09_26", "_schools_full_", "adopted_2026_09_26", "_sept26_")` |
| distribution | `distribute.py` `LATER_CASES` | `("main_case_schools_full_2026_09_26", "adopted_2026_09_26")` |
| uncertainty | `later_cases.json`, read by `sept24_specs.cjs` and `propagate.py` | `"main_case_schools_full_2026_09_26"` |
| debt legacy | `debt_legacy.py` `LATER_CASES` | `("main_case_schools_full_2026_09_26", "main case adopted 2026-09-26, schools at full average cost")` |
| old → new | `old_new_lanes.py` reads the back-cast's `LATER_CASES` | `--case` defaults to the last entry, `--middle` to `sept26` |

Responses come from each case's `corrections.json` `meta.responses`: schools 1.0000/1.0000 and general
government 0.6000/0.8504. Every lane that reads them stops if they differ from that lane's `summary.json`;
the back-cast reads only the engine's bands. The strings
0.63/0.66 now appear only in labels and docstrings. The distribution lane records the responses but does not
compute with them: the band change moves A.

## Gates

| Lane | Earlier cases, byte for byte | New-case gates (all pass) | Tests |
|---|---|---|---|
| back-cast | `sept26` = f5b4aae, `sept24` = da2b107 (both derived files) | The lane's `adopted_2026_09_26` variant equals the back-cast's `_sept26_` 2024 anchors (1e-9). The band equals `summary.json` 258.4885–291.9548 (1e-4). Receipts at the base variant equal the `_sept26_` receipts. No concept tag contains another. | 3 |
| distribution | `sept26` = f697514 (13 files), `sept24` = 6e554a3 (13), `sept23` = 5b8957e (12) | 224 gates. The base is the Sept 26 band (1e-4 bands, 1e-9 summary). The change equals the schools `summary.json` `change` +57.5705/+46.2599 (1e-12). The band is rebuilt from A (1e-3). | 4 |
| uncertainty | `derived/sept24/` and `derived/sept26/` are unchanged in place | Payload responses equal `summary.json`'s. They replace Sept 24's one for one per `package.cjs` `MAIN_SPECS`. The 64 specifications span the uncorrected 265.5903–298.6797 and the adopted 258.4885–291.9548. | 12 |
| debt legacy | `sept26` = e62fccb (13 files), `sept24` = ed1b623 (12), `sept23` = 96a5c3b (10) | Payload responses equal `summary.json`'s, and lines and edits equal Sept 26's. The corners reproduce the full band 258.4885/291.9548, non-school-fixed 204.7765/265.8072 and proportional 301.2853/334.7516. Bridge: at matched specifications only education lines move (1e-9). The gap move equals the change plus ΔP (1e-6), and the steps add (1e-9). The programme control's largest difference is $0.00005bn. | 4 |
| old → new | none | The rebuilt default of distribution and debt legacy equals the working tree. | 2 runs identical |

Determinism: a full rerun of all four lanes, with the defaults to scratch and the uncertainty lane in place,
leaves the 59 working-tree derived files unchanged. Each default rebuild test compares against the working
tree.

## Findings for the lead

1. **The school step is not all state and local.** Taken at Sept 26's end specifications (56/7), it adds
   $58.36/45.44bn to the gap. Its federal part is $4.79/3.73bn under the central convention (8.2%),
   $0.57/0.45bn under the low convention (1.0%) and $7.53/5.86bn under the high one (12.9%). The central
   convention spreads federal education grants pro rata over state-local education consumption, the low
   one keeps federal consumption only, and the high one uses the high federal K-12 share for the school
   part (`debt_legacy.py` `federal_shares`). The claim holds under the low convention only. File:
   `debt_legacy_2026_09_23/derived/sept26_schools_bridge_2024.csv`.
2. **The bridge from Sept 26 is ordered.** The matched-specification step is followed by a single "range
   ends move" of −$0.79/+0.81bn as the ends shift to 48/11. The step equals the schools lane's
   `unfunded_by_rule.one_year` (f1e4f5b) and W2's union (0f22f0c) to the digits shown. At the schools
   corners, the per-specification school line is $138.7/172.5bn, the value f1e4f5b now publishes.
3. **The corners change but the allocation does not.** The low end keeps the shared allocation and gdp
   normalization, with school share 0.715 (Sept 26: 0.865). The high end keeps the personal allocation and
   cash normalization, with school share 0.865 (was 0.715). Because the allocation at each end is
   unchanged, the distribution rule that the band-end change moves A still applies.

## Files changed (uncommitted, none staged)

| Lane | Code | Derived |
|---|---|---|
| `historical_backcast_2026_09_20/` | `backcast.py`, `README.md` (case paragraph), `test_backcast.py` **new** | `backcast_annual.csv` and `backcast_windows.csv` gain the `_schools_full_` family; earlier columns are unchanged |
| `distribution_weights_2026_09_23/` | `distribute.py`, `test_distribute.py` | `channel_by_decile.csv`, `channel_by_percentile.csv`, `channel_by_quintile.csv`, `gates.json`, `inputs.json`, `ranges_weighted.csv`, `regressivity.csv`, `weighted_totals.csv` |
| `uncertainty_propagation_2026_09_22/` | `propagate.py`, `sept24_specs.cjs`, `test_uncertainty.py`, `later_cases.json` **new** | `sept26_schools/` **new**: `case_uncertainty.csv`, `line_targets.csv`, `spec_costs.csv`, `summary.json` |
| `debt_legacy_2026_09_23/` | `debt_legacy.py`, `test_debt_legacy.py` | `adopted_backcast_windows.csv`, `corrections_federal_by_component_2024.csv`, `corrections_federal_split_2024.csv`, `federal_gap_annual.csv`, `federal_split_2024.csv`, `federal_split_2024_lines.csv`, `forward_path.csv`, `stocks.csv`, `summary.json`; `sept26_schools_bridge_2024.csv` **new** (`sept26_bridge_2024.csv` unchanged) |
| `sept26_propagation_2026_09_26/` | `old_new_lanes.py` **new** | `derived/old_new_lanes.csv` **new**; this file |

The new files need a `git add` before a pathspec commit. W4 edited `band_variants.*`, `real_costs_totals.*`
and `sept26/` in `sept26_propagation_2026_09_26/derived/`, along with its own lanes; none of those is mine.

## Consumers outside these directories

| Consumer | Reads | Effect |
|---|---|---|
| `figures_2026_09_22` | distribution and back-cast at 6e554a3 and da2b107 via `git show` (fef4d12) | none |
| `winners_losers_2026_09_24` (W4) | distribution and debt legacy at pinned commits; debt `--case sept23` | none; the pins and `sept23` rebuild byte for byte |
| `sept24_propagation_2026_09_24/constant_choices.py` (W4) | the debt legacy lane | W4's |
| `cps_imputation_keys_2026_09_23/distribution_check.py` | a `--case sept23` rebuild; stops on any other case | none |
| `school_capital_return_2026_09_26/capital_return.py` (untracked, not mine) | the debt legacy lane's `RESULT.md` text | none; unchanged |

Left for the lead: the `RESULT.md` verdict brackets in distribution, uncertainty and debt legacy still name
Sept 24 as the default. I did not bracket them because the brief limits prose to this file.

## Reproduce (repository root)

```sh
export OPENBLAS_NUM_THREADS=1
uv run --no-project python3 infra/immigration-fiscal/historical_backcast_2026_09_20/backcast.py
uv run --no-project python3 infra/immigration-fiscal/distribution_weights_2026_09_23/distribute.py
node infra/immigration-fiscal/uncertainty_propagation_2026_09_22/sept24_specs.cjs
uv run --no-project python3 infra/immigration-fiscal/uncertainty_propagation_2026_09_22/propagate.py
uv run --no-project python3 infra/immigration-fiscal/debt_legacy_2026_09_23/debt_legacy.py
uv run --no-project python3 infra/immigration-fiscal/sept26_propagation_2026_09_26/old_new_lanes.py
uv run --no-project python3 -m pytest infra/immigration-fiscal/historical_backcast_2026_09_20/test_backcast.py \
  infra/immigration-fiscal/distribution_weights_2026_09_23/ infra/immigration-fiscal/uncertainty_propagation_2026_09_22/ \
  infra/immigration-fiscal/debt_legacy_2026_09_23/ -q --import-mode=importlib
```

Pass `--case sept26` or `--case sept24` to any lane, or `--case sept23` to distribution and debt legacy, with
`--out-dir DIR` to rebuild an earlier case. The uncertainty lane writes `derived/<case>/` for every case.

## Old → new

The table below is `old_new_lanes.py` output (`derived/old_new_lanes.csv`, 94 rows), pasted unedited. The
Sept 24 column is e5e23ec. A range reads low end to high end, and costs in the distribution rows are
negative.

**main case (reference)**

| Quantity | Unit | Sept 24 | Sept 26, CBO's one-year school response (0.63–0.66) | Sept 26, schools at full cost | File |
|---|---|---:|---:|---:|---|
| fiscal main case | $bn | 200.9 to 246.3 | 200.9 to 245.7 | 258.5 to 292.0 | `<case lane>/derived/summary.json` |
| group receipts, reference incidence rule (shared allocation) | $bn | 488.5 | 492.5 | 492.5 | `<case lane>/derived/summary.json` |

**back-cast (ladder 162, 219)**

| Quantity | Unit | Sept 24 | Sept 26, CBO's one-year school response (0.63–0.66) | Sept 26, schools at full cost | File |
|---|---|---:|---:|---:|---|
| main case, whole-budget rules, 2015-2024 | $tn | 1.73 to 2.43 | 1.73 to 2.43 | 2.24 to 2.84 | `historical_backcast_2026_09_20/derived/backcast_windows.csv` |
| main case, whole-budget rules, 2010-2024 | $tn | 2.49 to 3.64 | 2.49 to 3.63 | 3.21 to 4.21 | `historical_backcast_2026_09_20/derived/backcast_windows.csv` |
| main case, whole-budget rules, 2005-2024 | $tn | 2.98 to 4.48 | 2.98 to 4.48 | 3.86 to 5.19 | `historical_backcast_2026_09_20/derived/backcast_windows.csv` |
| main case, flat rule, 2015-2024 | $tn | 1.92 to 2.35 | 1.92 to 2.34 | 2.46 to 2.78 | `historical_backcast_2026_09_20/derived/backcast_windows.csv` |
| main case, ratio rule, 2015-2024 | $tn | 1.73 to 2.14 | 1.73 to 2.13 | 2.24 to 2.54 | `historical_backcast_2026_09_20/derived/backcast_windows.csv` |
| main case, income rule, 2015-2024 | $tn | 2.03 to 2.43 | 2.03 to 2.43 | 2.54 to 2.84 | `historical_backcast_2026_09_20/derived/backcast_windows.csv` |
| proportional benchmark, whole-budget rules, 2015-2024 | $tn | 2.64 to 3.23 | 2.62 to 3.22 | 2.62 to 3.22 | `historical_backcast_2026_09_20/derived/backcast_windows.csv` |
| proportional benchmark, whole-budget rules, 2010-2024 | $tn | 3.76 to 4.76 | 3.74 to 4.75 | 3.74 to 4.75 | `historical_backcast_2026_09_20/derived/backcast_windows.csv` |
| proportional benchmark, whole-budget rules, 2005-2024 | $tn | 4.54 to 5.94 | 4.52 to 5.91 | 4.52 to 5.91 | `historical_backcast_2026_09_20/derived/backcast_windows.csv` |
| proportional benchmark, flat rule, 2015-2024 | $tn | 2.89 to 3.21 | 2.87 to 3.19 | 2.87 to 3.19 | `historical_backcast_2026_09_20/derived/backcast_windows.csv` |
| proportional benchmark, ratio rule, 2015-2024 | $tn | 2.64 to 2.94 | 2.62 to 2.92 | 2.62 to 2.92 | `historical_backcast_2026_09_20/derived/backcast_windows.csv` |
| proportional benchmark, income rule, 2015-2024 | $tn | 2.93 to 3.23 | 2.92 to 3.22 | 2.92 to 3.22 | `historical_backcast_2026_09_20/derived/backcast_windows.csv` |

**debt legacy (ladder 207)**

| Quantity | Unit | Sept 24 | Sept 26, CBO's one-year school response (0.63–0.66) | Sept 26, schools at full cost | File |
|---|---|---:|---:|---:|---|
| federal part of the 2024 fiscal gap, central convention | $bn | 32.0 to 51.9 | 31.8 to 51.6 | 36.5 to 55.4 | `debt_legacy_2026_09_23/derived/federal_split_2024.csv` |
| 2024 fiscal gap (cost + P) | $bn | 200.6 to 246.2 | 200.7 to 245.5 | 258.3 to 291.8 | `debt_legacy_2026_09_23/derived/federal_split_2024.csv` |
| federal share of the 2024 gap, central convention | % | 15.9 to 21.1 | 15.8 to 21.0 | 14.1 to 19.0 | `debt_legacy_2026_09_23/derived/federal_split_2024.csv` |
| federal share of the 2024 gap, low convention | % | 5.08 to 11.97 | 4.84 to 11.83 | 3.98 to 10.11 | `debt_legacy_2026_09_23/derived/federal_split_2024.csv` |
| federal share of the 2024 gap, high convention | % | 21.2 to 27.0 | 21.2 to 27.1 | 18.9 to 25.3 | `debt_legacy_2026_09_23/derived/federal_split_2024.csv` |
| legacy stock entering 2024 (central rule) | $bn | 876.5 to 1,126.8 | 873.7 to 1,124.3 | 932.4 to 1,171.4 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| stock, share of debt at end FY2023 (central rule) | % | 3.34 to 4.29 | 3.33 to 4.29 | 3.55 to 4.46 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| legacy interest, 2024 (central rule) | $bn | 28.3 to 36.4 | 28.2 to 36.3 | 30.1 to 37.9 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| interest per group member (central rule) | $ | 693 to 891 | 691 to 889 | 737 to 926 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| interest per other resident (central rule) | $ | 95 to 122 | 94 to 121 | 101 to 127 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| interest, share of FY2024 net interest (central rule) | % | 3.22 to 4.14 | 3.21 to 4.13 | 3.43 to 4.30 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| interest over the account's interest row allocation (central rule) | ratio | 0.22 to 0.28 | 0.22 to 0.28 | 0.23 to 0.29 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| the brief's D, stock at the end of FY2024 (central rule) | $bn | 904.9 to 1,163.2 | 902.0 to 1,160.6 | 962.5 to 1,209.3 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| nominal sum of the 2005-2023 federal gaps (central rule) | $bn | 768.7 to 981.1 | 766.2 to 978.9 | 816.0 to 1,018.9 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| the 2024 gap's own part-year interest (central rule) | $bn | 0.52 to 0.84 | 0.51 to 0.83 | 0.59 to 0.90 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| legacy interest across back-cast rules, central convention | $bn | 6.28 to 37.25 | 6.15 to 37.17 | 8.03 to 38.69 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| legacy stock across back-cast rules, central convention | $tn | 0.19 to 1.15 | 0.19 to 1.15 | 0.25 to 1.20 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| legacy interest across rules and payer conventions | $bn | -3.15 to 42.88 | -3.38 to 42.87 | -3.11 to 45.64 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| legacy interest, every specification | $bn | -4.28 to 57.54 | -4.59 to 57.53 | -4.24 to 61.24 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| legacy interest, central rule, every specification | $bn | 5.98 to 56.45 | 5.92 to 56.44 | 5.98 to 60.15 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| legacy interest, low payer convention | $bn | 18.8 to 26.7 | 18.6 to 26.5 | 18.9 to 26.8 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| legacy interest, high payer convention | $bn | 32.4 to 42.1 | 32.4 to 42.1 | 34.7 to 44.8 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| legacy interest, constant 3.22% rate | $bn | 30.6 to 39.4 | 30.5 to 39.3 | 32.6 to 41.0 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| legacy interest, 10-year Treasury rate | $bn | 38.0 to 48.9 | 37.9 to 48.8 | 40.5 to 50.8 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| legacy interest, public securities rate | $bn | 31.1 to 40.1 | 31.0 to 40.0 | 33.1 to 41.6 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| legacy interest, window from 2010 | $bn | 25.8 to 32.1 | 25.7 to 32.0 | 27.2 to 33.2 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| legacy interest, window from 2015 | $bn | 16.8 to 21.2 | 16.7 to 21.1 | 17.7 to 21.9 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| legacy interest, half borrowed | $bn | 14.2 to 18.2 | 14.1 to 18.2 | 15.1 to 18.9 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| legacy interest, proportional benchmark | $bn | 38.5 to 46.2 | 38.8 to 46.5 | 38.8 to 46.5 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| omitted benefits mobility: federal 2024 | $bn | 0.0252 | 0.0252 | 0.0252 | `debt_legacy_2026_09_23/derived/benefit_sensitivity.csv` |
| omitted benefits mobility: stock reduction | $bn | 0.39 | 0.39 | 0.39 | `debt_legacy_2026_09_23/derived/benefit_sensitivity.csv` |
| omitted benefits mobility: interest reduction 2024 | $bn | 0.0126 | 0.0126 | 0.0126 | `debt_legacy_2026_09_23/derived/benefit_sensitivity.csv` |
| omitted benefits mobility_and_scale: federal 2024 | $bn | 5.29 | 5.29 | 5.29 | `debt_legacy_2026_09_23/derived/benefit_sensitivity.csv` |
| omitted benefits mobility_and_scale: stock reduction | $bn | 82.3 | 82.3 | 82.3 | `debt_legacy_2026_09_23/derived/benefit_sensitivity.csv` |
| omitted benefits mobility_and_scale: interest reduction 2024 | $bn | 2.66 | 2.66 | 2.66 | `debt_legacy_2026_09_23/derived/benefit_sensitivity.csv` |
| forward federal debt from the 2024 gap, 10 years | $bn | 370.4 to 600.6 | 367.8 to 598.1 | 422.6 to 642.1 | `debt_legacy_2026_09_23/derived/forward_path.csv` |
| forward federal debt from the 2024 gap, 20 years | $bn | 878.9 to 1,425.2 | 872.9 to 1,419.3 | 1,003 to 1,524 | `debt_legacy_2026_09_23/derived/forward_path.csv` |
| forward federal debt from the 2024 gap, 30 years | $bn | 1,577 to 2,557 | 1,566 to 2,547 | 1,799 to 2,734 | `debt_legacy_2026_09_23/derived/forward_path.csv` |
| forward debt if the whole gap were borrowed, 10 years | $tn | 2.32 to 2.85 | 2.32 to 2.84 | 2.99 to 3.38 | `debt_legacy_2026_09_23/derived/forward_path.csv` |
| back-cast net cost, programme, 2015-2024 | $tn | 1.95 to 2.33 | 1.95 to 2.33 | 2.47 to 2.75 | `debt_legacy_2026_09_23/derived/adopted_backcast_windows.csv` |
| back-cast net cost, programme, 2010-2024 | $tn | 2.75 to 3.30 | 2.75 to 3.30 | 3.50 to 3.89 | `debt_legacy_2026_09_23/derived/adopted_backcast_windows.csv` |
| back-cast net cost, programme, 2005-2024 | $tn | 3.27 to 3.97 | 3.27 to 3.96 | 4.21 to 4.72 | `debt_legacy_2026_09_23/derived/adopted_backcast_windows.csv` |
| back-cast net cost, programme_income, 2015-2024 | $tn | 2.19 to 2.56 | 2.19 to 2.56 | 2.71 to 2.97 | `debt_legacy_2026_09_23/derived/adopted_backcast_windows.csv` |
| back-cast net cost, programme_income, 2010-2024 | $tn | 3.21 to 3.74 | 3.22 to 3.74 | 3.96 to 4.34 | `debt_legacy_2026_09_23/derived/adopted_backcast_windows.csv` |
| back-cast net cost, programme_income, 2005-2024 | $tn | 3.92 to 4.58 | 3.93 to 4.58 | 4.86 to 5.33 | `debt_legacy_2026_09_23/derived/adopted_backcast_windows.csv` |
| per-correction federal part, tax_stack, central convention | $bn | 16.0 to 17.2 | 16.0 to 17.2 | 16.0 to 17.2 | `debt_legacy_2026_09_23/derived/corrections_federal_by_component_2024.csv` |
| per-correction federal part, medical_ethnicity_and_ltss, central convention | $bn | -15.24 to -15.23 | -15.24 to -15.23 | -15.24 to -15.23 | `debt_legacy_2026_09_23/derived/corrections_federal_by_component_2024.csv` |
| per-correction federal part, audit_row1_premium_credits, central convention | $bn | -14.2 to -14.2 | -14.2 to -14.2 | -14.2 to -14.2 | `debt_legacy_2026_09_23/derived/corrections_federal_by_component_2024.csv` |
| per-correction federal part, education_row6_and_school_price, central convention | $bn | 0.0580 to -0.0437 | 0.0612 to -0.0420 | 0.0480 to 0.0499 | `debt_legacy_2026_09_23/derived/corrections_federal_by_component_2024.csv` |
| per-correction federal part, lane_constants, central convention | $bn | -5.11 to -5.14 | -5.11 to -5.14 | -5.11 to -5.14 | `debt_legacy_2026_09_23/derived/corrections_federal_by_component_2024.csv` |
| per-correction federal part, finite_removal, central convention | $bn | — | -0.0015 to -0.0015 | -0.0015 to -0.0015 | `debt_legacy_2026_09_23/derived/corrections_federal_by_component_2024.csv` |
| per-correction federal part, consumption_key, central convention | $bn | — | -0.58 to -0.58 | -0.58 to -0.58 | `debt_legacy_2026_09_23/derived/corrections_federal_by_component_2024.csv` |
| federal part of the school-response step at matched specifications, central convention | $bn | — | — | 4.79 to 3.73 | `debt_legacy_2026_09_23/derived/<case>_bridge_2024.csv` |
| federal part of the school-response step at matched specifications, low convention | $bn | — | — | 0.57 to 0.45 | `debt_legacy_2026_09_23/derived/<case>_bridge_2024.csv` |
| federal part of the school-response step at matched specifications, high convention | $bn | — | — | 7.53 to 5.86 | `debt_legacy_2026_09_23/derived/<case>_bridge_2024.csv` |

**distribution (ladder 194)**

| Quantity | Unit | Sept 24 | Sept 26, CBO's one-year school response (0.63–0.66) | Sept 26, schools at full cost | File |
|---|---|---:|---:|---:|---|
| fiscal cost channel, A_mid + F_c (negative = cost) | $bn | -225.1 | -224.8 | -276.7 | `distribution_weights_2026_09_23/derived/channel_by_quintile.csv` |
| fiscal cost, tax-share financing, fifth 1 | $bn | -6.83 | -6.82 | -8.39 | `distribution_weights_2026_09_23/derived/channel_by_quintile.csv` |
| fiscal cost, tax-share financing, fifth 2 | $bn | -14.4 | -14.4 | -17.7 | `distribution_weights_2026_09_23/derived/channel_by_quintile.csv` |
| fiscal cost, tax-share financing, fifth 3 | $bn | -24.3 | -24.2 | -29.8 | `distribution_weights_2026_09_23/derived/channel_by_quintile.csv` |
| fiscal cost, tax-share financing, fifth 4 | $bn | -39.8 | -39.7 | -48.9 | `distribution_weights_2026_09_23/derived/channel_by_quintile.csv` |
| fiscal cost, tax-share financing, fifth 5 | $bn | -139.8 | -139.6 | -171.9 | `distribution_weights_2026_09_23/derived/channel_by_quintile.csv` |
| fiscal cost, per-person cuts, each fifth | $bn | -45.0 | -45.0 | -55.3 | `distribution_weights_2026_09_23/derived/channel_by_quintile.csv` |
| fiscal cost, top fifth's part under tax-share financing | % | 62.1 | 62.1 | 62.1 | `distribution_weights_2026_09_23/derived/channel_by_quintile.csv` |
| fiscal cost under per-person cuts, share of resources, bottom and top fifth | % | -7.93 to -0.84 | -7.92 to -0.84 | -9.75 to -1.03 | `distribution_weights_2026_09_23/derived/channel_by_quintile.csv` |
| central total with the social items (TOTAL) | $bn | -259.8 | -259.5 | -311.4 | `distribution_weights_2026_09_23/derived/channel_by_quintile.csv` |
| central total, share of resources, bottom and top fifth, tax-share | % | -5.23 to -1.75 | -5.23 to -1.74 | -5.50 to -2.35 | `distribution_weights_2026_09_23/derived/channel_by_quintile.csv` |
| central total, share of resources, bottom and top fifth, per-person | % | -12.0 to 0.0 | -11.9 to 0.0 | -13.8 to -0.2 | `distribution_weights_2026_09_23/derived/channel_by_quintile.csv` |
| central total at eta 1.3, equal-split equivalent, tax-share | $bn | -180.9 | -180.8 | -199.0 | `distribution_weights_2026_09_23/derived/weighted_totals.csv` |
| central total at eta 1.3, mean-normalized, tax-share | $bn | -404.9 | -404.7 | -445.4 | `distribution_weights_2026_09_23/derived/weighted_totals.csv` |
| central total at eta 1.3, equal-split equivalent, per-person | $bn | -327.1 | -326.8 | -378.7 | `distribution_weights_2026_09_23/derived/weighted_totals.csv` |
| central total at eta 1.3, mean-normalized, per-person | $bn | -732.0 | -731.3 | -847.5 | `distribution_weights_2026_09_23/derived/weighted_totals.csv` |
| outside the budget: bottom four fifths, top fifth | $bn | -80.7 to 46.0 | -80.7 to 46.0 | -80.7 to 46.0 | `distribution_weights_2026_09_23/derived/channel_by_quintile.csv` |
| direct fiscal response A at the band ends (negative = cost) | $bn | -214.2 to -255.1 | -214.2 to -254.5 | -271.8 to -300.7 | `distribution_weights_2026_09_23/derived/inputs.json` |

**uncertainty (ladder 184)**

| Quantity | Unit | Sept 24 | Sept 26, CBO's one-year school response (0.63–0.66) | Sept 26, schools at full cost | File |
|---|---|---:|---:|---:|---|
| per-case SE, sources independent | $bn | 10.8 to 10.9 | 10.8 to 11.0 | 10.9 to 11.0 | `uncertainty_propagation_2026_09_22/derived/<case>/summary.json` |
| per-case SE, all positively correlated | $bn | 17.2 to 17.8 | 17.3 to 17.8 | 18.0 to 18.4 | `uncertainty_propagation_2026_09_22/derived/<case>/summary.json` |
| per-case SE, CPS keys only | $bn | 8.93 to 9.03 | 8.95 to 9.06 | 8.95 to 9.06 | `uncertainty_propagation_2026_09_22/derived/<case>/summary.json` |
| 95% intervals of the main band's cases, union | $bn | 179.5 to 267.6 | 179.5 to 267.0 | 236.9 to 313.4 | `uncertainty_propagation_2026_09_22/derived/<case>/summary.json` |
| 95% intervals at the correlated upper bound, union | $bn | 166.4 to 280.4 | 166.3 to 279.9 | 222.5 to 327.2 | `uncertainty_propagation_2026_09_22/derived/<case>/summary.json` |
| 95% intervals with the benefit keys' SE, union | $bn | 179.4 to 267.7 | 179.4 to 267.1 | 236.8 to 313.5 | `uncertainty_propagation_2026_09_22/derived/<case>/summary.json` |
| per-case SE, uncorrected model at the adopted responses (control) | $bn | — | 12.2 to 12.3 | 12.27 to 12.34 | `uncertainty_propagation_2026_09_22/derived/<case>/summary.json` |

## Parent integration (2026-09-27, 00:15)

The parent reran every lane on every case: each older case matches its commit byte for byte, two
default runs are byte-identical and equal the working tree, and 23 tests pass (3/4/12/4).
`old_new_lanes.py` reproduces `derived/old_new_lanes.csv`. The lane verdict brackets that still
named September 24 as the default now carry the schools-case figures, added by the parent.

| Lane | Sept 26 commit | Schools-case commit |
|---|---|---|
| Back-cast | f5b4aae | c0297e4 |
| Distribution | f697514 | 39b854b |
| Uncertainty | 1d14940, ca18777 | eab844f |
| Debt legacy | e62fccb | 1db19c8 |

The parent's premise that the school step is almost all state and local was wrong: it is 8.2%
federal under the debt lane's central convention.
