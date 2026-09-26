claude-opus-5-5

**Verdict:** Done, not committed. On top of 2441ac8 the generation account's bridge is now the
parent's ordered chain at matched specifications. The four September 26 parts are followed by
`school_full_cost` and `band_end_specs`, whose union sum equals the schools lane's own change from
September 26 (+$57.57bn / +$46.26bn). The three generations add to **$258.4885–291.9548bn** in all 64
specifications under both conventions, and the uncorrected union reproduces $265.5903–298.6797bn; both
bands are read from the schools lane's `main_case_bands.csv`. Against the one-year scenario, schools at
full cost add $58.4bn at the union's low end and $45.4bn at its high end. Under (a) the second and
third-plus generations carry 76–91% of that; under (b) the Mexico-born carry 43–44%. `--case sept26`
reproduces the four September 26 outputs byte for byte, and `--case sept24` those of ba12f3c. Every
gate passes, two default runs are byte-identical, and against HEAD only `generation_summary.json`
changes.

Model self-report: claude-opus-5-5. Worker W2 (`generation`), 2026-09-26.

## The bridge: September 24 → September 26 → schools case

Net cost to other US residents, $bn a year, at the union's low / high range end (shared / personal
allocation). Every generation is evaluated at the union's end specifications, not at its own minimum
and maximum. The chain runs at matched specifications, and its parts add exactly (within 5.7e-14bn)
for every generation and the union (`generation_summary.json` → `change_from_sept24`, six parts, and
`change_from_sept26`, the last two):

1. general government, 0.59/0.84 → 0.6000/0.8504;
2. schools, finite removal, 0.63/0.66 → 0.6522/0.6813;
3. row 8 at 0.949;
4. the consumption key. Parts 1–4 reach the September 26 case at specifications 56 and 7, which are
   both the September 24 and the September 26 ends (gate).
5. `school_full_cost`: schools 0.6522/0.6813 → 1 at specifications 56 and 7.
6. `band_end_specs`: the schools case at its own ends, 48 and 11, less the same case at 56 and 7. The
   ends move because at a response of 1 the school-share bound flips (0.865 → 0.715 low, 0.715 → 0.865
   high).

| $bn, low / high | Sept 24 | General government | Schools, finite removal | Row 8 at 0.949 | Consumption key | **Sept 26** | Schools at full cost | Band end moves | **Schools case** | Move |
|---|---|---|---|---|---|---|---|---|---|---|
| (a) G1 | 63.79 / 53.56 | +0.13 / +0.14 | +0.89 / +0.26 | −0.03 / −0.03 | −0.93 / −0.93 | **63.85 / 52.99** | +13.98 / +3.88 | −0.18 / +0.04 | **77.65 / 56.91** | +13.85 / +3.35 |
| (a) G2 | 81.74 / 95.12 | +0.17 / +0.18 | +1.48 / +1.44 | −0.04 / −0.04 | −1.23 / −1.23 | **82.12 / 95.47** | +23.20 / +21.58 | −0.32 / +0.41 | **105.00 / 117.46** | +23.26 / +22.34 |
| (a) G3+ | 55.34 / 97.64 | +0.17 / +0.18 | +1.35 / +1.34 | −0.04 / −0.04 | −1.89 / −1.89 | **54.95 / 97.23** | +21.18 / +19.98 | −0.29 / +0.37 | **75.84 / 117.58** | +20.50 / +19.95 |
| (b) G1 | 110.22 / 134.76 | +0.19 / +0.19 | +1.61 / +1.35 | −0.04 / −0.04 | −1.36 / −1.36 | **110.62 / 134.90** | +25.29 / +20.11 | −0.35 / +0.37 | **135.56 / 155.38** | +25.34 / +20.62 |
| (b) G2 | 50.18 / 52.96 | +0.15 / +0.15 | +1.12 / +0.85 | −0.03 / −0.03 | −0.77 / −0.77 | **50.64 / 53.16** | +17.50 / +12.68 | −0.24 / +0.22 | **67.90 / 66.06** | +17.72 / +13.10 |
| (b) G3+ | 40.47 / 58.60 | +0.14 / +0.15 | +0.99 / +0.85 | −0.03 / −0.03 | −1.92 / −1.92 | **39.66 / 57.64** | +15.57 / +12.65 | −0.20 / +0.22 | **55.02 / 70.52** | +14.55 / +11.92 |
| Union | 200.88 / 246.32 | +0.47 / +0.49 | +3.72 / +3.04 | −0.10 / −0.10 | −4.05 / −4.05 | **200.92 / 245.69** | +58.36 / +45.44 | −0.79 / +0.81 | **258.49 / 291.95** | +57.61 / +45.64 |

The union's parts 5 and 6 add to +$57.5705bn / +$46.2599bn, the schools lane's `summary.json` →
`change` (gate, 1.1e-13bn).

**The school line's own split.** The first column is part 5. "School line in the case" is what the case
charges each generation for schools at the union's range end: its cost at a school response of 1 less
its cost at 0 (`school_line_bn`). A generation's share is the same in both columns, since both scale
the same school costs under the same allocation.

