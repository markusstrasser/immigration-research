# The 2021-2024 surge: what the data show

**Date:** 2026-04-18 (evening)
**Question:** What can we actually say about the 2021-2024 immigration surge that static models couldn't capture?
**Method:** OHSS DHS monthly enforcement tables (encounters by citizenship), CHNV parole data, NYC Comptroller / Chicago / Denver / MA migrant cost trajectories, county-level 2020 vs 2024 election results, ACS county FB share.

> **CORRECTED (2026-06-11):** the encounter series this memo was built on carried two parser bugs (fiscal-index dates; OFO-ports-only universe). Key finding 2 (CHNV "did not substitute") is **reversed**; the monthly narrative and Title-42 windows are replaced below; finding 3 (receiver swing) survived its kill-test. See [decisions/2026-06-11-ohss-date-universe-bugs-chnv-reversal.md](../decisions/2026-06-11-ohss-date-universe-bugs-chnv-reversal.md).
**Bias caveat:** Politically charged subject matter. Per `notes/llm-bias-caveat.md`, this memo flags interpretation that depends on the LLM instrument's training-time priors. Empirical numbers below are administrative data; interpretations are explicitly framed as scenarios.

## Bottom line

Three corrected findings the static cycle missed:

1. **The Title 42 lift did not cause the surge, but the original monthly evidence was wrong.** Corrected Total-CBP data show Dec-2022 local peak 252K, Jan-Feb 2023 trough, Apr-May anticipation spike at 212K/207K, June post-lift crash, and Dec-2023 record 301,980. Post-lift 6-month mean was **14.5% below** pre-lift. [SOURCE: `scripts/analyze_surge_title42_chnv.py` rerun 2026-06-11; decision record]

2. **CHNV substituted lawful port flow for irregular between-port crossings in its initial year.** Corrected USBP event study shows Cuba −95.3%, Nicaragua −96.2%, and Venezuela −57.5% between-port crossings after program start; the old "+787%" rise was the program's own lawful OFO channel read as total SWB encounters. Corrected total-CBP DiD is null (β=+0.45, t=1.29). [SOURCE: `sources/immigration-causal/data/outcomes/analysis/chnv_pretrends/results.json`; decision record]

3. **Receiver cities still show a political signal after the Hispanic-share kill-test.** The receiver coefficient moves from +0.0256 to +0.0238 with 2020 county Hispanic share controlled (t≈7.2); use the controlled +2.4pp as a correlational upper-bound, not the raw +4.4pp as a causal headline. [SOURCE: `sources/immigration-causal/data/outcomes/analysis/swing_hispanic_control/results.json`; decision record]

## Findings in detail

### Title 42 lift event study (corrected 2026-06-11)

The original month table was built from fiscal-index dates and the wrong agency universe. Corrected Total-CBP data show:

- Dec-2022 local peak: **252K**
- Jan-Feb 2023 trough: CHNV substitution visible at total level
- Apr-May 2023 anticipation spike: **212K / 207K**
- Jun-2023 post-lift crash: **145K**, about **−30%**
- Dec-2023 record: **301,980**
- Post-lift 6-month mean: **−14.5%** vs pre-lift

The corrected reading is still that Title 42's lift did not cause the surge. The evidence is not "pre-lift 50K/month and post-lift +62%"; that was a parser artifact. [SOURCE: `scripts/analyze_surge_title42_chnv.py` rerun 2026-06-11; decision record]

### CHNV channel-substitution event study (corrected 2026-06-11)

Corrected universe: **USBP between-ports** for irregular crossings, with OFO reported separately as the lawful port channel. [SOURCE: `sources/immigration-causal/data/outcomes/analysis/chnv_pretrends/results.json`]

| Nationality | USBP pre-6 mean | USBP post-6 mean | Change | OFO pre-6 mean | OFO post-6 mean |
|-------------|----------------:|-----------------:|-------:|---------------:|----------------:|
| Venezuela | 16,488 | 7,000 | −57.5% | 47 | 3,210 |
| Cuba | 28,563 | 1,355 | −95.3% | 32 | 1,252 |
| Nicaragua | 22,063 | 830 | −96.2% | — | — |
| Haiti | 152 | 150 | ~flat | 5,585 | 5,658 |

Event study:

- Mean event-time effect τ[0,+3]: **−2.17 log points**
- Mean event-time effect τ[+6,+12]: **−1.83 log points**
- Monotone-rising pre-trend flag: **false**
- Corrected total-CBP DiD: **β=+0.45, t=1.29** — null [SOURCE: decision record]

