# IQ Sex Differences - PISA 2018 Fixed-Anchor Purified DIF Pass

**Date:** 2026-03-06  
**Purpose:** test whether the surviving `PISA 2018` content-family geometry still holds when the matching score is rebuilt only from low-DIF anchor items rather than from all non-focal items or plausible values.

This is stronger than the earlier proxy and leave-out passes, but it is still **not** full multi-group IRT or formal iterative purification.

---

## Why This Pass Exists

The current `PISA` branch had already survived two important attacks:

1. plausible-value conditioning [SOURCE: `research/iq-sex-differences-pisa2018-dif-proxy.md`]
2. focal-item / focal-family leave-out matching [SOURCE: `research/iq-sex-differences-pisa2018-dif-leaveout.md`]

The remaining live objection was:

> even the leave-out pass still builds the matching score from the same contaminated item pool, so the residual family ordering might collapse if the match were rebuilt from a narrower low-DIF anchor set. [INFERENCE]

This pass attacks that objection directly.

---

## Method

### Inputs

1. `sources/iq-sex-diff/data/pisa/pisa2018_math_item_extract.parquet`
2. `sources/iq-sex-diff/data/pisa/pisa2018_item_level_gaps.tsv`
3. `sources/iq-sex-diff/data/pisa/pisa2018_unit_framework_proxy.tsv`
4. `sources/iq-sex-diff/data/pisa/pisa2018_item_dif_leaveout.tsv`

### Outputs

1. `sources/iq-sex-diff/data/pisa/pisa2018_item_dif_purified.tsv`
2. `sources/iq-sex-diff/data/pisa/pisa2018_dif_purified_content_summary.tsv`
3. `sources/iq-sex-diff/data/pisa/pisa2018_dif_purified_context_summary.tsv`
4. `sources/iq-sex-diff/data/pisa/pisa2018_dif_purified_anchor_items.tsv`
5. `sources/iq-sex-diff/data/pisa/pisa2018_dif_purified_anchor_gap.tsv`

### Anchor construction

The seed anchor set is taken from the contamination-aware leave-out pass:

1. keep items with `abs(uniform_beta_family_out) <= 0.025`
2. keep items with `abs(nonuniform_beta_family_out) <= 0.015`
3. if that leaves too few items, fall back to the `15` lowest combined DIF-score items

[SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_item_dif_leaveout.tsv`]

In the current run, that yields `23` anchor items:

1. `9` in `change_relationships`
2. `8` in `space_shape`
3. `3` in `quantity`
4. `3` in `uncertainty_data`

[SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_dif_purified_anchor_items.tsv`]

### Matching score

For each focal item:

1. standardize all item scores within country using student weights
2. rebuild the matching score from the anchor items only
3. exclude the focal item if it is itself part of the anchor set
4. standardize that anchor score within country

[INFERENCE]

### Item model

For each scored item:

`item_score ~ female + anchor_score + female*anchor_score + country_FE`

Implementation details:

1. country fixed effects handled by weighted within-country demeaning
2. weighted least squares solved on the demeaned design
3. this pass is coefficient-focused, not inference-focused; it does **not** claim clustered significance testing

[SOURCE: `sources/iq-sex-diff/pisa2018_dif_purification_pass.py`]

---

## Main Results

### 1. The content-family ordering survives the fixed-anchor score

| content family | raw item gap `d` | leave-out family beta | fixed-anchor purified beta |
| --- | ---: | ---: | ---: |
| `space_shape` | `-0.061` | `-0.015` | `-0.017` |
| `change_relationships` | `-0.053` | `-0.010` | `-0.015` |
| `quantity` | `-0.036` | `-0.002` | `-0.010` |
| `uncertainty_data` | `-0.023` | `+0.003` | `-0.003` |

[SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_dif_leaveout_content_summary.tsv`; `sources/iq-sex-diff/data/pisa/pisa2018_dif_purified_content_summary.tsv`]

The main substantive point is simple:

`the residual content-family pattern does not collapse when the match is rebuilt from a narrower low-DIF anchor set`

### 2. The purified anchor score itself is modestly male-leaning

On the fixed-anchor score:

- `female_minus_male_d = -0.060`

[SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_dif_purified_anchor_gap.tsv`]

So the purified score is not neutralized into a female-leaning or null battery by anchor restriction.

### 3. The anchor set is not one-family cherry-picking

The final anchors still span all four content families:

1. `change_relationships = 9`
2. `space_shape = 8`
3. `quantity = 3`
4. `uncertainty_data = 3`

[SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_dif_purified_anchor_items.tsv`]

That does not eliminate all anchor-selection concerns, but it is better than a single-family anchor core.

### 4. The purified pass slightly strengthens, rather than weakens, the male residual ordering

Compared with the leave-out pass:

1. `space_shape` stays the strongest male residual
2. `change_relationships` moves further male
3. `quantity` moves from near parity to modestly male
4. `uncertainty_data` moves from near parity / slight female to slight male

[SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_dif_leaveout_content_summary.tsv`; `sources/iq-sex-diff/data/pisa/pisa2018_dif_purified_content_summary.tsv`]

---

## Best Read

This pass hardens the repo’s `PISA` measurement claim.

What it now says is:

1. the raw male item lean still compresses a lot under ability-conditioning
2. but the surviving content-family geometry does not disappear when the score is rebuilt from a narrower low-DIF anchor core
3. the earlier residual ordering was therefore not just a plausible-value artifact and not just a whole-pool matching artifact

[INFERENCE]

The right interpretation is still narrow:

- this is evidence for a real residual content-family measurement node
- it is **not** proof of psychometric unfairness
- it is **not** full formal DIF
- it is **not** enough on its own to settle any global `g` claim

---

## What Hardens

1. `PISA` residual content-family structure is now harder to dismiss as a matching-surface artifact. [INFERENCE]
2. `space_shape` remains the strongest male-residual content family under every local conditioning scheme tried so far. [SOURCE: `research/iq-sex-differences-pisa2018-framework-proxy.md`; `research/iq-sex-differences-pisa2018-dif-leaveout.md`; `sources/iq-sex-diff/data/pisa/pisa2018_dif_purified_content_summary.tsv`]
3. The repo’s novelty claim improves slightly on the measurement branch: it is no longer just “we saw an item-family pattern,” but “we saw one that survived plausible-value conditioning, leave-out matching, and a fixed-anchor purified score.” [INFERENCE]

## What Remains Open

1. whether full multi-group IRT or iterative purification would shrink the same pattern further
2. whether `TIMSS` shows the same anchor-resistant residual geometry
3. whether process-informed rescoring would move the purified ordering materially

---

## Causal-Check Summary

- `P(cause)`: `0.82` that the `PISA` school-age disagreement contains a real residual content-family measurement node rather than just a contaminated matching-score artifact. [INFERENCE]
- `Top alternative`: `0.10` that a fuller multi-group IRT / invariant-item pass would still flatten the purified family ordering enough to demote it back to a weak secondary effect. [INFERENCE]
- `Falsifier`: a full latent-variable / invariant-item analysis showing the fixed-anchor residual ordering disappears once the battery is purified more rigorously. [INFERENCE]
- `Decision impact`: the measurement branch is now hard enough that the biggest remaining causal bottleneck shifts back toward restricted transcript/process access and mediator identification, not another light `PISA` conditioning tweak. [INFERENCE]

