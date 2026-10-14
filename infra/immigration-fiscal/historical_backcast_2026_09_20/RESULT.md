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

## Round-2 corrections — 2026-10-15

The adopted payloads differ from the candidate's only in their stamps: meta.adopted "2026-10-15", status
"adopted: main case v8; ...", case "...; v8 adopted"; summary.json v8.status "adopted". Every number is unchanged.
A pin you took on the candidate's corrections.json / corrections_cash.json / summary.json bytes must be refreshed
to the committed bytes (verify the numbers match, then re-pin; never enrol silently).

REQUIRED before your phase 2: read the amendment file for your lane name; it changes your phase 2.
- p8-prop-a: already delivered by resume (note_a8_phase2.md); nothing new.
- p8-prop-b: /private/tmp/claude-501/-Users-alien-Projects-immigration-research/75b08f57-63cc-4e3d-96dc-60050327b5c1/scratchpad/prop8/note_b8_r2b.md
- p8-prop-d: nothing new (note_d8_r2.md and note_d8_r2b.md stand).`.

| Rule/scenario | 2015–2024 low / high, $bn | 74ce1f67 comparison low / high, $bn | Change low / high, $bn |
|---|---:|---:|---:|
| ratio: live_fixed_resource_rates | 3597.709115 / 4350.283007 | 2850.858677 / 3753.615749 | +746.850438 / +596.667258 |
| income: live_fixed_resource_rates | 3906.869647 / 4647.415995 | 3118.521350 / 4008.904121 | +788.348297 / +638.511874 |
| flat: live_fixed_resource_rates | 3485.772136 / 4338.405633 | 2984.959801 / 4018.492547 | +500.812335 / +319.913086 |
| programme: v7_measured_programme_overlay_beside | 3515.606037 / 4268.925394 | 3255.471617 / 3953.588138 | +260.134420 / +315.337256 |
| programme_income: v7_measured_programme_overlay_beside | 3758.381245 / 4496.968549 | 3456.748965 / 4139.786677 | +301.632280 / +357.181872 |
| joint: live_programme_measured_per_part_income | 3758.381245 / 4496.968549 | 3118.521350 / 4008.904121 | +639.859895 / +488.064428 |
| joint: programme_measured_before_unit_income | 3720.764203 / 4459.351507 | 3118.521350 / 4008.904121 | +602.242854 / +450.447386 |
| income: before_unit_income_fixed_rates | 3869.252606 / 4609.798954 | 3118.521350 / 4008.904121 | +750.731256 / +600.894832 |
| income: median_earnings_proxy_beside | 3917.674886 / 4658.221234 | 3118.521350 / 4008.904121 | +799.153536 / +649.317113 |
| income: wage_only_worker_split_beside | 3890.729557 / 4631.275905 | 3118.521350 / 4008.904121 | +772.208207 / +622.371783 |
| ratio: previous_unit_income_dfii10_stack | 3098.144149 / 4066.718388 | 2850.858677 / 3753.615749 | +247.285471 / +313.102638 |
| income: previous_unit_income_dfii10_stack | 3369.687639 / 4326.234334 | 3118.521350 / 4008.904121 | +251.166289 / +317.330212 |
| flat: previous_unit_income_dfii10_stack | 3237.338708 / 4338.405633 | 2984.959801 / 4018.492547 | +252.378907 / +319.913086 |
| ratio: financing_cost_dfii10_floor0_beside | 3374.759810 / 4350.283007 | 2850.858677 / 3753.615749 | +523.901133 / +596.667258 |

Capital-rate correction on the same ratio account, financing-cost DFII10 → fixed resource rates, $bn over2015–2024:

- low: 3374.759810 → 3597.709115 (+222.949305).
- high: 4350.283007 → 4350.283007 (+0.000000).

Income-linked carried-component change (before unit elasticity → after per-part rules), $bn over 2015–2024:

- low: -26.099349 → +11.517692.
- high: -38.126894 → -0.509852.

Own-formula PIA response derived from the pension lane, with its careers and vesting rules:

| Group | PIA earnings elasticity at 2024 | Mean AIME / first bend point |
|---|---:|---:|
| union | 0.557993 | 3.590069 |
| g1 | 0.566128 | 2.947100 |
| g2 | 0.557955 | 3.966727 |
| g3plus | 0.550857 | 4.037374 |

Part A has zero earnings elasticity conditional on covered workers: its transport follows under65 workers per member. Earned OASDI follows all positive-tax workers per member times the finite benefit-formula response. Current cash offsets retain benefit/use rules. Retiree-health national function price swaps carry no additional individual earnings elasticity. Legal/on-books participation adjustments are held assumptions. CPS earned-income proxies do not identify an exact ACS split into workers and earnings: ACS nonlabor income, survey composition, work-spell age and legal coverage remain unmatched.

Changes against74ce1f67 include v7→v8 propagation and round-2 rules. The previous_unit_income_dfii10_stack rows price the old74ce1f67 rule on the same v8 components, including its2024 financing-rate movement, to isolate that distinction.

2024 lineage: 45.2301 million. Annual anchors/per-member gates: 1e-4bn/$0.01; explicit component closure: 1e-9bn. Fixed capital and pension-rule regressions are in test_backcast.py. Programme paths replace the broad charged-base scaling and retain fixed resource rates, with new items on their own typed series.
[CALCULATION: derived/oct15/round2_windows.csv, round2_income_parts.csv, round2_pension_audit.json; ASSUMPTION: fixed legal/on-books adjustment; pre2019 fixed relative worker coverage and unsplit ACS earnings proxy]

The live joint stack starts with programme spending, then measured EIP shares, historical school/Medicaid use and per-part income. The broad charged-base correction stays a diagnostic because programme paths replace that same expenditure scaling. New completion/coverage school and Medicaid pieces receive their known source use keys. The old v7 programme displacement is transported onto v8. Item11 now uses its exact source r0 programme/generation split, including income and state taxes, non-EIP refundable credits, Medicaid, ACA, SNAP, property, housing and consumption. Its D_added residual remains a separate G3+ lineage part. The preserved consumption aggregate uses a declared national-receipt composite; historical allocations within that aggregate are unobserved. Unclassified coverage retains its declared population proxy. This remains conditional transport of the current programme scope rather than a reconstruction of historical statutes.

| Live branch: leave-one-branch-out → joint, $bn over 2015–2024 | Low before → after | High before → after |
|---|---:|---:|
| historical_school_medicaid | 3674.865731 → 3758.381245 (+83.515515) | 4399.484233 → 4496.968549 (+97.484316) |
| new_known_use_keys | 3756.522926 → 3758.381245 (+1.858319) | 4494.733985 → 4496.968549 (+2.234564) |
| pandemic_measured | 3809.227782 → 3758.381245 (-50.846536) | 4547.815085 → 4496.968549 (-50.846536) |
| per_part_income | 3515.606037 → 3758.381245 (+242.775208) | 4268.925394 → 4496.968549 (+228.043155) |
| precision_anchor | 3758.381415 → 3758.381245 (-0.000170) | 4496.968174 → 4496.968549 (+0.000375) |
| programme_spending | 3542.762307 → 3758.381245 (+215.618938) | 4286.603191 → 4496.968549 (+210.365358) |

Charged-base → programme replacement reconciliation (income branch excluded), $bn:

- low: original ratio 3265.459971 → charged ratio 3597.709115 (+332.249144) → programme 3515.606037; replacement -82.103078; maximum annual closure residual 2.84e-14.
- high: original ratio 4009.687317 → charged ratio 4350.283007 (+340.595690) → programme 4268.925394; replacement -81.357614; maximum annual closure residual 2.84e-14.

Exact item11 programme split and covered-G3+ count-path correction, replacing the previous aggregate tax proxy/count path together:

- low: 3768.372422 → 3758.381245bn (-9.991177). The count correction affects per-member denominators, not these cost totals. In the pre2024 fixture, the old path counts9.00 units and the corrected path8.72 units; the2024 anchor remains13.00. Actual covered-G3+2024 people690117.6475 now follow the same identified-G3+ path as their costs.
- high: 4504.665274 → 4496.968549bn (-7.696725). The count correction affects per-member denominators, not these cost totals. In the pre2024 fixture, the old path counts9.00 units and the corrected path8.72 units; the2024 anchor remains13.00. Actual covered-G3+2024 people690117.6475 now follow the same identified-G3+ path as their costs.

Missing school-age and Medicaid cells now fail by (key, group, income year); only absent Medicaid coverage before2019 is held. Deletion fixtures verify both a school cell and a 2021 Medicaid cell fail.

Added-descendant expenditure has an explicit gross base; all of it is separately priced by programme, leaving a zero residual broad base. Applying a second broad sigma would double count those components.
- low: gross added expenditure2024 $60.955268bn; separately carried $60.955268bn; residual $0; broad sigma before carrier exclusion would be $+4.431454bn over2015–24.
- high: gross added expenditure2024 $62.851571bn; separately carried $62.851571bn; residual $0; broad sigma before carrier exclusion would be $+4.569316bn over2015–24.
- Held-ratio descendants, low: live lineage–union gap $214.758353bn; an illustrative20% lower average ratio changes it by $-42.951671bn. Reviewer's earlier $169bn/$34bn illustration remains an illustration, not an estimated historical decline.
- Held-ratio descendants, high: live lineage–union gap $258.202950bn; an illustrative20% lower average ratio changes it by $-51.640590bn. Reviewer's earlier $169bn/$34bn illustration remains an illustration, not an estimated historical decline.
[CALCULATION: round2_programme_branches.csv, round2_added_expenditure_base.csv, round2_descendants.csv; ASSUMPTION: held descendants/identified-G3+ ratio]

Final validation receipts:

- bridge7: exit0, 27.584s, peak child RSS 0.455GB. See `/private/tmp/claude-501/-Users-alien-Projects-immigration-research/75b08f57-63cc-4e3d-96dc-60050327b5c1/scratchpad/prop8/backcast-bridge7.log`.
- producer7: exit0, 29.498s, peak child RSS 0.438GB. See `/private/tmp/claude-501/-Users-alien-Projects-immigration-research/75b08f57-63cc-4e3d-96dc-60050327b5c1/scratchpad/prop8/backcast-producer7.log`.
- tests3: exit0, 42.813s, peak child RSS 0.556GB. See `/private/tmp/claude-501/-Users-alien-Projects-immigration-research/75b08f57-63cc-4e3d-96dc-60050327b5c1/scratchpad/prop8/backcast-tests3.log`.
- orderfix: exit0, 0.466s, peak child RSS 0.131GB. See `/private/tmp/claude-501/-Users-alien-Projects-immigration-research/75b08f57-63cc-4e3d-96dc-60050327b5c1/scratchpad/prop8/backcast-orderfix.log`.
- rerun: exit0, 125.115s, peak child RSS 0.834GB. See `/private/tmp/claude-501/-Users-alien-Projects-immigration-research/75b08f57-63cc-4e3d-96dc-60050327b5c1/scratchpad/prop8/backcast-rerun.log`.
- Regression result: 42 passed in 42.33s.
- Physical-footprint gates before publication: native bridge0.596GB and latest back-cast0.484GB, below the shared2.5GB budget. Source scanning is streaming; deterministic audit bytes contain no timing or memory readings.
- The official seven-command gate sums required work. The measured stage receipts above identify the bridge, producer and full regression costs; worker extraction previously took23.550s and the longest individual regression fixture9.45s. The rerun harness records stage return codes but does not expose stage timing/stdout on success, so these are pre-rerun timings, not invented per-stage rerun measurements. No full rerun was repeated after exit0.
- The first official rerun exited1 with93/94 files unchanged: round2_income_parts.csv differed only in row order. All25,120 rows were exactly equal after canonical key sorting. The linked-set loops and writer now sort explicitly; the existing joint fixture verifies canonical CSV order. Failure log/timing are retained in backcast-rerun-failed-order.log and backcast-rerun-failed-order-timing.json; full original backup remains at /var/folders/td/k9yd1c8n5478my_42k9tb89h0000gn/T/rerun_m26uj0m4/lane. No values, rounding or gate tolerances were changed. The final rerun below validates the fix.
- The next attempt exited1 at the coverage source gate before comparing outputs: completion_keys.py and completion_jobs changed after the source freeze. Evidence is retained in backcast-rerun-failed-completion-source.log and its timing JSON; backup rerun_q6qcrk5w remains beside the first backup. No provenance gate was waived. The final recipe validates the exact original pricing arrays under the current source before rerunning.
- A subsequent bridge stopped when the authoritative cash recipe was refreshed between conversion and use. Re-conversion and repeated read-only pair checks passed: original set/cash compressed caches are exactly the owned replay bytes; every economic audit field matches, with only dependency_manifest_sha256 differing. This was a provenance update, not a cohort or price change. Stable source manifest hashes and both cache hashes are retained in backcast-contract-proof.json. The successful final bridge/source gate validates the current authoritative contracts.
- Official lane reproducibility: [rerun] IDENTICAL: 94/94 files unchanged (backup removed).

Covered: live oct15 set/cash, all typed items9–12, historical worker/pension and programme paths, archived-case byte-preservation fixtures and physical-memory gates. Earlier case outputs remain archived rather than being regenerated as live results. Raw source files were read only. Social and debt/uncertainty outputs remain the parent and sibling agents' responsibilities. The bridge physical probe executes bridge_memory.py dynamically; the official rerun exemption names only that demonstrated dynamic call, not a missing analysis command.

### Round-3 correction (2026-10-15 06:19:49 JST, `date`, parent)

Rerun on corrected v8 (`d1a24d47`: the coverage term no longer charges the missed people's custody, arrests and ICE a second time, −$3.199004 / −$3.221092bn on the lineage). The 2015–2024 cumulative (joint, live programme measured per part income) is
**$3,729.284421–4,467.674125bn** (was $3,758.381245–4,496.968549bn in the README's round-2 table); the programme
overlay beside is $3,486.509213–4,239.630970bn. `coverage_components_oct15.json` records the hash of the uncertainty
lane's `coverage_pes.py`, which round 3's fix changed; its values are unchanged. The rerun exempts
`bridge_memory.py`, which `v8_components.cjs` spawns (README, Covered). Parent rerun IDENTICAL 94/94, exit 0.
