claude-opus-5-5

**Verdict:** Done, not committed. The generation account (`../generation_account_2026_09_24/`) now
runs on the main case with schools at full average cost (`main_case_schools_full_2026_09_26`) by
default. The three generations add to **$258.4885–291.9548bn** in all 64 specifications under both
conventions, and the uncorrected union reproduces $265.5903–298.6797bn. `--case sept26` keeps the
one-year scenario and `--case sept24` the September 24 record (byte for byte against HEAD). From
September 24, schools at full cost add $62.1bn at the low end and $48.5bn at the high end to the
union. Under (a) the second and third-plus generations carry 76–91% of that; under (b) the Mexico-born
carry 43–44%. Every generation remains a net cost at every specification. Every gate passes, and two
full runs are byte-identical.

Model self-report: claude-opus-5-5. Worker W2 (`generation`), 2026-09-26.

## September 24 → schools case, by generation

Net cost to other US residents, $bn a year, low / high end. The September 24 ends are specifications
56 and 7. The schools case's ends are 48 and 11, because at a school response of 1 the school-share
bound flips. Each move splits exactly into five parts (`generation_summary.json` →
`change_from_sept24`; they add within 1.5e-13bn). The responses act at the September 24 end's
specification, and "band end" then moves the end to the case's specification: the brief's bridge
order.

| $bn, low / high | Sept 24 | Schools at 1 | General government | Band end | Row 8 at 0.949 | Consumption key | **Schools case** | Move |
|---|---|---|---|---|---|---|---|---|
| (a) G1 | 63.79 / 53.56 | +14.87 / +4.14 | +0.13 / +0.14 | −0.18 / +0.04 | −0.03 / −0.03 | −0.93 / −0.93 | **77.65 / 56.91** | +13.85 / +3.35 |
| (a) G2 | 81.74 / 95.12 | +24.68 / +23.02 | +0.17 / +0.18 | −0.32 / +0.41 | −0.04 / −0.04 | −1.23 / −1.23 | **105.00 / 117.46** | +23.26 / +22.34 |
| (a) G3+ | 55.34 / 97.64 | +22.54 / +21.32 | +0.17 / +0.18 | −0.29 / +0.37 | −0.04 / −0.04 | −1.89 / −1.89 | **75.84 / 117.58** | +20.50 / +19.95 |
| (b) G1 | 110.22 / 134.76 | +26.91 / +21.46 | +0.19 / +0.19 | −0.35 / +0.37 | −0.04 / −0.04 | −1.36 / −1.36 | **135.56 / 155.38** | +25.34 / +20.62 |
| (b) G2 | 50.18 / 52.96 | +18.62 / +13.53 | +0.15 / +0.15 | −0.24 / +0.22 | −0.03 / −0.03 | −0.77 / −0.77 | **67.90 / 66.06** | +17.72 / +13.10 |
| (b) G3+ | 40.47 / 58.60 | +16.56 / +13.50 | +0.14 / +0.15 | −0.20 / +0.22 | −0.03 / −0.03 | −1.92 / −1.92 | **55.02 / 70.52** | +14.55 / +11.92 |
| Union | 200.88 / 246.32 | +62.08 / +48.49 | +0.47 / +0.49 | −0.79 / +0.81 | −0.10 / −0.10 | −4.05 / −4.05 | **258.49 / 291.95** | +57.61 / +45.64 |

**The school line's own split.** The first column below is what the case charges each generation for
schools at its band end: the cost at a school response of 1 less the cost at 0
(`school_line_at_case_bn`). Each generation's share of the line equals its share of the "Schools at 1"
move above, since both scale the same school costs under the same allocation (the gate checks that
the generations' parts add to the union's).

| $bn, low / high | School line in the case | Share of the union's line and of its move | Schools at 1 (the move) |
|---|---|---|---|
| (a) G1 | 33.22 / 14.74 | 24% / 9% | +14.87 / +4.14 |
| (a) G2 | 55.15 / 81.90 | 40% / 47% | +24.68 / +23.02 |
| (a) G3+ | 50.36 / 75.84 | 36% / 44% | +22.54 / +21.32 |
| (b) G1 | 60.13 / 76.34 | 43% / 44% | +26.91 / +21.46 |
| (b) G2 | 41.60 / 48.11 | 30% / 28% | +18.62 / +13.53 |
| (b) G3+ | 37.00 / 48.02 | 27% / 28% | +16.56 / +13.50 |
| Union | 138.73 / 172.47 | 100% | +62.08 / +48.49 |

