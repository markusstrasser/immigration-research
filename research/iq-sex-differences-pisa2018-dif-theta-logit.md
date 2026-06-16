# IQ Sex Differences - PISA 2018 Latent-Theta DIF Pass

**Date:** 2026-03-07  
**Purpose:** replace the earlier hand-built binary anchor average with a latent anchor-based `theta` and check whether the current `PISA 2018` residual family ordering still survives.

## Why This Pass Exists

After the weighted binary-logit pass and the anchored-Rasch sensitivity, the remaining reasonable objection was:

> the current family ordering might still depend on a constructed matching score rather than on a latent ability estimate from the anchor items themselves.

This pass answers that objection with the smallest honest upgrade:

- fit a combined-sex Rasch model on the binary anchor core inside each country
- estimate anchor-based `theta` for every student from that Rasch model
- use leave-one-out `theta` for focal anchor items
- fit the same weighted binomial DIF model on that latent `theta`

This is still not full weighted joint multi-group IRT. It is the strongest local hybrid pass the current public stack supports without pretending the tooling is richer than it is. [INFERENCE]

## Design

The pass uses:

- binary-scored `PISA 2018` math items only
- the final iterative low-DIF binary anchor set
- a combined-sex Rasch `MML` fit inside each country on the anchor items
- anchor-based `theta` from `ability_eap`
- weighted binomial GLMs with:
  - `female`
  - latent anchor `theta`
  - `female * theta`
  - country fixed effects

Outputs:

1. `sources/iq-sex-diff/data/pisa/pisa2018_theta_anchor_gap.tsv`
2. `sources/iq-sex-diff/data/pisa/pisa2018_item_dif_theta_logit.tsv`
3. `sources/iq-sex-diff/data/pisa/pisa2018_dif_theta_logit_content_summary.tsv`
4. `sources/iq-sex-diff/data/pisa/pisa2018_dif_theta_logit_context_summary.tsv`
5. `sources/iq-sex-diff/data/pisa/pisa2018_theta_logit_vs_prior_compare.tsv`

[SOURCE: `sources/iq-sex-diff/pisa2018_dif_theta_logit_pass.py`]

## Main Result

The latent-`theta` pass keeps the same ordering again.

Weighted uniform residuals:

- `space_shape = -0.141`
- `change_relationships = -0.099`
- `quantity = -0.085`
- `uncertainty_data = -0.024`

[SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_dif_theta_logit_content_summary.tsv`]

The anchor-based latent score itself is again near parity:

- `female_minus_male_d = -0.012`

[SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_theta_anchor_gap.tsv`]

And the item-level pattern is almost identical to the earlier weighted logit pass:

- correlation with prior weighted logit residuals: `0.991`
- correlation with the country-aggregated Rasch item summary: `0.939`

[SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_theta_logit_vs_prior_compare.tsv`]

## What This Means

This is the cleanest local answer to the “matching-score artifact” objection so far. [INFERENCE]

The `PISA` family ordering now survives:

1. plausible-value conditioning
2. leave-item / leave-family matching
3. fixed-anchor purification
4. iterative anchor updating
5. weighted binary logit on a leave-one-out anchor score
6. anchored Rasch sensitivity on item difficulties
7. weighted binary logit on latent anchor `theta`

[INFERENCE based on: `research/iq-sex-differences-pisa2018-dif-proxy.md`; `research/iq-sex-differences-pisa2018-dif-leaveout.md`; `research/iq-sex-differences-pisa2018-dif-purified.md`; `research/iq-sex-differences-pisa2018-dif-iterative.md`; `research/iq-sex-differences-pisa2018-dif-logit.md`; `research/iq-sex-differences-pisa2018-dif-rasch.md`; `sources/iq-sex-diff/data/pisa/pisa2018_dif_theta_logit_content_summary.tsv`]

The measurement branch is therefore very hard to dismiss as:

- a plausible-value artifact
- a whole-pool matching artifact
- a simple male-anchor artifact
- a linear-model artifact
- a hand-built total-score artifact

[INFERENCE]

## Measurement Read

> **Observation:** after replacing the constructed matching score with a latent anchor-based `theta`, the same residual family ordering still survives and the item-level agreement with the prior weighted logit pass is almost perfect. [SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_dif_theta_logit_content_summary.tsv`; `sources/iq-sex-diff/data/pisa/pisa2018_theta_logit_vs_prior_compare.tsv`]
>
> **Null:** if the current local `PISA` family ordering were mainly an artifact of the earlier matching-score construction, it should weaken or reorder once the conditioning surface becomes latent anchor `theta` rather than a hand-built anchor average. [INFERENCE]
>
> **Residual after null:** it does not. `space_shape` remains strongest male, `uncertainty_data` remains closest to parity, and the item-level correlation with the prior weighted logit pass is `0.991`. [SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_dif_theta_logit_content_summary.tsv`; `sources/iq-sex-diff/data/pisa/pisa2018_theta_logit_vs_prior_compare.tsv`]

- `P(cause)`: `0.88` that the current local `PISA` family ordering reflects a real residual measurement/content structure rather than the specific earlier matching-score design. [INFERENCE]
- `Top alternative`: `0.08` that the ordering is still materially shaped by the hybrid estimation strategy and would compress under a truly weighted joint multi-group latent-variable analysis. [INFERENCE]
- `Falsifier`: a weighted joint multi-group IRT / invariant-item analysis where the current family ordering compresses sharply once the latent scale is identified in one joint model rather than through country-wise anchor Rasch plus weighted logistic DIF. [INFERENCE]
- `Decision impact`: the public `PISA` branch is now close to saturation. The next meaningful local psychometric step is true weighted joint multi-group modeling, not more proxy or wrapper changes. [INFERENCE]

## Limits

This is still a hybrid rather than a final IRT solution:

- the anchor Rasch fit is unweighted
- the latent score is estimated country by country
- the focal DIF model is weighted but not joint with the Rasch estimation
- the pass remains limited to binary items

[SOURCE: `sources/iq-sex-diff/pisa2018_dif_theta_logit_pass.py`; INFERENCE]
