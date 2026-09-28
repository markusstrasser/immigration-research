# Who wins and who loses

Date: 2026-09-25. The operator asked on 2026-09-24: "it would be good to track who loses and who
wins exactly". [MODEL / FRAMING-SENSITIVE] Three choices shape the result:
- how the fiscal cost is financed;
- where the state and local cost falls;
- whether a household's gains and costs are shared among its members.

Every figure below names the choice it uses.

**Update, 2026-09-28 (the September 27 case, $321.8–387.4bn; [decision](../decisions/2026-09-27-main-case-capital-return-and-long-run-responses.md)).** About one other
US resident in six now comes out ahead. Pooled within households, 17.8% are ahead under tax-share
financing and 17.0% under per-person cuts (schools case: 20.5% and 19.0%). Every choice at its least
costly value gives 24%, and at its most costly 11%; with wages going to the earner alone, 16.9% under both.
The fiscal channel now splits. Taxpayers carry $349.3bn at central values, 85% of it state and local and
$44.7bn of it the return on public capital, which is never borrowed. Rental assistance and LIHEAP
($5.1bn) fall on eligible households that go without the aid. The social net on today's residents is
−$386.6bn, or −$1,307 per other resident. Who comes out where does not change:
- behind: 97–99% in California and Texas, 98–99% of US-born adults with a high-school education or
  less, 90–92% of renters, and from 83% to over 99% of each decile in the bottom half;
- most often ahead: the top decile (31% under tax shares, 55% under per-person cuts) and landlords
  (37–42%), whose pooled net under tax shares falls to −$701 a year (was −$227).

Preferences are now an attribution under a stated proportional-replacement rule. White natives' part is
−$0.58bn, and other recipients in the same pools, mostly in admissions, carry −$0.97bn; "with proposed"
moves by 0.1 point. [CALCULATION: ledger lane, `--case sept27`, 62f1e5a; every old and new value in
`infra/immigration-fiscal/sept27_propagation_2026_09_27/derived/old_new_ledger.csv` (718 rows), 73cc30c]
[FRAMING-SENSITIVE]

**Update, 2026-09-26 (schools at full average cost, $258.5–292.0bn; [decision](../decisions/2026-09-26-main-case-schools-full-cost.md)).** About one other
US resident in five now comes out ahead. Pooled within households, 20.5% are ahead under tax-share
financing and 19.0% under per-person cuts (below: 23.9% and 21.4%). Every choice at its least
costly value gives 27%, and at its most costly 12%; with wages going to the earner alone, 18.4% and
18.3%. The fiscal channel is $275.0bn at central values (below: $223.4bn), 83% of it state and
local, and the social net on today's residents is −$314.4bn, or −$1,063 per other resident. Who
comes out where does not change:
- behind: 96–98% in California and Texas, 97–99% of US-born adults with a high-school education or
  less, 88–91% of renters, and from 81% to over 99% of each decile in the bottom half;
- most often ahead: the top decile (36% under tax shares, 57% under per-person cuts) and landlords
  (43–47%). Landlords' pooled net under tax shares turns negative, −$227 a year (was +$114).

School dilution leaves the nets, since nothing is left unfunded at a school response of 1, and the
consumption key sits inside the fiscal channel. The first-year budget response stays within 0.1 point of
the September 24 shares. The sections below keep the September 24 figures. [CALCULATION: ledger
lane, `--case sept26_schools`, fa1bd3a; every old and new value in
`infra/immigration-fiscal/sept26_propagation_2026_09_26/derived/old_new_ledger.csv` (643 rows),
d27dcb1] [FRAMING-SENSITIVE]

**Verdict:** About one other US resident in four or five comes out ahead of the Mexican-origin
group's presence, and the rest come out behind.
- Counting each household's gains and costs as shared among its members, 23.9% come out ahead if the
  fiscal cost is financed by tax shares, and 21.4% if by equal cuts per person.
- Setting every choice at its least costly value gives 30%, and at its most costly 14%.
- Giving wages to the earner alone, while taxes and rent stay shared, gives 20.1% and 19.9%.

The count runs person by person over the 295.8m other residents in CPS ASEC 2025. It covers the
adopted main case and the social items priced beside it, at central values.

