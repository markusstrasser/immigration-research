# IQ Sex Differences - PISA 2018 Theta-Conditioned Response-Time DIF

**Date:** 2026-03-07  
**Purpose:** upgrade the earlier `PISA 2018` response-time pilot by conditioning on the strongest current local latent anchor surface instead of the older non-focal accuracy match.

## Why This Pass Exists

The earlier timing pilot already suggested:

- broad female-slower timing exists
- that broad timing pattern does not line up tightly with the localized score-family ordering

But that pilot still used a weaker matching surface. [SOURCE: `research/iq-sex-differences-pisa2018-time-dif-pilot.md`]

This pass asks the cleaner question:

> after conditioning on the same Rasch-based anchor `theta` that now hardens the score branch, does the timing result change enough to rescue a generic timing explanation?

[INFERENCE]

## Design

The pass uses:

- the same binary anchor core from the iterative `PISA` branch
- combined-sex country-specific Rasch anchor estimation
- anchor-based `theta` from `ability_eap`
- leave-one-out `theta` for focal anchor items
- weighted item-level time models:
  - `log_time ~ female + theta + female*theta + country_FE`

Outputs:

1. `sources/iq-sex-diff/data/pisa/pisa2018_time_theta_anchor_gap.tsv`
2. `sources/iq-sex-diff/data/pisa/pisa2018_time_dif_theta_item.tsv`
3. `sources/iq-sex-diff/data/pisa/pisa2018_time_dif_theta_content_summary.tsv`
4. `sources/iq-sex-diff/data/pisa/pisa2018_time_dif_theta_context_summary.tsv`
5. `sources/iq-sex-diff/data/pisa/pisa2018_time_dif_theta_score_time_relation.tsv`

[SOURCE: `sources/iq-sex-diff/pisa2018_time_dif_theta_pass.py`]

## Main Result

The broad female-slower timing pattern survives, and the weak score-time alignment survives too.

Weighted female time residuals by content family:

- `quantity = +0.102`
- `change_relationships = +0.088`
- `uncertainty_data = +0.084`
- `space_shape = +0.066`

[SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_time_dif_theta_content_summary.tsv`]

Item counts:

- girls are slower on `57/59` items
- every content family stays net female-slower

[SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_time_dif_theta_content_summary.tsv`; `sources/iq-sex-diff/data/pisa/pisa2018_time_dif_theta_item.tsv`]

The anchor `theta` gap itself is again near parity:

- `female_minus_male_d = -0.012`

[SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_time_theta_anchor_gap.tsv`]

And the score-time alignment stays weak:

- correlation between `female_theta_time_beta` and `uniform_theta_logit_beta` = `-0.076`
- sign-agreement rate = `0.305`

[SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_time_dif_theta_score_time_relation.tsv`]

## What This Means

This is the strongest local timing check so far because it uses the same latent anchor surface that now supports the strongest score pass. [INFERENCE]

The result still does **not** support a single generic timing explanation of the score-family ordering.

The geometry remains:

- time residuals are broad and mostly positive for girls
- score residuals are localized and male-leaning mainly in specific content families

[INFERENCE based on: `sources/iq-sex-diff/data/pisa/pisa2018_time_dif_theta_content_summary.tsv`; `sources/iq-sex-diff/data/pisa/pisa2018_dif_theta_logit_content_summary.tsv`]

So the repo can now say this more confidently:

> broad same-ability female-slower timing is real on the local `PISA` surface, but it does not explain the localized male score-residual family ordering.

[INFERENCE]

## Measurement Read

> **Observation:** after conditioning response time on the strongest current local latent anchor `theta`, girls still look broadly slower across nearly all items, but the item-level relationship between time residuals and score residuals remains weak and negative. [SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_time_dif_theta_content_summary.tsv`; `sources/iq-sex-diff/data/pisa/pisa2018_time_dif_theta_score_time_relation.tsv`]
>
> **Null:** if a generic timing burden were the main explanation of the current score-family ordering, strengthening the matching surface to latent anchor `theta` should make the score-time relation stronger and more coherent. [INFERENCE]
>
> **Residual after null:** it does not. The broad female-slower timing footprint remains, but the score-time relation is still weak and in the opposite direction (`r = -0.076`). [SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_time_dif_theta_score_time_relation.tsv`]

- `P(cause)`: `0.78` that broad timing/style differences are a real process layer on `PISA` math, but not the main driver of the localized score-family ordering. [INFERENCE]
- `Top alternative`: `0.14` that a fuller response-time DIF model jointly using times, visits, and latent speed would reveal stronger family-specific score-time alignment than this hybrid pass detects. [INFERENCE]
- `Falsifier`: a formal response-time DIF or nuisance-trait process model showing that the same content families driving male score residuals also drive the strongest same-ability time residuals in a consistent direction. [INFERENCE]
- `Decision impact`: the local process branch is now close to saturation too. The next meaningful measurement move is a full response-time / process-data model or a pivot back to the restricted-data frontier. [INFERENCE]

## Limits

This is still a hybrid pass:

- unweighted Rasch anchor estimation
- weighted time regression in a separate stage
- no explicit latent-speed model
- no joint modeling of time and visits

[SOURCE: `sources/iq-sex-diff/pisa2018_time_dif_theta_pass.py`; INFERENCE]
