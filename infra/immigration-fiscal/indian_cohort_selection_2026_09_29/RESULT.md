claude-opus-5-5

**Verdict:** The India-born flow that household surveys can see is not becoming less selected. At a fixed 0–5
years since arrival, ages 25–54, each arrival cohort since 1995 sits at the 75th–78th percentile of the US white
education distribution of its own year: 75.5 (1995–2000 arrivals), 76.6 (2005–10) and 78.2 (2018–23) on the census
reference; 77.7, 76.6, 76.3, 76.9 and 77.8 for the five-year windows from 2000–04 to 2020–24 on the
selection-curve reference. The less-selected wave was the 1975–94 arrivals (69.0–72.7), the family-preference years after the 1965 Act [INFERENCE on the cause]. They sit
inside the "1965–1990 doctor/engineer" window the question assumes. Only the 1970–74 cohort matches today's level (78.3 at 6–10 years).
Wage-earnings percentiles at 6–10 years in the US are flat to rising (ACS 62.1 for 1990s arrivals, 64.3 and 63.8
for 2010–14 and 2015–19). The parents of today's 0.83M US-born children with an India-born parent are 42% 2000–09
arrivals and 39% post-2010 arrivals. Their education percentile is flat since 2005 (74.1 → 74.7) and their earnings
percentile is up 8 points (57.5 → 65.7). Pushed through the selection curve's G1→G2 slopes, the future adult G2
comes out 0.1–1.8 points above today's adult G2 on education and 2.3–4.5 points above on earnings. On the Indian ledger's
gradient of $485 per earnings point, that is about +$1.1k to +$2.2k per adult-year [INFERENCE]. The measured
change is a mix shift, not a skill decline. Physicians fell from 12% of employed pre-1980 arrivals to 1% of recent
ones, and computing rose from 14% to 36%. The open risk is the post-2021 irregular inflow, which these surveys
under-cover. CBP recorded 64k–97k encounters of Indian nationals a year in FY2022–24. The unauthorized estimates
disagree threefold (DHS 220k in 2022, Pew 680k in 2023). A bound is in §5.

The stock (§6): of 3.22M India-born residents in the ACS 2024, the pre-1990 waves are 13% and mostly past 60, and
post-2010 arrivals are 51%. The 1.62M US-born with an India-born parent are 61% under 18 (CPS 2024–25). By home
language (§7), the waves shifted from Gujarati and Punjabi toward Hindi and Telugu. Telugu went from 4–5% of the
pre-1990 waves to 21% of 2020+ arrivals, and Gujarati and Punjabi together fell from 25–30% to 11%. Punjabi speakers are the one
low-selection sub-population: education percentile 47, 17% of the employed in trucking, 21% self-employed. Language is a region proxy, not caste.

