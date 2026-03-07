# IQ Sex Differences - TIMSS Frontier

**Date:** 2026-03-05
**Purpose:** first-pass `TIMSS 2019` grade-surface and `TIMSS Advanced 2015` upper-track check.

This memo is descriptive. It does **not** identify a latent developmental causal effect.

## Data And Method

Datasets used:

- `TIMSS 2019` Grade 4 main national student achievement files: `sources/iq-sex-diff/data/timss_grade4/T19_G4_SPSS%20Data.zip`
- `TIMSS 2019` Grade 8 main national student achievement files: `sources/iq-sex-diff/data/timss/T19_G8_SPSS%20Data.zip`
- `TIMSS Advanced 2015` advanced mathematics main student files: `sources/iq-sex-diff/data/timss_advanced/TA15_SPSSData.zip`

Execution scripts and outputs:

- script: [timss_grade_decomposition.py](/Users/alien/Projects/research/sources/iq-sex-diff/timss_grade_decomposition.py)
- script: [timss_advanced_first_pass.py](/Users/alien/Projects/research/sources/iq-sex-diff/timss_advanced_first_pass.py)
- shared helper: [timss_common.py](/Users/alien/Projects/research/sources/iq-sex-diff/timss_common.py)
- outputs: [timss_2019_grade_gaps.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/timss_grade_compare/timss_2019_grade_gaps.tsv), [timss_2019_grade_summary.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/timss_grade_compare/timss_2019_grade_summary.tsv), [timss_2019_grade_paired_deltas.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/timss_grade_compare/timss_2019_grade_paired_deltas.tsv), [timss_2019_grade_paired_summary.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/timss_grade_compare/timss_2019_grade_paired_summary.tsv)
- outputs: [timss_advanced_2015_gaps.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/timss_advanced/timss_advanced_2015_gaps.tsv), [timss_advanced_2015_summary.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/timss_advanced/timss_advanced_2015_summary.tsv)

Frozen choices:

1. only main national student files were used
2. benchmark and `eTPSI` files were excluded
3. sex gap is `female - male` in weighted `Cohen's d`
4. variance uses `TOTWGT` plus `JKZONE` / `JKREP` jackknife replication
5. plausible-value uncertainty is combined across the 5 official PVs

## Main Results

### TIMSS 2019 Grade 4

Across the main Grade 4 country set, overall math is male-leaning and science is female-leaning:

- overall math: mean `d = -0.069` across `64` countries
- overall science: mean `d = +0.035` across `64` countries

Math subdomains at Grade 4 are mostly male-leaning:

- number: mean `d = -0.077`
- geometry: mean `d = -0.101`
- knowing: mean `d = -0.111`
- reasoning: mean `d = -0.097`
- applying: mean `d = -0.043`
- data: mean `d = -0.029`

Source table: [timss_2019_grade_summary.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/timss_grade_compare/timss_2019_grade_summary.tsv)

### TIMSS 2019 Grade 8

Across the main Grade 8 country set, broad math is near zero to slightly female-leaning:

- overall math: mean `d = +0.017` across `46` countries
- overall science: mean `d = +0.080` across `46` countries

Grade 8 math does **not** look uniformly male-leaning:

- algebra: mean `d = +0.088` across `43` countries
- number: mean `d = -0.056`
- geometry: mean `d = +0.016`
- knowing: mean `d = +0.029`
- reasoning: mean `d = +0.017`
- applying: mean `d = -0.002`
- data and probability: mean `d = -0.008`

Source table: [timss_2019_grade_summary.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/timss_grade_compare/timss_2019_grade_summary.tsv)

### Grade 4 To Grade 8 Overlap

The more defensible comparison is the paired overlap by common country code.

For the `38` countries with both Grade 4 and Grade 8 overall-math surfaces:

- mean Grade 4 overall-math gap: `d = -0.067`
- mean Grade 8 overall-math gap: `d = +0.009`
- mean `Grade 8 - Grade 4` delta: `+0.076`
- `29 / 38` countries move in the female direction at Grade 8

