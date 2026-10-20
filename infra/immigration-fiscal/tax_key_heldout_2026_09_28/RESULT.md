**Verdict:** On IRS tax year 2023, which no step of the key used, the September 27 case's final income-tax key
misses the AGI-bin distribution of income tax after credits by **23.5pp** of total variation across the memo's 19
bins (replicate SE 1.0). Frozen IRS 2022 shares miss by 2.4pp. The final key does no better than the raw CPS
construction (24.1pp) because CPS AGI stops at $3.1M: CBO's gradient moves top tax into the $1–1.5M bin, where IRS
has 5.3% of the tax and the key 20.4%. With the bins from $1M pooled, the gradient cuts the miss from 18.5pp to
8.4pp (frozen IRS 2.4pp). Below $1M, the key has too much tax at $200k–$1M (+8.4pp) and too little at $50k–$200k
(−3.3pp), where the group's share is higher. Matching IRS therefore **raises** the group's federal income tax:
- by **$3.2bn at the low end and $3.1bn at the high end** (SE 1.3–1.4) when CBO's group shares are kept;
- by $4.5bn and $4.0bn when only the bins are matched.

The case would move from $321.8–387.4bn to **$318.6–384.3bn** (or $317.4–383.4bn). This tests allocation, not a
forecast. It cannot see the group's share inside an AGI bin, which comes from the CPS and, from $1M up, rests on
15 union records.

Lane run by claude-opus-5-5 on 2026-09-28 for parent session immigration-research-1c ([brief](BRIEF.md)).
Nothing was proposed or changed in the case; `ends.cjs` only reruns it with each edit.

## 1. The key and the IRS years it used

The income-tax key comes from three layers:
- **Base.** The account's `federal_liability` key is CPS ASEC 2025 `FEDTAX_BC` (income year 2024) over the
  civilian universe. Under the personal rule it sits on the carrier; under the shared rule it is split equally
  within the SPM unit. The union's share is 0.053348 personal and 0.057399 shared. [DATA:
  `assumption_explorer_2026_09_21/derived/model.json`, `federal_income_tax`, scenario `cbo_collective`;
  reproduced to 1e-9, gate `key_is_the_accounts_federal_liability`.]
  - `FEDTAX_BC` is tax after nonrefundable and before refundable credits
    (`FEDTAX_AC = FEDTAX_BC − ACTC_CRD − EIT_CRED`, `research/immigration-fiscal-account-2024-2026-09-05.md`).
    That is the same concept as IRS's "Income tax after credits", so the comparison is like for like.
- **CBO gradient.** Since September 24 the case gives this key CBO's 2022 income gradient, spec
  `individual_inc_tax=individual_inc_tax_gross|2022`, which replaced audit row 3.
  - Each CBO income group takes CBO's share of the tax, and the union's share inside each group stays the CPS's.
  - This lowers the union's share to 0.047867 personal and 0.051552 shared: −$13.17bn and −$14.05bn before the
    stack factor. [DATA: `external_benchmarks_2026_09_24/derived/cbo_deltas.json`; reproduced to 1e-12, gate
    `cbo_gradient_reproduces_the_adopted_delta`.]
- **Stack factor.** The tax-records stack scales the result by 0.888 or 0.875 (personal) and 0.907 or 0.888
  (shared), for hot-deck and matched-over-pooled respectively.
  - The case's union federal income tax is $101.5bn at the high end (spec 11, personal) and $111.2bn at the low
    end (spec 48, shared), averaged over the two methods.
  - The rerun gate `case_union_tax_is_stack_factor_times_the_cbo_share` checks that the amount equals stack
    factor × national × CBO share, that the ends charge it at response 1, and that the band is $321.8194–387.3701bn.

**IRS years.** No IRS table by AGI enters the key. Its only tax-year input is CBO's *Distribution of Household
Income, 2022*, which rests on tax year 2022 returns. CBO's 2018 and 2019 editions served only as robustness specs.
Two earlier lanes compared the CPS with IRS but changed nothing:
- `admin_tax_checks_2026_09_19`: "No ledger inputs are changed".
- `same_year_tax_2026_09_20`: "No fiscal-ledger parameter is changed". It compared CPS income 2023 with IRS tax
  year 2023, so that year was inspected but never fitted.

## 2. Held-out year and score

