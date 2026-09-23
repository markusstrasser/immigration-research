# Brief: where in Mexico's schooling distribution do Mexican migrants come from, by arrival cohort?

Date: 2026-09-23. Operator question, verbatim: "I thought the mexican cohort comes from the middle of
the mexican school/school performance distribution?" and, on selection over time, "Butcher & Piehl
found each recent cohort more positively selected than the last ... can we see that in our data?"

## Deliverables (in this directory only; do not edit any other file; do not commit)

1. `RESULT.md` opening with `**Verdict:**` (plain prose, short, numbers with sources), then method,
   tables, limits, reproduce commands. Tags: `[SOURCE: …]`, `[DATA: …]`, `[CALCULATION: …]`,
   `[INFERENCE]`, `[UNVERIFIED]`.
2. Scripts plus `derived/*.csv` tables (aggregates only). Microdata goes in `_cache/` (ignored: add
   a `.gitignore` with `_cache/`). IPUMS microdata must never be committed.
3. Return the RESULT.md path and ≤10 lines.

## Estimand

For Mexico-born adults who arrived at age 20 or older (schooling finished in Mexico; show 18+ as a
sensitivity), by arrival cohort (five-year windows from 1975–79 to 2015–19, plus 2020–23 if
possible): their position in the schooling distribution of their own birth cohort in Mexico.

- Report the share in each attainment category next to Mexico's shares for the same birth years
  (none/primary incomplete, primary, lower secondary, upper secondary, tertiary), and a mean
  percentile rank (ridit: 0.5 = a random draw from Mexico; ties spread within a category).
- Say directly whether the migrants are drawn from the middle (fewer in both tails than Mexico),
  from the top, or from the bottom, and whether that position changed across cohorts.
- Sex separately and pooled.

## Data

- Origin side: INEGI census tabulations of attainment by five-year age. 2020 is held
  (`sources/immigration-fiscal/data/external/stage3/inegi/cpv_educacion/cpv2020_b_eum_07_educacion.xlsx`,
  see `infra/immigration-fiscal/arrival_cohorts_2026_09_18/ACQUIRED.md`). Fetch the 1990, 2000,
  2010 census and 2015 Intercensal equivalents from inegi.org.mx, pin URL and sha256 in a
  `sources.json`. Better if available: IPUMS International Mexico samples (1990, 2000, 2010, 2015,
  2020) through the IPUMS API (`IPUMS_API_KEY` in `infra/immigration-fiscal/acquire/config.local.env`;
  source it with `set -a; . <file>; set +a`; never print it). If the account lacks IPUMS-I access,
  use the INEGI tabulations and say so.
- Migrant side: the held IPUMS USA panel (`immigration_microdata.duckdb`, table
  `ipums_usa_borjas_panel`, located via `infra/immigration-fiscal/_data_paths.py` or as in
  `arrival_cohorts_2026_09_18/ipums_cohorts.py`; BPL = 200 is Mexico; EDUC/EDUCD; YRIMMIG; AGE) for
  1980/1990/2000/2010/2023, and ACS PUMS via the Census API (SCHL detailed grades, POBP = 303, YOEP,
  AGEP, SEX, PWGTP + 80 replicates) for other years. Census key in the same config file; pipe any
  output that may echo a URL through `sed -E 's/key=[A-Za-z0-9]+/key=<KEY>/g'`. The API truncates
  large responses silently: pull by state or verify counts.
- Compare each cohort with Mexico's distribution for the same birth years in the census nearest
  the arrival window (and in 2020 as a check). Map US grades to Mexican levels explicitly (grade 6
  = primaria, grade 9 = secundaria, HS diploma or grade 12 = media superior; say how "some college"
  and associate degrees are treated) and test the mapping's sensitivity.

## Traps and competing evidence (address each)

- Chiquiar & Hanson (2005 JPE): intermediate or positive selection on observables, 1990/2000.
  Fernández-Huertas Moraga (2011 REStat): negative selection with Mexican panel data, attributed to
  an undercount of unskilled migrants in US sources. Run an undercount sensitivity: inflate the
  lowest category of recent, likely unauthorized arrivals by 1.1–1.75 (the arrival-cohort lane's
  section 7 used 1.75).
- Our ENADID lane (ladder 174): returnees had about one year less schooling than stayers (men
  only). Returnees are a selected subset; say how that bears on the stock result.
- The US stock drops return migrants and the dead, so older cohorts observed late are survivors.
  Prefer measuring each cohort within 0–5 years of arrival.
- Schooling is one dimension. Do not read it as selection on crime propensity or ability.

## Existing work to build on (read before computing; do not redo)

- `research/immigration-mexican-arrival-cohorts-2026-09-18.md` §8 (slope result: selection flat)
  and `infra/immigration-fiscal/arrival_cohorts_2026_09_18/` (`origin_relative.py`, `origin_age.py`,
  `derived/origin_age_vs_acs.csv`, which already shows a same-age comparison for 2019/2021)
- `decisions/2026-09-17-selection-measurement-scope.md` (a BA-share gap is not overall selection)
- `infra/immigration-fiscal/enadid_return_selectivity_2026_09_22/RESULT.md`

## Run conventions

`OPENBLAS_NUM_THREADS=1 uv run --no-project python3 <script>` from the repo root. Report every
specification you computed. Before finishing, re-run every script from a clean `derived/` and
confirm the tables reproduce.
