claude-opus-5-5
**Verdict:** Setting the Mexico-born unauthorized to outside totals moves the adopted set at specifications 48 / 11 as follows: +$1.45 / +$1.37bn at Pew's 4.3M, −$1.14 / −$1.10bn at DHS's 4.8M, and −$2.91 / −$2.80bn at CMS's 5.1M. That gives $372.9–436.2bn, $370.3–433.7bn and $368.5–432.0bn, so every target changes the printed $371.4–434.8bn at one decimal. This arm sits beside the case and is not adopted.

The case's own count is 4.607M, so Pew lowers it and DHS and CMS raise it. More unauthorized makes the set cheaper. The pension accrual credits an unauthorized worker-year with 10% of the accrual on the 52.6% of its taxes that are on the books. That saving, together with the EITC the movers lose, outweighs the income and payroll taxes that go off the books.

- **Cash set** ($294.7–361.8bn): the moves are small: −0.86 / −0.84, −0.06 / −0.06 and +0.12 / +0.12.
- **Proportional alternative**: it moves the set by +1.66 / +1.57, −0.90 / −0.85 and −2.30 / −2.18.
- **Medicaid** does not move.

Tags: `[DATA]` CPS ASEC 2025 and the cited lanes' derived files; `[CALCULATION]` this lane's scripts and every figure in `derived/`; `[INFERENCE]` and `[TRAINING-DATA]` where marked. The instrument is an LLM working on a politically charged question (`notes/llm-bias-caveat.md`). The counts and prices below are mechanical.

## The arms

Each figure is in $bn, the two fill-in methods averaged, at specifications 48 / 11. In every arm both methods keep their ends at 48 / 11, so each figure is also the arm's band. A plus sign raises the account's cost. [CALCULATION: `derived/arm_bands.csv`]

| Target | Mexico-born unauthorized | Rule | Set | Move | Printed | Cash set | Move |
|---|---:|---|---|---|---|---|---|
| Adopted case | 4.607M | the case's flag | 371.4146 / 434.8410 | — | $371.4–434.8bn | 294.7011 / 361.8175 | — |
| Pew, 2023 | 4.3M | tiers (earliest arrivals legal first) | 372.8660 / 436.2156 | **+1.4514 / +1.3746** | $372.9–436.2bn | 293.8428 / 360.9728 | −0.8583 / −0.8447 |
| | | proportional | 373.0741 / 436.4147 | +1.6595 / +1.5737 | $373.1–436.4bn | 294.1615 / 361.2606 | −0.5396 / −0.5569 |
| DHS, January 2022 | 4.8M | tiers (weakest legal signal first) | 370.2796 / 433.7419 | **−1.1350 / −1.0991** | $370.3–433.7bn | 294.6435 / 361.7565 | −0.0576 / −0.0610 |
| | | proportional | 370.5154 / 433.9890 | −0.8992 / −0.8520 | $370.5–434.0bn | 294.9634 / 362.0931 | +0.2623 / +0.2756 |
| CMS, 2024 | 5.1M | tiers | 368.5058 / 432.0413 | **−2.9088 / −2.7997** | $368.5–432.0bn | 294.8199 / 361.9421 | +0.1188 / +0.1246 |
| | | proportional | 369.1115 / 432.6592 | −2.3031 / −2.1817 | $369.1–432.7bn | 295.3711 / 362.5215 | +0.6700 / +0.7040 |

The next table splits the set's move by channel under the tiers rule. The parts add to the move. [CALCULATION: `derived/arm_lines.csv`, signed as cost]

| Channel | Pew | DHS | CMS |
|---|---|---|---|
| Income taxes (federal, state and local, other personal) | −0.429 / −0.404 | +0.093 / +0.094 | +0.263 / +0.267 |
| Payroll taxes (OASDI, HI, self-employment, other contributions) | −0.723 / −0.706 | +0.234 / +0.227 | +0.734 / +0.726 |
| Refundable credits (EITC, ACTC) | +0.236 / +0.212 | −0.386 / −0.385 | −0.867 / −0.860 |
| Social Security accrual | +1.828 / +1.738 | −0.728 / −0.688 | −2.103 / −1.999 |
| Part A accrual | +0.482 / +0.482 | −0.350 / −0.350 | −0.925 / −0.925 |
| Sales taxes, duties, transfers received, roads, capital | +0.057 / +0.053 | +0.002 / +0.003 | −0.011 / −0.009 |
| **Move** | **+1.451 / +1.375** | **−1.135 / −1.099** | **−2.909 / −2.800** |

