**Verdict:** [2026-09-28: the scripts now default to the September 27 case (`--case sept27`, $321.8–387.4bn, pins 78766c2, e03450b, 8654a0c), and `derived/` holds that run. Pooled within SPM units, 17.8% of other residents come out ahead under tax-share financing and 17.0% under per-person cuts (schools case: 20.5%, 19.0%), 11.1–24.0% across the stacks under (a); the person count gives 16.9% under both. The fiscal channel now has three financing parts. Taxpayers carry $349.3bn at central values, 85% of it state and local; of that, $44.7bn is the return on public capital, enterprise capital included, which is never borrowed. The capped programs, $5.1bn of rental assistance and LIHEAP, fall on eligible households without the aid under both conventions (`displaced_beneficiaries`). The social net on today's residents is −$386.6bn. Congestion is the long-run re-derivation, $13.0bn central ($2.0–30.8bn). Where the uniform lane cut outweighs the group's traffic, other residents gain: in 18–27 of the 50 states and DC across the levels, 22 at central values ($0.9bn). The preferences row is an attribution under a stated replacement rule; the DBE premium's part already in the fiscal channel ($2.6m) is netted, and the rule's other recipients' part (−$0.97bn) sits beside it in "with proposed". `specs.cjs` writes each capital component as a line `capital_<id>`. `--case sept26_schools` rewrites fa1bd3a's files byte for byte, and `sept26` and `sept24` reproduce theirs. Old → new: `../sept27_propagation_2026_09_27/RESULT_ledger.md`.] [2026-09-26, later: the scripts now default to the main case with schools at full cost (`--case sept26_schools`, $258.5–292.0bn), and `derived/` holds that run. Pooled within SPM units, 20.5% of other residents come out ahead under tax-share financing and 19.0% under per-person cuts (text below: 23.9%, 21.4%), 11.9–27.1% across the stacks under (a); the person count gives 18.4% and 18.3% (below: 20.1%, 19.9%). The fiscal channel is $275.0bn at central values (below: $223.4bn), 83% of it state and local, and the social net on today's residents is −$314.4bn (below: −$263.9bn). School dilution stays in the role table, since nothing is left unfunded at a school response of 1; the consumption key is inside the fiscal channel. `--case sept26` gives the one-year scenario (23.9%, 21.4%). `--case sept24` reproduces the run described below byte for byte. Old → new: `../sept26_propagation_2026_09_26/RESULT_ledger.md`.] [Parent ruling 7, 2026-09-25: the count pooled within SPM units is central: 23.9% ahead under (a) and 21.4% under (b), 13.9–30.0% across the stacks. The person count gives wages to the earner but shares taxes and rent within the unit, so it counts children and non-earners in winning units as behind by construction; it stays as the alternative. Memo: [who wins and who loses](../../../research/immigration-winners-and-losers-2026-09-25.md), ladder 226.] About one other resident in five comes out ahead of the Mexican-origin group's presence and
four in five come out behind. The person count ("wages to the earner, taxes and rent shared within the
unit") puts 20.1% ahead with tax-share financing (a) and 19.9% with per-person cuts (b). Pooling every
amount within each SPM unit raises that to 23.9% under (a) and 21.4% under (b). Under (a), 28m people,
mostly children and non-working adults in units that gain, move ahead, and 17m, nearly all earners in
units that lose, move behind. The person count stays central until the parent chooses. The count covers
the adopted account plus the social items beside it, at central values; stacking every choice low or
every choice high gives 14–24%. This is the final run, with every sister lane final. All of the parent's
rulings are applied (tables below). Before them the shares were 19.9% and 19.8%, so together the rulings
move the person count by about 0.2 points or less. The consumption lane's proposed key, −$4.1bn on the
fiscal total, is listed in the registry and kept out of every net and of the adopted total.
[CALCULATION: `winners_losers.py` → `derived/net_shares.csv`, `derived/pooling_moves.csv`]

- **Winners:** mostly workers with some college or more who live outside California, Texas and Arizona,
  and landlords. Among US-born degree holders who are also landlords, 58–66% are ahead.
- **Losers:** adults with high school or less (99% behind), renters, and nearly everyone in California,
  Texas and Arizona. In those three states the average other resident is $2,660–2,830 a year behind; in
  all states other than California and Texas, $544.
- **Why geography separates them:** state and local budgets carry 81% of the fiscal cost, and they carry
  it where the group lives.
- **Future taxpayers:** the federal deficit-financed part, $11.3bn a year, falls on them and is not
  allocated to anyone living today.

## Rulings and coordination notes applied

| Item | Before | Now | Effect on the share ahead, (a) / (b) |
|---|---|---|---|
| 1. Victims' harm | $34.58bn, a hybrid this lane built (30.93 × 32.34 / 28.92) | $30.93bn central (decision 4's figure), each row's footing named; $28.92bn and $32.34bn as allocated variants | all items together: 19.9 → 20.1% / 19.8 → 19.9%; the custody footing gives 20.0% / 19.8% |
| 2. Housing | metro-local arm's own low / central / high (net 2.30 / 3.51 / 5.17) | ladder 190: central 3.51 (metro-local), national-uniform 0.71 as a variant, low and high the long-run grid's extremes (−0.38, +9.40) | central unchanged; 0.71 instead gives 18.5% / 18.5% |
| 3. Debt legacy | Sept 23 files at b42efdc: interest $30.5–38.9bn | Sept 24 files at 7ec7144: $28.3–36.4bn; b42efdc stays the method's positive control | none (never added) |
| 3. Federal part, central convention | this lane's split of the corrections: $32.25bn / $52.20bn | the debt lane's split: $31.98bn / $51.86bn | not separated; $0.27–0.34bn moves from the federal to the state-local part |
| 4. Rows 8 and 10 | row 8 at 0, row 10 at family and general assistance | the debt lane's per-correction file (row 8 +$0.03bn federal, row 10 $0.00bn) | inside item 3 |
| Note 2. Direct response A | engine run (`specs.cjs`) | `fiscal_totals("sept24")` at 7ec7144, the base lane's definition | +4.9e-5 / −3.4e-5bn at the band ends |
| Notes 1–2. Regression targets | working-tree-safe pin 5b8957e | fixed commits: 5b8957e (Sept 23) and 7ec7144 (Sept 24) | none |
| Sister counterfactual rule (2026-09-25) | movers' and vending's rows allocated in "with proposed" (−0.66 and +0.31) | only rows on the group's (or its pupils') absence enter a net, gated; movers, vending and compliance sit in the role table only; dilution stays in "with proposed", labelled a present value of lifetime earnings | with proposed 20.57 → 20.58% / 20.51 → 20.51%; social net none |
| Generations (2026-09-25) | no split | the account's own split with no reference group (NAS convention), in the group frame only | none (never netted) |
| Consumption key (2026-09-25) | sister lane pending | registry row, "proposed change to the account's consumption key, −$4.1bn on the fiscal total"; never in a net or the adopted total | none |
| 5. Crime-footing pairing (2026-09-25) | `account_plus_social`, $252.5–297.9bn, shown as a total | relabelled "allocation base: adopted fiscal band + decision 4 victims (mixed footing), not a published total"; totals quoted from the published pairing, $247.7–298.4bn (equal footing) and $253.4–304.0bn (custody footing), range $248–304bn; the person nets keep decision 4's $30.93bn | none |
| 6. SPM-unit pooling (2026-09-25) | person count only | a pooled variant of every net, stack and convention (`unit` in `net_shares.csv`; pooled columns in `person_nets_by_cut.csv`); the person count stays central | a variant: social net 20.1 → 23.9% / 19.9 → 21.4% |
| Data fix: remittances (2026-09-25) | $64.7bn, "Banxico, all US senders" (the unrevised total from all countries) | $62.8bn, Banxico CE167, US-origin receipts, revised | none (group frame, context) |

