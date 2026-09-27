**Verdict:** Earlier enrollment-response estimates improve later spending prediction
relative to a proportional response carrying the same kind of estimated trend.
They do not consistently beat simple frozen-spending or proportional baselines.
Spending and teacher staffing adjust differently in growing and shrinking districts;
neither observed resources nor pupil/teacher ratios validate achievement or a
causal long-run removal saving. [CALCULATION / INFERENCE]

September 28, 2026. Retrospective tests using held source years, with [design](Design.md)
written before this lane scored them. No account parameter or national total changed.

## 1. Earlier school-finance rules predict a later interval

Fit FY2000→2010 changes; predict FY2010→2019 changes conditional on actual later
enrollment. Eligible districts are regular/noncharter, have at least100 own-F33
pupils and positive finite spending. The model fits12234 training districts and
scores12011 test districts for current spending, across51 jurisdictions. Training
membership never depends on2019 spending. The instructional test has12010 test
districts. CPI-U deflates money to2020 dollars; later CPI is a declared common
conditional input, not a school-spending trend fitted to test outcomes.
[DATA: `derived/coverage.csv`; CODE: `load_primary`, `pair` in `validate.py`]

| Frozen rule | District log RMSE | Initial-pupil-weighted log RMSE | District mean absolute level error, $m |
|---|---:|---:|---:|
| Unchanged real spending | .1945 | .1863 | 6.50 |
| Proportional enrollment, no trend | .1926 | **.1693** | **5.86** |
| Training state trend only | .2108 | .2023 | 7.89 |
| Proportional enrollment + training state trend | .2015 | .1817 | 7.54 |
| Free response + training state trend | **.1820** | .1747 | 7.09 |
| Separate growth/shrink response + training state trend | **.1815** | .1737 | 7.07 |

The first and third numeric columns use district-unweighted fitting/scoring;
the middle column uses initial-pupil-weighted fitting/scoring. Every arm uses the
same test districts within an outcome. State trends are estimated from each arm's
training residual means and scaled9/10; no test-year school-spending trend enters.
Dollar predictions exponentiate log predictions without post-score bias correction.
[CALCULATION: `derived/scores.csv`, all-stratum current-spending rows]

The free training slope is**.683 unweighted / .817 pupil-weighted**. Its improvement
over proportional-with-training-trend is .0196/.0070 log RMSE. State-cluster
bootstrap intervals for the differences (free minus proportional) are
**[−.0286,−.0103] / [−.0126,−.0006]**, using1000 draws and fixed trained rules.
These are uncertainty about geographic score aggregation conditional on the fit,
not confidence intervals for a causal response or uncertainty from refitting.
[CALCULATION: `derived/rules.json`, `derived/paired_score_intervals.csv`]

**Retain the adverse comparisons.** The free model's unweighted aggregate spending
prediction is4.27% above actual, versus proportional-no-trend8.23% below. Its
district average absolute growth error is14.96 percentage points, versus14.28 for
proportional-no-trend. Log level errors equal log change errors because initial
spending is known; those are not independent validations. The lower dollar error
of the simple baseline and the weighted ranking prevent a general model victory.
[CALCULATION: `derived/scores.csv`]

The growth/shrink split is consequential. For4462 growing districts, proportional
without trend scores**.156**, versus free-with-trend.184; for7511 shrinking
districts, unchanged real spending scores**.167**, versus free-with-trend.181 and
proportional-no-trend.212. The small-change subset (9657 districts, absolute log
enrollment change≤.2) also favors simple baselines: frozen.161, proportional.163,
free-with-trend.174. These strata were declared before scoring, and every result
is retained. This supports heterogeneous adjustment and unstable secular trends,
not a single universally superior cost exponent. [CALCULATION / INFERENCE]

## 2. Spending and teacher FTE on the same districts

A separate panel joins CCD fall2000/2018/2023 teacher FTE to F33 FY2001/2019/2024
finance and own-year pupils. Training spans18 years; testing spans5 years and
crosses COVID. All three outcomes use identical eligible rows in each interval.
Public F33 regular district definitions differ from the first panel's CCD
regular/noncharter screen. Spending here is in2024 real dollars. [DATA / CODE]

One support failure was caught before scores: all671 rows in the New Jersey
fall2000 directory have teacher-FTE sentinel−1. The training-state intercept is
therefore unavailable. The guard stopped; the documented availability amendment
excludes525 New Jersey test districts (1,311,116 initial pupils) from **all joint
prediction arms**. They remain in the separate observed-resource table. No
unknown-state prediction is silently filled. Final fit11446 districts/50
jurisdictions; score11613/50. [DATA: `derived/coverage.csv`; `Design.md` amendment]

