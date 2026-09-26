# Housing supply, Mexican-origin demand and rents — California against Texas

**Verdict:** "California is not building, only Texas is" is true as a rate and false as a
rate relative to population growth. Texas authorised 2.2 to 2.5 times as many housing units
per resident as California on average over 2000–2024, and California sat below the national
rate in every one of the 25 years. But over 2010–2024 California's housing stock grew faster
than its population (1.77 added people per added unit against 2.31 in Texas), because its
population barely grew. The same demand shift moves rents about 2.0 to 2.5 times more in
coastal California than in Houston on published supply elasticities, which is why an equal
Mexican-origin share can carry unequal rent effects. Across the 152 of 168 metros with a 2015 rent value, those whose
Mexican-origin share rose more in 2010–2023 had higher rent growth in 2015–2026 (about 0.03
log points per percentage point within state), but the "amplified where supply is inelastic"
interaction is not separately identified in this cross-section. In 2024 native non-Hispanic
white adults left California on net at 11.7 per 1,000, steeper without a degree (14.8 against
8.9), while Texas was flat. Everything here is descriptive; no causal claim is made, because
the instruments for Mexican inflows are dead after 2005 (ladder 136).

September 22, 2026. Frame: the operator's question of how to model housing shocks from a
population that is about 32% Mexican-origin in both states, and what "California is not
building" means in numbers. Executed in
[`housing_supply_ca_tx_2026_09_22`](../infra/immigration-fiscal/housing_supply_ca_tx_2026_09_22/RESULT.md)
from primary sources (Census Building Permits Survey, population estimates, ACS tables and
2024 PUMS, Zillow ZORI, Saiz 2010 elasticities). Confidence ladder entry 180. The parent
reproduced the FRED permit sums, the state-fixed-effects regression and the PUMS migration
flows independently before writing this memo; all three matched.

## 1. Three objects, not one

A question about "the effect of the Mexican-origin population on rents" mixes three things
that the evidence treats differently.

- **A flow effect.** An inflow of 1% of a metro's population raises rents about 1% on Saiz
  (2007), up to 2.2% for rents and 3.8% for prices on Cabral and Steingress (2026), measured
  on ten-year inflows of a few percent
  ([housing lane of September 16](../infra/immigration-fiscal/housing_deport_2026_09_16/RESULT.md)).
- **A stock counterfactual.** "32% of the state is Mexican-origin, what did it do to rents" is
  outside that support. Over decades supply adjusts to the population, so the answer depends
  on the long-run elasticity, near zero for an elastic market and large for a constrained
  one. Any number for it is modelled with every input assumed except the shares.
- **A same-shift, different-response comparison.** With demand shift d, supply elasticity
  ε_S and demand elasticity ε_D, the rent response is d ÷ (ε_S + ε_D). This is arithmetic on
  published elasticities and is the one piece that can be stated now (§3).

## 2. Supply: permits, stock and population

`[SOURCE: Census BPS state files 2000–2024; Census population estimates; ACS 1-year B25001]`
`[CALCULATION: derived/state_supply.csv, derived/state_growth_2010_2024.csv]`

Permits per 1,000 residents, period means:

| Period | California | Texas | United States | TX ÷ CA |
|---|---|---|---|---|
| 2000–2007 | 4.64 | 7.81 | 6.07 | 1.68 |
| 2008–2011 | 1.24 | 3.93 | 2.17 | 3.17 |
| 2012–2019 | 2.42 | 6.07 | 3.55 | 2.51 |
| 2020–2024 | 2.81 | 7.98 | 4.65 | 2.84 |
| 2000–2024 | 3.02 | 6.67 | 4.36 | 2.21 |

The year-by-year ratio averages 2.46 and runs from 1.37 (2004) to 3.66 (2009). Per 1,000
existing units the picture is the same: 7.5 in California against 18.4 in Texas in 2023, with
the United States at 10.0. Over the whole window Texas authorised 4.34 million units to
California's 2.80 million from a population averaging 69% of California's.

Against population growth the claim inverts:

| 2010–2024 | Population growth | Housing-unit growth | Added people per added unit |
|---|---|---|---|
| California | +5.66% | +8.73% | 1.77 |
| Texas | +23.96% | +26.22% | 2.31 |
| United States | +9.95% | +11.19% | 2.06 |

California added housing faster than it added people. The arithmetic reason is the first
column: its population grew 5.7% in fourteen years, Texas's 24%. `[FRAMING-SENSITIVE]` Which
framing is "the" supply story is a judgment: rates per resident favour the Texas-builds
reading, rates per unit of population growth do not, and a market with high prices and low
population growth is consistent with both constrained supply and demand rationed by price.
Permits are authorisations, not completions, and the December year-to-date product differs
from the as-published monthly series by −1.7% to +3.1%; the parser is gated on the monthly
files, which reproduce FRED to the unit.

## 3. Same demand shift, different rent response

`[DATA: Saiz 2010 elasticities, local file; ε_D assumed]` `[CALCULATION: derived/mechanical_response.csv]`

| Metro | Saiz ε_S | Response to a 1% demand shift, ε_D = 0.7 | Ratio to Houston |
|---|---|---|---|
| Los Angeles | 0.63 | 0.75% | 2.26 |
| San Francisco | 0.66 | 0.73% | 2.20 |
| San Diego | 0.67 | 0.73% | 2.19 |
| Riverside | 0.94 | 0.61% | 1.83 |
| Dallas | 2.18 | 0.35% | 1.04 |
| Houston | 2.30 | 0.33% | 1.00 |
| San Antonio | 2.98 | 0.27% | 0.82 |
| Austin | 3.00 | 0.27% | 0.81 |

At ε_D between 0.5 and 1.0 the coastal-California-to-Houston ratio runs 2.0 to 2.5 and
narrows as the assumed demand elasticity rises. This is a single-market competitive
calculation on elasticities estimated on 1970–2000 land and regulation data, not an estimate
of any actual rent change. It says how much more the same Mexican-origin demand shift would
move rents in Los Angeles than in Houston before any building responds, which is the
mechanism behind an equal share carrying an unequal price effect.

## 4. The metro cross-section, 168 metros

`[DATA: ACS 5-year B03001 by CBSA, 2010 and 2023; Zillow ZORI 2015-01 to 2026-05; Saiz elasticities]`
`[CALCULATION: derived/metro_panel.csv, derived/metro_regressions.csv]`

California's 19 metros: elasticity 1.45, Mexican-origin share +3.75 points 2010–2023, rent
growth 0.60 log points. Texas's 13: elasticity 2.99, +1.88 points, 0.44 log points. All 168:
2.30, +1.30, 0.56. Rent growth by elasticity quartile shows almost no gradient (0.56, 0.58,
0.57, 0.53 from least to most elastic).

Descriptive regressions of rent growth on the share change, heteroskedasticity-robust
standard errors, no instrument:

| Specification | Δ share (per pp) | Δ share × 1/ε | n |
|---|---|---|---|
| share only | +0.016 (0.005) | | 152 |
| share, state fixed effects | **+0.030 (0.007)** | | 152 |
| product with main effects, state FE | | −0.007 (0.017) | 152 |
| annualised, all metros, state FE | +0.0025 (0.0007) per year | | 168 |
| annualised product, all metros | | +0.0018 (0.0015) per year | 168 |

Within a state, a metro whose Mexican-origin share rose one point more had about 0.03 log
points more rent growth over eleven years. The interaction with inverse elasticity is
significant only as a bare product, which is nearly collinear with the share change, and is
indistinguishable from zero once main effects are present. `[INFERENCE]` On this
cross-section the amplification-where-inelastic pattern is not separately identified; that is
a statement about 168 observations and a names-only metro crosswalk, not evidence that the
amplification is absent. The share change is not exogenous: people move to where rents and
jobs are, so the coefficient carries reverse causation and omitted demand.

## 5. Native sorting, one year

`[DATA: ACS 2024 1-year PUMS, MIGSP, 80 replicate weights]` `[CALCULATION: derived/native_migration_2024.csv]`

