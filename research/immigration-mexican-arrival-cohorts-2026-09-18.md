claude-opus-5[1m]

# Mexico-born arrival cohorts: did selection fall across cohorts? (2026-09-18)

**Verdict:** Measured skill rose sharply; selection relative to Mexico did not move. Mexico-born
arrivals observed at ages 25–54 within five years of arrival went from 82.5% less-than-high-school
and 3.4% BA+ in the 1980 census (1975–80 arrivals) to 33.3% and 21.7% in the 2023 ACS (2018–23
arrivals), a monotone improvement with no reversal at any step. On the education-conditional
log-income residual against US-born white workers of the same age in the same survey, cohort quality
fell between 1980 and 1990 and then improved steadily: −0.429, −0.552, −0.473, −0.418, −0.309 log
points for the 1975–80, 1985–90, 1995–2000, 2005–10 and 2018–23 arrival windows. The shape on
earnings is a decline through the 1980s followed by a sustained recovery, not a secular fall.

**But the origin distribution moved just as fast.** Migrant entry cohorts gained 2.37 years of mean
schooling between the 2000 and 2023 surveys; INEGI puts the gain for the Mexican population aged 15
and over at 2.20 years between 2000 and 2020. The difference is about two months of schooling over
two decades. So the large rise in absolute attainment among Mexican arrivals is almost entirely the
rise in Mexican attainment, and selection — position within the origin distribution — is flat.
Anyone reading the education series as evidence that migration became more selective is reading a
Mexican schooling expansion.

Two further results. The 2020–24 cohort is the best-educated in the file and its short-duration wage
residual is the worst, which is duration and not cohort: at matched duration the recent cohort is
ahead of every predecessor. And the post-2020 border increase was not a Mexican phenomenon — Mexican
nationals are 14.3% of foreign-born 2021–24 arrivals aged 25–54 in the ACS, and 10.9% of FY2021
Southwest border encounters once Title 42 repeat crossings are excluded, against a headline
encounter share of 37.8%. [SOURCE: own computation on the IPUMS census/ACS panel, ACS 2023 and 2024
1-year PUMS, and CBP Nationwide Encounters; INEGI for the origin series; see
`infra/immigration-fiscal/arrival_cohorts_2026_09_18/`]

---

## 1. Data and construction

Two independent instruments, deliberately kept separate because they carry different variables.

**IPUMS USA panel** (`immigration_microdata.duckdb`, table `ipums_usa_borjas_panel`, read-only,
44.4M person records): 1980, 1990, 2000 5% censuses plus 2010 and 2023 ACS. Mexico-born is
`BPL == 200`. Comparison group is US-born (`BPL < 150`) `RACE == 1` white. This extract has no
`SEX`, no `HISPAN`, no `SPEAKENG`, no `INCWAGE` and no `UHRSWORK`, so everything from it is
all-sex, the comparison group is white including Hispanic white, and income is `INCTOT` (total
personal income, nominal).

**ACS 1-year PUMS 2023 and 2024** (staged person files, ages 25–54 extracted to parquet): Mexico-born
is `POBP == 303`, comparison group is `NATIVITY == 1 & HISP == 1 & RAC1P == 1`, i.e. US-born
non-Hispanic white. This lane carries `SEX`, `ENG`, `SCHL`, `WAGP`, `WKHP`, `WKWN`, `CIT`, so it
supplies the by-sex education, English and full-time-full-year wage results.

Education is coded from the harmonised IPUMS `EDUC`, not `EDUCD`, because the 1980 census codes
grade 12 as `EDUCD` 60 with no diploma/GED split; using `EDUCD <= 61` would have classified 1980
high-school completers as less-than-high-school and manufactured a spurious 1980 outlier. The
`EDUC` mapping is: `<=5` below grade 12, `=6` grade 12 including 12th-no-diploma, `7–9` some
college, `>=10` bachelor's or more. The cost is that roughly 5 percentage points of
12th-grade-no-diploma sits in the high-school category in every year; that share is stable across
survey years, so the cross-cohort comparison is not affected. The ACS lane uses `SCHL` where the
diploma split is unambiguous (`<=15` less than HS, `16–17` HS/GED, `18–20` some college, `>=21` BA+).

Arrival cohorts are cut from `YRIMMIG` (IPUMS) or `YOEP` (ACS) at pre-1980, 1980–89, 1990–99,
2000–07, 2008–14, 2015–19, and 2020–24 split into 2020–21 and 2022–24 where cells allow. All
statistics are person-weighted (`PERWT`, `PWGTP`). Intervals are weighted normal intervals on the
effective sample size and are **design-naive**: PUMS replicate weights were not used, so the true
intervals are wider, by a factor commonly around 1.3–1.7 for ACS person means. Ranking conclusions
below rest on gaps of 10–50 percentage points or 0.1–0.25 log points, which survive that inflation;
adjacent-cohort orderings within a few hundredths of a log point do not.

Ages are restricted to 25–54 at observation throughout, so schooling is essentially complete and,
for people who arrived as adults, largely acquired in Mexico.

**The two lanes reproduce each other exactly.** For Mexico-born aged 25–54 who arrived in 2020 or
later, both lanes read the same 3,378 unweighted records, and once the education definitions are
aligned — IPUMS `EDUC <= 5` against ACS `SCHL <= 14`, both meaning fewer than twelve years and
excluding 12th-grade-no-diploma — they give identical weighted shares of 0.3287 less than twelve
years and 0.2259 BA+. Using the ACS `SCHL <= 15` definition instead, which counts
12th-grade-no-diploma as less than high school, raises that to 0.3672, which is the 3.9-point
definitional wedge described above. The IPUMS 2023 sample and the 2023 ACS PUMS person file are the
same records, so this is a check on the code, not on the data.

