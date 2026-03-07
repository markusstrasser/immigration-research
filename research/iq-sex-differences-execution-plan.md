# IQ Sex Differences - Execution Plan

**Date:** 2026-03-06
**Purpose:** convert the current causal tree into an execution sequence that can reduce uncertainty quickly and decisively.

This is the operational companion to:

- `research/iq-sex-differences-current-position.md`
- `research/iq-sex-differences-decisive-causal-tree.md`
- `research/iq-sex-differences-node-table.md`
- `research/iq-sex-differences-analysis-protocol.md`
- `research/iq-sex-differences-master-plan.md`
- `research/iq-sex-differences-next-level-research-plan.md`
- `research/iq-sex-differences-mediator-design.md`
- `research/iq-sex-differences-restricted-data-plan.md`
- `research/iq-sex-differences-addhealth-ahaa-application-scope.md`

For the full end-to-end roadmap, literature tracks, validation ladder, and completion criteria, read `research/iq-sex-differences-master-plan.md` first. This file remains the shorter execution-order companion.

---

## Objective

The next tranche should answer one narrow question:

> after separating measurement surface, school pipeline, and track selection, is there any stable residual that still looks like a battery-invariant sex difference in general ability?

That means the plan is **not**:

1. run more generic pooled regressions
2. keep re-estimating the same composite on new samples
3. argue from one battery to all batteries

The plan **is**:

1. kill or harden the highest-value nodes in order
2. use the smallest number of analyses that create qualitatively different footprints
3. keep destructive and downstream controls out of the primary specs

---

## Current Node Ranking

From the current project state, the active nodes are:

1. `MeasurementSurface`
2. `SchoolPipeline`
3. `EarlySchoolEmergence`
4. `TrackSelection`
5. `AdultAccumulation`
6. residual `LatentGeneralGap`

Current probabilities are in `research/iq-sex-differences-decisive-causal-tree.md`.

Operational consequence:

- attack Nodes `1` and `2` first
- make Node `3` explicit before overloading transcript and track explanations
- only then attack Node `4`
- postpone stronger claims about Node `6` until the earlier nodes are materially reduced

---

## Execution Sequence

## Stage 1 - `PISA 2018` Item-Family And Timing Decomposition

**Priority:** highest
**Node attacked:** `MeasurementSurface`, then `SchoolPipeline`
**Why first:** `PISA 2018` is already local, public, large, item-level, and process-rich.

**Status:** raw item/process pass, framework-proxy pass, face-valid item audit, first DIF-style conditioning pass, the contamination-aware leave-out sensitivity pass, the first process-style nuisance prototype, and the first direct response-time DIF pilot are now executed in `research/iq-sex-differences-pisa2018-item-split.md`, `research/iq-sex-differences-pisa2018-framework-proxy.md`, `research/iq-sex-differences-item-face-validity-audit.md`, `research/iq-sex-differences-pisa2018-dif-proxy.md`, `research/iq-sex-differences-pisa2018-dif-leaveout.md`, `research/iq-sex-differences-pisa2018-process-nuisance.md`, and `research/iq-sex-differences-pisa2018-time-dif-pilot.md`. Current read: broad female-slower timing exists on the local `PISA` surface, but it does not line up tightly with the localized male score-residual family ordering. So the next serious measurement move is a formal process-data rescoring / response-time DIF method, or a shift back to the restricted transcript/process frontier.

### Questions

1. Do female-tilting math surfaces concentrate in school-knowledge-heavy item families?
2. Do applied / reasoning-heavy or high-friction process items tilt differently?
3. Do timing, actions, or revisit patterns explain part of the apparent surface split?
4. Does the residual family ordering survive once the matching score excludes the target items or target family?

### Primary estimands

1. sex gap on `PV1MATH` to `PV10MATH`
2. sex gap on item-family subscores
3. sex gap on timing / actions / revisit summaries
4. sex coefficient on item response under item fixed effects and item-family interactions

### Core methods

