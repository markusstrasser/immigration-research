**Verdict:** The return on school capital that the account leaves out is **$9.5bn a year at a 2% real rate and $14.3bn at 3%** for the Mexican-origin group's 8.49m pupils (key range $9.3–9.8bn and $13.9–14.7bn), before land, which BEA does not measure [GAP]. By the brief's formula, that is 0.52–0.63 times (2%) and 0.78–0.95 times (3%) the depreciation already inside the school line ($15.1–18.2bn). Against the depreciation of K-12 assets alone ($11.1bn), it is 0.85 and 1.28 times. Adding it double counts nothing in the main case: the interest row, which holds the $23.1bn of interest on school debt, stays at response 0, and debt_legacy covers federal debt only.
[CALCULATION: `capital_return.py` → `derived/`; 32 gates pass; a second run is byte-identical]

Lane run by claude-opus-5-5[1m] on 2026-09-26 for the figures session f5e074c6 ([brief](BRIEF.md)). The
numbers sit beside the account and are not adopted. All amounts are 2024 dollars for income year 2024.
[FRAMING-SENSITIVE] Both rates are conventions, and so is the decision to charge a return on public
capital at all.

## Results

| $bn a year | 2% (OMB A-4, 2023) | 3% (OMB A-4, 2003) |
|---|---:|---:|
| National K-12 capital, 2024 average of year-end stocks | 2,723.9 | 2,723.9 |
| National return | 54.5 | 81.7 |
| **Group return (× s = 0.1748)** | **9.52** | **14.28** |
| Range across the K-12 split key (0.659–0.695) | 9.29–9.81 | 13.94–14.72 |
| End-2024 stock instead of the 2024 average | 9.69 | 14.54 |
| Share of the school line at full cost ($138.7bn low end / $172.5bn high end) | 5.5–6.9% | 8.3–10.3% |
| Main case if the return were added (not adopted; now $258.5–292.0bn) | 268.0–301.5 | 272.8–306.2 |

[DATA: `derived/capital_return.csv`, `derived/national_k12_capital.csv`; CALCULATION on
`main_case_schools_full_2026_09_26/derived/summary.json`]

Comparators on the same stock:
- **Market real rates.** Treasury's 2024 mean par real yields, 2.06% at 20 years and 2.15% at 30 years,
  give $9.8bn and $10.2bn.
- **OMB's other rate.** A-4 (2003) also prescribes 7%, "an estimate of the average before-tax rate of
  return to private capital". At 7% the group's return is $33.3bn. The result is linear in the rate, and
  the 7% figure is reported only.
- **Land [GAP].** Each 10% of land value relative to K-12 structures would add $0.93bn at 2% or $1.40bn
  at 3%. That is a conversion factor, not an estimate.

## 1. National K-12 capital

**What BEA publishes.** The Fixed Assets Accounts split government structures by type, not by function.
State and local "Educational" structures carry no K-12/higher-education split, and equipment, software and
R&D carry no function split (FAAt701–707). BEA's detailed fixed-asset files cover private assets and
consumer durables only (`_cache/fa_details_index.html`). NIPA publishes no consumption of fixed capital by
function: the NIPA table and series registers list none. [SOURCE]

**Educational structures.** The current-cost net stock was $3,876.4bn at the end of 2023 and $4,018.7bn
at the end of 2024. Depreciation in 2024 was $72.18bn, and the average age is 25.2 years.
[DATA: FAAt701, FAAt703 and FAAt707, line 62]

**Split key.** Each vintage of BEA's investment gets its K-12 share:
- **1993–2024 vintages (74% of the 2024 stock).** These use Census VIP's primary/secondary share of state
  and local educational construction. It ranges from 58.1% (2015) to 74.5% (1998) and was 66.9% in 2024.
- **Earlier vintages (26%).** These use NCES Digest Table 236.10 K-12 capital outlay × 0.80 (the
  construction share of F-33 capital outlay in FY2019 and FY2024), divided by BEA's investment. The
  anchors are 77.5% (1950), 76.8% (1960), 63.4% (1970) and 68.6% (1980), interpolated to VIP's 66.8% in
  1993. In the 15 school years where both exist, this method sits 4.2 points below to 6.1 points above
  VIP.