---

## 2. The cleanest object: entry quality at fixed duration

Holding years since arrival fixed and stepping across surveys compares arrival cohorts at the same
point in their US careers. This is the Borjas 1985/1995 cohort-quality object, and at 0–5 years
since arrival it is measured before most return migration has had time to occur, which is what
makes it the least contaminated cut available here.

Mexico-born, ages 25–54, arrived within the previous five years. Worker definition is employed with
positive income, because the 2010 ACS carries no continuous weeks-worked variable in this extract.

| Survey | Arrival window | n | <HS | HS | Some college | BA+ | Employed | Residual, age only | Residual, age + education |
|---|---|---|---|---|---|---|---|---|---|
| 1980 census | 1975–80 | 11,972 | 82.5% | 9.4% | 4.8% | 3.4% | 64.1% | −0.662 [−0.683, −0.641] | −0.429 [−0.449, −0.408] |
| 1990 census | 1985–90 | 21,193 | 66.4% | 18.5% | 9.3% | 5.8% | 63.5% | −0.852 [−0.869, −0.834] | −0.552 [−0.569, −0.535] |
| 2000 census | 1995–2000 | 46,781 | 61.5% | 26.8% | 5.6% | 6.2% | 57.7% | −0.783 [−0.796, −0.770] | −0.473 [−0.485, −0.460] |
| 2010 ACS | 2005–10 | 5,567 | 51.7% | 31.8% | 7.4% | 9.1% | 65.2% | −0.777 [−0.809, −0.746] | −0.418 [−0.448, −0.387] |
| 2023 ACS | 2018–23 | 4,913 | 33.3% | 35.7% | 9.3% | 21.7% | 73.4% | −0.566 [−0.603, −0.529] | −0.309 [−0.345, −0.273] |

`derived/entry_quality_fixed_duration_ipums.csv`

Restricting to full-year workers (`WKSWORK1 >= 48`), which drops 2010, moves the levels but not the
shape: age-only residuals of −0.610, −0.668, −0.610, −0.472 and education-conditional residuals of
−0.404, −0.427, −0.357, −0.250 for 1975–80, 1985–90, 1995–2000 and 2018–23.

Two readings, both supported:

**Education.** The less-than-high-school share of arrivals falls in every step, by 49 percentage
points across the series, and the BA+ share rises from 3.4% to 21.7%. There is no year in which
the ordering reverses.

**Earnings.** The age-only entry gap widens by 19 log points between 1980 and 1990 and then closes
by 29 log points between 1990 and 2023. Conditional on education, the same pattern: −0.43 → −0.55
→ −0.47 → −0.42 → −0.31. So the decline in cohort quality that Borjas identified for the 1970s and
1980s is present in these data, and it stops. About half of the post-1990 improvement in the
age-only gap survives an education control, meaning the recovery is not purely a composition
effect of better-schooled arrivals.

The direction agrees with ladder entry 92's administrative evidence (Akee, Chin & Crown, NBER
w35582): "entry gaps fell from 70 to 30 log points across cohorts." The magnitudes are not
comparable — theirs are SSA-recorded earnings against a native benchmark over 1981–2021, mine are
census/ACS self-reported income against US-born white workers in the same survey — but two
independent data systems produce the same sign and roughly the same order of closure.

---

## 3. Education at each cohort's first observation, and ten years later

The same result organised by cohort rather than by survey. "First" is the first survey in the panel
in which the cohort is observed at ages 25–54; "+10" is the next survey ten years on. Shares are
crude and age-standardised to the 2000 census Mexico-born 25–54 age distribution; the two differ by
at most 2.5 percentage points anywhere, so age composition is not driving anything here.

| Cohort | Obs | Survey | Mean years since arrival | n | <HS | HS | Some college | BA+ |
|---|---|---|---|---|---|---|---|---|
| pre-1980 | first | 1980 | 15.0 | 52,379 | 76.4% | 13.5% | 6.8% | 3.3% |
| pre-1980 | +10 | 1990 | 21.8 | 72,349 | 66.3% | 18.7% | 11.4% | 3.6% |
| 1980–89 | first | 1990 | 6.7 | 44,580 | 68.8% | 18.0% | 8.7% | 4.4% |
| 1980–89 | +10 | 2000 | 15.2 | 95,795 | 62.9% | 26.6% | 6.7% | 3.8% |
| 1990–99 | first | 2000 | 5.8 | 91,459 | 62.0% | 27.4% | 5.6% | 5.1% |
| 1990–99 | +10 | 2010 | 15.3 | 21,435 | 55.3% | 31.4% | 8.7% | 4.6% |
| 2000–07 | first | 2010 | 7.3 | 14,542 | 54.6% | 32.3% | 7.2% | 5.9% |
| 2008–14 | first | 2010 | 1.3 | 1,792 | 51.4% | 30.1% | 7.2% | 11.3% |
| 2015–19 | first | 2023 | 6.1 | 3,923 | 34.9% | 36.5% | 9.8% | 18.7% |
| 2020–24 | first | 2023 | 1.5 | 3,378 | 32.9% | 34.9% | 9.7% | 22.6% |

`derived/bound_agestd_education_first_obs.csv`, `derived/ipums_edu_by_cohort_year.csv`

