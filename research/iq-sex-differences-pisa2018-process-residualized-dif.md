# PISA 2018 Process-DIF Reduction With Ability-Residualized Public Process Traits

## Why this pass exists

Earlier `PISA` process passes showed two things:

1. girls are broadly slower on most math items
2. that broad timing pattern does not line up tightly with the localized residual score geometry

The remaining open question was whether the public `TT` / `V` process variables could still reduce score-side differential item functioning once the process terms were stripped of obvious ability signal.

This pass implements the best feasible public-data approximation:

- low-DIF anchor `theta`
- non-focal process metrics only
- ability-residualized process traits within country
- weighted focal-item logit models

This is a stronger test than the earlier crude process-style pass because it is trying to remove the part of process variation that just proxies for ability. It is still not a full joint score-time multigroup model.  
[SOURCE: https://www.cambridge.org/core/services/aop-cambridge-core/content/view/69A15CC6FFB38BDCB1F9C0FBDE550A6D/S0033312325100720a.pdf/div-class-title-reducing-differential-item-functioning-via-process-data-div.pdf]  
[SOURCE: https://webfs.oecd.org/pisa2018/index.html#_Toc14472]

## Data and method

Inputs:

- public `PISA 2018` math item extract
- iterative low-DIF anchor list from the local purification branch
- public item-level `TT` total time and `V` visit counts
- country weights `W_FSTUWT`

For each focal item:

1. build a low-DIF anchor `theta`
2. residualize non-focal process variables on anchor `theta` within country
3. aggregate the residualized non-focal process surface into:
   - residual time mean
   - residual time SD
   - residual visit mean
   - residual revisit mean
   - residual response breadth
4. fit weighted score DIF models with and without those residualized process terms

This is the local script:

- [pisa2018_process_residualized_dif_pass.py](/Users/alien/Projects/research/sources/iq-sex-diff/pisa2018_process_residualized_dif_pass.py)

Main outputs:

- [pisa2018_process_residualized_item.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/pisa/pisa2018_process_residualized_item.tsv)
- [pisa2018_process_residualized_content_summary.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/pisa/pisa2018_process_residualized_content_summary.tsv)
- [pisa2018_process_residualized_context_summary.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/pisa/pisa2018_process_residualized_context_summary.tsv)
- [pisa2018_process_residualized_vs_theta_compare.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/pisa/pisa2018_process_residualized_vs_theta_compare.tsv)

## Main result

The stronger residualized process block still does **not** reduce the residual content-family geometry in a coherent way.

Weighted family summaries:

| family | base | process-residualized | weighted abs reduction |
|---|---:|---:|---:|
| `space_shape` | `-0.140` | `-0.198` | `-0.076` |
| `change_relationships` | `-0.100` | `-0.177` | `-0.046` |
| `quantity` | `-0.084` | `-0.159` | `-0.046` |
| `uncertainty_data` | `-0.024` | `-0.205` | `-0.098` |

Across all `59` binary items:

- items with smaller absolute female coefficient after residualized process adjustment: `24`
- items with larger absolute female coefficient after residualized process adjustment: `35`
- mean absolute-gap reduction: `-0.0659`

So the residualized block is slightly less damaging than the earlier non-residualized rich block, but it still does not produce net DIF reduction.

## Comparison to the earlier non-residualized rich pass

The earlier rich pass mostly made the residual male pattern stronger because the added process block still carried ability signal. The residualized version improves that only marginally:

| family | rich process beta | residualized process beta |
|---|---:|---:|
| `space_shape` | `-0.210` | `-0.198` |
| `change_relationships` | `-0.183` | `-0.177` |
| `quantity` | `-0.172` | `-0.159` |
| `uncertainty_data` | `-0.203` | `-0.205` |

So residualization helped at the margin, but not enough to change the branch-level interpretation.

## Item-level nuance

This is not a claim that process variables are useless at the item level.

Some focal items did shrink materially once the residualized nuisance traits were added:

- `CM939Q02S`: `-0.275 -> -0.081`
- `CM961Q03S`: `-0.235 -> -0.070`
- `CM905Q01S`: `-0.288 -> -0.129`
- `CM982Q02S`: `+0.329 -> +0.203`

But the shrinkage is not coherent enough across items or families to support the stronger claim:

> public `TT/V` process data explain the residual score-side family ordering

The data do not support that claim.

## Interpretation

Current best read:

1. broad same-ability timing/process differences are real
2. public `TT/V` process summaries do contain some local explanatory signal
3. but public `TT/V` alone are too thin to reduce the residual score-side family geometry in a stable way

That points to a real methodological wall:

- process-based DIF reduction looks promising in the recent methods literature
- but the public `PISA` process surface is much thinner than the richer log data those approaches would ideally want

So the right update is not “process data don’t matter.” It is:

> with public `PISA 2018` `TT/V` only, process-based DIF reduction does not yet overturn the residual content-family pattern.

## Causal / epistemic update

`Observation:` residualized non-focal process traits do not coherently compress the residual family ordering.  
`Null:` the earlier process failure was mainly because the process block still contained ability signal.  
`Residual:` ability leakage was part of the problem, but removing it is still not enough with public `TT/V`.

Current lean:

- `P(cause) = 0.65` that the residual score-family geometry is not reducible to public `TT/V` process style alone
- `Top alternative = 0.20` that a richer confidential process-log representation would reduce more of it
- `Falsifier:` a full log-based nuisance-trait reduction on confidential `PISA` process data that materially compresses the family ordering

## Decision impact

This public branch is close to saturation.

What should not happen next:

- more light `PISA` process regressions with the same `TT/V` surface
- more generic timing narratives

What should happen next if this branch is pursued further:

1. richer confidential process logs
2. heavier joint score-time latent modeling
3. direct experiments on item timing and design

Without one of those, the next pass is likely to be more polishing than uncertainty reduction.
