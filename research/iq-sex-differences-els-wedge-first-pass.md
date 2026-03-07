# IQ Sex Differences - ELS Wedge First Pass

**Date:** 2026-03-06  
**Status:** first external replication of the school-linked wedge using public-use `ELS:2002/2012` student and transcript surfaces

## Scope

This pass asks a narrower question than `HSLS`.

> In public-use `ELS`, do school-linked track and evaluation surfaces tilt female while the later tested-math surface remains male-leaning?

This is **not** a full transcript-GPA replication, because the obvious transcript GPA surfaces are suppressed in the public student file. [SOURCE: `sources/iq-sex-diff/data/els/els_02_12_byf3pststu_v1_0.sav`; `sources/iq-sex-diff/data/els/ELS_2002-12_v1_0_CodeBook_RecordFileLayout.zip`]

## Data And Surfaces

Script:

- [SOURCE: `sources/iq-sex-diff/els_wedge_first_pass.py`]

Primary local outputs:

- [SOURCE: `sources/iq-sex-diff/data/els/els_wedge_extract.parquet`]
- [SOURCE: `sources/iq-sex-diff/data/els/els_wedge_overall.tsv`]
- [SOURCE: `sources/iq-sex-diff/data/els/els_wedge_by_ladder.tsv`]
- [SOURCE: `sources/iq-sex-diff/data/els/els_wedge_models.tsv`]
- [SOURCE: `sources/iq-sex-diff/data/els/els_behavior_f1math_dag_output.json`]
- [SOURCE: `sources/iq-sex-diff/data/els/els_behavior_math_sensemakr.json`]

Public-use variables used:

- `BYTXMSTD`, `BYTXRSTD` base-year math and reading standardized scores [SOURCE: `sources/iq-sex-diff/data/els/els_02_12_byf3pststu_v1_0.sav`]
- `F1TXMSTD` first-follow-up math standardized score [SOURCE: `sources/iq-sex-diff/data/els/els_02_12_byf3pststu_v1_0.sav`]
- `F1HIMATH` highest math course of a half year or more [SOURCE: `sources/iq-sex-diff/data/els/els_02_12_byf3pststu_v1_0.sav`]
- `BYS23C` recognized for good grades [SOURCE: `sources/iq-sex-diff/data/els/els_02_12_byf3pststu_v1_0.sav`]
- `BYTM19` math-teacher recommendation for `AP/honors classes/academic honors` [SOURCE: `sources/iq-sex-diff/data/els/els_02_12_byf3pststu_v1_0.sav`]
- `BYMATHSE`, `F1MATHSE` math self-efficacy [SOURCE: `sources/iq-sex-diff/data/els/els_02_12_byf3pststu_v1_0.sav`]
- `BYACTCTL`, `BYHMWRK`, `BYSCSAF2`, `BYS24C`, `BYS24F`, `BYP77O` as the pre-follow-up behavior/compliance block [SOURCE: `sources/iq-sex-diff/data/els/els_02_12_byf3pststu_v1_0.sav`]

Important public-use limitation:

- `F1RGPA`, `F1RAGPH`, `F1RAGPHP`, `F1RHTUN`, and `F1RHMA_C` are present but suppressed in the public student file, so this pass cannot identify a transcript-GPA wedge directly. [SOURCE: `sources/iq-sex-diff/data/els/els_02_12_byf3pststu_v1_0.sav`]

## Main Findings

### 1. The later tested-math surface is male-leaning

In the transcript-observed analytic sample:

- base-year math: `female - male = -0.962` raw points, `d = -0.097`
- first-follow-up math: `female - male = -1.408` raw points, `d = -0.141`

[SOURCE: `sources/iq-sex-diff/data/els/els_wedge_overall.tsv`]

In the same `n = 10,475` common sample used for the full behavior-adjusted model:

- same-sample base `F1TXMSTD_z ~ female`: `beta = -0.173`
- adjusted `F1TXMSTD_z ~ female + BYTXMSTD_z + BYTXRSTD_z + behavior_index_z`: `beta = -0.072`

[SOURCE: `sources/iq-sex-diff/data/els/els_wedge_models.tsv`]

So the later tested-math surface remains male-leaning even after baseline achievement anchoring. [INFERENCE]

### 2. School-linked track surfaces tilt female

Overall:

- `algebra2_plus`: `female - male = +0.0559`
- `trig/precalc/calc`: `female - male = +0.0282`

[SOURCE: `sources/iq-sex-diff/data/els/els_wedge_overall.tsv`]

Conditional on base-year math, reading, and the behavior index:

- `algebra2_plus`: `beta_female = +0.0626`
- `trig/precalc/calc`: `beta_female = +0.0403`

[SOURCE: `sources/iq-sex-diff/data/els/els_wedge_models.tsv`]

That is the same basic geometry already visible in `HSLS`: the later tested-math surface and the later course-track surface do not move together. [INFERENCE]

### 3. Evaluation surfaces also tilt female

Within the public transcript-linked analytic sample:

- recognized for good grades: `female - male = +0.128`

[SOURCE: `sources/iq-sex-diff/data/els/els_wedge_overall.tsv`]

