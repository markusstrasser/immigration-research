claude-opus-5-5

**Verdict:** Letting roads, parks and economic administration respond in the long run raises the
main case from $258.49–291.95bn to a candidate **$277.93–321.59bn** a year (end specifications 48
and 11, unchanged). At fixed specifications the move is **+$19.44bn** at the low end and **+$29.63bn**
at the high end. State-local highways carry 62% of the low-end move ($11.98bn) and 55% of the
high-end move ($16.20bn). The congestion item beside the account falls from $19.16bn to $13.99bn
(low end) and $12.02bn (high end) once lanes shrink with highway spending. Account and congestion
together move **+$14.27bn / +$22.49bn**. The low end is the better-measured reading, and a land-area
control does not dislodge it. The high end rests on two things: within-state estimates capped at 1,
and federal budgets that respond by rule. With the across-state reading at both ends, the way the
main case treats general government, the candidate is $277.93–316.37bn.
[CALCULATION: `derived/candidate_band.json`, `derived/net_change.json`; lane result, proposed, not adopted]

Date 2026-09-27. Brief: [BRIEF.md](BRIEF.md). Frame unchanged: the complete annual account's
stationary 2024 comparison, main case `main_case_schools_full_2026_09_26` (profile
`cbo_category_lag_non_school_full`, where both lines sit at response 0 under CBO's short-run
category lag).

## Responses by subfunction

A response applies to the account's keyed amount of the line. Economic affairs uses the resources key:
the group holds 8.06% after the main case's corrections, $36.43bn of $451.9bn. Recreation uses the
population key: 11.72%, $6.37bn of $54.3bn. Elasticities are read over the removal,
r = [1 − (1 − s)^b] / s at s = 0.120245. National amounts are 2024 consumption, $bn.
[CALCULATION: `derived/response_table.csv`, `derived/subfunctions.csv`]

| Subfunction | National | Group, main case | Low end | High end | Rule and reason |
|---|---:|---:|---:|---:|---|
| S&L highways | 201.005 | 16.203 | 0.7392 | 1 | Nontoll highways across states 0.727 (low); within states 1.464 → 1.4225, capped at 1 (high) |
| S&L general economic and labor affairs | 29.358 | 2.367 | 0.8504 | 0.8504 | Administration: the main case's general-government response for state-local administration |
| S&L recreation and culture | 48.901 | 5.730 | 0.9512 | 1 | Parks across states 0.948 (low); within states 1.412 → 1.3759, capped at 1 (high) |
| Federal air | 30.604 | 2.467 | 0 | 1 | FAA operations and TSA screening scale with traffic; no air row, so the highway reading applies; federal budgets fixed at the low end |
| Federal general economic and labor affairs | 35.431 | 2.856 | 0 | 0.8504 | Same treatment as general government's federal part: fixed at the low end, the administration response at the high end |
| Federal highways; federal transit and rail | 1.827; 0.094 | 0.147; 0.008 | 0 | 1 | Nearest measured transport function |
| Federal recreation and culture | 5.430 | 0.636 | 0 | 1 | National parks and federal cultural agencies; parks reading |
| Federal water, space, agriculture, energy, natural resources | 18.209; 21.230; 17.540; 23.406; 32.036 | 9.062 together | 0 | 0 | Spending follows waterways, missions, farms and the resource base, not residents (the brief's rule) |
| S&L agriculture, natural resources | 10.007; 31.990 | 3.385 together | 0 | 0 | As above |
| Federal postal service; S&L commercial activities | −0.177; −0.625 | −0.065 | 0 | 0 | Enterprise nets |

Blended line responses (what the engine sets): economic affairs 0.3840 / 0.6386, recreation
0.8562 / 1. Contributions at the end specifications add to the moves: low end 11.98 + 2.01 + 5.45;
high end 16.20 + 2.01 + 5.73 + 2.47 + 2.43 + 0.64 + 0.15 + 0.01.
[CALCULATION: `derived/candidate_band.json` `contributions_at_end_specifications`]

**Why the high end reaches 1 and stops there.** Every within-state point estimate exceeds 1 in all
three sample windows: highways 1.46, 1.60 and 1.78; parks 1.41, 1.38 and 1.72. All are imprecise
(highways SE 0.49, 95% interval 0.48–2.45) [DATA: `scaling_test_2026_09_20/derived/state/estimates.csv`].
The account prices no line above 1. `cost()` holds public order and safety and health at 1 although
police (1.037), fire (1.085) and hospitals (1.374) scale above 1 across states, and the schools
decision records above-1 costs as an unpriced upside [DATA: `main_case_2026_09_24/package.cjs`
`cost()`; decisions/2026-09-26-main-case-schools-full-cost.md]. Priced uncapped, the within-state
readings would add $10.35bn at the high end.

**Why administration takes general government's responses.** General economic and labor affairs
covers labor departments, economic development, licensing, regulation, and statistical and commerce
agencies. Those are administration. The account already has an adopted response for administration:
0.8504 for state and local government at both ends, and the federal part fixed at the low end
(decisions/2026-09-23-main-case-general-government-and-use-keys.md). The within-state administration
estimate (0.471) is the one that decision judged unable to tell zero from one. The scaling test's
panel estimate, 0.824 (r 0.836), would move the result by −$0.03bn.

## Disconfirmation: is the across-state highway slope geography?

Small-population states include large, sparse ones with long road networks per resident. The group's
removal would take residents out of existing states without changing their land. So the across-state
0.727 could overstate scale economies. I refitted the scaling test's own model (it reproduces
0.726607 exactly) with log land area added, using the 2020 Census Gazetteer, ALAND summed by
state. The population slope falls to **0.690** (SE 0.044) for highways and 0.917 for parks, and
administration is unchanged (0.825). Land has its own positive effect (0.16), and population and land
are only weakly correlated (0.20). The across-state reading is not a land artifact. If anything, a
removal at fixed land saves slightly less (r 0.703 instead of 0.739, −$0.6bn at the low end). The
low end is kept at the scaling test's published estimate.
[CALCULATION: `land_check.py` → `derived/land_check.csv`; SOURCE: https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2020_Gazetteer/2020_Gaz_counties_national.zip]

