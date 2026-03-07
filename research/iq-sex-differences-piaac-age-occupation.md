# IQ Sex Differences PIAAC Age And Occupation Extension

**Date:** 2026-03-05
**Scope:** `PIAAC p1` age-band heterogeneity plus first occupation-proxy pass

**Scripts executed:**

- `sources/iq-sex-diff/piaac_p1_age_stratified.py`
- `sources/iq-sex-diff/piaac_p1_occupation_proxy.py`

**Outputs:**

- `sources/iq-sex-diff/data/piaac/piaac_p1_age_stratified_gaps.tsv`
- `sources/iq-sex-diff/data/piaac/piaac_p1_age_grouped_summary.tsv`
- `sources/iq-sex-diff/data/piaac/piaac_p1_iscoskil4_gaps.tsv`
- `sources/iq-sex-diff/data/piaac/piaac_p1_iscoskil4_summary.tsv`

---

## Bottom Line

The `PIAAC` extension weakens the strongest version of the adult-accumulation story without killing it.

What survives:

1. male numeracy gaps are already present in younger adults
2. those numeracy gaps get larger in middle and older age bands
3. they also remain male-leaning inside every broad `ISCOSKIL4` occupation-skill group on average

So the clean update is:

- accumulation probably matters for **magnitude**
- accumulation does **not** look sufficient to explain the existence of the male numeracy pattern

## Age-Band Surface

Age grouping used here:

- `young` = `AGEG10LFS_T` bands `1` and `2`
- `middle` = bands `3` and `4`
- `older` = band `5` and older-coded cases when present

### Grouped Means Across Country-Waves

| domain | young | middle | older |
|---|---:|---:|---:|
| `literacy` | `+0.005` | `-0.032` | `-0.092` |
| `numeracy` | `-0.185` | `-0.263` | `-0.330` |
| `problem_solving` | `-0.094` | `-0.158` | `-0.258` |

Read:

- literacy is near zero in younger adults and becomes modestly more male-leaning with age
- numeracy is male-leaning already in younger adults and gets steadily more male-leaning with age
- problem solving shows the same directional age gradient as numeracy

### Causal Read On Age

This age geometry matters:

- if adult labor-market accumulation were the whole story, the young-adult numeracy surface should be close to zero
- it is not; the mean young-adult numeracy gap is still about `-0.185`
- but the monotone shift toward `-0.330` in older adults is consistent with later amplification through experience, sorting, or accumulated practice

So age looks like an **amplifier**, not a sole origin.

## Occupation Proxy Surface

Proxy used here:

- `ISCOSKIL4`
- codebook label: occupational classification of respondent's job, **last or current**, 4 skill-based categories

This is a useful descriptive proxy but not a clean causal control because it is downstream of education, selection, and prior skill differences.

### Proxy Availability

The proxy is broadly usable in the local `p1` files:

- `ISCOSKIL4` is nonmissing for about `95%` to `100%` of rows across country-waves

### Mean Gaps Across Country-Waves

| domain | skilled | semi-skilled white-collar | semi-skilled blue-collar | elementary |
|---|---:|---:|---:|---:|
| `literacy` | `-0.088` | `-0.035` | `+0.050` | `-0.218` |
| `numeracy` | `-0.374` | `-0.220` | `-0.173` | `-0.371` |
| `problem_solving` | `-0.198` | `-0.151` | `+0.033` | `-0.360` |

Read:

- numeracy remains male-leaning in every broad occupation-skill group on average
- the largest mean numeracy gaps are in skilled and elementary occupations
- literacy and problem solving are much noisier in semi-skilled blue-collar work, with some female-leaning cells and wide intervals

### Causal Read On Occupation

This weakens the coarse occupation-sorting story:

- if broad occupational sorting were doing most of the work, the numeracy gap should flatten sharply within occupation-skill groups
- it does not
- what does happen is heterogeneity in literacy and problem solving, especially in blue-collar cells with smaller female counts

So `ISCOSKIL4` looks like a **modifier** of some domains, not a full absorber of the numeracy pattern.

## What This Does To The Causal Graph

### Observation

After the first `PIAAC` frontier, the main open alternative was:

- maybe the male numeracy pattern is mostly an adult accumulation artifact

The extension gives two new footprints:

1. younger adults already show a male numeracy gap
2. broad occupation-skill stratification does not remove it

### Updated Ranking

#### `H1` Stable Domain Pattern With Later Amplification

Strongest current explanation.

Mechanism:

- some male-leaning numeracy / problem-solving difference is present before late-career accumulation
- later education, work sorting, and practice amplify the magnitude

#### `H2` Adult Accumulation As Main Cause

Weakened.

Mechanism prediction:

- young-adult gaps near zero
- within-occupation gaps near zero

Observed:

- neither prediction holds for numeracy

#### `H3` Battery / Construct / Age-Surface Divergence For `NLSY97`

Still strong.

- the `NLSY97` quantitative sign flip now looks even less likely to be a generic education or occupation-composition story

## Causal-Check Summary

> **Observation:** in `PIAAC`, male numeracy gaps remain negative in young, middle, and older age groups, and remain negative on average across all broad `ISCOSKIL4` occupation-skill groups.
> **Null:** the male adult numeracy pattern is mostly produced by post-school accumulation or occupational sorting.
> **Residual after null:** stratifying by age and broad occupation does not remove the gap.
> **Geometry:** broad class-wide persistence with gradual age amplification.
> **Magnitude:** young `-0.185`, middle `-0.263`, older `-0.330`; occupation-group means from about `-0.173` to `-0.374`.
> **Lag window:** early adulthood through later working life.

- `P(cause)`: `0.65` that age and occupation mainly amplify an existing male numeracy pattern rather than create it from scratch
- `Top alternative`: `0.20` that even the young-adult `PIAAC` groups already reflect substantial pre-labor-market sorting by field and track, so the apparent early signal is still mostly accumulation-by-selection
- `Falsifier`: a closer-to-school-exit international battery where numeracy is near zero after education-track adjustment
- `Decision impact`: treat adult accumulation as part of the story, but stop treating it as the whole story

## Epistemic Limits

1. `AGEG10LFS_T` is a released grouped age variable, not exact age.
2. `ISCOSKIL4` is explicitly based on **last or current** job, so it is a rough accumulation proxy rather than a pure current-job control.
3. Some blue-collar and elementary cells have small female counts, so literacy and problem-solving estimates there are much noisier than numeracy.
4. None of these stratifications are causal identification; they are descriptive stress tests on competing narratives.

## Best Next Steps

1. add a tighter young-adult slice wherever available, because that is now the highest-leverage discriminant
2. inspect education-track or field-of-study proxies if the public files expose them under country-specific names
3. map `NLSY97 quantitative` more carefully onto comparable `PIAAC` and `ASVAB` constructs instead of treating all of them as one latent object
