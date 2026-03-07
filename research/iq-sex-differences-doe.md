# IQ Sex Differences - Research Program and DOE

**Date:** 2026-03-05
**Purpose:** turn the current literature review, causal graph, and downloaded datasets into a disciplined research program that can separate measurement artifacts, real domain differences, schooling/practice channels, and outcome relevance.

---

## Executive Aim

The goal is **not** to answer one vague question like "are men or women smarter?"

The goal is to answer four narrower questions in the right order:

1. **Measurement question:** is the disagreement in the literature mostly caused by battery composition, timing, and composite weighting?
2. **Domain question:** which sex differences are stable at the subtest or domain level?
3. **Causal-channel question:** how much of those stable domain gaps are explained by family background, schooling, practice, and task format?
4. **Outcome question:** do any of these gaps matter for education, earnings, occupation, or life success after controls?

If these questions are collapsed into one slogan, the project will drift back into narrative rather than inference. [INFERENCE]

---

## Core Observation

The stable empirical pattern is:

- domain-specific sex differences replicate more reliably than a single overall `g` gap
- male-favoring results are stronger in spatial / mechanical material
- female-favoring results are stronger in clerical coding / scanning / naming material
- overall composite differences move around when batteries, timing rules, and latent models change

[SOURCE: `research/iq-sex-differences-verification.md`; `research/iq-sex-differences-timing-channels.md`; `research/iq-sex-differences-causal-graph.md`]

## Null

If there is **no large stable sex difference in general intelligence**, then a mix of:

- real domain-specific differences
- schooling / literacy practice
- task-format effects
- timing rules
- sample selection
- composite weighting

can generate the observed literature without requiring a single global latent-`g` gap. [INFERENCE]

---

## Epistemic Rules

1. Treat **sex**, **measured subtest performance**, **latent factor estimates**, and **life outcomes** as different objects.
2. Do not infer biology from persistence alone.
3. Do not infer socialization from plausibility alone.
4. Do not infer real-world success from a subtest gap unless criterion-validity evidence is shown directly.
5. Do not claim a root cause unless the proposed cause predicts a footprint that competing hypotheses do not.
6. Use the same estimand across datasets wherever possible so cross-dataset comparisons are real, not rhetorical.

---

## Stage Gates Before Main Analysis

### Stage -1 - Pre-Analysis Lock

Before any analyst estimates sex gaps from the local microdata, freeze:

1. the exact model formulas
2. the composite-weight grid
3. the covariate block order
4. the sibling-pair construction rule
5. the numeric decision thresholds used later in the decision tree

This can be done in a dated markdown protocol or a timestamped analysis script. The point is not ceremony. The point is to keep the DOE from becoming post-hoc narrative dressed up as prespecification. [INFERENCE]

Current implementation:

- protocol lock: `research/iq-sex-differences-analysis-protocol.md`
- machine-readable config: `sources/iq-sex-diff/stage0_config.py`

### Stage 0 - Data Audit, Precision Audit, and Attrition Audit

Stage 0 is not just variable discovery. It also needs:

1. row counts and missingness tables
2. effective sample sizes for the demanding cells
3. minimum detectable effect calculations for the sibling-FE and country-stratified analyses
4. an attrition / selection audit for the longitudinal datasets

If a primary design cell cannot reliably detect the effect sizes the literature cares about, the DOE should mark that experiment as precision-limited before looking at the coefficient. [INFERENCE]

### Stage 0A - Analysis-Target Audit

Before cross-dataset comparisons or outcome models begin, freeze the dataset-specific scoring and survey-design choices:

1. exact score variable(s) used
2. raw vs normed vs latent scoring
3. weight variable and variance-estimation rule
4. plausible-value handling for `PIAAC`
5. attrition / selection adjustment rule
6. whether the estimand is population-weighted or sample-descriptive
7. the executable sibling-pair construction algorithm for `NLSY79`

This is where the project stops scoring choices from quietly becoming findings. [INFERENCE]

Current implementation:

- dataset cards: `research/iq-sex-differences-dataset-cards.md`
- executable sibling-pair builder: `sources/iq-sex-diff/build_nlsy79_sibling_pairs.py`
- local audit snapshot: `sources/iq-sex-diff/data/stage0_audit_snapshot.json`
- first executed results: `research/iq-sex-differences-first-pass-results.md`
- second executed results: `research/iq-sex-differences-second-pass-results.md`
- cohort replication results: `research/iq-sex-differences-nlsy97-replication.md`
- PIAAC frontier results: `research/iq-sex-differences-piaac-frontier.md`
- PIAAC age / occupation extension: `research/iq-sex-differences-piaac-age-occupation.md`
- next-node validation memo: `research/iq-sex-differences-next-node-validation.md`
- NLSY97 Stage A results: `research/iq-sex-differences-nlsy97-stage-a.md`

