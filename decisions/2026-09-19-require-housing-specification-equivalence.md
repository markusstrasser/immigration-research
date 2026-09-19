# 2026-09-19: Require equivalent housing specifications before an era-change claim

## Context

The September19 housing memo and confidence-ladder155 called the modern exercise an exact reproduction and explained its disagreement with Saiz–Wachter2011 using measurement and changed diffusion. Reading the full original specification and online appendix reveals simultaneous differences in controls, outcome, sample, inference and gravity construction.

## Alternatives considered

1. Keep the era-change/failed-reproduction interpretation because the modern negative gradient is fragile. This confuses the modern study's sensitivity with a test of the original study.
2. Treat the original estimate as verified today. This assumes transportability that the current checks do not establish.
3. Retain both bodies of evidence, withdraw exact equivalence, reproduce original data first and then change specifications separately.

## Decision

Adopt3. The completed modern comparisons remain a contemporary sensitivity exercise. They do not produce an identified composition-amenity price or establish that the historical relationship disappeared. The original-data replay is pending archive download, not a failed replication. This changes claim confidence, not the central research question or welfare weights.

## Evidence

[Source contract and computed comparisons](../research/immigration-hedonic-replay-2026-09-19.md), including the original appendix's β1.6 gravity convention and median-price robustness; independent full-dummy WLS/IV/first-stage checks of the new modern bridge.

## Revisit if

The original data and executable code reproduce the published targets and a comparison holding measurement, controls and sample definitions constant identifies the source of the modern discrepancy. A failed exact replay must first distinguish data/version/coding differences from a substantive failure.

## Supersedes

The exact-reproduction and established-measurement-explanation ratings in confidence-ladder155 and the September19 housing memo. Original numbers remain available with dated corrections.

## Follow-through after authorized archive acquisition, September 19

The original `.dta` and both author `.do` files are now acquired and hash-registered. Python translation recovers all six Table1 coefficients/SEs, columns5/6 F and Hansen J p-values, with independent full-dummy estimator checks. Historical mean/median comparisons on identical21,681 rows are both negative. The earlier pending-download statement describes the decision's initial state.

**Interpretation update:** preserve the historical result as reproduced on its prepared data. Modern sensitivity does not establish its disappearance. Code-versus-table differences are bounded:43 rather than44 baseline controls, column1 N34,835 rather than34,833, appendix first-stage sample35,120, and unresolved column4 F76.01. No native Stata execution or upstream source-data reconstruction is claimed.

The old modern estimator's moment quadratic at the2SLS coefficient is not the documented efficient-GMM Hansen J. Its generator now fails closed with missing J and explicit status; old rejection claims are withdrawn from verified evidence while their outputs remain preserved. Correct original-data J is independently calculated. A new modern GMM analysis is deferred because this archive reproduction does not establish an appropriate modern identification design; it is unnecessary for the surviving outcome-sensitivity conclusion.

[Computed evidence and source record](../research/immigration-hedonic-replay-2026-09-19.md).
