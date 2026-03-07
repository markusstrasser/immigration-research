# IQ Sex Differences - NLSCYA Early-School First Pass

**Date:** 2026-03-05
**Purpose:** first local early-school-emergence pass using the public `NLSCYA` child supplement, after widening the intake map to include `PIAT Math` standard scores.

This is the first empirical Stage 2 result. It is useful, but it is not the final early-school adjudication.

---

## Data Surface

Local inputs:

1. `sources/iq-sex-diff/data/nlscya/nlscya_all_1979-2020.zip`
2. `sources/iq-sex-diff/data/nlscya/nlscya_early_school_variable_map.tsv`
3. `sources/iq-sex-diff/data/nlscya/nlscya_early_school_extract.tsv.gz`

The earlier intake note understated the available early-school math surface. The widened map now includes:

1. `PIAT Math` standard scores in `1986`, `1988`, and `1990`
2. `PIAT Reading Comprehension` standard scores in `1986`, `1988`, and `1990`
3. `PPVT` standard scores in `1986`, `1988`, and `1990`
4. assessment ages and child sampling weights for the same waves

Primary outputs:

- `sources/iq-sex-diff/data/nlscya/nlscya_early_school_panel.parquet`
- `sources/iq-sex-diff/data/nlscya/nlscya_early_school_surface_gaps.tsv`
- `sources/iq-sex-diff/data/nlscya/nlscya_early_school_agebin_gaps.tsv`
- `sources/iq-sex-diff/data/nlscya/nlscya_early_school_models.tsv`

---

## Main Results

### 1. The first public `NLSCYA` math surface is not showing a simple early male edge

Weighted wave-level `PIAT Math` standard-score gaps (`d = female - male`) are:

1. `1986`: about `+0.074`
2. `1988`: about `+0.059`
3. `1990`: about `+0.024`

So on this first local early-school surface, girls are slightly ahead rather than behind.

### 2. The female edge fades with age

Age-bin `PIAT Math` gaps are:

1. ages `4-5`: about `+0.105`
2. ages `6-7`: about `+0.085`
3. ages `8-9`: about `-0.027`
4. ages `10-11`: about `-0.011`
5. ages `12-13`: about `-0.010`

That is the most important footprint in the pass:

- early-childhood `PIAT Math` is female-leaning
- by later childhood it moves toward parity or slight male lean

### 3. Reading comprehension is more strongly female-leaning than math

Age-bin `PIAT Reading Comprehension` gaps are:

1. ages `6-7`: about `+0.161`
2. ages `8-9`: about `+0.198`
3. ages `10-11`: about `+0.063`

So the early-school female advantage is not math-only on this public surface.

### 4. `PPVT` is smaller and less stable

`PPVT` shows:

1. a female edge at ages `4-5` of about `+0.121`
2. near parity to slight male lean in later childhood bins
3. much noisier movement than reading comprehension

That makes the first `NLSCYA` picture more like:

- broad early female edge on some standardized child surfaces
- then narrowing with age

not:

- immediate early-school male widening across all cognitive surfaces

### 5. The age-interaction model points the same way, but with uncertainty

In the weighted early-school model:

1. `PIAT Math` female coefficient at age `7` is about `+0.86` standard-score points
2. female-by-age interaction is about `-0.32` per year
3. the interaction confidence interval still includes zero

So the directional read is:

- female edge earlier
- narrowing with age

but the slope estimate should still be treated as provisional.

---

## Causal Update

### What hardens

1. The early-school node is real enough to model explicitly.
2. Early-school broad surfaces can move differently from later transcript, school-knowledge, and advanced-track surfaces.
3. The repo should stop talking as if early-school dynamics are already known from later-school data.

### What softens

1. The strong prior that early school must already show a clean male broad-math divergence right after school entry.
2. Any attempt to use recent literature alone as if it had already settled the local early-school node.

### What remains open

1. whether `NLSCYA` is idiosyncratic because it is a children-of-`NLSY79` cohort rather than a school-entry sample like `ECLS`
2. whether `ECLS-K:2011` replicates the early female edge, the later narrowing, both, or neither
3. whether the `PIAT` standard-score surface is the right early-school analogue for later broad school-math batteries

---

## Best Read

This first Stage 2 result does **not** support a simple story that male-favoring broad math divergence is already obvious on every early-school surface.

The better read is:

1. on the public `NLSCYA` standard-score surface, early math is female-leaning
2. that female edge narrows with age and reaches rough parity by later childhood
3. early-school dynamics therefore remain open and dataset-sensitive

That is useful because it tells the project exactly what to do next:

- replicate in `ECLS-K:2011`
- do not let late-school or advanced-track mechanisms absorb the entire early-school node

---

## Limits

This pass should not be over-read.

1. `NLSCYA` is not the same design as `ECLS-K`
2. the public early-school math surface here is still sparse compared with later-school datasets
3. the pass uses a standardized score surface, not item-level math content families
4. the age-pattern estimate is directionally informative but not yet a decisive growth model

So the right conclusion is not "early-school male divergence is false."
The right conclusion is "the local early-school node is now empirically open, and the first public pass points away from a simple immediate male-edge story."

---

## Causal-Check Summary

- `P(cause)`: `0.55` that early-school emergence is a real separate node, but its direction and timing are more surface-sensitive than the recent frontier shorthand suggests.
- `Top alternative`: `NLSCYA` is a cohort- or surface-specific exception, and `ECLS` will show a cleaner male broad-math widening after entry.
- `Falsifier`: `ECLS-K:2011` and `ECLS-K` both show immediate male-favoring broad-math widening from entry onward on aligned early-school scales.
- `Decision impact`: move `ECLS-K:2011` up immediately. The early-school node now needs replication, not assumption.

---

## Outputs

Primary artifacts:

1. `sources/iq-sex-diff/nlscya_early_school_first_pass.py`
2. `sources/iq-sex-diff/data/nlscya/nlscya_early_school_panel.parquet`
3. `sources/iq-sex-diff/data/nlscya/nlscya_early_school_surface_gaps.tsv`
4. `sources/iq-sex-diff/data/nlscya/nlscya_early_school_agebin_gaps.tsv`
5. `sources/iq-sex-diff/data/nlscya/nlscya_early_school_models.tsv`
