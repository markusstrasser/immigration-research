**Verdict:** Priced by state on both sides, the group costs **+$2.19bn more at the low end and +$2.27bn at the high end** in the central package. Spending rises **+$8.58/8.64bn**: every S&L sub-function of public order and safety (police +2.58, courts +0.09, fire +1.50, state prisons per prisoner +1.00, protective inspection +1.23), health +1.80 and parks and libraries +0.37/0.43. Receipts rise **$6.39/6.37bn**: general sales tax index 1.115 (+5.65; Texas taxes sales at 1.30× the US rate per PCE dollar) and motor vehicle licences 1.262 (+0.75/0.72). The narrow arm (police and health, less the same receipts) is **−$2.01/−1.99bn**. Administration, housing and selective excises stay national: administration's sign is not identified across the E23 break, and the other two are within ±2%. Prisons are priced per state prisoner (BJS Table 2 was local after all): index 1.103 with the group located as each state imprisons, 1.310 on population shares (+$3.02bn arm). [CALCULATION: state_price.py → derived/corrections.csv, receipts_corrections.csv, prison_per_inmate.csv, net_state_correction.csv]
claude-opus-5-5

Lane `state_priced_services_2026_09_29`, 2026-09-29. The lane adopts nothing and edits no other lane; the lead integrates.

## Proposed corrections

The index is the group's population-weighted mean, across states, of state-and-local direct expenditure per resident (Census FY2024, level 1, E+F codes) relative to the US. For each function f, correction = S&L amount_f × the line's adopted group share × (index_f − 1) × the line's response at the band end. The federal portion is untouched, and each line keeps its own key. [CALCULATION]

| Line | Function (Census codes) | S&L amount $bn | Group share | Index (SE) | Low end $bn | High end $bn | Clears ±2%? | Recommendation |
|---|---|---:|---:|---:|---:|---:|---|---|
| public_order_safety | police (E/F62) | 166.75 | 0.13417 | **1.1154** (0.0058) | **+2.58** | **+2.58** | yes | adopt |
| public_order_safety | judicial (E/F25) | 63.19 | 0.13417 | 1.0111 (0.0039) | +0.09 | +0.09 | no | in the central package (whole POS line priced), noise on its own |
| health_services | health, excluding hospitals (E/F32) | 126.84 | 0.05660 | **1.2507** (0.0149) | **+1.80** | **+1.80** | yes | adopt |
| general_public_services | administration (E23+E29+E31) | 304.54 | 0.11718 | 0.9635 (0.0047) | −0.78 | −1.11 | yes, negative | no change: sign not identified |
| general_public_services | administration excluding E23 (E29+E31) | 304.54 | 0.11718 | 1.0414 (0.0051) | +0.89 | +1.26 | yes | no change: sign not identified |

- **Shares and responses.** These come from the adopted main case, read by `probe_engine.cjs` from `main_case_long_run_2026_09_27/package.cjs` at end specifications 48 and 11. Its positive control reproduces the published band, **$321.819–387.370bn**, to 1e-6 [CALCULATION: derived/engine_lines.json]. POS and health respond at 1 at both ends; GPS responds at 0.600/0.850. The POS share is the corrected line share, 0.13417 (the brief's 13.17% predates the audit corrections).
- **POS amount.** The NIPA S&L POS total of $440.09bn is split by Census FY2024 direct shares: police 37.9%, judicial 14.4%, fire 17.3%, corrections 25.0%, protective inspection 5.4%.
- **SE.** The standard errors are CPS sampling SEs from the 160 replicate weights (4/160 × Σ(θ_r − θ)²). The Census finance CVs are not propagated.
- **corrections.csv columns.** The file has the brief's columns plus `pre_response_bn`, `response_low/high`, `index_min/max_variants` and `candidate`. A synthetic line should carry `pre_response_bn` and take the parent line's response. For GPS, that is the general-government response, not 1.

**Positive controls.**
- The index weighted by all residents (PEP populations) is exactly 1 for every function, year and basis, and the script stops otherwise.
- The CPS civilian-weighted index lies between 0.9982 and 1.0021.
- State sums equal the file's own US row (state 00) to 1e-6.
- The group by state sums to **40,896,574.15**. CA is 13.0828m and TX 9.7615m, which matches `ledger_stress_2026_09_17/derived/state_populations.csv` (the three Mexican groups summed) to 1e-6. [CALCULATION: derived/manifest.json → checks]

## Receipts priced by state (added 2026-09-29, second brief)

For each S&L receipt line keyed at a national rate, index_r = Σ_s c_s·(rate_s / rate_US). The rate is Census FY2024 tax revenue (level 1) per dollar of BEA SAPCE1 personal consumption (mean of calendar 2023 and 2024) for sales taxes, and per resident for motor vehicle licences.
- c_s is the group's population share (the consumption key has no state split). Motor vehicle licences use the group's adult share, since that line's key is adults.
- Receipt gain = S&L part of the line × the group's share (mean of the two methods, at each end's allocation) × (index − 1) × response. It lowers the cost one for one.
- Positive control: the index weighted by each state's own base (PCE, or population) is exactly 1, and the script stops otherwise. [CALCULATION: derived/receipt_indexes.csv, receipts_corrections.csv; DATA: BEA SAPCE.zip, fetched 2026-09-29 to `_cache/`, sha256 pinned in the script]

