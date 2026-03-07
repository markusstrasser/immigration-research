# IQ Sex Differences - Master DAG

**Date:** 2026-03-06  
**Purpose:** one inspectable ASCII causal graph for the current project state.

This is the repo's current best DAG-style compression of the project.

It is **not** a claim that every arrow is proven. It is a working causal structure used to decide:

1. what causes what
2. which controls are admissible
3. which remaining datasets would actually kill live nodes

Companion files:

- `research/iq-sex-differences-decisive-causal-tree.md`
- `research/iq-sex-differences-current-position.md`
- `research/iq-sex-differences-node-table.md`
- `research/iq-sex-differences-next-level-research-plan.md`
- `research/iq-sex-differences-mediator-design.md`
- `research/iq-sex-differences-analysis-protocol.md`

---

## Conventions

- `-->` = supported enough to use operationally
- `-?>` = plausible / open / partially identified
- `[obs]` = observed surface
- `[lat]` = latent or partially latent construct
- `[sel]` = selection / analyzability node

This graph is forced to be acyclic by using time slices.

So when a process really feeds back over years, read it as:

- `t0 -> t1 -> t2`

rather than as one instantaneous loop. [INFERENCE]

---

## 1. Master Graph

```text
PRE-TREATMENT / CONTEXT
-----------------------

[Sex]
[Family SES]
[Parent education]
[Family structure]
[Race / ethnicity]
[Cohort / country / policy regime]
[School context / institution quality]
[Test design / score construction]


EARLY CHILDHOOD / SCHOOL ENTRY
------------------------------

[Family SES] ------------------------------+
[Parent education] ------------------------+--------------------+
[Family structure] ------------------------+                    |
[Race / ethnicity] ------------------------+                    |
[Cohort / country / policy regime] --------+                    |
                                                                v
                                                      [Early environment / practice]
                                                                |
                                                                v
[Sex] -?> [Latent verbal profile t0] ---------------------------+-------> [Observed reading / verbal surface t0] [obs]
   |                                                            |                 ^
   |                                                            |                 |
   |                                                            |                 |
   +--> [Latent spatial / mechanical profile t0] ---------------+                 |
   |                                                                              |
   +-?> [Latent broad quantitative profile t0] ----------------------------------+-----> [Observed math / quantitative surface t0] [obs]
   |                                                                              ^                 ^
   +-?> [Behavior / compliance / engagement t0] ---------------------------------+                 |
                                                                                                    |
[Test design / score construction] ---------------------------------------------------------------+
[Sample selection / analyzability t0] [sel] ------------------------------------------------------+


EARLY SCHOOL EMERGENCE
----------------------

[Observed reading / verbal surface t0] [obs] ------------------------------------+
[Observed math / quantitative surface t0] [obs] ---------------------------------+-----> [Relative child math vs verbal geometry]
[School context / institution quality] ------------------------------------------+
[Sex] ---------------------------------------------------------------------------+
                                                                                 |
                                                                                 v
                                                                 [Early school divergence t1]
                                                                                 |
                                                                                 v
                                                           [Observed broad school math t1] [obs]


LATE SCHOOL / PIPELINE
----------------------

[Sex] ---------------------------------------+
[Family SES] --------------------------------+-----------------------------+
[Parent education] --------------------------+                             |
[Family structure] --------------------------+                             |
[Race / ethnicity] --------------------------+                             |
[School context / institution quality] ------+                             |
[Early school divergence t1] ----------------+                             |
                                                                            v
                                                          [School behavior / compliance / homework]
                                                                            |
                                                                            +----------------------+
                                                                            |                      |
                                                                            v                      v
                                                           [School evaluation / grades / recs]   [School-knowledge accumulation]
                                                                            |                      |
                                                                            |                      |
                                                                            v                      v
                                              [Transcript exposure / course ladder / credits]   [Observed school-knowledge test] [obs]
                                                                            |                      ^
                                                                            |                      |
                                                                            +----------+           |
                                                                                       |           |
                                                                                       v           |
                                                              [Track selection / advanced participation]
                                                                                       |           |
                                                                                       |           |
                                         [Latent spatial / mechanical / quantitative profile t1] --+
                                                                                       |
                                                                                       +-----------> [Observed applied / reasoning test] [obs]
                                                                                                      ^                    ^
                                                                                                      |                    |
[Test design / score construction] ------------------------------------------------------------------+                    |
[Sample selection / analyzability late school] [sel] ----------------------------------------------------------------------+


TRANSITION / ADULTHOOD
----------------------

[School evaluation / grades / recs] -----------------------+
[Transcript exposure / course ladder / credits] -----------+-----------------------+
[Track selection / advanced participation] ----------------+                       |
[Observed applied / reasoning test] [obs] -----------------+                       |
[Observed school-knowledge test] [obs] --------------------+                       |
[Sex] -----------------------------------------------------+                       |
[Family SES / background] ---------------------------------+                       |
                                                                                   v
                                                             [Field / major / occupation / adult use]
                                                                                   |
                                                                                   v
                                                         [Adult accumulation / use-dependent amplification]
                                                                                   |
                                                                                   v
                                                                       [Observed adult numeracy] [obs]
                                                                                   |
                                                                                   v
                                                                          [Attainment / later outcomes]
```

