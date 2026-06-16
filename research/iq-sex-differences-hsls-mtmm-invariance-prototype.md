# IQ Sex Differences - HSLS MTMM And Prediction Prototype

**Date:** 2026-03-10  
**Purpose:** run the first public-use latent surface-family prototype on a cohort that contains both tested-math and evaluation-math indicators plus later transcript-based outcomes.

Primary artifacts:

- `sources/iq-sex-diff/data/mtmm/hsls_mtmm_model_fit.tsv`
- `sources/iq-sex-diff/data/mtmm/hsls_mtmm_loadings.tsv`
- `sources/iq-sex-diff/data/mtmm/hsls_mtmm_prediction_models.tsv`
- `sources/iq-sex-diff/data/mtmm/hsls_mtmm_multigroup_summary.json`

Code:

- `sources/iq-sex-diff/hsls_mtmm_prediction_prototype.py`

Companion files:

- `research/iq-sex-differences-alpha-master-plan.md`
- `research/iq-sex-differences-mediator-design.md`
- `research/iq-sex-differences-school-wedge-extended-synthesis.md`

---

## Scope

This is a prototype for two workstreams:

1. `MTMM` / latent surface-family modeling
2. joint measurement plus prediction invariance

It is **not** a causal mediation design. No treatment effect of sex is being estimated here. [INFERENCE]

## Data

The prototype merges:

1. local `HSLS` refinement extract with tested-math and transcript-grade indicators
2. `HSLS 2017 PETS` public follow-up for degree and STEM outcomes

The current merge is keyed on `STU_ID`. Earlier local prototype outputs that joined `PETS` on the transcript weight field were wrong and are superseded by the current artifacts. [SOURCE: `sources/iq-sex-diff/hsls_mtmm_prediction_prototype.py`]

Indicators:

1. `X1TXMTSCOR_z`
2. `X2TXMTSCOR_z`
3. `X3TGPAMAT_z`
4. `X3TGPAHIMTH_z`

Outcomes:

1. `bachelor_plus` from `X5PFYDEGREE >= 4`
2. `stem_degree` from `X5STEMCRED`

[SOURCE: `sources/iq-sex-diff/data/hsls/hsls_wedge_refinement_extract.parquet`; `sources/iq-sex-diff/data/hsls/HSLS_2017_PETS_SR_v1_0_SPSS_Datasets.zip`; `sources/iq-sex-diff/hsls_mtmm_prediction_prototype.py`]

## Models

### Measurement side

One-factor model:

1. `school_math =~ tested + tested + evaluation + evaluation`

Two-factor model:

1. `tested_math =~ X1TXMTSCOR_z + X2TXMTSCOR_z`
2. `evaluation_math =~ X3TGPAMAT_z + X3TGPAHIMTH_z`

[SOURCE: `sources/iq-sex-diff/hsls_mtmm_prediction_prototype.py`]

### Prediction side

Observed composite proxies were used for the first outcome pass:

1. `tested_surface_z = mean(X1TXMTSCOR_z, X2TXMTSCOR_z)`
2. `evaluation_surface_z = mean(X3TGPAMAT_z, X3TGPAHIMTH_z)`

Then weighted and unweighted logit models were fit with sex interactions for:

1. `bachelor_plus`
2. `stem_degree`

[SOURCE: `sources/iq-sex-diff/hsls_mtmm_prediction_prototype.py`; `sources/iq-sex-diff/data/mtmm/hsls_mtmm_prediction_models.tsv`]

## Main result

The two-factor split is real on this public `HSLS` surface.

Full sample fit:

1. one-factor: `CFI = 0.770`, `RMSEA = 0.512`
2. two-factor: `CFI = 0.999`, `RMSEA = 0.046`

Male-only:

1. one-factor: `CFI = 0.769`, `RMSEA = 0.520`
2. two-factor: `CFI = 0.99984`, `RMSEA = 0.019`

Female-only:

1. one-factor: `CFI = 0.785`, `RMSEA = 0.489`
2. two-factor: `CFI = 0.99781`, `RMSEA = 0.070`

[SOURCE: `sources/iq-sex-diff/data/mtmm/hsls_mtmm_model_fit.tsv`]

