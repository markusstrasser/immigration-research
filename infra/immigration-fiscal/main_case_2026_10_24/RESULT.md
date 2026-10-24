claude-opus-5-5

**Verdict:** candidate v10 (key `oct24`, status candidate, not adopted) is **$381.0–440.3bn** counting promises as
earned (set) and **$297.3–356.7bn** counting benefits when paid (cash), against v9's $368.0–436.6bn and
$284.4–352.9bn. The joint change from v9 is **+$12.953bn / +$3.773bn** at the two ends, in both set and cash. By item,
each alone on v9: item 22 (capital rate bounded over θ) +$13.038bn / +$3.888bn; item 23 (K-12 capital where enrolled)
+$0.543bn at both ends; item 24 (parks and college where-used prices) −$0.628bn / −$0.657bn. The order dependence is
−$0.0005bn / −$0.0001bn, because item 22's rates price the return parts of 23 and 24. Item 25 (land) is built and
tested but **off and pending**: `V10_LAND_LANE` is unset, and the land figure is still being reworked in
`land_price_rule_r2_2026_10_24`. The end specifications are still 16 (low) and 11 (high) in both methods, and v9
reproduces exactly with the new items off. One source oracle does not match to 1e-6: v10's in-run item 22 is
**+$0.120bn / +$0.043bn** above the rate lane's band ($380.949 / 440.406bn), because the lane prices completion and
coverage capital at the plain state/local rate (Upstream issues 1). Items 23 and 24 and the corrected 23+24 sum match
their oracles to 1e-6. The ancestry-share companion is pending; every other v9 companion is recomputed.
[CALCULATION: derived/summary.json v10.band_bn, v10.cash_set_bn, v10.change_by_item, v10.interactions, v10.item22]

## Items

All four are post-engine terms. v10 adds no engine edits and no people, so the payload model, edits and population are
v9's (gated). `items.cjs` `post()` derives each term inside the run it prices, per specification, method, allocation
and reading, from the v9 evaluator's own capital components. Following item 20, those include union-completion
capital carriers, own coverage capital parts, the item 16/17 count parts, item 15's college capital and item 21's
health capital (construction as `public_land_2026_10_24/case_contract.cjs`). The total of those pieces at the case rate
equals the capital implied by v9's 7% arm to 1e-9 at both ends.

| item | rule | source (read-only) |
|---|---|---|
| 22 `capital_rate_theta_bound` | Each capital piece that item 20 prices at 2.0810698764% is repriced at its end's rate: low end θ = 1 (rᵢ = GRR), high end θ = 0 (rᵢ = Baa). State/local 2.6221% / 2.2215%; `hwy_sl` only, at the federal-aid highway blend, 3.1550% / 2.3599%; federal 3.8759% / 2.5471%. Item 6 is unchanged at both ends. | `public_capital_rate_2026_10_24/derived/rate_model.json` `theta_pairing.bound` |
| 23 `k12_capital_where_enrolled` | The K-12 return is multiplied by (F_stock/k − 1), and national K-12 depreciation by the run's K-12 capital key times (F_structures/k − 1) and (F_equipment/k − 1), with k the embedded preferred school price 1.0341917412 (divisor 0.9868). The return part moves with item 22's state/local rate in the joint case; depreciation does not. Year one charges no capital return: depreciation is taken at the matched long-run K-12 key and moved by the education response ratio. | `school_capital_where_enrolled_2026_10_24/derived/summary.json` `headline_key_consistent_A`, `case_base`; k from `user_fee_allocation_2026_10_07/derived/fee_lines.json` |
| 24 `where_used_prices` | Parks: the run's unpriced recreation operating amount (engine, completion carriers, coverage and count parts) × the state/local parks share × the matched municipal bridge index change. Colleges: the run's college capital pieces (at item 22's rate when it is on) × the higher-education fraction × (gross-book factor − 1), case_fall, graduate weight 2. K-12 is not included here; item 23 is that. | `where_used_prices_2026_10_24/derived/parks.json`, `college_factors.csv`; parks budget from `state_priced_services_2026_09_29/derived/corrections.csv` |
| 25 `public_land` (off) | For each land line, the land value × the summed full-return coefficient of that physical line's capital pieces (key × response, all pieces, at that end's item 22 rate when 22 is on), with no depreciation. K-12 also carries the lane's `group_ratio`, which can differ by value variant. Off unless `V10_LAND_LANE` names a lane with `derived/land_by_line.csv`. | the lane named by `V10_LAND_LANE`; tested against `land_price_rule_2026_10_24` (r1) |

<!-- tables:start (write_result.py) -->
### Band [CALCULATION: derived/summary.json v10.band_bn, v10.cash_set_bn, v10.v9_band_bn]