Current-spending log RMSE is.1416 for the free response versus.1501 for proportional
with training trend (unweighted); .1112 versus.1177 weighted. Frozen real spending
is.1501/.1238; proportional-no-trend.1595/.1441. Teacher-FTE prediction adds little
over frozen staffing: weighted log RMSE**.1207 free versus .1211 frozen**; free
aggregate teachers are4.64% below actual, frozen1.98% below. This is not a strong
overall staffing-forecast success. [CALCULATION: `derived/scores.csv`]

The **12138 matched districts**, including New Jersey, show:

| FY2019→2024 matched group | Pupils | Current spending, real | Instruction, real | Teacher FTE | Pupils per teacher, start→end |
|---|---:|---:|---:|---:|---:|
| All | −3.46% | +5.50% | +2.83% | +1.99% | 16.01→15.15 |
| Growing districts | +7.33% | +11.41% | +9.49% | +9.60% | 15.90→15.57 |
| Shrinking districts | −7.32% | +3.63% | +0.75% | −0.75% | 16.05→14.99 |

These are changes of pooled levels, not average district percentage changes.
The corresponding teacher/pupil and instructional resource channels overlap:
do not add them as separate welfare losses. School consolidation, reclassification,
different pupil needs, labor prices, policy and pandemic support remain potential
drivers. The code does not equate these observed changes with immigrant effects.
[CALCULATION: `derived/joint_observed.csv`; INFERENCE]

## 3. Quality is measured separately, and does not follow mechanically

The held ECLS1998/2011 extracts contain child achievement and internal school IDs,
but no external CCD/LEA identifier with which to join the district finance panel.
Their fields and hashes are inventoried in `derived/field_inventory.json`. The
original three-wave finance files also lack building capacity or classroom occupancy.
Teacher FTE supplies a pupil/teacher ratio; it does not measure either class size
or vacant physical capacity. [DATA / MEASUREMENT LIMIT]

An additional compatible *state-level* cross-check was possible: match51 state/DC
aggregates of the resource panel to2019/2024 NAEP grade4/8 math/reading. The matched
districts cover73.6–100% of eligible regular-F33 pupils by state in2019 and72.4–100%
in2024. NAEP represents public-school grade-specific populations beyond these
matched districts. Retain the full state table and coverage rather than calling
this a pupil-level joint sample. [CALCULATION: `derived/state_resource_quality.csv`]

National-public NAEP mean scores fell **2.70 points in grade4 mathematics, 8.75 in
grade8 mathematics, 5.17 in grade4 reading, and 5.34 in grade8 reading**. Independent-
cycle difference SE approximations are.36/.46/.42/.47 respectively. Across state/DC
point estimates,49 of51 fall in grade4 reading;46 states/DC have both a falling
pupil/teacher ratio in the matched resource sample and falling grade4 reading.
These descriptive signs are not49 significant declines or evidence that additional
teachers caused lower scores. The simple inference is narrower: improved measured
staffing ratios did not guarantee stable observed achievement across this pandemic
interval. The test cannot attribute the achievement change to immigration or
separate service quality from composition and other shocks.
[DATA: `derived/naep_national.csv`, `derived/state_resource_quality.csv`; INFERENCE]

## Reproduction, provenance and coverage

Run from the main repository, substituting the script path when working in a worktree:

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/validation_schools_2026_09_28/validate.py --source-root /Users/alien/Projects/immigration-research
uv run --no-project python3 -m unittest discover -s infra/immigration-fiscal/validation_schools_2026_09_28 -p 'test_*.py' -v
```

Seven guard tests pass: train-year leakage, interval membership independence,
reachable baseline wins, annualized trend arithmetic, duplicate keys, unknown state
handling and hand-calculated level/change scores. `derived/audit.json` records
source/code/design hashes, verifies inputs unchanged during the run and fingerprints
all exported outputs. It is written only after successful completion. Raw files
were not changed. Passing these guards establishes implementation properties only.

Primary providers: [Census F33 school-finance files](https://www.census.gov/programs-surveys/school-finances/data/datasets.html),
[NCES CCD](https://nces.ed.gov/ccd/files.asp), and
[NAEP Data Service](https://www.nationsreportcard.gov/dataservice/).
The first panel uses existing Urban redistributions of Census/CCD, with source
route `https://educationdata.urban.org/api/v1/school-districts/ccd/` documented by
`school_flight_2026_09_18/pull_districts.py`. Joint finance uses the existing Census
F33 materialized panel and its pinned builder/source manifest; source raw files
were not downloaded again. NAEP query URLs are preserved in the result tables.

Covered: two frozen temporal resource tests, both fitting/scoring weight choices,
growth/shrink/small-change strata, current/instruction/teacher outcomes, geographic
score uncertainty, dollar levels and growth, same-district resource accounting,
ECLS join inventory and state achievement cross-check. Skipped: a causal immigration
shock design, building-capacity measurement, matched district achievement, and
long-run counterfactual removal validation, because these inputs/designs are not
supplied by the compatible holdings. No public payroll replacement-hiring model
is identified by teacher FTE. [COVERAGE / LIMIT]
