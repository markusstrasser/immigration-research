**Verdict:** Measured skill of Mexico-born arrival cohorts ROSE across cohorts; it did not fall.
At a fixed 0–5 years since arrival, ages 25–54, the less-than-high-school share went 82.5% (1975–80
arrivals, 1980 census) → 66.4% (1985–90) → 61.5% (1995–2000) → 51.7% (2005–10) → 33.3% (2018–23),
and BA+ went 3.4% → 5.8% → 6.2% → 9.1% → 21.7%. The education-conditional log-income residual
against US-born white workers of the same age in the same survey went −0.429 → −0.552 → −0.473 →
−0.418 → −0.309: a deterioration through the 1980s, then a sustained recovery. The shape is
U-shaped, not a secular decline.

Model ID of the lane agent: `claude-opus-5[1m]`.

## Files

| File | What it holds |
|---|---|
| `derived/entry_quality_fixed_duration_ipums.csv` | Headline table: entry quality at fixed duration (0–3 and 0–5 years), two worker definitions |
| `derived/ipums_edu_by_cohort_year.csv` | Education and employment, Mexico-born, by cohort × survey year |
| `derived/ipums_wage_residual_by_cohort_year.csv` | Synthetic-cohort assimilation profiles |
| `derived/ipums_wage_residual_by_ysm_band.csv` | Same, by years-since-arrival band |
| `derived/ipums_native_white_benchmark.csv`, `derived/ipums_native_cell_means.csv` | Comparison-group cells |
| `derived/acs_cohort_composition.csv`, `..._allsex.csv` | ACS 2023/2024 by cohort × sex: education, English, employment, non-citizen share |
| `derived/acs_wage_residual_by_cohort.csv`, `..._allsex.csv`, `..._unadjusted.csv`, `..._by_ysm_band.csv` | ACS wage residuals with intervals |
| `derived/acs_native_benchmark.csv`, `derived/acs_native_cell_means.csv` | ACS comparison-group cells |
| `derived/acs_recent_arrival_origin_mix.csv` | Mexican share of 2020–21 / 2021–24 / 2022–24 foreign-born arrivals aged 25–54 |
| `derived/acs_2024_top_origins_2021_24_arrivals.csv` | Top 15 birthplaces among 2021–24 arrivals |
| `derived/bound_agestd_education_first_obs.csv` | Crude and age-standardised education at each cohort's first observation and ten years later |
| `derived/bound_implied_leaver_education.csv` | Return-migration accounting bound on education |
| `derived/bound_stayer_residual_inflation.csv` | Stayer-only bias in the earnings residual as L·δ |
| `derived/bound_undercount_sensitivity.csv` | ACS undercount stress test for the 2018–23 cohort |

## Scripts

`stage_acs.py` (stream-extract PUMS columns to `_cache/*.parquet`), `ipums_cohorts.py`,
`acs_cohorts.py`, `entry_quality.py`, `bounds.py`. All run with
`uv run --no-project --with duckdb --with pandas --with numpy --with pyarrow python3`.

## Data

- IPUMS USA panel `ipums_usa_borjas_panel` in
  `/Users/alien/research-data/immigration-fiscal/derived/immigration_microdata.duckdb`, opened
  read-only and not modified. 1980/1990/2000 censuses + 2010/2023 ACS. Mexico-born `BPL == 200`.
- ACS 1-year PUMS 2023 (`data/census/acs_pums_2023_person.zip`) and 2024
  (`data/external/acs_pums_2024_1yr/csv_pus.zip`). Mexico-born `POBP == 303`.

## Not delivered

- **English at two fixed points per cohort.** Needs ACS 1-year files for 2005–2019 to separate
  duration from cohort. The Census FTP site served at roughly 13 MB/min during this lane; partial
  downloads are parked at `data/external/acs_pums_years/pus_{2005,2010,2013,2015,2019}.zip.part`
  and a resumable fetch loop is in `/tmp/dl_pums.sh`. English is reported as a 2023/2024
  duration profile only, explicitly marked as not identified.
- **Origin-relative selection.** No INEGI or IPUMS-International Mexican attainment table was
  fetched; Chiquiar-Hanson 2005 and Fernández-Huertas Moraga 2011 are named but not quoted from
  source. Section 8 of the memo is marked [UNVERIFIED] throughout.
- **CBP encounters by nationality.** The FY2021–FY2024 nationwide-encounters CSV is at
  `https://www.cbp.gov/sites/default/files/2024-10/nationwide-encounters-fy21-fy24-aor.csv`
  (HTTP 200 confirmed). The ACS-side answer to the same question is delivered: Mexican-born are
  14.3% of 2021–24 foreign-born arrivals aged 25–54.

## Caveats that travel with these numbers

All intervals are design-naive (no replicate weights). The IPUMS extract has no `SEX`, `HISPAN`,
`SPEAKENG`, `INCWAGE` or `UHRSWORK`, so its results are all-sex and its comparison group is white
including Hispanic white. Education uses harmonised `EDUC`, not `EDUCD`, because the 1980 census
codes grade 12 as `EDUCD` 60 with no diploma split. The 2010 ACS carries no continuous weeks-worked
variable, so the headline table uses "employed with positive income" rather than full-year workers.
Every level is a stayer statistic.

Not committed.
