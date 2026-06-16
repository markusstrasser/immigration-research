# IQ Sex Differences - MTMM Crosswalk

**Date:** 2026-03-07  
**Purpose:** freeze the first machine-readable trait/method crosswalk for the alpha phase.

This is the bridge between the repo’s surface-family synthesis and the first actual latent models.

Primary artifact:

- `sources/iq-sex-diff/data/latent/mtmm_surface_crosswalk.tsv`

Companion files:

- `research/iq-sex-differences-alpha-master-plan.md`
- `research/iq-sex-differences-psid-cds-mtmm-prototype.md`
- `research/iq-sex-differences-addhealth-evaluation-invariance-pilot.md`

## Why this exists

The current project already argues that the disagreement is better represented as recurring surface families than as one global `IQ` or `math` gap. That claim cannot stay purely narrative. The first MTMM step is to make the candidate traits and methods explicit by cohort. [INFERENCE]

## What was built

The crosswalk is a curated table, not a raw codebook dump.

Rows are keyed by:

1. `dataset`
2. `branch`
3. `trait_family`
4. `method_family`
5. `variable`
6. `role`
7. `outcome_available`
8. `notes`

[SOURCE: `sources/iq-sex-diff/build_mtmm_crosswalk.py`; `sources/iq-sex-diff/data/latent/mtmm_surface_crosswalk.tsv`]

## Current coverage

The first version spans:

1. `PSID_CDS_2002`
2. `AddHealth_public`
3. `HSLS_public`
4. `ELS_public`
5. `NELS_public`
6. `NLSY97_public`
7. `PSID_TAS_public`
8. `PISA2018_public`

[SOURCE: `sources/iq-sex-diff/data/latent/mtmm_surface_crosswalk.tsv`]

## Most important use cases

### 1. Smallest viable trait/method prototype

`PSID_CDS_2002` is the cleanest starting point because it has:

1. tested `math`
2. tested `reading`
3. teacher-rated `math`
4. teacher-rated `reading`

in one public cohort. That makes it the best first place to test whether the repo’s method-family claim survives a formal latent prototype. [INFERENCE]

### 2. First joint measurement/prediction invariance pilot

`AddHealth_public` is the cleanest first target for the evaluation family because it has:

1. multiple subject-grade indicators
2. a verbal anchor (`PVTSTD1`)
3. later attainment outcomes

It is not a transcript/test adjudication dataset, but it is enough to test whether the grade family behaves like a clean latent scalar and whether its predictive slope changes sharply by sex. [INFERENCE]

### 3. Cross-cohort MTMM expansion

The `HSLS`, `ELS`, `NELS`, and `NLSY97` rows show where the next true cross-cohort latent family model could go once the single-cohort prototypes are stable. [INFERENCE]

## Current limits

1. This is not exhaustive.
2. Some rows are family summaries rather than raw indicators, especially on the `PISA` branch.
3. Restricted-use transcript assets are not yet in the table because they are not locally analyzable.

[INFERENCE]

## Best current read

The crosswalk is strong enough to move the project from “surface families as a narrative” to “surface families as an executable latent-model agenda.” [INFERENCE]
