# IQ Sex Differences - FFCWS Achievement First Pass

**Date:** 2026-03-06  
**Purpose:** test whether the project's current math / verbal and school-transition story survives in a very different cohort: the public `Fragile Families and Child Wellbeing Study` (`FFCWS`).

## What Was Built

The repo now has a first cleaned `FFCWS` panel linking:

- baseline sex and family-background fields
- Year 9 child cognitive surfaces
- Year 22 college-exposure and GPA surfaces

[SOURCE: `sources/iq-sex-diff/ffcws_achievement_first_pass.py`; `sources/iq-sex-diff/data/ffcws/ffcws_achievement_extract.parquet`]

The Year 9 child battery used here is:

- `CH5PPVTSS` (`PPVT`)
- `CH5WJ9SS` (`Woodcock-Johnson Passage Comprehension`)
- `CH5WJ10SS` (`Woodcock-Johnson Applied Problems`)
- `CH5DSSS` (`Digit Span`)

[SOURCE: `sources/iq-sex-diff/data/ffcws/ICPSR_31622/DS0001/31622-0001-User_guide-Year9_MULTI.pdf`; `sources/iq-sex-diff/data/ffcws/ffcws_achievement_extract.parquet`]

The Year 22 transition surfaces used here are:

- `K7B2` (`years of college completed`)
- `K7B45` (`ever enrolled in college`)
- `K7B55` (`current GPA`)
- `K7B56` (`highest GPA`)
- normalized first-college GPA from `K7B76_1 / K7B77_1`

[SOURCE: `sources/iq-sex-diff/data/ffcws/ICPSR_31622/DS0001/31622-0001-User_guide-Year22_MULTI.pdf`; `sources/iq-sex-diff/data/ffcws/ffcws_achievement_extract.parquet`]

## Data-Hygiene Notes

Three points matter enough to carry forward:

1. Negative survey missing codes were recoded explicitly before all summaries and models. [SOURCE: `sources/iq-sex-diff/ffcws_achievement_first_pass.py`]
2. The Year 9 child assessments have more observed cases than the Year 9 primary-caregiver national weight, so the first pass treats weighted Year 9 summaries as sensitivity checks rather than the only canonical read. [SOURCE: `sources/iq-sex-diff/data/ffcws/ffcws_y9_surface_gaps.tsv`; `sources/iq-sex-diff/ffcws_achievement_first_pass.py`]
3. Year 22 GPA fields are highly selected. The cleanest transition outcome in the current public file is `college_years`, not current GPA. [SOURCE: `sources/iq-sex-diff/data/ffcws/ffcws_y22_transition_gaps.tsv`]

## Main Year 9 Geometry

The Year 9 sex-gap geometry is not a simple male-math / female-verbal cliché.

Unweighted female-minus-male `d` values:

- `PPVT`: `-0.064`
- `Passage Comprehension`: `+0.206`
- `Applied Problems`: `+0.050`
- `Digit Span`: `+0.104`

Weighted sensitivity using `P5NATWT`:

- `PPVT`: `-0.034`
- `Passage Comprehension`: `+0.201`
- `Applied Problems`: `+0.053`
- `Digit Span`: `+0.050`

[SOURCE: `sources/iq-sex-diff/data/ffcws/ffcws_y9_surface_gaps.tsv`]

So the cleanest descriptive read is:

- girls are clearly ahead on reading comprehension
- `Applied Problems` is close to parity with a slight female lean
- `PPVT` is slightly male-leaning
- `Digit Span` is slightly female-leaning

[INFERENCE]

## Relative Math-Versus-Verbal Surfaces

The relative same-child surfaces are more informative than the raw scores:

- `applied minus passage`: `d = -0.193`
- `applied minus PPVT`: `d = +0.099`
- `applied minus mean verbal`: `d = -0.039`
- `passage minus PPVT`: `d = +0.299`

Weighted sensitivity tells the same directional story:

- `applied minus passage`: `d = -0.179`
- `applied minus PPVT`: `d = +0.084`
- `applied minus mean verbal`: `d = -0.043`
- `passage minus PPVT`: `d = +0.253`

