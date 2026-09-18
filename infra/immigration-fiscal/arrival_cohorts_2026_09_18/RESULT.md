**Verdict:** Measured skill of Mexico-born arrival cohorts rose sharply; selection relative to the
Mexican origin distribution did not move. At a fixed 0–5 years since arrival, ages 25–54, the
less-than-high-school share went 82.5% (1975–80 arrivals, 1980 census) → 66.4% (1985–90) → 61.5%
(1995–2000) → 51.7% (2005–10) → 33.3% (2018–23), and BA+ went 3.4% → 5.8% → 6.2% → 9.1% → 21.7%.
The education-conditional log-income residual against US-born white workers of the same age in the
same survey went −0.429 → −0.552 → −0.473 → −0.418 → −0.309: deterioration through the 1980s, then
sustained recovery. But migrant entry cohorts gained 2.37 years of mean schooling between the 2000
and 2023 surveys while INEGI puts the Mexican 15+ gain at 2.20 years between 2000 and 2020, so the
absolute improvement is the Mexican schooling expansion, not a change in who migrates.

Model ID of the lane agent: `claude-opus-5[1m]`.

Memo: `/Users/alien/Projects/immigration-research/research/immigration-mexican-arrival-cohorts-2026-09-18.md`

## Files

| File | What it holds |
|---|---|
| `derived/entry_quality_fixed_duration_ipums.csv` | Headline table: entry quality at fixed duration (0–3 and 0–5 years), two worker definitions |
| `derived/origin_relative_mean_years.csv` | Migrant mean years at entry against the INEGI origin series |
| `derived/ipums_edu_by_cohort_year.csv` | Education and employment, Mexico-born, by cohort × survey year |
| `derived/ipums_wage_residual_by_cohort_year.csv` | Synthetic-cohort assimilation profiles |
| `derived/ipums_wage_residual_by_ysm_band.csv` | Same, by years-since-arrival band |
| `derived/ipums_native_white_benchmark.csv`, `derived/ipums_native_cell_means.csv` | Comparison-group cells |
| `derived/acs_cohort_composition.csv`, `..._allsex.csv` | ACS 2023/2024 by cohort × sex: education, English, employment, non-citizen share |
| `derived/acs_wage_residual_by_cohort.csv`, `..._allsex.csv`, `..._unadjusted.csv`, `..._by_ysm_band.csv` | ACS wage residuals with intervals |
| `derived/acs_native_benchmark.csv`, `derived/acs_native_cell_means.csv` | ACS comparison-group cells |
| `derived/acs_recent_arrival_origin_mix.csv` | Mexican share of 2020–21 / 2021–24 / 2022–24 foreign-born arrivals aged 25–54 |
| `derived/acs_2024_top_origins_2021_24_arrivals.csv` | Top 15 birthplaces among 2021–24 arrivals |
| `derived/cbp_mexican_share_encounters.csv` | Mexican share of CBP encounters FY2021–FY2025, with the Title 8-only column |
| `derived/cbp_top_nationalities_sw_fy2023.csv`, `..._fy2024.csv` | Southwest border nationality mix |
| `derived/bound_agestd_education_first_obs.csv` | Crude and age-standardised education at each cohort's first observation and ten years later |
| `derived/bound_implied_leaver_education.csv` | Return-migration accounting bound on education |
| `derived/bound_stayer_residual_inflation.csv` | Stayer-only bias in the earnings residual as L·δ |
| `derived/bound_undercount_sensitivity.csv` | ACS undercount stress test for the 2018–23 cohort |
| `derived/english_*.csv`, `derived/edu_*_cohort_x_duration_matrix.csv` | English and education by cohort × duration band, **2023 and 2024 only**, so most cells are empty and the decomposition is not identified (see Not delivered) |

## Scripts

`stage_acs.py` (stream-extract PUMS columns to `_cache/*.parquet`), `ipums_cohorts.py`,
`acs_cohorts.py`, `entry_quality.py`, `bounds.py`, `origin_relative.py`, `cbp_nationality.py`,
`english_cohorts.py`. `english_cohorts.py` carries a hard guard that refuses any state-chunked
survey year with fewer than 51 state files, because a partial state set dominated by one large
state reads like a survey year and would silently corrupt every cross-cohort comparison. All run with
`uv run --no-project --with duckdb --with pandas --with numpy --with pyarrow python3`.

