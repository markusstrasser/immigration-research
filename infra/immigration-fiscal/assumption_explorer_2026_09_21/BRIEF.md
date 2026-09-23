# Brief: show the adopted main case in the assumption explorer

Date: 2026-09-23. The operator adopted three changes to the complete account's main case
([decision](../../../decisions/2026-09-23-main-case-general-government-and-use-keys.md);
[main-case lane](../main_case_2026_09_23/RESULT.md)):

1. general government responds at 0.59–0.84 (`derived/scaling_check.json` composite_low/high);
2. public order and safety keyed by use: the target's amount on `public_order_safety` becomes
   `cj_use_allocation_2026_09_23/derived/summary.json` `central.target_bn` (68.369bn, +5.944bn
   over the population key), national total conserved; the raw-coding variant is +1.670bn
   (`one_at_a_time_change_bn.scaling_raw`);
3. uncompensated care: the target's amount on `medicaid_and_chip_other_medical` rises by the
   under-charged inside part, a range `uncompensated_care_2026_09_23/derived/summary.json`
   `inside_undercharged_bn_use_1.0` = [3.652, 5.748] (0.7× use: `inside_undercharged_bn_use_0.7`).

Result to reproduce (oracle: `../main_case_2026_09_23/derived/main_case_bands.csv`, variant
`adopted`): main profile cost 203.2–249.6bn; non-school education fixed 158.9–212.6bn;
proportional 307.9–341.0bn. The page still labels the general-government preset "Proposed, not
adopted", and the justice and uncompensated-care keys do not exist in the model.

## Do

- `build_model.py`: ADD executed keys, never change `preferred_key` or existing keys
  (`main_case.js` depends on them): `public_order_safety` gains `use` (central) and
  `use_raw_coding`; `medicaid_and_chip_other_medical` gains `uninsured_use_low` and
  `uninsured_use_high` (equal use; add the 0.7× pair if it stays tidy). Each key moves only the
  target/other split for both allocations and keeps the national total. Read every number from the
  two summary.json files; hand-type none.
- `engine.js`: let `unresolvedRange` span two more declared bands, following the
  `school_response_band` precedent: `general_government_response_band` ([low, high]) and
  `key_band` ({line_id: [keyA, keyB]}). Evaluate the cartesian product; report min and max.
- `presets.json`: turn `repo_central_gg` into the adopted main case (kind_label "This repo,
  adopted 2026-09-23"; general-government band via `value_from` composite_low/composite_high;
  `key_override` public_order_safety → `use`; `key_band` Medicaid → the two uninsured-use keys).
  Relabel `repo_central` as the September 20 version (general government fixed), still valid as a
  convention. Give the proportional preset the same three changes if the page's benchmarks are to
  match the INDEX (308–341bn), and say the September 20 value was 270–289bn. Update `misses`
  (police, courts and prisons are no longer per head; victims' harm, unreimbursed care outside
  budgets and housing transfers are reported beside the fiscal account, see
  `research/immigration-real-fiscal-and-social-costs-2026-09-23.md`). Replace hand-typed band
  numbers in notes with `value_from` or remove them.
- `sources.json`: add the decision, the two lanes and the main-case lane; `build_ui.py` refuses
  unknown places or sources without a link or repo reference.
- `README.md`: replace "General government: a proposal, not the published account" with an
  adopted section (keep its evidence text, add the decision link and the two use keys).
- `ui.js`/`template.html`: only what is needed to show the new bands and keys; keep the operator's
  design (one light theme, paper #fffff8, serif, booktabs tables, native controls, no boxes or
  pills, colour on data marks only). A preset setting that is a band should read like the school
  band does ("both values enter the range").

## Gates (all must pass; report the output)

```sh
cd /Users/alien/Projects/immigration-research
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/assumption_explorer_2026_09_21/build_model.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/assumption_explorer_2026_09_21/build_ui.py
node infra/immigration-fiscal/assumption_explorer_2026_09_21/test_engine.js
node infra/immigration-fiscal/main_case_2026_09_23/main_case.js   # must pass; outputs byte-identical
git diff --no-ext-diff --stat -- infra/immigration-fiscal/main_case_2026_09_23/derived/   # must be empty
```

(Check the README's Reproduce section for the exact build order; follow it if it differs.)

- Add to `test_engine.js`: the adopted preset's range equals the oracle's `adopted` row for the
  main profile to 1e-6 (welfare sign: negative = cost), and the same for any other preset you
  switch to the adopted conventions; the September 20 presets still reproduce their published
  bands.
- Headless check with agent-browser (`agent-browser --session <s> open file://…/derived/explorer.html`;
  `eval`, `errors`, `screenshot`; in zsh wrap it in a function). Select the adopted preset, confirm
  the pinned headline shows 203–250 and no console errors, and LOOK at a screenshot of the preset
  section and the ledger table.

## Limits

Write only in `assumption_explorer_2026_09_21/`. Do not commit, stash or checkout. Report files
changed, gate output and anything you could not do, in at most 10 lines.