- Under (a), children count in their own generation, so the line falls mostly on the second and
  third-plus generations. At the shared low end, parents carry part of their children's costs
  through the SPM unit's equal split: the Mexico-born take 24% there and 9% at the personal high end.
- Under (b), minors count with their parents, and the Mexico-born take 43–44%.
- **The bridge order matters for the split between schools and the band end, not for their sum.**
  Taken at the case's own end specifications, schools add $51.3bn / $63.8bn to the union and the end
  move +$10.0bn / −$14.5bn. In both orders the two sum to +$61.3bn / +$49.3bn, and the generations'
  shares of the school term do not change. (Union figures, computed from the package with the end
  moved first at the September 24 responses.)
- Over the September 26 one-year scenario the union moves +$57.6bn / +$46.3bn, as the decision
  states; that bridge carries only the school response and the band end.

## Headline, schools case

| $bn a year, low / high | G1 | G2 | G3+ | All three |
|---|---|---|---|---|
| (a) own generation | 77.65 / 56.91 | 105.00 / 117.46 | 75.84 / 117.58 | 258.49 / 291.95 |
| (a) $ per member | 6,354 / 4,657 | 7,326 / 8,195 | 5,288 / 8,198 | 6,321 / 7,139 |
| (b) minors with parents | 135.56 / 155.38 | 67.90 / 66.06 | 55.02 / 70.52 | 258.49 / 291.95 |
| (b) $ per adult | 11,612 / 13,309 | 7,617 / 7,410 | 6,723 / 8,617 | 8,984 / 10,147 |

Every generation's lowest cost over the 64 specifications is positive: (a) $49.3bn, $105.0bn and
$75.8bn; (b) $135.6bn, $60.9bn and $55.0bn. Under the eight alternative split rules no generation
moves by more than $3.7bn.

## How the edits split, and why

- **Responses** (general government 0.6000/0.8504, schools 1/1). They are engine state, so each
  generation's model responds on its own lines. They come from the package's `MAIN_SPECS`, gated
  against `corrections.json` → `meta.responses`. No 0.63/0.66 remains in a computation: the lane's
  only literal responses are `correction_rules.py`'s `SHELTER_GG` 0.59/0.84, which mirror the
  September 24 package's shelter keying (`main_case_2026_09_24/package.cjs:323`). That keying is
  inherited and is not a service response.
- **Row 8** (−$0.10bn on the constants line) splits as the lane splits audit row 8, by population
  (`correction_rules.json` → `constants.row8`). This is the brief's rule.
- **The consumption key** (spec `both_corridor_net_h2`, −$4.05bn) is split exactly, with the same
  numbers as on September 26. The consumption lane's frame is this lane's, person for person.
  `consumption_split.py` rebuilds the lane's 40 union edits from generation totals with a maximum
  difference of 0.0. Each generation's saving part then takes its own stack factor (0.85, 0.98 and
  0.99 under (a)); the corridor's dollars are not scaled. The alternatives, the union's factor and the
  old key's shares, run as sensitivities. They move no generation by more than $0.51bn against the
  central split.

## The case switch

`run_generations.cjs` has one table of cases, and repointing is a one-line change:

```js
const CASES = { sept26_schools: "main_case_schools_full_2026_09_26", sept26: "main_case_2026_09_26", sept24: "main_case_2026_09_24" };
const CASE = arg("--case", "sept26_schools");
```

The package, `corrections.json`, `summary.json` and the gate bands all come from `CASES[CASE]`.
`--out-dir DIR` writes elsewhere (`compare_ledger.py` takes the same flag).

## Gates

