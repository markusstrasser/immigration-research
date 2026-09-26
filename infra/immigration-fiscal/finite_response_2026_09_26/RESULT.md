**Verdict:** [2026-09-26, later: adopted together with the consumption key in
`main_case_2026_09_26` ($200.9–245.7bn; decision
`decisions/2026-09-26-main-case-finite-removal-and-consumption-key.md`). The text below is the
proposal as sized.] The main case uses two sets of elasticities as the share of average cost a removal
saves: general government at 0.59–0.84 (cross-state scale elasticities) and schools at 0.63–0.66
(CBO's growth-rate coefficients, "to first order"). For a power-law cost, removing a group that is
12% of residents and 17.5% of pupils saves more than the elasticity: r = [1 − (1 − s)^b] / s.
Read that way, the adopted **$200.9–246.3bn becomes $205.0–249.7bn (+$4.1bn / +$3.4bn)**. Schools
carry most of it (+$3.7 / +$3.0bn); general government adds +$0.37 / +$0.39bn net. **Proposed, not
adopted**: under a fixed-plus-constant-marginal cost r equals b and nothing changes, and one
standard error on the administration elasticity moves general government by $1.2–1.9bn, more than
this correction. Composed in one engine run with the consumption-key proposal (ladder 225,
−$4.1bn), the main case is **$200.9–245.7bn**, which rounds to the published $201–246bn (run K).
[CALCULATION: `r_values.py` → `derived/r_values.json`; `runner.cjs` → `derived/runs.json`]

# Finite-removal responses in the adopted main case

Date: 2026-09-26. Trigger: the [weekly conceptual audit](../../../research/immigration-weekly-conceptual-audit-2026-09-25.md)
("marginal elasticity versus finite removal") and the
[decision](../../../decisions/2026-09-25-weekly-audit-corrections.md) to size it separately. The
[service-scaling memo](../../../research/immigration-service-scaling-test-2026-09-20.md) derived
r = [1 − (1 − s)^b] / s on September 20 and noted that only infinitesimal changes give r = b.

## What the main case uses

- **General government.** `main_case_2026_09_24/package.cjs` applies `scaling_check.json`'s
  composite (0.59 low, 0.84 high) as the response of the engine line `general_public_services`
  ($401.6bn; $48.3bn at full response on the group's population key). The composite is a
  spending-weighted mean of 50-state log-log elasticities: state and local at the administration
  elasticity 0.842, federal tax collection at financial administration 0.789, and at the low end the
  federal executive and legislature fixed at 0. The key is national, so a state-share version is
  not defined in the engine.
- **Schools.** 0.63 and 0.66 are 1 − 0.37 (growth) and 1 − 0.34 (decline) from CBO's state panel
  of per-pupil spending growth on enrollment growth (`full_account_2026_09_20/service_response.py`,
  `school_response_derivation`; [evidence note](../../../notes/immigration-service-response-external-evidence-2026-09-20.md)).
  A growth-rate coefficient is a first-order elasticity. The group holds 8.487m of 48.551m pupils
  (s = 0.1748, `school_cost_where_enrolled_2026_09_24/derived/account_embedded_price.json`).
- **Dependent constant.** Dataset-audit row 8 charges unallocable state and local spending at the
  all-spending elasticity 0.962 instead of 0.842; under r its increment shrinks by 0.949.

| Response | Stored | b unrounded | r, national s 0.1202 | r, engine key s 0.1215 |
|---|---:|---:|---:|---:|
| General government, low | 0.59 | 0.5939 | 0.6000 | 0.6001 |
| General government, high | 0.84 | 0.842 | 0.8504 | 0.8505 |
| Schools, growth (s = 0.1748) | 0.63 | 0.63 | 0.6522 | |
| Schools, decline (s = 0.1748) | 0.66 | 0.66 | 0.6813 | |

At component level the low end is 0.600, not the audit's 0.605, because the fixed federal component
stays at zero.

## Runs, central band, $bn a year

| Run | Low | High | Δ low | Δ high |
|---|---:|---:|---:|---:|
| A: adopted, reproduced (gate: to 1e-4 of `main_case_bands.csv`) | 200.8752 | 246.3184 | 0 | 0 |
| B: general government at unrounded b (rounding only) | 201.0596 | 246.4126 | +0.18 | +0.09 |
| C: general government finite r, national s | 201.3480 | 246.8076 | +0.47 | +0.49 |
| D: same, engine key s | 201.3510 | 246.8118 | +0.48 | +0.49 |
| E: row 8 finite | 200.7735 | 246.2168 | −0.10 | −0.10 |
| I: general government only (C + E) | 201.2463 | 246.7060 | +0.37 | +0.39 |
| F: schools finite r, s 0.1748 | 204.5987 | 249.3591 | +3.72 | +3.04 |
| G: schools, s 0.16 | 204.2571 | 249.0806 | +3.38 | +2.76 |
| H: schools, s 0.18 | 204.7198 | 249.4578 | +3.84 | +3.14 |
| **J: all (C + E + F)** | **204.9697** | **249.7466** | **+4.09** | **+3.43** |
| L: consumption key alone (ladder 225, `both_corridor_net_h2`), payload path | 196.8235 | 242.2667 | −4.05 | −4.05 |
| **K: J with the consumption key, one engine run** | **200.9180** | **245.6949** | **+0.04** | **−0.62** |

The outer range ($172–276bn) was not recomputed; its ends move by about the central shift.

K and L go through the corrections payload, as `consumption_key_2026_09_24/engine_run.cjs`
composes it: `package.cjs`'s `correctionsPayload()` with the lane's receipt edits appended. The
same path first reproduces A and J to 1e-3, and L matches the consumption lane's own
$196.823–242.267bn. The key's edits are receipt-side and the finite responses act on spending
lines, so K is the sum of the two changes. **Adopted together, the two proposals leave the main
case at $200.9–245.7bn, which rounds to the published $201–246bn.** Adopting only one of them moves
the headline by about $4bn, up for this lane and down for the consumption key.

## Limits

- **The functional form decides the correction.** The power law is the form that log-log and
  log-change estimates imply, and the repo's own derivation uses it. A fixed cost plus a constant
  marginal cost gives r = b. Neither form is measured over a 12–17% removal.
- **The elasticities' uncertainty is larger.** Administration 0.842 (SE 0.039) and financial
  administration 0.789 (0.052) are cross-sectional scale estimates; CBO's school coefficients are
  short-run and "not a causal long-run estimate".
- **School dilution.** The dilution lane (ladder 222) prices the part of school cost left free at
  0.63–0.66. At 0.652–0.681 that part is about 6% smaller, and the $16.1bn beside the account would
  shrink roughly in proportion. Not recomputed. [INFERENCE]
- The shelter constant keyed to 0.59/0.84 moves by about −$0.002bn and is held fixed.

## Reproduce

```sh
cd infra/immigration-fiscal/finite_response_2026_09_26
uv run --no-project python3 r_values.py   # -> derived/r_values.json
node runner.cjs                           # -> derived/runs.json; exits 1 unless run A reproduces the adopted case
```

`runner.cjs` imports `main_case_2026_09_24/package.cjs` as `sign_reversal.cjs` does and changes its
specs in memory only. Importing the package re-vendors the CPS stack file; when the CPS cache has not
drifted it writes identical bytes, and `git status` on the main-case lane stays clean.

Sizing by a lane worker on 2026-09-26 (self-report `claude-opus-5-5`), rebuilt in the repo and
rerun by the parent; the repo runs match the worker's scratch runs exactly.
