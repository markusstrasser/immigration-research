# IQ Sex Differences - School-Wedge Mechanism Triage

**Date:** 2026-03-06  
**Scope:** `NLSY97`, `HSLS`, `ELS`, `NELS`

## Why This Memo Exists

The repo had already shown that the late-school wedge is plural.

That still left a sharper question open:

1. do the measured behavior / identity / climate / exposure blocks actually compress the wedge where they should
2. or do they mainly move tested-math surfaces while leaving the evaluation family and the `NLSY97` school-knowledge residual intact

This memo answers that using the already-executed cohort-specific passes rather than another new pooled regression. [SOURCE: `research/iq-sex-differences-nlsy97-behavior-evaluation-pass.md`; `research/iq-sex-differences-nlsy97-course-dag-robustness.md`; `research/iq-sex-differences-hsls-wedge-refinement.md`; `research/iq-sex-differences-els-wedge-first-pass.md`; `research/iq-sex-differences-nels-wedge-first-pass.md`]

## Artifacts

- [school_wedge_mechanism_shift.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/school_wedge_mechanism/school_wedge_mechanism_shift.tsv#L1)
- [school_wedge_mechanism_family_summary.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/school_wedge_mechanism/school_wedge_mechanism_family_summary.tsv#L1)
- [school_wedge_course_mechanism_summary.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/school_wedge_mechanism/school_wedge_course_mechanism_summary.tsv#L1)
- [school_wedge_mechanism_notes.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/school_wedge_mechanism/school_wedge_mechanism_notes.tsv#L1)

Generator:

- [school_wedge_mechanism_triage.py](/Users/alien/Projects/research/sources/iq-sex-diff/school_wedge_mechanism_triage.py#L1)

## Main Result

Across the late-school cohorts, the measured pre-follow-up behavior / identity / climate / anchor blocks do **not** behave like the master explanation of the wedge. [SOURCE: `sources/iq-sex-diff/data/school_wedge_mechanism/school_wedge_mechanism_family_summary.tsv`]

What they do instead is more specific:

1. they compress tested-math surfaces modestly in `HSLS` and strongly in public `ELS`
2. they leave the evaluation family intact or slightly stronger in `HSLS`, `ELS`, and `NELS`
3. they leave the `NLSY97` school-knowledge residual basically unchanged
4. the `NLSY97` course-exposure DAG pass still does not turn current advanced-course flags into a positive explanation of the `Math Knowledge` wedge

That means the surviving late-school read is now tighter:

1. `behavior / compliance / identity` is not carrying the wedge in the way the strong alternative required
2. `course exposure` is not carrying the `NLSY97` school-knowledge wedge either
3. the remaining live late-school family is still `evaluation / transcript-GPA / school-knowledge surface`, not a broad tested-math or course-quantity story [INFERENCE]

## Family-Level Pattern

### Tested math

- `HSLS` later tested math moves from `-0.079` to `-0.045` after the first behavior / identity / teacher-climate block
- `ELS` later tested math moves from `-0.173` to `-0.072` after baseline math/reading plus behavior
- `NELS` later tested math at `F2` moves from `-0.055` to `-0.088` after baseline anchoring
- `NLSY97` `Arithmetic Reasoning` is near zero and stays near zero under the behavior/climate block [SOURCE: `sources/iq-sex-diff/data/school_wedge_mechanism/school_wedge_mechanism_shift.tsv`]

So tested math is the family most likely to move under the obvious pre-follow-up blocks, but it does not converge onto a stable female-leaning result. [INFERENCE]

### Evaluation family

- `HSLS` transcript math GPA rises from `+0.241` to `+0.268`
- `HSLS` highest-math GPA rises from `+0.173` to `+0.196`
- `ELS` recognition rises from `+0.100` to `+0.112`
- `ELS` math-teacher honors recommendation rises from `+0.008` to `+0.032`
- `NELS` recognition stays strongly female at `+0.142` after anchoring
- `NELS` grade quality rises from `+0.086` to `+0.101`
- `NLSY97` transcript math GPA barely moves from `+0.231` to `+0.226` [SOURCE: `sources/iq-sex-diff/data/school_wedge_mechanism/school_wedge_mechanism_shift.tsv`]

This is the central narrowing result. The obvious measured blocks do **not** kill the evaluation family. [INFERENCE]

### Track and quantity

- `HSLS` `precalc_plus` rises slightly from `+0.045` to `+0.053`
- `ELS` `algebra II+` and `trig/precalc/calc` both strengthen slightly after adjustment
- `NELS` academic/rigorous program weakens slightly but stays positive with intervals near zero
- `NELS` transcript math quantity falls from `+0.012` to `+0.001` [SOURCE: `sources/iq-sex-diff/data/school_wedge_mechanism/school_wedge_mechanism_shift.tsv`]

This keeps the earlier read intact: track and quantity are the least stable school-linked family. [INFERENCE]

### `NLSY97` course exposure

The `NLSY97` DAG-valid course-exposure pass still does not support the strong “girls only look better because they took more advanced math” story.

For `Math Knowledge`:

- observed-confounder `wls` treatment betas run from about `-0.042` to `-0.003`
- offer-stress `wls` treatment betas run from about `-0.034` to `-0.003`
- female residuals remain around `+0.170` to `+0.191` [SOURCE: `sources/iq-sex-diff/data/school_wedge_mechanism/school_wedge_course_mechanism_summary.tsv`]

For `Arithmetic Reasoning`, course treatment betas are also weak and mostly negative or null, while the female residual stays near zero. [SOURCE: `sources/iq-sex-diff/data/school_wedge_mechanism/school_wedge_course_mechanism_summary.tsv`]

That is the wrong footprint for a clean course-exposure explanation. [INFERENCE]

## Causal Check

### Observation

Measured pre-follow-up behavior / identity / climate / anchor blocks move tested-math surfaces somewhat, but they do not materially compress the evaluation family and they do not explain the `NLSY97` school-knowledge wedge. [SOURCE: `sources/iq-sex-diff/data/school_wedge_mechanism/school_wedge_mechanism_family_summary.tsv`; `sources/iq-sex-diff/data/school_wedge_mechanism/school_wedge_course_mechanism_summary.tsv`]

### Null

If those blocks were the main explanation of the late-school wedge, then:

1. evaluation and transcript-GPA surfaces should compress materially
2. `NLSY97 Math Knowledge` should move toward zero once behavior/climate or course-exposure blocks are added
3. cross-cohort adjusted effects should converge more strongly than they do now

### Residual After Null

That footprint does not appear.

- `HSLS` and `ELS` tested math compresses somewhat, but school-linked evaluation mostly survives or strengthens
- `NELS` transcript quantity moves toward neutral while evaluation stays female
- `NLSY97` school-knowledge and transcript GPA barely move under the behavior/climate block
- DAG-valid course-exposure treatment effects in `NLSY97` are weak to negative and fragile [SOURCE: `research/iq-sex-differences-nlsy97-course-dag-robustness.md`; `research/iq-sex-differences-nlsy97-behavior-evaluation-pass.md`; `sources/iq-sex-diff/data/els/els_behavior_math_sensemakr.json`; `sources/iq-sex-diff/data/nels/nels_behavior_f2math_sensemakr.json`]

### Best Current Read

The strongest surviving late-school node is now:

`school evaluation / transcript-GPA / school-knowledge surface`

not:

1. broad tested-math ability
2. simple behavior/compliance
3. simple advanced-course exposure [INFERENCE]

## Probabilistic Update

- **Most likely cause (55%):** the late-school split is primarily an evaluation / school-knowledge family phenomenon that is not explained by the first measured behavior or course-exposure blocks. [INFERENCE]
- **Top alternative (20%):** the relevant engagement / stakes / compliance variables are still under-measured, so the behavior story survives in a narrower “wrong indicators” form. [INFERENCE]
- **Another alternative (15%):** transcript and school-linked public observables are still too non-equivalent across cohorts for a sharper causal read. [INFERENCE]
- **Falsifier:** a transcript-rich external replication where a pre-treatment behavior/stakes block or a better-timed course-exposure block materially compresses the school-evaluation and school-knowledge residuals on adequate common samples. [INFERENCE]
- **Decision impact:** stop spending cycles on more internal pooled wedge regressions. The late-school frontier now needs either stronger restricted transcript/process access or a true mediator design, not more same-cohort control shopping. [INFERENCE]
