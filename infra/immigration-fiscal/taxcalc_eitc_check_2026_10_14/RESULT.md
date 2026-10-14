Model ID: unavailable in this worker runtime; system identifies GPT-6.

**Verdict:** Correcting the two specified defects raises main case v6's band by **+$0.000238bn low / +$0.000896bn high, first order** (about $0.24m / $0.90m). **Neither clears $0.5bn.** This is the central status/on-books case, averaging its two main fill-in methods, and translating the federal-income-tax and refundable-credit lines only. EITC fit improves; ACTC fit worsens slightly. [CALCULATION: `measure.py` → `derived/summary.json`, `first_order_band_change_bn.central`; `derived/validation.csv`]

## Scope and rule

This is a paired operator measurement on income-year 2024 CPS ASEC 2025, under the existing case's removal frame. Every original donor run is executed; the corrected run replays its exact donor-row and collapse-level arrays. The published inputs, return/dependent mapping, seed, donor weights, other taxes and AGI construction stay fixed. A guard checks that only `EIT_CRED`, `ACTC_CRD` and `SPM_RESOURCES` differ. The process writes only inside this lane; it does not fix the upstream module or rebuild the case. [CALCULATION: `measure.py`; all 16 donor hashes in `summary.json.donor_checks`]

The corrected EITC is `max(min(phase_in, maximum_credit − phaseout), 0)`, with phase-out income the greater of AGI and earned income. Earned income is wages plus net business/farm profit **minus half the self-employment tax**, computed separately for each person before summing return members. This reuses `mixed_unit_credits_2026_10_14/credits.py::eitc` and `half_se_tax`, including the 2024 wage base, rates and earnings floor. `taxcalc.compute` is monkeypatched; an in-memory AST clone of `hotdeck.run` changes exactly `earned_old` and `earned_new`. [SOURCE: [26 U.S.C. §32(a)(1)–(2), (c)(2)(A)(ii), 2024 edition](https://www.govinfo.gov/content/pkg/USCODE-2024-title26/html/USCODE-2024-title26-subtitleA-chap1-subchapA-partIV-subpartC-sec32.htm); [§164(f)](https://www.govinfo.gov/content/pkg/USCODE-2024-title26/html/USCODE-2024-title26-subtitleA-chap1-subchapB-partVI-sec164.htm); IRS Rev. Proc. 2023-34 §3.06, implemented in the reused rule]

**ACTC uses the same net earned-income base.** Section 24(d)(1)(B)(i) refers to earned income within §32; the 2024 Schedule 8812 earned-income worksheet subtracts Schedule 1 line 15, the deductible self-employment-tax amount. Thus the base correction applies to ACTC too, despite its worse Census fit below. The probe leaves the simplified model's other ACTC choices intact, including its omission of the three-child payroll-tax alternative. [SOURCE: [26 U.S.C. §24(d)(1)(B)(i), 2024 edition](https://www.govinfo.gov/content/pkg/USCODE-2024-title26/html/USCODE-2024-title26-subtitleA-chap1-subchapA-partIV-subpartA-sec24.htm); [2024 Schedule 8812 instructions, Earned Income Worksheet lines 5–7](https://www.irs.gov/pub/irs-prior/i1040s8--2024.pdf)]

The half-SE deduction's effect on the hot deck's **AGI change** is a separate, unmeasured correction here. Published AGI is already the baseline; subtracting the deduction from it again would double-count it. This lane corrects earned income at both evaluations and holds the old AGI-change operator. Consequently `FEDTAX_BC` is exactly unchanged at every seed, variant and population basis. [CALCULATION: unchanged-field gates; `totals.csv`; `verify.py`]

## CPS-dollar changes

Changes are **corrected minus published operator**, $bn, arithmetic means of the five `main` seeds (20260923–20260927). The union uses audit row 4's **39,712,493** people (weighted sum 39,712,493.3312); everyone else means other civilians on the account's universe. Raw published-weight results are also supplied, explicitly labeled `published`, alongside the row-4 results. The donor procedure retains its original published weights. [DATA: `main_case_candidate_2026_09_28/derived/production_row4.json`; CALCULATION: `totals.csv`, `summary.json.populations`]

| Donors | Group | ΔEIT_CRED | ΔFEDTAX_BC | ΔACTC_CRD |
|---|---|---:|---:|---:|
| Union/nativity matched | Union | −0.013818825 | 0 | +0.000786720 |
| Union/nativity matched | Everyone else | −0.044484989 | 0 | +0.001437457 |
| Pooled control | Union | −0.011519484 | 0 | −0.000042903 |
| Pooled control | Everyone else | −0.038357391 | 0 | +0.002476762 |

[CALCULATION: `derived/totals.csv`, `main,mean,*,row4,*`; every individual seed and both variants included.]

The original lane's two methods are **shares**, not unnormalized credit-dollar totals. `b_hotdeck_union_matched` uses matched shares; `b_matched_over_pooled` uses `base_share × matched_share / pooled_share`. As its driver does, the method mean is formed from mean matched and pooled shares, **then** their ratio is taken; it is not the arithmetic mean of the seed ratios. `all_items` uses its three original seeds (20260923–20260925), also measured in full. [SOURCE: `cps_imputation_keys_2026_09_23/run_hotdeck.py::SPECS`, lines 55–60; `combine_onbooks_lane.py::assemble`; CALCULATION: `keys.csv`, `totals.csv`]

## Main-case first-order translation

The primary translation applies row-4 weights and the adopted state-aware status flag, using the existing origin-specific central on-books shares. EITC is zero on flagged unauthorized records; ACTC takes their on-books fraction. The published operator's two method shares reproduce the adopted stack's refundable-line deltas at **all three** on-books arms and both allocations, within $1 of account money. These status rules and national normalization explain why the raw union changes above cannot simply be multiplied by 1.90 to obtain the adopted case change. [SOURCE: `combine_status.py::status_vectors`; `combine_onbooks_lane.py::assemble`; DATA: `_cache/onbooks_lane_line_deltas.json`; CALCULATION: `verify.py`]

For each method/allocation, the CPS group-equivalent change is the **published, status-adjusted national key × change in the method's group share**. This expresses the case's normalized share movement in CPS dollars, with the national base held fixed. Multiply it by the brief's **1.90 account dollars per CPS dollar** on `refundable_tax_credits`. This is an account-allocation translation, not a claim that national spending changes by the corrected Census-dollar total. [SOURCE: `mixed_unit_credits_2026_10_14/RESULT.md`, Limits; CALCULATION: `summary.json.translation`]

| Main method, central status arm | Allocation/end | CPS group-equivalent Δ, $bn | Refundable line / net cost Δ, $bn | Federal income-tax Δ, $bn |
|---|---|---:|---:|---:|
| b_hotdeck_union_matched | shared / low | +0.000418211 | +0.000794600 | 0 |
| b_hotdeck_union_matched | personal / high | +0.000670510 | +0.001273969 | 0 |
| b_matched_over_pooled | shared / low | −0.000168129 | −0.000319445 | 0 |
| b_matched_over_pooled | personal / high | +0.000272958 | +0.000518620 | 0 |
| **Mean of methods** | **low** | | **+0.000237577** | **0** |
| **Mean of methods** | **high** | | **+0.000896295** | **0** |

[CALCULATION: `summary.json.translation`, mean of the two `main` methods in `case_central`. Transfers have response 1.]

The case's IRS translation multiplies its federal-tax stack by the ratio of the IRS-rekeyed to prior group share (`main_case_candidate_v2_2026_09_28/package.cjs::taxEditOf`, `tax_key_heldout_2026_09_28/derived/translation_inputs.json`). Here its input change is **zero**, so that ratio produces zero at both allocations; no average IRS-dollar conversion is substituted for it. [SOURCE: cited caller and translation inputs; CALCULATION: `totals.csv`, `summary.json.translation`]

The low/on-books arm gives +$0.000041bn / +$0.000717bn; the high arm +$0.000429bn / +$0.001072bn. The `all_items` sensitivity, central status arm and its own three seeds, gives −$0.002236bn / +$0.000168bn. None clears $0.5bn. For the main per-seed mean of the two methods, effects range from −$0.007465bn to +$0.008853bn shared and −$0.006921bn to +$0.007533bn personal. These are seed spreads, not sampling confidence intervals. [CALCULATION: `summary.json.translation`, `first_order_band_change_bn`; ranges of per-seed method means]

**What an engine rebuild would add:** the changed credits alter SPM resources, hence the consumption and resource keys. All affected `line_deltas.json` fields are measured for every seed and method, including the mean: `general_sales_tax`, `excise_selective_sales`, `customs_duties`, `personal_current_transfers`, `economic_affairs_services`, `housing_community_services`, `recreation_culture`, `refundable_tax_credits`, and the four resource-keyed subsidy lines. The supplied deltas follow the original lane's full line totals; the case separately restricts the refundable line to its non-PTC part. A full rebuild would propagate those other keys through the case's consumption correction, state prices, benchmark scaling, added-descendant edits, public-capital account and endpoint selection. It would also use the exact refundable conversion (about 1.902) and the OTA adjustment rather than the requested rounded 1.90. **That full band effect has not been measured.** [CALCULATION: `line_deltas.csv`, `line_deltas.json`; SOURCE: `translate.py::line_deltas`, `combine_onbooks_lane.py::stack`; `mixed_unit_credits_2026_10_14/RESULT.md`, Limits]

## Validation and disconfirmation

Validation uses published incomes, the existing return mapping and published weights, exactly the original `taxcalc_validation.csv` pattern (64,276 returns). The baseline table is reproduced before evaluating the corrected operator. [CALCULATION: `validation.csv`; baseline validation gate in `measure.py`]

| Field | Census total, $bn | Model total before → after, $bn | Weighted correlation before → after | Mean absolute error before → after, dollars | Within $100 before → after |
|---|---:|---:|---:|---:|---:|
| FEDTAX_BC | 1,987.795 | 2,123.291 → 2,123.291 | .990289 → .990289 | 853.793 → 853.793 | 78.241% → 78.241% |
| EIT_CRED | 43.299 | 41.011 → 41.239 | .976900 → .977490 | 19.587 → 17.580 | 98.616% → 99.019% |
| ACTC_CRD | 21.900 | 20.622 → 20.570 | .989977 → .989957 | 8.944 → 9.270 | 98.535% → 98.393% |

[CALCULATION: `validation.csv`.]

The EITC correction improves all three fit measures; the ACTC correction worsens all three slightly and moves its total farther below Census. A legally better earned-income base does not guarantee a better fit when return mapping and other model simplifications remain. The larger corrected EITC *level* on published incomes also does not imply a larger hot-deck *difference*: corrections to old and new incomes cancel. The very small case result is measured, not inferred from that cancellation. [CALCULATION: validation table, paired-seed results; INFERENCE: explanation of remaining model mismatch]

This numerical probe retains the existing politically sensitive frame and status assumptions. LLM interpretation is unverified until checked; the legal sources, original seed outputs, adopted-stack checks and countervailing ACTC fit are supplied to make the conclusion independently checkable. It establishes no new population attribution or removal response. [SOURCE: `notes/llm-bias-caveat.md`; CALCULATION: `measure.py`, `verify.py`]

## Files and reproduction

- `measure.py`: operator patch, paired donor execution, full-weight key/line calculations, validation and provenance hashes. `--profile-one` profiles one original main donor run without changing outputs.
- `verify.py`: adopted-stack baselines, seed coverage, total means, zero federal-tax movement, conversion, finite values and LF checks.
- `derived/totals.csv`: before/after/change CPS totals, every seed and arithmetic mean, main and all-items, both donor variants, both population bases, union and everyone else.
- `derived/keys.csv`: every changed method key, each seed and driver-style mean, both plain bases and all three case status arms.
- `derived/line_deltas.csv` and `line_deltas.json`: corrected-minus-published changes in every affected original line field; JSON holds the method means.
- `derived/validation.csv`: both operators on published incomes.
- `derived/summary.json`: first-order translation at every seed/arm, donor hashes, gates and source hashes. Runtime/peak memory print to stdout to keep outputs reproducible.

```sh
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 uv run --no-project python3 \
  scripts/rerun_lane.py infra/immigration-fiscal/taxcalc_eitc_check_2026_10_14 \
  "uv run --no-project python3 {lane}/measure.py" \
  "uv run --no-project python3 {lane}/verify.py"
```

Initial measurement passed 498 gates, with peak resident memory **1.123 GB**. Independent accounting/adopted-stack checks and both script compile checks passed. The first full rerun reproduced all calculations, validation, donor hashes and gates; its only difference was the whole-file fingerprint of the concurrently edited `mixed_unit_credits/credits.py` (8/9 files identical; exit 1). Both imported functions and their constants were unchanged. **The final full rerun against the refreshed source fingerprint passed: IDENTICAL 9/9, exit 0; both commands exited 0.** This final receipt was appended after that comparison; no analytical artifact or script changed afterward. [CALCULATION: rerun stdout, exact summary-object comparison; `verify.py`]

## Log

- 2026-10-14 06:03:19 UTC (`date -u`): paired operator probe running; first two variants reproduce the stored full-weight keys; donor replay and unchanged-field gates pass.
- 2026-10-14 06:05:56 UTC (`date -u`): internal profiling completes: 25.605 seconds for one original run, 23.630 in donor construction. Corrected runs replay donor arrays; duplicate plain-key construction removed for the rerun. Host process inspection is unavailable (`sysmond service not found`), so profiling used the probe's own cProfile route, not process-list inference.
- 2026-10-14 06:12:10 UTC (`date -u`): all 16 paired runs complete; 498 gates pass, 645.957 seconds, peak RSS 1.123 GB; only credits/resources differ.
- 2026-10-14 06:13:32 UTC (`date -u`): independent verifier reproduces all 12 adopted credit-stack baselines, confirms seed coverage and arithmetic; EITC fit improves and ACTC fit worsens. First-order central band change is +0.000237577 / +0.000896295bn.
- 2026-10-14 06:23:54 UTC (`date -u`): first required rerun exits 1, DIFFERS 8/9; both commands exit 0. Only the concurrently edited credits.py whole-file hash changes in summary.json; all calculation values, validation, donor hashes and gates reproduce exactly. The imported functions and constants match the versions read initially. Raw CPS zip independently matches pinned SHA256 318845a2b5e0034eb2973898de1738f4df0025727de38499e7669cb9c0deef0b. Population presentation corrected against the generated weighted total; clean rerun follows.
- 2026-10-14 06:31:21 UTC: final required rerun passes IDENTICAL 9/9, exit 0; measure.py and verify.py each exit 0. All outputs, donor identities, validation and provenance reproduce. Completion receipt appended; no Git metadata operations performed. Exact model-ID environment variables were absent, and the optional request for the assigned ID had not received a response.
- 2026-10-14 06:32:08 UTC (`date -u`): date-backed completion receipt recorded. The preceding 06:31:21 finish time came from the clock tool. Git operations were read-only status/ls-files checks; no merge, stage, commit or other Git metadata mutation occurred. Changed repository paths are exactly the nine files listed above.
