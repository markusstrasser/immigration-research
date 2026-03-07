# IQ Sex Differences - Next-Level Research Plan

**Date:** 2026-03-06
**Purpose:** identify the next designs that can create genuinely new insight rather than more public-use coefficient reshuffling.

This is the forward-looking companion to:

- `research/iq-sex-differences-current-position.md`
- `research/iq-sex-differences-master-plan.md`
- `research/iq-sex-differences-master-dag.md`
- `research/iq-sex-differences-mediator-design.md`
- `research/iq-sex-differences-restricted-data-plan.md`

---

## 1. Causal-Check Summary

**Observation:** the public-use stack has now localized the disagreement to a small number of surface families. The most stable female-leaning family is school evaluation/GPA, the most stable male-leaning families are applied/reasoning-heavy math and adult numeracy, and the most localized female-looking late-school anomaly is school-knowledge-heavy `Math Knowledge`. [SOURCE: `research/iq-sex-differences-school-wedge-synthesis.md`; `research/iq-sex-differences-pisa2018-dif-leaveout.md`; `research/iq-sex-differences-nlsy97-piat-cat-pass.md`; `research/iq-sex-differences-piaac-frontier.md`]

**Null:** one more public cohort or one more descendant-heavy regression will mostly reshuffle those same surface families without identifying mechanism. [INFERENCE]

**Residual after null:** the project’s bottleneck is now identification, not raw dataset count. [INFERENCE]

**Geometry:** repeated cross-cohort replication plus diminishing marginal returns from more public-use slices. [SOURCE: `research/iq-sex-differences-current-position.md`; `research/iq-sex-differences-execution-plan.md`]

**Magnitude:** the late-school family summary is already stable enough to treat as a real wedge geometry: `gpa mean beta = +0.256`, `evaluation = +0.127`, `tested_math = -0.053`, `tested_math_knowledge = +0.167`. The residual `PISA 2018` family ordering also survives contamination control: `space_shape = -0.015`, `change_relationships = -0.010`, `uncertainty_data = +0.003`. [SOURCE: `sources/iq-sex-diff/data/school_wedge_synthesis/school_wedge_family_summary.tsv`; `sources/iq-sex-diff/data/pisa/pisa2018_dif_leaveout_content_summary.tsv`]

**Lag window:** school entry through early adulthood. The active mechanisms are not all contemporaneous. [INFERENCE]

**Most likely cause (0.72):** the next ceiling is lack of stronger causal design, not lack of another generic public dataset. [INFERENCE]

**Top alternative (0.20):** one high-quality restricted transcript/process dataset could still resolve most of the remaining uncertainty without any new method. [INFERENCE]

**Falsifier:** if another public-use cohort with materially different instrumentation creates a qualitatively new surface family, then the “identification ceiling” claim weakens. [INFERENCE]

**Decision impact:** stop treating “more public regressions” as the default next step. The next jump should be either richer data access, a better identification strategy, or an original experiment. [INFERENCE]

---

## 2. What Counts As A Real Next-Level Insight

A result counts as a real upgrade only if it does at least one of these:

1. separates `measurement surface` from `latent domain` more cleanly than the current `PISA/TIMSS/NLSY` proxy passes
2. separates `school evaluation` from `transcript quantity / track / tested math` under a design that does not rely on bad controls
3. identifies a mechanism on the outcome branch under explicit treatment-dependent-confounding discipline rather than attenuation rhetoric
4. directly randomizes one of the candidate channels

If it does not do one of those things, it is likely just another descriptive extension. [INFERENCE]

---

## 3. Ranked Agenda

## A. Best Restricted-Data Upgrade: `Add Health` Restricted-Use + `AHAA`

**Why it matters**

This is the best live restricted-data upgrade because it combines:

1. a nationally representative school-based cohort
2. transcript detail
3. school context
4. later adult outcomes
5. contractual access that is still open

