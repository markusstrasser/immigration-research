**Verdict:** The September 27 case is **$321.82–387.37bn** ($321.8194–387.3701bn), end specifications 48 / 11
in both fill-in methods. It is $63.33bn above the schools case ($258.4885–291.9548bn) at the low end and $95.42bn
above it at the high end. Each addition first reproduces its own lane. All 55 gates pass, two runs are
byte-identical, and the three earlier main cases still pass with clean `git status`. Status: proposed; the parent
commits. [CALCULATION: `main_case.cjs` → `derived/summary.json`]

## The case

The schools case gains four additions, which add exactly at every specification. The moves below are at the fixed
end specifications, with 2% at the low end and 3% at the high end. The two fill-in methods agree on both ends and
are averaged:

| Addition, in chain order | Low end, $bn | High end, $bn | Reproduced against |
|---|---|---|---|
| Long-run road and park responses | +19.4405 | +29.6324 | response lane: its $277.93–321.59bn band, per-spec costs and 5 sensitivities |
| Rental assistance at response 1 | +4.5321 | +4.5321 | its corrected group amount, at every specification |
| Capital return, core (8 components) | +15.9943 | +25.7797 | capital lane: `per_spec_components.csv` and its core band |
| Capital return, roads and parks (5) | +6.1782 | +12.4728 | capital lane: `per_spec_block.csv` |
| Enterprise receipt re-key | 0 | 0 | exactly 0, because the receipt is still at response 0 when the re-key applies |
| Enterprise surplus at response 1 | +5.5611 | +5.5611 | capital lane: re-keyed option D row |
| Enterprise capital return (11 components) | +11.6247 | +17.4371 | capital lane: `per_spec_block.csv` and the re-keyed option D row |
| **Total** | **+63.3309** | **+95.4153** | equals the band move, because the ends do not move |

- Public housing accounts for $0.99bn / $1.48bn of the enterprise return.
- The re-key lowers the case by $0.45bn / $0.60bn. The same case with the receipt left at model.json's share is
  $322.27–387.97bn. The difference equals the capital lane's gap between its plain and re-keyed option D rows.
- At the ends, the capital return is $33.80bn / $55.69bn: state and local $32.97 / $53.95bn, federal
  $0.83 / $1.74bn. [CALCULATION]

