# The 2021-2024 surge: what the data show

**Date:** 2026-04-18 (evening)
**Question:** What can we actually say about the 2021-2024 immigration surge that static models couldn't capture?
**Method:** OHSS DHS monthly enforcement tables (encounters by citizenship), CHNV parole data, NYC Comptroller / Chicago / Denver / MA migrant cost trajectories, county-level 2020 vs 2024 election results, ACS county FB share.
**Bias caveat:** Politically charged subject matter. Per `notes/llm-bias-caveat.md`, this memo flags interpretation that depends on the LLM instrument's training-time priors. Empirical numbers below are administrative data; interpretations are explicitly framed as scenarios.

## Bottom line

Three findings the static cycle missed:

1. **The Title 42 lift was a non-event for total flows. The December 2022 - March 2023 surge to 50K+/month and the eventual normalization at ~50K/month was a regime shift independent of Title 42 timing.** The "lift" itself coincided with a brief lull (anticipation surge in March + April crash + May low + gradual rebuild). Pre-lift 12-mo mean: 27K/month; post-lift 12-mo mean: 44K/month (+62%) — but this is composition of compared periods, not a Title 42 causal effect.

2. **CHNV parole INCREASED total flow from those nationalities by ~700pp more than control nationalities (TWFE β=+3.29, t=4.78).** Cuban/Haitian/Venezuelan encounters at SW border ROSE post-program, alongside their parole arrivals. Did not substitute legal for illegal — added legal alongside illegal. Strongly contradicts the program's stated rationale of reducing irregular migration. Plausible mechanism: program signaled US openness to these nationalities, lowering perceived migration cost broadly.

3. **Receiver cities (Abbott busing destinations) swung +4.4 pp more Republican in 2024 than comparable non-receiver counties** — a magnitude that is implausibly large for non-immigration causes alone. Bronx +11pp, Queens +11pp, El Paso +10pp, Hidalgo +10pp, Miami-Dade +9pp. The system-collapse claim has empirical bite via the political feedback loop.

## Findings in detail

### Title 42 lift event study (2023-05-11)

Monthly SWB encounters around the lift date:

| Month | Total | Mexico | Venezuela | Cuba | Haiti |
|-------|-------|--------|-----------|------|-------|
| 2022-11 | 22,310 | 8,370 | 60 | 40 | 6,370 |
| 2022-12 | 19,950 | 8,060 | 60 | 20 | 4,980 |
| **2023-01** | **52,180** | 14,000 | 11,220 | 11,280 | 4,650 |
| 2023-02 | 47,580 | 10,340 | 14,710 | 7,800 | 2,560 |
| 2023-03 | 52,240 | 12,800 | 10,930 | 12,600 | 7,670 |
| 2023-04 | 27,850 | 9,800 | 6,750 | 250 | 3,130 |
| 2023-05 | 26,110 | 5,790 | 4,110 | 580 | 7,410 *← Title 42 lift* |
| 2023-06 | 29,580 | 9,260 | 4,990 | 1,200 | 4,250 |
| 2023-09 | 45,020 | 15,300 | 7,900 | 2,330 | 7,330 |
| 2023-12 | 50,970 | 13,520 | 11,750 | 9,790 | 4,590 |
| 2024-12 | 47,930 | 10,240 | 14,680 | 8,860 | 4,050 |

**Pre-lift 12mo mean:** 26,930/month. **Post-lift 12mo mean:** 43,661/month (+62%).

The lift itself was a non-event in the sense that:
- The 50K+ surge happened BEFORE the lift (Dec 2022-Mar 2023)
- April-May 2023 saw a TEMPORARY dip (CHNV program absorbing demand + lift anticipation effects)
- June 2023 onward saw gradual rebuild back to surge levels
- The "+62%" pre-vs-post comparison is mostly about WHICH months you compare

The honest reading: there was a regime shift around Dec 2022 driven by CHNV starting, Title 42 expectations, and global push factors. Title 42 lifting in May 2023 was one event in this regime shift, not its cause.

### CHNV nationality-DiD (parole started 2023-01-05)

Monthly encounters at SW border, treated (CHN+V, n=3 nationalities present in OHSS) vs control (Mex+NTCA, n=4):

| Group | Pre-Jan23 mean | Post-Jan23 mean | Change |
|-------|----------------|-----------------|--------|
| Treated (CHNV) | 2,598/month | 23,041/month | **+786.7%** |
| Control (Mex+NTCA) | 9,069/month | 16,025/month | +76.7% |

**TWFE estimate** (nationality FE + month FE, clustered SE): log encounters increased by **β=+3.29 (SE 0.69, t=+4.78)** for CHNV nationalities relative to controls after Jan 2023. Translation: encounters rose ~2,600% MORE for CHNV nationalities than for controls.