### Stage 0.5 - Measurement Invariance / DIF Gate

For batteries where item-level information is available, test measurement invariance or DIF before treating score differences as latent-trait differences.

Priority targets:

- `ICAR / SAPA`
- `NLSY79 ASVAB`
- `NLSY97 CAT-ASVAB`

If scalar invariance or a usable invariant-item subset is not available, treat the affected domain as measurement-contaminated and downgrade causal claims built on raw score gaps. [INFERENCE]

---

## Hypothesis Register

### H1 - Global `g` Gap Hypothesis

There is a stable male advantage in general intelligence, and the literature mainly disagrees because some batteries under-measure the most `g`-loaded male-favoring content.

### H2 - Domain Plus Design Hypothesis

There is no large stable battery-independent `g` gap; the literature mainly disagrees because domain differences are real but composites move with timing, weighting, and battery construction.

### H3 - Schooling / Practice Hypothesis

Female advantages on coding-like or clerical processing-speed tasks are materially driven by literacy, reading-writing fluency, classroom behavior, and related practice.

### H4 - Family / Background Confounding Hypothesis

Part of the observed sex pattern is inflated by family-level or environment-level confounding rather than reflecting within-family differences.

### H5 - Outcome Overreach Hypothesis

Popular claims about productivity, success, or civilizational relevance are much stronger than the data justify; most of the leap from subtest gaps to life outcomes is over-inference.

### H6 - Selection / Sample Composition Hypothesis

Some strong reported sex gaps are products of nonrepresentative samples, attrition, or cohort composition rather than stable population structure.

---

## Primary Estimands

To avoid drifting between incompatible summaries, the project should keep using the same small set of estimands.

1. **Subtest mean gap:** standardized mean difference by sex on each subtest or domain score
2. **Within-family subtest gap:** sex coefficient from sibling fixed-effects models
3. **Composite sensitivity:** movement in overall gap under prespecified reweighting rules
4. **Education mediation:** attenuation of sex coefficients after schooling / literacy controls
5. **Outcome increment:** added predictive value of subtest profile after broader controls
6. **Heterogeneity:** whether gaps change by cohort, country, education level, or sample design
7. **Variance ratio:** male variance divided by female variance by domain or composite
8. **Tail ratio:** sex representation in upper and lower tails under prespecified cutoffs

Each estimand must be frozen at the formula level in the Stage -1 protocol, not only named in prose. [INFERENCE]

---

## DOE Overview

The right structure is not one giant model. It is a staged DOE where each experiment is meant to harden or soften specific nodes.

### Stage 0 - Data Audit and Reproducibility Lock

**Purpose:** make sure every later estimate is reproducible and tied to named variables.

**Local assets:**

- `sources/iq-sex-diff/data/README.md`
- `sources/iq-sex-diff/data/nlsy/nlsy_asvab_variables.tsv`
- `sources/iq-sex-diff/data/piaac/*.csv`
- `sources/iq-sex-diff/data/icar/sapaICARData18aug2010thru20may2013.csv`

**Deliverables:**

1. a per-dataset variable manifest for sex, family ID, subtests, education, and outcomes
2. row counts and missingness summaries
3. a single harmonized naming table for domain groups:
   - verbal
   - spatial / mechanical
   - clerical processing speed
   - math / quantitative
4. a power / precision table for each primary experiment
5. an attrition / selection audit for `NLSY79`, `NLSY97`, and `PIAAC`
6. a cross-dataset construct-alignment table with confidence grades:
   - high
   - medium
   - low
7. a frozen analysis script or dated protocol that contains the exact composite weights, covariate blocks, and decision thresholds
8. a dataset card for each source that freezes scoring, weights, plausible-value handling, and whether the resulting estimate is population-weighted or sample-descriptive

**Why first:** every later causal claim depends on consistent variable boundaries.

---

## Stage 0.5 - Measurement Invariance and DIF

**Purpose:** stop raw score gaps from being mistaken for latent-trait gaps when the test is not functioning equivalently across sexes.

**Deliverables:**

1. configural, metric, and scalar invariance checks where feasible
2. item-level DIF checks where feasible
3. sex-gap estimates under three scoring regimes when possible:
   - raw scores
   - full latent scoring
   - invariant-item subset scoring

**Decision rule:**

- if the sex gap changes materially across these scoring regimes, the domain is flagged as measurement-sensitive and downstream causal claims are downgraded
- provisional default for "materially": gap shift greater than `0.10` SD or greater than `25%` of the primary-spec estimate

