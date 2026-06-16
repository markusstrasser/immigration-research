# IQ Sex Differences - HSLS First Joint Invariance Target

**Date:** 2026-03-10  
**Purpose:** freeze the first joint measurement/prediction invariance target so the latent branch stops drifting between datasets, family definitions, and later outcomes.

Primary artifacts:

- `sources/iq-sex-diff/build_hsls_invariance_target_grid.py`
- `sources/iq-sex-diff/data/mtmm/hsls_invariance_target_grid.tsv`
- `research/iq-sex-differences-hsls-mtmm-invariance-prototype.md`
- `research/iq-sex-differences-weighted-mtmm-sensitivity.md`
- `research/iq-sex-differences-addhealth-evaluation-invariance-prototype.md`

## Executive Answer

The first joint measurement/prediction invariance target should be:

1. dataset: `HSLS`
2. surface family pair: `tested_math` versus `evaluation_math`
3. primary later outcome: `STEM` degree
4. secondary calibration outcome: `bachelor_plus`

[SOURCE: `research/iq-sex-differences-hsls-mtmm-invariance-prototype.md`; `research/iq-sex-differences-weighted-mtmm-sensitivity.md`; `sources/iq-sex-diff/data/mtmm/hsls_invariance_target_grid.tsv`]

Do **not** freeze `Add Health` as the first joint target and do **not** freeze a single broad college outcome by itself.

Why:

1. `HSLS` is the only current local public branch that already identifies the core late-school family pair directly: tested math and evaluation math in the same cohort. [SOURCE: `research/iq-sex-differences-hsls-mtmm-invariance-prototype.md`; `research/iq-sex-differences-mtmm-crosswalk.md`]
2. `Add Health` hardens the evaluation family, but it does not provide the same-wave tested-math counterpart needed for the strongest first family-pair paper. [SOURCE: `research/iq-sex-differences-addhealth-evaluation-invariance-prototype.md`; `research/iq-sex-differences-addhealth-school-surface-first-pass.md`]
3. The current `HSLS` bachelor result is useful as a calibration outcome, but the sharper stress test is still `STEM` because that is where the raw prototype interaction is largest and where disagreement across model classes is most diagnostic. The new weighted `lavaan` pass does not change that ranking, but it does add a new caution: the surviving `STEM` interaction sits on a very thin `87`-positive outcome and therefore cannot carry a broad headline by itself. [SOURCE: `research/iq-sex-differences-hsls-mtmm-invariance-prototype.md`; `research/iq-sex-differences-weighted-mtmm-sensitivity.md`; `research/iq-sex-differences-hsls-lavaan-weighted-pass.md`; `sources/iq-sex-diff/data/mtmm/hsls_invariance_target_grid.tsv`; `sources/iq-sex-diff/data/mtmm/hsls_mtmm_lavaan_sample.tsv`]

## Why `HSLS`

The first target has to do more than show that a grade family exists.

It has to answer the narrower late-school question:

> when the repo’s strongest public family pair is put into one cohort, do tested math and evaluation math behave like one surface or two, and do they predict the same later outcome equally by sex?

[INFERENCE]

`HSLS` is currently the best local target because:

1. the one-factor `school_math` model fits badly while the two-factor split fits extremely well in pooled and sex-specific runs [SOURCE: `research/iq-sex-differences-hsls-mtmm-invariance-prototype.md`; `research/iq-sex-differences-weighted-mtmm-sensitivity.md`]
2. that split survives the weighted covariance sensitivity, so the basic family separation is not mainly an unweighted artifact [SOURCE: `research/iq-sex-differences-weighted-mtmm-sensitivity.md`; `sources/iq-sex-diff/data/mtmm/hsls_invariance_target_grid.tsv`]
3. the cohort includes later degree outcomes, so the same target can support both measurement and prediction checks [SOURCE: `research/iq-sex-differences-hsls-mtmm-invariance-prototype.md`]

## Why `STEM` Is Primary And `bachelor_plus` Is Secondary

The repo should not freeze one college outcome and pretend it speaks for every later return surface.

The current best read is:

1. `bachelor_plus` is the broad calibration outcome
2. `STEM` degree is the sharper discrimination outcome

[INFERENCE]

Why this split is better:

1. on the prototype branch, `bachelor_plus` shows broad predictive value for both families but only mixed evidence of sex-differential slopes [SOURCE: `research/iq-sex-differences-hsls-mtmm-invariance-prototype.md`; `sources/iq-sex-diff/data/mtmm/hsls_invariance_target_grid.tsv`]
2. on the same branch, `STEM` is where the tested-math interaction is largest on the first prototype pass, making it the cleanest place to look for a break that either survives or dies under stronger latent modeling [SOURCE: `research/iq-sex-differences-hsls-mtmm-invariance-prototype.md`; `sources/iq-sex-diff/data/mtmm/hsls_invariance_target_grid.tsv`]
3. the weighted latent sensitivity keeps the family split intact but also warns that the prediction branch is still model-sensitive, so `STEM` should be treated as a stress test rather than as a settled non-invariance result [SOURCE: `research/iq-sex-differences-weighted-mtmm-sensitivity.md`; `sources/iq-sex-diff/data/mtmm/hsls_invariance_target_grid.tsv`]
4. the stronger weighted `lavaan` factor-score pass keeps only the `STEM` tested-factor interaction alive, while broad bachelor-level interactions disappear; that strengthens the case for `STEM` as the sharper discrimination outcome but also makes the sample-size limitation explicit [SOURCE: `research/iq-sex-differences-hsls-lavaan-weighted-pass.md`; `sources/iq-sex-diff/data/mtmm/hsls_mtmm_lavaan_prediction.tsv`; `sources/iq-sex-diff/data/mtmm/hsls_mtmm_lavaan_sample.tsv`]

