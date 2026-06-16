# IQ Sex Differences - PISA Frontier Comparison

**Date:** 2026-03-06  
**Purpose:** compare the repo's strongest current local `PISA` result against directly relevant prior `PISA` psychometric literature rather than only against generic recent-format and timing papers.

## Bottom Line

The local `PISA 2018` result is **not** a brand-new raw fact in the sense of being the first evidence that spatially loaded mathematics surfaces are more male-leaning than other content families.

Older direct `PISA 2003` work already reported:

- small overall male advantages
- the largest male gap on `Space and Shape`
- weaker gaps on `Quantity`

[SOURCE: https://bse.berkeley.edu/sites/default/files/gse-archive-4/Wilson8.pdf]

What the repo adds is different:

1. the same broad spatial dominance still survives on a later public `PISA 2018` surface
2. it survives a longer local hardening ladder:
   - leave-out matching
   - fixed-anchor purification
   - iterative purification
   - weighted binary logit
   - anchored Rasch sensitivity
3. it is placed inside a cross-surface project where school-evaluation, school-knowledge, applied/reasoning, process/timing, and adult accumulation are separate nodes rather than one pooled "math gap"

[INFERENCE]

## Direct Comparator 1 - Multidimensional Rasch on PISA 2003

Liu, Wilson, and Paek (2008) is the closest direct comparator to the repo's new Rasch sensitivity.

Their study:

- uses `PISA 2003`
- focuses on U.S. 15-year-olds
- uses a multidimensional Rasch model
- calibrates four mathematics domains:
  - `Space and Shape`
  - `Change and Relationships`
  - `Quantity`
  - `Uncertainty`

Their reported conclusion is:

- all domain gaps are small and favor boys
- `Space and Shape` shows the largest gender gap
- `Quantity` shows the least gender difference

[SOURCE: https://bse.berkeley.edu/sites/default/files/gse-archive-4/Wilson8.pdf]

## Direct Comparator 2 - U.S. vs Hong Kong PISA 2003

Liu and Wilson (2009) broadens the comparison by looking at the United States and Hong Kong in `PISA 2003`.

The abstract-level takeaways are:

- males in both systems demonstrate superior performance overall
- the strongest male edge appears on complex multiple-choice items
- females score higher on probability, algebra, and reproduction items

[SOURCE: https://scholar.google.com/scholar_url?ei=ONeraczQN66y6rQP4ty9gA8&hl=en&oi=scholarr&sa=X&scisig=AFtJQixVPIBTGbSLTrWXuUt4zJcP&url=https%3A%2F%2Fwww.tandfonline.com%2Fdoi%2Fabs%2F10.1080%2F15305050902733547 ; https://bse.berkeley.edu/sites/default/files/gse-archive-4/Wilson6.pdf]

That matters because it reinforces the older frontier point:

the sex-gap geometry depends on item family and format, not only on a single pooled mathematics score. [INFERENCE]

## Where The Repo Aligns

The new local `PISA 2018` anchored-Rasch sensitivity lines up with the older frontier in one major respect:

- `space_shape` remains the strongest male-residual family

Current local Rasch-weighted family contrasts:

- `space_shape = -0.138`
- `quantity = -0.092`
- `change_relationships = -0.084`
- `uncertainty_data = -0.046`

[SOURCE: `sources/iq-sex-diff/data/pisa/pisa2018_rasch_content_summary.tsv`; `research/iq-sex-differences-pisa2018-dif-rasch.md`]

So the repo is **aligned** with the older `PISA 2003` literature on the most important structural point:

spatially loaded math content is the strongest male-leaning family. [INFERENCE]

## Where The Repo Adds Something

The current repo does add two useful things.

### 1. Later-cycle persistence under harder local stress tests

The repo is not just restating `PISA 2003`.

It shows on local `PISA 2018` public data that the family ordering survives multiple modern local hardening passes, including a new anchored-Rasch sensitivity and a weighted binary-logit item model. [SOURCE: `research/iq-sex-differences-pisa2018-dif-leaveout.md`; `research/iq-sex-differences-pisa2018-dif-purified.md`; `research/iq-sex-differences-pisa2018-dif-iterative.md`; `research/iq-sex-differences-pisa2018-dif-logit.md`; `research/iq-sex-differences-pisa2018-dif-rasch.md`]

### 2. A shifted weakest family

The most interesting difference from the older U.S.-focused `PISA 2003` result is not the strongest family but the weakest one.

- older `PISA 2003` Rasch result: `Quantity` least different
- current local `PISA 2018` cross-country result: `uncertainty_data` closest to parity

[SOURCE: https://bse.berkeley.edu/sites/default/files/gse-archive-4/Wilson8.pdf ; `sources/iq-sex-diff/data/pisa/pisa2018_rasch_content_summary.tsv`]

That is **not yet** a clean historical trend claim, because:

- the older paper is U.S.-specific
- the current local result is cross-country
- the item pools are different
- the current local pass uses a binary-only public subset plus an unweighted Rasch sensitivity

[INFERENCE]

But it is a real hypothesis worth carrying:

> the strongest male-leaning `PISA` family may be stable across cycles, while the weakest family may be more cycle-, country-, or item-pool-dependent.

[INFERENCE]

## Novelty Read After The Comparison

- `P(novel as first notice that space/shape is male-leaning)`: low, around `0.10`
- `P(novel as stronger 2018-era public-data hardening of that family ordering)`: moderate, around `0.45`
- `P(novel as integrated cross-surface causal representation)`: still high, around `0.75`

[INFERENCE]

So the honest claim is:

the repo is not first to see the broad `PISA` content-family geometry, but it is doing a more integrated and more heavily stress-tested version of it than the casual literature discussion usually does. [INFERENCE]

## Decision Impact

This comparison lowers the risk of overclaiming novelty on the `PISA` branch.

It also clarifies what a publishable contribution would need to say:

- not "we discovered that space and shape favors boys"
- but rather "this family ordering persists on later-cycle public `PISA` data after multiple local hardening passes and fits into a wider cross-surface causal map that separates evaluation, school-knowledge, applied/reasoning, process, and accumulation"

[INFERENCE]
