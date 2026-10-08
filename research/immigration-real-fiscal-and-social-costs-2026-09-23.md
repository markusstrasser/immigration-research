# Real fiscal and social costs of the Mexican-origin population to other residents

**Verdict:** The complete account's main case is a net cost to other residents of **$389.1–461.5bn a year**
([decision](../decisions/2026-10-07-main-case-v6.md), ladder 295), counting the pension promises members earn
as they work and, as whole people at their measured ages, the 3.04M descendants who no longer report Mexican
origin; counting benefits when paid, it is $307.4–385.4bn. Two of its settings come from this memo (§6): courts,
police and prisons are charged by use, and the government part of uncompensated hospital care is keyed to uninsured
use. The main case does not isolate what either key adds; if Mexican-origin offending equals the Hispanic average
as census codes record it, the case is **$4.8bn lower** at both ends. Hispanic residents are 20.2% of people in
prisons and jails combined, close to their
20.7% share of working-age residents, and 23.4% in state and federal prisons. The account compares the group with
the average other resident, not with whites; Hispanic adults are imprisoned at 2.6 times the white rate.

Fiscal and social costs together come to **$489.0–570.7bn a year** at central values, or $11.4–13.3k per member
of the 42.75M lineage (ladders 274, 295); counting benefits when paid, $407.3–494.6bn. The low end
assumes Mexican-origin offending equals the Hispanic average; the high end assumes it sits above that average, as
custody does (§7). Every social row is restated on the account's 39.7M, and the 3.04M added descendants' own rows
take their share of each row's engine key at their measured ages [ASSUMPTION]. The lanes' own figures, on the CPS's
40.9M and without the added descendants' rows, give $483.0–564.8bn, and stacking every item's low and high values
gives $208.8–830.9bn. The social rows, $bn a year at the low / high end:

| Item | $bn | Section, ladder |
|---|---:|---|
| Crime victims' harm, full cost including lives lost and pain (tangible losses $4.5bn) | 30.5 / 31.9 | §3; 202, 218 |
| Property crime | 1.3 / 1.4 | §3 |
| Unreimbursed hospital care, borne by hospitals, physicians and private payers | 3.1 / 5.3 | §3 |
| Housing net: other renters pay $22–58bn more, almost all to landlords who are other residents | −3.4 / −0.7 | §3; 200 |
| Road congestion that remains once road budgets respond | 13.6 / 11.6 | §3; 195 |
| Fine particles (PM2.5) from the group's consumption | 68.1 | §3b; 260 |
| Road crashes, other residents with against without the group's traffic | 10.6 | §3b; 266 |
| Fear and avoidance 10.3, private security −0.5, school disruption −1.9 | 7.9 | §3b; 258 |
| Five benefits: city size net of schooling 13.7, restaurants 6.8, volunteering 6.0, trade ties 6.8, consumer-side scale 2.1 | −35.4 | §3b; 201, 261, 265 |
| The 3.04M added descendants' rows: each row above times their share of its engine key (PM2.5 6.1) | 8.4 / 8.5 | §7; 281, 295 |

Wages move **$66–166bn** a year from less-educated to more-educated natives. Like the rent, this is a transfer among
other residents, not a net cost. By income the transfers run upward: outside the budget the bottom four fifths of
other residents lose $80.3bn a year and the top fifth gains $45.4bn (§4). Beside the total, capital at 7% on every
component would add $91 / 81bn to the fiscal case, and leaving out the government enterprises (option A) would remove
$17 / 23bn. [CALCULATION:
`infra/immigration-fiscal/sept24_propagation_2026_09_24/derived/oct07/real_costs_totals.csv`, rows
`pairing_on_priced_count`, `pairing_on_priced_count_cash_set`, `lineage_social_*`, `hispanic_mixed_group`,
`custody`, `full_span`, `capital_at_7pct` and `enterprises_out_option_a` (b0a2ccac);
`population_basis_2026_09_29/derived/restated_pairing.csv`;
`distribution_weights_2026_09_23/derived/oct07/channel_by_quintile.csv` (498a6a71)]

Date: 2026-09-23. Operator request: "equal charge --- should it be weighted with use of
courts, police, prisons? Do the remaining common sense stuff to get at the real fiscal and
social costs?"

## 1. Object and frame

Every number below uses the frame of the
[complete annual account](immigration-complete-annual-account-2026-09-20.md). It measures the
effect of the Mexican-origin residents, all generations and all schooling levels, on **all other US
residents** in 2024: 39,712,493 people as the account prices them, after the dataset audit scaled
the CPS's 40,896,574 to the ACS count of the Mexico-born outside California and Texas (ladders 209,
274). The comparison is stationary, with and without the group, in 2024 dollars a year. The main
case ($389.1–461.5bn; [decision](../decisions/2026-10-07-main-case-v6.md)) takes CBO's tax-incidence rules and
budget-category rule and sets:

- school spending at the full average cost per pupil (response 1); the first-year budget response
  keeps CBO's 63–66%;
- general public services at a finite-removal response of 0.60–0.85, with the consumption key
  corrected for saving and remittances;
- justice charged by use and uncompensated care keyed to uninsured use (this memo, §6);
- long-run road, park and economic-administration responses, rental assistance at 1, every
  government enterprise and a 2–3% real return on public capital;
- Social Security and Medicare Part A as the promises members earn as they work, at the benefits current
  law can pay on the 2026 Trustees Reports' separate OASI and DI funds (charged when paid instead, the case is
  $307.4–385.4bn); long-run property taxes; the income-tax key matched to IRS totals; state and local prices
  where the group lives; roads keyed by miles driven;
- retiree health on accrual, as pensions; user fees and the education keys, priced on the identified 39.71M
  only [ASSUMPTION]: public colleges keyed by measured use, tuition and hospital charges credited to who pays
  them, Pell keyed by the group's share and BEA's K-12 weight;
- since October 5, the 3.04M descendants who no longer report Mexican origin, counted as whole people (a
  42.75M-person lineage), at their measured ages since October 7; their own social rows take their share of
  each row's engine key (§7);
- defense, existing interest and business subsidies at zero response by assumption; other services
  respond proportionally.

Its per-case sampling standard error is $10.2–10.5bn, a partial approximation rather than a floor (ladder 184; [CALCULATION:
`uncertainty_propagation_2026_09_22/derived/oct07/summary.json`, 8020417a]). This is not the generation ledger.
Per-person gaps against whites come from a different object and do not combine with these totals
([FAQ, "Before combining numbers"](immigration-objections-faq-2026-09-21.md)).

