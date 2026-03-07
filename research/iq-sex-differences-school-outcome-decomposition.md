# IQ Sex Differences - School Outcome Decomposition

**Date:** 2026-03-06  
**Purpose:** test whether the public-use outcome branch adds real causal structure or just repeats the existing school-linked wedge in another set of regressions.

## What Was Run

The repo now has a descriptive cross-cohort outcome decomposition linking:

- adolescent school/test surfaces to later attainment in public `Add Health`
- early-childhood cognitive surfaces to later college exposure in public `FFCWS`

[SOURCE: `sources/iq-sex-diff/school_outcome_decomposition.py`; `sources/iq-sex-diff/data/school_outcome_decomposition/addhealth_attainment_decomposition.tsv`; `sources/iq-sex-diff/data/school_outcome_decomposition/ffcws_attainment_decomposition.tsv`; `sources/iq-sex-diff/data/school_outcome_decomposition/school_outcome_decomposition_summary.tsv`]

The point of this pass is narrow: decide whether the female later-attainment residual is mostly absorbed by the most relevant public school/cognitive surfaces already local, and decide whether that answer looks the same across cohorts. [INFERENCE]

## DAG Discipline

For the total effect of `female -> attainment`, the background-only specs are admissible in the current DAGs:

- `Add Health`: `age_w2`, `parent_ed_max`, `any_parent_professional`, `any_parent_public_assist`, `resident_mother`, `resident_father`
- `FFCWS`: `ch5age_years`, `cm1inpov`, `mother_education_cat`, `mother_race_cat`, `family_structure`

[SOURCE: `sources/iq-sex-diff/data/school_outcome_decomposition/addhealth_sex_total_dag.json`; `sources/iq-sex-diff/data/school_outcome_decomposition/ffcws_sex_total_dag.json`]

Once `pvtstd1`, grades, or the Year 9 battery are added to those `sex -> attainment` models, the estimand changes. In the current DAGs those variables are descendants/mediators on the path from sex to attainment, so they are **not** valid ordinary controls for the total effect.

- `Add Health` invalid descendants: `pvtstd1`, `math_grade_points`, `english_grade_points`
- `FFCWS` invalid descendants: `ch5ppvt_z`, `ch5wj9_z`, `ch5wj10_z`

[SOURCE: `sources/iq-sex-diff/data/school_outcome_decomposition/addhealth_sex_descendant_dag.json`; `sources/iq-sex-diff/data/school_outcome_decomposition/ffcws_sex_descendant_dag.json`]

So the coefficient movement in this memo is **descriptive channel decomposition**, not a causal direct-effect estimate. [INFERENCE]

## Add Health Result

On the locked common sample (`n = 2,524`), the female coefficient on wave IV attainment (`h4ed2`) behaves like this:

- background only: `+0.601`
- `+ pvtstd1`: `+0.654`
- `+ pvtstd1 + math_grade_points`: `+0.559`
- `+ pvtstd1 + english_grade_points`: `+0.443`
- `+ pvtstd1 + both grades`: `+0.422`

[SOURCE: `sources/iq-sex-diff/data/school_outcome_decomposition/addhealth_attainment_decomposition.tsv`]

The attenuation on the common sample is about `29.8%` once both grades are added. English carries more of that compression than math:

- `math_grade_points` coefficient: `+0.437`
- `english_grade_points` coefficient: `+0.575`
- joint model: `math = +0.290`, `english = +0.461`

[SOURCE: `sources/iq-sex-diff/data/school_outcome_decomposition/addhealth_attainment_decomposition.tsv`]

This means the public `Add Health` female attainment edge is **not** mostly explained by the wave I verbal anchor. It is more sensitive to later school-performance / evaluation surfaces, especially English-heavy ones, and even then only partly. [INFERENCE]

That read is consistent with the earlier DAG-valid school-surface models and their robustness:

- `math_grade_points -> h4ed2`: `RV = 0.205`
- `english_grade_points -> h4ed2`: `RV = 0.249`

[SOURCE: `research/iq-sex-differences-addhealth-school-surface-first-pass.md`; `sources/iq-sex-diff/data/addhealth/addhealth_school_surface_math_h4ed2_sensemakr.json`; `sources/iq-sex-diff/data/addhealth/addhealth_school_surface_english_h4ed2_sensemakr.json`]

## FFCWS Result

On the locked common sample (`n = 1,636`), the female coefficient on `college_years` behaves like this:

- background only: `+0.637`
- `+ ppvt`: `+0.635`
- `+ passage`: `+0.593`
- `+ applied`: `+0.628`
- `+ joint battery`: `+0.625`

[SOURCE: `sources/iq-sex-diff/data/school_outcome_decomposition/ffcws_attainment_decomposition.tsv`]

