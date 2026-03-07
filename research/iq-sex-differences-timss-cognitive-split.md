# IQ Sex Differences - TIMSS Cognitive Split

**Date:** 2026-03-05
**Purpose:** test whether the `NLSY97` `Math Knowledge` wedge has a broader footprint in school-math batteries by separating `TIMSS` into `knowing`, `applying`, and `reasoning` surfaces.

Script: [timss_cognitive_split.py](/Users/alien/Projects/research/sources/iq-sex-diff/timss_cognitive_split.py)

Inputs:

- [timss_2019_grade_gaps.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/timss_grade_compare/timss_2019_grade_gaps.tsv)
- [timss_2019_grade_summary.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/timss_grade_compare/timss_2019_grade_summary.tsv)
- [timss_2019_grade_paired_deltas.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/timss_grade_compare/timss_2019_grade_paired_deltas.tsv)
- [timss_advanced_2015_gaps.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/timss_advanced/timss_advanced_2015_gaps.tsv)
- [timss_advanced_2015_summary.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/timss_advanced/timss_advanced_2015_summary.tsv)

Outputs:

- [timss_cognitive_grade_summary.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/timss_cognitive_split/timss_cognitive_grade_summary.tsv)
- [timss_cognitive_grade_paired.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/timss_cognitive_split/timss_cognitive_grade_paired.tsv)
- [timss_cognitive_grade_contrasts.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/timss_cognitive_split/timss_cognitive_grade_contrasts.tsv)
- [timss_cognitive_advanced_summary.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/timss_cognitive_split/timss_cognitive_advanced_summary.tsv)
- [timss_cognitive_advanced_contrasts.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/timss_cognitive_split/timss_cognitive_advanced_contrasts.tsv)

Official sources:

- TIMSS 2019 international database: <https://timssandpirls.bc.edu/timss2019/international-database/>
- TIMSS Advanced 2015 international database: <https://timssandpirls.bc.edu/timss2015/advanced/international-database/>

---

## Question

The `NLSY97` same-cohort pass showed:

1. `Math Knowledge` female-leaning
2. `Arithmetic Reasoning` near null / slightly male
3. `PIAT Math` near null / slightly male

That suggests a narrower school-knowledge surface, not one generic math gap.

The `TIMSS` question is:

> does broad school math show the same kind of split when we separate `knowing` from `applying` and `reasoning`?

## Main Result

Yes, with an age-and-track twist.

### Grade 4

- `overall_math`: `d = -0.069`
- `knowing`: `d = -0.111`
- `applying`: `d = -0.043`
- `reasoning`: `d = -0.097`

At Grade 4, `knowing` is actually **more male-leaning** than `applying`, not less.

### Grade 8

- `overall_math`: `d = +0.017`
- `knowing`: `d = +0.029`
- `applying`: `d = -0.002`
- `reasoning`: `d = +0.017`
- `algebra`: `d = +0.088`

By Grade 8, `knowing` becomes the most female-tilting cognitive surface in the broad school sample, with `applying` closest to parity.

### Grade 8 minus Grade 4 shift

Across overlap countries:

- `overall_math`: `+0.076`
- `knowing`: `+0.139`
- `reasoning`: `+0.113`
- `applying`: `+0.043`

So the largest femaleward shift is in `knowing`, not in `applying`.

### TIMSS Advanced 2015

Upper-track advanced math flips back male:

- `overall_advanced_math`: `d = -0.148`
- `knowing`: `d = -0.127`
- `applying`: `d = -0.111`
- `reasoning`: `d = -0.195`
- `geometry`: `d = -0.205`
- `algebra`: `d = -0.142`
- `calculus`: `d = -0.105`

So the broad-population Grade 8 femaleward move does not carry into the advanced-track surface.

## What This Means

This does **not** perfectly replicate the `NLSY97` pattern.

It does something more useful:

1. it shows that school-math sex gaps are highly sensitive to cognitive subtype and academic stage
2. it shows that `knowing` moves femaleward faster than `applying` from Grade 4 to Grade 8
3. it shows that upper-track advanced math remains male-leaning across all cognitive domains, especially `reasoning`

That is directionally consistent with a **school-knowledge / curriculum / track** story, not with one simple latent general-math difference.

## Best Causal Read

### What this strengthens

1. The live `NLSY97` anomaly is unlikely to be a pure fluke.
2. School-knowledge-heavy surfaces can move differently from other math surfaces.
3. Track selection matters enough to reverse broad-population direction by the time we reach advanced mathematics.

### What this weakens

1. a single “boys better at math” story
2. a single “girls better at school math” story
3. the idea that one cognitive-domain label settles the latent-trait question

### Cleanest synthesis

The best-supported synthesis is:

> broad school-math surfaces become more female-tilting with age, especially on `knowing`, but advanced-track math remains male-leaning, especially on `reasoning`.

That maps cleanly onto the current project state:

- `NLSY97 Math Knowledge` female-leaning
- `PIAT` and `Arithmetic Reasoning` not female-leaning
- `HSLS` transcript math surfaces female-leaning
- `TIMSS Grade 8 knowing` slightly female-leaning
- `TIMSS Advanced reasoning` clearly male-leaning

## Causal-Check Update

- `P(cause)`: `0.65` that the active quantitative disagreement is driven mainly by school-knowledge / curriculum / track surfaces rather than one battery-invariant latent quantitative gap.
- `Top alternative`: `0.20` that item format and scaling alone are doing most of the work, with little substantive schooling or track mechanism behind them.
- `Falsifier`: a transcript-aware school dataset where `knowing`, `applying`, `reasoning`, and advanced-track math all move together once exposure and track are aligned.
- `Decision impact`: the next datasets should be used to split `school knowledge`, `applied/problem-solving`, and `advanced-track selection` instead of talking about “math” as one object.

## Next Step

The best next external extension is still `PISA 2018` item-format decomposition, because it can test:

1. school-knowledge-heavy versus applied/problem-solving items
2. digital/item-format effects
3. whether the Grade 8 `TIMSS` pattern is specific to `TIMSS` or generalizes to another large school-age battery
