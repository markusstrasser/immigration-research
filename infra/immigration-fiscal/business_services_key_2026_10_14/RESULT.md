**Verdict:** Retain v7's central (339.552–423.649bn/year); no measured national business-serving spending/stock share was identified that justifies a central change. The narrow incident-proxy arm lowers the identified union by 1.032bn and the lineage by 1.124bn at both personal endpoints, below the $5bn review bar. Freight already enters the existing road key. Its goods-output arm raises the lineage endpoints by 0.180/0.283bn, conditional on an approximate effective lineage split. None of the reported one-change arms reaches $5bn; unmeasured administration/enterprise shares leave larger changes unresolved. [CALCULATION: `analyze.py` → `derived/summary.json`] [INFERENCE]

Perspective: annual net resource/fiscal cost to other residents, income year 2024, personal allocation, specifications 16/11. Negative changes reduce that cost. These are conditional modeled reallocations of the frozen account, not measured causal budget effects, migration admission effects or welfare judgments. The public-capital return is imputed and never a cash/debt flow. The instrument is an LLM; primary-file parsing, positive controls and symmetric supply/demand arms constrain interpretive drift. [FRAMING-SENSITIVE] [DATA: frozen v7 payload, `meta.allocation`, `meta.capital_return`]

## Frame and the change being tested

The identified union has 39,712,493.33 members; the lineage 42,752,212.92. The union is the affine zero-addition intercept **at the lineage's current responses**, not a separate union-only removal with its own scale response. Its baseline is 317.743/395.811bn. `inventory.cjs` reuses the frozen `lineage_addition.cjs` construction with later-only and G3-rate-only cases; both the full case and the union intercept reproduce its oracle at 1e-9bn. The two fill-in methods are averaged after computing their individual changes. Endpoints remain specifications 16/11; tables give a fixed-endpoint pair and do not claim a newly optimized band over altered specifications. [CALCULATION: `inventory.cjs` → `derived/inventory.json`]

All arms start from the same v7 baseline. National budgets/stocks, responses, the household-serving part, production, all receipts, state-price intensity and the population frame hold fixed. Item 6's tax changes are neither added again nor recalculated. Business activity follows its corrected/smoothed industry wage-share method, weighted here by private gross output rather than tax bases. Government and housing output are excluded; private nonprofits remain. Mining's old service allocation is retained in the main proxy: nonmining numerator / full output + mining output fraction × old household/demand key. Added people take the case's G3plus/white wage shares times those groups' output factors, exactly the item-6 addition rule. This is a modeled industry profile for the unobserved added people. [DATA: `activity_keys.json`; `inventory.json:added_wage_shares`] [ASSUMPTION]

## Primary shares and what they measure

Police: the FBI 2023/2024 NIBRS location archives are parsed into selected commercial-location offense fractions. These are reported **offenses**, not deduplicated incidents, business victims or staff time. Fire: USFA NFIRS 2020 all-run property-use percentages, including EMS and aid, are parsed; the fire-only denominator is expressly rejected for all-department spending. Their dates/coverage differ. Commercial locations can contain household victims or medical calls. Treating a location fraction as a spending fraction requires equal resource intensity, an unverified assumption. The broad arm adds mixed/public uses and is not a higher measured business share. [SOURCE: FBI/USFA primary links and pins in `source-evidence.md`; DATA: `inputs/incident_shares.json`] [ASSUMPTION]

Police preserves the current half-offending/half-population construction, applying the business proxy only to the protective population half of the non-border pool. CBP and all ICE custody retain their keys. Fire's business fraction replaces its population allocation. Both changes preserve the current state-price correction using a common intensity factor; the location or cost index of business-serving work is not measured. BEA 2024 Table 3.16 provides police/fire/courts/prisons proportions; they close to the parent public-safety total and reproduce the existing CJ lane. That expense mix is a crosswalk to the current aggregate, not a newly observed line-specific budget. [CALCULATION: `spending_inputs.py` → `inputs/spending_shares.json`; `analyze.py` → `line_changes.csv`] [ASSUMPTION]

Courts and general administration: measured business involvement in state contract trials exists, but its denominator excludes most court work and gives no spending share. Their rekeying is **0 by unresolved-data assumption**, not a finding of zero business use. Courthouses are in office/general-government capital; those components remain unchanged. Municipal-enterprise business load fractions were not identified here. Their current capital keys and enterprise surplus remain unchanged; no generic output share is imposed on water, sewer, power, transit, airports, ports, toll roads or the residual. [SOURCE: BJS primary table and U.S. Courts catalog traced in `source-evidence.md`; DATA: `inventory.json:meta.capital_return`; GAP] [ASSUMPTION]

