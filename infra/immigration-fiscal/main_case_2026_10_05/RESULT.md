claude-opus-5-5

**Verdict:** Main case v5 (PENDING: the operator has not yet chosen the counting rule, whole people or ancestry share; as of 2026-10-05 17:45 JST) is built as a payload-first successor to
`main_case_2026_09_29/`, with the same package API and the same output contract. It is the September 29 case plus the
descendants of Mexican immigrants who no longer report Mexican origin, arm b of `main_case_lineage_2026_10_05/`:
3.04M added people, a lineage of 42.75M, counted whole [FRAMING-SENSITIVE: whole people; the fractional and replacement
readings stay sensitivities in the lineage lane]. The case costs **$390.29–461.24bn** (ends 48/11 in both fill-in
methods), **$9,129–10,789 per member**; the cash set is **$307.38–383.41bn** [CALCULATION: derived/summary.json]. Both
equal the lineage lane's arm-b bands to 1e-9. All five gates pass:
- G1, the bands and the payload: 54 gates in `main_case.cjs`, 15 in `sign_reversal.cjs`.
- G2, the contract: every September 29 derived file, column, row and key is here; one documented relocation.
- G3, the lineage off: the September 29 lane's own `main_case.cjs` and `sign_reversal.cjs`, run on this package with
  that lane's payload, reproduce its six derived files byte for byte (53 + 12 gates).
- G4, the API: 8 consumer call patterns, 55 checks; 8 consumer gates need code (listed in `derived/api_check.json`).
- G5, reproduction: `scripts/rerun_lane.py` over the five scripts, IDENTICAL 17/17 files, exit 0.

A consumer moves from `sept29` to this case by reading `main_case_2026_10_05` and keying the case `oct05`; what each
must do with the added people is in [Consumers](#consumers). Nothing is committed.

## What the lane is

- `derived/corrections.json` is the case: the September 29 payload with the lineage lane's payload addition merged in
  (`package.cjs` `merge()`), plus the adoption stamps (`adoptLineage()`: `source`, `adopted` "2026-10-05",
  `decision` "decisions/2026-10-05-main-case-v5.md", `case`, `status`) and `meta.lineage`.
  - It appends the addition's 336 edits to v4's 416: the added people's amounts in every engine cell, then one edit,
    audit row 8's change at the larger group.
  - It takes the addition's production P and F (the union's grid plus the added G3+ members'), keeping v4's dimensions
    and standard errors.
  - It takes the addition's `meta.responses`: 19 group-size values move (general government and its s, row 8's factor,
    the long-run lines and subfunctions, the road lines, recreation's state price, the long-run property receipts).
    The long-run capital components' `values` are rewritten at them. Everything else in v4's payload is unchanged.
  - `meta.lineage` records the population: arm b, generation G3plus, 3,039,719.6 added (1,944,891.7 at the G3 rate,
    1,094,827.9 later losses), lineage 42,752,212.9, union 39,712,493.3. It also holds C3 0.5567 (SE 0.2457, "pooled
    with CPS monthly 1994-2026 (central)", from `generation_carryover_2026_09_27/summarize.py SPLIT_C3`, imported),
    members m_G 1,956,998.4 and m_W 1,082,721.2, and s 0.1202 → 0.1292.
- `derived/corrections_cash.json` is the cash set's payload, built the same way on candidate v4's cash payload.
- `package.cjs` is `forCase(SEPT29, payload)`. It exports the September 29 package's API (every export name, same
  signatures) plus `SEPT29`, `SEPT29_CASH`, `CASH`, `withLineage`, `moveSpec`, `viaCandidate` and the lineage's edits
  and meta.
  - Models are the September 29 package's plus the lineage (`withLineage`).
  - A specification's readings move by `moveSpec()`. The case's v4 reading becomes v5's, and 0 and 1 stay. The long-run
    lines are re-derived at v5's subfunction table for the specification's long-run variant. Any other reading moves
    by the case's change, at first order.
  - Item variants go through candidate v4's package (`viaCandidate`). The road capital is keyed on the evaluation and
    the long-run capital is moved to v5 afterwards.

## Results

| Row ($bn, low / high end) | Sept 29 | v5 | Lineage |
|---|---|---|---|
| Main case (`adopted`) | 371.41 / 434.84 | **390.29 / 461.24** | +18.88 / +26.40 |
| Cash set | 294.70 / 361.82 | 307.38 / 383.41 | +12.68 / +21.59 |
| Without the capital return | 336.99 / 377.67 | 353.15 / 399.39 | +16.16 / +21.72 |
| General government at 0 | 341.15 / 390.50 | 357.68 / 413.47 | +16.53 / +22.97 |
| Uncorrected at the case's responses | 313.26 / 378.92 | 313.06 / 378.71 | −0.20 / −0.21 |
| Capital return at 7% (beside) | 457.47 / 511.07 | 483.16 / 543.72 | +25.69 / +32.65 |
| Enterprises out, option A (beside) | 355.88 / 413.67 | 373.53 / 438.41 | +17.65 / +24.74 |

The September 29 column is that lane's `main_case_bands.csv`; the lineage column is the difference of the printed bands
(unrounded for every variant row: `summary.json` `v5.lineage_by_variant_row_bn`) [CALCULATION: derived/main_case_bands.csv].

Per member, at 42.75M, the set is $9,129–10,789, against $9,353–10,950 for the September 29 case at 39.71M. The cash
set is $7,190–8,968. The total rises and the cost per member falls, because the added people cost less than the
average member [CALCULATION: summary.json `v5.per_member_usd`].

**The lineage line, by part** (each method's end specifications, 48 low and 11 high, averaged; `summary.json`
`change_at_fixed_specifications`):

| Part | $bn |
|---|---|
| The union's response move (v4's model with row 8's change, at v5's group-size responses) | −0.30 / −0.32 |
| Added people priced as identified G3+ members (1.96M) | +16.72 / +22.96 |
| Added people priced as third-plus non-Hispanic whites at G3+ ages (1.08M) | +2.46 / +3.76 |
| **Total** (the band move; the ends do not move) | **+18.88 / +26.40** |

