**Verdict:** The complete public-land correction is **not identified**. Applying the requested residential-price method to the mapped and inventoried subset gives an annual group charge of **$32.93–39.61bn under arm B**, **$50.61–60.88bn under A**, and **$4.04–5.35bn under C**, at the case's 2.0810698764% rate. These are conditional scenarios, beside the adopted case. Incomplete facility acreage, uncertain title, overlapping rights, and unmeasured developability prevent interpreting them as the national estate's value or a lower bound. [CALCULATION: `derived/summary.json`, `derived/land_by_line.csv`; DATA: `derived/coverage.csv`, `derived/footprint_sources.json`]

Under B the valued land is $15.563tn nationally. Its group charge is 8.95% of the low $368.030bn case endpoint and 9.07% of the high $436.562bn endpoint. Roads and parks account for almost all of the increment. This is an imputed resource charge, with no land depreciation; it is not a debt flow, current payment, or measured sale receipt. [CALCULATION: `derived/summary.json` `totals`; FRAMING-SENSITIVE]

## 1. What the numbers mean

The group is the case's whole Mexican-immigrant lineage, including added nonreporting descendants and Census coverage corrections. Each capital line retains its own case key and response. [SOURCE: adopted case payload and `derived/case_contract.json`]

The frame is the adopted case's income-year-2024 account for all other residents, with its two service-response endpoints and no white reference group. Values are in 2024 dollars. Roads measure 2024 mileage; the reused school universe is 2023–24, IPEDS is 2023, and facility, park and airport inventories have later source dates (FAA 2026/10/01, Overture 2026-10-21.0). This is a valuation of those inventories at 2024 prices, not an observed balance sheet of land held on a single 2024 date. [DATA: acquisition manifests and `derived/universe_records.csv`; SOURCE: adopted `main_case_2026_10_16/package.cjs`]

| Price construction | Valued national land, $bn | Annual group charge at case rate, $bn | Share of respective case endpoints | At uniform 2.42%, $bn | At 7%, $bn |
|---|---:|---:|---:|---:|---:|
| A, all acres at residential price | 23,921.12 | 50.61–60.88 | 13.75% / 13.94% | 58.85–70.79 | 170.24–204.77 |
| B, developable-share rule | 15,562.65 | 32.93–39.61 | 8.95% / 9.07% | 38.30–46.06 | 110.77–133.22 |
| C, vacant-land plattage reference | 2,227.71 | 4.04–5.35 | 1.10% / 1.23% | 4.70–6.22 | 13.59–18.00 |

[CALCULATION: `derived/summary.json` `totals`; shares pair low with the low case denominator and high with the high denominator. The A/B/C differences are construction sensitivities, not statistical intervals.]

A is the brief's residential ceiling reference, not a ceiling on every feasible alternative use; C is its lower reference, not a bound on legally restricted assets. B imports the school's 65% developable share for sites over two acres and 80% below two acres. No evidence here establishes those shares for highways or large state parks. The full-estate total is explicitly `null` in the machine output. Missing or excluded acreage was not inflated by inverse match rates. [SOURCE: school-land price functions and their Gyourko–Krimmel / Albouy–Ehrlich–Shin evidence; INFERENCE]

The uniform 2.42% column is exactly the requested land-rate sensitivity. The paired-theta source model has different federal and state/local rates and an item-6 corporate-receipt leg. This lane does not add that separate repricing of the existing case to its land charge. [SOURCE: `public_capital_rate_2026_10_24/derived/rate_model.json`; CALCULATION: `derived/summary.json` `paired_rate_note`]

## 2. Every physical capital line

B results below charge land once per physical line. Signed user-fee capital adjustments share the parent line's parcel, rather than receiving additional land. Exact charged stocks, engine keys and responses, full effective coefficients and all A/B/C line results are in `case_physical_lines.csv`, `case_contract.json` and `land_by_line.csv`. [CALCULATION]

