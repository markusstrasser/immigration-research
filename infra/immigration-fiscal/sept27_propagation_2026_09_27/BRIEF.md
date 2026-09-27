# Lane brief: move every consumer to the main case of 2026-09-27

Date 2026-09-27. The operator adopted the September 27 case (`../main_case_long_run_2026_09_27/`, decision
`../../../decisions/2026-09-27-main-case-capital-return-and-long-run-responses.md`). Rulings:
- 15:21 JST: rates of 2% at the low end and 3% at the high end, with 7% reported beside the account; rental
  assistance at 1; land a reported gap;
- 16:58 JST: option D, every government enterprise responds.

The case is the schools case ($258.4885–291.9548bn) plus four additions:

- **Long-run responses** for `economic_affairs_services` and `recreation_culture`, per subfunction (low
  readings at the low end, high at the high end), from `../service_response_long_run_2026_09_27/derived/responses.json`.
- **Rental assistance** (`housing_subsidies`, key `housing_support`) at response 1 instead of 0.
- **The return on public capital**, a post-engine term: the charged stock × the rate × the key share × the
  response. It covers 8 core components (schools, colleges, offices, public safety, health) and 5 road and park
  components, at 2% at the low end and 3% at the high end. No charge is netted: the account's lines are
  already net of sales, so netting would credit them twice.
- **Government enterprises (option D).**
  - The `enterprise_surplus` receipt (−$47.46bn national, the enterprises' operating result net of
    depreciation) responds at 1. It is re-keyed from model.json's population share 0.1202 to the case's
    corrected population share, as the corrections already do for the 15 population-keyed spending lines.
  - The full return is charged on all government-enterprise capital ($4,960.4bn, FAAt701 line 79) in 11
    components: public housing, transit, airports, ports, S&L power, water, sewers, tolls, federal power and
    two remainders. Each takes the receipt's key share and the switch's response.
  - Enterprise interest is not added: NIPA's enterprise surplus excludes interest, which sits in the
    account's interest row, held at 0 (BEA MP-5, 2005, p. I-13).
  - Option A (enterprises out) is a labelled variant beside the range.

The case's RESULT gives the final band (expected about $321.8–387.4bn). Read its section "For consumers" first.

## What changes for a consumer

1. **The package.** `../main_case_long_run_2026_09_27/package.cjs` has the schools package's interface plus:
   - `stateFor(m, spec, profile)`: the one engine-state definition, now also in
     `../main_case_2026_09_24/package.cjs`;
   - `evaluateFull(m, spec, profile)`, which returns `{evaluation, capital: {components, total_bn}, cost_bn}`;
   - `capitalReturn(evaluation, spec)`.

   Its `MAIN_SPECS` are the schools case's 64 specifications, in the same order, with `reading`, `rate` and
   `line_responses` added. `line_responses` holds the two long-run lines, `housing_subsidies: 1` and
   `"receipt:enterprise_surplus": 1`; `stateFor` sets receipt ids as engine.js does
   (`response_override["receipt:<id>"]`). **A consumer that builds engine state itself switches to
   `stateFor`**: `winners_losers_2026_09_24/specs.cjs` `evaluate()` and
   `generation_account_2026_09_24/run_generations.cjs` near line 611. The Python engine port in `debt_legacy.py`
   has no response override at all; it must implement both kinds. Copied state is how a consumer silently
   misses a response.
2. **The payload.** `derived/corrections.json` carries the schools case's lines and edits plus one receipt edit,
   the enterprise re-key. Its `meta` adds:
   - `responses.economic_affairs_services`, `responses.recreation_culture`, `responses.housing_subsidies` and
     the enterprise receipt's response;
   - `capital_return`: the rule, rates, `enterprises: "D"` and the components, each with its level, key rule
     and stock;
   - `beside_the_account.congestion`.

   A consumer that applies the payload without the package must set every line and receipt response in
   `meta` and add the capital return from `meta`. **Gate against `derived/per_spec.csv`** at every method and
   specification.
3. **The capital return is part of the direct fiscal response A.** It is a cost of the budgets that hold the
   capital.
   - Its level split, federal against state and local, is per component.
   - Split it by generation by evaluating each generation's model through `capitalReturn`: every key comes from
     the evaluation passed in. Core and block components key off their spending lines. The 11 enterprise
     components key off the `enterprise_surplus` receipt's group amount over its national amount, so a
     generation's receipt share splits them.
   - The enterprise surplus at response 1 is a **receipt** inside the engine cost. Where a consumer reports
     receipts and spending apart, it goes on the receipt side: the group's share of the enterprises' operating
     loss. Its federal share is `debt_legacy.py`'s existing `t32(23) / t31(19)` (NIPA 3.2 line 23 over 3.1
     line 19).
4. **Congestion** beside the account falls from $19.16bn to $13.99bn (low end) and $12.02bn (high end), since
   roads now respond (`beside_the_account.congestion`). Every social total that carries congestion moves with it.