| $bn, low / high | Schools at full cost | Its share of the union's | School line in the case | Its share |
|---|---|---|---|---|
| (a) G1 | +13.98 / +3.88 | 24% / 9% | 33.22 / 14.74 | 24% / 9% |
| (a) G2 | +23.20 / +21.58 | 40% / 47% | 55.15 / 81.90 | 40% / 47% |
| (a) G3+ | +21.18 / +19.98 | 36% / 44% | 50.36 / 75.84 | 36% / 44% |
| (b) G1 | +25.29 / +20.11 | 43% / 44% | 60.13 / 76.34 | 43% / 44% |
| (b) G2 | +17.50 / +12.68 | 30% / 28% | 41.60 / 48.11 | 30% / 28% |
| (b) G3+ | +15.57 / +12.65 | 27% / 28% | 37.00 / 48.02 | 27% / 28% |
| Union | +58.36 / +45.44 | 100% / 100% | 138.73 / 172.47 | 100% / 100% |

- Under (a), children count in their own generation, so the line falls mostly on the second and
  third-plus generations. At the shared low end parents carry part of their children's costs through
  the SPM unit's equal split: the Mexico-born take 24% there and 9% at the personal high end.
- Under (b), minors count with their parents, and the Mexico-born take 43–44%.

**Tied band ends.** At a school response of 1 the growth and decline specifications coincide: all 32
pairs are identical, and their costs are equal (`===`) for the union and every generation. The low end
is attained at specifications 48 and 52 and the high end at 11 and 15. `indexOf` (argmin/argmax) takes
the first of each, 48 and 11, which carry the growth index (0.63 on September 24, 0.6522 on
September 26). The tie is exact, so the choice moves no number (gate; `generation_summary.json` →
`band_end_ties`).

## Headline, schools case

| $bn a year at the union's low / high end | G1 | G2 | G3+ | All three |
|---|---|---|---|---|
| (a) own generation | 77.65 / 56.91 | 105.00 / 117.46 | 75.84 / 117.58 | 258.49 / 291.95 |
| (a) $ per member | 6,354 / 4,657 | 7,326 / 8,195 | 5,288 / 8,198 | 6,321 / 7,139 |
| (b) minors with parents | 135.56 / 155.38 | 67.90 / 66.06 | 55.02 / 70.52 | 258.49 / 291.95 |
| (b) $ per adult | 11,612 / 13,309 | 7,617 / 7,410 | 6,723 / 8,617 | 8,984 / 10,147 |

Every generation's lowest cost over the 64 specifications is positive: (a) $49.3bn, $105.0bn and
$75.8bn; (b) $135.6bn, $60.9bn and $55.0bn. Under the eight alternative split rules no generation moves
by more than $3.7bn.

## How the edits split, and why

- **Responses** (general government 0.6000/0.8504, schools 1/1) are engine state, so each generation's
  model responds on its own lines. They come from the package's `MAIN_SPECS`, gated against
  `corrections.json` → `meta.responses`. No 0.63/0.66 remains in a computation. The lane's only literal
  responses are `correction_rules.py`'s `SHELTER_GG` 0.59/0.84, which mirror the September 24 package's
  shelter keying (`main_case_2026_09_24/package.cjs:323`). That keying is inherited and is not a
  service response.
- **Row 8** (−$0.10bn on the constants line) splits as the lane splits audit row 8, by population
  (`correction_rules.json` → `constants.row8`). This is the brief's rule.
- **The consumption key** (spec `both_corridor_net_h2`, −$4.05bn) is split exactly, with the same numbers
  as on September 26. The consumption lane's frame is this lane's, person for person.
  `consumption_split.py` rebuilds the lane's 40 union edits from generation totals with a maximum
  difference of 0.0. Each generation's saving part then takes its own stack factor (0.85, 0.98 and 0.99
  under (a)), and the corridor's dollars are not scaled. The alternatives, the union's factor and the
  old key's shares, run as sensitivities. They move no generation by more than $0.51bn against the
  central split.

## The case switch

`run_generations.cjs` has one table of cases. The parent renamed the default key to `sept26_schools`
before 2441ac8:

```js
const CASES = { sept26_schools: "main_case_schools_full_2026_09_26", sept26: "main_case_2026_09_26", sept24: "main_case_2026_09_24" };
const CASE = arg("--case", "sept26_schools");
```

The package, `corrections.json`, `summary.json` and `main_case_bands.csv` all come from `CASES[CASE]`.
`--out-dir DIR` writes elsewhere, and `compare_ledger.py` takes the same flag. Under `sept26` the
summary keeps that run's `change_from_sept24` format field for field.

## Gates