| Gate | Result |
|---|---|
| a. Regression, before any change: the lane's steps as they stood | **Pass.** Exit 0, every gate passed, and all 19 files in `derived/` equalled HEAD (sha256). The last `run_all.sh` step, which rewrites `main_case_2026_09_24/`, was skipped as outside my boundary. |
| b. `--case sept24 --out-dir DIR` on the final code against HEAD | **Pass.** `generation_results.csv`, `generation_summary.json`, `generation_corrections.json` and `ledger_comparison.csv` are identical. The other 15 derived files do not depend on the case and still equal HEAD. |
| `corrections.json` is the schools package's payload | **Pass**, deep-equal |
| Specifications carry `meta.responses` | **Pass**: general government 0.6000/0.8504, schools 1/1 |
| Lanes rebuild the package's `packageShifts` (row 8 included), both fill-in methods | **Pass** |
| Consumption split: frames, key shares against `key_specs.csv` (1e-12), union edits against `payloads.json` | **Pass**: 40 cells, maximum difference 0.0bn |
| Every split adds to its union shift or cell | **Pass**: 2.1e-12bn |
| Netted generation edits add to `corrections.json`, 270 cells | **Pass**: 1.4e-12bn (a), 1.3e-12bn (b) |
| c. Corrected union reproduces $258.4885–291.9548bn (1e-4) | **Pass** |
| c. Uncorrected union reproduces $265.5903–298.6797bn (1e-4) | **Pass** |
| The three generations add to the union, 64 specifications, both conventions | **Pass**: corrected 1.4e-12bn, uncorrected 1.1e-13bn |
| September 24 cross-check inside the run | **Pass**: $200.8752–246.3184bn. The nine lanes' generation payloads add to the September 24 `corrections.json` (1.4e-12bn), and their costs add in all 64 specifications (1.5e-12bn). |
| Move from September 24 = schools + general government + band end + row 8 + consumption key; generations' school parts add to the union's | **Pass**: 1.5e-13bn |
| `--case sept26` | **Pass**: 27 gates. It reproduces $200.9180–245.6949bn and $207.4046–253.1859bn, and its CSV, payload and ledger comparison equal the earlier September 26 run. |
| d. Determinism: the full pipeline twice | **Pass**: all 20 derived files byte-identical; 186 gate lines per run, none failed |
| Other lanes untouched | **Pass**: no new or modified files in the package lanes or the consumption lane |

## Files changed

All in `../generation_account_2026_09_24/`, none committed:
- `consumption_split.py` (new): step 4b, the consumption key's correction by generation.
- `run_generations.cjs`:
  - the case table (`CASES`, default `sept26_schools`) and `--out-dir`;
  - the lanes `row8_finite` and `consumption_key`;
  - the uncorrected-union gate;
  - `change_from_sept24`, with the band-end term and the school line;
  - the sensitivity `consumption_key_by_old_key_shares`.

  After sept24, the uncorrected model at the same specification is named `uncorrected_*`
  (`uncorrected_same_spec_bn`, `uncorrected_cost_bn`, `uncorrected_bn`). Under sept24 it stays
  `sept23_*`.
- `compare_ledger.py`: `--out-dir`. The column is `account_uncorrected` after sept24 and
  `account_sept23` under it.
- `run_all.sh`: the consumption step, the final check on
  `main_case_schools_full_2026_09_26/main_case.cjs`, and the commands for the other cases.
- `RESULT.md`: a schools-case section on top. The September 24 text is kept below it under
  "September 24 record (superseded 2026-09-26)".
- `derived/`: `generation_results.csv`, `generation_summary.json`, `generation_corrections.json` and
  `ledger_comparison.csv` hold the schools case. `consumption_key_by_generation.json` is new. The other
  15 files are unchanged.

## Old → new, every published number

Old is the September 24 case (HEAD, reproduced by `--case sept24`). New is the schools case in
`derived/`. The decomposition and school-line tables are above. Generated by a scratch script from
the two runs' outputs.

### Headline, $bn a year and $ per head (generation_summary.json `conventions`, generation_results.csv)

