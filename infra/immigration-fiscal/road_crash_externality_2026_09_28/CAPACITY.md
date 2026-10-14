**Verdict:** On the requested arm that treats both multi-vehicle and non-motorist volume effects as density effects, the union's crash row becomes **$7.031 / $5.628bn**, down **$3.535 / $4.939bn** at the case's low / high ends. The v7 road-key lineage extrapolation, with its recipient boundary held fixed, moves **−$3.765 / −$5.259bn**: only the high end clears the $5bn review bar. This is conditional on transferring pedestrian/cyclist traffic-volume elasticities to road density. Keeping those elasticities on total motor traffic instead gives a small increase. Both arms are delivered; neither changes the original producer or any consumer. [CALCULATION: `capacity_response.py` → `derived/capacity_items.csv`] [ASSUMPTION]

## What changes and what is held fixed

Frame: with versus without the group, personal allocation at specifications 16 / 11 of main case v7, `oct14`. Costs are annual 2024 dollars, at the original lane's crash counts. The union is audit row 4's 39,712,493 people, with NHTS ratios applied to persons aged 5+. The added descendants bring the lineage to 42,752,213. The beneficiaries of the union row are residents outside the union; the `lineage` rows remove the added descendants from recipients under an exchangeable-recipient assumption. [DATA: `population_basis_2026_09_29/derived/frame_counts.csv`; `main_case_decomposition_2026_09_29/derived/age_bins.csv`; `sept24_propagation_2026_09_24/derived/oct14/band_variants.json`]

The road-capacity cuts are the congestion case's own uniform cuts: **0.059051 / 0.080610**, recomputed from its national-amount-weighted highway responses times the group's economic-affairs key and gated to `net_change.json`. Congestion's $13.602 / $11.617bn are dollar-valued time savings; their ratio to fixed-network congestion is not a physical density ratio. This computation uses the actual capacity cut, not that monetary ratio. The congestion producer flags that it has not recomputed its network since v4's roads-by-mile change; this task deliberately uses the same network as that row rather than silently updating it. [DATA: `service_response_long_run_2026_09_27/congestion.py:133-165`, its `derived/net_change.json`; `main_case_2026_09_29/derived/summary.json` `beside_the_account.congestion.not_recomputed`]

Let `s` be the group's share of VMT and `c` the capacity cut. With remaining residents' VMT fixed, without/with VMT per lane is `(1-s)/(1-c)`. Residual density relief is `d = 1-(1-s)/(1-c)` and each original density term is multiplied by `d/s`. The original crash model is linear in the finite traffic share, so this keeps its finite-change convention. Negative relief is retained when `c>s`. At central inputs, `s=0.102233`, so relief is **0.045892 / 0.023519**, multipliers **0.448898 / 0.230049**. No extra driving by other residents is assumed. [CALCULATION: `capacity_response.py` `residual_share()` → `derived/capacity_components.csv`] [ASSUMPTION]

The four density terms are exactly the original `x`/`beta` volume terms before composition: nonfatal and fatal multi-vehicle, nonfatal and fatal pedestrian/cyclist. The original composition term **$1.691bn**, liability flows, single-vehicle loss **$1.914bn**, all prices, culpability odds, victim shares, exposure mixing, and every grid factor stay fixed. Density plus all held terms closes to each original cell at below 1e-9bn; the national cost components also close below 1e-9bn. [CALCULATION: `density_parts()`; `derived/capacity_model.json` gates]

## Results

Each span is the minimum and maximum over the original 19,683 combinations, recomputed for that capacity cut. It is a sensitivity span, not a confidence interval. Replicate SEs are unavailable: the producer supplies a factorial grid, not joint replicate estimates of culpability, density and capacity. The union's original published control is **11.053646bn (−57.681946 to +74.337390)**. On the live row-4, age-5+ frame, its fixed-network baseline is **10.566366bn (−55.071430 to +70.843377)**. [CALCULATION: `capacity_response.py` → `derived/capacity_model.json`]

