# Immigration — Dataset Register

This is the working register for the immigration project. It is not the byte-level storage manifest. For raw-file inventory and trap-file warnings, see `sources/immigration-fiscal/data/MANIFEST.md`. For datasets we **don't have yet** (acquisition targets, crime + benefit-side gaps), see `research/immigration-dataset-roadmap.md`.

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
| Immigration context DuckDB | `warehouse/immigration_context.duckdb` (internal) + symlink at `sources/immigration-fiscal/data/derived/` | Local, rebuilt 2026-06-15 (stage1+2) | Main query surface for state/origin/county context joins | Not a lifetime causal model by itself |
| Lifetime evidence DuckDB | `warehouse/immigration_lifetime_evidence.duckdb` | Local, rebuilt 2026-06-15 | 113-source catalog, 138 claims, 63 generators, 24 structured tables (Saiz/ITEP/stage2/5/MEPS) | No row-level join to papers; bridge via `education_bucket`, `state_fips`, `topic` |
| Fiscal union DuckDB | `warehouse/immigration_fiscal_union.duckdb` | Local, rebuilt 2026-06-15 | ATTACH shell + cross-domain views (`v_education_stock_with_npv`, etc.) | Views only; rebuild after either parent DB changes |
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
| ACS 2024 1-Year PUMS person/household | `sources/immigration-causal/data/external/census_acs_2024_1yr/` | Local, staged | Post-surge receiver exposure: nativity, recent movers, housing stress, children, education, PUMA geography | No undocumented status; PUMA geography needs crosswalk/approximation |
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
| NAS 2017 catalog page | `sources/immigration-fiscal/data/nap/nas_2017_immigration_economic_fiscal.html` | Local HTML only | Canonical benchmark reference | Full report not locally archived as PDF |

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
| Local burden examples | `research/immigration-state-local-cost-examples-ny-ca-tx.md` | Memo, not raw data | Concrete burden illustrations | Not a reusable database |

## Program and household-transition data

| Dataset / source | Local path | Status | Primary use | Main limit |
|---|---|---|---|---|
| SIPP 2024 public-use | `sources/immigration-fiscal/data/external/stage3/census/sipp/pu2024_csv.zip` | Local | Monthly program participation and household transitions | Short panel, weak status identification |
| SIPP documentation | `sources/immigration-fiscal/data/external/stage3/census/sipp/` | Local | Field and methodology reference | Documentation only |
| SIPP 2023 public-use | `sources/immigration-fiscal/data/external/stage2/census/sipp/pu2023_csv.zip` | Local | Earlier staging/calibration | Same |
| SIPP calibration extract | `sources/immigration-fiscal/data/derived/stage2/sipp_foreign_low_skill_calibration_2023.csv` | Local | Calibration input for stage 2 | Derived, not source-of-record |
| MEPS HC-251 | `sources/immigration-fiscal/data/external/stage3/ahrq/meps/` | Local | Medical spending and payer incidence | Not immigrant-status rich by itself |
| MEPS health-cost module 2023 metadata | `sources/immigration-fiscal/data/derived/stage3_proto/meps_health_cost_module_2023.meta.json` | Local, built | Value labels, row counts, and build notes for the MEPS module | Metadata only, not the module table itself |
| SIPP 2024 public MVP cells | `sources/immigration-fiscal/data/derived/stage3_proto/sipp_public_mvp_cells_2024.csv` | Local, built | Working-age nativity/citizenship/education transition cells for SIPP scenario scaffolding | Public file has no clean legal-status panel |
| SIPP→MEPS bridge cells 2024 | `sources/immigration-fiscal/data/derived/stage3_proto/sipp_meps_bridge_cells_2024.csv` | Local, built | Join layer mapping SIPP cells to MEPS age/nativity/insurance health-cost cells | No undocumented-specific inference introduced |
| SIPP→MEPS expected health-cost cells 2024 | `sources/immigration-fiscal/data/derived/stage3_proto/sipp_meps_expected_health_cost_cells_2024.csv` | Local, built | Collapsed per-SIPP-cell expected payer-spend profile used by public MVP | Not itself a final lifetime estimate |
| IRS SOI mirror | `/Volumes/2TBPNY/corpus/irs_soi` | Local SSD mirror | Federal tax microsim backbone | External path, confidentiality edits; re-stage if missing |

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
| `immigrant_assimilation_profile` (204 cells) | **Built (cluster-V)** | First-generation immigrant↔native gap (employment, log-income) by origin region × arrival-cohort × census year (1980–2023), **synthetic cohorts** (Borjas cohort-quality confound removed). Mexican income gap halves (−0.70→−0.24 log pts) over ~30 yrs in-US; employment gap closes by 15–25 yrs. The buildable FIRST-GEN decay measure for V04/V08; the true 2nd-gen needs CPS (below). | `build_immigrant_assimilation_profile.py` (IPUMS-USA microdata → aggregate; skips if SSD absent) |

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
| Next | ACS 2024 PUMS | causal `external/census_acs_2024_1yr/` | Already on PNY (~575MB) |
| Next | BPS + HUD HIC/PIT | causal `data/threshold/` | Already acquired |
| Next | NCES district English-learner counts | — | Not in current CCD file-tool |
| Next | Receiver-city admin costs | causal `bused_cities/` | Fragmented city FOIA |
| Next | SSA actuarial unauthorized estimates | — | Report PDFs, not microdata |
| Next | IPUMS CPS historical (parental birthplace) | — | Registration-gated. **Needed for cluster-V V02:** the true cross-generational 2nd-gen-by-origin test — IPUMS-USA lacks parental birthplace (dropped post-1970), CPS has FBPL/MBPL. corpus `census_cps` empty |

## Best next steps

1. Build a small `SIPP` ingest around the dictionary instead of bulk-loading the whole file.
2. Integrate `sipp_meps_expected_health_cost_cells_2024.csv` and wire the bridge into the public MVP scenario engine.
3. Lock down access to the individual `IRS SOI PUF`.
4. Get `PSID` for descendant dynamics.
