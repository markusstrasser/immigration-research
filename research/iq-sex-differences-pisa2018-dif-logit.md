# IQ Sex Differences - PISA 2018 Binary Logit DIF Pass

**Date:** 2026-03-06  
**Purpose:** test whether the current `PISA 2018` residual item-family ordering survives under a more appropriate response model for the binary-scored math items.

## Why This Pass Exists

The remaining easy objection to the local `PISA` branch was:

> the ordering might survive in linear residual models but disappear once the binary item responses are fit with a proper binomial link.

This pass addresses that directly on the binary-scored items. [INFERENCE]

## Design

The pass uses:

- binary-scored math items only
- the iterative anchor set from the stronger local purification pass
- a leave-one-out binary anchor score
- a weighted binomial GLM with:
  - `female`
  - anchor score
  - `female * anchor`
  - country fixed effects

Outputs:

1. `sources/iq-sex-diff/data/pisa/pisa2018_item_dif_logit.tsv`
2. `sources/iq-sex-diff/data/pisa/pisa2018_dif_logit_content_summary.tsv`
3. `sources/iq-sex-diff/data/pisa/pisa2018_dif_logit_anchor_gap.tsv`

[SOURCE: `sources/iq-sex-diff/pisa2018_dif_logit_pass.py`]

## Main Result

The same family ordering survives again.

Weighted uniform logit residuals:

- `space_shape = -0.140`
- `change_relationships = -0.102`
- `quantity = -0.087`
- `uncertainty_data = -0.028`

[SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_dif_logit_content_summary.tsv`]

The binary anchor score itself is near parity:

- `female_minus_male_d = -0.012`

[SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_dif_logit_anchor_gap.tsv`]

So the local `PISA` residual geometry now survives:

1. plausible-value conditioning
2. leave-item / leave-family matching
3. fixed-anchor purification
4. iterative anchor updating
5. a binomial item model on the binary-scored items

[INFERENCE]

## What This Means

This does **not** prove formal multi-group IRT DIF.

It does make one weaker claim harder to dodge:

> the surviving `PISA` family ordering is not just a linear-model artifact.

[INFERENCE]

The ordering remains the same:

- `space_shape` strongest male
- `change_relationships` next
- `quantity` also male
- `uncertainty_data` closest to parity

[SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_dif_logit_content_summary.tsv`; `sources/iq-sex-diff/data/pisa/pisa2018_dif_iterative_content_summary.tsv`]

## Causal / Measurement Read

> **Observation:** on binary-scored `PISA` items with a binomial link and country fixed effects, the residual item-family ordering still matches the earlier local passes while the anchor score remains near parity. [SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_dif_logit_content_summary.tsv`; `sources/iq-sex-diff/data/pisa/pisa2018_dif_logit_anchor_gap.tsv`]
>
> **Null:** if the local `PISA` family ordering were mainly a byproduct of linear approximation, it should weaken sharply or reorder under a binomial item model. [INFERENCE]
>
> **Residual after null:** it does not. The same ordering survives and the strongest male-residual family is still `space_shape`. [SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_dif_logit_content_summary.tsv`]

- `P(cause)`: `0.81` that the current local `PISA` residual family ordering is a real measurement structure rather than just a linear-model convenience artifact. [INFERENCE]
- `Top alternative`: `0.11` that the pattern is still a byproduct of the current matching-score design and would shrink materially only under full latent-variable multi-group IRT. [INFERENCE]
- `Falsifier`: a stricter invariant-item / multi-group IRT analysis where the current family ordering compresses toward near-zero once latent scoring is purified at the model level. [INFERENCE]
- `Decision impact`: the local measurement branch is now strong enough that the next step should not be another lightweight specification tweak. The next real upgrade is full latent-variable psychometrics or a shift back to the restricted-data frontier. [INFERENCE]
