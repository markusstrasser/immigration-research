# IQ Sex Differences - HSLS Wedge Refinement

**Date:** 2026-03-06  
**Status:** pre-follow-up behavior/identity and teacher-climate stress test on the existing `HSLS` transcript wedge

## Scope

This pass does **not** estimate a clean causal effect.

It asks a narrower question:

> Does the `HSLS` transcript wedge materially compress once the obvious pre-follow-up homework, self-efficacy, belonging, teacher-encouragement, and math-teacher climate surfaces are added?

That makes this a same-sample mechanism stress test, not a valid ordinary-control model for the total effect of `sex`. [INFERENCE]

## Data And Surfaces

Script:

- [SOURCE: `sources/iq-sex-diff/hsls_wedge_refinement.py`]

Outputs:

- [SOURCE: `sources/iq-sex-diff/data/hsls/hsls_wedge_refinement_extract.parquet`]
- [SOURCE: `sources/iq-sex-diff/data/hsls/hsls_wedge_refinement_gaps.tsv`]
- [SOURCE: `sources/iq-sex-diff/data/hsls/hsls_wedge_refinement_models.tsv`]

Added public-use surfaces:

- `S1NOHWDN` how often the 9th grader goes to class without homework done [SOURCE: `sources/iq-sex-diff/data/hsls/HSLS_2017_PETS_SR_v1_0_SPSS_Datasets.zip`]
- `S1HRMHOMEWK` hours spent on math homework/studying on a typical schoolday [SOURCE: `sources/iq-sex-diff/data/hsls/HSLS_2017_PETS_SR_v1_0_SPSS_Datasets.zip`]
- `X1MTHEFF` base-year math self-efficacy [SOURCE: `sources/iq-sex-diff/data/hsls/HSLS_2017_PETS_SR_v1_0_SPSS_Datasets.zip`]
- `X1SCHOOLBEL` base-year school belonging [SOURCE: `sources/iq-sex-diff/data/hsls/HSLS_2017_PETS_SR_v1_0_SPSS_Datasets.zip`]
- `S1MTEACHER` taking fall 2009 math because a teacher encouraged it [SOURCE: `sources/iq-sex-diff/data/hsls/HSLS_2017_PETS_SR_v1_0_SPSS_Datasets.zip`]
- `S1MTCHFAIR`, `S1MTCHTREAT`, `S1MTCHMFDIFF`, `S1MTCHCONF`, `S1MTCHINTRST`, `S1MTCHEASY` as math-teacher climate / fairness items [SOURCE: `sources/iq-sex-diff/data/hsls/HSLS_2017_PETS_SR_v1_0_SPSS_Datasets.zip`]

Derived indices:

- `base_behavior_identity_index_z`
- `teacher_climate_index_z`

[SOURCE: `sources/iq-sex-diff/hsls_wedge_refinement.py`]

## Main Findings

### 1. The added mechanism surfaces are not strongly male-leaning

In the transcript-covered analytic sample:

- `base_behavior_identity_index_z`: `beta_female = +0.0499`
- `teacher_climate_index_z`: `beta_female = +0.0230`, CI overlaps zero

[SOURCE: `sources/iq-sex-diff/data/hsls/hsls_wedge_refinement_gaps.tsv`]

So the obvious pre-follow-up behavior/identity block is mildly female-leaning, while teacher-climate is near neutral. [INFERENCE]

### 2. The later standardized-math surface stays male-leaning

On the same `n = 9,114` common sample:

- same-sample base `X2TXMTSCOR_z ~ female`: `beta = -0.0786`
- adjusted `X2TXMTSCOR_z ~ female + X1TXMTSCOR_z + base_behavior_identity_index_z + teacher_climate_index_z`: `beta = -0.0453`

[SOURCE: `sources/iq-sex-diff/data/hsls/hsls_wedge_refinement_models.tsv`]

So the later standardized math surface moves somewhat toward zero, but it does not reverse and it does not disappear. [INFERENCE]

### 3. The school-linked wedge survives, and if anything becomes clearer on the common sample

Math GPA:

- same-sample base: `beta_female = +0.2406`
- adjusted: `beta_female = +0.2681`

Highest-math GPA:

- same-sample base: `beta_female = +0.1734`
- adjusted: `beta_female = +0.1958`

`precalc_plus`:

- same-sample base: `beta_female = +0.0448`
- adjusted: `beta_female = +0.0526`

[SOURCE: `sources/iq-sex-diff/data/hsls/hsls_wedge_refinement_models.tsv`]

That means the obvious pre-follow-up homework / belonging / self-efficacy / teacher-climate block does **not** explain away the school-linked wedge. The grade-track side survives this stress test cleanly. [INFERENCE]

## Causal Check

> **Observation:** in `HSLS`, later standardized math remains male-leaning on the same common sample while transcript GPA and `precalc_plus` stay female-leaning after the obvious pre-follow-up behavior/identity and teacher-climate surfaces are added. [SOURCE: `sources/iq-sex-diff/data/hsls/hsls_wedge_refinement_models.tsv`]
>
> **Null:** if the `HSLS` wedge is mostly just a reflection of girls doing more homework, feeling more belonging, reporting higher self-efficacy, or having nicer/fairer math-teacher climates, then those blocks should materially compress both the transcript-GPA and track wedges. [INFERENCE]
>
> **Residual after null:** the later tested-math surface shrinks a bit, but the school-linked wedge survives and slightly strengthens on the common sample. [SOURCE: `sources/iq-sex-diff/data/hsls/hsls_wedge_refinement_models.tsv`]

- `P(cause)`: `0.68` that the `HSLS` school-linked wedge is not mainly explained by these obvious pre-follow-up behavior/identity and teacher-climate surfaces. [INFERENCE]
- `Top alternative`: `0.20` that the remaining wedge still reflects other unmeasured school-process or grading channels rather than a distinct evaluation/placement node. [INFERENCE]
- `Falsifier`: a richer `HSLS` refinement with better discipline/absence/teacher-report or restricted transcript data that materially compresses the transcript-GPA and track wedges on the same sample. [INFERENCE]
- `Decision impact`: the project can now treat the `HSLS` wedge as robust to a first plausible mechanism block, but not as causally identified. [INFERENCE]

## What This Changes

1. The `HSLS` wedge is no longer vulnerable to the simple objection that it is just homework, belonging, self-efficacy, or obvious math-teacher climate. [INFERENCE]
2. Combined with the new `ELS` pass, the school-linked node is now supported by:
   - transcript GPA and track in `HSLS`
   - track and evaluation surfaces in `ELS`
   - a localized school-knowledge / transcript wedge in `NLSY97`

[SOURCE: `research/iq-sex-differences-hsls-wedge-first-pass.md`; `research/iq-sex-differences-els-wedge-first-pass.md`; `research/iq-sex-differences-nlsy97-transcript-deep-pass.md`]

3. The next useful move is not another generic local regression. It is either:
   - a stronger external school-linked replication such as `NELS` or restricted transcript data, or
   - a synthesis pass that explicitly separates tested-math, track, GPA, and evaluation surfaces across `HSLS`, `ELS`, and `NLSY97`. [INFERENCE]
