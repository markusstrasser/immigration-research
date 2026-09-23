# Lane: does local general government grow with population? (2026-09-23)

A county instrumental-variables test of the general-government response the main case adopted on
2026-09-23 (0.59–0.84, from `assumption_explorer_2026_09_21/scaling_check.py`). The brief is
`BRIEF.md`; the findings are in `RESULT.md`.

Outcome: real current operations of every local government in a county area on financial
administration (Census item E23), central staff (E29) and general public buildings (E31). Variants
add judicial and legal (E25) and use direct expenditure (E, F, G, J). Regressor: log change in
July-1 population. Instruments: an industry-mix employment shock (County Business Patterns) and an
immigrant settlement shift-share (2000 Census country-of-birth shares).

## Inputs

| Input | Where | Notes |
|---|---|---|
| Census individual-unit finance files 2012, 2017, 2022 | `../local_spending_composition_2026_09_18/_cache/indunit_<y>.zip` | read-only; the 2022 file is the July 2026 re-release |
| Government Finance Database (1967–2024) | `sources/.../government_finance_database/gfd_entire.zip` | 2.9 GB Deflate64 CSV streamed through `unzip -p`, never extracted |
| County Business Patterns 2012, 2017, 2022 | `sources/.../cbp_county/cbp{12,17,22}co.txt` | copied from the corpus by the lead |
| County Business Patterns 2007 | `_cache/cbp/cbp07co.zip` | census.gov |
| County population | `_cache/pep/co-est00int-tot.csv`, `_cache/pep/cc-est2020int-agesex-all.csv`, `sources/.../census_county_pop/cc-est2023-alldata.csv` | intercensal 2000–2010 and 2010–2020, vintage 2023 |
| Country of birth | `_cache/api/` | 2000 SF3 PCT019; ACS 5-year B05006 for 2009, 2014, 2019, 2024 |
| CPI-U | `../local_spending_composition_2026_09_18/_cache/cpi.json`, `_cache/cpi_extra.json` (1997, BLS API) | annual averages |
| Median household income | `../local_spending_composition_2026_09_18/derived/county_shares.csv` | ACS 5-year |

## Run

From the repository root. The main checkout's `.venv` (numpy, pandas, openpyxl) is enough; no
`--with` wheels are needed. `node` runs the evaluator.

```bash
set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a   # CENSUS_API_KEY, never printed
L=infra/immigration-fiscal/gg_response_county_iv_2026_09_23
r() { OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 uv run --no-project python3 "$@"; }
r $L/fetch.py 2>&1 | sed -E 's/key=[A-Za-z0-9]+/key=<KEY>/g'   # cached after the first run
r $L/gfd_stream.py           # ~1 min: county sums of the database's administration columns
r $L/gates.py                # gates 1-3 of the brief
node $L/main_case_map.js     # gate 4 (runs main_case.js with writes intercepted); maps once estimates exist
r $L/build_panel.py          # ~25 s
r $L/estimate.py             # ~10 s, 780 estimates
r $L/verify.py               # independent full-matrix recomputation of the key estimates
node $L/main_case_map.js     # gates again, then the main-case map
```

## Scripts

| File | What it does |
|---|---|
| `fetch.py` | curl downloads into `_cache/`: population estimates, CBP 2007, Census API tables, BLS CPI 1997 |
| `gfd_stream.py` | streams the database CSV, sums local units to counties for census years 1992–2022 |
| `finance.py` | individual-unit parser (E and direct items for 23, 25, 29, 31) and unit directory, reusing the composition lane's layouts |
| `gates.py` | reproduces 0.59/0.84, the administration lane's 0.47, the composition lane's county totals, and the database against the Census files |
| `no_write_hook.js` | preload that stops another lane's script writing and compares what it would write with its files on disk |
| `main_case_map.js` | gate on `main_case.js`; the lane's evaluator; composite and main-case band at each mapped elasticity |
| `build_panel.py` | harmonised county panel, CBP imputation, both instruments |
| `iv.py` | OLS, 2SLS, first stages, effective F, Anderson-Rubin sets, Hansen J, Rotemberg weights |
| `estimate.py` | every specification, placebos, cross-sections, key results |
| `verify.py` | recomputes key estimates without `iv.py`'s partialling-out and checks Anderson-Rubin bounds directly |

## Outputs

| File | Contents |
|---|---|
| `derived/gates.json`, `derived/main_case_gates.json` | gate results |
| `derived/panel.csv` | 3,098 county areas: population, real spending by item and year, instruments, flags |
| `derived/build_audit.json` | CBP suppression shares, instrument national changes, origin coverage, national spending by year |
| `derived/estimates.csv` | 780 rows: every OLS, 2SLS, first stage, reduced form and placebo computed |
| `derived/rotemberg.csv` | industry Rotemberg weights and just-identified estimates, 2012–2022, 2007–2017, 2007–2012 |
| `derived/cross_section.csv` | elasticities in levels: counties, state sums of county areas, states (state and local) |
| `derived/estimates_summary.json` | key specifications, Anderson-Rubin tally, map points |
| `derived/main_case_map.csv` | composite response and adopted main-case band at each mapped elasticity |

## Traps

- The 2022 individual-unit file (re-released July 2026) carries local financial administration of
  $39.9bn against $18.9bn in 2017; NYC alone reports +$9.55bn. The published 2022 Table 1 shows
  $23.7bn. Windows ending in 2022 are contaminated; see `RESULT.md`.
- New York City's government is filed under New York County; the five boroughs are one unit here.
- CBP suppresses 53–55% of county 3-digit cells in 2007 and 2012. They are imputed from size classes.
- Python's `zipfile` cannot read the database's Deflate64 member; `unzip -p` can.
- Running another lane's script to check a gate would rewrite its outputs; `no_write_hook.js` blocks that.
