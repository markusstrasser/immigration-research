# Immigration — Topic Index

Files the agent should consult before acting. Start with Core State, then branch by question.

For **what our data show**, first use the [dataset register](immigration-dataset-register.md)
and the relevant analysis README to locate inputs, variables and executed outputs.
The [raw-file manifest](../sources/immigration-fiscal/data/MANIFEST.md) records storage;
the [reproduction-input guide](../infra/immigration-fiscal/REPRODUCTION_INPUTS.md)
records acquisition and joins. Check local availability, including ignored files,
before treating an old roadmap item or an uncomputed table as missing data.

Instrument note: this topic is politically charged and much of the synthesis is LLM-assisted. Treat this index as a routing layer, not as a neutral substitute for the cited artifacts. Consult `notes/llm-bias-caveat.md` before writing headline claims.

Status: rows without a tag are live. Superseded and cruft documents were deleted on 2026-09-29 ([decision](../decisions/2026-09-29-delete-superseded-and-cruft-docs.md)); the tombstone table at the end lists each deleted path with its last commit and successor, so `git show <last commit>:<path>` recovers it. Records (decision records, ladder entries, lane RESULTs, dated audits) stay as written; a record's link to a deleted file resolves through that table.

## Core State

[Confidence ladder](immigration-confidence-ladder.md): the live claim register, one entry per finding with its rating and source; entries 52 onward are live, 1–51 sit below its historical-snapshot marker.

[Measured school growth and pupil-level checks](immigration-school-peer-checks-2026-09-20.md):
actual Texas/California enrollment and staffing; ECLS-K white US-born pupils'
scores conditional on starting scores and school, including retained-K forms.
Mixed classroom associations, explicit uncertainty and causal limits replace
using the illustrative 10% enrollment stress case as an observed change.

[Executed causal checks](immigration-causal-execution-2026-09-20.md): actual
Chalfin crime-data translation and 21 public school-finance synthetic-control models;
count/rate identities, weak-IV intervals, donor influence and calendar limits.
[Incumbent school-capacity harm](immigration-school-capacity-harms-2026-09-20.md)
adds conditional learning-loss estimates and withdraws the old $0/no-harm claim.
Neither exercise adds an identified national dollar term.

System-wide school quality, which within-school and sibling designs cannot see:
[state NAEP](../infra/immigration-fiscal/school_systemwide_2026_09_27/RESULT.md) (ladder 248)
shows no loss for white pupils where the Hispanic or immigrant-origin share rose (+0.087 and
−0.019 SD per 10 points, 2003–2019). The English-learner share gives −0.035, fading with
region-by-year effects, about $1bn of lifetime earnings per white cohort if causal. Cut
scores, NAEP exclusion, graduation and exit exams do not move with the shares. Across
countries, [PISA](../infra/immigration-fiscal/pisa_germany_2026_09_27/RESULT.md) (ladder 243,
246) puts immigration at about 7–14% of German natives' 2012→2022 fall (0 to about 45%), and
the 2015–16 asylum wave shows no native effect by 2018. A shift common to every state or
country is outside both designs. Within districts, the 2022–2024 newcomer surge in New York City, Chicago and
Denver ([lane](../infra/immigration-fiscal/newcomer_school_shock_2026_09_28/RESULT.md), ladder 252)
moved never-English-learner scores by at most a few hundredths of an SD per 10 points of
newcomer share, while staff and money followed the pupils at about half to 0.6 and late.

Civil custody, criminal offenses and fiscal spending: [detention/crime measurement scope](immigration-detention-crime-and-fiscal-scope-2026-09-20.md). ACS institutional counts cannot separate immigration detention; government custody spending remains a cost, with intergovernmental payments consolidated once.

Crime selection by arrival cohort ([lane](../infra/immigration-fiscal/crime_selection_cohorts_2026_09_23/RESULT.md), ladder 196): Mexico-born arrival cohorts from 1975 to 2019 do not show rising positive selection on custody. Butcher and Piehl's result covers all immigrants and is measured in percentage points. The interstate movers' advantage is their schooling. The 2000 census assigned a US birthplace to most institutionalized Mexican-origin men whose birthplace it allocated, so 2000-census immigrant institutional rates (Butcher–Piehl, Rumbaut) run low for the foreign-born. BJS prison counts confirm it: the census found fewer institutionalized noncitizens (73,395) than state and federal prisons alone held (89,676). After correction, Rumbaut's ratio of US-born to foreign-born Mexican men's rates is 2.5–3.5 instead of 8.4.

Schooling position by arrival cohort ([lane](../infra/immigration-fiscal/schooling_selection_position_2026_09_23/RESULT.md), ladder 197): Mexican adult arrivals rank at a mean percentile of 0.51–0.56 among Mexicans of their own sex and birth year, where 0.50 is the median. The rank shows no rise across cohorts from 1975 to 2023. Every specification stays within 0.44–0.60; without the ACS 2020 no-schooling reporting step the 2020–23 cohort reads 0.543–0.545 (the step and the lanes it reaches are sized in [`acs_schooling_break_2026_09_26`](../infra/immigration-fiscal/acs_schooling_break_2026_09_26/RESULT.md)). Studies on Mexican surveys, which count mostly returnees, find negative selection.