| Gate | Result |
|---|---|
| Regression, `--case sept24 --out-dir DIR` against ba12f3c, the September 24 record (HEAD now holds the schools case) | **Pass.** `generation_results.csv`, `generation_summary.json`, `generation_corrections.json` and `ledger_comparison.csv` are identical. |
| Regression, `--case sept26 --out-dir DIR` against the four September 26 derived files, copied to the scratchpad at 23:11 before the switch | **Pass.** All four are identical, the summary included. |
| `corrections.json` is the schools package's payload, and its edits are the September 26 payload's | **Pass**, deep-equal |
| Specifications carry `meta.responses` | **Pass**: general government 0.6000/0.8504, schools 1/1 |
| Corrected union against `main_case_bands.csv` `adopted` (main profile), 1e-4 | **Pass**: 258.4885–291.9548 |
| Uncorrected union against `main_case_bands.csv` `uncorrected_at_adopted_responses`, 1e-4 | **Pass**: 265.5903–298.6797 |
| `summary.json`'s full-precision bands round to those rows | **Pass** |
| Lanes rebuild the package's `packageShifts` (row 8 included), both fill-in methods | **Pass** |
| Consumption split: frames, key shares, union edits against `payloads.json` | **Pass**: 40 cells, maximum difference 0.0bn |
| Every split adds to its union shift or cell | **Pass**: 2.1e-12bn |
| Netted generation edits add to `corrections.json`, 270 cells | **Pass**: 1.4e-12bn (a), 1.3e-12bn (b) |
| The three generations add to the union, 64 specifications, both conventions | **Pass**: corrected 1.4e-12bn, uncorrected 1.1e-13bn |
| September 24 cross-check | **Pass**: $200.8752–246.3184bn. The nine lanes' generation payloads add to its `corrections.json` (1.4e-12bn), and their costs add in all 64 specifications (1.5e-12bn). |
| The September 26 case has the September 24 ends and reproduces its band | **Pass**: specifications 56 and 7, $200.9180–245.6949bn |
| The chain's parts add to each move and end at the case's own cost, every generation and the union | **Pass**: 5.7e-14bn |
| The generations' parts add to the union's, part by part, both conventions | **Pass**: 1.6e-12bn |
| The union's parts 5 + 6 equal the schools lane's `change` | **Pass**: +57.5705 / +46.2599, 1.1e-13bn |
| The band ends tie exactly at a school response of 1 | **Pass**: 48 and 52, 11 and 15 (`===`); `indexOf` takes 48 and 11 |
| Determinism: the default pipeline twice | **Pass**: all 20 derived files byte-identical, 192 gate lines per run, none failed |
| Against HEAD | Only `generation_summary.json` changes. `change_from_sept24` is restructured, and `change_from_sept26` and `band_end_ties` are added. The CSV, the payload and the ledger comparison are identical. |
| Other lanes untouched | **Pass**: no new or modified files in the package lanes or the consumption lane |

## Files changed since 2441ac8

All in `../generation_account_2026_09_24/`, none committed:
- `run_generations.cjs`:
  - the bands come from `main_case_bands.csv`;
  - the chain writes `change_from_sept24` (six parts) and `change_from_sept26`, while `sept26` keeps
    its own format;
  - the tie gate and `band_end_ties`;
  - the header.
- `run_all.sh`: the September 26 main case's check before the schools case's.
- `RESULT.md`: the schools section on top, with range-end labels, the chain, the school line and the
  ties. Then "September 26 case (the one-year scenario since 22:39)", then the September 24 record.
- `derived/generation_summary.json`: the chain's fields.
- This file.

## Old → new, September 26 → schools case, every published number

Old is the September 26 case: the four files as `derived/` held them before the switch, which
`--case sept26` reproduces. New is `derived/`. The move's decomposition is the bridge above. The tables
are generated from the two runs' outputs.

### Headline, $bn a year and $ per head (generation_summary.json `conventions`, generation_results.csv)

| Convention, generation | $bn at the union's low end (shared) | $bn at the union's high end (personal) | Own range over the 64 specifications, $bn | $ per member, low / high | $ per adult, low / high |
|---|---|---|---|---|---|
| (a) G1 | 63.85 → **77.65** | 52.99 → **56.91** | 44.2–74.6 → 49.3–85.4 | 5,225 / 4,336 → 6,354 / 4,657 | 5,469 / 4,539 → 6,651 / 4,875 |
| (a) G2 | 82.12 → **105.00** | 95.47 → **117.46** | 82.1–95.5 → 105.0–117.5 | 5,729 / 6,661 → 7,326 / 8,195 | 9,212 / 10,710 → 11,778 / 13,176 |
| (a) G3+ | 54.95 → **75.84** | 97.23 → **117.58** | 54.9–97.2 → 75.8–117.6 | 3,831 / 6,779 → 5,288 / 8,198 | 6,714 / 11,881 → 9,268 / 14,369 |
| (b) G1 | 110.62 → **135.56** | 134.90 → **155.38** | 110.6–134.9 → 135.6–155.4 | 6,563 / 8,003 → 8,043 / 9,218 | 9,475 / 11,555 → 11,612 / 13,309 |
| (b) G2 | 50.64 → **67.90** | 53.16 → **66.06** | 44.4–59.6 → 60.9–73.0 | 4,148 / 4,354 → 5,562 / 5,411 | 5,681 / 5,963 → 7,617 / 7,410 |
| (b) G3+ | 39.66 → **55.02** | 57.64 → **70.52** | 39.7–57.6 → 55.0–70.5 | 3,352 / 4,872 → 4,650 / 5,960 | 4,846 / 7,044 → 6,723 / 8,617 |
| Union (main case) | 200.9180 → **258.4885** | 245.6949 → **291.9548** | | | |

### The corrections against the uncorrected model at the same specification, $bn (`correction_bn`)

Old: against the uncorrected model at the case's responses (general government 0.6000/0.8504, schools 0.6522/0.6813). New: against the uncorrected model at the case's responses (general government 0.6000/0.8504, schools 1/1).

| Generation | (a) low | (a) high | (b) low | (b) high |
|---|---|---|---|---|
| G1 | +5.06 → +4.84 | +3.40 → +4.12 | -1.05 → -1.97 | -2.11 → -2.32 |
| G2 | -5.47 → -5.88 | -7.36 → -7.47 | -3.48 → -3.45 | -4.14 → -3.64 |
| G3+ | -6.07 → -6.05 | -3.53 → -3.38 | -1.96 → -1.68 | -1.24 → -0.76 |