1. weighted descriptive gaps with replicate-weight variance
2. item-family decomposition
3. multilevel logistic or linear probability item models with item fixed effects
4. leave-item-out or leave-content-family-out matching-score reconstruction
5. rapid-guess / response-time sensitivity or exclusion screen
6. optional anchor-item or iterative-purification DIF screen on the highest-value item clusters

### Success criteria

1. if the residual `space_shape` ordering survives contamination-free matching, Node `1` hardens materially
2. if timing / action or rapid-guess sensitivity materially compresses the residual ordering, the active mechanism shifts from content-family to process burden
3. if all residual item families move together once matching contamination is removed, Node `1` softens and latent-domain explanations strengthen

### Output artifacts

1. `research/iq-sex-differences-pisa2018-item-split.md`
2. `research/iq-sex-differences-pisa2018-framework-proxy.md`
3. `research/iq-sex-differences-item-face-validity-audit.md`
4. `research/iq-sex-differences-pisa2018-dif-proxy.md`
5. `sources/iq-sex-diff/data/pisa/pisa2018_item_family_gaps.tsv`
6. `sources/iq-sex-diff/data/pisa/pisa2018_process_gaps.tsv`
7. `sources/iq-sex-diff/data/pisa/pisa2018_item_models.tsv`
8. `sources/iq-sex-diff/data/pisa/pisa2018_item_dif_proxy.tsv`
9. `sources/iq-sex-diff/data/pisa/pisa2018_dif_content_summary.tsv`
10. `sources/iq-sex-diff/data/pisa/pisa2018_dif_context_summary.tsv`
11. `sources/iq-sex-diff/data/pisa/pisa2018_dif_anchor_candidates.tsv`

### Stop rule

Do not claim formal DIF from the current `PISA` results, but the residual family ordering can now be used operationally because it survives focal-item and focal-family exclusion.

---

## Stage 2 - Early-School Emergence Pass

**Priority:** highest
**Node attacked:** `EarlySchoolEmergence`
**Why second:** recent literature says some broad school-math divergence may open within the first years of schooling, and the repo already has local early-school datasets staged.

**Status:** the original three first-pass cohorts now exist locally, the first reading-anchor pass is done, the age-matched bridge is done, `PSID CDS` now adds a family-linked public child panel pointing the same way on the aligned `math versus reading` surface, and the multi-anchor plus rank-based child bridge passes are now executed in `research/iq-sex-differences-child-bridge-multi-anchor.md` and `research/iq-sex-differences-child-bridge-rank-sensitivity.md`. Current read: the public child branch is no longer reading-only and no longer obviously a raw-scale artifact; `PPVT` alone is the weak anchor. The remaining early-school work is now publication-grade psychometric refinement rather than another public cohort hunt.

### Datasets

1. `ECLS-K`
2. `ECLS-K:2011`
3. `NLSCYA`
4. `PSID CDS`

### Questions

1. Is the broad math gap near zero at entry and then male-favoring after the first school years?
2. Does early-school growth look different from the later `school-knowledge / transcript / labels` family now visible in `NLSY97` and `HSLS`?
3. Is the early-school surface broad math, or does it already show content-family splitting?
4. Does the child-bridge sign survive across reading, vocabulary/language, verbal composites, and rank-based residualization?

### Primary estimands

1. sex gap in early math at entry wave
2. sex gap in early math at later elementary waves
3. within-child or repeated-wave change in the sex gap across the first school years
4. early math versus early reading profile where the battery allows it

### Core methods

1. repeated-wave weighted descriptive gaps
2. cohort-comparable scaling checks
3. growth or difference models with frozen sign conventions
4. sensitivity to sample analyzability and school-entry age
5. multi-anchor bridge sensitivity

### Success criteria

1. near-zero or female-leaning entry plus early male widening hardens Node `3`
2. stable male lean on both `ECLS` cohorts but weaker / later lean on raw `NLSCYA` that collapses under multiple anchors points to score-family mismatch rather than killing Node `3`
3. if the sign survives only under one anchor family, the child bridge becomes provisional rather than hardened
4. no meaningful widening across aligned child score families weakens the need for a separate early-school node

### Output artifacts

