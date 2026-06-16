# IQ Sex Differences - Alpha Master Plan

**Date:** 2026-03-07  
**Purpose:** convert the alpha agenda into a full execution program with explicit estimands, epistemic guardrails, dependence order, and stop rules.

This is the canonical "do all of them thoroughly" roadmap for the next research phase.

Companion files:

- `research/iq-sex-differences-current-position.md`
- `research/iq-sex-differences-alpha-research-program.md`
- `research/iq-sex-differences-novel-synthesis-roadmap.md`
- `research/iq-sex-differences-novelty-audit.md`
- `research/iq-sex-differences-execution-plan.md`
- `research/iq-sex-differences-mediator-design.md`
- `research/iq-sex-differences-causal-methods-frontier.md`
- `research/iq-sex-differences-addhealth-ahaa-application-scope.md`

---

## 1. Objective

The next phase should answer this narrower question:

> can the repo move from a strong synthesis of recurring surface families to a set of validated claims about which differences are `trait`, which are `method`, which are `school-pipeline`, and which are `design/process`?

[INFERENCE]

That means the objective is **not**:

1. produce one final global sex-gap coefficient
2. keep extending public-use regressions
3. keep relabeling descriptive attenuation as mechanism

The objective **is**:

1. formalize the surface-family claim
2. separate trait from method where possible
3. separate transcript strength from evaluation
4. test whether any surfaces are both measurement-invariant and prediction-invariant
5. run at least one direct experiment on a live node
6. only escalate to proximal or transport methods once the proxy and source-target maps are explicit

[INFERENCE]

---

## 2. Epistemic Rules

These are mandatory for every workstream.

### 2.1 Evidence hierarchy

1. local raw data and primary technical manuals
2. official dataset documentation and codebooks
3. peer-reviewed psychometric / education papers
4. recent preprints only when the method frontier is newer than the journal cycle
5. commentary pieces and blogs only for narrative mapping, never as core evidence

[SOURCE: `CLAUDE.md`; `research/iq-sex-differences-novelty-audit.md`]

### 2.2 Claim discipline

Every workstream must keep four layers separate:

1. descriptive fact
2. measurement statement
3. causal claim
4. predictive / decision claim

[SOURCE: `research/iq-sex-differences-mediator-design.md`; `research/iq-sex-differences-alpha-research-program.md`]

### 2.3 Mandatory adversarial checks

Before hardening a claim:

1. run `/causal-check` on the observation
2. run `/causal-dag` before any causal regression or adjustment set
3. run `/causal-robustness` only where OLS total-effect or decomposition models are admissible
4. run a literature disconfirmation search
5. update the claim register with a falsifier

[SOURCE: `research/iq-sex-differences-claim-register.md`; `research/iq-sex-differences-alpha-research-program.md`]

### 2.4 What does not count as progress

1. another regression on the same surface with a different control bundle
2. another pooled sex-gap estimate with no new estimand
3. another memo that only restates the same synthesis in new words

[INFERENCE]

---

## 3. Dependency Order

Some projects can run in parallel. Others should not.

### 3.1 Sequential dependencies

1. `Add Health/AHAA` access before transcript-theta adjudication
2. MTMM variable crosswalk before formal latent family modeling
3. one joint invariance target chosen before prediction-invariance work
4. experiment materials frozen before recruitment

[INFERENCE]

### 3.2 Parallelizable branches

These can run at the same time:

1. restricted-data application work
2. public-data MTMM crosswalk and first latent-model prototype
3. `PISA` process-DIF reduction
4. `OMIB` experiment deployment prep
5. blinded grading audit design and materials

[INFERENCE]

### 3.3 Publication logic

The intended paper stack is:

1. **surface-families paper**  
   MTMM + cross-surface representation
2. **school-evaluation / transcript-strength paper**  
   transcript theta + evaluation residual
3. **measurement + prediction invariance paper**  
   same data, same surfaces, same groups
4. **original experiment paper**  
   `OMIB` and/or grading audit

[INFERENCE]

---

## 4. Workstream A - Add Health Restricted-Use + AHAA

