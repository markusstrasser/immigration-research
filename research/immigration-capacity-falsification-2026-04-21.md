# Immigration capacity falsification pass — 2026-04-21

**Question:** After correcting the earlier placebo bug, what survives real falsification pressure in the county `flow/capacity` result, and what has to be narrowed?  
**Tier:** Deep | **Date:** 2026-04-21  
**Ground truth:** The prior frontier memo argued that `recent immigrant flow relative to local build capacity` was the cleaner county stress object for wages, employment, and local sorting pressure than stock share alone. [SOURCE: research/immigration-capacity-frontier-2026-04-21.md]  
**Instrument note:** This is a politically charged topic; treat the synthesis as a repo artifact to be checked against raw outputs, not as neutral narration from a bias-free instrument. [SOURCE: notes/llm-bias-caveat.md]

## Bottom line

1. The county `load/capacity` signal is still **structurally real on the descriptive side**. It beats `1,000` within-state permutations at the floor `p<=0.001`, survives leave-one-division-out, and remains strongly monotone across load deciles. [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_permutation_results.csv] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_geographic_leaveout.csv] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_monotonicity.csv]
2. The old `2021–2022` placebo section was mislabeled because it used overlapping treatment windows. After rebuilding the panel, moving the permit baseline back to `2017–2019`, and extending QCEW to add a second clean pre-COVID window (`2017–2018`), the annual presurge evidence still does **not** yield a clean causal reading. [SOURCE: .model-review/2026-04-22-immigration-capacity-falsification-83e8f8/verified-disposition.md] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_pretrend_results.csv]
3. The annual-data causal split is now **provisional, not settled**:
   - `wage story`: not clean either, because the two clean presurge windows move in opposite directions (`2017–2018` positive, `2018–2019` weak negative), which looks more like unstable lead-exposure association than a stable causal pretrend test [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_pretrend_results.csv]
   - `employment story`: remains more suspicious, because both clean presurge windows are already negative [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_pretrend_results.csv]
   - any stronger wage-versus-employment split that leans on `2019–2020` or `2020–2021` is still contaminated by COVID-era annual averaging and should be treated as unverified pending quarterly or better pre-2020 reruns [INFERENCE]
4. The threshold result no longer supports a generic “real family across outcomes” claim. It now supports a **wage-tuned exploratory threshold search that beats the null on performance but not on stable location**. Wage holdout sign stability beats the null strongly, while the selected cutoff surface is diffuse, transfer to `margin` is poor, and transfer to `employment` is only moderate. [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_search_holdout.csv] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_search_null.csv] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_surface.csv]
5. The right updated claim is:
   - `flow/capacity` is a robust county stress marker [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_permutation_results.csv] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_geographic_leaveout.csv] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_monotonicity.csv]
   - it is a strong descriptive stress marker, but the annual county panel still does not cleanly identify the wage channel as causal [INFERENCE]
   - county employment effects remain harder to separate from preexisting weakness [INFERENCE]
   - the current falsification claim set excludes the IRS domestic-migration layer because it is not a native-incumbent-only outcome [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_sample_accounting.json]
   - the county panel is still not enough to settle the full local-incidence causal graph by itself [INFERENCE]

## New artifacts

1. [analyze_capacity_falsification.py](/Users/alien/Projects/research/sources/immigration-causal/scripts/analyze_capacity_falsification.py)
2. [county_capacity_falsification_summary.json](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_capacity_falsification_summary.json)
3. [county_capacity_sample_accounting.json](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_capacity_sample_accounting.json)
4. [county_capacity_permutation_results.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_capacity_permutation_results.csv)
5. [county_capacity_pretrend_results.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_capacity_pretrend_results.csv)
6. [county_capacity_overlap_results.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_capacity_overlap_results.csv)
7. [county_capacity_geographic_leaveout.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_capacity_geographic_leaveout.csv)
8. [county_capacity_threshold_search_holdout.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_search_holdout.csv)
9. [county_capacity_threshold_search_null.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_search_null.csv)
10. [county_capacity_threshold_surface.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_surface.csv)
11. [county_capacity_monotonicity.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_capacity_monotonicity.csv)
12. [county_outcome_panel_audit.json](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/county_outcome_panel_audit.json)

## Claims table

