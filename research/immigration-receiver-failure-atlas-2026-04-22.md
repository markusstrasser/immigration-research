# Receiver atlas: measured programs, selected places, and attribution

**Current assessment — 2026-09-05.** The historical atlas records different shelter, spending, and election patterns in selected receiver locations. Its data do not establish a ranking of physical “failures,” identify institutional cost amplification, or show that overload caused voting changes. [INFERENCE]

## Capacity and fiscal comparisons

A sheltered-PIT/HIC ratio above one requires matching program categories, date, geography, and overflow/seasonal inventory before it is interpreted as physical saturation. Total PIT also includes unsheltered people, so total-PIT/shelter-beds is not occupancy. Repeating an unmatched ratio across years does not validate it. The reported Denver 1.34, NYC 1.21, and Bexar 1.02 ratios remain historical screen values pending reconciliation, not proven bed-capacity breaches. [SOURCE: historical atlas; [HUD definitions](https://www.huduser.gov/portal/sites/default/files/pdf/2024-AHAR-Part-1.pdf); INFERENCE]

HIC and shelter counts can themselves respond to the influx and policy; ratios can decline because capacity expanded even while demand or spending rose. Permits per HIC bed mix a housing-unit authorization flow and a service-bed stock. These measures cannot establish a universal immigration threshold or be interpreted as migrant-specific demand without separate population data. [INFERENCE]

The quoted Boston/MA-core spending per resident combines a state-level expenditure with a narrower local population. The **$415 comparison with NYC's $429 is withdrawn as a matched fiscal comparison** until the payer, beneficiaries, geographic denominator, and fiscal period are aligned. City, county, CoC, and state ledgers cannot be interchanged. Gross program outlays also differ from incremental net fiscal effects. [SOURCE: historical cost/scope labels and [surge correction](immigration-causal-surge-2021-2024.md); INFERENCE]

## Causal claims and the score

High spending beside a low shelter ratio does not isolate shelter law, assignment, or procurement as the cause. It can also reflect program scope, added beds, covered populations, prices, or inconsistent geography. A count of heuristic stress flags is a researcher-chosen index; correlated flags are not independent confirmations, and the score does not estimate the magnitude of welfare loss. [INFERENCE]

Election changes in these selected locations are descriptive. A mismatch between shelter ratios and vote swings shows that one scalar does not describe all outcomes; it does not establish which omitted mechanism caused the votes. The later [synthetic comparisons](immigration-receiver-counterfactuals-2026-04-22.md) did not provide decisive ratio-placebo evidence and should not be bypassed by calling the original atlas a causal object. [INFERENCE]

The original atlas joins and yearly files were not recovered for a rerun. Administrative records can support specific gross local pressures after source reconciliation, but this audit does not freshly verify the numeric rankings or infer a national/general receiver failure rate. [GAP]

## Revisions

- **2026-09-05:** Withdrew unmatched saturation/cost rankings and causal regime/voting claims while preserving all historical numbers and case distinctions. [Decision](../decisions/2026-09-05-material-inference-repair.md).

<!-- historical-snapshot:start superseded=2026-09-05 -->
<details>
<summary>Superseded historical analysis — retained verbatim for source and correction provenance</summary>

**Historical text, not the current assessment.** Its earlier verdicts, confidence labels, and source-version claims are superseded by the corrections above. It is retained to preserve quotations and the reasoning that was corrected.

# Immigration receiver failure atlas — 2026-04-22

**Question:** If the county annual panel is only a screening surface, what do the actual receiver nodes look like when we track shelter load, permits, spending, and political shift directly?  
**Tier:** Deep | **Date:** 2026-04-22  
**Ground truth:** The receiver-node panel already staged the cleanest public shelter-capacity series in the repo; this pass turns it into a proper `failure atlas` rather than a one-row 2024 snapshot. [SOURCE: sources/immigration-causal/data/threshold/analysis/receiver_threshold_panel.parquet] [SOURCE: sources/immigration-causal/scripts/analyze_receiver_failure_atlas.py]

## Bottom line

1. `Denver` is still the clearest **physical shelter-saturation** case. It has the highest `2024` sheltered/HIC ratio at about `1.34`, the highest overall/HIC ratio at about `1.68`, and it is the **only** node with shelter saturation in multiple years since `2021`. [SOURCE: sources/immigration-causal/data/outcomes/analysis/receiver_failure_atlas_summary.json]
2. `NYC` is the clearest **total-stress** case. It is saturated in `2024`, has the lowest `permit_to_hic` among the saturated nodes in this public panel, the highest spending per resident at about `$429`, and the highest heuristic stress-flag count. [SOURCE: sources/immigration-causal/data/outcomes/analysis/receiver_failure_atlas_2024.csv] [SOURCE: sources/immigration-causal/data/outcomes/analysis/receiver_failure_atlas_summary.json]
3. `Boston / MA core` is the clearest **high-cost regime** case without physical shelter saturation. It stays below `1.0` on sheltered/HIC, but spending per resident is about `$415`, almost as high as `NYC`. [SOURCE: sources/immigration-causal/data/outcomes/analysis/receiver_failure_atlas_2024.csv]
4. `Bexar`, `Miami-Dade`, and `Harris` show why a simple shelter-ratio story is incomplete. They sit above `1.0` on `overall/HIC` in `2024`, and several of them stay there for multiple years, even when `sheltered/HIC` stays below `1.0`. [SOURCE: sources/immigration-causal/data/outcomes/analysis/receiver_failure_atlas_summary.json]

## New artifacts

1. [analyze_receiver_failure_atlas.py](sources/immigration-causal/scripts/analyze_receiver_failure_atlas.py)
2. [receiver_failure_atlas_2018_2024.csv](sources/immigration-causal/data/outcomes/analysis/receiver_failure_atlas_2018_2024.csv)
3. [receiver_failure_atlas_2024.csv](sources/immigration-causal/data/outcomes/analysis/receiver_failure_atlas_2024.csv)
4. [receiver_failure_atlas_summary.json](sources/immigration-causal/data/outcomes/analysis/receiver_failure_atlas_summary.json)

## Claims table

| # | Claim | Evidence | Confidence | Source | Status |
|---|---|---|---|---|---|
| 1 | Denver is the clearest multi-year physical saturation node | Highest `2024` sheltered/HIC and only node with multi-year shelter saturation since `2021` | HIGH | [receiver_failure_atlas_summary.json](sources/immigration-causal/data/outcomes/analysis/receiver_failure_atlas_summary.json) | VERIFIED |
| 2 | NYC is the heaviest all-around stress node in `2024` | Saturated, low permit-to-capacity, highest spending per resident, highest heuristic stress flags | HIGH | [receiver_failure_atlas_2024.csv](sources/immigration-causal/data/outcomes/analysis/receiver_failure_atlas_2024.csv) | VERIFIED |
| 3 | Boston is a regime-cost case, not a simple shelter-saturation case | High spending with no shelter/HIC saturation | HIGH | [receiver_failure_atlas_2024.csv](sources/immigration-causal/data/outcomes/analysis/receiver_failure_atlas_2024.csv) | VERIFIED |
| 4 | Several border / transit nodes show chronic overall-over-capacity pressure without the same sheltered signature | `Bexar`, `Miami-Dade`, and `Harris` are above `overall/HIC > 1` in `2024`, with multi-year persistence for some | HIGH | [receiver_failure_atlas_summary.json](sources/immigration-causal/data/outcomes/analysis/receiver_failure_atlas_summary.json) | VERIFIED |

## What changed

The earlier receiver summaries were useful but too static. This pass adds:

1. annual node history from `2018–2024`
2. node-level population context
3. permit throughput per resident
4. spending per resident
5. persistence metrics for `sheltered/HIC > 1` and `overall/HIC > 1`
6. vote-shift context at the node level

That turns the receiver panel into a real `failure atlas`, not a one-year descriptive table. [INFERENCE]

## 1) Physical shelter saturation

The clearest `2024` saturation nodes are:

1. `Denver`: `sheltered/HIC ≈ 1.34`, `overall/HIC ≈ 1.68`, `permit_to_hic ≈ 0.47` [SOURCE: sources/immigration-causal/data/outcomes/analysis/receiver_failure_atlas_summary.json]
2. `NYC`: `sheltered/HIC ≈ 1.21`, `overall/HIC ≈ 1.25`, `permit_to_hic ≈ 0.24` [SOURCE: same]
3. `Bexar`: `sheltered/HIC ≈ 1.02`, `overall/HIC ≈ 1.39`, `permit_to_hic ≈ 3.42` [SOURCE: same]

The new persistence metric matters more than the one-year ratio:

1. `Denver` is the only node with shelter saturation in multiple years since `2021`. [SOURCE: same]
2. `Bexar`, `Miami-Dade`, and `Harris` stay above `overall/HIC > 1` for multiple years even when the sheltered ratio does not stay above `1.0`. [SOURCE: same]

That supports a more precise statement:

1. `Denver` looks like chronic shelter saturation.
2. `NYC` looks like extreme fiscal and political stress with real shelter saturation.
3. `Bexar` and some other transit-heavy nodes look more like broad homelessness / overflow pressure than a pure sheltered-bed story.

## 2) Fiscal stress does not map one-for-one onto physical saturation

The `2024` spending-per-resident ranking is:

1. `NYC`: about `$429`
2. `Boston / MA core`: about `$415`
3. `Denver`: about `$126`
4. `Chicago`: about `$44`
5. `DC`: about `$60`

`Boston` is the key case here. It never crosses `sheltered/HIC > 1`, but it still shows very large spending. [SOURCE: sources/immigration-causal/data/outcomes/analysis/receiver_failure_atlas_2024.csv]

That is strong evidence that:

1. `physical shelter saturation` is not the only relevant threshold
2. `legal regime`, `assignment obligations`, and `procurement structure` are first-order channels too

This was already suspected in the earlier memos; the new atlas makes it harder to ignore. [INFERENCE]

## 3) Politics tracks stress, but not in one clean pattern

The largest node-level `2020→2024` weighted GOP shifts are:

1. `El Paso`: about `+10.3 pp`
2. `Miami-Dade`: about `+9.3 pp`
3. `NYC`: about `+7.8 pp`

This does **not** line up perfectly with shelter saturation alone. [SOURCE: sources/immigration-causal/data/outcomes/analysis/receiver_failure_atlas_summary.json]

So the right political read is:

1. overload matters
2. but so do broader border/travel corridor dynamics and Hispanic realignment

The atlas is useful here because it makes the mismatch explicit instead of hiding it inside one regression. [INFERENCE]

## What now survives

1. receiver-node analysis is a better object than another county threshold sweep [INFERENCE]
2. `Denver` and `NYC` are real saturation cases, not rhetorical examples [SOURCE: sources/immigration-causal/data/outcomes/analysis/receiver_failure_atlas_summary.json]
3. `Boston` is a real cost case even below physical saturation [SOURCE: sources/immigration-causal/data/outcomes/analysis/receiver_failure_atlas_2024.csv]
4. the local-incidence story is multi-channel: `shelter`, `overall homeless load`, `fiscal regime`, and `politics` do not collapse into one scalar threshold [INFERENCE]

## Best current formulation

The receiver frontier is now:

1. `physical saturation`
2. `duration above capacity`
3. `regime-cost amplification`
4. `political response`

That is already a cleaner causal object than the annual county wage panel. [INFERENCE]

</details>
<!-- historical-snapshot:end -->
