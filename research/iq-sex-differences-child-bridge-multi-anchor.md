# IQ Sex Differences - Child Bridge Multi-Anchor Pass

**Date:** 2026-03-06  
**Purpose:** reduce the remaining early-school bridge blind spot by testing whether the relative child math result survives more than one verbal anchor.

This memo is the follow-through on the open Stage 2 critique that the child bridge had been hardened mostly on `reading`, not on a broader anchor family.

## What Was Built

The new analysis script is:

- `sources/iq-sex-diff/child_bridge_multi_anchor.py`

Outputs:

- `sources/iq-sex-diff/data/child_bridge_multi_anchor/child_bridge_multi_anchor_summary.tsv`
- `sources/iq-sex-diff/data/child_bridge_multi_anchor/child_bridge_multi_anchor_family_fe.tsv`
- `sources/iq-sex-diff/data/child_bridge_multi_anchor/child_bridge_multi_anchor_compare.tsv`
- `sources/iq-sex-diff/data/child_bridge_multi_anchor/child_bridge_multi_anchor_models.tsv`

The pass uses three child datasets with different anchor surfaces:

1. `PSID CDS`
2. `NLSCYA`
3. `FFCWS`

`ECLS` is not rerun here because the public early-school extracts only expose broad math and broad reading. The point of this pass is to test whether the bridge survives once richer verbal anchors are available. [INFERENCE]

## Main Results

### 1. `PSID CDS` is strongly male-leaning on relative child math under every tested verbal anchor

Pooled weighted female-minus-male `d`:

- `math minus broad_reading`: `-0.317`
- `math minus letter_word`: `-0.327`
- `math minus passage`: `-0.330`
- `math minus mean_verbal`: `-0.345`

[SOURCE: `sources/iq-sex-diff/data/child_bridge_multi_anchor/child_bridge_multi_anchor_summary.tsv`]

The within-family version points the same way:

- `broad_reading` anchor: `beta_female = -5.06`, `95% CI [-6.86, -3.26]`
- `letter_word` anchor: `beta_female = -4.14`, `95% CI [-5.63, -2.66]`
- `passage` anchor: `beta_female = -4.40`, `95% CI [-6.00, -2.80]`
- `mean_verbal` anchor: `beta_female = -4.11`, `95% CI [-5.43, -2.79]`
- joint `letter_word + passage` family fixed-effects model: `beta_female = -3.28`, `95% CI [-4.63, -1.93]`

[SOURCE: `sources/iq-sex-diff/data/child_bridge_multi_anchor/child_bridge_multi_anchor_family_fe.tsv`]

That is the strongest new child result in the repo. It says the male-leaning relative child-math result is not a reading-only artifact in the family-linked public child panel. [INFERENCE]

### 2. `NLSCYA` still points male under reading and mean-verbal anchors, but `PPVT` alone is weaker and can briefly reverse

Pooled weighted female-minus-male `d`:

- `math minus reading`: `-0.163`
- `math minus mean_verbal`: `-0.137`
- `math minus PPVT`: `+0.022`

[SOURCE: `sources/iq-sex-diff/data/child_bridge_multi_anchor/child_bridge_multi_anchor_summary.tsv`]

By age bin, the same pattern holds:

- `reading` and `mean_verbal` are male-leaning in every `4-5`, `6-7`, `8-9`, `10-11`, and `12-13` bin
- `PPVT` is the unstable anchor: female-leaning at `6-7` and `8-9`, then near null to male later

[SOURCE: `sources/iq-sex-diff/data/child_bridge_multi_anchor/child_bridge_multi_anchor_summary.tsv`]

The critical sanity check is the `PPVT` overlap sample:

- `math minus reading` on the same `PPVT`-observed subset: `d = -0.076`
- `math minus mean_verbal` on the same `PPVT`-observed subset: `d = -0.041`

[SOURCE: `sources/iq-sex-diff/data/child_bridge_multi_anchor/child_bridge_multi_anchor_summary.tsv`]

So the `PPVT` issue is not enough to reopen the child sign conflict by itself. The bridge still leans male once reading or mean-verbal anchors are used on that overlapping subset. [INFERENCE]

### 3. `NLSCYA` joint-anchor models are mixed, but they do not support a clean female relative-math story

Model summaries:

- `piat_math ~ female + reading + PPVT + age_bin`: `beta_female = -0.18`, `95% CI [-1.17, 0.81]`
- `piat_math ~ female + mean_verbal + age_bin`: `beta_female = -0.81`, `95% CI [-1.43, -0.19]`

