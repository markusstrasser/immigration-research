# IQ Sex Differences - PISA 2018 Framework-Proxy Pass

**Date:** 2026-03-05
**Purpose:** refine the first `PISA 2018` item/process pass by mapping math units onto the official `PISA` content and context taxonomy at a coarse proxy level.

This is a **framework-proxy** pass, not a final official item-key pass.

---

## Why This Is A Proxy

The local `PISA 2018` codebook and item-level public files are usable, but the OECD cognitive compendium file needed for a cleaner official unit-to-framework crosswalk was blocked at the direct file URL by a Cloudflare challenge. The public first pass therefore stopped at unit labels and process traces.

This pass moves one step further by coding each math unit to the official `PISA` mathematics taxonomy:

1. content:
   - `quantity`
   - `uncertainty_data`
   - `change_relationships`
   - `space_shape`
2. context:
   - `personal`
   - `occupational`
   - `societal`
   - `scientific`

but it does so **from unit labels only**, with explicit confidence flags.

That means:

1. the result is good enough to test whether the item heterogeneity is coherent
2. the result is **not** yet a substitute for a fully official item-framework map

Proxy artifact:

- `sources/iq-sex-diff/data/pisa/pisa2018_unit_framework_proxy.tsv`

Summary outputs:

- `sources/iq-sex-diff/data/pisa/pisa2018_framework_proxy_unit_summary.tsv`
- `sources/iq-sex-diff/data/pisa/pisa2018_framework_proxy_content_summary.tsv`
- `sources/iq-sex-diff/data/pisa/pisa2018_framework_proxy_context_summary.tsv`
- `sources/iq-sex-diff/data/pisa/pisa2018_framework_proxy_content_context_summary.tsv`

---

## Main Results

### 1. `space_shape` is the most male-leaning content family in this proxy pass

Weighted mean item gaps (`d = female - male`):

1. `space_shape`: about `-0.061`
2. `change_relationships`: about `-0.053`
3. `quantity`: about `-0.036`
4. `uncertainty_data`: about `-0.023`

The same ordering survives the medium/high-confidence-only sensitivity pass:

1. `space_shape`: about `-0.065`
2. `change_relationships`: about `-0.051`
3. `quantity`: about `-0.025`
4. `uncertainty_data`: about `-0.023`

So the first coherent content-level footprint is:

- strongest male lean on `space_shape`
- next on `change_relationships`
- weakest male lean on `uncertainty_data`

That is already more informative than the earlier burden-quartile split.

### 2. Context matters too, but less than content

Weighted mean item gaps by proxy context:

1. `occupational`: about `-0.060`
2. `personal`: about `-0.056`
3. `scientific`: about `-0.041` overall and about `-0.019` in the higher-confidence subset
4. `societal`: about `-0.029`

So the current public school-age `PISA` surface looks more male-leaning in the `personal` and `occupational` unit families than in the `societal` or `scientific` families.

### 3. The most male-leaning proxy cell is `space_shape x occupational`

In the proxy cross-classification:

1. `space_shape x occupational` is entirely male-leaning in the current pass (`9/9` items)
2. `space_shape x personal` is also strongly male-leaning (`4/5` items)
3. `uncertainty_data x societal` is much closer to parity
4. `uncertainty_data x scientific` is actually female-leaning, but that cell is one item and should not be over-read

This is the strongest concrete Stage 1 update so far: the heterogeneity is **not** random.

---

## Causal Update

### What hardens

1. `MeasurementSurface` remains first-order.
2. The broad `PISA 2018` male lean is hiding a coherent content-family structure, not just noise.
3. The current local geometry is now more consistent with a school-age split between `space_shape` / some `change_relationships` surfaces and the weaker-gap `uncertainty_data` surfaces.

### What softens

1. The idea that the remaining `PISA` heterogeneity is mostly generic time / visit burden.
2. The idea that broad school-age math disagreement is content-agnostic.

### What remains open

1. whether the proxy map lines up with the fully official compendium once that file is recovered cleanly
2. whether the weaker-gap `uncertainty_data` pattern is the best public school-age analogue of the narrower school-knowledge wedge seen in `NLSY97` and `HSLS`
3. whether `PISA` process variables explain more **within** these content/context families than they did in the aggregate first pass

---

## Best Read

This pass does **not** say girls have an edge on broad school-age math.

It says something narrower and more useful:

1. the broad `PISA 2018` math surface is still male-leaning
2. the item-level heterogeneity is structured
3. the strongest male-leaning block is the proxy `space_shape` family
4. the weakest male-leaning block is the proxy `uncertainty_data` family

That is enough to move the repo from "item heterogeneity exists" to "item heterogeneity has a coherent geometry."

---

## Causal-Check Summary

- `P(cause)`: `0.68` that the school-age measurement disagreement is partly a content-family problem rather than a generic process-burden problem.
- `Top alternative`: the proxy map is misclassifying enough units that the apparent content ordering is partly coding noise.
- `Falsifier`: the official compendium or a stronger item-key showing the same units belong to different framework families and the current ordering collapses.
- `Decision impact`: the next Stage 1 step should be official-compendium recovery or a second proxy coder comparison, not another pooled `PISA` regression.

---

## Outputs

Primary artifacts:

1. `sources/iq-sex-diff/data/pisa/pisa2018_unit_framework_proxy.tsv`
2. `sources/iq-sex-diff/pisa2018_framework_proxy_split.py`
3. `sources/iq-sex-diff/data/pisa/pisa2018_framework_proxy_unit_summary.tsv`
4. `sources/iq-sex-diff/data/pisa/pisa2018_framework_proxy_content_summary.tsv`
5. `sources/iq-sex-diff/data/pisa/pisa2018_framework_proxy_context_summary.tsv`
6. `sources/iq-sex-diff/data/pisa/pisa2018_framework_proxy_content_context_summary.tsv`
