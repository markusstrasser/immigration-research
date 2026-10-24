claude-opus-5-5

**Verdict:** candidate v10, built on the committed rate lane (1a18b174, `rate_model.json` sha256 `92c332e48bd6`);
not adopted. The case is **$383.0–441.4bn** counting promises as earned (set) and **$299.4–357.7bn** counting
benefits when paid (cash), against v9's $368.0–436.6bn and $284.4–352.9bn. The joint change from v9 is
**+$15.017 / +$4.819bn** at the two ends, in set and cash alike. It breaks down as:

- item 22 (capital rate bounded over θ) +$14.356 / +$4.246bn;
- item 23 (K-12 capital where enrolled) +$0.543 / +$0.542bn (high end moved one unit so the parts add);
- order dependence +$0.118 / +$0.031bn, because item 22's rate prices item 23's return part.

[CALCULATION: summary.json v10.band_bn, v10.cash_set_bn, v10.change_by_item, v10.interactions]

**Cross-check against the rate lane.** The rate lane's bound, v9 plus item 22 on its own approximate line split, is
$382.250–440.760bn set (item 22 +$14.220 / +$4.199bn). v10 prices item 22 in-run at +$14.356 / +$4.246bn, so
the gap is **+$0.136 / +$0.047bn**, the same sign and size as the earlier +0.120 / +0.043. It comes from where the sub-rows sit. v10 prices
each completion carrier and coverage part at its parent component's level (coverage of highway capital at the
highway rate). The rate lane's map lists `capital_reporter` and `capital_coverage` as their own components at
`state_local`. Moving those sub-rows to `state_local` would shift item 22 by −$0.152 / −$0.052bn, leaving
−$0.016 / −$0.005bn, the lane's approximate split of the remaining lines.
[CALCULATION: rate_model.json theta_pairing.bound.set.rate_delta_bn; corrections.json meta.items
capital_rate_theta_bound post_engine_by_end rows]

**Scratch-rate reproduction (logged check).** Before the rate lane landed, a scratch copy of the then-committed rate
file (sha256 `4cbde717b446`) added the brief's level map. On it, item 22 alone reproduced b1cbb824's committed
+$13.038 / +$3.888bn (13.038477164561849 / 3.8876668079193664 against 13.038477164561868 / 3.887666807919402). The
scratch path is gone from code and `run_all.sh`; the check stands in the log (20:34 JST). The real rates raise
item 22 by +$1.318 / +$0.358bn over the scratch build; the rate lane's own bound moved +$1.301 / +$0.355bn.

**Components the lane's map lacks.** The map covers all 28 central capital components; the unit test checks this.
v10 places these on a parent or declared level:

- completion carriers, coverage, college, count and health sub-rows ride on their parent component's level.
  The map's `capital_reporter` and `capital_coverage` entries (`state_local`) are therefore not read.
- The nine components the inherited capital-definition range variants add are `eq_college_sl`, `eq_pos_sl`,
  `eq_health_sl`, `eq_gps_sl`, `eq_income_security_sl`, `eq_pos_fed`, `eq_gps_fed`, `eq_income_security_fed` and
  `gps_sl_row8_increment`. Each takes the level its source declares, and seven of the nine have a parent whose
  mapped level it must match. They are used only in the "inherited range variants" phase, never the band
  (Upstream issue 1). Any other unmapped component stops `[BLOCKED]`.

Item 24 (where-used prices) stands beside the band as not identified. With it, the case would be $382.3–440.7bn,
a change of −$0.757 / −$0.691bn. Item 25 (land) stays off and pending.

The ancestry-share readings:

- [FRAMING-SENSITIVE] G4+ at nothing: $258.9–300.7bn (v9 $248.7–297.4bn);
- [FRAMING-SENSITIVE] G4+ at its bound: $310.9–359.6bn (v9 $298.8–355.7bn).

All other v9 companions are re-derived with the v10 terms. The end specifications are still 16 / 11. Nothing
failed. [CALCULATION: summary.json v10.companions]

## Review findings: verification and changes

The blind review (`scratchpad/v10review/review.md`) listed ten findings. I checked each against the code and the files.

