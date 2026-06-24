# Immigration next-agent handoff — 2026-04-11

## Purpose

This is the handoff state for the public-use lifetime-fiscal build.

Read this first before touching the newly acquired public datasets.

## Current state

The project is no longer blocked on basic public-data acquisition.

What is now true:
1. `SIPP 2024` is on disk and verified to contain the key nativity / citizenship / year-of-entry / earnings / transfer fields.
2. `MEPS HC-251` is on disk and verified to contain the key health-cost and payer-incidence fields.
3. The `MEPS` health-cost module has been built as a compact derived table at [meps_health_cost_module_2023.csv](sources/immigration-fiscal/data/derived/stage3_proto/meps_health_cost_module_2023.csv).
4. `IRS SOI` county aggregates are on the SSD, but they are not the individual tax microdata needed for federal microsimulation.
5. `Synthetic SIPP` is worth pursuing and the application-side documents are staged locally.
6. `PSID` exists and is public-use, but direct scripted download was brittle in this pass.
7. A clean weighted `ACS` stock cut now exists for foreign-born adults ages `25-64` in three education buckets: `<HS`, `HS / GED`, and `some college / associate`.
8. There is still no repo-grade bucket-specific lifetime `NPV` for those three education buckets.
9. A stage-4 local-capacity acquisition pass is now on disk for `SAIPE`, court/language-access documents, and current NCES CCD `LEA` file-tool artifacts.
10. The current public route to district-level `English learner` counts is still not pinned down cleanly; the saved NCES `2023-24` `LEA` file-tool response surfaced `Directory`, `Membership`, and `Staff`, but not a validated current `EL` component.
11. A national stage-4 school-service context layer is now built from `SAIPE` + Census school finance + the current NCES `LEA` directory.
12. A bounded `ELSi` web-method probe for `2023-24` and `2024-25` district tabs did not surface current district `English learner` columns in the expected enrollment tabs.
13. `SIPP` to `MEPS` bridge output is now built and complete: `sipp_meps_bridge_cells_2024.csv` plus `sipp_meps_expected_health_cost_cells_2024.csv` (expected rows for the scenario engine).

## Files to read first

1. [immigration-public-mvp-readiness-2026-04-11.md](research/immigration-public-mvp-readiness-2026-04-11.md)
2. [immigration-public-mvp-meps-module-2026-04-11.md](research/immigration-public-mvp-meps-module-2026-04-11.md)
3. [immigration-public-mvp-profiling-findings-2026-04-11.md](research/immigration-public-mvp-profiling-findings-2026-04-11.md)
4. [immigration-public-mvp-sipp-meps-bridge-2026-04-11.md](research/immigration-public-mvp-sipp-meps-bridge-2026-04-11.md)
5. [immigration-public-mvp-variable-dictionary-2026-04-11.md](research/immigration-public-mvp-variable-dictionary-2026-04-11.md)
6. [build_public_mvp_sipp_module_2024.py](sources/immigration-fiscal/data/derived/build_public_mvp_sipp_module_2024.py)
7. [sipp_public_mvp_cells_2024.meta.json](sources/immigration-fiscal/data/derived/stage3_proto/sipp_public_mvp_cells_2024.meta.json)
8. [build_public_mvp_sipp_meps_bridge_2024.py](sources/immigration-fiscal/data/derived/build_public_mvp_sipp_meps_bridge_2024.py)
9. [sipp_meps_bridge_cells_2024.meta.json](sources/immigration-fiscal/data/derived/stage3_proto/sipp_meps_bridge_cells_2024.meta.json)
10. [meps_health_cost_module_2023.meta.json](sources/immigration-fiscal/data/derived/stage3_proto/meps_health_cost_module_2023.meta.json)
11. [build_public_mvp_meps_module.py](sources/immigration-fiscal/data/derived/build_public_mvp_meps_module.py)
12. [public_mvp_input_profile_2026-04-11.json](sources/immigration-fiscal/data/derived/public_mvp_input_profile_2026-04-11.json)
13. [profile_public_mvp_inputs.py](sources/immigration-fiscal/data/derived/profile_public_mvp_inputs.py)
14. [immigration-education-bucket-stock-and-lifetime-status-2026-04-11.md](research/immigration-education-bucket-stock-and-lifetime-status-2026-04-11.md)
15. [immigration-frontier-data-acquisition-2026-04-11.md](research/immigration-frontier-data-acquisition-2026-04-11.md)
16. [immigration-school-service-complexity-2026-04-11.md](research/immigration-school-service-complexity-2026-04-11.md)