Three cohorts are observed at nearly identical duration — 1980–89 at 6.7 years, 1990–99 at 5.8,
2015–19 at 6.1 — and the less-than-high-school share across them is 68.8% → 62.0% → 34.9%, with
BA+ 4.4% → 5.1% → 18.7%. The 2008–14 and 2020–24 cells are thin (n = 1,792 and 3,378 unweighted)
and are read at 1.3 and 1.5 years since arrival, where the ACS captures recent unauthorised
arrivals worst; section 7 stress-tests exactly that.

Within every cohort the less-than-high-school share falls between the first reading and the
reading ten years later, by 5.9 to 10.1 percentage points. That drift is the ladder-92 mechanism
made visible, and section 6 bounds how much of it return migration can account for.

---

## 4. The 2023 and 2024 cross-section: by sex, with English and citizenship

The ACS PUMS lane carries the variables the IPUMS extract lacks. ACS 2024, Mexico-born aged 25–54.
"English very well or only English at home" pools the `ENG == 1` category with people who report
speaking only English.

| Cohort | Sex | n | Mean YSA | <HS | BA+ | English very well+ | English not at all | Employed | Non-citizen |
|---|---|---|---|---|---|---|---|---|---|
| pre-1980 | men | 773 | 48.3 | 28.7% | 14.7% | 71.7% | 3.5% | 86.9% | 31.4% |
| 1980–89 | men | 2,670 | 38.1 | 40.7% | 9.3% | 54.0% | 4.8% | 86.7% | 44.3% |
| 1990–99 | men | 7,773 | 29.0 | 46.9% | 7.1% | 43.5% | 6.7% | 89.7% | 68.0% |
| 2000–07 | men | 7,600 | 21.3 | 48.5% | 6.7% | 37.1% | 9.5% | 90.1% | 80.1% |
| 2008–14 | men | 2,692 | 13.2 | 42.4% | 14.5% | 32.3% | 14.2% | 90.6% | 77.5% |
| 2015–19 | men | 1,898 | 7.0 | 39.1% | 18.2% | 27.8% | 19.5% | 90.5% | 87.0% |
| 2020–21 | men | 850 | 3.4 | 43.5% | 19.3% | 22.8% | 30.6% | 88.1% | 96.4% |
| 2022–24 | men | 2,028 | 1.1 | 38.3% | 20.7% | 22.4% | 35.0% | 87.0% | 97.1% |
| pre-1980 | women | 848 | 48.3 | 24.7% | 17.6% | 74.4% | 3.9% | 72.8% | 21.3% |
| 1980–89 | women | 2,473 | 38.2 | 31.9% | 14.2% | 60.5% | 6.1% | 69.8% | 36.2% |
| 1990–99 | women | 7,623 | 29.0 | 40.7% | 10.1% | 43.1% | 9.1% | 65.4% | 62.5% |
| 2000–07 | women | 7,410 | 21.2 | 44.9% | 9.4% | 34.9% | 15.0% | 59.6% | 77.5% |
| 2008–14 | women | 2,444 | 13.3 | 37.2% | 17.4% | 32.2% | 17.6% | 57.0% | 71.5% |
| 2015–19 | women | 1,678 | 7.1 | 36.4% | 20.4% | 26.6% | 25.3% | 57.4% | 83.1% |
| 2020–21 | women | 677 | 3.4 | 28.6% | 25.5% | 26.3% | 28.8% | 58.6% | 91.0% |
| 2022–24 | women | 1,255 | 1.2 | 32.6% | 28.1% | 25.0% | 36.1% | 48.1% | 97.0% |

`derived/acs_cohort_composition.csv` (2023 rows also present)

Education by cohort is U-shaped in both sexes, worst for the 2000–07 cohort and better on either
side. Women's BA+ share among 2022–24 arrivals, 28.1%, is the highest of any Mexico-born cell in
the file, three times the 2000–07 cohort's 9.4%.

**English cannot be decomposed here.** The monotone fall in English ability with recency is
mechanically what a single cross-section produces, because duration in the US and arrival cohort are
collinear within one survey year. Separating them needs the same cohort read at the same duration in
different survey years, which requires ACS 1-year files between 2005 and 2019. Those are not staged
locally, the Census FTP site served full-year PUMS zips at roughly 13 MB/min and dropped every large
transfer partway, and the Census PUMS API — which can return Mexico-born records alone, and does
work — delivered about 27 KB/s, roughly an hour per survey year. **The brief's item (2), English at
two fixed points per cohort, is therefore not delivered, and no cohort-versus-duration claim about
English is made in this memo.** The machinery is in place for whoever picks it up:
`english_cohorts.py` consumes state-chunked API pulls from `_cache/states_<year>/`, and partial
pulls for 2013 and 2019 were accumulating when this memo was written.

What the table does show, with duration and cohort deliberately not separated, is that
duration-0–1 arrivals in 2024 report speaking English "not at all" at 35%, against 19.5% for the
2015–19 cohort at duration 7 and 4.8% for the 1980–89 cohort at duration 38. That is consistent
with ordinary language acquisition over time in the US, with a genuinely language-poorer recent
inflow, or with both, and these two survey years cannot choose between them.

---

## 5. Wage residuals with intervals

Full-time full-year workers (`WKHP >= 35`, `WKWN >= 48`) with positive wage income. Residual is
log `WAGP` minus the weighted mean log `WAGP` of US-born non-Hispanic white workers of the same
sex, five-year age group and education category in the same survey year; this is a saturated
cell-mean regression with survey-year fixed effects by construction.

ACS 2024, education-conditional:

| Cohort | Men | 95% interval | Women | 95% interval |
|---|---|---|---|---|
| pre-1980 | −0.105 | [−0.177, −0.034] | −0.047 | [−0.109, +0.016] |
| 1980–89 | −0.123 | [−0.159, −0.088] | −0.142 | [−0.184, −0.099] |
| 1990–99 | −0.181 | [−0.202, −0.161] | −0.153 | [−0.177, −0.128] |
| 2000–07 | −0.219 | [−0.240, −0.198] | −0.196 | [−0.222, −0.169] |
| 2008–14 | −0.208 | [−0.243, −0.174] | −0.195 | [−0.241, −0.149] |
| 2015–19 | −0.276 | [−0.321, −0.232] | −0.296 | [−0.355, −0.237] |
| 2020–21 | −0.333 | [−0.396, −0.269] | −0.197 | [−0.279, −0.116] |
| 2022–24 | −0.348 | [−0.398, −0.298] | −0.207 | [−0.285, −0.129] |

`derived/acs_wage_residual_by_cohort.csv`; unadjusted (age only) in
`derived/acs_wage_residual_unadjusted.csv`; 2023 reproduces the 2024 ordering to within 0.03 log
points everywhere except the 2015–19 male cell.

This table read down the column is **not** a cohort-quality ranking. It is the assimilation profile
and the cohort effect summed, and in a single cross-section they are not separable. The pre-1980
cohort's −0.10 is 48 years of US labour-market experience plus whatever it started with. The
fixed-duration series in section 2 is the version of this object that holds duration constant, and
it points the other way.

The male 2020–24 cells are the one place where the recent cohorts look worse rather than better:
−0.333 and −0.348 at durations of 3.4 and 1.1 years, against −0.276 for the 2015–19 cohort at
duration 7.0. Since wages rise steeply in the first years after arrival, most or all of that gap
is duration. The IPUMS lane gives the same comparison at matched duration and finds the opposite
sign: 2018–23 arrivals at 0–5 years sit at −0.309 education-conditional, against −0.418 for
2005–10 arrivals and −0.473 for 1995–2000 arrivals at the same duration. Where the two lanes can
be made comparable, the recent cohort is better; the apparent deterioration is an artefact of
comparing cohorts at different durations.

---

## 5b. Synthetic-cohort assimilation profiles

The same cohorts followed across surveys in the IPUMS lane. Each row is one cohort observed in one
survey; reading across a cohort gives its earnings profile as it ages in the US. Residual is log
`INCTOT` of full-year workers against US-born white workers of the same age group and education in
the same survey.

| Cohort | 1980 | 1990 | 2000 | 2023 |
|---|---|---|---|---|
| pre-1980 | −0.217 (15.5y) | −0.111 (21.9y) | −0.100 (27.5y) | −0.101 (47.5y) |
| 1980–89 | — | −0.352 (7.2y) | −0.193 (15.3y) | −0.135 (37.2y) |
| 1990–99 | — | — | −0.320 (6.0y) | −0.188 (28.1y) |
| 2000–07 | — | — | −0.351 (0.0y) | −0.224 (20.3y) |
| 2008–14 | — | — | — | −0.228 (12.1y) |
| 2015–19 | — | — | — | −0.212 (6.1y) |
| 2020–24 | — | — | — | −0.276 (1.6y) |

Mean years since arrival in parentheses. `derived/ipums_wage_residual_by_cohort_year.csv`;
the same object cut by years-since-arrival band is in
`derived/ipums_wage_residual_by_ysm_band.csv`.

Every cohort converges toward the native benchmark, and convergence is fast in the first fifteen
years and slow after. The pre-1980 cohort is flat from 21 years onward at roughly −0.10, which is
where the 1980–89 cohort has also arrived by 2023. No Mexico-born cohort in this file reaches
parity with US-born white workers of the same age and education at any duration.

**These profiles track stayers only** (ladder 92). Part of every within-cohort improvement across
columns is the negatively selected fifth-to-a-third of the cohort leaving, not the survivors' wages
rising. Section 6 puts the size of that at up to 0.099 log points, which is a large share of the
0.10–0.16 log-point convergence observed between the second and third reading of each cohort. The
cross-cohort comparisons in section 2 avoid this by holding duration at 0–5 years, before most
departures occur; the profiles here do not, and should be read as an upper bound on true individual
assimilation.

---

## 6. Return-migration bound (ladder 92)

Ladder entry 92 records that a fifth to a third of Mexican arrivals leave within ten years and
that leavers are negatively selected with flat or falling relative earnings. The panel observes
stayers only, so every within-cohort improvement over time is partly composition.

**On education.** If the entire fall in a cohort's less-than-high-school share over ten years were
return migration, the leavers would have to have had the following less-than-high-school shares:

| Cohort | <HS first | <HS +10y | Drift | Leavers 20% | Leavers 25% | Leavers 33% |
|---|---|---|---|---|---|---|
| pre-1980 (1980→1990) | 76.4% | 66.3% | −10.1pp | 116.9% (infeasible) | 106.7% (infeasible) | 96.9% |
| 1980–89 (1990→2000) | 68.8% | 62.9% | −5.9pp | 92.2% | 86.4% | 80.7% |
| 1990–99 (2000→2010) | 62.0% | 55.3% | −6.7pp | 88.8% | 82.1% | 75.6% |

`derived/bound_implied_leaver_education.csv`

The implied leaver education distributions are extreme but, at a one-third leaver share, feasible:
76–97% less-than-high-school among leavers against 55–66% among stayers. So return migration alone
can account for essentially the whole within-cohort drift, and the residual role for US schooling
acquisition, mortality and reporting change may be small. The pre-1980 row is arithmetically
impossible at leaver shares of 20% and 25%, which says the leaver share for that cohort over that
decade must have been near a third, or that something other than return migration contributed.

