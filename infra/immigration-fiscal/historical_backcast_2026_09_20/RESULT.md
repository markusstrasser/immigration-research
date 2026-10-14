**Verdict:** The three controlled changes together put the 2015–2024 lineage back-cast at $2.8509–3.7536tn (`ratio`), $3.1185–4.0089tn (`income`) and $2.9850–4.0185tn (`flat`, with the historical capital-rate exception). These are beside results, not adopted changes to the fiscal case. The programme rule with measured pandemic shares and available school-age/coverage keys gives $3.2555–3.9536tn or $3.4567–4.1398tn with income scaling. [CALCULATION: `p7_backcast.py` → `derived/p7/windows.csv`]

The current `derived/oct14/` files stay byte-identical. This is a model of historical costs in 2024 dollars, summed without discounting, not observed historical group borrowing. Public-capital returns are imputed resource costs; pension accrual is valued future benefits. Personal allocation and specifications 16 / 11 are held throughout, rather than re-selecting historical band ends. [ASSUMPTION; DATA: `case_components_oct14.json`, `programme_inputs.json`]

## Controlled changes

Each entry is **low / high**, $bn accumulated in real 2024 dollars. Delta is against the same population, rule and window of the current case. The `union` means its 39.71M identified members; `lineage` includes the 3.04M added descendants (42.75M in 2024). The added people's historical path is the identified G3+ count/share, with their 2024 ratio held fixed. The union follows the case-components split: the enlarged group's response change stays on the union. [DATA: `case_components_oct14.json` `lineage`; CALCULATION: `carried_parts`, `changes_annual.csv`]

### lineage: totals

| Scenario | Rule | 2015–2024 | 2010–2024 | 2005–2024 |
|---|---|---:|---:|---:|
| fixed_2pct | flat | 3,221.206 / 4,018.493 | 4,693.284 / 5,854.775 | 5,957.167 / 7,431.245 |
| fixed_2pct | ratio | 3,007.184 / 3,696.585 | 4,246.711 / 5,226.069 | 5,136.168 / 6,362.921 |
| fixed_2pct | income | 3,304.827 / 3,994.228 | 4,831.281 / 5,810.639 | 5,951.971 / 7,178.724 |
| yield_floor0 | flat | 2,984.960 / 4,018.493 | 4,331.560 / 5,854.775 | 5,592.751 / 7,431.245 |
| yield_floor0 | ratio | 2,795.225 / 3,696.585 | 3,933.559 / 5,226.069 | 4,820.703 / 6,362.921 |
| yield_floor0 | income | 3,092.868 / 3,994.228 | 4,518.128 / 5,810.639 | 5,636.506 / 7,178.724 |
| yield_unfloored | flat | 2,958.183 / 4,018.493 | 4,297.155 / 5,854.775 | 5,558.346 / 7,431.245 |
| yield_unfloored | ratio | 2,770.298 / 3,696.585 | 3,902.479 / 5,226.069 | 4,789.624 / 6,362.921 |
| yield_unfloored | income | 3,067.940 / 3,994.228 | 4,487.049 / 5,810.639 | 5,605.427 / 7,178.724 |
| charged_base | flat | 3,221.206 / 4,018.493 | 4,693.284 / 5,854.775 | 5,957.167 / 7,431.245 |
| charged_base | ratio | 3,062.817 / 3,753.616 | 4,270.332 / 5,250.283 | 5,103.879 / 6,329.820 |
| charged_base | income | 3,360.460 / 4,051.259 | 4,854.902 / 5,834.853 | 5,919.682 / 7,145.623 |
| income_linked | flat | 3,221.206 / 4,018.493 | 4,693.284 / 5,854.775 | 5,957.167 / 7,431.245 |
| income_linked | ratio | 3,007.184 / 3,696.585 | 4,246.711 / 5,226.069 | 5,136.168 / 6,362.921 |
| income_linked | income | 3,274.846 / 3,951.873 | 4,779.118 / 5,732.012 | 5,880.295 / 7,067.739 |
| stack | flat | 2,984.960 / 4,018.493 | 4,331.560 / 5,854.775 | 5,592.751 / 7,431.245 |
| stack | ratio | 2,850.859 / 3,753.616 | 3,957.180 / 5,250.283 | 4,788.414 / 6,329.820 |
| stack | income | 3,118.521 / 4,008.904 | 4,489.587 / 5,756.226 | 5,532.540 / 7,034.638 |

### lineage: one-change deltas and stack