1. `research/iq-sex-differences-nlscya-early-school-first-pass.md`
2. `research/iq-sex-differences-eclsk2011-early-school-first-pass.md`
3. `research/iq-sex-differences-eclsk-early-school-first-pass.md`
4. `research/iq-sex-differences-early-school-score-alignment.md`
5. `research/iq-sex-differences-early-school-age-matched-alignment.md`
6. `research/iq-sex-differences-psid-cds-first-pass.md`

### Stop rule

Do not let adolescent transcript or advanced-track stories absorb early broad-school divergence until the bridge survives more than one anchor family.

---

## Stage 3 - Deep `NLSY97` Transcript Payload Pass

**Priority:** highest
**Node attacked:** `SchoolPipeline`
**Why third:** this is the cohort that generated the anomaly, and current evidence says the anomaly is localized, but it should now be interpreted after the early-school node is separated out.
**Status:** the first deep transcript pass is now executed in `research/iq-sex-differences-nlsy97-transcript-deep-pass.md`, the first explicit DAG / robustness follow-up is now executed in `research/iq-sex-differences-nlsy97-course-dag-robustness.md`, the first pre-test behavior / climate follow-up is now executed in `research/iq-sex-differences-nlsy97-behavior-evaluation-pass.md`, the first external `ELS` replication is now executed in `research/iq-sex-differences-els-wedge-first-pass.md`, the first `HSLS` refinement is now executed in `research/iq-sex-differences-hsls-wedge-refinement.md`, the first external `NELS` replication is now executed in `research/iq-sex-differences-nels-wedge-first-pass.md`, the first cross-dataset late-school synthesis is now executed in `research/iq-sex-differences-school-wedge-synthesis.md`, the first family-level mechanism triage is now executed in `research/iq-sex-differences-school-wedge-mechanism-triage.md`, the first family-linked `PSID TAS` transition extension is now executed in `research/iq-sex-differences-psid-tas-transition-first-pass.md`, the first canonical public-use `Add Health` school-surface pass is now executed in `research/iq-sex-differences-addhealth-school-surface-first-pass.md`, the public `Add Health` family-linkage probe is now executed in `research/iq-sex-differences-addhealth-public-pair-note.md`, the first public `FFCWS` child/transition pass is now executed in `research/iq-sex-differences-ffcws-achievement-first-pass.md`, and the first public-use outcome decomposition is now executed in `research/iq-sex-differences-school-outcome-decomposition.md`. Current read: the wedge survives `PIAT` anchoring plus design, self-reported exposure, and school-offer controls; the first DAG-valid course-exposure pass does not provide a clean positive explanation of the `Math Knowledge` wedge; the first internal `NLSY97` behavior/compliance pass does not materially compress the wedge; public-use `ELS` externally replicates the school-linked split on track and evaluation surfaces even though transcript GPA itself is suppressed; the first `HSLS` mechanism refinement says the obvious homework / belonging / self-efficacy / teacher-climate block does not materially compress the school-linked wedge either; older-cohort `NELS` replicates the tested-math versus evaluation split while also showing that transcript math quantity is much less female-leaning than grades or recognitions; the cross-dataset synthesis now says the evaluation family is the most stable female-leaning family, while tested math is more male/null and track/quantity are less stable; the family-level triage now says the measured behavior / identity / climate / anchor blocks mostly move tested-math surfaces rather than eliminating the evaluation family or the `NLSY97` school-knowledge residual; `PSID TAS` says the GPA-versus-tested-math split extends into a family-linked transition panel; public-use `Add Health` now says the broader school-performance family is not confined to transcript-rich NCES cohorts or `PSID` transition data; the public `Add Health` within-family extension looks blocked in the current files; `FFCWS` says the transition wedge survives in another non-NCES cohort while the child math-versus-verbal geometry remains anchor-sensitive; and the new outcome decomposition says adolescent school/evaluation surfaces absorb a meaningful but partial share of the female later-attainment edge while the early-childhood battery barely moves the later female college-years residual. The next highest-value discriminator is now stronger restricted transcript/process access, a real mediator design, or a cross-cohort synthesis that treats anchor-sensitive child geometry and school-linked transition accumulation as separate objects rather than one wedge.

### Questions

