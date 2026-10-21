# Who wins and who loses

Date: 2026-09-25. The operator asked on 2026-09-24: "it would be good to track who loses and who
wins exactly". [MODEL / FRAMING-SENSITIVE] Three choices shape the result:
- how the fiscal cost is financed;
- where the state and local cost falls;
- whether a household's gains and costs are shared among its members.

Every figure below names the choice it uses.

**Verdict (2026-10-21, main case v9, $368.0–436.6bn; [decision](../decisions/2026-10-16-main-case-v9.md)):**
Few other US residents come out ahead of the Mexican-immigrant lineage's presence, 3–8% at central values
depending on how the fiscal cost is financed, and the rest come out behind.
- Counting each household's gains and costs as shared among its members, and charging every part of the cost to
  today's residents (stationary financing), 2.70% come out ahead if the cost is financed by tax shares (a), 4.51% if
  by equal cuts per person (b) and 7.90% if by cuts to the programmes that respond (c). [CALCULATION:
  `derived/oct16/p7_net_shares.csv`, arm `recommended`, epsilon `infinite`, frame `stationary`, level `central`,
  sharing `pooled`]
- At the case's low end with the social rows' low values, 41.94% / 39.76% / 41.61% come out ahead under (a) / (b) /
  (c); at its high end with their high values, 2.84% / 3.02% / 3.53% [CALCULATION: the same rows, levels `low` and
  `high`].
- Giving wages to the earner alone, while taxes and rent stay shared, gives 3.41% / 4.33% / 9.05% [CALCULATION:
  sharing `person`].
- Spreading the trust-fund block over the next 30 years' payers instead (cohort financing, beside) gives
  7.69% / 10.46% / 14.87% [CALCULATION: frame `cohort30`].

The count runs person by person over the 292.59m other residents in CPS ASEC 2025. It covers the main case and
the social rows of the case's social pairing, each allocated by its own key (§2). At central values (the case's
midpoint with the social rows' central values) the net on today's residents is −$509.23bn, or −$1,740 per other
resident; it is −$191.94bn at the low end and −$830.15bn at the high. Under stationary financing nothing is left
to future payers: the $83.64bn of Social Security and Part A promises that the group's 2024 work earns is charged
to today's covered earnings, and state and local budgets carry $265.22bn. The group receives a direct transfer of
$9,190 per member of the 44.90M-person lineage. [CALCULATION: `p7_net_shares.csv`, `total_bn`, `mean_usd`;
`derived/oct16/p7_channel_table.csv`, channels `trust_accrual` and `state_local`; `derived/oct16/group_frame.csv`]

Who comes out where, at central values, pooled [CALCULATION: `derived/oct16/p7_cuts.csv.gz`, cuts `state3`,
`edu_nativity`, `tenure` and `decile`; §3]:
- **Behind:** 97–98% in California and Texas, 98–99% of US-born adults with a high-school education or less, 99%
  of renters, and over 98% of each decile in the bottom half, under (a) and (b).
- **Most often ahead:** landlords (22.9% under (a), 28.3% under (b), 35.2% under (c)), whose pooled net under
  tax shares is −$1,112 a year, and the top decile (9.1%, 28.3% and 37.7%).

Preferences, school dilution and the debt legacy's interest stay out of every net (§6, §7).
[CALCULATION: [ledger lane](../infra/immigration-fiscal/winners_losers_2026_09_24/RESULT.md), "v9 case (oct16)",
`--case oct16` → `derived/oct16/`; ladder 226] [FRAMING-SENSITIVE]

## 1. Object and frame

The frame is the [complete annual account](immigration-complete-annual-account-2026-09-20.md) on main case v9.
It measures the effect of the Mexican-immigrant lineage, all generations, on all other US residents in 2024,
comparing the year with and without the group. The lineage is the case's 44.90M people. Of them, 42.95M sit on
observed or proxy survey records: the reporters, item 10's completion and the 3.04M descendants who no longer report
Mexican origin, whom the lane takes out of the US-born nonmembers with two US-born parents in their five-year age
band and places at the identified third-plus members' records [ASSUMPTION]. The 1.95M people the Census misses are on no household record
and are left out of the payer pool. Native-minor calibration (item 16) changes only members' weights. [DATA:
`derived/oct16/p7_inputs.json`, `population`; lane RESULT, "v9 case (oct16)"]

