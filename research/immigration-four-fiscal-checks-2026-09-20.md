# Four executed fiscal checks and the revised annual account

**Verdict:** Actual public-school enrollment raises the modeled Mexican-origin
annual deficit by **$25.04bn shared / $26.94bn personal**. The revised partial
balances are **−$259.38bn / −$283.20bn**. National coverage, tax and healthcare
checks identify important remaining measurement limits; they do not justify
assigning national residuals to this population. [CALCULATION / INFERENCE]

This is the executed follow-up to the [gap diagnosis](immigration-gap-diagnosis-and-data-2026-09-19.md).
It covers the existing observed Mexican-origin union, **40.896574 million**
civilian household residents of all ages and education levels. Its observable
generation categories do not recover all distant ancestry. These are annual
attributed fiscal balances in 2024 dollars, not a low-skill-only account, an
estimate of policy savings, or a complete social cost-benefit calculation.
Negative numbers mean receipts minus attributed spending is negative.

## Current annual version

| Allocation | Receipts, $bn | Spending, $bn | Revised balance, $bn | Change from September 19 finance version, $bn |
|---|---:|---:|---:|---:|
| Household sharing | 444.422 | 703.801 | **−259.379** | −25.040 |
| Personal source | 422.914 | 706.114 | **−283.200** | −26.937 |

[CALCULATION: school lane `derived/updated_account_components.csv` and
`annual_balance.csv`, primary `all_ages` construction.] Receipts include the
existing mapped service fees. Only school operating, capital/interest and
district-differential costs change; the school-lunch reversal remains fixed.
The two rows are attribution conventions, not confidence bounds. No national
tax or medical-spending residual is inserted as an ethnic correction.

The [September 19 finance version](immigration-macro-reconciliation-2026-09-19.md)
remains the preceding annual release. Existing [lifetime profiles](immigration-yearly-lifetime-cost-repair-2026-09-19.md)
retain their earlier component and age-profile vintage: multiplying this annual
change by a lifespan would not update them correctly.

## School enrollment: a measured correction with a transport assumption

