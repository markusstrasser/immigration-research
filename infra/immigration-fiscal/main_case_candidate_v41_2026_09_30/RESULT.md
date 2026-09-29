claude-opus-5-5
**Verdict:** Candidate v4.1 builds and passes every gate. It is v4 with the five published-weight inputs moved to audit row 4 at their inputs, and it gives $371.2146 / 434.6300bn at specifications 48 / 11 for the set and $295.4036 / 362.5193bn for the cash set. The adopted case gives $371.4146 / 434.8410bn and $294.7011 / 361.8175bn. At one decimal the set falls $0.2bn at both ends, from $371.4–434.8bn to $371.2–434.6bn ($9,353–10,950 to $9,348–10,944 per member on 39,712,493). The cash set rises $0.7bn at both ends, from $294.7–361.8bn to $295.4–362.5bn ($7,421–9,111 to $7,439–9,129). At whole billions the headline stays $371–435bn, and the cash set's high end rounds to $363bn instead of $362bn. With every re-key off, the builder reproduces the adopted corrections.json and the cash payload byte for byte. Each re-key alone reproduces its row4_class pricing row, and two reruns are IDENTICAL.

**Candidate, not adopted; the operator decides.** Until then the adopted case stays `main_case_2026_09_29`,
$371.4–434.8bn.

## What this is

`row4_class_2026_09_29` (75d1ae05) found five inputs of the adopted v4 case summed at the survey's published weights,
the CPS ASEC 2025 union of 40,896,574, instead of audit row 4's 39,712,493, the frame the rest of the account uses. This
lane builds the case with those inputs on row 4, reading the values from `row4_class_2026_09_29/derived/*.json`:

| Input | v4 (published weights) | v4.1 (row 4) | Where it enters |
|---|---|---|---|
| owner-occupied property's key (item 5) | model.json's cell, share 0.063237 | share 0.062121: every incidence rule's group amount over kappa 1.01797579 | `modeled_owner_property`, v3's model, where item 5 enters |
| Part A accrual (pension switch) | $41.137128bn | $40.109099bn | `meta.pension_accrual.part_a_accrual_bn`; Medicare's edit |
| benefit-tax receipt (pension switch) | $2.091206bn shared / $1.816900bn personal | $2.063957bn / $1.788698bn | `meta.pension_accrual.benefit_tax_receipt_bn`; federal income tax's edits |
| state price gaps (state item) | public order and safety 47.792084, health 31.793561, recreation 3.651861 | 49.965888, 33.581151, 3.611535 | `meta.state_pricing` lines' `national_gap_bn`; the three synthetic lines |
| state price receipt factors (state item) | general sales 0.115117, licences 0.262393 | 0.114860, 0.275781 | `meta.state_pricing` receipts' `factor`; sales and licence edits |
| OASDI ratio_net (pension switch) | 0.973667 | 0.975027 | `meta.pension_accrual.ratio_net`; Social Security's edit |

[DATA: `row4_class_2026_09_29/derived/row4_parta.json`, `row4_benefit_tax.json`, `row4_state_index.json`,
`row4_oasdi_ratio.json`, `price_rekeys.json`]

