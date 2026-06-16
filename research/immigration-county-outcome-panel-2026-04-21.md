# Immigration county outcome panel: labor, domestic migration, and backlash

Supersession note: this memo is an earlier county-outcome pass. For the current stance, read [immigration-capacity-falsification-2026-04-21.md](/Users/alien/Projects/research/research/immigration-capacity-falsification-2026-04-21.md), which extends QCEW back to `2017`, adds explicit window metadata, and downgrades the causal confidence of the wage/employment story.

**Question:** After joining official county QCEW annual outcomes to the threshold panel, what actually moves in high-immigration, low-capacity counties: employment, wages, IRS domestic migration, politics, or some narrower combination?  
**Tier:** Deep | **Date:** 2026-04-21  
**Ground truth:** The prior threshold pass showed that capacity variables mattered more than immigrant-stock variables, but it still did not directly price county labor outcomes. This memo adds county labor outcomes and an IRS domestic net-migration layer to the same county spine. That IRS layer is `Total Migration-US`, not a native-incumbent-only measure. [SOURCE: research/immigration-threshold-causal-levers-2026-04-21.md] [SOURCE: sources/immigration-causal/data/internal_migration/county_inflow_2022_23.csv]

## Bottom line

1. **The first county-outcome pass looked more like a wage-growth story than an employment-collapse story.** In counties with very high recent immigration and low permit throughput, countywide weekly wage growth from `2021` to `2024` is about `1.5 pp` lower, while employment growth is not significantly lower in this first reduced-form pass. [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_summary.json] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_lever_comparison.csv]
2. **Backlash and labor do not load on exactly the same moderator in this first pass.** In the top recent-immigration counties, both `low permit` and `high rent burden` predict more GOP shift, but the wage-growth penalty attaches to `low permit`, while IRS domestic net out-migration attaches more to `high rent burden`. [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_lever_comparison.csv]
3. **That is a better causal decomposition than “immigration hurts the local economy.”** The data now point to:
   - `permit throughput / housing-supply response` as the wage and backlash moderator
   - `rent burden / affordability` as the domestic-migration / sorting moderator
   - `shelter and legal regime` as the receiver-city crisis amplifier
   - no strong evidence here of a broad county employment collapse [INFERENCE]

## Claims table

| # | Claim | Evidence | Confidence | Source | Status |
|---|---|---|---|---|---|
| 1 | High recent-immigration counties with low permit throughput show slower county wage growth | HC3 OLS: `high_recent_fb × low_permit ≈ -1.49 pp` on `2021–2024` QCEW weekly wage log growth, `t≈-3.15`, `p≈0.0017`; result survives with rent burden added | HIGH | [county_outcome_summary.json](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_outcome_summary.json), [county_outcome_lever_comparison.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_outcome_lever_comparison.csv) | VERIFIED |
| 2 | The same interaction does not produce a clear county employment-growth penalty | HC3 OLS: `high_recent_fb × low_permit ≈ -0.33 pp`, `t≈-0.67`, `p≈0.50` on QCEW employment log growth | HIGH | [county_outcome_summary.json](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_outcome_summary.json) | VERIFIED |
| 3 | In top recent-immigration counties, wage and employment medians improve as permit capacity rises | Q5 surge counties: median employment growth `2.72 -> 5.04 -> 6.15 -> 8.55 pp`; median weekly wage growth `11.00 -> 10.75 -> 11.45 -> 13.13 pp` across permit quartiles | HIGH | [county_outcome_bins.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_outcome_bins.csv) | VERIFIED |
| 4 | IRS domestic net migration responds more to rent burden than to low permit throughput in high-immigration counties | HC3 OLS: `high_recent_fb × high_rent_burden ≈ -0.21 pp`, `t≈-2.85`, `p≈0.0044`; `high_recent_fb × low_permit` is near zero | MEDIUM | [county_outcome_lever_comparison.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_outcome_lever_comparison.csv), [county_inflow_2022_23.csv](/Users/alien/Projects/research/sources/immigration-causal/data/internal_migration/county_inflow_2022_23.csv), [county_outflow_2022_23.csv](/Users/alien/Projects/research/sources/immigration-causal/data/internal_migration/county_outflow_2022_23.csv) | VERIFIED |
| 5 | County political backlash in the high-immigration tail responds to both permit scarcity and rent burden | In this outcome-panel sample, `high_recent_fb × low_permit ≈ +0.75 pp`, `p≈0.064`; `high_recent_fb × high_rent_burden ≈ +0.75 pp`, `p≈0.038` | MEDIUM | [county_outcome_lever_comparison.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_outcome_lever_comparison.csv) | VERIFIED |