**On earnings.** If a fraction L of a cohort leaves and leavers sit δ log points below stayers, the
stayer-only mean overstates the full cohort mean by exactly L·δ:

| L | δ = 0.05 | δ = 0.10 | δ = 0.20 | δ = 0.30 |
|---|---|---|---|---|
| 0.20 | 0.010 | 0.020 | 0.040 | 0.060 |
| 0.25 | 0.013 | 0.025 | 0.050 | 0.075 |
| 0.33 | 0.017 | 0.033 | 0.066 | 0.099 |

`derived/bound_stayer_residual_inflation.csv`

The largest bias in the table is 0.099 log points. The cross-cohort differences the verdict rests
on are 0.16 to 0.24 log points in the fixed-duration series and 28 to 49 percentage points in the
education series. For return migration to reverse the earnings ranking, the leaver share would have
to differ sharply *across* cohorts in the direction that flatters recent arrivals, and by enough to
move a 0.24-log-point gap. At δ = 0.30 that needs a leaver-share difference of about 80 percentage
points between cohorts, which is outside any plausible range. The education ranking is further out
of reach still. The bound does not overturn the verdict; it does mean every *level* in sections 2–5
is a stayer statistic and overstates its cohort by up to a tenth of a log point.

One direction cuts the other way, as ladder 92 notes: unauthorised off-books earnings sit outside
the SSA record, and in a household survey they are self-reported and plausibly understated, more so
for the recent, overwhelmingly non-citizen cohorts (97% non-citizen among 2022–24 arrivals). That
biases recent cohorts' measured wages *down*, so correcting it would strengthen, not weaken, the
finding of improvement.

---

## 7. Undercount stress test for the recent cohorts

The ACS misses recent unauthorised arrivals disproportionately, and that population is
disproportionately less-educated. Suppose the true 2018–23 Mexican arrival cohort aged 25–54 is k
times the surveyed count and **every** missed person has less than a high-school education, the
most adverse assumption available:

| Undercount factor k | Implied <HS share | Below 1985–90 (66.4%)? | Below 1995–2000 (61.5%)? | Below 2005–10 (51.7%)? |
|---|---|---|---|---|
| 1.0 | 33.3% | yes | yes | yes |
| 1.2 | 44.4% | yes | yes | yes |
| 1.3 | 48.7% | yes | yes | yes |
| 1.5 | 55.5% | yes | yes | no |
| 1.75 | 61.9% | yes | no | no |
| 2.0 | 66.6% | no | no | no |

`derived/bound_undercount_sensitivity.csv`

The education ranking against the 1985–90 and 1995–2000 cohorts survives an undercount of up to
75% extra people, all of them less-than-high-school. It fails only at a doubling. The benchmark
cohorts were themselves undercounted, which this test ignores, so it is one-sided and conservative
in the direction that could kill the finding.

---

## 8. Selection relative to the Mexican origin distribution

Rising absolute schooling among migrants is not the same thing as rising selection. Mexican
schooling rose steeply over the same decades, so the test is whether migrant attainment rose
*faster* than the origin distribution it was drawn from.

**Origin side.** INEGI reports mean years of schooling for the Mexican population aged 15 and over
at 7.5 (2000), 8.1 (2005), 8.6 (2010), 9.2 (2015) and 9.7 (2020), from the Censo de Población y
Vivienda, the 2005 Conteo and the 2015 Encuesta Intercensal. Verbatim: *"En México, entre 2000 y
2020, el grado promedio de escolaridad de las personas de 15 años y más se incrementó 2.2 años. En
2000 el promedio fue de 7.5 años de estudio (entre primero y segundo de secundaria). En 2020 llegó
a 9.7 años (un poco más de la secundaria completa)."* ["In Mexico, between 2000 and 2020, mean
years of schooling of people aged 15 and over rose by 2.2 years. In 2000 the mean was 7.5 years of
study (between first and second year of lower secondary). In 2020 it reached 9.7 years (a little
more than completed lower secondary)."] The 2020 census attainment distribution for the same
population is 4.9% no schooling, 49.3% básica, 24.0% media superior, 21.6% superior, 0.2%
unspecified. [SOURCE: https://cuentame.inegi.org.mx/poblacion/escolaridad.aspx and
https://www.inegi.org.mx/temas/educacion/, both fetched 2026-09-18]

**Migrant side.** Mapping harmonised `EDUC` to years of schooling at category midpoints and taking
Mexico-born aged 25–54 who arrived within the previous five years:

| Survey | Arrival window | n | Migrant mean years at entry | INEGI 15+ mean years | Difference |
|---|---|---|---|---|---|
| 1980 | 1975–80 | 10,885 | 7.12 | not in the INEGI series | — |
| 1990 | 1985–90 | 18,510 | 8.96 | not in the INEGI series | — |
| 2000 | 1995–2000 | 42,265 | 9.55 | 7.5 (2000) | +2.05 |
| 2010 | 2005–10 | 5,261 | 10.12 | 8.6 (2010) | +1.52 |
| 2023 | 2018–23 | 4,553 | 11.92 | 9.7 (2020) | +2.22 |

`derived/origin_relative_mean_years.csv`

**The slopes are the same.** Migrant entry cohorts gained 2.37 years of schooling between the 2000
and 2023 surveys. The Mexican origin population gained 2.20 years between 2000 and 2020. The
difference is +0.17 years over two decades. Extrapolating the INEGI series to 2023 at its own
2015–20 pace (+0.5 per five years) puts the origin at about 10.0 and the 2023 difference at +1.9
rather than +2.2, which moves the slope comparison to roughly −0.15 years. Either way the answer is
the same: **the large rise in measured schooling among Mexican arrivals is almost entirely the rise
in Mexican schooling, not a change in who selects into migrating.**

That is the most important qualification in this memo, and it cuts against the natural reading of
sections 2 and 3. Absolute skill of arrivals rose a great deal. Selection — position in the origin
distribution — did not measurably move.

The levels are not comparable and should not be read as such: the origin figure covers ages 15 and
over, which includes teenagers still in school and an elderly cohort schooled in the 1940s and
1950s, while the migrant figure covers ages 25–54. The persistent positive difference of 1.5–2.2
years is therefore mostly an age-composition artefact, not a measurement of positive selection. The
slope comparison does not suffer from this, because the age bases are held fixed on both sides
across the two decades.

**The sign of the level of selection, from primary sources.** Chiquiar & Hanson's own text, from
the NBER working-paper version of the 2005 JPE article (w9242, October 2002, fetched 2026-09-18):

> "We find that 1) Mexican immigrants, while much less educated than U.S. natives, are on average
> more educated than residents of Mexico, and 2) were Mexican immigrants in the United States to be
> paid according to current skill prices in Mexico they would tend to occupy the middle and upper
> portions of Mexico's wage distribution. These results are inconsistent with the negative-selection
> hypothesis and suggest, instead, that in terms of observable skills there is intermediate or
> positive selection of immigrants from Mexico."