A person is "ahead" when their sum over the priced channels is positive. Unpriced effects are not in
the count. The FAQ's rules for combining numbers apply: the channels below come from one frame and are
allocated, not added across objects.

Each channel goes to persons by its own key:
- **Fiscal cost:**
  - Federal general-fund costs go by federal tax share (a), per person (b) or receipt of the responding
    programmes (c). Rule (c) values each programme at its national budget and response; cash and SPM noncash
    receipts are survey fields, and health and school receipt are proxied by enrollment and age.
  - The state and local part stays in the states where the group lives, split by state and local taxes (a), per
    person (b) or programme receipt (c).
  - The trust-fund accrual goes to covered earnings under stationary financing and to future payroll payers,
    future births included, under cohort financing.
  - The return on public capital is a resource cost, never borrowed; the unlocated block goes per head.
- **Wages** (inside the account): the account's production nest, split at high school or less (σ 2, ε ∞).
- **Rent and housing:** renters and landlords, by ACS income cells and state.
- **Social rows** (the pairing's rows, beside the account): crime victims' harm, property crime, fear and private
  security by crime risk in the group's states; business crime and commercial security by national consumption,
  as passed to purchasers; unreimbursed care; congestion and crashes by urban vehicle exposure;
  PM2.5 by the source's local share plus national dispersion; school disruption by pupils in the group's states;
  city size, restaurant variety, volunteering, consumer scale and trade by national or state consumption keys. Every
  key is an incidence proxy.
- **Non-members who stay in mixed households** (item 11): their recomputed taxes, credits and benefits.

**Ways to count persons.**
- **Person count:** wages go to the earner, while taxes and rent are shared within the household
  (SPM unit). A degree-holding earner can come out ahead while the children and a non-working spouse
  carry their shares of the household's taxes with no offsetting gain.
- **Pooled count** (central here): each household's amounts are added up and shared among its
  other-resident members. The pooled amount is the household's person-weighted mean, which keeps every
  channel's total exact.
- **Mixed-unit count** (beside): it also shares the members' own after-tax resources with the other residents of
  their units. The sharing rules are sensitivities, not bounds: an individual's sign can fall outside both
  endpoints (lane RESULT, "Sharing rules are sensitivities, never bounds").

## 2. Who gains and who loses, by channel

$bn a year at central values, stationary financing, signed from other residents' side. The channel totals do not
depend on how persons are counted, and (a) and (b) differ only in who pays. Controlled rounding: the unlocated
block prints −4.7 (nearest −4.6) so the parts add to the total.
[CALCULATION: `derived/oct16/p7_channel_table.csv`, arm `recommended`, epsilon `infinite`, frame `stationary`,
level `central`; the mixed-unit boundary row is left out]

| Channel | (a) and (b) | (c) |
|---|---:|---:|
| Trust-fund accrual (Social Security and Part A promises) | −83.6 | −83.6 |
| Federal general fund | −38.7 | −94.2 |
| Current trust-fund cash | 0.0 | +55.5 |
| State and local, in the group's states | −265.2 | −265.2 |
| Unlocated fiscal block, per head | −4.7 | −4.7 |
| Beneficiaries displaced from capped programmes | −9.5 | −9.5 |
| Wage gains, workers with some college or more | +91.1 | +91.1 |
| Wage losses, workers with high school or less | −91.7 | −91.7 |
| Crime: victims, property, business, fear, private and commercial security | −52.0 | −52.0 |
| Health and environment: PM2.5 and unreimbursed care | −81.3 | −81.3 |
| Roads: congestion and crashes | −24.9 | −24.9 |
| Housing | +2.3 | +2.3 |
| School disruption | +2.2 | +2.2 |
| City size, variety, volunteering, consumer scale, trade | +35.8 | +35.8 |
| Non-members who stay in mixed households (item 11) | +11.0 | +11.0 |
| **Net on today's residents** | **−509.2** | **−509.2** |

The wage channel nets to −$0.6bn, but it moves $91bn a year from workers with high school or less to workers with
more schooling. Rule (c) splits the federal part differently, the general fund at −$94.2bn and the trust funds' current cash at
+$55.5bn, for the same net. The mixed-unit count adds a −$55.35bn boundary row for resources shared across the
member/nonmember line, for a net of −$564.58bn. [CALCULATION: `p7_channel_table.csv`, channel `mixed_boundary`;
`p7_net_shares.csv`, sharing `mixed_unit`]

## 3. Person nets by the cuts that separate them

Net (a) is in $ per person a year, pooled, at central values under stationary financing. The next three columns
give the share ahead, pooled, under each financing rule; the last gives the share ahead under the person count, (a).
[CALCULATION: `derived/oct16/p7_cuts.csv.gz`, arm `recommended`, epsilon `infinite`, frame `stationary`, level
`central`]

| Cut | People (m) | Net (a), $ | Ahead (a) | Ahead (b) | Ahead (c) | Person count, ahead (a) |
|---|---:|---:|---:|---:|---:|---:|
| California | 25.2 | −5,522 | 2.9% | 3.1% | 4.1% | 2.7% |
| Texas | 20.1 | −3,998 | 2.4% | 2.8% | 3.9% | 2.4% |
| All states except California and Texas | 247.2 | −1,171 | 2.7% | 4.8% | 8.6% | 3.6% |
| US-born, below high school, 25+ | 8.5 | −1,769 | 1.2% | 1.1% | 2.5% | 1.2% |
| US-born, high school, 25+ | 47.8 | −2,245 | 1.6% | 1.6% | 4.3% | 1.4% |
| US-born, some college, 25+ | 46.9 | −1,559 | 2.7% | 3.3% | 7.7% | 3.3% |
| US-born, BA or more, 25+ | 69.8 | −1,829 | 4.3% | 8.5% | 15.9% | 6.9% |
| Other foreign-born, below high school, 25+ | 4.6 | −2,232 | 1.1% | 0.9% | 1.3% | 1.0% |
| Other foreign-born, high school, 25+ | 8.2 | −2,519 | 1.5% | 1.6% | 3.0% | 1.3% |
| Other foreign-born, some college, 25+ | 5.5 | −1,885 | 2.2% | 2.7% | 5.8% | 3.0% |
| Other foreign-born, BA or more, 25+ | 16.9 | −2,426 | 3.3% | 7.3% | 11.5% | 6.1% |
| Under 25 | 84.5 | −1,232 | 2.3% | 3.9% | 4.2% | 1.8% |
| Renters | 85.7 | −2,071 | 0.6% | 0.9% | 1.3% | 0.7% |
| Owners without rental income | 182.6 | −1,669 | 1.0% | 3.1% | 7.4% | 1.9% |
| Landlords | 24.2 | −1,112 | 22.9% | 28.3% | 35.2% | 24.7% |
| Under 18 | 59.5 | −1,103 | 2.6% | 4.4% | 4.6% | 1.9% |
| 18–64 | 175.0 | −1,819 | 2.8% | 5.0% | 7.5% | 4.2% |
| 65 and over | 58.2 | −2,157 | 2.6% | 3.3% | 12.4% | 2.6% |
| Workers in construction | 9.7 | −2,188 | 2.7% | 4.0% | 5.9% | 4.0% |
| Workers in restaurants | 8.4 | −1,749 | 1.8% | 2.3% | 3.1% | 2.0% |
| Workers in agriculture | 1.7 | −1,683 | 3.8% | 5.2% | 9.6% | 4.4% |
| Workers in landscaping | 1.2 | −1,667 | 3.2% | 3.8% | 5.8% | 3.4% |
| Workers in other industries | 130.7 | −1,975 | 3.1% | 5.8% | 8.9% | 5.0% |
| Not working | 140.9 | −1,493 | 2.4% | 3.5% | 7.4% | 2.0% |
| Non-Hispanic white | 189.7 | −1,689 | 3.1% | 5.3% | 9.6% | 3.9% |
| Non-Hispanic Black | 41.5 | −1,434 | 1.3% | 1.8% | 3.6% | 1.7% |
| Non-Hispanic Asian | 22.6 | −2,652 | 2.4% | 5.2% | 8.0% | 3.6% |
| Hispanic, other than Mexican origin | 27.7 | −1,770 | 2.4% | 3.2% | 4.3% | 2.7% |
| Other race | 11.1 | −1,833 | 1.8% | 3.1% | 4.5% | 2.0% |
| Women | 149.1 | −1,707 | 2.7% | 4.4% | 7.7% | 2.8% |
| Men | 143.5 | −1,775 | 2.7% | 4.6% | 8.1% | 4.0% |

**By income.** SPM deciles of other residents; net in $ per person, pooled, the share ahead pooled
[CALCULATION: `p7_cuts.csv.gz`, cut `decile`]:

| Decile | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Net (a) | −1,255 | −1,255 | −1,277 | −1,364 | −1,447 | −1,493 | −1,677 | −1,825 | −1,991 | −3,823 |
| Ahead (a) | 0.7% | 0.8% | 1.1% | 1.7% | 1.8% | 2.4% | 2.0% | 2.9% | 4.6% | 9.1% |
| Net (b) | −2,048 | −1,883 | −1,875 | −1,860 | −1,852 | −1,777 | −1,855 | −1,784 | −1,653 | −815 |
| Ahead (b) | 0.4% | 0.7% | 0.8% | 1.3% | 1.4% | 2.0% | 1.7% | 2.7% | 5.9% | 28.3% |
| Net (c) | −2,441 | −2,306 | −2,184 | −1,965 | −1,823 | −1,663 | −1,678 | −1,533 | −1,352 | −456 |
| Ahead (c) | 0.7% | 1.1% | 1.9% | 2.8% | 4.0% | 4.9% | 5.0% | 7.5% | 13.4% | 37.7% |

- **Tax-share financing (a).** The top decile pays the most dollars. As a share of SPM resources, though, the net
  is four times heavier in the bottom quintile: −13.1% there against −3.2% in the top [CALCULATION: cut
  `quintile`, `pct_of_resources`]. Rent, wages and crime fall toward the bottom, while landlord receipts and wage
  gains go to the top.
- **Per-person cuts (b) and programme cuts (c).** The bottom deciles lose more and the top decile less; under (c)
  37.7% of the top decile come out ahead, the most of any decile.

## 4. What drives the split

- **Financing.** It is the largest single choice. Stationary financing charges the trust-fund accrual and the
  borrowed federal part to today's residents; cohort financing moves the trust block to the payers of the next 10 or
  30 years and raises the share ahead to 7.6–14.9% (sensitivities below).
- **Where the case and the social rows sit in their ranges.** At the low end with the social rows' low values about
  two in five come out ahead under every rule; at the high end 3–4%. The social producers' ranges move several rows
  by tens of billions in opposite directions (crashes and city size above all), and the low end's net on today's
  residents is under a quarter of the high end's.
- **Geography.** State and local budgets carry the largest part of the fiscal cost, and the lane charges it to the
  states where the group lives [INFERENCE: a state-level fiscal account would test it]. The average other resident
  is $5,522 behind in California and $3,998 in Texas, against $1,171 elsewhere, under (a).
  These are other residents' shares of the account's cost, a financing allocation. They are not the per-member gaps
  of the [California–Texas memo](immigration-california-texas-fiscal-geography-2026-09-21.md), and the two are never
  combined (FAQ, "Before combining numbers").
- **Schooling.** The production nest moves $91bn a year of after-tax wages from workers with high school or less to
  workers with more schooling. That puts US-born adults with high school or less 98–99% behind. Degree holders are
  ahead more often than other schooling groups (4.3% of US-born under (a), 8.5% under (b)).
  - The nest is the account's calibration, not a measured wage effect.
  - Measured effects on less-educated natives are disputed in both directions
    ([real costs](immigration-real-fiscal-and-social-costs-2026-09-23.md) §4).
- **Tenure.** Rent is the channel that lifts landlords: they are ahead 23–35% of the time, renters under 2%.
- **Household composition.** Pooled, children are ahead about as often as working-age adults under (a). People 65
  and over are ahead in 2.6% of cases under (a) but 12.4% under (c), where cuts follow programme receipt.

**Sensitivities.** Share of other residents ahead, pooled, central values unless named. [CALCULATION:
`derived/oct16/p7_net_shares.csv`; enumerated extrema `derived/oct16/p7_grid_extrema.csv`]

| Variant | (a) | (b) | (c) |
|---|---:|---:|---:|
| Central: stationary financing | 2.70% | 4.51% | 7.90% |
| Low end, social rows low | 41.94% | 39.76% | 41.61% |
| High end, social rows high | 2.84% | 3.02% | 3.53% |
| Person count | 3.41% | 4.33% | 9.05% |
| Mixed-unit count | 2.79% | 4.59% | 7.93% |
| Cohort financing, 30 years | 7.69% | 10.46% | 14.87% |
| Cohort financing, 10 years | 7.61% | 10.43% | 14.75% |
| State wage markets, rent capitalized, landlords by owner type (stacked arm) | 1.67% | 1.92% | 3.61% |
| Nest's within-cell elasticity 8.7 | 2.78% | 4.62% | 8.09% |
| Nest's within-cell elasticity 17.9 | 2.74% | 4.54% | 7.98% |

Over the lane's enumerated grid under stationary financing and pooling (both case ends, social settings, the
recommended and stacked arms), the share ahead runs from 1.25% to 41.94% under (a), 1.39% to 39.76% under (b) and
1.74% to 41.61% under (c). These are extrema of a declared finite grid, not bounds on household outcomes.

