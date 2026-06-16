# IQ Sex Differences - Measurement-Error Pilot

**Date:** 2026-03-10  
**Purpose:** test whether a lightweight measurement-error-aware upgrade materially changes the current public latent-family branch, or whether the practical gains require heavier weighted joint latent modeling and/or restricted transcript data.

Primary artifacts:

- `sources/iq-sex-diff/measurement_error_pilot.py`
- `sources/iq-sex-diff/data/mtmm/measurement_error_pilot_reliability.tsv`
- `sources/iq-sex-diff/data/mtmm/measurement_error_pilot_coefficients.tsv`
- `sources/iq-sex-diff/data/mtmm/measurement_error_pilot_comparison.tsv`

Companion files:

- `research/iq-sex-differences-causal-methods-frontier.md`
- `research/iq-sex-differences-hsls-mtmm-invariance-prototype.md`
- `research/iq-sex-differences-addhealth-evaluation-invariance-prototype.md`

---

## Scope

This is a bounded public-data pilot. It is **not** full joint latent-outcome estimation, full structural equation modeling with binary outcomes, or causal mediation. [INFERENCE]

It asks a narrower question:

> On the current public `HSLS` and `Add Health` latent-family prototypes, does lightweight measurement correction move the substantive geometry enough to matter?

The answer determines whether the methods-frontier memo was too optimistic about simple local `EIV` / attenuation fixes. [INFERENCE]

---

## Design

## Datasets

1. Public `Add Health` school-surface extract with four grade indicators and later attainment outcomes. [SOURCE: `sources/iq-sex-diff/data/addhealth/addhealth_school_surface_extract.parquet`]
2. Public `HSLS` refinement extract merged to `2017 PETS` outcomes with two tested-math and two evaluation-math indicators. [SOURCE: `sources/iq-sex-diff/data/hsls/hsls_wedge_refinement_extract.parquet`; `sources/iq-sex-diff/data/hsls/HSLS_2017_PETS_SR_v1_0_SPSS_Datasets.zip`]

## Predictors compared

For each latent family, three versions were compared:

1. naive observed composite
2. loading-weighted latent proxy built from the fitted CFA loadings
3. approximate reliability-corrected composite slope using `beta / reliability`

[SOURCE: `sources/iq-sex-diff/measurement_error_pilot.py`]

The reliability-corrected version is intentionally labeled approximate. It assumes classical attenuation and is included as a stress test, not as the new canonical coefficient. [INFERENCE]

## Outcomes

`Add Health`:

1. `bachelor_plus`
2. `some_college_plus`

`HSLS`:

1. `bachelor_plus`
2. `stem_degree`

[SOURCE: `sources/iq-sex-diff/measurement_error_pilot.py`]

## Estimation

Weighted linear probability models were fit with sex interactions:

1. `outcome ~ female + family_surface + female*family_surface`
2. robust `HC1` standard errors

This is a prediction-side attenuation pilot, not a causal effect model. `sensemakr` is therefore not the main tool here. [INFERENCE]

---

## Reliability

The current public latent-family indicators are already fairly reliable:

1. `Add Health evaluation alpha = 0.748`
2. `HSLS tested alpha = 0.859`
3. `HSLS evaluation alpha = 0.888`

[SOURCE: `sources/iq-sex-diff/data/mtmm/measurement_error_pilot_reliability.tsv`]

That matters because very large attenuation corrections were never likely on these specific public families. [INFERENCE]

---

## Main Result

Lightweight measurement correction does **not** materially change the public branch geometry. [INFERENCE]

## Add Health

`bachelor_plus`:

1. composite evaluation slope: `0.2275`
2. loading-weighted factor proxy slope: `0.2278`
3. female interaction: `-0.0068` vs `-0.0066`

`some_college_plus`:

1. composite evaluation slope: `0.1817`
2. loading-weighted factor proxy slope: `0.1831`
3. female interaction: `-0.0177` vs `-0.0179`

[SOURCE: `sources/iq-sex-diff/data/mtmm/measurement_error_pilot_comparison.tsv`]

So on `Add Health`, moving from a naive evaluation composite to a loading-weighted latent proxy changes the main slope by about `0.1%` to `0.8%` and leaves the interaction essentially unchanged. [INFERENCE]