**Why here:** this is a gate, not a side note. If the measurement layer is unstable, every later model inherits the defect. [INFERENCE]

---

## Experiment 1 - ICAR Open-Data Decomposition

**Dataset:** `ICAR / SAPA`

**Question:** in an open multi-domain battery, how much can the overall sex gap be moved by changing domain weights?

**Primary hypotheses tested:** `H2`, `H6`

**Design:**

1. score `VR`, `LN`, `MR`, and `R3D` domains
2. estimate sex gaps by domain
3. construct prespecified composites:
   - equal weights
   - verbal-heavy
   - matrix-heavy
   - spatial-heavy
4. measure how much the composite sex gap moves under reweighting

**What hardens H2:**

- large movement in the composite gap under the frozen weight grid while domain gaps themselves remain stable

**What softens H2:**

- a stable same-direction gap across all reasonable weightings

**Guardrail:**

- report the full distribution of sex gaps across the prespecified composite grid, not only the most rhetorically useful composite

**Known limit:** convenience sample means this cannot settle population-level claims by itself.

---

## Experiment 2 - NLSY79 Opposite-Sex Sibling Fixed Effects

**Dataset:** `NLSY79`

**Question:** within the same family, do the spatial/mechanical and clerical-speed patterns persist?

**Primary hypotheses tested:** `H2`, `H3`, `H4`

**Design:**

1. identify opposite-sex sibling pairs using household / family structure variables
2. estimate sibling fixed-effects models for key ASVAB subtests:
   - `Coding Speed`
   - `Numerical Operations`
   - `Word Knowledge`
   - `Paragraph Comprehension`
   - `Auto & Shop`
   - `Mechanical Comprehension`
   - `Math Knowledge`
   - `Arithmetic Reasoning`
3. compare raw sex gaps to within-family sex gaps

**Interpretation:**

- if the gaps persist strongly within family, **shared-family** confounding weakens
- if they shrink sharply within family, `H4` hardens

**Important limit:**

- sibling FE does **not** eliminate sex-differentiated treatment within the same household, birth-order effects, or age-at-test artifacts

**Design upgrade:**

- restrict primary analysis to tightly spaced opposite-sex siblings where feasible
- include age-at-test and birth-order adjustments in the fixed-effects design
- freeze the pair-construction algorithm in Stage 0A, including kinship definition, maximum age gap, test-stage window, and tie-break rules for families with multiple eligible pairs

**Why this is the keystone experiment:**

- it is the best immediate attack on the "this is all SES / upbringing" story using public-use data already on disk

---

## Experiment 3 - NLSY79 Mediation by Schooling and Practice Proxies

**Dataset:** `NLSY79`

**Question:** do schooling-linked proxies explain more of the female clerical-speed advantage than they explain male mechanical advantages?

**Primary hypotheses tested:** `H3`

**Design:**

Start from the sibling and full-sample models, then add controls in blocks:

1. age and race / ethnicity
2. clearly pre-test schooling exposure variables
3. literacy / coursework / school-behavior proxies that can be defended as channel measures rather than post-treatment colliders

**Bad-control warning:**

- grades, school track, and later education can themselves be downstream consequences of ability
- they should therefore be treated as DAG-sensitive mediation variables, not automatically as "safe controls"

**Interpretation rule:**

- the default result here is **descriptive attenuation**
- it should only be upgraded to **causal mediation** if temporal ordering and DAG assumptions are made explicit and defended

**Prediction unique to H3:**

- clerical-speed gaps should attenuate more under schooling / literacy controls than mechanical gaps do

**What would count as a serious negative result for H3:**

- coding-speed and numerical-operations gaps remain almost unchanged while mechanical and verbal gaps attenuate similarly

---

## Experiment 4 - NLSY97 CAT-ASVAB Cohort Replication

**Dataset:** `NLSY97`

**Question:** did the sex pattern change in the newer cohort under CAT-ASVAB and a later schooling environment?

**Primary hypotheses tested:** `H2`, `H3`, `H6`

**Design:**

1. identify matched CAT-ASVAB constructs using `nlsy_asvab_variables.tsv`
2. estimate comparable subtest gaps
3. compare the direction and magnitude to `NLSY79`
4. compare variance ratios and tail ratios, not only means

**Interpretation:**

- stability across cohorts hardens the "real domain difference" part of `H2`
- systematic drift in clerical or verbal-like tasks hardens `H3`
- strong instability everywhere suggests more measurement or sample dependence than the current literature admits

---

## Experiment 5 - PIAAC Education-Stratified Cross-Country Analysis