## 5. The group itself

This section is beside the account, and none of it is netted against other residents' rows.
[CALCULATION: `derived/oct16/group_frame.csv`]

| Item | $bn a year (range) | Basis |
|---|---:|---|
| Direct fiscal transfer received (the engine's direct response, sign flipped) | +412.7 (380.5–444.8) | at the case's ends; $9,190 per member |
| First generation's market gain over its earnings in Mexico | +201.9 (176.6–218.2) | place premium Re 2.46 (2.08–2.79) × $340.1bn of US earnings |
| Wage competition among the group's own workers with high school or less | −19.8 (ε ∞); −32.7 (ε 3) | account nest × members' CPS earnings |
| Wage gain of the group's own workers with some college or more | +6.0 (ε ∞); +6.1 (ε 3) | same |
| Victims inside the group, excluded from the victim lane | −20.1 | the victim lane's rows, on its equal footing |

Notes on the table:
- **Direct transfer.** It includes the imputed capital and post-engine components. It is not all cash members
  receive: item 11 carries effects on the non-members who stay.
- **Place premium.** The source reads: "the average emigrant comes from the 56th percentile of
  residual wages, suggesting that Ro/Re = 1.03 … so that Re ≈ 2.46" [SOURCE: Clemens, Montenegro &
  Pritchett, "The Place Premium", HKS RWP09-004, sec. 3.3 and Table 8, quote verified in the corpus].
  The gain assumes the same employment and hours in both countries [INFERENCE]. The second and
  third-plus generations have no counterfactual in Mexico here, and none is invented. The
  [world ledger](../infra/immigration-fiscal/world_ledger_2026_09_27/RESULT.md) (ladder 250) builds
  one for G2 (the same people raised in Mexico by parents with the same schooling who stayed) and bounds G3+
  between no premium and an upper bound; its live readings hold G3+ at the zero bound
  (`world_ledger_2026_09_27/derived/g2_premium_oct16.csv`, `readings_status_oct16.csv`).
