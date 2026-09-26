**Verdict:** Done. On the schools case (the main case charges pupils at their full average cost),
fewer other residents come out ahead of the group's presence. Pooled within households, **20.5%** are
ahead under tax-share financing and **19.0%** under per-person cuts, down from 23.9% and 21.4%. The
person count gives 18.4% and 18.3% (was 20.1% and 19.9%).
- The fiscal channel rises from $223.4bn to **$275.0bn** at central values. 83% of it is state and
  local (was 81%), because the school step is 8.2% federal.
- The social net on today's residents goes from −$263.9bn to **−$314.4bn**, or −$1,063 per other
  resident.
- School dilution ($20.1bn) leaves the nets, since nothing is left unfunded at a school response of 1.
  The consumption key sits inside the fiscal channel, so its proposal row is gone.
- The one-year scenario stays within 0.1 point of September 24 on every headline share (largest gap
  0.07 point). Across all 238 percentage rows the largest gap is 0.22 point (landscaping workers,
  person count).
- Real-costs totals (step 1): the published pairing is **$305–350bn** (was $248–304bn).
- `--case sept24` still rebuilds all 23 committed ledger files byte for byte. Two runs of each case
  are identical.

`winners_losers_2026_09_24/derived/` now holds the schools case, the convention W1 and W2 used for
their lanes. Three Sept 24-named files there are left from the old run and need a decision at commit
(see "For the parent"). Step 1 is committed (4e66adb); step 2 is not.

# W4 `ledger`: real-costs totals and the winners-and-losers ledger on the schools case

Date 2026-09-26. Case `sept26_schools` = `main_case_schools_full_2026_09_26` ($258.4885–291.9548bn).
Its responses are school 1/1 and general government 0.6000/0.8504, both read from `corrections.json`
→ `meta.responses`. Pins from the parent:
- base (distribution) 39b854b, and f697514 for the one-year scenario;
- debt legacy 1db19c8, and e62fccb for the one-year scenario. The ledger reads these derived files
  through git, and they are identical at 90c4b23. `constant_choices.py` ran `debt_legacy.py` itself
  at 90c4b23;
- generation 0f22f0c;
- sister lanes at their current commits.

## Step 1: band variants, real-costs totals, constant choices (final)

**What changed.** `band_variants.cjs`, `real_costs_totals.py` and `constant_choices.py` in
`sept24_propagation_2026_09_24/` each take `--case sept24 | sept26 | sept26_schools`. The default is
`sept26_schools`, and no script was copied.

| Case | Package, payload, responses | Outputs |
|---|---|---|
| `sept24` | `main_case_2026_09_24` | `sept24_propagation_2026_09_24/derived/` (committed files, unchanged) |
| `sept26_schools` (default) | `main_case_schools_full_2026_09_26` | `sept26_propagation_2026_09_26/derived/` |
| `sept26` (one-year scenario) | `main_case_2026_09_26` | `--out-dir` only; written to `sept26_propagation_2026_09_26/derived/sept26/` |

- **`band_variants.cjs`** runs the September 23 and 24 cases as before. For a later case it adds the
  uncorrected model and the case's payload, both at the responses in `meta.responses`, mapped value
  for value onto the September 24 specifications.
- **`real_costs_totals.py`** reads its band file from the same directory and adds the case's column.
  `change` is the case minus September 24, and the file must name its case.
- **`constant_choices.py`** builds its base split from a `debt_legacy.py --case` run into a temporary
  directory. On the September 26 cases row 8 includes its finite-removal piece (`row8_finite`,
  −$0.10bn), and the ledger lane's choice zeroes both parts. It writes nothing until every gate
  passes.

**Gates** (all pass):
- `sept24` reproduces all six committed files byte for byte.
- On the schools case, `meta.responses` equals `summary.json` → `responses`, and the mapped
  specifications equal the package's `MAIN_SPECS`.
- The adopted variant reproduces $258.4885–291.9548bn, and the uncorrected model
  $265.5903–298.6797bn. Both hold to 1e-9 against `summary.json` and to 1e-4 against
  `main_case_bands.csv`.
- Each variant moves every specification by the same amount on the uncorrected and corrected models
  (largest gap 1.1e-13).
- The one-year scenario passes the same gates at $200.9180–245.6949bn.
- Two runs of each case are byte-identical.

**Final runs.** Both schools-case JSONs record the f1e4f5b `summary.json`; that commit changed only
its `school` key, which these scripts do not read. `constant_choices.py` ran on all three cases after
W1's commit, and a second run was byte-identical. Those runs executed `debt_legacy.py` at 90c4b23,
which was in the working tree from 00:16 and committed later. Its outputs match those under
1db19c8's `debt_legacy.py`. A rerun on the clean tree at 90c4b23 on 2026-09-27 reproduces all six
committed files (4e66adb). The early values below proved final.

### Old → new, band variants ($bn a year; low end shared allocation, high end personal)

