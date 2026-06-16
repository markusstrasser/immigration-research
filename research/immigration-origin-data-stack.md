# Immigration origin analysis: datasets, ontologies, and paper stack

Date: 2026-04-10

## Purpose

This note defines the minimum public-data stack needed to make serious statements about low-skill immigration by origin mix and destination, without using ad hoc exclusions such as "not Japan" or "not the EU." The correct object is not "low-skill immigration" in the abstract. It is low-skill immigration from specific origins into specific destinations with specific household structures. [INFERENCE]

## What we already have locally

### Person-level stock data

1. ACS PUMS person file: [csv_pus.csv](/Volumes/SSK1TB/corpus/census_acs/csv_pus.csv)
2. CPS public-use file: `/Volumes/SSK1TB/corpus/census_cps/jan24pub.csv`

### Local context data already ingested

1. FHFA state purchase-only HPI: [fhfa_hpi_po_state.txt](/Users/alien/Projects/research/sources/immigration-fiscal/data/external/fhfa_hpi_po_state.txt)
2. Census 2023 school-finance summary rows: [census_school_finance_2023_summary.txt](/Users/alien/Projects/research/sources/immigration-fiscal/data/external/census_school_finance_2023_summary.txt)
3. Derived DuckDB warehouse: [immigration_context.duckdb](/Users/alien/Projects/research/sources/immigration-fiscal/data/derived/immigration_context.duckdb)
4. DuckDB build script: [build_immigration_context_duckdb.sql](/Users/alien/Projects/research/sources/immigration-fiscal/data/derived/build_immigration_context_duckdb.sql)

## New origin-layer datasets acquired in this pass

### Official and machine-readable

1. World Bank country metadata API dump: [worldbank_country_metadata.json](/Users/alien/Projects/research/sources/immigration-fiscal/data/external/origin/worldbank_country_metadata.json)
   What it gives:
   country name, ISO2/ISO3, World Bank region, income group, lending type, capital city.
   Source: `https://api.worldbank.org/v2/country?format=json&per_page=400`

2. ACS 2023 table `B05006` metadata: [census_acs1_2023_B05006_metadata.json](/Users/alien/Projects/research/sources/immigration-fiscal/data/external/origin/census_acs1_2023_B05006_metadata.json)
   What it gives:
   labeled place-of-birth categories for the foreign-born population.
   Source: `https://api.census.gov/data/2023/acs/acs1/groups/B05006.json`

3. ACS 2023 table `B05006` state-level data: [census_acs1_2023_B05006_state_origin.json](/Users/alien/Projects/research/sources/immigration-fiscal/data/external/origin/census_acs1_2023_B05006_state_origin.json)
   What it gives:
   state-by-origin counts for the foreign-born population, with Census labels available through the metadata file.
   Source: `https://api.census.gov/data/2023/acs/acs1?get=NAME,group(B05006)&for=state:*`

4. ACS 2023 subject definitions PDF: [census_2023_subject_definitions.pdf](/Users/alien/Projects/research/sources/immigration-fiscal/data/external/origin/census_2023_subject_definitions.pdf)
   What it gives:
   official ACS variable definitions and coding guidance.
   Source: `https://www2.census.gov/programs-surveys/acs/tech_docs/subject_definitions/2023_ACSSubjectDefinitions.pdf`

5. OHSS LPR recent-arrivals CBSA workbook: [ohss_lpr_recent_arrivals_cbsa_2024.xlsx](/Users/alien/Projects/research/sources/immigration-fiscal/data/external/origin/ohss_lpr_recent_arrivals_cbsa_2024.xlsx)
   What it gives:
   lawful permanent resident estimates for recent arrivals among top 50 CBSAs by county.
   Source page: `https://ohss.dhs.gov/topics/immigration/population-estimates/lawful-permanent-residents`
   Direct file path used: `https://ohss.dhs.gov/sites/default/files/2024-12/2024_1206_ohss_lpr-and-eligible-to-naturalize-jan-01-2024.xlsx`