| | low $bn | high $bn |
|---|---:|---:|
| v9 (oct16), set | 368.0 | 436.6 |
| v10 candidate (oct24), set | 381.0 | 440.3 |
| v9 (oct16), cash | 284.4 | 352.9 |
| v10 candidate (oct24), cash | 297.3 | 356.7 |

Per member of the 44.90M lineage: set $8,485–9,806; cash $6,622–7,944. [CALCULATION: v10.per_member_usd]

### Change from v9 by item, standalone and joint [CALCULATION: v10.change_by_item, v10.interactions]

Each item alone on v9, then the order dependence (joint minus the sum of standalones). Controlled rounding to $0.001bn; a part marked * was moved one unit so the column adds.

| | set low | set high | cash low | cash high |
|---|---:|---:|---:|---:|
| v9 (oct16) | 368.030 | 436.562 | 284.397 | 352.929 |
| 22 capital rate bounded over θ | +13.038 | +3.887* | +13.038 | +3.888 |
| 23 K-12 capital where enrolled | +0.543 | +0.542* | +0.543 | +0.542* |
| 24 where-used prices (parks, colleges) | -0.628 | -0.657 | -0.628 | -0.657 |
| order dependence (joint − sum) | -0.001 | 0.000 | 0.000* | 0.000 |
| **v10 candidate** | 380.982 | 440.334 | 297.350 | 356.702 |

Pair interactions (set; cash is the same to 1e-9): 22 + 23: +0.117 / +0.030; 22 + 24: -0.118 / -0.031; 23 + 24: 0.000 / 0.000; higher order 0.000000 / 0.000000. [CALCULATION: v10.interactions.pairs]

