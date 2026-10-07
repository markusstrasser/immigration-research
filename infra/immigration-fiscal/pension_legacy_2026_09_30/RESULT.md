claude-opus-5-5

**Verdict (verified and corrected 2026-09-30):** On matched group keys and the account's headcount, the Mexican-origin union's attributed public-employee pension interest expense exceeds third-plus-generation non-Hispanic whites' by **$4.89 / $4.68bn in 2024**. The union is $20.61 / $21.53bn and whites $15.72 / $16.85bn. These are modeled allocations of measured national liabilities and interest, including imputed expense; they are not cash payments by the group. On the engine's own union keys, the stock remains **$422–448bn**, with **$20.9–22.1bn** interest ($527–558 per member), and its difference from the corrected white slice is $5.21 / $5.30bn. [CALCULATION: `pension_legacy.py` → `derived/summary.csv`, arm `adopted`; matched difference `mexican_origin_rough_minus_A1_white`; low / high = specifications 48 / 11]

None of this is priced in the main case. BEA books the interest inside the domestic interest row ($1,118.87bn) that the case holds at zero response. The case's pension accrual covers Social Security and Part A only. This legacy stays beside the annual account and the federal financing model. **Their additivity has not been established:** the federal model compounds NIPA consumption, which already contains accrued public-employee compensation. See overlap checks below and the [separate-statement decision](../../../decisions/2026-09-30-legacy-comparisons-separate.md).

Lane `infra/immigration-fiscal/pension_legacy_2026_09_30/`, written 2026-09-30, 05:26–05:55 JST (times from `date`). Low and high ends follow the main case's specifications 48 and 11 ($371.4 / 434.8bn). Per-member figures divide by the 39,712,493 people the account prices (dataset audit row 4). Every comparator has the union's headcount and follows its population path (replacement framing).

## 1. What was measured

### The interest inside the row the case holds at zero