| # | Claim | Evidence | Confidence | Source | Status |
|---|---|---|---|---|---|
| 1 | The county `load/capacity` signal is much stronger than a random within-state reassignment | All four predeclared outcomes beat `1,000` within-state permutations with zero exceedances, so the empirical p-value is at the floor `p<=0.001` rather than a more precise tail estimate | HIGH | [county_capacity_permutation_results.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_capacity_permutation_results.csv) | VERIFIED |
| 2 | The descriptive sign is not just Texas or one regional corridor | Leave-one-division-out and leave-one-state-out preserve the sign for margin, wages, and employment | HIGH | [county_capacity_geographic_leaveout.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_capacity_geographic_leaveout.csv) | VERIFIED |
| 3 | Decile monotonicity is real at the main outcomes | Spearman trends remain strong and correctly signed across the load deciles for margin, wages, and employment | HIGH | [county_capacity_monotonicity.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_capacity_monotonicity.csv) | VERIFIED |
| 4 | The clean presurge windows do not give a clean causal wage reading, while employment remains suspicious | `2017–2018` wage is positive and `2018–2019` wage is weak negative, while both clean employment windows are already negative under the same `2017–2019` permit baseline | HIGH | [county_capacity_pretrend_results.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_capacity_pretrend_results.csv) | VERIFIED |
| 5 | A wage-tuned threshold search beats the null on performance, but not on stable cutoff location | Under state-group holdouts, wage holdout sign stability is `96.0%` versus `43.0%` in the null search, but the joint-mode actual cutoff cell appears in only `22%` of splits and the top-three actual cells sum to `47.0%` | MEDIUM | [county_capacity_threshold_search_holdout.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_search_holdout.csv) [county_capacity_threshold_search_null.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_search_null.csv) [county_capacity_threshold_surface.csv](/Users/alien/Projects/research/sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_surface.csv) | VERIFIED |

## 1) Sample definition and measurement limits

The corrected falsification pass uses:

1. `2,390` counties with `population >= 10,000` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_sample_accounting.json]
2. `64` counties with zero `2021–2024` permits and `77` counties with zero `2017–2019` permits, which means the continuous load ratio excludes some no-build counties by construction [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_sample_accounting.json]
3. a `recent foreign-born flow` proxy built from ACS `2022` 5-year `B05005 entered 2010 or later` stock divided by `12`, which is useful but **not** a sharp `2021–2024` arrival measure [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_sample_accounting.json]
4. the rebuilt county panel audit now carries explicit machine-readable window metadata, including which windows touch `2020` and which are intended only for descriptive overlap [SOURCE: sources/immigration-causal/data/outcomes/county_outcome_panel_audit.json]
5. the falsification pass excludes the IRS `97/000` domestic-migration layer from the main claim set because it is `Total Migration-US`, not a native-incumbent-only measure [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_sample_accounting.json]
6. the clean pre-surge regressions run on `2,313` counties rather than the full `2,390`, because the prebase load ratio drops counties with zero `2017–2019` permit units [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_sample_accounting.json] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_pretrend_results.csv]

That measurement structure is good enough for a stress-object audit. It is not good enough to pretend we have exact arrival timing. [INFERENCE]

## 2) Permutation and geographic robustness: the descriptive signal survives

Using `1,000` within-state permutations of the contemporaneous `load/capacity` variable:

1. `margin shift`: observed `t≈6.96`, empirical `p<=0.001` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_permutation_results.csv]
2. `wage growth 2021–2024`: observed `t≈-4.08`, empirical `p<=0.001` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_permutation_results.csv]
3. `employment growth 2021–2024`: observed `t≈-7.10`, empirical `p<=0.001` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_permutation_results.csv]

This is enough to reject the cheap objection that the county load result is just arbitrary noise. [INFERENCE]

A remaining limit is spatial autocorrelation: within-state permutations and division leave-out do not fully solve corridor-level dependence. The permutation result is still strong, but it should be read as strong evidence against cheap random reassignment, not as the last word on spatially aware inference. [INFERENCE]

The stricter leave-out check also survives:

1. leaving out the whole `West South Central` division still leaves wage `t≈-3.30` and employment `t≈-4.24` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_geographic_leaveout.csv]
2. leaving out `Texas` still leaves wage `t≈-3.46` and employment `t≈-5.27` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_geographic_leaveout.csv]
3. leaving out `California` still leaves margin `t≈6.54` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_geographic_leaveout.csv]

So the descriptive sign is not being carried solely by Texas or by one Census division. [INFERENCE]

## 3) Monotonicity: the gradient is still real

