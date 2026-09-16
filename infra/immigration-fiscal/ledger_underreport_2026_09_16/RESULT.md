**Verdict:** The gap survives. **No arm built from published under-reporting ratios moves the Mexican-second-generation versus third-plus-non-Hispanic-white gap by more than $269** on either allocation, against a baseline of −6,066 (taxes minus selected transfers) and −8,286 (extended balance). The largest literature-grounded move is the false-negative arm at **+269** (narrowing, i.e. favourable to the Mexican second generation) on `equal_all_members`; the differential arm moves it **−151** (widening) on `equal_adults_18plus`. Nothing crosses $500 and nothing comes near flipping the sign. The mechanical reason is that the Mexican second generation *receives less* in selected transfers than the white reference group ($1,700 versus $2,599 per adult), so scaling receipt upward adds more dollars to the reference group's transfer column than to theirs, and the correction runs in the gap's favour rather than against it.

Model self-report: **claude-opus-5[1m]** (Opus 5, 1M context).

[DATA] CPS ASEC 2025 public-use microdata, 160-replicate SDR. [SOURCE: https://www.nber.org/papers/w35680] [SOURCE: https://www.nber.org/papers/w32860] [SOURCE: https://www.nber.org/papers/w21399] [INFERENCE] every arm is an accounting scenario, not a measurement.

## Gate A — reproduction before touching anything: PASS

```
-- GATE A: reproduce the peer lane's extended ledger before touching anything --
   extended balance gap, equal_all_members : -8,286 (se 443)   expected -8,286 (se 443)   deviation -0.23
   taxes-minus-transfers gap, same          : -6,066 (se 353)   expected -6,066 (se 353)   deviation +0.17
   [gate A] PASS (within $50 of -8,286)
```

`underreport.py` imports `extend_ledger.build()`, which itself imports `prepare()`, `allocate()` and `estimate()` from `analyze_cps_fiscal_2025.py`. All of the base generator's integrity gates run unchanged: the federal refundable-credit identity, SPM-unit dollar conservation, head-weight agreement, unit-field constancy. Nothing is re-implemented, so the reproduction is exact to 23 cents.

## Headline result

Mexican second generation minus third-plus non-Hispanic white, annual dollars per adult aged 25–64, income year 2024. SDR standard error in parentheses; "move" is the change from the reported-receipt baseline, positive meaning the gap narrows.

### Taxes minus selected transfers (baseline −6,066)

| arm | equal_all_members | move | equal_adults_18plus | move |
|---|---|---|---|---|
| baseline, reported receipt | −6,066 (353) | — | −7,625 (462) | — |
| (a) proportional, base ratios | −5,973 (365) | **+93** | −7,630 (478) | −5 |
| (a) proportional, in-kind programs also scaled | −6,020 (366) | +46 | −7,734 (479) | −109 |
| (a) proportional, w21399 2000–12 vintage | −5,947 (365) | +119 | −7,589 (477) | +36 |
| (b) false negative, 50-draw Monte Carlo | −5,797 (354) | **+269** | −7,385 (464) | +241 |
| (c) differential, receipt-rate ratios | −6,103 (367) | −37 | −7,776 (480) | **−151** |
| (c) differential, dollar ratios | −6,076 (367) | −10 | −7,725 (479) | −100 |
| bound: uniform 0.5 on every transfer (**not a literature value**) | −5,167 (409) | +899 | −6,911 (520) | +715 |

### Extended balance (baseline −8,286)

| arm | equal_all_members | move | equal_adults_18plus | move |
|---|---|---|---|---|
| baseline, reported receipt | −8,286 (443) | — | −10,633 (587) | — |
| (a) proportional, base ratios | −8,193 (452) | **+93** | −10,638 (600) | −5 |
| (a) proportional, in-kind programs also scaled | −8,240 (453) | +46 | −10,742 (604) | −109 |
| (a) proportional, w21399 2000–12 vintage | −8,167 (452) | +119 | −10,598 (599) | +36 |
| (b) false negative, 50-draw Monte Carlo | −8,017 (444) | **+269** | −10,393 (589) | +241 |
| (c) differential, receipt-rate ratios | −8,323 (453) | −37 | −10,784 (601) | **−151** |
| (c) differential, dollar ratios | −8,297 (453) | −10 | −10,733 (600) | −100 |
| bound: uniform 0.5 on every transfer (**not a literature value**) | −7,387 (487) | +899 | −9,919 (634) | +715 |

Monte Carlo sd of the arm (b) gap across 50 draws: **50** on `equal_all_members`, **52** on `equal_adults_18plus`. The draw-to-draw noise is a fifth of the arm's own effect and an eighth of the SDR sampling error, so 50 draws is ample.

**Signs.** Arms (a) and (b) *narrow* the gap. Arm (c) *widens* it, because Hispanic recipients under-report Social Security and UI more than white recipients do, so a correction that respects the ethnic pattern adds relatively more to the Mexican column — but SNAP runs the other way (Hispanic under-reporting is slightly *less* severe than white), and the net is −37 to −151. The two families nearly cancel.

**Headroom bound.** The last row assumes the CPS captures exactly half of every dollar of every transfer, Social Security included, whose measured bias is 8 percent. That is far outside anything published and it still leaves an extended gap of −7,387. Under-reporting cannot be made to carry more than roughly $900 of the −8,286 under *any* proportional correction, because the entire reported transfer difference between the two groups is only $899 per adult.

## Why the correction runs the "wrong" way

```
group                            transfers, reported   transfers, scaled    extended balance   vs reported
third_plus_nh_white                            2,599               3,181              15,402          -582
all_native                                     2,639               3,254              13,650          -616
all_second_gen                                 1,990               2,478              15,171          -487
mexican_second_gen                             1,700               2,189               7,209          -489
mexican_third_plus_selfid                      2,281               2,825               9,161          -545
mexico_born                                    1,106               1,381               4,187          -275
```

Among adults 25–64 the white reference group draws *more* in selected transfers than the Mexican second generation, driven by Social Security (disabled-worker and survivor benefits in this age band) and UI. The base proportional arm adds $582 per adult to the white column and $489 to the Mexican column, so the gap narrows by $93. The −6,066 was never a transfer-side gap: per the peer lane's decomposition it is −6,965 of modeled tax against +994 of *lower* cash transfer receipt. Under-reporting corrections operate on the smaller, wrong-signed component.

## Sources and the exact numbers taken from them

| Ledger program | CPS field | Ratio used | Source, with page |
|---|---|---|---|
| Social Security | `SS_VAL` | 0.919 | w35680 **Table 4, printed p.48**, "Total Net Survey Error for Dollar Amounts and Its Components (as a % of Survey Targets), 2017", Total Net Error row, col (2) OASDI = **−8.1** |
| SSI | `SSI_VAL` | 1.019 | w35680 **Table 4, p.48**, col (5) SSI = **+1.9** (the survey *overstates* SSI dollars) |
| Cash assistance (TANF/GA) | `PAW_VAL` | 0.500 | w21399 **Table 1 Panel A, printed p.34**, CPS row, AFDC/TANF = **−0.500**. Not covered by w35680. |
| Unemployment | `UC_VAL` | 0.577 | w35680 **Table 4, p.48**, col (6) UI = **−42.3** |
| Veterans | `VET_VAL` | 0.620 | w35680 **Table 4, p.48**, col (7) VA Disability = **−38.0** |
| SNAP | `SPM_SNAPSUB` | 0.531 | w35680 **Table 4, p.48**, col (8) SNAP = **−46.9** |
| Energy assistance | `SPM_ENGVAL` | 1.000 base | No linked-administrative estimate published. Sensitivity arm uses SNAP's 0.531 as a proxy. |
| WIC | `SPM_WICVAL` | 1.000 base | No dollar estimate. Sensitivity arm uses w21399 **Table 1 Panel B, p.34**, CPS WIC *months* = **−0.341** → 0.659. |
| School lunch | `SPM_SCHLUNCH` | 1.000 base | No dollar estimate. Sensitivity arm uses w21399 **Table 1 Panel B, p.34**, CPS NSLP *months* = **−0.503** → 0.497. |
| Broadband subsidy | `SPM_BBSUBVAL` | 1.000 base | Program began 2021; nothing published. Sensitivity arm uses SNAP's 0.531. |

Vintage cross-check between the two Meyer teams, CPS dollars: SNAP 0.583 (w21399, 2000–12) against 0.531 (w35680, 2017); OASI 0.914 against 0.951; UI 0.675 against 0.577. Same direction, worsening over time except OASI, which is consistent with w35680's own narrative (§4.2, p.17–18: "Trends over time also generally point toward worsening TSE"). SSI is the one disagreement — 0.838 in w21399 against 1.019 in w35680 — and w35680 explains it directly (p.18: "increasing confusion between SSI and the larger OASDI program", producing a 36.1% false-positive contribution in Table 4 col (5)). The `a_proportional_w21399_vintage` arm runs the whole ledger on the older numbers and moves the gap by +119, so the disagreement does not matter.

### Race and ethnicity, arm (c)

All from w32860, **Table 4, printed p.34**, "Bias in Estimates of Program Receipt and Average Amounts for True Reporting Recipients", and **Table 2, printed p.32**, "False Negative and False Positive Rates by Race and Ethnicity".

| Program | Study, as reported in w32860 | white | Black | Hispanic |
|---|---|---|---|---|
| SNAP receipt rate, survey/admin | Shantz & Fox (2018), 2010–16 CPS | 8.5/14.6 | 21.8/38.8 | 22.9/37.7 |
| SNAP amount, survey/admin | same | 3,409/3,607 | 3,825/4,172 | 3,528/3,638 |
| TANF receipt rate, survey/admin | same | 0.9/1.2 | 4.6/7.1 | 2.0/3.0 |
| TANF amount, survey/admin | same | 2,567/2,196 | 3,420/2,640 | 3,006/1,455 |
| UI receipt rate, survey/admin | Meyer et al. (2023), 2011 CPS | 4.2/5.9 | 4.8/8.3 | 3.4/6.2 |
| UI amount, survey/admin | same | 8,065/8,808 | 6,917/7,990 | 7,556/8,803 |
| OASDI false-negative rate | Bee & Mitchell (2017), 2013 CPS, Table 2 p.32 | 6.4% | 13.6% | 14.3% |

w35680 itself reports **no** race or ethnicity split of its error decomposition; race and ethnicity enter only as covariates in its inverse-probability reweighting (p. 3067 of the extracted text, appendix). w32860 is the only split available, and it is a literature review, so the differential arm inherits samples from 2010–16 rather than 2024.

After renormalisation (below), the ratios actually applied were:

```
   c_differential_receipt_rates
      social_security   white=0.933  black=0.861  hispanic=0.854
      cash_assistance   white=0.533  black=0.461  hispanic=0.474
      unemployment      white=0.628  black=0.510  hispanic=0.484
      snap              white=0.530  black=0.512  hispanic=0.553
   c_differential_dollar_ratios
      social_security   white=0.933  black=0.861  hispanic=0.854
      cash_assistance   white=0.456  black=0.437  hispanic=0.716
      unemployment      white=0.644  black=0.494  hispanic=0.465
      snap              white=0.531  black=0.497  hispanic=0.569
```

## Construction, arm by arm

**(a) Proportional.** Every resource unit's dollars for program *p* are multiplied by 1/ratio_p. Purely multiplicative, so the aggregation convention is irrelevant to the result.

**(b) False-negative only.** For each program the national shortfall is `reported_aggregate × (1/ratio − 1)`, computed as the SPM-unit-weighted sum of unit totals. It is assigned *only* to units reporting zero receipt that pass an eligibility screen, each selected unit receiving the weighted mean reported unit benefit. Selection is Bernoulli at the probability that hits the shortfall in expectation, 50 draws, seed 20260916. SSI gets no assignment because its ratio exceeds 1 — a false-negative mechanism cannot remove an overstatement.

```
   social_security    ratio 0.919  shortfall $   108.2B  mean unit benefit $  27,565  eligible non-reporting units   21.6M  p=0.1821
   ssi                ratio 1.019  no false-negative assignment (survey overstates)
   cash_assistance    ratio 0.500  shortfall $     7.5B  mean unit benefit $   4,852  eligible non-reporting units   20.7M  p=0.0743
   unemployment       ratio 0.577  shortfall $    17.8B  mean unit benefit $   7,137  eligible non-reporting units   24.5M  p=0.1017
   veterans           ratio 0.620  shortfall $    80.8B  mean unit benefit $  24,684  eligible non-reporting units   11.7M  p=0.2807
   snap               ratio 0.531  shortfall $    39.2B  mean unit benefit $   3,145  eligible non-reporting units   47.5M  p=0.2624
```

No program hit the probability cap, so nothing is `[DEGRADED]`; the full shortfall was assignable in every case.

Eligibility screens, all on the SPM resource unit:

| Program | Screen |
|---|---|
| SNAP | `SPM_RESOURCES / SPM_POVTHRESHOLD ≤ 2.0` (broad-based categorical eligibility raises gross-income limits to 200% of poverty in most states) |
| Cash assistance | resource ratio ≤ 1.0 |
| SSI | resource ratio ≤ 1.5 and a member aged 65+ or `PRDISFLG = 1` (not exercised, ratio > 1) |
| Social Security | a member aged 62+ or `PRDISFLG = 1`; no income test |
| Unemployment | a member aged 18–64 with `1 ≤ WKSWORK ≤ 51`, a part-year worker |
| Veterans | a member with `PEAFEVER = 1`, ever served on active duty |

The veterans screen is the one place the obvious field is wrong: `VET_YN` is veterans-*payment recipiency*, not veteran status, so screening on it leaves literally zero non-reporters and silently drops the arm. `PEAFEVER` is the correct field and yields 5,177 unweighted veterans with zero `VET_VAL`. The first run of this script hit exactly that trap and reported `[DEGRADED] no eligible non-reporting units` before the fix.

**(c) Differential.** Per-record ratios `r_g = r_national × s_g / c`, where `s_g` is the published group pattern and `c = A / Σ_g (A_g / s_g)` is chosen so that `Σ_g A_g / r_g = A / r_national` exactly. The national calibration to the administrative target is therefore preserved, and only the *distribution* across groups changes. Cash programs use the recipient's own `PEHSPNON` / `PRDTRACE`; in-kind programs, which carry a single SPM-unit value, use the unit head's. Every race other than Black and every non-Hispanic is folded into "white", since w32860's Asian estimates cover fewer programs.

## Assumptions, stated

1. **The tax side is untouched, and this is correct rather than convenient.** `FEDTAX_AC`, `STATETAX_A` and `FICA` are Census *model* output computed from reported income, not reported tax payments. EITC and ACTC sit inside `FEDTAX_AC` and are likewise modeled. The survey-error literature measures reported *receipt*, which does not apply to a modeled liability.
2. **The arms are biased toward narrowing, and the true answer is therefore at least as adverse as reported.** Adding transfer dollars without re-running the tax model omits the tax those dollars would generate. UI is fully taxable and up to 85% of Social Security is taxable. The reference group receives more of both, so re-running the tax model would raise its modeled tax more, pushing the gap further negative. The reported moves are upper bounds on the narrowing.
3. **Aggregation convention.** National aggregates are SPM-unit-weighted sums of unit totals, not person-weighted sums of person values. Person weights differ within a household while `SPM_WEIGHT` is the head's, so the two differ slightly. The convention is used consistently for the shortfall in arm (b) and the renormalisation in arm (c); arm (a) is invariant to it.
4. **w35680's ratios are 2017; the ledger is income year 2024.** No 2024 linked-administrative estimate exists. The `a_proportional_w21399_vintage` arm substitutes 2000–12 ratios throughout and moves the gap by +119 rather than +93, which is the available evidence on vintage sensitivity.
5. **`VET_VAL` is broader than VA disability compensation.** The ledger field covers all veterans' payments; the 0.620 ratio is measured on VA disability specifically. The implied administrative target ($212B) is above published VA compensation and pension outlays, so the veterans arm is if anything over-corrected — and it corrects a program the white reference group draws more of, which again runs in the gap's favour.
6. **Arm (c) ratios are pooled across 2010–16 samples and two different studies.** Combining a receipt rate with a conditional amount is not the same as a dollar aggregate, because the survey aggregate includes false positives who have no administrative amount. The `c_differential_dollar_ratios` variant makes that approximation explicit; the `c_differential_receipt_rates` variant avoids it by using the extensive margin alone, which w35680 finds is the dominant channel (Table 4, p.48: false negatives are −31.7 of pensions' −44.0, −32.8 of UI's −42.3, −21.6 of SNAP's −46.9).
7. **Earnings under-reporting is not addressed.** w35680 covers transfer and pension receipt, not wage and salary income. If earnings are differentially under-reported, the tax side moves, and that is a separate and larger threat to this ledger than transfer receipt is.
8. **Medicaid and housing assistance carry no dollar value in this ledger at all.** They are the two programs with the largest recipient-side bias in w35680 (Table 3, p.47: −30.8 and +11.6) and they cannot move a ledger that does not price them.
9. **Sampling error only.** SDR standard errors cover CPS sampling. They cover neither error in the published ratios nor the transport of a national ratio onto an individual resource unit.

## Verification, run and pasted

```
$ cd /Users/alien/Projects/immigration-research && uv run python3 infra/immigration-fiscal/ledger_underreport_2026_09_16/underreport.py
EXIT=0

-- GATE A: reproduce the peer lane's extended ledger before touching anything --
   extended balance gap, equal_all_members : -8,286 (se 443)   expected -8,286 (se 443)   deviation -0.23
   taxes-minus-transfers gap, same          : -6,066 (se 353)   expected -6,066 (se 353)   deviation +0.17
   [gate A] PASS (within $50 of -8,286)

======================================================================================================================
== EXTENDED BALANCE: Mexican 2nd gen minus 3rd+ NH white, annual $ per adult 25-64 ==
======================================================================================================================
arm                                                  equal_all_members      move       equal_adults_18plus      move
baseline_reported                                         -8,286 (443)         —             -10,633 (587)         —
a_proportional_base                                       -8,193 (452)       +93             -10,638 (600)        -5
a_proportional_noncash_extended                           -8,240 (453)       +46             -10,742 (604)      -109
a_proportional_w21399_vintage                             -8,167 (452)      +119             -10,598 (599)       +36
b_false_negative_mc                                       -8,017 (444)      +269             -10,393 (589)      +241
                                            (Monte Carlo sd of the gap across 50 draws: equal_all_members 50  equal_adults_18plus 52)
c_differential_receipt_rates                              -8,323 (453)       -37             -10,784 (601)      -151
c_differential_dollar_ratios                              -8,297 (453)       -10             -10,733 (600)      -100
a_bound_uniform_half_NOT_A_LITERATURE_VALUE               -7,387 (487)      +899              -9,919 (634)      +715

Wrote .../underreport_arms.csv
Wrote .../underreport_result.txt
```

The only stderr output is a pandas `PerformanceWarning` about frame fragmentation raised inside the peer lane's `extend_ledger.py:162`, unchanged by this work.

## Files

| File | What |
|---|---|
| `underreport.py` | The run. Imports `extend_ledger.build()`, applies the three arms, writes both outputs. |
| `underreport_arms.csv` | 192 rows: arm × allocation × group × metric, estimate, SDR se, difference from third-plus non-Hispanic white and its se, Monte Carlo sd where applicable. |
| `underreport_result.txt` | The printed tables, the ratio table, the arm (b) allocation plan, the renormalised arm (c) ratios, the caveats block. |

The CPS ASEC 2025 file is reused from the peer lane's cache at `infra/immigration-fiscal/gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip`, sha256 `318845a2…`, so this lane downloads nothing. The three source PDFs (w35680, w32860, w21399) were fetched free from nber.org; all three working papers are ungated.