- **Remittances.** Mexico received $62.8bn of remittances from the United States in 2024 [SOURCE:
  Banxico SIE table CE167, US-origin receipts, revised]. The corridor carries more than the CPS
  households send at surveyed amounts ([outside checks](immigration-outside-checks-2026-09-24.md),
  section "Consumption taxes").
- **By generation.** The account's split by generation is a cost to others, not a gain to the group,
  and it has no reference group. It is in
  [the account by generation](immigration-adopted-account-by-generation-2026-09-25.md) (ladder 224).

## 6. Items out of the totals, and rows on other counterfactuals

**Items kept out of every net:**
- **School dilution.** A present value of other residents' pupils' lifetime earnings, not annual cash. The operator
  adopted it on 2026-09-25 as priced beside the account; it stays out of every total unless option 3 is chosen
  ([decision](../decisions/2026-09-25-school-dilution-priced-beside.md)).
- **Preferences, the group's part** (proposed): an attribution under a proportional-replacement rule.

City size and schooling mix, which the September tables kept out, is now a social row of the pairing and enters
the nets (§2).

**Rows on other counterfactuals.** Three sister lanes price effects against other comparisons:
- movers: the movers staying in California;
- vending: California before SB 946;
- compliance: workers paid on the books.

A row enters a net only if its counterfactual is the group's absence. These rows therefore sit in the
role table (`derived/sister_other_counterfactuals.csv`) and in no net.

