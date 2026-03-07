# Review 1 Audit

**Date:** 2026-03-05
**Subject:** audit of `research/review-1.md`
**Purpose:** decide what to keep, soften, or reject from the external GPT review.

---

## Verdict

Mostly cosign.

The review is materially useful because its strongest claims survive direct checking against:

- the local `NLSY97` Stage A script and output tables
- the official `NLSY97` CAT-ASVAB documentation
- the official `NLSY97` PIAT / transcript documentation
- the official ASVAB CAT-vs-paper technical bulletin

The main value is methodological, not rhetorical:

1. it correctly identifies a bad-control problem in the current `NLSY97` Stage A interpretation
2. it correctly upgrades same-sample selection / observability as part of the local sign-flip story
3. it correctly promotes same-cohort `PIAT Math` + transcript / honors / course-ladder work as the cleanest immediate next discriminating pass
4. it correctly downgrades `PISA 2022` as the primary public timing / visits dataset relative to `PISA 2018`

I do **not** cosign it wholesale. The exact posterior probabilities are subjective, some phrasing overstates novelty, and a few source / formatting details are sloppy.

## Keep

### 1. Stage A is a robustness warning, not causal identification

Cosign.

The review is right that the current `process_core` block is not a clean nuisance-adjustment block. The local script includes:

- `numerical_operations_items_complete`
- `coding_speed_items_complete`
- `arithmetic_reasoning_post_variance`
- `math_knowledge_post_variance`
- `effort`

Those are not generic exogenous room-noise controls. Several are descendants of the score-generating process itself. That means coefficient movement in Stage A is evidence that the raw `NLSY97` female quantitative edge is fragile, but not clean evidence that process / measurement *caused* it.

Local provenance:

- `sources/iq-sex-diff/nlsy97_stage_a_pass.py`
- `sources/iq-sex-diff/stage0_config.py`
- `sources/iq-sex-diff/data/nlsy/nlsy97_stage_a_covariate_gaps.tsv`

### 2. Same-sample movement is already doing real work

Cosign.

The review is right that part of the `NLSY97` story is selection / observability, not just adjustment. In the local Stage A tables:

- unrestricted `quantitative`: `+0.054`
- same-sample base `process_core`: `+0.037`
- same-sample base `school_core`: `-0.007`
- same-sample base `process_plus_school_core`: `-0.010`

That means the subset mechanics already move the sign before the full blocks are applied. `H4` was underweighted in the earlier narrative.

### 3. The omitted design controls matter

Cosign.

The review is right that our local emphasis was slightly upside-down. The official `NLSY97` docs make these design features salient:

- adaptive power tests versus non-adaptive speed tests
- an easy start form for the youngest 1983/1984 birth cohorts
- internal age-group norming for the NLS-created math-verbal percentile

Those are closer to primary design-adjustment variables than `effort`, `items_complete`, or posterior variance.

### 4. Same-cohort `PIAT Math` is the highest-leverage missing internal check

Cosign with a caution.

The docs do explicitly point to using `PIAT Math` together with transcript / curriculum information. That makes the same-cohort `CAT-ASVAB` versus `PIAT Math` comparison a strong next pass.

The caution is that `PIAT Math` is not a perfect arbiter. It is a younger and narrower school-math surface, so ceiling / sample-selection issues remain live.

### 5. `PISA 2018` is stronger than `PISA 2022` for public timing / visits work

Cosign.

The review’s correction here is useful. For public process analysis, `PISA 2018` should be preferred over `PISA 2022` when the target is cognitive time / visits files. `PISA 2022` remains useful for item content and current adaptive structure, but it is not the best public timing file.

## Soften

### 1. “Largest conceptual error”

Too strong.

The repo had already recorded construct-mismatch risk before this review. The review is right that the issue needs stronger operational handling, but it is not a brand-new discovery.

### 2. Exact posterior probabilities

Do not adopt as-is.

The review’s qualitative ranking is useful:

- score-surface non-equivalence still leads
- selection / observability should be upgraded
- school sorting remains live but underidentified

The exact numbers `0.36 / 0.20 / 0.18 / 0.16 / 0.10` are judgment calls, not something the sources uniquely determine.

### 3. “Single best next move is not external”

Mostly right, not absolute.

The internal `NLSY97` same-cohort pass is the highest-leverage immediate move because it attacks the anomaly directly. But it should not crowd out `HSLS:09` and `ELS:2002`; those remain the cleanest external adjudicators for the school-sorting branch.

## Reject Or Flag

### 1. Formatting and citation hygiene

The file has visible formatting damage:

- broken section numbering
- repeated object markers `￼`

That does not invalidate the content, but it is a reliability warning.

### 2. Some URL-level sloppiness

At least one source pointer is stale or weakly verified:

- the cited `NAEP` process-data URL in the review does not resolve cleanly in a simple HTTP check
- the `Project Talent` access claim was explicitly not fully verified by the review itself

These are not fatal because they are peripheral to the main causal correction, but they are a reminder not to treat the whole file as source-perfect.

## Net Update To Project State

1. Keep the claim that the raw `NLSY97` female quantitative edge is fragile.
2. Soften the claim that current Stage A already shows a primarily process / measurement cause.
3. Upgrade selection / observability as part of the `NLSY97` node.
4. Separate `NLSY97` follow-up models into:
   - design-only adjustment
   - mechanism blocks
   - bad-control stress tests
5. Promote same-cohort `PIAT Math` + transcript / honors / course-ladder comparison ahead of more external battery rhetoric.
6. Prefer `PISA 2018` over `PISA 2022` for public cognitive timing / visits analysis.

## Adoption Decision

**Status:** adopted in part

What I am adopting:

- the bad-control critique of Stage A
- the selection / observability upgrade
- the design-control correction
- the `PIAT Math` next-step promotion
- the `PISA 2018` process-data correction

What I am not adopting directly:

- the exact posterior numbers
- the strongest phrasing about novelty
- any claim that the review alone settled the `NLSY97` node
