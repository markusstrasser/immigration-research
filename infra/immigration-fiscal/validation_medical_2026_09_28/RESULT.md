**Verdict:** The new 2022 MCBS check does not reproduce the large 2023 discrepancy,
although it is too imprecise to exclude it. The 2023 difference survives age/sex
standardization and an analogue of MCBS disclosure top-coding; 85% of its arithmetic
decomposition is Medicare. Public files do not identify the remaining cause. No
Mexican-specific fiscal correction is justified by these all-Hispanic comparisons.

## Scope and evidence

The cross-survey quantity is mean annual Medicare-plus-Medicaid service payments per
Medicare-ever beneficiary aged 65+, Hispanic divided by non-Hispanic white. It is not
spending per covered month, all public medical spending, the Mexican-origin transport
ratio, or the cost of immigration. Means are nominal dollars within each year; the
retrospective pooled prediction uses medical CPI to put MEPS dollars in 2024 prices.
The reproduced MEPS baseline retains its original valid-donor restriction to known
US/foreign birth; releasing that restriction changes the 2023 ratio only from .845
to .843 (449 Hispanic and 3,197 NH-white records), so this small exclusion does not
explain the gap. This extra diagnostic was added after the main scoring pass. [CALCULATION]
This is a measurement-validation exercise; no model parameter changes. [FRAMING-SENSITIVE]

Executed source: [analysis.py](analysis.py). Every numerical result below is a
[CALCULATION] from its `derived/diagnostics.csv`, `cross_survey_gaps.csv`,
`payer_decomposition.csv` or `retrospective_2024.csv`; raw file and source-code SHA-256
values are retained in `derived/audit.json`. [Design.md](Design.md) was saved before new
scoring. Baseline 2023 ratios were already known. The 2022 MCBS data were acquired after
the new-year comparison was specified. All 2024 MEPS observations had already appeared
in previous project analyses, so the 2024 check is retrospective, not a fresh prospective test.

## 1. The previously unused 2022 MCBS cost file

| Year | MEPS ratio (SE) | MCBS ratio (SE) | MCBS minus MEPS (SE) |
|---|---:|---:|---:|
| **2022, new external check** | **1.009 (.109)** | **1.114 (.151)** | **+.106 (.186)** |
| 2023, reproduced | .845 (.089) | 1.265 (.152) | +.420 (.177) |

The 2022 difference has a 95% normal interval of approximately −.259 to +.470;
the 2023 difference is +.074 to +.766. The new point estimate is much closer, but
its interval still contains the old discrepancy. Thus it does not establish that
there is no instrument difference or that the difference changed significantly.
MCBS2022 and MCBS2023 can share respondents and cannot be linked through PUF IDs;
we do not treat their results as independent year-to-year observations. Within each
year the cross-survey SE assumes independent MEPS and MCBS samples. [INFERENCE]

The new CMS2022 file contains 6,621 people; its age and race category counts reproduce
the official codebook exactly. At 65+, the comparison uses 543 Hispanic and 4,281
NH-white records in MCBS2022, and 545 and 3,600 in MEPS2022. It is a new external
measurement check, not a held-out forecast of a Mexican-origin population. [DATA]

## 2. Which payer produces the 2023 disagreement?

| Survey | Hispanic Medicare | White Medicare | Hispanic Medicaid | White Medicaid |
|---|---:|---:|---:|---:|
| MEPS2023 | $7,285 | $9,994 | $1,405 | $284 |
| MCBS2023 | $13,258 | $12,102 | $2,379 | $260 |

These are dollars per person in the common nominal-year domain, including zero
payments. Both surveys show much higher Hispanic Medicaid spending relative to
NH-white spending. They disagree sharply on Medicare: ratios .729 (.076) and
1.096 (.124). This argues against treating the entire discrepancy as Medicaid
enrollment or Medicaid reimbursement error. [INFERENCE]

For each survey, the exact identity is
`ratio − 1 = (Hispanic Medicare − white Medicare)/white public total +
(Hispanic Medicaid − white Medicaid)/white public total`.
The between-survey difference .419534 decomposes into **.357178 Medicare (85.1%)**
and **.062357 Medicaid (14.9%)**. This is an arithmetic attribution of the disagreement,
not causal identification of a reporting defect. [CALCULATION]