## 7. Limits

- **One year.** The count covers the people alive in 2024. It cannot say what today's children will
  pay or receive as adults.
- **State and local incidence.** It uses national ITEP rates by income group, not state rates;
  Texas's taxes are more regressive.
- **Wages.** They are national in the central arm; the stacked arm's state wage markets lower the share ahead.
- **Survey gaps.** CPS has no school type, no gross rents and few restaurant owners. Landlords are
  assumed to live in the state where the rent is paid.
- **Pooling.** It treats each household as sharing everything and measures nothing about how families
  actually share. The truth for any family need not lie between the counts.
- **Kept out of every net.**
  - The debt legacy's interest on past gaps is a different object; historical financing is not yet measured on
    v9 (`derived/oct16/channels.csv`, row `debt_legacy`).
  - The owners' home-value gain is a stock.
  - The consumer-price and care side views overlap the wage channel.
- **The net is not the published total.** The lane's −$509.23bn allocates the case and its social rows, with the
  wage transfer and item 11's stayers, to today's residents. The published fiscal-plus-social total on main case v9
  is $483.1–557.3bn on the 44.90M-person lineage (`sept24_propagation_2026_09_24/derived/oct16/real_costs_totals.json`,
  `joint_social_stack.ends`, `with_round1_social_fixes_bn`); the two are different objects.
