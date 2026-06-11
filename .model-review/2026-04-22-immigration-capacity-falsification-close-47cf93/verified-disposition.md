# Verified Disposition — 2026-04-22

**Claims:** 19 total — 9 CONFIRMED, 0 CORRECTED, 0 HALLUCINATED, 10 INCONCLUSIVE


| # | Verdict | Claim | Notes |
|---|---------|-------|-------|
| 1 | CONFIRMED | Immigrant inflow proxy annualizes a 12-year stock by dividing by 12 | sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py anchors ACS, IRS, recent_fb_annual_avg |
| 2 | CONFIRMED | Mislabeling of pretrend test as pure placebo | sources/immigration-causal/data/outcomes/analysis/county_capacity_falsification_summary.json anchors ACS; sources/immigration-causal/data/outcomes/analysis/county_capacity_falsification_summary.json anchors ACS |
| 3 | INCONCLUSIVE | Unreported sample attrition for zero-permit counties | sources/immigration-causal/data/outcomes/analysis/county_capacity_pretrend_results.csv exists; anchors not corroborated in resolved file context |
| 4 | INCONCLUSIVE | Contradictory employment effect claims across documents | research/immigration-county-outcome-panel-2026-04-21.md exists; anchors not corroborated in resolved file context |
| 5 | CONFIRMED | QCEW nondisclosures are handled implicitly via numeric coercion instead of expli... | sources/immigration-causal/scripts/build_county_outcome_panel.py anchors QCEW, annual_avg_emplvl, annual_avg_wkly_wage, disclosure_code, pd.NA, pd.to_numeric(ratio, errors="coerce"), to_numeric |
| 6 | INCONCLUSIVE | Cross-outcome transfer of threshold discovery | sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_validation.csv exists; anchors not corroborated in resolved file context |
| 7 | CONFIRMED | Pretrend check uses only one clean pre-period difference | sources/immigration-causal/scripts/build_county_outcome_panel.py anchors QCEW |
| 8 | CONFIRMED | Underspecified QCEW nondisclosure handling | sources/immigration-causal/data/outcomes/county_outcome_panel_audit.json anchors QCEW; sources/immigration-causal/data/outcomes/county_outcome_panel_audit.json anchors QCEW |
| 9 | INCONCLUSIVE | Inconsistent county universes across analysis sections | sources/immigration-causal/data/outcomes/analysis/county_capacity_falsification_summary.json exists; sources/immigration-causal/data/outcomes/analysis/county_capacity_falsification_summary.json exists; anchors not corroborated in resolved file context |
| 10 | INCONCLUSIVE | Low absolute concentration of threshold location | sources/immigration-causal/data/outcomes/analysis/county_capacity_falsification_summary.json exists; sources/immigration-causal/data/outcomes/analysis/county_capacity_falsification_summary.json exists; anchors not corroborated in resolved file context |
| 11 | CONFIRMED | Nominal QCEW wage comparisons likely understate real wage penalties in low-capac... | research/immigration-county-outcome-panel-2026-04-21.md anchors -1.49 pp, QCEW, low_permit |
| 12 | INCONCLUSIVE | Inconsistent document provenance and timestamps | research/immigration-reasoning-evolution-2026-04-21.md exists |
| 13 | INCONCLUSIVE | County population filter may bias the domestic-versus-immigrant newcomer ratio | sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py exists; anchors not corroborated in resolved file context |
| 14 | INCONCLUSIVE | Permit baseline may not map cleanly to surge-period housing throughput | no file references or structured file anchors |
| 15 | CONFIRMED | County outcome regressions may be vulnerable to omitted state-level or remote-wo... | sources/immigration-causal/scripts/analyze_county_outcome_panel.py anchors QCEW, high_recent_fb, low_permit |
| 16 | CONFIRMED | Persistent [DATA] placeholders in county-outcome memo | research/immigration-county-outcome-panel-2026-04-21.md anchors DATA |
| 17 | CONFIRMED | Missing instrument-bias caveats in index documentation | research/immigration-INDEX.md anchors INDEX |
| 18 | INCONCLUSIVE | Native-flight interpretation is tested with net migration instead of gross outfl... | no file references or structured file anchors |
| 19 | INCONCLUSIVE | Capacity ranking ignores persons-per-unit differences in permit counts | no file references or structured file anchors |

