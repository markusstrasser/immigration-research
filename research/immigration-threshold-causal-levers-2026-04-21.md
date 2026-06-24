# Immigration threshold causal levers: what actually binds in the joined panel

**Question:** After normalizing the joined threshold panel more aggressively, what look like the real levers and causal channels behind surge-era local stress and backlash?  
**Tier:** Deep | **Date:** 2026-04-21  
**Ground truth:** The first joined-data threshold memo already found that the better threshold variables were capacity-linked, not a simple immigrant-stock breakpoint. This memo tests that claim more directly by comparing alternative county moderators and by normalizing the receiver nodes against shelter inventory and permit flow. [SOURCE: research/immigration-threshold-first-panel-2026-04-21.md]

## Bottom line

1. **The county-side moderator that survives is permit throughput, not generic rent burden.** In the joined county panel, `high_recent_fb × low_permit` is about `+0.62 pp` in the simple interaction model and about `+0.67 pp` in the combined model, both statistically nontrivial, while `high_recent_fb × high_rent_burden` is near zero and not significant. [DATA]
2. **The best threshold variable is still not “foreign-born share.”** Among counties in the top recent-immigration quintile, median GOP margin shift falls almost monotonically from about `+5.12 pp` in the lowest-permit quartile to about `+3.79 pp` in the highest-permit quartile. The rent-burden bins do not show a similar monotone pattern. [DATA]
3. **Receiver-node stress is best understood as `load / capacity stock`, with institutional regime as the main exception handler.** The `2024` saturated nodes are `Denver`, `NYC`, and `Bexar`; they have lower permit-to-capacity ratios on average than the unsaturated nodes, but `Bexar` is an obvious border / assignment-regime exception. [DATA] [INFERENCE]
4. **The real causal story is therefore narrower and more actionable than “immigration increases costs.”** The leading levers are:
   - local permit throughput
   - shelter inventory relative to sheltered load
   - assignment / legal regime (`right-to-shelter`, emergency placement, border-transit management)
   - visibility / concentration of the shock [INFERENCE]

## Claims table

| # | Claim | Evidence | Confidence | Source | Status |
|---|---|---|---|---|---|
| 1 | In high recent-immigration counties, low permit throughput is a stronger backlash moderator than rent burden | HC3 OLS with state FE + log population; `high_recent_fb × low_permit ≈ +0.62 pp` in permit-only model and `≈ +0.67 pp` in joint model; rent-burden interaction is near zero | HIGH | [county_lever_comparison.csv](sources/immigration-causal/data/threshold/analysis/county_lever_comparison.csv) | VERIFIED |
| 2 | Within the highest recent-immigration counties, permit bins show a cleaner threshold shape than rent-burden bins | Top-quintile counties show `5.12 -> 5.05 -> 4.25 -> 3.79 pp` across permit quartiles, while rent-burden bins are non-monotone `4.01 -> 3.12 -> 3.91 -> 5.54 pp` | HIGH | [county_lever_bins.csv](sources/immigration-causal/data/threshold/analysis/county_lever_bins.csv) | VERIFIED |
| 3 | Saturated receiver nodes are generally the low permit-to-capacity nodes, but not all low-capacity stress is physical saturation | `Denver`, `NYC`, and `Bexar` cross `sheltered / HIC > 1` in `2024`; saturated nodes have lower `permit_to_hic` than the unsaturated group on average, but `Boston` and `Chicago` still show high fiscal stress below `1.0` | MEDIUM | [receiver_normalized_2024.csv](sources/immigration-causal/data/threshold/analysis/receiver_normalized_2024.csv) | VERIFIED |
| 4 | Institutional regime is needed to explain the exceptions | `Boston` and `Chicago` spend heavily without crossing the same shelter-saturation ratio as `Denver` or `NYC`, and Denver’s baseline/peak shelter denominator is itself regime-dependent in the local cost file | MEDIUM | [receiver_normalized_2024.csv](sources/immigration-causal/data/threshold/analysis/receiver_normalized_2024.csv), [receiver_city_costs.csv](sources/immigration-causal/data/bused_cities/receiver_city_costs.csv) | INFERENCE |

## Key findings

### 1) Permit throughput beats rent burden as the county-side moderator

The county evidence is clearer after forcing the comparison directly. In the same county panel used for the first threshold memo, I estimated three HC3-robust OLS specifications with state fixed effects and log population. [DATA]

The result:

1. `high_recent_fb × low_permit ≈ +0.62 pp`, `t≈2.58`, `p≈0.0098` in the permit-only interaction model. [DATA]
2. `high_recent_fb × high_rent_burden ≈ +0.04 pp`, `t≈0.19`, `p≈0.85` in the rent-only interaction model. [DATA]
3. In the combined model, the permit interaction remains about `+0.67 pp`, `t≈2.80`, `p≈0.0051`, while the rent interaction stays near zero. [DATA]

That does **not** prove permit scarcity is the whole causal mechanism. It does show that, in this joined county pass, “housing stress” needs to be made more concrete. A throughput proxy beats a price-level proxy. [INFERENCE]

### 2) The threshold shape is visible in permit bins, not in rent-burden bins

Looking only at counties in the highest recent-immigration quintile:

1. lowest permit quartile: median GOP margin shift `+5.12 pp` [DATA]
2. second quartile: `+5.05 pp` [DATA]
3. third quartile: `+4.25 pp` [DATA]
4. highest permit quartile: `+3.79 pp` [DATA]