**Winner shares before and after the rulings.** The share of other residents who come out ahead, (a) /
(b). Of the run before the rulings, only its reported shares (one decimal), its social stacks (reported as
one range, 15–24%) and the (b) rows of its with-proposed net survive. After 01:15 only the counterfactual
rule changed a person-count share. Ruling 5 changes labels and quoted totals, and ruling 6 adds a variant.
[CALCULATION: `derived/net_shares.csv`; the 01:15 run's copy was kept before the counterfactual rule]

| Net | Before the rulings (00:30) | After rulings 1–4 and the notes (01:15) | Final (02:11) |
|---|---:|---:|---:|
| Social net, central (the verdict) | 19.9 / 19.8% | 20.06 / 19.87% | 20.06 / 19.87% |
| Social net, every choice least costly | 24% | 23.96 / 23.73% | 23.96 / 23.73% |
| Social net, every choice most costly | 15% | 13.98 / 14.10% | 13.98 / 14.10% |
| With proposed, central | 20.5 / 20.4% | 20.57 / 20.51% | 20.58 / 20.51% |
| With proposed, least costly | — / 30.77% | 31.64 / 30.80% | 31.63 / 30.79% |
| With proposed, most costly | — / 10.99% | 10.67 / 10.76% | 10.68 / 10.76% |
| Social net, central, SPM units pooled (ruling 6 variant) | — | — | 23.87 / 21.39% |

**Federal split: where the old one differed.** The old split applied the September 23 per-line
fractions and split the lane constants itself. Against the debt lane's split, at the low and high ends:

- shelter: −$0.21bn and −$0.23bn. This lane had put it at zero federal; the debt lane keys it to its
  income-security, housing, general-government and health lines.
- row 9: −$0.09bn and −$0.10bn. The debt lane gives $0.25bn of it to Medicare, which is 100% federal.
- row 8: +$0.03bn.
- care, row 10 and the small items: $0.00bn. Care is 0.797 federal in both: the debt lane puts hours taxes
  at the receipts' federal share, 0.884, and elder care at Medicaid's, 0.640. The 0.884 in its
  `summary.json` is the omitted benefits' fraction, which is now mobility only.
- the other lines' September 24 fractions: −$0.01bn and −$0.04bn.

[DATA: `debt_legacy_2026_09_23/derived/corrections_federal_split_2024.csv` (untracked at run time),
`federal_split_2024*.csv` at 7ec7144]

## Who gains and who loses

Central values, $bn a year, 2024. Signs are from the named people's side; per-person figures divide by
the people with a nonzero amount. [CALCULATION: `derived/winners_losers_table.csv`]

| Who | Gain or loss | $bn/yr | People (m) | $/person | Channel | Basis | Inside or beside |
|---|---|---:|---:|---:|---|---|---|
| Taxpayers today, by federal tax share and by state-local taxes in the group's states (a) | loss | −212.1 | 293.2 | −723 | fiscal cost | measured budgets, modelled response | inside |
| Every other resident equally; the state-local part within the group's states (b) | loss | −212.1 | 295.8 | −717 | fiscal cost | same | inside |
| Future federal taxpayers (deficit-financed part) | loss | −11.3 | — | — | fiscal cost | measured deficit share | inside, not allocated [FRAMING-SENSITIVE] |
| Workers with some college or more | gain | +95.8 | 107.0 | +895 | wages after tax | modelled (σ 2, ε ∞) | inside |
| Workers with high school or less | loss | −96.0 | 47.1 | −2,037 | wages after tax | modelled | inside |
| Renter households | loss | −33.9 | 85.0 | −398 | rent | measured rents, modelled elasticity | beside |
| Landlords | gain | +37.4 | 24.5 | +1,524 | rent receipts | same | beside |
| People 12+, by victimisation risk, in the group's states | loss | −30.9 | 256.7 | −121 | crime victims' harm | measured incidents, modelled prices | beside |
| Metropolitan commuters, by the urban areas' states | loss | −19.2 | 133.5 | −144 | road congestion | measured traffic shares, modelled delay | beside |
| Privately insured, in the states with the group's uninsured | loss | −4.4 | 199.5 | −22 | unreimbursed hospital care | measured uninsured share, assumed use | beside |
| Households in the group's states | loss | −1.3 | 295.8 | −4 | property crime | proxy | beside |
| US-born men with high school or less; all workers | gain | +0.7 | 154.1 | +4 | mobility insurance, Borjas's gain | modelled | beside |
| US-born non-Hispanic whites | loss | −0.6 | 182.5 | −3 | preferences, Mexican-origin beneficiaries' part | modelled, weak evidence | beside (proposed) |
| Workers in the group's metros | gain | +8.0 | 154.1 | +52 | city size and schooling mix, earnings part | one regression | beside (proposed) |

Taxes and wages are inside the account. In total they come to −$223.6bn: −$212.3bn falls on today's
residents and −$11.3bn on future taxpayers. The wage channel's net is −$0.2bn, but it moves $96bn from
workers with high school or less to workers with more schooling.

## Person nets by the cuts that separate them

The net is the social net: the account plus the social items beside it, at central values. It is given in
$ per person a year, with the share of people who come out ahead. (a) is tax-share financing and (b) is
per-person cuts [FRAMING-SENSITIVE]. [CALCULATION: `derived/person_nets_by_cut.csv`, `derived/cuts.csv`]

| Cut | People (m) | Net (a) | Ahead (a) | Net (b) | Ahead (b) |
|---|---:|---:|---:|---:|---:|
| California | 26.3 | −2,751 | 3.5% | −2,712 | 5.0% |
| Texas | 21.2 | −2,661 | 2.3% | −2,653 | 3.9% |
| Arizona | 5.1 | −2,832 | 3.2% | −2,811 | 4.1% |
| All states except CA and TX | 248.3 | −544 | 23.3% | −549 | 22.8% |
| High school, US-born, 25+ | 48.2 | −1,985 | 1.1% | −2,123 | 1.0% |
| Below high school, US-born, 25+ | 8.5 | −1,184 | 0.7% | −1,462 | 0.6% |
| Some college, US-born, 25+ | 47.3 | −444 | 33.7% | −524 | 30.2% |
| BA+, US-born, 25+ | 70.4 | −433 | 43.3% | −47 | 46.0% |
| BA+, other foreign-born, 25+ | 16.9 | −762 | 40.1% | −418 | 40.6% |
| Renters | 86.8 | −1,269 | 13.1% | −1,478 | 11.8% |
| Owners without rental income | 184.5 | −849 | 20.4% | −833 | 20.4% |
| Landlords | 24.5 | +114 | 41.8% | +740 | 44.7% |
| Construction workers | 9.8 | −2,033 | 27.1% | −1,988 | 26.4% |
| Restaurant workers | 8.5 | −1,211 | 16.8% | −1,368 | 12.9% |
| Not working | 142.7 | −610 | 2.2% | −799 | 2.2% |
| Under 18 / 18–64 / 65+ | 60.9 / 176.7 / 58.3 | −607 / −1,051 / −707 | 1.5 / 29.9 / 9.6% | −785 / −976 / −748 | 1.3 / 29.5 / 10.2% |

Two-way cells sharpen the picture [CALCULATION: `derived/winner_cells.csv`]:

- **Most often ahead:** US-born BA+ landlords (8.7m) are ahead in 58% of cases under (a), with a mean of
  +$804, and in 66% under (b), with a mean of +$1,881.
- **Top decile:** top-decile landlords are ahead in 47% of cases under (a) and 66% under (b).
- **Most often behind:** almost all California renters are behind, at a mean of −$3,799 under (a) and
  −$4,355 under (b). US-born adults with a high-school education in California and Texas are behind by
  $3,810–4,530.

The greedy tree splits first on work, then on schooling, then on state. Its largest winning leaf is
workers other than US-born high-school graduates, outside California and Texas: 105m people, 53% of them
ahead under (a).
[CALCULATION: `derived/winners_tree.csv`]

**By income** (SPM quintiles of other residents, $ per person a year, central):

| | Q1 | Q2 | Q3 | Q4 | Q5 |
|---|---:|---:|---:|---:|---:|
| Fiscal (a) | −164 | −280 | −439 | −695 | −2,007 |
| Fiscal (b) | −674 | −672 | −683 | −735 | −821 |
| Wages | −105 | −215 | −163 | −6 | +485 |
| Renters + landlords | −121 | −89 | −64 | −32 | +366 |
| Crime victims | −160 | −99 | −86 | −85 | −93 |
| Congestion | −32 | −49 | −63 | −80 | −100 |
| **Social net (a)** | **−593** | **−747** | **−832** | **−918** | **−1,370** |
| **Social net (b)** | **−1,103** | **−1,139** | **−1,076** | **−958** | **−184** |
| Share ahead (a) / (b) | 4.8 / 2.1% | 13.0 / 8.6% | 21.5 / 18.5% | 28.1 / 28.7% | 32.9 / 41.6% |
| Social net (a) as % of SPM resources | −6.2% | −3.9% | −2.9% | −2.1% | −1.5% |

Under tax-share financing the top quintile pays the most dollars, but as a share of resources the burden
is still four times heavier at the bottom. That is because rent, wages and crime fall on the bottom
while landlord receipts and wage gains go to the top.

**Sensitivities** (social net, central; share ahead under (a) / (b)) [CALCULATION: `net_shares.csv`]:

| Variant | Ahead (a) | Ahead (b) |
|---|---:|---:|
| Central: person count ("wages to the earner, taxes and rent shared within the unit") | 20.1% | 19.9% |
| SPM units pooled: social net | 23.9% | 21.4% |
| SPM units pooled: account net (person count 22.4% / 21.6%) | 28.5% | 23.5% |
| SPM units pooled: with proposed (person count 20.6% / 20.5%) | 20.8% | 20.3% |
| Fiscal cost pooled nationally, no state geography | 13.0% | 12.7% |
| Housing at the national-uniform central (net $0.71bn) | 18.5% | 18.5% |
| Victims' harm on the custody footing ($32.34bn) | 20.0% | 19.8% |
| Every choice least costly / most costly | 24.0 / 14.0% | 23.7 / 14.1% |

**Pooling within SPM units (ruling 6).** The person count gives wages, mobility, scale and care earnings
to each earner, while taxes and rent are shared within the household. So a degree-holding earner can be
ahead while the children and a non-working spouse carry per-capita tax shares with no offsetting gain.
The pooled variant adds up the other residents' amounts in each SPM unit and gives each of them the
unit's mean. 83% of other residents share their SPM unit with at least one more of them. Group members
stay out, and their items stay in the group frame; 7.0m other residents share a unit with a group member.
Under (a), at central values [CALCULATION: `derived/pooling_moves.csv`, `derived/person_nets_by_cut.csv`]:

- **Children:** 1.5% ahead become 27.8%. 16.1m children move ahead because their units come out ahead.
- **Adults not working:** 2.8% become 10.8%; 6.8m move ahead.
- **Working adults:** 37.2% become 29.6%. 16.6m earners who are ahead on their own live in units that
  come out behind, and 5.2m move the other way.
- **Winning units:** they hold 70.6m people. 60% of them are ahead on their own, and 88% of their
  working adults.

In all, 28.1m people move ahead and 16.8m behind. Under (b) the moves are smaller: children 1.3% → 20.1%,
adults not working 2.9% → 8.9%, working adults 36.9% → 28.9%, everyone 19.9% → 21.4%. The median net
falls (−$284 → −$377 under (a)) because a few members' gains are spread over their units; the mean does
not change. The shares rise most at the top: the top decile goes from 33.1% to 41.3% ahead under (a),
and the bottom decile stays at 3%. US-born BA+ adults go from 43.3% to 37.4%, and everyone under 25 from
4.0% to 25.4%.

The pooled amount is each unit's weighted mean. In 42% of units the members' CPS person weights differ.
There the ruling's plain sum over the number of members moves the totals (the social net by +$1.0bn)
and fails the gate that pooling keeps every channel's total; it would put 24.3% and 21.7% ahead
[CALCULATION: `derived/inputs.json`, `pooling.plain_mean`].

**Geography is an assumption, and the result depends on it.** The state and local part is spread over
states in proportion to where the group lives [INFERENCE]. Pooled nationally, California's net per person
changes from −$2,751 to −$1,359, and the rest of the country's from −$544 to −$810.

## Against the base lane's September 24 table

Fed the September 24 inputs, this code reproduces the base's committed `channel_by_quintile.csv` (git
7ec7144) to 2.8e-14bn over 468 cells in 13 channels, and the September 23 one (5b8957e) to the same
precision [`derived/regression_sept24.csv`, `regression_sept23.csv`]. The frame's own channels of the
same name differ by construction. Values are $bn by SPM quintile, central
[`derived/quintiles_vs_base_sept24.csv`].