Who comes out where:
- **Most often ahead:** households whose earners have some college or more and live outside
  California and Texas, especially at the top of the income distribution. In the top decile, 41% are
  ahead under tax-share financing and 60% under per-person cuts. About half of landlords are ahead.
- **Behind:**
  - nearly everyone in California and Texas (95–98%);
  - US-born adults with a high-school education or less (97–98%);
  - renters (87–90%);
  - the bottom half of the income distribution (77–99% behind).

[CALCULATION: [ledger lane](../infra/immigration-fiscal/winners_losers_2026_09_24/RESULT.md),
`winners_losers.py` → `derived/net_shares.csv`, `person_nets_by_cut.csv`; ladder 226]

## 1. Object and frame

The frame is the [complete annual account](immigration-complete-annual-account-2026-09-20.md) on the
main case adopted September 24 ($200.9–246.3bn). [2026-09-26, later: the lane now runs the schools case, $258.5–292.0bn;
see the update at the top.] It measures the effect of the 40.9m Mexican-origin
residents, all generations, on all other US residents in 2024. It compares the year with and without
the group.

A person is "ahead" when their sum over the priced channels is positive. Unpriced effects are not in
the count. The FAQ's rules for combining numbers apply: the channels below come from one frame and are
allocated, not added across objects.

Each channel goes to persons by its own key:
- **Fiscal cost** (inside the account, $223.4bn at central values):
  - The federal part financed today is split by federal tax share (a) or per person (b).
  - The state and local part is 81% of the cost. It stays in the states where the group lives, split
    by state and local taxes (a) or per person (b).
  - The deficit-financed federal part, $11.3bn, falls on future taxpayers and is not allocated to
    anyone alive today.
- **Wages** (inside the account): the account's production nest, split at high school or less (σ 2,
  ε ∞).
- **Rent** (beside the account): renters and landlords, by ACS income cells and state.
- **Crime victims' harm, congestion, unreimbursed hospital care, property crime and mobility** (beside
  the account): by the states where the group lives or drives, then by the income-split lane's keys
  within each state.

**Two ways to count persons.**
- **Person count:** wages go to the earner, while taxes and rent are shared within the household
  (SPM unit). A degree-holding earner can come out ahead while the children and a non-working spouse
  carry their shares of the household's taxes with no offsetting gain.
- **Pooled count** (central here): each household's amounts are added up and shared among its
  members, as the income-split lane ([ladder 194](immigration-real-fiscal-and-social-costs-2026-09-23.md))
  already ranks them. The pooled amount is the household's person-weighted mean, which keeps every
  channel's total exact.

Pooling moves 28.1m people ahead and 16.8m behind under (a). They are mostly children and non-working
adults in households that gain, and earners in households that lose.

The lane reuses the income-split lane's person frame. It reproduces that lane's September 23 and
September 24 tables to 2.8e-14bn.

## 2. Who gains and who loses, by channel

The table gives $bn a year at central values, signed from the named people's side. Per-person
figures divide by the people who have a nonzero amount. It does not depend on how persons are counted.
[CALCULATION: `derived/winners_losers_table.csv`]

| Who | Gain or loss | $bn a year | People (m) | $ per person | Channel | Inside or beside the account |
|---|---|---:|---:|---:|---|---|
| Taxpayers today: federal tax share, and state and local taxes in the group's states (a) | loss | −212.1 | 293.2 | −723 | fiscal cost | inside |
| Every other resident equally; the state and local part within the group's states (b) | loss | −212.1 | 295.8 | −717 | fiscal cost | inside |
| Future federal taxpayers (the deficit-financed part) | loss | −11.3 | — | — | fiscal cost | inside, not allocated |
| Workers with some college or more | gain | +95.8 | 107.0 | +895 | wages after tax | inside |
| Workers with high school or less | loss | −96.0 | 47.1 | −2,037 | wages after tax | inside |
| Renter households | loss | −33.9 | 85.0 | −398 | rent | beside |
| Landlords | gain | +37.4 | 24.5 | +1,524 | rent receipts | beside |
| People 12 and over, by victimization risk, in the group's states | loss | −30.9 | 256.7 | −121 | crime victims' harm | beside |
| Metropolitan commuters, by the states of the congested urban areas | loss | −19.2 | 133.5 | −144 | road congestion | beside |
| Privately insured, in the states of the group's uninsured | loss | −4.4 | 199.5 | −22 | unreimbursed hospital care | beside |
| Households in the group's states | loss | −1.3 | 295.8 | −4 | property crime (proxy) | beside |
| US-born men with high school or less, and all workers | gain | +0.7 | 154.1 | +4 | mobility insurance | beside |