| Convention, generation | $bn low end | $bn high end | Own range, $bn | $ per member, low / high | $ per adult, low / high |
|---|---|---|---|---|---|
| (a) G1 | 63.79 → **77.65** | 53.56 → **56.91** | 44.7–74.8 → 49.3–85.4 | 5,220 / 4,383 → 6,354 / 4,657 | 5,464 / 4,588 → 6,651 / 4,875 |
| (a) G2 | 81.74 → **105.00** | 95.12 → **117.46** | 81.7–95.1 → 105.0–117.5 | 5,703 / 6,636 → 7,326 / 8,195 | 9,169 / 10,670 → 11,778 / 13,176 |
| (a) G3+ | 55.34 → **75.84** | 97.64 → **117.58** | 55.3–97.6 → 75.8–117.6 | 3,859 / 6,808 → 5,288 / 8,198 | 6,763 / 11,931 → 9,268 / 14,369 |
| (b) G1 | 110.22 → **135.56** | 134.76 → **155.38** | 110.2–134.8 → 135.6–155.4 | 6,539 / 7,995 → 8,043 / 9,218 | 9,441 / 11,543 → 11,612 / 13,309 |
| (b) G2 | 50.18 → **67.90** | 52.96 → **66.06** | 44.0–59.3 → 60.9–73.0 | 4,110 / 4,338 → 5,562 / 5,411 | 5,629 / 5,941 → 7,617 / 7,410 |
| (b) G3+ | 40.47 → **55.02** | 58.60 → **70.52** | 40.5–58.6 → 55.0–70.5 | 3,420 / 4,952 → 4,650 / 5,960 | 4,945 / 7,160 → 6,723 / 8,617 |
| Union (main case) | 200.8752 → **258.4885** | 246.3184 → **291.9548** | | | |

### The corrections against the uncorrected model at the same specification, $bn (`correction_bn`)

Old: against the September 23 case (the uncorrected model at 0.59/0.84 and 0.63/0.66). New: against the uncorrected model at the case's responses.

| Generation | (a) low | (a) high | (b) low | (b) high |
|---|---|---|---|---|
| G1 | +6.04 → +4.84 | +4.33 → +4.12 | +0.40 → -1.97 | -0.66 → -2.32 |
| G2 | -4.20 → -5.88 | -6.05 → -7.47 | -2.69 → -3.45 | -3.35 → -3.64 |
| G3+ | -4.17 → -6.05 | -1.60 → -3.38 | -0.04 → -1.68 | +0.69 → -0.76 |

| Uncorrected model at the band ends, $bn | (a) low | (a) high | (b) low | (b) high |
|---|---|---|---|---|
| G1 | 57.76 → 72.81 | 49.23 → 52.79 | 109.82 → 137.53 | 135.42 → 157.70 |
| G2 | 85.94 → 110.88 | 101.18 → 124.93 | 52.87 → 71.36 | 56.31 → 69.70 |
| G3+ | 59.51 → 81.90 | 99.24 → 120.96 | 40.51 → 56.70 | 57.90 → 71.28 |

### Allocation swap, $bn (`allocation_swap`)

| | Low end (shared) | Low end, personal instead | High end (personal) | High end, shared instead |
|---|---|---|---|---|
| (a) G1 | 63.8 → 77.6 | 44.7 → 49.3 | 53.6 → 56.9 | 74.8 → 85.4 |
| (a) G2 | 81.7 → 105.0 | 82.6 → 111.4 | 95.1 → 117.5 | 93.0 → 111.0 |
| (a) G3+ | 55.3 → 75.8 | 86.1 → 112.1 | 97.6 → 117.6 | 65.6 → 81.3 |
| (b) G1 | 110.2 → 135.6 | 119.2 → 145.9 | 134.8 → 155.4 | 125.5 → 145.1 |
| (b) G2 | 50.2 → 67.9 | 44.0 → 60.9 | 53.0 → 66.1 | 59.3 → 73.0 |
| (b) G3+ | 40.5 → 55.0 | 50.2 → 65.9 | 58.6 → 70.5 | 48.6 → 59.6 |

### Sensitivities of the flagged and literal rules, $bn: central (lowest–highest alternative) (`sensitivities`)

Old: 7 alternatives. New: 8 (consumption_key_by_old_key_shares added).

| | (a) low | (a) high | (b) low | (b) high |
|---|---|---|---|---|
| G1 | 63.8 (60.7–65.5) → 77.6 (74.4–79.3) | 53.6 (50.3–54.9) → 56.9 (53.5–58.2) | 110.2 (107.2–111.6) → 135.6 (132.4–137.0) | 134.8 (131.8–135.9) → 155.4 (152.3–156.6) |
| G2 | 81.7 (80.2–83.7) → 105.0 (103.5–107.0) | 95.1 (94.4–98.8) → 117.5 (116.7–121.2) | 50.2 (48.8–53.3) → 67.9 (66.5–71.1) | 53.0 (52.3–56.5) → 66.1 (65.3–69.6) |
| G3+ | 55.3 (54.5–56.5) → 75.8 (75.0–77.1) | 97.6 (97.1–98.1) → 117.6 (117.0–118.1) | 40.5 (39.9–40.9) → 55.0 (54.5–55.5) | 58.6 (58.0–59.1) → 70.5 (70.0–71.0) |

