# NELS Late-School Wedge First Pass

**Date:** 2026-03-06  
**Question:** does the school-linked wedge seen in `HSLS`, `ELS`, and parts of `NLSY97` appear in the older `NELS:88` public-use cohort?

## Result

Yes, with the same basic geometry and a narrower track signal.

On the transcript-core `NELS` sample (`F4TRSCWT > 0`), later tested math is not female-leaning, while several school-linked surfaces are. [SOURCE: `sources/iq-sex-diff/data/nels/nels_wedge_overall.tsv`; `sources/iq-sex-diff/data/nels/nels_wedge_models.tsv`]

- `F12XMSTD` is near parity raw and near null after baseline anchoring: adjusted `beta_female = -0.003`. [SOURCE: `sources/iq-sex-diff/data/nels/nels_wedge_models.tsv`]
- `F22XMSTD` is male-leaning once anchored on base-year math and reading: adjusted `beta_female = -0.088`, `95% CI [-0.157, -0.018]`. [SOURCE: `sources/iq-sex-diff/data/nels/nels_wedge_models.tsv`]
- transcript math units are basically neutral after anchoring: adjusted `beta_female = +0.001`. [SOURCE: `sources/iq-sex-diff/data/nels/nels_wedge_models.tsv`]
- school-evaluation surfaces tilt female:
  - math grade quality `+0.101`
  - recognition for good grades `+0.142`
  - academic honors recommendation `+0.023` [SOURCE: `sources/iq-sex-diff/data/nels/nels_wedge_models.tsv`]
- track/program surfaces are weaker but still tend female:
  - academic-or-rigorous program `+0.031`
  - rigorous-academic program `+0.023` with CI crossing zero after anchoring [SOURCE: `sources/iq-sex-diff/data/nels/nels_wedge_models.tsv`]

So `NELS` does not replicate a female advantage in later tested math. It does replicate the broader claim that school-linked evaluation surfaces can diverge from tested math in a female direction. [INFERENCE]

## What Replicates

The broad pattern now looks cross-cohort rather than `HSLS`-specific.

1. tested math surfaces are male-leaning or near null
2. school-linked evaluation surfaces tilt female
3. track signals are weaker and more cohort-specific than grade / recognition signals

That is exactly the pattern in this first `NELS` pass. [INFERENCE based on: `sources/iq-sex-diff/data/nels/nels_wedge_models.tsv`; `research/iq-sex-differences-hsls-wedge-first-pass.md`; `research/iq-sex-differences-els-wedge-first-pass.md`]

## What Does Not Replicate Cleanly

`NELS` does **not** reproduce a strong female transcript-course advantage once the surface is actual transcript math units rather than grades or recognitions.

- raw transcript math units: `d = +0.010`
- anchored transcript math units: `beta_female = +0.001`, CI crossing zero [SOURCE: `sources/iq-sex-diff/data/nels/nels_wedge_overall.tsv`; `sources/iq-sex-diff/data/nels/nels_wedge_models.tsv`]

That matters because it narrows the wedge:

- the more stable replication is on **evaluation / recognition**
- the weaker replication is on **pure quantity of transcript math**

This softens any over-strong “girls always take more math once baseline is fixed” story. [INFERENCE]

## Within-Program Tested Math

Inside transcript-indicated program groups, later `F22` math remains mostly male-leaning.

- rigorous academic: `d = -0.318`
- academic: `d = -0.055`
- vocational: `d = -0.535`
- none of above: `d = -0.173`
- academic/vocational mixed: `d = +0.268` [SOURCE: `sources/iq-sex-diff/data/nels/nels_wedge_by_program.tsv`]

This is descriptive only. Program is downstream selection, so it should not be treated as a clean control surface. [SOURCE: `research/iq-sex-differences-analysis-protocol.md`]

## Behavior / Compliance Check

I also ran the analogous behavior/compliance probe for `F1 behavior -> F2 math`.

- DAG-valid adjustment set for `BehaviorIndexF1 -> F2MathScore`: `{Sex, BYMath, BYReading}`. [SOURCE: `sources/iq-sex-diff/data/nels/nels_behavior_f2math_dag_output.json`]
- OLS estimate: `behavior_index_z = +0.163` on `F22XMSTD_z`. [SOURCE: `sources/iq-sex-diff/data/nels/nels_behavior_f2math_model_data.csv`]
- `sensemakr`: `RV = 0.161`, below the strongest observed benchmark (`BY2XMSTD_z`, partial `R² ≈ 0.470`). [SOURCE: `sources/iq-sex-diff/data/nels/nels_behavior_f2math_sensemakr.json`]

So behavior/compliance remains a plausible channel, but this particular `NELS` behavior effect is not robust enough to carry the wedge explanation by itself. [INFERENCE]

## Causal Read

- `Observation:` older `NELS` reproduces female-leaning evaluation / recognition surfaces alongside male-leaning or null tested-math surfaces. [SOURCE: `sources/iq-sex-diff/data/nels/nels_wedge_models.tsv`]
- `Null:` if the `HSLS` / `ELS` wedge were just a newer-cohort artifact, `NELS` should not line up this cleanly. [INFERENCE]
- `Best current cause:` school-linked evaluation surfaces encode something more female-favoring than standardized tested math, while pure transcript quantity and tested math do not move the same way. [INFERENCE]
- `Top alternative:` cohort-specific weighting / access / transcript-core selection is still producing some of the alignment. [INFERENCE]
- `Falsifier:` another transcript-rich cohort where grades / recognition / recommendation do not tilt female once baseline math and reading are fixed, or where tested math tilts female instead of male/null. [INFERENCE]

## Decision Impact

`NELS` strengthens the school-linked wedge node.

It does **not** support:

1. a broad female tested-math advantage
2. a simple “girls just take more math” transcript-quantity story

It **does** support:

1. female-leaning school-evaluation surfaces
2. male-leaning or null tested-math surfaces
3. another independent reason not to use grades, recognitions, or honors recommendations as clean latent-ability proxies

## Artifacts

- extract: `sources/iq-sex-diff/data/nels/nels_wedge_extract.parquet`
- overall gaps: `sources/iq-sex-diff/data/nels/nels_wedge_overall.tsv`
- by-program table: `sources/iq-sex-diff/data/nels/nels_wedge_by_program.tsv`
- models: `sources/iq-sex-diff/data/nels/nels_wedge_models.tsv`
- DAG input/output: `sources/iq-sex-diff/data/nels/nels_behavior_f2math_dag_input.json`, `sources/iq-sex-diff/data/nels/nels_behavior_f2math_dag_output.json`
- sensitivity: `sources/iq-sex-diff/data/nels/nels_behavior_f2math_sensemakr.json`
