# IQ Sex Differences - PSID CDS Teacher Pass

**Date:** 2026-03-07  
**Purpose:** test whether the remaining public `PSID CDS` child mechanism branch gets materially sharper once school-facing teacher reports are added.

## What Was Added

This pass uses the public elementary/middle-school teacher files in `PSID CDS`:

- `1997`: rich teacher behavior and competence items from `EMSTEACH97`
- `2002`: teacher reading ability, math ability, and discipline-problem items from `EMSTEACH`

[SOURCE: `sources/iq-sex-diff/data/psid/unpacked/CDS1997/1997/EMSTEACH97.do`; `sources/iq-sex-diff/data/psid/unpacked/CDS2002/2002/EMSTEACH.do`]

The new analysis script is:

- `sources/iq-sex-diff/psid_cds_teacher_pass.py`

Outputs:

- `sources/iq-sex-diff/data/psid/psid_cds_teacher_1997_gaps.tsv`
- `sources/iq-sex-diff/data/psid/psid_cds_teacher_1997_models.tsv`
- `sources/iq-sex-diff/data/psid/psid_cds_teacher_2002_gaps.tsv`
- `sources/iq-sex-diff/data/psid/psid_cds_teacher_2002_models.tsv`
- `sources/iq-sex-diff/data/psid/psid_cds_teacher_1997_behavior_sensemakr.json`
- `sources/iq-sex-diff/data/psid/psid_cds_teacher_1997_applied_sensemakr.json`
- `sources/iq-sex-diff/data/psid/psid_cds_teacher_2002_behavior_sensemakr.json`
- `sources/iq-sex-diff/data/psid/psid_cds_teacher_2002_mathrel_sensemakr.json`

[SOURCE: `sources/iq-sex-diff/psid_cds_teacher_pass.py`; `sources/iq-sex-diff/data/psid/psid_cds_teacher_1997_gaps.tsv`; `sources/iq-sex-diff/data/psid/psid_cds_teacher_1997_models.tsv`; `sources/iq-sex-diff/data/psid/psid_cds_teacher_2002_gaps.tsv`; `sources/iq-sex-diff/data/psid/psid_cds_teacher_2002_models.tsv`]

## DAG Discipline

This is a school-facing channel split, not identified mediation.

```text
[Sex] -------------------------------------> [Latent child domain profile]
  |                                                      |
  +-----------------------------------------------------> [Observed applied minus reading]
  |
  +-----------------------------------------------------> [Teacher-rated behavior / discipline]
  |
  +-----------------------------------------------------> [Teacher-rated academic strength]

[Shared family background] -----------------------------> [Teacher ratings]
[Shared family background] -----------------------------> [Observed applied minus reading]
[Age / grade within family] ---------------------------> [Teacher ratings]
[Age / grade within family] ---------------------------> [Observed applied minus reading]
```

Classification:

- treatment: `female`
- outcomes: teacher-facing school surfaces or aligned child `applied_minus_reading`
- admissible within-family nuisance adjustment: `age_years`
- not admissible as total-effect controls: teacher ratings themselves, because they are descendants of `sex` and part of the channel we are trying to understand

[INFERENCE]

So the base family fixed-effects models answer:

- do school-facing teacher surfaces separate by sex inside families?

The teacher-added models answer only:

- does the matched-sample score gap shrink descriptively when those school-facing surfaces are entered?

They do **not** identify clean mediation. [INFERENCE]

## 1997: Rich Teacher Behavior Surface

The `1997` teacher file gives the cleanest public school-facing behavior block now local.

Constructed surfaces:

- `teacher_behavior_index`
  - mean of `argues`, `difficulty concentrating`, `mean to others`, `impulsive`, `restless`
- `teacher_school_disruption`
  - mean of `disobedient at school`, `academic underachiever`, `acts up in class`
- `teacher_academic_comp`
  - teacher global academic competence

[SOURCE: `sources/iq-sex-diff/data/psid/unpacked/CDS1997/1997/EMSTEACH97_codebook.txt`; `sources/iq-sex-diff/psid_cds_teacher_pass.py`]

### Descriptive Gaps

Weighted female-minus-male gaps:

- `teacher_behavior_index`: `d = -0.674`
- `teacher_school_disruption`: `d = -0.628`
- `teacher_academic_comp`: `d = +0.168`
- matched-sample `applied_minus_reading`: `d = -0.485`

[SOURCE: `sources/iq-sex-diff/data/psid/psid_cds_teacher_1997_gaps.tsv`]

So on the public `1997` teacher surface:

- boys are clearly worse on school-facing behavior and disruption
- girls are only slightly ahead on the teacher’s global academic-competence item
- the aligned child `math minus reading` surface still tilts male on the matched teacher subset

[INFERENCE]

### Within-Family Results

Family fixed effects with age adjustment:

- `teacher_behavior_index_z ~ female + age + family FE`
  - `beta_female = -0.426`
  - `SE = 0.162`
- `teacher_school_disruption_z ~ female + age + family FE`
  - `beta_female = -0.324`
  - `SE = 0.140`
- `teacher_academic_comp_z ~ female + age + family FE`
  - `beta_female = +0.027`
  - `SE = 0.124`

[SOURCE: `sources/iq-sex-diff/data/psid/psid_cds_teacher_1997_models.tsv`]

This means the school-facing teacher behavior split is not just family composition noise. It survives opposite-sex sibling comparison. [INFERENCE]

### Does It Explain The Child Bridge?

Matched-sample family fixed-effects on aligned child score:

- base: `applied_minus_reading ~ female + age + family FE`
  - `beta_female = -5.933`
  - `SE = 1.705`
- plus `teacher_behavior_index_z`
  - `beta_female = -6.142`
  - `SE = 1.838`
- plus `teacher_school_disruption_z`
  - `beta_female = -6.332`
  - `SE = 1.748`
- plus `teacher_academic_comp_z`
  - `beta_female = -5.835`
  - `SE = 1.705`

[SOURCE: `sources/iq-sex-diff/data/psid/psid_cds_teacher_1997_models.tsv`]

So the teacher-facing school behavior block does **not** explain away the aligned child `math minus reading` result on the matched `1997` sibling subset. [INFERENCE]

### Robustness

`/causal-robustness` was applied only to the base within-family `1997` edges, because those are the only ones close enough to standing on their own.

- teacher behavior outcome:
  - estimate `-0.308`
  - `RV = 0.159`
- aligned child score outcome:
  - estimate `-5.091`
  - `RV = 0.189`

[SOURCE: `sources/iq-sex-diff/data/psid/psid_cds_teacher_1997_behavior_sensemakr.json`; `sources/iq-sex-diff/data/psid/psid_cds_teacher_1997_applied_sensemakr.json`]

These are robust against an omitted confounder benchmarked only to observed `age_years`, which is a weak benchmark. That means the result is not automatically fragile, but the robustness numbers should not be oversold. [INFERENCE]

## 2002: Teacher Math-vs-Reading Surface

The `2002` teacher file is structurally different. It gives:

- teacher-rated `reading ability`
- teacher-rated `math ability`
- a binary `behavior/discipline problem` item

[SOURCE: `sources/iq-sex-diff/data/psid/unpacked/CDS2002/2002/EMSTEACH_codebook.txt`]

### Descriptive Gaps

Weighted female-minus-male gaps:

- `teacher_reading_ability`: `d = -0.000`
- `teacher_math_ability`: `d = -0.179`
- `teacher_math_minus_reading`: `d = -0.196`
- `teacher_behavior_problem`: `d = -0.480`
- matched-sample `applied_minus_reading`: `d = -0.093`

[SOURCE: `sources/iq-sex-diff/data/psid/psid_cds_teacher_2002_gaps.tsv`]

This is the key directional result:

- teachers do **not** rate girls higher on relative math versus reading
- if anything, boys are seen as relatively stronger in math than reading
- boys are also more likely to be flagged for school behavior/discipline problems

[INFERENCE]

### Within-Family Results

Family fixed effects with age adjustment:

- `teacher_math_minus_reading ~ female + age + family FE`
  - `beta_female = -0.154`
  - `SE = 0.144`
- `teacher_behavior_problem ~ female + age + family FE`
  - `beta_female = -0.241`
  - `SE = 0.080`