Model self-report: claude-opus-5-5. Times from `date`: started 2026-09-29 ~22:00 JST; verified 23:50 JST.
Descriptive throughout: arrival cohorts observed in repeated cross-sections are synthetic cohorts. Stayers are
measured; emigrants and non-respondents are not. [FRAMING-SENSITIVE: "selection" is measured as the position in
the US third-plus-generation non-Hispanic white distribution of the same survey year and age band (the
selection-curve lane's definition). It is not measured as the position in India's distribution, and it is not measured as absolute schooling.]

## Gates and validation

| check | result |
|---|---|
| India G1 education percentile, CPS 2015–2025, from this lane's code (imports `selection_curve_2026_09_27/cps_curve.py`) | **PASS** 73.48311 vs 73.4831 [DATA: `derived/gate.json`] |
| ACS India-born vs CPS India G1, same years and age standardisation | ACS −2.35 (education), −0.64 (earnings) in 2015–2024; −2.04 / +0.30 in 2005–2014 [DATA: `derived/acs_calibration.csv`] |
| Census panel restricted to detailed birthplace `BPLD` 52100 | the general `BPL` 521 also holds Pakistan, Bangladesh, Sri Lanka, Myanmar and Bhutan (≈20% of records); using it cut BA+ by ~10 points. Fixed before any result was read |
| Rerun from scratch (caches deleted, all six steps), byte-identical `derived/` | **PASS**: all six steps exited 0; all 14 outputs IDENTICAL, finished 23:50 JST (first run 23:14, 9 outputs) [DATA: `derived/verify.json`] |

The ACS–CPS level gap (~2 points on education) is an instrument difference; all within-ACS comparisons use one
instrument. Where an ACS level meets a CPS level (projection, measure b) only the ACS change is used.

## 1. Cohort selection at fixed duration

### 1a. The long series, 1970–2023 (IPUMS USA 5% censuses 1980–2000, ACS 2010 and 2023)

Ages 25–54, age-standardised to the view's pooled India-born age mix. The census reference is US-born whites of the same
year and five-year age band. The CPS reference (G3+ NH white) is only possible from 1994 on.
[CALCULATION: `census_ysm.py` → `derived/census_ysm.csv`]

| arrival | observed in | years in US | n | edu pct, census ref | edu pct, CPS ref | BA+ | graduate | white BA+ |
|---|---|---|---|---|---|---|---|---|
| 1970–74 | 1980 | 6–10 | 2,736 | **78.3** | — | 71.0% | 53.7% | 21.3% |
| 1975–80 | 1980 | 0–5 | 2,736 | 69.6 | — | 58.3% | 41.9% | 21.3% |
| 1980–84 | 1990 | 6–10 | 3,534 | 70.5 | — | 65.3% | 35.4% | 26.0% |
| 1985–90 | 1990 | 0–5 | 3,695 | 69.0 | — | 64.0% | 35.7% | 26.0% |
| 1990–94 | 2000 | 6–10 | 6,076 | 72.7 | 72.5 | 71.4% | 44.3% | 30.1% |
| 1995–2000 | 2000 | 0–5 | 9,951 | 75.5 | 75.2 | 79.8% | 38.9% | 30.1% |
| 2000–04 | 2010 | 6–10 | 2,416 | 78.1 | 77.4 | 83.9% | 51.0% | 32.8% |
| 2005–10 | 2010 | 0–5 | 2,681 | 76.6 | 75.9 | 84.1% | 42.8% | 32.8% |
| 2013–17 | 2023 | 6–10 | 3,804 | 77.2 | 76.8 | 89.5% | 58.8% | 44.2% |
| 2018–23 | 2023 | 0–5 | 3,666 | **78.2** | 77.9 | 91.6% | 54.8% | 44.2% |

1980 schooling is years completed: "BA+" is 4+ years of college and "graduate" is 5+ years. The ratio of the Indian BA+ share to
the white share falls (3.3× for 1970–74, 2.1× for 2018–23) because US whites gained degrees. The percentile, which
is what the selection curve uses, does not fall.

### 1b. ACS 2005–2024, one-year arrival detail, CPS G3+ NH white reference

Ages 25–54, 0–5 years since arrival, pooled India-born age mix. Occupation and industry shares are of the employed.
Computing is SOC 15-1; physicians are SOC 29-1060/29-12xx; retail is NAICS 44–45; accommodation and food is
NAICS 72. The status proxy is described in §5. [CALCULATION: `acs_cohorts.py` → `derived/acs_cohorts.csv`, view
`ysm_0_5_age25_54_by5yr`]

| arrival | n | edu pct | earn pct | BA+ | graduate | computing | physicians | retail | accom./food | self-emp. | residual no-BA noncitizen |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2000–04 | 5,974 | 77.7 | 52.7 | 84.2% | 47.2% | 34.4% | 3.7% | 9.8% | 4.3% | 2.9% | 11.5% |
| 2005–09 | 12,867 | 76.6 | 51.5 | 85.0% | 45.4% | 41.4% | 2.7% | 8.5% | 3.3% | 1.9% | 10.1% |
| 2010–14 | 16,806 | 76.3 | 53.5 | 89.0% | 45.7% | 45.7% | 1.4% | 7.7% | 2.8% | 2.2% | 7.0% |
| 2015–19 | 17,447 | 76.9 | 51.8 | 90.8% | 50.9% | 42.3% | 1.1% | 8.1% | 2.1% | 2.2% | 5.9% |
| 2020–24 | 7,540 | 77.8 | 47.5 | 92.5% | 52.5% | 37.8% | 1.5% | 9.0% | 2.0% | 2.0% | 4.8% |

At 6–10 years since arrival (ACS, same rules), education and earnings percentiles are: 1990s arrivals 76.3 and 62.1;
2000s 76.6 and 61.1; 2010–14 76.1 and 64.3; 2015–19 76.1 and 63.8. The CPS gives the same shape on its smaller
samples. At 0–5 years it gives 1990s 76.8, 2000s 78.0, 2010–14 78.3, 2015–19 77.1 and 2020+ 76.7 on education. At
6–10 years it gives 1990s 73.1 and 57.5, 2000s 77.0 and 61.5, 2010–14 79.1 and 66.3, and 2015–19 79.7 and 66.3
[DATA: `derived/cps_cohorts.csv`].

One soft spot: 2020–24 arrivals earn less at 0–5 years (ACS 47.5 against 51–54; CPS 41.1 against 48–54). They
are observed at a shorter mean duration (1.4 years against 2.5–3.7), during the COVID and 2023 tech-layoff years. Their
education is the highest of any cohort. The survey cannot yet tell a weaker cohort from a slow start.

### 1c. Mix by cohort in today's stock (ACS 2021–2024, ages 25–54)

[DATA: `derived/acs_cohorts.csv`, view `stock_2021_2024_age25_54`; durations differ by construction]

| arrival | n | edu pct | earn pct | citizen | physicians | computing | retail | self-emp. | BA field: computer/IT | engineering |
|---|---|---|---|---|---|---|---|---|---|---|
| pre-1980 | 903 | 74.3 | 62.7 | 84.6% | 11.6% | 14.1% | 6.3% | 16.2% | 12.6% | 12.3% |
| 1980–89 | 2,550 | 66.6 | 56.9 | 85.8% | 7.8% | 11.5% | 9.3% | 10.1% | 11.1% | 17.3% |
| 1990–99 | 10,871 | 68.7 | 61.6 | 91.0% | 4.8% | 16.4% | 9.7% | 9.3% | 12.9% | 20.6% |
| 2000–09 | 20,355 | 73.3 | 65.6 | 63.9% | 2.9% | 26.3% | 8.8% | 7.5% | 15.8% | 32.2% |
| 2010–14 | 12,012 | 73.3 | 65.1 | 28.7% | 1.7% | 36.5% | 8.5% | 5.0% | 20.7% | 36.1% |
| 2015–19 | 14,029 | 73.2 | 60.0 | 10.6% | 1.1% | 35.6% | 8.8% | 4.7% | 21.4% | 34.9% |
| 2020+ | 7,540 | 74.7 | 50.8 | 2.4% | 1.0% | 36.4% | 8.5% | 3.4% | 20.0% | 35.4% |

The pre-1980 row is the doctor wave, and it is a small tail of today's stock. The retail share is 6–10% in every cohort. The
motel and gas-station niche (accommodation and food, 2–3%) has not grown. Self-employment has fallen by
cohort. The stock views at all ages 25–64 are age-standardised to the white reference's age mix (the selection-curve rule). They give
recent cohorts lower education (64.5 for 2015–19) because that rule gives the late-life arrivals weight. Those are mostly parents admitted
as immediate relatives. So the fixed-duration views at 25–54 are the selection measure.

## 2. Who the future G2 are

Children 0–17 of the householder, with an India-born householder or spouse, ACS. Parent measures are the mean over
the India-born parents in the household, ages 25–64, on the ACS scale (add ~2.35 for the CPS scale).
[CALCULATION: `derived/acs_future_g2_parents.csv`]

| survey year | US-born children (weighted) | n | parents' edu pct | parents' earn pct | parents BA+ | both parents India-born | parents arrived pre-1990 | 1990–99 | 2000–09 | 2010+ |
|---|---|---|---|---|---|---|---|---|---|---|
| 2005 | 376k | 3,674 | 74.1 | 57.5 | 75.3% | 73.5% | 44.8% | 47.4% | 7.8% | 0% |
| 2010 | 524k | 4,874 | 75.7 | 60.7 | 80.0% | 78.1% | 24.2% | 48.7% | 27.0% | 0.1% |
| 2015 | 654k | 5,950 | 76.2 | 62.6 | 84.5% | 75.2% | 13.7% | 36.4% | 40.5% | 9.5% |
| 2019 | 723k | 6,942 | 75.0 | 64.0 | 85.9% | 75.4% | 8.9% | 26.4% | 44.0% | 20.7% |
| 2023 | 802k | 7,841 | 74.4 | 65.8 | 86.9% | 72.9% | 5.7% | 15.4% | 43.4% | 35.5% |
| 2024 | 827k | 7,573 | 74.7 | 65.6 | 87.0% | 70.8% | 6.5% | 12.6% | 41.8% | 39.1% |

The operator's premise holds on who the parents are. The 2005 children, now 21–38 and entering the adult G2, have
parents who are 45% pre-1990 and 47% 1990s arrivals. The 2024 children have parents who are 42% 2000s and 39% post-2010 arrivals. But on the measure
the selection curve uses, the new parents are no less selected: education percentile is flat and earnings are 8
points higher. The foreign-born children (G1.5, 208k in 2024) have parents 3–15 points lower on earnings because of
duration. They are not part of the G2 projection.

## 3. Projection of the future adult G2

Future G2 = observed G2 + b × Δx. The observed G2 is the selection-curve lane's India G2 in 2015–2025, paired with the
India G1 of 1994–2004 (spec `g1_1994_2004__g2_2015_2025`, read from its `origin_curve.csv`). b is the
cross-origin G1→G2 slope from its `slopes.csv`, or India's own observed step k = (G2 − 50)/(G1 − 50).
[CALCULATION: `project_g2.py` → `derived/projection.csv`] [MODEL: linear carry-over, no change in the G1→G2 process]

| outcome | parents' measure | x then | x now | Δx | slope 0.52/0.55 (all origins) | slope 0.36/0.30 (no Mexico) | India step k | G2 now | future G2 |
|---|---|---|---|---|---|---|---|---|---|
| education | (a) all India-born 25–64, CPS 2021–25 vs 1994–2004 | 71.1 | 74.5 | +3.4 | +1.8 | +1.2 | +3.8 (k 1.10) | 73.1 | 74.3–76.8 |
| education | (b) parents of US-born children, ACS 2023–24 vs 2005 | 74.1 | 74.5 | +0.4 | +0.2 | +0.1 | +0.4 | 73.1 | 73.2–73.5 |
| earnings | (a) | 54.0 | 61.6 | +7.6 | +4.2 | +2.3 | not used (k 2.95) | 61.9 | 64.2–66.1 |
| earnings | (b) | 57.5 | 65.7 | +8.2 | +4.5 | +2.5 | not used | 61.9 | 64.4–66.5 |

India's earnings step (G1 54.0 → G2 61.9, k = 2.95) comes from a G1 only 4 points above the median, so it is
unstable; it is reported in the CSV and left out of the range. Measure (b) is the cleaner like-for-like, because it uses one
instrument and one definition (parents of children). Measure (a) compares all adult G1, which is what the slopes
were fitted on.

### Fiscal translation [INFERENCE]

The Indian ledger's person-level fiscal net (CPS ASEC 2025, extended balance after health, equal_all_members) was
regressed on each adult's own percentile, using 160 SDR replicates (`derived/fiscal_gradient.csv`):

| percentile | sample | $ per point | se |
|---|---|---|---|
| wage earnings | all adults 25–64 (70,855) | 485 | 7 |
| wage earnings | India-born and India G2 (1,441) | 426 | 30 |
| education | all adults 25–64 | 299 | 6 |

Mapping: Δ fiscal net per future-G2 adult-year ≈ $485 × Δ earnings percentile, so +2.3 to +4.5 points is **+$1.1k to
+$2.2k**. On education, $299 × (+0.1 to +1.8) is +$0.04k to +$0.5k. The linear gradient understates the group gaps.
The India-born sit 10.7 earnings points above the median, and 10.7 × $485 = $5.2k against the ledger's +$10,732 gap.
For the India G2 it is 13.5 × $485 = $6.5k against +$20,572. Taxes are convex, and household structure adds more. Scaling the mapping by the
group ratio (≈2–3×) gives an upper arm of about +$2.3k to +$6.9k. Either way the sign is positive, and the change is
small next to the G2's existing +$20.6k gap. Standard errors of the projection are not propagated. The India G2 has n = 1,498
in the CPS (se of its mean percentile about 1.0–1.2) and 209 in the ledger.

## 4. Context (origin flow, primary sources)

Collected by a sub-agent into `context/context_notes.md`, which records URLs, sha256 hashes and quoted lines. Summary:

- **CBP encounters, citizenship India** (events, not persons) [DATA: `context/cbp_india_encounters_summary.csv`]:
  FY2020 19,883; FY2021 30,662; FY2022 63,927; FY2023 96,917; FY2024 90,415; FY2025 34,146. Southwest land border
  18.3k / 41.8k / 25.6k (FY2022–24). The northern border rose to 43.8k in FY2024. On the older DHS construct (USBP + ICE
  apprehensions) FY2018 was 9,953 and FY2019 8,926. [GAP] FY2019 on the nationwide-encounters basis.
- **Unauthorized India-born**: DHS OHSS revised series 120k (2000) → 540k (2018, old method) → 480k (2018, revised)
  → 220k (Jan 2022). Pew gives 680k (2023). MPI publishes no India figure (Asia total 851k). The producers differ about
  threefold. OHSS itself flags India as the case most sensitive to the nonimmigrant count.
- **USCIS H-1B characteristics** (India 36–76% of approvals; education and pay are for all beneficiaries, so this is
  an India-dominated proxy): the master's share rose from ~31–37% (FY2003–05) to 54–58% (FY2019–21, FY2025). The median
  approved compensation was $53k (FY2004) → $133k (FY2025), nominal.
- **DOL LCA wage levels** (certified H-1B LCAs, share of cases at levels I / II / III / IV;
  `context/lca_wage_levels.csv`) [CALCULATION]. The six India-heavy outsourcers are Infosys, TCS, Cognizant, Wipro,
  HCL and Tech Mahindra. FY2015: outsourcers 23.1 / 60.9 / 12.5 / 3.6, other employers 50.0 / 32.0 / 11.1 / 6.9.
  FY2019: 1.8 / 71.7 / 20.0 / 6.6 against 16.8 / 51.5 / 19.7 / 12.0. FY2024: 0.9 / 60.1 / 28.8 / 10.2 against
  20.4 / 43.6 / 20.3 / 15.7. Level I almost disappeared at the outsourcers, and their share of certified LCAs fell from
  14.3% to 6.9%. The level is set against the local wage for the occupation, so it is not a skill score. FY2019 uses
  the first worksite's level.
- **Origin test-taker pools** (self-selected applicants, **not immigrants**): GMAT means by citizenship, India
  576–582 against the US 531–537 (TY2010–14) and 577–583 against 547–563 (TY2016–20). The GRE for July 2024 to June 2025, by
  citizenship: India verbal 151.0, quant 158.6 (n 34,477); US 152.8 and 151.3 (n 80,508). Test-taking in India fell
  from 111k (2021–22) to 32k (2024–25). [GAP] No older GRE snapshot to compare with.

## 5. Disconfirmation and limits

1. **Coverage of the irregular inflow.** The ACS 2024 records 480k India-born noncitizens aged 18–64 who arrived
   2021–2024. About 63k of them lack a BA, and about 48k of those also lack every Borjas legal marker
   [DATA: `derived/acs_recent_arrivals.csv`]. CBP logged about 250k encounter events in FY2022–24. Either most were
   not released or did not stay, or the ACS misses them. Bound [INFERENCE]: suppose 200k missed adults sit near the white 30th
   percentile. Beside ~3.3M India-born adults 25–64 at about 75 (ledger weight 3.25M), that lowers the G1 mean by about 200/3,500 × 45 ≈ 2.6 points.
   That is a little less than the +3.4 education rise of measure (a). Through the slopes, it takes 0.9–1.3 points off the future G2's
   education. That is small, and only if those adults stay and have US-born children.
2. **The status proxy is weak for Indians.** The Borjas (2017) residual counts every noncitizen without a benefit,
   government job, licensed occupation or legal spouse as unauthorized. It labels 80% of 0–5-year arrivals, most of
   them H-1B, F-1 and H-4 holders. The table therefore reports only the residual among non-BA holders, which falls
   from 11.5% (2000–04) to 4.8% (2020–24). Rule (f), subsidised housing, is not in the ACS person file. HINS items
   begin in 2008.
3. **Selective return.** Temporary workers who leave are not observed. The fixed-duration views measure stayers.
   At 6–10 years this favours later cohorts, since more of them held temporary visas.
4. **Reference drift.** The white reference gained degrees (BA+ 21% → 44%). Percentiles hold the reference's own
   year, so "no decline" is relative to a rising US bar, not absolute.
5. **The G1→G2 step is a cross-origin average.** India's own step on education (1.10) is above the line. The
   projection range spans slope 0.36 to step 1.10.

## 6. Who is here now: the stock by arrival wave

### 6a. India-born residents, ACS 2024 (all ages, group quarters included)

[CALCULATION: `stock_language.py` → `derived/stock_by_cohort.csv`]

| arrival | n | weighted | share | median age | 0–17 | 18–34 | 35–54 | 55–64 | 65+ |
|---|---|---|---|---|---|---|---|---|---|
| all | 29,098 | 3.22M | 100% | 41 | 6.7% | 24.2% | 45.7% | 10.2% | 13.1% |
| pre-1980 | 1,980 | 180k | 5.6% | 74 | 0% | 0% | 10.7% | 13.0% | 76.3% |
| 1980–89 | 2,561 | 237k | 7.4% | 62 | 0% | 0% | 25.4% | 32.4% | 42.3% |
| 1990–99 | 4,549 | 445k | 13.8% | 53 | 0% | 8.9% | 47.8% | 28.5% | 14.7% |
| 2000–09 | 6,559 | 703k | 21.8% | 44 | 1.2% | 13.7% | 70.3% | 8.1% | 6.7% |
| 2010–14 | 3,729 | 443k | 13.8% | 37 | 9.8% | 22.8% | 60.6% | 2.8% | 4.0% |
| 2015–19 | 4,496 | 558k | 17.3% | 34 | 12.9% | 40.6% | 39.3% | 3.4% | 3.9% |
| 2020+ | 5,224 | 658k | 20.4% | 31 | 14.0% | 48.3% | 30.4% | 2.3% | 5.1% |

The pre-1990 waves the question calls the doctor/engineer generation are now 13% of the India-born, and they are
mostly past 60. Post-2010 arrivals are 51%.

### 6b. US-born with an India-born parent

[DATA: `derived/g2_stock.csv`]

- **CPS ASEC 2024–25, either parent born in India:** 1.62M (n 1,276). Of these, 61% are under 18, 14% are 18–24,
  11% are 25–34 and 13% are 35+. When both parents were born in India the figure is 1.35M. So the adult G2 is about
  0.63M, and only about 0.22M are 35 or older. The CPS records the parents' birthplace but not their arrival year.
- **ACS 2024, co-resident only** (US-born children of the householder with an India-born householder or spouse,
  any age; 1.02M), by the parent's arrival: pre-1980 46k, 1980s 110k, 1990s 219k, 2000–09 366k, 2010–14 155k,
  2015–19 81k, 2020+ 47k. Among co-resident children 0–17, 2000–09 parents are the largest group (§2). Children who
  have left home cannot be linked in the ACS, so the older G2 is under-counted here. The CPS total is the stock.

The G2 is still mostly children, and these children descend from the 2000s H-1B wave or later.

## 7. India-born by language spoken at home

ACS 2021–2024 pooled; the stock is the four-year mean of the weights. Outcomes are for adults 25–64, age-standardised to the
pooled India-born age mix. **Language is a proxy for home region in India. It does not measure caste or religion.**
English-only households are mostly long-resident or mixed households, and the English-only share falls with arrival
cohort partly because of duration. Trucking is SOC 53-30xx.
[CALCULATION: `derived/language_profile.csv`, `language_by_cohort.csv`, `language_children.csv`]

| language | n 25–64 | stock (all ages) | edu pct | earn pct | BA+ | graduate | computing | physicians | retail | accom./food | trucking | self-emp. | arrived 2010+ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 81,079 | 2.95M | 73.6 | 62.0 | 84% | 52% | 30% | 2.7% | 8.7% | 2.4% | 1.8% | 7.4% | 48% |
| Hindi | 20,371 | 719k | 77.6 | 64.7 | 90% | 59% | 29% | 3.2% | 9.2% | 2.2% | 1.2% | 6.9% | 54% |
| Telugu | 11,797 | 418k | 80.3 | 66.5 | 94% | 63% | 50% | 3.0% | 5.7% | 1.0% | 0.1% | 5.6% | 56% |
| Gujarati | 8,659 | 322k | 66.1 | 55.6 | 74% | 39% | 17% | 2.0% | 16.5% | 5.4% | 0.7% | 10.6% | 37% |
| Tamil | 7,988 | 268k | 80.1 | 65.4 | 95% | 60% | 40% | 2.0% | 5.4% | 0.8% | 0.2% | 4.3% | 54% |
| Punjabi | 5,507 | 223k | **47.4** | **47.3** | 47% | 21% | 7% | 2.4% | 13.7% | 4.7% | **17.4%** | **20.8%** | 38% |
| Malayalam | 4,557 | 158k | 72.6 | 60.8 | 83% | 44% | 24% | 2.1% | 6.7% | 1.3% | 0.6% | 4.1% | 42% |
| Marathi | 3,215 | 106k | 81.5 | 67.4 | 95% | 64% | 37% | 2.4% | 4.5% | 1.3% | 0.5% | 4.5% | 54% |
| Kannada | 2,306 | 72k | 81.1 | 66.9 | 96% | 61% | 37% | 3.8% | 5.1% | 1.0% | 0% | 4.0% | 55% |
| Bengali | 2,064 | 66k | 80.4 | 63.7 | 92% | 63% | 28% | 1.1% | 5.4% | 1.3% | 0.8% | 2.9% | 52% |
| Urdu | 1,473 | 63k | 69.6 | 50.6 | 80% | 43% | 24% | 3.5% | 6.9% | 2.5% | 1.3% | 10.1% | 42% |
| English only | 9,219 | 361k | 74.4 | 64.0 | 84% | 54% | 21% | 4.8% | 7.3% | 2.6% | 0.9% | 7.3% | 35% |
| other | 3,923 | 149k | 62.3 | 54.1 | 68% | 36% | 19% | 1.5% | 10.0% | 4.5% | 1.8% | 8.0% | 44% |

Malayalam speakers have the highest health-practitioner share (18% of employed, mostly nurses; SOC 29-1) [DATA].

**Which languages each wave brought** (India-born adults 18+, column shares by arrival cohort):

| arrival | Hindi | Telugu | Tamil | Gujarati | Punjabi | Malayalam | Marathi | Kannada | Bengali | Urdu | English only | other |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pre-1980 | 20.1% | 4.5% | 4.1% | 17.4% | 7.7% | 6.0% | 2.3% | 1.7% | 2.6% | 4.4% | 22.2% | 6.9% |
| 1980–89 | 20.3% | 4.9% | 5.6% | 18.8% | 10.7% | 7.2% | 1.8% | 1.6% | 2.2% | 2.9% | 17.3% | 6.8% |
| 1990–99 | 21.0% | 10.9% | 8.2% | 13.6% | 10.8% | 6.0% | 3.0% | 2.3% | 2.2% | 2.7% | 13.9% | 5.5% |
| 2000–09 | 23.8% | 15.6% | 9.3% | 11.7% | 7.8% | 6.1% | 3.7% | 2.2% | 2.1% | 2.1% | 11.0% | 4.6% |
| 2010–14 | 25.2% | 17.1% | 11.6% | 9.2% | 6.8% | 5.5% | 4.4% | 2.6% | 2.5% | 1.6% | 8.6% | 4.8% |
| 2015–19 | 29.3% | 16.5% | 9.9% | 8.7% | 7.1% | 4.4% | 4.1% | 2.7% | 2.5% | 1.6% | 8.8% | 4.5% |
| 2020+ | 31.9% | 20.7% | 9.6% | 6.4% | 4.6% | 3.7% | 4.4% | 3.4% | 2.2% | 1.6% | 7.3% | 4.0% |

The regional shift runs toward the high-selection groups. Telugu rose from 4–5% of the pre-1990 waves to 21% of 2020+
arrivals, and Hindi from 20% to 32%. Gujarati fell from 17–19% to 6%, and Punjabi from 11% to 5%. Those are the two
groups with the lowest education and the highest retail, trucking and self-employment shares. Part of the rise
in measured selection since 1995 is this regional mix shift [INFERENCE]. The caveat from §5.1 applies with
extra force here: if the post-2021 irregular inflow comes disproportionately from particular regions, the ACS
would under-show them. The survey cannot test that.

Parents' language for US-born children 0–17 with an India-born householder or spouse (2021–24 mean 803k): Hindi 23%, Telugu 17%, English
only 13%, Tamil 10%, Gujarati 8%, Punjabi 7%, Malayalam 6%, other 16%.

## 8. Last-ten-years data: flow sources for 2015–2025 Indian arrivals

The sub-agent fetched each source from the primary publisher, archived it and tabulated it: `context/flows_2015_2025.csv`, with the file, the
quoted row and the sha256 for each value; the details are in `context/context_notes.md` items 1–6. [DATA]

| source | what it counts | what it says, 2015→latest |
|---|---|---|
| DHS Yearbook Table 10 (+ OHSS special tabulation for EB principals and derivatives) | India-born persons obtaining LPR status, by class | total 64.1k (FY2015) → 127.0k (FY2022 peak) → 66.8k (FY2024). Employment-based 27.5k → 96.3k (FY2022) → 18.8k. EB principals are 40–45% of EB grants. Immediate relatives 20.6k → 34.1k (FY2024). Family preference 14.6k → 9.7k. The FY2021–22 EB spike is mostly status adjustment of people already here [INFERENCE] |
| USCIS H-1B characteristics reports | approved petitions, India-born beneficiaries (initial and continuing) | 195k (FY2015) → 284k (FY2025). Initial approvals 51k–80k a year, with no trend. India is 70–76% of all approvals. The master's share of all approvals is 54–58% in recent clean years |
| ICE SEVP "SEVIS by the Numbers" (calendar years 2017–2024) | active F-1/M-1 student records, citizens of India; STEM OPT records | active 247k (2017) → 207k (2020) → 422k (2024). STEM OPT 49k → 78k (2019) → 48k (2023) → ~79k (2024, derived). [GAP] 2015–16 by country; [GAP] post-completion OPT by country |
| DHS Yearbook FY2024 nonimmigrant tables | I-94 admissions (entries, not persons) of Indian citizens | all classes 1.90M (FY2015) → 0.54M (FY2021) → 2.94M (FY2024). FY2024 by class: H-1B 497k, H-4 215k, F-1 299k, L-1 65k, B-2 1.47M. [GAP] class by country for FY2015–23 |
| CBP nationwide encounters | encounter events, citizenship India | 19.9k (FY2020) → 96.9k (FY2023) → 90.4k (FY2024) → 34.1k (FY2025). Southwest border 1.1k → 41.8k (FY2023); the northern border peaked at 43.8k (FY2024). FY2018–19 are available only as Border Patrol + ICE apprehensions (10.0k, 8.9k). [GAP] FY2019 on the encounters basis |
| DHS OHSS / Pew / MPI unauthorized estimates | India-born unauthorized residents (residual method) | DHS 470k (2015) → 540k (2018) → revised 480k (2018) → 220k (2022). Pew 680k (2023). MPI gives only the Asia total (851k). The estimates disagree about threefold, and the disagreement turns on the count of legal temporary residents |

These flows count different things: grants, petitions, records, entries, events and residual stocks. None of them measures
new residents net of departures. The ACS arrival-year counts in §5.1 and §6a are the only resident-based series.
Taken together: the legal high-skill channels (H-1B, F-1, STEM OPT) grew or held in 2015–2024. Family-sponsored
green cards shifted toward immediate relatives (parents of citizens), which fits the older late-life arrivals
in the 2015+ stock views. The irregular channel spiked in FY2022–24 and fell sharply in FY2025.

## Files

| file | holds |
|---|---|
| `acs_extract.py` | slims ACS 2005–2024 person PUMS to India-linked households → `_cache/acs_india_<year>.parquet` |
| `common.py` | percentile machinery imported from the selection-curve lane; ACS/census → CPS code crosswalks |
| `cps_cohorts.py` | gate; CPS cohort views → `derived/cps_cohorts.csv`, `derived/gate.json` |
| `census_ysm.py` | 1980–2023 fixed-duration series → `derived/census_ysm.csv` |
| `acs_cohorts.py` | ACS cohort views, calibration, children's parents, recent arrivals → `derived/acs_*.csv` |
| `project_g2.py` | projection and fiscal gradient → `derived/projection.csv`, `derived/fiscal_gradient.csv` |
| `stock_language.py` | India-born stock by wave, G2 stock (CPS and ACS), language profiles → `derived/stock_by_cohort.csv`, `g2_stock.csv`, `language_*.csv` |
| `verify.py` | from-scratch rerun and byte comparison → `derived/verify.json` |
| `context/` | sub-agent's primary-source context (CBP, DHS/Pew/MPI, USCIS H-1B, LCA, test pools) |

Run order (repo root): `OPENBLAS_NUM_THREADS=1 uv run --no-project --with duckdb --with pyarrow python3
infra/immigration-fiscal/indian_cohort_selection_2026_09_29/<script>.py` for acs_extract, cps_cohorts, census_ysm,
acs_cohorts, project_g2; or `verify.py` for all of them.
