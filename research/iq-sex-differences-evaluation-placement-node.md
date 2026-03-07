# IQ Sex Differences - Evaluation / Placement Node

**Date:** 2026-03-05
**Purpose:** formalize the evaluation / placement asymmetry node so grades, honors, recommendations, and school-linked placement variables are not treated as clean latent-ability proxies.

---

## Scope

This note is about a narrow question:

> when school-linked variables move the observed sex gap, are they measuring curriculum exposure, or are they partly contaminated by evaluation / placement asymmetry?

It is **not** a memo about the City Journal or Quillette essays as such. Those essays are prompts for hypotheses, not evidence. [INFERENCE]

## Bottom Line

The evaluation / placement node is worth carrying forward.

The best-supported version is narrow:

1. grades and teacher assessments can diverge from standardized test performance in sex-coded ways
2. that makes recent grades, honors, recommendations, and some placement variables unsafe as primary nuisance controls in the `NLSY97` score model
3. this does **not** by itself show that `CAT-ASVAB` math is psychometrically biased toward girls
4. this also does **not** show that broad later representation gaps are evidence about the score node

So this node belongs in the DOE as a **school-linked contamination / mediation channel**, not as a master explanation for the raw test gap.

## Evidence Recital

### 1. Cornwell, Mustard, and Van Parys (2013)

Source:

- EconPapers summary: <https://econpapers.repec.org/article/uwpjhriss/v_3a48_3ay_3a2013_3ai_3a1_3ap_3a236-264.htm>
- Jessica Van Parys page with citation details: <https://www.jessicavanparys.com/research/education>

What the paper supports:

- grades awarded by teachers are not aligned with test scores
- boys with the same test scores are often graded less favorably
- but much of that less favorable treatment **essentially vanishes when noncognitive skills are taken into account**

Why it matters here:

- it supports a real **grade/test wedge**
- it also warns against a simplistic “teacher bias alone” story
- behavior and noncognitive traits are part of the wedge

### 2. Terrier (2020)

Sources:

- ScienceDirect article page: <https://www.sciencedirect.com/science/article/pii/S0272775718307714>
- IZA discussion paper page: <https://www.iza.org/en/publications/dp/10343/boys-lag-behind-how-teachers-gender-biases-affect-student-achievement>

What the paper supports:

- in French middle schools, girls received more favorable non-blind math evaluations conditional on blind scores
- the grading asymmetry had downstream consequences for progress and science-track selection

Why it matters here:

- it supports evaluation asymmetry as a real mechanism on school-linked surfaces
- but it is still a **grading / placement** result, not direct evidence about `CAT-ASVAB` latent math

### 3. Connor et al. (2023)

Sources:

- PubMed: <https://pubmed.ncbi.nlm.nih.gov/35587425/>
- DOI listing page: <https://researchwith.stevens.edu/en/publications/intersectional-implicit-bias-evidence-for-asymmetrically-compound>

What the paper supports:

- across five studies, the largest and most consistent implicit evaluative bias was reported as pro-women / anti-men

Why it matters here:

- it makes evaluation asymmetry a plausible background mechanism
- but transport from generic implicit evaluative bias to U.S. adolescent math placement is weak
- this source should be treated as **context**, not as direct identification for the score node

## What Is Still Unverified Or Overstated

1. The exact claim that males score higher on `NAEP` math within the same highest math course and within the same math-GPA quartile is **not independently verified in this note**. Treat it as a candidate lead, not as an adopted project fact. [UNVERIFIED]
2. The City Journal and Quillette essays are not evidence for the score node. They may point toward a real wedge mechanism, but they cannot carry the inference themselves. [INFERENCE]
3. Hiring-preference or downstream institutional-representation papers do not belong in the current `sex -> school-linked score` node. They are outcome-stage evidence. [INFERENCE]

## Causal Placement

### What this node is