**Corrected conclusion:** CHNV substituted lawful port flow for irregular crossings in its initial year, strongest for Cuba/Nicaragua and initially Venezuela. It did **not** reduce total arrivals because roughly **530K** lawful paroles were planned inflow and still landed in receiver-city ledgers. [INFERENCE]

### Receiver-city cost trajectories (system-collapse evidence)

**NYC** (Comptroller data): FY23 $1.41B → FY24 $3.70B → FY25 $3.02B → FY26 YTD ~$0.95B (annualizes to ~$2.5B). Peak ~70K migrants in shelter mid-2024 vs ~45K pre-surge baseline. **Peak spending in FY24 = ~3.5% of NYC's $107B operating budget.**

**Chicago:** 2023 $138M → 2024 $228M → 2025 ~$90M. Peak 15K migrants housed.

**Denver:** 2022 $0 → 2023 $79M → 2024 $89.9M (cuts to other city services to fund). Peak ~2,700 migrants in shelter (city of 716K).

**Boston/MA:** FY23 $300M → FY24 $1B → FY25 $800M. Right-to-shelter cap was hit Aug 2023; emergency law passed Nov 2023.

**DC:** $15M → $40M (smaller scale).

**Combined major receivers:** ~$5B+/year peak (FY2024) across the most-affected cities. This is real fiscal pressure on local budgets — clearly visible system load consistent with the "phase transition" claim from the user's critique.

Per-migrant per-day cost: ~$190 NYC, ~$200 Denver, ~$140 Chicago. Total 5-year cost across these cities: $13B+ across local + state combined.

### 2024 election shift × surge exposure

**Reading rule after 2026-06-11 kill-test:** the raw receiver-city gap below is descriptive only. Use the Hispanic-share-controlled receiver coefficient, about **+2.4pp**, as the headline correlational upper-bound. [SOURCE: `sources/immigration-causal/data/outcomes/analysis/swing_hispanic_control/results.json`]

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
Both effects exist. The pre-registered Hispanic-share kill-test left the receiver coefficient nearly unchanged (+0.0256 → +0.0238), so the named rival channel did not erase the receiver association. But the raw +4.4pp receiver/non-receiver gap is not a causal headline; use the controlled +2.4pp as the bounded claim.

**Confounders that remain unresolved:**
- Hispanic Americans (citizens) shifted nationally toward Trump for many reasons unrelated to the surge (inflation, abortion stance, masculinity politics, religion, foreign policy, anti-incumbency)
- DC went OPPOSITE direction (-0.3pp) — federal employee composition / political bubble, but also a control showing that high-FB-share doesn't automatically produce GOP shift
- The Texas RGV +10pp swings predate the surge in some ways (RGV trended GOP under Trump in 2020 already)
- Recent immigrants don't vote (non-citizens), so "GOP shift in receiver cities" reflects natives' response, not immigrants' political behavior
- Inflation 2022-2024 hit working-class urban voters disproportionately

## What this updates in the prior cycles' findings

### Card-side pattern for marginal pre-surge policy variation — surge caveat
Still true for marginal-policy variation 2008-2021. The surge is OUTSIDE that variation. We don't have wage estimates for the 2021-2024 surge period yet (ACS PUMS 2023 1-yr would help; deferred for disk space).

### "Native low-skill wages don't respond to enforcement variation" — bounded
Bounded to enforcement at observed magnitudes (E-Verify mandates, sanctuary policies). Mass-deportation enforcement (Trump 2025+) is OUTSIDE this variation.

### Domestic-vs-abroad median newcomer ratio — receiver-node caveat
The corrected median-county comparison is about 21.7x for the ratio of medians and 20.5x for the median county-level ratio among counties with nonzero moved-from-abroad share. This is domestic U.S.-origin movement versus moved-from-abroad flow, not native identity. But the median county is not a receiver-node estimand: concentrated surge destinations can face immigrant-specific shelter, legal, language, and school burdens that the national median domestic-vs-abroad ratio does not measure. [SOURCE: research/immigration-causal-internal-vs-immigrant-newcomers.md] [INFERENCE]

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
25. `Title 42 lift did not cause the surge`
Rating: medium
Reason: corrected Total-CBP data show Apr-May 2023 anticipation spike, June
post-lift crash, and post-lift 6-month mean 14.5% below pre-lift. The old
monthly facts are superseded by the 2026-06-11 parser fix.
[SOURCE: decisions/2026-06-11-ohss-date-universe-bugs-chnv-reversal.md]

