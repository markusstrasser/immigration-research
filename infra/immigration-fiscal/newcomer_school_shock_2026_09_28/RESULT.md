**Verdict:** Staff and money followed the newcomer pupils only partly and with a lag, and the other pupils' scores
barely moved.

- **Resources.** Per 10 pp of newcomer share:
  - In NYC, teachers and spending rose about half as fast as enrollment from the second year, and K-5 classes
    grew by about one pupil.
  - Chicago's teachers rose at about 0.6 of enrollment.
  - Denver added no teachers for two years, then caught up by fall 2025.
- **Never-English-learner scores.** Per 10 pp:
  - NYC with shelter-routed exposure: +0.014 SD in ELA and −0.005 SD in math; the 95% intervals are
    [−0.012, +0.040] and [−0.034, +0.024].
  - Denver: −0.016 and −0.012 SD, not significant.
  - Chicago ELA: about −0.035 SD in the first surge year only.
- **Identification.** This is a within-district design. It identifies local exposure, not district-wide costs or
  reallocation.

# Schools after the 2022–2024 newcomer surge: NYC, Chicago, Denver

Lane brief: `BRIEF.md` (68a5d0a). Source quotes: `reads/nyc_sources.md`, `reads/chicago_sources.md`,
`reads/denver_sources.md`, `reads/scale_sd_sources.md`.

- The Chicago panel, the Denver panel and the scale SDs were built by three workers. Here they were
  spot-checked for coverage, totals and group definitions, not re-derived.
- The NYC panel and the analysis (`build_nyc.py`, `extract_nysed_src.py`, `analyze.py`) were written here.
- Numbers are tagged by source. Model output is `[CALCULATION]` from `analyze.py`, and readings of it are
  `[INFERENCE]`.

## Task 1. Exposure

Done 2026-09-28. The school × year exposure panels exist for all three cities: NYC 2017-18 to 2025-26, Chicago
2016-17 to 2024-25, Denver 2016-17 to 2025-26.
The panels are `derived/nyc_schools.csv`, `derived/chicago_schools.csv` and `derived/denver_schools.csv`; the
per-school intensity is in `derived/exposure_by_school.csv`. Years below are spring years (2023 = 2022-23).

**What counts newcomers, by city.** No city publishes a clean newcomer count by school for every year, so each
city's count is the closest published series. The intensity is the same in all three:
X = (count in the October count of 2024 − count in the October count of 2021) / enrollment in 2021-22, for
schools with at least 100 pupils in 2021-22. The window runs to the October 2024 count because each city's series
peaks there.

| City | Count used | Citywide count, 2022 → 2023 → 2024 → 2025 (→ 2026) | Schools | X: median / p90 / p99 | Schools with X ≥ 0.10 |
|---|---|---|---|---|---|
| NYC | English language learners, demographic snapshot (Oct 31 register; ELL status as of June 30), districts 1–32 | 127,462 → 127,465 → 141,168 → 144,921 → 128,106 | 1,507 | 0.013 / 0.112 / 0.320 | 12.2% |
| Chicago | English learners, CPS 20th-day membership | 69,268 → 72,029 → 79,833 → 88,807 | 565 | 0.032 / 0.182 / 0.393 | 25.1% |
| Denver | CDE "Immigrant" pupils: not born in a US state, at most three full years in US schools (Oct 1 count) | 2,791 → 3,283 → 5,643 → 9,265 → 8,069 | 185 | 0.049 / 0.177 / 0.418 | 27.6% |

[DATA: `derived/nyc_schools.csv`, `derived/chicago_schools.csv`, `derived/denver_schools.csv`, summed by year]
[CALCULATION: `analyze.py` → `derived/exposure_summary.csv`]

- The enrollment-weighted mean of X is 0.021 in NYC, 0.060 in Chicago and 0.074 in Denver.
  [CALCULATION: `derived/analysis_audit.json`]
- **NYC's ELL count is a net count.** It stayed flat from 2021-22 to 2022-23, although the Project Open Arms
  memo had funded 5,851 first-time entrants in temporary housing by October 2022. New arrivals offset exits
  (reclassification and departures). Most 2022-23 arrivals came after the October 31 register: a DOE email
  quoted by a parent blog counts "13,248 asylum seeker students across 608 schools" as of March 18, 2023
  [SOURCE: familiesfornyc.com/blog/dropenrollment, 2023-05-18; secondary, the email itself is not public]. The
  count shows the surge from the October 2023 register.
