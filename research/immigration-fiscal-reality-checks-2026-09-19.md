# Fiscal reality checks: necessary implications and independent records

**Follow-up:** The [executed administrative checks](immigration-administrative-checks-2026-09-19.md)
now report earnings/payroll diagnostics, current transfer totals and pupil counts.
This original note preserves the test rationale and prior necessary implications.

**Verdict:** The next strongest check is administrative earnings and tax receipts,
followed by current transfer totals and state/age/eligibility spending. Our
account implies a receipt shortfall per resident, not unusually high spending
per resident across all programs. Administrative records can tightly constrain
many component totals; the public products inspected do not directly identify
the full Mexican-origin union or a causal admission effect. [INFERENCE]

Date: 2026-09-19. Fiscal-budget perspective; all observed generations and education
levels, 40.896574m civilian-household residents. This note computes implications
of the latest account and identifies tests; it does **not** claim those new tests
have passed. Sources were checked for availability, definitions and reuse.

## 1. What the current numbers necessarily imply

[CALCULATION] From the [observed2024 account](immigration-macro-reconciliation-2026-09-19.md),
`macro_closure_2026_09_19/derived/finance_vintage_totals.csv`: divide updated
receipts, spending and net balance by each group's population. Prices/income
year2024. These are allocated model amounts; the range is across personal-source
and household-sharing conventions, not confidence limits. No age standardization.

| Annual amount per resident | Observed Mexican-origin union | All other civilian-household residents |
|---|---:|---:|
| Attributed receipts including fees | $10,341–10,867 | $19,108–19,280 |
| Attributed spending | $16,597–16,607 | $21,000–21,067 |
| Attributed deficit | $5,730–6,266 | $1,786–1,892 |

The union is **12.145%** of this modeled population, receives **9.82–9.86%** of
attributed spending, and supplies **6.96–7.23%** of attributed receipts. Aggregate
assigned receipts are still **$423–444bn**. These are shares of the model's partial
account, not observed shares of every US tax or program dollar.

[INFERENCE] A successful independent check should reproduce the lower receipt
capacity after matching tax units, ages, earnings and credits. It should not
require exceptionally high elderly or healthcare expenditure per member. Lower
receipts per resident can reflect both more dependents and lower earnings; the
all-age comparison does not distinguish them.

[CALCULATION] Giving the union the rest of the population's same per-person
partial balance yields a deficit of **$73.06bn shared/$77.36bn personal**. The
additional unadjusted shortfall relative to that benchmark is **$161.28bn/$178.90bn**:

`benchmark balance = target population × other-resident balance / other-resident population`.

This is a comparison, not an immigration effect or proof of why the country runs
deficits. It separates the absolute deficit from the amount exceeding a stated
reference. Both groups inherit the same incomplete national coverage.

## 2. Highest-value federal checks

