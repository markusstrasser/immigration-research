# Immigration school service complexity layer

Date: 2026-04-11

## Purpose

This memo turns the stage-4 school-side acquisitions into a usable district/state context layer.

It does not estimate immigrant-specific school costs. It builds the public district surface needed before anyone can do that honestly.

## Built assets

Derived outputs:
1. [saipe_school_district_2023.csv](sources/immigration-fiscal/data/derived/stage4/saipe_school_district_2023.csv)
2. [school_service_complexity_district_2023.csv](sources/immigration-fiscal/data/derived/stage4/school_service_complexity_district_2023.csv)
3. [school_service_complexity_state_2023.csv](sources/immigration-fiscal/data/derived/stage4/school_service_complexity_state_2023.csv)
4. [school_service_complexity_2023.meta.json](sources/immigration-fiscal/data/derived/stage4/school_service_complexity_2023.meta.json)
5. [nces_elsi_district_english_columns_probe_2026-04-11.json](sources/immigration-fiscal/data/derived/stage4/nces_elsi_district_english_columns_probe_2026-04-11.json)

Build scripts:
1. [build_stage4_school_service_context.py](sources/immigration-fiscal/data/derived/build_stage4_school_service_context.py)
2. [probe_nces_elsi_district_english_columns.py](sources/immigration-fiscal/data/derived/probe_nces_elsi_district_english_columns.py)
3. [extend_immigration_context_stage4.sql](sources/immigration-fiscal/data/derived/extend_immigration_context_stage4.sql)

Raw inputs:
1. [ussd23.txt](sources/immigration-fiscal/data/external/stage4/saipe/ussd23.txt) [SOURCE: https://www2.census.gov/programs-surveys/saipe/datasets/2023/2023-school-districts/ussd23.txt]
2. [census_school_finance_2023.txt](sources/immigration-fiscal/data/external/census_school_finance_2023.txt)
3. [ccd_lea_029_2324_w_1a_073124.zip](sources/immigration-fiscal/data/external/stage4/nces/ccd_lea_029_2324_w_1a_073124.zip) [SOURCE: https://nces.ed.gov/ccd/Data/zip/ccd_lea_029_2324_w_1a_073124.zip]

## Method

1. Parsed `SAIPE` 2023 school-district fixed-width records using the official layout. [SOURCE: https://www2.census.gov/programs-surveys/saipe/technical-documentation/file-layouts/school-district/2023-district-layout.txt]
2. Reconstructed district `LEAID` as `state_fips + district_id`.
3. Joined that key to `Census school finance 2023` district rows and to the current `NCES` `2023-24` final `LEA` directory.
4. Materialized component ratios:
   - `relevant_children_poverty_rate_pct`
   - `relevant_children_per_enrolled_student`
   - `relevant_children_per_operational_school`

Important constraint:
1. this layer is about district child intensity and school context
2. it is not an immigrant-status ledger
3. it is not a marginal-cost model
4. it does not yet include validated current district `English learner` counts

## Coverage

Observed join coverage:
1. `13,143` `SAIPE` district rows
2. `12,915` school-finance matches, or `98.27%`
3. `13,106` current-directory matches, or `99.72%`

Source:
1. [school_service_complexity_2023.meta.json](sources/immigration-fiscal/data/derived/stage4/school_service_complexity_2023.meta.json)

Interpretation:
1. the public district surface is good enough to use for state/district burden structure
2. a few states still need caution on finance coverage, especially `VT`, `ME`, and `NH`

## Main findings

Largest states by relevant children `5-17` in the built layer:
1. `CA` `6.35M`, child poverty rate `14.35%`
2. `TX` `5.62M`, child poverty rate `17.40%`
3. `FL` `3.26M`, child poverty rate `15.06%`
4. `NY` `2.92M`, child poverty rate `17.43%`
5. `IL` `2.04M`, child poverty rate `13.90%`

Highest child-poverty states among states with at least `500k` relevant children:
1. `LA` `23.82%`
2. `MS` `23.02%`
3. `AL` `19.81%`
4. `OK` `18.95%`
5. `AR` `18.81%`

Illustrative large districts with high child-poverty rates in this layer:
1. `Detroit Public Schools Community District` `115,020` relevant children, `44.20%` child poverty
2. `Cleveland Municipal` `55,799` relevant children, `36.99%` child poverty
3. `Orleans Parish` `51,481` relevant children, `33.44%` child poverty
4. `Memphis-Shelby County Schools` `130,259` relevant children, `33.09%` child poverty
5. `ALIEF ISD` `51,124` relevant children, `31.72%` child poverty

Sources:
1. [school_service_complexity_state_2023.csv](sources/immigration-fiscal/data/derived/stage4/school_service_complexity_state_2023.csv)
2. [school_service_complexity_district_2023.csv](sources/immigration-fiscal/data/derived/stage4/school_service_complexity_district_2023.csv)

## Bounded `ELSi` result

I ran a bounded `ELSi` probe against district tabs for `2023-24` and `2024-25` using the public `tableGenerator.aspx/GetColumns` web method.

What survived:
1. district `Enrollments`, `Enrollment Details`, `Enrollment by Grade/Race/Ethnicity & Gender`, and `Characteristics` did not surface `English learner` columns in this pass
2. the only term hit was a false positive in `Teacher & Staff`, from `intellectual development` text rather than an `EL` measure

Source:
1. [nces_elsi_district_english_columns_probe_2026-04-11.json](sources/immigration-fiscal/data/derived/stage4/nces_elsi_district_english_columns_probe_2026-04-11.json)

Interpretation:
1. the current public route to district `EL` counts remains unresolved
2. the repo should not claim that current district `English learner` counts are already integrated

## What this changes

Before this build, the school side was mostly:
1. state averages
2. county bridges
3. prototype sub-state geometry work

After this build, the repo now has a national public district surface for:
1. child concentration
2. child poverty intensity
3. matched school-finance context
4. matched current `LEA` directory context

That is enough to support a more serious `school service complexity` branch.

It is still not enough for:
1. immigrant-status attribution
2. newcomer / `ELL` service intensity
3. a finished school-cost causal estimate

## Bottom line

The school burden question is now better posed.

The right object is no longer just `state per-pupil spending`.
It is `district child intensity + district child poverty + finance context + eventually validated EL counts`.