5. **The social-cost upper bound.** Capital at 7% is reported as a variant, never in the fiscal band.
6. **Capped programs' incidence.** New in this case; earlier cases stay reproducible as they were.
   - Rental assistance and LIHEAP are capped and rationed among eligible households. Without the group, those
     slots go to eligible households who now go without. Their channel therefore falls on eligible
     non-recipients (for example renters below 50% of state median income for rental aid, and households
     below 150% of poverty for LIHEAP), not on taxpayers, under both financing conventions.
   - TANF-type aid is a block grant that states can move to other purposes, so it keeps the financing
     conventions.
   - State each proxy and its source.

## Protocol for every consumer (as in `../sept26_propagation_2026_09_26/BRIEF.md`)

a. Regression gate first: rerun as it stands; the tracked outputs reproduce byte for byte on the current
   default (`sept26_schools`). Stop on the first nonzero exit code before comparing any hash.
b. Add `sept27` as the new default. Keep `sept26_schools`, `sept26` and `sept24` reproducible behind the
   lane's case flag.
c. Gates on the new case:
   - the corrected model reproduces the case's `main_case_bands.csv` `adopted` row (1e-4);
   - an uncorrected-model gate uses its `uncorrected_at_adopted_responses` row.
d. Two runs are byte-identical.
e. Report old → new for every published number, in a table in your RESULT file, with the file that holds each.

## Workers (resume the agents that did the schools-case propagation; they know these lanes)

**W1 `lanes`**, in this order:

1. **`../historical_backcast_2026_09_20/backcast.py`.** Each new component back-casts with its own national
   series times the group's share path the back-cast already uses for its parent line:
   - the capital return: BEA net stocks by type, 2005–2024, at a constant real rate, the enterprise stock
     included (FAAt701 line 79 and its types). The capital lane's `_cache` holds the FA tables;
   - the long-run lines: NIPA 3.17;
   - rental assistance: NIPA 3.13;
   - the enterprise surplus: NIPA 3.1 line 19, with its population-share path.

   Where a series is missing, say so and bound it.
2. **`../distribution_weights_2026_09_23/distribute.py --case sept27`.** A moves by the case's change at each
   band end; P and F do not move. Add the capped-programs incidence (item 6).
3. **`../uncertainty_propagation_2026_09_22/`.** `later_cases.json` gets a new entry; `sept24_specs.cjs`
   gains per-spec costs with the capital return as its own column; then run `propagate.py --case sept27`.
4. **`../debt_legacy_2026_09_23/debt_legacy.py --case sept27`.**
   - The engine port takes the three line responses and the enterprise receipt's response from
     `meta.responses`, and the capital return from `meta.capital_return`, split by component level. Implement
     the receipt override as engine.js does; gate the port against `per_spec.csv` with only the receipt at 1.
   - Rental assistance is federal. The enterprise surplus splits by the existing `t32(23) / t31(19)`.
   - The long-run subfunctions carry their levels in `responses.json`.
   - Gate that federal plus state and local equals the total at every specification against `per_spec.csv`.

**W2 `generation`**: `../generation_account_2026_09_24/`.
- Import the new package and evaluate each generation's model through `evaluateFull`.
- Gates:
  - the generations add to the union at every specification;
  - the union reproduces the case;
  - a chain from the schools case at matched specifications adds exactly to the case's `change`: long-run
    responses, rental assistance, capital core, capital block, then enterprises (the receipt re-key, the surplus
    at 1 and the enterprise returns).
- Report the enterprise surplus by generation on the receipt side, and the enterprise returns with the capital
  return.

**Round 2, W4 `ledger`** (after W1 and W2 are committed; the parent sends the pins):
1. **`../sept24_propagation_2026_09_24/`.** `band_variants.cjs`, `real_costs_totals.py` and
   `constant_choices.py` take `--case sept27`. The congestion row uses the re-derived figures. Add a 7% row
   and an option A row (enterprises out) as labelled variants outside the central total.
2. **`../winners_losers_2026_09_24/`.**
   - Case `sept27` becomes the default, with pins in the lane's style.
   - `specs.cjs` uses `evaluateFull`.
   - The capital return, enterprise returns included, goes in the fiscal channel with the enterprise surplus.
     The congestion channel is re-derived.
   - Add the capped-programs incidence (item 6).
   - The compliance and vending rows are rerun only if they depend on the case.

The explorer, figures page and prototypes stay on earlier cases (operator, 2026-09-26: "we don't have to
update all the uis ... we're still researching").

## Boundaries

- Edit only your listed directories, plus your `RESULT_<worker>.md` here. Do not edit the main-case lanes,
  the engine, `research/`, `decisions/`, `CLAUDE.md`, INDEX, FAQ or the ladder.
- Other workers share the checkout. No commits, and no `git add`, `stash`, `checkout` or `reset`.
- Consumers of `ledger_absolute_2026_09_17` verify stored hashes. Never edit a hash; report a guard instead.
- Run Python as `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 <script>` from the repository root.
- Never print keys. No personal identifier in any request header or payload.
- Stub `RESULT_<worker>.md` first with `**Verdict:** pending`. Final message: the RESULT path and at most ten
  lines.