| # | finding | verified | what changed |
|---|---|---|---|
| 1 | The payload keeps `meta.one_rate.flat_real_equivalent`, and the new items have no `post_engine_by_end`, so a flat-rate reader drops item 22 | yes (field present at b1cbb824; new records had `parts: {}`) | `flat_real_equivalent` is removed whenever item 22 is on, with a note in `meta.one_rate.v10`. `meta.v10.rates` publishes `level_by_component`, `rate_by_level_by_end`, `end_index` and `case_rate`. Each new `meta.items` record has `post_engine_by_end.{low,high}` in v9's shape, adding `by_method.{m}.{total_bn, parts, rows}`. `api_check.cjs` (446 checks) shows that a flat-rate reader stops, and that item 22 priced from the payload alone (parts × `meta.v10.rates`) equals the record. |
| 2 | Ancestry-share companions missing | yes | `generation.cjs` routes the v10 sub-rows by generation as `v9_split.cjs` does, and `ancestry.cjs` adds them, weighted by ancestry share, to v9's per-specification ancestry costs. Results are in the companions table, with the generation split at the ends in `ancestry.json` `generation_at_ends`. The reviewer's estimate (+$9.0 / +$2.6bn and +$10.6 / +$3.1bn) fell short at the high end: the computed changes are +$9.2 / +$3.1bn and +$11.1 / +$3.6bn. |
| 3 | Enterprise debt share and federal aid outside highways are unpriced | upstream premise, not a v10 defect | Measured in the rate lane (1a18b174): transit and airports get their own levels from federal grant shares (38.6%, 30.7%), and enterprise debt shares replace the flat 21%. v10 takes them through `level_by_component` / `rate_by_level_by_end` with no code change; item 22 moves from +$13.038 / +$3.888bn to +$14.356 / +$4.246bn. |
| 4 | Item 24 adopts a not-identified college proxy | yes (source verdict: "not identified") | Item 24 moved beside the band, as the companion `where_used_prices_beside`, with its parks and college parts at v10's rates (table). `BESIDE = [24]`, and `CANDIDATE` excludes it. Item 23 is kept. |
| 5 | The item 25 loader cannot read r2 and defaults to a ratio of 1 | yes | The ratio per line and variant is `group_weighted_value_<v>_bn` / `value_<v>_bn`, and any line that lacks one stops. The r1 test passes an explicit per-line override (K-12 recovered, other lines 1) and still matches all 102 r1 charges. Item 25 stays off. |
| 6 | In year one, item 24's parks base keeps untransported coverage and count parts | yes (the reviewer measured −$0.0064 / −$0.0074bn) | `parkRows` multiplies coverage parts by response ÷ source response and count parts by response ÷ the central run's response, as `companionPost` does. Item 24 in year one is now 0.000 / 0.000, gated per method. Items 22 and 23 were checked for the same pattern. Item 22 charges no capital in year one. Item 23's year-one depreciation uses the matched long-run K-12 key moved by the education response ratio and reads no coverage or count parts, so neither needed a change. |
| 7 | The candidate payload claims v9's adoption | yes | `meta.adopted` is null, `meta.decision` null, `meta.source` is `main_case_2026_10_24/package.cjs`, and `meta.status` is "candidate: main case v10" (unit-tested and api-gated). |
| 8 | v9's output contract is not preserved | yes (5 files against 22) | v10 now writes `main_case_bands.csv`, `components.csv`, `lineage_payload*.json`, `sign_reversal.csv`, `per_spec.csv` (v9's 95 columns plus 41 new) and `per_spec_cash.csv`. The summary adds per-member figures with and without coverage people, the `one_rate` replacement, `beside`, `coverage`, each companion's population and `carried_rows`. `contract.cjs` (G2) compares nine v9 files and passes with six negative probes. The thirteen v9 files not written are listed with reasons in `contract.cjs`. One is `lineage_addition.json`, a named gap: it is not recomputed for v10. |
| 9 | Gates that cannot fail | yes, each one named | Removed: the rate-lane replica, standalone = in-run delta, the 23+24 combined oracle, "item 25 off by default", and the year-one parks gate that I had briefly made always true. `test_lane`'s postEngine tautology became a raw-engine route, and its divisor test now reads the school lane's `r_embedded_account`. Added as independent checks: `check_item22.py`, which recomputes item 22 in Python on all 256 rows from `per_spec*.csv` pieces and the rate file; payload-only item 22 pricing; and sign-reversal checks, namely that v10-off reproduces v9's 16 printed cells and that the college and health fold changes welfare by the right amount. |
| 10 | Small items checked and found correct | rechecked | Still true: items 22 and 24 are zero in year one, cash equals set for every v10 term, and the interactions close (higher order 0). |