Across contemporaneous load deciles:

1. `margin shift`: Spearman `rho≈+0.83`, `p≈0.0029` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_monotonicity.csv]
2. `wage growth`: `rho≈-0.93`, `p≈0.00011` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_monotonicity.csv]
3. `employment growth`: `rho≈-0.96`, `p≈7.3e-06` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_monotonicity.csv]

This still looks more like a gradient than a single knife-edge cutoff. [INFERENCE]

## 4) Annual clean presurge windows: still not a clean causal read

This is the biggest correction relative to the earlier memo.

### Wage-side lead-exposure presurge windows

Using a pre-surge permit baseline from `2017–2019` and the two clean annual pre-COVID windows:

1. `wage 2017–2018`: `beta≈+0.00162`, `p≈0.0137` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_pretrend_results.csv]
2. `wage 2018–2019`: `beta≈-0.00078`, `p≈0.146` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_pretrend_results.csv]

That is not what a clean parallel-trends story looks like. The wage-side presurge association flips sign across the two clean windows, which is better read as unstable lead-exposure association than as evidence that the wage channel is now identified. [INFERENCE]

### Employment-side lead-exposure presurge windows

Employment is different:

1. `employment 2017–2018`: `beta≈-0.00246`, `p≈0.00087` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_pretrend_results.csv]
2. `employment 2018–2019`: `beta≈-0.00299`, `p≈1.6e-06` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_pretrend_results.csv]

What survives cleanly is narrower: employment is already negative in both clean presurge windows. That keeps the employment channel more suspicious, not less. [INFERENCE]

### Post-period with presurge controls

Even after controlling the `2023–2024` outcome for both clean presurge annual changes:

1. `wage post 2023–2024`: `beta≈-0.00126`, `p≈0.0338` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_pretrend_results.csv]
2. `employment post 2023–2024`: `beta≈-0.00230`, `p≈0.00123` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_pretrend_results.csv]

So the post-period effect does not disappear. But on annual data the right interpretation is only:

1. `wage`: still not cleanly identified, because the clean presurge windows do not deliver stable parallel-trends support [INFERENCE]
2. `employment`: also survives annual controls, but remains materially confounded and more suspicious because both clean presurge windows are already negative [INFERENCE]

## 5) Overlap windows: useful descriptively, not as placebo evidence

The earlier `2021–2022` and `2021–2023` results are still in the output, but they are now correctly labeled as **overlap windows**, not pretrends:

1. `wage overlap 2021–2022`: negative, `p≈0.026` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_overlap_results.csv]
2. `employment overlap 2021–2022`: negative, `p≈6.6e-05` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_overlap_results.csv]

Those results still matter descriptively. They just do not identify presurge weakness by themselves. [INFERENCE]

## 6) Threshold search: wage-only exploratory support survives, stable breakpoint claim does not

The corrected threshold pass tunes the cutoff on wage only, then evaluates transfer out of sample. That supports a statement about **search performance**, not a statement that one stable county breakpoint has been found.

### Actual search

The most common selected cells are diffuse:

1. `q80 recent-flow x q50 permit`: `25%` of splits [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_surface.csv]
2. `q70 recent-flow x q50 permit`: `16.7%` of splits [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_surface.csv]
3. the top three actual cells together account for only `56.7%` of splits [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_falsification_summary.json]

So there is no single stable cutoff to endorse. [INFERENCE]

Holdout results:

1. `wage`: holdout sign matches the wage-trained threshold in `96.0%` of splits, `95% CI ≈ [90.2%, 98.4%]`, median `|t|≈1.71` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_search_holdout.csv]
2. `employment`: cross-outcome sign matches the wage-trained threshold in `60.0%` of splits, `95% CI ≈ [50.2%, 69.1%]`, median `|t|≈1.07` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_search_holdout.csv]
3. `margin`: cross-outcome sign matches the wage-trained threshold in only `12%` of splits [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_search_holdout.csv]

### Null search

Under the same search procedure with within-state permuted `recent-flow`:

1. wage holdout sign matches the wage-trained threshold `43.0%` of the time, `95% CI ≈ [33.7%, 52.8%]` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_search_null.csv]
2. median holdout `|t|≈0.87` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_search_null.csv]
3. the real-minus-null wage sign-match delta is about `+53.0 pp`, and the real-minus-null median `|t|` delta is about `+0.84` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_falsification_summary.json]

