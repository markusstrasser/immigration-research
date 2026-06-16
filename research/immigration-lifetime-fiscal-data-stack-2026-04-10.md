# Data stack for building our own lifetime fiscal-impact model

Date: 2026-04-10

## Question

What data do we need to replace coarse benchmark lifetime fiscal estimates with our own model for immigration, especially low-education cases?

## Short answer

We cannot get there from `ACS` alone.

A real lifetime fiscal model needs four distinct layers:

1. `current composition` — who the households are now
2. `earnings/tax trajectories` — how earnings and tax payments evolve over time
3. `program receipt / health spending` — transfers and public-cost exposure over time
4. `descendants / family transitions / attrition` — children, marriage, return migration, mortality

The minimum viable public stack is:

1. `ACS PUMS` for current composition and local context
2. `SIPP` for monthly program participation and household transitions
3. `Synthetic SIPP` for public-use admin-linked earnings history proxies
4. `MEPS HC` for medical spending and payer incidence
5. `PSID` for long-run earnings and intergenerational dynamics
6. `IRS SOI PUF` or tax-calculator-compatible public tax files for federal tax mapping

The gold-standard stack requires restricted access:

1. linked `SIPP-SSA-IRS` data in an `FSRDC` or equivalent restricted environment
2. `LEHD` or SSA earnings histories for labor-market trajectories
3. restricted health or administrative benefit files if we want credible late-life cost paths

## Main conclusion

The right question is not "where is the one file?" There is no one file. The data have to be fused across public survey, administrative, and longitudinal sources.

## Evidence and source grades

### A1 sources: official dataset pages and documentation