Native-born adults 25–64, net interstate migration per 1,000 resident natives of the same
group, standard errors in parentheses:

| | NH white, all | NH white, BA+ | NH white, no BA | All natives |
|---|---|---|---|---|
| California | −11.73 (1.35) | −8.85 (1.82) | −14.75 (1.70) | −8.46 (0.76) |
| Texas | +0.20 (1.24) | −1.41 (1.87) | +1.53 (1.39) | +2.35 (0.98) |

California's net loss of native non-Hispanic white adults is large against its standard error
in every education group and steeper without a degree, a 5.9 per 1,000 difference that exceeds
the sum of the two standard errors. Texas is flat for that group and gains natives overall.
This is one year of gross flows with a one-year lookback; it counts moves, not motives. It is
consistent with the Ganong–Shoag mechanism, non-degree natives no longer moving toward
high-wage, high-rent places, and with the AGI outflow the
[Tiebout memo](immigration-native-sorting-tiebout-2026-09-18.md) measured (ladder 139), but it
does not attribute the moves to rents, to the Mexican-origin population or to anything else. §8 reads the movers' stated reasons.

## 6. How to model it, and what cannot be modelled with what we hold

Three layers, in order of what the data can bear:

1. **Accounting (done here).** Supply rates, stock against population, the mechanical response
   at published elasticities, and the descriptive metro association. Adds a sorting cut from
   the PUMS. Says nothing causal.
2. **Reduced form with an instrument (not done).** Change in log rent on the change in
   Mexican-born share, instrumented with settlement shares times the national inflow,
   interacted with elasticity, with native net migration by education as a second outcome.
   Ladder 136 found both standard instruments lose their variation after 2005, and the
   pre-1990 shift-share is alive only on 2000–2010 (ladder 140, F of 16 to 29). The honest
   version is therefore a 2000–2010 metro panel on Census 2000 and ACS 2010 rents, and its
   estimate would be about that decade. Wilson and Zhou's 2021–2024 design needs an
   administrative unauthorized-inflow measure the repo does not hold.
3. **Structural counterfactual (not done, and would be modelled).** Removing 32% of the
   population from a long-run market needs a long-run elasticity, a demand elasticity, a
   household-formation rate for the group and an assumption about what the vacated stock
   does. Every input but the share is assumed; the output would be a range labelled as such.

The repo's existing warehouse panels say the same thing descriptively: the foreign-born share
correlates +0.69 with rent levels and −0.17 with 2016–2025 rent growth across the same metros
([MSA rent panel](immigration-msa-rent-elasticity-panel-2026-06-25.md)), immigrants live in the
expensive inelastic metros and the recent growth was not where they are.

## 7. Disconfirmation and limits

- The strongest case for "California is not building" survives: below the national permit
  rate in 25 of 25 years, at 45% of the Texas rate.
- The strongest case against it, on these numbers: its stock outgrew its population over
  2010–2024. A reader who takes population as exogenous reads that as adequate building; a
  reader who takes population as rationed by price reads it as the symptom. The data do not
  pick.
- The metro association could be entirely reverse causation. Nothing here rules that out.
- Saiz elasticities are fixed at their 1970–2000 estimates; the crosswalk is names-only; 2010
  and 2023 CBSA geographies differ for some metros; the 2010 and 2023 ACS values are
  five-year averages.
- 16 of 168 metros lack a January 2015 rent value and are more elastic (3.10 against 2.21);
  the annualised specifications on all 168 reproduce the sign and pattern.
- The migration table is 2024 alone. One year does not show a trend, and the 2024 ACS
  reference period sits after the 2021–2024 inflow.
- Housing remains unpriced in the fiscal account in both directions (FAQ 4). Nothing here
  changes the $165–197bn figure or is meant to be added to it.

**Instrument note.** Built by a worker agent from a written brief and graded here against
three independent re-derivations; the judgment calls (reporting the population-relative
supply comparison beside the rate comparison, and reporting the interaction as not identified
rather than leaning on the one specification where the bare product is significant) are the
lane's and this model's, and a reader should check the tables rather than the prose
(`notes/llm-bias-caveat.md`).

