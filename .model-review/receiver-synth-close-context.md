## Scope
- Target users: personal research repo producing public-facing empirical memos
- Scale: currently 5 treated receiver nodes against a 2018-2024 national CoC donor universe of roughly 370 complete donor CoCs; designed-for scale is small-N treated-case causal analysis, not a general platform
- Rate of change: new immigration artifacts can arrive daily during an active research cycle; this packet targets the 2026-04-22 receiver-counterfactual tranche only

## Constitution
- Truth convergence beats volume.
- Source everything.
- Disconfirmation is mandatory.
- Quantify when possible.
- Politically charged topic: do not assume a neutral instrument.

## Review target
Close-review the new receiver-counterfactual tranche only:

1. `sources/immigration-causal/scripts/analyze_receiver_synthetic_controls.py`
2. `research/immigration-receiver-counterfactuals-2026-04-22.md`
3. `sources/immigration-causal/data/outcomes/analysis/receiver_synth_yearly.csv`
4. `sources/immigration-causal/data/outcomes/analysis/receiver_synth_summary.json`
5. `sources/immigration-causal/data/outcomes/analysis/receiver_synth_weights.csv`
6. `sources/immigration-causal/data/outcomes/analysis/receiver_synth_placebos.csv`

## What changed

This tranche:

1. built a national `HUD HIC/PIT` CoC panel for `2018-2024`
2. fit simplex-constrained synthetic-control style donor weights for `NYC`, `Denver`, `Boston`, `Chicago`, and `Bexar`
3. estimated post-2022 gaps for:
   - `sheltered_to_hic_ratio`
   - `overall_to_hic_ratio`
4. computed national donor placebos
5. wrote a memo that explicitly says the synthetic controls are directional and not decisive

## Claimed results to challenge

1. `Denver` is the clearest positive physical-overload divergence case.
2. `NYC` diverges strongly on `sheltered/HIC` but not on `overall/HIC`.
3. `Boston` and `Chicago` do not survive as simple positive shelter-divergence cases.
4. placebo rankings are too weak/noisy to count as decisive proof.

## Review questions

1. Is there any donor-pool leakage, especially accidental inclusion of treated or quasi-treated CoCs?
2. Is the synthetic-control construction mathematically or statistically broken?
3. Are the placebo p-values or filtered comparisons still misleading?
4. Are the memo claims stronger than what the outputs actually support?
5. Are there obvious better comparators or hidden data bugs that would overturn the main directional conclusions?