Joint amounts at the end specifications (method mean; the return parts of 23 and 24 at item 22's rates), set: 22 +13.038 / +3.888; 23 +0.660 / +0.573; 24 -0.745 / -0.688. [CALCULATION: v10.post_terms_at_ends_bn]

### Item 22 against its source [CALCULATION: v10.item22]

| | low $bn | high $bn |
|---|---:|---:|
| capital return at the case rate, in-run (= the 7% arm's total) | 40.679 | 44.623 |
| rate change, rate lane (`theta_pairing.bound.set.rate_delta_bn`) | 12.919 | 3.844 |
| rate change, v10 in-run | 13.038 | 3.888 |
| in-run minus lane | +0.120 | +0.043 |
| capital at case rate, state_local: in-run / lane | 32.359 / 32.777 | 33.309 / 33.886 |
| capital at case rate, state_local_highways: in-run / lane | 7.358 / 6.977 | 9.941 / 9.420 |
| capital at case rate, federal: in-run / lane | 0.961 / 0.925 | 1.374 / 1.317 |

### Companions [CALCULATION: v10.companions; v9 values from main_case_2026_10_16/derived/summary.json v9.companions]

| companion | v10 set $bn | v10 cash $bn | v9 set $bn | change, set |
|---|---:|---:|---:|---:|
| count arm a | 367.0–425.2 | 285.4–343.5 | 354.4–421.5 | +12.6* / +3.7 |
| count arm c | 395.0–455.5 | 309.3–369.8 | 381.6–451.6 | +13.4 / +3.9 |
| C3 − one SE | 385.2–444.4 | 301.6–360.9 | 372.3–440.7 | +12.9* / +3.7* |
| C3 + one SE | 376.7–436.2 | 293.1–352.5 | 363.8–432.5 | +12.9* / +3.7* |
| household-sharing allocation, item 11 excluded | 335.6–394.2 | 246.3–304.9 | 322.8–390.5 | +12.8 / +3.7 |
| schools at the within-district 0.836 response | 350.3–413.3 | 266.7–329.6 | 337.9–409.7 | +12.4 / +3.6 |
| year-one response coefficients | 313.9–370.9 | 230.3–287.3 | 313.8–370.8 | +0.1 / +0.1 |
| coverage from DA, through age 17 | 378.3–437.5 | 294.8–354.1 | 365.4–433.8 | +12.9 / +3.7* |
| coverage from DA, through 29 | 376.8–434.8 | 298.6–356.6 | 364.1–431.1 | +12.7 / +3.7 |
| item 21 population arm (v9 recomputed; not in v9.companions) | 374.6–434.0 | 290.9–350.3 | 361.7–430.2 | +12.9 / +3.8 |
| item 21 no-translation arm (v9 recomputed; not in v9.companions) | 374.8–434.2 | 291.2–350.5 | 361.9–430.4 | +12.9 / +3.8 |
| item 21 plain-pooled arm (v9 recomputed; not in v9.companions) | 388.2–447.5 | 304.6–363.9 | 375.2–443.7 | +13.0 / +3.8 |
| ancestry share | pending | pending | | |
| public land | pending | pending | | |

A change marked * was moved $0.1bn by controlled rounding so that v9 + change = v10 as printed; v9 is printed as v9 prints it.

Item 25 mechanism test: 102 per-line charges (17 lines × central/low/high values × 2 ends) against `infra/immigration-fiscal/land_price_rule_2026_10_24/derived/land_by_line.csv` at the case rate; largest absolute error 4.7e-11 $bn. This tests the mechanism only; it is not a v10 land result. [CALCULATION: v10.item25_mechanism_test]

Gates passed: 627 (derived/checks.json). End specifications: set [[16, 11], [16, 11]], cash [[16, 11], [16, 11]] (by method, numbered in the 64); same as v9: True.
<!-- tables:end -->

## End specifications

Picked fresh for each case from all 32 main specifications in both methods. Low is 16 and high is 11 in both methods,
in set and cash, for v9, for each item alone, for every pair, and for v10 joint. The per-end rates of item 22 do not
re-pick an end: the low end's specification remains the minimum and the high end's the maximum. The companions keep
v9's ends: shared allocation 48 / 43, school within district 24 / 3, year one 24 / 7.
[CALCULATION: summary.json v10.end_specifications, v10.change_by_item.*.ends, v10.companions.*.ends]

## Payload contract for the four new items

A raw-engine consumer evaluates exactly as for v9 (`Engine.evaluate(withSyntheticLines(m), stateFor(m, spec, profile))`
plus every v9 post term), then adds the v10 post terms. `evaluateFull` does all of that. Its result carries
`post_engine.<id>_bn` and `v10_post_engine.{amounts, parts}`. `postFor` returns the v10 additions only and `postFor9` the
v9 additions; `postEngine(s)` is the complete post total. The payload's `meta.items` gains four records with
`edits.count = 0`, and `meta.v10` gives the rates, constants, selected and pending items and the land lane.
`population_v9` (44.90M) stays the denominator. None of the items changes a count, so R1–R13 and the v9 contract apply
unchanged to everything else. A consumer that splits by generation, household or person must handle each item as
follows:

- **22**: split each capital piece as item 20's capital is split (engine component by its key, completion carriers by
  parent line, coverage and count parts by their typed generation, item 15 college capital and item 21 health capital by
  their declared population). Then multiply each piece by (rate(level, end)/2.0810698764% − 1), with `hwy_sl` at the
  highway rate. The parts rows are per line (`parts.capital_rate_theta_bound`).
- **23**: the return part follows the K-12 capital pieces (`k12`, `k12_user_fees`) exactly as 22 does. The depreciation
  part follows the K-12 capital key, which is per enrolled pupil, so it goes to the group's enrolled children's
  households. It has no people and no count term.
- **24**: the parks part follows the recreation/culture line's group amount, with its carriers, coverage and count
  spending parts. The college part follows the college capital pieces.
- **25** (when on): each land line follows that physical line's capital pieces, as 22 does, with no depreciation.
- Year one (capital off): 22, 25 and 24's college part are zero; 23's depreciation and 24's parks part remain.

## Companions

The companions table above recomputes each v9 companion with the v10 items on (`main_case.cjs` "companions"). Each item
term is re-derived inside each variant's own runs: the lineage counts, C3, the allocation, the school response, the DA
coverage, year one and the item 21 arms. None is a carried v9 value. **Ancestry share is pending.** Its rows weight each
generation's cost by its ancestry share, and the v10 terms have no generation split yet (that would need v9_split
generation parts for each capital component). v9's values are not carried.
[CALCULATION: summary.json v10.companions, v10.pending]

## Gates passed

`main_case.cjs` stops at the first failure. All gates pass (count in the tables block; list in `derived/checks.json`):

- Items off: `caseOf(OCT05, v9 CANDIDATE)` is the adopted v9 module. Its set and cash payloads equal v9's
  `corrections*.json`, its bands equal `v9.band_bn` and `v9.cash_set_bn` exactly, its ends equal v9's, and all 128
  v9 `per_spec.csv` costs reproduce as strings.
- 64 specifications are retained, and the ends agree across methods. Payload-model cost equals the method mean on
  every main specification (set, cash). v10 adds no edits, its payload model is byte-equal to v9's, and on all
  64 × 2 × 2 runs cost = v9 cost + v10 post total, with `postFor` and the post-engine total consistent.
- Item 22: a replica of the rate lane's construction, built from its own inputs, reproduces `bound.{set,cash}.band_bn`
  to 1e-6. The in-run capital at the case rate closes to the lane's 7%-arm total to 1e-9, and the standalone change
  equals the in-run rate delta.