- **NYC shelter-routed counts from the allocation memos:**
  - SAM 65 (FY2023, 2022-10-31): $2,000 per first-time entrant in temporary housing enrolled since
    July 2, 2022, for schools with six or more. It paid $11,702,000 to 369 schools, which is 5,851 students.
    [DATA: `_cache/nyc/sams/FY2023_SAM065_T01_wayback20221031.xlsx`] The live memo withdrew the school table
    "due to privacy and security concerns"; the table here is the Wayback copy of the day it was posted
    [SOURCE: `reads/nyc_sources.md`].
  - SAM 90 (FY2024, 2024-03-07): about $50 per first-time admit in temporary housing, July 2023 to February
    2024, with extra weight for 2024 entrants and a $600 floor. It paid $1,500,000 to 1,255 schools. Divided by
    $50, this gives a weighted count, not a head count.
  - Across schools, one SAM 65 student goes with 0.68 more ELLs between the 2021 and 2022 October registers.
    One SAM 90 weighted student goes with 0.43 more ELLs between the 2022 and 2023 registers. The correlation of X
    with the combined memo intensity is 0.43. [CALCULATION: `analyze.py`; scratch check of the same panel]
- **Chicago school-level newcomer counts** exist only for arrivals after the 20th day of SY2023-24, from the
  FY2025 budget: 3,250 students in 149 of 497 district-run schools (`reads/chicago_sources.md`).
- **Denver:** DPS publishes newcomer totals only for the district. The CDE immigrant count is the school-level
  series. Its blank cells mean 0–3 pupils and are set to 0 here.

## Task 2. Resources

Done 2026-09-28. Staff and spending rose with the newcomer pupils, but only partly and with a lag. In New York,
teachers and spending grew about half as fast as enrollment. Chicago's teachers grew at about 0.6 of
enrollment. Denver added no teachers for two years and caught up in the third.

**Design.** Each outcome is regressed on the intensity X interacted with year dummies, with school and year fixed
effects. The base year is 2021-22, schools are weighted by 2021-22 enrollment, and SEs are clustered by school.
[CALCULATION: `analyze.py` → `derived/estimates.csv`, block `resources`]

Resources followed pupils fully if the log change in staff or spending matched the log change in enrollment in
the same year. The ratio column below is the teacher coefficient divided by the enrollment coefficient.

Coefficients per 10 pp of X, relative to 2021-22; SEs are in `derived/estimates.csv`.

| City | Year | Enrollment (log) | Teachers (log) | Teachers ÷ enrollment | Spending (log) | Pupils per teacher | Class size |
|---|---|---|---|---|---|---|---|
| NYC | 2022-23 | +0.023 (0.003) | +0.007 (0.005) | 0.3 | +0.011 (0.003) | +0.20 (0.05) | K-5 +0.40 (0.10) |
| NYC | 2023-24 | +0.069 (0.005) | +0.034 (0.006) | 0.5 | +0.034 (0.005) | +0.43 (0.06) | K-5 +1.11 (0.13) |
| NYC | 2024-25 | +0.095 (0.005) | +0.048 (0.008) | 0.5 | +0.055 (0.006) | +0.55 (0.10) | K-5 +0.93 (0.12) |
| NYC | 2025-26 | +0.079 (0.007) | – | – | – | – | K-5 +0.59 (0.15) |
| Chicago | 2022-23 | +0.015 (0.004) | +0.012 Sep, +0.013 Mar | 0.8–0.9 | site +0.092 (0.036) | – | +0.65 (0.11) |
| Chicago | 2023-24 | +0.044 (0.005) | +0.026 Sep, +0.028 Mar | 0.6 | site +0.030 (0.008) | – | +0.95 (0.17) |
| Chicago | 2024-25 | +0.065 (0.006) | +0.038 Sep, +0.038 Mar | 0.6 | site +0.041 (0.008) | – | +0.83 (0.17) |
| Denver | 2022-23 | +0.007 (0.007) | −0.013 (0.008) | – | site −0.057 (0.018) | +0.27 (0.12) | – |
| Denver | 2023-24 | +0.033 (0.009) | 0.000 (0.010) | 0.0 | site −0.037 (0.020) | +0.49 (0.10) | – |
| Denver | 2024-25 | +0.060 (0.010) | +0.023 (0.012) | 0.4 | site +0.012 (0.022) | +0.53 (0.13) | – |
| Denver | 2025-26 | +0.048 (0.014) | +0.053 (0.013) | 1.1 | – | −0.06 (0.14) | – |