## Items

All terms are post-engine. v10 adds no engine edits and no people, so the payload model, edits and population are
v9's (gated). `items.cjs` `post()` derives each term inside the run it prices, from the v9 evaluator's own capital
components. Following item 20, those include union-completion capital carriers, own coverage capital parts, the item
16/17 count parts, item 15's college capital and item 21's health capital. At the case rate, the pieces add to the
capital implied by v9's 7% arm to 1e-9 at both ends.

| item | status | rule | source (read-only) |
|---|---|---|---|
| 22 `capital_rate_theta_bound` | in the band | Each capital piece that item 20 prices at 2.0810698764% is repriced at `rate_by_level_by_end[level_by_component[component]][end]`: θ = 1 at the low end, θ = 0 at the high. An unmapped component, or a rate file missing either key, stops `[BLOCKED]`. Item 6 is unchanged. | `public_capital_rate_2026_10_24/derived/rate_model.json` `theta_pairing.bound` |
| 23 `k12_capital_where_enrolled` | in the band | The K-12 return is multiplied by (F_stock/k − 1), and national K-12 depreciation by the run's K-12 capital key times (F_structures/k − 1) and (F_equipment/k − 1), with k = 1.0341917412, the embedded preferred school price. The return part moves with item 22's rate; depreciation does not. | `school_capital_where_enrolled_2026_10_24/derived/summary.json`; k from `user_fee_allocation_2026_10_07/derived/fee_lines.json` |
| 24 `where_used_prices` | beside, not identified | Parks: the run's recreation operating amount × the state/local parks share × the matched municipal bridge index change, with coverage and count parts transported in year one. Colleges: the college capital pieces at v10's rates × the higher-education fraction × (gross-book factor − 1). | `where_used_prices_2026_10_24/derived/{parks.json, college_factors.csv}` |
| 25 `public_land` | off, pending | Land value × group ratio × the line's full-return coefficient at item 22's rate, with no depreciation. | the lane named by `V10_LAND_LANE` (r2 schema) |

<!-- tables:start (write_result.py) -->
### Band [CALCULATION: summary.json v10.band_bn, v10.cash_set_bn, v10.v9_band_bn, v10.v9_cash_set_bn]

| | low $bn | high $bn |
|---|---:|---:|
| v9 (oct16), set | 368.0 | 436.6 |
| v10 candidate (oct24), set | 383.0 | 441.4 |
| v9 (oct16), cash | 284.4 | 352.9 |
| v10 candidate (oct24), cash | 299.4 | 357.7 |

Per member of the 44.90M lineage: set $8,531–9,830; cash $6,668–7,967. Per member of the 42.95M before coverage: set $8,918–10,276. [CALCULATION: v10.per_member_usd, v10.per_member_without_coverage_people_usd]

### Change from v9 by item, standalone and joint [CALCULATION: v10.change_by_item, v10.interactions]

Each item alone on v9, then the order dependence (joint minus the sum of standalones). Controlled rounding to $0.001bn; a part marked * was moved one unit so the column adds.

| | set low | set high | cash low | cash high |
|---|---:|---:|---:|---:|
| v9 (oct16) | 368.030 | 436.562 | 284.397 | 352.929 |
| 22 capital rate bounded over θ | +14.356 | +4.246 | +14.356 | +4.246 |
| 23 K-12 capital where enrolled | +0.543 | +0.542* | +0.543 | +0.542* |
| order dependence (joint − sum) | +0.118 | +0.031 | +0.118 | +0.031 |
| **v10 candidate** | 383.047 | 441.381 | 299.414 | 357.748 |

Joint amounts at the end specifications (method mean; item 23's return part at item 22's rate), set: 22 +14.356 / +4.246; 23 +0.661 / +0.573. [CALCULATION: v10.post_terms_at_ends_bn]

### Item 22's capital and rates [CALCULATION: v10.item22]