**Tax year 2024 is not published.** The evidence [DATA: `_cache/acquisition.json`; quoted in
`reads/soi_availability.md`]:
- SOI's Table 1.2, 1.1 and 1.4 names for tax year 2024 return 404, and so do the preliminary names for 2023 and 2024.
- `22in01pl.xls` exists.
- The tables-by-AGI page links files through tax year 2023.
- The Summer 2026 SOI Bulletin, where SOI printed individual preliminary data in past years, says it "does not
  include a featured article" and points to the complete report.

The held-out year is therefore **tax year 2023**: Table 1.2, Last-Modified 26 Mar 2026, the same file
`same_year_tax_2026_09_20` locked [`reads/irs_table_1_2_ty2023.md`]. The key's income year, 2024, is one year later.

**Construction.** The key's national distribution over IRS's 19 bins weights each CBO group's CPS distribution by
CBO's group share. Each carrier is binned by its tax unit's AGI, exactly as the validation lane binned it (the same
edges; gate `irs_bins_are_the_same_both_years_and_the_memos`). SEs use the 160 CPS replicates, holding the
IRS side fixed. [CALCULATION: `derived/scores.csv`]

| Arm | vs IRS 2023, 19 bins | SE | vs IRS 2023, $1M+ pooled | SE |
|---|---:|---:|---:|---:|
| Final key (CBO gradient), personal | **23.51** | 0.97 | **8.44** | 0.78 |
| Same, shared rule | 23.58 | 0.99 | 8.51 | 0.78 |
| Same, AGI deflated to 2023 dollars by nominal GDP (5.34%) | 22.20 | 0.94 | 8.67 | 0.76 |
| Key before CBO's gradient | 24.10 | 0.73 | 18.47 | 0.86 |
| Frozen IRS 2022 shares (the memo's baseline) | **2.43** | — | 2.38 | — |
| Memo: frozen CPS 2022 / same-year CPS 2023 | 25.20 / 24.06 | — | — | — |

- **The baseline reproduces.** The frozen-IRS figure matches the validation lane's `irs_distribution.csv` to
  1e-9 (2.4303pp). The memo's CPS arms are read from the same file.
- **The final key scores worse against the year CBO's gradient rests on.** Against IRS 2022 it gets 25.43pp
  (19 bins) and 10.31pp (pooled). So the held-out year shows no sign of overfitting. The key was fitted to CBO's
  income groups, not to AGI bins.
- **Most of the 19-bin miss is inside the $1M+ pool.** Pooling removes 15.07pp (23.51 − 8.44).
  - The CPS's largest AGI is $3,124,826, so the key has no tax in the $5–10M and $10M+ bins. IRS puts 14.76% of
    the tax there.
  - The key instead holds 20.40% in the $1–1.5M bin against IRS's 5.33%. [gate
    `cps_agi_top_coding_leaves_the_top_bins_empty`]

**Where the pooled miss lies.** Shares are percentages of national income tax after credits; the union's share and
the records are those behind each bin under the personal rule [CALCULATION: `derived/bins.csv`,
`derived/translation_bins.csv`].

| AGI | IRS 2023 | Final key | Gap (pp) | Union share in bin | Carrier records (union) |
|---|---:|---:|---:|---:|---:|
| Under $50k | 2.82 | 2.71 | +0.11 | 15.4% | 14,224 (2,491) |
| $50k–$75k | 4.59 | 3.95 | +0.64 | 12.0% | 8,916 (1,242) |
| $75k–$100k | 5.42 | 4.43 | +0.99 | 8.9% | 6,316 (710) |
| $100k–$200k | 19.42 | 17.73 | +1.69 | 6.3% | 13,309 (1,021) |
| $200k–$500k | 24.08 | 29.95 | −5.87 | 3.7% | 6,361 (303) |
| $500k–$1M | 12.69 | 15.25 | −2.56 | 2.3% | 652 (19) |
| $1M and up (pooled) | 30.99 | 25.99 | +5.00 | 3.5% | 309 (15) |

The gap is IRS minus key. The $1M+ records split as 276 (15) at $1–1.5M, 15 (0) at $1.5–2M and 18 (0) at $2–5M.

## 3. The dollars

