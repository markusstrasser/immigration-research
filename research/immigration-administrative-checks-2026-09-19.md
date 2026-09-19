# Executed fiscal checks against administrative records

**September20 follow-up:** [Four executed checks](immigration-four-fiscal-checks-2026-09-20.md)
replace the school proxy and execute matched-year tax/health diagnostics. The IRS
paragraph below is retained as a historical extraction; its amounts reproduce
**Tax Year2022**, despite the source PDF's2023 heading. Use the successor's pinned
2023 SOI tables for a matched comparison.

**Verdict:** The first checks support a substantial receipt gap, while finding
specific weaknesses in the payroll and schooling assumptions. They do not
independently identify the Mexican-origin fiscal total. The existing annual
account remains an attributed, incomplete resident account, not a measured
admission/removal effect or a complete welfare balance. [INFERENCE]

Checked 2026-09-19. Income/prices2024; the population is the observed Mexican-origin
union of all ages, education levels and observed generations, 40.896574m civilian
household residents. Baselines were computed before recalibration. No IQ claim
or narrative essay is involved. LLM-assisted analysis can favor either the
operator's thesis or familiar institutional assumptions; the concrete controls
below, rather than either disposition, determine the verdict.

## Earnings and taxes

[SOURCE / CALCULATION] Reconstructed the canonical CPS2025 tax and earnings inputs,
preserving all160 replicate weights, then compared their national totals with
SSA's employer-record [2024 AWI underlying data](https://www.ssa.gov/oact/cola/awidevelop.html).
The latter reports175.073m wage recipients and $11,734.670bn aggregate net
compensation. SSA's [definition](https://www.ssa.gov/oact/cola/netcomp.html)
includes deferred-compensation contributions and excludes certain distributions;
it is not literally the same measure or resident universe as CPS wages.

| National quantity | Uncalibrated CPS model | SSA comparator | Raw difference |
|---|---:|---:|---:|
| Wage dollars | $11,998.978bn | $11,734.670bn | +2.25% |
| Wage recipients | 165.849m | 175.073m | −5.27% |
| OASDI taxable-base proxy, wages plus self-employment | $10,869.325bn | $10,170.185bn | +6.87% |

