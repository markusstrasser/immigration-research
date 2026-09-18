**Verdict:** UNINFORMATIVE on the DSS employment-entry estimand; the identifying variation is absent on 2005–2023 US metro data for both the conventional past-settlement instrument and the JRS correction, and that absence is the finding.

Written by the parent session 2026-09-18 after the lane closed with estimates computed but sections 3 and 5 of the memo unwritten.

## Headline rows (min_pop 50,000, both sexes, native no-college E/POP 18–29, Mexico-born treatment)

| arm | coef (pp per pp) | 95% CI | first-stage F | Shea R² |
|---|---:|---|---:|---:|
| OLS, pooled 5y | +0.25 | [−0.07, +0.56] | | |
| IV-single, pooled 5y | −1.00 | [−5.26, +3.26] | 3.6 | 0.008 |
| IV-JRS, pooled 5y | −9.65 | [−53.2, +33.9] | 20.2 | 0.0007 (corr Zm, Zm lag 0.82) |
| IV-single, pooled 10y | −0.43 | [−1.28, +0.42] | 145 | 0.10 |
| IV-single, 2008–13 | +1.20 | [+0.62, +1.77] | 30 | |
| IV-single, 2013–18 | −0.83 | [−1.77, +0.10] | 152 | |
| College control, IV-single 10y | +0.09 | [−0.62, +0.80] | 95 | |
| Single-instrument placebo, 2013–18 on 2008–13 outcome | +2.36 (SE 0.53) reduced form | | | |

DSS benchmark in these units: about −0.6 (all natives), −0.9 (unskilled). The best interval contains zero and both.

## JRS check
Cannot be run: current and lagged multi-origin predicted inflows correlate 0.82 across metros; Shea's partial R² 0.0007 with F 20 is the underidentification signature JRS report for every US decade after the 1970s. The coefficient move from −1.0 to −9.7 has a ±40-point interval and no direction.

## Verification by the parent
- `estimate.py` re-run: `derived/estimates.csv` byte-identical (2,904 rows). `report.py` re-run: `derived/tables.md` byte-identical.
- `placebo_single.py` added and run: `derived/placebo_single.csv` (9 rows).
- Brief-vs-data corrections recorded in memo §1 (IPUMS panel has no sub-state geography or sex; rebuilt from the Census API on seven endpoint years; ACS 2020 1-year does not exist).

## Covered / skipped
Covered: OLS, IV-single, IV-multi, IV-JRS, multi-origin placebo, per-window and pooled, 5y/10y, men/women/both, 16–24, college control, two population floors, all-foreign-born arm. Skipped: wages (not pulled); annual panel between endpoint years (link too slow); Kleibergen–Paap (linearmodels exposes none; Shea used); metro-level native-mobility test (would need the same panel for all natives, not built).

## Files
Scripts: `fetch_crosswalks.py`, `fetch_origins.py`, `pull_pums3.py`, `pull_placebo.py`, `build_panel.py`, `build_instruments.py`, `diagnostics.py`, `estimate.py`, `report.py`, `write_memo.py`, `placebo_single.py`. Derived: `estimates.csv`, `tables.md`, `placebo_single.csv`, `metro_year_panel.csv` (byproduct: metro × year foreign-born and Mexico-born shares on fixed 2013 CBSAs, closes the rent-elasticity memo's gated input), `metro_base_2000.csv`, `metro_origin_base.csv`, `national_origin_stock.csv`, `national_mex_1864.csv`. `_cache/` is gitignored.
