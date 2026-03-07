# IQ Sex Differences - Early-School ACH

**Date:** 2026-03-05
**Purpose:** apply Analysis of Competing Hypotheses plus causal-check discipline to the active early-school anomaly:

> why does `NLSCYA` `PIAT Math` show an early female-leaning / parity-moving shape while the two `ECLS` broad school-entry math surfaces are male-leaning by early grade school?

This is a causal memo, not a new modeling pass.

---

## Phase 1 - Framing

**Observation:** in the current local early-school tranche, `NLSCYA` `PIAT Math` standard scores are female-leaning at ages roughly `7.5` to `9.1` (`d = +0.074`, `+0.059`, `+0.024`), while `ECLS-K:2011` broad school-entry math is near parity in kindergarten and male-leaning by spring first / second grade (`d = -0.029`, `-0.004`, `+0.019`, `-0.095`, `-0.142`, `-0.159`), and older `ECLS-K` broad school-entry math is male-leaning from kindergarten through spring first (`d = -0.024`, `-0.041`, `-0.042`, `-0.091`). [DATA: `sources/iq-sex-diff/data/nlscya/nlscya_early_school_surface_gaps.tsv`; `sources/iq-sex-diff/data/ecls_k2011/eclsk2011_early_school_surface_gaps.tsv`; `sources/iq-sex-diff/data/ecls_k/eclsk_early_school_surface_gaps.tsv`]

**Geometry:** isolated surface split, not a single temporal break. Two broad `ECLS` school-entry surfaces align with each other while a different child math surface (`PIAT Math`) does not.

**Null process:** different child batteries and sampling frames can produce modestly different mean gaps even if there is no single battery-invariant latent-sex-gap object. Given the project’s broader evidence, some cross-surface drift is expected without invoking a new deep cause.

**Residual after null:** the divergence is too structured to call random drift. The two `ECLS` cohorts line up directionally on math and reading, while `NLSCYA` diverges specifically on math.

**Domain:** mixed psychometric + sampling + developmental.

**Base-rate prior:** the wider repo already gives measurement / construct mismatch a high base rate because `NLSY97`, `TIMSS`, `PISA`, and `PIAAC` all showed surface-sensitive sex-gap geometry. [SOURCE: `research/iq-sex-differences-current-position.md`]

---

## Phase 2 - Hypotheses

Priors sum to `1.00`.

1. `H1` Measurement / score-family mismatch (`0.40`)
   - `PIAT Math` and the `ECLS` broad school-entry IRT scales do not measure the same child math surface closely enough, so the sex-gap geometry differs mainly because of construct / scaling / age-surface mismatch.
2. `H2` Sample / composition mismatch (`0.25`)
   - `NLSCYA` differs mainly because it follows children born to `NLSY79` mothers rather than a nationally representative kindergarten class, so the observed split is driven more by sample frame than by test surface.
3. `H3` Real cohort / developmental shift (`0.20`)
   - the difference is mostly real population change across cohorts or ages, not a test-surface problem.
4. `H4` Data artifact / extraction / weighting error (`0.15`)
   - one or more of the local early-school results is materially wrong because of archive, parser, or weight handling error.

---

## Phase 3 - Predicted Data Footprints

Likelihoods are `P(evidence | hypothesis)`.

| Evidence | If `H1` | If `H2` | If `H3` | If `H4` |
| --- | ---: | ---: | ---: | ---: |
| `E1` Two independent `ECLS` cohorts align directionally on broad math and reading | `0.80` | `0.60` | `0.25` | `0.20` |
| `E2` `NLSCYA` uses `PIAT Math` at older child ages while `ECLS` uses school-entry IRT math scales | `0.90` | `0.55` | `0.35` | `0.30` |
| `E3` Other batteries in the repo already show content-family / score-surface sensitivity (`Math Knowledge`, `knowing`, advanced reasoning) | `0.85` | `0.35` | `0.25` | `0.15` |
| `E4` `NLSCYA` sample frame differs from `ECLS` national kindergarten cohorts | `0.50` | `0.90` | `0.30` | `0.25` |
| `E5` After archive repair, older `ECLS-K` still matches `ECLS-K:2011`, reducing pure local-artifact risk | `0.70` | `0.65` | `0.40` | `0.10` |

---

## Phase 4 - Evidence

### `E1` Broad `ECLS` replication

**Query**

- `cat sources/iq-sex-diff/data/ecls_k2011/eclsk2011_early_school_surface_gaps.tsv`
- `cat sources/iq-sex-diff/data/ecls_k/eclsk_early_school_surface_gaps.tsv`

**Finding**