| Population and arm | Low-end central | Low-end span | High-end central | High-end span | Capacity-only change, low / high |
|---|---:|---:|---:|---:|---:|
| Union, all density | 7.031 | −28.627 to 41.156 | 5.628 | −18.126 to 29.367 | −3.535 / −4.939 |
| Lineage gross, all density | 7.566 | −30.802 to 44.283 | 6.055 | −19.503 to 31.598 | −3.804 / −5.314 |
| Lineage outside recipients, all density | 7.488 | −30.485 to 43.828 | 5.993 | −19.302 to 31.274 | −3.765 / −5.259 |
| Union, multi-vehicle only | 10.962 | −27.395 to 52.256 | 11.119 | −16.404 to 44.874 | +0.396 / +0.553 |
| Lineage outside recipients, multi-vehicle only | 11.674 | −29.173 to 55.648 | 11.841 | −17.469 to 47.787 | +0.421 / +0.589 |

[CALCULATION: `derived/capacity_items.csv`; exact extrema and their factor indices: `derived/capacity_extrema.csv`]

The lineage extrapolation preserves v7's existing road key, added/union **0.075974451**, at both ends [ASSUMPTION]. It scales the union calculation, including its capacity adjustment, rather than identifying a separate geography, crash composition or VMT response for descendants no longer reporting Mexican origin. The recipient correction removes added/(CPS civilian − union) = **1.027518%** of losses [ASSUMPTION: exchangeable recipients]. The lineage factor is `(1+road_key)*(1-recipient_share) = 1.064918618`. This preserves the original composition term after the same boundary/extrapolation scaling; it does not claim the added people's composition has been measured. [DATA: `derived/capacity_model.json` `recipient_share`, `ends`; `band_variants.json` `lineage_social_keys`]

Capacity-only changes compare matching recipient boundaries: the lineage baseline is $11.252320bn. The gross legacy-live baseline is $11.369140bn. If the recipient correction is adopted simultaneously, total changes from that gross baseline are **−$3.881346 / −$5.376282bn**. `change_from_gross_live_bn` reports that combined change explicitly; use `change_bn` when another worker already handles the recipient correction. [CALCULATION: `derived/capacity_items.csv`]

## Disconfirmation and limits

The lower row is not a mathematical consequence of capacity adjustment alone. In `crash_model.py`, multi-vehicle `x` is per-mile risk elasticity to traffic on a fixed network, while `beta` is the elasticity of pedestrian/cyclist crashes to total motor traffic. The data do not separately identify capacity's effect on those pedestrians, crossings or route lengths. Applying `beta` to density is an additional premise. If only multi-vehicle terms follow VMT/lane and the pedestrian/cyclist term remains proportional to motor traffic, the central increases slightly, because the original central multi-vehicle density contribution is negative (−$0.718bn). The requested decrease is driven by the non-motorist channel. [DATA: `crash_model.py:13-17,245-255`; `derived/capacity_components.csv`] [INFERENCE]

The strongest case for the all-density arm is a road network that expands traffic and the opportunities for pedestrians/cyclists proportionally, leaving risk per mile unchanged at constant density. Its strongest alternative is that road capacity changes speeds and vehicle interaction while pedestrians still face the lower volume of motor traffic. Evidence separately estimating crash severity and pedestrian/cyclist risk under capacity changes, at fixed traffic and victim exposure, would distinguish them. This lane does not infer +$18–25bn by assuming others' own VMT disappears with the group's share. [ASSUMPTION / INFERENCE]

No new source coefficient is fitted or typed from a paper. Existing inputs are pinned in `inputs/pins.json`; each dependency is verified before computation. The baseline crash producer's underlying price and culpability limitations remain those documented in its historical RESULT. An LLM conducted the implementation; the numeric identities and independent channels are exposed to limit framing-driven interpretation. [DATA: `inputs/pins.json`; `capacity_response.py`]

## Integration note: exact keys and overlap

Read `derived/capacity_items.csv` using the unique key **`item=road_crash_externality_capacity_response, measure=absolute, end=low|high, arm=all_density|multivehicle_only, population=union|lineage_gross|lineage`**. Original `items.csv` and `crash_model.py` are unchanged so historical controls and current consumers continue to reproduce. The parent chooses the arm and changes the live consumer separately.

