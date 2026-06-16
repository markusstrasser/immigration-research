# IQ Sex Differences - Alpha Research Program

**Date:** 2026-03-07  
**Purpose:** identify where the current literature is structurally underpowered or siloed, and specify the next designs that would create genuinely stronger claims instead of more familiar regressions.

This file is the practical companion to:

- `research/iq-sex-differences-current-position.md`
- `research/iq-sex-differences-alpha-master-plan.md`
- `research/iq-sex-differences-novel-synthesis-roadmap.md`
- `research/iq-sex-differences-novelty-audit.md`
- `research/iq-sex-differences-next-level-research-plan.md`
- `research/iq-sex-differences-mediator-design.md`
- `research/iq-sex-differences-causal-methods-frontier.md`

---

## 1. Causal-Check Summary

**Observation:** the repo now has a stable empirical pattern that keeps reappearing across child, school, transition, adult, and item/process layers: female-leaning `evaluation` surfaces, mixed or female-leaning `school-knowledge` surfaces, male-leaning `applied/reasoning` and `spatial/figural` surfaces, broad female-slower `process/timing`, and male-leaning `adult numeracy`. [SOURCE: `research/iq-sex-differences-current-position.md`; `research/iq-sex-differences-school-wedge-extended-synthesis.md`; `research/iq-sex-differences-pisa2018-dif-theta-logit.md`; `research/iq-sex-differences-pisa2018-time-dif-theta.md`; `research/iq-sex-differences-raven-open-data.md`; `research/iq-sex-differences-piaac-frontier.md`]

**Null:** the field already knows most of the component facts, so the repo is just another synthesis with no real edge. [SOURCE: `research/iq-sex-differences-frontier-literature-audit.md`; `research/iq-sex-differences-novelty-audit.md`]

**Residual after null:** the likely edge is not a new raw sex-gap fact; it is a better cross-surface representation plus a set of designs that connect literatures that usually stay separate. [INFERENCE]

**Geometry:** repeated convergence across datasets, plus diminishing returns from additional public-use slicing. [SOURCE: `research/iq-sex-differences-next-level-research-plan.md`; `research/iq-sex-differences-execution-plan.md`]

**Magnitude:** strong enough to justify a formal new research program, but not strong enough to claim the final root cause of a battery-invariant male or female general-intelligence gap. [INFERENCE]

**Most likely cause (0.71):** the literature is structurally siloed by method and outcome, so the main alpha is in integrating `measurement`, `evaluation`, `transcript strength`, and `prediction` rather than in finding one more dataset. [INFERENCE]

**Top alternative (0.21):** there is no special alpha here; one restricted transcript dataset plus standard methods will mostly settle the rest. [INFERENCE]

**Falsifier:** a recent integrated paper or project that already combines `measurement invariance`, `prediction invariance`, `transcript-strength IRT`, and `process-based DIF reduction` on the same sex-gap problem with the same surface-family framing. [INFERENCE]

**Decision impact:** the next work should be framed as a small number of paper-grade designs, each with explicit estimands and stop rules. [INFERENCE]

---

## 2. Where The Literature Leaves Alpha

The right frame is not “researchers are dumb.” It is “research programs optimize for different objects and usually stop at their local optimum.” [INFERENCE]

### 2.1 Psychometric fairness work

This literature is strong on:

1. measurement invariance
2. DIF detection
3. partial invariance
4. process-data interpretation of DIF