So the correct first paper-shaped question is not:

> does the late-school family pair predict “college” differently by sex in general?

It is:

> does the tested-versus-evaluation family split stay measurement-distinct, and is `STEM` the later surface where any prediction break is easiest to detect or to kill under stronger latent modeling?

[INFERENCE]

## Why Not `Add Health` First

`Add Health` remains useful, but it is the wrong first target for the main invariance paper.

It is better read as:

1. a holdout showing that the evaluation family is coherent enough to model
2. a check that broad later-attainment prediction is not obviously and globally sex-noninvariant on that family

[SOURCE: `research/iq-sex-differences-addhealth-evaluation-invariance-prototype.md`]

That is valuable, but it does **not** replace `HSLS` for the first joint target because:

1. it lacks the same-cohort tested-math versus evaluation-math pair [SOURCE: `research/iq-sex-differences-addhealth-evaluation-invariance-prototype.md`; `research/iq-sex-differences-mtmm-crosswalk.md`]
2. its cleanest prediction result is near-invariance on `some_college_plus`, which is a good anchor but not the strongest discriminatory test of the repo’s late-school family split [SOURCE: `research/iq-sex-differences-addhealth-evaluation-invariance-prototype.md`]
3. if used first, it would encourage the wrong headline: “evaluation is coherent,” instead of the stronger headline: “tested and evaluation math are distinct late-school surfaces and should not be pooled” [INFERENCE]

## Frozen Decision Grid

The first joint target should use this fixed grid:

1. measurement target:
   `HSLS` one-factor versus two-factor comparison on the common tested-plus-evaluation sample
2. prediction target:
   `STEM` degree as primary, `bachelor_plus` as secondary
3. surface contrasts:
   tested-math slope, evaluation-math slope, and sex interactions on both
4. interpretation rule:
   no global “prediction invariance” slogan unless the same answer survives across both outcomes

[SOURCE: `research/iq-sex-differences-hsls-mtmm-invariance-prototype.md`; `research/iq-sex-differences-weighted-mtmm-sensitivity.md`; `sources/iq-sex-diff/data/mtmm/hsls_invariance_target_grid.tsv`]

## Stop Rules

1. If the stronger next latent model makes the one-factor representation competitive, soften the current family-pair claim. [SOURCE: `research/iq-sex-differences-hsls-mtmm-invariance-prototype.md`; `research/iq-sex-differences-weighted-mtmm-sensitivity.md`]
2. If `STEM` interaction differences disappear under the stronger latent prediction model, soften the current non-invariance language to “outcome-specific prototype signal only.” [SOURCE: `research/iq-sex-differences-hsls-mtmm-invariance-prototype.md`; `sources/iq-sex-diff/data/mtmm/hsls_invariance_target_grid.tsv`]
3. If `bachelor_plus` remains mixed while `STEM` remains the sharper stress test, keep the interpretation narrow: the break is domain-specific prediction pressure, not a global return difference. [SOURCE: `research/iq-sex-differences-hsls-mtmm-invariance-prototype.md`; `research/iq-sex-differences-weighted-mtmm-sensitivity.md`; `research/iq-sex-differences-hsls-lavaan-weighted-pass.md`]
4. If the `STEM` branch continues to depend on a very sparse binary outcome, do not let it dominate the paper headline; treat it as a stress test that motivates richer later-outcome data rather than as the core generalizable result. [SOURCE: `research/iq-sex-differences-hsls-lavaan-weighted-pass.md`; `sources/iq-sex-diff/data/mtmm/hsls_mtmm_lavaan_sample.tsv`]
4. Do **not** promote this to a final weighted multigroup SEM verdict. The local stack still does not provide the publication-grade weighted joint latent model. [SOURCE: `research/iq-sex-differences-weighted-mtmm-sensitivity.md`; `research/iq-sex-differences-irt-tooling-feasibility.md`]

## Immediate Implementation Consequence

The next honest latent-model step is now narrower:

1. keep `HSLS` as the first joint invariance cohort
2. keep `tested_math` versus `evaluation_math` as the first family pair
3. keep `STEM` primary and `bachelor_plus` secondary
4. stop drifting back to `Add Health` or generic “college” outcomes when the question is the first joint family-pair test

[INFERENCE]