Common paired domains show the same broad shift:

- geometry delta: `+0.122` across `34` countries
- knowing delta: `+0.139` across `34` countries
- reasoning delta: `+0.113` across `34` countries
- applying delta: `+0.043` across `34` countries
- number delta: `+0.019` across `34` countries

Source table: [timss_2019_grade_paired_summary.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/timss_grade_compare/timss_2019_grade_paired_summary.tsv)

This is a real surface shift, not a one-country artifact. Country-level deltas vary, but the direction is broad enough that it should update the causal graph.

### TIMSS Advanced 2015

The upper-track advanced mathematics surface does **not** follow the broad Grade 8 pattern.

Across the `10` advanced-math countries:

- overall advanced math: mean `d = -0.148`
- geometry: mean `d = -0.205`
- reasoning: mean `d = -0.195`
- algebra: mean `d = -0.142`
- knowing: mean `d = -0.127`
- applying: mean `d = -0.111`
- calculus: mean `d = -0.105`

`8 / 10` countries are male-leaning on overall advanced math, and `7 / 10` have male-leaning `95%` CIs.

Source table: [timss_advanced_2015_summary.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/timss_advanced/timss_advanced_2015_summary.tsv)

## Interpretation

The most important update is structural:

1. broad school math is not a monotone male-advantage surface
2. upper-track advanced math is male-leaning
3. therefore "math gap" is not one thing

The current footprint is more consistent with **multiple math surfaces** than with one universal latent quantitative gap:

- elementary broad math: male-leaning on average
- middle-school broad math: close to parity or slightly female-leaning in many countries
- advanced upper-track mathematics: male-leaning again

That pattern weakens two simple stories:

1. "`boys are just better at math everywhere`"
2. "`girls are just better once school takes over`"

It also raises the priority of three nodes:

1. curriculum / item-content shift between Grade 4 and Grade 8
2. track / selection effects in advanced mathematics
3. evaluation / placement and identity sorting between broad school math and upper-track math

## Causal Update

This pass does **not** identify why the grade surfaces diverge. It does constrain the shape of any adequate explanation.

- `P(cause) = 0.60` that school-math and upper-track advanced-math gaps are materially different causal surfaces rather than noisy measures of one underlying stable sex difference. [INFERENCE]
- `Top alternative = 0.25`: much of the broad Grade 8 femaleward shift is measurement / item-content non-equivalence rather than a real developmental or school-pathway change. [INFERENCE]
- `Falsifier`: transcript-rich same-cohort data showing that once course ladder and track are fixed, broad school math and advanced math return the same sex-gap direction and magnitude. [INFERENCE]
- `Decision impact`: the next work should prioritize transcript-rich `HSLS` / `ELS` and same-cohort cross-surface checks over more generic adult-battery slicing. [INFERENCE]

## What This Does And Does Not Prove

What it does prove:

- the project can no longer talk about "the math gap" as if it were a single stable object
- a broad Grade 8 school-math surface can look very different from an advanced upper-track surface

What it does not prove:

- that girls have higher latent quantitative ability by adolescence
- that boys have higher latent quantitative ability but schools hide it
- that the Grade 4 to Grade 8 shift is developmental within persons

`TIMSS` Grade 4 and Grade 8 are cross-sectional international surfaces, not a within-person panel. `TIMSS Advanced` is also a selected upper-track population, not a population-wide adolescent battery.

## Next Discriminating Analyses

1. `HSLS:09` and `ELS:2002` transcript-rich replication:
   - broad math versus advanced-course / transcript ladder
   - grade-test wedge
   - identity / aspiration sorting
2. `PISA 2018` and `eTIMSS` process / item-format decomposition:
   - response-time and visits surfaces
   - item-format sex heterogeneity
3. same-cohort `NLSY97` `PIAT Math` versus `CAT-ASVAB`:
   - school-linked broad math surface versus adaptive test surface
   - design-only controls first, then mechanism strata
