# IQ Sex Differences - Master Plan

**Date:** 2026-03-05
**Purpose:** one canonical roadmap for the remaining work needed to move this project from exploratory multi-surface analysis to something stronger, replicated, and defensible.

This file is the operational master plan.

Use it when the question is not "what do we currently think?" but "what exactly do we do next, in what order, with which statistics, until the surviving claims are solid?"

Companion files:

- `research/iq-sex-differences-current-position.md`
- `research/iq-sex-differences-claim-register.md`
- `research/iq-sex-differences-analysis-protocol.md`
- `research/iq-sex-differences-decisive-causal-tree.md`

---

## End State

The project is done when it can make a small number of claims that survive:

1. cross-battery comparison
2. measurement-aware rescoring or item-family decomposition
3. transcript and school-pipeline scrutiny
4. early-school replication
5. advanced-track separation
6. at least one independent cohort replication for each important mechanism

"Solid" does **not** mean one magical coefficient.
"Solid" means the same qualitative story keeps surviving after the obvious ways it could be wrong are attacked directly.

---

## Final Questions

The project should finish by answering these six questions and nothing broader:

1. Which observed sex differences are broad and stable enough to treat as real domain-level phenomena?
2. Which observed differences are mostly measurement-surface effects?
3. Which observed differences are school-pipeline or evaluation/placement effects?
4. When do broad school-math differences first emerge?
5. How much of the upper-track / advanced-math pattern is selection versus residual performance difference?
6. After the earlier nodes are reduced, is there any residual stable battery-invariant difference large enough to justify a general-ability claim?

If a later result does not help answer one of those six questions, it is probably not worth the cycle time.

---

## Working Model

For the rest of the project, treat every observed gap as:

`ObservedGap = LatentDomainGap + MeasurementSurface + EarlySchoolEmergence + SchoolPipeline + TrackSelection + AdultAccumulation + SampleSelection + Noise`

The research job is to estimate which terms are clearly nonzero, which are cohort-specific, and which terms disappear once obvious contamination is removed.

Current lean from the project state:

1. `MeasurementSurface` is definitely live.
2. `SchoolPipeline` is definitely live.
3. `EarlySchoolEmergence` is likely live but still needs direct local confirmation.
4. `TrackSelection` is likely live.
5. `AdultAccumulation` is likely an amplifier.
6. A large battery-invariant residual `LatentGeneralGap` is not yet established.

---

## Non-Negotiable Rules

These rules apply to every stage.

1. Do not treat grades, honors, recommendations, or course placement as clean nuisance controls in primary ability models.
2. Do not treat process descendants like completion counts or posterior variance as clean causal controls. Use them for stress tests and score-surface diagnosis.
3. Do not collapse broad school math, advanced-track math, adult numeracy, adaptive quantitative tests, and IQ composites into one object.
4. Do not move from one dataset to a general claim without a construct map.
5. Do not interpret same-sample attenuation causally unless the adjusted variables are defensible pre-treatment nuisance variables.
6. Do not promote any result to "project conclusion" until it survives at least one nontrivial replication or convergent battery check.

---

## What Counts As A Real Result

A claim graduates from exploratory to operational only if it meets the appropriate bar below.

### Descriptive claim

Needs:

1. correct weights / replicate weights or other documented variance handling
2. frozen sign convention
3. same result under at least one same-sample robustness check
4. no unresolved manifest bug in variable selection or coding

### Mechanism claim

Needs:

1. construct map showing why the compared surfaces differ
2. a predicted footprint that distinguishes the mechanism from alternatives
3. at least one replication in another cohort or battery
4. explicit statement of what is still descendant-contaminated or selection-sensitive

### Strong synthesis claim

Needs:

1. convergence across at least two cohorts or battery families
2. survival after an obvious adversarial test
3. source-backed literature alignment or explicit frontier disagreement
4. a clear falsifier that has been partially attacked

---

## Stage Order

The stage order is not arbitrary. It follows causal leverage.

### Stage 0 - Freeze Inputs And Surface Definitions

**Goal:** make sure later analyses are not invalidated by moving definitions.

**Work:**

1. keep the frozen variable maps, score rules, weights, and sign conventions current in `research/iq-sex-differences-analysis-protocol.md`
2. keep dataset cards updated with what is actually local, partial, metadata-only, or restricted
3. for every dataset, define the exact math / quantitative surface before modeling

**Outputs:**

1. updated protocol file
2. updated dataset cards
3. one short construct table per new dataset

**Stop rule:** do not run new models on a dataset whose scoring or weight handling is still ambiguous.

---

### Stage 1 - Measurement Surface

**Question:** are the disagreements mainly coming from item families, timing, adaptivity, and score construction?

**Why first:** this is the highest-value node and it contaminates almost every later claim.