| Uncorrected model at the band ends, $bn | (a) low | (a) high | (b) low | (b) high |
|---|---|---|---|---|
| G1 | 58.80 → 72.81 | 49.59 → 52.79 | 111.67 → 137.53 | 137.01 → 157.70 |
| G2 | 87.59 → 110.88 | 102.83 → 124.93 | 54.12 → 71.36 | 57.29 → 69.70 |
| G3+ | 61.02 → 81.90 | 100.76 → 120.96 | 41.62 → 56.70 | 58.88 → 71.28 |

### Allocation swap, $bn (`allocation_swap`)

| | Low end (shared) | Low end, personal instead | High end (personal) | High end, shared instead |
|---|---|---|---|---|
| (a) G1 | 63.9 → 77.6 | 44.2 → 49.3 | 53.0 → 56.9 | 74.6 → 85.4 |
| (a) G2 | 82.1 → 105.0 | 83.3 → 111.4 | 95.5 → 117.5 | 93.1 → 111.0 |
| (a) G3+ | 54.9 → 75.8 | 86.1 → 112.1 | 97.2 → 117.6 | 64.9 → 81.3 |
| (b) G1 | 110.6 → 135.6 | 119.7 → 145.9 | 134.9 → 155.4 | 125.6 → 145.1 |
| (b) G2 | 50.6 → 67.9 | 44.4 → 60.9 | 53.2 → 66.1 | 59.6 → 73.0 |
| (b) G3+ | 39.7 → 55.0 | 49.5 → 65.9 | 57.6 → 70.5 | 47.6 → 59.6 |

### Sensitivities of the flagged and literal rules, $bn: central (lowest–highest alternative) (`sensitivities`)

Old: 8 alternatives. New: 8.

| | (a) low | (a) high | (b) low | (b) high |
|---|---|---|---|---|
| G1 | 63.9 (60.6–65.5) → 77.6 (74.4–79.3) | 53.0 (49.6–54.3) → 56.9 (53.5–58.2) | 110.6 (107.5–112.0) → 135.6 (132.4–137.0) | 134.9 (131.8–136.1) → 155.4 (152.3–156.6) |
| G2 | 82.1 (80.6–84.1) → 105.0 (103.5–107.0) | 95.5 (94.8–99.2) → 117.5 (116.7–121.2) | 50.6 (49.3–53.9) → 67.9 (66.5–71.1) | 53.2 (52.4–56.7) → 66.1 (65.3–69.6) |
| G3+ | 54.9 (54.1–56.2) → 75.8 (75.0–77.1) | 97.2 (96.7–97.7) → 117.6 (117.0–118.1) | 39.7 (39.1–40.2) → 55.0 (54.5–55.5) | 57.6 (57.1–58.2) → 70.5 (70.0–71.0) |

Largest move of any generation under any alternative: 3.71 → 3.71 $bn.

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

- old: (a) low: 5 up (≤1.7), 3 down (≤3.3); (a) high: 4 up (≤1.3), 4 down (≤3.4); (b) low: 4 up (≤1.4), 4 down (≤3.1); (b) high: 3 up (≤1.2), 5 down (≤3.1)
- new: (a) low: 5 up (≤1.7), 3 down (≤3.3); (a) high: 4 up (≤1.3), 4 down (≤3.4); (b) low: 4 up (≤1.4), 4 down (≤3.1); (b) high: 3 up (≤1.2), 5 down (≤3.1)

### Lane contributions by generation, $bn low / high (`lanes`)

| Lane | (a) G1 | (a) G2 | (a) G3+ | (b) G1 | (b) G2 | (b) G3+ |
|---|---|---|---|---|---|---|
| stack | +15.05 / +18.09 → +14.52 / +17.68 | +2.60 / -0.15 → +2.65 / -0.11 | +2.21 / +3.23 → +2.24 / +3.26 | +16.06 / +18.13 → +15.55 / +17.73 | +1.28 / -0.16 → +1.31 / -0.13 | +2.53 / +3.20 → +2.55 / +3.22 |
| cbo | +1.13 / +0.98 (same) | +5.15 / +3.88 (same) | +3.04 / +3.54 (same) | +1.57 / +0.75 (same) | +3.88 / +4.04 (same) | +3.87 / +3.61 (same) |
| ota | -0.09 / -0.12 (same) | -0.16 / -0.14 (same) | -0.12 / -0.08 (same) | -0.11 / -0.12 (same) | -0.15 / -0.14 (same) | -0.10 / -0.08 (same) |
| row1 | -3.97 / -11.39 (same) | -6.54 / -2.23 (same) | -3.72 / -0.62 (same) | -8.87 / -10.35 (same) | -3.53 / -2.91 (same) | -1.83 / -0.97 (same) |
| medical | -5.48 / -5.45 (same) | -5.26 / -5.27 (same) | -6.05 / -6.06 (same) | -6.29 / -6.27 (same) | -5.07 / -5.07 (same) | -5.44 / -5.44 (same) |
| education | +0.99 / +3.66 → +1.31 / +4.80 | -0.61 / -2.64 → -1.07 / -2.79 | +0.36 / -1.53 → +0.34 / -1.40 | -0.46 / -1.30 → -0.87 / -1.11 | +0.32 / +0.42 → +0.31 / +0.89 | +0.89 / +0.37 → +1.14 / +0.83 |
| benefits | +0.46 / +0.68 (same) | +0.90 / +0.77 (same) | +0.79 / +0.57 (same) | +0.73 / +0.73 (same) | +0.87 / +0.77 (same) | +0.55 / +0.51 (same) |
| justice | +0.53 / +0.53 (same) | +0.81 / +0.81 (same) | +0.69 / +0.69 (same) | +0.53 / +0.53 (same) | +0.81 / +0.81 (same) | +0.69 / +0.69 (same) |
| constants | -2.61 / -2.62 (same) | -1.10 / -1.12 (same) | -1.35 / -1.36 (same) | -2.80 / -2.82 (same) | -1.08 / -1.10 (same) | -1.18 / -1.19 (same) |
| row8_finite | -0.03 / -0.03 (same) | -0.04 / -0.04 (same) | -0.04 / -0.04 (same) | -0.04 / -0.04 (same) | -0.03 / -0.03 (same) | -0.03 / -0.03 (same) |
| consumption_key | -0.93 / -0.93 (same) | -1.23 / -1.23 (same) | -1.89 / -1.89 (same) | -1.36 / -1.36 (same) | -0.77 / -0.77 (same) | -1.92 / -1.92 (same) |
| Total correction | +5.06 / +3.40 → +4.84 / +4.12 | -5.47 / -7.36 → -5.88 / -7.47 | -6.07 / -3.53 → -6.05 / -3.38 | -1.05 / -2.11 → -1.97 / -2.32 | -3.48 / -4.14 → -3.45 / -3.64 | -1.96 / -1.24 → -1.68 / -0.76 |