- **Instrument.** The analysis ran through an LLM with known dispositions on charged topics
  ([caveat](../notes/llm-bias-caveat.md)). Every figure here comes from scripts the parent re-ran
  byte-identically (lane RESULT, final oct16 replay, IDENTICAL 239/239). The choices that move the result
  (financing, the case's range, geography, pooling) are each reported more than one way.

**Would change it:**
- a state-level fiscal account, which would settle the geography;
- a local-labor-market wage model;
- measured recipient keys for the social rows;
- the operator's choice of financing convention.

## Sources

- **Lane.** [`winners_losers_2026_09_24`](../infra/immigration-fiscal/winners_losers_2026_09_24/RESULT.md), section
  "v9 case (oct16)": `run_all.sh`, `winners_losers.py`, the P7 frames and the oct16 derived files [DATA].
- **Inputs.** Every input is pinned by SHA-256 in `inputs/p9_pins_oct16.json` and `derived/oct16/p7_inputs.json`
  (`source_pins`): the adopted main case (`main_case_2026_10_16`), the case's social pairing, the generation account
  and the income-split person frame.
- **Parent rerun, 2026-10-21.** `rerun_lane.py`: IDENTICAL 239/239, exit 0, 106 tests, after the two new social rows [CALCULATION].
- **Rulings.** The parent's rulings 1–7 are in the lane's RESULT, "Rulings and coordination notes
  applied". Ruling 7 makes the pooled count central.

## Revisions

- 2026-10-21 ([decision](../decisions/2026-10-21-business-crime-in-pairing.md)): the pairing now counts business
  crime at its net ($1.38 / 1.35bn at the case's ends) and commercial security against member victims ($1.90 /
  1.96bn), and the completion and item 16 people send crime in every crime row; the pairing moves from $479.6–553.7bn
  to $483.1–557.3bn. The lane allocates both new rows by national consumption, as passed to purchasers, inside §2's
  crime channel, which grows from −$48.4bn to −$52.0bn at central values. The net on today's residents moves from
  −$505.65bn to −$509.23bn (−$1,740 per other resident), and the share ahead falls to 2.70% / 4.51% / 7.90% from
  2.79% / 4.71% / 8.31%; every sensitivity row, cut and decile follows the lane's rebuilt `derived/oct16/` files.
  Who comes out ahead and behind is unchanged. Concept affected: who comes out ahead, and the social rows allocated.
- 2026-10-21 (main case v9, [decision](../decisions/2026-10-16-main-case-v9.md), e6dcde3c): the verdict and §§1–7
  follow the lane's oct16 run and its P7 method, which the memo had not yet taken. The claim changes: about one other
  resident in five no longer comes out ahead. At central values 2.79% / 4.71% / 8.31% do under tax shares, per-person
  cuts and programme-receipt cuts (a third rule, new here). Most of the change is the method, not v9: stationary
  financing charges the trust-fund accrual and the borrowed federal part to today's residents instead of leaving them
  to future payers; the pairing's complete social rows (PM2.5, crashes, fear, scale and the rest) are allocated; the
  non-members who stay in mixed households (item 11) get their own rows; and the central sits at the case's midpoint
  with the social rows' central values. On the same method v8 gave 2.61% / 4.49% / 8.03% and −$514.54bn (lane
  RESULT, "v8 case (oct15)"); v9 gives −$505.65bn. The ends now differ widely, 40–42% ahead at the low end and 3–4%
  at the high, because the social producers' ranges are paired with the case's ends. The September 24 tables are
  replaced by the oct16 tables; the September record stays in git and in the lane RESULT. Concept affected: who
  comes out ahead, the financing convention and the channel set (ladder 226).