- `ECLS-K:2011` and older `ECLS-K` are directionally aligned on broad early-school math and reading.
- Both show female-leaning reading and male-leaning broad math by early grade school.

**Most supports:** `H1`

### `E2` Score-family / age-surface mismatch

**Query**

- `cat sources/iq-sex-diff/data/nlscya/nlscya_early_school_surface_gaps.tsv`
- local extraction code and variable maps

**Finding**

- `NLSCYA` uses `PIAT Math` standard scores with mean ages around `7.5` to `9.1` in the current first pass.
- `ECLS` uses broad school-entry IRT math scales from kindergarten / first-grade waves.

**Most supports:** `H1`

### `E3` Cross-battery consistency outside early school

**Query**

- read `research/iq-sex-differences-nlsy97-piat-cat-pass.md`
- read `research/iq-sex-differences-timss-cognitive-split.md`
- read `research/iq-sex-differences-pisa2018-framework-proxy.md`

**Finding**

- the broader repo already shows that sex-gap geometry changes with surface family:
  - `NLSY97` female-looking signal is localized to `Math Knowledge`
  - `TIMSS` `knowing` shifts differently from advanced `reasoning`
  - `PISA` content-family heterogeneity is structured rather than random

**Most supports:** `H1`

### `E4` Sample-frame mismatch

**Query**

- official cohort pages

**Finding**

