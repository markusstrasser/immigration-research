# IQ Sex Differences Second Pass Results

**Date:** 2026-03-05
**Scope:** `NLSY79` same-sample schooling check plus stats-stack hardening
**Scripts executed:**

- `sources/iq-sex-diff/nlsy79_schooling_pass.py`
- `sources/iq-sex-diff/nlsy79_stats_pipeline.py`

**Environment:**

- `sources/iq-sex-diff/pyproject.toml`
- `sources/iq-sex-diff/uv.lock`

**Output tables:**

- `sources/iq-sex-diff/data/nlsy/nlsy79_schooling_pass.tsv`
- `sources/iq-sex-diff/data/nlsy/nlsy79_stats_pipeline.tsv`

---

## Bottom Line

The second pass weakens the strong version of the "schooling / educator attention explains the pattern" story.

What changed is methodological, not rhetorical:

1. the earlier schooling pass mixed coefficient change with complete-case sample loss
2. the new `uv` pipeline separates:
   - the base pair estimate on all eligible pairs
   - the base estimate on the exact schooling-model sample
   - the schooling-block estimate on that same sample
3. once that is done, the clerical-speed attenuation is only modest, the verbal attenuation is real but partial, and the male-leaning quantitative / mechanical coefficients get larger in magnitude rather than collapsing

That means the schooling block looks like a **partial explanation for some verbal / clerical differences**, not a general explanation for the overall domain pattern.

## Key Same-Sample Results

Positive values favor females. Negative values favor males.

| score | weighted gap | pair FE all pairs | pair FE same sample | schooling-block same sample | attenuation |
|---|---:|---:|---:|---:|---:|
| `coding_speed` | `+0.444` | `+0.431` | `+0.439` | `+0.416` | `5.3%` |
| `numerical_operations` | `+0.235` | `+0.273` | `+0.282` | `+0.256` | `9.3%` |
| `clerical_speed` | `+0.369` | `+0.382` | `+0.391` | `+0.364` | `6.9%` |
| `paragraph_comprehension` | `+0.184` | `+0.183` | `+0.172` | `+0.141` | `18.0%` |
| `verbal` | `+0.113` | `+0.132` | `+0.120` | `+0.088` | `26.9%` |
| `arithmetic_reasoning` | `-0.259` | `-0.195` | `-0.213` | `-0.238` | `-11.7%` |
| `quantitative` | `-0.179` | `-0.105` | `-0.114` | `-0.142` | `-25.5%` |
| `auto_shop` | `-1.194` | `-0.959` | `-1.022` | `-1.043` | `-2.1%` |
| `mechanical` | `-1.079` | `-0.855` | `-0.913` | `-0.939` | `-2.9%` |
| `mechanical_plus_electronic` | `-1.031` | `-0.810` | `-0.866` | `-0.896` | `-3.4%` |

Interpretation:

- positive attenuation means the schooling block shrinks the same-sample coefficient
- negative attenuation means the same-sample coefficient moves further away from zero after the schooling block

## What Actually Attenuates

- `coding_speed`, `numerical_operations`, and `clerical_speed` attenuate only modestly: about `5%` to `9%`
- `paragraph_comprehension` and `verbal` attenuate more: about `18%` to `28%`
- the strongest male-leaning quantitative and mechanical channels do **not** attenuate; they become more male-leaning on the same complete-case sample

So the data are not consistent with a single-schooling-channel explanation that should broadly compress both female-leaning and male-leaning coefficients toward zero.

## Sample-Selection Check

The new pipeline also reports how much the complete-case restriction alone moves the coefficient before any schooling controls are added.

| score | selection shift from all-pairs base to same-sample base |
|---|---:|
| `clerical_speed` | `+0.009` |
| `verbal` | `-0.013` |
| `quantitative` | `-0.009` |
| `auto_shop` | `-0.063` |
| `mechanical` | `-0.060` |
| `mechanical_plus_electronic` | `-0.057` |

This matters because the earlier schooling pass implicitly folded these shifts into "attenuation." The clean reading is:

- some of the movement is sample composition
- the real same-sample schooling attenuation is smaller than the earlier quick pass suggested

## Robustness

- descriptive weighted gaps stay close to the first-pass magnitudes
- sibling FE estimates stay close to the first-pass magnitudes
- strict explicit `brother / sister` pairs remain close to the primary pair surface
- confidence intervals remain far from zero for the large clerical and mechanical effects

## Causal Update

### `H3` Schooling / Practice

Still alive, but narrower.

- it remains plausible for part of the female verbal / clerical edge
- it is not a good omnibus explanation for the whole pattern

### `H4` Shared-Family Confounding

Weakened further.

- once the comparison is inside families and on the same schooling-complete-case sample, the biggest coefficients persist

### `H2` Domain Pattern

Hardens again.

- the signal remains domain-specific rather than collapsing toward one small generic coefficient

## Data-Artifact Note

The execution work surfaced a real manifest bug before cohort replication:

- the frozen `NLSY97` sex field in the first config was wrong for this public extract
- `R0001000` is largely missing here
- the usable respondent sex field is `R0536300` / `KEY!SEX_1997`

That correction is now in `sources/iq-sex-diff/stage0_config.py`. It is a concrete example of why the "data artifact / measurement layer" has to stay in the causal graph.

## Best Next Steps

1. move to `PIAAC p1` education-stratified cross-country models now that the cohort replication is in hand
2. revisit the quantitative node specifically, because the `NLSY79` and `NLSY97` surfaces now disagree on its sign
3. look for richer pre-test practice or schooling proxies before making any stronger causal claim about the female verbal / clerical edge

## Causal-Check Summary

- `P(cause)`: `0.65` that schooling / practice explains a **minority** of the female verbal / clerical edge but not the large mechanical pattern
- `Top alternative`: `0.25` that the schooling block is still too crude and the remaining attenuation is mostly measurement / proxy error rather than real causal insulation
- `Falsifier`: a richer pre-test schooling / practice block that compresses the same-sample clerical and verbal coefficients by `40%+` while leaving sample composition stable
- `Decision impact`: treat schooling as a local channel to test harder, not as the master explanation for the sex-difference structure
