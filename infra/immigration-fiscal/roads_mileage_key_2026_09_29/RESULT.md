claude-opus-5-5
**Verdict:** Keying roads by use raises the group's cost by **+$1.96bn at the low end and +$3.69bn at the high end**, taking the case from $321.82–387.37bn to **$323.78–391.06bn**. This is a candidate for the next revision; nothing is adopted. [CALCULATION: `rekey.cjs` → `derived/summary.json`]

- **Spending rises by +$3.19bn (low end) and +$5.02bn (high end).** Highway consumption adds +$2.22 / 3.03bn and the road capital return adds +$0.97 / 1.99bn.
- **Receipts rise by +$1.23bn and +$1.33bn.** Gasoline taxes add +$1.44bn at both ends; personal motor vehicle licences subtract −$0.20 / 0.11bn.

The road key moves from 8.06% (SPM resources) to 9.56%: passenger costs at the group's share of driver miles (10.12%) and freight costs at its consumption share (8.12%). Across the three NHTS ratios the change runs from **+$0.88bn to +$2.06bn at the low end and from +$0.91bn to +$3.97bn at the high end**. The 2022 national file (0.692) gives the low figures and the 2017 national file (0.893) the high ones. The central 2017 south-western cut (0.874) sits near the top of that range.

The group drives **13.6% fewer miles per head** than the average resident (0.864), not 11%. NHTS counts only persons aged 5 and over, and 8.0% of the group is under 5 against 5.2% of other residents.

# Roads keyed by vehicle miles: candidate re-key of the economic-affairs line

Lane `roads_mileage_key_2026_09_29`, 2026-09-29. The lane adopts nothing and edits no other lane. Brief: the team lead's message (question, inputs and gates as below).

## Results

All figures are changes to the adopted band. Each is the mean of the two fill-in methods, taken at the end specifications of `main_case_long_run_2026_09_27/derived/summary.json`.

| NHTS driver-VMT ratio (group / non-Hispanic, per person 5+) | Group VMT share | vs average resident | Road key | Spending low / high | Receipts low / high | **Cost change low / high** | Case $bn |
|---|---:|---:|---:|---:|---:|---:|---:|
| **2017 south-west, 0.874 (central)** | 10.12% | 0.864 | 9.56% | +3.19 / +5.02 | +1.23 / +1.33 | **+1.96 / +3.69** | 323.78–391.06 |
| 2017 national, 0.893 | 10.32% | 0.880 | 9.69% | +3.49 / +5.49 | +1.42 / +1.52 | **+2.06 / +3.97** | 323.88–391.34 |
| 2022 national, 0.692 (1,722 Hispanic persons) | 8.18% | 0.698 | 8.16% | +0.22 / +0.34 | −0.67 / −0.57 | **+0.88 / +0.91** | 322.70–388.28 |

At the central ratio, spending and receipts split into these components ($bn, low / high end):

| Component | Low | High | Rule |
|---|---:|---:|---|
| Highway consumption (S&L $201.005bn at 0.739 / 1, federal $1.827bn at 0 / 1) | +2.221 | +3.031 | (road key − 8.06%) × amount × subfunction response |
| Road capital return (hwy_sl $4,389bn, hwy_fed $54.6bn stock at 2% / 3%) | +0.970 | +1.992 | same key change × stock × rate × response |
| Gasoline taxes ($71.71bn: federal $26.86bn + 75.9% of State motor-fuel taxes $59.10bn) | +1.438 | +1.438 | (VMT share − consumption share) × taxes × 1 |
| Personal motor vehicle licences ($26.125bn) | −0.203 | −0.107 | (VMT share − adults share 10.90% / 10.53%) × licences × 1 |
| **Cost change** | **+1.956** | **+3.693** | spending − receipts |

[CALCULATION: `derived/rekey_lines.csv`, per method and mean; `derived/keys.csv`]

**Variants.** Each variant changes one input at the central ratio; the table uses line arithmetic.

