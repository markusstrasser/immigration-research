# Housing supply, Mexican-origin demand and rents: California against Texas

Lane for [BRIEF.md](BRIEF.md). Four descriptive pieces and one mechanical calculation.
**Nothing here is causal.** No identification strategy is used, claimed or implied.

## Run

```sh
# from the repository root
set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a   # exports CENSUS_API_KEY

PYTHONUNBUFFERED=1 uv run --no-project python3 \
    infra/immigration-fiscal/housing_supply_ca_tx_2026_09_22/fetch.py

OPENBLAS_NUM_THREADS=1 PYTHONUNBUFFERED=1 uv run --no-project python3 \
    infra/immigration-fiscal/housing_supply_ca_tx_2026_09_22/analysis.py

uv run --no-project python3 -m pytest \
    infra/immigration-fiscal/housing_supply_ca_tx_2026_09_22/ -q
```

`fetch.py` is idempotent: anything already listed in `_cache/manifest.json` and present on
disk is skipped, so a re-run costs nothing. Delete a cache entry to force a refetch.
`analysis.py` reads only `_cache/` and the read-only local sources below, and exits non-zero
if any gate fails. No extra wheels are needed beyond the checkout's `.venv`
(pandas, numpy, duckdb, requests, pytest); robust standard errors are computed in numpy,
so statsmodels is not a dependency.

The Census API key is read from the environment and never printed. Every URL and exception
passes through `redact()` first, in both scripts.

## Inputs

Downloaded by `fetch.py` into `_cache/` (git-ignored; see `_cache/manifest.json` for the
URL, byte count and sha256 of each file):

| Source | What | Used for |
|---|---|---|
| Census Building Permits Survey, `State/st{YY}12y.txt`, 2000-2024 | December year-to-date state permits | annual permit totals |
| Census BPS, `State/st{YY}{MM}c.txt` for 2015, 2019, 2023 | monthly state permits | gate G1b vintage check |
| Census BPS, `Documentation/stateasc.pdf` | state file record layout | parser validation |
| FRED `CABPPRIV`, `TXBPPRIV` | monthly private units authorised | gate G1 cross-check |
| Census popest `NST-EST2024-ALLDATA.csv`, `nst-est2019-alldata.csv`, `st-est00int-alldata.csv` | state population 2000-2024 | permits per resident |
| ACS 1-year `B25001_001E` (2010, 2015, 2019, 2023, 2024) | state housing units | permits per existing unit |
| ACS 1-year `B01003_001E` (2023) | state population | gate G2 |
| ACS 1-year `B05003H_009E`, `B05003H_020E` (2024) | native white non-Hispanic 18+ | gate G4 |
| ACS 5-year `B03001_001E`, `B03001_004E` (2010, 2023) by CBSA | Mexican-origin metro share | metro cross-section |
| ACS 2024 PUMS data dictionary | code lists | variable validation |

Read-only local sources (never modified, hashes recorded in `derived/audit.json`):

- `warehouse/immigration_context.duckdb`, table `msa_rent_elasticity_panel` (168 metros:
  Saiz elasticity, WRLURI, Saiz-to-Zillow name crosswalk), opened read-only.
- `sources/immigration-fiscal/data/external/urban_housing/zillow/metro_zori_sfrcondomfr_sm_month.csv`
- `sources/immigration-fiscal/data/external/lifetime/saiz/saiz_2010_msa_elasticity.dta`
- `sources/immigration-fiscal/data/external/acs_pums_2024_1yr/csv_pus.zip`, read in place
  with `zipfile` and streamed in chunks. It is never unzipped into the repository.

## Definitions

**Permits.** Total units authorised = the sum of the `Units` field across the 1-unit, 2-unit,
3-4 unit and 5+ unit structure classes (columns 6, 9, 12 and 15, zero-indexed). The trailing
"rep" block of the BPS file is the reported, non-imputed subset and is deliberately not used.
Permits are authorisations, not starts or completions.

