# Immigration capacity frontier: stock, flow, load, and what still remains

**Question:** After extending the county panel again, what is the cleanest current answer on thresholds, counterfactual levers, subgroup needs, voting, and welfare?  
**Tier:** Deep | **Date:** 2026-04-21  
**Ground truth:** The prior county and threshold passes suggested that `permit throughput` and `rent burden` were more informative than generic immigrant-share rhetoric, but they still leaned on one or two threshold constructions. This memo compares `stock`, `flow`, and `flow-to-build-capacity` directly and checks whether the threshold survives outside a single arbitrary split. [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md] [SOURCE: research/immigration-threshold-causal-levers-2026-04-21.md]

## Bottom line

1. The repo's strongest current one-predictor county model signal for `political response` remains `immigrant stock share`, but `flow-to-build-capacity` still adds residual signal once stock and flow are both included. [DATA]
2. For `wage growth`, `employment growth`, and `native net migration`, `recent immigrant flow relative to local permit capacity` is the more relevant descriptive stress proxy than stock share alone. For wages, the adjusted-`R²` edge is small and should not be treated as a settled ranking. [DATA] [INFERENCE]
3. A recurring threshold pattern is visible, but it is not best described as `foreign-born share crosses X`. It looks more like a `high-flow tail x weak build response` pattern. The interaction appears around the `70th-80th` flow percentiles with `bottom-half or bottom-quartile` permit capacity, but q90 comparisons may be power-limited and the grid is not multiplicity-adjusted. [DATA] [INFERENCE]
4. This tightens the current repo view:
   - `politics`: stock + load both matter
   - `wages`: load/capacity is marginally best-fitting in this one-predictor pass
   - `employment`: still not a generic collapse story, but a negative signal does appear under direct load-capacity formulations
   - `native sorting`: load/capacity and affordability both matter descriptively; whether this is native exit caused by capacity strain still needs counterfactual identification [INFERENCE]
5. The remaining frontier is now clearer:
   - `subgroup composition` needs the missing origin warehouse or new acquisition
   - `voting` needs a native-turnout / precinct or survey design, not county returns alone
   - `welfare` needs state/local service and federal-transfer linkage, not just macro aggregates
   - `receiver-city counterfactuals` still need synthetic controls [INFERENCE]

## New artifacts

1. [analyze_capacity_frontier.py](/Users/alien/Projects/research/sources/immigration-causal/scripts/analyze_capacity_frontier.py)
2. [county_capacity_frontier_summary.json](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_capacity_frontier_summary.json)
3. [county_capacity_model_comparison.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_capacity_model_comparison.csv)
4. [county_capacity_threshold_grid.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_grid.csv)
5. [county_load_capacity_deciles.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_load_capacity_deciles.csv)
6. [receiver_capacity_descriptives_2024.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/receiver_capacity_descriptives_2024.csv)

## Measurement frame

The new derived variable is:

`recent immigrant load per permit unit = annual recent immigrant persons / annual permit units`

using:

1. `annual recent immigrant persons = recent_fb_annual_share * total population` [DATA]
2. `annual permit units = permit_units_2021_2024 / 4` [DATA]
3. a heuristic `2.5 persons per housing unit` when translating units into rough people-capacity [INFERENCE]

This is not a full housing-market model. It is a tractable public-data proxy for:

`flow / local build capacity`

That is the more relevant descriptive object if the threshold story is about absorption rather than stock. But permit units also proxy local economic vitality, so a load ratio can pick up weak local growth mechanically; a stronger design should show load adds signal beyond permit level itself. [INFERENCE]

## Claims table