[SOURCE: `sources/iq-sex-diff/data/ffcws/ffcws_y9_relative_gaps.tsv`]

This means the Year 9 geometry is anchor-sensitive:

- relative to reading comprehension, applied math tilts male
- relative to vocabulary, applied math tilts female
- relative to the average of the two verbal anchors, the net difference is close to zero

[INFERENCE]

That does **not** look like a simple broad male math edge. It looks like another case where the observed sex gap depends on which surface family is being compared. [INFERENCE]

## Adjusted Year 9 Surface Models

The first adjusted descriptive pass used:

- `female`
- Year 9 child age
- baseline mother education
- baseline poverty ratio
- baseline mother race
- baseline family structure

[SOURCE: `sources/iq-sex-diff/ffcws_achievement_first_pass.py`; `sources/iq-sex-diff/data/ffcws/ffcws_y9_surface_models.tsv`]

Female coefficients:

- `PPVT`: `-0.766`, `95% CI [-1.647, 0.115]`
- `Passage Comprehension`: `+2.993`, `95% CI [2.092, 3.894]`
- `Applied Problems`: `+0.874`, `95% CI [-0.148, 1.896]`
- `Digit Span`: `+0.303`, `95% CI [0.117, 0.489]`
- `applied minus passage`: `-0.159`, `95% CI [-0.215, -0.103]`
- `applied minus PPVT`: `+0.091`, `95% CI [0.029, 0.153]`
- `applied minus mean verbal`: `-0.031`, `95% CI [-0.083, 0.021]`

[SOURCE: `sources/iq-sex-diff/data/ffcws/ffcws_y9_surface_models.tsv`]

The adjusted read is basically the same as the raw one:

- the biggest female edge is in reading comprehension
- `Applied Problems` is not a strong female or male edge on its own
- relative interpretation still depends on whether the anchor is passage comprehension or `PPVT`

[INFERENCE]

## Year 22 Transition Surfaces

Female-minus-male transition gaps:

- `college_years`: `d = +0.331` unweighted, `+0.256` weighted
- `ever_college`: `d = +0.332` unweighted, `+0.340` weighted
- `current GPA`: near null
- `highest GPA`: small positive
- normalized first-college GPA: female-leaning

[SOURCE: `sources/iq-sex-diff/data/ffcws/ffcws_y22_transition_gaps.tsv`]

The strongest clean transition surface here is `college_years`, not GPA. [INFERENCE]

## DAG-Valid Transition Models

For the observed-confounder transition question, the validated adjustment set for:

- `AppliedProblems_y9 -> college_years`
- `PPVT_y9 -> college_years`

is:

- `female`
- `ch5age_years`
- `mother_education`
- `baseline_poverty`
- `mother_race`
- `family_structure`

[SOURCE: `sources/iq-sex-diff/data/ffcws/ffcws_dag_wj10_to_college_years.json`; `sources/iq-sex-diff/data/ffcws/ffcws_dag_ppvt_to_college_years.json`]

Single-score OLS results:

- `college_years ~ applied_problems_z + controls`: `beta = +0.289`, `SE = 0.032`
- `college_years ~ PPVT_z + controls`: `beta = +0.243`, `SE = 0.032`
- `college_years ~ passage_z + controls`: `beta = +0.232`, `SE = 0.030`
- `college_years ~ digit_span_z + controls`: `beta = +0.182`, `SE = 0.028`

[SOURCE: `sources/iq-sex-diff/data/ffcws/ffcws_transition_models.tsv`]

Joint model:

- `female`: `+0.563`, `SE = 0.057`
- `applied_problems_z`: `+0.204`, `SE = 0.043`
- `PPVT_z`: `+0.113`, `SE = 0.040`
- `passage_z`: `+0.031`, `SE = 0.044`
- `digit_span_z`: `+0.065`, `SE = 0.032`

[SOURCE: `sources/iq-sex-diff/data/ffcws/ffcws_transition_joint_models.tsv`]

Weighted sensitivity using `K7NATWT`:

- `female`: `+0.620`, `SE = 0.150`
- `applied_problems_z`: `+0.182`, `SE = 0.105`
- `PPVT_z`: `+0.194`, `SE = 0.095`
- `passage_z`: `-0.012`, `SE = 0.113`
- `digit_span_z`: `+0.141`, `SE = 0.069`

[SOURCE: `sources/iq-sex-diff/data/ffcws/ffcws_transition_weighted_joint_models.tsv`]

So the transition result is:

- Year 9 applied problems is at least as relevant as the verbal surfaces for later college years
- the female college-years residual survives the observed Year 9 battery and baseline SES block

[INFERENCE]

## Robustness

Observed-confounder robustness for the single-score `college_years` models:

- `Applied Problems`: `RV = 0.178`
- `PPVT`: `RV = 0.147`

Both are materially larger than the strongest observed benchmark in the current benchmark set. [SOURCE: `sources/iq-sex-diff/data/ffcws/ffcws_transition_applied_sensemakr.json`; `sources/iq-sex-diff/data/ffcws/ffcws_transition_ppvt_sensemakr.json`]

This does **not** prove the transition coefficients are causal. It says the current observed-confounder result is not trivial to erase with an omitted variable that is only as strong as the benchmarked observed covariates. [INFERENCE]

## Causal Check

> **Observation:** in `FFCWS`, the Year 9 child battery does not show a simple broad male math edge: `Applied Problems` is close to parity while reading comprehension is clearly female-leaning and `PPVT` is slightly male-leaning. At the same time, Year 22 college exposure is female-leaning, and the female college-years residual survives the Year 9 battery plus baseline SES block. [SOURCE: `sources/iq-sex-diff/data/ffcws/ffcws_y9_surface_gaps.tsv`; `sources/iq-sex-diff/data/ffcws/ffcws_y9_relative_gaps.tsv`; `sources/iq-sex-diff/data/ffcws/ffcws_transition_joint_models.tsv`]
>
> **Null:** if the current project story were just a middle-class transcript artifact or a single broad male-math versus female-verbal pattern, this cohort should either collapse the transition wedge or show a cleaner male math edge than it actually does. [INFERENCE]
>
> **Residual after null:** it does not. The Year 9 geometry is plural and anchor-sensitive, while the transition wedge remains clearly female-leaning. [SOURCE: `sources/iq-sex-diff/data/ffcws/ffcws_y9_relative_gaps.tsv`; `sources/iq-sex-diff/data/ffcws/ffcws_y22_transition_gaps.tsv`; `sources/iq-sex-diff/data/ffcws/ffcws_transition_joint_models.tsv`]

- `P(cause)`: `0.68` that `FFCWS` strengthens the project's existing "multiple surface families" view rather than either falsifying it or simplifying it into a single male-math edge. [INFERENCE]
- `Top alternative`: `0.20` that the `FFCWS` pattern is mostly a disadvantaged urban-cohort special case and should not be generalized into the main synthesis without another non-NCES replication. [INFERENCE]
- `Falsifier`: a similarly disadvantaged public cohort where Year 9 or early-adolescent math, reading, and transition surfaces line up cleanly into one dominant male-math or female-schooling story instead of splitting by anchor and later outcome. [INFERENCE]
- `Decision impact`: treat `FFCWS` as evidence that the transition wedge and the child math-versus-verbal split both survive outside the main NCES / `PSID` stack, but do not use it as a clean transcript/test adjudication dataset. [INFERENCE]

## What This Changes

What hardens:

- the late transition wedge is not confined to `HSLS`, `ELS`, `NELS`, `PSID TAS`, or public `Add Health`
- Year 9 applied-problems math still carries real later-schooling signal in a very different cohort

What softens:

- the lazy version of "boys math, girls verbal" in child data
- any claim that one verbal anchor is enough to stand in for "verbal ability" across cohorts

What stays open:

- whether the female transition residual is evaluation, compliance, aspiration, or another downstream schooling process
- whether the anchor-sensitive child geometry would look cleaner with richer same-age math batteries than `FFCWS` provides