Largest move of any generation under any alternative: 3.66 → 3.71 $bn.

Each alternative's move against the central split (new, $bn, (a) low / (a) high / (b) low / (b) high, G1; G2; G3+):

- `benefits_to_g1`: +1.69 / +1.26 / +1.39 / +1.19; -0.88 / -0.72 / -0.84 / -0.71; -0.80 / -0.55 / -0.54 / -0.48
- `benefits_to_usborn`: -0.47 / -0.72 / -0.74 / -0.77; +0.26 / +0.42 / +0.46 / +0.47; +0.21 / +0.30 / +0.29 / +0.31
- `justice_per_adult`: +0.29 / +0.29 / +0.29 / +0.29; -0.18 / -0.18 / -0.18 / -0.18; -0.11 / -0.11 / -0.11 / -0.11
- `foster_care_by_children`: +0.21 / +0.21 / -0.11 / -0.11; -0.10 / -0.10 / +0.11 / +0.11; -0.11 / -0.11 / -0.01 / -0.01
- `status_rules_all_to_g1`: +1.31 / -0.63 / +0.95 / -0.63; -1.53 / +0.16 / -1.39 / +0.16; +0.22 / +0.47 / +0.44 / +0.47
- `fill_ins_by_imputed_dollars`: -3.27 / -3.44 / -3.15 / -3.06; +2.02 / +3.71 / +3.22 / +3.57; +1.26 / -0.27 / -0.07 / -0.50
- `stack_scaling_by_union_factor`: +0.19 / +1.07 / +0.37 / +0.53; -0.07 / -0.64 / -0.15 / -0.36; -0.12 / -0.44 / -0.22 / -0.17
- `consumption_key_by_old_key_shares`: -0.17 / -0.17 / -0.03 / -0.03; -0.10 / -0.10 / -0.48 / -0.48; +0.26 / +0.26 / +0.51 / +0.51

Lean of the central rules, first generation: alternatives that would raise / lower its cost (largest move):

- old: (a) low: 5 up (≤1.7), 2 down (≤3.1); (a) high: 4 up (≤1.3), 3 down (≤3.3); (b) low: 4 up (≤1.4), 3 down (≤3.0); (b) high: 3 up (≤1.2), 4 down (≤2.9)
- new: (a) low: 5 up (≤1.7), 3 down (≤3.3); (a) high: 4 up (≤1.3), 4 down (≤3.4); (b) low: 4 up (≤1.4), 4 down (≤3.1); (b) high: 3 up (≤1.2), 5 down (≤3.1)

### Lane contributions by generation, $bn low / high (`lanes`)