| 2024, $bn | Value | Source |
|---|---:|---|
| Government interest to persons and business (the account's `domestic_interest`) | 1,118.870 | BEA T3.1 line 28 |
| of which federal / state-local | 844.262 / 274.608 | T3.2 line 34 / T3.3 line 29 |
| State-local DB plans: imputed interest on plans' claims on employers | **162.963** | T7.24 line 13 |
| Federal DB plans: imputed interest on plans' claims on employers | **62.006** | T7.23 line 19 |
| Federal DB plans: monetary interest (on Treasury securities the plans hold) | **89.071** | T7.23 line 18 |
| Pension interest in the row, all three | **314.040** (28.1% of the row) | sum |
| Imputed interest only (BEA's "unfunded" measure) | 224.969 (20.1%) | sum |

[SOURCE: BEA NIPA Section 3 workbook, published 2026-08-26, SHA256 `69b5c7ae…615e`; Section 7 workbook, SHA256 `ce107c8c…b9ef`, the back-cast's pinned copy; `derived/measured_2024.csv`, `derived/domestic_interest.csv`]

**Is it inside the $1,118.87bn row?** Yes. The footnotes say so for each government, and `measure_bea()` gates on them:

- **Table 3.1, footnote 2:** interest to persons and business "includes interest accrued on the actuarial liabilities of defined benefit pension plans for government employees".
- **Table 3.2, footnote 4:** the same wording "for federal government employees".
- **Table 3.3, footnote 1:** the same wording "for state and local government employees".

[SOURCE: workbook footnotes] The engine keys `domestic_interest` at $1,118.87bn with response 0 at both ends. The script stops if that changes. [DATA: `white_replacement_2026_09_28/derived/engine_lines_sept29.json`] State-local imputed interest is 59.3% of all state-local interest paid. [CALCULATION]

**What the federal part covers.** For federal plans, the interest accrued on the liabilities is T7.23 line 41, $151.077bn. That equals imputed plus monetary interest, so Table 3.2's footnote places both in line 34. [SOURCE: T7.23 lines 17–19, 41]

- **The $89.071bn of monetary interest** is dominated by interest on Treasury securities, but the aggregate does not identify every issuer. Their assets include $2,639bn of nonmarketable Treasury securities, $1,164bn of claims on the sponsor, and $28.6bn of everything else (including marketable Treasuries). [DATA: Z.1 S129s1.2.s, end-2023]
- **Consolidation convention:** Treasury securities are internal federal claims; the lane's consolidated stock removes nonmarketable securities and sponsor claims, while the narrow arm reports sponsor claims alone.
- **For state-local plans,** the government pays only the imputed part. The plans' monetary interest and dividends ($116.1bn) come from other issuers.

### The unfunded stock, BEA basis

| $bn | End-2023 | End-2024 | Source |
|---|---:|---:|---|
| State-local DB: claims of pension fund on sponsor (unfunded) | **3,125.6** | 3,005.9 | Z.1 FL223073045 |
| State-local DB: pension entitlements | 8,942.7 | 9,253.6 | Z.1 FL224190043 |
| Federal DB: claims on sponsor (BEA's unfunded) | 1,163.7 | 962.0 | Z.1 FL343073045 |
| Federal DB: pension entitlements | 3,831.7 | 3,871.9 | Z.1 FL344190045 |
| Federal DB: entitlements less assets other than sponsor claims and nonmarketable Treasuries | **3,803.1** | | [CALCULATION] |

[SOURCE: Federal Reserve Z.1 CSV release through 2026:Q2, SHA256 `b63af975…e4b6`]

- **Funded share.** State-local plans are 65.0% funded on this basis. [CALCULATION]
- **Implied rates.** 2024 imputed interest over the end-2023 stock is 5.21% for state-local plans. Interest accrued on all state-local entitlements is 4.94%. All federal plan interest over the consolidated stock is 3.97%. [CALCULATION] The stock and the interest are both BEA's, so the attribution uses one fraction for both.
- **Cross-check.** The Financial Report's FY2024 interest on the federal pension liability is **$151.0bn** (civilian $75.3bn, military $75.7bn), against BEA's $151.077bn. The Report's liability is larger ($5,364bn at the start of FY2024) because it discounts at 2.5–3.0% Treasury rates. [SOURCE: Financial Report of the U.S. Government FY2025, Note 13, FY2024 columns, SHA256 `deed540c…d55`]
- **Stock trend.** The state-local stock peaked at $4.49tn at end-2018 and fell to $3.01tn at end-2024. The entitlement level fell in 2022, so the BEA revaluation drives this. [DATA: `derived/headcount_path.csv` source series]

### Retiree health (OPEB), separately

- **Federal.** Post-retirement health liabilities were **$1,740.9bn** at end-FY2024: civilian $443.1bn, military $1,297.8bn. FY2024 interest on them was **$45.5bn** ($12.2bn civilian, $33.3bn military). [SOURCE: FR FY2025 Note 13] NIPA has no DB pension table for these. It books the Medicare-Eligible Retiree Health Care Fund as an insurance fund in employer contributions (T7.8 line 16, footnote 2), so this interest is not in the $1,118.87bn row. [INFERENCE: table structure] At the adopted weighting, the union's share is **$0.49–0.56bn** a year (civilian only; military follows defense, at zero response). At average cost, with defense per head, it is $4.2bn. [CALCULATION: `derived/opeb_federal.csv`]
- **State-local.** Not measured. No national 2024 aggregate of GASB 75 liabilities was found in a primary source, and neither NIPA nor Z.1 carries one. It is a named gap, and adding it could only raise every group's figure.

## 2. Overlap checks

| Possible double count | Finding | Evidence |
|---|---|---|
| Normal cost is already in 2024 function spending | **Yes, and correctly.** Benefits earned in 2024 enter compensation and each function's consumption. This lane prices interest on the pre-2024 stock. | T7.8 line 10, state-local retirement contributions of $192.994bn, equals DB employer pension compensation of $172.711bn (T7.24 lines 5+6, including $29.260bn service charges) plus DC contributions of $20.283bn (T7.25 line 8). Pure DB employer normal cost is $143.451bn. Federal civilian pension compensation plus TSP is $71.747bn = $58.719bn + $13.028bn; military $49.321bn = $47.443bn + $1.878bn. [SOURCE; CALCULATION, compensation identity gated in the test] |
| Amortization payments | Not in current spending and not added here. Contributions above normal cost (state-local $41.6bn, federal $144.3bn, the negative imputed contributions) repay the stock. | T7.24 line 6; T7.23 line 8 |
| Federal legacy model (`debt_legacy_2026_09_23`) | **Unreconciled; do not sum.** Excluding pension interest from the Treasury rate does not remove unpaid employer pension contributions from the spending gap being compounded. Both benefit conventions retain NIPA consumption. | `debt_legacy.py` → `programme_federal()` carries the T3.17 consumption categories; `stock()` compounds the gap without a public-employee pension financing bridge. [SOURCE: [BEA accrual treatment](https://www.bea.gov/index.php/news/blog/2013-06-17/bea-move-accrual-accounting-defined-benefit-pension-plans); CALCULATION: code trace in the decision] |
| Main case pension accrual | **None.** It covers Social Security (OASDI) and Medicare Part A only. | `main_case_2026_09_29/derived/corrections.json` → `meta.pension_accrual` (`oasdi_lines`, `part_a_accrual_bn`) |
| Capital return | None: public capital stocks only. | `capital_return_services_2026_09_27/capital_return.py:388,1721` holds `domestic_interest` at response 0 ("double-count gate") |

## 3. Attribution

**Which services built the liability.** State-local payroll by function, March 2024: education 51.2% (with libraries), public order and safety 16.8% (police, fire, courts, corrections), health and hospitals 10.3%, and administration 7.3%. The remainder is spread thinly. [SOURCE: Census ASPEP 2024 via the `timeseries/govsemp` API; `derived/function_mix.csv`]

- **Federal civilian.** Defense civilians are 33.1% of civilian compensation (T3.11.5 line 7 against T3.10.5 line 37). The nondefense rest is spread by nondefense consumption by function (T3.17 lines 12–20), a proxy for payroll.
- **Federal military.** Defense throughout.
- **Enterprises.** Utilities, transit and liquor stores take the per-head key of the case's enterprise line.

**The group's use.** Each line takes the group's 2024 share of that line:

- **The union.** The engine's own shares at each end (the sept29 dump), plus its state-price and road-mile terms. The low end reproduces `black_comparator_rough_2026_09_28/derived/rekey_line_shares_sept29.csv` to 5e-7 (gated).
- **Third-plus whites, the all-residents slice and the matched union.** The white lane's current row-4 line amounts including their sept29 state-price and road terms, exported by `legacy_comparators_2026_09_30/group_lines.py`. Every slice's recorded population and each line's national amount and response are checked against the case. The prior September 27 share file is no longer read.
- **Responses.** Each line responds as the main case says: education, public order and health at 1, general government 0.60–0.85, economic affairs 0.38–0.64, and defense 0. [DATA: `derived/group_shares.csv`]

Key shares, union / white / all-residents:

| Line | Union | Whites | All residents |
|---|---:|---:|---:|
| Education | 0.157 | 0.100 | 0.118 |
| Public order, state-priced | 0.147 | 0.097 | 0.118 |
| Health | 0.062 | 0.081 | 0.118 |

**The time path.** The end-2023 stock pays for service rendered before 2024. The Mexican-origin population share relative to 2024 is built as the back-cast builds it:

- ACS 2005–2024 over BEA population;
- decennial counts before 2005, spliced to the ACS level by the 2010 ratio of 1.0356;
- log-linear between anchors.

The path is 0.33 in 1980, 0.47 in 1990, 0.64 in 2000 and 0.93 in 2010. [DATA: `derived/headcount_path.csv`] The anchors are the 2000 and 2010 counts of 20,640,711 and 31,798,258, from the 2010 brief's table 1. The 1990 count, 13.50M, comes from the 2000 brief's +52.9%. The 1980 and 1970 counts, 8.74M and 4.53M, come from the WE-2R chart's +54.4% and +92.8%. [SOURCE: Census C2010BR-04, C2KBR/01-3, WE-2R]

Service years are weighted by a vintage kernel. Benefits not yet in payment are held whole for 15 years, then run off linearly to zero at 45 years. State-local weights are scaled by population, because state-local FTE per resident is steady (5.25% in 1998, 5.11% in 2024; T6.5D). [ASSUMPTION; DATA] The resulting time factor is **0.828** for state-local plans and 0.812 for federal plans. [CALCULATION]

### Arms (union / whites / difference; interest in $bn a year, low–high)

| Arm | Union stock | Union interest | Whites interest | Difference (interest) | Per member, union |
|---|---:|---:|---:|---:|---:|
| **Headcount path, vintage kernel (engine union anchor)** | **421.8–447.9** | **20.94–22.15** | 15.72–16.85 | **+5.21–5.30** | **$527–558** |
| Simple: 2024 shares × stock | 511.1–543.0 | 25.35–26.82 | 19.06–20.43 | +6.30–6.39 | $638–675 |
| Headcount path, weights = yearly change in the stock | 363.6–385.8 | 18.10–19.13 | 13.55–14.50 | +4.55–4.63 | $456–482 |
| Kernel short (10 / 35 years) | 453.2–481.4 | 22.49–23.79 | 16.90–18.11 | +5.59–5.68 | $566–599 |
| Kernel long (20 / 60 years) | 379.6–403.0 | 18.86–19.94 | 14.15–15.15 | +4.71–4.79 | $475–502 |
| Federal narrow (BEA's claims on sponsor only) | 367.5–385.6 | 19.15–20.10 | 13.98–14.74 | +5.17–5.36 | $482–506 |
| Average cost (every response 1, defense per head) | 697.2–702.7 | 32.14–32.44 | 27.40 | +4.75–5.04 | $809–817 |

For the comparison with the federal lane, use the **matched union**, $20.61 / $21.53bn interest, minus the same whites: **+$4.89 / $4.68bn**. The engine-versus-white differences in the table use a different union key. The all-residents slice is $384–409bn of stock and $18.8–19.9bn interest ($473–500 per member). [CALCULATION: `derived/summary.csv`; every cell in `derived/attribution.csv`]

**Which arm to adopt: the headcount path with the central kernel.** The stock pays for benefits earned mostly from 1979 to 2023. In those years the union was 33–98% of its 2024 population share. Applying 2024 shares charges it for services to people who were not yet here, which overstates by about a fifth: the simple arm is 21% higher. The kernel beats the stock-change weights because most changes in the stock are revaluations and investment gains and losses on benefits of all vintages, not services rendered that year. Stock-change weights would charge the 2008 asset loss to 2008's users. Its $18.1–19.1bn is kept as the low companion. [FRAMING-SENSITIVE]

**Federal consolidated over narrow.** Most federal fund assets are internal Treasury claims. The consolidated arm uses all $151.1bn of pension interest, alongside the narrow sponsor-claim arm ($1.2–1.4bn federal for the engine union, against $3.0–3.5bn). Its stock excludes sponsor claims and nonmarketable Treasuries from covering assets but still counts $6.173bn of marketable Treasuries among other assets, so it is an approximation to full federal consolidation. This limitation concerns the stock; the interest amount comes directly from BEA.

**Main-case responses over average cost.** They keep the line consistent with the account and the debt legacy. The convention-driven zeros are priced, not hidden:

- Average cost adds **$11.2bn / $10.3bn** a year to the union's figure, almost all federal military pensions at defense's per-head key.
- With matched union and white keys, the average-cost difference is +$4.43bn at both ends, against +$4.89 / $4.68bn under the main-case responses.

**Original attribution, before the row-4 correction (superseded).** By line, low end; the updated figures are in `derived/by_line.csv`:

- **Schools:** +$3.77bn. The union's education share is 0.157 against 0.103.
- **Public order:** +$1.37bn. State-local $3.33bn against $2.23bn, plus federal +$0.27bn. The union's share carries its state-price term: its police price index is 1.12, against whites' 0.94 (`v4_group_terms_sept29.csv`).
- **Income security:** +$0.60bn.
- **Offsets:** health −$0.55bn and economic affairs and highways −$0.43bn, where whites use more.

## 4. What this is not

- **The stock is never added to an annual figure.** $422–448bn is a balance entering 2024. Only the $20.9–22.1bn of interest is an annual cost.
- **It never enters the 2024 with/without headline.** Removing the group in 2024 does not remove benefits already earned by past service. The interest is owed either way. The line answers the historical question (what past services to the group left unpaid), as the debt legacy does, and is stated beside the account.
- **It is not the stock's principal as a 2024 cost.** Amortization payments are principal and are not counted here.
- **It is not a claim that the group caused underfunding.** Funding policy, benefit enhancements and asset returns set how much of the promised cost went unpaid. This lane allocates the unpaid part by who received the services.
- **Do not add it to the federal legacy model.** Actual Treasury debt and pension claims are distinct instruments, but the federal model's accumulated NIPA spending has not been reconciled to those instruments. A common financing bridge is needed before summing.

## 5. Limits and checks against the result

- **Liability basis [FRAMING-SENSITIVE].** BEA discounts state-local liabilities at an implied ~4.9%. On the plans' own ~7% assumptions the unfunded stock is smaller. At Treasury rates, which the Financial Report uses for federal plans, it is larger. Every group scales together, so the difference scales with the level.
- **Vintage mismatch.** Section 7 (T7.23, T7.24) carries the September 2025 annual update, while the Section 3 interest row is the August 2026 vintage. The 2024 imputed interest may since have been revised. Its size is unknown.
- **Frames, corrected 2026-09-30.** The first run mixed published-count comparator shares with row-4 overlays and denominators. The current run consumes the same gated row-4 export as the federal comparator lane, including a matched union. The engine's own union attribution is retained separately.
- **Intensities held at 2024.** Each group's per-head use of each function is held at its 2024 level, as the back-cast's flat rule holds it. The union's school intensity was probably higher in 1990–2010, when it was younger. That would raise its figure. [INFERENCE]
- **Geography.** It is not modelled. Unfundedness per resident varies widely by state. Illinois and New Jersey are heavy; California and Texas, where most of the union lives, carry large plans. The national share could be off in either direction. [INFERENCE]
- **Measured and assumed inputs.**
  - Measured: every stock, interest and payroll figure, and the population counts.
  - Assumed: the vintage kernel; the federal nondefense payroll mix, proxied by consumption; hospitals keyed on the health line; USPS in the federal civilian stock but not in its function mix.
- **Disconfirmation tried.** Three checks could have broken the result. None did.
  - If the $1,118.87bn row held no pension interest, the line would be empty. The footnotes and T7.24 rule that out.
  - If normal cost were outside compensation, this lane would be undercounting. T7.8 reconciles to the dollar.
  - If the Financial Report's pension interest disagreed with BEA's, the federal measure would be suspect. It agrees within $0.08bn.

## Reproduce

```sh
# inputs, once (ASPEP needs the Census key; the key is read, never written or printed)
uv run --no-project python3 infra/immigration-fiscal/pension_legacy_2026_09_30/pension_legacy.py --fetch
uv run --no-project python3 infra/immigration-fiscal/pension_legacy_2026_09_30/pension_legacy.py
uv run --no-project python3 -m pytest infra/immigration-fiscal/pension_legacy_2026_09_30/ -q
```

Inputs are cached in `_cache/` (ignored), and `source_pins.json` records the SHA256 and size of each. The BEA Section 3 and Section 7 hashes equal the pins in `full_account_spending_2026_09_20` and `historical_backcast_2026_09_20`. The sibling-lane inputs read in place are:

- `white_replacement_2026_09_28/derived/engine_lines_sept29.json`;
- `legacy_comparators_2026_09_30/derived/group_lines_sept29.csv` (regenerate with that lane's `group_lines.py`, which runs the current white re-key's frame and case gates);
- `historical_backcast_2026_09_20/inputs/acs_mexican_origin.csv`.

## Validation

Current repair (2026-09-30): **9 tests pass**; `rerun_lane.py` with the generator and test commands
returns **IDENTICAL: 13/13, exit 0**. Wrong-count, changed-response, nonfinite and duplicate
exports are rejected before attribution. The original four-test run below is retained as history.

```
$ uv run python3 -m pytest infra/immigration-fiscal/pension_legacy_2026_09_30/ -q
....                                                                     [100%]
4 passed in 2.01s
exit=0
$ uv run python3 scripts/rerun_lane.py infra/immigration-fiscal/pension_legacy_2026_09_30 "uv run python3 {lane}/pension_legacy.py" "uv run python3 -m pytest {lane}/test_pension_legacy.py -q"
[rerun] uv offline (UV_OFFLINE=1)
[rerun] 1/2 rc=0  uv run python3 infra/immigration-fiscal/pension_legacy_2026_09_30/pension_legacy.py
[rerun] 2/2 rc=0  uv run python3 -m pytest infra/immigration-fiscal/pension_legacy_2026_09_30/test_pension_legacy.py -q
[rerun] IDENTICAL: 13/13 files unchanged
exit=0
```

The test file is named as a second rerun command so that the harness does not flag it NOT RUN.

## Log

- 2026-09-30 05:26 JST: lane started; sources fetched and pinned.
- 2026-09-30 05:49 JST: first full run; tests pass (4).
- 2026-09-30 05:51 JST: RESULT drafted.
- 2026-09-30 05:55 JST: final run after the footnote wording was gated. pytest passes 4/4 and `rerun_lane.py` reports IDENTICAL 13/13, both with exit 0.

## v5 case (oct05), 2026-10-05

[2026-10-07: the comparators' IPEDS keys revise this section's matched-union, A1 and difference rows.
`derived/oct05/` now holds the revised figures (matched difference $5.22 / 5.14bn, engine difference $5.75 / 5.96bn),
listed in "v6 case (oct07)" below. The engine union's and the all-residents slice's rows stand.]

[2026-10-05: on main case v5 (`oct05`, `../main_case_2026_10_05/`), the adopted arm gives the engine's union
**$454.6 / 485.1bn** of attributed pension stock and **$22.57 / 23.99bn** of 2024 interest, **$528 / 561 per member** of
the lineage's 42,752,213 (sept29: $421.8 / 447.9bn, $20.94 / 22.15bn, $527 / 558 on 39,712,493). On matched keys the
union exceeds third-plus whites by **$5.32 / 5.24bn** ($124 / 122 per member; sept29 $4.89 / 4.68bn, $123 / 118); the
engine union exceeds them by $5.64 / 5.85bn (sept29 $5.21 / 5.30bn). [CALCULATION: `pension_legacy.py --case oct05` →
`derived/oct05/summary.csv`, arm `adopted`]]

claude-opus-5-5 (v5consC)

**Rules (the case lane's Consumers row: both sides on 42.75M).**
- The groups' line amounts are `legacy_comparators_2026_09_30/derived/group_lines_oct05.csv`. Both union rows carry the
  3,039,720 added people at the case lane's amounts on every line; A1 and the all-residents slice are on 42,752,213.
  The engine union's amounts are gated against the white lane's `engine_lines_oct05.json` (the case, not its union dump).
- Per member divides by 42,752,213, and the per-head key (defense, enterprises) is 0.117175 × 42,752,213 / 39,712,493
  = 0.126144, gated for every group.
- [ASSUMPTION] **The added people follow the union's headcount path** back to 1946, so the time factors are
  unchanged (0.828 state-local, 0.812 federal). The back-cast, debt legacy and legacy comparator lanes carry them on
  the identified third-plus generation's path instead, measured only for 2005–2024 (`historical_backcast_2026_09_20/inputs/cps_g3plus_path.csv`), where most
  of this kernel's weight before 2005 has no measurement. On that path, with its 2005 ratio to the union's path held
  before 2005, the time factor is 0.723 state-local and 0.707 federal, and the union's interest would be about
  **$0.21 / 0.23bn lower** [CALCULATION: scratch check, not a lane output; the added people's part approximated as the
  oct05 less sept29 interest by plan].

| Adopted arm, $bn (per member $) | oct05 | sept29 |
|---|---:|---:|
| Engine union, stock | 454.6 / 485.1 | 421.8 / 447.9 |
| Engine union, interest | **22.57 / 23.99** ($528 / 561) | 20.94 / 22.15 ($527 / 558) |
| Matched (rough) union, interest | 22.25 / 23.37 ($520 / 547) | 20.61 / 21.53 ($519 / 542) |
| Third-plus whites (A1), interest | 16.93 / 18.14 ($396 / 424) | 15.72 / 16.85 ($396 / 424) |
| All-residents slice, interest | 20.22 / 21.38 ($473 / 500) | 18.78 / 19.86 ($473 / 500) |
| **Matched union − A1, interest** | **5.32 / 5.24** ($124 / 122) | 4.89 / 4.68 ($123 / 118) |
| Engine union − A1, interest | 5.64 / 5.85 ($132 / 137) | 5.21 / 5.30 ($131 / 133) |

[CALCULATION: `derived/oct05/summary.csv`; every arm in `derived/oct05/attribution.csv`]

The slices' interest grows by 7.67%, about the count's ratio (1.076543), and the engine union's by 7.8%, so the added
people's attributed interest per head is close to the identified union's and per-member figures barely move. The
other arms move alike: the simple arm gives the engine union $27.33 / 29.05bn (sept29 $25.35 / 26.82bn) and the
average-cost arm $34.64bn at the low end (sept29 $32.14bn).

**Gates.** `pension_legacy.py --case oct05` exits 0 with every gate of the sept29 run (the BEA, Z.1 and Financial Report
parses; the export's counts, lines, responses and engine amounts against the case; the per-head key). The sept29 run
rewrites `derived/` byte for byte, and the lane's tests pass, 9 of 9 (the rebuild test now compares the files in
`derived/` only, since the oct05 outputs sit in `derived/oct05/`). `rerun_lane.py` with the sept29 run, the oct05 run
and pytest: **IDENTICAL 22/22, exit 0** (2026-10-06 00:44:02–00:44:06 JST).

**Reproduce (oct05)**, after `group_lines.py --case oct05` and the white lane's oct05 dumps:

```sh
uv run --no-project python3 infra/immigration-fiscal/pension_legacy_2026_09_30/pension_legacy.py --case oct05
```

New: `derived/oct05/` with the nine files of `derived/`. `pension_legacy.py` gained `--case` and `use_case()`;
`test_pension_legacy.py` lists only the files in `derived/`.

## v6 case (oct07), 2026-10-07

[2026-10-07: on main case v6 (`oct07`, `../main_case_2026_10_07/`), the adopted arm gives the engine's union
**$452.7 / 484.4bn** of attributed pension stock and **$22.46 / 23.95bn** of 2024 interest, **$525 / 560 per member** of
the lineage's 42,752,213 (oct05: $454.6 / 485.1bn, $22.57 / 23.99bn, $528 / 561). On matched keys the union exceeds
third-plus whites by **$5.41 / 5.39bn** ($127 / 126 per member); the engine union exceeds them by $5.62 / 5.90bn. The
comparators now key Pell and public higher education by IPEDS, a defect fix for oct05 and oct07. It moves oct05's
matched difference from $5.32 / 5.24bn to $5.22 / 5.14bn and its engine difference from $5.64 / 5.85bn to
$5.75 / 5.96bn; sept29 keeps its keys and its outputs. [CALCULATION: `pension_legacy.py --case oct07` →
`derived/oct07/summary.csv`; `--case oct05` → `derived/oct05/summary.csv`; arm `adopted`]]

claude-opus-5-5 (prop-b, v6 consumer)

**Rules.**
- The groups' line amounts are `legacy_comparators_2026_09_30/derived/group_lines_oct07.csv`, built on the white lane's
  oct07 run (`../white_replacement_2026_09_28/`, d2554cb2). The engine union's amounts are gated against that lane's
  `engine_lines_oct07.json`. Per member divides by 42,752,213, and the per-head key 0.126144 is gated for every group:
  v6 does not move the lineage's count.
- [ASSUMPTION] **Retiree health scales a line, overlay included.** Item 2 sets ten lines' national totals (engine
  `scaleLine`). Three of them carry a state-price overlay: public order 519.153 → 521.203, health 306.539 → 308.359 and
  recreation 54.331 → 54.484. A group's base amount scales with its line, but the case leaves the overlay unscaled. The
  lane divides each overlay by the line's unscaled national, as if the item scaled the overlay too, so a use share does
  not move when every cost on the line rises alike. The overlay gate takes the national from the payload's
  national-scale edits (`SCALED` in `use_case()`; ten lines on oct07, none on oct05) and stops on a repeated line or
  on a scale edit that also carries a shift (`by`). Dividing by the scaled national instead moves a share by at most 5.2e-5, and any group's or difference's
  interest by at most $0.0036bn in the adopted arm ($0.0044bn in any arm). [CALCULATION: scratch variant of
  `pension_legacy.py`, not a lane output]
- The items reach the lane only through the export's line amounts:
  - item 3 (the added people at their measured ages) moves both union rows;
  - item 4 (user fees and the education keys) moves the engine union at the engine's amounts. Its education cell
    shift, −$3.61bn, is the tuition term (+$1.84bn) plus public colleges keyed by use (−$5.45bn). Its education share
    falls from 0.1701 to 0.1681 at the low end and from 0.1773 to 0.1764 at the high end. Its health terms (+$0.64bn),
    less the added people's ages (−$0.24bn), raise its health share from 0.0676 to 0.0688. The rough union takes health
    at the engine's amounts (the white lane's
    rule 5), and the rough union and A1 take the tuition term on education by the white lane's rule (+$1.8446bn and
    +$0.3495bn, `ipeds_terms_oct07.csv`). Item 4's K-12 weight parts sit on the school-correction lines
    (`school_reprice`, `college_rekey`), which this lane has never read;
  - item 1 (the 2026 Trustees inputs) touches no service line;
  - item 2 scales whites' and the all-residents slice's base amounts and nationals alike, so their shares move only by
    A1's tuition term.
- [ASSUMPTION] **Education is a share net of tuition.** Item 4 books tuition the group pays short of its use on the
  education line, so the lane's education share charges public colleges' pension cost by use less tuition, as the case
  charges colleges. Without the tuition term on every group, the engine and matched unions are $0.105bn lower, A1
  $0.020bn lower, and both differences $0.085bn lower (matched $5.32 / 5.31bn). [CALCULATION: scratch variant]
- **Hospitals, beside.** The engine and rough unions carry item 4's health terms. The white lane prices the comparators'
  hospital term beside (key mismatch), so A1's health line has none. With A1's beside term (−$2.6507bn) on its health
  line, A1's interest falls $0.227bn and the matched difference is $5.64 / 5.62bn. With the union's terms off its rough
  row instead, the matched difference is $5.35 / 5.34bn. [CALCULATION: scratch variants]
- **The comparator keys (oct05 and oct07; sept29 keeps its keys).** These follow the white lane's "The IPEDS keys".
  Public higher education goes on each group's measured use. At both ends this lowers the rough union's education amount
  by $3.6199bn and A1's by $1.8852bn on oct05 (the use terms are −$3.6354bn and −$1.8933bn on oct07). Pell moves on
  other federal benefits, which no plan's function mix uses. The college-capital part sits in the export's cost row,
  which this lane does not read. No other input to this lane changes.
- The headcount path stays the union's, as on oct05 [ASSUMPTION]. On oct05 the G3+ path lowered the union's interest
  by $0.21 / 0.23bn; that check is not rerun here.

| Adopted arm, $bn a year | oct05, IPEDS keys | **oct07** |
|---|---:|---:|
| Engine union, stock | 454.6 / 485.1 | 452.7 / 484.4 |
| Engine union, interest (per member $) | 22.57 / 23.99 ($528 / 561) | **22.46 / 23.95** ($525 / 560) |
| Matched (rough) union, interest | 22.04 / 23.17 | 22.25 / 23.44 |
| Third-plus whites (A1), interest | 16.82 / 18.03 | 16.84 / 18.05 |
| All-residents slice, interest | 20.22 / 21.38 | 20.22 / 21.38 |
| **Matched union − A1, interest** (per member $) | 5.22 / 5.14 ($122 / 120) | **5.41 / 5.39** ($127 / 126) |
| Engine union − A1, interest (per member $) | 5.75 / 5.96 ($134 / 139) | 5.62 / 5.90 ($131 / 138) |

[CALCULATION: `derived/oct05/summary.csv`, `derived/oct07/summary.csv`; every arm in `attribution.csv`. Per member
on 42,752,213. Each printed difference equals its printed parts.]

**Old → new, every case** (adopted arm, interest in $bn a year, low / high):
- **sept29: unchanged.** The white lane kept sept29's keys, so `group_lines_sept29.csv` and `engine_lines_sept29.json`
  are HEAD's, and `derived/` rebuilds byte for byte (9 of 9).
- **oct05, as published 2026-10-05 → on the IPEDS keys.** Only the rough union's and A1's education rows move, by the
  same amount at both ends:
  - rough union 22.249 / 23.375 → 22.042 / 23.167 (−0.207);
  - A1 16.929 / 18.139 → 16.821 / 18.031 (−0.108);
  - matched difference 5.320 / 5.235 → 5.220 / 5.136 (−0.099);
  - engine difference 5.641 / 5.850 → 5.749 / 5.958 (+0.108).

  The rough union's education share falls from 0.1679 to 0.1650 at the low end (0.1701 to 0.1671 at the high end), and
  A1's from 0.1073 to 0.1058. The engine union, the all-residents slice and every national input are unchanged. Across
  the eight arms the matched difference now runs 4.49–6.30 (published 4.58–6.42).
- **oct07 against oct05 on the IPEDS keys:**
  - engine union −0.108 / −0.041: education −0.135 / −0.062, health +0.033;
  - rough union +0.209 / +0.276: education +0.176 / +0.249 (the tuition term +0.105; the rest is mostly item 3's
    ages), health +0.039;
  - A1 +0.020 (the tuition term);
  - matched difference +0.189 / +0.256;
  - engine difference −0.128 / −0.061.

  Across the eight arms the matched difference runs 4.72–6.53. The average-cost arm gives the engine union $34.53bn at
  the low end (oct05 $34.64bn).

**Gates.** `pension_legacy.py --case oct07` exits 0 with every gate of the oct05 run, the overlay nationals gated at the
payload's scale edits. The sept29 run rewrites `derived/` byte for byte. Against HEAD, the oct05 run changes only the
rows named above, in `group_shares.csv`, `by_line.csv`, `attribution.csv`, `opeb_federal.csv` and `summary.csv`;
`measured_2024.csv`, `domestic_interest.csv`, `function_mix.csv` and `headcount_path.csv` are byte for byte. The lane's
tests pass, 9 of 9. Inputs read (sha256 prefixes): `group_lines_oct05.csv` 112eb192c7e3, `group_lines_oct07.csv`
2ea07aa1ea9f, `engine_lines_oct07.json` 1d17cb78d2e2, the case's `corrections.json` f8d346aacf05 (the committed
payload).

**Reproduce (oct07)**, after `group_lines.py --case oct07` and the white lane's oct07 dumps:

```sh
uv run --no-project python3 infra/immigration-fiscal/pension_legacy_2026_09_30/pension_legacy.py --case oct07
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/pension_legacy_2026_09_30 \
  "uv run --no-project python3 {lane}/pension_legacy.py" "uv run --no-project python3 {lane}/pension_legacy.py --case oct05" \
  "uv run --no-project python3 {lane}/pension_legacy.py --case oct07" \
  "uv run --no-project python3 -m pytest {lane}/test_pension_legacy.py -q"
```

New: `derived/oct07/` with the nine files of `derived/`; `derived/oct05/` rebuilt on the IPEDS keys. `pension_legacy.py`
gained the oct07 entry in `CASES` and the items' national-scale edits in `use_case()`.

Log (times from `date`):
- 2026-10-07 14:07–14:09 JST: code ready; candidate checked on the candidate exports (oct07 run exit 0; sept29 and oct05
  byte for byte against HEAD).
- 17:02:37 JST: prop-d reports the comparator exports final in all three cases (sept29 unchanged).
- 17:04:13–17:04:27 JST: the three runs in place, each exit 0. Checked against HEAD with a row diff: sept29 9 of 9 byte
  for byte; oct05 confined to the rough union's and A1's education rows and their aggregates.
- 17:06:17–17:06:19 JST: pytest, 9 passed.
- 17:06:30–17:06:34 JST: `rerun_lane.py` with the four commands above: IDENTICAL, 31/31 files, exit 0.
- 17:07:37–17:21:03 JST (output file times): scratch variants on the final inputs: the overlay divisor (17:07:37),
  tuition off (17:14:42) and the hospital terms (17:20:46, 17:21:03). At 17:08:27 the `CASES` comment's bounds were
  updated to the final inputs' 5.2e-5 and $0.0044bn (adopted arm $0.0036bn), a comment-only edit.
- 17:32:34–17:32:38 JST: `rerun_lane.py` after that edit, the same four commands: IDENTICAL, 31/31 files, exit 0
  (pytest 9 passed inside it). The outputs are newer than every script.

## Revisions

- 2026-09-30, source verification: corrected both comparator frames and added a matched union. The original $4.88–4.94bn difference mixed keys and counts; the current matched difference is $4.89 / $4.68bn, while the engine-union difference is $5.21 / $5.30bn. National inputs and the engine union are unchanged. Corrected cash-payment and no-overlap claims, and distinguished employer normal cost from compensation including service charges. The [decision](../../../decisions/2026-09-30-legacy-comparisons-separate.md) keeps the two legacies separate. Earlier logs and the original by-line description are preserved as historical evidence.
- Output contract: summary and detailed tables add `mexican_origin_rough` and the summary adds its matched white difference. The three `*_normal_cost_employer` measurement labels are renamed `*_employer_pension_compensation` to include service charges explicitly; a repository search found no consumers of the old measurement labels.
- 2026-10-07, comparator keys: the comparators of oct05 and oct07 key Pell and public higher education by IPEDS
  ([white lane, "The IPEDS keys"](../white_replacement_2026_09_28/RESULT.md), d2554cb2). The rough keys gave every
  group the CPS college key for public colleges and charged Pell by Social Security receipts; the fix was decided in the
  v6 propagation. On oct05 it moves the matched difference from $5.32 / 5.24bn to $5.22 / 5.14bn and the engine
  difference from $5.64 / 5.85bn to $5.75 / 5.96bn. sept29 keeps its keys, and its outputs are unchanged. See
  "v6 case (oct07)".
