# IQ Sex Differences Dataset Expansion

**Date:** 2026-03-05
**Purpose:** record the expanded data-acquisition surface, what each dataset can
actually adjudicate, and which files are locally staged versus merely named in
planning docs.

This file is the acquisition-side companion to:

- `research/iq-sex-differences-dataset-cards.md`
- `research/iq-sex-differences-analysis-protocol.md`
- `research/iq-sex-differences-next-node-validation.md`
- `research/iq-sex-differences-additional-datasets.md`

## Why Expand The Stack

The active project risk is not “too little data” in the abstract. It is
over-relying on a few score surfaces and then narrating around them.

The expanded stack is meant to break that failure mode by adding four distinct
design families:

1. `TIMSS` grade 4 versus grade 8 for earlier-emergence checks.
2. `PISA` score, timing, and questionnaire layers for item-format and
   response-process audits near school exit.
3. `TIMSS Advanced` for upper-track / upper-tail adjudication.
4. `HSLS` / `ELS` / `NELS` / `HS&B` metadata and transcript infrastructure for
   grade-test wedge, course-ladder, and placement analysis.

## 2026-03-05 Follow-On Acquisition Update

Direct public-use acquisitions completed in this tranche:

0. `PSID CDS/TAS`
   - local downloads now staged under `sources/iq-sex-diff/data/psid/downloads/`
   - unpacked raw files now staged under `sources/iq-sex-diff/data/psid/unpacked/`
   - first cleaned child panel now built at `sources/iq-sex-diff/data/psid/psid_cds_panel.parquet`
   - first cleaned transition panel now built at `sources/iq-sex-diff/data/psid/psid_tas_panel.parquet`
   - first-pass memo: `research/iq-sex-differences-psid-cds-first-pass.md`
   - transition memo: `research/iq-sex-differences-psid-tas-transition-first-pass.md`

1. `NLSCYA`
   - local: `sources/iq-sex-diff/data/nlscya/nlscya_all_1979-2020.zip`
   - quick archive check confirms bundled `.csv`, `.dat`, `.sas`, and `.R` assets
2. `ECLS-K`
   - local: `sources/iq-sex-diff/data/ecls_k/Childk8p.zip`
   - quick archive check confirms `childk8p.dat`
3. `ECLS-K:2011`
   - local: `sources/iq-sex-diff/data/ecls_k2011/ChildK5p.zip`
   - quick archive check confirms `childK5p.dat`

NCES `Online Codebook` follow-through completed after that first pass:

4. `HSLS:09`
   - local: `sources/iq-sex-diff/data/hsls/HSLS_2017_PETS_SR_v1_0_SPSS_Datasets.zip`
   - local: `sources/iq-sex-diff/data/hsls/HSLS_2017_PETS_SR_v1_0_CodeBook_RecordFileLayout.zip`
   - manifest: `sources/iq-sex-diff/data/hsls/hsls_onlinecodebook_manifest.json`
5. `ELS:2002`
   - local: `sources/iq-sex-diff/data/els/ELS_2002-12_PETS_v1_0_Student_SPSS_Datasets.zip`
   - local: `sources/iq-sex-diff/data/els/ELS_2002-12_PETS_v1_0_Student_BRR_SPSS_Datasets.zip`
   - local: `sources/iq-sex-diff/data/els/ELS_2002-12_PETS_v1_0_Other_SPSS_Datasets.zip`
   - local: `sources/iq-sex-diff/data/els/ELS_2002-12_v1_0_CodeBook_RecordFileLayout.zip`
   - manifest: `sources/iq-sex-diff/data/els/els_onlinecodebook_manifest.json`
6. `NELS:88`
   - local: `sources/iq-sex-diff/data/nels/NELS_1988-00_v1_0_SPSS_Datasets.zip`
   - local: `sources/iq-sex-diff/data/nels/NELS_1988-00_v1_0_CodeBook_RecordFileLayout.zip`
   - manifest: `sources/iq-sex-diff/data/nels/nels_onlinecodebook_manifest.json`

Important blocker discovered in the same NCES pass:

- `HS&B` sessions can be created through the same `Online Codebook` API, and
  the browser renders a working `Download -> Get SPSS Formatted Data Files`
  control
- but the backing endpoint `GET /datalab/api/v1/onlinecodebook/session/<GUID>/file/data/1`
  currently returns `HTTP 500` for tested `HS&B` sessions
- that means `HS&B` is still public-use in principle, but currently blocked by
  an NCES-side server failure rather than by licensing or shell automation

