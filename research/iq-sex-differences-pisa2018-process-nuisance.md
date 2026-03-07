# IQ Sex Differences - PISA 2018 Process-Nuisance Prototype

**Date:** 2026-03-06
**Purpose:** test whether non-focal process style materially compresses the surviving `PISA 2018` residual content-family ordering after the contamination-aware leave-out pass.

This is a prototype, not a final process-data DIF paper.

It sits between:

1. the existing leave-out accuracy matching pass
2. a heavier process-informed rescoring or formal response-time DIF program

Companion files:

- `research/iq-sex-differences-pisa2018-dif-leaveout.md`
- `research/iq-sex-differences-next-level-research-plan.md`
- `research/iq-sex-differences-master-dag.md`

---

## Why This Pass Exists

The repo already showed:

1. the raw `PISA 2018` family geometry compresses once ability is held fixed
2. the residual family ordering survives focal-item and focal-family leave-out matching

That still left one live question:

> does non-focal process style explain the residual ordering that survives the leave-out accuracy match?

This pass answers that question with the current public data surface. [INFERENCE]

---

## DAG Discipline

This is **not** a causal total-effect model of `sex -> item response`.

The relevant diagnostic DAG is:

```text
Sex -> process style
Sex -> latent domain
Latent domain -> focal item score
Latent domain -> non-focal accuracy match
Latent domain -> non-focal process style
Process style -> focal item score
Test design -> focal item score
Test design -> process style
```

So:

1. non-focal process variables are descendants of both sex and latent ability
2. they are **not** admissible controls for a causal sex effect
3. they are admissible only for a **measurement-diagnostic** question:
   - does matching on non-focal process style compress the residual family ordering further?

[SOURCE: `research/iq-sex-differences-master-dag.md`; `research/iq-sex-differences-analysis-protocol.md`]

Because this is not a causal OLS estimand, I did **not** run `sensemakr` here. That would pretend a causal interpretation the model does not deserve. [INFERENCE]

---

## Method

### Inputs

1. `sources/iq-sex-diff/data/pisa/pisa2018_math_item_extract.parquet`
2. `sources/iq-sex-diff/data/pisa/pisa2018_item_level_gaps.tsv`
3. `sources/iq-sex-diff/data/pisa/pisa2018_unit_framework_proxy.tsv`

### Script

1. `sources/iq-sex-diff/pisa2018_process_nuisance_pass.py`

### Outputs

1. `sources/iq-sex-diff/data/pisa/pisa2018_process_nuisance_item.tsv`
2. `sources/iq-sex-diff/data/pisa/pisa2018_process_nuisance_content_summary.tsv`
3. `sources/iq-sex-diff/data/pisa/pisa2018_process_nuisance_context_summary.tsv`

### Matching surfaces

For each math item:

1. keep the existing `family-out` non-focal accuracy match
2. build non-focal-family process-style scores from:
   - mean standardized `log(time)`
   - mean standardized visits
   - non-focal-family observed item count

### Same-sample comparison

For each item, fit:

1. **base diagnostic model**
   - `item_score ~ female + nonfocal_accuracy + female*nonfocal_accuracy + country_FE`
2. **process diagnostic model**
   - `item_score ~ female + nonfocal_accuracy + female*nonfocal_accuracy + nonfocal_time + nonfocal_visits + nonfocal_count + female*nonfocal_time + female*nonfocal_visits + country_FE`

Then compare the female coefficient on the **same estimation sample**.

I also ran a rough trimmed version that excludes the bottom focal-item time decile before refitting the process model.

This is deliberately narrower than the recent process-data literature:

- it is not the GLM nuisance-trait scoring rule proposed in Chen et al. [SOURCE: https://arxiv.org/abs/2504.00136] [PREPRINT]
- it is not a formal response-time DIF detector of the Liu et al. type [SOURCE: https://link.springer.com/article/10.1186/s40536-026-00290-1]
- it is closer to a local prototype of the “use response-process data to interpret DIF” idea [SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC11607718/]

---

## Main Results

### 1. Process style does not materially compress the residual family ordering

Weighted content summaries:

| family | base same-sample beta | process beta | process trimmed | weighted abs reduction |
| --- | ---: | ---: | ---: | ---: |
| `space_shape` | `-0.0148` | `-0.0159` | `-0.0177` | `-0.0011` |
| `change_relationships` | `-0.0101` | `-0.0133` | `-0.0164` | `-0.0007` |
| `quantity` | `-0.0020` | `-0.0068` | `-0.0099` | `+0.0025` |
| `uncertainty_data` | `+0.0033` | `-0.0016` | `-0.0038` | `+0.0010` |

Overall weighted mean female coefficient across items:

1. same-sample base: `-0.0075`
2. process model: `-0.0107`
3. process trimmed: `-0.0133`

Overall weighted mean absolute-gap reduction:

1. `+0.00005`

So the best simple summary is:

`non-focal process style buys almost no net compression`

and if anything the weighted residual moves slightly more male. [SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_process_nuisance_content_summary.tsv`; `sources/iq-sex-diff/data/pisa/pisa2018_process_nuisance_item.tsv`]

### 2. The strongest residual family ordering survives

The rank ordering remains effectively the same:

1. `space_shape` remains the clearest male-residual family
2. `change_relationships` remains next
3. `quantity` stays weaker than those two
4. `uncertainty_data` stays closest to parity, even though the process model pushes it slightly male

[SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_process_nuisance_content_summary.tsv`]

### 3. Process style itself is predictive, but mostly not sex-differentially predictive

Weighted average process coefficients across items:

1. `time_beta_process = +0.0212`
2. `visit_beta_process = +0.0040`
3. `count_beta_process = +0.0123`
4. `female_time_beta_process = -0.0012`
5. `female_visit_beta_process = +0.0009`

Interpretation:

1. non-focal process style carries predictive information
2. but the sex-specific process interactions are very small on average
3. that is consistent with process style being informative without being the main driver of the residual family ordering

[SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_process_nuisance_item.tsv`] [INFERENCE]

### 4. The biggest item-level shrinkages are localized, not family-wide

Examples where the absolute residual shrank most:

1. `Flu test Q03`
2. `Seats in a Theatre Q01`
3. `Diving Q01`
4. `Medicine doses Q01`

But the largest male-residual items remain male after the process model, including:

1. `Cash Withdrawal Q01`
2. `Crazy Ants Q01`
3. `Running Time Q01`
4. `Speeding Fines Q03`

[SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_process_nuisance_item.tsv`]

---

## Best Read

This prototype weakens one specific story:

> the surviving `PISA` family ordering is mostly just a generic non-focal process-style artifact

That story no longer looks strong.

The current best read is:

1. the residual `PISA 2018` family ordering is not mainly explained by non-focal time/visit/count style
2. process style matters somewhat for prediction, but not much for the sex-specific residual family geometry
3. the residual content-family node now looks more like a real measurement/content-family structure than a simple process-style mirage
4. the next process step, if worth doing, should be a **real** process-data rescoring or formal response-time DIF pass, not another proxy regression

[INFERENCE]

---

## What Hardens

1. the residual `PISA` family ordering is not just a leave-out matching artifact
2. it is also not well explained by this first process-style nuisance match
3. `space_shape` remains the strongest male-residual family in every serious local `PISA` pass so far

---

## What Softens

1. the idea that simple time/visit/completion style is the main reason the `PISA` residual ordering survives
2. the idea that a light process adjustment would likely collapse the residual ordering

---

## What Remains Open

1. whether a fuller process-data nuisance-trait scoring rule would do more than this prototype
2. whether direct response-time DIF methods would isolate item-specific timing unfairness more cleanly
3. whether the same result holds on `TIMSS` once a comparable pass is built

---

## Causal-Check Summary

- `P(cause)`: `0.74` that the surviving `PISA 2018` residual family ordering is mainly a real content-family measurement node rather than a generic non-focal process-style artifact.
- `Top alternative`: `0.16` that a stronger process-data method, such as nuisance-trait rescoring or direct response-time DIF, would still compress the current residual ordering materially.
- `Falsifier`: a fuller process-data rescoring or formal response-time DIF pass that drives `space_shape` and `change_relationships` close to the `uncertainty_data` residual.
- `Decision impact`: the next highest-value measurement step is no longer another proxy process regression. It is either a real process-data rescoring method or a move back to the restricted transcript/process frontier.