Baselines for 2021-22 [CALCULATION: scratch check on the derived panels]:

- NYC: 12.3 pupils per teacher; K-5 classes average 21.1; median spending per pupil $20,648.
- Chicago: classes average 23.2.
- Denver: 14.7 pupils per teacher.

Sources for each column:

- **NYC:** snapshot enrollment; NYSED teacher counts and total spending; own pupil-teacher ratio; K-5 average
  class size from the February (updated) reports.
- **Chicago:** CPS 20th-day enrollment; CPS roster teacher FTE on September 30 and March 31; ISBE site-based
  spending; ISBE average class size.
- **Denver:** CDE October membership, teacher FTE and pupil-teacher ratio; ESSA site spending.

What the lag looks like:

- **NYC.**
  - In 2022-23, teachers rose 0.3 as fast as pupils. From 2023-24 on they rose about half as fast.
  - Class sizes and pupils per teacher absorbed the rest: K-5 classes grew about one pupil per 10 pp of X.
  - Spending rose about half as fast as enrollment, so spending per pupil fell per 10 pp of X by 1.3% in 2022-23,
    3.9% in 2023-24 and 4.5% in 2024-25.
  - The 2023-24 reporting break is described in `reads/nyc_sources.md` §4. If the break is allowed to load on
    2021-22 spending per pupil, the fall is 1.2%, 2.5% and 3.2%, and total spending follows enrollment at
    0.6–0.74.
  - The estimates hold with community-district × year effects: teachers +0.006, +0.033, +0.046; enrollment +0.021,
    +0.065, +0.091.
  - Classes did not grow more during the year in high-X schools. In 2023-24 the November-to-June change in K-5
    class size was +0.09 per 10 pp (SE 0.10).
- **The dedicated newcomer money was small.**
  - SAM 65 paid $2,000 per shelter entrant: $11.7m, "cannot be used to hire full-time staff".
  - SAM 90 paid about $50 per entrant: $1.5m.
  - Most of the money came through the normal register-based formula, as SAM 85 FY2023 states: "Schools with
    weighted register increases will receive the full balance of their mid-year adjustment through the usual
    process" (`reads/nyc_sources.md` §3).
- **Chicago.**
  - Teachers kept pace in 2022-23 at 0.8–0.9, then rose at 0.6 of enrollment.
  - The March roster matches the September one, so there was no mid-year staffing response beyond the fall's.
  - Site spending jumped in 2022-23 (+0.092, SE 0.036), then rose at 0.6–0.7 of enrollment.
  - Class sizes rose 0.7–1.0 pupil per 10 pp. The class-size pre-trend fails, however (Wald p = 0.004).
    [CALCULATION: `derived/analysis_audit.json`]
- **Denver.**
  - The receiving schools were shrinking before the surge. From 2018-19 to 2021-22 they lost 6.3% of enrollment
    and 6.3% of teachers relative to other schools per 10 pp. The pre-trend Wald p is 0.009 for enrollment and
    0.001 for teachers. DPS placed newcomers where there were seats. [INFERENCE]
  - After 2021-22 enrollment turned up. Teachers stayed flat through 2023-24, and pupils per teacher rose by 0.5.
  - Staffing caught up by fall 2025: +5.3% teachers against +4.8% pupils, with pupils per teacher back at baseline.
  - Site spending per pupil fell 4.6–6.8% per 10 pp in 2022-23 to 2024-25.
- **NYC with the shelter-routed intensity.** The SAM 65 + SAM 90 intensity (Z) says little about the response.
  Schools with shelter entrants had been shrinking: enrollment was +4.3% and spending +2.6% per 10 pp in 2018-19
  relative to 2021-22. After the surge their enrollment recovered part of that loss (+2.6–2.7% in 2023-24 and
  2024-25), while spending fell further (−1.8% and −1.2%).

## Task 3. Achievement of other students