[SOURCE / CALCULATION] The [October 2024 CPS supplement](https://www.census.gov/data/datasets/2024/demo/cps/cps-school-enrollment.html)
contains actual public/private school and grade responses. The two child/adult
question branches yield **47.954m public K–12 pupils nationally**, including
**8.634m** in the canonical observed Mexican-origin target. Of the latter,
0.485m are outside ages 5–17. The construction agrees with Census's combined
enrollment recode and all 161 published weight controls.

The previous calculation applied a uniform **80.27%** factor to ages 5–17.
Measured October rates are transported by age/origin cells to the March 2025
ASEC population. These are different surveys/months, not linked pupils. Measured
origin-specific rates are used where supported; sparse younger/older cells are
pooled. Existing state average-cost schedules are retained. The resulting
target exposure rises from **7.181m to 8.487m** expected pupils. Direct October
counts and transported ASEC exposure are distinct quantities.

| Enrollment construction | Shared target balance, $bn | Personal target balance, $bn |
|---|---:|---:|
| Old uniform factor | −234.339 | −256.263 |
| Measured rates, ages 5–17 only | −250.946 | −274.138 |
| Measured rates, grades K–12 at ages 3–24 | −258.819 | −282.665 |
| Measured rates, all reported K–12 ages; primary | **−259.379** | **−283.200** |
| Pool origins within age; all ages | −249.628 | −272.422 |

[MODEL OUTPUT / SENSITIVITY] Roughly two-thirds of the primary correction is
better enrollment rates inside ages 5–17; the remainder adds enrolled pupils
outside that range. Pooling origin rates discards a measured difference and is
shown as a transport sensitivity. Removing age 25+ changes the result by only
$0.56bn/$0.54bn, addressing the weaker fit of older students to standard K–12
costs. None of these rows estimates marginal school costs of immigration.

[DISCONFIRMATION] Rates fitted **excluding both California and Texas** predict
target pupil counts with residuals of +17k/+27k, against residual sampling SEs
of 69k/59k. Texas's other-resident pupils are underpredicted by 154k (SE69k).
The direct national count exceeds unused ACS2024 comparison cells by 0.973m;
Texas Hispanic pupils fall 330k below the lagged TEA2023–24 control. Survey
timing, grades and universes differ; these discrepancies remain unresolved.
Hispanic administrative counts do not identify Mexican-origin pupils.

All 160 October replicate rates and 160 March exposure replicates are propagated.
Because sample overlap leaves their covariance unknown, the sum-of-SE upper
envelope is **$2.12bn shared/$2.26bn personal for this correction**. That excludes
transport and cost uncertainty and is not the SE of the whole fiscal balance.
See [implementation, source lock and checks](../infra/immigration-fiscal/school_enrollment_2026_09_20/README.md).

## National accounting: locate omissions before allocating them

[SOURCE / CALCULATION] The [national coverage execution](immigration-national-coverage-execution-2026-09-20.md)
exhaustively partitions the earlier finance-version receipt discrepancy against
BEA2024 accounts. Important positive BEA-minus-model differences include
**$312bn general sales taxes**, **$357bn property taxes** and **$385bn federal
personal income taxes**, plus separately identified premiums, licenses, tariffs,
asset income and transfers. Broader business/property bases and timing prevent
treating these as pure missing household payments.

Moving modeled refundable credits from negative receipts to spending raises
both sides by $65–67bn nationally and changes neither balance. The existing
defense/interest/general-government allocation alternative would add about
**$1.74tn nationally**. Seven other zeroed functions have gross pools of about
$321bn, but their unresolved grant overlap with existing state/local services
prevents counting them as additional expenditure. This locates explicit
conventions but mixes FY source pools
with a CY current-account benchmark; it is not an exact expenditure reconciliation.

[LIMIT] The remaining national expenditure difference in that bridge is
$1.55–1.57tn before the new school correction, and the receipt difference about
$2.00–2.07tn. This release's school revision separately increases national modeled
spending by $95.73bn/$98.60bn. Coverage, institutions, capital, survey universes,
and timing still prevent a complete closure. Public-good and business-tax
incidence cannot be inferred from population share alone.

## Matched-year taxes: the residual is concentrated, not proportional

[SOURCE / CALCULATION] Income-2023 CPS ASEC 2024 is compared with the
[2023 IRS detailed tables](https://www.irs.gov/pub/irs-soi/23in12ms.xls) and
[SSA employer-record compensation](https://www.ssa.gov/oact/cola/awidevelop.html).
Native CPS tax-unit IDs and tax carriers preserve every tax dollar; dependent
filers remain separate. These are modeled filings, not linked IRS observations.

| Income-2023 national comparison | CPS | Administrative comparator | Raw difference |
|---|---:|---:|---:|
| Wages / W-2 net compensation, $bn | 11,105.609 | 11,103.241 | +0.021% |
| Annual wage recipients, millions | 163.093 | 173.671 | −6.091% |
| OASDI wage-base proxy, $bn | 9,779.053 | 9,290.622 | +5.257% |
| HI wage-base proxy, $bn | 11,105.609 | 11,254.976 | −1.327% |
| Income tax before refundable credits, $bn | 1,819.018 | 2,108.587 | −13.733% |

The income-tax gap is **−$489.776bn at AGI $500,000+**, offset by **+$200.207bn
below $500,000**. The total −$289.569bn therefore does not support a uniform
ethnic tax multiplier. Tax modeling, income reporting, disclosure treatment,
filing construction and remaining scope could all contribute; their separate
causal shares are not identified. SSA state-table comparisons remove territories
and other/unknown geography; AWI remains all-area. Institutional/military and
annual-survivor boundaries, compensation definitions and payroll exemptions
still differ. [CALCULATION / LIMIT]

[SOURCE CORRECTION] The old IRS $9,738.951bn wage/$2,098.923bn tax anchors
reproduce the detailed **2022** tables exactly, despite their2023 heading in
Publication 4801. The new2023 sources give $10,204.096bn wages/$2,108.587bn tax.
The old metadata is corrected and the original diagnostic preserved. This is
an internal publication inconsistency, not evidence of intent.

[DISCONFIRMATION] With a common civilian-household definition, ACS2024 and
CPS2025 give Mexican-self-ID/complement wages-per-earner ratios **0.692 and
0.687**, respectively. Absolute earnings differ for both groups; the relative
gap is similar. The Mexico-born ratios differ more, **0.685 versus0.646**, so
corroboration is not universal. ACS lacks parental birthplace and uses rolling
annual income; it cannot validate the whole CPS ancestry union. All replicate
weights are retained. See [tax results, uncertainties and source proof](../infra/immigration-fiscal/same_year_tax_2026_09_20/README.md).

## Healthcare: better scope checks, no supported group adjustment

[SOURCE / CALCULATION] The public CMS per-capita data's latest comparison year
is **2023**; this diagnostic therefore uses MEPS2023 and CPS ASEC2024 rather
than relabeling the current2024 account. The [CMS national profile, page15](https://www.medicaid.gov/medicaid/quality-of-care/downloads/beneficiary-profile-2026.pdf)
reports $877.2bn Medicaid spending and94.0m member-years. Direct MEPS spending
is $278.156bn, or **$429.250bn after the inherited1.5432 multiplier**. The
remaining **$447.950bn** is a mixed-scope national difference, not missing
Mexican-origin expenditure.

The coverage denominator matters: MEPS has81.353m people ever covered but69.585m
member-years. Using the latter raises spending per enrolled year by16.91%, to
$6,169 after the multiplier. This fixes the diagnostic denominator; it does not
increase annual spending dollars. Administrative figures include institutions,
territories and Medicare premiums; MEPS includes CHIP, excludes institutions
and measures service payments. Exact state eligibility expenditures/member-months
are not exposed by the retrieved CMS API. Age groups are not substituted for
disability or ACA eligibility. [MEASUREMENT LIMIT]

[DISCONFIRMATION / SCALE TEST] Published2023 institutional LTSS is only about
$82.74bn. Subtracting it from the CMS comparator, net of the small DSH overlap,
still leaves **$365.27bn** relative to calibrated MEPS. Even subtracting **all
published LTSS**, including home-care spending that overlaps MEPS, leaves
**$219.36bn**. These are scale stresses, not hard lower bounds: LTSS encounters
and CMS cash payments differ, and California HCBS data have high concern flags.
Institutions alone are consequently not an adequate demonstrated reconciliation.

Managed-care payments cannot simply be removed from CMS: MEPS already imputes
the services they finance. The missing comparison is capitation versus
comparable services, including overhead, retained amounts and timing. The
existing historical multiplier remains an assumption rather than an
administratively validated current adjustment. The [health results and source
boundaries](../infra/immigration-fiscal/health_admin_2026_09_20/RESULT.md) retain
all five observed eligibility rates and the California/Texas transport checks.
No national healthcare residual is assigned to the target population.

The direct MEPS total includes141 records with unavailable end-year age,
representing $9.228bn raw spending. Their explicit residual now reconciles the
reported age totals; the canonical donor cells still exclude them. This is a
declared donor-versus-national population difference, not an automatic amount
to add to current household residents. The reconstructed CPS diagnostic now
also preserves the prior-year newborn exclusion and canonical civilian/origin
boundaries. [CODE TRACE / CALCULATION]

## Interpretation and reproducibility

[INFERENCE] The school check strengthens the conclusion that the previous
partial account understated this group's school exposure. It does not validate
all other components. A negative partial balance remains the measured model
result; the complete national-account attribution and the effect of an
immigration-policy change remain separate, unresolved questions.

Executed: all four generators in the main repository (including the separate
ACS run), **28 focused tests**, source/output fingerprints, school component
replacement and receipt-minus-spending checks, independent review by authors
of other lanes, and the fiscal dependency doctor. Review removed the gross-grant
addition from the national bridge and repaired the healthcare exposure/domain
boundaries. Raw data and generated tables remain ignored; sources, scripts and
calculation notes are retained. See the [decision record](../decisions/2026-09-20-measured-enrollment-and-residual-boundaries.md).

The LLM instrument caveat applies to source choice and interpretation. Source
tables, explicit units, held-out discrepancies and reproducible arithmetic take
precedence over whether a revision agrees with the expected conclusion.
