# First threshold panel: exploratory associations

**Current assessment — 2026-09-05.** The panel supplies candidate relationships between recent foreign-born exposure, housing measures, receiver status, and election change. It does not demonstrate a causal immigration threshold, a national capacity limit, or a welfare break-even point. The underlying joined panel and estimation scripts were not recovered for replication. [INFERENCE; GAP]

## The county results

The historical specifications report positive election-change interactions for high recent-foreign-born exposure and low permits, including a +0.62-percentage-point estimate with t=2.58. Those are observational conditional associations. They depend on exposure measurement, chosen cutpoints, covariates, and inference. “Recent foreign-born” residence/arrival measures also need their source definition verified before being labeled annual inflows or unauthorized arrivals. [SOURCE: historical panel results; INFERENCE]

A threshold indicator imposes a break in the fitted model; its coefficient does not demonstrate that a physical process has a discontinuity there. The high-exposure permit-bin medians, 5.12, 5.05, 4.25, and 3.79 percentage points of GOP shift, show a reported gradient with a **1.33-point** end-bin contrast. Binning the same observations is not independent validation of the regression and does not control for other differences between bins. Smooth heterogeneity, selected cutpoints, and a causal threshold are distinct hypotheses. [SOURCE: historical table; CALCULATION; INFERENCE]

The comparison of a significant permit interaction with an insignificant rent-burden interaction does not demonstrate that the mechanisms differ. A meaningful coefficient contrast and its uncertainty are required; multiple cutpoints and specifications also affect the interpretation of a selected p-value. Permits over 2021–2024 can respond during the exposure/outcome window and are not automatically a pre-existing supply constraint. HC3 errors and state fixed effects do not remove spatial dependence, endogenous migration, or post-treatment conditioning. [INFERENCE]

## What a receiver snapshot measures

