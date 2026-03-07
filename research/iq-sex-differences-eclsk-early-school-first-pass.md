# IQ Sex Differences - ECLS-K Early-School First Pass

**Date:** 2026-03-05
**Purpose:** older `ECLS-K` replication of the early-school node using the local kindergarten-to-eighth-grade public-use child file, restricted here to kindergarten through spring first grade for direct comparison with the other early-school passes.

This is the third local early-school cohort after `NLSCYA` and `ECLS-K:2011`.

---

## Data Surface

Local inputs:

1. `sources/iq-sex-diff/data/ecls_k/Childk8p.zip`
2. `sources/iq-sex-diff/data/ecls_k/Childk8p.z01` through `Childk8p.z05`
3. `sources/iq-sex-diff/data/ecls_k/ECLSK_Kto8_child_STATA.dct`
4. `sources/iq-sex-diff/data/ecls_k/refresh/childk8p.dat`

Local extraction / analysis artifacts:

1. `sources/iq-sex-diff/extract_eclsk_early_school.py`
2. `sources/iq-sex-diff/data/ecls_k/eclsk_early_school_extract.tsv.gz`
3. `sources/iq-sex-diff/eclsk_early_school_first_pass.py`
4. `sources/iq-sex-diff/data/ecls_k/eclsk_early_school_panel.parquet`
5. `sources/iq-sex-diff/data/ecls_k/eclsk_early_school_surface_gaps.tsv`
6. `sources/iq-sex-diff/data/ecls_k/eclsk_early_school_models.tsv`

Practical note:

- the older `ECLS-K` child archive did not extract cleanly through the ordinary split-zip path
- the working path was to concatenate the NCES split parts, extract the full ASCII, and then parse the record layout from the official Stata dictionary
- the selected early-school fields all live on `_line(1)`, but the file still uses `15` physical lines per logical record

This first pass uses:

1. `C1R4MSCL` through `C4R4MSCL`
2. `C1R4RSCL` through `C4R4RSCL`
3. `C1MTHFLG` through `C4MTHFLG`
4. `C1RDGFLG` through `C4RDGFLG`
5. child composite sex `GENDER`
6. round composite child weights `C1WEIGHT` through `C4WEIGHT`

The pass stops at spring first grade because that is enough to test the early-school node on the older cohort without mixing in the round-5 jump to spring third grade.

---

## Main Results

### 1. The older `ECLS-K` cohort looks much more like `ECLS-K:2011` than `NLSCYA`

Weighted math gaps (`d = female - male`) are:

1. fall kindergarten: `-0.024`
2. spring kindergarten: `-0.041`
3. fall first grade: `-0.042`
4. spring first grade: `-0.091`

That is not the `NLSCYA` geometry. It is another school-entry cohort with modest male-leaning math from the start and stronger male lean by spring first grade.

### 2. Reading is female-leaning throughout

Weighted reading gaps are:

1. fall kindergarten: `+0.123`
2. spring kindergarten: `+0.157`
3. fall first grade: `+0.164`
4. spring first grade: `+0.164`

So the early-school split is not a generic male cognitive edge. It is domain-specific again.

### 3. The pooled wave model points the same way

In the weighted models:

1. math female-by-wave slope is about `-0.469` per wave step (`95% CI -0.631 to -0.308`)
2. reading female-by-wave slope is about `+0.871` per wave step (`95% CI +0.593 to +1.150`)

The absolute math intercept is close to zero, but the direction of change is not.

### 4. The local early-school picture is now split by score family, not just by “early vs late”

Current local early-school state:

1. `NLSCYA` `PIAT Math` standard scores:
   - female-leaning at younger ages
   - move toward parity later
2. `ECLS-K:2011` broad school-entry math scales:
   - near parity in kindergarten
   - male by spring first and second grade
3. older `ECLS-K` broad school-entry math scales:
   - modestly male from kindergarten
   - more male by spring first grade

That means the active disagreement is no longer “does early-school emergence exist?” It does.

The disagreement is now:

1. why `PIAT Math` behaves differently from the broad `ECLS` school-entry scales
2. whether that is mostly score family, cohort, weighting, or some combination

---

## Causal Update

### What hardens

1. `EarlySchoolEmergence` is now active in three local cohorts.
2. The broad `ECLS` school-entry math surfaces are directionally aligned across the `1998-99` and `2011` cohorts.
3. The early-school node is domain-specific, because reading stays female-leaning while math moves male.

### What softens

1. Any attempt to use `NLSCYA` alone to settle the early-school node.
2. Any narrative that expects one child battery to represent the whole early-school construct.

### What remains open

1. whether the `NLSCYA` divergence is mainly score-family (`PIAT` versus `ECLS` IRT school scales)
2. whether aligned rescoring or age handling can compress the `NLSCYA` / `ECLS` disagreement
3. how far the `ECLS` male-leaning broad math shape persists once later grades and track separation enter

---

## Best Read

The early-school branch is no longer acquisition-limited.

The best current read is:

1. the early-school node is real
2. two `ECLS` cohorts now point in the same direction on broad school-entry math
3. `NLSCYA` remains the outlier surface and should now be treated as a score-family problem to explain, not a reason to deny the node

That is a real project update because it changes what “replication” means here.

It is no longer:

- “find one more child cohort and see which side wins”

It is now:

- “align the child score families and explain why `PIAT` and `ECLS` broad school-entry math do not have the same sex-gap geometry”

---

## Causal-Check Summary

- `P(cause)`: `0.80` that early-school emergence is a genuine node and that the broad `ECLS` school-entry math surface is male-leaning by early grade school.
- `Top alternative`: the `ECLS` pair and `NLSCYA` disagree mainly because of scale family and weighting rather than a real developmental difference.
- `Falsifier`: aligned `PIAT` / `ECLS` rescoring or another child cohort showing the `ECLS` pattern collapses once score family is harmonized.
- `Decision impact`: the next early-school step is score-family alignment, not more raw cohort acquisition.

---

## Outputs

Primary artifacts:

1. `sources/iq-sex-diff/extract_eclsk_early_school.py`
2. `sources/iq-sex-diff/eclsk_early_school_first_pass.py`
3. `sources/iq-sex-diff/data/ecls_k/eclsk_early_school_extract.tsv.gz`
4. `sources/iq-sex-diff/data/ecls_k/eclsk_early_school_panel.parquet`
5. `sources/iq-sex-diff/data/ecls_k/eclsk_early_school_surface_gaps.tsv`
6. `sources/iq-sex-diff/data/ecls_k/eclsk_early_school_models.tsv`