6. ACS PUMS code-list workbook: [ACSPUMS2019_2023CodeLists.xlsx](/Users/alien/Projects/research/sources/immigration-fiscal/data/external/origin/ACSPUMS2019_2023CodeLists.xlsx)
   What it gives:
   official `POBP` birthplace codes and descriptions needed to decode the ACS person file.
   Source: `https://www2.census.gov/programs-surveys/acs/tech_docs/pums/code_lists/ACSPUMS2019_2023CodeLists.xlsx`

7. OHSS country-by-major-class workbook: [lpr_country_birth_major_class_2005_2022.xlsx](/Users/alien/Projects/research/sources/immigration-fiscal/data/external/origin/ohss/lpr_country_birth_major_class_2005_2022.xlsx)
   What it gives:
   administrative lawful-permanent-resident admissions by country of birth, major class, and fiscal year.
   Source: `https://ohss.dhs.gov/sites/default/files/2023-12/plcy_lpr_by_country_of_birth_by_major_class_fy2005-2022_d.xlsx`

8. OHSS top-200 counties workbook: [lpr_counties_top_200_fy2022.xlsx](/Users/alien/Projects/research/sources/immigration-fiscal/data/external/origin/ohss/lpr_counties_top_200_fy2022.xlsx)
   What it gives:
   county-level administrative admissions by country and major class for the top 200 counties in FY2022.
   Source: `https://ohss.dhs.gov/sites/default/files/2023-12/plcy_lpr_counties_top_200_fy2022_d.xlsx`

9. ACS 2023 state median gross rent JSON: [census_acs1_2023_state_median_gross_rent.json](/Users/alien/Projects/research/sources/immigration-fiscal/data/external/origin/census_acs1_2023_state_median_gross_rent.json)
   What it gives:
   official renter-side housing cost by state.
   Source: `https://api.census.gov/data/2023/acs/acs1?get=NAME,B25064_001E&for=state:*`

### Acquired paper layer

1. Colas and Sachs paper PDF: [colas_sachs_indirect_fiscal_benefits.pdf](/Users/alien/Projects/research/sources/immigration-fiscal/data/external/origin/colas_sachs_indirect_fiscal_benefits.pdf)
   Source: `https://www.econstor.eu/bitstream/10419/282044/1/352.pdf`

## Official sources identified but not cleanly downloaded yet

1. CBO 2025 state/local immigration report
   Canonical URL: `https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf`
   Status:
   direct `curl` returned an HTML trap, not a PDF.
   Use the canonical URL as source for now.

2. OHSS LPR pages for:
   `LPRs by State, County, Country, and Major Class of Admission`
   `LPRs by Country of Birth and Major Classes of Admission`
   Status:
   page-level evidence is clear, but I have not yet extracted the exact direct file URLs for those specific workbooks.
   Source page: `https://ohss.dhs.gov/topics/immigration/population-estimates/lawful-permanent-residents`

3. UN M49 country/region ontology
   Source page: `https://unstats.un.org/unsd/methodology/m49/overview/`
   Status:
   HTML table is accessible and machine-parseable. This pass materializes it into the derived layer rather than storing a raw download file.

## Executed outputs

The plan has now been executed into both flat derived assets and the existing DuckDB warehouse.

### Derived flat assets

Created by [build_origin_assets.py](/Users/alien/Projects/research/sources/immigration-fiscal/data/derived/build_origin_assets.py):

1. [country_origin_dim.csv](/Users/alien/Projects/research/sources/immigration-fiscal/data/derived/origin/country_origin_dim.csv)
2. [worldbank_country_dim.csv](/Users/alien/Projects/research/sources/immigration-fiscal/data/derived/origin/worldbank_country_dim.csv)
3. [un_m49_country_dim.csv](/Users/alien/Projects/research/sources/immigration-fiscal/data/derived/origin/un_m49_country_dim.csv)
4. [state_origin_stock_2023.csv](/Users/alien/Projects/research/sources/immigration-fiscal/data/derived/origin/state_origin_stock_2023.csv)
5. [state_median_gross_rent_2023.csv](/Users/alien/Projects/research/sources/immigration-fiscal/data/derived/origin/state_median_gross_rent_2023.csv)
6. [ohss_lpr_country_birth_major_class_2005_2022.csv](/Users/alien/Projects/research/sources/immigration-fiscal/data/derived/origin/ohss_lpr_country_birth_major_class_2005_2022.csv)
7. [ohss_lpr_counties_top_200_fy2022.csv](/Users/alien/Projects/research/sources/immigration-fiscal/data/derived/origin/ohss_lpr_counties_top_200_fy2022.csv)