And their headline comparison, which doubles as a validation of this memo's own computation:

> "In 1990, 72.3% of all Mexican immigrant men and 68.2% of recent Mexican immigrant men had
> completed 11 or fewer years of school, compared to only 19.0% of U.S. native men. However,
> Mexican immigrants, and recent immigrants in particular, compare favorably when we examine
> educational attainment in Mexico. In 1990, 81.0% of male residents of Mexico had 11 or fewer
> years of schooling."

Their 68.2% for recent Mexican immigrant men in 1990 sits next to this memo's 66.4%
less-than-twelve-years for 1985–90 arrivals aged 25–54, all-sex, computed independently from the
1990 census. The two agree to within two points, which is the check that the education construction
here is sound.

**Fernández-Huertas Moraga 2011** (*Review of Economics and Statistics* 93(1), 72–96) reaches the
opposite conclusion on the level of selection. The published abstract, as carried in the RePEc
record of the article (fetched 2026-09-18; the article PDF itself is behind a subscription and was
not retrieved):

> "This paper examines the extent to which Mexican emigrants to the United States are negatively
> selected. Previous studies have been limited by the lack of nationally representative
> longitudinal data. This one uses a newly available household survey, that identifies emigrants
> before they leave. On average, U.S.-bound Mexican emigrants from 2000 to 2004 earn lower wages
> and have less (more for females) schooling than nonmigrant Mexicans, evidence of negative
> selection. This argues against Chiquiar and Hanson's (2005) findings. The discrepancy is
> primarily due to an undercount of unskilled migrants in U.S. sources and secondarily to the
> omission of unobservables in their methodology."

Two things follow. First, the sign of the *level* of Mexican selection is genuinely contested by
careful work in overlapping periods, which is why this section reports a slope comparison and not a
level claim. Second, and more pointedly for this memo, Fernández-Huertas Moraga's stated reason for
the disagreement — "an undercount of unskilled migrants in U.S. sources" — is the exact mechanism
the stress test in section 7 was built to probe. His argument implies the US-side education
distributions used throughout this memo, including the Chiquiar-Hanson numbers, are biased upward.
That objection applies to every cohort in the series, so it moves levels rather than the
cross-cohort ordering, unless the undercount itself changed sharply across cohorts. Section 7 shows
the ordering survives an undercount factor of 1.75 concentrated entirely in the recent cohort. The
level statement "Mexican migrants are more educated than Mexican residents" is not something this
memo can adjudicate and is not claimed here.

Both anchors are now quoted from source. The remaining gap in this section is an origin attainment
distribution **by birth cohort**, which would let the migrant cohorts be placed in the origin
distribution of their own generation rather than against a national mean. INEGI's census tabulados
carry it; it was not retrieved here. **[UNVERIFIED]** for that cut specifically.

---

## 9. The 2021–24 arrivals were mostly not Mexican

Equating the post-2020 border increase with Mexican migration is a category error. Among
foreign-born people aged 25–54 who reported arriving in 2021 or later, the Mexican-born share is:

| Survey | Arrival window | Weighted arrivals 25–54 | Mexico-born | Mexican share | Unweighted n |
|---|---|---|---|---|---|
| ACS 2023 | 2020–21 | 1,244,933 | 203,179 | 16.3% | 9,455 |
| ACS 2023 | 2021–24 | 2,449,699 | 349,056 | 14.2% | 19,302 |
| ACS 2024 | 2020–21 | 1,337,202 | 209,556 | 15.7% | 9,403 |
| ACS 2024 | 2022–24 | 3,001,061 | 435,877 | 14.5% | 21,800 |
| ACS 2024 | 2021–24 | 3,877,572 | 554,722 | 14.3% | 27,986 |

`derived/acs_recent_arrival_origin_mix.csv`

