# IQ Sex Differences - PSID CDS First Pass

**Date:** 2026-03-06  
**Purpose:** record the first cleaned public-use `PSID CDS` result and update the early-school branch with a family-linked child panel outside the `NLSY` / `ECLS` stacks.

## What Was Built

The repo now has a compact public-use `PSID CDS` child panel built from the downloaded `1997`, `2002`, and `2007` `CDS` bundles plus the cumulative linkage and sex map files. [SOURCE: `sources/iq-sex-diff/psid_cds_build_panel.py`; `sources/iq-sex-diff/data/psid/psid_cds_panel.parquet`; `sources/iq-sex-diff/data/psid/psid_cds_build_diagnostics.json`]

Wave coverage in the current build:

- `1997`: `2,223` rows
- `2002`: `2,644` rows
- `2007`: `1,506` rows
- combined panel: `6,373` rows, `3,220` unique children, `1,322` unique `1968` families

[SOURCE: `sources/iq-sex-diff/data/psid/psid_cds_build_diagnostics.json`]

The public `CDS/TAS` study documentation says the system provides linked child-development and transition data and supports intergenerational/family designs. [SOURCE: https://psidonline.isr.umich.edu/CDS/; https://psidonline.isr.umich.edu/CDS/Guide/StudyDesign.aspx]

## Data Hygiene Fixes

Three build issues mattered enough to change the first pass:

1. `999`-style sentinel values in the public child score fields had to be recoded to missing before any summary or model was trustworthy. [SOURCE: `sources/iq-sex-diff/psid_cds_first_pass.py`]
2. `2002` and `2007` age-at-interview variables in the assessment files are already in months, not years. Treating them as years and multiplying by `12` was wrong. [SOURCE: `sources/iq-sex-diff/psid_cds_build_panel.py`]
3. `1997 broad_math` is not an independent surface in the current public child file for this build; it duplicates the `1997 applied_problems` values and should not be counted separately. [SOURCE: `sources/iq-sex-diff/data/psid/psid_cds_surface_gaps.tsv`; `sources/iq-sex-diff/psid_cds_build_panel.py`]

These are real public-file hygiene issues, not cosmetic cleanup. [INFERENCE]

## Main Descriptive Result

The weighted public-use `CDS` child surfaces look structurally similar to the repo’s other early-school results:

- reading surfaces are female-leaning
- applied-problems math is male-leaning
- the aligned `math minus reading` surface is male-leaning in every available wave

[SOURCE: `sources/iq-sex-diff/data/psid/psid_cds_surface_gaps.tsv`; `sources/iq-sex-diff/data/psid/psid_cds_aligned_gaps.tsv`; `sources/iq-sex-diff/psid_cds_first_pass.py`]

Key weighted gaps (`female - male`, Cohen’s `d`):

### Raw score surfaces

- `1997 applied_problems`: `-0.131`
- `2002 applied_problems`: `-0.134`
- `2007 applied_problems`: `-0.130`
- `1997 broad_reading`: `+0.215`
- `2002 broad_reading`: `+0.139`
- `2007 broad_reading`: `+0.136`
- `1997 letter_word`: `+0.174`
- `2002 letter_word`: `+0.173`
- `2007 letter_word`: `+0.127`

[SOURCE: `sources/iq-sex-diff/data/psid/psid_cds_surface_gaps.tsv`]

### Relative `math minus reading` surfaces

- `1997 applied_minus_reading`: `-0.500`
- `2002 applied_minus_reading`: `-0.269`
- `2007 applied_minus_reading`: `-0.325`
- `1997 calculation_minus_reading`: `-0.285`

[SOURCE: `sources/iq-sex-diff/data/psid/psid_cds_aligned_gaps.tsv`]

## Family-Linked Check

The first family-linked check is a weighted family fixed-effects regression on the aligned child surfaces:

`score ~ female + age_years + C(wave) + C(family_id68)`

with clustered standard errors by `family_id68`. [SOURCE: `sources/iq-sex-diff/psid_cds_first_pass.py`; `sources/iq-sex-diff/data/psid/psid_cds_family_fe.tsv`]

Key coefficients:

- `applied_minus_reading`: `beta_female = -6.61`, `SE = 1.53`, `95% CI [-9.61, -3.61]`
- `calculation_minus_reading`: `beta_female = -4.50`, `SE = 1.55`, `95% CI [-7.54, -1.46]`

[SOURCE: `sources/iq-sex-diff/data/psid/psid_cds_family_fe.tsv`]

This does **not** identify a causal sex effect. It does reduce the simpler objection that the aligned child pattern is only shared-family composition. [INFERENCE]

## Causal Check

> **Observation:** in a family-linked public child panel, reading surfaces are female-leaning, applied-problems math is male-leaning, and aligned `math minus reading` remains male-leaning both descriptively and within-family. [SOURCE: `sources/iq-sex-diff/data/psid/psid_cds_surface_gaps.tsv`; `sources/iq-sex-diff/data/psid/psid_cds_aligned_gaps.tsv`; `sources/iq-sex-diff/data/psid/psid_cds_family_fe.tsv`]
>
> **Null:** the old child contradiction was mainly a score-family / anchoring problem rather than a true directional disagreement across cohorts. [INFERENCE]
>
> **Residual after null:** the `PSID CDS` result points the same way as the aligned `ECLS` work and weakens the case for reopening the child branch as directionally unresolved. [INFERENCE]

- `P(cause)`: `0.75` that the `PSID CDS` first pass strengthens the early-school emergence node rather than reopening the old child contradiction. [INFERENCE]
- `Top alternative`: `0.20` that anchor choice still exaggerates the magnitude of the child residual even though the direction is now stable. [INFERENCE]
- `Falsifier`: a stronger child bridge using multiple anchors or better psychometric rescoring that flips the aligned `PSID` sign back female or near zero. [INFERENCE]
- `Decision impact`: stop treating the old raw `NLSCYA` contradiction as the live child problem; the remaining child problem is magnitude, timing, and anchor choice. [INFERENCE]

## What This Does And Does Not Settle

What it settles enough to use:

- the repo now has a family-linked public child panel outside `NLSY` / `ECLS`
- early-school evidence is no longer resting on only the `ECLS` pair plus anchored `NLSCYA`
- the relative child `math versus reading` split is now stronger than it was yesterday

What it does **not** settle:

- battery-independent absolute early-math advantage
- the underlying mechanism of the child divergence
- whether the right anchor is reading, vocabulary, language, or something else

## Next Step

The best next child step is no longer “find another cohort.” It is:

1. multi-anchor child bridge sensitivity using `reading`, `letter-word`, and other verbal anchors where available
2. if the child branch still needs more leverage after that, decide whether `TAS` transition outcomes belong in the same developmental chain or in the later school/outcome branch

[INFERENCE]
