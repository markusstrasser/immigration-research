# V9: how much remaining-household work would have to change

**Verdict:** We can narrow the household concern, but cannot close it. Within the
observed household roster, the broad care proxy gives a relatively modest direct
tax-and-SNAP sensitivity: **$2.40–2.45bn less modeled fiscal cost at a 25% earnings
loss, and $6.78–8.61bn less at complete loss of current positive earnings**. Across
all remaining adults sharing a household with someone removed, a **10% earnings
loss gives $12.07–12.18bn less**. That broader channel cannot be dismissed from
exposure size alone. These are conditional annual statutory cash responses,
**not measured behavior, complete bounds, or an adopted correction to v9**.
[CALCULATION: [response table](../infra/immigration-fiscal/household_behavior_bound_2026_10_16/derived/responses.csv)]

This answers one link from the [feedback review](immigration-v9-behavioral-feedback-2026-10-16.md):
departure changes a remaining household's income or available help, which changes
remaining adults' work and hence public receipts/benefits. Lost help can reduce
work; lost income can induce more work. The analysis tests both signs rather than
assuming the direction. It measures exposure from raw records and then applies
declared earnings changes. No causal elasticity is estimated. [INFERENCE]

## What the raw records establish

The raw material is the pinned **2025 CPS ASEC**, income year **2024**: person and
household records, parent/spouse links, earnings components and all 160 signed
replicate weights. The loader verifies the archive hash and person-key joins.
The departure mask combines the original union, v9's exact observed completion
records, and the existing located latent-child subset. That subset is part of the
already counted lineage; it is not a new population addition. Adult exposure
weights are the adults' own weights; the current native-minor calibration leaves
adult factors at one. [DATA: [audit and source hashes](../infra/immigration-fiscal/household_behavior_bound_2026_10_16/derived/audit.json);
raw archive `infra/immigration-fiscal/gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip`]

| Remaining civilian adults | Sample adults / households | Weighted adults, millions | Current annual earnings, $bn |
|---|---:|---:|---:|
| Share a household with an observed departure | 3,044 / 2,370 | 6.038 (SE 0.145) | 314.749 (SE 10.336) |
| Above, with a departing adult and another remaining person under 13, 65+, or reporting disability | 432 / 240 | 0.849 (SE 0.073) | 27.273 (SE 3.194) |
| Broad group, with another remaining person reporting dressing/bathing or errands difficulty | 101 / 59 | 0.188 (SE 0.031) | 5.014 (SE 1.283) |

Rows overlap; do not add them. The second row is the **care proxy** used below.
Neither age nor disability establishes caregiving, unmet need, or the departing
person's contribution. The narrow disability questions do not cover children
under 15. The first group contains 4.539 million adults with positive labor
income; the care proxy contains 0.541 million. SEs reflect survey sampling,
conditional on the classification and calibration; they do not cover unknown
ancestry or behavioral uncertainty. [CALCULATION: audit `exposures`; SOURCE:
Census dictionary `payroll_compliance_2026_09_28/_cache/sources/asec2025_ddl_pub_full.txt`,
lines 1648–1810, 2522–2528, 2697–2703, 2837–2889]

Some descendants and all net Census-missed additions lack household locations.
Some nominal remaining outsiders may themselves be unlocated descendants, and
some currently unexposed households may be affected by those unlocated people.
Thus the observed roster is neither a complete lineage roster nor a guaranteed
lower or upper bound on exposure. Current household composition is measured in
2025, whereas earnings refer to 2024. [DATA: v9 payload `meta.population_v9`,
`meta.union_completion`; INFERENCE]

## What the fiscal calculation says

The comparison is **changed earnings after removal minus unchanged earnings after
removal**, on the same people and claimant links. Positive wage and positive net
self-employment income change by the listed fraction; losses and other income
stay fixed. Federal and state income taxes include refundable credits. Payroll
includes employer and employee contributions. SNAP has four declared shelter/
participation specifications. The range in each row spans those specifications;
it is not a confidence interval. All amounts are annual $bn. [CALCULATION]

| Earnings change | All exposed adults: change in net fiscal cost | Care proxy: change in net fiscal cost |
|---|---:|---:|
| −10% | −12.18 to −12.07 | −0.99 to −0.97 |
| −25% | −30.36 to −29.87 | −2.45 to −2.40 |
| −50% | −60.30 to −58.52 | −5.05 to −4.75 |
| −100% | −111.94 to −99.31 | −8.61 to −6.78 |
| +10% | +12.29 to +12.34 | +1.02 to +1.02 |
| +25% | +30.87 to +30.99 | +2.54 to +2.57 |
| +50% | +62.36 to +62.60 | +5.13 to +5.18 |
| +100% | +126.35 to +126.66 | +10.45 to +10.51 |
| $10,000 wages for each currently zero-positive-labor-income adult | +2.34 to +2.95 | +0.43 to +0.52 |