| Case line | Valued B land, $bn | B land / case structures | Annual group charge, low / high, $bn | Coverage interpretation |
|---|---:|---:|---:|---|
| `k12` | 626.891 | 0.2353 | 2.8763 / 2.8763 | Reused school estimate, including its validated imputation |
| `college` | 137.373 | 0.1146 | 0.3504 / 0.3504 | Mapped public-college sites; libraries/preschool residual not covered nationally |
| `pos_sl` | 0.0925 | 0.000319 | 0.000283 / 0.000283 | Few public-use safety polygons; national total unknown |
| `pos_fed` | — | — | — | No identified in-scope priced sites |
| `health_sl` | 11.555 | 0.0316 | 0.0368 / 0.0368 | Public-hospital site subset |
| `health_fed` | 5.820 | 0.0549 | 0.0077 / 0.0077 | Identified nondefense federal hospital subset |
| `gps_sl` | 0.00753 | 0.0000058 | 0.000012 / 0.000018 | Four mapped public-use office sites; highly incomplete |
| `gps_fed` | — | — | — | No identified priced sites |
| `hwy_sl` | 8,559.739 | 1.9503 | 14.3506 / 19.3875 | Measured mileage × modeled ROW widths × county prices |
| `hwy_fed` | 416.115 | 7.6249 | 0 / 0.9425 | Nondefense owner codes; response zero at low end |
| `rec_sl` | 5,195.305 | 12.2219 | 13.6297 / 14.3246 | Selected public-fee park designations; residential-price scenario |
| `air_fed` | — | — | — | FAA civil-airport acres do not identify federal air-traffic-control sites |
| `rec_fed` | — | — | — | Broad federal natural estates excluded; capital-bearing site land unresolved |
| `ent_housing_sl` | 1.368 | 0.00326 | 0.00251 / 0.00251 | Public-use residential polygons; almost no HUD parcel coverage |
| `ent_transit_sl` | 0.00987 | 0.0000195 | 0.000027 / 0.000027 | Mapped site subset; rights-of-way unresolved |
| `ent_airports_sl` | 549.592 | 0.9224 | 1.5153 / 1.5153 | FAA reported public-airport acreage, priced at reference points |
| `ent_ports_sl` | 0.2957 | 0.00313 | 0.000815 / 0.000815 | Four mapped public-use polygons |
| `ent_power_sl` | 0.0376 | 0.0000694 | 0.000104 / 0.000104 | Ten public-tagged polygons; corridors and most sites unresolved |
| `ent_power_fed` | — | — | — | No identified priced sites |
| `ent_water_sl` | 0.01175 | 0.0000128 | 0.000032 / 0.000032 | Fifteen public-tagged footprints; networks unresolved |
| `ent_sewer_sl` | 0.01455 | 0.0000119 | 0.000040 / 0.000040 | Nine accepted footprints, one unpriced; networks unresolved |
| `ent_tolls_sl` | 58.422 | 0.1166 | 0.1611 / 0.1611 | Toll-associated road strips; managed-lane split unresolved |
| `ent_other_sl` | 0 by case convention | n/a | 0 increment | Residual has no net structures in the case's decomposition |
| `ent_other_fed` | 0 by case convention | n/a | 0 increment | Same convention; not evidence that postal/other enterprise land is absent |