#### Experiment 1A - `PISA 2018` framework-linked item split

**Data:** local `PISA 2018`

**Goal:** move from generic item heterogeneity to official framework categories.

**Estimands:**

1. sex gap on `PV1MATH` to `PV10MATH`
2. sex gap by official content category
3. sex gap by official process category
4. item-level sex coefficients with item fixed effects and item-family interactions

**Statistics:**

1. weighted descriptive gaps with replicate-weight variance
2. multilevel item models or linear probability models with country fixed effects
3. specification curve:
   - unrestricted
   - same-sample
   - design-only
   - process-stress

**What would harden the node:**

1. female-positive and male-positive items cluster by framework family rather than random noise
2. item-family pattern survives country controls and same-sample restriction

**What would soften it:**

1. item-family differences collapse after proper framework mapping
2. most item heterogeneity turns out to be weak and unstable

#### Experiment 1B - Invariant-item / DIF pass

**Data:** `PISA 2018`, `ICAR`, then any recoverable item-level `NLSY` surface

**Goal:** see how much the gap moves under invariant-item rescoring, using a matching surface that excludes the target items or target family whenever feasible.

**Estimands:**

1. raw-score gap
2. latent-score gap
3. invariant-item rescored gap
4. item-level DIF burden by family

**Statistics:**

1. multi-group IRT where feasible
2. logistic DIF screens
3. anchor-item rescoring
4. leave-item-out or leave-content-family-out matching-score reconstruction
5. rapid-guess / response-time sensitivity when the battery allows it

**Decision rule:** if the sign or a large share of the magnitude moves under invariant-item rescoring, no broad latent claim should be made from the raw score surface. Do not harden residual family ordering from proxy passes that still condition on contaminated matching scores.

**Current status update:** the contamination-aware leave-out pass has now been run and the residual family ordering largely survives. That means Stage 1 no longer blocks the next late-school tranche, though a formal IRT / anchor-item pass is still the upgrade path if publication-grade fairness claims become necessary.

---

### Stage 2 - Early-School Emergence

**Question:** does broad school-math divergence emerge early enough that late-school transcript and advanced-track mechanisms cannot explain it all?

**Datasets in order:**

1. `NLSCYA`
2. `ECLS-K:2011`
3. `ECLS-K`

#### Experiment 2A - Entry versus follow-up gaps

**Goal:** estimate whether broad early math is near zero at entry and then moves male after schooling begins, while keeping separate the absolute math question from the relative `math versus reading` bridge question.

**Estimands:**

1. sex gap at entry wave
2. sex gap at later elementary waves
3. change in the gap over the first school years
4. math-reading profile where available

**Statistics:**

1. weighted repeated-wave gaps
2. repeated-measures growth or stacked-wave models
3. sensitivity to school-entry age and analyzable panel restriction
4. multi-anchor bridge sensitivity where score families are otherwise non-commensurate

**What would harden the node:**

1. near-zero entry followed by repeated male-favoring widening in at least two cohorts

**What would soften it:**

1. stable male lean already present at entry
2. no meaningful widening after aligned scaling
3. direction of the aligned bridge depends heavily on one anchor family only

#### Experiment 2B - Early construct-family split

**Goal:** test whether early divergence is broad math or already concentrated in particular early content families.

**Need:** only if early datasets expose enough subdomain structure.

**Decision rule:** if early broad math widens before transcript or track mechanisms exist, later school-pipeline stories must be layered on top of that fact, not used to replace it.

---

### Stage 3 - School Pipeline And Evaluation / Placement

**Question:** are grades, course-linked surfaces, and school-knowledge-heavy tests a distinct family from alternate tested-math surfaces?

**Datasets in order:**

1. `NLSY97`
2. `HSLS`
3. `ELS:2002`

#### Experiment 3A - Deep `NLSY97` transcript payload pass

**Goal:** unpack the cohort that generated the anomaly using raw transcript detail rather than only derived summaries.

**Current status update:** the first deep pass is now executed in `research/iq-sex-differences-nlsy97-transcript-deep-pass.md`, and the first explicit DAG / robustness follow-up is now executed in `research/iq-sex-differences-nlsy97-course-dag-robustness.md`. Current descriptive result: the wedge survives `PIAT` anchoring plus design, self-reported exposure, and school-offer controls; `Math Knowledge` and transcript math surfaces stay female-leaning while `Arithmetic Reasoning` does not. The first DAG-valid course-exposure pass does not provide a clean positive explanation of the wedge. The main unresolved mechanism is now behavior / compliance versus evaluation, not generic exposure.

**Estimands:**