Highways: FHWA HCAS V-21 already splits cost responsibility between passenger vehicles (autos, pickups/vans, buses) and freight trucks. The inherited transcription was parsed, its 44 cells independently checked visually against the pinned primary image; this is not claimed as fresh OCR. Federal addendum HTML, VM-1 XLSX and Oregon's corrected PDF are parsed directly. Current truck mileage, federal cost responsibility and Oregon's heavy-vehicle forecast have different estimands; substitution arms do not form a statistical confidence interval. No measured national business-use share for light pickups/vans was obtained. [SOURCE: primary links/pins in `highways-evidence.md`; DATA: `inputs/highway_shares.json`]

The road demand arm retains the existing consumption-keyed freight contribution and changes nothing. The union freight key is verified against the authoritative pre-road v4 model with `roadKeysOf`, 1e-12; gasoline receipts remain fixed. The supply arm changes only that existing freight contribution and the corresponding highway-capital key once. [CALCULATION: `inventory.cjs:direct_union_road_keys`; `analyze.py`]

**[DEGRADED] Lineage freight split:** the age-mix item independently profiles the economic-affairs parent, roads correction and excise receipts. Their current totals can be inverted into an effective passenger/consumption pair, but that pair is not a literal measured lineage consumption key. Lineage supply-key and share-substitution arms are therefore effective-key approximations; union freight results use the verified principal key. This limitation affects the freight sensitivities, not the central-zero recommendation or the police/fire arm. [DATA: `method-review.md`; `main_case_2026_10_07/item_age_mix.cjs:profileOf`; INFERENCE]

## Every arm, one change from v7

Each entry is low / high in $bn/year. SEs apply only to the union and condition on the national functional/location shares, BEA output, pooling, mean fill-in factors, state-price intensity and mapped household key. Road consumption is held fixed in its SE. Replicate covariance is preserved by combining vectors before calculating SDR errors. No full lineage SE is reported: added people are not observed in CPS, and correlated model uncertainties are not propagated. [CALCULATION: `activity_keys.py`, `analyze.py`]

| Arm | Union Δ | Lineage Δ | Conditional union SE | $5bn bar |
|---|---|---|---|---|
| `unchanged_recommended` | +0.000 / +0.000 | +0.000 / +0.000 | 0.000 / 0.000 | below |
| `incident_proxy` | -1.032 / -1.032 | -1.124 / -1.124 | 0.051 / 0.051 | below |
| `incident_proxy_plain_wage` | -1.115 / -1.115 | -1.203 / -1.203 | 0.039 / 0.039 | below |
| `incident_proxy_mining_moves` | -1.028 / -1.028 | -1.119 / -1.119 | 0.052 / 0.052 | below |
| `police_2023_proxy` | -0.825 / -0.825 | -0.898 / -0.898 | 0.041 / 0.041 | below |
| `police_2024_proxy` | -0.844 / -0.844 | -0.919 / -0.919 | 0.042 / 0.042 | below |
| `fire_all_runs_proxy` | -0.188 / -0.188 | -0.205 / -0.205 | 0.009 / 0.009 | below |
| `broader_location_proxy` | -1.838 / -1.838 | -2.001 / -2.001 | 0.091 / 0.091 | below |
| `pos_capital_expenditure_mix_proxy` | -1.053 / -1.064 | -1.146 / -1.157 | 0.052 / 0.052 | below |
| `freight_demand_control` | +0.000 / +0.000 | +0.000 / +0.000 | 0.000 / 0.000 | below |
| `freight_goods_output` | +0.293 / +0.462 | +0.180 / +0.283 | 0.262 / 0.411 | below |
| `freight_goods_output_mining_moves` | +0.512 / +0.805 | +0.404 / +0.635 | 0.316 / 0.496 | below |
| `freight_plain_wage` | -0.173 / -0.272 | -0.283 / -0.445 | 0.086 / 0.136 | below |
| `oregon_cost_share_demand` | -0.033 / -0.051 | -0.032 / -0.050 | 0.000 / 0.000 | below |
| `federal_cost_share_demand` | -0.502 / -0.789 | -0.488 / -0.767 | 0.000 / 0.000 | below |
| `truck_vmt_2023_demand` | +0.760 / +1.196 | +0.739 / +1.163 | 0.000 / 0.000 | below |
| `truck_vmt_2024_demand` | +0.767 / +1.206 | +0.746 / +1.172 | 0.000 / 0.000 | below |
| `combined_incidents_goods_output` | -0.738 / -0.570 | -0.944 / -0.841 | 0.287 / 0.436 | below |