| Scenario | Rule | 2015–2024 delta | 2010–2024 delta | 2005–2024 delta | 2024 annual delta |
|---|---|---:|---:|---:|---:|
| yield_floor0 | flat | -236.246 / 0.000 | -361.724 / 0.000 | -364.416 / 0.000 | -1.167 / 0.000 |
| yield_floor0 | ratio | -211.959 / 0.000 | -313.152 / 0.000 | -315.465 / 0.000 | -1.167 / 0.000 |
| yield_floor0 | income | -211.959 / 0.000 | -313.152 / 0.000 | -315.465 / 0.000 | -1.167 / 0.000 |
| yield_unfloored | flat | -263.023 / 0.000 | -396.129 / 0.000 | -398.821 / 0.000 | -1.167 / 0.000 |
| yield_unfloored | ratio | -236.886 / 0.000 | -344.232 / 0.000 | -346.544 / 0.000 | -1.167 / 0.000 |
| yield_unfloored | income | -236.886 / 0.000 | -344.232 / 0.000 | -346.544 / 0.000 | -1.167 / 0.000 |
| charged_base | flat | 0.000 / 0.000 | 0.000 / 0.000 | 0.000 / 0.000 | 0.000 / 0.000 |
| charged_base | ratio | 55.633 / 57.031 | 23.621 / 24.214 | -32.290 / -33.101 | 0.000 / 0.000 |
| charged_base | income | 55.633 / 57.031 | 23.621 / 24.214 | -32.290 / -33.101 | 0.000 / 0.000 |
| income_linked | flat | 0.000 / 0.000 | 0.000 / 0.000 | 0.000 / 0.000 | 0.000 / 0.000 |
| income_linked | ratio | 0.000 / 0.000 | 0.000 / 0.000 | 0.000 / 0.000 | 0.000 / 0.000 |
| income_linked | income | -29.980 / -42.354 | -52.163 / -78.627 | -71.676 / -110.985 | 0.000 / 0.000 |
| stack | flat | -236.246 / 0.000 | -361.724 / 0.000 | -364.416 / 0.000 | -1.167 / 0.000 |
| stack | ratio | -156.325 / 57.031 | -289.531 / 24.214 | -347.754 / -33.101 | -1.167 / 0.000 |
| stack | income | -186.305 / 14.677 | -341.694 / -54.413 | -419.431 / -144.085 | -1.167 / 0.000 |

### union: totals

| Scenario | Rule | 2015–2024 | 2010–2024 | 2005–2024 |
|---|---|---:|---:|---:|
| fixed_2pct | flat | 3,032.253 / 3,776.727 | 4,422.471 / 5,508.269 | 5,619.234 / 6,998.858 |
| fixed_2pct | ratio | 2,822.462 / 3,466.651 | 3,988.188 / 4,904.188 | 4,825.226 / 5,973.601 |
| fixed_2pct | income | 3,120.105 / 3,764.294 | 4,572.758 / 5,488.758 | 5,641.029 / 6,789.403 |
| yield_floor0 | flat | 2,813.685 / 3,776.727 | 4,087.445 / 5,508.269 | 5,281.727 / 6,998.858 |
| yield_floor0 | ratio | 2,626.329 / 3,466.651 | 3,698.088 / 4,904.188 | 4,532.991 / 5,973.601 |
| yield_floor0 | income | 2,923.972 / 3,764.294 | 4,282.658 / 5,488.758 | 5,348.794 / 6,789.403 |
| yield_unfloored | flat | 2,789.000 / 3,776.727 | 4,055.684 / 5,508.269 | 5,249.967 / 6,998.858 |
| yield_unfloored | ratio | 2,603.342 / 3,466.651 | 3,669.391 / 4,904.188 | 4,504.294 / 5,973.601 |
| yield_unfloored | income | 2,900.985 / 3,764.294 | 4,253.961 / 5,488.758 | 5,320.097 / 6,789.403 |
| charged_base | flat | 3,032.253 / 3,776.727 | 4,422.471 / 5,508.269 | 5,619.234 / 6,998.858 |
| charged_base | ratio | 2,878.096 / 3,523.682 | 4,011.809 / 4,928.402 | 4,792.937 / 5,940.500 |
| charged_base | income | 3,175.738 / 3,821.325 | 4,596.379 / 5,512.972 | 5,608.740 / 6,756.303 |
| income_linked | flat | 3,032.253 / 3,776.727 | 4,422.471 / 5,508.269 | 5,619.234 / 6,998.858 |
| income_linked | ratio | 2,822.462 / 3,466.651 | 3,988.188 / 4,904.188 | 4,825.226 / 5,973.601 |
| income_linked | income | 3,074.895 / 3,707.625 | 4,491.132 / 5,382.592 | 5,528.940 / 6,640.796 |
| stack | flat | 2,813.685 / 3,776.727 | 4,087.445 / 5,508.269 | 5,281.727 / 6,998.858 |
| stack | ratio | 2,681.963 / 3,523.682 | 3,721.709 / 4,928.402 | 4,500.702 / 5,940.500 |
| stack | income | 2,934.396 / 3,764.656 | 4,224.652 / 5,406.806 | 5,204.415 / 6,607.696 |

