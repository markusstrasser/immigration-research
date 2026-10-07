claude-opus-5-5

**Verdict:** The stall is not caused by early Texas lines. In the CPS, later vintages have not moved from G2 to G3+
faster than earlier ones, so nothing supports a much smaller carry-over for the descendants of post-1965 arrivals;
the closest analog sits at or slightly below the ladder's 0.84–0.86. Younger cohorts do show a lower ratio, but
because their second generation is further behind whites; their third-plus generation is no closer.
- **Texas.** Texas + New Mexico and California give about the same G2→G3+ ratio. In the ladder's frame (Census
  ASEC 2022–25, cohorts born 1980–2000) BA+ is 0.98 (SE 0.11) in Texas and 0.96 (0.06) in California, and the
  partial ledger 0.73 (0.13) and 0.96 (0.06), Texas the lower. Over 1994–2026, pooled across cohorts, Texas minus
  California is +0.02 to +0.06 (SE 0.03–0.04; z up to 2.0, on the rank gap), and −0.03 to +0.09 within the cohorts
  born after 1970. Only the rest of the country is clearly lower, at 0.76–0.88. [CALCULATION]
- **Cohort.** Within a birth cohort, G3+ is as far from whites as G2 or further for people born before 1970
  (ratios 1.08–1.36 on the schooling rank gap). For the 1970s cohort the BA+ ratio is about 1 (0.99–1.00). For
  those born 1980–2001 it is 0.87–0.96 on BA+, 0.75–0.90 on earnings and 0.81–0.84 on the ledger. [CALCULATION]
- **What moves is G2.** The G3+ schooling rank gap stays at −12.0 to −14.7 percentile points from the 1950s to
  the 1990–2001 cohort. G2 born in the 1960s, children of the small pre-1965 inflow, sat at −10.1; G2 born
  1970–2001, mostly children of post-1965 arrivals, sit at −12.7 to −15.1. [CALCULATION; INFERENCE for the vintage
  reading]
- **Spaced one generation apart.** Each comparison takes G2 of birth cohort c and G3+ born 30 years later. The
  earliest vintage took the largest step: 0.73–0.78 for G2 born in the 1930s, 0.84–0.90 for the 1940s, 1.06–1.07
  for the 1950s and 1.18–1.19 for the 1960s. [CALCULATION]
- **Post-1965 descendants.** Their G3 adults are almost unobservable before 2026. The closest observed case is the
  same-cohort ratio for people born 1980–2001: 0.87–0.96 on BA+ and 0.81–0.84 on the ledger among identifiers. With
  the ladder's identity correction (×0.937) that is about 0.82–0.90 on BA+ and 0.76–0.79 on the ledger, at or a
  little below the ladder's 0.84–0.86. [CALCULATION; the correction assumes c does not vary by cohort]
- **Lineage frame (parent and adult child in one household).** Selection dominates it for recent vintages, so it is
  reported as a failed diagnostic. Identity loss within it has no vintage trend: 12.5–17.4% of G3 children do not
  report Mexican origin, whatever the parent's birth decade. [CALCULATION]

[FRAMING-SENSITIVE: every gap is group minus third-plus non-Hispanic whites of the same stratum, age × sex matched;
vintage is never observed in the CPS and is proxied by birth cohort and state]

# Carry-over by arrival vintage (ladder 232 follow-up, 2026-10-07)

**Question.** Ladder 232 finds G2→G3+ carries 0.84–0.86 of the Mexican-origin gap after identity correction, and it
lists vintage as not excluded. Van Hook & Bachmeier (*Texas-Style Exclusion*, 2024; [literature
memo](../../../research/immigration-recent-papers-2026-10-06.md)) argue that slow progress comes mainly from early
Texas arrivals. In their account, later vintages close the high-school gap but not the bachelor's gap. Does the
carry-over differ for the descendants of later vintages?

**Steel-man for vintage.** Today's adult G3+ descend from pre-1965 migrants: many arrived before 1930, settled in
Texas and had little schooling (NLSY97 Tables 5, 15 and 16 in the carry-over lane). If those lines are unusually
slow, the cross-sectional ratio averages over the past and overstates the stall that post-1965 lines will
show. The test asks whether the carry-over is higher in Texas, higher for older cohorts and lower for
later-vintage pairs.

## Data and design