**Detention spending investigation completed through September 20, 2026:**
[FY2024 reconciled accounts, verified custody subtotal and identification limits](../infra/immigration-fiscal/detention_reconciliation_2026_09_20/README.md).
Expired-funding records have been acquired and reconciled; the unresolved pieces
are custody allocation and matched local expenses/receipts, not missing account
downloads. Start with the [reuse handoff](immigration-verification-handoff.md#detention-crime-and-spending-reuse-before-researching)
and [specific records needed](../infra/immigration-fiscal/detention_reconciliation_2026_09_20/RECORDS_NEEDED.md).
No exact national total is identified by the examined files; this is not a claim
that such a total is impossible in principle.

Latest complete annual account: [national reconciliation and conditional net effects](immigration-complete-annual-account-2026-09-20.md).
**Adopted main case (October 7): $389–461bn/year conditional net cost to other US residents**
($389.1–461.5bn, $9.1–10.8k per member of a 42.75M-person lineage; [lane](../infra/immigration-fiscal/main_case_2026_10_07/RESULT.md),
[decision](../decisions/2026-10-07-main-case-v6.md), ladder 295). Its four newest items each replace an assumption
with a measurement or put a line on the rule its neighbours already follow:
- the pension accrual on the 2026 Trustees Reports and current law's separate OASI and DI funds, −$2.8 / −$2.7bn
  (ladder 286); the combined fund, which the Trustees say assumes a change in law, is an arm;
- retiree health on accrual, as the account already treats pensions: normal costs replace pay-go premiums, and care
  bought for military retirees' past service goes to zero, +$0.6 / +$0.7bn (288);
- the 3.04M added descendants at their measured ages, younger than the identified third-plus (51.2% under 20,
  against 46.7%), +$1.3 / +$2.9bn (292);
- user fees and the education keys on the identified 39.71M: public colleges keyed by measured use, tuition and
  hospital charges credited to who pays them, Pell keyed by the group's share and BEA's K-12 weight, −$0.3 / −$0.7bn
  (294).

The items interact by +$0.0 / +$0.1bn.
Counting benefits when paid, the cash set is $307.4–385.4bn ($7.2–9.0k per member); it has no pension item. The
3.04M added descendants of Mexican immigrants who no longer report Mexican origin, whom the survey cannot see, are
counted as whole people and add $20.0 / $29.2bn:
- the 1.09M lost after the third generation cost what an identified third-plus member of the same ages costs,
  $9,603 / 14,030 a year;
- the 1.94M lost at the third-generation rate, with their descendants, cost (1 − C3) of that plus C3 times a
  third-plus non-Hispanic white at the same ages, $5,054 / 7,257. Third-generation adults who no longer identify
  close C3 = 0.557 (SE 0.246) of the identifiers' college gap to third-plus whites (ladder 280).

An added person costs others $6,692 / 9,696, less than an identified member ($9,293 / 10,886), so the cost per member
is below the identified union's. How identity loss continues past the third generation is modelled: arms a and c
(1.81M and 4.27M added) give $378.0–445.3bn and $400.2–477.7bn, and C3 ± 1 SE gives $386.3–465.4bn. Counted by each
person's share of Mexican-immigrant ancestry instead of whole, the lineage costs $274.9–374.8bn [FRAMING-SENSITIVE];
that reading stays beside the headline ([FAQ entry 19](immigration-objections-faq-2026-09-21.md)).

The label "cost to other residents" assumes that other residents carry the lineage's whole share of the federal
deficit that everyone runs together, because current law schedules no rule that closes the budget
[FRAMING-SENSITIVE]. Suppose the budget were closed by a permanent fix and the lineage paid its share. Take
Auerbach–Gale's 2026 current-law gap, net of the OASI shortfall the account already treats as cut on current law's
separate funds, split by household as AEI proposes. The cost to others is then $357.1–429.5bn, 7–8% below the
headline. Across current-law gaps and sharing rules it is $346.7–451.4bn
([lane](../infra/immigration-fiscal/closed_budget_2026_10_06/RESULT.md), FAQ entry 20). Most of the cost falls on
state and local budgets, which balance each year, so no federal fix shares it.

Beside the account:
- capital at 7%: $481–543bn;
- enterprises out: $372–439bn;
- land [GAP]: $3.6 / $6.0bn per 10% of land-to-structure value;
- congestion: $13.6 / $11.6bn now that roads grow; not recomputed for the added descendants;
- a typical budget year instead of 2024 (the average of 2015–2019 and 2022–2023, replayed on the back-cast): 10–20%
  less per member, $312–415bn at today's size ([FAQ entry 18](immigration-objections-faq-2026-09-21.md)).

Two known residuals are measured and left out of the headline, as too small to justify a new case: the 1.08M
lineage members priced as third-plus whites still carry the income tax they report to the survey, and five items
are summed on the survey's published weights instead of the account's 39.71M. Corrected, the case is
$387.1–462.3bn ($306.4–387.2bn counting benefits when paid; ladder 298). Out of scope: the cost of removing a
person, and an account of all unauthorized immigrants of every origin; each would be a new analysis.

The low side, with schools at the within-district 0.836, is $361–435bn. The outer range is $312–516bn ($354–484bn in
quadrature). The sign break-even is −3.7% to 5.4% of assigned service costs; a negative share means that end is a net
cost at every service response. The capital return is an imputed resource cost and never enters a debt flow, and
rental assistance moves who loses, not the budget ([audit](immigration-conceptual-audit-2026-09-27.md) §1). With
non-school education budgets fixed as well the case is $328–428bn, and with every service proportional $418–476bn.
The consumer lanes re-run on this case under the key `oct07`.

Inside the group, about one in six of the 42.75M members lives in a household that pays more than it costs: 17.5% / 14.2% with every line allocated, 24.2% / 22.7% counting only services a household uses itself and its own pension accrual. The 3.04M added descendants, whom the survey cannot see, are placed in the households of identified third-plus members of their own ages, band by band. Each worker carries the accrual that the case's pension model gives their on-books payroll taxes, and the payroll taxes follow on-books pay; spread per payroll-tax dollar instead, the shares are 17.0% / 13.1% and 24.6% / 23.0%. The accrual no longer charges retirees their current benefits, so working households cross zero and retiree households get cheaper. At the low end the share rises with the head's education (7% below high school, 39% with a BA or more) and generation (12% Mexico-born, 23% third-plus). The costliest tenth of households carries 49–56% of the net cost. Households headed by an unauthorized immigrant pay their way a little more often than those headed by a legal immigrant, 13.2% against 11.7%, only because the case credits the unauthorized with a tenth of the pension their taxes earn; with full claims the order reverses, 9.3% against 12.9% (ladder 268, [lane](../infra/immigration-fiscal/within_group_distribution_2026_09_29/RESULT.md)).

Why it costs what it costs: $104.95–158.93bn is what any 42.75M average residents would cost other residents under the same rules, mainly because governments spend more than they tax. The group's own excess over as many average residents is $284.13–302.55bn. Lower taxes at the same ages make up $256.35 / 249.09bn of it (90% / 82%); its age mix adds $19.09 / 63.99bn and its use of services at given ages +$8.69 / −10.53bn (ladder 269, [lane](../infra/immigration-fiscal/main_case_decomposition_2026_09_29/RESULT.md)). The added people sit at their measured ages, where 47% are children. Counting pensions as they accrue moves their cost to the working ages that earn them, so the young age mix no longer lowers the cost. On the cash set lower taxes exceed the whole excess (171% / 145%), and the age mix and service use reduce it. The case prices the account's 39.71M people plus the 3.04M added descendants, and per-member figures divide by that 42.75M (the CPS's raw 40.90M overcounts the Mexico-born outside California and Texas, ladder 209): it is $9,101–10,794 a year per member.

The average resident is not a neutral baseline. The average includes the lineage itself, about 13% of residents, so against everyone else the excess is larger by about 1/0.873, roughly $326–347bn [CALCULATION: excess ÷ (1 − 0.1274), the lineage's share of the account's 335.54M-person frame, `decompose.cjs:243`], and it also includes other high-cost groups. Third-plus non-Hispanic whites are a cleaner reference. Since October 7 every comparison group's income taxes take the case's own keys, which charge the whole national lines, the $422bn of federal and $45bn of state income tax the CPS misses, mostly at the top, included ([decision](../decisions/2026-10-07-comparators-income-tax-keys.md)). On those keys the whites about break even on accrual, between a $1.2k net contribution and a $54 cost a person; counting benefits when paid they cost others $0.7–2.0k, since 23% of them are 65 or older. Against 42.75M of them, $432–436bn of the lineage's cost is its own. The earlier rule charged each group only the income tax it reports to the CPS, which left the whites costing others $0.4–1.6k a person and the gap at $380–385bn. One convention still holds down what whites pay: with capital-side taxes also responding to the population, they pay $4.3–5.5k more than they cost, and the gap is $503–509bn (October 7 case; [lane](../infra/immigration-fiscal/white_replacement_2026_09_28/RESULT.md), ladder 263).

What would overturn the conclusions: on main case v6 one of the evidence map's nine claims splits by end, and the other eight hold. With pensions on accrual the group's direct taxes exceed its household transfers by $6.2bn at the low end and fall $5.3bn short at the high end, so "taxes cover benefits" holds at the low end and breaks at the high end. The 3.04M added descendants pay $9.9 / 8.0bn more in direct taxes than they draw in household transfers (rounded so the parts add); the identified members alone fall $3.7 / 13.3bn short. Services decide the sign only at the least adverse end, where a service response below 1.6–5.4% would flip it. The map states the gap against as many whites, on every group's income taxes at the case's keys, as $432–436bn against third-plus whites and $529–531bn against local whites, the second resting on a few top-income households. Within the accrual no swap moves it by a quarter (the old CPS-dollar rule −11.8%, capital-side taxes +16.6%). No premise swapped for its best-supported alternative breaks more than one: the first-year budget horizon breaks only the size (the case −26.5%, the pairing about −21%), counting the lineage by share of ancestry breaks it at its stated bound's low end (−30.0%) [FRAMING-SENSITIVE], and pensions back on cash restore "taxes cover benefits" and break nothing at the union's ages; at whites' own ages they break the white gap downward (−38.5%), the age artefact the accrual removes [FRAMING-SENSITIVE]. Next observations worth making: budgets after population outflows, and the Mexico-born on-books share from SSA and ITIN records (ladder 270, [lane](../infra/immigration-fiscal/break_conditions_2026_09_29/RESULT.md)).

How far to trust the review lanes: on 24 error cases and 24 sound claims, half of each taken from the project's own record and half synthetic mirrors of them, both caught every error when the evidence was in the packet. GPT-6 Astra (xhigh) also accused a quarter of the sound claims at 0.90–0.99 confidence, Opus 5.5 one in 24; three of those accusations (Astra's on V06m and V08m, Opus's on V08m) found real defects that the test's builder had put into two mirrors by mistake. Neither was measurably harsher on claims that make the group look costlier, though the test is too small to rule out a moderate bias. Treat an Astra accusation as a lead to verify (ladder 271, [lane](../infra/immigration-fiscal/reviewer_calibration_2026_09_29/RESULT.md)).

**Earlier cases.** Each main case replaced the one before. The first-year budget response is a named scenario
of the current account, not an earlier estimate: with CBO's year-to-year responses, no long-run
road, park or property-tax response and no capital return, it is $288.9–336.5bn, and $207.3–260.3bn counting benefits
when paid ([lane](../infra/immigration-fiscal/break_conditions_2026_09_29/RESULT.md), ladder 270).

| Case | Net cost to other residents | What it changed | Record |
|---|---|---|---|
| September 20, as published | $165.1–197.4bn | general government fixed, justice charged per head | [decision](../decisions/2026-09-20-category-service-response.md) |
| September 23 | $203.2–249.6bn | general government at 0.59–0.84; justice and uncompensated care keyed by use | [decision](../decisions/2026-09-23-main-case-general-government-and-use-keys.md) |
| September 24 | $200.9–246.3bn | dataset audit, pooled-MEPS medical figure, care, shelter keys, outside checks | [decision](../decisions/2026-09-24-main-case-audit-and-outside-checks.md), ladder 219 |
| First-year budget response (September 26) | $200.9–245.7bn | finite-removal responses (+$4.1 / +$3.4bn) and the consumption key (−$4.1bn), with CBO's year-to-year school response of 0.63–0.66 | [decision](../decisions/2026-09-26-main-case-finite-removal-and-consumption-key.md), ladder 229 |
| Schools case (September 26) | $258.5–292.0bn | schools at their full average cost per pupil (1.004 across 2019 districts, 0.973 across states); low side $233.9–269.6bn | [decision](../decisions/2026-09-26-main-case-schools-full-cost.md), ladder 230 |
| September 27 | $321.8–387.4bn | the return on public capital, long-run roads and parks, rental assistance, enterprises | [decision](../decisions/2026-09-27-main-case-capital-return-and-long-run-responses.md), ladder 237–239 |
| September 29 | $371.4–434.8bn | the pension accrual at payable benefits, long-run property taxes, the IRS income-tax key, state prices, roads by miles and five smaller keys; cash set $294.7–361.8bn | [decision](../decisions/2026-09-29-main-case-v4.md), ladder 275 |
| October 5 | $390.3–461.2bn | the 3.04M descendants who no longer report Mexican origin, counted as whole people (a 42.75M lineage); cash set $307.4–383.4bn | [decision](../decisions/2026-10-05-main-case-v5.md), ladder 281 |
| October 7 (current) | $389.1–461.5bn | the 2026 Trustees on separate funds, retiree health on accrual, the added people at their measured ages, user fees and the education keys; cash set $307.4–385.4bn | [decision](../decisions/2026-10-07-main-case-v6.md), ladder 295 |

[By generation](immigration-adopted-account-by-generation-2026-09-25.md) (ladder 224,
[lane](../infra/immigration-fiscal/generation_account_2026_09_24/RESULT.md)), all three Mexican-origin generations are
net costs at every specification under both ways of counting children, with the 3.04M descendants who no longer
report Mexican origin counted in the third-plus. Counted with their parents, as the National
Academies count them, the Mexico-born cost others **$169–197bn** a year ($16.0–18.6k per adult), the second
generation **$109–121bn** ($12.3–13.5k) and the third-plus **$111–144bn** ($11.3–14.7k); counted in their own
generation, $87–97bn, $150–178bn and $142–197bn. Per-person figures divide by the 42.75M lineage (29.27M adults,
the added people's at their measured ages).
The added people move only the third-plus; under the parents' count they stay in the third-plus, since their parents' generation is not observed.
The pension accrual follows this year's payroll taxes, so it lands mostly on the US-born generations. The split is
computed on the account itself, with no reference group, and is not the September 19 ledger's gaps against whites.

[Against 42.75M third-plus whites](../infra/immigration-fiscal/white_replacement_2026_09_28/RESULT.md) (ladder 263, both sides on the lineage's count, every group's income taxes on the case's own keys): the union costs other residents $432–436bn a year more once cash accounting's age artefact is removed, which the case's pension accrual now does (white rates at the union's ages on cash give $420–426bn); $263–270bn on raw cash at white ages; $529–531bn against local whites state by state (California $17.8k per member). That figure rests on few records: in Texas and California, 14 and 16 white households with AGI of $1M or more carry 50% and 38% of the comparison whites' federal income tax there after the IRS raking. Its white-side sampling error is about $33bn, against $14bn for national whites, and without the 10 largest-contributing households it is $453–456bn. The national key's split across states is not the cause: raking California and Texas to their own IRS state tax data moves the gap +$7.7bn ([fragility checks](../infra/immigration-fiscal/white_replacement_2026_09_28/RESULT.md), c61f00aa, 94dd712d). Per member the gap is $10.1–10.2k, below the identified members' $10.2–10.3k, because an added descendant costs less. Every comparison now keys Pell and public colleges by IPEDS enrollment on both sides; the earlier rough keys charged Pell by Social Security receipt, which put it on old whites, and the fix with item 4's tuition term adds $6.5–6.6bn to the gap. The difference is taxes, schools and transfers, not scale effects, and capital-side taxes held at zero response still understate what whites pay (see the reference paragraph above). [Connectedness](../infra/immigration-fiscal/connectedness_fragmentation_2026_09_28/RESULT.md) (ladder 262): counties with a larger Hispanic share have fewer cross-income friendships, mostly through residential separation; the payoff does not grow with county size, so no dollar figure. Reader-facing summary of the whole ladder: `infra/immigration-fiscal/overview_2026_09_28/` (`build.py` writes `derived/overview.html`; every new ladder entry must be placed in its `groups.py`).

Production is held fully adjusted while service responses vary; these transferred short-run assumptions do not
identify a long-run effect. The production term's perfect-substitution assumption has an executed sensitivity: a
[native–immigrant nest](immigration-production-term-nativity-nest-2026-09-22.md) gives +$17.9 / +$27.1bn at ε = 3
against the September 20 account's +$8.8 / +$13.3bn (ladder 176). The directly estimated low-skill elasticities
8.7–17.9 (ladder 181) give +$10–18bn, and the computed ε = 5 and ε = 7 about +$13–22bn; the file's job overlap fits a
value near 6 only through a sketch whose component elasticities are chosen. None is applied. Sampling plus donor error is about **±$10.20–10.47bn (1 SE)**,
and the 64 specifications' 95% intervals run **$369–481bn** together; C3's own error, beside them, widens the end specifications' interval to $368–483bn. The SE is a partial approximation whose net
error is unresolved (audit ffcce20 §A). Across constructions the assumptions dominate (ladder 184,
[uncertainty lane](../infra/immigration-fiscal/uncertainty_propagation_2026_09_22/RESULT.md)). With every service fixed,
the low end is still a net cost and the high end turns positive (the sign break-even above), and
service-quality effects remain unresolved ([response decision](../decisions/2026-09-20-category-service-response.md)).
"CBO-informed" means CBO's tax-incidence rules and the budget categories its scoring treats as responsive. The main
case goes further: schools at their full average cost (ladder 230), general government at 0.60–0.85 as a finite
removal (ladder 227), roads, parks, rental assistance and enterprises at their long-run responses, and property taxes at theirs (ladder 253). Defense,
existing interest and business subsidies stay at **zero response by assumption**, not by a CBO estimate
([scope memo](immigration-education-administration-scope-2026-09-20.md)).

[Real fiscal and social costs](immigration-real-fiscal-and-social-costs-2026-09-23.md) (ladder 188–193) prices the
channels the headline left out. Two are in the main case:
- courts, police and prisons by use, **+$5.9bn** ($1.7bn if Mexican-origin offending equals the Hispanic average
  as census codes record it);
- the government part of uncompensated hospital care, **+$3.7–5.7bn**.

Beside the fiscal account, a **fiscal-plus-social total** adds other residents' social costs and benefits:
**$489.0–570.7bn a year** at central values ($11.4–13.3k per member of the 42.75M lineage;
[decision](../decisions/2026-09-29-crash-item-with-against-without.md), ladders 266 and 274,
[lane](../infra/immigration-fiscal/sept24_propagation_2026_09_24/RESULT.md)). Counting benefits
when paid, it is $407.3–494.6bn. Its low
end assumes Mexican-origin offending equals the Hispanic average, its high end that it sits above that average
as custody does. The 3.04M added descendants' own rows, $8.4 / 8.5bn, take their share of each row's key
[ASSUMPTION]; every other row is on the 39.71M people the account identifies, and the crash and congestion rows
use the NHTS driving ratios per person aged 5+ (ladder 274,
[lane](../infra/immigration-fiscal/population_basis_2026_09_29/RESULT.md)).
It contains:
- crimes by group members against other residents, costing the victims $30.5–31.9bn ($15–45bn across the
  lane's arms; police records give $28.6bn, and the $43bn arrest-share arm fails a victim-count check, ladders
  202 and 218), and property crime, $1.3–1.4bn;
- unreimbursed hospital care, $3.1–5.3bn;
- the housing net, **+$0.7–3.4bn** to other residents, while their renters pay $22–58bn more ($30bn central once
  cheaper construction is counted, ladder 200);
- road congestion that remains once road budgets respond, $11.6–13.6bn in time and fuel (ladder 195);
- fine particles (PM2.5) from the group's consumption, $68.1bn ($30.8–119.7bn across the lane's grid), and road
  crashes with against without the group's traffic, $10.6bn (−$55.1bn to +$70.8bn); the crash figure charged by
  fault, $40.6bn, sits beside (ladders 264 and 266;
  [decision](../decisions/2026-09-28-social-items-pollution-crashes.md); ranges on the 39.71M,
  [lane](../infra/immigration-fiscal/social_spans_priced_count_2026_09_29/RESULT.md));
- fear and avoidance by non-victims $10.3bn, private security −$0.5bn and school disruption −$1.9bn, because
  Hispanic pupils are suspended less often than others; property values are 0, since a price discount is a
  transfer or already priced (ladder 258, [decision](../decisions/2026-09-28-social-items-fear-security-schools.md),
  [lane](../infra/immigration-fiscal/social_costs_unpriced_2026_09_28/RESULT.md));
- five benefits as negative costs, $35.4bn together: the scale net $13.7bn, restaurant variety $6.8bn,
  volunteering $6.0bn, trade and visit ties with Mexico $6.8bn and consumer-side scale $2.1bn (ladders 201, 261
  and 265; [decision](../decisions/2026-09-28-social-items-scale-benefits.md),
  [decision](../decisions/2026-09-28-social-items-more-benefits.md)).

Diluted instruction would cost other residents' pupils about **$16bn** a year in present-value lifetime earnings
(−$2bn to +$36bn) where school budgets respond less than fully. At the adopted response of 1 nothing is left
unfunded, so it applies only to the first-year scenario and is in no total (ladders 222 and 230;
[decision](../decisions/2026-09-25-school-dilution-priced-beside.md)).

For comparison, a rough re-key of the main case to non-Hispanic Black residents, with every group's income taxes
on the case's own keys, costs $501–549bn a year, $11.9–13.1k per member, 1.2–1.3× the Mexican-origin figure per
member of the 42.75M lineage; counting benefits when paid it is 1.4–1.6×. The pension accrual narrows the ratio because it charges the young Mexican-origin workforce's
accruing promises in place of its few retirees' benefits. Ladder 258's four
social items (fear, security, property values, school disruption) come to $51.0bn, and violent offences cost victims $185bn, $73bn of it outside the
group. This is not an engine run (ladder 259,
[lane](../infra/immigration-fiscal/black_comparator_rough_2026_09_28/RESULT.md)).

Wages move **$66–166bn** from less- to more-educated natives. The transfers are not added, but they run from poorer
to richer residents: outside the budget the bottom four fifths lose $80.3bn a year and the top fifth gains $45.4bn
(the lineage's production term scales the wage changes).
The fiscal cost is progressive if financed by tax shares and regressive if by equal cuts per person (ladder 194).
The fiscal channel is $415.9bn, of which $78.9bn is the pension accrual and $48.8bn the return on
public capital, and per-person cuts take 14.7% of the bottom fifth's resources; the capped programmes ($8.8bn),
including public housing, fall on eligible households that go without, $6.5bn of it on the bottom fifth.
The survey cannot find the 3.04M added
descendants, so they stay among the payers.

[Who wins and who loses](immigration-winners-and-losers-2026-09-25.md) (ladder 226) follows every priced channel
of the main case to persons. About one other resident in six comes out ahead: 17.5% under tax-share financing
and 16.8% under per-person cuts, with households pooled; 16.7% with wages going to the earner alone; 11–24%
across all choices. A minority ahead holds throughout; its size is conditional on incidence. Taxpayers' fiscal
channel is $415.9bn plus $8.8bn on capped programmes; its $78.9bn pension accrual falls on the future payers of
Social Security and Medicare, so the social net on today's residents is $378.6bn. The group's rows count the 42.75M lineage, the 3.04M added descendants placed at
the identified third-plus members' records of their own five-year age band [ASSUMPTION]. Nearly everyone in California and Texas, US-born adults
with high school or less, and renters come out behind. The top income decile and landlords come out ahead most
often. Where the state and local cost falls is the largest single choice:
charged nationally, the share ahead falls to 7.5%.

The [world ledger](../infra/immigration-fiscal/world_ledger_2026_09_27/RESULT.md) (ladder 250, 297) sets the main
case against the group living in Mexico, on the 42.75M people the case prices. Other US residents lose $471bn a year
in every reading, the fiscal cost plus the costs outside the budget, and more once raising the taxes is costed.
Adding everyone's dollars at equal weight, the
world gains $287bn in the recommended reading (Mexican pay in cities of 100,000+ at household prices, US pay at
state prices, the group's services at US prices) and $78bn in a low reading, which takes urban Mexican pay at the
70th percentile of selection (CMP's p70, against p56) and at common output prices, US health and social services
at Mexican prices and public goods at the cost of extending them [FRAMING-SENSITIVE]; on
national cells at GDP prices it is $321bn. That says whether the world is richer, not whether Americans are. The
pay gain is output, not a price artefact: valued at common prices industry by industry, the world total moves
+$2bn. Same-person pay is a parameter, not a reading: followed before and after the move, migrants gain 2.0 an hour
(1.59 a person) against the cells' 3.28, but that sample earned half the 2024 stock's US pay an hour; on the
recommended reading it gives $179–223bn, and CMP's 2.46 gives $255bn. The transfer leaks in part: raising
revenue costs payers 1.16–1.5 per dollar (at 1.16 the two readings give $27–243bn), and $61–62bn of the
$401–469bn direct cost buys the group nothing it values. Measured welfare weights rank the group's dollar above
the payers', not below. The added descendants' schooling is valued at zero, as every generation's is; over
generations the sign turns on how fast descendants catch up (ladder 154). The US plus the group comes out behind
only if the group's welfare counts for less than 0.74 of other residents' in the recommended reading (0.55
counting Mexico's residents); in the low reading it is behind at equal weights. On national cells, with every low
choice and λ 1.5, the world comes out behind by $31bn. That span does not charge the cost of raising revenue on the
pension accrual, which no tax raises this year. The second generation
costs other residents $150–178bn a year against a $252bn premium over being raised in Mexico. [FRAMING-SENSITIVE]

Benefits are priced to the same standard as the costs (evidence-symmetry rule 5). The
[care lane](../infra/immigration-fiscal/care_household_services_2026_09_23/RESULT.md) (ladder 198) puts **$4.1bn a
year** ($2.6–13.3bn) inside the fiscal account: native women's hours taxes of $2.7bn and an elder-care Medicaid
saving of $1.5bn net. Cheaper services, worth $21.8bn to consumers, overlap the production gain without being
reconciled with it, so they are neither added nor counted as included. The
[construction lane](../infra/immigration-fiscal/construction_housing_supply_2026_09_23/RESULT.md) (ladder 200) adds
nothing: the group makes construction 0.75% cheaper, which trims other renters' extra rent from $33.5bn to $29.9bn a
year, but that gain is inside the production term. The
[scale lane](../infra/immigration-fiscal/scale_spillovers_2026_09_23/RESULT.md) (ladder 201) measures city size and
schooling mix in one regression: bigger cities add $38.6bn to other residents' earnings and the group's lower
schooling takes back $24.9bn. Computed jointly, the net is +$13.9bn on the lane's CPS count, $0.2bn above the
parts' difference (95% −$56.6bn to +$84.4bn), and **+$13.7bn** on the account's 39.7M, which counts in the
fiscal-plus-social total; the 1970–2000 college-share studies would make it a $109–677bn cost instead. The
[mobility lane](../infra/immigration-fiscal/labor_mobility_insurance_2026_09_23/RESULT.md) (ladder 203) is worth
$0.65bn a year beside both totals: the Mexico-born no longer move more than natives within the US. The ancestry
instrument could not measure the congestion or wage slopes, so both figures stand (ladder 199).

The [dataset integrity audit](../infra/immigration-fiscal/dataset_integrity_2026_09_23/README.md)
(ladder 204 and 208–210) checks the inputs themselves: formatting, columns, implausible statistics and category
coding, across the CPS, ACS, spending and crime files. It was adopted into the case on September 24 (ladder 219),
with row 6 run through the engine, row 3 replaced by CBO's income-tax gradient and row 5 by the pooled-MEPS
figure. The defects are real, run both ways and nearly cancel:
- **Spending keys, net −$28.1bn.** ACA premium credits are keyed as EITC (−$14.2bn). Medicaid
  long-term care is keyed by a community-only survey (−$11.1bn; the group draws 7.4% of those
  dollars, not 12.25%). The education key over-weights K–12 (−$3.5bn).
- **Tax records that overstate the group's taxes, stacked: +$27.9bn / +$29.6bn.** The Census tax
  model assumes every respondent is a legal, fully compliant filer. The CPS fill-ins give the group
  too much income (ladder 208). Federal tax the CPS misses at the top is spread by CPS liability.
  Recounting the Mexico-born at the ACS level offsets part of this: ASEC 2025 counts about 1.2M too
  many, which is worth −$2.2–2.5bn once the tax corrections are in (ladder 209).

The [debt legacy lane](../infra/immigration-fiscal/debt_legacy_2026_09_23/RESULT.md) (ladder 207) prices interest
on the group's past federal gaps. On the cash-benefit convention, the 2005–2023 gaps leave $0.98–1.37tn of
modeled debt, with **$31.8–44.2bn** of 2024 interest under the all-borrowed rule ($744–1,033 per member of the 42.75M
lineage; $6.8–45.0bn across rules). The 3.04M added descendants follow the identified third-plus generation's path back in time; they add to the
2024 cash gap but lower its federal part, since they pay more federal tax than they draw. The pension accrual, the
capital return and the capped programmes are reported beside it, never compounded. Compounding the accrual as if it
were borrowing would give $64.0–74.2bn. That answers a historical question; the main
case's static comparison treats existing interest as sunk. These are conditional financing attributions; even the
cash-benefit convention retains NIPA's accrued public-employee compensation. They are stated as separate history
lines, since removing the group in 2024 leaves past obligations in place; they must never be added to the assigned
balance, nor the stock to an annual figure.

**Legacy comparisons, stated separately (September 30).** For the federal line, use 2005–2023:
annual ACS headcounts begin in 2005; earlier starts require more interpolation. Every comparison uses
the same headcount path, ending at 42.75M people (the 3.04M added descendants on the identified third-plus
generation's path, from 2005), and matched CPS/MEPS group keys, every group's income taxes on the case's own
keys. These are modeled
2024 annual charges over third-plus non-Hispanic whites, under the main case's paired specifications:

| Legacy component | Excess over whites, $bn in 2024 | Interpretation |
|---|---:|---|
| Federal gaps, accrued promises capitalized as if borrowed | **101.6–101.7** | Treasury-rate financing equivalent; **92.2–92.3** when accrual follows payroll rather than benefits |
| Public-employee pensions, service years 1980–2023 | **5.4** | Attributed interest expense on prior liabilities, including imputed interest |

The federal accrual levels on those matched keys are Mexican-origin $58.3–66.7bn, whites −$43.4 to −$35.0bn, and
an average-resident slice −$6.9 to +$1.0bn. The white negative is a modeled financing credit, not observed debt
repayment. The federal gap is $2.4k per member. Counting Social Security and Medicare when paid gives
$35.6–36.3bn over whites. Pell and public colleges are keyed by IPEDS enrollment on both sides; the earlier rough
keys charged Pell by Social Security receipt, and the fix adds about $4bn to the federal gap.
The pension comparison corrects stale comparator weights and uses the same keys on both sides.
**Do not sum the two rows:** the federal simulation retains accrued public-employee compensation,
so a common pension/borrowing reconciliation is still needed. Both stay outside the fiscal and
fiscal-plus-social headlines. [CALCULATION: [federal comparison](../infra/immigration-fiscal/legacy_comparators_2026_09_30/RESULT.md),
[pension comparison](../infra/immigration-fiscal/pension_legacy_2026_09_30/RESULT.md), ladders 278–279;
[source verification](../infra/immigration-fiscal/legacy_comparators_2026_09_30/verification-2026-09-30.md);
[decision](../decisions/2026-09-30-legacy-comparisons-separate.md); FRAMING-SENSITIVE]

The [status-benefits sweep](immigration-status-benefits-sweep-2026-09-24.md) (September 24) follows
the City Journal article on California. It covers benefits paid regardless of status, improper
payments, ITIN credits and migrant shelters in one table.
- California's Medi-Cal for undocumented residents costs **$10.8bn** a year from the General Fund.
  That is lawful spending, already inside BEA Medicaid.
- Other states add $1.0–1.4bn.
- Shelters cost five places $4.7bn in 2024.
- About $1.1bn of federal money was claimed improperly and repaid.
- No charged fraud tied to status was found.

The one keying mismatch is shelters. The account over-charges the group about $0.5bn, because
Mexican nationals were 0.50–0.84% of the people served. Federal fraud sentencing by citizenship
(ladder 214) puts noncitizens at 1.8–2.0 times the citizen rate per adult, the same as for their
other non-immigration federal crime. They hold 8.5% of government-program fraud loss, against 7.7%
of adults.

The [preferences lane](../infra/immigration-fiscal/affirmative_action_cost_2026_09_24/RESULT.md) (September 24,
ladder 213) prices what race- and ethnicity-based preferences cost non-Hispanic white natives: about
**$4bn a year** ($0.2–18.7bn), or $41 per white native worker, through admissions, contractor hiring and
set-asides. About 28% of it is tied to Hispanic beneficiaries. It is a transfer beside ladder 194 and
is not in the account.

[Rule-breaking competition](immigration-rule-breaking-competition-2026-09-25.md) (September 25,
ladder 220) asks whether employers who break labor and tax rules drive honest firms out. Paying a
worker off the books saves 11–24% of the wage; in construction, landscaping, janitorial services and
restaurants the edge is **$0–14.8bn a year** in 2024 (central $6.4bn, all origins), and $4.5bn of it
is payroll tax already inside the account; the Mexico-born half, $2.3bn of tax, is the part inside
the group's account. Covered establishments and employment grew no slower where the group's share
grew, and the pre-registered E-Verify design fails its pre-trend test, so no displacement of
compliant firms is measured. Beside the account: $0–2.2bn of workers' compensation premiums avoided
and $0–2.3bn of underpayment, both transfers from off-books workers to their employers. Street
vending (ladder 223): after California legalized it in 2019, licensed restaurants did not lose
ground where vending is common, a result about the law, which changed enforcement little, not about
the existing vendors; street food is about 1.3% of the City of Los Angeles's restaurant sales, at
most about $0.4bn a year statewide if all of it came from restaurants.

[Outside checks on the account's shares](immigration-outside-checks-2026-09-24.md) (ladders 215–218) test the keys
against data built independently of the account; they were adopted with the audit on September 24 (ladder 219). The
BEA closure (−$2,053bn) cannot catch a wrong key, because a wrong key only moves dollars between groups. Schools
(ladder 215): the group's districts and schools spend about 3.4% more than their states', and the case prices
pupils where the group enrolls. Taxes and transfers (ladder 216): CBO's 2022 income distribution and Treasury's
EITC shares by ethnicity corroborate most keys, each moving the case by $2.1bn or less (a materiality rule, not a
statistical fit; the agreement shares the account's within-bin origin shares, validation memo §4). The income-tax
key was too flat at the top and now follows CBO's gradient; scored on IRS 2023, which it never used, that gradient
overshoots at $200k–$1M, and the main case has matched IRS since September 29 (ladders 249 and 275). Benefits (ladder 217): administrative
records by ethnicity show no fear-driven under-reporting of SNAP or Medicaid; unemployment insurance, WIC and
TANF's California share are under-reported, and the case keys them on administrative records (+$2.2bn). SNAP's
quality-control file miscodes Hispanic ethnicity in 25 states and cannot support national SNAP-by-ethnicity
figures. Crime (ladder 218): the known errors lean one way in jail counts, bookings and the victim-harm count, not
in the offending ratios; the NIBRS murder ratio stays at 2.30, and crimes by Hispanic offenders are reported to
police more often. Consumption (ladder 225): keyed on what households at each income rank spend (CE 2024), net of
remittances, the group pays more of the $1,198bn of consumption-keyed receipts (−$4.1bn); CBO's excise
distribution, ITEP's gradient and Mexican-origin CE units support the direction. Finite removal (ladder 227): read
as the removal of 12% of residents, general government's cross-state elasticities save 0.60–0.85 of average cost
([lane](../infra/immigration-fiscal/finite_response_2026_09_26/RESULT.md)). Both were adopted on September 26;
finite removal's school part was superseded the same day by full average cost (ladder 230).

[Objections and answers](immigration-objections-faq-2026-09-21.md): eighteen standard
objections (age, fixed public goods, payroll taxes without benefits, off-budget gains,
second generation, reference group, education, single year, legacy cohorts, ageing,
policy reading, crime, elder care, native–immigrant complementarity, California vs Texas,
CBO's surge projection, survey reliability, whether 2024 was an unusual year), each
steel-manned and routed to its executed table.

[California vs Texas](immigration-california-texas-fiscal-geography-2026-09-21.md):
same Mexican-origin share (~32%); common-age gap vs **local** whites **−$15,228** (CA) vs
**−$9,267** (TX) on the shared all-age ledger with the income tax the survey misses; LA **−$21,083**, Houston
**−$8,977**. With taxes as the survey reports them, −$12,133, −$7,479, −$17,196 and −$7,493; the ten largest white
households carry most of the added tax in each state. Share does not produce the coastal dollar gap. Not the main-case account. NY is 1.4% of US
Mexican-origin; SF has no single-metro gap.

[Why US-born adults leave California](immigration-housing-supply-ca-tx-2026-09-22.md) §8
(September 25, ladder 221): they name jobs (38%), family (27%) and housing (19%) as the main
reason, and cheaper housing 2.2 times as often as other states' leavers, in every race,
education, income and age group. "Better neighborhood/less crime" is **1.47%** (other states
1.90%), and white and Mexican-origin leavers differ from other states' leavers by the same
amount. These are reason shares among leavers, not leaving rates; a composition effect acting
through housing costs or schools would be reported as housing or schools. Each year's net cohort
takes $0.63–1.05bn of California state and local tax to other states, gross of the spending that
moves with it.

[Seven papers from the Marginal Revolution archive, read in full](immigration-marginal-revolution-leads-read-2026-09-21.md):
headline unchanged. Counting US-born aides, the nursing-home channel reaches the group and nets about $1.5bn a
year of Medicaid saving, inside the main case (ladder 198). The 2025 municipal-bond paper cannot identify the
service-response share. The production term's perfect-substitution assumption is executed (ladder 176): at the
direct estimates of ladder 181 the term rises $1.5–4.7bn, and at ε = 5 to 7 by about half, to roughly $13–22bn (on the
September 20 account). The removal model's $27–80bn is a different population and a
different elasticity (ladder 166).

[Cumulative 2005–2024 back-cast](immigration-historical-backcast-2026-09-20.md): no past year is measured. Actual
BEA budgets, each benefit programme's own series and ACS population by year, with the 2024 relative position held
or income-adjusted, give **$3.4–4.4tn (10y), $4.8–6.4tn (15y) and $5.8–8.1tn (20y)** under the
whole-budget rules, 2024 dollars, no interest, of which the return on public capital is $0.3–0.6tn over ten years.
The 3.04M added descendants follow the identified third-plus generation's count back in time. The October 7 case's items leave all three windows unchanged at this
rounding.
The group got the pandemic payments at 0.87–1.03 times other residents per person, not at the 2024 credit ratio
of 2.34 (ladder 251). Measured trend (ACS): per-capita income 0.52→0.61 of the national figure over 2008–2024,
median household income 0.78→0.91, full-time men's earnings 0.64→0.75 with the gain in 2016–2019 and 2021–2023
and none in 2024. Model ranges, not intervals; a measured series needs the account rebuilt on each ASEC file.
Not comparable with ladder 137's forward debt path.

[Executed service-scaling test](immigration-service-scaling-test-2026-09-20.md):
school panel spending elasticity .735 unweighted/.836 pupil-weighted; across-district
prediction favors proportional spending over universal 3/4 or 5/6. Ten state-service
within-panel estimates are imprecise. Complexity theory supplies an exact finite-cost
sensitivity, not another discount on the CBO-informed account.

[Policy effects and new administrative outcomes](immigration-policy-causal-evidence-2026-09-20.md)
checks Secure Communities victimization/reporting, Mariel school spending and
H-2B employer benefits; records the direct Mexican-inflow crime replication route.
Adds a verified 72 MB BEA/IRS county panel, with source units, missing years and
geographic coverage preserved. Immigration-only offenses carry no automatic
victim-harm charge. These findings do not change the conditional national total.

Scope checks: [education and administration](immigration-education-administration-scope-2026-09-20.md)
shows which staffing costs are already included and isolates the general-government
response assumption. The [executed state/local response test](immigration-administration-response-test-2026-09-20.md)
is too imprecise to identify an actual fixed/variable share; the 25% illustration
remains an assumption. [Fourth-generation coverage](immigration-fourth-generation-scope-2026-09-20.md)
now separates observed G3 (2.870m) and G4+ (2.073m), leaving 9.399m unresolved
within the existing G3+ total. Additional checks find 25–32k adjacent-year CPS
candidates and an independent GSS adult benchmark; neither imputes the residual.
Exact G4 versus G5+ remains unmeasured. No fiscal total changes.
[Age-adjusted generation estimates](immigration-later-generation-estimates-2026-09-20.md)
give 3.51–3.83m generic G4+ adults under central assumptions; missing-age and
grandparent scenarios span 2.71–4.71m before sampling error. Historical Pew is
lower, and PSID exact-generation completeness awaits authenticated data access.
[Ancestry and outcomes](immigration-ancestry-outcomes-evidence-2026-09-20.md)
adds a direct Pew schooling comparison of identifiers and nonidentifiers, the
newly acquired historical MASP family data, and the verified SIPP linkage route.
It supplies no national all-descendant fiscal or crime correction.
Later same-day execution completes MASP/Pew sensitivities and stops this search:
public SIPP birthplace fields are region recodes, relevant samples are small,
and PSID's current conditions prohibit the proposed AI use. See the linked
ancestry-outcomes memo's continuation and [stopping decision](../decisions/2026-09-20-ancestry-outcome-data-ceiling.md).
[Program-fraud trace index](immigration-fraud-trace-index-2026-09-20.md) links SNAP,
childcare, adult-day and hospice cases to records, separating paid losses, billings,
allegations and duplicate fiscal attribution. No fraud adjustment has been estimated.

Preceding partial account: [four executed fiscal checks](immigration-four-fiscal-checks-2026-09-20.md).
Measured public-school enrollment raises the partial deficit to **$259.38bn shared
/$283.20bn personal**. Matched-year tax units locate the national income-tax
shortfall mainly at high incomes; healthcare and national-account checks retain
material unresolved scope/attribution. These are all-age resident balances,
not policy effects or confidence bounds. [National coverage detail](immigration-national-coverage-execution-2026-09-20.md).

Gap diagnosis: [which assumptions should change and better data](immigration-gap-diagnosis-and-data-2026-09-19.md)
decomposes the school discrepancy: the fixed enrollment rate explains 63–64% of
the all-child CA/TX shortfall and almost all the national Hispanic shortfall.
Verifies the public October CPS enrollment route, matched-year tax comparisons,
health-data boundaries and restricted-access limits. National accounting coverage
remains the larger completeness issue; execution is linked above.

Executed reality checks: [administrative earnings, benefit totals and pupil counts](immigration-administrative-checks-2026-09-19.md)
compare the uncalibrated model with unused official observations. National wages
are 2.25% above SSA employer records; wage-recipient and payroll coverage still
differ. The receipt-gap mechanism survives this check. Pupil exposure and older
benefit-reporting factors need refinement; the memo separates raw errors from
uniform-calibration sensitivities. These do not validate a causal ethnic cost.

Test design: [necessary fiscal implications and administrative tests](immigration-fiscal-reality-checks-2026-09-19.md)
shows that the current partial account assigns lower receipts **and lower spending**
per Mexican-origin resident than per other resident. Priorities are tax/earnings
distributions, current transfer totals, Medicaid eligibility costs and public-pupil
counts; CA/TX records and source-reuse limits are linked. Read the executed results
above for the outcome; exact state administrative-eligibility matching remains unavailable.

Previous three checks: [observed2024 fiscal refresh and national reconciliation](immigration-macro-reconciliation-2026-09-19.md)
produced the **$234.34bn shared/$256.26bn personal** annual version, superseded by
the September20 enrollment correction above;
[matched skill/capital/tax benefits](immigration-matched-benefits-2026-09-19.md)
gives $6–19bn long-run production gains in the source-centered grid, with larger
conditional capital-tax effects requiring ownership/overlap accounting;
[projection back-tests](immigration-projection-backtest-2026-09-19.md) find the
NRC debt rule failed, no general optimistic schooling bias, and material
education/parentage/exit sensitivities. These govern the older releases below.
They are calculation notes, not a complete net-cost estimate or narrative essay.

Education-specific fiscal evidence: [annual comparisons, lifetime uncertainty and methods](immigration-education-fiscal-and-methods-2026-09-19.md) separates below-HS from HS-only, five origin regions, current stocks and recent arrivals; retains same-education and all-education native references. Adds joint survey uncertainty, material healthcare-matching tests and explicit institutional-cost scenarios. Below-HS Mexican-born adults do at least as well as below-HS natives at common ages (with the income tax the survey misses, the advantage holds only with household costs shared), while HS-only do worse; this qualifies blanket origin-based rankings. These remain resident-account models, not admission effects.

Earlier repaired fiscal profiles: [yearly and lifetime results](immigration-yearly-lifetime-cost-repair-2026-09-19.md). The ledger's annual totals (−$203.52bn / −$223.94bn with item T) are superseded for annual totals by the finance refresh and September20 school correction above. Lifetime comparisons retain pinned age profiles, conditional survival and explicit discount/allocation assumptions; they are not validated admission forecasts. The [September19 cross-check](immigration-five-day-cross-check-2026-09-19.md) and birth-versus-arrival budget remain superseded/withdrawn. Narrative and essay writing are operator-owned.

[Practitioner range for the September 19 ledger](immigration-ledger-practitioner-range-2026-09-22.md):
the conventions a budget modeler would run put the union's annual expanded balance at
**−$277bn to −$176bn** around −$204bn with item T (ladder 172); the full 63-cell design spans −$482bn to
−$62bn, and the −$548/−$87bn range still printed in the ledger's RESULT.md is the stale
September 17 build. Public goods per capita is a second object (−$488 to −$388bn). Convention
hulls, not confidence intervals.

Consistent accounting and raw histories: [all-age fiscal and later-generation findings](immigration-all-age-and-lineage-findings-2026-09-17.md) rebuilds the expanded account on one population with CPS/MEPS uncertainty, tests fixed-budget attribution and common ages, and reconstructs IIMMLA generations/outcomes. Large benchmark shortfalls persist; absolute partial balances, allocation effects and outcome-specific generation differences are reported separately (ladder 123–124). Within-state and metro matching, with the income tax the survey misses: CA **−$15,228** / TX **−$9,267** vs local whites; LA **−$21,083** (−$12,133, −$7,479 and −$17,196 with taxes as the survey reports them; ladder 125, 128). Pair with the [CA–TX geography note](immigration-california-texas-fiscal-geography-2026-09-21.md).

All-age claim audit: [fiscal benchmark gaps, remittances and later generations](immigration-aggregate-and-generation-audit-2026-09-17.md) reproduces the $212bn/$153bn partial-account differences, exposes their positive absolute balance, and corrects the remittance ceiling and incompatible ancestry definitions.

Country comparisons: [five-year LATAM economic comparison and dataset expansion](immigration-latam-benchmark-comparison-2026-09-17.md) uses explicit birthplace benchmarks, first/second generations, common age/sex standards and survey uncertainty; distinguishes measured economic gaps from crime, trust, fiscal and genetic claims.

Expanded transfer check: [other LATAM countries, distance selection and the Somali counterexample](immigration-latam-selection-transfer-2026-09-17.md) compares origin/cohort outcomes and narrows the earlier BA-share selection interpretation; distinguishes evidence for individual genetic effects from unsupported genetic attribution of migrant-group differences.

Origin scope and trust: [LATAM, Southeast Asia and social trust](immigration-latam-southeast-asia-trust-2026-09-17.md) checks the latest located unauthorized-origin stock estimates, limits Mexican-to-LATAM extrapolation, separates Southeast Asian economic outcomes, and weighs local cooperation costs against claims of inevitable or centuries-long trust decline.

Latest executed frontier: [stronger findings and remaining limits](immigration-frontier-execution-2026-09-17.md), with [reproduction and coverage](../infra/immigration-fiscal/frontier_execution_2026_09_17/README.md). Adds official NLS variance validation and adult outcomes, three-year disability and full-denominator trust, NYC exposure accounting, fiscal reconciliation, raw-mirror Bracero wage reconstruction, and bounded H-2B/automation/institutions checks (ladder 115–120). These qualifications govern earlier score, trust, disability and fiscal headlines.

Research priorities: [stronger questions across domains](immigration-research-question-frontier-2026-09-17.md) separates verified descriptions, policy identification, transfer and value judgments; ranks remaining score, selection, incidence and causal-design work; and marks cultural/institutional/environmental questions needing their own outcomes.

Latest completed collection analysis: [organized surveys and conclusions](immigration-organized-surveys-analysis-2026-09-17.md), with [NLS parent reconstruction](immigration-nlsy97-parent-linkage-2026-09-17.md), [Pew generations and denominators](immigration-pew-generation-denominators-2026-09-17.md), and [public LNS author replications](immigration-lns-public-replications-2026-09-17.md). These update the earlier audit below (ladder112–114). [Named local library](../infra/immigration-fiscal/new_datasets_2026_09_17/library/README.md) accounts for the downloads and their duplicates.

Latest supplied-data audit: [immigration-new-datasets-and-conclusions-2026-09-17.md](immigration-new-datasets-and-conclusions-2026-09-17.md) covers all13 files, valid joins, Pew ancestry selection, NLS export gaps and recovered outcomes, GSS coding repairs, and corrections to CILS/IIMMLA floor/parity interpretations (ladder107–111).

| File | Topic | Consult before |
|------|-------|----------------|
| `immigration-political-trajectory-county-panel-2026-09-19.md` | County panel 2000–2024: Mexican-origin share growth has no effect on Democratic share or turnout with state×year FE; composition worth +0.29 points nationally vs −2.80 from the group's own swing; CA–TX gap is conversion not composition (66 vs 23 in low-Mexican counties); tuition laws track group size, restrictive laws track the rest of the electorate | Any "they vote us into X" or vortex claim; the input side of ladder 97/102; the CA–TX comparison |
| `immigration-lineage-cost-century-2026-09-19.md` | Historical conditional −$1.48M white-reference lineage gap (with item T); incomplete coverage, 101 original intervals, no validated admission cost. Current projection checks qualify education, parentage, policy and exit assumptions. 2026-09-25: "legal status is nearly irrelevant" withdrawn; under statutory senior eligibility, legalising at year 10 widens the gap by $418k. 2026-09-26: with emergency Medicaid, state programs and uncompensated care priced it still widens it, by $355–390k under the rules a new enrollee faced in 2026 and $250–400k across the rules of 2020–2026 | Any lifetime/lineage figure; read projection checks first |
| `immigration-mexican-origin-population-total-2026-09-19.md` | Mexican-origin population by generation: 40.97M self-ID, 42–45M with attrition and coverage (floor 41.8M), 44.0–46.3M adding identity loss past G3 (ladder 158); Duncan–Trejo attrition reproduced and found halved (third generation 11% vs 28%); ancestry question gives fewer, not more; attriters narrow the per-person gap by about $240 (−$8,218 → −$7,981 on the population lane's base with item T, measured generation split) | Any total for the Mexican-origin lineage; any attrition correction; the 0.82 coverage-ratio trap |
| `immigration-unauthorized-population-size-2026-09-19.md` | Unauthorized stock by definition (broad 14.6–16.7M for 2024–25, narrow 8–9.5M), coverage grid (PES 4.99% vs CMS 22%; ACS/CPS weights already embed the 2024 migration revision), stock-flow 16.7M for Jan 2025, falling since; no definition reaches 40M | Any unauthorized headcount; any claim of 20M+ or 40M; comparing the CPS residual to gross inflows |
| [Parents' legal status by education](../infra/immigration-fiscal/parent_status_2026_09_23/RESULT.md) | 2026-09-23, ladder 185: Mexico-born parents of US-born minors, imputed unauthorized: below high school 47–62% (1.51M parents), high school 37–52%, all 38–51%; US-born minors in the lowest-education Mexican families with no legal parent present 45–62%, all 30–41% (5.0M children). Current status, not status at birth; range is the Medicaid rule. Ladder 186: their US-born children do worse while parents stay unauthorized (poverty +10–20 pts, college −12–14 pts at 18–24, CPS 2025) and match legal entrants' children once parents legalized (IIMMLA 2004). Ladder 187: of Mexican adults getting green cards in 2003, 55% had once entered without papers and 77% of those used 245(i), closed to post-2001 petitions; about 1% of unauthorized Mexicans legalized that year; 2026 routes need a citizen or resident spouse or parent (I-601A, interview abroad), cancellation of removal (4,000 a year) or a U visa (288k pending); a US-born child cannot waive a parent's ten-year bar | Birthright-citizenship questions; any claim that low-skill parents are almost all unauthorized; "children of illegals do worse/better"; "how easy is it to get legal status" |
| `immigration-cultural-output-and-variety-saturation-2026-09-19.md` | Creative labour per head at matched SES 0.72–0.74 of whites (music at parity), awards 0.47→0.65 of the BA+ benchmark, Mexican-restaurant variety elasticity 0.18 in group share (saturates by a 10–20% local share; national counterfactual not identified), 12% of US cooks Mexico-born, Latin music 8–9% of revenue | Any "cultural enrichment" or "contributes nothing" claim; any argument that variety benefits scale with population |
| `immigration-hedonic-replay-2026-09-19.md` | Original-data replay recovers all six historical coefficients/SEs and stronger IV diagnostics; matched historical means and medians both negative. Modern exercise is not equivalent; old custom J output disabled | Read before claiming a replication failure, era change or identified composition-amenity price |
| `immigration-hedonic-composition-amenity-2026-09-19.md` | Contemporary housing sensitivity exercise: matched ACS/Zillow outcome sensitivity and no identified amenity dollar price. Exact-reproduction and established measurement-explanation claims superseded by the replay note | Any attempt to dollarize neighbourhood composition or reuse Saiz–Wachter's historical estimate today |
| [Clemens–Pritchett calibration](immigration-clemens-pritchett-calibration-mexican-origin-2026-09-19.md) | Equations and parameter sensitivity reproduce; earnings/fiscal/attitude substitutions do not measure the paper's TFP-assimilation rate, so the negative optimum is conditional | Reusing the new institutional-transmission framework |
| `immigration-local-spending-composition-2026-09-18.md` | Local-budget associations do not show the predicted law-and-order shift; failed IV does not prove a null and treatment differs from unauthorized-arrival study | Claiming causal spending effects or a replication failure |
| `immigration-ncvs-victim-offender-off-the-murder-margin-2026-09-18.md` | Victim/perceived-offender distributions; corrected Hispanic $90.91 annual CJS scenario reproduces, but severity is imputed and victim ethnicity does not identify taxpayer incidence; age adjustment is a proxy | Separating measured incident distributions from cost scenarios |
| `immigration-apportionment-seats-attributable-2026-09-18.md` | 24-seat fixed-location count counterfactual for Mexican-origin residents; depends on size and uneven geography; not ethnic seat ownership or an immigration-policy/election effect | Representation counterfactuals |
| [Non-citizen voting evidence](../notes/noncitizen-voting-evidence-2026-09-19.md) | Primary-source review, 2026-09-19, plus Block 8 of 2026-09-23 (Reuters: >30,000 error registrations since 2000, ballots unknown). Real but mostly motor-vehicle errors that registered people who had declared non-citizenship; about 300–3,000 ballots per federal election; counted ballots 5.8 per million (PA 2000–17) to 22 (IA 2024); flag counts overstate (IA 87% of flags were citizens). Not a fiscal item. Qualified 2026-09-25: the 9,000–24,000 figures are ceilings on detected voting, not upper bounds, and the closest House margins (Iowa 2nd 2020: 6 votes, 0.0015%) sit at or within reach of them; no contest is shown decided | Any non-citizen voting, voter-roll or election-integrity claim |
| [Current yearly/lifetime calculation index](immigration-yearly-lifetime-cost-repair-2026-09-19.md) | Repaired program ownership, personal/shared annual balances, actual-age survival NPVs, real discounts and explicit unresolved coverage | Reusing any September yearly or lifetime scalar |
| [Practitioner range, Sept 19 ledger](immigration-ledger-practitioner-range-2026-09-22.md) | 2026-09-22, ladder 172: with item T, practitioner hull −$277 to −$176bn around −$204bn; design hull −$482 to −$62bn (+$55bn with the dial at zero); public-goods object −$488 to −$388bn; stale 144-cell range stamped | Quoting any range for the ledger, or choosing between its conventions |
| [Elderly public medical by ethnicity, MCBS 2023](immigration-elderly-medical-by-ethnicity-2026-09-22.md) | 2026-09-22, ladder 173: Hispanic/white public payments at 65+ 1.27 (CI 0.97–1.56), total spending equal, Medicaid 9×, income reverses the sign; with the MEPS Mexican-origin check (ladder 175) the 65+ ethnicity dimension is unsigned, about −40% to +56% | Any claim about elderly medical cost by origin; the re-aged and lifetime 65+ cells |
| [Mexican-origin medical on the transport's MEPS file](immigration-mexican-origin-medical-transport-check-2026-09-22.md) | 2026-09-22, ladder 175: Mexican-origin/all-donor public spending 0.89 at 65+ (CI 0.61–1.18), 0.69 at 18–64 (excludes 1); Medicaid 3.3× but Medicare, out-of-pocket and private lower; 65+ translation $2.7bn less (SE 6.7); all-ages unusable (one record) | Any ethnicity adjustment to the medical transport; read with the MCBS row |
| [Pooled MEPS medical by ethnicity, 2016–2024](../infra/immigration-fiscal/medical_ethnicity_pooled_2026_09_23/RESULT.md) | 2026-09-23, ladder 206 (supersedes 175's 0.69): union-weighted cell ratios children 1.38 (1.16 winsorized), 18–64 0.92, 65+ 0.88, all ages 1.00; ledger medical +$0.15bn (SE 10.4); account Medicaid line +$13.6bn and Medicare −$9.9bn, five lines −$3.0bn (SE 8.0); nursing-facility Medicaid over-charged $4.0–6.2bn by the community key; the +$68.7bn coverage-key stress rejected (19.4% of covered, 13.5% of dollars); MCBS 65+ conflict open | Any ethnicity adjustment to medical charges; adopted in the main case on 2026-09-24, with long-term care charged by use; the MCBS 65+ ratio is open |
| [Production term under imperfect substitution](immigration-production-term-nativity-nest-2026-09-22.md) | 2026-09-22, ladder 176: native–immigrant nest inside the skill cells doubles the production term at ε = 3 (+$27.1 / +$17.9bn GDP / cash against +$13.3 / +$8.8bn); natives +$54bn, other foreign-born −$46bn, about 85% nets out. Job overlap fits an elasticity near 6 only through a sketch with chosen component elasticities (about 4–9), an illustration, not an estimate; the computed neighbors ε = 5 and ε = 7 give +$21.5 / +$14.2bn and +$19.2 / +$12.6bn. Union-as-own-branch variant structurally unverified; headline band not re-run | Any reading of the account's production term or the removal-model comparison (FAQ 14) |
| [Return migration selectivity, ENADID 2018/2023](immigration-mexico-return-migration-selectivity-2026-09-22.md) | 2026-09-22, ladder 174: returnees from the US hold about one year less schooling than Mexico-born stayers (tertiary −12 to −14 points), men only; short-window returnees are better educated (22–28% tertiary); departures unmeasured on schooling. Qualified 2026-09-25: against Mexico non-migrants only; the sign against emigrants who stay in the US is not established. Measured 2026-09-26 (ladder 228, §7): returnee men hold 6–8 points less tertiary schooling than Mexico-born men still in the US (about half from stayers who arrived as children); exit raises the stock's tertiary share by 0.13–0.23 points per five-year window. ACS no-schooling reports step up between 2019 and 2020 | Any attrition or exit assumption; reading US arrival-cohort education trends |
| `immigration-lifetime-longevity-and-social-security-timing-2026-09-18.md` | Historical mortality/timing study; flat-shift results superseded by current calculation index; invalid SSA accrual adjustment disabled | Tracing earlier lifetime claims |
| `immigration-marginal-revolution-claims-audit-2026-09-18.md` | Source archive and commentator comparisons; schooling-loan HARD grade and claim totals withdrawn by the September 19 audit; resident accounting is not a full cost-benefit analysis | Reusing a commentator rebuttal |
| `immigration-first-generation-crime-cost-weighted-2026-09-18.md` | Texas all-age cost-weighted foreign-born charge ratio 0.79 vs all US-born; adult/18–39 versions change denominators only; DHS-record explanation corrected | Comparing status, age and charge denominators |
| `immigration-new-conclusions-audit-2026-09-17.md` | Adversarial correction of fertility, automation, disability, agglomeration and political-cost conclusions; proposed family-migration-history classification with public/restricted data limits | Reusing ladder 93–97, the political dollar range, or “third generation” as a complete ancestry category |
| `immigration-clarity-update-2026-09-05.md` | September 5 integrated findings, the entry point before the complete account: fiscal account, Black wage/crime groups, missing residents and recording failures | Answering what the completed audit and data expansion established |
| `immigration-second-order-effects-2026-09-05.md` | Concise evidence by mechanism: incumbent welfare, capacity, institutions and conditional restrictions | What second-order costs establish, and what remains unmeasured |
| `immigration-fiscal-account-2024-2026-09-05.md` | CPS2025 taxes/credits/transfers, MEPS2024 health and actual public-pupil exposure | Comparing annual fiscal components beyond the older payroll proxy |
| `immigration-measurement-uncertainty-2026-09-05.md` | Missing status versus missing people; two-sided selection and crime recording thresholds | Treating untracked residents or selective enforcement as a settled correction factor |
| `immigration-wage-race-strata-2026-09-05.md` | ACS2019/2024 race × nativity wages, earnings, employment and worker-only estimates | Pooling Black, White and Hispanic native/foreign-born wage populations |
| `immigration-crime-race-ethnicity-2026-09-05.md` | BJS2022/2023 imprisonment rates and SPI2016 joint prisoner composition | Separating Black people in crime statistics or treating White as non-Hispanic/native |
| `immigration-crime-statistics-bias-mechanisms-2026-09-16.md` | Mechanisms by which immigrant-vs-native crime statistics mislead: status-identification timing, residual relabelling, exposure denominators, immigration offences as crime, non-recording of ethnicity; signs and magnitudes | Citing any immigrant/native crime ratio without its extract date, denominator definition and offence scope; evaluating "police won't record" claims |
| `immigration-generational-crime-mechanisms-2026-09-16.md` | Why first-generation immigrants offend less than the second: 2018–2026 within-family, survival, register and quasi-experimental evidence; the gap is an adult-arrival floor; mechanism scoreboard (legal status, parental resources, peers, selection, culture, measurement); European age-standardization and widening residuals; new angles | Any claim about "the second generation" and crime, generational assimilation, age at arrival, or what causes the first-generation advantage |
| `immigration-mexican-origin-generation-incarceration-2026-09-16.md` | Central memo, §1–§18 (ladder 65–97, corrections 98–103, then 104–106): the 3.5× recomputed (1.7–1.9×, 1.68× pooled 2020–24); generation shares; origin cells; offence mix; EU data regimes; Pueyo repro; mechanisms and the origin-mean regression; the September 16 extended per-adult-year ledger (historical; the ledger's same-age second-generation gap is −$8,499) (−$8.3k to −$8.9k second generation, status split, residuals, remittances, disability); housing/capacity/schools/coercion/agglomeration; consumption and wealth; attitudes by generation; automation (unpriced); political externality (proposed dollar range withdrawn by September 17 audit) | Any "second generation counted as native" argument, the 3.5× figure, or a Mexican vs other-origin comparison |
| `immigration-secgen-origin-divergence-mechanisms-2026-09-16.md` | Why second generations diverge by parental origin: ranked mechanisms with identification grades (parental legal status 1.24 yr IRCA-IV; parental English A− IV; attrition both directions; selectivity small at individual level; no identified ethnic-capital or resettlement estimate; family structure wrong sign); five CPS/ACS tests | Any claim that culture, discrimination, selectivity or legal status explains an origin gap in second-generation outcomes |
| [Indian-origin residents: treasury, coordination, giving, vote](immigration-indian-origin-fiscal-coordination-politics-2026-09-18.md) | Favorable working-age partial-ledger contrast; raw/conditional civic participation and approximate uncertainty; cross-survey education benchmarks do not identify a voting decomposition; adjudicated favoritism limited to one firm | Origin comparisons on matched accounts and civic populations |
| [Indian 2nd/3rd generation at white ages](immigration-indian-later-generation-fiscal-2026-09-21.md) | 2026-09-21: G2 age-std gap **+$23,692 (se 5,482)** on the 2025 extended ledger; G3+ race/ID n=49, **+$11,806 (se 8,150)**, does not reject white parity; 5-year own-tax G3 **+$4,101 (se 3,880)** with 2023 below whites; ACS US-born Asian Indian 25–64 mean PINCP **+$59k** vs US-born NH whites, 65–80 cell below. IT mix is **8%/4%** of the CPS-G2 / ACS-ancestry employed-earnings gap; dropping IT leaves G2 at +$47k. H-1B is G1 only (proxy 30% of India-born 25–64, lowest-net G1 arm) | Same-age Indian descendant fiscal claims; “they only look good because they are young”; treating native self-ID as G3; “it’s all software/H-1B” |
| [Generational trajectory: Mexican and Indian origin, G1 to G4+](immigration-generational-trajectory-mexican-indian-2026-09-27.md) | 2026-09-27, ladder 232–236: G1→G2 carries ~half the distance from the white mean across 78 origins (slope 0.52 education); Mexican gap then stalls (G2→G3+ ρ ≈ 0.86 once the hidden third generation is put back, its closing share measured on 526 G3 non-identifiers in the CPS basic monthly files 1994–2026; identity loss explains about 6% of the ratio and cohort about as much, [lane](../infra/immigration-fiscal/carryover_identity_2026_09_27/RESULT.md); G4+ no better than G3); turnout −10/−9 at equal SES, endogamy 90→72→56%; attachment to Mexico fades (very connected 50%→7%), nationality by descent unlimited since 2021; IR-5 parent $267–285k at 3%; Indian advantage a whole-distribution shift, 94% of the fiscal gap survives dropping the top 1% | "They'll regress/assimilate by the third generation"; "it's the top 1%"; dual nationality; sponsored parents |
| [Pooled G3 non-identifier test](../infra/immigration-fiscal/g3_identity_pooled_2026_10_05/RESULT.md) | 2026-10-05, ladder 280: IPUMS-CPS basic monthly 1994–2026 (526 unique G3 non-identifiers at 25+; the ASEC frame has 325); they close c = 0.57 (SE 0.26) of the identifiers' BA+ gap; pooled with NLSY97, C3 = 0.557 (0.246) and G2→G3+ ρ\* = 0.86; identity loss 11% recent, 15–18% at 18+ by period since 1994 | Any attrition or lineage correction; "the ones who stop identifying are the successful ones" |
| [Indian-origin: full account, arrival cohorts, home regions](immigration-indian-origin-full-account-and-selection-2026-09-29.md) | 2026-09-29, ladder 276–277: net benefit to others $11.4–12.9k per member ($9.2–10.6k at white ages) on main case v6 with social rows and every group's income taxes on the case's own keys; arrivals since 1995 at the 75th–78th education percentile, no decline in the surveyed flow; Punjabi speakers at 47, Telugu, Tamil and Kannada near 80; irregular inflow under-counted | Quoting "Indians are net positive" without the region split, the irregular-flow gap or the CPS/ACS count difference |
| [Indian vs white physicians: malpractice and fraud](immigration-indian-physician-malpractice-fraud-2026-09-21.md) | 2026-09-21: no US Indian-vs-White malpractice or fraud rate (NPDB has neither race nor school country). IMGs: fraud exclusion aOR **0.95** (ns), any exclusion **1.30**, health-crime **1.62** (Chen/Jena 2018). US paid-claim difference vs USMGs is small/null nationally (GAO 2010); Illinois ~1.2× paid claims, not more discipline; Caribbean not India is the negligence outlier. Rankings are AU/UK *school-country* complaint rates: India OR **1.61** in Australia (7th of named high-risk countries), UK GMC performance assessments ~**5×** UK-trained (mid-pack; Bangladesh 13×). Medicare internist IMGs have *lower* 30-day mortality (Tsugawa 2017) | “Indian doctors are worse / more fraudulent”; mixing IMG with Indian-origin; transferring UK GMC rates to US NPDB |
| [High-education origin screen](../infra/immigration-fiscal/high_skill_origin_screen_2026_09_21/RESULT.md) | 2026-09-21, ladder 168: 19 birthplace groups on the education-by-origin account; none clearly negative; Philippines-born at zero for an age reason; degree holders from Venezuela (−$23,512) and Pakistan/Bangladesh (−$16,878) far below native degree holders, India +$5,749, no longer clear of zero with item T; Russia/Ukraine-born positive, with 42% of their elderly on Medicaid (ACS), which the account does not see. Ladder 169: at the native age mix India +$32,159 → +$24,258, Venezuela → +$148, Mexico → −$5,360; ordering survives | "High-skill immigrants are all fiscally positive" claims; "young groups only look good" objections; choosing an origin for an ACS-based account (Bangladesh, Armenia) |
| [Muslim-majority origins: fiscal position, attitudes, extremism counts, mosque funding](immigration-muslim-origins-funding-outcomes-2026-09-21.md) | 2026-09-21: high-education Muslim-majority birthplaces fiscally positive, weak groups are refugee-route origins and Bangladesh; Pew 2017 (religion observed): degrees and $100k+ incomes at the public's rate, more under $30k, violence rejected at the public's rate; Cato: 3,046 murders by foreign-born terrorists in 50 years, 97.8% on 9/11, native-born not counted; Europe much worse and its author says it does not transfer; mosque funding has no ledger by statute, survey has no foreign item, median budget $80k; Alavi (Iran) litigation status unverified; **2026-09-22 microdata (§2a, ladder 177):** nativity does not move the attitude items, the violence figure is foreign-born South Asian and reversed by their US-born children, US-born Muslims are two populations; **NIS 2003 cohort (§2b, ladder 179):** the Muslim employment deficit at admission (−10.4 points) is composition (−0.8 with country of birth) and the pay-rate gap is zero | Questions about Muslim immigrants, Islamism or mosque funding; Europe-to-US transfer claims |
| [Second generation by parental origin, IPUMS-CPS 1994–2025](immigration-second-generation-by-origin-2026-09-22.md) | 2026-09-22, ladder 178: the US-born children of Mexican immigrants close 76% of the first generation's no-high-school gap but 31% of the college gap (−29.8 → −20.6 points against third-plus non-Hispanic whites at the same age, sex and year), 59% of employment, 66% of log income; self-identified third-plus Mexicans sit at the second generation's level; 1994–2025 the second generation's college gap widened (−17.4 → −22.5) while its no-high-school gap narrowed and its income gap stayed flat; Mexico is the only top-ten parental birthplace whose second generation is behind on college. Descriptive, cross-sectional; SEs are lower bounds | Any claim about convergence or stalling by generation; FAQ 5; the generation ledger's flat first-to-second fiscal gap |
| [Careers of Hispanic sons and daughters, NLSY97](../infra/immigration-fiscal/career_trajectories_2026_09_29/RESULT.md) | 2026-09-29, ladder 272: second-generation Hispanic sons' earnings gap to third-plus white men −0.150 at 25–27 → −0.271 at 35–40, widening −0.116 (0.057) for the same men, mostly pay and following schooling; daughters −0.134 → −0.202, widening −0.059 (0.060), about zero at equal schooling with pay 8% higher; third-plus Hispanics no closer; the CPS–SSA studies (Villarreal–Tamborini 2023, 2024) agree except on women's employment | Whether the second generation catches up over a career; sons against daughters; reading one year's cross-section as a lifetime |
| [Admission route against origin religion](../infra/immigration-fiscal/admission_route_2026_09_21/RESULT.md) | 2026-09-21, ladder 171, design fixed before the data: across 66 birthplaces the employment-route share predicts how a degree converts (+29 points of degree holders earning $100k+ from 10% to 50% employment route); the origin's Muslim share carries no earnings penalty among degree holders and predicts women's employment 13–17 points lower whatever the route; by the pre-set rule the test is not settled; ecological | "Is it the origin or how they were admitted?"; claims about Muslim-majority origins; routes as the policy lever |
| [Military service by ancestry](../infra/immigration-fiscal/civic_service_by_ancestry_2026_09_21/RESULT.md) | 2026-09-21, ladder 170: US-born men of Asian Indian ancestry ever on active duty 1.05% against 6.6–7.8% for English, German, Irish ancestry; holds among degree holders and at ages 25–34; Korean and Filipino at the white rate, Mexican-ancestry degree holders above it (8.2%); parental income and metro not held constant | Questions about civic attachment of high-skill groups; a behavioural companion to ladder 152's giving, volunteering and turnout |
| [Military and public service at equal SES](../infra/immigration-fiscal/service_by_ses_2026_09_23/RESULT.md) | 2026-09-23, ladder 205 (extends 170 and 152): ACS 2022–24 men 18–49 ever on active duty: US-born Asian Indian ancestry 0.16× US-born non-Hispanic whites and 0.18–0.24 under every whole-group adjustment (age, schooling, birth state, residence, tract income); US-born Mexican origin 0.79×, 0.88 at the same ages, 0.74–1.46 at equal schooling and place depending on whose mix, the gap sitting among California- and Texas-born men; Mexican-origin women 1.10 at the same ages and men now on active duty at 18–24 0.98; police 1.01 per worker (1.17 at equal age and schooling); CPS volunteering and giving gaps shrink 40–60% for Mexican origin at equal SES and widen to −16 to −18 points for the India-born | Who serves at equal SES; never quote the Indian white-mix rakings as the adjusted gap; schooling and residence adjustments cannot separate cause from outcome |
| [Homicide victims, offenders and treasury cost](immigration-homicide-victim-offender-and-treasury-cost-2026-09-18.md) | Cleared-case victim/offender distributions; the memo's $1.5–1.8m treasury scenario predates the September 19 repair and assumes conviction and prison sentencing, not an expected cost per cleared case; read the lane's current tables before reuse | Reusing homicide cost or victim-incidence figures |
| [Enclave neighborhood quality and informality](immigration-enclave-neighborhood-quality-and-informality-2026-09-18.md) | 2026-09-18 | AHS 2023 at equal income/tenure/metro/crowding: Mexico-born householders no likelier in inadequate units, fewer abandoned buildings, better neighborhood ratings; only trash-within-half-block survives (+0.87 pp, Hispanic; ns for Mexican origin); SF inspector litter association falls two-thirds within neighborhoods, Mexican-origin t 1.5; LA 311 income-driven; Mission Street storefronts 90.9% registered vs 83.6% citywide, Chinatown 90.5%; H2 falsified | Any "they can't maintain their neighborhoods" or "those shops aren't legit" claim; AHS neighborhood-item coding |
| [School flight and public goods](immigration-school-flight-and-public-goods-2026-09-18.md) | School-flight effect unestablished; district revenue associations and state aid responses; voucher evidence includes non-test-score benefits, so immigration-attributable defensive tuition remains unpriced | Interpreting school choice and public spending |
| [Native displacement onto transfers](immigration-native-displacement-to-transfers-2026-09-18.md) | Adverse-to-hypothesis associations coexist with failed identification; not a causal null; baseline association is a diagnostic, and single-instrument scalar sign does not change 2SLS | Claims about displacement onto welfare or disability |
| [California vs Texas fiscal geography](immigration-california-texas-fiscal-geography-2026-09-21.md) | Same ~32% Mexican-origin share; CA −$15,228 vs TX −$9,267 vs local whites (shared all-age ledger, with the income tax the survey misses; −$12,133 / −$7,479 with taxes as the survey reports them); LA −$21,083 vs Houston −$8,977; NY 0.50m; SF gap not estimated; not the complete-account total | "It's just California"; "share catching up explodes the national gap"; asking for SF/NY |
| [Metro-matched gaps](../infra/immigration-fiscal/metro_match_2026_09_17/RESULT.md) | National per-person gap barely moved by metro matching (−$6,910 → −$6,818 vs whites with item T; −$5,734 → −$5,797 with taxes as the survey reports them); six published metros all adverse at the point estimate (with item T Riverside's interval reaches +$79); nominal $, no PPP | Single-metro vs-white figures; claiming geography matching erases the gap |
| [Native sorting (Tiebout)](immigration-native-sorting-tiebout-2026-09-18.md) | CA and TX already at the same Mexican-origin share; IRS/ACS sorting tracks tax rates not that share; TX AGI inflow; moving motives unresolved | Explaining native migration or assigning its revenue cost |
| [Who pays the fiscal gap](immigration-fiscal-gap-incidence-who-pays-2026-09-18.md) | Historical $2,246/household and 89% state-local superseded; rebuilt financing requires explicit correctional-payer sensitivity and remains imposed incidence | Reusing household burden or payer-share figures |
| [Housing supply, demand and rents: California against Texas](immigration-housing-supply-ca-tx-2026-09-22.md) | 2026-09-22, ladder 180: Texas permits 2.2–2.5× California's per resident on average over 2000–2024 (1.4× in 2004 to 3.7× in 2009), but California's stock outgrew its population 2010–2024 (1.77 vs 2.31 people per added unit) [FRAMING-SENSITIVE]; same demand shift moves coastal-CA rents 2.0–2.5× Houston's on Saiz elasticities; 152 of 168 metros: +0.030 log points of 2015–2026 rent growth per point of Mexican-origin share change within state, elasticity interaction not identified; 2024 PUMS: native NH white adults leave CA at −11.7/1,000, steeper without a degree; TX flat. Descriptive, no instrument | Any rent, zoning or "Texas builds" claim; the housing channel of FAQ 4 and 15; modelling a stock counterfactual (§6 says why not) |
| [Rents and values against the 2000–2010 inflow, instrumented](../infra/immigration-fiscal/housing_causal_2000_2010_2026_09_22/RESULT.md) | 2026-09-22, ladder 183: per point of foreign-born share, rents +1.4% (SE 1.4, null containing Saiz's 1) and values +11.6% (2.9; +5.7% with the 2000 level) with the ancestry instrument; settlement instrument 2.5–5.7× larger and rejected by Hansen J; no inelastic-metro amplification (223 Saiz-matched metros); all-foreign-born, one cycle. Qualified 2026-09-25: the instrument is a same-decade pull (ladder 199), so these are diagnostics, not causal effects | Quoting a causal rent or value effect for a decade; using the Saiz mechanical response (ladder 180) as a rent prediction |
| [Second instrument for the 2000–2010 inflow](../infra/immigration-fiscal/ancestry_instrument_2026_09_22/RESULT.md) | 2026-09-22, ladder 182: the public ancestry push-pull prediction (F 63.9 vs 29.1, passes the baseline-level test the settlement instrument fails, Mexico a third of its variance) halves the SSI response to −0.28 (0.06) and makes the public-assistance response a null (−0.10 ± 0.19); Hansen J rejects the pair; the displacement lane's negative claim stands at smaller size. Qualified 2026-09-23/25: a same-decade pull whose F is fragile to geography (ladder 199), with all-household outcomes, so no native claim; diagnostics only | Quoting the displacement lane's public-assistance coefficient; choosing an instrument for any 2000–2010 metro design |
| [US low-skill effect papers: what joins the account](immigration-us-lowskill-effects-integration-2026-09-22.md) | 2026-09-22, ladder 181: fourteen primary texts read in full; the removal model's ε = 3 rests on a firm-level 1.26 (95% CI 0.12–2.39) and a calibrated 4.6 whose authors' aggregate is ≈9, while direct low-skill estimates are 8.7 (Caiumi–Peri) and 17.9 (Piyapromdee); computed on the nest, ε = 8.7 and 17.9 give +$18.0 / +$11.9bn and +$15.6 / +$10.3bn (GDP / cash) against the published +13.3 / +8.8bn, a $2–5bn headline move rather than $9–14bn, not applied; ten papers feed four stand-alone sections (wage incidence, removal and jobs, housing horizons, selection) and none carries a fiscal line | Placing any of these papers in an essay section; choosing ε for FAQ 14; reusing the ancestry-instrument files (Wilson–Zhou's rejected instrument, F 6.80) or the Bracero package |
| [Employment-entry displacement, US metros](immigration-employment-entry-displacement-2026-09-18.md) | Recent metro causal effect unresolved; preserve weak-stage and placebo results, withdraw small/negative scalar explanation and college-control proof | Running or interpreting recent settlement-share IVs |
| [Institutions and liberal norms by generation](immigration-institutions-and-liberal-norms-by-generation-2026-09-18.md) | GSS/ANES survey contrasts by generation and reference; response-style share unidentified; political-violence item requires behaviorally validated replication | Interpreting norms, institutions and survey measurement |
| [Mexico-born arrival cohorts](immigration-mexican-arrival-cohorts-2026-09-18.md) | 2026-09-18; age cut 2026-09-22 | Cohort quality 1975–2024: LTHS among new arrivals 82% → 33%, BA+ 3% → 22%; wage residual U-shaped; migrants' schooling rises +2.53 yr with no-schooling reports scored at zero (+2.67–2.69 without the ACS 2020 reporting step) against Mexico 15+ +2.20, 0.0–0.5 yr more than Mexico's. Same-age INEGI 2020 sheet 13 vs ACS 2019 0–5 YSM: LTHS 9–13 pp below origin in every band 25–54, gap not larger for younger births; BA+ within 3 pp except n=233. US stayers; ACS secundaria-as-HS. [Companion](immigration-mexican-origin-age-attainment-2026-09-22.md) | Any "earlier Mexican cohorts were better" or "the surge was Mexican" claim |
| [Consumer prices and native women's hours](immigration-consumer-price-and-native-hours-2026-09-18.md) | Extrapolated worker-removal scenarios; $21.8bn combines private gains and tax receipts and is not a bound on total benefits or a matched offset to the all-generation account; goods-price evidence is not a failed services replication | Comparing benefits on a common policy and population |
| [Claim scorecard: Smith, Caplan, Decker, Nowrasteh](immigration-claim-scorecard-2026-09-18.md) | September 19 corrections govern the retained rows: no CBO-per-capita refutation of incumbent welfare; no fee/loan falsification from a benchmark shortfall; counts withdrawn | Matching the actual claim before grading a rebuttal |
| [Yglesias claims audit](immigration-yglesias-claims-audit-2026-09-21.md) | 2026-09-21: 40 claims and 15 concessions from 15 primary pieces; he has conceded the skill gradient (2021), housing (2025), asylum and enforcement (2023–25); unsupported: the 2020 universals, a loose reading of Borjas, and a welfare-wall remedy that does not reach most of the gap; no fiscal number in his own voice (the CBO posts are guests') | Quoting or rebutting Yglesias; the matching rule applied before grading |
| [National Academies 1997 and 2016, low-skill rows by assumption](immigration-nrc-1997-low-skill-assumptions-2026-10-07.md) | 2026-10-07 | Every published education row puts an immigrant without high school negative: 1997 −$89,000 own life, −$13,000 with descendants (1996 $); 2016 −$109,000/−$115,000, −$116,000/−$185,000 with children and grandchildren (2012 $). The 1997 +$80,000 average rests on the 2016 debt freeze (−$15,000 without). Eight assumptions scored: three lean toward immigrants, three against or realized in their favour (capital taxes omitted, low rates, welfare reform); only Clemens's capital-tax adjustment turns the dropout positive |
| [Canon citation audit](immigration-canon-citation-audit-2026-09-17.md) | 2026-09-17 | Most-cited low-skill immigration papers ranked by Semantic Scholar and OpenAlex counts (S2 fragments Borjas 2003 and Card 1990; every affected row tagged), 26 papers audited: one defective result per side (Borjas 2017 Mariel; Longhi 2005 as an estimate), over-citation the dominant failure (8 of 13 pro, 4 of 13 con), pro canon rests on the shift-share instrument Jaeger–Ruist–Stuhler show is biased against short-run effects and con canon on fixed-capital skill cells biased the other way; CIS/Heritage absent from the citation record | Citing any canonical immigration paper for a claim; "the literature shows" arguments on either side |
| [Published accounts compared](../notes/immigration-published-accounts-comparison-2026-09-30.md) | 2026-09-30 | Twenty published fiscal accounts graded on this account's eight pieces. At least eight cover four to six in partial form (the Danish Finance Ministry and Dutch register studies five each, NAS 2017, Cato 2026's 1994–2023 back-cast); none reaches four at depth. None prices other residents' non-budget costs, who bears them or the sending country in the fiscal account, and none covers Mexican origin across generations. The only Mexico figure is Manhattan Institute's October 2025 federal one: $10,000 of debt per Mexican immigrant over 30 years. The grades are an agent's, from excerpts | Claiming novelty or completeness; comparing with the Dutch, Danish or National Academies accounts |
| [Linked records: what they would change](../notes/immigration-linked-records-evidence-2026-09-30.md) | 2026-09-30 | Published survey-to-tax-and-benefit record linkages, read against the case's survey-keyed lines. Among linked workers the survey understates Hispanic and immigrant earnings (Kim & Tamborini 2014: 4.1 and 5.5 log points against W-2s), and Census's linked NEWS estimates raise Hispanic median household income 8.6% against 5.4% for white non-Hispanics. Transported onto the case, linkage would lower it by about $5bn (−$15bn to +$8bn). Noncitizen Hispanic workers link at 44%, so linked files cannot see the on-books share of the unauthorized, the largest survey-driven assumption | Answering "better data would change the result"; the income-tax key's remaining test (Treasury OTA WP-124 per-return tax) |
| [Dataset loose ends](../notes/immigration-dataset-loose-ends-2026-09-30.md) | 2026-09-30 | The broad dataset check's three loose ends plus linked records. Raking legal status to outside counts moves the case −$2.9 to +$1.4bn; SSA's SSI totals add at most $1.5bn; descendants who stopped identifying add $2.1–20.5bn at the average resident's cost and leave the excess over average residents unchanged; linked records, about −$5bn. None changes a conclusion | Answering "what about the unauthorized count, SSI or people who stopped identifying?" |
| [Conceptual audit of newer models](immigration-conceptual-audit-2026-09-27.md) | 2026-09-27: accounting/welfare bridges, selection and identity claims, capacity and transfer conservation. Expanded pass checks tax/benefit inputs, production, recoverable covariance, service beneficiaries, sponsorship hazards and birth survival; seven reproducible probes, with subsequent repairs recorded | Extending the main case into debt, world welfare, generational forecasts or policy rankings; checking what the audit has and has not covered |
| [Strong objections without discarding real costs](immigration-adversarial-audit-2026-09-28.md) | 2026-09-28: public-payroll reconciliation, mixed-household response, preferences-policy attribution, generation nonadditivity; corrects amenity-zero and innovation-null synthesis claims; two read-only probes, no new headline | Defending broad fiscal/social claims; separating valid criticism from objections that erase real costs |
| [Validation and back-testing](immigration-validation-and-backtesting-2026-09-28.md) | 2026-09-28, follow-ups executed: mixed temporal school/fiscal prediction; CPS tax distribution still fails against IRS; new MCBS2022 check is closer but imprecise; medical definitions differ; coherent joint Mariel budget loses its pretreatment baseline; earlier GSS/SNAP tests retained | Component prediction versus full-counterfactual validation; failed comparisons, corrected claims and remaining tests |
| [Weekly conceptual audit](immigration-weekly-conceptual-audit-2026-09-25.md) | 2026-09-25, snapshot `beefbba`: ancestry-IV construction/native outcome, distribution sensitivity, school expenditure-to-output bridge, lineage eligibility, off-books population, return-selection comparator and voting-bound problems; debt and negative-result interpretation limits; two reproduced probes and explicit coverage | Reusing the September 19–25 findings as causal effects, welfare totals, winner counts or hard bounds |
| [Study integrity audit](immigration-study-integrity-audit-2026-09-23.md) | 2026-09-23: 26 external studies behind the crime, legalization and children's conclusions traced from data capture; none fabricated; the repo went beyond its source 18 times (14 favourable to immigration, 3 against, 1 both), mostly composition (two-thirds of studies overstated on each side), plus two double standards that favour immigration (Lott against Light; Freedman–Owens–Bohn's ethnicity proxy) | Citing a causal estimate on crime, legalization or children's outcomes; dismissing a study for a flaw |
| [IGM panel immigration polls](immigration-igm-panel-audit-2026-09-17.md) | 2026-09-17 | Every IGM/Clark Center immigration poll (13 polls, 22 statements, 986 responses from the site's CSVs): all on legal admission, none on unauthorized immigration; the 2013 low-skill statement at 52% panel agreement with 17 of 24 agreers giving no reason and the same panel agreeing low-skilled Americans lose; per-comment audit against the ledger; weighted/unweighted gap is partly a denominator change | Any "economists agree immigration is good" claim, or citing the IGM low-skill poll |
| [Bookmark claims and commentator source notes](immigration-essay-angles-from-bookmarks-2026-09-16.md) | Source-grounded claims, commentator positions and research questions from the operator's bookmarks; retain as evidence notes | Locating original statements and source coverage |
| `immigration-conduct-denominators-2026-09-05.md` | Corrected Texas native denominator, official SPI recode, recent custody/fraud and audits | Reusing old SPI rates or cumulative convictions as a current rate |
| `immigration-admission-work-access-2026-09-05.md` | Reconciled admission distributions, 2026 EAD/refugee data and undercount assumptions | Equating new entries, adjustments, application queues and resident cohorts |
| `immigration-sipp-2024-benefits-2026-09-05.md` | Actual calendar2024 selected benefits with 240 replicate weights | Comparing benefit receipt or interpreting coarsened arrival bins |
| `immigration-welfare-use-by-generation-2026-09-16.md` | Welfare use by immigrant generation (CPS ASEC 2024–25): gen2 34.6% vs gen3+ 29.4%, 1.5 pts after age adjustment, below gen3+ within white/Black/Asian; cash lowest in gen2 | Any claim about the second or third generation's welfare use, or reading CIS generation tables |
| `immigration-mexican-origin-by-generation-2026-09-16.md` | Mexican-origin residents by generation (CPS ASEC 2024–25): education, work, earnings, poverty, welfare; Borjas–Katz wage effect; fiscal and crime cross-refs; what is conclusive vs contested vs unmeasurable | Any claim about Mexicans' economic or crime impact by generation |
| `immigration-local-cost-incidence-2026-09-05.md` | NYC financing, household-nights, enrollment and school-spending definitions | Converting gross services into per-person or net welfare costs |
| `immigration-material-repair-report-2026-09-05.md` | September 5 repair report: source corrections and validation evidence | Reusing numerical or causal conclusions from older memos |
| `immigration-cohort-clarity-2026-09-05.md` | All-native versus Mexico-born partial fiscal comparison; actual 2019/2024 recent-entry profiles and discriminating next checks | Asking whether the newer intake differs, what Somali-origin data establish, or which fiscal ranking is supported |
| `immigration-recent-cohort-data-availability-2026-09-05.md` | Verified ACS/SIPP/CPS release periods, actual SSD paths and administrative counting limits | Assuming 2025/2026 microdata are already available or equating admissions with residents |
| `immigration-cohort-narratives-2026-09-05.md` | Targeted official X sample on recent cohorts, refugee/fraud and Somali claims with primary checks | Reusing current cohort or group-generalization narratives |
| `immigration-framing-refresh-2026-09-05.md` | Recent evidence integrated: work rights, adjustment, housing, victimization and policy mechanisms | Choosing the next empirical comparison or interpreting current narratives |
| `immigration-recent-papers-2026-09-05.md` | June–September primary papers/revisions with designs, dates and access limits | Quoting recent labor, housing, fiscal or enforcement research |
| `immigration-recent-papers-2026-10-06.md` | July 2025–October 2026 scan across seven lanes, graded against the account's claims and revised 2026-10-07 after full-text reads: the closed-budget estimand ($354.6–425.6bn central), school decline asymmetry, surge wages, Hispanic identity, survey income tax and nonresponse, the 2026 public-charge rule ($5.0bn for the lineage) and the 2025 budget law | Asking whether new work shows the account wrong, or answering a reader who cites it |
| `immigration-v6-red-team-2026-10-08.md` | Outside red team of main case v6 and its docs (GPT-6 Astra and Gemini 3.8 Flash, 57 findings): no headline mover; FAQ 19's double-count defense withdrawn, FAQ 14's occupation sketch relabelled, FAQ 11's Lee–Scafidi timing and FAQ 17's sign claim scoped, the payload consumer's capital fail-open closed; every rejected attack routed to its answering entry | Before re-raising a known attack on the case (capital double count, accrual against cash, whole people, school stickiness, fourth-plus pricing) |
| `immigration-recent-narratives-2026-09-05.md` | Current essays/news and selective official X sample; counterexamples and claim checks | Repeating current public arguments |
| `immigration-dataset-proxy-refresh-2026-09-05.md` | BLS/BPS/ICE acquisitions and BEA audit, provenance and principal checks | Using recent outcomes, capacity proxies or enforcement counts |
| `immigration-conceptual-audit-2026-09-05.md` | Material audit: SIPP household/person and education errors; GDP/incumbent and CRS mistakes; Cato mischaracterization; global-gains arithmetic; conditional crime-bias sign | Reusing June fiscal-proxy figures or the dismantling synthesis; these corrections supersede the specified claims |
| `immigration-evidence-base-audit.md` | Which claims are well-supported vs thin | Repeating literature claims or writing summaries |
| `immigration-glossary.md` | Definitions and term discipline | Using terms like `unauthorized`, `low-skill`, `surge`, `fiscal` |
| `immigration-economist-effects-matrix.md` | What economists are actually pricing vs omitting | Comparing Smith, Decker, Borjas, Clark poll economists |
| `immigration-source-incentive-regrade-2026-06-23.md` | Source-incentive heuristics for prioritizing checks; grades are not truth probabilities or evidence weights | Assessing source incentives while verifying methods and primary tables |
| `immigration-dataset-register.md` | Data register by domain: core files, data held inside analysis lanes, and data [not held](immigration-dataset-register.md#not-held) (restricted, lost, open leads) | Asking "what data do we have?" or "what should we get next?" |
| `immigration-verification-handoff.md` | Verification map: repo files, datasets, paper families, disciplines | Handing the topic to another agent |
| `immigration-friend-reproduce-guide.md` | **Clone → build → read → query** for a human collaborator | Sharing reasoning + reproduction steps |
| `immigration-redteam-2026-06-25.md` | June red-team, status as of 2026-09-05 | Closing out a conclusion; before publishing |
| `immigration-preregistration-ledger.md` | Frozen predictions written before the gated datasets land | Interpreting a new gated-data result; checking for post-hoc drift |
| `immigration-interpreted-insights-2026-06-24.md` | Interpreted insights from the June frontier pass, repaired 2026-09-05 | Quoting a June-era interpretation |

## June method check and gated-data specs (2026-06-24/25)

A resolved method check, and the acquisition specs that the second-generation loaders follow. The June scouting lists
that sat here were deleted on 2026-09-29 (tombstones at the end); their open leads are in the
[dataset register](immigration-dataset-register.md#open-leads).

| File | What |
|------|------|
| `immigration-clemens-method-check-2026-06-24.md` | Clemens GE versus partial-equilibrium method check |
| `immigration-gated-data-specs-2026-06-25.md` | Acquisition specs for gated datasets (IPUMS-CPS second-generation extract and others) |

## Frontier expansion (2026-06-25)

Historical five-domain research/acquisition pass. DOI resolution checks bibliographic identity; it does not verify an effect size or inference. September corrections in confidence-ladder entries 52–60 and the linked memos supersede affected June claims. The coverage matrix records a search episode, not proof that economics or crime research is exhausted.

| File | What | Consult before |
|------|------|----------------|
| `immigration-research-coverage-matrix-2026-06-25.md` | **The map** — per-domain saturation-vs-frontier + the 5-agent integration log + synthesis verdict | Asking "what research is left?"; planning the next acquisition |
| `immigration-economics-disconfirmers-2026-06-25.md` | Mariel artifact (Clemens-Hunt), Colas-Sachs GE ~$750, CBO −$0.9T federal surge, Dustmann-Frattini UK | Quoting the Borjas wage spine or NAS net-cost as settled |
| `immigration-policy-frontier-2026-06-25.md` | Legalization→crime CAUSAL cluster (jobs channel); enforcement≈null; DACA + refugee evals | Crime/policy causal claims; "does enforcement reduce crime?" |
| `immigration-crime-frontier-2026-06-25.md` | Crime outcomes, generational evidence, ecological versus individual estimates and source limits | Generalizing beyond the measured justice outcome and population |
| `immigration-sociology-frontier-2026-06-25.md` | Trust meta-analysis, selection and generational measurement limits | Inferring social or institutional mechanisms |
| `immigration-urbanism-frontier-2026-06-25.md` | Housing evidence, assessment of 2026-09-05: Wilson–Zhou's local estimates (an inflow of 1% of employment raises house prices about 2.2% and rents 1.4%), what the data can identify, and why a price effect is not a welfare or fiscal effect | Using a local housing coefficient as a national, welfare or fiscal figure |

## Fiscal Ledger

| File | Topic | Consult before |
|------|-------|----------------|
| `immigration-fiscal-impact-unauthorized-memo.md` | **[pre-repair, March 2026; status banner added 2026-09-21]** Literature memo: federal/state-local split, wage debate, child-attribution dispute. Its NAS "second generation net positive" statements are all-origin, not the Mexican-origin result | The literature and the child-attribution dispute; **not** a current fiscal bottom line (use Core State) |
| `immigration-household-weighted-correction.md` | Household vs person correction issues | Reusing external figures without checking unit of analysis |
| `immigration-nas-scope-and-bias-update-2026-04-10.md` | What NAS does and does not cover | Treating NAS as final or complete |

## Data Stack

| File | Topic | Consult before |
|------|-------|----------------|
| `immigration-lifetime-fiscal-data-stack-2026-04-10.md` | Minimum viable and gold-standard lifetime model stack | Saying ACS alone is enough |
| `immigration-borjas-supply-shock-panel-2026-06-23.md` | **Built** real 1980–2023 immigrant-share-by-skill panel from IPUMS census/ACS (`borjas_supply_shock_panel`); <HS share 9.8%→40.8%. Qualified 2026-09-26: the builder drops no-schooling records; kept, 10.2%→44.1%; the ACS 2020 reporting step moves 2023 about +1 point. Rebuilt the same day with them kept: the table reads 10.2%→44.1% (43.7% without the step); release v2026-09-05 keeps the old cells | Citing the supply-shock *quantity*; do NOT read it as a wage verdict (that's the Card-vs-Borjas debate) |
| `immigration-restrictionist-arguments-steelman-2026-06-15.md` | **Steel-man** restrictionist chains: Borjas, BGH, NAS/Orrenius, Gould, Razin, FAIR | Arguing against immigration; follow their logic |
| `immigration-restrictionist-corpus-parse-2026-06-15.md` | **Full marker-modal parse** of 8 restrictionist PDFs → perspectives, narratives, generators S06–S14 | Deep read of restrictionist corpus; generator mining |
| `immigration-restrictionist-corpus-full-extract-2026-06-15.md` | **Section-by-section full read** of all 9 papers (~220 claims, 62 sections) | Authoritative claim register after full parse |
| `immigration-restrictionist-dataset-integration-2026-06-15.md` | **Paper → dataset → DuckDB** map; Tier A–C acquire list | Planning integration after restrictionist corpus read |
| `immigration-origin-data-stack.md` | Origin/destination and ontology layer | Making claims by origin mix |
| `immigration-frontier-data-acquisition-2026-04-11.md` | Stage 4 local-capacity acquisition pass: `SAIPE`, court/interpreter docs, and NCES CCD file-tool artifacts | Building school-service or court-friction modules |
| `immigration-public-mvp-meps-module-2026-04-11.md` | Built MEPS health-cost module for the public MVP | Using MEPS-derived health-cost outputs |
| `immigration-education-bucket-stock-and-lifetime-status-2026-04-11.md` | Weighted ACS stock cut by education bucket plus current lifetime-estimate status | Asking for `<HS` / `HS` / `some college` counts or state shares |
| `immigration-local-burden-puma-layer.md` | PUMA/local burden layer | Moving from state averages to sub-state analysis |
| `immigration-stage2-county-bridge-batch.md` | County bridge build status | County-level joining or school/housing overlays |

## Interpretation & External Debate

Current cross-media coverage: [podcast, YouTube and Substack audit](immigration-media-perspectives-audit-2026-09-20.md) checks 16 media pieces with explicit access limits, maps claims to existing evidence, adds visa-mobility/H-1B/Dutch study screens, and distinguishes high-skill selection from low-skill evidence. The user-linked Reddit bibliography remains inaccessible and ungraded.

| File | Topic | Consult before |
|------|-------|----------------|
| `immigration-clark-respondent-audit.md` | How to read the Clark poll without overclaiming | Saying "economists agree" |
| `immigration-smith-decker-friedman-comparative-quantitative-audit-2026-04-11.md` | Unified comparative audit with one quantitative framework across all three commentators | Wanting a more decisive first-principles comparison |
| `immigration-david-d-friedman-claims-audit-2026-04-11.md` | Named audit of David D. Friedman claims with a first-principles quantitative pass | Checking libertarian open-borders arguments against the repo and official sources |
| `immigration-bryan-caplan-claims-audit-2026-04-21.md` | Claim-by-claim audit of Bryan Caplan with a causal graph tying his optimistic channels to current surge, housing, fiscal, and political-response evidence | Evaluating Caplan directly rather than treating him as generic open-borders rhetoric |
| `immigration-sumner-claims-audit-2026-09-22.md` | Claim-by-claim audit of Scott Sumner's surge, wage, housing, Social Security and scale claims against his own pages, with the pasted AI critique graded cosign / throw out / complement; the Social Security "best solution" quote does not exist; the Trustees sensitivity is 0.38% of payroll (about $2.6tn of $22.6tn), not $1.5tn; CBO surge routed to FAQ 16 | Quoting Sumner; the "CBO says the surge shrinks the deficit" objection; the Social Security financing claim |
| `immigration-economist-rhetorical-failures-2026-04-22.md` | Bounded memo on the strongest fair critique of mainstream pro-immigration economics rhetoric: ledger switching, upper-bound laundering, marginal-to-mass extrapolation, capacity erasure, denominator masking, and political-economy underspecification | Asking how to kill the strongest economist arguments without overclaiming beyond the repo's current evidence |
| `immigration-noah-smith-nicholas-decker-claims-audit-2026-04-11.md` | Named audit of Noah Smith and Nicholas Decker claims | Checking pundit or commentator claims against the repo and official sources |
| `immigration-economist-dismantling-2026-06-25.md` | June dismantling pass (corrected 2026-09-05): fundamental fair-is-the-weapon dismantling of the pro-immigration canon across 3 tiers (Commentators: Smith/Decker/CATO; Academic Foundations: Card-Peri/Clemens; Popular Books: Hernandez/*Streets of Gold*); grants the repo-confirmed core, kills only the coordinate-switches, quotes the canon's own primary texts | Building any step-by-step takedown of pro-immigration arguments; wanting the synthesis across all 7 targets |
| `immigration-dismantle-noah-smith-2026-06-25.md` | Corrected claim-by-claim assessment: average gains, local costs, projections and welfare incidence | Comparing Smith's exact populations and claims |
| `immigration-dismantle-decker-2026-06-25.md` | Corrected returns-to-scale, incumbent welfare and global-gains arithmetic | Using GDP/person or complementarity to infer welfare |
| `immigration-dismantle-cato-2026-06-25.md` | Corrected descendant accounting and allocation sensitivity; no uncomputed sign reversal; the 2026-09-20 [bridge check](../notes/immigration-cato-bridge-check-2026-09-20.md) shows why the account's negative figure and Cato's are not comparable | Citing the historical $14.5T or descendant-inclusive estimates |
| `immigration-dismantle-hernandez-2026-06-25.md` | Corrected annual-versus-lifetime NAS figures, inventor attribution and crime scope | Evaluating book claims using primary evidence |
| `immigration-dismantle-card-peri-2026-06-25.md` | Card–Peri wage evidence, assessment of 2026-09-05: the published Ottaviano–Peri model gives about +0.6% for average native wages and −6.7% for previous immigrants (1990–2006, long run); Mariel is a local null with adjustment; the June memo's three "kills" do not survive | Citing Card, Peri or Mariel for or against wage harm |
| `immigration-dismantle-clemens-2026-06-25.md` | Clemens and open-borders gains, assessment of 2026-09-05: large potential gains survive; their size, distribution and transition are model- and policy-dependent; no demonstrated global upper bound | Calling world-GDP doubling a forecast, or calling it impossible |
| `immigration-dismantle-streets-of-gold-2026-06-25.md` | *Streets of Gold* mobility claims, assessment of 2026-09-05: the conditional mobility result survives; universal transfer, every-group convergence and a policy-welfare conclusion do not follow | Citing Abramitzky–Boustan for or against assimilation |
| `immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md` | Open Borders "double world GDP" and "apartheid" audit, assessment of 2026-09-05: doubling is a conditional model result, not a forecast; the repo's earlier rejection also went beyond its evidence | Quoting the doubling slogan or the apartheid analogy |
| `immigration-open-borders-break-even-bounds-2026-04-22.md` | Open-borders break-even arithmetic, assessment of 2026-09-05: conditional loss thresholds and a US housing-unit requirement; neither is an estimated loss or an upper bound on gains | Treating a break-even threshold as an observed loss |
| `immigration-low-skill-origin-incidence-memo.md` | Why origin mix and household structure matter | Treating low-skill immigration as one undifferentiated object |
| `immigration-fiscal-deceptive-data-reading-pack.md` | Common bad-faith or sloppy readings of the data | Debunking a chart, thread, or pundit claim |
| `immigration-fiscal-camarota-cis-testimony-audit.md` | Restrictionist benchmark audit | Using CIS/Camarota as baseline evidence |
| `immigration-crime-rates-unauthorized-vs-native-born.md` | Crime-rate evidence review | Mixing crime claims into a fiscal memo |
| `immigration-agi-reframing.md` | Off-mainline strategic reframing | Pulling the project into speculative macro territory |
| `immigration-recent-literature-surge-threshold-audit-2026-04-21.md` | Post-2023 economics literature on surge and threshold effects | Claiming the literature has or lacks a threshold result |
| `immigration-jre-2460-rachel-wilson-claims.md` | JRE #2460 Rachel Wilson claims 1–10 verification | Checking podcast claims |
| `immigration-jre-2460-claims-11-20.md` | JRE #2460 claims 11–20 verification | Checking podcast claims |
| `immigration-jre-2460-exa-crosscheck.md` | Exa Answer API cross-check of the JRE #2460 verifications | Trusting an answer-engine verdict |

## Causal-design layer (2026-04-18)

April 2026 county/receiver causal layer. Its analyses were superseded on 2026-09-05 (causal-lever, threshold and receiver-node claims withdrawn) and were deleted on 2026-09-29 (tombstone tables at the end); the provenance record below remains live. The analysis result files under `sources/immigration-causal/data` were lost with the SSD tree in August 2026 and are deliberately not rebuilt (see the [data availability memo](immigration-recent-cohort-data-availability-2026-09-05.md), Revisions).

| File | Topic | Consult before |
|------|-------|----------------|
| `immigration-reasoning-evolution-2026-04-21.md` | Narrative provenance trace of how the repo’s immigration reasoning changed, including the `/critique close` correction and later downgrade that left the annual wage/employment split unresolved | Wanting the evolution of reasoning itself traced rather than only the latest stance |

## Raw Data & Warehouse

`sources/` is a real directory in the checkout, and `~/research-data` is a symlink to it; builds run with `bash ../infra/immigration-fiscal/reproduce.sh` (staged builds since 1ee53c4). What survived the August 2026 SSD loss, what was re-acquired and which April analysis outputs are gone: `immigration-recent-cohort-data-availability-2026-09-05.md` (Revisions).

| File | Topic | Consult before |
|------|-------|----------------|
| `../sources/immigration-fiscal/data/MANIFEST.md` | Raw-file manifest with paths and acquisition notes | Looking for a specific local file |
| `../warehouse/immigration.duckdb` | Unified warehouse (context + lifetime + fiscal union, schema-namespaced); `immigration_context.duckdb` beside it is the aggregate warehouse | Querying state/origin/context data |
| `../infra/immigration-fiscal/reproduce.sh` | `doctor`, `download`, `verify`, `build`, `query`, `package` entry points | Rebuilding or extending the warehouses |
| `../sources/immigration-causal/data/lehd/qwi_state_panel.parquet` | LEHD QWI `se` state × quarter × industry × education panel 2003–2023, re-pulled 2026-09-16 (`ACQUIRED.md` beside it) | Using QWI earnings; it has no nativity variable |
| `../sources/immigration-causal/data/cbp/raw/` | CBP southwest-border encounter CSVs FY22–FY26 (April) | Counting encounters versus arrivals |

## Quick Start

If the question is:

1. `What do we currently think?` Start with Core State above: the main case, the [objections FAQ](immigration-objections-faq-2026-09-21.md) and the [real-costs memo](immigration-real-fiscal-and-social-costs-2026-09-23.md). The [confidence ladder](immigration-confidence-ladder.md) gives claim confidence (entries 52 onward are live), and `../decisions/` says what changed and why.
2. `Is low-skill immigration good or bad for natives?` The [complete account](immigration-complete-annual-account-2026-09-20.md) and its [generation split](immigration-adopted-account-by-generation-2026-09-25.md), [who wins and who loses](immigration-winners-and-losers-2026-09-25.md), and the mechanisms in `immigration-second-order-effects-2026-09-05.md`. `immigration-economist-effects-matrix.md` (April) is for how economists frame the question, not for numbers.
3. `Crime?` Start with the [custody and crime measurement rule](immigration-detention-crime-and-fiscal-scope-2026-09-20.md); then `immigration-conduct-denominators-2026-09-05.md` and `immigration-crime-race-ethnicity-2026-09-05.md` for the corrected rates, `immigration-crime-statistics-bias-mechanisms-2026-09-16.md` for how the statistics mislead, `immigration-generational-crime-mechanisms-2026-09-16.md` for first versus second generation, and FAQ entry 12 for the priced costs. `immigration-crime-frontier-2026-06-25.md` and `immigration-crime-rates-unauthorized-vs-native-born.md` carry dated revisions.
4. `What data do we have locally?` Start with `immigration-dataset-register.md`, then `immigration-recent-cohort-data-availability-2026-09-05.md`, then `../sources/immigration-fiscal/data/MANIFEST.md`.
5. `Can we model this ourselves?` Start with `../infra/immigration-fiscal/REPRODUCTION_INPUTS.md`, `immigration-friend-reproduce-guide.md` and `../infra/immigration-fiscal/reproduce.sh`; the current model is the main-case lane, `../infra/immigration-fiscal/main_case_2026_10_07/` (`main_case.cjs`, `package.cjs`). `immigration-lifetime-fiscal-data-stack-2026-04-10.md` is the April design note.
6. `What is the current `<HS` / `HS` / `some college` stock split?` Start with `immigration-education-bucket-stock-and-lifetime-status-2026-04-11.md` (April ACS cut; the fiscal account carries the current education definitions).

## Builder specs kept, and deleted files

Superseded and cruft documents were deleted on 2026-09-29 ([decision](../decisions/2026-09-29-delete-superseded-and-cruft-docs.md)). The two files below stay because live builders cite them as their specifications; neither may be cited as current. Six memos once listed here have held only their corrected 2026-09-05 assessment since 2026-09-29 and are indexed in their topic sections; each one's Revisions section names the commit that holds its pre-repair text.

| File | Former section | Was | Superseded by |
|------|----------------|-----|---------------|
| `immigration-verified-findings-report-2026-04-10.md` | Core State | Historical findings with September corrections and current-report link | `immigration-clarity-update-2026-09-05.md`, `immigration-material-repair-report-2026-09-05.md` (September corrections sit above the snapshot marker) |
| `immigration-net-negative-dataset-frontier-2026-06-15.md` | Data Stack | Datasets to test net-negative fiscal/local-cost claims (+ disconfirmation) | `immigration-fiscal-account-2024-2026-09-05.md`, `immigration-conceptual-audit-2026-09-05.md` |

### Deleted 2026-09-29 (tombstones)

Recover a file with `git show <last commit>:<path>`. Every one is also on GitHub at origin/main 9a73476.

| Path | Last commit | Successor |
|---|---|---|
| `CYCLE.md` | `39560e2` (2026-06-16) | — |
| `notes/immigration-fiscal-political-economy.md` | `ab5d135` (2026-03-13) | — |
| `notes/immigration-lifetime-sweep-protocol.md` | `39560e2` (2026-06-16) | — |
| `notes/immigration-lifetime-synthesis-diverge-cookbook.md` | `75e5eff` (2026-06-24) | — |
| `research/immigration-adversarial-review.md` | `b24c75c` (2026-09-16) | [adversarial-audit-2026-09-28](immigration-adversarial-audit-2026-09-28.md), [conceptual-audit-2026-09-27](immigration-conceptual-audit-2026-09-27.md) |
| `research/immigration-benefits-and-macro-scale-2026-09-19.md` | `a04db1e` (2026-09-19) | [macro-reconciliation-2026-09-19](immigration-macro-reconciliation-2026-09-19.md), [matched-benefits-2026-09-19](immigration-matched-benefits-2026-09-19.md) |
| `research/immigration-capacity-falsification-2026-04-21.md` | `080ddae` (2026-09-05) | [second-order-effects-2026-09-05](immigration-second-order-effects-2026-09-05.md), [material-repair-report-2026-09-05](immigration-material-repair-report-2026-09-05.md) |
| `research/immigration-capacity-frontier-2026-04-21.md` | `080ddae` (2026-09-05) | [second-order-effects-2026-09-05](immigration-second-order-effects-2026-09-05.md), [material-repair-report-2026-09-05](immigration-material-repair-report-2026-09-05.md) |
| `research/immigration-causal-everify-card-vs-borjas.md` | `080ddae` (2026-09-05) | [material-repair-report-2026-09-05](immigration-material-repair-report-2026-09-05.md), [recent-papers-2026-09-05](immigration-recent-papers-2026-09-05.md) |
| `research/immigration-causal-internal-vs-immigrant-newcomers.md` | `080ddae` (2026-09-05) | [second-order-effects-2026-09-05](immigration-second-order-effects-2026-09-05.md), [material-repair-report-2026-09-05](immigration-material-repair-report-2026-09-05.md) |
| `research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md` | `080ddae` (2026-09-05) | [second-order-effects-2026-09-05](immigration-second-order-effects-2026-09-05.md), [material-repair-report-2026-09-05](immigration-material-repair-report-2026-09-05.md) |
| `research/immigration-causal-saiz-elasticity-rent.md` | `080ddae` (2026-09-05) | [housing-supply-ca-tx-2026-09-22](immigration-housing-supply-ca-tx-2026-09-22.md) |
| `research/immigration-causal-surge-2021-2024.md` | `080ddae` (2026-09-05) | [material-repair-report-2026-09-05](immigration-material-repair-report-2026-09-05.md), [conduct-denominators-2026-09-05](immigration-conduct-denominators-2026-09-05.md) |
| `research/immigration-causal-synthesis-2026-04-18.md` | `080ddae` (2026-09-05) | [second-order-effects-2026-09-05](immigration-second-order-effects-2026-09-05.md), [material-repair-report-2026-09-05](immigration-material-repair-report-2026-09-05.md) |
| `research/immigration-claims-evolution-ledger-2026-04-23.md` | `8be9f94` (2026-09-05) | [material-repair-report-2026-09-05](immigration-material-repair-report-2026-09-05.md) |
| `research/immigration-claims-matrix-2026-04-11.md` | `b24c75c` (2026-09-16) | [confidence-ladder](immigration-confidence-ladder.md), [objections-faq-2026-09-21](immigration-objections-faq-2026-09-21.md) |
| `research/immigration-conclusion-audit-running-fixes.md` | `8be9f94` (2026-09-05) | [material-repair-report-2026-09-05](immigration-material-repair-report-2026-09-05.md) |
| `research/immigration-costs-causal-analysis.md` | `080ddae` (2026-09-05) | [second-order-effects-2026-09-05](immigration-second-order-effects-2026-09-05.md), [2026-09-05-material-inference-repair](../decisions/2026-09-05-material-inference-repair.md) |
| `research/immigration-country-fiscal-tensor-2026-06-15.md` | `8be9f94` (2026-09-05) | [fiscal-account-2024-2026-09-05](immigration-fiscal-account-2024-2026-09-05.md), [conceptual-audit-2026-09-05](immigration-conceptual-audit-2026-09-05.md) |
| `research/immigration-county-outcome-panel-2026-04-21.md` | `080ddae` (2026-09-05) | [second-order-effects-2026-09-05](immigration-second-order-effects-2026-09-05.md), [material-repair-report-2026-09-05](immigration-material-repair-report-2026-09-05.md) |
| `research/immigration-dataset-roadmap.md` | `0ebd603` (2026-09-17) | [dataset-register, Not held](immigration-dataset-register.md#not-held) |
| `research/immigration-economist-debate-sheet-2026-04-22.md` | `080ddae` (2026-09-05) | — |
| `research/immigration-economist-one-pager-2026-04-22.md` | `080ddae` (2026-09-05) | — |
| `research/immigration-epistemic-check.md` | `a6baa32` (2026-06-16) | [llm-bias-caveat](../notes/llm-bias-caveat.md), [quant-bias-checklist](../notes/quant-bias-checklist.md) |
| `research/immigration-europe-caucasian-fiscal-findings-2026-06-15.md` | `8be9f94` (2026-09-05) | [fiscal-account-2024-2026-09-05](immigration-fiscal-account-2024-2026-09-05.md), [conceptual-audit-2026-09-05](immigration-conceptual-audit-2026-09-05.md) |
| `research/immigration-federal-distribution-findings-2026-06-15.md` | `8be9f94` (2026-09-05) | [fiscal-account-2024-2026-09-05](immigration-fiscal-account-2024-2026-09-05.md), [conceptual-audit-2026-09-05](immigration-conceptual-audit-2026-09-05.md) |
| `research/immigration-fiscal-welfare-ledger-map.md` | `36c4477` (2026-09-05) | [second-order-effects-2026-09-05](immigration-second-order-effects-2026-09-05.md), [fiscal-account-2024-2026-09-05](immigration-fiscal-account-2024-2026-09-05.md) |
| `research/immigration-frontier-rethink-2026-04-22.md` | `080ddae` (2026-09-05) | [second-order-effects-2026-09-05](immigration-second-order-effects-2026-09-05.md), [material-repair-report-2026-09-05](immigration-material-repair-report-2026-09-05.md) |
| `research/immigration-full-spectrum-costs-scoring-model.md` | `080ddae` (2026-09-05) | [second-order-effects-2026-09-05](immigration-second-order-effects-2026-09-05.md) |
| `research/immigration-full-spectrum-costs-unauthorized-memo.md` | `f96e3926` (2026-09-05) | [real-fiscal-and-social-costs-2026-09-23](immigration-real-fiscal-and-social-costs-2026-09-23.md) |
| `research/immigration-knowledge-delta-agent-loop-2026-06-16.md` | `080ddae` (2026-09-05) | — |
| `research/immigration-lifetime-country-approx-brainstorm-2026-06-15.md` | `8be9f94` (2026-09-05) | [fiscal-account-2024-2026-09-05](immigration-fiscal-account-2024-2026-09-05.md), [conceptual-audit-2026-09-05](immigration-conceptual-audit-2026-09-05.md) |
| `research/immigration-lifetime-dataset-brainstorm-2026-06-15.md` | `8be9f94` (2026-09-05) | [fiscal-account-2024-2026-09-05](immigration-fiscal-account-2024-2026-09-05.md), [conceptual-audit-2026-09-05](immigration-conceptual-audit-2026-09-05.md) |
| `research/immigration-lifetime-fiscal-generators.md` | `8be9f94` (2026-09-05) | [fiscal-account-2024-2026-09-05](immigration-fiscal-account-2024-2026-09-05.md), [conceptual-audit-2026-09-05](immigration-conceptual-audit-2026-09-05.md) |
| `research/immigration-lifetime-unified-theory-2026-06-15.md` | `8be9f94` (2026-09-05) | [fiscal-account-2024-2026-09-05](immigration-fiscal-account-2024-2026-09-05.md), [conceptual-audit-2026-09-05](immigration-conceptual-audit-2026-09-05.md) |
| `research/immigration-main-question-reset.md` | `933b831` (2026-06-24) | [GOALS](../GOALS.md), this index |
| `research/immigration-mexico-npv-population-synthesis-2026-06-15.md` | `8be9f94` (2026-09-05) | [fiscal-account-2024-2026-09-05](immigration-fiscal-account-2024-2026-09-05.md), [conceptual-audit-2026-09-05](immigration-conceptual-audit-2026-09-05.md) |
| `research/immigration-msa-rent-elasticity-panel-2026-06-25.md` | `080ddae` (2026-09-05) | [housing-supply-ca-tx-2026-09-22](immigration-housing-supply-ca-tx-2026-09-22.md) |
| `research/immigration-next-agent-handoff-2026-04-11.md` | `933b831` (2026-06-24) | [friend-reproduce-guide](immigration-friend-reproduce-guide.md), this index |
| `research/immigration-next-data-upgrades.md` | `933b831` (2026-06-24) | [dataset-register](immigration-dataset-register.md) |
| `research/immigration-path-to-minus-200k-scenario-audit.md` | `b24c75c` (2026-09-16) | [lineage-cost-century-2026-09-19](immigration-lineage-cost-century-2026-09-19.md), [yearly-lifetime-cost-repair-2026-09-19](immigration-yearly-lifetime-cost-repair-2026-09-19.md) |
| `research/immigration-prototype-progress.md` | `a6baa32` (2026-06-16) | — |
| `research/immigration-public-data-acquisition-2026-04-11.md` | `933b831` (2026-06-24) | [dataset-register](immigration-dataset-register.md) |
| `research/immigration-public-mvp-profiling-findings-2026-04-11.md` | `8be9f94` (2026-09-05) | [material-repair-report-2026-09-05](immigration-material-repair-report-2026-09-05.md), [fiscal-account-2024-2026-09-05](immigration-fiscal-account-2024-2026-09-05.md) |
| `research/immigration-public-mvp-readiness-2026-04-11.md` | `8be9f94` (2026-09-05) | [material-repair-report-2026-09-05](immigration-material-repair-report-2026-09-05.md), [fiscal-account-2024-2026-09-05](immigration-fiscal-account-2024-2026-09-05.md) |
| `research/immigration-public-mvp-sipp-meps-bridge-2026-04-11.md` | `8be9f94` (2026-09-05) | [material-repair-report-2026-09-05](immigration-material-repair-report-2026-09-05.md), [fiscal-account-2024-2026-09-05](immigration-fiscal-account-2024-2026-09-05.md) |
| `research/immigration-public-mvp-variable-dictionary-2026-04-11.md` | `8be9f94` (2026-09-05) | [material-repair-report-2026-09-05](immigration-material-repair-report-2026-09-05.md), [fiscal-account-2024-2026-09-05](immigration-fiscal-account-2024-2026-09-05.md) |
| `research/immigration-receiver-counterfactuals-2026-04-22.md` | `080ddae` (2026-09-05) | [second-order-effects-2026-09-05](immigration-second-order-effects-2026-09-05.md), [material-repair-report-2026-09-05](immigration-material-repair-report-2026-09-05.md) |
| `research/immigration-receiver-failure-atlas-2026-04-22.md` | `080ddae` (2026-09-05) | [second-order-effects-2026-09-05](immigration-second-order-effects-2026-09-05.md), [material-repair-report-2026-09-05](immigration-material-repair-report-2026-09-05.md) |
| `research/immigration-receiver-node-kill-test-2026-04-23.md` | `080ddae` (2026-09-05) | [second-order-effects-2026-09-05](immigration-second-order-effects-2026-09-05.md), [material-repair-report-2026-09-05](immigration-material-repair-report-2026-09-05.md) |
| `research/immigration-resident-weighted-exposure-2026-04-22.md` | `080ddae` (2026-09-05) | [second-order-effects-2026-09-05](immigration-second-order-effects-2026-09-05.md), [material-repair-report-2026-09-05](immigration-material-repair-report-2026-09-05.md) |
| `research/immigration-scenario-composition-2026-06-15.md` | `8be9f94` (2026-09-05) | [fiscal-account-2024-2026-09-05](immigration-fiscal-account-2024-2026-09-05.md), [conceptual-audit-2026-09-05](immigration-conceptual-audit-2026-09-05.md) |
| `research/immigration-school-burden-per-adult-2026-06-15.md` | `8be9f94` (2026-09-05) | [school-peer-checks-2026-09-20](immigration-school-peer-checks-2026-09-20.md), [four-fiscal-checks-2026-09-20](immigration-four-fiscal-checks-2026-09-20.md) |
| `research/immigration-state-local-cost-examples-ny-ca-tx.md` | `b24c75c` (2026-09-16) | [complete-annual-account-2026-09-20](immigration-complete-annual-account-2026-09-20.md), [california-texas-fiscal-geography-2026-09-21](immigration-california-texas-fiscal-geography-2026-09-21.md) |
| `research/immigration-sweep-cycles-13-22-2026-06-15.md` | `8be9f94` (2026-09-05) | [fiscal-account-2024-2026-09-05](immigration-fiscal-account-2024-2026-09-05.md), [conceptual-audit-2026-09-05](immigration-conceptual-audit-2026-09-05.md) |
| `research/immigration-sweep-cycles-23-32-2026-06-15.md` | `8be9f94` (2026-09-05) | [fiscal-account-2024-2026-09-05](immigration-fiscal-account-2024-2026-09-05.md), [conceptual-audit-2026-09-05](immigration-conceptual-audit-2026-09-05.md) |
| `research/immigration-thesis-generator-audit-2026-06-16.md` | `6af9276` (2026-06-16) | — |
| `research/immigration-threshold-causal-levers-2026-04-21.md` | `080ddae` (2026-09-05) | [second-order-effects-2026-09-05](immigration-second-order-effects-2026-09-05.md), [2026-09-05-material-inference-repair](../decisions/2026-09-05-material-inference-repair.md) |
| `research/immigration-threshold-first-panel-2026-04-21.md` | `080ddae` (2026-09-05) | [second-order-effects-2026-09-05](immigration-second-order-effects-2026-09-05.md), [2026-09-05-material-inference-repair](../decisions/2026-09-05-material-inference-repair.md) |
| `research/immigration-unified-scenarios-memo.md` | `b24c75c` (2026-09-16) | [complete-annual-account-2026-09-20](immigration-complete-annual-account-2026-09-20.md), [real-fiscal-and-social-costs-2026-09-23](immigration-real-fiscal-and-social-costs-2026-09-23.md) |

### Deleted 2026-09-29, second pass (tombstones)

Fifteen more files went the same day under the same rule. Recover one with `git show <last commit>:<path>`; every one
is also on GitHub at origin/main 3791d32.

| Path | Last commit | Successor |
|---|---|---|
| `notes/provenance-tags.md` | `39560e2` (2026-06-16) | [CLAUDE.md principle 1](../CLAUDE.md#principles), `~/Projects/skills/references/provenance-tags.md` |
| `research/immigration-acquisition-gaps-2026-06-24.md` | `9ddf700` (2026-06-25) | [dataset-register § Open leads](immigration-dataset-register.md#open-leads) |
| `research/immigration-claim-candidates-2026-06-24.md` | `080ddae` (2026-09-05) | [confidence-ladder](immigration-confidence-ladder.md), [dataset-register § Open leads](immigration-dataset-register.md#open-leads) |
| `research/immigration-dataset-roadmap-additions-2026-06-24.md` | `14d4912` (2026-06-24) | [dataset-register § Open leads](immigration-dataset-register.md#open-leads) |
| `research/immigration-dataset-roadmap-batch3-2026-06-24.md` | `8be9f94` (2026-09-05) | [dataset-register § Open leads](immigration-dataset-register.md#open-leads) |
| `research/immigration-dataset-roadmap-batch4-intl-2026-06-24.md` | `c6b7780` (2026-06-24) | [dataset-register § Open leads](immigration-dataset-register.md#open-leads) |
| `research/immigration-dataset-roadmap-batch4-us-2026-06-24.md` | `c6b7780` (2026-06-24) | [dataset-register § Open leads](immigration-dataset-register.md#open-leads) |
| `research/immigration-dataset-roadmap-batch5-benefit-2026-06-24.md` | `6f7c31a` (2026-06-24) | [dataset-register § Open leads](immigration-dataset-register.md#open-leads) |
| `research/immigration-dataset-roadmap-batch5-cost-2026-06-24.md` | `6f7c31a` (2026-06-24) | [dataset-register § Open leads](immigration-dataset-register.md#open-leads) |
| `research/immigration-integration-opportunities-2026-06-24.md` | `14d4912` (2026-06-24) | [dataset-register § Warehouses](immigration-dataset-register.md#warehouses-and-derived-layers) |
| `research/immigration-paper-gaps-2026-06-24.md` | `14d4912` (2026-06-24) | [crime-rates-unauthorized-vs-native-born](immigration-crime-rates-unauthorized-vs-native-born.md), [mexican-origin-generation-incarceration-2026-09-16](immigration-mexican-origin-generation-incarceration-2026-09-16.md) |
| `research/immigration-receiver-data-acquisition-2026-04-23.md` | `2618b0d` (2026-06-16) | [dataset-register § Lost](immigration-dataset-register.md#lost-not-rebuilt-or-on-the-ssd-only) |
| `research/immigration-school-service-complexity-2026-04-11.md` | `933b831` (2026-06-24) | [dataset-register § Lost](immigration-dataset-register.md#lost-not-rebuilt-or-on-the-ssd-only) |
| `research/immigration-surge-threshold-dataset-frontier-2026-04-21.md` | `2618b0d` (2026-06-16) | [dataset-register § Lost](immigration-dataset-register.md#lost-not-rebuilt-or-on-the-ssd-only) |
| `research/immigration-theory-verdicts-2026-06-25.md` | `36c4477` (2026-09-05) | [material-repair-report-2026-09-05](immigration-material-repair-report-2026-09-05.md) |

## Revisions

- 2026-09-30 ([decision](../decisions/2026-09-30-legacy-comparisons-separate.md)): adopted separate legacy comparisons with a 2005 federal start after source verification. Corrected the pension comparator frame and distinguished financing-equivalent accrual charges from cash interest. Concept affected: historical financing attribution; no combined legacy total is adopted while the pension/borrowing bridge is unreconciled.
- 2026-10-07 ([decision](../decisions/2026-10-07-main-case-v6.md)): the adopted main case moves to v6, $389.1–461.5bn a year ($307.4–385.4bn counting benefits when paid): the 2026 Trustees Reports on current law's separate OASI and DI funds, retiree health on accrual, the 3.04M added descendants at their measured ages, and public colleges, fees and Pell keyed by use. Every consumer follows on `oct07`. The comparisons with whites, Black and Indian-origin residents and the legacy comparisons now key Pell and public colleges by IPEDS enrollment on both sides, in their October 5 runs too; the earlier rough keys charged Pell by Social Security receipt. The world ledger no longer charges the cost of raising revenue on the pension accrual, which moves its low outer span on October 5 from −$70.5bn to −$31.5bn. The reference-group paragraph adds that the rough re-key credits no one with the income tax the survey misses at the top: spread in proportion, third-plus whites roughly break even. Concept affected: the headline main case, every figure computed from it, and the comparators' education keys.
- 2026-10-07, later ([decision](../decisions/2026-10-07-comparators-income-tax-keys.md); white and Black cc793ccf, Indian ac6cc2ac, legacy 8bfae970, break conditions 406d3163, evidence map 3834b1c8): every comparison group's income taxes now take the case's own keys, which charge the whole national lines, so the tax the CPS misses at the top ($422bn federal, $45bn state) counts for the groups that pay it. The reference paragraph and the white, Black, legacy, Indian and overturn paragraphs follow: third-plus whites about break even on accrual, the gap against them is $432–436bn (was $380–385bn), and the September 27 claim of $320–405bn breaks upward. The ancestry-share break now reads v6's own companions (−30.0%; −29.9% was printed). The headline does not move: the case's own white end W, still on the earlier rule, would move it −$1.7bn at the shared allocation and +$1.1bn at the personal one, measured beside. The evidence map moves to v6 at the operator's request. Concept affected: the comparison groups' income-tax incidence.
- 2026-10-08: living text states only the live case, at the operator's request; earlier-case figures removed, recoverable at 0e0c5e28.
- 2026-10-08 ([decision](../decisions/2026-10-07-ledger-item-t-income-tax-keys.md), ladder 296–298): the generation ledger's income taxes include what the survey misses, on the main case's keys (item T); its figures here are restated (practitioner hull −$277 to −$176bn around −$204bn; lineage −$1.48M; origin screen: India's degree advantage no longer clear of zero), and partial-account figures carry the label "taxes as the survey reports them" beside the figures with the missing tax. Below-high-school Mexico-born adults' advantage over natives holds only with household costs shared. The headline paragraph gains the case's two measured residuals ($387.1–462.3bn corrected; not adopted) and the account's scope; the overturn paragraph follows C8 onto the map's live claim, which holds; the world-ledger paragraph gives the side readings (other US residents −$471bn; world +$78–287bn). Concept affected: the white-reference gaps, the education claim, the world readings.
- 2026-10-08 (outside red team): the production-term passages no longer read the file's job overlap as an estimate of
  the elasticity (its sketch chooses the component elasticities); the direct estimates carry the reading. The metro
  row's "all adverse" now names Riverside's interval, and the IR-5 parent range follows item T. Concept affected: the
  evidence on the production elasticity.

<!-- knowledge-index
generated: 2026-09-29T07:51:14Z
hash: c6e94d9ecded

cross_refs: decisions/2026-09-05-material-inference-repair.md, decisions/2026-09-20-ancestry-outcome-data-ceiling.md, decisions/2026-09-20-category-service-response.md, decisions/2026-09-23-main-case-general-government-and-use-keys.md, decisions/2026-09-24-main-case-audit-and-outside-checks.md, decisions/2026-09-25-school-dilution-priced-beside.md, decisions/2026-09-26-main-case-finite-removal-and-consumption-key.md, decisions/2026-09-26-main-case-schools-full-cost.md, decisions/2026-09-27-main-case-capital-return-and-long-run-responses.md, decisions/2026-09-28-pension-accrual-payable-benefits.md, decisions/2026-09-28-social-items-fear-security-schools.md, decisions/2026-09-28-social-items-more-benefits.md, decisions/2026-09-28-social-items-pollution-crashes.md, decisions/2026-09-28-social-items-scale-benefits.md, decisions/2026-09-29-crash-item-with-against-without.md, decisions/2026-09-29-delete-superseded-and-cruft-docs.md, research/immigration-acquisition-gaps-2026-06-24.md, research/immigration-adversarial-review.md, research/immigration-benefits-and-macro-scale-2026-09-19.md, research/immigration-capacity-falsification-2026-04-21.md, research/immigration-capacity-frontier-2026-04-21.md, research/immigration-causal-everify-card-vs-borjas.md, research/immigration-causal-internal-vs-immigrant-newcomers.md, research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md, research/immigration-causal-saiz-elasticity-rent.md, research/immigration-causal-surge-2021-2024.md, research/immigration-causal-synthesis-2026-04-18.md, research/immigration-claim-candidates-2026-06-24.md, research/immigration-claims-evolution-ledger-2026-04-23.md, research/immigration-claims-matrix-2026-04-11.md, research/immigration-conclusion-audit-running-fixes.md, research/immigration-costs-causal-analysis.md, research/immigration-country-fiscal-tensor-2026-06-15.md, research/immigration-county-outcome-panel-2026-04-21.md, research/immigration-dataset-roadmap-additions-2026-06-24.md, research/immigration-dataset-roadmap-batch3-2026-06-24.md, research/immigration-dataset-roadmap-batch4-intl-2026-06-24.md, research/immigration-dataset-roadmap-batch4-us-2026-06-24.md, research/immigration-dataset-roadmap-batch5-benefit-2026-06-24.md, research/immigration-dataset-roadmap-batch5-cost-2026-06-24.md, research/immigration-dataset-roadmap.md, research/immigration-economist-debate-sheet-2026-04-22.md, research/immigration-economist-one-pager-2026-04-22.md, research/immigration-epistemic-check.md, research/immigration-europe-caucasian-fiscal-findings-2026-06-15.md, research/immigration-federal-distribution-findings-2026-06-15.md, research/immigration-fiscal-welfare-ledger-map.md, research/immigration-frontier-rethink-2026-04-22.md, research/immigration-full-spectrum-costs-scoring-model.md, research/immigration-full-spectrum-costs-unauthorized-memo.md, research/immigration-integration-opportunities-2026-06-24.md, research/immigration-knowledge-delta-agent-loop-2026-06-16.md, research/immigration-lifetime-country-approx-brainstorm-2026-06-15.md, research/immigration-lifetime-dataset-brainstorm-2026-06-15.md, research/immigration-lifetime-fiscal-generators.md, research/immigration-lifetime-unified-theory-2026-06-15.md, research/immigration-main-question-reset.md, research/immigration-mexico-npv-population-synthesis-2026-06-15.md, research/immigration-msa-rent-elasticity-panel-2026-06-25.md, research/immigration-next-agent-handoff-2026-04-11.md, research/immigration-next-data-upgrades.md, research/immigration-paper-gaps-2026-06-24.md, research/immigration-path-to-minus-200k-scenario-audit.md, research/immigration-prototype-progress.md, research/immigration-public-data-acquisition-2026-04-11.md, research/immigration-public-mvp-profiling-findings-2026-04-11.md, research/immigration-public-mvp-readiness-2026-04-11.md, research/immigration-public-mvp-sipp-meps-bridge-2026-04-11.md, research/immigration-public-mvp-variable-dictionary-2026-04-11.md, research/immigration-receiver-counterfactuals-2026-04-22.md, research/immigration-receiver-data-acquisition-2026-04-23.md, research/immigration-receiver-failure-atlas-2026-04-22.md, research/immigration-receiver-node-kill-test-2026-04-23.md, research/immigration-resident-weighted-exposure-2026-04-22.md, research/immigration-scenario-composition-2026-06-15.md, research/immigration-school-burden-per-adult-2026-06-15.md, research/immigration-school-service-complexity-2026-04-11.md, research/immigration-state-local-cost-examples-ny-ca-tx.md, research/immigration-surge-threshold-dataset-frontier-2026-04-21.md, research/immigration-sweep-cycles-13-22-2026-06-15.md, research/immigration-sweep-cycles-23-32-2026-06-15.md, research/immigration-theory-verdicts-2026-06-25.md, research/immigration-thesis-generator-audit-2026-06-16.md, research/immigration-threshold-causal-levers-2026-04-21.md, research/immigration-threshold-first-panel-2026-04-21.md, research/immigration-unified-scenarios-memo.md
table_claims: 136

end-knowledge-index -->
