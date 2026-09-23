claude-opus-5-5[1m]

# Ancestry IV on commute time and native wages, 2000–2010

**Verdict:** The instrument measures neither slope. Z2 does not move metro population (first-stage
F 1.4–1.9). It fails the level placebo for both commute time and wages. Each of its origin terms
allocates that origin's 2000s national inflow according to where immigrants **from other
continents** settled in the same decade. That is the Burchardi–Chaney–Hassan pull, so across metros
Z2 measures a metro's same-decade attraction for immigrants rather than a pre-determined
shift-share. Its "Mexico" term follows Asian and European destinations: San Jose, Champaign,
Washington and Ann Arbor rank highest, and its R² with the change in the Mexico-born share is 0.000.

- **Congestion: $19.2bn stays borrowed from CDT.** Commute time changes −0.45% (SE 0.55) per point
  of foreign-born population share (Anderson–Rubin set −1.73% to +0.51%). Assuming no
  displacement, that is a time–population elasticity of −0.40 (0.49), 1.1 SE below
  Couture–Duranton–Turner's +0.12 (0.035). Taken at face value, it rules out B1 above $61bn. Once
  the 2000 commute level is held fixed, the elasticity is +0.26 (0.88) and nothing below $128bn is
  ruled out.
- **Wages: $66–166bn stays a calibration.** For natives without a BA, the estimate is −0.11%
  (0.32) per point of the immigrant share of employment. At the Mexican-origin group's 2024
  presence that is −1.2% (AR −10.1% to +5.5%) or −$47bn, and both the calibration's −2.2 to −4.2%
  and zero lie inside the interval. The relative wage of less-educated natives falls −0.64%
  (0.22) per point, which gives σ̂ 2.3 (AR 0.8–6.2), inside the calibration's range. But in the
  same metros it fell 2.5 times as much in the 1990s (−1.17, SE 0.31), before the inflow Z2
  predicts. In the two-inflow model the 2000s coefficient is +0.19 (0.31).

Lane result, 2026-09-23; not integrated anywhere, nothing in other lanes edited. Every number is
[CALCULATION] from this directory's scripts and `derived/` files unless tagged otherwise.
Percent effects are 100 × log points per percentage point of the treatment share; SEs are HC1,
population-weighted; "AR" is the Anderson–Rubin 95% set.

## What the estimates do to the two channels

| Channel | Account's value | This lane (IV with Z2) | Excludes, taken at face value | Why it cannot replace the account's value |
|---|---|---|---|---|
| Congestion, B1 | $19.2bn ($8.0–35.3bn); time elasticity +0.12 | −0.40 (0.49) in PC; −0.24 (0.49) without LA; B1 $0 at the point | B1 above $61bn (PC), $76bn (without LA); with the 2000 level held, nothing below $128bn | population not moved; level placebo +5.2% per unit Z2 (t 5) |
| Wages, natives without a BA | −2.2 to −4.2%; −$82 to −166bn | −1.2% (AR −10.1 to +5.5); −$47bn (AR −$385bn to +$211bn) | losses beyond 10.1%, gains beyond 5.5% | level placebo t 11; +1.29 (0.48) per point with the 2000 level held |
| High school or less | −3.7 to −7.0%; −$66 to −137bn | −1.4% (AR −8.8 to +4.6); −$25bn (AR −$161bn to +$84bn) | losses beyond 8.8% | same |
| Natives with a BA | +1.0 to +3.0% | +6.3% (AR −0.6 to +12.7) | nothing | 1990s placebo +1.54 (0.33) per point |
| Relative wage, σ | σ 1.5–2.5 | σ̂ 2.3 (AR 0.8–6.2), no BA / BA; σ̂ 6.2 (AR 3.3–16.4), high school or less / BA | the HS/BA pairing excludes 1.5–2.5, but it is not the calibration's pairing | 1990s placebo 2.5–3× the 2000s slope; the two-inflow 2000s coefficient is null |

The calibration values are from `wage_distribution_2026_09_23/derived/wage_distribution_long_run_default.csv`
(read through `derived/wage_implications.json`) and `congestion_2026_09_23/RESULT.md` [DATA].

## The instrument and the samples