**Dataset:** `PIAAC` main files

**Question:** how much do sex gaps change within education strata and across countries?

**Primary hypotheses tested:** `H3`, `H6`, partially `H5`

**Design:**

1. use the public-use main files already local
2. estimate sex gaps on:
   - literacy plausible values
   - numeracy plausible values
   - problem solving plausible values where available
3. stratify by education and age
4. compare across countries

**Construct-alignment warning:**

- `PIAAC` constructs are not automatically equivalent to `ASVAB` or `ICAR` constructs just because they share a label like "numeracy" or "verbal"
- cross-dataset comparisons should therefore be limited to mappings rated `high` or `medium` in the Stage 0 alignment table

**What hardens schooling / practice explanations:**

- sex gaps that move materially within education strata or differ strongly across countries with different schooling and labor patterns

**What softens them:**

- highly stable patterns across education strata and countries

**Important limit:**

- PIAAC is better for adult skill structure and heterogeneity than for spatial or clerical-speed decomposition
- country comparisons remain provisional unless translation / adaptation artifacts are checked through released OECD scaling evidence or invariant-item analysis

---

## Experiment 6 - PIAAC Process / Log Files

**Dataset:** `PIAAC` process data once downloaded

**Question:** are observed sex differences driven more by accuracy, response process, or time-on-task behavior?

**Primary hypotheses tested:** `H3`, `H2`

**Design:**

1. link log/process files to main files by respondent ID
2. analyze:
   - time on task
   - first action latency
   - interaction counts
   - completion patterns
3. compare process differences to score differences

**Why this matters:**

- it directly attacks the conflation of "scored higher" with "processed faster in a general sense"

**Status:** blocked only by missing local log files, not by conceptual ambiguity.

---

## Experiment 7 - Outcome-Relevance Models

**Datasets:** `NLSY79`, `NLSY97`, `PIAAC`

**Question:** does clerical processing speed or mechanical / spatial performance have meaningful incremental value for adult outcomes?

**Primary hypotheses tested:** `H5`

**Outcomes:**

- education
- occupational complexity
- earnings / income
- technical occupation entry

**Design:**

1. first estimate bivariate outcome gradients by subtest
2. then add controls:
   - broader ability profile
   - education
   - family background
   - demographics
3. check whether clerical-speed effects survive

**Primary-outcome rule:**

- designate one primary outcome per dataset before analysis
- treat the remaining outcomes as secondary and report multiplicity correction

**Reporting firewall:**

- draft the write-up for Experiments 1 through 6 before running Experiment 7, so outcome knowledge does not leak backward into the interpretation of the psychometric stages

**Decision rule:**

- if clerical processing speed loses most of its predictive power after controls, stop treating it as a proxy for real-world productivity

---

## Prespecified Decision Tree

### If Experiment 2 shows strong within-family persistence

Then stop saying the whole pattern is "just between-family SES" or "just shared-family background."

### If Experiment 3 shows sharp attenuation for clerical-speed but not mechanical tasks

Then harden the schooling / practice channel specifically for the female clerical advantage.

### If Experiment 4 shows the same domain pattern in both cohorts

Then harden the claim that the pattern is not just one-battery noise.

### If Experiment 5 shows major cross-country or education-strata drift

Then harden the environment / practice channel and soften any universalist biological claim.

### If Experiment 7 shows weak incremental outcome value

Then separate psychometric sex differences from popular claims about life success.

---

## What Would Actually Count As "Root Cause"

Because sex itself is not manipulable, the project should use "root cause" carefully.

For this project, a node counts as a root cause only if:

1. it survives controls and more restrictive designs
2. it predicts a footprint that competing nodes do not
3. it replicates across at least two datasets or design families
4. it changes the interpretation of the popular headline claim

This means the final answer may be plural:

- **root cause of literature disagreement:** battery design plus task composition
- **root cause of male mechanical advantage:** likely real domain difference, not fully explained by timing
- **root cause of female clerical-speed advantage:** likely mixed schooling / practice plus possibly fine-motor channel
- **root cause of overclaim in public debate:** criterion-validity slippage from subtest gaps to life outcomes

That is not evasion. It is a more causally correct answer shape. [INFERENCE]

---

## Stop Rules

To stay aligned with epistemic reality, the project should stop escalating a claim when:

1. the effect disappears under the first serious design improvement
2. the sign flips across reasonable model choices
3. the claim depends on a composite whose weights were chosen after looking at the gaps
4. the outcome interpretation is stronger than the criterion-validity evidence

---

## Numeric Decision Thresholds

These are provisional default thresholds to be frozen in the Stage -1 protocol unless the Stage 0 power audit forces a change.

