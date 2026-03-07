# IQ Sex Differences - PISA 2018 Leave-Out DIF Sensitivity Pass

**Date:** 2026-03-06
**Purpose:** remove the main blind spot in the first `PISA 2018` conditional item pass by rebuilding the matching surface without target-item leakage.

This is still **not** full multi-group IRT. It is a stronger conditional item screen than the first plausible-value proxy because the matching score is rebuilt from the item responses themselves while excluding the focal item or focal family.

---

## Why This Pass Matters

The previous `PISA` conditioning pass was useful, but the review correctly flagged one major weakness:

1. the matching surface used OECD plausible values
2. those plausible values likely contain information from the target items
3. so the residual family ordering could have been partly an artifact of target-item contamination

This pass directly attacks that problem.

---

## Method

### Data

Inputs:

1. `sources/iq-sex-diff/data/pisa/pisa2018_math_item_extract.parquet`
2. `sources/iq-sex-diff/data/pisa/pisa2018_item_level_gaps.tsv`
3. `sources/iq-sex-diff/data/pisa/pisa2018_unit_framework_proxy.tsv`

Outputs:

1. `sources/iq-sex-diff/data/pisa/pisa2018_item_dif_leaveout.tsv`
2. `sources/iq-sex-diff/data/pisa/pisa2018_dif_leaveout_content_summary.tsv`
3. `sources/iq-sex-diff/data/pisa/pisa2018_dif_leaveout_context_summary.tsv`
4. `sources/iq-sex-diff/data/pisa/pisa2018_dif_leaveout_anchor_candidates.tsv`

Script:

1. `sources/iq-sex-diff/pisa2018_dif_leaveout_pass.py`

### Matching surfaces

For each scored math item:

1. standardize every item within country using student weights
2. build an `item-out` matching score:
   - average of all other observed item `z` scores excluding the focal item
3. build a `family-out` matching score:
   - average of all other observed item `z` scores excluding every item from the focal content family

So the new comparison is:

`female residual at the same within-country level on all other math items, excluding the focal source of contamination`

### Item model

For each scored math item:

`item_score ~ female + match_score + female*match_score + country_FE`

Implementation details:

1. country fixed effects handled by weighted within-country demeaning
2. weighted least squares used `W_FSTUWT`
3. standard errors are cluster-robust by country
4. a response-time sensitivity pass also trims the bottom item-specific time decile before refitting the `family-out` model

Interpretation:

1. `uniform_beta_item_out` = residual item tilt after excluding the focal item from the matching surface
2. `uniform_beta_family_out` = residual item tilt after excluding the full focal content family
3. `uniform_beta_family_out_trimmed` = same residual after rough low-time trimming

---

## Main Results

### 1. The residual family ordering survives the contamination fix

Weighted mean raw item gap versus new leave-out residuals:

| content family | raw item gap `d` | item-out beta | family-out beta | family-out trimmed |
| --- | ---: | ---: | ---: | ---: |
| `space_shape` | `-0.061` | `-0.012` | `-0.015` | `-0.018` |
| `change_relationships` | `-0.053` | `-0.009` | `-0.010` | `-0.014` |
| `quantity` | `-0.036` | `-0.003` | `-0.002` | `-0.007` |
| `uncertainty_data` | `-0.023` | `+0.002` | `+0.003` | `-0.002` |

So the main update is:

`the old residual family ordering was not mostly a plausible-value mirage`

The contamination-free pass lands very close to the original proxy summary.

### 2. `space_shape` still has the clearest residual male tilt

The core ordering stays the same:

1. `space_shape` remains the strongest male-residual family
2. `change_relationships` remains next
3. `quantity` weakens substantially toward parity
4. `uncertainty_data` remains the closest to parity

That is true under:

1. focal-item exclusion
2. full-family exclusion
3. rough low-time trimming

### 3. The residual pattern is not just a generic response-time artifact

The rough low-time trimming does not erase the family ordering. If anything, the trimmed pass moves most families a little further male:

1. `space_shape`: `-0.018`
2. `change_relationships`: `-0.014`
3. `quantity`: `-0.007`
4. `uncertainty_data`: `-0.002`

That is not a clean rapid-guess design, but it is enough to weaken the strongest “this is mostly low-time response noise” story.

### 4. The item-level residuals stay localized, not whole-test

Most male-residual items under the `family-out` pass include:

1. `Cash Withdrawal Q01`: `-0.074`
2. `Crazy Ants Q01`: `-0.056`
3. `Chair Lift Q02`: `-0.048`
4. `Speeding Fines Q03`: `-0.046`
5. `Running Time Q01`: `-0.046`
6. `Wooden Train Set Q01`: `-0.045`
7. `Containers Q01`: `-0.041`

Most female-residual items include:

1. `Employment Data Q02`: `+0.060`
2. `Seats in a Theatre Q01`: `+0.059`
3. `Medicine doses Q01`: `+0.058`
4. `Carbon Tax Q02`: `+0.047`
5. `Part Time Work Q01`: `+0.047`

So the improved pass still points to localized residual clusters rather than a uniform whole-battery reversal.

---

## Best Read

The main blind spot in the old `PISA` proxy pass is now materially reduced.

The strongest current read is:

1. much of the raw `PISA` item geometry still compresses once ability is held fixed
2. the residual geometry survives even when the matching score excludes the focal item or focal family
3. `space_shape` remains the clearest male-residual family
4. `uncertainty_data` remains the closest to parity
5. the next step is no longer “prove the proxy is not contaminated”; it is “decide whether a formal IRT / invariant-item pass is worth the marginal gain”

So the right update is:

`the residual PISA family pattern is now better supported than it was after the review, though it is still not identical to full formal DIF`

---

## What Hardens

1. the school-age measurement node still contains real content-family structure after a contamination-aware sensitivity pass
2. `space_shape` remains the strongest male-residual family in the local `PISA` battery
3. the old residual ordering was not mainly an artifact of conditioning on plausible values

## What Softens

1. the strongest review claim that the first `PISA` pass might be mostly a matching-surface artifact
2. the idea that the residual ordering would likely collapse once the target-item contamination was removed

## What Remains Open

1. whether full multi-group IRT or invariant-item rescoring would shrink the same pattern further
2. whether `TIMSS` shows the same contamination-resistant residual ordering
3. whether the surviving residual items cluster by format in a way the current proxy framework still misses

---

## Causal-Check Summary

- `P(cause)`: `0.78` that the `PISA` school-age disagreement contains a real residual content-family measurement node, not just a raw-score or plausible-value artifact.
- `Top alternative`: `0.12` that a fuller IRT or invariant-item pass would compress the residual ordering enough to demote it back to a weak secondary effect.
- `Falsifier`: a formal anchor-item or multi-group IRT pass showing the same ordering disappears once latent scoring is purified more rigorously.
- `Decision impact`: the top `PISA` blind spot is no longer the matching-surface contamination. The highest-value next move shifts back toward the late-school transcript wedge unless a publication-grade fairness pass is needed.
