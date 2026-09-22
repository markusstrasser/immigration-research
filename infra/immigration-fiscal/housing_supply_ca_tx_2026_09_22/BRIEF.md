# Brief — housing supply, Mexican-origin demand and rents: California against Texas, and the metro cross-section

Owner: worker agent `housing-ca-tx`. Parent: session immigration-research-f5. Date: 2026-09-22.
You own this directory only. Do not edit or commit anything outside it. Do not commit at all; the
parent grades and commits.

## Question

California and Texas hold the same Mexican-origin population share (about 32%; FAQ 15 of
`research/immigration-objections-faq-2026-09-21.md`). The operator's claim to test and quantify:
"California is not building, only Texas is." Three descriptive pieces and one mechanical
calculation, nothing causal:

1. **State supply.** Permits per 1,000 residents and per 1,000 existing housing units, by year
   2000–2024, for California, Texas and the United States; population growth against
   housing-unit growth over 2010–2024.
2. **Metro cross-section.** For the metros in the warehouse table `msa_rent_elasticity_panel`
   (168 rows; Saiz supply elasticity, WRLURI, Zillow rent growth): the change in the
   Mexican-origin population share 2010 → 2023 (ACS 5-year), Zillow ZORI rent growth
   2015 → latest, and the Saiz elasticity. Report the descriptive regression of rent growth on
   the share change, on the share change × (1 / elasticity), and with state fixed effects, with
   heteroskedasticity-robust standard errors. Label it descriptive; ladder 136 says the usual
   instruments for Mexican inflows lose their variation after 2005, so no IV here.
3. **Mechanical price response.** In a market with demand shift `d`, supply elasticity `ε_S` and
   demand elasticity magnitude `ε_D`, the rent response is `d / (ε_S + ε_D)`. For Los Angeles,
   San Francisco, San Diego, Riverside, Houston, Dallas, Austin, San Antonio: the response to a
   1% demand shift at that metro's Saiz elasticity with `ε_D` at 0.5, 0.7 and 1.0 (assumed;
   say so), and the ratio of each California metro's response to Houston's. This is arithmetic
   on published elasticities, not an estimate.