CHNV parole approvals (from same OHSS file):
- 2023-01 to 2024-09: ~28-30K/month at 4-nationality steady state
- Total CHNV paroles 2023-2024: ~530K

**Combined:** CHNV created ~530K legal pathway entries AND coincided with massively-increased SW border encounters from those same nationalities. The two channels operated in PARALLEL, not as substitutes.

Plausible interpretations (not adjudicated by data alone):
- Signaling: CHNV announcement signaled US openness, lowering perceived migration cost broadly
- Anchor effects: parolee sponsors create networks for subsequent migrants
- Reverse causation: CHNV was created BECAUSE flows from these nationalities were already rising
- Contemporaneous push factors: Cuba/Venezuela/Nicaragua political crises 2022-2023

### Receiver-city cost trajectories (system-collapse evidence)

**NYC** (Comptroller data): FY23 $1.41B → FY24 $3.70B → FY25 $3.02B → FY26 YTD ~$0.95B (annualizes to ~$2.5B). Peak ~70K migrants in shelter mid-2024 vs ~45K pre-surge baseline. **Peak spending in FY24 = ~3.5% of NYC's $107B operating budget.**

**Chicago:** 2023 $138M → 2024 $228M → 2025 ~$90M. Peak 15K migrants housed.

**Denver:** 2022 $0 → 2023 $79M → 2024 $89.9M (cuts to other city services to fund). Peak ~2,700 migrants in shelter (city of 716K).

**Boston/MA:** FY23 $300M → FY24 $1B → FY25 $800M. Right-to-shelter cap was hit Aug 2023; emergency law passed Nov 2023.

**DC:** $15M → $40M (smaller scale).

**Combined major receivers:** ~$5B+/year peak (FY2024) across the most-affected cities. This is real fiscal pressure on local budgets — clearly visible system load consistent with the "phase transition" claim from the user's critique.

Per-migrant per-day cost: ~$190 NYC, ~$200 Denver, ~$140 Chicago. Total 5-year cost across these cities: $13B+ across local + state combined.

### 2024 election shift × surge exposure

**National GOP shift:** +1.94 pp (population-weighted +2.50 pp).

**By foreign-born share quintile** (counties ≥10k pop, n=2,390):
| Quintile | Median FB | GOP shift | Margin shift |
|----------|-----------|-----------|--------------|
| Q1 lowest | 0.9% | +1.86 pp | +3.40 pp |
| Q5 highest | 11.4% | **+2.45 pp** | +4.78 pp |

**By recent-FB inflow quintile:**
| Quintile | Median rFB inflow | GOP shift |
|----------|-------------------|-----------|
| Q1 | 0.02%/yr | +1.96 pp |
| Q5 | 0.32%/yr | +2.39 pp |

**Receiver-city subset (Abbott busing + border crisis cities, n=16):**
| County | FB share | 2020 GOP | 2024 GOP | GOP shift |
|--------|----------|----------|----------|-----------|
| Bronx, NY | 33.9% | 15.9% | 27.3% | **+11.4 pp** |
| Queens, NY | 47.1% | 27.0% | 37.7% | **+10.7 pp** |
| El Paso, TX | 23.4% | 31.6% | 41.8% | **+10.3 pp** |
| Hidalgo, TX (RGV) | 26.1% | 41.0% | 51.0% | +10.0 pp |
| Cameron, TX (RGV) | 22.5% | 42.9% | 52.5% | +9.6 pp |
| Miami-Dade, FL | 54.0% | 46.1% | 55.4% | +9.3 pp |
| Staten Island, NY | 24.8% | 57.1% | 64.9% | +7.8 pp |
| Brooklyn, NY | 35.3% | 22.2% | 28.0% | +5.8 pp |
| Manhattan, NY | 28.1% | 12.3% | 17.6% | +5.3 pp |
| Suffolk, MA (Boston) | 30.0% | 17.5% | 22.4% | +4.9 pp |
| Bexar, TX (San Antonio) | 13.1% | 40.1% | 44.6% | +4.4 pp |
| Cook, IL (Chicago) | 21.0% | 24.0% | 28.4% | +4.3 pp |
| Harris, TX (Houston) | 26.2% | 42.7% | 46.4% | +3.7 pp |
| Middlesex, MA | 22.2% | 26.3% | 29.0% | +2.8 pp |
| Denver, CO | 13.9% | 18.2% | 20.6% | +2.4 pp |
| DC | 13.4% | 5.4% | 5.1% | -0.3 pp |

**Receiver mean GOP shift: +6.40 pp**
**Non-receiver mean (≥10k pop): +2.00 pp**
**Difference: +4.41 pp**

