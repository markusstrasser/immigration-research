**Verdict:** Most of the school cost the account leaves free is diluted instruction, not economies of
scale. At the account's own response (spending follows the group's pupils at 0.63–0.66), instruction
carries 58% of the free $51–59bn a year, pupil and staff support 11%, and fixed costs (administration,
buildings, transport) 31%. Priced with Jackson–Mackevicius and Chetty–Friedman–Rockoff, the instruction
shortfall costs other residents' pupils about **$16bn a year in present-value lifetime earnings** (JM's
90% range of contexts: −$2bn to +$36bn), or $9–13bn on bounded forms of the same rule. The loss is
concentrated: the West bears half, and per other pupil the poorest fifth of districts loses four times
what the least poor lose. It is also transitional within districts: over 19 years spending follows
pupils at 0.87 (instruction 0.92), which cuts the price to $3.6bn, but then the account's 63–66% is too
low and the account undercharges schools. Between states the lag lasts: CBO's design on Census data
gives 0.65–0.79 unweighted (CBO: 0.63–0.66), and pupil-weighted or long-difference state estimates are
lower still (0.27–0.56). Compensatory state and federal money follows the group's pupils but is offset
by falling local revenue, so composition leaves instruction per pupil unchanged within districts. Class
size gives $2.6bn and is not added; peer effects stay unpriced; the channel sits beside the account,
and its tax consequence (about $5bn a year, decades later) is not added. [CALCULATION: `price.py` →
`derived/winners_losers_rows.csv`]

| Other residents' pupils, $bn a year (PV of lifetime earnings, 2024 dollars) | Low | Central | High |
|---|---:|---:|---:|
| Instruction, account's response (linear rule, against absence) — **the row beside the account** | −2.1 | **16.1** | 35.5 |
| Same, constant-elasticity form (overlaps) | −1.5 | 12.6 | 28.0 |
| Same, full-funding split: other pupils' share (overlaps) | −1.1 | 9.2 | 20.2 |
| Pupil and staff support, account's response (beside; outside the brief's instruction measure) | −0.5 | 4.0 | 8.8 |
| Instruction, 19-year within-district response (overlaps) | −0.5 | 3.6 | 7.7 |
| Composition: compensatory money net of falling local revenue (overlaps; measured) | −3.7 | 2.6 | 8.8 |
| Class size, same resource in teachers (overlaps; never added) | | 2.6 | 8.8 |
| Peer effects | unpriced | | |

Low and high are JM's 90% range of contexts, except composition (the 95% CI of the district estimate)
and class size (the 2000–18 and 2018–23 teacher responses). A negative low end means a gain.

## 1. What the free 34–37% is made of

The adopted account charges each of the group's 8.487m pupils 63–66% of average spending
([school-cost lane](../school_cost_where_enrolled_2026_09_24/)). At the account's school step of
$87.1–114.0bn, the part charged to no one is $51.2–58.7bn a year. [CALCULATION: `price.py`,
87.14 × 0.37/0.63 and 113.96 × 0.34/0.66]

Census F-33 district finance for FY2000–FY2024 splits current spending into its functions. Within
districts, pupil-weighted, with district-spell and state-by-year fixed effects, each function's response
to enrollment is estimated by one-year differences, a three-year distributed lag, stacked 4–5-year
differences, one 19-year difference and all-horizon fixed effects in logs and levels. Each function then
contributes its share of spending times its non-response. [CALCULATION: `estimate_functions.py`,
`decompose.py` → `derived/function_elasticities.csv`, `derived/nonresponse_summary.csv`]

| Horizon (pupil-weighted, FY2000–2019) | Current spending response | Instruction response | Non-response | Instruction share of it | With pupil and staff support | Fixed costs |
|---|---:|---:|---:|---:|---:|---:|
| 1 year | 0.449 [0.383, 0.515] | 0.481 [0.409, 0.553] | 0.551 | 58% | 69% | 31% |
| 3 years | 0.700 [0.636, 0.763] | 0.749 [0.677, 0.822] | 0.300 | 53% | 64% | 36% |
| 4–5 years | 0.758 [0.706, 0.810] | 0.807 [0.745, 0.869] | 0.242 | 50% | 62% | 38% |
| 19 years (2000→2019) | 0.869 [0.821, 0.916] | 0.924 [0.861, 0.986] | 0.131 | 37% | 47% | 53% |
| All horizons, logs | 0.830 [0.787, 0.873] | 0.890 [0.837, 0.943] | 0.170 | 42% | 54% | 46% |
| All horizons, levels (marginal/average cost) | 0.734 [0.690, 0.778] | 0.768 [0.713, 0.823] | 0.266 | 54% | 66% | 34% |

Instruction is 62% of current spending but 58% of the short-run non-response, so it responds only a
little more than the rest. Administration (0.39 in one year), operation and maintenance (0.40) and
transport (0.38) respond less, as fixed costs should, but not by much. Spending is sticky downward: in
one year it follows growth at 0.57 and decline at 0.34 (instruction 0.60 and 0.37). Capital outlay
(0.05 in one year, 0.75 over 19) and interest sit outside current spending and outside the account's
line; they are reported and never added. [CALCULATION: `derived/function_elasticities.csv`, specs
`fd_asym_fy2000_2019`, `ld19_2000_2019`]

So the brief's two readings are both partly true. At the one-to-five-year horizons that match the
account's response, half to three-fifths of the free part is instruction per pupil that did not keep
pace, which is dilution; a third is fixed cost spread over more pupils. Over two decades districts close
most of the instruction gap, and fixed costs become the larger part of a much smaller remainder.

**Account-consistent instruction response.** If current spending responds at the account's r and
instruction carries the one-year share φ = 0.584 of the non-response, instruction responds at
b = 1 − φ(1 − r)/w, with w = 0.618 its share of current spending: **0.650 at r = 0.63 and 0.678 at
r = 0.66**. With φ from the 3-year or 4–5-year split, b is 0.681–0.722. [CALCULATION: `price.py`
`horizons()`]

## 2. Reconciling with CBO's 63–66%

CBO regresses a state's per-pupil spending growth, net of federal grants, on its enrollment growth
relative to the nation, with state fixed effects, over state CCD data 1999–2000 to 2019–20; per-pupil
spending falls 0.37 points per point of growth and 0.34 per point of decline, a response of 0.63–0.66.
[SOURCE: CBO, *The Fiscal Impact of Immigration on State and Local Governments* (publication 61256),
pp.10, 29–30; `sources/immigration-fiscal/data/cbo/61256-immigration-state-local.pdf`]

The same design on F-33 state totals lands near CBO's range unweighted (0.65–0.79, net of federal
revenue, depending on the end year) and falls well below it when states are weighted by pupils:

| State panel (F-33, 50 states + DC) | FY2000–2019 | FY2000–2024 |
|---|---:|---:|
| Net of federal revenue, unweighted (CBO's measure) | 0.788 (SE 0.128) | 0.649 (0.142) |
| Current spending, unweighted | 0.707 (0.157) | 0.597 (0.172) |
| Current spending, pupil-weighted | 0.349 (0.174) | 0.271 (0.147) |
| Net of federal, pupil-weighted | 0.453 (0.241) | 0.295 (0.224) |
| Current spending, growth / decline years, unweighted | 0.453 / 0.813 | 0.260 / 0.763 |
| Long difference 2000→2019 (2024), current, unweighted | 0.488 (0.132) | 0.563 (0.126) |
| Same, instruction | 0.418 (0.151) | 0.533 (0.163) |

[CALCULATION: `estimate_functions.py` `state_cbo()` → `derived/function_elasticities.csv`]

The reconciliation: CBO's number is a state-level, medium-horizon response. Within a state, a growing
district's spending catches up (0.87 over 19 years) because state formulas pay per pupil; between
states, faster-growing states let per-pupil spending lag (0.49–0.56 over two decades). The
within-district design absorbs every state-by-year shock, so it cannot see dilution that happens
through state budgets. The account's 0.63–0.66 sits between the district short run (0.45) and long run
(0.87), and above the state long difference. [FRAMING-SENSITIVE] Which horizon applies to a stock of
pupils present for decades is a judgment, not an estimate.

The state estimates are correlations: fast-growing states (the South and West) differ from slow ones
in cost levels, tax preferences and income growth, so the state long difference is not a causal
response. [INFERENCE]

A shift-share instrument (fall-2000 Hispanic share × national growth of Hispanic and other enrollment,
Digest table 203.50) is weak in every specification: first-stage F 3.6 unweighted, 1.1 pupil-weighted,
1.7 in long differences. Its 2SLS estimates are in the appendix and are not used. [CALCULATION:
`estimate_iv.py` → `derived/iv_first_stage.csv`]

**Consistency condition for the account.** If the 19-year within-district response held nationally,
the free part would shrink from $51–59bn to $18–23bn and the school step would be $120–150bn instead
of $87–114bn. The account cannot have both a low response and no dilution: the smaller its school
charge, the larger the loss to other pupils. [CALCULATION: full cost 87.14/0.63 = 138.3 and
113.96/0.66 = 172.7; × 0.869 = 120.2 and 150.0; × 0.131 = 18.1 and 22.6]

## 3. Does money follow the group's pupils? (task 2)

F-33 separates Title I (C14), federal bilingual aid through the state (B11, Title III), state
compensatory programs (C06) and state bilingual programs (C07). Formula weights paid inside general
state aid (California's LCFF supplemental and concentration grants; Texas's compensatory and
bilingual allotments) are not separable from general formula aid (C01). [SOURCE: Census F-33
technical documentation FY2015, `_cache/f33/school15doc.pdf`]

Across districts in the same state (FY2020, pupil-weighted), revenue per pupil rises with the Hispanic
share, but because of poverty: +$1,806 per unit share (SE 422) falls to +$439 (656) once child poverty
is controlled. English learners do carry money: +$3,797 (1,780) per unit EL share with poverty held,
+$3,697 (1,337) in current spending, +$85 (24) federal bilingual and +$254 (126) state bilingual aid.
Instruction per pupil does not rise significantly with either share once poverty is held
(Hispanic +$166, SE 314; EL +$1,125, SE 1,287). [CALCULATION: `compensatory.py` →
`derived/compensatory_estimates.csv`, FY2020 cross-sections]

Within districts over FY2001–FY2020, holding enrollment, with district and state-by-year effects:

| Dollars per pupil per unit Hispanic share (2024 dollars) | Estimate | SE |
|---|---:|---:|
| State revenue | +3,404 | 711 |
| of which general formula aid | +3,142 | 713 |
| Federal revenue | +1,161 | 196 |
| of which Title I | +501 | 166 |
| Local revenue | −6,215 | 1,772 |
| Total revenue | −1,650 | 2,253 |
| Current spending | −1,284 | 1,744 |
| Instruction | −1,175 | 1,459 |

In logs, total current spending follows pupils at 0.831 (SE 0.021) with or without the Hispanic share,
whose own coefficient is −0.012 (0.066). [CALCULATION: `derived/compensatory_estimates.csv`,
`panel_fy2001_2020`]

So compensatory money does follow the group's pupils: state formula aid and Title I rise with the
share. But local revenue per pupil falls by more, and instruction per pupil does not measurably change
with composition. The dilution comes through enrollment, not composition. Whether the local fall is
lower tax rates or a smaller tax base per pupil cannot be told from F-33. [INFERENCE]

## 4. Price of the dilution (task 3)

**Per pupil-year.** Jackson and Mackevicius pool quasi-experimental US studies of policy-induced
spending changes (40 test-score estimates): $1,000 per pupil (2018 dollars) sustained four years raises
test scores 0.0316 SD (SE 0.00559), with a 90% range of −0.004 to 0.067 SD across contexts; the
population is US public-school pupils exposed to finance reforms and capital or operating spending
changes. Chetty, Friedman and Rockoff find a 1 SD higher test score is associated with 12% higher
earnings at age 28 (Appendix Table 3: $2,585, SE 59, on a mean of $21,622), in a large urban
district's grades 3–8. Their present value of lifetime earnings at age 12 is $522,000 (2010 dollars,
3% real). Dividing JM by four for one year of exposure [ASSUMPTION: linear
accumulation], and carrying dollars with CPI-U, **one dollar of instruction lost for one pupil-year
costs $0.570 of lifetime earnings in present value** (JM range −$0.072 to $1.208; $0.489 with CFR's
value-added-implied 10.3% per SD). [CALCULATION: `price.py` `pv_per_dollar()` →
`derived/pricing_constants.json`; quotes in section 10]

**Per other pupil and nationally.** The group's pupils are placed in districts with the school-cost
lane's Mexican-origin weights (CCD 2023–24), scaled to 8.487m; instruction per pupil is F-33 FY2024
(group-weighted $9,902). Instruction dollars not following the group, district by district, are
(1 − b) × instruction per pupil × group pupils. At the account's response the average other pupil in
the group's districts loses $689–750 of instruction a year, worth $393–427 in present value; across
all 39.45m other pupils the present value averages $408 a year. [CALCULATION: `price.py` →
`derived/pricing_by_horizon.csv`]

| Response basis (FY2024 prices) | Instruction response | Instruction $bn a year not following the group | PV of other pupils' earnings, $bn a year: JM low / central / high |
|---|---:|---:|---|
| Account, r = 0.63 | 0.650 | 29.4 | −2.1 / 16.8 / 35.5 |
| Account, r = 0.66 | 0.678 | 27.0 | −1.9 / 15.4 / 32.7 |
| Account, instruction share from the 3-year split | 0.681–0.707 | 24.7–26.8 | 14.1–15.3 central |
| Account, instruction share from the 4–5-year split | 0.698–0.722 | 23.3–25.4 | 13.3–14.5 central |
| District, 1 year | 0.481 | 43.6 | −3.1 / 24.9 / 52.7 |
| District, 3 years | 0.749 | 21.1 | −1.5 / 12.0 / 25.5 |
| District, 4–5 years | 0.807 | 16.2 | −1.2 / 9.2 / 19.6 |
| District, 19 years | 0.924 | 6.4 | −0.5 / 3.6 / 7.7 |
| District, all horizons, logs | 0.890 | 9.3 | −0.7 / 5.3 / 11.2 |
| District, all horizons, levels | 0.768 | 19.5 | −1.4 / 11.1 / 23.6 |
| State, CBO design, unweighted | 0.902 | 8.3 | −0.6 / 4.7 / 10.0 |
| State, CBO design, pupil-weighted | 0.335 | 55.9 | −4.0 / 31.8 / 67.5 |
| State, long difference 2000–2019 | 0.418 | 48.9 | −3.5 / 27.8 / 59.0 |

