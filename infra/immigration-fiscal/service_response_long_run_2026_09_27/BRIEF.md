# Brief: long-run responses for economic affairs and recreation, with the congestion interaction

Date 2026-09-27. Parent session immigration-research-1c, under the operator's delegation ("ok do what
you think is well reasoned and makes sense", 13:22 JST) and his note in the figures session (13:26 JST)
that economists miss "the full picture and Nth order consequences". The gap was raised by the figures
session.

## Why

The main case (`main_case_schools_full_2026_09_26`, $258.4885–291.9548bn) charges schools at full
average cost, the long-run cross-sectional reading (decision 2026-09-26-main-case-schools-full-cost).
Its profile `cbo_category_lag_non_school_full` still holds two lines at zero response under CBO's
short-run category lag (decision 2026-09-20-category-service-response): `economic_affairs_services`
($451.9bn nationally; about $36.3bn at the group's key) and `recreation_culture` ($54.3bn; about
$6.5bn). The engine applies `state.service_response * state.delayed_response` to the ids in
`model.service.delayed` (`assumption_explorer_2026_09_21/engine.js` line 135; `derived/model.json`).
That is the lag logic the schools decision dropped. The repo's own scaling test
(`research/immigration-service-scaling-test-2026-09-20.md`, table near line 100;
`administration_response_2026_09_20/derived/estimates.csv`) gives, across states with year
effects, 0.727 for nontoll highways and 0.948 for parks (within states 1.464 and 1.412, imprecise).

The same test gives financial/central administration 0.824, police 1.037, fire 1.085, libraries
0.974 and health 1.009; the main case already uses cross-state scale for general government.

## Scope

1. **Decompose the two lines.** Split `economic_affairs_services` and `recreation_culture` into their
   NIPA Table 3.17 subfunctions (state and local, and federal where the account's line includes it),
   using the account's own BEA inputs (find where the explorer's model builds these lines). Give each
   subfunction's national amount and its amount at the group's key.
2. **Map each subfunction to a long-run response.**
   - Use the scaling test's rows where a subfunction matches (nontoll highways, parks, libraries,
     central administration). Read each elasticity b over the removal, as the finite-removal decision
     does (`decisions/2026-09-26-main-case-finite-removal-and-consumption-key.md`):
     r = [1 − (1 − s)^b] / s at s = 0.120245.
   - Subfunctions with no matching row: state a rule and its reason. Examples: hold at 0 when spending
     is not population-driven (agriculture, natural resources, energy, space); take the nearest
     measured function when it is (transit, general economic and labor administration). Show every
     choice in a table.
   - Where the evidence gives two readings (across-state and within-state, finite and marginal),
     carry a low and a high response.
3. **The congestion interaction.** `congestion_2026_09_23/` prices road congestion ($19.2bn,
   $8.0–35.3bn) as a social cost beside the account because road budgets are fixed ("fixed lanes").
   If highway spending responds, the account must not charge both the spending response and the
   full fixed-lane congestion. Re-derive the congestion item with road capacity scaling consistently
   with the spending response, or bound it if capacity cannot be tied to spending, and report the net
   change (spending response plus congestion change). Read `ancestry_iv_congestion_wages_2026_09_23/`
   for the slopes it could and could not measure.
4. **Run the engine.** For each of the 64 specifications of the main case (`package.cjs`
   `MAIN_SPECS`, `cost()`), evaluate the case with the new responses for these lines through the
   engine's own state (set per line; if the engine only has one `delayed_response`, find a
   line-level route or split the line in a lane-local copy of the model, and gate that it reproduces
   the engine at the old responses). Report the candidate band (min and max over specifications) with
   its end specifications, and the move at fixed specifications. Never difference two bands' ends.
5. **Hand-off to the capital lane.** `capital_return_services_2026_09_27/` prices the return on public
   capital for every responsive line. Write the responses you settle on, per subfunction and band end,
   to `derived/responses.json` so that lane can price road and park capital consistently.

## Outputs (all inside this directory)

- Scripts (deterministic; stop with `[BLOCKED] …` and write nothing on a failed gate).
- `derived/`: subfunction table, response table with sources, per-spec costs, candidate band,
  congestion bridge, `responses.json`, `gates.json`.
- `RESULT.md` opening with `**Verdict:**`: the responses, the candidate main case, the congestion
  change, every judgment call and gap, and the files covered and skipped.

## Gates

- At the old responses the lane reproduces the main case, $258.4885–291.9548bn, to 1e-6 at every
  specification, and `node infra/immigration-fiscal/main_case_schools_full_2026_09_26/main_case.cjs`
  still ends "all gates passed".
- The subfunctions add to the account's two lines exactly.
- Two runs are byte-identical.

## Rules

- Do not commit, stage or stash. The checkout is shared with the figures session: touch nothing
  outside this directory (it owns `main_case_schools_full_2026_09_26/`, `school_capital_return_2026_09_26/`
  and `figures_2026_09_22/`).
- Primary sources only for numbers used in calculations (BEA NIPA 3.17, Census, the repo's pinned
  files); tag `[SOURCE]`, `[DATA]`, `[CALCULATION]`, `[INFERENCE]`, `[GAP]`.
- `csv.writer(..., lineterminator="\n")`. Never print the Census API key.
- Write `RESULT.md` early and update it as you go.
