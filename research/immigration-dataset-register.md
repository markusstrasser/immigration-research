# Immigration — Dataset Register

This is the project's register of the data it holds: what each dataset is for, where the local copy lives, and what
it can and cannot answer. Everything in the domain sections is on this machine unless its row says otherwise. Data we
do not hold, lost files and open leads are under [Not held](#not-held). Byte counts and hashes of the core raw files
are in `sources/immigration-fiscal/data/MANIFEST.md`, which sits in the ignored `sources/` tree, and in each lane's
manifest. Official acquisition routes, pins and normalization are in
[REPRODUCTION_INPUTS](../infra/immigration-fiscal/REPRODUCTION_INPUTS.md).

Each domain section lists the core files first. Under "In analysis lanes" it then lists the source files an analysis
lane downloaded into its own ignored `_cache/` or `raw/` folder; that lane's RESULT or README gives the acquisition
route and limits.

Sections: [first stops](#first-stops-by-question) · [storage](#storage-and-reproduction) ·
[warehouses](#warehouses-and-derived-layers) · [population and income surveys](#population-and-income-surveys) ·
[health and care](#health-and-care) · [public finance and tax](#public-finance-and-tax) · [schools](#schools) ·
[housing, labor and local economy](#housing-labor-and-local-economy) ·
[migration, origin and admissions](#migration-origin-and-admissions) ·
[custody, crime and enforcement](#custody-crime-and-enforcement) ·
[transport, environment and safety](#transport-environment-and-safety) ·
[identity, family history and attitudes](#identity-family-history-and-attitudes) · [international](#international) ·
[replication packages and papers](#replication-packages-and-papers) · [not held](#not-held) ·
[do not use without checking](#do-not-use-without-checking) · [revisions](#revisions)

## First stops by question

1. **Do we hold X?** Search this file. For anything it does not list, run
   `rg --files --no-ignore sources infra | rg -i <name>`: raw pulls sit in ignored folders.
2. **Can I query it now?** The unified `warehouse/immigration.duckdb` holds the context, lifetime and fiscal tables,
   schema-qualified; `SELECT * FROM _catalog` lists them. Rebuild it with `reproduce.sh build unified`.
3. **What do the data show?** The [topic index](immigration-INDEX.md) for current results; the
   [objections FAQ](immigration-objections-faq-2026-09-21.md) for "what about X?".
4. **How do I fetch a file again?** [REPRODUCTION_INPUTS](../infra/immigration-fiscal/REPRODUCTION_INPUTS.md),
   `infra/immigration-fiscal/REPRODUCE.md` and the lane's own manifest.
5. **Crime, custody or detention cost?** First read the
   [custody/crime measurement rule](immigration-detention-crime-and-fiscal-scope-2026-09-20.md) and the
   [detention spending audit](../infra/immigration-fiscal/detention_reconciliation_2026_09_20/README.md).

## Storage and reproduction

`sources/` is a physical, ignored directory inside this checkout; `~/research-data` is a symlink to it, kept for
saved commands.

- `sources/immigration-fiscal/data/`: raw fiscal inputs. Most acquisitions are under `external/`; the March 2026 core
  set is in `census/`, `cbo/`, `itep/`, `irs/`, `ssa/`, `nces/`, `pew/`, `dhs/`, `usaspending/`, `bls/`, `fred/` and
  `usda/`.
- `sources/immigration-fiscal/derived/`: generated tables and DuckDB files. `sources/immigration-fiscal/data/derived`
  is a symlink to it.
- `sources/immigration-causal/data/`: what survives of the causal layer (`cbp/`, `internal_migration/`, `lehd/`).
- `sources/reused-surveys/`: ECLS-K, ECLS-K:2011 and PIAAC.
- `sources/corpus/`: local copies of corpus files (BEA SAINC).
- `.scratch/`: ignored staging from the September 5 repair, still read by the cards that name it.

Analysis lanes keep their own raw pulls in ignored `_cache/` or `raw/` folders under
`infra/immigration-fiscal/<lane>/`, with tracked manifests or source records.

The external SSD `/Volumes/2TBPNY` holds the shared snapshot corpus (`corpus/`) and a frozen backup of the raw and
derived trees as of 2026-09-16 (`research-data/`). It is not mounted by default, and no current result needs it. The
EOIR case data of February 2026 and the LEHD LODES files exist only there.

```bash
./scripts/reproduce-immigration-data.sh init
./scripts/reproduce-immigration-data.sh doctor
./scripts/reproduce-immigration-data.sh all minimal    # ~2 GB → immigration_context.duckdb
./scripts/reproduce-immigration-data.sh all standard   # full public stack
```

The wrapper calls `infra/immigration-fiscal/reproduce.sh`; run it with bash, since it refuses zsh. The guide
`infra/immigration-fiscal/REPRODUCE.md` covers tiers, the manual-acquire list and verify modes. Scripts and manifests:
`infra/immigration-fiscal/acquire/setup.sh` and `DOWNLOAD_MANIFEST.tsv`; `acquire/config.env.example` holds portable
defaults, and the untracked `acquire/config.local.env` holds machine overrides and the Census API key. Key builders:
`build_immigration_warehouse.py`, `build_stage5_local_cost_context.py`, `compose_scenario_ledger.py`. Downloads that
need a login or a browser are listed in four MANUAL_ACQUIRE notes under `sources/immigration-fiscal/data/external/`:
`crime_frontier/MANUAL_ACQUIRE.md` (openICPSR, ICPSR and page-driven crime, mobility and survey files),
`stage5_net_negative/kff_refs/MANUAL_ACQUIRE.md` (KFF, TRAC, NAS, EDFacts), `lifetime/applications/MANUAL_ACQUIRE.md`
and `urban_housing/MANUAL_ACQUIRE.md`.

## Warehouses and derived layers

| Dataset and vintage | Where it is | Use | Limits |
|---|---|---|---|
| Unified warehouse | `warehouse/immigration.duckdb`, last written 2026-09-26 | Schema-qualified `context`, `lifetime` and `fiscal` tables and `_catalog` | Copies keep their source's scope; a query that runs does not make an estimate causal |
| Context warehouse, 71 tables and views | `warehouse/immigration_context.duckdb`; rebuilt 2026-09-16 after the SSD loss, last written 2026-09-26 | State, origin and county context, person-level donor projections, and the crime and origin tables below | Partial descriptive accounting, not a lifetime causal model |
| Lifetime evidence warehouse | `warehouse/immigration_lifetime_evidence.duckdb`, rebuilt 2026-09-16 | Source catalog, unverified extracted claims, unadjudicated proposals, annual and lifetime benchmark tables | No row-level join to papers; units, assumptions and source confidence stay explicit |
| Fiscal union warehouse | `warehouse/immigration_fiscal_union.duckdb`, rebuilt 2026-09-16 | Materialized tensor and scenario tables plus cross-domain views | Rebuild after either parent changes; keep the scenario and unit keys |
| Sweep warehouse | `warehouse/immigration_sweep.duckdb`, June 18 | Nothing: one empty table | The unified build excludes it |
| IPUMS USA person panel | `sources/immigration-fiscal/derived/immigration_microdata.duckdb`, 44,393,133 rows, rebuilt 2026-09-16 | Long-run person panel; foreign-born is `BPL >= 150` | The extract store is described in the IPUMS USA card |
| Warehouse build script | `infra/immigration-fiscal/build/build_immigration_warehouse.py` | Rebuilds core, stage 2 and the federal microsimulation | Stage-2 housing uses CHAS Table 11 when the zip is present, else an ACS PUMA fallback |
| Stage 2 derived tables | `sources/immigration-fiscal/derived/stage2/`: PUMA–county area crosswalk 2023, CHAS county housing stress 2018–2022, county school finance 2023, IRS county migration 2022–23 | County and PUMA bridges for the context warehouse | The crosswalk has 4,701 rows, a county aggregate of 14,856 county-subdivision rows, so the builder's row check (at least 14,000) prints WARN for it |
| Stage 3 prototype tables | `sources/immigration-fiscal/derived/stage3_proto/`, among them the MEPS health-cost module 2023 with its metadata; ACS foreign-born education buckets 2023 (totals and state shares); the SIPP public MVP cells, person donor cells, SIPP→MEPS bridge and expected health-cost cells and the 98-cell scenario ledger, 2024; the origin fiscal scenario 2023 | Inputs to the public MVP scenario engine | Prototypes. The MEPS module is descriptive payer incidence by age × nativity × insurance, not lifetime or legality-specific; the education buckets cover the foreign-born stock aged 25–64; the SIPP cells have no clean legal-status panel |
| Stage 5 derived tables | `sources/immigration-fiscal/derived/stage5/` | The local-cost context layer; see [its table](#stage-5-local-cost-context) | — |
| Stage 6 and tier-A cross-country tables | `sources/immigration-fiscal/derived/stage6/` and `derived/tier_a/` | See [International](#international) | — |
| Origin tables | Context warehouse: `acs_origin_*` (national, PUMA, household, microsim and recipient cells, 2023) and `origin_puma_*_context_2023` | Origin stock, rent and admissions context by PUMA | Stock and administrative layers, not unauthorized status. The April CSV exports under `derived/origin/` no longer exist; these tables replace them |
| `immigrant_assimilation_profile`, 204 cells | Context warehouse; `build_immigrant_assimilation_profile.py`, from IPUMS USA | First-generation employment and conditional log-income profiles by origin region × arrival cohort × census year, 1980–2023 | Descriptive: synthetic cohorts do not remove cohort selection, period effects or selective emigration, so the profiles cannot identify individual assimilation; see the [duration-matched comparison](immigration-cohort-clarity-2026-09-05.md) |
| `msa_rent_elasticity_panel` | Context warehouse; `build_msa_rent_elasticity_panel.py` | Zillow rent and home-value paths × Saiz elasticity, January 2016–December 2025 | The first-city/state join is not a validated CBSA crosswalk; a bivariate null does not identify demand or immigration effects. Current housing evidence: [housing supply, CA and TX](immigration-housing-supply-ca-tx-2026-09-22.md) |

## Population and income surveys

| Dataset and vintage | Where it is | Use | Limits |
|---|---|---|---|
| ACS 2023 one-year PUMS, person and household | `sources/immigration-fiscal/data/census/acs_pums_2023_person.zip`, `acs_pums_2023_household.zip` | Composition, education, geography, commute, household structure and income; housing context | Lifetime paths and legal status are not observed |
| ACS one-year `B03001` and Selected Population Profile `S0201`, 2005–2024 | Tracked `historical_backcast_2026_09_20/inputs/acs_mexican_origin.csv`, regenerated by `pull_acs.py` (needs `CENSUS_API_KEY`) | National Mexican-origin count every year; per-capita income, median age, median full-time year-round earnings by sex and median household income for the Mexican group and the total, 2008 onward, for the [2005–2024 back-cast](immigration-historical-backcast-2026-09-20.md) | No 2020 release; the profile endpoint starts in 2008 and failed for 2010. The group code is `401` to 2022 and `4015` from 2023, variable codes move yearly, and `S0201PR_*` Puerto Rico variants share labels: resolve by label on `S0201_\d+E` only. Self-identified origin, not the account's birthplace-plus-identification union (ratio 1.049 in 2024) |
| ACS 2019 and 2024 race wages and public-pupil exposure | The ACS 2019 and 2024 person files below; no separate acquisition | `analyze_wage_race.py`, `measure_acs_school_exposure_2024.py`: Black-alone and any-race sensitivity, ethnicity precedence; employment, annual wages and earnings kept separate | Public enrollment in the prior 3 months is not annual student-days |
| CPS ASEC 2024 (income 2023) | `sources/immigration-fiscal/data/census/cps_asec_2024_march.zip`; a later download is byte-identical, SHA256 `cdb39cdac34bef99dd0940ab28e306f692404c2eea44d85dfd634214872a0a09` | Income, insurance and benefit cross-checks; native `TAX_ID`, tax carriers, dependent filers and 160 replicate weights (`same_year_tax_2026_09_20`) | Modeled returns, not observed filings; 560 zero-income filing units need a count convention or bounds; weak for recent immigration-flow levels |
| CPS ASEC 2025 (income 2024) | `sources/immigration-fiscal/data/external/stage3/census/cps_asec_2025/asecpub25csv.zip`, 147,271,429 bytes: person, household and family CSVs and 160 replicate weights, with the dictionary, replicate instructions, the 2026 household-position correction and the tax-method notes; [official directory](https://www2.census.gov/programs-surveys/cps/datasets/2025/march/) | The income-year 2024 account; `analyze_cps_fiscal_2025.py`: 142,125 people, 58,147 SPM units, Census-modeled taxes, credits and selected transfers | No current legal status; unit allocation and actual collection differ |
| CPS ASEC 2024 and 2025, Census API person pulls | `sources/immigration-fiscal/data/external/cps/asec/asec_{2024,2025}_{persons,supp,supp2}.json`, about 85 MB; re-pull with `infra/immigration-fiscal/cps_generation_welfare_2026_09_16/pull_cps_asec*.sh` (needs `CENSUS_API_KEY`, about 15 minutes); rows in `DOWNLOAD_MANIFEST.tsv` | Parental birthplace (`PEFNTVTY`/`PEMNTVTY`), Hispanic detail (`PRDTHSP`) and program flags, for second and third-plus generations by parental origin without IPUMS: `asec_generation_welfare.py`, `mexican_origin_by_generation.py` and the 2026-09-16 welfare and Mexican-origin generation memos | Third-plus is self-identified, so ethnic attrition applies; no under-16 enrolment field; no replicate weights |
| CPS-ASEC-2022-FULL (2022 survey, 2021 income) | `infra/immigration-fiscal/latam_comparison_2026_09_17/_cache/2022/asecpub22csv.zip`, 157,679,473 bytes, SHA256 `7338011adefca16dae30a4469ddaf0c01cef579b607b26b4bceec749376e4ac9`, with `asec2022_ddl_pub_full.pdf` and the replicate-weight instructions; [official release](https://www.census.gov/data/datasets/time-series/demo/cps/cps-asec.2022.html) | Own and parents' birthplace, race and Hispanic self-ID, schooling, work, person poverty and earnings; full and 160 replicate person weights ([country comparison](immigration-latam-benchmark-comparison-2026-09-17.md)) | Join person to weights by `PH_SEQ,PPPOS` / `h_seq,PPPOS`, never by row order |
| CPS-ASEC-2023-FULL (2023 survey, 2022 income) | `infra/immigration-fiscal/latam_comparison_2026_09_17/_cache/2023/asecpub23csv.zip`, 150,165,063 bytes, SHA256 `d2e000250782adfbdd7f29c82b66d866591a30f0d330496698ec19f9c784ce11`, with its dictionary and replicate instructions; [official directory](https://www2.census.gov/programs-surveys/cps/datasets/2023/march/) | Same constructs and join; completes the full-weight and replicate coverage the earlier API extract lacked. Joins are checked in `latam_comparison_2026_09_17/derived/audit.json`, the disability audit in `frontier_execution_2026_09_17/derived/social/cps_audit.json` | Pooled years are overlapping cross-sections, not independent: keep each year's population controls and treat cross-year covariance conservatively. No legal-status or grandparent field |
| SIPP 2023, public use | `sources/immigration-fiscal/data/external/stage2/census/sipp/pu2023_csv.zip` | Earlier staging and calibration | See the SIPP 2024 card |
| SIPP 2025 (reference year 2024) | `sources/immigration-fiscal/data/external/stage3/census/sipp_2025/{pu2025_csv.zip,rw2025_csv.zip}`, 88,088,487 and 535,845,832 bytes, with schemas, dictionary and guide; [official directory](https://www2.census.gov/programs-surveys/sipp/data/datasets/2025/) | `analyze_sipp_2025.py`: 379,215 person-months and 240 Fay-BRR weights; selected benefits allocated once before the age and nativity filters | `TYRENTRY` 2025 denotes 2022–25; `TIMSTAT` is first entry as Permanent/Other, not current status. Own and parent foreign birthplaces are region recodes, not Mexican-country identifiers ([lineage audit](../infra/immigration-fiscal/sipp_lineage_2026_09_20/RESULT.md)); identifier-only G3/G4+ adult support is small, and no nonidentifier correction is fitted |
| ACS one-year person PUMS 2005–2018, 2021 and 2022 (16 zips, 9.4 GB) | `sources/immigration-fiscal/data/external/acs_pums_years/csv_pus_{2005..2018,2021,2022}.zip`, fetch log `download.log` | read by `return_vs_us_stayers_2026_09_26` (`compare.py`), `dataset_integrity_2026_09_23` (`acs_extract.py`), `schooling_selection_position_2026_09_23` (`acs_pums_check.py`); fetched by `arrival_cohorts_2026_09_18`; cited in `acs_schooling_break_2026_09_26` | ACS 2019, 2023 and 2024 are held elsewhere; 2020 is not held |
| BLS Consumer Expenditure Survey published tables: income quintiles 2023 and 2024 (Table 1101), all consumer units 2024 (Table 2500), aggregate shares by quintile 2024 | `sources/immigration-fiscal/data/external/cex_2024/{cu-income-quintiles-before-taxes-2023,cu-income-quintiles-before-taxes-2024,cu-all-detail-2024,agg-share-quintiles-2024}.xlsx` (the 2024 quintile table is the same size as the copy in `consumption_key_2026_09_24/_cache/sources/`) | read by `consumer_price_benefit_2026_09_18` (`cex_parse.py`) | tables by income group only; no nativity or origin split |
| Census population estimates vintage 2024, state totals (`NST-EST2024-ALLDATA.csv`) | `sources/immigration-fiscal/data/external/census_popest_2024/NST-EST2024-ALLDATA.csv` (same size as the copy in `apportionment_2026_09_18/_cache/`) | read by `assumption_explorer_2026_09_21` (`scaling_check.py`), `full_account_receipts_2026_09_20` (`builder.py`), `state_priced_services_2026_09_29` (`state_price.py`), `unauthorized_population_size_2026_09_19` (`coverage_and_ladder.py`) | — |
| CPS ASEC 2025 technical documentation (`cpsmar25.pdf`) and public-use data dictionary (PDF and text) | `sources/immigration-fiscal/data/external/cps_asec_doc/{cpsmar25.pdf,asec2025_ddl_pub_full.pdf,ddl25.txt}` | read by the `builder.py` of `admin_tax_checks_2026_09_19`, `education_origin_fiscal_2026_09_19` and `full_account_receipts_2026_09_20`; cited in `arrival_window_fiscal_2026_09_18`, `candidate_attack_2026_09_28`, `cps_imputation_keys_2026_09_23`, `mexican_origin_population_total_2026_09_19` | documentation of the registered CPS ASEC 2025 file |
| PIAAC United States 2017 public-use file (`prgusap1_2017.csv`) | `sources/reused-surveys/piaac/prgusap1_2017.csv` | no script reads it | — |
| Federal Reserve Survey of Consumer Finances 2022: full public dataset and summary extract (Stata), codebook | `sources/immigration-fiscal/data/external/stage3/frb/scf2022/{scf2022s.zip,scfp2022s.zip,codebk2022.txt}`, hashes in `ACQUIRED.md` | [scf_filing_status_2026_10_07](../infra/immigration-fiscal/scf_filing_status_2026_10_07/RESULT.md) (`scf_joint.py`): Hispanic and white joint filers' income tax under Tax-Calculator against Treasury OTA's tax-record ratio | Five implicates, replicate weights not used; race is the designated respondent's (`X7004`, `X6809`); filing items (`X5744`, `X5746`) and incomes refer to 2021 |

ASEC 2020, 2021 and 2026, the CPS basic monthly files and the CPS supplements are held inside lanes; see the table at
the end of this section.

### ACS2024_PUMS_VERIFIED_LOCATION — current resident-cohort source

**Source:** US Census Bureau; relocated and reverified 2026-09-05, no duplicate download.
**Local:** `sources/immigration-fiscal/data/external/acs_pums_2024_1yr/`: person ZIP `csv_pus.zip` 602,847,146 bytes,
household ZIP `csv_hus.zip` 251,500,587 bytes and the official dictionary `PUMS_Data_Dictionary_2024.pdf`, 395,086
bytes; CSV and text dictionaries are in `external/acs_pums_dict/`.
[Official files](https://www2.census.gov/programs-surveys/acs/data/pums/2024/1-Year/),
[dictionary](https://www2.census.gov/programs-surveys/acs/tech_docs/pums/data_dict/PUMS_Data_Dictionary_2024.pdf).
**Checks:** the person ZIP was fully analyzed: 3,422,888 rows, weighted 340,110,990 people. Full and SDR-SE
calibration checks reproduce the male and age 25–34 populations. The person SHA256 and raw member details are in
`.scratch/cohort-clarity-20260905/analysis/manifest_2024.json` and `standardization/results.json`. The geography
header is `STATE`; `POBP` 448 is Somalia.
**Use:** recent-entry resident profiles, birthplace, education, employment, earnings and 80 replicate weights; the tax
lane's common civilian-household comparison (`STATE`, `HISP=2`, `POBP=303`, wages with `ADJINC`, 80 replicates; hash in
that lane's audit); the same generators as the 2019 card.
**Limits:** 2024 only, not the 2020–2024 pooled file or an admission ledger. Income is a rolling prior 12 months; no
legal status, religion, ideology or parental origin; no complete match to the CPS union. Read the schooling break below
before comparing schooling across 2019/2020.

### ACS2019_PUMS_NATIONAL_PERSON — recent-entry baseline

**Source:** US Census Bureau; acquired 2026-09-05, recovered from the USB and matched to its recorded hash 2026-09-20.
**Local:** `sources/immigration-fiscal/data/external/acs_pums_2019_1yr/csv_pus.zip`, 567,851,237 bytes, SHA256
`18e4ece4cc24781c01e8046c2d5afbabeb1f15452ddec43f60fdf3b1f6e67b92`; the ZIP includes the official README.
[2019 one-year PUMS directory](https://www2.census.gov/programs-surveys/acs/data/pums/2019/1-Year/),
[person ZIP](https://www2.census.gov/programs-surveys/acs/data/pums/2019/1-Year/csv_pus.zip),
[documentation](https://www.census.gov/programs-surveys/acs/microdata/documentation.2019.html),
[accuracy PDF](https://www2.census.gov/programs-surveys/acs/tech_docs/pums/accuracy/2019AccuracyPUMS.pdf).
**Checks:** both national CSV members read completely; 3,239,553 rows and 328,239,523 weighted people reproduce the
official PUMS checks.
**Key variables:** `NATIVITY`, `POBP`, `YOEP`, `AGEP`, `SEX`, `RELSHIPP`, `ESR`, `SCHL`, `PERNP`, `PINCP`, `ENG`,
`ADJINC`, `PWGTP1–80`. Recent `YOEP` values are single years, and the most recent entry is not necessarily the first
immigration. Income covers the prior 12 months, including zeros and losses; `ADJINC` alone does not put different
survey years into common dollars. All 80 replicate weights are kept, including negative and zero values.
**Used in:** the [2019/2024 cohort comparison](immigration-cohort-clarity-2026-09-05.md);
`infra/immigration-fiscal/build/analyze_arrival_cohorts.py`, `standardize_arrival_profiles.py` and
`summarize_arrival_cohorts.py`. Generated evidence and input hashes: `.scratch/cohort-clarity-20260905/analysis/` and
`standardization/`.

### ACS_PRICE_AND_CALIBRATION_2019_2024 — comparison inputs

**Source:** [Census ACS comparison guidance](https://www.census.gov/programs-surveys/acs/guidance/comparing-acs-data/2024.html),
retrieved 2026-09-05. **Local:** `.scratch/cohort-clarity-20260905/availability/inflation.json` and `inflation-source-*`.

R-CPI-U-RS annual indices: 2019 = 375.8, 2023 = 449.3, 2024 = 462.5, so the 2019→2024 factor is 462.5/375.8 and the
2023→2024 factor 462.5/449.3. The manifest pins the Census-guidance vintage; the later corrected BLS workbook was not
retrieved. Four official CSVs supply the 2019 and 2024 person counts and the PUMS full and SE calibration anchors;
URLs, byte counts and hashes are in the JSON. These are documentation and calibration data, not a household survey.
Both comparison generators use them, and processed income gets the cross-year factor only once.

### Known break in ACS schooling

Among Mexico-born adults aged 20–64, reports of no schooling completed (`SCHL` 1; IPUMS `EDUCD` 2) step from 5.55% in
2019 to 8.45% in 2020 and stay there (8.66% in 2021, 9.11% in 2024); a fixed 1990–99 arrival cohort shows the same
step. Grade 8 or less looks continuous in raw totals (29.2% to 29.0%), but detrended it steps up 0.8–1.0 points for the
Mexico-born and 0.13–0.15 for the US-born. Grade 9 supplies about a quarter of the lost reports, and natives aged 20–64
gain +0.20 points of "none" (+30%). The step is a reporting or processing change whose exact cause is not identified.
The Census Bureau documents over-reporting of "No schooling completed" in mail and internet responses (ACS Design and
Methodology v4.0, §5.10), and it changed the item in the 2025 ACS, a second break in the same item and in the diploma
and some-college categories. Series that split the bottom band or score years of schooling across 2019/2020 need a
break term. First documented as F6 of the
[dataset integrity audit](../infra/immigration-fiscal/dataset_integrity_2026_09_23/acs.md); sizes, exposed lanes and a
preferred flow-rate correction are in
[`acs_schooling_break_2026_09_26`](../infra/immigration-fiscal/acs_schooling_break_2026_09_26/RESULT.md).
[DATA: `infra/immigration-fiscal/return_vs_us_stayers_2026_09_26/derived/acs_no_schooling_break.csv`, reproduced from
the Census PUMS files for 2017–2019 and 2021–2024]

### SIPP_2024 — public use, reference year 2023

**Source:** Census public-use files, reacquired 2026-09-05.
**Local:** `sources/immigration-fiscal/data/external/stage3/census/sipp/pu2024_csv.zip`; the repair staging copy, with
the schema and dictionary, is in `.scratch/data/external/stage3/census/sipp/`.
**Primary data:** [pu2024_csv.zip](https://www2.census.gov/programs-surveys/sipp/data/datasets/2024/pu2024_csv.zip),
102,122,301 bytes, SHA256 `3a78b26988c76c02b9e206f72507390fb6ec9dac7974ec31aa90abc9d9809764`.
**Schema:** [pu2024_schema.json](https://www2.census.gov/programs-surveys/sipp/data/datasets/2024/pu2024_schema.json),
757,529 bytes, SHA256 `601042d6f32e4c8ccd98952e91d0e25dc02d22d2dcb8babd4a2c269046d87b3d`.
**Dictionary:** [2024_SIPP_Data_Dictionary.pdf](https://www2.census.gov/programs-surveys/sipp/tech-documentation/data-dictionaries/2024/2024_SIPP_Data_Dictionary.pdf),
4,015,396 bytes, SHA256 `f7af93a5b75fc6c3b67ca9c8aad7de78c32d071aa829b682f01312a3f46c7289`. The three files total
106,895,226 bytes.

**Key definitions:** `EEDUC` 31–38 = less than high school; 39 = HS/GED; 40–42 = some college/associate; 43–46 = BA+.
`TAGE_EHC` is reference-month age. `TPEARN` may include negative business income. SNAP/TANF amounts are held on the
named benefit owner, with covered members identified by the owner/member fields; SSI is individual. Household and
benefit-unit totals must not be copied to every ACS adult. Annual donors use reference-year earnings and the
appropriate annual weight. [SOURCE: Census dictionary and user guide]

**Use:** person-month earnings and explicitly linked benefit units for reference year 2023 (the file label 2024 is not
the income or tax year). Read by `infra/immigration-fiscal/build/build_federal_microsim_sipp_2024.py` and
`build_public_mvp_sipp_module_2024.py`; the person donors, monthly profiles, health bridge and scenario exports were
rebuilt on it in September. Donor grids hold 64 cells each
([nativity/support decision](../decisions/2026-09-05-person-donor-support.md)). Historical `_usborn` keys mean the ACS
native definition, including citizenship at birth abroad. Raw MEPS was not re-estimated; the retained aggregate means
carry corrected source labels and an explicitly approximate birthplace bridge.
**Limits:** not a household-total donor for each adult; no clean legal-status panel; own and parent foreign
birthplaces are region recodes ([lineage audit](../infra/immigration-fiscal/sipp_lineage_2026_09_20/RESULT.md)).

The [16-file fiscal input catalog](../infra/immigration-fiscal/acquire/fiscal_2024_sources.tsv) pins exact URLs, bytes
and SHA256 for the CPS, SIPP and MEPS data and documents, including SIPP definitions reused from the admission
acquisition. The 2024 accounts, race splits and uncertainty CSVs built from them are standalone products, not
substituted into the earlier 2023 fiscal tensor ([integrated findings](immigration-clarity-update-2026-09-05.md)).

### IPUMS_CPS_ASEC_1994_2025_2NDGEN — parental birthplace and outcomes, 32 ASEC files

- Source/acquired: IPUMS CPS extract 1 on the operator's account, submitted and downloaded through the IPUMS API by
  `infra/immigration-fiscal/acquire/ipums_cps_second_gen.py` on September 22, 2026.
- Local/codebook/size: `sources/immigration-fiscal/data/external/cps/cps_2ndgen.csv.gz`, 131,330,429 bytes, SHA256
  `a510e7a969548694…` in `cps_2ndgen.manifest.json` beside it; DDI codebook `cps_2ndgen.xml` (31 variables); 5,721,633
  person rows, ASEC 1994–2025, rectangular person file.
- Key variables: `NATIVITY` (1 both parents native … 5 foreign-born), `BPL`/`FBPL`/`MBPL` (5-digit IPUMS-CPS detailed
  codes: 09900 US, 20000 Mexico, 21030 El Salvador, 51500 India), `CITIZEN`, `YRIMMIG`, `AGE`, `SEX`, `RACE`,
  `HISPAN`, `MARST`, `EDUC`, `EMPSTAT` (10/12 employed), `LABFORCE` (2 in labor force), `INCTOT`/`INCWAGE` (999999999
  not in universe), `UHRSWORKLY`, `WKSWORK1`, `NCHILD`, `YNGCH`, `ASECWT`; record ids `SERIAL`, `PERNUM`, `CPSID`,
  `CPSIDP`.
- Quirks/use: parental birthplace is country-level, but the loader collapses it to nine regions; `EDUC` is a code, not
  years; no replicate weights were requested; the ASEC oversample flags (`ASECFLAG`, `HFLAG`) are carried.
  `build/load_cps_second_gen.py` builds `derived/lifetime/cps_second_gen_by_origin.csv` (37 generation × origin cells,
  ages 25–64, n ≥ 100; context warehouse table `cps_second_gen_by_origin`). Memo:
  [second generation by origin](immigration-second-generation-by-origin-2026-09-22.md) (ladder 178). Also read by
  `schooling_selection_position_2026_09_23/cps_check.py`, `mexborn_count_2026_09_23`, `selection_curve_2026_09_27` and
  `world_ledger_2026_09_27/g2_premium.py`.

### IPUMS_CPS_ASEC_1999_2025_MOVERS — reason for moving, migration, replicate weights (extracts 2 and 3)

- Source/acquired: IPUMS CPS extracts 2 and 3 on the operator's account, submitted by
  `infra/immigration-fiscal/movers_reasons_2026_09_24/fetch_ipums.py` on September 24, 2026 and downloaded with the same
  script.
- Local/codebook/size: lane cache `infra/immigration-fiscal/movers_reasons_2026_09_24/_cache/ipums/` (ignored).
  `cps_main.csv.gz`, 113,716,045 bytes, SHA256 `948c590b0fcf49c3…`, DDI `cps_main.xml` (35 variables), 5,027,101 person
  rows, ASEC 1999–2025. `cps_repwt.csv.gz`, 34,279,160 bytes, SHA256 `ee28a211cb585…`, DDI `cps_repwt.xml` (178
  variables), 59,734 interstate movers (MIGRATE1 = 5), ASEC 2005–2025. Manifest `manifest.json` beside them.
- Key variables: `WHYMOVE` (main reason for moving, 20 codes), `MIGRATE1`, `MIGSTA1`, `STATEFIP`,
  `COUNTY`/`COUNTYERR`, `METFIPS`, `NATIVITY`, `BPL`, `CITIZEN`, `HISPAN`, `RACE`, `AGE`, `SEX`, `EDUC`, `INCTOT`,
  `HHINCOME`, `OWNERSHP`, `RELATE`, `HFLAG`, `ASECWT`, `CPI99`; `REPWTP1`–`REPWTP160` in extract 3.
- Quirks/use: no county or metro of residence one year ago exists in IPUMS ASEC; the 2014 ASEC's two files are each
  weighted to the full population (scale by 0.6986/0.3014); in ASEC 2012–2015 reason codes 14–17 nearly vanish while
  code 13 swells; the CPS finds 0.62–0.87 of the ACS level of California out-movers. Consumed by the movers lane
  (`build_cps.py` and after; ladder 221).

### IPUMS_USA_EXTRACTS_2026_09_23 — IPUMS USA extracts 2–15, one store

- Source/acquired: IPUMS USA, University of Minnesota [SOURCE: https://usa.ipums.org/usa/]. Extracts 1 and 2 were built
  in the browser on June 23, 2026. Extract 1 was superseded by 2 and never downloaded, and the files of both have since
  expired at IPUMS. The schooling, crime and ancestry lanes submitted extracts 3–15 through the API on September 23,
  2026. `infra/immigration-fiscal/ipums_usa_store_2026_09_23/organize.py` downloaded 7 and 8, fetched the missing DDIs
  and built the store. Every September file matches IPUMS's published sha256
  [DATA: `infra/immigration-fiscal/ipums_usa_store_2026_09_23/derived/gates.csv`].
- Local/codebook/size: `sources/immigration-fiscal/data/external/ipums/usa_extract/usa_000NN_<samples>_<universe>[_<content>].csv.gz`,
  each with its DDI beside it as `.xml` (none exists for 2). These are hard links to the lane caches. Catalog:
  `usa_extract/CATALOG.md` and `catalog.json`, with a tracked copy in the lane's `derived/`. 14 held extracts,
  97,451,092 person rows, 1.64 GB compressed. Typed Parquet (1.13 GB) is in `sources/immigration-fiscal/derived/ipums_usa/`.
  DuckDB `sources/immigration-fiscal/derived/ipums_usa_extracts.duckdb` has views `usa_00002`…`usa_00015`, `qflags`,
  `usa_000NN_q` and `usa_00002_sex`, and tables `catalog`, `variables`, `value_labels`, `joins` and `gates`. SHA256 per
  file in the raw-file manifest.
- Key variables: person key `YEAR`, `SAMPLE`, `SERIAL`, `PERNUM`, unique within every extract and the same person across
  extracts. Also `BPL`/`BPLD`, `CITIZEN`, `YRIMMIG`, `EDUC`/`EDUCD`, `AGE`, `SEX` (not in 2), `HISPAN`, `RACE`,
  `GQ`/`GQTYPE`, `STATEFIP`, `PERWT`, and `REPWTP1`–`REPWTP80` (5 and 7). Extract 10 has wages, hours, weeks, commute,
  `PUMA` and `MET2013`; 11 has the same with `METAREA` and `COUNTYFIP`. Allocation flags `QBPL`, `QYRIMM`, `QEDUC` and
  `QCITIZEN` come from 6, 13, 14 and 15.
- Universes:
  - 2: all persons in the 1980, 1990 and 2000 5% censuses and the ACS 2010 and 2023.
  - 3: the Mexico-born, 1980–2000 censuses and ACS 2005–2024.
  - 4 and 6: men 18–40, 1980–2000 censuses.
  - 5: Mexico-born men 18–40, ACS 2006–2024 without 2020.
  - 7 and 9: US-born men 18–40, ACS 2019, 2023 and 2024.
  - 8: US-born men 18–40, ACS 2006–2024 without 2020.
  - 10: ages 16–64 in the 2000 5% census, the ACS 2010 and the ACS 2009–2011.
  - 11: ages 16–64 in the 1990 5% census.
  - 12: the Mexico-born, ACS 2000–2004.
  - 13: QEDUC for the people of 3 and 12.
  - 14: institutionalized men 18–40, 1980–2000.
  - 15: institutionalized persons of all ages, 2000.
- Quirks/use:
  - Joins: all 55 pairs of extracts that share a sample were joined on the four keys. Every record inside an
    overlapping universe found its counterpart, and 788 shared columns agree record by record, so flags and SEX carry
    across extracts [DATA: `infra/immigration-fiscal/ipums_usa_store_2026_09_23/derived/joins.csv`]. `usa_000NN_q`
    attaches the flags to each extract they cover; a NULL flag means not extracted for that record.
  - SEX for the Borjas panel: `usa_00002_sex` covers 29–66% of weighted records by year. It includes two absence rules,
    each tested at 0 errors [DATA: `infra/immigration-fiscal/ipums_usa_store_2026_09_23/derived/sex_coverage.csv`].
  - Store layout: the slugged names share `usa_extract/` with the original `usa_00002.csv.gz`, which
    `build/load_ipums_borjas_panel.py` resolves by exact name (4767db7). The views hold absolute Parquet paths, so re-run
    `organize.py duckdb` after moving the repository.
  - Content limits: the 1990 and 2000 files do not identify institution type. US-born means the 50 states and DC. The
    ACS schooling break above applies to `EDUCD` 2.
  - Used by: crime_selection_cohorts (4, 5, 6, 9, 14, 15), schooling_selection_position (3, 12, 13),
    ancestry_iv_congestion_wages (10, 11) and the Borjas panel loader (2). Extracts 7 and 8 are not yet used
    [INFERENCE: from `rg` over the lanes' scripts]. Store README:
    [`ipums_usa_store_2026_09_23/README.md`](../infra/immigration-fiscal/ipums_usa_store_2026_09_23/README.md).
  - Outside the store: extracts 16 (employed persons, ACS one-year 2012–2024, 19,103,402 rows) and 17 (the same for
    2005–2011, 9,683,631 rows) sit in `compliance_gap_2026_09_24/_cache/ipums/` as `workers.csv.gz` and
    `workers_pre.csv.gz`, each matching IPUMS's published sha256 (ladder 220).

### In analysis lanes

| Dataset and vintage | Where it is | Use | Limits |
|---|---|---|---|
| BLS Consumer Expenditure Survey: 2024 Interview PUMD with dictionary; published tables 2023–2024 (income groups, Latino reference person) | [consumption_key_2026_09_24](../infra/immigration-fiscal/consumption_key_2026_09_24/RESULT.md) `_cache/sources/intrvw24.zip`, `_cache/sources/ce-pumd-interview-diary-dictionary.xlsx`, `_cache/sources/{cu-*,reference-person-*}.xlsx` | spending-to-income ratios by income rank for the consumption-tax key (ladder 225) | units classed by reference person's Hispanic origin; no nativity or parents' birthplace |
| Census 2020 Post-Enumeration Survey memorandum G-05, net coverage error by race and Hispanic origin | [mexican_origin_population_total_2026_09_19](../infra/immigration-fiscal/mexican_origin_population_total_2026_09_19/RESULT.md) `_cache/sources/pes_net_coverage_race_hispanic.pdf` | Hispanic net undercount (4.99%) for the coverage arm (ladder 158) | an upper bound on the census-base component, not an additive correction |
| Census apportionment results 2020 (tables 1–2) and 2010 (table 1, priority values, overseas counts) | [apportionment_2026_09_18](../infra/immigration-fiscal/apportionment_2026_09_18/RESULT.md) `_cache/{apportionment-2020-table01.xlsx,apportionment-2020-table02.xlsx,apport2010-table1.xls,PriorityValues2010.xls,2010CensusOverseasCounts.xlsx}` | Huntington-Hill check and counterfactual House-seat arms (ladder 147) | counts every resident regardless of immigration status |
| Census population estimates: state totals (intercensal 2000–2010; vintages 2019, 2024, 2025), national monthly and characteristics (vintage 2024), county and CBSA totals (vintage 2025) | [apportionment_2026_09_18](../infra/immigration-fiscal/apportionment_2026_09_18/RESULT.md) `_cache/{NST-EST2024-ALLDATA.csv,NST-EST2024-POP.xlsx}`; [displacement_transfers_2026_09_18](../infra/immigration-fiscal/displacement_transfers_2026_09_18/RESULT.md) `_cache/NST-EST202{4,5}-ALLDATA.csv`; [enforcement_rents_2025_2026_09_27](../infra/immigration-fiscal/enforcement_rents_2025_2026_09_27/RESULT.md) `_cache/popest/{NST-EST2025-ALLDATA.csv,co-est2025-alldata.csv,cbsa-est2025-alldata.csv}`; [housing_supply_ca_tx_2026_09_22](../infra/immigration-fiscal/housing_supply_ca_tx_2026_09_22/RESULT.md) `_cache/{popest_2000_2010_intercensal.csv,popest_2010_2019.csv,popest_2020_2024.csv}`; [nibrs_arrests_2026_09_16](../infra/immigration-fiscal/nibrs_arrests_2026_09_16/RESULT.md) `_cache/nc-est2024-alldata-h-file{02,08,10}.csv`; [clemens_pritchett_calibration_2026_09_19](../infra/immigration-fiscal/clemens_pritchett_calibration_2026_09_19/RESULT.md) `_cache/{NA-EST2024-POP.xlsx,NST-EST2024-ALLDATA.csv}` | population denominators, net migration, apportionment, permits per resident (ladders 78, 140, 147, 154, 180, 245) | vintage 2025 ends June 2025, before most of the enforcement surge |
| CPS ASEC public-use CSV 2020, 2021 and 2026 (income years 2019, 2020 and 2025), with data dictionaries (Census) | [backcast_pandemic_measured_2026_09_28](../infra/immigration-fiscal/backcast_pandemic_measured_2026_09_28/RESULT.md) `_cache/asecpub{20,21}csv.zip`, `_cache/ddl{2020,2021,2022}.pdf`, hashes in `acquire.py`; [ledger_asec2026_2026_09_16](../infra/immigration-fiscal/ledger_asec2026_2026_09_16/RESULT.md) `_cache/{asecpub26csv.zip,asecpub26csv.zip.sha256,asec2026_ddl_pub_full.pdf,ddl2026.txt,ddl2025.txt}` | benefit-key shares for income years 2019–2020 (ladder 251); second-generation gap on income year 2025 | 2020–21 files lack an SSN field; 2026 file drops SPM broadband and migration columns |
| CPS basic monthly public-use files, January 2024 – August 2026 (October 2025 never collected), with record layouts | [mexborn_count_2026_09_23](../infra/immigration-fiscal/mexborn_count_2026_09_23/RESULT.md) `_cache/basic/{jan…dec}{24,25,26}pub.zip`, `_cache/layout/*`, `_cache/sources/bls_population_control_adjustments_{2025,2026}.{pdf,txt}`; March 2025 also in [cps_imputation_keys_2026_09_23](../infra/immigration-fiscal/cps_imputation_keys_2026_09_23/RESULT.md) `_cache/basic/mar25pub.csv` | monthly Mexico-born series (ladder 209); ASEC imputation check against weekly earnings (ladder 208) | arrival year 20–24% allocated; the imputation check cannot separate zero from the drift |
| FDIC National Survey of Unbanked and Underbanked Households (CPS June supplement): reports 2015–2019, technical documentation 2011–2019 | [consumption_key_2026_09_24](../infra/immigration-fiscal/consumption_key_2026_09_24/RESULT.md) `_cache/senders/fdic_report_{2015b,2017,2019}.pdf`, `_cache/senders/techdoc_jun{11,13,15,17,19}.pdf`; person rows are Census API pulls `_cache/senders/unbank_{2011,2013,2015,2017,2019}.json` | household remittance-sender rates by nativity and generation (ladder 225) | asks whether anyone sends money abroad, not how much |
| Federal Reserve Survey of Consumer Finances 2022, summary extract public data (Stata), with the bulletin macro | [housing_transfer_2026_09_23](../infra/immigration-fiscal/housing_transfer_2026_09_23/RESULT.md) `_cache/scfp2022s.zip`, `_cache/scf/rscfp2022.dta`, `_cache/scf/bulletin.macro.txt`, hashes in `_cache/manifest.json`; read in place by [distribution_weights_2026_09_23](../infra/immigration-fiscal/distribution_weights_2026_09_23/RESULT.md) | Hispanic shares of rental and other real-estate ownership (ladder 190) | — |
| Opportunity Insights public tables (2018): Opportunity Atlas national and county outcomes; Race and Economic Opportunity tables | [oi_parental_income_2026_09_16](../infra/immigration-fiscal/oi_parental_income_2026_09_16/RESULT.md) `_cache/national_percentile_outcomes.csv`, `_cache/{table_1,table_5…table_10,race_t2,race_t3,race_t4,race_t7}.csv`; [connectedness_fragmentation_2026_09_28](../infra/immigration-fiscal/connectedness_fragmentation_2026_09_28/RESULT.md) `_cache/oa/county_outcomes_simple.csv` | male incarceration by parental income and race (ladder 82); county child income rank (ladder 262) | tax linkage drops children of non-filers; cohorts born 1978–83, observed 2010 |

## Health and care

| Dataset and vintage | Where it is | Use | Limits |
|---|---|---|---|
| MEPS HC-251, 2023 full-year file | `sources/immigration-fiscal/data/external/stage3/ahrq/meps/` | Medical spending and payer incidence; the health-admin lane reuses it read-only, turning monthly coverage into member-years | Few immigrant-status fields |
| MEPS HC-256, 2024 | `sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/{h256dat.zip,h256su.txt,h256doc.pdf,h256cb.pdf}`, data ZIP 6,125,956 bytes; [release, August 2026](https://meps.ahrq.gov/mepsweb/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-256); a failed partial codebook is excluded | `meps_health_transport_2024.py`: 19,140 records, 18,683 positive weights, 105 strata and 264 PSUs; six disjoint public payers | Donors by US or foreign birth only; no direct Mexico or status costs; institutional care and administration omitted |
| MCBS 2023 Cost Supplement PUF | [Acquisition and access report](../infra/immigration-fiscal/fiscal_access_2026_09_20/RESULT.md), [manifest](../infra/immigration-fiscal/fiscal_access_2026_09_20/manifest.json), [recipe](../infra/immigration-fiscal/fiscal_access_2026_09_20/README.md) | 6,920 records × 134 fields: payer and service spending, age, sex, broad race, main weight and 100 replicates; 65+ public payments by ethnicity in [`mcbs_elderly_medical_2026_09_22`](../infra/immigration-fiscal/mcbs_elderly_medical_2026_09_22/RESULT.md) (ladder 173) | No Mexico or parent birthplace; facility, hospice and institutional events excluded; costs top-coded; randomized IDs cannot join other MCBS releases, claims or years; not full claims |
| CMS Scorecard EX.5 and 2026 Beneficiary Profile, CY2023; EX.2, FY2023 | `health_admin_2026_09_20/raw/`; [pins, API requests and hashes](../infra/immigration-fiscal/health_admin_2026_09_20/source_pins.json); ETL 3.9.61 / data 20251205 | 648 EX.5 eligibility, state and year rates with quality notes; national member-years and spending; EX.2 service and program scale | Institutions, territories and Medicare premiums included; EX.5 excludes CHIP, administration and DSH; state eligibility numerators and member-months are not exposed by the API |
| CMS/Mathematica LTSS tables 2023 and methodology | Same health lane; nine health and documentation files, 8,224,811 bytes; [card](../infra/immigration-fiscal/health_admin_2026_09_20/REGISTER_SNIPPET.md) | Institutional and home-and-community spending by state and delivery system; source-quality flags | TAF encounters differ from CMS-64 cash; California HCBS is flagged high concern; scope tests are not exact reconciliations or bounds |
| CMS National Health Expenditure tables, 1970–2024 | `sources/immigration-fiscal/data/external/nhea/`: the tables zip (unpacked in `nhe_tables/`) and the NHE summary with shares of GDP, 1960–2023; the same tables zip is in `mr_leads_papers_2026_09_21/_cache/nhe-tables.zip`, 520,391 bytes, SHA256 `a09ef6d3e84e25d745047a47b6b08a0d96b303085b4c725b67ce67a0eb0c4420`, [CMS](https://www.cms.gov/files/zip/nhe-tables.zip) | Table 15 nursing care facilities by payer (2024: total $219.9bn, Medicaid $78.9bn, Medicare $47.3bn); Table 14 home health (total $169.4bn, Medicaid $38.2bn); `debt_legacy_2026_09_23` also reads the tables | National totals for all ages; most Medicaid home-and-community waiver spending sits in Table 13, not Table 14 |
| ACS 2024 one-year PUMS, elder-care tabulations | Tracked `mr_leads_papers_2026_09_21/derived/acs_care_inputs.csv`, regenerated by `pull_acs_care.py` (needs `CENSUS_API_KEY`); raw responses in the lane's ignored `_cache/` | Employed aides and nursing assistants (occupation codes 3601, 3602, 3603, 3605) by nativity, Mexican birthplace and Mexican origin; working-age population with less than one year of college; population 65+ and 80+ by housing type and nativity ([papers memo](immigration-marginal-revolution-leads-read-2026-09-21.md)) | Weighted counts only, no standard errors; institutional group quarters not split by type; occupation is the current or most recent job |
| NHIS 2023 and 2024 Sample Adult | `sources/immigration-fiscal/data/external/crime_frontier/nhis/nhis_{2023,2024}_sample_adult.zip`, 4.8 and 5.5 MB, fetched by `setup-crime-frontier.sh` | Not read by any lane yet | — |
| State budget documents on coverage for unauthorized immigrants: LAO Medi-Cal May Revision 2025; California enacted HHS summaries 2025-26 and 2026-27 and eBudget HHS 2024-25; Illinois HBIA tracking (March 2025); Washington OFM decision package 77936 | `sources/immigration-fiscal/data/external/state_medicaid/{lao_medical_may_revision_2025,hhs_2025-26_Enacted,hhs_2026-27_Enacted,ca_ebudget_2024-25_hhs,il_hbia_tracking_mar2025,wa_ofm_decision_package_77936}.pdf`, text extractions, `agent_findings.json` (agent-extracted figures with quotes, 2026-09-17) | no script reads it; `debt_legacy_2026_09_23` RESULT cites `lao_may.txt` for California's state-only Medi-Cal spending on undocumented enrollees | five `.pdf` files are bot-block or 403 HTML pages: `cbo_emergency_medicaid.pdf`, `cbo_emergency_medicaid_2024.pdf`, `d.pdf`, `dhcs_may2024_local_assistance_estimate.pdf`, `co_jbc_hcpf_figsetting_fy2627.pdf`; the real CBO emergency-Medicaid letter (257,767 bytes) is in `infra/immigration-fiscal/medical_ethnicity_pooled_2026_09_23/_cache/` |

### MCBS-CSPUF-2022 — CMS medical spending by payer, unused-year cross-check

**Source:** Centers for Medicare & Medicaid Services. **Acquired:** 2026-09-28.
**Local:** `infra/immigration-fiscal/validation_medical_2026_09_28/_cache/` (ignored; restorable through the lane's
pinned `acquire.py`).
**Official:** [CMS dataset catalog](https://catalog.data.gov/dataset/medicare-current-beneficiary-survey-cost-supplement).
**Codebook:** `CSPUF2022_Codebook.txt`;
[official codebook](https://data.cms.gov/sites/default/files/2025-01/CSPUF2022_Codebook.txt).
**Size:** ZIP 10,208,378 bytes plus codebook 32,191 bytes; 6,621 records, 134 variables.
**Pins:** data SHA256 `d500832a0d832419f7c5ff23df56d91ee5348bc092d53f0dd7345e01fb699875`; codebook SHA256
`7b7da7f5f7ded9c5c424e5cd3805c4580179d20c0574348e70af052bce71655e`.

**Fields:** `CSP_AGE`, `CSP_SEX`, `CSP_RACE`, `CSP_INCOME`, payer amounts `PAMTCARE`, `PAMTMADV`, `PAMTCAID`, full
weight `CSPUFWGT`, 100 Fay BRR replicate weights.
**Quirks:** no Mexican origin or birthplace; age and income coarse; facility and hospice users excluded; service costs
adjusted; payer tails replaced by tail means; payer-positive is not enrollment; PUF IDs cannot link to other years or
the survey PUF. The chronic-condition field contains a refusal code and is not used. Codebook age and race frequencies
reproduce exactly.
**Used in:** `validation_medical_2026_09_28/analysis.py` and `RESULT.md`.

### In analysis lanes

| Dataset and vintage | Where it is | Use | Limits |
|---|---|---|---|
| AHA Uncompensated Hospital Care Cost Fact Sheet (February 2022; national totals 2000–2020) | [uncompensated_care_2026_09_23](../infra/immigration-fiscal/uncompensated_care_2026_09_23/RESULT.md) `_cache/aha_2020_uncompensated_fact_sheet.pdf` | national uncompensated care at cost, keyed by uninsured exposure (ladder 192) | includes insured patients' bad debt; excludes physicians' and clinics' free care |
| CalHHS open data, Medi-Cal: certified eligibles by age and sex (t1) and aid category (t7), January 2010 – September 2026; status-blind expansion enrollment, June 2026 | [lineage_cost_2026_09_19](../infra/immigration-fiscal/lineage_cost_2026_09_19/RESULT.md) `_cache/{chhs_t7_aid_category_201001_202609.csv,chhs_oae_50plus_06-2026.csv}`; [california_medical_status_2026_09_23](../infra/immigration-fiscal/california_medical_status_2026_09_23/RESULT.md) `_cache/t{1_eligibility_by_age_group_sex,7_eligibility_by_aid_category}_201001_202609.csv`, `_cache/{sb75_children_under19,yae_19_25,ae_26_49,oae_50plus}.csv`, `_cache/updated_072026-aid-category-grouping-schema.pdf`, URLs and hashes in `derived/sources.json` | 50+ expansion enrollment (ladder 159); benchmarks for survey Medi-Cal reporting and status imputation | expansion counts include lawfully present people; monthly stocks against CPS any-time coverage |
| CBO letter to Chairman Arrington on emergency Medicaid for non-US nationals, FY2017–2023 (October 2024) | [lineage_cost_2026_09_19](../infra/immigration-fiscal/lineage_cost_2026_09_19/RESULT.md) `_cache/cbo_arrington_emergency_medicaid_2024-10-02.pdf`; [medical_ethnicity_pooled_2026_09_23](../infra/immigration-fiscal/medical_ethnicity_pooled_2026_09_23/RESULT.md) `_cache/cbo_emergency_medicaid_2024.pdf` (same size) | emergency Medicaid series 2017–2023; bound on the Medicaid line (ladders 159, 206) | cannot separate the unauthorized from other restricted-coverage immigrants |
| CDC WONDER Underlying Cause of Death, single race 2018–2023 (D158): homicide deaths 2019–2023 (XML query results) | [homicide_cost_2026_09_18](../infra/immigration-fiscal/homicide_cost_2026_09_18/RESULT.md) `_cache/wonder_D158_*.xml` | reweights the SHR to recorded homicide deaths (ladder 143) | suppressed small cells; no denominator for age by Hispanic origin |
| CMS Hospital Provider Cost Report (HCRIS) public files 2020–2023, with dictionaries, PRM-2 chapter 40 and S-10 Q&A | [backtest_published_2026_09_28](../infra/immigration-fiscal/backtest_published_2026_09_28/RESULT.md) `_cache/hcris/{CostReport_202{0..3}_Final.csv,catalog.json,dictionary_2022-12.pdf,dictionary_update_2024-03.pdf,prm2_ch40_r18.pdf,s10_ucc_qandas.pdf}`, pins in `derived/sources.json` | Worksheet S-10 uncompensated care by state against the account's key (ladder 256) | state level only; a regional factor cannot be separated from the group's use rate |
| CMS Medicaid LTSS: expenditures and users workbooks CY2019–2022, users and expenditures briefs 2022–2023, rebalancing brief 2023, FFY2020 report (Wayback copies) | [ltss_share_2026_09_23](../infra/immigration-fiscal/ltss_share_2026_09_23/RESULT.md) `_cache/wayback/ltss-expenditures-user-data-{2019-2021,2022}.zip`, `_cache/wayback/ltss-user-character-brief-{2022,2023}.pdf`, `_cache/wayback/ltss-users-taf-method-2023.pdf`, `_cache/wayback/ltssexpenditures2020{.pdf,-app-d.xlsx,-app-e.xlsx}`, CY2023 read from `health_admin_2026_09_20/raw/ltss2023_tables.zip`; [medical_ethnicity_pooled_2026_09_23](../infra/immigration-fiscal/medical_ethnicity_pooled_2026_09_23/RESULT.md) `_cache/{ltss-users-expenditures-category-brief-2022.pdf,ltss-users-expenditures-category-brief-2023.pdf,ltss-rebalancing-brief-2023.pdf}` | Hispanic and Mexican-origin shares of LTSS dollars (ladder 210); nursing-facility bound (ladder 206) | TAF omits California's IHSS in every year |
| CMS Medicaid T-MSIS Analytic Files: DQ Atlas race/ethnicity 2019–2023 Release 1, REI 2020–2022 file, 2023 beneficiary profile | [admin_benefit_keys_2026_09_24](../infra/immigration-fiscal/admin_benefit_keys_2026_09_24/RESULT.md) `_cache/medicaid/raw/{dq_race_20{19..23}_r1.csv,rei_2020_2022.csv,beneficiary_profile_2023.pdf,brief_20{19,20}.pdf}` | CPS Medicaid coverage against TAF enrollment by ethnicity, test only (ladder 217) | Arizona T-MSIS carries almost no Hispanic codes; no spending by ethnicity published |
| CMS Provider Data Catalog, Nursing Home Provider Information (dataset 4pq5-n9py), August 2026 | [care_household_services_2026_09_23](../infra/immigration-fiscal/care_household_services_2026_09_23/RESULT.md) `_cache/NH_ProviderInfo_Aug2026.csv`, `_cache/cms_nh_provider_meta.json` | nursing-home residents per day, to price Medicaid care per resident (ladder 198) | — |
| CMS-64 Medicaid and CHIP Financial Management Report, net expenditures FY2023 and FY2024 (medicaid.gov via Wayback) | [lineage_cost_2026_09_19](../infra/immigration-fiscal/lineage_cost_2026_09_19/RESULT.md) `_cache/{cms_fmr_fy2023.zip,cms_fmr_fy2024.zip,fmr23/,fmr24/,cms64_line27_emergency_fy2023_fy2024.csv}`; [ltss_share_2026_09_23](../infra/immigration-fiscal/ltss_share_2026_09_23/RESULT.md) `_cache/wayback/financial-management-report-fy{2023,2024}.zip` | emergency Medicaid, line 27 (ladder 159); California personal-care dollars missing from TAF (ladder 210) | line 27 has no age, service or enrollee count |
| DHCS Medi-Cal Local Assistance Estimates, May 2022, May 2023, May 2025 and November 2025; DHCS budget highlights FY2025-26 and FY2026-27 | [lineage_cost_2026_09_19](../infra/immigration-fiscal/lineage_cost_2026_09_19/RESULT.md) `_cache/{dhcs_M22_medi-cal_la_estimate.pdf,dhcs_M23_medi-cal_la_estimate.pdf,dhcs_M22.txt,dhcs_M23.txt}`; [california_medical_status_2026_09_23](../infra/immigration-fiscal/california_medical_status_2026_09_23/RESULT.md) `_cache/{M25,N25}-Medi-Cal-Local-Assistance-Estimate.{pdf,txt}`; [california_program_costs_2026_09_23](../infra/immigration-fiscal/california_program_costs_2026_09_23/RESULT.md) `_cache/N25-Medi-Cal-Local-Assistance-Estimate.pdf`, `_cache/DHCS-FY-{2025-26,2026-27}-*-Highlights.pdf` (Wayback copies) | cost of the 50+ expansion (ladder 159); Medi-Cal totals and undocumented enrollees' cost | no UIS caseload total; the November 2025 estimate has no UIS subtotal |
| Florida AHCA hospital patient immigration-status reports (2023 data; 2025) and Texas HHSC GA-46 FY2025 summary and form | [external_benchmarks_2026_09_24](../infra/immigration-fiscal/external_benchmarks_2026_09_24/RESULT.md) `_cache/arm4/fl_ahca_*.pdf`, `_cache/arm4/fl_press_*.pdf`, `_cache/arm4/tx_hhsc_*.pdf`, `_cache/arm4/tx_ga46_*.pdf` | outside check on uncompensated-care keying of the unauthorized (ladder 216) | omit patients who declined to answer; cannot sign the account's error |
| KFF Status of State Medicaid Expansion Decisions, map data (Datawrapper ZJUAA v5, August 2026) | [backtest_published_2026_09_28](../infra/immigration-fiscal/backtest_published_2026_09_28/RESULT.md) `_cache/kff/dw_ZJUAA_5_dataset.csv` | 2023 expansion indicator in the S-10 slope fit (ladder 256) | — |
| LAO The 2026-27 Budget: In-Home Supportive Services (March 2026); CHCF/ATI brief on Medi-Cal HCBS recipients (October 2025) | [ltss_share_2026_09_23](../infra/immigration-fiscal/ltss_share_2026_09_23/RESULT.md) `_cache/web/{2026-27_IHSS_031826,chcf_who_receives_hcbs_2025}.pdf` | IHSS dollars and Latino share of recipients added to TAF (ladder 210) | — |
| MACPAC MACStats Exhibit 22: Medicaid benefit spending per full-year-equivalent enrollee by state and group, FY2023 | [welfare_by_sex_2026_09_29](../infra/immigration-fiscal/welfare_by_sex_2026_09_29/RESULT.md) `_cache/macpac_ex22_fy2023.pdf` | Medicaid value per enrollee by eligibility group (national row) | groups proxied: disabled by SSI receipt, other adults by parenthood |
| MEPS full-year consolidated files 2016–2022 (HC-192 to HC-243) with documentation, and HC-036 pooled linkage file 1996–2024 (AHRQ) | [medical_ethnicity_pooled_2026_09_23](../infra/immigration-fiscal/medical_ethnicity_pooled_2026_09_23/RESULT.md) `_cache/{h192,h201,h209,h216,h224,h233,h243}{dat.zip,doc.pdf,cb.pdf,su.txt}`, `_cache/h36u24{dat.zip,doc.pdf,cb.pdf,su.txt}`; HC-243 Stata also in [lineage_cost_2026_09_19](../infra/immigration-fiscal/lineage_cost_2026_09_19/RESULT.md) `_cache/meps/{h243.dta,h243dta.zip}` | pooled MEPS years for Mexican-origin public medical cost (ladders 159, 206) | civilian non-institutional population only; Mexican origin is self-reported |
| NCHS United States Life Tables 2023 and 2024 by Hispanic origin, race and sex, with table workbooks | [lifetime_longevity_sstiming_2026_09_18](../infra/immigration-fiscal/lifetime_longevity_sstiming_2026_09_18/RESULT.md) `_cache/nvsr{74-06,75-05}.pdf`, `_cache/lt{2023,2024}_Table{01,04,05,06,16,17,18}.xlsx`; [pension_accrual_2026_09_28](../infra/immigration-fiscal/pension_accrual_2026_09_28/RESULT.md) `_cache/lt2024_Table0{2,3}.xlsx` | survival by origin for lifetime balances and benefit accrual (ladders 146, 257) | the pooled Hispanic table is the wrong instrument for Mexican origin |
| NRMP Results and Data: 2025 Main Residency Match (May 2025) | [residency_visas_2026_09_27](../infra/immigration-fiscal/residency_visas_2026_09_27/RESULT.md) `_cache/nrmp_rd_2025.pdf` | match rates and unplaced US graduates against non-citizen IMGs (ladder 244) | "non-U.S. IMG" means non-citizen, including permanent residents |
| NVSS natality (NCHS): public-use files 1980–2010 tabulated from the NBER mirror; 2024 CDC WONDER exports (D149); Births: Final Data for 2010 and 2023 | [ir5_fraud_and_cohorts_2026_09_27](../infra/immigration-fiscal/ir5_fraud_and_cohorts_2026_09_27/RESULT.md) `_cache/{natality_counts_r1.json,natality_counts_r2.json}`, NBER dictionaries `_cache/dct/natality{1980..2012}.dct`, `_cache/docs/` (raw files not held); [backtest_admin_totals_2026_09_28](../infra/immigration-fiscal/backtest_admin_totals_2026_09_28/RESULT.md) `_cache/wonder_2024_{state_all,state_x_origin,state_x_mexico_born,payer_x_origin,payer_mexico_born}.tsv`; [demo_momentum_2026_09_16](../infra/immigration-fiscal/demo_momentum_2026_09_16/RESULT.md) `_cache/nvsr{61-01,74-01}.pdf` | IR-5 parent cohorts (ladder 242); Medicaid-paid births by state (255); TFR by origin (88) | 2005–10 births by mother's birthplace not public; WONDER suppresses 1–9 births |
| State reports on unauthorized seniors' coverage: California LAO report 5010 (March 2025), Illinois HFS HBIS tracking (March 2026) | [lineage_cost_2026_09_19](../infra/immigration-fiscal/lineage_cost_2026_09_19/RESULT.md) `_cache/{lao_5010_senior_caseload_2025-03.pdf,il_hfs_hbis_tracking_2026-03.pdf}` | 65+ share of California's expansion; Illinois HBIS enrollment and cost (ladder 159) | LAO's 65+ share applies a 2021–22 age mix to later enrollment |

## Public finance and tax

| Dataset and vintage | Where it is | Use | Limits |
|---|---|---|---|
| CBO, federal budget effects of the immigration surge, 2024 | `sources/immigration-fiscal/data/cbo/60569-immigration-federal.pdf` | Federal budget and macro effects of the recent surge | Aggregate; surge arrivals only |
| CBO, state and local effects of the surge, 2025 | `sources/immigration-fiscal/data/cbo/61256-immigration-state-local.pdf` | State and local taxes, spending and crowding | Surge-specific, not a model of the settled stock |
| ITEP, tax payments by undocumented immigrants, 2024 | `sources/immigration-fiscal/data/itep/ITEP-Tax-Payments-by-Undocumented-Immigrants-2024.pdf`; structured tables `itep_table_*.tsv` | State-by-state tax contributions | Taxes only, no spending side |
| IRS Data Book table | `sources/immigration-fiscal/data/irs/24dbs01t02nr.xlsx` | Tax-filing context | Not immigrant-specific |
| SSA Actuarial Note 151 | `sources/immigration-fiscal/data/ssa/actuarial_note_151.pdf` | Unauthorized workers' payroll contributions | Aggregate only |
| IRS SOI complete 2023 Tables 1.2 and 1.4; 2022 tables and the June 2026 Publication 4801 | `same_year_tax_2026_09_20/_cache/`; [source lock](../infra/immigration-fiscal/same_year_tax_2026_09_20/source_lock.json) | 19 AGI bands: return counts, AGI, taxable income, tax after nonrefundable credits, total and W-2 wages, in thousands | Publication 4801 p. 9 repeats 2022 totals under a 2023 heading, so use the year-specific tables; tax liability, collections and payroll stay distinct |
| SSA 2025 Annual Statistical Supplement 4.B10 and 4.B12, income 2023 | [Pinned primary transcription](../infra/immigration-fiscal/same_year_tax_2026_09_20/ssa_sources.json); direct HTTP returned 403, so the official page was read through a web tool | OASDI and HI wage and self-employment amounts by geography; domestic-scope diagnostics | Preliminary 1% CWHS estimates, no origin; removing the territories still does not match every CPS population or compensation boundary |
| BEA NIPA Sections 1 and 3 (`Section1All_xls.xlsx`, `Section3All_xls.xlsx`, August 26, 2026 vintage) | `sources/immigration-fiscal/data/external/bea_nipa/`; hashes enforced by `backcast.py` and pinned read-only by the macro lane | Tables 3.1 receipts, 3.2, 3.3, 3.12 benefits by program, 3.13 subsidies, 3.17 consumption by function, 3.18B and 1.1.9 deflator, 2005–2025, for the back-cast; the [macro reconciliation](immigration-macro-reconciliation-2026-09-19.md)'s current/capital, fiscal/calendar and grant boundaries | National totals, no origin dimension; Table 3.19 ends in 2023 |
| BEA NIPA Section 7, Table 7.1 midperiod population, 1929–2025 | `historical_backcast_2026_09_20/_cache/Section7All_xls.xlsx`, 1,003,641 bytes, SHA256 `ce107c8ce92393613c0abae38156afcfaef8ab571eedf0302dc09ca44738b9ef`, [BEA](https://apps.bea.gov/national/Release/XLS/Survey/Section7All_xls.xlsx), published 2026-08-26 | Resident denominator for per-capita national series | 340.095m in 2024 against the account's 340.111m; the back-cast levels it to the account |
| BEA SAINC35, state transfer receipts, 1929–2024 | `sources/corpus/bea_data/SAINC/SAINC35__ALL_AREAS_1929_2024.csv`, recovered and hash-matched 2026-09-20 | Gross transfer receipts by GeoFIPS × LineCode × year, in thousands of dollars ([BEA regional data](https://www.bea.gov/data/economic-accounts/regional)) | 780 hierarchy checks across 60 geographies balance in 2024; nested and memorandum lines overlap; neither recipient nativity nor the tax side is observed |
| USAspending enforcement extracts; FY2024 DHS Files A and B, SF133 and Treasury | `sources/immigration-fiscal/data/usaspending/`; [FY2024 reconciliation](../infra/immigration-fiscal/detention_reconciliation_2026_09_20/README.md) | Earlier obligations series plus complete September 2024 account and activity outlays: 587 File A and 10,956 File B rows; all 35 selected ICE accounts reconcile | September cumulative, not monthly flows; ERO is broader than custody; gross and net differ. The linked lane pins 11 public originals, 14,840,772 bytes, including the local-finance controls |
| Census 2024 state and local individual government finance files | [Acquired 2026-09-20, pins and probe](../infra/immigration-fiscal/detention_reconciliation_2026_09_20/LOCAL_FINDINGS.md); official public-use ZIP, 4,267,040 bytes, with methodology and classification | 511,362 finance records and 24,520 government IDs; broad functional expense and intergovernmental revenue codes | No ICE-purpose expenditure or receipt join; local years differ from federal FY2024; IDs and codes verified, amounts not yet aggregated (they need the full layout documentation) |
| NAS, The Economic and Fiscal Consequences of Immigration (NAP 23550) | Two PDFs with that title: `sources/immigration-fiscal/data/external/nas_2016/23550.pdf` (643 pages, 7,195,875 bytes, SHA256 `c6fffc8f764e257b…`; NAP download by the operator, September 22, 2026) and `external/lifetime/nas/nas_2017_immigration_economic_fiscal_full.pdf` (509 pages, 5,385,001 bytes; read 2026-09-05) | Chapters 7–8 fiscal accounts (static 2011–2013 scenarios; 75-year net present values by education and generation) and the chapter 12 framework the complete annual account cites | Take every NAS-attributed number from the 643-page file and parse tables from it, never from a summary (a Firecrawl extraction once fabricated an SSA table). Keep price year, age, public-goods allocation, generations and baseline emigration explicit. Not yet used in a lane |
| NYC service census, budget and school tabs | `frontier_execution_2026_09_17/raw/local/`, 13 snapshots, [URLs and hashes](../infra/immigration-fiscal/frontier_execution_2026_09_17/local/source_manifest.json) | Calendar join of the monthly shelter census and fiscal-year spending | Two official census charts differ; school tabs cannot establish attendance or capacity effects |
| NYC program financing and schools, FY2023–FY2026 | `.scratch/clarity-next-20260905/local/`: 9 official HTML snapshots, 3,016,301 bytes, with a source manifest and a separately labeled school-guide transcription | `analyze_recent_local_costs.py`: FY2023–25 financing, FY2026 partial cash, household-nights, actual enrollment | Gross service costs, grants and cash receipts are distinct; no migrant-specific marginal cost |
| Receiver-city migrant costs | `sources/immigration-fiscal/data/external/stage5_net_negative/receiver/receiver_city_migrant_costs.csv`; warehouse table `receiver_city_migrant_costs`; shelter and financial-administration costs by unit in [`migrant_shelter_costs_2026_09_23`](../infra/immigration-fiscal/migrant_shelter_costs_2026_09_23/RESULT.md) | Local fiscal shock by city | Assembled from fragmented city reports |
| Census Annual Survey of State Government Tax Collections FY2024, detailed table (transposed) | `sources/immigration-fiscal/data/external/census_stc/FY2024-STC-Detailed-Table-Transposed.xlsx` | no script reads it | state government taxes only; no local taxes |
| OMB Historical Tables, FY2027 Budget: Tables 2.1, 2.4, 2.5, 3.1 and 3.2 | `sources/immigration-fiscal/data/external/omb_hist_fy2027/hist{02z1,02z4,02z5,03z1,03z2}_fy2027.xlsx` (Table 3.2 same size as `debt_legacy_2026_09_23/_cache/hist03z2_fy2027.xlsx`) | read by `debt_legacy_2026_09_23` (`debt_legacy.py`) and `winners_losers_2026_09_24` (`winners_losers.py`); cited in `cj_use_allocation_2026_09_23` | — |
| paymentaccuracy.gov program pages saved as text: SSI, unemployment insurance, EITC, ACTC, Medicaid, Medicare fee-for-service, SNAP | `sources/immigration-fiscal/data/external/paymentaccuracy/*.txt` (7 files) | no script reads it; `ledger_absolute_2026_09_17/params/PARAMS.md` cites paymentaccuracy.gov FY2024 figures | web-page text, not data tables; pages mix reporting years FY2021–FY2026 |
| USDA FNS SNAP state participation and benefits, FY1969–FY2026 (yearly workbooks; state detail from FY1989), SNAP and WIC national annual summaries, WIC state participation | `sources/immigration-fiscal/data/usda/{snap-state-fy69tocurrent.zip,snap-annualsummary.xlsx,wic-summary.xlsx,wic-state-participation.xlsx}` | no script reads it; a 2026-09-17 review note (`all_age_ledger_2026_09_17/derived/review/allage-calibration-readiness-20260917.md`) proposed it as a SNAP control | `snap_participation.xlsx` and `wic_participation.xlsx` are the same FNS "Page Not Found" HTML page, not workbooks |
| CBO, *The Long-Term Budget Outlook Data: 2026 to 2056* (pub 62044, February 2026; data workbook only, no report this year) | `sources/immigration-fiscal/data/external/stage3/cbo/ltbo_2026/62044-2026-LTBO.xlsx`, 121,371 bytes, hash in `ACQUIRED.md` | read by `closed_budget_2026_10_06` (`trust_funds.py`): sheet 1a Social Security revenues and outlays 2026–2056 for the post-depletion shortfall | CBO projects HI exhaustion in 2052, so HI adds nothing inside a 2056 window on CBO's reading |
| 2026 OASDI and Medicare Trustees Reports, with OCACT Actuarial Note 2026.3 | `sources/immigration-fiscal/data/external/stage3/ssa/trustees_2026/{tr2026.pdf,tr2026.txt,an2026-3.pdf}`, `sources/immigration-fiscal/data/external/stage3/cms/trustees_2026/{mtr2026.pdf,mtr2026.txt}`; hashes in each `ACQUIRED.md` | `trust_funds.py` parses OASDI Table IV.B3 and HI Tables III.B7 × V.B2 with gates (83% payable at 2034; HI 89% at 2033, 93% at 2100); the pension lane's 2026 rerun | Intermediate assumptions only; the text layer is `pdftotext -layout` and the parser keys on table headings |
| Published fiscal gaps: Auerbach & Gale, *An Update on the Federal Budget Outlook* (Brookings/TPC, March 2026); CBO letter on alternative scenarios (pub 62758, 24 September 2026); Treasury *Financial Report* FY2025, Note 24 and RSI | `sources/immigration-fiscal/data/external/stage3/brookings/auerbach_gale_2026/`, `sources/immigration-fiscal/data/external/stage3/cbo/alt_scenarios_62758/`, `sources/immigration-fiscal/data/external/stage3/treasury/financial_report_fy2025/` (PDFs with text layers) | `closed_budget_2026_10_06/sources.json` quotes each gap with page and convention | Every gap pays scheduled Social Security and Part A benefits after depletion; no macro feedback except CBO's |
| DHS public-charge final rule (91 FR 45324, 2026-07-20; FR doc 2026-14539) and its RIA table images (Tables IV.11–IV.13, IV.15–IV.16) | `sources/immigration-fiscal/data/external/stage3/federal_register/public_charge_2026_final_rule/`: 154-page PDF, five `ER20JY26.*.png` (transparent; flatten on white to read) | `public_charge_share_2026_10_07`: DHS's federal dollars by programme and rate, transcribed into the script with a sum gate | Tables exist only as images; DHS's recipient counts are built from national shares, not microdata |
| CBO cost estimate of P.L. 119-21, relative to the January 2025 baseline (61570) and the Senate enforcement baseline (61569) | `sources/immigration-fiscal/data/external/stage3/cbo/pl119_21_estimate/`, two workbooks via Wayback `id_` captures (cbo.gov is walled) | Section-level outlays and revenues by fiscal year, 2025–2034; the noncitizen eligibility sections (10108, 71109, 71110, 71201, 71301, 71302) | No narrative PDF; the child-credit parent-SSN rule is bundled in §70104 and not priced alone; no split by origin |
| Census *Research Matters* nonresponse-bias posts on the 2025 and 2026 CPS ASEC (Bee & Rothbaum); Fox & Jensen, SEHSD WP 2026-16 (Vintage 2025 controls) | `sources/immigration-fiscal/data/external/stage3/census/research_matters_nonresponse/` (pages and Figures 3–6 as JPEG), `sources/immigration-fiscal/data/external/stage3/census/sehsd_wp2026_16/` (PDF, Tables 1–3) | Survey-to-adjusted household income ratios by percentile and group (2025: Hispanic median +3.8%); Hispanic persons +0.88% under the 2025 controls | Ratios are published only as figures; the 2026 post has no group split; no nativity split |
| Retiree health (OPEB): Pew, *Do States Have Enough Saved for Retiree Health Care Benefits?* (April 2023); CRR State and Local Pension brief 48 (2016); Reason Foundation OPEB liability survey (2021); DoD Medicare-Eligible Retiree Health Care Fund, FY2024 Agency Financial Report | `sources/immigration-fiscal/data/external/stage3/{pew/opeb_2023,crr/slp48,reason/opeb_2021,dod/merhcf_afr_fy2024}/`, hashes in each `ACQUIRED.md` | [public_pension_legacy_2026_10_07](../infra/immigration-fiscal/public_pension_legacy_2026_10_07/RESULT.md) (`opeb_national.py`): the states' GASB 75 normal cost over contributions (1.20, FY2019), its scaling to all governments, the military retirees' fund | State plans only, FY2019; GASB 75 discounts unfunded plans at municipal-bond rates; the Reason page is HTML |
| CBO, estimated effects of selected health coverage policies (pub 61734, letter of 2025-09-18), data workbook | `sources/immigration-fiscal/data/external/stage3/cbo/ptc_extension_61734/61734-data.xlsx`, a Wayback `id_` capture (cbo.gov returns 403), hash in `ACQUIRED.md` | [post2024_law_2026_10_07](../infra/immigration-fiscal/post2024_law_2026_10_07/RESULT.md) (`post2024_law.py`): net cost of the expanded premium tax credit, FY2027 $31.9bn, FY2028 $30.4bn | Baseline through 2025-08-22, after P.L. 119-21; the letter's PDF capture was empty; no split by origin |

The [four fiscal checks](immigration-four-fiscal-checks-2026-09-20.md) of September 20 have recipes for
[school](../infra/immigration-fiscal/school_enrollment_2026_09_20/README.md),
[tax](../infra/immigration-fiscal/same_year_tax_2026_09_20/README.md),
[health](../infra/immigration-fiscal/health_admin_2026_09_20/README.md) and
[national coverage](../infra/immigration-fiscal/national_coverage_2026_09_20/README.md). No restricted linkage or
administrative Mexican-origin tax or health file was acquired for them.

### CENSUS_SLGF_2024_AND_2022 — observed state and local finance

US Census public aggregates, [FY2024 release, July 2026](https://www.census.gov/data/datasets/2024/econ/local/public-use-datasets.html);
[API documentation](https://www.census.gov/data/developers/data-sets/govslocalfin.html). Acquired 2026-09-19. Government
type 001; 50 states and DC, plus independent US totals. Ignored cache:
`infra/immigration-fiscal/macro_closure_2026_09_19/_cache/`. Public queries, byte counts, rows and SHA256 are in the
[pinned manifest](../infra/immigration-fiscal/macro_closure_2026_09_19/census_sources.json).

Schema: geography × YEAR × GOVTYPE × AGG_DESC; AMOUNT in **thousands of dollars**, with amount flags and CVs kept. Four
data responses plus variables metadata and the FY2024 methodology. Repeated predicate columns must agree before
collapsing. Omitted state values become zero at published precision only after the nonnegative reported cells exhaust
the independent US control; flagged values fail.

Use: G/P functions, mapped fees, and combined state and local corporate and selective-sales taxes. The
[generator contract](../infra/immigration-fiscal/macro_closure_2026_09_19/README.md) specifies the codes and the Census
2024 population join, excluding Puerto Rico. Fiscal year ends and survey uncertainty differ across states; this is not
ethnic microdata.

### GFD_FULL_LOCAL_FINANCE — Government Finance Database

**Source:** Pierson, Hand and Thompson's recoding of Census government finance. **Recovered:** 2026-09-20 from the
existing Modal `gfd` volume.
**Local:** `sources/immigration-fiscal/data/external/government_finance_database/gfd_entire.zip`.
**Upstream:** [recorded full archive](https://drive.google.com/uc?export=download&id=1FtZQR34S69D2DnOeM_agRTeIVwojbaAK).
**Size:** 340,921,174 bytes; all members pass `unzip -tqq`.
**SHA-256:** `86cf9b3adecbc1309bf29c9e8d1ff6a960793fd6381e30170263fe05e1d9d7e0`.
**Codebook:** the archive holds the database appendix, the PLoS paper, the 2006 classification manual and the 2017
individual-unit disclaimer beside the full CSV.
**Fields/use:** government and year identifiers, county geography and direct expenditure on education, police,
corrections, judiciary, welfare and health;
[county aggregation recipe and limits](../infra/immigration-fiscal/local_spending_composition_2026_09_18/README.md).
The county subset and the historical school-finance supplement are separate artifacts, and this archive can regenerate
the subset. It carries no consular-ID migration treatment.

### BEA_CAINC4_CORPUS_20260920 — county income components

**Source/acquired:** US BEA; copied read-only from the operator's external corpus on September 20, 2026.
[Official release route](https://apps.bea.gov/regional/zip/CAINC4.zip). CSV 29,012,947 bytes; full source 1969–2024,
joined subset 2011 and 2013–2022.
**Local:** `infra/immigration-fiscal/causal_evidence_2026_09_20/raw/county_outcomes/raw/bea_cainc4/`.
[Pinned hash](../infra/immigration-fiscal/causal_evidence_2026_09_20/SOURCES.json),
[acquisition and verification](../infra/immigration-fiscal/causal_evidence_2026_09_20/CORPUS.md).
**Variables:** GeoFIPS and year, population (line 20), workplace earnings 35, social-insurance contributions 36,
residence adjustment 42, net residence earnings 45, transfers 47, wages 50. Population is persons; monetary fields are
thousands of nominal dollars.
**Quirks/use:** transfers include net business transfers, not only government benefits. Virginia's combined areas are
excluded from exact county joins; historical boundaries and the Connecticut and Alaska mismatches remain unresolved. No
ethnicity or policy treatment. Used in the [policy evidence memo](immigration-policy-causal-evidence-2026-09-20.md).

### IRS_COUNTY_NOAGI_2011_2013_2022 — returns, income and tax liability

**Source/acquired:** IRS SOI; 11 corpus CSVs copied September 20, 2026, 43,107,945 bytes; 11 official annual codebooks
acquired and read. [Official catalog](https://www.irs.gov/statistics/soi-tax-stats-county-data).
**Local:** the same lane, `raw/county_outcomes/raw/irs_soi/county/`; guides under `raw/county_outcomes/codebooks/`. All
23 combined BEA and IRS inputs have hashes and URLs in
[SOURCES.json](../infra/immigration-fiscal/causal_evidence_2026_09_20/SOURCES.json).
**Variables:** state and county FIPS, AGI_STUB=0 total rows, N1 returns, A00100 AGI, A00200 wage income, A06500
income-tax amount, N00200/N06500 counts. The guides confirm amounts in thousands; later A06500 labels specify after
credits.
**Quirks/use:** tax liability is not net federal receipts; refunds and other taxes stay distinct. 2012 is absent. A
zero amount with zero returns is disclosure-ambiguous and masked; positive cells can also omit protected amounts. Filing
windows and ZIP-derived geography differ from BEA concepts. The outer county-year join keeps 34,733 rows, unmatched
records included, not a balanced national panel. No origin, nativity or legal-status field.

### Stage 5 local-cost context

| Dataset and vintage | Where it is | Use | Limits |
|---|---|---|---|
| CMS Medicaid financial management | `sources/immigration-fiscal/data/external/stage5_net_negative/cms/medicaid_financial_management.csv` | State Medicaid spending by service | — |
| BEA regional price parities | `sources/immigration-fiscal/data/external/stage5_net_negative/bea/` | Deflating local costs | — |
| SNAP state panel FY2023 | `sources/immigration-fiscal/derived/stage5/snap_state_2023.csv`, from the NDB public workbook in the USDA zip | Average households, persons and benefits by state | — |
| State stage-5 context 2023 | `sources/immigration-fiscal/derived/stage5/state_stage5_context_2023.csv` | RPP, Medicaid, English learners, SAFMR and SNAP by state | Use the context warehouse's 24-column table; the lifetime warehouse's copy is stale |
| Other stage-5 tables | `sources/immigration-fiscal/derived/stage5/`: SAFMR by ZIP, county, PUMA and state 2025; state EL/LEP 2018; state per-pupil spending 2023; SAIPE state school poverty 2023; ACS foreign-born school-age and immigrant-health state summaries 2023; the CMS Medicaid state panel; HUD PIT by CoC; OHSS state immigration 2023; the Gould asylum-shelter attribution 2022–2024 | Loaded into the context warehouse by `build_stage5_local_cost_context.py` | The loader prints DEGRADED for each missing input CSV |

The June [net-negative dataset frontier](immigration-net-negative-dataset-frontier-2026-06-15.md) has the tier list and
disconfirmation requirements behind this layer; it is a historical snapshot.

### In analysis lanes

| Dataset and vintage | Where it is | Use | Limits |
|---|---|---|---|
| BEA Fixed Assets Accounts Section 7, government fixed assets 1925–2024, and NIPA Section 5 workbook, with table registers | [school_capital_return_2026_09_26](../infra/immigration-fiscal/school_capital_return_2026_09_26/RESULT.md) `_cache/{fa_Section7All_xls.xlsx,fa_TablesRegister.txt,nipa_Section5All_xls.xlsx,nipa_TablesRegister.txt}`, URLs and hashes in `derived/sources.csv` | stock and depreciation of K-12 capital for its imputed return (ladder 231) | NIPA has no education CFC; BEA does not measure land under schools |
| BEA NIPA annual series flat file 1929–2025, with series and table registers | [backtest_published_2026_09_28](../infra/immigration-fiscal/backtest_published_2026_09_28/RESULT.md) `_cache/bea/{NipaDataA.txt,SeriesRegister.txt,TablesRegister.txt}` | 2024 federal and state-local splits of corporate, excise and production taxes (ladder 256) | — |
| BEA, Effects of Selected Federal Pandemic Response Programs on Personal Income, 2022Q4 third estimate (March 2023) | [backcast_pandemic_measured_2026_09_28](../infra/immigration-fiscal/backcast_pandemic_measured_2026_09_28/RESULT.md) `_cache/bea_pandemic_2022q4_3rd.pdf` | 2020–2021 pandemic payments inside the refundable-credit line (ladder 251) | March 2023 vintage; later revisions land in the rest of the line |
| California CDTFA taxable sales by county and city, 2015–2025 (open data) | [vending_restaurants_2026_09_24](../infra/immigration-fiscal/vending_restaurants_2026_09_24/RESULT.md) `_cache/cdtfa/Taxable_Sales_{Cities,Counties}_*.json` | restaurant taxable sales before and after vending legalization (ladder 223) | some cities lack a 2024 quarter; disclosure-flagged units dropped |
| California DOF budget summaries and program detail (5180 DSS, 8660 CPUC), FY2025-26 to FY2026-27; LAO Medi-Cal and budget reports | [california_program_costs_2026_09_23](../infra/immigration-fiscal/california_program_costs_2026_09_23/RESULT.md) `_cache/ebudget.ca.gov_{2025-26,2026-27}_pdf_*BudgetSummary_*.pdf`, `_cache/op_eb_{5180,8660}_{gb,en}2627.pdf`, `_cache/lao_{4423,5075,5083,5092,5126,5146}.html`, `_cache/{Medi-Cal-in-the-May-Revision-051925,26-27-Medi-Cal-Outlook-111925}.pdf` | state HHS and Medi-Cal totals, General Fund against total funds | LAO: the estimate "does not fully breakout spending for these enrollees" |
| California Elections Data Archive (CEDA), local ballot measures 1998–2024 (justindbk/ceda mirror of the CSUS portal) | [school_flight_2026_09_18](../infra/immigration-fiscal/school_flight_2026_09_18/RESULT.md) `_cache/ceda/CEDA{1998..2024}Data.xls[x]` | school bond and parcel-tax votes against district Hispanic share (ladder 141) | — |
| California program reports: FTB CalEITC (TY2023, TY2024) and Golden State Stimulus I and II (2022), CSAC Cal Grant, CDSS May Revision 2026, CPUC LifeLine, CDI Low Cost Auto, Los Angeles County letters | [california_program_costs_2026_09_23](../infra/immigration-fiscal/california_program_costs_2026_09_23/RESULT.md) `_cache/op_*.{pdf,html}`, URLs in `_cache/other_programs_notes.md` | eligibility and cost of non-Medi-Cal programs open regardless of status | ITIN share of CalEITC not broken out; Cal Grant offer counts only, no dollars |
| CBO, The Distribution of Household Income, 2022 (61911, January 2026), with researcher data 1979–2022; 2021 edition (60341) | [distribution_weights_2026_09_23](../infra/immigration-fiscal/distribution_weights_2026_09_23/RESULT.md) `_cache/sources/cbo_61911_report.pdf`, `_cache/sources/cbo_61911-additional-data-for-researchers.zip`, unpacked `_cache/sources/cbo_61911/…`; [external_benchmarks_2026_09_24](../infra/immigration-fiscal/external_benchmarks_2026_09_24/RESULT.md) `_cache/arm1/61911-{Household-Income-2022.pdf,additional-data-for-researchers.zip,data-underlying-figures.xlsx,supplemental-data.xlsx}`, `_cache/arm1/cbo61911_data/…`, `_cache/arm1/60341-income.pdf` | federal tax shares by income group (ladder 194); tax-key benchmark (ladder 216) | 2022 shares applied to 2024 totals; tax-record income differs from the top-coded CPS |
| Census of Governments 2022, state and local government finances by state, Table 1 | [assumption_explorer_2026_09_21](../infra/immigration-fiscal/assumption_explorer_2026_09_21/README.md) `_cache/slf2022.xlsx`; [ledger_residual_agg_2026_09_16](../infra/immigration-fiscal/ledger_residual_agg_2026_09_16/RESULT.md) `_cache/22slsstab1.xlsx`; [school_capital_return_2026_09_26](../infra/immigration-fiscal/school_capital_return_2026_09_26/RESULT.md) `_cache/cog_22slsstab1.xlsx` (all same SHA-256) | cross-state spending elasticities; general-services charges; education capital outlay (ladder 231) | a cross-section shows long-run scale, not a measured response to this group |
| Census of Governments FY2022 Individual Unit File (state and type file) | [receipt_side_long_run_2026_09_28](../infra/immigration-fiscal/receipt_side_long_run_2026_09_28/RESULT.md) `_cache/census_2022_individual_unit_file.zip` | school districts' share of local property tax, 40.8% (ladder 253) | — |
| Census Value of Construction Put in Place (C30), state and local public construction, 1993–2025 | [school_capital_return_2026_09_26](../infra/immigration-fiscal/school_capital_return_2026_09_26/RESULT.md) `_cache/{c30_state.xlsx,c30_stateha.xls,c30_stateha1.xls,c30_stateha2.xlsx}` | educational construction's share of public investment (ladder 231) | — |
| GAO-24-105833, federal fraud loss estimate from FY2018–2022 data | [fraud_by_citizenship_2026_09_24](../infra/immigration-fiscal/fraud_by_citizenship_2026_09_24/RESULT.md) `_cache/refs/gao-24-105833.pdf` | scales noncitizens' fraud-loss share to $233–521bn a year (ladder 214) | GAO: its 3–7% "should not be applied at the agency or program level" |
| HUD FY2026 Congressional Justifications (Public Housing Fund, Tenant-Based Rental Assistance) and FY2026 outlay consistency table | [main_case_candidate_2026_09_28](../infra/immigration-fiscal/main_case_candidate_2026_09_28/RESULT.md) `_cache/hud/{2026_CJ_Program_PH_Fund.pdf,2026_CJ_Program_TBRA.pdf,FY_26_Outlay_Table_Consistency.pdf}` | public housing's FY2024 operating subsidy, sizing the transfer consolidation | Section 8 paid to housing authorities as landlords is unpublished detail |
| IRS SOI individual income tax statistics: Table 1.2 by AGI and marital status (tax years 2022–2023); state data (tax year 2023) | [tax_key_heldout_2026_09_28](../infra/immigration-fiscal/tax_key_heldout_2026_09_28/RESULT.md) `_cache/{22in12ms.xls,23in12ms.xls}`, pins in `_cache/acquisition.json`; [backtest_admin_totals_2026_09_28](../infra/immigration-fiscal/backtest_admin_totals_2026_09_28/RESULT.md) `_cache/23in55cmcsv.csv`, `_cache/soi_23incmdocguide.doc` | held-out test of the income-tax key (ladder 249); state EIC and ACTC back-tests (ladder 255) | no nativity or ancestry; the group's within-bin shares rest on CPS |
| ITEP, Who Pays? 7th edition (January 2024), report and appendices A–F | [distribution_weights_2026_09_23](../infra/immigration-fiscal/distribution_weights_2026_09_23/RESULT.md) `_cache/sources/itep_ITEP-Who-Pays-7th-edition.{pdf,txt}`, `_cache/sources/itep_APPENDIX-{A…F}-Who-Pays-7th-Edition.{pdf,txt}` | state and local tax rates by income group, Appendix A (ladder 194) | rates for non-elderly families are applied to all ages |
| Lincoln Institute Significant Features of the Property Tax: 2024 limit flags; 2022 assessment, levy and rate limit workbooks | [receipt_side_long_run_2026_09_28](../infra/immigration-fiscal/receipt_side_long_run_2026_09_28/RESULT.md) `_cache/lincoln/{report_2024_rows.json,recs2024.json,assessment_limits_2022-3.xlsx,levy_limits_2022.xlsx,rate_limits_2022-2.xlsx}`, curated `inputs/lincoln_limits_2024.csv` | property-tax limit regime by state for the long-run response (ladder 253) | — |
| National Taxpayer Advocate, 2024 Annual Report to Congress, Research Report 3 (ITIN filers, IRS data to TY2022) | [itin_credits_student_aid_2026_09_23](../infra/immigration-fiscal/itin_credits_student_aid_2026_09_23/RESULT.md) `_cache/ARC24_RR_Research_3_wb.{pdf,txt}`; [external_benchmarks_2026_09_24](../infra/immigration-fiscal/external_benchmarks_2026_09_24/RESULT.md) `_cache/arm3/ARC24_RR_Research_3_wb.pdf` (same size) | ITIN return counts, taxes and nonrefundable credits, TY2021–2022 (ladder 216) | ITIN returns by state and filing country, not by birth or citizenship |
| OMB budget data: Historical Tables 3.2, 7.1 and 12.3 (FY2027 Budget); Public Budget Database outlays (FY2025 and FY2027 Budgets) | [debt_legacy_2026_09_23](../infra/immigration-fiscal/debt_legacy_2026_09_23/RESULT.md) `_cache/hist{03z2,07z1,12z3}_fy2027.xlsx`; [ledger_absolute_2026_09_17](../infra/immigration-fiscal/ledger_absolute_2026_09_17/RESULT.md) `_cache/{outlays_fy2027,omb_hist12z3_fy2027}.xlsx` (Table 12.3 same size as debt_legacy's); [ir5_adjusters_2026_09_27](../infra/immigration-fiscal/ir5_adjusters_2026_09_27/RESULT.md) `_cache/ptc/BUDGET-2025-DB-2.xlsx` | interest rates and grant types (ladder 207); FY2024 outlays (130); premium tax credit (247) | BEA grants by function differ from OMB programme classifications |
| SNAP Quality Control public-use file FY2024 with technical documentation (USDA FNS, snapqcdata.net) | [admin_benefit_keys_2026_09_24](../infra/immigration-fiscal/admin_benefit_keys_2026_09_24/RESULT.md) `_cache/snap/{qcfy2024_csv.zip,FY-2024-Tech-Doc.pdf,techdoc.txt}` | administrative Hispanic SNAP share against CPS reporting (ladder 217) | codebook advises against national ethnicity tabulations; 16.55% lack race/ethnicity |
| SSA FY2025 Agency Financial Report (Statements of Social Insurance) and CMS Financial Report FY2025 | [pension_accrual_2026_09_28](../infra/immigration-fiscal/pension_accrual_2026_09_28/RESULT.md) `_cache/{ssa_afr2025_fin,cms_fr2025}.pdf` | closed-group Statement of Social Insurance check on the accrual ratio (ladder 257) | the Statement of Social Insurance stops in 2099 |
| SSA OASDI Trustees Report 2025 (and 2026 section VI.D), Medicare Trustees Report 2025, SSA Actuarial Notes 2025.1, 2025.3 and 2025.7, OCACT letter on the OBBBA (August 2025), SSA wage and trust fund pages | [pension_accrual_2026_09_28](../infra/immigration-fiscal/pension_accrual_2026_09_28/RESULT.md) `_cache/{tr2025,mtr2025,an2025-1,an2025-3,ocact_obbba_wyden_20250805}.pdf`; [lifetime_longevity_sstiming_2026_09_18](../infra/immigration-fiscal/lifetime_longevity_sstiming_2026_09_18/RESULT.md) `_cache/{ssa_tr2025_IVA,tr2025_vid,tr2026_vid,ssa_awi,ssa_cbb,ssa_table4a3}.html`, `_cache/ssa_an2025-7.pdf`; Medicare report same size in [ir5_adjusters_2026_09_27](../infra/immigration-fiscal/ir5_adjusters_2026_09_27/RESULT.md) `_cache/law/trustees_2025.pdf`; Actuarial Note 151 copies (`lifetime_longevity_sstiming_2026_09_18/_cache/note151.pdf`, `onbooks_share_2026_09_23/_cache/note151_wb.pdf`) are the same size as the register's `ssa/actuarial_note_151.pdf` | OASDI and HI accrual, payable benefits and money's-worth checks (ladders 146, 257) | — |
| SSA statistical compilations: OASDI beneficiaries by state and county 2024, SSI Annual Statistical Report 2024, Annual Statistical Supplement 2025 Table 7.B7 | [backtest_admin_totals_2026_09_28](../infra/immigration-fiscal/backtest_admin_totals_2026_09_28/RESULT.md) `_cache/ssa_{oasdi_sc24,ssi_asr24,supplement2025_7b}.xlsx` | state Social Security and SSI payments to back-test dollar keys (ladder 255) | SSI total includes California's state supplement, which the line excludes |
| State budget documents, fiscal notes and agency reports on status-blind programs, 2021–2026: CO, CT, DC, IL, MA, ME, MN, NJ, NY, OR, RI, UT, VT, WA | [state_programs_unauthorized_2026_09_23](../infra/immigration-fiscal/state_programs_unauthorized_2026_09_23/RESULT.md) `_cache/{co,ct,dc,il,ma,me,mn,nj,ny,or,ri,vt,wa}_*.pdf`, `_cache/ut_lfa_sb217_fiscal_note.html` | state and local cost of status-blind programs outside California | no state except California publishes a status-specific figure |
| State ITIN tax-credit reports: Colorado DOR Tax Profile and Expenditure Report 2024; Washington Working Families Tax Credit 2025; California FTB Golden State Stimulus II 2022 | [itin_credits_student_aid_2026_09_23](../infra/immigration-fiscal/itin_credits_student_aid_2026_09_23/RESULT.md) `_cache/co_tper_2024.{pdf,txt}`, `_cache/WFTC_2025-LegReport.{pdf,txt}`, `_cache/ftb_gss2_report_2022.{pdf,txt}`; the FTB report also in [california_program_costs_2026_09_23](../infra/immigration-fiscal/california_program_costs_2026_09_23/RESULT.md) `_cache/op_ftb_gss2_2022.pdf` (same size) | Colorado expanded-EITC dollars; Washington ITIN share of credit applications | Washington publishes application shares only, not ITIN credit dollars |
| TANF recipient characteristics FY2022–FY2024 and TANF/MOE financial data FY2024 (HHS ACF OFA) | [admin_benefit_keys_2026_09_24](../infra/immigration-fiscal/admin_benefit_keys_2026_09_24/RESULT.md) `_cache/wic_tanf/tanf/{fy2022_characteristics.xlsx,fy2023_characteristics.xlsx,fy2024-characteristics.xlsx}`, `_cache/tanf_fin/fy-2024-tanf-moe-financial-data.xlsx` | Hispanic TANF recipient shares; state basic-assistance dollar weights (ladder 217) | characteristics are samples; CA, TX, NM, NV shares about ±6–7 points |
| Treasury Monthly Treasury Statement Table 5, FY2024 premium tax credit; CMS 2017 state default age-rating curves | [ir5_adjusters_2026_09_27](../infra/immigration-fiscal/ir5_adjusters_2026_09_27/RESULT.md) `_cache/ptc/{mts_table5_ptc_fy2024.json,cms_state_age_curves_2017.pdf}` | premium tax credit outlays re-keyed by Marketplace coverage and age (ladder 247) | — |
| Unemployment insurance reports ETA 203 (claimant characteristics) and ETA 5159 (benefits), with ET Handbook 402 data map (DOL ETA) | [admin_benefit_keys_2026_09_24](../infra/immigration-fiscal/admin_benefit_keys_2026_09_24/RESULT.md) `_cache/ui/{ar203.csv,ar5159.csv,eta_datamap_4024c6.pdf}` | Hispanic share of 2024 UI claimant-weeks; state UI benefit weights (ladder 217) | Hispanic share observed only for claimant-weeks with known ethnicity |
| US Treasury daily par real yield curve rates, 2024 | [school_capital_return_2026_09_26](../infra/immigration-fiscal/school_capital_return_2026_09_26/RESULT.md) `_cache/treasury_real_yield_2024.csv` | market check on the 2% and 3% real rates (ladder 231) | no primary municipal real-yield series |
| US Treasury OTA tax-record distributions by race and ethnicity: Working Papers 122 and 124, Technical Paper 11, 2024 family counts, Advancing Equity FY2025 | [external_benchmarks_2026_09_24](../infra/immigration-fiscal/external_benchmarks_2026_09_24/RESULT.md) `_cache/arm2/{WP-122,WP-124,TP-11,OTA-2024-Family-Counts-Race,Advancing-Equity-FY2025}.{pdf,txt}` | taxes and credits by Hispanic ethnicity against the account's CPS keys (ladder 216) | ethnicity imputed to the primary filer; no income-tax or AGI shares |
| USAspending.gov contract obligations by set-aside code and owner category, FY2022–FY2025 (API JSON) | [affirmative_action_cost_2026_09_24](../infra/immigration-fiscal/affirmative_action_cost_2026_09_24/RESULT.md) `_cache/usaspending/{sa8a,setaside,sot}_*_FY20{22..25}.json` | 8(a) and disadvantaged-business contract dollars by owner group (ladder 213) | federal only; state and local set-asides missing, no national total |
| WIC Participant and Program Characteristics 2020 and 2022, reports and appendices (USDA FNS) | [admin_benefit_keys_2026_09_24](../infra/immigration-fiscal/admin_benefit_keys_2026_09_24/RESULT.md) `_cache/wic_tanf/wic/{WICPC2020-1.pdf,WICPC2020-Appendix.pdf,wic-ppc-2022-report.pdf,wic-ppc-2022-appendices.pdf}` | Hispanic WIC participant shares by state, Appendix Table B.8 (ladder 217) | shares are April 2022, against calendar-2024 CPS receipt |
| WIC program data FY2024: state agency food costs and monthly national series (USDA FNS) | [admin_benefit_keys_2026_09_24](../infra/immigration-fiscal/admin_benefit_keys_2026_09_24/RESULT.md) `_cache/wic_cost/{wicagencies2024ytd-9.xlsx,37wic-monthly-9.xlsx,wisummary-9.xlsx}` | FY2024 food-cost state weights; WIC share of BEA line 39 (ladder 217) | — |

## Schools

| Dataset and vintage | Where it is | Use | Limits |
|---|---|---|---|
| CPS October 2024 school supplement | `school_enrollment_2026_09_20/_cache/`: four files, 82,301,431 bytes, 160 replicate weights, dictionary and SAS controls; [source URLs and hashes](../infra/immigration-fiscal/school_enrollment_2026_09_20/sources.json), [card](../infra/immigration-fiscal/school_enrollment_2026_09_20/DATASET_CARD.md) | Grade and public/private branches for children and adults; own and parent birthplace, self-ID, age and state; a within-October `QSTNUM/OCCURNUM` join only | 27,342 zero-weight nonperson rows lack replicates; four implied weight decimals; carrying the October rate to March is not person linkage or annual pupil-months |
| ECLS-K 1998 cohort, K–8 public child file (waves 1998, 1999 and 2000 used) | `sources/reused-surveys/ecls_k/childk8p.dat`, 1.59 GB, 21,409 children, with its Stata dictionary; compact selected Parquet in `school_peer_checks_2026_09_20/_cache/`; [card](../infra/immigration-fiscal/school_peer_checks_2026_09_20/DATASET_CARD.md), [source hashes](../infra/immigration-fiscal/school_peer_checks_2026_09_20/sources.json), [recipe](../infra/immigration-fiscal/school_peer_checks_2026_09_20/README.md) | Child birthplace, race and home language, repeated IRT scale scores, school IDs, classroom LEP and race counts, weights; the retained-K form is harmonized | LEP and nonwhite counts are not immigrant counts; public and private schools; model-based rather than full survey-design variance |
| ECLS-K:2011, K–5 public file | `sources/reused-surveys/ecls_k2011/childK5p.dat`, 2.46 GB, with its dictionary; [coverage limits](../infra/immigration-fiscal/school_peer_checks_2026_09_20/DATASET_CARD.md) | Feasibility only: repeated scores, classroom EL counts and internal school IDs survive | Child birthplace, teacher and external CCD IDs are suppressed, so no native-born regression comes from this release |
| TEA 2018–19 and 2023–24; CDE 2018–19 to 2025–26 official tables | `school_peer_checks_2026_09_20/tabulate_growth.py`: exact source values, URLs and five generated CSVs | Observed enrollment, recent-immigrant program stocks, teacher and staff FTE, earmarked grants | Program stocks are not arrivals or descendants; statewide staffing ratios do not identify local crowding or immigration-caused spending |
| Census school finance 2023 (`elsec23`) | `sources/immigration-fiscal/data/external/census_school_finance_2023.txt` and `census_school_finance_2023_summary.txt`; county rollup `sources/immigration-fiscal/derived/stage2/school_finance_county_2023.csv` | School-cost context; the county bridge for local burden | Needs rollups and joins |
| NCES Digest Table 236.10, per-pupil spending | `sources/immigration-fiscal/data/nces/tabn236.10.xlsx` | Education cost anchors | Not immigrant-specific |
| NCES CCD LEA English learners, 2017–18 and 2018–19 | `sources/immigration-fiscal/data/external/stage5_net_negative/nces/ccd_lea_141_{1718,1819}_english_learners.zip`; state EL/LEP 2018 in `sources/immigration-fiscal/derived/stage5/state_el_lep_2018.csv` | District school-cost intensity anchor | No later district EL file is held |
| NCES CCD LEA 2023–24 file-tool artifacts | `sources/immigration-fiscal/data/external/stage4/nces/`: file-tool JSON, data notes, LEA membership companion, release notes | Reproducible route to the current district directory | Holds no district EL counts |
| NCES CCD school and LEA directories 2023–24 | `sources/immigration-fiscal/data/external/stage2/nces/ccd_{lea,sch}_029_2324_w_1a_073124.zip` | School and district directory | Replaces the dead `ccd_2024_25_universe` URL |
| SAIPE 2023 school districts | `sources/immigration-fiscal/data/external/stage4/saipe/` (`ussd23.txt`, `ussd23.xls`, layout) | District child counts and child poverty; the context warehouse holds only the state table `saipe_state_school_poverty_2023` | Not immigrant-specific; the April parsed district table no longer exists |
| Census Annual Survey of School System Finances (F-33) FY2024 district files: all items (`elsec24.txt`) and summary items (`elsec24t.txt`, `.xlsx`) | `sources/immigration-fiscal/data/external/census_f33_district/{elsec24.txt,elsec24t.txt,elsec24t.xlsx}` (`elsec24.txt` same size as `school_dilution_2026_09_24/_cache/f33/elsec24.txt`) | read by `school_cost_where_enrolled_2026_09_24` (`weighting.py`, `test_lane.py`) | — |
| IPEDS 2022–23 public-institution finance (GASB F1A), 12-month FTE (EFIA), tuition by residency (IC AY 2023–24), first-time students' residence (EF C, fall 2022 and 2023), response flags, with dictionaries (NCES) | `sources/immigration-fiscal/data/external/stage3/nces/ipeds_2023/`, hashes in `ACQUIRED.md`; HD2023 and EF2023A are read from `affirmative_action_cost_2026_09_24/_cache/ipeds/` | [user_fee_allocation_2026_10_07](../infra/immigration-fiscal/user_fee_allocation_2026_10_07/RESULT.md) (`higher_ed.py`): the group's shares of public colleges' cost (0.116) and of tuition plus Pell (0.098) | FY2024 finance returned 404 on 2026-10-07; four large universities report under FASB and fall outside; race is Hispanic, made Mexican-origin by the ACS state ratio |

Executed results for the pupil-level checks: [school peer checks](immigration-school-peer-checks-2026-09-20.md).

### GFD_PLOS_S7_2015 — historical school-district finance

**Source/acquired:** Pierson, Hand, Thompson, based on Census; public PLOS S7 acquired 2026-09-20.
[Article](https://doi.org/10.1371/journal.pone.0130119).
**Local:** `infra/immigration-fiscal/causal_execution_2026_09_20/mariel/work/`.
**Size:** ZIP 85,277,958 bytes, underlying CSV 649,878,780 bytes streamed; the selected 1967–92 extract has 268,798 rows
and 17,259 units. [Source lock and recipe](../infra/immigration-fiscal/causal_execution_2026_09_20/mariel/README.md).
**Variables:** Census government `ID`, survey `Year4`, `FYEndDate`, enrollment, `Total_Current_Oper`, total
expenditure, taxes and intergovernmental revenues.
**Quirks/use:** dollars are nominal thousands; survey and fiscal calendars align unit by unit; historical enrollment can
be substituted or unusable; current operating spending differs from total minus capital. No pupil nativity, white
outcome or class-size measure. Used in 21 conditional Mariel SCM models, not in national population accounting.

### In analysis lanes

| Dataset and vintage | Where it is | Use | Limits |
|---|---|---|---|
| Census Annual Survey of School System Finances (F-33): district files FY2000–FY2024, summary tables FY2005–FY2024, FY2024 all-items workbook and form, FY2015 documentation | [school_dilution_2026_09_24](../infra/immigration-fiscal/school_dilution_2026_09_24/RESULT.md) `_cache/f33/elsec{00..24}.txt`, `_cache/f33/elsec22.xlsx`, `_cache/f33/elsec{05,10,15,19,23,24}_s*tables.xls*`, `_cache/f33/school15doc.pdf` (FY2023 same size as the register's `census_school_finance_2023.txt`); [school_cost_where_enrolled_2026_09_24](../infra/immigration-fiscal/school_cost_where_enrolled_2026_09_24/RESULT.md) `_cache/elsec24_{sumtables,all_items}.xlsx`, `_cache/f33_2024_form.{pdf,txt}`, `_cache/elsec19t.txt`; [school_capital_return_2026_09_26](../infra/immigration-fiscal/school_capital_return_2026_09_26/RESULT.md) `_cache/{elsec19_sumtables.xls,elsec24_sumtables.xlsx}`; [gen_ledger_extension_2026_09_16](../infra/immigration-fiscal/gen_ledger_extension_2026_09_16/RESULT.md) `census_assf_fy2024_summary_tables.xlsx` (tracked, lane root); the FY2024 summary tables are the same size in all four lanes | per-pupil spending and state prices (ladders 76, 215, 222); K-12 capital outlay and debt (231) | FY2022 text file is partial (xlsx used); district sums diverge from Table 8 by state |
| Census SAIPE school-district estimates 2005, 2010, 2018, 2019 and 2023 | [school_dilution_2026_09_24](../infra/immigration-fiscal/school_dilution_2026_09_24/RESULT.md) `_cache/saipe/ussd{05,10,19,23}.txt` (2023 same size as the register's `stage4/saipe/ussd23.txt`); [school_cost_where_enrolled_2026_09_24](../infra/immigration-fiscal/school_cost_where_enrolled_2026_09_24/RESULT.md) `_cache/ussd18.txt` | district child poverty for dilution quintiles (ladder 222) and English-learner spending (215) | — |
| Chicago Data Portal CPS school profiles and progress reports, SY2016-17 to SY2024-25 | [newcomer_school_shock_2026_09_28](../infra/immigration-fiscal/newcomer_school_shock_2026_09_28/RESULT.md) `_cache/chicago/portal/{profile,progress}_SY*.csv` | links CPS School IDs to state RCDTS and finance IDs (ladder 252) | — |
| Chicago Public Schools 20th-day membership demographics, including English learners and special education, SY2017–SY2025 | [newcomer_school_shock_2026_09_28](../infra/immigration-fiscal/newcomer_school_shock_2026_09_28/RESULT.md) `_cache/chicago/cps/demographics_*.{xls,xlsx}` | school English-learner counts, the newcomer intensity (ladder 252) | — |
| Chicago Public Schools employee position rosters, quarterly, September 2016 – June 2025 | [newcomer_school_shock_2026_09_28](../infra/immigration-fiscal/newcomer_school_shock_2026_09_28/RESULT.md) `_cache/chicago/cps_positions/employeepositionroster*.xls` | school teacher FTE on September 30 and March 31 (ladder 252) | — |
| Chicago Public Schools IAR/PARCC results 2015–2024 (school and citywide) and IAR proficiency SY2025 onward | [newcomer_school_shock_2026_09_28](../infra/immigration-fiscal/newcomer_school_shock_2026_09_28/RESULT.md) `_cache/chicago/cps/{iar-parcc_2015to2024_*,IARProficiency_SY2025_Present}.xlsx` | proficiency of pupils who were never English learners (ladder 252) | non-EL results for 2024 are not published |
| Chicago Public Schools school budget overviews FY2025–FY2026 and budget appendices FY2024–FY2026 | [newcomer_school_shock_2026_09_28](../infra/immigration-fiscal/newcomer_school_shock_2026_09_28/RESULT.md) `_cache/chicago/cps_budget/*.{xlsx,pdf}` | newcomer enrollment adjustments in school budgets (ladder 252) | FY2024 school budgets were not retrievable |
| Civil Rights Data Collection 2021–22 First Look report (US Department of Education, OCR) | [social_costs_unpriced_2026_09_28](../infra/immigration-fiscal/social_costs_unpriced_2026_09_28/RESULT.md) `_cache/crdc_2021_22_first_look.pdf` | out-of-school suspensions by race and sex as the disruption proxy (ladder 258) | Hispanic pupils of any race stand in for the Mexican-origin group |
| Colorado CDE CMAS results, 2017–2026: overall, disaggregated and by language proficiency, with file layouts | [newcomer_school_shock_2026_09_28](../infra/immigration-fiscal/newcomer_school_shock_2026_09_28/RESULT.md) `_cache/denver/cde_cmas_*.{xlsx,pdf}`, sources in `_cache/denver/SOURCES.tsv` | Denver scale scores of pupils who were never English learners (ladder 252) | — |
| Colorado CDE ESSA per-pupil expenditure files FY2019–FY2025 and Denver (0880) ESSA local reports 2022–2025 | [newcomer_school_shock_2026_09_28](../infra/immigration-fiscal/newcomer_school_shock_2026_09_28/RESULT.md) `_cache/denver/cde_ft_essa_ppe_fy20{19…25}.xls*`, `_cache/denver/cde_essa_local_report_0880_*.xlsx` | Denver school site spending (ladder 252) | — |
| Colorado CDE pupil membership by school (grade level and instructional program), 2016-17 to 2025-26 | [newcomer_school_shock_2026_09_28](../infra/immigration-fiscal/newcomer_school_shock_2026_09_28/RESULT.md) `_cache/denver/cde_pm_{grade_school,ipst_school}_*.xlsx`, `_cache/denver/cde_pm_school_workbook_2026.xlsx` | Denver "Immigrant" pupil counts, the newcomer intensity (ladder 252) | blank immigrant counts (0–3 pupils) are set to 0 |
| Colorado CDE pupil-teacher ratios and staff statistics by school, 2016-17 to 2025-26 | [newcomer_school_shock_2026_09_28](../infra/immigration-fiscal/newcomer_school_shock_2026_09_28/RESULT.md) `_cache/denver/cde_ptr_school_*.xlsx`, `_cache/denver/cde_staff_ratio_workbook_2026.xlsx` | Denver teacher FTE and pupils per teacher (ladder 252) | Denver school budgets and class sizes were not obtainable |
| IPEDS 2023 institutional characteristics (HD), fall enrollment by race (EF A) and admissions (ADM), with dictionaries (NCES) | [affirmative_action_cost_2026_09_24](../infra/immigration-fiscal/affirmative_action_cost_2026_09_24/RESULT.md) `_cache/ipeds/{HD2023,EF2023A,ADM2023}.zip`, extracted `{HD2023,ef2023a,adm2023}.csv` | first-year seats by race at elite and selective colleges (ladder 213) | — |
| ISBE Illinois Report Card public data sets 2017–2025, with glossaries and metric business rules | [newcomer_school_shock_2026_09_28](../infra/immigration-fiscal/newcomer_school_shock_2026_09_28/RESULT.md) `_cache/chicago/isbe/*Data-Set.xlsx`, `_cache/chicago/isbe/rc17*.zip`, glossary and business-rule PDFs in `_cache/chicago/isbe/` | Chicago site-based spending and average class size (ladder 252) | Illinois's new cut scores in 2025 break the score series |
| NAEP state results, grades 4 and 8 math and reading, 1996–2024, by race, English-learner status and parental education (NAEP Data Service API pulls) | [school_systemwide_2026_09_27](../infra/immigration-fiscal/school_systemwide_2026_09_27/RESULT.md) `_cache/naep/*.json` | white and non-EL pupils' state scores against share changes (ladder 248) | parental education only for grade 8; 2022 and 2024 confounded by school closures |
| NCES Common Core of Data: school membership 2021-22 (file 052), LEA staff 2018-19 and 2023-24 (059), and Urban Institute portal pulls of district enrollment, directory, English learners and F-33 finance, 1998–2023 | [school_cost_where_enrolled_2026_09_24](../infra/immigration-fiscal/school_cost_where_enrolled_2026_09_24/RESULT.md) `_cache/ccd_sch_052_2122_l_1a_071722.zip`, `_cache/ccd_SCH_052_2122_l_1a_071722_CSV.zip`; [school_dilution_2026_09_24](../infra/immigration-fiscal/school_dilution_2026_09_24/RESULT.md) `_cache/nces/ccd_lea_059_{1819_l_1a_091019,2324_l_1a_073124}.zip`, `_cache/ccd/dir_{2000..2003}_<state>.csv` (Urban portal); [school_flight_2026_09_18](../infra/immigration-fiscal/school_flight_2026_09_18/RESULT.md) `_cache/dist/{fin,enr,dir}_<year>_<fips>.csv` (Urban portal, waves 2000, 2005, 2010, 2015, 2019); [school_systemwide_2026_09_27](../infra/immigration-fiscal/school_systemwide_2026_09_27/RESULT.md) `_cache/grade_shares/race_g*_*.json`, `_cache/shares/ccd_{race,el}_*.json` (Urban portal) | Hispanic and English-learner shares, teacher FTE, within-district weights (ladders 141, 215, 222, 248) | Urban's F-33 stops at 2020; 2005 and 2015 waves partial; EL counts have state gaps |
| NCES School-Level Finance Survey (SLFS) FY2022, data and documentation (NCES 2025-047r) | [school_cost_where_enrolled_2026_09_24](../infra/immigration-fiscal/school_cost_where_enrolled_2026_09_24/RESULT.md) `_cache/slfs22_data_2025047_4_0_1.zip`, `_cache/slfs_fy22_2025047r.zip`, `_cache/slfs22_doc/` | school spending per pupil within districts (ladder 215) | a provisional file from a COVID-relief year |
| NYC DOE class-size reports by school, 2017-18 to 2025-26 (none for 2020-21) | [newcomer_school_shock_2026_09_28](../infra/immigration-fiscal/newcomer_school_shock_2026_09_28/RESULT.md) `_cache/nyc/class_size/*.{xlsx,csv}` | K-5 average class size (ladder 252) | — |
| NYC DOE demographic snapshots, 2017-18 to 2025-26 (NYC Open Data c7ru-d68s and InfoHub) | [newcomer_school_shock_2026_09_28](../infra/immigration-fiscal/newcomer_school_shock_2026_09_28/RESULT.md) `_cache/nyc/demographic-snapshot-{2017-18-to-2021-22-opendata-c7ru-d68s.csv,2021-22-to-2025-26-public.xlsx}` | school ELL counts and enrollment, the newcomer intensity (ladder 252) | ELL count is net of exits; most 2022-23 arrivals came after the October register |
| NYC DOE ELA and math test results 2018–2026, school and citywide (InfoHub, as of August 3, 2026) | [newcomer_school_shock_2026_09_28](../infra/immigration-fiscal/newcomer_school_shock_2026_09_28/RESULT.md) `_cache/nyc/{school,citywide}-{ela,math}-results-public.xlsx` | mean scale scores of never-ELL pupils by school and grade (ladder 252) | school-grade means mix score changes with changes in who is tested |
| NYC DOE School Allocation Memoranda tables, FY2022–FY2026 (SAMs 65, 73, 81, 84, 85, 86, 90) | [newcomer_school_shock_2026_09_28](../infra/immigration-fiscal/newcomer_school_shock_2026_09_28/RESULT.md) `_cache/nyc/sams/FY20{22…26}_SAM*_T01*.xlsx` | shelter-routed newcomer funding by school, the alternative intensity (ladder 252) | SAMs 65 and 90 cover only the arrivals those two memos recorded |
| NYSED School Report Card database, releases SRC2019 and SRC2021–SRC2025 (school years 2017-18 to 2024-25) | [newcomer_school_shock_2026_09_28](../infra/immigration-fiscal/newcomer_school_shock_2026_09_28/RESULT.md) `_cache/nyc/nysed_src/SRC{2019,2021…2025}.zip`, extracted `_cache/nyc/nysed_src/tables/`, hashes in `extract_nysed_src.py` | NYC school teacher counts and spending per pupil (ladder 252) | school spending jumps in 2023-24, a reporting break the ReadMe omits |
| SHEEO State Higher Education Finance (SHEF), FY25 report data: education appropriations and net FTE enrolment by state, FY2024 | [ledger_residual_agg_2026_09_16](../infra/immigration-fiscal/ledger_residual_agg_2026_09_16/RESULT.md) `_cache/SHEEO_SHEF_FY25_Report_Data.xlsx` | public higher-education appropriation per enrolled 18–24-year-old, by state | enrolment intensity unmodelled: a half-time student counts as a full FTE |
| Stanford Education Data Archive (SEDA) 6.0: geographic-district annual subgroup scores (cohort scale) and covariates, with codebooks | [school_systemwide_2026_09_27](../infra/immigration-fiscal/school_systemwide_2026_09_27/RESULT.md) `_cache/seda/{seda_geodist_annualsub_cs_6.0,seda_cov_geodist_annual_6.0}.csv`, `_cache/seda/seda_codebook_*_6.0.xlsx`, `_cache/seda/SEDA_documentation_6.0.pdf` | district scores linked to NAEP against immigrant-origin shares (ladder 248) | district zeros treated as missing; Hawaii and DC absent, Virginia reading only |
| State assessment technical reports: NYSED grades 3–8 2018–2025; ISBE PARCC 2018 and IAR 2019–2025; CDE CMAS state summaries 2017, 2018, 2021 | [newcomer_school_shock_2026_09_28](../infra/immigration-fiscal/newcomer_school_shock_2026_09_28/RESULT.md) `_cache/sd/{nysed_3-8,isbe_iar,isbe_parcc}_techreport_*.pdf`, `_cache/sd/cde_cmas_state_summary_*`, sources in `_cache/sd/SOURCES.tsv` | statewide student-level SDs to standardize school scale scores (ladder 252) | statewide SDs only; no 2026 NYSED technical report |
| State student-aid statistics for undocumented students: Minnesota State Grant FY2025; THECB affidavit students (FY2017); WSAC 2024 need-based aid | [itin_credits_student_aid_2026_09_23](../infra/immigration-fiscal/itin_credits_student_aid_2026_09_23/RESULT.md) `_cache/mn_state_grant_eoy_fy2025.{pdf,txt}`, `_cache/thecb_affidavit_overview.{pdf,txt}`, `_cache/wsac_2024_stateneedbased_by_inst.{pdf,txt}` | state grant aid to undocumented students, about $83m a year | Texas figures date from FY2017; its affidavit-student aid ended in 2025 |

## Housing, labor and local economy

| Dataset and vintage | Where it is | Use | Limits |
|---|---|---|---|
| CBP_COUNTY_2012_2017_2022: County Business Patterns, county files 2012, 2017 and 2022 | `sources/immigration-fiscal/data/external/cbp_county/cbp{12,17,22}co.txt`, copied 2026-09-23 from the SSD corpus's copy of census.gov `cbp/datasets/20YY/cbpYYco.zip`; 2007 in `gg_response_county_iv_2026_09_23/_cache/cbp/`; hashes and official routes in `MANIFEST.md` | March employment and establishments by county and NAICS; the [county IV lane](../infra/immigration-fiscal/gg_response_county_iv_2026_09_23/README.md)'s industry-mix (Bartik) instrument uses 3-digit NAICS | 53–55% of county 3-digit cells are suppressed in 2007 and 2012 and imputed from size classes; place of work, not residence |
| PEP_CC_EST2023_ALLDATA: county population by age, sex, race and Hispanic origin, vintage 2023 | `sources/immigration-fiscal/data/external/census_county_pop/cc-est2023-alldata.csv`, the same bytes as census.gov `popest/datasets/2020-2023/counties/asrh/`; intercensal years in `gg_response_county_iv_2026_09_23/_cache/pep/` | County population for 2022 | Vintage 2023 estimates, not the ACS; latin-1 encoding |
| LEHD QWI state panel | `sources/immigration-causal/data/lehd/qwi_state_panel.parquet`, 151,128 rows × 12 columns, restored 2026-09-16 through the Census QWI API (`acquire/pull_qwi_state_panel.py`, 36 calls); `ACQUIRED.md` beside it | State-quarter employment, earnings and flows | QWI has no immigrant status, so exposure must come from other layers. The county receiver panel was lost (see [Not held](#not-held)) |
| BLS QCEW 2023 annual, by industry | `sources/immigration-fiscal/data/bls/qcew_2023_annual_by_industry.zip`; extracted sector files in `bls/extracted/2023.annual.by_industry/` | Sector employment and wages (construction, hospitality) | Industry totals, not immigrant composition |
| BLS CPS labor force by nativity, monthly | `.scratch/frontier-20260905/datasets/bls/`, January 2021–August 2026; URLs, times, units and SHA-256 in that folder's `manifest.json` | Eight national 16+ series (population, employed, employment/population, unemployment) by nativity and month | 544 rows, with eight missing October 2025 values kept; compare matched calendar months. Not legal status; not seasonally adjusted, and the 2026 population-control break rules out a causal displacement reading ([BLS Table A-7](https://www.bls.gov/webapps/legacy/cpsatab7.htm)) |
| Census county building permits | `.scratch/frontier-20260905/datasets/bps/`: 2025 annual and May–July 2026 monthly | Authorized residential units, reported and estimated, by state and county FIPS × period | Permits are not completions; reported units are a subset, not an extra quantity ([Census files](https://www2.census.gov/econ/bps/County/)) |
| BLS LAUS, county monthly | `sources/immigration-fiscal/data/external/stage2/bls/laus/` | Labor-panel seed | — |
| FRED series (unemployment, CPI, housing starts, Case-Shiller, household income, participation and others) | `sources/immigration-fiscal/data/fred/` and `external/fred/` | Macro context | — |
| FHFA state house price index | `sources/immigration-fiscal/data/external/fhfa_hpi_po_state.txt` | Owner-side housing context | State level only |
| HUD Small Area Fair Market Rents FY2025 | `sources/immigration-fiscal/data/external/stage5_net_negative/hud/fy2025_safmrs_revised.xlsx`, fetched with Playwright 2026-06-18; panels by ZIP, county, PUMA and state in `sources/immigration-fiscal/derived/stage5/safmr_{zip,county,puma,state}_2025.csv` | ZIP rent caps for voucher and local-burden context; PUMA and state rent context | ZCTA → county → PUMA through Census crosswalks |
| HUD CHAS 2018–2022, county | `sources/immigration-fiscal/data/external/stage2/hud/chas/2018thru2022-050-csv.zip`, acquired 2026-06-18 through a Playwright session | County share with at least one of four housing problems (Table 11) | Not a welfare measure |
| ACS 2023 median gross rent, state and PUMA | `sources/immigration-fiscal/data/external/origin/census_acs1_2023_{state,puma}_median_gross_rent.json` | Renter-side housing context | — |
| Zillow ZORI and ZHVI metro panels, 2015–2026 | `sources/immigration-fiscal/data/external/urban_housing/zillow/metro_{zori,zhvi}_*.csv`, acquired 2026-06-25 (`setup-urban-housing.sh`) | 739-metro monthly rent (ZORI, repeat-rent, ACS-weighted) and home value (ZHVI), the Wilson–Zhou housing outcome; join to the ACS foreign-born share by CBSA | Asking rents on new leases, not contract rent; CBSA level, so the warehouse's PUMA bridge needs a PUMA↔CBSA crosswalk |
| PUMA↔county-subdivision relationship file 2020 | `sources/immigration-fiscal/data/external/stage2/census/geo/tab20_puma520_cousub20_natl.txt` | Input to the stage-2 PUMA–county bridge | — |
| Saiz (2010) MSA housing-supply elasticities with the 2006 Wharton Residential Land Use Regulatory Index (WRLURI) | `sources/immigration-fiscal/data/external/lifetime/saiz/saiz_2010_msa_elasticity.dta` | read by `housing_supply_ca_tx_2026_09_22` (`analysis.py`), `housing_causal_2000_2010_2026_09_22` (`estimate.py`), `receipt_side_long_run_2026_09_28` (`housing.py`) | metro areas on 1999 definitions; the receipt-side lane maps them with `census_1999_msa_fips.txt` |

The September 5 refresh rows (BLS by nativity, county permits, the Vera ICE workbook and SAINC35) have their source
details, bootstrap and failure tests and `principal_checks.json` in the
[dataset refresh](immigration-dataset-proxy-refresh-2026-09-05.md). Its
[acquisition script](../infra/immigration-fiscal/acquire/refresh-frontier-20260905.py) reuses verified files and
refuses altered cached sources.

### AHS_2023_NATIONAL_PUF — full housing survey archives

**Source:** US Census Bureau. **Recovered:** 2026-09-20.
**Local:** `sources/immigration-fiscal/data/external/ahs_2023/`.
**Official:** [Census 2023 AHS directory](https://www2.census.gov/programs-surveys/ahs/2023/).
**Size:** v1.0 141,729,433 bytes; v1.1 141,845,539 bytes, both full-CRC verified.
**SHA-256:** v1.0 `c595a82f1bfff2b992e5f2b1711556436a785ebc3fe940c522483c501bd195dc`;
v1.1 `429be06168986d87a9e5f9b2bc2c722ece90726c2e0cdbf7630c444073d6d08a`.
**Codebooks:** `enclave_quality_2026_09_18/_cache/ahs_mini_2023.pdf`, `ahs_items.pdf`, `ahs_definitions.pdf` and
`ahs_cdbk_ref.pdf` under the fiscal infra tree.
**Fields/use:** CONTROL, WEIGHT, HHSPAN, HHRACE, HHNATVTY, HINCP, TENURE and housing and neighborhood quality;
[analysis](../infra/immigration-fiscal/enclave_quality_2026_09_18/ahs_analysis.py). Public-use household sample;
distinguish survey versions, nativity and Hispanic identity, and use the documented complex-sample weights. The lane's
v1.0 cache holds a verified clone in place of its truncated download. Both releases are kept.

### In analysis lanes

| Dataset and vintage | Where it is | Use | Limits |
|---|---|---|---|
| ACS EEO Tabulation 2014–2018, EEOALL1R (occupation by race and ethnicity) for EEO county sets, with county-set crosswalk | [vending_restaurants_2026_09_24](../infra/immigration-fiscal/vending_restaurants_2026_09_24/RESULT.md) `_cache/eeo/{acseeo5y2018-eeoall1r.dat.gz,acseeo5y2018-eeoall1r.ann.gz,county_sets_2018.xlsx}` | Hispanic share of food-preparation workers by county (ladder 223) | published for 1,440 county sets, mapped to counties |
| Autor–Dorn county to 1990 commuting zone crosswalk (`cw_cty_czone`) | [scale_spillovers_2026_09_23](../infra/immigration-fiscal/scale_spillovers_2026_09_23/RESULT.md) `_cache/cw_cty_czone.zip`, unpacked `_cache/cw_cty_czone/` | commuting-zone geography for the city-size gradients (ladder 201) | — |
| BEA input-output accounts (use tables 2017 detail and 1997–2023 summary; supply-use), GDP-by-industry gross output and value added, NIPA Section 6 | [construction_housing_supply_2026_09_23](../infra/immigration-fiscal/construction_housing_supply_2026_09_23/RESULT.md) `_cache/bea/{AllTablesIO.zip,AllTablesSUP.zip,IOUse_Before_Redefinitions_PRO_2017_Detail.xlsx,IOUse_Before_Redefinitions_PRO_1997-2023_Summary.xlsx,GrossOutput.xlsx,ValueAdded.xlsx,Section6All_xls.xlsx}` | construction cost shares for the group's effect on structure costs (ladder 200) | materials held at the numeraire; their labour content is not traced |
| BEA regional accounts SAPCE1: personal consumption expenditures by state, 1997–2024 (September 2025 release) | [state_priced_services_2026_09_29](../infra/immigration-fiscal/state_priced_services_2026_09_29/RESULT.md) `_cache/SAPCE.zip` (sha256 pinned in the script) | state sales-tax revenue per dollar of consumption, 2023–2024 mean (ladder 267) | the group's consumption has no state split; population shares stand in |
| BEA Regional CAINC1 county personal income, population and per-capita income, 1969–2024 | [automation_channel_2026_09_16](../infra/immigration-fiscal/automation_channel_2026_09_16/RESULT.md) `_cache/{CAINC1.zip,CAINC1__ALL_AREAS_1969_2024.csv,CAINC1_<ST>_1969_2024.csv}` | San Joaquin Valley per-capita income against California and US (ladder 94) | per-capita income cannot show whether incumbents' own incomes fell |
| BLS Quarterly Census of Employment and Wages: annual single files 2006, 2010, 2012, 2016, 2019–2023; county restaurant and grocery files 2014–2023; 2021 Q1 US file | [labor_mobility_insurance_2026_09_23](../infra/immigration-fiscal/labor_mobility_insurance_2026_09_23/RESULT.md) `_cache/qcew/{2006,2010,2012,2016,2019,2020,2021,2022,2023}_annual_singlefile.zip`; [vending_restaurants_2026_09_24](../infra/immigration-fiscal/vending_restaurants_2026_09_24/RESULT.md) `_cache/qcew/qcew_<year>_<naics>.csv`; [housing_transfer_2026_09_23](../infra/immigration-fiscal/housing_transfer_2026_09_23/RESULT.md) `_cache/qcew_2021q1_us.csv` | metro employment shocks (ladder 203); restaurant jobs (223); March 2021 covered employment (190) | place-of-work payroll employment; the API has no 2012–2013 industry slices |
| Census 2022 Industry Code List with crosswalk to NAICS | [winners_losers_2026_09_24](../infra/immigration-fiscal/winners_losers_2026_09_24/RESULT.md) `_cache/sources/census_industry_2022_crosswalk.xlsx` | NAICS templates for industry-worker groups in the winners count (ladder 226) | — |
| Census Building Permits Survey: state files annual 2000–2024 and monthly 2015, 2019, 2023; metro files 2019–2023; CBSA files 2024–2025 | [housing_supply_ca_tx_2026_09_22](../infra/immigration-fiscal/housing_supply_ca_tx_2026_09_22/RESULT.md) `_cache/{bps_state_20{00..24}.txt,bps_state_monthly_{2015,2019,2023}{01..12}.txt,bps_stateasc.pdf,fred_CABPPRIV.csv,fred_TXBPPRIV.csv}`, pins in `_cache/manifest.json`; [enforcement_rents_2025_2026_09_27](../infra/immigration-fiscal/enforcement_rents_2025_2026_09_27/RESULT.md) `_cache/bps/{ma20{19..23}a.txt,ma2{1,2,3}12y.txt,cbsa202{4,5}a.txt}` | units authorised per resident, California against Texas (ladder 180); rent-supply control (245) | authorisations, not completions; imputed for non-responding offices; 2024 metro delineation differs |
| Census County and ZIP Code Business Patterns 2012–2023: restaurants and grocery by county, ZIP and CBSA; US flat files 2019 and 2023 | [vending_restaurants_2026_09_24](../infra/immigration-fiscal/vending_restaurants_2026_09_24/RESULT.md) `_cache/cbp/cbp_<year>_<naics>_{county,us}.json`, `_cache/cbp/{cbp19us.zip,cbp23us.zip}`, `_cache/zbp/zbp_<year>_<naics>[_<county><n>].json` (Census API); [cultural_output_2026_09_19](../infra/immigration-fiscal/cultural_output_2026_09_19/RESULT.md) `_cache/cbp/cbp_2023_restaurants_cbsa.csv` (Census API) | restaurant establishments and jobs around the vending law (ladder 223); OSM coverage check (156) | establishments and employment, not margins |
| Census Gazetteer files (land area, interior points): counties and ZCTAs 2020, tracts 2019, CBSAs 2023 | [connectedness_fragmentation_2026_09_28](../infra/immigration-fiscal/connectedness_fragmentation_2026_09_28/RESULT.md) `_cache/gaz/2020_Gaz_{counties,zcta}_national.{zip,txt}`; [service_response_long_run_2026_09_27](../infra/immigration-fiscal/service_response_long_run_2026_09_27/RESULT.md) `_cache/2020_Gaz_counties_national.zip`; [hedonic_composition_2026_09_19](../infra/immigration-fiscal/hedonic_composition_2026_09_19/RESULT.md) `_cache/gaz_tracts_2019.zip`, `_cache/gaz/2019_Gaz_tracts_national.txt`; [scale_spillovers_2026_09_23](../infra/immigration-fiscal/scale_spillovers_2026_09_23/RESULT.md) `_cache/2023_Gaz_cbsa_national.zip` | land area for density controls, county land checks and CBSA area caps | — |
| Census geographic relationship files: 2020-to-2010 tracts, 2020 tract-to-PUMA, 2010 ZCTA-to-county and ZCTA-to-place, Connecticut county-to-planning-region | [hedonic_composition_2026_09_19](../infra/immigration-fiscal/hedonic_composition_2026_09_19/RESULT.md) `_cache/{tab20_tract20_tract10.txt,zcta_county_rel_10.txt,ct_cou_to_cousub_crosswalk.xlsx}`; [receipt_side_long_run_2026_09_28](../infra/immigration-fiscal/receipt_side_long_run_2026_09_28/RESULT.md) `_cache/census_2020_tract_to_puma.txt`; [vending_restaurants_2026_09_24](../infra/immigration-fiscal/vending_restaurants_2026_09_24/RESULT.md) `_cache/{zcta_place_rel_10.txt,zcta_county_rel_10.txt}` | tract, ZIP and PUMA panels on fixed geography (ladders 155, 223, 253) | — |
| Census Rental Housing Finance Survey 2024 public-use file and codebook | [housing_transfer_2026_09_23](../infra/immigration-fiscal/housing_transfer_2026_09_23/RESULT.md) `_cache/rhfspuf2024.csv`, `_cache/rhfs2024_codebook.{pdf,txt}` | rental units by owner entity (ladder 190) | the public file has no owner race or ethnicity item |
| Census Services Annual Survey revenue, investigation and security services (NAICS 5616, via FRED); BLS OES security guards (33-9032) | [social_costs_unpriced_2026_09_28](../infra/immigration-fiscal/social_costs_unpriced_2026_09_28/RESULT.md) `_cache/fred_REVEF5616*.csv`, `_cache/{bls_oes.json,bls_oes_339032.htm}` | private security spending for the security cost item (ladder 258) | the crime share of security spending is an assumed parameter |
| Census TIGER/Line shapefiles: CBSA cartographic boundaries 2023 (1:500k); California ZCTAs 2010 | [cultural_output_2026_09_19](../infra/immigration-fiscal/cultural_output_2026_09_19/RESULT.md) `_cache/tiger/cb_2023_us_cbsa_500k.{zip,shp,dbf}`; [vending_restaurants_2026_09_24](../infra/immigration-fiscal/vending_restaurants_2026_09_24/RESULT.md) `_cache/lapd/tl_2010_06_zcta510.zip` | point-in-polygon assignment of restaurants to CBSAs (156) and arrests to ZIPs (223) | — |
| Federal Reserve Z.1 Financial Accounts of the United States, release current on 2026-09-23 (CSV files and data dictionary) | [housing_transfer_2026_09_23](../infra/immigration-fiscal/housing_transfer_2026_09_23/RESULT.md) `_cache/z1_csv_files.zip`, unpacked `_cache/z1/` | land share of owner-occupied real estate; foreign direct investment in real estate (ladder 190) | — |
| FHFA land prices and land shares, Davis–Larson–Oliner–Shui (FHFA WP 19-01), data version 4.0, June 2024 | [receipt_side_long_run_2026_09_28](../infra/immigration-fiscal/receipt_side_long_run_2026_09_28/RESULT.md) `_cache/fhfa_land_prices_2024_06.xlsx`, pins in `inputs/pins.json` | land share of home value where the group pays property tax (ladder 253) | single-family parcels only; multifamily land shares are lower |
| Geocorr PUMA allocation factors (MCDC; 2000, 2012 and 2022 PUMAs to counties; 2022 PUMAs to 2020 urban areas and 2023 CBSAs) and metro delineations (1999 MSAs, OMB February 2013 and July 2023, List 1) | [displacement_transfers_2026_09_18](../infra/immigration-fiscal/displacement_transfers_2026_09_18/RESULT.md) `_cache/{xwalk_puma2k.csv,xwalk_puma12.csv,xwalk_puma22.csv,omb_delineation_2013_list1.xls}`; the four files at the same sizes in [school_flight_2026_09_18](../infra/immigration-fiscal/school_flight_2026_09_18/RESULT.md) and [employment_entry_2026_09_18](../infra/immigration-fiscal/employment_entry_2026_09_18/RESULT.md) `_cache/`; [labor_mobility_insurance_2026_09_23](../infra/immigration-fiscal/labor_mobility_insurance_2026_09_23/RESULT.md) `_cache/xwalk/xwalk_{puma2k,puma12,puma22}.csv` (same sizes); [hedonic_composition_2026_09_19](../infra/immigration-fiscal/hedonic_composition_2026_09_19/RESULT.md) `_cache/cbsa_list1_2013.xls`; [congestion_2026_09_23](../infra/immigration-fiscal/congestion_2026_09_23/RESULT.md) `_cache/xwalk_puma22_ua20.csv`; [service_by_ses_2026_09_23](../infra/immigration-fiscal/service_by_ses_2026_09_23/RESULT.md) `_cache/xwalk_puma22_cbsa23.csv`, `_cache/list1_2023.xlsx`; [scale_spillovers_2026_09_23](../infra/immigration-fiscal/scale_spillovers_2026_09_23/RESULT.md) `_cache/xwalk_puma22_cbsa23.csv` (same size); [receipt_side_long_run_2026_09_28](../infra/immigration-fiscal/receipt_side_long_run_2026_09_28/RESULT.md) `_cache/census_1999_msa_fips.txt` | fixed metro, urban-area and county geographies for PUMA panels (ladders 136, 140, 141, 195, 205, 253) | — |
| HUD Picture of Subsidized Households 2023 and 2024, state and US files on 2020 census geography | [admin_benefit_keys_2026_09_24](../infra/immigration-fiscal/admin_benefit_keys_2026_09_24/RESULT.md) `_cache/hud/{STATE,US}_{2023,2024}_2020census.xlsx`, `_cache/hud/dictionary_2024.pdf` | federal housing-assistance spending by head's ethnicity against CPS (ladder 217) | validity screen misfires for housing, where many assisted households are Black |
| IRS SOI state migration data, tax-year pairs 2011–12 to 2022–23: inflow and outflow files, in-migration by AGI, full archives for four pairs | [tiebout_sorting_2026_09_18](../infra/immigration-fiscal/tiebout_sorting_2026_09_18/RESULT.md) `_cache/{stateinflow,stateoutflow}{1112,1213,…,2223}.csv`, `_cache/{1112,1213,…,2223}inmigall.csv`, `_cache/{1112,1516,1617,1718}migrationdata.zip`; the register lists a 2011–22 panel at `/Volumes/2TBPNY/corpus/irs_soi/migration/` (SSD not mounted, sizes unchecked) | high-income out-migration and AGI outflow by state (ladder 139) | the IRS 2014-15 AGI-bracket file covers only 14 states |
| OpenStreetMap restaurant and fast-food features, 32 states (Overpass API, September 2026) | [cultural_output_2026_09_19](../infra/immigration-fiscal/cultural_output_2026_09_19/RESULT.md) `_cache/osm/<ST>.json`, `_cache/osm/_manifest*.json` | Mexican restaurants per head across metros, variety saturation (ladder 156) | cuisine tagging is voluntary and uneven |
| RIAA year-end music revenue reports 2024 (all and Latin) and 2025 (Latin) | [cultural_output_2026_09_19](../infra/immigration-fiscal/cultural_output_2026_09_19/RESULT.md) `_cache/riaa/{riaa_all_2024_year_end.pdf,riaa_latin_2024_year_end.pdf,riaa_latin_2025_year_end.pdf}` | Latin music share of US recorded-music revenue (ladder 156) | "Latin" is a genre, not Mexican-origin output; listener composition unmeasured |
| Social Capital Atlas county and ZIP files (Chetty et al., via HDX) with July 2022 codebook | [connectedness_fragmentation_2026_09_28](../infra/immigration-fiscal/connectedness_fragmentation_2026_09_28/RESULT.md) `_cache/sca/social_capital_{county,zip}.csv`, `_cache/sca/readme.pdf` | county economic connectedness against Hispanic share (ladder 262) | measures friendships across socioeconomic status, not across ethnic groups |
| Zillow Observed Rent Index (ZORI; metro, city and ZIP, to August 2026) and ZIP-level Home Value Index (ZHVI, 2000–2026) | [enforcement_rents_2025_2026_09_27](../infra/immigration-fiscal/enforcement_rents_2025_2026_09_27/RESULT.md) `_cache/zillow/{Metro_zori_uc_sfrcondomfr_sm_month.csv,Metro_zori_uc_sfrcondomfr_sm_sa_month.csv,City_zori_uc_sfrcondomfr_sm_month.csv}`; [hedonic_composition_2026_09_19](../infra/immigration-fiscal/hedonic_composition_2026_09_19/RESULT.md) `_cache/zillow/zip_{zhvi,zori}.csv` | DHS rent-drop claims and metro rent growth (ladder 245); ZIP prices against Hispanic-share change (155) | smoothed repeat-rent index; asking and new-lease rents fall more in gluts |

## Migration, origin and admissions

| Dataset and vintage | Where it is | Use | Limits |
|---|---|---|---|
| INEGI ENADID 2018 and 2023, complete open-data bundles | [Card](../infra/immigration-fiscal/enadid_2026_09_20/DATASET_CARD.md), [12 source hashes and URLs](../infra/immigration-fiscal/enadid_2026_09_20/sources.json), [recipe](../infra/immigration-fiscal/enadid_2026_09_20/README.md) | Validated `TMigrante` departures, destination and return, and `TSDem` birthplace and prior residence, with weights, strata and PSUs; keep string person keys and each wave's question mapping. Returnee schooling with design SEs in [`enadid_return_selectivity_2026_09_22`](../infra/immigration-fiscal/enadid_return_selectivity_2026_09_22/RESULT.md) (ladder 174) | Household-reported five-year departures and residents' five-year residence endpoints cover different people; not an annual bilateral net series; whole-household departures can be missed |
| INEGI Censo 2020, education tabulation 13 (ISCED × five-year age) | `sources/immigration-fiscal/data/external/stage3/inegi/cpv_educacion/cpv2020_b_eum_07_educacion.xlsx`, 3,079,946 bytes, SHA-256 `1f55ffc5d1797bf76c72da4aa2d53604c75c829d78702bff8114852c36d5a98d`, [official](https://www.inegi.org.mx/contenidos/programas/ccpv/2020/tabulados/cpv2020_b_eum_07_educacion.xlsx); [acquisition note](../infra/immigration-fiscal/arrival_cohorts_2026_09_18/ACQUIRED.md) | National counts by ISCED level and average grade, ages 15–19 through 85+; derived `inegi_2020_isced_by_age.csv` and `origin_age_vs_acs.csv` | 2020 census against ACS 2019/2021; the less-than-high-school mapping is ISCED 0–2 against `SCHL` ≤ 15; the ACS treats secundaria as a diploma; the 2010 national-by-age file was not isolated |
| ACS birthplace code lists 2019–2023 | `sources/immigration-fiscal/data/external/origin/ACSPUMS2019_2023CodeLists.xlsx` | Official `POBP` decoding | Coding only |
| ACS B05006 state-by-origin 2023, with metadata | `sources/immigration-fiscal/data/external/origin/census_acs1_2023_B05006_*.json` | Official origin-stock validation | Aggregate only |
| World Bank country metadata | `sources/immigration-fiscal/data/external/origin/worldbank_country_metadata.json` | Region and income-group ontology | Not immigration-specific |
| OHSS LPR workbooks | `sources/immigration-fiscal/data/external/origin/ohss/` | Legal permanent resident admissions by country, county and class | Legal channels only |
| OHSS state immigration flat file 2013–2023 | `sources/immigration-fiscal/data/external/origin/ohss/state_immigration_data_2013_2023.csv`, acquired 2026-06-18 | State-year refugee, LPR, naturalization and nonimmigrant panel | Replaces the dead ACF ORR CSV |
| Pew 2025 unauthorized-immigrant report | `sources/immigration-fiscal/data/pew/pew-unauthorized-immigrants-2025.pdf` | Population size and composition anchor | Report PDF, not machine tables |
| OHSS, RPC and USCIS admission and work-access evidence | 23 pinned public sources in `.scratch/clarity-next-20260905/admission/`; `acquire_admission_evidence_20260905.py` stores URLs and hashes and validates staged files | `analyze_admission_channels.py`: FY2019 and FY2022–25 national LPR and refugee distributions, 2024 joint broad classes, 2026 EAD flows and pending ages ([admission analysis](immigration-admission-work-access-2026-09-05.md)) | Source vintages and nationality/birthplace stay separate; pending-case reports disagree |
| CBP southwest border encounters, FY2022–FY2026 (April) | `sources/immigration-causal/data/cbp/raw/sbo_encounters_fy22_fy25.csv` and `sbo_encounters_fy23_fy26_apr.csv`, re-acquired from cbp.gov 2026-09-16 | Encounter counts | — |
| IRS SOI county migration 2022–23 | `sources/immigration-fiscal/data/external/stage2/irs/county{inflow,outflow}2223.csv`; byte-identical copies in `sources/immigration-causal/data/internal_migration/` | County inflows and outflows of returns and exemptions | Tax filers only; no nativity |
| ORR Annual Report to Congress FY2021 | `sources/immigration-fiscal/data/external/crime_frontier/orr/orr_annual_report_to_congress_fy2021.pdf` | Refugee and unaccompanied-children program spending and counts | Report PDF; the ORR arrivals-by-state file was not obtained (`external/origin/orr/` is empty) |

### RPC_REFUGEE_FY2022_FY2023_FY2025 — refugee admission reports

**Source:** State Department Refugee Processing Center, [RPC archive](https://www.rpc.state.gov/archives/); acquired
2026-09-05. **Local:** `.scratch/cohort-clarity-20260905/availability/rpc_fy{2022,2023,2025}.pdf`, three files,
3,236,929 bytes; URLs and hashes in `manifest.json` and the
[availability memo](immigration-recent-cohort-data-availability-2026-09-05.md).
**Keys:** destination state × principal applicant nationality × admission month. These are refugee-channel arrivals,
not all foreign-born residents, ancestry, religion or a deduplicated union with court, border or LPR records.
**Status:** the [admission analysis](immigration-admission-work-access-2026-09-05.md) reconciles the RPC reports for
2019, 2023 and 2025 and FY2026 through July 31; their Somalia totals are 231, 1,385, 2,496 and 0. The FY2025 monthly
total, 38,102, reconciles. National FY2022 and FY2024 distributions come from separately named OHSS Excel vintages. The
RPC state matrices stay excluded, because text extraction fragments their rows.

### ICPSR_38031_V3 — New Immigrant Survey 2003, Round 1, public use

- Source/acquired: ICPSR 38031 version 3 (Jasso, Massey, Rosenzweig, Smith), downloaded by the operator with an ICPSR
  login, September 22, 2026. Round 2 (ICPSR 38061) is not held.
- Local/size: `sources/immigration-fiscal/data/external/icpsr_nis_2003/ICPSR_38031-V3.zip`, 567,819,638 bytes; 1.26 GB
  unpacked, 675 files, 66 tab-separated data files with ICPSR and PI codebooks and questionnaires. Adult sample 8,573
  respondents: DS0001 roster (1,884 variables), DS0002 preload, DS0003 Section A demographics (3,461 variables),
  DS0004–DS0005 Section B pre-immigration, DS0006–DS0024 sections C–R; later blocks repeat the sections for the spouse
  and child samples.
- Key variables: religion in Section J, DS0017 (`J30_1MO` respondent's religion, `J31_1MO` other, `J33_1MO`
  denomination, `J36_1MO` another religion). Employment and the pay rate are in Section C (DS0006, DS0007: `C1`,
  `C48_1PPP`, `C49_1PPP`) and twelve-month wage income in Section G (DS0011, DS0012: `G7APPP`, spouse path `G16PPP` in
  DS0054). Section H (DS0013, DS0014: `H54*`, `H58*`) holds assets and housing. Occupation and industry codes are in
  Section A (`A959OC`, `A959IN`).
- Quirks/use: new legal permanent residents of 2003–04 only, no unauthorized population; sampling weights are
  documented in `38031-Documentation-sampling_weights.pdf`; ICPSR missing-value codes are in the TSVs. Used for religion
  by earnings among new green-card holders in
  [`nis2003_religion_earnings_2026_09_22`](../infra/immigration-fiscal/nis2003_religion_earnings_2026_09_22/RESULT.md)
  (ladder 179), where Section H served only a home-ownership anchor. Unpacked copies are also read by
  `parent_status_2026_09_23`, `consumption_key_2026_09_24` and `ir5_adjusters_2026_09_27`.

### In analysis lanes

| Dataset and vintage | Where it is | Use | Limits |
|---|---|---|---|
| Center for Migration Studies undocumented population by state 2010–2019 | [apportionment_2026_09_18](../infra/immigration-fiscal/apportionment_2026_09_18/RESULT.md) `_cache/cms_undoc_state_2010_2019.xlsx` | alternative unauthorized-removal arm (ladder 147) | — |
| CILS 1991–2006, Children of Immigrants Longitudinal Study (ICPSR 20520 V3): DS0001 with codebook and questionnaire | [cils_2026_09_17](../infra/immigration-fiscal/cils_2026_09_17/RESULT.md) `raw/ICPSR_20520-V3.zip`, `raw/ICPSR_20520/DS0001/20520-0001-Data.tsv` | arrest, incarceration, schooling and welfare by origin and generation (ladder 106) | no weights; crime items cover the last five years, not a lifetime |
| DHS OHSS Legal Immigration and Adjustment of Status Report, fourth-quarter workbooks FY2019 and FY2022–FY2025 | [ir5_adjusters_2026_09_27](../infra/immigration-fiscal/ir5_adjusters_2026_09_27/RESULT.md) `_cache/ohss_lias/lias_fy{2019,2022,2023,2024,2025}_q4.xlsx` | adjustment shares for parents of citizens and Mexican nationals (ladder 247) | splits by nationality or by class, never both; no prior status |
| DHS OHSS Profiles on Lawful Permanent Residents: Mexico, India, China and Philippines, FY2005–2024, with the FY2024 file index | [late_arrival_tail_2026_09_27](../infra/immigration-fiscal/late_arrival_tail_2026_09_27/RESULT.md) `_cache/profiles/{mexico,india,china,philippines}_{2005…2024}.xls`, `_cache/lpr_cob_index.csv` | upper bound on the share of IR-5 parents admitted at 55+ (ladder 235) | all classes combined, so only an upper bound; uninformative outside Mexico |
| DHS Yearbook of Immigration Statistics: INS yearbooks FY1997–FY2003; OHSS LPR tables FY2004–FY2024 with expanded Tables 8–11; nonimmigrant workbook FY2024; LPRs by country and class, FY2005–2024 edition | [admission_route_2026_09_21](../infra/immigration-fiscal/admission_route_2026_09_21/RESULT.md) `_cache/lpr_fy{2004..2021}.zip`, `_cache/lpr_fy{2022,2023}.xlsx`, unpacked `_cache/lpr_fy*/`, URLs and hashes in `_cache/acquire_manifest.json`; [indian_ledger_2026_09_18](../infra/immigration-fiscal/indian_ledger_2026_09_18/RESULT.md) `_cache/{yearbook_lpr_fy20{20..24}.xlsx,yearbook_nonimmigrants_fy2024.xlsx}`; [late_arrival_tail_2026_09_27](../infra/immigration-fiscal/late_arrival_tail_2026_09_27/RESULT.md) `_cache/yearbook_lpr_2013.zip` (same SHA-256 as admission_route's), unpacked `_cache/yb2013/`, `_cache/2026_0604_ohss_lpr_by_country_by_major_class_and_deriv_emp-based_fy2005-2024.xlsx`, `_cache/{2025_0828_ohss_tables8-11newadj_fy2023_v2,2026_0604_ohss_tables8-11newadj_fy2024}.xlsx`; [clemens_pritchett_calibration_2026_09_19](../infra/immigration-fiscal/clemens_pritchett_calibration_2026_09_19/RESULT.md) `_cache/dhs_lpr_fy2024.xlsx`; [ir5_adjusters_2026_09_27](../infra/immigration-fiscal/ir5_adjusters_2026_09_27/RESULT.md) `_cache/who/Yearbook_Immigration_Statistics_{1997..2003}.{pdf,txt}`, `_cache/who/ohss_expanded_t9_immediate_relatives_fy2023_fy2024.txt` | admission routes by birthplace (ladder 171); IR-5 parents (235, 247); India (150); Mexico (154) | counts status grants, not arrivals; omits temporary workers, students and unauthorized residents |
| IIMMLA 2004, Immigration and Intergenerational Mobility in Metropolitan Los Angeles (ICPSR 22627 V1): data, codebook, questionnaire | [iimmla_2026_09_17](../infra/immigration-fiscal/iimmla_2026_09_17/RESULT.md) `raw/ICPSR_22627-V1.zip`, unpacked `raw/ICPSR_22627/DS0001/{22627-0001-Data.tsv,22627-0001-Codebook.pdf,22627-0001-Questionnaire.pdf}` | incarceration, schooling and welfare by origin and generation (ladder 105) | quota sample without weights; Greater Los Angeles only, 2004, ages 20–39 |
| Pew Research Center unauthorized immigrants by state 1990–2023 (August 2025 release) with the 2025 report | [apportionment_2026_09_18](../infra/immigration-fiscal/apportionment_2026_09_18/RESULT.md) `_cache/{pew_state_trends.xlsx,pew_2025_unauthorized_report.pdf}` | removing the unauthorized from state apportionment counts (ladder 147) | figures rounded to 5,000–25,000 |

## Custody, crime and enforcement

The [detention and crime reporting rule](immigration-detention-crime-and-fiscal-scope-2026-09-20.md) applies to every
row here: ACS institutional residence cannot distinguish immigration custody, criminal custody and noncorrectional
institutions, so keep that limitation at the claim, and keep detention as a fiscal cost with federal and local payments
consolidated once. The [FY2024 account reconciliation](../infra/immigration-fiscal/detention_reconciliation_2026_09_20/README.md)
holds USAspending, SF133, Treasury and national local-finance evidence with source pins and offline probes, so
expired-funding payments need no new download. Custody-purpose and local-reimbursement splits remain unidentified; use
its linked records specification rather than restarting the acquisition. Its verified custody subtotal is not a
national net total.

| Dataset and vintage | Where it is | Use | Limits |
|---|---|---|---|
| BJS Jail Inmates 2023, Table 12 | `detention_evidence_2026_09_20` (official CSV) | Midyear local-jail inmates held for ICE, USMS and other authorities, with survey uncertainty | A stock, not annual days; ICE-held local inmates can overlap ICE totals; no Mexican generation split |
| USSC 2024 Table 9 and Appendix A | `detention_evidence_2026_09_20/_cache/` (official tables and definitions) | Sentenced federal cases by citizenship and primary offense, separating the immigration category | Citizenship is not nativity; the immigration category includes smuggling and document offenses and does not prove that every count was immigration-only |
| SCAAP FY2024 awards and solicitation | `detention_evidence_2026_09_20` (485 parsed application rows) and `.scratch/clarity-next-20260905/conduct/` ([BJA award table](https://bja.ojp.gov/funding/scaap-fy24-awards.pdf), audit and agency releases, source-schema inventories) | Criminal-custody salaries; total, confirmed and unknown-status inmate-days; federal reimbursement; reporting period July 2022–June 2023. `analyze_conduct_denominators.py` also covers separate Minnesota programs and case-money measures | Not civil ICE contracts; unknown days are not all undocumented; awards are not verified outlays; all-inmate salaries are not undocumented-only costs; consolidate transfers once. No annual origin or status offending denominator |
| SCAAP FY2023 awards and FY2025 solicitation | `sources/immigration-fiscal/data/external/crime_frontier/scaap/scaap_fy23_awards.pdf`, `scaap_fy25_solicitation.pdf` | The warehouse tables `crime_scaap_awards` and `crime_scaap_state_2023` below | See the FY2024 row |
| ICE and CBP budget justifications, FY2025 and FY2026; ICE FY2024 annual report | `sources/immigration-fiscal/data/dhs/{cbp,ice}_fy{25,26}_budget_justification.pdf`; the ICE documents are also retained in `detention_evidence_2026_09_20` | Detention cost definitions, prior-year performance estimates, appropriations and requests; federal enforcement-cost context | Budgeted, enacted and requested amounts are not actual spending; attributing them to unauthorized immigrants is inferential; no verified matched FY2024/25 federal-plus-local detention cost total |
| ICE ERO annual reports, FY2023 and FY2024 | `sources/immigration-fiscal/data/external/crime_frontier/ice/ice_ero_annual_fy{2023,2024}.pdf` | Removals, detention and alternatives to detention; headline removals by criminality (FY2024: 88,763 of 271,484 removed had criminal charges or convictions, report p. 1) | The removals-by-criminality panel needs the dashboard export (see [Not held](#not-held)) |
| EOIR workload PDFs and parsed panels | `sources/immigration-fiscal/data/external/stage4/courts/eoir/*.pdf`, acquired 2026-06-18, scripted from the justice.gov statistics page; parsed CSVs in `sources/immigration-fiscal/derived/stage4/eoir/` (`build-context.sh` parses them) | Court workload over 44 years, pending cases from FY2016, UAC, amnesty by state (56) | Text extracted from chart PDFs |
| Court interpreter and language-access documents | `sources/immigration-fiscal/data/external/stage4/courts/`: California language need and interpreter use 2025; Washington interpreter reimbursement 2025–2027 | Interpreter scheduling, reimbursement and language-access operating-cost context | Operational documents, not microdata |
| BJS Survey of Prison Inmates 2016 (SPI2016), public use | `sources/immigration-fiscal/data/external/crime_frontier/spi/ICPSR_37692-V5.zip` and the extracted `ICPSR_37692/DS0001/` (Stata data, codebook); official reconstruction syntax in `.scratch/clarity-next-20260905/conduct-race/`; read by `build/load_spi_citizenship.py`, `analyze_conduct_race.py` and `cj_use_allocation_2026_09_23` | The warehouse table `crime_spi_inmates_by_citizenship`; joint race/ethnicity × birthplace × citizenship prisoner counts with missingness bounds | Citizenship is not nativity or status; an incarceration rate needs a matched 2016 adult denominator, so the old rate table was withdrawn |
| BJS Prisoners in 2023 | `.scratch/clarity-next-20260905/conduct-race/` ([report](https://bjs.ojp.gov/document/p23st.pdf)); hashes in the manifest | Adult sentenced imprisonment rates, 2022–2023 (`analyze_conduct_race.py`) | No immigration-status split; the rates include survey-based administrative adjustments |
| Light/He/Robey, Texas arrests by immigration status, 2012–2018 (openICPSR 124923; [PNAS 2020](https://www.pnas.org/doi/10.1073/pnas.2014704117)) | `sources/immigration-fiscal/data/external/crime_frontier/light_texas/124923-V1.zip`, loaded by `load_light_tx_crime.py`; also unzipped by `crime_cost_firstgen_2026_09_18` (ladder 144) | The warehouse table `crime_tx_arrests_by_status` and view `v_crime_tx_status_ratio` | See the table below |
| BOP population quick facts (JSON, last updated 12 September 2026) | `sources/immigration-fiscal/data/external/bop_quickfacts/quickfacts.json` | no script reads it | federal prisons only; a one-day snapshot |
| DHS Budget in Brief FY2025 and FY2026; CBP and ICE FY2026 Congressional Justifications (PDF and text) | `sources/immigration-fiscal/data/external/dhs_budget/{dhs_fy2025_bib,dhs_fy2026_bib,cbp_fy2026_cj,ice_fy2026_cj}.{pdf,txt}` (the CBP and ICE PDFs are the same size as `sources/immigration-fiscal/data/external/lifetime/admin/{cbp,ice}_fy26_budget_justification.pdf`) | no script reads it | — |
| DOJ FY2026 Budget and Performance Summary (PDF and text) | `sources/immigration-fiscal/data/external/doj_budget/doj_fy2026_bps.{pdf,txt}` | no script reads it | — |

**Crime tables in the context warehouse.** All load into the unified `immigration.duckdb` as aggregates; IPUMS
microdata stay local. Acquisition: `acquire/setup-crime-frontier.sh`; manual downloads:
`crime_frontier/MANUAL_ACQUIRE.md`.

| Table or view | Build | What it answers | Limits |
|---|---|---|---|
| `status_class_def`, `status_class_crosswalk`, `v_status_class_sources` | `build_status_crosswalk.py` | The canonical citizenship and legal-status enum and a six-source crosswalk, with lossy and verified flags; every crime↔fiscal status join loads it | — |
| `crime_scaap_awards` (501 jurisdictions), `crime_scaap_state_2023` (45 states) | `parse_scaap_awards.py`, from the FY23 award PDF | Per-jurisdiction criminal-alien inmate-days and reimbursement; the state rollup has 7.8M inmate-days and $210M reimbursed in FY23 | See the SCAAP rows above |
| `v_crime_scaap_x_state_fiscal` | `build_crime_views.py` | Criminal-alien incarceration burden × state immigrant-cost context (Medicaid, SNAP, English learners) | — |
| `crime_tx_arrests_by_status` (268 rows), `v_crime_tx_status_ratio` | `load_light_tx_crime.py`, `build_crime_views.py`; [source and code audit](immigration-conduct-denominators-2026-09-05.md) | Light/He/Robey Texas recorded arrest charges, 2012–18. The baseline is native-born, and CMS_nat splits naturalized from legal immigrants. 2018 violent rates: 103.52 unauthorized against 226.45 native per 100k, a ratio of 0.4571 | No race or arrival-cohort split |
| `crime_spi_inmates_by_citizenship` | `load_spi_citizenship.py`; [conduct audit](immigration-conduct-denominators-2026-09-05.md) | SPI2016 official RV0004 counts: sample 22,982 citizens, 1,766 noncitizens and 100 ambiguous; weighted noncitizen share 6.831% | Counts only; citizenship is not nativity or status |

### ICE_DETENTION_STATS — ERO detention statistics workbooks, FY2019–FY2026

- **Official workbooks:** ICE Detention Statistics (ice.gov/detain/detention-management), downloaded by the operator
  September 22, 2026: FY19–FY24, FY25 (September 24, 2025 release) and FY26 year to date (July 20, 2026 release), in
  `sources/immigration-fiscal/data/external/ice_detention_stats/*.xlsx`, 132 KB to 1.57 MB each; SHA256 per file in the
  raw-file manifest. Automated fetching is blocked at the site.
- **Vera archive copies:** the [detention evidence lane](../infra/immigration-fiscal/detention_evidence_2026_09_20/RESULT.md)
  pins the FY2024 year-end and FY2025 partial-year workbooks with their documentation and reuses the FY2026 July
  workbook ([manifest](../infra/immigration-fiscal/detention_evidence_2026_09_20/manifest.json),
  [recipe](../infra/immigration-fiscal/detention_evidence_2026_09_20/README.md)). The September 5 refresh holds the July 20
  workbook (observation cutoff July 11) and the matched processed series in `.scratch/frontier-20260905/datasets/ice/`,
  from the [Vera archive](https://github.com/vera-institute/ice-fytd-stats) at tree
  `a6bf48e2627323f01827d52776f0d08023c410ba`; June's 34,551 total exits and 27,679 removal exits reconcile to the raw
  workbook.
- **Key sheets:** `Detention FYxx` (currently detained by processing disposition and by criminality; initial book-ins
  by facility type; book-outs by release reason; average daily population and average length of stay by arresting
  agency, CBP against ICE, by criminality), `Facilities FYxx` (per-facility ADP, detailed type IGSA/CDF/SPC/USMS,
  classification levels, ALOS, inspections), `ICLOS and Detainees` (from FY22), ATD, semiannual, segregation and
  vulnerable-population sheets.
- **Limits:** no country of citizenship and no cost or per-diem column; layouts change every year (`Facilities FY19` is
  220 × 31, `Facilities FY25` 196 × 28; the FY25 segregation sheet spans 16,383 mostly empty columns). Custody history
  is not current custody's legal basis. In the Vera copies FY2024 is complete, FY2025 ADP runs only through September
  20, and July FY2026 is partial; detention exits are not all national removals. No ACS-matched origin, age or sex
  linkage.
- **Use:** allocating Custody Operations dollars by arresting agency and facility type for the custody item in the
  [detention reconciliation](../infra/immigration-fiscal/detention_reconciliation_2026_09_20/README.md); it does not
  close that lane's execution-records gap. No lane reads the official FY19–FY26 set yet.

### In analysis lanes

| Dataset and vintage | Where it is | Use | Limits |
|---|---|---|---|
| BJS Criminal Victimization (NCVS) bulletins and data tables 2018–2024; victims and offenders by race and Hispanic origin 2012–15 (NCJ 250747); N-DASH person files 1993–2024 | [ncvs_victim_offender_2026_09_18](../infra/immigration-fiscal/ncvs_victim_offender_2026_09_18/RESULT.md) `_cache/cv{18,19,21,22,23,24}.zip` (unpacked `_cache/cv*/`), `_cache/{cv19.pdf,cv21.pdf,cv24.pdf,rhovo1215.pdf,nd_person_all_all.csv,nd_person_race_all.csv,nd_person_injury_all.csv}`; [distribution_weights_2026_09_23](../infra/immigration-fiscal/distribution_weights_2026_09_23/RESULT.md) `_cache/sources/bjs_cv{22,23,24}.{pdf,txt}` (2023 revised June 2025) | victim-by-offender ethnicity matrix (ladder 148); victimization by household income (194) | offender ethnicity is the victim's perception; no Mexican origin; income under-reported |
| BJS prison and jail reports: Jail Inmates in 2023 and at Midyear 2010–2012; Prison and Jail Inmates at Midyear 1996–1998 and 2000–2003; Prisoners in 2000–2005 and 2023; Census of Jails 2005–2019; Profile of Jail Inmates (Survey of Inmates in Local Jails) 1989, 1996, 2002; National Inmate Survey reports 2008–09, 2011–12; Immigration Offenders 2000; CJ-3/CJ-5 forms | [crime_ratio_direction_2026_09_24](../infra/immigration-fiscal/crime_ratio_direction_2026_09_24/RESULT.md) `_cache/jail/{ji23st.zip,ji23st_csv/,jim1{0,1,2}st.pdf,cj0519st.zip,cj0519st_csv/,pji{89,96,02}.pdf,pjimy96.pdf,pjim{97,98,02}.pdf,svpjri{0809,1112}.pdf,cj5_*.pdf,CJ3_2019.pdf,cj3-2024.pdf}`; [crime_selection_cohorts_2026_09_23](../infra/immigration-fiscal/crime_selection_cohorts_2026_09_23/RESULT.md) `_cache/admin/{p00…p05,pjim00…pjim03,pji02,iofcjs00}.{pdf,txt}` (its `_cache/ipums/` extracts are hard links into the registered IPUMS USA store); Prisoners in 2023 in [state_priced_services_2026_09_29](../infra/immigration-fiscal/state_priced_services_2026_09_29/RESULT.md) `_cache/p23st.pdf` (same size as the registered copy in `.scratch/clarity-next-20260905/conduct-race/`) | jail Hispanic share corrected with self-report surveys (ladder 218); noncitizen counts against the 2000 census (196) | survey respondents reweighted on administrative race; no counts by origin |
| Brookings "Beyond Arrests" (September 2026) appendices and metro data table | [enforcement_rents_2025_2026_09_27](../infra/immigration-fiscal/enforcement_rents_2025_2026_09_27/RESULT.md) `_cache/web/{Beyond-Arrests-Appendices.pdf,Beyond-Arrests-Metro-Data.pdf}` | metro enforcement-surge indicator (ladder 245) | table transcribed from an image PDF; small rounding inconsistencies |
| Deportation Data Project ICE arrests FOIA file (2022-10-01 to 2026-08-06) and ICE AOR-to-county file | [enforcement_rents_2025_2026_09_27](../infra/immigration-fiscal/enforcement_rents_2025_2026_09_27/RESULT.md) `_cache/ice/{arrests-latest.parquet,ice-aor-county-shp.parquet}`, pins in `_cache/manifest.json` | state and AOR arrest rates against metro rent growth (ladder 245) | only 91.1% of 2024 arrests carry a state; state rates include border arrests |
| DHS OHSS Immigration Enforcement and Legal Processes Monthly Tables, November 2024 edition | [cj_use_allocation_2026_09_23](../infra/immigration-fiscal/cj_use_allocation_2026_09_23/RESULT.md) `_cache/ohss/ohss_monthly_tables_nov2024.xlsx`; [unauthorized_population_size_2026_09_19](../infra/immigration-fiscal/unauthorized_population_size_2026_09_19/RESULT.md) `_cache/sources/ohss_monthly_nov2024.xlsx` (same SHA-256) | Mexico shares of FY2024 book-ins and removals (ladder 188); FY2022–24 border releases (157) | series stops with the November 2024 edition; Mexico counts are by citizenship |
| FBI Crime in the United States (Crime Data Explorer): persons arrested and estimated crime 2020, 2023, 2024; offenses known 2023–2024; 2019 Table 43C | [nibrs_arrests_2026_09_16](../infra/immigration-fiscal/nibrs_arrests_2026_09_16/RESULT.md) `_cache/{persons-arrested-202{0,3,4}.zip,cius-estimations-202{0,3,4}.zip,offenses-known-to-le-202{3,4}.zip}`, unpacked `_cache/x/{pa2023,pa2024,est2023,est2024}/`; [crime_victim_cost_2026_09_23](../infra/immigration-fiscal/crime_victim_cost_2026_09_23/RESULT.md) `_cache/fbi_cius2019_table43c.xls` | adult arrests by offence and ethnicity (ladder 78); Hispanic murder-arrest share check (189) | non-Hispanic white arrests are constructed; the reporting panel grew since 2019 |
| FBI NIBRS state incident files, Texas, Arizona and California 2022–2023 (CDE bulk store), with CDE agency lists and UCR participation 1960–2025 | [offender_ethnicity_nibrs_2026_09_23](../infra/immigration-fiscal/offender_ethnicity_nibrs_2026_09_23/RESULT.md) `_cache/{TX,CA,AZ}-202{2,3}.zip`, `_cache/{cde_agencies_TX.json,cde_agencies_CA.json,cde_agencies_AZ.json,ucr_participation_1960_2025.csv}`, hashes in `derived/source_manifest.csv` | police-recorded offender ethnicity for the victim cost (ladder 202) | Hispanic, not Mexican origin; ethnicity partly from victims' and witnesses' descriptions |
| FBI Supplementary Homicide Reports 1976–2025, Murder Accountability Project compilation (`SHR76_25a.csv`) | [homicide_cost_2026_09_18](../infra/immigration-fiscal/homicide_cost_2026_09_18/RESULT.md) `_cache/SHR76_25a.csv` (sha256 in RESULT), `_cache/mapdocs.html` | victim-by-offender ethnicity, offender age and clearance, 2015–2023 (ladder 143) | covers 80% of WONDER homicide deaths; over-represents white victims in cleared cases |
| Jail populations by ethnicity: Colorado HB19-1297 county jail summary (September 2020); Connecticut, Delaware and NYC DOC open-data pulls | [crime_ratio_direction_2026_09_24](../infra/immigration-fiscal/crime_ratio_direction_2026_09_24/RESULT.md) `_cache/jail/{co_hb1297_2020_report.pdf,ct_pretrial_race_*.json,de_detention_20{19,23,24}.json,nyc_doc_race_counts.json}` | jail systems' Hispanic shares against adult parity (ladder 218) | — |
| LAPD arrests under LAMC 42.00 (street vending), 2010–2019 (Los Angeles open data) | [vending_restaurants_2026_09_24](../infra/immigration-fiscal/vending_restaurants_2026_09_24/RESULT.md) `_cache/lapd/lamc4200_arrests.json` | pre-law vending enforcement exposure by ZIP (ladder 223) | City of Los Angeles only |
| Minnesota program-fraud reports: Legislative Auditor special reviews (CCAP 2019, Feeding Our Future 2024, EIDBI 2026) and House Oversight staff report (June 2026) | [fraud_by_citizenship_2026_09_24](../infra/immigration-fiscal/fraud_by_citizenship_2026_09_24/RESULT.md) `_cache/mn/{ola_2019_ccap_fraud_allegations,ola_2024_mde_fof_special_review,ola_2026_dhs_eidbi_kickbacks_special_review,house_oversight_2026-06_mn_fraud_staff_report}.pdf` | Minnesota fraud amounts alleged, proven and recovered (ladder 214) | no document states any defendant's national origin, birthplace or citizenship |
| NCVS Select personal victimization (record level, 1993–2024) and personal population files, with codebook (BJS API) | [crime_ratio_direction_2026_09_24](../infra/immigration-fiscal/crime_ratio_direction_2026_09_24/RESULT.md) `_cache/ncvs/{ncvs_select_personal_victimization.csv,ncvs_select_population_year_race_region.csv,NCVS_Select_person_level_codebook.pdf}` | perceived offender ratios and police reporting against NIBRS (ladder 218) | offender ethnicity is perceived; only four census regions identified |
| USSC individual offender datafiles FY2015–FY2025 (CSV) with economic-crime files, codebooks and Sourcebook Table 9 (FY2019, FY2022) | [fraud_by_citizenship_2026_09_24](../infra/immigration-fiscal/fraud_by_citizenship_2026_09_24/RESULT.md) `_cache/ussc/opafy{15..25}nid_csv.zip`, `_cache/ussc/econ{15..25}_csv.zip`, `_cache/ussc/USSC_*_Codebook_*.pdf`, `_cache/ussc/sourcebook/table9_{2019,2022}.pdf` | fraud sentencing rates and guideline losses by citizenship (ladder 214) | citizenship, not nativity; federal cases only |

## Transport, environment and safety

The crash, traffic and pollution data are all held inside the lanes that priced those items.

### In analysis lanes

| Dataset and vintage | Where it is | Use | Limits |
|---|---|---|---|
| California Crash Reporting System (CCRS, CHP via data.ca.gov): crashes, parties and injured/witness/passenger files 2022–2024, with export layout | [ccrs_nonfatal_involvement_2026_09_28](../infra/immigration-fiscal/ccrs_nonfatal_involvement_2026_09_28/RESULT.md) `_cache/ccrs/{crashes,parties,injuredwitnesspassengers}_{2022,2023,2024}.csv.gz` (hashes in sibling `.json`), `_cache/rawdata_template.txt`, `_cache/ckan_ccrs.json` | at-fault odds of Hispanic drivers by quasi-induced exposure (ladder 264) | officer-entered race, no Mexican origin; no insurance field; incomplete local coverage |
| Insurance Research Council, uninsured and underinsured motorists 2017–2023, research summary | [road_crash_externality_2026_09_28](../infra/immigration-fiscal/road_crash_externality_2026_09_28/RESULT.md) `_cache/irc_um_uim_2017_2023.pdf` | national uninsured-driver rate (15.4% in 2023) | the state table sits in the paywalled full report, not retrieved |
| NHTS 2017 and 2022 (NextGen) public-use CSV (FHWA/ORNL), with 2017 replicate weights, codebooks and users' guides | [congestion_2026_09_23](../infra/immigration-fiscal/congestion_2026_09_23/RESULT.md) `_cache/nhts{2017,2022}_csv.zip`, `_cache/nhts2022_codebook.xlsx`; [main_case_candidate_v3_2026_09_28](../infra/immigration-fiscal/main_case_candidate_v3_2026_09_28/RESULT.md) `_cache/transit/nhts{2017,2022}_csv.zip` (same size), `_cache/transit/nhts2017_replicates_csv.zip`, `nhts{2017,2022}_users_guide.pdf`, codebooks; hashes in each lane's `manifest.json` | Hispanic driving, occupancy and peak ratios (ladder 195); transit all-trip adjustments (candidate v3) | Hispanic stands in for Mexican origin; 2022 Hispanic sample is 1,722 persons |
| NHTSA FARS 2023 national CSV (accident, person, vehicle, MIPER, driver and crash factors, violations) | [road_crash_externality_2026_09_28](../infra/immigration-fiscal/road_crash_externality_2026_09_28/RESULT.md) `_cache/FARS2023NationalCSV.zip`, unpacked `_cache/fars2023/FARS2023NationalCSV/`; its `_cache/FARS2022NationalCSV.zip` is truncated (see below) | culpability of the group's killed drivers, per-mile risk (ladders 264, 266) | origin recorded only for the dead, from death certificates |
| NHTSA reports: Blincoe et al. 2023 crash costs (DOT HS 813 403); Traffic Safety Facts 2023 (DOT HS 813 738); fatality disparities by race and ethnicity (DOT HS 813 188) | [road_crash_externality_2026_09_28](../infra/immigration-fiscal/road_crash_externality_2026_09_28/RESULT.md) `_cache/{blincoe_2023_dot_hs_813403.pdf,tsf2023.pdf,nhtsa_disparities_813188.pdf}` | crash cost base, national crash counts, per-mile fatality rates (ladders 264, 266) | Blincoe's comprehensive costs are 2019 levels |
| Our World in Data CO2 dataset (Global Carbon Budget), country-years to 2024 | [air_pollution_2026_09_28](../infra/immigration-fiscal/air_pollution_2026_09_28/RESULT.md) `_cache/owid-co2-data.csv` | US and Mexico consumption-based CO2 per head for the CO2 arm (ladder 260) | consumption-based series ends 2023; scaled to 2024 by the territorial ratio |
| TTI Urban Mobility Report 2025 workbook (2024 data), report and appendices A–D; 2023 report | [congestion_2026_09_23](../infra/immigration-fiscal/congestion_2026_09_23/RESULT.md) `_cache/complete-data-2025-umr-by-tti.xlsx`, `_cache/mobility-report-2025{,-appx-a,-appx-b,-appx-c,-appx-d}.pdf`, `_cache/mobility-report-2023.pdf`, hashes in `_cache/manifest.json` | network delay base and delay per urban area (ladder 195) | delay against overnight free flow; misses local streets and areas outside 494 urban areas |

## Identity, family history and attitudes

The family-history and attitude surveys supplied on September 17 are organized in the
[named library](../infra/immigration-fiscal/new_datasets_2026_09_17/library/README.md), generated by `organize.py`,
which accounts for every supplied file, equivalent later exports and the extracted ICPSR folder. Acquisition record:
[ACQUIRED.md](../infra/immigration-fiscal/new_datasets_2026_09_17/ACQUIRED.md) and the
[SHA-256 and member manifest](../infra/immigration-fiscal/new_datasets_2026_09_17/manifest.json). **Raw root** below
means `infra/immigration-fiscal/new_datasets_2026_09_17/raw/`. Codebooks and questionnaires sit beside the data where
supplied; derived text, dictionaries and tables are in the lane's ignored `derived/`. Sizes are compressed decimal MB.
Used in the [new-data audit](immigration-new-datasets-and-conclusions-2026-09-17.md) and the
[completed synthesis](immigration-organized-surveys-analysis-2026-09-17.md); commands in the
[lane README](../infra/immigration-fiscal/new_datasets_2026_09_17/README.md).

| Dataset and vintage | Where it is | Use | Limits |
|---|---|---|---|
| GSS cumulative file 1972–2024, R3a, as used for trust | `attitudes_gen_2026_09_16/raw/GSS_stata/gss7224_r3a.dta` (see the lane rows below); its hash and the selection's are in `frontier_execution_2026_09_17/derived/social/gss_provenance.json` | Trust with its denominator, nonresponse weights, design and corrected parental birthplace. `hispanic_0022` keeps the detailed origins that the simplified `hispanic` drops. Standard-TRUST second-generation observations across the 2000–22 waves: Mexican 310, Cuban 15, Salvadoran 10, Dominican 10, Colombian 6 (unweighted readiness counts; `gss_readiness.py`) | Conditional attitudes; the parent questions give US or foreign birth, not the country; identity attrition applies; a smaller-country second-generation trust ranking is not supported at these sizes |
| Opportunity Insights race tables (OI-RACE-T1, OI-RACE-T3-NATIVEMOM, OI-RACE-T5-INCOME) and Changing Opportunity tables (OI-CHANGING-PRIMARY, OI-CHANGING-SECONDARY) | `infra/immigration-fiscal/latam_comparison_2026_09_17/_cache/oi/`, with codebooks; URLs, times and SHA256 in `_cache/oi/manifest.json` | T1: parent-income percentile, race and sex, household income with a native-mother subset; T3: native-mother income transitions by race and sex; T5: parent and child income percentile-bin means; Changing Opportunity: national age-27 income and employment for the 1978–92 cohorts, plus schooling, marriage, mortality and parent outcomes | No country key and no parental-nativity or third-plus field; the native-mother restriction covers only its named household-income fields; a group's mean rank mapped through the nonlinear crosswalk is not its mean dollars; keep each outcome's age and window |
| Opportunity Insights country tables 6a and 6b | `oi_origin_regression_2026_09_16/race_table6a_parametric.csv`, `race_table6b_nonpar.csv`; codebooks in `latam_comparison_2026_09_17/_cache/oi/race_table6{a,b}_codebook.pdf` | Income ranks by country of origin: 6a has 51 country labels including the USA, 6b has 23 | No country crime, trust or employment. The paper's authorized-family sample frame ([§III.A](https://opportunityinsights.org/wp-content/uploads/2018/04/race_paper.pdf)) does not represent unauthorized families, and a table-specific exclusion of foreign-born children is unverified. The native-mother series is a benchmark, not a substitute for white third-plus |

### LNS_BRANTON_2015_V2_1 — author policy/protest derivative

- Source/acquired: [Harvard Dataverse DOI 10.7910/DVN/27113](https://doi.org/10.7910/DVN/27113), version 2.1,
  retrieved September 17 through the unrestricted public API.
- Local/size: raw root `lns_replications/branton_2015_social_protest/analysis.dta`, 1,089,708 bytes, 49 variables, with
  the author's do-file and source metadata.
  [Exact URLs, metadata, hashes and staging map](../infra/immigration-fiscal/new_datasets_2026_09_17/lns_replications/source_manifest.json).
- Units/variables/weight: LNS 2006 respondent derivative; 8,561 physical rows, 349 entirely blank, 8,212 nonblank, 8,169
  with generation. `generation`, `immpolinew`, `wt_nation_rev` revised national weight. No respondent ID; no
  cross-package merge.
- Use/quirks: descriptive legalization-option table under source-defined groups. The raw parent and grandparent
  reconstruction is absent; generation mixes citizenship with migration generation. An unexplained 422-record nonblank
  shortfall against the original 8,634 and a published benchmark mismatch mean this is not a reproduction of the full
  original study. [Analysis and primary coding evidence](immigration-lns-public-replications-2026-09-17.md).

### LNS_WALLACE_2014_V3_1 — author attitudes/protest projection

- Source/acquired: [Harvard Dataverse DOI 10.7910/DVN/SZK4NF](https://doi.org/10.7910/DVN/SZK4NF), version 3.1,
  September 17, unrestricted API. Same source manifest as above.
- Local/size: raw root `lns_replications/wallace_2014_spatial_temporal/analysis.dta`, 1,381,043 bytes; the author's
  do-file, replication codebook, the original LNS questionnaire and codebook, and repository metadata.
- Units/variables/weight: 8,634 rows, 30 variables, 8,634 unique nonmissing `respid`; a first-generation indicator,
  several origin indicators, government-attitude items and a derived party scale. **No weight.** The same N as the
  original does not by itself establish that the ID sets are equal.
- Use/quirks: a variable-availability and ID-validation target if the originals are acquired later. `partyid7` drops
  3,144 original "don't care" and "don't know/other party" cases, so it is not a whole-sample party balance. No
  second-versus-third distinction. No weighted national table and no matching to other derivatives.
  [Audit](immigration-lns-public-replications-2026-09-17.md).

### LNS_PEREZ_2011_V1_0 — author language-effects derivative

- Source/acquired: [Harvard Dataverse DOI 10.7910/DVN/1KWH3E](https://doi.org/10.7910/DVN/1KWH3E), version 1.0,
  September 17, unrestricted API. The author's article is kept for its source definitions.
- Local/size: raw root `lns_replications/perez_2011_language_effects/analysis.dta`, 696,494 bytes; README, variable
  notes, metadata and article. Exact bytes and SHA-256 are in the source manifest.
- Units/variables/weight: 7,688 respondents from the five largest origin groups, 22 variables; `second`, `third`
  (actually third-plus), party dummies and constructed identity and knowledge scales. A positive national `weight`
  exists, but whether it is the revised weight is unverified; no respondent ID.
- Use/quirks: the all-zero party-dummy group is a documented residual, not ignorable nonresponse. The README's
  `noparty` label conflicts with the paper and the original questionnaire; the paper identifies "don't care." Mexican
  origin as the all-zero origin baseline is supported by the paper's five-origin restriction, unlike the Branton
  residual. No weighted party finding is promoted while the weight vintage is unresolved.
  [Audit](immigration-lns-public-replications-2026-09-17.md).

### NLSY97_GEN_CRIME_20260917 — supplied exports and the full archive

- **Files:** the sibling `iq-sex-differences/data/nlsy/nlsy97_all_1997-2023.zip` (806-field extraction; archive and CSV
  SHA256 in the lane README) and three supplied NLS Investigator exports in the raw root: `nlsy97_gen_crime_1 (9).zip`
  (25.330 MB, nine members including `.csv`, `.cdb` and SAS/SPSS/Stata setup; `nlsy97_gen_crime_1.zip` is
  byte-identical), `nlsy97_gen_crime_2.zip` (8,974,865 bytes, 8,608 fields; its `(2)` and `(3)` copies are byte-identical) and
  `default.zip` (1,209,449 bytes). `gen_crime_2026.NLSY97` (160,060 bytes) is a variable-selection basket, not
  respondent data. [Official access](https://www.nlsinfo.org/content/access-data-investigator).
- **Coverage:** `default.zip` holds all 98 requested fields plus `R1235800` for the same 8,984 unique respondent IDs,
  with codebook coverage for every field, and all 97 requested non-ID columns match the full archive exactly
  ([source hashes and comparison](../infra/immigration-fiscal/new_datasets_2026_09_17/completion_check.json)).
  Cumulative arrest `E8033100`, incarceration `E8043100` and the incomplete-history flag `E8043601` agree with the
  archive, and 7,059 ability IDs validate. No further export is needed.
- **Family linkage:** the [corrected parent linkage](immigration-nlsy97-parent-linkage-2026-09-17.md) joins 104 selected
  source fields from the full archive on validated `PUBID`; unknown detailed family history falls from 7,759 to 3,266
  without assigning unknown branches as US-born. Provenance: `derived/nlsy_family/extraction.json` and
  `nlsy/parent_linkage_fields.NLSY97` in the intake lane.
- **Use:** design, AFQT and monthly crime history; exact IDs join earlier family and adult rows with overlap checks.
- **Limits:** public self-ID and generic birthplace do not recover restricted Mexico lineage; the public grandparent
  birthplace indicators distinguish the US and territories from outside, not Mexican birthplace; parent-country detail
  is unavailable, so there is no ancestry-complete Mexican group. The join with the archive is a verified same-person
  join, not an independent replication.

### PEW_NSL_2011 — earlier identity and immigration attitudes

- Source/acquired: Pew Research Center public-use release, supplied by the user September 17, 2026.
  [Pew datasets](https://www.pewresearch.org/datasets/); the packaged DOCX holds the questionnaire and methodology.
- Local/codebook/size: raw root `PHCNSL2011PubRelease.zip`, 0.469 MB, two members (updated SAV and DOCX); 1,220 records.
  Weight `weight`.
- Key variables: `qn4/qn7/qn8` own and parents' nativity; `qn54` typical American; `combo81_82` leaned party;
  immigration-policy items.
- Quirks/use: self-identified Hispanic adult cross-section, November–December 2011; no nonidentifier complement or
  validated panel link. Question dictionary inventoried by `pew/probe.py`; not in the 2015 paired analysis.

### PEW_NSL_2012 — identity, immigration policy and religion oversample

- Source/acquired: Pew Research Center, supplied by the user September 17, 2026;
  [dataset portal](https://www.pewresearch.org/datasets/).
- Local/codebook/size: raw root `PHCNSL2012PublicRelease.zip`, 6.050 MB, two members (updated SAV and DOCX); 1,765
  records. Weight `weight`.
- Key variables: `qn4/qn7/qn8` nativity, `qn31` DACA approval, `Combo61_62` leaned party.
- Quirks/use: September–October 2012 self-ID Hispanic cross-section, including a 438-person non-Catholic oversample, so
  unweighted pooling misrepresents composition. Inventoried; not a repeated-person panel or paired attrition sample.

### PEW_LATINO_RELIGION_2013 — religion, identity and nativity

- Source/acquired: Pew Research Center, supplied by the user September 17, 2026;
  [dataset portal](https://www.pewresearch.org/datasets/).
- Local/codebook/size: raw root `Pew-Research-Center-2013-U.S.-Latino-Religion-Survey.zip`, 1.125 MB; SAV plus separate
  codebook, background and questionnaire PDFs; 5,103 records.
- Key variables: `Q4/Q410/Q411` own and parents' nativity; `Q130` typical American; `Q105` effects of undocumented
  immigration. Weights `totalwt`, `form06wt`, `form12ncowt`.
- Quirks/use: the full weight is not interchangeable with the FORM-specific weights, and questionnaire routing changes
  item denominators. The self-ID sample cannot estimate nonidentifiers. Inventoried for later religion and attitude
  comparisons.

### PEW_NSL_2014 — mixed reported family origin

- Source/acquired: Pew Research Center, supplied by the user September 17, 2026;
  [dataset portal](https://www.pewresearch.org/datasets/).
- Local/codebook/size: raw root `Pew-Research-Center_2014-National-Survey-of-Latinos-Dataset.zip`, 1.062 MB; SAV, PDF,
  readmes and macOS metadata; 1,520 records. Weight `weight`.
- Key variables: `q52a/q52b` parents' Hispanic/Latino/Spanish origin; `q53` grandparents' origin; `q4/q7/q8` nativity.
- Quirks/use: wording differs from 2015; self-ID recruitment excludes nonidentifiers. ReadStat auto-decoding failed;
  explicit Latin-1 succeeded and is recorded. Inventoried as a mixed-heritage sensitivity source.

### PEW_NSL_2015 — identifying half of the ancestry comparison

- Source/acquired: Pew Research Center, supplied by the user September 17, 2026;
  [primary report and methodology](https://www.pewresearch.org/race-and-ethnicity/2017/12/20/methodology-hispanic-identity/).
- Local/codebook/size: raw root `Pew-Research-Center_2015-National-Survey-of-Latinos-Dataset.zip`, 1.295 MB; SAV,
  questionnaire and methodology PDF, readmes; 1,500 records. Weight `weights`.
- Key variables: `q10a/q10b` parent origin, `q11a/q11b` grandparent-origin pair counts, `q4/q7/q8` nativity and
  `q8aa/q8ab/q8ba/q8bb` grandparent nativity; `party_combo`, `q14`, `q16c`.
- Quirks/use: fielded October–November 2015; its partner is the 2015–2016 omnibus. Append the two with externally
  calibrated weights; never join numeric IDs. Grandparents' Hispanic origin is not Mexican birthplace. Analyzed by
  `pew/analyze.py`.

### PEW_NONHISPANIC_2015_2016 — nonidentifiers with reported ancestry

- Source/acquired: Pew Research Center, supplied by the user September 17, 2026;
  [methodology](https://www.pewresearch.org/race-and-ethnicity/2017/12/20/methodology-hispanic-identity/).
- Local/codebook/size: raw root `Pew-Research-Center_2016-Survey-of-Self-Identified-non-Hispanics-Dataset.zip`, 0.577
  MB; internal `NSL2015 Omnibus_FOR RELEASE.sav`, PDF and readmes; 401 records. Weight `OMNIWeight`.
- Key variables: `ha2a/ha2b/ha4/ha6` family-origin eligibility, `ha_combo`, nativity and grandparent fields,
  `party_combo`, `q16cx` Hispanic ancestry salience, `q22` ever personally identified as Hispanic.
- Quirks/use: every supplied `immgen` value is unknown, so reconstruct generation from the direct items and keep the
  unresolved cases. The ZIP's 2016 label is not its paired NSL year. Earlier-ancestor-only cases are included; the
  89/11 split and the published counts of 37.8m and 4.9m are external and cannot be recovered as prevalence from these
  401 records. Analyzed by `pew/analyze.py`.

### PEW_NSL_2016 — election and American-dream attitudes

- Source/acquired: Pew Research Center, supplied by the user September 17, 2026;
  [dataset portal](https://www.pewresearch.org/datasets/).
- Local/codebook/size: raw root `Pew-Research-Center_2016-National-Survey-of-Latinos-Dataset.zip`, 1.095 MB; SAV, PDF
  and readmes; 1,507 records. Weight `weights`.
- Key variables: `qn4/qn7/qn8` own and parents' nativity, `generations`, `party_combo`, election and American-dream
  questions.
- Quirks/use: August–September 2016 self-ID cross-section, not the omnibus's field period. No equivalent direct
  grandparent-origin battery located. Inventoried; not in the paired analysis.

### PEW_NSL_2018 — later attitude and identity cross-section

- Source/acquired: Pew Research Center, supplied by the user September 17, 2026;
  [dataset portal](https://www.pewresearch.org/datasets/).
- Local/codebook/size: raw root `Pew-Research-Center_2018-National-Survey-of-Latinos-Dataset.zip`, 5.084 MB, updated
  SAV and DOCX; 1,501 records. Weight `weight`.
- Key variables: `qn4/qn7/qn8`, `immgen`, identity and political items.
- Quirks/use: July–September 2018 self-ID Hispanic adults. No repeated-person linkage or matched grandparent-origin
  battery. Inventoried for question-level harmonization.

### PEW_US_MUSLIMS_2017 — 2017 Survey of U.S. Muslims, public use

- Source/acquired: Pew Research Center dataset download (questionnaire, codebook, SPSS file, full report), by the
  operator with a Pew account, September 22, 2026.
- Local/size: `sources/immigration-fiscal/data/external/pew/Pew-2017-US-Muslims.zip`, 6,121,578 bytes; SPSS
  `2017USMuslimPublicData - checked.sav`, 1,001 respondents, 222 variables; `Codebook`,
  `Muslim-American-Final-Questionnaire.pdf`, `U.S.-MUSLIMS-FULL-REPORT.pdf`. SHA256 in the raw-file manifest.
- Key variables: `respondent_birthregion2`, `father_birthregion2`, `mother_birthregion2` (birth countries collapsed to
  regions), `citizen`, `income` (2016 family income bands), `educrec`, `fertREC` (children ever born), `party`/`partyln`,
  attitude items (`qa2`, `qb2*`, `qc11*`), `weight` (main weight; further weights per the codebook).
- Quirks/use: self-identified Muslim adults only, 2017 cross-section; birthplace is a region, not a country; income is
  banded. The only US file observing religion with nativity and income that could be obtained quickly (HUMAN.md ask
  of September 21). Used in [`pew_muslims_2017_2026_09_22`](../infra/immigration-fiscal/pew_muslims_2017_2026_09_22/RESULT.md)
  (ladder 177).

### ICPSR_30302_V1 — New York second generation, DOCUMENTATION ONLY

- Source/acquired: supplied September 17, 2026; [official catalog](https://www.icpsr.umich.edu/web/ICPSR/studies/30302).
  Raw root `ICPSR_30302-V1.zip`, 2.737 MB, six members: codebook and questionnaire, catalog, manifest, bibliography,
  terms.
- Expected data: 3,415 cases × 428 variables; `30302-0001-Data.dta` is absent. The catalog requires a restricted-data
  agreement; filenames in a study manifest do not establish access or possession.
- Key variables: `ID`, `COB/AGEUS/MCOB/FCOB`, `MEDUC/FEDUC`, `ARRESTED/INCARCER`, `INGRPWT/WEIGHT/SAMEWT`.
- Quirks/use: selected local origins, ages 18–32, no Mexican analytic group; no general four-grandparent birthplace
  battery. A retrospective cross-section, not a parent-child panel. `icpsr/analyze_codebooks.py` verifies published
  marginal counts only.

### ICPSR_20862_V6 — Latino National Survey 2006, DOCUMENTATION ONLY

- Source/acquired: supplied September 17, 2026; [official catalog](https://www.icpsr.umich.edu/web/ICPSR/studies/20862).
  Raw root `ICPSR_20862-V6.zip`, 7.191 MB, ten members including four codebooks and two questionnaires. A second
  download, `ICPSR_20862-V6 (1).zip` (2,385,704 bytes), holds seven documentation files, all byte-identical to the first
  ([inventory and hashes](../infra/immigration-fiscal/new_datasets_2026_09_17/completion_check.json)).
- Expected data: 8,634 cases; public DS0001 has 275 columns and the public contextual DS0003 427. `20862-0001-Data.dta`
  and `20862-0003-Data.dta` are missing; DS0002/4 are restricted variants, not waves. The official access attempt
  returned HTTP 403, and the delivery page reports a non-member account restriction
  ([exact message and file checks](../infra/immigration-fiscal/new_datasets_2026_09_17/access-status.md)); identical
  browser retries will not clear it.
- Key variables: `CASEID/RESPID`, `BORNUS/BIRTHPLC`, `PARBORN/GRANBORN`, `PAREDUC`, `INCSUPP/HEALTH/GOVTRUST/PARTYID`,
  revised `WT_NATION_REV/WT_STATE_REV/WT_METRO_REV`.
- Quirks/use: the self-ID Latino frame misses nonidentifiers and non-Latino controls; a foreign-born grandparent count
  does not prove Mexican birthplace. DK codes can remain nominally valid in software metadata. No respondent arrest or
  incarceration outcome was established. Only marginal-frequency bounds were analyzed.

### MASP_AUTHOR_2019 — Mexican American Study Project family follow-up

**Source/acquired:** Edward Telles and Vilma Ortiz; 2026-09-20, the author-distributed Stata data acquired and parsed.
[Official project and download](https://www.edwardtelles.com/masp), [codebook](https://www.edwardtelles.com/new-page-1).
**Local:** `infra/immigration-fiscal/masp_2026_09_20/raw/`; two downloads, 24,552,591 bytes. Data: 1,850 rows × 2,560
fields, not 1,850 independent child respondents. [Hashes and recipe](../infra/immigration-fiscal/masp_2026_09_20/ACQUIRED.md).
**Key variables:** `v75` own birth country, `c28/c29` the nonrespondent parent's parents' birthplace,
`v25/v26.../v51` ethnic identification, `v348` family income, `v338` SSI, `c80/c94/c95...` schooling.
**Quirks:** a historical Los Angeles and San Antonio family follow-up, 1965–66 baseline and 1998–2002 follow-up. The
author labels the data 2019; the older ICPSR 28481 v2 codebook cannot establish identical variables, blanking or missing
codes. Identity needs a multiple-response and skip reconstruction, not `v25` alone.
**Executed:** the [MASP analysis](../infra/immigration-fiscal/masp_2026_09_20/RESULT.md) identifies 758 adult-child
interviews in 482 families and distinguishes initial ethnic mentions (`v12–v23`), preferred identity (`v25`) and the
race-form response (`v51`). It completes education, benefit and genealogy comparisons with an explicit informant-code
sensitivity; small nonidentifier-generation cells prevent a national correction. Also used in the
[ancestry-outcomes evidence update](immigration-ancestry-outcomes-evidence-2026-09-20.md).

### COHORT_X_NARRATIVES_20260905 — selective official API evidence

**Source:** the official X API, through the existing `x-api` skill. **Acquired:** 2026-09-05.
**Local:** `.scratch/cohort-clarity-20260905/x/`: four returned archives plus the query specification, source-check
results, cost record and hash manifest. Exact 90-day query window: June 7 10:50:43 UTC to September 5 10:50:43 UTC. 111
distinct returned posts, 103 new beyond the earlier 207-post sample; 310 unique across both. Local tally $0.555, vendor
invoice unverified.

This is purposive claim discovery, not representative opinion, and duplicated wording is not independent confirmation.
The [narrative audit](immigration-cohort-narratives-2026-09-05.md) grades five specific claims and records the
unresolved primary-source gaps.

### In analysis lanes

| Dataset and vintage | Where it is | Use | Limits |
|---|---|---|---|
| AAPI Data / APIAVote Asian American Voter Survey 2020, national crosstabs (PDF) | [indian_politics_2026_09_18](../infra/immigration-fiscal/indian_politics_2026_09_18/RESULT.md) `raw/aavs2020_crosstab.pdf` (unreadable, see below) | not used: party-ID figures stay secondhand via Carnegie footnotes (ladder 153) | the held PDF reports 0 pages; treat as not obtained |
| ANES 2020 Time Series (CSV release 2022-02-10) and ANES 2024 Time Series (CSV release 2026-05-19), with codebooks | [attitudes_gen_2026_09_16](../infra/immigration-fiscal/attitudes_gen_2026_09_16/RESULT.md) `raw/anes_timeseries_{2020_csv_20220210,2024_csv_20260519}{.zip,/}`; [norms_gen_2026_09_18](../infra/immigration-fiscal/norms_gen_2026_09_18/RESULT.md) reads it through its `raw/` symlink | group thermometers, immigration views and norms by Hispanic generation (ladders 104, 135) | weighted to citizen-eligible adults, so G1 cells are not the GSS's G1 |
| Census 2010 surname file (names.zip, Names_2010Census), via Wayback capture | [cultural_output_2026_09_19](../infra/immigration-fiscal/cultural_output_2026_09_19/RESULT.md) `_cache/surnames/{names.zip,names_wb.zip,Names_2010Census.xlsx,Names_2010Census.csv}` | imputing Hispanic origin of award winners from surnames (ladder 156) | cannot separate Mexican from other Hispanic origin or catch married-name changes |
| Correlates of State Policy Project v2.2 (MSU IPPSR) | [political_trajectory_county_2026_09_19](../infra/immigration-fiscal/political_trajectory_county_2026_09_19/RESULT.md) `_cache/correlatesofstatepolicyprojectv2_2.csv` | state immigration-related laws against Mexican-origin share (ladder 160) | no driver's-licence, E-Verify, sanctuary or 287(g) variables; party control ends 2011 |
| County presidential returns: MEDSL countypres 2000–2016 (MIT Election Data and Science Lab GitHub mirror) and tonmcg county results 2016, 2020, 2024 | [political_trajectory_county_2026_09_19](../infra/immigration-fiscal/political_trajectory_county_2026_09_19/RESULT.md) `_cache/countypres_2000-2016.csv`, `_cache/tonmcg_{2016,2020,2024}.csv`, route in `_cache/SOURCE_USED.txt` | county vote and turnout against Mexican-origin share growth (ladder 160) | ecological county regressions do not identify individual votes |
| CPS November Voting and Registration Supplement 2004–2024: public-use files 2020–2024 with replicate weights 2022, 2024; Census API pulls; P20 voting tables 2020–2024 | [civic_trajectory_mexican_2026_09_27](../infra/immigration-fiscal/civic_trajectory_mexican_2026_09_27/RESULT.md) `_cache/cps/{nov20pub.zip,nov22pub.zip,nov24pub.zip,nov22rep.zip,nov24rep.zip}`, `_cache/{cpsnov20.pdf,cpsnov22.pdf,cpsnov24.pdf,vote01_2020.xlsx,vote01_2022.xlsx,vote01_2024.xlsx}`; [indian_civic_cps_2026_09_18](../infra/immigration-fiscal/indian_civic_cps_2026_09_18/RESULT.md) Census API pulls of the 2016–2024 supplements `_cache/cps_voting_{2016,2018,2020,2022,2024}.json` (per-state parts in `_cache/parts/voting_<year>/`) and P20-585 Tables 1, 11–13 `_cache/p20_585_table{01,11,12,13}.xlsx`; [political_trajectory_county_2026_09_19](../infra/immigration-fiscal/political_trajectory_county_2026_09_19/RESULT.md) Census API pulls of the presidential-year supplements 2004–2024 `_cache/cps_voting_{2004,2008,2012,2016,2020,2024}.parquet` | turnout and registration by birthplace, origin and generation (ladders 152, 160, 233) | CPS over-reports Hispanic turnout relative to white; no 2020 replicate weights |
| CPS September Civic Engagement and Volunteering Supplement 2019–2023: public-use and replicate-weight files 2021 and 2023; Census API pulls 2019–2023; AmeriCorps CEV national rates | [service_by_ses_2026_09_23](../infra/immigration-fiscal/service_by_ses_2026_09_23/RESULT.md) `_cache/cps/sep{21,23}{pub,nrrep}.{zip,csv}`, `_cache/cps/cpssep23.{pdf,txt}`; [indian_civic_cps_2026_09_18](../infra/immigration-fiscal/indian_civic_cps_2026_09_18/RESULT.md) Census API pulls `_cache/cps_volunteer_{2019,2021,2023}.json` (per-state parts in `_cache/parts/volunteer_<year>/`), `_cache/americorps_cev_national.csv`; its `_cache/pub/sep23{pub,nrrep}.csv` are truncated (see below) | volunteering, giving and veteran status by generation and birthplace (ladders 152, 205) | small subgroups (170 Indian second-generation respondents); giving asks no amount |
| DoD, Population Representation in the Military Services, FY2023 Appendix B and FY2022 Table B-41 | [service_by_ses_2026_09_23](../infra/immigration-fiscal/service_by_ses_2026_09_23/RESULT.md) `_cache/poprep_fy23_appendix_b.pdf`, `_cache/poprep_fy22_b41.pdf` | enlisted accessions by home-tract income quintile; recruits' schooling (ladder 205) | enlisted accessions only, by home-of-record tract rather than ZIP |
| GSS cumulative 1972–2024, release R3a (Stata, NORC), with codebook and release notes | [attitudes_gen_2026_09_16](../infra/immigration-fiscal/attitudes_gen_2026_09_16/RESULT.md) `raw/GSS_stata.zip`, `raw/GSS_stata/gss7224_r3a.dta`; [norms_gen_2026_09_18](../infra/immigration-fiscal/norms_gen_2026_09_18/RESULT.md) reads it through `raw/`, a symlink to attitudes_gen's `raw/`; read in place by [frontier_execution_2026_09_17](../infra/immigration-fiscal/frontier_execution_2026_09_17/README.md) (social), whose `derived/social/gss_provenance.json` the register's GSS row cites without a path | attitudes, trust and institutional confidence by Hispanic generation (ladders 87, 135) | Hispanic item only from 2000; ISSP immigration items fielded in some years only |
| Wikidata award-winner statements, 27 categories (Academy, Pulitzer, National Book, Grammy, Tony, MacArthur, National Medal of Arts), fetched 2026-09-19 | [cultural_output_2026_09_19](../infra/immigration-fiscal/cultural_output_2026_09_19/RESULT.md) `_cache/awards/*.json` | Mexican-origin share of canon and award winners 1990–2025 (ladder 156) | secondary compilation; year qualifier missing for 35–54% of some awards' rows |

## International

Cross-country and origin-country data beyond the migration surveys above.

| Dataset and vintage | Where it is | Use | Limits |
|---|---|---|---|
| Derived tier-A context tables: UN WPP population forecast, demographic push, IMF GDP per capita panel, OECD social spending, bilateral migration skill panel, Borjas and BGH cells, Razin–Wahba; Borjas supply-shock panel (derived) | `sources/immigration-fiscal/derived/stage6/*.csv` (8 files), `sources/immigration-fiscal/derived/tier_a/borjas_supply_shock_panel.csv` | written by `build/build_tier_a_context_panels.py` (stage6) and `build/build_borjas_supply_shock_panel.py` (tier_a); cited in `acs_schooling_break_2026_09_26/triage_b.md` | derived, rebuildable |
| OECD SOCX aggregate social expenditure, % of GDP, 1980–1995 (JSON, 274 MB) | `sources/immigration-fiscal/data/external/oecd/socx_agg_pct_gdp_1980_1995.json` | fetched by `acquire/setup-tier-a-labor-demography.sh`; read by `build/build_tier_a_context_panels.py` | — |
| UN World Population Prospects location list (UN Data Portal API, 300 locations) | `sources/immigration-fiscal/data/external/un_wpp/locations.json` | fetched by `acquire/setup-tier-a-labor-demography.sh`; read by `build/build_tier_a_context_panels.py` | location codes only; no population series |
| World Bank WDI GDP per capita, constant 2015 US$ (NY.GDP.PCAP.KD), by country (API JSON) | `sources/immigration-fiscal/data/external/tier_a/worldbank_gdp_pcap_kd.json` | API cache read by `build/build_tier_a_context_panels.py` (`WB_CACHE`) | — |

### In analysis lanes

| Dataset and vintage | Where it is | Use | Limits |
|---|---|---|---|
| Barro-Lee educational attainment dataset v3, both sexes (BL_v3_MF) | [selection_curve_2026_09_27](../infra/immigration-fiscal/selection_curve_2026_09_27/RESULT.md) `_cache/BL_v3_MF.csv` | immigrants' percentile in their origin cohort's schooling distribution (ladder 236) | tertiary defined differently from Wittgenstein for rich European origins |
| BEA direct investment by country, 2020–2025: US direct investment abroad (position, detailed country) and foreign direct investment in the US | [trade_networks_2026_09_28](../infra/immigration-fiscal/trade_networks_2026_09_28/RESULT.md) `_cache/{usdia-position-2020-2025.xlsx,usdia-detailedcountry-2020-2025.xlsx,fdius-detailedcountry-2020-2025.xlsx}` | pricing investment and trade ties with Mexico as a benefit (ladder 265) | network-created share and excess return are assumed, capped by BEA's 2024 returns |
| ESRU-EMOVI 2017 social mobility survey (CEEY): respondent and household files with dictionary | [world_ledger_2026_09_27](../infra/immigration-fiscal/world_ledger_2026_09_27/RESULT.md) `_cache/mexico/esru_emovi_2017_bases.zip`, unpacked `_cache/mexico/emovi/` | schooling given parents' schooling for the second-generation counterfactual (ladder 250) | — |
| IEA TIMSS 2015 grade 4 student background files (SPSS) and user guide; TIMSS 2011/2015 grade 4 and PIRLS 2011/2016 almanacs | [pisa_germany_2026_09_27](../infra/immigration-fiscal/pisa_germany_2026_09_27/RESULT.md) `_cache/grade4/t15_g4_spss/ASG*M6.sav`, `_cache/grade4/T15_UserGuide.pdf`, `_cache/grade4/{T15_G4,T11_G4,P16,P11}_Almanacs.zip`, extracted `_cache/grade4/x/` | grade-4 immigrant-background shares by country (ladders 243, 246) | only TIMSS 2015 has parental birthplace; other cycles carry proxies |
| INEGI census schooling tabulations: XII Censo 2000 national education characteristics, Censo 2010 state tables, Encuesta Intercensal 2015 education workbook | [schooling_selection_position_2026_09_23](../infra/immigration-fiscal/schooling_selection_position_2026_09_23/RESULT.md) `_cache/inegi/cpv2000/CPyV2000_NAL_Caracteristicas_educativas.pdf`, `_cache/inegi/cpv2010/07_{08,10,11,12,14}B_ESTATAL.xls`, `_cache/inegi/eic2015/06_educacion.xls`; its IPUMS `_cache/us_mexborn*.data.csv.gz` are hard links to the register's store (extracts 3, 12, 13) | Mexico's schooling distribution by cohort, to rank Mexican arrivals (ladder 197) | five-year age tabulations, not microdata; 2015 lacks grades by age |
| INEGI ENIGH 2024 (nueva serie) microdata: persons, household summary, income and jobs | [world_ledger_2026_09_27](../infra/immigration-fiscal/world_ledger_2026_09_27/RESULT.md) `_cache/mexico/enigh2024_ns_{poblacion,concentradohogar,ingresos,trabajos}_csv.zip`, unpacked `_cache/mexico/enigh/` | Mexican labour income for the place premium and Mexico's tax side (ladder 250) | records take-home pay, grossed up here by 2024 withholding |
| INEGI ENOE 2024, quarters 1 and 2, sociodemographic files | [world_ledger_2026_09_27](../infra/immigration-fiscal/world_ledger_2026_09_27/RESULT.md) `_cache/mexico/{enoe_2024_trim1_csv.zip,enoe_2024_trim2_csv.zip}`, `_cache/mexico/enoe/ENOE_SDEMT{124,224}.csv` | cross-check on Mexican earnings, hours and employment (ladder 250) | first two quarters only; INEGI's server refuses the later files |
| OECD PISA 2015 and 2022 student questionnaire files (SPSS) | [pisa_germany_2026_09_27](../infra/immigration-fiscal/pisa_germany_2026_09_27/RESULT.md) `_cache/microdata/{stu2015_spss,stu2022_spss}.zip`, unpacked `_cache/microdata/{CY6_MS_CMB_STU_QQQ.sav,CY08MSP_STU_QQQ.SAV}` | shares of recently arrived pupils by country, 2015 and 2022 (ladders 243, 246) | Sweden 2022 has no arrival ages and drops out |
| OECD PISA results volumes (2009 II, 2012 II, 2015 I, 2018 II, 2022 I) and their StatLink tables | [pisa_germany_2026_09_27](../infra/immigration-fiscal/pisa_germany_2026_09_27/RESULT.md) `_cache/pisa20{09,12,15,18,22}_vol*.{pdf,txt}`, `_cache/reg_pisa20{12,15}_vol*`, `_cache/statlink_*.xls*` | country immigrant shares and native scores for cross-country slopes (ladders 243, 246) | ecological design with 37 countries; 2022 volume tables start in 2012 |
| Pew Research Center, Future of World Religions country table, 2010–2050 | [admission_route_2026_09_21](../infra/immigration-fiscal/admission_route_2026_09_21/RESULT.md) `_cache/pew_religious_composition_2010_2050.xlsx` | origin country's 2010 Muslim share as predictor (ladder 171) | describes the origin country, not its emigrants in the US |
| Remittances to Mexico: Banxico remittance release (December 2024) and SIE tables CE81, CE164, CE167 (2022–2025); BEA International Transactions 2024–2026; CEMLA and BBVA notes; USCIS H-2B FY2024 characteristics | [remit_leak_2026_09_16](../infra/immigration-fiscal/remit_leak_2026_09_16/RESULT.md) `_cache/trans424.{pdf,txt}` (BEA, fourth quarter and year 2024), `_cache/banxico_dic2024.pdf`, `_cache/cemla_2025-03.pdf`; [consumption_key_2026_09_24](../infra/immigration-fiscal/consumption_key_2026_09_24/RESULT.md) `_cache/sources/corridor/{banxico_*,bea_*,uscis_h2b_fy24_characteristics,cemla_*,bbva_*}.{xlsx,pdf}`, `_cache/sources/cemla_2018_migracion_mexicana.pdf` | 2024 transfers abroad and inflows to Mexico (ladder 90); remittance outflow calibration (225) | BEA's $69.9bn and Banxico's $62.5bn disagree; Banxico records the remitter's country only |
| SHCP tax incidence by decile ("Distribución del pago de impuestos y recepción del gasto público"), editions 2024 and 2026; public finance report January–December 2024 | [world_ledger_2026_09_27](../infra/immigration-fiscal/world_ledger_2026_09_27/RESULT.md) `_cache/reads/{shcp_ig_2024.pdf,shcp_ig_2026.pdf,shcp_fp_202412.pdf}` | Mexico's consumption-tax incidence for the group's taxes in Mexico (ladder 250) | IEPS read from chart labels to one decimal; base is national-accounts income |
| Wittgenstein Centre Human Capital Data Explorer v3, SSP2 population by age and education | [selection_curve_2026_09_27](../infra/immigration-fiscal/selection_curve_2026_09_27/RESULT.md) `_cache/wic_v3_ssp2_pop-age-edattain.rds` | origin schooling where Barro-Lee lacks the country (ladder 236) | tertiary defined differently from Barro-Lee for rich European origins |
| World Bank WDI series via API: Mexico and US 2015–2024 (PPP factors, GDP, population, taxes, consumption, health and education spending, homicide), trade, GDP per head PPP by country | [world_ledger_2026_09_27](../infra/immigration-fiscal/world_ledger_2026_09_27/RESULT.md) `_cache/mexico/wdi_*.json`; [trade_networks_2026_09_28](../infra/immigration-fiscal/trade_networks_2026_09_28/RESULT.md) `_cache/{wb_gdp.json,wb_NE.EXP.GNFS.CD.json,wb_NE.IMP.GNFS.CD.json}`; [pisa_germany_2026_09_27](../infra/immigration-fiscal/pisa_germany_2026_09_27/RESULT.md) `_cache/wb_gdppc_ppp_kd.json` | PPP conversion and Mexico checks (ladder 250); trade scale (265); GDP control (243, 246) | — |

## Replication packages and papers

| Dataset and vintage | Where it is | Use | Limits |
|---|---|---|---|
| Seven working papers, primary PDFs and text | `mr_leads_papers_2026_09_21/_cache/<slug>.pdf` and `.txt`; tracked reading notes in `notes/` | Estimates with page and table references (each note's files-covered section); [papers memo](immigration-marginal-revolution-leads-read-2026-09-21.md) | Working-paper versions; two published versions were not opened; image-only figures gave no numbers |
| Meyer, Wyse and Williams 2026, homelessness article | Primary PDF in `frontier_execution_2026_09_17/raw/local/`, hash recorded | Published direct and indirect Table 1 arithmetic | No raw respondents and no incumbent-displacement estimate; the estimators are not confidence limits |
| H-2B final July 2026 paper and appendix | `frontier_execution_2026_09_17/policy/raw/`, [manifest](../infra/immigration-fiscal/frontier_execution_2026_09_17/policy/manifest.json) | First-stage, reduced-form and IV source-table arithmetic | Raw package not retrieved; response, survival and spillover limits |
| Bracero raw mirror, primary paper and appendix | `frontier_execution_2026_09_17/policy/raw/bracero-mirror/`; [Git tree, blob and SHA256 record](../infra/immigration-fiscal/frontier_execution_2026_09_17/policy/epoch2-sources.json) | State and month exposure and wage re-estimation with an independent solver | [DEGRADED] Original Stata identity unverified; the employment sample and coefficients fail to reproduce |
| Danzer 2024, main paper and supplement | Primary PDFs and text in `frontier_execution_2026_09_17/policy/raw/`, with source hashes | Annual count coefficients and a covariance-conservative geometric ratio | No raw rows, fitted counterfactual counts or joint covariance; no cumulative-count estimate |
| Swiss citizenship, discovery only | Author and PMC snapshots in `frontier_execution_2026_09_17/raw/swiss/`, [access record](../infra/immigration-fiscal/frontier_execution_2026_09_17/social/swiss/acquisition.json) | Documents the public routes inspected | [DEGRADED] No usable author data: the supplement returned HTML and Dataverse 403; no regression reproduced |
| Literature on immigration's fiscal effects under `lifetime/` (AEI, AER, Bank of Canada, Brookings, CGD, CReAM, Dallas Fed, EconStor, FRBSF, IMF, NBER, NRC; 40 NBER working papers) | `sources/immigration-fiscal/data/external/lifetime/aei/`, `sources/immigration-fiscal/data/external/lifetime/aer/`, `sources/immigration-fiscal/data/external/lifetime/banqueducanada/`, `sources/immigration-fiscal/data/external/lifetime/brookings/`, `sources/immigration-fiscal/data/external/lifetime/cgdev/`, `sources/immigration-fiscal/data/external/lifetime/cream/`, `sources/immigration-fiscal/data/external/lifetime/dallasfed/`, `sources/immigration-fiscal/data/external/lifetime/econstor/`, `sources/immigration-fiscal/data/external/lifetime/frbsf/`, `sources/immigration-fiscal/data/external/lifetime/imf/`, `sources/immigration-fiscal/data/external/lifetime/nber/`, `sources/immigration-fiscal/data/external/lifetime/nrc/` | catalogued by `build/build_lifetime_evidence_warehouse.py`, which lists every file under `lifetime/`; nber, cgdev, dallasfed and econstor papers also cited by `build/mine_restrictionist_full_claims.py`, `build/run_sweeps_23_32.py` or review notes | `aer/lee_miller_2000_…pdf` is a zip holding an AEA disclosure statement, not the paper; `nrc/nrc_1997_new_americans.pdf` is the NAP HTML page |
| Other paper sets: Cortés on low-skilled immigration and prices or women's labour supply (2005 WP, NBER w31234, AEJ appendix); Treasury OTA TP-5 (2012) and WP-115 (2017); NBER w21399 and w35680 on survey under-reporting; AHRQ WP 17003 reconciling MEPS and NHEA | `sources/immigration-fiscal/data/external/papers_consumer_price/`, `sources/immigration-fiscal/data/external/corporate_incidence/`, `sources/immigration-fiscal/data/external/underreporting/`, `sources/immigration-fiscal/data/external/meps_nhea/` | no script reads them; `ledger_underreport_2026_09_16/underreport.py` transcribes w35680 Table 4 figures | HTML pages saved as `.pdf`: `papers_consumer_price/{cbo_marginal,fh,furtado_hock_2010,liser_brief}.pdf`, and `corporate_incidence/t`; `treasury_ota_wp5.pdf` is OTA WP 5 (1976) on charities, not incidence |

These sources are compared across studies, not joined as if they held the same people.

### OPENICPSR_114757_V1 — Saiz–Wachter original housing replication

**Source:** Albert Saiz and Susan Wachter / American Economic Association, openICPSR.
**Acquired:** 2026-09-19, authenticated browser download after the operator approved the download terms.
**Official:** [Project 114757, V1](https://www.openicpsr.org/openicpsr/project/114757/version/V1/view), DOI 10.3886/E114757V1.
**Local path:** `infra/immigration-fiscal/hedonic_replay_2026_09_19/_cache/original/` (ignored).
**Codebook:** labels in `DATAAEJPOLICY_MS_2009_191.dta`, the main and supplemental `.do` files and the packaged README.
**Size:** five files; ZIP 41,152,145 bytes; `.dta` 105,273,639 bytes, 102,766 rows × 248 fields.
[Hashes and provenance](../infra/immigration-fiscal/hedonic_replay_2026_09_19/ACQUIRED.md).

**Key variables:** `dloval`/`dlomval` changes in log mean and median house value; `dforeigncap` change in foreign-born
share; `l1own` initial owner-unit weight; `tract`/`year` unique row key; `msayear` fixed effect; `immicapmsa` metro
inflow rate; `cha*`/`Ql1*` housing controls; `pull`/`pulli`/`pullmsa` supplied gravity instruments.

**Known quirks:** only 1990 and 2000 rows, representing prior-decade changes. This is a prepared analysis file, with no
upstream Geolytics or gravity build code. Historical keys need validated crosswalks before any modern ACS join. The
archived baseline has 43 controls against 44 in the prose; column 1 and the appendix first-stage Ns differ from the
printed tables; the main column 4 F remains unresolved. Source details and the separate matched-row mean and median
checks are in the [replay note](immigration-hedonic-replay-2026-09-19.md).

**Used in:** the replay note and the lane's `src/original_replay.py` and `src/verify_original.py`. Six historical
coefficients and SEs, stronger-IV F and J diagnostics and the appendix median estimate are recovered by an
independently checked Python translation. No native Stata run or upstream-data reconstruction is claimed.

### OPENICPSR_113382_V1 — Chalfin 2015 Mexican-inflow crime panel

**Source/acquired:** Aaron Chalfin, AEA, openICPSR; the operator's existing download, verified 2026-09-20.
[Official record](https://doi.org/10.3886/E113382V1).
**Local:** `infra/immigration-fiscal/causal_execution_2026_09_20/raw/chalfin/`.
**Size:** archive 138,701 bytes; data 259,427 bytes, 276 × 172, 92 MSAs, 1980, 1990 and 2000.
[Hashes and acquisition recipe](../infra/immigration-fiscal/causal_execution_2026_09_20/README.md).
**Variables:** `FMSA`, `year`, initial-population `popweight`, the prepared instrument `dins`, exposure `dmexfb_alt`,
offense counts and the supplied `dlogpc_*` outcomes.
**Quirks/use:** `dlogpc_*` numerically equals the change in log counts, not rate levels; exposure equals 100 × the
change in `mexfba`, whose exact age definition is undocumented. Crime and Census geographies differ; there is no
per-arrival dollar conversion. Prepared upstream instrument only.
[Seven-model replay and sensitivities](immigration-causal-execution-2026-09-20.md).

### In analysis lanes

| Dataset and vintage | Where it is | Use | Limits |
|---|---|---|---|
| Card, Rothstein and Yi (2023, NBER w31587) public commuting-zone place-effects file, 691 CZs | [scale_spillovers_2026_09_23](../infra/immigration-fiscal/scale_spillovers_2026_09_23/RESULT.md) `_cache/L3_czeffects.dta` | city-size and college-share earnings gradients, reproducing CRY Table 3 (ladder 201) | premia are CRY's best linear predictions, so regression SEs are too small |
| Cremieux, "America's Bad Cities Are Costing You" agglomeration–crime replication package, OSF node xzfdw, version 4 (2026-09-07) | [agglom_crime_2026_09_17](../infra/immigration-fiscal/agglom_crime_2026_09_17/RESULT.md) `_cache/repl.zip`, unpacked in `_cache/pkg/replication/agglomeration_crime_replication/` | tracing the $888 density-loss and $392 crime-wave arithmetic (ladder 96) | no raw data (about 20 GB, fetch scripts only); scripts not rerun |
| Light, He and Robey (PNAS 2020) replication package, openICPSR 124923-V1: Texas felony arrest charges by immigration status, 2012–2018 | [crime_cost_firstgen_2026_09_18](../infra/immigration-fiscal/crime_cost_firstgen_2026_09_18/README.md) `_cache/light_texas/` (unzipped from `sources/immigration-fiscal/data/external/crime_frontier/light_texas/124923-V1.zip`, the package behind the register's warehouse table `crime_tx_arrests_by_status`) | cost-weighted felony arrest rates by immigration status (ladder 144) | felony arrest charges, not convictions or distinct incidents |

## Not held

### Restricted or gated

| Dataset | What it would add | Access |
|---|---|---|
| Census survey–IRS/SSA linkages; detailed CMS Medicare and Medicaid records | Approved linkages could validate earnings, taxes and health spending | Restricted: US residency and security requirements, an approved project and DUA, possible fees; overseas access is prohibited under the checked routes ([verified routes and gates](../infra/immigration-fiscal/fiscal_access_2026_09_20/RESULT.md)). Public claims fields alone would not identify Mexican generations |
| LEHD worker histories | Labor-market trajectories | FSRDC approval |
| SSA Earnings Suspense File microdata | Unauthorized workers' payroll contributions | Restricted |
| ICE ERO removals by criminality × origin panel | Criminal-removal composition and enforcement intensity | The annual reports give headlines only; the panel needs the dashboard Excel export |
| ICPSR 30302 and ICPSR 20862 respondent data | Second-generation and Latino outcomes | Documentation only; see their cards |
| ORR/ASR microdata | Refugee outcomes | Restricted |
| Add Health | Second-generation networks and outcomes | Tiered; network data restricted |

### Blocked or not acquired

| Dataset | What it would add | Blocker |
|---|---|---|
| PSID | Long-run earnings and intergenerational dynamics | Registration and browser flow |
| Synthetic SIPP | A public proxy for admin-linked earnings histories | Only the landing page and documentation were found |
| IRS SOI individual public-use file | Federal tax microsimulation | Only the limitations paper is held (`external/lifetime/irs/irs_soi_puf_limitations_06resconf.pdf`) |
| LAPOP US 2019 microdata | Trust and victimization | The [official codebook](https://www.vanderbilt.edu/center-for-global-democracy/data/?lp_download=2273) (DOI `10.15695/lapop/CGD1387`; `latam_comparison_2026_09_17/_cache/social/lapop-us2019-codebook.pdf`, 181,681 bytes, SHA256 `92f809fd4935041d2e22b87dc638e0c079e7c5d590b5dc323b385cdc0c105e57`) lacks detailed origin and parent birthplace, so the microdata were not acquired |
| Pew 2008 Latino crime and police-contact survey | Victimization and police contact | Login-gated; detailed-country coverage unverified |

### Lost, not rebuilt, or on the SSD only

The causal raw layer disappeared from the SSD in mid-August 2026. The analyses that used these files were withdrawn on
2026-09-05, so they were deliberately not re-fetched; if one of those questions reopens, rebuild from raw under the
corrected method.

| Dataset | What it held | Status |
|---|---|---|
| QWI county receiver panel, 2017Q1–2024Q4 | County-quarter employment and earnings by education and industry in receiver states | Lost; its specification (industries, education groups, counties) was never recorded. The state panel is held |
| ACS 2024 receiver-exposure PUMA layer; receiver-node kill-test outputs | Post-surge exposure screen; nine-node synchronized-pressure screen | Lost with the 68 causal analysis outputs |
| BPS compiled file (`BPS_Compiled_202601.zip`), HUD HIC 2007–2024, county QCEW 2017–2024, OHSS enforcement workbook of November 2024 | Threshold and receiver inputs | Lost, not re-fetched. County permits for 2025–July 2026 and HUD PIT by CoC are held |
| April 2026 derived layers: school-service district and state tables, the parsed SAIPE district table, the ELSi English-column probe, the CCD 2024–25 bundle inventory, the SIPP low-skill calibration extract, the origin CSVs | School-side and origin context | No tracked builder produces them, so the September rebuild did not regenerate them; the origin data live on as context-warehouse tables |
| EOIR case data, the February 2026 extract labelled 2026-0301 (6.5 GB) | Immigration court load by court, date, nationality, proceeding and application | SSD corpus only (`eoir_case_data_2026_02`); EOIR's FOIA library has since listed a July 2026 release ([availability memo](immigration-recent-cohort-data-availability-2026-09-05.md)). Court venue is not the respondent's residence, and the raw data need code-key joins |
| LEHD LODES | Workplace × residence flows | SSD corpus only (`census_lehd`) |

### Open leads

These come from the June 2026 roadmaps and were checked on 2026-09-29. Since June the project has acquired
Light/He/Robey, the USSC 2024 tables and the USSC offender files, SPI2016, SCAAP, NIS Round 1, CILS, NCVS, NIBRS, the
GSS, Zillow, the OI tables and the state E-Verify mandate dates (coded in `compliance_gap_2026_09_24/everify.py`); all
appear above. The June scouting memos were deleted on 2026-09-29; the INDEX tombstones give the commits to recover
them from. The [gated-data specifications](immigration-gated-data-specs-2026-06-25.md) stay.

| Lead | What it would add | Status and route |
|---|---|---|
| Abramitzky, Boustan, Jácome and Pérez, intergenerational mobility 1880–2015 (openICPSR 120490; [AER 2021](https://www.aeaweb.org/articles?id=10.1257/aer.20191586)) | Father–son rank mobility by origin country | Not held; the NBER working papers w26408 and w22381 are held as PDFs in `external/lifetime/nber/`. Route in `crime_frontier/MANUAL_ACQUIRE.md` |
| Census Annual Business Survey, owner characteristics (`abscbo`, 2023) | Business ownership by US birth and citizenship × industry × geography | Not held; `setup-crime-frontier.sh` fetches it once `CENSUS_API_KEY` is set |
| Wharton land-use regulation index 2018 | The 2006→2018 change in regulation | Not held; the 2006 index (WRLURI) is in the Saiz file |
| Arizona immigration status, crime and victimization, 2007–23 (ICPSR 39107) | Person-level status data outside Texas | Not held; ICPSR login and DUA |
| BJS National Corrections Reporting Program, 1991–2021 (ICPSR 39234) | Corrections flows | Not held; ICPSR login |
| Secure Communities activation dates by county and month | The staggered-rollout instrument | Not held; `causal_evidence_2026_09_20` holds only the Gonçalves–Jácome–Weisburst paper text |
| DHS Yearbook enforcement tables | Enforcement flows | Not held; Yearbook LPR tables are held in lanes |
| TRAC immigration series | Court, detention and enforcement FOIA series | Not held |
| OECD International Migration Outlook, fiscal chapter | Cross-country fiscal benchmark | Not held |
| USPTO PatentsView with inventor nativity | Innovation channel | Not held |
| SSA Earnings Public-Use File (1% CWHS, 1951–2006) | Long earnings histories | Not held; route in `crime_frontier/MANUAL_ACQUIRE.md` |
| Statistics Canada IMDB, table 43-10-0026 | Fiscal outcomes by admission category and source country | Not held; route in `crime_frontier/MANUAL_ACQUIRE.md` |
| NAWS public data | Farmworker work-authorization status | Not held; route in `crime_frontier/MANUAL_ACQUIRE.md` |
| DOL OFLC disclosure data | H-1B, PERM and H-2A wages by occupation and state | Not held; route in `crime_frontier/MANUAL_ACQUIRE.md` |
| HHS ORR unaccompanied-children portal data | Counts and costs of unaccompanied children | Not held; the FY2021 annual report is held |
| NIS Round 2 (ICPSR 38061) | The follow-up of the 2003 new-LPR cohort | Not held; public use since 2024 |

## Do not use without checking

These categories are high-risk for bad inference:

1. `ACS alone` for lifetime fiscal claims.
2. `CPS population levels` for recent foreign-born stock changes without checking fixed controls.
3. `ITEP` as a full fiscal estimate; it is a tax estimate.
4. `CBO surge reports` as if they were the same object as the settled undocumented stock.
5. Any file flagged as an HTML trap: the list in `sources/immigration-fiscal/data/MANIFEST.md`, and five pages saved
   with `.pdf` names in `sources/immigration-fiscal/data/external/state_medicaid/` (`cbo_emergency_medicaid.pdf`,
   `cbo_emergency_medicaid_2024.pdf`, `d.pdf`, `dhcs_may2024_local_assistance_estimate.pdf`,
   `co_jbc_hcpf_figsetting_fy2627.pdf`). The real CBO emergency-Medicaid letter (257,767 bytes) is in
   `infra/immigration-fiscal/medical_ethnicity_pooled_2026_09_23/_cache/`.
6. `Census government finance, financial administration (E23), FY2022 on`. National current operations run $53.6bn in
   2021, $97.3bn in 2022 and $96.3bn in 2023: the July 2026 re-release of the 2022 unit file and the 2023
   state-by-level file carry a new level (NYC alone +$9.4bn; Wisconsin, New York and California ×3–5). The 2024 unit
   file keeps the new level: NYC $9.8bn, and Chicago up from $0.16bn in 2021 to $4.5bn, 30% of its total. Cook County
   government and Massachusetts show no break [DATA:
   `infra/immigration-fiscal/migrant_shelter_costs_2026_09_23/derived/census_e23_by_unit.csv`]. The published 2022
   Table 1 shows $70.7bn. Windows ending in 2022 or later need an ex-administration check; see
   `infra/immigration-fiscal/gg_response_county_iv_2026_09_23/e23_other_lanes.py`. BEA NIPA Table 3.17 shows no break
   of that size. BEA's state and local tax collection and financial management (Table 3.16, line 83) grew 26% in 2021
   and 30% in 2022, then 5%: a two-year surge rather than a step, worth at most $1.2–1.7bn on the September 23 case if
   all of it were an artifact. It was not recomputed on the September 27 case, where general government is a finite
   removal at 0.60–0.85.
7. Files in analysis lanes that are broken or unusable (paths relative to `infra/immigration-fiscal/`):
   - `indian_civic_cps_2026_09_18/_cache/pub/sep23pub.csv`: CPS September 2023 public-use CSV cut off mid-record at 5.6 MB. The full 152.3 MB file is `service_by_ses_2026_09_23/_cache/cps/sep23pub.csv`.
   - `indian_civic_cps_2026_09_18/_cache/pub/sep23nrrep.csv`: the matching replicate-weight CSV, cut off mid-record at 6.7 MB. The full 80.8 MB file is `service_by_ses_2026_09_23/_cache/cps/sep23nrrep.csv`.
   - `onbooks_share_2026_09_23/_cache/note151.pdf`: an SSA "Access Denied" HTML page saved with a `.pdf` name. The real Actuarial Note 151 is `note151_wb.pdf` in the same folder.
   - `onbooks_share_2026_09_23/_cache/lr2026.pdf`: an SSA "Access Denied" page in place of the 2026 long-range model documentation.
   - `onbooks_share_2026_09_23/_cache/tas2024.pdf`: the Taxpayer Advocate Service home page (HTML) saved with a `.pdf` name.
   - `onbooks_share_2026_09_23/_cache/actnotes.html`: an SSA "Access Denied" page in place of the actuarial notes index.
   - `remit_leak_2026_09_16/_cache/trans125.pdf`: a BEA "page not found" HTML page saved with a `.pdf` name.
   - `remit_leak_2026_09_16/_cache/ft900_dec2024.pdf`: a Census "Page not found" HTML page saved with a `.pdf` name.
   - `indian_politics_2026_09_18/raw/aavs2020_crosstab.pdf`: the 2020 Asian American Voter Survey crosstabs; `pdfinfo` reports 0 pages and the lane treats it as not obtained.
   - `road_crash_externality_2026_09_28/_cache/FARS2022NationalCSV.zip`: truncated download (curl exit 56) with no zip directory; the lane uses FARS 2023.
   - `school_dilution_2026_09_24/_cache/f33/elsec22.txt`: Census's FY2022 F-33 text file is a partial upload (1,729 of 14,105 rows); the lane uses `elsec22.xlsx`.

## Revisions

- **2026-09-17, supplied survey batch:** Registered all 13 supplied files in the cards below; two NLS ZIPs are exact
  duplicates, and both new ICPSR ZIPs contain documentation only. `sources` now resolves to `/Users/alien/research-data`,
  superseding the September 5 symlink-status observation above. This batch is physically staged inside the
  repository's analysis directory; no old warehouse availability claim is inferred from that symlink repair.
- **2026-09-05:** Registered the new 2019 baseline, actual 2024 path, price/calibration inputs, bounded RPC reports and
  targeted X sample. Corrected the empty-CPS-mirror statement and qualified the older synthetic-cohort identification
  claim under the [cohort decision](../decisions/2026-09-05-arrival-cohort-comparison.md). SIPP 2025 is officially
  available for reference 2024 but has not yet been acquired or incorporated.
- **2026-09-05, later expansion:** Acquired and analyzed SIPP 2025/CPS 2025/MEPS 2024, completed national admission
  distributions and race-stratified products, and promoted corrected crime categories/counts with the invalid rate
  withdrawn. This supersedes the earlier same-day acquisition limits above; see the
  [measurement/ledger decision](../decisions/2026-09-05-measurement-and-ledger-boundaries.md).
- 2026-09-16 to 09-28 (recorded 2026-09-29): the causal raw layer was found lost from the SSD, and the QWI state panel,
  CBP encounters and IRS 2022–23 migration were re-fetched; raw and derived trees moved to the Mac disk and the
  warehouses were rebuilt (09-16). `sources/` became a physical directory, and ACS 2019, SAINC35, AHS and GFD were
  recovered and verified ([storage notes](../notes/immigration-storage-cleanup-2026-09-20.md)); MASP was analyzed, and
  the SIPP lineage audit withdrew the Mexican-country inference (09-20). The NIS key-variable sections were corrected
  (09-22). The ACS no-schooling break was documented (09-23) and refined (09-26). IPUMS USA extracts 16–17 arrived
  outside the store (09-25).
- 2026-09-29 ([decision](../decisions/2026-09-29-delete-superseded-and-cruft-docs.md)): rewritten by domain.
  Statuses corrected: the NAS report, IPUMS CPS parental birthplace, Pew Muslims, MASP, the ICE workbooks, QWI,
  English-learner counts, receiver-city costs, the SSA note and ACS 2024's local path. SSD-only and lost files moved to
  Not held, and the June roadmap was merged into its open leads and deleted. Data held in 97 lanes and 41 `sources/`
  directories that the register had not named were added; 13 more unnamed lanes hold only literature or
  derived caches. Concept affected: which datasets the project holds and
  where.

### PEW_UNAUTHORIZED_MOTHER_BIRTHS_2026 — Annual births, 1990–2023

**Source:** Pew Research Center, March 31, 2026. **Acquired:** 2026-10-02.
**Official:** [Published birth table](https://www.pewresearch.org/chart/sr_26-04-31_birthrightscotus/).
**Local:** `infra/immigration-fiscal/school_growth_1975_2025_2026_10_02/inputs/pew_births.csv`;
raw HTML in that lane's ignored `_cache/pew_births.html`.
**Size:** 34 annual rows, three columns. Public published aggregate table.
**Variables:** Year; all births to unauthorized mothers; subset whose father is
neither a citizen nor lawful permanent resident. Both count columns are in **thousands**.
**Quirks:** Rounded to 5,000; survey/imputation estimates, not individual observed status.
Births are not surviving resident children; excludes births after maternal legalization
and births to lawful mothers with unauthorized fathers. No parental arrival-window filter.
**Used in:** [School-demand reconstruction](../infra/immigration-fiscal/school_growth_1975_2025_2026_10_02/README.md).
`extract_births.py` reproduces the table from cached HTML; `build.py` ages cohorts and
models subsequent maternal descendants. No education or ethnicity proxy is used.

### MPI_CHILDREN_UNAUTHORIZED_COUNTIES_2016 — Enrollment and parent status

**Source:** Migration Policy Institute,2016. **Acquired:**2026-10-02.
**Official:** [County workbook](https://www.migrationpolicy.org/sites/default/files/publications/Children-of-Unauthorized-CountyData.xlsx).
**Local:** `infra/immigration-fiscal/school_growth_1975_2025_2026_10_02/_cache/Children-of-Unauthorized-CountyData.xlsx`.
**Documentation:** workbook cover sheet; public published aggregate tables.
**Variables:** county/national child counts, parent-status groups, citizenship,
enrollment by ages3–4,5–11,12–14,15–17. ACS2009–13 pooled with SIPP2008 status imputation.
**Quirks:** enrollment combines public/private schools; historical, not current.
Parent-status children require a co-resident parent; not all descendants.
**Used in:** `school_growth_1975_2025_2026_10_02/los_angeles.py`, matched LA County/US shares.

### NCES_PUBLIC_ENROLLMENT_HISTORY_PROJECTION — National enrollment context

**Source:** NCES Digest 2003 table 3; Digest 2023/2025 table 203.10.
**Acquired:** 2026-10-02. **License:** public published aggregates.
**Official:** [Historical table](https://nces.ed.gov/programs/digest/d03/tables/dt003.asp),
[latest observed table](https://nces.ed.gov/programs/digest/d25/tables/dt25_203.10.asp),
[projection table](https://nces.ed.gov/programs/digest/d23/tables/dt23_203.10.asp).
**Local:** `school_growth_1975_2025_2026_10_02/_cache/nces_{d03,d23,d25}_20310.html`
under `infra/immigration-fiscal/`; three HTML tables including source notes.
**Variables:** fall year, public pre-K–12/ungraded enrollment, grade counts;
source counts in thousands. Annual observed totals 1975–2024; old projections
through 2031. `counterfactual.py` parses and hashes the raw inputs.
**Quirks:** early pre-K underreporting and recent state imputations; old forecast
levels differ from recent observations. Rebased/extended values through 2035
are our scenario. No immigration status in these tables. The subtracted demand
model is partial and covers ages 5–17, so its residual is not native-only.
**Used in:** [national school comparison](../infra/immigration-fiscal/school_growth_1975_2025_2026_10_02/README.md#national-total-versus-partial-removal-2026-10-02).