| # | Claim | Evidence | Confidence | Source | Status |
|---|---|---|---|---|---|
| 1 | Stock share has the highest adjusted `R²` among one-predictor county margin models | In separate one-predictor county models, standardized `fb_share` has larger `t` and higher adjusted `R²` than flow or load | HIGH | [county_capacity_model_comparison.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_capacity_model_comparison.csv) | VERIFIED DESCRIPTIVE MODEL OUTPUT |
| 2 | Load-capacity still adds residual political-response signal beyond stock and flow | In the combined margin model, standardized load remains positive and significant (`t≈2.74`, `p≈0.006`) | HIGH | [county_capacity_model_comparison.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_capacity_model_comparison.csv) | VERIFIED |
| 3 | Wage-growth models are marginally best-fitting under load-capacity in this one-predictor pass | Load-only wage model has the strongest negative `t` and best adjusted `R²`, but the adjusted-`R²` spread versus stock/flow is only about 0.007-0.010 | MEDIUM | same | VERIFIED DESCRIPTIVE MODEL OUTPUT — RANKING THIN |
| 4 | A negative employment signal appears under direct load-capacity formulations even though the earlier coarse threshold did not show broad job loss | Load-only and combined employment models are negative and highly significant; stock and flow alone are weak or null | HIGH | same | VERIFIED |
| 5 | The threshold screen appears in the broad high-flow tail (`70th-80th percentile`) interacted with low permit capacity | Interaction grid shows stronger wage and some politics/employment effects at `q70-q80` than at `q90`, but q90 power and multiple-testing concerns remain | MEDIUM | [county_capacity_threshold_grid.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_grid.csv) | VERIFIED DESCRIPTIVE SCREEN |
| 6 | Native net migration is more negative in higher load-capacity deciles | Load deciles show about `-1.07 pp` gap from `D1` to `D10`; load-based models outperform stock-only on adjusted `R²` | HIGH | [county_load_capacity_deciles.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_load_capacity_deciles.csv), [county_capacity_model_comparison.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_capacity_model_comparison.csv) | VERIFIED |
| 7 | Receiver-city spending is more tightly tied to absolute shelter shortfall than to saturation ratio alone | In 2024 receiver descriptives, `corr(shelter_gap_vs_hic, spending) ≈ 0.93`, much larger than `corr(sheltered_to_hic_ratio, spending)` | MEDIUM | [receiver_capacity_descriptives_2024.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/receiver_capacity_descriptives_2024.csv) | VERIFIED |

**Scope note:** In this table, `HIGH` and `VERIFIED` mean the reported model-output pattern is file-backed and reproducible from the listed artifacts. They do not mean the county associations are clean causal effects; the causal caveats below still apply. [INFERENCE]

## What changed from the prior position?

The prior county memo said:

1. `permit throughput` was the wage-side bottleneck [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md]
2. `rent burden` was the stronger native-sorting signal [SOURCE]
3. there was no clear broad county `employment-collapse` signal under the `high_recent_fb x low_permit` specification [SOURCE]

That still mostly survives, but the more direct `flow / build-capacity` formulation sharpens it:

1. `permit throughput` was the right direction
2. the more precise object is `immigrant flow relative to annual permit capacity`
3. under that object, `employment` no longer looks fully null

So the update is not `the old memo was wrong`. It is:

1. the earlier threshold split was too coarse
2. the direct load-capacity ratio finds additional strain that the binary split missed

## Model comparison: what actually predicts what?

### 1) Politics: stock is still strongest, but load is not fake

For `margin_shift`, the simple one-predictor ranking is:

1. `stock_only`: `beta≈+0.0150`, `t≈12.08`, `adj_R²≈0.415` [DATA]
2. `flow_only`: `beta≈+0.0099`, `t≈9.32`, `adj_R²≈0.369` [DATA]
3. `load_only`: `beta≈+0.0054`, `t≈6.96`, `adj_R²≈0.345` [DATA]

So the stock variable still carries the most countywide political signal. That matters because it means the political-response story is **not** reducible to a pure recent-surge story. Established immigrant concentration, long-run demographic sorting, and Hispanic realignment are still in the political mix. [INFERENCE]

But the combined model matters too:

1. `load` remains positive and significant with `t≈2.74`, `p≈0.006` after including both stock and flow [DATA]

So the stronger claim is:

1. `stock` carries the broad political-map signal in this county model
2. `load / capacity` still adds residual strain in that map

### 2) Wages: load-capacity is marginally best-fitting in this pass

For `weekly wage growth`:

1. `stock_only`: `t≈-3.97`, `adj_R²≈0.147` [DATA]
2. `flow_only`: `t≈-3.75`, `adj_R²≈0.144` [DATA]
3. `load_only`: `t≈-4.08`, `adj_R²≈0.154` [DATA]

And in the combined model:

1. `load` stays negative with `t≈-2.49`, `p≈0.013` [DATA]

