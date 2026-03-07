# IQ Sex Differences - ECLS-K:2011 Early-School First Pass

**Date:** 2026-03-05
**Purpose:** first external replication of the early-school node using the local `ECLS-K:2011` kindergarten-through-grade-5 public-use file, focused narrowly on kindergarten through spring second grade.

This is the first local early-school replication after the `NLSCYA` pass.

---

## Data Surface

Local inputs:

1. `sources/iq-sex-diff/data/ecls_k2011/ChildK5p.zip`
2. `sources/iq-sex-diff/data/ecls_k2011/childK5p.dat`
3. `sources/iq-sex-diff/data/ecls_k2011/ECLSK2011_K5PUF.dct`

Local extraction artifacts:

1. `sources/iq-sex-diff/extract_eclsk2011_early_school.py`
2. `sources/iq-sex-diff/data/ecls_k2011/eclsk2011_early_school_extract.tsv.gz`
3. `sources/iq-sex-diff/eclsk2011_early_school_first_pass.py`
4. `sources/iq-sex-diff/data/ecls_k2011/eclsk2011_early_school_panel.parquet`
5. `sources/iq-sex-diff/data/ecls_k2011/eclsk2011_early_school_surface_gaps.tsv`
6. `sources/iq-sex-diff/data/ecls_k2011/eclsk2011_early_school_models.tsv`

The pass uses:

1. `X1MSCALK5` through `X6MSCALK5`
2. `X1RSCALK5` through `X6RSCALK5`
3. revised child sex `X_CHSEX_R`
4. wave-matched full-sample weights for the first six waves

Weight guidance is based on the official `ECLS-K:2011` psychometric documentation:

- <https://nces.ed.gov/pubs2020/2020123.pdf>
- <https://nces.ed.gov/pubs2018/2018183.pdf>

This first pass stops at spring second grade on purpose because that is already enough to test whether the local early-school node looks more like `NLSCYA` or more like the recent male-widening literature.

---

## Main Results

### 1. `ECLS-K:2011` does not replicate the early female math edge from `NLSCYA`

Weighted math gaps (`d = female - male`) are:

1. fall kindergarten: about `-0.029`
2. spring kindergarten: about `-0.004`
3. fall first grade: about `+0.019`
4. spring first grade: about `-0.095`
5. fall second grade: about `-0.142`
6. spring second grade: about `-0.159`

That is a very different geometry from the first `NLSCYA` pass.

### 2. The male math edge strengthens after first grade on this surface

The simplest read of the math trajectory is:

1. near parity in kindergarten
2. still near parity in fall first grade
3. clear male lean by spring first grade
4. stronger male lean by second grade

So on this cleaner school-entry cohort, the early-school node points much more in the direction suggested by the recent literature than the `NLSCYA` pass did.

### 3. Reading moves the other way

Weighted reading gaps are female-leaning at every wave:

1. fall kindergarten: about `+0.094`
2. spring kindergarten: about `+0.131`
3. fall first grade: about `+0.196`
4. spring first grade: about `+0.169`
5. fall second grade: about `+0.193`
6. spring second grade: about `+0.220`

That means the math result is not just a generic early-school male cognitive edge. The surface split is domain-specific.

### 4. The pooled wave model says the same thing

In the weighted cluster-robust model:

1. math female-by-wave slope is about `-0.593` per wave step
2. reading female-by-wave slope is about `+0.493` per wave step

So the replication is not just about isolated wave means. The direction of change differs by domain.

---

## Causal Update

### What hardens

1. `EarlySchoolEmergence` is a real node in the project.
2. On at least one clean school-entry cohort, broad school math is near parity in kindergarten and then moves male by early grade school.
3. The early-school node is domain-specific, because reading moves female while math moves male.

### What softens

1. The idea that `NLSCYA` already settled the local early-school node.
2. Any story that expects one universal early-school direction across every child dataset and every score surface.

### What remains open

1. whether the `NLSCYA` / `ECLS-K:2011` disagreement is mostly cohort, score-surface, or weighting/design driven
2. whether the older `ECLS-K` cohort looks more like `ECLS-K:2011` or more like `NLSCYA`
3. whether early math widening is strongest on broad school-entry scales but later fragments into school-knowledge, applied, and advanced-track families

---

## Best Read

`ECLS-K:2011` changes the early-school picture materially.

The best current read is now:

1. the early-school node is real
2. `ECLS-K:2011` is closer to the recent literature than `NLSCYA` is
3. the direction of early-school emergence is surface-sensitive, not already uniform across local datasets

That means the repo should stop making either of these lazy moves:

1. "late-school mechanisms explain broad school math"
2. "`NLSCYA` already disproves early male widening"

Neither survives the current local evidence.

---

## Combined Early-School Read After `NLSCYA` And `ECLS-K:2011`

The current local early-school state is now:

1. `NLSCYA`:
   - early female-leaning `PIAT Math` standard scores
   - narrowing with age
2. `ECLS-K:2011`:
   - near-parity kindergarten math
   - male-widening by spring first and second grade

So the real project update is not one of those datasets winning by vibe.

It is:

- early-school emergence is now empirically active
- direction depends on cohort and score surface
- replication pressure just got stronger, not weaker

That is a good outcome for the project because it localizes the next question cleanly.

---

## Causal-Check Summary

- `P(cause)`: `0.75` that early-school emergence is a genuine causal node, but one whose observed direction is materially surface-sensitive.
- `Top alternative`: the `NLSCYA` / `ECLS-K:2011` disagreement is mostly an artifact of scoring, weighting, or cohort design rather than a real developmental difference.
- `Falsifier`: the older `ECLS-K` cohort and alternate early-school scales both collapsing back to the `NLSCYA` shape after aligned handling.
- `Decision impact`: move next to older `ECLS-K` and then score-family alignment. The early-school node is no longer a speculative branch.

---

## Outputs

Primary artifacts:

1. `sources/iq-sex-diff/extract_eclsk2011_early_school.py`
2. `sources/iq-sex-diff/eclsk2011_early_school_first_pass.py`
3. `sources/iq-sex-diff/data/ecls_k2011/eclsk2011_early_school_extract.tsv.gz`
4. `sources/iq-sex-diff/data/ecls_k2011/eclsk2011_early_school_panel.parquet`
5. `sources/iq-sex-diff/data/ecls_k2011/eclsk2011_early_school_surface_gaps.tsv`
6. `sources/iq-sex-diff/data/ecls_k2011/eclsk2011_early_school_models.tsv`