| Channel | Frame total | Base total | Q1 frame / base | Q5 frame / base | Why |
|---|---:|---:|---:|---:|---|
| Fiscal (a) | −212.10 | −225.10 | −9.70 / −6.83 | −118.73 / −139.82 | +$1.70bn: F is the account's own (mean 11.25; the base's 9.56 is the below-BA split's); +$11.30bn: the future taxpayers' part is not allocated; federal and state-local keys, the latter within the group's states |
| Fiscal (b) | −212.10 | −225.10 | −39.88 / −45.02 | −48.55 / −45.02 | same totals; state-local part per person within the group's states |
| Fiscal, pooled nationally (a) / (b) | −212.10 | −225.10 | shares equal the base's | | total only |
| Wages | −0.20 | −1.47 | −6.20 / −4.79 | +28.68 / +30.40 | the account's split (high school or less) against the base's below-BA split; the base's channel itself matches to 0 (control) |
| Renters; landlords | −33.86; +37.37 | the same | equal | equal | the rake keeps the base's income cells and adds states |
| Crime victims | −30.93 | −32.34 | −9.44 / −10.41 | −5.52 / −4.89 | decision 4's figure against the custody footing; the group's states |
| Crime, custody footing | −32.34 | −32.34 | −9.87 / −10.41 | −5.77 / −4.89 | the group's states only |
| Unreimbursed care | −4.40 | −4.40 | −0.45 / −0.45 | −1.25 / −1.16 | the states of the group's uninsured |

