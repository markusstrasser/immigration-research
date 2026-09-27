claude-opus-5-5

**Verdict:** Done, not committed. `generation_account_2026_09_24/` now defaults to the September 27 case
(`--case sept27`). Every generation's model is evaluated through the package's `evaluateFull()`, and
each is re-keyed with `rekeyEdits()` on its own schools-case model. The three generations add to
**$321.8194–387.3701bn** in all 64 specifications under both conventions (1.7e-12bn). The union reproduces
the case's `main_case_bands.csv` `adopted` and `uncorrected_at_adopted_responses` rows, and its
`per_spec.csv` against the mean of the two fill-in methods (576 values, 2.3e-13bn). The chain from the
schools case follows `main_case.cjs`:
- long-run responses, rental assistance, capital core and capital block;
- then the enterprises: the re-key (exactly 0), the surplus at 1 and the enterprise returns.

Its union parts equal the case's `change_at_fixed_specifications` part by part and add to its `change`,
+$63.33bn / +$95.42bn (1.1e-13bn). All three generations still cost others at every specification.
Under (a):
- G1 $93.8 / 78.3bn (was 77.6 / 56.9);
- G2 $127.6 / 153.0bn (was 105.0 / 117.5);
- G3+ $100.5 / 156.1bn (was 75.8 / 117.6).

The second and third-plus generations carry 75–78% of the move. Under (b) the Mexico-born carry 37%. The
regression gate passed first. `sept26_schools`, `sept26` and `sept24` reproduce their four outputs byte
for byte against 0f22f0c, the saved September 26 outputs and ba12f3c. All 58 gates pass, and two full
default runs are byte-identical.

Worker W2 (`generation`), 2026-09-27: `../generation_account_2026_09_24/` on the September 27 case
(`sept27`). Model self-report: claude-opus-5-5.

## What changed in the lane

- **`run_generations.cjs`.**
  - Case `sept27` (package `main_case_long_run_2026_09_27/package.cjs`) is the default, with
    `sept26_schools`, `sept26` and `sept24` behind `--case`.
  - Each generation's payload is its schools-case split (unchanged) plus its eight re-key edits. It
    evaluates every corrected model through `evaluateFull()`; costs come from `cost()`, which is
    `evaluateFull().cost_bn`.
  - The ledger bridge's own copy of the engine state (the `stateOf` mirror near line 611 that the brief
    names) is gone. The bridge calls the package's `stateFor()`, and under `sept27` `evaluateFull()`.
  - The September 24 → schools chain now runs on the schools package and schools-case models whenever the
    case is `sept27`. It still reproduces the schools run's figures exactly.
  - The new chain `change_from_sept26_schools`, the rows beside the account, and the new lane
    `enterprise_rekey` in the lane contributions are added. The eight split sensitivities re-key each
    variant model the way `modelFor()` does.
  - A failed gate now writes nothing. Before, the outputs were written before the exit.
- **`compare_ledger.py`.** With a `sept27` bridge it adds `account_capital_return_*` columns (per person and
  $bn): the capital return inside the proportional, adopted-responses and adopted columns.
- **`run_all.sh`.** The final step now runs the September 27 main case; the September 26 and schools cases
  stay before it. The header gives the older cases' reproduction commands. I did not run the three
  main-case steps: they write outside this lane.
- **`RESULT.md`.** It has a new verdict and a "September 27 case" section on top. The schools section is
  kept below, marked superseded as the default, with its verdict of 2026-09-26.

## The chain from the schools case, by generation

These are net costs to other US residents, $bn a year, at the union's range ends. The ends are
specification 48 (shared allocation, 2%, the low long-run readings) and 11 (personal, 3%, the high
readings); they are the schools case's too (gate). The parts add to each generation's move within
3.6e-14bn. The generations add to the union part by part, and so does every item outside the sum (1.5e-12bn).

