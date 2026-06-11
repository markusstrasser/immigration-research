# Verified Disposition — 2026-04-22

**Claims:** 20 total — 9 CONFIRMED, 0 CORRECTED, 0 HALLUCINATED, 11 INCONCLUSIVE


| # | Verdict | Claim | Notes |
|---|---------|-------|-------|
| 1 | CONFIRMED | "Pre-trend" placebo uses a post-treatment, endogenous permit denominator | sources/immigration-causal/scripts/analyze_capacity_falsification.py anchors permit_units_2021_2024, prepare, recent_fb_per_permit_unit, wage_log_change_2021_2022 |
| 2 | CONFIRMED | 2021–2022 is mislabeled as a placebo/pre-trend window | sources/immigration-causal/scripts/analyze_capacity_falsification.py anchors wage_log_change_2021_2022 |
| 3 | CONFIRMED | Invalid placebo/pre-trend semantics | sources/immigration-causal/scripts/analyze_capacity_falsification.py anchors permit_units_2021_2024 |
| 4 | CONFIRMED | Threshold stability metric uses median instead of original estimate | sources/immigration-causal/scripts/analyze_capacity_falsification.py anchors share_same_sign |
| 5 | INCONCLUSIVE | Acceleration null is misinterpreted as evidence against an effect | research/immigration-reasoning-evolution-2026-04-21.md exists; anchors not corroborated in resolved file context |
| 6 | INCONCLUSIVE | Causal downgrade in falsification memo is premature because it relies on flawed ... | research/immigration-capacity-falsification-2026-04-21.md exists; anchors not corroborated in resolved file context |
| 7 | INCONCLUSIVE | Over-claimed 'Real Threshold Family' without null benchmark | sources/immigration-causal/scripts/analyze_capacity_falsification.py exists; anchors not corroborated in resolved file context |
| 8 | CONFIRMED | Permutation test resolution is too low and reported p-value is falsely precise | sources/immigration-causal/scripts/analyze_capacity_falsification.py anchors PERMUTATIONS, PERMUTATIONS = 300 |
| 9 | CONFIRMED | Silent exclusion of zero-permit counties | sources/immigration-causal/scripts/analyze_capacity_falsification.py anchors NaNs |
| 10 | INCONCLUSIVE | Coarse permutation inference and missing multiplicity adjustment | sources/immigration-causal/scripts/analyze_capacity_falsification.py exists; anchors not corroborated in resolved file context |
| 11 | INCONCLUSIVE | Lack of uncertainty intervals for split-share and permutation metrics | no file references or structured file anchors |
| 12 | CONFIRMED | State-level leave-one-out is too weak for geographically clustered shocks | sources/immigration-causal/scripts/analyze_capacity_falsification.py anchors LOSO, leave_one_state_out |
| 13 | INCONCLUSIVE | Mislabeling of exploratory findings as causal evidence | research/immigration-capacity-falsification-2026-04-21.md exists |
| 14 | INCONCLUSIVE | True pre-trend outcome windows are missing from the panel build | sources/immigration-causal/scripts/build_county_outcome_panel.py exists; anchors not corroborated in resolved file context |
| 15 | INCONCLUSIVE | Reasoning-evolution doc lacks artifact provenance | research/immigration-reasoning-evolution-2026-04-21.md exists; anchors not corroborated in resolved file context |
| 16 | CONFIRMED | Recent foreign-born numerator may blur the treatment window via ACS rolling aver... | sources/immigration-causal/scripts/analyze_capacity_falsification.py anchors annual_recent_fb_persons, recent_fb_annual_share |
| 17 | CONFIRMED | Threshold validation likely leaks target information and overstates threshold st... | sources/immigration-causal/scripts/analyze_capacity_falsification.py anchors threshold_validation |
| 18 | INCONCLUSIVE | Missing framing-sensitivity tags on policy claims | research/immigration-capacity-falsification-2026-04-21.md exists; anchors not corroborated in resolved file context |
| 19 | INCONCLUSIVE | Missing LLM-bias disclosure | no file references or structured file anchors |
| 20 | INCONCLUSIVE | Insufficient steel-manning of alternative explanations | research/immigration-capacity-falsification-2026-04-21.md exists |

