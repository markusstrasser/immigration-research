# IQ Sex Differences - Weighted MTMM Sensitivity

**Date:** 2026-03-10  
**Purpose:** test whether the first public latent-family prototypes survive weighting, or whether the current school-surface split is mainly an unweighted artifact.

Primary artifacts:

- `sources/iq-sex-diff/weighted_mtmm_sensitivity.py`
- `sources/iq-sex-diff/data/mtmm/weighted_mtmm_fit.tsv`
- `sources/iq-sex-diff/data/mtmm/weighted_mtmm_loadings.tsv`
- `sources/iq-sex-diff/data/mtmm/weighted_mtmm_prediction_models.tsv`

Companion files:

- `research/iq-sex-differences-hsls-mtmm-invariance-prototype.md`
- `research/iq-sex-differences-addhealth-evaluation-invariance-prototype.md`
- `research/iq-sex-differences-measurement-error-pilot.md`

---

## Scope

This is a weighted latent **sensitivity**, not full survey-weighted multigroup SEM. [INFERENCE]

The local `semopy` stack does not support design-based survey SEM directly, so this pass uses weighted covariance matrices for the measurement side and weighted outcome models for the prediction side. That is stronger than the earlier unweighted prototype but weaker than a full survey-latent solution. [SOURCE: `sources/iq-sex-diff/weighted_mtmm_sensitivity.py`; `research/iq-sex-differences-irt-tooling-feasibility.md`]

---

## Questions

1. Does the `HSLS` tested-math versus evaluation-math split survive weighting?
2. Does the `Add Health` evaluation factor survive weighting?
3. Do weighted latent proxies materially change the public prediction geometry relative to weighted composites?

---

## HSLS Measurement Result

The `HSLS` two-factor split survives weighting decisively.

Weighted pooled fit:

1. one-factor `CFI = 0.762`, `RMSEA = 0.503`
2. two-factor `CFI = 0.999`, `RMSEA = 0.056`

Weighted male fit:

1. one-factor `CFI = 0.754`, `RMSEA = 0.519`
2. two-factor `CFI = 0.99947`, `RMSEA = 0.034`

Weighted female fit:

1. one-factor `CFI = 0.780`, `RMSEA = 0.477`
2. two-factor `CFI = 0.99690`, `RMSEA = 0.080`

[SOURCE: `sources/iq-sex-diff/data/mtmm/weighted_mtmm_fit.tsv`]

That means the main latent-family claim is not riding on unweighted CFA convenience. [INFERENCE]

### Weighted loadings

The weighted group-specific two-factor loadings stay similar:

1. male `X2TXMTSCOR_z` on `tested_math = 1.146`
2. female `X2TXMTSCOR_z` on `tested_math = 1.054`
3. male `X3TGPAHIMTH_z` on `evaluation_math = 0.792`
4. female `X3TGPAHIMTH_z` on `evaluation_math = 0.781`

[SOURCE: `sources/iq-sex-diff/data/mtmm/weighted_mtmm_loadings.tsv`]

This still is not formal equality-constrained invariance, but it weakens the simple “the split is just an unweighted sample artifact” objection. [INFERENCE]

---

## Add Health Measurement Result

The weighted `Add Health` evaluation factor also survives cleanly.

Weighted pooled fit:

1. `CFI = 0.997`
2. `RMSEA = 0.034`

Weighted male fit:

1. `CFI = 0.995`
2. `RMSEA = 0.043`

Weighted female fit:

1. `CFI = 0.995`
2. `RMSEA = 0.045`

[SOURCE: `sources/iq-sex-diff/data/mtmm/weighted_mtmm_fit.tsv`]

Weighted group loadings preserve the same broad ordering seen in the unweighted holdout, with somewhat stronger non-math loadings for males:

1. male `english = 1.244`, `history = 1.195`, `science = 1.222`
2. female `english = 1.102`, `history = 1.105`, `science = 1.066`

[SOURCE: `sources/iq-sex-diff/data/mtmm/weighted_mtmm_loadings.tsv`]

So the evaluation-family claim also survives weighting. [INFERENCE]

---

## Weighted Prediction Sensitivity

Weighted latent proxies barely change the public prediction geometry.

## HSLS

`bachelor_plus`

1. weighted composite `tested = 0.1348`, `evaluation = 0.1097`
2. weighted factor proxy `tested = 0.1324`, `evaluation = 0.1125`
3. female tested interaction `0.0411 -> 0.0407`
4. female evaluation interaction `-0.0152 -> -0.0144`

`stem_degree`

1. weighted composite `tested = 0.00182`, `evaluation = 0.00246`
2. weighted factor proxy `tested = 0.00165`, `evaluation = 0.00273`
3. female tested interaction `0.00597 -> 0.00608`
4. female evaluation interaction `-0.00036 -> -0.00063`

[SOURCE: `sources/iq-sex-diff/data/mtmm/weighted_mtmm_prediction_models.tsv`]

## Add Health

`bachelor_plus`

1. weighted composite `evaluation = 0.2275`
2. weighted factor proxy `evaluation = 0.2282`
3. female interaction `-0.0068 -> -0.0073`

`some_college_plus`

1. weighted composite `evaluation = 0.1817`
2. weighted factor proxy `evaluation = 0.1834`
3. female interaction `-0.0177 -> -0.0180`

[SOURCE: `sources/iq-sex-diff/data/mtmm/weighted_mtmm_prediction_models.tsv`]

So the weighted latent-proxy upgrade is still confirmatory, not transformative. [INFERENCE]

---

## What This Hardens

1. The `HSLS` tested-versus-evaluation split survives weighting decisively. [SOURCE: `sources/iq-sex-diff/data/mtmm/weighted_mtmm_fit.tsv`]
2. The `Add Health` evaluation factor survives weighting cleanly. [SOURCE: `sources/iq-sex-diff/data/mtmm/weighted_mtmm_fit.tsv`]
3. The current public latent-family prediction geometry is not highly sensitive to replacing weighted composites with weighted loading-based latent proxies. [SOURCE: `sources/iq-sex-diff/data/mtmm/weighted_mtmm_prediction_models.tsv`]

---

## Causal-Check

**Observation:** the first latent-family prototypes were vulnerable to the objection that the split might be largely an unweighted artifact. [SOURCE: `research/iq-sex-differences-hsls-mtmm-invariance-prototype.md`; `research/iq-sex-differences-addhealth-evaluation-invariance-prototype.md`]

**Null:** once weighting is introduced, the one-factor representation will fit much better, or the weighted latent prediction geometry will differ substantially from the weighted composite geometry. [INFERENCE]

**Residual:** the null fails. Weighting leaves the main latent-family structure intact and barely changes the public prediction geometry. [SOURCE: `sources/iq-sex-diff/data/mtmm/weighted_mtmm_fit.tsv`; `sources/iq-sex-diff/data/mtmm/weighted_mtmm_prediction_models.tsv`]

**Decision impact:** the next measurement frontier is no longer “did we forget weights?” It is full survey-latent estimation, restricted transcript-theta work, or richer process-DIF reduction. [INFERENCE]

---

## Limitations

1. Weighted covariance fitting is not full survey SEM.
2. Prediction still uses weighted latent proxies rather than a joint latent-outcome model.
3. This pass does not use replicate weights.
4. This pass does not establish formal equality-constrained multigroup invariance.

[INFERENCE]