They enter at their inputs. `build.cjs` `modelFor` is candidate v4's `package.cjs` `modelFor`
(`main_case_candidate_v4_2026_09_29/package.cjs:289-321`) step for step. Its state-pricing and pension steps take the
inputs as arguments, and the owner line's key is corrected in v3's model, where item 5 enters. Candidate v4's builder
(`payload.cjs` `build()`, given those two fill-in methods' models) then writes the payload. The state inputs are v4's
CSV-based values times the rerun's row-4 / published ratio; the receipt factors are v4's plus the rerun's change. The
rerun reproduces v4's values to 1e-7. Everything else is v4's: the items, responses, capital components, production
grid and specifications. [CALCULATION: `build.cjs`]

The set payload has 424 edits against v4's 416. v4's edits keep their order. Medicare, Social Security, federal income
tax, general sales, licences and the three state-price lines carry new amounts, and the owner line adds one edit for each
of the eight incidence rules. The cash set (422 against 414) moves only the owner line and state pricing, because the
pension switch is off there. `meta.responses`, `meta.capital_return`, the lines, the receipt lines and the production
grid are v4's. `meta.pension_accrual` and `meta.state_pricing` carry the row-4 values, each with a `rekeyed_on_row4`
block holding the published ones. `meta.candidate_v41` records each input, its source file and sha256, and what was not
re-keyed.

## Bands

$bn at specifications 48 / 11, the two fill-in methods' mean. Both methods' ends are 48 / 11 in all four cases.
Per-method rows are in `derived/bands.csv`; all 64 specifications are in `derived/per_spec.csv`. Per member is on the
account's 39,712,493 (`V4.COUNT`, 39,712,493.33). [CALCULATION: `build.cjs` → `derived/bands.csv`]

| Case | 48 / 11 | Per member |
|---|---:|---:|
| adopted v4 (`main_case_2026_09_29`) | 371.4146 / 434.8410 | $9,353 / 10,950 |
| candidate v4.1 | 371.2146 / 434.6300 | $9,348 / 10,944 |
| adopted cash set | 294.7011 / 361.8175 | $7,421 / 9,111 |
| candidate v4.1 cash set | 295.4036 / 362.5193 | $7,439 / 9,129 |

The pricing of each re-key is `row4_class_2026_09_29`'s. `derived/rekeys_at_inputs.csv` rebuilds it here at the
inputs, and the file is byte-identical to that lane's `price_rekeys.csv`.

## Gates

All 44 pass (`derived/build_gates.json`). The script writes nothing and exits 1 if any gate fails.
- **Inputs.** The reruns' published values are v4's inputs: the Part A accrual, benefit-tax receipts and ratio_net to
  1e-9 (the pension summary through `pensionNet()`); the state gaps to 1e-7 and receipt factors to 1e-9 (v4's
  `SP_PRE`, `SP_RECEIPT`). Kappa is `summary_sept29.json` `v4.kappas` at both ends. Every row4_class output passed its
  own gates.
- **Re-keys off.** This `modelFor` equals candidate v4's for both methods, set and cash (JSON). The builder's set
  payload, stamped by the adopted package's `adopt()`, is `main_case_2026_09_29/derived/corrections.json` byte for
  byte (317,957 bytes). The cash payload is `main_case_candidate_v4_2026_09_29/derived/corrections_v4_cash.json` byte for
  byte. The bands are $371.4146 / 434.8410bn and $294.7011 / 361.8175bn (the adopted `summary.json`, 1e-9).
- **Re-keys on.** $371.2146 / 434.6300bn and cash $295.4036 / 362.5193bn (1e-4). The edits that move are exactly the
  re-keyed lines'. adopted and decision are null, and the case and status name candidate v4.1.
- **Alone.** Each re-key alone, the class-A joint row and the all-five joint row match `price_rekeys.csv` (1e-6; its six
  decimals) and `price_rekeys.json` (1e-9; the largest gap is 9.7e-12).
- **Payload.** In all four cases the payload model gives the two methods' mean at all 64 specifications (1e-9). So does
  candidate v4's `consumer.cjs`, which uses engine.js, model.json and the payload with no package. The adopted case's
  per-method ends are candidate v4's `bands.csv`.
- **Rerun.** `rerun_lane.py` twice: IDENTICAL, 7/7 files, rc 0 both times.

## What adoption would need

1. **An adopted lane for v4.1.** The adopted package cannot carry this payload. Its `forPayload` rebuilds with candidate
   v4's builder and refuses edits it cannot rebuild: "[BLOCKED] candidate v4's builder at the payload's item options
   does not rebuild its edits" (`main_case_2026_09_29/package.cjs:89-94`, checked on `corrections_v41.json`). An adopted
   v4.1 lane would build through this lane's `modelFor` (`build.cjs` `buildOf`), keep the package API, and rerun
   `main_case.cjs` and `sign_reversal.cjs`: bands, per_spec, components, summary and sign reversal. It also needs:
   - a decision record and a ladder entry with notes;
   - new text for `meta.responses.modeled_owner_property.rule`, which says "the line keeps its key" (item 5's rule),
     while the key is now row 4's.
2. **The consumer lanes that read `main_case_2026_09_29`** (`rg -l main_case_2026_09_29 infra/immigration-fiscal`, code
   files): black_comparator_rough_2026_09_28, break_conditions_2026_09_29, debt_legacy_2026_09_23,
   distribution_weights_2026_09_23, generation_account_2026_09_24, historical_backcast_2026_09_20,
   late_arrival_account_line_2026_09_27, main_case_decomposition_2026_09_29, sept24_propagation_2026_09_24 (its sept29
   outputs, including the pairing), uncertainty_propagation_2026_09_22, white_replacement_2026_09_28,
   winners_losers_2026_09_24, within_group_distribution_2026_09_29, world_ledger_2026_09_27, and the drift audit's
   `number_drift_audit_2026_09_29/memo_sweep.py`. row4_class_2026_09_29 prices against v4 by design and stays as the
   record.
   - Lanes that re-apply the pension rule by generation from `meta.pension_accrual` would take row 4's Part A split.
     The whole change is G1's, $12.585bn to $11.557bn; G2 and G3+ are unchanged (`row4_parta.json` `central`).
3. **The docs that print the case.** Those printing one decimal or per member change:
   - research/immigration-real-fiscal-and-social-costs-2026-09-23.md (9 lines);
   - the objections FAQ (6);
   - immigration-adopted-account-by-generation-2026-09-25.md (5);
   - the complete annual account (4);
   - the INDEX (3);
   - the Indian-origin memo (2);
   - one each in the winners memo, the validation memo, the reproduce guide, the dataset register, README.md and
     CLAUDE.md.

   The ladder (4) and the decisions are records, so they take bracketed notes. The whole-billion headline $371–435bn
   (FAQ 8, back-cast 2, INDEX, handoff, reproduce guide, README, CLAUDE.md) does not change. Every figure a doc quotes
   from a consumer lane moves when that lane reruns: pairing, generation split, household split, debt, back-cast,
   winners, world ledger, uncertainty, decomposition and break conditions.
4. **The channels beside the account on the published 40.9M.** These are renters, landlords, crime victims, property
   crime, unreimbursed care, congestion and mobility, with a central sum of −$45.44bn. The winners lane and the world
   ledger take them as their lanes publish them, and those lanes pin the union at 40,896,574. If each is linear in the
   count, scaling by 39.71 / 40.90 moves them by about $1.32bn (`winners_losers_2026_09_24/RESULT.md:604`;
   `world_ledger_2026_09_27/RESULT.md:1331-1334`; both [INFERENCE; not computed]). They are the same class as the five
   here, published weights where the account uses row 4, and they belong to the same revision. They are not priced here.
5. The presentation layers (the evidence map, the explorer, the figures page) follow only when the operator asks.

## Not re-keyed

As in row4_class_2026_09_29, these are recorded in `meta.candidate_v41.not_rekeyed`:
- the OASDI share of self-employment tax: 0.803496 published, 0.803466 on row 4, negligible;
- the scheduled-benefits arm's ratio_net, which sits beside the case;
- item 7's pooled workers'-compensation ratio: pwwgt0 in every year, and row 4 exists only for income year 2024;
- item 5's tenant and personal-property keys: ACS 2024 shares, neither frame;
- item 3's IRS share change, which reaches row 4 through the stack-factor rule.

## Reproduce

From the repository root; under 10 seconds, with no Python and no network:

```sh
node infra/immigration-fiscal/main_case_candidate_v41_2026_09_30/build.cjs
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/main_case_candidate_v41_2026_09_30 "node {lane}/build.cjs"
```

Inputs, all read-only:
- the adopted lane's package, `derived/corrections.json` and `summary.json`;
- candidate v4's package, builder, consumer, cash payload and `bands.csv`;
- `row4_class_2026_09_29/derived/`;
- `main_case_decomposition_2026_09_29/derived/summary_sept29.json`;
- the explorer's engine.js and model.json;
- the pension summary at 9ea1beb (through `git show`, as candidate v4 reads it).

Their sha256 values are in `derived/build_gates.json`.

## Log

Times from `date` (JST), 2026-09-30.
- 01:24:59: lane created.
- 01:27:26: first run. It stopped with a TypeError in the last gate: a naive CSV split misread candidate v4's
  `bands.csv`, whose labels hold commas. Nothing was written. Every earlier gate passed, including the byte-for-byte
  reproduction of the adopted payload and the on values.
- 01:28:03–01:28:11: second run, with a quote-aware CSV split: 44 gates PASS, outputs written.
- 01:28:42–01:28:51: rerun_lane twice: IDENTICAL, 7/7, rc 0.
- 01:30:27: the edit-order gate tightened; v4's edits keep their order and the owner line adds eight. 44 PASS.
- 01:30:32–01:30:39: rerun_lane twice: IDENTICAL, 7/7, rc 0.
- 01:30:51: RESULT written; reported to the lead.
