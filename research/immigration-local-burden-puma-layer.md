# Local-burden upgrade: PUMA destination costs and school-age child exposure

Date: 2026-04-10

## Why I did not use metros

The public ACS microdata identify households by `STATE` and `PUMA`, not by `CBSA`. A metro layer can be approximated with crosswalks, but that adds fuzzy geography and invented precision. For this question, `PUMA` is the defensible public-use destination geography.

So this upgrade uses:

1. official ACS 2023 `PUMA` median gross rent from the Census API
2. household-level child-age counts from the local ACS person file
3. existing state-level school-spending context retained as the best currently joined public-finance layer

## New assets

1. [build_puma_context_assets.py](/Users/alien/Projects/research/sources/immigration-fiscal/data/derived/build_puma_context_assets.py)
2. [extend_immigration_context_with_pumas.sql](/Users/alien/Projects/research/sources/immigration-fiscal/data/derived/extend_immigration_context_with_pumas.sql)
3. [puma_median_gross_rent_2023.csv](/Users/alien/Projects/research/sources/immigration-fiscal/data/derived/origin/puma_median_gross_rent_2023.csv)
4. [census_acs1_2023_puma_median_gross_rent.json](/Users/alien/Projects/research/sources/immigration-fiscal/data/external/origin/census_acs1_2023_puma_median_gross_rent.json)
5. `puma_median_gross_rent_2023` in [immigration_context.duckdb](/Users/alien/Projects/research/sources/immigration-fiscal/data/derived/immigration_context.duckdb)
6. `acs_origin_puma_2023` in the same warehouse
7. `origin_puma_context_2023` in the same warehouse

## New measures

For each `origin x state x puma` cell, the warehouse now tracks:

1. `recent_low_skill_mean_hh_children_u18`
2. `recent_low_skill_share_with_children_u18_pct`
3. `recent_low_skill_mean_hh_school_age_children`
4. `recent_low_skill_share_with_school_age_children_pct`
5. `recent_low_skill_mean_hh_preschool_children`
6. `recent_low_skill_share_with_preschool_children_pct`
7. `median_gross_rent` at the `PUMA` level

This is materially better than the earlier state-average rent plus all-children count.

## Warehouse scale

1. `puma_median_gross_rent_2023`: `2,486` PUMAs
2. `acs_origin_puma_2023`: `33,997` origin-destination cells

## What changed substantively

Compared with the older state-level rent averages, the PUMA layer changes measured housing-cost exposure in both directions, depending on where within states origin groups actually concentrate.

Examples from the upgraded warehouse:

1. Colombia
   - weighted state rent: about `1685.88`
   - weighted PUMA rent: about `1870.13`
   - delta: about `+184.25`

2. Brazil
   - weighted state rent: about `1672.09`
   - weighted PUMA rent: about `1829.60`
   - delta: about `+157.51`

3. China
   - weighted state rent: about `1729.66`
   - weighted PUMA rent: about `1879.82`
   - delta: about `+150.16`

4. Venezuela
   - weighted state rent: about `1614.89`
   - weighted PUMA rent: about `1750.48`
   - delta: about `+135.59`

5. Mexico
   - weighted state rent: about `1715.56`
   - weighted PUMA rent: about `1604.47`
   - delta: about `-111.09`

The upgrade also sharpens the child-burden picture by separating school-age exposure from preschool exposure.

Top school-age exposure groups among origins with at least `10,000` recent low-skill adults:

1. Afghanistan: `2.69` school-age children per qualifying adult household on average; `87.89%` with school-age children
2. Myanmar: `1.38`; `70.42%`
3. Honduras: `1.19`; `68.64%`
4. El Salvador: `1.06`; `58.60%`
5. Dominican Republic: `0.96`; `56.95%`
6. Guatemala: `0.95`; `57.28%`
7. Mexico: `0.92`; `49.02%`

## Interpretation

The old state-average layer hid important within-state sorting. For urban-concentrated origin groups, state medians often understated destination rent. For some very large groups, especially Mexico, the state average overstated rent because the actual PUMA mix skews less expensive than the state mix.

The revised read is:

1. the `state-local negative` side remains strong for high school-age-child groups
2. housing exposure should be measured on actual destination geography, not assumed from state averages
3. the distribution of destination within a state materially changes the rent-incidence picture

## Limits that still remain

1. this is still `PUMA`, not true school district or municipal geography
2. school spending is still state-level, not district-level
3. rent is not the same thing as welfare loss
4. household child exposure is measured around qualifying adults, so two qualifying adults in one household can duplicate the same household child burden

## Bottom line

This is the right next layer. It is more precise than the earlier state-only model and avoids pretending that public-use microdata cleanly identify metro areas when they do not.
