# IQ Sex Differences - Add Health Evaluation Invariance Pilot

**Date:** 2026-03-07  
**Purpose:** run the first joint measurement/prediction invariance pilot on a late-school evaluation surface.

Primary artifacts:

- `sources/iq-sex-diff/addhealth_evaluation_invariance_pilot.py`
- `sources/iq-sex-diff/data/addhealth/addhealth_evaluation_invariance_sample.parquet`
- `sources/iq-sex-diff/data/addhealth/addhealth_evaluation_model_compare.tsv`
- `sources/iq-sex-diff/data/addhealth/addhealth_evaluation_measurement_stats.tsv`
- `sources/iq-sex-diff/data/addhealth/addhealth_evaluation_measurement_estimates.tsv`
- `sources/iq-sex-diff/data/addhealth/addhealth_evaluation_group_stats.tsv`
- `sources/iq-sex-diff/data/addhealth/addhealth_evaluation_group_estimates.tsv`
- `sources/iq-sex-diff/data/addhealth/addhealth_evaluation_factor_scores.parquet`
- `sources/iq-sex-diff/data/addhealth/addhealth_evaluation_prediction_models.tsv`

## Why this target

The public `Add Health` branch is the cleanest currently local late-school evaluation family with:

1. multiple subject-grade indicators
2. baseline verbal/background controls
3. later attainment outcomes

[SOURCE: `research/iq-sex-differences-addhealth-school-surface-first-pass.md`; `sources/iq-sex-diff/data/addhealth/addhealth_school_surface_extract.parquet`]

That makes it the right first place to ask two questions:

1. does the grade family behave like a clean latent evaluation surface by sex?
2. does that latent surface predict later attainment differently by sex?

[INFERENCE]

## Important limitation up front

This is an **approximate** invariance pilot, not a final multi-group SEM result.

Why:

1. the CFA stage is unweighted
2. grades are treated as continuous rather than ordinal
3. the current local Python path does not yet implement the weighted joint multi-group SEM that would be the publication-grade endpoint

[SOURCE: `research/iq-sex-differences-irt-tooling-feasibility.md`; `sources/iq-sex-diff/addhealth_evaluation_invariance_pilot.py`]

So the right use is:

- to test whether the branch is promising or structurally weak
- not to issue a final invariance verdict

[INFERENCE]

## Measurement stage

Common sample:

- `n = 2,036`

[SOURCE: `sources/iq-sex-diff/data/addhealth/addhealth_evaluation_model_compare.tsv`]

Two candidate structures were compared:

1. one-factor `evaluation`
2. two-factor `quant_eval + verbal_eval`

Fit summary:

| model | chi2 | df | CFI | TLI | RMSEA | AIC | BIC |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `one_factor` | `265.03` | `3` | `0.847` | `0.695` | `0.207` | `13.74` | `53.07` |
| `two_factor` | `310.84` | `3` | `0.821` | `0.642` | `0.225` | `13.69` | `53.03` |

[SOURCE: `sources/iq-sex-diff/data/addhealth/addhealth_evaluation_model_compare.tsv`]

The message is not “two-factor wins clearly.” It does not.

The message is:

1. neither simple latent representation fits especially well
2. the grade family is highly coherent but not cleanly summarized by a trivial latent scalar under this approximation

[INFERENCE]

That is already informative because it means the late-school evaluation family should not be treated lazily as one clean latent ability proxy. [INFERENCE]

## Group structure

Even though global fit is weak, the sex-specific loading geometry is fairly similar under the two-factor approximation:

Male:

1. `science_grade_z ~ quant_eval = +0.768`
2. `history_grade_z ~ verbal_eval = +0.788`
3. `quant_eval ~~ verbal_eval = +0.953`

Female:

1. `science_grade_z ~ quant_eval = +0.806`
2. `history_grade_z ~ verbal_eval = +0.772`
3. `quant_eval ~~ verbal_eval = +0.909`

[SOURCE: `sources/iq-sex-diff/data/addhealth/addhealth_evaluation_group_estimates.tsv`]

So the first obstacle is not obvious sex-specific loading drift. It is that the broad grade family itself is too coarse for a clean low-dimensional latent summary under the current approximation. [INFERENCE]

## Prediction stage

Using the chosen two-factor approximation, factor scores were then entered into weighted clustered models for:

1. `h4ed2`
2. `some_college_plus`

with the same background/verbal block already validated on the public `Add Health` branch:

1. `female`
2. `age_w2`
3. `pvtstd1`
4. `parent_ed_max`
5. `any_parent_professional`
6. `any_parent_public_assist`
7. `resident_mother`
8. `resident_father`

[SOURCE: `research/iq-sex-differences-addhealth-school-surface-first-pass.md`; `sources/iq-sex-diff/data/addhealth/addhealth_evaluation_prediction_models.tsv`]

Key interaction results:

- `h4ed2`
  - `quant_eval_factor:female = +0.426`, `SE = 0.604`
  - `verbal_eval_factor:female = -0.488`, `SE = 0.593`
- `some_college_plus`
  - `quant_eval_factor:female = -0.020`, `SE = 0.149`
  - `verbal_eval_factor:female = -0.010`, `SE = 0.147`

[SOURCE: `sources/iq-sex-diff/data/addhealth/addhealth_evaluation_prediction_models.tsv`]

So under this pilot:

1. the predictive main effects are present
2. the sex interactions are not doing obvious work

[INFERENCE]

That weakens the simplest “female school surfaces are obviously inflated and pay off less” story on this public branch. [INFERENCE]

## Causal / epistemic discipline

This is not a clean causal mediation design.

What it is:

1. approximate measurement-structure check
2. approximate prediction-invariance check on a later outcome

What it is not:

1. a total-effect estimate
2. a direct-effect estimate
3. a formal weighted multi-group invariance test

[SOURCE: `research/iq-sex-differences-mediator-design.md`; `research/iq-sex-differences-alpha-master-plan.md`]

`/causal-robustness` was **not** applied here. That is deliberate. The main uncertainty is latent measurement adequacy, not omitted-variable bias in an otherwise well-identified causal OLS target. [INFERENCE]

## Best current read

The pilot gives two useful results:

1. the public `Add Health` grade family is too heterogeneous to treat as a trivially clean latent evaluation scalar
2. conditional on the approximated latent grade factors, obvious sex-differential predictive slopes are not the main story

[INFERENCE]

That combination points to a stronger next move:

- move from coarse public grades to transcript-rich or recommendation-rich surfaces for the real joint measurement/prediction invariance paper

[INFERENCE]

## Stop-rule consequence

Do **not** upgrade the claim to “the evaluation family is measurement-invariant and prediction-invariant.”

That would overstate the result.

The correct upgrade is narrower:

> on the public `Add Health` branch, the first failure point is weak latent unidimensionality of the grade family, not obvious sex-differential predictive returns once that family is approximated.

[INFERENCE]