## What was joined

This pass built a common county panel from:

1. the existing threshold county spine with elections, permits, recent foreign-born share, and newcomer controls [SOURCE: [county_threshold_election_panel.parquet](/Users/alien/Projects/research/sources/immigration-causal/data/threshold/analysis/county_threshold_election_panel.parquet)]
2. official BLS QCEW annual county totals for `2021–2024` [SOURCE: https://www.bls.gov/cew/downloadable-data-files.htm] [SOURCE: [ACQUIRED.md](/Users/alien/Projects/research/sources/immigration-causal/data/qcew/ACQUIRED.md)]
3. cleaned IRS SOI county inflow and outflow aggregates for domestic migration (`97/000` total-US rows) [SOURCE: [county_inflow_2022_23.csv](/Users/alien/Projects/research/sources/immigration-causal/data/internal_migration/county_inflow_2022_23.csv)] [SOURCE: [county_outflow_2022_23.csv](/Users/alien/Projects/research/sources/immigration-causal/data/internal_migration/county_outflow_2022_23.csv)]

Produced artifacts:

1. [build_county_outcome_panel.py](/Users/alien/Projects/research/sources/immigration-causal/scripts/build_county_outcome_panel.py)
2. [analyze_county_outcome_panel.py](/Users/alien/Projects/research/sources/immigration-causal/scripts/analyze_county_outcome_panel.py)
3. [county_qcew_2017_2024.parquet](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/county_qcew_2017_2024.parquet)
4. [county_outcome_panel.parquet](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/county_outcome_panel.parquet)
5. [county_outcome_summary.json](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_outcome_summary.json)
6. [county_outcome_bins.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_outcome_bins.csv)
7. [county_outcome_lever_comparison.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_outcome_lever_comparison.csv)

## Key findings

### 1) The labor-market damage channel is slower wage growth, not broad county job loss

Using HC3-robust county regressions with state fixed effects, the main new labor result is:

1. `high_recent_fb × low_permit ≈ -1.49 pp` on QCEW weekly wage log growth from `2021` to `2024`, `t≈-3.15`, `p≈0.0017` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_summary.json]
2. the same interaction on QCEW employment log growth is only about `-0.33 pp`, `t≈-0.67`, `p≈0.50` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_summary.json]

So the county economy in those places does not look like it is mechanically shedding jobs. It looks more like labor absorption under capacity strain is happening through slower wage growth. [INFERENCE]

That is a materially sharper claim than the repo could make before this pass.

### 2) Permit throughput matters for wages; rent burden does not

The wage result is not just “bad urban counties.”

1. `high_recent_fb × low_permit ≈ -1.49 pp` in the permit-only wage model [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_lever_comparison.csv]
2. `high_recent_fb × high_rent_burden ≈ +0.32 pp`, `t≈0.75`, `p≈0.45` in the rent-only wage model [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_lever_comparison.csv]
3. in the combined wage model, the permit interaction remains about `-1.44 pp`, `t≈-3.01`, `p≈0.0026`, while the rent interaction stays small and not significant [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_lever_comparison.csv]

So the county wage-growth penalty is a `capacity-to-add-supply` result, not a generic “expensive places are worse” result. [INFERENCE]

### 3) The top recent-immigration counties sort cleanly by permit capacity

