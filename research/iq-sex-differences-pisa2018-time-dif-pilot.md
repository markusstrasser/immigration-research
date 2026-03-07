# IQ Sex Differences - PISA 2018 Response-Time DIF Pilot

**Date:** 2026-03-06
**Purpose:** test whether the surviving `PISA 2018` score-residual geometry is mirrored by a same-ability response-time geometry.

This is a pilot, not a full response-time DIF paper.

Companion files:

- `research/iq-sex-differences-pisa2018-process-nuisance.md`
- `research/iq-sex-differences-pisa2018-dif-leaveout.md`
- `research/iq-sex-differences-next-level-research-plan.md`

---

## Question

After the leave-out accuracy match, do girls and boys spend systematically different amounts of time on the same items at the same non-focal math level?

And if so:

> does that time geometry line up with the residual score geometry?

That is the useful measurement question here. [INFERENCE]

---

## DAG Discipline

This is another diagnostic measurement model, not a causal total-effect estimate.

The relevant graph is:

```text
Sex -> response-time style
Sex -> latent domain
Latent domain -> focal item score
Latent domain -> focal item time
Latent domain -> non-focal accuracy match
Item design -> focal item time
Item design -> focal item score
```

So the pilot asks:

1. conditional on a non-focal accuracy surface
2. within country
3. is there a residual sex difference in focal log-response time?

It does **not** identify whether that time difference is ability, strategy, caution, interface burden, or fairness. [INFERENCE]

---

## Method

### Inputs

1. `sources/iq-sex-diff/data/pisa/pisa2018_math_item_extract.parquet`
2. `sources/iq-sex-diff/data/pisa/pisa2018_item_level_gaps.tsv`
3. `sources/iq-sex-diff/data/pisa/pisa2018_unit_framework_proxy.tsv`
4. `sources/iq-sex-diff/data/pisa/pisa2018_process_nuisance_item.tsv`

### Script

1. `sources/iq-sex-diff/pisa2018_time_dif_pass.py`

### Outputs

1. `sources/iq-sex-diff/data/pisa/pisa2018_time_dif_item.tsv`
2. `sources/iq-sex-diff/data/pisa/pisa2018_time_dif_content_summary.tsv`
3. `sources/iq-sex-diff/data/pisa/pisa2018_time_dif_context_summary.tsv`
4. `sources/iq-sex-diff/data/pisa/pisa2018_time_dif_score_time_relation.tsv`

### Model

For each item with a focal `TT` field:

`log_time ~ female + nonfocal_family_accuracy + female*nonfocal_family_accuracy + country_FE`

where the non-focal-family accuracy match is the same leave-out style surface used in the score pass.

This is intentionally close to the recent response-time DIF literature in spirit, but it is still a local pilot rather than a formal log-normal response-time DIF framework. [SOURCE: https://link.springer.com/article/10.1186/s40536-026-00290-1]

---

## Main Results

### 1. Girls are slower on most items even after the non-focal accuracy match

Weighted average female time residual by content family:

| family | weighted female time beta | female-slower items | male-slower items |
| --- | ---: | ---: | ---: |
| `quantity` | `+0.104` | `10` | `0` |
| `change_relationships` | `+0.096` | `21` | `3` |
| `uncertainty_data` | `+0.085` | `10` | `0` |
| `space_shape` | `+0.070` | `16` | `0` |

Overall weighted mean female time residual:

1. `+0.0878`

That is a broad pattern, not a niche cluster. On this pilot, girls are slower on `57/60` scored math items after the non-focal accuracy match. [SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_time_dif_content_summary.tsv`; `sources/iq-sex-diff/data/pisa/pisa2018_time_dif_item.tsv`]

### 2. The time geometry is broader than the score geometry

The score-residual pass was localized:

1. strongest male score residual in `space_shape`
2. then `change_relationships`
3. weaker in `quantity`
4. near parity in `uncertainty_data`

The time pilot is different:

1. female residual time is positive in **every** content family
2. the family spread is much narrower
3. the pattern is broad rather than localized

So the broad time footprint and the localized score footprint are not the same object. [INFERENCE]

### 3. Score residuals and time residuals align weakly and in the opposite direction

Item-level relation between:

1. `female_time_beta`
2. `uniform_beta_process` from the score-residual prototype

Results:

1. Pearson correlation: `-0.155`
2. sign agreement rate: `0.333`

That means:

1. items with bigger female time residuals are not the same items with female score residuals
2. the weak relationship actually tilts the other way:
   - broader female-slower time
   - more localized male score residual

[SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_time_dif_score_time_relation.tsv`]

### 4. The largest female-slower items are not confined to one family

Examples:

1. `Speeding Fines Q02` `+0.218`
2. `Cash Withdrawal Q02` `+0.197`
3. `Medicine doses Q04` `+0.188`
4. `Chair Lift Q02` `+0.166`
5. `Stop The Car Q01` `+0.162`

The broad spread reinforces the same point:

`response-time residuals look much more global than score residuals`

[SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_time_dif_item.tsv`]

---

## Best Read

This pilot supports a more specific measurement story:

1. there is a broad female-slower response-time residual on `PISA 2018` math
2. but that broad time residual does **not** map tightly onto the localized score-residual family ordering
3. therefore the current score geometry is unlikely to be explained by a single generic timing story

The cleanest interpretation is:

`timing differences look broad; score differences look family-structured`

That makes a pure generic speed explanation too weak. [INFERENCE]

---

## What Hardens

1. a broad same-ability response-time difference exists on the local `PISA` math surface
2. the score-residual content-family pattern is not just a restatement of that broad time pattern
3. `space_shape` remains special on score geometry even though time geometry is more diffuse

---

## What Softens

1. the idea that the residual score family ordering is mostly the direct consequence of a single generic female-slower timing effect
2. the idea that time geometry and score geometry are just two views of the same latent measurement distortion

---

## What Remains Open

1. whether a formal response-time DIF model would show stronger family structure than this pilot
2. whether time residuals become more informative once visits/actions are modeled jointly
3. whether the same broad-female-slower but localized-male-score pattern appears on `TIMSS`

---

## Causal-Check Summary

- `P(cause)`: `0.71` that the `PISA` timing story is broad and partly orthogonal to the localized score-residual content-family story, rather than being the single main cause of it.
- `Top alternative`: `0.19` that a fuller response-time DIF model would reveal stronger score-time alignment than this simple pilot detects.
- `Falsifier`: a formal response-time DIF pass showing that the same item families driving male score residuals also drive the strongest same-ability time residuals in a consistent direction.
- `Decision impact`: the next serious measurement step should treat timing as one process layer among several, not as the master explanation of the surviving score geometry.