So the threshold search still beats the null for **wage**, but the cutoff surface is not concentrated enough to justify “the threshold is q80 x q50” or any other single cell. It does **not** justify a sweeping “real family across outcomes” line. [INFERENCE]

## 7) Rival explanations

The strongest alternatives are still:

1. `selection into structurally weaker counties`
2. `regional growth and decline patterns that co-move with both immigration pressure and local outcomes`
3. `timing blur from the ACS recent-arrival proxy`
4. `remaining annual-data limitations relative to a quarterly QCEW design`

What the current pass rules out:

1. pure random reassignment [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_permutation_results.csv]
2. a result carried only by Texas or by a single Census division [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_geographic_leaveout.csv]

What it does **not** fully rule out:

1. preexisting employment weakness
2. omitted local shocks that align with both build constraints and immigrant inflow
3. county-selection dynamics rather than a pure post-surge break

## What now survives

1. `flow relative to local build capacity` is a robust county stress marker [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_permutation_results.csv] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_geographic_leaveout.csv] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_monotonicity.csv]
2. the county signal is not random and is not carried only by Texas or one division [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_permutation_results.csv] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_geographic_leaveout.csv]
3. wage-side post effects remain after annual presurge controls, but the clean presurge wage windows do not support a stable causal reading by themselves [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_pretrend_results.csv]
4. a wage-tuned exploratory threshold search beats a null search on performance [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_search_holdout.csv] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_search_null.csv]
5. the location of that exploratory threshold remains diffuse [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_surface.csv] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_falsification_summary.json]

## What now fails

1. `We found a clean generic post-surge causal threshold from the county panel alone.`  
This is too strong. [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_surface.csv] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_search_holdout.csv]

2. `The annual-data wage-versus-employment causal split is already settled.`  
Too strong. Even after moving the permit baseline back to `2017–2019` and adding a second clean pre-COVID window, the wage-side presurge association flips sign while employment stays negative, so the annual county panel still does not cleanly identify the split. [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_pretrend_results.csv] [SOURCE: sources/immigration-causal/data/outcomes/county_outcome_panel_audit.json]

3. `The threshold story generalizes equally well to wages, employment, and politics.`  
False in the corrected pass. Margin transfer is poor. [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_search_holdout.csv]

## Best current formulation

The strongest defensible version is:

1. `flow/capacity is a robust and highly structured county stress marker` [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_permutation_results.csv] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_geographic_leaveout.csv] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_monotonicity.csv]
2. `it is a strong descriptive stress marker consistent with local strain amplification, but not itself clean causal proof` [INFERENCE]
3. `the annual county panel still does not cleanly identify the wage channel, because the clean presurge wage windows are unstable while employment remains suspicious` [INFERENCE]
4. `receiver-city shelter and service counterfactuals are still the best next causal design` [INFERENCE]
5. `policy relevance remains high` [FRAMING-SENSITIVE] [INFERENCE] because the county stress marker is strong even where the causal partition is incomplete

## Repo stance update

The repo's current best position should now be:

1. `descriptive confidence`: high [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_permutation_results.csv] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_geographic_leaveout.csv] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_capacity_monotonicity.csv]
2. `causal confidence on a clean wage-versus-employment split from the annual county panel`: low [INFERENCE]
3. `causal confidence on the broader stress-marker result`: moderate [INFERENCE]
4. `policy relevance`: still high [FRAMING-SENSITIVE] [INFERENCE], but only if phrased as a stress-marker claim rather than a clean threshold-identification claim

## Revisions

### 2026-04-22

The first draft of this memo treated `2021–2022` overlap windows as placebo/pretrend evidence. After `/critique close` flagged that as a real semantics bug, the county panel was rebuilt with earlier QCEW windows, the falsification script was rewritten around a true presurge permit baseline, and the threshold section was downgraded again once the exported threshold surface showed diffuse cutoff selection. The next close review still objected that one clean pre-COVID window was not enough, so the county panel was extended to `2017` and the annual controls were rerun. That extension weakened the stronger wage-side causal reading further: the clean presurge wage windows are unstable, while employment stays negative in both clean windows. [SOURCE: .model-review/2026-04-22-immigration-capacity-falsification-83e8f8/verified-disposition.md] [SOURCE: .model-review/2026-04-22-immigration-capacity-falsification-final-36f586/verified-disposition.md] [SOURCE: .model-review/2026-04-22-immigration-capacity-falsification-close-47cf93/verified-disposition.md]