- the `NLSY79 Child` sample is comprised of children born to `NLSY79` mothers, not a nationally representative kindergarten class. [SOURCE: <https://www.nlsinfo.org/content/cohorts/nlsy79-children/intro-to-the-sample/sample-design>; <https://www.nlsinfo.org/content/cohorts/nlsy79-children/intro-to-the-sample/nlsy79-childyoung-adult-sample-introduction>]
- older `ECLS-K` is a nationally representative sample of children in kindergarten in `1998-99`. [SOURCE: <https://nces.ed.gov/fCSM/eclsk.asp>; <https://nces.ed.gov/statprog/handbook/ecls_surveydesign.asp>]
- `ECLS-K:2011` is a nationally representative sample of children in kindergarten in `2010-11`. [SOURCE: <https://nces.ed.gov/ecls/kindergarten2011.asp>; <https://nces.ed.gov/fCSM/eclsk2011.asp>]

**Most supports:** `H2`

### `E5` Artifact audit

**Query**

- archive repair path for older `ECLS-K`
- compare final older `ECLS-K` result with `ECLS-K:2011`

**Finding**

- the older `ECLS-K` archive was painful, but the final repaired result still matches the independently extracted `ECLS-K:2011` directionally.
- that weakens a pure “local parser / weight bug created the pattern” story.

**Most supports:** `H1`

---

## Phase 5 - ACH Scoring

Raw Bayesian update using the priors and likelihoods above:

| Hypothesis | Prior | Posterior |
| --- | ---: | ---: |
| `H1` Measurement / score-family mismatch | `0.40` | `0.831` |
| `H2` Sample / composition mismatch | `0.25` | `0.164` |
| `H3` Real cohort / developmental shift | `0.20` | `0.005` |
| `H4` Data artifact / extraction / weighting error | `0.15` | `0.0003` |

**Separation:** log-odds gap between `H1` and `H2` is about `1.62`, which is strong by the skill’s threshold.

**Prior sensitivity:** even halving the `H1` prior leaves it ahead (`0.711` versus `0.280` for `H2`), so the verdict is not a fragile prior trick.

Important caveat:

- some evidence items are correlated, especially `E1` and `E3`
- so the raw `0.831` posterior should be read as directional evidence, not as a literal calibrated probability

Calibrated causal read after discounting that correlation:

- `P(cause) ≈ 0.70` for `H1`
- `P(cause) ≈ 0.20` for `H2`
- the rest is split between `H3` and `H4`

---

## Phase 5b - IBE Scoring

### IBE table

| Hypothesis | Scope | Specificity | Parsimony | Unification | Fertility | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `H1` Measurement / score-family mismatch | `5` | `4` | `4` | `5` | `5` | `23` |
| `H2` Sample / composition mismatch | `3` | `3` | `3` | `2` | `3` | `14` |
| `H3` Real cohort / developmental shift | `2` | `2` | `3` | `1` | `2` | `10` |
| `H4` Data artifact / extraction / weighting error | `1` | `1` | `4` | `1` | `1` | `8` |

`H1` wins on unification and fertility because it predicts the exact next checks the project now needs:

1. align `PIAT Math` and `ECLS` scale families
2. find a bridge battery that carries both school-entry broad math and `PIAT`-like math
3. test whether the `NLSCYA` outlier shrinks when score family, not just cohort, is aligned

---

## Phase 3b - Recursive Causal Audit

### RCA for `H1`

**Chain:** `score family / scaling / age surface mismatch -> different child math construct emphasis -> different observed sex-gap geometry`

1. `score family -> construct emphasis`
   - directional: `yes`
   - necessary: `partly`
   - proportional: `yes`
   - confounder risk: `medium`
2. `construct emphasis -> sex-gap geometry`
   - directional: `yes`
   - necessary: `partly`
   - proportional: `yes`
   - confounder risk: `medium`

**Weakest link:** the exact `PIAT Math` versus `ECLS` construct contrast is still inferred from the broader project geometry; it has not yet been harmonized item-by-item or rescaled on a bridge sample.

**Bad controls:** none in this ACH pass.

### RCA for `H2`

**Chain:** `NLSY79 Child sample frame -> different family / age / cohort composition -> different observed early math gap`

1. `sample frame -> composition difference`
   - directional: `yes`
   - necessary: `yes`
   - proportional: `yes`
   - confounder risk: `low`
2. `composition difference -> different math gap`
   - directional: `possible`
   - necessary: `no`
   - proportional: `weak`
   - confounder risk: `high`

**Weakest link:** there is no direct evidence yet that the sample-frame difference explains the specifically math-only divergence while leaving the reading pattern aligned.

**Bad controls:** none in this ACH pass.

---

## Phase 6 - Kill or Promote

### Killed

1. `H4` Data artifact / extraction / weighting error
   - dies because the repaired older `ECLS-K` result still lines up with `ECLS-K:2011`
   - a pure local artifact would need a shared hidden bug across two different public-use cohorts and extractors
2. `H3` Real cohort / developmental shift
   - dies because the `1998-99` and `2010-11` `ECLS` cohorts are not diverging in the way this hypothesis needs
   - the older cohort does not look like `NLSCYA`; it looks like the later `ECLS`

### Surviving explanation

1. `H1` Measurement / score-family mismatch survives clearly
2. `H2` Sample / composition mismatch survives as the top alternative and likely amplifier, not the main cause

This is best read as:

- **primary cause:** score-family mismatch
- **secondary amplifier:** sample-frame difference

That is a multi-cause interpretation, but not factor-listing, because the two causes have different fingerprints:

1. `H1` explains the cross-battery geometry
2. `H2` explains why `NLSCYA` should not be expected to mirror a national kindergarten class perfectly

---

## Verdict

**Most likely cause (calibrated `70%`, strengthened by the first alignment pass):** `H1` measurement / score-family mismatch. The early-school anomaly is best explained by `PIAT Math` and the `ECLS` broad school-entry scales being different child math surfaces, with different construct emphasis and age geometry.

**Top alternative (`20%`):** `H2` sample / composition mismatch. It is real and relevant because `NLSCYA` and `ECLS` do not sample the same population frame, but it is less specific because it does not naturally explain why the divergence is math-specific while the reading direction stays aligned.

**Falsifier:** a stronger bridge analysis showing that once `PIAT Math` and `ECLS` broad school-entry math are aligned better than the current reading-anchor pass, the anomaly reopens directionally and remains just as large.

**Decision impact:** stop treating the early-school branch as a pure “which cohort wins” question. The next experiment should be score-family alignment, not another raw child-cohort pass.

---

## Evidence Summary Table

| # | Evidence | Finding | Most supports | Source |
| --- | --- | --- | --- | --- |
| `E1` | Two `ECLS` replications | both `ECLS` cohorts align on male-leaning broad math and female-leaning reading | `H1` | local TSV outputs |
| `E2` | Score-family mismatch | `NLSCYA` uses `PIAT Math` at older child ages; `ECLS` uses school-entry IRT scales | `H1` | local extraction outputs |
| `E3` | Cross-battery surface geometry | `NLSY97`, `TIMSS`, and `PISA` already show content-family-sensitive math geometry | `H1` | local memos |
| `E4` | Sample-frame mismatch | `NLSY79 Child` is children of `NLSY79` mothers; both `ECLS` cohorts are national kindergarten samples | `H2` | official cohort pages |
| `E5` | Artifact audit | repaired older `ECLS-K` still matches `ECLS-K:2011` | `H1` | local archive and output audit |

---

## Next Diagnostic Checks

1. Align `PIAT Math` and `ECLS` broad school-entry scales more tightly than the current reading-anchor pass.
2. Find a bridge battery or literature crosswalk that can say whether `PIAT Math` is closer to later school-knowledge surfaces or to broad school-entry applied math.
3. Only after that, revisit whether the remaining child-cohort disagreement is large enough to require a stronger sample-composition story.