To replace the union crash row, select `population=union`; it already uses row-4 weights and the age-5+ traffic basis, so do not apply the population-restatement factor again. To replace the whole lineage row with the recipient correction included, select `population=lineage`; do not multiply by the added-people road key or recipient correction again. `lineage_gross` is a boundary-comparison arm, retaining added descendants among recipients, and must not enter an outside-lineage total. Each row carries `comparator=with_without`, the explicit `beneficiary_population`, `valuation_basis=crash_resource_and_harm`, and JSON `overlap_set=["mortality","road_congestion"]`.

Replace the crash row; never add the new row to it. Congestion delay and EMS remain excluded from the comprehensive crash base. The fault-based and normalized alternatives are unchanged and remain beside the total. Broader overlap of publicly funded crash care/lost taxes is inherited, not resolved by this capacity arm. The output does not alter the fiscal account, PM2.5 or the congestion row itself. `capacity_components.csv` is a decomposition, never an additional item.

## Gates and reproduction

`capacity_response.py` passes **1,017 gates**: every pinned dependency; original central and full span before changes; original and row-4 traffic self-exposure with area-by-area conservation; row-4 and live age-5+ central controls; live full span; national cost closure; the congestion case's capacity cuts; lineage population closure and personal end specifications; component closure and preservation of all nondensity terms over every grid cell; zero-cut and density-held controls; unique output keys. No tolerance was loosened.

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/road_crash_externality_2026_09_28/capacity_response.py
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/road_crash_externality_2026_09_28 \
  "uv run --no-project python3 {lane}/fars_group.py" \
  "uv run --no-project python3 {lane}/crash_model.py" \
  "uv run --no-project python3 {lane}/capacity_response.py"