**The linking assumption.** The union's share of tax inside each AGI bin, or inside each CBO-group × AGI-bin cell,
is the CPS's. Only the bins' shares of the national total move to IRS's. The national line ($2,403.242bn) and the
stack factor are held. The union's tax change is stack factor × national × change in share, and each change is
rerun through the adopted case at all 64 specifications by `ends.cjs`. The engine moves the ends by exactly minus
the union's tax change (gate `engine_change_equals_minus_the_union_tax_change`), and the end specs stay 48 and 11.
[CALCULATION: `derived/main_case_change.csv`, `derived/main_case_translation.json`]

The first two columns are the change in the union's federal income tax at each end; SEs use the 160 replicates.

| Reading | Low end (spec 48, shared) | High end (spec 11, personal) | Case band |
|---|---:|---:|---:|
| Adopted | — | — | $321.8–387.4bn |
| **IRS 2023 bins, CBO's group shares kept (raked)** | **+$3.20bn** (SE 1.33) | **+$3.10bn** (SE 1.37) | **$318.6–384.3bn** |
| IRS 2023 bins only, $1M+ pooled | +$4.47bn (1.29) | +$3.95bn (1.25) | $317.4–383.4bn |
| IRS 2023 bins only, $500k+ pooled | +$3.10bn (0.54) | +$3.07bn (0.52) | $318.7–384.3bn |
| IRS 2022 bins only, $1M+ pooled (not held out) | +$5.19bn (1.76) | +$4.67bn (1.70) | $316.6–382.7bn |
| IRS 2023, all 19 bins | +$1.73bn (4.24) | −$3.07bn (1.29) | $320.1–390.4bn |

The rows differ in how they treat the CBO margin and the top bins:
- **Raked.** This row keeps the adopted CBO gradient and adds the IRS margin. Iterative proportional fitting
  matches both margins to 1e-12 (180 iterations personal, 179 shared), holding the union's share inside each
  CBO-group × AGI-bin cell.
- **Bins only.** Matching bins alone breaks CBO's group margin: the top 1% rises from 36.1% to 39.3% of the tax,
  and the 96th–99th percentiles fall from 20.1% to 16.6% (personal) [DATA: `derived/summary.json` → `raking`].
- **All 19 bins.** This row gives the $1.5–5M bins the union share of their 33 records, none of them union, and the
  empty $5M+ bins the pooled share. Its sign turns on that zero, so it is not a usable estimate.

**The same test on the key before CBO's gradient.** Matching IRS 2023 bins alone ($1M+ pooled) would cut the
union's tax by $7.90bn personal (SE 4.53) and $7.98bn shared (SE 4.72), before the stack factor. CBO's gradient
cut it by $13.17bn and $14.05bn [DATA: `derived/summary.json` → `bin_reweighting_of_the_key_before_cbo`].
- The IRS bins confirm the direction of the INDEX's "too flat at the top" finding.
- They support about 60% of its size.
- Starting from the final key, matching IRS gives back $3.5–5.0bn of CBO's cut before the stack factor
  (national × the share changes in `derived/translation_inputs.json`), or $3.1–4.5bn after it.

## 4. Test of allocation, not a forecast

This is an out-of-sample test of **allocation**. It asks whether the key spreads a fixed national tax across AGI
bins the way IRS returns do, in a year the key never saw. It forecasts nothing: no quantity is projected, and the
key's income year (2024) is later than the test year (2023). A TY2024 table would be the matched-year test when
SOI publishes it.

It cannot identify:
- **The union's share inside a bin.** SOI has no nativity or ancestry, so every dollar figure in §3 rests on
  the CPS's within-bin shares. From $1M up those rest on 15 union records.
  - If the CPS understates the union's top incomes, or places the group's filers wrongly within bins, this test
    cannot see it.
  - The next test, which the September 24 decision lists, is IRS tables by state × AGI crossed with the group's
    state composition.
- **Tax above $3.1M.** The CPS has no records there. The pooled readings assume the union's share of tax above
  $5M equals its share from $1M up.
- **The level of the line.** The key only splits NIPA's $2,403bn; an error in the national total is outside the
  test.
- **The status corrections.** The stack factor acts on the union's amount, not on bins, and is held.

## Files

**Read.** All of these are read-only.
- The lane's own sources:
  - `_cache/22in12ms.xls` and `_cache/23in12ms.xls`, fetched by `acquire.py`; their hashes equal
    `same_year_tax_2026_09_20/source_lock.json`.
  - `_cache/acquisition.json`, including the Summer 2026 Bulletin page.