1. Does the female-looking `Math Knowledge` signal stay localized once raw transcript ladder and course payload are unpacked?
2. Do transcript ladder, credits, and GPA move together, or are they different surfaces?
3. Does the grade-test wedge survive within narrower course ladders and transcript-defined exposure sets?

### Primary estimands

1. sex gap by transcript-defined course ladder
2. sex gap by transcript-defined math credits and GPA
3. residual wedge:
   - `transcript_math_gpa ~ female + PIAT + ladder + design block`
   - `PIAT ~ female + transcript_math_gpa + ladder + design block`
   - `MathKnowledge ~ female + PIAT + ladder + design block`

### Core methods

1. transcript-payload parsing and harmonization
2. same-sample specification curve
3. explicit DAG audit before any causal regression:
   - total `sex` effect
   - course-exposure effect
   - behavior / compliance effect
   - evaluation-surface effect
4. sequential wedge decomposition:
   - pre-treatment baseline
   - course-exposure block
   - behavior / compliance block
   - evaluation / grading block
5. post-estimation robustness for any causal OLS worth interpreting
6. subgroup checks by age-at-test and grade-at-test

### Success criteria

1. if `Math Knowledge` and transcript GPA stay female-tilting while `PIAT` / `AR` do not, Node `2` hardens
2. if the wedge mostly collapses inside the behavior / compliance block, the active mechanism shifts away from a pure evaluation story
3. if the wedge survives exposure and school-offer blocks but collapses only in tiny evaluation-heavy subsamples, do not treat that collapse as decisive
4. if the wedge collapses after better transcript alignment or external replication, Node `2` softens materially
5. if a proposed late-school estimate only exists under a bad-control specification, do not promote it into the causal tree

### Output artifacts

1. `research/iq-sex-differences-nlsy97-transcript-deep-pass.md`
2. `research/iq-sex-differences-nlsy97-course-dag-robustness.md`
3. `sources/iq-sex-diff/data/nlsy/nlsy97_transcript_deep_surface_gaps.tsv`
4. `sources/iq-sex-diff/data/nlsy/nlsy97_transcript_deep_models.tsv`
5. `sources/iq-sex-diff/data/nlsy/nlsy97_transcript_deep_transcript_models.tsv`
6. `sources/iq-sex-diff/data/nlsy/nlsy97_transcript_deep_by_mathpipe.tsv`
7. `sources/iq-sex-diff/data/nlsy/nlsy97_course_causal_models.tsv`
8. `sources/iq-sex-diff/data/nlsy/nlsy97_course_causal_sensemakr_*.json`
9. `research/iq-sex-differences-nlsy97-behavior-evaluation-pass.md`
10. `sources/iq-sex-diff/data/nlsy/nlsy97_behavior_*.tsv`

### Stop rule

Do not use grades or transcript variables as nuisance controls in any general-ability claim unless this pass first shows they are not wedge surfaces. Do not interpret any new late-school OLS as causal without a named estimand, a DAG-valid adjustment set, and a robustness read. Once course and pre-test behavior blocks have both failed internally, shift effort to external replication before adding more same-cohort slices.