## Verified local assets

### `SIPP`

Core files:
1. [pu2024_csv.zip](sources/immigration-fiscal/data/external/stage3/census/sipp/pu2024_csv.zip)
2. [2024_SIPP_Users_Guide.pdf](sources/immigration-fiscal/data/external/stage3/census/sipp/2024_SIPP_Users_Guide.pdf)
3. [SIPP_Data_Primer_MAY24.pdf](sources/immigration-fiscal/data/external/stage3/census/sipp/SIPP_Data_Primer_MAY24.pdf)

What is verified:
1. Header contains `5203` fields.
2. Verified fields present: `EBORNUS`, `ECITIZEN`, `TYRENTRY`, `EORIGIN`, `EHISPAN`, `ERACE`, `WPFINWGT`, `TPEARN`, `TSNAP_AMT`, `TTANF_AMT`, `TSSI_AMT`.
3. Official naming rules matter:
   - `A*` = status flags
   - `E*` = edited variables
   - `R*` = recodes
   - `T*` = public-use collapsed/topcoded variables
4. `TPEARN` is monthly total earnings from all jobs, not annual income.

What is not yet verified enough for publication:
1. full code meanings for `EBORNUS` and `ECITIZEN`
2. full-file national estimates from `SIPP`
3. any undocumented-specific inference from `SIPP`

### `MEPS`

Core files:
1. [h251dta.zip](sources/immigration-fiscal/data/external/stage3/ahrq/meps/h251dta.zip)
2. [h251dat.zip](sources/immigration-fiscal/data/external/stage3/ahrq/meps/h251dat.zip)
3. [h251su.txt](sources/immigration-fiscal/data/external/stage3/ahrq/meps/h251su.txt)

What is verified:
1. `MEPS` has `BORNUSA`, `YRSINUS`, `PERWT23F`, `INSURC23`, `TOTEXP23`, `TOTSLF23`, `TOTMCR23`, `TOTMCD23`, `TOTPRV23`, `TOTSTL23`.
2. `BORNUSA` meanings are decoded from the setup file:
   - `1` = yes, born in the U.S.
   - `2` = no
3. `YRSINUS` is categorical, not literal years.
4. `INSURC23` for under-65 is decoded:
   - `1` = any private
   - `2` = public only
   - `3` = uninsured
5. Full-file parsing through selected fixed-width fields succeeded.

What the first pass found:
1. foreign-born `25-64` adults have lower observed annual total health spending than U.S.-born adults in this file
2. foreign-born `25-64` adults also appear more uninsured

What is now built:
1. the module table has `81` cells from `18,919` MEPS person rows
2. cells are grouped by `age band x nativity x insurance category`
3. payer-specific means now exist for `TOTEXP23`, `TOTSLF23`, `TOTMCR23`, `TOTMCD23`, `TOTPRV23`, and `TOTSTL23`

### `IRS SOI`

Local path:
1. `/Volumes/SSK1TB/corpus/irs_soi`

What is verified:
1. county aggregates exist
2. corporate and exempt-org families exist
3. this is not the individual `IRS SOI PUF`

Implication:
1. usable for contextual calibration only
2. not usable as household-level tax microsim truth

### `Synthetic SIPP`

Staged application-side files:
1. [SSB_Application_clean_07.02.24.docx](sources/immigration-fiscal/data/external/stage3/census/sipp/SSB_Application_clean_07.02.24.docx)
2. [GSF_v7_Codebook.pdf](sources/immigration-fiscal/data/external/stage3/census/sipp/GSF_v7_Codebook.pdf)
3. [SSB_Request_Guidelines_May_2024.docx](sources/immigration-fiscal/data/external/stage3/census/sipp/SSB_Request_Guidelines_May_2024.docx)
4. [CLEARANCE_REQUEST_MEMO_SSBupdate_5.24.24.docx](sources/immigration-fiscal/data/external/stage3/census/sipp/CLEARANCE_REQUEST_MEMO_SSBupdate_5.24.24.docx)