That is close to the threshold pattern the user expected: once inflow is high, lower local absorption capacity is associated with more backlash. [INFERENCE]

The rent-burden comparison is much less clean:

1. lowest burden: `+4.01 pp` [DATA]
2. second quartile: `+3.12 pp` [DATA]
3. third quartile: `+3.91 pp` [DATA]
4. highest burden: `+5.54 pp` [DATA]

That is not a stable monotone gradient. It looks more like a mixed urbanicity / politics proxy than a clean causal moderator. [INFERENCE]

### 3) Receiver-node stress is best read as `load / capacity stock`

The normalized `2024` receiver table sharpens the shelter story.

The three nodes with `sheltered / HIC > 1` are:

1. `Denver`: `1.34` sheltered / HIC, `1.68` overall / HIC, `permit_to_hic ≈ 0.47` [DATA]
2. `NYC`: `1.21` sheltered / HIC, `1.25` overall / HIC, `permit_to_hic ≈ 0.24` [DATA]
3. `Bexar`: `1.02` sheltered / HIC, `1.39` overall / HIC, `permit_to_hic ≈ 3.42` [DATA]

Across the full `2024` receiver set, the correlation between `sheltered_to_hic_ratio` and `permit_to_hic` is about `-0.38`. Saturated nodes have lower `permit_to_hic` than unsaturated nodes on average, but the sample is small and `Bexar` clearly breaks a pure housing-supply story. [DATA] [INFERENCE]

So the shelter threshold is real, but it is not reducible to one scalar. The dominant pattern is low capacity relative to load, plus at least one institutional / transit exception. [INFERENCE]

### 4) Boston and Chicago show why regime matters

`Boston` and `Chicago` are the most important warning against a naive mechanical threshold story.

In `2024`:

1. `Boston` has `sheltered / HIC ≈ 0.83`, well below `1.0`, but very high documented spending, including about `$1.0B` in the local cost file and about `$133k` per peak shelter census in the normalized table. [DATA]
2. `Chicago` has `sheltered / HIC ≈ 0.85`, also below `1.0`, but still about `$228M` in spending. [DATA]

That means a city or state can incur large costs before raw shelter saturation shows up in the public `HIC/PIT` ratio. The likely mechanisms are legal obligation, hotel-based overflow, assignment practice, procurement cost, and political choice about service level. [INFERENCE]

The Denver rows also force caution. The local cost file codes a `3000` baseline shelter census for `2022`, which makes Denver’s `2024` “peak minus baseline” denominator negative. That does **not** invalidate the saturation signal, but it means the spend-per-extra-shelter normalization is not portable across cities without checking the underlying regime and baseline definition first. [SOURCE: sources/immigration-causal/data/bused_cities/receiver_city_costs.csv] [INFERENCE]

## What survives

1. **Threshold effects are real.** [DATA]
2. **They are better modeled as capacity thresholds than as immigrant-stock thresholds.** [DATA] [INFERENCE]
3. **The cleanest county-side moderator in this public panel is permit throughput.** [DATA]
4. **The cleanest receiver-side variable is shelter load relative to inventory, but legal/assignment regime explains important exceptions.** [DATA] [INFERENCE]

## What does not survive

1. **“Foreign-born share crosses X” as a standalone explanation.** The joined panel still does not support one universal stock-share breakpoint. [DATA] [INFERENCE]
2. **“High rent burden” as the main county-side causal lever.** In this pass it does not do the work that permit throughput does. [DATA]
3. **A single national narrative for all receiver nodes.** `Denver`, `NYC`, `Boston`, `Chicago`, and `Bexar` are not the same treatment. [DATA] [INFERENCE]

## What remains uncertain

1. The county panel still does **not** identify native wage or GDP-per-capita effects directly. That needs `QWI/QCEW/LAUS` extension below the state level. [INFERENCE]
2. The receiver panel is still small and partly hand-mapped. [SOURCE: sources/immigration-causal/data/threshold/receiver_nodes.csv]
3. `HIC/PIT` are annual snapshots, not shelter microflows. `HMIS/LSA` is still the real frontier for saturation measurement. [SOURCE: research/immigration-surge-threshold-dataset-frontier-2026-04-21.md]
4. Some “cost per extra shelter” normalizations are not cross-city comparable without better denominator discipline. Denver is the obvious example. [SOURCE: sources/immigration-causal/data/bused_cities/receiver_city_costs.csv]

## Best current causal formulation

The best current public-data formulation is:

1. **High inflow does not by itself identify the binding constraint.** [INFERENCE]
2. **Where backlash rises, the strongest county-side moderator in this panel is low permit throughput, not rent burden by itself.** [DATA]
3. **Where local systems visibly break, the operative ratio is usually some version of `incoming load / capacity stock`, especially shelter inventory.** [DATA] [INFERENCE]
4. **Where costs are very large without raw physical saturation, institutional regime is the missing variable.** [DATA] [INFERENCE]

## Files produced or updated by this pass

1. [analyze_threshold_effects.py](sources/immigration-causal/scripts/analyze_threshold_effects.py)
2. [county_lever_comparison.csv](sources/immigration-causal/data/threshold/analysis/county_lever_comparison.csv)
3. [county_lever_bins.csv](sources/immigration-causal/data/threshold/analysis/county_lever_bins.csv)
4. [receiver_normalized_2024.csv](sources/immigration-causal/data/threshold/analysis/receiver_normalized_2024.csv)
5. [threshold_results_summary.json](sources/immigration-causal/data/threshold/analysis/threshold_results_summary.json)
