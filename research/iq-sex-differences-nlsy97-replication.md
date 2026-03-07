# IQ Sex Differences NLSY97 Replication

**Date:** 2026-03-05
**Scope:** `NLSY97` CAT-ASVAB descriptive replication after correcting the respondent-sex field
**Script executed:** `sources/iq-sex-diff/nlsy97_stats_pipeline.py`

**Environment:**

- `sources/iq-sex-diff/pyproject.toml`
- `sources/iq-sex-diff/uv.lock`

**Output tables:**

- `sources/iq-sex-diff/data/nlsy/nlsy97_stats_pipeline.tsv`
- `sources/iq-sex-diff/data/nlsy/nlsy97_signed_score_diagnostics.tsv`

---

## Bottom Line

The `NLSY97` cohort does **not** give a simple “everything is the same” replication of `NLSY79`.

What it does show is:

1. the female clerical-speed and verbal pattern still exists
2. the male mechanical pattern still exists
3. the quantitative pattern shifts materially, from male-leaning in `NLSY79` to near-zero or slightly female-leaning in `NLSY97`

So the cross-cohort evidence now points to a mixed conclusion:

- the broad domain structure is fairly stable
- the **magnitude** and even **sign** of some domains can shift across cohorts and test formats

That hardens the claim that the sex-difference story is domain-specific and measurement-sensitive, not battery-invariant.

## Core Weighted Gaps

Positive values favor females. Negative values favor males.

| score | `NLSY97` weighted gap | `95%` CI |
|---|---:|---:|
| `coding_speed` | `+0.368` | `(+0.314, +0.423)` |
| `numerical_operations` | `+0.169` | `(+0.115, +0.223)` |
| `clerical_speed` | `+0.262` | `(+0.208, +0.316)` |
| `paragraph_comprehension` | `+0.251` | `(+0.197, +0.304)` |
| `word_knowledge` | `+0.009` | `(-0.045, +0.062)` |
| `verbal` | `+0.138` | `(+0.084, +0.192)` |
| `arithmetic_reasoning` | `-0.044` | `(-0.097, +0.010)` |
| `math_knowledge` | `+0.143` | `(+0.090, +0.197)` |
| `quantitative` | `+0.054` | `(+0.001, +0.108)` |
| `auto_information` | `-0.499` | `(-0.552, -0.445)` |
| `shop_information` | `-0.649` | `(-0.703, -0.596)` |
| `mechanical_comprehension` | `-0.291` | `(-0.345, -0.238)` |
| `electronic_information` | `-0.347` | `(-0.400, -0.293)` |
| `mechanical` | `-0.546` | `(-0.599, -0.492)` |
| `assembling_objects` | `+0.128` | `(+0.074, +0.181)` |
| `general_science` | `-0.157` | `(-0.210, -0.103)` |
| `math_verbal_percentile` | `+0.079` | `(+0.025, +0.132)` |

## Cross-Cohort Read

Matched domain comparison against the current `NLSY79` weighted surfaces:

| domain | `NLSY79` | `NLSY97` | read |
|---|---:|---:|---|
| `clerical_speed` | `+0.369` | `+0.262` | female advantage persists, smaller in later cohort |
| `verbal` | `+0.113` | `+0.138` | female advantage persists |
| `quantitative` | `-0.179` | `+0.054` | meaningful cohort shift, including sign flip |
| `mechanical` | `-1.079` | `-0.546` | male advantage persists, smaller in later cohort |

This is not the footprint of one stable global latent gap. It is the footprint of a structured domain pattern whose magnitude depends on cohort and measurement surface.

## Signed `POS/NEG` Score Diagnostics

The CAT-ASVAB public-use fields store positive and negative sides separately. The frozen combine rule is:

- `signed = POS` when only `POS` is observed
- `signed = -NEG` when only `NEG` is observed
- `signed = POS - NEG` only when both are nonmissing

The diagnostic table shows this is mostly clean in practice:

- most subtests have either `POS` or `NEG`, not both
- only `general_science` had any `both_nonmissing` cases, and there were only `5`
- the rest of the score surface is effectively a one-side sign reconstruction rather than a noisy two-field merge

That means the `POS/NEG` combine rule does not look like the main driver of the observed cohort pattern.

## Interpretation

### What Replicates

- female advantage on `coding_speed`
- female advantage on `numerical_operations`
- female advantage on `paragraph_comprehension`
- male advantage on `auto_information`, `shop_information`, `mechanical_comprehension`, and `electronic_information`

### What Moves

- `math_knowledge` is female-leaning in `NLSY97`
- `quantitative` moves from male-leaning in `NLSY79` to slightly female-leaning in `NLSY97`
- the male mechanical composite remains large, but much smaller than in `NLSY79`

## Causal Update

### `H2` Domain Pattern

Still hardens.

- the later cohort keeps the same broad clerical / verbal versus mechanical split

### `H3` Schooling / Practice

Gets some support, but not a monopoly.

- the quantitative sign flip and smaller mechanical magnitude are compatible with cohort-level schooling / practice / exposure shifts
- but the broad domain structure does not disappear

### `H6` Cohort / Selection

Hardens.

- the cohort comparison now shows that some domains are materially cohort-sensitive

## Causal-Check Summary

- `P(cause)`: `0.60` that the stable part of the pattern is domain-specific, while the moving part is driven by cohort / measurement / practice differences rather than one invariant latent gap
- `Top alternative`: `0.25` that CAT-ASVAB scoring or sample-composition differences are producing more of the cross-cohort movement than genuine cohort change
- `Falsifier`: a matched-cohort or alternative battery replication showing the same quantitative sign in both cohorts after harmonized scoring
- `Decision impact`: treat `NLSY79` quantitative results as cohort-contingent, but treat the clerical-versus-mechanical split as the more stable empirical signal

## Best Next Steps

1. move to `PIAAC p1` for education-stratified cross-country checks on the clerical, verbal, and quantitative channels
2. revisit the quantitative node specifically, because it is now the main place where the cohort story changes sign
3. test whether the smaller `NLSY97` mechanical gap is a cohort effect, a CAT-ASVAB effect, or a domain-harmonization issue
