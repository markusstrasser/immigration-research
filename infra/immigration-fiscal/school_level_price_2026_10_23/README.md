# School-level price of the group's pupils

One question: when the case prices each group pupil at its state's average spending per pupil,
how much should the price rise because the pupil sits in a particular district and school?

The sibling lane `school_cost_where_enrolled_2026_09_24` priced the **state** and proposed a
**district** correction k = 1.034. This lane goes to the **school**: CCD membership by
race/ethnicity (2021–22) merged to SLFS FY2022 school-level current expenditures.

## Inputs

Both files are already in `../school_cost_where_enrolled_2026_09_24/_cache/`:

- `ccd_SCH_052_2122_l_1a_071722_CSV.zip` — CCD school membership by race/ethnicity.
- `slfs22_data_2025047_4_0_1.zip` — SLFS FY2022 school-level finance (`slfs22_1a.txt`).

Unzip them into this lane's ignored `_cache/`:

```sh
cd infra/immigration-fiscal/school_level_price_2026_10_23/_cache
unzip -o ../../school_cost_where_enrolled_2026_09_24/_cache/ccd_SCH_052_2122_l_1a_071722_CSV.zip
unzip -o ../../school_cost_where_enrolled_2026_09_24/_cache/slfs22_data_2025047_4_0_1.zip slfs22_1a.txt
```

## Build and test

```sh
uv run --no-project python3 infra/immigration-fiscal/school_level_price_2026_10_23/build.py
uv run --no-project python3 -m pytest infra/immigration-fiscal/school_level_price_2026_10_23/ -q
```

`build.py` uses DuckDB for the 2.2 GB CCD file; it runs in seconds.

## Outputs

`derived/`:

- `state_k.csv` — Hispanic- and white-weighted price vs state average, by state.
- `district_k.csv` — within-district price gap, by district (≥5 schools, ≥100 Hispanic pupils).
- `summary.json` — national readings, the decomposition and the checks.

`_cache/` (ignored) holds the three intermediate tables: `ccd_school_2122.csv`,
`slfs_school_2122.csv` and `school_merge.csv`.

## What it says

The group's pupils attend schools that spend **5.9% more than the national average** and **12.4% more
than the schools white pupils attend**, but the within-district gap is **0.1%**. The gap is between
districts and states. The within-state correction is **1.027**, against the proposed district
k = 1.034; the national 1.059 is mostly the state mix the case already prices. See `RESULT.md`.

## Limits

CCD reports Hispanic, not Mexican origin. SLFS is a sample, not the universe. FY2022 current
expenditures carry COVID relief and exclude capital; the sibling lane's ASSF FY2024 measure gives
different levels, so compare ratios within a measure, not levels across them.