## 3. Tested explanations for 2023

| Diagnostic | MEPS ratio (SE) | MCBS ratio (SE) | Remaining point gap |
|---|---:|---:|---:|
| Raw aligned payer/age/Medicare-ever definitions | .845 (.089) | 1.265 (.152) | .420 |
| Common uniform age-sex distribution | .870 (.090) | 1.244 (.142) | .374 |
| MEPS with CMS-style tail-mean analogue | .854 (.087) | 1.265 (.152) | .411 |
| Both surveys additionally capped at payer p99.5 | .861 (.085) | 1.175 (.122) | .314 |
| Both surveys additionally capped at payer p99 | .864 (.084) | 1.156 (.111) | .293 |

The fixed standard population gives one quarter of its weight to each of 65–74 male,
65–74 female, 75+ male and 75+ female. It is hypothetical, used identically in both
surveys; all cells have at least 62 Hispanic observations. The result removes about
11% of the point gap. This refutes a simple explanation entirely in terms of those
four demographic shares, while leaving finer age, health and income composition open.
[CALCULATION; INFERENCE]

**Top-coding is not ordinary winsorization.** CMS replaces the highest unweighted
0.5% of each payer/service variable with that tail's mean. We applied this rule to
MEPS Medicare and Medicaid over valid Medicare-ever respondents, including under-65
beneficiaries, before estimating the 65+ ratio. It moves the estimate only .009.
The public MCBS payer components have already been disclosure-treated separately;
MEPS cannot replicate their unknown raw tails or split its total Medicare into the
same fee-for-service/MA components. The additional capped-tail rows change the
estimand and report SEs conditional on estimated caps; they reduce, but do not remove,
the point discrepancy. [SOURCE: CMS Microdata PUF User Guide §3.4; CALCULATION]

**Income is informative but not fully aligned.** Below $25,000, the MCBS ratio is
1.538 (.263), versus .704 (.112) above that threshold. MEPS using its full family
income gives .914 (.131) and .752 (.100), respectively. CMS defines its income
concept as the beneficiary's and spouse's income; MEPS family income can include
other relatives. These cuts consequently do not prove that income composition
explains the gap. In particular, the high-income results agree much more closely,
but that does not identify the low-income discrepancy. [SOURCE: CMS income FAQ;
MEPS HC-251 family-income variable; CALCULATION; INFERENCE]

**MA payment-positive and enrolled are different conditions.** The MCBS ratio is
1.210 (.155) among people with MA payments and 1.165 (.280) among people without
them. MEPS is .972 (.096) among people reporting MA in any observed round and
.479 (.159) among people consistently observed as not managed-care, with at least
one Medicare-covered round. Medicare-ever people with incomplete/ambiguous round
coverage remain in the raw estimate and are excluded only from the latter proxy.
Among Hispanic beneficiaries, these MEPS proxies cover 69.6% and 15.0%; their sum
is below 100%. MCBS payment-positive covers 62.8%. These are not comparable exact
FFS/MA strata and do not identify an MA adjustment. [CALCULATION]

The CMS guide states that PUF payments include adjustment for Medicare-covered days
outside interview reference periods, and upward adjustment of MA non-drug utilization
and expenditure. The PUF supplies no unadjusted amounts or enrollment months.
MEPS payments combine household and provider data with imputation, so the earlier
shorthand “household reports versus administrative claims” is incomplete. Neither
PAMTMADV nor MEPS TOTMCR should be equated with government capitation remittances
to plans: these files summarize service payments under different collection and
adjustment procedures. [SOURCE: CMS guide §3.3; AHRQ HC-251 §B.2 and HC-233 §2.5.11;
INFERENCE]