1. `SIPP` is a longitudinal survey designed for income, employment, household composition, and program participation. [A1]
   [SOURCE: https://www.census.gov/programs-surveys/sipp.html]
2. `SIPP datasets` are publicly released by year, including `2024 SIPP data` covering calendar year `2023`. [A1]
   [SOURCE: https://www.census.gov/programs-surveys/sipp/data/datasets.html]
3. The `2024 SIPP Users Guide` says public-use files strip out the administrative records, but the imputation process uses SSA/IRS records such as `Detailed Earnings Record (DER)` and benefit records. [A1]
   [SOURCE: https://www2.census.gov/programs-surveys/sipp/tech-documentation/methodology/2024_SIPP_Users_Guide.pdf]
4. `Synthetic SIPP` is public-use and links SIPP respondents to SSA/IRS `W-2` and SSA benefit records in a privacy-protected synthetic product. [A1]
   [SOURCE: https://www.census.gov/programs-surveys/sipp/guidance/sipp-synthetic-beta-data-product.html]
5. `MEPS Household Component` collects health-care use, charges, payments, insurance coverage, income, and employment. [A1]
   [SOURCE: https://meps.ahrq.gov/survey_comp/household.jsp]
6. `MEPS` public-use data file types are available, but some NHIS-linked files are only available through secure data centers. [A1]
   [SOURCE: https://meps.ahrq.gov/mepsweb/data_stats/more_info_download_data_files.jsp]
7. `PSID` is the longest-running household longitudinal panel and is explicitly intergenerational. [A1]
   [SOURCE: https://psidonline.isr.umich.edu/]
8. `IRS SOI` provides public-use microdata files for individual returns, though they are altered and incomplete for some tax-liability reconstruction. [A1]
   [SOURCE: https://www.irs.gov/statistics/soi-tax-stats-individual-public-use-microdata-files]
9. The IRS also documents that the public-use file does not contain all fields needed to calculate tax liability exactly, so some inference is unavoidable. [A1]
   [SOURCE: https://www.irs.gov/pub/irs-soi/06resconf.pdf]
10. `LEHD` is restricted-use and accessed through `FSRDCs`; it covers linked employer-employee data and uses administrative sources including SSA-linked demographics. [A1]
   [SOURCE: https://www.census.gov/data/datasets/time-series/adrm/ces-restricted-lehd.html]
11. Census documentation confirms that many administrative-linkage inventories are restricted, even when they inform public-use products. [A1]
   [SOURCE: https://www2.census.gov/library/working-papers/2024/demo/sehsd-wp2024-01.pdf]
   [SOURCE: https://www2.census.gov/about/linkage/data-file-inventory.pdf]

### B1/B2 sources: established microsimulation and modeling context

1. `TRIM3` is a long-running Urban microsimulation built primarily on CPS ASEC and used for taxes and transfer analysis, including immigration-related benefit/tax analysis. [B1/B2]
   [SOURCE: https://www.urban.org/research/data-methods/data-analysis/quantitative-data-analysis/microsimulation/transfer-income-model-trim]
2. Urban and other modelers have used microsimulation for immigrant fiscal and tax analysis, but those are models, not raw datasets. [B2]
   [SOURCE: https://www.urban.org/sites/default/files/publication/24146/412944-understanding-the-economic-and-fiscal-impacts-of-immigration-reform.pdf]

## What each dataset actually solves

### 1. ACS PUMS

What it gives us:

1. origin mix
2. education
3. age
4. destination geography
5. current household structure
6. wages/income proxies
7. insurance and public-assistance proxies

What it does **not** give us:

1. lifetime tax trajectories
2. clean monthly benefit histories
3. descendants tracked over long horizons
4. undocumented status

Current local file:
1. [csv_pus.csv](/Volumes/SSK1TB/corpus/census_acs/csv_pus.csv)

Judgment:
1. necessary but not sufficient

### 2. SIPP

What it gives us:

1. monthly program participation
2. household composition changes
3. employment dynamics
4. poverty spells
5. detailed benefit receipt categories
6. short longitudinal panel structure

Why it matters:
1. this is the public survey best aligned to transfer-incidence modeling
2. it is far better than ACS for welfare/program use over time

Limit:
1. panel is still too short for a full lifetime model by itself

Official source:
1. [SIPP main page](https://www.census.gov/programs-surveys/sipp.html)
2. [SIPP datasets](https://www.census.gov/programs-surveys/sipp/data/datasets.html)

### 3. Synthetic SIPP

What it gives us:

1. public-use proxy for linked SSA/IRS earnings and benefits history
2. administrative-history flavor without entering a restricted environment

Why it matters:
1. this is the single most promising public-use upgrade over plain SIPP for lifetime earnings/tax trajectory estimation

Limit:
1. it is synthetic, not raw admin truth
2. undocumented-status inference remains weak

Official source:
1. [Synthetic SIPP beta product](https://www.census.gov/programs-surveys/sipp/guidance/sipp-synthetic-beta-data-product.html)

### 4. MEPS Household Component

What it gives us:

1. medical use
2. expenditure levels
3. source of payment
4. insurance
5. employment and income context

Why it matters:
1. one of the hardest parts of lifetime fiscal modeling is health-cost incidence
2. ACS and SIPP are much weaker here than MEPS

Limit:
1. it is not an immigrant-status panel by itself
2. some useful links are restricted

Official source:
1. [MEPS Household Component overview](https://meps.ahrq.gov/survey_comp/household.jsp)
2. [MEPS file types](https://meps.ahrq.gov/mepsweb/data_stats/more_info_download_data_files.jsp)

### 5. PSID

What it gives us:

1. long-run household earnings trajectories
2. intergenerational links
3. descendants and family transitions
4. wealth and long-run outcomes

Why it matters:
1. this is the best public-use source for descendant modeling and long-run earnings mobility

Limit:
1. immigrant-origin granularity is weaker than ACS
2. undocumented-status identification is poor
3. it is not a pure tax/benefit panel

Official source:
1. [PSID home](https://psidonline.isr.umich.edu/)

### 6. IRS SOI Public-Use File

What it gives us:

1. tax-return microdata structure
2. federal-tax mapping backbone
3. calibration target for tax microsimulation

Why it matters:
1. if we want our own federal tax liability engine, this is the closest public-use anchor

Limit:
1. altered for confidentiality
2. not all liability-driving fields are available
3. not linked to immigration status or descendants directly

Official source:
1. [IRS SOI PUF](https://www.irs.gov/statistics/soi-tax-stats-individual-public-use-microdata-files)
2. [IRS note on missing fields](https://www.irs.gov/pub/irs-soi/06resconf.pdf)

### 7. Restricted linked data: SIPP-SSA-IRS, LEHD, FSRDC

What it gives us:

1. real earnings histories
2. stronger tax and benefit trajectories
3. much better labor-market path modeling
4. a serious chance at replacing NAS rather than just refining it

Why it matters:
1. this is the level where a debiased lifetime fiscal model becomes genuinely credible

Limit:
1. restricted access
2. project approval required
3. slower workflow

Official sources:
1. [LEHD restricted data](https://www.census.gov/data/datasets/time-series/adrm/ces-restricted-lehd.html)
2. [Census linkage inventory](https://www2.census.gov/about/linkage/data-file-inventory.pdf)
3. [SIPP research file working paper](https://www2.census.gov/library/working-papers/2024/demo/sehsd-wp2024-01.pdf)

## What data are needed for each model component

| Model component | Public option | Better option | Status |
|---|---|---|---|
| Current composition | ACS PUMS | ACS + admin linkage | Already strong |
| Monthly transfer use | SIPP | linked SIPP admin records | Public path exists |
| Federal taxes | IRS SOI PUF + tax model | IRS-linked restricted microdata | Public path partial |
| Medical/public health cost | MEPS | restricted MEPS/NHIS link / admin | Public path partial |
| Earnings trajectory | PSID + Synthetic SIPP | SIPP-SSA/IRS + LEHD | Public path weak; restricted path strong |
| Descendants/intergenerational mobility | PSID | linked admin-child data | Public path partial |
| Undocumented status | residual inference only | restricted admin / model-based proxy | weak either way |
| Return migration | ACS/SIPP indirect inference | admin linkage / better panel | currently weak |

## What we can build now without restricted access

### Public MVP

We can build a materially better-than-NAS model now if we accept that it is still not the final word.

Stack:

1. `ACS` for current immigrant composition by origin/destination/household
2. `SIPP` for monthly safety-net and household-transition dynamics
3. `Synthetic SIPP` for admin-like earnings histories in public use
4. `MEPS` for age/insurance/medical-spending profiles
5. `PSID` for long-run descendant and earnings transition parameters
6. `IRS SOI PUF` or a tax-calculator-compatible public tax file for federal liability mapping

This would let us estimate:

1. federal taxes paid over stylized lifetime paths
2. transfer use over stylized household paths
3. health-cost profiles by age and insurance status
4. descendant burden/benefit with a real intergenerational source

But it would still be weak on:

1. undocumented identification
2. exact local public-service burden
3. return migration

## What we need if we want to actually beat NAS

### Gold-standard path

1. `FSRDC` access
2. restricted `SIPP-SSA-IRS` linked records
3. restricted `LEHD` or equivalent earnings panel
4. restricted or stronger health-utilization linkage
5. public ACS local-context warehouse as the incidence layer on top

That is the path to a genuinely debiased replacement, not just a refined public approximation.

## Acquisition strategy

### Acquire now

1. `Synthetic SIPP`
2. latest `SIPP` public files and codebooks
3. `MEPS HC` public-use files and documentation
4. `PSID` public documentation and access setup
5. `IRS SOI PUF` access materials

### Do not waste time on right now

1. trying to infer lifetime federal tax incidence from ACS alone
2. trying to infer undocumented status directly from public-use survey data as if it were observed
3. pretending CPS/ACS current cross-sections solve descendants or late-life spending

### If we escalate

1. draft an `FSRDC` project concept note
2. specify exact linked datasets needed
3. justify why public-use files are insufficient

## Bottom line

To replace NAS for lifetime fiscal impacts, the most important public-use addition is not another ACS table. It is:

1. `SIPP`
2. `Synthetic SIPP`
3. `MEPS`
4. `PSID`
5. `IRS SOI PUF`

If we want a truly serious replacement model rather than a refined approximation, the answer is restricted linked data through `FSRDC`, especially `SIPP-SSA-IRS` and `LEHD`.