| | Schools case | Roads and parks, long run | Rental assistance | Capital, core | Capital, roads and parks | Re-key | Enterprise surplus (receipt) | Capital, enterprises | **September 27** | Change |
|---|---|---|---|---|---|---|---|---|---|---|
| Union | 258.49 / 291.95 | +19.44 / +29.63 | +4.53 / +4.53 | +15.99 / +25.78 | +6.18 / +12.47 | 0.00 / 0.00 | +5.56 / +5.56 | +11.62 / +17.44 | **321.82 / 387.37** | +63.33 / +95.42 |
| (a) G1 | 77.65 / 56.91 | +4.98 / +7.53 | +0.85 / +0.85 | +3.96 / +3.49 | +1.56 / +3.14 | 0.00 / 0.00 | +1.55 / +1.55 | +3.23 / +4.85 | **93.77 / 78.31** | +16.13 / +21.40 |
| (a) G2 | 105.00 / 117.46 | +6.66 / +10.10 | +1.40 / +1.40 | +6.22 / +11.46 | +2.10 / +4.23 | 0.00 / 0.00 | +2.01 / +2.01 | +4.20 / +6.29 | **127.58 / 152.95** | +22.58 / +35.49 |
| (a) G3+ | 75.84 / 117.58 | +7.80 / +12.00 | +2.28 / +2.28 | +5.82 / +10.83 | +2.52 / +5.11 | 0.00 / 0.00 | +2.01 / +2.01 | +4.20 / +6.30 | **100.47 / 156.10** | +24.62 / +38.52 |
| (b) G1 | 135.56 / 155.38 | +6.67 / +10.03 | +1.27 / +1.27 | +6.66 / +10.90 | +2.06 / +4.15 | 0.00 / 0.00 | +2.19 / +2.19 | +4.59 / +6.88 | **159.01 / 190.80** | +23.45 / +35.42 |
| (b) G2 | 67.90 / 66.06 | +6.07 / +9.26 | +1.26 / +1.26 | +4.87 / +7.45 | +1.93 / +3.90 | 0.00 / 0.00 | +1.71 / +1.71 | +3.57 / +5.36 | **87.31 / 95.00** | +19.41 / +28.94 |
| (b) G3+ | 55.02 / 70.52 | +6.70 / +10.34 | +2.01 / +2.01 | +4.46 / +7.43 | +2.18 / +4.42 | 0.00 / 0.00 | +1.66 / +1.66 | +3.46 / +5.20 | **75.49 / 101.57** | +20.47 / +31.05 |

Share of the change by generation, low / high:

- (a) G1 25% / 22%; G2 36% / 37%; G3+ 39% / 40%
- (b) G1 37% / 37%; G2 31% / 30%; G3+ 32% / 33%

## The capital return and the enterprise surplus by generation

The return is an imputed resource cost: the opportunity cost of the capital at 2% / 3%, not a payment. The
enterprise surplus is a receipt: the group's share of the enterprises' operating loss (−$47.46bn), at
response 1. The table gives its group amount on the receipt side and its cost to others. The enterprise
components are keyed by each generation's own receipt share. At the ends, the union's figures equal the
case's `capital_at_end_specifications` and `enterprises.receipt_at_end_specifications` (7.1e-15bn).

| | Capital return | of which core | roads and parks | enterprises | public housing (in enterprises) | state and local | federal | Enterprise surplus, group amount | its share of −$47.46bn | cost to others | re-key's move of the amount |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Union | +33.80 / +55.69 | +15.99 / +25.78 | +6.18 / +12.47 | +11.62 / +17.44 | +0.99 / +1.48 | +32.97 / +53.95 | +0.83 / +1.74 | −5.56 / −5.56 | 0.1172 | +5.56 / +5.56 | +0.15 / +0.15 |
| (a) G1 | +8.75 / +11.47 | +3.96 / +3.49 | +1.56 / +3.14 | +3.23 / +4.85 | +0.27 / +0.41 | +8.52 / +11.00 | +0.23 / +0.47 | −1.55 / −1.55 | 0.0326 | +1.55 / +1.55 | +0.16 / +0.16 |
| (a) G2 | +12.51 / +21.98 | +6.22 / +11.46 | +2.10 / +4.23 | +4.20 / +6.29 | +0.36 / +0.53 | +12.21 / +21.36 | +0.30 / +0.62 | −2.01 / −2.01 | 0.0423 | +2.01 / +2.01 | −0.01 / −0.01 |
| (a) G3+ | +12.54 / +22.24 | +5.82 / +10.83 | +2.52 / +5.11 | +4.20 / +6.30 | +0.36 / +0.53 | +12.24 / +21.59 | +0.30 / +0.65 | −2.01 / −2.01 | 0.0423 | +2.01 / +2.01 | −0.01 / −0.01 |
| (b) G1 | +13.32 / +21.93 | +6.66 / +10.90 | +2.06 / +4.15 | +4.59 / +6.88 | +0.39 / +0.58 | +13.02 / +21.30 | +0.29 / +0.62 | −2.19 / −2.19 | 0.0462 | +2.19 / +2.19 | +0.16 / +0.16 |
| (b) G2 | +10.38 / +16.72 | +4.87 / +7.45 | +1.93 / +3.90 | +3.57 / +5.36 | +0.30 / +0.45 | +10.11 / +16.16 | +0.27 / +0.56 | −1.71 / −1.71 | 0.0360 | +1.71 / +1.71 | −0.01 / −0.01 |
| (b) G3+ | +10.11 / +17.05 | +4.46 / +7.43 | +2.18 / +4.42 | +3.46 / +5.20 | +0.29 / +0.44 | +9.84 / +16.49 | +0.27 / +0.56 | −1.66 / −1.66 | 0.0349 | +1.66 / +1.66 | −0.01 / −0.01 |

