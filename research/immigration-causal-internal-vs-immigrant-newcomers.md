# Domestic migration vs moved-from-abroad counts

Supersession note: for the corrected `typical resident / renter / child` exposure framing, read [immigration-resident-weighted-exposure-2026-04-22.md](research/immigration-resident-weighted-exposure-2026-04-22.md). This file remains useful for the county-level descriptive geography, but not as the best population-exposure summary. [SOURCE: research/immigration-resident-weighted-exposure-2026-04-22.md]

**Date:** 2026-04-22  
**Question:** For county-level newcomer pressure, is the relevant object immigration specifically or newcomer flow more generally?  
**Answer:** County newcomer counts are much larger on the domestic side than on the moved-from-abroad side, but the comparison is descriptive, not like-for-like causal accounting. The current median county with `totpop >= 10k` shows about `4.59%` IRS `Total Migration-US` inflow versus about `0.21%` ACS `Moved from abroad` in the past year. The **ratio of medians** is about `21.7x`, while the **median county-level ratio** among counties with nonzero moved-from-abroad share is about `20.5x`. [SOURCE: sources/immigration-causal/data/analysis/county_newcomer_comparison.parquet]

## Status

This memo supersedes the older `33x` claim that used an annualized `B05005` stock proxy. The current artifact is [county_newcomer_comparison.parquet](sources/immigration-causal/data/analysis/county_newcomer_comparison.parquet), built by [analyze_internal_vs_immigrant_newcomers.py](sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py). Treat older citations to `33x` as outdated. [SOURCE: sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py]

## What The Data Actually Compare

1. **IRS SOI `97/000` inflow**: `Total Migration-US` into a county in `2022–2023`, measured from tax-filer returns and exemptions. This is not a native-only series and it misses some movers. [SOURCE: sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py]
2. **ACS `B07001_081E`**: people age `1+` who `moved from abroad` in the past year, from the `2022` ACS `5-year` file. This is not an immigrant-only series; it can include returning U.S. citizens and other international movers. [SOURCE: sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py]
3. **Denominators differ from the earlier memo**: the ACS moved-from-abroad share now uses `B07001_001E` (population age `1+`) rather than total population. [SOURCE: sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py]

## Current Descriptive Facts

Using counties with `totpop >= 10k`:

1. Median IRS `Total Migration-US` inflow share: about `4.59%`. [SOURCE: sources/immigration-causal/data/analysis/county_newcomer_comparison.parquet]
2. Median ACS moved-from-abroad share: about `0.21%`. [SOURCE: sources/immigration-causal/data/analysis/county_newcomer_comparison.parquet]
3. Median ratio of the two shares: about `20.5x`. [SOURCE: sources/immigration-causal/data/analysis/county_newcomer_comparison.parquet]
4. The direction of measurement bias is **ambiguous**, not one-way. IRS misses some domestic movers, while ACS moved-from-abroad includes some returning U.S. citizens and uses a pooled `5-year` window that can smooth late accelerations in international flow. [SOURCE: sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py]
5. Counties with zero moved-from-abroad share are excluded from the median county-level ratio by construction; that is a different estimand from the ratio of medians. [SOURCE: sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py]

## Why This Still Matters

The repo should stop using “newcomer burden” as if it automatically meant immigration burden at the county level. County aggregates are picking up a much broader mobility process. That does **not** mean immigration-specific channels disappear:

1. immigrant concentration can still matter more at neighborhood, school, or shelter-node scale [INFERENCE]
2. language, legal status, and household structure still make immigrant inflows qualitatively different from generic domestic movers [INFERENCE]
3. countywide newcomer counts alone cannot price those composition effects [INFERENCE]

The clean correction is narrower:

1. county newcomer totals are not immigration-specific by default [SOURCE: sources/immigration-causal/data/analysis/county_newcomer_comparison.parquet]
2. immigration-specific burden claims need a more targeted denominator and geography than this county comparison provides [INFERENCE]

## Limits

1. IRS SOI counts tax-filer units and dependents, not a full resident universe, and likely understates mover counts for some non-filer groups. [SOURCE: sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py]
2. ACS `B07001_081E` is a `5-year` pooled estimate, so it is not a sharp `2022–2023` county flow. [SOURCE: sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py]
3. The current script flags counties where ACS moved-from-abroad MOE is at least as large as the estimate; those counties should be treated cautiously. [SOURCE: sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py]
4. None of this identifies school burden, shelter burden, or wage incidence directly. It is a frame-correction artifact, not a causal burden model. [INFERENCE]

## Repo Implication

Future county-level memos should say one of the following, not “immigrant newcomer burden” by default:

1. `domestic newcomer flow`
2. `moved-from-abroad flow`
3. `newcomer flow, mixed source`

If a memo wants to make an immigration-specific burden claim, it needs a construct that actually isolates that burden rather than borrowing it from a mixed county newcomer count. [INFERENCE]

<!-- knowledge-index
generated: 2026-04-22T23:59:00Z
hash: current

cross_refs: research/immigration-confidence-ladder.md, sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py

end-knowledge-index -->
