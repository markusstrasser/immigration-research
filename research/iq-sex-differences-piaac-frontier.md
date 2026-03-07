# IQ Sex Differences PIAAC Frontier

**Date:** 2026-03-05
**Scope:** `PIAAC p1` education-stratified cross-country gap surface
**Script executed:** `sources/iq-sex-diff/piaac_p1_stratified.py`

**Outputs:**

- `sources/iq-sex-diff/data/piaac/piaac_p1_stratified_gaps.tsv`
- `sources/iq-sex-diff/data/piaac/piaac_p1_grouped_summary.tsv`

**Method lock used:**

- `p1` only
- `EDCAT6` as the primary education stratifier
- grouped education surface:
  - `low` = `EDCAT6 = 1`
  - `middle` = `EDCAT6 = 2 or 3`
  - `high` = `EDCAT6 = 4, 5, 6`
- plausible values:
  - `PVLIT1..10`
  - `PVNUM1..10`
  - `PVPSL1..10`
- replicate weights:
  - `SPFWT0` for point estimates
  - `SPFWT1..R` with released `VEMETHOD`, `VEFAYFAC`, and `VENREPS`

**Local methodological references:**

- [2016667REV_codebook.pdf](/Users/alien/Projects/research/sources/iq-sex-diff/data/docs/2016667REV_codebook.pdf)
- [iq-sex-differences-analysis-protocol.md](/Users/alien/Projects/research/research/iq-sex-differences-analysis-protocol.md#L125)

---

## Bottom Line

`PIAAC p1` does **not** support the story that the current sex-gap structure is mostly an artifact of education composition.

The cleanest result is numeracy:

1. the numeracy gap is male-leaning in every overall country-wave surface in the local `PIAAC p1` snapshot
2. it remains male-leaning in every grouped education cell
3. it usually gets **more** male-leaning at higher education levels rather than collapsing inside strata

That directly softens the strong version of the "education effects are larger, so the gap may mostly disappear once we stratify" story.

`PIAAC` also changes the interpretation of the `NLSY97` sign flip:

- `NLSY97 quantitative` is slightly female-leaning
- `PIAAC numeracy` is broadly male-leaning across adult country-wave and education cells

That makes the `NLSY97` reversal look more like a **battery / cohort / age-surface issue** than a stable general quantitative reversal.

## Overall Country-Wave Surface

Positive values favor females. Negative values favor males.

### Literacy

| country-wave | `d` | `95%` CI |
|---|---:|---:|
| `Finland` | `+0.063` | `(-0.005, +0.131)` |
| `Germany` | `-0.107` | `(-0.169, -0.046)` |
| `Italy` | `+0.006` | `(-0.073, +0.084)` |
| `Japan` | `-0.078` | `(-0.143, -0.014)` |
| `Netherlands` | `-0.126` | `(-0.186, -0.067)` |
| `USA 2012` | `-0.013` | `(-0.071, +0.044)` |
| `USA 2017` | `-0.003` | `(-0.074, +0.067)` |

### Numeracy

| country-wave | `d` | `95%` CI |
|---|---:|---:|
| `Finland` | `-0.196` | `(-0.260, -0.132)` |
| `Germany` | `-0.329` | `(-0.393, -0.264)` |
| `Italy` | `-0.216` | `(-0.287, -0.145)` |
| `Japan` | `-0.284` | `(-0.358, -0.210)` |
| `Netherlands` | `-0.332` | `(-0.393, -0.271)` |
| `USA 2012` | `-0.249` | `(-0.299, -0.198)` |
| `USA 2017` | `-0.161` | `(-0.232, -0.091)` |

### Problem Solving

Italy is absent here in the local snapshot because the released `PVPSL` surface does not yield a usable analysis cell for this file.

| country-wave | `d` | `95%` CI |
|---|---:|---:|
| `Finland` | `-0.083` | `(-0.146, -0.020)` |
| `Germany` | `-0.122` | `(-0.193, -0.051)` |
| `Japan` | `-0.192` | `(-0.272, -0.111)` |
| `Netherlands` | `-0.198` | `(-0.268, -0.128)` |
| `USA 2012` | `-0.113` | `(-0.183, -0.042)` |
| `USA 2017` | `-0.112` | `(-0.205, -0.020)` |

## Grouped Education Surface

### Literacy

Mean grouped gap across country-waves:

- `low`: `-0.056`
- `middle`: `-0.050`
- `high`: `-0.118`

Read:

- literacy is near zero to mildly male-leaning in low and middle education groups
- the high-education literacy surface is more consistently male-leaning
- the literacy cell pattern is heterogeneous and often not far from zero, so this is not a high-confidence universal literacy gap

### Numeracy

Mean grouped gap across country-waves:

- `low`: `-0.222`
- `middle`: `-0.288`
- `high`: `-0.418`

Read:

- numeracy is male-leaning in every grouped education cell in every country-wave
- `20 / 21` grouped numeracy cells have confidence intervals entirely below zero
- the male numeracy gap is generally largest in the high-education group

### Problem Solving

Mean grouped gap across country-waves:

- `low`: `-0.067`
- `middle`: `-0.142`
- `high`: `-0.199`

Read:

- problem solving is male-leaning overall
- low-education cells are weaker and sometimes near zero
- middle and high education groups are more consistently male-leaning

## What This Does To The Causal Graph

### Observation

The active anomaly after the cohort work was:

- `NLSY79 quantitative`: `-0.179`
- `NLSY97 quantitative`: `+0.054`

The `PIAAC` frontier adds a new quantitative footprint:

- overall adult numeracy is male-leaning in all current country-wave files
- within grouped education strata it remains male-leaning, not neutralized

### Null

A weak null would say the `NLSY79` and `NLSY97` difference is just ordinary dataset drift, with no broader implication.

`PIAAC` rejects the stronger version of the "education composition explains it" null, because the numeracy gap remains within education strata.

### Residual Geometry

- not a universal sharp reversal
- closer to an **isolated cohort / battery divergence** on the quantitative node
- the broader adult international pattern remains male-leaning for numeracy and problem solving

## Hypothesis Ranking

### `H1` Battery / Construct / Age-Surface Difference

Strongest current explanation.

Mechanism:

- `CAT-ASVAB quantitative` in `NLSY97` is not behaving like a stable general numeracy construct across the same way that adult `PIAAC` numeracy behaves
- the younger cohort and test format produce a local reversal that does not generalize to adult international skills data

### `H2` Education-Composition Story

Weakened.

Mechanism prediction:

- if education composition were doing most of the work, conditioning on education should compress the male numeracy gap materially toward zero

Observed:

- within-stratum numeracy remains male-leaning and often gets more male-leaning at higher education

### `H3` Broad Stable Domain Pattern With Heterogeneous Magnitude

Also supported.

Mechanism:

- the sign is fairly stable for numeracy and problem solving
- the magnitude shifts across country-wave and education cells

## Causal-Check Summary

> **Observation:** `NLSY97 quantitative` is slightly female-leaning (`+0.054`), but `PIAAC` numeracy is male-leaning in every overall country-wave and every grouped education cell in the local `p1` snapshot.
> **Null:** education composition or generic sampling drift explains the earlier cohort disagreement.
> **Residual after null:** stratifying by education does not remove the male numeracy pattern.
> **Geometry:** isolated cohort / battery divergence rather than a broad class-wide reversal.
> **Magnitude:** grouped numeracy ranges from about `-0.073` to `-0.540`; high-education mean is `-0.418`.
> **Lag window:** one cohort and one adult generation; this is compatible with age-surface and battery-surface differences.

- `P(cause)`: `0.70` that the current quantitative disagreement is driven more by battery / construct / age-surface differences than by education composition alone
- `Top alternative`: `0.20` that the adult `PIAAC` numeracy pattern mostly reflects labor-market and field-of-study accumulation after schooling, so it is not a clean adjudicator of youth quantitative ability
- `Falsifier`: a harmonized youth or young-adult international battery showing the same slight female quantitative edge across countries after education stratification
- `Decision impact`: downgrade any claim that `NLSY97` proves a general female quantitative edge; treat it as a cohort-specific or measurement-specific result until it replicates on a closer surface

## Epistemic Limits

1. `PIAAC` is adult skill data, not a youth norming sample.
2. The literacy domain here is not identical to `ASVAB` verbal or school-grade reading measures.
3. The problem-solving surface is thinner than numeracy because not every file yields a full usable `PVPSL` analysis surface.
4. Education stratification is not causal identification; adults with the same attained education can still differ by field, occupation, and accumulated practice.
5. This pass uses released survey design and plausible values correctly, but it is still a descriptive frontier, not a mediation model.

## Best Next Steps

1. split `PIAAC` further by age bands so we can test whether the male numeracy pattern is concentrated in older cohorts
2. add field-of-study or occupation proxies where available to see whether the high-education male numeracy gap is accumulation-driven
3. revisit the `NLSY97` quantitative node with a tighter construct map instead of treating `CAT-ASVAB quantitative` and adult `PIAAC` numeracy as identical