4. **Native migration, one year.** From the local ACS 2024 1-year person PUMS: native-born
   non-Hispanic white adults 25–64 who lived in a different state one year earlier (`MIGSP`),
   by destination state (California, Texas) and by education (bachelor's or more vs less), as
   gross in-flows and out-flows and the net rate per 1,000 resident natives of the same group;
   standard errors from the 80 replicate weights (successive-difference formula:
   SE² = 4/80 × Σ (θ_r − θ)²). Report the same for all natives as a check row.

## Inputs — primary sources only, no web summaries

- **Permits.** Census Building Permits Survey annual state files under
  `https://www2.census.gov/econ/bps/State/` (list the directory; read the documentation under
  `https://www2.census.gov/econ/bps/Documentation/` before parsing; total units = sum of the
  units columns across the 1-unit, 2-unit, 3–4-unit and 5+-unit structure classes). Cross-check
  three years for each state against FRED `CABPPRIV` and `TXBPPRIV`
  (`https://fred.stlouisfed.org/graph/fredgraph.csv?id=CABPPRIV`, monthly, sum to calendar
  years; no key). Record the relative difference; a difference above 1% is a gate failure to
  explain, not to hide.
- **Population.** Census population estimates: `NST-EST2024-ALLDATA.csv` (2020–2024),
  `nst-est2019-alldata.csv` (2010–2019) and the 2000–2010 intercensal state file, all under
  `https://www2.census.gov/programs-surveys/popest/datasets/`. Verify the exact paths by listing.
- **Housing units.** ACS 1-year `B25001_001E` by state for 2010, 2015, 2019, 2023, 2024 through
  the Census API, or the popest housing-unit estimate files if they cover the years; say which.
- **Metro Mexican-origin population.** ACS 5-year `B03001_004E` (Hispanic or Latino: Mexican)
  and `B03001_001E` (total) by metropolitan/micropolitan statistical area, vintages 2010 and
  2023, through the Census API. Confirm the variable labels from the API's `variables.json`
  (key-free) before use and record them in `audit.json`.
- **Rents and elasticities.** Local, read-only:
  `sources/immigration-fiscal/data/external/urban_housing/zillow/metro_zori_sfrcondomfr_sm_month.csv`;
  `warehouse/immigration_context.duckdb` table `msa_rent_elasticity_panel` (open read-only;
  gives the Saiz-metro ↔ Zillow-metro name crosswalk, elasticity and WRLURI);
  `sources/immigration-fiscal/data/external/lifetime/saiz/saiz_2010_msa_elasticity.dta`.
  The name crosswalk is names-only (see `research/immigration-msa-rent-elasticity-panel-2026-06-25.md`);
  report how many of the 168 metros you could join to a 2010 and a 2023 ACS CBSA row and list
  the failures.
- **PUMS.** `sources/immigration-fiscal/data/external/acs_pums_2024_1yr/csv_pus.zip` (read
  in place with DuckDB or pandas; do not unzip into the repo). Confirm the variable names from
  the file header (`STATE` or `ST`, `MIGSP`, `NATIVITY`, `RAC1P`, `HISP`, `AGEP`, `SCHL`,
  `PWGTP`, `PWGTP1`–`PWGTP80`) and the code lists from the 2024 PUMS data dictionary
  (`https://www2.census.gov/programs-surveys/acs/tech_docs/pums/data_dict/`), recorded in
  `audit.json`.

## Census API key

```sh
cd /Users/alien/Projects/immigration-research
set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a   # exports CENSUS_API_KEY
```

Never print the key. Wrap every request so that any exception or URL you print has the `key=`
query parameter removed (`re.sub(r"key=[^&]+", "key=REDACTED", text)`). Do not run `ps` or
`pgrep` dumps. Cache raw responses under `_cache/` (ignored by the `.gitignore` you create:
one line `_cache/`).

## Deliverables (all inside this directory)

- `fetch.py` — every download, with source URL, bytes and sha256 written to `_cache/manifest.json`.
- `analysis.py` — builds `derived/state_supply.csv` (state-year rows for CA, TX, US: permits,
  population, housing units, permits per 1,000 residents, permits per 1,000 units),
  `derived/metro_panel.csv` (one row per joined metro), `derived/metro_regressions.csv`,
  `derived/mechanical_response.csv`, `derived/native_migration_2024.csv`, and
  `derived/audit.json` (gates, variable labels, join counts, source hashes, limitations).
- `test_analysis.py` — at least: the BPS parser on a small inline fixture; the mechanical
  formula against hand values; the replicate-weight SE against a hand-computed fixture; the
  metro join refusing duplicate names.
- `README.md` — run commands, inputs, definitions.
- `RESULT.md` — first line `**Verdict:** …`, then the numbers with `[SOURCE]` / `[DATA]` /
  `[CALCULATION]` tags on every figure, the gates table, a "Files covered / skipped" section
  with reasons, and the limitations copied from `audit.json` without softening. Include your
  model self-report line.

Gates, each recorded PASS/FAIL in `audit.json` and `RESULT.md`:

- G1 permits: BPS annual totals vs FRED for CA and TX in 2015, 2019, 2023 within 1%.
- G2 population: popest 2023 state totals vs ACS 1-year `B01003_001E` 2023 within 2%.
- G3 metro join: report joined / unjoined counts; the regression runs on the joined set only.
- G4 PUMS: the weighted count of native-born non-Hispanic white adults 25–64 in California and
  Texas, with the SE, printed and compared against the ACS 1-year table `B05003H` (or the
  closest published table you can find; say which) within 3%.
- G5 every reported ratio has a finite denominator; no row with fewer than 100 PUMS
  observations is reported.

Run everything from the repository root with `uv run --no-project python3 …`; add
`--with pyreadstat` or `--with pandas` only if an import fails, and record the extra wheel in
README. Tests: `uv run --no-project python3 -m pytest infra/immigration-fiscal/housing_supply_ca_tx_2026_09_22/ -q`.

## Rules

- Primary sources only; if a source is unreachable, write `[BLOCKED] <source>: <error without
  key>` in RESULT.md and continue with the rest.
- No causal language anywhere. "Associated with" and "at this elasticity the arithmetic gives".
- Print line-based progress, no carriage returns, `PYTHONUNBUFFERED=1`.
- When done, reply with the path of `RESULT.md` and at most ten lines: verdict, gate results,
  anything skipped and why.