**Two Census permit products.** The December year-to-date file is Census's cumulative annual
count and absorbs reports that arrive after each month was first published. FRED mirrors the
as-published monthly series. The two differ by −1.7% to +3.1% for CA and TX; summing the 12
monthly files reproduces FRED to the unit (gate G1). The year-to-date file is used for the
headline series because it is the count Census publishes as the year's total;
`derived/permits_vintage_check.csv` shows both against FRED so the choice is inspectable, and
`audit.json → permit_vintage_reconciliation` records the six differences.

**Mexican-origin share.** `B03001_004E / B03001_001E`, ACS 5-year, vintages 2010 (2006-2010)
and 2023 (2019-2023). The change is in percentage points and is a change in five-year averages.

**Rent growth.** Zillow ZORI (smoothed, all homes plus multifamily), metro level.
`zori_log_growth` is log(latest / 2015-01) and is the brief's window. `zori_annualized_from_first`
divides log(latest / first observed month) by the elapsed years and exists for every metro;
16 metros have no January 2015 value and they are smaller and more elastic than the rest,
so specifications 6 to 8 re-run the descriptive regressions on all 168.

**Metro join.** The crosswalk in `msa_rent_elasticity_panel` is names-only. A Zillow metro is
matched to an ACS CBSA row on principal-city name plus state: a first-city match is preferred,
any-principal-city is the fallback, and **an ambiguous match is refused** and reported as a
join failure rather than resolved arbitrarily.

**Mechanical response.** `d / (eps_S + eps_D)` for a 1% demand shift, at each metro's Saiz
elasticity, with the demand elasticity magnitude assumed at 0.5, 0.7 and 1.0. This is
arithmetic on published elasticities under a single-market competitive assumption. It is not
an estimate of any actual rent change.

**Migration.** ACS 2024 1-year PUMS. Native-born is `NATIVITY == 1`; non-Hispanic white is
`RAC1P == 1 and HISP == 1`; bachelor's or more is `SCHL >= 21`. An interstate in-migrant to a
state has `MIGSP` equal to a different US state code (1-56); an out-migrant has `MIGSP` equal
to that state while living elsewhere. Moves from abroad (`MIGSP >= 72`) are not interstate
flows. Standard errors use the 80 replicate weights with the successive-difference formula
`SE^2 = 4/80 * sum_r (theta_r - theta)^2`, applied to the ratio itself for rates.

## Outputs (`derived/`)

| File | Contents |
|---|---|
| `state_supply.csv` | state-year rows for CA, TX, US: permits, population, housing units, permits per 1,000 residents, permits per 1,000 units |
| `state_growth_2010_2024.csv` | population against housing-unit growth, 2010-2024 |
| `permits_vintage_check.csv` | December year-to-date against monthly sum against FRED |
| `metro_panel.csv` | one row per joined metro: elasticity, WRLURI, Mexican-origin share 2010 and 2023, ZORI levels and growth |
| `metro_join_failures.csv` | metros that could not be joined unambiguously (empty when all 168 join) |
| `metro_regressions.csv` | eight descriptive specifications, coefficient, HC1 standard error, t, n, R-squared |
| `mechanical_response.csv` | rent response to a 1% demand shift and the ratio to Houston |
| `native_migration_2024.csv` | gross and net native interstate flows with replicate standard errors |
| `pums_cells_raw.csv` | the weighted cell sums the migration table is built from |
| `audit.json` | gates, variable labels, join counts, source hashes, regression samples, limitations |

## Gates

`G1` the BPS parser against FRED: the sum of the 12 monthly state files within 0.1% of the
FRED calendar sum for CA and TX in 2015, 2019 and 2023. The December year-to-date product's
difference from FRED (−1.7% to +3.1%, a vintage property of the source) is recorded in
`audit.json → permit_vintage_reconciliation` and `derived/permits_vintage_check.csv`, not
gated. `G2` popest against ACS population within 2%. `G3` metro join counts. `G4` PUMS native
non-Hispanic white 18+ against published `B05003H` within 3%. `G5` finite positive
denominators and no reported row under 100 PUMS observations. `G6` warehouse elasticities
re-joined to the primary Saiz file.

The lane was delivered with the year-to-date comparison as a failing 1% gate; the parent
restated it on 2026-09-22 after reproducing the FRED sums independently. `analysis.py` exits
non-zero if any gate fails.