### DuckDB extension

Created by [extend_immigration_context_with_origins.sql](/Users/alien/Projects/research/sources/immigration-fiscal/data/derived/extend_immigration_context_with_origins.sql) inside [immigration_context.duckdb](/Users/alien/Projects/research/sources/immigration-fiscal/data/derived/immigration_context.duckdb):

1. `country_origin_dim`
2. `worldbank_country_dim`
3. `un_m49_country_dim`
4. `state_origin_stock_2023`
5. `state_median_gross_rent_2023`
6. `ohss_lpr_country_birth_major_class_2005_2022`
7. `ohss_lpr_counties_top_200_fy2022`
8. `acs_origin_state_2023`
9. `acs_origin_national_2023`
10. `ohss_country_major_class_2022`
11. `origin_destination_context_2023`

## Epistemic guardrails from the executed build

1. `POBP` is now officially decoded through the ACS code-list workbook rather than inferred from values.
2. Historical or aggregate birthplace labels such as `USSR`, `Yugoslavia`, `Europe`, and `Korea` are intentionally left unmatched or only broadly classified. That is a feature, not a bug. Overmatching these would create fake origin precision.
3. Renter-side housing is represented with ACS state median gross rent. That is cleaner than forcing county FMR data into a state average without a defensible weighting rule.
4. OHSS county data is useful but not fully joinable to the current state-level warehouse. The directly joinable OHSS layer is country-by-major-class, not county incidence.
5. The CBO 2025 report remains a canonical source but the direct PDF URL returned an HTML trap to `curl`. Use the CBO page URL as the source of record.

## Datasets we should add next

### High priority

1. OHSS LPR by country/state/class workbook
   Why:
   administrative legal-status composition by origin, separate from ACS stock counts.

2. UN M49 local extract
   Why:
   region and subregion ontology without hand-built groupings.

3. HUD Fair Market Rent or other rent index
   Why:
   FHFA captures ownership-side housing values; we still need renter pressure.

4. CBP nationality data or other recent border-arrival administrative data
   Why:
   better handle on recent flow composition by origin and legal channel.

5. SIPP household transfer data
   Why:
   better household-level benefit incidence than ACS alone.

### Lower priority

1. BLS LAUS or alternative labor-market context
   Why:
   destination labor-market slack.
   Status:
   public flat files returned HTML traps to plain `curl`, so this needs a better acquisition path.

2. NCES / EDFacts English learner counts
   Why:
   school-system language burden, though ACS `ENG` and `LANP` already provide a partial measure.

## Ontology stack

To avoid arbitrary region exclusions, impose these layers:

### Layer 1: official birthplace ontology

Use ACS `POBP` and ACS table `B05006` labels as the canonical origin vocabulary. [SOURCE: Census ACS API and subject definitions]

### Layer 2: official country context ontology

Join origins to:

1. World Bank region
2. World Bank income group
3. UN M49 region and subregion

This gives a non-ad hoc regional and development classification. [SOURCE: World Bank API; UN M49 page]

### Layer 3: empirical selection ontology

Create a derived classification from observed U.S. data:

1. college share among recent immigrants from origin `o`
2. median wage among recent immigrants from origin `o`
3. child intensity among households from origin `o`
4. Medicaid/public-assistance incidence among recent low-skill adults from origin `o`

This is the right way to define `low-selection origin` if the policy question is really about likely fiscal and local-incidence pressure. [INFERENCE]

### Layer 4: destination-cost ontology

For each state or metro, assign:

1. housing-cost regime
2. school-cost regime
3. transit/congestion regime
4. renter-vs-homeowner incidence profile

This prevents the false move of treating an immigrant in Texas and an immigrant in Massachusetts as fiscally interchangeable. [INFERENCE]

## What each data layer enables

| Layer | Dataset | Join key | What it lets us say |
|---|---|---|---|
| Person microdata | ACS PUMS | `STATE`, `POBP`, `SERIALNO` | Education, income, commute, household structure, children, benefits, years since entry |
| Aggregate validation | ACS `B05006` | `state`, labeled origin columns | State-by-origin stock validation with official labels |
| Origin ontology | World Bank metadata | ISO3 / country name | Region and income-group classification |
| Legal/admin composition | OHSS LPR files | country, state, CBSA, admission class | Legal-status and admission-channel mix |
| Housing cost | FHFA HPI + future rent series | state or metro | Ownership-side and renter-side local pressure |
| School burden | Census school finance + ACS children/language | state, district, household | Education-cost exposure and ELL-related pressure |

## Paper stack that actually changes the modeling

### High-value papers and reports

1. Colas and Sachs, *The Indirect Fiscal Benefits of Low-Skilled Immigration*
   Why it matters:
   adds a missing indirect fiscal channel through resident wages and labor supply.
   Source: `https://www.econstor.eu/bitstream/10419/282044/1/352.pdf`

2. CBO, *Effects of the Surge in Immigration on State and Local Budgets in 2023*
   Why it matters:
   clean recent official treatment of state/local tax revenue, spending, and crowding effects.
   Source: `https://www.cbo.gov/publication/61256`

3. Brookings 2026 immigration-flow update
   Why it matters:
   explicit warning not to infer foreign-born population levels from CPS because of fixed population controls.
   Source: `https://www.brookings.edu/articles/macroeconomic-implications-of-immigration-flows-in-2025-and-2026-january-2026-update/`

4. Vigdor, Bier, and Howard, *Immigrants, Housing Wealth, and Local Government Finances*
   Why it matters:
   forces the housing/property-tax capitalization channel into the local fiscal ledger.
   Source: `https://www.cato.org/briefing-paper/immigrants-housing-wealth-local-government-finances`

5. Clemens, *The Fiscal Effect of Immigration: Reducing Bias in Influential Estimates*
   Why it matters:
   sharp critique of cashflow accounting that ignores capital-tax incidence.
   Source: `https://www.iza.org/publications/dp/15592/the-fiscal-effect-of-immigration-reducing-bias-in-influential-estimates`

### Still useful but secondary

1. Abramitzky et al. on children of immigrants
2. Duncan and Trejo on slower convergence for some Hispanic-origin groups
3. Saiz on housing rents/prices
4. Dustmann and Frattini on fiscal accounting in a different institutional setting

## What we can say after this stack is joined

Not yet fully estimated, but the stack is sufficient to support statements like:

1. which origin groups have the lowest direct fiscal capacity in the U.S. sample,
2. which origin groups have the highest household child intensity,
3. which origin groups are disproportionately concentrated in high school-cost or high housing-cost states,
4. whether a given origin group is primarily a federal revenue positive but state/local cost negative,
5. whether broad labels like `South Asian` hide major within-region differences.

## What we should not say yet

1. any blanket claim about "Asian" or "European" immigrants as a whole,
2. any origin-specific causal claim about wages, rents, or school crowding without a panel design,
3. any statement that uses CPS to infer recent immigrant population levels,
4. any statement that treats state and local incidence as interchangeable with federal incidence.

## Recommended next build

1. Materialize a `country_origin_dim` table from World Bank metadata plus UN M49.
2. Build a `state_origin_stock_2023` table from ACS `B05006`.
3. Extend the current DuckDB with an `acs_origin_state_2023` summary using `POBP`, `SERIALNO`, and child counts.
4. Add renter-side housing data.
5. Add OHSS legal-status / admission-channel composition where possible.

That is the minimum credible stack for saying anything sharper than slogans.
