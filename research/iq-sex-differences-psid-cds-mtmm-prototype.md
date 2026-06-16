# IQ Sex Differences - PSID CDS MTMM Prototype

**Date:** 2026-03-07  
**Purpose:** run the smallest viable trait-versus-method latent prototype on public data.

Primary artifacts:

- `sources/iq-sex-diff/psid_cds_mtmm_prototype.py`
- `sources/iq-sex-diff/data/psid/psid_cds_mtmm_2002_sample.parquet`
- `sources/iq-sex-diff/data/psid/psid_cds_mtmm_2002_model_compare.tsv`
- `sources/iq-sex-diff/data/psid/psid_cds_mtmm_2002_estimates.tsv`
- `sources/iq-sex-diff/data/psid/psid_cds_mtmm_2002_group_stats.tsv`
- `sources/iq-sex-diff/data/psid/psid_cds_mtmm_2002_group_estimates.tsv`

## Setup

The public `PSID CDS 2002` teacher surface is the cleanest currently local trait/method prototype because it contains:

1. tested math: `applied_problems_std`
2. tested reading: `broad_reading_std`
3. teacher-rated math: `teacher_math_ability`
4. teacher-rated reading: `teacher_reading_ability`

[SOURCE: `sources/iq-sex-diff/data/psid/psid_cds_panel.parquet`; `sources/iq-sex-diff/data/psid/psid_cds_teacher_2002_gaps.tsv`; `sources/iq-sex-diff/psid_cds_teacher_pass.py`]

The analytic sample is `n = 659` after requiring all four indicators and positive child weights. [SOURCE: `sources/iq-sex-diff/data/psid/psid_cds_mtmm_2002_model_compare.tsv`]

## Models compared

Three models were fit on standardized indicators:

1. `one_factor`
   - one general factor for all four indicators
2. `two_trait`
   - `math_trait` measured by test math and teacher math
   - `reading_trait` measured by test reading and teacher reading
3. `two_trait_method`
   - same two trait factors
   - plus same-method correlated residuals for:
     - test math with test reading
     - teacher math with teacher reading

[SOURCE: `sources/iq-sex-diff/psid_cds_mtmm_prototype.py`]

This is a correlated-uniqueness MTMM prototype, not a full CT-CM model. That choice is deliberate because the four-indicator public surface is too small for a richer trait-plus-method model without bad identification. [INFERENCE]

## Fit comparison

Model fit summary:

| model | chi2 | df | CFI | TLI | RMSEA | AIC | BIC |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `one_factor` | `175.65` | `3` | `0.728` | `0.457` | `0.296` | `13.47` | `44.90` |
| `two_trait` | `286.06` | `3` | `0.555` | `0.109` | `0.379` | `13.13` | `44.57` |
| `two_trait_method` | `53.15` | `1` | `0.918` | `0.508` | `0.282` | `17.84` | `58.26` |

[SOURCE: `sources/iq-sex-diff/data/psid/psid_cds_mtmm_2002_model_compare.tsv`]

The absolute fit is still imperfect. But the important comparison is that the trait-plus-method prototype fits materially better than either the one-factor or trait-only models. [INFERENCE]

## Parameter geometry

In the preferred prototype:

1. teacher-method covariance is clearly positive:
   - overall: `teacher_math_z ~~ teacher_reading_z = +0.480`
2. trait correlation is high:
   - `math_trait ~~ reading_trait = +0.814`
3. teacher indicators load meaningfully but not identically on the trait factors:
   - `teacher_math_z ~ math_trait = +0.395`
   - `teacher_reading_z ~ reading_trait = +0.401`

[SOURCE: `sources/iq-sex-diff/data/psid/psid_cds_mtmm_2002_estimates.tsv`]

So the first latent prototype does **not** behave like one broad child-performance factor. It behaves like overlapping math/reading traits with a nontrivial teacher-rating method component layered on top. [INFERENCE]

## Sex-specific follow-up

The preferred prototype was then fit separately by sex.

Female group:

1. `teacher_math_z ~ math_trait = +0.469`
2. `teacher_reading_z ~ reading_trait = +0.374`
3. `teacher_math_z ~~ teacher_reading_z = +0.443`

Male group:

1. `teacher_math_z ~ math_trait = +0.351`
2. `teacher_reading_z ~ reading_trait = +0.412`
3. `teacher_math_z ~~ teacher_reading_z = +0.511`

[SOURCE: `sources/iq-sex-diff/data/psid/psid_cds_mtmm_2002_group_estimates.tsv`]

The method signal is present in both groups. The exact loadings differ somewhat, but not in a way that reopens the “teacher method is only a female artifact” story. [INFERENCE]

## Causal-check summary

> **Observation:** in the cleanest public child trait/method surface now local, a two-trait-plus-method prototype fits materially better than one-factor or trait-only alternatives, and the teacher-method covariance is substantial in both sexes. [SOURCE: `sources/iq-sex-diff/data/psid/psid_cds_mtmm_2002_model_compare.tsv`; `sources/iq-sex-diff/data/psid/psid_cds_mtmm_2002_group_estimates.tsv`]
>
> **Null:** if the current surface-family story were mostly narrative overfitting, the first latent prototype should collapse toward either one broad factor or weak method structure. [INFERENCE]
>
> **Residual after null:** it does not. The smallest viable public prototype already requires method structure to fit the data tolerably. [INFERENCE]

- `P(cause) = 0.70` that at least part of the child branch is genuinely trait-plus-method rather than one scalar performance surface. [INFERENCE]
- `Top alternative = 0.20` that the result is mainly an artifact of the small four-indicator setup and would weaken in a richer cross-cohort model. [INFERENCE]
- `Falsifier:` a broader MTMM or weighted joint model collapsing the teacher-method covariance toward zero while preserving fit. [INFERENCE]

## Limits

1. This is one cohort and one wave family.
2. The indicators are treated as continuous.
3. The absolute fit is still rough.
4. This is not the full cross-cohort MTMM the alpha plan ultimately wants.

[INFERENCE]

## Bottom line

The first latent prototype is good enough to harden one narrow claim:

> the repo’s `surface-family` representation is not just narrative convenience; even the smallest viable public child prototype already shows nontrivial method structure.

[INFERENCE]