Do not treat descendant-heavy public `sex -> attainment` decompositions as a substitute for mediator identification. Once the broad public outcome branch has been stress-tested in `Add Health`, `PSID TAS`, and `FFCWS`, the next honest move is the frozen mediator design or restricted transcript/process access rather than more attenuation tables. `Add Health` restricted-use / `AHAA` is the best live path; `HSTS` and `NAEP` are currently preparation targets because the official `NCES` / `ResearchDataGov` path is paused for new applications. The exact `Add Health` request scope, bundle families, and copy-ready project language are now frozen in `research/iq-sex-differences-addhealth-ahaa-application-scope.md`. [SOURCE: `research/iq-sex-differences-mediator-design.md`; `research/iq-sex-differences-restricted-data-plan.md`; `research/iq-sex-differences-addhealth-ahaa-application-scope.md`; https://manager.researchdatagov.org/RDG_User_Guide.pdf]

---

## Stage 4 - `ELS:2002` Grade-Test-Course Wedge Replication

**Priority:** high
**Node attacked:** `SchoolPipeline`
**Why fourth:** `HSLS` could still be idiosyncratic; `ELS` decides whether the wedge is cohort-specific or structural.

### Questions

1. Does the `HSLS` wedge replicate in another U.S. school-to-college panel?
2. Does transcript math GPA remain female-tilting while standardized math does not?
3. Does the wedge survive within comparable course ladders?

### Primary estimands

1. standardized math gap
2. transcript math GPA gap
3. highest-math-ladder conditional gaps
4. residual wedge models aligned to the `HSLS` pass

### Core methods

1. weighted descriptive comparisons
2. ladder-stratified gaps
3. same model family as `HSLS`

### Success criteria

1. if `ELS` replicates `HSLS`, the wedge becomes a real cross-cohort node
2. if `ELS` fails badly while `HSLS` holds, the wedge downgrades from structural to cohort-sensitive

### Output artifacts

1. `research/iq-sex-differences-els-wedge-replication.md`
2. `sources/iq-sex-diff/data/els/els_wedge_overall.tsv`
3. `sources/iq-sex-diff/data/els/els_wedge_by_ladder.tsv`

---

## Stage 5 - Invariant-Item / DIF Pass

**Priority:** high
**Node attacked:** `MeasurementSurface`
**Why fifth:** by this point the likely item families are visible, so invariance work becomes targeted instead of exploratory.

### Datasets

1. `PISA 2018`
2. `ICAR`
3. `NLSY79` / `NLSY97` only if usable item layers can be recovered cleanly

### Questions

1. How much does the gap move under invariant-item rescoring?
2. Are the female-tilting and male-tilting surfaces partly driven by DIF-heavy items?

### Primary estimands

1. raw-score gap
2. latent-score gap
3. invariant-item subset gap

### Core methods

1. multi-group CFA / IRT where feasible
2. item-level DIF screens
3. compare gap movement under frozen thresholds from the protocol

### Success criteria

1. gap shift `> 0.10 SD` or `> 25%` of primary estimate hardens measurement sensitivity
2. stable gaps across scoring regimes soften measurement-surface explanations

### Output artifacts

1. `research/iq-sex-differences-invariance-pass.md`
2. `sources/iq-sex-diff/data/measurement/invariant_gap_compare.tsv`

---

## Stage 6 - Broad-Population Versus Advanced-Track Split

**Priority:** medium-high
**Node attacked:** `TrackSelection`
**Why sixth:** the project already has the descriptive clue from `TIMSS`; now it needs aligned modeling.

### Datasets

1. `HSLS`
2. `ELS`
3. `TIMSS 2019`
4. `TIMSS Advanced 2015`

### Questions

1. Are broad school math and advanced-track math behaving as different causal objects?
2. Does the male lean in advanced math survive earlier-math alignment?

### Primary estimands

1. sex coefficient for advanced-math participation conditional on earlier math
2. sex gap in advanced-track performance conditional on earlier math
3. upper-tail representation ratios kept separate from means

### Core methods

1. logistic models for advanced-track entry
2. conditional performance models inside advanced-track groups
3. separate tail and mean analyses

### Success criteria

1. divergence between broad-population and advanced-track surfaces hardens Node `3`
2. collapse of the divergence after prior-math adjustment softens Node `3`

### Output artifacts

1. `research/iq-sex-differences-track-selection-pass.md`
2. `sources/iq-sex-diff/data/track/track_entry_models.tsv`
3. `sources/iq-sex-diff/data/track/track_performance_models.tsv`

---

## Stage 7 - `PIAAC` Adult Accumulation And Process Pass

**Priority:** medium
**Node attacked:** `AdultAccumulation`
**Why seventh:** adult numeracy matters, but it should not decide youth-stage causes before school-stage nodes are resolved.

### Questions

1. Is the adult numeracy gap already present in younger adults and then amplified?
2. Do process traces change the adult interpretation materially?

### Primary estimands

1. age-band numeracy gaps
2. field / occupation-stratified gaps where available
3. process-aware gap movement

### Core methods

1. plausible-value estimation with replicate weights
2. age-by-field / occupation heterogeneity
3. log-file process models

### Success criteria

1. early presence plus later widening supports amplification
2. collapse after field / process alignment weakens Node `4`

### Output artifacts

1. `research/iq-sex-differences-piaac-accumulation-pass.md`
2. `sources/iq-sex-diff/data/piaac/piaac_accumulation_models.tsv`

---

## Stage 8 - Residual General-Ability Synthesis

**Priority:** last
**Node attacked:** `LatentGeneralGap`
**Why last:** this claim should only be addressed after the earlier nodes are materially reduced.

### Questions

1. After surface-aware rescoring and school / track decomposition, is any male-leaning residual stable enough to deserve a general-ability interpretation?

### Primary estimands

1. residual gap across aligned balanced surfaces
2. cross-battery consistency of sign and magnitude
3. tail behavior kept separate from means

### Core methods

1. hierarchical meta-analytic synthesis over aligned surfaces
2. preregistered exclusion of contaminated surfaces
3. sensitivity analysis to measurement and selection assumptions

### Success criteria

1. same-sign residual across balanced surfaces hardens the residual-general-gap story
2. continued sign instability rejects strong battery-invariant claims

### Output artifacts

1. `research/iq-sex-differences-residual-synthesis.md`

---

## Statistical Standards

Every stage should keep the same reporting skeleton:

1. unrestricted descriptive estimate
2. same-sample base estimate
3. design-only estimate
4. mechanism estimate
5. stress-test estimate

Every stage should also report:

1. sample size
2. missingness or analyzability restriction
3. exact sex-gap sign convention
4. whether the estimate is weighted or sample-descriptive
5. what would count as a belief update before seeing the result

---

## Anti-Slop Rules

Do not count any of the following as decisive:

1. attenuation from adding descendant or collider controls
2. one battery's composite gap
3. a pooled result that hides item-family or track differences
4. upper-tail rhetoric inferred from mean gaps
5. adult numeracy used to settle school-stage causes by itself
6. adolescent transcript stories used to settle whether the divergence already appeared in early school

---

## Immediate Work Queue

The immediate queue is:

1. use `research/iq-sex-differences-mediator-design.md` as the hard constraint for any new outcome-branch model
2. pursue the live restricted path: `Add Health` restricted-use / `AHAA`
3. prepare, but do not actively file, `HSTS` and `NAEP` restricted-use materials until the `NCES` pause lifts

That is the shortest path to materially reducing uncertainty without reopening already-saturated public-use branches.

---

## Definition Of Done

This execution plan has succeeded when the project can say one of the following with discipline:

1. the disagreement is mostly surface-level, and strong general-ability claims should be downgraded
2. the disagreement survives surface-aware rescoring and school / track decomposition, so a narrower latent-domain or residual-general-gap claim is now justified

If neither statement can be defended, the honest answer remains that the project has localized the disagreement but not fully resolved it.

Current execution status now also includes:

1. `PISA 2018` framework-proxy pass written to `research/iq-sex-differences-pisa2018-framework-proxy.md`
2. widened `NLSCYA` intake written to `sources/iq-sex-diff/data/nlscya/nlscya_early_school_variable_map.tsv` and `sources/iq-sex-diff/data/nlscya/nlscya_early_school_extract.tsv.gz`
3. `NLSCYA` early-school first pass written to `research/iq-sex-differences-nlscya-early-school-first-pass.md`
4. `ECLS-K:2011` early-school first pass written to `research/iq-sex-differences-eclsk2011-early-school-first-pass.md`
5. older `ECLS-K` early-school first pass written to `research/iq-sex-differences-eclsk-early-school-first-pass.md`
6. early-school score-alignment pass written to `research/iq-sex-differences-early-school-score-alignment.md`
7. first external `NELS` wedge replication written to `research/iq-sex-differences-nels-wedge-first-pass.md`
8. first cross-dataset late-school synthesis written to `research/iq-sex-differences-school-wedge-synthesis.md`
9. restricted-data frontier frozen in `research/iq-sex-differences-restricted-data-plan.md`
10. outcome-branch mediator design frozen in `research/iq-sex-differences-mediator-design.md`