| Source | Frame | Outcomes | SE | Script |
|---|---|---|---|---|
| Census CPS ASEC public files 2022–25 (the ladder's) | adults 25–64; G2 = a Mexico-born parent; G3+ = US-born of US-born parents reporting Mexican origin | BA+, less than HS, employed, mean worker earnings, partial ledger | 160 SDR replicates | `census_asec.py` |
| IPUMS-CPS basic monthly, MIS 1 and 5, Jan 1994–Aug 2026 (pooled lane's extract 5) | same groups, adults 25–64 | BA+, schooling rank, less than HS, years, employed | bootstrap, 500 draws over 1,000 random groups of household clusters | `vintage.py`, `estimate.py` |
| IPUMS-CPS ASEC 1994–2026 (pooled lane's extract 4) | as monthly | + mean wage earnings (INCWAGE, 2024 $) | same | same |

- **Groups and weights.** Definitions, codes and weights are those of `generation_carryover_2026_09_27/analyze_cps.py`
  (Census) and `g3_identity_pooled_2026_10_05/analyze.py` (IPUMS), imported read-only.
- **Gaps.** Each gap is the group mean minus that of third-plus non-Hispanic whites of the same stratum, the whites
  reweighted to the group's age × sex cells. ρ = gap(G3+) / gap(G2).
- **Gates.**
  - The Census unsplit stratum reproduces the carry-over lane's ten published pop gaps and SEs to a relative 1e-9
    (median earnings is left out: the reduced build carries means only).
  - The IPUMS ASEC 2022–25 window gives ρ BA+ 0.916 (0.039), against the Census 0.921 (0.039). The random-group
    bootstrap SE matches the SDR SE.
  - The lineage frame's G3 children equal `analyze.py` `classify()`'s G3 lineage at 25+ in all 66 source-years.
- **Schooling rank gap (new measure).** This is the group's mean percentile rank in the age-matched white schooling
  distribution, minus 50 (ties at the mid-rank). A BA+ gap in points grows with the white BA+ share, which rose
  across these cohorts, so only the rank gap compares cohorts. Gate: whites ranked against themselves give 0.
- **Strata.**
  - Birth cohort (survey year minus age).
  - State group: Texas + New Mexico, California, elsewhere. Whites come from the same state group, and in a
    variant from the whole country.
  - Cohort × state, and cohort × survey period.
  - Lagged: G3+ of cohort c against G2 of cohort c − 30, each against its own cohort's whites.
- **Lineage.** Adults 25+ living with a linked parent, each matched to the parent's own record. ρ_lin is the
  children's gap over their parents' gap, against white child–white parent pairs of the same stratum, split by the
  parent's birth decade. Pairs whose parent is less than 14 years older are dropped: 124 g2g3 records in the monthly
  frame and 70 in the ASEC.
- **Counts.** n is the number of unique persons (CPSIDP) for IPUMS and person-years for Census, the lane's
  convention. Peak RSS: 0.87 GiB (`vintage.py`), 0.68 GiB (`estimate.py`), 1.77 GiB (`census_asec.py`; the
  imported loader's CSV read).

## 1. The ladder's frame by cohort and state (Census ASEC 2022–25)

ρ G2→G3+ (identifiers), SDR SE. n = person-years G2 / G3+ on BA+. [CALCULATION: `derived/census_rho.csv`]

| Stratum | n G2 / G3+ | BA+ | Less than HS | Mean earnings | Partial ledger |
|---|---|---|---|---|---|
| All (published) | 9,468 / 10,040 | 0.92 (0.04) | 0.85 (0.09) | 0.90 (0.07) | 0.90 (0.05) |
| Born 1958–69 | 980 / 1,834 | 1.45 (0.28) | 0.91 (0.22) | 1.54 (0.75) | 1.26 (0.29) |
| Born 1970–79 | 1,529 / 2,141 | 0.99 (0.10) | 0.73 (0.14) | 0.82 (0.11) | 0.92 (0.10) |
| Born 1980–89 | 2,558 / 2,814 | 0.87 (0.06) | 0.58 (0.11) | 0.75 (0.10) | 0.81 (0.08) |
| Born 1990–2000 | 4,401 / 3,251 | 0.88 (0.06) | 0.84 (0.18) | 0.82 (0.09) | 0.84 (0.08) |
| TX + NM | 2,012 / 3,409 | 1.06 (0.09) | 0.83 (0.12) | 1.03 (0.16) | 0.91 (0.10) |
| California | 3,668 / 2,462 | 0.97 (0.05) | 0.91 (0.15) | 1.00 (0.07) | 0.99 (0.05) |
| Elsewhere | 3,788 / 4,169 | 0.83 (0.06) | 0.78 (0.11) | 0.73 (0.09) | 0.76 (0.07) |
| Born 1958–79, TX + NM | 640 / 1,499 | 1.16 (0.14) | 0.85 (0.18) | 1.20 (0.33) | 1.09 (0.22) |
| Born 1958–79, CA | 924 / 945 | 1.02 (0.10) | 0.93 (0.20) | 0.97 (0.09) | 0.98 (0.08) |
| Born 1958–79, elsewhere | 945 / 1,531 | 1.04 (0.15) | 0.64 (0.13) | 0.63 (0.14) | 0.84 (0.18) |
| Born 1980–2000, TX + NM | 1,372 / 1,910 | 0.98 (0.11) | 0.67 (0.14) | 0.81 (0.14) | 0.73 (0.13) |
| Born 1980–2000, CA | 2,744 / 1,517 | 0.96 (0.06) | 0.73 (0.17) | 0.93 (0.08) | 0.96 (0.06) |
| Born 1980–2000, elsewhere | 2,843 / 2,638 | 0.78 (0.06) | 0.79 (0.16) | 0.77 (0.10) | 0.76 (0.08) |

- **Within each state group, younger cohorts carry over less.** Older cohorts run 1.02–1.16 on BA+ and younger
  ones 0.78–0.98.
- **Young Texans are not behind young Californians.** Within the 1980–2000 cohort, Texas + NM carries over about
  the same BA+ share as California and less of the ledger gap.
- **National whites as the reference change the state ratios by 0.04 or less** on BA+
  (`state_national_whites` rows).

## 2. Thirty-three years of cohorts (IPUMS-CPS 1994–2026)

Same-cohort ρ G2→G3+ (identifiers). Monthly frame; earnings from the ASEC frame. n = unique persons G2 / G3+.
The rank columns are the gaps in percentile points. [CALCULATION: `derived/xs_rho.csv`, `derived/xs_gaps.csv`]

| Born | n G2 / G3+ | Rank gap G2 | Rank gap G3+ | ρ BA+ | ρ rank | ρ less than HS | ρ years | ρ earnings (ASEC) |
|---|---|---|---|---|---|---|---|---|
| 1930–39 | 1,049 / 896 | −17.5 | −21.9 | 0.97 (0.11) | 1.25 (0.10) | 1.32 (0.11) | 1.13 (0.09) | 1.13 (0.26) |
| 1940–49 | 2,445 / 4,748 | −16.3 | −18.5 | 1.09 (0.06) | 1.13 (0.05) | 1.07 (0.06) | 1.09 (0.05) | 1.33 (0.20) |
| 1950–59 | 5,181 / 13,475 | −13.6 | −14.7 | 1.12 (0.05) | 1.08 (0.04) | 0.86 (0.04) | 0.96 (0.04) | 1.14 (0.14) |
| 1960–69 | 9,046 / 20,623 | −10.1 | −13.7 | 1.25 (0.04) | 1.36 (0.05) | 1.09 (0.05) | 1.21 (0.04) | 1.23 (0.10) |
| 1970–79 | 13,485 / 20,249 | −13.9 | −13.7 | 1.00 (0.03) | 0.99 (0.03) | 0.84 (0.04) | 0.94 (0.02) | 1.03 (0.06) |
| 1980–89 | 14,038 / 15,683 | −15.1 | −14.4 | 0.96 (0.02) | 0.96 (0.02) | 0.78 (0.04) | 0.93 (0.03) | 0.90 (0.06) |
| 1990–2001 | 9,527 / 7,864 | −12.7 | −12.0 | 0.93 (0.03) | 0.94 (0.04) | 0.74 (0.10) | 0.93 (0.04) | 0.83 (0.08) |
| Survey 2022–25 | 10,188 / 11,681 | −12.7 | −12.1 | 0.94 (0.03) | 0.95 (0.03) | 0.84 (0.07) | 0.94 (0.03) | 0.94 (0.07) |

- **Differences on the same draws.** On BA+, born 1990–2001 minus born 1950–59 is −0.19 (SE 0.06); on the rank
  gap, −0.14 (0.06). Texas + NM minus California is +0.04 (0.03) on BA+ and +0.06 (0.03) on rank; Texas + NM
  minus elsewhere is +0.12 (0.04) and +0.18 (0.04). [CALCULATION: `derived/xs_contrasts.csv`]
- **The ASEC frame agrees within 0.06 on every cohort ratio** on BA+ and rank, except BA+ for the 1930s cohort
  (1.11 vs 0.97, SE 0.11–0.14). The two frames share March households. (`xs_rho.csv`, source `asec`)
- **Young cohorts by state, on rank.** Born 1970–2001: Texas + NM 0.97–1.05, California 0.96–1.02, elsewhere
  0.86–0.88. [CALCULATION: `xs_rho.csv`, split `cohort_x_state`]
- **The cohort decline does not come from age or period.** Born 1980–89: 0.97 (0.03) measured in 2007–21, 0.93
  (0.05) in 2022–25. Born 1970–79: 0.97, 1.02 and 1.04 across the three periods to 2025. [CALCULATION:
  `cohort_x_period`]
- **The 1994–2026 pool's "all" row (BA+ 1.06) is not the ladder's estimand.** It mixes 33 years of cohorts against
  whites matched only on age × sex. The 2022–25 row is the comparable one.
- **The two high-school-gap patterns agree with Van Hook & Bachmeier.** For people born 1970–2001, G3+ closes more
  of the less-than-high-school gap (ρ 0.72–0.84) than of the BA+ gap (0.93–1.00). That is their description of
  later vintages. [CALCULATION]

**Why the ratio falls.** The rank gap of G3+ does not trend from the 1950s cohort on (−14.7, −13.7, −13.7, −14.4,
−12.0). G2's does: −13.6 and −10.1 for the 1950s and 1960s cohorts, then −13.9, −15.1 and −12.7. The low young-cohort
ratio is therefore a larger denominator: G2 born after 1970 are mostly children of post-1965 arrivals. [CALCULATION;
INFERENCE: the Mexico-born population grew from about 0.76M in 1970 to 2.2M in 1980 and 4.3M in 1990, so most G2
births after the mid-1970s are to post-1965 arrivals [TRAINING-DATA]]

## 3. Generation-spaced pairs: G2 of cohort c against G3+ of cohort c + 30

[CALCULATION: `xs_rho.csv`, split `lagged_30y`; monthly / ASEC]

| G2 born → G3+ born | Rank gap G2 → G3+ | ρ rank | ρ years | ρ BA+ points (biased upward) |
|---|---|---|---|---|
| 1930–39 → 1960–69 | −17.5 → −13.7 | 0.78 (0.05) / 0.73 (0.05) | 0.47 / 0.46 | 1.39 / 1.43 |
| 1940–49 → 1970–79 | −16.3 → −13.7 | 0.84 (0.04) / 0.90 (0.05) | 0.58 / 0.61 | 1.11 / 1.20 |
| 1950–59 → 1980–89 | −13.6 → −14.4 | 1.06 (0.04) / 1.07 (0.05) | 0.81 / 0.81 | 1.35 / 1.40 |
| 1960–69 → 1990–2001 | −10.1 → −12.0 | 1.19 (0.05) / 1.18 (0.07) | 0.98 / 0.96 | 1.41 / 1.44 |

- **The trend runs against the vintage story.** The earliest pairs took the largest step. Their G2 had parents who
  arrived before 1940, in the Texas-heavy era.
- **BA+ in points is biased upward.** It exceeds 1 because the white BA+ share rose between the two cohorts. The
  rank gap removes that.
- **Limit: G3+ born c are not all children of G2 born c − 30.** They include G4+ of older lines, and those G4+ pull
  every row toward the G3+ level. [INFERENCE]

## 4. Lineage frame: parent and adult child in one household (diagnostic, fails for recent vintages)

ρ_lin on the rank gap, monthly frame (ASEC in brackets). n = unique children. Children are counted whatever origin
they report. [CALCULATION: `derived/lineage_rho.csv`, `derived/lineage_gaps.csv`]

| Parent born | G1→G2 (n) | G2→G3 (n) | G3+→G4 (n) | G3 child rank gap |
|---|---|---|---|---|
| All | 0.12 (0.01) [0.13], 9,010 | 0.43 (0.04) [0.41], 2,995 | 0.68 (0.08) [0.53], 2,460 | −5.6 |
| 1900–39 | 0.21 (0.03) [0.21], 1,034 | 0.43 (0.04) [0.42], 1,123 | 0.30 (0.10) [0.14], 237 | −9.0 |
| 1940–49 | 0.12 (0.03) [0.14], 1,494 | 0.44 (0.10) [0.30], 680 | 0.46 (0.11) [0.29], 504 | −5.4 |
| 1950–59 | 0.14 (0.02) [0.15], 2,487 | 0.51 (0.12) [0.60], 591 | 0.72 (0.09) [0.72], 841 | −5.5 |
| 1960–69 | 0.10 (0.02) [0.11], 2,848 | −0.16 (0.83) [−0.04], 430 | 0.55 (0.17) [0.24], 640 | +1.2 |
| 1970+ | −0.10 (0.04) [−0.09], 1,291 | unstable, 205 | 0.35 (1.06) [0.07], 259 | +2.3 |

- **Selection fails the frame.** Adult children who still live with their parents are a selected group, and young
  co-resident whites are more negatively selected.
  - The G2 children's rank gap is −3.5 here, against −11.6 for all G2 adults (§2).
  - The gap turns positive for children of parents born 1970+ (+2.8), which no population estimate supports.
  - The ratios are far below the cross-section's on every step, and the frame cannot price levels.
- **No improvement for later vintages, inside the frame.** For parents born before 1960, where the frame still
  yields estimable ratios, G2→G3 runs 0.43, 0.44 and 0.51 (ASEC 0.42, 0.30 and 0.60). Texas + NM minus
  California is −0.03 (0.07). [CALCULATION: `derived/lineage_contrasts.csv`]
- **Identity loss has no vintage trend.** The share of G3 children not reporting Mexican origin, by parent decade,
  is 12.5%, 14.9%, 17.4%, 12.5% and 15.2% (SE 1.1–3.3). By state it is 9.0% in Texas + NM, 13.3% in California
  and 23.5% elsewhere. [CALCULATION: `derived/lineage_identity_shares.csv`]

## 5. Disconfirmation and what survives

| Prediction if the stall were early-vintage/Texas | Result |
|---|---|
| Texas carries over more of the gap than California | About equal: Texas minus California is +0.02 to +0.06 (SE 0.03–0.04) pooled, −0.03 to +0.09 within cohorts born after 1970; in young cohorts BA+ 0.98 vs 0.96 and ledger 0.73 vs 0.96 (Census), the ledger the other way |
| Older cohorts (more early-vintage G3+) stall, younger ones progress | Yes on the same-cohort ratio (≥1 before 1970, 0.87–0.99 after), but the change is in G2, not G3+ |
| Later-vintage generation pairs take a larger step | No: 0.73–0.78 for the earliest pair, 1.18–1.19 for the latest |
| Later-vintage G2 parents' children close more (lineage) | Not measurable for parents born after 1960 (selection); flat before |
| Identity loss differs by vintage, so the correction should differ | No trend across parent decades |

Two readings remain open:
- **Reading A.** The G3 of post-1965 lines lands where every G3+ cohort since the 1950s has landed, at −12 to −15
  rank points. Their ρ is then today's young-cohort value: 0.87–0.96 on BA+ and 0.81–0.84 on the ledger.
- **Reading B.** Post-1965 lines differ from all earlier lines in a way no observed cohort shows. Nothing in the CPS
  supports it.

A finer split cannot be made in public CPS data. The survey records no grandparent's arrival year, and the G3
adults whose grandparents arrived after 1965 are only now reaching 25. [INFERENCE]

## What this does and does not change

- **The account.** Unchanged. It prices the 2024 population, and none of this enters it.
- **Ladder 232.** The vintage caveat can be narrowed. Early Texas lines do not drive the stall; Texas and
  California carry over about the same share. The cohort pattern the ladder already reports (0.87 at 25–44) comes from a
  wider post-1965 G2 gap, not from younger G3+ being closer to whites.
- **The step for post-1965 descendants.** The best analog is the young-cohort ratio, identity-corrected at ×0.937:
  about 0.82–0.90 on BA+ and 0.76–0.79 on the ledger. That is at or slightly below 0.84–0.86, and on the dollar
  measures it means slightly faster closing than the pooled value.
- **FAQ 5.** The step to third-plus is not a forecast, and this lane does not make it one. Vintage, the main
  argument that today's G3+ understates future progress, finds no support. [INFERENCE]
- **Not done.** The projection (G4 −$6.3k, G5 −$6.4k) was not rerun at the young-cohort step. On the ledger the step
  would fall from ≈0.85 to ≈0.77, which moves the projection toward the regression band; the size is not computed.

## Limits

- **Proxies.** Vintage is never observed. Birth cohort and state stand in for it, and the mapping from G2 birth
  decade to grandparents' arrival is an inference.
- **G3+ composition.** G3+ mixes G3, G4 and G5+. Every split compares a G2 vintage with a mix of G3+ vintages.
- **Identity.** Identifiers only, the published convention. Identity loss (11–17%) is corrected by one factor, on the
  assumption that the closing share c does not differ by cohort. The HISPAN question changed in 2003.
- **Lineage frame.** Selection dominates it (§4). The minimum parent–child age gap (14 years) is a choice.
- **SEs.**
  - Cross-cohort comparisons on the BA+ and years scales are not scale-free; the rank gap is.
  - IPUMS SEs come from an unstratified random-group bootstrap (K = 1,000). They match the SDR SE where both
    exist (0.039 vs 0.039).
  - Census n are person-years; adjacent ASECs share households.
- **Peak memory.** `census_asec.py` peaks at 1.77 GiB, under the 2 GiB limit; the carry-over lane's own build peaks
  at 3 GiB.

## Reproduce

From the repository root, in order (`stage.py` reads the pooled lane's `_cache/` extracts; `census_asec.py` reads the
Census zips the carry-over lane names):

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/carryover_vintage_2026_10_07/stage.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/carryover_vintage_2026_10_07/vintage.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/carryover_vintage_2026_10_07/estimate.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/carryover_vintage_2026_10_07/census_asec.py
```

Outputs in `derived/`: `stage_audit.json`, `aggregate_audit.json`, `xs_gaps.csv`, `xs_rho.csv`, `xs_contrasts.csv`,
`lineage_gaps.csv`, `lineage_rho.csv`, `lineage_contrasts.csv`, `lineage_identity_shares.csv`, `census_gaps.csv`,
`census_rho.csv`, `census_audit.json`. `_cache/` (staged parquet, aggregates) is ignored.

## Log
- 2026-10-07 10:44 JST — lane created; reading ladder 232 lanes.
- 2026-10-07 10:51 JST (from `date`) — read ladder 232 and the three lanes (generation_carryover, carryover_identity, g3_identity_pooled). Plan: (A) Census ASEC 2022–25, the ladder's own frame and outcome set incl. the partial ledger, ρ G2→G3+ split by birth cohort and by TX+NM / CA / elsewhere, SDR SEs; (B) IPUMS-CPS monthly (MIS 1/5) and ASEC 1994–2026 from the pooled lane's caches: the same cross-sectional ρ by birth cohort and state over a 33-year window, plus a co-resident parent–child lineage ratio split by the parent's birth cohort (G1→G2, G2→G3, G3+→G4).
- 2026-10-07 10:51 JST (from `date`; run finished just before) — stage.py: both IPUMS extracts staged to parquet (5,856,362 ASEC and 11,990,720 monthly rows; 10.6 s, peak RSS 304 MiB).
- 2026-10-07 11:03 JST (from `date`) — vintage.py and estimate.py run. The in-memory running totals peaked at 2.1 GiB,
  so they were replaced by yearly part files that DuckDB sums (0.87 GiB). The rank gap was added after the BA+ point
  gaps proved scale-biased across cohorts (lagged BA+ ratios above 1 while years and rank fell).
- 2026-10-07 11:05 JST (from `date`) — census_asec.py: the carry-over lane's build() peaked at 3.07 GiB, so the
  script was rewritten to reduce each year to cell × replicate totals (1.77 GiB). The gate reproduces 10 published
  cells.
- 2026-10-07 11:07 JST (from `date`) — results tabulated; RESULT written; rerun check next.
- 2026-10-07 11:13 JST (from `date`) — RESULT claims re-checked against the CSVs (Texas wording softened to
  "about the same", ranges corrected); `scripts/rerun_lane.py` with the four commands: IDENTICAL 18/18, exit 0.