At FY2019 prices carried to 2024 dollars (pre-COVID), the account row is $26.2bn and $14.9bn
(r = 0.63). [CALCULATION: `derived/pricing_by_horizon.csv`, `fy2019_in_2024usd`]

**Where the linear rule is stretched.** The account's rule charges r of average cost per group pupil,
so in its own arithmetic the unfunded (1 − r) is spread over the district's other pupils. 39% of the
loss falls in districts where the group is a majority; there other pupils would each gain $5,500 to
$19,000 of instruction a year on the group's absence, far outside the $1,000 changes JM's studies
measure. Two bounded forms avoid that extrapolation: the constant-elasticity form of the same response
($12.0–13.2bn), and a full-funding split that keeps the account's dollars, in which every pupil in a
district is short (1 − b) × s × instruction per pupil, so other pupils bear their share 1 − s
($8.8–9.5bn) and the group's own pupils the rest ($6.9bn). [CALCULATION: `price.py`; scratch
diagnostic of the same frame: loss share by group share of district 15% (s ≤ 0.1), 15% (0.1–0.25),
31% (0.25–0.5), 25% (0.5–0.75), 14% (> 0.75)] [FRAMING-SENSITIVE] The row beside the account uses the
group's absence, the account's own counterfactual; the full-funding split answers a different
question, how the shortfall is shared among the pupils who are there.

## 5. Who bears it: region and district income

At the account's response (mean of the two ends), central present value:

| Other residents' pupils | Other pupils (m) | Group share of pupils | $bn a year | Per other pupil, $ a year |
|---|---:|---:|---:|---:|
| West | 7.58 | 35.0% | 8.32 | 1,097 |
| South | 15.98 | 16.6% | 4.72 | 295 |
| Midwest | 8.78 | 9.9% | 2.00 | 228 |
| Northeast | 7.11 | 3.5% | 1.04 | 146 |
| Q1, least-poor districts | 8.84 | 7.8% | 1.36 | 153 |
| Q2 | 8.24 | 14.1% | 2.47 | 300 |
| Q3 | 7.72 | 19.4% | 3.46 | 448 |
| Q4 | 7.14 | 23.5% | 4.18 | 586 |
| Q5, poorest districts | 7.51 | 23.7% | 4.61 | 613 |

Quintiles are pupil-weighted national quintiles of SAIPE 2023 child poverty in the district.
[CALCULATION: `price.py` → `derived/pricing_by_region_income.csv`] The loss falls where the group
lives: in the West and in poorer districts, whose other pupils are themselves disproportionately
Hispanic and low-income. [INFERENCE]

## 6. Class size, the same loss in teachers (not added)

Teachers follow pupils within states at 0.931 (95% CI 0.911–0.952) over 2000→2018, pupil-weighted,
11,172 districts, and at 0.756 (0.670–0.842) over 2018→2023, 12,046 districts. Holding a pupil-teacher
ratio of 16.14, other pupils' ratio rises 0.17 or 0.57 pupils. With JM's own benchmark ($1,000 for four
years ≈ 1.8 fewer pupils per class, p.427–428), that is $2.6bn or $8.8bn a year, beside the 19-year
instruction figure of $3.6bn and within the range above. It measures the same resource loss and is
never added. [CALCULATION: `class_size.py`, `price.py` → `derived/class_size_elasticities.csv`,
`derived/pricing_class_size.csv`]

## 7. Peer effects (task 4)

The repo's [capacity memo](../../../research/immigration-school-capacity-harms-2026-09-20.md) table:
Florida (Figlio et al., ReStud 2024, US-born white pupils, +10 pp foreign-born cohort exposure) math
+0.0128 SD, CI −0.0082 to +0.0338; North Carolina (Diette–Oyelere 2017) no significant average
effect on white pupils; Hamburg (+1 pp refugee share) +0.0027 SD, CI −0.0087 to +0.0141; Denmark
(any refugee arrival) reading −0.010 SD, CI −0.028 to +0.008; Italy (Ballatore–Fort–Ichino 2018, one
immigrant replacing a native at fixed class size) language −1.58 points correct, CI −3.09 to −0.07,
on a weak first stage (F ≈ 2.8). The only interval excluding zero on the harm side is Italy's, on a
weak instrument and a non-US population. By symmetry rule 1, no peer channel is priced; by rule 5, the
Florida gain is not priced either. [SOURCE: capacity memo, table and sources there]

## 8. Symmetry: compensatory benefits priced the same way (task 5)

The composition channel is the compensatory benefit to other pupils, net of the local revenue that
falls with it, priced exactly as the loss: the within-district effect of Hispanic share on instruction
per pupil (−$1,175, 95% CI −$4,034 to +$1,684) times the change in Hispanic share the group's absence
would make, times the same $0.570 per dollar. Central: a further **$2.6bn loss**; the interval runs
from a $3.7bn gain to an $8.8bn loss. It is marked as overlapping the account row, because CBO's
response was estimated on enrollment growth that was mostly Hispanic and so already carries it.
[CALCULATION: `price.py` → `derived/pricing_composition.csv`]

The gross compensatory flows are shown by payer (section 9). Scale economies are the account's
benefit side for taxpayers and are inside it. Apart from the Florida peer estimate above, unpriced like
its harm-side counterpart, this pass found no other benefit channel for other pupils.

## 9. Winners and losers

`derived/winners_losers_rows.csv` holds one row per group and channel, with the brief's columns.
Money is $bn a year; human-capital rows are present values of lifetime earnings.
`relation_to_account`: `beside` rows can be added to the account's social total; `overlaps:` rows are
alternative measures of a channel already counted; `inside` rows are splits of money the account
already carries.

| Group | Channel | Direction | Low | Central | High | Basis | Relation |
|---|---|---|---:|---:|---:|---|---|
| Other residents' pupils | instruction, account's response | loss | −2.1 | 16.1 | 35.5 | modelled | beside |
| Other residents' pupils | pupil and staff support | loss | −0.5 | 4.0 | 8.8 | modelled | beside |
| Other residents' pupils | peer effects | loss | | | | unpriced | beside |
| The group's pupils | shared instruction shortfall (against full funding) | loss | −0.8 | 6.9 | 15.3 | modelled | overlaps |
| Taxpayers | unfunded instruction | gain | 29.9 | 32.1 | 34.3 | modelled | inside |
| Taxpayers | unfunded pupil and staff support | gain | 5.5 | 5.9 | 6.3 | modelled | inside |
| Taxpayers | scale economies (administration, plant, transport, food) | gain | 15.8 | 17.0 | 18.1 | modelled | inside |
| State taxpayers | compensatory financing | loss | 12.5 | 21.1 | 29.7 | measured | inside |
| Federal taxpayers | compensatory financing | loss | 4.8 | 7.2 | 9.6 | measured | inside |
| Local taxpayers in the group's districts | local revenue falls $38.5bn | gain | | | | unpriced | inside |
| Future taxpayers | lower tax on other pupils' earnings, decades later | loss | −0.5 | 4.8 | 12.4 | assumed | overlaps |

Region, income-quintile, long-run, bounded, composition and class-size rows are in the file and in
Table A12. The taxpayers' "gain" rows are the account's free part: the same dollars other pupils lose.
The state and federal rows split by payer spending the account already charges. The future-tax row is
part of the gross earnings loss (25–35% combined rate, an assumption) and falls decades later, when
today's pupils work; it is stated and not added. [CALCULATION: `price.py` `winners_losers()`]

## 10. Verbatim sources for the two pricing parameters

Jackson, C. Kirabo, and Claire L. Mackevicius (2024), "What Impacts Can We Expect from School Spending
Policy? Evidence from Evaluations in the United States," *AEJ: Applied Economics* 16(1): 412–46
[SOURCE: https://kirabojackson.com/pdfs/jackson-mackevicius-2024-school-spending-policy.pdf,
`_cache/lit/jm2024.pdf`]:

- p.413: "The pooled meta-analytic average estimate indicates that, on average, a $1,000 per pupil
  increase in school spending sustained over four years increases test scores by 0.0316σ ( p-value <
  0.001)."
- p.418: "for each study we compute the overall effect of a $1,000 per pupil spending increase (in 2018
  dollars using CPI 2020), sustained for four years, on standardized outcomes"
- p.424: "An implication of our pooled estimate 0.0316σ, our estimated heterogeneity 0.0207σ, and the
  normality of true effects is that while the pooled effect is 0.0316σ, in other contexts one can
  expect estimates between −0.004σ and 0.067σ about 90 percent of the time (Figure 2)."
- p.425, Table 3, column 1 (also Table 2, column 1, p.424): Overall 0.0316 (0.00559), 40 observations.
- pp.427–428: "our $1,000 test score effects are equivalent to reducing class size by 1.8 students";
  p.428: "For both benchmarking interventions, the spending impacts on educational attainment are at
  least twice as large as those on test scores."

Chetty, Raj, John N. Friedman, and Jonah E. Rockoff (2013), "Measuring the Impacts of Teachers II:
Teacher Value-Added and Student Outcomes in Adulthood," NBER Working Paper 19424 (published *AER*
2014) [SOURCE: https://www.nber.org/system/files/working_papers/w19424/w19424.pdf,
`_cache/lit/cfr_w19424.pdf`]:

- p.19 (PDF p.21): "A 1 SD increase in student test scores, controlling for the student- and
  class-level characteristics Xit , is associated with a 12% increase in earnings at age 28 (Appendix
  Table 3, Column 3, Row 2)."
- p.19 (PDF p.21): "Assume ... that earnings are discounted at a 3% real rate (i.e., a 5% discount rate
  with 2% wage growth) back to age 12, the mean age in our sample. Under these assumptions, the mean
  present value of lifetime earnings at age 12 in the U.S. population is approximately $522,000."
- p.12 (PDF p.14): "Conditional on the student- and class-level controls Xit that we define in Section
  III.A below, a 1 SD increase in the current test score is associated with $2,600 (12%) increase in
  earnings on average."
- Appendix Table 3, column 3, row 2: $2,585 (SE 59) on mean earnings of $21,622.

## 11. Steel-man, disconfirmation and the literature

**The case that the free part costs pupils nothing.** Marginal pupils cost less than average because
buildings, administration and routes are shared; weighted formulas route money to poor and
English-learner pupils; districts adapt over time; and US peer studies find no harm. The data support
part of it: a third of the short-run shortfall is fixed cost, compensatory money is real, the 19-year
response is 0.87, and no US peer estimate is negative.

**The case that dilution is large.** The one-year response is 0.45 and sticky on the way down; state
budgets do not scale with state enrollment (0.27–0.56 on the pupil-weighted and long-difference
designs); and JM's attainment effects are at least twice their test-score effects, so the test-score
route understates the earnings loss.

Contrary and supporting studies found in this pass, with the populations they measure (rule 1; no
intervals were recovered where none is quoted):

| Study | Population and design | Finding | Direction |
|---|---|---|---|
| St. Clair (2024, *Regional Science and Urban Economics* 109; 2023 working paper) | Miami-Dade school district after the 1980 Mariel boatlift, synthetic control | Expenditures +26% a year on average 1981–90, current operating spending +20% (the paper's Table A2), against enrollment +8%; the district's effect exceeds all 43 placebos; financed by state transfers and about 5 basis points of property tax | Against dilution |
| Ozdogan and Shih (2025, IZA DP 18339), PDF p.6 | New York City public elementary schools, 2022–24 asylum-seeker inflow | Weighted Fair Student Funding with two mid-year adjustments: a simulated $15 drop per student against $1,500 under an unweighted formula; English-as-a-second-language instructors rose, "pupil-teacher ratios remained unchanged"; no detected harm to non-migrants | Against dilution where funding is weighted and fast |
| Sabet (2023, SSRN 4592964) | US public schools 1982–2000, county IRCA-applicant share | Enrollment rose more than teaching staff; student-teacher ratios rose significantly | For dilution (class size) |
| Bernini and Sabet (2025, SSRN 5467448) | School districts 1987–97, county IRCA exposure | No change in total spending; current share −0.6 points, capital +0.6; teacher salaries cut; teacher numbers unchanged | For dilution of current spending |
| Coen-Pirani (Carnegie Mellon working paper; *J. Public Econ.* 2011 [TRAINING-DATA]) | California 1970–2000, calibrated voting model | Spending per student would have been 24% higher in 2000 had immigration stayed at its 1970 level | For dilution through state politics (model, no interval) |
| Mayda, Senses and Steingress (2023, CEPR DP 18054) | US counties 1990–2010 | Per capita public spending falls with low-skilled immigrant arrivals and rises with high-skilled ones | For dilution per capita (abstract; magnitudes not recovered) |

[SOURCE: https://wagner.nyu.edu/files/faculty/publications/Mariel%20Boatlift.pdf (read through Exa's
crawl; curl got HTTP 403), `_cache/lit/stclair_mariel_exa.txt`; https://docs.iza.org/dp18339.pdf,
`_cache/lit/iza_dp18339.pdf`; https://doi.org/10.2139/ssrn.4592964; https://doi.org/10.2139/ssrn.5467448;
https://ideas.repec.org/p/cmu/gsiawp/1236867145.html; https://cepr.org/publications/dp18054. The SSRN,
IDEAS and CEPR passages were read as Exa search extracts, not page-verified.]

