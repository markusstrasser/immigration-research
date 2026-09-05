# Receiver synthetic comparisons: divergence without identified overload

**Current assessment — 2026-09-05.** The reported synthetic comparisons are useful diagnostics of how selected shelter outcomes differ across places. They do not establish Denver as a causally identified physical-overload “survivor,” Chicago as a proven capacity failure, or Boston as an institution-caused high-cost case. The weak ratio-placebo results and unresolved denominator/support problems remain binding. [INFERENCE]

## What was compared

The historical design fits 2018–2021 CoC outcome paths, treats 2022 as the common intervention start, excludes selected recipient/border hubs, and compares ratios and log counts through 2024. Actual arrival timing can differ by city; treatment, donor spillovers, COVID-era reporting, and CoC boundary/program consistency need checking. A common calendar cutoff is not random assignment. The original panel, donor weights, and fitting code were not recovered here. [SOURCE: historical design; GAP; INFERENCE]

The reported Chicago log gaps of 1.380 for sheltered counts and 1.062 for total homelessness exponentiate to **3.97× and 2.89×**, respectively. That arithmetic is correct **relative to the fitted log-scale comparator**. If weights are applied to donor log counts, exponentiation gives a weighted geometric comparator, not the arithmetic weighted count. Neither ratio is automatically a causal increase from immigration. [SOURCE: historical results; DERIVATION]

A post-period level gap must be assessed against pre-period fit and common support. NYC's reported 2.957 log-point gap is roughly 19.24× the fitted level, making size and pre-fit diagnostics essential before calling it new divergence. A concentrated Seattle donor weight is a sensitivity issue, not by itself proof of invalidity; equally, its sign cannot validate a counterfactual that fails to match the prior level/path. [SOURCE: historical NYC weights/gaps; DERIVATION; INFERENCE]

## Ratios, counts, and inference

Shelter use and inventory can both respond to arrivals and policy. More sheltered people with a muted ratio can reflect added capacity, changes in who is counted, or other forces; it does not show that capacity “failed to keep absolute load down.” Absolute homelessness is an outcome, not a direct excess-demand measure. HUD's sheltered/unsheltered populations and shelter versus permanent-housing program inventories must be aligned. [SOURCE: [HUD 2024 AHAR](https://www.huduser.gov/portal/sites/default/files/pdf/2024-AHAR-Part-1.pdf); INFERENCE]

The reported filtered ratio-placebo p-values are high (for example Denver about 0.71 and 0.89). They do not show unusually large treatment statistics under that comparison scheme. They also do not prove no effect or equivalence. The absolute-count outcomes did not receive the same placebo procedure; their visible gaps cannot borrow inferential support from a different outcome. [SOURCE: historical placebo section; INFERENCE]

## What remains

The original comparisons challenge a universal shelter-saturation story: the cases differ across ratios, counts, and costs. That is a useful descriptive warning. Boston's low ratio does not isolate procurement or legal regime as the cause of statewide spending, and a high ratio elsewhere does not itself establish physical overflow or migration attribution. The fiscal, housing, and election questions need matched populations and distinct causal evidence. No previously qualified case is promoted back to a confirmed receiver-overload finding by this audit. [INFERENCE]

## Revisions

- **2026-09-05:** Retained the earlier weak placebo result and case heterogeneity; clarified log/count arithmetic, pre-fit support, endogenous inventory, and the absence of identified causal overload. [Decision](../decisions/2026-09-05-material-inference-repair.md).

<!-- historical-snapshot:start superseded=2026-09-05 -->
<details>
<summary>Superseded historical analysis — retained verbatim for source and correction provenance</summary>

**Historical text, not the current assessment.** Its earlier verdicts, confidence labels, and source-version claims are superseded by the corrections above. It is retained to preserve quotations and the reasoning that was corrected.

# Immigration receiver counterfactuals — 2026-04-22