### union: one-change deltas and stack

| Scenario | Rule | 2015–2024 delta | 2010–2024 delta | 2005–2024 delta | 2024 annual delta |
|---|---|---:|---:|---:|---:|
| yield_floor0 | flat | -218.568 / 0.000 | -335.026 / 0.000 | -337.506 / 0.000 | -1.072 / 0.000 |
| yield_floor0 | ratio | -196.133 / 0.000 | -290.100 / 0.000 | -292.235 / 0.000 | -1.072 / 0.000 |
| yield_floor0 | income | -196.133 / 0.000 | -290.100 / 0.000 | -292.235 / 0.000 | -1.072 / 0.000 |
| yield_unfloored | flat | -243.253 / 0.000 | -366.787 / 0.000 | -369.267 / 0.000 | -1.072 / 0.000 |
| yield_unfloored | ratio | -219.120 / 0.000 | -318.797 / 0.000 | -320.932 / 0.000 | -1.072 / 0.000 |
| yield_unfloored | income | -219.120 / 0.000 | -318.797 / 0.000 | -320.932 / 0.000 | -1.072 / 0.000 |
| charged_base | flat | 0.000 / 0.000 | 0.000 / 0.000 | 0.000 / 0.000 | 0.000 / 0.000 |
| charged_base | ratio | 55.633 / 57.031 | 23.621 / 24.214 | -32.290 / -33.101 | 0.000 / 0.000 |
| charged_base | income | 55.633 / 57.031 | 23.621 / 24.214 | -32.290 / -33.101 | 0.000 / 0.000 |
| income_linked | flat | 0.000 / 0.000 | 0.000 / 0.000 | 0.000 / 0.000 | 0.000 / 0.000 |
| income_linked | ratio | 0.000 / 0.000 | 0.000 / 0.000 | 0.000 / 0.000 | 0.000 / 0.000 |
| income_linked | income | -45.210 / -56.669 | -81.626 / -106.166 | -112.090 / -148.607 | 0.000 / 0.000 |
| stack | flat | -218.568 / 0.000 | -335.026 / 0.000 | -337.506 / 0.000 | -1.072 / 0.000 |
| stack | ratio | -140.499 / 57.031 | -266.479 / 24.214 | -324.525 / -33.101 | -1.072 / 0.000 |
| stack | income | -185.709 / 0.362 | -348.106 / -81.952 | -436.614 / -181.708 | -1.072 / 0.000 |

## Rate, base and income rules