**Construction.** Z2 = 100 × Σ_origins PushPull_10 × 1000 / 2000 population, taken from the
ancestry lane's `derived/cbsa_predicted_inflow.csv`; its `second_instrument.py` is imported, not
re-implemented. Gates G1/G2 reproduce that lane's first stage (0.3147, SE 0.0394, n 334) and SSI IV
(−0.2805, SE 0.0649) to 1e-9 before any new row is written. Variants: Z2_mex (Mexico's row),
Z2_exmex = Z2 − Z2_mex, Z (the displacement lane's pre-1990 settlement shift-share), Z+Z2 (with
Hansen's J), and Z2_1990s (PushPull_9, pre-trend work only).

**F4: what PushPull_10 measures.** BCH measure the pull from origin o toward county d as "the
fraction of migrants coming from anywhere in the world who settle in d at time t, excluding
migrants from the same continent as o". The push is o's arrivals at time t outside d's census
region. [SOURCE: Burchardi, Chaney and Hassan (2019), *Review of Economic Studies* 86(4), preprint
https://sciencespo.hal.science/hal-03260190. The file's page, https://www.immigrationshock.com/ancestry-instruments,
says its push-pull variables are their equation 3.] For the 2000–2010 wave, push and pull are
both same-decade flows. BCH's first stage has destination fixed effects that absorb a county's
overall attraction; a metro-level regression has none. Z2 is therefore national flows allocated by
each metro's same-decade attraction for other continents' immigrants, a contemporaneous
leave-out inflow [INFERENCE]. The Mexico rows show the consequence:

| Regressor, per 100 residents (341 metros) | R² with 2000 Mexico-born employment share | R² with its 2000–2010 change | R² with Mexican employment growth |
|---|---|---|---|
| Z2_mex (the file's Mexico PushPull_10) | 0.003 | 0.000 | 0.004 |
| Mexico PushPull_9 (1990s wave) | 0.001 | 0.000 | 0.011 |
| The file's predicted 2010 Mexican ancestry | 0.900 | 0.393 | 0.741 |

The largest Z2_mex values are San Jose (3.7), Champaign–Urbana (3.4), Washington (3.0), Ann Arbor
(2.8) and State College (2.6). State College's Mexico-born share of employment was 0.04% in 2000, and the file
predicts more Mexican arrivals for Centre County, PA (3.6k) than for Hidalgo, TX (1.9k).
[CALCULATION: `check_mexico_component.py` → `derived/mexico_component_check.csv`,
`derived/mexico_component_top_metros.csv`.] So "Z2 without Mexico" removes Mexico's national flow
as allocated by Asian, European and African settlement, not variation specific to Mexico. The
brief's Mexico-removed rows below carry that meaning.

**F1: geography.** The ancestry lane's panel matches 2000 rows built on the February-2013 CBSA
delineation to ACS 2010 rows published on the 2009 delineation, by code. Los Angeles (31080 vs
31100; 12.4m people, 34.8% foreign-born) and six other 100k+ metros have no match. 64 matched
codes carry different titles, several with different footprints (Gulfport–Biloxi 364k in 2000 vs
250k in 2010). New York's published 2010 foreign-born share is 28.79%, against 28.02% on a fixed
footprint. [DATA: `displacement_transfers_2026_09_18/derived/metro_panel.csv`; fixed footprint
from `derived/commute_metro.csv`.]

**F2: the first stage depends on the sample.**

| Sample | Treatment | First stage on Z2 | F |
|---|---|---|---|
| PC: the ancestry lane's 334 metros, its published 2010 endpoint | change in foreign-born share of population | 0.315 (0.039) | 63.9 |
| The same 334 metros, fixed 2008–12 county endpoint | same | 0.269 (0.049) | 29.6 |
| FG: all 341 metros of 100k+, fixed endpoint | same | 0.189 (0.080) | 5.5 |
| FG_noLA: FG without Los Angeles | same | 0.266 (0.049) | 30.0 |
| FG | change in foreign-born share of employment, 16–64 (IPUMS) | 0.658 (0.084) | 61.1 |
| FG_noLA / PC | same | 0.724 (0.073) / 0.728 (0.075) | 98.1 / 95.5 |

Los Angeles has Z2 = 6.2. Its foreign-born share of population fell 0.59 points while its
foreign-born share of employment rose from 40.9% to 43.9%. Unweighted, the FG population-share
first stage has F 77.

**F3: Z2 does not move population.** The first stage on the change in log population is 0.0067
(0.0058) with F 1.35 in FG, F 1.88 without LA and F 1.84 in PC. The IV of log commute on log
population is −0.13 (0.24), −0.08 (0.18) and −0.16 (0.22) respectively. All three AR sets are the
whole line, and the Wald bounds for these rows in `commute_implications.json` are flagged invalid.

**Microdata and gates.** IPUMS USA: the 2000 5% file (8,713,769 persons 16–64, 14.1% foreign-born),
the ACS 2010 (1,902,839; 16.35%) and the ACS 2009–11 (5,655,340), all on 2000-vintage PUMAs mapped
to 2013 CBSAs through Geocorr (PUMA merge miss 0.00% in 2000, 0.02% in 2010). The 1990 5% file uses its
county-identified footprint.

| Gate | Check | Result |
|---|---|---|
| G3 | 2000 PUMS mean commute vs SF3 P033001/P031002, 381 CBSAs | weighted correlation 0.994; mean gap +0.15 min |
| G4 | 2010 PUMS vs ACS 2010 1-year CBSA table, 372 CBSAs | 0.992; +0.12 min |
| G5 | PUMS 2000 persons 16–64 / SF1 population | median 0.622 (p05 0.573, p95 0.660) |
| 1990 footprint | weight in identified counties | 66.2%; 377 counties, 230 CBSAs; 220 with ≥ 50% of 2000 population (median 95%) |

[DATA: `derived/pums_checks.json`, `derived/pums_gates.json`.]

## Commute time

The outcome is mean one-way minutes of workers who do not work at home. In the summary tables it
is the 2000 SF3 aggregate over workers, and for 2010 either the ACS 2008–12 county file summed onto
2013 CBSAs (FG) or the ACS 2010 1-year CBSA table (PC). IPUMS gives natives' commute and natives'
car commute directly. The treatment is the change in the foreign-born share of population, in
points. Commute time conflates speed and distance: a metro whose jobs move closer to workers shows
shorter commutes at unchanged speed.

**Table C1. Log mean commute, % per point.**

| Row | PC (334) | FG_noLA (340) | FG (341) |
|---|---|---|---|
| First stage on Z2 | 0.315 (0.039), F 63.9 | 0.266 (0.049), F 30.0 | 0.189 (0.080), F 5.5 |
| OLS | −0.13 (0.24) | +0.00 (0.23) | +0.08 (0.19) |
| Reduced form on Z2 | −0.14 (0.16) | −0.07 (0.14) | −0.09 (0.13) |
| **IV, Z2** | **−0.45 (0.55)**, AR [−1.73, +0.51] | −0.27 (0.55), AR [−1.67, +0.70] | −0.47 (0.78), AR [−6.15, +0.87] |
| IV, Z2 without Mexico | −0.68 (0.53), AR [−1.96, +0.24] | −0.43 (0.53), AR [−1.73, +0.48] | −0.74 (0.83), AR [−22.7, +0.56] |
| IV, Z2 Mexico only | +0.02 (0.59), AR [−1.36, +1.11] | +0.06 (0.63) | +0.01 (0.77) |
| IV, Z (settlement) | −1.96 (0.87), AR [−4.20, −0.48]; first stage F 29.1 | −2.24 (1.00); F 12.0 | first stage F 0.17 |
| IV, Z+Z2; Hansen J p | −0.39 (0.55); 0.015 | +0.01 (0.53); 0.025 | +0.54 (0.47); 0.032 |
| IV, Z2, 2000 level held | +0.29 (1.00) | +0.74 (0.91) | +1.03 (1.46) |
| Level placebo: 2000 log commute on Z2 | +5.24 (1.03) | +5.22 (1.03) | +5.22 (0.94) |
| … given 2000 log population | +1.45 (0.43) | +1.42 (0.43) | +1.41 (0.43) |
| Level placebo on Z / on Z2 without Mexico | +3.87 (0.95) / +7.12 (1.52) | +3.85 (0.94) / +7.09 (1.52) | +3.09 (0.82) / +7.08 (1.36) |

The level placebos are in % of the 2000 commute per unit of the instrument. In minutes, the PC IV
is −0.16 (0.16) per point, AR [−0.54, +0.11]. [DATA: `derived/estimates_commute.csv`.]

**Table C2. Other commute outcomes, IV with Z2, % per point.**

| Outcome | Sample (n) | First-stage F | IV | AR |
|---|---|---|---|---|
| Log commute, change in transit and work-at-home shares held | PC (231) | 41.0 | −1.06 (0.65) | [−2.59, +0.13] |
| same | FG_noLA (340) | 37.0 | −0.72 (0.57) | [−2.08, +0.30] |
| Log commute without public transport (metros with complete county data) | PC (136) | 31.1 | −1.39 (0.87) | [−3.70, +0.06] |
| same | FG_noLA (99) | 6.3 | −4.83 (2.41) | [−23.7, −1.80] |
| Natives' commute, IPUMS 2009–11 | FG_noLA (340) | 30.0 | −0.41 (0.68) | [−2.06, +0.81] |
| Natives' car commute, IPUMS 2009–11 | FG_noLA (340) | 30.0 | −0.78 (0.67) | [−2.48, +0.40] |
| Natives' car commute, IPUMS 2010 | FG_noLA (340) | 30.0 | −0.73 (0.74) | [−2.52, +0.63] |
| All workers, IPUMS 2009–11 | FG_noLA (340) | 30.0 | −0.34 (0.67) | [−1.99, +0.85] |

The mode-share-controlled rows condition on outcomes of the inflow (bad controls). They are a
check, not the specification. The non-transit series exists only where the ACS 5-year B08136 is
unsuppressed in every county of the metro. The FG version (F 0.34) is unidentified.

**Mode shares (points per point, IV with Z2, FG_noLA):** transit +0.83 (0.46), AR [+0.08, +2.08];
work at home +0.32 (0.10), AR [+0.14, +0.56]; drove alone −1.18 (0.63), AR [−2.95, −0.18]; carpool
−0.41 (0.13), AR [−0.72, −0.15]. The inflow moved commuters out of cars. Transit commutes are
longer, so holding mode fixed makes the commute-time slope more negative (Table C2, first rows).

**Table C3. Conversion to the congestion lane's elasticity and B1.** The time–population
elasticity is the IV divided by the population change per point of foreign-born share with no
displacement, d ln P = ds/(1 − s): 1.13% per point, with s the 2000 weighted foreign-born share of
the sample (0.115–0.127). B1 is the congestion lane's own arm (`arms.arm_pop`) evaluated on its
saved central exposure. It reproduces the lane's three grid points ($13.91bn, $19.16bn, $24.21bn at
0.085, 0.12, 0.155) to 1e-14 [CALCULATION: `derived/commute_implications.json`,
`b1_model_positive_control`].

| Specification | Elasticity (SE) | Interval | B1 at the upper end |
|---|---|---|---|
| PC, log commute | −0.40 (0.49) | AR [−1.53, +0.46] | $60.8bn |
| FG_noLA, log commute | −0.24 (0.49) | AR [−1.48, +0.62] | $75.6bn |
| FG, log commute (F 5.5) | −0.41 (0.68) | AR [−5.37, +0.76] | $86.1bn |
| FG_noLA, natives' car commute 2009–11 | −0.69 (0.60) | AR [−2.20, +0.36] | $49.6bn |
| PC, mode shares held (bad control) | −0.94 (0.58) | AR [−2.29, +0.11] | $18.3bn |
| PC, 2000 level held | +0.26 (0.88) | Wald [−1.47, +1.99] | $128.2bn |
| FG_noLA, 2000 level held | +0.65 (0.80) | Wald [−0.92, +2.23] | $133.6bn |
| CDT, the account's B1 | +0.12 (0.035) | — | $19.2bn |

Every Z2 point estimate in the long difference is negative, so B1 is $0 at the point. The conversion
assumes one added resident per immigrant. The measured log-population response per point is
+2.8% (2.0) in PC (AR −1.4% to +6.6%), and at that value the PC elasticity would be −0.16. The OLS
of log commute on log population change is +0.00 (0.02) in FG and −0.02 (0.02) in PC: metros that
grew faster in 2000–2010 did not see longer commutes. That is not CDT's fixed-lanes slope, since
roads and job locations adjusted [INFERENCE].

**Pre-trend, commute (FG_1990fp, n 220).** Natives' commute over 1990–2000 on the 2000s treatment:
−0.23 (0.29); natives' car commute −0.10 (0.30). The 2000s estimates on the same metros are −0.42
(0.32) and −0.51 (0.33). There is no pre-trend. Double differences on the acceleration of the
foreign-born share give +0.27 (0.64) and +0.57 (0.64).

**Reading.** In the long difference, commute times did not rise with the inflow Z2 predicts, and
the AR sets exclude elasticities above about 0.46–0.76. That bound depends on a specification that
fails the level placebo: each unit of Z2 goes with a 5.2% longer 2000 commute, 1.4% conditional on
size.
The specification that answers the placebo is too imprecise to exclude anything below the model's
free-flow cap. Neither can move the $19.2bn central, which remains CDT's cross-section.

## Native wages

**Outcomes.** Composition-adjusted log weekly wages of native full-time full-year wage workers
25–64 (weeks 50–52, 35+ hours), and log hourly wages of all native wage workers 25–64. Real
hourly wages are trimmed to $2–200 in 1999 dollars. Each person's log wage is taken net of the
national native mean in their cell of 8 age bands × sex × 5 education levels in the same sample
year, and the net values are averaged by metro. "Relative" is the no-BA mean minus the BA mean.
**Treatment:** the change in the foreign-born share of employment 16–64 (the brief's), plus
Card's inflow rate, the Mexico-born share and Δln(L/H). Main sample FG, 2010 ACS endpoint.

**Table W1. FG, 2010, % per point of foreign-born employment share (n 341; first stage 0.658
(0.084), F 61.1).**

| Row | Natives without a BA | High school or less | Natives with a BA | Relative (no BA − BA) |
|---|---|---|---|---|
| OLS | +0.36 (0.21) | +0.26 (0.20) | +0.44 (0.23) | −0.08 (0.14) |
| Reduced form on Z2 | −0.07 (0.21) | −0.08 (0.18) | +0.35 (0.20) | −0.42 (0.12) |
| **IV, Z2** | **−0.11 (0.32)**, AR [−0.86, +0.47] | −0.12 (0.28), AR [−0.75, +0.39] | +0.54 (0.28), AR [−0.05, +1.08] | **−0.64 (0.22)**, AR [−1.15, −0.26] |
| IV, Z2 without Mexico (F 65.1) | −0.04 (0.28), AR [−0.68, +0.47] | −0.05 (0.26) | +0.48 (0.25), AR [−0.05, +0.97] | −0.52 (0.19), AR [−0.95, −0.17] |
| IV, Z2 Mexico only (F 37.3) | −0.29 (0.51), AR [−1.56, +0.57] | −0.29 (0.42) | +0.68 (0.41) | −0.97 (0.34), AR [−1.87, −0.43] |
| IV, Z (F 4.7, weak) | +0.16 (0.39) | +0.18 (0.34) | +0.36 (0.48) | −0.20 (0.46) |
| IV, Z+Z2; Hansen J p | −0.11 (0.33); 0.39 | −0.12 (0.28); 0.25 | +0.54 (0.28); 0.71 | −0.65 (0.22); 0.30 |
| IV, Z2, 2000 level held | +1.29 (0.48) | +1.16 (0.45) | +1.99 (0.54) | −1.30 (0.33) |
| Level placebo: 2000 level on Z2 | +4.07 (0.36) | +3.72 (0.35) | +5.33 (0.46) | −1.26 (0.20) |
| … given 2000 log population | +2.35 (0.44) | +2.17 (0.44) | +2.77 (0.55) | — |
| Level placebo on Z2 without Mexico / on Z | +5.32 (0.69) / +2.15 (0.43) | +4.78 (0.67) / +1.88 (0.43) | +7.18 (0.83) / +2.94 (0.52) | −1.86 (0.30) / −0.79 (0.12) |

Hourly: no BA −0.06 (0.28), AR [−0.68, +0.44]; BA +0.85 (0.29), AR [+0.24, +1.40]; relative −0.92
(0.17). Unadjusted weekly: no BA −0.25 (0.35), BA +0.63 (0.31). Some college: −0.20 (0.40). Native
employment 25–64 (log change): +0.29 (0.68), AR [−1.24, +1.54], so there is no sign of natives
leaving, though the interval is wide. [DATA: `derived/estimates_wages.csv`.]

**Table W2. The same IV across samples, endpoints and treatments.**

| Sample, endpoint, treatment | First-stage F | No BA | BA | Relative |
|---|---|---|---|---|
| FG, 2010, foreign-born employment share | 61.1 | −0.11 (0.32) | +0.54 (0.28) | −0.64 (0.22) |
| FG, 2009–11 | 83.2 | −0.10 (0.29) | +0.58 (0.27) | −0.68 (0.16) |
| FG_noLA, 2010 | 98.1 | −0.04 (0.31) | +0.56 (0.27) | −0.60 (0.20) |
| PC, 2010 | 95.5 | −0.04 (0.31) | +0.55 (0.27) | −0.59 (0.20) |
| PC, 2009–11 | 130.8 | −0.03 (0.28) | +0.58 (0.26) | −0.61 (0.14) |
| FG, 2010, Card inflow rate | 44.5 | −0.06 (0.18) | +0.30 (0.16) | — |
| FG, 2010, Mexico-born share of employment | 6.6 on Z2; 0.00 on Z2 Mexico only | −0.52 (1.55) | +2.65 (2.02) | −3.17 (1.62) |

The Mexico-born treatment is weak on Z2 and has no first stage at all on the Mexico term (F4
explains why), so there is no Mexico-specific wage estimate.

**Every specification computed.** `derived/spec_summary.csv` counts all IV rows by outcome,
treatment and arm. The long-difference arm has 30 rows per outcome for the foreign-born
employment-share treatment (3 samples × 2 endpoints × 5 instrument sets), 28 of them with
first-stage F ≥ 10:

- **Natives without a BA:** coefficients −0.29 to +0.34, none excluding zero by Wald or AR. With
  the 2000 level held, all 28 are positive and significant (+0.88 to +2.68).
- **High school or less:** −0.41 to +0.33, none significant.
- **Natives with a BA:** +0.39 to +0.70, 15 of 28 significant; AR excludes zero in 9 of 22.
- **Relative wage:** −0.97 to −0.09, 24 of 28 significant; AR excludes zero in 18 of 22.
- **Log commute:** −2.2% to +0.1% per point across 10 strong rows, and the only two significant
  rows use Z.

**Table W3. Relative wage on relative supply: the CES slope −1/σ.**

| Pairing, sample, endpoint | First stage on Z2 (F) | IV, Z2 | AR | σ̂ (AR) | Z2 without Mexico, σ̂ | Z, σ̂ |
|---|---|---|---|---|---|---|
| No BA / BA, FG, 2010 | 0.96 (0.29), 11.2 | −0.44 (0.20) | [−1.24, −0.16] | 2.3 (0.8–6.2) | 3.5 | 15 (F 31.9) |
| No BA / BA, FG, 2009–11 | 0.77 (0.27), 7.8 | −0.58 (0.25) | [−2.12, −0.27] | 1.7 | 2.6 | 9 |
| No BA / BA, FG_noLA, 2010 | 0.86 (0.29), 9.0 | −0.50 (0.24) | [−1.66, −0.18] | 2.0 | 3.2 | 17 |
| No BA / BA, PC, 2010 | 0.84 (0.29), 8.5 | −0.51 (0.25) | [−1.78, −0.18] | 2.0 | 3.2 | 16 |
| High school or less / BA, FG, 2010 | 2.66 (0.40), 43.1 | −0.16 (0.06) | [−0.31, −0.06] | 6.2 (3.3–16.4) | 8.2 | 41 |

OLS is +0.01 (0.03). Z+Z2 rejects over-identification (J p 0.013 for no BA / BA, 0.040 for high
school / BA): the two shift-shares disagree. The calibration's σ applies to high school or less
against everyone above high school, which is not the HS/BA pairing here. Scaled by the group's
11.8% shift in ln(L/H), the no-BA/BA slope implies a relative-wage effect of −5.2% (AR −14.7% to
−1.9%). The calibration's gap is −3.8% to −7.2%.

**Table W4. Pre-trend battery (FG_1990fp, n 220; 2000s first stage 0.638 (0.096), F 44.2).**
Here Z2 predicts the 1990s change in the foreign-born employment share more strongly than the
2000s change (1.09 (0.08), F 198, vs 0.64). The two decades' changes correlate (OLS 0.56 (0.06)).

| Outcome, % per point | 1990s change on the 2000s treatment (placebo) | 2000s, same metros | 2000s, own 1990s change held | 2000s minus 1990s, on the acceleration | Two inflows: 2000s / 1990s | Persistence of the outcome change |
|---|---|---|---|---|---|---|
| Relative wage | **−1.17 (0.31)**, AR [−1.99, −0.68] | −0.46 (0.24) | −0.64 (0.28) | −1.00 (0.48) on the foreign-born share; **+0.26 (0.10)** on ln(L/H) | **+0.19 (0.31)** / −0.39 (0.19) | −0.04 (0.09) |
| No BA | +0.36 (0.29) | +0.08 (0.37) | +0.10 (0.39) | +0.40 (0.60) | +1.27 (0.51) / −0.70 (0.25) | −0.06 (0.10) |
| High school or less | +0.01 (0.34) | +0.05 (0.32) | +0.05 (0.32) | −0.05 (0.62) | +0.85 (0.47) / −0.47 (0.23) | −0.02 (0.10) |
| BA | **+1.54 (0.33)**, AR [+0.93, +2.27] | +0.54 (0.33) | +1.07 (0.35) | +1.40 (0.68) | +1.08 (0.50) / −0.31 (0.22) | −0.14 (0.10) |
| Relative wage on ln(L/H) (σ design) | −0.60 (0.17) | −0.24 (0.14) | — | — | — | — |
| HS / BA relative wage on ln(HS/BA) | −0.34 (0.06) | −0.11 (0.06) | — | +0.27 (0.11) | −0.23 (0.33) / −0.16 (0.17) (on the foreign-born share) | +0.02 (0.07) |
| ln(L/H) | −0.82 (0.53) | +1.95 (0.55) | +2.25 (0.50) | — | — | +0.36 (0.09) |

The two-inflow model is Jaeger–Ruist–Stuhler's: the 2000s change on both decades' inflows, with Z2
and Z2_1990s as instruments. Its Sanderson–Windmeijer conditional F is 45.0 for the 2000s inflow
and 103.3 for the 1990s inflow. The double-difference first stages are −0.45 (0.12), F 14.5, for the
foreign-born share and +1.77 (0.26), F 46.4, for ln(L/H); the two treatments moved in opposite
directions in high-Z2 metros. [DATA: `derived/estimates_pretrend.csv`.]

**Reading.** The level of less-educated natives' wages shows no response in any specification
except the 2000-level arm, where the response is positive. The relative wage of less-educated
natives fell in high-Z2 metros in both decades. The 1990s decline, measured before the inflow Z2
predicts, is 2.5 times the 2000s decline on the same metros. Two readings fit:

- **Each decade's inflow lowers the relative wage in the decade it arrives.** Z2 predicts both
  inflows, and the relative-wage change does not persist across decades (−0.04). This reading is
  supported by the lagged-change control, which leaves −0.64 (0.28).
- **A standing gap in relative wage growth in immigrant metros.** This reading is supported by the
  two-inflow model, where the 2000s inflow gets +0.19 (0.31), and by the double difference on
  relative supply (+0.26 (0.10)).

The design cannot choose between them. F4 adds a third reason for doubt: a metro's same-decade
attraction for immigrants from other continents plausibly moves skill prices directly.

**Table W5. Scaled to the Mexican-origin group's 2024 presence.** The group is 11.76 points of 2024
earners (Mexico-born 4.58; all foreign-born 19.29), from the CES account's own CPS branch file
[DATA: `production_nativity_nest_2026_09_22/derived/branch_composition.csv`, PEARNVAL proxy]. The
IV per point is multiplied by 11.76, and dollars use natives' 2024 earnings in the group ($3,821bn
without a BA, $1,829bn high school or less, $5,615bn with a BA).

| Group | This lane: point (AR) | Dollars (AR) | CES calibration |
|---|---|---|---|
| Natives without a BA | −1.2% (−10.1% to +5.5%) | −$47bn (−$385bn to +$211bn) | −2.2% to −4.2%; −$82bn to −166bn |
| High school or less | −1.4% (−8.8% to +4.6%) | −$25bn (−$161bn to +$84bn) | −3.7% to −7.0%; −$66bn to −137bn |
| Natives with a BA | +6.3% (−0.6% to +12.7%) | +$354bn (−$36bn to +$713bn) | +1.5% to +3.0% (below-BA split); +1.0% to +2.0% (HS split) |
| Relative, no BA − BA | −7.5% (−13.5% to −3.1%) | — | −3.8% to −7.2% |

The scaling is linear in a local, relative estimate. It also treats the group's US-born members as
the same supply shock as immigrants, which is the calibration's own convention.

## Adjacent check: ladder 182 on fixed geography

The ancestry lane's household-receipt IV re-run with a fixed 2010 endpoint (ACS 2008–12 counties
summed onto 2013 CBSAs), per point of foreign-born population share:

| Sample | First stage on Z2 (F) | SSI, IV Z2 | AR | Without Mexico | Z | Public assistance, IV Z2 |
|---|---|---|---|---|---|---|
| Lane panel, published 2010 (334) | 0.315 (0.039), 63.9 | −0.281 (0.065) | [−0.43, −0.17] | −0.292 (0.066) | −0.443 (0.098) | −0.10 (0.19) |
| Same 334, fixed endpoint | 0.269 (0.049), 29.6 | −0.272 (0.117) | [−0.61, −0.095] | −0.293 (0.110) | −0.779 (0.299) | −0.17 (0.24) |
| All 341, fixed | 0.189 (0.080), 5.5 | −0.363 (0.189) | [−2.24, −0.13] | −0.407 (0.215) | weak (F 0.2) | −0.41 (0.41) |
| 340 without LA | 0.266 (0.049), 30.0 | −0.275 (0.117) | [−0.61, −0.098] | −0.296 (0.109) | −0.802 (0.306) | −0.19 (0.24) |

The SSI sign and size survive; the SE roughly doubles and F halves. The SSI level placebo passes in
every sample (−0.055 to −0.087, SE about 0.08). Wages and commute time fail it (Tables C1, W1), so the ancestry
lane's "passes the level placebo" holds for SSI only. F4 applies to ladder 182 as well.
[DATA: `derived/ssi_fixed_geography.csv`.]

## Limits

1. **Instrument (F4).** Same-decade pull with no destination fixed effects. The failed level
   placebos and the 1990s placebo on relative wages are what that construction predicts. Read the
   IV numbers as how outcomes co-move with a metro's 2000s attraction for immigrants.
   Z2_1990s has the same construction for the 1990s, so the two-inflow split rests on two
   same-decade pulls.
2. **Local, relative effects.** Cross-metro designs estimate effects relative to other metros.
   National effects can be larger if natives, capital or trade spread the shock
   [TRAINING-DATA: Borjas 2006 on native internal migration; Dustmann, Schönberg and Stuhler 2016
   on what spatial designs identify]. The native employment response here is +0.29 (0.68), a null
   with a wide interval.
3. **Commute time is not speed.** Distance, mode and job location all move. Non-transit time
   covers only 99–136 metros, those with complete county data. There is no lane-mile control: the
   UMR workbook has none and HPMS was not pulled.
4. **Composition adjustment** covers observable cells. It does not correct for selective native
   stayers.
5. **1990 footprint** is partial (median 95% of the 2000 population; 220 metros at ≥ 50%).
6. **B1 above ε 0.155** evaluates the congestion lane's model outside the range it ran. More urban
   areas hit the free-flow cap there.
7. **The ACS 2010 one-year file is small** (628,696 FTFY natives); the 2009–11 file checks it and
   agrees (Table W2).
8. **Instrument bias of the analyst.** The brief fixed the specification menu, and every computed
   row is in `derived/` with the summary in `spec_summary.csv`.

## What would measure these slopes (successor ideas, not done)

- **A pre-determined ancestry instrument.** Predict 2000 ancestry from the file's pre-2000 waves
  (PushPull_1–9) and interact it with 2000s national origin flows. This is the stock-based use
  BCH's design supports. Then run the same placebo battery. [INFERENCE]
- **Road speed.** Link-level speeds (NPMRDS or HPMS) and lane-miles, so speed is separated from
  distance and road building. The ACS commute cannot do this.

## Reproduce

```sh
# from the repository root; keys are read inside the scripts and never printed
L=infra/immigration-fiscal/ancestry_iv_congestion_wages_2026_09_23
set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a
uv run --no-project python3 $L/ipums_extract.py submit core pre   # then: wait, download
uv run --no-project python3 $L/fetch_commute.py
for s in build_commute build_pums build_pums_1990; do
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with xlrd python3 $L/$s.py; done
for s in gate_pums estimate_commute estimate_wages estimate_pretrend check_ssi_fixed_geography \
         check_mexico_component spec_summary; do
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with statsmodels --with scipy python3 $L/$s.py; done
```

Other lanes' code is imported read-only with bytecode writing off:
`ancestry_instrument_2026_09_22/second_instrument.py` (instrument, estimators) and
`congestion_2026_09_23/arms.py` (B1). IPUMS microdata (core 323.5 MB, pre 131.3 MB) and Census API
pulls stay in `_cache/`, which is ignored.

## Files

| File | Content |
|---|---|
| `ipums_extract.py`, `fetch_commute.py` | IPUMS extracts #10 (core) and #11 (1990); Census SF1/SF3/ACS pulls with row-count checks |
| `build_commute.py` → `derived/commute_metro.csv` | commute, mode shares, fixed-footprint 2010 values and SSI/PA per CBSA |
| `build_pums.py`, `build_pums_1990.py` → `derived/pums_metro*.csv` | CBSA × sample weighted sums: wages, cells, employment, commute |
| `gate_pums.py` → `derived/pums_gates.json`; `derived/pums_checks.json` | G3–G5 and extract checks |
| `common.py` | instrument import, gates G1/G2, samples, AR sets, specification menu |
| `estimate_commute.py` → `derived/estimates_commute.csv`, `commute_implications.json` | 1,428 commute rows; elasticity and B1 mapping |
| `estimate_wages.py` → `derived/estimates_wages.csv`, `wage_implications.json` | 6,852 wage rows; presence scaling, σ design |
| `estimate_pretrend.py` → `derived/estimates_pretrend.csv` | 1,150 rows: placebos, lagged control, double differences, two-inflow IV, persistence |
| `check_ssi_fixed_geography.py` → `derived/ssi_fixed_geography.csv` | ladder-182 check |
| `check_mexico_component.py` → `derived/mexico_component_*.csv` | F4 |
| `spec_summary.py` → `derived/spec_summary.csv` | every IV row summarised |

## Covered and skipped

Covered: every item in the brief. That includes commute on the foreign-born share and on log
population, with and without mode shares, converted to the CDT elasticity. It includes wages
without and with a BA (FTFY weekly and all-worker hourly, cell-adjusted), on the immigrant and
Mexico-born shares, scaled to the group's presence. Each outcome has its first stage, reduced
form, OLS, level placebo and Mexico-removed instrument. Added beyond the brief: fixed geography
(F1–F2), the 1990s pre-trend battery, the σ design, the ladder-182 check, and the diagnosis of
what PushPull_10 measures (F4). Skipped, with reasons:

- Lane-mile control: not in the UMR workbook, HPMS not pulled.
- UMR travel-time index: modelled before 2009.
- Drive-alone time: not in SF3 2000.
- Log population and BA share as trend controls in the main specification: the 2000-level arm and
  the pre-trend battery cover the concern.
- A Mexico-specific wage estimate: no first stage (F4).