| Receipt line | Census codes / base | S&L $bn | Group share (low/high) | Index (SE) | Variants | Receipt gain low / high $bn | Clears ±2%? |
|---|---|---:|---:|---:|---:|---:|---|
| general_sales_tax | T09 / PCE | 602.43 | 0.0814 | **1.1151** (0.0057) | 1.110–1.116 | **+5.65 / +5.65** | yes |
| excise_selective_sales (S&L part, 3.5/23) | T10–T16, T19 / PCE | 271.30 | 0.0812 | 0.9893 (0.0040) | 0.979–0.989 | (−0.24) | no: noise, no change |
| personal_motor_vehicle | T24 / resident | 26.13 | 0.1090 / 0.1053 | **1.2624** (0.0111) | 1.244–1.273 | **+0.75 / +0.72** | yes |

- Variants cover FY2023 and FY2024 and population, adult and income (PTOTVAL) weights.
- **Where the sales index comes from:**
  - California's effective general sales tax rate is 0.93× the US (it exempts food and most services, and its PCE is high), which contributes −0.023.
  - Texas is 1.30× (no income tax), contributing +0.072.
  - The rest (AZ, IL, WA and others) contributes +0.067.
- **Motor vehicle licences** come almost entirely from California (1.99×, the vehicle licence fee): +0.33.
- **Pattern.** The mirror of spending holds: California's high taxes are on income, which the account already prices by state, while Texas's and the rest's are on sales, which it priced nationally.

Receipt lines that need no correction (`receipts_corrections.csv`, `candidate=False`):
- `state_local_income_tax` and `other_personal_tax`: key `state_liability` (CPS STATETAX_A), already each state's own tax.
- `modeled_owner_property`: the owner model applies each state's effective property tax rate to reported home value (`generation_account_2026_09_24/keys.py:50`, from `gen_ledger_extension_2026_09_16/state_parameters.csv`). It is already state-priced, and its response is 0.
- `personal_property_tax`, `remaining_production_property`, `other_production_taxes`: key `capital`, response 0 at both ends, so a state index moves nothing. Their incidence also falls on capital owners wherever the property sits, not on the group's state of residence.
- `personal_current_transfers` (fines, fees, donations; federal + S&L): not a tax rate, left national. `customs_duties`: federal.

## Which spending lines share police's per-head logic

The cj lane keys the sublines of `public_order_safety` as follows:
- fire: 100% per head;
- police: ½ per head, ½ arrests;
- courts: 40% per head, 60% arrests;
- prisons: custody;
- CBP and ICE: federal.

Every line or subline with a per-head part is priced at a per-resident cost, so the same state price applies. Outside POS, the population-keyed S&L consumption lines with a nonzero response are GPS (unidentified above), housing and community services, and recreation and culture. Economic affairs is keyed by resources, and schools are already state-priced.

| Line | Function (Census) | S&L $bn | Index (SE) | Low / high $bn | Clears ±2%? | In the consistent package |
|---|---|---:|---:|---:|---|---|
| public_order_safety | fire (E/F24) | 76.27 | 1.1470 (0.0055) | +1.50 / +1.50 | yes | yes |
| public_order_safety | protective inspection (E/F66) | 23.96 | 1.3820 (0.0170) | +1.23 / +1.23 | yes | yes, conditional (below) |
| housing_community_services | housing and community development (E/F50) | 11.77 | 0.9921 (0.0080) | −0.01 | no | no |
| recreation_culture | parks (E/F61) + libraries (E/F52) | 48.90 | 1.0747 (0.0057) | +0.37 / +0.43 (response 0.856/1) | yes | yes |