What is verified:
1. official process is application -> approval -> SecureFTP
2. official page says there are four files of about `3-4GB` each
3. Census warns against publishing unvalidated synthetic-data results without validation against the confidential gold-standard files

## What not to trust

1. Any early `SIPP` result that used `A*` variables as substantive values.
2. Any interpretation of `TPEARN` as annual income.
3. Any use of county `IRS SOI` aggregates as if they were individual tax microdata.
4. Any undocumented-specific lifetime estimate from the current public stack.
5. Any claim that public-use data have already replaced `NAS`.
6. Any claim that the repo already has a defensible lifetime `NPV` for `<HS`, `HS / GED`, or `some college / associate`.

## What survives as high-confidence

1. `MEPS` now supports a real built health-cost module, not just a profiling note.
2. `SIPP` can support a real transition / transfers / labor-income module now, if the variable dictionary is respected.
3. The public MVP should be modular, not a one-number scalar NPV engine.
4. The repo can now answer three-bucket stock and state-share questions cleanly for the foreign-born `25-64` population.
5. The repo now has enough staged public material to start a `school service complexity` or `court and interpreter friction` memo without another generic scraping pass.
6. The `school service complexity` branch is no longer just a memo idea; it now has built district and state context tables plus a warehouse load script.
7. The `SIPP` transition module is now joined to MEPS health-cost cells with explicit bridge metadata.

## Recommended next build order

1. Build a small `SIPP` ingest around the verified dictionary.
   - do not bulk-load everything blindly
2. **Done**: Bridge the `SIPP` module to the built `MEPS` health-cost table and produce scenario-ready expected-health outputs.
3. Pin down access to the individual `IRS SOI PUF`.
4. Acquire `PSID` via its Data Center or packaged files.
5. Apply for `Synthetic SIPP`.
6. Resolve current district-level `English learner` counts from a source better than the current `ELSi` district tabs, or document the gap as a hard public-data limit.
7. Use the built school-service layer to produce a sharper district-based local-burden memo before attempting any causal school-cost scalar.

## Concrete next tasks

### Task 1: `SIPP` minimal module

Goal:
1. produce a compact derived table for working-age nativity/citizenship/year-of-entry cells with weighted monthly earnings and transfer exposure

Important constraint:
1. use only variables already vetted in the dictionary
2. do not infer semantics from prefixes casually

### Task 2: `IRS` access note

Goal:
1. document whether the individual PUF can be fetched directly, requested by contact, or needs a different acquisition path

### Task 3: `SIPP` -> `MEPS` bridge note

Goal:
1. **DONE** documented: mapping is now implemented in [build_public_mvp_sipp_meps_bridge_2024.py](sources/immigration-fiscal/data/derived/build_public_mvp_sipp_meps_bridge_2024.py) and recorded in [immigration-public-mvp-sipp-meps-bridge-2026-04-11.md](research/immigration-public-mvp-sipp-meps-bridge-2026-04-11.md).
2. next: consume [sipp_meps_expected_health_cost_cells_2024.csv](sources/immigration-fiscal/data/derived/stage3_proto/sipp_meps_expected_health_cost_cells_2024.csv) inside your scenario engine

## Practical engineering notes

1. Avoid expanding the full `3.43GB` `SIPP` CSV unless needed.
2. Streaming from zip worked and did not explode RAM.
3. The environment has `duckdb`, `pdftotext`, and `uv`.
4. The environment does **not** currently have `pandas` or `pyreadstat` installed.
5. For `MEPS`, the fixed-width parse via the official SAS setup file worked.

## Current stance

The project has crossed from `data acquisition` into `controlled module construction`.

The biggest remaining risk is not lack of data.
The biggest remaining risk is semantic sloppiness.
