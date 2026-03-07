# IQ Sex Differences - PSID TAS Transition First Pass

**Date:** 2026-03-06  
**Purpose:** record the first cleaned public-use `PSID TAS` transition result and decide whether the school-linked wedge extends beyond transcript-rich school cohorts into early-adult GPA and admissions-test surfaces.

## What Was Built

The repo now has a compact public-use `PSID TAS` transition panel built from the downloaded `2017`, `2019`, `2021`, and `2023` `TAS` bundles plus the `IND2023ER` identity map used to recover stable `1968` family/person IDs and sex. [SOURCE: `sources/iq-sex-diff/psid_tas_build_panel.py`; `sources/iq-sex-diff/data/psid/psid_tas_panel.parquet`; `sources/iq-sex-diff/data/psid/psid_tas_build_diagnostics.json`]

Wave coverage in the current build:

- `2017`: `2,526` rows
- `2019`: `2,595` rows
- `2021`: `2,362` rows
- `2023`: `2,434` rows
- combined panel: `9,917` rows, `4,586` unique people, `1,511` unique `1968` families

[SOURCE: `sources/iq-sex-diff/data/psid/psid_tas_build_diagnostics.json`]

The official `CDS/TAS` study-design page says `TAS` follows the original `CDS` children into adulthood and supports intergenerational/family designs. [SOURCE: https://psidonline.isr.umich.edu/CDS/Guide/StudyDesign.aspx]

## Data Hygiene Fixes

Three public-file issues mattered enough to change the first pass:

1. `2019` `cross_weight` is nonmissing but entirely zero in the current public file, so weighted summaries must fall back to the positive `prior_cds_tas_weight` field in that wave. [SOURCE: `sources/iq-sex-diff/data/psid/psid_tas_panel.parquet`; `sources/iq-sex-diff/psid_tas_first_pass.py`]
2. `TAS` GPA surfaces are not comparable without normalization by the reported maximum scale, so the current pass uses `hs_gpa / hs_gpa_max` and `college_gpa_actual / college_gpa_max`. [SOURCE: `sources/iq-sex-diff/psid_tas_first_pass.py`]
3. College GPA is split across paired public fields (`K/Y` and `M/Z`) and must be coalesced before modeling. [SOURCE: `sources/iq-sex-diff/psid_tas_first_pass.py`]

These are real public-use score-surface quirks, not cosmetic cleanup. [INFERENCE]

## Main Descriptive Result

The public-use `TAS` panel extends the school-linked wedge into the transition branch:

- normalized high-school GPA is female-leaning
- normalized college GPA is female-leaning
- `SAT math` is male-leaning
- `ACT composite` is male-leaning
- the aligned `GPA minus SAT math` surfaces are strongly female-leaning

[SOURCE: `sources/iq-sex-diff/data/psid/psid_tas_wave_surface_gaps.tsv`; `sources/iq-sex-diff/data/psid/psid_tas_best_surface_gaps.tsv`; `sources/iq-sex-diff/data/psid/psid_tas_aligned_gaps.tsv`]

### Best/latest weighted surfaces

Key weighted gaps (`female - male`, Cohen’s `d`):

- `hs_gpa_norm`: `+0.289`
- `college_gpa_norm`: `+0.383`
- `sat_math`: `-0.355`
- `sat_reading`: `-0.088`
- `act_composite`: `-0.119`

[SOURCE: `sources/iq-sex-diff/data/psid/psid_tas_best_surface_gaps.tsv`]

### Aligned weighted surfaces

- `hs_gpa_minus_sat_math_z`: `+0.480`
- `college_gpa_minus_sat_math_z`: `+0.626`
- `sat_math_minus_reading_z`: `-0.286`

[SOURCE: `sources/iq-sex-diff/data/psid/psid_tas_aligned_gaps.tsv`]

The basic geometry is clear: on this public transition surface, girls and young women look better on GPA-type evaluation outputs while boys and young men look better on high-stakes quantitative testing. [INFERENCE]

## Family-Linked Check

The first within-family check is a weighted family fixed-effects regression on the aligned best surfaces:

`score ~ female + age_years + C(family_id68)`

with clustered standard errors by `family_id68`. [SOURCE: `sources/iq-sex-diff/psid_tas_first_pass.py`; `sources/iq-sex-diff/data/psid/psid_tas_family_fe.tsv`]

Key coefficients:

- `hs_gpa_minus_sat_math_z`: `beta_female = +0.707`, `SE = 0.166`, `95% CI [0.381, 1.033]`
- `college_gpa_minus_sat_math_z`: `beta_female = +1.167`, `SE = 0.509`, `95% CI [0.169, 2.165]`
- `sat_math_minus_reading_z`: `beta_female = -0.423`, `SE = 0.136`, `95% CI [-0.690, -0.156]`

[SOURCE: `sources/iq-sex-diff/data/psid/psid_tas_family_fe.tsv`]

This does **not** identify a causal sex effect. It does reduce the simpler objection that the transition-stage GPA-versus-tested-math split is only shared-family composition. [INFERENCE]

## Causal Check

> **Observation:** in a family-linked public transition panel, normalized GPA surfaces tilt female, `SAT math`/`ACT` surfaces tilt male, and the aligned `GPA minus SAT math` wedge remains female-leaning both descriptively and within-family. [SOURCE: `sources/iq-sex-diff/data/psid/psid_tas_best_surface_gaps.tsv`; `sources/iq-sex-diff/data/psid/psid_tas_aligned_gaps.tsv`; `sources/iq-sex-diff/data/psid/psid_tas_family_fe.tsv`]
>
> **Null:** if the earlier school-linked wedge were only a low-stakes transcript artifact, the transition branch should not keep reproducing a female GPA versus male tested-math split on these later public surfaces. [INFERENCE]
>
> **Residual after null:** the `PSID TAS` result says the wedge is not confined to one transcript-rich school cohort and not confined to low-stakes standardized school tests. [INFERENCE]

- `P(cause)`: `0.72` that the school-linked / evaluation-versus-tested branch now extends into early-adult transition outcomes rather than stopping at secondary-school transcripts. [INFERENCE]
- `Top alternative`: `0.20` that this is still mostly a scale-composition issue because GPA normalization, admissions-test take-up, and college selection are all moving at once. [INFERENCE]
- `Falsifier`: a better-aligned transition dataset where GPA-type and tested quantitative surfaces converge once take-up, selection, and scale handling are fixed on common samples. [INFERENCE]
- `Decision impact`: treat `PSID TAS` as new support for the replicated evaluation-versus-tested split, not as a new general-ability surface. [INFERENCE]

## What This Does And Does Not Settle

What it settles enough to use:

- the public `PSID` branch is now not just child development; it also gives a family-linked transition panel
- the late-school wedge is no longer confined to `HSLS` transcript GPA or NCES school-recognition measures
- the transition branch now shows the same broad geometry: female GPA-type outputs, male tested-math outputs

What it does **not** settle:

- whether `GPA` and `SAT math` are separable because of evaluation, compliance, course choice, admissions selection, or college major selection
- whether the transition wedge is causally the same node as the secondary-school transcript wedge
- anything battery-independent about `g`

## Next Step

The best next transition step is not another raw summary. It is:

1. integrate `PSID TAS` into the school-wedge synthesis as a transition extension
2. keep the `2019` zero-weight caveat explicit in any weighted reuse
3. if the repo wants stronger causal leverage here, move to a mediator design or a richer restricted transcript/process surface rather than more public-use `TAS` slicing

[INFERENCE]