The two episodes where money was explicitly weighted or the state stepped in show spending keeping
pace or more; the broad panels and the political-economy model point to dilution. This lane's
within-district result sits with the first, its state-level result with the second. Rule 2: the NYC
figure is a formula simulation and Coen-Pirani's a calibrated model; both are graded as model outputs,
not estimates. [INFERENCE]

## 12. Gates

| Gate | Result |
|---|---|
| F-33 national current spending per pupil within 0.5% of Census for two years | **Pass**: FY2015 $11,384 vs $11,392 (−0.07%), FY2019 $13,183 vs $13,187 (−0.03%); also FY2023 +0.12%, FY2024 +0.12%. FY2005 and FY2010 sit 1.2% and 1.0% below, because before FY2015 the file's fall membership counts pupils Table 8 excludes (its FY2010 note names private charter schools, state facilities and federal systems). Table A1. |
| Enrollment panel row counts and district coverage by year | **Pass**: Table A2 (25 fiscal years; 14,077–15,514 rows, 13,038–14,254 regular districts with pupils and spending, 46.4–48.6m pupils), Tables A2b–c (estimation samples by year) |
| Every computed specification in RESULT.md, null ones included | **Pass**: Tables A1–A13 are generated from every derived CSV by `tables.py` |
| JM and earnings-per-SD figures quoted verbatim with page | **Pass**: section 10 |

The convention matches Census Table 8: spending of systems with pupils divided by their fall
membership; including service agencies without pupils ($12.05bn in FY2019) put the first version
0.9–1.9% high. [CALCULATION: `build_panel.py` → `derived/gate_national_pp.csv`]

## 13. What blocked, and what replaced it

