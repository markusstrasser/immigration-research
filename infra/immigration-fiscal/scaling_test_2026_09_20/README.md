# Test of service-cost scaling

Specification recorded 2026-09-20 before estimating the new coefficients.

Question: do public-service monetary costs support a universal sublinear exponent,
and does a relationship across differently sized jurisdictions also describe the
spending response when a jurisdiction grows? This is an observational falsification
exercise, not an identified immigration shock or a replication of physical-network
scaling. No fiscal parameter is automatically replaced by a regression slope.

Primary school outcome: log current elementary/secondary operating expenditure in
2020 dollars, own-year F33 pupils as size. Existing matched district panel actually
contains 2000/2010/2019, not the five planned waves in its upstream docstring.
Main comparison: 2019 cross-section with state effects versus a balanced three-wave
district panel with district and state-by-year effects. State-clustered CR1 errors
and t critical values; unweighted primary, pupil-weighting sensitivity. Cross-section
weights use 2019 enrollment; panel and long differences use initial 2000 enrollment,
fixing weights before growth rather than weighting by current outcome.

Prespecified disconfirmation: compare slopes with1,3/4,5/6 and0.85; separately fit
districts below1000,1000–9999 and10000+ pupils; instructional spending as a distinct
outcome; 2010–2019 long differences and asymmetric growing/shrinking slopes; remove
changes exceeding0.2 absolute log points as a merger/large-change sensitivity.
Rebuild a broader finance+directory sample without the existing per-pupil spending
band or Hispanic-share completeness screen. Require positive current costs and
own-year pupils>=100, regular noncharter districts, complete states in each wave.
Keep source missing/sentinel values out of logs. Do not silently fill gaps.

Predictive test: deterministic five-fold held-out districts in the2019 cross-section.
Compare fixed exponents .75,5/6,.85,1 and a free slope, with state-specific intercepts
estimated using training rows only. Score held-out log-dollar RMSE, not in-sample
fit. Folds preserve district identity; this is prediction across districts, not
a growth forecast. Unknown test-state intercepts fail the check.

State/local functions: reuse official weighted aggregate tables, not unweighted
annual unit sums. Compare pooled cross-section with state/year fixed effects;
current operations and population, with census-wave and pre2020 sensitivities.
States are a different spatial scale from cities; failure here challenges a
universal fiscal extension, not every urban-infrastructure finding.

Interpretation gate: do not call economies of scale causal unless service quality,
prices, composition and endogenous enrollment are addressed. Similar coefficients
across methods strengthen descriptive consistency only. Divergent coefficients,
size strata or functions reject a universal coefficient for our account. Treat
statistical intervals as sampling/model intervals, not bounds on specification or
transport error. Report all planned specifications; no clipping to[0,1].

Complexity bridge: for C=aN^b, local marginal/average cost=b, while a finite removal
share s gives r=[1-(1-s)^b]/s. This requires unchanged a and a correctly chosen
geographic unit. Compute theory-only fiscal illustrations separately from fitted
school sensitivities. A national origin-share substitution is diagnostic, not a
causal estimate when settlement is uneven or services are composition-dependent.

Inputs are already acquired Census/NCES/Urban files and their existing local
builders. Raw data remain read-only. `analyze.py` records source hashes and writes
ignored derived results. School staffing/quality is not in the matched finance
panel; instructional dollars are not a quality outcome. Source and response
composition limits remain explicit in the research memo.

Execution amendment before results: held-out state-intercept support fails for
single-district jurisdictions (DC/Hawaii). Exclude DC from the main school sample;
retain Hawaii in regressions but exclude states with fewer than five districts
from five-fold prediction only. Allocate folds by deterministic district-hash rank
within state. Report the excluded states/rows and keep the unknown-intercept guard.

## Reproduction and results

Run from the repository root with the existing cached project dependencies:

```sh
UV_CACHE_DIR=/private/tmp/codex-uv-cache uv run --offline --with scipy python3 infra/immigration-fiscal/scaling_test_2026_09_20/analyze.py
UV_CACHE_DIR=/private/tmp/codex-uv-cache uv run --offline --with scipy python3 infra/immigration-fiscal/scaling_test_2026_09_20/state_analyze.py
UV_CACHE_DIR=/private/tmp/codex-uv-cache uv run --offline --with scipy python3 infra/immigration-fiscal/scaling_test_2026_09_20/verify_school.py
UV_CACHE_DIR=/private/tmp/codex-uv-cache uv run --offline python3 infra/immigration-fiscal/scaling_test_2026_09_20/verify_state.py
UV_CACHE_DIR=/private/tmp/codex-uv-cache uv run --offline --with scipy python3 -m unittest discover -s infra/immigration-fiscal/scaling_test_2026_09_20 -v
```

The existing upstream school and annual-account exports must be present and their
receipts current. Their acquisition and rebuild commands remain in their own lanes;
this lane acquires no new raw data. `analyze.py` verifies the annual-account source
receipts before computing a theoretical fiscal illustration. State inputs are pinned
by the existing administration-response input manifest; 12 national expenditure
anchors must match the independently acquired 2022 Census API exactly.

Outputs in ignored `derived/`: 54 school coefficient rows, two-sample held-out
prediction and coverage tables, 16 theory-only fiscal rows; `state/` contains
350 state-year observations, 60 coefficients and national reconciliation. School
current dollars are 2020-real; state current operations are nominal with year effects.
None is a net fiscal balance until explicitly joined to the separate annual account.

Independent verifiers reproduce the eight primary school regressions and all
60 state regressions using closed-form residualization rather than the producers'
estimators. Guards reject missing/duplicate models, nonfinite numbers and source
or output drift. Four tests cover weighted absorption versus explicit dummy OLS,
held-out prediction, finite-removal arithmetic and corrupt verification exports.

See [empirical interpretation](../../../research/immigration-service-scaling-test-2026-09-20.md)
and [theory evidence](../../../notes/immigration-scaling-theory-evidence-2026-09-20.md).
The [annual account](../../../research/immigration-complete-annual-account-2026-09-20.md)
keeps its CBO-informed category comparison: these descriptive regressions do not
identify an extra discount. Review repaired nonfinite/coverage acceptance guards;
that correction changes no finite coefficient in the executed results.
