# Immigration — Dataset Register

This is the working register for the immigration project. It is not the byte-level storage manifest. For raw-file inventory and trap-file warnings, see `sources/immigration-fiscal/data/MANIFEST.md`. For datasets we **don't have yet** (acquisition targets, crime + benefit-side gaps), see `research/immigration-dataset-roadmap.md`.

**Verified storage update, 2026-09-05:** `sources` currently points to a missing SSD offload directory. Historical paths below describe the older layout and are not proof of current availability. Verified fiscal raw root: `/Volumes/2TBPNY/research-data/immigration-fiscal/data`; corrected derived root: `/Volumes/2TBPNY/research-data/immigration-fiscal/derived`. Local warehouses remain in `warehouse/`. The [repair report](immigration-material-repair-report-2026-09-05.md) governs corrected outputs; the [recent acquisition memo](immigration-dataset-proxy-refresh-2026-09-05.md) binds new files to hashes and source definitions.

## What exists already

Yes, there is a raw data manifest:

- `sources/immigration-fiscal/data/MANIFEST.md`

No, before this file there was not a concise use-case register that told an agent:

1. what each dataset is for,
2. whether it exists locally,
3. where the local copy lives,
4. what question it can and cannot answer.

That is what this file is for.

## Reproducing downloads (git-tracked)

**Entry point:** `./scripts/reproduce-immigration-data.sh` (or `infra/immigration-fiscal/reproduce.sh`)

```bash
./scripts/reproduce-immigration-data.sh init
./scripts/reproduce-immigration-data.sh doctor
./scripts/reproduce-immigration-data.sh all minimal    # ~2 GB → immigration_context.duckdb
./scripts/reproduce-immigration-data.sh all standard   # full public stack
```

Guide: `infra/immigration-fiscal/REPRODUCE.md` — tiers, manual-acquire list, verify modes.

`research/sources` is an SSD symlink — **not in git**. Scripts + manifest live at:

- **`infra/immigration-fiscal/`** — `reproduce.sh`, `acquire/setup.sh`, `DOWNLOAD_MANIFEST.tsv`
- `acquire/config.env.example` — portable `$HOME/research-data/...` defaults
- `acquire/config.local.env` — machine overrides (gitignored)

Key builders: `build_immigration_warehouse.py`, `build_stage5_local_cost_context.py`, `compose_scenario_ledger.py`.

## Core local warehouse

| Dataset / asset | Local path | Status | Primary use | Main limit |
|---|---|---|---|---|
| Immigration context DuckDB | `warehouse/immigration_context.duckdb` | Fiscal/housing repairs rebuilt 2026-09-05; unrelated inputs preserved | State/origin/county context and consistent person-level donor projections | Partial descriptive accounting; not a lifetime causal model |
| Lifetime evidence DuckDB | `warehouse/immigration_lifetime_evidence.duckdb` | Relevant definitions, mined labels and shared-source imports repaired 2026-09-05 | Source catalog, unverified extracted claims, unadjudicated proposals, annual and lifetime benchmark tables | No row-level join to papers; units, assumptions and source confidence stay explicit |
| Fiscal union DuckDB | `warehouse/immigration_fiscal_union.duckdb` | Rebuilt 2026-09-05 | Materialized tensor/scenario tables plus cross-domain views | Rebuild after either parent changes; keep scenario and unit keys |
| Unified DuckDB | `warehouse/immigration.duckdb` | Rebuilt from the three repaired domain warehouses | Schema-qualified `context`, `lifetime`, `fiscal` tables and `_catalog` | Copies preserve source scope; query success does not establish causal validity |
| DuckDB build script | `infra/immigration-fiscal/build/build_immigration_warehouse.py` | Git-tracked | Rebuild core + stage2 + federal microsim | Stage2 housing from CHAS Table 11 when zip present; ACS PUMA fallback |
| ACS 2024 receiver exposure PUMA layer | `sources/immigration-causal/data/derived/acs_2024_receiver_exposure/acs_2024_receiver_exposure_puma.parquet` | Local, built | First post-surge PUMA exposure screen for receiver states | Public-use PUMA geography; no undocumented status |
| Receiver-node kill-test outputs | `sources/immigration-causal/data/outcomes/analysis/receiver_node_kill_test/` | Local, built | Nine-node synchronized-pressure screen across ACS, EOIR, QWI, shelter/capacity, and politics | Screening table only; PUMA bridge is area-weighted and EOIR venue is not residence |
| Origin extension assets | `sources/immigration-fiscal/data/derived/origin/` | Local | Origin ontology, stock, rent, OHSS derived tables | Mostly stock/admin layers, not unauthorized status |
| Stage 2 derived assets | `sources/immigration-fiscal/data/derived/stage2/` | Local, rebuilt 2026-06-18 | County/PUMA bridge, housing stress, school finance, IRS migration | CHAS via Playwright + `cp/` portal; ACS proxy if zip missing |
| MEPS health-cost module 2023 | `sources/immigration-fiscal/data/derived/stage3_proto/meps_health_cost_module_2023.csv` | Local, built | Public MVP payer-incidence table by age x nativity x insurance | Descriptive module only, not lifetime or legality-specific |
| ACS education-bucket totals 2023 | `sources/immigration-fiscal/data/derived/stage3_proto/acs_foreign_born_education_bucket_totals_2023.csv` | Local, built | Weighted foreign-born `25-64` stock totals for `<HS`, `HS / GED`, and `some college / associate` | Foreign-born stock only, not undocumented or lifetime |
| ACS education-bucket state shares 2023 | `sources/immigration-fiscal/data/derived/stage3_proto/acs_foreign_born_education_state_shares_2023.csv` | Local, built | State shares within each of the three education buckets | Same scope limits as above |
| Stage 3 prototype assets | `sources/immigration-fiscal/data/derived/stage3_proto/` | Local | Prototype local microsim context | Prototype only, not production-ready |