The parts equal the lineage lane's `of_which_*` to 1e-9.

**By generation** (G4 pattern 3: the September 29 generation payloads, with `withLineage` on G3+, add to this case at
every specification, 1e-9). At specifications 48 / 11: G1 $97.15 / 87.02bn, G2 $151.47 / 179.25bn, G3+
$141.67 / 194.97bn. The September 29 split was G1 97.23 / 87.11, G2 151.57 / 179.35 and G3+ 122.61 / 168.38
(`generation_account_2026_09_24/derived/generation_results_sept29.csv`, convention a). G3+ now has 17.38M members.
The high ends use controlled rounding (G1 87.0262 printed 87.02; G3+ 168.3749 printed 168.38), so the parts add to the
printed bands.

**Range.** The range is $312.4–515.4bn (quadrature 354.6–483.7), against 296.8–487.3 on September 29. It has the same 21
components. **Sign reversal** (`sign_reversal.csv`, new columns `oct05_low`/`oct05_high`): with services frozen and
capital fixed, welfare is −82.7 to +28.2bn (September 29: −86.7 to +17.8). The service break-even, personal, is −8.8%
to −0.4% (September 29: −11.0% to −2.4%).

Other profiles: long-run non-school fixed $328.11–426.44bn; proportional reference $419.28–475.58bn; the old main
profile (category lag) $358.79–409.89bn.

## Gates

- **G1** (`main_case.cjs`, exit 1 and nothing written on failure):
  - The set and the cash set are the lineage lane's arm-b bands (1e-9), with ends 48/11 in both methods.
  - The payload model gives the methods' mean at every specification (1e-9), and so does `consumer.cjs` (engine,
    model.json and the payload, no package).
  - The merged payload's model is model.json with the v4 payload and then the lineage payload applied, exactly.
  - The payload is v4's plus the merge and the stamps, nothing else. `meta.lineage` is population.json's arm b and C3.
    Only group-size responses differ from v4's.
  - The specification, profile and general-government-at-0 gates are ported from the September 29 lane.
  - The September 29 case re-derives through `SEPT29`. Its history rows print as that lane's.
  - The lineage line's parts add to the change and match the lineage lane's.
  - The item variants' route, on the case's own options, gives the case and the cash set (1e-9).
  - Only item 8 and the property range's case-scaled tenant national change a line's national total, of the 99 option
    sets the lane runs. Under both, the added people's key is the case's in every cell (1e-12).
  - The side, enterprise, re-key and land gates are ported.
