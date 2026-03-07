# IQ Sex Differences - PISA 2018 Item And Process First Pass

**Date:** 2026-03-05
**Purpose:** first public school-age item-level pass on `PISA 2018` mathematics using the local `SPSS` bundles plus the official OECD codebook.

This pass is designed to attack the `MeasurementSurface` node first, not to settle latent-trait claims.

---

## Data Surface

Local inputs:

1. `sources/iq-sex-diff/data/pisa/SPSS_STU_QQQ.zip`
2. `sources/iq-sex-diff/data/pisa/SPSS_STU_COG.zip`
3. `sources/iq-sex-diff/data/pisa/SPSS_STU_TTM.zip`
4. `sources/iq-sex-diff/data/pisa/docs/PISA2018_CODEBOOK.xlsx`

Notable data note:

- the OECD codebook downloaded cleanly and was used for the item metadata
- the cognitive compendium link that surfaced from the OECD page returned HTML rather than the archive, so this pass uses the official codebook and variable labels rather than a fuller item-framework crosswalk

That matters because this is a **response-process and item-surface first pass**, not yet the final process/content/context decomposition.

---

## Analytic Surface

The key discovery from the official codebook is that:

- `CM...` variables are the mathematics cognitive namespace in `PISA 2018`
- the local math-item surface contains `60` scored math items
- the item/process merge yields `551,928` respondents across `71` countries
- the actual math-item process subset is `266,271` respondents with at least one observed math item

The first pass uses:

1. overall math plausible values from `PV1MATH` to `PV10MATH`
2. scored item responses `CM...S`
3. total time `CM...TT`
4. total visits `CM...V`

All descriptive item gaps use the project sign convention:

`d = female - male`

and item summaries are aggregated as country-weighted within-item gaps, not as raw pooled item means only.

---

## Main Results

### 1. Broad `PISA 2018` math is male-leaning

In the math-item subset with country fixed effects:

- base model: female coefficient `-0.048`
- process-stress model: female coefficient `-0.073`

Source table:

- `sources/iq-sex-diff/data/pisa/pisa2018_item_models.tsv`

Interpretation:

- the broad public `PISA 2018` math surface is male-leaning in this first pass
- the larger male lean in the process-stress model is **not** causal evidence, because item count, time, and visits are score-generation descendants
- it is only a fragility / process-surface warning

### 2. The item surface is heterogeneous, but mostly male-leaning

Across the `60` math items:

- `43` are male-leaning
- `17` are female-leaning
- mean country-weighted item gap is about `-0.048`

Source table:

- `sources/iq-sex-diff/data/pisa/pisa2018_item_level_gaps.tsv`

This hardens the claim that broad `PISA 2018` math is not hiding a general female edge.

### 3. Female-positive items do exist, but they do not cluster in a trivial burden family

Strongest female-positive items in this first pass:

1. `Employment Data - Q02`
2. `Medicine doses - Q01`
3. `Carbon Tax - Q02`
4. `Part Time Work - Q01`

Strongest male-positive items:

1. `Cash Withdrawal - Q01`
2. `Wooden Train Set - Q01`
3. `Speeding Fines - Q03`
4. `Racing - Q02`

This matters because the disagreement is not being created by one generic process class.

### 4. Burden quartiles are not the main story

By burden quartile, mean item gaps are:

- `q1_low`: `-0.057`
- `q2_midlow`: `-0.023`
- `q3_midhigh`: `-0.067`
- `q4_high`: `-0.043`

The correlation between item sex gap and:

- female-minus-male time gap is about `-0.09`
- female-minus-male visit gap is about `-0.09`

So the first public process pass does **not** support a simple story that female-positive items are just the higher-time or higher-visit items.

Source tables:

- `sources/iq-sex-diff/data/pisa/pisa2018_item_family_gaps.tsv`
- `sources/iq-sex-diff/data/pisa/pisa2018_process_gaps.tsv`

---

## Causal Update

### What hardens

1. `MeasurementSurface` remains first-order.
2. The broad school-age math surface can still conceal strong item-level heterogeneity.
3. A generic "timing / visits explains the female-tilting surfaces" story is too weak after this pass.

### What softens

1. The idea that `PISA 2018` is likely to reveal a broad female-leaning school-age math surface.
2. The idea that simple process burden by itself explains the school-surface disagreement.

### What remains open

1. whether the female-positive `PISA` items line up with official math framework categories such as content / process / context
2. whether those female-positive item families align with the `NLSY97 Math Knowledge` wedge and the `TIMSS knowing` shift

That is the real next step. This pass has narrowed the target enough to make a framework-linked item map worth the effort.

---

## Causal-Check Summary

- `P(cause)`: `0.60` that school-age math disagreement still lives mainly in item-family and measurement-surface heterogeneity rather than in a broad latent female edge.
- `Top alternative`: a narrower school-knowledge / curriculum family that the current first-pass burden summaries do not isolate yet.
- `Falsifier`: official-framework mapping showing female-positive items are not concentrated in any coherent school-knowledge or format family.
- `Decision impact`: move next to framework-linked item classification, not another pooled school-math regression.

---

## Outputs

Primary artifacts:

1. `sources/iq-sex-diff/pisa2018_item_split.py`
2. `sources/iq-sex-diff/data/pisa/pisa2018_math_item_extract.parquet`
3. `sources/iq-sex-diff/data/pisa/pisa2018_item_level_gaps.tsv`
4. `sources/iq-sex-diff/data/pisa/pisa2018_item_family_gaps.tsv`
5. `sources/iq-sex-diff/data/pisa/pisa2018_process_gaps.tsv`
6. `sources/iq-sex-diff/data/pisa/pisa2018_item_models.tsv`