1. **Rate:** DFII10 is the daily inflation-indexed ten-year Treasury yield, in percent. Annual means exclude the file's blank non-trading days; 245–265 daily observations must exist per year. The low end uses the year's mean, floored at zero, divided by the old 2% on every capital component. The unfloored arm permits a negative cost of money. The high end retains 3%. The annual 2024 yield is 1.937120%; its low-end cost moves -1.167 / 0.000bn. That movement is shown explicitly; it is not calibrated away. [SOURCE: https://fred.stlouisfed.org/series/DFII10; DATA: pinned `_cache/DFII10.csv`, `inputs/pins.json`; CALCULATION: `primary_rates` → `real_yields.csv`]

2. **Charged base:** subtract NIPA 3.1 interest (line 27), subsidies (line 30) and NIPA 3.17 defence consumption (line 3) from total current expenditures. Recalibrate sigma at 2024, holding the base's charged group dollars fixed. The receipt base and the separately carried lines are held. Housing subsidies that the case does charge remain in the separate rental-assistance addition: excluding the whole subsidy line here avoids carrying the base with the excluded business subsidies. Flat has no national spending index, so this changes neither flat end. National totals close within 1e-9bn; the new spending index is exactly 1 at 2024. [DATA: pinned BEA Section3 workbook source cells; CALCULATION: `controlled_changes` → `charged_base.csv`]

3. **Income:** apply the same measured ACS relative-income multiplier to the separately carried income-linked receipts, job-capital taxes keyed to wages, payroll-earned OASDI/Part A accrual, and induced production receipts. Property on homes, enterprises, user-fee carriers, other spending and private production value retain their existing path. A wages-based job-capital key is not an observation of historical capital-tax receipts. This preserves the unit-elasticity assumption. Every part's included/excluded classification is exported; ratio and flat do not use this multiplier. [ASSUMPTION; DATA: `income_classification.csv`; CALCULATION: `controlled_changes`]

4. **Fail closed:** only `(T31200-A:20, 2005–2014)` is a permitted source/year blank. The pinned BEA note 4 says the post-2015 line includes reimbursements for healthcare received at private facilities; no such amounts are reported in the model's pre-2015 window. Every other absent or non-finite observation stops before cells are summed. Injection tests cover a missing 2019 observation, a missing year, a different source and infinity. This applies to both whole-budget and programme helpers; numerical controls are unchanged. [SOURCE: BEA T31200-A footnote 4; DATA: `STRUCTURAL_ZEROS`; CALCULATION: `test_p7_backcast.py`]

**Disconfirmation of reviewer point estimates:** The live computation reproduces the ten-year low rate reduction to within about $0.2bn of the review's $211.8bn. The base correction is 55.633 / 57.031bn, not $66bn. The income-linked correction is -29.980 / -42.354bn, not −$65bn / +$39bn. The reviewer estimates were leads, not input data. [CALCULATION: `windows.csv`]

**Review bar:** These are historical-rule corrections, not a new annual fiscal case. Rate has a 2024 change below $5bn at both ends; base and income recalibration preserve 2024; programme closes to the original case within 1e-6bn. None changes the annual headline by $5bn. The stated claim that every part of the current back-cast follows its programme series is falsified: its base follows whole-budget aggregates. The cumulative shifts exceed $5bn over many windows, which is a different denominator. [CALCULATION; INFERENCE]

## Programme beside rule

### lineage

| Variant | Rule | 2015–2024 total | 2010–2024 total | 2005–2024 total |
|---|---|---:|---:|---:|
| programme | programme | 3,222.803 / 3,906.950 | 4,530.110 / 5,503.512 | 5,496.733 / 6,720.753 |
| programme | programme_income | 3,424.080 / 4,093.149 | 4,926.613 / 5,868.156 | 6,050.672 / 7,227.864 |
| programme_pandemic | programme | 3,171.956 / 3,856.104 | 4,479.264 / 5,452.666 | 5,445.887 / 6,669.906 |
| programme_pandemic | programme_income | 3,373.233 / 4,042.302 | 4,875.766 / 5,817.309 | 5,999.826 / 7,177.018 |
| programme_measured | programme | 3,255.472 / 3,953.588 | 4,606.699 / 5,603.270 | 5,581.464 / 6,830.357 |
| programme_measured | programme_income | 3,456.749 / 4,139.787 | 5,003.202 / 5,967.914 | 6,135.402 / 7,337.468 |

### union

| Variant | Rule | 2015–2024 total | 2010–2024 total | 2005–2024 total |
|---|---|---:|---:|---:|
| programme | programme | 3,038.081 / 3,677.017 | 4,271.587 / 5,181.631 | 5,185.792 / 6,331.432 |
| programme | programme_income | 3,224.129 / 3,848.901 | 4,638.627 / 5,518.736 | 5,699.317 / 6,800.921 |
| programme_pandemic | programme | 2,989.876 / 3,628.812 | 4,223.382 / 5,133.426 | 5,137.586 / 6,283.227 |
| programme_pandemic | programme_income | 3,175.924 / 3,800.696 | 4,590.421 / 5,470.530 | 5,651.112 / 6,752.716 |
| programme_measured | programme | 3,072.496 / 3,725.482 | 4,351.662 / 5,285.320 | 5,278.300 / 6,450.158 |
| programme_measured | programme_income | 3,258.544 / 3,897.366 | 4,718.701 / 5,622.424 | 5,791.825 / 6,919.648 |

`programme` evaluates all charged v7 engine lines, at the personal specifications, on their national source series. OASDI accrual and the Part A accrual part of Medicare follow payroll contributions; Medicare's remaining part follows its benefit series. Synthetic lines follow their parents. The pension benefit-tax adjustment follows income-tax receipts. Capital follows its stock series at fixed 2% / 3%; private and induced production terms follow real GDP times their population-share path, as the case's existing production mapping does. `lane_constants` holds its 2024 value per person (no budget programme series). It includes the charged rental/energy-assistance and public-capital costs; a fiscal-gap-only debt output would omit those. The 2024 totals close to the full-precision engine at 1e-6bn. [DATA: `programme_inputs.json`; CALCULATION: `programme_lines.csv`]

`programme_pandemic` replaces the refundable-credit line's 2020/2021 EIP part with the existing measured personal payment shares under the `borjas` SSN treatment and income-year/payment-year mapping. It applies measured relative use to the rest of that credit line. National EIP levels are parsed from annual line 31 of the pinned primary BEA PDF. The added non-identifying descendants' pandemic relative-use change is assumed to equal the identified union's, applied to their own G3+ population path; they are not observed by CPS identity. Other programme keys are held. [SOURCE: pinned BEA PDF URL in `inputs/pins.json`; DATA: `backcast_pandemic_measured_2026_09_28/derived/measured_shares.csv`; ASSUMPTION]

`programme_measured` adds school-age (5–17 at survey) relative shares in 2005–2024 on the K-12 operating portion of education (the case's share coefficient) and school reprice, and Medicaid coverage relative shares in 2019–2024 on the medical line excluding its uncompensated-care key shift. The coverage fraction is held at the 2024 case fraction; the added people's fraction takes the same split. Medicaid is held at its 2024 relative key before 2019 because the local historical extract lacks coverage fields. Coverage counts are not programme spending; school age is a pupil-use proxy, not measured attendance. Capital and fee keys remain fixed at 2024. Both group paths are divided by the same extract's 2024 relative-use key; raw CPS headcounts are not scaled onto the case total. [DATA: `historical_use.csv`, `use_source_manifest.json`; ASSUMPTION]

The coverage source has 160 replicate weights for 2019–2024. `programme_medicaid_se.csv` propagates each year's union/G3 covariance to a conditional annual price-change SE (2024 key and case prices fixed). The anchored 2024 change and SE are zero. Full-window SEs are not identified without cross-year survey covariance; school-age paths have no full-window replicates in the local extract. Rate and base use published series and have no survey sampling SE. No historical-tax/benefit causal estimate is claimed. [CALCULATION: `historical_use_replicates.csv`, `programme_medicaid_se.csv`; INFERENCE]

`programme_pandemic_se.csv` prices the source lane's replicate SEs for the non-payment credit part, conditional on 2024 keys and prices. For the EIP part it gives lower/upper SE bounds across unknown round covariance (a single round has identical bounds). It does not add these parts' SEs or claim a whole-window SE. [DATA: source `measured_shares.csv` `relative_use_se`; CALCULATION: `programme_pandemic_se.csv`]

## Gates, provenance and reproduction

- Four live outputs reproduce byte for byte before any correction.
- National charged/un-charged sums close at 1e-9bn; finite series and source/year gap checks fail closed.
- Engine line effects plus production and capital close at 1e-9bn; programme/measurement 2024 anchors at 1e-6bn.
- Historical-use grids: 52 central rows, 1,932 replicate rows; union plus other conserves national weights.
- Rate high end and all inactive flat/income-index arms have exact zero shifts; the stack equals the three changes.
- Primary downloads are immutable pins in `inputs/pins.json`; reused microdata hashes are in `use_source_manifest.json`, other dependencies in `audit.json`.

Source-derived values and calculations constrain this LLM-produced output. The remaining political frame and historical relative-use assumptions are explicit, not made empirical by the arithmetic. [INFERENCE; repo instrument-bias caveat]

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/historical_backcast_2026_09_20/acquire_p7.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/historical_backcast_2026_09_20/historical_use.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/historical_backcast_2026_09_20/p7_backcast.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/historical_backcast_2026_09_20/write_p7_result.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest infra/immigration-fiscal/historical_backcast_2026_09_20/ -q --import-mode=importlib
```

## Execution log

- 2026-10-14 22:03 JST (`date`): the first programme union closure rejected the debt twin's split; traced its attribution difference and used the case's authoritative lineage parts instead.
- 2026-10-14 22:10 JST (`date`): controls and 27 tests passed. Excel-sheet caching removed repeated parsing; P7 builds measured 4–8 seconds / about 0.20GB with `time.perf_counter` and `resource.getrusage`. Historical-use extraction measured 24.13 seconds / 1.90GB.
- Final review/check receipts are in `validation.md`; no staging, merging or commits performed.