## New Local Acquisitions

### Raw or Nearly-Raw Public Files Now Local

1. `TIMSS 2019 Grade 8`
   - local: `sources/iq-sex-diff/data/timss/T19_G8_SPSS Data.zip`
   - companions local: `Codebooks`, `Item Information`, `User Guide`
   - official page: <https://timss2019.org/international-database/>
   - why it matters: this is a real public international math battery with item
     support files, not just a citation target

2. `TIMSS 2019 Grade 4`
   - local files now present: `sources/iq-sex-diff/data/timss_grade4/T19_G4_SPSS Data.zip`,
     `T19_G4_Codebooks.zip`, `T19_G4_Item Information.zip`
   - why it matters: it gives an earlier developmental surface, which is the
     cleanest counter to “adult numeracy just reflects later accumulation”

3. `TIMSS Advanced 2015`
   - local files now present: `sources/iq-sex-diff/data/timss_advanced/TA15_SPSSData.zip`,
     `TA15_Codebooks.zip`, `TA15_UserGuide.pdf`, `TA15_ItemInformation.zip`
   - official page: <https://timssandpirls.bc.edu/timss2015/advanced-international-database/>
   - why it matters: it hits the advanced-track branch directly instead of
     inferring upper-tail behavior from broad-population adult numeracy

4. `PISA`
   - local now: `sources/iq-sex-diff/data/pisa/SPSS_STU_COG.zip`,
     `sources/iq-sex-diff/data/pisa/SPSS_STU_QQQ.zip`,
     `sources/iq-sex-diff/data/pisa/index.html`
   - additional `2018` timing / visits and `2022` cognitive / questionnaire
     files were actively downloading in this tranche
   - official index: <https://webfs.oecd.org/pisa2022/index.html>
   - why it matters: `PISA 2018` is the strongest public score-plus-timing
     school-exit surface currently identified in this project

### Metadata / Support Surfaces Still Useful Locally

1. `HSLS:09` variable list
   - local: `sources/iq-sex-diff/data/hsls/HSLS09_VariableList_rev01-24.xlsx`
   - official study page: <https://nces.ed.gov/surveys/hsls09/>
   - why it matters: keeps variable discovery lightweight even though the public-use respondent bundle is now staged

2. `ELS:2002` variable list and transcript support
   - local: `sources/iq-sex-diff/data/els/ELS2002_Variable_List_throughF3-PETS.zip`
   - support doc: `sources/iq-sex-diff/data/docs/ELS_03_transcript.pdf`
   - official page: <https://nces.ed.gov/surveys/els2002/availdataproducts.asp>
   - why it matters: transcript taxonomy and variable discovery are still easier here than inside the larger respondent files

3. `NELS:88` variable list
   - local: `sources/iq-sex-diff/data/nels/NELS_Variable_List.zip`
   - official page: <https://nces.ed.gov/surveys/nels88/data_products.asp>

4. `HS&B` study variable list
   - local: `sources/iq-sex-diff/data/hsb/HSB_STUDY_VARIABLE_LIST.xlsx`
   - official page: <https://nces.ed.gov/surveys/hsb/data.asp>

5. `HSTS` course taxonomy support file
   - local: `sources/iq-sex-diff/data/naep_hsts/cssc_list.xls`
   - official page: <https://nces.ed.gov/use-work/elementarysecondary/hst-high-school-transcript-studies>

## Datasets That Add Real Causal Leverage

| Dataset | New node it attacks | Why it is high value | Current local status |
|---|---|---|---|
| `TIMSS 2019 Grade 4 + Grade 8` | early emergence versus accumulation | Lets us see whether the male-leaning math surface is already there before school-exit sorting fully compounds | usable locally now |
| `PISA 2018` | timing / process / item-format / anxiety | Best public score-plus-response-process school-exit surface currently identified | partial local staging |
| `PISA 2022` | current item-content / adaptivity surface | Useful cross-check, but not the primary public timing file | partial local staging |
| `TIMSS Advanced 2015` | upper-track / advanced-selection branch | Cleaner than arguing from adult numeracy about the upper tail | usable locally now |
| `HSLS:09` | grade-test wedge, transcript ladder, identity sorting | Best U.S. school-exit replication target with public-use respondent files now staged | usable locally now |
| `ELS:2002` | earlier-cohort school-pipeline replication | Second transcript-rich U.S. cohort for stability checks, including BRR file | usable locally now |
| `NELS:88` | older-cohort background check | Helps distinguish recent-schooling stories from older recurring patterns | usable locally now |
| `HS&B` | older-cohort background check | Conceptually valuable, but the current NCES backend is failing on the public-use file endpoint | blocked by server error |

