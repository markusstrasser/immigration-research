# School capital where the group enrolls (2026-10-24)

This lane builds a district perpetual inventory of K-12 capital from Census F-33 FY1992–FY2024. It measures capital per pupil where the Mexican-origin group's pupils enroll, relative to the nation. The relative is applied as a factor to the oct16 case's K-12 capital charge, which is the return at 2.081% plus depreciation. The result sits beside the case and is not adopted. Findings are in [RESULT.md](RESULT.md) and the brief in [BRIEF.md](BRIEF.md).

## Files

- `acquire.py` downloads the F-33 all-items district files FY1992–FY1999 from www2.census.gov into `_cache/f33_pre2000/` (about 110 MB, ignored). FY1999's xls is converted to CSV. It writes `derived/sources_pre2000.json` with the URL, bytes, SHA-256 and rows for each file. An existing file is hashed, not refetched.
- `build.py` runs the inventory, weights, ratios and dollars, and writes `derived/`. It runs `case_base.cjs`. It reads FY2000–2024 from `school_dilution_2026_09_24/_cache/f33`, plus the following:
  - BEA tables and K-12 keys from `school_capital_return_2026_09_26`;
  - weights from `school_cost_where_enrolled_2026_09_24/weighting.py`.
- `case_base.cjs` reads the adopted oct16 package (read-only) and writes `derived/case_base.json`: the K-12 capital return at the one rate by population part, at both end specifications, with gates.
- `test_lane.py` holds the gates and a raw-file hand check of Los Angeles Unified's structures stock.

## Outputs (`derived/`)

| File | Contents |
|---|---|
| `summary.json` | Rates, π, calibration, chain coverage, survey-year coverage, R_K by concept, arm order, case base, headline (key-consistent A) and literal (C) deltas, FY2000-start sensitivity, land floor, input hashes |
| `dollars.csv` | Δ$bn low/high by start year, pre-start arm, variant (primary, realloc, bea_level, fy2000_start), weighting and factor family |
| `r_k_by_concept.csv` | R for every stock concept × weighting × family (C district, state-weighted, A account state mix, A state mix only, B CCD state mix); `s2000_` concepts are the FY2000 start |
| `state_breakdown.csv` | Per state: account pupils and price, structures per pupil (all pupils and group, arms a and b), within-state factor |
| `national_flows.csv` | Per fiscal year: units, nominal and real flows, depreciated stock, prices, chained shares |
| `top_group_districts.csv` | The 40 districts with the most group pupils: measured and pre-1992 stock, per-pupil stock by arm |
| `gates.csv` | Build gates (24) |
| `case_base.json` | The case's K-12 capital base amounts |
| `sources_pre2000.json` | Download provenance for FY1992–1999 |

## Reproduce

```sh
# from the repository root
uv run --no-project --with xlrd python3 infra/immigration-fiscal/school_capital_where_enrolled_2026_10_24/acquire.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/school_capital_where_enrolled_2026_10_24/build.py
uv run --no-project python3 -m pytest infra/immigration-fiscal/school_capital_where_enrolled_2026_10_24/test_lane.py -q
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/school_capital_where_enrolled_2026_10_24 \
  "uv run --no-project --with xlrd python3 {lane}/acquire.py" \
  "uv run --no-project python3 {lane}/build.py" \
  "uv run --no-project python3 -m pytest {lane}/test_lane.py -q"
```

The build takes about 30 s. It needs the sibling lanes' `_cache` directories: `school_dilution_2026_09_24` (F-33 FY2000–2024 and CPI) and `school_capital_return_2026_09_26` (BEA fixed assets). It also needs CCD and ACS inputs, which `weighting.py` reads.