| Test | What to compare and what would fail | Primary source and boundary |
|---|---|---|
| Income and income-tax distribution | Reconstruct tax units, then compare earnings/AGI, filer counts, tax liability and credits by income band and state. A large receipt underestimate on matched cells would directly weaken the deficit. | [IRS Historic Table2](https://www.irs.gov/statistics/soi-tax-stats-historic-table-2), tax-year2023 available. Match year and refund convention; federal individual tax is only part of our receipts. State residence is not ethnicity. |
| Covered earnings/payroll | Compare workers, earnings below the Social Security cap, uncapped Medicare wages, self-employment and contributions by age/state. Employer and employee halves must reconcile separately. | [SSA Annual Supplement2025 §4.B](https://www.ssa.gov/policy/docs/statcomps/supplement/2025/4b.html). Its2024 summary earnings are explicitly preliminary BLS/BEA estimates; use final administrative detailed cells where available. |
| Current program totals | Reconcile model OASDI/SSI/SNAP/UI amounts to same-year administrative payments and the same covered population. Reject historical reporting multipliers that fail current totals. | SSA, USDA and program accounts. Our `absolute_ledger.py` itemU transports major reporting ratios from income2017; new2024 totals test that transport. They are not already guaranteed to match. |
| Healthcare cost by eligibility | Compare enrollment member-years and payments for children, other adults, aged and disabled groups; account separately for dual eligibility and institutional services. Reject charging every enrollee the all-recipient average. | [CMS per-capita methodology2025](https://www.medicaid.gov/state-overviews/scorecard/content/scorecard-release/PerCapitaExpendDataMethod-2025.pdf): five eligibility groups, member-months/12, TAF allocation of CMS-64 totals and specific payment exclusions. |
| Redistribution by income/family type | Check whether our low-income and high-income tax/transfer profiles resemble an independently implemented fiscal distribution. Compare scope before comparing totals. | [CBO2022 distribution](https://www.cbo.gov/publication/62300) and [methods appendix](https://www.cbo.gov/publication/60706). CBO statistically matches IRS SOI to CPS; partly independent tax data/methods, not a wholly independent population sample. It excludes many services in our account. |

[SOURCE / CODE TRACE] `all_age_ledger_2026_09_17/analyze.py:38` combines CPS
FICA, FEDTAX_AC and STATETAX_A. An IRS1040 comparison must first separate federal
income tax from payroll/state tax. `absolute_ledger.py:683` and its parameter
file document the older program-specific reporting ratios. Rechecking an input
used to calibrate an amount establishes reproduction; unused years or
state/age/eligibility distributions provide actual out-of-sample checks.

## 3. Concrete state checks

[SOURCE] Texas HHS's [Medicaid/CHIP reference guide, 15th edition](https://www.hhs.texas.gov/sites/default/files/documents/texas-medicaid-chip-reference-guide-15th-edition.pdf)
uses stateFY2023 for these figures: non-disabled children were **73% of caseload
but32% of spending**; age/disability-related groups were **14% and55%**. Its
monthly full-benefit client costs were $261 for children and $2,228 for the
age/disability group. Caseload measures are generally monthly averages; the
pandemic coverage regime affected this dated observation. These are not current
2026 rates or Mexican-specific costs. [Guide data notes/Quick Facts, pp.iii,2–3.]

[INFERENCE] That distribution is a strong falsifier for using an undifferentiated
medical cost per enrollee. Compare model Medicaid costs by state, eligibility,
age and covered person-years, reconciling long-term/institutional care once.
California DHCS and CMS records also require a federal/state/local payer split;
the state General Fund is not the entire public cost.

[SOURCE] [Texas school enrollment2023–24](https://tea.texas.gov/reports-and-data/school-performance/accountability-research/enroll-2023-24.pdf)
was **5,531,236**, including **2,942,144 Hispanic pupils (53.2%)**. This includes
early education/pre-K. [California's grade table](https://www.cde.ca.gov/ds/ad/cefenrollmentcomp.asp)
reports **5,837,690 public pupils for2023–24**, including151,491 transitional
kindergarten pupils. Grade, public/private status and reporting date must match
before comparing with our CPS child counts. Broader Hispanic counts do not
reveal Mexican parentage or generation; non-Hispanic ancestry attriters further
complicate an ethnic ceiling. [INFERENCE]

[SOURCE] The [Texas FY2024 cash report](https://comptroller.texas.gov/transparency/reports/cash-report/2024/96-368.pdf)
records $181.1bn net revenue and $175.8bn net spending, excluding trust funds,
including **$81.9bn state taxes and $58.9bn federal income**. This is a cash
boundary for the year ended August31,2024. The [Comptroller's tax table](https://comptroller.texas.gov/about/media-center/infographics/2025/bre26-27/collections.php)
has $47.160bn state sales-tax collections and $81.874bn total taxes. Texas has
[no individual state income tax](https://gov.texas.gov/business/page/why-texas).

[INFERENCE] Check that the model assigns zero Texas state personal-income tax,
yet includes applicable federal income/payroll, consumption and property-tax
incidence. Collections inside Texas and taxes borne by Texas residents differ,
so reconcile instrument-specific totals before origin attribution. Local taxes
are additional to the quoted state totals. State cash surplus cannot establish
an all-government ethnic balance or pension solvency.

For school and state-finance dollar totals already used to set model prices,
matching is mainly source reconciliation. Unused administrative pupil counts,
eligibility distributions and years can challenge the survey-derived allocation.
The [TEA funding report](https://tea.texas.gov/about-tea/government-relations-and-legal/government-relations/public-education-state-funding-transparency-dec-2025.pdf)
also distinguishes federal/local/state sources and teacher-retirement financing;
do not add a grant, pension payment or capital outlay twice. [SOURCE / INFERENCE]

## 4. Where certainty stops

[SOURCE] The [Treasury's tax-data explanation](https://home.treasury.gov/news/featured-stories/disparities-in-the-benefits-of-tax-expenditures-by-race-and-ethnicity)
states that IRS tax returns do not collect race/ethnicity. Treasury's broad
race/Hispanic estimates are imputed. They are not observed Mexican-origin,
parentage or third-generation records. A Hispanic statistic or a county with
many Mexican-origin residents cannot simply be relabeled the target population.

Administrative does not always mean a complete census or perfect classification.
The [USDA FY2023 SNAP characteristics report](https://fns-prod.azureedge.us/sites/default/files/resource-files/snap-FY23-Characteristics-Report.pdf),
TableB.10, has unknown household-head race/Hispanic status for **19.1% nationally,
22.4% in California and65.4% in Texas**. Those are weighted review-sample
household-head categories, not participant ancestry. They constrain an ethnic
SNAP comparison; they do not invalidate program-wide payment totals.

[INFERENCE] A state budget surplus or deficit alone neither validates nor refutes
this all-government account. Federal financing, local school/property-tax
finance, high-income taxpayers, debt and different tax systems can offset a
particular group's assigned balance. Conversely, a poor high-Mexican-share
county is insufficient confirmation: income, age, economic geography and policy
can produce the same pattern.

More direct ethnic earnings/tax validation would require appropriately linked
survey and administrative records. Census describes such linkages in its
[SIPP guidance](https://www.census.gov/programs-surveys/sipp/guidance.html), but
synthetic public data are not literal linked records. [Restricted-use access](https://www.census.gov/topics/research/guidance/restricted-use-microdata.html)
requires approved projects, and the current SAP catalog controls availability.
No application, eligibility or exact-generation coverage is assumed here.

## 5. Decision

Leading explanation to test: lower earnings/tax capacity and age composition
produce the partial gap. Main alternative: tax-unit/coverage errors and
transported spending/reporting assumptions overstate it. The discriminating
evidence is unused administrative earnings, receipts and beneficiary-cost cells,
not another broad narrative correlation. Freeze parameters before the check;
if they are then fitted to those cells, reserve a new holdout for validation.

Priority: IRS/SSA distribution first, updated transfer totals second, Medicaid
eligibility and public-school pupil counts third. Passing would strengthen the
resident fiscal account; causal policy savings and total welfare would still
need their own counterfactuals. [INFERENCE; FRAMING-SENSITIVE]

LLM-assisted source selection and interpretation follow the project's
[instrument caveat](../notes/llm-bias-caveat.md). Contrary facts and source-quality
limits are retained above. No inference of institutional deception is made from
ordinary missingness, revisions or modeling assumptions.

## Revisions

- 2026-09-19: [Executed the next checks](immigration-administrative-checks-2026-09-19.md).
  National earnings are close in dollars but differ in recipient/coverage
  distributions; transported benefit and pupil factors require refinement.
  The original test specification above is retained. No new ethnic total or
  causal policy estimate is claimed.