Within the highest recent-immigration quintile:

1. median employment growth rises from about `2.72 pp` in the lowest-permit quartile to about `8.55 pp` in the highest-permit quartile [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_bins.csv]
2. median weekly wage growth rises from about `11.00 pp` to about `13.13 pp` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_bins.csv]
3. median GOP margin shift falls from about `+5.12 pp` to about `+3.79 pp` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_bins.csv]

That is a coherent county story:

1. low-capacity counties see more backlash
2. they do not obviously lose jobs
3. but they do show slower wage progression [INFERENCE]

### 4) IRS domestic migration reacts more to rent burden than to permit scarcity

The IRS domestic net-migration outcome tells a different story.

1. `high_recent_fb × low_permit` is near zero on IRS domestic net migration share, `p≈0.69` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_lever_comparison.csv]
2. `high_recent_fb × high_rent_burden ≈ -0.21 pp`, `t≈-2.85`, `p≈0.0044` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_lever_comparison.csv]

So IRS-measured domestic migration appears to respond more to direct affordability pressure than to permit scarcity alone. That is suggestive for sorting, but it is not a native-incumbent-only result. [INFERENCE]
This is why `rent burden` still matters, even though it is not the best wage moderator.

### 5) Politics responds to both scarcity and affordability

In this broader outcome-panel sample, the backlash result is more mixed than in the earlier threshold-only memo:

1. `high_recent_fb × low_permit ≈ +0.75 pp`, `p≈0.064` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_lever_comparison.csv]
2. `high_recent_fb × high_rent_burden ≈ +0.75 pp`, `p≈0.038` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_lever_comparison.csv]

That is a plausible refinement rather than a contradiction.

The earlier pass asked which moderator best explained backlash on a narrower threshold frame and found permit throughput cleaner. This pass says that once you look at the high-immigration tail alongside labor and mobility outcomes, politics responds to both:

1. inability to add supply
2. direct cost pressure felt by residents [INFERENCE]

## What changed from the prior position?

Before this pass, the repo could say:

1. capacity thresholds are real
2. shelter saturation is real
3. backlash is worse in constrained places
4. labor conclusions at the county threshold level were still mostly missing

Now it can also say:

1. the first broad county labor response is slower wage growth, not strong job loss [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_summary.json]
2. permit throughput is the wage-side moderator in this first pass [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_lever_comparison.csv]
3. rent burden is the cleaner IRS domestic-migration moderator [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_lever_comparison.csv]
4. politics sits on top of both channels [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_lever_comparison.csv] [INFERENCE]

## Best current causal formulation

The best public-data formulation is now:

1. **`low permit throughput` is the main county wage-growth bottleneck under high recent immigration in this first pass.** [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_lever_comparison.csv]
2. **`high rent burden` is the stronger IRS domestic-migration signal.** [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_lever_comparison.csv]
3. **`political backlash` responds to both scarcity and affordability.** [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_lever_comparison.csv]
4. **`employment collapse` is not the clean county-level story in this panel.** [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_outcome_summary.json]
5. **receiver-city crisis severity still depends on shelter stock and institutional regime, which the county panel cannot replace.** [SOURCE: research/immigration-threshold-causal-levers-2026-04-21.md]

## What remains uncertain

1. QCEW is county-total employment and wages, not native-only outcomes. It is a strong local labor barometer, not a native-incidence estimator. [INFERENCE]
2. QCEW weekly wages are nominal. In low-permit counties with faster shelter-cost pressure, the nominal wage penalty likely understates any real wage penalty. [INFERENCE]
3. IRS SOI migration is filer-based, not a full resident microflow. [INFERENCE]
4. This is still reduced-form county evidence, not a structural model with endogenous housing supply, relocation, and sector composition. [INFERENCE]
5. The shelter/legal-regime story still needs the receiver-node panel and ideally `HMIS/LSA` for a fuller local-capacity account. [SOURCE: research/immigration-surge-threshold-dataset-frontier-2026-04-21.md]