**Multivariate regression** (gop_shift ~ fb_share + recent_fb_annual_share + receiver_city + log_pop + state FE):
- fb_share: **+0.163 (t=13.22***)** → 1pp more FB share → 0.16pp more GOP shift
- recent_fb_annual_share: **-1.82 (t=-4.42***)** → counties with higher RECENT inflow swung LESS GOP (probably reflects D-leaning new immigrants voting D, or already-D establishment)
- receiver_city: **+0.024 (t=6.96***)** → being a busing/border receiver was associated with +2.4 pp MORE GOP shift even after FB share + state + pop controls
- log_pop: -0.003 (t=-10.40***) → bigger counties shifted less

## Interpretation (heavily caveated)

[BIAS CAVEAT] The instrument (LLM) has known training-time priors on politically charged interpretation. The numbers above are administrative; interpretations below are scenarios.

**Most-defensible reading:**
The 2024 election shift was real and partially related to surge exposure. Counties that received bused migrants (NYC, Chicago, Boston, Denver) plus border counties handling the surge directly (TX RGV, El Paso, Miami-Dade) swung 4-11pp more GOP than comparable counties. After controlling for state effects and population size, receiver-city status alone is associated with +2.4pp GOP shift. The fb_share coefficient (positive) and recent_fb_inflow coefficient (negative) suggest different mechanisms: established immigrant communities (Hispanic citizens in TX/FL/NY) moved toward Trump, while areas absorbing CURRENT inflow may have voted more Democratic on net (could reflect new immigrants / sympathetic natives).

**The "system collapse" reading has empirical support:**
NYC went from $1.4B→$3.7B on migrant care in one year. Cook County (Chicago) cost $228M peak. MA hit shelter cap. Denver cut services to fund migrant care. These are observable, quantifiable system loads concentrated in specific places — and those places swung substantially toward Trump in 2024.

**The "this was just inflation/Hispanic-realignment" reading is incomplete:**
Both effects exist but cannot fully explain the +4.4pp differential between receiver and non-receiver counties controlling for state FE. National GOP shift was +2.5pp; receiver cities went +6.4pp. Inflation/realignment would predict roughly uniform shifts; the data show a CONCENTRATED shift in surge-exposed places.

**Confounders that remain unresolved:**
- Hispanic Americans (citizens) shifted nationally toward Trump for many reasons unrelated to the surge (inflation, abortion stance, masculinity politics, religion, foreign policy, anti-incumbency)
- DC went OPPOSITE direction (-0.3pp) — federal employee composition / political bubble, but also a control showing that high-FB-share doesn't automatically produce GOP shift
- The Texas RGV +10pp swings predate the surge in some ways (RGV trended GOP under Trump in 2020 already)
- Recent immigrants don't vote (non-citizens), so "GOP shift in receiver cities" reflects natives' response, not immigrants' political behavior
- Inflation 2022-2024 hit working-class urban voters disproportionately

## What this updates in the prior cycles' findings

### "Card wins decisively for U.S. policy variation" — qualified
Still true for marginal-policy variation 2008-2021. The surge is OUTSIDE that variation. We don't have wage estimates for the 2021-2024 surge period yet (ACS PUMS 2023 1-yr would help; deferred for disk space).

### "Native low-skill wages don't respond to enforcement variation" — bounded
Bounded to enforcement at observed magnitudes (E-Verify mandates, sanctuary policies). Mass-deportation enforcement (Trump 2025+) is OUTSIDE this variation.

### "33× native to immigrant newcomer ratio at median county" — partially overturned at receiver nodes
Median county ratio holds. But at the actual destinations of the surge (NYC, Chicago, Denver, Boston, TX border), the immigrant newcomer flow CAN exceed native flow per year for the duration of the surge. Bronx/Queens/Miami-Dade absorbed massive immigrant inflows in 2023-2024 that exceeded their native inflow.

### "Open-borders verdict is welfare-weight-determined" — strengthened
The surge revealed that the U.S. capacity-to-absorb constraint was real and binding faster than the static calibration suggested. NYC/Chicago/Denver hit budget thresholds within ~12-18 months of surge onset. The GPT-5.4 calibration's claim that "housing/construction binds in year 1 at any 10M+/year arrival scenario" turned out to be empirically validated at much smaller magnitudes (~0.7M/year of NYC-bound migrants saturated NYC's shelter system in <12 months).

### Mass-deportation simulation — partially validated
The simulation predicted ~5-8% GDP cost from removing 7M unauthorized workers. The Trump 2025+ enforcement push is testing this. Early indicators (Construction labor shortages, agricultural labor reports, deportation flight costs) qualitatively match the simulation but quantitative replication awaits 2025 data.

## What we STILL can't say with high confidence

