# IQ Sex Differences First Pass Results

**Date:** 2026-03-05
**Scope:** first locked empirical tranche after Stage `-1` / `0A`
**Scripts executed:**

- `sources/iq-sex-diff/icar_decomposition.py`
- `sources/iq-sex-diff/nlsy79_first_pass.py`

**Output tables:**

- `sources/iq-sex-diff/data/icar_first_pass.tsv`
- `sources/iq-sex-diff/data/nlsy/nlsy79_first_pass.tsv`

---

## Bottom Line

The first empirical pass does **not** support the simple story that the observed pattern is mostly a between-family artifact or mostly a composite-weighting trick.

What it does support is a more structured position:

1. inside `ICAR`, all four domains are male-leaning and the composite remains male-leaning across the full frozen weight grid
2. inside `NLSY79`, the large clerical-speed female advantages and large mechanical male advantages survive strongly within opposite-sex sibling pairs
3. quantitative / math results are more mixed than the mechanical and clerical results

That hardens `H2` and weakens the strong form of `H4`. It does **not** settle `H3`, because within-family persistence is still compatible with within-household schooling or practice differences.

## ICAR

### Domain Gaps

Negative values favor males. Positive values favor females.

| score | female `n` | male `n` | `d` |
|---|---:|---:|---:|
| `ln` | 45,483 | 23,129 | `-0.162` |
| `mr` | 45,698 | 23,063 | `-0.147` |
| `r3d` | 26,967 | 13,586 | `-0.300` |
| `vr` | 51,226 | 25,993 | `-0.218` |

### Composite Sensitivity

| composite | female `n` | male `n` | `d` |
|---|---:|---:|---:|
| `equal_weights` | 18,545 | 9,430 | `-0.275` |
| `verbal_heavy` | 18,545 | 9,430 | `-0.258` |
| `matrix_heavy` | 18,545 | 9,430 | `-0.248` |
| `spatial_heavy` | 18,545 | 9,430 | `-0.307` |

### Interpretation

- `R3D` is the strongest male-leaning domain in this open battery.
- The composite gap moves across weights, but the movement range is only about `0.059` SD from `-0.248` to `-0.307`.
- That is below the DOE threshold for a large composite movement (`0.15` SD).
- So battery composition matters here, but not enough inside `ICAR` to manufacture a null or female-leaning result.

## NLSY79

### Raw Weighted Gaps

Negative values favor males. Positive values favor females.

| score | raw weighted gap |
|---|---:|
| `coding_speed` | `+0.444` |
| `numerical_operations` | `+0.235` |
| `clerical_speed` | `+0.350` |
| `paragraph_comprehension` | `+0.184` |
| `verbal` | `+0.107` |
| `word_knowledge` | `+0.028` |
| `arithmetic_reasoning` | `-0.259` |
| `quantitative` | `-0.183` |
| `math_knowledge` | `-0.081` |
| `auto_shop` | `-1.194` |
| `mechanical_comprehension` | `-0.774` |
| `electronic_information` | `-0.771` |
| `mechanical` | `-1.025` |
| `mechanical_plus_electronic` | `-0.974` |

### Within-Family Pair Estimates

Primary sibling surface uses the locked opposite-sex pair file with age and older-sibling adjustments.

| score | primary pair FE | strict `6/7` pair FE |
|---|---:|---:|
| `coding_speed` | `+0.431` | `+0.431` |
| `numerical_operations` | `+0.273` | `+0.281` |
| `clerical_speed` | `+0.363` | `+0.368` |
| `paragraph_comprehension` | `+0.183` | `+0.179` |
| `verbal` | `+0.125` | `+0.125` |
| `word_knowledge` | `+0.063` | `+0.066` |
| `arithmetic_reasoning` | `-0.195` | `-0.186` |
| `quantitative` | `-0.107` | `-0.096` |
| `math_knowledge` | `-0.005` | `+0.007` |
| `auto_shop` | `-0.959` | `-0.934` |
| `mechanical_comprehension` | `-0.603` | `-0.590` |
| `electronic_information` | `-0.595` | `-0.593` |
| `mechanical` | `-0.812` | `-0.792` |
| `mechanical_plus_electronic` | `-0.765` | `-0.751` |

### Pair-Surface Stability

- The locked primary file contains `1,461` opposite-sex pairs.
- `1,309` of those pairs have explicit `brother / sister` relationship codes on both sides.
- The strict explicit-code sensitivity is very close to the primary surface.
- That means the sibling-marker fallback is not driving the main result.

### Interpretation

- The large female clerical-speed pattern survives within family almost unchanged.
- The large male mechanical / auto / electronic pattern also survives within family almost unchanged.
- `Math Knowledge` is the main exception: the raw male advantage is small and collapses to roughly zero within family.
- `Quantitative` attenuates meaningfully but does not vanish.

## Hypothesis Impact

### `H2` Domain Plus Design

Hardens.

- The domain pattern is sharp and internally coherent in `NLSY79`.
- `ICAR` also shows domain-specific structure rather than one generic flat gap.

### `H4` Family / Background Confounding

Softens in its strong form.

- Shared-family background does **not** explain away the biggest clerical or mechanical gaps.
- At most it explains part of the weaker quantitative pattern.

### `H3` Schooling / Practice

Still open.

- Within-family persistence does not kill this hypothesis because siblings can still receive sex-differentiated practice inside the same household or school context.
- But the burden is now higher: `H3` needs to explain why the female clerical pattern remains so strong after the shared-family layer is removed.

### `H5` Outcome Overreach

Untested in this pass.

- No outcome models were run yet.

## Limits

1. `ICAR` is still a convenience sample with planned missingness.
2. `NLSY79` age-at-test is proxied by `AGE OF R 81`.
3. The pair model uses `# SIBS OLDER THAN R 79` as a birth-order proxy rather than a direct birth-order field.
4. The `NLSY79` pair surface is unweighted by design.
5. This pass did not run mediation, invariance, or outcome models.

## Best Next Steps

1. Run the `NLSY79` schooling / practice attenuation pass with the frozen pre-test block.
2. Build the `NLSY97` CAT-ASVAB signed ability scores and replicate the domain pattern by cohort.
3. Start `PIAAC p1` only for the education-stratified cross-country analysis.

That sequence now has a real empirical reason behind it: the first-pass results show where the signal is strong enough to deserve a more causal second pass.