1. gap by raw course ladder
2. gap by transcript math credits
3. gap by transcript math GPA
4. residual wedge models:
   - `MathKnowledge ~ female + PIAT + ladder + design block`
   - `PIAT ~ female + transcript_math_gpa + ladder + design block`
   - `transcript_math_gpa ~ female + PIAT + ladder + design block`

**Statistics:**

1. same-sample specification curve
2. ladder-stratified descriptive gaps
3. DAG-first causal modeling with treatment-specific adjustment sets
4. post-estimation robustness for causal OLS
5. residual wedge modeling
6. negative-control read with reading/verbal surfaces where sensible

**What would harden the node:**

1. transcript GPA and `Math Knowledge` remain female-tilting while `PIAT Math` and `Arithmetic Reasoning` do not
2. exposure and school-offer blocks fail to erase the wedge in adequate sample

**What would soften it:**

1. the wedge collapses after raw transcript ladder alignment and analyzability correction
2. an external transcript-rich replication shows the `NLSY97` pattern is cohort-local or collapses once engagement / compliance is modeled

**Guardrail:**

Do not let late-school “causal” claims rest on models that control for `PIAT`, current ladder, grades, transcript outputs, honors, or test-process variables without first naming the estimand and showing the DAG that makes those controls admissible.

#### Experiment 3B - `HSLS` wedge refinement

**Goal:** move beyond first-pass GPA and ladder summaries.

**Work:**

1. refine course-ladder categories
2. add baseline-to-follow-up math alignment
3. isolate GPA versus placement versus intention surfaces

#### Experiment 3C - `ELS` replication

**Goal:** test whether the school-surface wedge is structural or cohort-specific.

**Decision rule:** if `HSLS` and `ELS` converge, the wedge becomes a stable project node.

---

### Stage 4 - Track Selection And Upper-Tail Separation

**Question:** are broad-population school math and advanced-track math different causal objects?

**Datasets:**

1. `TIMSS`
2. `TIMSS Advanced`
3. `HSLS`
4. `ELS`

#### Experiment 4A - Broad versus advanced-track decomposition

**Estimands:**

1. broad-population mean gap
2. advanced-track mean gap
3. probability of advanced-track entry conditional on earlier math
4. performance gap within advanced track

**Statistics:**

1. conditional selection models
2. within-track descriptive gaps
3. upper-tail analysis separated from mean-gap analysis

**What would harden the node:**

1. broad-population and advanced-track surfaces keep diverging after prior-math adjustment

**What would soften it:**

1. advanced-track male lean mostly disappears once earlier math and selection are aligned

**Rule:** never use advanced-track evidence as if it were evidence about the whole population.

---

### Stage 5 - Adult Accumulation

**Question:** does adult numeracy mostly continue earlier differences or amplify them?

**Data:** `PIAAC`

#### Experiment 5A - Young-adult versus older-adult amplification

**Estimands:**

1. age-band numeracy gaps
2. education-stratified age-band gaps
3. occupation- or field-proxy-conditioned gaps

**Statistics:**

1. weighted grouped gaps
2. partial-pooling age-band models
3. process-aware stress tests if log files become accessible

**What would harden the node:**

1. male numeracy visible in young adults and then larger in field / occupation intensive environments

**What would soften it:**

1. large adult gap mostly vanishes after aligned field/use/process handling

**Rule:** `PIAAC` is an adult-accumulation node, not a primary adjudicator of school-entry mechanisms.

---

### Stage 6 - Residual General-Ability Claim

**Question:** after the earlier nodes are reduced, is there any stable residual worth calling a battery-invariant general-ability gap?

**This stage should happen last.**

**Required inputs before running it:**

1. at least one invariant-item or DIF-aware measurement pass
2. at least one early-school pass
3. at least one transcript-rich school-pipeline replication
4. broad versus advanced-track separation

#### Experiment 6A - Residual synthesis

**Goal:** estimate how much sign-stable residual remains after obvious surface nodes are explicitly handled.

**Approach:**

1. align surfaces into broad families:
   - early broad math
   - school-knowledge / transcript family
   - applied / reasoning family
   - advanced-track family
   - adult numeracy
   - spatial / mechanical
2. synthesize sign and magnitude by family, not by arbitrary file order
3. ask whether any single latent story still explains the residual better than the family-specific alternative

**Decision rule:** if the residual keeps changing sign by family even after better measurement handling, the project should reject the one-gap generalization.

---

## Cross-Cutting Statistical Program

These are the default statistics for the remainder of the project.

### 1. Specification curves

Every important model family should show:

1. unrestricted
2. same-sample
3. design-only
4. mechanism
5. stress-test

This keeps fragility visible.

### 2. Fixed sign convention

Use one convention everywhere and keep it documented. Do not allow ad hoc flips in memos.

### 3. Weighted design-correct estimation

Use official weights and replicate weights where available. If not available, say so explicitly.