The third comparator is explicitly **preliminary**, based on BLS/BEA estimates
in [SSA Table4.B1](https://www.ssa.gov/policy/docs/statcomps/supplement/2025/4b.html),
not a completed administrative census. Our proxy treats wages as covered and
shares the Social Security cap between wages and net self-employment earnings;
actual exemptions, government employment, territories and other coverage
differences remain. It is a diagnostic, not a replacement for CPS FICA.

[INFERENCE] These results do not show massive aggregate wage undercoverage.
They also do not justify declaring the earnings distribution validated: too few
recipients alongside slightly higher total wages imply higher average wages in
the CPS universe. Aggregate agreement can conceal offsetting distribution errors.
The positive payroll-base discrepancy warrants a coverage adjustment before any
claim of precise payroll-tax measurement.

[CALCULATION] Under personal-source attribution, the observed Mexican-origin
union supplies **11.73% of wage recipients, 8.32% of wages, 4.74% of federal income
tax after refundable credits, and8.90% of CPS-plus-employer payroll contributions**,
against12.145% of the civilian population. Its amounts are19.450m wage recipients,
$998.728bn wages, $90.757bn federal income tax and$153.297bn payroll contributions.
These are survey/model allocations, **not administrative ethnic observations**.
Shared-family allocation is retained separately and must not be called a count
of ethnic wage earners.

The same personal-source extraction gives wages per wage recipient of
**$51,348 for the union versus$75,139 for other residents**. Federal income tax
after refundable credits per resident is$2,219 versus$6,171; payroll contributions
per resident are$3,748 versus$5,302. Lower earnings and progressive income taxes
are therefore observable parts of the modeled receipt gap, in addition to the
all-age denominator. This does not establish why earnings differ. [CALCULATION]

[HISTORICAL EXTRACTION; YEAR CORRECTED ABOVE] [Publication4801](https://www.irs.gov/pub/irs-pdf/p4801.pdf),
revision June2026, supplies a further federal-income-tax diagnostic. Its tax
liability after nonrefundable credits is$2,098.923bn, compared with CPS2024
FEDTAX_BC$1,981.110bn, a raw−5.61%. Different income years, tax units, nonfilers,
income concepts and credits prevent a validation verdict. A matched2023 tax-unit
distribution was not reconstructed in this pass. No residual is allocated to
Mexican origin merely because it exists nationally.

## Current transfer totals

[CALCULATION] Reconstructed every program in the existing underreporting
adjustment, matching all six canonical U totals: shared/personal allocation
times target/rest/national population. SNAP, Social Security, SSI and UI reporting
ratios were transported from income2017; correctly applying their arithmetic does
not establish that they still fit2024. The following are **raw national comparator
gaps**, not estimated pure reporting errors. Amounts are billions of dollars,
shared allocation and calendar2024 unless noted.

| Program | Before existing adjustment | After existing adjustment | Administrative comparator | Remaining raw gap |
|---|---:|---:|---:|---:|
| SNAP | 46.103 | 86.822 | 95.115 | −8.72% |
| Social Security | 1,254.671 | 1,365.208 | 1,449.964 | −5.85% |
| SSI | 58.673 | 57.582 | 63.079 | −8.72% |

[SOURCE] SNAP sums all twelve Jan–Dec2024 benefit-cost cells of the
[USDA monthly workbook](https://www.fns.usda.gov/sites/default/files/resource-files/snap-4fymonthly-9.xlsx),
release September11,2026. Its fiscal2024 total$93.836bn was not substituted.
Benefits exclude administration but include territorial programs; their removal
is unresolved. Social Security subtracts territories, foreign countries and
unknown geography from [SSA Table5.J1](https://www.ssa.gov/policy/docs/statcomps/supplement/2025/5j.html),
leaving50states/DC. It still includes institutional recipients and people who
died before the CPS2025 interview. No adjustment for these groups is fabricated.

[SOURCE] SSI's$63.079bn is [SSA2024 Statistical Report Table2](https://www.ssa.gov/policy/docs/statcomps/ssi_asr/2024/sect01.html):
federal plus federally administered state supplements, assigned by month due and
net of recoveries. State-administered supplements are excluded. The near-identical
[SSA federal-only payment-date total](https://www.ssa.gov/oact/ssir/SSI25/IV_C_Payments.html)
is a different concept; numerical proximity does not reconcile them. The existing
BEA workbook gives a broader federal/state SSI comparator$65.134bn. It is retained
as a separate sensitivity and explicitly marked common-source reuse.

[CHECK] No SNAP duplication bug was found. The canonical estimate takes one
benefit per SPM unit before allocation; wrongly summing its repetition on every
person would produce$150.181bn. Unique-head weighting and current equal-member,
person-weighted allocation produce different estimates, $44.425bn/$46.103bn.
That weighting difference is preserved, not hidden by normalization.

[SCENARIO] Replace each historical multiplier with
`admin total / original national program amount`, separately by allocation;
retain modeled group shares. SNAP plus domestic Social Security alone makes the
target balance **$4.94bn shared/$6.06bn personal more negative**. Adding the two
SSI comparator alternatives yields **$5.39–5.56bn shared/$6.51–6.68bn personal**
more negative. Resulting balances are about−$239.7–239.9bn shared and
−$262.8–262.9bn personal, relative to−$234.34bn/−$256.26bn baselines.
These are conditional recalibrations, not confidence intervals or identified
missing Mexican-origin payments. The broader administrative boundary is assumed
onto the household survey for this scenario; it is not empirically allocated.

[DISCONFIRMATION] UI points in the opposite direction: its historical adjustment
raises shared national benefits from$25.061bn to$43.434bn, above BEA$36.468bn.
Direct DOL program matching was not completed, so UI is excluded from the new
rakes. PAW_VAL likewise includes assistance beyond TANF; a block-grant total is
not a matched cash-payment target. Neither UI nor TANF is silently treated as
having passed. Medicaid eligibility-cost matching and same-year IRS distribution
validation also remain outside this completed pass.

## Pupil counts and education charges

[CALCULATION] The model applies one public-pupil factor, **80.270%**, to children
aged5–17. It came from public-pupil/child exposure allocated to native adults in
ACS2024 households. Direct, previously unused child/state cells in the same ACS
instead give **81.505% nationally, 86.701% for Hispanic children, and about85% in
California and Texas overall**. This is a test of transporting an estimated
ratio, not a wholly independent data source.

| Public K–12 pupils aged5–17 | CPS model, millions | Direct ACS2024, millions | Model shortfall |
|---|---:|---:|---:|
| US, all | 43.728 | 44.363 | 1.43% |
| US, Hispanic | 11.590 | 12.516 | 7.40% |
| California, all | 4.906 | 5.371 | 8.66% |
| California, Hispanic | 2.506 | 2.936 | 14.66% |
| Texas, all | 4.426 | 4.834 | 8.45% |
| Texas, Hispanic | 2.117 | 2.449 | 13.54% |

These differences combine the fixed attendance factor with survey population
and timing differences: March2025 CPS versus annual-average2024 ACS households.
They should not be relabeled pure nonresponse errors. Both surveys' replicate
standard errors are exported; the attendance factor is held fixed and its
estimation uncertainty is not included. Hispanic is not the full Mexican-origin
union. [MEASUREMENT LIMIT]

[SOURCE / CALCULATION] A second bridge checks the ACS count against **administrative
grade membership**, with all K–12 ages retained on both sides. California ACS
has5.674m, compared with CDE5.686m in2023–24 or5.629m in2024–25 after excluding
transitional kindergarten: differences−0.22%/+0.80%.
[CDE grade table](https://www.cde.ca.gov/ds/ad/cefenrollmentcomp.asp).
Texas ACS has5.144m against TEA5.256m K–12, −2.14%; its Hispanic count is2.608m
against2.775m, −6.01%, after removing early education/pre-K.
[TEA2023–24, Tables10/12](https://tea.texas.gov/reports-and-data/school-performance/accountability-research/enroll-2023-24.pdf).
Fall membership, annual-average attendance, household/group-quarter coverage and
TK reporting can differ. These are useful proximity checks, not exact equality
tests or administrative counts of Mexican descendants.

The ACS extract also counts **2.618m public K–12 pupils outside ages5–17**
nationally, including0.796m Hispanic pupils. They are outside this model's direct
pupil charge and the rate-only scenarios below. The school component therefore
remains incomplete even after replacing its attendance factor. No Mexican-origin
amount is imputed from the broader Hispanic count. [CALCULATION / COVERAGE]

[SCENARIO] Replacing the model factor uniformly with the direct all-child share
raises attributed schooling costs by **$2.17bn shared/$2.28bn personal**. Using
the Hispanic share as a deliberately broad proxy raises them by **$11.32bn/$11.86bn**.
Both apply the factor consistently to school operating costs, capital/interest
and district differentials; existing school-lunch overlap removal stays fixed.
Neither is a calibrated ethnic correction or a confidence bound. The exercise
shows that more realistic pupil exposure can increase the fiscal deficit; the
baseline was not automatically constructed to maximize it.

[CHECK] All9,373 sampled Texas civilian records have exactly zero STATETAX_A,
as expected for the held tax model. Federal/payroll and other tax contributions
remain. This passes the narrow no-state-personal-income-tax check; it does not
reconcile Texas's entire revenue system or establish an ethnic net balance.

## Reproduction and interpretation

The [tax generator](../infra/immigration-fiscal/admin_tax_checks_2026_09_19/README.md),
[transfer generator](../infra/immigration-fiscal/admin_transfer_checks_2026_09_19/README.md)
and [school generator](../infra/immigration-fiscal/admin_school_checks_2026_09_19/README.md)
pin sources and administrative transcriptions, export component/count and
sensitivity tables, and leave the current fiscal account unchanged. New checks
are evaluated on the unadjusted baseline; a sensitivity's forced agreement with
its target is never counted as an independent pass.

All three complete builds and11 boundary/accounting tests pass. Source tax and
employer amounts, group partitions, existing U adjustments, calendar-month
coverage and replacement-rake identities reproduce. The native read-only review
covers the new code; this is not an external econometric replication.

[INFERENCE] Better computation can improve specific published methods when it
uses better data, fixes an identified error or predicts unused observations more
accurately. This pass demonstrates component checks and a pupil-rate transport
weakness. It does not benchmark GPT6 against economists, establish a general
intelligence ranking, or turn descriptive origin correlations into causal effects.
The live question is how well each construction survives the same controls.

## Follow-up, 2026-09-19

The [gap diagnosis and data check](immigration-gap-diagnosis-and-data-2026-09-19.md)
decomposes the school discrepancy, resolves the small SNAP territorial component
using a separate matched administrative series, and identifies usable public
enrollment, tax and health checks. The baseline and conditional rakes above are
unchanged; unresolved residuals are not relabeled ethnic reporting errors.

## Revisions

2026-09-20: [Measured enrollment and residual boundaries](../decisions/2026-09-20-measured-enrollment-and-residual-boundaries.md)
replaces the school proxy and executes matched-year tax checks. The old IRS
amounts reproduce2022, not2023; source metadata is repaired while the historical
diagnostic remains visible. No national tax residual is assigned proportionally.
