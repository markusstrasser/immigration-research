# Synthesis: which new datasets should actually be fused

Date: 2026-04-10

## Bottom line

Do not add datasets just to make the warehouse look sophisticated. Add the smallest set that kills the strongest remaining objections.

The three most important fusion bundles are:

1. `School bundle`: `CCD district spine + F-33 + EDFacts`
2. `Housing bundle`: `CHAS + SAFMR + AHS`
3. `Federal/adjustment bundle`: `SIPP + LODES + IRS SOI + ORR`

If we build only those bundles, the analysis becomes much harder to dismiss.

## Why these bundles dominate

### 1. School bundle

This is the best next move because our current school-cost layer is still state-average and therefore blunt.

What it solves:
1. District finance instead of state finance.
2. English learner and migrant-student composition instead of plain child counts.
3. A real school burden surface instead of a proxy.

Expected effect on conclusions:
1. It will not erase the finding that some origin mixes are school-heavy.
2. It may materially reorder which destinations are most burdened.
3. It may show that some local-burden stories were understated because state averages washed out district intensity.

Primary sources:
1. NCES CCD district data [SOURCE: https://nces.ed.gov/ccd/pubageninfo.asp]
2. NCES F-33 [SOURCE: https://nces.ed.gov/ccd/f33agency.asp]
3. EDFacts [SOURCE: https://www.ed.gov/data/edfacts-initiative]

### 2. Housing bundle

This is second because our current housing signal is still mostly `rent exposure`, not `housing stress`.

What it solves:
1. Overcrowding and cost burden instead of rent alone.
2. ZIP-level or subcounty rent surfaces where PUMA medians are too coarse.
3. Doubling-up and unit quality, which matter more than price level for the crowding argument.

Expected effect on conclusions:
1. Some `housing-heavy` origin groups will stay housing-heavy.
2. Others may turn out to be `high-rent but not high-stress` groups.
3. The distinction between renter harm and owner gains becomes easier to discuss honestly.

Primary sources:
1. HUD CHAS [SOURCE: https://www.huduser.gov/portal/datasets/cp.html]
2. HUD SAFMR [SOURCE: https://www.huduser.gov/portal/datasets/fmr/smallarea/index.html]
3. AHS [SOURCE: https://www.census.gov/programs-surveys/ahs.html]

### 3. Federal/adjustment bundle

This is third, but conceptually it is the biggest missing piece.

What it solves:
1. A first real federal tax/transfer microsimulation using public-use data.
2. Relocation response rather than assuming static local populations.
3. Commuting-flow calibration rather than reading congestion off mean commute time.
4. Admission-channel decomposition for refugee-like flows.

Expected effect on conclusions:
1. This is the bundle most likely to weaken an overly negative national-welfare claim.
2. It is also the bundle most likely to clarify `federal positive / local negative` cells.
3. It will sharpen, not erase, the case for heterogeneity.

Primary sources:
1. SIPP [SOURCE: https://www.census.gov/programs-surveys/sipp.html]
2. LEHD LODES [SOURCE: https://lehd.ces.census.gov/data/#lodes]
3. IRS SOI migration [SOURCE: https://www.irs.gov/statistics/soi-tax-stats-migration-data]
4. ORR refugee arrivals [SOURCE: https://acf.gov/archive/orr/data/refugee-arrival-data]

## Denial pass

If the current analysis were wrong, what missing datasets would most likely expose that?

1. `SIPP` would expose a bad federal-incidence story.
2. `CHAS` and `AHS` would expose a bad housing-welfare story.
3. `CCD/F-33/EDFacts` would expose a bad school-cost magnitude story.
4. `IRS SOI` and `LODES` would expose a bad static-local-equilibrium story.

## Domain-forcing pass

Different disciplines point to different missing datasets:

1. `School administration` wants district finance, ELL, and district child concentration.
2. `Housing policy` wants overcrowding, cost burden, voucher rent surfaces, and housing quality.
3. `Transport engineering` wants OD commuting flows, not just average commute minutes.
4. `Public finance` wants actual transfer/tax structure, not wage proxies.

## Constraint-inversion pass

If we were forced to use only `three` new sources, they would be:

1. `NCES F-33 + EDFacts` as one school bundle,
2. `HUD CHAS`,
3. `SIPP`.

Reason:
1. Together they hit the two biggest current weaknesses: school-cost realism and federal-incidence realism.
2. `LODES` is fourth because it is excellent but less central than fixing the school and tax sides first.

## Recommended acquisition order

1. `CCD district spine + F-33 + EDFacts`
2. `HUD CHAS`
3. `SIPP`
4. `LEHD LODES`
5. `IRS SOI migration`
6. `SAFMR`
7. `AHS`
8. `ORR`
9. `BEA RPP + FHFA HPI`
10. `SAIPE`

## What not to do

1. Do not chase proprietary traffic feeds first.
2. Do not chase state Medicaid claims microdata first.
3. Do not expand the warehouse laterally before fixing the core incidence holes.

Those may matter later, but they are not the fastest path to a materially truer answer.