### 4. Item-family before latent metaphysics

If item-level data exist, inspect item-family geometry before jumping to latent-factor claims.

### 5. Partial pooling across countries or cohorts

Where multiple country-waves or cohorts exist, prefer partial pooling or at least explicit between-sample heterogeneity summaries over cherry-picked country tables.

### 6. Negative controls

Use them deliberately:

1. reading or verbal surfaces when testing math-specific school-pipeline stories
2. non-advanced tracks when testing advanced-track selection stories
3. alternate math surfaces in the same cohort when testing measurement-surface stories

### 7. Missingness discipline

For every important result:

1. show unrestricted estimate
2. show same-sample base estimate
3. only then show adjusted estimates

This prevents selection from hiding inside controls.

### 8. Tail discipline

Upper-tail or advanced-track claims must be reported separately from mean-gap claims.

---

## Literature Program

The literature work should now be targeted, not ambient.

### Literature Track A - Measurement / fairness / DIF

Questions:

1. recent subgroup comparability work for adaptive testing
2. response-time DIF and speed-accuracy decomposition
3. item-format and school-knowledge family differences

Use this track to interpret Stages 1 and 6.

### Literature Track B - Early-school emergence

Questions:

1. kindergarten / first-grade math-gap emergence
2. classroom instruction and practice pathways
3. early math versus early reading divergence

Use this track to interpret Stage 2.

### Literature Track C - Evaluation / placement / transcripts

Questions:

1. grade-test wedge
2. teacher evaluation versus tested performance
3. transcript ladder, placement, and course-taking by sex

Use this track to interpret Stage 3.

### Literature Track D - Advanced track and upper tail

Questions:

1. advanced course entry
2. advanced-track persistence
3. upper-tail math and contest-like or reasoning-heavy surfaces

Use this track to interpret Stage 4.

### Literature Track E - Adult accumulation

Questions:

1. field-of-study sorting
2. occupational numeracy use
3. adult process/log-file literature

Use this track to interpret Stage 5.

### Literature workflow

For each track:

1. update the memo only after a new empirical stage lands
2. prefer 2023-2026 papers first, then backfill older canonical pieces
3. mark whether each paper supports, weakens, or redirects the local causal tree
4. explicitly log papers that looked promising but did not survive scrutiny

---

## Validation Ladder

This is the bar for saying the project has something real.

### Level 1 - Descriptive solid

1. multiple datasets point the same way on the same surface family
2. no unresolved coding bug
3. same-sample and weighted handling do not reverse the claim

### Level 2 - Mechanism solid

1. the claim predicts a distinctive footprint
2. that footprint appears in at least two datasets
3. the nearest alternative explanation is actively weakened

### Level 3 - Synthesis solid

1. the surviving mechanism map explains more of the project than the competing slogans
2. major nodes are linked to specific datasets and replications
3. residual uncertainty is explicit and bounded

The project does not need Level 3 on every subquestion before publishing internal conclusions, but it does need Level 2 on the important nodes.

---

## Sequenced Next Actions

If the team just wants the next concrete moves, use this order:

1. recover the official `PISA 2018` compendium or run a second independent coding sensitivity check against the current framework-proxy pass
2. run deep `NLSY97` transcript payload models
3. if needed, return to the child bridge with composition-aware reweighting or a stronger psychometric bridge than reading
4. refine `HSLS` wedge models
5. run `ELS` wedge replication
6. run targeted invariant-item / DIF pass
7. only then draft the residual general-ability synthesis

That order is chosen to kill the highest-value nodes with the data already local.

---

## What The Final Synthesis Should Probably Look Like

Do not expect the end state to be one macho or egalitarian slogan.

The most likely final structure is:

1. some domain differences are real and stable
2. some school-linked surfaces are meaningfully different from alternate tested-math surfaces
3. some divergence emerges early
4. advanced-track math is a different object from broad school math
5. adult numeracy is partly continuation and partly amplification
6. the evidence for one battery-invariant general-ability gap remains weaker than popular discourse assumes

If the final synthesis does **not** look like a decomposed structure of that sort, it should have to beat that structure on evidence, not rhetoric.

---

## Completion Criteria

The project can stop when all of the following are true:

1. Stage 1 has an official-framework and at least one DIF-aware result
2. Stage 2 has at least two early-school cohorts analyzed
3. Stage 3 has one deep same-cohort transcript pass and one external replication
4. Stage 4 has broad versus advanced-track separation with explicit selection logic
5. Stage 5 has adult amplification bounded clearly enough not to be a mystery sink
6. Stage 6 can state whether a residual battery-invariant claim survives, with a straight face, without hiding the failures

At that point the repo will have something real: not a slogan, but a validated causal map with explicit residual uncertainty.