**Question:** What happens if we stop using counties as the donor pool and instead build synthetic-control style shelter counterfactuals for the main receiver nodes using the national CoC panel?  
**Tier:** Deep | **Date:** 2026-04-22  
**Ground truth:** The receiver failure atlas improved the local object. This pass tests whether the main receiver nodes still look abnormal once matched against the full national `HIC/PIT` donor universe. [SOURCE: research/immigration-receiver-failure-atlas-2026-04-22.md] [SOURCE: sources/immigration-causal/scripts/analyze_receiver_synthetic_controls.py]

## Bottom line

1. `Denver` is still the clearest physical-overload survivor. Even after excluding the most obvious quasi-treated donor hubs, `2024` `sheltered/HIC` is about `+0.48`, `2024` `overall/HIC` about `+0.40`, and `2024` absolute sheltered count about `+0.82` log points above synthetic. [SOURCE: sources/immigration-causal/data/outcomes/analysis/receiver_synth_summary.json]
2. `Chicago` now splits cleanly: ratios stay muted or negative, but absolute load is clearly above synthetic. In `2024`, `log sheltered` is about `+1.38` and `log overall homeless` about `+1.06` above synthetic, which is roughly `4.0x` and `2.9x` the synthetic counts. [SOURCE: same] [INFERENCE]
3. `Boston` still does **not** look like a physical-overload outlier. It remains below synthetic on both ratio outcomes and near-flat on sheltered absolute load, which keeps the `high-cost regime case` interpretation alive. [SOURCE: same]
4. `NYC` remains real but match-fragile. It is strongly above synthetic on sheltered and overall absolute counts, but the synthetic fit is now effectively a `Seattle/King County` match on the log-count outcomes and almost entirely `Seattle` on `sheltered/HIC`, so the absolute-gap signal is directionally useful but not robust enough to treat as clean causal proof. [SOURCE: same] [SOURCE: sources/immigration-causal/data/outcomes/analysis/receiver_synth_weights.csv]
5. The inferential limit survives. Ratio-outcome placebo p-values remain high across treated nodes, so this is still a `directional counterfactual` layer, not decisive synthetic-control identification. [SOURCE: same]

## New artifacts

1. [analyze_receiver_synthetic_controls.py](sources/immigration-causal/scripts/analyze_receiver_synthetic_controls.py)
2. [national_coc_shelter_panel_2018_2024.parquet](sources/immigration-causal/data/outcomes/analysis/national_coc_shelter_panel_2018_2024.parquet)
3. [receiver_synth_yearly.csv](sources/immigration-causal/data/outcomes/analysis/receiver_synth_yearly.csv)
4. [receiver_synth_weights.csv](sources/immigration-causal/data/outcomes/analysis/receiver_synth_weights.csv)
5. [receiver_synth_placebos.csv](sources/immigration-causal/data/outcomes/analysis/receiver_synth_placebos.csv)
6. [receiver_synth_summary.json](sources/immigration-causal/data/outcomes/analysis/receiver_synth_summary.json)

## Claims table

| # | Claim | Evidence | Confidence | Source | Status |
|---|---|---|---|---|---|
| 1 | Denver is the clearest positive post-2022 shelter divergence case | Positive gaps on both shelter outcomes, largest among treated nodes | HIGH | [receiver_synth_summary.json](sources/immigration-causal/data/outcomes/analysis/receiver_synth_summary.json) | VERIFIED |
| 2 | Chicago is an absolute-load divergence case even though its ratio outcomes are muted | Large positive log-count gaps with negative ratio gaps | HIGH | [receiver_synth_summary.json](sources/immigration-causal/data/outcomes/analysis/receiver_synth_summary.json) | VERIFIED |
| 3 | Boston's stress is not well described as abnormal physical overload in the public shelter panel | Negative ratio gaps and near-flat sheltered-count gap despite high local spending | HIGH | [receiver_synth_summary.json](sources/immigration-causal/data/outcomes/analysis/receiver_synth_summary.json) [receiver_failure_atlas_2024.csv](sources/immigration-causal/data/outcomes/analysis/receiver_failure_atlas_2024.csv) | VERIFIED |
| 4 | NYC's synthetic-control result is directionally real but match-fragile | Large positive log-count gaps, but weight concentration collapses onto `WA-500` or near-equivalent two-donor fits | MEDIUM | [receiver_synth_summary.json](sources/immigration-causal/data/outcomes/analysis/receiver_synth_summary.json) [receiver_synth_weights.csv](sources/immigration-causal/data/outcomes/analysis/receiver_synth_weights.csv) | VERIFIED |
| 5 | The placebo universe does not make the ratio divergences look inferentially rare | Filtered placebo p-values remain high across treated nodes | HIGH | [receiver_synth_summary.json](sources/immigration-causal/data/outcomes/analysis/receiver_synth_summary.json) | VERIFIED |