## The candidate and its alternatives

| Construction | Band, $bn | Move at fixed specifications (low / high) | Congestion beside | Net with congestion |
|---|---:|---:|---:|---:|
| Main case (reproduced) | 258.49–291.95 | — | 19.16 (B1, lanes fixed) | — |
| **Candidate (brief's rule)**: low readings at the low end, high at the high end | **277.93–321.59** | +19.44 / +29.63 | 13.99 / 12.02 | +14.27 / +22.49 |
| Across-state readings at both ends; only the federal treatment differs (as general government) | 277.93–316.37 | +19.44 / +24.41 | 13.99 / 13.99 | +14.27 / +19.24 |
| Low responses throughout (federal fixed, across-state) | 277.93–311.40 | +19.44 / +19.44 | 13.99 | +14.27 |
| High responses throughout | 288.12–321.59 | +29.63 / +29.63 | 12.02 | +22.49 |

The move is the same at every one of the 64 specifications for a given reading: +19.47 / +29.68 in
fill-in method `b_hotdeck_union_matched`, +19.41 / +29.58 in `b_matched_over_pooled`. The only
difference is the group's keyed amount of the line ($36.51bn against $36.35bn). The two allocation
conventions give the same amount. [CALCULATION: `derived/per_spec_costs.csv`]

Sensitivities at the end specifications [CALCULATION: `derived/candidate_band.json`
`sensitivities_at_end_specifications`]:

| Change | Low end | High end |
|---|---:|---:|
| Measured responses taken as r = b (marginal) instead of the finite removal | −0.24 | −0.04 |
| Within-state readings priced above 1 (the unpriced upside) | 0 | +10.35 |
| Federal subfunctions fixed at the high end too | 0 | −5.69 |
| S&L highways and parks at the across-state reading at the high end | 0 | −5.22 |
| Every held-at-0 subfunction at 1 instead (water, space, agriculture, energy, natural resources) | +12.38 | +12.38 |
| Within-state administration 0.471 (r 0.487) for S&L general economic and labor at the low end | −0.86 | 0 |

## Congestion

The congestion lane's B1 is Couture–Duranton–Turner's speed regression across 100 MSAs (table 10
column 6): population −0.12 (SE 0.035), lanes 0.066 (SE 0.038). With lanes fixed it gives
$19.16bn. With lanes shrinking by c,
ln C₀ = 0.12 ln(1 − s_i) − 0.066 ln(1 − c) [SOURCE: CDT working paper, lane `_cache/cdt_speed_2016_hal.firecrawl.md`].
The lane's own keyed variant, lanes cut by the 8.10% key, gives $11.98bn. Both reproduce exactly,
along with B1's factorial range of $8.05–35.25bn [CALCULATION: `congestion.py`, gates].

Capacity is tied to spending as c = κ × h × k. Here h is the highway response (S&L and federal
highways, amount-weighted: 0.7325 at the low end, 1 at the high end), k is the group's key share at
the end specification (0.0806), and κ is the elasticity of lane capacity with respect to highway
spending. Highway consumption is the maintenance, operations and depreciation of the network, so
κ = 1 is central [INFERENCE]. κ = 0 is the bound where the saving comes from maintaining an unchanged
network: congestion then stays at $19.16bn and the net change is the account move alone.

| Band end | Lane cut | Congestion, central (factorial range) | Change vs B1 | Cut where the group lives instead |
|---|---:|---:|---:|---:|
| Low | 5.91% | $13.99bn ($2.01–32.05bn) | −$5.17bn | $14.69bn (−$4.47bn) |
| High | 8.06% | $12.02bn (−$0.92–30.83bn) | −$7.14bn | $12.85bn (−$6.31bn) |

[CALCULATION: `derived/congestion_bridge.csv`] The factorial adds the lanes coefficient ±1 SE to the
lane's B1 factors. Its lower tail goes negative at the high end: with a large lanes coefficient, an
8% smaller network without the group would slow others more than the group's traffic does. The
ancestry-IV lane measured neither slope: its instrument does not move metro population (first-stage
F 1.4–1.9), so B1 stays borrowed from CDT, and nothing in the repo measures κ [DATA:
`ancestry_iv_congestion_wages_2026_09_23/RESULT.md`]. The congestion lane also noted pavement wear on a
fixed maintenance budget as an unpriced cost of the zero-response assumption. Under a responding
highway budget that cost no longer arises.

## How the lines were split

Table 3.17 gives consumption by function and level but not by subfunction. Table 3.16 gives current
expenditures by subfunction. Consumption by subfunction is 3.16 less the social benefits, grants and
subsidies that 3.17 gives by function and subfunction. [DATA: pinned BEA Section 3 workbook, sha256
69b5c7ae…, `derived/gates_build.json` lists every cell used]

- **State and local.** S&L economic affairs is exactly consumption + benefits + subsidies
  (273,825 = 271,735 + 1,377 + 713, $m). The benefits are Table 3.12's employment and training
  (1,377, exact), taken off general economic and labor affairs. The subsidies (713) equal S&L transit
  and rail current expenditure, since transit is a government enterprise with no consumption. S&L air
  and water have no 3.16 line (enterprises). The published rounding (+1) sits on highways.
- **Federal.** Grants by transport mode come from consolidation: government = federal + S&L − grants.
  That gives highways 0, air 0, water 175 and transit 100. The same identity reproduces 3.17's
  published grants for the other subfunctions (7,712 against 7,713; the rest exact).
- **Assignment 1.** The $10.1bn federal transportation subsidy (Amtrak) goes to transit and rail. At
  least $9.6bn must go there, because federal transit consumption plus investment is only $572m
  (3.15.5). At most $0.48bn could belong to air or water, which changes the result by under $0.04bn.
- **Assignment 2.** The unallocated federal residual of $10.152bn is economic-affairs benefits (7,497)
  plus other current transfers (2,655, federal only). It goes to general economic and labor affairs.
  At least $5.3bn must go there, or that subfunction's implied investment turns negative. Placing only
  the minimum there would raise the high end by at most $0.33bn.
- Implied gross investment (3.15.5 less consumption) is non-negative in every subfunction, with a
  minimum of $463m. The rows add to 451,935 and 54,331 exactly.

## Gaps

- **[GAP] The high end is a rule, not a measurement.** The within-state estimates are imprecise and
  plausibly confounded by state revenue shocks and income growth [INFERENCE]. Federal responses have
  no measured row.
- **[GAP] Key.** The line's resources key gives the group 8.06% of highways. Its traffic share is
  10.8% nationally (congestion lane). A traffic key would raise the S&L highway charge by about a
  third. The account's key convention is not changed here.
- **[GAP] Capital return.** NIPA consumption includes depreciation but no return on public capital.
  `capital_return_services_2026_09_27` prices that return at these responses, from
  `derived/responses.json`. It is not in the candidate.
- **[GAP] κ**, the link from spending to lane capacity, is assumed (1 central, 0 bound).
- **[GAP] Range.** The main case's outer range ($198–324bn) was not recomputed on the candidate.
  The sensitivities above are the new components.
- Not covered: the other two service profiles (fixed non-school education; the proportional
  reference, which already charges these lines at 1), transit crowding and parking, and the
  government-enterprise surplus on the receipts side (S&L transit's operating deficit sits there,
  not in consumption).

## Hand-off: `derived/responses.json`

`meta` holds s, the rule and the band ends. `lines.<line_id>` holds `national_bn`, `key`,
`key_share_uncorrected`, `main_case_response` (0), `response` {low, high} (the blend the engine sets
through `state.response_override[line_id]`), and `subfunctions[]` with {id, level, subfunction,
national_bn, share_of_line, response {low, high}, basis}. Low responses apply at the candidate's
low-end specification (48) and high responses at its high end (11). The group's amounts at those
specifications are in `derived/candidate_band.json` → `group_amounts_at_end_specifications_bn`.

## Validation

- `build.py`: 30 gates. BEA pin; the account's lines are 3.17 lines 5 and 8; the NIPA identities
  above; investment ≥ 0; the subfunctions add exactly. The finite-removal formula reproduces the
  main case's general-government response 0.8503957662 exactly.
- `engine.cjs`: 13 gates.
  - At the old responses the lane's cost function equals the package's `cost()` exactly at all 64
    specifications × 2 methods, and the band is $258.488495–291.954773bn (summary.json, 1e-6).
  - The split-line model, where each line is split into its subfunctions, agrees with the blended
    responses to 1.1e-13, as does the linear path of package cost + response × group amount.
  - The end specifications stay 48 and 11.
- `land_check.py`: 6 gates. It reproduces the scaling test's estimates to 1e-12.
- `congestion.py`: 6 gates. It reproduces B1 ($19.162711bn), B1's factorial range and the keyed
  proportional variant ($11.978123bn).
- All four scripts run twice give byte-identical `derived/` (13 files).
- `node infra/immigration-fiscal/main_case_schools_full_2026_09_26/main_case.cjs` ends "all gates
  passed" (15 PASS, 0 FAIL), and its `derived/` files are byte-identical before and after.

## Files

Created in this directory: `build.py`, `engine.cjs`, `land_check.py`, `congestion.py`, this
`RESULT.md`. In `derived/`: `subfunctions.csv`, `response_table.csv`, `responses.json`,
`per_spec_costs.csv`, `candidate_band.json`, `land_check.csv`, `congestion_bridge.csv`,
`net_change.json`, `gates_build.json`, `gates_engine.json`, `gates_land.json`,
`gates_congestion.json`, `gates.json`. In `_cache/` (ignored): `2020_Gaz_counties_national.zip`
(sha256 02ef546e…). Nothing outside this directory was written. The congestion lane's `arms.py` is
imported and its `_cache/` and `derived/` read, never written.

Note: the brief points to `administration_response_2026_09_20/derived/estimates.csv` for the
highway and park rows. That file holds only administration rows. The rows quoted in the memo are in
`scaling_test_2026_09_20/derived/state/estimates.csv`, which this lane reads.

## Reproduce

```sh
# from the repository root, in this order
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/service_response_long_run_2026_09_27/build.py
node infra/immigration-fiscal/service_response_long_run_2026_09_27/engine.cjs
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/service_response_long_run_2026_09_27/land_check.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/service_response_long_run_2026_09_27/congestion.py
```
