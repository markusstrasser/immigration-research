claude-opus-5-5

**Verdict:** The adopted main case of 2026-09-29 is built as a payload-first successor to
`main_case_long_run_2026_09_27/`. The case costs **$371.4–434.8bn** (ends 48/11 in both fill-in methods). The cash set is
**$294.7–361.8bn**, recorded as the band row `cash_set`. All five gates pass:
- G1: the bands equal candidate v4's to 1e-9.
- G2: every September 27 derived file, column, row and key is present; one documented relocation.
- G3: the September 27 lane's own scripts, run on this package with its payload, reproduce all six of its derived
  files byte for byte.
- G4: 8 consumer call patterns, 50 checks.
- G5: two rerun passes IDENTICAL, 16/16 files.

The package evaluates models the consumer builds (blocker 1 fixed), the uncorrected `MODEL` included, which v4-debt-lane
required: every line a specification names is added to it at zero. Every consumer still needs at least a path swap; six
consumer gates that G4 ran need code because the case changed, not the API. Nothing is committed.

## What the lane is

- `derived/corrections.json` is the case. It is candidate v4's builder
  (`main_case_candidate_v4_2026_09_29/payload.cjs` `build()` at the set's options) with five meta stamps and no other
  change: `source`, `adopted` "2026-09-29", `decision` "decisions/2026-09-29-main-case-v4.md", `case` ("; v4, adopted
  2026-09-29: " replaces "; candidate v4, not adopted: ") and `status`. G1's payload gate checks this against
  `corrections_v4.json`.
- `package.cjs` is `forPayload(payload)`:
  - It exports the September 27 package's API: every one of its 112 export names, with the same functions and
    signatures.
  - At load, the builder, run at the payload's item options, must rebuild the payload's lines, receipt lines, edits,
    production grid, `meta.responses` and `meta.capital_return`. `MAIN_SPECS` must also carry `meta.responses` at each
    reading. If either fails, the load stops.
  - `evaluateFull(m, spec, profile)` takes any model: the package's own, `Engine.applyCorrections(MODEL, payload)`, the
    uncorrected `MODEL`, a generation's or a cell's. It:
    1. adds, through `withSyntheticLines(m)`, the payload's lines the model lacks at zero: the 8 correction spending
       lines and the 2 receipt lines the payload splits out (`housing_enterprise_surplus`, `tenant_occupied_property`),
       each with national, amounts and shares 0. Every line a specification's `line_responses` names is then on the
       model, so the September 24 `stateFor`'s unknown-line check passes. A consumer that runs the engine itself calls
       `Engine.evaluate(withSyntheticLines(m), stateFor(m, spec, profile))`, which is gated equal to `evaluateFull`'s
       evaluation;
    2. sets the engine state with the September 27 conventions;
    3. computes the return on public capital from the payload's components on that same evaluation. Every key kind is
       covered, including the new `part_rekeyed`: the parent line's amount over its national, plus the correction line's
       amount over `part_national_bn`.
  - An item variant (options whose item fields differ from the case's), built with `withCentral`, `modelFor` and
    `specsFor`, is passed to candidate v4's `evaluateFull` and matches it exactly. The payload does not carry that
    variant's capital rules. A copied specification, or the case's specification on a variant's model, stops with
    `[BLOCKED]`.
- `forPayload(other)` gives the same API for any payload the builder rebuilds. G3 uses it for the September 27 payload;
  `main_case.cjs` uses it for the cash set's.

## Results

| Quantity (main profile, $bn) | Low end | High end |
|---|---|---|
| **Adopted case** (range 296.8–487.3; quadrature 338.0–456.3) | **371.4146** | **434.8410** |
| Cash set (pension switch off: current benefits) | 294.7011 | 361.8175 |
| September 27 case (`sept27_case`) | 321.8194 | 387.3701 |
| Change from September 27 | +49.5952 | +47.4709 |
| Without the capital return | 336.9919 | 377.6711 |
| Capital return (federal 0.8275 / 1.7644) | 34.4227 | 57.1699 |
| General government at 0 (`general_government_fixed`) | 341.1452 | 390.5026 |
| Uncorrected model at the adopted responses | 313.2581 | 378.9158 |
| Option A, beside | 355.8774 | 413.6679 |
| All capital at 7%, beside | 457.4713 | 511.0675 |
| Item 8 (transit at the riders' key), beside | 371.5842 | 435.0218 |
| Item 10 (uninsured use 0.7x), beside | 369.8811 | 432.5986 |

The change from September 27, by item, at fixed specifications, adding items in the brief's order (the parts add to the
change):

| Item | Change ($bn, low / high) |
|---|---|
| 1 | −1.6912 / −1.6912 |
| 2 (production, row 4) | +1.6427 / +1.1074 |
| 3 | −3.2005 / −3.0966 |
| 4 | −0.3529 / −0.5293 |
| 5 (property) | −27.1863 / −27.1863 |
| 6a | +0.3948 / +0.5387 |
| 7 | −0.9482 / −0.7324 |
| Pension | +76.7135 / +73.0235 |
| State pricing | +2.1517 / +2.2394 |
| Roads by miles | +2.0717 / +3.7978 |

- **Each item alone** is in `each_addition` (bands) and `v4.items_alone_at_fixed_specifications_bn`. It equals the
  candidate's attribution to 5.7e-14.
- **By side, against the uncorrected model:** receipts +26.993 / +28.205, spending +29.521 / +26.612, production
  +1.643 / +1.107.
- **Enterprise receipt's move from the schools case:** 4.8676, which is the re-key 0.0220 plus public housing's split
  4.8456. The enterprise line's national falls from −47.46 to −7.162.
- **Sign reversal** (`sign_reversal.csv`, September 29 columns):
  - The service break-even is −11.0% to −2.4% personal and −9.3% to −0.6% shared. With enterprises at s it is −5.5% to
    +1.5% personal and −3.8% to +3.3% shared.
  - Frozen services: −86.7 to +17.8, and −65.5 to +33.3 with enterprises at s.
  - The September 26 and 27 columns print as the September 27 lane's file.

## Gates

- **G1 (bands = the candidate's):** `main_case.cjs` [G1].
  - The set and the cash set equal candidate v4's `summary.json` bands (`at_48_11_bn`, `own_band_bn`, `by_method`) to
    1e-9 and print as its `bands.csv`. The ends are 48/11 in both methods. By method: b_hotdeck 367.312 / 431.971, b_matched
    375.517 / 437.711; cash 291.388 / 359.459 and 298.014 / 364.176.
  - At every specification the payload models and `consumer.cjs` (engine plus payload, no package) give the methods'
    mean (max |diff| 1.7e-13).
  - The package's evaluation equals candidate v4's package's (0.0).
  - 95 variant and range bands equal candidate v4's package's (0.0).
- **G2 (contract):** `contract.cjs` → `derived/contract.json`. No September 27 file, column, row or key is missing; none
  changes type.
  - CSVs: the columns are kept in order. `sign_reversal.csv` adds `sept29_low`, `sept29_high`. `main_case_bands.csv`
    goes from 26 to 28 rows (`sept27_case`, `cash_set` added). `components.csv` goes from 19 to 21 rows
    (`property_long_run`, `payroll_compliance` added). `per_spec.csv` keeps 128 rows.
  - `corrections.json`: 190 paths → 566, adding 376 paths in 24 subtrees.
  - `summary.json`: 579 paths → 834, adding 252 paths in 68 subtrees, with one relocation (below).
- **G3 (generality):** `generality.cjs` → `derived/generality.json`.
  - Method: the September 27 lane's own `main_case.cjs` and `sign_reversal.cjs` run unmodified, each in a child process.
    Their `require("./package.cjs")` resolves to this package's `forPayload()` of that lane's `corrections.json`. HERE is
    that lane's directory. Their `fs` sends writes to a temporary directory and stops any other write.
  - Result: all their gates pass (63 and 8), and all six files are byte-identical.
- **G4 (API):** `api_check.cjs` → `derived/api_check.json`. Eight call patterns ran as their consumers write them, 50
  checks. Four pass their own models:
  - `sept24_specs.cjs`: `MODEL` and `applyCorrections(MODEL, payload)`.
  - `generation_lines.cjs`: the generation lane's `model_G*.json` at 8654a0c. The oracle is that the generations add to
    the whole group: 1.1e-13 under the September 27 package, then 1.1e-13 under this one. `forPayload` of the September
    27 payload on that pin's corrected generation models equals the September 27 package exactly.
  - `specs.cjs`: both cases' payloads applied by the consumer.
  - `band_variants.cjs`: its justice and uncompensated-use variants on the uncorrected and the corrected model, through
    `cost(m, s)`. On the September 27 payload, `forPayload` prints all 14 published `sept27_uncorrected` and `sept27` rows
    of `sept27_propagation_2026_09_27/derived/band_variants.csv` exactly (toPrecision(15)). On this case the lane's gates
    hold: the uncorrected run gives `uncorrected_at_adopted_responses`, and every variant moves the uncorrected and
    corrected models by the same amount (1.1e-13).
- **G5:** `uv run --no-project python3 scripts/rerun_lane.py --allow-unrun infra/immigration-fiscal/main_case_2026_09_29/package.cjs infra/immigration-fiscal/main_case_2026_09_29 "node {lane}/main_case.cjs" "node {lane}/sign_reversal.cjs" "node {lane}/generality.cjs" "node {lane}/contract.cjs" "node {lane}/api_check.cjs"`.
  - Two passes were IDENTICAL (16/16).
  - An earlier pass reported `generality.json` CHANGED. That was expected: the method text had been corrected after the
    file was written.
  - `package.cjs` is a module, not a script, hence `--allow-unrun`.

The other gate groups in `main_case.cjs` (53 gates in all) and `sign_reversal.cjs` (12) are:
- the payload stamps;
- specifications: September 27's fields plus the 9 added line responses;
- profiles;
- general government at 0: it moves only its line and the gps capital;
- the uncorrected model at the adopted responses:
  - `withSyntheticLines(model.json)` appends exactly the 8 + 2 lines at zero and changes nothing else;
  - every specification evaluates in all 4 profiles, and each `line_responses` entry has its engine row;
  - the direct engine run equals `evaluateFull` exactly;
  - `consumer.cjs` (no package) on model.json with the lines at zero gives the same cost at every specification (0.0),
    whose span is `uncorrected_at_adopted_responses`;
- history rows: they re-derive exactly;
- items: sequential sums, all off = September 27, all on = the case;
- the range, enterprises, land rows and sides;
- sign reversal: one engine, s = 1 is the proportional reference (0 diff), and linearity in s.

## Output contract: what each September 27 row and key holds here

Every row and key keeps its September 27 name, and its meaning except where noted below. It holds one of four kinds of
value:

- **v4 value:** the quantity on this case. These are:
  - **Rows:** `adopted`, `uncorrected_at_adopted_responses`, `without_capital_return`, `school_within_district`,
    `school_within_district_as_response`, `enterprises_out_option_a`, `enterprise_receipt_at_model_json_share`,
    `capital_return_at_7pct`, `rental_assistance_at_0`, `general_government_fixed`, `k12_capital_at_pupil_share`,
    `audit_row3_instead_of_cbo_income_tax`, `no_fill_in_correction`, and the other-profile `adopted` and
    `uncorrected_at_adopted_responses` rows.
  - **Keys:** `main_case`, `change`, `end_specifications`, `lines_at_end_specifications`, `capital_at_end_specifications`,
    `enterprises`, `school`, `rental_assistance`, `responses`, `range`, `components`, `by_side_…` and `group_receipts_bn`.
  - **Files:** `per_spec.csv`, `components.csv` and `corrections.json`.
- **History:** the September 27 lane's value. Where the value is a band, it re-derives exactly through `forPayload`.
  These rows and keys describe how that case was built, as they did in its own files:
  - band rows `first_year_response`, `schools_case` (every profile), `long_run_responses_alone`,
    `rental_assistance_alone` and `long_run_responses_and_capital_return_option_a`;
  - `summary.json` `adopted_2026_09_2x`, `first_year_response` and `schools_case`;
  - `each_addition`'s five September 27 entries;
  - `enterprises.capital_lane_rows_before_rental_assistance` and `enterprises.interest`.
- **Relocated (one block):** `change_at_fixed_specifications` now holds v4's change from the September 27 case. Its
  parts are `item_1` … `item_roads`, and `total` and `note` keep their names. The ten September 27 parts moved to
  `change_at_fixed_specifications.sept27_case.<part>`. Any reader of the September 27 chain (`run_generations.cjs`
  `PARTS27`, `case_components.cjs:129-133`) must read that path.
- **Documented values:**
  - `change` is the change from the previous adopted case, now the September 27 case (+49.5952 / +47.4709). September
    27's was its change from the schools case (+63.3309 / +95.4153), which is `adopted_2026_09_27` less
    `schools_case` here.
  - `audit_row3_instead_of_cbo_income_tax` is `{incomeTax: "row3", tax_key: "cbo_2022"}`. Audit row 3 replaces the
    income-tax key, and item 3 had moved it to the IRS-raked key.
  - `beside_the_account.congestion` is the September 27 figure with `not_recomputed`: it was derived with roads on
    economic affairs' key, before roads were keyed by miles.
  - `enterprises.receipt_at_end_specifications.move_from_the_schools_case_bn` is the re-key plus item 1's public-housing
    split, with `of_which_rekey_bn` and `of_which_public_housing_split_bn`. September 27's value was the re-key alone.
  - `range` has no component for items 7, pension, state or roads. `transit_key` is skipped because item 8 is beside
    the case (`v4.range_components_skipped`).
  - The other profiles for the correction lines are **new definitions**, which candidate v4's package refused to
    evaluate:
    - `roads_vmt_sl`, `roads_vmt_fed` and `state_price_recreation_culture` follow their long-run parents: 0 under the
      category lag, 1 under the proportional reference.
    - The public-order and health lines follow their parents, which are at 1 in every profile.
    - Receipt responses apply in every profile.
    - This gives `long_run_non_school_fixed` 313.9994 / 402.9844, `proportional_reference` 398.1491 / 448.0053, and the
      old main profile 342.2107 / 387.2405.
- **Added:**
  - band rows `sept27_case` (with the September 27 range) and `cash_set`;
  - `summary.json`: `adopted_2026_09_27`, `cash_set`, `receipts_at_end_specifications` (the 5 receipt overrides), `v4`
    (items, rules, payload provenance, correction-line parents, input hashes), the item entries in `each_addition` and
    `change_at_fixed_specifications`, the 5 correction lines in `lines_at_end_specifications`, the 9 new
    `responses`/`line_responses` entries, `enterprises.public_housing`, `beside_the_account` items 8 and 10, and
    `by_side_…production`.

## Consumers

**API differences common to every consumer.**
- **Path swap:** `main_case_long_run_2026_09_27` → `main_case_2026_09_29`, for `package.cjs` and `derived/*`. The
  previous case's band row is `sept27_case`, where September 27 used `schools_case`. Its package is `P.SEPT27`, as
  September 27 used `P.PSCHOOLS`.
- **Exports:** all 112 September 27 names are present.
  - 20 are payload-first versions: `HERE MAIN_SPECS CENTRAL stateFor cost band correctionsPayload evalPackage central
    RESPONSES responsesFor specsFor bandFor componentsFor keyOf capitalReturn evaluateFull withCentral modelFor
    capitalMeta`.
  - The other 92 are the September 27 objects themselves.
  - Added: `LANE SEPT27 V4PKG BUILDER ITEMS PARENT FOLLOW_LR ENTERPRISE_SPLITS PAYLOAD_LINES PAYLOAD_RECEIPT_LINES
    ZERO_RECEIPT_LINES LINE_RESPONSES KEY_KINDS RESPONSE_KINDS withSyntheticLines payloadModel forPayload adopt ADOPTED
    DECISION STAMPED CANDIDATE_TEXT optionsOf stripSpec`.
- **Specifications:** the same 12 fields in the same order. `line_responses` has **13 entries** (September 27: 4):
  - economic affairs, recreation and culture, housing subsidies;
  - five receipt overrides (`enterprise_surplus`, `housing_enterprise_surplus`, `modeled_owner_property`,
    `tenant_occupied_property`, `personal_property_tax`);
  - `roads_vmt_sl`, `roads_vmt_fed` and the three `state_price_*` lines.

  `P.LINE_RESPONSES` maps each key to its `meta.responses` entry. Every receipt override has low = high.
- **Capital rules:** `componentsFor(null)` is `meta.capital_return.components`.
  - `hwy_sl` and `hwy_fed` are keyed `part_rekeyed`.
  - `ent_housing_sl` is keyed by `housing_subsidies`.
  - `P.CAP` and `P.CAP_FILE` are still the capital lane's file, whose rules differ for those three: read
    `componentsFor`.
- **Lines:** `SYN_LINES` is still the September 24 three. `PAYLOAD_LINES` holds all 8 and `PAYLOAD_RECEIPT_LINES` the 2.
  `withSyntheticLines` (now exported) adds the missing ones of all 10 at zero. `ZERO_RECEIPT_LINES` holds the 2 receipt
  lines in that form (national, amounts and shares 0), for ports such as `debt_legacy.py`. Evaluate the engine yourself
  only as `Engine.evaluate(withSyntheticLines(m), stateFor(m, spec, profile))`.
- **Evaluation:** `evaluateFull` returns `{evaluation, capital, cost_bn}` as before. For a variant it hands to candidate
  v4, the candidate-only fields `road_return_removed_bn` and `public_pay_bn` are dropped. `cost_bn` still includes
  public pay when that option is on.
- **Payloads:** `correctionsPayload()` is `corrections.json`. `correctionsPayload(o)` with item options returns the
  builder's unstamped payload for that variant. Options that move a specification field have no payload, and the
  builder stops.
- **Options:** `modelFor` requires options built by `withCentral`, which carry every item key.

**Each consumer.** Line numbers come from the read-only survey of 11:09–11:21 JST. They were not re-read in files that
peers have modified since: `case_ends.cjs`, `distribute.py`, `debt_legacy.py`, the world-ledger scripts. The ✓G4 rows
were run here.

| Consumer | Path swap | Change needed beyond the swap |
|---|---|---|
| `assumption_explorer_2026_09_21/engine.js` | — | None: done in db5840f. |
| `distribution_weights_2026_09_23/case_ends.cjs` ✓G4 | `CASES` entry (a peer's uncommitted edit adds `sept29`) | None. It reads the bands by position (columns kept). Its production block passes G4. |
| `distribution_weights_2026_09_23/distribute.py` | `LATER_CASES :165`, base variant `sept27_case` | Split the change into A and P+F. The production item moves P and F only (+1.643 / +1.107). Silent otherwise. |
| `world_ledger_2026_09_27/generation_lines.cjs` ✓G4 | `CASES` and the `FULL` flag (the peer's edit); a sept29 generation pin | None in the package calls: `evaluateFull` and `stateFor` on generation models pass G4. |
| `world_ledger_2026_09_27/split_residual.py` | `choices :78` | `e["by"]` for national-scale edits (`:67`, `:127`). `receipt_lines` in the correction-only set (`:88`, `:99`). |
| `world_ledger_2026_09_27/valuation.py` | pins | Classes for `roads_vmt_sl/fed` and `state_price_*` in `LINES :84`. |
| `generation_account_2026_09_24/run_generations.cjs` | `CASES :91` | Large. <br>• A generation-split rule for every v4 edit (`:499`) and row-4 production by generation (`:565`, `:730`). <br>• The payload gate `:164-171`. <br>• `PARTS27 :984`: read `change_at_fixed_specifications.sept27_case`, plus the `item_*` keys for v4. <br>• `enterprises…move_from_the_schools_case_bn` (`:1052-1059`) now includes the split. <br>The package side works on generation models (G4). |
| `late_arrival_account_line_2026_09_27/run_cells.cjs` | `CASES :31` | As `run_generations`: netting `x.by` (`:385-405`), production per cell (`:431`), `tenant_occupied_property` in `RECEIPT_GROUPS :441`. |
| late arrival `verify.py`, `build_line.py:24`, `medicaid_check.py:122` | `MAIN :22` and the two | None beyond config. |
| `debt_legacy_2026_09_23/debt_legacy.py` | `LATER_CASES :299` | Large; it has its own engine port. <br>• It needs `receipt_lines`, national-scale edits and the production grid (`:326`, `:372`). <br>• The five correction lines' responses (`:576-595`). <br>• `part_rekeyed` in `capital_rows :500`. <br>• Federal shares for the new lines (`split_corner :983`). <br>• `case_payload` and `rekey_edits` (`:1584`, `:1597`). |
| `sept24_propagation_2026_09_24/band_variants.cjs` ✓G4 | `CASES :50-57` | Build `line_responses` from every `meta.responses` entry (`:152-154`). Written as it is, the `MAIN_SPECS` gate fails. G4 shows that the full rebuild equals `MAIN_SPECS`, and that the 7% and option A bands reproduce. |
| `sept24_propagation_2026_09_24/real_costs_totals.py` | `LANES`/`OUT_DIRS :105-108`, `LONG_RUN :110`, `SOCIAL_ITEMS :114`, `RESTATED :133` | Its congestion quote (`:336`) now reads a value flagged `not_recomputed`. |
| `sept24_propagation_2026_09_24/constant_choices.py` | `OUT_DIRS :50-51` | Runs after `debt_legacy.py`. |
| `uncertainty_propagation_2026_09_22/sept24_specs.cjs` ✓G4 | a `later_cases.json` entry | <br>• A `part_rekeyed` branch, with `housing_subsidies` and `roads_vmt_*` added to `KLINES` (`:86`, `:122`, `:125`); today it stops there. <br>• The model-independence gate (`:144-146`) fails by design: the payload rescales `housing_subsidies` (60.261 → 55.003) and `enterprise_surplus` (−47.46 → −7.162). <br>• `lineTargets :62` on new receipt lines (survey; not run here). <br>The spec-field, `componentsFor(null)`, response and span gates pass G4. |
| `uncertainty_propagation_2026_09_22/propagate.py` | `--case` | `KCOEF_LINES :241`; `es_national :385/:416`; the base rebuild with receipt overrides (`:440-452`); the capital rebuild (`:501`); the production SE (`:745`, silent). |
| `uncertainty_propagation_2026_09_22/test_uncertainty.py` | — | None: `per_spec.csv` keeps `capital_k12_bn` and `capital_college_bn`. |
| `winners_losers_2026_09_24/specs.cjs` ✓G4 | `CASES`: `["adopted_2026_09_27", SEPT27 lane, "sept27_case", P.SEPT27]`, `["adopted_2026_09_29", this lane, "adopted", P]` | `:151` requires exactly 4 line responses; use `P.LINE_RESPONSES`' count. G4: both bands reproduce. |
| `winners_losers_2026_09_24/winners_losers.py` | `CASES :176`, pins beside `:128-130` | Wage basis on row-4 P (`:1843`); debt fractions for new lines (`:537`). |
| `winners_losers_2026_09_24/test_winners_losers.py` | default-case asserts `:279`, `:298-299` | None. |
| `historical_backcast_2026_09_20/case_components.cjs` | `CASES :27` | Fixed additions (`:62-63`) and its "no other line moves" gate (`:115`); production is not an addition; parts from `change_at_fixed_specifications.sept27_case` or `item_*` (`:129-133`). |
| `historical_backcast_2026_09_20/backcast.py` | `LATER_CASES :60` (base `sept27_case`) | `ADDITIONS :69`: one national series per v4 item. |
| `overview_2026_09_28/build.py` | `MAIN :36` | The waterfall `:152`/`:199` needs v4 steps (`item_*`). The sensitivity rows `:505-518` read band rows, which are all kept. About 20 registry rows bind September 27 paths. |
| `main_case_decomposition_2026_09_29/decompose.cjs` (dated) ✓G4 | `:55`, `:74-75` | Its payload gate (`:77`) and union pass G4. The five new lines and the two new receipt lines need their own age treatment (`:177`, `:216-218`; see `P.PAYLOAD_LINES`). |
| `within_group_distribution_2026_09_29/export_lines.cjs` (dated) ✓G4 | `:24`, `:37`; band `:41` → 371.4146 / 434.8410 | `capRule` (`:29-30`) reads the capital lane's rules, which differ for `hwy_sl`, `hwy_fed`, `ent_housing_sl` (silent; G4): read `componentsFor`. `households.py` needs the new key vectors. |
| `break_conditions_2026_09_29/engine_breaks.cjs` (dated) | package `:22`; bands `:45-46`; arms `:55` | `ADD :65` would double-count item 5 and the pension switch. The C3 split `:130` drops `receipt_lines` and `production`. |
| Black and white comparators `engine_lines.cjs` (dated) | package `:8` | `rekey.py:218` prices a line at national × share, and the correction lines' national is 0 (silent). New receipt lines raise a KeyError (`:199`). |

## Files

- `package.cjs`: the adopted case's definitions (payload-first; `forPayload`, `adopt`).
- `main_case.cjs`: G1 and the case gates; writes `main_case_bands.csv`, `components.csv`, `per_spec.csv`,
  `summary.json` and `corrections.json`.
- `sign_reversal.cjs`: writes `sign_reversal.csv`.
- `generality.cjs`: G3, writes `generality.json`.
- `contract.cjs`: G2, writes `contract.json`.
- `api_check.cjs`: G4, writes `api_check.json`.

Run them in that order from the repository root, with the G5 command above.

## Log (append-only; times from `date`)

- 2026-09-29 15:15 JST: stub written after the parent's brief (the operator adopted v4: "1 ok do"). Worker model
  claude-opus-5-5. New files only, in this directory; nothing is committed.
- 2026-09-29 16:27 JST: `package.cjs`, `main_case.cjs`, `sign_reversal.cjs` and `generality.cjs` were written, and their
  gates passed, before this time; their exact times were not recorded. The context was compacted. G2 (`contract.cjs`)
  was written and run.
- 2026-09-29 16:37 JST: G3 reran after the item-variant delegation in `package.cjs` and passed byte for byte. G4
  (`api_check.cjs`) was written: 46 checks passed and six consumer gates need code. G2 was final.
- 2026-09-29 16:37–16:39 JST: G5. Pass 1 reported `generality.json` CHANGED (the method text had been corrected) and
  `package.cjs` NOT RUN (a module). Passes 2 and 3 were IDENTICAL, 16/16.
- 2026-09-29 16:41–16:45 JST: this RESULT was written. `P.CAP` was checked against the capital lane's
  `engine_components.json` (identical).
- 2026-09-29 16:45–16:54 JST: the lead passed on v4-debt-lane's requirement for the uncorrected model.
  - `withSyntheticLines` now also adds the payload's 2 receipt lines at zero, and `stateFor` no longer drops their
    responses.
  - `main_case.cjs` gained 4 gates on the uncorrected model; all 53 pass. The derived outputs are byte-identical.
  - G4 gained band_variants' variant runs on both payloads (50 checks).
  - G3 reran: byte for byte.
  - v4-dist-lane's three questions were answered: per-method models, all four profiles, the summary keys.
- 2026-09-29 16:52–16:54 JST: G5. Pass 4 reported `api_check.json` CHANGED (a pattern's line citation had been
  corrected). Passes 5 and 6 were IDENTICAL, 16/16.
