# Mexico-born returnees against Mexico-born people still in the US, 2018 and 2023

**Verdict:** Returnees have less schooling than the Mexico-born who were in the United States at
the start of the same five-year window and are still there. Exit therefore removes the less
schooled, and the US stock is positively selected by return. Men carry the result. With male
stayers reweighted to the returnees' age bands, men who went back to Mexico are 7.6 ± 1.6 points
less likely to hold any tertiary schooling in 2018 and 6.4 ± 2.0 points less likely in 2023.
They also hold 1.41 ± 0.19 and 0.75 ± 0.21 fewer years of schooling. The women's gaps are −6.5 ± 3.7 and −1.0 ± 4.8 points and −0.51 ± 0.39 and −0.06 ± 0.55 years, and none
reaches two standard errors. Pooled over sex-by-age cells, the gaps are −7.4 ± 1.5 and −5.5 ± 1.9
points and −1.24 ± 0.18 and −0.63 ± 0.21 years [CALCULATION: compare.py; DATA:
derived/comparison.csv, spec `main`].

For men and pooled, the tertiary sign survives every sensitivity in both waves. That includes the
most severe non-citizen undercount (k = 1.75), which leaves 2023 pooled at −2.3 ± 1.8 points. The
mean-years sign survives every sensitivity in 2018. In 2023 it flips at k = 1.75 (men +0.08 ± 0.21)
and shrinks to −0.29 ± 0.21 for men when half of US diplomas are read as Mexican secundaria. For
women only the 2018 tertiary sign survives every sensitivity, and it clears two standard errors
only when under a year of college counts as tertiary [DATA: derived/comparison.csv, all specs].

Two findings qualify the headline. Half or more of the tertiary gap comes from stayers who arrived
before age 18, who are 43% of the stock. Against stayers who arrived aged 18 or older, the men's
gap is −3.7 ± 1.6 points and −0.93 ± 0.20 years in 2018. In 2023 it is −3.3 ± 2.0 points and
−0.23 ± 0.21 years, which is not resolved. The effect on the US stock is also small: the window's
returnees equal 3.0% and 2.4% of the stayers, so their exit raises the stock's tertiary share by
0.23 and 0.13 points [CALCULATION: derived/audit.json `universe_main`, `stock_shift`;
derived/comparison.csv, spec `f_stayers_arrived_as_adults`].

Model self-report: claude-opus-5-5 (Opus 5.5), lane teammate, 2026-09-26. No commit; the parent
integrates.

## What is compared

