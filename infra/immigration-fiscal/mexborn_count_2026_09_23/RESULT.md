**Verdict:** About 11.1M is the right Mexico-born level for February–April 2025, not 12.2M. The CPS
has run 9–13% above the ACS on the Mexico-born since 2019, in the ASEC and in all 31 monthly files
from January 2024. This is a standing CPS composition bias, not a quirk of the ASEC sample or of the
2025 controls. In 2024 the CPS carried 1.38M more Mexico-born and 1.81M fewer other Hispanics than the
ACS, under a lower Hispanic total. At the central level (ACS 2024 in the CPS universe, 11.07M), the
main case overstates the first generation's share by 9.5%: **−$6.4bn to −$7.9bn** on $203.2–249.6bn
(about −$7.2bn at the midpoint). The low and high cases give **−$5.4bn and −$10.3bn**. The
unauthorized lane's 4.567M Mexico-born falls to about **4.07M (range 3.96–4.16M)**, a cut of
0.4–0.6M. The 2025→2026 CPS drop is mostly nonresponse among newly contacted households, not
outflow, so ASEC 2026's 11.1M is not an independent confirmation.

# Mexico-born count adjudication (audit row 4)

Lane `mexborn_count_2026_09_23`, 2026-09-23. It answers `BRIEF.md`, adjudicating
`dataset_integrity_2026_09_23/cps.md` §3 (defect-table row 3, the brief's "row 4").

## Answers to the brief

1. **Does the count jump in the ASEC months, or is the ASEC sample alone high?** Neither. The March
   2025 basic records alone, on the basic CPS weight, give 12.045M. The ASEC oversample adds no
   excess (`derived/asec_sample_split.csv`). The monthly files read 11.91–12.05M in February–April
   2025 and averaged 12.38M across 2024. IPUMS ASEC 2024 read 12.38M. The audit left the ASEC 2024
   cross-check open because it had no file; this settles it. [CALCULATION: `gate_asec.py`,
   `monthly_series.py`, `annual_series.py`]
2. **Did the Vintage 2024 controls create it?** No. Every month of 2024, still on Vintage 2023
   controls, read 12.09–12.70M. When the new controls arrived in January 2025, Hispanics 16+ rose by
   1.277M [SOURCE: BLS, *Adjustments to Household Survey Population Estimates in January 2025*, table,
   parsed by `benchmarks.py`], but the Mexico-born moved by −0.17M, within monthly noise.
   [CALCULATION: `control_jump.py`]
3. **Which level is right?** The ACS level: 11.07M (range 10.72–11.26M). The reasons are in "Why
   the ACS level" below.
4. **Is the 2025→2026 drop (−1.12M) real outflow?** Mostly not. See the rotation-group evidence
   below. Real outflow was probably about 0.3M [INFERENCE].

## Gate

`gate_asec.py` → `derived/asec_gate.csv`. The audit's counts reproduce exactly: ASEC 2025 is
12.231214M and ASEC 2026 is 11.108947M (PENATVTY 303, PRCITSHP 4/5, MARSUPWT/100). The IPUMS extracts
used for the long series reproduce ASEC 2025 at 12.231214M. They reproduce ACS 2024 at 11.005332M
(households) and 11.153915M (all). [CALCULATION]

## Monthly series, CPS basic files January 2024 – August 2026

`monthly_series.py` → `derived/monthly_series.csv`, and `rotation_design.py` →
`derived/rotation_by_month.csv`. Figures are in millions, weighted by PWSSWGT. October 2025 was never
collected. MIS 1–4 and MIS 5–8 are ratio estimates from each half of the rotation groups, scaled to
the full population. From April 2025, MIS 1–4 are households first contacted in 2025.

| Month | Total | CA+TX | Other states | Naturalized | Noncitizen | n | MIS 1–4 | MIS 5–8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2024-01 | 12.32 | 6.39 | 5.93 | 4.40 | 7.93 | 3,036 | 12.25 | 12.40 |
| 2024-02 | 12.36 | 6.58 | 5.78 | 4.20 | 8.16 | 3,094 | 11.98 | 12.75 |
| 2024-03 | 12.70 | 6.82 | 5.89 | 4.26 | 8.45 | 3,074 | 12.58 | 12.83 |
| 2024-04 | 12.14 | 6.76 | 5.38 | 4.05 | 8.08 | 3,092 | 11.80 | 12.48 |
| 2024-05 | 12.22 | 6.83 | 5.39 | 4.21 | 8.01 | 3,210 | 12.00 | 12.44 |
| 2024-06 | 12.09 | 6.84 | 5.25 | 4.09 | 8.00 | 3,121 | 11.80 | 12.38 |
| 2024-07 | 12.29 | 6.97 | 5.32 | 4.14 | 8.15 | 3,134 | 12.17 | 12.42 |
| 2024-08 | 12.51 | 6.86 | 5.65 | 4.21 | 8.30 | 3,204 | 12.18 | 12.84 |
| 2024-09 | 12.53 | 6.61 | 5.92 | 4.09 | 8.44 | 3,148 | 11.70 | 13.36 |
| 2024-10 | 12.50 | 6.47 | 6.03 | 4.13 | 8.37 | 3,099 | 12.08 | 12.91 |
| 2024-11 | 12.26 | 6.09 | 6.17 | 4.00 | 8.26 | 3,010 | 12.01 | 12.51 |
| 2024-12 | 12.70 | 6.43 | 6.26 | 4.13 | 8.57 | 3,142 | 12.74 | 12.65 |
| 2025-01 | 12.52 | 6.45 | 6.08 | 4.29 | 8.24 | 2,971 | 12.40 | 12.65 |
| 2025-02 | 12.05 | 6.35 | 5.70 | 4.29 | 7.76 | 2,869 | 11.61 | 12.50 |
| 2025-03 | 12.03 | 6.47 | 5.56 | 4.20 | 7.83 | 2,724 | 11.22 | 12.83 |
| 2025-04 | 11.91 | 6.19 | 5.72 | 4.33 | 7.58 | 2,737 | 11.51 | 12.32 |
| 2025-05 | 12.09 | 6.50 | 5.59 | 4.43 | 7.66 | 2,765 | 11.29 | 12.88 |
| 2025-06 | 11.98 | 6.43 | 5.54 | 4.23 | 7.74 | 2,687 | 11.03 | 12.88 |
| 2025-07 | 12.01 | 6.47 | 5.53 | 4.57 | 7.44 | 2,628 | 10.93 | 13.06 |
| 2025-08 | 11.60 | 6.33 | 5.27 | 4.56 | 7.03 | 2,699 | 10.54 | 12.64 |
| 2025-09 | 11.38 | 6.13 | 5.25 | 4.59 | 6.79 | 2,629 | 10.47 | 12.29 |
| 2025-11 | 11.42 | 5.98 | 5.43 | 4.54 | 6.88 | 2,533 | 10.94 | 11.89 |
| 2025-12 | 11.68 | 6.23 | 5.45 | 4.46 | 7.22 | 2,635 | 11.08 | 12.26 |
| 2026-01 | 11.54 | 6.06 | 5.48 | 4.38 | 7.16 | 2,571 | 10.95 | 12.13 |
| 2026-02 | 10.77 | 5.85 | 4.92 | 4.23 | 6.54 | 2,513 | 10.37 | 11.17 |
| 2026-03 | 10.95 | 5.86 | 5.09 | 4.22 | 6.73 | 2,443 | 11.01 | 10.88 |
| 2026-04 | 11.27 | 5.99 | 5.28 | 4.60 | 6.67 | 2,651 | 11.06 | 11.48 |
| 2026-05 | 11.11 | 5.98 | 5.13 | 4.40 | 6.71 | 2,668 | 11.29 | 10.92 |
| 2026-06 | 11.22 | 5.97 | 5.25 | 4.51 | 6.71 | 2,595 | 11.29 | 11.14 |
| 2026-07 | 10.92 | 5.87 | 5.06 | 4.53 | 6.39 | 2,505 | 10.97 | 10.88 |
| 2026-08 | 11.00 | 5.74 | 5.26 | 4.48 | 6.52 | 2,515 | 11.07 | 10.92 |

Averages: 2024 is 12.38M (CA+TX 6.64, other 5.75, noncitizen 8.23). February–April 2025 is 12.00M.
July–August 2026 is 10.96M (CA+TX 5.80, other 5.16). Against the ACS 2024 in households, the 2024
CPS average is 5% higher in CA+TX and 22% higher elsewhere. ASEC 2025's match in CA+TX (6.30 against
6.31) was not typical of the monthly files. [CALCULATION]