- **The 1989-90 anchor (91%) is set aside.** That year NCES outlay exceeds BEA's educational investment,
  and in 1993–94, the first VIP years, VIP runs 22–25% above BEA's series, so the pairing is off.
- **Vintage weights.** A perpetual inventory on BEA's investment quantity index (FAAt706 line 62) at
  BEA's implied rate of 1.83% reproduces 98.1% of BEA's 2024 stock and its 1993–2024 real growth (×2.085
  against ×2.058).

[DATA: `derived/k12_share_key.csv`; CALCULATION]

The K-12 share is **0.675**. The low end, 0.659, puts all pre-1993 vintages at the lowest anchor (63.4%);
the high end, 0.695, puts them at the highest (77.5%). Keeping the 1990 anchor gives 0.731, which would add
$0.8bn at 2%. Alternatives were computed but not used:
- VIP 2024 alone: 0.669.
- Census of Governments FY2022 capital outlay, which includes equipment and land: 0.718.
- NIPA 3.15.5, K-12's share of education consumption plus investment: 0.758. This is not a capital
  measure.

[DATA: `derived/summary.json` → `k12_structures_key_alternatives`]

**Equipment and software.** K-12's F-33 equipment outlay is 14.7% (FY2019) to 16.1% (FY2024) of BEA's
state and local equipment-plus-software investment. On that stock the share gives $60.0bn. R&D is left out
because school districts do none [INFERENCE]. Structures are 97.8% of K-12 capital.

**Result.** K-12 capital averages **$2,723.9bn** over 2024 ($2,657–2,807bn), about $56,000 per public
pupil, and is $2,772bn at the end of 2024. Its 2024 depreciation is $63.7bn: $48.7bn on structures and
$15.0bn on equipment and software, on the NIPA basis (see Gates). The group's share, s × K, is $476bn.
[CALCULATION]

## 2. Land under schools [GAP]

Land is not a produced asset, so BEA's stocks and the account both leave it out. No primary source for the
value of land under public schools was at hand, so no estimate is made. Closing the gap would take two
inputs:
- **Site acreage** of district-owned school parcels, from state facility inventories or county assessor
  parcel files;
- **Land prices per acre** by tract, for example FHFA's residential land price series.

The conversion factor is in the Results section. District financial statements carry land at historical
cost, far below today's value, so they cannot close it. [GAP]

## 3. The rate [FRAMING-SENSITIVE]

- **2%: A-4 (2023).** "The result is an estimate of the social rate of time preference of 2.0 percent per
  year": the 30-year average real 10-year Treasury yield plus a 0.3-point PCE adjustment (pp. 76–77).
- **3%: A-4 (2003).** "the real rate of return on long-term government debt may provide a fair
  approximation" of the social rate of time preference.
- **Which one is current.** OMB M-25-15 (12 February 2025) revoked the 2023 Circular and reinstated the
  2003 one, so 3% and 7% are the guidance in force. The 2% remains the measured 30-year real Treasury rate.
- **Market check.** Treasury's 2024 real yields are 1.94% (10-year), 2.06% (20-year) and 2.15%
  (30-year).
- **Municipal bonds.** No primary series of real municipal yields was at hand. Tax exemption puts them
  below Treasury yields. [INFERENCE]

[SOURCE: `_cache/omb_a4_2023.txt`, `omb_a4_2003.txt`, `omb_m25_15.txt`, `treasury_real_yield_2024.csv`;
text gated]

The current-cost net stock is valued at replacement cost less depreciation, and a real rate on it excludes
holding gains, which is the standard user-cost pairing. Two opposite biases remain unpriced. Special-purpose
school buildings might sell for less than their depreciated replacement cost, while land is missing
altogether. [INFERENCE]

## 4. The group's share, and capital where the group enrolls