Top birthplaces among 2021–24 arrivals aged 25–54 in the ACS 2024: Mexico 14.3%, India 10.1%, Cuba
6.4%, Venezuela 6.3%, Colombia 4.1%, China 3.4%, Haiti 3.4%, Honduras 2.8%, Brazil 2.8%,
Philippines 2.7%, Guatemala 2.6%, Nicaragua 2.5%, Dominican Republic 1.9%, El Salvador 1.9%,
Ukraine 1.8%. `derived/acs_2024_top_origins_2021_24_arrivals.csv`

Mexico is the largest single origin and still under a seventh of the total. For comparison, the
Mexican share of the same age group among 2015–19 arrivals is 12.1–12.8%, so the Mexican share of
recent arrivals did not rise during the surge years by more than two or three points.

**Border encounters tell the same story, once Title 42 is handled.** CBP's Nationwide Encounters
file gives, for the Southwest land border:

| Fiscal year | Total encounters | Mexican nationals | Mexican share | Title 42 share of total | Mexican share, Title 8 only |
|---|---|---|---|---|---|
| 2021 | 1,734,686 | 655,594 | 37.8% | 61.3% | 10.9% |
| 2022 | 2,378,944 | 808,339 | 34.0% | 45.4% | 8.9% |
| 2023 | 2,475,669 | 717,333 | 29.0% | 22.8% | 19.3% |
| 2024 | 2,135,005 | 653,684 | 30.6% | 0% | 30.6% |
| 2025 (through Sep) | 443,671 | 177,052 | 39.9% | 0% | 39.9% |

`derived/cbp_mexican_share_encounters.csv`. The nationwide FY2024 total of 2,901,142 matches CBP's
published figure, which is the check that the file was read correctly.

The Title 8-only column is the important one. CBP counts **encounters**, which are events and not
persons, and a Title 42 expulsion carried no legal consequence, so the same person re-crossing was
counted each time. Those repeat crossings were overwhelmingly Mexican: 582,537 of the 655,594
Mexican encounters at the Southwest border in FY2021 were Title 42, 89% of the Mexican total
against 61% for all nationalities, and 692,363 of 808,339, or 86%, in FY2022. Stripping Title 42
out puts the Mexican share of Southwest encounters at 10.9% in FY2021 and 8.9% in FY2022, against
headline shares of 37.8% and 34.0%. The encounter share therefore overstates Mexican participation
in the post-2020 increase by a factor of roughly three and a half in FY2021 and four in FY2022,
and by a third in FY2023.

Top Southwest-border nationalities in FY2024: Mexico 30.6%, Venezuela 12.2%, Guatemala 9.6%, Cuba
7.1%, Honduras 6.6%, Colombia 6.0%, Ecuador 5.7%, Haiti 4.2%, El Salvador 2.5%, China 1.8%, Peru
1.7%. `derived/cbp_top_nationalities_sw_fy2023.csv`, `..._fy2024.csv`

The two instruments agree. Mexican nationals are 14.3% of foreign-born 2021–24 arrivals aged 25–54
in the ACS and 8.9–30.6% of Title 8 Southwest encounters depending on the year. Neither supports
treating the post-2020 increase as a Mexican phenomenon.

---

## 10. What this does not identify

**Legal status.** Nothing here observes authorisation. Non-citizen share is a weak proxy and rises
to 97% for the newest cohorts partly because naturalisation takes years. A shift in the legal
composition of arrivals — more humanitarian parole, fewer clandestine entries, or the reverse —
would move measured education without any change in selection within a status category.

**Ability beyond schooling and wages.** Years of schooling and log earnings are the only skill
measures in these files. Mexican secondary schooling expanded enormously over the period, so a year
of Mexican schooling in 2020 is not the same object as a year in 1975, and the education series
partly measures credential inflation rather than human capital.

**Survivorship.** Every level is a stayer statistic (section 6). Every cohort is also conditioned on
surviving to ages 25–54 in the US at the observation date.

**Period versus cohort.** The fixed-duration series in section 2 holds duration constant but not the
macroeconomy. The 1990 reading falls in a recession, the 2010 reading just after one, the 2023
reading in a tight labour market. Some of the 1980→1990 deterioration and some of the 2010→2023
improvement is business cycle, and with five survey years there is no way to net it out. The fact
that the education series, which has no cyclical component, moves monotonically in the same
direction is the main reason to think the cycle is not doing all the work in the earnings series.

**The comparison group differs between lanes.** IPUMS uses US-born white including Hispanic white;
ACS uses US-born non-Hispanic white. The IPUMS comparison group is therefore slightly lower-paid,
which makes IPUMS residuals slightly less negative than the ACS ones. This affects levels across
lanes, not the within-lane cross-cohort comparisons that the verdict rests on.

**Intervals are design-naive.** Replicate weights were not used.

---

## 11. Disconfirmation

Four ways this verdict could be wrong, and what each would take.

**The origin distribution moved faster than the migrant distribution.** This was the strongest
objection and it is now measured rather than conceded, in section 8. The answer is that the two
moved at the same rate to within 0.17 years over two decades, which does not overturn the
measured-skill finding but does destroy any reading of it as rising selectivity. The remaining
weakness is that the origin benchmark is a national mean for ages 15 and over, not an attainment
distribution by birth cohort; the latter would be the decisive version of the test and was not
retrieved.

**Differential undercount.** Tested in section 7, and it is the objection Fernández-Huertas Moraga
raises against exactly this class of US-source evidence: he attributes his disagreement with
Chiquiar-Hanson "primarily to an undercount of unskilled migrants in U.S. sources." It would take
an undercount factor near 2.0, with every missed person less-than-high-school, to overturn the
education ranking against the 1985–90 cohort. That is larger than published coverage-error
estimates for the ACS foreign-born, but those estimates are themselves contested for the
unauthorised population. The objection bites hardest on levels, which this memo does not use for
anything, and on the cross-cohort ordering only if the undercount changed sharply between cohorts.