- **Census FY2022 all-items text file is a partial upload**: `elsec22.txt` holds 1,729 of 14,105 rows
  (1,061,580 bytes, equal to the server's Content-Length, so the download is faithful). The same
  release's `elsec22.xlsx` is used. [DATA: `acquire.py`, `derived/sources_f33.json`]
- **Urban Institute Education Data API** slowed and then stopped answering (one state's request timed
  out at 120 s). This lane holds complete CCD directory pulls for falls 2000–2002 (teachers and English
  learners for fall 2000); membership for falls 2000/2005/2010/2019 and directories for 2005/2010/2019
  come from the school-flight lane's pull of the same endpoints (2026-09-18); fall 2023 membership from
  the school-cost lane's NCES aggregation; English learners 2018–19 and teachers 2018–19 and 2023–24
  from NCES CCD files. No EL counts for fall 2023, so FY2024 has no EL specification.
- **Shift-share instrument weak** (F ≤ 3.6): reported, not used.
- **Two papers' PDFs refused curl** (NYU Wagner, CEPR, HTTP 403): read through Exa instead, as marked.

## 14. Limits

- Linear, first-order pricing. The account's rule, extrapolated to districts where the group is a
  majority, carries 39% of the central figure; the bounded forms are $9–13bn.
- State-by-year effects remove state-level dilution from the district designs; the state designs are
  correlations.
- JM's effect is per dollar of total spending and is applied to instruction dollars, which is
  conservative if non-instruction dollars are less productive. Dividing a four-year effect by four is
  an assumption; test-score pricing omits attainment effects JM find at least twice as large.
- CFR's 12% per SD is a conditional association in one large district's grades 3–8, earnings at 28,
  held constant over the life cycle as CFR do.
- The composition channel's local-revenue fall is not identified as rate or base; it may also overlap
  the account row, and is marked so.
- Class size holds the pupil-teacher ratio at 16.14 and uses JM's equivalence.
- Group pupils by district are the school-cost lane's modelled weights, not counts; 8.5% of them sit in
  districts without FY2024 F-33 data (mostly independent charters) and take their state's mean.
- Instrument bias: this was produced by an LLM on a politically charged topic
  (`notes/llm-bias-caveat.md`); every number above is reproducible from the scripts.

## 15. Would change it

A credible estimate of the response of state and district spending to immigrant-driven enrollment
specifically (a strong instrument, or a sharp arrival such as a refugee placement program) that moves
the medium-run instruction response above about 0.85 or below 0.5; evidence that JM's per-dollar
effect falls steeply beyond $1,000 per pupil (the majority-group districts); or a finding that the
local revenue fall is rate cuts, which would turn part of it into a taxpayer gain.

## 16. Reproduce

From the repository root, in order (each step writes the ignored `_cache/` or the tracked `derived/`):

```sh
L=infra/immigration-fiscal/school_dilution_2026_09_24
export OPENBLAS_NUM_THREADS=1
uv run --no-project --with pandas --with openpyxl python3 $L/acquire.py
# pull_ccd.py fetched the fall-2000 directory (KINDS=dir YEARS=2000); other CCD falls reuse
# ../school_flight_2026_09_18/_cache/dist and ../school_cost_where_enrolled_2026_09_24/_cache
uv run --no-project --with pandas --with pyarrow --with xlrd --with openpyxl python3 -W ignore $L/build_panel.py
uv run --no-project --with pandas --with pyarrow --with pyfixest python3 -W ignore $L/estimate_functions.py
uv run --no-project --with pandas --with pyarrow --with pyfixest python3 -W ignore $L/estimate_iv.py
uv run --no-project --with pandas python3 $L/decompose.py
uv run --no-project --with pandas --with pyarrow --with pyfixest python3 -W ignore $L/compensatory.py
uv run --no-project --with pandas --with pyarrow --with pyfixest python3 -W ignore $L/class_size.py
uv run --no-project --with pandas --with pyarrow python3 -W ignore $L/price.py
uv run --no-project --with pandas python3 $L/tables.py
```

`price.py` imports the school-cost lane's `weighting.py` read-only. No shared file needs an edit for
this lane; adding the `beside` rows to the account's social total is the parent's and the ledger
lane's call.

Model: claude-opus-5-5[1m] (Opus 5.5, 1M context), lane worker, 2026-09-24/25.

## Appendix: every computed specification

Generated by `tables.py` from `derived/`; do not edit by hand.

<!-- tables:start -->

**Table A1.** Gate: national current spending per pupil, systems with pupils (Census Table 8 convention), dollars.

| fiscal_year | computed_pp | published_pp | rel_diff | pass_0.5pct |
|---|---|---|---|---|
| 2005 | 8,599.87 | 8,701.06 | -0.01163 | False |
| 2010 | 10,492.67 | 10,600.06 | -0.01013 | False |
| 2015 | 11,384.11 | 11,391.79 | -0.00067 | True |
| 2019 | 13,182.92 | 13,187.35 | -0.00034 | True |
| 2023 | 16,545.93 | 16,525.88 | 0.00121 | True |
| 2024 | 17,641.28 | 17,619.39 | 0.00124 | True |

**Table A2.** F-33 panel by fiscal year: rows, districts and pupils (pupils in millions after division; spending in $bn nominal).

| fiscal_year | rows | rows_with_ncesid | regular_districts_with_pupils_and_spending | pupils_all_units | pupils_regular | current_spending_all_units_bn | current_pp_all_units | cpi_fy |
|---|---|---|---|---|---|---|---|---|
| 2000 | 15,514 | 15,328 | 14,254 | 46.433 | 46.306 | 320.51 | 6,779 | 169.292 |
| 2001 | 15,470 | 15,316 | 14,210 | 46.731 | 46.513 | 345.27 | 7,258 | 175.067 |
| 2002 | 15,383 | 15,248 | 14,178 | 47.115 | 46.999 | 364.96 | 7,593 | 178.167 |
| 2003 | 15,361 | 15,265 | 14,142 | 47.603 | 47.488 | 384.88 | 7,925 | 182.092 |
| 2004 | 15,370 | 15,329 | 14,115 | 47.855 | 47.736 | 399.93 | 8,196 | 186.108 |
| 2005 | 15,249 | 15,208 | 14,006 | 48.055 | 47.937 | 421.71 | 8,600 | 191.700 |
| 2006 | 15,188 | 15,150 | 13,945 | 48.301 | 48.180 | 445.77 | 9,043 | 198.942 |
| 2007 | 14,885 | 14,851 | 13,736 | 48.405 | 48.279 | 472.15 | 9,561 | 204.112 |
| 2008 | 14,866 | 14,838 | 13,703 | 48.401 | 48.269 | 500.64 | 10,137 | 211.684 |
| 2009 | 14,633 | 14,604 | 13,495 | 48.259 | 48.127 | 511.11 | 10,381 | 214.649 |
| 2010 | 14,549 | 14,543 | 13,420 | 48.266 | 48.131 | 516.70 | 10,493 | 216.761 |
| 2011 | 14,491 | 14,477 | 13,372 | 48.276 | 48.155 | 518.28 | 10,522 | 221.061 |
| 2012 | 14,482 | 14,468 | 13,370 | 48.214 | 48.064 | 518.16 | 10,550 | 227.554 |
| 2013 | 14,460 | 14,441 | 13,424 | 48.298 | 48.141 | 526.15 | 10,700 | 231.389 |
| 2014 | 14,401 | 14,381 | 13,379 | 48.379 | 48.223 | 541.14 | 10,984 | 234.989 |
| 2015 | 14,376 | 14,362 | 13,329 | 48.514 | 48.353 | 562.09 | 11,384 | 236.670 |
| 2016 | 14,328 | 14,314 | 13,338 | 48.581 | 48.426 | 581.30 | 11,747 | 238.243 |
| 2017 | 14,309 | 14,294 | 13,313 | 48.631 | 48.471 | 603.69 | 12,190 | 242.675 |
| 2018 | 14,274 | 14,259 | 13,183 | 48.596 | 48.414 | 621.19 | 12,553 | 248.131 |
| 2019 | 14,197 | 14,188 | 13,125 | 48.011 | 47.891 | 644.98 | 13,183 | 253.258 |
| 2020 | 14,136 | 14,132 | 13,075 | 48.009 | 47.888 | 660.69 | 13,502 | 257.272 |
| 2021 | 14,120 | 14,117 | 13,058 | 46.425 | 46.310 | 679.54 | 14,379 | 263.151 |
| 2022 | 14,105 | 14,102 | 13,056 | 46.456 | 46.324 | 738.66 | 15,634 | 282.028 |
| 2023 | 14,088 | 14,085 | 13,041 | 46.576 | 46.431 | 783.58 | 16,546 | 299.656 |
| 2024 | 14,077 | 14,075 | 13,038 | 46.372 | 46.222 | 832.30 | 17,641 | 309.567 |

**Table A2b.** Estimation sample FY2000-2019 by year (districts passing the spending band, size and spell rules; pupils in millions).

| year | districts | pupils_m |
|---|---|---|
| 2000 | 12,991 | 46.192 |
| 2001 | 13,018 | 46.414 |
| 2002 | 13,067 | 46.943 |
| 2003 | 13,040 | 47.431 |
| 2004 | 13,024 | 47.632 |
| 2005 | 12,935 | 47.880 |
| 2006 | 12,883 | 48.094 |
| 2007 | 12,840 | 48.188 |
| 2008 | 12,824 | 48.207 |
| 2009 | 12,636 | 48.071 |
| 2010 | 12,611 | 48.074 |
| 2011 | 12,432 | 47.952 |
| 2012 | 12,528 | 47.976 |
| 2013 | 12,525 | 48.053 |
| 2014 | 12,479 | 48.137 |
| 2015 | 12,497 | 48.278 |
| 2016 | 12,485 | 48.347 |
| 2017 | 12,487 | 48.408 |
| 2018 | 12,317 | 48.250 |
| 2019 | 12,216 | 47.720 |

**Table A2c.** Estimation sample FY2000-2024 by year (districts passing the spending band, size and spell rules; pupils in millions).

| year | districts | pupils_m |
|---|---|---|
| 2000 | 12,994 | 46.192 |
| 2001 | 13,021 | 46.414 |
| 2002 | 13,068 | 46.943 |
| 2003 | 13,040 | 47.431 |
| 2004 | 13,025 | 47.632 |
| 2005 | 12,936 | 47.880 |
| 2006 | 12,884 | 48.094 |
| 2007 | 12,840 | 48.188 |
| 2008 | 12,824 | 48.207 |
| 2009 | 12,636 | 48.071 |
| 2010 | 12,611 | 48.074 |
| 2011 | 12,432 | 47.952 |
| 2012 | 12,528 | 47.976 |
| 2013 | 12,525 | 48.053 |
| 2014 | 12,480 | 48.138 |
| 2015 | 12,499 | 48.278 |
| 2016 | 12,489 | 48.355 |
| 2017 | 12,491 | 48.408 |
| 2018 | 12,397 | 48.302 |
| 2019 | 12,363 | 47.840 |
| 2020 | 12,333 | 47.838 |
| 2021 | 12,301 | 46.244 |
| 2022 | 12,300 | 46.258 |
| 2023 | 12,284 | 46.366 |
| 2024 | 12,248 | 46.111 |

**Table A3a.** Response of spending to pupils by function: elasticity for log and difference designs, marginal over average cost for `fe_level`, 1 + coefficient for the CBO-style per-pupil designs (`x`, `up`, `down` at state level); SE in parentheses.

| spec | weight | term | obs | current | instruction | instr_support | pupil_support | instr_staff | administration | gen_admin | school_admin | business |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fe_log_fy2000_2019 | unweighted | lnN | 253,795 | 0.682 (0.027) | 0.744 (0.029) | 0.734 (0.049) | 0.758 (0.050) | 0.748 (0.059) | 0.541 (0.024) | 0.377 (0.023) | 0.694 (0.029) | 0.487 (0.031) |
| fe_log_fy2000_2019 | pupils | lnN | 253,795 | 0.830 (0.022) | 0.890 (0.027) | 0.804 (0.049) | 0.848 (0.039) | 0.750 (0.066) | 0.729 (0.026) | 0.475 (0.048) | 0.848 (0.034) | 0.666 (0.038) |
| fe_level_fy2000_2019 | unweighted | x | 253,795 | 0.606 (0.020) | 0.655 (0.023) | 0.569 (0.027) | 0.552 (0.030) | 0.592 (0.043) | 0.500 (0.044) | 0.319 (0.043) | 0.612 (0.029) | 0.521 (0.120) |
| fe_level_fy2000_2019 | pupils | x | 253,795 | 0.734 (0.022) | 0.768 (0.028) | 0.674 (0.031) | 0.704 (0.031) | 0.640 (0.054) | 0.702 (0.053) | 0.399 (0.059) | 0.796 (0.049) | 0.712 (0.100) |
| fd_fy2000_2019 | unweighted | dlnN | 239,192 | 0.270 (0.029) | 0.297 (0.032) | 0.260 (0.034) | 0.277 (0.034) | 0.250 (0.040) | 0.195 (0.029) | 0.128 (0.031) | 0.259 (0.027) | 0.192 (0.038) |
| fd_asym_fy2000_2019 | unweighted | up | 239,192 | 0.344 (0.042) | 0.362 (0.043) | 0.351 (0.067) | 0.363 (0.067) | 0.315 (0.071) | 0.273 (0.040) | 0.227 (0.075) | 0.292 (0.035) | 0.300 (0.041) |
| fd_asym_fy2000_2019 | unweighted | down | 239,192 | 0.200 (0.017) | 0.237 (0.022) | 0.175 (0.029) | 0.198 (0.022) | 0.190 (0.039) | 0.123 (0.020) | 0.036 (0.025) | 0.229 (0.027) | 0.090 (0.045) |
| fd_fy2000_2019 | pupils | dlnN | 239,192 | 0.449 (0.034) | 0.481 (0.037) | 0.399 (0.044) | 0.415 (0.037) | 0.374 (0.055) | 0.392 (0.034) | 0.293 (0.024) | 0.444 (0.040) | 0.352 (0.046) |
| fd_asym_fy2000_2019 | pupils | up | 239,192 | 0.566 (0.053) | 0.600 (0.056) | 0.537 (0.068) | 0.577 (0.064) | 0.471 (0.083) | 0.490 (0.052) | 0.361 (0.058) | 0.520 (0.060) | 0.513 (0.070) |
| fd_asym_fy2000_2019 | pupils | down | 239,192 | 0.338 (0.030) | 0.369 (0.041) | 0.269 (0.044) | 0.264 (0.045) | 0.282 (0.056) | 0.299 (0.045) | 0.229 (0.068) | 0.372 (0.055) | 0.201 (0.075) |
| dl3_fy2000_2019 | unweighted | cumulative_3yr | 210,814 | 0.529 (0.031) | 0.581 (0.032) | 0.553 (0.053) | 0.579 (0.055) | 0.507 (0.060) | 0.427 (0.028) | 0.296 (0.020) | 0.575 (0.030) | 0.381 (0.029) |
| dl3_fy2000_2019 | pupils | cumulative_3yr | 210,814 | 0.700 (0.032) | 0.749 (0.037) | 0.669 (0.055) | 0.731 (0.039) | 0.607 (0.070) | 0.631 (0.035) | 0.440 (0.033) | 0.743 (0.037) | 0.555 (0.047) |
| ld_stacked_fy2000_2019 | unweighted | dlnN | 49,395 | 0.585 (0.032) | 0.636 (0.033) | 0.621 (0.055) | 0.621 (0.044) | 0.617 (0.059) | 0.463 (0.029) | 0.326 (0.027) | 0.587 (0.029) | 0.432 (0.034) |
| ld_stacked_fy2000_2019 | pupils | dlnN | 49,395 | 0.758 (0.027) | 0.807 (0.032) | 0.713 (0.040) | 0.746 (0.045) | 0.666 (0.052) | 0.652 (0.025) | 0.389 (0.058) | 0.758 (0.033) | 0.625 (0.031) |
| ld19_2000_2019 | unweighted | dlnN | 11,726 | 0.797 (0.023) | 0.861 (0.024) | 0.879 (0.048) | 0.894 (0.039) | 0.923 (0.079) | 0.655 (0.025) | 0.464 (0.035) | 0.801 (0.024) | 0.605 (0.042) |
| ld19_2000_2019 | pupils | dlnN | 11,726 | 0.869 (0.024) | 0.924 (0.032) | 0.878 (0.038) | 0.901 (0.036) | 0.846 (0.051) | 0.774 (0.027) | 0.543 (0.056) | 0.871 (0.029) | 0.708 (0.051) |
| state_ld_2000_2019 | unweighted | dlnN | 51 | 0.488 (0.132) | 0.418 (0.151) | 0.693 (0.361) | 0.237 (0.252) | 1.200 (0.467) | 0.137 (0.228) | -0.024 (0.425) | 0.342 (0.215) | 0.111 (0.442) |
| state_ld_2000_2019 | pupils | dlnN | 51 | 0.373 (0.243) | 0.339 (0.257) | 0.245 (0.353) | -0.001 (0.394) | 0.573 (0.375) | 0.361 (0.315) | 0.027 (0.638) | 0.392 (0.318) | 0.490 (0.375) |
| state_cbo_2019 | unweighted | x | 969 | 0.707 (0.157) | 0.902 (0.260) | 0.204 (0.187) | -0.249 (0.388) | 0.710 (0.149) | 0.432 (0.099) | 0.369 (0.202) | 0.087 (0.306) | 0.895 (0.310) |
| state_cbo_asym_2019 | unweighted | up | 969 | 0.453 (0.235) | 0.339 (0.398) | 1.132 (0.411) | 1.514 (0.697) | 0.750 (0.475) | 0.606 (0.181) | 0.013 (0.474) | 0.879 (0.259) | 1.387 (1.115) |
| state_cbo_asym_2019 | unweighted | down | 969 | 0.813 (0.262) | 1.139 (0.429) | -0.187 (0.262) | -0.992 (0.569) | 0.693 (0.185) | 0.358 (0.145) | 0.519 (0.311) | -0.247 (0.393) | 0.687 (0.214) |
| state_cbo_2019 | pupils | x | 969 | 0.349 (0.174) | 0.335 (0.228) | 0.362 (0.170) | 0.254 (0.149) | 0.553 (0.285) | 0.543 (0.106) | -0.601 (1.024) | 0.419 (0.124) | 0.783 (0.332) |
| state_cbo_asym_2019 | pupils | up | 969 | 0.989 (0.218) | 1.118 (0.257) | 1.255 (0.512) | 1.064 (0.354) | 1.440 (0.948) | 0.860 (0.376) | 1.251 (0.987) | 0.954 (0.335) | 0.541 (0.473) |
| state_cbo_asym_2019 | pupils | down | 969 | 0.083 (0.202) | 0.010 (0.259) | -0.008 (0.208) | -0.082 (0.241) | 0.184 (0.298) | 0.411 (0.172) | -1.371 (1.571) | 0.197 (0.186) | 0.884 (0.357) |
| fe_log_fy2000_2024 | unweighted | lnN | 315,499 | 0.690 (0.024) | 0.755 (0.026) | 0.735 (0.045) | 0.757 (0.043) | 0.744 (0.059) | 0.553 (0.023) | 0.392 (0.022) | 0.690 (0.026) | 0.508 (0.032) |
| fe_log_fy2000_2024 | pupils | lnN | 315,499 | 0.816 (0.022) | 0.880 (0.026) | 0.803 (0.038) | 0.826 (0.030) | 0.767 (0.051) | 0.711 (0.025) | 0.494 (0.041) | 0.814 (0.030) | 0.657 (0.036) |
| fe_level_fy2000_2024 | unweighted | x | 315,499 | 0.604 (0.016) | 0.660 (0.020) | 0.569 (0.024) | 0.561 (0.029) | 0.581 (0.038) | 0.483 (0.031) | 0.309 (0.037) | 0.604 (0.029) | 0.481 (0.074) |
| fe_level_fy2000_2024 | pupils | x | 315,499 | 0.709 (0.020) | 0.747 (0.025) | 0.657 (0.030) | 0.662 (0.031) | 0.651 (0.045) | 0.661 (0.043) | 0.392 (0.054) | 0.747 (0.044) | 0.665 (0.076) |
| fd_fy2000_2024 | unweighted | dlnN | 300,449 | 0.263 (0.027) | 0.293 (0.029) | 0.255 (0.033) | 0.276 (0.033) | 0.233 (0.040) | 0.183 (0.025) | 0.117 (0.028) | 0.242 (0.023) | 0.185 (0.032) |
| fd_asym_fy2000_2024 | unweighted | up | 300,449 | 0.336 (0.038) | 0.359 (0.039) | 0.332 (0.062) | 0.360 (0.067) | 0.278 (0.062) | 0.256 (0.034) | 0.203 (0.065) | 0.283 (0.031) | 0.295 (0.034) |
| fd_asym_fy2000_2024 | unweighted | down | 300,449 | 0.196 (0.016) | 0.233 (0.021) | 0.185 (0.026) | 0.200 (0.023) | 0.192 (0.038) | 0.116 (0.017) | 0.038 (0.022) | 0.204 (0.024) | 0.083 (0.040) |
| fd_fy2000_2024 | pupils | dlnN | 300,449 | 0.427 (0.033) | 0.469 (0.036) | 0.359 (0.043) | 0.375 (0.041) | 0.325 (0.052) | 0.351 (0.034) | 0.258 (0.024) | 0.404 (0.038) | 0.325 (0.040) |
| fd_asym_fy2000_2024 | pupils | up | 300,449 | 0.559 (0.053) | 0.599 (0.056) | 0.527 (0.065) | 0.572 (0.065) | 0.446 (0.079) | 0.459 (0.044) | 0.322 (0.058) | 0.497 (0.058) | 0.475 (0.057) |
| fd_asym_fy2000_2024 | pupils | down | 300,449 | 0.305 (0.028) | 0.349 (0.037) | 0.204 (0.048) | 0.195 (0.057) | 0.214 (0.060) | 0.251 (0.043) | 0.200 (0.060) | 0.319 (0.052) | 0.186 (0.063) |
| dl3_fy2000_2024 | unweighted | cumulative_3yr | 271,305 | 0.509 (0.030) | 0.566 (0.032) | 0.535 (0.051) | 0.571 (0.053) | 0.472 (0.056) | 0.399 (0.026) | 0.279 (0.019) | 0.536 (0.029) | 0.369 (0.027) |
| dl3_fy2000_2024 | pupils | cumulative_3yr | 271,305 | 0.657 (0.034) | 0.715 (0.037) | 0.616 (0.047) | 0.696 (0.038) | 0.532 (0.061) | 0.564 (0.034) | 0.357 (0.046) | 0.681 (0.031) | 0.492 (0.052) |
| state_ld_2000_2024 | unweighted | dlnN | 51 | 0.563 (0.126) | 0.533 (0.163) | 0.692 (0.289) | 0.471 (0.276) | 0.982 (0.331) | 0.275 (0.201) | 0.144 (0.378) | 0.492 (0.245) | 0.030 (0.401) |
| state_ld_2000_2024 | pupils | dlnN | 51 | 0.390 (0.206) | 0.390 (0.222) | 0.205 (0.381) | 0.047 (0.479) | 0.432 (0.335) | 0.288 (0.280) | -0.220 (0.746) | 0.396 (0.295) | 0.386 (0.326) |
| state_cbo_2024 | unweighted | x | 1,224 | 0.597 (0.172) | 0.753 (0.265) | 0.250 (0.150) | -0.232 (0.324) | 0.759 (0.148) | 0.352 (0.065) | 0.278 (0.186) | 0.095 (0.204) | 0.740 (0.282) |
| state_cbo_asym_2024 | unweighted | up | 1,224 | 0.260 (0.205) | 0.126 (0.339) | 1.034 (0.351) | 1.125 (0.573) | 0.940 (0.388) | 0.379 (0.155) | -0.128 (0.473) | 0.680 (0.326) | 0.978 (0.760) |
| state_cbo_asym_2024 | unweighted | down | 1,224 | 0.763 (0.280) | 1.062 (0.439) | -0.138 (0.226) | -0.903 (0.528) | 0.669 (0.220) | 0.339 (0.112) | 0.479 (0.298) | -0.194 (0.347) | 0.623 (0.209) |
| state_cbo_2024 | pupils | x | 1,224 | 0.271 (0.147) | 0.237 (0.192) | 0.359 (0.158) | 0.169 (0.137) | 0.619 (0.245) | 0.446 (0.094) | -0.431 (0.872) | 0.310 (0.107) | 0.668 (0.354) |
| state_cbo_asym_2024 | pupils | up | 1,224 | 0.682 (0.191) | 0.747 (0.229) | 1.109 (0.409) | 0.789 (0.297) | 1.420 (0.730) | 0.603 (0.286) | 1.061 (0.816) | 0.649 (0.269) | 0.428 (0.368) |
| state_cbo_asym_2024 | pupils | down | 1,224 | 0.074 (0.200) | -0.008 (0.250) | -0.002 (0.209) | -0.128 (0.232) | 0.235 (0.276) | 0.371 (0.150) | -1.146 (1.440) | 0.148 (0.188) | 0.783 (0.438) |

**Table A3b.** Response of spending to pupils by function: elasticity for log and difference designs, marginal over average cost for `fe_level`, 1 + coefficient for the CBO-style per-pupil designs (`x`, `up`, `down` at state level); SE in parentheses.

| spec | weight | term | obs | om | transport | other_elsec | support_other | support_total | capital_outlay | interest | net_federal |
|---|---|---|---|---|---|---|---|---|---|---|---|
| fe_log_fy2000_2019 | unweighted | lnN | 253,795 | 0.565 (0.031) | 0.596 (0.031) | 0.713 (0.022) | 0.738 (0.066) | 0.585 (0.027) | 0.600 (0.080) | 0.968 (0.095) |  |
| fe_log_fy2000_2019 | pupils | lnN | 253,795 | 0.733 (0.019) | 0.709 (0.024) | 0.791 (0.033) | 0.748 (0.056) | 0.747 (0.021) | 0.438 (0.083) | 0.574 (0.142) |  |
| fe_level_fy2000_2019 | unweighted | x | 253,795 | 0.482 (0.029) | 0.469 (0.036) | 0.677 (0.029) | 1.827 (1.376) | 0.512 (0.023) | 0.570 (0.172) | 1.067 (0.205) |  |
| fe_level_fy2000_2019 | pupils | x | 253,795 | 0.680 (0.035) | 0.637 (0.058) | 0.709 (0.038) | -1.118 (1.368) | 0.676 (0.027) | 0.373 (0.145) | 0.743 (0.323) |  |
| fd_fy2000_2019 | unweighted | dlnN | 239,192 | 0.203 (0.029) | 0.244 (0.029) | 0.380 (0.033) | 0.449 (0.109) | 0.212 (0.027) | 0.073 (0.110) | 0.344 (0.043) |  |
| fd_asym_fy2000_2019 | unweighted | up | 239,192 | 0.315 (0.049) | 0.311 (0.035) | 0.431 (0.051) | 0.589 (0.172) | 0.301 (0.043) | 0.078 (0.140) | 0.248 (0.077) |  |
| fd_asym_fy2000_2019 | unweighted | down | 239,192 | 0.098 (0.016) | 0.182 (0.034) | 0.334 (0.030) | 0.295 (0.088) | 0.129 (0.014) | 0.069 (0.116) | 0.435 (0.056) |  |
| fd_fy2000_2019 | pupils | dlnN | 239,192 | 0.397 (0.035) | 0.382 (0.047) | 0.486 (0.035) | 0.757 (0.042) | 0.393 (0.032) | 0.046 (0.118) | 0.267 (0.094) |  |
| fd_asym_fy2000_2019 | pupils | up | 239,192 | 0.507 (0.048) | 0.521 (0.062) | 0.599 (0.056) | 0.714 (0.053) | 0.503 (0.052) | 0.161 (0.164) | 0.393 (0.128) |  |
| fd_asym_fy2000_2019 | pupils | down | 239,192 | 0.293 (0.044) | 0.252 (0.035) | 0.380 (0.025) | 0.841 (0.222) | 0.289 (0.027) | -0.064 (0.153) | 0.145 (0.129) |  |
| dl3_fy2000_2019 | unweighted | cumulative_3yr | 210,814 | 0.422 (0.038) | 0.465 (0.033) | 0.585 (0.026) | 0.679 (0.124) | 0.443 (0.032) | 0.163 (0.144) | 0.748 (0.086) |  |
| dl3_fy2000_2019 | pupils | cumulative_3yr | 210,814 | 0.595 (0.032) | 0.645 (0.033) | 0.720 (0.033) | 0.797 (0.053) | 0.625 (0.033) | 0.066 (0.169) | 0.745 (0.119) |  |
| ld_stacked_fy2000_2019 | unweighted | dlnN | 49,395 | 0.474 (0.038) | 0.535 (0.038) | 0.631 (0.035) | 0.693 (0.064) | 0.501 (0.032) | 0.574 (0.123) | 0.897 (0.082) |  |
| ld_stacked_fy2000_2019 | pupils | dlnN | 49,395 | 0.690 (0.034) | 0.676 (0.044) | 0.789 (0.058) | 0.798 (0.019) | 0.682 (0.024) | 0.543 (0.141) | 0.569 (0.140) |  |
| ld19_2000_2019 | unweighted | dlnN | 11,726 | 0.645 (0.030) | 0.742 (0.029) | 0.784 (0.024) | 0.745 (0.061) | 0.704 (0.026) | 0.835 (0.083) | 0.977 (0.091) |  |
| ld19_2000_2019 | pupils | dlnN | 11,726 | 0.752 (0.025) | 0.780 (0.024) | 0.790 (0.023) | 0.775 (0.061) | 0.795 (0.021) | 0.750 (0.154) | 0.328 (0.166) |  |
| state_ld_2000_2019 | unweighted | dlnN | 51 | 0.794 (0.294) | 0.479 (0.147) | 0.562 (0.195) | -26.559 (2.244) | 0.529 (0.211) | 0.049 (0.571) | 0.463 (0.474) | 0.382 (0.142) |
| state_ld_2000_2019 | pupils | dlnN | 51 | 0.508 (0.352) | 0.493 (0.221) | 0.608 (0.126) | -28.721 (3.199) | 0.419 (0.263) | 0.542 (0.465) | 0.071 (0.880) | 0.296 (0.267) |
| state_cbo_2019 | unweighted | x | 969 | 0.090 (0.180) | 8.767 (5.258) | 0.495 (0.118) | -10.524 (5.209) | 0.490 (0.071) | 2.404 (0.578) | 1.123 (0.283) | 0.788 (0.128) |
| state_cbo_asym_2019 | unweighted | up | 969 | 0.088 (0.435) | -6.157 (4.520) | 0.300 (0.261) | 17.185 (15.909) | 0.515 (0.143) | 1.313 (1.662) | 1.787 (0.621) | 0.463 (0.254) |
| state_cbo_asym_2019 | unweighted | down | 969 | 0.091 (0.151) | 15.056 (7.053) | 0.577 (0.110) | -36.509 (19.778) | 0.479 (0.116) | 2.864 (1.167) | 0.649 (0.398) | 0.926 (0.208) |
| state_cbo_2019 | pupils | x | 969 | 0.342 (0.171) | 1.361 (0.895) | 0.403 (0.122) | -6.486 (7.211) | 0.363 (0.111) | 1.434 (0.477) | 0.751 (0.433) | 0.453 (0.241) |
| state_cbo_asym_2019 | pupils | up | 969 | 0.582 (0.345) | 0.441 (0.625) | 0.727 (0.202) | 2.723 (15.472) | 0.785 (0.218) | 3.248 (0.994) | 1.920 (1.076) | 1.011 (0.243) |
| state_cbo_asym_2019 | pupils | down | 969 | 0.242 (0.224) | 1.743 (1.541) | 0.268 (0.153) | -32.816 (21.018) | 0.188 (0.139) | 0.680 (0.542) | 0.247 (0.584) | 0.221 (0.326) |
| fe_log_fy2000_2024 | unweighted | lnN | 315,499 | 0.547 (0.028) | 0.624 (0.032) | 0.694 (0.019) | 0.732 (0.079) | 0.592 (0.024) | 0.570 (0.079) | 0.952 (0.098) |  |
| fe_log_fy2000_2024 | pupils | lnN | 315,499 | 0.696 (0.020) | 0.705 (0.020) | 0.768 (0.028) | 0.684 (0.063) | 0.728 (0.020) | 0.485 (0.066) | 0.613 (0.127) |  |
| fe_level_fy2000_2024 | unweighted | x | 315,499 | 0.461 (0.026) | 0.501 (0.038) | 0.654 (0.030) | 1.655 (1.230) | 0.504 (0.018) | 0.792 (0.272) | 1.077 (0.266) |  |
| fe_level_fy2000_2024 | pupils | x | 315,499 | 0.637 (0.030) | 0.613 (0.056) | 0.692 (0.030) | -1.144 (1.390) | 0.644 (0.026) | 0.761 (0.316) | 0.816 (0.385) |  |
| fd_fy2000_2024 | unweighted | dlnN | 300,449 | 0.183 (0.025) | 0.231 (0.027) | 0.378 (0.032) | 0.469 (0.111) | 0.200 (0.024) | 0.027 (0.103) | 0.328 (0.047) |  |
| fd_asym_fy2000_2024 | unweighted | up | 300,449 | 0.289 (0.043) | 0.279 (0.032) | 0.416 (0.049) | 0.574 (0.146) | 0.281 (0.038) | 0.091 (0.143) | 0.212 (0.085) |  |
| fd_asym_fy2000_2024 | unweighted | down | 300,449 | 0.086 (0.014) | 0.188 (0.032) | 0.344 (0.030) | 0.354 (0.115) | 0.125 (0.013) | -0.033 (0.099) | 0.435 (0.054) |  |
| fd_fy2000_2024 | pupils | dlnN | 300,449 | 0.344 (0.037) | 0.330 (0.049) | 0.500 (0.043) | 0.685 (0.041) | 0.350 (0.032) | 0.008 (0.136) | 0.302 (0.093) |  |
| fd_asym_fy2000_2024 | pupils | up | 300,449 | 0.485 (0.049) | 0.471 (0.066) | 0.550 (0.052) | 0.620 (0.059) | 0.482 (0.049) | 0.268 (0.204) | 0.349 (0.145) |  |
| fd_asym_fy2000_2024 | pupils | down | 300,449 | 0.214 (0.047) | 0.202 (0.046) | 0.454 (0.053) | 0.807 (0.205) | 0.228 (0.028) | -0.232 (0.150) | 0.258 (0.134) |  |
| dl3_fy2000_2024 | unweighted | cumulative_3yr | 271,305 | 0.392 (0.036) | 0.428 (0.031) | 0.565 (0.027) | 0.672 (0.108) | 0.419 (0.030) | 0.066 (0.135) | 0.725 (0.086) |  |
| dl3_fy2000_2024 | pupils | cumulative_3yr | 271,305 | 0.539 (0.032) | 0.571 (0.044) | 0.674 (0.041) | 0.735 (0.047) | 0.568 (0.033) | 0.044 (0.171) | 0.735 (0.113) |  |
| state_ld_2000_2024 | unweighted | dlnN | 51 | 0.817 (0.287) | 0.573 (0.175) | 0.547 (0.181) | -27.554 (3.510) | 0.571 (0.174) | 0.025 (0.400) | 0.754 (0.425) | 0.513 (0.154) |
| state_ld_2000_2024 | pupils | dlnN | 51 | 0.524 (0.313) | 0.499 (0.228) | 0.494 (0.185) | -28.845 (3.078) | 0.397 (0.235) | 0.490 (0.310) | 0.374 (1.034) | 0.335 (0.227) |
| state_cbo_2024 | unweighted | x | 1,224 | -0.025 (0.170) | 7.474 (4.673) | 0.400 (0.102) | 3.270 (12.559) | 0.414 (0.099) | 1.913 (0.545) | 0.470 (0.290) | 0.649 (0.142) |
| state_cbo_asym_2024 | unweighted | up | 1,224 | -0.148 (0.414) | -5.497 (4.079) | 0.251 (0.336) | 34.089 (20.595) | 0.344 (0.145) | 1.167 (1.500) | 0.392 (0.658) | 0.152 (0.238) |
| state_cbo_asym_2024 | unweighted | down | 1,224 | 0.035 (0.124) | 13.880 (6.850) | 0.473 (0.127) | -40.402 (13.828) | 0.448 (0.144) | 2.281 (1.236) | 0.531 (0.466) | 0.894 (0.224) |
| state_cbo_2024 | pupils | x | 1,224 | 0.232 (0.210) | 1.105 (0.785) | 0.432 (0.115) | 22.985 (21.228) | 0.294 (0.102) | 1.219 (0.388) | 0.236 (0.561) | 0.295 (0.224) |
| state_cbo_asym_2024 | pupils | up | 1,224 | 0.222 (0.380) | 0.192 (0.548) | 0.658 (0.265) | 37.454 (28.919) | 0.545 (0.194) | 2.771 (0.841) | 0.319 (1.052) | 0.557 (0.252) |
| state_cbo_asym_2024 | pupils | down | 1,224 | 0.237 (0.211) | 1.543 (1.447) | 0.324 (0.146) | -28.481 (21.095) | 0.174 (0.147) | 0.474 (0.482) | 0.195 (0.707) | 0.170 (0.360) |

**Table A4a.** Split of the non-response of current spending, pupil-weighted district designs FY2000-2019 (shares of the sum of parts).

| spec | horizon | current_response | nonresponse_total | nonresponse_sum_of_parts | additivity_gap | instruction_response | dilution_share_of_parts | dilution_broad_share_of_parts | scale_share_of_parts |
|---|---|---|---|---|---|---|---|---|---|
| fd_fy2000_2019 | 1 year | 0.449 | 0.551 | 0.549 | 0.003 | 0.481 | 0.584 | 0.691 | 0.309 |
| dl3_fy2000_2019 | 3 years | 0.700 | 0.300 | 0.291 | 0.010 | 0.749 | 0.533 | 0.642 | 0.358 |
| ld_stacked_fy2000_2019 | 4-5 years | 0.758 | 0.242 | 0.236 | 0.006 | 0.807 | 0.505 | 0.624 | 0.376 |
| ld19_2000_2019 | 19 years | 0.869 | 0.131 | 0.126 | 0.006 | 0.924 | 0.374 | 0.471 | 0.529 |
| fe_log_fy2000_2019 | within-district, all horizons | 0.830 | 0.170 | 0.163 | 0.008 | 0.890 | 0.419 | 0.537 | 0.463 |
| fe_level_fy2000_2019 | within-district, all horizons (additive) | 0.734 | 0.266 | 0.266 | 0.000 | 0.768 | 0.539 | 0.658 | 0.342 |

**Table A4b.** Each function's share of the non-response (capital outlay and interest: their own response, outside current spending).

| spec | instruction | pupil_support | instr_staff | gen_admin | school_admin | business | om | transport | other_elsec | support_other | capital_outlay | interest |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fd_fy2000_2019 | 0.582 | 0.055 | 0.051 | 0.023 | 0.056 | 0.038 | 0.104 | 0.047 | 0.038 | 0.000 | resp 0.046 | resp 0.267 |
| dl3_fy2000_2019 | 0.516 | 0.047 | 0.059 | 0.034 | 0.047 | 0.048 | 0.128 | 0.050 | 0.038 | 0.001 | resp 0.066 | resp 0.745 |
| ld_stacked_fy2000_2019 | 0.493 | 0.055 | 0.062 | 0.046 | 0.055 | 0.050 | 0.122 | 0.057 | 0.036 | 0.001 | resp 0.543 | resp 0.569 |
| ld19_2000_2019 | 0.359 | 0.039 | 0.053 | 0.063 | 0.055 | 0.072 | 0.179 | 0.071 | 0.066 | 0.001 | resp 0.750 | resp 0.328 |
| fe_log_fy2000_2019 | 0.400 | 0.047 | 0.066 | 0.056 | 0.050 | 0.064 | 0.149 | 0.072 | 0.051 | 0.001 | resp 0.438 | resp 0.574 |
| fe_level_fy2000_2019 | 0.539 | 0.058 | 0.061 | 0.041 | 0.043 | 0.035 | 0.114 | 0.058 | 0.045 | 0.006 | resp 0.373 | resp 0.743 |

**Table A5a.** Shift-share first stage (fall-2000 Hispanic share x national group growth); F is the clustered Wald F. Weak in every specification; not used.

| weight | first_stage_coef | se | F_cluster | n_obs | districts | mean_h0_pupil_weighted | spec | strong_F_ge_10 |
|---|---|---|---|---|---|---|---|---|
| unweighted | 0.233 | 0.124 | 3.550 | 234204 | 13009 | 0.166 | fe_fy2001_2019 | False |
| pupils | -0.144 | 0.135 | 1.143 | 234204 | 13009 | 0.166 | fe_fy2001_2019 | False |
| unweighted | 0.184 | 0.139 | 1.744 | 11734 | 11736 |  | long_difference_fy2001_2019 | False |
| pupils | -0.149 | 0.116 | 1.671 | 11734 | 11736 |  | long_difference_fy2001_2019 | False |

**Table A5b.** 2SLS elasticities on the weak instrument, shown because computed; not used.

| spec | weight | current | instruction | instr_support | pupil_support | instr_staff | administration | om | capital_outlay |
|---|---|---|---|---|---|---|---|---|---|
| iv_shiftshare_fe_fy2001_2019 | unweighted | 0.984 (0.229) | 0.898 (0.256) | 1.500 (0.589) | 1.133 (0.565) | 2.242 (0.944) | 0.830 (0.201) | 0.986 (0.331) | 2.487 (1.027) |
| iv_shiftshare_fe_fy2001_2019 | pupils | 0.395 (0.753) | 0.378 (0.912) | 3.260 (2.923) | 3.488 (3.170) | 2.317 (2.108) | 0.889 (0.909) | -0.422 (1.451) | -2.079 (3.719) |
| iv_shiftshare_ld_fy2001_2019 | unweighted | 1.160 (0.327) | 1.046 (0.290) | 1.700 (0.855) | 0.838 (0.598) | 3.091 (1.839) | 0.885 (0.287) | 0.917 (0.402) | 2.249 (1.271) |
| iv_shiftshare_ld_fy2001_2019 | pupils | 0.118 (0.874) | 0.273 (0.926) | 0.674 (0.546) | 2.505 (1.669) | -1.577 (2.348) | 0.039 (0.921) | 0.047 (0.748) | -1.178 (1.655) |

**Table A6a.** Compensatory-funding waves: districts, pupils (m), pupil-weighted Hispanic share and covariate coverage.

| fall | fy | districts | pupils_m | hisp_share_pw | el_covered_pupil_share | pov_covered_pupil_share |
|---|---|---|---|---|---|---|
| 2000 | 2001 | 13096 | 46.456 | 0.162 | 0.826 | 0.000 |
| 2005 | 2006 | 12904 | 48.130 | 0.197 | 0.894 | 0.997 |
| 2010 | 2011 | 12547 | 48.011 | 0.231 | 0.874 | 0.999 |
| 2019 | 2020 | 12334 | 47.783 | 0.273 | 0.974 | 0.998 |
| 2023 | 2024 | 12274 | 46.113 | 0.290 | 0.000 | 0.998 |

**Table A6b.** Compensatory funding, revenue outcomes: dollars per pupil (2024) per unit share (log-total specs: elasticities); state fixed effects in cross-sections, district and state-year effects in panels; SE clustered by state.

| design | fy | spec | term | districts | rev_total | rev_state | rev_local | rev_federal | title1 | fed_bilingual | state_comp | state_bilingual | state_formula | idea |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cross_section | 2020 | hisp | hisp_share | 12,332 | 1,806 (422) | 6,445 (1,343) | -6,134 (1,577) | 1,496 (189) | 520 (48) | 26 (7) | 160 (81) | 86 (44) | 5,755 (1,248) | 50 (16) |
| cross_section | 2020 | hisp_pov | hisp_share | 12,206 | 439 (656) | 2,466 (1,210) | -1,962 (1,447) | -64 (167) | -76 (42) | 27 (7) | -79 (86) | 100 (47) | 2,577 (1,155) | -6 (27) |
| cross_section | 2020 | hisp_pov | pov_rate | 12,206 | 6,587 (2,116) | 19,428 (3,679) | -20,478 (3,306) | 7,636 (462) | 2,916 (195) | -1 (6) | 1,172 (401) | -69 (37) | 15,509 (3,044) | 274 (65) |
| cross_section | 2020 | el_pov | el_share | 10,019 | 3,797 (1,780) | 743 (1,584) | 2,455 (1,510) | 599 (277) | -50 (85) | 85 (23) | -24 (161) | 254 (126) | 362 (1,329) | 11 (40) |
| cross_section | 2020 | el_pov | pov_rate | 10,019 | 5,316 (1,967) | 21,535 (3,705) | -23,490 (3,536) | 7,271 (340) | 2,864 (198) | -8 (5) | 1,109 (390) | -74 (40) | 17,892 (3,147) | 265 (58) |
| cross_section | 2020 | el_hisp_pov | hisp_share | 10,019 | -1,098 (1,161) | 3,751 (1,383) | -4,491 (2,117) | -359 (329) | -99 (39) | 2 (5) | -118 (94) | 42 (24) | 4,079 (1,299) | -16 (28) |
| cross_section | 2020 | el_hisp_pov | el_share | 10,019 | 5,218 (2,977) | -4,110 (1,070) | 8,265 (2,962) | 1,063 (654) | 79 (84) | 82 (28) | 129 (181) | 200 (109) | -4,915 (735) | 32 (19) |
| cross_section | 2020 | el_hisp_pov | pov_rate | 10,019 | 5,820 (2,059) | 19,814 (3,629) | -21,429 (3,310) | 7,435 (421) | 2,910 (201) | -9 (5) | 1,163 (402) | -93 (43) | 16,021 (2,989) | 272 (67) |
| cross_section | 2024 | hisp | hisp_share | 12,253 | 4,737 (874) | 7,474 (1,910) | -5,601 (1,598) | 2,863 (269) | 506 (58) | 37 (4) | 195 (100) | 103 (52) | 6,369 (1,601) | 44 (14) |
| cross_section | 2024 | hisp_pov | hisp_share | 12,136 | 1,350 (1,005) | 3,215 (1,673) | -1,607 (1,420) | -259 (280) | -93 (37) | 36 (4) | -43 (88) | 119 (55) | 3,112 (1,385) | -30 (18) |
| cross_section | 2024 | hisp_pov | pov_rate | 12,136 | 17,658 (2,501) | 22,259 (3,980) | -20,940 (3,252) | 16,339 (875) | 3,130 (144) | 9 (9) | 1,249 (401) | -82 (50) | 17,009 (3,205) | 387 (71) |
| cross_section | 2011 | hisp | hisp_share | 12,545 | 1,747 (609) | 5,268 (950) | -5,434 (1,028) | 1,913 (180) | 828 (66) | 38 (14) | 273 (172) | 69 (40) | 4,038 (754) | 63 (21) |
| cross_section | 2011 | hisp_pov | hisp_share | 12,496 | -194 (910) | 1,299 (766) | -879 (1,238) | -614 (191) | -250 (83) | 37 (13) | 3 (139) | 84 (46) | 1,015 (637) | -26 (35) |
| cross_section | 2011 | hisp_pov | pov_rate | 12,496 | 6,947 (1,872) | 14,293 (2,622) | -16,435 (3,139) | 9,089 (616) | 3,882 (225) | 4 (8) | 971 (416) | -54 (31) | 10,879 (2,296) | 322 (90) |
| cross_section | 2011 | el_pov | el_share | 11,659 | 4,314 (2,867) | -2,252 (1,476) | 7,165 (2,370) | -599 (906) | -576 (213) | 92 (33) | -356 (246) | 271 (122) | -2,783 (1,206) | -121 (60) |
| cross_section | 2011 | el_pov | pov_rate | 11,659 | 5,773 (1,902) | 15,774 (3,158) | -19,129 (3,266) | 9,128 (518) | 3,927 (214) | -7 (6) | 1,031 (521) | -58 (24) | 12,719 (2,556) | 385 (62) |
| cross_section | 2011 | el_hisp_pov | hisp_share | 11,659 | -2,307 (1,116) | 2,434 (1,400) | -3,817 (1,813) | -925 (427) | -225 (81) | 3 (6) | 129 (277) | 56 (40) | 2,573 (1,170) | -38 (28) |
| cross_section | 2011 | el_hisp_pov | el_share | 11,659 | 7,514 (3,439) | -5,628 (2,696) | 12,458 (3,517) | 684 (1,450) | -265 (227) | 88 (33) | -535 (441) | 194 (81) | -6,351 (2,011) | -68 (67) |
| cross_section | 2011 | el_hisp_pov | pov_rate | 11,659 | 6,581 (2,049) | 14,922 (2,965) | -17,793 (3,327) | 9,451 (498) | 4,006 (216) | -8 (6) | 986 (470) | -77 (35) | 11,818 (2,442) | 399 (63) |
| cross_section | 2006 | hisp | hisp_share | 12,902 | 1,763 (836) | 5,654 (1,008) | -5,534 (925) | 1,642 (139) | 840 (61) | 35 (17) | 679 (608) | 89 (53) | 3,996 (579) | 40 (20) |
| cross_section | 2006 | hisp_pov | hisp_share | 12,706 | 555 (995) | 1,362 (761) | -451 (1,222) | -356 (250) | 121 (105) | 28 (18) | 166 (376) | 105 (59) | 962 (558) | -28 (20) |
| cross_section | 2006 | hisp_pov | pov_rate | 12,706 | 4,659 (2,275) | 16,380 (2,675) | -19,345 (2,869) | 7,625 (531) | 2,742 (291) | 25 (20) | 1,955 (1,056) | -62 (37) | 11,549 (1,699) | 258 (73) |
| cross_section | 2006 | el_pov | el_share | 10,943 | 3,990 (2,145) | -880 (1,180) | 3,943 (2,244) | 927 (537) | 357 (227) | 113 (34) | -245 (374) | 114 (77) | -1,184 (671) | -28 (27) |
| cross_section | 2006 | el_pov | pov_rate | 10,943 | 4,381 (2,512) | 17,705 (3,260) | -20,129 (2,602) | 6,805 (539) | 2,621 (308) | -2 (17) | 2,468 (1,598) | -10 (31) | 12,321 (1,822) | 258 (77) |
| cross_section | 2006 | el_hisp_pov | hisp_share | 10,943 | -1,469 (913) | 3,340 (1,164) | -3,641 (1,349) | -1,168 (409) | 52 (90) | -18 (12) | 354 (723) | 98 (63) | 2,832 (753) | -44 (31) |
| cross_section | 2006 | el_hisp_pov | el_share | 10,943 | 5,611 (1,953) | -4,565 (1,636) | 7,961 (1,822) | 2,215 (871) | 300 (237) | 133 (36) | -635 (1,026) | 6 (36) | -4,309 (759) | 20 (40) |
| cross_section | 2006 | el_hisp_pov | pov_rate | 10,943 | 5,076 (2,597) | 16,124 (2,974) | -18,406 (2,824) | 7,358 (555) | 2,597 (329) | 7 (20) | 2,300 (1,292) | -56 (41) | 10,980 (1,736) | 279 (83) |
| panel_fy2001_2020 |  | levels_hisp_lnN | hisp_share | 12,993 | -1,650 (2,253) | 3,404 (711) | -6,215 (1,772) | 1,161 (196) | 501 (166) | 44 (13) | -226 (371) | 124 (77) | 3,142 (713) | 33 (21) |
| panel_fy2001_2020 |  | levels_hisp_pov_lnN | hisp_share | 12,516 | -3,484 (2,704) | 3,234 (1,187) | -7,344 (2,166) | 626 (374) | 553 (154) | 54 (18) | -336 (671) | 159 (97) | 3,110 (885) | -88 (49) |
| panel_fy2001_2020 |  | log_total_lnN_hisp | lnN | 12,993 | 0.766 (0.031) |  |  |  |  |  |  |  |  |  |
| panel_fy2001_2020 |  | log_total_lnN_hisp | hisp_share | 12,993 | -0.008 (0.078) |  |  |  |  |  |  |  |  |  |
| panel_fy2001_2020 |  | log_total_lnN_only | lnN | 12,993 | 0.766 (0.031) |  |  |  |  |  |  |  |  |  |
| panel_fy2001_2024 |  | levels_hisp_lnN | hisp_share | 13,162 | -611 (2,177) | 3,986 (739) | -5,819 (1,712) | 1,223 (409) | 434 (105) | 38 (12) | -148 (357) | 141 (87) | 3,818 (823) | -19 (24) |
| panel_fy2001_2024 |  | levels_hisp_pov_lnN | hisp_share | 12,658 | -724 (2,275) | 3,881 (938) | -5,722 (1,990) | 1,118 (424) | 403 (135) | 41 (16) | -217 (538) | 163 (100) | 3,902 (851) | -112 (35) |
| panel_fy2001_2024 |  | log_total_lnN_hisp | lnN | 13,162 | 0.756 (0.035) |  |  |  |  |  |  |  |  |  |
| panel_fy2001_2024 |  | log_total_lnN_hisp | hisp_share | 13,162 | 0.049 (0.072) |  |  |  |  |  |  |  |  |  |
| panel_fy2001_2024 |  | log_total_lnN_only | lnN | 13,162 | 0.758 (0.035) |  |  |  |  |  |  |  |  |  |

**Table A6c.** Compensatory funding, spending outcomes: dollars per pupil (2024) per unit share (log-total specs: elasticities); state fixed effects in cross-sections, district and state-year effects in panels; SE clustered by state.

| design | fy | spec | term | districts | current | instruction | instr_support | administration |
|---|---|---|---|---|---|---|---|---|
| cross_section | 2020 | hisp | hisp_share | 12,332 | 2,171 (368) | 939 (262) | 342 (81) | 234 (48) |
| cross_section | 2020 | hisp_pov | hisp_share | 12,206 | 534 (573) | 166 (314) | 268 (163) | 4 (74) |
| cross_section | 2020 | hisp_pov | pov_rate | 12,206 | 7,947 (1,756) | 3,729 (1,342) | 365 (652) | 1,122 (232) |
| cross_section | 2020 | el_pov | el_share | 10,019 | 3,697 (1,337) | 1,125 (1,287) | 1,509 (522) | 606 (178) |
| cross_section | 2020 | el_pov | pov_rate | 10,019 | 6,868 (1,648) | 3,323 (1,535) | 63 (663) | 865 (221) |
| cross_section | 2020 | el_hisp_pov | hisp_share | 10,019 | -916 (1,021) | -267 (732) | -322 (269) | -276 (119) |
| cross_section | 2020 | el_hisp_pov | el_share | 10,019 | 4,882 (2,366) | 1,470 (2,095) | 1,925 (800) | 964 (313) |
| cross_section | 2020 | el_hisp_pov | pov_rate | 10,019 | 7,289 (1,718) | 3,445 (1,404) | 211 (671) | 991 (229) |
| cross_section | 2024 | hisp | hisp_share | 12,253 | 3,968 (546) | 1,914 (377) | 650 (109) | 398 (70) |
| cross_section | 2024 | hisp_pov | hisp_share | 12,136 | 1,239 (708) | 640 (404) | 373 (205) | 21 (90) |
| cross_section | 2024 | hisp_pov | pov_rate | 12,136 | 14,258 (1,398) | 6,657 (1,528) | 1,449 (898) | 1,970 (312) |
| cross_section | 2011 | hisp | hisp_share | 12,545 | 1,967 (563) | 1,216 (521) | 220 (89) | 127 (51) |
| cross_section | 2011 | hisp_pov | hisp_share | 12,496 | -67 (821) | 248 (516) | -65 (167) | -131 (111) |
| cross_section | 2011 | hisp_pov | pov_rate | 12,496 | 7,296 (1,588) | 3,478 (908) | 1,022 (609) | 927 (269) |
| cross_section | 2011 | el_pov | el_share | 11,659 | 3,178 (2,437) | 1,909 (1,443) | 524 (516) | 598 (358) |
| cross_section | 2011 | el_pov | pov_rate | 11,659 | 6,498 (1,529) | 3,394 (1,045) | 790 (672) | 660 (284) |
| cross_section | 2011 | el_hisp_pov | hisp_share | 11,659 | -1,305 (1,033) | -129 (692) | -380 (285) | -482 (145) |
| cross_section | 2011 | el_hisp_pov | el_share | 11,659 | 4,987 (2,772) | 2,088 (1,448) | 1,051 (722) | 1,267 (463) |
| cross_section | 2011 | el_hisp_pov | pov_rate | 11,659 | 6,955 (1,712) | 3,439 (987) | 923 (694) | 829 (307) |
| cross_section | 2006 | hisp | hisp_share | 12,902 | 2,269 (673) | 1,320 (552) | 424 (139) | 124 (52) |
| cross_section | 2006 | hisp_pov | hisp_share | 12,706 | 593 (849) | 565 (580) | 179 (127) | -102 (109) |
| cross_section | 2006 | hisp_pov | pov_rate | 12,706 | 6,427 (1,883) | 2,943 (926) | 947 (587) | 820 (323) |
| cross_section | 2006 | el_pov | el_share | 10,943 | 3,183 (1,826) | 1,703 (936) | 754 (445) | 324 (263) |
| cross_section | 2006 | el_pov | pov_rate | 10,943 | 6,611 (1,957) | 3,486 (924) | 902 (767) | 594 (371) |
| cross_section | 2006 | el_hisp_pov | hisp_share | 10,943 | -1,045 (868) | -227 (692) | -204 (221) | -350 (109) |
| cross_section | 2006 | el_hisp_pov | el_share | 10,943 | 4,336 (1,713) | 1,954 (902) | 979 (586) | 710 (270) |
| cross_section | 2006 | el_hisp_pov | pov_rate | 10,943 | 7,106 (2,100) | 3,593 (893) | 999 (738) | 760 (387) |
| panel_fy2001_2020 |  | levels_hisp_lnN | hisp_share | 12,993 | -1,284 (1,744) | -1,175 (1,459) | 287 (217) | -297 (178) |
| panel_fy2001_2020 |  | levels_hisp_pov_lnN | hisp_share | 12,516 | -2,237 (2,477) | -1,649 (1,901) | 234 (169) | -508 (363) |
| panel_fy2001_2020 |  | log_total_lnN_hisp | lnN | 12,993 | 0.831 (0.021) | 0.894 (0.024) | 0.809 (0.040) | 0.720 (0.027) |
| panel_fy2001_2020 |  | log_total_lnN_hisp | hisp_share | 12,993 | -0.012 (0.066) | -0.023 (0.066) | 0.165 (0.094) | -0.131 (0.108) |
| panel_fy2001_2020 |  | log_total_lnN_only | lnN | 12,993 | 0.831 (0.021) | 0.893 (0.024) | 0.813 (0.040) | 0.717 (0.027) |
| panel_fy2001_2024 |  | levels_hisp_lnN | hisp_share | 13,162 | -1,041 (1,640) | -1,063 (1,345) | 287 (300) | -268 (227) |
| panel_fy2001_2024 |  | levels_hisp_pov_lnN | hisp_share | 12,658 | -1,238 (1,909) | -1,068 (1,517) | 234 (223) | -376 (316) |
| panel_fy2001_2024 |  | log_total_lnN_hisp | lnN | 13,162 | 0.817 (0.021) | 0.890 (0.023) | 0.796 (0.032) | 0.689 (0.024) |
| panel_fy2001_2024 |  | log_total_lnN_hisp | hisp_share | 13,162 | 0.013 (0.063) | -0.011 (0.062) | 0.225 (0.080) | -0.087 (0.120) |
| panel_fy2001_2024 |  | log_total_lnN_only | lnN | 13,162 | 0.817 (0.021) | 0.890 (0.023) | 0.802 (0.032) | 0.686 (0.025) |

**Table A7.** Teachers on pupils, long differences within state.

| spec | weight | teacher_elasticity | se | ci_low | ci_high | n_districts | ptr_start_pw | ptr_end_pw |
|---|---|---|---|---|---|---|---|---|
| ld_2000_2018 | unweighted | 0.828 | 0.018 | 0.794 | 0.863 | 11172 | 16.290 | 16.139 |
| ld_2000_2018 | pupils | 0.931 | 0.010 | 0.911 | 0.952 | 11172 | 16.290 | 16.139 |
| ld_2018_2023 | unweighted | 0.587 | 0.034 | 0.520 | 0.654 | 12046 | 15.995 | 15.119 |
| ld_2018_2023 | pupils | 0.756 | 0.044 | 0.670 | 0.842 | 12046 | 15.995 | 15.119 |

**Table A8.** Instruction dilution by response basis: instruction dollars a year ($bn, 2024) and present value of other pupils' lifetime earnings ($bn a year).

| horizon | price_year | b_instruction | response_current | instruction_dilution_bn | instruction_dilution_power_law_bn | instruction_dilution_full_funding_others_bn | instr_support_dilution_bn | per_other_pupil_in_group_districts_usd | pv_earnings_bn_jm_low | pv_earnings_bn_jm_central | pv_earnings_bn_jm_high | pv_earnings_bn_jm_central_cfr_va | pv_earnings_bn_jm_central_power_law | pv_earnings_bn_jm_central_full_funding_others |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| account_low_end | fy2024 | 0.650 | 0.630 | 29.413 | 23.165 | 16.731 | 7.288 | 750 | -2.121 | 16.760 | 35.535 | 14.396 | 13.199 | 9.533 |
| account_low_end | fy2019_in_2024usd | 0.650 | 0.630 | 26.221 | 20.761 | 15.125 | 5.686 | 669 | -1.891 | 14.940 | 31.677 | 12.833 | 11.830 | 8.618 |
| account_high_end | fy2024 | 0.678 | 0.660 | 27.029 | 21.101 | 15.375 | 6.697 | 689 | -1.949 | 15.401 | 32.653 | 13.229 | 12.023 | 8.760 |
| account_high_end | fy2019_in_2024usd | 0.678 | 0.660 | 24.095 | 18.916 | 13.898 | 5.225 | 614 | -1.738 | 13.729 | 29.109 | 11.793 | 10.778 | 7.919 |
| account_low_end_phi_3yr | fy2024 | 0.681 | 0.630 | 26.839 | 20.938 | 15.267 | 7.440 | 684 | -1.936 | 15.293 | 32.424 | 13.136 | 11.931 | 8.699 |
| account_low_end_phi_3yr | fy2019_in_2024usd | 0.681 | 0.630 | 23.926 | 18.770 | 13.801 | 5.805 | 610 | -1.726 | 13.633 | 28.905 | 11.710 | 10.695 | 7.864 |
| account_high_end_phi_3yr | fy2024 | 0.707 | 0.660 | 24.663 | 19.090 | 14.029 | 6.837 | 629 | -1.779 | 14.053 | 29.795 | 12.071 | 10.877 | 7.994 |
| account_high_end_phi_3yr | fy2019_in_2024usd | 0.707 | 0.660 | 21.986 | 17.116 | 12.682 | 5.335 | 561 | -1.586 | 12.527 | 26.561 | 10.761 | 9.753 | 7.226 |
| account_low_end_phi_4_5yr | fy2024 | 0.698 | 0.630 | 25.405 | 19.717 | 14.451 | 8.155 | 648 | -1.832 | 14.475 | 30.692 | 12.434 | 11.234 | 8.234 |
| account_low_end_phi_4_5yr | fy2019_in_2024usd | 0.698 | 0.630 | 22.647 | 17.677 | 13.063 | 6.363 | 578 | -1.633 | 12.904 | 27.360 | 11.084 | 10.072 | 7.443 |
| account_high_end_phi_4_5yr | fy2024 | 0.722 | 0.660 | 23.345 | 17.984 | 13.279 | 7.494 | 595 | -1.684 | 13.302 | 28.203 | 11.426 | 10.247 | 7.566 |
| account_high_end_phi_4_5yr | fy2019_in_2024usd | 0.722 | 0.660 | 20.811 | 16.127 | 12.004 | 5.847 | 531 | -1.501 | 11.858 | 25.142 | 10.186 | 9.189 | 6.840 |
| district_1yr | fy2024 | 0.481 | 0.449 | 43.613 | 36.274 | 24.808 | 10.757 | 1,112 | -3.146 | 24.850 | 52.689 | 21.346 | 20.669 | 14.136 |
| district_1yr | fy2019_in_2024usd | 0.481 | 0.449 | 38.879 | 32.467 | 22.426 | 8.393 | 992 | -2.804 | 22.153 | 46.969 | 19.029 | 18.500 | 12.778 |
| district_3yr | fy2024 | 0.749 | 0.700 | 21.074 | 16.105 | 11.988 | 5.930 | 537 | -1.520 | 12.008 | 25.460 | 10.315 | 9.176 | 6.831 |
| district_3yr | fy2019_in_2024usd | 0.749 | 0.700 | 18.787 | 14.445 | 10.837 | 4.627 | 479 | -1.355 | 10.705 | 22.696 | 9.195 | 8.230 | 6.175 |
| district_4_5yr | fy2024 | 0.807 | 0.758 | 16.206 | 12.176 | 9.218 | 5.131 | 413 | -1.169 | 9.234 | 19.578 | 7.932 | 6.938 | 5.253 |
| district_4_5yr | fy2019_in_2024usd | 0.807 | 0.758 | 14.447 | 10.925 | 8.333 | 4.003 | 368 | -1.042 | 8.232 | 17.453 | 7.071 | 6.225 | 4.748 |
| district_19yr | fy2024 | 0.924 | 0.869 | 6.405 | 4.656 | 3.643 | 2.186 | 163 | -0.462 | 3.649 | 7.737 | 3.135 | 2.653 | 2.076 |
| district_19yr | fy2019_in_2024usd | 0.924 | 0.869 | 5.709 | 4.181 | 3.293 | 1.706 | 146 | -0.412 | 3.253 | 6.897 | 2.794 | 2.383 | 1.876 |
| district_fe_log | fy2024 | 0.890 | 0.830 | 9.261 | 6.796 | 5.268 | 3.504 | 236 | -0.668 | 5.277 | 11.188 | 4.533 | 3.872 | 3.002 |
| district_fe_log | fy2019_in_2024usd | 0.890 | 0.830 | 8.256 | 6.102 | 4.762 | 2.734 | 211 | -0.595 | 4.704 | 9.974 | 4.041 | 3.477 | 2.713 |
| district_fe_level | fy2024 | 0.768 | 0.734 | 19.500 | 14.819 | 11.092 | 5.828 | 497 | -1.406 | 11.111 | 23.558 | 9.544 | 8.444 | 6.320 |
| district_fe_level | fy2019_in_2024usd | 0.768 | 0.734 | 17.383 | 13.293 | 10.027 | 4.548 | 443 | -1.254 | 9.905 | 21.000 | 8.508 | 7.575 | 5.713 |
| state_cbo_unweighted | fy2024 | 0.902 | 0.707 | 8.266 | 6.046 | 4.702 | 14.236 | 211 | -0.596 | 4.710 | 9.986 | 4.046 | 3.445 | 2.679 |
| state_cbo_unweighted | fy2019_in_2024usd | 0.902 | 0.707 | 7.369 | 5.429 | 4.250 | 11.108 | 188 | -0.531 | 4.199 | 8.902 | 3.607 | 3.093 | 2.422 |
| state_cbo_pupils | fy2024 | 0.335 | 0.349 | 55.892 | 48.920 | 31.793 | 11.409 | 1,425 | -4.031 | 31.847 | 67.524 | 27.356 | 27.874 | 18.116 |
| state_cbo_pupils | fy2019_in_2024usd | 0.335 | 0.349 | 49.825 | 43.734 | 28.741 | 8.902 | 1,271 | -3.594 | 28.390 | 60.194 | 24.386 | 24.919 | 16.376 |
| state_ld_19yr | fy2024 | 0.418 | 0.488 | 48.872 | 41.527 | 27.800 | 5.493 | 1,246 | -3.525 | 27.847 | 59.043 | 23.920 | 23.662 | 15.840 |
| state_ld_19yr | fy2019_in_2024usd | 0.418 | 0.488 | 43.567 | 37.151 | 25.131 | 4.286 | 1,111 | -3.142 | 24.824 | 52.634 | 21.324 | 21.168 | 14.319 |

**Table A9.** By region and district child-poverty quintile (pupil-weighted, SAIPE 2023; Q1 least poor): pupils (m), dilution ($bn), per other pupil ($).

| horizon | dimension | group | other_pupils_m | group_pupils_m | group_share_of_pupils | instruction_dilution_bn | per_other_pupil_usd | pv_bn_jm_central | pv_bn_jm_low | pv_bn_jm_high | pv_per_other_pupil_usd_jm_central | pv_bn_jm_central_full_funding_others | pv_per_other_pupil_usd_full_funding |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| account_low_end | region | Midwest | 8.777 | 0.969 | 0.099 | 3.658 | 417 | 2.084 | -0.264 | 4.419 | 237 | 1.531 | 174 |
| account_low_end | region | Northeast | 7.108 | 0.255 | 0.035 | 1.904 | 268 | 1.085 | -0.137 | 2.300 | 153 | 0.971 | 137 |
| account_low_end | region | South | 15.981 | 3.178 | 0.166 | 8.628 | 540 | 4.916 | -0.622 | 10.424 | 308 | 2.863 | 179 |
| account_low_end | region | West | 7.585 | 4.085 | 0.350 | 15.223 | 2,007 | 8.674 | -1.098 | 18.391 | 1,144 | 4.168 | 550 |
| account_low_end | income_group | Q1 least poor | 8.842 | 0.745 | 0.078 | 2.481 | 281 | 1.414 | -0.179 | 2.998 | 160 | 1.179 | 133 |
| account_low_end | income_group | Q2 | 8.236 | 1.352 | 0.141 | 4.523 | 549 | 2.577 | -0.326 | 5.464 | 313 | 1.797 | 218 |
| account_low_end | income_group | Q3 | 7.723 | 1.862 | 0.194 | 6.331 | 820 | 3.608 | -0.457 | 7.649 | 467 | 2.081 | 269 |
| account_low_end | income_group | Q4 | 7.138 | 2.192 | 0.235 | 7.654 | 1,072 | 4.361 | -0.552 | 9.247 | 611 | 2.250 | 315 |
| account_low_end | income_group | Q5 poorest | 7.513 | 2.335 | 0.237 | 8.424 | 1,121 | 4.800 | -0.608 | 10.177 | 639 | 2.226 | 296 |
| account_high_end | region | Midwest | 8.777 | 0.969 | 0.099 | 3.361 | 383 | 1.915 | -0.242 | 4.061 | 218 | 1.407 | 160 |
| account_high_end | region | Northeast | 7.108 | 0.255 | 0.035 | 1.750 | 246 | 0.997 | -0.126 | 2.114 | 140 | 0.892 | 126 |
| account_high_end | region | South | 15.981 | 3.178 | 0.166 | 7.929 | 496 | 4.518 | -0.572 | 9.579 | 283 | 2.631 | 165 |
| account_high_end | region | West | 7.585 | 4.085 | 0.350 | 13.989 | 1,844 | 7.971 | -1.009 | 16.900 | 1,051 | 3.830 | 505 |
| account_high_end | income_group | Q1 least poor | 8.842 | 0.745 | 0.078 | 2.280 | 258 | 1.299 | -0.164 | 2.755 | 147 | 1.083 | 123 |
| account_high_end | income_group | Q2 | 8.236 | 1.352 | 0.141 | 4.156 | 505 | 2.368 | -0.300 | 5.021 | 288 | 1.652 | 201 |
| account_high_end | income_group | Q3 | 7.723 | 1.862 | 0.194 | 5.818 | 753 | 3.315 | -0.420 | 7.029 | 429 | 1.912 | 248 |
| account_high_end | income_group | Q4 | 7.138 | 2.192 | 0.235 | 7.033 | 985 | 4.008 | -0.507 | 8.497 | 561 | 2.068 | 290 |
| account_high_end | income_group | Q5 poorest | 7.513 | 2.335 | 0.237 | 7.741 | 1,030 | 4.411 | -0.558 | 9.352 | 587 | 2.045 | 272 |
| district_19yr | region | Midwest | 8.777 | 0.969 | 0.099 | 0.797 | 91 | 0.454 | -0.057 | 0.962 | 52 | 0.333 | 38 |
| district_19yr | region | Northeast | 7.108 | 0.255 | 0.035 | 0.415 | 58 | 0.236 | -0.030 | 0.501 | 33 | 0.211 | 30 |
| district_19yr | region | South | 15.981 | 3.178 | 0.166 | 1.879 | 118 | 1.070 | -0.136 | 2.270 | 67 | 0.623 | 39 |
| district_19yr | region | West | 7.585 | 4.085 | 0.350 | 3.315 | 437 | 1.889 | -0.239 | 4.005 | 249 | 0.908 | 120 |
| district_19yr | income_group | Q1 least poor | 8.842 | 0.745 | 0.078 | 0.540 | 61 | 0.308 | -0.039 | 0.653 | 35 | 0.257 | 29 |
| district_19yr | income_group | Q2 | 8.236 | 1.352 | 0.141 | 0.985 | 120 | 0.561 | -0.071 | 1.190 | 68 | 0.391 | 48 |
| district_19yr | income_group | Q3 | 7.723 | 1.862 | 0.194 | 1.379 | 179 | 0.786 | -0.099 | 1.665 | 102 | 0.453 | 59 |
| district_19yr | income_group | Q4 | 7.138 | 2.192 | 0.235 | 1.667 | 233 | 0.950 | -0.120 | 2.013 | 133 | 0.490 | 69 |
| district_19yr | income_group | Q5 poorest | 7.513 | 2.335 | 0.237 | 1.834 | 244 | 1.045 | -0.132 | 2.216 | 139 | 0.485 | 65 |

**Table A10.** Composition channel: others' instruction change and its present value ($bn a year; negative is a loss).

| gamma_case | gamma_usd_per_unit_share | others_instruction_change_bn | pv_bn_jm_central | pv_bn_jm_low | pv_bn_jm_high |
|---|---|---|---|---|---|
| central | -1,175 | -4.514 | -2.572 | 0.326 | -5.453 |
| low | -4,034 | -15.498 | -8.830 | 1.118 | -18.723 |
| high | 1,684 | 6.470 | 3.687 | -0.467 | 7.817 |

**Table A11.** Class size as the same resource loss (never added).

| spec | teacher_elasticity | others_ptr_rise_pupils_weighted_mean | pv_bn_jm_central_via_class_size |
|---|---|---|---|
| ld_2000_2018 | 0.931 | 0.167 | 2.596 |
| ld_2018_2023 | 0.756 | 0.568 | 8.812 |

**Table A12.** `derived/winners_losers_rows.csv` ($bn a year; per person in dollars; the counterfactual and source columns are in the file).

| group | channel | direction | bn_low | bn_central | bn_high | population_m | per_person_usd | basis | relation_to_account |
|---|---|---|---|---|---|---|---|---|---|
| other_residents_pupils | instruction_dilution_account | loss | -2.122 | 16.080 | 35.535 | 39.452 | 408 | modelled | beside |
| other_residents_pupils | instruction_dilution_long_run | loss | -0.462 | 3.649 | 7.737 | 39.452 | 92 | modelled | overlaps:instruction_dilution_account |
| other_residents_pupils:region=Midwest | instruction_dilution_account | loss | -0.264 | 2.000 | 4.419 | 8.777 | 228 | modelled | overlaps:instruction_dilution_account |
| other_residents_pupils:region=Northeast | instruction_dilution_account | loss | -0.137 | 1.041 | 2.300 | 7.108 | 146 | modelled | overlaps:instruction_dilution_account |
| other_residents_pupils:region=South | instruction_dilution_account | loss | -0.622 | 4.717 | 10.424 | 15.981 | 295 | modelled | overlaps:instruction_dilution_account |
| other_residents_pupils:region=West | instruction_dilution_account | loss | -1.098 | 8.322 | 18.391 | 7.585 | 1,097 | modelled | overlaps:instruction_dilution_account |
| other_residents_pupils:district child-poverty quintile=Q1 least poor | instruction_dilution_account | loss | -0.179 | 1.357 | 2.998 | 8.842 | 153 | modelled | overlaps:instruction_dilution_account |
| other_residents_pupils:district child-poverty quintile=Q2 | instruction_dilution_account | loss | -0.326 | 2.473 | 5.464 | 8.236 | 300 | modelled | overlaps:instruction_dilution_account |
| other_residents_pupils:district child-poverty quintile=Q3 | instruction_dilution_account | loss | -0.457 | 3.461 | 7.649 | 7.723 | 448 | modelled | overlaps:instruction_dilution_account |
| other_residents_pupils:district child-poverty quintile=Q4 | instruction_dilution_account | loss | -0.552 | 4.184 | 9.247 | 7.138 | 586 | modelled | overlaps:instruction_dilution_account |
| other_residents_pupils:district child-poverty quintile=Q5 poorest | instruction_dilution_account | loss | -0.608 | 4.605 | 10.177 | 7.513 | 613 | modelled | overlaps:instruction_dilution_account |
| other_residents_pupils | support_services_dilution_account | loss | -0.483 | 3.984 | 8.804 | 39.452 | 101 | modelled | beside |
| other_residents_pupils | compensatory_composition | loss | -3.687 | 2.572 | 8.831 | 39.452 | 65 | measured | overlaps:instruction_dilution_account |
| other_residents_pupils | class_size_same_resource | loss |  | 2.596 | 8.812 | 39.452 | 66 | modelled | overlaps:instruction_dilution_account |
| other_residents_pupils | peer_effects | loss |  |  |  | 39.452 |  | unpriced | beside |
| other_residents_pupils | instruction_dilution_account_power_law | loss | -1.522 | 12.611 | 27.985 | 39.452 | 320 | modelled | overlaps:instruction_dilution_account |
| other_residents_pupils | instruction_dilution_full_funding_share | loss | -1.109 | 9.147 | 20.213 | 39.452 | 232 | modelled | overlaps:instruction_dilution_account |
| group_pupils | instruction_dilution_shared | loss | -0.841 | 6.933 | 15.321 | 8.487 | 817 | modelled | overlaps:instruction_dilution_account |
| taxpayers | unfunded_instruction | gain | 29.903 | 32.102 | 34.301 |  |  | modelled | inside |
| taxpayers | unfunded_instructional_support | gain | 5.470 | 5.873 | 6.275 |  |  | modelled | inside |
| taxpayers | scale_economies_admin_plant_transport_food | gain | 15.805 | 16.967 | 18.129 |  |  | modelled | inside |
| state_taxpayers | compensatory_financing | loss | 12.464 | 21.099 | 29.735 |  |  | measured | inside |
| federal_taxpayers | compensatory_financing | loss | 4.816 | 7.195 | 9.574 |  |  | measured | inside |
| local_taxpayers_in_group_districts | compensatory_financing | gain |  |  |  |  |  | unpriced | inside |
| future_taxpayers | lower_tax_on_other_pupils_earnings | loss | -0.530 | 4.824 | 12.437 |  |  | assumed | overlaps:instruction_dilution_account |

**Table A13.** Pricing constants (`derived/pricing_constants.json`).

| constant | value |
|---|---|
| pv_per_dollar | {"low": -0.0721255922663106, "central": 0.5697921789038539, "high": 1.2081036704607029} |
| pv_per_dollar_cfr_va | 0.4894 |
| cpi | {"2010": 218.0761666666667, "2018": 251.0995, "2024": 313.6981666666667} |
| pv_lifetime_earnings_2024usd | 750,886.4701 |
| group_pupils_m | 8.4870 |
| all_pupils_m | 47.9387 |
| other_pupils_m | 39.4517 |
| group_weighted_instruction_pp_fy2024 | 9,901.9672 |
| group_weighted_current_pp_fy2024 | 16,965.6900 |
| group_pupils_imputed_price_share | 0.0854 |
| gamma | {"central": -1174.960377, "low": -4034.27241, "high": 1684.351655} |

<!-- tables:end -->
