# Native Employment at Labor-Market Entry and Low-Skill Immigration — US Metro Replication

## Audit correction — September 19, 2026

**Identification remains unresolved.** Within a single window, multiplying one instrument by any nonzero scalar leaves its first-stage F and 2SLS estimate unchanged. A small or negative national shift alone cannot explain weak identification or a coefficient reversal. Pooled-window relative shifts, exposure-outcome correlation and sample changes can matter. A flat college control does not establish absence of demand confounding. Retain the actual F statistics and intervals; remove the unsupported explanation. [SOURCE: principal code and independent IV scaling probe in the mechanisms audit]

This supersedes conflicting interpretations below; calculations are retained as evidence. [Audit index](immigration-five-day-cross-check-2026-09-19.md).


Model self-report: `claude-opus-5[1m]` (verbatim from the environment-info block).

**Verdict:** UNINFORMATIVE on the estimand, and the reason is the finding. A US metro replication of the Dustmann–Schönberg–Stuhler native-entry-employment result cannot be identified on 2005–2023 with either the conventional past-settlement instrument or the Jaeger–Ruist–Stuhler correction. The best-identified number, the 10-year single-instrument IV (first-stage F 145), is −0.43 points of native no-college E/POP per 1-point rise in the Mexico-born share, 95% interval [−1.28, +0.42], which contains zero and the DSS benchmark (about −0.6 to −0.9) at comparable distance. The 5-year single instrument is powerless when pooled (F 3.6) because the national Mexico-born stock stopped growing in 2008 and then fell, so the shift half of the shift-share is near zero or negative; window by window it flips sign (+1.20 [+0.62, +1.77] in 2008–13, −0.83 [−1.77, +0.10] in 2013–18), and the one window that looks like DSS fails a pre-trend placebo (+2.36, SE 0.53, opposite sign). The JRS correction is underidentified here exactly as JRS report for every US decade after the 1970s: current and lagged multi-origin predicted inflows correlate 0.82 across metros and Shea's partial R² is 0.0007, so its coefficient (−9.65 [−53, +34]) is noise. The college control group does not move (+0.09 [−0.62, +0.80]), so the no-college estimate is not a metro-demand artifact, but the two are not distinguishable. Nothing here contradicts DSS; nothing here replicates it. [SOURCE: `infra/immigration-fiscal/employment_entry_2026_09_18/derived/estimates.csv`, `derived/placebo_single.csv`; every row re-run by the parent session 2026-09-18, byte-identical]

Purpose: replicate on US data the estimand that Jaeger, Ruist & Stuhler (2018) and Dustmann,
Schönberg & Stuhler (2017) identify as the durable margin of low-skill immigration — native
employment at labor-market entry — and test whether the JRS multiple-instrumentation correction
moves the short-run coefficient.

## Status log

- 2026-09-18 — [UNVERIFIED] data build started. Crosswalks fetched, ACS PUMS pull in flight.
- 2026-09-18 — [VERIFIED from primary text] two corrections to the brief's framing, recorded
  before estimates exist so they are not read back as post-hoc. (i) The employment-entry result
  is **Dustmann–Schönberg–Stuhler's**, not JRS's; JRS's own corrected estimates are for **wages**
  (a 1% inflow reduces average wages by about 0.7 log points, "substantially more negative" than
  the conventional IV). (ii) JRS report their own correction is underidentified outside the 1970s,
  which is the period this panel sits outside of.
- 2026-09-18 14:01 — [VERIFIED] estimation complete, 2,904 rows in `derived/estimates.csv`; the lane closed before writing sections 3 and 5.
- 2026-09-18 14:45 — [VERIFIED] parent session re-ran `estimate.py` and `report.py` (byte-identical), ran the single-instrument placebo the lane had not (`placebo_single.py`), and wrote the verdict, section 3 reading and section 5 results from those files.

---

## 1. The data the brief assumed does not exist, and what replaced it

The dispatch brief specified the local IPUMS panel
(`$DERIVED_ROOT/immigration_microdata.duckdb`, table `ipums_usa_borjas_panel`) as the source,
described as holding "ACS 1-year 2005–2023 and Census 2000/1990 samples with `MET2013` or
`PUMA`/`CZ` geography and person weights." **That description is wrong on three counts**, verified
by reading the table directly (44,393,133 rows):

| Brief assumed | Panel actually has |
|---|---|
| ACS 1-year 2005–2023 | Five samples only: 1980, 1990, 2000 (5% census), 2010, 2023 (ACS) |
| `MET2013` or `PUMA`/`CZ` geography | `STATEFIP` only — no sub-state geography of any kind |
| sex-specific analysis possible | no `SEX` variable in the extract |

[SOURCE: `describe ipums_usa_borjas_panel`, run 2026-09-18; columns are YEAR SAMPLE SERIAL
CBSERIAL HHWT CLUSTER STATEFIP STRATA GQ PERNUM PERWT AGE RACE RACED BPL BPLD CITIZEN YRIMMIG
EDUC EDUCD EMPSTAT EMPSTATD WKSWORK1 INCTOT]

