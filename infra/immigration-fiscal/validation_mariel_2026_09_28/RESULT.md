**Verdict:** One shared set of donor weights makes the school-budget predictions
accounting-coherent, but both fixed joint specifications lose to a simple baseline
on pretreatment prediction. Do not use this construction to claim a validated
Mariel fiscal balance. This failure neither proves zero immigration costs nor
adjudicates every specification in the published Mariel literature. [CALCULATION / INFERENCE]

September 28, 2026. [Design.md](Design.md) fixed the comparison before these new
joint fits were scored. Earlier separate fits and the historical sources were
already inspected: this is retrospective validation. No national parameter changed.

## Pretreatment prediction

The primary sample is Dade plus 28 donors with consistently observed June 30 fiscal
dates. Train on 1970–1976, predict 1977–1979, before the 1980 Mariel event. Seven
primitive budget lines share nonnegative weights summing to one; the same weights
predict all reported totals and accounting residuals. The baseline freezes Dade's
1976 component mix and scales it with average donor expenditure growth. All methods
may observe contemporaneous donor outcomes, but no later Dade outcome enters the
fit or prediction. [CODE: `joint_budget.py`; DATA: upstream GFD panels]

| Fixed rule | Joint normalized RMSE | Total-expenditure normalized RMSE |
|---|---:|---:|
| Equal relative component importance | 39.75% | 44.59% |
| Common total-revenue unit for all components | 26.65% | 8.49% |
| Donor-growth baseline | **16.02%** | **7.59%** |
| Relative-components fit, largest donor deleted | 44.24% | 40.15% |
| Common-unit fit, largest donor deleted | 32.23% | 10.13% |

The joint score is the root mean squared error over six endpoints and three held-out
years, after dividing each endpoint's error by its treated training mean (floored
at 1% of training total revenue). Endpoints are revenue, expenditure, current
operations, own-source revenue and federal/state transfers. This gives correlated
endpoints explicit importance; it is not a percentage fiscal loss or confidence
interval. Raw dollar and endpoint errors remain in `derived/june30_scores.csv`.
[CALCULATION]

The broader pool, retaining its unresolved fiscal-calendar limitation, has 44
complete donors and the same ordering: joint scores 41.00% and 26.53%, versus
16.26% for the baseline. One otherwise eligible unit (`85002601`) lacks complete
primitive endpoints and is reported as excluded. Completeness and calendar screens
use later source availability, so the eligible panel itself is retrospective.
[CALCULATION: `derived/summary.json`, `full_timing_diagnostic_scores.csv`]

## What accounting coherence does and does not establish

Revenue components almost sum to reported revenue, with discrepancies up to one
source unit ($1,000). The reported expenditure total can differ materially from the
selected current, capital and interest components. The generator carries that
unclassified residual explicitly rather than guessing its meaning or forcing it
to zero. Shared weights preserve both identities and revenue minus expenditure
to numerical tolerance. This is implementation validation, not evidence that the
counterfactual predicts well. [CODE / DATA]

After refitting on 1970–1979, the mean annual 1981–1990 total-expenditure gap
`actual / predicted − 1` is +54.48% under relative component importance, +31.48%
under the common unit and +21.31% under donor growth. These are descriptive model
gaps, **not validated causal effects**; failed pretreatment prediction and weighting
sensitivity prevent that upgrade. The source units are nominal thousands in each
fiscal year; the script retains annual series and does not call their sum a real
cumulative cost. [CALCULATION: `derived/june30_annual.csv`; INFERENCE]

Donor-placebo post/pre expenditure-RMSPE ranks are 6 of 29 (relative components)
and 3 of 29 (common unit), counting Dade and ties at least as large. Every placebo
excludes Dade as a donor, and the tables retain pre-fit quality. These ranks are
conditional diagnostics, not randomization p-values: districts were not randomly
assigned and fit quality differs. [CALCULATION: `derived/june30_placebos.csv`]

Even a well-predicted local school financing balance would not be a national fiscal
balance. State/federal grants are local revenue but transfers within the national
government system. Nor would this one episode identify a long-run nationwide
removal of today's Mexican-origin resident union. [INFERENCE]

## Reproduction and verification

```sh
OPENBLAS_NUM_THREADS=1 \
uv run --no-project --with scipy --with pandas --with numpy python3 \
  infra/immigration-fiscal/validation_mariel_2026_09_28/joint_budget.py
OPENBLAS_NUM_THREADS=1 \
uv run --no-project --with scipy --with pandas --with numpy python3 -m unittest discover \
  -s infra/immigration-fiscal/validation_mariel_2026_09_28 -p 'test_*.py' -v
```

Six tests cover a known convex mixture, nonfinite input rejection, invariance to
later treated outcomes, accounting identities, discriminatory scoring and invalid
scoring-normalizer rejection. The
optimizer also fails on nonconvergence, invalid weights or excessive convex
simplex duality gap. The full run and tests exit successfully. Source and design
hashes are retained in `derived/summary.json`; outputs are ignored and reproducible.
Native-First: NumPy/pandas and SciPy constrained least squares on existing pinned
source panels; no replacement dataset or synthetic outcomes. [EXECUTION]
Update 2026-09-28: `derived/` outputs are now tracked in git.

Source: Pierson, Hand and Thompson (2015),
[Government Finance Database](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0130119),
the pinned S7 data used by `causal_execution_2026_09_20/mariel/scm_reconstruction.py`.
This is our new joint construction; it is not represented as an exact reproduction
of a published Mariel estimator. [SOURCE / METHOD]

Covered: both fixed weightings, joint identities, pretreatment holdout, matched
baseline, all endpoints, donor deletion, placebo fits and calendar sensitivity.
Skipped: causal identification of the post-event gap, quality effects and national
translation; those require evidence this construction does not supply. [SCOPE]
