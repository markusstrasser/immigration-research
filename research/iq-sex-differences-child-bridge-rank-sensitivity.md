# IQ Sex Differences - Child Bridge Rank Sensitivity

**Date:** 2026-03-06  
**Purpose:** test whether the early-school child bridge still points the same way once score-family intensity is stripped out with within-stage percentile-rank residualization.

This memo is the direct follow-through on the remaining Stage 2 objection after the multi-anchor pass:

> maybe the bridge still looks male only because the raw score scales load differently, even when multiple anchors are used.

## What Was Built

The new script is:

- `sources/iq-sex-diff/child_bridge_rank_sensitivity.py`

Outputs:

- `sources/iq-sex-diff/data/child_bridge_rank/child_bridge_rank_summary.tsv`
- `sources/iq-sex-diff/data/child_bridge_rank/child_bridge_rank_family_fe.tsv`

Method:

1. within each dataset-stage, compute weighted percentile ranks for math and the chosen verbal anchor
2. form `math_rank - anchor_rank`
3. estimate weighted female-minus-male `d` on that rank-gap surface
4. for `PSID CDS`, rerun the rank-gap surface in a family fixed-effects specification

This is still a descriptive bridge method, not a treatment-effect design. No causal DAG is claimed here because there is no causal estimand being fit. [INFERENCE]

## Main Results

### 1. `PSID CDS` remains male-leaning under every anchor even after rank transformation

Pooled weighted female-minus-male `d`:

- `broad_reading`: `-0.416`
- `letter_word`: `-0.356`
- `passage`: `-0.385`
- `mean_verbal`: `-0.388`

[SOURCE: `sources/iq-sex-diff/data/child_bridge_rank/child_bridge_rank_summary.tsv`]

The family fixed-effects version also stays male:

- `broad_reading`: `beta_female = -0.0776`, `95% CI [-0.1015, -0.0537]`
- `letter_word`: `beta_female = -0.0680`, `95% CI [-0.0924, -0.0436]`
- `passage`: `beta_female = -0.0883`, `95% CI [-0.1139, -0.0628]`
- `mean_verbal`: `beta_female = -0.0758`, `95% CI [-0.0979, -0.0536]`

[SOURCE: `sources/iq-sex-diff/data/child_bridge_rank/child_bridge_rank_family_fe.tsv`]

That removes the strongest remaining “raw scale intensity” objection for the family-linked public child panel. [INFERENCE]

### 2. `NLSCYA` keeps the same ordering after rank transformation

Pooled weighted female-minus-male `d`:

- `reading`: `-0.128`
- `mean_verbal`: `-0.121`
- `PPVT`: `+0.023`

[SOURCE: `sources/iq-sex-diff/data/child_bridge_rank/child_bridge_rank_summary.tsv`]

By age bin:

- `reading` is male-leaning at `6-7`, `8-9`, and `10-11`, and near null at `12-13`
- `mean_verbal` is male-leaning at `4-5`, `6-7`, `8-9`, and `10-11`, and near null at `12-13`
- `PPVT` is the unstable anchor again: positive at `6-7` and `8-9`, then negative later

[SOURCE: `sources/iq-sex-diff/data/child_bridge_rank/child_bridge_rank_summary.tsv`]

So the rank pass says the same thing as the raw multi-anchor pass: the live ambiguity is `PPVT`, not the whole child branch. [INFERENCE]

### 3. `FFCWS` still behaves like a later-child anchor-sensitivity stress test, not like an early-school reversal

Weighted female-minus-male `d` on rank-gap surfaces:

- `passage`: `-0.217`
- `mean_verbal`: `-0.076`
- `PPVT`: `+0.043`

[SOURCE: `sources/iq-sex-diff/data/child_bridge_rank/child_bridge_rank_summary.tsv`]

That is the same ordering as before. The rank transform does not rescue a general female relative-math reading in `FFCWS`; it just keeps showing that `PPVT` is a weaker and more volatile verbal anchor than passage/reading-like anchors. [INFERENCE]

## Causal Check

> **Observation:** once the child bridge is rewritten in percentile-rank space, `PSID CDS` remains clearly male-leaning under every tested anchor and still does so within families; `NLSCYA` remains male under reading and mean-verbal anchors; `PPVT` alone remains the only weak/unstable exception; `FFCWS` keeps the same anchor ordering. [SOURCE: `sources/iq-sex-diff/data/child_bridge_rank/child_bridge_rank_summary.tsv`; `sources/iq-sex-diff/data/child_bridge_rank/child_bridge_rank_family_fe.tsv`]
>
> **Null:** the earlier multi-anchor result was mostly a raw-score-scale artifact, so the sign should disappear once every surface is converted to within-stage ranks. [INFERENCE]
>
> **Residual after null:** it does not disappear. The same broad ordering survives. [INFERENCE]

- `P(cause)`: `0.82` that the early-school bridge is directionally robust on public data under both multi-anchor and rank-based checks, with `PPVT` alone remaining a weaker and more sample-sensitive exception rather than a branch reversal. [INFERENCE]
- `Top alternative`: `0.12` that a stronger psychometric bridge could still shrink the magnitude enough that the public child result becomes near null rather than clearly male-leaning. [INFERENCE]
- `Falsifier`: an invariant-item or stronger latent bridge where the rank-based child result turns female or close to zero under a mean-verbal anchor, not just under `PPVT`. [INFERENCE]
- `Decision impact`: Stage 2 no longer needs to block the project on public-use data. If more child work is done, it should be psychometric refinement rather than another cohort hunt. [INFERENCE]

## Operational Read

The public child branch is now good enough to summarize this way:

1. the relative early-school math result is not reading-only
2. it is not a raw-scale artifact either
3. `PPVT` alone remains the unstable anchor and should be treated as sensitivity, not veto

That means the next high-value uncertainty is no longer “is the child branch real?” It is the remaining late-school mediator / restricted-transcript / process frontier. [INFERENCE]