```

The original FARS and crash producer commands remain part of the lane's reproducibility check; no `--allow-unrun` exemption is needed. Timing and maximum resident memory use Python `time.perf_counter` and `resource.getrusage`, printed separately from deterministic derived outputs.

## Log (times from `date`)

- 2026-10-14 21:58:33 JST — traced the capacity cut to the congestion producer and read the live case and consumer declarations.
- 2026-10-14 22:02:07 JST — the requested all-density calculation and the multi-vehicle-only disconfirmation arm pass; original and live-frame positive controls reproduce. A strict self-exposure check first caught the congestion lane's rounded TARGET versus the CPS file's full precision; reading its authoritative declaration fixed the mismatch, with the 1e-12 tolerance retained.
- Reproducibility: all three commands exit 0; `rerun_lane.py` **IDENTICAL 16/16**, exit 0. Python-measured 4.035 seconds, peak child RSS 636,059,648 bytes; new producer alone 1.257 seconds and 101,826,560 bytes. No `--allow-unrun` exemption.

## Round-2 corrections — 2026-10-15

The oct15 branch uses the adopted case's native highway key **0.103045731939**, actual personal specifications 16/11 and the amount-weighted state/local and federal highway responses. Capacity cuts change **0.059051 / 0.080610 → 0.075587 / 0.103046** (rounded). The traffic quantities, row-4/5+ normalization, culprit/victim mixing, v7 descendant road factor and recipient boundary are transported from the original source; they are not observed oct15 geography. Completion and coverage resource additions have no separately measured physical road response. The complete oct15 population is used only for the per-member denominator. [CALCULATION: `derived/capacity_model_oct15.json`; `service_response_long_run_2026_09_27/derived/net_change_oct15.json`] [ASSUMPTION]

Central is **multivehicle-only, uniform DOT VSL**. All-density remains beside because it additionally transfers pedestrian/cyclist traffic elasticities to road density. All dollar figures below have the same outside-lineage recipient boundary. [FRAMING-SENSITIVE]

| Mortality basis and capacity arm | Low end, before native key | Low end, after | High end, before | High end, after |
|---|---:|---:|---:|---:|
| Uniform, multivehicle-only | 11.673727 | 11.801388 | 11.841073 | 12.023762 |
| Uniform, all-density | 7.487794 | 6.347376 | 5.992857 | 4.360858 |
| Life years, 0%, multivehicle-only | 11.305474 | 11.367384 | 11.386629 | 11.475224 |
| Life years, 3%, multivehicle-only | 11.221315 | 11.262017 | 11.274670 | 11.332916 |

[CALCULATION: `derived/capacity_items_oct15.csv`; factorial spans are sensitivity ranges, not confidence intervals.]

Life-year arms reprice **gross mortality only** using observed national FARS 2023 victim-class ages and the common NVSS 2024 period table, relative to remaining years at age 40. Multivehicle victims are occupants; single-vehicle external victims are passengers, matching the model's passenger term; nonmotorists are pedestrians and cyclists. Missing age takes the known-age mean within its class, with age-0/100 bounds reported. The conditional age distribution of victims outside the lineage is unmeasured, so national class ages are transported. Common within-age mortality is retained. [DATA: `derived/fars_mortality_2023.json`; `fars_group.py`; `crime_victim_cost_2026_09_23/vsl_standard.py`] [ASSUMPTION]

NHTSA's net quality-of-life amount subtracts market and household productivity from gross QALY loss (Blincoe report, chapter 5, p.92, cached `_cache/blincoe.txt`). Multiplying that net amount would also reprice the subtraction. Instead, each held fatal physical allocation is represented as gross DOT mortality plus a fixed net nonmortality residual. Only gross mortality changes; economic/nonfatal losses, liability flows and that residual stay fixed. Uniform and an age-40 reference identity reproduce the original cells. The original TSF model holds 40,901 deaths; revised cached FARS has 41,025. FARS supplies age proportions only, and does not silently replace the held quantities. [SOURCE: cached Blincoe report] [CALCULATION: `mortality_base()`, `reprice_mortality()`]

`capacity_items_oct15.csv` has 36 unique rows keyed by `valuation`, `real_discount_rate`, `end`, `arm`, `population`. Valuation/rate cells are `dot_uniform/0`, `dot_life_years/0`, `dot_life_years/0.03`; consumers must select an exact cell and cannot fall back to uniform. `before_live_key_central_bn` and `live_key_delta_bn` isolate the key update at each valuation; `mortality_only_delta_bn` compares the same current capacity with uniform. Replace the crash row once. Original outputs remain unchanged. [CALCULATION]

Explicit admission of verified inputs writes `inputs/pins_oct15.json` via `--pin-new-inputs`; default replay fails if those pins are missing or stale. All new outputs are staged after fail-loud source/accounting/physical-budget gates. Physical footprint uses the shared memory-budget definition; RSS is diagnostic only. Reproduce this branch with FARS (cached openpyxl), capacity, and its tests; no historical crash-model regeneration is needed.

Validation — 2026-10-15 02:58:07 JST: **1,070 capacity gates**, three capacity regressions and two congestion regressions pass. Default FARS/capacity/test branch replay is **IDENTICAL 23/23**, exit 0, measured 3.486s. A first replay caught admission omitting two successful pin-gate records; admission and default replay now emit the same receipt. FARS physical footprint 0.829GB; capacity 0.256GB, both below the shared 2.5GB budget. All 23 historical derived files across the road and service lanes match the pre-edit hashes, including every adopted service-response input. No network, historical regeneration, Git writes or tolerance relaxation.

### Round-2 replacement-baseline repair

2026-10-15 03:25:33 JST (`date`): full mortality replacement deltas subtract the original uniform fixed-network baseline, while capacity-only deltas retain the selected valuation baseline. Previously subtraction of an already-repriced baseline canceled the fixed-network mortality repricing. The all-channel lineage multivehicle life-year pairing falls a further0.152778bn at0% or0.167079bn at3%, at both ends; uniform central unchanged. Four regressions,1,070 gates and default branch reproduction IDENTICAL23/23 exit0 pass. Physical footprint0.256GB. The consumer uses exact replacement levels and the original embedded sender amount. [CALCULATION: `test_capacity.py`; scratch `b8-final-road.log`]

Log: 2026-10-15 06:01:26 JST (`date`, parent): rerun on corrected v8 (`d1a24d47`): capacity IDENTICAL 23/23, congestion IDENTICAL 24/24, exit 0. No road key or response moves, so every figure above stands; `inputs/pins_oct15.json` re-pins `service_response_long_run_2026_09_27/derived/net_change_oct15.json`, whose values are unchanged (its recorded source hashes moved).
