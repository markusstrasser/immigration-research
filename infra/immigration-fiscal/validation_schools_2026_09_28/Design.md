# School spending and staffing temporal validation

Written 2026-09-28 before this lane scores held-out outcomes. This is retrospective:
the source years and related full-panel regressions were inspected in earlier work.

## Construct and target

Test whether rules fitted to earlier within-district enrollment and resource changes
predict later changes, conditional on the later *observed enrollment*. This is not
an unconditional enrollment forecast or a causal immigration/removal estimate.
Primary interval: FY2000→2010 training and FY2010→2019 testing. Target is log current
operating expenditure; instructional expenditure is a separately reported outcome.

## Inclusion and provenance

Use all 51 jurisdiction files in each wave from `school_flight_2026_09_18/_cache/dist`.
Regular, noncharter districts with at least 100 own-F33 pupils and positive finite
outcome at both ends of each interval qualify. No ethnicity completeness or
per-pupil-expenditure screen. Training eligibility uses only 2000/2010 observations;
test eligibility uses 2010/2019 observations. The two sets need not coincide.
Known test enrollment is an input, never an outcome-dependent model-selection rule.
Report source coverage, joins and included pupils. Districts moving state fail.
Duplicate district-year identifiers fail, rather than silently choosing a row.

The same eligible rows score every arm for a given outcome. The only test-outcome
screen is positive finite measurement required for a log outcome. As a declared
diagnostic, separately score absolute log enrollment changes ≤0.2; keep all-change
results primary. Missing/merged district identities and selective survival remain
limitations. These are administrative panels, not a survey respondent sample.

## Frozen models and common information

Fit log resource change = state intercept + enrollment response on training data.
Compare: (1) unchanged real resources, (2) proportional enrollment with no trend,
(3) training state trend with zero enrollment response, (4) proportional response
plus training state trend, (5) freely fitted common slope plus training state trend,
(6) separate freely fitted growth/shrink slopes plus training state trend. Each
trend is the training residual state mean conditional on that arm's slope, then
scaled by 9/10 to the test interval. Free slopes use training state-demeaned data.
Fit both district-unweighted and initial-pupil-weighted versions. Do not estimate
test-period trends or choose a model from test results. Retain all arms.

CPI-U converts money to 2020 real dollars. Later CPI is a declared known deflator,
common to every arm; no realized later school-spending trend is supplied. This
isolates resource-volume prediction conditional on the common inflation measure.

## Scores and uncertainty

Report log-change RMSE/MAE/bias, percentage-point error in resource growth, and
level-dollar MAE/RMSE plus aggregate level bias. A level prediction is the observed
initial level times exponentiated predicted log change (a log-scale central
prediction, with no post-hoc smearing). Log level and log change errors are
algebraically identical because initial levels are known; dollar errors are not
an independent validation. Both district-unweighted and initial-pupil-weighted
scores; all/growing/shrinking/unchanged and small-change strata. No significance
claim from one favorable cell. State-cluster bootstrap paired primary score
differences, 1,000 draws, fixed seed; this describes geographic score uncertainty
conditional on trained rules, not model-estimation or causal uncertainty.

Prespecified comparisons: free vs proportional-with-training-trend; asymmetric vs
free; proportional-with-training-trend vs trend-only; proportional-no-trend vs
unchanged-real-resources. A lower error is favorable prediction evidence only.
Intervals crossing zero are inconclusive, never equivalence. Fixed available
sample, no post-score stopping or threshold adjustment.

## Separate joint resource test and quality availability

Existing CCD teachers are available for fall2000/2018/2023; finance aligns to
FY2001/2019/2024. Fit on the first 18-year interval, score the next 5-year interval,
scaling training state trends by 5/18. Join current spending, instruction, teacher
FTE and pupils on the same district observations; report pupil/FTE as a capacity
proxy. Report separately from the primary pre-pandemic prediction test: the later
interval crosses COVID and fiscal support changes. This panel supplies no pupil
achievement, classroom occupancy or building capacity. Inventory available ECLS
and CCD files and document exact missing join/measurement rather than inventing
a quality measure. Positive finite teachers required; no pupil/teacher ratio
screen in primary scoring. Show the earlier 5–40 ratio band only as a sensitivity
if needed for measurement diagnostics, never as a hidden outcome screen.

## Mechanical checks and reachable falsifiers

Guard: training receives only the two training years; no test expenditure can
change fitted parameters. Witness pass: changing 2019 expenditures leaves fits
identical; fail: fitting with year2019 raises. A synthetic exact proportional
relationship must score zero for proportional and positive error for frozen
resources; constant resources give the reverse. Duplicate keys, nonfinite
predictions, an unknown test-state intercept or missing required year fails loudly.
These checks verify implementation, not empirical truth. All raw files read-only;
new code, source hashes and results remain in this lane.

## Pre-score support amendment

The unknown-state guard stopped the first run before scoring: New Jersey has
test-period joint observations but no eligible training-period joint observations.
Its fall2000 teacher source is present but does not support the required match.
Exclude unsupported states from *all prediction arms on the joint panel*, with
excluded rows and pupils reported. Preserve those districts in the separate
observed-resource table, which requires no trained intercept. The primary finance
panel is unaffected. This is an availability restriction, not outcome tuning.

Availability extension before reading quality outcomes: the active systemwide lane
holds state NAEP grade4/8 math/reading for 2019/2024. Join their all-student means
to state aggregates of the matched spending/teacher panel. Publish both endpoints,
point differences and their independent-cycle SE approximation, plus matched-pupil
coverage versus eligible F33 regular districts. This is a descriptive cross-check
of whether resources and achievement moved together, not a forecast of achievement,
not a district-level join and not an estimate of immigration's role. No regression
or causal coefficient will be fitted to these quality outcomes. Full-state public
school NAEP includes pupils beyond the matched regular-district sample.
