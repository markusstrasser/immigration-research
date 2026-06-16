# Immigration glossary

## Geography and identifiers

`PUMA`
: Public Use Microdata Area. A Census geography used in ACS microdata. It is large enough to preserve privacy, so it is coarser than tract or district geography. It is the finest consistent geography available in public ACS person records for this project.

`County`
: Standard local administrative geography. Counties are the clean bridge for school finance, HUD CHAS housing stress, IRS migration flows, and many labor or demographic controls.

`CBSA`
: Core-Based Statistical Area. Roughly a metro or micropolitan labor-market geography defined by OMB. Useful for metro analysis, but not directly available as a clean public-use join key in the ACS microdata we are using.

`Census tract`
: Small neighborhood-scale Census geography. Better than PUMA for local precision, but public-use ACS person files do not expose tract IDs.

`FIPS`
: Federal Information Processing Standards code. Short numeric code for states and counties. For counties, the common join key is 5 digits: state 2-digit FIPS plus county 3-digit FIPS.

`GEOID`
: Census concatenated identifier for a geography. Often just the FIPS code in string form for counties and states.

## Core datasets

`ACS`
: American Community Survey. Census survey used for demographic, education, household, income, insurance, commuting, and housing variables.

`PUMS`
: Public Use Microdata Sample. The person- and household-level ACS microdata, rather than pre-aggregated tables.

`ACS tables`
: Pre-aggregated Census outputs like `B05006`. Easier to interpret, less flexible than microdata.

`SIPP`
: Survey of Income and Program Participation. Richer federal-program and income dynamics dataset than ACS, but more complex. Useful for transfer/tax microsimulation if handled carefully.

`CHAS`
: Comprehensive Housing Affordability Strategy data from HUD. County/state/tract tables on housing cost burden, overcrowding, plumbing/kitchen issues, and other housing stress measures.

`CHAS Table 11`
: Table used here for `1 or more of the 4 housing problems`. This is a broader housing-stress measure than just rent level.

`HAMFI`
: HUD Area Median Family Income benchmark used inside CHAS income buckets.

`IRS migration`
: IRS Statistics of Income county/state migration tables based on address changes in tax returns. Good for broad mobility balance context, not a direct immigrant count.

`IRS SOI`
: IRS Statistics of Income more broadly. Includes migration and other tax-base related files.

`LEHD`
: Longitudinal Employer-Household Dynamics. Useful for workplace and residence flows, labor geography, and local labor-market structure.

`LODES`
: LEHD Origin-Destination Employment Statistics. Public workplace/residence flow extracts.

`QCEW`
: Quarterly Census of Employment and Wages. High-value county/industry employment and wage source from BLS.

`FHFA HPI`
: Federal Housing Finance Agency house price index. House-price context, not the same thing as renter welfare.

`OHSS`
: DHS Office of Homeland Security Statistics data products. Useful for legal admissions composition, such as LPR or refugee-related flows.

`LPR`
: Lawful Permanent Resident. A legal-status category, not a skill category.

## Analytical terms

`Low-skill`
: In this project, usually proxied as low educational attainment in ACS, such as less than college. It is a practical proxy, not a deep statement about ability or productivity.

`Recent immigrant`
: Usually proxied from ACS year-of-entry variables. The exact cut matters because local burden and fiscal contribution change with time since arrival.

`Origin`
: Birthplace or sending-country category, often derived from `POBP` in ACS and joined to World Bank or UN country ontologies.

`Incidence`
: Who gains and who loses. The same immigration flow can help employers and consumers while hurting local budgets or directly competing workers.

`Federal incidence`
: Effects on federal taxes and transfers.

`State/local incidence`
: Effects on state and municipal budgets, schools, housing pressure, transit, and other local systems.

`Household-normalized child burden`
: A correction for the fact that multiple adults in one household can otherwise cause the same children to be counted more than once. This project now uses household-normalized school-age burden rather than the earlier bad proxy.

`School-age burden`
: Usually children ages `5-17` linked to qualifying households, normalized carefully.

`Housing stress`
: Broad local housing strain, not just price level. In the CHAS layer this includes cost burden and non-price housing problems.

`Area-weighted crosswalk`
: A geographic bridge where a PUMA is split across counties by land area share. It is weaker than a population-weighted bridge, but honest when no direct population crosswalk is available.

`PUMA-to-county area share`
: The proportion of a PUMA’s land area overlapping a county. Used here to build county-context proxies for each PUMA.

`Weighted count`
: Survey-weighted estimate rather than raw row count.

`PWGTP`
: ACS person weight.

`WGTP`
: ACS household weight.

## Interpretation warnings

`Average citizen`
: A framing-sensitive phrase. It can hide big differences across workers, renters, homeowners, taxpayers, and local governments.

`Bad for a country`
: Too coarse on its own. The question should be split by horizon, geography, incidence group, and counterfactual.

`AGI soon`
: A major scenario assumption. If true, it can reduce the long-run importance of some wage effects and increase the importance of short-run transition costs, political economy, care bottlenecks, and automation complementarity.