Conditional on base-year math, reading, and action control:

- `recognized_good_grades`: `beta_female = +0.1119`

[SOURCE: `sources/iq-sex-diff/data/els/els_wedge_models.tsv`]

On the cleaner base-year teacher evaluation surface:

- same-sample base `math_teacher_honors_rec ~ female`: `beta = +0.0075`
- adjusted `math_teacher_honors_rec ~ female + BYTXMSTD_z + BYTXRSTD_z + BYACTCTL_z`: `beta = +0.0321`

[SOURCE: `sources/iq-sex-diff/data/els/els_wedge_models.tsv`]

So in `ELS`, female-tilting evaluation is not just “students say grades matter.” It appears on a math-teacher recommendation surface once baseline tested achievement is held fixed. [INFERENCE]

### 4. Within-track tested math still tilts male

Conditional on being in the same highest-math ladder, the later tested-math surface remains male-leaning for most ladder levels:

- pre-algebra/general math: `d = -0.248`
- algebra I: `d = -0.283`
- geometry: `d = -0.263`
- algebra II: `d = -0.234`
- trig/precalc/calc: `d = -0.249`

[SOURCE: `sources/iq-sex-diff/data/els/els_wedge_by_ladder.tsv`]

That means the female track advantage is not just boys dominating the highest ladder and inflating the global test gap. The male test lean survives inside shared ladders. [INFERENCE]

### 5. Behavior/compliance is not the main story here either

The behavior/compliance index is mildly female-leaning:

- `female - male = +0.0649`, `d = +0.133`

[SOURCE: `sources/iq-sex-diff/data/els/els_wedge_overall.tsv`]

But adding it to the main `ELS` follow-up math and track models does not erase the split:

- `F1TXMSTD_z`: still `beta_female = -0.0724`
- `algebra2_plus`: still `beta_female = +0.0626`
- `trig/precalc/calc`: still `beta_female = +0.0403`

[SOURCE: `sources/iq-sex-diff/data/els/els_wedge_models.tsv`]

For the narrower causal-style question `BehaviorIndexBY -> F1MathScore`, the explicit DAG-valid observed adjustment set is `{Sex, BYMath, BYReading}`. [SOURCE: `sources/iq-sex-diff/data/els/els_behavior_f1math_dag_output.json`]

Under that model:

- `behavior_index_z`: `estimate = +0.0781`
- `RV = 0.0778`
- interpretation: `fragile`

[SOURCE: `sources/iq-sex-diff/data/els/els_behavior_math_sensemakr.json`]

So the `ELS` behavior block is usable as a candidate channel, but not strong enough to treat as the main explanation of the later male tested-math surface. [INFERENCE]

## Causal Check

> **Observation:** in public-use `ELS`, later tested math is male-leaning, while higher-math-course reach, grade recognition, and adjusted math-teacher honors recommendations tilt female. [SOURCE: `sources/iq-sex-diff/data/els/els_wedge_overall.tsv`; `sources/iq-sex-diff/data/els/els_wedge_models.tsv`]
>
> **Null:** if school-linked evaluation and placement surfaces are not clean proxies for tested math, then those surfaces can tilt female even when the later standardized math surface tilts male. [INFERENCE]
>
> **Residual after null:** behavior/compliance still contributes some predictive signal for later math, but it does not compress the school-linked versus tested-math split enough to carry the whole explanation. [SOURCE: `sources/iq-sex-diff/data/els/els_behavior_math_sensemakr.json`; `sources/iq-sex-diff/data/els/els_wedge_models.tsv`]

- `P(cause)`: `0.70` that `ELS` supports a real school-linked `evaluation / placement / track` node distinct from the later tested-math node. [INFERENCE]
- `Top alternative`: `0.20` that public-use suppression and teacher-response selection are generating too much of the apparent evaluation tilt. [INFERENCE]
- `Falsifier`: a less-suppressed or restricted-use replication where transcript GPA and teacher-evaluation surfaces stop tilting female once the same base-year achievement anchors are used. [INFERENCE]
- `Decision impact`: the repo should now treat the school-linked wedge as externally replicated across `HSLS` and `ELS`, but still stop short of claiming that the public `ELS` file alone proves a transcript-GPA mechanism. [INFERENCE]

## What This Changes

1. The school-linked wedge is no longer just an `HSLS` one-off. `ELS` now shows the same broad split between later standardized math and school-linked track/evaluation surfaces. [INFERENCE]
2. The public `ELS` file does **not** rescue a broad female tested-math story. Later standardized math remains male-leaning even after base-year anchoring. [SOURCE: `sources/iq-sex-diff/data/els/els_wedge_models.tsv`]
3. The current `NLSY97` late-school anomaly should still be read as narrower than “female quantitative advantage,” but the external `ELS` replication makes it harder to dismiss the school-linked side as just a local coding quirk or one-dataset oddity. [INFERENCE]
4. The next high-value move is now cross-dataset synthesis of the school-linked wedge or a stronger restricted-use transcript pass, not more generic internal slicing of `NLSY97`. [INFERENCE]