Done 2026-09-28. In receiving schools, the scores of students who were never English learners did not fall by
more than a few hundredths of an SD per 10 pp of newcomer share. In every city the 95% intervals of the main
rows exclude −0.07 SD per 10 pp, the smallest of the system-level estimates in the operator answer of 01:44 (−0.07
to −0.14). The only
significant negative is Chicago ELA in 2022-23, at about −0.035 SD. NYC's ELL-based estimates have a failed
pre-trend; its shelter-routed estimates do not.

**Design.**
- Rows are school × grade (3–8) × year. Fixed effects are school × grade and grade × year.
- NYC and Denver outcomes are mean scale scores standardized by the statewide student-level SD for that grade,
  subject and year (`derived/scale_sd.csv`). SD-unit models stop at 2025 in NYC, where no 2026 technical report
  exists, and at 2026 in Denver.
- Weights are the 2021-22 number tested. SEs are clustered by school. The base year is 2021-22.
- The pre-period is 2017-18 and 2018-19 in NYC. In Denver it is 2018-19 and 2020-21 for never-EL, and 2016-17 to
  2020-21 for not-EL.
- Chicago publishes no never-EL or non-EL results. Non-EL is ISBE all-students minus EL at school level, in
  percent proficient, for 2018, 2019 and 2021–2023. Nothing comparable exists for 2024, and 2025 uses new cut
  scores (`reads/chicago_sources.md`).

[CALCULATION: `analyze.py` → `derived/estimates.csv`, block `achievement`; Wald tests in `derived/analysis_audit.json`]

Per 10 pp of X, with SE:

| City, group, subject | Pre-period (each year vs 2021-22) | Pre-trend p | 2022-23 | 2023-24 | 2024-25 | 2025-26 | Pooled post |
|---|---|---|---|---|---|---|---|
| NYC never-ELL ELA, SD | −0.024 (0.008), −0.017 (0.008) | 0.009 | −0.004 (0.007) | −0.012 (0.009) | −0.011 (0.010) | – | +0.005 (0.008) |
| NYC never-ELL math, SD | −0.030 (0.009), −0.023 (0.009) | 0.005 | −0.008 (0.008) | −0.028 (0.009) | −0.017 (0.011) | – | +0.000 (0.009) |
| NYC never-ELL ELA, SD, shelter-routed Z (reduced form) | +0.001 (0.008), +0.005 (0.007) | 0.52 | +0.002 (0.006) | +0.008 (0.007) | +0.018 (0.009) | – | +0.007 (0.007) |
| NYC never-ELL math, SD, shelter-routed Z (reduced form) | +0.011 (0.009), +0.010 (0.008) | 0.40 | −0.001 (0.007) | −0.001 (0.009) | +0.016 (0.011) | – | −0.003 (0.008) |
| NYC never-ELL ELA, SD, X instrumented by Z | +0.001 (0.015), +0.010 (0.014) | – | +0.004 (0.012) | +0.015 (0.013) | +0.033 (0.017) | – | +0.014 (0.013) |
| NYC never-ELL math, SD, X instrumented by Z | +0.020 (0.018), +0.019 (0.015) | – | −0.001 (0.013) | −0.002 (0.016) | +0.029 (0.023) | – | −0.005 (0.015) |
| Denver never-EL ELA, SD | +0.018 (0.021), +0.002 (0.039) | 0.68 | −0.014 (0.015) | −0.019 (0.018) | −0.004 (0.019) | +0.006 (0.021) | −0.016 (0.019) |
| Denver never-EL math, SD | +0.028 (0.026), −0.052 (0.038) | 0.05 | −0.013 (0.013) | −0.004 (0.020) | −0.006 (0.022) | +0.001 (0.024) | −0.012 (0.023) |
| Chicago non-EL ELA, pp proficient | −0.11 (0.62), +0.02 (0.62), +0.31 (0.45) | 0.88 | −1.19 (0.38) | – | – | – | −1.24 (0.39) |
| Chicago non-EL math, pp proficient | −0.43 (0.45), −0.47 (0.43), +0.08 (0.34) | 0.73 | −0.25 (0.27) | – | – | – | −0.05 (0.29) |

Sample sizes [DATA: `derived/estimates.csv`]:

- NYC: 19,144 school-grade-years, 3,609 school-grades, 1,098 schools.
- Denver: 2,237 school-grade-years, 403 school-grades, 134 schools.
- Chicago: 1,437 school-years, 288 elementary schools.