[SOURCE: `sources/iq-sex-diff/data/psid/psid_cds_teacher_2002_models.tsv`]

So the public `2002` teacher behavior result is still clearly more male, while the teacher math-vs-reading relative rating is directionally male but imprecise within families. [INFERENCE]

### Does It Explain The Child Bridge?

Matched-sample family fixed-effects on aligned child score:

- base `applied_minus_reading`
  - `beta_female = -7.357`
  - `SE = 6.491`
- plus `teacher_math_minus_reading`
  - `beta_female = -7.549`
  - `SE = 7.231`
- plus `teacher_behavior_problem`
  - `beta_female = -8.488`
  - `SE = 7.119`

[SOURCE: `sources/iq-sex-diff/data/psid/psid_cds_teacher_2002_models.tsv`]

This subset is too thin to resolve mechanism. The point estimates still lean male on aligned child math, but the confidence band is wide enough that the `2002` teacher subset should be treated as directional only. [INFERENCE]

### Robustness

- `teacher_behavior_problem`
  - estimate `-0.228`
  - `RV = 0.245`
- `teacher_math_minus_reading`
  - estimate `-0.156`
  - `RV = 0.112`, but `RV_alpha = 0.0`

[SOURCE: `sources/iq-sex-diff/data/psid/psid_cds_teacher_2002_behavior_sensemakr.json`; `sources/iq-sex-diff/data/psid/psid_cds_teacher_2002_mathrel_sensemakr.json`]

Interpretation:

- the school-behavior result is reasonably stable on the observed benchmark scale
- the teacher math-vs-reading family effect is too imprecise to treat as hardened, regardless of the raw `RV`

[INFERENCE]

## Causal Check

> **Observation:** in public `PSID CDS`, school-facing teacher reports are strongly more male on behavior/disruption, and `2002` teacher math-vs-reading ratings are directionally more male as well; adding these teacher surfaces does not collapse the aligned child `math minus reading` pattern where the matched sibling sample is informative. [SOURCE: `sources/iq-sex-diff/data/psid/psid_cds_teacher_1997_gaps.tsv`; `sources/iq-sex-diff/data/psid/psid_cds_teacher_1997_models.tsv`; `sources/iq-sex-diff/data/psid/psid_cds_teacher_2002_gaps.tsv`; `sources/iq-sex-diff/data/psid/psid_cds_teacher_2002_models.tsv`]
>
> **Null:** once school-facing teacher behavior and relative teacher academic judgments are observed, the public child bridge should mostly collapse because the remaining male edge is really a classroom-behavior or teacher-perception artifact. [INFERENCE]
>
> **Residual:** the public teacher files do not support that collapse. In `1997`, the aligned child bridge survives the richer school-facing teacher block. In `2002`, the teacher math-vs-reading surface points in the same direction as the child bridge rather than reversing it, but the within-family sample is too small to settle mediation. [INFERENCE]

- `P(cause)`: `0.68` that the strongest remaining public teacher evidence does **not** support a simple “school-facing behavior/evaluation artifact explains the child bridge” story. [INFERENCE]
- `Top alternative`: `0.20` that a richer, cleaner school-facing teacher panel with consistent waves could still explain more than the public files reveal, especially on transcript or teacher-test linkage surfaces. [INFERENCE]
- `Falsifier`: a stronger public or restricted teacher/transcript panel where school-facing ratings or placements materially compress the same within-family child `math minus reading` effect. [INFERENCE]
- `Decision impact`: the public child branch is close to saturation. School-facing teacher reports strengthen the claim that boys are more behavior-problematic in school, but they do not currently dissolve the relative child-math pattern. The next meaningful move is stronger transcript/process access, not another light public cohort slice. [INFERENCE]

## What This Settles

What settles enough to use:

- the public child branch now has both caregiver-facing and school-facing behavior checks
- school-facing teacher behavior is even more male than the caregiver block
- the teacher-facing `2002` relative math-versus-reading surface does not point in a female direction

What remains open:

- whether restricted transcript or richer teacher-linked data would identify mediation more cleanly
- whether the `2002` teacher math-vs-reading family effect is real but underpowered
- whether later school-evaluation wedges are driven by channels that are not yet visible in the public child files
