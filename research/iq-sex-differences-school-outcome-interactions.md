# IQ Sex Differences - School Outcome Interactions

**Date:** 2026-03-06  
**Purpose:** test whether the main school/test predictors of later attainment have materially different downstream slopes by sex in the currently staged public-use cohorts.

## Why This Matters

The lazy objection to the school-linked wedge is:

> girls may look better on grades or related school surfaces, but those surfaces could be inflated and therefore less consequential for later outcomes

This pass does not fully settle that objection, but it does test the cleanest public-use version of it:

- do grade/test predictors have weaker later-attainment slopes for girls than for boys?

[INFERENCE]

## Models Run

### Add Health

Outcome:

- `h4ed2`

Predictors tested one at a time:

- `math_grade_points`
- `english_grade_points`

Controls:

- `female`
- `age_w2`
- `parent_ed_max`
- `any_parent_professional`
- `any_parent_public_assist`
- `resident_mother`
- `resident_father`
- `pvtstd1`

The valid observed-confounder DAG for `grade -> h4ed2` was already established in the earlier school-surface memo; this pass adds `female:grade` effect-modification terms rather than changing the base DAG. [SOURCE: `research/iq-sex-differences-addhealth-school-surface-first-pass.md`; `sources/iq-sex-diff/data/addhealth/addhealth_dag_mathgrade_to_h4ed2_v2.json`; `sources/iq-sex-diff/data/addhealth/addhealth_dag_englishgrade_to_h4ed2_v2.json`]

### FFCWS

Outcome:

- `college_years`

Predictors tested one at a time:

- `ch5wj10_z`
- `ch5wj9_z`
- `ch5ppvt_z`

Controls:

- `female`
- `ch5age_years`
- `cm1inpov`
- `mother_education_cat`
- `mother_race_cat`
- `family_structure`

The valid observed-confounder DAGs for these Year 9 battery predictors were already established in the earlier `FFCWS` memo; again, this pass adds `female:score` effect-modification terms rather than redefining the base DAG. [SOURCE: `research/iq-sex-differences-ffcws-achievement-first-pass.md`; `sources/iq-sex-diff/data/ffcws/ffcws_dag_wj10_to_college_years.json`; `sources/iq-sex-diff/data/ffcws/ffcws_dag_ppvt_to_college_years.json`]

All outputs were written by:

- `sources/iq-sex-diff/school_outcome_interactions.py`

[SOURCE: `sources/iq-sex-diff/data/school_outcome_interactions/addhealth_outcome_interactions.tsv`; `sources/iq-sex-diff/data/school_outcome_interactions/ffcws_outcome_interactions.tsv`; `sources/iq-sex-diff/data/school_outcome_interactions/school_outcome_interactions_summary.tsv`]

## Main Result

## Add Health

### Math grades

- male slope on `h4ed2`: `+0.421`
- female slope on `h4ed2`: `+0.439`
- interaction: `+0.018`, `95% CI [-0.165, +0.201]`

[SOURCE: `sources/iq-sex-diff/data/school_outcome_interactions/addhealth_outcome_interactions.tsv`]

### English grades

- male slope on `h4ed2`: `+0.613`
- female slope on `h4ed2`: `+0.539`
- interaction: `-0.074`, `95% CI [-0.245, +0.097]`

[SOURCE: `sources/iq-sex-diff/data/school_outcome_interactions/addhealth_outcome_interactions.tsv`]

The operative read is simple:

- both grade surfaces predict later attainment strongly
- neither interaction is cleanly different from zero
- there is no strong public-use evidence here that girls' grades are less consequential than boys' grades

[INFERENCE]

## FFCWS

### Applied Problems

- male slope on `college_years`: `+0.340`
- female slope on `college_years`: `+0.313`
- interaction: `-0.027`, `95% CI [-0.366, +0.312]`

### Passage Comprehension

- male slope: `+0.237`
- female slope: `+0.081`
- interaction: `-0.156`, `95% CI [-0.474, +0.163]`

### PPVT

- male slope: `+0.401`
- female slope: `+0.156`
- interaction: `-0.245`, `95% CI [-0.497, +0.006]`

[SOURCE: `sources/iq-sex-diff/data/school_outcome_interactions/ffcws_outcome_interactions.tsv`]

This is weaker and less stable than `Add Health`:

- `Applied Problems` looks similar across sex
- `Passage` trends male-stronger but is noisy
- `PPVT` is the strongest hint of a weaker female payoff, but it is still borderline rather than decisive

[INFERENCE]

## Best Current Read

The public-use interaction evidence does **not** support a strong generic “female school surfaces are inflated and therefore pay off less” story.

What it supports is narrower:

1. in `Add Health`, grades are highly consequential for later attainment for both sexes, with no clean evidence of weaker female returns
2. in `FFCWS`, some early child cognitive slopes may be somewhat stronger for boys, but the evidence is noisy and not broad across the battery
3. if there is a “female surfaces are less predictive” story, it is not a simple universal fact across these public cohorts

[INFERENCE]

## Causal Check

> **Observation:** in the current public-use interaction pass, `Add Health` grade predictors have similar later-attainment slopes for boys and girls, while `FFCWS` child-score interactions are mostly negative but imprecise, with `PPVT` the only near-nonzero case. [SOURCE: `sources/iq-sex-diff/data/school_outcome_interactions/addhealth_outcome_interactions.tsv`; `sources/iq-sex-diff/data/school_outcome_interactions/ffcws_outcome_interactions.tsv`]
>
> **Null:** if the school-linked wedge were mostly a grade-inflation or low-value female-label story, the female interaction terms should be consistently and materially negative across the school/test predictors most tied to later outcomes. [INFERENCE]
>
> **Residual after null:** that footprint does not appear in `Add Health`, and it appears only weakly and selectively in `FFCWS`. [INFERENCE]

- `P(cause)`: `0.64` that the simple “girls’ school surfaces are broadly less consequential” story is too strong for the current public-use evidence. [INFERENCE]
- `Top alternative`: `0.24` that the relevant return differences are real but hidden by sample restriction, outcome mismatch, and noisy public-use surfaces; the strongest current hint is the `FFCWS PPVT` interaction. [INFERENCE]
- `Falsifier`: a transcript/test-linked cohort where female interaction terms are consistently and materially negative across grades, tested math, and verbal anchors on common samples. [INFERENCE]
- `Decision impact`: do not dismiss the evaluation/school-performance family as mere inflation just because it is female-leaning. The current public outcome branch says those surfaces still carry substantial later-attainment signal. [INFERENCE]

## What This Changes

What hardens:

- the school-linked wedge is not obviously low-value in later outcomes
- public `Add Health` weakens the simple grade-inflation story

What stays open:

- whether richer transcript/test/process datasets would show stronger sex-specific payoff differences
- whether `FFCWS PPVT` is a real interaction or just a noisy cohort-specific hint
- whether predictive-validity differences are larger for selective STEM outcomes than for general educational attainment

## Next Step

If the project wants to push the outcome branch further, the best next move is not more public-use interaction hunting.

The next honest steps are:

1. selective-STEM or transcript-linked outcomes in a richer cohort
2. restricted transcript/process access
3. an explicit mediator design instead of informal attenuation or interaction rhetoric

[INFERENCE]