Negative means removal leaves remaining residents with a worse fiscal balance,
reducing the modeled fiscal cost attributed to the departing group. It does not
mean the remaining households become better off. The entry arm is an illustrative
earnings change, not an estimate of employment transitions. Positive shocks need
not be feasible hours changes for people already working full time. [INFERENCE]

For an uncertainty example, the broad −10% scenario with zero shelter deduction
and full takeup among newly eligible SNAP units is **−$12.149bn, SDR SE $0.433bn**;
the care-proxy complete-loss scenario in that specification is **−$8.612bn,
SE $1.105bn**. These sampling errors do not validate the assumed work response.
[CALCULATION: response table]

The predeclared materiality reference is **5% of v9's lower cash endpoint**, or
**$14.220bn**. This is a decision convention. The broader group crosses that scale
between the **10% and 25%** loss scenarios; straight-line interpolation suggests
roughly **12%**, but is not an exact nonlinear tax threshold. None of the care
proxy's prescribed scenarios reaches it. Even complete earnings loss in that
proxy is a stress scenario, not a formal bound on all caregiving effects.
The crossing assumes the same proportional shock to every exposed earner;
concentrating the same aggregate loss on different earners can change the fiscal
response. The secondary scale reference, 5% of the accrual lower endpoint, is
**$18.401bn**; it is not an accrual valuation of this response.
[CALCULATION: [design](../infra/immigration-fiscal/household_behavior_bound_2026_10_16/DESIGN.md),
audit, response table; FRAMING-SENSITIVE]

## What makes this check trustworthy—and what still prevents adoption

The independent anchors are the Census source records, the local pinned NBER
income-tax calculator, and the SSA/IRS/USDA statutory rules. High-wage fixtures
found that the calculator's combined payroll and Additional Medicare outputs
do not match the source formulas. We therefore compute payroll separately,
subtract its named Additional Medicare component from federal tax, and insert
the correct component once. The remaining income-tax calculation is still the
pinned kernel, not an exact administrative return reconstruction. [SOURCE:
[SSA 2024](https://www.ssa.gov/news/en/cola/factsheets/2024.html),
[IRS Additional Medicare](https://www.irs.gov/taxtopics/tc560),
[NBER TAXSIM](https://taxsim.nber.org/taxsimtest/);
CALCULATION: [fixtures](../infra/immigration-fiscal/household_behavior_bound_2026_10_16/test_bound.py),
[failure record](../infra/immigration-fiscal/household_behavior_bound_2026_10_16/failure-catalog.md)]

The surviving claimant registry covers every exposed adult exactly once,
including modeled individual returns for otherwise unrepresented adults. A joint
return uses its surviving claimant's survey weight; payroll uses each person's
own weight. SNAP uses the original mean person weight per SPM unit, fixed across
shocks. Its annual-income, assistance-unit, shelter and participation assumptions
are explicit; Alaska/noncivilian units are excluded from priced SNAP changes.
The original income residual and deductions are frozen, and an earnings shock
changes both gross and earned income. No old removal correction is subtracted
again. [CALCULATION: [implementation](../infra/immigration-fiscal/household_behavior_bound_2026_10_16/bound.py)]

These are **statutory survey-dollar sensitivities**, without v9's IRS allocation
multipliers, receipt calibration or status/compliance adjustment. They hold
deductions and surviving dependent claims fixed as earnings change. Health
coverage, other benefits, consumption taxes and newly earned retirement/Medicare
promises are unpriced, as are relocation and market-wide work responses. The
care/production terms already in v9 may overlap with a measured future work
response; no overlap has been priced away here. For these reasons **do not add
the table mechanically to either v9 endpoint**, particularly its accrual headline.
[INFERENCE]

The defensible update is specific: the directly observed care proxy has a smaller
tax-and-SNAP exposure than the broad household channel, even under severe assumed
earnings losses. The broad channel remains potentially consequential. Resolving
its sign and magnitude requires credible evidence on the earnings change of
remaining adults—not another choice of tax parameters. A useful next empirical
estimand would be annual earnings changes among remaining spouses/adults after
an externally induced household departure, with intact-household controls and
relocation/attrition tracked. A localized departure estimate would still need a
separate transport argument for v9's full-lineage counterfactual. [INFERENCE]

Instrument check: LLM-assisted politically sensitive research. The negative and
positive work responses were computed symmetrically. The apparent reassurance
for the care proxy is limited by its incomplete population and partial fiscal
coverage; the larger broad-group sensitivity is not promoted to an effect.
The design's implementation correction is disclosed. [FRAMING-SENSITIVE]

Validation and [Gemini/Astra review dispositions](../infra/immigration-fiscal/household_behavior_bound_2026_10_16/review.md)
found no material defect in the stated conditional conclusion. Model review is
not independent empirical confirmation of the hypothetical work response.