- Item 23 = `k12_capital_existing_k_denominator_diagnostic` (+$0.542615bn) to 1e-6, with return +$0.450560bn and
  depreciation +$0.092055bn to 5e-7. Item 24 = parks matched municipal + college gross-book proxy to 1e-6, part by part.
  Items 23 + 24 = `combined_denominator_diagnostic_book_capital_municipal` (−$0.085 / −0.115bn) to 1e-6.
  [DATA: where_used_prices_2026_10_24/derived/case_scenarios.csv]
- Item changes plus order dependence close to the joint change; the pairs plus the higher-order remainder close.
- Item 25: the mechanism's per-line charges at the case rate match all 102 r1 charges to 1e-6 (max error in the tables
  block). Item 25 is off when the variable is unset.
- v9's item 21 arm bands reproduce v9's `main_case_bands.csv` to 5e-5.
- `test_lane.cjs` (12 unit tests): the land loader's failures and its ratio defaults, rate levels, the bound's rates,
  the corrected divisor, item order, candidate identity, and one-evaluation accounting.
- `write_result.py`: printed parts add to the printed totals (controlled rounding; it stops otherwise).

Peak RSS of `main_case.cjs`: about 1.69 GB under `--max-old-space-size=1536`; it runs in about 55 s.

## Upstream issues

1. **Rate lane line split (item 22).** `public_capital_rate_2026_10_24/rate_model.py` builds its per-line capital
   from v8-standalone `one_rate` parts, rescaled to v9's 7%-arm total. It books union-completion (`capital_reporter`)
   and coverage (`capital_coverage`) capital as separate lines at the plain state/local rate. That puts the completion
   and coverage capital of `hwy_sl` and the federal lines at the wrong rate, and it moves the count, college and health
   pieces through the rescaling. The total capital agrees with v10's in-run pieces to 1e-9. The split does not:
   `hwy_sl` holds $7.358bn in-run against the lane's $6.977bn at the low end. v10 keeps every piece on its parent line,
   which is the brief's "derive it inside the engine run" rule, and so lands +$0.120bn / +$0.043bn above the lane's
   rate change. I did not re-pick: if the parent prefers the lane's figure, the lane should be corrected rather than
   v10 made to copy its split. [CALCULATION: summary.json v10.item22]
2. **School lane divisor.** `school_capital_where_enrolled_2026_10_24/derived/summary.json` (and its
   `case_base.cjs`/`build.py`) still give F against the uncorrected embedded relative 0.954. v10 applies the
   correction itself (F/k, divisor 0.9868) and matches the corrected +$0.54bn. The lane's +$1.36bn headline is unchanged.
3. **Land lane schema for item 25.** The r1 `land_by_line.csv` has no line-level `group_ratio`. K-12's effective ratio
   differs by value variant (central 1.14481, low 1.14473, high 1.14886, because schools are capped at their ATF
   value). The test recovers those ratios from the lane's own coefficient column. v10's loader requires a
   `group_ratio` column for K-12 (optional `group_ratio_low` / `group_ratio_high`) and stops without one, so the r2
   lane must publish them.

## Reproduction

```sh
# from the repository root
sh infra/immigration-fiscal/main_case_2026_10_24/run_all.sh
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/main_case_2026_10_24 "sh {lane}/run_all.sh"
# item 25 on (once the r2 land lane publishes group_ratio): write to scratch, not derived/
V10_LAND_LANE=infra/immigration-fiscal/<land lane> NODE_OPTIONS=--max-old-space-size=1536 \
  node infra/immigration-fiscal/main_case_2026_10_24/main_case.cjs --out-dir <scratch>
```

## Log

- 2026-10-24 15:42 JST — started; reading v9 lane and the three source lanes.
- 2026-10-24 19:22 JST — resumed after the subscription session limit (stopped 17:52); on disk: items.cjs only, no derived outputs. Rate input: theta_pairing.bound, hwy_sl on rate_state_local_highways_by_end.
- 2026-10-24 19:33 JST — package.cjs, main_case.cjs, test_lane.cjs, write_result.py, run_all.sh written; scratch build passes all gates; items 23/24 match oracles; item 22 in-run +0.120/+0.043 above the rate lane (split, upstream issue 1).
- 2026-10-24 19:35 JST — controlled rounding holds v9 figures fixed; full run_all.sh rc 0 (627 gates); starting rerun_lane.
- 2026-10-24 19:37 JST — rerun_lane "sh {lane}/run_all.sh": IDENTICAL 12/12, exit 0. Done; nothing committed (parent commits).
- 2026-10-24 19:42 JST — parent: upstream issue 1 resolved in favour of the in-run split; the rate lane carries a dated correction (52ff8246). Committed as a candidate; critique round and the land check pending.