| Lane | (a) G1 | (a) G2 | (a) G3+ | (b) G1 | (b) G2 | (b) G3+ |
|---|---|---|---|---|---|---|
| stack | +15.10 / +18.14 → +14.52 / +17.68 | +2.60 / -0.15 → +2.65 / -0.11 | +2.20 / +3.22 → +2.24 / +3.26 | +16.10 / +18.17 → +15.55 / +17.73 | +1.28 / -0.16 → +1.31 / -0.13 | +2.53 / +3.20 → +2.55 / +3.22 |
| cbo | +1.13 / +0.98 (same) | +5.15 / +3.88 (same) | +3.04 / +3.54 (same) | +1.57 / +0.75 (same) | +3.88 / +4.04 (same) | +3.87 / +3.61 (same) |
| ota | -0.09 / -0.12 (same) | -0.16 / -0.14 (same) | -0.12 / -0.08 (same) | -0.11 / -0.12 (same) | -0.15 / -0.14 (same) | -0.10 / -0.08 (same) |
| row1 | -3.97 / -11.39 (same) | -6.54 / -2.23 (same) | -3.72 / -0.62 (same) | -8.87 / -10.35 (same) | -3.53 / -2.91 (same) | -1.83 / -0.97 (same) |
| medical | -5.48 / -5.45 (same) | -5.26 / -5.27 (same) | -6.05 / -6.06 (same) | -6.29 / -6.27 (same) | -5.07 / -5.07 (same) | -5.44 / -5.44 (same) |
| education | +0.96 / +3.59 → +1.31 / +4.80 | -0.60 / -2.61 → -1.07 / -2.79 | +0.34 / -1.51 → +0.34 / -1.40 | -0.45 / -1.29 → -0.87 / -1.11 | +0.30 / +0.40 → +0.31 / +0.89 | +0.86 / +0.35 → +1.14 / +0.83 |
| benefits | +0.46 / +0.68 (same) | +0.90 / +0.77 (same) | +0.79 / +0.57 (same) | +0.73 / +0.73 (same) | +0.87 / +0.77 (same) | +0.55 / +0.51 (same) |
| justice | +0.53 / +0.53 (same) | +0.81 / +0.81 (same) | +0.69 / +0.69 (same) | +0.53 / +0.53 (same) | +0.81 / +0.81 (same) | +0.69 / +0.69 (same) |
| constants | -2.61 / -2.62 (same) | -1.10 / -1.12 (same) | -1.35 / -1.36 (same) | -2.80 / -2.82 (same) | -1.08 / -1.10 (same) | -1.18 / -1.19 (same) |
| row8_finite | new -0.03 / -0.03 | new -0.04 / -0.04 | new -0.04 / -0.04 | new -0.04 / -0.04 | new -0.03 / -0.03 | new -0.03 / -0.03 |
| consumption_key | new -0.93 / -0.93 | new -1.23 / -1.23 | new -1.89 / -1.89 | new -1.36 / -1.36 | new -0.77 / -0.77 | new -1.92 / -1.92 |
| Total correction | +6.04 / +4.33 → +4.84 / +4.12 | -4.20 / -6.05 → -5.88 / -7.47 | -4.17 / -1.60 → -6.05 / -3.38 | +0.40 / -0.66 → -1.97 / -2.32 | -2.69 / -3.35 → -3.45 / -3.64 | -0.04 / +0.69 → -1.68 / -0.76 |

Union contribution of each lane (sum of the generations under (a)), $bn low / high:

- stack: +19.91 / +21.21 → +19.41 / +20.82
- cbo: +9.32 / +8.40 → +9.32 / +8.40
- ota: -0.36 / -0.34 → -0.36 / -0.34
- row1: -14.23 / -14.23 → -14.23 / -14.23
- medical: -16.80 / -16.78 → -16.80 / -16.78
- education: +0.71 / -0.53 → +0.58 / +0.61
- benefits: +2.15 / +2.02 → +2.15 / +2.02
- justice: +2.03 / +2.03 → +2.03 / +2.03
- constants: -5.06 / -5.10 → -5.06 / -5.10
- row8_finite: new -0.10 / -0.10
- consumption_key: new -4.05 / -4.05

### Ledger comparison, account rows, $ per person a year (ledger_comparison.csv)