The cash set's move equals the sum of every row except the two accruals, to 1e-4. On the cash set, Social Security and Part A are the benefits paid in 2024, and no status input touches those benefits.

The DHS movers are low earners. Their EITC is $981 a head and their ACTC $469, while their federal income tax is $815. On the cash set, the taxes they stop paying and the credits they lose nearly cancel.

## The frame

**The count.** Every count uses the frame of the case's status stack:
- CPS ASEC 2025 persons in the group, civilian;
- the account's row-4 weights, which put the Mexico-born outside California and Texas at their ACS 2024 level;
- the state-aware flag, which reads Medicaid as no status signal at the state-ages of `STATUS_BLIND_2024`.

On that frame the Mexico-born unauthorized number **4,607,453**. That is the CPS lane's 4.607M [SOURCE: `cps_imputation_keys_2026_09_23/RESULT.md:757`]. Two other counts in the record use other frames:
- 5.227M: the same flag on the published CPS weights;
- 4.074M: the CPS residual scaled to the ACS noncitizen count [SOURCE: `mexborn_count_2026_09_23/RESULT.md:228`].

**The targets** are the published Mexico-born totals [SOURCE: `mexborn_count_2026_09_23/RESULT.md:243`]:
- Pew 4.3M (2023);
- DHS 44% of 10.99M (1 January 2022);
- CMS 5.1M (2024).

The DHS figure is 4.836M unrounded. The arm uses the brief's 4.8M. At 4.836M the DHS move would be about −1.35 / −1.30 [INFERENCE: linear in T1's fraction].

**What moves.** Each arm re-assigns status among the group's Mexico-born noncitizens, who number 7.187M on the frame. Status moves; head counts do not. CMS and DHS add coverage for people the survey misses, which the count lane puts at 0.2–0.3M for Mexico [SOURCE: same line]. This arm instead assigns that part to status among people already counted. The targets are also dated 2022–2024, against a March 2025 frame. A target reached here is a status mix, not a population check [INFERENCE].

## Who moves: the rule and its alternative

**The rule** ranks movers by the residual method's own criteria. That method calls a noncitizen legal on any of its signals (a)–(i) [SOURCE: `status_impute_2026_09_16/RESULT.md:53-63`]. Whole tiers move in order. The tier that would overshoot moves a uniform fraction θ of its members, so each total is hit exactly and no record order decides who moves. [CALCULATION: `derived/tiers.csv`, `derived/movers.csv`]

**Raising (DHS, CMS): legal to unauthorized, weakest legal signal first.**
- **T1, legal only through the Medicaid clause** (392,829 persons, 236 records). These Mexico-born noncitizens become unauthorized once the clause is dropped at every state-age, which is the status lane's `no_medicaid_rule`. The adopted flag already drops the clause where 2024 coverage ignored status.
  - The status lane calls receipt "a much weaker legal-status signal than it was in Borjas's 2012–13 sample" [SOURCE: `status_impute_2026_09_16/RESULT.md:98-100`].
  - In unlisted states, 38% of the reports behind the clause are donor-imputed [SOURCE: `california_medical_status_2026_09_23/RESULT.md:69`].
  - Profile: 99% report Medicaid and none live in California. Mean wage is $17.6k and mean federal liability $815.
- **T2, legal only through clause (i)**, a legal or citizen spouse, once the Medicaid clause is dropped (943,444 persons). The back-cast lane runs the same variant as `borjas_own` [SOURCE: `backcast_pandemic_measured_2026_09_28/measure_shares.py:118`]. Mean wage is $33.7k.
- **How far each target reaches.** DHS moves 49.0% of T1. CMS moves all of T1 and 10.6% of T2. Neither reaches T3, everyone else legal (1,243,134 persons).