[CALCULATION: `derived/land_by_line.csv`; physical denominators in `derived/case_physical_lines.csv`. Dashes mean unknown, not measured zero. Machine tables report finite **mapped** ratios, including zero when nothing is mapped; their `national_total_status` explicitly preserves nonidentification. The two residual rows use ratio zero by convention and state that convention. K-12's structures denominator is $2,663.947bn; its charged stock including equipment/software is $2,723.919bn.]

**Allocation is the case's, including later corrections.** The contract reads all 28 signed components at both endpoints and both methods. It retains union-completion capital, own coverage, selected count items, college response and item 21's health-capital terms. Their reconstructed capital return closes to the independent full-evaluator capital-only 7% arm: $40.671102/$44.617347bn for hotdeck and $40.685970/$44.629351bn for pooled. The effective coefficient includes each response; no response is multiplied twice. The rounded rate-lane line split is a discovery aid, not the principal allocation source. [CALCULATION: `derived/case_contract.json`, 458 gates]

**School benchmark versus case allocation.** The reused school inputs reproduce **$2.605156bn** under B with that lane's pupil share 0.174806 and where-enrolled factor 1.142348. The case's full net K-12 coefficient is approximately 0.193 after fees/completion/coverage/count changes. Applying that coefficient to the same land and measured location factor gives **$2.876299bn**. The difference is a key change, not newly discovered acreage. No where-used price factor is invented for any other line. [CALCULATION: `derived/summary.json` `school_input_reproduction`; `land_by_line.csv`; DATA: school lane summary]

## 3. What is measured, and what is transferred

**Roads.** FHWA mainline spatial-table aggregates and the separate county summary partition the mileage frame: classes 1–5 and urban minor collectors from mainline; rural minor collectors and all local roads from county summary. All **714 state × urban/rural × functional-class cells** reproduce the primary HM-20 workbook, totaling **4,208,454.2294 miles** before owner/scope exclusions. No county allocation or national mileage calibration was used. ROW acreage is miles × design feet × 5,280 / 43,560, not a measured cadastral inventory. The in-scope central scenario has **43,998,956 acres**. [DATA: `derived/roads_mileage_closure.csv`, `roads_summary.json`; SOURCE: FHWA 2024 HM-20 and HPMS]

FHWA/ITE's reproduced AASHTO urban-local/collector ROW tables anchor those classes. Other width ranges come from NCDOT's primary ROW chapter; this is an explicit departure from the preferred national guidance because that guidance does not supply nationally representative existing widths. The ranges are design templates, not confidence bounds. Missing rural arterial lane counts take the two-lane template. Whole-strip toll assignment can overstate land attributable to tolled lanes. [SOURCE: primary PDFs and parsers in `roads.py`; DATA: `roads_county_acres.csv`]

BEA's principal stock is federal **nondefense**. Explicit military road owners 72/73/74 are excluded; Army Corps 70 remains because it includes civil works. Tribal owner 50 is included in the local account: BEA's 2005 NIPA article explicitly classifies tribal government as local. Alternatives preserve add-military/remove-tribal amounts. The correction excludes 5,769.1444 military miles and includes 17,289.1497 tribal miles; neither changes the full mileage reconciliation. [SOURCE: parsed BEA FAAt701-A row 49 and BEA SCB October 2005, printed p.8; DATA: `roads_scope_alternatives.csv`, `roads_summary.json`]

**Parks.** PAD-US 4.1 Fee Managers supplies **144,003 polygon/source records**, not that many distinct named parks: fee ownership STAT/LOC/DIST/TRIB and recreation designations SP/SREC/LP/LREC/REC. Their repaired source area is 17.680m acres, versus 17.516m source-reported acres. Exact intersections with 2010 tracts retain 17.462m raw acres; subtracting overlapping source polygons leaves **16.654m**. There are 1,975 identical geometries and 808,519 overlapping acres removed. The 143,741 intersecting records cover 99.82% of the selected records and 98.77% of raw source geometry area. Unmatched area is not renormalized. [DATA: `footprint_sources.json`]

Source precision leaves 5,710 invalid polygons; explicit structure repair resolves all except one, which requires a recorded zero-buffer fallback. Bayshore Boulevard Greenway changes from 7.9433 raw to 7.9358 repaired acres (reported 8). One API page uses maximum generalization 0.00005° after a transport-size failure; per-page scientific query parameters and hashes are retained. B/C discounts use original whole-site acreage even when tract boundaries split it. These geometry checks do not establish saleability or residential developability. [DATA: `footprint_sources.json`; `footprint_acquired_sources.json`]

**Other facilities.** Authoritative active public-institution lists are matched inside the smallest corresponding Overture campus polygon. Explicit private ownership vetoes a point proxy; mixed public/private institutions without public-title evidence remain held. Source-verified federal colleges, Defense hospitals and unresolved federal hospital scope veto mapped sites, including publicly tagged ones. Same-line overlapping accepted polygons are dissolved; 3,065 accepted source polygons become 3,027 sites. Only 2,845 receive an in-US tract/county price; US bounding boxes also contain cross-border map features, which remain unpriced without US geography. [CALCULATION: `facility_matches.csv`, summary `facility_overlap`; DATA: institution and footprint inventories]

## 4. Coverage

| Class | Authoritative/mapped frame | Observed matching or area coverage |
|---|---|---|
| K-12 | 98,065 nonvirtual schools | 72,088 matched, 73.51% of schools / 81.3% of pupils; source lane imputes unmatched sites |
| Public colleges | 1,945 active candidates after ten explicit federal/non-S&L exclusions | 1,563 inside accepted campuses, 80.36%; no unmatched-acre expansion |
| Public hospitals | 1,329 open eligible public records | 1,027 inside accepted campuses, 77.28%; 108 public Defense hospitals excluded and 38 unresolved public federal records held before OPEN filtering |
| HUD housing | 5,889 development records | Only six eligible point matches, 0.10%; coarse and scattered points cannot delineate parcels |
| FAA airports | 4,017 open publicly owned civil airports | 3,787 report positive acreage, 94.27%; nine of those reference points remain unpriced |
| Selected PAD fee recreation records | 144,003 polygon records | 143,741 intersect tracts; within-source overlaps removed |
| Highways | 714 official mileage cells | Full mileage reconciliation; width distribution unmeasured |
| Offices/safety/utilities/ports/transit | Volunteer map with explicit ownership/operation tags | No complete national parcel denominator; tiny known subsets cannot identify national acreage |

[DATA: `derived/coverage.csv`, `universe_coverage.json`, `universe_airport_checks.json`, school summary. Overture class inventories in `footprint_coverage.csv` cover the queried US boxes; they are not national institutional universes.]

IPEDS institutional control is not a deed register. HIFLD hospital scope uses source agency, preserving VA while excluding TRICARE/Defense; its `MILITARY` type alone does not distinguish them. CMS's 5,354-hospital/1,144-government crosscheck has a different Medicare frame and no coordinates, so it is not used as an acreage multiplier. HUD represents a development at an address/largest building, including scattered sites. FAA verifies public **ownership**, not merely public use, and directly reports acreage; 230 missing acreages, including 139 in Alaska, remain missing. It does not delineate airport fee/easement parcels or separate every civilian federal owner. [SOURCE: primary dictionaries/agency metadata; DATA: `universe_*` outputs]

Pricing falls from tract to FHFA county, then state exactly as in the school method. `price_coverage.csv` reports acres and record counts at each level. Some zero-exclusive-area park pieces count as unpriced records; they do not represent lost acreage. Across all classes the positive unpriced area is 12,727.8 acres, but missing or non-geolocated sites and absent corridors are not limited to that number. [DATA: `price_coverage.csv`, summary `unpriced_acres`; INFERENCE]

## 5. Concentration and disconfirmation

The ten highest-valued counties hold **30.46% of B's summed national value**. Cross-class overlap remains unresolved, so this is concentration of the scenario's summed line values. [CALCULATION: `county_concentration.csv`]

| County/FIPS | B value, $bn |
|---|---:|
| Los Angeles, 06037 | 1,027.99 |
| Santa Clara, 06085 | 755.06 |
| Manhattan/New York, 36061 | 703.73 |
| Orange, 06059 | 547.51 |
| San Diego, 06073 | 530.65 |
| San Mateo, 06081 | 310.93 |
| Alameda, 06001 | 241.80 |
| Alaska county-equivalent 02070 | 237.99 |
| Kings, 36047 | 199.09 |
| San Francisco, 06075 | 186.09 |

[DATA: FHFA county names/FIPS; CALCULATION: `county_concentration.csv`.]

| B variation, other assumptions held | Total group charge, low / high, $bn |
|---|---:|
| Central mapped/design construction | 32.93 / 39.61 |
| Remove Manhattan, San Francisco and DC assets | 31.04 / 37.34 |
| Drop every state-price fallback asset | 29.54 / 35.21 |
| Drop road owners 11/12/40, which can overlap park/instrumentality estates | 32.86 / 39.51 |

[CALCULATION: summary `variants`; exclusions remove contributions rather than reweighting the remaining population. They are subset sensitivities, not lower confidence limits.]

The strongest disconfirmation is the price transfer itself. For example, the FHFA state fallback prices Harney OR's modeled federal ROW at approximately $940,000 per acre and Inyo CA's at $3.41m per acre. Those are residential-market proxies, not observed values for rural public corridors. Alaska 02070 also enters the top ten without an observed county cross-section price. Arithmetic and mileage reconciliation do not validate these counterfactual prices. Dropping state fallbacks removes $3.39–4.40bn of the B group charge, but county residential prices still need not describe remote strips or parkland. [DATA: FHFA parsed tables, `price_coverage.csv`; CALCULATION: road source probe and summary `variants`; INFERENCE]

| Road block only | Group charge, low / high, $bn |
|---|---:|
| B, central design widths | 14.51 / 20.49 |
| B, lower design widths | 11.58 / 16.31 |
| B, upper design widths | 16.73 / 23.71 |
| C, one-mile representative strip | 3.07 / 4.36 |
| C, 0.1-mile representative strip | 11.95 / 16.96 |
| C, ten-mile representative strip | 0.74 / 1.05 |

[CALCULATION: summary `road_scenarios_group_charge_bn` and `land_by_line.csv`. The C size dependence is structural: HPMS row lengths are dynamic segmentation, not cadastral parcels. No road geometry was used to manufacture a parcel definition.]

## 6. Consequential remaining limits

- **The national total is absent, not zero.** Federal offices/safety/air-control/park sites, most publicly owned utility land and corridors, transit yards, public housing and college residual functions are not covered nationally. Incomplete tags are selected observations; multiplying by inverse match rates would assume an unmeasured acreage distribution.
- **Sale and service counterfactuals are unobserved.** Parks, reservoirs, steep land, conservation restrictions and road easements cannot automatically be developed or sold. B's subdivision rule does not remove all of these constraints. Releasing land can require demolition, relocation and new infrastructure. These costs are unpriced. Conversely, denser permitted redevelopment can exceed the residential single-family reference. [FRAMING-SENSITIVE]
- **Rights overlap.** Same-line map overlaps and PAD duplicates are removed, but roads may cross parks and school/airport estates; underground utilities and transit may share corridors. No polygon road overlay was invented. The summed scenario is not a strict lower bound because missing sites and repeated rights can move it in opposite directions.
- **Use is not title.** A public institution or government operator may lease its site. Current rents may already be in operating expenditures, creating double counting if imputed land charges are added without a title/rent reconciliation. Public residential polygons do not provide a HUD asset-type/deed crosswalk. The school lane's charter caveat travels with its reuse.
- **Valuation support is narrow.** FHFA prices single-family residential land. County/state fallbacks, the 2022→2024 house-price carry-forward, large-park extrapolation and C's strip segmentation are model assumptions. These uncertainties dominate many geometric repairs.
- **Spatial allocation is unmeasured outside schools.** Each other line uses its own national case key, with its full fiscal response/corrections. No claim is made that the group's road/park/airport use follows national land value. The school location factor itself is a pupil proxy transported to the case's broader lineage.

These limitations prevent adopting a complete, consistent land item from this lane alone. The delivered tables identify the measured mileage/ownership/acreage inputs, show what the requested valuation rule produces, and leave the unresolved estate total null. [INFERENCE]

## 7. Reproduction, review and files

This is an LLM-assisted construction; the instrument's known dispositions are documented in [the project bias caveat](../../../notes/llm-bias-caveat.md). Extraction and accounting checks do not verify the assumed alternative land use or removal response.

Run commands and primary URLs: [README.md](README.md). `build.py` invokes all acquisitions, normalization, case extraction and the scientific test suite in isolated Python. The 14 tests pass. The exact single-command byte-identical rerun is recorded at closeout below. The existing case, school lane, INDEX and FAQ are untouched; no Git metadata was written. [CALCULATION: `_cache/build.log`]

The bounded independent source review found the empty/unlocated-price edge case and a tribal-scope test inconsistency; both were corrected with regressions. The separate case trace checked component routing, and its 7% derivative gate passes. A later read-only diff review found no remaining material source defect; final output certification rests on the executed checks here, not model agreement. [DATA: test suite and review receipts]

## Work log

- 2026-10-24 01:46:19 JST: Read the assigned brief; started source and case-contract inspection. Git metadata is read-only; no staging or commits will be performed.
- 2026-10-24 01:50:56 JST: Reconstructed all 28 capital components at the case's endpoints, including fee offsets, completion, own coverage, count changes, college response and health residual. 458 gates pass; the full capital response closes to the independently evaluated 7% arm. Physical land will be charged once per parent component.
- 2026-10-24 01:56:49 JST: FHWA county mileage closes to all 714 HM-20 cells. FAA supplies directly reported publicly owned airport acreage (3,787 of 4,017 open civil airports). PAD-US public-fee recreation extraction and Overture ownership/footprint matching remain in progress. No national unknown-ownership or unmatched-area multiplier is authorized by the observed data.
- 2026-10-24 02:09:39 JST: The initial class-equality/spatial join selected a roughly 196m-comparison hash join. Partitioning by class selected DuckDB spatial joins and reproduced the identical match CSV hash in 3.89 seconds, versus 74.86 seconds for the first probe. Same-line overlap queries use the same partitioning.
- 2026-10-24 02:13:12 JST: First full priced outputs complete. PAD source records are fee polygons, not unique parks; overlap/repair/generalization diagnostics retained. The full-estate total remains not identified.
- 2026-10-24 02:16:11 JST: Current full build exited 0, including 14 tests. Python measured 35.954 seconds and 2,830,516,224 peak resident bytes for the process; child peak 761,249,792 bytes, not added to process peak. Cache remains below 1GB. Required byte-identical rerun pending final check.
- 2026-10-24 02:20:26 JST: Required command completed with exit 0: `uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/public_land_2026_10_24 "uv run --no-project python3 {lane}/build.py"` — **IDENTICAL: 35/35 files unchanged**. The build executed all 14 tests. No scripts exempted, no Git metadata written.
