---
date: 2026-09-17
concept: country-origin-comparison
status: adopted
relations:
  - refines: 2026-09-17-selection-measurement-scope
---

# 2026-09-17: Compare measured parent origins with explicit native benchmarks

## Context

The user asked for datasets and whether any LATAM group approaches “bio-Americans.” No standard public dataset variable implements that term. Country, race, family birthplace, self-identification and genetic ancestry are different constructs. The explicit benchmark clarification remained unanswered while acquisition and analysis proceeded.

## Alternatives considered

1. Reuse the old ethnicity-only or father-priority tables. Easier, but loses mixed origins and self-identification attrition and lacks proper survey variance.
2. Treat country categories as genetic fractions. Rejected: no genotypes or country-specific grandparent reconstruction in CPS.
3. Compare reported own/parent birthplaces, retain both native-parent benchmarks and overlapping mixed-origin membership. Adopted for descriptive economic outcomes.

## Decision

Use five complete CPS ASEC releases, 2022–2026, with all replicate weights. Main reference is US-born non-Hispanic white-alone adults with two US-born parents; retain all-race US-parent and broader-native sensitivities. Primary G2 membership is US birth plus any named-country-born parent. One-US-parent and two-same-country-parent profiles were added transparently after first results as exploratory checks, not new confirmatory tests. No central research question or causal protocol was changed.

Acquisition and locked analysis specification are in [the lane](../infra/immigration-fiscal/latam_comparison_2026_09_17/README.md); findings and explicit uncertainty in [the memo](../research/immigration-latam-benchmark-comparison-2026-09-17.md). Larger income tables do not fill national country-specific trust/crime gaps.

## Evidence and correction

The new analysis separates regional averages from country exceptions and shows sensitivity to parental composition. Both-Cuban-parent estimates approach the main benchmark, while Mexican-parent gaps remain substantial. Current sample precision does not establish corrected all-four-outcome noninferiority for any country.

The [OI race paper §III.A](https://opportunityinsights.org/wp-content/uploads/2018/04/race_paper.pdf) explicitly describes an authorized-family target frame, stronger selection than merely “legal status is not released.” Newly acquired native-mother tables improve context but do not establish two native parents or white third-plus ancestry. Country-income and race/geography crime tables cannot be merged into missing country-crime observations. This refines source scope, without retrospectively changing the paper's numbers.

## Revisit if

The user specifies a different benchmark; sufficiently large national grandparent-origin data become available; verified cross-year survey covariance improves precision; or matched country/outcome data alter the findings. Genetic attribution requires a separate identifying design and is not inferred from these descriptive comparisons.

## Supersedes

No earlier numerical result is erased. Narrows the OI transfer scope and replaces the older descriptive CPS tables as the preferred current country-economic comparison. Earlier memo revisions link here.
