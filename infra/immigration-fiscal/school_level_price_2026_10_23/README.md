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
uv run --no-project python3 infra/immigration-fiscal/school_level_price_2026_10_23/state_elasticity.py
uv run --no-project python3 -m pytest infra/immigration-fiscal/school_level_price_2026_10_23/ -q
```

`build.py` uses DuckDB for the 2.2 GB CCD file; it runs in seconds.

## Outputs

`derived/`:

- `state_k.csv` — Hispanic- and white-weighted price vs state average, by state.
- `district_k.csv` — within-district price gap, by district (≥5 schools, ≥100 Hispanic pupils).
- `summary.json` — national readings, the decomposition and the checks.
- `state_elasticity.csv` — within-district spending elasticity by state (district FE, pupil weighted).
- `state_elasticity_summary.json` — national pooled and Hispanic-weighted state averages.

`_cache/` (ignored) holds the three intermediate tables: `ccd_school_2122.csv`,
`slfs_school_2122.csv` and `school_merge.csv`.

## What it says

The group's pupils attend schools that spend **5.9% more than the national average** and **12.4% more
than the schools white pupils attend** in the SLFS measure, but that is mostly composition. The
group-weighted **within-district** factor is **1.005** (1.037 excluding single-school districts and
NYC), not zero; the unweighted median 1.001 was misleading because 4,531 of 15,949 districts are
single-school. The within-state correction is **1.027**, against the proposed 1.034. The state-level
0.75–0.92 is a **cross-school size gradient, not the response**; the 0.836 panel response remains the
case's. The shares are Hispanic, not Mexican-origin: 52.7% of Texas pupils, 56.1% of California's,
74.1% of LAUSD's; the Mexican-origin under-30 share in Texas is 38.0%, a plurality, not a majority.
See `RESULT.md`.

## Limits

CCD reports Hispanic, not Mexican origin. SLFS is a sample, not the universe. FY2022 current
expenditures carry COVID relief and exclude capital; the sibling lane's ASSF FY2024 measure gives
different levels, so compare ratios within a measure, not levels across them.
