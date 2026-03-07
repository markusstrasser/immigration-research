# IQ Sex Differences NLSY97 Stage A

**Date:** 2026-03-05
**Scope:** first discriminating pass on the `NLSY97` quantitative anomaly using process / precision and school-exposure covariates
**Script executed:** `sources/iq-sex-diff/nlsy97_stage_a_pass.py`

**Environment:**

- `sources/iq-sex-diff/pyproject.toml`
- `sources/iq-sex-diff/uv.lock`

**Output tables:**

- `sources/iq-sex-diff/data/nlsy/nlsy97_stage_a_extract.parquet`
- `sources/iq-sex-diff/data/nlsy/nlsy97_stage_a_models.tsv`
- `sources/iq-sex-diff/data/nlsy/nlsy97_stage_a_covariate_gaps.tsv`

---

## Bottom Line

The raw `NLSY97` quantitative female edge is **fragile**.

The strongest result in this pass is not from a tiny corner case. It is from the larger `process_core` sample:

1. unrestricted `quantitative` gap: `+0.054`
2. same-sample base on the `process_core` subset: `+0.037`
3. after adding process / precision covariates: `-0.041`, with `95% CI = (-0.060, -0.022)`

So the `NLSY97` sign flip does **not** look like a stable latent quantitative female advantage.

What it currently looks like is:

- part measurement / process surface
- part sample selection into the analyzable subset
- possibly part school-exposure sorting, but that block is more selection-sensitive and should be treated more cautiously

## Quantitative Node

Positive values favor females. Negative values favor males.

| model | `n` | same-sample base | adjusted | `95%` CI adjusted |
| --- | ---: | ---: | ---: | ---: |
| `process_core` | `5,267` | `+0.037` | `-0.041` | `(-0.060, -0.022)` |
| `process_extended` | `3,157` | `+0.016` | `-0.051` | `(-0.077, -0.024)` |
| `school_core` | `2,902` | `-0.007` | `-0.207` | `(-0.267, -0.147)` |
| `school_extended` | `919` | `-0.009` | `-0.192` | `(-0.290, -0.094)` |
| `process_plus_school_core` | `2,890` | `-0.010` | `-0.104` | `(-0.134, -0.075)` |
| `process_plus_school_full` | `916` | `-0.014` | `-0.074` | `(-0.119, -0.029)` |

Two things matter here:

1. the sign is unstable even before controls once we move to tighter same-sample subsets
2. the process block alone is already enough to flip the coefficient male on a reasonably large sample

That pushes the current posterior away from the story that `NLSY97` discovered a real general female quantitative edge.

## Score-Surface Stress Test

The subtest decomposition points in the same direction.

| score | `process_core` base | `process_core` adjusted | read |
| --- | ---: | ---: | --- |
| `arithmetic_reasoning` | `-0.058` | `-0.090` | male-leaning before and after |
| `math_knowledge` | `+0.124` | `+0.010` | female edge mostly disappears |
| `numerical_operations` | `+0.158` | `+0.064` | female edge shrinks but remains positive |
| `quantitative` | `+0.037` | `-0.041` | flips male |
| `quantitative_plus_numerical_operations` | `+0.137` | `+0.043` | stress surface still attenuates sharply |
| `math_verbal_percentile` | `+0.066` | `+0.001` | essentially disappears |

This is the footprint of a score surface that is doing real work.

The main raw female contribution inside the `NLSY97` quantitative node came from `math_knowledge`, not from a stable male-neutral pattern across both quantitative subtests.

## Negative Controls

The negative controls are useful because they show the Stage A blocks are not flattening everything uniformly.

### `process_core`

- `clerical_speed`: `+0.252` to `+0.162`
- `verbal`: `+0.124` to `+0.056`
- `mechanical`: `-0.557` to `-0.611`

### `process_plus_school_core`

- `clerical_speed`: `+0.220` to `+0.088`
- `verbal`: `+0.087` to `-0.013`
- `mechanical`: `-0.716` to `-0.719`

Interpretation:

- the male mechanical pattern stays large and stable
- the female clerical pattern attenuates but does not vanish in the core combined block
- the female verbal edge is more sensitive than the clerical or mechanical channels

So the Stage A controls do not just mechanically drive all coefficients toward zero. They hit some domains much more than others.

## What To Trust More And Less

### More Trustworthy In This Pass

- `process_core`
- `process_extended`
- `process_plus_school_core`

Reason:

- larger `n`
- less dependence on the thin `grade_fall_1997` subset
- more direct relevance to the `CAT-ASVAB` measurement / process story

### Less Trustworthy As Causal Mediation

- `school_core`
- `school_extended`

Reason:

- same-sample base is already near zero or slightly male before the school controls are added
- these variables are closer to post-treatment schooling states and selected in-school subsets than to clean pre-treatment causes
- the school block is still useful as a *sorting* test, but not yet as a clean mediation estimate

## Causal Update

### `H1` Construct / Score-Surface Artifact

Hardens.

- the quantitative sign is not stable across score surfaces
- the `math_knowledge` female edge largely collapses after the process / precision block
- the official `math_verbal_percentile` surface also collapses toward zero

### `H3` Test-Process / Precision Channel

Hardens.

- the larger-sample process block alone is enough to move `quantitative` from slightly female to modestly male
- this is exactly the kind of footprint we would expect if completion / precision / mode variables matter

### `H2` School-Exposure / Sorting

Still alive, but narrower.

- the school block also flips the coefficient male
- but a lot of that movement is happening in selected subsets where the same-sample base is already near zero
- so this is evidence for sorting sensitivity, not clean proof of schooling causality

### `H4` Pure Sample / Weight Artifact

Some support, but not enough on its own.

- same-sample base movement explains part of the raw `+0.054` edge
- it does not explain the whole Stage A pattern without the process / school blocks

## Causal-Check Summary

- `P(cause)`: `0.55` that the `NLSY97` quantitative female edge is primarily a measurement / process surface artifact rather than a stable latent quantitative female advantage
- `Top alternative`: `0.25` that the sign flip is mostly a real school-exit sorting effect driven by course-taking / track / recent exposure
- `Falsifier`: a transcript-rich school-exit replication or item-level cross-country replication showing a stable female quantitative edge after process-aware correction
- `Decision impact`: stop using the raw `NLSY97` `+0.054` as strong evidence of a general female quantitative edge; move next to `HSLS:09` and `PISA 2022`

## Best Next Steps

1. download and stage `HSLS:09`
2. download and stage `PISA 2022`
3. run the same node in a transcript-rich U.S. school-exit dataset before doing more adult slicing
4. run an item-format / timing decomposition in `PISA` before treating the `NLSY97` sign flip as substantive