- **`sign_reversal.cjs`**: one engine; each case brings its own general-government pair, since v5's is the larger
  group's. The September 26, 27 and 29 columns print as the September 29 lane's `sign_reversal.csv`. At s = 1 the
  definition is this case's proportional reference (exact), and welfare is linear in s.
- **G2** `contract.cjs`, **G3** `generality.cjs`, **G4** `api_check.cjs`: see the verdict.

## Approximations and assumptions

- [ASSUMPTION] **Variants that change the union's data** leave the added people's amounts at the case's. The lineage
  lane priced them at the case's options only. 15 of the 21 range components deviate as on September 29, within
  $0.001bn: tax block, income tax, medical, LTSS, education, benefits, justice, rows 8–10, small, shelter, care,
  consumption key and payroll. Had the added people moved in proportion to the union (the 7.65% added share), the
  range's ends would move by −2.38 / +2.34bn (`summary.json` `range.at_the_case_data`; an indication, not a bound).
- [ASSUMPTION] **Options that change a line's structure** keep the added people's key, their amount over the line's
  national (`package.cjs` `followNationals()`):
  - a line whose national changes scales their amount;
  - a part split off a line (item 8's transit) takes that line's key;
  - a line an item off removes takes their amount on it along: the split receipts merge back, and the road and
    state-price corrections go.
  Item 8 then moves v5 by +0.17 / +0.18bn, as it moved the September 29 case.
- [APPROX] **Readings moved at first order** (`summary.json` `range.first_order`):
  - general government and row 8 at the engine population key;
  - the receipt-side lane's low property readings.
  Each moves by the case's change.
- [APPROX] **The school within-district response and the K-12 capital at the pupil share** use v4's pupil share, so
  the added people's pupils are not in them. Under `k12_capital_at_pupil_share` the lineage adds 18.16 / 25.17bn
  against 18.88 / 26.40bn in the case.
- **Not recomputed.** The congestion figure beside the account is the September 27 lane's, carried
  (`beside_the_account.congestion.not_recomputed_v5`).

Two package defects were found while building these rows and fixed before the outputs were written; both are now
gated:
- Candidate v4's route keyed the road capital at a road key computed before the lineage's edits: −0.5 to −1.0bn on
  item variants.
- Lineage edits sat on lines whose national an option changed: item 8 read −0.73 / −1.17bn instead of +0.17 / +0.18bn.

## Output contract

Every September 29 file, column, row and key is kept (G2), with v5's value wherever the quantity is defined on v5.

**History rows** keep the September 29 lane's values: the first-year response, the schools case, the September 27 case
and its additions, the earlier adopted bands, v4's `summary.json` block, the capital lane's rows and congestion.

**Moved:** `change_at_fixed_specifications` now holds v5's change from the September 29 case, by part. The September 29
case's own parts (its items, and the September 27 case's under them) moved to
`change_at_fixed_specifications.sept29_case`.

**Added:**
- the band rows `sept29_case` and `sept29_cash_set`;
- the `summary.json` keys `adopted_2026_09_29`, `cash_set.change_from_the_september_29_cash_set_bn`,
  `range.first_order`, `range.at_the_case_data`, `each_addition.lineage`,
  `beside_the_account.congestion.not_recomputed_v5`, `group_receipts_bn.adopted_2026_09_29` and `v5`;
- the `sign_reversal.csv` columns `oct05_low` and `oct05_high`;
- `derived/corrections_cash.json`.

## Consumers

These are the lanes the 2026-09-29 decision moved (Scope), plus the two the API check covers. Each keys the case
`oct05` beside `sept29`, through a path swap to this lane. The table gives what each must do with the added people.
The lanes themselves are not edited here.

