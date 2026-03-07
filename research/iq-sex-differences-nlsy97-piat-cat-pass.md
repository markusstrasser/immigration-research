# IQ Sex Differences - NLSY97 PIAT vs CAT Pass

**Date:** 2026-03-05
**Purpose:** test whether the `NLSY97` quantitative sign flip looks like a broad youth math advantage for females, or a narrower test-surface wedge inside the same cohort.

Script: [nlsy97_piat_cat_pass.py](/Users/alien/Projects/research/sources/iq-sex-diff/nlsy97_piat_cat_pass.py)

Outputs:

- [nlsy97_piat_cat_extract.parquet](/Users/alien/Projects/research/sources/iq-sex-diff/data/nlsy/nlsy97_piat_cat_extract.parquet)
- [nlsy97_piat_cat_overlap_extract.parquet](/Users/alien/Projects/research/sources/iq-sex-diff/data/nlsy/nlsy97_piat_cat_overlap_extract.parquet)
- [nlsy97_piat_cat_surface_gaps.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/nlsy/nlsy97_piat_cat_surface_gaps.tsv)
- [nlsy97_piat_cat_models.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/nlsy/nlsy97_piat_cat_models.tsv)
- [nlsy97_piat_cat_cross_surface.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/nlsy/nlsy97_piat_cat_cross_surface.tsv)
- [nlsy97_piat_cat_transcript_models.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/nlsy/nlsy97_piat_cat_transcript_models.tsv)

Official anchors:

- `NLSY97` CAT-ASVAB appendix: <https://www.nlsinfo.org/content/cohorts/nlsy97/other-documentation/codebook-supplement/appendix-10-cat-asvab-scores>
- `NLSY97` child assessments / PIAT: <https://www.nlsinfo.org/content/cohorts/nlsy97/topical-guide/other-assessments/child-assessments>
- `NLSY97` high school transcript survey: <https://www.nlsinfo.org/content/cohorts/nlsy97/topical-guide/education/high-school-transcript-survey>

---

## Question

The unresolved node was:

> is the `NLSY97` female-leaning quantitative result a broad youth math signal, or a battery-local surface effect?

The cleanest same-cohort falsification is `PIAT Math` versus `CAT-ASVAB` quantitative inside the overlap sample.

Why this pass matters:

1. `PIAT Math` is a second math surface inside the same cohort
2. `CAT-ASVAB` and `PIAT` can be compared on the same respondents
3. if the female-looking result is broad and latent, it should show up on both surfaces
4. if it is construct-local, the sign should diverge inside the same overlap sample

## Data Handling

### Surfaces added

- `CV_PIAT_STANDARD_SCORE_1997`
- `CV_PIAT_PERCENTILE_SCORE_1997`
- `ASVAB` test month and year
- age in months at the 1997 interview
- 1997 self-reported math-honors items
- high school transcript math surfaces:
  - `TRANS_CRD_GPA_MATH_HSTR`
  - `TRANS_MATHPIPE_HSTR`
  - `TRANS_TOT_MATH_HSTR`
  - `TRANS_TOT_ADV_MATH_HSTR`

### Important hygiene rule

The transcript and `PIAT` fields use additional negative missing codes beyond the earlier Stage A surfaces. This pass explicitly recodes those negative values to missing before any standardization or modeling. That matters because transcript variables use codes such as `-6`, `-7`, `-8`, and `-9` in the public-use file.

### Sample geometry

- weighted-sex valid `NLSY97` core: `6,748`
- nonmissing `PIAT` standard score 1997: `4,518`
- `PIAT` / `CAT` overlap with age and test-date fields: `3,738`

The official `PIAT` topical guide says the assessment was fielded in Round 1 for the age/grade-eligible youth subset, not the entire cohort. So this is a same-cohort youth-subset test, not a full-cohort generalization.

## Main Result

The female-looking `NLSY97` quantitative signal does **not** replicate as a broad math advantage on the alternate surface.

Inside the same `PIAT`/`CAT` overlap sample `n=3,738`:

- `PIAT Math`: `d = -0.046`, `95% CI (-0.110, +0.017)`
- `Arithmetic Reasoning`: `d = -0.036`, `95% CI (-0.100, +0.027)`
- `Math Knowledge`: `d = +0.132`, `95% CI (+0.071, +0.192)`
- `Quantitative = AR + MK`: `d = +0.052`, `95% CI (-0.009, +0.114)`

So the observed female-leaning signal is concentrated in `Math Knowledge`, not in `Arithmetic Reasoning`, and not on `PIAT Math`.

That is the key empirical footprint.

## Design-Only Models

Using only:

- age in months
- `ASVAB` test month
- `ASVAB` test year

the same overlap sample gives:

- `PIAT Math`: female beta `-0.052`, `95% CI (-0.114, +0.009)`
- `Arithmetic Reasoning`: female beta `-0.024`, `95% CI (-0.087, +0.039)`
- `Math Knowledge`: female beta `+0.151`, `95% CI (+0.093, +0.210)`
- `Quantitative`: female beta `+0.069`, `95% CI (+0.009, +0.130)`

So basic design alignment does not collapse the split. If anything, it sharpens it.

## Cross-Surface Wedge

The strongest diagnostic models are the conditional cross-surface fits.

### Conditional on `PIAT Math`

From [nlsy97_piat_cat_cross_surface.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/nlsy/nlsy97_piat_cat_cross_surface.tsv):

- `Quantitative ~ female + PIAT + age + test date`:
  - female beta `+0.109`
  - `95% CI (+0.070, +0.147)`
- `Arithmetic Reasoning ~ female + PIAT + age + test date`:
  - female beta `+0.015`
  - `95% CI (-0.027, +0.058)`
- `Math Knowledge ~ female + PIAT + age + test date`:
  - female beta `+0.188`
  - `95% CI (+0.147, +0.228)`

### Conditional on `CAT Quantitative`

- `PIAT ~ female + quantitative + age + test date`:
  - female beta `-0.106`
  - `95% CI (-0.145, -0.067)`

Interpretation:

1. once `PIAT Math` is held fixed, the female residual lives almost entirely in `Math Knowledge`
2. once `CAT quantitative` is held fixed, `PIAT Math` still tilts male
3. that is not the footprint of one broad female math advantage
4. it is the footprint of a real same-cohort surface wedge

## Transcript Math Surfaces

Later high school transcript math surfaces remain female-favoring:

- transcript math GPA full-valid `d = +0.218`
- transcript math pipe full-valid `d = +0.085`
- transcript total math credits full-valid `d = +0.094`

And they stay female-favoring even conditional on `PIAT` or conditional on `CAT quantitative`:

- `transcript_math_gpa ~ female + PIAT + age + test date`: female beta `+0.259`
- `transcript_math_gpa ~ female + quantitative + age + test date`: female beta `+0.215`

That does **not** show that girls have higher IQ.

It does show that school-linked math outputs inside `NLSY97` move in a different direction from the alternate youth test surface.

## Causal Read

### What this pass hardens

1. The `NLSY97` anomaly is **not** a broad same-cohort female math result.
2. The anomaly is more local than the earlier project state allowed.
3. The local female-looking signal is concentrated in `Math Knowledge` and school-linked transcript surfaces.
4. `Arithmetic Reasoning` and `PIAT Math` do not carry the same female edge.

### What this pass weakens

1. a generic "girls are ahead on youth quantitative ability in `NLSY97`" story
2. a pure process-only explanation, because the divergence is not broad across the entire `CAT` quantitative surface
3. a same-sample missingness-only story, because the wedge survives inside the explicit overlap sample

### Best current explanation

The most defensible read is:

> the `NLSY97` sign flip is mainly a construct-local school-knowledge surface effect, not evidence of a broad female quantitative advantage.

That still leaves open whether the local surface difference is driven more by:

- item content / format
- curriculum exposure
- evaluation / placement channels
- some mixture of all three

But it is no longer clean to describe `NLSY97` as a simple counterexample to the male-leaning quantitative / numeracy pattern.

## Causal-Check Update

- `P(cause)`: `0.60` that the `NLSY97` quantitative anomaly is mainly a battery-local construct / item-family / school-knowledge surface effect.
- `Top alternative`: `0.20` that recent course exposure and school-linked knowledge accumulation create a real near-school-exit female edge on learned-math surfaces.
- `Falsifier`: a same-age youth battery where `PIAT`-like and `CAT Math Knowledge`-like surfaces point the same direction after aligned age and timing adjustment.
- `Decision impact`: stop using raw `NLSY97 quantitative` as generic evidence about overall quantitative ability or IQ; use it as evidence about a narrower `Math Knowledge`-heavy school-exit surface.

## Limitations

1. `PIAT` is only available for the youth-eligible subset, not the entire `NLSY97` cohort.
2. transcript variables are collected later and are selection-sensitive; they are useful mechanism surfaces, not clean nuisance controls.
3. this pass still does not have item-level `CAT` routing or DIF decomposition, so the exact item-family mechanism remains open.

## Best Next Step

The next highest-value analyses are now:

1. item-family and format decomposition in `PISA 2018` / `TIMSS 2019`, especially applied/problem-solving versus learned school-knowledge surfaces
2. `ELS` or further `HSLS` transcript replication of the grade / test / ladder wedge
3. if feasible, a deeper `NLSY97` transcript-course pass using the high school transcript course payload rather than only the derived summary fields
