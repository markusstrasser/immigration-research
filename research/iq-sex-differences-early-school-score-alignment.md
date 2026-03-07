# IQ Sex Differences - Early-School Score Alignment

**Date:** 2026-03-05
**Purpose:** run the first direct score-family alignment pass across `NLSCYA`, `ECLS-K:2011`, and older `ECLS-K` by anchoring math to reading within the same child-wave surface instead of comparing raw math scales across batteries.

This is the next diagnostic step after the early-school ACH.

---

## Question

The active question was:

> does the `NLSCYA` early female-looking `PIAT Math` result stay different once child math is aligned against a common within-dataset reading anchor, or does the anomaly mostly collapse?

If the ACH was right, the anomaly should shrink materially once the comparison is:

1. same child
2. same wave
3. same dataset
4. math relative to reading, not raw math level alone

---

## Data Surface

Inputs:

1. `sources/iq-sex-diff/data/nlscya/nlscya_early_school_panel.parquet`
2. `sources/iq-sex-diff/data/ecls_k2011/eclsk2011_early_school_panel.parquet`
3. `sources/iq-sex-diff/data/ecls_k/eclsk_early_school_panel.parquet`

New analysis script:

1. `sources/iq-sex-diff/early_school_score_alignment.py`

Outputs:

1. `sources/iq-sex-diff/data/early_school_alignment/early_school_alignment_pairs.parquet`
2. `sources/iq-sex-diff/data/early_school_alignment/early_school_alignment_gaps.tsv`
3. `sources/iq-sex-diff/data/early_school_alignment/early_school_alignment_models.tsv`
4. `sources/iq-sex-diff/data/early_school_alignment/early_school_alignment_summary.tsv`

---

## Method

For each dataset-wave with paired math and reading scores:

1. standardize math within the wave using weighted mean and SD
2. standardize reading within the wave using weighted mean and SD
3. compute `math_minus_reading_z = math_z - reading_z`
4. estimate the female-minus-male `d` on:
   - `math_z`
   - `reading_z`
   - `math_minus_reading_z`
5. run weighted `math_z ~ female + reading_z`

Interpretation:

- `math_minus_reading_z` asks whether math is relatively more male-leaning than reading inside the same wave
- `female` in `math_z ~ reading_z` asks whether girls still look advantaged on math once the same-wave reading surface is held fixed

This is not a perfect psychometric harmonization. It is a first alignment pass.

---

## Main Results

### 1. The raw `NLSCYA` female math edge mostly collapses once math is anchored to reading

Raw paired-sample `NLSCYA` math `d` is:

1. `1986`: `+0.052`
2. `1988`: `+0.042`
3. `1990`: `-0.039`

But the aligned `math_minus_reading_z` gap is:

1. `1986`: `-0.034`
2. `1988`: `-0.123`
3. `1990`: `-0.218`

So the female-looking raw math result is not stable after the reading anchor. Relative to reading, math is already more male-leaning in every `NLSCYA` wave in the paired sample.

### 2. The two `ECLS` cohorts and `NLSCYA` now line up directionally

Aligned `math_minus_reading_z` gaps:

`ECLS-K`

1. fall kindergarten: `-0.198`
2. spring kindergarten: `-0.247`
3. fall first grade: `-0.256`
4. spring first grade: `-0.314`

`ECLS-K:2011`

1. fall kindergarten: `-0.172`
2. spring kindergarten: `-0.175`
3. fall first grade: `-0.231`
4. spring first grade: `-0.356`
5. fall second grade: `-0.438`
6. spring second grade: `-0.511`

`NLSCYA`

1. `1986`: `-0.034`
2. `1988`: `-0.123`
3. `1990`: `-0.218`

The magnitude is still not identical, but the directional disagreement is mostly gone.

### 3. Conditional-on-reading models say the same thing

Female coefficient in weighted `math_z ~ female + reading_z`:

`NLSCYA`

1. `1986`: `+0.005` (`CI` crosses zero)
2. `1988`: `-0.045` (`CI` crosses zero)
3. `1990`: `-0.132` (`CI` below zero)

`ECLS-K`

1. `fall_k`: `-0.113`
2. `spring_k`: `-0.147`
3. `fall_1`: `-0.153`
4. `spring_1`: `-0.201`

`ECLS-K:2011`

1. `fall_k`: `-0.098`
2. `spring_k`: `-0.096`
3. `fall_1`: `-0.119`
4. `spring_1`: `-0.216`
5. `fall_2`: `-0.280`
6. `spring_2`: `-0.317`

So after reading is held fixed, the project no longer has a real early-school directional split between `NLSCYA` and the `ECLS` cohorts.

### 4. The anomaly did not disappear completely, but it changed category

Before alignment, the live question looked like:

1. why is `NLSCYA` female-leaning while `ECLS` is male-leaning?

After alignment, the live question is:

1. why is the `NLSCYA` math-specific male lean smaller and later than the `ECLS` broad school-entry math-specific male lean?

That is a much narrower and more plausible question.

---

## Causal Update

### What hardens

1. The early-school ACH was basically right: the anomaly is mainly a score-family problem, not a real cohort reversal.
2. The two `ECLS` cohorts and `NLSCYA` can be brought into directional agreement once math is anchored to reading within the same wave.
3. The broad local early-school pattern is now: reading female, math relatively more male.

### What softens

1. Any reading of the raw `NLSCYA` `PIAT Math` result as evidence against early male broad-math emergence.
2. The stronger sample-frame-only explanation.

### What remains open

1. why the `NLSCYA` math-specific male lean is weaker than the `ECLS` math-specific male lean in the earliest waves
2. whether the remaining difference is mostly age, scale family, or composition
3. whether a better bridge than reading can shrink the remaining gap further

---

## Best Read

The early-school branch is materially cleaner now.

The best current read is:

1. broad raw scales made the `NLSCYA` / `ECLS` split look bigger than it really was
2. once child math is aligned against reading, the three local cohorts point in the same direction
3. the remaining disagreement is about degree and timing, not sign

That is a real causal improvement because it kills the strongest version of the “maybe the early-school node is just contradictory noise” objection.

---

## Causal-Check Summary

- `P(cause)`: `0.80` that the raw early-school anomaly was mainly a score-family alignment problem rather than a real cohort reversal.
- `Top alternative`: `0.15` that sample-frame differences still explain most of the remaining magnitude mismatch.
- `Falsifier`: a stronger bridge analysis showing the aligned `NLSCYA` math-specific residual flips back female once age and score-family are handled better than the current reading anchor.
- `Decision impact`: stop treating `NLSCYA` as a directional contradiction. The next work should explain the remaining magnitude gap, not the sign.

---

## Outputs

Primary artifacts:

1. `sources/iq-sex-diff/early_school_score_alignment.py`
2. `sources/iq-sex-diff/data/early_school_alignment/early_school_alignment_pairs.parquet`
3. `sources/iq-sex-diff/data/early_school_alignment/early_school_alignment_gaps.tsv`
4. `sources/iq-sex-diff/data/early_school_alignment/early_school_alignment_models.tsv`
5. `sources/iq-sex-diff/data/early_school_alignment/early_school_alignment_summary.tsv`
