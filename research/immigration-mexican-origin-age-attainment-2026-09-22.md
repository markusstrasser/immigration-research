# Mexico-born vs origin, same 5-year ages (2026-09-22)

Companion to [arrival-cohorts memo](immigration-mexican-arrival-cohorts-2026-09-18.md) section 8,
which still uses INEGI 15+ mean years for the *slope* and left age×cohort placement unretrieved.
This file is that cut. It does not change the slope finding and is not a Fernández-Huertas Moraga
replication.

**Verdict:** At matched 5-year ages, recent Mexico-born US stayers (ACS 2019, 0–5 years since
arrival, 25–54) have a less-than-high-school share 9–13 pp below Mexican residents of that age
in the 2020 census. The gap is present in every band from birth years 1966–70 through 1991–95
and does not widen for the young. BA+ is within three points except the smallest cell (50–54,
n=233). Same-age placement therefore does not revive “selection rose.”
[DATA: `infra/immigration-fiscal/arrival_cohorts_2026_09_18/derived/origin_age_vs_acs.csv`]
[CALCULATION: `origin_age.py`]
[FRAMING-SENSITIVE] as a selection *level* (US-side stayers, ACS can code Mexican secundaria as a
US diploma); the cross-age stability of the LTHS gap is a measurement.

## Table

Origin: INEGI Censo 2020 cuestionario básico tabulado 13, national Total. LTHS = ISCED 0–2
(less than primary + primary + lower secondary). BA+ = ISCED 6–8 (tertiary, master’s,
doctorate); short-cycle tertiary is not BA+. Shares of specified (unspecified <0.3%).
[SOURCE: https://www.inegi.org.mx/contenidos/programas/ccpv/2020/tabulados/cpv2020_b_eum_07_educacion.xlsx fetched 2026-09-22]
ACS: 2019 1-year PUMS, POBP=303, SCHL ≤15 LTHS, ≥21 BA+, YOEP ≥ 2014.
[DATA: `infra/immigration-fiscal/arrival_cohorts_2026_09_18/derived/origin_age_vs_acs.csv`]
[CALCULATION: `origin_age.py`]

| Age | Origin birth years | Mexico LTHS | US recent LTHS | Gap | Mexico BA+ | US recent BA+ | US n |
|---|---|---|---|---|---|---|---|
| 25–29 | 1991–95 | 45.0% | 36.2% | −8.9 pp | 22.9% | 20.3% | 1,033 |
| 30–34 | 1986–90 | 49.5% | 40.5% | −9.0 pp | 22.5% | 22.7% | 796 |
| 35–39 | 1981–85 | 55.4% | 41.9% | −13.5 pp | 20.4% | 18.5% | 612 |
| 40–44 | 1976–80 | 60.9% | 51.9% | −9.0 pp | 17.5% | 18.5% | 469 |
| 45–49 | 1971–75 | 63.4% | 50.7% | −12.7 pp | 15.6% | 15.8% | 343 |
| 50–54 | 1966–70 | 64.7% | 52.8% | −11.9 pp | 14.8% | 9.6% | 233 |

Origin mean years of schooling on the same rows: 11.49 (25–29) down to 9.33 (50–54). National
15+ mean on the sheet is 9.738, matching Cuéntame’s 9.7.
[SOURCE: https://www.inegi.org.mx/contenidos/programas/ccpv/2020/tabulados/cpv2020_b_eum_07_educacion.xlsx sheet 13 Total]
[DATA: `derived/inegi_2020_isced_by_age.csv`]

## What this is not

- Not a slope. The 15+ mean-years comparison (migrant +2.37 vs origin +2.20, 2000–2023/2020)
  stays in the parent memo. [DATA: `infra/immigration-fiscal/arrival_cohorts_2026_09_18/derived/origin_relative_mean_years.csv`]
- Not Mexico-side emigrant identification. Fernández-Huertas Moraga’s negative-selection result
  used ENADID; this is ACS stayers against the origin census. The two can disagree without either
  arithmetic being wrong. [DATA: research/immigration-mexican-arrival-cohorts-2026-09-18.md §8]
  The held ENADID files do disagree: Mexico-born ages 25–54 now in Mexico who lived in the US
  five years earlier have 8.98 vs 10.29 mean years (2018; n=836) and 9.66 vs 10.79 (2023; n=511).
  [DATA: `infra/immigration-fiscal/enadid_2026_09_20/derived/return_selectivity_by_schooling.csv`]
  [CALCULATION: `selectivity.py`] Returnees only; departures still abroad are not in TSDem.
- Not the all-duration stock. Mexico-born 25–29 in the US including child arrivals are 28.5%
  LTHS (stock) vs 36.2% (0–5 YSM) vs 45.0% (origin). Child arrivals finish US high school.
  [DATA: `derived/origin_age_vs_acs.csv` columns `sh_lths_stock_2019`, `sh_lths_recent_2019`]
- Not robust to ACS secundaria-as-diploma coding, which shrinks migrant LTHS and inflates
  apparent positive selection on that margin. [DATA: research/immigration-confidence-ladder.md entry 133]

2021 ACS 0–5 YSM repeats the LTHS sign in every band. [DATA: `sh_lths_recent_2021` in the same csv]
2010 INEGI national-by-age ISCED was not isolated (Basico 07_* is state `.xls`; 07_01B is 6–14
literacy). [SOURCE: https://www.inegi.org.mx/contenidos/programas/ccpv/2010/tabulados/Basico/07_01B_ESTATAL.xls]

Acquisition: [ACQUIRED.md](../infra/immigration-fiscal/arrival_cohorts_2026_09_18/ACQUIRED.md).
Stop rule: [two-source stop](../notes/immigration-two-source-stop-2026-09-22.md).
