# What has been validated, and what can be back-tested?

**Verdict:** Several important inputs are independently corroborated, and outside
checks have found real errors. We have some held-out prediction tests. We have
**not** independently back-tested the complete national counterfactual. Confidence
in observed earnings, enrollment and some benefit shares is stronger than confidence
in the spending response, lifetime projection or complete welfare total. [INFERENCE]

September 28, 2026. Validation audit, following the [conceptual audit](immigration-adversarial-audit-2026-09-28.md).
The current object is the September 27 account's **$321.8–387.4bn annual conditional
net cost to other US residents**, including imputed public-capital services. Its
broader component sensitivity is **$258.6–436.1bn**; neither band is an empirically
validated confidence interval. It concerns the observed Mexican-origin resident
union, including US-born descendants, not all immigrants or a specified admission
policy. [CALCULATION: [current case](../infra/immigration-fiscal/main_case_long_run_2026_09_27/RESULT.md)]

## 1. The useful cross-references we already have

These are results of the earlier checks, before their subsequent use in calibration.
Dollar amounts from different account vintages are not combined here.

| Quantity checked | Actual comparison | Interpretation |
|---|---|---|
| Relative earnings, two surveys | For civilian household residents with positive wages, Mexican self-ID / other-self-ID mean earnings is **0.6919 in ACS2024 and 0.6866 in CPS2025**. Sampling intervals: .6867–.6972 and .6649–.7082. | Strong descriptive corroboration of an important tax-capacity input. Absolute earnings differ; Mexico-born ratios agree less closely (.6851/.6458). Neither survey identifies the full target union equally or establishes why earnings differ. |
| National wages, administrative records | Income2023 CPS wages **$11,105.6bn** versus SSA compensation **$11,103.2bn**, a **+0.021%** difference. Income2024 comparison: **+2.25%**. | The overall wage scale is plausible. CPS wage-recipient counts are lower by 6.09%/5.27%; totals can agree while the distribution is wrong. Coverage and compensation definitions differ. |
| School enrollment transport | Rates fitted excluding **both California and Texas** predicted their Mexican-origin pupil counts with residuals **+17k/+27k**, versus sampling SEs **69k/59k**. | A real geographic transport check. Texas other-resident pupils were underpredicted by 154k (SE69k), and administrative Hispanic counts still disagree. This checks pupil exposure, not spending avoidability. |
| SNAP benefit allocation | California FY2024 Hispanic benefit-dollar share: **43.989% administrative QC versus 44.078% CPS**. | Useful local agreement, not proof of national ethnic accuracy. Unknown/coding problems invalidate many other states' ethnic comparisons; the administrative point estimate includes a treatment of unknown ethnicity. Hispanic is not Mexican-origin. |
| Federal tax distribution | Income2023 modeled federal income tax before refundable credits is **13.73% below IRS**. The shortfall above $500k AGI is $489.8bn, partly offset by $200.2bn excess below it. | A failed distribution check. Applying the national discrepancy proportionally to Mexican-origin taxes is unsupported. Later income-gradient corrections address this class of discrepancy; matching the same target afterward is calibration. |

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
Hispanic versus non-Hispanic-white Medicare-plus-Medicaid spending, aligned MEPS2023
gives **0.845 (SE .089)** and MCBS2023 **1.265 (.152)**. Pooling MEPS2016–24 gives
**1.005 (.056)**. Neither public-use file here includes facility users, so
institutions do not explain away this difference. Coverage-count agreement with
Medicaid records cannot validate medical dollars. [DATA: [definition-by-definition
reconciliation](../infra/immigration-fiscal/medical_ethnicity_pooled_2026_09_23/RESULT.md#7-65-mcbs-nursing-facilities-and-institutions)]

## 2. What is genuinely back-testable?

**Observed component levels:** yes. Freeze a model using earlier years, then predict
later earnings distributions, tax liabilities, pupil counts, benefit shares and
costs by beneficiary type. A conditional prediction may use later population
composition or enacted tax rules, but it must say so: that tests allocation or
transport, not an unconditional forecast. Compare with a simple frozen-share or
population-proportional baseline. [PROPOSED VALIDATION]

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
reported group/frame comparisons, which overlap and are **not nine independent
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

## 3. Where further cross-checking has the most value

The ranking is a judgment about consequence and tractability, not a measured
value-of-information calculation. [FRAMING-SENSITIVE]

1. **Joint service-response tests.** Freeze a prediction for growing and shrinking
   districts or localities, and score spending, staffing, capacity and incumbent
   outcomes together over short and longer horizons. Flat spending with worse
   service is not evidence of zero cost; extra spending with stable quality can be
   a real resource cost. Conversely, persistent unused capacity weakens full-cost
   avoidability. Use held-out periods and locations, pre-event checks, and report
   endogenous migration/funding limitations. Public payroll and replacement hiring
   belong in the same exercise. Existing cross-sectional fits, within-panel
   associations and the donor-sensitive Mariel school test constrain this question
   without settling it. [PROPOSED; [executed causal checks](immigration-causal-execution-2026-09-20.md),
   [payroll gap](immigration-adversarial-audit-2026-09-28.md)]

   Two concrete tests use existing holdings: fit school spending with F33's
   2000/2010 waves and score 2019 changes; and predict Mariel's local revenue and
   spending endpoints jointly. The latter needs one coherent counterfactual
   budget: separately fitted synthetic controls cannot simply be added into a
   net fiscal balance. Both are retrospective exercises, not untouched future
   observations. [PROPOSED; source scope in the scaling and causal memos above]
2. **Medical spending, not just enrollment.** Reconcile MEPS and MCBS payer,
   Medicare Advantage, top-coding and reporting definitions; use unused
   year/state/eligibility spending cells wherever available. Separate member-years
   from people ever enrolled, household services from institutions, and actual
   payments from modeled allocation. A lower or higher independent cost ratio
   should move the account by the same evidence standard. [PROPOSED; reconciliation above]
3. **Allocation transport across states and years.** The new SNAP test above
   finds worse point prediction with a simple pooled correction on its chosen score;
   geographic heterogeneity needs attention before assuming transport. Reserve
   a later unused administrative year after freezing the rule. For taxes, extend
   the matched income-bin/state checks; do not claim these identify within-bin
   Mexican-origin payments. Treasury's [tax-record model](https://home.treasury.gov/system/files/131/WP-122.pdf)
   imputes broad ethnicity, so it is a useful separate construction but not a
   direct Mexican-origin administrative census. [PROPOSED; source rechecked September28]
4. **An actual historical account reconstruction.** Rebuild earlier annual accounts
   from that year's microdata and policy, then freeze the transport rules and test
   later observables. The existing fixed-birth/entry cohort follows surviving
   residents in repeated cross-sections; it does not follow original individuals'
   lifetime taxes and benefits. Attrition, return migration, identity change and
   policy changes need explicit treatment. [PROPOSED; [projection limits](immigration-projection-backtest-2026-09-19.md)]

These are incompletely validated avenues, not a claim that nobody has looked at
them. School-systemwide and enforcement/rent work is already active in the
September27 lanes; preliminary output is not a completed independent check.
The current [conceptual audit](immigration-adversarial-audit-2026-09-28.md) separately
tracks mixed-household eligibility, public payroll and unpriced social channels.
[REPO STATUS: inspected September28; active peer files not modified]

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
  the evidence. [CODE: `external_benchmarks_2026_09_24/benchmarks.py:27–35`]
- Agreement on gross earnings or spending does not deliver the same percentage
  accuracy for a net balance obtained by subtracting large quantities. Nor do
  empirical back-tests settle whose welfare should count. [INFERENCE]

**Retained:** independently corroborated earnings patterns, meaningful exposure
checks and actual public-resource costs. **Qualified:** conditional response and
whole-model precision claims. **Unresolved:** complete causal validation, medical
cross-survey disagreement and prospective performance after calibration. The audit
contains supportive and adverse findings; political usefulness is not a scoring
criterion. LLM selection and interpretation biases remain a reason to retain
failed tests and all calculated alternatives. [INFERENCE / INSTRUMENT NOTE]

Coverage: existing fiscal outside checks, temporal/cohort checks, service-scaling
holdouts and bounded crime/production/housing validation were inspected; two cheap
diagnostics were executed. Legacy raw builders were not rerun, active peer work
was not changed, and no new causal coefficient or national total was estimated.
The old preregistration ledger was checked as an additional lead; its unresolved
entries are not counted as validation successes.