**Reading the NYC rows.**

- The ELL-growth intensity X fails the pre-trend test.
  - Schools that later gained ELLs were improving relative to other schools by about 0.006–0.0075 SD per 10 pp
    per year from 2017-18 to 2021-22.
  - Measured against 2021-22 alone, never-ELL scores dipped by 0.01–0.03 SD per 10 pp after the surge.
  - Measured against the whole pre-period, they did not dip: pooled +0.005 and +0.000.
  - If the 2017-18 to 2021-22 trend is extended through the surge, the deviations are larger:
    - ELA −0.011, −0.025 (0.011), −0.029 (0.012);
    - math −0.015, −0.042 (0.011), −0.039 (0.013).
    Extending a trend that runs through the pandemic years is an assumption, not a measurement.
  - Community-district × year effects and 2021-22 covariates × year leave the pattern unchanged: pre-trend
    p 0.02 and 0.09, and 0.013 and 0.034. The covariates are ELL share, Economic Need Index and the 2019–2022
    enrollment change.
- The shelter-routed intensity has no pre-trend, including with district × year effects (p 0.94 and 0.34).
  - It gives zero to slightly positive effects.
  - It is Z = (SAM 65 entrants + SAM 90 weighted entrants above the $600 floor) / 2021-22 enrollment.
  - Instrumenting X with Z gives pooled post effects of +0.014 (0.013) for ELA and −0.005 (0.015) for math. The
    95% intervals are [−0.012, +0.040] and [−0.034, +0.024]. The first-stage F is 46 and 40.
  - Placement by shelter location is the brief's premise, so this is the most credible NYC row. It uses only the
    part of the inflow that the two memos record.
- **Composition.** Never-ELL test takers per school-grade did not fall with X after the surge. The change was
  between −0.009 and +0.002 log points per 10 pp; the pre-trend p is 0.03 and 0.04. No flight shows up in
  who took the test.
- **Scale points.** The same NYC X rows in scale points, including 2025-26, give math −0.46, −1.05, −0.75 and
  −0.83 points per 10 pp against pre-period coefficients of −0.57 and −0.45.
- The 2025 change in attributing out-of-district testers (`reads/nyc_sources.md` §2) moves some students into
  school results from 2025.

**Denver.**

- Never-EL estimates are small, negative and insignificant.
- With 2021-22 EL share and the 2019–2022 enrollment change × year, the pooled post effects turn positive: +0.010
  (0.023) for ELA and +0.015 (0.027) for math, with pre-trend p 0.79 and 0.82.
- The broader not-EL group includes former ELs and pupils still in FEP monitoring. Its ELA coefficient in 2023-24
  is −0.036 (0.016); the others lie between −0.022 and −0.006.
- All-student scores, which include the newcomers themselves, fall −0.069 (0.019) in ELA and −0.055 (0.019) in
  math by 2024-25. That is the newcomers' own scores entering the average, not an effect on other students.

**Chicago.**

- Only the first surge year can be observed. X counts arrivals through the October 2024 count, so it overstates
  the exposure present in spring 2023.
- The intensity measured to the fall-2023 count (the 20th day of SY2023-24, `X_2024`) gives −1.15 pp (0.56) for
  ELA and −0.38 (0.39) for math.
- Converted at the normal density at the 2021-22 non-EL proficiency rate, 1 pp is about 0.030 SD in ELA (27.9%
  proficient) and 0.034 SD in math (21.7%) [INFERENCE: probit approximation, within-group SD]. The ELA estimate
  is about −0.035 SD per 10 pp, with a 95% interval of roughly −0.013 to −0.058; math is about −0.009 SD.

## Task 4. What the design identifies

**What it identifies.** The design compares schools in the same district and year that received more newcomers
with schools that received fewer. It identifies local exposure within a district: the effect of a school's own
newcomer inflow on its pupils, staff and budget.

Everything common to all schools in a city in a given year is absorbed by the year effects and cannot appear in
these coefficients:

- the citywide cost of the surge, such as NYC's asylum spending of $3,752m in FY2024
  (`migrant_shelter_costs_2026_09_23/RESULT.md`);
- district budget decisions;
- test changes: New York's new standards in 2023 and Illinois's new cut scores in 2025;
- the pandemic recovery.

In NYC the community-district × year version narrows the comparison further, to schools in the same community
school district.