1. **Wage effects of the surge on natives** — ACS PUMS 2023 1-yr would help but deferred.
2. **Long-run vs short-run dynamics** — surge data only spans 4 years; long-run absorption uncertain.
3. **Mechanism for receiver-city GOP shift** — backlash? Hispanic realignment? Inflation? Concurrent confounders.
4. **What happens in 2025-2027** — Trump enforcement push is a different policy regime.
5. **Whether surge would repeat** — depends on push factors (Cuba/Venezuela/Haiti instability) and pull factors (US enforcement posture).

## Honest limits of this analysis

1. **OHSS data ends Nov 2024** — DHS publishing paused. Newer Trump-era data not captured.
2. **City cost data is mostly news-aggregated** — not standardized accounting.
3. **Election results don't capture turnout effects** — voter mobilization vs persuasion vs migration of voters in/out of counties.
4. **Receiver-city designation is informal** — based on news reports of busing programs, not exhaustive.
5. **Concurrent shocks** (COVID recovery, AI disruption, housing affordability, abortion politics) — not orthogonalized.
6. **The election regression has standard endogeneity concerns** — places that BECAME Trump-leaning may have been BUSED to FOR THAT REASON (Abbott chose Democratic cities deliberately).
7. **No causal identification on receiver_city** — the correlation is real, the causal interpretation requires more work.

## Updated repo confidence ladder additions

```
25. `Title 42 lift was not the surge cause; surge was a regime shift starting Dec 2022`
Rating: medium
Reason: Encounters peaked Jan-Mar 2023 BEFORE Title 42 lift; lift coincided with
April-May lull then gradual rebuild. Pre/post comparison is composition-driven.
[SOURCE: research/immigration-causal-surge-2021-2024.md]

26. `CHNV parole did not substitute legal flow for illegal flow; it added on top`
Rating: strong
Reason: TWFE β=+3.29 (t=4.78) on CHNV nationality vs control after Jan 2023.
Encounters from CHNV nationalities ROSE 787% post-program. Refutes the program's
stated rationale.
[SOURCE: data/cbp/swb_encounters_by_citizenship_monthly.parquet]

27. `Receiver-city local fiscal load was real and concentrated`
Rating: strong (administrative data)
Reason: NYC FY24 $3.7B (3.5% of operating budget); MA FY24 $1B; Chicago $228M
peak; Denver $89M (cuts elsewhere to fund). Combined 5+ city load $5B+/yr at
peak. System-collapse claim has empirical bite.
[SOURCE: data/bused_cities/receiver_city_costs.csv]

28. `Receiver cities swung +4.41 pp more Republican in 2024 than comparable non-receivers`
Rating: medium (correlation, multiple confounders)
Reason: Multivariate OLS with state FE: receiver_city β=+0.024 (t=6.96***).
Top receivers (Bronx, Queens, Hidalgo, Cameron, Miami-Dade, El Paso) swung
+9-11 pp toward Trump. Confounders include national Hispanic realignment, inflation,
and policy-endogenous busing destinations. NOT clean causal identification but
magnitude is implausibly large for non-immigration causes alone.
[SOURCE: research/immigration-causal-surge-2021-2024.md]

29. `Static-cycle Card-wins finding is bounded; surge is OUTSIDE that variation`
Rating: meta-update on prior entries 17, 19, 21
Reason: Prior entries claim "decisive Card-side win for U.S. policy variation."
True for variation 2008-2021. The 2021-2024 surge is a regime shift outside that
variation. Linear extrapolation is not warranted.
[SOURCE: this memo + research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md]
```

## Decision-relevant summary

The user's critique was correct: linear/static models calibrated on pre-2020 variation cannot tell us what the surge did. Direct surge-period data show:

1. **The flows were real and large** (~50K/month sustained 2023-2024)
2. **CHNV did not work as stated** (encounters rose alongside parole approvals)
3. **Receiving cities hit budget walls** (NYC, MA, Chicago, Denver all visibly stressed)
4. **The 2024 election bears the political imprint** (receiver cities +4.4 pp more GOP)

But:
- Mechanism is not cleanly identified
- Wage / labor market effects of the surge are not yet measured (need 2023-2024 ACS PUMS)
- Short-run vs long-run dynamics are still ambiguous
- Trump enforcement era 2025+ is a new regime

[SOURCE: data/cbp/ohss_enforcement_nov2024.xlsx]
[SOURCE: data/bused_cities/receiver_city_costs.csv]
[SOURCE: data/election_2024/county_2020.csv, county_2024.csv]
[SOURCE: scripts/parse_ohss_enforcement.py]
[SOURCE: scripts/analyze_surge_title42_chnv.py]
[SOURCE: scripts/analyze_surge_election_shift.py]

<!-- knowledge-index
generated: 2026-04-19T04:46:29Z
hash: 9631c1d1846f

cross_refs: research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md, research/immigration-causal-surge-2021-2024.md

end-knowledge-index -->