[CALCULATION: `derived/arms.csv`; full resulting levels and members in that file. `line_changes.csv` preserves method/line changes; `break_shares.csv` stores unresolved-share diagnostics.]

General administration would need a business-serving share of about 49.7%/34.0% to move the lineage endpoints by $5bn under this output key and expense/stock crosswalk. An illustrative 100% business allocation of the nonhousing municipal-enterprise capital alone moves them -3.522/-5.283bn, holding its surplus receipts fixed; that construction is not recommended. Thus the review's rough $3.5–14bn fall is not established by the acquired event data, but a larger fall cannot be ruled out without those missing expenditure/load shares. [CALCULATION: `break_shares.csv`] [ASSUMPTION]

## Complete spending and capital inventory

Amounts below are union / lineage charge at low then high, $bn/year, averaged across methods. Every responsive spending row and public-capital component is present; fixed spending rows also appear in `inventory.csv`. Synthetic corrections are signed adjustments, not new national budgets. The engine's authoritative amounts are used; the stored `share` field can differ from target/national after source re-pricing. Capital rule definitions and exact stocks/responses are retained in `inventory.json:meta.capital_return`. [CALCULATION: `inventory.cjs`]

| Spending line | Key | Response low/high | U low / L low / U high / L high |
|---|---|---|---|
| general_public_services | population | 0.601/0.851 | 28.342 / 30.511 / 40.165 / 43.240 |
| public_order_safety | use | 1.000/1.000 | 69.930 / 74.550 / 69.930 / 74.550 |
| economic_affairs_services | resources | 0.384/0.639 | 14.045 / 15.283 / 23.332 / 25.388 |
| housing_community_services | population | 1.000/1.000 | 1.728 / 1.860 / 1.728 / 1.860 |
| health_services | health_other | 1.000/1.000 | 18.096 / 19.352 / 18.096 / 19.352 |
| recreation_culture | population | 0.856/1.000 | 5.467 / 5.886 / 6.384 / 6.873 |
| education_services | education_mix | 1.000/1.000 | 195.256 / 216.304 / 195.256 / 216.304 |
| income_security_services | cash_assistance | 1.000/1.000 | 28.106 / 29.853 / 28.106 / 29.853 |
| social_security | social_security | 1.000/1.000 | 100.754 / 108.117 / 100.754 / 108.117 |
| medicare | medicare | 1.000/1.000 | 72.511 / 76.721 / 72.511 / 76.721 |
| unemployment | unemployment | 1.000/1.000 | 4.764 / 4.971 / 4.764 / 4.971 |
| railroad_retirement | social_security | 1.000/1.000 | 0.531 / 0.567 / 0.531 / 0.567 |
| pension_guaranty | age65plus | 1.000/1.000 | 0.038 / 0.040 / 0.038 / 0.040 |
| veterans_life_insurance | veterans | 1.000/1.000 | 0.023 / 0.025 / 0.023 / 0.025 |
| workers_compensation | workers_comp | 1.000/1.000 | 1.556 / 1.643 / 1.556 / 1.643 |
| military_medical | tricare | 1.000/1.000 | 0.313 / 0.351 / 0.313 / 0.351 |
| veterans_pension_disability | veterans | 1.000/1.000 | 9.133 / 9.987 / 9.133 / 9.987 |
| veterans_readjustment | veterans | 1.000/1.000 | 0.576 / 0.630 / 0.576 / 0.630 |
| veterans_other | va_medical | 1.000/1.000 | 1.597 / 1.735 / 1.597 / 1.735 |
| snap | snap | 1.000/1.000 | 13.589 / 14.625 / 13.589 / 14.625 |
| black_lung | workers_comp | 1.000/1.000 | 0.033 / 0.035 / 0.033 / 0.035 |
| ssi | ssi | 1.000/1.000 | 5.094 / 5.463 / 5.094 / 5.463 |
| refundable_tax_credits | refundable_credits | 1.000/1.000 | 35.152 / 37.170 / 35.152 / 37.170 |
| other_federal_benefits | all_cash | 1.000/1.000 | 6.793 / 6.980 / 6.793 / 6.980 |
| temporary_disability | workers_comp | 1.000/1.000 | 2.521 / 2.652 / 2.521 / 2.652 |
| medicaid_and_chip_other_medical | uninsured_use_low | 1.000/1.000 | 117.640 / 126.087 / 119.736 / 128.209 |
| family_and_general_assistance | cash_assistance | 1.000/1.000 | 11.687 / 12.361 / 11.687 / 12.361 |
| energy_assistance | energy | 1.000/1.000 | 0.562 / 0.605 / 0.562 / 0.605 |
| other_state_welfare | wic | 1.000/1.000 | 5.214 / 5.602 / 5.214 / 5.602 |
| education_benefits | postsecondary | 1.000/1.000 | 8.945 / 9.604 / 8.945 / 9.604 |
| employment_training | working_age | 1.000/1.000 | 0.167 / 0.177 / 0.167 / 0.177 |
| other_state_benefits | population | 1.000/1.000 | 0.337 / 0.363 / 0.337 / 0.363 |
| housing_subsidies | housing_support | 1.000/1.000 | 4.137 / 4.489 / 4.137 / 4.489 |
| school_reprice | k | 0.715/0.865 | 0.427 / 0.302 / 0.516 / 0.365 |
| college_rekey | k | 0.285/0.135 | -1.339 / -1.476 / -0.634 / -0.699 |
| lane_constants | k | 1.000/1.000 | -5.209 / -5.400 / -5.209 / -5.400 |
| roads_vmt_sl | k | 0.740/1.000 | 2.243 / 2.267 / 3.030 / 3.063 |
| roads_vmt_fed | k | 0.000/1.000 | 0.000 / 0.000 / 0.028 / 0.028 |
| state_price_public_order_safety | k | 1.000/1.000 | 6.704 / 6.931 / 6.704 / 6.931 |
| state_price_health_services | k | 1.000/1.000 | 1.901 / 1.970 / 1.901 / 1.970 |
| state_price_recreation_culture | k | 0.856/1.000 | 0.362 / 0.377 / 0.423 / 0.440 |