## 2. Charging courts, police and prisons by use

Yes, use is the better key. It changes little because of what the account compares against.

| Part of public order and safety (BEA line 4, $519.2bn) | Per head | By use | Change $bn | Key |
|---|---:|---:|---:|---|
| Prisons ($121.3bn) | 12.0% | 14.2% | +2.63 | the group's share of institutional residents 18–64, ACS 2024 |
| Police excluding CBP and ICE custody ($210.7bn) | 12.0% | 13.1% | +2.21 | half arrests, half per head (patrol serves everyone) |
| Law courts ($80.2bn) | 12.0% | 13.3% | +1.01 | 60% criminal, keyed by arrests |
| ICE custody, interior part ($0.9bn) | 12.0% | 22.6% | +0.10 | Mexico's interior bed-day share |
| CBP ($23.9bn) and fire ($80.2bn) | 12.0% | 12.0% | 0 | not driven by residents' offending |
| **Total** | **$62.4bn** | **$68.4bn** | **+5.94** | in every main case since September 23 |

[CALCULATION: [justice-by-use lane](../infra/immigration-fiscal/cj_use_allocation_2026_09_23/RESULT.md),
`derived/central_split.csv`; 38 gates, rerun identical]

- **Why it is small.** Hispanic residents hold 20.2% of institutional places at 18–64 and are
  20.7% of household residents that age [DATA: `cj_use_allocation_2026_09_23/derived/acs_hisp_nativity_gq.csv`,
  sum of the Hispanic rows]. BJS counts give the same 20.2% for prisoners and jail inmates
  together. They are 23.4% of sentenced state and federal prisoners, whose ethnicity BJS adjusts
  with its prisoner surveys, and 14.4% of jail inmates, whose counts are unadjusted
  administrative reports. How much of that gap is coding is not established; if jails
  under-record Hispanic origin, the custody key is too low.
  [SOURCE: BJS, *Prisoners in 2023*, Tables 3 and 6; *Jail Inmates in 2023*, Table 5, via the lane]
  Hispanic adults are imprisoned at 606 per 100,000 against 460 for all adults (1.32 times),
  2.62 times the non-Hispanic white rate; non-Hispanic Black adults are at 5.27 times
  [DATA: *Prisoners in 2023* Table 6; `crime_victim_cost_2026_09_23/derived/offender_rate_crosscheck.csv`].
  Removing the group lowers custody costs by its share of custody. The comparison with whites
  belongs to the generation ledger, not to this account. [FRAMING-SENSITIVE]
- **The group's own excess depends on a coding correction.** The group is about 12.4% of
  residents aged 18–64 [CALCULATION: CPS/ACS scaling 1.0824 × ACS Mexican-origin household
  residents 18–64 ÷ all residents 18–64] and holds 14.2% of institutional places once ACS inmates
  coded only as "other Hispanic" are reassigned to named groups. Native "other Hispanic" adults
  show an institutional rate of 4.3%, against 1.2% for all natives, which points to institutional
  records without detailed origin rather than a real group [INFERENCE].
  Without the reassignment the prison share is 12.6% and the whole change is **+$1.67bn**.
- **Police rests on a 2019 arrest share.** It is the last year FBI tables report ethnicity.
  Hispanic adults made up 1.15 times their share of adult arrests. BJS's adult imprisonment
  ratio is also above 1: 1.42 in 2019 and 1.32 in 2023. NCVS victims' perceptions put Hispanic
  offending below the national rate, at 0.80. Carrying the arrest ratio down by the 2019–2023
  fall in imprisonment gives +$4.44bn. At the national arrest rate the central is +$3.19bn.
- **CBP is a boundary call.** Border spending follows crossings, not residents' offending. The
  lane keeps it per head. Holding it fixed, as the account holds defense, lowers the charge by
  $3.11bn (central +$2.84bn). Charging it by Mexico's share of encounters would raise it.
  Per head sits between the two.
- **Nativity.** The custody key raises the charge on US-born members, from $10.2bn to $12.7bn
  for prisons, and barely on the Mexico-born ($4.36bn to $4.51bn). At 18–64, 1.43% of US-born
  Mexican-origin adults and 0.79% of the Mexico-born live in institutions (after reassignment).
- **Full grid:** −$1.03bn to +$8.65bn across 216 key combinations. The Mexican-to-Hispanic
  ratio of 1.14 also moves between files: at its 2016 value (1.08) the central is +$4.70bn.
  [CALCULATION: justice lane `summary.json`, second pass 0a7299c]

## 3. What each priced channel adds

| Channel | What it is | $bn a year to other residents | Measured or modelled | Adds to the net? |
|---|---|---:|---|---|
| Courts, police, prisons by use | reallocation inside the fiscal account | +5.9 adopted (+1.7 raw codes; grid −1.0 to +8.7) | measured shares, assumed keys | adopted into the main case |
| Uncompensated hospital care | government offsets keyed below use; unreimbursed care outside any budget | +7.3 to +10.6: +3.7 to +5.7 inside, +3.2 to +5.6 outside budgets (+4.7 to +7.4 at 0.7× use) | measured uninsured share, published offsets, assumed use | inside part adopted; outside part a social item |
| Crime victims' harm | losses of other residents who are victims; excludes justice costs and offenders | 30.5 / 31.9 at the low / high end on the 39.7M (ladder 218); the first run's 28.9, before the mixed-group correction and on the CPS count, had one at a time 23.5–34.0, envelope 15.4–45.3 and arrest shares 43.1; 4.5 tangible (1.3–6.0) | measured incidents, modelled prices (lives valued at VSL) | yes, as a social (Z) item |
| Property crime | same frame, arrest-share proxy | 1.3–1.4 | proxy | yes, as Z; separate from the violent figure |
| Housing, net to other residents | rent the group pays to other residents' landlords, less the surplus triangle | −0.7 to −3.5, a gain (range −9.4 to +0.4) | modelled elasticities, measured rents | yes, as Z, long run only |
| Road congestion | other residents' extra travel time and fuel | 13.6 / 11.6 at the low / high end once roads respond, on the 39.7M (14.0 / 12.0 and full span 2.0–30.8 on the CPS count); 19.2 (8.0–35.3) with road budgets fixed, on the CPS count; network approaches 7–60 | measured traffic shares and delay, modelled speed response | yes, as Z beside the main case |

