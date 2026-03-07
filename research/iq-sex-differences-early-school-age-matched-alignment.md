# IQ Sex Differences - Early-School Age-Matched Alignment

**Date:** 2026-03-05
**Purpose:** tighten the child-score bridge after the first reading-anchor pass by comparing `NLSCYA` and `ECLS-K:2011` on explicit overlapping age windows rather than broad wave labels.

This is the second bridge step after the early-school ACH and the first score-alignment pass.

---

## Question

The live question after the first score-alignment pass was:

> once the raw directional conflict is removed, does the remaining `NLSCYA` versus `ECLS` difference survive explicit age matching, or was wave-level comparison still exaggerating the disagreement?

The prediction from the current causal tree was:

1. the sign conflict should stay dead under age matching
2. the remaining difference should shrink to a magnitude / timing problem
3. `NLSCYA` should not reopen a female-leaning child-math contradiction once math is anchored to same-age reading

---

## Data Surface

Inputs:

1. `sources/iq-sex-diff/data/nlscya/nlscya_early_school_panel.parquet`
2. `sources/iq-sex-diff/data/ecls_k2011/eclsk2011_early_school_panel.parquet`
3. `sources/iq-sex-diff/data/ecls_k/eclsk_early_school_panel.parquet`

New analysis script:

1. `sources/iq-sex-diff/early_school_age_matched_alignment.py`

Outputs:

1. `sources/iq-sex-diff/data/early_school_alignment/early_school_age_matched_pairs.parquet`
2. `sources/iq-sex-diff/data/early_school_alignment/early_school_age_matched_gaps.tsv`
3. `sources/iq-sex-diff/data/early_school_alignment/early_school_age_matched_models.tsv`
4. `sources/iq-sex-diff/data/early_school_alignment/early_school_age_matched_compare.tsv`

Important note:

1. older `ECLS-K` wave `5` carries an age field on a non-month scale (`1` to `6` in the local extract), so it is not usable for the late child age-matched bridge and is treated as support only through the valid earlier-age windows

---

## Method

For each dataset:

1. pair math and reading within the same child-wave
2. require the paired math and reading age fields to match exactly up to a small numeric tolerance
3. assign explicit age bins in months:
   - `84_90`
   - `90_96`
   - `96_102`
   - `102_108`
   - `108_114`
   - `114_120`
   - `120_126`
   - `126_132`
4. standardize math and reading within each dataset-age-bin
5. compute:
   - `math_z`
   - `reading_z`
   - `math_minus_reading_z`
6. estimate weighted female-minus-male `d` on all three outcomes
7. run weighted `math_z ~ female + reading_z` within each dataset-age-bin

Interpretation:

1. `math_minus_reading_z` asks whether math is relatively more male-leaning than reading at the same child age
2. `female` in `math_z ~ female + reading_z` asks whether girls still retain a math advantage once the same-age reading surface is held fixed

This is still a bridge analysis, not a full psychometric harmonization.

---

## Main Results

### 1. The directional bridge holds under explicit age matching

Across every overlapping `NLSCYA` and `ECLS-K:2011` bin from `84` to `126` months, aligned `math_minus_reading_z` remains male-leaning in both datasets.

`NLSCYA math_minus_reading_z`

1. `84_90`: `-0.186`
2. `90_96`: `-0.185`
3. `96_102`: `-0.135`
4. `102_108`: `-0.227`
5. `108_114`: `-0.266`
6. `114_120`: `-0.354`
7. `120_126`: `-0.124`

`ECLS-K:2011 math_minus_reading_z`

1. `84_90`: `-0.369`
2. `90_96`: `-0.467`
3. `96_102`: `-0.502`
4. `102_108`: `-0.550`
5. `108_114`: `-0.474`
6. `114_120`: `-0.552`
7. `120_126`: `-0.444`

So the first score-alignment result was not a wave-label artifact. The child-level sign conflict stays gone under explicit age matching.

### 2. The remaining disagreement is magnitude, not sign

Relative to `ECLS-K:2011`, `NLSCYA` is consistently less male-leaning on the aligned math-versus-reading surface.

Difference in aligned `math_minus_reading_z`:

1. `84_90`: `+0.183`
2. `90_96`: `+0.283`
3. `96_102`: `+0.367`
4. `102_108`: `+0.323`
5. `108_114`: `+0.208`
6. `114_120`: `+0.198`
7. `120_126`: `+0.320`

The project should now stop talking as if `NLSCYA` directionally contradicts the `ECLS` cohorts. It does not. The remaining question is why the aligned `ECLS-K:2011` surface is more male-leaning at the same ages.

### 3. Conditional-on-reading models say the same thing

Female coefficient in weighted `math_z ~ female + reading_z`:

`NLSCYA`

1. `84_90`: `-0.111`
2. `90_96`: `-0.135`
3. `96_102`: `-0.082`
4. `102_108`: `-0.126`
5. `108_114`: `-0.081`
6. `114_120`: `-0.324`
7. `120_126`: `-0.128`
8. `126_132`: `+0.006`

`ECLS-K:2011`

1. `84_90`: `-0.206`
2. `90_96`: `-0.285`
3. `96_102`: `-0.281`
4. `102_108`: `-0.331`
5. `108_114`: `-0.288`
6. `114_120`: `-0.367`
7. `120_126`: `-0.285`
8. `126_132`: `-0.381`

So the same-age conditional math residual is negative in both datasets through almost the full overlap range. `NLSCYA` simply stays closer to parity.

### 4. The older `ECLS-K` cohort still supports the earlier-age geometry

Where older `ECLS-K` has valid month-scale ages, the aligned residual is also male-leaning:

1. `84_90`: `-0.298`
2. `90_96`: `-0.298`
3. `96_102`: `-0.393`

That keeps the older cohort consistent with the general direction of the bridge, even though its later age field is not usable for direct late-child matching.

---

## Causal Update

### What hardens

1. the first alignment result was real, not a wave-label convenience
2. the early-school anomaly is now best understood as a magnitude mismatch after alignment, not a sign contradiction
3. score-family mismatch remains the leading explanation for why raw `PIAT Math` looked different from raw `ECLS` broad math

### What softens

1. any remaining narrative that `NLSCYA` directionally contradicts early male broad-math emergence
2. the need to keep reopening the early-school sign question

### What remains open

1. why aligned `ECLS-K:2011` is still more male-leaning than aligned `NLSCYA` at the same ages
2. whether the remaining gap is mostly sample-frame composition, scale-family intensity, or residual age-structure mismatch inside the public pairable subsamples
3. whether a stronger psychometric bridge than reading can shrink the remaining magnitude gap further

---

## Best Read

The early-school branch is materially cleaner again.

The best current read is:

1. the project no longer has a real early-school directional conflict
2. after explicit age matching, `NLSCYA` and `ECLS-K:2011` still point the same way
3. the remaining disagreement is that `ECLS-K:2011` is more male-leaning than aligned `NLSCYA` at the same ages

That means the early-school node is now good enough to stop absorbing time as a “maybe it is all contradictory” objection. The next high-value move can shift back toward the late-school transcript node.

---

## Causal-Check Summary

- `P(cause)`: `0.85` that the raw early-school anomaly was mainly score-family mismatch, with residual magnitude differences left over after alignment.
- `Top alternative`: `0.10` that sample-frame composition explains most of the remaining aligned magnitude gap.
- `Falsifier`: a stronger bridge analysis showing aligned `NLSCYA` turns female again or a composition-aware reweighting that makes the datasets diverge directionally.
- `Decision impact`: stop treating the child branch as directionally unresolved. The next major tranche should focus on the deeper `NLSY97` transcript payload pass unless a better psychometric child bridge becomes easy to run.

---

## Outputs

Primary artifacts:

1. `sources/iq-sex-diff/early_school_age_matched_alignment.py`
2. `sources/iq-sex-diff/data/early_school_alignment/early_school_age_matched_pairs.parquet`
3. `sources/iq-sex-diff/data/early_school_alignment/early_school_age_matched_gaps.tsv`
4. `sources/iq-sex-diff/data/early_school_alignment/early_school_age_matched_models.tsv`
5. `sources/iq-sex-diff/data/early_school_alignment/early_school_age_matched_compare.tsv`
