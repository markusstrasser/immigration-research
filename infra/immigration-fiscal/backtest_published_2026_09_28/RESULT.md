claude-opus-5-5

**Verdict:** Scored against the predictions frozen in 0f9eea7.
- **Check 3 (CMS S-10, pre-registered).** The level and national tests hit. The slope test, expected to have no
  power, favors r = 0.7. It depends on the contrast between regions, and region controls leave it with no power.
  - Level: TVD 0.134 against the population baseline's 0.210.
  - National: $43.0bn against the account's $48.9bn.
  - Slope: −0.60, 95% interval −1.14 to −0.07.
- **Check 1 (NAE 2021, shared method).** No finding on any of its three items, and agreement cannot validate the
  account.
- **Check 2 (NAS 2017 Table 8-1, a disclosed comparison).** Partial. Outlays hit at 0.899 against 0.902. Receipts miss
  at 0.853 against 0.794. After the fact, the gap fits the rise in the foreign-born's relative income between 2013
  and 2024.

# Do subsets of the account reproduce what others published? (pre-registered)

Lane: `infra/immigration-fiscal/backtest_published_2026_09_28/`. Brief: `BRIEF.md` (commit 78ca741). Three checks:
AIC "New Americans" taxes and spending power of Mexican immigrants; NAS 2017 Table 8-1 ratios (not blind); HCRIS
Worksheet S-10 uncompensated care by state. Phase 1 computes and freezes predictions; Phase 2 scores them after the
parent's go.

## Scores (Phase 2, 2026-09-28)

`score.py` refuses to run unless `derived/predictions.csv` and `derived/tolerances.json` are identical to the freeze
commit 0f9eea7. It reads every source from a pinned sha256 (`derived/sources.json`) and quotes the cells it uses in
`reads/`. Verdicts are in `derived/scores.csv`. Post-hoc material sits beside them in `derived/notes.csv`, labelled,
and never replaces a verdict. All numbers are [CALCULATION: `score.py`] unless tagged otherwise.

| Check | Item | Published | Account (frozen) | Tolerance | Verdict |
|---|---|---:|---:|---|---|
| 1 | Income per Mexican undocumented immigrant, 2019 $ | $21,903 | $24,243 | $19,394–30,303 | no finding (−9.7%) |
| 1 | Payroll (SS + Medicare) / household income | 0.1575 | S = 0.1405 | 0.119–0.162 or 0.060–0.081 | no finding (+12%, statutory band) |
| 1 | State shares, TVD | 0.074 | baseline 0.097 | ≤ 0.08 and below the baseline | no finding |
| 1 | Federal / income (reading A) | 0.059 | 0.163 / 0.165 | finding only above 0.206 | no finding (lower, as expected) |
| 1 | State and local / income | 0.048 | 0.103 / 0.104 | finding only above 0.129 | no finding (lower, as expected) |
| 1 | Spending power / income | 0.894 | 0.734 / 0.732 | finding only below 0.702 | no finding (higher, as expected) |
| 2 | First generation receipts ratio | 0.794 | 0.856 / 0.850 | 0.806–0.900 | miss (+0.059), disclosed comparison |
| 2 | First generation outlays ratio | 0.902 | 0.903 / 0.896 | 0.853–0.946 | hit (−0.002), disclosed comparison |
| 3 | State shares of S-10 line 30, TVD | 0.134 | population 0.210 | ≤ 0.15 and ≤ 0.8 × population | hit |
| 3 | Slope of log error on the group's share | −0.60 (95% −1.14 to −0.07) | 0 (r = 1); −0.329 (r = 0.7) | by the 95% interval | favors r = 0.7 |
| 3 | National line 30, FY2023 | $43.03bn | $48.92bn | 0.8–1.25 × | hit (0.88) |

### Check 1: NAE 2021 (shared method, so only a disagreement would count)

- **Income per household.** NAE states no household count (reads), so the declared fallback applies: income per
  Mexican undocumented immigrant.
  - NAE: $91,992M over "more than 4.2 million" = $21,903.
  - Account: $32,946 in 2024 × the central bridge 0.736 = $24,243.
  - NAE sits at 1.004 × the bridge's low end. That end holds ACS income at 0.90 of CPS and lets the group's wages
    outgrow the average wage index by 5%. The declared year and survey gap covers it.
- **Payroll share.** NAE's 0.1575 is 1.12 × the statutory rule on the frame (0.1405), inside the statutory band. NAE did
  not halve payroll.
  - Post hoc: NAE's Medicare column implies earnings of 1.049 × its household income at 2.9%. Within one set of
    households that is impossible, so NAE's payroll covers Mexican undocumented earners outside the counted
    households. Its methods say "all individual wage earners".
  - The frame's household members earn 0.949 of household income. The unit difference is the likely source of the
    +12%. [INFERENCE]
- **State distribution.** D = 0.074 against the population baseline's 0.097. The largest gaps (NAE minus account):
  TX +0.041, GA −0.020, IL +0.009.
- **Tax ratios.** All run in the direction the conventions predict, since NAE halves CBO's and ITEP's average rates.
  - Federal is 0.059 of income. That fits reading A halved, not reading B. [INFERENCE]
  - State and local is 0.048 and spending power 0.894.