Sources: [victim harm](../infra/immigration-fiscal/crime_victim_cost_2026_09_23/RESULT.md),
[uncompensated care](../infra/immigration-fiscal/uncompensated_care_2026_09_23/RESULT.md),
[housing](../infra/immigration-fiscal/housing_transfer_2026_09_23/RESULT.md),
[congestion](../infra/immigration-fiscal/congestion_2026_09_23/RESULT.md).

- **Congestion.** With road budgets fixed, the cross-city estimate that a metro with more people is
  slower on the same lanes (elasticity −0.12, SE 0.035, Couture, Duranton and Turner) gives $19.2bn on
  the CPS count, 94% of it time valued at USDOT's rates and 6% excess fuel. Approaches built on the Urban
  Mobility Report's delay (9.8bn hours, $269bn, reproduced) give $7–60bn. The spread comes from
  two inputs: how steeply delay rises with traffic (the link-level curve's 4 against 1.0–2.5 for
  whole networks) and how much of the freed road space other drivers refill (Duranton and
  Turner). Sharing CDT's slope and refill, the approaches agree near $10bn. The group drives
  about 12% of commute vehicles and lives in congested metros; ten metros carry 47% of the cost,
  Los Angeles 13%. Per other commuter it is $767 a year in Los Angeles and $58 in New York.
  Under the proportional benchmark roads grow with population and only a $9.0bn residual
  remains. Since September 27 the main case lets road budgets respond in the long run, which takes
  part of the traffic cost into the account: $14.0bn remains at the low end and $12.0bn at the high
  end on the CPS count, $13.6bn and $11.6bn on the account's 39.7M, the central the total carries
  (`service_response_long_run_2026_09_27`, ladder 274). Crashes and PM2.5 are priced in §3b; pavement wear
  is not.

- **Victims.** The central counts about 1,020 killings and 402,000 non-fatal violent
  victimisations of other residents a year, $707 per member of the CPS's 40.9M ($718 per member of
  the 39.7M the account prices). Murder is 32% of the full
  cost. Victim-only unit prices (Miller et al. 2021) are used, as the
  [crime-harm rule](immigration-policy-causal-evidence-2026-09-20.md) requires. The older
  McCollister prices double count deaths, which is corrected in e8eab52. The offender input
  was the weakest link. NCVS victims perceive Hispanic non-fatal offending at 0.94 times the
  white rate. Texas–Arizona police records (NIBRS 2022–2023) put it at 1.7–2.2 times, and 4.2
  times for robbery, or 0.92–1.18 times all residents. They also put 70–81% of Hispanic
  offenders' victims in-group, against about 40% in NCVS. The two corrections nearly cancel.
  The result is $28.6bn full ($24.8–30.3bn over 20 specifications), or $32.0bn on the custody
  footing. The $43.1bn arrest-share arm and a $40.0bn offender-share arm keep NCVS's victim
  mix. Both imply twice the cross-group offending that police records support, and both fail
  an adding-up check against NCVS victim counts (ladder 202).
- **One footing for both crime lanes.** The justice central assumes Mexican-origin offending
  sits above the Hispanic average as custody does (ratio 1.14). The victim central assumes the
  two are equal. On the equal footing the pair is **+$1.7bn and $28.9bn**; on the custody
  footing it is **+$5.9bn and $32.3bn**.
  [CALCULATION: justice `summary.json` `scaling_raw`; victim `arms.csv` "ACS institutional ratio 1.118"]
- **Uncompensated care.** The group holds 25.7% (SE 0.6) of the nation's uninsured
  person-years against 12.0% of residents: 35.1% of the Mexico-born are uninsured and 14.3% of
  US-born members. That is $11.0–13.2bn of hospitals' uncompensated care. Governments offset
  58–70% of it (Urban Institute, VA and IHS care excluded). The account keys those offsets by
  measured MEPS payments: Medicaid 12.3%, Medicare 5.8%, government health consumption 7.7%. The
  first version of this lane used 12.0–19.6% and understated the gap (corrected 575e2ee). The
  0.7× rows assume the group's uninsured use hospitals at 0.7 times the average.
- **Housing.** The long-run arm matches the account's primary case: structures are rebuilt and
  land is scarce. The short-run arm (fixed stock: renters pay $110–120bn) must not be paired with
  it. Monras (2020) finds rents *fall* with low-skilled Mexican inflows because construction
  gets cheaper. The repo's decade estimate (ladder 183) cannot reject that.

## 3b. Social items added on September 28–29

The operator added ten items to the social rows, costs and benefits, from the September 27 case on
([decision](../decisions/2026-09-28-social-items-fear-security-schools.md),
[decision](../decisions/2026-09-28-social-items-pollution-crashes.md),
[decision](../decisions/2026-09-28-social-items-scale-benefits.md),
[decision](../decisions/2026-09-28-social-items-more-benefits.md),
[decision](../decisions/2026-09-29-crash-item-with-against-without.md)). $bn a year; the central on the
account's 39.7M people (ladder 274), the lanes' own central and range on the CPS's 40.9M, and the figure
against as many average residents on the lanes' counts, which sits beside and is never added:

| Item | Central | Lane central (range) | Normalized, lane's count, beside | Ladder |
|---|---:|---|---:|---|
| Fear and avoidance among residents who are not victims | 10.3 | 10.5 (5.2 to 30.3) | — | 258 |
| Private security | −0.5 | −0.6 (−2.9 to 0.4) | — | 258 |
| School disruption: Hispanic pupils are 29% of enrollment and 24% of out-of-school suspensions | −1.9 | −1.95 (−11.7 to −0.5) | — | 258 |
| PM2.5 from the group's consumption | 68.1 | 69.7 (31.5 to 122.5) | −46.5 | 260 |
| Road crashes, with against without the group's traffic | 10.6 | 11.1 (−57.7 to 74.3) | 0.6 | 264, 266 |
| City size net of the schooling mix (gain) | −13.7 | −13.9 (−84.4 to 56.6) | 24.9 | 201 |
| Restaurant market size (gain) | −6.8 | −6.8 (−19.2 to −1.1) | 1.2 | 261 |
| Formal volunteering for people outside the group (gain) | −6.0 | −6.2 (−7.9 to −4.5) | 4.2 | 265 |
| Consumer-side scale: network costs, grocery variety, media (gain) | −2.1 | −2.2 (−11.9 to 6.1) | 2.5 | 265 |
| Trade, travel and investment ties with Mexico (gain) | −6.8 | −6.8 (−23.8 to −1.1) | 0.8 | 265 |
| **Net of the ten** | **51.2** | **52.8** (−182.8 to 282.9) | | |