| | low end | high end |
|---|---:|---:|
| capital return at the case rate, in-run (= the 7% arm's total), $bn | 40.679 | 44.623 |
| state_local: capital at the case rate $bn; rate | 10.723; 2.6752% | 11.673; 2.2353% |
| state_local_hwy: capital at the case rate $bn; rate | 7.358; 3.1855% | 9.941; 2.3678% |
| state_local_k12: capital at the case rate $bn; rate | 10.941; 2.6278% | 10.941; 2.2230% |
| state_local_water: capital at the case rate $bn; rate | 2.525; 2.6598% | 2.525; 2.2313% |
| state_local_sewer: capital at the case rate $bn; rate | 3.377; 2.7254% | 3.377; 2.2484% |
| state_local_power: capital at the case rate $bn; rate | 1.495; 2.6787% | 1.495; 2.2362% |
| state_local_transit: capital at the case rate $bn; rate | 1.395; 3.1830% | 1.395; 2.3672% |
| state_local_airports: capital at the case rate $bn; rate | 1.643; 2.9881% | 1.643; 2.3166% |
| state_local_ports: capital at the case rate $bn; rate | 0.260; 2.5163% | 0.260; 2.1941% |
| federal: capital at the case rate $bn; rate | 0.961; 3.8759% | 1.374; 2.5471% |
| rate change, $bn | 14.356 | 4.246 |

Independent check (`check_item22.py`, Python, without items.cjs): item 22 recomputed from each row's capital pieces × the rate file on 256 rows (set and cash); largest error 1.8e-15 $bn. [CALCULATION: independent_check.json]

### Item 24 beside the band: where-used prices, not identified [CALCULATION: v10.companions.where_used_prices_beside, v10.item24_beside]

not identified, beside: where_used_prices_2026_10_24 RESULT verdict ('neither is a complete national estimate or an adopted change'); held off the band under the same standard as item 25.

| | low $bn | high $bn |
|---|---:|---:|
| v10 with item 24, set | 382.3 | 440.7 |
| v10 with item 24, cash | 298.7 | 357.1 |
| parks, at the end specifications | -0.175 | -0.205 |
| colleges, at v10's rates, at the end specifications | -0.582 | -0.486 |
| change from v10 (set and cash) | -0.757 | -0.691 |
| item 24 alone on v9 | -0.628 | -0.657 |

In year one item 24 adds 0.000 / 0.000: the recreation response at the year-one ends (specifications 24 and 7) is 0, and year one charges no capital return.

### Companions [CALCULATION: v10.companions; v9 values from main_case_2026_10_16/derived/summary.json]

| companion | v10 set $bn | v10 cash $bn | v9 set $bn | change, set |
|---|---:|---:|---:|---:|
| count arm a | 369.0–426.2 | 287.4–344.5 | 354.4–421.5 | +14.6* / +4.7 |
| count arm c | 397.1–456.6 | 311.5–370.9 | 381.6–451.6 | +15.5 / +5.0 |
| C3 − one SE | 387.3–445.5 | 303.7–361.9 | 372.3–440.7 | +15.0 / +4.8 |
| C3 + one SE | 378.8–437.3 | 295.1–353.6 | 363.8–432.5 | +15.0 / +4.8 |
| household-sharing allocation, item 11 excluded | 337.6–395.2 | 248.3–305.9 | 322.8–390.5 | +14.8 / +4.7* |
| schools at the within-district 0.836 response | 352.4–414.3 | 268.7–330.7 | 337.9–409.7 | +14.5 / +4.6 |
| year-one response coefficients | 313.9–370.9 | 230.3–287.3 | 313.8–370.8 | +0.1 / +0.1 |
| coverage from DA, through age 17 | 380.4–438.6 | 296.9–355.1 | 365.4–433.8 | +15.0* / +4.8 |
| coverage from DA, through 29 | 378.9–435.8 | 300.6–357.6 | 364.1–431.1 | +14.8* / +4.7 |
| item 21 population arm | 376.6–435.0 | 293.0–351.4 | 361.7–430.2 | +14.9* / +4.8 |
| item 21 no-translation arm | 376.9–435.2 | 293.2–351.6 | 361.9–430.4 | +15.0 / +4.8 |
| item 21 plain-pooled arm | 390.3–448.5 | 306.6–364.9 | 375.2–443.7 | +15.1 / +4.8 |
| [FRAMING-SENSITIVE] ancestry share, G4+ at nothing (beside) | 258.9–300.7 | 198.8–240.6 | 248.7–297.4 | +10.2 / +3.3 |
| [FRAMING-SENSITIVE] ancestry share, G4+ at its bound (beside) | 310.9–359.6 | 241.8–290.4 | 298.8–355.7 | +12.1* / +3.9 |

A change marked * was moved $0.1bn by controlled rounding so that v9 + change = v10 as printed; v9 is printed as v9 prints it.

### Sign-reversal readings [CALCULATION: sign_reversal.csv oct16_*, oct24_*]

| measure | v9 low | v9 high | v10 low | v10 high |
|---|---:|---:|---:|---:|
| `service_break_even_personal` | -0.0154 | 0.1239 | -0.0189 | 0.1085 |
| `service_break_even_personal__enterprises_at_s` | 0.0229 | 0.1570 | 0.0217 | 0.1493 |
| `service_break_even_shared` | 0.0394 | 0.1879 | 0.0355 | 0.1708 |
| `service_break_even_shared__enterprises_at_s` | 0.0762 | 0.2191 | 0.0745 | 0.2093 |
| `frozen_services_capital_fixed_welfare_bn_cbo_preferred` | -50.8950 | 103.2575 | -52.4831 | 97.5847 |
| `frozen_services_capital_fixed_welfare_bn_cbo_preferred__enterprises_at_s` | -33.4054 | 120.7471 | -33.8536 | 119.4647 |
| `frozen_services_capital_fixed_welfare_bn_cbo_preferred_personal` | -50.8950 | 76.1287 | -52.4831 | 70.4559 |
| `frozen_services_capital_fixed_welfare_bn_cbo_preferred_personal__enterprises_at_s` | -33.4054 | 93.6183 | -33.8536 | 92.3358 |

- Pending, public land: item 25 off: V10_LAND_LANE unset; the r2 land figure is not identified (land_price_rule_r2_2026_10_24).
- Pending, rate lane variant components: the rate lane's level_by_component omits the 9 components the inherited range variants add (eq_college_sl, eq_pos_sl, eq_health_sl, eq_gps_sl, eq_income_security_sl, eq_pos_fed, eq_gps_fed, eq_income_security_fed, gps_sl_row8_increment); v10 prices them at their source's declared level, equal to their parent's, until the lane maps them.

Item 25 mechanism test: 102 per-line charges against `infra/immigration-fiscal/land_price_rule_2026_10_24/derived/land_by_line.csv` at the case rate; largest absolute error 4.7e-11 $bn. This tests the mechanism only; it is not a v10 land result. [CALCULATION: v10.item25_mechanism_test]

Gates passed: 1195 in main_case (checks.json), 446 consumer-API checks (api_check.json), v9's output contract PASS with 6 negative probes (contract.json). End specifications: set [[16, 11], [16, 11]], cash [[16, 11], [16, 11]] (by method, numbered in the 64); same as v9: True.
<!-- tables:end -->

## Payload contract

- **Raw-engine consumer.** Evaluate exactly as for v9 (`Engine.evaluate(withSyntheticLines(m), stateFor(m, spec,
  profile))`, plus every v9 post term), then add the v10 post terms. `evaluateFull` does all of that, and its result
  carries `v10_post_engine.{amounts, parts, rows, capital_pieces}`. `postFor` returns the v10 additions, `postFor9`
  the v9 additions, and `postEngine(s)` the complete post total.
- **Rates.** `meta.one_rate.flat_real_equivalent` is absent whenever item 22 is on. A flat-rate reader must stop and
  price capital from `meta.v10.rates`:
  - `level_by_component[c]` gives the level (the rate lane's map, as published);
  - `variant_level_by_component[c]` gives the level of the nine components only the inherited range variants add;
  - `on_parent_components` lists the sub-row components priced at their parent component's level, not their own
    map entry;
  - `rate_by_level_by_end[level][end_index[end]]` gives the rate;
  - `case_rate` is item 20's 2.0810698764%.

  Item 22 on a piece is piece × (rate ÷ case_rate − 1). The payload's capital pieces (`capital_pieces[].id`) are
  the central components, every one in `level_by_component`. A variant without item 22 keeps the flat field, with
  `rates: null` (api-gated).
- **Item records.** Each new `meta.items` record (`kind: post_engine`, `edits.count = 0`) has
  `post_engine_by_end.{low,high}`, which holds:
  - `total_bn`, `specification` (16 / 11) and the method-mean `parts`;
  - `by_method.{m}.{total_bn, parts, rows}`.

  `rows` are typed sub-rows, `{item, part, component, line, generation?, population?, value_bn, coef, delta_bn}`,
  with `part` one of engine, completion, college, coverage, count and health, and they sum to the total. These are
  item 20's routing fields.
- **Generation split.** The v10 terms by generation at the ends are in `ancestry.json` `generation_at_ends`. They
  close to `post_engine_by_end` to 1e-6, which is api-gated.
- **Splitting by generation, household or person.** Each item needs its own rule:
  - **22**: split each sub-row as item 20's capital is split. Engine components go by their key, completion carriers
    by parent line, coverage and count parts by their typed generation, and college and health parts by their
    declared population.
  - **23**: the return part follows the K-12 pieces as 22 does. The depreciation part follows the K-12 capital key,
    to enrolled children's households; it has no people and no count term.
  - **24** (beside) and **25** (off): as 22, on their own rows.
- **Denominator and counts.** `population_v9` (44.90M) stays the denominator. No item changes a count, so R1–R13 and
  v9's payload contract apply unchanged to everything else.

## Sign-reversal readings

`sign_reversal.cjs` imports v9's `withCase` unchanged and sweeps v9's package and model. Its `options.post` hook prices
v9's post amounts and then v10's items at each sweep point:

- engine and completion capital follow the sweep's service response;
- coverage and count parts are fixed costs, as v9 holds items 12, 16 and 17;
- the college and health parts of items 22 and 23 are added to items 15 and 21, so v9's rule raw(s) − (1 − s)·raw(0)
  scales them too.

It passes 14 gates:

- with v10 off, it reproduces all 16 of v9's printed `oct16` cells;
- at s = 1, welfare equals minus v10's full cost on all 64 specifications (6.8e-13);
- welfare is linear in s (1.7e-13);
- at s = 0, no engine or completion part on service capital stays charged (1,080 rows);
- at s = 0, v10 changes welfare by its total less the folded parts, which are up to $0.171bn (gap 1.1e-14).

## Companions

Each companion re-derives the v10 terms inside its own runs: the lineage counts, C3, the allocation, the school
response, DA coverage, year one and the item 21 arms. None is a carried v9 value.

The ancestry-share rows take v9's per-specification ancestry costs from `main_case_2026_10_16/derived/summary.json`.
Each specification then adds the v10 terms by generation, weighted by v9's shares (G1 1, G2 0.9248, G3+ 0.3046,
added 0.4075 at G4+ at nothing), and the ends are re-picked. v10 adds no people, so the shares and fractional
populations are v9's. [CALCULATION: ancestry.json set, cash]

## Gates passed

On the committed rate file:

- `test_lane.cjs`: 18 unit tests, including the map's coverage of every central component and the range-variant
  levels.
- `ancestry.cjs`.
- `main_case.cjs`: 1,195 gates, including:
  - v9 reproduction with the items off;
  - the payload contract;
  - the 7%-arm closure;
  - the item 23 oracle and its literal parts;
  - the item 24 oracle;
  - the year-one parks gate;
  - the r1 land mechanism and the r2 ratios;
  - per_spec descriptors matching v9's strings;
  - the rate-file sha shared with ancestry.json.
- `sign_reversal.cjs`: 14 gates.
- `check_item22.py`: 256 rows, largest error 1.8e-15.
- `api_check.cjs`: 446 checks.
- `contract.cjs`: PASS with 6 negative probes.
- `write_result.py`: stops if any gate file fails, and printed parts add to printed totals.

`main_case.cjs` peaks at 1.51 GB RSS under `--max-old-space-size=1536` and ran in 205 s.

## Upstream issues

1. **The rate lane's level map omits the range variants' nine added components.** The capital-definition range
   variants add them: `equipment_and_software` adds `eq_college_sl`, `eq_pos_sl`, `eq_health_sl`, `eq_gps_sl`,
   `eq_income_security_sl`, `eq_pos_fed`, `eq_gps_fed` and `eq_income_security_fed`, and
   `sl_office_at_unallocable_response` adds `gps_sl_row8_increment`. The committed map (1a18b174) has 30 entries and
   none of these. Rather than stop, v10 gives each one the level that
   `capital_return_services_2026_09_27/derived/engine_components.json` `variants.*.adds` declares (`state_local` or
   `federal`, the rate lane's general levels for functions it does not measure separately). It gates three things:
   that list equals `items.cjs` `VARIANT_PARENT`; each declared level equals the mapped level of its parent line
   (`college`, `pos_sl`, `health_sl`, `gps_sl`, `pos_fed`, `gps_fed`; the two income-security components have none);
   and a lane mapping, once added, wins. These components appear only in the inherited range variants, not in the
   band or the companions. Fix upstream: add them to `level_by_component`.
2. **Rate lane premises (review finding 3)** were measured in 1a18b174 and taken with no v10 code change.
3. **The school lane's divisor** is unchanged from before. v10 applies the correction itself (F/k, divisor
   0.9868222477 = `r_embedded_account` × k, unit-tested).

Earlier issue 1 (the rate lane's capital split) was resolved in 52ff8246. Earlier issue 3 (the land ratio schema)
was resolved by r2's `group_weighted_value_*` columns, which v10 now reads.

## Reproduction

```sh
# from the repository root
sh infra/immigration-fiscal/main_case_2026_10_24/run_all.sh
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/main_case_2026_10_24 "sh {lane}/run_all.sh"
# item 25 on: V10_LAND_LANE=infra/immigration-fiscal/<land lane>, with --out-dir to scratch (main_case, ancestry,
# sign_reversal, api_check, contract) and --dir (check_item22.py, write_result.py), not derived/
```

## Log

- 2026-10-24 15:42 JST — started; reading v9 lane and the three source lanes.
- 2026-10-24 19:22 JST — resumed after the subscription session limit (stopped 17:52); on disk: items.cjs only, no derived outputs. Rate input: theta_pairing.bound, hwy_sl on rate_state_local_highways_by_end.
- 2026-10-24 19:33 JST — package.cjs, main_case.cjs, test_lane.cjs, write_result.py, run_all.sh written; scratch build passes all gates; items 23/24 match oracles; item 22 in-run +0.120/+0.043 above the rate lane (split, upstream issue 1).
- 2026-10-24 19:35 JST — controlled rounding holds v9 figures fixed; full run_all.sh rc 0 (627 gates); starting rerun_lane.
- 2026-10-24 19:37 JST — rerun_lane "sh {lane}/run_all.sh": IDENTICAL 12/12, exit 0. Done; nothing committed (parent commits).
- 2026-10-24 19:42 JST — parent: upstream issue 1 resolved in favour of the in-run split; the rate lane carries a dated correction (52ff8246). Committed as a candidate; critique round and the land check pending.
- 2026-10-24 20:02 JST — resumed for the item-review fixes (brief: findings 1–10; do not commit; scratch rates until the rate lane lands).
- 2026-10-24 20:18 JST — scratch main_case stopped [BLOCKED] on `eq_college_sl`: the scratch map covered central components only; extended it to the capital variants' added components (Upstream issue 1).
- 2026-10-24 20:23 JST — scratch run read the rate lane's in-flux working copy (rewritten 20:21 by a peer; item 22 +13.973 / +4.146); rebuilt the scratch map from the committed HEAD file.
- 2026-10-24 20:34 JST — scratch main_case 1,195 gates and check_item22 pass; item 22 alone reproduces the committed +13.038477 / +3.887667; sign_reversal reference moved out of the patched engine.
- 2026-10-24 20:37 JST — sign_reversal, api_check (446) and contract (G2) pass; gate 4 of sign_reversal rewritten to a two-pass on/off check after the first form was vacuous.
- 2026-10-24 20:42 JST — RESULT rewritten on the scratch build. Verdict: awaiting rate lane. derived/ untouched (b1cbb824); rerun check not run; nothing committed.
- 2026-10-24 20:43 JST — resumed: rate lane landed (1a18b174; level_by_component 30 entries, rate_by_level_by_end 10 levels). Removed the V10_RATE_MODEL override from items.cjs, main_case, ancestry, sign_reversal, api_check, check_item22.py and write_result.py.
- 2026-10-24 20:52 JST — the committed map lacks the nine range-variant components (Upstream issue 1): placed them at their source's declared level, gated against parent lines and the source list; two unit tests; meta.v10.rates publishes variant_level_by_component and on_parent_components. run_all.sh rc 0 on the committed rate file: band $383.0–441.4bn set, $299.4–357.7bn cash; item 22 +14.356 / +4.246, +0.136 / +0.047 above the rate lane's line split (sub-row placement −0.152 / −0.052; residual −0.016 / −0.005).
- 2026-10-24 21:01 JST — stale "rate lane premises" pending note replaced with the variant-component note; run_all.sh rc 0 again; RESULT rewritten to the real-rate figures; scratch reproduction kept as the logged check of 20:34.
- 2026-10-24 21:09 JST — rerun_lane "sh {lane}/run_all.sh": IDENTICAL 28/28, exit 0; no session-path references in the lane's code or outputs. Done; nothing committed (parent commits).
