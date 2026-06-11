# Verified Disposition — 2026-04-22

**Claims:** 16 total — 12 CONFIRMED, 0 CORRECTED, 1 HALLUCINATED, 3 INCONCLUSIVE

**Hallucination rate:** 6%


| # | Verdict | Claim | Notes |
|---|---------|-------|-------|
| 1 | CONFIRMED | Pretrend windows incorrectly include COVID-disrupted 2020 annual QCEW data | sources/immigration-causal/scripts/build_county_outcome_panel.py anchors (2018, 2020), (2019, 2020), QCEW, annual_avg_emplvl, annual_avg_wkly_wage |
| 2 | CONFIRMED | Memo's wage-versus-employment causal split may be an artifact of 2020 COVID effe... | research/immigration-capacity-falsification-2026-04-21.md anchors COVID |
| 3 | CONFIRMED | Annual-average 2020 QCEW introduces composition bias that can distort wage and e... | sources/immigration-causal/scripts/build_county_outcome_panel.py anchors QCEW, annual_avg_emplvl, annual_avg_wkly_wage |
| 4 | CONFIRMED | Analysis acknowledges COVID contamination but does not perform the basic 2017-20... | research/immigration-capacity-falsification-2026-04-21.md anchors COVID |
| 5 | CONFIRMED | Threshold-surface concentration comparison is likely apples-to-oranges | sources/immigration-causal/scripts/analyze_capacity_falsification.py anchors surface_actual, surface_null; sources/immigration-causal/scripts/analyze_capacity_falsification.py anchors surface_actual, surface_null |
| 6 | INCONCLUSIVE | Remaining bare [SOURCE] placeholders in memos | research/immigration-capacity-falsification-2026-04-21.md exists |
| 7 | CONFIRMED | County panel audit does not actually audit the new 2018–2020 falsification windo... | sources/immigration-causal/scripts/build_county_outcome_panel.py anchors annual_avg_emplvl_2021, isna, qcew_row_missing; sources/immigration-causal/scripts/build_county_outcome_panel.py anchors annual_avg_emplvl_2021, isna, qcew_row_missing |
| 8 | INCONCLUSIVE | Falsification memo conclusion should not retain 'preexisting county weakness' wi... | research/immigration-capacity-falsification-2026-04-21.md exists; anchors not corroborated in resolved file context |
| 9 | CONFIRMED | Reasoning-evolution record does not document the April 21 causal split as a COVI... | research/immigration-reasoning-evolution-2026-04-21.md anchors QCEW |
| 10 | CONFIRMED | QCEW pipeline is too coarse because annual files smear pre-pandemic and peak-pan... | sources/immigration-causal/scripts/build_county_outcome_panel.py anchors QCEW, annual_singlefile, annual_singlefile.zip |
| 11 | CONFIRMED | Spatial robustness wording may outrun the demonstrated leave-out design | research/immigration-capacity-falsification-2026-04-21.md anchors county_capacity_geographic_leaveout |
| 12 | CONFIRMED | Threshold null search may understate false positives by not preserving spatial a... | sources/immigration-causal/scripts/analyze_capacity_falsification.py anchors threshold_null |
| 13 | CONFIRMED | 'Zero base' audit counts are semantically contaminated by missingness | sources/immigration-causal/scripts/build_county_outcome_panel.py anchors _zero_base_count, add_log_change, missing_input, zero_base, zero_base_count, zero_base_flag |
| 14 | HALLUCINATED | Review artifact is being used as empirical evidence, not just provenance | model-review/verified-disposition.md not found |
| 15 | CONFIRMED | Memo claims more window construction than the visible builder shows | sources/immigration-causal/scripts/build_county_outcome_panel.py anchors QCEW |
| 16 | INCONCLUSIVE | Missing memo-to-output consistency checks | no file references or structured file anchors |