- **Protective inspection.** NIPA's POS has four sublines (police, fire, law courts, prisons), which sum to $519.15bn in the cj lane's `central_split.csv`, so Census E66 has no NIPA subline of its own. If BEA files it inside police, its $1.23bn is part of police's state price and belongs in the package. If BEA files it outside POS, the S&L POS split should drop E66: police would then be about +$2.73bn and fire about +$1.59bn, and the package would be about $1.0bn smaller. I did not verify where BEA files it. [INFERENCE] **[GAP]**
- **Parks and libraries.** Wage demarcation uses all S&L government pay (QCEW NAICS 10); QCEW has no clean public-parks industry.

## Prisons: priced per state prisoner (third brief)

The first pass called BJS state counts "not local". That was wrong: the full *Prisoners in 2023* PDF was held at `.scratch/clarity-next-20260905/conduct-race/p23st.pdf` (sha256 `22a4cbe8…`, the same file the cj lane's extract pins). It is now copied to `_cache/`, and the script parses Table 2 with `pdftotext -layout`. The parse stops unless it finds 50 states summing to BJS's state totals (1,070,834 in 2022; 1,097,597 in 2023). [DATA: derived/prison_cost_by_state.csv]

- **Price.** State government corrections, Census level 2 (E04+F04, institutions), per prisoner under state jurisdiction on 31 Dec 2023, the middle of FY2024:
  - California $131,421 (2.35× the US);
  - Texas $31,794 (0.57×);
  - US $55,951.
  - Six integrated states (AK CT DE HI RI VT) count jail inmates in both numerator and denominator.
- **Where the group's prisoners are.** Custody by state for the group is not local (the cj lane's ACS custody is national).
  - The central locates the group's prisoners as each state imprisons its residents: weight w_s × prisoners_s/pop_s. This moves weight to Texas, which imprisons at about twice California's rate.
  - The arm uses the group's population share.
  - The truth lies between them. Hispanic Texans are imprisoned at higher rates than Hispanic Californians, but not necessarily at the all-resident ratio. [INFERENCE]
- **Scope.** The index prices the state-prison part of S&L corrections, which is 66.0% of it (level 2 share of level 1 direct; $72.57bn of $109.91bn). Jails (local, level 3) stay national, because jail inmates by state are not held. **[GAP]**

| Weights | FY2024 institutions | FY2024 all corrections (+E05 probation/parole) | FY2023 institutions | Correction $bn |
|---|---:|---:|---:|---:|
| **group × state imprisonment rate (central)** | **1.1031** (SE 0.0113) | 1.0975 | 1.1309 | **+1.00** |
| group population share (arm) | 1.3102 (0.0131) | 1.3151 | 1.3378 | +3.02 |
| all prisoners (positive control) | 1.0000 | 1.0000 | 1.0000 | 0 |

[CALCULATION: derived/prison_per_inmate.csv]

The per-resident index (1.204, +$3.01bn) remains an arm only, because it counts state incarceration-rate differences that the custody key already carries.

## The central rule

The bar decides whether a line opens: at least one of its S&L functions must clear ±2%. Once a line is open, all its S&L sub-functions are priced.
- **Public order and safety** opens (police clears), so courts (+$0.09bn) are priced too. The engine's `use` key applies to the whole line and carries no state pricing (lead, verified in `assumption_explorer_2026_09_21/README.md`), so the state index adds to it and does not double count.
- **Health** is a single function (E32).
- **Recreation** opens (parks and libraries 1.075).
- **Housing** (0.992) and **selective excises** (0.989) do not open.
- **GPS** is the exception: its functions clear in opposite directions depending on E23, so the sign is not identified.
- **Receipts** follow the same rule line by line.

`corrections.csv` now carries `candidate` (central) and `narrow` columns. `net_state_correction.csv` has the two packages, and the script checks that every central line has a function clearing the bar.

## Net state correction

Positive = the group costs more. Values are $bn, low end / high end. [CALCULATION: derived/net_state_correction.csv]

| Package | Spending | Receipts gain | **Net** |
|---|---:|---:|---:|
| **Central:** all S&L POS sub-functions (police, courts, fire, state prisons per prisoner, protective inspection) + health + parks and libraries, less sales and motor vehicle taxes | +8.58 / +8.64 | 6.39 / 6.37 | **+2.19 / +2.27** |
| Central with prisons on population shares (1.310) | +10.59 / +10.66 | 6.39 / 6.37 | +4.20 / +4.29 |
| Central, protective inspection outside NIPA POS (approximate; police about +2.73, fire about +1.59) | about +7.6 | 6.39 / 6.37 | about +1.2 |
| Narrow arm: police + health, less sales and motor vehicle taxes | +4.38 / +4.38 | 6.39 / 6.37 | **−2.01 / −1.99** |

