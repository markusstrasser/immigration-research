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