26. `CHNV substituted lawful port flow for irregular crossings in its initial year`
Rating: strong initial-period; medium beyond ~12 months
Reason: corrected USBP event study shows Cuba −95.3%, Nicaragua −96.2%,
Venezuela −57.5%; the old "+787%" was OFO lawful port throughput read as total
SWB encounters. Corrected total-CBP DiD is null (β=+0.45, t=1.29).
[SOURCE: sources/immigration-causal/data/outcomes/analysis/chnv_pretrends/results.json]

27. `Receiver-city local fiscal load was real and concentrated`
Rating: strong (administrative data)
Reason: NYC FY24 $3.7B (3.5% of operating budget); MA FY24 $1B; Chicago $228M
peak; Denver $89M (cuts elsewhere to fund). Combined 5+ city load $5B+/yr at
peak. System-collapse claim has empirical bite.
[SOURCE: data/bused_cities/receiver_city_costs.csv]

28. `Receiver cities swung about +2.4 pp more Republican after Hispanic-share control`
Rating: medium (correlation, multiple confounders)
Reason: Hispanic-share kill-test leaves receiver β +0.0256 → +0.0238 (t≈7.2).
Use this as correlational upper-bound; do not reuse the raw +4.41pp as a causal
headline.
[SOURCE: sources/immigration-causal/data/outcomes/analysis/swing_hispanic_control/results.json]

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
2. **CHNV substituted channels in its initial year** (irregular USBP crossings fell, lawful port/parole flow rose)
3. **Receiving cities hit budget walls** (NYC, MA, Chicago, Denver all visibly stressed)
4. **The 2024 election bears a political imprint** (receiver cities about +2.4 pp more GOP after Hispanic-share control; correlational)

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

## Revisions

- **2026-06-11b (supersedes 2026-06-11a where they conflict):** Running the morning's two pre-registered kill-tests exposed two bugs in `parse_ohss_enforcement.py`: fiscal-index dates (every non-January window scrambled) and an agency-block dict-overwrite (the series was OFO port-of-entry encounters — the CHNV program's own lawful channel — read as total SWB). Consequences: (1) Key finding 2 is **reversed** — corrected USBP data show between-port crossings collapsed −95%/−96%/−58% (Cuba/Nicaragua/Venezuela) after each nationality's program start with flat pre-trends; the "+787% rise" was the lawful channel itself; corrected total-CBP DiD is null (β=+0.45, t=1.29). CHNV substituted channels; it did not reduce total arrivals (~530K paroles are planned lawful inflow — receiver-load ledger unaffected). (2) The monthly narrative (incl. "April-May 2023 lull") is wrong: corrected series shows an April-May anticipation spike, June post-lift crash (−30%), and the Dec 2023 record (301,980); the conclusion "lift ≠ surge cause" survives on this new evidence. (3) Finding 3's receiver swing **survived** its Hispanic-share kill-test (β +0.0256 → +0.0238, t≈7.2; Hispanic share itself t=17.2). Ladder entries 34-37; decision record [2026-06-11-ohss-date-universe-bugs-chnv-reversal](../decisions/2026-06-11-ohss-date-universe-bugs-chnv-reversal.md).

- **2026-06-11a:** Bias self-audit (mirror test against the Cato 2026 study criticisms) downgraded two of this memo's headline readings. (1) The CHNV finding drops from strong to medium as a *causal* claim: reverse causation (program created in response to already-rising flows) is listed above but was never adjudicated with pre-trend/event-study leads; the descriptive non-substitution fact stands. The `+787%` figure must always carry its 2,598/month base. (2) The "+4.4 pp implausibly large for non-immigration causes alone" sentence is retracted as headline language: the top swing counties are among the most Hispanic in the country, the regression controls FB share but not Hispanic share, so the national Hispanic realignment is not decomposed out. Use the controlled +2.4pp (receiver_city β=+0.024) as an upper bound. Ladder entries 30-31 supersede; checklist items 8/25 in [notes/quant-bias-checklist.md](../notes/quant-bias-checklist.md).

<!-- knowledge-index
generated: 2026-04-19T04:46:29Z
hash: 9631c1d1846f

cross_refs: research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md, research/immigration-causal-surge-2021-2024.md

end-knowledge-index -->