**Recommendation:** integrate the central package as two synthetic lines, one for spending (with per-line responses; `pre_response_bn` × parent response) and one for receipts. The net of about **+$2.2bn** is 0.6% of the band. It is small because two effects of similar size point in opposite directions: the group lives in high-cost California and in high-sales-tax Texas and Arizona. Adopting spending alone would overstate the correction by $6.4bn. [INFERENCE]

## Index variants (group weights)

| Function | FY2024 direct | FY2024 current (E only) | FY2023 direct | FY2023 current | FY2024 direct, adult weights |
|---|---:|---:|---:|---:|---:|
| police | 1.1154 | 1.1087 | 1.1132 | 1.1063 | 1.1271 |
| judicial | 1.0111 | 1.0126 | 1.0199 | 1.0119 | 1.0169 |
| health (E32) | 1.2507 | 1.2546 | 1.2303 | 1.2321 | 1.2747 |
| health + hospitals net of charges (E32+E36−A36) | 1.2533 | 1.2556 | 1.2177 | 1.2213 | 1.2693 |
| health + hospitals gross (E32+E36) | 1.1782 | 1.1760 | 1.1551 | 1.1545 | 1.1897 |
| administration (E23+E29+E31) | 0.9635 | 0.9827 | 0.9810 | 0.9964 | 0.9690 |
| administration excluding E23 | 1.0414 | 1.0980 | 1.0774 | 1.1293 | 1.0478 |

[CALCULATION: derived/indexes.csv]

- **Arrest weighting for police and courts.** The cj lane (`cj_use_allocation_2026_09_23`) has **no state split**: its arrest share is one national FBI 2019 ratio, so arrest-weighted state presence cannot be built from it. The adult-weighted column above is the nearest proxy, since arrests are of adults. It raises police to 1.127 (+$2.84bn) and courts to 1.017 (+$0.14bn, still under the bar).
- **Health.** I use E32, "health" excluding hospitals, because NIPA's $126.84bn is S&L health net of sales to other sectors, and hospital sales are most of those sales ($364.5bn of $491.4bn gross). A gross hospital index would price hospital output that patients and insurers already buy.
  - With hospitals net of hospital charges (E36 + F36 − A36), which is the closest Census analogue of "net of sales", the index is 1.253, almost the same as E32.
  - The gross hospital arm gives 1.178 (+$1.28bn).
  - All three clear the bar, so the choice moves the size, not the sign.

## California against Texas against the rest (FY2024 direct)

Each state's contribution to (index − 1) is w_s·(pc_s/pc_US − 1). The dollars are before the line response. Group weights: CA 0.320 (SE 0.008), TX 0.239 (0.007), rest 0.441.

| Function | CA relative price | TX relative price | CA $bn | TX $bn | Rest $bn | Total index − 1 |
|---|---:|---:|---:|---:|---:|---:|
| police | 1.581 | 0.794 | +4.16 | −1.10 | −0.47 | +0.115 |
| judicial | 1.239 | 0.748 | +0.65 | −0.51 | −0.04 | +0.011 |
| health (E32) | 2.417 | 0.585 | +3.26 | −0.71 | −0.75 | +0.251 |
| administration | 1.119 | 0.689 | +1.36 | −2.65 | −0.02 | −0.037 |
| administration excluding E23 | 1.334 | 0.702 | +3.81 | −2.54 | +0.20 | +0.041 |

[CALCULATION: derived/decomposition.csv] Outside CA and TX, the group lives in states that spend slightly below average on each function. California's high prices drive every positive index, and Texas's low ones offset part of it.

## Wage demarcation

Higher-paying states spend more for the same service. That is still a resource cost, and the schools precedent charges it, so the table below only separates wage level from quantity; it does not propose removing the wage part. Each state's relative spending is divided by its relative average pay for state and local government in the function (BLS QCEW 2023, own codes 2+3, the function's NAICS). The "real" index is the group's quantity-weighted index over the all-resident one. [CALCULATION: derived/wage_demarcation.csv; DATA: sources/immigration-fiscal/data/bls/qcew_2023_annual_by_industry.zip]