The corrections lower G1's population cell of `general_public_services` by $1.35bn and raise G2's and
G3+'s by $0.06bn each. The re-key therefore moves G1's receipt share from 0.0359 to 0.0326 and nearly
nothing for the others. Its effect on the case, −$0.45bn / −$0.60bn for the union, falls on G1
(−$0.49bn / −$0.66bn; the others +$0.02bn / +$0.03bn each).

Roads and parks by line (group amount × response), and the re-key's effect on the case, $bn low / high (`change_from_sept26_schools`):

| | Economic affairs (roads, transit and the rest of the line) | Recreation and culture (parks) | Re-key's effect (case less the same case at model.json's share) |
|---|---|---|---|
| Union | +13.99 / +23.27 | +5.45 / +6.37 | −0.45 / −0.60 |
| (a) G1 | +3.46 / +5.76 | +1.51 / +1.77 | −0.49 / −0.66 |
| (a) G2 | +4.69 / +7.81 | +1.97 / +2.30 | +0.02 / +0.03 |
| (a) G3+ | +5.83 / +9.70 | +1.97 / +2.30 | +0.02 / +0.03 |
| (b) G1 | +4.52 / +7.52 | +2.15 / +2.51 | −0.49 / −0.65 |
| (b) G2 | +4.39 / +7.30 | +1.68 / +1.96 | +0.02 / +0.02 |
| (b) G3+ | +5.08 / +8.45 | +1.62 / +1.90 | +0.02 / +0.02 |

Beside the account, never in the range, $bn at each variant's own union ends (48 / 11 for all three; the union reproduces `main_case_bands.csv`; `beside_the_account`):

| | Without the capital return | Option A, enterprises out | Capital at 7% on every component |
|---|---|---|---|
| Union | 288.02 / 331.68 | 304.63 / 364.37 | 406.31 / 461.62 |
| (a) G1 | 85.02 / 66.84 | 89.00 / 71.92 | 115.64 / 93.61 |
| (a) G2 | 115.07 / 130.97 | 121.38 / 144.65 | 158.85 / 182.26 |
| (a) G3+ | 87.93 / 133.87 | 94.26 / 147.80 | 131.81 / 185.76 |
| (b) G1 | 145.70 / 168.88 | 152.23 / 181.72 | 192.30 / 220.04 |
| (b) G2 | 76.94 / 78.28 | 82.03 / 87.93 | 113.25 / 117.29 |
| (b) G3+ | 65.39 / 84.52 | 70.37 / 94.72 | 100.76 / 124.30 |

## Gates (58 in a `sept27` run, plus the ledger step's 3)

The case is the September 27 main case.
- `summary.json` rounds to `main_case_bands.csv`, and `corrections.json` deep-equals the package's
  payload.
- The specifications carry `meta.responses`: general government, schools, the two long-run lines,
  rental assistance, the enterprise receipt, the rates and option D.
- `corrections.json` is the schools payload in order plus eight re-key edits, which equal `rekeyEdits()`
  on the schools-case model.

The split:
- The lanes rebuild `packageShifts`, and every lane split adds to its union shift (2.1e-12bn).
- No generation's schools-case payload touches `enterprise_surplus`.
- The generations' re-key edits add to the case's eight (2.7e-14bn).
- The uncorrected generation models need no re-key: their receipt share equals their population share to
  1.9e-12, as the union's does (4.6e-12).
- The netted edits add to `corrections.json` in all 278 cells (1.4e-12bn).

The engine:
- The union reproduces `adopted` 321.8194–387.3701 and `uncorrected_at_adopted_responses`
  332.7493–398.3079 (1e-4), and `per_spec.csv` (1e-9).
- The schools payload on its own package reproduces 258.4885–291.9548.
- In all 64 specifications and both conventions, the generations add to the union: corrected,
  uncorrected and the schools case.
- Each generation's payload gives the model `modelFor()` builds (deep-equal).
- Each generation's receipt sits at its own corrected population share.
- The generations' capital return (total, by level, by part) and receipt add to the union's.
- Lane contributions add to each generation's correction.

The bridges:
- The `stateFor()` / `evaluateFull()` evaluation returns `cost()` exactly.
- The production parts equal the attribution.
- The September 24 → schools chain gates all pass. Its union's last two parts equal the schools lane's
  `change`, +57.5705 / +46.2599.