**Priority:** highest  
**Why:** best single dataset upgrade for transcript strength, school context, and later outcomes in one coherent frame. [SOURCE: `research/iq-sex-differences-addhealth-ahaa-application-scope.md`]

### A1. Immediate tasks

1. submit the restricted-use / `AHAA` application
2. finalize variable bundle against the live portal
3. freeze the restricted-use research questions before data access
4. prepare the local data-security and IRB materials

[SOURCE: `research/iq-sex-differences-addhealth-portal-fill-guide.md`; `research/iq-sex-differences-addhealth-contract-checklist.md`; `research/iq-sex-differences-addhealth-irb-language-draft.md`]

### A2. Core estimands

1. transcript theta gap by sex
2. evaluation residual gap after transcript theta and tested surfaces
3. transcript theta versus evaluation residual prediction of later outcomes
4. whether school context materially shifts the transcript/evaluation split

[INFERENCE]

### A3. DAG

```text
Sex -> transcript_strength
Sex -> school_evaluation
Sex -> tested_surface
Sex -> attainment

Background -> transcript_strength
Background -> school_evaluation
Background -> tested_surface
Background -> attainment

School_context -> transcript_strength
School_context -> school_evaluation
School_context -> attainment

transcript_strength -> attainment
school_evaluation -> attainment
tested_surface -> attainment
```

[INFERENCE]

### A4. Key outputs

1. transcript theta construction note
2. transcript theta versus GPA versus tested surface memo
3. transcript theta predictive-validity memo
4. updated claim-register entries

### A5. Stop rules

1. if transcript theta mostly absorbs the evaluation family, soften the current “evaluation is distinct” claim
2. if evaluation residual survives transcript theta and predicts outcomes differently, harden the school-evaluation node
3. if transcript quality or missingness is too weak for stable theta estimation, do not force a high-stakes transcript-theta claim

[INFERENCE]

---

## 5. Workstream B - MTMM Surface-Family Model

**Priority:** highest parallel branch  
**Why:** formalizes the repo’s strongest synthesis claim rather than leaving it as a narrative. [SOURCE: `research/iq-sex-differences-alpha-research-program.md`]

### B1. Question

Are the recurring sex differences better represented as differences in latent traits, latent methods, or both?

[INFERENCE]

### B2. Traits

1. `school-knowledge math`
2. `applied/reasoning math`
3. `relative verbal`
4. `visuospatial/figural`
5. `evaluation/performance`

[INFERENCE]

### B3. Methods

1. standardized test
2. transcript/grade
3. recommendation/recognition
4. process/timing
5. later predictive surface

[INFERENCE]

### B4. Dataset mapping

1. child: `ECLS`, `NLSCYA`, `PSID CDS`
2. late school: `NLSY97`, `HSLS`, `ELS`, `NELS`
3. transition/adult: `PSID TAS`, `Add Health`, `PIAAC`

[SOURCE: `research/iq-sex-differences-current-position.md`; `research/iq-sex-differences-school-wedge-extended-synthesis.md`]

### B5. Immediate tasks

1. build a variable crosswalk by trait and method family
2. identify which families are observed in at least two cohorts
3. prototype the smallest viable latent family model on one branch before going cross-cohort
4. compare one-factor, trait-only, method-only, and trait-plus-method structures

[INFERENCE]

### B6. Outputs

1. `MTMM` crosswalk table
2. smallest viable latent family prototype memo
3. full cross-cohort MTMM memo
4. claim-register updates

### B7. Falsifier

If the best-fitting model collapses to weak method structure and one dominant trait factor, the main surface-family novelty claim weakens. [INFERENCE]

### B8. Robustness

Use:

1. model comparison
2. anchor sensitivity
3. family-inclusion sensitivity
4. cohort holdout validation

Do **not** use `/causal-robustness` here. This is a latent measurement problem, not an OLS omitted-variable problem. [SOURCE: `research/iq-sex-differences-alpha-research-program.md`]

---

## 6. Workstream C - Joint Measurement and Prediction Invariance

