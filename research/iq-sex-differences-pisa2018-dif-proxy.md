# IQ Sex Differences - PISA 2018 DIF-Style Proxy Pass

**Date:** 2026-03-06
**Purpose:** move the `PISA 2018` school-age measurement node from raw item-family heterogeneity toward an actual fairness-style conditional item pass.

This is **not** full multi-group IRT. It is a first-pass DIF-style screen using the local public `PISA 2018` item extract and the OECD plausible-value math surface.

---

## Why This Pass Matters

Before this pass, the project had:

1. raw item-gap geometry
2. framework-proxy content-family geometry
3. public item face-validity inspection

What it did **not** have was a conditional item pass answering:

> after conditioning on overall within-country math ability, which item families still show residual sex tilt?

That is the right next question if the project wants to separate:

1. broad score-level sex differences
2. content-family differences
3. possible item-level distortion

---

## Method

### Data

Inputs:

1. `sources/iq-sex-diff/data/pisa/pisa2018_math_item_extract.parquet`
2. `sources/iq-sex-diff/data/pisa/pisa2018_item_level_gaps.tsv`
3. `sources/iq-sex-diff/data/pisa/pisa2018_unit_framework_proxy.tsv`

### Conditioning surface

I used:

`math_avg = mean(PV1MATH ... PV10MATH)`

then standardized that **within country** using student weights:

`math_country_z`

So the comparison is not “girls versus boys in richer or poorer countries,” but:

`female residual at the same relative math level inside country`

### Item model

For each scored math item:

`item_score ~ female + math_country_z + female*math_country_z + country_FE`

Implementation details:

1. country fixed effects were handled by weighted within-country demeaning
2. weighted least squares used `W_FSTUWT`
3. standard errors are cluster-robust by country

Interpretation:

1. `uniform_female_beta` = conditional residual item tilt at the same within-country math level
2. `female*math_country_z` = nonuniform DIF-style proxy

This is a **screen**, not a final latent-trait fairness model. [INFERENCE]

---

## Main Results

### 1. Conditioning compresses the raw content-family gaps sharply

Weighted mean raw item gap versus weighted mean conditioned residual:

| content family | raw item gap `d` | conditioned uniform beta |
| --- | ---: | ---: |
| `space_shape` | `-0.061` | `-0.015` |
| `change_relationships` | `-0.053` | `-0.011` |
| `quantity` | `-0.036` | `-0.006` |
| `uncertainty_data` | `-0.023` | `+0.000` |

So the first decisive update is:

`a large share of the raw PISA item-family gap is ability-surface rather than pure item distortion`

That matters because it softens any claim that raw item geometry alone proves school-age unfairness.

### 2. `space_shape` still has the clearest residual male tilt

Even after conditioning, `space_shape` remains the most male-tilting content family on average:

1. `space_shape`: `-0.015`
2. `change_relationships`: `-0.011`
3. `quantity`: `-0.006`
4. `uncertainty_data`: `~0`

This is smaller than the raw geometry, but it does **not** disappear.

So the content-family ordering survives, just in compressed form.

### 3. `uncertainty_data` is basically neutral on average after conditioning

This is the cleanest family-level result in the pass.

Raw:

- `uncertainty_data = -0.023`

Conditioned:

- `uncertainty_data = +0.000`

That means the weak male tilt on raw data-display items is mostly gone once overall math level is held fixed.

### 4. Residual uniform DIF-style signals are item-specific, not generic

Most male-tilting residual items:

1. `Cash Withdrawal Q01`: `-0.076`
2. `Crazy Ants Q01`: `-0.052`
3. `Chair Lift Q02`: `-0.052`
4. `Running Time Q01`: `-0.050`
5. `Speeding Fines Q03`: `-0.049`
6. `Containers Q01`: `-0.044`
7. `Wooden Train Set Q01`: `-0.041`

Most female-tilting residual items:

1. `Seats in a Theatre Q01`: `+0.060`
2. `Employment Data Q02`: `+0.055`
3. `Part Time Work Q01`: `+0.052`
4. `Medicine doses Q01`: `+0.049`
5. `Carbon Tax Q02`: `+0.045`

These residuals are much narrower than the raw broad score story. They look like localized item-family / format / context effects, not a uniform whole-battery reversal.

### 5. Nonuniform DIF-style effects are mostly small

The nonuniform interaction term is generally weak at the family level:

1. `space_shape`: `+0.001`
2. `quantity`: `+0.001`
3. `change_relationships`: `-0.005`
4. `uncertainty_data`: `-0.005`

The biggest item-level nonuniform signals are still modest. The strongest was:

- `Wooden Train Set Q01`: about `-0.040`

So the current local `PISA` evidence points much more strongly to **uniform residual item-family tilt** than to big sex-by-ability slope reversals.

---

## Best Read

This pass changes the project in a useful way.

Before:

- raw `PISA` item geometry showed structured heterogeneity

Now:

- conditioning on OECD math ability removes a lot of that raw heterogeneity
- but it does **not** remove it all
- the remaining residual structure still points most clearly at `space_shape`
- `uncertainty_data` now looks close to measurement-invariant on average in this first pass

So the right update is:

`the PISA school-age measurement story is not “raw item gaps are fake,” and it is not “PISA is obviously biased.” It is “most raw content-family differences shrink under conditioning, but a smaller residual geometry survives, strongest in space-shape items.”`

---

## What Hardens

1. `MeasurementSurface` remains live, but it now looks more specific.
2. The strongest residual school-age content-family asymmetry is still in `space_shape`.
3. The weakest family after conditioning is `uncertainty_data`, which makes the raw/content split more interpretable.
4. The item-level fairness question should now focus on localized residual clusters, not a generic whole-test indictment.

## What Softens

1. The strongest reading of the raw `PISA` item-gap geometry as evidence of broad item unfairness.
2. The idea that all school-age content families retain equally strong residual sex tilt after ability conditioning.

## What Remains Open

1. whether full multi-group IRT / invariant-item rescoring would compress the residual `space_shape` pattern further
2. whether `TIMSS` shows the same residual family ordering
3. whether the highest-residual items cluster by format in a way the current proxy map is still missing

---

## Anchor Candidates

The pass also produced a first anchor-item list for a later invariant-item proxy score.

Lowest combined uniform + nonuniform residual items in this pass include:

1. `Number Check`
2. `Fence`
3. `Computer Game`
4. `Thermometer Cricket`
5. `Pipelines`

That is useful for Stage `1B`, but not yet decisive by itself because booklet rotation limits anchor coverage. [INFERENCE]

---

## Causal-Check Summary

- `P(cause)`: `0.75` that the school-age `PISA` disagreement is partly a content-family / residual measurement-surface problem rather than a generic process-burden problem or a broad female-favoring math surface.
- `Top alternative`: `0.15` that the surviving residual family pattern would mostly disappear under fuller IRT / invariant-item rescoring.
- `Falsifier`: a stronger latent-DIF pass showing the residual `space_shape` ordering collapses and `uncertainty_data` no longer stays closest to neutrality.
- `Decision impact`: the next measurement-stage move should be either a fuller invariant-item rescore on `PISA` or a parallel `TIMSS` DIF-style pass, not another raw pooled math regression.

---

## Outputs

Primary artifacts:

1. `sources/iq-sex-diff/pisa2018_dif_proxy_pass.py`
2. `sources/iq-sex-diff/data/pisa/pisa2018_item_dif_proxy.tsv`
3. `sources/iq-sex-diff/data/pisa/pisa2018_dif_content_summary.tsv`
4. `sources/iq-sex-diff/data/pisa/pisa2018_dif_context_summary.tsv`
5. `sources/iq-sex-diff/data/pisa/pisa2018_dif_anchor_candidates.tsv`