Files, by column:
- Sept 24: `sept24_propagation_2026_09_24/derived/band_variants.csv`, case `sept24`.
- Schools case: `sept26_propagation_2026_09_26/derived/band_variants.csv`, cases `sept26_schools` and
  `sept26_schools_uncorrected`.
- One-year: `…/derived/sept26/band_variants.csv`, cases `sept26` and `sept26_uncorrected`.

| Variant | Sept 24 | Schools case | One-year scenario |
|---|---:|---:|---:|
| adopted | 200.9 to 246.3 | 258.5 to 292.0 | 200.9 to 245.7 |
| justice_raw_coding | 196.6 to 242.0 | 254.2 to 287.7 | 196.6 to 241.4 |
| justice_grid_low | 193.9 to 239.3 | 251.5 to 285.0 | 193.9 to 238.7 |
| justice_grid_high | 203.6 to 249.0 | 261.2 to 294.7 | 203.6 to 248.4 |
| justice_cbp_fixed | 197.8 to 243.2 | 255.4 to 288.8 | 197.8 to 242.6 |
| uncompensated_use_0.7 | 199.3 to 244.1 | 257.0 to 289.7 | 199.4 to 243.5 |
| justice_grid_low_and_uncompensated_use_0.7 | 192.4 to 237.1 | 250.0 to 282.7 | 192.4 to 236.5 |
| Uncorrected model at the case's responses | — | 265.6 to 298.7 | 207.4 to 253.2 |

### Old → new, real-costs totals (memo §7 and §7b)