## Core public microdata

| Dataset | Local path | Status | What it answers | What it cannot answer cleanly |
|---|---|---|---|---|
| ACS 2023 PUMS person | `sources/immigration-fiscal/data/census/acs_pums_2023_person.zip` | Local | Composition, education, geography, commute, household structure, income proxies | Lifetime trajectories, undocumented status |
| ACS 2023 PUMS household | `sources/immigration-fiscal/data/census/acs_pums_2023_household.zip` | Local | Household and housing context | Same as above |
| ACS 2024 1-Year PUMS person/household | `/Volumes/2TBPNY/corpus/census_acs_2024_1yr/` | Actual raw ZIPs verified 2026-09-05; national person analysis complete | Recent-entry resident profiles, birthplace, education, employment, earnings and 80 replicate weights | Earlier causal-staging pointer is unavailable; no legal status, religion or ideology; see new acquisition cards below |
| CPS ASEC 2024 March | `sources/immigration-fiscal/data/census/cps_asec_2024_march.zip` | Local | Cross-checks on income, insurance, benefits | Weak for recent immigration-flow levels |
| Local ACS mirror | `/Volumes/2TBPNY/corpus/census_acs/csv_pus.zip` | Local SSD mirror | Faster direct ACS work outside repo zip flow | External path, not repo-contained |
| Local CPS mirror | `/Volumes/2TBPNY/corpus/census_cps/` | Local SSD mirror | CPS cross-checks | Same CPS limitations |

## Fiscal benchmark sources

| Dataset / source | Local path | Status | Primary use | Main limit |
|---|---|---|---|---|
| CBO federal immigration report 2024 | `sources/immigration-fiscal/data/cbo/60569-immigration-federal.pdf` | Local | Federal budget and macro effects of recent surge | Aggregate, not person-level |
| CBO state/local report 2025 | `sources/immigration-fiscal/data/cbo/61256-immigration-state-local.pdf` | Local | State/local taxes, spending, broader crowding effects | Surge-specific, not a general immigrant stock model |
| ITEP 2024 PDF | `sources/immigration-fiscal/data/itep/ITEP-Tax-Payments-by-Undocumented-Immigrants-2024.pdf` | Local | Tax contributions of undocumented immigrants | Tax side only |
| ITEP structured tables | `sources/immigration-fiscal/data/itep/itep_table_*.tsv` | Local | State-by-state tax extraction | No spending side |
| IRS Data Book table | `sources/immigration-fiscal/data/irs/24dbs01t02nr.xlsx` | Local | Tax-filing context | Not immigrant-specific |
| SSA actuarial note | `sources/immigration-fiscal/data/ssa/actuarial_note_151.pdf` | Local | Unauthorized-worker contribution context | Aggregate only |
| NCES per-pupil spending | `sources/immigration-fiscal/data/nces/tabn236.10.xlsx` | Local | Education cost anchors | Not immigrant-specific |
| Pew 2025 unauthorized report | `sources/immigration-fiscal/data/pew/pew-unauthorized-immigrants-2025.pdf` | Local | Population-size and composition anchor | Report PDF, not clean machine tables |
| NAS 2017 full report | `$PNY_DATA_ROOT/external/lifetime/nas/nas_2017_immigration_economic_fiscal_full.pdf` | Local PDF verified and read 2026-09-05; separate catalog HTML also present | Individual/descendant lifetime scenarios and annual fiscal definitions | Price year, age, public-goods allocation, generations and baseline emigration must remain explicit |

## Enforcement and budget sources

| Dataset / source | Local path | Status | Primary use | Main limit |
|---|---|---|---|---|
| EOIR Case Data 2026-0301 | `sources/immigration-causal/data/external/eoir_case_data_2026_02/eoir_case_data_feb2026.zip` | Local, staged, integrity-checked | Immigration court load by court/date/nationality/proceeding/application after extraction | Court venue is not respondent residence; raw admin data needs code-key joins |
| CBP budget justifications | `sources/immigration-fiscal/data/dhs/cbp_fy25_budget_justification.pdf`, `.../cbp_fy26_budget_justification.pdf` | Local | Federal enforcement-cost context | Attribution to unauthorized immigrants is inferential |
| ICE budget justifications | `sources/immigration-fiscal/data/dhs/ice_fy25_budget_justification.pdf`, `.../ice_fy26_budget_justification.pdf` | Local | Same | Same |
| USAspending enforcement extracts | `sources/immigration-fiscal/data/usaspending/` | Local | Time series of DHS sub-agency obligations | Program mapping still rough |

## Labor-market and housing context