- The band-end ties (48 = 52, 11 = 15) hold in the September 27 case too.

The new chain:
- The case keeps 48 / 11 in both methods.
- The parts add, and the re-key is exactly 0.
- The two long-run lines add to `long_run_responses`.
- The generations add to the union.
- The union equals `change_at_fixed_specifications` (seven parts, the total and three items outside the
  sum) and `change`.
- The union's capital and receipt equal `summary.json` at the ends.
- The rows beside the account reproduce `main_case_bands.csv`.

## Old → new: schools case (0f22f0c) → September 27 case

Every published number in `generation_account_2026_09_24/derived/`, old → new. The file holding each is
named in its heading. The four input files and the 16 other derived files do not change.
`generation_corrections.json` gains the eight re-key edits at the end of each payload, and its `meta`
adds `enterprise_rekey`. `generation_results.csv` gains `capital_return_bn` and
`enterprise_surplus_receipt_bn`. `generation_summary.json` gains `change_from_sept26_schools`,
`beside_the_account` and three `*_capital_return_bn` fields in `ledger_bridge_a`. Its `change_from_sept24`
and `change_from_sept26` keep their values, which are the schools run's (the ends key reads
`sept26_schools` instead of `case`), and `band_end_ties` is unchanged.

### Headline, $bn a year and $ per head (generation_summary.json `conventions`, generation_results.csv)

| Convention, generation | $bn at the union's low end (shared) | $bn at the union's high end (personal) | Own range over the 64 specifications, $bn | $ per member, low / high | $ per adult, low / high |
|---|---|---|---|---|---|
| (a) G1 | 77.65 → **93.77** | 56.91 → **78.31** | 49.3–85.4 → 63.5–109.6 | 6,354 / 4,657 → 7,673 / 6,408 | 6,651 / 4,875 → 8,032 / 6,708 |
| (a) G2 | 105.00 → **127.58** | 117.46 → **152.95** | 105.0–117.5 → 127.6–153.0 | 7,326 / 8,195 → 8,901 / 10,671 | 11,778 / 13,176 → 14,311 / 17,157 |
| (a) G3+ | 75.84 → **100.47** | 117.58 → **156.10** | 75.8–117.6 → 100.5–156.1 | 5,288 / 8,198 → 7,005 / 10,884 | 9,268 / 14,369 → 12,277 / 19,076 |
| (b) G1 | 135.56 → **159.01** | 155.38 → **190.80** | 135.6–155.4 → 159.0–190.8 | 8,043 / 9,218 → 9,434 / 11,320 | 11,612 / 13,309 → 13,620 / 16,343 |
| (b) G2 | 67.90 → **87.31** | 66.06 → **95.00** | 60.9–73.0 → 80.2–102.2 | 5,562 / 5,411 → 7,152 / 7,781 | 7,617 / 7,410 → 9,794 / 10,656 |
| (b) G3+ | 55.02 → **75.49** | 70.52 → **101.57** | 55.0–70.5 → 75.5–101.6 | 4,650 / 5,960 → 6,380 / 8,584 | 6,723 / 8,617 → 9,225 / 12,412 |
| Union (main case) | 258.4885 → **321.8194** | 291.9548 → **387.3701** | | | |

### The corrections against the uncorrected model at the same specification, $bn (`correction_bn`)

Old: against the uncorrected model at the case's responses (general government 0.6000/0.8504, schools 1/1). New: against the uncorrected model at the case's responses (general government 0.6000/0.8504, schools 1/1; roads 0.3840/0.6386, parks 0.8562/1.0000, rental assistance and the enterprise receipt at 1, and the capital return at 2%/3%).

| Generation | (a) low | (a) high | (b) low | (b) high |
|---|---|---|---|---|
| G1 | +4.84 → +2.63 | +4.12 → +1.55 | -1.97 → -4.64 | -2.32 → -5.77 |
| G2 | -5.88 → -6.71 | -7.47 → -8.39 | -3.45 → -4.12 | -3.64 → -4.18 |
| G3+ | -6.05 → -6.85 | -3.38 → -4.10 | -1.68 → -2.17 | -0.76 → -1.00 |

| Uncorrected model at the band ends, $bn | (a) low | (a) high | (b) low | (b) high |
|---|---|---|---|---|
| G1 | 72.81 → 91.14 | 52.79 → 76.76 | 137.53 → 163.65 | 157.70 → 196.57 |
| G2 | 110.88 → 134.29 | 124.93 → 161.34 | 71.36 → 91.44 | 69.70 → 99.17 |
| G3+ | 81.90 → 107.32 | 120.96 → 160.20 | 56.70 → 77.66 | 71.28 → 102.57 |

