**Verdict:** Pricing K-12 capital where the group enrolls adds **+$1.36bn** a year to the oct16 case at both ends (pre-1992 stock allocated by enrollment, arm a, the central). That is 0.37% of $368.0bn and 0.31% of $436.6bn. Arm b gives +$1.16bn. The case keeps its $368.0–436.6bn; this sits beside it and is not adopted. [CALCULATION: derived/dollars.csv, variant primary, weighting mexican_district_share, factor key_consistent_A]

The inventory starts at FY1992, not FY2000. The FY1992–1999 district files (downloaded under the coordinator's authorization) replace an allocation assumption with measurement. They show the group's districts built *less* per pupil than the nation in the 1990s: the 1992–1999 vintages have a relative of 0.943, against the 0.991 the FY2000-start inventory had assumed for all pre-2000 stock. The measured years lower the result by $0.23bn. The FY2000 start is kept as a sensitivity at +$1.59bn (arm a) and +$1.52bn (arm b).

| R_K, mexican district weights | Structures | Equipment | Stock-weighted |
|---|---|---|---|
| Literal district ratio C, arm a | 1.0379 | 0.8550 | 1.0339 |
| Literal district ratio C, arm b | 1.0272 | 0.8550 | 1.0234 |
| State-weighted check, arm a / b | 1.0604 / 1.0589 | 0.8646 | 1.0561 / 1.0546 |
| Applied factor F_A = R_K^A / 0.9542, arm a | 1.0804 | 0.9172 | 1.0768 |
| Applied factor F_A, arm b | 1.0708 | 0.9172 | 1.0674 |
| FY2000 start, literal C, arm a / b | 1.0494 / 1.0501 | 0.8550 | 1.0452 / 1.0458 |

Coverage:
- 0.9911 of FY1992–2024 real construction chains to an FY2024 NCES ID (0.9829 for FY1992–1999 alone). That is 0.9922 of the depreciated stock.
- 0.9143 of the CCD group pupils sit in a district with a capital price. The rest take their state's mean.
- National calibration: the F-33 inventory is 0.982 of BEA's K-12 structures of the same vintages, and 0.982 of BEA's $2,723.9bn in total.

## Why the applied factor is not the literal R_K

The brief describes the case as charging capital at national-average capital per pupil. It does not. The case keys K-12 capital by the account's school spending key, `school_part`. That key prices each group pupil at its state's average *current* spending per pupil, so the case already charges the group's capital at 0.9542 × the national average per pupil (`school_cost_where_enrolled_2026_09_24/derived/account_embedded_price.json`, `r_embedded_personal`).

On the same pupils (the account's CPS state mix), the right charge is national capital per pupil × R_K^A. The case's charge is national capital per pupil × 0.9542. The relative correction is therefore F = R_K^A / 0.9542.

Read the other way, the group's districts carry less current spending per pupil than the nation (0.954) but more capital per pupil (1.031 structures on the account's state mix). Capital per pupil is 8% above what the case's spending key implies. The literal district ratio C ignores the key the case already applies. Applied to the case, it would give +$0.31bn (arm a) and +$0.09bn (arm b) [CALCULATION: dollars.csv, brief_literal_C]. I report it because the brief named it. It is not the correction to the case.

The base amounts scaled (`case_base.cjs` → `derived/case_base.json`, run through `evaluateFull` on oct16):

- **K-12 return at the one rate.** 2.0810698764% × $2,723.9bn × effective key 0.193000 = **$10.9405bn**. This holds at both end specifications (16/11) and in both methods. It covers:
  - the engine's `k12` and `k12_user_fees` capital components, plus the `union_completion_k12*` lines, rescaled from the spec rate to the one rate;
  - the coverage capital parts (+$0.2945bn);
  - the item 16 and 17 count parts (−$0.1000bn and +$0.0056bn), which are already at the one rate, as the gate checks.
- **K-12 depreciation inside the school line.** BEA K-12 depreciation × the same key: structures $48.709bn × 0.193 = **$9.401bn**; equipment and software $15.009bn × 0.193 = **$2.897bn**.
- **The split.** Structures and equipment take their own factors. The return is split by BEA stock weights (2,663.95 / 59.97).

For arm a, +$0.840bn of the +$1.356bn comes from the return and +$0.516bn from depreciation. The equipment factor (0.917) offsets part of the structures factor (1.080).

Sensitivity range for F_A over the three weightings and the primary, reallocation, BEA-level and FY2000-start variants: +$1.15 to +$1.85bn. Family B (CCD state mix) runs up to +$2.04bn. [CALCULATION: dollars.csv]

## Method

Details are in `build.py`'s docstring.

**Panel.** Census F-33 all-items district files FY1992–FY2024. FY1992–1999 come from `acquire.py`, which holds the URLs and hashes in `derived/sources_pre2000.json`. FY2000–2024 come from `school_dilution_2026_09_24/_cache/f33`.
- Items: F12 construction, G15 land and existing structures, K09+K10+K11 equipment.
- TCAPOUT = F12+G15+K09+K10+K11+J99 holds to the dollar on every row. J99 starts in FY2000.
- FY2024 F12 ($90.159bn) and capital outlay ($113.088bn) match the capital lane exactly.
- FY1993 and FY1994 are survey years. Their reported rows hold 0.955 and 0.954 of the 1992/1995 mean pupils, and the missing rows are small, sampled-out districts. Reported rows are used unweighted. In FY1994 every California district carries weight 0 but full reported data, so weighting would have dropped California.

**Inventory.** Real flows use BEA's state-and-local educational structures price (FAAt705/706 line 62) and equipment price (line 56), as fiscal-year means.
- Geometric depreciation at BEA's implied 2024 rates: structures 1.828%; equipment 21.91% (line 56, 2024; 17.47% in 2023, 28.37% with software). Mid-year convention to mid-2024.
- Pre-FY1992 structures: π = 0.2537 of BEA's K-12 structures, from the capital lane's vintage weights × K-12 key. National pre-FY1992 stock is π/(1−π) × the F-33 FY1992–2024 inventory = $663.8bn ($675.8bn on the BEA level, a variant).
- Allocation arms: (a) FY1992 enrollment; (b) FY1992 enrollment × the district's FY1992–1996 real construction per pupil over national.
- Pre-FY1992 equipment is a steady state at the FY1992 level ($0.005bn; nothing survives).

**Chaining.** Districts chain by 7-digit NCES ID to FY2024. Unchained outlay comes from merged or closed IDs, for example the Memphis/Shelby 2013 merger and the California unifications. It is dropped in the primary run and reallocated within its state by FY2024 enrollment in the `realloc` variant. R_K moves by under 0.001.

The 0.98 chain threshold is justified by that reallocation test: the unchained share is too small and too evenly spread to move R_K. `test_lane.py` asserts both.

**Weights.** `school_cost_where_enrolled_2026_09_24/weighting.py` `build()`, unchanged: CCD 2023-24 Hispanic K-12 pupils × the district's ACS Mexican share of Hispanics, raked to the account's state pupil shares. Families:
- C, the district ratio;
- A, the account's CPS state mix at state capital per pupil × the within-state factor;
- B, the CCD state mix.

**Hispanic-proxy caveat (as in that lane).** District group counts are Hispanic pupils × a residential ACS Mexican share. They are not Mexican-origin pupils, and they do not include the later generations the account counts but who do not report Hispanic origin. The family A weights are identical under the Hispanic and Mexican state-share weightings because the within-state factor uses a constant state share.

## Arms ordered as expected, or explained

**FY2000 start.** Arm b ≥ arm a, as the brief expected: pre-2000 relative 0.9934 against 0.9911.

**FY1992 start.** Arm b < arm a: pre-1992 relative 0.9250 against 0.9665. The reason is that the group's districts were building little in 1992–1996. Construction per pupil relative to national [CALCULATION: raw F-33 F12/V33]:

| District | 1992 | 1994 | 1996 | 2004–2008 |
|---|---|---|---|---|
| California | 0.73 | 0.92 | 0.51 | 1.20–1.46 |
| Los Angeles Unified | 0.46 | 0.23 | 0.33 | 1.73–1.93 |

Los Angeles' building came after its 1997–2008 bond measures [TRAINING-DATA for the measure dates].

Arm b carries that 1992–1996 trough back onto pre-1992 vintages. It gives Los Angeles Unified $3.4bn of pre-1992 stock, against $10.1bn under arm a (`top_group_districts.csv`). For a district whose buildings largely predate 1970, that is not credible [INFERENCE]. So arm a is the central and arm b the low sensitivity.

The measured FY1992–1999 vintages (relative 0.943, 14.8% of the FY1992–2024 stock) are an observation, not an arm. They say old stock in the group's districts is, if anything, below national per pupil. Arm a's 0.967 is therefore not obviously conservative for the case's cost. It sits between the measured 1990s and parity.

## Land (secondary, lower bound)

G15 purchases cumulated at CPI-U, FY1992–2024, with no depreciation and no real appreciation: national **$163.6bn**. The group's G15 per pupil relative is R_C 1.051, R_A 1.041 and state-weighted 1.099.

At the 2.081% return only, the group's share is a **lower-bound charge of $0.72bn** a year on the case's key (key-consistent; $0.69bn literal). It falls to $0.57bn from FY2000. The case charges no land at all, since BEA's stock excludes land, so this is a level and not a delta.

[GAP] Land under schools bought before FY1992 (most school sites) and all real land appreciation are unmeasured. G15 also mixes existing-structure purchases with land. This floor is far below a site-value estimate, which needs parcel acreage × land prices.

## Confounders

- **California state bonds.** The brief's premise, that state bonds are absent from district outlay and so bias California down, does not hold for the inventory. Proposition 1A/47/55/1D and later School Facility Program money is granted to districts, which build, so the spending lands in district F12 when it is spent. Only the debt sits on state books [INFERENCE from the F-33 structure; program names TRAINING-DATA].
  - Evidence: California's J99 (state outlay on the district's behalf) is $0 in every checked year (every fourth year, FY2000–FY2024). California F12 runs $3.9–13.1bn a year. The national F-33/BEA calibration is 0.98.
  - California C12 (state capital revenue) is only $0.5–0.6bn through FY2012 and $0 since FY2016, so SFP grants are booked under another revenue code. Revenue coding does not matter for outlay.
  - One residual risk: state-built facilities recorded nowhere in F-33. The 1.8% national calibration gap bounds this.