## 8. Why US-born adults leave California: stated reasons (2026-09-25)

`[DATA: IPUMS-CPS ASEC 1999–2025, WHYMOVE, 160 replicate weights; IRS SOI state and county migration files 2011–12 to 2022–23]`
`[CALCULATION: [movers lane](../infra/immigration-fiscal/movers_reasons_2026_09_24/RESULT.md), ladder 221]`

§5 counts moves. The CPS also asks each mover for one main reason. Among US-born adults who left
California, ASEC 2005–2025 (n = 3,586), shares in %, SE in points:

| Main reason | California leavers | Leavers of all other states | California minus others |
|---|---|---|---|
| Jobs | 38.11 (1.29) | 40.41 (0.47) | −2.30 (1.34) |
| Family | 27.22 (1.26) | 26.37 (0.39) | |
| Housing | 18.98 (1.19) | 14.70 (0.32) | +4.28 (1.24) |
| of which cheaper housing | 7.73 (0.79) | 3.51 (0.17) | +4.22 (0.83) |
| Better neighborhood/less crime | 1.47 (0.25) | 1.90 (0.12) | −0.43 (0.26) |
| Climate | 0.90 (0.20) | 2.39 (0.15) | −1.49 (0.24) |

The neighborhood/crime answer is the only one that could carry a composition motive, and the
Census category mixes crime, schools, disorder and neighbors. About 4,200 US-born adults a year
give it at the CPS level, 3,600–7,000 at the ACS level (the CPS finds 0.62–0.87 of the ACS count
of California leavers), or 0.2–0.3 per 1,000 US-born adults living in California. Against §5's
net loss of 11.73 per 1,000 native non-Hispanic white adults, that is small, but the two are not
comparable as a ratio: one is a net rate for one group, the other a gross rate for one reason.

The test that could have favored a composition reading does not. California's non-Hispanic white
leavers and its US-born Mexican-origin leavers differ from other states' leavers by the same
amount on neighborhood/crime (−0.17, SE 0.35, and −0.14, SE 0.89), and both show the housing
excess, larger for Mexican-origin (+6.2) and Black (+8.3) leavers than for white ones (+3.1).
Across origin states the neighborhood/crime share falls as the origin's Mexican-origin share
rises (−0.28 to −0.36 points per 10 points, t −2.8 to −3.6). The same design detects both
positive controls (origin rent predicts cheaper-housing moves, t 4.3; a cold origin predicts
climate moves, t 5.1), so the null-or-negative gradient is informative about stated reasons; it
weakens for whites alone and without California, and within a state over time it cannot be
estimated precisely.

**The Texas flow.** California-to-Texas tax filers had lower AGI per return than California
stayers from 2011–12 to 2018–19 (0.82–0.96 times), higher in 2019–20 to 2021–22 (1.04–1.32) and
lower again in 2022–23 (0.93). Returns moving to the Austin–Round Rock counties are the high end,
$144–237k per return. Each year's net cohort to all states takes $0.63–1.05bn of California
state and local tax with it ($0.13–0.22bn to Texas, where $0.06–0.17bn is collected), gross of
the spending that moves with the people; neither state's net budget sign is known from this.

**Limits.** One self-reported main reason per mover, with no second reason; social desirability
could push a composition motive into "cheaper housing", "family" or "other"; origin is known only
to the state; every model is descriptive. The literature shows minority and foreign-born shares
predicting neighborhood exits within metros (Card, Mas & Rothstein; Crowder, Hall & Tolnay),
while studies that separate the Hispanic share find it adds little (Hall & Crowder; Pais, South &
Crowder); none links California's interstate out-migration to its Hispanic share. A MIGPUMA
design on ACS PUMS (revealed moves, no reasons) is the next test.

## Sources

