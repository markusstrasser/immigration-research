# IQ Sex Differences - NLSY97 Behavior / Compliance Versus Evaluation Pass

**Date:** 2026-03-06
**Purpose:** test whether the late-school `NLSY97` wedge is mainly a behavior / compliance / observability story or whether that node is weaker than the school-knowledge / evaluation-family story

---

## Scope

This pass uses pre-test or same-year school behavior and climate surfaces rather than test-time descendants.

It asks three narrower questions:

1. do girls and boys differ materially on the available 1997 behavior / compliance and school-climate items in the same cohort?
2. does adding those blocks compress the female residual on `Math Knowledge` or transcript math GPA?
3. is transcript observability selection strong enough to manufacture the wedge?

This is **not** a total-effect model of `sex -> outcome`. It is a mechanism-screening pass with an explicit DAG for the narrower `BehaviorCompliance1997 -> outcome` question.

## Data And Derived Surfaces

Primary extract: [nlsy97_behavior_evaluation_extract.parquet](/Users/alien/Projects/research/sources/iq-sex-diff/data/nlsy/nlsy97_behavior_evaluation_extract.parquet#L1)

Main outputs:

- [nlsy97_behavior_gaps.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/nlsy/nlsy97_behavior_gaps.tsv#L1)
- [nlsy97_behavior_block_models.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/nlsy/nlsy97_behavior_block_models.tsv#L1)
- [nlsy97_behavior_ipw_models.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/nlsy/nlsy97_behavior_ipw_models.tsv#L1)
- [nlsy97_behavior_causal_models.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/nlsy/nlsy97_behavior_causal_models.tsv#L1)
- [nlsy97_behavior_common_sample_models.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/nlsy/nlsy97_behavior_common_sample_models.tsv#L1)
- [nlsy97_dag_behavior_to_mathknowledge.json](/Users/alien/Projects/research/sources/iq-sex-diff/data/nlsy/nlsy97_dag_behavior_to_mathknowledge.json#L1)
- [nlsy97_dag_behavior_to_transcriptgpa.json](/Users/alien/Projects/research/sources/iq-sex-diff/data/nlsy/nlsy97_dag_behavior_to_transcriptgpa.json#L1)
- [nlsy97_behavior_sensemakr_math_knowledge.json](/Users/alien/Projects/research/sources/iq-sex-diff/data/nlsy/nlsy97_behavior_sensemakr_math_knowledge.json#L1)
- [nlsy97_behavior_sensemakr_transcript_gpa.json](/Users/alien/Projects/research/sources/iq-sex-diff/data/nlsy/nlsy97_behavior_sensemakr_transcript_gpa.json#L1)

Derived indices:

1. `behavior_compliance_index_z`
   - lower absence
   - lower lateness
   - lower suspension
   - more homework days
   - more homework time
2. `climate_fairness_index_z`
   - teachers good
   - teacher interest
   - students graded fairly
   - discipline fair
   - feel safe at school
   - lower disruption / cheating climate

## DAG Discipline

For the narrower `BehaviorCompliance1997 -> MathKnowledge` and `BehaviorCompliance1997 -> TranscriptMathGPA` questions, the first observed DAG-valid adjustment set is:

`{Sex, AgeMonths1997, PIAT1997, SampleType1997, SchoolSize1997, StudentTeacherRatio1997}`

Validator results:

- `behavior -> MathKnowledge`: valid at [nlsy97_dag_behavior_to_mathknowledge.json](/Users/alien/Projects/research/sources/iq-sex-diff/data/nlsy/nlsy97_dag_behavior_to_mathknowledge.json#L1)
- `behavior -> TranscriptMathGPA`: valid at [nlsy97_dag_behavior_to_transcriptgpa.json](/Users/alien/Projects/research/sources/iq-sex-diff/data/nlsy/nlsy97_dag_behavior_to_transcriptgpa.json#L1)

Important caveat:

- `PIAT1997 -> BehaviorCompliance1997` is still temporally uncertain, so these are observed-confounder approximations, not clean causal proofs.

## Main Findings

### 1. The available behavior / compliance and climate indices are not strongly sex-differentiated

In the first weighted gaps:

- `behavior_compliance_index_z`: female beta `+0.012`, `p = 0.40`
- `climate_fairness_index_z`: female beta `-0.022`, `p = 0.14`

Most individual items are also small. The only clearly non-null item in this screen is `teachers_good_pos_1997_z`, which is slightly male-leaning (`-0.056`, `p = 0.024`). [SOURCE: `sources/iq-sex-diff/data/nlsy/nlsy97_behavior_gaps.tsv`]

So the basic geometry is already awkward for a strong behavior/compliance explanation: the hypothesized mechanism surfaces are not very sex-separated in this extract.

### 2. Adding behavior or climate blocks barely moves the female late-school wedge

For `Math Knowledge`:

- base context: female beta `+0.193`
- plus behavior: `+0.194`
- plus climate: `+0.194`
- plus behavior + climate: `+0.195`

For transcript math GPA:

- base context: female beta `+0.231`
- plus behavior: `+0.227`
- plus climate: `+0.230`
- plus behavior + climate: `+0.226`

For `Arithmetic Reasoning`, the female residual stays near zero throughout. [SOURCE: `sources/iq-sex-diff/data/nlsy/nlsy97_behavior_block_models.tsv`]

That means this first behavior/compliance screen does **not** explain the wedge in the way the active alternative required.

### 3. Transcript observability weighting does not materially change the residuals

Using transcript-observation IPW:

- `Math Knowledge` female beta moves from `+0.191` to `+0.193`
- transcript GPA female beta moves from `+0.227` to `+0.216`

That is not enough to rescue a strong analyzability / observability story. [SOURCE: `sources/iq-sex-diff/data/nlsy/nlsy97_behavior_ipw_models.tsv`]

### 4. The one non-null behavior effect is sample-sensitive

In the broader DAG-valid behavior model:

- `behavior_compliance_index_z -> MathKnowledge`: `+0.045`, `p = 0.020`
- `behavior_compliance_index_z -> TranscriptMathGPA`: `+0.008`, `p = 0.80`

But once `Math Knowledge`, `Arithmetic Reasoning`, and transcript GPA are forced onto the same transcript-observed sample:

- `behavior -> MathKnowledge`: `+0.024`, `p = 0.34`
- `behavior -> transcript GPA`: `-0.022`, `p = 0.57`

So the apparent positive `behavior -> MathKnowledge` result does not survive the cleaner common-sample comparison. [SOURCE: `sources/iq-sex-diff/data/nlsy/nlsy97_behavior_causal_models.tsv`; `sources/iq-sex-diff/data/nlsy/nlsy97_behavior_common_sample_models.tsv`]

### 5. The non-null behavior effect is fragile even before the common-sample collapse

`sensemakr` on the broader `behavior -> MathKnowledge` model gives:

- `estimate = +0.0468`
- `RV = 0.0424`
- interpretation: `fragile`

The transcript-GPA behavior estimate is even weaker:

- `estimate = +0.0106`
- `RV = 0.0064`
- interpretation: `fragile`

[SOURCE: `sources/iq-sex-diff/data/nlsy/nlsy97_behavior_sensemakr_math_knowledge.json`; `sources/iq-sex-diff/data/nlsy/nlsy97_behavior_sensemakr_transcript_gpa.json`]

## Causal Check

### Observation

The late-school female wedge in `NLSY97` remains concentrated in `Math Knowledge` and transcript math surfaces, while the available pre-test behavior/compliance and climate/fairness indicators are only weakly sex-differentiated and do not materially attenuate the female residual. [SOURCE: `sources/iq-sex-diff/data/nlsy/nlsy97_behavior_gaps.tsv`; `sources/iq-sex-diff/data/nlsy/nlsy97_behavior_block_models.tsv`]

### Null

If behavior / compliance / observability were the main explanation of the late-school wedge, then:

1. those behavior surfaces should show stronger sex separation
2. adding them should compress the female `Math Knowledge` and transcript-GPA residuals materially
3. transcript-observability weighting should move the results more than a few hundredths

### Residual After Null

That footprint does not appear. The female residuals barely move, and the one non-null behavior effect is sample-sensitive and fragile. [SOURCE: `sources/iq-sex-diff/data/nlsy/nlsy97_behavior_block_models.tsv`; `sources/iq-sex-diff/data/nlsy/nlsy97_behavior_ipw_models.tsv`; `sources/iq-sex-diff/data/nlsy/nlsy97_behavior_common_sample_models.tsv`; `sources/iq-sex-diff/data/nlsy/nlsy97_behavior_sensemakr_math_knowledge.json`]

### Surviving Read

This weakens the strong version of the behavior/compliance story inside `NLSY97`.

The current best late-school read is now:

1. the wedge is still real as a `school-knowledge / transcript` surface
2. current advanced-course exposure is not the main explanation
3. the first pre-test behavior/compliance and climate/fairness pass is not the main explanation either
4. the remaining live options are:
   - evaluation-family / school-knowledge surface differences
   - unmeasured engagement or stakes channels not captured by this 1997 block
   - cohort-local school-surface structure that needs external replication

## Probabilistic Update

- **Most likely cause (45%):** the late-school `NLSY97` wedge remains primarily a `school-knowledge / transcript / evaluation-family` surface rather than a behavior/compliance story. [INFERENCE]
- **Top alternative (25%):** the relevant behavior/stakes variables are still under-measured here, so the live behavior story survives only in a weaker “wrong indicators” form. [INFERENCE]
- **Another alternative (20%):** remaining sample and transcript-selection issues still matter, but not enough to explain the wedge on their own. [INFERENCE]
- **Falsifier:** an external transcript-rich replication where behavior/compliance measures materially compress the late-school female `Math Knowledge` or transcript-GPA residual in adequate sample. [INFERENCE]
- **Decision impact:** the next best move is external replication, not more internal `NLSY97` course/behavior slicing. `ELS:2002` now has higher leverage than another local same-cohort stress test. [INFERENCE]
