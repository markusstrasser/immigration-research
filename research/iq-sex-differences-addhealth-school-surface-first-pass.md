# IQ Sex Differences - Add Health School-Surface First Pass

**Date:** 2026-03-06  
**Purpose:** decide whether public-use `Add Health` strengthens the replicated school-linked wedge or adds a genuinely new math-specific contradiction.

## What Was Built

The repo now has a cleaned public-use `Add Health` panel linking:

- wave I parent-background variables
- wave II subject-grade surfaces
- wave I `PVTSTD1` recovered from the public wave III `PVT` release
- wave IV educational attainment

[SOURCE: `sources/iq-sex-diff/addhealth_school_surface_pass.py`; `sources/iq-sex-diff/data/addhealth/addhealth_school_surface_extract.parquet`]

The current working sample is the intersection of the public wave I in-home file, the wave II in-home file and weights, the wave III `PVT` public file, and the wave IV in-home file and weights. [SOURCE: `sources/iq-sex-diff/addhealth_school_surface_pass.py`]

## Data-Hygiene Corrections

Three corrections matter enough to treat this pass as the canonical `Add Health` branch rather than a minor extension of the exploratory script:

1. **Parent background moved to wave I.** The first exploratory pass did not have a credible pre-treatment SES block. The new pass uses wave I resident mother/father education, occupation, and public-assistance variables. [SOURCE: `sources/iq-sex-diff/data/addhealth/addhealth_public_codebook_extracts.txt`; `sources/iq-sex-diff/addhealth_school_surface_pass.py`]
2. **`PVTSTD1` is a wave I score, not a wave III descendant.** The public `PVT` documentation says `PVTSTD1` is the improved standardized score for wave I, reconstructed with corrected ages and sampling weights. That makes it usable as a pre-grade verbal anchor. [SOURCE: `sources/iq-sex-diff/data/addhealth/addhealth_public_codebook_extracts.txt`]
3. **`CLUSTER2` is design structure, not a primary control.** The public design note says `CLUSTER2` is the cluster variable for waves I-IV and that no strata variable is available. In the canonical pass it is used for clustered standard errors, not as a fixed-effect covariate. [SOURCE: `sources/iq-sex-diff/data/addhealth/addhealth_public_codebook_extracts.txt`; `sources/iq-sex-diff/addhealth_school_surface_pass.py`]

These corrections reduce the strongest local objections to the original exploratory pass. [INFERENCE]

## Main Descriptive Result

Public-use `Add Health` is not a transcript/test adjudication dataset. It is a broad school-performance / later-attainment dataset.

On wave II grades, girls are ahead in every core subject:

- English grade points: `d = +0.362`
- Math grade points: `d = +0.207`
- History grade points: `d = +0.216`
- Science grade points: `d = +0.223`

[SOURCE: `sources/iq-sex-diff/data/addhealth/addhealth_school_surface_grade_gaps.tsv`]

On relative profile surfaces:

- `math minus english`: `d = -0.114`
- `math minus history`: `d = +0.020`
- `math minus science`: `d = +0.010`

[SOURCE: `sources/iq-sex-diff/data/addhealth/addhealth_school_surface_relative_gaps.tsv`]

So the public `Add Health` grade pattern is not “girls especially dominate math.” It is:

- broad female grade advantage
- with English more female-tilted than math

[INFERENCE]

Wave IV attainment is also female-leaning:

- `h4ed2`: `d = +0.270`
- `some_college_plus`: `d = +0.257`
- `bachelor_plus`: `d = +0.151`

[SOURCE: `sources/iq-sex-diff/data/addhealth/addhealth_school_surface_attainment_gaps.tsv`]

## Parent-Background Surface

The new wave I SES block does **not** show a simple female-favoring family-background story that could trivially explain the later grade geometry:

- `parent_ed_max`: `d = -0.041`
- `any_parent_professional`: `d = -0.067`
- `any_parent_public_assist`: `d = -0.016`
- `resident_mother`: `d = +0.079`
- `resident_father`: `d = -0.058`

[SOURCE: `sources/iq-sex-diff/data/addhealth/addhealth_school_surface_parent_background.tsv`]

The sex balance on observed family background is mixed and fairly small relative to the grade gaps. [INFERENCE]

## SES-Adjusted Grade-Surface Result

After adjusting for:

- sex
- age at wave II
- wave I `PVTSTD1`
- wave I `parent_ed_max`
- wave I `any_parent_professional`
- wave I `any_parent_public_assist`
- wave I resident mother / father presence

the female residual on grades remains:

- `math_grade_points`: `beta_female = +0.226`, `95% CI [0.146, 0.307]`
- `english_grade_points`: `beta_female = +0.353`, `95% CI [0.289, 0.417]`
- `math_minus_english`: `beta_female = -0.116`, `95% CI [-0.206, -0.026]`

[SOURCE: `sources/iq-sex-diff/data/addhealth/addhealth_school_surface_grade_models.tsv`]

This is the cleanest local summary of the public `Add Health` school surface:

- the female grade advantage survives the obvious baseline verbal and family-background block
- math is less female-tilted than English, but still female-tilted in absolute grade points

[INFERENCE]

## DAG-Valid Grade-to-Attainment Result

For the causal question “do wave II grades predict later educational attainment under the observed pre-treatment block?”, the validated adjustment set is:

- `female`
- `age_w2`
- `pvtstd1`
- `parent_ed_max`
- `any_parent_professional`
- `any_parent_public_assist`
- `resident_mother`
- `resident_father`

with `CLUSTER2` used for clustered standard errors only. [SOURCE: `sources/iq-sex-diff/data/addhealth/addhealth_dag_mathgrade_to_h4ed2_v2.json`; `sources/iq-sex-diff/data/addhealth/addhealth_dag_englishgrade_to_h4ed2_v2.json`]

Under that specification:

- `h4ed2 ~ math_grade_points + controls`: `beta = +0.430`, `SE = 0.039`
- `h4ed2 ~ english_grade_points + controls`: `beta = +0.574`, `SE = 0.044`

[SOURCE: `sources/iq-sex-diff/data/addhealth/addhealth_school_surface_models.tsv`]

If both grades are entered jointly, both remain positive, but English stays stronger:

- `math_grade_points`: `beta = +0.290`, `SE = 0.041`
- `english_grade_points`: `beta = +0.461`, `SE = 0.048`

[SOURCE: `sources/iq-sex-diff/data/addhealth/addhealth_school_surface_joint_models.tsv`]

That is not a math-specific wedge. It is a broader school-performance / evaluation surface that continues to matter for later attainment. [INFERENCE]

## Robustness

The SES-adjusted grade-to-attainment models are not fragile under the observed benchmark set:

- math-grade model: `RV = 0.205`
- English-grade model: `RV = 0.249`

Strongest observed benchmark partial `R²` values are around `0.052` to `0.060` (`pvtstd1` and `parent_ed_max`), so the current treatment estimates require a materially stronger omitted confounder than any single observed benchmark to explain away. [SOURCE: `sources/iq-sex-diff/data/addhealth/addhealth_school_surface_math_h4ed2_sensemakr.json`; `sources/iq-sex-diff/data/addhealth/addhealth_school_surface_english_h4ed2_sensemakr.json`]

This is still an observed-confounder robustness claim, not proof against all hidden selection. [INFERENCE]

## Causal Check

> **Observation:** in public-use `Add Health`, girls have higher grades across all four wave II core subjects, the female grade advantage survives a wave I verbal-plus-family-background block, and both math and English grades strongly predict wave IV attainment under a DAG-valid observed-confounder set. [SOURCE: `sources/iq-sex-diff/data/addhealth/addhealth_school_surface_grade_gaps.tsv`; `sources/iq-sex-diff/data/addhealth/addhealth_school_surface_grade_models.tsv`; `sources/iq-sex-diff/data/addhealth/addhealth_school_surface_models.tsv`]
>
> **Null:** if the existing school-linked wedge were mostly an `HSLS` transcript artifact or just obvious family-composition imbalance, the public `Add Health` grade surface should compress sharply once wave I ability and parent background are introduced. [INFERENCE]
>
> **Residual after null:** it does not. The grade advantage remains, and English remains more female-tilted than math. [SOURCE: `sources/iq-sex-diff/data/addhealth/addhealth_school_surface_grade_models.tsv`]

- `P(cause)`: `0.74` that public-use `Add Health` strengthens the broad school-performance / evaluation family rather than adding a new contradiction to it. [INFERENCE]
- `Top alternative`: `0.18` that the public grade surfaces are mostly picking up broad conscientiousness / compliance / self-report advantages rather than institutional evaluation asymmetry or schooling performance per se. [INFERENCE]
- `Falsifier`: a stronger same-cohort dataset with both grades and standardized math where the female grade residual collapses once baseline ability, family background, and school context are aligned on common samples. [INFERENCE]
- `Decision impact`: treat `Add Health` as support for the general school-surface node, not as evidence about battery-independent `g` and not as a math-specific transcript/test adjudication. [INFERENCE]

## What This Does And Does Not Settle

What it settles enough to use:

- the school-linked wedge is not confined to `HSLS`, `ELS`, `NELS`, or `PSID TAS`
- public `Add Health` extends the female-leaning evaluation / school-performance family into another nationally representative adolescent cohort
- the female school-surface advantage is broader than math alone, with English even more female-tilted than math

What it does **not** settle:

- whether the grade surface is driven more by evaluation, compliance, classroom performance, or a combination
- whether a same-wave standardized math surface in `Add Health` would look more like `HSLS` tested math or more like the grade surfaces
- anything battery-independent about `g`

## Next Step

The best next `Add Health` move is not more grade slicing. It is one of:

1. find a real family-linked design in the public `Add Health` files if it exists
2. move to restricted `Add Health` / `AHAA` transcript access if transcript/test linkage is worth the friction
3. use this result in the cross-dataset school-wedge synthesis as a broad school-performance replication

[INFERENCE]
