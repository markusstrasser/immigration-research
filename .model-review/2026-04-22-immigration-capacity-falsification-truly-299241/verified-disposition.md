# Verified Disposition — 2026-04-22

**Claims:** 17 total — 13 CONFIRMED, 0 CORRECTED, 0 HALLUCINATED, 4 INCONCLUSIVE


| # | Verdict | Claim | Notes |
|---|---------|-------|-------|
| 1 | CONFIRMED | IRS domestic migration extract appears to use foreign-migration code 97 instead ... | sources/immigration-causal/scripts/build_county_outcome_panel.py anchors FIPS, IRS, load_native_inflow, load_native_outflow, net_us_migration_share_2022_23, us_inflow_returns_2022_23, us_outflow_returns_2022_23, y1_statefips, y2_statefips |
| 2 | CONFIRMED | "Rules out a one-state artifact" appears unsupported by the visible artifact set | research/immigration-capacity-falsification-2026-04-21.md anchors county_capacity_geographic_leaveout |
| 3 | CONFIRMED | Pretrend falsification baseline is endogenous because permit capacity includes 2... | sources/immigration-causal/scripts/analyze_capacity_falsification.py anchors QCEW, extract_pre_surge_permits |
| 4 | CONFIRMED | Annual-average QCEW windows spanning 2020 blur the pandemic shock and may destab... | sources/immigration-causal/scripts/build_county_outcome_panel.py anchors QCEW |
| 5 | CONFIRMED | Code materializes contaminated windows without machine-readable metadata | sources/immigration-causal/scripts/build_county_outcome_panel.py anchors NOT |
| 6 | CONFIRMED | "2018–2020 pretrend windows" language remains semantically loose | research/immigration-INDEX.md anchors INDEX, QCEW |
| 7 | CONFIRMED | Threshold-language is still under-quantified | research/immigration-capacity-falsification-2026-04-21.md anchors CSV |
| 8 | CONFIRMED | Native-mobility threshold and null analyses should be rerun after correcting the... | sources/immigration-causal/data/outcomes/analysis/county_capacity_falsification_summary.json anchors threshold_null, threshold_surface |
| 9 | CONFIRMED | Sample-accounting audit is not aligned to the actual clean-window claim | sources/immigration-causal/scripts/build_county_outcome_panel.py anchors annual_avg_emplvl_2021, qcew_row_missing; sources/immigration-causal/scripts/build_county_outcome_panel.py anchors annual_avg_emplvl_2021, qcew_row_missing |
| 10 | CONFIRMED | Hardcoded occupants-per-unit scalar may systematically mis-scale housing capacit... | sources/immigration-causal/scripts/analyze_capacity_falsification.py anchors ACS, FIPS, OCCUPANTS_PER_UNIT, OCCUPANTS_PER_UNIT = 2.5 |
| 11 | INCONCLUSIVE | "Not a binning accident" is broader than the demonstrated checks | research/immigration-capacity-falsification-2026-04-21.md exists |
| 12 | CONFIRMED | County panel does not explicitly handle QCEW privacy suppressions, risking sampl... | sources/immigration-causal/scripts/build_county_outcome_panel.py anchors FIPS, QCEW, pd.NA |
| 13 | INCONCLUSIVE | Annual causal claims for COVID-overlap years should be explicitly blocked until ... | no file references or structured file anchors |
| 14 | CONFIRMED | IRS migration is treated as a generic native-mobility proxy despite undercoverag... | sources/immigration-causal/scripts/build_county_outcome_panel.py anchors IRS |
| 15 | INCONCLUSIVE | Single-threshold search may be the wrong model for a diffuse cutoff surface | sources/immigration-causal/scripts/analyze_capacity_falsification.py exists; anchors not corroborated in resolved file context |
| 16 | CONFIRMED | Inconsistent sourcing with bare placeholders | research/immigration-capacity-falsification-2026-04-21.md anchors CSV |
| 17 | INCONCLUSIVE | Policy relevance claim is not falsifiable | research/immigration-capacity-falsification-2026-04-21.md exists |