### Allocation swap, $bn (`allocation_swap`)

| | Low end (shared) | Low end, personal instead | High end (personal) | High end, shared instead |
|---|---|---|---|---|
| (a) G1 | 77.6 → 93.8 | 49.3 → 63.5 | 56.9 → 78.3 | 85.4 → 109.6 |
| (a) G2 | 105.0 → 127.6 | 111.4 → 135.1 | 117.5 → 153.0 | 111.0 → 144.8 |
| (a) G3+ | 75.8 → 100.5 | 112.1 → 137.8 | 117.6 → 156.1 | 81.3 → 118.1 |
| (b) G1 | 135.6 → 159.0 | 145.9 → 169.6 | 155.4 → 190.8 | 145.1 → 180.1 |
| (b) G2 | 67.9 → 87.3 | 60.9 → 80.2 | 66.1 → 95.0 | 73.0 → 102.2 |
| (b) G3+ | 55.0 → 75.5 | 65.9 → 86.7 | 70.5 → 101.6 | 59.6 → 90.3 |

### Sensitivities of the flagged and literal rules, $bn: central (lowest–highest alternative) (`sensitivities`)

Old: 8 alternatives. New: 8.

| | (a) low | (a) high | (b) low | (b) high |
|---|---|---|---|---|
| G1 | 77.6 (74.4–79.3) → 93.8 (90.7–95.1) | 56.9 (53.5–58.2) → 78.3 (75.2–79.4) | 135.6 (132.4–137.0) → 159.0 (156.2–160.0) | 155.4 (152.3–156.6) → 190.8 (188.2–191.2) |
| G2 | 105.0 (103.5–107.0) → 127.6 (126.1–129.6) | 117.5 (116.7–121.2) → 153.0 (152.3–156.7) | 67.9 (66.5–71.1) → 87.3 (85.9–90.5) | 66.1 (65.3–69.6) → 95.0 (94.6–98.4) |
| G3+ | 75.8 (75.0–77.1) → 100.5 (100.4–101.5) | 117.6 (117.0–118.1) → 156.1 (155.5–156.6) | 55.0 (54.5–55.5) → 75.5 (75.2–76.0) | 70.5 (70.0–71.0) → 101.6 (100.7–102.0) |

Largest move of any generation under any alternative: 3.71 → 3.71 $bn.

Each alternative's move against the central split (new, $bn, (a) low / (a) high / (b) low / (b) high, G1; G2; G3+):

- `benefits_to_g1`: +0.23 / -0.20 / +0.09 / -0.12; -0.33 / -0.16 / -0.34 / -0.21; +0.10 / +0.36 / +0.26 / +0.32
- `benefits_to_usborn`: -0.04 / -0.29 / -0.08 / -0.11; +0.09 / +0.26 / +0.20 / +0.21; -0.06 / +0.03 / -0.12 / -0.10
- `justice_per_adult`: +0.30 / +0.30 / +0.30 / +0.30; -0.18 / -0.18 / -0.18 / -0.18; -0.12 / -0.12 / -0.12 / -0.12
- `foster_care_by_children`: +0.21 / +0.21 / -0.11 / -0.11; -0.10 / -0.10 / +0.11 / +0.11; -0.11 / -0.11 / -0.01 / -0.01
- `status_rules_all_to_g1`: +1.31 / -0.63 / +0.95 / -0.63; -1.53 / +0.16 / -1.39 / +0.16; +0.22 / +0.47 / +0.44 / +0.47
- `fill_ins_by_imputed_dollars`: -3.06 / -3.08 / -2.85 / -2.62; +2.05 / +3.71 / +3.16 / +3.45; +1.01 / -0.63 / -0.30 / -0.83
- `stack_scaling_by_union_factor`: +0.10 / +1.04 / +0.24 / +0.40; -0.08 / -0.67 / -0.15 / -0.35; -0.03 / -0.37 / -0.10 / -0.05
- `consumption_key_by_old_key_shares`: -0.24 / -0.29 / -0.15 / -0.23; -0.05 / -0.02 / -0.34 / -0.24; +0.29 / +0.31 / +0.49 / +0.47

Lean of the central rules, first generation: alternatives that would raise / lower its cost (largest move):

- old: (a) low: 5 up (≤1.7), 3 down (≤3.3); (a) high: 4 up (≤1.3), 4 down (≤3.4); (b) low: 4 up (≤1.4), 4 down (≤3.1); (b) high: 3 up (≤1.2), 5 down (≤3.1)
- new: (a) low: 5 up (≤1.3), 3 down (≤3.1); (a) high: 3 up (≤1.0), 5 down (≤3.1); (b) low: 4 up (≤0.9), 4 down (≤2.9); (b) high: 2 up (≤0.4), 6 down (≤2.6)