This is the strongest county-level associative signal in this panel that the `worker` question may be tied to:

`inflow under weak absorption capacity`

not just `immigrant stock exists`. [INFERENCE]

### 3) Employment: still not collapse rhetoric, but no longer cleanly null

This is the most important revision.

Under the old `high_recent_fb x low_permit` interaction, employment was basically null. [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md]

Under the direct load-capacity metric:

1. `stock_only`: weak, `p≈0.17` [DATA]
2. `flow_only`: weak, `p≈0.079` [DATA]
3. `load_only`: `beta≈-0.0087`, `t≈-7.10`, `adj_R²≈0.117` [DATA]
4. `combined`: `beta≈-0.0123`, `t≈-8.83`, `adj_R²≈0.129` [DATA]
5. `high_load90`: `beta≈-0.0106`, `p≈0.013` [DATA]

Basic robustness checks keep the sign:

1. using a `95th` rather than `99th` percentile winsorization leaves the employment result strongly negative [DATA: `county_capacity_frontier_summary.json`]
2. excluding receiver and border counties still leaves a negative load effect with `t≈-4.79` [DATA]

That does **not** justify `immigration causes county employment collapse`.

It does justify this narrower update:

1. `high immigrant load relative to local build capacity` is associated with slower employment growth as well as slower wage growth

### 4) Native sorting: load-capacity beats stock-only

For `net U.S. migration share`, all three predictors are strongly negative, but `load_only` has the best single-predictor adjusted `R²`, and the combined model improves further. [DATA]

The decile table is intuitive:

1. `D1` median net domestic migration share: about `+0.82 pp` [DATA]
2. `D10` median net domestic migration share: about `-0.24 pp` [DATA]
3. gap: about `-1.07 pp` [DATA]

This is a more directly relevant descriptive screen for the destination-country question than global-output arguments:

1. counties where immigrant inflow materially outruns local build response show more negative domestic net migration; whether incumbents sort away because of that load still needs counterfactual identification

## Threshold effects: where do they actually show up?

The threshold grid matters because it checks whether the story is just one arbitrary `80th percentile x median permit` construction.

### What survives

The clearest and most repeatable interaction is:

1. `high flow x low permit` hurts `wage growth`

Examples:

1. `q70 flow x q25 permit`: wage `beta≈-0.0160`, `p≈0.011` [DATA]
2. `q80 flow x q25 permit`: wage `beta≈-0.0203`, `p≈0.025` [DATA]
3. `q80 flow x q50 permit`: wage `beta≈-0.0151`, `p≈0.0015` [DATA]

Politics also shows up in the broad high-flow tail:

1. `q70 flow x q50 permit`: margin shift `beta≈+0.62 pp`, `p≈0.040` [DATA]
2. `q80 flow x q50 permit`: margin shift `beta≈+0.85 pp`, `p≈0.029` [DATA]

Employment appears in some of the same bands:

1. `q70 flow x q25 permit`: employment `beta≈-1.86 pp`, `p≈0.0045` [DATA]
2. `q80 flow x q25 permit`: employment `beta≈-1.82 pp`, `p≈0.019` [DATA]

### What weakens

The `q90` extreme-flow interactions are weaker and less stable for politics and wages, but that may partly reflect lower tail power rather than a weaker underlying effect. [DATA] [INFERENCE]

That suggests, but does not prove, the observed threshold pattern is **not**:

1. `only the absolute top-decile explodes`

It looks more like:

1. `once a county enters the broad high-flow tail and also has weak building response, strain becomes visible`

That is a better descriptive threshold story. Causal interpretation still needs a design that separates inflow, housing response, and destination selection. [INFERENCE]

## Decile read: how large is the gap?

From the load-capacity deciles:

1. `D1` median flow-per-permit-unit: about `0.04`
2. `D10` median flow-per-permit-unit: about `3.56`

Associated median changes:

1. `margin shift`: `+3.12 pp` -> `+4.90 pp` (`+1.78 pp` gap) [DATA]
2. `weekly wage growth`: `13.56 pp` -> `11.99 pp` (`-1.56 pp` gap) [DATA]
3. `employment growth`: `6.07 pp` -> `4.50 pp` (`-1.56 pp` gap) [DATA]
4. `native net migration share`: `+0.82 pp` -> `-0.24 pp` (`-1.07 pp` gap) [DATA]