## 1) Design

This pass:

1. rebuilt the full national CoC `2018–2024` panel from `HUD HIC/PIT`
2. treated `2022` as the common post-surge start
3. used `2018–2021` pre-period outcome paths plus size predictors to fit simplex-constrained synthetic-control style weights
4. excluded the most obvious quasi-treated donor hubs from the donor pool:
   `Los Angeles`, `San Diego`, `Orange County`, `District of Columbia`, `Miami-Dade`, `Dallas`, `El Paso`, `Texas Balance of State`, and `Houston/Harris`
5. estimated treated gaps for:
   - `sheltered_to_hic_ratio`
   - `overall_to_hic_ratio`
   - `log_pit_sheltered_total`
   - `log_pit_overall_homeless`
6. ran national donor placebos only on the ratio outcomes and then filtered them by comparable pre-fit quality

[SOURCE: sources/immigration-causal/scripts/analyze_receiver_synthetic_controls.py]

The donor pool is still imperfect. The main obvious recipient and border hubs are removed, but several fits remain weight-concentrated on `Seattle/King County`, `Washington Balance of State`, `Philadelphia`, or `Indiana Balance of State`, so the design is still closer to a high-value matching diagnostic than a final causal estimator. [SOURCE: sources/immigration-causal/data/outcomes/analysis/receiver_synth_weights.csv] [INFERENCE]

## 2) The strongest treated divergences

### Denver

`Denver` is the clearest positive divergence case:

1. `sheltered/HIC` average post gap about `+0.27`, `2024` gap about `+0.48`
2. `overall/HIC` average post gap about `+0.28`, `2024` gap about `+0.40`
3. `log sheltered` average post gap about `+0.49`, `2024` gap about `+0.82`
4. `log overall homeless` average post gap about `+0.41`, `2024` gap about `+0.68`

[SOURCE: same]

This is the cleanest counterfactual support for the receiver-atlas story. [INFERENCE]

### Chicago

`Chicago` is the biggest substantive upgrade from the first pass:

1. `sheltered/HIC` average post gap about `-0.045`, `2024` gap about `+0.055`
2. `overall/HIC` average post gap about `-0.230`, `2024` gap about `-0.265`
3. `log sheltered` average post gap about `+0.444`, `2024` gap about `+1.380`
4. `log overall homeless` average post gap about `+0.254`, `2024` gap about `+1.062`

[SOURCE: same]

So `Chicago` now looks like an `absolute load` case more than a `saturation ratio` case. The natural reading is that capacity expanded enough to mute the ratios, but not enough to keep absolute load from moving sharply above synthetic. [INFERENCE]

### NYC

`NYC` stays strong on absolute counts but weakens as a synthetic-control object:

1. `sheltered/HIC` average post gap about `+0.117`, `2024` gap about `+0.202`
2. `overall/HIC` average post gap about `-0.383`, `2024` gap about `-0.375`
3. `log sheltered` average post gap about `+2.617`, `2024` gap about `+2.957`
4. `log overall homeless` average post gap about `+1.826`, `2024` gap about `+2.117`
5. `log` outcomes are matched almost entirely by `WA-500`, and `sheltered/HIC` is `97.5%` `WA-500`

[SOURCE: same] [SOURCE: sources/immigration-causal/data/outcomes/analysis/receiver_synth_weights.csv]

That means the direction of the `NYC` result is still informative, but the fit is too singular to treat as stable counterfactual proof. [INFERENCE]

### Boston