PIT covers sheltered and unsheltered homelessness on one night, while HIC inventories different housing-program categories. Occupancy needs matching program categories, place, and date. [SOURCE: [HUD 2024 AHAR](https://www.huduser.gov/portal/sites/default/files/pdf/2024-AHAR-Part-1.pdf)]

A sheltered-PIT/HIC ratio above one should first trigger reconciliation of beds, program eligibility, overflow/seasonal inventory, and geography; it is not automatically a measured physical capacity threshold. Total PIT divided by shelter beds includes people outside shelter and is not shelter occupancy. Neither measure isolates migrant demand. Housing permits per HIC bed mixes annual construction flow and a service-capacity stock, and ratios sharing HIC can be statistically coupled through that denominator. [INFERENCE]

The memo also mixes some state spending with city/CoC populations. Massachusetts statewide emergency spending cannot be allocated to Boston's shelter population by simple division. A cross-place table can still record different pressures, but comparisons need matched fiscal scope, dates, household/person units, and populations before supporting cost-per-person or capacity calculations. [INFERENCE]

## What remains usable

Reported budget pressures, explicit program caps, and documented shelter use can establish local gross demand on a particular service. They do not alone identify how much migration caused it, whether extra revenue or other benefits offset it, or how capacity evolves. The panel is a hypothesis-generating screen for whether **pre-existing** capacity modifies arrival effects. Its election association does not identify individual voter motives or a causal fiscal-load-to-vote chain. [INFERENCE]

See the [causal-levers correction](immigration-threshold-causal-levers-2026-04-21.md) for the same estimand boundaries. Reusing these rows in another memo does not create another independent test.

## Revisions

- **2026-09-05:** Reclassified the panel as exploratory, corrected significance-versus-difference and threshold reasoning, and required aligned capacity denominators and pre-exposure moderators. [Decision](../decisions/2026-09-05-material-inference-repair.md).

<!-- historical-snapshot:start superseded=2026-09-05 -->
<details>
<summary>Superseded historical analysis — retained verbatim for source and correction provenance</summary>

**Historical text, not the current assessment.** Its earlier verdicts, confidence labels, and source-version claims are superseded by the corrections above. It is retained to preserve quotations and the reasoning that was corrected.

# Immigration threshold first panel: permits, shelter capacity, and backlash

**Question:** After downloading and joining new official datasets, what do the first direct threshold tests show about surge immigration, capacity constraints, and backlash?  
**Tier:** Deep | **Date:** 2026-04-21  
**Method:** Built a new threshold-oriented panel from official `BPS` county annual permits and `HUD AHAR` `HIC/PIT` CoC files, then joined them to the repo's existing county surge/election panel and receiver-city cost data. [SOURCE: sources/immigration-causal/scripts/build_threshold_panel.py] [SOURCE: sources/immigration-causal/scripts/analyze_threshold_effects.py]

## Bottom line

1. **The threshold story survives, but not in the naive form “immigrant share crosses X.”** The better threshold variables are:
   - new arrivals relative to local permit flow
   - sheltered / overall homeless relative to shelter inventory
   - local institutional regime (`right-to-shelter`, receiver-city policy, emergency expansion capacity)

2. **The county cross-section gives a modest pro-threshold signal, not a slam dunk.**
   - In the county regression, `high_recent_fb × low_permit` is about `+0.75 pp` on `2020→2024` GOP margin shift, `t≈1.88`. [SOURCE: sources/immigration-causal/data/threshold/analysis/threshold_results_summary.json]
   - The simpler `receiver_city × low_permit` interaction is negative and not significant in this first pass. [SOURCE: same]

3. **The bin summaries are more intuitive than the coefficient table.**
   - Among counties in the **highest recent-foreign-born quintile**, the median GOP margin shift is about `+5.12 pp` in the **lowest-permit quartile**, versus about `+3.79 pp` in the **highest-permit quartile**. Difference: about `+1.33 pp`. [SOURCE: sources/immigration-causal/data/threshold/analysis/county_threshold_bins.csv]

4. **The receiver-node shelter panel is much cleaner than the county election regression.**
   - `Denver` and `NYC` clearly crossed shelter-capacity ratios above `1.0` by `2024`.
   - `Bexar` also crossed `1.0` on `sheltered / HIC beds` by `2024`.
   - `Boston` and `Chicago` had large local costs without the same clean ratio break, implying that institutional rules and emergency expansion matter, not just physical inventory. [SOURCE: sources/immigration-causal/data/threshold/analysis/receiver_threshold_summary.csv]

5. **So the first joined-data answer is not “no threshold” and not “one universal breakpoint.”**
   It is:
   - real capacity-linked nonlinear pressure in specific receiver nodes
   - modest national evidence that low housing-permit capacity amplifies backlash in high recent-immigration counties
   - large remaining uncertainty because local assignment and HMIS shelter microflows are still not fully observed

## What was newly downloaded

1. `BPS master compiled county/place/state/metro file`
   - `sources/immigration-causal/data/threshold/bps/BPS_Compiled_202601.zip`
   - official source: [SOURCE: https://www2.census.gov/econ/bps/Master%20Data%20Set/BPS%20Compiled_202601.zip]

2. `HUD HIC by CoC`
   - `sources/immigration-causal/data/threshold/hud_ahar/2007-2024-HIC-Counts-by-CoC.xlsx`
   - official source: [SOURCE: https://www.huduser.gov/portal/sites/default/files/xls/2007-2024-HIC-Counts-by-CoC.xlsx]

3. `HUD PIT by CoC`
   - `sources/immigration-causal/data/threshold/hud_ahar/2007-2024-PIT-Counts-by-CoC.xlsb`
   - official source: [SOURCE: https://www.huduser.gov/portal/sites/default/files/xls/2007-2024-PIT-Counts-by-CoC.xlsb]

These were staged with provenance in:
1. `sources/immigration-causal/data/threshold/ACQUIRED.md`

## What was joined

### County panel

The county-level threshold election panel joins:

1. `BPS` annual county permits, latest revision snapshot, `2021–2024`
2. existing `election_surge_county.csv`
3. existing county newcomer/ACS panel

Output:
1. [county_threshold_election_panel.parquet](sources/immigration-causal/data/threshold/analysis/county_threshold_election_panel.parquet)

### Receiver-node panel

The receiver-node panel joins:

1. `HUD HIC` CoC inventory
2. `HUD PIT` CoC homelessness counts
3. annual county permit flow aggregated to hand-mapped receiver nodes
4. existing local receiver-city spending / shelter files

Output:
1. [receiver_threshold_panel.parquet](sources/immigration-causal/data/threshold/analysis/receiver_threshold_panel.parquet)
2. [receiver_threshold_summary.csv](sources/immigration-causal/data/threshold/analysis/receiver_threshold_summary.csv)

## County-level findings

### 1) Low permit capacity amplifies the high-immigration backlash signal

The strongest county result from the first pass is:

1. `high_recent_fb × low_permit` coefficient: about `+0.75 pp`
2. `t ≈ 1.88`

That is not conventionally decisive, but it points in the direction the user expected: when recent immigration is high and local permit capacity is low, the political reaction is worse. [SOURCE: sources/immigration-causal/data/threshold/analysis/threshold_results_summary.json]

### 2) The binned pattern is easier to trust than the single coefficient

Among counties in the top recent-foreign-born quintile:

1. lowest-permit quartile: median GOP margin shift `+5.12 pp`
2. highest-permit quartile: median GOP margin shift `+3.79 pp`

Difference:
1. about `+1.33 pp` more GOP swing in the low-permit places. [SOURCE: sources/immigration-causal/data/threshold/analysis/county_threshold_bins.csv]

That is exactly the kind of “capacity amplifies response” pattern that average-effect immigration papers smooth away.

### 3) The receiver-only interaction is weaker

The `receiver_city × low_permit` coefficient is not useful in this first pass.

Reason:
1. the treated receiver set is small
2. receiver designation is hand-compiled and politically endogenous
3. several receivers have unusual institutions that swamp a simple housing-capacity story

So the broader `high_recent_fb × low_permit` interaction is the more informative county result here. [INFERENCE]

## Receiver-node findings

### 1) Denver is the clearest threshold case

By `2024`:

1. `sheltered / HIC beds ≈ 1.34`
2. `overall homeless / HIC beds ≈ 1.68`
3. local migrant spending about `$89.9M`
4. annual county permit units only about `3,994`

That is an actual capacity-break story, not a generic anti-immigration narrative. [SOURCE: sources/immigration-causal/data/threshold/analysis/receiver_threshold_summary.csv]

### 2) NYC also crosses a real shelter threshold

By `2024`:

1. `sheltered / HIC beds ≈ 1.21`
2. `overall homeless / HIC beds ≈ 1.25`
3. local spending about `$3.7B`
4. peak shelter census about `70,000`, up about `25,000` above baseline

This is the strongest big-city example that the local system can move from absorbable to overloaded. [SOURCE: same]

### 3) Bexar crosses the sheltered-inventory line too

By `2024`:

1. `sheltered / HIC beds ≈ 1.02`
2. `overall homeless / HIC beds ≈ 1.39`

That broadens the threshold story beyond just `NYC` and `Denver`. [SOURCE: same]

### 4) But Boston and Chicago warn against a single mechanical threshold

`Boston` in `2024`:

1. `sheltered / HIC beds ≈ 0.83`
2. spending about `$1.0B`

`Chicago` in `2024`:

1. `sheltered / HIC beds ≈ 0.85`
2. spending about `$228M`

Those places incurred major costs without crossing the same ratio thresholds seen in `Denver` and `NYC`.

That implies:

1. legal obligations
2. emergency-housing rules
3. rapid inventory expansion
4. budget accounting choices

all matter alongside the raw physical capacity ratio. [INFERENCE]

## What changed from the pre-existing repo position?

Before this pass, the repo had:

1. strong housing-elasticity context
2. strong surge-economy and receiver-city cost evidence
3. weak direct measurement of permit-capacity and shelter-inventory thresholds

After this pass, the repo can now say:

1. counties with high recent immigration and weak permit flow show larger political backlash in the first cross-section
2. actual receiver nodes do show shelter-capacity crossings above `1.0` in some cases
3. the threshold is better framed as `new arrivals / capacity stock` than as `foreign-born share`

## What this does **not** settle

1. It does **not** identify a universal breakpoint like `6%` or `10%` foreign-born.
2. It does **not** fully identify causal effects for wages or GDP per capita in receiver counties.
3. It does **not** solve final local assignment of surge migrants.
4. It does **not** replace `HMIS/LSA` for the shelter-system frontier.

## Best current formulation

The best current repo formulation is:

1. **Threshold effects are real, but they are mostly capacity thresholds, not stock-share thresholds.**
2. **Housing-permit scarcity appears to amplify backlash where recent immigration is high.**
3. **Shelter saturation is observable in some receiver nodes, especially `Denver` and `NYC`.**
4. **Institutional rules can make costs large even before raw shelter ratios cross `1.0`.**

## Files produced by this pass

1. [build_threshold_panel.py](sources/immigration-causal/scripts/build_threshold_panel.py)
2. [analyze_threshold_effects.py](sources/immigration-causal/scripts/analyze_threshold_effects.py)
3. [county_bps_permits_2021_2024.parquet](sources/immigration-causal/data/threshold/analysis/county_bps_permits_2021_2024.parquet)
4. [county_threshold_election_panel.parquet](sources/immigration-causal/data/threshold/analysis/county_threshold_election_panel.parquet)
5. [receiver_threshold_panel.parquet](sources/immigration-causal/data/threshold/analysis/receiver_threshold_panel.parquet)
6. [threshold_results_summary.json](sources/immigration-causal/data/threshold/analysis/threshold_results_summary.json)
7. [receiver_threshold_summary.csv](sources/immigration-causal/data/threshold/analysis/receiver_threshold_summary.csv)
8. [county_threshold_bins.csv](sources/immigration-causal/data/threshold/analysis/county_threshold_bins.csv)

</details>
<!-- historical-snapshot:end -->