**Population remains imperfectly aligned.** The 2023 eligible samples represent
5.503m Hispanic and 43.372m NH-white people in MEPS, versus 4.342m and 42.382m in
MCBS. The MCBS PUF excludes anyone with a facility interview or any facility,
hospice or institutional event/cost in the year. MEPS's civilian noninstitutional
population definition does not supply the identical exclusion. Medicare-ever
matching does not equal person-month exposure matching. Exact region, country of
origin, health burden and institutional-use alignment are unavailable in these PUFs;
these remain unidentified mechanisms, not known directions of bias. [DATA; SOURCE:
CMS guide §3.3; INFERENCE]

## 4. Retrospective 2024 MEPS prediction

Freeze 2016–2023 pooled ratios and predict 2024; compare with simply repeating 2023.
Use the common HC-036 PSU structure for the prediction-minus-observed SE, preserving
covariance from shared respondents and sampling units. [CALCULATION]

| 65+ target/reference; payer | Pooled prediction | 2024 observed | Pooled error (SE) | Repeat-2023 error |
|---|---:|---:|---:|---:|
| Hispanic/NH-white; Medicare | .862 | .836 | +.026 (.101) | −.107 |
| Hispanic/NH-white; Medicaid | 5.219 | 3.181 | +2.038 (.961) | +1.768 |
| Hispanic/NH-white; Medicare+Medicaid | 1.021 | .903 | +.118 (.106) | −.057 |
| Mexican/all valid donors; Medicare | .778 | .874 | −.096 (.142) | −.226 |
| Mexican/all valid donors; Medicaid | 1.906 | 1.834 | +.073 (.371) | +.281 |
| Mexican/all valid donors; Medicare+Medicaid | .850 | .924 | −.074 (.137) | −.202 |

The Mexican/all-donor comparison includes all valid 65+ donors, as in the existing
transport audit; the Hispanic/NH-white comparison additionally requires Medicare-ever.
Pooling improves absolute error in four of six overlapping outcomes. It worsens two
Hispanic outcomes, including the aggregate payer ratio, and overpredicts the Hispanic
Medicaid ratio by about 2.1 SE. The six outcomes are correlated, not six independent
tests. These mixed results argue for keeping payer-specific uncertainty instead of
using a stable pooled total as proof of stable components. [INFERENCE]

## Retained, corrected, unresolved

- **Retained:** age/nativity/ethnicity-specific MEPS modeling and the need to distinguish
  coverage from dollars; no evidence here supports a blanket adverse ethnicity multiplier.
- **Corrected:** the 2023 discrepancy is primarily Medicare in the arithmetic sense;
  age/sex mix and disclosure top-coding do not account for most of it. MCBS tail coding
  is tail-mean substitution, and MEPS is not solely household-reported expenditure.
- **New disconfirmation:** 2022's point gap is substantially smaller, without proving
  equality; pooled training does not beat a last-year prediction on every medical outcome.
- **Unresolved:** fine population, exposure, payer measurement and MA adjustment
  differences; Mexican-specific external claims validation; full national fiscal-model
  validation. No new dollar correction is applied to the $322–387bn model. [INFERENCE]

## Primary sources

- [CMS official dataset and year-specific downloads](https://catalog.data.gov/dataset/medicare-current-beneficiary-survey-cost-supplement).
- [CMS 2022 codebook](https://data.cms.gov/sites/default/files/2025-01/CSPUF2022_Codebook.txt).
- [CMS PUF methodology package](https://data.cms.gov/sites/default/files/2026-01/2023%20Cost%20Supplement%20Methodology.zip),
  local `fiscal_access_2026_09_20/_cache/methodology/MCBSMicrodataPUFDataUsersGuide.pdf`,
  §§3.3, 3.4, 7.1 (facility exclusion, adjustments, tail treatment and Fay BRR).
- [CMS income definitions](https://data.cms.gov/medicare-current-beneficiary-survey-mcbs/income-and-asset-ownership).
- [MEPS HC-251 documentation](https://meps.ahrq.gov/data_stats/download_data/pufs/h251/h251doc.pdf)
  and [HC-233 expenditure documentation](https://meps.ahrq.gov/data_stats/download_data/pufs/h233/h233doc.pdf).

This analysis was produced with an LLM; framing and interpretation require the same
skepticism as the model under examination. Empirical results are traceable to code and
primary files, rather than the language model's prior expectations. [INFERENCE]