- **Charters and county offices.**
  - Charter schools that lease buildings carry their facility cost in current spending, not F12. Leased private buildings are outside BEA's public K-12 stock, so low public capital per charter pupil is the right reading for the public stock the case charges.
  - Charters and county offices without a district price (part of the 8.6% of group pupils without one) take their state's mean.
  - County-office capital, such as California special education, is priced on the offices' own small enrollment.
  - Direction is unsigned. The effect is small at the 0.914 coverage.
- **Texas debt finance versus pay-as-you-go.** Irrelevant to a PIM: outlay enters when spent, however it is financed. Texas's C12 is 0 because its state facility aid pays debt service, which is not outlay.
- **Portables.** Purchased relocatables enter F12 or equipment when bought. Leased ones are current spending and outside the public stock.
  - Districts that absorb growth with portables or crowding show lower capital per pupil. That is the real resource use, not an error.
  - Portables bought as equipment depreciate at 21.9% here, faster than their service life, which understates them slightly in growth districts [INFERENCE; unmeasured].
- **Equipment rate.** The 2023 rate (17.5%) or the rate with software (28.4%) was not rerun. Equipment is 2.2% of the stock, and a rate change mostly moves its level, which the relative factor discards; its relative rests on the last decade of flows under any of these rates [INFERENCE].

## Run log

- 2026-10-24 00:54:33 JST: build.py (FY1992 start) started. Finished 00:54:59, rc 0, 24/24 gates. [`date`]
- 2026-10-24 00:56:47 JST: test_lane.py, 7 passed. [`date`]
- 2026-10-24 00:59:01 JST: rerun_lane.py with acquire.py, build.py and pytest. Finished 00:59:28: `IDENTICAL: 16/16 files unchanged`, exit 0. [`date`]

## Reviewer note

- 2026-10-24 01:00 JST: the divisor 0.9542 is the September 24 account's embedded price
  (`account_embedded_price.json`, 8.49M pupils). The v9 engine's K-12 capital key is 0.17724 against a pupil
  share of 0.17481, so v9's pupil count and price are not separately read here. If v9's embedded price differs
  from 0.954 by ±2%, the delta moves by about ±$0.2bn. Not load-bearing at this size; re-derive on adoption.