[SOURCE: https://addhealth.cpc.unc.edu/data/; https://addhealth.cpc.unc.edu/wp-content/uploads/docs/user_guides/DesignPaperWave_I-IV.pdf; http://www.laits.utexas.edu/ahaa/descrip]

**What it can identify better**

- whether the school-evaluation wedge survives when transcript grades, course sequence, school structure, and later outcomes are all in one coherent dataset
- whether transcript course sequence and transcript grades behave like separate mediators
- whether the public `Add Health` grade/attainment result was mostly a coarse proxy for a richer transcript process

**DAG skeleton**

```text
Sex -> transcript grades -> attainment
Sex -> course sequence -> attainment
Sex -> tested/verbal anchor -> attainment
Background -> all school nodes and attainment
School context -> grades, course sequence, attainment
```

**Treatment / outcome**

- treatment: `Sex`
- outcome: attainment, field/major, adult status outcomes
- mediators: transcript grades, math/science sequence, school context, later testing where available
- admissible background block: family SES, parent education, family structure, race/ethnicity, cohort, school stratum

**Bad controls to avoid**

- postsecondary outcomes when estimating school-node effects
- transcript descendants when estimating the total `sex -> attainment` effect
- descendant-heavy “explained by” language unless the mediator design is used

**Stop rule**

If `AHAA` still yields the same family geometry the public stack already shows, stop pretending one more transcript dataset will be decisive by itself. Move to mediator identification or original experiments. [INFERENCE]

---

## B. Best Public-Data Upgrade: Process-Data Rescoring / DIF Reduction

**Why it matters**

This is the highest-value method upgrade available on the data already staged locally.

Recent work now goes beyond “detect DIF” toward:

1. using response-process features to interpret DIF
2. detecting response-time DIF directly
3. using process data to reduce DIF via nuisance-trait surrogates

[SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC11607718/; https://link.springer.com/article/10.1186/s40536-026-00290-1; https://arxiv.org/abs/2504.00136]

**What it can identify better**

- whether the remaining `PISA` / `TIMSS` residual family ordering is mostly latent-domain structure or partly nuisance-process contamination
- whether `space_shape` survives after explicit process-based nuisance adjustment rather than only leave-out matching
- whether response-time DIF is itself part of the school-age geometry

**Why it is genuinely new for this repo**

The repo has already done:

1. raw item-family decomposition
2. plausible-value conditioning
3. leave-item-out and leave-family-out matching

The missing step is process-informed rescoring or process-informed DIF interpretation. That is a different method class, not another slice of the same model. [INFERENCE]

**Recommended implementation order**

1. `PISA 2018`: process-data nuisance-trait surrogate on the current math item extract
2. `TIMSS`: port response-time/item-family logic if process fields support it
3. `NAEP` process data if restricted access opens later

**Stop rule**

If process-informed rescoring barely moves the residual family ordering, measurement surface remains live but smaller, and the next bottleneck shifts toward school evaluation rather than test-process explanations. [INFERENCE]

---

## C. Best Identification Upgrade On Existing Outcomes: Separable / Interventional Mediation

**Why it matters**

The outcome branch is no longer limited by sample size. It is limited by the fact that grades, transcript progression, tested math, and school behavior are sequential descendants with treatment-dependent confounding.

Recent methods directly address that problem:

- separable-effects mediation for longitudinal multilevel / latent-growth settings [SOURCE: https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/s12874-024-02358-4]
- longitudinal modified-treatment-policy mediation [SOURCE: https://arxiv.org/abs/2403.09928] [PREPRINT]
- mediation with treatment-dependent confounders under additional identifying structure [SOURCE: https://arxiv.org/abs/2501.04581] [PREPRINT]
- path-specific educational returns framed as sequential transitions rather than one-shot schooling [SOURCE: https://sciety.org/articles/activity/10.31235/osf.io/sgh3k_v1] [PREPRINT]

**What it can identify better**

- whether the female attainment edge is mediated more through evaluation/GPA than through tested-math surfaces
- whether course progression is mostly a mediator or mostly a downstream consequence of earlier evaluation
- whether the “direct” residual after school-evaluation and transcript pathways is still substantial

**DAG skeleton**

```text
Sex -> behavior_t1 -> grades_t2 -> attainment_t4
Sex -> tested_math_t2 -> attainment_t4
Sex -> transcript_progression_t3 -> attainment_t4
Background -> all intermediate school nodes and attainment
School context -> grades_t2, progression_t3, attainment_t4
```

**Why this is better than more attenuation tables**

Because it treats post-treatment confounding as the main design problem rather than pretending it away. [INFERENCE]

**Stop rule**

If the sequential mediator design becomes too assumption-heavy relative to the observed support, downgrade it and do not call the result identified mediation. Better a restrained partial-mediation analysis than a false clean decomposition. [INFERENCE]

---

## D. Best Original Causal Experiment: Released-Item Randomization

**Why it matters**

This is the cleanest way to attack `MeasurementSurface` directly instead of inferring it from observational score geometry.

The repo already has:

1. released `PISA` items
2. official `ASVAB` sample items
3. a face-valid construct audit

[SOURCE: `research/iq-sex-differences-item-face-validity-audit.md`; https://www.oecd.org/pisa/pisaproducts/pisa-test-questions.htm; https://www.officialasvab.com/recruiters/sample-questions/]

**Proposed design**

Randomize participants across:

1. time limit vs no time limit
2. school-framed vs neutral-framed instructions
3. multiple-choice vs worked-response format where feasible
4. diagram-heavy vs text-heavy presentation
5. calculator/interface aids vs stripped interface

**Treatment / outcome**

- treatment: randomized item condition
- outcome: accuracy, response time, action sequence, confidence, quit/skip rate

**Why this is strong**

Randomization kills the confounding problem that keeps appearing in the observational branch. [INFERENCE]

**What would be decisive**

If the sex gap moves sharply under timing, framing, or format changes, that is direct causal evidence that surface design is part of the observed gap. If the gap barely moves, the latent-domain story strengthens. [INFERENCE]

---

## E. Best Original School-Pipeline Experiment: Blinded Grading / Recommendation Audit

**Why it matters**

The school-linked wedge is now strong enough observationally that the right next move is to randomize the evaluation layer itself.

Relevant recent designs already exist:

- AP recommendation audit: White males more likely to be recommended for AP Calculus at the same apparent preparedness, and name-blind review did not fix it [SOURCE: https://ideas.repec.org/a/aea/apandp/v114y2024p205-09.html]
- factorial grading/expectation experiment in education [SOURCE: https://sociologicalscience.com/download/vol_11/august/SocSci_v11_743to776.pdf]
- teacher stereotype / awareness experiment [SOURCE: https://link.springer.com/article/10.1007/s11218-025-10138-1]

**Proposed design**

Randomize:

1. sex-coded name or sex marker
2. blind vs visible student identity
3. rubric emphasis on effort/behavior vs correctness/mastery
4. recommendation task vs grading task

Use the same math work, same prior record, and same apparent test score.

**Treatment / outcome**

- treatment: evaluator condition or student sex marker
- outcome: grade, honors recommendation, AP recommendation, narrative feedback

**Why this is strong**

It attacks the exact node that now replicates across `HSLS`, `ELS`, `NELS`, `PSID TAS`, and public `Add Health`: school evaluation. [INFERENCE]

**Stop rule**

If the randomized audit finds no evaluation asymmetry, the wedge may still be real but it likely reflects broader behavior/performance bundles rather than evaluator discrimination alone. [INFERENCE]

---

## F. Best Integrative Synthesis: Surface-Family Model

**Why it matters**

This repo’s most novel potential contribution is no longer “one more battery estimate.” It is the family decomposition itself:

1. `evaluation`
2. `school-knowledge`
3. `applied/reasoning`
4. `track/quantity`
5. `process/timing`
6. `adult accumulation`

[INFERENCE]

**What to build**

A hierarchical synthesis model that maps every local observed surface to one of those families and estimates:

1. mean sex effect by family
2. between-dataset heterogeneity by family
3. age-gradient by family
4. whether a common residual remains after family decomposition

**Why this matters**

If that model explains most of the apparent contradictions, the repo has something the literature often lacks: one cross-battery representation instead of separate battery fights. [INFERENCE]

**Stop rule**

If the family classification is too unstable to survive adversarial re-labeling, do not oversell novelty. Then the contribution is still careful synthesis, not a new formal model. [INFERENCE]

---

## 4. Dataset Ranking From Here

### Highest value

1. `Add Health` restricted-use + `AHAA` transcripts  
   [SOURCE: https://addhealth.cpc.unc.edu/data/; http://www.laits.utexas.edu/ahaa/descrip]
2. `NAEP` process data  
   [SOURCE: https://www.nationsreportcard.gov/process_data/; `research/iq-sex-differences-restricted-data-plan.md`; https://manager.researchdatagov.org/RDG_User_Guide.pdf]
3. `HSTS` restricted transcript microdata  
   [SOURCE: https://nces.ed.gov/surveys/slsp/transcripts.asp; `research/iq-sex-differences-restricted-data-plan.md`; https://manager.researchdatagov.org/RDG_User_Guide.pdf]

`Add Health` is the best live restricted path now. `NAEP` and `HSTS` remain scientifically high-value, but the current `NCES` / `ResearchDataGov` route is administratively paused for new applications, so those are preparation targets rather than immediate filings. [SOURCE: `research/iq-sex-differences-restricted-data-plan.md`; https://manager.researchdatagov.org/RDG_User_Guide.pdf]

### Valuable but lower current ROI

4. `SECCYD` as an extra early-childhood stress test, not as the main decisive dataset  
   [SOURCE: https://www.icpsr.umich.edu/web/DSDR/studies/21940]
5. `ABCD` for cognitive-family structure and neurocognition, but it is weaker than transcript-rich education datasets for the active school-pipeline question  
   [SOURCE: https://abcdstudy.org/scientists/data-sharing/; https://abcdstudy.org/scientists/data-sharing-archive/]

---

## 5. Immediate Order Of Operations

1. use the strict node accounting and family representation as the frozen base layer
2. start the `Add Health` restricted-use / `AHAA` application scope
3. prototype process-data nuisance-trait rescoring on local `PISA 2018`
4. freeze the first separable/interventional mediator estimand on one existing cohort before fitting anything
5. design the released-item randomized experiment
6. design the grading/recommendation audit experiment

This ordering matters:

- restricted transcript/process access attacks the best live data gap
- process-data rescoring attacks the best live measurement gap
- mediator design attacks the best live outcome-identification gap
- the two randomized designs are the cleanest way to get causal leverage if the observational frontier stalls

[INFERENCE]

---

## 6. What Not To Do

1. do not keep adding descendant-heavy regression blocks and calling the coefficient movement causal
2. do not add more public cohorts unless they clearly attack a node not already hit by `HSLS/ELS/NELS/PSID/Add Health/FFCWS`
3. do not collapse `grades`, `track`, `school-knowledge`, and `applied math` into one school-pipeline object
4. do not call the residual battery-invariant `g` question resolved before the measurement and evaluation nodes are hit harder

[INFERENCE]

---

## 7. Bottom Line

The next big insight is unlikely to come from another plain observational sex-gap table.

It is most likely to come from one of three things:

1. richer transcript/process access
2. process-data-informed measurement models
3. direct randomized experiments on items or evaluation

That is where the project can still become genuinely more decisive and more original. [INFERENCE]