- 2026-10-15 (corrected main case v8, [decision](../decisions/2026-10-15-main-case-v8.md)): the separate fiscal-plus-social total follows the current joint pairing. The lane's distribution/allocation results are left for the pending v8 rerun. Concept affected: the distinction between the allocation base and the complete published total.

- 2026-09-25 (morning): the operator adopted the school-dilution relabel as priced beside the account
  (decision option 2), so §6 lists it as kept out of every total rather than proposed. No figure
  changes. Concept affected: the status of the dilution row.
- 2026-09-25 (weekly audit §2): the elasticity sensitivity, the enumerated range and the
  mixed-household boundary are added under the sensitivity table. "A minority comes out ahead"
  holds in every variant computed; the precise share is conditional on the gross wage incidence,
  the financing rule and where state and local costs fall. [CALCULATION:
  [audit probe](../infra/immigration-fiscal/conceptual_audit_2026_09_25/README.md#distribution-probe),
  `_cache/sensitivity.csv`, which reproduces the published central exactly]
  [Decision](../decisions/2026-09-25-weekly-audit-corrections.md).
- 2026-09-26 (schools at full average cost, [decision](../decisions/2026-09-26-main-case-schools-full-cost.md)):
  the ledger now runs the new main case (fa1bd3a). The pooled share ahead falls to 20.5% / 19.0%
  (from 23.9% / 21.4%), the person count to 18.4% / 18.3%, and the fiscal channel rises to
  $275.0bn at central values. School dilution leaves the nets, since nothing is left unfunded at a
  response of 1. Who comes out ahead and who behind is unchanged. Concept affected: the share of
  other residents ahead and the nets by cut (ladder 226).
- 2026-09-28 (the September 27 case, [decision](../decisions/2026-09-27-main-case-capital-return-and-long-run-responses.md)): the ledger runs the new case (62f1e5a). The
  pooled share ahead falls to 17.8% / 17.0%, the person count to 16.9% / 16.9%, and taxpayers' fiscal
  channel is $349.3bn plus $5.1bn on capped programmes. Preferences became an attribution under
  proportional replacement. Who comes out ahead and who behind is unchanged. Concept affected: the share
  of other residents ahead and the nets by cut (ladder 226).
- 2026-09-28: the world ledger (ladder 250, e1910ec) builds the Mexico counterfactual this memo's group frame left out for G2 and bounds it for G3+; bracketed in §5. Concept affected: the group's own gain in the world frame.
- 2026-09-29 (cleanup, [decision](../decisions/2026-09-29-delete-superseded-and-cruft-docs.md)): the verdict states the
  September 27 run; the September 24 verdict and the schools-case update became one table of earlier cases;
  dated notes are folded into the text. §6 no longer calls the scale net and the consumption key proposed, and §7
  gives the current fiscal-plus-social total ($413.7–488.1bn, ladder 274). Concept affected: which run the memo
  states as current.
- 2026-09-29 (number drift audit): the pairing's upper end is $488.0bn (488.047), not $488.1bn, and the scale net is $13.7bn on the priced count ($13.9bn on the CPS count). Concept affected: none; rounding and count basis only.
- 2026-09-29, later (main case v4, [decision](../decisions/2026-09-29-main-case-v4.md), ladder 275): the verdict runs the main case of that date (858f77a). 17.9% / 17.1% of other residents come out ahead, pooled; the $74.9bn pension accrual falls on the future payers of Social Security and Medicare, so the social net on today's residents falls to −$360.6bn while the case rises. Landlords ahead 39–43% (pooled net −$524); California and Texas 97–98% behind. Concept affected: who comes out ahead, and who bears the pension accrual.
- 2026-10-05, later (main case v5, [decision](../decisions/2026-10-05-main-case-v5.md), ladder 281): the verdict runs main case v5 (c1c259ef). 17.6% / 16.9% of other residents come out ahead, pooled, and 16.7% / 16.8% with wages to the earner; taxpayers' fiscal channel is $416.4bn, the pension accrual $80.4bn and the social net on today's residents −$378.2bn. The group's rows count the 42.75M lineage, the 3.04M added descendants placed at the identified third-plus members' records; the September 29 verdict's figures are a column of the earlier-cases table, and the pairing, the debt legacy and the G3+ premium bound follow v5. Concept affected: who comes out ahead, and the group frame's count.
- 2026-10-07 (main case v6, [decision](../decisions/2026-10-07-main-case-v6.md), ladder 295): the verdict runs main case v6 (f2d96008). 17.5% / 16.8% of other residents come out ahead, pooled, and 16.7% under both with wages to the earner; taxpayers' fiscal channel is $415.9bn, the pension accrual $78.9bn, the borrowed part $13.2bn and the social net on today's residents −$378.6bn. The case falls $0.5bn at central values, but the accrual falls $1.5bn and the borrowed part rises $0.6bn, so today's residents carry $0.4bn more and the share slips. The group's rows place the 3.04M added descendants at the identified third-plus records of their own five-year age band. The October 5 verdict's figures are a column of the earlier-cases table; the pairing ($489.0–570.7bn) and the debt legacy ($31.8–44.2bn) follow v6, and the G3+ premium bound stays on v5 with the world ledger. §1 now names the run and the lineage, which it had not since September 29, and the preferences paragraph dates its 0.1-point move to the September 27 case. Concept affected: who comes out ahead, and the group frame's age placement.
- 2026-10-08: living text states only the live case, at the operator's request; earlier-case figures removed, recoverable at 0e0c5e28.
- 2026-10-08 (item T): §4's pointer to the California–Texas gaps leads with their item-T values, because the white-reference ledger's expanded account now charges the income tax the survey misses on the main case's keys (item T; [decision](../decisions/2026-10-07-ledger-item-t-income-tax-keys.md)): −$12,133 / −$7,479 → −$15,228 / −$9,267, with the survey-tax pair and the few-records caveat beside them. No figure of this memo's own changes. Concept affected: the pointer to the per-member geography gaps.
- 2026-10-14 (main case v7, [decision](../decisions/2026-10-14-main-case-v7.md)): the current verdict uses `oct14` (2204a2bc), with both case ends personal and the job-capital tax receipts included. Pooled, 19.6% / 18.7% of other residents come out ahead under tax shares / per-person cuts; with wages to the earner, 17.9% / 18.0%. The fiscal taxpayer channel is $372.2bn centrally and the social net on today's residents −$341.7bn; the minority-ahead conclusion holds. The dated September 24 tables remain a calculation record. Concept affected: the share ahead and the present/future financing allocation.
