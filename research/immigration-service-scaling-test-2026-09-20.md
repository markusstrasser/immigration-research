# Public-service scaling: executed test

Date: 2026-09-20. **Verdict:** Sublinear school spending is visible within districts,
but a universal 3/4 or 5/6 exponent does not describe public-service budgets. The
findings support category-specific sensitivity analysis; they do not identify an
additional saving to apply to the annual immigration account. [EMPIRICAL MODEL /
INFERENCE; [reproduction and complete outputs](../infra/immigration-fiscal/scaling_test_2026_09_20/README.md)]

## Hypothesis and derivation

The strongest complexity-theory case is that denser populations share physical
networks, lowering required infrastructure per resident. In Bettencourt's urban
model, land area A scales as N^(2/3); spacing d scales as (A/N)^(1/2); network
volume proportional to Nd therefore scales as N^(5/6). The exponent describes
a particular physical quantity under particular geometry, rather than annual
government dollars. Network length and volume have different predicted exponents.
[SOURCE: [Bettencourt 2013, pp.1438–1440](https://www.colorado.edu/socialreactors/sites/default/files/attached-files/bettencourt_2013_science.pdf);
[derivation and contrary evidence](../notes/immigration-scaling-theory-evidence-2026-09-20.md)]

For monetary cost C=pQ, the cost exponent equals the quantity exponent plus the
unit-price exponent. Teachers, care hours, urban wages, congestion, service quality
and fixed appropriations need not follow network geometry. French road exponents
range from .664 to 1.202 across city definitions; a favorable Brazilian scaling
study finds sublinear roads/school counts but linear aggregate budgets. These
are direct reasons to test universality, not presume it.
[IDENTITY; SOURCE: [Cottineau et al., Table 4](https://arxiv.org/pdf/1507.07878),
[Meirelles et al. 2018](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0204574)]

## School spending: across size versus within-place growth

[ESTIMATED ASSOCIATIONS] Reused Census/NCES F33 district current operating
expenditure and own-fiscal-year fall enrollment, retrieved through the existing
Urban API acquisition. Available matched waves are 2000, 2010 and 2019. This is
the available three-wave panel, not a chosen favorable window; 2010–2019 is a
separate window check. The 50-state screened sample has 38,080 district-year rows;
11,788 districts survive all three waves. Regular noncharter districts with at
least 100 pupils enter. The main inherited sample also screens per-pupil spending
and Hispanic-share completeness; a broader rebuild removes those two restrictions.
DC is excluded; Hawaii stays in regressions. [SOURCE: `school_coverage.csv`,
upstream `school_flight_2026_09_18` cache and builder;
[F33 definitions](https://nces.ed.gov/ccd/pdf/2021306_FY19F33_Documentation.pdf)]

The table reports elasticity of **gross current school spending** with respect to
pupils: beta=.8 means approximately .8% more spending per 1% more pupils, within
the fitted relationship. It does not mean that 80% of a net fiscal deficit responds.
Costs use 2020 dollars. Across-district models absorb state differences; panel
models absorb district and state-by-year differences. Intervals are state-clustered
CR1 95% intervals using t critical values, not causal uncertainty bounds.

| Specification | Districts weighted equally | Pupil-weighted |
|---|---:|---:|
| Across districts, 2019 | .945 [.929, .962] | 1.004 [.991, 1.017] |
| Within districts, 2000/2010/2019 | .735 [.675, .796] | .836 [.787, .884] |
| Within districts, 2010–2019 difference | .618 [.542, .694] | .778 [.694, .862] |
| Within districts, instructional spending | .801 [.736, .866] | .922 [.883, .961] |

Pupil weights use 2019 enrollment for the cross-section and fixed 2000 enrollment
for panel/difference models. They emphasize larger systems; neither weighting is
an estimate specifically for Mexican-origin children. The broader sample's total
spending panel estimates are .719 unweighted and .833 weighted. Thus the original
screen does not create the entire sublinear association. [SOURCE: `school_estimates.csv`]

**Disconfirmation of a universal exponent:** across 2019 districts, the unweighted
slopes are .849 for fewer than 1,000 pupils, .986 for 1,000–9,999, and 1.028 for
10,000+. Apparent economies are concentrated among smaller districts in this
cross-sectional comparison. Within-panel .836 happens to resemble 5/6, but the
near-proportional weighted cross-section and instructional response prevent treating
that coincidence as a verified network mechanism. [ESTIMATES / INFERENCE]

Five-fold held-out prediction uses training-only state intercepts. Hawaii's single
district cannot supply both training and test rows, so prediction excludes it and
scores 12,370 districts. Log-dollar RMSE is **.301 for 3/4, .233 for 5/6, .223 for
.85, .203 for proportional spending, and .192 for a freely fitted slope**. The
broader sample preserves this ordering. These are predictive scores, not formal
pairwise significance tests or forecasts of within-district growth. The proposed
universal exponents lose this cross-sectional prediction test. [SOURCE: `school_cv.csv`]

Remaining planned checks: growing/shrinking 2010–2019 associations are .713/.541
unweighted and .822/.751 weighted; their difference has not been separately tested.
Restricting absolute enrollment log change to at most .2 gives .643/.784. Keeping
these construction alternatives matters more than selecting the coefficient
closest to a preferred theory. [SOURCE: complete coefficient export]

## Ten state/local functions

[ESTIMATED ASSOCIATIONS] Official weighted Census state/local current-operations
aggregates cover 50 states in 2012, 2017–2019 and 2021–2023: 350 observations.
Missing 2020 ACS population is excluded, not interpolated. Year effects absorb
common nominal price changes, not region-specific prices. Population rather than
service users is the size measure here. State geography is not functional-city
geography. Twelve 2022 national category anchors match an independent Census API
extract exactly; national/state-sum differences are at most $6,000 of rounding.
[SOURCE: `state/national_2022_anchors.csv`, `state/audit.json`;
[source paths and original acquisition](../infra/immigration-fiscal/administration_response_2026_09_20/README.md)]

| Function | Across states, year effects | Within states and years, 95% interval |
|---|---:|---:|
| K–12 | .973 | .768 [.184, 1.353] |
| Higher education, core | .891 | .783 [−.418, 1.985] |
| Financial/central administration and public buildings | .824 | .471 [−.748, 1.689] |
| Police | 1.037 | .851 [.399, 1.303] |
| Fire | 1.085 | 1.175 [.659, 1.691] |
| Nontoll highways | .727 | 1.464 [.484, 2.445] |
| Parks | .948 | 1.412 [.698, 2.125] |
| Libraries | .974 | .676 [.020, 1.331] |
| Health | 1.009 | 1.174 [−.585, 2.933] |
| Hospitals | 1.374 | .451 [−1.535, 2.436] |

All ten full-panel within-state intervals include 1; that is imprecision, not
proof of proportional costs. Census-wave and pre-2020 specifications are exported
for every function. For example, pre-2020 K–12 is 1.380 [.669, 2.091], showing
substantial window sensitivity. No multiple-testing-adjusted discoveries are
claimed. Public provision shares, ages, policy and prices remain possible drivers.
[SOURCE: all 60 rows of `state/estimates.csv`]

## Exact fiscal bridge and consequence

[MODEL DERIVATION] If C(N)=aN^b with unchanged a, composition and quality, and s is
the target share of the relevant service population, its incremental cost relative
to proportional assigned costs is:

`r = [C(N) − C((1−s)N)] / [s C(N)] = [1−(1−s)^b] / s`.

Only infinitesimal changes give r=b. At the annual account's national target share
40.896574m/340.110988m = .120245, the exact values are .761879 for b=.75 and
.842102 for b=5/6. A roughly 20% response requires b around .19, nowhere near
either proposed scaling law. Fixed costs can lower total response further, but
costs already treated as fixed must not be discounted twice. [CALCULATION]

As a deliberately uniform **theory-only** transfer to every ordinary-service
category, holding receipts, household benefits and production unchanged:

| Assumed cost power | Conditional annual net cost to other US residents, 2024 $bn |
|---|---:|
| 1, proportional reference | 269.8–288.7 |
| .85 | 219.7–237.9 |
| 5/6 | 214.0–232.2 |
| .75 | 185.7–203.5 |

These are four-case model ranges across personal/shared allocation and cash/GDP
production scaling, not confidence intervals. National origin share is not each
locality's target pupil/service-user share; F33 cash operations also differ from
BEA current consumption including depreciation. Therefore this diagnostic does
not calibrate the account. Its purpose is to make the magnitude of the theory
explicit. CBO's existing school response and these scaling coefficients may capture
the same adjustment; multiplying them would assume independent savings without
evidence. [SOURCE: `theory_fiscal_scenarios.csv`; MODEL / FRAMING-SENSITIVE]

**Integration:** retain the [annual account's](immigration-complete-annual-account-2026-09-20.md)
$165–197bn CBO-informed conditional comparison and $121–160bn additional
fixed-non-school-education sensitivity, alongside the $270–289bn proportional
benchmark. This test neither independently verifies those totals nor supplies an
extra discount. It strengthens the case for reporting heterogeneous service
responses and weakens the case for a universal fiscal exponent.

## What this resolves and what remains

- **Leading explanation:** school spending responds less than proportionately in
  the observed panel; service budgets combine scale, fixed resources and policy.
- **Top alternative:** lower spending per pupil reflects crowding or delayed
  appropriations rather than producing the same quality more efficiently. Sorting,
  income, grants and measurement error can also change the estimated slopes.
- **Discriminating evidence:** link plausibly external enrollment shocks to regional
  input prices, staffing, class sizes, attainment and spending over several horizons.
  Sustained lower inputs per pupil with preserved outcomes would support efficiency;
  worsening quality or later spending catch-up would favor rationing or delay.
- **Decision:** keep category-specific fiscal sensitivities; no additional complexity
  discount, no new causal ethnic estimate. [Decision record](../decisions/2026-09-20-service-scaling-calibration.md)
- **Next empirical step:** quality/staffing and stable-boundary shock designs. They
  are absent from this matched panel; instructional dollars cannot substitute for
  quality. Neither fixed effects nor a large row count resolves that absence.

[VERIFICATION] Four tests passed; independent residualization reproduced eight
primary school and all 60 state regressions. Native review found no numerical
defect and prompted fail-closed finite-value/model-coverage guards. Source bytes,
producer and outputs are hashed. The school sensitivity coefficients and prediction
scores are not all independently re-estimated by the second verifier. Raw inputs
remain unchanged; generated outputs are ignored. [INSTRUMENT] LLM-assisted design
and interpretation can favor a construction; all prespecified estimates, competing
weights and disconfirming prediction scores are retained.
