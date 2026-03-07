# IQ Sex Differences - NLSY97 Course DAG And Robustness Pass

**Date:** 2026-03-06
**Purpose:** use `causal-dag`, `causal-check`, and `causal-robustness` discipline on the late-school `NLSY97` anomaly instead of adding controls ad hoc

---

## Scope

This memo answers two different causal questions that were getting blurred:

1. **Total sex effect question:** what is the causal effect of `sex` on late-school `Math Knowledge`?
2. **Course exposure question:** what is the causal effect of current advanced math-course exposure on late-school `Math Knowledge`?

Those questions do **not** have the same valid control set.

## Part A - DAG Audit For Sex -> Math Knowledge

### Phase 1: Variable Classification

| Variable | Classification | Temporal Order | Justification |
| --- | --- | --- | --- |
| `Sex` | Treatment (`X`) | Fixed at birth | Exposure of interest |
| `MathKnowledge` | Outcome (`Y`) | At CAT-ASVAB test time | Late-school school-knowledge-heavy outcome |
| `PIAT1997` | Mediator / descendant of treatment | Before CAT-ASVAB, after birth | Later cognitive surface already downstream of sex |
| `HighestMath1997` | Mediator | During 1997 schooling | Course placement is downstream of sex and prior schooling |
| `Grades1997` | Descendant of treatment / mediator | During 1997 schooling | Classroom evaluation is downstream of sex and school performance |
| `TranscriptMathGPA` | Descendant of treatment / descendant of outcome-side surfaces | After course performance | Cumulative school-linked output |

### Phase 2: DAG

```text
Sex -> PIAT1997
Sex -> HighestMath1997
Sex -> MathKnowledge
Sex -> Grades1997
Sex -> TranscriptMathGPA
PIAT1997 -> HighestMath1997 [?]
PIAT1997 -> MathKnowledge
PIAT1997 -> Grades1997
HighestMath1997 -> MathKnowledge
HighestMath1997 -> Grades1997
Grades1997 -> TranscriptMathGPA
MathKnowledge -> TranscriptMathGPA [?]
```