## Data

- IPUMS USA panel `ipums_usa_borjas_panel` in
  `/Users/alien/research-data/immigration-fiscal/derived/immigration_microdata.duckdb`, opened
  read-only and not modified. 1980/1990/2000 censuses + 2010/2023 ACS. Mexico-born `BPL == 200`.
- ACS 1-year PUMS 2023 (`data/census/acs_pums_2023_person.zip`) and 2024
  (`data/external/acs_pums_2024_1yr/csv_pus.zip`). Mexico-born `POBP == 303`.
- Mexico-born person records for ACS 1-year 2005–2021 pulled from the Census PUMS API with the
  predicate `POBP=303`, cached in `_cache/pums_api_<year>_mex.json`.
- CBP Nationwide Encounters FY2021–FY2024 (retrieved this lane, saved to
  `data/external/cbp/nationwide-encounters-fy21-fy24-aor.csv`) and FY2022–FY2025 (already staged).
- INEGI grado promedio de escolaridad 2000–2020 and the 2020 census attainment distribution,
  fetched from `cuentame.inegi.org.mx` and `inegi.org.mx/temas/educacion`.
- Chiquiar & Hanson NBER w9242 full text; Fernández-Huertas Moraga 2011 published abstract via
  RePEc.

## Operational notes for whoever extends this

The Census FTP site served full-year PUMS zips at roughly 13 MB/min and dropped HTTP/2 connections
with `PROTOCOL_ERROR` partway through every large transfer. Two workarounds were needed and both
worked: force `--http1.1` with `-C -` resume for files that support byte ranges, and for files that
do not (cbp.gov), loop fresh fetches and validate the payload before accepting it. The Census PUMS
API with a `POBP=303` predicate is far cheaper than downloading the full person file when only one
birthplace is needed; it also drops connections, so validate that the JSON ends in `]]`.
Partial FTP downloads are parked at `data/external/acs_pums_years/pus_*.zip.part` with the
resumable loop in `/tmp/dl_pums.sh`.

## Caveats that travel with these numbers

All intervals are design-naive (no replicate weights), so true intervals are wider. The IPUMS
extract has no `SEX`, `HISPAN`, `SPEAKENG`, `INCWAGE` or `UHRSWORK`, so its results are all-sex and
its comparison group is white including Hispanic white. Education uses harmonised `EDUC`, not
`EDUCD`, because the 1980 census codes grade 12 as `EDUCD` 60 with no diploma split; using `EDUCD`
manufactures a spurious 1980 outlier. The 2010 ACS carries no continuous weeks-worked variable, so
the headline table uses "employed with positive income" rather than full-year workers. Every level
is a stayer statistic. The origin comparison is a slope comparison only; the levels are not
comparable because the INEGI base is ages 15+ and the migrant base is 25–54.

## Not delivered

**English ability at two fixed points per cohort** (brief item 2). Separating cohort from duration
needs ACS 1-year files between 2005 and 2019. The Census FTP site served full-year PUMS zips at
roughly 13 MB/min and dropped every large transfer; the Census PUMS API with a `POBP=303` predicate
returns exactly the right records and works, but at about 27 KB/s, roughly an hour per survey year.
`english_cohorts.py` is written and tested against the staged 2023/2024 files and consumes
state-chunked API pulls from `_cache/states_<year>/st_*.json`; the fetcher is `/tmp/fetch_states.sh
<year>`, which skips state files it already has, so rerunning it resumes. Partial 2013 and 2019
pulls (4 of 51 states each) are on disk; the background fetchers were stopped when this lane closed
rather than left competing for bandwidth. Run the fetcher to completion and then
`english_cohorts.py` to finish the item. No cohort-versus-duration claim about
English appears in the memo.

**Origin attainment by birth cohort.** The origin comparison uses INEGI's national mean years of
schooling for ages 15+, which supports a slope comparison but not placement of each migrant cohort
in the origin distribution of its own generation. INEGI's census tabulados carry attainment by age
group; they were not retrieved.

Not committed.
