# Percentile → percentile mapping: design (prereg draft)

2026-09-29. Status: draft, not attacked, nothing run. Builds on
[selection_curve_2026_09_27](../selection_curve_2026_09_27/RESULT.md) (ladder entry of that lane), which
measured the chain descriptively: origin pct → US pct (slope 1.19, R² 0.28 ex-Mexico, adult arrivals)
and G1 → G2 group slopes 0.52 education / 0.55 earnings over 78 origins (0.36 / 0.30 without Mexico).
India 95 → 73 → 73. This design asks what those slopes identify and how to project a future G2 from
a changing parent pool (the operator's Indian question: are the post-2000 cohorts less selected, and
what do their children become?).

## 1. Construct

Three links, each a different object:

| Link | Object | What it is not |
|---|---|---|
| A. origin pct → G1 US pct | how a migrant's standing at home converts to standing here, by admission route and years in the US | a measure of ability; it mixes ability, credential transfer, language, route and survivorship |
| B. G1 US pct → G2 US pct | how much of the parents' US standing the children keep | the individual rank-rank slope (≈0.3 in US tax data); a group-mean carryover is larger because group traits transmit on top of family |
| C. origin population mean → G2 | whether children regress toward their *origin population's* mean, not the US mean | measured by B; B alone assumes regression toward the US mean |

The load-bearing first-principles point is C. A migrant's position is part persistent (traits that
transmit) and part transitory (luck, credential, a visa lottery, the job offer). Children regress
toward the mean of the population whose persistent traits they inherit. If the migrants are a
selected slice of a low-mean origin, their children regress toward that origin's mean, and a model
with only parent pct (link B) over-projects them. Clark's surname work puts persistence of the
latent component near 0.7–0.8 per generation against ≈0.3–0.5 for measured outcomes
[TRAINING-DATA, verify before use]. This is the Galton structure; it predicts that
G2 = a + b·p1 + c·μ_origin with c > 0, and that c grows as the transitory share of selection grows.

## 2. Model

Latent persistent standing z and observed pct p = f(z + e), e transitory.

- Selection: migrants from origin o have z drawn from the origin distribution truncated by the
  route's filter (employment visa, student, family, lottery, unauthorized). Routes filter on
  different things: an employment visa on a job offer (observed skill + luck), family on kinship
  (little skill filter), unauthorized on willingness and proximity.
- Transmission: z_child = μ_o + λ (z_parent − μ_o) + u, with λ the persistent-trait carryover and
  μ_o the origin population mean on the same scale.
- Observed G2 pct = f(z_child + e_child), plus a US-environment uplift δ (the ≈5-point common
  uplift the selection-curve lane found at the white median).

What each quantity needs:
- μ_o on the US scale: origin-country education (Barro-Lee, WIC) mapped to US percentiles; for
  cognitive skill, PISA/PIAAC/TIMSS country means where available. Coarse, and education quality
  differs across countries; carry two scales and report both.
- Parent z vs e split: the reliability of parent pct as a measure of persistent standing. Two
  routes: (i) repeated measures of the same parents (CPS rotation 2 years; ACS synthetic cohorts
  over years since arrival), giving the transitory variance; (ii) route contrasts: a lottery
  route (DV lottery) selects less on z than an employment route at the same education, so the
  route difference in G2 at equal parent pct identifies how much of parent pct is persistent.

## 3. Arms (estimation specs), all on the same outcome, universe and reference

| Arm | G2 pct regressed on | Identifies |
|---|---|---|
| B0 | parent-origin mean G1 pct (the existing 0.52) | baseline, replicate first |
| B1 | + μ_origin (origin population mean on US scale) | c, regression toward origin mean |
| B2 | B1 + route mix of the parent cohort (employment share, from DHS LPR by country × year) | whether selection by route transmits |
| B3 | B1 with parent pct split into education-predicted and residual (earnings net of education) | whether the unobserved part transmits |
| B4 | individual level where parents are linked (NLSY97 parent linkage; CPS/ACS co-resident children) | individual λ vs group slope |

The rule is identical for every origin: same reference (third-plus NH whites, year × 5-year age
cell, mid-rank), same universe (25–64), same weights. Mexico enters every arm and is also reported
held out, because it is the high-leverage point (without it the slopes fall to 0.36 / 0.30).

## 4. Controls and falsifiers

- **Negative control:** permute μ_origin across origins; c must return ≈0 (it can pass; it can
  fail if μ is collinear with parent pct, so report the collinearity).
- **Positive control:** simulate the §2 model with known λ and c from the observed origin set,
  run B0–B3, recover the parameters. If B1 cannot recover a planted c at our n, the design cannot
  answer the question and says so.
- **Out-of-time test (the real one):** fit on G2 born to parents arriving before 1985 (adults
  now), predict the G2 of 1985–1995 arrivals (now 25–40), compare with observed. A model with c
  should beat B0 on held-out origins whose migrants are strongly selected from low-mean origins
  (India, Nigeria, Philippines) and tie on origins near the US mean (Canada, UK).