| Variant | Low | High |
|---|---:|---:|
| Central | +1.96 | +3.69 |
| NHTS ratio applied per resident, with no under-5 adjustment (the brief's "11% fewer") | +2.11 | +4.09 |
| Passenger share of S&L cost responsibility only (0.751) | +2.10 | +3.92 |
| Passenger share of federal cost responsibility only (0.604) | +1.47 | +2.93 |
| Licences left at the adults key | +1.75 | +3.59 |

[CALCULATION: `derived/summary.json` → `variants_central_ratio`]

## Method

**What moves.** The adopted case charges each economic-affairs subfunction at the line's key times the subfunction's long-run response. The key is SPM resources: 0.080780 under the hot-deck method and 0.080440 under matched-over-pooled, mean 8.06%. The engine applies the amount-weighted blend of the subfunction responses. The road capital components (hwy_sl, hwy_fed) take the same line share as their key. Re-keying the two highway subfunctions from k_old to k_road therefore changes the cost by:

- highway consumption: (k_road − k_old) × (S&L highways × r_sl + federal highways × r_fed);
- road capital return: (k_road − k_old) × rate × (the hwy_sl stock × r_sl + the hwy_fed stock × r_fed).

The responses are the adopted ones (0.7392 / 1 for S&L, 0 / 1 for federal) and are left unchanged. Air, water, transit, space, administration, agriculture, energy and natural resources keep the resources key. None of them is road use. S&L transit consumption in the line is zero (transit is an enterprise), and federal transit is $0.09bn. [DATA: `service_response_long_run_2026_09_27/derived/responses.json`; `capital_return_services_2026_09_27/derived/engine_components.json`]

**Keys.**
- **Driver VMT share.** s_vmt = p(1−u_g)ρ / [p(1−u_g)ρ + (1−p)(1−u_o)].
  - p = 0.117175 is the account's per-head share, the corrected population cell that `populationShare()` reads.
  - u_g = 7.97% and u_o = 5.18% are the under-5 shares from row-4 weights (`main_case_decomposition_2026_09_29/derived/age_bins.csv`).
  - ρ is the NHTS ratio of driver VMT per person aged 5+, Hispanic against non-Hispanic (`congestion_2026_09_23/derived/nhts_ratios.csv`). Hispanic persons stand in for the Mexican-origin group, as in the congestion and crash lanes. [DATA]
- **Road key.** k_road = f_p × s_vmt + (1 − f_p) × k_cons.
  - f_p = 0.7168 is the passenger share (autos, pickups and vans, buses) of 2000 highway cost responsibility for all levels of government. [SOURCE: FHWA, 1997 Federal Highway Cost Allocation Study, Table V-21, https://www.fhwa.dot.gov/policy/hcas/final/five.cfm; transcribed in `derived/hcas_v21.csv`]
  - k_cons is the case's corrected consumption share, read from excise_selective_sales: 0.081364 / 0.081006. Freight is keyed there because its cost ends up in what people buy.
  - The all-levels share is used because the line consolidates federal grants into S&L consumption. The S&L-only and federal-only shares appear as variants.
  - Buses are 0.7% of cost and sit in HCAS's passenger row. Keying them per head would move the result by less than $0.04bn [CALCULATION: 0.007 × (0.117 − 0.101) × ($203bn of highways + $133bn of capital return at 3%)].
- **Receipts, keyed by the same symmetry.**
  - **Gasoline taxes move to s_vmt.** They are the federal gasoline excise ($26.864bn, NIPA Table 3.5 line 5) plus the gasoline part of State motor-fuel taxes ($59.096bn, line 25, times 0.7589).
  - **The 0.7589 split.** It is Σ_state gallons × rate over MF-2 (net gallons taxed, 2023) and MF-121T (State gasoline and diesel rates, 31 Dec 2023). The gallon share alone gives 0.7588. [DATA: `derived/state_fuel_split.csv`]
  - **Diesel stays at the consumption key.** This covers federal diesel ($10.379bn), the diesel part of State taxes and the federal truck and tyre excises. That is where freight is keyed, so none of it moves.
  - **Personal motor vehicle licences move from the adults key to s_vmt** (NIPA 3.4 line 10, $26.125bn).
  - **Business licences are unchanged.** They are $15.0bn (3.5 line 40) inside other_production_taxes, which responds at 0, so no key moves them.
  - **Fuel economy is not adjusted.** There are no group data on it.
  - Both receipt lines respond at 1 in the adopted case.
- **Engine run.** For each fill-in method the corrected model gets the following. The engine's cost change is the same as the line arithmetic.
  - Two synthetic spending lines (`roads_vmt_sl`, `roads_vmt_fed`) carry N × (k_road − k_old) per allocation. They take the subfunction responses through `line_responses`.
  - Receipt shifts, `expand()`ed to every incidence rule, move excise_selective_sales by gasoline × (s_vmt − k_cons) and licences by $26.125bn × (s_vmt − k_adults).
  - An in-memory capital variant keys hwy_sl and hwy_fed at the constant k_road for that method and allocation. No file is edited.
  - `evaluateFull` then runs at the case's end specifications (48 and 11).

## Gates

1. **Positive control (pass):** the probe reproduces the adopted band, $321.819357 / 387.370055bn, which matches `summary.json` to 1e-6.
2. **Engine delta equals line arithmetic (pass, all three ratios):** the largest gap is 7e-14 $bn. The synthetic lines took their subfunction responses, the capital components took k_road, and national totals hold on the edited receipt cells.
3. **Shares sum to 1 (pass):** the group and other residents' shares sum to 1 to 1e-12 under the VMT key and under the road blend. This holds for every ratio, allocation and method, and for the four key variants.
4. **Byte-identical reruns (pass):** `inputs.py` and `rekey.cjs` were rerun into a scratch `--out-dir`. Both exit 0, and all 6 derived files are identical (`hcas_v21.csv`, `inputs.json`, `keys.csv`, `rekey_lines.csv`, `state_fuel_split.csv`, `summary.json`).

Supporting checks (`derived/inputs.json` → `gates`, 25 pass):
- The cached sources match their pinned sha256.
- The NIPA line labels and series codes are checked, and lines 4 + 23 reproduce model.json's $371.262bn.
- MF-2's State rows add to its printed totals.
- Table V-21's rows add across levels and to its subtotal rows, and its total matches the page text ($125bn; autos $64bn).
- The evaluation's shares equal the model's cells, and its line response equals the blend of the adopted subfunction responses.

**One check failed and was replaced.** Before seeing the data, the lane set a check that gallons × rates reproduce MF-1's gross State motor-fuel collections within 10%. The result was +13.0% ($62.11bn against $54.95bn), because rates as of 31 Dec 2023 overstate a year in which several States changed rates [INFERENCE]. The level is only a control: the split uses the share, which the weighting barely moves (0.7589 against 0.7588). The recorded checks are now "within 15%" and "the two weightings agree within 1 point".

## What this does not settle

- **Which NHTS ratio.** The spread is wide at the high end: +$0.91bn with 2022, +$3.97bn with 2017 national.
  - The 2022 file has 1,722 Hispanic persons and follows the pandemic's shift in commuting. The congestion lane chose the 2017 south-western cut as central, and this lane keeps it.
  - At 0.692 the group's VMT share (8.18%) almost equals its consumption share, so gasoline taxes barely move. The licence re-key then subtracts −$0.71 / −0.61bn from receipts.
- **Others include non-Mexican Hispanics.** NHTS compares against non-Hispanics, but the account's other residents include about 25M other Hispanics, who drive less. Correcting this would lower others' VMT by about 1%. That raises s_vmt by about 0.001 and the cost by about +$0.05bn (low end) to +$0.14bn (high end). [INFERENCE; not computed in the script]
- **Business use of light vehicles.** HCAS puts pickups and vans in the passenger row, and gasoline taxes include commercial light-vehicle fuel. Both are keyed by household VMT here. The same error sits on both sides, so it partly cancels. [INFERENCE]
- **HCAS vintage and cost type.**
  - Table V-21 allocates 2000 program costs, mostly capital. The line is consumption: maintenance, operation and depreciation.
  - Pavement wear is load-driven, so freight's share of consumption could differ from its share of program costs.
  - The federal-only (0.604) and S&L-only (0.751) shares bracket the central at +$1.47–2.10 (low end) and +$2.93–3.92 (high end). [FRAMING-SENSITIVE]
- **Licences.** Registration fees are paid per vehicle, and California's are value-based. VMT is the symmetric road-user key. A vehicles key would need an NHTS vehicle tabulation this lane did not run [GAP]. The adults-key variant bounds the item at +$0.20 / 0.11bn.
- **Cross-lane flag.** The crash lane's s = 10.8% uses 12.1% of residents and no under-5 adjustment. The same NHTS ratio gives 10.12% on the account's headcount and age mix. Any account item that scales with s would shrink by about 6% if restated on this basis. [CALCULATION: `derived/keys.csv`; the crash lane is not edited]
- **What is not touched.** Tolls sit in the enterprise surplus. Highway patrol is in public order and safety. The congestion item stays beside the account.

## Files

- `inputs.py` reads primary sources (NIPA 3.5 and 3.4 from the pinned workbook, FHWA MF-1, MF-2 and MF-121T for 2023, HCAS Table V-21) and the two lane inputs. It writes `derived/inputs.json`, `derived/state_fuel_split.csv` and `derived/hcas_v21.csv`, with 25 gates.
- `rekey.cjs` runs the probe, keys, line arithmetic and engine run, with gates 1–3. It writes `derived/keys.csv`, `derived/rekey_lines.csv` and `derived/summary.json`.
- `_cache/` is ignored and holds the FHWA pages and tables fetched 2026-09-29, pinned by sha256 in `inputs.py`. The Table V-21 image is a Wayback copy of `final/five/img27.gif`, because FHWA timed out.

Run from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project --offline python3 infra/immigration-fiscal/roads_mileage_key_2026_09_29/inputs.py
node infra/immigration-fiscal/roads_mileage_key_2026_09_29/rekey.cjs
```

## Log (append-only; times from `date`)

- stub written before any read.
- 01:36 read the engine chain (`main_case_long_run_2026_09_27/package.cjs` → schools → Sept 24 package →
  `assumption_explorer_2026_09_21/engine.js`). economic_affairs_services is NIPA Table 3.17 line 5 consumption,
  $451.935bn, key `resources`; its highway subfunctions (service_response_long_run_2026_09_27 responses.json) are
  S&L $201.005bn (response 0.7392 / 1) and federal $1.827bn (0 / 1). The road capital return (hwy_sl $4,389.0bn,
  hwy_fed $54.6bn stock) is keyed by the same line share, so it moves with the re-key. [DATA]
- 01:50 NIPA Table 3.5, 2024 (pinned Section3All workbook): federal gasoline $26.864bn (line 5), federal diesel
  $10.379bn (line 8), S&L "gasoline" $59.096bn (line 25, all state motor-fuel taxes: FHWA MF-1 2023 gross
  $54.95bn), all inside excise_selective_sales ($371.262bn = lines 4 + 23). Personal motor vehicle licences $26.125bn
  (Table 3.4 line 10); business licences (3.5 line 40, $15.0bn) sit in other_production_taxes at response 0. [DATA]
- 02:00 HCAS 1997 Table V-21 (all levels of government, 2000, $m) read from the page's image (Wayback copy of
  `final/five/img27.gif`; FHWA timed out): passenger vehicles $89,832m of $125,322m. The image stops at the
  ≥80,000 lb row; the combination-truck and all-vehicle totals are summed from the rows and match the page text
  ($125bn total, autos $64bn). [SOURCE: fhwa.dot.gov/policy/hcas/final/five.cfm]
- 02:10 FHWA Highway Statistics 2023 MF-2 (gallons taxed by fuel and state) and MF-121T (state rates, 31 Dec 2023)
  fetched to split state motor-fuel taxes into gasoline and diesel. Firecrawl search returned 402 (credits). [DATA]
- 02:25 the 10% MF-1 level check failed (+13.0%); replaced by a 15% level control plus the share-robustness gate
  (0.7589 rate-weighted vs 0.7588 gallon-weighted). All gates pass; central +$1.956 / +3.693bn; reruns into a
  scratch directory byte-identical (6 files).
- 02:27 RESULT written with results, variants, gates and open points.

## Lead verification (2026-09-29 02:37 JST)

- Hand arithmetic reproduces the central row: road key 0.7168 × 10.12% + 0.2832 × 8.12% = 9.55%; highway consumption 0.0150 × (201.005 × 0.7392) = +2.23 (low), 0.0150 × 202.83 = +3.04 (high); capital return 0.0150 × 2% × (4,389 × 0.7392) = +0.97 (low), 0.0150 × 3% × 4,443.6 = +2.00 (high); gasoline (0.1012 − 0.0812) × 71.71 = +1.43; licences (0.1012 − 0.1090) × 26.125 = −0.20 (low), −0.11 (high). Net +1.96 / +3.69.
- `scripts/rerun_lane.py` over inputs.py and rekey.cjs: IDENTICAL 9/9.
- The cross-lane flag stands: the crash and congestion items read the group's VMT share as 10.8% (12.1% of residents, no under-5 adjustment); on the account's headcount and age mix it is 10.12%. Queued with the population-basis restatement for the next revision.