The return uses the brief's pupil share, s = 8.487m / 48.551m = 0.17481, at national average capital per
pupil (gated to the brief's value). Capital per pupil where the group enrolls plausibly differs. The
evidence below is described, not modelled.

| Per public pupil, F-33 FY2024 | Capital outlay | Interest | Debt outstanding |
|---|---:|---:|---:|
| United States | $2,439 | $498 | $12,547 |
| Group's pupils, weighted by state | $2,670 (+9.5%) | $655 (+31.5%) | $16,534 (+31.8%) |
| California (2.45m of the group's pupils) | $2,758 | $764 | $19,153 |
| Texas (2.00m) | $3,384 | $994 | $26,444 |

[DATA: `derived/capital_per_pupil_where_enrolled.csv`; weighted by district rather than state, the
school-cost lane has capital outlay at 1.067 and interest at 1.258:
`school_cost_where_enrolled_2026_09_24/derived/r_other_concepts.csv`]

The group's districts are building more per pupil, which fits enrollment growth in Texas and California.
Newer buildings are less depreciated, so current-cost capital per pupil is plausibly above the national
average. Overcrowded sites and portable classrooms would push the other way. Debt per pupil mostly reflects
how states finance construction, not the stock: Texas districts borrow, while California also uses state
bonds that district debt omits [TRAINING-DATA]. BEA publishes no state-level stocks. [INFERENCE]

## 5. The depreciation already in the school line

NIPA has no education CFC, so the lane builds one from the Fixed Assets Accounts:
- **Structures only: $73.3bn.** This is state and local ($72.18bn) plus federal ($1.13bn) educational
  structures.
- **All assets: $120.6bn.** This adds state and local R&D ($25.1bn) and education's 22.7% of state and
  local equipment-plus-software depreciation.
- **Where the 22.7% comes from.** State and local education investment ($180.8bn, NIPA 3.17 line 132),
  less educational structures ($126.3bn) and R&D ($29.8bn), divided by equipment-plus-software investment
  ($108.8bn).
- **R&D spread instead** of charged to education: $121.6bn.

Education CFC is 6.0% (structures) to 9.9% (all assets) of the account's education line, below the
12.26% state and local average.

| Depreciation for the group, $bn | Amount | Return ÷ it at 2% | At 3% |
|---|---:|---:|---:|
| Brief's formula: education CFC (all assets) × school fraction × s | 15.08 (low end, 0.715) to 18.24 (high end, 0.865) | 0.52–0.63 | 0.78–0.95 |
| Same CFC share applied to the account's school line ($138.7–172.5bn) | 13.70–17.03 | 0.56–0.70 | 0.84–1.04 |
| Brief's formula, structures only | 9.17–11.09 | 0.86–1.04 | 1.29–1.56 |
| Like for like: K-12 assets' depreciation × s | 11.14 | 0.85 | 1.28 |

[DATA: `derived/depreciation_comparison.csv`; the school-fraction bounds come from `model.json`, and gates
check that each end pairs with its own specification's school share: low end 0.715, high end 0.865]

The brief's formula has the larger denominator because of how the account splits education. It charges
71.5–86.5% of the education line, and so the same share of all education depreciation, to schools. That
share includes university R&D and higher-education equipment. K-12, however, holds 67.5% of educational
structures and none of the R&D.

Applying the same proportional split to capital instead (school fraction × all education capital of
$4,242bn × s) gives a return of $10.6–12.8bn at 2% and $15.9–19.2bn at 3%, 0.70 and 1.06 times the
depreciation. On K-12's own assets the return is 0.85 times the depreciation at 2% and 1.28 times at 3%.
That follows from a stock worth 43 years of depreciation. [CALCULATION]

## 6. Double count: none in the main case

- **The school line carries depreciation only.** It is BEA consumption, which "assumes a zero net return
  on these assets" (NIPA 3.10.5, note 2, gated).
- **Interest is held at 0.** The account's `domestic_interest` row ($1,118.87bn nationally, $134.5bn to
  the group at the population key) contains state and local interest, including the $23.1bn of interest
  on school debt (F-33 FY2024). Its response class `interest` returns `state.interest_response` (engine.js
  line 123). The default is 0 (engine.js line 41). The main case builds its state from
  `Engine.defaultState` and overrides only the service lines
  (`main_case_2026_09_24/package.cjs` lines 75 and 82). The two later packages never mention interest.
  [DATA; gate `interest_row_held_at_zero_in_main_case`]
- **No lane charges school-debt interest to the group.** `debt_legacy_2026_09_23` prices interest on
  federal debt from the group's past federal gaps. It keeps "the lead's no-legacy framing for state-local
  gaps", and "State-local interest ($274.6bn) sits in the account's interest row" (RESULT.md lines
  381–385). That line stays beside the main case in any case. [SOURCE]
- **The ledger is a separate account.** `ledger_absolute_2026_09_17` item K charges cash outlay plus
  interest, but that ledger is not the main case (section 7).
- **Private capital is separate.** The production term already pays the opportunity cost of private
  capital (`research/immigration-matched-benefits-2026-09-19.md` line 77). Public school capital is not in
  it. [INFERENCE]

Two conditional overlaps:
- **A scenario that charges existing interest.** An interest response above 0, an explorer control, would
  put the group's population share of school-debt interest into the account: $2.78bn at response 1. That
  is part of the return's debt-financed slice, so it would have to come off.
- **A future price for new seats.** The schools decision lists "new seats at today's construction cost" as
  an unpriced upside (`decisions/2026-09-26-main-case-schools-full-cost.md` line 65). If that is ever
  priced as a user cost of new capacity, it contains this return, and only one of them should be counted.

## 7. Comparator: ledger item K, on a cash basis

| Group, $bn a year | Basis | Amount |
|---|---|---:|
| Ledger item K, Mexican-origin union (40.90m people) | cash: F-33 FY2024 capital outlay + interest, by state | 22.73 |
| Same F-33 per-pupil amounts on the account's 8.49m pupils | cash | 28.22 (outlay 22.66 + interest 5.56) |
| National F-33 total × s | cash | 23.80 |
| Depreciation in the school line (brief) + return | accrual, 2% | 24.60–27.76 |
| Same | accrual, 3% | 29.36–32.52 |
| K-12 depreciation × s + return | accrual, 2% / 3% | 20.66 / 25.42 |

[DATA: `derived/comparator_item_k.csv`; item K is read from
`ledger_absolute_2026_09_17/derived/items_by_group.csv`]

Nationally, cash is $136.2bn and accrual is $118.2bn at 2% or $145.4bn at 3%. The two are equal at a real
rate of 2.66%. The components differ:
- **Capital outlay exceeds depreciation.** Outlay is $113.1bn against $63.7bn of depreciation, mostly
  because of net investment. BEA-basis K-12 structures investment was $85.2bn against $48.7bn of
  depreciation, and the real stock grew 1.36% in 2024. Outlay also includes land and existing structures
  ($5.4bn), which BEA leaves out, and equipment ($17.5bn against $15.0bn of depreciation). School and
  calendar years differ by six months.
- **Interest is far below the return.** Interest ($23.1bn) compares with a return of $54.5–81.7bn,
  because school debt ($581.8bn) finances only 21% of K-12 capital. Its nominal rate, 3.97% of year-end
  debt, still exceeds the 2–3% real rates.
- **Over the cycle.** In a steady state without growth, capital outlay would approach depreciation, and
  nominal interest would exceed the real return on the debt-financed part by inflation. The accrual
  measure offsets that inflation with holding gains.

[DATA: `derived/cash_accrual_bridge_national.csv`]

Why the group figures differ:
1. **Population.** It is not the cause. Item K's union is the same 40.9m people as the account's target.
2. **Pupil base.** This is most of the gap between $22.7bn and $28.2bn. Item K multiplies children aged
   5–17 by the native pupil ratio of 0.8027 for every group (`absolute_ledger.py` line 624;
   `gen_ledger_extension_2026_09_16/extend_ledger.py` line 100). At the group's cash per pupil that is
   6.84m pupil-equivalents, against the account's 8.49m enrolled pupils. This is the ledger's documented
   central pupil rule, "children 5–17 × public-pupil ratio ≈0.803" (`ledger_absolute_2026_09_17/BRIEF_build.md`
   line 8). The extension uses the same rule for its K-12 charges (`extend_ledger.py` lines 282–296) and
   computes flat-0.90 and group-differential arms beside it (lines 314–316). Its differential arm gives
   Mexico-born and Mexican-origin households 0.9048 (line 101), and at that ratio item K would be about
   $25.6bn. Nothing was edited here. [Coordinator note: added after the lane run.]
3. **State mix.** The group's states spend 13% more per pupil on capital and interest than the national
   average ($28.2bn against 8.49m × the national $2,937). Cash charges that; the accrual figures use
   national average capital per pupil (section 4).
4. **Vintage.** Both cash figures use the same F-33 FY2024 file (a gate checks the ledger's totals), so the
   vintage explains little. Item K is carried on the ledger's own central (shared) allocation.
5. **Cash against accrual.**
   - At 2%, the brief-formula accrual ($24.6–27.8bn) sits between item K and the state-weighted cash,
     and the like-for-like version ($20.7bn) sits below both.
   - At 3%, the brief-formula version is above both, and the like-for-like version ($25.4bn) is between
     them.
   - The cash charge is inflated this year by net investment and by the inflation in nominal interest. It
     is depressed by the 79% of capital that carries no interest.

## 8. The other services charged in full (structures by type)

BEA gives structures by type, so the functions below are matched by type. The group's share is the main
case's allocation key for each function line.

| Function | BEA structure types | Stock, 2024 average | Return to the group at 2% / 3% | Note |
|---|---|---:|---:|---|
| Public order and safety | public safety, S&L and federal nondefense | 399.7 | 0.96 / 1.44 (population key); 1.05 / 1.58 (use key) | courthouses may sit in "Office" |
| Health | health care, S&L and federal nondefense | 472.0 | 0.72 / 1.09 | the account's line is net of hospital sales (S&L gross $491.4bn, net $126.8bn); fee recovery is not netted here |
| Housing and community services | S&L residential, sewer, water | 2,561.2 | 6.16 / 9.24 | mostly fee-financed utilities and rented housing; not comparable with a tax-financed charge |
| Income security | none | — | — | offices sit in "Office" [GAP] |

[DATA: `derived/other_services.csv`]

## Gates (all 32 pass; `derived/gates.csv`)

- **Premise.** The NIPA note carries the zero-net-return sentence. The reused facts match:
  - s = 0.17480600215120404;
  - the school fraction bounds are 0.7153 and 0.8652, and each end of the main case's school line sits
    at one of them (both fill-in methods agree);
  - the account's education line equals NIPA 3.17 line 9;
  - state and local CFC is $312.559bn of $2,550.362bn.
- **Net stock over CFC.** Educational structures are at 54.7 and all K-12 assets at 42.7; the range for
  structures is 30–80.
- **The FA tables against NIPA's CFC where both exist.** NIPA has no education CFC, so this runs at the
  finest common level, with a 0.5% tolerance:
  - 2024 government structures: $327.106bn against $327.088bn;
  - 2024 intellectual property products: $299.606bn against $299.641bn;
  - state and local all assets in 2022 and 2023, within 0.04%.
  - In 2024 the FA tables' state and local depreciation exceeds NIPA's by $13.0bn. The gate places it in
    equipment (the government equipment gap is $12.9bn), which leaves structures, 97.8% of K-12 capital,
    unaffected. The already-counted depreciation therefore uses NIPA-basis equipment ($58.0bn, not
    $71.0bn).
  - The 2024 closing stock matches NIPA 5.10 exactly.
- **The key.** The perpetual inventory reproduces BEA's stock and its real growth. VIP tracks BEA's
  investment at a ratio of 0.83–1.25, and the NCES method tracks VIP within 7 points. The key is plausible
  (0.5–0.85), and educational structures fall inside NIPA's education investment.
- **Double count and comparator.** The interest row is at 0, debt_legacy is federal only, the ledger's
  F-33 totals match, the pupils by state sum to the account's, and item K's pupil ratio was read.
- **Rates.** The 2%, 3%/7% and M-25-15 sentences are present in the primary texts.

## Gaps

- [GAP] Land under schools (section 2).
- [GAP] No published K-12/higher-education split or education CFC. Both are built from documented keys,
  with the key's range reported.
- [GAP] Capital per pupil by state. The group's share uses national average capital per pupil.
- [GAP] Income-security structures; function-level offices.
- [GAP] No primary municipal real-yield series.
- [GAP] BEA's 2024 difference between the FA tables and NIPA in state and local equipment depreciation
  ($13.0bn) is located but not explained.

## Files covered and skipped

Covered, all parsed by the script:
- **BEA Fixed Assets Section 7:** FAAt701, 702, 703, 705, 706 and 707
  (https://apps.bea.gov/national/FixedAssets/Release/XLS/Section7All_xls.xlsx; file created 15 Sep 2025,
  data 1925–2024).
- **The pinned NIPA Section 3 workbook**
  (`sources/immigration-fiscal/data/external/bea_nipa/Section3All_xls.xlsx`): T31005 lines 47 and 51 and
  note 2; T31505 lines 109–111; T31700 lines 9, 26, 27 and 132.
- **NIPA Section 5**, T51000 lines 39–42 and 74, and **Section 7**, T70500 lines 22–27
  (https://apps.bea.gov/national/Release/XLS/Survey/), plus the NIPA table and series registers.
- **Census Value of Construction Put in Place**, state and local, 1993–2025
  (https://www.census.gov/construction/c30/: `xls/stateha.xls`, `xls/stateha1.xls`,
  `xlsx/stateha2.xlsx`, `xlsx/state.xlsx`).
- **Census of Governments 2022**, Table 1, lines 69–74
  (https://www2.census.gov/programs-surveys/gov-finances/tables/2022/22slsstab1.xlsx).
- **Census school finance (F-33)** FY2024 summary Tables 9, 10 and 19 (`elsec24_sumtables.xlsx`) and
  FY2019 Tables 9, 10 and 19 (`elsec19_sumtables.xls`).
- **NCES Digest 2023**, Table 236.10, column 10.
- **Treasury** daily par real yield curve, 2024.
- **OMB:** A-4 (2023), A-4 (2003) and M-25-15.
- **Registry.** URLs and hashes are in `derived/sources.csv`.

Read-only repo inputs, with hashes in `derived/summary.json`:
- `school_cost_where_enrolled_2026_09_24/derived/`: `account_embedded_price.json`,
  `account_pupils_by_state.csv`, `r_other_concepts.csv`, and that lane's RESULT.md around line 255;
- `main_case_schools_full_2026_09_26/derived/summary.json` and RESULT.md;
- `assumption_explorer_2026_09_21/derived/model.json` and `engine.js`;
- the `package.cjs` files of the 09-24, 09-26 and schools-full cases;
- `debt_legacy_2026_09_23/RESULT.md` (its `debt_legacy.py` was searched only; a peer is editing it);
- `ledger_absolute_2026_09_17` (RESULT.md, README.md, `absolute_ledger.py`, `params/params.json`,
  `derived/items_by_group.csv`) and `gen_ledger_extension_2026_09_16/extend_ledger.py`;
- decisions `2026-09-20-category-service-response.md` and `2026-09-26-main-case-schools-full-cost.md`.

Skipped:
- **BEA API.** It needs a key; the public files carry the same tables.
- **IPEDS finance.** Public colleges' capital assets would check the higher-education side, but only at
  book value, and VIP suffices.
- **The NCES facilities survey.** It reports building age by region, which belongs to the described,
  unmodelled point.
- **Land-price and parcel data.** See the land gap.

## Reproduce

```sh
# once, or with --refresh: stage and hash the primary files (xlrd is needed only here)
uv run --no-project --with xlrd python3 infra/immigration-fiscal/school_capital_return_2026_09_26/acquire.py
# the lane: prints the results, writes derived/, exits 1 on a failed gate
uv run --no-project python3 infra/immigration-fiscal/school_capital_return_2026_09_26/capital_return.py
```

## Run log

- **23:07 Stub written.** Coordinator addition at 23:14: the item K comparator (section 7).
- **23:31 Sources staged.** The scratch numbers of that entry were superseded by the script. The same day,
  OMB M-25-15 was checked in the primary memo.
- **Validation.** 30 of 30 gates pass, `rc=0`, and a rerun is byte-identical.
- **23:55 Coordinator fix.** The schools lane now reads its school line at fixed specifications (f1e4f5b):
  $138.7bn at the low end and $172.5bn at the high end, where the first version gave $167.0bn and
  $143.4bn. The script had paired the low end with the 0.865 share to fit the old figures. Each end now
  takes its own specification's share, and two gates guard that. The return itself does not use the line
  and is unchanged. The school-line shares, the via-line depreciation row and the end labels moved. 32 of
  32 gates pass, and a rerun is byte-identical.
