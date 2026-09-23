# Can population data identify fixed administration costs?

Date: 2026-09-20. [DESCRIPTIVE ESTIMATION / IDENTIFICATION CHECK]

**Result:** The executed US state/local panel does not identify a defensible fixed-versus-variable percentage. Its main population–administration elasticity is **0.47**, with an approximate 95% interval **−0.72 to 1.66**. Weighting larger states more changes the point estimate to **−0.27**. Both zero and proportional spending response remain compatible with the main specifications. This is not evidence that administration is free, or that 47% is the actual variable share. No federal response or Mexican-origin-specific elasticity was estimated.

## Data and estimand

[SOURCE / MEASUREMENT] Official Census published state-by-government-level finance estimates, current operations E23 (financial administration), E29 (central staff) and E31 (general public buildings). These selected functions are narrower than the BEA general-public-services pool. Employee compensation and other operating inputs are included; capital expenditure is excluded. Published weighted estimates are used rather than unweighted sums of the annual local-government sample. The 2012 Census ordinal state codes are explicitly mapped to FIPS.

The primary panel has **50 states × seven years = 350 observations**: 2012, 2017–2019 and 2021–2023. The window follows existing cached finance and ACS1 population coverage; missing 2020 ACS1 is excluded, not interpolated. DC/territories are excluded. The primary outcome and all diagnostic specifications were recorded before running the analysis. State-only building-operation cells are incomplete: those secondary specifications have 297 observations/48 states, while combined and local panels are complete.

[MODEL] Regress log current spending on log population, with state and year fixed effects. The coefficient is the within-state spending association with a 1% population change after common year shocks. Nominal-dollar year effects absorb a common price index, not region-specific wages. Inference clusters on state; intervals use CR1 standard errors and a normal 1.96 critical value. They omit survey/imputation and specification uncertainty. The weighted version fixes weights at each state's initial population.

## Results

| Prespecified diagnostic | Population elasticity | Approximate 95% interval |
|---|---:|---:|
| Main: state/year effects, unweighted | 0.47 | −0.72 to 1.66 |
| Initial-population weighted | −0.27 | −1.97 to 1.43 |
| Census waves only: 2012/2017/2022 | −0.23 | −1.78 to 1.31 |
| Pre-2020 only | 0.38 | −0.78 to 1.54 |
| Exclude 2020–2022 | 0.59 | −0.63 to 1.81 |
| Add state-specific linear trends | −0.39 | −3.52 to 2.74 |

[DERIVATION] The 2012–2017, 2017–2022 and 2012–2022 long-difference estimates are also imprecise. Removing one state at a time leaves the unweighted main point estimate between 0.27 and 0.68; the uncertainty is not resolved by dropping a single state. Component and government-level estimates, both weighting conventions and all diagnostic outputs are retained in `derived/estimates.csv` and `derived/leave_one_state_out.csv` under the [reproduction directory](../infra/immigration-fiscal/administration_response_2026_09_20/README.md).

## Why this does not yield an actual fixed fraction

[DERIVATION] Under the specific cost function `C(N) = F + vN`, with fixed F and constant per-person variable cost v:

`population elasticity = (N/C) × dC/dN = vN/C`.

Only under that model, and with an identified causal response, does elasticity equal the variable-cost share. Policy, wages, grants, technology and service quality change over time. Migration also responds to economic conditions and public services. State/year effects do not remove these channels, and the panel contains no exogenous population shock. Negative or greater-than-one estimates must not be clipped into a reassuring fixed/variable split.

For a finite population change, define the responsive fraction of the per-capita allocation as `[C(N)−C((1−s)N)]/[sC(N)]`. This equals the variable share under the affine model above; under a constant-elasticity model it is `[1−(1−s)^epsilon]/s`. A local elasticity and the response to a roughly 12% smaller population therefore need not coincide.

## External check and next discriminating evidence