- **Context, not a verdict.** NAE credits the group with 1.79 × the account's own payroll share (0.087 / 0.089). The
  account keeps about half the group's wages on the books (audit row 2), and NAE assumes full statutory payroll.

### Check 2: NAS 2017 Table 8-1 (a disclosed comparison, not a pre-registered test)

- **Outlays agree:** 0.903 / 0.896 against 0.902.
- **Receipts miss:** 0.856 / 0.850 against 0.794, a gap of +0.06. The freeze named four candidates: the eleven
  years, the dependent definition (NAS Box 8-2 also counts some 18–23-year-olds), the institutionalized and the
  receipt keys.
- **Post hoc, the years carry the gap.**
  - NAS's own first-generation receipts ratio barely moved from 1994 to 2013 (0.787 → 0.794).
  - The foreign-born's relative income rose after 2013. The ACS median of the foreign-born over all rose from 0.884
    (2013) to 0.952 (2024), +7.6% [SOURCE: ACS B06011, `reads/acs_b06011.md`]. The mean income of foreign-born adults
    over all adults rose from 0.858 (2010) to 0.958 (2023), +11.6% [DATA: local IPUMS ACS panel].
  - NAS's 0.794 scaled by the median change is 0.855, the account's value.
  - This assumes taxes move at least in proportion to income. [INFERENCE]
  - The dependent and institutional differences are not quantified.

### Check 3: CMS HCRIS Worksheet S-10 line 30 by state (pre-registered)

The year rule selects FY2023: 6,103 reports against 6,064 the year before. After the declared cleaning, 4,437 reports
from 4,407 providers remain (`reads/hcris_s10.md`). KFF's expansion dates reproduce the frozen 2023 list exactly
(`reads/kff_expansion.md`).

- **Level: hit.** TVD against the S-10 shares:
  - account (r = 1): 0.134;
  - population: 0.210;
  - r = 0.7: 0.131;
  - full-year uninsured count: 0.126;
  - row 4: 0.132;
  - ACS 2023 uninsured: 0.106.

  Uncompensated care follows uninsured exposure, not population. The person-year key does no better than the plain
  count of the uninsured, and the two predictions sit 0.024 apart.
- **National: hit.** $43.03bn against the account's $48.92bn (AHA 2020 × its uplift), a ratio of 0.88.
- **Slope: favors r = 0.7.** The group's uninsured draw less S-10 uncompensated care per person-year than others do.
  The frozen consequence, a candidate rather than an adoption, is that the 0.7 arm cuts the uninsured-use addition
  from $3.65bn / $5.75bn to $2.12bn / $3.51bn at specifications 48 / 11: −$1.53bn / −$2.24bn on the case
  [DATA: `uncompensated_care_2026_09_23/derived/summary.json`].

| Fit | Slope (SE) | 95% interval | Verdict |
|---|---:|---|---|
| Primary: weighted, expansion indicator | −0.60 (0.27) | −1.14 to −0.07 | favors r = 0.7 |
| Weighted, no expansion indicator | −0.45 (0.49) | −1.40 to 0.50 | no power |
| Unweighted, expansion | −1.07 (0.31) | −1.69 to −0.46 | miss |
| Unweighted, no expansion | −0.99 (0.36) | −1.70 to −0.28 | favors r = 0.7 |
| Row 4 weights | −0.58 (0.25) | −1.07 to −0.09 | favors r = 0.7 |
| ACS 2023 shares and regressor | −0.63 (0.28) | −1.18 to −0.07 | favors r = 0.7 |
| Post hoc: CPS shares, ACS 2023 regressor | −0.56 (0.25) | −1.05 to −0.07 | favors r = 0.7 |
| Post hoc: Census region dummies added | −0.11 (0.17) | −0.45 to 0.22 | no power |

Post-hoc reading:
- **The sign is not a sampling artifact.** An ACS regressor has sampling error independent of the CPS shares, and it
  gives the same slope.
- **The evidence is regional.** Within the four Census regions the slope is −0.11. The contrast rests on Western
  states such as NV, AZ and WA, which report less uncompensated care per uninsured person-year and hold a large share
  of the group. A regional factor cannot be separated from the group's use rate. Candidates are prices, county
  indigent programs and emergency Medicaid. [INFERENCE on the candidates]
- **Implied r.** The point estimate implies r ≈ 0.49, with an interval of 0.16–0.93.
- **Expansion.** States without expansion in 2023 report 45% more per uninsured person-year (coefficient 0.373, SE
  0.084).
- **Maryland.** Its residual is −1.03, as expected under all-payer rates. Its weight is small.

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
- 2026-09-28, Phase 2 scored after the parent's go and the freeze commit 0f9eea7.
  - `score.py` refuses to run if `predictions.csv` or `tolerances.json` differs from 0f9eea7. It checks 13 sources
    against pinned sha256.
  - Sources: the NAE page (now opened), NAS Table 8-1, CMS's cost-report files for FY2020–2023 with the S-10
    instructions (data dictionary, PRM-II §4012.1, CMS Q&A), KFF's expansion dates and ACS B06011.
  - Quotes are in `reads/nae_2021_tables.md`, `nas_2017_table_8_1.md`, `hcris_s10.md`, `kff_expansion.md` and
    `acs_b06011.md`.
  - Verdicts and post-hoc notes are as in "Scores" above. Check 2 stays labelled a disclosed comparison.