That is the cleanest single descriptive picture in the new pass.

## Receiver nodes: what matters most in the crisis cases?

The receiver-node panel remains small-N, so it is descriptive rather than causal.

Still, two points survive:

1. the saturated `2024` nodes remain `Denver`, `New York City`, and `Bexar` [DATA]
2. spending aligns much more with `absolute shelter shortfall` than with simple saturation ratio:
   - `corr(shelter_gap_vs_hic, spending) ≈ 0.93`
   - `corr(sheltered_to_hic_ratio, spending) ≈ 0.32` [DATA]

This matters because it means the receiver-city crisis is not only about crossing `ratio > 1`. It is also about:

1. how large the absolute shortfall is
2. what legal and assignment regime turns that shortfall into fiscal outlay [INFERENCE]

One caution remains:

1. Denver's `peak_minus_baseline_shelter` denominator is still distorted by the baseline issue already noted in the threshold memo, so cost-per-extra-shelter normalization should still be handled carefully. [SOURCE: research/immigration-threshold-causal-levers-2026-04-21.md]

## What this updates, and what it does not settle

### What now looks stable enough for the repo

1. `Foreign-born share` alone is not the right master threshold variable. [DATA]
2. `Flow x capacity` is a useful descriptive county stress object for wages, employment, and native sorting, but the wage ranking is thin and the permit denominator may proxy local economic vitality. [DATA] [INFERENCE]
3. `Politics` still loads heavily on stock, but capacity strain adds model residual signal. [DATA]
4. The relevant threshold is broad high-flow exposure under weak building response, not only an extreme top-decile event. [DATA]

### What is still open

1. **Counterfactual receiver-city paths**
   We still need synthetic controls or better event-study controls for `NYC`, `Chicago`, `Denver`, `Boston`, `Bexar`. [INFERENCE]

2. **Subgroup composition**
   The origin warehouse cited by earlier memos is not actually present in the current local repo state, so a real `subgroup / ethnic / pathway / family-structure` extension is not valid to rerun right now without reacquiring or rebuilding that layer. [DATA: missing local artifact]

3. **Voting**
   County returns do not identify whether the effect is native turnout, persuasion, composition change, or precinct-level backlash. The current county evidence is about `political response`, not immigrant voting behavior. [INFERENCE]

4. **Welfare**
   We still do not have a joined micro-to-local service ledger that cleanly separates:
   - federal taxes/transfers
   - state/local education
   - shelter/emergency services
   - Medicaid/uncompensated care
   - pathway and family composition [INFERENCE]

## Best current synthesis

The repo's current best answer is now:

1. `Global gains` are still possible at bounded margins, but destination-country incidence depends heavily on capacity. [SOURCE: research/immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md]
2. `County stress` is best understood as `flow relative to build capacity`, not as immigrant share in the abstract. [DATA]
3. `Stock` still matters politically, so the political-response story is not just about the recent surge. [DATA]
4. `High load / low capacity` is where wage growth, employment growth, domestic net migration, and political-response metrics move in the adverse direction together. [DATA]

That is a stricter and more useful answer than either:

1. `immigration is good because GDP`
2. `immigration is bad because stock share rose`

The better formula is:

`incidence = stock + flow + capacity + composition + regime`

and in the current public-data stack, `flow + capacity` is where the new descriptive traction is coming from. Causal identification still needs stronger counterfactual design. [INFERENCE]

## Revisions

| Date | Change |
|------|--------|
| 2026-06-16 | Replaced the remaining "stock drives the broad political map" shortcut with descriptive model-signal language. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Replaced residual "established"/"settles" wording with suggested/updates language; county capacity models remain descriptive model-output evidence, not settled causal identification. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Added a claims-table scope note: `HIGH`/`VERIFIED` refer to reproducible model-output patterns, not causal identification. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Reframed the native-sorting sentence as a descriptive association rather than a causal incumbent-exit claim. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Removed residual causal verbs from the claims table and wage section: the load-capacity rows are verified descriptive model-output patterns, not causal response estimates. See `immigration-conclusion-audit-running-fixes.md`. |