Union contribution of each lane (sum of the generations under (a)), $bn low / high:

- stack: +19.86 / +21.17 → +19.41 / +20.82
- cbo: +9.32 / +8.40 → +9.32 / +8.40
- ota: -0.36 / -0.34 → -0.36 / -0.34
- row1: -14.23 / -14.23 → -14.23 / -14.23
- medical: -16.80 / -16.78 → -16.80 / -16.78
- education: +0.75 / -0.51 → +0.58 / +0.61
- benefits: +2.15 / +2.02 → +2.15 / +2.02
- justice: +2.03 / +2.03 → +2.03 / +2.03
- constants: -5.06 / -5.10 → -5.06 / -5.10
- row8_finite: -0.10 / -0.10 → -0.10 / -0.10
- consumption_key: -4.05 / -4.05 → -4.05 / -4.05

### Ledger comparison, account rows, $ per person a year (ledger_comparison.csv)

| Row | G1 shared | G2 shared | G3+ shared | G1 personal | G2 personal | G3+ personal |
|---|---|---|---|---|---|---|
| Direct lines at average cost | -7,647 → -7,647 | -8,894 → -8,894 | -7,027 → -7,027 | -5,763 → -5,763 | -9,816 → -9,816 | -9,701 → -9,701 |
| The same lines at the adopted responses | -5,533 → -6,680 | -6,281 → -7,906 | -4,398 → -5,854 | -4,534 → -4,796 | -7,286 → -8,828 | -7,121 → -8,529 |
| Plus the production term (the uncorrected model at the same specification) | -4,811 → -5,958 | -6,111 → -7,736 | -4,254 → -5,710 | -4,058 → -4,320 | -7,174 → -8,716 | -7,026 → -8,434 |
| Plus the corrections (adopted main case) | -5,225 → -6,354 | -5,729 → -7,326 | -3,831 → -5,288 | -4,336 → -4,657 | -6,661 → -8,195 | -6,779 → -8,198 |

Ledger rows (published gap, eight-band gaps, own balance) do not change: they are the September 19 ledger's.

### Numbers quoted in the lane RESULT's prose

- Minors moved to their parents' generation shift onto G1: $46.8–81.9bn → $57.9–98.5bn.
- Household allocation rule, (a), G1 and G3+ at the two ends: $19.6–32.3bn → $28.4–36.3bn.
- (b) second-generation adult as a share of a Mexico-born adult (per adult): 52–60% → 56–66%.
- old: corrections at the low end, $ per person (G1, G2, G3+): -414, +382, +423; production term 722, 169, 144; marginal responses take off 2,113, 2,613, 2,628, 1,228, 2,530, 2,581 (shared G1–G3+, personal G1–G3+); direct lines at the responses differ from the ledger's own balance by 175–400 (shared); account G2 below G1 by 505 (shared); G3+ below G2 by 118 (personal).
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

## Old → new, September 24 → September 26 (the earlier record)

Old is ba12f3c (`--case sept24`), and new is the September 26 case, as reported earlier today.

### Headline, $bn a year and $ per head (generation_summary.json `conventions`, generation_results.csv)

