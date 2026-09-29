claude-opus-5-5
**Verdict:** Owner-occupied property is one of a class of three published-weight lines, all entering with v4: owner-occupied property (+$0.3364 / +0.3364bn at specs 48 / 11; cash set the same), the pension switch's Part A accrual (a $41.137bn total summed over the published 40.90M frame; on row 4 $40.109bn: −$1.0280 / −1.0280bn) and its benefit-tax receipt (−$0.0273 / −0.0282bn); the last two are set-only. Joint move −$0.7189 / −0.7198bn: the set becomes $370.6957 / 434.1212bn, printed $370.7–434.1bn against $371.4–434.8bn, so both ends change at one decimal ($9,334–10,932 per member against $9,353–10,950). The cash set moves +$0.3364 / +0.3364bn to $295.0375 / 362.1539bn, printed $295.0–362.2bn against $294.7–361.8bn, which also changes. Beside that class, two ratios are summed at published weights and move on row 4: state pricing's price indexes (+$0.3661 / +0.3654bn, set and cash) and the OASDI accrual ratio (+$0.1528 / +0.1435bn, set only). With all five, the set is $371.2146 / 434.6301bn (−$0.2000 / −0.2109bn) and the cash set $295.4036 / 362.5193bn (+$0.7025 / +0.7018bn).

**Recorded, not applied.** Nothing here changes the adopted case: it stays $371.4–434.8bn (cash set $294.7–361.8bn) until
the operator decides whether to re-key these lines. The re-keys would belong to the adopted lane's payload.

## Question

Which lines of the adopted v4 case (`main_case_2026_09_29`, lane commit 40c4ba7) are keyed on the survey's published
weights instead of audit row 4? The scope is every line v4 moved or added, and every line at zero response on
September 27 that responds in v4. Each line's frame is read from the code (table below, with file:line). Each
published-frame input is re-keyed on row 4 by rerunning its own lane's computation at row-4 weights, and priced through
`main_case_2026_09_29/package.cjs` (`evaluateFull` at `MAIN_SPECS[48]` / `[11]`) for the set and, through
`forPayload(main_case_candidate_v4_2026_09_29/derived/corrections_v4_cash.json)`, for the cash set, alone and jointly.

Audit row 4 is the CPS ASEC 2025 weights with the Mexico-born naturalized (PRCITSHP 4) and noncitizen (PRCITSHP 5)
outside California and Texas scaled to their ACS 2024 levels: factors 0.8556255897504617 and 0.7781269999470055
(`cps_imputation_keys_2026_09_23/combine_onbooks_lane.py`, `weight_arms`), union 40,896,574 → 39,712,493.
[DATA: `derived/row4_parta.json`; `population_basis_2026_09_29/derived/frame_counts.csv`]

## Why the class exists

The September 24 row-4 step (`cps_imputation_keys_2026_09_23/combine_onbooks_lane.py:817-823`) re-weighted only the
keys of lines that responded then and of direct receipts. Owner property kept its model.json cell because it was an
indirect receipt at response 0. The pension accrual lane and the state-pricing lane came later and weight the CPS at
pwwgt0 (`pension_accrual_2026_09_28/pension_accrual.py:70`, `state_priced_services_2026_09_29/state_price.py:53`).
Lanes that carried row 4 themselves are clean: roads (under-5 shares from the row-4 bins), production (the row-4 grid),
payroll compliance (calibrated to the row-4 stacks), and items 1 and 4 (the evaluated rental key). [INFERENCE from the
code cited in the table]

## Pricing

$bn at specs 48 / 11. Base: set $371.4146 / 434.8410bn, cash set $294.7011 / 361.8175bn. Class A: group dollars
summed at the published weights. Class B: ratios summed at the published weights and applied to row-4 amounts. The
pension switch is off in the cash set, so its re-keys do not touch it. Printed with controlled rounding, so the parts
add to the joint rows and base + move = cost in every row: six printed values differ from their own rounding by 0.0001
(the benefit-tax move and cost at spec 48; the owner, Part A, class-A and all-five costs at spec 11).
`derived/price_rekeys.csv` has the unrounded values to six decimals.
[CALCULATION: `price_rekeys.cjs` → `derived/price_rekeys.json`, `derived/price_rekeys.csv`]

