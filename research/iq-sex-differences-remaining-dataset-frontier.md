# Remaining Dataset Frontier

**Date:** 2026-03-06  
**Question:** after the current local stack (`NLSY79`, `NLSY97`, `ICAR`, `PIAAC`, `TIMSS`, `PISA`, `NLSCYA`, `ECLS`, `HSLS`, `ELS`, `NELS`), which additional datasets would still materially reduce uncertainty?

For the exact live access states and blockers, see `research/iq-sex-differences-access-playbook.md`.

## Executive Answer

The next outside data should not be “more math tests” in the abstract.

The remaining high-leverage additions are:

1. a transcript-test linkage dataset with stronger transcript microdata
2. a restricted process dataset that can actually test score-generation artifacts
3. a sibling / twin / upper-tail cohort for the residual-general-gap branch
4. an older-cohort background file if the public route becomes stable again

That ranks the current frontier as:

1. `HSTS` restricted microdata
2. `NAEP` process data
3. `Project Talent`
4. `HS&B` once the public endpoint works again

## Resolved Frontier Item - `PSID CDS/TAS`

**Why it matters**

This is now the cleanest family-linked external panel missing from the repo.

- the official `CDS-TAS` home page says the data center provides “easy and free access” to all waves of `CDS` and `TAS` data [SOURCE: https://psidonline.isr.umich.edu/CDS/]
- the `Getting Started` page says users should register, then use the data center [SOURCE: https://psidonline.isr.umich.edu/CDS/GettingStarted.aspx]
- the `Study Design` page says `CDS/TAS` supports caregiver and child standardized assessments of achievement and explicitly enables intergenerational and sibling-type designs [SOURCE: https://psidonline.isr.umich.edu/CDS/Guide/StudyDesign.aspx]
- the `FAQ` says the original `CDS` included Woodcock-Johnson math tests and broader developmental outcomes [SOURCE: https://psidonline.isr.umich.edu/CDS/Guide/FAQ.aspx]

**What node it attacks**

- `EarlySchoolEmergence`
- family-linked developmental heterogeneity
- sibling spillovers and within-family developmental sorting

**Why it is better than another school-exit cohort**

Because the current repo already has several late-school wedges. What it still lacks is a strong multigenerational family panel outside the `NLSY` ecosystem. [INFERENCE]

**Current local state**

The public-use bundles are now local and the first cleaned `CDS` child panel is built. So `PSID` is no longer part of the remaining external frontier. It has moved from acquisition to analysis. [SOURCE: `research/iq-sex-differences-access-playbook.md`; `research/iq-sex-differences-psid-cds-first-pass.md`]

## 2. `HSTS` Restricted Microdata

**Why it matters**

This is still the strongest transcript-test linkage target that is not fully local.

- the official `HST` access page says transcript data are available **only as restricted-use data** because of sensitivity [SOURCE: https://nces.ed.gov/surveys/hst/data.asp]
- the `Transcripts FAQ` confirms transcript data exist across `HS&B`, `NELS`, `ELS`, and `HSLS` collections and points users to restricted transcript access [SOURCE: https://nces.ed.gov/surveys/slsp/transcripts.asp]
- the NAEP research-center page says restricted-use `HSTS` files include school-linkable variables and transcript-school linkage infrastructure [SOURCE: https://nces.ed.gov/nationsreportcard/researchcenter/variablesrudata.aspx]
- the `HSTS` design page says microdata access exists under restricted-use licensing when needs cannot be met by the public explorer [SOURCE: https://nces.ed.gov/nationsreportcard/hsts/design.aspx]

**What node it attacks**

- transcript quantity versus transcript grade versus tested math
- whether the `school-evaluation` family and `transcript-quantity` family really separate in cleaner microdata

**Why it is high value**

The current late-school synthesis says evaluation is the most stable female-leaning family and transcript quantity is less stable. `HSTS` is exactly the kind of dataset that can test whether that is real or a public-use artifact. It is also a real licensing decision, not a scraper problem. [INFERENCE]

## 3. `NAEP` Process Data

**Why it matters**

This is the cleanest remaining U.S. school-math process target, but it is restricted.

- the official `NAEP Process Data` page says grade 8 math process data were previously released and grade 4 math process data are also available for secondary analysis under restricted-use access [SOURCE: https://www.nationsreportcard.gov/process_data/]
- the same page says researchers get raw cognitive responses, process data, and survey data, and must apply for restricted-use access [SOURCE: https://www.nationsreportcard.gov/process_data/]

**What node it attacks**

- `MeasurementSurface`
- process burden versus content-family versus interface/navigation effects

**Why it matters now**

The repo already has good `PISA` and `TIMSS` process-adjacent evidence. The remaining U.S. school-age measurement question needs a restricted process dataset, not another proxy. [INFERENCE]

## 4. `Project Talent`

**Why it matters**

This is still the strongest upper-tail / sibling / twin addition.

- AIR’s researcher page says `Project Talent` base-year data include cognitive ability, academic aptitude, and a very large national school sample with `4,508` twins/triplets and `83,948` siblings [SOURCE: https://www.air.org/project-talent/researchers]
- the same page currently says several federally funded repositories and active projects are **on hold** while administration priorities are being considered [SOURCE: https://www.air.org/project-talent/researchers]

**What node it attacks**

- `TrackSelection`
- upper-tail / advanced-selection claims
- sibling / twin residual-general-gap branch

**Why it is not first**

Because the current main uncertainty is still school-pipeline decomposition, not upper-tail metaphysics. `Project Talent` is valuable, but it is not the shortest path to reducing the current uncertainty. [INFERENCE]

## 5. `HS&B`

**Why it matters**

Still useful as an older-cohort background check.

- the official `HS&B` access page says public-use microdata are available through the `Online Codebook` and restricted-use data are also available [SOURCE: https://nces.ed.gov/surveys/hsb/accessingData.asp]
- the same site has a separate restricted-data page [SOURCE: https://nces.ed.gov/surveys/hsb/restricted_data.asp]

**Current local blocker**

The live `Online Codebook` public file endpoint has been returning `HTTP 500` in our local acquisition path, so `HS&B` is conceptually available but operationally blocked right now. [SOURCE: `research/iq-sex-differences-nces-datalab-acquisition.md`]

## Ranked Next Acquisitions

1. `HSTS` restricted microdata
2. `NAEP` process data
3. `Project Talent`
4. `HS&B` once the NCES endpoint works or a manual route is used

## Decision Impact

The external frontier has shifted.

The repo no longer needs another family-linked child panel first; `PSID CDS` now covers that design family, and `PSID TAS` now covers the same family-linked line into the transition branch.

It now needs:

1. transcript/test linkage with better transcript detail
2. true process logs
3. upper-tail / sibling leverage
4. an older-cohort background file if the public endpoint becomes stable

That is a better next external stack than another generic adult numeracy or school-exit battery. [INFERENCE]