1. **Strong within-family persistence:** within-family coefficient is at least `50%` of the raw sex-gap magnitude and the `95%` CI excludes zero
2. **Sharp attenuation:** schooling / practice block reduces the clerical-speed coefficient by at least `40%` while the comparable mechanical coefficient attenuates by less than `20%`
3. **Large composite movement:** composite sex gap moves by at least `0.15` SD across the frozen reweighting grid
4. **Weak outcome increment:** partial `R² <= 0.005` or standardized coefficient `< 0.05` after the full control set, with CI including zero
5. **Meaningful heterogeneity:** cohort / country difference in the sex-gap estimate is at least `0.10` SD and the uncertainty interval excludes zero
6. **No meaningful effect:** may only be claimed if the experiment's minimum detectable effect is smaller than the smallest effect size of interest or an equivalence-style test passes

These are not sacred constants. But they are better than verbal thresholds like "strong" and "sharp," which invite motivated reinterpretation. [INFERENCE]

---

## Execution Order

1. finalize dataset manifests and harmonized variable groups
2. run `ICAR` decomposition as the fast sandbox
3. run `NLSY79` sibling fixed effects as the keystone causal test
4. run `NLSY97` cohort replication
5. run `PIAAC` education-stratified cross-country analysis
6. add `PIAAC` process files when local
7. run outcome-relevance models last, not first

The next open node after the current `PIAAC` tranche is now frozen more explicitly in `research/iq-sex-differences-next-node-validation.md`: decide whether the `NLSY97` quantitative sign flip is a real school-exit sorting effect or a battery-local measurement / process artifact before broadening the verbal story again. [INFERENCE]

This order is important. If we start with outcomes or ideology-heavy synthesis first, we will overfit stories before we know what is even stable at the measurement level. [INFERENCE]

---

## Current Best Provisional Position

### What is already fairly hard

- there is no settled battery-independent sex difference in overall `g`
- spatial / mechanical male advantages are more stable than the global `g` claim
- clerical processing-speed female advantages are more stable than the global `g` claim
- test design and composite weighting matter materially

### What is still soft

- how much of the clerical-speed pattern is schooling / practice versus fine-motor / physiological channel
- whether any of these gaps have large independent real-world payoff
- how much sample composition explains stronger historical claims

---

## Model-Guide Review Summary

This plan was adversarially reviewed after drafting using the `model-guide`
workflow.

Models actually used:

- `Gemini 3.1 Pro` on two prompts: causal-identification critique and execution critique
- `GPT-5.3 Instant` on one causal-identification critique
- `GPT-5.4` on two prompts: causal-identification critique and execution critique

An earlier `llmx` call to `gpt-5-pro` stalled because that was the wrong local
model name. The usable OpenAI review came from `gpt-5.4`. A `Claude Sonnet 4.6`
review call was also launched but did not return usable output before synthesis.
[INFERENCE]

Convergent criticisms that changed the DOE:

1. add a measurement-invariance / DIF gate before interpreting sex gaps
2. add variance and tail estimands, not just means
3. narrow the sibling-FE interpretation to shared-family confounding
4. freeze the composite grid, covariate blocks, and decision thresholds before analysis
5. add explicit construct-alignment checks across `ASVAB`, `ICAR`, and `PIAAC`
6. replace verbal decision rules with numeric thresholds
7. add a reporting firewall so outcome analyses do not retroactively contaminate measurement-stage interpretation
8. add a Stage 0A scoring / weights / plausible-values lock
9. split descriptive attenuation from true causal mediation language

These changes were incorporated directly into the plan above rather than left as separate review notes. [INFERENCE]

---

## Causal Check

**Observation:** the literature disagrees most at the composite `g` layer, but agrees more at the domain layer. [SOURCE: `research/iq-sex-differences-verification.md`; `research/iq-sex-differences-causal-graph.md`]

**Most likely cause (70%):** different upstream nodes explain different parts of the pattern, with battery design explaining much of the literature disagreement and schooling / practice likely explaining part of the female clerical-speed advantage. [INFERENCE]

**Top alternative (20%):** there is a true stable male `g` advantage, and most of the disagreement is downstream noise or politically loaded measurement design. This is weaker because it does not naturally explain the repeated null and female-tilting findings across multiple batteries. [INFERENCE]

**Falsifier:** if sibling, cohort, and cross-country analyses all point in the same male-favoring direction for both domain scores and balanced composites, with little mediation by education or task format, then the current mixed-node explanation should be downgraded. [INFERENCE]

**Decision impact:** proceed with node-by-node DOE rather than argument by blog post, ideology, or one favored battery. [INFERENCE]
