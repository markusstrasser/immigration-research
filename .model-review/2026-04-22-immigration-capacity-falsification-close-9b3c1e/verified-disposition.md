# Verified Disposition — 2026-04-22

**Claims:** 18 total — 9 CONFIRMED, 0 CORRECTED, 0 HALLUCINATED, 9 INCONCLUSIVE


| # | Verdict | Claim | Notes |
|---|---------|-------|-------|
| 1 | CONFIRMED | Conflation of newcomer ratio estimands | research/immigration-causal-internal-vs-immigrant-newcomers.md anchors IRS |
| 2 | INCONCLUSIVE | Invalid Wilson intervals on dependent splits | sources/immigration-causal/scripts/analyze_capacity_falsification.py exists; anchors not corroborated in resolved file context |
| 3 | CONFIRMED | Ambiguous directional bias in newcomer comparison | research/immigration-causal-internal-vs-immigrant-newcomers.md anchors ACS, IRS, MOE |
| 4 | CONFIRMED | QCEW wage growth is analyzed in nominal terms without inflation adjustment | sources/immigration-causal/scripts/build_county_outcome_panel.py anchors QCEW, annual_avg_wkly_wage |
| 5 | CONFIRMED | Dropped QCEW nondisclosures may create MNAR sample bias | sources/immigration-causal/scripts/build_county_outcome_panel.py anchors QCEW, county_outcome_panel_audit, county_outcome_panel_audit.json, disclosure_code, disclosure_code == 'N', recent_fb_annual_share; sources/immigration-causal/data/outcomes/county_outcome_panel_audit.json anchors QCEW, disclosure_code, disclosure_code == 'N' |
| 6 | INCONCLUSIVE | Unjustified upgrade to moderate causal confidence | research/immigration-capacity-falsification-2026-04-21.md exists |
| 7 | CONFIRMED | Permutation null may be invalid if shuffled series re-aligns on original index | sources/immigration-causal/scripts/analyze_capacity_falsification.py anchors .to_numpy, recent_fb_annual_share, to_numpy |
| 8 | CONFIRMED | Median-county newcomer ratios likely misstate typical resident exposure | sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py anchors ACS, IRS, moved_from_abroad_share, us_inflow_share |
| 9 | INCONCLUSIVE | Threshold-search null lacks regional or spatial correlation structure | sources/immigration-causal/scripts/analyze_capacity_falsification.py exists; anchors not corroborated in resolved file context |
| 10 | INCONCLUSIVE | Pretrend instability is not formalized with an explicit stability metric | sources/immigration-causal/scripts/analyze_capacity_falsification.py exists; anchors not corroborated in resolved file context |
| 11 | CONFIRMED | Underspecified newcomer ratio for zero denominators | sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py anchors moved_from_abroad |
| 12 | INCONCLUSIVE | Lack of quantitative metrics for threshold surface diffuseness | sources/immigration-causal/scripts/analyze_capacity_falsification.py exists; anchors not corroborated in resolved file context |
| 13 | CONFIRMED | IRS migration data uncertainty is not quantified alongside ACS error | sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py anchors ACS, IRS, SOI |
| 14 | INCONCLUSIVE | Improper source attribution for semantic claims | research/immigration-causal-internal-vs-immigrant-newcomers.md exists |
| 15 | INCONCLUSIVE | Flow-to-capacity stress metric may be unstable near zero permit capacity | sources/immigration-causal/scripts/analyze_capacity_falsification.py exists; anchors not corroborated in resolved file context |
| 16 | INCONCLUSIVE | Wilson intervals may be too narrow if holdout folds are correlated | sources/immigration-causal/scripts/analyze_capacity_falsification.py exists; anchors not corroborated in resolved file context |
| 17 | CONFIRMED | Newcomer shares use inconsistent denominators | sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py anchors ACS, B01003_001E, B07001_001E, B07001_081E, moved_from_abroad_share, totpop, us_inflow_persons, us_inflow_share |
| 18 | INCONCLUSIVE | Non-falsifiable policy relevance claim | no file references or structured file anchors |