`Boston` remains the key negative result:

1. `sheltered/HIC` average post gap about `-0.077`, `2024` gap about `-0.170`
2. `overall/HIC` average post gap about `-0.303`, `2024` gap about `-0.378`
3. `log sheltered` average post gap about `+0.059`, `2024` gap about `+0.089`
4. `log overall homeless` average post gap about `-0.292`, `2024` gap about `-0.249`

[SOURCE: same]

That is not a public-data physical-overload profile. It keeps `Boston` in the `high-cost regime / assignment burden / procurement stress` bucket rather than the `physical shelter saturation` bucket. [INFERENCE]

### Bexar

`Bexar` is not cleanly one-sided:

1. `sheltered/HIC` average post gap about `+0.064`
2. `overall/HIC` average post gap about `-0.398`
3. `log sheltered` average post gap about `+0.228`
4. `log overall homeless` average post gap about `+0.016`

[SOURCE: sources/immigration-causal/data/outcomes/analysis/receiver_synth_summary.json]

That means the border/transit case still needs its own logic. [INFERENCE]

## 3) The placebo problem

This is the main limit and it matters.

The script computes placebo comparisons only for the ratio outcomes:

1. raw placebo p-values over all donor CoCs
2. filtered placebo p-values keeping only donor placebos with pre-RMSPE at most `5x` the treated unit's pre-RMSPE

[SOURCE: sources/immigration-causal/data/outcomes/analysis/receiver_synth_summary.json]

Those filtered p-values are still high:

1. `Denver sheltered/HIC`: about `0.71`
2. `Denver overall/HIC`: about `0.89`
3. `NYC sheltered/HIC`: about `0.93`
4. `Chicago sheltered/HIC`: about `0.90`
5. `Boston sheltered/HIC`: about `0.94`

[SOURCE: same]

So the correct reading is:

1. the synthetic controls sharpen **which direction** each receiver differs from its synthetic match
2. the ratio outcomes do **not** make those differences look unusually rare relative to the full national donor volatility
3. the absolute-count outcomes are useful disconfirmation checks against denominator endogeneity, but they are not yet backed by the same placebo layer

That means this is not the final inferential design. [INFERENCE]

## 4) What this changes

The synthetic-control pass is still useful because it kills a few tempting shortcuts:

1. it kills “all stressed receivers are shelter-saturation outliers”  
   `Boston` still does not survive that story.
2. it kills “Chicago disappears under counterfactuals”  
   `Chicago` reappears once the endogenous-denominator problem is checked with absolute counts.
3. it kills “NYC and Denver are the same type of case”  
   `Denver` is the cleaner physical divergence case; `NYC` is larger but much more match-fragile.
4. it keeps alive the claim that `Denver` is the strongest positive shelter-overload case in the current public panel.

## What now survives

1. `Denver` remains the clearest physical receiver overload case [SOURCE: same]
2. `Chicago` remains a real receiver-stress case once absolute load is separated from saturation ratios [SOURCE: same]
3. `Boston` remains a high-cost but not clean physical-overload case [SOURCE: same] [SOURCE: research/immigration-receiver-failure-atlas-2026-04-22.md]
4. `NYC` remains real, but the synthetic match is too concentrated for strong causal rhetoric [SOURCE: same] [SOURCE: sources/immigration-causal/data/outcomes/analysis/receiver_synth_weights.csv]
5. shelter synthetic controls alone do not settle the broader local-incidence claim [INFERENCE]

## Best current formulation

The best current counterfactual statement is:

1. `receiver-node analysis was the right frontier shift`
2. `shelter synthetic controls are informative but not decisive`
3. `Denver` is the strongest physical-overload survivor
4. `Chicago` is an absolute-load survivor even though its ratios are muted
5. `Boston` still points harder toward regime-cost and service-load analysis than toward physical shelter overload
6. `NYC` still needs a more stable counterfactual design than the current highly concentrated donor match

That is a narrower, better claim than either “county thresholds prove it” or “the receiver cases disappear under counterfactuals.” [INFERENCE]

</details>
<!-- historical-snapshot:end -->