- **Early readout of the future G2:** children of post-2000 arrivals are school age. Check whether
  a test-score file identifies parent birthplace country: ECLS-K:2011 suppresses child birthplace
  in the public file (register); verify parent-birthplace fields before relying on it. Other
  candidates: HSLS:09, NAEP restricted, state test files with home language (Telugu, Gujarati,
  Hindi as proxies). A test-score percentile for Indian-origin children by parents' arrival
  cohort would test the projection directly.

## 5. Witness pairs

| Surface | Passes on | Fails on |
|---|---|---|
| c > 0 (regression toward origin) | Indian G2 at 73 when parents 73 and μ_India ≈ 20 → requires the unobserved selection to be persistent (λ high); consistent with c small | Nigerian or Indian G2 of later cohorts falling below their parents' pct by more than B0 predicts |
| Route transmits (B2) | employment-route origins' G2 above B1's prediction | family/lottery-route origins at equal parent pct matching employment-route ones |
| Cohort decline (Indian) | post-2000 parent cohorts' US pct below the 1965–90 cohorts' at equal years in US | equal or higher |

## 6. Measurement traps (each named in an existing lane)

- Duration and survivorship: a cohort's US pct rises with years in the US and falls through
  selective return (H-1B non-renewals leave). Compare cohorts at equal years since arrival; flag
  survivorship as unmeasured unless NIS Round 2 (not held) is acquired.
- Age at arrival: adult arrivals only for link A (schooling abroad).
- Synthetic cohorts: G2 observed today are children of older waves, not the current ones.
- Assortative mating: Indian G1 endogamy 96%; both parents come from the same selection, so the
  family's position is the couple's, and dependent spouses (H-4) are selected through the principal.
- Identity attrition in G3 (ladder 232 for Mexicans; the Indian G3 cell is n = 49).

## 7. Decision rule, before data

- c's 95% interval excludes 0 and the out-of-time test favours B1 over B0 by at least 2 pct points
  of mean absolute error on held-out origins → project the Indian future G2 with B1.
- c's interval includes 0 and the out-of-time test ties → B0 stands; report c as not identified
  at this n, with its interval.
- The positive control fails to recover a planted c → no claim about regression toward the origin
  mean from this data; the projection carries B0 and B1 as a range.

## 8. Heretic before results

A cross-lab attack on this draft (the causal structure in §1–2 and the identification in §3–4)
comes before any estimation run.

## Revision 1 — after the cross-lab attack (2026-09-29)

GPT-6 Astra, xhigh, [attack_astra.md](attack_astra.md). Each finding checked against the design and
the selection-curve outputs; the one numerical claim was verified: the B0 education line is
28.72 + 0.522·G1 (`selection_curve_2026_09_27/derived/slopes.csv`), fixed point 60.1, so §1's
"B alone assumes regression toward the US mean" is wrong — B0 already regresses toward about 60.

| # | Finding | Verdict | Change |
|---|---|---|---|
| 1 | c is estimable but not a mechanism; US conditions tied to origin load on it | accept | B1's estimand is renamed "incremental association of origin conditions with G2"; no reversion claim from B1 alone |
| 2, 7 | the national mean is the wrong reference; with a fixed India mean the c term cancels for any within-India change in selection | accept, decisive | the projection for India needs **sub-population means** (state × caste × language from IHDS/NSS/PLFS) and the migrant mixture over them (ACS home language by arrival cohort, being built in `indian_cohort_selection_2026_09_29`); national μ stays only as a contextual predictor |
| 3 | percentile means don't recover latent transmission; b and c are composites | accept | percentile models are predictive only; the Clark calibration of λ is dropped |
| 4 | route contrasts are not randomized; conditioning on parent standing opens a collider | accept | B2 is predictive heterogeneity only |
| 5 | reliability measures stability, not transmission; ACS gives no within-person repeats | accept | B3 relabelled descriptively; repeat-measure reliability dropped as an identification route |
| 6 | the out-of-time test needs parent arrival years for adult G2, which CPS/ACS do not carry | accept, gate | **step 0 is a linkage audit** (NLSY97 parent linkage, CILS, co-resident ACS/CPS); if no file links adult G2 to parents' arrival, the test becomes an explicit synthetic-cohort exercise and makes no forecast-validation claim |
| 8, 9, 10 | context, assortative mating, return migration and period effects | accept | both parents' characteristics; childhood destination; attrition bounds; claims limited to residents |
| 11, 12 | permutation and planted-effect controls pass under confounding | accept | conditional-null simulation on the fixed predictor matrix, plus zero-reversion scenarios with subgroup mixtures and destination effects |
| 13, 14 | weighting target and decision rule gaps | accept | loss targets India's future cohorts; the decision rule separates "forecasts better" from "mechanism supported"; numeric predictions written before fitting |

What survives: the question is now two separable pieces. (a) **Composition:** has the Indian flow
shifted toward sub-populations with lower home means (region, caste, route)? Measurable from ACS
language × cohort and India-side sub-population data. (b) **Transmission:** given a family's
standing, how far do its children fall back, and toward what? Only linked parent–child data
answer that, and step 0 decides whether we have any. No estimation lane runs before the
composition result and the linkage audit are in.