[SOURCE: https://www.mdpi.com/2079-3200/11/9/180; https://www.researchgate.net/publication/342344680_Examining_gender_DIF_and_gender_differences_in_the_PISA_2018_reading_literacy_scale_A_partial_invariance_approach; https://pmc.ncbi.nlm.nih.gov/articles/PMC11607718/; https://doi.org/10.1027/1015-5759/a000820]

But it usually stops before asking:

1. whether the same surfaces are predictively invariant
2. whether transcript/evaluation surfaces behave like distinct methods measuring overlapping traits
3. whether detected DIF can be reduced and whether that reduction changes downstream interpretation

[SOURCE: https://link.springer.com/article/10.1007/s11336-018-9649-2; https://doi.org/10.1027/1015-5759/a000820; https://doi.org/10.1017/psy.2025.10072]

**Alpha:** move from `is the test fair?` to `which surface families are fair, predictive, and method-distinct?` [INFERENCE]

### 2.2 Education-economics and sociology work

This literature is strong on:

1. grades versus tests
2. recommendations and AP/honors gatekeeping
3. transcript/course-taking pathways
4. attainment consequences

[SOURCE: https://www.frontiersin.org/journals/sociology/articles/10.3389/fsoc.2024.1448488/full; https://ideas.repec.org/a/aea/apandp/v114y2024p205-09.html; https://files.eric.ed.gov/fulltext/ED671123.pdf; https://ideas.repec.org/a/bla/obuest/v87y2025i5p924-941.html]

But it usually uses:

1. coarse test surfaces
2. GPA or ladder summaries rather than formal transcript strength
3. limited psychometric scrutiny of the test side

[SOURCE: https://files.eric.ed.gov/fulltext/ED671123.pdf; https://ideas.repec.org/a/bla/obuest/v87y2025i5p924-941.html]

**Alpha:** stop treating GPA, track, and tested math as interchangeable proxies. [INFERENCE]

### 2.3 Intelligence / cognitive-differences work

This literature is strong on:

1. latent `g`
2. subtest and variance debates
3. high-level construct arguments

[SOURCE: `research/iq-sex-differences-verification.md`; `research/iq-sex-differences-test-construction.md`]

But it usually does not integrate:

1. transcript strength
2. teacher/evaluator surfaces
3. process logs
4. later predictive invariance

[INFERENCE]

**Alpha:** reconnect psychometrics to the actual school and life-course surfaces people smuggle into the debate anyway. [INFERENCE]

### 2.4 Why this matters

The repo’s best synthesis claim already implies the gap:

> the field keeps treating “math” or “ability” as one object, while the data keep sorting into recurring method/trait families.

[SOURCE: `research/iq-sex-differences-novel-synthesis-roadmap.md`; `research/iq-sex-differences-novelty-audit.md`]

That is where the remaining alpha lives. [INFERENCE]

---

## 3. DAG-First Program

The central mistake to avoid is collapsing different questions into one regression. [INFERENCE]

### 3.1 Master treatment/outcome problem

```text
Sex -> latent_trait_family
Sex -> behavior/compliance
Sex -> school_evaluation
Sex -> transcript_strength
Sex -> tested_surface
Sex -> adult_outcomes

Background -> behavior/compliance
Background -> school_evaluation
Background -> transcript_strength
Background -> tested_surface
Background -> adult_outcomes

School_context -> school_evaluation
School_context -> transcript_strength
School_context -> tested_surface
School_context -> adult_outcomes

behavior/compliance -> school_evaluation
behavior/compliance -> tested_surface
school_evaluation -> transcript_strength
school_evaluation -> adult_outcomes
transcript_strength -> adult_outcomes
tested_surface -> adult_outcomes
```

[INFERENCE]

### 3.2 Variable classes

| Node | Class | Why it matters |
| --- | --- | --- |
| `Sex` | treatment / grouping factor | exposure of interest |
| `Background` | pre-treatment confounder block | valid adjustment for total-effect models |
| `School context` | pre-treatment or early-treatment context | can confound school-surface and outcome relations |
| `Behavior/compliance` | mediator or mediator-outcome confounder | usually bad as a default control in sex-effect models |
| `School evaluation` | mediator family | grades, recommendations, recognition |
| `Transcript strength` | mediator family | course rigor plus grade information |
| `Tested surface` | mediator family | applied/reasoning, school-knowledge, matrix, numeracy |
| `Adult outcomes` | outcome family | attainment, field, later numeracy, labor-market outcomes |

[INFERENCE]

### 3.3 What should be estimated separately

1. total-effect models: `Sex -> later outcome`, background-adjusted only  
   [SOURCE: `research/iq-sex-differences-mediator-design.md`]
2. MTMM trait/method models: no single causal coefficient, but latent trait and method loadings  
   [SOURCE: https://www.researchgate.net/publication/248780626_Analyzing_Multitrait-Multimethod_Data_A_Comparison_of_Three_Approaches; https://www.cambridge.org/core/product/02A7E7AD369AD0DD50FF1A5AD449ACD9/core-reader]
3. transcript-strength models: transcript theta versus GPA versus tested theta  
   [SOURCE: https://files.eric.ed.gov/fulltext/ED671123.pdf]
4. joint measurement/prediction invariance: same surface, same data, same group split  
   [SOURCE: https://link.springer.com/article/10.1007/s11336-018-9649-2]
5. randomized experiments: timing/format or grading/recommendation interventions  
   [SOURCE: `research/iq-sex-differences-matrix-experiment-protocol.md`; https://ideas.repec.org/a/aea/apandp/v114y2024p205-09.html]

---

## 4. The Best New Research Designs

## 4.1 MTMM surface-family model

### Why this is high alpha

It turns the repo’s strongest synthesis claim into a formal model instead of a narrative. [INFERENCE]

### Traits

1. `school-knowledge math`
2. `applied/reasoning math`
3. `relative verbal`
4. `visuospatial/figural`
5. `evaluation/performance`

[INFERENCE]

### Methods

1. standardized test
2. transcript/grade
3. recommendation/recognition
4. process/timing
5. later predictive surface

[INFERENCE]

### Candidate datasets

1. child branch: `ECLS`, `NLSCYA`, `PSID CDS` [SOURCE: `research/iq-sex-differences-current-position.md`]
2. late-school branch: `NLSY97`, `HSLS`, `ELS`, `NELS` [SOURCE: `research/iq-sex-differences-school-wedge-extended-synthesis.md`]
3. adult branch: `PIAAC`, `PSID TAS`, `Add Health` public / restricted [SOURCE: `research/iq-sex-differences-psid-tas-transition-first-pass.md`; `research/iq-sex-differences-restricted-data-plan.md`]

### What would count as a real result

1. female-leaning latent method factor for `evaluation` with weaker or opposite latent trait factors on tested reasoning
2. stable method-family loadings across cohorts
3. evidence that some “gap” is method variance masquerading as trait variance

[INFERENCE]

### Disconfirmation

If the MTMM model mostly collapses into one latent factor with weak method structure, the repo’s strongest synthesis claim weakens sharply. [INFERENCE]

## 4.2 Transcript IRT plus evaluation residual

### Why this is high alpha

Transcript IRT exists, but it has not yet been used here to adjudicate the repo’s main school-pipeline split. [SOURCE: https://files.eric.ed.gov/fulltext/ED671123.pdf]

### Core move

Estimate:

1. transcript theta from course-taking plus grades
2. tested theta from standardized surfaces
3. evaluation residual from GPA/recommendation after transcript theta and tested theta

[INFERENCE]

### Strongest target

`Add Health` restricted-use plus `AHAA`, because it can hold transcript detail, school context, and later outcomes in one frame. [SOURCE: `research/iq-sex-differences-addhealth-ahaa-application-scope.md`; `research/iq-sex-differences-addhealth-ahaa-file-crosswalk.md`]

### What would count as a real result

1. transcript theta narrows the GPA/test split substantially
2. evaluation residual remains female after transcript theta and tested theta
3. transcript theta and evaluation residual have different predictive slopes

[INFERENCE]

### Disconfirmation

If transcript theta absorbs most of the evaluation family, then the current “evaluation is distinct” story softens into “crude transcript proxies were the problem.” [INFERENCE]

## 4.3 Joint measurement invariance and prediction invariance

### Why this is high alpha

This is exactly where Millsap says the literature is thin. [SOURCE: https://link.springer.com/article/10.1007/s11336-018-9649-2]

### Core move

For each surface family, estimate:

1. measurement invariance by sex
2. prediction invariance by sex for later outcomes

Then classify each surface into:

1. invariant measure / invariant prediction
2. invariant measure / non-invariant prediction
3. non-invariant measure / invariant prediction
4. non-invariant measure / non-invariant prediction

[INFERENCE]

### Why this matters

It answers the real policy question:

> even if a surface shows group differences, is it measuring the same thing, and does it predict the same later object?

[INFERENCE]

### Disconfirmation

If most surfaces are already invariant on both dimensions, the repo’s “plural surface” story becomes less practically important. [INFERENCE]

## 4.4 Process-based DIF reduction, not just detection

### Why this is high alpha

The current repo already has strong evidence on `PISA` timing and residual item-family ordering. The field is only recently moving from `detect DIF` to `reduce DIF`. [SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC11607718/; https://doi.org/10.1017/psy.2025.10072]

### Core move

Use response-process data to build nuisance-process surrogates, then compare:

1. raw DIF / residual family ordering
2. process-informed reduced DIF ordering
3. downstream predictive meaning of the reduced score

[INFERENCE]

### What would count as a real result

1. `space_shape` survives reduction, which strengthens a trait-family interpretation
2. or `space_shape` collapses strongly, which strengthens a process-design interpretation

[INFERENCE]

### Disconfirmation

If reduction barely moves anything and prediction is unchanged, the process-data branch becomes less central than the school-evaluation branch. [INFERENCE]

## 4.5 Original experiments

### A. OMIB matrix experiment

Already staged locally. The right manipulations are:

1. tight versus generous time
2. format/presentation burden
3. possibly confidence or quit/skip prompts

[SOURCE: `research/iq-sex-differences-matrix-experiment-protocol.md`; `research/iq-sex-differences-open-matrix-assets.md`]

### B. Blinded grading / recommendation audit

The right move is not another “teacher bias” regression. It is randomization. Relevant recent designs already show how to do this. [SOURCE: https://ideas.repec.org/a/aea/apandp/v114y2024p205-09.html; https://ideas.repec.org/a/bla/obuest/v87y2025i5p924-941.html]

---

## 5. Robustness Discipline

`sensemakr` is useful here, but only on the branches where OLS total-effect or descriptive decomposition models are still admissible. [INFERENCE]

### Use `/causal-robustness` on

1. background-adjusted `Sex -> attainment` models
2. transcript-theta versus outcome OLS models
3. evaluation-residual versus outcome OLS models

[SOURCE: `research/iq-sex-differences-mediator-design.md`; `research/iq-sex-differences-nlsy97-course-dag-robustness.md`]

### Do not pretend `/causal-robustness` solves

1. MTMM latent factor identification
2. DIF / invariance problems
3. transcript IRT measurement construction
4. randomized experiment analysis

[INFERENCE]

### Replacement tools by design

| Design | Main robustness tool |
| --- | --- |
| MTMM / latent models | invariance sensitivity, model-comparison, anchor sensitivity |
| transcript IRT | item/course exclusion, school heterogeneity sensitivity, predictive validation |
| process-DIF reduction | anchor sensitivity, cross-family stability, predictive value after reduction |
| randomized OMIB / grading audit | permutation/randomization inference |

[SOURCE: https://files.eric.ed.gov/fulltext/ED671123.pdf; https://doi.org/10.1017/psy.2025.10072; https://www.cambridge.org/core/journals/experimental-economics/article/permutation-tests-for-experimental-data/4FDAEE783F1A617C941D7F7DAEA90FE5]

---

## 6. Ranked Alpha Agenda

1. **`Add Health` restricted-use plus `AHAA` transcript-theta program**  
   Best single dataset upgrade. It can adjudicate the school-pipeline split in one coherent cohort. [SOURCE: `research/iq-sex-differences-addhealth-ahaa-application-scope.md`]

2. **Formal MTMM surface-family model on the existing cross-cohort stack**  
   Best synthesis-to-method upgrade. It operationalizes the repo’s strongest distinct claim. [INFERENCE]

3. **Joint measurement plus prediction invariance on one high-leverage surface family**  
   Best “so what?” upgrade. It answers whether a surface is both comparable and decision-relevant. [SOURCE: https://link.springer.com/article/10.1007/s11336-018-9649-2]

4. **Transcript theta plus evaluation residual paper**  
   Best school-pipeline paper if the restricted transcript access lands. [SOURCE: https://files.eric.ed.gov/fulltext/ED671123.pdf]

5. **Process-based DIF reduction on `PISA`**  
   Best remaining public-data psychometric move. [SOURCE: https://doi.org/10.1017/psy.2025.10072]

6. **OMIB timing experiment**  
   Best original causal experiment with no new licensing barrier. [SOURCE: `research/iq-sex-differences-matrix-experiment-protocol.md`]

7. **Blinded grading / recommendation audit**  
   Best direct test of the evaluation node. [SOURCE: https://ideas.repec.org/a/aea/apandp/v114y2024p205-09.html]

---

## 7. Safe And Unsafe Claims

### Safe now

1. The literature’s contradictions are better represented as recurring surface families than as one stable sex-gap object. [SOURCE: `research/iq-sex-differences-novelty-audit.md`; `research/iq-sex-differences-novel-synthesis-roadmap.md`]
2. The field appears more siloed by method and outcome than the public debate admits. [SOURCE: https://link.springer.com/article/10.1007/s11336-018-9649-2; https://files.eric.ed.gov/fulltext/ED671123.pdf; https://doi.org/10.1017/psy.2025.10072; https://ideas.repec.org/a/bla/obuest/v87y2025i5p924-941.html]
3. The next real gains come from integrating transcript, psychometric, process, and predictive layers, not from another generic public-use regression. [SOURCE: `research/iq-sex-differences-next-level-research-plan.md`; `research/iq-sex-differences-mediator-design.md`]

### Unsafe now

1. “We have discovered the root cause.”
2. “Teacher bias explains the wedge.”
3. “Timing explains the male score residual.”
4. “Transcript theta will settle the whole debate.”
5. “This proves men or women have higher general intelligence.”

[INFERENCE]

---

## 8. Minimal Next Execution Order

1. Finish the `Add Health/AHAA` restricted-use submission using the existing scope and form drafts. [SOURCE: `research/iq-sex-differences-addhealth-portal-fill-guide.md`; `research/iq-sex-differences-addhealth-irb-language-draft.md`]
2. Draft the exact MTMM variable crosswalk by cohort and surface family. [INFERENCE]
3. Pre-register one joint measurement/prediction invariance pass on the most stable late-school family split. [INFERENCE]
4. Run the `OMIB` timing pilot if human subjects are available sooner than restricted data. [SOURCE: `research/iq-sex-differences-matrix-experiment-protocol.md`]

The constraint is no longer imagination. It is selecting one of these and actually taking it far enough to break or harden the current synthesis. [INFERENCE]