### Rotation groups: the 2025 fall is a first-contact effect

BLS phased in a new 2020-based sample from April 2025 to July 2026, one rotation group a month [SOURCE:
https://www.bls.gov/cps/methods/sample_redesign_2025.htm]. Households first contacted before 2025 (MIS
5–8 through January 2026) kept reading 11.9–13.1M through 2025. Households first contacted in 2025
(MIS 1–4 from about March 2025) read 10.5–11.5M. The gap in noncitizen Mexico-born averaged about
−0.3M in 2024. It reached −1.5M in March 2025, before any new-design household entered, and
−2.1 to −2.7M from July 2025 to January 2026. It closed to −0.3M in March 2026, a month before
MIS 5–8 began turning over to the new design. So it tracks when a household was first reached, not
which design selected it. From April 2026 both halves read 10.9–11.5M.

The redesign itself does not remove the excess outside CA+TX: the difference-in-differences there is
−0.14M (naive z −1.2; `derived/rotation_did.csv`). MIS 5–8 fell only about 0.3M between the 2024 average
(12.66M) and July 2025–January 2026 (12.38M). That puts real 2025 outflow at roughly 0.3M. The rest
of the 1.1–1.4M CPS fall is response. [CALCULATION: `rotation_design.py`] [INFERENCE: continuing
households may also have stopped responding, which would make 0.3M an upper bound; single months
carry about ±0.4M of noise]