Inside the account, taxes and wages come to −$223.6bn: −$212.3bn on today's residents and −$11.3bn
on future taxpayers. The wage channel nets to −$0.2bn, but it moves $96bn a year from workers with
high school or less to workers with more schooling. Allocated to today's residents, the account and
the social items come to −$263.9bn, a mean of −$892 per other resident. The median is −$377 under (a)
and −$505 under (b), pooled.

## 3. Person nets by the cuts that separate them

The social net is the account plus the social items beside it. Net (a) is in $ per person a year,
pooled. The next two columns give the share ahead, pooled, under each convention. The last column
gives the share ahead under the person count, (a).
[CALCULATION: `derived/person_nets_by_cut.csv`, columns `net_social_*_spm_pooled_*`]

| Cut | People (m) | Net (a) | Ahead (a) | Ahead (b) | Person count, ahead (a) |
|---|---:|---:|---:|---:|---:|
| California | 26.3 | −2,751 | 3.3% | 4.7% | 3.5% |
| Texas | 21.2 | −2,661 | 2.2% | 3.5% | 2.3% |
| All states except California and Texas | 248.3 | −544 | 27.9% | 24.7% | 23.3% |
| US-born, below high school, 25+ | 8.5 | −981 | 2.8% | 1.7% | 0.7% |
| US-born, high school, 25+ | 48.2 | −1,460 | 3.2% | 2.7% | 1.1% |
| US-born, some college, 25+ | 47.3 | −657 | 25.6% | 21.3% | 33.7% |
| US-born, BA or more, 25+ | 70.4 | −708 | 37.4% | 39.4% | 43.3% |
| Other foreign-born, below high school, 25+ | 4.6 | −1,389 | 3.0% | 1.7% | 0.3% |
| Other foreign-born, high school, 25+ | 8.2 | −1,666 | 5.3% | 3.4% | 0.9% |
| Other foreign-born, some college, 25+ | 5.5 | −832 | 29.3% | 21.1% | 36.6% |
| Other foreign-born, BA or more, 25+ | 16.9 | −1,024 | 37.1% | 36.0% | 40.1% |
| Under 25 | 86.3 | −724 | 25.4% | 19.0% | 4.0% |
| Renters | 86.8 | −1,269 | 13.3% | 10.5% | 13.1% |
| Owners without rental income | 184.5 | −849 | 25.5% | 22.6% | 20.4% |
| Landlords | 24.5 | +114 | 48.8% | 50.5% | 41.8% |
| Under 18 | 60.9 | −629 | 27.8% | 20.1% | 1.5% |
| 18–64 | 176.7 | −1,037 | 26.6% | 25.0% | 29.9% |
| 65 and over | 58.3 | −727 | 11.5% | 11.8% | 9.6% |
| Workers in construction | 9.8 | −1,504 | 19.6% | 17.9% | 27.1% |
| Workers in restaurants | 8.5 | −1,072 | 18.4% | 14.5% | 16.8% |
| Workers in agriculture | 1.7 | −963 | 21.5% | 21.9% | 26.4% |
| Workers in landscaping | 1.2 | −1,064 | 15.3% | 12.7% | 18.5% |
| Workers in other industries | 131.9 | −1,093 | 31.1% | 30.7% | 39.0% |
| Not working | 142.7 | −651 | 17.9% | 13.5% | 2.2% |
| Non-Hispanic white | 191.8 | −828 | 25.9% | 24.2% | 22.0% |
| Non-Hispanic Black | 41.9 | −810 | 18.3% | 13.7% | 16.7% |
| Non-Hispanic Asian | 22.7 | −1,286 | 25.9% | 24.9% | 20.0% |
| Hispanic, other than Mexican origin | 28.1 | −1,075 | 18.6% | 13.5% | 14.7% |
| Other race | 11.4 | −1,032 | 18.3% | 15.5% | 12.4% |
| Women / men | 150.7 / 145.1 | −828 / −959 | 23.7 / 24.0% | 21.1 / 21.7% | 19.1 / 21.0% |

