# Verified Disposition — 2026-04-22

**Claims:** 15 total — 11 CONFIRMED, 0 CORRECTED, 0 HALLUCINATED, 4 INCONCLUSIVE


| # | Verdict | Claim | Notes |
|---|---------|-------|-------|
| 1 | INCONCLUSIVE | Synthetic control is underdetermined and prone to severe overfitting | sources/immigration-causal/scripts/analyze_receiver_synthetic_controls.py exists; anchors not corroborated in resolved file context |
| 2 | CONFIRMED | Interference/Leakage in Donor Pool | sources/immigration-causal/data/outcomes/analysis/receiver_synth_weights.csv anchors CoC, NYC |
| 3 | CONFIRMED | `overall_to_hic_ratio` uses an endogenous denominator that can mask overload | sources/immigration-causal/scripts/analyze_receiver_synthetic_controls.py anchors CoCs, HIC, NYC, overall_to_hic_ratio |
| 4 | CONFIRMED | Donor pool is likely contaminated by quasi-treated migrant hubs | sources/immigration-causal/scripts/analyze_receiver_synthetic_controls.py anchors CoCs, NYC, receiver_synth_weights, receiver_synth_weights.csv |
| 5 | CONFIRMED | Placebo inference may be invalid if placebos are ranked by raw post-gap without ... | sources/immigration-causal/scripts/analyze_receiver_synthetic_controls.py anchors MSPE, RMSPE, receiver_synth_placebos, receiver_synth_placebos.csv |
| 6 | CONFIRMED | Inconsistent Placebo P-Value Filtering | sources/immigration-causal/data/outcomes/analysis/receiver_synth_placebos.csv anchors RMSPE |
| 7 | CONFIRMED | Memo conclusions rely on ratios and omit absolute sheltered/unsheltered count ch... | research/immigration-receiver-counterfactuals-2026-04-22.md anchors HIC, PIT, sheltered |
| 8 | INCONCLUSIVE | Temporal Misalignment of Post-Period Start | sources/immigration-causal/scripts/analyze_receiver_synthetic_controls.py exists; anchors not corroborated in resolved file context |
| 9 | CONFIRMED | Treatment timing is oversimplified despite PIT counts being annual January snaps... | sources/immigration-causal/scripts/analyze_receiver_synthetic_controls.py anchors HUD, PIT |
| 10 | CONFIRMED | Synthetic control specification omits structural covariates | sources/immigration-causal/scripts/analyze_receiver_synthetic_controls.py anchors CoCs |
| 11 | CONFIRMED | HUD PIT data are treated as neutral despite known instrument bias | research/immigration-receiver-counterfactuals-2026-04-22.md anchors HUD, PIT |
| 12 | INCONCLUSIVE | No in-time placebo falsification is reported | sources/immigration-causal/scripts/analyze_receiver_synthetic_controls.py exists; anchors not corroborated in resolved file context |
| 13 | CONFIRMED | Unified panel treats transit hubs and destination cities as causally identical | sources/immigration-causal/scripts/analyze_receiver_synthetic_controls.py anchors CoCs, NYC |
| 14 | CONFIRMED | Donor pool is not screened for unstable pre-treatment measurement artifacts | sources/immigration-causal/scripts/analyze_receiver_synthetic_controls.py anchors CoCs, PIT |
| 15 | INCONCLUSIVE | Strict Convex Hull Constraint Without Intercept | sources/immigration-causal/scripts/analyze_receiver_synthetic_controls.py exists; anchors not corroborated in resolved file context |