The top quintile's share of fiscal (a) is 56.0% here against the base's 62.1%. The frame keys the
state-local part, 81% of the cost, by state-local taxes, which are less progressive than federal ones,
and only in the states where the group lives.

## The group itself (beside the account)

[CALCULATION: `derived/group_frame.csv`]

| Item | $bn a year (range) | Per member | Basis |
|---|---:|---:|---|
| Direct fiscal transfer received (A, sign flipped) | +234.7 (214.2–255.1) | $5,738 | `fiscal_totals("sept24")` at the band ends |
| *The account's own split by generation: its net cost to other residents, no reference group, minors with their parents (NAS 2017)* | | | |
| — G1, born in Mexico (16.86m) | 110.2–134.8 | $6,539–7,995 | `generation_account_2026_09_24` (ba12f3c) |
| — G2, US-born, a parent born in Mexico (12.21m) | 50.2–53.0 | $4,110–4,338 | same |
| — G3+, US-born of US-born parents (11.83m) | 40.5–58.6 | $3,420–4,952 | same |
| First generation's market gain over its Mexico earnings | +224.6 (196.5–242.8) | $18,377 per Mexico-born member (12.22m) | place premium Re 2.46 (2.08–2.79) × $378.4bn US earnings |
| Second and third-plus generations (28.68m, US-born) | none | — | no Mexico counterfactual exists; none invented |
| Wage competition among the group's own workers, high school or less (ε ∞) | −20.8 (−16.6 to −25.1) | −$509 | account nest × members' CPS earnings |
| Same, ε 3 | −37.9 (−30.1 to −45.7) | −$927 | same |
| Wage gain of the group's workers with some college or more (ε ∞) | +5.8 (4.6–7.0) | +$143 | same |
| Victims inside the group, equal footing | −20.1 | −$492 | victim lane's rows (1,280 homicides, 187k non-fatal) |
| Remittances received in Mexico from the United States, 2024 (context) | 62.8 | — | Banxico CE167, US-origin receipts, revised: 96.58% of $65.0bn from all countries |

**Remittances (data fix).** The previous run's $64.7bn was Banxico's unrevised total from all
countries. The consumption lane's corridor (`consumption_key_2026_09_24`, 6841b39) needs 3.3 times the
surveyed sending amount (CEMLA, $6,035 a year per sending unit), so it includes flows beyond the CPS
households. [SOURCE: Banxico SIE table CE167, series SE43675 and SE43738, read from
`consumption_key_2026_09_24/_cache/sources/corridor/banxico_CE167_2022_2025.xlsx` the way
`remittance.py` `primary_flows()` reads it; gated against that lane's committed $62.794bn]

Place premium: "the average emigrant comes from the 56th percentile of residual wages, suggesting that
Ro/Re = 1.03 (with a 95% confidence interval of (0.96, 1.12)), so that Re ≈ 2.46". Table 8 gives Mexico Re
2.79 at the 50th percentile and 2.08 at the 70th, a percentile "stronger than *any* of the evidence from
*any* country above supports". [SOURCE: Clemens, Montenegro & Pritchett, "The Place Premium", HKS
RWP09-004, sec. 3.3 and Table 8; corpus `doi_10_2139_ssrn_1211427`, `page.md` lines 333, 532, 583]

The generation rows are the account's own split of its cost to other residents, low to high end.

- **Sign:** they are costs to others, not the group's gains, and they are never netted against other
  residents' rows. The page table leaves them out.
- **Reference group:** there is none. The September 19 ledger's gaps are measured against third-plus
  non-Hispanic whites and are never scaled onto them.
- **Children in their own generation:** G1 is $63.8bn at the low end and $53.6bn at the high end, G2
  $81.7bn and $95.1bn, G3+ $55.3bn and $97.6bn [FRAMING-SENSITIVE].
- **Check:** under both conventions the three add to the band ends to 1e-6bn (gated).

Two assumptions sit behind the market-gain row [INFERENCE]:

- the premium is a PPP wage ratio for the same worker;
- the gain assumes the same employment and hours in both countries.

The in-group victim figure is on the victim lane's equal footing, the footing of its rows. No lane
computed it on the custody footing or with the mixed-group correction, so neither is applied (the
custody-scaled −$22.5bn of the previous run is withdrawn under ruling 1). Police records put 70–81% of
Hispanic offenders' victims in-group, which would raise it.

## Channel registry

`derived/channels.csv`: 39 rows. Each row gives the key id (`who`), `relation`, `in_net`, the
counterfactual, the source lane, the ladder, the status and the date. Values are signed from other
residents' side, in $bn a year. Every total is read from its lane's derived files.

| Channel | Low | Central | High | Relation | Status |
|---|---:|---:|---:|---|---|
| Main case (fiscal + wages) | −200.9 | −223.6 | −246.3 | total | adopted (219) |
| Allocation base: adopted fiscal band + decision 4 victims (mixed footing), not a published total | −252.5 | −275.2 | −297.9 | allocation base | adopted |
| Allocation base, every choice low / every choice high (mixed footing), not a published total | −217.0 | | −334.0 | allocation base (published full span −210.2 / −336.9) | adopted |
| Published total at central values, equal footing (justice on its raw-coding key; victims $30.93bn) | −247.7 | −273.0 | −298.4 | total (published) | published |
| Published total at central values, custody footing (adopted band; victims $32.34bn) | −253.4 | −278.7 | −304.0 | total (published) | published |
| Fiscal, A + F | −200.6 | −223.4 | −246.2 | inside | adopted |
| — federal, financed today / state-local / future taxpayers | −23.4 / −168.7 / −8.6 | −30.6 / −181.5 / −11.3 | −37.9 / −194.3 / −14.0 | parts of fiscal | adopted |
| Wages (production term P) | −0.24 | −0.20 | −0.16 | inside | adopted (191) |
| Wages, ε 3 (receipts +4.6 central) | +8.0 | +6.7 | +5.3 | overlaps:wages | proposed |
| Care (hours taxes, elder care) | +2.6 | +4.1 | +13.3 | inside the fiscal row | adopted (198) |
| Consumer prices (CEX); care consumer surplus | +23.8; +3.9 | +23.8; +11.9 | +23.8; +12.8 | overlaps:wages, never added | side views |
| Renters / landlords | −50.5 / +50.1 | −33.9 / +37.4 | −57.8 / +67.2 | beside; levels ordered by the net | adopted (190) |
| Housing net (national-uniform central) | −0.38 | +3.51 (+0.71) | +9.40 | overlaps | adopted (190) |
| Crime victims (decision 4; the victim lane's envelope) | −15.4 | −30.9 | −45.3 | beside | adopted (189, 218) |
| — equal footing / custody footing / NIBRS arm | | −28.9 / −32.3 / −28.6 | | overlaps, not in the nets | adopted |
| Property crime (proxy) | −1.27 | −1.27 | −1.38 | beside | adopted |
| Unreimbursed care | −3.2 | −4.4 | −5.6 | beside | adopted (192) |
| Congestion | −8.0 | −19.2 | −35.3 | beside | adopted (195) |
| Mobility | +0.18 | +0.65 | +2.46 | beside | adopted (203) |
| Preferences, whole regime / group part | −0.2 / −0.01 | −4.0 / −0.58 | −18.7 / −3.76 | beside, group part in the proposed net | adopted / proposed (213) |
| City size and schooling mix | −56.6 | +13.9 | +84.4 | beside | proposed (201) |
| Debt legacy interest | −28.3 | −32.4 | −36.4 | apart, never added | adopted (207) |
| House-value gain to owners (a stock) | +1,264 | +1,932 | +2,855 | apart, never added | adopted (190) |
| Consumption key, proposed (6841b39) | +4.05 | +4.05 | +4.05 | a change to the account; never in a net or the adopted total | proposed |
| Sister lanes | see below | | | beside; only dilution in a net ("with proposed") | proposed |

**Crime footing.** Every crime row is a figure a lane computed, and each row names its footing.

- **Central, $30.93bn:** decision 4's figure. It is on the equal footing (Mexican-origin offending at NCVS
  Hispanic rates) with ladder 218's mixed-group correction, θ 0.4977
  [DATA: `crime_ratio_direction_2026_09_24/derived/dollar_effects.csv`].