- The CPS and the model:
  - `gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip`, through `external_benchmarks_2026_09_24/frame.py`,
    with its parquet cache redirected into this lane's `_cache/`.
  - `assumption_explorer_2026_09_21/derived/model.json`.
- The benchmark lane:
  - `external_benchmarks_2026_09_24/cbo_arm.py`, for the groups.
  - Its `derived/cbo_components.csv`, `cbo_group_shares.csv`, `cbo_translation.csv` and `cbo_deltas.json`.
- The validation lane: `validation_fiscal_years_2026_09_28/analysis.py` (the bin edges) and
  `derived/irs_distribution.csv`.
- The case: `main_case_long_run_2026_09_27/package.cjs` and `derived/summary.json`.
- NIPA Section 1 (`Section1All_xls.xlsx`, sha256 238ba851…, the vintage `debt_legacy_2026_09_23` pins).
- Context: the INDEX line, the September 24 decision, and both earlier tax lanes' READMEs.

**Skipped.**
- **CBO's researcher zip.** It is not in `external_benchmarks_2026_09_24/_cache/arm1`, so CBO's group shares come
  from that lane's tracked CSV. The reproduction gates tie them to the adopted delta.
- **IRS state × AGI tables and ACS composition.** They are outside this brief (§4).

**Written.** Everything is inside this directory:
- `acquire.py`, `heldout.py` and `ends.cjs`;
- `derived/`: `bins.csv`, `scores.csv`, `translation_bins.csv`, `main_case_change.csv`, `main_case_translation.json`,
  `translation_inputs.json`, `summary.json` and `gates.json` (11 gates);
- `reads/`: the IRS cells for both years and the availability record.

## Live-case reproduction (oct15)

`ends.cjs` defaults to the live oct15 residual. It reads personal end specifications from
`summary.json` `v8.end_specifications`, the `white_end_tax_keys` item from the case's registry, and
the independent receipt-only white-lane measurement in `income_tax_keys_oct15_meta.json`. Its hashes
tie it to the final case, canonical key code, frame, raw inputs and exported CSVs. An applied item must leave a measured
and priced residual of zero at 1e-9, in both the set and the cash set. Totals gate against the case's
full-precision `summary.json` at 1e-9 and its four-decimal `main_case_bands.csv` at 5e-5. The white
lane must run first. `test_keys.py` checks A1's person-level tax shares against that lane's live
`income_tax_keys_oct15.csv` at both allocations. `evaluateFull` carries v8's post-engine mixed-unit
removal and coverage, together with the capital return. The oct15 zero gate stays at 1e-9; the
oct14 printing-tolerance decision below is retained as history and does not loosen that gate.
The A1 comparison CSV uses `meta.population_v8.with_coverage`; item 7's independent movement
keeps its original white-priced count and age mix. The tests check those two declared frames
separately: the live CSV on the full comparison count, the historical shared-share pin on
`meta.lineage.counts.lineage_population`. The export metadata names and hashes both frames.

The original held-out key translation is a frozen input to the candidate-v2 package, which v8
still consumes. Its files, IRS reads and person-key definition remain source measurements;
live propagation does not regenerate them. `heldout.py` explicitly selects the translator's
`--historical-sept27` route when reproducing that historical measurement. The new consumer writes
`main_case_translation_oct15.json` and `main_case_change_oct15.csv` only after all gates pass.

```sh
node infra/immigration-fiscal/tax_key_heldout_2026_09_28/ends.cjs --case oct15
node infra/immigration-fiscal/tax_key_heldout_2026_09_28/test_residual_gate.cjs
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest -p no:cacheprovider infra/immigration-fiscal/tax_key_heldout_2026_09_28/test_keys.py -q
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/tax_key_heldout_2026_09_28 \
  "node {lane}/ends.cjs --case oct15" \
  "node {lane}/test_residual_gate.cjs" \
  "uv run --no-project python3 -m pytest -p no:cacheprovider {lane}/test_keys.py -q" \
  --allow-unrun infra/immigration-fiscal/tax_key_heldout_2026_09_28/ends_oct15.cjs \
  --allow-unrun infra/immigration-fiscal/tax_key_heldout_2026_09_28/heldout.py
```