[SOURCE: `sources/iq-sex-diff/data/child_bridge_multi_anchor/child_bridge_multi_anchor_models.tsv`]

Best read:

- the larger `mean_verbal` model still points male
- the smaller `reading + PPVT` overlap model weakens and becomes noisy

That means the child branch is materially more stable than it was, but not fully psychometrically closed. [INFERENCE]

### 4. `FFCWS` confirms that anchor sensitivity remains real outside early-school

Year 9 weighted female-minus-male `d`:

- `applied minus passage`: `-0.179`
- `applied minus PPVT`: `+0.084`
- `applied minus mean_verbal`: `-0.043`

[SOURCE: `sources/iq-sex-diff/data/child_bridge_multi_anchor/child_bridge_multi_anchor_summary.tsv`]

The residual models are near zero:

- `applied ~ female + passage + PPVT + background`: `beta_female = -0.004`, `95% CI [-0.109, 0.101]`
- `applied ~ female + mean_verbal + background`: `beta_female = +0.010`, `95% CI [-0.092, 0.112]`

[SOURCE: `sources/iq-sex-diff/data/child_bridge_multi_anchor/child_bridge_multi_anchor_models.tsv`]

So `FFCWS` should still be treated as a later-child anchor-sensitivity stress test, not as the dataset that decides the early-school branch. [INFERENCE]

## Causal Check

> **Observation:** once richer anchors are added, the family-linked `PSID CDS` child panel stays clearly male-leaning on relative math under every tested verbal anchor, while `NLSCYA` stays male under reading and mean-verbal anchors but weakens under `PPVT` alone; the `PPVT` overlap subset still leans male under reading and mean-verbal; `FFCWS` confirms that anchor sensitivity remains real in later-child data. [SOURCE: `sources/iq-sex-diff/data/child_bridge_multi_anchor/child_bridge_multi_anchor_summary.tsv`; `sources/iq-sex-diff/data/child_bridge_multi_anchor/child_bridge_multi_anchor_family_fe.tsv`; `sources/iq-sex-diff/data/child_bridge_multi_anchor/child_bridge_multi_anchor_models.tsv`]
>
> **Null:** the child bridge only looked male because the repo happened to anchor on reading, and the direction should collapse or reverse once vocabulary/language anchors are added. [INFERENCE]
>
> **Residual after null:** that strong null does not survive. The result is no longer reading-only. The sharper residual is: `PPVT` is a weaker and more unstable anchor than reading or a broader mean-verbal composite, especially in `NLSCYA` and `FFCWS`. [INFERENCE]

- `P(cause)`: `0.78` that the child branch is directionally robust under reading and broader mean-verbal anchoring, with `PPVT` alone acting as a weaker and more sample-sensitive anchor rather than overturning the branch. [INFERENCE]
- `Top alternative`: `0.16` that the apparent robustness still depends too much on reading-like school-language anchors, and a stronger psychometric bridge could shrink the male relative-child-math result further. [INFERENCE]
- `Falsifier`: another family-linked child cohort or a stronger rank-based / invariant-item bridge where the relative child-math sign turns female or near zero under a mean-verbal anchor rather than only under `PPVT`. [INFERENCE]
- `Decision impact`: stop treating the child branch as “reading only,” and stop treating `PPVT` alone as a decisive counter-anchor. The remaining child issue is bridge quality and magnitude, not basic sign instability. [INFERENCE]

## What This Changes

What hardens:

1. the `PSID CDS` child panel materially strengthens the early-school branch because it survives multiple verbal anchors and a family-linked specification
2. the `NLSCYA` / `ECLS` alignment is no longer hanging on reading alone
3. `PPVT` should be treated as a special-case anchor, not as the child-bridge veto

What softens:

1. the stronger claim that the child branch is fully solved
2. any move from “male relative child math” to “battery-independent early male absolute math advantage”

What remains open:

1. whether a better psychometric bridge than reading / mean verbal / `PPVT` would shrink the remaining magnitude gap further
2. whether rank-based residualization or richer child verbal composites would tighten the `NLSCYA` result
3. whether the later-child anchor sensitivity seen in `FFCWS` reflects age, construct family, or cohort-specific score geometry

## Operational Read

The child branch is now good enough to stop blocking the rest of the project.

The right live summary is:

1. early relative child math is male-leaning in the stronger public child panels
2. that result is no longer reading-only
3. `PPVT` alone is the unstable anchor and should be treated as a sensitivity surface, not as the main bridge

If the project wants publication-grade closure here, the next step is a stronger psychometric bridge or rank-based residualization. If not, effort should shift back to the remaining late-school mediator / transcript / process frontier. [INFERENCE]
