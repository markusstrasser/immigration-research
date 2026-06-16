# IQ Sex Differences - PISA 2018 Iterative Purification Pass

**Date:** 2026-03-06  
**Purpose:** move the `PISA 2018` measurement branch one step beyond the fixed-anchor purified pass by iteratively updating the low-DIF anchor set rather than freezing it after one selection.

## Why This Pass Exists

The strongest remaining local objection to the fixed-anchor purified pass was straightforward:

> maybe the residual family ordering survives only because the anchor set was frozen after one low-DIF selection.

This pass tests that objection directly. [INFERENCE]

## Build

The iterative loop starts from the contamination-aware leave-out seed, then repeats:

1. fit item models using the current anchor set
2. keep items with `|uniform| <= 0.025` and `|nonuniform| <= 0.015`
3. if too few items remain, backfill to `15+` anchors with the smallest combined residuals
4. rebuild the anchor score and repeat

Outputs:

1. `sources/iq-sex-diff/data/pisa/pisa2018_item_dif_iterative.tsv`
2. `sources/iq-sex-diff/data/pisa/pisa2018_dif_iterative_content_summary.tsv`
3. `sources/iq-sex-diff/data/pisa/pisa2018_dif_iterative_context_summary.tsv`
4. `sources/iq-sex-diff/data/pisa/pisa2018_dif_iterative_anchor_items.tsv`
5. `sources/iq-sex-diff/data/pisa/pisa2018_dif_iterative_anchor_gap.tsv`
6. `sources/iq-sex-diff/data/pisa/pisa2018_dif_iterative_history.tsv`

[SOURCE: `sources/iq-sex-diff/pisa2018_dif_iterative_pass.py`]

## Main Result

The residual family ordering still survives, and the male-leaning anchor objection gets weaker rather than stronger.

Final weighted uniform residuals:

- `space_shape = -0.0246`
- `change_relationships = -0.0216`
- `quantity = -0.0157`
- `uncertainty_data = -0.0088`

[SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_dif_iterative_content_summary.tsv`]

Final iterative anchor score:

- `female_minus_male_d = -0.010`

[SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_dif_iterative_anchor_gap.tsv`]

That is the key footprint:

- the anchor score itself is now near parity
- the residual family ordering still points male
- `space_shape` still remains the strongest male-residual family
- `uncertainty_data` still remains the closest to parity

[INFERENCE based on: `sources/iq-sex-diff/data/pisa/pisa2018_dif_iterative_content_summary.tsv`; `sources/iq-sex-diff/data/pisa/pisa2018_dif_iterative_anchor_gap.tsv`]

## Comparison To Earlier Passes

This is stronger than the earlier local sequence:

1. plausible-value conditioning
2. leave-item / leave-family matching
3. one-shot fixed-anchor purification

because the current result no longer depends on keeping a visibly male-leaning anchor core. The final anchor score is nearly neutral, but the residual family ordering remains. [INFERENCE]

## Important Limitation

This still is **not** a final formal DIF result.

The iterative history says the anchor set was still moving through six iterations:

- iteration `1`: `23` anchors
- iteration `2`: `18`
- iteration `3`: `16`
- iteration `4`: `17`
- iteration `5`: `16`
- iteration `6`: `18`

and the set did not fully stabilize before the loop cap. [SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_dif_iterative_history.tsv`]

So this pass should be read as:

- a stronger stress test
- not full multi-group IRT
- not guaranteed iterative convergence
- not a final fairness verdict

[INFERENCE]

## Causal / Measurement Read

> **Observation:** after iterative anchor updating, the final anchor score is basically at parity, but the residual item-family ordering remains male-leaning and still ranks `space_shape` as the strongest residual family. [SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_dif_iterative_content_summary.tsv`; `sources/iq-sex-diff/data/pisa/pisa2018_dif_iterative_anchor_gap.tsv`]
>
> **Null:** if the earlier purified result were mostly a byproduct of starting from a male-leaning anchor core, iterative updating should pull the residual family ordering materially toward zero once the anchor score itself becomes neutral. [INFERENCE]
>
> **Residual after null:** it does not. The anchor gap shrinks almost to zero, but the residual family pattern survives and in some families becomes slightly more male. [SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_dif_iterative_content_summary.tsv`; `sources/iq-sex-diff/data/pisa/pisa2018_dif_purified_content_summary.tsv`]

- `P(cause)`: `0.78` that the current `PISA` residual family ordering is not just a male-anchor artifact. [INFERENCE]
- `Top alternative`: `0.14` that the ordering is still partly an artifact of nonconverged iterative purification or linear-probability approximation rather than a real stable item-family pattern. [INFERENCE]
- `Falsifier`: a fuller multi-group IRT / invariant-item analysis where the ordering shrinks sharply once latent scoring is purified to convergence. [INFERENCE]
- `Decision impact`: the local measurement branch is now strong enough to treat the `PISA` residual family ordering as a real working structure, while still keeping the final psychometric verdict open. [INFERENCE]