| Function | Index | Group wage level | Real (quantity) index | Wage part of the gap |
|---|---:|---:|---:|---:|
| police (922120) | 1.115 | 1.077 | 1.017 | ~86% |
| judicial (922110+922130) | 1.011 | 1.091 | 0.917 | all of it and more (real < 1) |
| health (923120, a weak proxy) | 1.251 | 1.054 | 1.094 | ~63% |
| administration (921) | 0.964 | 1.132 | 0.868 | real < 1 |
| administration excluding E23 (921) | 1.041 | 1.132 | 0.920 | real < 1 |

- **Police.** The police premium is almost all California pay: in quantity terms the group lives where police input per resident is about average.
- **Health.** Health keeps a real premium of about 9%.
- **Suppressed QCEW cells** fall back to all state and local government pay in the state. They are listed per function in the CSV (police: AK, DE, DC, MD, WY) [DATA].

## Administration: why no change

`derived/admin_by_year.csv`, current operations, 50 states (DC weight 0.03% dropped) [CALCULATION; DATA: administration_response_2026_09_20/derived/panel.csv]:

| Year | 2012 | 2017 | 2018 | 2019 | 2021 | 2022 | 2023 | 2024 (this file) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| with E23 | 0.969 | 0.957 | 0.963 | 0.943 | 0.961 | 1.032 | 0.999 | 0.983 |
| excluding E23 | 1.016 | 1.040 | 1.057 | 1.058 | 1.085 | 1.114 | 1.134 | 1.098 |

- **Before the break** (FY2021 and earlier), complete administration sits 3–6% **below** 1, because Texas spends little per resident on financial administration.
- **The E23 level break of FY2022** (register, "Do not use without checking" item 6) lifts it toward 1.
- **Excluding E23**, the index is above 1 and rising in every year. That arm drops 40–60% of the function, and its FY2024 value moves from 1.04 (direct) to 1.10 (current) because of capital outlay.
- **Across years and arms** the correction runs from −$1.2/−1.7bn (FY2019, with E23) to +$4.1bn (FY2023, excluding E23, high end) after the 0.60/0.85 response, straddling zero.
- **Other gaps.** Census administration covers about 58% of NIPA S&L GPS ($177bn of $304.5bn), so the index also has to stand in for the rest. [INFERENCE] The sign is not identified, so I recommend no change.

## Disconfirmation

- **Stability.** Police (1.106–1.115) and health (1.230–1.255) hold across two fiscal years and both bases, with replicate SEs of 0.006 and 0.015. Neither comes near the bar. [CALCULATION]
- **Is health one outlier state?** California's E32 is $1,127 per resident, against $464 nationally (2.42×), and its CV is 0.25%, so it is not a sampling artifact of the finance survey. [DATA: derived/state_per_capita.csv] Without California the health index would fall below 1. The correction therefore rests on California's county health spending (public and behavioral health). [INFERENCE] **[GAP]** Part of that spending may serve the uninsured, whom the account already charges through `medicaid_and_chip_other_medical` on the uninsured-use key. The dollars do not double count: they are different NIPA cells. But the index may give the group a price premium for services whose use the key does not show. I did not test this.
- **Key interaction.** The index scales the whole line share. For police, the cj central subline share is 0.1307 against the line's 0.1342. Using it would cut the police correction by about 3% (to about +$2.51bn). [CALCULATION: cj_use_allocation_2026_09_23/RESULT.md subline table × this index]
- **Level of geography.** This is state level only. The schools lane found the group's districts spend 2.5% more than their state averages (Los Angeles, NYC, Chicago, Dallas). The same pattern is plausible for police and health (Los Angeles County), which would push both corrections up, not down. **[GAP]** A county-level arm would need the unit file's county governments joined to CPS county (identified only for large counties). [INFERENCE]
- **Per-resident price is the wrong unit for corrections.** Corrections (+$3.01bn, index 1.204) clears the bar but stays `candidate=False`: it is keyed by custody, and per-resident spending mixes incarceration rates with cost per inmate. The central package instead uses the per-prisoner price (see "Prisons: priced per state prisoner"); jails remain a **[GAP]**. Fire and protective inspection moved into the package in the second brief.
- **Receipts disconfirmation.**
  - The sales index holds at 1.110–1.116 across years and weights.
  - Per dollar of PCE is the right base for a consumption-keyed share. Per resident gives a different number, because PCE per head varies: the all-resident population-weighted index is 1.010.
  - Part of S&L general sales tax falls on business inputs. That changes the level of each state's effective rate but not obviously its ranking. **[GAP]** A state business-input share (COST/EY studies) would test it.

