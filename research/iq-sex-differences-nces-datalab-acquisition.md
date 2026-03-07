# NCES DataLab Acquisition Notes

**Date:** 2026-03-05
**Purpose:** record the actual `NCES Online Codebook` acquisition path used to
stage `HSLS`, `ELS`, and `NELS`, and the live server-side failure encountered
for `HS&B`.

## What Was Verified

1. `NCES Online Codebook` exposes a direct API behind the browser UI.
2. Session GUIDs can be minted without manual browser interaction.
3. The file manifest endpoint returns direct zip URLs for at least `HSLS`,
   `ELS`, and `NELS`.
4. `HS&B` sessions can also be minted and opened in the browser, but the file
   endpoint currently returns `HTTP 500` for tested sessions.

## Verified API Path

### 1. Survey catalog

`GET https://nces.ed.gov/datalab/api/v1/onlinecodebook/survey?`

This exposes the survey catalog used by the browser UI.

### 2. Session GUID

Pattern:

`GET https://nces.ed.gov/datalab/api/v1/onlinecodebook/session/guid?surveyId=<ID>&surveyYear=<YEAR>&versionNumber=1.0`

Verified survey IDs and years used in this repo:

- `HSLS`: `surveyId=37`, `surveyYear=2017`
- `ELS`: `surveyId=11`, `surveyYear=2012`
- `NELS`: `surveyId=20`, `surveyYear=2000`
- `HS&B`: `surveyId=25`, `surveyYear=1980` also produced a session GUID

### 3. File manifest

Pattern:

`GET https://nces.ed.gov/datalab/api/v1/onlinecodebook/session/<GUID>/file/data/1`

Observed behavior:

- `HSLS`, `ELS`, `NELS`: returns JSON manifest with direct zip `location` URLs
- `HS&B`: returns `{"statusCode":500,"message":""}`

## Local Acquisition Outputs

### `HSLS`

Local files:

- `sources/iq-sex-diff/data/hsls/HSLS_2017_PETS_SR_v1_0_SPSS_Datasets.zip`
- `sources/iq-sex-diff/data/hsls/HSLS_2017_PETS_SR_v1_0_CodeBook_RecordFileLayout.zip`
- `sources/iq-sex-diff/data/hsls/hsls_onlinecodebook_manifest.json`

Quick archive check:

- `hsls_09_school_v1_0.sav`
- `hsls_17_student_pets_sr_v1_0.sav`

### `ELS`

Local files:

- `sources/iq-sex-diff/data/els/ELS_2002-12_PETS_v1_0_Student_SPSS_Datasets.zip`
- `sources/iq-sex-diff/data/els/ELS_2002-12_PETS_v1_0_Student_BRR_SPSS_Datasets.zip`
- `sources/iq-sex-diff/data/els/ELS_2002-12_PETS_v1_0_Other_SPSS_Datasets.zip`
- `sources/iq-sex-diff/data/els/ELS_2002-12_v1_0_CodeBook_RecordFileLayout.zip`
- `sources/iq-sex-diff/data/els/els_onlinecodebook_manifest.json`

Quick archive check:

- `els_02_12_byf3pststu_v1_0.sav`

### `NELS`

Local files:

- `sources/iq-sex-diff/data/nels/NELS_1988-00_v1_0_SPSS_Datasets.zip`
- `sources/iq-sex-diff/data/nels/NELS_1988-00_v1_0_CodeBook_RecordFileLayout.zip`
- `sources/iq-sex-diff/data/nels/nels_onlinecodebook_manifest.json`

Quick archive check:

- `nels_88_00_psef3f4_v1_0.SAV`
- `nels_88_00_byf4stu_v1_0.SAV`
- `nels_88_00_instf3f4_v1_0.SAV`
- `nels_88_00_pse1994_v1_0.SAV`

## `HS&B` Failure State

What was confirmed:

1. The browser can open a valid `HS&B` codebook session.
2. The `Download -> Get SPSS Formatted Data Files` control appears in the UI.
3. Clicking it triggers:

`GET https://nces.ed.gov/datalab/api/v1/onlinecodebook/session/<GUID>/file/data/1`

4. The response is `HTTP 500` with body:

`{"statusCode":500,"message":""}`

Interpretation:

- this is an NCES-side backend failure for the tested public-use `HS&B`
  `Online Codebook` path
- it is not just a shell limitation and not just a missing static link on the
  study page

Local probe artifact:

- `sources/iq-sex-diff/data/hsb/hsb_onlinecodebook_probe.txt`

## Reproducible Fetch Script

Local script:

- `sources/iq-sex-diff/download_nces_onlinecodebook_assets.py`

Example:

```bash
cd sources/iq-sex-diff
uv run python download_nces_onlinecodebook_assets.py --survey hsls els nels --download
```

The script:

- resolves the session GUID
- fetches the manifest JSON
- writes the manifest into the target data directory
- downloads the zip assets listed in the manifest

## Decision Impact

- `HSLS`, `ELS`, and `NELS` should now be treated as locally staged
  respondent-level public-use datasets, not as metadata-only targets.
- `HS&B` should stay in the plan, but as a concrete server-blocked acquisition
  target rather than as a vague “interactive-only” dataset.
