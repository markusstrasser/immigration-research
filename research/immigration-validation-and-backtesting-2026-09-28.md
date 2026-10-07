# What has been validated, and what can be back-tested?

**Verdict:** Several important inputs are independently corroborated. Four further
checks now produce a mixed result: demographic profiles help predict some later
fiscal shares; school adjustment depends on the population and score; medical
disagreement survives several attempted explanations; and the new joint Mariel
budget loses to its simple baseline. We have **not** independently back-tested the
complete national counterfactual. The evidence is stronger for selected observed
components than for spending responses, lifetime projections or the complete total.
[CALCULATION / INFERENCE: executed checks in section 3]

September 28, 2026. Validation audit, following the [conceptual audit](immigration-adversarial-audit-2026-09-28.md).
The current object is the September 27 account's **$321.8–387.4bn annual conditional
net cost to other US residents**, including imputed public-capital services. Its
broader component sensitivity is **$258.6–436.1bn**; neither band is an empirically
validated confidence interval. It concerns the observed Mexican-origin resident
union, including US-born descendants, not all immigrants or a specified admission
policy. [CALCULATION: [current case](../infra/immigration-fiscal/main_case_long_run_2026_09_27/RESULT.md)]
[2026-09-29: the main case is now the September 29 case, $371.4–434.8bn (ladder 275,
[lane](../infra/immigration-fiscal/main_case_2026_09_29/RESULT.md)); this audit's checks were run on the
September 27 case.] [2026-10-05: the main case is now the October 5 case, $390.3–461.2bn, which counts the descendants who no
longer report Mexican origin (ladder 281, [lane](../infra/immigration-fiscal/main_case_2026_10_05/RESULT.md)).]
[2026-10-07: the main case is now the October 7 case, $389.1–461.5bn: the October 5 case with the pension accrual on the
2026 Trustees and separate funds, retiree health on accrual, the added descendants at their measured ages, and user fees
with the education keys (ladder 295, [lane](../infra/immigration-fiscal/main_case_2026_10_07/RESULT.md)).]

## 1. The useful cross-references we already have

These are results of the earlier checks, before their subsequent use in calibration.
Dollar amounts from different account vintages are not combined here.

| Quantity checked | Actual comparison | Interpretation |
|---|---|---|
| Relative earnings, two surveys | For civilian household residents with positive wages, Mexican self-ID / other-self-ID mean earnings is **0.6919 in ACS2024 and 0.6866 in CPS2025**. Sampling intervals: .6867–.6972 and .6649–.7082. | Strong descriptive corroboration of an important tax-capacity input. Absolute earnings differ; Mexico-born ratios agree less closely (.6851/.6458). Neither survey identifies the full target union equally or establishes why earnings differ. |
| National wages, administrative records | Income2023 CPS wages **$11,105.6bn** versus SSA compensation **$11,103.2bn**, a **+0.021%** difference. Income2024 comparison: **+2.25%**. | The overall wage scale is plausible. CPS wage-recipient counts are lower by 6.09%/5.27%; totals can agree while the distribution is wrong. Coverage and compensation definitions differ. |
| School enrollment transport | Rates fitted excluding **both California and Texas** predicted their Mexican-origin pupil counts with residuals **+17k/+27k**, versus sampling SEs **69k/59k**. | A real geographic transport check. Texas other-resident pupils were underpredicted by 154k (SE69k), and administrative Hispanic counts still disagree. This checks pupil exposure, not spending avoidability. |
| SNAP benefit allocation | California FY2024 Hispanic benefit-dollar share: **43.989% administrative QC versus 44.078% CPS**. | Useful local agreement, not proof of national ethnic accuracy. Unknown/coding problems invalidate many other states' ethnic comparisons; the administrative point estimate includes a treatment of unknown ethnicity. Hispanic is not Mexican-origin. |
| Federal tax distribution | Income2023 modeled federal income tax before refundable credits is **13.73% below IRS**. The shortfall above $500k AGI is $489.8bn, partly offset by $200.2bn excess below it. | A failed distribution check. Applying the national discrepancy proportionally to Mexican-origin taxes is unsupported. Later income-gradient corrections address this class of discrepancy [2026-09-28 (ladder 249): below $1M only; across all 19 bins the final key still misses IRS 2023 by 23.5pp, 8.4pp with $1M+ pooled, against 2.4pp for frozen IRS shares]; matching the same target afterward is calibration. |