Strict validator output is saved at [nlsy97_dag_sex_to_mathknowledge.json](/Users/alien/Projects/research/sources/iq-sex-diff/data/nlsy/nlsy97_dag_sex_to_mathknowledge.json#L1).

### Phase 3: Valid Adjustment Set

- **Valid adjustment set:** `{}` in the observed DAG
- **Excluded and why:**
  - `PIAT1997`: mediator / descendant of `Sex`
  - `HighestMath1997`: mediator
  - `Grades1997`: descendant of treatment
- **Remaining open back-door paths:** none in the observed DAG
- **Unobserved threats:** family background, school context, and selection can still matter in practice, but the key point is simpler: most of the variables we were tempted to “control for” are not valid total-effect controls

### Phase 4: Bad-Control Audit

| Variable | In DAG? | Classification | In valid adjustment set? | Problem? |
| --- | --- | --- | --- | --- |
| `PIAT1997` | Yes | Mediator | No | Over-control |
| `HighestMath1997` | Yes | Mediator | No | Over-control |
| `Grades1997` | Yes | Descendant of treatment | No | Collider / post-treatment bias |

### Phase 5: Specification Output

**STOP for total-effect regression.**

If the estimand is the total effect of `sex` on late-school `Math Knowledge`, then `PIAT`, course ladder, grades, transcript GPA, honors, and test-process variables should not be used as standard controls.

That means many earlier late-school regressions are best read as **surface decomposition / stress tests**, not as total-effect causal models.

## Part B - DAG Audit For Course Exposure -> Math Knowledge

### Phase 1: Variable Classification

| Variable | Classification | Temporal Order | Justification |
| --- | --- | --- | --- |
| `PrecalcPlus1997` | Treatment (`X`) | Current 1997 course exposure | Exposure of interest |
| `MathKnowledge` | Outcome (`Y`) | At CAT-ASVAB test time | Late-school school-knowledge-heavy outcome |
| `Sex` | Pre-treatment confounder | Before course exposure | Affects course sorting and outcome surface |
| `AgeMonths1997` | Pre-treatment confounder | Before test | Affects ladder placement and score level |
| `PIAT1997` | Pre-treatment confounder proxy `[?]` | Before or alongside current course placement | Used as prior-math proxy, but same-round timing is not perfectly clean |
| `SchoolCalcOffer` | Pre-treatment confounder | School context before or during placement | Affects access to advanced course and learned content |
| `SchoolAPOffer` | Pre-treatment confounder | School context before or during placement | Same logic |
| `SchoolIBOffer` | Pre-treatment confounder | School context before or during placement | Same logic |
| `Grades1997` | Mediator / descendant of treatment | During course exposure | Downstream of course-taking |
| `TranscriptMathGPA` | Descendant of treatment | After course performance | Downstream school-linked output |

### Phase 2: DAG

```text
Sex -> PrecalcPlus1997
Sex -> MathKnowledge
Sex -> PIAT1997
AgeMonths1997 -> PrecalcPlus1997
AgeMonths1997 -> MathKnowledge
PIAT1997 -> PrecalcPlus1997 [?]
PIAT1997 -> MathKnowledge
SchoolCalcOffer -> PrecalcPlus1997
SchoolCalcOffer -> MathKnowledge
SchoolAPOffer -> PrecalcPlus1997
SchoolAPOffer -> MathKnowledge
SchoolIBOffer -> PrecalcPlus1997
SchoolIBOffer -> MathKnowledge
PrecalcPlus1997 -> MathKnowledge
PrecalcPlus1997 -> Grades1997
Grades1997 -> TranscriptMathGPA
PrecalcPlus1997 -> TranscriptMathGPA
```

Strict validator outputs:

- base observed-confounder proposal at [nlsy97_dag_precalc_to_mathknowledge.json](/Users/alien/Projects/research/sources/iq-sex-diff/data/nlsy/nlsy97_dag_precalc_to_mathknowledge.json#L1)
- offer-adjusted valid set at [nlsy97_dag_precalc_to_mathknowledge_offer_adjusted.json](/Users/alien/Projects/research/sources/iq-sex-diff/data/nlsy/nlsy97_dag_precalc_to_mathknowledge_offer_adjusted.json#L1)

### Phase 3: Valid Adjustment Set

- **Observed valid adjustment set:** `{Sex, AgeMonths1997, PIAT1997, SchoolCalcOffer, SchoolAPOffer, SchoolIBOffer}`
- **Excluded and why:**
  - `Grades1997`: mediator / descendant of treatment
  - `TranscriptMathGPA`: descendant of treatment
  - `Honors`: likely downstream evaluation surface
  - `ItemsComplete`, posterior variance, effort, room variables: descendants of treatment-time behavior or score-generation descendants, not clean confounders
- **Remaining open back-door paths in the base observed-confounder proposal:** school-offer paths stay open if school-offer proxies are omitted
- **Unobserved threats:** family background, school quality beyond offer flags, and the imperfect timing of `PIAT1997`

### Phase 4: Bad-Control Audit

| Variable | In DAG? | Classification | In valid adjustment set? | Problem? |
| --- | --- | --- | --- | --- |
| `Grades1997` | Yes | Mediator | No | Over-control |
| `TranscriptMathGPA` | Yes | Descendant of treatment | No | Post-treatment bias |
| `Math honors` | Plausibly yes | Descendant / evaluation surface | No | Over-control / collider risk |
| `Effort` | No clean pre-treatment role | Test-time descendant | No | Unjustified for causal adjustment |
| `Items complete` | No clean pre-treatment role | Score-generation descendant | No | Bad control |

### Phase 5: Clean Regression Specification

**Model:** `MathKnowledge ~ PrecalcPlus1997 + Sex + PIAT1997 + AgeMonths1997 + SchoolOffer proxies`

**Treatment:** `PrecalcPlus1997`

**Controls:** `Sex`, `PIAT1997`, `AgeMonths1997`, `SchoolCalcOffer`, `SchoolAPOffer`, `SchoolIBOffer`

**Excluded:** grades, transcript GPA, honors, and test-process descendants

**Estimand:** observed-confounder-adjusted association intended as the best local approximation to the causal effect of current advanced course exposure on `Math Knowledge`

**Threats:** imperfect timing of `PIAT1997`, residual family / school confounding, and heavy missingness in school-offer fields

## Model Results

Primary output table: [nlsy97_course_causal_models.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/nlsy/nlsy97_course_causal_models.tsv#L1)

Model data: [nlsy97_course_causal_model_data.csv](/Users/alien/Projects/research/sources/iq-sex-diff/data/nlsy/nlsy97_course_causal_model_data.csv#L1)

### Main facts

1. The dose-response story fails in the expected direction. In the observed-confounder OLS models, higher current-course thresholds do **not** raise `Math Knowledge` conditional on `Sex`, `PIAT`, and age. The estimates are small to negative:
   - `highest_math`: `-0.0056`
   - `algebra2+`: `-0.0636`
   - `precalc+`: `-0.0550`
   - `calc+`: `-0.0548`
2. The same pattern is not specific to `Math Knowledge`; `Arithmetic Reasoning` is also near null to negative under the same course-threshold models.
3. The female coefficient remains positive on `Math Knowledge` in these models, which means current advanced course exposure is not rescuing the wedge story.
4. Offer-adjusted models on the smaller transcript-offer sample do not reverse that conclusion. The `precalc+` effect on `Math Knowledge` remains negative to near-zero, and the `Arithmetic Reasoning` effect remains small and non-significant.

## Robustness

Corrected sensitivity outputs:

- [nlsy97_course_causal_sensemakr_math_knowledge.json](/Users/alien/Projects/research/sources/iq-sex-diff/data/nlsy/nlsy97_course_causal_sensemakr_math_knowledge.json#L1)
- [nlsy97_course_causal_sensemakr_arithmetic_reasoning.json](/Users/alien/Projects/research/sources/iq-sex-diff/data/nlsy/nlsy97_course_causal_sensemakr_arithmetic_reasoning.json#L1)
- [nlsy97_course_causal_partial_r2.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/nlsy/nlsy97_course_causal_partial_r2.tsv#L1)

### Reading the sensitivity results

For the offer-adjusted OLS `Math Knowledge` model:

- `estimate = -0.050`
- `RV = 0.0377`
- strongest observed benchmark on outcome side: `PIAT1997` with partial `R² = 0.5048`
- `female` benchmark partial `R² = 0.0157`
- `age` benchmark partial `R² = 0.1990`

For the offer-adjusted OLS `Arithmetic Reasoning` model:

- `estimate = -0.0229`
- `RV = 0.0163`
- strongest observed benchmark on outcome side: `PIAT1997` with partial `R² = 0.5128`

So the conditional course-exposure estimates are **fragile**. Even before arguing about latent causality, they are much smaller than the observed prior-math benchmark and therefore should not be used to build a strong exposure story.

## Causal Check

### Phase 0: Characterize Observation

> **Observation:** in the `PIAT`-overlap `NLSY97` sample, girls are less likely than boys to report `precalc+` (`-0.169`) and `calc+` (`-0.200`), yet `Math Knowledge` remains female-leaning (`d = +0.141`) while `Arithmetic Reasoning` is near null / slightly male (`d = -0.036`). [SOURCE: `sources/iq-sex-diff/data/nlsy/nlsy97_transcript_deep_binary.tsv`; `sources/iq-sex-diff/data/nlsy/nlsy97_transcript_deep_surface_gaps.tsv`]
>
> **Null:** if current advanced-course exposure is the main driver of the late-school anomaly, then after observed-confounder adjustment it should load positively on `Math Knowledge`, and girls taking less of it should not retain a positive `Math Knowledge` wedge. [INFERENCE]
>
> **Residual after null:** the exposure coefficients are small to negative and fragile, while the female `Math Knowledge` residual stays positive. [SOURCE: `sources/iq-sex-diff/data/nlsy/nlsy97_course_causal_models.tsv`; `sources/iq-sex-diff/data/nlsy/nlsy97_course_causal_sensemakr_math_knowledge.json`]
>
> **Geometry:** localized late-school wedge, not broad same-cohort mathematical superiority [INFERENCE]
>
> **Magnitude:** current-course effects are `0.00` to `-0.06` SD in the OLS observed-confounder models; the female `Math Knowledge` coefficient stays around `+0.15` to `+0.17` SD [SOURCE: `sources/iq-sex-diff/data/nlsy/nlsy97_course_causal_models.tsv`]
>
> **Lag window:** same school year with imperfect timing between `PIAT`, current course report, and CAT-ASVAB [SOURCE: `https://www.nlsinfo.org/content/cohorts/nlsy97/topical-guide/education/administration-cat-asvab`; `https://www.nlsinfo.org/content/cohorts/nlsy97/topical-guide/education/cognitive-tests`]

### Surviving hypotheses

1. `H1`: the late-school wedge is mainly a `school-knowledge / evaluation-family` surface, not current advanced-course exposure
2. `H2`: the current course flags are poor exposure proxies because of timing, retention, and misalignment with accumulated math pathway
3. `H3`: residual family / school confounding is still large enough that the observed course coefficients are not informative

### Specificity ranking

| Hypothesis | Temporal | Magnitude | Scope | Mechanism | New prediction | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `H1` | 3 | 3 | 3 | 3 | 2 | 14 |
| `H2` | 3 | 2 | 3 | 2 | 2 | 12 |
| `H3` | 2 | 2 | 2 | 2 | 3 | 11 |

### RCA

`H1` chain:

`Sex -> school-knowledge / evaluation-family surface -> MathKnowledge / transcript outputs`

- Link `Sex -> school-knowledge surface`: directional yes, necessary no, proportional uncertain, confounder risk medium
- Link `school-knowledge surface -> observed wedge`: directional yes, necessary yes for this hypothesis, proportional medium, confounder risk medium
- Weakest link: whether the current observed indicators fully separate evaluation from behavior / compliance
- Bad controls: grades, transcript GPA, honors, effort, and items-complete if used as ordinary controls in a total-effect model

`H2` chain:

`Current course flag mismeasures real cumulative exposure -> negative / null conditional exposure coefficients -> wedge appears disconnected from course-taking`

- Weakest link: direct evidence on the timing and meaning of `selfreport_precalc_plus_1997`

## Commit

- **Most likely cause (55%):** the late-school `NLSY97` anomaly is not being driven by current advanced-course exposure; it sits in a school-knowledge / evaluation-family surface that remains distinct from `Arithmetic Reasoning`. [INFERENCE]
- **Top alternative (25%):** current 1997 course flags are poor proxies for the relevant accumulated math pathway, so the negative / null exposure coefficients are mostly measurement failure rather than true null effects. [INFERENCE]
- **Falsifier:** a transcript-rich replication with clearly pre-treatment baseline math and clean course sequencing where advanced math exposure loads strongly and positively on `Math Knowledge`, and the female `Math Knowledge` residual compresses accordingly. [INFERENCE]
- **Decision impact:** stop using the current `NLSY97` self-reported advanced-course flags as a main explanation for the female `Math Knowledge` wedge. The next late-school discriminator should be behavior / compliance versus evaluation, plus an external replication such as `ELS`. [INFERENCE]
