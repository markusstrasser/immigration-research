# Verified Disposition — 2026-04-22

**Claims:** 19 total — 11 CONFIRMED, 0 CORRECTED, 0 HALLUCINATED, 8 INCONCLUSIVE


| # | Verdict | Claim | Notes |
|---|---------|-------|-------|
| 1 | CONFIRMED | Archival newcomer memo is internally contradictory | research/immigration-causal-internal-vs-immigrant-newcomers.md anchors ACS, B07001_081E |
| 2 | INCONCLUSIVE | Current citation graph points to semantically stale source | research/immigration-confidence-ladder.md:22 readable |
| 3 | INCONCLUSIVE | Missing machine-readable measurement metadata | no file references or structured file anchors |
| 4 | INCONCLUSIVE | Failure to source internal narrative blocks | research/immigration-causal-internal-vs-immigrant-newcomers.md exists |
| 5 | CONFIRMED | Threshold holdout splits may leak spatially correlated counties between train an... | sources/immigration-causal/scripts/analyze_capacity_falsification.py anchors THRESHOLD_SPLITS, threshold_search_holdout |
| 6 | CONFIRMED | Newcomer script semantics were only partially cleaned | sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py anchors B05005_002E, B05005_004E, fetch_acs_county_population_and_recent_fb |
| 7 | INCONCLUSIVE | README output-path contract is stale | sources/immigration-causal/README.md exists; anchors not corroborated in resolved file context |
| 8 | CONFIRMED | ACS moved-from-abroad share uses the wrong population universe as denominator | sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py:114 anchors ACS, moved_from_abroad_share; sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py anchors ACS, B07001_081E, moved_from_abroad_share |
| 9 | CONFIRMED | Newcomer memo omits the direction of measurement bias in the 20.5x ratio | research/immigration-causal-internal-vs-immigrant-newcomers.md anchors ACS, B07001_081E, IRS |
| 10 | INCONCLUSIVE | Annual county panels are insufficient for causal wage-channel inference and shou... | no file references or structured file anchors |
| 11 | INCONCLUSIVE | Threshold search should be framed as descriptive classification, not a causal br... | no file references or structured file anchors |
| 12 | CONFIRMED | Zero-base growth handling can create survivor bias if reused for sector-level QC... | sources/immigration-causal/scripts/build_county_outcome_panel.py anchors QCEW, zero_base_count |
| 13 | CONFIRMED | Threshold-search confidence is qualitatively downgraded but under-quantified | sources/immigration-causal/scripts/analyze_capacity_falsification.py anchors THRESHOLD_SPLITS |
| 14 | CONFIRMED | Missing ACS MOE filtering for newcomer comparison | sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py anchors ACS, B07001_081E |
| 15 | INCONCLUSIVE | Under-quantification of evidence strength | research/immigration-capacity-falsification-2026-04-21.md exists |
| 16 | CONFIRMED | IRS and ACS newcomer shares are not directly comparable because they count diffe... | sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py anchors ACS, IRS, SOI, us_inflow_persons |
| 17 | INCONCLUSIVE | Missing memo-artifact consistency linter | no file references or structured file anchors |
| 18 | CONFIRMED | QCEW nondisclosure handling lacks an explicit assertion check | sources/immigration-causal/scripts/build_county_outcome_panel.py anchors QCEW, nondisclosure_missing_base_count, to_numeric |
| 19 | CONFIRMED | Legacy 'native' terminology should be removed from the immigration index and pla... | research/immigration-INDEX.md anchors INDEX, IRS |

