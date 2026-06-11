# Dataset fusion matrix for immigration incidence work

Date: 2026-04-10

| Priority | Dataset | Channel | Grain | Join spine | Why it matters | Main caveat | Source |
|---|---|---|---|---|---|---|---|
| P0 | NCES CCD district spine | School | District | `state_fips`, `nces_leaid`, geography crosswalk | Needed to move from state school averages to district-level burden. | Requires district/PUMA geography bridge. | https://nces.ed.gov/ccd/pubageninfo.asp |
| P0 | NCES F-33 district finance | School | District-year | `nces_leaid` | Gives district revenue, expenditure, and per-pupil finance. | Finance only; no ELL composition. | https://nces.ed.gov/ccd/f33agency.asp |
| P0 | EDFacts / CCD special populations | School | District-year | `nces_leaid` | Adds English learner and migrant-student structure. | Field availability varies by year. | https://www.ed.gov/data/edfacts-initiative |
| P1 | Census SAIPE school districts | School | District-year | district crosswalk | Adds child poverty and ages `5-17` context for district burden sizing. | ID cleanup may be annoying. | https://www.census.gov/programs-surveys/saipe/technical-documentation/methodology/school-districts/overview-school-district.html |
| P0 | HUD CHAS | Housing | Tract/county/place | `geoid` | Measures overcrowding and cost burden directly. | Multi-year lag; not person-level. | https://www.huduser.gov/portal/datasets/cp.html |
| P1 | HUD SAFMR / FMR | Housing | ZIP-year / metro-year | `zip`, `county_fips`, `metro_area` | Improves subcounty rent surface. | Payment standard, not market-clearing rent. | https://www.huduser.gov/portal/datasets/fmr/smallarea/index.html |
| P1 | American Housing Survey | Housing | National + selected metros | metro code | Adds doubling-up, unit quality, tenure, and mobility. | Metro-only for local detail. | https://www.census.gov/programs-surveys/ahs.html |
| P0 | LEHD LODES | Transport | Block OD / aggregated | geocodes + PUMA crosswalk | Replaces average commute proxies with actual commuting flows. | Covered employment only. | https://lehd.ces.census.gov/data/#lodes |
| P1 | BEA RPP + FHFA HPI | Cost surface | State/metro + county/MSA | `state_fips`, `county_fips`, `msa_code` | Separates cost level from price appreciation. | Composite fusion, not one native table. | https://www.bea.gov/data/prices-inflation/regional-price-parities-state-and-metro-area |
| P1 | IRS SOI migration | Adjustment margins | State/county OD | `state_fips`, `county_fips` | Observes relocation responses directly. | Misses some non-filers. | https://www.irs.gov/statistics/soi-tax-stats-migration-data |
| P0 | SIPP | Federal tax/transfer | Household/person microdata | calibration cells | Best public-use base for first serious federal microsimulation. | Weak local geography. | https://www.census.gov/programs-surveys/sipp.html |
| P1 | ORR refugee arrivals + ASR | Admission channel | State-by-origin flow + survey | `state`, `origin`, `year` | Splits refugee-like from labor-migrant origin effects. | Only humanitarian-related flows. | https://acf.gov/archive/orr/data/refugee-arrival-data |
