**Verdict:** Every computation that still read an old main case now has a run on the adopted September 24 case ($200.9–246.3bn). The debt legacy and distribution lanes switched their defaults. Their old results stay behind `--case sept23`, which reproduces the committed files byte for byte. The uncertainty lane adds `--case sept24` and leaves its September 20 files unchanged. No sign or conclusion changes:

- **Debt legacy.** The 2024 interest falls from $30.5–38.9bn to **$28.3–36.4bn**, because the corrections move cost from federal to state-local budgets. The federal share of the gap falls from 19.0–23.4% to 15.9–21.1%.
- **Real costs.** On the adopted justice footing the total moves from $256–307bn to **$253–304bn**.
- **Distribution.** The fiscal channel moves from $227.9bn to **$225.1bn**.
- **Sampling error.** The per-case SE is **$10.8–10.9bn** and the 95% union is **$180–268bn**. This SE is a floor: most corrections carry their error as ranges, not SEs. [2026-09-28: withdrawn. The joint CPS SE is not a floor: the benefit re-keys are computed on the same 160 replicate weights, and their sampling error moves against the account's (correlation about −0.4), so carrying them jointly gives a smaller SE than appending them as independent. The SE is a partial approximation whose net error is unresolved (audit ffcce20 §A, `research/immigration-conceptual-audit-2026-09-27.md`; the uncertainty lane withdrew the reading in 796f057).]

The lifetime anchors read no main case, so they had nothing to switch. The parent still edits the memos, the ladder, INDEX, the explorer context and one figures-page gate (see "For the parent"). Nothing is committed.

Date: 2026-09-24, finished after midnight (lane worker "propagate"). Status: [CALCULATION] unless marked. Model: claude-opus-5-5[1m] (Opus 5.5, 1M context).

## What still read the September 23 case

`inventory.py` writes `derived/inventory.csv`: 807 rows over 451 files. It searches infra/ and research/ with `rg --no-ignore` for the brief's eight tokens, plus 32 strings computed on the September 23 case. Three live computations read an old case:

- `debt_legacy.py` read September 23;
- `distribute.py` read September 23;
- `propagate.py` read September 20 ($165.1–197.4bn) and carries no Sept 23 token.

The real-costs totals are hand sums in the memo. The other hits fall into three groups:

- correctly dated historical text;
- frame inputs measured on the September 23 frame by design (package.cjs gates each one);
- coincidental numbers.

The main case RESULT lists "the ten-year and lifetime anchors" as not re-run:

- **Ten-year.** This is the back-cast's ten-year total. Its whole-budget rules moved in da2b107 ($1.7–2.4tn). Its programme-by-programme version was never re-run (INDEX line 233). The debt legacy runs that version (its control reproduces the back-cast lane to 5e-5). On the adopted anchor, 2015–2024 comes to **$1.95–2.33tn** ($2.19–2.56tn income-adjusted; was $2.02–2.42tn).
- **Lifetime.** These are the period-profile NPVs of the Sept 19 generation ledger (`ledger_absolute_2026_09_17/lifetime.py`). That object never reads a main case, so there is nothing to switch. It sits behind the fingerprint guard and was not run.

## Debt legacy (ladder 207)

`debt_legacy.py` now defaults to `--case sept24`. It applies `corrections.json` to the model with a port of `engine.js` `applyCorrections`. It then splits every correction into federal and state-local parts by the government level of the line it edits, with the shares the lane already uses for that line. The lane constants take these shares:

- row 8: the federal-grant share of state-local general public services (zero under the low convention);
- row 9: Medicare and Medicaid;
- row 10: other state welfare (BEA 3.12 line 39, where foster care sits);
- small items: the corner's federal share;
- shelter: the shelter lane's mapping-A parts;
- care: by channel (hours taxes at the labour share, elder care at Medicaid's).

`export_package.cjs` rebuilds the package component by component (348 cells). It gates that the components sum to `corrections.json` in every cell.

Gates:

- The corrected model reproduces $200.8752–246.3184bn at every corner, and the uncorrected one $203.2070–249.6400bn (1e-6).
- Federal plus state-local equals every correction (1e-12).
- The corrections' parts add to the change in the whole split (1e-9).
- `--case sept23 --out-dir <dir>` reproduces the 10 committed files byte for byte, and a Sept 24 rerun is byte-identical.

The corrections cut the gap by $2.3–3.3bn but its federal part by $6.6bn. Premium credits (−$14.2bn) and the medical ratios (−$16.8bn) are almost all federal. The tax stack (+$21.2bn) is 81% federal. So less of the gap is borrowed. [CALCULATION: `debt_legacy_2026_09_23/derived/corrections_federal_by_component_2024.csv`, high end, central convention]

`test_debt_legacy.py` makes the `--case sept23` reproduction a permanent gate. It rebuilds the Sept 23 run into a temporary directory and compares every file with the one committed at 96a5c3b (the last commit whose `derived/` held that run). That pin still works after the Sept 24 files are committed. The distribution lane has the same test (`test_distribute.py`, pinned at 5b8957e). Both pass.

### Rows 8 and 10: the two constant splits that differ from the ledger lane

The ledger lane now reads `corrections_federal_split_2024.csv` as the single definition, so these two choices are the ones that carry over. `constant_choices.py` evaluates both lanes' choices on the same Sept 24 split. It then re-runs `debt_legacy.py` with each of the ledger lane's choices in turn (its `constant_parts()` wrapped, nothing edited) to size the effect on the legacy stock. Gate: each re-run moves the 2024 federal part by exactly the direct difference.

- **Row 8** (+$2.0bn, unallocable state-local general public services, audit spending.md #7). This is state-local spending. The only federal money in state-local general government is federal grants, so the federal part is the grant share of state-local general-government spending: federal grants for that function over state-local consumption plus benefits in it, 1.43% in 2024. The low payer convention counts grant-financed spending as state-local, so it gives 0. The ledger lane's 0 applies the low convention's rule to all three conventions.
- **Row 10** (−$1.5bn, foster care and adoption keyed by WIC, audit spending.md #9). The audit re-keys dollars inside BEA Table 3.12 line 39, "Other" state welfare. Its footnote 11 lists WIC food, foster care, adoption assistance and payments to nonprofit welfare institutions. In the model that line is `other_state_welfare`. `family_and_general_assistance` is a different line (TANF and general assistance, keyed by cash assistance) that the audit row does not touch.
  - Both lines carry the lane's state-welfare grant fraction (67.0% under the central and high conventions, 45.0% under the low), so the 2024 split is the same either way.
  - The line matters only for the history that carries the constant back into the stock.
  - [INFERENCE, not measured here] The line's fraction includes WIC food, which is all federal. Foster care's own federal share is probably lower.

| Effect of the ledger lane's choice, minus this lane's, $bn | Row 8 (0 instead of the grant share) | Row 10 (family and general assistance) |
|---|---:|---:|
| Federal part of the 2024 gap, central and high conventions | −0.029 | 0.000 |
| Federal part of the 2024 gap, low convention | 0 | 0.000 |
| Legacy stock entering 2024 (central rule) | −0.37 | +2.03 |
| Legacy interest, 2024 (central rule) | −0.012 | +0.066 |

The effects are the same at both band ends. Neither choice moves the 2024 federal part or the 2024 interest by more than $0.07bn. Row 10's history moves the stock by $2.0bn, 0.2% of it. [CALCULATION: `derived/constant_choices.csv`, `derived/constant_choices_stock.csv`]

## Distribution (ladder 194)

`distribute.py` now defaults to `--case sept24`. It moves A at each band end by the package's change, and P and F do not move. `--case sept23 --out-dir <dir>` reproduces all 12 committed files (212 gates); the Sept 24 run passes 216. Only the fiscal channel and the totals built on it change:

- fiscal cost: $227.9bn → $225.1bn;
- central total: $262.6bn → $259.8bn;
- at η = 1.3, equal-split equivalents: $182bn → $181bn (tax share) and $330bn → $327bn (per person).

The top fifth still bears 62% under tax-share financing. Outside the budget nothing moves: the bottom four fifths lose $80.7bn and the top fifth gains $46.0bn.

## Real-costs totals (memo §7 and §7b)

`band_variants.cjs` evaluates the four fiscal variants the memo pairs with the social rows: raw ethnicity codes, the justice grid's two ends, and 0.7× uncompensated use. It uses the package's own evaluator on both cases, and the Sept 23 variants reproduce its bands file to 1e-4. `real_costs_totals.py` reads every social row from its lane and rebuilds the memo's sums.

Every Sept 23 total the memo prints reproduces. Most match exactly. Three match only as sums of the memo's one-decimal rows: social high 57.8 and 57.2 (57.7 and 57.1 exact) and the scale-net fiscal low 185.2 (185.1 exact). The memo's 2026-09-24 revision note gives "$253–304bn"; the exact figure is $252.7–303.4bn, which rounds to 253–303.

| $bn a year, central values | Sept 23 (memo) | Sept 24 |
|---|---:|---:|
| §7, custody ratio carried over (adopted justice key) | 256–307 | **253–304** |
| §7, Mexican-origin rates = Hispanic, victims $28.9bn (memo definition) | 248–300 | 246–296 |
| §7, same footing, victims $30.9bn (ladder 218; decision 4's figure) | — | 248–298 |
| §7, full span (every low choice, then every high one) | 212–340 | 210–337 |
| §7, full span also stacking the package's own range ($172–276bn) [INFERENCE: may double count the arrest ratio] | — | 182–367 |
| §7b, costs only (Sept 24: care's $4.15bn added back) | 256–307 | 258–308 |
| §7b, with care and mobility | 251–303 | 253–303 |
| §7b, adding the proposed scale net | 237–289 | 239–289 |
| Omitted benefits, without / with the scale net | 4.8 / 18.7 | 0.65 / 14.6 |

On September 24 care sits inside the account, so the only omitted benefits left are mobility and the proposed scale net. The memo's verdict line "$248–307bn … (full span $212–340bn), $6.1–7.5k per member" becomes one of two versions:

- with its victims definition: **$246–304bn** (full span $210–337bn), $6.0–7.4k;
- with decision 4's victims figure: **$248–304bn**, $6.1–7.4k.

Per-member figures are in the table below.

**Disagreements with the sister ledger lane** (`winners_losers_2026_09_24/derived/channels.csv` at run time). Congestion (8.05 / 19.16 / 35.25), unreimbursed care (3.24 / 4.40 / 5.56), property crime (1.27–1.38), mobility (0.65), scale (13.93) and care (4.15) are the same. Five points differ:

| Channel | This lane | winners_losers | Why |
|---|---:|---:|---|
| Victims' harm, custody footing, $bn | 32.34 | 34.58 | The sister scales the mixed-group figure (30.93) by the custody ratio (32.34 / 28.92). The victim lane has not computed that correction on this footing. With 34.58 the custody total is $255.6–306.3bn. |
| Housing net gain, $bn | 0.71–3.51 (both geography arms; span −0.38 to 9.40) | 2.30 / 3.51 / 5.17 | The sister uses the metro-local arm's own low, central and high values. |
| Debt legacy interest, $bn | 28.3–36.4 | 30.5–38.9 | The sister pins the Sept 23 files (git b42efdc). |
| Federal part of the gap, central convention, $bn | 32.0–51.9 | 32.3–52.2 | The sister applies Sept 23 line fractions and approximates the corrections: row 8 at 0, row 10 at family and general assistance, care at the Sept 23 omitted-benefit fraction, schools and colleges at education's fraction. Per the parent, it now reads this lane's per-correction split, so the gap closes on its next run. |
| Channels outside the memo's sums | — | preferences −3.96, school dilution (proposed), consumer prices (side view), debt legacy (beside, decision 4) | Not in the memo's definition. |

[2026-09-25: all four disagreements are resolved on the ledger's final run. The ledger withdrew its $34.58bn victims hybrid (parent's ruling 1; it was never a lane arm) and now allocates decision 4's $30.93bn, with $28.92bn and $32.34bn as variants. It takes ladder 190's housing values, and it reads the September 24 debt split and interest at 7ec7144. The published pairing stays $248–304bn: equal footing $247.7–298.4bn, custody footing $253.4–304.0bn (`winners_losers_2026_09_24/derived/channels.csv`). The `custody_mixed_scaled` rows in `derived/real_costs_totals.csv` are kept as computed and are quoted nowhere.]

## Sampling uncertainty (ladder 184)

`sept24_specs.cjs` costs the 64 main specifications on both cases with the engine. `propagate.py --case sept24` then carries the lane's sources through them (CPS replicate keys, MEPS donor covariance, the school correction and the production term).

The September 23 frame is each September 20 case plus three changes: general government at 0.59 or 0.84 on the per-head key, and the justice and uninsured-use key shifts. Every specification rebuilds this way to 1e-6. On the Sept 23 frame the CPS, MEPS and school errors of the Sept 20 cases reproduce to 1e-9. On September 24, each line's CPS replicate deviation and each MEPS payer gradient is scaled by the group's corrected over uncorrected target on the key the lane rebuilt. The Sept 20 outputs stay byte-identical, and the lane's 10 tests pass.

| | Sept 20 (published) | Sept 23 case | Sept 24 case |
|---|---:|---:|---:|
| Per-case SE, sources independent, $bn | 12.2 | 12.2–12.3 | **10.8–10.9** |
| 95% intervals of the band's cases, union, $bn | 141–221 | 179–274 | **180–268** |
| Correlated upper bound, union, $bn | 127–235 | 165–288 | 166–280 |

The SE falls because the corrections lower the group's dollars on the CPS- and MEPS-keyed lines, and first-order scaling shrinks their errors with them. The corrections' own sampling errors are not in this SE. The one exception is the benefit keys' published SE (1.15/1.17bn), which gives $10.9–11.0bn. The rest (CBO tables, pooled MEPS ratios, the tax stack's hot deck) sit in the package's $172–276bn range. Read $10.9bn as a floor. [2026-09-28: not a floor; see the bracket in the verdict (audit ffcce20 §A, 796f057).]

## For the parent

Lines that carry numbers computed on the Sept 23 case (new values in the table below):

- `research/immigration-real-fiscal-and-social-costs-2026-09-23.md`: lines 30–35, 220 (262.6), 287–290, 326–329 and 379.
- `research/immigration-confidence-ladder.md`:
  - 299 (141–221);
  - 317 (4,969–6,104, 228–287);
  - 319 (262.6);
  - 321 (248–307, 212–340);
  - 333 (189.3–235.7, now 186.9–232.4);
  - 345 and 369 (debt legacy);
  - 431.
- `research/immigration-INDEX.md`:
  - 76;
  - 105;
  - 123;
  - 127–130;
  - 154–155;
  - 233 (the programme version is now computed; see above).
- `assumption_explorer_2026_09_21/context.json`: lines 601 and 2483.
- Figures page:
  - `build_data.cjs` gate "fiscal cost total −227.9" fails on the next build; the value is now −225.10;
  - `src/lib/WhoPays.svelte:83` text "$227.9bn".
- Stale or undated labels:
  - `research/immigration-outside-checks-2026-09-24.md` lines 54, 137 and 190;
  - `research/immigration-status-benefits-sweep-2026-09-24.md` line 82 (shelter "proposed, not adopted").
- `cps_imputation_keys_2026_09_23/distribution_check.py` adds the fill-in correction to the distribution lane's committed total. Re-run on the new files, it would count that correction twice. If it is re-run, read the Sept 23 file from git.
- The lane texts of the debt legacy, distribution and uncertainty lanes still describe their old case.

## Files and reruns

Run order from the repository root; every step exits nonzero on a failed gate:

```
node infra/immigration-fiscal/sept24_propagation_2026_09_24/export_package.cjs
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/debt_legacy_2026_09_23/debt_legacy.py --case sept24 --out-dir DIR
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/distribution_weights_2026_09_23/distribute.py --case sept24 --out-dir DIR
node infra/immigration-fiscal/uncertainty_propagation_2026_09_22/sept24_specs.cjs
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/uncertainty_propagation_2026_09_22/propagate.py --case sept24
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/uncertainty_propagation_2026_09_22/audit.py
node infra/immigration-fiscal/sept24_propagation_2026_09_24/band_variants.cjs --case sept24
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/sept24_propagation_2026_09_24/real_costs_totals.py --case sept24
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/sept24_propagation_2026_09_24/inventory.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/sept24_propagation_2026_09_24/old_new.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/sept24_propagation_2026_09_24/constant_choices.py --case sept24
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest infra/immigration-fiscal/debt_legacy_2026_09_23/ infra/immigration-fiscal/distribution_weights_2026_09_23/ -q --import-mode=importlib
```

The old results come back with `debt_legacy.py --case sept23 --out-dir DIR` and `distribute.py --case sept23 --out-dir DIR`. The two tests keep that reproduction pinned to the committed Sept 23 files (2 passed, 59 s). `propagate.py` without `--case sept24` still writes only the Sept 20 files. [2026-09-26, later: the scripts now default to the schools case, `sept26_schools`, so the block above names `--case sept24`. `band_variants.cjs`, `real_costs_totals.py` and `constant_choices.py` then rewrite this lane's committed files in place. `debt_legacy.py` and `distribute.py` write to their own `derived/` for any case, so their Sept 24 run goes to `--out-dir DIR` and is compared with `git show ed1b623:` and `6e554a3:`. `propagate.py` without `--case` now runs the schools case; `--case sept20` writes only the Sept 20 files. `inventory.py` and `old_new.py` searched and compared the repository as it stood on 2026-09-24; they record that run and do not reproduce it today.] [2026-09-28: `band_variants.cjs`, `real_costs_totals.py` and `constant_choices.py` now default to the September 27 case, `sept27`, and write to `../sept27_propagation_2026_09_27/derived/`. `--case sept26_schools` rewrites 4e66adb's files in `../sept26_propagation_2026_09_26/derived/` byte for byte; `--case sept24` and `--case sept26 --out-dir ../sept26_propagation_2026_09_26/derived/sept26` do the same for theirs. Old → new: `../sept27_propagation_2026_09_27/RESULT_ledger.md`.]

Uncommitted changes:

- **Debt legacy:** `debt_legacy.py`, new `test_debt_legacy.py`; its `derived/` has 8 files modified and 2 new (`corrections_federal_split_2024.csv`, `corrections_federal_by_component_2024.csv`).
- **Distribution:** `distribute.py`, new `test_distribute.py`; 7 files modified in its `derived/`.
- **Uncertainty:** `propagate.py`, new `sept24_specs.cjs`, and new `derived/sept24/` (`spec_costs.csv`, `line_targets.csv`, `case_uncertainty.csv`, `summary.json`).
- **This lane:**
  - scripts: `inventory.py`, `export_package.cjs`, `band_variants.cjs`, `real_costs_totals.py`, `old_new.py`, `constant_choices.py`;
  - `derived/`: `inventory.csv`, `package_components.json`, `band_variants.csv` and `.json`, `real_costs_totals.csv` and `.json`, `old_new.csv`, `constant_choices.csv`, `constant_choices_stock.csv`.

None of these paths is ignored. No memo, FAQ, INDEX, ladder, `engine.js`, `package.cjs`, `main_case.cjs` or fingerprint hash was edited.

## Old → new (generated by `old_new.py` from the files named; `derived/old_new.csv`)

Old values are the committed files (git HEAD). For the real-costs rows they are this lane's exact September 23 sums; for uncertainty they are the September 20 published band unless the row says otherwise. Negative values in the distribution rows are costs.

**main case (reference)**

| Quantity | Unit | Old | New | File |
|---|---|---:|---:|---|
| fiscal main case | $bn | 203.2 to 249.6 | 200.9 to 246.3 | `main_case_2026_09_24/derived/summary.json` |
| fiscal main case per group member | $ | 4,969 to 6,104 | 4,912 to 6,023 | `main_case_2026_09_24/derived/summary.json` |

**debt legacy**

| Quantity | Unit | Old | New | File |
|---|---|---:|---:|---|
| federal part of the 2024 fiscal gap, central convention | $bn | 38.6 to 58.4 | 32.0 to 51.9 | `debt_legacy_2026_09_23/derived/federal_split_2024.csv` |
| federal share of the 2024 gap, central convention | % | 19.0 to 23.4 | 15.9 to 21.1 | `debt_legacy_2026_09_23/derived/federal_split_2024.csv` |
| federal share of the 2024 gap, low convention | % | 8.14 to 14.29 | 5.08 to 11.97 | `debt_legacy_2026_09_23/derived/federal_split_2024.csv` |
| federal share of the 2024 gap, high convention | % | 23.9 to 29.0 | 21.2 to 27.0 | `debt_legacy_2026_09_23/derived/federal_split_2024.csv` |
| legacy stock entering 2024 (central rule) | $bn | 942.6 to 1,202.1 | 876.5 to 1,126.8 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| stock, share of debt at end FY2023 (central rule) | % | 3.59 to 4.58 | 3.34 to 4.29 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| legacy interest, 2024 (central rule) | $bn | 30.5 to 38.9 | 28.3 to 36.4 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| interest per group member (central rule) | $ | 745 to 950 | 693 to 891 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| interest per other resident (central rule) | $ | 102 to 130 | 95 to 122 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| interest, share of FY2024 net interest (central rule) | % | 3.46 to 4.42 | 3.22 to 4.14 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| interest over the account's interest row allocation (central rule) | ratio | 0.23 to 0.29 | 0.22 to 0.28 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| legacy interest across back-cast rules, central convention | $bn | 7.66 to 42.82 | 6.28 to 37.25 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| legacy stock across back-cast rules, central convention | $tn | 0.24 to 1.32 | 0.19 to 1.15 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| legacy interest across rules and payer conventions | $bn | -1.94 to 48.23 | -3.15 to 42.88 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| legacy interest, every specification | $bn | -2.68 to 64.70 | -4.28 to 57.54 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| legacy interest, central rule, every specification | $bn | 6.36 to 59.43 | 5.98 to 56.45 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| legacy interest, low payer convention | $bn | 20.8 to 28.9 | 18.8 to 26.7 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| legacy interest, high payer convention | $bn | 34.2 to 44.3 | 32.4 to 42.1 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| legacy interest, constant 3.22% rate | $bn | 33.0 to 42.1 | 30.6 to 39.4 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| legacy interest, 10-year Treasury rate | $bn | 40.9 to 52.2 | 38.0 to 48.9 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| legacy interest, public securities rate | $bn | 33.5 to 42.7 | 31.1 to 40.1 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| legacy interest, window from 2010 | $bn | 27.8 to 34.3 | 25.8 to 32.1 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| legacy interest, window from 2015 | $bn | 17.6 to 22.2 | 16.8 to 21.2 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| legacy interest, half borrowed | $bn | 15.2 to 19.4 | 14.2 to 18.2 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| legacy interest, proportional benchmark | $bn | 41.1 to 49.1 | 38.5 to 46.2 | `debt_legacy_2026_09_23/derived/stocks.csv` |
| omitted benefits care_and_mobility -> mobility: federal 2024 | $bn | 3.33 | 0.03 | `debt_legacy_2026_09_23/derived/benefit_sensitivity.csv` |
| omitted benefits care_and_mobility -> mobility: stock reduction | $bn | 51.8 | 0.39 | `debt_legacy_2026_09_23/derived/benefit_sensitivity.csv` |
| omitted benefits care_and_mobility -> mobility: interest reduction 2024 | $bn | 1.67 | 0.01 | `debt_legacy_2026_09_23/derived/benefit_sensitivity.csv` |
| omitted benefits care_mobility_and_scale -> mobility_and_scale: federal 2024 | $bn | 8.60 | 5.29 | `debt_legacy_2026_09_23/derived/benefit_sensitivity.csv` |
| omitted benefits care_mobility_and_scale -> mobility_and_scale: stock reduction | $bn | 133.7 | 82.3 | `debt_legacy_2026_09_23/derived/benefit_sensitivity.csv` |
| omitted benefits care_mobility_and_scale -> mobility_and_scale: interest reduction 2024 | $bn | 4.32 | 2.66 | `debt_legacy_2026_09_23/derived/benefit_sensitivity.csv` |
| forward federal debt from the 2024 gap, 10 years | $bn | 447.5 to 676.9 | 370.4 to 600.6 | `debt_legacy_2026_09_23/derived/forward_path.csv` |
| forward federal debt from the 2024 gap, 20 years | $bn | 1,062 to 1,606 | 878.9 to 1,425.2 | `debt_legacy_2026_09_23/derived/forward_path.csv` |
| forward federal debt from the 2024 gap, 30 years | $bn | 1,906 to 2,882 | 1,577 to 2,557 | `debt_legacy_2026_09_23/derived/forward_path.csv` |
| forward debt if the whole gap were borrowed, 10 years | $tn | 2.35 to 2.89 | 2.32 to 2.85 | `debt_legacy_2026_09_23/derived/forward_path.csv` |
| back-cast net cost, programme, 2015-2024 | $tn | 2.02 to 2.42 | 1.95 to 2.33 | `debt_legacy_2026_09_23/derived/adopted_backcast_windows.csv` |
| back-cast net cost, programme, 2010-2024 | $tn | 2.82 to 3.39 | 2.75 to 3.30 | `debt_legacy_2026_09_23/derived/adopted_backcast_windows.csv` |
| back-cast net cost, programme, 2005-2024 | $tn | 3.31 to 4.04 | 3.27 to 3.97 | `debt_legacy_2026_09_23/derived/adopted_backcast_windows.csv` |
| back-cast net cost, programme_income, 2015-2024 | $tn | 2.29 to 2.68 | 2.19 to 2.56 | `debt_legacy_2026_09_23/derived/adopted_backcast_windows.csv` |
| back-cast net cost, programme_income, 2010-2024 | $tn | 3.34 to 3.89 | 3.21 to 3.74 | `debt_legacy_2026_09_23/derived/adopted_backcast_windows.csv` |
| back-cast net cost, programme_income, 2005-2024 | $tn | 4.04 to 4.73 | 3.92 to 4.58 | `debt_legacy_2026_09_23/derived/adopted_backcast_windows.csv` |

**distribution (ladder 194)**

| Quantity | Unit | Old | New | File |
|---|---|---:|---:|---|
| fiscal cost channel, A_mid + F_c (negative = cost) | $bn | -227.9 | -225.1 | `distribution_weights_2026_09_23/derived/channel_by_quintile.csv` |
| fiscal cost, tax-share financing, fifth 1 | $bn | -6.91 | -6.83 | `distribution_weights_2026_09_23/derived/channel_by_quintile.csv` |
| fiscal cost, tax-share financing, fifth 2 | $bn | -14.6 | -14.4 | `distribution_weights_2026_09_23/derived/channel_by_quintile.csv` |
| fiscal cost, tax-share financing, fifth 3 | $bn | -24.6 | -24.3 | `distribution_weights_2026_09_23/derived/channel_by_quintile.csv` |
| fiscal cost, tax-share financing, fifth 4 | $bn | -40.3 | -39.8 | `distribution_weights_2026_09_23/derived/channel_by_quintile.csv` |
| fiscal cost, tax-share financing, fifth 5 | $bn | -141.6 | -139.8 | `distribution_weights_2026_09_23/derived/channel_by_quintile.csv` |
| fiscal cost, per-person cuts, each fifth | $bn | -45.6 | -45.0 | `distribution_weights_2026_09_23/derived/channel_by_quintile.csv` |
| fiscal cost, top fifth's part under tax-share financing | % | 62.1 | 62.1 | `distribution_weights_2026_09_23/derived/channel_by_quintile.csv` |
| fiscal cost under per-person cuts, share of resources, bottom and top fifth | % | -8.03 to -0.85 | -7.93 to -0.84 | `distribution_weights_2026_09_23/derived/channel_by_quintile.csv` |
| central total with the social items (TOTAL) | $bn | -262.6 | -259.8 | `distribution_weights_2026_09_23/derived/channel_by_quintile.csv` |
| central total, share of resources, bottom and top fifth, tax-share | % | -5.24 to -1.78 | -5.23 to -1.75 | `distribution_weights_2026_09_23/derived/channel_by_quintile.csv` |
| central total, share of resources, bottom and top fifth, per-person | % | -12.1 to 0.0 | -12.0 to 0.0 | `distribution_weights_2026_09_23/derived/channel_by_quintile.csv` |
| central total at eta 1.3, equal-split equivalent, tax-share | $bn | -181.9 | -180.9 | `distribution_weights_2026_09_23/derived/weighted_totals.csv` |
| central total at eta 1.3, mean-normalized, tax-share | $bn | -407.1 | -404.9 | `distribution_weights_2026_09_23/derived/weighted_totals.csv` |
| central total at eta 1.3, equal-split equivalent, per-person | $bn | -329.9 | -327.1 | `distribution_weights_2026_09_23/derived/weighted_totals.csv` |
| central total at eta 1.3, mean-normalized, per-person | $bn | -738.3 | -732.0 | `distribution_weights_2026_09_23/derived/weighted_totals.csv` |
| outside the budget: bottom four fifths, top fifth (unchanged) | $bn | -80.7 to 46.0 | -80.7 to 46.0 | `distribution_weights_2026_09_23/derived/channel_by_quintile.csv` |

**real-costs totals (memo §7, §7b)**

| Quantity | Unit | Old | New | File |
|---|---|---:|---:|---|
| §7 hispanic: fiscal main case | $bn | 198.9 to 245.4 | 196.6 to 242.0 | `sept24_propagation_2026_09_24/derived/real_costs_totals.csv` |
| §7 hispanic: total at central values | $bn | 248.0 to 299.7 | 245.7 to 296.4 | `sept24_propagation_2026_09_24/derived/real_costs_totals.csv` |
| §7 hispanic: per group member | $k | 6.06 to 7.33 | 6.01 to 7.25 | `sept24_propagation_2026_09_24/derived/real_costs_totals.csv` |
| §7 hispanic: victims' harm, full cost | $bn | 28.9 | 28.9 | `sept24_propagation_2026_09_24/derived/real_costs_totals.csv` |
| §7 custody: fiscal main case | $bn | 203.2 to 249.6 | 200.9 to 246.3 | `sept24_propagation_2026_09_24/derived/real_costs_totals.csv` |
| §7 custody: total at central values | $bn | 255.7 to 307.4 | 253.4 to 304.0 | `sept24_propagation_2026_09_24/derived/real_costs_totals.csv` |
| §7 custody: per group member | $k | 6.25 to 7.52 | 6.20 to 7.43 | `sept24_propagation_2026_09_24/derived/real_costs_totals.csv` |
| §7 custody: victims' harm, full cost | $bn | 32.3 | 32.3 | `sept24_propagation_2026_09_24/derived/real_costs_totals.csv` |
| §7 hispanic_mixed_group: total at central values | $bn | — | 247.7 to 298.4 | `sept24_propagation_2026_09_24/derived/real_costs_totals.csv` |
| §7 hispanic_mixed_group: per group member | $k | — | 6.06 to 7.30 | `sept24_propagation_2026_09_24/derived/real_costs_totals.csv` |
| §7 custody_mixed_scaled: total at central values | $bn | — | 255.6 to 306.3 | `sept24_propagation_2026_09_24/derived/real_costs_totals.csv` |
| §7 full_span: low end | $bn | 212.5 | 210.2 | `sept24_propagation_2026_09_24/derived/real_costs_totals.csv` |
| §7 full_span: high end | $bn | 340.2 | 336.9 | `sept24_propagation_2026_09_24/derived/real_costs_totals.csv` |
| §7 full_span: per group member, low | $k | 5.20 | 5.14 | `sept24_propagation_2026_09_24/derived/real_costs_totals.csv` |
| §7 full_span: per group member, high | $k | 8.32 | 8.24 | `sept24_propagation_2026_09_24/derived/real_costs_totals.csv` |
| §7 full_span_with_package_range: low end | $bn | — | 181.5 | `sept24_propagation_2026_09_24/derived/real_costs_totals.csv` |
| §7 full_span_with_package_range: high end | $bn | — | 366.8 | `sept24_propagation_2026_09_24/derived/real_costs_totals.csv` |
| §7b costs_only: fiscal main case | $bn | 203.2 to 249.6 | 205.0 to 250.5 | `sept24_propagation_2026_09_24/derived/real_costs_totals.csv` |
| §7b costs_only: social items beside the account | $bn | 52.5 to 57.7 | 52.5 to 57.7 | `sept24_propagation_2026_09_24/derived/real_costs_totals.csv` |
| §7b costs_only: total at central values | $bn | 255.7 to 307.4 | 257.5 to 308.2 | `sept24_propagation_2026_09_24/derived/real_costs_totals.csv` |
| §7b costs_only: per group member | $k | 6.25 to 7.52 | 6.30 to 7.54 | `sept24_propagation_2026_09_24/derived/real_costs_totals.csv` |
| §7b with_care_and_mobility: fiscal main case | $bn | 199.1 to 245.5 | 200.9 to 246.3 | `sept24_propagation_2026_09_24/derived/real_costs_totals.csv` |
| §7b with_care_and_mobility: social items beside the account | $bn | 51.9 to 57.1 | 51.9 to 57.1 | `sept24_propagation_2026_09_24/derived/real_costs_totals.csv` |
| §7b with_care_and_mobility: total at central values | $bn | 250.9 to 302.6 | 252.7 to 303.4 | `sept24_propagation_2026_09_24/derived/real_costs_totals.csv` |
| §7b with_care_and_mobility: per group member | $k | 6.14 to 7.40 | 6.18 to 7.42 | `sept24_propagation_2026_09_24/derived/real_costs_totals.csv` |
| §7b adding_scale_net: fiscal main case | $bn | 185.1 to 231.6 | 186.9 to 232.4 | `sept24_propagation_2026_09_24/derived/real_costs_totals.csv` |
| §7b adding_scale_net: social items beside the account | $bn | 51.9 to 57.1 | 51.9 to 57.1 | `sept24_propagation_2026_09_24/derived/real_costs_totals.csv` |
| §7b adding_scale_net: total at central values | $bn | 237.0 to 288.6 | 238.8 to 289.5 | `sept24_propagation_2026_09_24/derived/real_costs_totals.csv` |
| §7b adding_scale_net: per group member | $k | 5.79 to 7.06 | 5.84 to 7.08 | `sept24_propagation_2026_09_24/derived/real_costs_totals.csv` |
| §7b omitted_benefits: without the scale net | $bn | 4.80 | 0.65 | `sept24_propagation_2026_09_24/derived/real_costs_totals.csv` |
| §7b omitted_benefits: with the scale net | $bn | 18.7 | 14.6 | `sept24_propagation_2026_09_24/derived/real_costs_totals.csv` |
| §7b omitted_benefits: share of main case, low (%) | % | 1.92 | 0.27 | `sept24_propagation_2026_09_24/derived/real_costs_totals.csv` |
| §7b omitted_benefits: share of main case, high (%) | % | 9.22 | 7.26 | `sept24_propagation_2026_09_24/derived/real_costs_totals.csv` |
| §revision_2026_09_24 with_care_and_mobility: total, low | $bn | — | 252.7 | `sept24_propagation_2026_09_24/derived/real_costs_totals.csv` |
| §revision_2026_09_24 with_care_and_mobility: total, high | $bn | — | 303.4 | `sept24_propagation_2026_09_24/derived/real_costs_totals.csv` |

**uncertainty (ladder 184)**

| Quantity | Unit | Old | New | File |
|---|---|---:|---:|---|
| per-case SE, sources independent | $bn | 12.16 to 12.22 | 10.8 to 10.9 | `uncertainty_propagation_2026_09_22/derived/sept24/summary.json` |
| per-case SE, all positively correlated | $bn | 19.1 to 19.7 | 17.2 to 17.8 | `uncertainty_propagation_2026_09_22/derived/sept24/summary.json` |
| 95% intervals of the main band's cases, union | $bn | 141.2 to 221.3 | 179.5 to 267.6 | `uncertainty_propagation_2026_09_22/derived/sept24/summary.json` |
| 95% intervals at the correlated upper bound, union | $bn | 127.0 to 235.3 | 166.4 to 280.4 | `uncertainty_propagation_2026_09_22/derived/sept24/summary.json` |
| 95% intervals with the benefit keys' SE, union | $bn | — | 179.4 to 267.7 | `uncertainty_propagation_2026_09_22/derived/sept24/summary.json` |
| per-case SE on the Sept 23 case (never published) -> Sept 24 | $bn | 12.2 to 12.3 | 10.8 to 10.9 | `uncertainty_propagation_2026_09_22/derived/sept24/summary.json` |
| 95% union on the Sept 23 case (never published) -> Sept 24 | $bn | 179.3 to 273.6 | 179.5 to 267.6 | `uncertainty_propagation_2026_09_22/derived/sept24/summary.json` |


## Progress log (appended as confirmed)

- 2026-09-24 23:2x. Regression gate, debt legacy: `debt_legacy.py` on the September 23 input
  exits 0 and reproduces all 10 tracked `derived/` files byte for byte. [CALCULATION]
- Regression gate, uncertainty propagation: `propagate.py` then `audit.py` exit 0 and reproduce all
  15 tracked `derived/` files byte for byte. Its input is the September 20 case ($165.1–197.4bn),
  not September 23. [CALCULATION]
- Regression gate, distribution lane (ladder 194): `distribute.py` exits 0 (212 gates) and
  reproduces all 12 tracked `derived/` files byte for byte. [CALCULATION]
- Inventory written: `inventory.py` → `derived/inventory.csv` (primary token search, a search
  for numbers derived from the September 23 case, and explicit rows for the three items no token
  reaches). Live computations that read an old case: `debt_legacy.py` (Sept 23),
  `distribute.py` (Sept 23), `propagate.py` (Sept 20). The real-costs totals are hand sums in the
  memo. The lifetime anchors are the Sept 19 generation ledger's NPVs and read no main case.
- Debt legacy re-run on the adopted case (`debt_legacy.py`, default `--case sept24`; `--case sept23
  --out-dir <dir>` reproduces the 10 committed files byte for byte). Gates pass: the corrected
  model on the frame reproduces $200.8752–246.3184bn and the uncorrected one $203.2070–249.6400bn
  (1e-6, all three profiles); every correction's federal plus state-local part equals it; the
  corrections' parts add to the change in the whole split at each corner (1e-9). Central: stock
  $877–1,127bn (was $943–1,202bn), 2024 interest **$28.3–36.4bn** (was $30.5–38.9bn), federal share
  of the 2024 gap 15.9–21.1% (was 19.0–23.4%). Rerun is byte-identical. [CALCULATION]
- Real-costs totals (`band_variants.cjs` then `real_costs_totals.py`). The four fiscal variants the
  memo pairs with the social rows (raw ethnicity codes, justice grid ends, 0.7x uncompensated use)
  reproduce the Sept 23 bands file to 1e-4 on the uncorrected model, then run on the corrected one
  (raw coding $196.6–242.0bn, grid low with 0.7x use $192.4bn, grid high $249.0bn). Every Sept 23
  total the memo prints reproduces: most exactly, three only as sums of its one-decimal rows
  (social high 57.8 and 57.2, scale fiscal low 185.2; exact 57.7, 57.1, 185.1). Custody footing
  $255.7–307.4bn → **$253.4–304.0bn**; Hispanic footing $248.0–299.7bn → $245.7–296.4bn; full span
  $212.5–340.3bn → $210.2–336.9bn. §7b with care and mobility $250.9–302.6bn → $252.7–303.4bn;
  costs only (care added back) → $257.5–308.2bn; omitted benefits $4.8bn → $0.65bn. [CALCULATION]
- Distribution lane (ladder 194) re-run on the adopted case: `distribute.py` now defaults to
  `--case sept24`, and `--case sept23 --out-dir <dir>` reproduces all 12 committed files byte for byte
  (212 gates). The Sept 24 run passes 216 gates and moves A by the package's change at each band end.
  Only the fiscal channel and totals move: fiscal cost $227.9bn → **$225.1bn** (top fifth still 62%
  under tax-share financing; 8.0% → 7.9% of the bottom fifth's resources under per-person cuts);
  central total $262.6bn → $259.8bn; at η = 1.3 its equal-split equivalents are $182bn → $181bn
  (tax share) and $330bn → $327bn (per person). Outside the budget is unchanged (−$80.7bn / +$46.0bn).
  The figures page's gate "fiscal cost total −227.9" (`figures_2026_09_22/build_data.cjs`) will fail
  on its next build until the parent updates it. [CALCULATION]
- Uncertainty propagation (ladder 184) carried to the adopted cases: `node sept24_specs.cjs` then
  `propagate.py --case sept24` (Sept 20 outputs unchanged: all 15 tracked files byte-identical after
  `propagate.py` and `audit.py`; 10 tests pass). Positive controls: on the Sept 23 frame every
  specification rebuilds from its Sept 20 case to 1e-6, and the CPS, MEPS and school errors of the
  Sept 20 cases reproduce to 1e-9. Per-case SE: Sept 23 case $12.2–12.3bn, 95% union $179.3–273.6bn;
  Sept 24 case **$10.8–10.9bn**, 95% union **$179.5–267.6bn** (envelope $166.4–280.4bn). The drop is
  mechanical: first-order ratio scaling shrinks the CPS and MEPS errors where the corrections lower the
  group's dollars. The corrections' own sampling errors are not in this SE except the benefit keys'
  (1.15/1.17bn, giving $10.9–11.0bn); the rest sit in the package's $172–276bn range. [CALCULATION]
- 2026-09-25 (after the parent's follow-up). The two constant splits that differ from the ledger
  lane are documented with their federal-dollar effect (`constant_choices.py`). Row 8 at 0 would move
  the 2024 federal part by −$0.029bn and the stock by −$0.37bn. Row 10 on family and general
  assistance leaves the 2024 split unchanged and moves the stock by +$2.03bn. The re-run gate
  confirms each 2024 difference. The `--case sept23` reproduction is now a permanent test in the
  debt legacy lane (pinned at 96a5c3b) and the distribution lane (pinned at 5b8957e); both pass.
  [CALCULATION]

## v4 case (sept29), 2026-09-29

**Verdict.** On the main case adopted 2026-09-29 (candidate v4, `../main_case_2026_09_29/`, $371.41–434.84bn), the
fiscal-plus-social pairing on the 39,712,493 people the account prices is **$462.95–535.52bn a year**, or
**$11,657–13,485 per member**. On the September 27 case it was $413.74–488.05bn and $10,419–12,290. The low end
prices offending at the Hispanic average: the case run with justice keyed on the raw census codes, $366.68bn, plus the
social rows at the low end. The high end is the custody footing: the case's $434.84bn plus the social rows at the high
end. The social rows are the population lane's restatement on the priced count, $96.26bn and $100.68bn, unchanged from
September 27. Beside it, never in it, the cash set (the pension switch off) pairs to $386.23–462.49bn
($9,726–11,646). [CALCULATION: `band_variants.cjs` → `real_costs_totals.py` → `derived/sept29/real_costs_totals.csv`,
column `pairing_on_priced_count`]

### What changed, and where the outputs go

The three scripts take `--case sept29` and write to `derived/sept29/` in this lane. Their September 27 runs write
into `../sept27_propagation_2026_09_27/derived/`, a lane this task did not own, so the new case sits here, one
constant per script (`CASES`, `OUT_DIRS`). Every default and every earlier case is unchanged.

- **`band_variants.cjs`.**
  - A specification's `line_responses` are rebuilt from every entry of `meta.responses`: 13 on September 29 (the
    September 27 four, four more receipt overrides and five correction lines). An entry with a reading that names no
    line stops the run. The rebuild equals the package's `MAIN_SPECS` (gate).
  - **Designed rule: state prices follow the justice key.** v4 prices public order and safety at the states' price
    level with a correction line, `state_price_public_order_safety`. Its group amount is national_gap_bn × the parent's
    key share "on its evaluated key" (`meta.state_pricing.rule`): $47.79bn × 69.655 / 519.153 = $6.412bn on the
    case's use key. A justice variant evaluates the parent on another key (raw coding) or moves its use key (the grid
    ends, CBP held fixed). The script therefore re-prices that line on the variant's key. Raw coding lowers the key share
    by 6.1% (65.382 / 69.655), so the line falls $0.393bn at every specification.
    - Justification: the gap is a price applied to the group's quantity of justice services. The Hispanic footing says
      that quantity is the Hispanic average, so the price gap applies to that quantity. The payload's own rule states
      the evaluated key.
    - Alternative, written beside as `<variant>_state_price_held`: the line held at the case's use-key amount. The
      pairing's low end would be $463.34bn ($11,667 per member) instead of $462.95bn ($11,657); the high end does not
      use a justice variant.
    - No capital component is keyed on or responds as a state-priced line (gate), so the re-pricing's whole effect is
      the line's own amount.
  - **The cash set runs beside the case.** Its payload is the candidate's `corrections_v4_cash.json`, which the
    adopted lane's `main_case.cjs` reads. It is costed through the package's `forPayload()` of it, with every variant.
    It is never in the case's band.
- **`real_costs_totals.py`.**
  - The case's social rows are September 27's: the same items, and the long-run congestion figures ($13.99bn at the
    low end, $12.02bn at the high end).
  - **Designed rule: the pairing on the priced count.** The population lane restated the September 27 pairing, so its
    rows cannot be read for September 29 as they stand. The script takes its section `pairing_5plus` less its fiscal
    row, which leaves the restated social rows, and adds the case's own fiscal rows. Gates: the lane's fiscal rows are
    the September 27 bands, unrestated (1e-6), and its published social rows are this script's social rows for the case
    (2e-6: the lane prints six decimals, and each social figure is a difference of two). Alternative: a rerun of the
    population lane on the new case. It would give the same social rows unless a row reads something v4 moves. In
    that lane's `basis.csv` only congestion does: its lane cut is held at the adopted case's key share (below).
    Trade reads the CPS consumption key, which v4 does not change.
  - **The congestion figure is carried over, not recomputed.** The adopted summary flags it
    (`beside_the_account.congestion.not_recomputed`), and the script carries the flag into its JSON. v4 keys highways
    by vehicle miles and raises the group's share of highway spending from the economic-affairs key, 8.06%, to the
    road key, 9.57%. With the network following spending, a larger removed share offsets more of the decongestion, so
    the carried $13.99bn / 12.02bn is probably too high [INFERENCE, direction only; the size needs
    `service_response_long_run_2026_09_27/congestion.py` rerun on the road key].
  - The runs beside the case (7% on capital, option A and the cash set) each get their totals, and the cash set also
    gets its pairing on the priced count.
- **`constant_choices.py`.** It runs `debt_legacy.py --case sept29` (the debt lane's September 29 port) for the base
  split and with each of the ledger lane's choices. The results are as on September 27: row 8 at 0 moves the 2024
  federal part by −$0.027bn, the stock by −$0.35bn and 2024 interest by −$0.011bn. Row 10 on family and general
  assistance leaves 2024 alone and moves the stock by +$2.03bn and interest by +$0.066bn. The re-run gate holds.
  [CALCULATION: `derived/sept29/constant_choices.csv`, `constant_choices_stock.csv`]

### The September 29 figures ($bn a year; per member on 39,712,493)

| | Low end | High end |
|---|---:|---:|
| Fiscal main case (custody footing) | 371.4146 | 434.8410 |
| Fiscal, Hispanic footing (raw coding; the state-priced justice line re-priced) | 366.6820 | 430.0755 |
| Fiscal, Hispanic footing, the justice line held (alternative) | 367.0754 | 430.4689 |
| Social rows on the priced count (population lane, 5+ traffic basis) | 96.2647 | 100.6770 |
| **Pairing on the priced count** | **462.9467** | **535.5180** |
| Per member | $11,657 | $13,485 |
| Same pairing with the social rows on the published 40.90M union (the record's old basis) | 465.3947 | 538.2073 |
| Cash set, pairing on the priced count (beside) | 386.2332 | 462.4945 |
| Cash set, per member | $9,726 | $11,646 |
| September 27 case, pairing on the priced count | 413.7448 | 488.0471 |

The pairing moves +$49.20bn at the low end and +$47.47bn at the high end. The fiscal case moves +$49.60 / +47.47bn; the
low end moves $0.39bn less, the justice line's re-pricing. [CALCULATION: `derived/sept29/real_costs_totals.csv`,
`band_variants.csv`; the September 27 row from `../sept27_propagation_2026_09_27/derived/real_costs_totals.csv`]

Log (append-only; times from `date`):
- 2026-09-29 17:19 JST: section written by v4-debt-lane (claude-opus-5-5). The sept29 runs of `band_variants.cjs` (53
  gates pass), `real_costs_totals.py` and `constant_choices.py` exit 0. Gate 1: HEAD's and the edited
  `band_variants.cjs` and `real_costs_totals.py` write byte-identical files for sept24, sept26, sept26_schools and
  sept27 (16/16, into one scratch directory in turn). Nothing is committed, staged or stashed.
- 2026-09-29 21:15 JST (resumed after the machine rebooted at about 20:51; the earlier gate logs were lost with
  `/private/tmp`, so every gate was rerun and printed). The six pre-reboot files in `derived/sept29/` all parse. Fresh
  sept29 runs of the three scripts (21:04, rc 0 each; `band_variants.cjs` 53 gates pass, `real_costs_totals.py` 43,
  `constant_choices.py` its re-run gate) wrote all six byte-identical to them. Gate 3: `sept29` reproduces the adopted
  lane's `main_case`, $371.4146–434.8410bn, and `sept29_cash_set` its `cash_set`, $294.7011–361.8175bn, at 1e-9
  against `summary.json` and 1e-4 against `main_case_bands.csv`. Gate 1, into scratch output directories only:
  HEAD's `band_variants.cjs` and `real_costs_totals.py` and the edited ones write byte-identical files for sept24,
  sept26, sept26_schools and sept27 (16/16), and `constant_choices.py` writes the tracked files for all four cases
  (8/8). Against the tracked files, the edited scripts' outputs are identical in 10 of 16. The other six differ for
  reasons that predate this change, since HEAD's scripts write the same bytes:
  - two JSONs record the scratch directory as an input path (sept24 and sept26_schools `real_costs_totals.json`;
    identical once the path is mapped back);
  - `../sept26_propagation_2026_09_26/derived/sept26/real_costs_totals.csv` and `.json` were not rebuilt by b7f14e7e,
    which moved every adopted column's per-member divisor to the priced 39,712,493: the tracked file divides by
    40,896,574 (per member, low, 6.0088 against 6.1879 now);
  - `../sept27_propagation_2026_09_27/derived/band_variants.json` records `main_case_bands.csv`'s hash from before
    b3f4d849 (6e550bd3…; now 46443c0c…), and its `real_costs_totals.json` records that JSON's hash. The CSVs match.
  Gate 4: two `rerun_lane.py` passes over the lane's sept24 and sept29 commands, IDENTICAL 23/23, rc 0 each
  (21:09–21:13). No tracked file in `derived/` differs from HEAD. Every figure in the table above matches the fresh
  outputs.
- 2026-09-29 22:55 JST (after the lead committed 911afa6 and handed over the two stale files for this task). These
  scripts rebuilt them in place at 22:02:
  - `real_costs_totals.py --case sept26 --out-dir ../sept26_propagation_2026_09_26/derived/sept26` now puts per member
    on the priced 39,712,493, as b7f14e7e did for the other cases. Against HEAD, 14 of 56 CSV rows change, every one a
    "per group member" row of §7 or §7b, in the sept24, sept26 and change columns only. Each new value is the old one
    × 40,896,574 / 39,712,493 (1.029816; largest gap 9.1e-7, the six-decimal printing). The sept23 column stays on
    the published union. The JSON gains two keys, `per_member_population_m` and the `sources_sha256` entry for
    `main_case_decomposition_2026_09_29/derived/headcount.csv` (the divisor and its source).
  - `band_variants.cjs --case sept27` and `real_costs_totals.py --case sept27`: one key each changes, the
    `sources_sha256` entry for `main_case_long_run_2026_09_27/derived/main_case_bands.csv` (6e550bd3… → 46443c0c…,
    that file's sha256 since b3f4d849) and, in `real_costs_totals.json`, the entry for the refreshed
    `band_variants.json` (141869a7… → 2a2e0978…). Both CSVs are unchanged.
  - Nothing else in either lane moved: `rerun_lane.py` over each with all its commands, IDENTICAL 11/11 (sept27) and
    20/20 (sept26), and `git status` shows the four files only. Only sept27's own `real_costs_totals.json` records
    a hash of any of the four.

## v5 case (oct05), 2026-10-05

[2026-10-05: on main case v5 (`oct05`, `../main_case_2026_10_05/`, $390.29–461.24bn), the fiscal-plus-social pairing on
the lineage's 42,752,213 people is **$490.22–570.68bn a year**, **$11,466–13,349 per member**. On the September 29
case (`sept29`) it was $462.95–535.52bn and $11,657–13,485 on 39,712,493. The fiscal rows move +$18.71 / +26.40bn at
the pairing's ends (raw coding at the low end, the custody footing at the high end), and the added people's own social
rows add $8.56 / 8.76bn: +$27.27 / +35.16bn in all. The total rises and the cost per member falls, as in the fiscal
case. The cash set pairs to $407.30–492.85bn ($9,527–11,528 per member) beside it. [CALCULATION: `band_variants.cjs --case oct05` →
`real_costs_totals.py --case oct05` → `derived/oct05/real_costs_totals.csv`, column `pairing_on_priced_count`]]

### What changed

Both scripts take `--case oct05` and write to `derived/oct05/`. The `sept29` files and every earlier case are unchanged
(the edited scripts rewrite them byte for byte).

- **`band_variants.cjs`.**
  - The cash set is the case lane's own `derived/corrections_cash.json`, costed through the package's `CASH`. Gate: `CASH`
    has that payload exactly.
  - **The variant gate is split** (the case lane's Consumers row: it failed as written). A variant that picks another key
    moves the added people's own cells on that key. The September 29 payload now runs at the case's specifications as a
    gate-only run, never written. Gate 1: it moves every specification as the uncorrected model does (1e-9), the old
    gate. Gate 2: the case moves by that plus the lineage's own move, recomputed from its edits (1e-9). The own move is
    the edits on the variant's key less those on the case's key, times the line's response, plus the return on the
    capital keyed on that line (`pos_sl`, `pos_fed`). At the band ends it is −$0.160 / −0.161bn for raw coding and
    −$0.039 / −0.058bn for uncompensated care at 0.7x use. The grid ends and CBP held fixed move none of the added
    people's cells (`band_variants.json` `lineage.own_move_bn`).
  - [ASSUMPTION] **State prices with the lineage.** The added people's state-price amount on justice is the lineage's
    edit, $0.231bn. That edit is priced on their G3+ and white cells, not as national_gap_bn × their key share
    ($0.435bn). The rule therefore re-prices the union's part, and scales the added people's own amount by their
    raw-coded over use-key amount (0.9666). On the case's key it rebuilds the payload's line (8.9e-16).
  - **The added people's key shares** for the social rows (`lineage_social_keys`) are read at the band ends'
    specifications, 48 and 11 (gated equal to the case's ends in both fill-in methods). Each is their amount over the
    union's, the September 29 payload's, on one key:

    | Key | Low end | High end |
    |---|---:|---:|
    | Justice, raw coding / custody use | 6.98% | 6.78% |
    | Uninsured use | 7.09% | 6.99% |
    | Road (`hwy_sl`'s key) | 7.74% | 7.74% |
    | Consumption (general sales tax) | 9.17% | 9.17% |
    | K-12 operating | 8.21% | 9.35% |
    | Adults | 6.65% | 6.65% |
    | Head count | 7.65% | 7.65% |
- **`real_costs_totals.py`.**
  - [ASSUMPTION] **The added people's social rows** (the Consumers row: the social items were priced on the 39.71M
    union). Each of the population lane's restated rows is multiplied by the added people's share of the engine key it
    scales with (`LINEAGE_ROW_KEYS`). The restated rows are on audit row 4's union, with crash and congestion on the 5+
    basis.
    - The crime rows (victims, property crime, fear and avoidance, private security) use the justice key of each end's
      footing.
    - Unreimbursed care uses the uninsured-use key.
    - Congestion and crashes use the road key.
    - PM2.5, consumer scale and trade ties use the consumption key.
    - Schools use the K-12 operating key, and volunteering the adults key.
    - Housing and the scale net use the head count.
    - Restaurant variety, which the population lane found carries no head count, is not priced (0).

    Gate: the restated rows add to the restated social rows (2e-6). The added rows come to $8.56 / 8.76bn, of which
    PM2.5 is $6.25bn. At the union's average per member they would be $7.37 / 7.71bn: the added people consume more per
    head than the union, and their pupil shares are higher. The added people's crime, congestion and crash amounts rest
    on the engine's G3+ and third-plus white cells, not on measured G3+ offending or driving.
  - Every per-member figure of the case divides by the lineage population (gated: union + added = the case's 42.75M).
  - The record-basis rows of §7 (central values on two footings, the full span) use the lanes' published social rows,
    so they carry the union's social rows only. Use the pairing on the priced count.
  - The congestion figure is still the September 27 one. The JSON carries the case's `not_recomputed_v5` flag beside
    the v4 one.
- **`constant_choices.py --case oct05`** (run once the debt legacy lane had its `oct05` port, 00:05 JST 10-06) writes
  `derived/oct05/`. Each row also carries the lineage's parts of it, which the ledger lane's choice moves alike: audit
  row 8's change at the larger group (`v5_union_response:row8`, a `row8_finite` part) and the added people's copies of
  the row 8, finite and row 10 parts (`v5_lineage:constants` on their lines). The ledger lane's choices against this
  lane's: row 8, −$0.028bn of 2024 federal dollars, −$0.363bn of stock and −$0.012bn of 2024 interest (sept29 −0.027,
  −0.353, −0.011); row 10, +$2.09bn of stock and +$0.068bn of interest (sept29 +2.03, +0.066). Gate: each re-run moves
  the 2024 federal part by part 1's difference (2e-6). [CALCULATION: `derived/oct05/constant_choices_stock.csv`]

### The October 5 figures ($bn a year; per member on 42,752,213)

| | Low end | High end |
|---|---:|---:|
| Fiscal main case (custody footing) | 390.2940 | 461.2431 |
| Fiscal, Hispanic footing (raw coding; the state-priced justice line re-priced) | 385.3937 | 456.3087 |
| Fiscal, Hispanic footing, the justice line held (alternative) | 385.7948 | 456.7098 |
| Social rows on the priced union (population lane, 5+ basis) | 96.2647 | 100.6770 |
| The added people's social rows | 8.5593 | 8.7590 |
| **Pairing on the priced count** | **490.2177** | **570.6791** |
| Per member | $11,466 | $13,349 |
| Cash set, pairing on the priced count (beside) | 407.3001 | 492.8452 |
| Cash set, per member | $9,527 | $11,528 |
| September 29 case, pairing (39,712,493) | 462.9467 | 535.5180 |

Log (append-only; times from `date`):
- 2026-10-05 23:11 JST: section written by v5consC (claude-opus-5-5). `band_variants.cjs --case oct05` passes 67
  gates; `real_costs_totals.py --case oct05` passes 52. The edited scripts rewrite every earlier case's files byte for
  byte, in place: sept24, sept26_schools (`../sept26_propagation_2026_09_26/derived/`), sept27
  (`../sept27_propagation_2026_09_27/derived/`) and sept29. `git status` shows no derived change outside
  `derived/oct05/`. `rerun_lane.py` over the sept24, sept29 and oct05 commands (eight, with `constant_choices.py` for
  sept24 and sept29) reports IDENTICAL 27/27, rc 0. Nothing is committed.
- 2026-10-06 00:15 JST: `constant_choices.py --case oct05` run on the debt legacy lane's `oct05` port (its gates pass;
  the sept29 run rewrites its two files byte for byte). `rerun_lane.py` over the nine commands (`constant_choices.py`
  for sept24, sept29 and oct05 included) reports IDENTICAL 29/29, rc 0 (00:13–00:15). Nothing is committed.