The module `ends_oct15.cjs` is executed by `ends.cjs`; the allowance declares this indirect caller.
`heldout.py` remains a historical caller and is not regenerated. Historical oct14 outputs stay unchanged.
The isolated `test_residual_gate.cjs` regression uses mock inputs: exact zero must pass,
the inherited six-decimal source remainder must fail at 1e-9 before writing outputs, and
an earlier adopted stamp must fail before writing oct15 outputs. It performs no live I/O.

## Historical reproduction (key measurement; not the live consumer)

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/tax_key_heldout_2026_09_28/acquire.py   # network, once
OPENBLAS_NUM_THREADS=1 uv run --no-project --with xlrd python3 infra/immigration-fiscal/tax_key_heldout_2026_09_28/heldout.py
```

Two consecutive runs of `heldout.py` wrote byte-identical `derived/` and `reads/` (11 files, sha256 compared).

## Log

- Stub written before reading the inputs.
- Task 1 (key and years), from the files: the September 27 case's income-tax key is the account's
  `federal_liability` key, CPS ASEC 2025 `FEDTAX_BC` (income year 2024), personal on the carrier or shared
  equally within the SPM unit [DATA: `assumption_explorer_2026_09_21/derived/model.json`, line
  `federal_income_tax`, scenario `cbo_collective`]. The September 24 package replaces audit row 3 with CBO's
  2022 income gradient (spec `individual_inc_tax=individual_inc_tax_gross|2022`, deltas −13.17 personal and
  −14.05 shared) and scales it by the tax-records stack factor
  [DATA: `external_benchmarks_2026_09_24/derived/cbo_deltas.json`; `main_case_2026_09_24/package.cjs`
  `packageShifts`]. No IRS table by AGI enters the key. The only tax-year input is CBO's *Distribution of
  Household Income, 2022*, which rests on tax year 2022 returns; CBO's 2018 and 2019 editions were robustness
  specs. `admin_tax_checks_2026_09_19` and `same_year_tax_2026_09_20` are uncalibrated checks ("No ledger
  inputs are changed"; "No fiscal-ledger parameter is changed", their READMEs); the second compared CPS income
  2023 with IRS tax year 2023, so that year was inspected but never fitted.
- Task 2 (held-out year): SOI has not published tax year 2024. `24in12ms.xls`/`.xlsx`, `24in11si.xls`,
  `24in14ar.xls` and the preliminary names `23in01pl.xls`/`24in01pl.xls` return 404; `22in01pl.xls` returns 200;
  the tables-by-AGI page links files through tax year 2023 [DATA: `_cache/acquisition.json`, fetched
  2026-09-27T18:50:31Z]. Tax year 2023 (Table 1.2, Last-Modified 26 Mar 2026) is the held-out year: no step of
  the key used it. Its file hash equals `same_year_tax_2026_09_20/source_lock.json`.
- First scoring run: the 19-bin score (23.5pp) barely moves from the raw key's, and the empty bins are 0, 17 and 18.
  I added the pooled $1M+ score, the carrier record counts per bin, a $500k+ pooled translation, and the raked
  translation that keeps CBO's group shares. The raked version became the recommended reading once the bins-only
  step was seen to push the top 1% to 39.3%.
- Refetched at 2026-09-27T19:19:28Z to archive the Summer 2026 Bulletin notice. Both tables' hashes and all
  probe statuses were unchanged.
- Final runs: 11 gates pass, and two consecutive runs are byte-identical.
- Parent's integration rerun (2026-09-28, 04:24 JST) ran `acquire.py` again: both tables' hashes and every probe status were unchanged, so only the check time in `reads/soi_availability.md` (2026-09-27T19:24:51Z) and the `_cache/acquisition.json` hash in `derived/summary.json` moved. `heldout.py` alone then reran byte-identical, 16 of 16 files.
- 2026-10-14 18:39:13 JST — Live consumer and person-key tests moved to oct14 after CASE_FINAL (`148ed1ea`); the frozen historical key measurement remains an input. Five key tests pass for both allocations. Their explicit test-only rerun is IDENTICAL: 19/19, exit 0; it excludes the blocked live residual translator and historical `heldout.py`, so it is not a full-lane pass. Final white receipt-only metadata passes source-hash, W-count (1e-9), applied-item and residual-arithmetic (1e-12) gates. Independently measured W movement is 1.086440193243434bn; the adopted item's six-decimal source supplies 1.08644bn. Both sets' low/high residuals are +1.932434339213529e-7bn (about $193.24), exceeding the required 1e-9bn ($1) zero gate. The live command exits 1 before pricing or writing either oct14 translation output; no full consumer rerun is claimed. **STOP / exact question:** should item 7 consume the full-precision measurement and the parent rebuild the frozen case, or is there an authoritative precision convention reconciling the six-decimal source with this zero-at-1e-9 contract? No tolerance is loosened and no residual rounded to zero. [DATA: `../white_replacement_2026_09_28/derived/income_tax_keys_oct14_meta.json`, `../main_case_2026_10_14/derived/corrections{,_cash}.json`; CALCULATION: scratch `tax-residual-final.log`; pytest and test-only `rerun_lane.py` stdout recorded in the propagation session]

## v7 wave 2: frozen-source representation bound (2026-10-14)

The parent explicitly resolves the prior precision stop: item 7 reads limits_oct07.csv printed to six-decimal bn, frozen in adopted case 148ed1ea. The measured-versus-input check therefore uses 5e-7bn (half a printing unit). Every other residual keeps 1e-9; source hashes/count and arithmetic keep their existing stricter checks. The independent measured remainder is exactly +1.932434339213529e-7bn, about $193.24, at both ends and on both bases; it remains in the JSON and CSV. Neither the source nor frozen case is rebuilt. [DATA: ../white_replacement_2026_09_28/derived/income_tax_keys_oct14_meta.json; CALCULATION: ends_oct14.cjs]

Live commands: node infra/immigration-fiscal/tax_key_heldout_2026_09_28/ends.cjs --case oct14; OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest -p no:cacheprovider infra/immigration-fiscal/tax_key_heldout_2026_09_28/test_keys.py -q. The live full rerun allows ends_oct14.cjs as the module executed by ends.cjs, and heldout.py as the preserved historical caller (compile-checked, not regenerated).

- 2026-10-14 19:11:30 JST — live translation exits 0 with 45 gates; five person-key tests pass. Full live-consumer rerun IDENTICAL 21/21, exit 0. Both full-precision baseline totals reproduce the adopted case at 1e-9; the engine prices the preserved remainder at 1e-9. [CALCULATION: ends.cjs --case oct14; test_keys.py; wave-2 rerun]


## 2026-10-15 Round-2 comparator fixes

The parent resolves the oct15 precision stop: frozen v7 item 7 remains 1.08644bn at six decimals. Only the measured-versus-carried comparison admits 5e-7bn. Engine pricing and the priced remainder beyond that declared rounding stay at 1e-9; the exact measured rounding remainder remains visible in both output sets. `test_residual_gate.cjs` accepts 1.932434339e-7bn, rejects 6e-7bn and a stale case stamp, and checks the unchanged 1e-9 closure metadata. This supersedes the earlier strict-rounding stop; no source bytes change. [SOURCE: parent second resume note; CALCULATION: ends_oct15.cjs, test_residual_gate.cjs]

- 2026-10-15 00:50 JST — isolated residual probe and Node syntax check pass. CASE_FINAL remains absent; no final live output or reproducibility receipt is claimed.


### Adopted v8 receipt, 2026-10-15

Final White export_keys was rebuilt after Black exporter; all source hashes pass. The earlier source-order failure is resolved by regenerated metadata, without editing a stored hash. Live consumer passes46gates and5keytests plus isolated VM controls. Actual measured-minus-carried item7 residual remains+1.932434339213529e-7bn at both ends/bases; only that six-decimal comparison uses5e-7bn. Engine pricing and the remainder beyond the declared rounding close at1e-9bn. Rerun IDENTICAL25/25,exit0,8.808s; child RSS1,498,497,024bytes informational via Python resource. heldout.py is explicitly allow-unrun: preserved historical measurement, not a live producer. ends_oct15.cjs is traced through ends.cjs and needs no indirect-module exemption. [CALCULATION: derived/main_case_translation_oct15.json,main_case_change_oct15.csv; scratch tax-final.json,tax-repro.json]

Log: 2026-10-15 06:19:49 JST (`date`, parent): rerun on corrected v8 (`d1a24d47`: the coverage term no longer charges the missed people's custody, arrests and ICE a second time, −$3.199004 / −$3.221092bn on the lineage), IDENTICAL 25/25, exit 0. The held-out tax key's residual is unchanged (1.932435e-7bn); the baselines it adds to are now $365.791930 / 455.981785bn set, $281.752564 / 371.942418bn cash.

## Live v9 residual (oct16), preparation 2026-10-15

`ends.cjs` defaults to oct16 and calls `ends_oct16.cjs`. It consumes the new independent
White income-tax-key receipt, selected item7 metadata and v9's declared personal ends.
The full evaluator includes the basket, calibration/tenure, military/health and effective
capital-rate changes. Old held-out measurements and oct15 outputs are preserved.
[CALCULATION: ends.cjs; ends_oct16.cjs]

Frozen item7 remains printed to six-decimal bn: only measured-minus-carried admits 5e-7bn.
The exact measured rounding remainder stays visible. Engine pricing and any residual beyond
that declared rounding retain 1e-9bn. This is the existing parent-authorized precision rule,
not a new tolerance or an erased remainder. [SOURCE: above 2026-10-15 precision resolution]

```sh
node infra/immigration-fiscal/tax_key_heldout_2026_09_28/ends.cjs --case oct16
node infra/immigration-fiscal/tax_key_heldout_2026_09_28/test_residual_gate_oct16.cjs
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/tax_key_heldout_2026_09_28 \
  'node {lane}/ends.cjs --case oct16' 'node {lane}/test_residual_gate_oct16.cjs' \
  'uv run --no-project python3 -m pytest -p no:cacheprovider {lane}/test_keys.py -q' \
  --allow-unrun infra/immigration-fiscal/tax_key_heldout_2026_09_28/heldout.py
