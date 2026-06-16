# IQ Sex Differences - PISA 2018 2PL Anchor Sensitivity

**Date:** 2026-03-07  
**Purpose:** test whether a stronger latent-variable sensitivity using `py-irt` `2PL` meaningfully hardens or overturns the current public `PISA 2018` measurement branch.

This memo is a saturation check, not a new headline result.

---

## Executive Answer

The balanced-country `2PL` pass does **not** overturn the current `PISA` measurement story, but it also does **not** add clean new certainty.

What survives:

1. the broad residual split does not reverse into a female-favoring content-family geometry [SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_dif_2pl_anchor_content_summary.tsv`; `sources/iq-sex-diff/data/pisa/pisa2018_2pl_seed_sensitivity.tsv`]
2. `uncertainty_data` remains closest to parity on average across the seed checks [SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_2pl_seed_sensitivity.tsv`]
3. the `2PL` branch does not rescue a simple “timing/process explains the male residual score families” story [INFERENCE from the new `2PL` results plus `research/iq-sex-differences-pisa2018-time-dif-theta.md`]

What fails:

1. the family ordering is too seed/sample unstable to harden beyond the existing Rasch/theta stack [SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_2pl_seed_sensitivity.tsv`]
2. even the same nominal seed did not reproduce cleanly on rerun under the current `py-irt` path [SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_2pl_seed_sensitivity.tsv`; `sources/iq-sex-diff/data/pisa/pisa2018_2pl_same_seed_compare.tsv`]

### Causal-check

> **Observation:** the public `PISA` branch already survives leave-out matching, fixed-anchor purification, iterative purification, weighted binary logit, anchored Rasch, latent-`theta` score DIF, and latent-`theta` time DIF. The new `2PL` pass preserves the coarse male residual geometry on average but is materially unstable across repeated stochastic fits on the sparse rotated-booklet anchor core. [SOURCE: `research/iq-sex-differences-pisa2018-dif-leaveout.md`; `research/iq-sex-differences-pisa2018-dif-purified.md`; `research/iq-sex-differences-pisa2018-dif-iterative.md`; `research/iq-sex-differences-pisa2018-dif-logit.md`; `research/iq-sex-differences-pisa2018-dif-rasch.md`; `research/iq-sex-differences-pisa2018-dif-theta-logit.md`; `research/iq-sex-differences-pisa2018-time-dif-theta.md`; `sources/iq-sex-diff/data/pisa/pisa2018_2pl_seed_sensitivity.tsv`]
>
> **Null:** if the earlier public `PISA` residual family ordering was mostly an artifact of weaker anchor construction, a stronger `2PL` anchor should either collapse the ordering or reproduce a clearly more stable version of it. [INFERENCE]
>
> **Residual after null:** the coarse split survives, but the `2PL` route itself is not stable enough in the current public design to become the new canonical result. [INFERENCE]

- `P(cause)`: `0.72` that the public `PISA` measurement branch is now saturated enough that more local hybrid psychometric tweaks will add less certainty than a tooling change or restricted-data shift. [INFERENCE]
- `Top alternative`: `0.18` that a better-tuned local `2PL` / joint latent model would still materially sharpen the family ordering without needing a different environment. [INFERENCE]
- `Falsifier`: a weighted joint multi-group latent-variable model in which the current residual content-family ordering collapses cleanly. [INFERENCE]
- `Decision impact`: stop treating local public `PISA` hybrid refinements as the main frontier; move either to a different psychometric toolchain or to restricted transcript/process data. [INFERENCE]

---

## Design

The new pass uses:

1. the iterative low-DIF binary anchor set from the current public `PISA` branch (`17` items) [SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_item_dif_iterative.tsv`]
2. a balanced-country sampled design with `120` respondents per country where possible (`71` countries, `8,520` respondents total) [SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_2pl_anchor_diagnostics.tsv`]
3. a minimum of `4` answered anchor items per respondent, because the rotated booklet design never gives more than `7` of the retained anchor items to any one person in the local extract [SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_2pl_anchor_diagnostics.tsv`; local distribution probe in session]
4. `py-irt` `2PL` training for `60` epochs on the sampled anchor core [SOURCE: `sources/iq-sex-diff/pisa2018_dif_2pl_anchor_pass.py`; `sources/iq-sex-diff/data/pisa/pisa2018_2pl_anchor_diagnostics.tsv`]
5. weighted within-country standardization of the exported anchor `theta`
6. weighted item-level binomial DIF with country fixed effects using that `theta` as the match surface [SOURCE: `sources/iq-sex-diff/pisa2018_dif_2pl_anchor_pass.py`]

This is stronger than the earlier hand-built or Rasch-only match surfaces in one sense, but still weaker than a weighted joint multi-group latent model. [INFERENCE]

---

## Main Results

### 1. Base rerun

In the current base rerun, the anchor `theta` itself is slightly female-leaning:

- anchor gap `d = +0.060` [SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_2pl_anchor_gap.tsv`]

The weighted content-family summary is:

- `change_relationships = -0.001`
- `quantity = -0.031`
- `space_shape = -0.019`
- `uncertainty_data = +0.032`

[SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_dif_2pl_anchor_content_summary.tsv`]

So the base rerun does **not** reverse into a female-favoring overall residual geometry, but it is much flatter than the current Rasch/theta stack. [INFERENCE]

### 2. Seed sensitivity

Across three explicit seed checks:

- `change_relationships` is male in `3/3`
- `quantity` is male in `2/3`
- `space_shape` is male in `1/3`
- `uncertainty_data` is male in `1/3`

[SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_2pl_seed_sensitivity.tsv`]

Across the same seed checks, the mean family effects are:

- `space_shape mean = -0.039`, `sd = 0.095`
- `quantity mean = -0.027`, `sd = 0.043`
- `change_relationships mean = -0.052`, `sd = 0.046`
- `uncertainty_data mean = -0.005`, `sd = 0.135`

[SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_2pl_seed_sensitivity.tsv`]

That is too unstable to call a new hardened family ranking.

### 3. Same-seed rerun instability

The same nominal seed (`20260307`) did not reproduce cleanly on rerun. The current rerun differs from the earlier saved `20260307` row by:

- `change_relationships`: `+0.030`
- `quantity`: `+0.017`
- `space_shape`: `-0.022`
- `uncertainty_data`: `+0.023`

[SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_2pl_seed_sensitivity.tsv`; `sources/iq-sex-diff/data/pisa/pisa2018_2pl_same_seed_compare.tsv`]

This is the most important epistemic result in the memo. Under the current sparse anchor/booklet geometry and local `py-irt` path, the `2PL` pass is not deterministic enough to become the new canonical psychometric result.

---

## Comparison To The Current Canonical PISA Stack

The earlier public branch already established:

1. strong agreement between weighted binary logit and anchored Rasch (`r = 0.930`) [SOURCE: `research/iq-sex-differences-pisa2018-dif-rasch.md`]
2. almost perfect agreement between weighted binary logit and latent-`theta` logit (`r = 0.991`) [SOURCE: `research/iq-sex-differences-pisa2018-dif-theta-logit.md`]
3. broad female-slower timing that still does not line up tightly with the localized residual score geometry [SOURCE: `research/iq-sex-differences-pisa2018-time-dif-theta.md`]

The `2PL` pass does not falsify that stack. It shows that a sampled `2PL` hybrid route on the public extract is itself noisier than the existing Rasch/theta stack.

[INFERENCE] That means the existing canonical `PISA` read should remain:

1. the residual family split is real enough to use operationally
2. the strongest local public support still comes from the Rasch/theta stack
3. the next real step is not another local hybrid tweak, but a tooling upgrade or restricted-data shift

---

## Decision

Do **not** promote the current `2PL` family ordering into the claim register as a stronger replacement for the current Rasch/theta stack.

Do use this pass for two narrower updates:

1. the public `PISA` branch is now saturated enough that more local hybrid refinements are low-yield [INFERENCE]
2. the remaining psychometric frontier is a weighted joint multi-group latent-variable model, not another local approximate sensitivity [INFERENCE]