| Dataset / source | Local path | Status | Primary use | Main limit |
|---|---|---|---|---|
| LEHD QWI county receiver panel 2017Q1-2024Q4 | `sources/immigration-causal/data/lehd/qwi_county_receiver_panel.parquet` | Local, built | County-quarter employment, stable employment, payroll, and earnings by education/industry in receiver states | QWI is not immigrant-status data; exposure must be joined from other layers |
| BLS QCEW 2023 annual | `sources/immigration-fiscal/data/bls/qcew_2023_annual_by_industry.zip` | Local | Sector employment/wage context | Industry totals, not immigrant composition |
| Extracted QCEW sector files | `sources/immigration-fiscal/data/bls/extracted/2023.annual.by_industry/` | Local | Focus sectors such as construction and hospitality | Same |
| FHFA state HPI | `sources/immigration-fiscal/data/external/fhfa_hpi_po_state.txt` | Local | Owner-side housing context | State-level only |
| HUD SAFMR FY2025 (zip-level) | `sources/immigration-fiscal/data/external/stage5_net_negative/hud/fy2025_safmrs_revised.xlsx` | Local, acquired 2026-06-18 | Zip-code rent caps for voucher/local burden | Playwright fetch |
| SAFMR panels (zip/county/PUMA/state) | `derived/stage5/safmr_{zip,county,puma,state}_2025.csv` | Built | PUMA/state rent context for stage5 warehouse | ZCTA→county→PUMA via Census crosswalks |
| HUD CHAS 2018–2022 county CSV | `sources/immigration-fiscal/data/external/stage2/hud/chas/2018thru2022-050-csv.zip` | Local, acquired 2026-06-18 | County share with 1+ of 4 housing problems (Table 11) | Needs Playwright session fetch; not welfare scalar |
| ACS state rent JSON | `sources/immigration-fiscal/data/external/origin/census_acs1_2023_state_median_gross_rent.json` | Local | Renter-side housing context | State-level only |
| Zillow ZORI + ZHVI metro panels 2015–2026 | `external/urban_housing/zillow/metro_{zori,zhvi}_*.csv` | **Local, acquired 2026-06-25** (`setup-urban-housing.sh`) | 739-metro MONTHLY rent (ZORI, repeat-rent ACS-weighted) + home-value (ZHVI) panel — the Wilson-Zhou (2026) housing outcome var; join to ACS foreign-born-share by CBSA → the rent-incidence panel (E-001…E-008) | Asking-rent index (new leases) ≠ contract rent; CBSA-level → needs Geocorr PUMA↔CBSA for the warehouse PUMA bridge |
| `msa_rent_elasticity_panel` (derived table) | context warehouse | Rebuilt 2026-09-05 (`build_msa_rent_elasticity_panel.py`) | Zillow rent/home-value trajectory × Saiz elasticity with a fixed January 2016–December 2025 window | Approximate first-city/state join is not a validated CBSA crosswalk; a bivariate null does not identify demand or immigration effects; see `immigration-msa-rent-elasticity-panel-2026-06-25.md` |
| Local burden examples | `research/immigration-state-local-cost-examples-ny-ca-tx.md` | Memo, not raw data | Concrete burden illustrations | Not a reusable database |

## Program and household-transition data

| Dataset / source | Local path | Status | Primary use | Main limit |
|---|---|---|---|---|
| SIPP 2024 public-use | `$PNY_DATA_ROOT/external/stage3/census/sipp/pu2024_csv.zip`; verified local staging `.scratch/data/external/stage3/census/sipp/` | Reacquired from Census 2026-09-05; SSD copy also present | Person-month earnings and explicitly linked benefit units, reference year **2023** | Not a household-total donor for each adult; no clean legal-status panel; see provenance below |
| SIPP documentation | Same staging: `pu2024_schema.json`, `2024_SIPP_Data_Dictionary.pdf`; SSD also contains user guide | Verified 2026-09-05 | EEDUC, monthly age, benefit owner/member links, annual weighting | Codebook defines units; file label 2024 is not the income/tax reference year |
| SIPP 2023 public-use | `sources/immigration-fiscal/data/external/stage2/census/sipp/pu2023_csv.zip` | Local | Earlier staging/calibration | Same |
| SIPP calibration extract | `sources/immigration-fiscal/data/derived/stage2/sipp_foreign_low_skill_calibration_2023.csv` | Local | Calibration input for stage 2 | Derived, not source-of-record |
| MEPS HC-251 | `sources/immigration-fiscal/data/external/stage3/ahrq/meps/` | Local | Medical spending and payer incidence | Not immigrant-status rich by itself |
| MEPS health-cost module 2023 metadata | `sources/immigration-fiscal/data/derived/stage3_proto/meps_health_cost_module_2023.meta.json` | Local, built | Value labels, row counts, and build notes for the MEPS module | Metadata only, not the module table itself |
| SIPP 2024 public MVP cells | `sources/immigration-fiscal/data/derived/stage3_proto/sipp_public_mvp_cells_2024.csv` | Local, built | Working-age nativity/citizenship/education transition cells for SIPP scenario scaffolding | Public file has no clean legal-status panel |
| SIPP→MEPS bridge cells 2024 | `sources/immigration-fiscal/data/derived/stage3_proto/sipp_meps_bridge_cells_2024.csv` | Local, built | Join layer mapping SIPP cells to MEPS age/nativity/insurance health-cost cells | No undocumented-specific inference introduced |
| SIPP→MEPS expected health-cost cells 2024 | `sources/immigration-fiscal/data/derived/stage3_proto/sipp_meps_expected_health_cost_cells_2024.csv` | Local, built | Collapsed per-SIPP-cell expected payer-spend profile used by public MVP | Not itself a final lifetime estimate |
| IRS SOI mirror | `/Volumes/2TBPNY/corpus/irs_soi` | Local SSD mirror | Federal tax microsim backbone | External path, confidentiality edits; re-stage if missing |

