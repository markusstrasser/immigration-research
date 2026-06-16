# IQ Sex Differences - Add Health Evaluation Invariance Prototype

**Date:** 2026-03-07  
**Purpose:** provide a cleaner holdout for the `evaluation` family using a four-indicator public school-grade factor with later attainment outcomes.

Primary artifacts:

- `sources/iq-sex-diff/data/mtmm/addhealth_evaluation_model_fit.tsv`
- `sources/iq-sex-diff/data/mtmm/addhealth_evaluation_loadings.tsv`
- `sources/iq-sex-diff/data/mtmm/addhealth_evaluation_prediction_models.tsv`
- `sources/iq-sex-diff/data/mtmm/addhealth_evaluation_multigroup_summary.json`

Code:

- `sources/iq-sex-diff/addhealth_evaluation_invariance_prototype.py`

Companion files:

- `research/iq-sex-differences-addhealth-school-surface-first-pass.md`
- `research/iq-sex-differences-school-outcome-interactions.md`
- `research/iq-sex-differences-hsls-mtmm-invariance-prototype.md`

---

## Scope

This is a holdout and triangulation pass for the `evaluation` family.

It asks:

1. does a simple latent evaluation factor fit well by sex?
2. does its later attainment prediction look invariant by sex?

This is not a transcript-strength model and not a causal decomposition. [INFERENCE]

## Data

Indicators:

1. `math_grade_points`
2. `english_grade_points`
3. `history_grade_points`
4. `science_grade_points`

Outcomes:

1. `bachelor_plus`
2. `some_college_plus`

[SOURCE: `sources/iq-sex-diff/data/addhealth/addhealth_school_surface_extract.parquet`; `sources/iq-sex-diff/addhealth_evaluation_invariance_prototype.py`]

## Measurement result

A one-factor evaluation model fits well in the pooled sample and within both sexes.

Fit:

1. pooled `CFI = 0.997`, `RMSEA = 0.038`
2. male `CFI = 0.998`, `RMSEA = 0.026`
3. female `CFI = 0.994`, `RMSEA = 0.052`

[SOURCE: `sources/iq-sex-diff/data/mtmm/addhealth_evaluation_model_fit.tsv`]

Loadings stay in the same order by sex, with somewhat stronger non-math loadings for males:

1. male `science_grade_points = 1.222`
2. female `science_grade_points = 1.084`

[SOURCE: `sources/iq-sex-diff/data/mtmm/addhealth_evaluation_loadings.tsv`; `sources/iq-sex-diff/data/mtmm/addhealth_evaluation_multigroup_summary.json`]

Best read:

1. the evaluation family is coherent as a latent factor
2. exact loading equality is not established here
3. but this does not look like a one-sex-only factor

[INFERENCE]

## Prediction result

### Some college

The evaluation factor predicts `some_college_plus` strongly, and the sex interaction is near zero:

1. weighted `female_evaluation p = 0.271`
2. unweighted `female_evaluation p = 0.762`

[SOURCE: `sources/iq-sex-diff/data/mtmm/addhealth_evaluation_prediction_models.tsv`]

That is the cleaner prediction-invariance result in this cohort. [INFERENCE]

### Bachelor’s degree

The evaluation factor again predicts strongly, but the sex interaction is mixed:

1. weighted `female_evaluation = -0.354`, `p < 0.001`
2. unweighted `female_evaluation = -0.334`, `p = 0.154`

[SOURCE: `sources/iq-sex-diff/data/mtmm/addhealth_evaluation_prediction_models.tsv`]

Best read:

1. bachelor prediction non-invariance is plausible
2. but the public holdout does not harden it on unweighted evidence alone

[INFERENCE]

## Why this matters

This holdout complements the `HSLS` prototype.

`HSLS` says:

1. tested math and evaluation math are distinct latent families
2. prediction invariance can fail, especially for STEM

`Add Health` says:

1. the evaluation family itself is real and coherent
2. some outcomes look predictively invariant, others do not

[SOURCE: `research/iq-sex-differences-hsls-mtmm-invariance-prototype.md`; `sources/iq-sex-diff/data/mtmm/addhealth_evaluation_model_fit.tsv`; `sources/iq-sex-diff/data/mtmm/addhealth_evaluation_prediction_models.tsv`]

## Limitation

This is still a public-use, grade-only evaluation factor. It does not adjudicate transcript strength versus evaluation residual. That remains the job of the `AHAA` restricted-data branch. [SOURCE: `research/iq-sex-differences-addhealth-ahaa-application-scope.md`]
