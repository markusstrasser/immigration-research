claude-opus-5-5

**Verdict:** pending

# Do subsets of the account reproduce what others published? (pre-registered)

Lane: `infra/immigration-fiscal/backtest_published_2026_09_28/`. Brief: `BRIEF.md` (commit 78ca741). Three checks:
AIC "New Americans" taxes and spending power of Mexican immigrants; NAS 2017 Table 8-1 ratios (not blind); HCRIS
Worksheet S-10 uncompensated care by state. Phase 1 computes and freezes predictions; Phase 2 scores them after the
parent's go.

## Log

- 2026-09-28: stub written; Phase 1 under way.
- 2026-09-28, check 1 retargeted. A firewalled reader found no AIC publication that gives taxes or
  spending power for all Mexico-born immigrants (`reads/aic_methodology.md`, methods only, results redacted).
  The only AIC/NAE piece with Mexico-born figures is NAE's "Examining the Economic Contributions of
  Undocumented Immigrants by Country of Origin" (8 March 2021, ACS 2019 1-year). It covers "Mexican
  undocumented households" only. The parent was told at the time; check 1 now predicts that target.
- 2026-09-28, inputs for check 1's level splits: BEA NIPA annual flat file fetched to `_cache/bea/`
  (sha256 93b9fcb1…). For 2024, federal taxes on corporate income are $491.660bn of $663.685bn and federal
  excise is $99.964bn of $371.262bn. [DATA: series B075RC, W025RC, B234RC, LA000239]
- 2026-09-28: `predict.py` written. It imports the account's builders and gates every key against
  `model.json`.
- 2026-09-28, predictions frozen (Phase 1 complete). All gates pass:
  - 430 receipt and 178 spending cells reproduce `model.json` to 1e-9;
  - the Mexico-born (b) shares reproduce `generation_key_shares.json`;
  - the group's 25.74% of uninsured person-years reproduces the uncompensated-care key;
  - row 4's weights reach the ACS cells;
  - the NIPA splits add to the account's lines.

  Two runs of `scripts/rerun_lane.py` were IDENTICAL, 12/12 files each. `PREDICTIONS.md` states every
  number, baseline, tolerance and named gap, and `derived/tolerances.json` holds the bounds. The headline
  predictions [CALCULATION: `predict.py`]:
  - Check 1: undocumented Mexican households had $111.7bn of household income in 2019 ($95.2–135.2bn
    bridged from $151.8bn in 2024). Federal taxes are 0.163 of income under CBO's scope and 0.057 for
    income tax alone; state and local 0.103; spending power 0.734. The group's income is 28.0% in CA and
    19.3% in TX.
  - Check 2 (not blind): on the report's scenario 1, the first generation and their dependents have
    receipts at 0.856 / 0.850 and outlays at 0.903 / 0.896 of the average; NAS 2013 had 0.79 and 0.90.
    The conventions move the ratios by at most 0.002 (receipts) and 0.011 (outlays).
  - Check 3: each state's share of uninsured person-years (TX 17.4%, CA 8.2%, FL 8.1%). The r = 0.7
    arm implies a slope of −0.33. The prior standard error of 0.17–0.33 makes "no power" the expected
    outcome of the slope test.
- 2026-09-28, check 1 revised before any commit, on the parent's two conditions. The first "predictions
  frozen" message crossed with them, and the parent held the commit.
  - Check 1 is now labelled a shared-method comparison: NAE and the account both impute status by a
    Borjas-style residual and both use CBO's federal rates, so only a disagreement is informative.
  - Three items can yield a finding [CALCULATION: `predict.py`]:
    - income per household: $60,570 in 2019 dollars at the central bridge (0.736; range 0.662–0.813,
      income only). NAE publishes no household count as far as the methods show, so the scored
      figure falls back to income per Mexican undocumented immigrant, $24,243. Band 0.80–1.25 ×;
    - the payroll share: S = 0.1405 of household income under NAE's statutory rule on the frame's
      earnings, or 0.0703 halved, ±15% each;
    - the state distribution: the TVD rule unchanged.
  - The tax ratios are reported with the direction the conventions predict (NAE lower on taxes and
    higher on spending power). They count as a finding only if the gap runs the other way beyond the
    band.
  - The level bands on household income and the person count were dropped. Levels stay descriptive in
    `nae_quantities.csv`. Checks 2 and 3 are unchanged.
  - Two runs of `scripts/rerun_lane.py` were IDENTICAL, 13/13 files each.
- 2026-09-28: at the parent's request, check 2 is scored as a disclosed comparison, not a pre-registered
  test. Its ±0.05 tolerance was written down only after the run. `PREDICTIONS.md` carries the same label.