Capital business shares are zero in the recommended central. Highway supply arms carry their altered road key through both spending and capital. The POS-capital arm additionally imposes the expense proxy mix on public-safety structures; that spending-to-stock crosswalk is unmeasured, so it stays beside the central. Office/courthouse stock stays fixed. [ASSUMPTION]

| Capital component | Key rule | Response rule | U low / L low / U high / L high |
|---|---|---|---|
| k12 | lines_amount_over_national | line_response_over_share | 8.700 / 9.627 / 13.050 / 14.441 |
| college | lines_amount_over_national | line_response_over_share | 3.724 / 4.126 / 5.586 / 6.189 |
| pos_sl | lines_amount_over_national | line_response | 0.777 / 0.828 / 1.165 / 1.242 |
| pos_fed | lines_amount_over_national | line_response | 0.296 / 0.315 / 0.444 / 0.473 |
| health_sl | lines_amount_over_national | line_response | 0.430 / 0.459 / 0.644 / 0.689 |
| health_fed | lines_amount_over_national | line_response | 0.124 / 0.133 / 0.187 / 0.200 |
| gps_sl | lines_amount_over_national | line_response | 1.820 / 1.959 / 3.868 / 4.164 |
| gps_fed | lines_amount_over_national | line_response | 0.214 / 0.231 / 0.455 / 0.490 |
| hwy_sl | part_rekeyed | long_run_subfunction | 6.217 / 6.689 / 12.599 / 13.556 |
| rec_sl | lines_amount_over_national | long_run_subfunction | 0.948 / 1.020 / 1.494 / 1.609 |
| hwy_fed | part_rekeyed | long_run_subfunction | 0.000 / 0.000 / 0.157 / 0.169 |
| air_fed | lines_amount_over_national | long_run_subfunction | 0.000 / 0.000 / 0.086 / 0.093 |
| rec_fed | lines_amount_over_national | long_run_subfunction | 0.000 / 0.000 / 0.147 / 0.158 |
| ent_housing_sl | lines_amount_over_national | enterprises_switch | 0.632 / 0.686 / 0.949 / 1.029 |
| ent_transit_sl | receipt_amount_over_national | enterprises_switch | 1.185 / 1.276 / 1.778 / 1.914 |
| ent_airports_sl | receipt_amount_over_national | enterprises_switch | 1.396 / 1.503 / 2.094 / 2.255 |
| ent_ports_sl | receipt_amount_over_national | enterprises_switch | 0.221 / 0.238 / 0.332 / 0.357 |
| ent_power_sl | receipt_amount_over_national | enterprises_switch | 1.270 / 1.368 / 1.905 / 2.051 |
| ent_water_sl | receipt_amount_over_national | enterprises_switch | 2.147 / 2.311 / 3.220 / 3.466 |
| ent_sewer_sl | receipt_amount_over_national | enterprises_switch | 2.871 / 3.090 / 4.306 / 4.635 |
| ent_tolls_sl | receipt_amount_over_national | enterprises_switch | 1.175 / 1.264 / 1.762 / 1.897 |
| ent_power_fed | receipt_amount_over_national | enterprises_switch | 0.065 / 0.070 / 0.097 / 0.105 |
| ent_other_sl | receipt_amount_over_national | enterprises_switch | 0.177 / 0.190 / 0.265 / 0.286 |
| ent_other_fed | receipt_amount_over_national | enterprises_switch | 0.133 / 0.143 / 0.199 / 0.215 |
| k12_user_fees | receipt_amount_over_national | line_response_over_share | 0.531 / 0.531 / 0.797 / 0.797 |
| college_user_fees | receipt_amount_over_national | line_response_over_share | -0.924 / -0.924 / -1.386 / -1.386 |
| health_sl_user_fees | receipt_amount_over_national | line_response | -0.015 / -0.015 / -0.023 / -0.023 |
| health_fed_user_fees | receipt_amount_over_national | line_response | -0.004 / -0.004 / -0.007 / -0.007 |