## Access-Gated Or Friction-Heavy Targets

### `PIAAC` log/paradata

This remains worth pursuing, but it is not yet “download and go” in this tree.

- OECD cycle page: <https://www.oecd.org/en/data/datasets/piaac-1st-cycle-database.html>
- GESIS public-use files: <https://www.gesis.org/en/data-on-adult-education/daten/piaac-daten-zyklus-1/piaac-international/international-public-use-files>
- GESIS international log files: <https://www.gesis.org/en/data-on-adult-education/daten/piaac-daten-zyklus-1/piaac-international/international-piaac-log-files>

Why still important:

- adult numeracy is one of the project’s more stable male-leaning surfaces
- process traces are the cleanest way to test whether timing / navigation / DIF
  explanations can move that adult surface materially

### `Project Talent`

The official researcher portal is promising for sibling / twin and high-ability
questions, but it is not staged locally yet.

- official portal: <https://www.air.org/project-talent/researchers>

Why it matters:

- long follow-up and strong ability / schooling surface
- plausible use for upper-tail and within-family questions

Current constraint:

- the site was partially blocked in shell access during this snapshot, so it is
  indexed here as a target rather than a staged asset

### `NAEP` process data

- official process-data page: <https://www.nationsreportcard.gov/processdata/>

Why it matters:

- the 2017 grade 4 and grade 8 mathematics process files are exactly the kind
  of score-generation surface that could strengthen or weaken the measurement
  artifact story

Current constraint:

- the richest public-use workflow is still more awkward than `TIMSS` / `PISA`
  for this project’s immediate next pass

## What Could Become Obvious With This Stack

### 1. Whether the math surface appears early or mostly accumulates

If `TIMSS Grade 4` is already materially male-leaning in mathematics across
countries and content domains, that weakens the strongest “later school
selection creates the whole gap” story.

If the main movement appears from `Grade 4` to `Grade 8` to `PISA`, that
hardens curriculum exposure, placement, or practice channels.

### 2. Whether the score gap is partly a response-process artifact

If `PISA 2018` timing / visits features materially compress or reverse a raw
math gap in a stable way, that would strengthen the measurement / process
artifact branch beyond the current `NLSY97` Stage A evidence.

If timing / visits barely move the gap, the project should stop leaning so hard
on process stories in school-exit datasets.

### 3. Whether the real disagreement lives in advanced-track selection

If `TIMSS Advanced 2015` shows a much more male-leaning advanced-math surface
than broad-population `PISA` or `TIMSS`, then part of the debate may be about
selection into advanced tracks rather than broad-population general ability.

### 4. Whether grades and placement are contaminated relative to tests

`HSLS`, `ELS`, and `NELS` do not help merely by existing. They help only if
used to measure the grade-test wedge, course ladders, transcript placement,
and identity sorting within the same cohort. `HS&B` stays on the map, but right
now it is acquisition-blocked by an NCES server failure rather than by theory.

## Immediate Priority Order

1. Finish the remaining `PISA` downloads already in motion.
2. Run `TIMSS 2019` grade 4 versus grade 8 first-pass sex-gap decomposition.
3. Build a `PISA 2018` score-plus-timing-plus-questionnaire intake script.
4. Run a `TIMSS Advanced 2015` upper-track mathematics pass once the first
   `TIMSS` grade decomposition is in place.
5. Use the now-local `HSLS` / `ELS` / `NELS` respondent bundles plus their
   staged manifests to lock the transcript / course / grade wedge variable map.
6. Keep `HS&B` as a live acquisition target, but treat it as server-blocked for
   now rather than “interactive-only”.

## Bottom Line

The dataset expansion changed the project in one important way: the next phase
no longer depends on arguing from `NLSY` plus `PIAAC` alone.

There is now a real staged path for:

- earlier-emergence checks (`TIMSS Grade 4`)
- school-exit timing / process checks (`PISA 2018`)
- advanced-track adjudication (`TIMSS Advanced 2015`)
- transcript / placement / wedge analysis (`HSLS`, `ELS`, `NELS`, `HSTS`)
- a concrete acquisition blocker report for `HS&B`, instead of vague “maybe
  interactive” uncertainty

That is a materially better evidence stack than the project had at the start of
the day.