```

The explicitly excluded historical heldout.py is not regenerated. Initial provisional oct16
probe stops on the not-yet-produced independent White key receipt; final runs wait for that
receipt and CASE_FINAL. [CALCULATION: ends_oct16.cjs provisional stderr]

### Adopted v9 direct receipt — 2026-10-20 20:36 JST

The independent White receipt was regenerated after both key CSV writers. The live
translator passes **51 gates** and exits 0 in 31.633s, including current source hashes,
actual W count, selected item7 subtraction, full-precision and published-band parity,
and the canonical physical-footprint guard (869,706,592 bytes). Set baselines are
368.029739 / 436.561527bn and cash baselines are 284.397043 / 352.928831bn, rounded
once from `sets.*.baseline_bn`. The independently measured item7 remainder is still
**+1.932434339213529e-7bn** at both ends and on both bases; it is not reported as exact
zero. Only measured-minus-carried uses the existing 5e-7bn convention. Engine pricing
and the excess beyond that convention close at 1e-9. [CALCULATION:
`derived/main_case_translation_oct16.json`, `sets.*.measured_residual_bn`, `residual_bn`;
`prop9/d9-tax-final.json` and `.log`]

The adoption guard reads the case package's `STATUS` and `ADOPTED`; it no longer
substitutes the October 16 case date for the October 20 adoption. The isolated fixture
accepts the declared stamp and rejects stale data before writes. Historical heldout.py
and all older keyed outputs are preserved. [CALCULATION: `test_residual_gate_oct16.cjs`]

Final live replay: **IDENTICAL 29/29, exit 0**, 50.320s. All three documented live
commands return 0, including isolated zero/rounding/stale/memory controls and five
person-key tests. `heldout.py` remains the explicitly excluded historical measurement,
not an omitted live producer. [CALCULATION: `prop9/d9-tax-repro.json` and `.log`]

### Refresh after the main case's custody rebuild — 2026-10-21 00:16 JST (`date`)

After the case's custody-only rebuild and White's gate fixes (White's income-tax key bytes unchanged), the three
documented commands rerun, then `rerun_lane.py` (heldout.py allowed unrun, as before): **IDENTICAL 29/29, exit 0**
(23:59:00 JST, 10.4s). `derived/main_case_translation_oct16.json` `sets.*.measured_residual_bn` is still
1.932434339213529e-7bn at both ends of both sets, inside the inherited 5e-7bn rounding exception; it is not a measured
zero. [CALCULATION: rerun_lane.py; derived/main_case_translation_oct16.json]