### Lane contributions by generation, $bn low / high (`lanes`)

| Lane | (a) G1 | (a) G2 | (a) G3+ | (b) G1 | (b) G2 | (b) G3+ |
|---|---|---|---|---|---|---|
| stack | +14.52 / +17.68 → +12.87 / +15.22 | +2.65 / -0.11 → +2.27 / -0.58 | +2.24 / +3.26 → +2.13 / +3.12 | +15.55 / +17.73 → +13.66 / +15.00 | +1.31 / -0.13 → +1.05 / -0.45 | +2.55 / +3.22 → +2.57 / +3.20 |
| cbo | +1.13 / +0.98 (same) | +5.15 / +3.88 (same) | +3.04 / +3.54 (same) | +1.57 / +0.75 (same) | +3.88 / +4.04 (same) | +3.87 / +3.61 (same) |
| ota | -0.09 / -0.12 (same) | -0.16 / -0.14 (same) | -0.12 / -0.08 (same) | -0.11 / -0.12 (same) | -0.15 / -0.14 (same) | -0.10 / -0.08 (same) |
| row1 | -3.97 / -11.39 (same) | -6.54 / -2.23 (same) | -3.72 / -0.62 (same) | -8.87 / -10.35 (same) | -3.53 / -2.91 (same) | -1.83 / -0.97 (same) |
| medical | -5.48 / -5.45 → -5.58 / -5.60 | -5.26 / -5.27 → -5.30 / -5.33 | -6.05 / -6.06 → -6.09 / -6.11 | -6.29 / -6.27 → -6.40 / -6.43 | -5.07 / -5.07 → -5.10 / -5.12 | -5.44 / -5.44 → -5.46 / -5.48 |
| education | +1.31 / +4.80 → +1.39 / +5.26 | -1.07 / -2.79 → -1.14 / -3.11 | +0.34 / -1.40 → +0.36 / -1.58 | -0.87 / -1.11 → -0.93 / -1.26 | +0.31 / +0.89 → +0.33 / +0.95 | +1.14 / +0.83 → +1.21 / +0.88 |
| benefits | +0.46 / +0.68 → +0.05 / +0.27 | +0.90 / +0.77 → +0.22 / +0.09 | +0.79 / +0.57 → -0.30 / -0.52 | +0.73 / +0.73 → +0.12 / +0.12 | +0.87 / +0.77 → +0.27 / +0.17 | +0.55 / +0.51 → -0.41 / -0.45 |
| justice | +0.53 / +0.53 → +0.54 / +0.55 | +0.81 / +0.81 → +0.82 / +0.83 | +0.69 / +0.69 → +0.70 / +0.71 | +0.53 / +0.53 → +0.54 / +0.55 | +0.81 / +0.81 → +0.82 / +0.83 | +0.69 / +0.69 → +0.70 / +0.71 |
| constants | -2.61 / -2.62 (same) | -1.10 / -1.12 (same) | -1.35 / -1.36 (same) | -2.80 / -2.82 (same) | -1.08 / -1.10 (same) | -1.18 / -1.19 (same) |
| row8_finite | -0.03 / -0.03 (same) | -0.04 / -0.04 (same) | -0.04 / -0.04 (same) | -0.04 / -0.04 (same) | -0.03 / -0.03 (same) | -0.03 / -0.03 (same) |
| consumption_key | -0.93 / -0.93 → -0.58 / -0.30 | -1.23 / -1.23 → -0.93 / -0.70 | -1.89 / -1.89 → -1.49 / -1.19 | -1.36 / -1.36 → -0.88 / -0.52 | -0.77 / -0.77 → -0.59 / -0.44 | -1.92 / -1.92 → -1.53 / -1.23 |
| enterprise_rekey | new -0.49 / -0.66 | new +0.02 / +0.03 | new +0.02 / +0.03 | new -0.49 / -0.65 | new +0.02 / +0.02 | new +0.02 / +0.02 |
| Total correction | +4.84 / +4.12 → +2.63 / +1.55 | -5.88 / -7.47 → -6.71 / -8.39 | -6.05 / -3.38 → -6.85 / -4.10 | -1.97 / -2.32 → -4.64 / -5.77 | -3.45 / -3.64 → -4.12 / -4.18 | -1.68 / -0.76 → -2.17 / -1.00 |

Union contribution of each lane (sum of the generations under (a)), $bn low / high:

- stack: +19.41 / +20.82 → +17.27 / +17.76
- cbo: +9.32 / +8.40 → +9.32 / +8.40
- ota: -0.36 / -0.34 → -0.36 / -0.34
- row1: -14.23 / -14.23 → -14.23 / -14.23
- medical: -16.80 / -16.78 → -16.97 / -17.03
- education: +0.58 / +0.61 → +0.62 / +0.58
- benefits: +2.15 / +2.02 → -0.02 / -0.16
- justice: +2.03 / +2.03 → +2.06 / +2.08
- constants: -5.06 / -5.10 → -5.06 / -5.10
- row8_finite: -0.10 / -0.10 → -0.10 / -0.10
- consumption_key: -4.05 / -4.05 → -3.00 / -2.19
- enterprise_rekey: new -0.45 / -0.60

### Ledger comparison, account rows, $ per person a year (ledger_comparison.csv)

| Row | G1 shared | G2 shared | G3+ shared | G1 personal | G2 personal | G3+ personal |
|---|---|---|---|---|---|---|
| Direct lines at average cost | -7,647 → -8,747 | -8,894 → -10,121 | -7,027 → -8,332 | -5,763 → -7,049 | -9,816 → -11,668 | -9,701 → -11,631 |
| The same lines at the adopted responses | -6,680 → -8,180 | -7,906 → -9,539 | -5,854 → -7,627 | -4,796 → -6,758 | -8,828 → -11,369 | -8,529 → -11,265 |
| Plus the production term (the uncorrected model at the same specification) | -5,958 → -7,458 | -7,736 → -9,369 | -5,710 → -7,482 | -4,320 → -6,281 | -8,716 → -11,257 | -8,434 → -11,170 |
| Plus the corrections (adopted main case) | -6,354 → -7,673 | -7,326 → -8,901 | -5,288 → -7,005 | -4,657 → -6,408 | -8,195 → -10,671 | -8,198 → -10,884 |
| Of which the capital return, proportional | new -821 | new -923 | new -925 | new -1,006 | new -1,548 | new -1,548 |
| Of which the capital return, adopted responses | new -773 | new -874 | new -866 | new -1,006 | new -1,548 | new -1,548 |
| Of which the capital return, adopted | new -716 | new -873 | new -874 | new -939 | new -1,534 | new -1,551 |

Ledger rows (published gap, eight-band gaps, own balance) do not change: they are the September 19 ledger's.

### Numbers quoted in the lane RESULT's prose

- Minors moved to their parents' generation shift onto G1: $57.9–98.5bn → $65.2–112.5bn.
- Household allocation rule, (a), G1 and G3+ at the two ends: $28.4–36.3bn → $30.2–38.0bn.
- (b) second-generation adult as a share of a Mexico-born adult (per adult): 56–66% → 65–72%.
- old: corrections at the low end, $ per person (G1, G2, G3+): -396, +411, +422; production term 722, 169, 144; marginal responses take off 967, 988, 1,172, 967, 988, 1,172 (shared G1–G3+, personal G1–G3+); direct lines at the responses differ from the ledger's own balance by 751–2,025 (shared); account G2 below G1 by 972 (shared); G3+ below G2 by 3 (personal).
- new: corrections at the low end, $ per person (G1, G2, G3+): -216, +468, +478; production term 722, 169, 144; marginal responses take off 568, 582, 706, 292, 299, 366 (shared G1–G3+, personal G1–G3+); direct lines at the responses differ from the ledger's own balance by 2,251–3,658 (shared); account G2 below G1 by 1,228 (shared); G3+ below G2 by 213 (personal).

### Consumption key by generation (consumption_key_by_generation.json)

| | Old key share | Saving only | Saving and corridor | Receipts change at the union's phi, $bn: saving / remittances / net |
|---|---|---|---|---|
| Union | 8.104% | 8.894% | 8.599% | +4.052 (net) |
| (a) G1 | 2.204% | 2.600% | 2.377% | +4.372 / -3.031 / +1.341 |
| (a) G2 | 2.654% | 2.909% | 2.798% | +2.909 / -1.870 / +1.039 |
| (a) G3+ | 3.246% | 3.385% | 3.423% | +2.015 / -0.344 / +1.671 |
| (b) G1 | 2.787% | 3.294% | 3.017% | +5.504 / -3.784 / +1.720 |
| (b) G2 | 2.507% | 2.657% | 2.597% | +1.858 / -1.251 / +0.607 |
| (b) G3+ | 2.809% | 2.943% | 2.984% | +1.934 / -0.210 / +1.725 |

Own-factor remainder over the four lines: max 0.306 $bn; ratio-type lanes' remainder max 0.4315 → 0.4315 $bn.

## Files

Covered:
- `generation_account_2026_09_24/`: `run_generations.cjs`, `compare_ledger.py`, `run_all.sh` and
  `RESULT.md` (edited);