## Files covered and skipped

- **Covered:**
  - CPS ASEC 2025 pppub25, hhpub25 and repwgt;
  - Census FY2024 and FY2023 `statetypepu` (level 1);
  - NST-EST2024-ALLDATA;
  - QCEW 2023 annual;
  - `administration_response_2026_09_20/derived/panel.csv`;
  - `ledger_stress_2026_09_17/derived/state_populations.csv` (check);
  - the main-case package (read only; receipts at the end specifications, mean of the two methods);
  - BEA SAPCE (`_cache/SAPCE.zip`, fetched 2026-09-29, sha256 pinned);
  - Census T09–T19 and T24 from the same statetypepu files.
- **Skipped:**
  - the Census PID file's state populations, which are the Vintage 2022 estimates (CA 39,029,342), so PEP Vintage 2024 is used, as the mean of July 1 of the two years each fiscal year spans;
  - county-level finance (out of scope; see [GAP]);
  - the cj arrest data by state (does not exist).

## Reproduce

```sh
cd ~/Projects/immigration-research
node infra/immigration-fiscal/state_priced_services_2026_09_29/probe_engine.cjs      # -> derived/engine_lines.json
OPENBLAS_NUM_THREADS=1 uv run --no-project --offline python3 infra/immigration-fiscal/state_priced_services_2026_09_29/state_price.py
```

Outputs:
- `derived/group_population_by_state.csv`: reusable, with 51 states, the group, its share and replicate SE, adults and CPS civilians.
- `state_per_capita.csv`
- `indexes.csv`
- `decomposition.csv`
- `wage_demarcation.csv`
- `admin_by_year.csv`
- `corrections.csv`
- `engine_lines.json`
- `manifest.json`: input sha256 and checks.
- `receipt_indexes.csv`, `receipts_corrections.csv`, `net_state_correction.csv` (second brief).
- `prison_per_inmate.csv`, `prison_cost_by_state.csv` (third brief; BJS p23st Table 2 parsed from `_cache/p23st.pdf`, which needs poppler `pdftotext`).

Both scripts were rerun with `--out-dir` to scratch (rc 0 for both), and all 9 outputs are byte-identical.

## Log

- 2026-09-29 00:17 JST: lane started, stub written.
- 2026-09-29 00:23 JST: probe reproduces the main case ($321.819–387.370bn). First run done; the admin-by-year arm and the ledger_stress check were added. Rerun to scratch gave byte-identical outputs.
- 2026-09-29 00:24 JST: RESULT written; admin range recomputed from admin_by_year.csv.
- 2026-09-29 00:33 JST (second brief): receipts side added (SAPCE fetched), plus the per-head consistency lines (fire, protective inspection, housing, parks) and the net correction. Candidates now require clearing ±2%, so administration excluding E23 is no longer flagged. Prisons skipped (not local). Both scripts rerun to scratch: rc 0, 12 of 12 outputs byte-identical.
- 2026-09-29 00:47 JST (third brief): prisons priced per state prisoner from the held BJS p23st PDF, correcting the earlier "not local". The central package now prices all five S&L POS sub-functions by the line-opening rule, with police + health as the narrow arm, and the candidate flags match the verdict. Rerun to scratch: rc 0, 14 of 14 outputs byte-identical.

## Lead verification (2026-09-29 00:53 JST)

- Reran both scripts in place with `scripts/rerun_lane.py`: rc 0, 17 of 17 files byte-identical.
- Arithmetic re-derived by hand: police 166.748 × 0.13417 × 0.11537 = 2.58; health 126.839 × 0.05660 × 0.25066 = 1.80; sales tax 602.43 × 0.08142 × 0.11512 = 5.65; state prisons 72.57 × 0.13417 × 0.1031 = 1.00.
- The group-by-state file sums to 40,896,574 (CA 13.08m, TX 9.76m).
- The engine's `use` key for public order and safety is the national per-head allocation plus the justice lane's +$5.94bn (`assumption_explorer_2026_09_21/README.md`). It carries no state pricing, so the index adds to it.
- Protective inspection [GAP] resolved in favour of the central: BEA's comparison of classifications maps NIPA "Public order and safety" to the Census function group "Public safety", and that group contains protective inspection and regulation. [SOURCE: BEA, "Government Spending by Function", *Survey of Current Business*, June 2000, p. 21, https://apps.bea.gov/scb/pdf/national/niparel/2000/0600gf.pdf] The table is from 2000 and works at group level, so ±$1.0bn of uncertainty remains.