[DATA / CALCULATION: [matched-year taxes and survey earnings](../infra/immigration-fiscal/same_year_tax_2026_09_20/README.md),
[2024 administrative checks](immigration-administrative-checks-2026-09-19.md),
[school transport](immigration-four-fiscal-checks-2026-09-20.md),
[administrative benefit shares](../infra/immigration-fiscal/admin_benefit_keys_2026_09_24/RESULT.md).
Primary administrative source: [SSA wage records](https://www.ssa.gov/oact/cola/awidevelop.html),
rechecked September 28; IRS year-specific tables are pinned in the tax lane.]

The school-price comparison is also reassuring within its scope: district/school
location raised the **already state-priced** group school cost by about **3.4%**.
This is a modest allocation correction. It does not validate charging full average
cost as a long-run response. [CALCULATION: [outside checks](immigration-outside-checks-2026-09-24.md)]

**Healthcare has a live disagreement.** For age65+, Medicare-ever beneficiaries,
Hispanic versus non-Hispanic-white Medicare-plus-Medicaid spending, payer/age-aligned MEPS2023
gives **0.845 (SE .089)** and MCBS2023 **1.265 (.152)**. Pooling MEPS2016–24 gives
**1.005 (.056)**. **Correction after the deeper check:** the population exclusions
are not identical. MCBS excludes anyone with a facility interview or any facility,
hospice or institutional event/cost; MEPS's civilian noninstitutional population
does not impose the identical rule. We cannot rule out that channel from these
public files. Coverage-count agreement with Medicaid records cannot validate
medical dollars. [DATA: [earlier reconciliation](../infra/immigration-fiscal/medical_ethnicity_pooled_2026_09_23/RESULT.md#7-65-mcbs-nursing-facilities-and-institutions);
SOURCE / CALCULATION: [new definition audit](../infra/immigration-fiscal/validation_medical_2026_09_28/RESULT.md)]

## 2. What is genuinely back-testable?

**Observed component levels:** yes. Freeze a model using earlier years, then predict
later earnings distributions, tax liabilities, pupil counts, benefit shares and
costs by beneficiary type. A conditional prediction may use later population
composition or enacted tax rules, but it must say so: that tests allocation or
transport, not an unconditional forecast. Compare with a simple frozen-share or
population-proportional baseline. Section 3 now executes this for selected fiscal
components. [INFERENCE / VALIDATION METHOD]

**Responses to population changes:** partly. We can confront predictions about
district staffing, budgets, rents, wages, capacity and service quality with actual
episodes. Causal attribution requires an adequate control or identifying design;
predicting a level alone does not establish a response. Historical episodes also
need the model's own prediction for that episode's population and horizon. A paper
reporting an immigration coefficient is not automatically a test of our engine.
[INFERENCE]

**The complete no-target-population counterfactual:** not directly observable.
Component tests can disconfirm its premises and constrain its scale, but no public
administrative table reports the other United States in which the target population
was absent. State budget balances cannot substitute: they mix federal grants,
local taxes, debt and other residents' tax bases. Likewise, the historical backcast
transports a current anchor backward; matching its own anchor is not a successful
forecast. [INFERENCE; [backcast scope](immigration-historical-backcast-2026-09-20.md),
[reality-check boundaries](immigration-fiscal-reality-checks-2026-09-19.md)]

We do already have two informative prediction exercises:

1. **School spending in held-out districts.** Five-fold 2019 prediction scored
   12,370 districts. Log-dollar RMSE was .301 for a 3/4 cost exponent, .233 for
   5/6, .223 for .85, **.203 for proportional spending and .192 for a freely fitted
   slope**. The broader screen preserves that order. Proportional spending beats
   the strong economies-of-scale rules here, but a free slope does better still.
   This is prediction across places, not within-place adjustment following removal.
   [DATA: [scaling test](immigration-service-scaling-test-2026-09-20.md)]
2. **Education in later birth cohorts.** The auxiliary GSS model fits parent-to-child
   schooling transitions on birth cohorts1961–71 observed through1996 and tests
   disjoint cohorts born1972+ observed1998–2024, both ages25–34. It uses the later
   observed parent-education mix. Thus it is a retrospective conditional temporal
   test, not an original 1996 fiscal forecast. [DATA / CODE:
   [projection check](immigration-projection-backtest-2026-09-19.md)]

I added a simple benchmark to the GSS exercise: predict the later distribution by
freezing the training distribution, without updating parental composition. The
score is half the sum of absolute errors across below12/exactly12/above12 years of
schooling, expressed in percentage points; lower is better. [CALCULATION:
[new reproducible probe](../infra/immigration-fiscal/validation_audit_2026_09_28/README.md)]

| GSS all-origin generation, English-language frame | Transition model error | Frozen-distribution error |
|---|---:|---:|
| Second generation | **4.59pp** | 5.67pp |
| Third generation | **2.80pp** | 5.16pp |
| Fourth-plus | **3.39pp** | 9.24pp |

The model adds predictive information in these three comparisons. But retaining
the alternate frames matters: in the pre2021 English frame, second-generation
error is **3.29pp versus 2.72pp**, so the model loses. It improves in eight of nine
reported group/frame comparisons [2026-09-28 (7a43e65): the fourth-plus rows of the English-only and
all-languages frames are the same sample, so it is seven of eight distinct; the frozen baseline was
chosen after the model's results were known, as the lane's README says], which overlap and are **not nine independent
replications**. No survey-design uncertainty for the score difference is available.
Mexican-origin G2 has only13 training respondents and fails the upstream cell-support
rule in every frame; **there is no Mexican-specific pass**. Parent-link weighting
also differs from a unique-child population distribution. This validates a narrow
education transition exercise, not the fiscal model or lifetime NPV. [CALCULATION / LIMIT]

**A second new probe gives an adverse result.** For SNAP, I fit one common
Hispanic-versus-other reporting-odds correction on 25 valid state/DC jurisdictions
and predict the 26th, rotating through every jurisdiction passing the existing
administrative screen. Benefit-dollar-weighted mean absolute error **worsens from
5.16 to 5.69pp**, and RMSE from 8.13 to 8.79pp. Average signed error improves from
+1.03 to −0.19pp; 20 of 26 jurisdictions improve individually, but deterioration
in large states dominates. The 17-state higher-sample-support subset also worsens
(MAE 5.42→6.11pp).
[CALCULATION: [SNAP probe and retained residuals](../infra/immigration-fiscal/validation_audit_2026_09_28/README.md)]

This is a failed point-prediction comparison for a **new pooled correction**, not
a test of the adopted key's direct administrative substitutions and not a fiscal
dollar correction. The sources and state validity screen had already been
inspected; this is retrospective cross-validation. Unknown ethnicity is imputed,
QC participants differ from CPS SPM-unit members, and no uncertainty interval for
the score difference is claimed. The finding is that reducing aggregate bias can
worsen geographic accuracy; a common correction needs evidence of transport.
[LIMIT / INFERENCE]

## 3. Four follow-ups now executed

Each lane saved its split, score and alternatives before calculating the new
results. [2026-09-28 (7a43e65): true of the prediction tests. The schools lane's NAEP join behind "46 of
51" entered its design after the first prediction scores, and the medical unknown-birthplace
sensitivity after scoring.] Most source outcomes had been inspected in earlier work, so these are
retrospective tests. The newly acquired MCBS2022 file is a previously unused
external measurement check. [2026-09-28 (7a43e65): the file is new but the people partly are not.
MCBS panels span years, and 41% of MEPS respondents aged 65+ in 2023 also answered in 2022 (46% of
2024's in 2023).] Neither label makes the entire account validated.
[METHOD: linked designs and results below]

### School spending, staffing and quality

Fit FY2000→2010 spending changes and predict FY2010→2019, conditional on actual
later enrollment and CPI. Across **12,011 districts**, the free enrollment response
with a training-period state trend has district log RMSE **.182**, versus **.202**
for proportional enrollment with its training trend. But proportional enrollment
**without** a trend wins when fitting and scoring weight initial pupils: **.169
versus .175**, and also has lower district mean absolute dollar error (**$5.86m
versus $7.09m**, in 2020 dollars for the unweighted fits). Growing districts favor
the simple proportional rule; shrinking districts favor unchanged real spending.
There is no universally winning exponent. [CALCULATION:
[school tests](../infra/immigration-fiscal/validation_schools_2026_09_28/RESULT.md)]

Within a separate panel of 12,138 districts matched across FY2019→2024,
pupils fall **3.46%**, real current spending rises **5.50%**, and teacher FTE rises
**1.99%**. These are pooled level changes, not causal immigration effects. The
prediction exercise excludes New Jersey because its early teacher data lack
usable support; the observed table retains it. Frozen staffing is competitive
with the fitted model. These results do not support treating a pupil decline as
an immediate proportional saving, and they do not identify long-run avoidable
costs. COVID, funding, pupil needs and labor prices remain competing explanations.
[CALCULATION / INFERENCE: school tests]

Quality has a separate check: **46 of 51 state/DC jurisdictions** have both lower
pupils per teacher in the matched resource panel and lower NAEP grade4 reading
point estimates in 2019→2024. The finance and NAEP populations are not identical;
this is not 46 significant declines or evidence that more teachers harmed learning.
It shows why staffing ratios cannot certify stable achievement. Matched district
achievement, building capacity and incumbent-specific outcomes remain unavailable
in these joined inputs. [CALCULATION / LIMIT: school tests]

### Medical dollars: a new year and attempted explanations

For Hispanic/NH-white Medicare-plus-Medicaid payments per Medicare-ever person
aged 65+, MCBS2022 gives **1.114 (SE .151)** versus MEPS2022 **1.009 (.109)**.
Their gap is **.106 (.186)**, compared with **.420 (.177)** in 2023. The new point
gap is smaller, but its 95% interval **[−.259,+.470]** still includes the old gap:
this establishes neither equivalence nor a significant year-to-year change.
[CALCULATION: [medical checks](../infra/immigration-fiscal/validation_medical_2026_09_28/RESULT.md)]

**85.1%** of the 2023 gap's exact arithmetic decomposition is Medicare. Applying a
common four-cell age/sex distribution leaves **.374** of the original .420 gap;
an analogue of CMS's tail-mean disclosure treatment leaves **.411**. Additional
p99 caps leave .293 but change the estimand. CMS adjusts MA service spending, and
the public files cannot exactly align MA enrollment, covered months, institutional
use or detailed origin. These findings narrow explanations without identifying a
defect in either survey. [SOURCE / CALCULATION / LIMIT: medical checks]

Freezing pooled MEPS2016–2023 ratios predicts 2024 better than repeating 2023 on
four of six correlated outcomes, but worsens the Hispanic aggregate public-payment
ratio and Medicaid ratio. The Mexican/all-donor public-payment error is **−.074
(SE .137)** versus **−.202** repeating 2023; those are ratio errors, not dollar
corrections. These tests retain uncertainty by payer and supply no blanket adverse
Mexican-origin multiplier. [CALCULATION / INFERENCE: medical checks]

### Actual earlier fiscal components and later prediction

Reconstruct actual CPS income-year 2021–2024 wages, federal/payroll tax and selected
transfers, preserving each year's released policy treatment and the canonical
resource-sharing rules. Freeze income2022 profiles and predict 2024 shares. Across
eight declared, overlapping outcomes, mean absolute allocation-share error falls
from **.495pp** with frozen shares to **.415pp** with updated age/sex/generation
composition. Wages and tax keys improve; **SNAP, Social Security and SSI worsen**.
Later population composition and national totals are conditional inputs. This is
a test of component allocation, not a forecast of national budgets; it reconstructs
selected components, not full historical government accounts. [CALCULATION:
[fiscal-year tests](../infra/immigration-fiscal/validation_fiscal_years_2026_09_28/RESULT.md)]

The independent tax comparison is much less reassuring. Predicting the **2023 IRS
tax distribution across 19 AGI bins** with frozen 2022 CPS shares gives **25.20pp
total-variation error**, versus **2.43pp** simply freezing 2022 IRS shares. Same-year
CPS2023 still errs by 24.06pp. This is the released CPS tax construction before our
later administrative calibration, not a score of the final calibrated key. [2026-09-28
(ladder 249): the final calibrated key scores 23.5pp against IRS 2023 (8.4pp with $1M+
pooled, against 18.5pp before CBO's gradient); matching IRS with CBO's groups kept would
raise the group's income tax by $3.2bn / $3.1bn. See the
[held-out tax lane](../infra/immigration-fiscal/tax_key_heldout_2026_09_28/RESULT.md).] [After the
cross-lab review: that correction is fitted to the same 2023 year the old key was scored on,
and most of it comes from the $1M+ bin, where the group's share rests on 15 CPS records
extrapolated above $3.1M; the parent now recommends it beside the case.] It
exposes a distribution mismatch that close within-CPS ethnic prediction cannot
resolve; the IRS bins do not identify Mexican-origin taxes. No proportional
Mexican-origin correction follows from these errors. [CALCULATION / LIMIT: fiscal-year tests]

The policy stress matters: carrying income2021's pandemic net-tax profile into 2024
underpredicts the target union's share by **4.77pp**, or **$90.86bn** conditional on
the 2024 CPS national net-tax total. This is a failed old-profile prediction, **not
an error estimate or correction to today's account**. The 2021 definition includes
additional refundable credits and EIP3; unadjusted profiles do not travel safely
across policy regimes. [SOURCE / CALCULATION: fiscal-year tests]

### A coherent Mariel school budget

One donor-weight vector now predicts the revenue and spending components, totals
and retained accounting residuals. On a 1970–1976 fit predicting 1977–1979, the two
fixed weightings have joint normalized RMSE **39.75% and 26.65%**, versus **16.02%**
for a simple donor-growth baseline. The score normalizes six endpoints by their
training levels; it is neither a fiscal-loss percentage nor a confidence interval.
Deleting the largest donor does not rescue either fit. [CALCULATION:
[joint Mariel test](../infra/immigration-fiscal/validation_mariel_2026_09_28/RESULT.md)]

**This construction fails its own prediction check.** [2026-09-28 (7a43e65): it already misses its
1970–76 training years by 29–34% normalized RMSE. Dade's federal revenue exceeds every donor's in 6 of 7
of them, so the failure is one of fit.] Accounting coherence is
necessary but insufficient. Positive post-event spending gaps remain model outputs
with weak predictive support; they cannot validate a net causal school balance.
A local balance would also require distinguishing outside grants from national
resource savings. This finding qualifies our new joint estimator; it does not
establish zero costs or refute every published Mariel design. [INFERENCE]

### What is still open

The main unfinished tests are a policy-updated fiscal forecast against genuinely
reserved administrative outcomes; comparable medical person-month and service
payments by detailed origin; district spending, capacity and achievement following
a credible population shock; and full historical government accounts. The current
holdings do not identify those quantities merely because these four executions
succeeded. [2026-09-28, later: the within-district part of the school test is done for
the 2022–2024 newcomer surge in New York City, Chicago and Denver (ladder 252). Staff
and money followed the new pupils at about half to 0.6 of enrollment and late, and
never-English-learner scores barely moved. District budgets and any system-level
effect remain open.] [2026-09-28, later still: a test of the account's keys against
administrative totals it never used, with predictions committed before any target was
opened (883182b), is scored (ladder 255). Births to Mexican-origin mothers and the
group's share of Medicaid-paid births hit [after the cross-lab review: the second only by
the tolerance rule; it is significantly low, +8.1% with z 2.4, worth about +$0.2–0.3bn]; the credit, SSI and Social Security keys have
no power on state totals, so the dollar keys remain untested by this route. A second
pre-registered test against published figures (NAE 2021, NAS 2017, hospital cost
reports) is being scored.] [2026-09-28, later: scored (ladder 256). Hospital cost reports
hit on state shares and the national total; the use-rate slope favors 0.7× only between
regions. NAE agrees on a shared method, so it validates nothing; NAS outlays match.] [After the
cross-lab review: NAS's receipts gap has a plausible post-hoc explanation, not a reconciliation, and
the note calling NAE's earnings-over-income ratio impossible was wrong; both lanes are corrected.] Public payroll replacement, mixed-household eligibility and
unpriced social channels remain in the [conceptual audit](immigration-adversarial-audit-2026-09-28.md).
Separate school-systemwide and enforcement/rent analyses have their own populations
and designs; their estimates are not added to these validation scores. [LIMIT / INFERENCE]

## 4. What we should stop counting as confirmation

- BEA national closure, source hashes, passing unit tests and exact reruns establish
  accounting or implementation properties. Group allocation can be wrong while
  national totals still match perfectly. [INFERENCE]
- CBO/SSA/Penn Wharton/ITEP agreement is not automatically multiple independent
  replications. There are shared inputs and model assumptions; CBO reweighting
  retains our within-income-bin origin shares. [SOURCE / CODE: [outside checks](immigration-outside-checks-2026-09-24.md)]
- Once an outside result is incorporated, reproducing it is calibration. Preserve
  the original residual, the correction and the next unused test separately.
  [INFERENCE]
- The external-benchmark script's **“corroborates”** flag can mean an implied
  change no larger than $2bn, rather than a statistically close fit. This is a
  materiality rule; counting its green rows as validation successes overstates
  the evidence. [2026-09-28 (7a43e65): rows without an implied effect use a second rule, an
  external/account ratio within 0.8–1.25. Of 61 "corroborates" rows, 54 pass the $2bn rule and 7 the
  ratio band; neither is a statistical test.] [CODE: `external_benchmarks_2026_09_24/benchmarks.py:27–35`]
- Agreement on gross earnings or spending does not deliver the same percentage
  accuracy for a net balance obtained by subtracting large quantities. Nor do
  empirical back-tests settle whose welfare should count. [INFERENCE]

**Retained:** independently corroborated earnings patterns, meaningful exposure
checks and actual public-resource costs. **Qualified:** conditional response and
whole-model precision claims. **Rejected for these tests:** the claim that our new
joint Mariel model predicts better than its baseline, and automatic transport of
pandemic net-tax profiles. **Corrected:** the claim that identical institutional
exclusions remove that explanation for the medical discrepancy. **Unresolved:**
complete causal validation, medical cross-survey disagreement and prospective
performance after calibration. The audit
contains supportive and adverse findings; political usefulness is not a scoring
criterion. LLM selection and interpretation biases remain a reason to retain
failed tests and all calculated alternatives. [INFERENCE / INSTRUMENT NOTE]

Coverage: the original audit's GSS and SNAP diagnostics are retained. Four follow-up
lanes now execute temporal school finance/staffing tests, a state achievement join,
medical definition/payer/year checks, actual CPS annual-component reconstruction
and independent IRS comparisons, and a joint Mariel budget. Each linked result
records input coverage, exclusions, naive baselines, uncertainty and reproduction
commands. No new causal coefficient or national total was adopted. [EXECUTION]

## Revisions

- **2026-09-28, executed follow-ups:** replaced proposed checks with their results,
  retained their adverse comparisons, and corrected the institutional-exclusion
  claim. The [validation decision](../decisions/2026-09-28-component-validation-boundaries.md)
  records why predictive successes remain component-specific and why the failed
  joint Mariel construction is not carried into the fiscal account.
- **2026-09-28, verification (7a43e65):** all 125 numbers match their lanes. Brackets qualify five readings: the tax corrections hold below $1M only (ladder 249), GSS is seven of eight distinct, design-before-scoring has two later additions, MEPS and MCBS respondents overlap across years, and the Mariel model fails in its training years. The "corroborates" rule has a second, ratio-band branch.
- **2026-09-28, newcomer schools:** the credible-shock school test is done within
  districts (ladder 252); its district-wide part stays open.
- **2026-09-28, administrative back-test:** the pre-registered test against state and national administrative
  totals is scored (ladder 255): two powered hits, no power on the dollar keys, no correction.
- **2026-09-28, published-figures back-test:** scored (ladder 256): S-10 level and national hits, a
  regional slope toward 0.7× uninsured use, NAE agreement by shared method, NAS outlays matched.
- **2026-09-28, cross-lab review (GPT-6 Astra, xhigh; each finding checked by the parent):** three readings
  qualified. The Medicaid-paid births share is a hit only by the tolerance rule; it is significantly low. NAS's
  receipts gap has a plausible explanation, not a reconciliation. The IRS tax-key correction rests mostly on 15
  top-income records. The NAE note calling earnings over income impossible was wrong.
- **2026-10-07, main case v6** ([decision](../decisions/2026-10-07-main-case-v6.md), ladder 295): the header notes
  the October 7 case, $389.1–461.5bn. This audit's checks stay on the September 27 case, and none of v6's four items
  is among the components it checks. Concept affected: the current object the audit points to.
