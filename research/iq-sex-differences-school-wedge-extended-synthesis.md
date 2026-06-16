# IQ Sex Differences - School/Transition Wedge Extended Synthesis

**Date:** 2026-03-06  
**Purpose:** extend the late-school wedge synthesis beyond `HSLS` / `ELS` / `NELS` / `NLSY97` and quantify whether the same family structure survives when public `Add Health` and `PSID TAS` are added.

## Scope

This is a **descriptive cross-surface synthesis**, not a formal meta-analysis. The summary mixes standardized betas, shares, and `d`-type gaps to answer one narrower question:

> does the same surface-family geometry survive once the public transition cohorts are added?

[INFERENCE]

The canonical outputs are:

1. `sources/iq-sex-diff/data/school_wedge_extended_synthesis/school_wedge_extended_synthesis_summary.tsv`
2. `sources/iq-sex-diff/data/school_wedge_extended_synthesis/school_wedge_extended_family_summary.tsv`

[SOURCE: `sources/iq-sex-diff/school_wedge_extended_synthesis.py`]

## Main Result

The extended synthesis strengthens the same pattern rather than reopening it:

- female-leaning `GPA` / grade / evaluation surfaces remain the most stable school/transition family
- male or null tested-math surfaces remain the counter-family
- the late-school female tested-math story still looks localized to school-knowledge-heavy surfaces rather than broad tested math

[SOURCE: `sources/iq-sex-diff/data/school_wedge_extended_synthesis/school_wedge_extended_synthesis_summary.tsv`; `sources/iq-sex-diff/data/school_wedge_extended_synthesis/school_wedge_extended_family_summary.tsv`]

## What The Extension Added

Two cohorts materially widen the picture:

1. `Add Health` adds a broad public school-performance cohort:
   - `english_grade_points = +0.353`
   - `math_grade_points = +0.226`
   - `math_minus_english = -0.116`
   - female attainment residual after observed `PVT + math + English grades = +0.422`
2. `PSID TAS` adds a family-linked transition panel:
   - `hs_gpa_norm = +0.289`
   - `college_gpa_norm = +0.383`
   - `sat_math = -0.355`
   - `act_composite = -0.119`
   - descriptive `hs_gpa_minus_sat_math_z = +0.480`
   - family-FE `hs_gpa_minus_sat_math_z = +0.707`

[SOURCE: `sources/iq-sex-diff/data/school_wedge_extended_synthesis/school_wedge_extended_synthesis_summary.tsv`]

So the wedge is no longer just a transcript-rich NCES story. It extends into:

- a broad school-grade panel (`Add Health`)
- a public transition panel with family fixed effects (`PSID TAS`)

[INFERENCE]

## Stable Families

### Female-leaning

The clearest replicated female-leaning families are:

- `gpa` / grade surfaces
- `evaluation` / recognition / recommendation surfaces
- some `track` surfaces in `HSLS`, `ELS`, and `NELS`
- the localized `tested_math_knowledge` surface in `NLSY97`

Numerically:

- late-school `gpa mean = +0.256`
- late-school `evaluation mean = +0.127`
- transition `gpa mean = +0.336`
- transition `gpa_vs_test_wedge = +0.480`
- transition `gpa_vs_test_wedge_fe = +0.707`

[SOURCE: `sources/iq-sex-diff/data/school_wedge_extended_synthesis/school_wedge_extended_family_summary.tsv`]

### Male or null

The clearest replicated male or null families are:

- broad tested math in `HSLS` / `ELS` / `NELS`
- transition tested math in `PSID TAS`
- the relative grade profile in public `Add Health` because English is more female-tilted than math
- `NLSY97` self-reported advanced-course flag, which still points male

Numerically:

- late-school `tested_math mean = -0.053`
- late-school `tested_math_f2 = -0.088`
- transition `tested_math mean = -0.237`
- late-school `relative_grade_profile = -0.116`
- late-school `track_selfreport = -0.179`

[SOURCE: `sources/iq-sex-diff/data/school_wedge_extended_synthesis/school_wedge_extended_family_summary.tsv`]

## What Did Not Change

The extension does **not** rescue a broad female tested-math claim.

The only female-leaning tested-math family that still stands out is the localized `NLSY97` school-knowledge branch:

- `Math Knowledge = +0.167`
- `quantitative composite = +0.092`
- `Arithmetic Reasoning = +0.005`

That keeps the current late-school read intact:

> broad tested math is not female-leaning overall; the anomaly is still a narrower school-knowledge-heavy surface.

[SOURCE: `sources/iq-sex-diff/data/school_wedge_extended_synthesis/school_wedge_extended_synthesis_summary.tsv`; `research/iq-sex-differences-nlsy97-piat-cat-pass.md`; `research/iq-sex-differences-nlsy97-transcript-deep-pass.md`]

## Causal Check

> **Observation:** after adding `Add Health` and `PSID TAS`, female-leaning school/evaluation surfaces still replicate, while tested-math surfaces remain male or null outside the localized `NLSY97` school-knowledge branch. [SOURCE: `sources/iq-sex-diff/data/school_wedge_extended_synthesis/school_wedge_extended_synthesis_summary.tsv`]
>
> **Null:** if the earlier wedge story were mostly a transcript-specific artifact or a fragile NCES-only pattern, adding a broad grade panel and a family-linked transition panel should materially blur or reverse the family ordering. [INFERENCE]
>
> **Residual after null:** it does not. The ordering survives and arguably strengthens: the transition data add the cleanest `GPA versus tested math` split in the repo so far. [SOURCE: `sources/iq-sex-diff/data/psid/psid_tas_best_surface_gaps.tsv`; `sources/iq-sex-diff/data/psid/psid_tas_family_fe.tsv`]

- `P(cause)`: `0.79` that the school/transition wedge is a real surface-family structure rather than an artifact of one transcript-rich cohort. [INFERENCE]
- `Top alternative`: `0.15` that the apparent family ordering is still mostly an artifact of mixed estimands and mixed scales rather than a common latent structure. [INFERENCE]
- `Falsifier`: a harmonized cross-cohort reanalysis on common constructs where evaluation/GPA surfaces, tested math, and transition surfaces converge once sample, timing, and scaling are forced onto the same geometry. [INFERENCE]
- `Decision impact`: the repo can now treat the school/transition wedge as a real descriptive structure. The open work is mechanism and mediation, not whether the wedge exists at all. [INFERENCE]

## What This Still Does Not Prove

This does **not** prove:

- identified mediation
- that grades are “inflated”
- that boys or girls have higher battery-independent `g`
- that all female-leaning school surfaces cash out equally in later outcomes

It does prove something narrower and stronger:

> the U.S. school/transition branch is not one surface. Evaluation/GPA and tested math are now clearly different families in the local evidence base.

[INFERENCE]