Under the person count, Arizona's 5.1m other residents are $2,832 behind on average, and 3.2% of them
are ahead (lane RESULT). Two-way cells under the person count: US-born degree holders who are also
landlords (8.7m) are ahead in 58% (a) to 66% (b) of cases. US-born adults with a high-school
education in California and Texas are behind by $3,810–4,530 [CALCULATION: `derived/winner_cells.csv`].

**By income.** The table covers SPM deciles of other residents. Net is the social net in $ per
person, the same under both counts; the share ahead is pooled.
[CALCULATION: `person_nets_by_cut.csv`, cut `decile`]

| Decile | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Net (a) | −559 | −627 | −704 | −789 | −826 | −838 | −908 | −928 | −937 | −1,804 |
| Ahead (a) | 2.8% | 7.4% | 12.2% | 17.4% | 22.6% | 29.1% | 30.1% | 36.6% | 39.3% | 41.3% |
| Net (b) | −1,126 | −1,081 | −1,135 | −1,143 | −1,113 | −1,039 | −1,026 | −890 | −688 | +319 |
| Ahead (b) | 0.5% | 0.9% | 2.7% | 6.8% | 12.3% | 20.6% | 28.1% | 38.2% | 44.3% | 59.6% |

- **Tax-share financing (a).** The top decile pays the most dollars. As a share of SPM resources,
  though, the social net is four times heavier in the bottom quintile: −6.2% there against −1.5% in
  the top (lane RESULT, quintile table). Rent, wages and crime fall toward the bottom, while landlord
  receipts and wage gains go to the top.
- **Per-person cuts (b).** The top decile gains on average (+$319), and it is the only decile where
  most people come out ahead (60%).

## 4. What drives the split

