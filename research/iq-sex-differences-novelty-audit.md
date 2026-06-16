# IQ Sex Differences - Novelty Audit

**Date:** 2026-03-07  
**Purpose:** audit which parts of the repo are already in the literature, which parts are mainly synthesis, and which parts still look distinct enough to claim as a research contribution.

This file is narrower than `research/iq-sex-differences-novel-synthesis-roadmap.md`.

It answers only:

1. what is already known
2. what is only partly known
3. what still looks distinct

---

## 1. Short Verdict

The repo does **not** have a strong claim to novelty on any single raw fact like:

- grades and tests differ
- timing matters
- early school math divergence can emerge quickly
- boys do better on some spatial or reasoning-heavy surfaces

Those are already in the literature.

What still looks distinct is the **integrated representation**:

> sex differences are better modeled as recurring surface families with different causal parents than as one stable “IQ gap” or one stable “math gap.”

[INFERENCE]

That is currently strongest as a synthesis contribution. It becomes stronger research if it is validated with:

1. a formal multitrait-multimethod latent model
2. a stronger transcript/process restricted dataset
3. a randomized design

---

## 2. What Is Already In The Literature

### 2.1 Grades versus standardized tests

This is not novel.

- `Lehti & Laaninen 2024` show boys’ grades are lower than would be expected from standardized test scores, and that the grade-test gap is partly explained by effort, interest, and conscientiousness, but not fully. [SOURCE: https://www.frontiersin.org/journals/sociology/articles/10.3389/fsoc.2024.1448488/full]
- The same paper explicitly discusses parallel patterns in math as well as literacy. [SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC11521978/]

So the repo should not claim novelty for “grades and tests diverge by sex.” [INFERENCE]

### 2.2 Timing and response-process effects

This is not novel.

- `Stoevenbelt et al. 2024` show that reducing or removing time pressure shrinks the math gender gap, sometimes substantially, without reducing predictive validity for university performance. [SOURCE: https://academic.oup.com/ej/article/134/664/3461/7693116]
- `Li et al. 2024` use `PIAAC` response-process data to interpret gender DIF items and argue that process data improve fairness interpretation. [SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC11607718/]
- `Liu et al. 2026` extend this by explicitly targeting non-uniform response-time DIF. [SOURCE: https://link.springer.com/article/10.1186/s40536-026-00290-1]
- `Chen, Zhang, and Liu 2026` explicitly target *reducing* DIF via process data rather than just detecting it. [SOURCE: https://www.cambridge.org/core/services/aop-cambridge-core/content/view/69A15CC6FFB38BDCB1F9C0FBDE550A6D/S0033312325100720a.pdf/div-class-title-reducing-differential-item-functioning-via-process-data-div.pdf]

So the repo should not claim novelty for “process data matter” or “timing matters.” [INFERENCE]

### 2.3 Early-school emergence

This is not novel.

- `Martinot et al. 2025` show a rapid male-favoring math gap opening during first grade in France after near parity at school entry. [SOURCE: https://www.nature.com/articles/s41586-025-09126-4]
- `Kuhfeld & Burchinal 2025` report that boys pull ahead during elementary school in a large U.S. assessment setting. [SOURCE: https://edworkingpapers.com/ai25-1297]

So the repo should not claim novelty for “something starts early.” [INFERENCE]

### 2.4 School evaluation, labels, recommendations

This is not novel.

- `Francis, de Oliveira, and Dimmitt 2024` show White males were more likely to be recommended to AP Calculus in an audit design, and name-blind review did not remove the recommendation gap. [SOURCE: https://ideas.repec.org/a/aea/apandp/v114y2024p205-09.html]
- `Gil-Hernández et al. 2024` use a factorial experiment and find bias in educational assessment favoring girls in essay grading and disadvantaging boys in longer-term expectations. [SOURCE: https://sociologicalscience.com/articles-v11-27-743/]
- `Dersch, Heyder, and Eitel 2025` run a video experiment on teachers’ awareness of math-gender stereotype-reinforcing behavior. [SOURCE: https://www.researchgate.net/publication/397308627_Teachers'_awareness_of_math-gender_stereotype-reinforcing_behaviors_in_the_classroom_a_video_experiment]

So the repo should not claim novelty for “teacher/evaluation channels matter.” [INFERENCE]

### 2.5 Transcript modeling beyond GPA

This is no longer novel as a method idea.

- `Shores & Student 2024` use IRT on high school transcripts to estimate transcript strength and course difficulty, explicitly arguing that GPA alone misses selection into harder courses. [SOURCE: https://files.eric.ed.gov/fulltext/ED671123.pdf]

So transcript IRT is a strong next move, but not a novel method in itself. [INFERENCE]

---

## 3. What Is Only Partly Known

### 3.1 Prediction invariance and measurement invariance are rarely integrated

The literature contains the idea, but it is not routine in practice.

- `Culpepper et al. 2019` explicitly argue that empirical work rarely studies prediction invariance and measurement invariance together in the same high-stakes setting. [SOURCE: https://link.springer.com/article/10.1007/s11336-018-9649-2]

This supports the repo’s planned move toward a joint invariance framework. [INFERENCE]

### 3.2 Multitrait-multimethod models exist, but not usually for this exact problem

- MTMM / latent state-trait methodology is standard psychometrics, not a new invention. [SOURCE: https://www.researchgate.net/publication/248780626_Analyzing_Multitrait-Multimethod_Data_A_Comparison_of_Three_Approaches; https://www.cambridge.org/core/product/02A7E7AD369AD0DD50FF1A5AD449ACD9/core-reader]

But I did **not** find a recent paper that explicitly uses an MTMM-like framing to integrate:

1. tested math
2. transcript/grade surfaces
3. school-knowledge versus applied/reasoning splits
4. process/timing surfaces
5. adult numeracy/outcome surfaces

on the same sex-differences question. [INFERENCE]

That means the *method* is not novel, but the *application structure* may still be. [INFERENCE]

---

## 4. What Still Looks Distinct

### 4.1 The surface-family map

This is the best candidate.

The repo now has evidence for a recurring decomposition into:

1. `evaluation`
2. `school-knowledge`
3. `applied/reasoning`
4. `track/quantity`
5. `process/timing`
6. `adult accumulation`

[SOURCE: `research/iq-sex-differences-current-position.md`; `research/iq-sex-differences-school-wedge-extended-synthesis.md`; `research/iq-sex-differences-pisa2018-time-dif-theta.md`; `research/iq-sex-differences-piaac-frontier.md`]

I did **not** find a recent paper that presents the problem in exactly this integrated way across multiple datasets and developmental stages. [INFERENCE]

This is not proof of novelty. But it is the strongest plausible novelty claim the repo has. [INFERENCE]

### 4.2 The localized late-school anomaly

The repo’s `NLSY97` result is stronger than the loose “female quantitative edge” discourse:

- the female-looking anomaly localizes to `Math Knowledge` and related school-knowledge/evaluation surfaces
- it does not generalize to `PIAT Math` or `Arithmetic Reasoning`

[SOURCE: `research/iq-sex-differences-nlsy97-piat-cat-pass.md`; `research/iq-sex-differences-nlsy97-transcript-deep-pass.md`]

I did not find a recent paper making this exact localized same-cohort distinction. [INFERENCE]

That is distinct enough to matter if it is externally replicated. [INFERENCE]

### 4.3 Broad timing versus localized score residuals

The repo’s `PISA` branch now supports a specific synthesis claim:

1. broad female-slower timing exists
2. localized male score-family residuals exist
3. the score geometry does not reduce cleanly to the timing geometry

[SOURCE: `research/iq-sex-differences-pisa2018-time-dif-theta.md`; `research/iq-sex-differences-pisa2018-dif-theta-logit.md`; `research/iq-sex-differences-pisa2018-dif-2pl-anchor.md`]

The literature knows timing and DIF matter, but I did not find a recent paper stating this particular decoupling result in the same integrated setting. [INFERENCE]

### 4.4 Child-branch reconciliation by bridge alignment

The repo’s early-school work does something nontrivial:

1. it starts with apparently contradictory child cohorts
2. it shows that much of the conflict is bridge/anchor-related
3. it keeps the relative `math vs verbal` branch directionally male after multiple anchors and a family-linked public child panel

[SOURCE: `research/iq-sex-differences-early-school-score-alignment.md`; `research/iq-sex-differences-early-school-age-matched-alignment.md`; `research/iq-sex-differences-child-bridge-multi-anchor.md`; `research/iq-sex-differences-public-child-branch-ach.md`]

That is not a new developmental theory, but it is a strong reconciliation of what otherwise looks like internal contradiction. [INFERENCE]

---

## 5. What To Claim Publicly

### Safe

1. The repo’s strongest contribution is an integrated cross-surface representation, not a new universal sex-gap estimate.
2. The most stable female-leaning late-school family is evaluation/school-linked performance.
3. The most stable male-leaning families are applied/reasoning, spatial/figural, and adult numeracy.
4. Broad female-slower timing does not appear sufficient to explain the localized school-age male score residuals.

### Unsafe

1. “We discovered that grades and tests diverge by sex.”
2. “We discovered that timing matters.”
3. “We discovered early male math emergence.”
4. “We discovered transcript selection matters.”

Those are already in the literature. [INFERENCE]

---

## 6. Best Next Moves If The Goal Is Real Novelty

1. **MTMM / latent surface-family paper**
   - strongest synthesis contribution
2. **Restricted `AHAA` / transcript validation**
   - strongest empirical upgrade to the late-school wedge
3. **Process-based DIF reduction**
   - stronger than another DIF detection pass
4. **Original `OMIB` randomized experiment**
   - strongest direct causal test on the matrix branch
5. **Blinded grading / recommendation audit**
   - strongest direct causal test on the evaluation branch

---

## 7. Best Current Answer

The repo is most novel as a **representation**:

> sex differences in cognitive and academic performance are not well-described by one gap. They are better described as recurring surface families that diverge, recombine, and predict differently across developmental stages.

[INFERENCE]

That is the claim to lean on.

If the project wants stronger novelty than that, it needs one of:

1. a formal latent-family model,
2. a restricted-data validation,
3. or a randomized manipulation.

Without one of those, the repo remains strongest as a high-quality synthesis and causal map rather than a new empirical discovery.

---

## 8. Search Notes

I specifically looked for recent work on:

1. grade-test gaps
2. transcript modeling
3. response-time DIF / process-data fairness
4. early-school emergence
5. recommendation / grading audits
6. integrated latent-method frameworks

I found direct support for the component mechanisms, but not a recent paper that integrates them in the same way this repo currently does. That is a search result, not a proof of absence. [INFERENCE]