[SOURCE A2: [CBO's 2025 state/local immigration-surge analysis](https://www.cbo.gov/publication/61464), methodological appendix.] CBO explicitly assesses no spending response for executive/legislative and tax-collection/financial-management functions for at least the first three years of the surge. That is a short-run modeling judgment, not an estimated permanent zero. The report also recognizes service pressure without an immediate budget response; a flat budget does not establish zero crowding or welfare cost.

[INFERENCE] The best next evidence is function-specific workload and cost: tax returns, permits, claims or cases, their complexity, staffing/FTE, contractors and service performance. A longer public-employment panel can distinguish staffing from wage changes; it still needs credible variation for a causal interpretation. A federal example is [IRS budget/workforce history](https://www.irs.gov/statistics/irs-budget-and-workforce); it cannot stand in for all federal administration. An exogenous workload change with unchanged service standards and measured adjustment over several years would discriminate between the cost models more directly.

**Decision impact:** retain the labeled administration sensitivity and separate its scope from defense. Neither the illustrative 25% response nor a 47% response receives empirical validation here. Education and function-specific administrators remain in their existing service costs. The annual model's headline is unchanged and still conditional on its response assumptions.

## Verification

2022 national E23/E29/E31 totals match the independent cached Census API amounts exactly; state sums reconcile within rounding and combined/state/local component conservation is exact. Input hashes are pinned and changed vintages fail. Source documents, population extraction and dataset paths are linked by the reproduction README. The script retains missing component cells instead of treating them as zero. All outputs are rederivable; no raw data changed.

Independent double-demeaning and direct cluster-score calculations reproduce both main coefficients and standard errors within 3×10⁻¹⁴. A separate source check matches every one of the 1,050 level-specific panel rows to the original finance/population inputs. The reproducible `verify.py` retains the principal numerical and input-vintage checks.

## Revisions

**2026-09-23 — the 2022 and 2023 waves carry a reporting break in financial administration; the
verdict stands.** National E23 current operations in this lane's own inputs run $53.6bn in 2021,
**$97.3bn in 2022 and $96.3bn in 2023** (state $31.7bn → $57.4bn; local $21.9bn → $39.9bn), after
growing 2–6% a year from 2017. The jump is uneven: 2022/2021 ratios are 4.8 in Wisconsin, 3.4 in
New York and California, 2.9 in New Jersey and 2.3 in Illinois and Hawaii. Year effects therefore do
not absorb it. The county lane that found it traces the local rise to NYC, Cook County,
Philadelphia and Florida. [DATA: `derived/selected_finance.csv`, `derived/panel.csv`; CALCULATION:
`../infra/immigration-fiscal/gg_response_county_iv_2026_09_23/e23_other_lanes.py` →
`derived/e23_other_lanes.csv`; trigger: [county IV lane](../infra/immigration-fiscal/gg_response_county_iv_2026_09_23/RESULT.md)]

Specifications affected:
- **Contaminated:** the main estimate (0.47, which includes 2022 and 2023), census waves only
  (−0.23), "exclude 2020–2022" (0.59, which still includes 2023), and the long differences ending
  in 2022.
- **Clean:** pre-2020 only, **0.38 (−0.78 to 1.54)**, and the 2012–2017 long difference.

The clean estimate sits close to the main one and is just as wide, so the conclusion, that this
panel cannot identify a fixed share, does not change.

The main case does not read this series. Its general-government pool is BEA NIPA Table 3.17, and
its 0.59–0.84 response comes from the published 2022 Table 1, whose cross-state levels the county
lane found stable on either vintage. BEA's state and local general public service shows no break
of the Census size. It grew 13.5% in 2021, 14.7% in 2022 ($255.3bn to $292.8bn), then 2.9% and
1.1%. [DATA: `sources/immigration-fiscal/data/external/bea_nipa/Section3All_xls.xlsx`, T31700-A
line 22] BEA's own tax-collection-and-financial-management line (Table 3.16, line 83) rose 26% in
2021, before the Census break, and 30% in 2022 ($55.8bn to $72.5bn), then 5% and 2%. That is a
two-year surge, not a step, and its 2022 rise of $16.7bn is well under the Census's $43.7bn. If
all of it were the same artifact, the main case would move by at most $1.2–1.7bn: the union's 12%
at a 0.59–0.84 response. [DATA: T31600-A line 83; INFERENCE on attribution]