- a mediator / contamination channel for grades, honors, recommendations, and some placement variables
- a reason to treat those school-linked variables as mechanism surfaces rather than as clean controls

### What this node is not

- not a direct confounder of `sex -> CAT-ASVAB score`
- not proof that the test itself is biased
- not proof of a broad ideological story about misogyny or misandry

## Footprint Predictions

If evaluation / placement asymmetry is doing real work, we should see a **grade-test wedge**:

1. females retain a positive grade or placement residual conditional on transcript ladder and standardized math
2. males retain a positive standardized-math residual conditional on grade and ladder
3. the wedge is larger on teacher-assessed or school-placed surfaces than on externally scored standardized surfaces
4. the wedge weakens once behavior / noncognitive / observability channels are modeled explicitly

If this node is weak, then:

1. grade and test residuals should align once transcript ladder and prior math are fixed
2. school-linked variables should behave more like curriculum exposure than evaluation surfaces

## DOE Consequences

### Keep

- transcript / honors / course-ladder variables as mechanism strata
- same-cohort `CAT-ASVAB` versus `PIAT Math` comparison
- behavior / observability weighting as a separate audit

### Do Not Do

- do not put grades, honors, recommendations, and behavior items into the main sex-to-score regression and call the attenuation causal explanation
- do not use downstream hiring or representation evidence to adjudicate the score node

## Immediate Analyses

1. `NLSY97` grade-test wedge audit:
   - `math_grade_residual = GPA net of transcript ladder + standardized math`
   - `math_test_residual = standardized math net of GPA + transcript ladder`
2. `NLSY97` observability audit:
   - compare raw gap, same-sample base gap, and IPW gap
3. `HSLS:09` replication:
   - transcript ladder
   - grade/test wedge
   - identity / aspiration sorting handled separately

## Status

**Adopted as a live mechanism node.**

Confidence:

- `0.75` that grade / placement surfaces are contaminated enough to be unsafe as clean ability proxies
- `0.35` that this node explains a substantial share of the school-linked part of the `NLSY97` quantitative anomaly
- `0.10` that this node is mostly noise

That is deliberately narrower than saying “the misogyny myth essays were right.”

## 2026-03-05 HSLS Update

The first transcript-rich `HSLS` pass materially strengthens this node.

From `research/iq-sex-differences-hsls-wedge-first-pass.md`:

1. girls are near parity at baseline math and slightly below boys on the later
   standardized math surface
2. girls are clearly above boys on transcript math GPA and highest-math-course
   GPA
3. that wedge persists within common highest-math ladders such as `Algebra II`,
   `Precalculus`, and `AP/IB Calculus`
4. girls are slightly **more** likely to reach `precalculus+` conditional on
   baseline math in the first-pass `HSLS` model

Implication:

- the live school-linked node is now better described as a **grade-test /
  classroom-performance wedge** than as a simple “female underplacement” story
- grades and course placement should still not be used as clean nuisance
  controls
- but the strongest underplacement narrative should be softened, because the
  first `HSLS` footprint does not look like girls being generically held back
  from advanced math

## 2026-03-05 NLSY97 PIAT / CAT Update

The new same-cohort pass in [iq-sex-differences-nlsy97-piat-cat-pass.md](iq-sex-differences-nlsy97-piat-cat-pass.md) sharpens this node.

What changed:

1. inside the `PIAT` / `CAT` overlap, `PIAT Math` is slightly male-leaning /
   near null
2. `Arithmetic Reasoning` is also slightly male-leaning / near null
3. the female-looking `NLSY97` signal is concentrated in `Math Knowledge`
4. later transcript math surfaces remain female-favoring

Implication:

- the live school-linked node is now stronger as a **school-knowledge /
  transcript-surface wedge**
- but it should still not be overstated into “girls are just underplaced” or
  “therefore girls have higher IQ”
- the better reading is that school-linked math outputs and some
  school-knowledge-heavy test surfaces move together in a different direction
  from alternate youth math surfaces