- **Low, $15.41bn, and high, $45.34bn:** the victim lane's envelope, every arm at its low or high setting.
  Both use Miller 2021 prices; the high end adds the DOT 2024 VSL for murder
  [DATA: `crime_victim_cost_2026_09_23/derived/arms.csv`].
- **Allocated variants:**
  - $28.92bn, the equal footing without the correction (the victim lane's central);
  - $32.34bn, the custody footing (ACS institutional ratio 1.118), which is the propagation lane's
    footing;
  - decision 4's figure on the national key.
- **Listed only:** NIBRS's victim-conditional arm, $28.59bn. It is not allocated.

**Ruling 5: the pairing.** The adopted fiscal band charges justice by the custody ratio, while decision
4's figure is on the equal footing. The person nets keep decision 4's $30.93bn as the central victims
row. Their allocation base ($252.5–297.9bn) mixes the two footings. It is therefore labelled "allocation
base: adopted fiscal band + decision 4 victims (mixed footing), not a published total", and it is never
quoted as a total. The totals at central values are the published pairing, one footing at a time
[DATA: `sept24_propagation_2026_09_24/derived/real_costs_totals.csv`, section 7]:

- $247.7–298.4bn on the equal footing, with the justice line on its raw-coding key (band variant
  `justice_raw_coding`, $196.6–242.0bn);
- $253.4–304.0bn on the custody footing, on the adopted band;
- the published range is $248–304bn, from the equal footing's low end to the custody footing's high
  end. The published full span is $210–337bn.

A gate, `published_totals_on_their_bands`, checks each total's fiscal part against its band. The
person-level nets barely depend on the choice: 20.1% against 20.0% ahead under (a). The same file's
`custody_mixed_scaled` rows (victims $34.58bn) cite this lane's hybrid, withdrawn under ruling 1; nothing
here uses them.

**Federal split.** On the adopted case, 18.8% of the fiscal cost is federal ($41.9bn of $223.4bn; 15.9% at
the low end, 21.1% at the high end).

- **Source:** the debt lane's `federal_split_2024.csv` at 7ec7144, taken as it stands.
- **Check:** this lane's engine lines times that lane's per-line fractions reproduce its federal part to
  2.7e-6bn and its fiscal gap to 4.7e-7bn in all six end × convention cells, with the correction rows
  counted once as lines.
- **Correction rows:** the lines file's rows for the lane constants and for schools with colleges equal
  the per-correction file to 1e-16.
- **Positive control:** the same recomputation on September 23 reproduces b42efdc.
- **Frame's cost against the debt lane's gap:** −4.9e-5bn and +3.3e-5bn. This is the `fiscal_totals`
  rounding.
- **Deficit share:** 26.95% of the federal part is deficit-financed. It comes from FY2024 outlays of
  $6,735bn and receipts of $4,920bn [SOURCE: OMB Historical Tables 2.1 and 3.1, FY2027 release].

**Housing levels (ruling 2).** Renters and landlords move together by level, and the levels are ordered by
the net for other residents, as ladder 190 publishes it.

- **Central:** the metro-local arm's long-run central. It is the base's central, and this frame keys by
  state.
- **Low, −$0.38bn:** high elasticity, form A, national uniform, high ownership share.
- **High, +$9.40bn:** high elasticity, form C (semi-log), metro-local, low ownership share.
- **Scaling of the low and high rows:** they are spread by the form-A arm with the same elasticity and
  geography, scaled ×1.000 and ×1.154 to their totals. This assumes the functional form changes the
  level of the rent response more than its geography [INFERENCE].
- **The other published central:** the national-uniform arm (net +$0.71bn; renters −$33.47bn, landlords
  +$34.18bn) is allocated as a named variant.

**Care.** Care has been inside the fiscal row since September 24; it is not added beside the account. The
extra-hours gain goes to US-born women in the top wage quartile of their census division (16.4m in CPS
against the lane's 14.4m in the ACS).

- **The women:** they keep $3.6bn of after-tax earnings, but their private gain is about zero. The hours
  trade off leisure and home production (the envelope argument).
- **Budgets:** the $2.7bn of taxes goes to budgets and reaches everyone through the financing convention.
  The display row is `care_women_extra_hours`.

## Sister lanes (read at 2026-09-25 01:52 CEST, all final)

**Counterfactual rule (parent ruling, 2026-09-25).** A sister row may enter a net, including "with
proposed", only if its counterfactual is the group's absence, or its pupils' absence. That is the
account's counterfactual. The phrase must open the row's `counterfactual` field, and a qualifier that
changes the comparison disqualifies it, such as "enrollment held" or "spending that fully follows
enrollment".

- **Rows on other counterfactuals:** they go to the role table and to
  `derived/sister_other_counterfactuals.csv`, each labelled with its own counterfactual.
- **The page table:** it shows only rows on the account's counterfactual.
- **Gate:** a new gate, `sister_allocated_rows_on_account_counterfactual`, stops the run if any
  allocated row fails the rule.

| Lane | State at run time | Rows | On the account's counterfactual | Allocated, $bn (low / central / high) |
|---|---|---:|---:|---|
| school_dilution | committed e4bdf40 | 25 | 13 | +2.6 / −20.1 / −44.3 to other residents' pupils aged 5–17, from instruction (16.08 central) and support (3.98 central), spread by the lane's regional breakdown |
| vending_restaurants | final, committed c98f479 | 11 | 0 | none (was −0.34 / +0.31 / +0.94) |
| compliance_gap | committed fa338b8 | 11 | 0 | none (as before) |
| movers_reasons | committed f9c9504 | 14 | 0 | none (was −0.58 / −0.66 / −0.96) |
| consumption_key | final, committed 6841b39; no rows file | — | — | none; its proposed key is the registry row `consumption_key_proposal`, below |

generation_account (final, committed ba12f3c) writes no rows. Its split of the account by generation is
in the group frame above and never in a net. Movers' 14 rows, vending's 11 and compliance's 11 sit in the
role table only (`derived/role_table.csv`, status `role_only`); the only allocated rows are the school
lane's rows 0 and 11.

**The school rows** are the present value of lifetime earnings, not annual cash. The relabel is proposed
in `decisions/2026-09-25-school-dilution-priced-beside.md` (status proposed), so the rows enter only the
"with proposed" net and never the account or the social net. The lane's overlapping rows stay out:
regional and poverty splits, the long-run and power-law forms. The rows on the account's counterfactual
that overlap or sit inside the account are shown in `winners_losers_table.csv` and never added.

**The consumption key, beside the school rows (proposed).** The registry row `consumption_key_proposal`
reads "proposed change to the account's consumption key, −$4.1bn on the fiscal total". The consumption
lane keys consumption taxes on CE spending by income rank, net of corridor-calibrated remittances (spec
`both_corridor_net_h2`). That lowers the fiscal cost by $4.05bn at both band ends, to $196.8–242.3bn. Its
variants run from −$2.6bn to −$8.4bn, and surveyed remittances give −$6.7bn. It is a proposal and has
not been adopted, so it stays out of the central count, out of both conventions' nets and out of the
adopted total; the registry signs it +4.05 from other residents' side and allocates it to no one. Two
gates check it: the lane's adopted band equals the engine's to 5e-5bn, and its change equals its band
minus the adopted band. Every net is byte-identical to the run before the row was added.
[DATA: `consumption_key_2026_09_24/derived/engine_summary.json`]

**Before and after the rule.** Only the "with proposed" net changes. Its allocated sum moves from −$270.97bn to
−$270.62bn: out come vending's +$0.31bn and movers' −$0.66bn. The account and social nets do not change.

| Net, share ahead | Before (a) / (b) | After (a) / (b) |
|---|---:|---:|
| Social net, central (the verdict) | 20.1 / 19.9% | 20.1 / 19.9% |
| With proposed, central | 20.57 / 20.51% | 20.58 / 20.51% |
| With proposed, least costly | 31.64 / 30.80% | 31.63 / 30.79% |
| With proposed, most costly | 10.67 / 10.76% | 10.68 / 10.76% |

**Priced rows beside the account on other counterfactuals.** None of these rows is in any net. $bn a
year, central (low to high); every row, including the inside and overlapping ones, is in
`derived/sister_other_counterfactuals.csv`.

| Lane, row | Who | Channel | $bn | Counterfactual |
|---|---|---|---:|---|
| movers 3 | California state and local budgets | taxes on net income moved to all other states | −0.74 (−0.63 to −1.05) | the net movers stay; a transfer to other states |
| movers 5 | Texas state and local budgets | taxes on the net income moved from California | +0.10 (0.06 to 0.17) | the movers stay in California |
| movers 0 | US-born adults leaving California who cite conditions | moving costs | −0.03 (−0.01 to −0.09) | without the conditions they cite they stay; "an upper bound for moves driven by ethnic composition, which the category cannot isolate" |
| vending 0 | licensed restaurant owners | sales after legalization | +0.16 (−0.16 to +0.47) | California before SB 946 |
| vending 2 | restaurant workers | payroll after legalization | +0.17 (−0.17 to +0.50) | California before SB 946 |
| vending 1 | licensed restaurant owners | bound: every street-food dollar taken from restaurants | −0.41 (0 to −1.17) | no street-food vending at all |
| vending 4 | vendors | net income of street-food vendors | +0.04 (0.02 to 0.09) | no street-food vending at all |
| vending 8, 9 | budget | sales tax not remitted; City of LA program net of permits | −0.014; −0.004 | all vending sales taxed; no city vending program |
| compliance 1 | noncompliant employers in construction | workers' compensation premiums avoided | +1.31 (0 to 2.24) | the same workers paid on the books at the same gross wage |
| compliance 2, 3 | noncompliant employers; their off-books workers | wage-and-hour underpayment | +0.59; −0.59 (0 to ±2.26) | paid what wage-and-hour law requires |

The other allocation rules still apply:

- **Explicit key:** an explicit `key` column wins. Otherwise `key_map.csv` patterns decide, and a row with
  no defensible key stays in the role table.
- **Future taxpayers and bounds:** rows naming future taxpayers, and rows that are bounds, are never
  allocated.
- **Sign conventions:** two occur among the lanes, and both are read.
  - A central value of zero or more is an amount along the row's direction.
  - A loss row with a negative central is read as signed changes.
  - A gain row with a negative central is refused as ambiguous.
- **Templates:** `key_templates.csv` lists the templates with their CPS populations.
- **State words:** "City of LA" maps to California, not Louisiana.

## Method

- **Base.** `distribution_weights_2026_09_23` is loaded from git at 7ec7144, the commit that moved it to
  September 24, so later working-tree edits cannot change this lane. Its frame is reused unchanged:
  - 295.83m other residents in CPS ASEC 2025;
  - the SPM ranking, the tax key and the NCVS key;
  - the ACS and SCF housing cells.
- **Fiscal case.** `specs.cjs` evaluates the explorer engine on the 64 main-case specifications for the
  September 23 and September 24 models. It copies the specification grid of `package.cjs` without loading
  it, because loading it writes a file in another lane.
  - Per specification, fiscal = A + F and wages = P.
  - The frame's A at the band ends is the base's `fiscal_totals("sept24")`; F is the account's own.
- **Channel allocation.**
  - Fiscal: the debt lane's federal part. Today's share goes by federal tax share or per person; the
    state-local part goes by state, in proportion to where the group lives.
  - Wages: the account's own split (high school or less, cash, scaled ×1.5155 under GDP normalization).
  - Rent: renters, landlords and owners are raked to ACS income cells and state totals.
  - Crime, unreimbursed care and congestion: by the states where the group lives or drives, then by the
    base keys within each state.

## Gates

443 pass; the script stops on the first failure. Twelve pytest positive controls pass (synthetic frame,
sister ingestion, the counterfactual rule and its gate, SPM pooling, rake, fallbacks). Against the 434 of
the run before the counterfactual rule, seven fewer sister rows are allocated, each with three closure
gates (−21). These gates are new:

- the counterfactual gate (+1);
- four on the generation split (+4);
- two on the consumption proposal (+2);
- twenty on the pooling (+20): SPM units nest in households, pooling keeps every channel's total at every
  level (worst 3.1e-14bn), and the 18 pooled nets close;
- three on ruling 5 and the remittance fix (+3): the published totals sit on their bands, Banxico CE167
  matches the consumption lane's corridor, and the corridor needs over three times the surveyed amount.

- **Bands:** both bands reproduce `main_case_bands.csv`: 200.8752–246.3184 and 203.2070–249.6400.
- **Closure, headline:** CPS wages plus the engine's A + F equal the adopted cost in all 128 case ×
  specification pairs (max gap 2.4e-10bn).
- **Band ends with the shared A:** the frame's inside channels plus the future taxpayers' part equal the
  band ends to 4.9e-5bn. The difference is `fiscal_totals` rounding, and the tolerance is 1e-3.
- **Closure, persons:** persons sum to every channel's total at low, central and high, and to every
  sister row.
- **Regression:** both base tables reproduce to 2.8e-14bn: September 23 at 5b8957e and September 24 at
  7ec7144. Each gate first checks that the target file holds its case.
- **Shared inputs:**
  - the debt lane's September 24 band equals the engine's;
  - the interest is pinned at 28.3387 / 36.4297;
  - housing matches ladder 190's four values to 5e-6;
  - the crime figures are the lanes' own.
- **Cuts:** all eleven cuts sum to the frame [`derived/cut_reconciliation.csv`].

## Limits

- **State-local incidence:** it uses national ITEP rates by income group, not state rates (Texas taxes are
  more regressive).
- **Wages:** they are national; the account's nest has no local labour markets.
- **Missing CPS items:** CPS has no school type, no gross rents and few restaurant owners.
- **Landlords:** they are assumed to live in the state where the rent is paid.
- **Excluded from the nets:** the debt legacy, the owners' stock gain and the side views.
- **Unit of account:** the person count gives wages to the earner and shares taxes and rent within the
  household; the pooled variant shares everything within the SPM unit. Neither measures how families
  actually share income [FRAMING-SENSITIVE].

**Would change it:**

- State-specific tax incidence, or a state-level fiscal account, would change the geography of the fiscal
  row, and that geography drives the state gap.
- A local-labour-market wage model would concentrate the wage loss in the group's states.
- The parent's choices of financing convention and of the unit (person count or pooled SPM unit: 20.1%
  and 19.9% against 23.9% and 21.4% ahead) [FRAMING-SENSITIVE].
- The consumption lane's proposed key (6841b39, not adopted) would lower the main case by $4.05bn, to
  $196.8–242.3bn (variants −$2.6bn to −$8.4bn), and the fiscal channel with it. It is listed in the
  registry and is in no net.

## Files

- Run from the repository root:
  - `node infra/immigration-fiscal/winners_losers_2026_09_24/specs.cjs`
  - `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/winners_losers_2026_09_24/winners_losers.py`
  - `... -m pytest infra/immigration-fiscal/winners_losers_2026_09_24/ -q`
- [2026-09-26] Both scripts take `--case sept26_schools` (the default), `sept26` or `sept24`, and
  `--out-dir DIR` (default `derived/`); give both the same flags. The regression and quintile files
  are named by case: the schools run writes `regression_sept26.csv`, `regression_sept26_schools.csv`
  and `quintiles_vs_base_sept26_schools.csv`. `old_new.py` writes the three cases' old → new table to
  `../sept26_propagation_2026_09_26/derived/old_new_ledger.csv`.
- The September 24 run wrote these files. [2026-09-27, parent: `derived/` now holds the schools-case
  run of the same names plus its three case-named files. The September 24 run's `regression_sept23.csv`,
  `regression_sept24.csv` and `quintiles_vs_base_sept24.csv` stay, unchanged from 8a762fe, because the
  regression paragraph above cites them.]
  - `channels.csv`, `winners_losers_table.csv`, `person_nets_by_cut.csv`, `cuts.csv` (every channel at
    every level in every cut) and `cut_reconciliation.csv`;
  - `net_shares.csv` (`unit`: `person` or `spm_unit_pooled`), `pooling_moves.csv`, `winners_tree.csv`,
    `winner_cells.csv` and `group_frame.csv`;
  - `role_table.csv`, `sister_other_counterfactuals.csv`, `key_templates.csv` and
    `naics_census_industry.csv`;
  - `fiscal_specs.csv`, `fiscal_lines_band_ends.csv` and `fiscal_federal_split.csv`;
  - `regression_sept23.csv`, `regression_sept24.csv` and `quintiles_vs_base_sept24.csv`;
  - `inputs.json`, `gates.json` and `sources_manifest.csv`. The manifest pins every input by sha256,
    including the git blobs read at b42efdc, 7ec7144 and 5b8957e.
- `key_map.csv` holds the sister-row patterns.
- The person frame is `_cache/person_frame.parquet` (ignored). It carries `SPM_ID` and the pooled nets.
- Nothing outside this directory was edited, and nothing was committed.

Model self-report: claude-opus-5-5[1m], lane agent, 2026-09-24/25.

## v4 case (sept29), 2026-09-29

**Verdict:** On the v4 case ($371.4146 / $434.8410bn), pooled within SPM units, 17.9% of other residents come out ahead under tax-share financing (a) and 17.1% under per-person cuts (b), against 17.8% and 17.0% on September 27; the stacks give 11.1–24.4% under (a). The person count gives 16.9% under both, as on September 27. Taxpayers' fiscal channel is $394.4bn at central values (September 27: $349.3bn). Of it, $74.9bn is the pension accrual, which nothing finances in 2024. It sits with the future payers of Social Security and Medicare, beside the borrowed part ($13.1bn), and is not allocated to anyone living today. So the social net on today's residents falls in size, from −$386.6bn to −$360.6bn, while the case rises $48.5bn. The capped programs, now including public housing's deficit, fall on eligible households without the aid: $8.1bn (was $5.1bn). The group's own rows are now on the account's count, 39.71m members, with the CPS's 40.9m beside them. [CALCULATION: `specs.cjs --case sept29` and `winners_losers.py --case sept29`, pinned; `derived/sept29/`] [FRAMING-SENSITIVE: the accrual's payer]

claude-opus-5-5

**What runs.** `node specs.cjs --case sept29` evaluates the September 27 case (its band variant `sept27_case` in the adopted lane's `main_case_bands.csv`) and the adopted case with their own packages. `winners_losers.py --case sept29` allocates the adopted case and keeps September 27 as the positive control. Both write to `derived/sept29/`; `derived/` keeps the September 27 run. Pins in `CASES["sept29"]`:
- the distribution lane at 492bf32 (`derived/sept29/`, `case_ends_sept29.json`);
- the debt lane at 7e1b500 (`derived/sept29/`: `stocks.csv`, `summary.json` and the per-correction files);
- the generation account at aa1f53b (`generation_results_sept29.csv`);
- the propagation lane at 911afa6 (`sept24_propagation_2026_09_24/derived/sept29/`). As for every case, its real-costs totals and band variants are read from the working tree, which equals 911afa6 (`git diff 911afa6` empty; `sources_manifest.csv` holds their sha256);
- the debt lane's legacy interest (`SEPT29_INTEREST`): 30.7514 / 41.4794, gated at 5e-4 against `stocks.csv` at 7e1b500 (30.751354 / 41.479394);
- the ladder entry is 275 (d40e085), as the lead set; there is no new number.

`--dev-unpinned` is for dry runs before an upstream commit lands. It reads the missing pins' files from the working tree and stops unless `--out-dir` lies outside `derived/` (tested). The dry run used it; the final run does not.

Reproduce, from the repository root:
- `node infra/immigration-fiscal/winners_losers_2026_09_24/specs.cjs --case sept29`
- `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/winners_losers_2026_09_24/winners_losers.py --case sept29`

**Channels, central values, $bn a year** (`derived/sept29/channels.csv`):

| Channel | September 27 | September 29 |
|---|---:|---:|
| Adopted main case, other residents' net (fiscal + wages) | −354.6 | −403.1 |
| Fiscal channel (taxpayers) | −349.3 | −394.4 |
| — cash financed today | −291.2 | −260.6 |
| — return on public capital (never borrowed) | −44.7 | −45.8 |
| — federal part financed by borrowing (future taxpayers) | −13.4 | −13.1 |
| — pension accrual (future payers of Social Security and Medicare) | — | −74.9 |
| Displaced beneficiaries of the capped programs | −5.1 | −8.1 |
| Wages (production on row 4) | −0.2 | −0.6 |
| Social net on today's residents | −386.6 | −360.6 |
| Debt legacy interest (beside, never added) | 30.9–41.6 | 30.8–41.5 |

The channels outside the budget do not change: renters −33.9, landlords +37.4, victims −30.9, congestion −13.0, unreimbursed care −4.4 and the rest. Each is taken as its lane publishes it. Those lanes price the CPS's 40.9m, not the account's 39.71m: each pins the union at 40,896,574 (housing_transfer `arms.py` TARGET, which scales the ACS metro counts to it; congestion and its long-run re-derivation; care; scale spillovers; labor mobility; the victim lane's target population). This lane does not re-estimate them. Where a channel is linear in the count, the first-order correction is × 0.971 (39.712 / 40.897), about $1.3bn on the social net of today's residents. [INFERENCE; not computed]

**Share of other residents ahead** (`net_shares.csv`, the social net, central; stacks least to most costly in brackets):

| Count | (a) tax-share | (b) per person |
|---|---|---|
| Pooled within SPM units | 17.8 → **17.9** (11.1–24.4) | 17.0 → **17.1** (11.4–22.4) |
| Person | 16.9 → **16.9** (12.5–20.9) | 16.9 → **16.9** (12.5–20.8) |

The share barely moves. The accrual leaves today's persons, and the rest of the case's rise falls on the same payers in the same proportions.

**The group itself, on the account's count** (`group_frame.csv`; the CPS's published weights in `group_frame_cps_published.csv`):

| Item | Row 4 (39.71m) | CPS published (40.90m) |
|---|---|---|
| Direct fiscal transfer received (A, sign flipped), $bn | +412.8 (383.1–442.5) | the same |
| — per member | $10,395 | $10,094 |
| First generation's market gain over its Mexico earnings, $bn | +201.9 (176.6–218.2) on $340.1bn of US earnings, 11.04m members | +224.6 (196.5–242.8) on $378.4bn, 12.22m |
| — per Mexico-born member | $18,290 | $18,377 |
| Wage competition among the group's own workers, high school or less (ε ∞), $bn | −18.4 (−14.6 to −22.2) | −19.5 |
| Same, ε 3 | −31.6 | −34.7 |
| Wage gain of the group's workers with some college or more (ε ∞) | +5.3 | +5.5 |
| Victims inside the group, per member | −$506 | −$492 |
| The account's split by generation (minors with their parents), $bn | G1 169.4–197.4, G2 110.7–121.8, G3+ 91.4–115.6 | the same (the account's own rows, on row 4) |

[CALCULATION: `derived/sept29/group_frame.csv` against `group_frame_cps_published.csv`]

**Rules designed.**
- **The group frame's count** (the lead's question of 11:23). Every person-based group row is on the account's row-4 weights: A per member, the first generation's earnings and market gain, the group's own wage rows, the victims per member and the member counts. `row4_group_weights` uses the base lane's row-4 rule, the same mask and factors as `v4_inputs.py` (production_row4.json: the Mexico-born naturalized × 0.8556 and noncitizens × 0.7781 outside California and Texas; no other resident moves). It gates the grid file's sha256, each cell's records and CPS population, that only group records move, and the group's count, 39,712,493.33. The published 40.9m frame stays beside it in `group_frame_cps_published.csv`. The counterfactual label names 39.7m. The other residents, the payers, are the same persons on the same weights under both frames. Alternative: keep the published 40.9m frame; its per-member A would divide the 39.71m account's total by 40.90m, 2.9% too low. The one other place the group's weights enter, the cut of the ten states with the most members, keeps its set on row 4: CA, TX, AZ, IL, CO, WA, FL, NC, GA and NV (Nevada and Georgia swap ranks; the cut is membership, so it does not move).
- **The pension accrual** is a fourth financing part (the debt lane's `accrual_bn`, all federal). It goes to the future payers of Social Security and Medicare (`future_pension_accrual`) and is left out of today's persons. Alternative: allocate it today on the federal tax key, as if the trust funds' later outlays were prefunded now (registry note).
- **Production on row 4.** The case's wages and F come from the base lane's row-4 re-solve, gated there against the case's grid; the September 27 control keeps the published rows.
- **Public housing's deficit** is capped like rental assistance, on rental assistance's key (the base's `CAPPED_KEY_OF`).

**The two fiscal-channel centrals.** This lane's $394.4bn is the case's mid, $403.1bn, less −P ($0.6bn) and the capped programs ($8.1bn). The distribution lane's $395.7bn adds $1.3bn of F difference (its central scenario's F, 10.26 against the engine's 8.98 at 48 / 11). The bridge is in the distribution lane's RESULT.

**Gates.**
- Cross-check: at 48 / 11 the fiscal channel's A is −383.094429 / −442.524231 (the base's one definition), and the engine's is −383.094478 / −442.524197. That matches −383.0945 / −442.5242 at the oracle's rounding, 1e-4.
- `specs.cjs --case sept29`: 25 PASS. The band is 371.4146–434.8410 against `main_case_bands.csv` (adopted), the September 27 control gives 321.8194–387.3701 (`sept27_case`), and each has its payload's 13 and 4 line responses.
- `winners_losers.py --case sept29`: exit 0, 524 gates: the dry run's 523 and `debt_legacy_pinned_sept29`. Every figure equals the dry run's; only provenance strings differ (the pins' commits in place of the working tree in `channels.csv`, `group_frame*.csv`, `sources_manifest.csv` and `inputs.json`).
- `scripts/rerun_lane.py` over the four commands (`specs.cjs` and `winners_losers.py`, the default and `--case sept29`), twice: IDENTICAL, 59/59 files both times. The first pass exited 3 only because `test_winners_losers.py` is not a rerun command; the second passed `--allow-unrun` for it and exited 0.
- Old outputs unchanged: no file under `derived/` outside `derived/sept29/` differs from HEAD.
- pytest: 17 passed, including the dry-run test.

**Log (times from `date` calls).**
- 20:58 JST: resumed after the 20:51 reboot. `specs.cjs` and `winners_losers.py` carried the sept29 edits made before it.
- 22:05: `specs.cjs --case sept29` into scratch, 25 PASS.
- 22:05–22:08: `winners_losers.py --case sept29 --dev-unpinned`. The first run stopped on a merge bug in `inputs.json`'s production metadata (a duplicate `weights` key); after the fix, exit 0 with 523 gates.
- 22:17–22:18: rerun_lane on the default case, IDENTICAL 35/35. pytest 17 passed.
- 22:33: the pins landed (debt 7e1b500, generation aa1f53b, propagation 911afa6); `SEPT29_INTEREST` set from `stocks.csv` at 7e1b500. `specs.cjs --case sept29` (25 PASS; both files identical to the dry run's) and `winners_losers.py --case sept29` (exit 0, 524 gates) into `derived/sept29/`, finished before 22:35:40.
- 22:35:40–22:39:14: rerun_lane pass 1, IDENTICAL 59/59 (exit 3: the test file). 22:39:26–22:47:15: pass 2 with `--allow-unrun`, IDENTICAL 59/59, exit 0. 22:47:20: pytest 17 passed.
