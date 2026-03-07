# Cross-Dataset School-Wedge Synthesis

**Date:** 2026-03-06  
**Scope:** `NLSY97`, `HSLS`, `ELS`, `NELS`

For the family-linked transition extension using public `PSID TAS`, see `research/iq-sex-differences-psid-tas-transition-first-pass.md`.

## Why This Memo Exists

The late-school branch was starting to collapse unlike things into one bucket:

- tested math
- school-knowledge math
- transcript quantity
- GPA / grades
- recommendation / recognition
- track / program

That is too coarse. The cross-cohort question is not just “does a wedge exist?” The better question is: **which school-linked surface families replicate?**

## Main Result

The most stable cross-cohort family is **female-leaning school evaluation**, not a universal female edge in tested math and not a universal female edge in raw course quantity. [SOURCE: `sources/iq-sex-diff/data/school_wedge_synthesis/school_wedge_synthesis_summary.tsv`]

Across the four local late-school cohorts:

1. tested math is male-leaning or near null on most broad surfaces
2. GPA / grades / recognition / recommendation surfaces tilt female
3. track and course-quantity surfaces are more heterogeneous than the evaluation family

That is the current best compression of the late-school evidence. [INFERENCE]

The family summary says the same thing in a cruder aggregate way:

- `gpa` family mean `+0.256` across two cohorts
- `evaluation` family mean `+0.127` across two cohorts
- broad `tested_math` family mean `-0.053` across two cohorts
- `tested_math_f2` in `NELS` is `-0.088`
- `track_selfreport` in `NLSY97` is `-0.179` [SOURCE: `sources/iq-sex-diff/data/school_wedge_synthesis/school_wedge_family_summary.tsv`]

## Cohort By Cohort

### `HSLS`

- tested math: `-0.033`
- transcript math GPA: `+0.267`
- highest-math-course GPA: `+0.195`
- `precalc+`: `+0.041` [SOURCE: `sources/iq-sex-diff/data/school_wedge_synthesis/school_wedge_synthesis_summary.tsv`]

This is the cleanest transcript-GPA wedge in the project. [INFERENCE]

### `ELS`

- tested math: `-0.072`
- `algebra II+`: `+0.063`
- `trig/precalc/calc`: `+0.040`
- recognition for good grades: `+0.112`
- teacher `AP/honors` recommendation: `+0.032` [SOURCE: `sources/iq-sex-diff/data/school_wedge_synthesis/school_wedge_synthesis_summary.tsv`]

This replicates the wedge without giving public transcript GPA. [INFERENCE]

### `NELS`

- first later tested math surface: `-0.003`
- second later tested math surface: `-0.088`
- transcript math units: `+0.001`
- math grades: `+0.101`
- recognition for good grades: `+0.142`
- academic-honors recommendation: `+0.023`
- academic or rigorous program: `+0.031` with CI crossing zero [SOURCE: `sources/iq-sex-diff/data/school_wedge_synthesis/school_wedge_synthesis_summary.tsv`]

This is the most useful narrowing result. `NELS` says the older-cohort wedge replicates most clearly on **evaluation** and much less clearly on **pure transcript quantity**. [INFERENCE]

### `NLSY97`

- applied/reasoning math: `+0.005`
- school-knowledge-heavy `Math Knowledge`: `+0.167`
- composite quantitative: `+0.092`
- transcript GPA: `+0.246`
- transcript math quantity: `+0.136`
- academic transcript math quantity: `+0.193`
- self-reported `precalc+`: `-0.179` [SOURCE: `sources/iq-sex-diff/data/school_wedge_synthesis/school_wedge_synthesis_summary.tsv`]

`NLSY97` remains the weirdest cohort. It is the one that keeps a female `Math Knowledge` / transcript-quantity wedge while self-reported course-taking tilts male. [INFERENCE]

## What Actually Replicates

### Strongest replicated family

Female-leaning **evaluation surfaces**:

- `HSLS` transcript GPA
- `ELS` recognition and teacher recommendation
- `NELS` grades, recognition, recommendation
- `NLSY97` transcript GPA [SOURCE: `sources/iq-sex-diff/data/school_wedge_synthesis/school_wedge_synthesis_summary.tsv`]

This now looks structural enough to treat as a real node, not just an `HSLS` anecdote. [INFERENCE]

### Moderately replicated family

Male-leaning or null **tested-math surfaces**:

- `HSLS` later tested math male
- `ELS` later tested math male
- `NELS` later tested math null to male
- `NLSY97` applied/reasoning math near null, but `Math Knowledge` female [SOURCE: `sources/iq-sex-diff/data/school_wedge_synthesis/school_wedge_synthesis_summary.tsv`]

This family is real, but not uniform because `NLSY97 Math Knowledge` still sits off to the side. [INFERENCE]

### Weakest replicated family

**Track / quantity** surfaces:

- `HSLS` `precalc+` female
- `ELS` course ladders female
- `NELS` academic/rigorous program weak female
- `NELS` transcript math units neutral
- `NLSY97` self-reported `precalc+` male
- `NLSY97` transcript math quantities female [SOURCE: `sources/iq-sex-diff/data/school_wedge_synthesis/school_wedge_synthesis_summary.tsv`]

This is the least stable family. It should stop being treated as a single mechanism. [INFERENCE]

## Causal Read

- `Observation:` evaluation surfaces replicate female, tested-math surfaces replicate male/null, track and quantity surfaces split by cohort and instrument. [SOURCE: `sources/iq-sex-diff/data/school_wedge_synthesis/school_wedge_synthesis_summary.tsv`]
- `Null:` if everything were just one latent math construct with noisy measurement, these families should not separate this cleanly across four cohorts. [INFERENCE]
- `Best current cause:` the school-pipeline node is internally plural:
  - evaluation / recognition
  - curriculum / track
  - tested performance
  - school-knowledge item families [INFERENCE]
- `Top alternative:` some of this separation still comes from incompatible public-use observables rather than real institutional channels. [INFERENCE]
- `Falsifier:` a harmonized transcript-rich reanalysis where these families converge once measures are aligned to common constructs and common samples. [INFERENCE]

## Decision Impact

This changes the next-stage target.

The late-school question is no longer:

1. “is there a school-linked wedge?”

It is now:

1. which school-linked family is the real causal driver
2. which are just correlated descendants or alternate measurements

The strongest next discriminators are:

1. stronger transcript access or harmonized transcript microdata
2. an explicit cross-cohort model that separates evaluation from quantity from track
3. item-family work that decides whether `NLSY97 Math Knowledge` is just a schooling/evaluation cousin or a distinct measurement surface

## Artifact

- `sources/iq-sex-diff/data/school_wedge_synthesis/school_wedge_synthesis_summary.tsv`
