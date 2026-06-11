# Verified Disposition — 2026-04-22

**Claims:** 19 total — 9 CONFIRMED, 0 CORRECTED, 0 HALLUCINATED, 10 INCONCLUSIVE


| # | Verdict | Claim | Notes |
|---|---------|-------|-------|
| 1 | CONFIRMED | Silent deduplication of QCEW county-year records | sources/immigration-causal/scripts/build_county_outcome_panel.py anchors QCEW, drop_duplicates |
| 2 | CONFIRMED | Raw `fips5` left joins can silently drop or null counties across IRS and QCEW so... | sources/immigration-causal/scripts/build_county_outcome_panel.py anchors FIPS, IRS, QCEW, elect, fips5, how="left", inflow, outflow, qcew |
| 3 | CONFIRMED | Zero-denominator log changes are silently dropped instead of handled explicitly | sources/immigration-causal/scripts/build_county_outcome_panel.py anchors QCEW, base_col, end_col, pd.Series(panel[end_col]).div(panel[base_col]).where(panel[base_col] > 0) |
| 4 | INCONCLUSIVE | Over-reification of modal threshold selection in wage analysis | sources/immigration-causal/scripts/analyze_capacity_falsification.py exists; anchors not corroborated in resolved file context |
| 5 | INCONCLUSIVE | Ambiguous semantic definition of 2018-2020 pretrend windows | sources/immigration-causal/scripts/build_county_outcome_panel.py exists; anchors not corroborated in resolved file context |
| 6 | INCONCLUSIVE | Missing outcome-window sample ledgers | no file references or structured file anchors |
| 7 | CONFIRMED | Within-state permutation inference ignores spatial autocorrelation and may overs... | sources/immigration-causal/scripts/analyze_capacity_falsification.py anchors default_rng, np.random.default_rng(20260421) |
| 8 | CONFIRMED | Panel builder does not materialize the claimed 2018–2020 QCEW window | sources/immigration-causal/scripts/build_county_outcome_panel.py:144 anchors QCEW; sources/immigration-causal/scripts/build_county_outcome_panel.py anchors (2018, 2019), (2019, 2020), (2020, 2021), (2021, 2022), (2021, 2023), (2021, 2024), (2023, 2024), QCEW, add_log_change; sources/immigration-causal/scripts/analyze_capacity_falsification.py anchors QCEW |
| 9 | CONFIRMED | Using QCEW annual-average 2020 as a pretrend baseline mixes in COVID shock volat... | sources/immigration-causal/scripts/build_county_outcome_panel.py anchors QCEW, chunk["qtr"] == "A" |
| 10 | INCONCLUSIVE | Overstated evidentiary level for real-vs-null search superiority | sources/immigration-causal/scripts/analyze_capacity_falsification.py exists; anchors not corroborated in resolved file context |
| 11 | INCONCLUSIVE | IRS migration measure may be temporally misaligned with the QCEW outcome windows | no file references or structured file anchors |
| 12 | CONFIRMED | Silent semantic failure in IRS migration zero-fill | sources/immigration-causal/scripts/build_county_outcome_panel.py anchors IRS |
| 13 | INCONCLUSIVE | Falsification memo uses vague pretrend language instead of reporting quantitativ... | research/immigration-capacity-falsification-2026-04-21.md exists; anchors not corroborated in resolved file context |
| 14 | INCONCLUSIVE | Memo-to-memo citation chains weaken source traceability | no file references or structured file anchors |
| 15 | CONFIRMED | Sparse application of framing-sensitivity tags | research/immigration-capacity-falsification-2026-04-21.md anchors FRAMING, SENSITIVE |
| 16 | CONFIRMED | IRS migration variable naming obscures the underlying tax-year timing | sources/immigration-causal/scripts/build_county_outcome_panel.py anchors IRS, us_inflow_persons_2022_23 |
| 17 | INCONCLUSIVE | Incomplete operationalization of rival explanations | research/immigration-capacity-falsification-2026-04-21.md exists |
| 18 | INCONCLUSIVE | Circular provenance in reasoning-evolution documentation | research/immigration-reasoning-evolution-2026-04-21.md exists; anchors not corroborated in resolved file context |
| 19 | INCONCLUSIVE | Tension between employment control survival and confounding claims | research/immigration-reasoning-evolution-2026-04-21.md exists |