---

## 2. Score-Generation Subgraph

This is the most important subgraph in the repo.

It explains why one latent surface can generate different observed sex gaps.

```text
[Latent domain ability at time t]
        |
        +------------------------------------+
                                             |
                                             v
                                [Observed test score / subtest score] [obs]
                                             ^
                                             |
[Test design / item family / timing /
 adaptivity / scoring / DIF / interface] ----+
                                             ^
                                             |
[Behavior / compliance / effort at test] ----+
                                             ^
                                             |
[Sample selection / analyzability] [sel] ----+
```

Operational meaning:

1. a sex gap in an observed score can come from the latent domain
2. or from the measurement surface
3. or from test-session behavior/process
4. or from who gets observed / linked / analyzed

[SOURCE: `research/iq-sex-differences-pisa2018-dif-leaveout.md`; `research/iq-sex-differences-nlsy97-stage-a.md`; `research/iq-sex-differences-analysis-protocol.md`]

---

## 3. Outcome / Mediation Subgraph

This is the outcome branch that the repo kept overreading before the mediator memo.

```text
[Sex]
  |
  +------------------------------> [Attainment / later outcomes]
  |
  +--> [School behavior / compliance]
  |          |
  |          +--> [School evaluation / grades / recs] --------+
  |          |                                                |
  |          +--> [Observed tested surface] [obs] --------+   |
  |          |                                            |   |
  |          +--> [Transcript exposure / course ladder] --+   |
  |                                                       |   |
  +-------------------------------------------------------+---+

[Family SES / parent ed / family structure / race] ------> all downstream school nodes and attainment
```

Interpretation:

1. total effect of `sex -> attainment` can use background-only adjustment
2. once grades, tests, or transcript nodes enter the model, the estimand changes
3. attenuation after adding those nodes is descriptive channel decomposition, not automatic mediation identification

[SOURCE: `research/iq-sex-differences-mediator-design.md`]

---

## 4. What Causes What

## Nodes that clearly cause a lot downstream

### `Sex`

Current repo read:

- clearly upstream of every observed sex difference by definition
- likely acts through multiple channels, not one
- strongest supported downstream channels are:
  - some domain differences
  - school-evaluation divergence
  - track/selection divergence
  - adult-use divergence

[SOURCE: `research/iq-sex-differences-current-position.md`; `research/iq-sex-differences-decisive-causal-tree.md`]

### `Family SES / parent education / family structure / race`

These are pre-treatment background causes for:

- school behavior
- grades / evaluation
- tested surfaces
- transcript exposure
- later attainment

These are ordinary background controls, not descendants. [SOURCE: `research/iq-sex-differences-mediator-design.md`]

### `School context / institution quality`

Causes:

- school behavior/compliance
- grades / evaluation / recommendations
- course offerings and ladder access
- school-knowledge accumulation

[INFERENCE]

### `Test design / score construction`

Causes:

- the observed score surface
- which item families dominate
- whether timing/adaptivity/process effects matter

It does **not** cause latent ability.