Total net international migration stayed positive: 1.3M for July 2024–June 2025, projected at about
321,000 for 2025–26 [SOURCE: Census Bureau press release, 27 January 2026,
https://census.gov/newsroom/press-releases/2026/population-growth-slows.html]. The January 2026
controls did not cut the Hispanic population: Hispanics 16+ rose 403,000 while the civilian
noninstitutional 16+ total fell 231,000 [SOURCE: BLS, *Adjustments … January 2026*, table, parsed by
`benchmarks.py`]. ASEC 2026's 11.11M therefore reflects post-2025 response, not a clean new level.

## Annual series: CPS ASEC against ACS, 2005–2025

`annual_series.py` → `derived/annual_series.csv`. CPS ASEC comes from IPUMS-CPS extract 1 (ASECWT;
the 2014 5/8 file). The ACS comes from IPUMS USA extract 3 (PERWT, households plus noninstitutional
group quarters). "ACS at ASEC" interpolates ACS t−1 and t to 15 March of t.

| Year | CPS ASEC | ACS, same year | ACS at ASEC | CPS ÷ ACS at ASEC |
|---|---:|---:|---:|---:|
| 2006 | 10.90 | 11.42 | 11.30 | 0.96 |
| 2007 | 11.57 | 11.62 | 11.57 | 1.00 |
| 2008 | 11.62 | 11.33 | 11.42 | 1.02 |
| 2009 | 11.62 | 11.35 | 11.35 | 1.02 |
| 2010 | 11.71 | 11.62 | 11.54 | 1.01 |
| 2011 | 11.58 | 11.55 | 11.57 | 1.00 |
| 2012 | 11.62 | 11.36 | 11.42 | 1.02 |
| 2013 | 11.51 | 11.44 | 11.41 | 1.01 |
| 2014 | 11.18 | 11.59 | 11.55 | 0.97 |
| 2015 | 11.91 | 11.47 | 11.51 | 1.03 |
| 2016 | 11.71 | 11.46 | 11.46 | 1.02 |
| 2017 | 11.83 | 11.14 | 11.23 | 1.05 |
| 2018 | 11.95 | 11.08 | 11.10 | 1.08 |
| 2019 | 12.06 | 10.78 | 10.87 | 1.11 |
| 2020 | 11.25 | 10.14 | 10.32 | 1.09 (ACS 2020 experimental) |
| 2021 | 11.70 | 10.63 | 10.49 | 1.12 |
| 2022 | 11.97 | 10.56 | 10.58 | 1.13 |
| 2023 | 11.71 | 10.80 | 10.73 | 1.09 |
| 2024 | 12.38 | 11.07 | 10.99 | 1.13 |
| 2025 | 12.23 | — | — | 1.105 against ACS 2024 |

The two surveys agreed within ±4% from 2006 to 2016. The gap opened in 2017–2019 and has held at
9–13% since. Against the prior-year ACS it is larger among noncitizens (1.12–1.20 since 2021) than
among the naturalized (1.02–1.11). [CALCULATION]

## Why the ACS level

1. **The two surveys hold the Hispanic total at the same level but split it differently.** Both are
   weighted to Census population estimates by age, sex, race and Hispanic origin, not by nativity or
   origin [SOURCE: Gross 2024, Census Bureau Population Division Working Paper 107,
   https://www2.census.gov/library/working-papers/2024/demo/pop-wp107.pdf]. The CPS controls Hispanic
   origin only nationally. Its state controls are broad race (Black / other), three age groups and
   sex [SOURCE: `indian_ledger_2026_09_18/_cache/cpsmar25.txt`, "Estimation Procedure", pp. 4–5]. The
   ACS controls by county. In the same year (2024), the CPS carried fewer Hispanics than the ACS
   (65.74M against 66.76M) but 1.38M more Mexico-born and 1.81M fewer other Hispanics. Outside CA+TX
   it carried fewer Hispanics too (37.88M against 38.56M). So the excess is composition inside the
   Hispanic control, not extra people found: the Mexico-born are 15.2% of Hispanics there against
   12.2% in the ACS. [CALCULATION: `hispanic_geography.py`] The deficit extends to groups with no
   enforcement exposure. Puerto Ricans are 0.94 of the ACS and South Americans 0.92 in ASEC 2025
   [DATA: `dataset_integrity_2026_09_23/derived/cps_vs_acs_origin.csv`].
2. **The divergence tracks falling CPS response.** ASEC basic interviews fell from 52,900 (2015) to
   40,000 (2025), and noninterviews rose from 8,200 to 20,000. The Hispanic coverage ratio before
   raking was 0.81–0.83 in March 2025 [SOURCE: cpsmar25, Tables 1 and 3, pp. 4 and 8]. The raking puts
   the missing Hispanic mass on the Hispanics who respond, and no origin control limits who absorbs
   it.
3. **Sample and response rate.** The ACS samples about 3.5M households a year and the CPS about
   60,000 housing units a month. The Census Bureau "routinely cautions against using the CPS to
   estimate the size and the geographic distribution of the foreign-born population when other data
   are available" [SOURCE: Gross 2024, question 4]. In 2022 the ACS response rate was about 85% and
   the CPS about 75% [SOURCE: Guo and Krolikowski 2024, Cleveland Fed Economic Commentary 2024-05,
   https://doi.org/10.26509/frbc-ec-202405]. CPS foreign-born weights rose after February 2020 in
   ways worker and survey characteristics do not explain [SOURCE: Butcher, Cain and García-Jimeno
   2023, Chicago Fed Letter 486, https://doi.org/10.21033/cfl-2023-486].
4. **Sampling error does not cover it.** ASEC 2025's replicate SE is 0.248M, and the gap is 1.16M
   against the like-for-like ACS figure [DATA: `dataset_integrity_2026_09_23/derived/cps_detail_checks.json`].
   The gap persists in every monthly file of 2024 and in every ASEC since 2019.

## Pricing

`price_row4.py` → `derived/pricing.csv`. The formula is the audit's: effect = −(12.231 − level) ÷
12.231 × G1 share × main case. The G1 share of the union net at ledger waterfall step 14 is −72.458 ÷
−217.316 = 0.3334 [DATA: `ledger_absolute_2026_09_17/derived/waterfall.csv`]. The main case is
$203.207–249.640bn [DATA: `main_case_2026_09_23/derived/main_case_bands.csv`, adopted row].

| Level for February–April 2025 | M | Excess share | Effect at $203.2bn | Effect at $249.6bn |
|---|---:|---:|---:|---:|
| Low effect: ACS 2024 trended to 15 March 2025 at its 2023–24 pace | 11.257 | 7.96% | −5.40 | −6.63 |
| **Central: ACS 2024, households + noninstitutional GQ** | **11.069** | **9.50%** | **−6.44** | **−7.91** |
| Check: ACS 2024 × MIS 5–8 change, 2024 → Feb–Apr 2025 | 10.966 | 10.35% | −7.01 | −8.61 |
| High effect: ACS 2024 × whole-sample CPS change, 2024 → Feb–Apr 2025 | 10.723 | 12.33% | −8.35 | −10.26 |
| Reference: ACS 2024 households only (audit) | 11.005 | 10.02% | −6.79 | −8.34 |
| Reference: ACS 2024 including institutional GQ (audit) | 11.154 | 8.81% | −5.97 | −7.33 |
| Reference: CPS ASEC 2026 | 11.109 | 9.18% | −6.22 | −7.64 |

The central level uses the right universe. The CPS covers the civilian noninstitutional population,
so the comparable ACS figure is households plus noninstitutional group quarters. The audit's two
figures bracket it. The high case includes some of the early-2025 first-contact fall, which
overstates the decline. The per-person figure does not change, and G1's step-14 net moves from
−72.46 to −65.57bn. [CALCULATION]

The excess is 76% noncitizen (0.88M of 1.16M). If noncitizen G1 members cost more per person than
the G1 average, the formula understates the effect. The ledger has no per-person figure by
citizenship, so this is untested. [INFERENCE]

## Unauthorized count

`derived/unauthorized_implication.csv`. The lane's 4.567M is a Borjas residual on ASEC 2025.

| Route | Mexico-born unauthorized, M | Change |
|---|---:|---:|
| Lane figure (CPS ASEC 2025) | 4.567 | — |
| Same rules on ACS 2024, the lane's own run | 3.964 | −0.603 (−13.2%) |
| Same, with OHSS coverage (lane's own run) | 4.162 | −0.405 (−8.9%) |
| **CPS residual × ACS/CPS noncitizen ratio** | **4.074** | **−0.493 (−10.8%)** |
| CPS residual × central level ÷ CPS count | 4.133 | −0.434 (−9.5%) |

The ACS run lacks the subsidised-housing rule, which leans its figure upward (unauthorized memo §3),
so 3.96M is not a floor. [CALCULATION: `price_row4.py`]

## Benchmarks, graded by evidence level

| Benchmark | Figure | Evidence level | Bearing |
|---|---|---|---|
| ACS 2024 1-year, IPUMS USA extract 3 | 11.154M all; 11.069M households + noninst. GQ; 11.005M households | Empirical, official survey (~3.5M households a year) | The level chosen |
| CPS ASEC 2025 / 2024 / 2026 | 12.231M (SE 0.248) / 12.375M / 11.109M | Empirical, survey (~95,000 households) | The excess is standing, not a single-year fluke |
| CPS basic monthly | 2024 mean 12.38M; Feb–Apr 2025 12.00M; Jul–Aug 2026 10.96M | Empirical, survey | Same instrument, same bias; the 2025 fall is response |
| ACS 2025 1-year | not released: HTTP 404 on 2026-09-23; release date "being determined" under a Commerce disclosure-avoidance order [SOURCE: census.gov ACS updates 2026, 6 August 2026] | — | Would be the decisive check |
| OHSS LPR population, Table 2a | Mexico-born LPRs 2.92M (1 Jan 2024, revised), 2.95M (1 Jan 2025) [SOURCE: https://ohss.dhs.gov/topics/immigration/lawful-permanent-residents/population-estimates/fy-25-lpr-pop-estimates] | Administrative (USCIS records from 1980; ACS for earlier entrants) | Noncitizens minus LPRs: ACS 4.33M, CPS 5.18M (`derived/lpr_anchor.csv`). Both fit inside the published range below, so it does not discriminate |
| Mexican unauthorized, published | DHS OHSS Jan 2022: 44% of 10.99M; Pew 2023: 4.3M; MPI mid-2023: 5.5M; CMS 2024: 5.1M (4.445M in 2020) [SOURCE: unauthorized lane `derived/published_estimates.csv`; CMS Table 5 and MPI fact sheet parsed by `benchmarks.py`] | Modelled: ACS-based residuals with coverage adjustments | A 1.2M spread across methods. CMS adds 5% for pre-2021 arrivals and DHS 13% at arrival decaying 7.5% a year, so the modelled truth is the ACS plus ~0.2–0.3M, not the CPS [INFERENCE; the lane's OHSS-coverage run adds 0.198M for Mexico] |
| Pew, key facts (Kramer and Passel, 21 August 2025) | "more than 11 million U.S. residents were born in Mexico" (2023 ACS). CPS immigrants 53.3M (January 2025) → 51.9M (June 2025), a decline that "may in part be due to technical reasons such as declining CPS survey participation among immigrants" [SOURCE: https://www.pewresearch.org/short-reads/2025/08/21/key-findings-about-us-immigrants/] | Expert, survey-based | Consistent with the ACS level and with the response finding |
| Census Vintage 2024 / 2025 NIM | 2,785,517 (July 2023–June 2024), with ACS immigration raised to cover 75% of humanitarian arrivals, and "Recent immigrants may not be fully represented in the ACS" [SOURCE: Census Random Samplings, 19 December 2024]. 1.3M (July 2024–June 2025); about 321,000 projected for 2025–26 [SOURCE: Census press release, 27 January 2026] | Modelled, official | No year of Mexico-specific outflow near 1.1M; the uplift targets mostly non-Mexican arrivals |
| BLS control changes | January 2025: civilian noninstitutional 16+ +2.871M, Hispanic +1.277M. January 2026: −0.231M, Hispanic +0.403M [SOURCE: BLS adjustment notes, parsed by `benchmarks.py`] | Official | Neither change explains the Mexico-born level or its fall |
| Census guidance (Gross 2024, WP-107) | Surveys "controlled … by age, sex, race and Hispanic origin, but not by nativity". The Bureau "routinely cautions against using the CPS" for foreign-born size | Expert guidance | Favours the ACS |
| Administrative-records census (CES-WP-23-42, 2023) | Foreign-born 52.5–54.9M against the ACS's 45.1M for 2020; noncitizens at least 11.0M higher, the widest gaps among Hispanics 25–64 [SOURCE: https://www2.census.gov/library/working-papers/2023/adrm/ces/CES-WP-23-42.pdf, excerpt only] | Contested: administrative records keep emigrants | Both surveys may be low. See disconfirmation |

INEGI, CONAPO and consular counts were not searched within the source budget. To my knowledge
[TRAINING-DATA], Mexican official figures on Mexicans in the US tabulate the US CPS or ACS, so they
would not be independent.

## Disconfirmation: what would make the CPS level right

The CPS level is right only if the ACS under-represents the Mexico-born relative to other Hispanics
in the same county, age and sex cells. The ACS's county controls would then push their weight onto
US-born and other-origin Hispanics.

- **For it:** the ACS's Mexico-born fell 0.9M from 2015 to 2022 while the CPS stayed flat. That fall
  coincides with the 2017–2020 enforcement climate and the census citizenship-question fight, which
  may have deterred mail-first ACS response more than the interviewer-led CPS [INFERENCE].
  CES-WP-23-42's administrative-records count shows large noncitizen shortfalls in the ACS, widest
  among Hispanics aged 25–64. The Census Bureau says recent immigrants are under-represented in the
  ACS.
- **Against it:** the ACS shortfall the Bureau documents concerns recent humanitarian arrivals, who
  are mostly not Mexican. Under the county Hispanic controls, missing them raises the ACS Mexico-born
  share rather than lowering it. The CPS shortfall falls on Puerto Ricans and South Americans, groups
  a Mexican-specific deterrent does not touch. In 2024 the CPS also carried fewer Hispanics outside
  CA+TX than the ACS, so it is not reaching people the ACS misses. The administrative-records gap
  concerns the level of the population controls both surveys share, so it cannot favour one survey's
  split. It belongs to the population lane's coverage arm (0 to +7.6%).
- **Tests that would flip this verdict:** (a) ACS 2025 1-year showing about 12M; (b) an
  administrative-records count by country of birth putting the Mexico-born near 12M while other
  Hispanic origins match the ACS; (c) evidence from linked ACS–IRS/SSA records that the ACS
  Mexico-born share within county Hispanic cells is biased low.

The residual estimators' coverage adjustments point to a modelled truth of about 11.3–11.4M, the ACS
plus 0.2–0.3M. That is close to the low-effect case, not to 12.2M. [INFERENCE]

## Limits

- Arrival year is 20–24% allocated in the CPS, and the cohort pattern existed in 2012–2015, when the
  totals agreed. So `cohort_compare.py` is weak evidence. ASEC 2025 minus ACS 2024: before 1990
  −0.04M, 1990s −0.06M, 2000s +0.44M, 2010s +0.29M, 2020 or later +0.53M. By age: 25–64 +0.89M,
  0–24 +0.16M, 65+ +0.11M.
- The rotation difference-in-differences uses a naive SE. Consecutive months share 75% of the sample,
  so its z-scores are overstated.
- The low and high levels move the ACS by trend: +0.19M, or −3.1% on the CPS's own change. Neither
  trend is measured for the Mexico-born in early 2025.
- Per-person effects by citizenship are untested (see Pricing).

## Files

Covered:
- ASEC 2025 and 2026 public-use zips.
- 31 CPS basic monthly files, January 2024 – August 2026, fetched by `fetch_basic.sh` into
  `_cache/basic/` (about 10 MB each; 28 GiB free at fetch).
- IPUMS-CPS extract 1 (`sources/immigration-fiscal/data/external/cps/cps_2ndgen.csv.gz`) and IPUMS USA
  extract 3 (`sources/immigration-fiscal/derived/ipums_usa/usa_00003_…_mexborn.parquet`).
- ACS 2024 PUMS subset (`mexican_origin_population_total_2026_09_19/_cache/acs2024_ancestry_subset.parquet`).
- cpsmar25 text.
- `main_case_bands.csv` and `waterfall.csv`.
- The unauthorized lane's derived outputs and its cached CMS and MPI texts.
- Primary documents in `_cache/sources/`: the OHSS LPR page and the BLS 2025 and 2026 adjustment
  PDFs, with their text.
- Web reads: the BLS redesign page, the Census Vintage 2024 blog and 2025 press release, WP-107
  (excerpt), Pew, the Chicago and Cleveland Fed pieces (excerpts), CES-WP-23-42 (excerpt), and the ACS
  2026 updates page.

Skipped:
- ACS 2025: not released.
- INEGI, CONAPO and consular counts: outside the source budget and likely not independent.
- Fox and Stern (2025): the monthly series around the January 2025 control change answers the same
  question for this cut.
- DHS naturalization flow reports: not needed once the LPR anchor proved non-discriminating.
- CPS replicate weights for monthly files: not held; the ASEC SE is used instead.

## Reproduction

From the repository root, run the scripts in this order. `derived/` is byte-identical on rerun:
sha256 of all 13 files matched before and after a full rerun on 2026-09-23.

```sh
bash infra/immigration-fiscal/mexborn_count_2026_09_23/fetch_basic.sh   # skips held, valid zips
for s in gate_asec monthly_series annual_series rotation_design cohort_compare \
         hispanic_geography control_jump benchmarks price_row4; do
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/mexborn_count_2026_09_23/$s.py
done
```

`benchmarks.py` reads cached copies of the OHSS page and the BLS PDFs. They were fetched with a
browser user agent (`curl -A …` for OHSS; the BLS PDFs through a web fetch) and converted with
`pdftotext -layout`. The Census API check used the untracked key, and output was redacted.

Model: claude-opus-5-5[1m] (Opus 5.5, 1M context).