**Returnees** are read from the ENADID lane and not recomputed [DATA:
`enadid_return_selectivity_2026_09_22/derived/return_migrants_by_schooling.csv`, group
`returnee_from_us`]. They are Mexico-born, aged 20–64, and resident in Mexico at the interview.
They lived in the US five years before it, in August 2013 for the 2018 wave and August 2018 for
2023. The samples are n = 969 (weighted 270,023) and n = 647 (202,515), and 81.4% and 82.3% are men
[DATA: that lane's RESULT.md, which 44 gates in `compare.py` match number for number].

**Stayers** come from the ACS one-year person PUMS of the same year. The universe is `POBP` 303,
`AGEP` 20–64 and `YOEP` ≤ year − 5, with group quarters kept. The samples are n = 67,452 (weighted
9,057,217) in 2018 and 67,271 (8,479,130) in 2023, and 52.3% are men in both years. Group quarters
hold 0.95% and 0.98% of the weighted universe (1,483 and 1,684 records). Schooling is allocated
(`FSCHLP` = 1) for 12.2% and 14.5% [DATA: derived/audit.json `universe_main`].

**Schooling.** The ENADID bands are INEGI's `niv_esc`. ACS `SCHL` goes through the shared scale of
`schooling_selection_position_2026_09_23`, whose map and years are imported, not copied. On that
scale, `SCHL` ≤ 11 is below lower secondary, 12 is lower secondary (grade 9), 13–18 is upper
secondary and 19–24 is tertiary. A gate checks this against the brief's mapping. ENADID mean years
are `esco_acum`. On the ACS side they come from the shared scale, which scores every degree from a
bachelor's up at 16.5 years. If a graduate degree adds two years, the ACS stayer mean is understated
by about 0.04 years in 2018 and 0.05 in 2023. That estimate uses graduate shares of 1.8% and 2.6%;
the two years are an assumption [CALCULATION: share × 2]. The understatement makes the gaps look
smaller, not larger.

**Standardization and errors.** Stayer cells are reweighted to the returnees' `weighted_pop`,
which is held fixed. By sex the cells are the age bands within sex; pooled, they are the sex-by-age
cells. The stayer SE is the successive-difference replicate SE over `PWGTP1`–`80`, with negative
and zero replicate weights kept. The returnee SE is the ENADID lane's design-based SE for the
slice, and the two combine in quadrature.

## Anchors, gated before any result

| Year | B05006 Mexico row | MOE (90%) | PUMS, `POBP` 303, `CIT` 4–5 | Gap | PUMS replicate SE | Gap in PUMS SEs |
|---|---:|---:|---:|---:|---:|---:|
| 2018 | 11,171,893 | 79,577 | 11,182,111 | +10,218 (+0.09%) | 56,166 | +0.18 |
| 2023 | 10,918,205 | 87,367 | 10,882,105 | −36,100 (−0.33%) | 56,563 | −0.64 |

[SOURCE: data.census.gov table API, `ACSDT1Y2018.B05006` and `ACSDT1Y2023.B05006`, United States,
retrieved 2026-09-26, URLs in derived/anchor.csv; DATA: derived/anchor.csv]

The keyless `api.census.gov` table endpoint redirected to `missing_key.html`, so the anchor uses
data.census.gov, as the brief allows. The 2023 gap is over 0.2%. PUMS person weights equal the
full ACS weight times a subsampling factor, raked to published totals by householder status, race,
Hispanic origin, sex and age. Place of birth is not a control, so the Mexico-born total carries the
subsample's own sampling error [SOURCE: ACS 2023 PUMS Accuracy of the Data, "Weighting",
https://www2.census.gov/programs-surveys/acs/tech_docs/pums/accuracy/2023AccuracyPUMS.pdf]. The gap
is 0.64 of that error. B05006 counts the foreign-born, so the anchor excludes people born in Mexico
to a US-citizen parent (`CIT` 3). The comparison keeps them, because ENADID's universe is
birthplace; they are 2.2% and 2.5% of the stayers [DATA: audit.json].

## Results, main specification

Shares in percent, differences in points, mean years in years. The "standardized" stayer column is
reweighted to the returnees' ages within sex, or to their sex-by-age cells for "Pooled"
[DATA: derived/comparison.csv; CALCULATION: compare.py].

**2018**

| Group | Measure | Returnee | SE | Stayer, standardized | SE | Difference | SE | Stayer, raw | Raw difference | SE |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Men | Less than lower secondary | 40.2 | 2.3 | 29.1 | 0.3 | +11.1 | 2.3 | 31.3 | +8.9 | 2.3 |
| Men | Lower secondary | 30.9 | 2.0 | 8.2 | 0.2 | +22.7 | 2.0 | 8.0 | +22.9 | 2.0 |
| Men | Upper secondary | 18.7 | 1.6 | 44.9 | 0.4 | −26.2 | 1.6 | 43.3 | −24.6 | 1.6 |
| Men | Tertiary | 10.2 | 1.6 | 17.8 | 0.2 | −7.6 | 1.6 | 17.4 | −7.2 | 1.6 |
| Men | Mean years | 8.66 | 0.19 | 10.07 | 0.02 | −1.41 | 0.19 | 9.88 | −1.22 | 0.19 |
| Women | Less than lower secondary | 29.5 | 4.9 | 26.9 | 0.3 | +2.6 | 4.9 | 29.5 | −0.1 | 4.9 |
| Women | Lower secondary | 28.6 | 4.0 | 7.9 | 0.2 | +20.6 | 4.0 | 7.8 | +20.7 | 4.0 |
| Women | Upper secondary | 26.5 | 4.1 | 43.2 | 0.3 | −16.7 | 4.1 | 41.7 | −15.2 | 4.1 |
| Women | Tertiary | 15.5 | 3.7 | 22.0 | 0.3 | −6.5 | 3.7 | 21.0 | −5.5 | 3.7 |
| Women | Mean years | 9.89 | 0.39 | 10.40 | 0.02 | −0.51 | 0.39 | 10.16 | −0.27 | 0.39 |
| Pooled | Less than lower secondary | 38.2 | 2.1 | 28.7 | 0.3 | +9.5 | 2.1 | 30.5 | +7.8 | 2.1 |
| Pooled | Lower secondary | 30.4 | 1.9 | 8.1 | 0.2 | +22.3 | 1.9 | 7.9 | +22.5 | 1.9 |
| Pooled | Upper secondary | 20.2 | 1.5 | 44.6 | 0.3 | −24.4 | 1.6 | 42.5 | −22.4 | 1.5 |
| Pooled | Tertiary | 11.2 | 1.5 | 18.6 | 0.2 | −7.4 | 1.5 | 19.1 | −7.9 | 1.5 |
| Pooled | Mean years | 8.89 | 0.18 | 10.13 | 0.02 | −1.24 | 0.18 | 10.01 | −1.12 | 0.18 |

**2023**

| Group | Measure | Returnee | SE | Stayer, standardized | SE | Difference | SE | Stayer, raw | Raw difference | SE |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Men | Less than lower secondary | 28.4 | 2.3 | 27.9 | 0.3 | +0.6 | 2.4 | 29.7 | −1.3 | 2.4 |
| Men | Lower secondary | 34.5 | 2.6 | 6.4 | 0.2 | +28.1 | 2.6 | 6.5 | +28.0 | 2.6 |
| Men | Upper secondary | 23.6 | 2.3 | 45.8 | 0.3 | −22.2 | 2.3 | 44.7 | −21.1 | 2.3 |
| Men | Tertiary | 13.5 | 1.9 | 20.0 | 0.3 | −6.4 | 2.0 | 19.1 | −5.6 | 2.0 |
| Men | Mean years | 9.34 | 0.21 | 10.09 | 0.03 | −0.75 | 0.21 | 9.90 | −0.56 | 0.21 |
| Women | Less than lower secondary | 26.2 | 4.3 | 23.9 | 0.3 | +2.3 | 4.3 | 26.4 | −0.2 | 4.3 |
| Women | Lower secondary | 21.7 | 4.2 | 5.8 | 0.2 | +16.0 | 4.2 | 6.3 | +15.4 | 4.2 |
| Women | Upper secondary | 27.4 | 4.9 | 44.7 | 0.4 | −17.3 | 4.9 | 43.9 | −16.5 | 4.9 |
| Women | Tertiary | 24.6 | 4.8 | 25.7 | 0.3 | −1.0 | 4.8 | 23.4 | +1.2 | 4.8 |
| Women | Mean years | 10.57 | 0.55 | 10.63 | 0.03 | −0.06 | 0.55 | 10.36 | +0.21 | 0.55 |
| Pooled | Less than lower secondary | 28.0 | 2.1 | 27.2 | 0.3 | +0.9 | 2.1 | 28.1 | −0.1 | 2.1 |
| Pooled | Lower secondary | 32.2 | 2.3 | 6.3 | 0.2 | +26.0 | 2.3 | 6.4 | +25.8 | 2.3 |
| Pooled | Upper secondary | 24.3 | 2.1 | 45.6 | 0.3 | −21.3 | 2.1 | 44.3 | −20.0 | 2.1 |
| Pooled | Tertiary | 15.5 | 1.8 | 21.0 | 0.2 | −5.5 | 1.9 | 21.1 | −5.7 | 1.8 |
| Pooled | Mean years | 9.56 | 0.20 | 10.19 | 0.02 | −0.63 | 0.21 | 10.12 | −0.56 | 0.20 |

The two middle bands differ by 16–28 points in opposite directions. Most of that is the ACS
instrument, not selection [INFERENCE]; see "Two ACS instrument problems" below. The full file also
carries each age band and each sex-by-age cell, raw.

## Does the sign survive?

Standardized difference, returnee minus stayer (SE). "Added" rows go beyond the brief; each one is
explained further down [DATA: derived/comparison.csv; CALCULATION: compare.py].

**Tertiary, points**

| Spec | 2018 men | 2018 women | 2018 pooled | 2023 men | 2023 women | 2023 pooled |
|---|---:|---:|---:|---:|---:|---:|
| Main | −7.6 (1.6) | −6.5 (3.7) | −7.4 (1.5) | −6.4 (2.0) | −1.0 (4.8) | −5.5 (1.9) |
| `YOEP` ≤ year − 6 | −7.6 (1.6) | −6.5 (3.7) | −7.4 (1.5) | −6.5 (2.0) | −1.1 (4.8) | −5.5 (1.9) |
| (a) `SCHL` 18 as tertiary | −10.8 (1.6) | −10.0 (3.7) | −10.6 (1.5) | −10.4 (2.0) | −5.5 (4.8) | −9.5 (1.9) |
| (b) half of diplomas as secundaria | −7.6 (1.6) | −6.5 (3.7) | −7.4 (1.5) | −6.4 (2.0) | −1.0 (4.8) | −5.5 (1.9) |
| (c) allocated schooling dropped | −6.1 (1.6) | −5.8 (3.7) | −6.0 (1.5) | −5.0 (2.0) | −0.5 (4.8) | −4.2 (1.9) |
| (d) households only, added | −7.7 (1.6) | −6.5 (3.7) | −7.5 (1.5) | −6.5 (2.0) | −1.0 (4.8) | −5.6 (1.9) |
| (f) stayers who arrived aged 18+, added | −3.7 (1.6) | −1.9 (3.7) | −3.4 (1.5) | −3.3 (2.0) | +3.6 (4.8) | −2.1 (1.9) |
| Undercount k = 1.10 | −7.1 (1.6) | −5.9 (3.7) | −6.9 (1.5) | −5.9 (2.0) | −0.5 (4.8) | −5.0 (1.9) |
| Undercount k = 1.25 | −6.4 (1.6) | −5.2 (3.7) | −6.2 (1.5) | −5.2 (2.0) | +0.2 (4.8) | −4.3 (1.8) |
| Undercount k = 1.75 | −4.5 (1.6) | −3.0 (3.7) | −4.2 (1.5) | −3.3 (2.0) | +2.2 (4.8) | −2.3 (1.8) |

**Mean years of schooling**

| Spec | 2018 men | 2018 women | 2018 pooled | 2023 men | 2023 women | 2023 pooled |
|---|---:|---:|---:|---:|---:|---:|
| Main | −1.41 (0.19) | −0.51 (0.39) | −1.24 (0.18) | −0.75 (0.21) | −0.06 (0.55) | −0.63 (0.21) |
| `YOEP` ≤ year − 6 | −1.41 (0.19) | −0.50 (0.39) | −1.24 (0.18) | −0.75 (0.21) | −0.07 (0.55) | −0.63 (0.21) |
| (a) `SCHL` 18 as tertiary | −1.44 (0.19) | −0.54 (0.39) | −1.27 (0.18) | −0.79 (0.21) | −0.11 (0.55) | −0.67 (0.21) |
| (b) half of diplomas as secundaria | −0.96 (0.19) | −0.07 (0.39) | −0.79 (0.18) | −0.29 (0.21) | +0.40 (0.55) | −0.17 (0.21) |
| (c) allocated schooling dropped | −1.26 (0.20) | −0.44 (0.39) | −1.11 (0.18) | −0.58 (0.21) | 0.00 (0.55) | −0.48 (0.21) |
| (d) households only, added | −1.41 (0.19) | −0.50 (0.39) | −1.24 (0.18) | −0.75 (0.21) | −0.07 (0.55) | −0.63 (0.21) |
| (e) 2023 no-schooling step removed, added | — | — | — | −1.00 (0.21) | −0.27 (0.55) | −0.87 (0.20) |
| (f) stayers who arrived aged 18+, added | −0.93 (0.20) | 0.00 (0.39) | −0.75 (0.18) | −0.23 (0.21) | +0.52 (0.55) | −0.10 (0.21) |
| Undercount k = 1.10 | −1.28 (0.19) | −0.39 (0.39) | −1.12 (0.18) | −0.62 (0.21) | +0.05 (0.55) | −0.50 (0.21) |
| Undercount k = 1.25 | −1.12 (0.19) | −0.23 (0.39) | −0.95 (0.18) | −0.43 (0.21) | +0.21 (0.55) | −0.32 (0.21) |
| Undercount k = 1.75 | −0.64 (0.19) | +0.23 (0.39) | −0.48 (0.18) | +0.08 (0.21) | +0.67 (0.55) | +0.19 (0.21) |

Reading the tables:

- For men and pooled, the tertiary gap is negative under every spec in both waves. It widens when
  under a year of college counts as tertiary (a). It narrows when allocated records are dropped
  (c), because allocated records hold tertiary schooling at 26.8% and 27.3% against 18.0% and
  20.1% for reported ones [DATA: audit.json `universe_main`]. The schooling-selection lane notes
  that the donors are not matched on birthplace [UNVERIFIED: stated in
  `schooling_selection_position_2026_09_23/acs_pums_check.py`, not checked against Census
  documentation]. Adult-arrival stayers (f) and the undercount narrow the gap too.
- For mean years, men and pooled are negative under every spec in 2018. In 2023 the sign flips only
  at k = 1.75. That factor raises the weight of every low-schooled non-citizen by 75%, the most
  severe value the schooling-selection lane used. Specs (b) and (e) pull the 2023 men's gap in
  opposite directions, to −0.29 and −1.00 years, so read them together.
- Women are 18–19% of returnees. Their gaps clear two standard errors only once: 2018 tertiary
  under (a), at −10.0 ± 3.7.
- The ENADID lane's pattern against Mexican non-migrants holds against US stayers too: negative
  selection is a male result. Against non-migrants, returnee men ran −1.59 and −1.33 years [DATA:
  ENADID RESULT.md]. Against male US stayers they run −1.41 and −0.75.

## Child arrivals in the stayer stock (added sensitivity f)

In both years, 29.2% and 30.6% of stayers arrived before age 15, and they hold tertiary schooling
at 30.8% and 32.3%. The 57.2% and 56.8% who arrived at 18 or older hold it at 14.9% and 16.9%
[DATA: audit.json `universe_main`; arrival age from `AGEP` and `YOEP`, within about a year]. Much of
the stayers' advantage is therefore American schooling of the 1.5 generation [INFERENCE]. ENADID
does not record when returnees went north, so the returnee side cannot be split the same way.

Spec (f) keeps only stayers who arrived aged 18 or older. Against them, the men's tertiary gap is
about half the main one: −3.7 ± 1.6 points in 2018 and −3.3 ± 2.0 in 2023. The mean-years gap is
−0.93 ± 0.20 and −0.23 ± 0.21. Take any child arrivals among returnees to be better schooled than
the adult-arrival returnees, as child arrivals are among stayers. Then the within-adult-arrival gap
is at least as negative as (f). Each question takes a different figure. For the US stock as it is,
the all-stayer comparison answers it. For an arrival-cohort analysis restricted to adult arrivals,
use (f) as the least-negative bound. The 2018 bound is resolved and the 2023 one is not.

## Two ACS instrument problems

**Secundaria reported as a US diploma.** ACS stayers report exactly grade 9 at 6–8%. Returnees
hold lower secondary at 22–35%, and Mexican non-migrants at 25.6% (2018) and 26.0% (2023)
[DATA: ENADID RESULT.md]. Meanwhile 28.5% and 29.5% of stayers report a US diploma or GED [DATA:
audit.json]. The schooling-selection lane found the same signature: arrival cohorts from 2000–04 on
hold complete upper secondary at 1.4–2.1 times Mexico's rate and secundaria at 0.47–0.68 times it
[DATA: `schooling_selection_position_2026_09_23/RESULT.md` §2]. The middle-band differences above
are therefore not selection estimates. Tertiary is untouched. Reading half the diplomas as
secundaria (b) lowers the stayer mean by 0.43–0.44 years and brings the stayers' lower-secondary
share to about 21–22%, near Mexico's 26%. Half is thus a plausible share, not an extreme one
[INFERENCE]. The 2023 men's gap is better read as −0.29 to −0.75 years than as the main figure
alone, and the 2020 step below pulls the other way.

**A 2020 step in ACS no-schooling reports.** Among Mexico-born adults aged 20–64, the share
reporting no schooling completed jumps between the 2019 and 2020 ACS and stays at the new level.
The grade-8-or-less total keeps its gradual decline [DATA: derived/acs_no_schooling_break.csv, from
IPUMS extract 3] [2026-09-26, later: in raw totals only; see Revisions]:

| ACS year | No schooling | Grade 8 or less, incl. none | Grade 9 | No schooling, 1990–99 arrivals |
|---|---:|---:|---:|---:|
| 2017 | 5.14 | 30.64 | 8.22 | 4.90 |
| 2018 | 5.39 | 30.05 | 7.92 | 4.89 |
| 2019 | 5.55 | 29.22 | 8.14 | 5.49 |
| 2020 | 8.45 | 28.09 | 6.60 | 8.54 |
| 2021 | 8.66 | 29.00 | 6.63 | 8.75 |
| 2023 | 8.92 | 27.65 | 6.50 | 9.52 |
| 2024 | 9.11 | 27.25 | 6.34 | 10.05 |

The fixed 1990–99 arrival cohort shows the same step, so this is a reporting or processing change,
not a population change. The cause is not identified here [INFERENCE]. The step moves reports from
grades 1–9 to none. It cuts the 2023 stayer mean years and shifts some grade-9 reports into the
bottom band. The tertiary share is unaffected. Within the stayer universe, no-schooling reports
rose from 5.46% to 9.12%. Spec (e) re-scores the 40.1% excess at the 6.69-year mean of grades 1–9,
which sets the 2023 no-schooling score to 2.68 years [DATA: audit.json `break_2023`]. The men's 2023
gap then moves from −0.75 to −1.00 years. The 2018 wave predates the step.

## Short-stay returnees against arrivals still in the US

Some returnees left Mexico inside the window and came back inside it. The ENADID lane measures
their schooling only through the household link: 77.4% and 77.8% of returned departure rows link
to a Mexico-born member aged 20–64 [DATA: ENADID `departures_by_schooling.csv`,
`linked_20_64_coverage`]. That link reaches 91.8% and 91.3% of returnees of any age or birthplace,
and it can never reach people still abroad [DATA: ENADID RESULT.md]. The ACS comparator is the
Mexico-born aged 20–64 with `YOEP` from year − 5 to year. The ACS figure is also shown reweighted to
the men's share of all returned departures (74.0% and 84.7%), the only sex split ENADID carries for
this group.

| Wave | Coding | Band | Short-stay returnees | SE | Recent arrivals | SE | Difference | SE | Recent arrivals, sex-reweighted | Difference | SE |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2018 | main | Tertiary | 28.1 | 2.5 | 27.0 | 0.8 | +1.2 | 2.6 | 25.8 | +2.4 | 2.6 |
| 2018 | (a) | Tertiary | 28.1 | 2.5 | 30.1 | 0.9 | −2.0 | 2.6 | 28.9 | −0.8 | 2.6 |
| 2018 | main | Less than lower secondary | 26.8 | 2.2 | 24.2 | 0.7 | +2.6 | 2.3 | 25.2 | +1.6 | 2.3 |
| 2023 | main | Tertiary | 22.6 | 2.3 | 28.4 | 0.7 | −5.8 | 2.4 | 26.2 | −3.6 | 2.5 |
| 2023 | (a) | Tertiary | 22.6 | 2.3 | 30.9 | 0.8 | −8.3 | 2.5 | 28.6 | −6.0 | 2.5 |
| 2023 | main | Less than lower secondary | 22.2 | 2.3 | 21.5 | 0.7 | +0.7 | 2.4 | 23.2 | −1.1 | 2.5 |

[DATA: derived/comparison.csv, specs `short_stay_recent_arrivals` and
`short_stay_recent_arrivals_a`; the middle bands carry the diploma problem and are in the file]

What it can show: short-stay returnees are not better schooled than people who arrived in the same
window and stayed. They are level with them in 2018 (every difference under one SE) and below them
in 2023, by 3.6–8.3 points (1.5–3.4 SE) depending on coding and weighting. The ENADID lane
contrasted short-stay returnees (28.1% and 22.6% tertiary) with endpoint returnees (11.2% and
15.5%). Part of that contrast reflects recent arrivals being better schooled than the older stock:
27–28% against 19–21% tertiary [DATA: derived/comparison.csv].

What it cannot show:

- **Different frames.** ENADID's household reports miss whole-household moves. Its still-abroad
  departures are 41% (2018) and 70% (2023) of the ACS count of Mexico-born recent arrivals of all
  ages: 419,882 against 1,015,194, and 850,752 against 1,220,607 [DATA: audit.json
  `short_stay_context`].
- **Timing.** `YOEP` counts January–July arrivals of year − 5, which fall before ENADID's August
  start. It also records the most recent entry, so earlier migrants who re-entered appear as recent
  arrivals.
- **Composition.** The sex reweighting uses all ages, the linked subset is not age-standardized,
  and ACS recent arrivals may still return after their survey.

## What return does to the US stock

The five-year window's returnees number 270,023 and 202,515. Beside 9,057,217 and 8,479,130
stayers, that is 3.0% and 2.4%. Had they stayed, the stock's tertiary share would be 0.23 points
lower (2018) and 0.13 points lower (2023), and its mean schooling 0.03 and 0.01 years lower
[CALCULATION: −gap × N_returnee ÷ (N_stayer + N_returnee) on the raw main-spec gaps; audit.json
`stock_shift`]. ENADID counts only returnees living in sampled households at the interview. Those
who died, moved on or live in institutions are missing. The true outflow is therefore larger, and
so is the shift if the missing returnees resemble the observed ones [INFERENCE].
The per-person selection is strong for men, but one window's return barely moves the stock.
Arrival cohorts face several windows, with higher return rates early on; this lane does not size
the cumulative effect.

## What this does not show

- **Schooling is measured at the survey.** For stayers, US schooling after arrival counts, which is
  the 1.5-generation effect above. For returnees, schooling after return counts. Neither side has
  schooling at departure.
- **The five-year window is not a trend.** There are two windows, 2013–2018 and 2018–2023. The
  men's tertiary gap moves from −7.6 to −6.4, a change of 1.1 ± 2.5 points, which is not resolved
  [CALCULATION: independent waves, SEs in quadrature].
- **The ACS covers residents, not all stayers.** Its undercount of unauthorized residents, who have
  less schooling, biases the stayer distribution upward; the k rows price that. People in the US at
  the start of the window who died or moved to a third country are in neither group.
- **ENADID returnees include deportees.** Voluntary and forced return are not separated. Nothing
  here says why anyone returned.
- **Causation.** The gaps describe who returned, not what returning does to anyone.

## Deviations from the brief

1. **2023 PUMS.** The brief said the 2023 file was not local. It is held at
   `sources/immigration-fiscal/data/census/acs_pums_2023_person.zip`, fetched by `acquire/setup.sh`
   from the same URL, and used by other lanes. A fresh download ran at 27 kB/s, about six hours for
   the file [DATA: 20-second rate probe on the partial download], so it was stopped and the partial
   file deleted. `verify_acs_2023.sh` replaces `fetch_acs_2023.sh`. It checks the held copy against
   the file Census serves [DATA: verify_acs_2023.sh output, 2026-09-26]:
   - equal Content-Length (597,292,173 bytes);
   - the central directory and sixteen 16 KiB ranges byte-identical to HTTP range reads;
   - `unzip -tqq`;
   - sha256 `98b6ecb1…d9d4`, as `service_by_ses_2026_09_23` recorded.

   All four passed. No file was added to `acs_pums_years/` and no line to its `download.log`.
2. **Anchor source.** The anchor comes from data.census.gov because the keyless `api.census.gov`
   endpoint redirected to `missing_key.html`. The repository's Census key was not used.
3. **Added specs.** Three sensitivities were added: (d) households only, (e) the 2023 no-schooling
   step and (f) adult-arrival stayers. So was one output, `derived/acs_no_schooling_break.csv`.
4. **Details the brief left open.**
   - (a) scores `SCHL` 18 at 13 years, the least that reading implies.
   - (b) moves `SCHL` 16 and 17 as the brief says. The schooling-selection lane moved regular
     diplomas only. GEDs are 3.5% and 4.4% of stayers [DATA: audit.json], so the two readings
     differ by 0.05–0.07 years of stayer mean schooling [CALCULATION: 0.5 × 3 years × GED share].
   - The short-stay comparison adds a sex-reweighted ACS figure.
   - The ENADID gates also cover the departure-table numbers read here: weighted counts and the
     returned men's share.

## For other lanes

The 2020 no-schooling step (above) affects any lane that splits the bottom of the ACS schooling
distribution, or scores years from `SCHL` or `EDUCD`, across the 2019/2020 boundary. One example is
the C1/C2 split (none or primary incomplete against primary) in
`schooling_selection_position_2026_09_23` for cohorts observed in the 2020–2024 ACS. That lane is
exposed but was not checked here.

## Reproduce

```sh
bash infra/immigration-fiscal/return_vs_us_stayers_2026_09_26/verify_acs_2023.sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/return_vs_us_stayers_2026_09_26/compare.py
uv run --no-project python3 -m pytest infra/immigration-fiscal/return_vs_us_stayers_2026_09_26/ -q
```

On 2026-09-26 both runs of `compare.py` exited 0 and wrote byte-identical `derived/` files (sha256
compared file by file). All 13 tests passed. The instrument here is arithmetic on public
microdata. Which comparisons to foreground (all stayers or adult arrivals, per-person gaps or stock
effect) is a framing choice, flagged above [FRAMING-SENSITIVE; see notes/llm-bias-caveat.md].

## Revisions

- 2026-09-26, later: [`acs_schooling_break_2026_09_26`](../acs_schooling_break_2026_09_26/RESULT.md) measured the step more closely. Three
  changes follow for this lane.
  - **The step is not new.** The dataset integrity audit first reported it on 2026-09-23 (F6 in
    `dataset_integrity_2026_09_23/acs.md`).
  - **The step reaches further than stated above.**
    - Once the band's own decline is removed, "grade 8 or less" also steps up, by 0.8–1.0 points.
    - Grade 9 supplies about a quarter of the lost reports.
    - Natives aged 20–64 gain 0.20 points of "none".
    - The Census Bureau documents over-reporting of "No schooling completed" in mail and
      internet responses. It changed the question for the 2025 ACS, which will be a second break.
  - **Spec (e) has a preferred alternative.** The flow-rate correction places the moved reports
    where they came from, including grade 9. It puts the men's 2023 mean-years gap at about
    −0.92, against spec (e)'s −1.00 and the main −0.75. This is scaled analytically, not re-run
    in `compare.py`. The negative selection of male returnees stands.
