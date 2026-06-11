# Verified Disposition — 2026-04-22

**Claims:** 16 total — 7 CONFIRMED, 0 CORRECTED, 0 HALLUCINATED, 9 INCONCLUSIVE


| # | Verdict | Claim | Notes |
|---|---------|-------|-------|
| 1 | CONFIRMED | IRS 2022-2023 migration is silently used as a proxy for 2021-2022 migration | sources/immigration-causal/scripts/build_county_outcome_panel.py anchors IRS, net_us_migration_persons_2022_23, net_us_migration_persons_ty2021_2022_proxy, panel["net_us_migration_persons_ty2021_2022_proxy"] = panel["net_us_migration_persons_2022_23"] |
| 2 | CONFIRMED | QCEW annual-average extraction hardcodes COVID contamination into 2020 outcome w... | sources/immigration-causal/scripts/build_county_outcome_panel.py anchors QCEW, chunk["qtr"] == "A" |
| 3 | CONFIRMED | Estimand mismatch in threshold-surface null comparison | sources/immigration-causal/scripts/analyze_capacity_falsification.py anchors actual_wage, build_summary, surface_actual, surface_null |
| 4 | INCONCLUSIVE | Semantically broad plural 'pretrends' usage for single window | research/immigration-capacity-falsification-2026-04-21.md exists |
| 5 | INCONCLUSIVE | Wilson CIs over repeated splits are anti-conservative | sources/immigration-causal/scripts/analyze_capacity_falsification.py exists; anchors not corroborated in resolved file context |
| 6 | CONFIRMED | BPS year filtering relies on fragile string-prefix date matching | sources/immigration-causal/scripts/analyze_capacity_falsification.py anchors BPS, Date, keep_years, to_datetime |
| 7 | INCONCLUSIVE | Pre-surge housing-capacity baseline includes 2020 permits that likely were not a... | sources/immigration-causal/scripts/build_county_outcome_panel.py exists; anchors not corroborated in resolved file context |
| 8 | INCONCLUSIVE | Threshold search is not benchmarked against a continuous capacity model | sources/immigration-causal/scripts/analyze_capacity_falsification.py exists; anchors not corroborated in resolved file context |
| 9 | CONFIRMED | Reasoning-evolution doc claims exceed falsification memo limits | research/immigration-reasoning-evolution-2026-04-21.md anchors COVID |
| 10 | INCONCLUSIVE | Threshold analysis universe restriction is understated | research/immigration-capacity-falsification-2026-04-21.md exists; anchors not corroborated in resolved file context |
| 11 | INCONCLUSIVE | Pandemic-period wage analyses do not control for sector-composition bias | sources/immigration-causal/scripts/analyze_capacity_falsification.py exists; anchors not corroborated in resolved file context |
| 12 | INCONCLUSIVE | Lack of window-specific sample accounting in builder | sources/immigration-causal/scripts/build_county_outcome_panel.py exists; anchors not corroborated in resolved file context |
| 13 | CONFIRMED | Unsourced scalar constant OCCUPANTS_PER_UNIT | sources/immigration-causal/scripts/analyze_capacity_falsification.py anchors OCCUPANTS_PER_UNIT |
| 14 | INCONCLUSIVE | Qualitative evidence descriptions lack quantification | research/immigration-capacity-falsification-2026-04-21.md exists |
| 15 | INCONCLUSIVE | Missing steel-man for smooth-response threshold interpretation | research/immigration-capacity-falsification-2026-04-21.md exists |
| 16 | CONFIRMED | Chunked Pandas QCEW extraction is described as unnecessarily slow and memory-hea... | sources/immigration-causal/scripts/build_county_outcome_panel.py anchors CSV, QCEW, ZIP, read_csv |

