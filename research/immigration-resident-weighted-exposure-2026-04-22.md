# Immigration resident-weighted exposure correction — 2026-04-22

**Question:** How much did the county-median newcomer framing distort the typical resident, renter, and child exposure story?  
**Tier:** Deep | **Date:** 2026-04-22  
**Ground truth:** The earlier newcomer memo was explicitly descriptive, but it still used county medians that were not aligned with typical resident exposure. This pass repairs that by weighting exposures by residents, renter households, and children. [SOURCE: .model-review/2026-04-22-immigration-capacity-falsification-close-9b3c1e/verified-disposition.md] [SOURCE: sources/immigration-causal/scripts/analyze_resident_weighted_exposure.py]

## Bottom line

1. The old county-median framing **overstated** how dominant domestic newcomer flows are relative to moved-from-abroad flows for the typical resident. The median-county ratio is still about `20.4x`, but the ratio of population-weighted means is only about `8.1x`, and the renter-weighted ratio is only about `7.1x`. [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_resident_weighted_exposure_summary.json]
2. County medians **understated** exposure to immigrant-specific flow layers. `moved_from_abroad_share` rises from a county median of about `0.21%` to a population-weighted mean of about `0.56%`. `recent_fb_annual_share` rises from about `0.08%` to about `0.35%`. [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_resident_weighted_metric_summary.csv]
3. Exposure is heavily concentrated once you weight by actual people. The top `20%` of counties by recent foreign-born inflow contain about `65.0%` of residents and `71.4%` of renter households. The `flow-capacity hotspot` slice is only about `7.0%` of counties, but it contains about `22.2%` of residents and `24.9%` of renter households. [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_resident_weighted_stress_shares.csv]
4. Receiver cities are a tiny county share but a nontrivial resident and renter share: only about `0.67%` of counties, but about `9.1%` of residents and `13.0%` of renter households. [SOURCE: same]

## New artifacts

1. [analyze_resident_weighted_exposure.py](sources/immigration-causal/scripts/analyze_resident_weighted_exposure.py)
2. [county_resident_weighted_metric_summary.csv](sources/immigration-causal/data/outcomes/analysis/county_resident_weighted_metric_summary.csv)
3. [county_resident_weighted_stress_shares.csv](sources/immigration-causal/data/outcomes/analysis/county_resident_weighted_stress_shares.csv)
4. [county_resident_weighted_exposure_summary.json](sources/immigration-causal/data/outcomes/analysis/county_resident_weighted_exposure_summary.json)

## Claims table

| # | Claim | Evidence | Confidence | Source | Status |
|---|---|---|---|---|---|
| 1 | County medians overstated domestic-vs-abroad newcomer dominance for the typical resident | `20.4x` median-county ratio falls to `8.1x` population-weighted and `7.1x` renter-weighted | HIGH | [county_resident_weighted_exposure_summary.json](sources/immigration-causal/data/outcomes/analysis/county_resident_weighted_exposure_summary.json) | VERIFIED |
| 2 | County medians understated immigrant-specific flow exposure | `moved_from_abroad_share` and `recent_fb_annual_share` both rise materially under resident weighting | HIGH | [county_resident_weighted_metric_summary.csv](sources/immigration-causal/data/outcomes/analysis/county_resident_weighted_metric_summary.csv) | VERIFIED |
| 3 | High-flow counties contain a disproportionate share of renters and children | Top `20%` recent-flow counties contain about `71.4%` of renter households and `65.5%` of children | HIGH | [county_resident_weighted_stress_shares.csv](sources/immigration-causal/data/outcomes/analysis/county_resident_weighted_stress_shares.csv) | VERIFIED |

## 1) The newcomer ratio changes once you weight by actual people

The old descriptive newcomer comparison said:

1. median county `us_inflow_share ≈ 4.55%`
2. median county `moved_from_abroad_share ≈ 0.21%`
3. median county ratio `≈ 20.4x`

That survives as a county-level descriptive fact. [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_resident_weighted_metric_summary.csv] [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_resident_weighted_exposure_summary.json]

But the resident-weighted repair changes the interpretation:

1. `us_inflow_share` population-weighted mean `≈ 4.51%`
2. `moved_from_abroad_share` population-weighted mean `≈ 0.56%`
3. ratio of those weighted means `≈ 8.1x`

The renter-weighted ratio is even lower at about `7.1x`. [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_resident_weighted_exposure_summary.json]

So the stronger corrected statement is:

1. domestic newcomer counts are still much larger than moved-from-abroad counts
2. but the old county-median framing made that gap look much larger than it is for the typical resident or renter

## 2) Resident weighting raises the immigrant-flow exposure story

The biggest shifts are:

1. `moved_from_abroad_share`: county median `0.21%` -> population-weighted mean `0.56%`
2. `recent_fb_annual_share`: county median `0.08%` -> population-weighted mean `0.35%`
3. `recent_fb_per_permit_share`: county median `0.086` -> population-weighted mean `0.326`

[SOURCE: sources/immigration-causal/data/outcomes/analysis/county_resident_weighted_metric_summary.csv]

That means the typical resident lives in counties with materially more immigrant-flow exposure than the county median suggests. [INFERENCE]

This matters because the local-incidence question is about people living in stressed places, not about the median county in the abstract. [INFERENCE]

## 3) The stress geography is much more concentrated for renters

Weighting by renter households strengthens the concentration result:

1. `high_recent_q80`: only `20%` of counties, but about `71.4%` of renter households
2. `flow_capacity_hotspot`: only about `7.0%` of counties, but about `24.9%` of renter households
3. `high_load_q90`: only about `9.7%` of counties, but about `20.9%` of renter households

[SOURCE: sources/immigration-causal/data/outcomes/analysis/county_resident_weighted_stress_shares.csv]

That is exactly the direction the repo should care about. Renters are more exposed than the county count alone suggests. [INFERENCE]

Children also concentrate in these counties, but a bit less than renters:

1. `high_recent_q80`: about `65.5%` of children
2. `flow_capacity_hotspot`: about `21.5%` of children
3. `high_load_q90`: about `17.6%` of children

[SOURCE: same]

## 4) Receiver cities are small in county count, large in actual exposure

Receiver cities are only about `0.67%` of counties in this sample, but they contain:

1. about `9.1%` of residents
2. about `13.0%` of renter households
3. about `9.1%` of children

[SOURCE: same]

So “receiver cities are a tiny special case” is true only in county-count terms, not in actual exposed population terms. [INFERENCE]

## What now survives

1. the earlier newcomer memo was directionally useful but the county-median ratio should not be used as the main population-exposure summary [INFERENCE]
2. resident-weighted and renter-weighted summaries are the right next default for local-incidence framing [INFERENCE]
3. renter exposure is more concentrated than county counts suggest [SOURCE: sources/immigration-causal/data/outcomes/analysis/county_resident_weighted_stress_shares.csv]

## Best current formulation

The corrected newcomer framing is:

1. `county medians` are a descriptive geography fact
2. `resident-weighted means` are better for typical exposure
3. `renter-weighted` and `child-weighted` views are better for housing and school-incidence questions

That is a real measurement upgrade, not a cosmetic rewrite. [INFERENCE]
