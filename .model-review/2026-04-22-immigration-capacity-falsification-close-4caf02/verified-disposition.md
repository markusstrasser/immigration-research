# Verified Disposition — 2026-04-22

**Claims:** 18 total — 10 CONFIRMED, 0 CORRECTED, 2 HALLUCINATED, 6 INCONCLUSIVE

**Hallucination rate:** 11%


| # | Verdict | Claim | Notes |
|---|---------|-------|-------|
| 1 | INCONCLUSIVE | Semantically incorrect 'pretrend' naming for lead associations | sources/immigration-causal/data/outcomes/analysis/county_capacity_falsification_summary.json exists; sources/immigration-causal/data/outcomes/analysis/county_capacity_falsification_summary.json exists; anchors not corroborated in resolved file context |
| 2 | INCONCLUSIVE | Employment post-effect fails magnitude check against pre-surge leads | sources/immigration-causal/data/outcomes/analysis/county_capacity_pretrend_results.csv exists; anchors not corroborated in resolved file context |
| 3 | HALLUCINATED | `recent_fb_proxy` is an invalid proxy for the 2021–2024 surge | falsification_summary.json not found; falsification_summary.js not found |
| 4 | CONFIRMED | Domestic-vs-foreign newcomer comparison mixes incompatible sources, time windows... | sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py anchors ACS, IRS, SOI, moved_from_abroad_share, us_inflow_persons |
| 5 | CONFIRMED | Threshold validation mislabeled as holdout stability | sources/immigration-causal/data/outcomes/analysis/county_capacity_threshold_validation.csv anchors test_sign_matches_train |
| 6 | CONFIRMED | Modal threshold calculated using marginal modes instead of joint mode | sources/immigration-causal/scripts/analyze_capacity_falsification.py anchors modal_permit_quantile, modal_recent_quantile, permit_quantile, recent_quantile |
| 7 | CONFIRMED | QCEW wage-change outcome is nominal and may confound inflation with real wage ef... | sources/immigration-causal/scripts/build_county_outcome_panel.py anchors QCEW, annual_avg_wkly_wage |
| 8 | CONFIRMED | Semantic regression in migration-series labels | sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py anchors ACS, IRS |
| 9 | INCONCLUSIVE | Narrative overreach regarding 'causal amplifier' vs 'stress marker' | research/immigration-capacity-falsification-2026-04-21.md exists |
| 10 | CONFIRMED | QCEW nondisclosure audit lacks analysis-sample intersection evidence | sources/immigration-causal/data/outcomes/county_outcome_panel_audit.json anchors QCEW; sources/immigration-causal/data/outcomes/county_outcome_panel_audit.json anchors QCEW |
| 11 | INCONCLUSIVE | Lack of hard narrative gate for causal prose | no file references or structured file anchors |
| 12 | CONFIRMED | IRS migration data likely undercounts low-income and undocumented movers, biasin... | sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py anchors ACS, IRS, SOI, us_inflow |
| 13 | CONFIRMED | `us_inflow_share` overstates what IRS code 97 measures | sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py anchors IRS, SOI, Total Migration-US, us_inflow_share, y1_statefips |
| 14 | CONFIRMED | Permutation test is under-specified and may violate exchangeability or ignore sp... | sources/immigration-causal/scripts/analyze_capacity_falsification.py anchors OLS, spearman_rho |
| 15 | CONFIRMED | QCEW suppression-induced attrition is not audited for treatment correlation | sources/immigration-causal/scripts/build_county_outcome_panel.py anchors QCEW, disclosure_code, disclosure_code == 'N' |
| 16 | HALLUCINATED | Research memos lack machine-readable status metadata for superseded/falsified ar... | research/*.md not found |
| 17 | INCONCLUSIVE | Missing finite-sample permutation reporting | no file references or structured file anchors |
| 18 | INCONCLUSIVE | Lack of source-transparency in threshold metadata | no file references or structured file anchors |