**Priority:** highest conceptual upgrade  
**Why:** strongest answer to “so what?” and still relatively underused in one unified design. [SOURCE: https://link.springer.com/article/10.1007/s11336-018-9649-2]

### C1. Core question

For a given surface family, is it:

1. measurement-invariant by sex?
2. prediction-invariant by sex?

### C2. First target

Pick one late-school family pair where the wedge is already strong:

1. tested math
2. evaluation / GPA / recommendation

[INFERENCE]

### C3. Four-cell outcome

1. invariant measure / invariant prediction
2. invariant measure / non-invariant prediction
3. non-invariant measure / invariant prediction
4. non-invariant measure / non-invariant prediction

[SOURCE: `research/iq-sex-differences-alpha-research-program.md`; https://link.springer.com/article/10.1007/s11336-018-9649-2]

### C4. Immediate tasks

1. choose the first target surface family
2. identify the cleanest dataset with both later outcomes and enough measurement structure
3. freeze the prediction target before fitting
4. pre-register the decision grid

### C5. Outputs

1. invariance analysis memo
2. prediction-invariance memo
3. combined interpretation memo

### C6. Stop rules

1. if the surface is neither measurement- nor prediction-invariant, do not use it as a high-level ability proxy
2. if it is invariant on both, the case for that surface strengthens even if mean gaps remain

[INFERENCE]

---

## 7. Workstream D - Process-Based DIF Reduction

**Priority:** highest remaining public-data psychometric branch  
**Why:** the current `PISA` branch is saturated on detection; reduction is the real next step. [SOURCE: `research/iq-sex-differences-pisa2018-time-dif-theta.md`; https://doi.org/10.1017/psy.2025.10072]

### D1. Question

Can process data reduce the residual item-family ordering, and if so, which part is process contamination versus stable trait-family structure?

### D2. Immediate tasks

1. define process nuisance surrogates explicitly
2. rerun the `PISA` score-family ordering after process-based reduction
3. compare reduced and unreduced scores on predictive meaning where possible
4. document what still survives

### D3. Outputs

1. process-reduction method note
2. reduced-versus-unreduced family summary
3. claim-register update on the measurement node

### D4. Falsifier

If the residual `space_shape` ordering collapses strongly under process-informed reduction, the trait-family interpretation weakens. [INFERENCE]

### D5. Robustness

Use:

1. anchor sensitivity
2. family-exclusion sensitivity
3. country holdout
4. reduced-score predictive checks

Do **not** use `/causal-robustness`. This is again a measurement design problem. [INFERENCE]

---

## 8. Workstream E - OMIB Timing Experiment

**Priority:** highest direct causal experiment with no licensing dependency  
**Why:** attacks the matrix/timing node directly under randomization. [SOURCE: `research/iq-sex-differences-matrix-experiment-protocol.md`]

### E1. Treatments

1. tight time limit
2. generous time limit
3. optional secondary manipulation: format or presentation burden

### E2. Outcomes

1. accuracy
2. item completion
3. response time
4. skip / quit behavior
5. confidence if collected

### E3. Immediate tasks

1. freeze the exact item set
2. freeze randomization protocol
3. build recruitment and consent materials
4. preregister the comparison and permutation-test analysis

### E4. Primary estimands

1. treatment effect of tighter timing on accuracy by sex
2. interaction of sex by timing condition
3. treatment effect on completion / skip behavior

### E5. Analysis

Use:

1. randomization inference
2. permutation tests
3. pre-specified subgroup contrasts

[SOURCE: https://www.cambridge.org/core/journals/experimental-economics/article/permutation-tests-for-experimental-data/4FDAEE783F1A617C941D7F7DAEA90FE5]

### E6. Stop rules

1. if timing barely changes the sex gap, stop treating timing as the main explanation on the matrix branch
2. if timing materially changes the gap, the matrix branch becomes a direct construct-choice result rather than a pure trait result

[INFERENCE]

---

## 9. Workstream F - Blinded Grading / Recommendation Audit

**Priority:** highest direct test of the evaluation node  
**Why:** the school-evaluation family is strong enough observationally that direct randomization is now justified. [SOURCE: `research/iq-sex-differences-school-wedge-extended-synthesis.md`; https://ideas.repec.org/a/aea/apandp/v114y2024p205-09.html]

### F1. Treatments

1. visible versus blind identity
2. male-coded versus female-coded student marker
3. grading task versus recommendation task
4. optional rubric emphasis variation

### F2. Outcomes

1. grade
2. recommendation probability
3. honors/AP placement decision
4. narrative feedback tone if captured

### F3. Immediate tasks

1. build matched student-work packets
2. freeze rubrics and randomization
3. recruit evaluators
4. preregister outcomes and analysis

### F4. Analysis

Use:

1. randomization inference
2. permutation tests
3. task-specific treatment contrasts

### F5. Stop rules

1. if no evaluation asymmetry appears under randomization, stop using “teacher bias” as the default explanation for the school-evaluation family
2. if asymmetry appears only in recommendation but not grading, narrow the claim to gatekeeping rather than broad evaluation

[INFERENCE]

---

## 10. Workstream G - Mediator Design On Outcomes

**Priority:** only after transcript/evaluation structure is clearer  
**Why:** the outcome branch is otherwise too easy to overclaim. [SOURCE: `research/iq-sex-differences-mediator-design.md`]

### G1. Rule

Do not run new outcome decompositions until the estimand is frozen as one of:

1. total effect
2. descriptive channel decomposition
3. effect modification
4. causal mediation under stronger assumptions

[SOURCE: `research/iq-sex-differences-mediator-design.md`]

### G2. Immediate tasks

1. choose one target outcome family
2. decide whether the design is descriptive or causal
3. write the DAG before adding mediators
4. only run `/causal-robustness` on admissible OLS models

### G3. Stop rules

1. no “direct effect of sex after controlling for grades/tests/transcripts” language without a defended identification strategy
2. no descendant-heavy decomposition promoted as causal mediation

[SOURCE: `research/iq-sex-differences-mediator-design.md`]

---

## 11. Cross-Model and Cross-Literature Review Gates

Each major workstream should pass three review gates before hardening claims:

1. local disconfirmation search against newer papers
2. one cross-model adversarial review for blind spots
3. claim-register update with falsifier and confidence revision

[SOURCE: `research/iq-sex-differences-model-review-2026-03-06.md`; `research/iq-sex-differences-claim-register.md`]

---

## 12. Sequence

### Phase 1 - start now

1. `Add Health/AHAA` application and portal completion
2. MTMM variable crosswalk
3. first joint measurement/prediction invariance target selection
4. `OMIB` experiment preregistration and deployment prep

### Phase 2 - once inputs are ready

1. process-based DIF reduction on `PISA`
2. smallest viable MTMM prototype
3. blinded grading / recommendation audit deployment

### Phase 3 - once restricted data land

1. transcript theta construction
2. transcript theta versus evaluation residual analysis
3. combined transcript/prediction paper

### Phase 4 - synthesis

1. unified surface-families paper
2. school-evaluation / transcript-strength paper
3. measurement plus prediction invariance paper
4. experiment paper

---

## 13. Completion Criteria

This phase counts as complete only if all of the following are true:

1. at least one restricted transcript workstream has actually run
2. at least one latent MTMM or equivalent trait-method model has run
3. at least one joint measurement/prediction invariance analysis has run
4. at least one direct randomized experiment has run
5. the claim register has been updated to distinguish:
   - hardened trait claims
   - hardened method claims
   - softened or killed explanations

[INFERENCE]

If those are not true, the project is still in strong-synthesis mode, not validated-next-level mode. [INFERENCE]

---

## 14. Immediate Next Actions

1. finish the `Add Health/AHAA` submission
2. create the MTMM crosswalk file
3. choose the first joint measurement/prediction invariance target
4. package the `OMIB` study for deployment
5. draft the blinded grading audit materials

That is the shortest path from “interesting synthesis” to “better claims with actual new evidence.” [INFERENCE]