| Convention, generation | $bn at the union's low end (shared) | $bn at the union's high end (personal) | Own range over the 64 specifications, $bn | $ per member, low / high | $ per adult, low / high |
|---|---|---|---|---|---|
| (a) G1 | 63.79 → **63.85** | 53.56 → **52.99** | 44.7–74.8 → 44.2–74.6 | 5,220 / 4,383 → 5,225 / 4,336 | 5,464 / 4,588 → 5,469 / 4,539 |
| (a) G2 | 81.74 → **82.12** | 95.12 → **95.47** | 81.7–95.1 → 82.1–95.5 | 5,703 / 6,636 → 5,729 / 6,661 | 9,169 / 10,670 → 9,212 / 10,710 |
| (a) G3+ | 55.34 → **54.95** | 97.64 → **97.23** | 55.3–97.6 → 54.9–97.2 | 3,859 / 6,808 → 3,831 / 6,779 | 6,763 / 11,931 → 6,714 / 11,881 |
| (b) G1 | 110.22 → **110.62** | 134.76 → **134.90** | 110.2–134.8 → 110.6–134.9 | 6,539 / 7,995 → 6,563 / 8,003 | 9,441 / 11,543 → 9,475 / 11,555 |
| (b) G2 | 50.18 → **50.64** | 52.96 → **53.16** | 44.0–59.3 → 44.4–59.6 | 4,110 / 4,338 → 4,148 / 4,354 | 5,629 / 5,941 → 5,681 / 5,963 |
| (b) G3+ | 40.47 → **39.66** | 58.60 → **57.64** | 40.5–58.6 → 39.7–57.6 | 3,420 / 4,952 → 3,352 / 4,872 | 4,945 / 7,160 → 4,846 / 7,044 |
| Union (main case) | 200.8752 → **200.9180** | 246.3184 → **245.6949** | | | |

### The corrections against the uncorrected model at the same specification, $bn (`correction_bn`)

Old: against the September 23 case (the uncorrected model at 0.59/0.84 and 0.63/0.66). New: against the uncorrected model at the case's responses (general government 0.6000/0.8504, schools 0.6522/0.6813).

| Generation | (a) low | (a) high | (b) low | (b) high |
|---|---|---|---|---|
| G1 | +6.04 → +5.06 | +4.33 → +3.40 | +0.40 → -1.05 | -0.66 → -2.11 |
| G2 | -4.20 → -5.47 | -6.05 → -7.36 | -2.69 → -3.48 | -3.35 → -4.14 |
| G3+ | -4.17 → -6.07 | -1.60 → -3.53 | -0.04 → -1.96 | +0.69 → -1.24 |

| Uncorrected model at the band ends, $bn | (a) low | (a) high | (b) low | (b) high |
|---|---|---|---|---|
| G1 | 57.76 → 58.80 | 49.23 → 49.59 | 109.82 → 111.67 | 135.42 → 137.01 |
| G2 | 85.94 → 87.59 | 101.18 → 102.83 | 52.87 → 54.12 | 56.31 → 57.29 |
| G3+ | 59.51 → 61.02 | 99.24 → 100.76 | 40.51 → 41.62 | 57.90 → 58.88 |

### Allocation swap, $bn (`allocation_swap`)

| | Low end (shared) | Low end, personal instead | High end (personal) | High end, shared instead |
|---|---|---|---|---|
| (a) G1 | 63.8 → 63.9 | 44.7 → 44.2 | 53.6 → 53.0 | 74.8 → 74.6 |
| (a) G2 | 81.7 → 82.1 | 82.6 → 83.3 | 95.1 → 95.5 | 93.0 → 93.1 |
| (a) G3+ | 55.3 → 54.9 | 86.1 → 86.1 | 97.6 → 97.2 | 65.6 → 64.9 |
| (b) G1 | 110.2 → 110.6 | 119.2 → 119.7 | 134.8 → 134.9 | 125.5 → 125.6 |
| (b) G2 | 50.2 → 50.6 | 44.0 → 44.4 | 53.0 → 53.2 | 59.3 → 59.6 |
| (b) G3+ | 40.5 → 39.7 | 50.2 → 49.5 | 58.6 → 57.6 | 48.6 → 47.6 |

### Sensitivities of the flagged and literal rules, $bn: central (lowest–highest alternative) (`sensitivities`)

Old: 7 alternatives. New: 8 (consumption_key_by_old_key_shares added).

| | (a) low | (a) high | (b) low | (b) high |
|---|---|---|---|---|
| G1 | 63.8 (60.7–65.5) → 63.9 (60.6–65.5) | 53.6 (50.3–54.9) → 53.0 (49.6–54.3) | 110.2 (107.2–111.6) → 110.6 (107.5–112.0) | 134.8 (131.8–135.9) → 134.9 (131.8–136.1) |
| G2 | 81.7 (80.2–83.7) → 82.1 (80.6–84.1) | 95.1 (94.4–98.8) → 95.5 (94.8–99.2) | 50.2 (48.8–53.3) → 50.6 (49.3–53.9) | 53.0 (52.3–56.5) → 53.2 (52.4–56.7) |
| G3+ | 55.3 (54.5–56.5) → 54.9 (54.1–56.2) | 97.6 (97.1–98.1) → 97.2 (96.7–97.7) | 40.5 (39.9–40.9) → 39.7 (39.1–40.2) | 58.6 (58.0–59.1) → 57.6 (57.1–58.2) |

Largest move of any generation under any alternative: 3.66 → 3.71 $bn.

Each alternative's move against the central split (new, $bn, (a) low / (a) high / (b) low / (b) high, G1; G2; G3+):