That is not a subtle fit difference. On this cohort, tested math and evaluation math should not be treated as one latent school-math factor. [INFERENCE]

## Approximate measurement stability by sex

The sex-specific two-factor loadings are similar rather than wildly different.

Tested factor:

1. male `X2TXMTSCOR_z` loading: `1.127`
2. female `X2TXMTSCOR_z` loading: `1.071`

Evaluation factor:

1. male `X3TGPAHIMTH_z` loading: `0.803`
2. female `X3TGPAHIMTH_z` loading: `0.814`

Both sex-specific two-factor fits remain good:

1. male `CFI = 0.99984`, `RMSEA = 0.019`
2. female `CFI = 0.99781`, `RMSEA = 0.070`

[SOURCE: `sources/iq-sex-diff/data/mtmm/hsls_mtmm_loadings.tsv`; `sources/iq-sex-diff/data/mtmm/hsls_mtmm_multigroup_summary.json`]

This is not full constrained invariance testing. It is a first stability check showing the two-factor structure is not obviously a one-sex-only artifact. [INFERENCE]

## Prediction prototype

### Bachelor’s degree

Both tested and evaluation surfaces predict `bachelor_plus` strongly.

Weighted interaction model:

1. `female_tested = +0.218`
2. `female_evaluation = -0.077`

Unweighted interaction model:

1. `female_tested p = 0.038`
2. `female_evaluation p = 0.031`

[SOURCE: `sources/iq-sex-diff/data/mtmm/hsls_mtmm_prediction_models.tsv`]

Best current read:

1. broad predictive value exists for both surface families
2. on this first composite-logit pass, bachelor prediction is not invariant in a simple one-direction way: tested and evaluation interactions move in opposite directions
3. that should still be treated as provisional because the prediction side remains composite-based rather than a joint latent-outcome model

[INFERENCE]

### STEM degree

The tested surface is different.

Weighted interaction model:

1. `female_tested = +1.352`
2. `female_evaluation = +0.305`

Unweighted interaction model:

1. `female_tested = +0.941`, `p = 0.0040`
2. `female_evaluation = +0.418`, `p = 0.259`

[SOURCE: `sources/iq-sex-diff/data/mtmm/hsls_mtmm_prediction_models.tsv`]

Best current read:

1. tested-math prediction for STEM degree is not prediction-invariant by sex on this prototype
2. evaluation-math prediction is not stably classifiable as invariant or non-invariant on this prototype because the weighted and unweighted reads diverge

[INFERENCE]

## Causal-check

**Observation:** the late-school wedge keeps separating tested math from evaluation math, and the two-factor latent model fits dramatically better than a one-factor model. [SOURCE: `sources/iq-sex-diff/data/mtmm/hsls_mtmm_model_fit.tsv`]

**Null:** the surface-family story is mostly narrative, and one general school-performance factor should fit about as well. [INFERENCE]

**Residual:** on this public `HSLS` branch, the null fails badly. The data want at least two surfaces. [INFERENCE]

**New footprint:** once the two-surface split is admitted, prediction invariance no longer has to move uniformly across outcomes or model choices. The current `HSLS` prototype leaves the measurement result strong, but the prediction side remains provisional rather than settled. [SOURCE: `sources/iq-sex-diff/data/mtmm/hsls_mtmm_prediction_models.tsv`]

## What this hardens

1. The late-school `tested math` versus `evaluation math` distinction is now a formal model result, not just a narrative synthesis. [SOURCE: `sources/iq-sex-diff/data/mtmm/hsls_mtmm_model_fit.tsv`]
2. The repo should stop talking as if school-math surfaces form one latent family by default. [INFERENCE]
3. The first joint measurement/prediction pass says the answer is not “invariant” or “non-invariant” in one global way; it depends on outcome and currently also on model class. [SOURCE: `sources/iq-sex-diff/data/mtmm/hsls_mtmm_prediction_models.tsv`; `research/iq-sex-differences-weighted-mtmm-sensitivity.md`]

## Limitations

1. This is not full multi-group constrained CFA.
2. The measurement fit is unweighted because the current semopy route does not solve the weighted joint model cleanly.
3. The prediction side uses composite proxies rather than jointly estimated latent-factor regression.
4. The outcome models are observational and predictive, not causal.

[INFERENCE]