Files, by column (low and high are the file's `(low)` and `(high)` rows):
- Sept 24: `sept24_propagation_2026_09_24/derived/real_costs_totals.csv`, column `sept24`.
- Schools case: `sept26_propagation_2026_09_26/derived/real_costs_totals.csv`, column `sept26_schools`.
- One-year: `…/derived/sept26/real_costs_totals.csv`, column `sept26`.

| Quantity | Unit | Sept 24 | Schools case | One-year scenario |
|---|---|---:|---:|---:|
| §7 hispanic: fiscal main case | $bn | 196.6 to 242.0 | 254.2 to 287.7 | 196.6 to 241.4 |
| §7 hispanic: total at central values | $bn | 245.7 to 296.4 | 303.3 to 342.0 | 245.7 to 295.7 |
| §7 hispanic: per group member | $k | 6.01 to 7.25 | 7.42 to 8.36 | 6.01 to 7.23 |
| §7 hispanic: victims' harm, full cost | $bn | 28.92 | 28.92 | 28.92 |
| §7 custody: fiscal main case | $bn | 200.9 to 246.3 | 258.5 to 292.0 | 200.9 to 245.7 |
| §7 custody: total at central values | $bn | 253.4 to 304.0 | 311.0 to 349.7 | 253.4 to 303.4 |
| §7 custody: per group member | $k | 6.20 to 7.43 | 7.60 to 8.55 | 6.20 to 7.42 |
| §7 custody: victims' harm, full cost | $bn | 32.34 | 32.34 | 32.34 |
| §7 hispanic_mixed_group (decision 4's victims): total | $bn | 247.7 to 298.4 | 305.3 to 344.0 | 247.7 to 297.7 |
| §7 hispanic_mixed_group: per group member | $k | 6.06 to 7.30 | 7.47 to 8.41 | 6.06 to 7.28 |
| §7 custody_mixed_scaled: total (withdrawn hybrid; quoted nowhere) | $bn | 255.6 to 306.3 | 313.2 to 351.9 | 255.7 to 305.7 |
| §7 full span | $bn | 210.2 to 336.9 | 267.8 to 382.6 | 210.2 to 336.3 |
| §7 full span per group member | $k | 5.14 to 8.24 | 6.55 to 9.35 | 5.14 to 8.22 |
| §7 full span with the case's own range [may double count the arrest ratio] | $bn | 181.5 to 366.8 | 207.1 to 414.9 | 173.1 to 367.7 |
| §7b costs only: fiscal (care's $4.15bn added back) | $bn | 205.0 to 250.5 | 262.6 to 296.1 | 205.1 to 249.8 |
| §7b costs only: social items | $bn | 52.51 to 57.73 | 52.51 to 57.73 | 52.51 to 57.73 |
| §7b costs only: total | $bn | 257.5 to 308.2 | 315.1 to 353.8 | 257.6 to 307.6 |
| §7b costs only: per group member | $k | 6.30 to 7.54 | 7.71 to 8.65 | 6.30 to 7.52 |
| §7b with care and mobility: fiscal | $bn | 200.9 to 246.3 | 258.5 to 292.0 | 200.9 to 245.7 |
| §7b with care and mobility: social items | $bn | 51.85 to 57.07 | 51.85 to 57.07 | 51.85 to 57.07 |
| §7b with care and mobility: total | $bn | 252.7 to 303.4 | 310.3 to 349.0 | 252.8 to 302.8 |
| §7b with care and mobility: per group member | $k | 6.18 to 7.42 | 7.59 to 8.53 | 6.18 to 7.40 |
| §7b adding the scale net: fiscal | $bn | 186.9 to 232.4 | 244.6 to 278.0 | 187.0 to 231.8 |
| §7b adding the scale net: social items | $bn | 51.85 to 57.07 | 51.85 to 57.07 | 51.85 to 57.07 |
| §7b adding the scale net: total | $bn | 238.8 to 289.5 | 296.4 to 335.1 | 238.8 to 288.8 |
| §7b adding the scale net: per group member | $k | 5.84 to 7.08 | 7.25 to 8.19 | 5.84 to 7.06 |
| §7b omitted benefits, without / with the scale net | $bn | 0.655 / 14.58 | 0.655 / 14.58 | 0.655 / 14.58 |
| §7b omitted benefits, share of main case (low, high) | % | 0.266, 7.26 | 0.224, 5.64 | 0.267, 7.26 |
| The memo's 2026-09-24 revision note (a Sept 24 figure) | $bn | 252.7 to 303.4 | — | — |

The published pairing runs from the equal footing's low end (decision 4's victims) to the custody
footing's high end: $247.7–304.0bn on Sept 24, **$305.3–349.7bn** on the schools case and
$247.7–303.4bn in the one-year scenario. The social rows do not depend on the case.

### Old → new, constant choices (row 8 and row 10: the ledger lane's split minus this lane's)

Files, by column: `sept24_propagation_2026_09_24/derived/constant_choices.csv` (the 2024 split) and
`constant_choices_stock.csv` (stock and interest) for Sept 24; the same two files in
`sept26_propagation_2026_09_26/derived/` (schools case) and `…/derived/sept26/` (one-year).

| Quantity, $bn | Sept 24 | Schools case | One-year |
|---|---:|---:|---:|
| Row 8 amount (with its finite-removal piece from Sept 26) | 2.000 | 1.898 | 1.898 |
| Row 8: federal part of the 2024 gap, central and high conventions | −0.0285 | −0.0271 | −0.0271 |
| Row 8: legacy stock entering 2024 (central rule) | −0.372 | −0.353 | −0.353 |
| Row 8: legacy interest 2024 (central rule) | −0.0120 | −0.0114 | −0.0114 |
| Row 10: federal part of the 2024 gap | 0.000 | 0.000 | 0.000 |
| Row 10: legacy stock / interest 2024 | +2.029 / +0.0656 | +2.029 / +0.0656 | +2.029 / +0.0656 |

The school response enters neither constant; the two later cases agree to 1e-6.

## Step 2: the winners-and-losers ledger on the schools case

### Item 1: unpinned reads (done in round 1)

The September 24 rerun found three inputs that had moved under the ledger:
- the debt lane's per-correction file, pinned at ed1b623;
- the generation results, pinned at ba12f3c;
- the four sister lanes' rows and verdicts, pinned at e4bdf40, c98f479, fa338b8 and f9c9504.

With those pins, all 23 committed `derived/` files reproduced byte for byte.

### Items 2–4: what changed in `winners_losers_2026_09_24/`

- **`specs.cjs`** takes `--case` and `--out-dir`. It imports the case's `package.cjs`, whose
  `MAIN_SPECS` carry the payload's responses (gated), and evaluates two models: the case and the case
  before it.

  | Case | Models evaluated |
  |---|---|
  | `sept24` | `adopted_2026_09_23`, `adopted_2026_09_24` |
  | `sept26` | `adopted_2026_09_24`, `adopted_2026_09_26` |
  | `sept26_schools` | `adopted_2026_09_26`, `adopted_2026_09_26_schools` |

  - Its band gates stay, now against the case's own `main_case_bands.csv`.
  - A new gate checks the engine state at every specification against the package's `cost()`
    (largest gap 0).
- **`winners_losers.py`** has a `CASES` table and `configure()`. Each case names:
  - its model, lane, ladder entry and previous case;
  - its pins: base, debt, per-correction file, generation, sisters and interest;
  - its real-costs directory.
- **Pins added in the lane's style:** `BASE26S_COMMIT = "39b854b"`, `DEBT26S_COMMIT = "1db19c8"` and
  `GEN26S_COMMIT = "0f22f0c"`. The one-year scenario costs one more row: `BASE26_COMMIT = "f697514"`
  and `DEBT26_COMMIT = "e62fccb"`, with its generation split read from `generation_summary.json` →
  `change_from_sept26` at 0f22f0c. The sister lanes are pinned by `SISTER26_COMMITS` (8936938,
  1c9b6fe, 1d14b54, 1c9b6fe), their latest commits. Between the two sets of pins only each lane's
  RESULT.md changed, and the ledger reads their verdict lines from it.
- **Per-correction check.** From September 26 on, row 8's finite piece is its own component
  (`finite_removal`), so the check matches `lane_constants` plus `finite_removal` against the
  `lane_constants` line (12 rows, largest gap 1.0e-6bn).
- **Consumption key (item 3).** The `consumption_key_proposal` registry row and its two gates run for
  `sept24` only. Under the later cases the fiscal row's note says the key is inside it.
- **School dilution (item 4).** At a school response of 1 in every specification, which is read
  from `fiscal_specs.csv`, the lane's rows 0 and 11 stay in the role table. They carry the label
  "applies to the lower-response scenarios only…", citing the decision's "School dilution" bullet.
  - The `school_dilution` registry row reads "role table only", and the page table's basis carries
    the label.
  - In the one-year scenario (0.652/0.681) the rows stay allocated, as on September 24.
- **Outputs.** Every case writes to `derived/` unless `--out-dir` is given; `derived/` holds the
  default case, as in W1's and W2's lanes.
  - The regression and quintile files are named by case.
  - The later cases add a `case` block to `inputs.json`.
  - An `--out-dir` run writes its person frame to `_cache/person_frame_<case>.parquet`.
- **`test_winners_losers.py`** adds three tests to the twelve: a role-only lane keeps its
  allocatable rows out of the nets; the school response selects that lane; `configure()` sets each
  case's paths and pins, with `sept24` on its committed paths. All 15 pass.
- **`old_new.py`** (new) writes `sept26_propagation_2026_09_26/derived/old_new_ledger.csv`. It
  selects 643 rows across the three cases from the ledger files, with nothing typed in. It rebuilds
  the one-year scenario into a temporary directory (21 s in all). A rerun is byte-identical.
- **Lane RESULT.md.** The verdict carries a dated bracket with the new headline, and the Files section
  gives the flags.

### Item 5: compliance and vending rows (no rerun needed)

Neither row builder depends on the case, so their files were left alone.

| Builder | What it reads |
|---|---|
| `compliance_gap_2026_09_24/winners_losers.py` | its own `derived/` (`edges_totals.csv`, `edges_by_industry_year.csv`, `edges_by_industry.csv`, `panel_c.csv`, `composition_check.csv`), its `_cache/panel/qcew_cells.parquet`, and constants from its `edges.py` |
| `vending_restaurants_2026_09_24/size_rows.py` | its own `_cache/` (BLS, CDTFA, ACS, CBP) and `derived/` files |

"main_case_2026_09_24" appears in both only as a text label naming the September 24 tax-records
correction. The later payloads carry that correction unchanged. The ledger reads both lanes' rows at
pinned commits (1d14b54, 1c9b6fe).

### Item 6: gates (all pass)

| Check | `sept24` | One-year (`sept26`) | Schools (`sept26_schools`) |
|---|---|---|---|
| Ledger gates, all passing | 443 | 441 (the consumption proposal's 2 drop out) | 435 (those 2 and the dilution rows' 6 closures drop out) |
| Generations add to the case's band (tolerance 1e-3) | to 4.8e-7bn (6-decimal file) | to 1.7e-12bn | to 6.8e-7bn (6-decimal file) |
| A from `fiscal_totals(case)` at the pinned base, minus the engine's | +4.9e-5 / −3.4e-5bn | same | same |
| Regression against the base lane's `channel_by_quintile.csv` (468 cells) | 5b8957e, 7ec7144: 2.8e-14bn | 7ec7144, f697514: 2.8e-14bn | f697514: 2.8e-14bn; 39b854b: 7.1e-15bn |
| Federal split recomputed from the debt lane's lines | b42efdc, 7ec7144: lines to 5.0e-7bn | 7ec7144, e62fccb: same | e62fccb, 1db19c8: same |
| Per-correction file against the lane's lines (12 rows) | 1.1e-16bn | 1.0e-6bn | 1.0e-6bn |
| Debt interest pinned, main benchmark ($bn) | 28.3387 / 36.4297 | 28.2483 / 36.3485 | 30.1448 / 37.8726 |
| `specs.cjs`: bands against `main_case_bands.csv` (1e-4); costs against the package's `cost()` | yes; gap 0 | yes; gap 0 | yes; gap 0 |

**Reproducibility:**
- `sept24` in place rewrote all 23 `derived/` files, each identical to the committed ones (8a762fe).
  With the final code, a run into a fresh `--out-dir` gives 22 byte-identical files. The manifest
  differs only in the two cells that record where the specs were read, and their hashes agree.
- Two in-place runs of the schools case left all 26 files in `derived/` byte-identical, and
  `derived/` still matches them. A scratch run matches except for the same two manifest cells.
- Two one-year runs into different directories agree except for those manifest cells.
- `specs.cjs` rerun into scratch on 2026-09-27 reproduces its two files for all three cases.
- The pytest suite passes (15).

## Old → new, the ledger's published numbers

The full table is in `sept26_propagation_2026_09_26/derived/old_new_ledger.csv` (643 rows):
- every share ahead, stack and unit;
- every channel-table row;
- every cut in the memo's tables;
- geography, quintile burden and winner cells;
- pooling, the registry at low, central and high;
- the group frame, the federal split, and the totals in `inputs.json`.

Files by column (all in `winners_losers_2026_09_24/derived/`):
- Sept 24: the files committed at 8a762fe.
- Schools case: the working tree.
- One-year: `--case sept26 --out-dir DIR`, which `old_new.py` rebuilds.

**Share of other residents ahead** (`net_shares.csv`)

| Quantity | Unit | Sept 24 | Schools case | One-year | Change to schools |
|---|---|---:|---:|---:|---:|
| Social net, pooled, tax shares (a) | % | 23.9 | 20.5 | 23.9 | −3.4 |
| Social net, pooled, per person (b) | % | 21.4 | 19.0 | 21.4 | −2.3 |
| Social net, pooled (a), every choice least costly | % | 30.0 | 27.1 | 30.0 | −2.9 |
| Social net, pooled (a), every choice most costly | % | 13.9 | 11.9 | 13.9 | −2.0 |
| Social net, pooled (b), least costly | % | 27.0 | 24.2 | 27.0 | −2.8 |
| Social net, pooled (b), most costly | % | 13.8 | 12.3 | 13.8 | −1.5 |
| Social net, person count (a) | % | 20.1 | 18.4 | 20.1 | −1.7 |
| Social net, person count (b) | % | 19.9 | 18.3 | 19.9 | −1.6 |
| Social net, person count (a), least / most costly | % | 24.0 / 14.0 | 22.2 / 12.8 | 24.0 / 14.0 | −1.8 / −1.2 |
| Account net, pooled (a) | % | 28.5 | 24.4 | 28.5 | −4.1 |
| Account net, pooled (b) | % | 23.5 | 20.6 | 23.5 | −2.9 |
| With proposed, pooled (a) | % | 20.8 | 21.6 | 20.8 | +0.8 |
| With proposed, pooled (b) | % | 20.3 | 20.2 | 20.3 | −0.1 |
| Fiscal cost charged nationally, person count (a) | % | 13.0 | 10.1 | 13.0 | −2.9 |
| Housing at the national-uniform central, person count (a) | % | 18.4 | 16.9 | 18.5 | −1.5 |
| Victims on the custody footing, person count (a) | % | 20.0 | 18.3 | 20.0 | −1.7 |

The "with proposed" net rises under (a) because school dilution (−$20.1bn on the households of
pupils) leaves it while the fiscal cost grows.

**Totals** (`fiscal_federal_split.csv`, `net_shares.csv`, `pooling_moves.csv`, `channels.csv`,
`inputs.json`)

| Quantity | Unit | Sept 24 | Schools case | One-year | Change to schools |
|---|---|---:|---:|---:|---:|
| Fiscal channel, central (A + F) | $bn | 223.4 | 275.0 | 223.1 | +51.6 |
| federal part, central payer convention | $bn | 41.9 | 46.0 | 41.7 | +4.0 |
| of which future taxpayers (deficit-financed) | $bn | 11.3 | 12.4 | 11.2 | +1.1 |
| state and local part | $bn | 181.5 | 229.1 | 181.4 | +47.6 |
| federal share | share | 0.188 | 0.167 | 0.187 | −0.021 |
| Account net on today's residents | $bn | −212.3 | −262.8 | −212.1 | −50.5 |
| Social net on today's residents | $bn | −263.9 | −314.4 | −263.7 | −50.5 |
| mean per other resident | $ | −892 | −1,063 | −891 | −171 |
| median, pooled (a) | $ | −377 | −443 | −377 | −66 |
| median, pooled (b) | $ | −505 | −593 | −504 | −88 |
| With proposed on today's residents | $bn | −270.6 | −301.1 | −270.4 | −30.5 |
| Pooling (a): moved ahead | m | 28.1 | 24.2 | 28.1 | −3.9 |
| Pooling (a): moved behind | m | 16.8 | 17.9 | 16.8 | +1.0 |
| Main case (registry, band ends; signed) | $bn | −200.9 to −246.3 | −258.5 to −292.0 | −200.9 to −245.7 | −57.6 / −45.6 |
| Published total, equal footing | $bn | 247.7 to 298.4 | 305.3 to 344.0 | 247.7 to 297.7 | +57.6 / +45.6 |
| Published total, custody footing | $bn | 253.4 to 304.0 | 311.0 to 349.7 | 253.4 to 303.4 | +57.6 / +45.6 |
| Published range | $bn | 247.7 to 304.0 | 305.3 to 349.7 | 247.7 to 303.4 | +57.6 / +45.6 |
| Published full span | $bn | 210.2 to 336.9 | 267.8 to 382.6 | 210.2 to 336.3 | +57.6 / +45.6 |
| Allocation base, every choice least / most costly (mixed footing; signed) | $bn | −217.0 to −334.0 | −274.6 to −379.7 | −217.0 to −333.4 | −57.6 / −45.6 |
| Debt legacy interest, 2024 (apart) | $bn | 28.3 to 36.4 | 30.1 to 37.9 | 28.2 to 36.3 | +1.8 / +1.4 |
| School dilution in the with-proposed net | $bn | −20.1 | role table only | −20.1 | — |
| Consumption-key proposal (registry row) | $bn | +4.05 | inside the fiscal row | inside the fiscal row | — |

**Who gains and who loses, by channel** (`winners_losers_table.csv`, $bn a year)

| Row | Sept 24 | Schools case | One-year |
|---|---:|---:|---:|
| Fiscal cost, tax-share financing (a): taxpayers today (293.2m; $ per person −723 → −896) | −212.1 | −262.6 | −211.9 |
| Fiscal cost, per-person financing (b): every other resident (295.8m; −717 → −888) | −212.1 | −262.6 | −211.9 |
| Future federal taxpayers (deficit-financed part) | −11.3 | −12.4 | −11.2 |
| School dilution rows 0 and 11 (instruction, support services) | −16.1, −4.0 (allocated) | −16.1, −4.0 (role table only) | −16.1, −4.0 (allocated) |

Wages (+95.8 / −96.0), rent (−33.9), rent receipts (+37.4), victims (−30.9), congestion (−19.2),
unreimbursed care (−4.4), property crime (−1.3), mobility (+0.7), preferences (−0.6) and city size
(+8.0) do not move.

**Person nets by cut** (`person_nets_by_cut.csv`, social net, pooled; $ per person a year)

| Cut | Net (a), Sept 24 → schools | Ahead (a) / (b), Sept 24 | Ahead (a) / (b), schools | Ahead (a), one-year |
|---|---:|---:|---:|---:|
| California | −2,751 → −3,344 | 3.3% / 4.7% | 2.7% / 3.9% | 3.3% |
| Texas | −2,661 → −3,207 | 2.2% / 3.5% | 1.8% / 3.0% | 2.2% |
| All states except California and Texas | −544 → −638 | 27.9% / 24.7% | 24.0% / 22.0% | 27.9% |
| US-born, below high school, 25+ | −981 → −1,047 | 2.8% / 1.7% | 2.4% / 1.5% | 2.8% |
| US-born, high school, 25+ | −1,460 → −1,573 | 3.2% / 2.7% | 2.7% / 2.4% | 3.2% |
| US-born, some college, 25+ | −657 → −811 | 25.6% / 21.3% | 21.3% / 18.4% | 25.6% |
| US-born, BA or more, 25+ | −708 → −975 | 37.4% / 39.4% | 32.4% / 35.9% | 37.5% |
| Other foreign-born, below high school, 25+ | −1,389 → −1,480 | 3.0% / 1.7% | 2.3% / 1.4% | 3.0% |
| Other foreign-born, high school, 25+ | −1,666 → −1,792 | 5.3% / 3.4% | 4.0% / 3.0% | 5.3% |
| Other foreign-born, some college, 25+ | −832 → −1,016 | 29.3% / 21.1% | 25.5% / 18.6% | 29.3% |
| Other foreign-born, BA or more, 25+ | −1,024 → −1,336 | 37.1% / 36.0% | 33.3% / 33.1% | 37.1% |
| Under 25 | −724 → −849 | 25.4% / 19.0% | 21.7% / 16.5% | 25.4% |
| Renters | −1,269 → −1,401 | 13.3% / 10.5% | 11.5% / 9.5% | 13.4% |
| Owners without rental income | −849 → −1,015 | 25.5% / 22.6% | 21.7% / 19.9% | 25.5% |
| Landlords | +114 → −227 | 48.8% / 50.5% | 42.8% / 46.8% | 48.8% |
| Under 18 | −629 → −754 | 27.8% / 20.1% | 23.7% / 17.3% | 27.8% |
| 18–64 | −1,037 → −1,227 | 26.6% / 25.0% | 22.9% / 22.4% | 26.6% |
| 65 and over | −727 → −887 | 11.5% / 11.8% | 9.9% / 10.6% | 11.5% |
| Workers in construction | −1,504 → −1,674 | 19.6% / 17.9% | 16.3% / 16.2% | 19.6% |
| Workers in restaurants | −1,072 → −1,203 | 18.4% / 14.5% | 16.1% / 12.3% | 18.4% |
| Workers in agriculture | −963 → −1,113 | 21.5% / 21.9% | 17.5% / 19.3% | 21.5% |
| Workers in landscaping | −1,064 → −1,186 | 15.3% / 12.7% | 13.5% / 11.7% | 15.3% |
| Workers in other industries | −1,093 → −1,315 | 31.1% / 30.7% | 26.8% / 27.7% | 31.2% |
| Not working | −651 → −778 | 17.9% / 13.5% | 15.3% / 11.7% | 17.9% |
| Non-Hispanic white | −828 → −1,004 | 25.9% / 24.2% | 22.2% / 21.6% | 26.0% |
| Non-Hispanic Black | −810 → −913 | 18.3% / 13.7% | 15.6% / 11.9% | 18.3% |
| Non-Hispanic Asian | −1,286 → −1,590 | 25.9% / 24.9% | 23.3% / 22.6% | 25.9% |
| Hispanic, other than Mexican origin | −1,075 → −1,203 | 18.6% / 13.5% | 16.0% / 11.7% | 18.6% |
| Other race | −1,032 → −1,213 | 18.3% / 15.5% | 15.6% / 13.5% | 18.4% |
| Women | −828 → −989 | 23.7% / 21.1% | 20.4% / 18.7% | 23.8% |
| Men | −959 → −1,140 | 24.0% / 21.7% | 20.5% / 19.4% | 24.0% |
| Decile 1 | −559 → −592 | 2.8% / 0.5% | 2.2% / 0.4% | 2.8% |
| Decile 2 | −627 → −677 | 7.4% / 0.9% | 6.0% / 0.7% | 7.4% |
| Decile 3 | −704 → −765 | 12.2% / 2.7% | 10.1% / 1.9% | 12.2% |
| Decile 4 | −789 → −867 | 17.4% / 6.8% | 14.7% / 4.8% | 17.4% |
| Decile 5 | −826 → −923 | 22.6% / 12.3% | 19.4% / 9.1% | 22.7% |
| Decile 6 | −838 → −956 | 29.1% / 20.6% | 25.0% / 16.4% | 29.1% |
| Decile 7 | −908 → −1,057 | 30.1% / 28.1% | 26.6% / 23.8% | 30.2% |
| Decile 8 | −928 → −1,117 | 36.6% / 38.2% | 31.4% / 34.4% | 36.6% |
| Decile 9 | −937 → −1,186 | 39.3% / 44.3% | 34.0% / 41.7% | 39.3% |
| Decile 10 | −1,804 → −2,490 | 41.3% / 59.6% | 35.5% / 57.1% | 41.3% |

Some quoted figures change sign or class:
- Landlords' pooled net under (a) turns negative (+$114 → −$227). Under (b) it stays positive
  (+$740 → +$543).
- The top decile's net under (b) and the person-count columns are in the CSV.

**Geography, burden and cells** (`cuts.csv`, `winner_cells.csv`; person count, central)

| Quantity | Unit | Sept 24 | Schools case | One-year |
|---|---|---:|---:|---:|
| California, social net (a) | $ | −2,751 | −3,344 | −2,750 |
| California, fiscal cost charged nationally (a) | $ | −1,359 | −1,588 | −1,358 |
| Texas, social net (a) | $ | −2,661 | −3,207 | −2,660 |
| Texas, fiscal cost charged nationally (a) | $ | −1,271 | −1,453 | −1,270 |
| All other states, social net (a) | $ | −544 | −638 | −543 |
| All other states, fiscal cost charged nationally (a) | $ | −810 | −974 | −809 |
| Arizona, social net (a) | $ | −2,832 | −3,399 | −2,830 |
| Arizona, share ahead (a) | % | 3.2 | 2.9 | 3.2 |
| Bottom quintile, social net (a), share of SPM resources | % | −6.2 | −6.6 | −6.2 |
| Top quintile, same | % | −1.5 | −2.0 | −1.5 |
| US-born BA+ landlords, share ahead (a) / (b) | % | 58.4 / 66.2 | 53.9 / 62.2 | 58.5 / 66.2 |
| US-born high school in California, mean net (a) / (b) | $ | −4,079 / −4,527 | −4,551 / −5,116 | −4,078 / −4,526 |
| US-born high school in Texas, mean net (a) / (b) | $ | −3,808 / −4,311 | −4,226 / −4,856 | −3,807 / −4,310 |

**The group's own frame** (`group_frame.csv`, $bn a year, low to high end)

| Item | Sept 24 | Schools case | One-year |
|---|---:|---:|---:|
| Direct fiscal transfer received (A, sign flipped) | 214.2 to 255.1 | 271.8 to 300.7 | 214.2 to 254.5 |
| Account's cost attributed to the first generation (NAS convention) | 110.2 to 134.8 | 135.6 to 155.4 | 110.6 to 134.9 |
| Second generation | 50.2 to 53.0 | 67.9 to 66.1 | 50.6 to 53.2 |
| Third-plus generation | 40.5 to 58.6 | 55.0 to 70.5 | 39.7 to 57.6 |

The place premium, the group's own wage rows, the victims inside the group and remittances do not
move. The generation rows equal the generation lane's (0f22f0c, and `change_from_sept26` for the
one-year scenario).

## For the parent

- **`derived/` of the ledger now holds the schools case**, following W1's and W2's convention.
  `--case sept24` rebuilds the committed September 24 files. These are left from that run and are
  not written by the default run: `regression_sept23.csv`, `regression_sept24.csv` and
  `quintiles_vs_base_sept24.csv`. They are unchanged from 8a762fe. I suggest deleting them in the
  commit that moves `derived/`, so the directory holds one run. I did not delete tracked files.
- **Downstream text still on Sept 24:**
  - the memo `research/immigration-winners-and-losers-2026-09-25.md` (last changed c959a02);
  - ladder 226;
  - the INDEX paragraph on the ledger (line 146: "23.9% under tax-share financing and 21.4% under
    per-person cuts").

  They are outside my boundary. The old → new CSV gives every quoted number.
- **The one-year ledger run is not stored** (23 files, 1.8 MB), so `derived/` holds one case.
  `old_new.py` rebuilds it into a temporary directory, and its numbers are the CSV's `sept26` column.
- **Debt lane after the pin:** 90c4b23 split that lane's bridge step in two, with the same totals.
  Among its derived files it changed only `sept26_schools_bridge_2024.csv`, which the ledger does not
  read. The ledger reads `federal_split_2024_lines.csv`, `federal_split_2024.csv`, `summary.json`,
  `stocks.csv` and the per-correction file through git at 1db19c8 and e62fccb. Those files are
  unchanged at 90c4b23, so the pins stand.

## Files

Step 1 is committed at 4e66adb:
- in `sept24_propagation_2026_09_24/`: `band_variants.cjs`, `real_costs_totals.py` and
  `constant_choices.py`;
- in `sept26_propagation_2026_09_26/derived/` and in `derived/sept26/`: `band_variants.csv` and
  `.json`, `real_costs_totals.csv` and `.json`, `constant_choices.csv` and
  `constant_choices_stock.csv`.

Step 2 is uncommitted:
- `sept26_propagation_2026_09_26/RESULT_ledger.md` and `derived/old_new_ledger.csv`
  (`old_new_lanes.csv` there is W1's).
- `winners_losers_2026_09_24/`:
  - `specs.cjs`, `winners_losers.py`, `test_winners_losers.py`, `old_new.py` (new) and `RESULT.md`
    (dated bracket and flags);
  - `derived/`: 17 files rewritten for the schools case, 3 new (`regression_sept26.csv`,
    `regression_sept26_schools.csv`, `quintiles_vs_base_sept26_schools.csv`), 3 unchanged
    case-neutral files and the 3 stale ones above.
- Not edited: `compliance_gap_2026_09_24/` and `vending_restaurants_2026_09_24/`.

## Reproduce (from the repository root)

```sh
F=infra/immigration-fiscal
# step 1 (default sept26_schools; --case sept24 rebuilds the committed files)
node $F/sept24_propagation_2026_09_24/band_variants.cjs
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $F/sept24_propagation_2026_09_24/real_costs_totals.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $F/sept24_propagation_2026_09_24/constant_choices.py
O=$F/sept26_propagation_2026_09_26/derived/sept26
node $F/sept24_propagation_2026_09_24/band_variants.cjs --case sept26 --out-dir $O
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $F/sept24_propagation_2026_09_24/real_costs_totals.py --case sept26 --out-dir $O
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $F/sept24_propagation_2026_09_24/constant_choices.py --case sept26 --out-dir $O
# step 2: the ledger on the schools case (derived/), then the old -> new table
node $F/winners_losers_2026_09_24/specs.cjs
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $F/winners_losers_2026_09_24/winners_losers.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $F/winners_losers_2026_09_24/old_new.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest $F/winners_losers_2026_09_24/ -q
# the September 24 check: same flags to both scripts, then compare with 8a762fe
node $F/winners_losers_2026_09_24/specs.cjs --case sept24 --out-dir DIR
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $F/winners_losers_2026_09_24/winners_losers.py --case sept24 --out-dir DIR
```

Model self-report: claude-opus-5-5 (Opus 5.5), W4 `ledger`, 2026-09-26 to 27.

## Parent integration (2026-09-27, 00:50)

Step 1 is committed at 4e66adb; the parent's rerun reproduced it on all three cases. For step 2 the
parent reran:
- `specs.cjs` and `winners_losers.py` with `--case sept24` into scratch: 22 of the 23 committed
  files are byte-identical, and `sources_manifest.csv` differs only in the two cells that record
  where the specs were read (same hashes); 443 gates;
- `--case sept26` into scratch: 441 gates;
- the default into scratch (equal to the working tree except the same two manifest cells), then twice
  in place: all 26 files in `derived/` unchanged; 435 gates;
- `old_new.py`: `old_new_ledger.csv` (643 rows) byte for byte;
- `constant_choices.py` on the three cases under the final ledger code: equal to 4e66adb;
- the 15 tests.

Readers: the audit probe (`conceptual_audit_2026_09_25/probe_distribution.py`) imports the ledger
code frozen at beefbba and refuses to run once inputs have changed; the figures pages do not read the
lane. The three September 24 files stay in `derived/`, since the lane RESULT cites them as the
regression evidence; the parent did not delete them.