- **Geography.** State and local budgets carry 81% of the fiscal cost, and the lane charges it to the
  states where the group lives [INFERENCE: a state-level fiscal account would test it].
  - The average other resident is $2,660–2,830 a year behind in California, Texas and Arizona, and
    $544 elsewhere.
  - Charged to the whole country instead, California's net per person moves from −$2,751 to −$1,359,
    and the rest of the country's from −$544 to −$810. The share ahead (person count) falls to 13%.
  - Geography is the largest single choice in the result.
  - These are other residents' shares of the account's cost, a financing allocation. They are not the
    per-member gaps of the [California–Texas memo](immigration-california-texas-fiscal-geography-2026-09-21.md)
    (−$12,133 / −$7,479 against local whites), and the two are never combined (FAQ, "Before combining
    numbers").
- **Schooling.** The account's production nest moves $96bn a year of after-tax wages from workers
  with high school or less to workers with more schooling. That puts US-born adults with high school
  or less 97–99% behind. Degree holders are ahead more often than any other schooling group (37–39%
  pooled).
  - The nest is the account's calibration, not a measured wage effect.
  - Measured effects on less-educated natives are disputed in both directions
    ([real costs](immigration-real-fiscal-and-social-costs-2026-09-23.md) §4).
- **Tenure.** Renters pay $33.9bn more in rent and landlords receive $37.4bn more. Rent is the channel
  that lifts landlords to a positive average: +$114 under (a) and +$740 under (b).
- **Household composition.** Pooled, children are ahead as often as working-age adults (28% against
  27% under (a)). People 65 and over are ahead in 12% of cases: they gain little in wages and carry
  their share of taxes.

**Sensitivities.** Share of other residents ahead, social net, central values. [CALCULATION:
`net_shares.csv`, columns `unit` and `stack`]

[2026-09-25, weekly audit §2: the rows below move one choice at a time or stack choices by their
dollars. The production nest's substitution elasticity alone moves the pooled share ahead from
29.2% (σ 1.5) through 23.9% (σ 2, central) to 18.7% (σ 2.5) under tax shares, and 26.2%, 21.4% and
17.7% under per-person cuts, while the net assigned to these people barely moves (−$260.1bn to
−$266.1bn): the wage channel's gross gains ($95.8bn) and losses ($96.0bn) almost cancel, so a
total that reconciles says little about who is ahead. The least- and most-costly rows stack dollar
extremes; enumerating the existing channel choices gives 13.9–30.5% under tax shares and
13.8–27.2% under per-person cuts. Pooling shares amounts among other-resident members only, and
6.97m other residents live in households with a group member whose resources it leaves out. See
Revisions.]

| Variant | Pooled (a) | Pooled (b) | Person count (a) | Person count (b) |
|---|---:|---:|---:|---:|
| Central | 23.9% | 21.4% | 20.1% | 19.9% |
| Every choice least costly | 30.0% | 27.0% | 24.0% | 23.7% |
| Every choice most costly | 13.9% | 13.8% | 14.0% | 14.1% |
| Account only: fiscal and wages, no social items | 28.5% | 23.5% | 22.4% | 21.6% |
| With the items kept out of the totals (§6; the lane's "with proposed" net), central | 20.8% | 20.3% | 20.6% | 20.5% |
| The same, least / most costly | 36.6 / 6.1% | 35.7 / 8.2% | 31.6 / 10.7% | 30.8 / 10.8% |
| State and local cost charged nationally | — | — | 13.0% | 12.7% |
| Housing at the national-uniform central (net +$0.71bn, not +$3.51bn) | — | — | 18.4% | 18.5% |
| Victims' harm on the custody footing ($32.34bn, not $30.93bn) | — | — | 20.0% | 19.8% |

The last three variants were run on the person count only. Pooling each household's amounts with a
plain mean instead of the weighted mean would put 24.3% and 21.7% ahead. That rule moves the totals
by $1.0bn, so it fails the lane's closure gate.

## 5. The group itself

This section is beside the account, and none of it is netted against other residents' rows.
[CALCULATION: `derived/group_frame.csv`]

| Item | $bn a year (range) | Basis |
|---|---:|---|
| Direct fiscal transfer received (the engine's direct response, sign flipped) | +234.7 (214.2–255.1) | at the band ends |
| First generation's market gain over its earnings in Mexico | +224.6 (196.5–242.8) | place premium Re 2.46 (2.08–2.79) × $378.4bn of US earnings |
| Wage competition among the group's own workers with high school or less | −20.8 (ε ∞); −37.9 (ε 3) | account nest × members' CPS earnings |
| Wage gain of the group's own workers with some college or more | +5.8 (ε ∞); +5.9 (ε 3) | same |
| Victims inside the group, excluded from the victim lane | −20.1 | the victim lane's rows, on its equal footing |

Notes on the table:
- **Place premium.** The source reads: "the average emigrant comes from the 56th percentile of
  residual wages, suggesting that Ro/Re = 1.03 … so that Re ≈ 2.46" [SOURCE: Clemens, Montenegro &
  Pritchett, "The Place Premium", HKS RWP09-004, sec. 3.3 and Table 8, quote verified in the corpus].
  The gain assumes the same employment and hours in both countries [INFERENCE]. The second and
  third-plus generations have no counterfactual in Mexico, and none is invented. [2026-09-28: the
  [world ledger](../infra/immigration-fiscal/world_ledger_2026_09_27/RESULT.md) (ladder 250) builds
  one for G2: the same people raised in Mexico by parents with the same schooling who stayed, a
  $252bn premium ($241–260bn). G3+ is bounded between no premium and $253bn. On gross pay and
  measured employment in both places, G1's premium is $263bn ($242–285bn), against $224.6bn here.]
- **Remittances.** Mexico received $62.8bn of remittances from the United States in 2024 [SOURCE:
  Banxico SIE table CE167, US-origin receipts, revised]. The corridor carries more than the CPS
  households send at surveyed amounts ([outside checks](immigration-outside-checks-2026-09-24.md),
  section "Consumption taxes").
- **By generation.** The account's split by generation is a cost to others, not a gain to the group,
  and it has no reference group. It is in
  [the account by generation](immigration-adopted-account-by-generation-2026-09-25.md) (ladder 224).

## 6. Items out of the totals, and rows on other counterfactuals

**Items kept out of every total** enter only the "with proposed" net (§4), never the verdict:
- **School dilution, −$20.1bn.** Instruction and support together: a present value of other
  residents' pupils' lifetime earnings, not annual cash. The operator adopted it on 2026-09-25 as
  priced beside the account; it stays out of every total unless option 3 is chosen
  ([decision](../decisions/2026-09-25-school-dilution-priced-beside.md)).
- **Preferences, the group's part, −$0.6bn** (proposed).
- **City size and schooling mix, +$13.9bn** (ladder 201, proposed).

The consumption-key correction (ladder 225, proposed) would lower the fiscal cost by $4.1bn. It is
listed in the lane's registry and not allocated.

**Rows on other counterfactuals.** Three sister lanes price effects against other comparisons:
- movers: the movers staying in California;
- vending: California before SB 946;
- compliance: workers paid on the books.

A row enters a net only if its counterfactual is the group's absence. These rows therefore sit in the
role table (`derived/sister_other_counterfactuals.csv`) and in no net. Applying that rule moved the
"with proposed" total from −$270.97bn to −$270.62bn and no share by more than 0.01 point.

## 7. Limits

- **One year.** The count covers the people alive in 2024. It cannot say what today's children will
  pay or receive as adults.
- **State and local incidence.** It uses national ITEP rates by income group, not state rates;
  Texas's taxes are more regressive.
- **Wages.** They are national. The nest has no local labor markets, and a local model would
  concentrate the wage loss in the group's states.
- **Survey gaps.** CPS has no school type, no gross rents and few restaurant owners. Landlords are
  assumed to live in the state where the rent is paid.
- **Pooling.** It treats each household as sharing everything and measures nothing about how families
  actually share. The truth for any family lies between the two counts.
- **Kept out of every net.**
  - The debt legacy's interest ($28.3–36.4bn) is a different object. [2026-09-26, later: $30.1–37.9bn on the
    schools case.] [2026-09-28: $30.9–41.6bn on the September 27 case.]
  - The owners' home-value gain is a stock ($1.3–2.9tn).
  - The consumer-price and care side views overlap the wage channel.
- **The allocation base is not a total.** The lane's allocation base, the adopted fiscal band plus
  decision 4's victims figure, mixes crime footings. The published fiscal-plus-social range stays
  $248–304bn: $247.7–298.4bn on the equal footing and $253.4–304.0bn on the custody footing
  ([real costs](immigration-real-fiscal-and-social-costs-2026-09-23.md)). [2026-09-26, later: on the
  schools case $305–350bn: $305.3–344.0bn and $311.0–349.7bn (4e66adb).] [2026-09-28: on the September 27
  case $363–438bn: $363.4–432.2bn and $369.2–438.0bn (73cc30c).] [2026-09-28, later: with fear, security
  and schools $371–446bn: $371.3–440.1bn and $377.1–445.9bn; the three items are not allocated
  ([decision](../decisions/2026-09-28-social-items-fear-security-schools.md)).]

- **Instrument.** The analysis ran through an LLM with known dispositions on charged topics
  ([caveat](../notes/llm-bias-caveat.md)). Every figure here comes from scripts the parent re-ran
  byte-identically. The three choices that move the result (geography, financing, pooling) are
  each reported both ways.

**Would change it:**
- a state-level fiscal account, which would settle the geography;
- a local-labor-market wage model;
- the operator's choice of financing convention and crime footing.

## Sources

- **Lane.** [`winners_losers_2026_09_24`](../infra/immigration-fiscal/winners_losers_2026_09_24/RESULT.md):
  the brief, `winners_losers.py`, `specs.cjs`, 12 tests and 23 derived CSV and JSON files [DATA].
- **Inputs.** Every input is pinned by sha256 in `derived/sources_manifest.csv`. They are:
  - the adopted main case (`main_case_2026_09_24`);
  - the income-split lane, read from git at 7ec7144;
  - the debt lane's federal split;
  - the housing, crime, congestion, unreimbursed-care, mobility, preference and city-size lanes;
  - the sister lanes' `winners_losers_rows.csv`.
- **Parent rerun, 2026-09-25.** `specs.cjs`, `winners_losers.py` (443 gates) and the 12 tests all exit
  0, and all 23 derived files are byte-identical. The input lanes are untouched. [CALCULATION]
- **Rulings.** The parent's rulings 1–7 are in the lane's RESULT, "Rulings and coordination notes
  applied". Ruling 7 makes the pooled count central.

## Revisions

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
