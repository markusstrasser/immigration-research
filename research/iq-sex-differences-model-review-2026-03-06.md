# IQ Sex Differences - Model Review 2026-03-06

**Date:** 2026-03-06
**Purpose:** record the cross-model blind-spot review, what survived local scrutiny, and what changed in the canonical project state.

Inputs:

1. Gemini `3.1 Pro` deep review in `.model-review/2026-03-06-iq-sex-differences-current-state-blind-s/gemini-output.md`
2. GPT-5.4 focused review in `.model-review/2026-03-06-iq-sex-differences-current-state-blind-s/gpt-output-brief.md`

No project `CONSTITUTION.md` or `GOALS.md` was present during this review run, so the models reviewed for internal coherence and evidence discipline rather than against project-specific principles.

---

## Surviving Findings

### 1. The `PISA` DIF-style pass is useful, but only as a proxy shrinkage diagnostic

Both reviewers converged on the same point:

1. the current pass is informative because it shows much of the raw item-family geometry compresses under ability conditioning
2. it is **not** strong enough to carry formal DIF-style claims because the conditioning surface uses OECD plausible values that likely contain target-item information

Adopted update:

- keep the pass as evidence that raw item-family gaps are not pure standalone content effects
- do **not** treat the residual family ordering or near-zero `uncertainty_data` estimate as hardened

### 2. The early-school bridge resolves a sign contradiction only on a relative estimand

The convergent critique was also right here:

1. `math minus reading` is not the same estimand as absolute early-school math
2. the bridge is still useful because it tests whether the cross-dataset contradiction survives after forcing a common internal anchor
3. the current result should therefore be stated as a **relative math-versus-reading bridge**, not as proof of battery-independent absolute early male math advantage

Adopted update:

- keep the bridge as a valid alignment result
- explicitly label it as a relative-performance bridge
- require multi-anchor sensitivity before treating the child branch as fully settled

### 3. The school-surface wedge still under-models behavior / compliance / stakes

The best surviving alternative mechanism is:

`behavior / effort / incentive sensitivity -> course exposure / evaluation -> school-knowledge and transcript surfaces`

That does not kill the current wedge result. It does change how the wedge should be interpreted:

1. not as clean evidence of pure evaluation bias
2. not as clean evidence of pure curriculum exposure
3. as a bundled mechanism family that still needs decomposition

Adopted update:

- later school-surface models should separate pre-treatment, course-exposure, behavior/compliance, and evaluation blocks
- within-ladder results stay descriptive, not causally clean

### 4. The project can over-count non-independent evidence

This critique survived too:

1. multiple `PISA` passes are not independent replications
2. multiple `PIAAC` cuts by age, education, and occupation are also not independent replications

Adopted update:

- repeated slices of the same battery should count as internal stress tests, not as independent confirmations

---

## Deferred Or Rejected Reviewer Claims

### Deferred

1. the strongest Gemini wording that the `PISA` pass is a “methodological hazard”
2. any strong claim that the early-school bridge is likely invalid rather than merely a different estimand
3. any specific behavioral mechanism that is not yet visible in the local covariates

Reason:

the reviewers were directionally right, but the stronger rhetoric outran what the local evidence can support.

### Rejected

1. any suggestion that the current `PISA` proxy pass is worthless
2. any suggestion that the child branch reopens as directionally unresolved right now

Reason:

the local results still contain real information even if the estimands need tighter wording.

---

## Canonical Changes From This Review

1. `PISA` residual-family claims were softened from near-hardened to provisional proxy status
2. child-bridge claims were rewritten to emphasize the relative `math vs reading` estimand
3. behavior / compliance / stakes and repeated-slice non-independence were promoted into explicit risks
4. the execution plan now prioritizes:
   - leave-item-out or anchor-item `PISA` upgrading
   - multi-anchor early-school sensitivity
   - sequential school-surface wedge decomposition

---

## Best Next 3 Analyses

1. rebuild the `PISA` matching variable with leave-item-out or leave-family-out proficiency and rerun the residual family table
2. decompose the `HSLS` / `NLSY97` school-surface wedge with pre-treatment and mechanism blocks kept separate
3. stress-test the early-school bridge with multiple anchors, including reading, vocabulary/language, and rank-based residualization

---

## Bottom Line

The review did not overturn the project. It narrowed the language around three places where the repo was still too confident:

1. the `PISA` conditional item pass
2. the meaning of the child-score bridge
3. the interpretation of the school-surface wedge

That is a real improvement in epistemic hygiene, not a reversal of the main project direction.
