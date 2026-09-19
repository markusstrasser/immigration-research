# Population-normalized fiscal differences, macro scale and benefits

**Later release, 2026-09-19:** Use [observed2024 finance and national boundaries](immigration-macro-reconciliation-2026-09-19.md)
and [matched skills/capital/tax benefits](immigration-matched-benefits-2026-09-19.md).
The homogeneous fixed-capital case below is a retained benchmark, not a bound.

Date: 2026-09-19. Calculation index, not essay text. [FRAMING-SENSITIVE]
Gains to residents outside the observed Mexican-origin union differ from gains
to all natives, all citizens or everyone. LLM-assisted interpretation is subject
to the [instrument caveat](../notes/llm-bias-caveat.md).

## Fiscal comparison after population normalization

[MODEL OUTPUT] Expanded partial account, income-year2024 CPS ASEC2025,
2024-price dollars, all ages and education. Negative balances shown as positive
deficits. Shared and personal are allocation conventions, not confidence bounds.

| Population | Millions | Shared annual deficit/person | Personal annual deficit/person |
|---|---:|---:|---:|
| Observed Mexican-origin union | 40.897 | $5,314 | $5,850 |
| Third-plus non-Hispanic white reference | 173.054 | $1,221 | $1,156 |

The white reference is 4.23 times larger. Per-person deficits are 4.35 and 5.06
times larger for the target. Holding actual age mixes, the difference relative
to a same-sized white-reference population is $167.38bn shared / $191.96bn personal.
These are descriptive gaps, not effects of replacing a population. The existing
common-age shared comparison also retains a large gap, $7,151.89 per standardized
person-year. [SOURCE: `ledger_absolute_2026_09_17/derived/age_profiles.csv`,
`complete_gaps.csv`, new `benefit_scale_2026_09_19/derived/fiscal_scale.csv`.]

## National finances

[OFFICIAL DATA] The 2026 Economic Report of the President reports CY2024 nominal
GDP $29,298bn (B-3, p374), revised FY2024 federal receipts $4,919.884bn and outlays
$6,735.261bn (B-48, p429), and consolidated CY2024 government current receipts
$8,008.3bn and current expenditures $10,061.5bn (B-49, p430). Federal cash deficit
is $1,815.377bn; all-government negative net saving is $2,053.2bn. Current saving
and cash deficits have different accounting boundaries.
[SOURCE: [official tables](https://www.whitehouse.gov/wp-content/uploads/2026/04/2026-Economic-Report-of-the-President.pdf).]

[CALCULATION] The $217.32–239.24bn modeled target deficit equals 0.742–0.817% of
GDP, 12.0–13.2% of the federal deficit, or 2.16–2.38% of all-government current
expenditure in magnitude. None identifies its share of an official macro outcome.

[MODEL OUTPUT] The shared account sums to $6,070.860bn receipts minus
$6,729.061bn outlays = **−$658.201bn** nationally. Its disjoint partition is
target −$217.316bn plus other residents −$440.885bn. Target residents are 12.15%
of the civilian-household population and 33.02% of this partial modeled deficit.
Do not call that a share of the official federal deficit.

[SOURCE / GAP] Against the model's mixed-vintage comparator, receipts cover
72.88% and spending 70.00%; the balance residual is −$625.274bn. The comparator
combines federal2024 with Census state/local2022 repriced to2024 and nets federal
grants once. Omitted defense, interest and general-government allocations alone
are about $1.760tn nationally; omitted receipts and other differences offset part
of this. The residual cannot be assigned proportionally to groups or treated as
an error bar. Institutional N also omits some foreign-origin groups nationally.
A personal full-national reconciliation is not exported. [SOURCE:
`ledger_absolute_2026_09_17/derived/audit.json`, `national_reconciliation.csv`;
`absolute_ledger.py:1558`; `consolidation.py`.]

Macro closure requires matching years and government boundaries, reconciling
receipts and final expenditure separately, removing intergovernmental transfers
once, allocating included items over disjoint populations, and exposing the
unallocated balance. Scaling all balances to the federal deficit is invalid.
[ACCOUNTING]

## Benefits calculated for the same population

[SURVEY ESTIMATE] The union has 20.532m people with positive annual earnings and
$1,049.422bn net annual cash earnings, 8.3527% of the national $12,563.922bn total.
Annual earners are not current employment or labor hours. Income paid to this
group does not measure the benefit accruing to others. Positive-only earnings
used for the efficiency proxy are $1,049.584bn, a share of 8.3529%; wage-only
income is $998.728bn. [SOURCE: fresh canonical CPS extraction,
`benefit_scale_2026_09_19/derived/income.csv`, with 161 aligned weights.]

[MODEL OUTPUT] In a fixed-capital, homogeneous-labor Cobb-Douglas model, the
benefit to other residents is `Y * [1 - s*m - (1-m)^s]`, where `m` is the target
labor-efficiency share and `s` the assumed labor output share. Earnings shares
proxy efficiency shares. Across wage/total-earnings proxies and
`s=0.60/0.65/0.70`, GDP normalization gives about **$22–26bn/year**; calibration
to cash earnings instead gives about **$13–18bn/year**. At `s=0.65`, total-earnings
GDP normalization gives **$24.17bn**. These are assumption scenarios, not an
empirical range for all benefits. [SOURCE:
[generator and checks](../infra/immigration-fiscal/benefit_scale_2026_09_19/README.md);
[NAS chapter4, pp169–174](https://www.nationalacademies.org/read/23550/chapter/8).]

Other residents own all capital in this model. Technology is fixed and pricing
competitive. Skill complementarity beyond homogeneous efficiency, trade, land,
foreign ownership, innovation and congestion are omitted. With complete capital
adjustment in the same model, this particular surplus is zero. Neither zero nor
the fixed-capital result bounds all benefits. A generations-old stock is poorly
represented by an unanticipated fixed-capital labor shock. [MODEL / DISCONFIRMATION]

This channel under these assumptions is much smaller than the attributed fiscal
deficit. Subtracting it would still not identify welfare loss: fiscal allocation
is not the matching avoidable-spending counterfactual, and financing incidence
and other channels remain unresolved. [INFERENCE]

The separate [services-price/native-hours scenarios](immigration-consumer-price-and-native-hours-2026-09-18.md)
remove roughly3.17m Mexico-born high-school-dropout workers; recipients include
US-born Mexican descendants. Treatment and beneficiaries differ. Do not scale
them to40.9m people or add them to this production surplus without overlap checks.

## Persistent origin differences

[INFERENCE] Persistent origin-associated outcomes can aid forecasting without
identifying an ultimate cause. Education can mediate intergenerational outcomes;
controlling for descendants' education does not erase the fiscal consequence of
a persistent education distribution. Equal formal rights do not guarantee equal
outcomes. Whether origin adds predictive value beyond observed applicant/family
characteristics requires out-of-sample comparison and transport to the actual
admission cohort. Irish/French historical comparisons need matched cohort, age
and ancestry definitions before numerical ranking. No new causal ethnic
mechanism is established here.

## Revisions

2026-09-19, later: [Matched accounts and projection checks](../decisions/2026-09-19-matched-accounts-and-projection-checks.md)
extends benefits to skills, capital adjustment and tax/private conservation,
and updates the available state/local fiscal source vintage.