The full joint Year 9 battery explains almost none of the female later-college residual on the common sample:

- attenuation: about `1.9%`

[SOURCE: `sources/iq-sex-diff/data/school_outcome_decomposition/school_outcome_decomposition_summary.tsv`]

This does **not** mean the Year 9 battery is irrelevant to attainment. It still predicts later college years in the earlier DAG-valid outcome models:

- `Applied Problems`: `RV = 0.178`
- `PPVT`: `RV = 0.147`

[SOURCE: `research/iq-sex-differences-ffcws-achievement-first-pass.md`; `sources/iq-sex-diff/data/ffcws/ffcws_transition_applied_sensemakr.json`; `sources/iq-sex-diff/data/ffcws/ffcws_transition_ppvt_sensemakr.json`]

What it means is narrower: in this cohort, the female later-college residual is much broader than the observed early-childhood cognitive block. [INFERENCE]

## Cross-Cohort Read

The cohorts now split in a way that is actually informative:

- `Add Health`: adolescent school-performance / evaluation surfaces absorb a meaningful but still partial share of the female attainment edge
- `FFCWS`: early-childhood cognitive surfaces barely absorb the female later-college edge

[SOURCE: `sources/iq-sex-diff/data/school_outcome_decomposition/school_outcome_decomposition_summary.tsv`]

That is the best current public-use outcome insight in the repo:

1. later female attainment differences are not well summarized by one early child cognitive battery
2. adolescent school/evaluation surfaces are more proximate to the later attainment edge than the early child battery is
3. even the stronger adolescent school/evaluation block does not come close to erasing the whole female attainment residual

[INFERENCE]

This pushes the project toward a life-course split:

- early child cognitive geometry
- adolescent school/evaluation accumulation
- later transition outcomes

Those are related, but they are not one estimand. [INFERENCE]

## Causal Check

> **Observation:** in public `Add Health`, the female later-attainment coefficient shrinks materially when adolescent grades are added on the common sample, especially with English grades; in public `FFCWS`, the female later-college coefficient barely shrinks when the Year 9 cognitive battery is added on the common sample. [SOURCE: `sources/iq-sex-diff/data/school_outcome_decomposition/addhealth_attainment_decomposition.tsv`; `sources/iq-sex-diff/data/school_outcome_decomposition/ffcws_attainment_decomposition.tsv`; `sources/iq-sex-diff/data/school_outcome_decomposition/school_outcome_decomposition_summary.tsv`]
>
> **Null:** if the observed female later-attainment edge were mainly just broad early cognitive advantage or mainly just one generic school-performance factor, the same kind of attenuation should appear across these public cohorts once the most relevant local surfaces are added. [INFERENCE]
>
> **Residual after null:** it does not. The later-attainment edge is much more sensitive to adolescent school/evaluation surfaces than to the early-childhood cognitive battery. [INFERENCE]

- `P(cause)`: `0.68` that later female attainment differences are more proximate to adolescent school/evaluation accumulation than to the currently observed early-childhood cognitive surfaces. [INFERENCE]
- `Top alternative`: `0.22` that this is mostly cohort/surface mismatch: `Add Health` uses adolescent grades plus wave IV attainment, while `FFCWS` uses a sparse Year 9 battery plus Year 22 college years, so the apparent life-course split is partly design-driven. [INFERENCE]
- `Falsifier`: a cohort with both early-childhood battery data and later transcript/grade surfaces showing that the early battery attenuates the female attainment edge as much as or more than the adolescent school surfaces do on common samples. [INFERENCE]
- `Decision impact`: treat the public outcome branch as support for a life-course channel split, not as proof of a causal direct effect and not as evidence that grades or test scores “explain” sex differences in attainment in a mediation-identified sense. [INFERENCE]

## What This Changes

What hardens:

- the school/evaluation family matters for life outcomes, not just for transcript-vs-test rhetoric
- the later female attainment edge is not well summarized by the currently staged early-childhood battery surfaces
- the project should keep early-childhood cognition and adolescent school/evaluation accumulation separate in the causal tree

What stays open:

- whether the school/evaluation channel is classroom performance, institutional evaluation, behavior/compliance, aspirations, or a mixture
- whether a richer transcript/test/process dataset would compress the female later-attainment residual more than the public surfaces do
- whether restricted transcript/process access is now the only real way to push the outcome branch materially further

## Next Step

The next honest move is **not** another descendant-heavy public-use regression on `female -> attainment`.

The next high-value moves are:

1. restricted transcript/process access (`HSTS`, `NAEP`, `AHAA`-type routes if available)
2. a real mediator design with explicitly separated pre-treatment, school-performance, evaluation, and transition stages
3. if staying public-use, cross-cohort outcome synthesis rather than more isolated cohort slicing

[INFERENCE]