| Other rows (`main_case_bands.csv`) | $bn |
|---|---|
| without the capital return (engine cost: long-run, rental assistance, the surplus at 1) | 288.02–331.68 |
| uncorrected model at the adopted responses | 332.75–398.31 |
| **option A, enterprises out (beside the range)** | 304.63–364.37 |
| capital at 7% on every component (beside the account) | 406.31–461.62 |
| rental assistance at 0 (public housing's capital stays) | 317.29–382.84 |
| K-12 capital at the pupil share instead of the account's key | 322.69–388.31 |
| old main profile (roads and parks at CBO's lag) with the other additions | 296.20–345.26 |
| profile `long_run_non_school_fixed` (schools case 204.78–265.81) | 264.40–355.51 |
| proportional reference (schools case 301.29–334.75) | 347.31–400.53 |
| range, components added (quadrature 290.90–408.23) | 258.65–436.05 |

The range carries three new components:

- `long_run_response`: −0.33 to +12.38 at the low end and −8.12 to +15.54 at the high end.
- `capital_rate`: 3% at both ends adds +16.90 at the low end; 2% at both ends subtracts 18.56 at the high end.
- `capital_definition`: −1.38 to +1.35 at the low end and −1.53 to +1.04 at the high end. It re-runs each of the
  12 variants at every specification. The widest are college capital by the account's school fraction
  (−1.38 / −1.53) and offices at response 1 (+1.35 / +0.76).

Two items sit beside the account:

- Land is a [GAP]: $3.33bn / $5.49bn per 10% of land-to-structure value. The core accounts for $1.58 / $2.55bn,
  roads and parks for $0.62 / $1.25bn and enterprises for $1.13 / $1.70bn.
- Congestion falls from $19.16bn to $13.99bn (low end) and $12.02bn (high end). [CALCULATION]

## For consumers

1. **Package** (case key `sept27`): `main_case_long_run_2026_09_27/package.cjs`.
   - It exports the schools package's names, plus `stateFor`, `evaluateFull`, `capitalReturn`, `specsFor`,
     `modelFor`, `componentsFor`, `rekeyEdits`, `populationShare` and `ENTERPRISES` (`"D"`).
   - `MAIN_SPECS` holds the schools case's 64 specifications in the same order. Each gains `reading`, `rate`
     (0.02 / 0.03), `enterprises: "D"` and `line_responses`. The last holds the two long-run lines at the
     reading, `housing_subsidies: 1` and `"receipt:enterprise_surplus": 1`.
   - A consumer that builds engine state itself must call `stateFor`.
2. **Models.** `modelFor(case, method, withCentral(o))` builds the schools model, then applies `rekeyEdits(m)`.
   These edits move that model's `enterprise_surplus` receipt to its own corrected population share, read from
   `general_public_services`' population cell.
   - A consumer that builds its own corrected models, such as one per generation, applies `rekeyEdits(m)` to each.
   - The uncorrected model gets no re-key: its receipt share and its spending share already agree (0.1202).
3. **Cost.** `evaluateFull(m, spec, profile)` returns `{evaluation, capital: {components, total_bn}, cost_bn}`.
   - Each component row carries `id`, `group` (the part: core, block or enterprise), `level`, `stock_charged_bn`,
     `key`, `response` and `return_bn`.
   - The 11 enterprise components are keyed by the evaluation's `enterprise_surplus` receipt amount over its
     national amount, so a generation's evaluation splits them by that generation's receipt share.
4. **Payload** (`derived/corrections.json`). It holds the schools case's 3 lines and 270 edits, then the 8
   re-key edits.
   - The re-key is one receipt shift, `enterprise_surplus`, +$0.145674bn on the reference rule. It is carried to
     the eight incidence rules as every receipt shift is.
   - `meta.responses` adds `economic_affairs_services` and `recreation_culture` (with their subfunctions),
     `housing_subsidies`, and `enterprise_surplus` (`{receipt: true, override: "receipt:enterprise_surplus",
     low: 1, high: 1}`).
   - `meta.capital_return` holds the rule, rates `{low 0.02, high 0.03, reported 0.07}`, `rule_kinds`,
     `enterprises: "D"`, `enterprise_option` (including `receipt_rekey`), the 24 components (each with its part,
     level, key rule, response rule and stock) and the source (sha256; committed at 250ccb5).
   - `meta` also carries `enterprise_receipt_rekey` and `beside_the_account.congestion`.
5. **Without the package.**
   - Apply the payload and set every response in `meta.responses`. Set the receipt through
     `response_override["receipt:enterprise_surplus"]`.
   - Add Σ stock × rate at the reading × key × response. The key kinds are `lines_amount_over_national`,
     `receipt_amount_over_national` and `constant`.
   - The response kinds are `line_response`, `line_response_over_share`, `fixed`, `enterprises_switch`
     (`values["D"]`) and `long_run_subfunction` (the subfunction's value at the reading, from
     `meta.responses.<line>.subfunctions`).
   - `independentCosts()` in `main_case.cjs` does exactly this. It matches every specification to 2.3e-13.
6. **Gate rows.**
   - `main_case_bands.csv`:
     - `adopted`: 321.8194 / 387.3701;
     - `uncorrected_at_adopted_responses`: 332.7493 / 398.3079;
     - `without_capital_return`: 288.0222 / 331.6804.
   - `per_spec.csv` has 128 rows, one per method and specification. Its columns:
     - cost, the engine cost (the receipt included) and the capital total;
     - capital by level and by part;
     - the receipt's response, group amount and cost;
     - 24 component columns;
     - the three lines' responses and group amounts.
7. **Chain.** `summary.json` `change_at_fixed_specifications` is the table above. Its parts add to `change`.
   `of_which_public_housing` and `enterprise_rekey_against_model_json_share` are reported outside the sum.
8. **Receipt side.** The surplus is a receipt: the group's −$5.5611bn share of the enterprises' −$47.46bn operating
   result. The re-key moves the group's receipts by +$0.1457bn; no other receipt moves.
9. **Beside the band, never in it:** 7%, option A, land and congestion.

## Rental assistance and the enterprise surplus (overlap)

The brief's double charge needs two conditions: line 4 includes federal payments to public housing authorities,
and the enterprise surplus excludes the subsidies those authorities receive. The first holds; the second does not.

1. **Line 4 includes those payments.**
   - NIPA Handbook ch. 2, p. 2-13: "Subsidies, which are subtracted in the calculation of GDI, are payments by
     government agencies to private business (for example, federal subsidies to farmers) and to government
     enterprises (for example, federal subsidies to state and local public housing authorities) to support their
     current operations." [SOURCE: https://www.bea.gov/resources/methodologies/nipa-handbook/pdf/chapter-02.pdf]
   - NIPA Handbook ch. 9, p. 9-3: "State and local government enterprises include housing authorities, transit
     systems, airports, water ports, and utilities." [SOURCE:
     https://www.bea.gov/resources/methodologies/nipa-handbook/pdf/chapter-09.pdf]
   - BEA glossary, "Subsidies": "The monetary grants paid by government agencies to private business or to
     government enterprises at another level of government." [SOURCE: https://www.bea.gov/help/glossary/subsidies]
2. **The surplus includes subsidies received.**
   - BEA glossary, "Current surplus of government enterprises": "The current operating revenue and subsidies
     received by government enterprises from other levels of government less the current expenses of government
     enterprises." [SOURCE: https://www.bea.gov/help/glossary/current-surplus-government-enterprises]
   - Handbook ch. 2, p. 2-13: "Subsidies are implicitly included in the measure of net operating surplus."
     [SOURCE: chapter-02.pdf]

So a federal payment S to a housing authority appears twice under option D:

- as spending on line 4, keyed by rental assistance (0.0752 at both ends);
- as revenue inside the surplus, keyed by the corrected population share (0.1172).

The two cancel except for the keys, so the authority's deficit before the subsidy is charged once. The key mismatch
favours the group by S × 0.042:

- at most **$2.53bn**, if all $60.261bn of line 4 went to enterprises;
- about **$0.2bn** for public housing's operating subsidies alone (about $5bn national [TRAINING-DATA]);
  [INFERENCE].

**Overlap netted: $0; bounded in `summary.json` `enterprises.overlap_with_rental_assistance`.**

Enterprise interest is not added. NIPA's surplus excludes interest, which sits in the account's interest row, held
at 0. BEA, Government Transactions (NIPA Methodology Paper 5, 2005), p. I-16: "Interest received and paid are
ignored in the calculation of the current surplus of government enterprises." [SOURCE: the capital lane's cached
`_cache/bea_mp5_government_transactions.pdf`, PDF page 22, footer I-16] The NIPA texts I fetched are cached
(ignored) in `_cache/nipa/`.

[Parent, 2026-09-27 21:25: p. I-13, which the propagation brief cites, is correct too. PDF page 19, footer I—13,
defines the surplus in its body text: "In calculating the current surplus, expenses include consumption of fixed
capital (CFC), but neither revenue nor expenses include interest." Only the page's footnotes are references. The
worker's remark that the page "ends a reference list" was removed.]

## Judgment calls

1. **Profiles.**
   - The main profile is named `long_run_non_school_full`; its variant is `long_run_non_school_fixed`.
   - `delayed: null` marks the profiles whose two lines take the specification's `line_responses`.
   - The proportional reference keeps both lines at 1.
   - The old main profile's variant row carries every other addition.
2. **Rental assistance is at response 1 in every profile.** It is a household transfer, and the account holds
   transfers at 1 everywhere.
3. **Roads and parks capital responds as its line does.**
   - It takes the long-run subfunction response when the line takes its long-run response.
   - It is 0 when the line is held fixed (the category lag, or long-run responses switched off).
   - It is 1 in the proportional reference.
   - The long-run range variants carry their subfunction responses into this capital.
   - The held-at-zero-at-1 variant prices current spending only, because no capital component exists for water or
     conservation.
4. **Enterprises under option D in every profile, the proportional reference included.** The receipt responds at
   1 through `line_responses["receipt:enterprise_surplus"]`, which `stateFor` passes through under every profile.
   Every enterprise component takes the switch's response of 1. The proportional reference has every budget
   respond in proportion, and enterprises are budgets too. A gate checks this in all four profiles.
5. **The re-key.**
   - The target share is `general_public_services`' population cell, as in the capital lane: 0.11717537467643237.
     It is the same in both methods, both allocations and the payload.
   - 14 of the 15 population-keyed lines the corrections edit sit at this share. The exception is
     `public_order_safety` at 0.1188: its population cell carries the CPS lane's shift scaled to the justice use
     key, and the case keys that line by use.
   - The edit is one receipt shift, carried to the 8 incidence rules in proportion (the package's `expand()`
     convention). Only the reference rule enters the case.
   - A gate requires its size to equal national × (spending key − receipt key) from the capital lane's
     `key_consistency`: +$0.145674bn.
6. **The re-key is a separate chain step, applied first.** In the propagation brief's order it moves nothing (0),
   because the receipt is still at 0. Its effect against model.json's share (−$0.45 / −$0.60bn) is reported
   separately.
7. **`without_capital_return` keeps the surplus at 1.** The surplus is a receipt inside the engine cost, not part
   of the post-engine return.
8. **Relaxed payload gates.**
   - The brief's "edits deep-equal the schools case" now reads: the schools case's edits, then the 8 re-key edits.
   - The brief's "the group's receipts do not move" now reads: they move by the re-key alone.
   - The parent ordered both changes with option D.
9. **K-12 takes the account's key**, as the brief says and as the capital lane's own definition now does. The
   pupil share is one of the 12 range variants and a labelled row: +$0.871 / +$0.944bn at the ends.
10. **No charges are netted**, as the capital lane rejects netting: the account's lines are already net of sales.
11. **Option A and 7% sit beside the range.** Land is a gap priced at the case's keys; enterprise land uses the
    corrected share.
12. **`meta.capital_return.enterprises` is the string `"D"`**, the shape the propagation brief names. The details
    are in `enterprise_option`.

## Gates (55, all pass)

- **Old settings.**
  - On the re-keyed models they reproduce the schools case at every specification exactly: the re-key alone moves
    nothing.
  - The band matches to 1e-6, and the first-year response gives the September 26 case.
- **Re-key.** One share across both methods, both allocations and the payload. The population-keyed lines sit at
  that share, `public_order_safety` excepted. The re-keyed receipt matches it. The payload's edit size matches the
  capital lane's (1e-12).
- **Long-run responses.**
  - They reproduce the response lane's band (1e-6), its per-spec costs (relative 1.7e-12) and its 5 sensitivities
    (4.6e-14).
  - Each line's response is the blend of its subfunctions.
- **Rental assistance** adds its group amount at every specification (7.3e-14).
- **Capital, on the capital lane's premises.**
  - Core components: 3,072 values, within 5.0e-7 (the file's 6 decimals).
  - The core band matches.
  - Roads and parks, enterprise returns and the surplus: 1,152 rows each at every reading and rate, within 4.9e-13.
  - Combined rows match to 1e-6: option D, option A and re-keyed option D.
  - 12 definition variants: 144 check values, within 7.1e-15.
  - Land rows match to 5.0e-7.
- **New case.**
  - The tied specifications give the crossed band, and the ends stay 48 / 11.
  - The receipt and every enterprise component respond at 1, and the enterprise components are keyed at the
    corrected share.
  - The additions add at every specification (6.7e-14).
  - No receipt's effect moves except the surplus.
  - The K-12 difference matches the capital lane's.
  - The chain adds to the band move.
  - Each capital part matches the lane's re-keyed option D column (4.4e-7).
  - The re-key effect matches the lane's row difference.
- **Profiles.** Each decomposes exactly; colleges are fixed in `long_run_non_school_fixed`; the block is at 1 in the
  proportional reference; enterprises are at 1 everywhere.
- **Payload.**
  - Lines and edits pass the relaxed gate, and each rule's re-key edit is in proportion.
  - `meta` records option D.
  - The independent path matches every specification (2.3e-13).
  - Receipts move by the re-key alone.
  - The payload reproduces the case (1e-4), and the two sides add.

## Validation (from the repository root)

- `node …/main_case_long_run_2026_09_27/main_case.cjs | tail -3`, twice, both exit 0, ending "all gates passed".
  `shasum -a 256 derived/*` is identical across the two runs:
  - `components.csv` 1ae4e20b…
  - `corrections.json` d3b10f14…
  - `main_case_bands.csv` 970d194d…
  - `per_spec.csv` 02819b54…
  - `summary.json` 50c03165…

  [Parent, 2026-09-27 21:25: the worker's last edit, at 21:12, added the MP-5 p. I-16 citation to `meta`. A network
  failure then stopped it before the rerun. The parent ran the whole Validation block afterwards, and every line
  below holds.
  - The two JSON files changed from the worker's run (`corrections.json` 44658e3a…, `summary.json` 7a454cd8…);
    both carry the new citation text.
  - The three numeric tables are byte-identical to the worker's run.]
- `main_case_2026_09_24`, `main_case_2026_09_26` and `main_case_schools_full_2026_09_26` each end "all gates
  passed" with exit 0, and `git status --short` is empty on each directory afterwards.
- `service_response_long_run_2026_09_27/engine.cjs` ends "all 13 gates passed", with exit 0.
- `capital_return_services_2026_09_27/spec_lines.cjs > /dev/null && echo ok` prints `ok`.
- `git status --short` on both sister lanes is empty.

## Files covered and skipped

Covered:

- `BRIEF.md` and `../sept27_propagation_2026_09_27/BRIEF.md`.
- The package chain:
  - `../main_case_schools_full_2026_09_26/`: `package.cjs` and `derived/{summary.json, corrections.json,
    main_case_bands.csv}`;
  - `../main_case_2026_09_24/package.cjs`: `stateFor`, `expand` and the stack's shifts;
  - `../main_case_2026_09_26/package.cjs`: `build` and `correctionsPayload`.
- `../service_response_long_run_2026_09_27/derived/{responses.json, candidate_band.json, per_spec_costs.csv,
  net_change.json}`.
- `../capital_return_services_2026_09_27/`:
  - `derived/{engine_components.json, summary.json, bands.csv, combined_bands.csv, per_spec_components.csv,
    per_spec_block.csv, gaps.csv}`;
  - `capital_return.py`: the re-key and land code, read only;
  - `spec_lines.cjs`, run only.
- `../assumption_explorer_2026_09_21/`: `engine.js` and `derived/model.json`.
- NIPA Handbook chapters 2 and 9 and two BEA glossary entries (`_cache/nipa/`).

Skipped:

- The capital lane's other derived tables (`per_spec.csv`, `components.csv`, `block_components.csv`,
  `enterprise_components.csv`, `enterprise_surplus_vs_return.csv`, `charges_over_production_costs.csv`,
  `census_finance.csv`, `asset_types.csv`, `transport_split.csv`, `mapping_check.csv`, `lines.csv`,
  `bea_vs_census_types.csv`, `gates.json`). These are its supporting tables. The case reads its components file
  and gates against its band, per-spec and gap files.
- The decision file `decisions/2026-09-27-main-case-capital-return-and-long-run-responses.md`, which the parent
  owns; the payload names it.

## Log (append-only)

- 2026-09-27 15:2x: stub written before reading the brief.
- Step 1 done.
  - `stateFor(m, spec, profile)` was added to `main_case_2026_09_24/package.cjs`, and `cost()` calls it.
  - `spec.line_responses` overrides the profile's responses for the named lines. An unknown line id or a
    non-number fails loudly.
  - The three existing cases rerun. Each ends "all gates passed" with no FAIL line, and `git status --short` shows
    only ` M main_case_2026_09_24/package.cjs` (the edit itself). The derived files of all three are unchanged.
    [CALCULATION: reruns of the three `main_case.cjs`]
- The parent committed the `stateFor` refactor as 1edd418. A second backward-compatible extension serves the
  enterprise option.
  - `line_responses` also takes receipt lines as `"receipt:<id>"`. The line must exist; the extension sets the
    engine's `response_override["receipt:<id>"]`.
  - The three `main_case.cjs` and both `sign_reversal.cjs` rerun with every gate passing and their derived files
    unchanged.
  - `"receipt:enterprise_surplus": 1` moves the cost by +$5.7068bn, the group's negative surplus at model.json's
    share. Unknown ids fail. [CALCULATION]
- The receipt extension is committed as 8d87481. I had called it uncommitted without checking `git log`.
- Enterprise option (parent): the case's choice, D or A, is a constant `ENTERPRISES` in `package.cjs`, set from the
  parent's go-ahead and gated against the components file's switch. A file without the switch, or an unset
  constant, stops the build with `[BLOCKED]`: there is no default.
- Land fix (parent, from the capital worker): my first land filter matched only rows beginning "land at 10%…". It
  dropped `gaps.csv`'s "block: land at 10%…" rows, and its guard checked only the ids it had found. The match now
  takes every part's prefix, and a gate requires one land row per component under its part.
- Step 2 done, before capital was wired in. At specifications 48 / 11: long-run responses +$19.4405 / +$29.6324bn,
  rental assistance +$4.5321bn at both ends. [CALCULATION]
- Rental assistance adds $4.53bn, not the uncorrected $7.54bn, because the adopted corrections already re-key the
  line:
  - the tax-records stack moves it −$0.94 / −$0.72bn;
  - the administrative benefit keys move it −$2.14 / −$2.21bn;
  - $4.4587 / $4.6054bn remains (fill-in methods b_hotdeck_union_matched / b_matched_over_pooled).
  [CALCULATION]
- K-12 key, checked before step 3:
  - For every line except K-12, the capital lane's keys equal amount / national from the evaluation.
  - K-12 used the fixed pupil share 0.174806. The account's own school key is 0.158816 at specification 48 and
    0.163251 at 11, the same in both methods.
  - Since 250ccb5 the lane's own definition uses the account key too. [CALCULATION]
- [STALE 2026-09-27 17:xx: under option D the receipt responds; see the overlap section above.] The step-2 overlap
  conclusion read: "the account holds the `enterprise_surplus` receipt at response 0 in every profile … rental
  assistance at response 1 therefore adds its group amount once. Overlap netted: $0." It was true for step 2.
- Step 3 (GO: capital 250ccb5, ENTERPRISES = "D", operator 16:58 JST).
  - The capital section of `package.cjs` was rewritten:
    - one rule set (the `lane_central_*` rules are gone and fail loudly if they reappear);
    - the enterprise part;
    - the `receipt_amount_over_national` key and the `enterprises_switch` response;
    - a gate that every kind in the file's `rule_kinds` is implemented;
    - the re-key in `modelFor` and in the payload.
  - `main_case.cjs` gates were rebuilt against the committed rows.
  - The result is $321.8194–387.3701bn, matching the parent's expected "about $321.8–387.4bn". [CALCULATION]

Worker: mainbuild, model claude-opus-5-5.