- `benefits_to_g1`: +1.69 / +1.26 / +1.39 / +1.19; -0.88 / -0.72 / -0.84 / -0.71; -0.80 / -0.55 / -0.54 / -0.48
- `benefits_to_usborn`: -0.47 / -0.72 / -0.74 / -0.77; +0.26 / +0.42 / +0.46 / +0.47; +0.21 / +0.30 / +0.29 / +0.31
- `justice_per_adult`: +0.29 / +0.29 / +0.29 / +0.29; -0.18 / -0.18 / -0.18 / -0.18; -0.11 / -0.11 / -0.11 / -0.11
- `foster_care_by_children`: +0.21 / +0.21 / -0.11 / -0.11; -0.10 / -0.10 / +0.11 / +0.11; -0.11 / -0.11 / -0.01 / -0.01
- `status_rules_all_to_g1`: +1.31 / -0.63 / +0.95 / -0.63; -1.53 / +0.16 / -1.39 / +0.16; +0.22 / +0.47 / +0.44 / +0.47
- `fill_ins_by_imputed_dollars`: -3.27 / -3.44 / -3.15 / -3.06; +2.02 / +3.71 / +3.22 / +3.57; +1.26 / -0.27 / -0.07 / -0.50
- `stack_scaling_by_union_factor`: +0.19 / +0.92 / +0.37 / +0.53; -0.07 / -0.56 / -0.16 / -0.36; -0.11 / -0.36 / -0.22 / -0.17
- `consumption_key_by_old_key_shares`: -0.17 / -0.17 / -0.03 / -0.03; -0.10 / -0.10 / -0.48 / -0.48; +0.26 / +0.26 / +0.51 / +0.51

Lean of the central rules, first generation: alternatives that would raise / lower its cost (largest move):

- old: (a) low: 5 up (≤1.7), 2 down (≤3.1); (a) high: 4 up (≤1.3), 3 down (≤3.3); (b) low: 4 up (≤1.4), 3 down (≤3.0); (b) high: 3 up (≤1.2), 4 down (≤2.9)
- new: (a) low: 5 up (≤1.7), 3 down (≤3.3); (a) high: 4 up (≤1.3), 4 down (≤3.4); (b) low: 4 up (≤1.4), 4 down (≤3.1); (b) high: 3 up (≤1.2), 5 down (≤3.1)

### Lane contributions by generation, $bn low / high (`lanes`)

| Lane | (a) G1 | (a) G2 | (a) G3+ | (b) G1 | (b) G2 | (b) G3+ |
|---|---|---|---|---|---|---|
| stack | +15.10 / +18.14 → +15.05 / +18.09 | +2.60 / -0.15 (same) | +2.21 / +3.23 (same) | +16.10 / +18.17 → +16.06 / +18.13 | +1.28 / -0.16 (same) | +2.53 / +3.20 (same) |
| cbo | +1.13 / +0.98 (same) | +5.15 / +3.88 (same) | +3.04 / +3.54 (same) | +1.57 / +0.75 (same) | +3.88 / +4.04 (same) | +3.87 / +3.61 (same) |
| ota | -0.09 / -0.12 (same) | -0.16 / -0.14 (same) | -0.12 / -0.08 (same) | -0.11 / -0.12 (same) | -0.15 / -0.14 (same) | -0.10 / -0.08 (same) |
| row1 | -3.97 / -11.39 (same) | -6.54 / -2.23 (same) | -3.72 / -0.62 (same) | -8.87 / -10.35 (same) | -3.53 / -2.91 (same) | -1.83 / -0.97 (same) |
| medical | -5.48 / -5.45 (same) | -5.26 / -5.27 (same) | -6.05 / -6.06 (same) | -6.29 / -6.27 (same) | -5.07 / -5.07 (same) | -5.44 / -5.44 (same) |
| education | +0.96 / +3.59 → +0.99 / +3.66 | -0.60 / -2.61 → -0.61 / -2.64 | +0.34 / -1.51 → +0.36 / -1.53 | -0.45 / -1.29 → -0.46 / -1.30 | +0.30 / +0.40 → +0.32 / +0.42 | +0.86 / +0.35 → +0.89 / +0.37 |
| benefits | +0.46 / +0.68 (same) | +0.90 / +0.77 (same) | +0.79 / +0.57 (same) | +0.73 / +0.73 (same) | +0.87 / +0.77 (same) | +0.55 / +0.51 (same) |
| justice | +0.53 / +0.53 (same) | +0.81 / +0.81 (same) | +0.69 / +0.69 (same) | +0.53 / +0.53 (same) | +0.81 / +0.81 (same) | +0.69 / +0.69 (same) |
| constants | -2.61 / -2.62 (same) | -1.10 / -1.12 (same) | -1.35 / -1.36 (same) | -2.80 / -2.82 (same) | -1.08 / -1.10 (same) | -1.18 / -1.19 (same) |
| row8_finite | new -0.03 / -0.03 | new -0.04 / -0.04 | new -0.04 / -0.04 | new -0.04 / -0.04 | new -0.03 / -0.03 | new -0.03 / -0.03 |
| consumption_key | new -0.93 / -0.93 | new -1.23 / -1.23 | new -1.89 / -1.89 | new -1.36 / -1.36 | new -0.77 / -0.77 | new -1.92 / -1.92 |
| Total correction | +6.04 / +4.33 → +5.06 / +3.40 | -4.20 / -6.05 → -5.47 / -7.36 | -4.17 / -1.60 → -6.07 / -3.53 | +0.40 / -0.66 → -1.05 / -2.11 | -2.69 / -3.35 → -3.48 / -4.14 | -0.04 / +0.69 → -1.96 / -1.24 |

Union contribution of each lane (sum of the generations under (a)), $bn low / high:

- stack: +19.91 / +21.21 → +19.86 / +21.17
- cbo: +9.32 / +8.40 → +9.32 / +8.40
- ota: -0.36 / -0.34 → -0.36 / -0.34
- row1: -14.23 / -14.23 → -14.23 / -14.23
- medical: -16.80 / -16.78 → -16.80 / -16.78
- education: +0.71 / -0.53 → +0.75 / -0.51
- benefits: +2.15 / +2.02 → +2.15 / +2.02
- justice: +2.03 / +2.03 → +2.03 / +2.03
- constants: -5.06 / -5.10 → -5.06 / -5.10
- row8_finite: new -0.10 / -0.10
- consumption_key: new -4.05 / -4.05

### Ledger comparison, account rows, $ per person a year (ledger_comparison.csv)

| Row | G1 shared | G2 shared | G3+ shared | G1 personal | G2 personal | G3+ personal |
|---|---|---|---|---|---|---|
| Direct lines at average cost | -7,635 → -7,647 | -8,882 → -8,894 | -7,015 → -7,027 | -5,751 → -5,763 | -9,804 → -9,816 | -9,689 → -9,701 |
| The same lines at the adopted responses | -5,448 → -5,533 | -6,165 → -6,281 | -4,294 → -4,398 | -4,505 → -4,534 | -7,171 → -7,286 | -7,014 → -7,121 |
| Plus the production term (the uncorrected model at the same specification) | -4,726 → -4,811 | -5,996 → -6,111 | -4,149 → -4,254 | -4,028 → -4,058 | -7,059 → -7,174 | -6,919 → -7,026 |
| Plus the corrections (adopted main case) | -5,220 → -5,225 | -5,703 → -5,729 | -3,859 → -3,831 | -4,383 → -4,336 | -6,636 → -6,661 | -6,808 → -6,779 |

Ledger rows (published gap, eight-band gaps, own balance) do not change: they are the September 19 ledger's.

### Numbers quoted in the lane RESULT's prose

- Minors moved to their parents' generation shift onto G1: $46.4–81.2bn → $46.8–81.9bn.
- Household allocation rule, (a), G1 and G3+ at the two ends: $19.1–32.0bn → $19.6–32.3bn.
- (b) second-generation adult as a share of a Mexico-born adult (per adult): 51–60% → 52–60%.
- old: corrections at the low end, $ per person (G1, G2, G3+): -494, +293, +291; production term 722, 169, 144; marginal responses take off 2,187, 2,717, 2,721, 1,246, 2,633, 2,675 (shared G1–G3+, personal G1–G3+); direct lines at the responses differ from the ledger's own balance by 71–481 (shared); account G2 below G1 by 483 (shared); G3+ below G2 by 171 (personal).
- new: corrections at the low end, $ per person (G1, G2, G3+): -414, +382, +423; production term 722, 169, 144; marginal responses take off 2,113, 2,613, 2,628, 1,228, 2,530, 2,581 (shared G1–G3+, personal G1–G3+); direct lines at the responses differ from the ledger's own balance by 175–400 (shared); account G2 below G1 by 505 (shared); G3+ below G2 by 118 (personal).

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

## For the parent

- **Not run by me.** The last two steps of `run_all.sh` (`main_case_2026_09_26/main_case.cjs`, then
  `main_case_schools_full_2026_09_26/main_case.cjs`) write into those lanes. Run them at commit time;
  both should leave their lanes byte-identical.
- **Research memo (20f68c1).** It quotes "$62.1bn (low end) and $48.5bn (high end) over September 24".
  That is still the sum of the two school parts at the September 24 ends: 3.72 + 58.36 and
  3.04 + 45.44. The shares (76–91%, 43–44%) are unchanged, so no number there is wrong. Against the
  one-year scenario the figure is +$58.4bn / +$45.4bn at matched specifications, or +$57.6bn / +$46.3bn
  with the move of the range ends.
- **Winners-and-losers ledger.** `winners_losers.py` reads `generation_results.csv` from the working
  tree, and that file is unchanged since 2441ac8. Its gate against its own September 24 band still
  fails until W4 moves it.
- **To commit** (explicit paths): `run_generations.cjs`, `run_all.sh`, `RESULT.md`,
  `derived/generation_summary.json` and this file.

## Limits

- **Bridge order** (the parent's call: matched specifications first). If the range ends moved first, at
  the September 26 responses, the union's last two links would be +$9.32bn / −$13.73bn (end move) and
  +$48.25bn / +$59.99bn (schools at full cost). Their sum does not change, and neither do the
  generations' shares of the school part.
- **Remainders.** The own-factor scaling leaves $0.31bn of the consumption key and $0.43bn of the
  ratio-type lanes to spread by cells. The union-factor alternative is reported.
- **Saving ratio.** It varies by income rank only, because CE records no parents' birthplace. The
  corridor's per-capita spread inside a unit is the consumption lane's, so a Mexico-born parent's
  remittances lower their US-born children's key.
- **Inherited from the main case.** The shelter constant stays keyed to 0.59/0.84, about −$0.002bn
  against the adopted general-government responses. School dilution does not apply at a response of
  1 (decision `2026-09-26-main-case-schools-full-cost`).
- **Instrument.** An LLM assembled this (`notes/llm-bias-caveat.md`). The split rules for the new edits
  were fixed before the results were seen, and neither the repointing nor the chain changed a rule.