- `derived/generation_results.csv`, `generation_summary.json`, `generation_corrections.json` and
  `ledger_comparison.csv` (rewritten by the pipeline);
- this file.

Skipped:
- the other 16 derived files, which are unchanged (steps 0–4 byte-identical);
- the main-case lanes and the engine, which are read-only (I did not run their `main_case.cjs`);
- `research/`, `decisions/`, INDEX, FAQ, ladder and `CLAUDE.md`, which are not mine to edit (see below).

## Judgment calls

- **The per-generation re-key.** Each generation's receipt goes to its own corrected population share,
  read from its `general_public_services` population cell. This is `rekeyEdits()` on the generation's
  schools-case model, as the case's "For consumers" item 2 says. The uncorrected generation models take
  none: their shares already agree, as the union's do.
- **The re-key as its own lane.** `enterprise_rekey` in `lanes` makes the lane contributions add to the
  correction, which now includes it.
- **The ledger bridge.** Under `sept27` the capital return sits inside `proportional_fiscal_bn`,
  `adopted_responses_fiscal_bn`, the uncorrected and adopted columns, following the brief's item 3 (part
  of the direct fiscal response). It is also reported alone. The September 19 ledger has no capital
  return, so a reader comparing the two should subtract it (`account_capital_return_*`).
- **Beside the account.** The rows are without the capital return, option A and 7%. Each takes that
  variant's own union ends, and all three are 48 / 11. I skipped rental assistance at 0: the chain already
  gives its part by generation.
- **The two conventions and the allocation rule** are unchanged conventions, not estimates. The capital
  return follows the same allocation as its keyed lines, so school capital follows the pupils at the
  personal high end.

## Notes for the parent

- **Commit** (explicit paths): the four edited files and four outputs in `generation_account_2026_09_24/`,
  plus this file. A possible message: `[analysis] Split the Sept 27 case by generation — all three still
  cost`.
- **Research record to update** (not edited here). These quote the schools-case split:
  - `research/immigration-adopted-account-by-generation-2026-09-25.md` (lines 7–21, 167);
  - `research/immigration-INDEX.md` (lines 97–99);
  - `research/immigration-objections-faq-2026-09-21.md` (line 229);
  - ladder entry 224;
  - `CLAUDE.md` (its pointer to `generation_results.csv`).

  The new figures are in the verdict and the chain table above.
- **Consumers of `derived/`**, which now holds `sept27`:
  - `late_arrival_account_line_2026_09_27/verify.py` reads `generation_summary.json` `case`. Its `sept27`
    check against G1 now activates: (a) 93.772592 / 78.312585, (b) 159.014731 / 190.801312.
  - `generation_carryover_2026_09_27/summarize.py` and `verify.py` read `per_adult_usd` from
    `generation_results.csv`; their outputs move on a rerun.
  - The world-ledger lane reads the same CSV.
  - The schools-case outputs are at 0f22f0c, or `--case sept26_schools --out-dir DIR`.
- **The late-arrival lane's `run_cells.cjs`** is a copy of this script at 0f22f0c. It still has the
  `stateOf` mirror that the brief retires.
- **Inherited, not repaired:** the housing-subsidy key mismatch (conceptual audit §7) passes into each
  generation.

## Progress (append-only)

- 21:55 JST. Regression gate on the default as it stood (`sept26_schools`): the full pipeline (`run_all.sh` minus the
  two main-case steps) exited 0, and all 20 tracked files in `generation_account_2026_09_24/derived/` are
  byte-identical to HEAD (0f22f0c's outputs). This also covers the Sept 24 package's `stateFor` refactor
  (1edd418, 8d87481), which landed after those outputs.
- 22:45 JST. `run_generations.cjs` takes `--case sept27` (the default) and `compare_ledger.py` reports the capital return
  in the ledger bridge. The older cases reproduce byte for byte into scratch: `sept26_schools` against HEAD (0f22f0c),
  `sept26` against the saved Sept 26 outputs and `sept24` against ba12f3c (all four output files each). The `sept27`
  run passes all 59 gates.
- 22:50 JST. Two full default runs (steps 0-6, derived/ in place) exit 0 and leave all 20 tracked derived files
  byte-identical to each other. The three main-case steps were not run: they write outside this lane.
- 23:17 JST. Correction to the 22:45 entry: a `sept27` run has 58 gates; the 59th check mark is the closing
  "all gates passed" line. After formatting edits to `run_generations.cjs`, all four cases were re-run into
  scratch: the three older ones are byte-identical to their references and `sept27` equals `derived/`. Two
  more full default runs (23:15, 23:16) exit 0 with all 20 tracked derived files byte-identical. `git status`
  on the four main-case lanes is clean.
