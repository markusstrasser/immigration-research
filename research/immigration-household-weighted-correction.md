# Household-weighted correction for local child-burden estimates

Date: 2026-04-10

## What was wrong

The earlier child-burden measures in the origin `PUMA` layer were adult-linked:

1. each qualifying adult carried the full count of children in the household
2. that is acceptable as a description of `the average adult's household`
3. it is not the right object for estimating household-normalized school burden

I then built a quick proxy using person weights as if they were household weights. That proxy was wrong and is superseded.

Do not use:

1. `acs_origin_puma_household_proxy_2023`
2. `origin_puma_household_proxy_context_2023`

## Correct method

Use the official ACS housing file and housing weight.

1. Merge ACS housing and person files on `SERIALNO`
2. Use `WGTP` for household-level estimates
3. Use `PWGTP` only for person-level counts
4. Keep `PUMA` as the public-use destination geography

Official sources:

1. ACS 2023 PUMS access page: https://www.census.gov/programs-surveys/acs/microdata/access.2023.html
2. ACS 2023 PUMS user guide: https://www2.census.gov/programs-surveys/acs/tech_docs/pums/2023ACS_PUMS_User_Guide.pdf
3. ACS 2023 PUMS data dictionary: https://www2.census.gov/programs-surveys/acs/tech_docs/pums/data_dict/PUMS_Data_Dictionary_2023.pdf

## New assets

1. [extend_immigration_context_with_households.sql](/Users/alien/Projects/research/sources/immigration-fiscal/data/derived/extend_immigration_context_with_households.sql)
2. [psam_husa.csv](/Volumes/SSK1TB/corpus/census_acs/psam_husa.csv)
3. [psam_husb.csv](/Volumes/SSK1TB/corpus/census_acs/psam_husb.csv)
4. `acs_origin_puma_household_2023` in [immigration_context.duckdb](/Users/alien/Projects/research/sources/immigration-fiscal/data/derived/immigration_context.duckdb)
5. `acs_origin_household_national_2023` in the same warehouse
6. `origin_puma_household_context_2023` in the same warehouse

## What the corrected table contains

For each `origin x state x puma` cell:

1. `linked_household_wgt`: households containing at least one qualifying recent low-skill adult from that origin
2. `allocated_household_wgt_by_adult_count`: household weight allocated across mixed-origin households by qualifying-adult count share
3. `linked_mean_qual_adults_per_household`
4. `linked_mean_hh_school_age_children`
5. `linked_mean_hh_preschool_children`
6. `linked_share_households_with_school_age_children_pct`
7. `linked_household_weight_single_origin_share_pct`
8. allocated child totals by adult-count share

## Main result

The bad proxy was catastrophically wrong. The proper housing-weighted correction is not.

Compared with the adult-linked `PUMA` layer, the proper linked-household estimates are usually in the same ballpark, but somewhat different.

Examples:

1. Myanmar
   - adult-linked school-age children: `1.3811`
   - housing-weighted linked household estimate: `1.2650`
   - delta: `-0.1161`

2. Venezuela
   - adult-linked: `0.6743`
   - linked household: `0.5668`
   - delta: `-0.1075`

3. Afghanistan
   - adult-linked: `2.6933`
   - linked household: `2.6291`
   - delta: `-0.0642`

4. Mexico
   - adult-linked: `0.9199`
   - linked household: `1.0114`
   - delta: `+0.0915`

5. Honduras
   - adult-linked: `1.1934`
   - linked household: `1.2855`
   - delta: `+0.0921`

So the correction matters, but it does not reverse the overall picture. The strongest local school-burden groups remain broadly the same.

## Corrected top school-age burden rankings

Among origin groups with at least `10,000` recent low-skill adults:

1. Afghanistan: `2.6291` school-age children; `86.67%` of linked households have school-age children
2. Honduras: `1.2855`; `70.87%`
3. Myanmar: `1.2650`; `66.14%`
4. El Salvador: `1.0600`; `58.63%`
5. Mexico: `1.0114`; `53.49%`
6. Guatemala: `0.9960`; `59.07%`
7. Dominican Republic: `0.9229`; `56.46%`
8. Brazil: `0.8333`; `52.02%`
9. Haiti: `0.8084`; `46.01%`
10. China: `0.7645`; `51.83%`

## Mixed-origin households are not the main problem

The linked-household single-origin shares are high.

Examples:

1. Mexico: `97.91%`
2. China: `98.71%`
3. India: `99.36%`
4. Afghanistan: `99.44%`
5. Honduras: `94.99%`
6. Guatemala: `94.80%`

This means mixed-origin qualifying households exist, but they are not the dominant source of distortion. The bigger issue was unit-of-analysis mismatch, not mixed-origin complexity.

## Combined local-pressure read

Using corrected school-age burden plus `PUMA` rent:

1. Afghanistan remains the clearest school-system burden case
2. Honduras, El Salvador, Mexico, and Guatemala remain the largest high-burden Latin American cases
3. China, Colombia, Brazil, and Venezuela remain notable for high `PUMA` rent exposure even when school-age burden is more moderate

## Bottom line

The right correction was to move from adult-linked child counts to housing-weighted household estimates.

That correction improves the analysis materially, but it does not rescue the optimistic reading. The local-burden story remains real. The stronger conclusion now is simply cleaner: some groups are school-heavy, some are housing-heavy, and some are both.