Rerun on the account's 39.7M, the PM2.5 range is $30.8–119.7bn (normalized −$45.5bn) and the crash range
−$55.1bn to +$70.8bn ([lane](../infra/immigration-fiscal/social_spans_priced_count_2026_09_29/RESULT.md)). Charging crashes by fault instead gives $40.6bn ($23.0–69.8bn; $42.3bn on
the lane's count), which sits beside and is never added: graded evidence
puts the response of the non-fatal crash rate to traffic near zero (+0.07) and of the fatal rate at
−0.21, so most crashes other residents have with the group's drivers would happen anyway (ladder 266).
Property values stay out: a price discount is a transfer between owners and buyers, or capitalises
crime and schools already priced; a flagged taste arm is $18.5bn. Run the same way for non-Hispanic Black
residents, fear, security, schools and property values come to $51.0bn ($16.5–158.8bn). The income split
(§4) and the winners-and-losers allocation do not carry these items. [CALCULATION:
`sept24_propagation_2026_09_24/derived/oct07/real_costs_totals.csv`, rows `social_item_*`;
`population_basis_2026_09_29/derived/restated_pairing.csv`; `social_costs_unpriced_2026_09_28/items.py` →
`derived/items.csv` (fa791b1)]

## 4. Transfers among other residents: not added, but who bears them

At fiscal weight 1 these cancel inside "other residents", and the production term already
contains their net. They answer who pays, not how much.
[CALCULATION: [wage split](../infra/immigration-fiscal/wage_distribution_2026_09_23/RESULT.md) (3afdb25);
[housing](../infra/immigration-fiscal/housing_transfer_2026_09_23/RESULT.md) §4, §8]

| Who | Long-run change a year |
|---|---|
| Less-educated native workers | wages 2.2–7.0% lower, −$66 to −$166bn (ε = ∞, the account's default); −$26 to −$107bn at ε = 3 |
| More-educated native workers | wages 1.0–3.0% higher, +$71 to +$163bn |
| Less-educated workers born abroad outside the group | −$14 to −$30bn (−$24 to −$50bn at ε = 3) |
| Natives as a whole, after tax | −$14.6 to −$0.3bn (+$26 to +$59bn at ε = 3) |
| Renter households outside the group (38.99m) | +$22 to +$58bn rent, central $34bn, about $860 a household |
| Owner-occupiers outside the group (80.64m) | +$1.2 to +$3.3tn home value, a stock |

The wage figures are the account's calibrated CES, not a measured wage effect. Measured wage
effects on less-educated natives are disputed in both directions
([canon audit](immigration-canon-citation-audit-2026-09-17.md)). The dollar size depends on
where the skill line falls and on the substitution elasticity σ.

**The transfers run from poorer to richer residents, measured.** The distribution lane ranks
other residents by SPM resources per equivalent adult (CPS ASEC 2025) and splits each channel by
income fifth, $bn a year, on main case v6:

| Channel | Bottom fifth | 2nd | 3rd | 4th | Top fifth | Total |
|---|---:|---:|---:|---:|---:|---:|
| Wages, after tax | −4.7 | −10.9 | −11.7 | −4.2 | +29.8 | −1.7 |
| Housing net (renters' extra rent, landlords' receipts) | −7.2 | −5.3 | −3.8 | −1.9 | +21.7 | +3.5 |
| Crime victims' harm (custody footing) | −10.4 | −6.5 | −5.5 | −5.0 | −4.9 | −32.3 |
| Unreimbursed hospital care | −0.5 | −0.7 | −0.9 | −1.1 | −1.2 | −4.4 |
| **Outside the budget, together** | **−22.8** | **−23.4** | **−21.9** | **−12.2** | **+45.4** | **−34.9** |
| Fiscal cost, financed in proportion to taxes paid | −12.6 | −26.7 | −45.0 | −73.7 | −259.1 | −417.1 |
| Fiscal cost, financed by equal cuts per person | −83.5 | −83.4 | −83.4 | −83.4 | −83.4 | −417.1 |
| Rental assistance, LIHEAP and public housing, borne by eligible households without the aid | −6.5 | −2.0 | −0.3 | −0.0 | 0.0 | −8.8 |

The cells are rounded under control so that every row and column adds: the third fifth's unreimbursed care and the
bottom fifth's per-person fiscal cost each sit 0.1 from their nearest rounding. The fiscal rows are the main case:
cash $289.4bn, the return on public capital's resource cost $48.8bn and the pension accrual $78.9bn, which the lane
distributes like the rest and reports apart. The winners lane's
construction of the same channel, which the INDEX quotes, comes to $415.9bn on this lane's bridge; the two differ only
in induced receipts: the engine's at the band's ends here, its central scenario's there ($1.2bn). The survey cannot
find the 3.04M added descendants, so they stay among the payers [ASSUMPTION]. The lineage's production term
scales the wage scenarios; the other rows do not move with the case.

In dollars the channels outside the budget nearly cancel. By income they do not: the bottom four
fifths lose $80.3bn a year and the top fifth gains $45.4bn.

- **Housing.** Renters pay about the same extra rent in every fifth ($566 a year per renter
  household at the bottom, $1,770 at the top, but 13.8m renter households against 4.0m).
  Landlords' receipts go 77% to the top fifth and 65% to the top tenth.
- **Wages.** Deciles 1–8 lose and the top two deciles gain.
- **Crime.** Victimisation is highest in low-income households: 40.0 violent victimisations per
  1,000 persons below $25,000 against 17.2–20.4 above $100,000 (NCVS 2022–2024). The harm takes
  1.83% of the bottom fifth's resources and 0.09% of the top fifth's.
- **Consumer prices** (side view, never added) are the one gain larger at the bottom relative
  to resources, 0.39% against 0.18%, though 41% of the dollars go to the top fifth.

**The fiscal cost's incidence is a financing convention.** If every tax rises in proportion, the
top fifth bears 62% of it. If services are cut equally per person, it takes 14.7% of the bottom
fifth's resources and 1.6% of the top fifth's. The actual mix of taxes, cuts and deficits is not
identified. With the channels above and the displaced beneficiaries added (congestion, property
crime and the §3b items excluded), the central total of $460.8bn takes 7.4% of the bottom fifth's
resources and 4.0% of the top fifth's under tax-share financing, and 19.9% and 0.71% under
per-person cuts.

**Weighted by income.** Each dollar is weighted by (y/ȳ)^−η, with a 5th-percentile floor, and
the result is reported as the equal per-person loss that would be as bad, which does not depend
on how the weights are normalized. The channels outside the budget cost $94–111bn at η = 1–2,
2.7–3.2 times their dollar sum. The whole central total is equivalent to $269.3bn under tax-share
financing and $540.1bn under per-person cuts at η = 1.3, the UK Green Book's value. OMB's 2023
Circular A-4 used 1.4; it was revoked in 2025 and the reinstated 2003 Circular sets no weights.
Choosing η is a value judgment, so η = 0, 1, 1.3, 1.4 and 2 are all in the lane. The lane's
mean-normalized totals (−$602.6bn and −$1,208.6bn at 1.3) are the same sums multiplied by the average
weight (2.24), not a larger harm.
[CALCULATION: [distribution lane](../infra/immigration-fiscal/distribution_weights_2026_09_23/RESULT.md)
(f5b6d67; v6 case 498a6a71),
`derived/oct07/channel_by_quintile.csv`, `derived/oct07/weighted_totals.csv`, `derived/case_ends_oct07.json`; 311
gates]
[FRAMING-SENSITIVE]

## 5. Checked and not found, or already inside the account

- **Native out-migration** from California is real, but the $2.1bn of state-local revenue it
  costs is 1.1% of that state's gap. It tracks top tax rates, not the Mexican-origin share
  (ladder 139).
- **Displaced natives drawing transfers:** no take-up on the margins measurable for 2000–2010.
  The instrument is weak on exogeneity, so this is a null, not a reversal (ladder 140).
- **Flight from public schools** does not reproduce. Local revenue falls where Hispanic
  enrollment rises, and state aid mostly offsets it (ladder 141).
- **Neighbourhood upkeep and petty disorder:** no group effect at equal income (ladder 142).
- **Extra school costs** in the districts where the group lives are already priced: the
  district differential is $0.50–0.56bn
  ([school lane](../infra/immigration-fiscal/school_enrollment_2026_09_20/README.md)).

## 6. Decisions (adopted 2026-09-23) and the rules since

The operator adopted the proposals on September 23
([decision](../decisions/2026-09-23-main-case-general-government-and-use-keys.md)). They are in every main
case since:

1. **Public order and safety keyed by use**: prisons by custody, police half by arrests, courts by the
   criminal share, CBP per head. CBP stays per head because both alternatives rest on counterfactual
   border flows the account does not model.
2. **Uncompensated hospital care keyed to uninsured use.** The under-charged government part enters the
   account; the unreimbursed part is a cost outside the budget.
3. **General government responds** instead of staying at zero, since September 26 as a finite removal at
   0.60–0.85
   ([decision](../decisions/2026-09-26-main-case-finite-removal-and-consumption-key.md)). Across states,
   administration spending scales at 0.842 (SE 0.039); the only within-state test gave 0.47 with a 95%
   interval of −0.72 to 1.66, which cannot tell zero from one. Zero was a budget-scoring convention.
4. **Social items stay beside the fiscal headline**, never folded into a figure labelled fiscal. Since
   September 28 they include the items of §3b.

## 7. Putting the pieces together

This section is computed on main case v6, which counts the 3.04M descendants who no longer report Mexican
origin as whole people at their measured ages. The rules: transfers (§4) are not added. The ledger and this account are not mixed. Each item
below is built in this account's frame and does not overlap the others: victims' harm excludes
justice costs, housing excludes the production term, uncompensated care is net of offsets
already charged. [CALCULATION: sums of the rows above]

The two crime lanes enter on one footing at a time (§3). The published pairing takes the envelope
of the two: the equal footing at the low end, with decision 4's mixed-group victims figure, and
the custody footing at the high end. Every row but the added descendants' is on the 39.7M people the account
identifies, with the crash and congestion rows' driving ratios per person aged 5+ (ladder 274); the added
descendants' rows take their share of each row's engine key at their measured ages [ASSUMPTION], with their crime,
congestion and crash amounts resting on the engine's third-plus and third-plus white cells, not on measured offending
or driving. Their shares are read before v6's other items, which change the lines' prices and keys but not the
quantities the social rows scale with, and the user-fee item's cell shifts stay with the identified union
[ASSUMPTION].

| $bn a year | Low end: Mexican-origin rates = Hispanic | High end: custody ratio carried over (adopted key) |
|---|---:|---:|
| Fiscal main case | 384.3 (justice +1.7) | **461.5** (justice +5.9) |
| + crime victims' harm, full cost | +30.5 | +31.9 |
| + property crime, arrest-share proxy | +1.3 | +1.4 |
| + unreimbursed hospital care, outside budgets | +3.1 | +5.3 |
| + road congestion, time and fuel, roads responding | +13.6 | +11.6 |
| − housing net gain | −3.4 | −0.7 |
| + the ten items of §3b, net | +51.2 | +51.2 |
| + the 3.04M added descendants' social rows | +8.4 | +8.5 |
| **= total at central values** | **489.0** | **570.7** |
| Per member of the 42.75M lineage | $11.4k | $13.3k |

At the low end the fiscal row is the case with justice on the census codes as recorded, $4.8bn below the case's
$389.1bn: the case prices public order and safety at the states' price level, and that line follows the justice
key. Every cell is at its nearest rounding and the columns add. Counting benefits when paid, the total is
$407.3–494.6bn.

On the custody footing alone the total is $489.2–564.8bn on the lanes' counts, without the added descendants' rows.
Stacking every low choice, then every high one, spans $208.8–830.9bn on the lanes' counts. The low end takes the
justice grid's low end, uncompensated care at 0.7× use, the victim envelope's low end, congestion's low end ($2.0bn)
and the housing range, plus each §3b item's low value; the high end takes the opposite ends.
The ten items' stacked range, −$182.8bn to +$282.9bn, drives most of the width: the crash item's
evidence range crosses zero, and the scale net runs from a $84.4bn gain to a $56.6bn cost.
[CALCULATION: `sept24_propagation_2026_09_24/derived/oct07/real_costs_totals.csv`, section 7 (b0a2ccac);
`population_basis_2026_09_29/derived/restated_pairing.csv`]

No priced item changes the sign. The low end is a net cost at every service response, even with every service budget
frozen; the high end turns only if every public production response falls below a common 3.2–5.4% of proportional.
With the government enterprises at 1 the break-even is −9.05% to +1.58%, so the high end turns only below a 1.58%
response with shared allocation ([sign reversal](../infra/immigration-fiscal/main_case_2026_10_07/RESULT.md),
`derived/sign_reversal.csv`, `oct07`).

## 7b. Benefits priced to the same standard

Evidence-symmetry rule 5 requires pricing the gains the account omits the way the costs above are
priced. Each lane ruled whether its gain already sits inside the production term P.

| Benefit | $bn a year, central (range) | Where it goes | Ladder |
|---|---:|---|---|
| Care: taxes on native women's extra hours (+2.69), net elder-care Medicaid saving (+1.49) and a second-order output effect with its taxes (−0.03) | +4.15 (2.60–13.35) | inside the fiscal account since September 24 | 198 |
| Cheaper services to consumers | 21.8 (11.9 net of native wage gains) | inside P; side view, not added | 198 |
| Cheaper construction (0.75%) | 0 | inside P; other renters' extra rent $33.5bn → $29.9bn | 200 |
| City size and schooling mix, one regression (Card–Rothstein–Yi) | +13.7; on the CPS count +13.9 (−56.6 to +84.4) | in the social rows since September 28 (§3b) | 201 |
| Restaurants, volunteering, consumer-side scale, trade ties | +21.7 | in the social rows since September 28 (§3b) | 261, 265 |
| Mobility: local-shock insurance and Borjas's gain | +0.65 (0.18–2.46) | beside the account; fiscal slice 0.03 | 203 |
| Innovation (patents) | not added | no response at the group's schooling; interval ±$500bn | 201 |

Scale is the one large and uncertain item. Bigger cities add $38.6bn to other residents'
earnings; the group's lower schooling takes back $24.9bn. The instrumented 1970–2000
college-share studies would make the net a cost of $109–677bn. Ciccone–Peri's joint estimate
from the same era gives +$116–169bn.

Of the benefits priced to this standard, only mobility ($0.65bn, 0.2% of the main case) stays outside
both the account and the pairing. None changes the sign. [CALCULATION: rows of §7 and the lanes'
`summary` files; care `care_household_services_2026_09_23/derived/summary.csv`, scale
`scale_spillovers_2026_09_23/derived/summary.csv`, mobility
`labor_mobility_insurance_2026_09_23/derived/insurance_summary.json`]

## 8. Still unpriced

- **Pavement wear** is not priced. Congestion (§3), crashes and PM2.5 (§3b) are. Priced but kept out
  of the total: CO2, ozone and government-services emissions, disease and food safety, and the
  cuisine mix (`sept24_propagation_2026_09_24/derived/oct07/real_costs_totals.json`, `never_added`).
- **Innovation and automation.** The transported patent-effect scenario is too imprecise to
  supply an identified offset; this is not evidence of zero innovation. The schooling-corrected
  arm has a positive point estimate with very wide uncertainty
  ([source correction](../infra/immigration-fiscal/scale_spillovers_2026_09_23/RESULT.md), September 26).
  No innovation term is added. Slower mechanisation is not priced.
- **Institutions, politics and trust.** No dollar measure is defensible from held data.
- **Amenity and culture.** The modern housing exercise identifies no defensible amenity
  dollar price; it does not establish zero amenity harm. The historical estimates reproduce
  ([corrected source](immigration-hedonic-replay-2026-09-19.md)). At matched
  age, education and sex, creative labour per head is 0.72–0.74 of whites' (ladder 156).
- **Remittances** are not a cost in this frame. They are the group's own income, and the
  consumption taxes they displace are already in the account's receipts.

## Limits

- The victim figure prices lives at the value of a statistical life and includes pain and
  suffering, so it is a welfare measure, not a budget cost. Its $4.5bn tangible part is the
  closest analogue to budget dollars. [FRAMING-SENSITIVE]
- The police key (half by arrests), the court criminal share (50–75%), CBP, and the offset
  shares for uncompensated care are assumptions with stated ranges.
- Input years differ: BEA 2024, ICE FY2024, arrests 2019, BJS 2023, NCVS 2022–2024,
  ACS 2024, CPS March 2025, AHA 2020.
- Built with an LLM on a politically charged topic ([bias caveat](../notes/llm-bias-caveat.md)).
  Each lane exports its inputs and disconfirming arms so every key can be rechecked.

## Sources

| Lane | Commit | Result |
|---|---|---|
| [Justice by use](../infra/immigration-fiscal/cj_use_allocation_2026_09_23/RESULT.md) | c124ac7, 0a7299c | +$5.94bn central; +$1.67bn raw coding; +$2.84bn with CBP fixed |
| [Crime victims' harm](../infra/immigration-fiscal/crime_victim_cost_2026_09_23/RESULT.md) | d5cf290, 95ed28d | $28.9bn full / $4.5bn tangible; $43.1bn on arrest shares |
| Double-count correction in older crime prices | e8eab52 | McCollister risk-of-homicide premium removed |
| [Housing transfer](../infra/immigration-fiscal/housing_transfer_2026_09_23/RESULT.md) | 073a79d | renters +$34bn; net +$0.7–3.5bn |
| [Uncompensated care](../infra/immigration-fiscal/uncompensated_care_2026_09_23/RESULT.md) | 06a42b7, corrected 575e2ee | +$7.3–10.6bn ($3.7–5.7bn inside the account) |
| [Wage split](../infra/immigration-fiscal/wage_distribution_2026_09_23/RESULT.md) | 3afdb25 | −$66 to −$166bn / +$71 to +$163bn |
| [Main case, October 7](../infra/immigration-fiscal/main_case_2026_10_07/RESULT.md) | 218a2fb2, 1548b396 | $389.1–461.5bn; $307.4–385.4bn counting benefits when paid; the 2026 Trustees on separate funds, retiree health on accrual, the added descendants at their measured ages, user fees and the education keys |
| [Congestion](../infra/immigration-fiscal/congestion_2026_09_23/RESULT.md) | dd3c45a | $19.2bn ($8.0–35.3bn); $14.0 / 12.0bn once roads respond (`service_response_long_run_2026_09_27`) |
| Totals: `sept24_propagation_2026_09_24/real_costs_totals.py` | b0a2ccac | the pairing and §7, §7b on main case v6 |
| [Population basis](../infra/immigration-fiscal/population_basis_2026_09_29/RESULT.md) | b7f14e7 | every row on the account's 39.7M |
| [Income weights](../infra/immigration-fiscal/distribution_weights_2026_09_23/RESULT.md) | f5b6d67, 498a6a71 | outside the budget on main case v6: bottom four fifths −$80.3bn, top fifth +$45.4bn |

## Revisions

- 2026-09-24 (main case adopted): the fiscal main case is now $200.9–246.3bn (ladder 219). It
  includes care and household services (−$4.15bn), which §7b listed beside the account. §7 and §7b
  stay as computed on the September 23 case. On the new case the central total with mobility is
  about $253–304bn; care now sits inside the account and the other social items are unchanged
  [CALCULATION: 200.9 + 51.9; 246.3 + 57.2]. The crime check's mixed-group correction adds $2.0bn
  to victims' harm on the Hispanic-rates footing (ladder 218). It is not recomputed on the custody
  footing. Concept affected: the fiscal row of the combined totals ([decision](../decisions/2026-09-24-main-case-audit-and-outside-checks.md)).

- 2026-09-23 (later): the operator adopted the §6 proposals
  ([decision](../decisions/2026-09-23-main-case-general-government-and-use-keys.md)), so the fiscal
  main case is now $203.2–249.6bn. Uncompensated care was corrected to the account's actual keys
  (575e2ee), which raised it from $1.6–9.2bn to $4.7–10.6bn. Totals are recomputed: $228–287bn at
  central values, $203–304bn full span. Concept affected: the complete account's main case and
  the social items beside it.
- 2026-09-23 (income distribution): §4 now reports the distribution lane's measured split
  (f5b6d67). The victimisation gradient is verified from the NCVS tables, and the sentence that
  the fiscal gap "may run the other way" is replaced by the two financing conventions. Concept
  affected: who bears the transfers among other residents.
- 2026-09-23 (congestion): road congestion priced (dd3c45a) and added to §7 as a social item,
  $19.2bn ($8.0–35.3bn). Property crime, listed in §3 but missing from the first §7 table, is now
  included. Totals: $248–307bn at central values, $212–340bn full span. Concept affected: the
  social costs reported beside the fiscal headline.
- 2026-09-23 (construction and grounding lanes): with cheaper construction (0.75%, ladder 200)
  other renters' extra rent is $29.9bn instead of $33.5bn; the housing net moves by −$0.01bn, so §7
  is unchanged. The ancestry instrument could not measure the congestion or wage slopes (ladder
  199), so the congestion item stays on Couture–Duranton–Turner's elasticity and the wage transfer
  stays a calibration. The distribution lane's quintile split (§4) used the $33.5bn and was not
  re-run; the change is $3.6bn on the renter side. Concept affected: housing transfer and the
  grounding of the social items.
- 2026-09-23 (offender ethnicity and benefits): police records (NIBRS, ladder 202) confirm the
  victims' central: $28.6bn against $28.9bn, and $32.0bn against $32.3bn on the custody footing.
  The $43bn arrest-share alternative fails a check against NCVS victim counts and leaves the
  verdict. §7b combines the four benefit lanes (ladder 198, 200, 201, 203) with the costs:
  $251–303bn with care and mobility, $237–289bn with the proposed scale net. Concepts affected:
  the offender input of victim harm; costs and benefits on one standard.

- 2026-09-25 (September 24 case, recomputed): the propagation lane rebuilt §7 and §7b from the
  lanes' files on both cases. Every September 23 total above reproduces (three only as sums of
  one-decimal rows). On the adopted case: §7 $246–296bn on the Hispanic-rates footing ($248–298bn
  with decision 4's victims figure) and $253–304bn on the custody footing, full span $210–337bn;
  §7b $258–308bn costs only, $253–303bn with care and mobility, $239–289bn adding the scale net.
  The 2026-09-24 note's "about $253–304bn" summed the printed one-decimal social row; the exact
  figure is $252.7–303.4bn. Concept affected: the combined totals' fiscal row
  ([lane](../infra/immigration-fiscal/sept24_propagation_2026_09_24/RESULT.md)).
- 2026-09-26 (schools at full average cost, [decision](../decisions/2026-09-26-main-case-schools-full-cost.md)):
  the propagation lane recomputed §7 and §7b on the new main case, $258.5–292.0bn (4e66adb). The
  fiscal row rises by the case's change since September 24, +$57.6bn and +$45.6bn, and the social
  rows do not move: $305–350bn at central values and $268–383bn full span; §7b $315–354bn costs
  only, $310–349bn with care and mobility and $296–335bn adding the scale net. The first-year
  budget response stays within $0.7bn of September 24. Concept affected: the combined totals' fiscal row.
- 2026-09-28 (amenity interpretation): the [adversarial audit](immigration-adversarial-audit-2026-09-28.md)
  found that §8 still said "Housing prices show no amenity discount" despite the
  [September 19 specification-equivalence correction](../decisions/2026-09-19-require-housing-specification-equivalence.md).
  Replaced that zero-effect reading with the source's unidentified contemporary valuation;
  historical coefficients reproduce. Concept affected: unpriced amenity harm. No priced total changed.
- 2026-09-28 (innovation interpretation): the same audit checked the adjacent statement
  "find no patent response" against the source's September 26 schooling correction.
  The corrected point scenario is positive but highly imprecise; §8 now preserves that
  uncertainty instead of implying zero innovation. Concept affected: unpriced productivity
  benefits. No dollar offset was adopted.
- 2026-09-28 (the September 27 case, [decision](../decisions/2026-09-27-main-case-capital-return-and-long-run-responses.md)): a new update block. Fiscal and social costs
  together are $363–438bn at central values (73cc30c). The 2026-09-26 block's statement that the social
  items do not depend on the case no longer holds: congestion moves by −$5.2bn and −$7.1bn at the ends.
  Concept affected: the fiscal-plus-social total and the congestion item.
- 2026-09-28, later (four unpriced social items, ladder 258): a new update block prices fear and
  avoidance, private security, property values and school disruption beside the account, +$7.9bn
  central for the union, not added pending the operator
  ([lane](../infra/immigration-fiscal/social_costs_unpriced_2026_09_28/RESULT.md)). Concept affected:
  the social costs reported beside the fiscal headline.
- 2026-09-28, latest (social items adopted, [decision](../decisions/2026-09-28-social-items-fear-security-schools.md)): fear, security and schools join the
  social rows from the September 27 case on, +$7.94bn at both ends of the central values; the pairing is
  $371–446bn. Property values stay out. Concept affected: the fiscal-plus-social total.
- 2026-09-28, latest (quality of life and scale benefits; decisions 2026-09-28-social-items-pollution-crashes and
  2026-09-28-social-items-scale-benefits): PM2.5 and road crashes join the social rows as costs, and the scale net and
  restaurant market size as gains. The crash item uses California's measured non-fatal fault. The pairing is
  $463–537bn. Concept affected: the fiscal-plus-social total.
- 2026-09-28, final (benefit search; decision 2026-09-28-social-items-more-benefits): volunteering, consumer-side scale
  and trade ties join the social rows as gains; the pairing is $447–522bn. Concept affected: the fiscal-plus-social total.
- 2026-09-29 (decision 2026-09-29-crash-item-with-against-without): road crashes move from fault-based attribution to with against without
  the group's traffic; the pairing is $416–491bn. Concept affected: the fiscal-plus-social total.
- 2026-09-29 (cleanup, [decision](../decisions/2026-09-29-delete-superseded-and-cruft-docs.md)): the verdict, §1, §3,
  §4, §6, §7 and §7b state the September 27 case; the eight dated update blocks became the earlier-totals
  table and §3b; the pairing is on the account's 39.7M people (ladder 274). The September 23 figures stay in
  that table and in `real_costs_totals.csv`'s sept23 column. Concept affected: which case the memo states as
  current, and the population behind the social rows.
- 2026-09-29 (number drift audit): the pairing's upper end is $488.0bn (488.047), not $488.1bn, which rounded 488.05 a second time. Concept affected: none; rounding only.
- 2026-09-29 (priced-count spans): §3b now gives the PM2.5 and crash ranges on the account's 39.7M, and the fault-based crash figure is $40.6bn ($23.0–69.8bn) on that count, $42.3bn on the lane's ([lane](../infra/immigration-fiscal/social_spans_priced_count_2026_09_29/RESULT.md)). Concept affected: none; the count the ranges are on.
- 2026-09-29 (memo sweep): §3's table and congestion note now give victims' harm ($30.5 / 31.9bn), congestion ($13.6 / 11.6bn), and §7b the scale net ($13.7bn), on the account's 39.7M, and label the CPS-count figures; $19.2bn is the roads-fixed arm, not the central. The four smaller benefits add to $21.7bn on the priced count (was printed $21.9bn; $22.0bn on the lanes' counts). Concept affected: none; which count and arm each figure is on.
- 2026-09-29, later (main case v4, [decision](../decisions/2026-09-29-main-case-v4.md), ladder 275): the verdict, §1, §4 and §7 state the main case of that date, $371.4–434.8bn. The pairing is $463.0–535.5bn ($11.7–13.5k per member), only the fiscal row moving, and $386.2–462.5bn counting benefits when paid. §4's fiscal rows carry the pension accrual and put public housing among the capped programmes; wages move slightly with the production model re-solved on the account's weights, so outside the budget the bottom four fifths lose $79.4bn and the top fifth gains $44.5bn. §4's table now adds by row and column. The sign's break-even is −5.5% to 3.3%, so the low end no longer turns at any service response. Concept affected: the fiscal-plus-social total, its distribution by income and the sign condition.
- 2026-09-29, later (number drift audit): the pairing's low end is $462.9bn (462.95), not the $463.0bn printed earlier that day, which was the sum of §7's rounded rows. §7 shows property crime's low end, $1.25bn, as 1.2 so the column adds. Concept affected: the fiscal-plus-social total's printed low end; no figure moved.
- 2026-10-05 (main case v5, [decision](../decisions/2026-10-05-main-case-v5.md), ladder 281): the verdict and §1 state the main case of that date, $390.3–461.2bn, which counts the 3.04M descendants who no longer report Mexican origin as whole people; the cash set is $307.4–383.4bn. The pairing, the standard error, §4's fiscal rows and §7 stay as computed on the September 29 case, and say so, until the propagation lane reruns them on the new case. Concept affected: the complete account's main case; the fiscal-plus-social total has not moved yet.
- 2026-10-05, later (v5 consumer lanes: distribution fecaae7e, uncertainty 9d37757d): §4, the verdict's income split and the standard error state main case v5. The fiscal rows are $417.6bn (cash $287.7bn, capital return $49.5bn, accrual $80.4bn) and the capped programmes $8.8bn; the lineage's production term scales the wage channel, so outside the budget the bottom four fifths lose $80.4bn and the top fifth gains $45.5bn. The standard error is $10.2–10.5bn. The pairing, §1's social rows and §7 stay on the September 29 case until the propagation lane's rerun. Concept affected: the main case's distribution by income.
- 2026-10-05, later (v5 consumer lanes: pairing 72f2e3bc, winners c1c259ef): the verdict's pairing, §1 and §7 state main case v5. Fiscal and social costs together are $490.2–570.7bn ($11.5–13.3k per member of the 42.75M lineage), $407.3–492.8bn counting benefits when paid; the fiscal row moves and the 3.04M added descendants' own social rows add $8.6 / 8.8bn, each row times their share of its engine key. §7's sign-reversal paragraph takes the v5 case's break-evens, and §4 names the $1.2bn of induced receipts between the two fiscal-channel centrals. Concept affected: the fiscal-plus-social total (ladders 274, 281).
- 2026-10-07 (main case v6, [decision](../decisions/2026-10-07-main-case-v6.md), ladder 295; consumer lanes: pairing b0a2ccac, distribution 498a6a71, uncertainty 8020417a): the verdict, §1, §4 and §7 state main case v6, $389.1–461.5bn ($307.4–385.4bn counting benefits when paid). Fiscal and social costs together are $489.0–570.7bn ($11.4–13.3k per member), $407.3–494.6bn counting benefits when paid. The added descendants' rows are $8.4 / 8.5bn (October 5: $8.6 / 8.8bn): at their measured ages they have smaller shares of consumption and road use. §4's fiscal rows are $417.1bn (cash $289.4bn, capital return $48.8bn, accrual $78.9bn), and outside the budget the bottom four fifths lose $80.3bn and the top fifth gains $45.4bn. §7's sign-reversal paragraph takes v6's break-evens, and §1's bullet on the added descendants no longer says their social rows wait on a rerun, which stopped being true on October 5. Concept affected: the fiscal-plus-social total and its distribution by income.
- 2026-10-08: living text states only the live case, at the operator's request; earlier-case figures removed, recoverable at 0e0c5e28.
- 2026-10-08 (live-case cleanup, with the FAQ): the verdict no longer quotes the use key's and the hospital-care key's increments measured on the September 23 case (+$5.9bn, $1.7bn with census ethnicity codes as recorded, +$3.7–5.7bn). The main case isolates neither key; with offending at the Hispanic average it is $4.8bn lower at both ends. §7b's care row prints its three channels at two decimals so the parts add: +2.69 + 1.49 − 0.03 = +4.15 (2.60–13.35), was +4.1 (2.6–13.3) naming two. §6 keeps the lane's own measurement as its record. Concept affected: none.