**Lowering (Pew): unauthorized to legal, earliest arrival first.**
- Rule (a) presumes pre-1980 arrivals legal, so the next arrival band, 1980–81, is the next most likely to be legal. It falls in IRCA's window, continuous residence since before 1982 [TRAINING-DATA]. Then come 1982–83 and so on.
- Pew moves the 1980–87 arrivals in full (238,097 persons) and 54.7% of the 1988–89 band (69,356).
- The movers average about 55 years old, with mean wages of $23–44k by band.

**The alternative** applies one fraction to everyone on the moving side:
- raising: every imputed-legal Mexico-born noncitizen of the group (2,579,407) becomes unauthorized with probability 7.46% (DHS) or 19.10% (CMS);
- lowering: every imputed unauthorized person becomes legal with probability 6.67% (Pew).

This keeps each status group's composition, so it prices the calibration as if the residual's ranking carried no information at the margin. Its movers earn more and draw less EITC than the rule's, so it moves the set by 0.2–0.6bn less when raising the count. When lowering, it moves the set 0.2bn more.

**Fractional θ.** A fractional θ counts a person unauthorized with weight θ in every input, linearly:
- the six scaled keys and the ACTC at (1 − θ) + θs, where s is the on-books share for the person's origin;
- the EITC at 1 − θ;
- the pension credit at (1 − θ) + θ × s × 0.10;
- the payroll item's four industries at (1 − θ) + θ(1 − slope).

At θ = 0 or 1, each formula is the case's rule bit for bit (gates 4, pension and payroll).

## The status-dependent inputs, recomputed

1. **The status stack** (audit row 2), in `calibrate.py`.
   - The rules zero the EITC. They scale by the on-books share the ACTC, federal and state liability, capped and uncapped wages, self-employment payroll and the FICA-worker count [SOURCE: `cps_imputation_keys_2026_09_23/combine_status.py:79-89`].
   - The shares are 0.5262685 for the Mexico-born and 0.5500608 for other Latin American-born, the on-books lane's central [DATA: `onbooks_share_2026_09_23/derived/onbooks_split.csv:45`].
   - The stack is rebuilt on the row-4 weights three times: for the rules alone, the union-matched hot deck and its pooled control, each hot deck over 5 seeds. It uses the CPS lane's own translation: MEPS and school keys, the justice per-head part, the uncompensated-care shift, the non-PTC refundable part.
   - The case reads the stack directly and through every stack factor: CBO's re-key, the medical, school and benefit shifts, and the IRS income-tax key.
2. **The pension accrual**, in `pension.py`, on the pension lane's frame. That frame uses the published CPS weights, as the case's ratio does. The case multiplies ratio_net by its own OASDI receipts, which the stack already moves, and adds the Part A accrual as a fixed amount. [CALCULATION: `derived/pension.json`]

   | | ratio_net | Part A accrual ($bn) | unauthorized share of the group's on-books OASDI tax |
   |---|---:|---:|---:|
   | adopted | 0.97367 | 41.137 | 8.67% |
   | Pew | 0.98538 | 41.619 | 8.04% |
   | DHS | 0.96864 | 40.787 | 8.95% |
   | CMS | 0.95950 | 40.212 | 9.48% |

   The self-employment OASDI share moves by at most 6.4e-5. The tax on 2024 benefits reads no status input and stays.
3. **The payroll-compliance item** (item 6a), in `payroll.py`. Its ratios are built on the paper flag and calibrated to the case's stacks. They are recomputed with the payroll lane's own frame and formulas:
   - the movers move on the paper flag by their change from the adopted flag, clipped to [0, 1];
   - the calibration reads the arm's stacks.

   The largest ratio change is 6.2e-4 (Pew), 5.6e-4 (DHS) and 9.4e-4 (CMS). These changes move the arms by up to 0.05bn. [CALCULATION: `derived/payroll.json`]
4. **Medicaid does not move.** The group's Medicaid amount is 117.7434 / 119.7361 in every arm, identical to the last digit, and SNAP likewise. The case keys Medicaid by use: the MEPS payer means and the uninsured-use shift. The status rules touch only the EITC, the ACTC and the six keys above. [CALCULATION: `derived/summary.json`, `group_amounts_at_48_11_bn`]