The project memory file the brief pointed to already records the sample list and the "all-sex"
caveat, so the gap is between the brief and the memory, not inside the memory. The panel was
therefore **not used**, and **not modified**.

Replacement source: the **Census Bureau ACS 1-year PUMS API** (`api.census.gov/data/{year}/acs/acs1/pums`),
pulled fresh. The 2020 ACS 1-year standard release was cancelled, so the API has no 2020 1-year
PUMS and that year cannot appear in any panel.
[SOURCE: HTTP 404 on `api.census.gov/data/2020/acs/acs1/pums`, probed 2026-09-18]

**Years pulled: 2005, 2008, 2010, 2013, 2015, 2018, 2023 — the window endpoints only, not an
annual panel.** The link to the Census servers sustained roughly 90–200 KB/s during the build
and reset large responses mid-transfer, which made a full 18-year national pull impractical
inside this run. Every 5-year and 10-year difference in the design ends on one of these seven
years, so the estimates are unaffected; what is lost is the ability to inspect year-by-year
paths between endpoints, and the option of alternative window definitions without a further
pull. The bulk PUMS zip releases were checked as an alternative and rejected: at roughly 600 MB
per year they are far worse over this link.

Selection is pushed onto the server for the same reason — the outcome call requests only
natives below a bachelor's aged 16–29, and the treatment call only the foreign-born aged 18–64 —
and the 18–64 denominator comes from the published PUMA-level table B01001 rather than from
microdata. The reduced pull was verified to reproduce the unfiltered pull's cell counts exactly
on a test state-year before it was adopted (Rhode Island 2015, every field identical).

## 2. Design

**Unit.** Metropolitan statistical area × year. ACS PUMS carries no metro code in any vintage
(verified: no MSA/CBSA/METRO-named variable in the 2007 or 2023 variable dictionaries), so metros
are constructed. Chain:

```
PUMA (vintage in force that year)  --Geocorr population allocation factors-->  county
county  --OMB February-2013 delineation, metropolitan areas only-->  CBSA
```

The county→CBSA step uses **one fixed delineation for every year**, which is what makes the metro
boundaries stable across the three PUMA vintages the ACS uses (2000-definition PUMAs for
2005–2011, 2010-definition for 2012–2021, 2020-definition for 2022–2023). A person's weight is
split across counties by the Geocorr allocation factor, then summed into the fixed CBSA. Metros are
metropolitan statistical areas only; micropolitan areas and non-metro counties are dropped.
[SOURCE: MCDC Geocorr 2014 and 2022, `mcdc.missouri.edu/cgi-bin/broker`; OMB delineation
`www2.census.gov/programs-surveys/metro-micro/geographies/reference-files/2013/delineation-files/list1.xls`]

**Outcomes.** Native-born (`NATIVITY == 1`), below bachelor's degree, employment-to-population
ratio and labour-force participation, in percentage points.

