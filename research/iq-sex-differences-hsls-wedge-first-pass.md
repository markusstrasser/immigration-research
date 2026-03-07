# IQ Sex Differences - HSLS Wedge First Pass

**Date:** 2026-03-05
**Purpose:** first transcript-rich `HSLS:09` pass on the grade-test wedge and
course-ladder node using the newly staged public-use respondent file.

**Primary files:**

- `sources/iq-sex-diff/hsls_wedge_first_pass.py`
- `sources/iq-sex-diff/data/hsls/hsls_wedge_extract.parquet`
- `sources/iq-sex-diff/data/hsls/hsls_wedge_frontier_sample.tsv`
- `sources/iq-sex-diff/data/hsls/hsls_wedge_overall.tsv`
- `sources/iq-sex-diff/data/hsls/hsls_wedge_by_ladder.tsv`
- `sources/iq-sex-diff/data/hsls/hsls_wedge_models.tsv`

## Bottom Line

The first `HSLS` pass finds a real school-surface wedge.

In the transcript-covered core sample (`n = 13,506`), girls are near parity at
baseline math, slightly below boys on the later standardized math surface, but
substantially above boys on transcript math GPA. That wedge persists inside the
common highest-math ladders.

So the project should stop treating transcript GPA or course placement as clean
ability proxies. But this does **not** prove simple female underplacement or
simple teacher bias as the whole mechanism.

## Observation Geometry

> **Observation:** in the transcript-covered `HSLS` core sample, weighted
> female-minus-male differences are `d = -0.017` at baseline math
> (`X1TXMTSCOR`), `d = -0.046` at the later math test (`X2TXMTSCOR`), but
> `d = +0.247` for transcript math GPA (`X3TGPAMAT`) and `d = +0.208` for GPA
> in the highest math course (`X3TGPAHIMTH`). [SOURCE:
> `sources/iq-sex-diff/data/hsls/hsls_wedge_overall.tsv`]
>
> **Null:** if transcript GPA, course placement, and standardized math all track
> the same latent math surface closely once prior math is known, then sex gaps
> should shrink toward zero and point in the same direction across those
> surfaces. [INFERENCE]
>
> **Residual after null:** the gaps point in opposite directions even within the
> same transcript-defined highest-math ladders. [SOURCE:
> `sources/iq-sex-diff/data/hsls/hsls_wedge_by_ladder.tsv`]
>
> **Geometry:** persistent cross-surface wedge, not a single all-surface gap.
> [INFERENCE]
>
> **Magnitude:** controlled female coefficient is about `-0.051` on the later
> math test but `+0.227` on transcript math GPA once baseline math, ladder, and
> credits are included. [SOURCE:
> `sources/iq-sex-diff/data/hsls/hsls_wedge_models.tsv`]
>
> **Lag window:** baseline grade-9 math to later school transcript surfaces.
> [SOURCE: `sources/iq-sex-diff/data/hsls/hsls_wedge_models.tsv`]

## Raw Surface Audit

The working public-use file was:

- `sources/iq-sex-diff/data/hsls/HSLS_2017_PETS_SR_v1_0_SPSS_Datasets.zip`

The core overlap required:

1. valid sex
2. positive transcript-compatible weight `W3W1W2STUTR`
3. transcript coverage `X3TCOVERAGE = 1`
4. nonmissing baseline math, later math, highest-math ladder, transcript math
   GPA, and highest-math GPA

That yields:

- `core_n = 13,506`

The public-use file does carry the needed surfaces directly:

- baseline and later math scores: `X1TXMTSCOR`, `X2TXMTSCOR`
- transcript ladder: `X3THIMATH`
- transcript math credits: `X3TCREDMAT`, `X3TCREDAPMTH`
- transcript GPA surfaces: `X3TGPAMAT`, `X3TGPAHIMTH`, `X3TGPAWGT`
- transcript-compatible longitudinal weight: `W3W1W2STUTR`

## Main Results

### Overall weighted gaps

From `sources/iq-sex-diff/data/hsls/hsls_wedge_overall.tsv`:

- baseline math: `d = -0.017`
- later math test: `d = -0.046`
- transcript math GPA: `d = +0.247`
- highest-math-course GPA: `d = +0.208`
- honors-weighted overall GPA: `d = +0.348`
- total math credits: `d = +0.076`
- AP/IB math credits: `d = -0.021`

That is already enough to say the transcript surface is not just mirroring the
standardized math surface.

### Within common highest-math ladders

From `sources/iq-sex-diff/data/hsls/hsls_wedge_by_ladder.tsv`:

- `Algebra II`: test `d = -0.109`, GPA `d = +0.232`
- `Precalculus`: test `d = -0.126`, GPA `d = +0.209`
- `AP/IB Calculus`: test `d = -0.234`, GPA `d = +0.153`
- `Calculus`: test `d = -0.139`, GPA `d = +0.161`
- `Probability and statistics`: test `d = -0.116`, GPA `d = +0.412`

So the wedge is not just “girls take different courses.” It remains visible
inside the same highest-math course categories.

### Weighted model table

From `sources/iq-sex-diff/data/hsls/hsls_wedge_models.tsv`:

- later math test with baseline + ladder + credits:
  - `beta_female = -0.051`
  - `95% CI = [-0.087, -0.015]`
- transcript math GPA with baseline + current test + ladder + credits:
  - `beta_female = +0.227`
  - `95% CI = [0.185, 0.268]`
- highest-math-course GPA with the same block:
  - `beta_female = +0.195`
  - `95% CI = [0.148, 0.242]`
- `precalc_plus ~ female + baseline_math`:
  - `beta_female = +0.041`
  - `95% CI = [0.017, 0.065]`

That last line matters: this does **not** look like a simple story where girls
are held out of advanced math given the same baseline.

## Causal Read

### What this does support

1. `HSLS` contains a real grade-test wedge on the school-math surface.
2. Grades and some placement surfaces are not interchangeable with standardized
   math.
3. A simple “girls are just obviously better on school math” reading is too
   strong, because the standardized test surface remains slightly male-leaning.
4. A simple “girls are just underplaced” reading is also too strong, because
   girls are slightly more likely to reach `precalculus+` conditional on
   baseline math in this first pass.

### What this does not support

1. It does **not** prove teacher bias as the dominant mechanism.
2. It does **not** prove the `HSLS` math test is itself sex-biased.
3. It does **not** prove anything final about latent general ability.

## Causal-Check Verdict

- `P(cause) = 0.55` that the main school-surface story here is a real
  evaluation / performance / transcript wedge: grades and course-linked school
  outputs encode something systematically more female-favoring than the tested
  math surface. [INFERENCE]
- `Top alternative = 0.25`: the `HSLS` standardized math surface itself is
  missing female-relevant classroom competence or is format-sensitive enough to
  understate female performance. This is less specific because the current pass
  does not yet use item/process data. [INFERENCE]
- `Falsifier`: a transcript-rich replication showing that once baseline math,
  course ladder, and transcript completeness are aligned, the GPA/test wedge
  shrinks near zero or flips to the same sign across surfaces. [INFERENCE]
- `Decision impact`: treat grades and course-placement variables as mechanism
  surfaces or strata, not as clean nuisance controls in the main causal model.
  Also stop using a generic “female underplacement” story as the default
  transcript explanation. [INFERENCE]

## Why `HSLS` Won The First Pass

`ELS` remains useful, but the immediate public-use `HSLS` surface was cleaner
for this question.

On the first raw audit:

- `HSLS` exposed varying transcript ladder, transcript GPA, transcript credits,
  and score variables directly in the staged student file
- several candidate `ELS` transcript summary variables appeared non-varying or
  effectively unusable in the first public-use pass, so it was the worse first
  surface for this exact wedge analysis

That is a workflow decision, not a final judgment on `ELS`.

## Next Best Moves

1. `ELS` viability audit:
   - determine which transcript/GPA/course variables survive in usable public
     form
   - replicate the wedge if the overlap is real
2. `NLSY97` same-cohort `PIAT Math` versus `CAT-ASVAB`:
   - test whether the `HSLS` wedge pattern appears inside the cohort that
     generated the raw female quantitative anomaly
3. `PISA 2018` / `eTIMSS` process pass:
   - test whether item format and process traces explain part of the remaining
     school-test surface