[SOURCE: `research/iq-sex-differences-pisa2018-dif-leaveout.md`; `research/iq-sex-differences-pisa2018-framework-proxy.md`; `research/iq-sex-differences-nlsy97-stage-a.md`]

## Nodes that sit in the middle of the pipeline

### `Early school divergence`

Current read:

- likely real
- not reducible to high-school transcript or advanced-track stories alone

Causes later differences in:

- broad school math
- later track selection
- later school-tested surfaces

[SOURCE: `research/iq-sex-differences-early-school-age-matched-alignment.md`; `research/iq-sex-differences-frontier-literature-audit.md`]

### `School behavior / compliance`

Likely causes:

- grades / evaluation
- some tested surfaces
- transcript exposure indirectly

Current repo read:

- this node is real
- but currently measured behavior blocks do **not** explain away the school wedge

[SOURCE: `research/iq-sex-differences-school-wedge-mechanism-triage.md`; `research/iq-sex-differences-nlsy97-behavior-evaluation-pass.md`]

### `School evaluation / grades / recommendations`

Causes or predicts:

- later attainment
- some track selection

Current repo read:

- this is the most stable female-leaning late-school family across cohorts

[SOURCE: `research/iq-sex-differences-school-wedge-synthesis.md`]

### `Transcript exposure / course ladder / credits`

Causes or predicts:

- advanced-track participation
- some later outcomes

Current repo read:

- this family is less stable than the evaluation family
- transcript quantity and transcript grade should not be collapsed

[SOURCE: `research/iq-sex-differences-school-wedge-synthesis.md`; `research/iq-sex-differences-nels-wedge-first-pass.md`]

### `Track selection / advanced participation`

Causes:

- advanced-math observed surfaces
- some later field/occupation sorting

Current repo read:

- broad-population school math and advanced-track math are different causal objects

[SOURCE: `research/iq-sex-differences-timss-frontier.md`; `research/iq-sex-differences-timss-cognitive-split.md`; `research/iq-sex-differences-decisive-causal-tree.md`]

### `Adult accumulation / use-dependent amplification`

Causes:

- part of adult numeracy

Current repo read:

- likely amplifier, not sole origin

[SOURCE: `research/iq-sex-differences-piaac-age-occupation.md`; `research/iq-sex-differences-decisive-causal-tree.md`]

## Nodes that are mostly open

### `Latent broad quantitative profile`

This is still open because observed quantitative surfaces split too much by battery.

[SOURCE: `research/iq-sex-differences-current-position.md`; `research/iq-sex-differences-verification.md`]

### `Residual battery-invariant general ability gap`

This is the weakest live node.

If it exists, it should cause consistent residual differences across balanced, process-aware, measurement-aware surfaces.

Current repo read:

- not established
- still possible in a narrower form

[SOURCE: `research/iq-sex-differences-decisive-causal-tree.md`; `research/iq-sex-differences-current-position.md`]

---

## 5. What Not To Control For

If treatment is `Sex`, do **not** casually control for:

- grades
- GPA
- recommendations
- transcript quantity
- course ladder
- homework / belonging / encouragement
- items completed
- posterior variance
- test-session effort/process descendants

These are downstream nodes for the main sex-effect question.

[SOURCE: `research/iq-sex-differences-mediator-design.md`; `research/iq-sex-differences-nlsy97-course-dag-robustness.md`]

---

## 6. Current Bottom Line

The repo's current full graph says:

1. `Sex` does not map straight to one battery-invariant `IQ` object.
2. It maps into a pipeline:
   - early divergence
   - measurement surface
   - school evaluation
   - transcript exposure
   - track selection
   - adult accumulation
3. Different datasets pick up different slices of that pipeline.
4. The strongest stable late-school female-leaning family is `evaluation`.
5. The strongest stable male-leaning families are `spatial/mechanical`, `adult numeracy`, and `advanced-track / reasoning-heavy` math.
6. The residual battery-invariant `g` node is still open, not settled.

[SOURCE: `research/iq-sex-differences-current-position.md`; `research/iq-sex-differences-school-wedge-synthesis.md`; `research/iq-sex-differences-decisive-causal-tree.md`]
