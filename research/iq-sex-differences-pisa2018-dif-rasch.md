# IQ Sex Differences - PISA 2018 Anchored Rasch Sensitivity

**Date:** 2026-03-06  
**Purpose:** test whether the current `PISA 2018` residual content-family ordering survives a more explicit latent-item calibration than the current matching-score and GLM passes.

## Why This Pass Exists

The strongest remaining local objection to the `PISA` branch was:

> the current family ordering survives matching-score and item-model checks, but it might still collapse once item difficulties are calibrated on a latent scale rather than borrowed from a constructed anchor score.

This pass addresses that objection with an anchored Rasch sensitivity. It is **not** a final multi-group IRT solution, because the local package path is unweighted and the booklet-matrix design still matters. [INFERENCE]

## Design

The pass uses:

- binary-scored `PISA 2018` math items only
- separate Rasch `MML` item-difficulty fits for males and females inside each country
- missing responses passed through the package's explicit invalid-response sentinel
- the final iterative low-DIF binary anchor set from the stronger local purification branch
- anchor alignment inside each country by subtracting the mean female-minus-male anchor difficulty difference
- a score-direction contrast defined as:
  - `male_difficulty - female_aligned_difficulty`
  - negative values therefore mean `male-positive` on the repo's existing sign convention

Outputs:

1. `sources/iq-sex-diff/data/pisa/pisa2018_rasch_country_item.tsv`
2. `sources/iq-sex-diff/data/pisa/pisa2018_rasch_item_summary.tsv`
3. `sources/iq-sex-diff/data/pisa/pisa2018_rasch_content_summary.tsv`
4. `sources/iq-sex-diff/data/pisa/pisa2018_rasch_context_summary.tsv`
5. `sources/iq-sex-diff/data/pisa/pisa2018_rasch_country_summary.tsv`
6. `sources/iq-sex-diff/data/pisa/pisa2018_rasch_vs_logit_item_compare.tsv`

[SOURCE: `sources/iq-sex-diff/pisa2018_dif_rasch_pass.py`]

## Main Result

The residual family ordering survives again under the anchored Rasch sensitivity.

Weighted content-family score-direction contrasts:

- `space_shape = -0.138`
- `quantity = -0.092`
- `change_relationships = -0.084`
- `uncertainty_data = -0.046`

[SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_rasch_content_summary.tsv`]

The context ordering also remains structured rather than collapsing:

- `occupational = -0.131`
- `personal = -0.123`
- `scientific = -0.056`
- `societal = -0.039`

[SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_rasch_context_summary.tsv`]

The result is broad rather than being driven by a handful of countries. Example country-level weighted summaries are:

- `SWE = -0.190`
- `ISR = -0.180`
- `ITA = -0.141`
- `ESP = -0.122`

[SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_rasch_country_summary.tsv`]

The item-level pattern also lines up strongly with the earlier weighted binary-logit pass:

- Pearson correlation with prior item-level logit residuals: `0.930`
- Spearman rank correlation: `0.935`

[SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_rasch_vs_logit_item_compare.tsv`]

## What This Means

This is the strongest local `PISA` hardening step so far that still uses only the staged public data. [INFERENCE]

The current family ordering now survives:

1. plausible-value conditioning
2. leave-item / leave-family matching
3. fixed-anchor purification
4. iterative anchor updating
5. weighted binary-logit item modeling
6. unweighted country-specific anchored Rasch calibration

[INFERENCE based on: `research/iq-sex-differences-pisa2018-dif-proxy.md`; `research/iq-sex-differences-pisa2018-dif-leaveout.md`; `research/iq-sex-differences-pisa2018-dif-purified.md`; `research/iq-sex-differences-pisa2018-dif-iterative.md`; `research/iq-sex-differences-pisa2018-dif-logit.md`; `sources/iq-sex-diff/data/pisa/pisa2018_rasch_content_summary.tsv`]

That does **not** mean the repo has finished the measurement branch.

The live limitations are still real:

- the Rasch sensitivity is unweighted
- it is not a joint multi-group calibration
- it does not model booklet assignment explicitly
- it is limited to binary-scored items

[SOURCE: `sources/iq-sex-diff/pisa2018_dif_rasch_pass.py`; INFERENCE]

## Measurement Read

> **Observation:** after separate male/female Rasch calibration within each country and anchor alignment on the low-DIF binary core, the residual family ordering still remains male-leaning, with `space_shape` the strongest family and `uncertainty_data` the weakest. [SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_rasch_content_summary.tsv`]
>
> **Null:** if the earlier `PISA` family ordering were mainly an artifact of the current matching-score construction, it should compress sharply or reorder once item difficulties are estimated on a latent Rasch scale and then aligned through the anchor set. [INFERENCE]
>
> **Residual after null:** it does not. The ordering survives, and the item-level correlation with the earlier logit pass is very high. [SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_rasch_content_summary.tsv`; `sources/iq-sex-diff/data/pisa/pisa2018_rasch_vs_logit_item_compare.tsv`]

- `P(cause)`: `0.85` that the surviving local `PISA` family ordering reflects a real measurement/content structure rather than just the specific earlier matching-score design. [INFERENCE]
- `Top alternative`: `0.10` that the current ordering is still materially distorted by the unweighted country-specific Rasch approximation and would shrink under a weighted joint multi-group IRT with booklet-aware design handling. [INFERENCE]
- `Falsifier`: a weighted multi-group latent-variable analysis where the current family ordering compresses toward zero once the latent scale is identified jointly rather than through separate country/sex fits plus anchor alignment. [INFERENCE]
- `Decision impact`: the local `PISA` measurement branch is now close to saturation on public-use stress tests. The next real upgrades are either weighted multi-group psychometrics or restricted transcript/process access on the broader project tree. [INFERENCE]

## Limits

This pass should be read as a **sensitivity** and not as the final psychometric verdict.

The package route is useful because it gets the repo one honest step closer to latent-item calibration without pretending we already have a full weighted invariant-item pipeline. [INFERENCE]