| Row | G1 shared | G2 shared | G3+ shared | G1 personal | G2 personal | G3+ personal |
|---|---|---|---|---|---|---|
| Direct lines at average cost | -7,635 → -7,647 | -8,882 → -8,894 | -7,015 → -7,027 | -5,751 → -5,763 | -9,804 → -9,816 | -9,689 → -9,701 |
| The same lines at the adopted responses | -5,448 → -6,680 | -6,165 → -7,906 | -4,294 → -5,854 | -4,505 → -4,796 | -7,171 → -8,828 | -7,014 → -8,529 |
| Plus the production term (Sept 23 case → uncorrected at the case's responses) | -4,726 → -5,958 | -5,996 → -7,736 | -4,149 → -5,710 | -4,028 → -4,320 | -7,059 → -8,716 | -6,919 → -8,434 |
| Plus the corrections (adopted main case) | -5,220 → -6,354 | -5,703 → -7,326 | -3,859 → -5,288 | -4,383 → -4,657 | -6,636 → -8,195 | -6,808 → -8,198 |

Ledger rows (published gap, eight-band gaps, own balance) do not change: they are the September 19 ledger's.

### Numbers quoted in the lane RESULT's prose

- Minors moved to their parents' generation shift onto G1: $46.4–81.2bn → $57.9–98.5bn.
- Household allocation rule, (a), G1 and G3+ at the two ends: $19.1–32.0bn → $28.4–36.3bn.
- (b) second-generation adult as a share of a Mexico-born adult (per adult): 51–60% → 56–66%.
- old: corrections at the low end, $ per person (G1, G2, G3+): -494, +293, +291; production term 722, 169, 144; marginal responses take off 2,187, 2,717, 2,721, 1,246, 2,633, 2,675 (shared G1–G3+, personal G1–G3+); direct lines at the responses differ from the ledger's own balance by 71–481 (shared); account G2 below G1 by 483 (shared); G3+ below G2 by 171 (personal).
- new: corrections at the low end, $ per person (G1, G2, G3+): -396, +411, +422; production term 722, 169, 144; marginal responses take off 967, 988, 1,172, 967, 988, 1,172 (shared G1–G3+, personal G1–G3+); direct lines at the responses differ from the ledger's own balance by 751–2,025 (shared); account G2 below G1 by 972 (shared); G3+ below G2 by 3 (personal).

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

## For the parent and round two

- **Not run by me:** the last step of `run_all.sh`, `main_case_schools_full_2026_09_26/main_case.cjs`,
  writes into that lane. Run it at commit time; it should leave that lane byte-identical.
- **Winners-and-losers ledger.** `winners_losers.py` reads `generation_results.csv` from the working
  tree, not a pinned commit, and gates that the generations add to its own September 24 band (1e-3).
  Until W4 moves it, a rerun fails that gate loudly: the sums are now 258.489 / 291.955 against
  200.875 / 246.318. For its September 24 run, pin the file at ba12f3c or use
  `run_generations.cjs --case sept24 --out-dir DIR`. It reads only `cost_bn` and `population`, whose
  names do not change.
- **Documents quoting the September 24 split** (outside my boundary): the research memo
  `research/immigration-adopted-account-by-generation-2026-09-25.md`, ladder 224, the INDEX (line 65)
  and the FAQ. The tables here hold every replacement number.
- **To commit** (explicit paths; `git add` the two new files first):
  - `consumption_split.py`, `derived/consumption_key_by_generation.json`;
  - `run_generations.cjs`, `compare_ledger.py`, `run_all.sh`, `RESULT.md`;
  - the four changed `derived/` files;
  - this file.

## Limits

- **Bridge order.** The split of the move between the school response and the band end depends on
  the order (see above). Their sum and the generations' shares of the school line do not.
- **Remainders.** The own-factor scaling leaves $0.31bn of the consumption key and $0.43bn of the
  ratio-type lanes to spread by cells. The union-factor alternative is reported.
- **Saving ratio.** It varies by income rank only, because CE records no parents' birthplace. The
  corridor's per-capita spread inside a unit is the consumption lane's, so a Mexico-born parent's
  remittances lower their US-born children's key.
- **Inherited from the main case.** The shelter constant stays keyed to 0.59/0.84, about −$0.002bn
  against the adopted general-government responses. School dilution does not apply at a response of
  1 (decision `2026-09-26-main-case-schools-full-cost`).
- **Instrument.** An LLM assembled this (`notes/llm-bias-caveat.md`). The split rules for the new edits
  were fixed before the results were seen, and repointing to the schools case changed no rule.

## Parent integration (2026-09-26, 23:33)

- **Case renamed.** The worker's `schools_full` is now `sept26_schools`, the name the other lanes
  use. The rename touched `run_generations.cjs` and this file; the only output change is the
  `case` field in `generation_summary.json`.
- **Parent rerun.**
  - `consumption_split.py`, then the default `run_generations.cjs` and `compare_ledger.py`: 0 FAIL
    lines. Two runs are byte-identical in all 20 `derived/` files.
  - `--case sept24`: all four case-dependent files equal HEAD.
  - `--case sept26`: every gate passes.
  - `main_case_schools_full_2026_09_26/main_case.cjs`: all gates pass, and the three main-case
    lanes stay clean.
- **Bridge.** The union's parts match the parent's own calculation from the package: school response
  at the Sept 26 ends +58.36 / +45.44, range ends −0.79 / +0.81.