## HSLS

`bachelor_plus`:

1. tested composite slope: `0.1348`
2. tested factor proxy slope: `0.1327`
3. evaluation composite slope: `0.1097`
4. evaluation factor proxy slope: `0.1122`
5. female tested interaction: `0.0411` vs `0.0408`
6. female evaluation interaction: `-0.0152` vs `-0.0145`

`stem_degree`:

1. tested composite slope: `0.00182`
2. tested factor proxy slope: `0.00167`
3. evaluation composite slope: `0.00246`
4. evaluation factor proxy slope: `0.00270`
5. female tested interaction: `0.00597` vs `0.00606`
6. female evaluation interaction: `-0.00036` vs `-0.00060`

[SOURCE: `sources/iq-sex-diff/data/mtmm/measurement_error_pilot_comparison.tsv`]

So on `HSLS`, the factor-proxy upgrade modestly perturbs magnitudes but does not flip signs, does not reorder the main surfaces, and does not change the basic interaction story. [INFERENCE]

---

## What The Approximate Reliability Correction Shows

The blunt `beta / reliability` correction is noticeably larger than the loading-weighted factor proxy:

1. `Add Health bachelor_plus`: `0.2275 -> 0.3041`
2. `Add Health some_college_plus`: `0.1817 -> 0.2429`
3. `HSLS bachelor_plus tested`: `0.1348 -> 0.1569`
4. `HSLS bachelor_plus evaluation`: `0.1097 -> 0.1235`

[SOURCE: `sources/iq-sex-diff/data/mtmm/measurement_error_pilot_comparison.tsv`]

But the factor-proxy estimates remain close to the naive composite estimates, not the reliability-divided values. [SOURCE: `sources/iq-sex-diff/data/mtmm/measurement_error_pilot_comparison.tsv`]

Best read:

1. there is some attenuation in principle
2. on these public families, the practical attenuation is modest
3. simple divide-by-reliability correction is too aggressive to become the canonical result

[INFERENCE]

---

## Causal-Check

**Observation:** the methods-frontier memo said measurement-error-aware latent modeling was the best immediate upgrade. [SOURCE: `research/iq-sex-differences-causal-methods-frontier.md`]

**Null:** a lightweight public-data measurement correction does not materially change the coefficient geometry because the staged families are already fairly reliable. [INFERENCE]

**Residual:** the null mostly survives on the current public branch. Factor-proxy versus composite estimates remain extremely similar even after the corrected `HSLS` follow-up merge. [SOURCE: `sources/iq-sex-diff/data/mtmm/measurement_error_pilot_comparison.tsv`]

**New footprint:** the value of the methods frontier now shifts upward:

1. away from simple public `EIV` correction
2. toward full weighted joint latent modeling
3. toward restricted transcript-theta models where the latent family itself is harder to observe cleanly

[INFERENCE]

---

## What This Hardens

1. The public latent-family branch is real, but simple measurement-error correction is **not** a magic source of new certainty on the current high-reliability `HSLS` and `Add Health` families. [SOURCE: `sources/iq-sex-diff/data/mtmm/measurement_error_pilot_reliability.tsv`; `sources/iq-sex-diff/data/mtmm/measurement_error_pilot_comparison.tsv`]
2. The strongest remaining gain is still heavier weighted joint latent modeling or restricted transcript data, not another light public attenuation tweak. [INFERENCE]
3. The methods-frontier memo needed a refinement, not a reversal: measurement-aware modeling is still the right direction, but the low-effort version pays only modest rent on the current public branch. [INFERENCE]

---

## Limitations

1. The pilot uses weighted linear probability models, not full joint latent-outcome estimation.
2. The latent predictors are loading-weighted proxies, not jointly estimated structural latent regressors.
3. The reliability correction is a stress test, not a preferred estimator.
4. This is prediction-side measurement work, not causal mediation or total-effect identification.

[INFERENCE]

---

## Decision Impact

Do **not** spend more cycles on lightweight public `EIV` corrections. [INFERENCE]

The next serious measurement moves are:

1. weighted joint multigroup latent modeling
2. restricted transcript-theta work
3. process-based DIF reduction on richer item/process data

[INFERENCE]
