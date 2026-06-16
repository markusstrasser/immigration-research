# Immigration Receiver Data Acquisition — 2026-04-23

## Bottom Line

[DATA] Three higher-certainty inputs are now staged for the receiver-node theory: 2024 ACS PUMS, a repaired QWI county-quarter receiver panel, and the March 2026 EOIR case-data archive. A first 2024 ACS PUMA exposure table is also built.

[INFERENCE] These are the right next inputs because the current frontier is no longer "does immigration have an average national effect?" It is whether particular receiver nodes show synchronized pressure across housing, courts, schools, shelter, labor markets, and political backlash after composition and capacity are accounted for.

## Acquired Artifacts

| Layer | Local artifact | Source | Verification |
|---|---|---|---|
| 2024 receiver exposure | `sources/immigration-causal/data/external/census_acs_2024_1yr/` | [SOURCE: https://www2.census.gov/programs-surveys/acs/data/pums/2024/1-Year/] | SHA-256 manifest in `ACQUIRED.md` |
| 2024 receiver exposure derived table | `sources/immigration-causal/data/derived/acs_2024_receiver_exposure/acs_2024_receiver_exposure_puma.parquet` | [SOURCE: https://www2.census.gov/programs-surveys/acs/data/pums/2024/1-Year/] | `1,134` receiver-state PUMAs; `1,552,403` person records kept |
| County-quarter labor market | `sources/immigration-causal/data/lehd/qwi_county_receiver_panel.parquet` | [SOURCE: https://api.census.gov/data/timeseries/qwi/se] | `750,192` rows; repaired timeout recorded in audit JSON |
| Immigration court load | `sources/immigration-causal/data/external/eoir_case_data_2026_02/eoir_case_data_feb2026.zip` | [SOURCE: https://fileshare.eoir.justice.gov/EOIR%20Case%20Data.zip] | `unzip -tq` passed; SHA-256 manifest in `ACQUIRED.md` |

## What Previous Passes Were Still Missing

[INFERENCE] Previous models over-focused on annual county averages. That surface is useful for screening, but it blurs the causal object: migrants arrive through specific receiver nodes, while burdens are borne by renters, school districts, court venues, shelters, and local budgets with different capacity constraints.

[INFERENCE] Previous models also tended to let one channel stand in for the whole theory. A wage null does not disprove court, shelter, or school overload. A shelter spike does not prove broad fiscal harm. The stronger test is channel synchronization after exposure is measured at the relevant receiver level.

[LIMIT] The new data still does not directly identify undocumented status in ACS, respondent residence in EOIR, or immigrant status in QWI. The stronger design is a triangulation design, not a single magic dataset.

## More Powerful Theory To Test

[INFERENCE] The current strongest theory is:

`flow x capacity x composition x regime -> local incidence -> political feedback`

This beats "immigration good/bad" because it predicts heterogeneity. The theory expects weak or null average effects in low-exposure or high-capacity places, and nonlinear pressure in low-capacity receiver nodes when large flows concentrate into constrained housing, court, shelter, school, or labor-market institutions.

## Next Analyses

1. Validate and enrich the 2024 ACS PUMS receiver-exposure table.
   - [DATA] Built fields include nativity, noncitizenship, year-of-entry `2020+`, moved-from-abroad `MIG == 2`, children, school-age children, no-HS adults, limited English, rent burden, and household crowding.
   - [LIMIT] PUMA geography requires crosswalk/approximation before county or metro joins.

2. Build the EOIR court-pressure panel.
   - [DATA] Start with `A_TblCase.csv`, `B_TblProceeding.csv`, `tbl_schedule.csv`, `tbl_Court_Appln.csv`, and lookups for court, nationality, decision, application, and base city.
   - [LIMIT] Treat court venue as a pressure venue, not a residence geography.

3. Join QWI to the receiver-county panel.
   - [DATA] Test county-quarter outcomes by education and industry for receiver states.
   - [LIMIT] QWI is an outcome layer; exposure must come from ACS, OHSS/encounters, or existing receiver/capacity panels.

4. Produce a kill-test table by receiver node.
   - [INFERENCE] The theory gets stronger if housing, shelter, court load, labor outcomes, and political shift move together in exposed low-capacity nodes.
   - [INFERENCE] The theory weakens if only one channel moves, or if movement disappears after resident-weighted exposure and capacity controls.

## Blocked Or Still Thin

[LIMIT] Current public NCES CCD pages expose current district directory files, but the current public district English Learner route remains unresolved in this repo. The school-service layer remains useful but not yet a clean current EL panel.

[LIMIT] The SSD staging path `/Volumes/SSK1TB/corpus/` is not reliable from this process right now because newly downloaded APFS/noowners files acquired unreadable provenance xattrs. Working copies for this pass were therefore staged internally under `sources/immigration-causal/data/external/`.

## First ACS Screen

[DATA] Highest `recent_entry_2020plus_share` PUMAs among the receiver states in the first pass are concentrated in Florida, Texas, New Jersey, and Massachusetts.

[LIMIT] These are exposure candidates, not causal findings. The next step is to map `STATE-PUMA` to metro/county/receiver-node definitions and then test whether housing, shelter, court, school, QWI, and political outcomes move in the same places.