- Lane: [`housing_supply_ca_tx_2026_09_22`](../infra/immigration-fiscal/housing_supply_ca_tx_2026_09_22/RESULT.md),
  `derived/state_supply.csv`, `state_growth_2010_2024.csv`, `metro_panel.csv`,
  `metro_regressions.csv`, `mechanical_response.csv`, `native_migration_2024.csv`,
  `audit.json` (source URLs, hashes, variable labels). [CALCULATION]
- Census Building Permits Survey state files; FRED `CABPPRIV`, `TXBPPRIV`; Census population
  estimates 2000–2024; ACS 1-year B25001, B01003, B05003H; ACS 5-year B03001 by CBSA (2010,
  2023); ACS 2024 1-year PUMS; Zillow ZORI metro file; Saiz (2010) elasticity file. [SOURCE]
- §8: [`movers_reasons_2026_09_24`](../infra/immigration-fiscal/movers_reasons_2026_09_24/RESULT.md),
  `derived/reasons_ca_leavers.csv`, `reasons_compare.csv`, `reasons_ca_by_subgroup.csv`,
  `q2_regressions.csv`, `irs_ca_tx.csv`, `tax_transfer.csv`, `q4_counts.csv`; reading notes in `lit/`. [CALCULATION]
- Repo context: [FAQ](immigration-objections-faq-2026-09-21.md) entries 4 and 15;
  [Tiebout memo](immigration-native-sorting-tiebout-2026-09-18.md); [September 16 housing lane](../infra/immigration-fiscal/housing_deport_2026_09_16/RESULT.md);
  [MSA rent panel](immigration-msa-rent-elasticity-panel-2026-06-25.md);
  [Saiz elasticity memo](immigration-causal-saiz-elasticity-rent.md); ladder 136, 139, 140.

## Revisions

- **2026-09-22 (initial).** Written from the lane after grading; the permit vintage check was
  restated from a failing gate to a recorded reconciliation before any number was copied.
- **2026-09-22 (evening, causal leg executed).** Layer 2 of §6 is run as
  [`housing_causal_2000_2010_2026_09_22`](../infra/immigration-fiscal/housing_causal_2000_2010_2026_09_22/RESULT.md)
  (ladder 183), on the all-foreign-born share rather than the Mexican-born share (no 2000
  metro endpoint for the latter) and with the ancestry push-pull prediction of ladder 182 as
  the instrument. Per point of foreign-born share over 2000–2010: rents +1.4% (SE 1.4), a
  null containing Saiz's one-for-one; values +11.6% (2.9), +5.7% (2.8) with the 2000 level.
  The settlement instrument gives two to five times more and Hansen J rejects the pair. No
  extra effect in supply-inelastic metros is detectable (rents −2.3% ± 3.9, values +0.9% ±
  6.2 on 223 Saiz-matched metros), which bounds the mechanical-response arithmetic of §4
  for rents: the two-to-three-fold coastal amplification it implies is outside the interval
  at the decade horizon. Native migration by education was not built. Nothing in §1–5
  changes.
- **2026-09-25 (movers' reasons).** §8 added from the
  [movers lane](../infra/immigration-fiscal/movers_reasons_2026_09_24/RESULT.md) (ladder 221):
  California's US-born leavers cite cheaper housing 2.2 times as often as other states' leavers
  and neighborhood/crime slightly less often (1.47% against 1.90%). Concept affected: the motive
  behind §5's native out-migration, previously unattributed. Nothing in §1–7 changes; 25 derived
  files byte-identical on the parent's rerun.
- **2026-09-25 (instrument qualified).** The causal leg's instrument (ladder 182) is a
  same-decade pull (ladder 199), so ladder 183's rent and value coefficients are diagnostics,
  not causal effects, and they no longer bound §4's mechanical-response arithmetic.
  [Decision](../decisions/2026-09-25-weekly-audit-corrections.md).
- **2026-09-25 (movers reading narrowed).** §8's stated reasons are shares among leavers. They do
  not measure leaving rates, and a composition effect acting through housing costs or schools
  would be reported as housing or schools, so "housing, not neighbors" describes answers, not the
  underlying cause. [Decision](../decisions/2026-09-25-weekly-audit-corrections.md).