### SIPP 2024 acquisition and interpretation revision — 2026-09-05

**Source / access:** Census public-use files, reacquired 2026-09-05. **Primary data:** [pu2024_csv.zip](https://www2.census.gov/programs-surveys/sipp/data/datasets/2024/pu2024_csv.zip), 102,122,301 bytes, SHA256 `3a78b26988c76c02b9e206f72507390fb6ec9dac7974ec31aa90abc9d9809764`. **Schema:** [pu2024_schema.json](https://www2.census.gov/programs-surveys/sipp/data/datasets/2024/pu2024_schema.json), 757,529 bytes, SHA256 `601042d6f32e4c8ccd98952e91d0e25dc02d22d2dcb8babd4a2c269046d87b3d`. **Dictionary:** [2024_SIPP_Data_Dictionary.pdf](https://www2.census.gov/programs-surveys/sipp/tech-documentation/data-dictionaries/2024/2024_SIPP_Data_Dictionary.pdf), 4,015,396 bytes, SHA256 `f7af93a5b75fc6c3b67ca9c8aad7de78c32d071aa829b682f01312a3f46c7289`. The three source files total 106,895,226 bytes. [SOURCE: Census downloads and local SHA256]

**Paths verified:** `.scratch/data/external/stage3/census/sipp/` is the local repair staging directory. The connected drive has the original ZIP/schema under `/Volumes/2TBPNY/research-data/immigration-fiscal/data/external/stage3/census/sipp/`. The old repository `sources` symlink points to an absent offload directory; that path is not evidence a dataset is absent. Use the configured data root. [SOURCE: filesystem inspection 2026-09-05]

**Key definitions:** `EEDUC` 31–38 = less than high school; 39 = HS/GED; 40–42 = some college/associate; 43–46 = BA+. `TAGE_EHC` is reference-month age. `TPEARN` may include negative business income. SNAP/TANF amounts are held on the named benefit owner, with covered members identified by the owner/member fields; SSI is individual. Household and benefit-unit totals must not be copied to every ACS adult. Annual donors use reference-year earnings and the appropriate annual weight. [SOURCE: Census dictionary and user guide]

**Used in:** `infra/immigration-fiscal/build/build_federal_microsim_sipp_2024.py` and `build_public_mvp_sipp_module_2024.py`. This acquisition supports the [material inference repair](../decisions/2026-09-05-material-inference-repair.md); it replaces the earlier donor interpretation, not the original raw observations. September person donors, monthly profiles, health bridge and scenario exports have been rebuilt. Donor grids now contain 64 cells each; [nativity/support decision](../decisions/2026-09-05-person-donor-support.md). Historical `_usborn` keys mean the ACS native definition, including citizenship at birth abroad. Raw MEPS was not re-estimated; retained aggregate means have corrected source labels and an explicitly approximate birthplace bridge.

## September 2026 datasets and proxy checks

All new source snapshots live in `.scratch/frontier-20260905/datasets/`, are gitignored, and have URLs, acquisition/verification times, units, license notes and SHA-256 hashes in `manifest.json`. The [acquisition script](../infra/immigration-fiscal/acquire/refresh-frontier-20260905.py) reuses verified files and refuses altered cached sources. Eighteen source/documentation/provenance files were staged across three dataset families; BEA was already present. [DATA: manifest and inspection]

| Dataset | Verified local asset and vintage | Variables / keys | Principal check and limitation |
|---|---|---|---|
| BLS CPS nativity monthly | `bls/`; January 2021–August 2026 | Eight 16+ national series: population, employed, employment/population and unemployment; nativity × month | 544 rows, eight missing October 2025 values preserved; matched calendar-month comparisons. Not legal status; NSA and 2026 population-control break prevent a causal displacement inference. [BLS Table A-7](https://www.bls.gov/webapps/legacy/cpsatab7.htm) |
| Census county BPS | `bps/`; 2025 annual and May–July 2026 monthly | Authorized residential units, reported versus estimated; state/county FIPS × period | Four actual data files inspected. Permits are not completions; reported units are a subset, not an extra quantity to add. [Census files](https://www2.census.gov/econ/bps/County/) |
| ICE detention via Vera archive | `ice/`; July 20 workbook with July 11 observation cutoff and matched processed series | Stocks, book-ins, book-outs and removal exits; fiscal year/month | June 34,551 total exits / 27,679 removal exits reconciled to raw workbook. July partial; detention exits are not all national removals. Pinned tree `a6bf48e2627323f01827d52776f0d08023c410ba`; retain license restrictions on dissemination. [Archive](https://github.com/vera-institute/ice-fytd-stats) |
| BEA SAINC35, existing | `/Volumes/2TBPNY/corpus/bea_data/SAINC/SAINC35__ALL_AREAS_1929_2024.csv` | Gross transfer receipts; GeoFIPS × LineCode × year, thousands of dollars | 780 hierarchy checks across 60 geographies in 2024 balance; nested and memorandum lines overlap. Neither recipient nativity nor tax side is observed. [BEA regional data](https://www.bea.gov/data/economic-accounts/regional) |

Source details, exact file names, bootstrap/failure tests and `principal_checks.json` are in the [dataset refresh](immigration-dataset-proxy-refresh-2026-09-05.md). New paper PDFs and X evidence are registered separately in the [paper](immigration-recent-papers-2026-09-05.md) and [narrative](immigration-recent-narratives-2026-09-05.md) memos; retrieval counts are not counts of independent causal studies.

## Origin and legal-channel layers

| Dataset / source | Local path | Status | Primary use | Main limit |
|---|---|---|---|---|
| ACS birthplace code lists | `sources/immigration-fiscal/data/external/origin/ACSPUMS2019_2023CodeLists.xlsx` | Local | Official `POBP` decoding | Coding only |
| ACS B05006 metadata and state-origin data | `sources/immigration-fiscal/data/external/origin/census_acs1_2023_B05006_*.json` | Local | Official origin stock validation | Aggregate only |
| World Bank country metadata | `sources/immigration-fiscal/data/external/origin/worldbank_country_metadata.json` | Local | Region and income-group ontology | Not immigration-specific |
| OHSS LPR workbooks | `sources/immigration-fiscal/data/external/origin/ohss/` and sibling OHSS files | Local | Legal permanent resident admissions by country/county/class | Legal channels only |
| OHSS state immigration flat file 2013–2023 | `sources/immigration-fiscal/data/external/origin/ohss/state_immigration_data_2013_2023.csv` | Local, acquired 2026-06-18 | State-year refugee/LPR/naturalization/nonimmigrant panel | Replaces dead ACF ORR CSV |
| Derived origin tables | `sources/immigration-fiscal/data/derived/origin/*.csv` | Local | Joined origin-destination context | Derived from the above, not independent evidence |

## Education and local-capacity overlays

| Dataset / source | Local path | Status | Primary use | Main limit |
|---|---|---|---|---|
| Census school finance 2023 raw | `sources/immigration-fiscal/data/external/census_school_finance_2023.txt` | Local | School-cost context | Needs rollups/joins |
| Census school finance summary | `sources/immigration-fiscal/data/external/census_school_finance_2023_summary.txt` | Local | Faster high-level school-finance use | Summary only |
| School-finance county output | `sources/immigration-fiscal/data/derived/stage2/school_finance_county_2023.csv` | Local | County bridge for local burden | Derived layer, not direct source |
| NCES CCD bundle inventory | `sources/immigration-fiscal/data/derived/stage2/nces_ccd_2024_25_bundle_inventory.csv` | Local | School inventory / acquisition tracking | Inventory, not outcome data |
| SAIPE 2023 district raw files | `sources/immigration-fiscal/data/external/stage4/saipe/` | Local, staged | District child-count and poverty overlays for school-burden sizing | Public district estimates only; not immigrant-status-specific |
| NCES CCD LEA 2023-24 file-tool artifacts | `sources/immigration-fiscal/data/external/stage4/nces/` | Local, staged | Reproducible path to current district directory and companion documentation | Current public district `EL` route still unresolved |
| Court and language-access PDFs | `sources/immigration-fiscal/data/external/stage4/courts/` | Local, staged | Interpreter scheduling, reimbursement, and language-access operating-cost context | Operational documents, not microdata |
| EOIR workload PDFs (curated) | `sources/immigration-fiscal/data/external/stage4/courts/eoir/*.pdf` | Local, acquired 2026-06-18 | Court backlog, UAC, amnesty-by-state screens | PDF tables — parse separately |
| EOIR parsed CSV panels | `sources/immigration-fiscal/data/derived/stage4/eoir/*.csv` | Local, built 2026-06-18 | FY workload (44y), pending FY2016+, amnesty-by-state (56) | Text extraction from chart PDFs |
| Parsed SAIPE district table 2023 | `sources/immigration-fiscal/data/derived/stage4/saipe_school_district_2023.csv` | Local, built | Clean district child-count and child-poverty table keyed by `LEAID` | Still not immigrant-specific |
| School-service district layer 2023 | `sources/immigration-fiscal/data/derived/stage4/school_service_complexity_district_2023.csv` | Local, built | Joined district child intensity, poverty, finance, and current LEA context | No validated current district `EL` counts yet |
| School-service state layer 2023 | `sources/immigration-fiscal/data/derived/stage4/school_service_complexity_state_2023.csv` | Local, built | State rollup of the district school-service layer | Still descriptive, not causal |
| NCES `ELSi` district English-column probe | `sources/immigration-fiscal/data/derived/stage4/nces_elsi_district_english_columns_probe_2026-04-11.json` | Local, built | Audit artifact showing what current public district tabs did or did not expose | Negative probe, not a dataset |

## What is blocked, restricted, or incomplete

| Dataset / source | Status | Why it matters | Blocker |
|---|---|---|---|
| PSID | Not locally acquired in this pass | Long-run earnings and intergenerational dynamics | Browser/registration flow |
| Synthetic SIPP artifact | Landing/docs found, clean artifact not staged | Public-use proxy for admin-linked earnings histories | Acquisition friction / stale links |
| LEHD | Restricted | Strong labor-market trajectory modeling | FSRDC approval |
| SSA Earnings Suspense File microdata | Restricted | Better unauthorized payroll contribution modeling | Restricted data |
| NAS 2017 full report PDF | Not locally archived | Canonical benchmark text | Paywall / purchase |

## Do not use without checking

These categories are high-risk for bad inference:

1. `ACS alone` for lifetime fiscal claims.
2. `CPS population levels` for recent foreign-born stock changes without checking fixed controls.
3. `ITEP` as a full fiscal estimate; it is a tax estimate.
4. `CBO surge reports` as if they were the same object as the settled undocumented stock.
5. Any file previously flagged as an `HTML trap` in `sources/immigration-fiscal/data/MANIFEST.md`.

## First stops by question

If the question is:

1. `What do we have locally?` Start with `sources/immigration-fiscal/data/MANIFEST.md`, then this file.
2. `Can we run a state/origin query now?` Start with the unified **`warehouse/immigration.duckdb`** (one file: all context+lifetime+fiscal tables; `SELECT * FROM _catalog` for the inventory). The per-domain warehouses (`immigration_context.duckdb` etc.) still build as inputs. Rebuild the unified file with `reproduce.sh build unified`.
3. `Can we build our own lifetime model?` Start with `research/immigration-lifetime-fiscal-data-stack-2026-04-10.md`.
4. `What was actually acquired?` Start with `research/immigration-public-data-acquisition-2026-04-11.md` and `research/immigration-frontier-data-acquisition-2026-04-11.md`.
5. `What school-side district layer now exists?` Start with `research/immigration-school-service-complexity-2026-04-11.md`.
6. `What new receiver-node data was acquired?` Start with `research/immigration-receiver-data-acquisition-2026-04-23.md`.
7. `What origin/channel data do we have?` Start with `research/immigration-origin-data-stack.md`.
8. `What datasets test net-negative claims?` Start with `research/immigration-net-negative-dataset-frontier-2026-06-15.md`.

## Stage 5 — net-negative evidence layer (2026-06-15)

| Dataset | Path | Status | Cost-channel use |
|---------|------|--------|------------------|
| CMS Medicaid financial management | `external/stage5_net_negative/cms/medicaid_financial_management.csv` | Acquired | State Medicaid spend by service |
| BEA regional price parities | `external/stage5_net_negative/bea/` | Acquired | Deflate local costs |
| NCES district EL 2017-18 | `external/stage5_net_negative/nces/ccd_lea_141_1718_english_learners.zip` | Acquired | School-cost intensity anchor |
| Receiver-city migrant spend | `external/stage5_net_negative/receiver/receiver_city_migrant_costs.csv` | Copied from causal | Assigned local fiscal shock |
| State stage5 context | `derived/stage5/state_stage5_context_2023.csv` | Built | RPP + Medicaid + EL + SAFMR + SNAP by state |
| SNAP state panel FY2023 | `derived/stage5/snap_state_2023.csv` | Built | Avg households/persons/benefits by state | From NDB public xlsx in USDA zip |
| SIPP scenario ledger 2024 | `derived/stage3_proto/sipp_scenario_ledger_2024.csv` | Built | 98-cell federal+health scenario inputs |
| Origin fiscal scenario 2023 | `derived/stage3_proto/origin_fiscal_scenario_2023.csv` | Built | Per-origin integrated scenario row |
| Manual acquire list | `external/stage5_net_negative/kff_refs/MANUAL_ACQUIRE.md` | Reference | KFF, TRAC, NAS, EDFacts EL |

See `research/immigration-net-negative-dataset-frontier-2026-06-15.md` for full tier list and disconfirmation requirements.

## Crime domain (built 2026-06-24)

First crime data wired into the warehouse (the project is "fiscal AND crime"; this is the first crime layer). Acquisition: `acquire/setup-crime-frontier.sh`. Roadmap for the rest: `research/immigration-dataset-roadmap.md`.

| Table / view | Status | What it answers | Build |
|---|---|---|---|
| `status_class_def` + `status_class_crosswalk` | Built | INT-06 spine: canonical citizenship/legal-status enum + 6-source crosswalk (lossy/verified flagged) — the keystone every crime↔fiscal status join loads | `build_status_crosswalk.py` |
| `crime_scaap_awards` (501 jurisdictions) | Built | DOJ SCAAP FY23 per-jurisdiction criminal-alien inmate-days + reimbursement $ | `parse_scaap_awards.py` (from auto-fetched PDF) |
| `crime_scaap_state_2023` (45 states) | Built | State rollup by `state_fips`; FY23 = 7.8M criminal-alien inmate-days, $210M reimbursed | same |
| `v_crime_scaap_x_state_fiscal` | Built | INT-03 join: criminal-alien incarceration burden × state immigrant-cost context (Medicaid/SNAP/EL) | `build_crime_views.py` |
| `crime_tx_arrests_by_status` (268 rows) + `v_crime_tx_status_ratio` | **Built (INT-01)** | Light/He/Robey TX DPS crime RATE per 100k by {undocumented, legal, naturalized, native-born} × {violent,property,drug,traffic} × {CMS, CMS_nat, Pew} denom, 2012–18. The CMS_nat denom adds the true-native-born split (vs "all citizens"). Headline: undocumented 0.21–0.67× the citizen rate (lowest on property, highest on traffic; violent ≈0.46× in 2018). **The load-bearing crime claim, SHOWN not gated.** | `load_light_tx_crime.py` (data = openICPSR 124923, gated, staged at `crime_frontier/light_texas/`) |
| ICE ERO removals-by-criminality panel | Roadmap (gated) | FY removals by conviction/charge × origin — PDF gives headline only; panel needs the dashboard Excel export (MANUAL_ACQUIRE) | INT-05 |
| `crime_spi_inmates_by_citizenship` | **Built (INT-02)** | BJS Survey of Prison Inmates 2016 (ICPSR 37692 DS0001): weighted 2016 US prison pop 1.42M, noncitizens = **6.9%** (V0950) vs ~7–9% of US adults ⇒ not over-represented. Verified the spine's BJS_SPI mapping. | `load_spi_citizenship.py` (data gated, staged at `crime_frontier/spi/`) |
| `immigrant_assimilation_profile` (204 cells) | **Built (cluster-V), descriptive** | First-generation immigrant↔native employment and conditional log-income profiles by origin region × arrival cohort × census year (1980–2023). **September correction:** synthetic cohorts do not by themselves remove cohort selection, period effects or selective emigration. Earlier gap-closing claims cannot identify individual assimilation; see the [new duration-matched comparison](immigration-cohort-clarity-2026-09-05.md). | `build_immigrant_assimilation_profile.py` (IPUMS-USA microdata → aggregate; skips if SSD absent) |

All flow into the unified `immigration.duckdb` (aggregate; license-clean — IPUMS microdata stays local, only cell means ship).

## Acquisition frontier (2026-06-15)

Re-staged after lost SSD. **`infra/immigration-fiscal/acquire/setup.sh`** (canonical; `sources/.../setup.sh` is a wrapper) pulls:

| Tier | Dataset | Path / notes | Status |
|---|---|---|---|
| A | MEPS HC-251 (full PUF + zips) | `external/stage3/ahrq/meps/` | In `setup.sh`; large zips (~50MB+ each) |
| A | Census school finance `elsec23` | `external/census_school_finance_2023*.txt` | Fixed URL (old zip path 404) |
| A | IRS SOI migration panel 2011–22 | `/Volumes/2TBPNY/corpus/irs_soi/migration/` | County + state inflow/outflow |
| A | PUMA↔cousub crosswalk (input) | `external/stage2/census/geo/tab20_puma520_cousub20_natl.txt` | County-bridge input |
| A | PUMA↔county area crosswalk (derived) | `derived/stage2/puma_county_area_xwalk_2023.csv` | 4,701 rows (cousub→county aggregate; memo had 14,856 cousub-level) |
| A | Stage2 warehouse tables | `warehouse/immigration_context.duckdb` | 16 tables, 4.3 MB — school/housing/IRS/county joins live |
| A | HUD CHAS county zip (Table 11) | `external/stage2/hud/chas/2018thru2022-050-csv.zip` | Playwright + `portal/datasets/cp/`; ACS proxy fallback in build |
| A | NCES CCD school universe | `external/stage2/nces/ccd_sch_*.zip` | Substitute for dead `ccd_2024_25_universe` URL |
| B | BLS LAUS county monthly | `external/stage2/bls/laus/` | Threshold / labor panel seed |
| B | CBP SBO encounters CSV | `immigration-causal/data/cbp/raw/` | Replaces retired xlsx tables |
| B | FRED macro CSV exports | `external/fred/` | UNRATE, CPI, HOUST, Case-Shiller |
| C | ORR arrivals by state | `external/origin/orr/` | ACF WAF — may need browser |
| A | EOIR workload PDFs | `external/stage4/courts/eoir/` | Scripted from justice.gov stats page |
| C | NYC Local Law 6 PDF | `external/stage4/courts/` | 403 without session |
| Blocked | PSID | — | Cloudflare / registration |
| Blocked | LEHD worker histories | — | FSRDC |
| Blocked | Synthetic SIPP artifact | landing HTML only | No direct zip |
| Next | QWI county/metro panel | extend causal `pull_qwi_state_panel.py` | API pull, not bulk mirror |
| Acquired / analyzed | ACS 2024 PUMS | `/Volumes/2TBPNY/corpus/census_acs_2024_1yr/` | Person ZIP 602,847,146 bytes; full national recent-entry analysis 2026-09-05 |
| Next | BPS + HUD HIC/PIT | causal `data/threshold/` | Already acquired |
| Next | NCES district English-learner counts | — | Not in current CCD file-tool |
| Next | Receiver-city admin costs | causal `bused_cities/` | Fragmented city FOIA |
| Next | SSA actuarial unauthorized estimates | — | Report PDFs, not microdata |
| Next | IPUMS CPS historical (parental birthplace) | — | Registration-gated historical extract; CPS parental birthplace can support second-generation comparisons. **September correction:** corpus `census_cps` contains `jan24pub.csv` (121,914,518 bytes); a historical parental-birthplace panel has not been verified. |

## Best next steps

1. Build a small `SIPP` ingest around the dictionary instead of bulk-loading the whole file.
2. Integrate `sipp_meps_expected_health_cost_cells_2024.csv` and wire the bridge into the public MVP scenario engine.
3. Lock down access to the individual `IRS SOI PUF`.
4. Get `PSID` for descendant dynamics.

### ACS2019_PUMS_NATIONAL_PERSON — recent-entry baseline

**Source:** US Census Bureau. **Acquired:**2026-09-05. **License:** public-use government microdata; disclosure protections and survey limitations apply.
**Local:** `/Volumes/2TBPNY/corpus/census_acs_2019_1yr/csv_pus.zip`.
**Official:** [2019 one-year PUMS directory](https://www2.census.gov/programs-surveys/acs/data/pums/2019/1-Year/); [person ZIP](https://www2.census.gov/programs-surveys/acs/data/pums/2019/1-Year/csv_pus.zip).
**Codebook/accuracy:** [2019 documentation](https://www.census.gov/programs-surveys/acs/microdata/documentation.2019.html), [accuracy PDF](https://www2.census.gov/programs-surveys/acs/tech_docs/pums/accuracy/2019AccuracyPUMS.pdf).
**Size/hash:**567,851,237 bytes; SHA256 `18e4ece4cc24781c01e8046c2d5afbabeb1f15452ddec43f60fdf3b1f6e67b92`. Both national CSV members read completely;3,239,553 rows and weighted328,239,523 people reproduce official PUMS checks. The ZIP also includes the official README.

**Key variables:** `NATIVITY`, `POBP`, `YOEP`, `AGEP`, `SEX`, `RELSHIPP`, `ESR`, `SCHL`, `PERNP`, `PINCP`, `ENG`, `ADJINC`, `PWGTP1–80`. Recent `YOEP` values are individual years; most recent entry is not necessarily first immigration. Income is rolling prior12months, including zeros/losses; `ADJINC` alone does not put different survey years into common dollars. All80 replicate weights, including negative and zero values, are retained.

**Used in:** [2019/2024 cohort comparison](immigration-cohort-clarity-2026-09-05.md); `infra/immigration-fiscal/build/analyze_arrival_cohorts.py`, `standardize_arrival_profiles.py`, `summarize_arrival_cohorts.py`. Generated evidence and input hashes: `.scratch/cohort-clarity-20260905/analysis/` and `standardization/`.

### ACS2024_PUMS_VERIFIED_LOCATION — current resident-cohort source

**Source:** US Census Bureau. **Existing acquisition relocated and reverified:**2026-09-05; no duplicate download.
**Local:** `/Volumes/2TBPNY/corpus/census_acs_2024_1yr/`: person ZIP602,847,146 bytes; household ZIP251,500,587; official dictionary395,086. [Official files](https://www2.census.gov/programs-surveys/acs/data/pums/2024/1-Year/), [dictionary](https://www2.census.gov/programs-surveys/acs/tech_docs/pums/data_dict/PUMS_Data_Dictionary_2024.pdf).

The person ZIP was fully analyzed:3,422,888 rows, weighted340,110,990 people. Full and SDR-SE calibration checks also reproduce male and age25–34 populations. Person source SHA256 and exact raw member information are in `analysis/manifest_2024.json` and `standardization/results.json`. Actual geography header is `STATE`; `POBP448` is Somalia. The old `sources/immigration-causal/...` pointer is unavailable. This is2024-only, not the2020–2024 pooled file or an admission ledger. Same variables/limits and generators as the preceding card. Household bytes were inventoried, not used in the new person analysis. [DATA]

### ACS_PRICE_AND_CALIBRATION_2019_2024 — verified comparison inputs

**Source/access:** [Census ACS comparison guidance](https://www.census.gov/programs-surveys/acs/guidance/comparing-acs-data/2024.html), retrieved2026-09-05; public statistical documentation. **Local:** `.scratch/cohort-clarity-20260905/availability/inflation.json` and `inflation-source-*`.

R-CPI-U-RS annual indices2019=375.8,2023=449.3,2024=462.5;2019→2024 factor462.5/375.8,2023→2024 factor462.5/449.3. The manifest pins the Census-guidance vintage; the later corrected BLS workbook was not retrieved. Four official CSVs provide2019/2024 person counts and PUMS full/SE calibration anchors. Source URLs, byte counts and hashes are in the JSON. These are documentation/calibration data, not an additional household survey. Used by both comparison generators; processed-income values receive the cross-year factor only once.

### RPC_REFUGEE_FY2022_FY2023_FY2025 — staged admission reports

**Source:** State Department Refugee Processing Center. **Acquired:**2026-09-05; public reports. **Official:** [RPC archive](https://www.rpc.state.gov/archives/). **Local:** `.scratch/cohort-clarity-20260905/availability/rpc_fy{2022,2023,2025}.pdf`; exact URLs/hashes in `manifest.json` and the [availability memo](immigration-recent-cohort-data-availability-2026-09-05.md).

**Size:**three files,3,236,929 bytes. **Keys:** destination state × principal applicant nationality × admission month. These are refugee-channel arrivals, not all foreign-born residents, ancestry, religion or a deduplicated union with court/border/LPR records. FY2025 monthly total38,102 reconciles; Somali national totals remain **unvalidated** because text extraction fragments rows. FY2024 download was deferred by the bounded lane's size cap; the current page's latest inspected cutoff wasJuly31,2026. No unvalidated origin totals enter the new analysis.

### COHORT_X_NARRATIVES_20260905 — selective official API evidence

**Source:** official X API; existing `x-api` skill. **Acquired:**2026-09-05. **Local:** `.scratch/cohort-clarity-20260905/x/`; four returned archives plus query specification, source-check results, cost record and hash manifest. Exact90-day query window:June7 10:50:43UTC–September5 10:50:43UTC.111 distinct returned posts,103 new beyond the earlier207-post sample; total310 unique across both. Local tally$0.555, vendor invoice unverified. Platform terms apply; collection remains local.

This is purposive claim discovery, not representative opinion or independent confirmations for duplicated wording. [Narrative audit](immigration-cohort-narratives-2026-09-05.md) grades five specific claims and records unresolved primary-source gaps. No X webpage scraping, messages or publication occurred.

## Revisions

- **2026-09-05:** Registered the new2019 baseline, actual2024 path, price/calibration inputs, bounded RPC reports and targeted X sample. Corrected the empty-CPS-mirror statement and qualified the older synthetic-cohort identification claim under the [cohort decision](../decisions/2026-09-05-arrival-cohort-comparison.md). SIPP2025 is officially available for reference2024 but has not yet been acquired or incorporated.