**What it cannot identify.**

- **District-wide reallocation.**
  - When a district pays for newcomer pupils out of the common budget, every school bears the cost, and a
    difference between schools does not measure it.
  - NYC paid register relief to shrinking schools: $323.7m in FY2022, $136.2m in FY2023, $161.3m in FY2025 and
    $261.7m in FY2026 (`reads/nyc_sources.md` §3).
  - Central hiring, hold-harmless rules and cuts elsewhere work the same way.
  - The school-level spending test measures only where the money landed, not what it cost the district.
- **Spillovers onto the comparison schools.**
  - If teachers or money moved from low-exposure to high-exposure schools, comparison schools were worse off too,
    and the difference understates the cost to receiving schools.
  - If the district protected receiving schools at others' expense, the difference understates the harm to the
    system.
- **The system-level effect.**
  - The systemwide lane's state-level estimates (−0.07 to −0.14 SD per 10 pp, imprecise) include district-wide
    effects that this design removes by construction.
  - The near-zero within-district estimates here do not contradict them. The gap could be a district-wide effect,
    confounding in the system-level design, or both, and this lane cannot say which.
- **Peer effects on the same students.**
  - School-by-grade means mix changes in students' scores with changes in who is in the group.
  - The tested-count check finds no flight in NYC or Denver. It cannot detect a selective exit that leaves counts
    unchanged.
- **Random placement within the district.**
  - Newcomers went where there were seats. NYC and Denver receiving schools were shrinking before the surge
    (Task 2), and NYC's ELL-growth intensity fails the achievement pre-trend test.
  - The shelter-routed NYC intensity passes that test, but it covers only arrivals that the two memos recorded:
    July–October 2022 in schools with six or more, and July 2023–February 2024, weighted.
- **Effects beyond two to three post-surge test years, and grades outside 3–8.**

## What was not checked

- **NYC.**
  - Students in temporary housing by school, the Advocates for Children / NYSED series. It was not fetched, and
    the results file omits its tabs: "Data for students in temporary housing … were not available at the time
    of publication".
  - The March 2023 Project Open Arms list of 13,248 students in 608 schools. A blog reports it; it is not public.
  - NYC School-Based Expenditure Reports. These could bridge the 2023-24 spending break.
  - FSF mid-year adjustment amounts by school. The guides are linked from SAMs 85 and 86; I did not read them.
- **Chicago.** Non-EL results for 2024 (not published) and FY2024 school budgets (not retrievable); see
  `reads/chicago_sources.md`.
- **Denver.**
  - DPS school budgets and class size (not obtainable; see `reads/denver_sources.md`).
  - Blank immigrant counts (0–3 pupils) are set to 0.
- **No student-level data.** Everything is a school or school-grade mean.
- **Scale SDs.** The SD conversion uses statewide SDs. Chicago's percent-proficient conversion to SD is a probit
  approximation.

## Reproduction

Run from the repository root. Each script pins its inputs by sha256 and stops with `[BLOCKED]` on a missing or
changed file.

```sh
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/newcomer_school_shock_2026_09_28 \
  "uv run --no-project python3 {lane}/extract_nysed_src.py" \
  "uv run --no-project python3 {lane}/build_nyc.py" \
  "uv run --no-project --with python-calamine==0.8.2 python3 {lane}/build_chicago.py" \
  "uv run --no-project python3 {lane}/build_denver.py" \
  "uv run --no-project python3 {lane}/extract_scale_sd.py" \
  "uv run --no-project python3 {lane}/analyze.py"
```

- **Rerun result, 2026-09-28.** All six commands returned rc=0, and 29 of 29 output files were IDENTICAL. A
  separate hash comparison of the 30 files in `derived/` and `_cache/nyc/nysed_src/tables/` also matched.
- **Tools.** `extract_nysed_src.py` needs mdbtools (`brew install mdbtools`; 1.0.1 used). The raw cache is 2.8 GB
  and git-ignored, most of it the six NYSED databases.
- **Size.** `derived/` is 55 MB. The three `*_scores.csv` files (11–20 MB each) stay untracked
  (`.gitignore`); the build scripts regenerate them, and the rerun compares them too.
- **Parent rerun, 2026-09-28 07:11 JST.** All six commands returned rc=0; 30 of 30 files were IDENTICAL,
  including the three untracked score files.