**Duration confounding for the newest cohorts.** Real and acknowledged (section 5). The
2020–24 cohort's education is the best in the file; its wage residual at very short duration is not.
With only 2023 and 2024 ACS plus a 2023 IPUMS reading, the cohort effect for 2020–24 arrivals is
weakly identified. The ACS 1-year files for 2005–2019 would fix this and were not obtainable in
time.

**Selective return migration differing by cohort.** Bounded in section 6. Overturning the earnings
ranking needs implausible cross-cohort differences in leaver shares; overturning the education
ranking needs more.

I looked for a cut in which the education ordering reverses and did not find one: it holds crude and
age-standardised, in both sexes separately, at matched durations of roughly six years for three
different cohorts, and in both the IPUMS and ACS lanes with different education variables and
different comparison groups. The earnings ordering is less robust — it reverses for the newest
male cohorts when duration is not held fixed, which is section 5's caveat.

---

## Sources

- **IPUMS USA census/ACS panel**, 1980/1990/2000 5% censuses and 2010/2023 ACS, 44,393,133 person
  records, local DuckDB `immigration_microdata.duckdb`, table `ipums_usa_borjas_panel`, accessed
  read-only 2026-09-18. Variable availability and the `BPL >= 150` foreign-born rule per the project
  memory note on this panel.
- **ACS 1-year PUMS 2023**, person file, `acs_pums_2023_person.zip` (staged locally), accessed
  2026-09-18. **ACS 1-year PUMS 2024**, person file,
  `data/external/acs_pums_2024_1yr/csv_pus.zip`, accessed 2026-09-18.
- **ACS PUMS 2024 data dictionary**, `data/external/acs_pums_dict/PUMS_Data_Dictionary_2024.csv`,
  used for the `POBP` birthplace labels, accessed 2026-09-18.
- **Akee, Chin & Crown**, NBER working paper w35582 (Aug 2026), via ladder entry 92 in
  `research/immigration-confidence-ladder.md`. Used for the return-migration leaver share and the
  70-to-30-log-point entry-gap statement. Not independently re-read for this memo.
- **CBP Nationwide Encounters**, FY2021–FY2024 file
  `https://www.cbp.gov/sites/default/files/2024-10/nationwide-encounters-fy21-fy24-aor.csv`
  (retrieved 2026-09-18, 5,767,158 bytes, saved to
  `data/external/cbp/nationwide-encounters-fy21-fy24-aor.csv`) and the FY2022–FY2025 file already
  staged at `data/external/cbp/nationwide-encounters-fy22-fy25-aor.csv`. Landing page:
  `https://www.cbp.gov/newsroom/stats/nationwide-encounters`. Shares computed here, not taken from
  CBP's own tabulations.
- **INEGI, grado promedio de escolaridad**, population aged 15 and over, 2000–2020, from Censo de
  Población y Vivienda 2000/2010/2020, Conteo 2005 and Encuesta Intercensal 2015:
  `https://cuentame.inegi.org.mx/poblacion/escolaridad.aspx`, fetched 2026-09-18. Quoted verbatim in
  section 8.
- **INEGI, Características educativas de la población**, 2020 census attainment distribution for
  ages 15 and over: `https://www.inegi.org.mx/temas/educacion/`, fetched 2026-09-18.
- **Chiquiar, Daniel and Gordon H. Hanson**, "International Migration, Self-Selection, and the
  Distribution of Wages: Evidence from Mexico and the United States", NBER working paper 9242
  (October 2002), the working-paper version of *Journal of Political Economy* 113(2) (2005).
  Retrieved in full from `http://papers.nber.org/papers/w9242.pdf` on 2026-09-18, 57 pages. Both
  passages in section 8 are quoted from that file.
- **Fernández-Huertas Moraga, Jesús**, "New Evidence on Emigrant Selection", *Review of Economics
  and Statistics* 93(1) (2011), 72–96. Published abstract quoted from the RePEc/EconPapers record,
  `https://econpapers.repec.org/RePEc:tpr:restat:v:93:y:2011:i:1:p:72-96`, fetched 2026-09-18. The
  article PDF is subscription-restricted and was not retrieved, so nothing beyond the abstract is
  cited.
- Analysis code and every table as CSV:
  `infra/immigration-fiscal/arrival_cohorts_2026_09_18/` (`ipums_cohorts.py`, `acs_cohorts.py`,
  `entry_quality.py`, `bounds.py`, `origin_relative.py`, `cbp_nationality.py`, `stage_acs.py`,
  `derived/*.csv`).

## Revisions

- 2026-09-23: The gap left open in section 8 and flagged in section 11 is now filled. That gap
  was an origin attainment distribution by birth cohort. The
  [schooling-position lane](../infra/immigration-fiscal/schooling_selection_position_2026_09_23/RESULT.md)
  (ladder 197) places each adult arrival among Mexicans of the same sex and birth year, using the
  INEGI 2000, 2010 and 2020 census tabulations. Arrivals rank at a mean percentile of 0.51–0.56
  in every cohort from 1975–79 to 2020–23, with no rise from cohort to cohort. That confirms the
  section 8 reading, which rejects rising selectivity, on the decisive cut. The level claim that
  migrants are "a little above the median" depends on US measurement: an undercount of the
  least-schooled by 1.19–2.36 brings each cohort to the median. Concept affected: the selection of
  Mexican arrival cohorts on schooling.