| Consumer (where it keys `sept29`) | What it must do with the added people |
|---|---|
| Generation account (`run_generations_v4.cjs:50` CASES; `v4_split.cjs`) | Put the lineage's edits and production on G3+ with `P.withLineage()` (G4 pattern 3: adds to v5 at 1e-9). G3+ goes from 14.34M to 17.38M members. The last edit (row 8, `meta.lineage.edits.row8_edit_index`) is the union's response move: split it by each generation's lane_constants k share. |
| Late-arrival line (`build_line.py:31`, `verify.py:29`, `medicaid_check.py:66`) | Nothing to place: the added people are G3+, so no arrival year. G1 moves only by the response move; read the `oct05` generation split. |
| Debt legacy (`debt_legacy.py` SEPT29, LATER_CASES) | Add `oct05` to the later cases. Its per-member figures use 42.75M, and its long-run capital responses come from `meta.responses` (moved). |
| Sept 24 propagation and pairing (`band_variants.cjs`; `real_costs_totals.py` SOCIAL_ITEMS) | The pairing's social items (crime, crashes, pollution, ...) are priced on the 39.71M union; price the 3.04M at G3+ rates or state the undercount. The variant gate at `band_variants.cjs:200-206` fails as written: a key variant moves the added people's own cells (G4, `consumer_code`). |
| Uncertainty (`propagate.py` CASH_PAYLOADS; `later_cases.json`) | Payloads are `derived/corrections.json` and `derived/corrections_cash.json`. The lineage's own uncertainty sits outside the propagation: C3's SE 0.2457 and arms a and c. Add it as a component from the lineage lane's arm and C3 ±1 SE bands. |
| Winners and losers (`specs.cjs`; `winners_losers.py`) | A per-person rule for the added people: m_G at G3+ members' amounts, m_W at third-plus whites' at G3+ ages. Without microdata for them, place them at the G3+ distribution or exclude them with the rule stated. |
| Back-cast (`backcast.py`) | Needs the lineage's count by year (G3+ by year x the attrition rate); until then, back-cast v5's 2024 lineage at the G3+ path and say so. The base row is `sept29_case`. |
| Distribution (`case_ends.cjs:38` CASES; `distribute.py`) | Split the change into A and P+F as for the union; the lineage's production delta belongs to the added G3+ members. |
| World ledger (`world_ledger.py`; `pins.json`; `generation_lines.cjs`) | Person rows count 42.75M; the G3+ line carries the lineage through `withLineage`. Pin the new generation split. |
| Within-group distribution (`export_lines.cjs:48`; `households.py`) | The household split needs a stated rule for the added people, who are not in the CPS as Mexican-origin. |
| Decomposition (`decompose.cjs`) | Place the lineage at G3+'s age structure (they are priced at G3+ ages); its edits are `meta.lineage.edits`. |

Other lanes key `sept29` outside the decision's scope: white replacement, legacy comparators, the Indian full account,
the rough Black comparator, the row-4 class, pension legacy, break conditions, the net-contributor comparison and
candidate v4.1. Each needs the same call when it moves.

## For the parent

- **Decision filename.** `DECISION` is `decisions/2026-10-05-main-case-v5.md`, an assumed filename stamped into the
  payload. Change it in `package.cjs` if the record lands elsewhere.
- **Commit 9f3ce4dd.** Its body says "221 gates". `derived/gates.json` at that commit records 175, and 176 now, after
  the fractional fix.
- **The draft decision is stale.** It cites "153 gates" for the lineage lane, the 16:25 count; the current count is 176.

## Files

- `package.cjs`: the case's API (`forCase`, `merge`, `adoptLineage`, `followNationals`, `viaCandidate`).
- `main_case.cjs`: G1 and the derived files.
- `sign_reversal.cjs`, `contract.cjs` (G2), `generality.cjs` (G3), `api_check.cjs` (G4).
- `derived/`:
  - `corrections.json`, `corrections_cash.json`;
  - `main_case_bands.csv`, `components.csv`, `per_spec.csv`, `summary.json`, `sign_reversal.csv`;
  - the gate records `contract.json`, `generality.json` and `api_check.json`.

Run order: `node main_case.cjs && node sign_reversal.cjs && node generality.cjs && node contract.cjs && node api_check.cjs`
(about 1 minute).

## Log (append-only; times from `date`)

- 2026-10-05 18:11 JST: lane built. G1 54 + 15 gates, G2 PASS, G3 PASS (53 + 12 gates, six files byte for byte), G4
  PASS (55 checks, 8 consumer gates need code). Two item-route defects were found and fixed before the outputs:
  - the road key: `viaCandidate` now keys `hwy_sl` and `hwy_fed` on the evaluation;
  - lines whose national an option changes: `followNationals`.
- 2026-10-05 18:14 JST: `rerun_lane.py --allow-unrun {lane}/package.cjs` over the five scripts in run order: IDENTICAL
  17/17 files, exit 0 (18:14:02). The lineage lane's final rerun (four steps) right after: IDENTICAL 21/21, exit 0
  (18:14:18).