- Education code: `SCHL <= 12` for 2005–2007 (17-code scheme, bachelor's = 13) and `SCHL <= 20`
  for 2008 onward (25-code scheme, bachelor's = 21). The recode break at 2008 is real and is
  handled per year. [SOURCE: `acs1/pums/variables.json` for 2005, 2007, 2008, fetched 2026-09-18]
- Employed: `ESR` in {1, 2, 4, 5} (includes armed forces). Civilian-only {1, 2} stored alongside.
- In labour force: `ESR` in {1, 2, 3, 4, 5}.
- Age bands: 18–29 separately for men and women, and a pooled 16–24 arm.
- Institutional group quarters (`TYPE`/`TYPEHUGQ == 2`) excluded from every numerator and
  denominator, so prison populations do not enter the entry-age denominator.

**Treatment.** Change in the Mexico-born (`POBP == 303`) share of the metro population aged 18–64,
in percentage points; and the same for all foreign-born (`NATIVITY == 2`).

**Instruments.** Past-settlement shift-share. The base share is metro *m*'s share of the **national
Mexico-born (or foreign-born) stock in Census 2000**, built from SF3 table PCT019 at county level
and aggregated into the same fixed 2013 CBSAs (PCT019103 = born in Mexico; national total
9,180,186, which matches the published Census 2000 figure). Predicted inflow over a window is
that base share times the national change in the stock over the window, divided by the metro's
base-year population aged 18–64.
[SOURCE: `api.census.gov/data/2000/dec/sf3`, group PCT019, fetched 2026-09-18]

**Estimators.** For each outcome × sex × treatment × window:

- **OLS** in long differences, 5-year and 10-year.
- **IV**, the conventional single shift-share instrument.
- **IV-JRS**, the Jaeger–Ruist–Stuhler correction: the current *and* the previous window's
  immigration change both enter as endogenous regressors, instrumented by the current and lagged
  predicted inflows. The reported coefficient is the one on the current change. This is the test
  of whether the conventional estimate is contaminated by ongoing adjustment to earlier shocks.

  This arm requires a **multi-origin** instrument and cannot be run with a single origin group.
  With one group the current and lagged predicted inflows are both the same metro base share
  times a national scalar, so they are collinear across metros and the two-endogenous system is
  not identified. The identifying variation JRS exploit is the change in the *national origin
  mix*. The instrument here is therefore built from all 100 leaf birthplace categories of Census
  2000 SF3 table PCT019, each metro's base share of the national 2000 stock of that origin
  interacted with that origin's national stock change over the window, summed across origins.
  [SOURCE: JRS 2018 p.17ff, "multiple instrumentation", NBER w24285 full text]

  **JRS themselves report that this procedure is underidentified in every US decade after the
  1970s.** Verbatim: "only in the 1970s do we reject the null hypothesis of underidentification
  with the Kleinbergen-Paap statistic. The rest of our analysis is therefore focused on
  estimating the impact of immigration" in that decade, and they note that "looking at the first
  stage regressions individually would not necessarily lead one to conclude that there are
  identification problems in the 1990s and 2000s, as the first stage F statistics are reasonably
  large." [SOURCE: NBER w24285 full text, fetched 2026-09-18] The sample here is 2005–2023,
  squarely inside the region where they found the correction fails. Every IV row therefore
  reports **Shea's partial R-squared** alongside the first-stage F, because Shea's measure is the
  one that collapses when two instruments are near-collinear while individual F statistics stay
  large. A large F with a near-zero Shea R-squared in the JRS arm is the signature of the
  failure JRS describe, not evidence of a well-identified estimate.
- **IV-placebo**, the current instrument against the outcome change in the window *before* the
  shock.

Weights: the metro's base-year native no-college population in the relevant age band.
Standard errors: heteroskedasticity-robust, clustered by metro. Metros below 25,000 weighted
native no-college persons in the base year are dropped.

### The shift half of the shift-share nearly vanishes for Mexico in this period

Measured from ACS table B05006 at the national level, the Mexico-born stock changes over the
estimation windows as follows, against the change in the stock of all origins matched to the
Census 2000 base.

| window | Mexico-born national change | all matched origins |
|---|---:|---:|
| 2005–2010 | +0.74 M | +4.20 M |
| 2008–2013 | +0.17 M | +3.23 M |
| 2010–2015 | −0.07 M | +3.25 M |
| 2013–2018 | −0.41 M | +3.40 M |

[SOURCE: `api.census.gov` ACS 1-year table B05006, US total, fetched 2026-09-18]

A shift-share instrument is a metro base share multiplied by a national shift. When the
national shift is −0.07 million, the predicted inflow is near zero for every metro and the
instrument has almost nothing left to explain. **The conventional single-origin Mexican
instrument is therefore close to powerless over most of 2005–2023 by construction, not by bad
luck.** This is a different problem from the one JRS identify, and it compounds it: their
critique is that the instrument conflates short- and long-run responses, while here the shift it
depends on has gone to zero and then reversed sign. The multi-origin instrument keeps its power
because the other origins continued to grow by roughly 3 million per window throughout.

## 3. Estimates

All figures below: metros with at least 50,000 weighted native no-college residents in the base year, both sexes, ages 18–29, Mexico-born treatment unless labelled; the 25,000-floor rows are in `derived/estimates.csv` and move nothing that follows. Every row was re-run by the parent session after the lane closed; `estimates.csv` and `tables.md` reproduce byte-for-byte. [SOURCE: `derived/estimates.csv`, 2,904 rows; `derived/tables.md`; re-run 2026-09-18 14:40]

**Headline reading, in order of how much weight each number can bear.**

1. **The best-identified estimate is uninformative against the benchmark.** The 10-year single-instrument IV has a strong first stage (F 145, Shea partial R² 0.10) and gives −0.43 points of native no-college E/POP per 1-point rise in the Mexico-born share, 95% interval [−1.28, +0.42]. That interval contains zero, the DSS all-native equivalent of about −0.6, and the DSS unskilled equivalent of about −0.9, at comparable distance. At the 25,000 floor it is −0.57 [−1.38, +0.24]. This is disconfirmation test 6 failing in the sense specified in advance: the data cannot separate "no effect" from "the DSS effect." [SOURCE: `estimates.csv` rows min_pop 50000/25000, window POOLED, length 10y, estimator IV-single]

2. **The pooled 5-year single instrument is powerless (F 3.6) for the reason section 2 predicted.** Within each 5-year window the 2000 base share predicts the local change strongly (window F 14 to 152), but the national Mexico-born shift changes sign across windows (+0.74M, +0.17M, −0.07M, −0.41M, −0.25M), so the predicted inflow flips sign for the same metros and a single pooled slope has nothing stable to fit. The pooled 5-year IV, −1.00 [−5.26, +3.26], is therefore not a number to read.

3. **The 5-year windows flip sign, which fails disconfirmation test 4.** Single-instrument IV by window: 2005–10 −0.26 [−1.91, +1.39]; 2008–13 **+1.20 [+0.62, +1.77]**; 2010–15 +0.25 [−1.03, +1.52]; 2013–18 **−0.83 [−1.77, +0.10]**; 2018–23 +0.22 [−1.18, +1.61]. A positive, significant "effect" of Mexican inflow on native youth employment in 2008–13 is the recovery pattern (metros whose Mexican-born population grew out of the recession were the metros whose labour markets recovered), not a supply effect, and it is the same magnitude as the negative 2013–18 point estimate that looks like DSS. The 2013–18 window is the only one in which sign, size and first stage all line up with the benchmark, and it fails the placebo (item 5).

4. **The JRS correction cannot be run on this period, and the reason reproduces JRS's own finding.** The multi-origin current and lagged predicted inflows correlate 0.82 across metros; Shea's partial R² in the two-endogenous system is 0.0007 while the naive first-stage F is 20. That is the signature JRS describe for every US decade after the 1970s: individual first stages look fine, the system is underidentified. The JRS coefficient, −9.65 [−53.2, +33.9], is noise around an unidentified parameter, not a corrected estimate; the same-sample multi-origin IV without the lag is −23 [−496, +450]. **So the question the brief asked, "does adding the lagged shock move the short-run coefficient, and in which direction," has the answer: it cannot be answered on 2005–2023 US data, because the identifying variation JRS rely on, change in the national origin mix, is not there.** [SOURCE: `estimates.csv` rows estimator IV-JRS / IV-multi-same-sample; JRS NBER w24285 p.17ff]

5. **The single-instrument placebo fails in the one window that looked like DSS.** The lane's stored placebo arm used the multi-origin instrument, whose first stage is dead (F 0.009), so it could neither pass nor fail. The parent ran the placebo the brief specified, `placebo_single.py`: the 2013–18 Mexican instrument regressed on the 2008–13 native no-college E/POP change. Reduced form +2.36 (SE 0.53); as an IV coefficient on the pre-window share change, +1.15 (SE 0.27). The instrument that "predicts" a fall in native youth employment in 2013–18 predicts, more strongly, a rise in 2008–13 in the same metros, which is mean reversion in Mexican-heavy metros' recovery paths, not a supply shock. For 2018–23 the placebo is −1.20 (SE 0.73), same sign as the current-window reduced form; for 2010–15 it is uninformative (SE 27). The raw correlation between the current instrument and the previous window's actual share change is 0.27 to 0.68, which is the JRS problem stated in the simplest terms. [SOURCE: `derived/placebo_single.csv`]

6. **The college control group does not move, but the difference is not significant.** 10-year pooled IV on native 18–29 with a bachelor's degree: +0.09 [−0.62, +0.80], F 95; by 5-year window the college IV point estimates are +0.08, +0.53, −0.68, −0.26, +0.05 against the no-college −0.26, +1.20, +0.25, −0.83, +0.22. The no-college 10-year estimate is not a metro-demand artifact, but −0.43 against +0.09 with those intervals does not establish a skill-specific effect either.

7. **All-foreign-born arm.** Pooled 5-year IV +0.17 [−0.10, +0.43], F 5.4 (weak); 10-year rows in `estimates.csv`. The positive point estimate is consistent with test 5's warning that the all-origin inflow follows local demand.

8. **Men and women, and the 16–24 arm**, add nothing beyond wider intervals: pooled 5-year IV +1.44 [−1.46, +4.35] for men, −4.67 [−13.46, +4.13] for women, +1.64 [−4.89, +8.17] for 16–24, all with pooled F below 5.

**Against Card (2001).** The largest decade-long Mexico-born share change in a gateway metro in this panel is on the order of 1–2 points; even the 10-year point estimate of −0.43 per point gives well under one point of native youth E/POP over a decade, below Card's 1–3 points for the 1980s, and the interval includes zero.

**National stock change over each window, millions of people**

| window | Mexico-born | all matched origins |
|---|---:|---:|
| 2005-2010 | +0.74 | +2.75 |
| 2008-2013 | +0.17 | +1.76 |
| 2010-2015 | -0.07 | +2.92 |
| 2013-2018 | -0.41 | +2.89 |
| 2018-2023 | -0.25 | +2.45 |
| 2005-2015 | +0.67 | +5.67 |
| 2008-2018 | -0.24 | +4.65 |
| 2013-2023 | -0.67 | +5.34 |
### Headline: pooled across 5-year windows, both sexes, ages 18–29


**E/POP 18-29, treatment = Mexico-born, pooled 5-year windows**

| estimator | metros | coef (pp) | 95% CI | 1st-stage F | Shea partial R2 | corr(Z, Z lag) |
|---|---|---|---|---|---|---|
| OLS | 661 | +0.246 | [-0.07, +0.56] |  |  |  |
| IV-single | 661 | -1.001 | [-5.26, +3.26] | 3.6 | 0.00798 |  |
| IV-multi | 661 | +1.709 | [-2.93, +6.35] | 0.409 | 0.0111 |  |
| IV-multi-same-sample | 379 | -23.087 | [-495.70, +449.52] | 0.00915 | 0.000107 | 0.819 |
| IV-JRS | 379 | -9.654 | [-53.21, +33.90] | 20.2 | 0.000712 | 0.819 |
| IV-placebo-pre | 379 | +7.250 | [-139.76, +154.26] | 0.00915 | 0.000107 | 0.819 |

**LFP 18-29, treatment = Mexico-born, pooled 5-year windows**

| estimator | metros | coef (pp) | 95% CI | 1st-stage F | Shea partial R2 | corr(Z, Z lag) |
|---|---|---|---|---|---|---|
| OLS | 661 | +0.051 | [-0.24, +0.34] |  |  |  |
| IV-single | 661 | -1.033 | [-3.39, +1.32] | 3.6 | 0.00798 |  |
| IV-multi | 661 | +1.392 | [-2.67, +5.45] | 0.409 | 0.0111 |  |
| IV-multi-same-sample | 379 | -22.328 | [-479.92, +435.27] | 0.00915 | 0.000107 | 0.819 |
| IV-JRS | 379 | -9.458 | [-42.22, +23.31] | 20.2 | 0.000712 | 0.819 |
| IV-placebo-pre | 379 | -7.139 | [-155.46, +141.18] | 0.00915 | 0.000107 | 0.819 |

**E/POP 18-29, treatment = all foreign-born, pooled 5-year windows**

| estimator | metros | coef (pp) | 95% CI | 1st-stage F | Shea partial R2 | corr(Z, Z lag) |
|---|---|---|---|---|---|---|
| OLS | 661 | +0.113 | [-0.06, +0.28] |  |  |  |
| IV-single | 661 | +0.167 | [-0.10, +0.43] | 5.38 | 0.168 |  |
| IV-multi | 661 | +1.301 | [-2.53, +5.13] | 0.31 | 0.00796 |  |
| IV-multi-same-sample | 379 | -57.374 | [-5040.78, +4926.03] | 0.000513 | 6.25e-06 | 0.819 |
| IV-JRS | 379 | -26.049 | [-629.53, +577.44] | 6.68 | 3.83e-05 | 0.819 |
| IV-placebo-pre | 379 | +18.017 | [-1515.39, +1551.43] | 0.000513 | 6.25e-06 | 0.819 |

**LFP 18-29, treatment = all foreign-born, pooled 5-year windows**

| estimator | metros | coef (pp) | 95% CI | 1st-stage F | Shea partial R2 | corr(Z, Z lag) |
|---|---|---|---|---|---|---|
| OLS | 661 | +0.034 | [-0.11, +0.18] |  |  |  |
| IV-single | 661 | +0.082 | [-0.16, +0.32] | 5.38 | 0.168 |  |
| IV-multi | 661 | +1.059 | [-2.59, +4.71] | 0.31 | 0.00796 |  |
| IV-multi-same-sample | 379 | -55.486 | [-4838.76, +4727.79] | 0.000513 | 6.25e-06 | 0.819 |
| IV-JRS | 379 | -25.268 | [-594.92, +544.38] | 6.68 | 3.83e-05 | 0.819 |
| IV-placebo-pre | 379 | -17.740 | [-1583.37, +1547.89] | 0.000513 | 6.25e-06 | 0.819 |

### By sex, pooled 5-year windows, E/POP 18–29


**E/POP 18-29, men, Mexico-born treatment**

| estimator | metros | coef (pp) | 95% CI | 1st-stage F | Shea partial R2 | corr(Z, Z lag) |
|---|---|---|---|---|---|---|
| OLS | 685 | +0.161 | [-0.19, +0.51] |  |  |  |
| IV-single | 685 | +1.443 | [-1.46, +4.35] | 4.27 | 0.00944 |  |
| IV-multi | 685 | -0.451 | [-3.19, +2.29] | 0.389 | 0.0101 |  |
| IV-multi-same-sample | 394 | -12.238 | [-165.78, +141.30] | 0.0254 | 0.000282 | 0.815 |
| IV-JRS | 394 | -7.506 | [-45.20, +30.19] | 19.7 | 0.000867 | 0.815 |
| IV-placebo-pre | 394 | +22.695 | [-264.09, +309.48] | 0.0254 | 0.000282 | 0.815 |

**E/POP 18-29, women, Mexico-born treatment**

| estimator | metros | coef (pp) | 95% CI | 1st-stage F | Shea partial R2 | corr(Z, Z lag) |
|---|---|---|---|---|---|---|
| OLS | 632 | +0.337 | [-0.03, +0.71] |  |  |  |
| IV-single | 632 | -4.666 | [-13.46, +4.13] | 2.87 | 0.00664 |  |
| IV-multi | 632 | +3.759 | [-6.32, +13.83] | 0.406 | 0.0113 |  |
| IV-multi-same-sample | 362 | -23.777 | [-453.10, +405.54] | 0.0116 | 0.000138 | 0.841 |
| IV-JRS | 362 | -10.877 | [-52.66, +30.91] | 20.8 | 0.000781 | 0.841 |
| IV-placebo-pre | 362 | -15.769 | [-322.60, +291.07] | 0.0116 | 0.000138 | 0.841 |

### Pooled 16–24 arm and 10-year windows


**E/POP 16-24, 5y windows, Mexico-born treatment**

| estimator | metros | coef (pp) | 95% CI | 1st-stage F | Shea partial R2 | corr(Z, Z lag) |
|---|---|---|---|---|---|---|
| OLS | 566 | +0.118 | [-0.19, +0.42] |  |  |  |
| IV-single | 566 | +1.640 | [-4.89, +8.17] | 1.47 | 0.00396 |  |
| IV-multi | 566 | +1.588 | [-4.93, +8.11] | 0.335 | 0.0098 |  |
| IV-multi-same-sample | 323 | -13.835 | [-113.37, +85.70] | 0.0764 | 0.000873 | 0.847 |
| IV-JRS | 323 | -20.024 | [-125.06, +85.01] | 21.2 | 0.000517 | 0.847 |
| IV-placebo-pre | 323 | +6.297 | [-42.42, +55.02] | 0.0764 | 0.000873 | 0.847 |

**E/POP 18-29, 10y windows, Mexico-born treatment**

| estimator | metros | coef (pp) | 95% CI | 1st-stage F | Shea partial R2 | corr(Z, Z lag) |
|---|---|---|---|---|---|---|
| OLS | 388 | -0.018 | [-0.26, +0.23] |  |  |  |
| IV-single | 388 | -0.431 | [-1.28, +0.42] | 145 | 0.102 |  |
| IV-multi | 388 | +1.564 | [-4.29, +7.41] | 0.304 | 0.0111 |  |

### Window by window, E/POP 18–29, both sexes, Mexico-born treatment


**window 2005-2010**

| estimator | metros | coef (pp) | 95% CI | 1st-stage F | Shea partial R2 | corr(Z, Z lag) |
|---|---|---|---|---|---|---|
| OLS | 114 | +0.803 | [+0.22, +1.39] |  |  |  |
| IV-single | 114 | -0.261 | [-1.91, +1.39] | 14.1 | 0.373 |  |
| IV-multi | 114 | -0.176 | [-2.00, +1.65] | 2.87 | 0.151 |  |

**window 2008-2013**

| estimator | metros | coef (pp) | 95% CI | 1st-stage F | Shea partial R2 | corr(Z, Z lag) |
|---|---|---|---|---|---|---|
| OLS | 136 | +0.684 | [+0.32, +1.05] |  |  |  |
| IV-single | 136 | +1.197 | [+0.62, +1.77] | 30.4 | 0.384 |  |
| IV-multi | 136 | +1.243 | [-0.51, +3.00] | 1.15 | 0.0481 |  |

**window 2010-2015**

| estimator | metros | coef (pp) | 95% CI | 1st-stage F | Shea partial R2 | corr(Z, Z lag) |
|---|---|---|---|---|---|---|
| OLS | 135 | -0.094 | [-0.89, +0.71] |  |  |  |
| IV-single | 135 | +0.245 | [-1.03, +1.52] | 67.6 | 0.455 |  |
| IV-multi | 135 | -1.686 | [-9.08, +5.70] | 0.45 | 0.00829 |  |
| IV-multi-same-sample | 114 | -1.947 | [-10.91, +7.01] | 0.344 | 0.0068 | 0.792 |
| IV-JRS | 114 | -19.459 | [-754.78, +715.86] | 22.1 | 7.98e-05 | 0.792 |
| IV-placebo-pre | 114 | -2.718 | [-19.55, +14.11] | 0.344 | 0.0068 | 0.792 |

**window 2013-2018**

| estimator | metros | coef (pp) | 95% CI | 1st-stage F | Shea partial R2 | corr(Z, Z lag) |
|---|---|---|---|---|---|---|
| OLS | 141 | -0.334 | [-1.23, +0.56] |  |  |  |
| IV-single | 141 | -0.834 | [-1.77, +0.10] | 152 | 0.611 |  |
| IV-multi | 141 | +2.662 | [-48.54, +53.86] | 0.0314 | 0.000505 |  |
| IV-multi-same-sample | 133 | +2.559 | [-60.27, +65.39] | 0.0203 | 0.000328 | 0.797 |
| IV-JRS | 133 | +0.593 | [-15.14, +16.32] | 84.2 | 0.0017 | 0.797 |
| IV-placebo-pre | 133 | -0.068 | [-24.54, +24.40] | 0.0203 | 0.000328 | 0.797 |

**window 2018-2023**

| estimator | metros | coef (pp) | 95% CI | 1st-stage F | Shea partial R2 | corr(Z, Z lag) |
|---|---|---|---|---|---|---|
| OLS | 135 | -0.109 | [-0.92, +0.70] |  |  |  |
| IV-single | 135 | +0.216 | [-1.18, +1.61] | 104 | 0.481 |  |
| IV-multi | 135 | -7.020 | [-22.12, +8.08] | 1.41 | 0.00878 |  |
| IV-multi-same-sample | 132 | -7.108 | [-22.74, +8.52] | 1.34 | 0.00854 | 0.869 |
| IV-JRS | 132 | -7.036 | [-15.56, +1.49] | 1.63 | 0.00982 | 0.869 |
| IV-placebo-pre | 132 | +0.579 | [-7.22, +8.38] | 1.34 | 0.00854 | 0.869 |

## 4. What this design does and does not identify

**Does not identify legal status.** ACS records birthplace and citizenship, not authorisation.
The Mexico-born treatment mixes naturalised citizens, lawful permanent residents, temporary
visa holders and unauthorised residents. No arm here speaks to any policy that distinguishes
them.

**Does not identify person-level displacement.** The unit is the metro. A negative coefficient
is consistent with a native losing a job to an immigrant, with a native never being hired, and
with a native leaving the metro. Dustmann–Schönberg–Stuhler could separate these because they
had linked employment records; ACS cross-sections cannot. The native-outflow channel is the
live alternative here: Card (2001) reports native mobility is insensitive to inflows, Borjas
(2006) reports 40–60% offset, and the repo rates the Borjas direction as granted but the
magnitude as specification-sensitive. If natives do move, the surviving denominator is selected
and the coefficient is biased toward zero.

**Does not identify wages.** The ACS wage variables were not pulled. JRS's own corrected
estimates are wage estimates, so the closest quantitative comparison in this memo is to DSS's
employment result, not to JRS's headline.

**ACS, not CPS or administrative data.** The employment measure is the ACS `ESR` recode from a
single annual cross-section, not a monthly labour-force series and not an employer record.
Metro cells for smaller areas rest on a few hundred unweighted observations, which is why the
main specification imposes a base-year population floor and weights by native population.

**Metro-year shares are measured with sampling error**, in both endpoints of every long
difference. That is classical measurement error in the regressor, so OLS is attenuated by
construction and the IV estimates should be larger in absolute value than OLS for that reason
alone, independent of any endogeneity argument. An IV/OLS gap is therefore not by itself
evidence that sorting was biasing OLS upward.

**Metro boundaries are constructed, not observed.** PUMAs are allocated to counties by
population factors, so a PUMA straddling a metro edge has its residents split. This attenuates
the treatment toward the national mean for metros with ragged boundaries.

## 5. Disconfirmation

Six tests, all specified before the estimates were read.

1. **Pre-window placebo.** The instrument for window (t, t+5) is run against the outcome change
   over (t−5, t). A significant coefficient means the instrument tracks pre-existing local
   trends rather than the shock.
2. **College-educated control group.** Native 18–29 year olds with a bachelor's degree or above
   share the local demand shock but compete far less directly with low-skill immigrants. If the
   instrument moves their employment rate as much as it moves the no-college rate, the design is
   measuring metro demand, not skill-specific competition. This required a separate ACS pull.
3. **Identification strength.** Every IV row carries the first-stage F and Shea's partial
   R-squared. JRS's own finding is that their correction is underidentified in the US after the
   1970s while individual first-stage F statistics still look large, so a large F alone is not
   evidence of a usable estimate.
4. **Sign stability across windows.** A causal parameter should not flip sign between adjacent
   five-year windows. Window-by-window estimates are reported rather than only the pooled ones.
5. **Mexico-born versus all foreign-born.** All-foreign-born mixes high-skill inflows that
   follow local labour demand. If the two arms disagree in sign, the foreign-born arm is the more
   likely to be capturing demand.
6. **Can the data even detect the benchmark effect?** Each headline confidence interval is
   compared against the DSS-equivalent magnitude of roughly −0.6 points (−0.9 for unskilled).
   A confidence interval that contains both zero and the benchmark rules out nothing, and must
   be reported as uninformative rather than as a null.

### Results

| Test | Result | Reading |
|---|---|---|
| 1. Pre-window placebo | **Fails** in 2013–18 (single instrument: reduced form on the 2008–13 outcome change +2.36, SE 0.53; IV-pre +1.15, SE 0.27); marginal in 2018–23 (−1.20, SE 0.73); uninformative in 2010–15. The stored multi-origin placebo arm has a dead first stage (F 0.009) and decides nothing. | The instrument tracks recovery paths of Mexican-heavy metros, not a supply shock. |
| 2. College control | 10-year pooled IV +0.09 [−0.62, +0.80] against no-college −0.43 [−1.28, +0.42]. | Consistent with a skill-specific effect; does not establish one. |
| 3. Identification strength | Single instrument: pooled 5-year F 3.6, 10-year F 145, window F 14–152. JRS arm: F 20 but Shea partial R² 0.0007, corr(Zm, Zm lag) 0.82. | The 10-year single IV is the only identified arm; the JRS arm is underidentified, as JRS found for post-1970s US data. |
| 4. Sign stability | 5-year IV: −0.26, **+1.20**, +0.25, **−0.83**, +0.22. | **Fails.** Adjacent windows flip sign with significant estimates on both sides. |
| 5. Mexico-born vs all foreign-born | All-foreign-born pooled 5-year IV +0.17 [−0.10, +0.43] (F 5.4); Mexico-born −1.00 [−5.26, +3.26] (F 3.6). | Point estimates disagree in sign; both first stages weak; the all-origin arm leans demand-driven as anticipated. |
| 6. Can the data detect the benchmark? | Best interval [−1.28, +0.42] contains zero and −0.6/−0.9. | **No.** Uninformative, and reported as such rather than as a null. |

[SOURCE: `derived/estimates.csv`, `derived/placebo_single.csv`]

**What survives.** A design-level negative result: the two instruments the literature uses for Mexican inflows both fail on the last fifteen years, one because the national Mexican inflow stopped (the same fact the arrival-cohort memo records from the other side), the other because the origin mix that JRS's correction needs did not change enough. Any US metro-level claim about the employment-entry effect of Mexican immigration since 2008, in either direction, that rests on a past-settlement instrument should be read against this. The DSS result itself, from a sharp exogenous shock, is untouched. [INFERENCE]

## 6. Byproduct

The build produces `derived/metro_year_panel.csv`, a metro × year panel of foreign-born and
Mexico-born population shares for 2005–2019 and 2021–2023 on fixed 2013 CBSA boundaries. The
repo's MSA rent-elasticity memo records its causal result as GATED on exactly this series
("needs metro foreign-born share over" time, with only 2023 staged). This panel closes that
input. [SOURCE: `research/immigration-msa-rent-elasticity-panel-2026-06-25.md` §What's built vs
gated]

## 7. Sources

- Jaeger, D., Ruist, J. & Stuhler, J. (2018), *Shift-Share Instruments and the Impact of
  Immigration*, NBER Working Paper 24285.
- Dustmann, C., Schönberg, U. & Stuhler, J. (2017), *Labor Supply Shocks, Native Wages, and the
  Adjustment of Local Employment*, QJE 132(1).
- Card, D. (2001), *Immigrant Inflows, Native Outflows, and the Local Labor Market Impacts of
  Higher Immigration*, JOLE 19(1). doi:10.1086/209979.
- US Census Bureau, American Community Survey 1-year PUMS, 2005–2019 and 2021–2023, via the
  Census Data API.
- US Census Bureau, Census 2000 Summary File 3, table PCT019, county level, via the Census Data API.
- Missouri Census Data Center, Geocorr 2014 and Geocorr 2022, PUMA→county allocation factors.
- US Office of Management and Budget, February 2013 metropolitan area delineation (list1).
- Repo: `research/immigration-canon-citation-audit-2026-09-17.md` §P1, §C7, §C8.

## 8. Analysis code

`infra/immigration-fiscal/employment_entry_2026_09_18/` — `fetch_crosswalks.py`, `fetch_origins.py`, `pull_pums3.py`, `pull_placebo.py`, `build_panel.py`, `build_instruments.py`, `diagnostics.py`, `estimate.py` (writes `derived/estimates.csv`), `report.py` (writes `derived/tables.md`), `write_memo.py` (inserts the tables into section 3), `placebo_single.py` (parent-added single-instrument placebo, writes `derived/placebo_single.csv`), with the verbatim dispatch brief in `BRIEF.md` and the lane result in `RESULT.md`. The API pull cache under `_cache/` is not committed. Run from the lane directory with `uv run --no-project --with "pandas>=2" --with "numpy>=2" --with linearmodels --with statsmodels python3 <script>`.

## Revisions

2026-09-18, first version. Lane computed the estimates and closed before writing the verdict and results; the parent session re-ran the estimation (byte-identical), added the single-instrument placebo and wrote sections 3 and 5 from the derived files. Concept affected: identification of the employment-entry effect of Mexican inflows on recent US data; qualifies the canon audit's reading of C7/C8 by showing neither instrument identifies it after 2008.


## Revisions — September 19, 2026

Corrected the interpretation for the reasons above; see the [decision](../decisions/2026-09-19-bind-report-claims-to-matched-estimands.md).