## Gates, files and reproduction

- Source/control SHA256 manifest: `inputs/pins.json` (26 records); changing a pinned source fails loudly.
- Existing-case positive controls: `inventory.cjs`, 316 gates, v7 and union intercept to 1e-9bn.
- Activity: 36 gates; generation/replicate conservation, old cell shares/SEs, primary-output normalization and national closure to 1e-6bn.
- National safety subfunctions close to one at 1e-12 and reproduce the CJ lane to 1e-9bn. FBI totals close exactly; printed source percentages retain explicit rounding bounds.
- Sensitivities: 897 gates, union road keys independently verified, zero-change controls, unchanged national budget/stock construction.
- `test_gates.py`: demand/freight overlap regression, every output's line closure, stale-source rejection, absent lineage SE. Incident acquisition also has source-corruption and wrong-total negative controls.
- Derived files: `inventory.json`, `inventory.csv`, `activity_keys.json`, `arms.csv`, `line_changes.csv`, `break_shares.csv`, `summary.json`.

Run offline from the repository root (default extraction commands do not download):

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/business_services_key_2026_10_14 \
  "uv run --no-project python3 {lane}/pins.py" \
  "node {lane}/inventory.cjs" \
  "uv run --no-project python3 {lane}/spending_inputs.py" \
  "uv run --no-project python3 {lane}/acquire_highways.py" \
  "uv run --no-project python3 {lane}/acquire_incidents.py --self-check" \
  "uv run --no-project python3 {lane}/activity_keys.py" \
  "uv run --no-project python3 {lane}/analyze.py" \
  "uv run --no-project python3 {lane}/test_gates.py" \
  "uv run --no-project python3 {lane}/report.py"
```

No `--allow-unrun` is needed. The final handoff records the lane-wide command's observed exit code and IDENTICAL count. Source acquisition for a fresh cache is documented in the source evidence files; initialization refuses to replace existing pins. No frozen case, other lane, research document or Git metadata is mutated.

## Log

- 2026-10-14 20:36:37 JST (`date`): scope/status read; handoff created before computation.
- 2026-10-14 20:41:31 JST (`date`): existing freight split and safety keys traced; inventory and safety-source controls passed.
- 2026-10-14 20:52:51 JST (`date`): all primary source subtasks read; first integrated proxy/freight rows inspected.
- 2026-10-14 20:56:36 JST (`date`): result rendered from current outputs; independent method review integrated. Activity builds used 3.85–17.22s and 1.09–1.60GB peak RSS; incident/highway/safety parsers each under 1s and 0.08GB. Integrated analysis under 0.02s. Measurements are Python `time.perf_counter`/`resource.getrusage`, not `/usr/bin/time -l`. Final combined rerun timing belongs to the handoff. [CALCULATION: script stdout and source evidence logs]