| Re-key | Class | Set move | Set cost | Cash move |
|---|---|---:|---:|---:|
| owner-occupied property (item 5) | A | +0.3364 / +0.3364 | 371.7510 / 435.1774 | +0.3364 / +0.3364 |
| Part A accrual (pension switch) | A | −1.0280 / −1.0280 | 370.3866 / 433.8130 | 0 / 0 |
| benefit-tax receipt (pension switch) | A | −0.0273 / −0.0282 | 371.3873 / 434.8128 | 0 / 0 |
| **joint, class A** | A | **−0.7189 / −0.7198** | **370.6957 / 434.1212** | **+0.3364 / +0.3364** (295.0375 / 362.1539) |
| state price indexes (state item) | B | +0.3661 / +0.3654 | 371.7807 / 435.2064 | +0.3661 / +0.3654 |
| OASDI ratio_net (pension switch) | B | +0.1528 / +0.1435 | 371.5674 / 434.9845 | 0 / 0 |
| joint, all five | A+B | −0.2000 / −0.2109 | 371.2146 / 434.6301 | +0.7025 / +0.7018 (295.4036 / 362.5193) |

The engine is linear in cell amounts, so the joint rows are the sums of the rows alone (−0.7189 = 0.3364 − 1.0280 −
0.0273). Per member on the account's 39.71M: class A $9,334 / 10,932, all five $9,348 / 10,944, against $9,353 /
10,950.

## Every line checked

Paths are under `infra/immigration-fiscal/`. "v4" = `main_case_candidate_v4_2026_09_29/package.cjs`, "v3" / "v2" the
candidate packages it imports, "items" = `receipt_side_long_run_2026_09_28/items.cjs`. Moves are $bn at specs 48 / 11
for the set; the cash set moves only where stated. The inventory of moved lines is `derived/lines_diff.json` (every
receipt, spending line and capital component whose amount, key or response differs between September 27 and v4).

