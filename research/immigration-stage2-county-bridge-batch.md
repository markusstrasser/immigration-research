# Immigration stage-2 county bridge batch

Date: 2026-04-10

## Result

This batch completed the `county-first` fusion path for the immigration incidence project.

The important methodological correction is that I did **not** force a district or CBSA bridge from public-use ACS geography. The defensible path is:
1. `origin x PUMA` from ACS-derived tables.
2. `PUMA x county` from TIGER geometry, area-weighted.
3. `county` school finance, housing stress, and IRS migration balance.

[SOURCE: sources/immigration-fiscal/data/derived/build_puma_county_crosswalk.py]
[SOURCE: sources/immigration-fiscal/data/derived/extend_immigration_context_stage2.sql]

## Data staged or acquired

New staged files under `sources/immigration-fiscal/data/external/stage2`:
1. NCES CCD fiscal bundle: [ccd_2024_25_universe_2025306_0.zip](sources/immigration-fiscal/data/external/stage2/nces/ccd_2024_25_universe_2025306_0.zip)
2. Census SIPP 2023 PUF: [pu2023_csv.zip](sources/immigration-fiscal/data/external/stage2/census/sipp/pu2023_csv.zip)
3. HUD CHAS county/state/tract bundles and dictionary:
[2018thru2022-050-csv.zip](sources/immigration-fiscal/data/external/stage2/hud/chas/2018thru2022-050-csv.zip)
[2018thru2022-040-csv.zip](sources/immigration-fiscal/data/external/stage2/hud/chas/2018thru2022-040-csv.zip)
[2018thru2022-140-csv.zip](sources/immigration-fiscal/data/external/stage2/hud/chas/2018thru2022-140-csv.zip)
[CHAS-data-dictionary-18-22.xlsx](sources/immigration-fiscal/data/external/stage2/hud/chas/CHAS-data-dictionary-18-22.xlsx)
4. IRS county/state migration CSVs:
[countyinflow2223.csv](sources/immigration-fiscal/data/external/stage2/irs/countyinflow2223.csv)
[countyoutflow2223.csv](sources/immigration-fiscal/data/external/stage2/irs/countyoutflow2223.csv)
[stateinflow2223.csv](sources/immigration-fiscal/data/external/stage2/irs/stateinflow2223.csv)
[stateoutflow2223.csv](sources/immigration-fiscal/data/external/stage2/irs/stateoutflow2223.csv)
5. TIGER 2023 PUMA ZIPs under [tiger_puma2023](sources/immigration-fiscal/data/external/stage2/census/tiger_puma2023)

## SSD corpus check

Most relevant SSD assets found:
1. `/Volumes/SSK1TB/corpus/census_acs` about `2.3G`
2. `/Volumes/SSK1TB/corpus/census_acs_5yr` about `45G`
3. `/Volumes/SSK1TB/corpus/census_acs_tables` about `1.3G`
4. `/Volumes/SSK1TB/corpus/hud_housing` about `184M`
5. `/Volumes/SSK1TB/corpus/irs_soi` about `1.1G`
6. `/Volumes/SSK1TB/corpus/census_lehd` about `363M`
7. `/Volumes/SSK1TB/corpus/bls_qcew` about `3.6G`
8. `/Volumes/SSK1TB/corpus/bea_data` about `312M` plus BEA GDP and CAINC files

Judgment:
1. The SSD is strong enough for a later LEHD/QCEW/BEA phase.
2. The staged IRS county/state extracts are still the cleaner immediate migration source.

## Derived artifacts

Scripts:
1. [build_stage2_incidence_context.py](sources/immigration-fiscal/data/derived/build_stage2_incidence_context.py)
2. [build_puma_county_crosswalk.py](sources/immigration-fiscal/data/derived/build_puma_county_crosswalk.py)
3. [extend_immigration_context_stage2.sql](sources/immigration-fiscal/data/derived/extend_immigration_context_stage2.sql)

Derived files:
1. [school_finance_county_2023.csv](sources/immigration-fiscal/data/derived/stage2/school_finance_county_2023.csv)
2. [chas_county_housing_stress_2018_2022.csv](sources/immigration-fiscal/data/derived/stage2/chas_county_housing_stress_2018_2022.csv)
3. [irs_migration_county_2022_2023.csv](sources/immigration-fiscal/data/derived/stage2/irs_migration_county_2022_2023.csv)
4. [puma_county_area_xwalk_2023.csv](sources/immigration-fiscal/data/derived/stage2/puma_county_area_xwalk_2023.csv)
5. [puma_county_area_xwalk_2023_summary.json](sources/immigration-fiscal/data/derived/stage2/puma_county_area_xwalk_2023_summary.json)
6. [nces_ccd_2024_25_bundle_inventory.csv](sources/immigration-fiscal/data/derived/stage2/nces_ccd_2024_25_bundle_inventory.csv)
7. [stage2_outputs.json](sources/immigration-fiscal/data/derived/stage2/stage2_outputs.json)

## Warehouse objects

Loaded into [immigration_context.duckdb](sources/immigration-fiscal/data/derived/immigration_context.duckdb):
1. `school_finance_county_2023` with `3120` rows
2. `chas_county_housing_stress_2018_2022` with `3222` rows
3. `irs_migration_county_2022_2023` with `3143` rows
4. `puma_county_area_xwalk_2023` with `14856` rows
5. `county_stage2_context_2023` with `3223` rows
6. `puma_county_context_2023` with `2487` rows
7. `origin_puma_household_stage2_context_2023` with `2853` rows

[SOURCE: DuckDB counts run this session]

## Important implementation details

School finance:
1. The county layer uses the full Census finance extract already present in the repo: [census_school_finance_2023.txt](sources/immigration-fiscal/data/external/census_school_finance_2023.txt)
2. `CONUM` is already county FIPS.
3. The raw file has a trailing blank field, so pandas must use `index_col=False` or columns shift.
4. County current spending is built from `TCURELSC + TCURINST + TCURSSVC + TCUROTH`, not from a nonexistent `TCURSPND` field.

Housing:
1. The county housing layer comes from CHAS `Table11` and measures `1 or more of the 4 housing problems` rather than pretending rent change is welfare.
2. This captures cost burden, overcrowding, and housing-quality stress.

Migration:
1. The bridged PUMA layer carries normalized IRS netflow balance percentages, not raw area-weighted counts.
2. Raw counts would look quantitative and mean very little. [INFERENCE]

## Unresolved

`SIPP` is staged but not trusted as a fused analytical layer.

Reason:
1. The file is pipe-delimited and person-wave structured.
2. The original parser assumptions were wrong.
3. I did not push another heavy laptop pass after the user explicitly warned about RAM pressure.

That means:
1. The county bridge is complete.
2. The school and housing bundles are fused.
3. The SIPP microsim layer remains `staged / unresolved`.

## Bottom line

The warehouse now supports a materially better local-burden analysis than the earlier state-average version, and it does so without fake district precision.