**Not recomputed**, because none enters the set or the cash set:
- the stacks for audit row 3 and the Medicare key fix, which feed only rows beside the case;
- the low and high on-books stacks, which feed only range rows;
- v3's gross pension switch, which is superseded;
- the payroll item's within-group r_cal, since the set reads r_cal_raw.

## Gates

All gates pass. Each would stop its script with `[BLOCKED]` before anything is written. `calibrate.log` shows two `[DEGRADED]` lines. They are the status lane's standing note on the paper flag's Medicaid clause, and the arm uses the state-aware flag that note points to.

- **Flags** (`calibrate.py` gate 1). The paper and state-aware flags reproduce the California lane's union counts, 4.5671M and 5.2265M. On the row-4 weights the adopted flag gives 4,607,453, the CPS lane's 4.607M. Every unauthorized union member is a Mexico-born noncitizen. Row 4 with unit factors returns the published weights bit for bit.
- **Targets** (gate 2). Each arm's total equals its target within 1,000 people: the miss is 0.000 in every arm (`derived/arms.csv`). Only Mexico-born noncitizens of the group move.
- **Hot deck** (gate 3). Every frame reproduces `run_hotdeck.py`'s stored shares to 1e-12.
- **Stacks** (gate 4). With the adopted flag, the rebuilt `row4+status_state_aware|central|{b_hotdeck_union_matched, b_matched_over_pooled, audit_rules_alone}` equal the case's stored stacks cell for cell, with a largest difference of 0.0.
- **Pension.** With the adopted flag, the recomputed values equal `summary.json` at 9ea1beb, with a largest difference of 6.9e-18. The values checked are ratio_net, the gross ratio, the future share, Part A and the self-employment share.
- **Payroll.** With the adopted flag and the case's stacks, r_cal_raw equals `items.json` on 14 lines × 2 allocations, with a largest difference of 0.0.
- **Price** (`price.cjs`).
  - The adopted flag through the rebuilt inputs gives 371.414600 / 434.840959 and 294.701076 / 361.817482. That reproduces the case's 371.4146 / 434.8410 and 294.7011 / 361.8175 at 1e-4, with the ends at 48 / 11 in both methods.
  - A child process with no substitution gives the same, and the two agree at every specification of both sets (max |diff| 0.0).
  - Every substituted arm reads the stacks, the pinned pension summary and the payroll items once each. Every arm moves the group's federal income tax receipt.
  - The child processes answer those three reads from this lane and report the CPS lane's cache absent, so the vendored copy is read. They stop on any fs write.
- **Rerun.** `uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/status_calibration_2026_09_30 "uv run --no-project python3 {lane}/calibrate.py" "uv run --no-project python3 {lane}/pension.py" "uv run --no-project python3 {lane}/payroll.py" "node {lane}/price.cjs"` ran twice in a row, and both passes reported **IDENTICAL: 14/14 files unchanged** (all four steps rc=0).

## Files

- `calibrate.py` builds the frame, the flags, the tiers, the arms' θ and their stacks. It writes `derived/arms.csv`, `tiers.csv`, `movers.csv` and `stacks.json`.
- `pension.py` computes the pension numbers per arm and writes `derived/pension.json`.
- `payroll.py` computes item 6a's ratios per arm and writes `derived/payroll.json`.
- `price.cjs` prices each arm through `../main_case_2026_09_29/package.cjs`. It writes `derived/arm_bands.csv`, `arm_lines.csv` and `summary.json`.
  - `arm_lines.csv` gives each engine line's change in `effect_bn`, where a plus sign lowers the cost, and the capital return's change as a cost.
  - An arm's cost move is the capital change minus the sum of the line changes.

Run the scripts in the order above from the repository root, as in the rerun command. Logs sit in the ignored `_cache/`.

## Log (append-only; times from `date` or file times)

- 2026-09-30 00:19:57 JST: brief received and the lane started.
- 02:35:10 JST: final `calibrate.py` run, file time of `_cache/calibrate.log`; `pension.py` 02:35:34, `payroll.py` 02:40:06.
- 02:42:13 to 02:44:30 JST: rerun pass 1, IDENTICAL 14/14.
- 02:44:30 to 02:48:09 JST: rerun pass 2, IDENTICAL 14/14.
- 03:21:05 JST: RESULT.md written, with every figure checked against `derived/`. Nothing committed.
