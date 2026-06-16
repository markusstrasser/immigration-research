# IQ Sex Differences - HSLS Weighted lavaan Measurement Pass

**Date:** 2026-03-10  
**Purpose:** replace the earlier unweighted `HSLS` latent prototype with a weighted multigroup `lavaan` pass that directly tests measurement invariance for the `tested_math` versus `evaluation_math` split, then check whether the earlier prediction story survives scalar-model factor scores.

Primary artifacts:

- `sources/iq-sex-diff/build_hsls_mtmm_lavaan_input.py`
- `sources/iq-sex-diff/hsls_mtmm_lavaan_measurement.R`
- `sources/iq-sex-diff/hsls_mtmm_lavaan_prediction.R`
- `sources/iq-sex-diff/data/mtmm/hsls_mtmm_lavaan_input.tsv`
- `sources/iq-sex-diff/data/mtmm/hsls_mtmm_lavaan_fit.tsv`
- `sources/iq-sex-diff/data/mtmm/hsls_mtmm_lavaan_lrt.tsv`
- `sources/iq-sex-diff/data/mtmm/hsls_mtmm_lavaan_parameters.tsv`
- `sources/iq-sex-diff/data/mtmm/hsls_mtmm_lavaan_prediction.tsv`
- `sources/iq-sex-diff/data/mtmm/hsls_mtmm_lavaan_sample.tsv`

Companion files:

- `research/iq-sex-differences-hsls-mtmm-invariance-prototype.md`
- `research/iq-sex-differences-weighted-mtmm-sensitivity.md`
- `research/iq-sex-differences-hsls-first-joint-invariance-target.md`

## Executive Answer

The stronger weighted `HSLS` measurement pass hardens the late-school family split.

1. A one-factor `school_math` model still fits disastrously under weighting.
2. A two-factor `tested_math` versus `evaluation_math` model fits extremely well.
3. Under weighted multigroup `lavaan`, the two-factor split remains practically stable through metric and scalar invariance constraints.
4. On scalar-model factor scores, the old broad bachelor-level sex-interaction story largely dies, while the remaining `STEM` tested-factor interaction survives only on a very thin outcome surface (`87` positives).

[SOURCE: `sources/iq-sex-diff/data/mtmm/hsls_mtmm_lavaan_fit.tsv`; `sources/iq-sex-diff/data/mtmm/hsls_mtmm_lavaan_lrt.tsv`; `sources/iq-sex-diff/data/mtmm/hsls_mtmm_lavaan_prediction.tsv`; `sources/iq-sex-diff/data/mtmm/hsls_mtmm_lavaan_sample.tsv`]

## Data

The input file freezes the current corrected `HSLS` branch:

1. measurement indicators come from the local `hsls_wedge_refinement_extract`
2. later outcomes come from `PETS`, merged on `STU_ID`
3. weights are `W3W1W2STUTR`

[SOURCE: `sources/iq-sex-diff/build_hsls_mtmm_lavaan_input.py`; `sources/iq-sex-diff/data/mtmm/hsls_mtmm_lavaan_input.tsv`]

Weighted measurement sample:

1. all: `13,506`
2. male: `6,681`
3. female: `6,825`

Later outcomes on that same measurement-complete sample:

1. `bachelor_plus`: `5,700` nonmissing, `3,633` positives
2. `stem_degree`: `6,350` nonmissing, `87` positives

[SOURCE: `sources/iq-sex-diff/data/mtmm/hsls_mtmm_lavaan_sample.tsv`]

## Measurement Result

The weighted pooled fit still rejects one school-math factor.

Pooled weighted fit:

1. one-factor robust fit: `CFI = 0.762`, `RMSEA = 0.503`
2. two-factor robust fit: `CFI = 0.999`, `RMSEA = 0.042`

[SOURCE: `sources/iq-sex-diff/data/mtmm/hsls_mtmm_lavaan_fit.tsv`]

The multigroup result is stronger than the earlier prototype because it is not just separate male/female fits. It is a formal equality-constrained weighted CFA.

Two-factor multigroup fit:

1. configural robust fit: `CFI = 0.99927`, `RMSEA = 0.0395`
2. metric robust fit: `CFI = 0.99882`, `RMSEA = 0.0354`
3. scalar robust fit: `CFI = 0.99871`, `RMSEA = 0.0303`

One-factor multigroup fit remains bad even after added constraints:

1. configural robust fit: `CFI = 0.767`, `RMSEA = 0.498`
2. metric robust fit: `CFI = 0.766`, `RMSEA = 0.377`
3. scalar robust fit: `CFI = 0.756`, `RMSEA = 0.322`

[SOURCE: `sources/iq-sex-diff/data/mtmm/hsls_mtmm_lavaan_fit.tsv`]

## Invariance Read

The weighted multigroup pass supports the narrow measurement claim:

1. the tested-versus-evaluation split is real
2. metric equality costs little in practical fit terms
3. scalar equality also remains acceptable

Formal nested comparisons:

1. two-factor metric versus configural: `p = 0.0329`
2. two-factor scalar versus metric: `p = 0.2016`

[SOURCE: `sources/iq-sex-diff/data/mtmm/hsls_mtmm_lavaan_lrt.tsv`]

With this sample size, the metric test is sensitive enough to detect small departures, so the practical fit change matters more than the bare `p` value here. The robust `CFI` drop from two-factor configural to metric is about `0.00044`, and the scalar step is smaller still. That is consistent with “close enough for a first public scalar factor-score pass,” not with “groups are fundamentally incomparable.” [INFERENCE]

## Boundary Caveat

The model is not perfectly clean.

In the weighted configural two-factor fit, `X3TGPAMAT_z` shows a small negative residual variance in both groups:

1. male residual variance: `-0.011`
2. female residual variance: `-0.076`

[SOURCE: `sources/iq-sex-diff/data/mtmm/hsls_mtmm_lavaan_parameters.tsv`]

That is a Heywood-style boundary warning, and it means the exact indicator-level variance decomposition inside the evaluation factor should not be overread. It does **not** rescue the one-factor model, and it does **not** make the tested-versus-evaluation split disappear. The safer read is that the evaluation side is very tight and close to locally saturated with only two indicators. [INFERENCE]

## Prediction Follow-up

The factor-score pass weakens the earlier broad prediction-noninvariance story.

For `bachelor_plus`:

1. `evaluation_factor` remains positively predictive (`0.323`, `p < 0.001`)
2. `female:tested_factor` is not significant (`p = 0.487`)
3. `female:evaluation_factor` is not significant (`p = 0.601`)

[SOURCE: `sources/iq-sex-diff/data/mtmm/hsls_mtmm_lavaan_prediction.tsv`]

So the stronger measurement-aware pass no longer supports a broad bachelor-level sex-differential return claim on this public branch. [INFERENCE]

For `stem_degree`:

1. `female:tested_factor = 0.825`, `p = 0.0208`
2. `female:evaluation_factor` is null (`p = 0.946`)
3. the outcome has only `87` positives

[SOURCE: `sources/iq-sex-diff/data/mtmm/hsls_mtmm_lavaan_prediction.tsv`; `sources/iq-sex-diff/data/mtmm/hsls_mtmm_lavaan_sample.tsv`]

So the only surviving outcome-specific non-invariance signal is still the `STEM` tested-factor interaction, and even that must be read as a thin-sample stress-test result rather than a hardened general return difference. [INFERENCE]

## What This Changes

### Harder claim

The `HSLS` late-school surface-family result is no longer just an unweighted prototype. The project now has a weighted multigroup CFA showing that:

1. one-factor `school_math` is inadequate
2. two-factor `tested_math` versus `evaluation_math` is the right first public representation
3. cross-sex comparability on the two-factor measurement side is close enough to support scalar factor-score work

[SOURCE: `sources/iq-sex-diff/data/mtmm/hsls_mtmm_lavaan_fit.tsv`; `sources/iq-sex-diff/data/mtmm/hsls_mtmm_lavaan_lrt.tsv`]

### Softer claim

The prediction branch is now narrower than the earlier prototype implied.

1. broad bachelor-level interaction claims should be softened
2. the remaining `STEM` tested-factor signal stays alive, but only on a very sparse binary outcome
3. the repo should stop talking as if public `HSLS` already shows a broad stable sex-differential prediction geometry

[SOURCE: `sources/iq-sex-diff/data/mtmm/hsls_mtmm_lavaan_prediction.tsv`; `sources/iq-sex-diff/data/mtmm/hsls_mtmm_lavaan_sample.tsv`]

## Limits

1. This is still not a joint latent categorical-outcome SEM.
2. It still does not use replicate weights or full survey-design SEM.
3. The evaluation factor still has a boundary warning because it is built from two very tight grade indicators.
4. The `STEM` outcome is too sparse to carry a broad headline by itself.

[INFERENCE]