| Line (side:id) | Item | Frame of the group amount or share | Evidence | Row-4 move |
|---|---|---|---|---|
| receipts:modeled_owner_property | 5 (response 0 → 0.763) | **published** (model.json cell 0.063237; key never recomputed) | items:7-8, :96 (response only); `cps_imputation_keys_2026_09_23/translate.py:42` (HELD) | +0.3364 / +0.3364; cash the same |
| spending:medicare, Part A accrual ($41.137bn) | pension | **published** (pension frame, union 40,896,574) | v4:98, :116, :233; `pension_accrual_2026_09_28/pension_accrual.py:70, :460-461, :510, :888-890` | −1.0280 / −1.0280; cash none |
| spending:medicare, Parts B and D | pension | row 4 (the case's MEPS key × (1 − 0.3751)) | v4:116; `cps_imputation_keys_2026_09_23/combine_onbooks_lane.py:538-552` (MEPS keys under the weight arms) | 0 |
| receipts:federal_income_tax, benefit-tax removal | pension | **published** (group share of the Census FEDTAX_BC key at ASEC weights) | v4:99, :117; `pension_accrual.py:649`; `pension_accrual_2026_09_28/benefit_tax.py:157, :268` | −0.0273 / −0.0282; cash none |
| receipts:federal_income_tax, IRS key | 3 | row 4 by the case's stack-factor rule (share change × row-4 stack factor × national) | v2:108-113 | 0 |
| receipts:federal_income_tax, compliance | 6a | row 4 (ratio × the case's amount; ratios calibrated to the row-4 stacks) | v3:113-119; `payroll_compliance_2026_09_28/compliance.py:801-809` | 0 |
| spending:social_security | pension | row-4 amount (the case's OASDI receipts) × ratio_net summed at published weights | v4:107, :115; `pension_accrual.py:350-380, :744-760` | ratio: +0.1528 / +0.1435; cash none |
| spending:state_price_public_order_safety, _health_services, _recreation_culture | state | row-4 key share (parent's evaluated key) × sum S&L × (index − 1), index on the published state mix | v4:135, :153; `state_priced_services_2026_09_29/state_price.py:53, :128-150, :366-367` | index (with the two receipts below): +0.3661 / +0.3654; cash the same |
| receipts:general_sales_tax | 6a + state | row-4 amount × 6a ratio × (1 + factor), factor from the published-mix index | v4:137, :155, :303; v3:119 | in the state row |
| receipts:personal_motor_vehicle | state + roads | miles key s_vmt(p) at row-4 p and U5, × (1 + factor), factor from the published-mix adult index | v4:179, :210, :155; `roads_mileage_key_2026_09_29/inputs.py:219-228` | in the state row |
| receipts:excise_selective_sales | 6a + roads | row 4 (gasoline at s_vmt − k_cons, both row 4; 6a ratio on the rest) | v4:197; v3:119 | 0 |
| spending:roads_vmt_sl, roads_vmt_fed | roads | row 4 (HWY_N × (k_road − k_old); p = the corrected population cell) | v4:194, :207-208; `main_case_long_run_2026_09_27/package.cjs:171-174` | 0 |
| capital:hwy_sl, hwy_fed | roads | row 4 (key k_road) | v4:339-341 (payload: part_rekeyed) | 0 |
| receipts:housing_enterprise_surplus (new) | 1 | row 4 (the corrected rental key, share 0.075207; published 0.125153) | v2:76-78 | 0 |
| spending:housing_subsidies (national −$5.258bn) | 1 | row-4 share held, national figure | v2:67 | 0 |
| receipts:enterprise_surplus (national −$40.298bn) | 1 | row 4 (the September 27 re-key to the corrected population share, 0.117174) | v2:71; `main_case_long_run_2026_09_27/package.cjs:165-181` | 0 |
| capital:ent_housing_sl | 4 | row 4 (housing_subsidies amount over national) | v3:65-75; `capital_return_services_2026_09_27/derived/engine_components.json` variant public_housing_at_rental_assistance_key | 0 |
| production grid | 2 | row 4 (naturalized × 0.856, noncitizens × 0.778, every cell) | `main_case_candidate_2026_09_28/production_row4.py:3-12`; its package.cjs:36-62 | 0 |
| receipts:tenant_occupied_property (new) | 5 | neither: ACS 2024 contract-rent share 0.114667 (ACS group 39.43M) | items:66-69, :83; `receipt_side_long_run_2026_09_28/housing.py:140, :355` | not a published-frame line |
| receipts:personal_property_tax (0 → 1) | 5 | neither: ACS 2024 vehicle share 0.102078 | items:73-77, :84; `housing.py:358` | not a published-frame line |
| receipts:remaining_production_property (national −$83.840bn) | 5 | row-4 capital key held; response 0 | items:63-65 | no cost |
| spending:workers_compensation | 7 | row-4 amount × pooled 2019-2024 / 2024 relative use, each year at pwwgt0 | v4:66-68; `backcast_pandemic_measured_2026_09_28/measure_shares.py:230-253` | ratio, not priced (row 4 exists only for income year 2024) |
| receipts:employee/employer OASDI and HI, self_employment_oasdi_hi, other_domestic_social_contributions, state_local_income_tax, other_personal_tax, customs_duties, personal_current_transfers, corporate_labor | 6a | row 4 (ratio × the case's amount) | v3:113-119; `compliance.py:801-809` | 0 |
| receipts:government_asset_income (not moved by v4) | — | published per head (resident_population, 0.120245) | `translate.py:42`; model.json | response 0 in both cases: no cost |

Lines at zero response on September 27 that respond in v4: modeled_owner_property and personal_property_tax, plus the
two new receipt lines. No spending line changes response. Of the receipt keys the row-4 stack never recomputes
(`translate.py:42`: modeled_owner_property, none, resident_population) only modeled_owner_property responds in v4;
enterprise_surplus was re-keyed to the corrected population share on September 27 (v4 share −0.8392 / −7.162 =
0.117174, the row-4 population share). [DATA: `derived/lines_diff.json`]

## The four reruns

Each imports its lane's own functions read-only, reproduces that lane's published outputs at the published weights,
then sums the same person vectors at row 4's weights.

- **Part A accrual** (`row4_parta.py` → `derived/row4_parta.json`). v4's Medicare line is
  `pp.part_a_accrual_bn * refs.partAScale[a] - pp.part_a_share * km[a].target_bn` (v4:116; partAScale 1 under
  `part_a_rule: "fixed"`, :233, :317); the accrual is the pension lane's `central_decomposition.low.part_a_accrual_bn`
  (v4:98), summed as `accrual_bn = (w * acc)[m].sum() / 1e9` with `w = u.w` over the stage frame whose union is gated at
  40,896,574.15 (`pension_accrual.py:70, :100-118, :460-461, :510`). Numerically v4's Medicare 73.8932 − (1 −
  416.3/1109.8) × 52.4192 = 41.1368. Rerun of `hi_accrual` with p.w × row 4's factors: union $41.137128bn → $40.109099bn
  (−$1.028029bn, kappa 1.025631), all of it G1 ($12.585bn → $11.557bn); covered workers 20.53M → 19.72M.
- **Benefit-tax receipt** (`row4_benefit_tax.py` → `derived/row4_benefit_tax.json`, Tax-Calculator 6.8.2). v4 removes
  `pp.receipt_bn[a] * refs.fitScale[a]` from federal_income_tax (v4:117; fitScale 1 under `benefit_tax_rule: "fixed"`,
  :233, :316); `receipt_bn` is national FIT × the group's benefit tax / the national Census FEDTAX_BC key
  (`pension_accrual.py:649`), both at ASEC weights (`benefit_tax.py:157`, `tot = W`; units line :268). The lane's
  row-scaled alternative (`current_receipt_scaled_to_case_line_bn`, `pension_accrual.py:657`) is not the one used.
  Receipt removed: shared (spec 48) 2.091206 → 2.063957 (−0.027249); personal (spec 11) 1.816900 → 1.788698 (−0.028202).
  Removing less raises FIT, so the cost falls by that much. The relative rate (benefit tax per benefit dollar, group over
  nation) is 0.523382 published and 0.526351 on row 4.
- **State price indexes** (`row4_state_index.py` → `derived/row4_state_index.json`). Each synthetic line is
  `SP_PRE[id] * k[a].target_bn / l.national_bn` (v4:153): the parent's evaluated (row-4) key share times `SP_PRE` = sum_f
  S&L_f × (index_f − 1) (v4:135); the sales and licence receipts move by (S&L / national) × (index − 1) × the row-4
  amount (v4:137, :155). Every index_f = sum_s w_s × relative price_s (`state_price.py:366-367`), w_s the group's state
  shares at pwwgt0 (`state_price.py:53, :128-150`). Row 4 removes 1.18M people, every one outside California and Texas,
  so it moves w_s. sum S&L × (index − 1): public order and safety 47.792 → 49.966 (×1.045485), health 31.794 → 33.581
  (×1.056225), recreation 3.652 → 3.612 (×0.988957). Receipt factors: general sales 0.115117 → 0.114860; personal motor
  vehicle licences (adult weights) 0.262393 → 0.275781.
- **OASDI ratio** (`row4_oasdi_ratio.py` → `derived/row4_oasdi_ratio.json`). v4's Social Security line is
  `pp.ratio_net * refs.oasdi[a]` (v4:115): the case's (row-4) OASDI receipts times the union's accrual per tax dollar net
  of the future benefit tax, summed over the pension frame at published weights (`pension_accrual.py:350-380`,
  `:744-760`). Row 4: gross ratio 1.018377851 → 1.020076752, timing 0.083884 → 0.083904; with the row-4 relative rate,
  ratio_net 0.973667 → 0.975027 (+0.140%; 0.975281 with the rate held at its published value). The SE OASDI share moves
  0.803496 → 0.803466 (negligible, not priced).

## Unsettled

- Item 7's pooled/2024 workers'-compensation ratio is summed at pwwgt0 in every year. It is not priced: row 4 exists only
  for income year 2024, and a consistent reweight of every year would largely cancel inside the ratio [INFERENCE].
- Item 5's tenant and personal-property keys are ACS 2024 shares (ACS group 39.43M), neither published CPS nor row 4,
  with decomposition kappa 0.980. They are not priced.
- Item 3's IRS share change is on row 4 only through the case's stack-factor rule (share change × row-4 stack factor).

## Gates

All pass; each script writes nothing and exits 1 on any failure.
- Oracle (`lines_diff.cjs`, `price_rekeys.cjs`): the adopted payload gives $371.4146 / 434.8410bn and the cash set
  $294.7011 / 361.8175bn, equal to `main_case_2026_09_29/derived/summary.json` (`main_case`, `cash_set.band_bn`) to 1e-9
  and to v4 as adopted to 1e-4; the September 27 package gives $321.8194 / 387.3701bn (`adopted_2026_09_27`, 1e-9).
- Positive control (`price_rekeys.cjs`): owner property on row 4 moves the set +0.3364 / +0.3364 to $371.7510 /
  435.1774bn, against the decomposition lane's +$0.34bn and $371.75 / 435.18bn
  (`main_case_decomposition_2026_09_29/RESULT.md`, "item 5's owner-occupied property tax"; 0.005).
- Each rerun reproduces its lane's published outputs before re-keying: the Part A accrual
  (`pension_accrual_2026_09_28/derived/summary.json`, 1e-9); the group benefit tax, national key and relative rate
  (`benefit_tax.json`) and the receipts (`summary.json` `current_receipt_bn`), 1e-9; every central state index
  (`corrections.csv`, `receipts_corrections.csv`, 1e-8) and the by-state group counts; the gross ratio, future share,
  ratio_net and SE OASDI share (`summary.json`, 1e-9 / 1e-12). Union counts reproduce
  `population_basis_2026_09_29/derived/frame_counts.csv` (published 40,896,574.15; row 4 39,712,493.33). The pension
  stage cache must exist (no rebuild).
- `price_rekeys.cjs` checks the reruns against the payload's own inputs (`V4PKG.pensionNet()`, `SP_PRE`, `SP_RECEIPT`)
  and that the cash set's Medicare equals the September 27 case's (1e-9).
- Every classified line cites file:line (table above).

## Reproduce

From the repository root, in this order (`row4_parta.py` first: the other three Python scripts read its factors;
`price_rekeys.cjs` last). The benefit-tax step needs the Tax-Calculator 6.8.2 wheel (`--with`, from uv's cache under
UV_OFFLINE=1); the rest use the main checkout's `.venv`. Times are the 2026-09-30 run: about 6 minutes in all, so run
it detached (the probe ran the OASDI step under `bgrun`); nothing is slow enough to leave out of the rerun check.

```sh
export OPENBLAS_NUM_THREADS=1 UV_OFFLINE=1
L=infra/immigration-fiscal/row4_class_2026_09_29
uv run --no-project python3 $L/row4_parta.py                                   # 1.5 min
uv run --no-project --with "taxcalc==6.8.2" python3 $L/row4_benefit_tax.py     # 2.6 min, the slowest (two Tax-Calculator runs)
uv run --no-project python3 $L/row4_state_index.py                             # 0.5 min
uv run --no-project python3 $L/row4_oasdi_ratio.py                             # 1.1 min (the central model grid)
node $L/lines_diff.cjs                                                          # seconds
node $L/price_rekeys.cjs                                                        # seconds
```

Rerun check (every output byte-identical):

```sh
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/row4_class_2026_09_29 \
  "uv run --no-project python3 {lane}/row4_parta.py" \
  "uv run --no-project --with taxcalc==6.8.2 python3 {lane}/row4_benefit_tax.py" \
  "uv run --no-project python3 {lane}/row4_state_index.py" \
  "uv run --no-project python3 {lane}/row4_oasdi_ratio.py" \
  "node {lane}/lines_diff.cjs" \
  "node {lane}/price_rekeys.cjs"
```

Inputs, all read-only: the adopted lane and its candidate packages, `main_case_long_run_2026_09_27`,
`main_case_decomposition_2026_09_29` (`profiles.py`, `summary_sept29.json`), `pension_accrual_2026_09_28` (code and
`derived/`), `state_priced_services_2026_09_29`, `population_basis_2026_09_29/derived/frame_counts.csv`, and the
ignored caches those lanes read: the CPS ASEC 2025 public-use zip
(`gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip`), the generation lane's person frame and the pension
lane's stage file (`pension_accrual_2026_09_28/_cache/stage_<hash>.parquet`; a script stops if it is missing rather
than rebuild it). With those caches present a run writes only this lane's `derived/` (checked by file times after the
2026-09-30 first run).

## Log

Times from `date` (JST).
- 2026-09-29 22:57:41: probe started in the scratch folder (read-only analysis); v4's edits listed.
- 23:00:40: `lines_diff.cjs`: oracle PASS, line inventory written.
- 23:12:10: `row4_parta.py`: all gates PASS; Part A −$1.028029bn.
- 23:16:07: `row4_benefit_tax.py` first run: all gates PASS.
- 23:17:58: `row4_state_index.py`: all gates PASS.
- 23:21:35–23:22:41: `row4_oasdi_ratio.py` under bgrun (rc 0): all gates PASS.
- 23:30:01: `row4_benefit_tax.py` rerun with the row-4 relative rate added (gate PASS); the OASDI row moved from
  +0.1814 / +0.1703 (rate held at its published value) to +0.1528 / +0.1435.
- 23:31:00: `price_rekeys.cjs`: all gates PASS; the pricing table above.
- 23:32:54: scratch verdict final; reported to the lead.
- 2026-09-30 00:01:51: this lane created; the six probe scripts ported. Paths resolve from each script's location,
  outputs go to `derived/`, gate references come from the lanes' derived files (`frame_counts.csv`, the pension
  `summary.json`, the adopted `summary.json`), no script writes after a failed gate, and `price_rekeys.cjs` adds
  `derived/price_rekeys.csv`.
- 00:04:57: `lines_diff.cjs` from the repository root: gates PASS; `derived/lines_diff.json` byte-identical to the
  probe's.
- 00:05:28–00:11:09: first full run from the repository root (bgrun; OPENBLAS_NUM_THREADS=1, UV_OFFLINE=1):
  `row4_parta.py` 00:05:28–00:06:55, `row4_benefit_tax.py` 00:06:55–00:09:33, `row4_state_index.py`
  00:09:33–00:09:59, `row4_oasdi_ratio.py` 00:09:59–00:11:05, `lines_diff.cjs` 00:11:05–00:11:07,
  `price_rekeys.cjs` 00:11:07–00:11:09. 52 gates PASS, none FAIL. All six JSON outputs byte-identical to the probe's:
  class A −0.7189 / −0.7198, all five −0.2000 / −0.2109, cash +0.3364 and +0.7025 / +0.7018.
- Before the rerun check (no time taken): the printed table and verdict put under controlled rounding; six printed
  values moved by 0.0001 (Pricing). No output changed.
- 00:12:58–00:17:41: `scripts/rerun_lane.py` over the six commands under Reproduce: every command rc 0, IDENTICAL
  (14/14 files unchanged), exit 0.
- 00:18:05: Reproduce and Log sections written; reported to the lead.
