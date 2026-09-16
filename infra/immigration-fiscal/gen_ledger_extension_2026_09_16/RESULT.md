**Verdict:** The sign does not change and the magnitude gets worse. Every one of the three added taxes and the added K-12 cost moves the Mexican-second-generation balance *further* below third-plus non-Hispanic whites, because all four items scale with earnings, home value or child count, and the Mexican second generation is lower on the first two and higher on the third. Under the memo's headline construction (equal shares among all resource-unit members, person weights, adults 25-64) the gap goes from **−6,066 (se 353)** to **−8,286 (se 443)** per adult per year, a 37% widening. Under the equal-shares-among-adults-18+ construction it goes from −7,625 to −10,633 (se 587). No sensitivity arm I ran reverses or even meaningfully shrinks this: the eight variants span −8,123 to −8,555 on the headline construction. [DATA: CPS ASEC 2025 public-use file, sha256 318845a2… , 160-replicate SDR] [INFERENCE for the reading]

`[UNVERIFIED]` markers are used below for the two items that are modeled from published aggregate rates rather than measured in the microdata.

## Step A — baseline reproduction: PASS

```
-- STEP A reproduction check --
Mexican 2nd gen minus 3rd+ NH white, taxes minus selected transfers,
equal_all_members allocation, person weights, adults 25-64: -6,066 (se 353)
Published in research/immigration-mexican-origin-by-generation-2026-09-16.md table 5: -6,066 (se 353)
Deviation from the published -6,066: +0.17
[reproduction check] PASS (within $50 of the published -6,066)
```

The reproduction is exact to 17 cents because `extend_ledger.py` imports `prepare()`, `allocate()`, `estimate()` and `summarize()` from `infra/immigration-fiscal/build/analyze_cps_fiscal_2025.py` and rebuilds the group masks with the same code, rather than re-implementing them. All of that script's integrity gates run unchanged: the federal refundable-credit identity, SPM-unit dollar conservation, the head-weight/person-weight agreement, the unit-field constancy checks.

Note on the brief's wording: the published **−6,066** is the `equal_all_members` allocation, not `equal_adults_18plus`. The 18+ allocation gives −7,625 in the peer result file and in my run. Both are reported below.

## Step E — extended ledger, `equal_all_members` allocation, person weights, adults 25–64

Annual dollars per adult, 2024 income year, SDR standard error in parentheses. Transfer and cost rows are shown as positive amounts (the layout of memo §5), so a larger number in those rows is a larger outflow.

| | 3rd+ NH white | All natives | All 2nd gen | Mexican 2nd gen | Mexican 3rd+ | Mexico-born |
|---|---|---|---|---|---|---|
| Modeled taxes (payroll + federal + state) | 14,383 (238) | 13,110 (184) | 13,653 (351) | 7,419 (268) | 9,149 (440) | 4,874 (221) |
| Selected cash transfers | 2,453 (48) | 2,451 (38) | 1,823 (73) | 1,460 (102) | 2,049 (134) | 860 (63) |
| Selected non-cash transfers | 145 (4) | 188 (4) | 167 (7) | 240 (14) | 232 (16) | 246 (13) |
| **= Taxes minus selected transfers** | **11,785 (250)** | **10,472 (195)** | **11,663 (361)** | **5,719 (278)** | **6,868 (468)** | **3,768 (230)** |
| + Employer payroll tax | 3,489 (28) | 3,307 (22) | 3,494 (49) | 2,542 (52) | 2,852 (62) | 1,895 (37) |
| + Sales/excise tax (0.35 taxable share) | 1,050 (10) | 997 (8) | 1,043 (16) | 784 (16) | 893 (22) | 592 (12) |
| + Property tax (owner-occupied) | 1,313 (16) | 1,180 (12) | 1,313 (32) | 765 (29) | 808 (28) | 518 (25) |
| − K-12 public schooling | 1,652 (23) | 1,690 (19) | 1,855 (47) | 2,112 (86) | 1,715 (69) | 2,311 (62) |
| **= EXTENDED BALANCE** | **15,984 (292)** | **14,266 (232)** | **15,658 (439)** | **7,698 (375)** | **9,705 (561)** | **4,462 (290)** |

Difference from third-plus non-Hispanic white, same rows:

| | All natives | All 2nd gen | Mexican 2nd gen | Mexican 3rd+ | Mexico-born |
|---|---|---|---|---|---|
| Modeled taxes | −1,273 (104) | −730 (399) | −6,965 (330) | −5,234 (438) | −9,509 (325) |
| Selected cash transfers | −2 (26) | −630 (86) | −994 (119) | −404 (146) | −1,593 (84) |
| Selected non-cash transfers | 42 (3) | 21 (8) | 95 (15) | 86 (17) | 101 (14) |
| **Taxes minus selected transfers** | **−1,313 (106)** | **−122 (413)** | **−6,066 (353)** | **−4,916 (456)** | **−8,016 (338)** |
| Employer payroll tax | −182 (13) | 5 (52) | −946 (55) | −637 (63) | −1,594 (44) |
| Sales/excise tax | −53 (5) | −7 (18) | −266 (18) | −157 (22) | −457 (15) |
| Property tax | −133 (8) | 0 (35) | −548 (33) | −505 (31) | −795 (29) |
| K-12 schooling (cost, so + means more cost) | 38 (13) | 204 (51) | 460 (90) | 64 (68) | 660 (69) |
| **EXTENDED BALANCE** | **−1,719 (124)** | **−327 (488)** | **−8,286 (443)** | **−6,279 (546)** | **−11,522 (402)** |

### What fraction of the −6,066 gap each addition closes or widens

| Addition | Effect on the gap | Share of the −6,066 baseline gap | Running gap |
|---|---|---|---|
| Employer payroll tax | −946 | widens 15.6% | −7,012 |
| Sales/excise tax (0.35 share) | −266 | widens 4.4% | −7,278 |
| Property tax (owner-occupied) | −548 | widens 9.0% | −7,826 |
| K-12 public schooling | −460 | widens 7.6% | −8,286 |
| **Extended gap** | | **136.6% of baseline** | **−8,286 (se 443)** |

Nothing closes any of it. The reason is structural: the ledger's gap was already almost entirely a tax-side gap (the Mexican second generation pays $6,965 less modeled tax and receives $994 *less* in selected cash transfers), and all three added taxes are functions of the same earnings and the same wealth that produce the original tax gap. K-12 is the only item that could in principle have gone either way, and it goes against the group because their resource units hold 0.149 children aged 5–17 per adult against 0.119 for white natives.

## Same table, `equal_adults_18plus` allocation

| | 3rd+ NH white | All natives | All 2nd gen | Mexican 2nd gen | Mexican 3rd+ | Mexico-born |
|---|---|---|---|---|---|---|
| = Taxes minus selected transfers | 14,409 (286) | 12,669 (224) | 14,282 (442) | 6,784 (382) | 8,093 (528) | 4,023 (251) |
| + Employer payroll tax | 4,291 (30) | 4,053 (24) | 4,276 (55) | 3,215 (61) | 3,522 (70) | 2,362 (41) |
| + Sales/excise tax | 1,283 (12) | 1,220 (9) | 1,291 (19) | 1,005 (21) | 1,112 (25) | 749 (13) |
| + Property tax | 1,617 (18) | 1,454 (14) | 1,661 (38) | 964 (36) | 1,019 (36) | 648 (27) |
| − K-12 public schooling | 3,501 (56) | 3,621 (48) | 3,881 (116) | 4,501 (213) | 3,660 (170) | 4,628 (156) |
| **= EXTENDED BALANCE** | **18,099 (333)** | **15,776 (267)** | **17,629 (544)** | **7,466 (515)** | **10,086 (652)** | **3,154 (354)** |
| Difference from 3rd+ NH white | — | −2,323 (144) | −470 (609) | **−10,633 (587)** | −8,013 (634) | −14,945 (475) |

On this allocation the baseline gap is −7,625 and the extended gap is −10,633, again 139% of baseline. The K-12 charge roughly doubles because the cost is spread over adults only.

## Sensitivity: eight variants of the extended balance (headline allocation)

| Variant | 3rd+ NH white | Mexican 2nd gen | Gap (se) |
|---|---|---|---|
| Base (0.35 taxable share, owner property, ACS native pupil ratio) | 15,984 | 7,698 | −8,286 (443) |
| Taxable consumption share 0.25 | 15,685 | 7,474 | −8,210 (439) |
| Taxable consumption share 0.45 | 16,284 | 7,922 | −8,362 (447) |
| Sales tax from ITEP effective-rate schedule | 16,747 | 8,201 | −8,546 (446) |
| Renter property-tax pass-through added | 16,289 | 8,165 | −8,123 (444) |
| Pupil ratio flat 0.90 (the brief's fallback) | 15,784 | 7,442 | −8,342 (447) |
| Pupil ratio differential (0.803 white/native, 0.905 Mexican-origin) | 15,984 | 7,430 | −8,555 (447) |
| Net of SPM school lunch (avoid double-counting food services) | 16,026 | 7,783 | −8,243 (442) |

The full span is −8,123 to −8,555. The renter arm is the most gap-friendly assumption available and it still leaves the gap 34% wider than baseline.

## Sources

| Item | Source |
|---|---|
| CPS ASEC 2025 public-use microdata (income year 2024) | https://www2.census.gov/programs-surveys/cps/datasets/2025/march/asecpub25csv.zip — sha256 `318845a2b5e0034eb2973898de1738f4df0025727de38499e7669cb9c0deef0b`, byte-identical to the file the peer generator used (`manifest.json` from `.scratch/mexgen-20260916/fiscal/cps-health/`) |
| OASDI taxable wage base 2024 = $168,600 | IRS Publication 15 (2024), page 2: "The social security wage base limit is $168,600." https://www.irs.gov/pub/irs-prior/p15--2024.pdf |
| Employer payroll rates 6.2% OASDI (capped) + 1.45% HI (uncapped) | Same publication |
| Combined state + average local sales tax rate, 1 January 2024, by state | Tax Foundation, *State and Local Sales Tax Rates, 2024*, Table 1. https://taxfoundation.org/data/all/state/2024-sales-taxes/ — staged to `taxfoundation_2024_state_sales_tax_rates.csv` |
| Sales-and-excise effective rates for the ITEP arm (7.0% lowest quintile, 4.8% middle quintile, 1.0% top 1%) | ITEP, *Who Pays?* 7th edition, January 2024. https://itep.org/whopays-7th-edition/ |
| Per-pupil current spending, FY2024, national $17,619 and by state | U.S. Census Bureau, 2024 Annual Survey of School System Finances, Summary Table 8. https://www2.census.gov/programs-surveys/school-finances/tables/2024/secondary-education-finance/elsec24_sumtables.xlsx — release: https://www.census.gov/newsroom/press-releases/2026/school-system-finances.html |
| Public pupils per child aged 5–17 (0.8027 native households, 0.9048 Mexico-born households) | Repo's own `infra/immigration-fiscal/build/measure_acs_school_exposure_2024.py` on ACS 2024 PUMS, results in `.scratch/clarity-next-20260905/fiscal/schools/school_exposure.csv` |
| State effective property tax rate on owner-occupied housing | ACS 2023 1-year B25103_001E ÷ B25077_001E via the Census Data API. Validated against Tax Foundation's CY2022 published effective rates: Alabama 0.36% vs 0.36%, Hawaii 0.27% vs 0.26%, Illinois 1.93% vs 1.95%, New Jersey 1.99% vs 2.08%, Arizona 0.44% vs 0.45%. https://taxfoundation.org/data/all/state/property-taxes-by-state-county-2024/ |
| State median gross rent (renter pass-through arm) | ACS 2023 1-year B25064_001E via the Census Data API |
| NCES cross-check on the per-pupil level | Digest of Education Statistics 2023, Table 236.55: 2020-21 current expenditure per pupil in fall enrollment $14,295 unadjusted, $16,280 in constant 2022-23 dollars. https://nces.ed.gov/programs/digest/d23/tables/dt23_236.55.asp. The Census FY2024 figure is used because the ledger's income year is 2024, and because it is what the repo's September 5 fiscal memo already cites. |

## Assumptions, stated

1. **Employer payroll** [DATA + rate applied]. 6.2% of wage-and-salary earnings (`WSAL_VAL`) up to $168,600 plus 1.45% of all such earnings. Self-employment and farm self-employment income are **excluded** because the Census FICA field already carries both halves of SECA for them; including them would double count. This is why employer payroll comes to 91–94% of the modeled personal `FICA` field rather than 100%.
2. **Sales and excise** [UNVERIFIED — modeled from an aggregate rate, no consumption is observed in CPS ASEC]. Base case follows the brief exactly: state combined rate × min(income, 0.9 × income) × 0.35 taxable share, i.e. 0.315 × income × rate. Income is the SPM unit's `SPM_RESOURCES` (post-tax, post-transfer resources), floored at zero, which is the closest thing in the file to a consumption capacity. The rate is the state of the unit head's household. **This model is demonstrably low.** It implies roughly 2.2% of resources for white natives, against ITEP's published 4.8% for the middle quintile. The ITEP arm applies ITEP's own effective-rate schedule directly and is the better-grounded variant; it widens the gap slightly more (−8,546). ITEP's Q2, Q4 and Q5 rates (5.9%, 4.0%, 3.0%) are my interpolation between their published lowest-quintile, middle-quintile and top-1% anchors, not ITEP figures.
3. **Property tax** [UNVERIFIED — modeled; CPS ASEC has no property-tax-paid field]. CPS ASEC 2025 carries no `PROP_TAX` variable (checked: 844 person-file columns, none matching `PROP`; the household file has `HPROP_VAL`, a house *value*). Owner-occupied households (`H_TENURE` = 1) are charged state effective rate × `HPROP_VAL`, split evenly across household members and summed into SPM units, which conserves the household total across the SPM units inside it. **Renters are charged zero in the base case**, as the brief directs. The renter sensitivity charges 15% of annual rent proxied by the state median gross rent, because no rent amount exists in the file; that arm narrows the gap by $163, to −8,123.
4. **K-12** [DATA for the child counts, modeled for attendance and price]. CPS ASEC has **no school-enrollment field for children under 16** (`A_ENRLW` is populated only for ages 16–24 and carries no public/private split), so enrollment cannot be measured here and the brief's fallback applies. Children aged 5–17 in the SPM unit are counted from the microdata, multiplied by a public-pupil-per-child ratio and by the state's FY2024 per-pupil current spending, then allocated like any other unit resource. The base ratio is 0.8027, the repo's own ACS 2024 measurement of public pupils per child 5–17 in native households, rather than the brief's flat 0.90, because it is measured rather than assumed; the 0.90 arm and a differential arm (0.9048 for Mexican-origin and Mexico-born groups, the ACS Mexico-born figure) are both reported and both widen the gap further.
5. **Attribution of the children's cost** [FRAMING-SENSITIVE, stated as the brief directs]. A child of Mexican-second-generation parents is *third* generation by the repo's own definition, so the child is not a member of the group being measured. The cost is nevertheless charged to the adults' group, exactly as SNAP, WIC and school lunch already are in the baseline ledger, because the question is the balance of the resource unit those adults live in. The alternative framing, charging each generation only its own members' schooling, would move most of the K-12 cost onto the group the children belong to and would make the second-generation comparison look better.
6. **Average, not marginal, cost.** Per-pupil current spending is an average. The marginal cost of one more pupil in an existing system is lower. The same caveat the September 5 fiscal memo attaches to its school scenario applies here.
7. **Food services double-count.** Census "current spending" includes school food services, and the baseline ledger already subtracts the SPM school-lunch resource. The `extended_balance_net_of_school_lunch` arm adds the lunch resource back before charging schools; it moves the gap by $43.
8. **SPM units are not ACS households.** The children-per-adult ratios here are computed inside SPM resource units, which are narrower than the ACS households the prior school-exposure script used. Under the 18+ allocation this run finds 0.203 pupils per white-native adult and 0.208 per adult across all natives, against the ACS script's 0.2155 for all natives, and 0.268 per Mexico-born adult (0.302 on the differential arm) against the ACS script's 0.3266. The SPM construction therefore charges the Mexico-born group **less** school cost than the ACS household construction would.
9. Sampling error only. The SDR standard errors cover CPS sampling. They do not cover error in any of the applied rates, in the transport of state averages to individual units, or in CPS income under-reporting.

## What remains outside the ledger

- **Institutional care.** Medicaid nursing-home and long-term-care spending, prisons and jails, and the institutional population generally. MEPS-HC is non-institutional, so the life-cycle version's health figures miss this too. A separate lane (`infra/immigration-fiscal/acs_institutional_2026_09_16/`) is working the ACS institutional population.
- **Corporate income tax**, and any incidence of it assigned to workers or shareholders.
- **Public health spending** is in the life-cycle version of the peer ledger but not in this annual table, which extends only the annual construction the memo's §5 table reports.
- **Medicare and Social Security accrual.** The ledger counts benefits received this year, not claims accrued. A younger group with lower lifetime earnings accrues less future benefit, which this annual snapshot does not credit.
- **Pure public goods.** Defense, debt service, general government administration, courts, diplomacy. Whether these are charged per capita or treated as non-rival is the single largest discretionary choice in any fiscal-impact accounting, and it is not made here.
- **Indirect and general-equilibrium effects.** Wage and price effects on natives, capital deepening, complementarity in production, fiscal effects on other residents' incomes and therefore their taxes. The Borjas–Katz versus Card–Peri dispute in memo §4 is exactly this channel and it is not in any accounting ledger.
- **Excise taxes not proxied by the consumption model**: motor fuel, tobacco, alcohol, telecoms. The ITEP arm implicitly includes them; the base 0.35-share arm nominally covers "sales/excise" with a general sales rate and so understates them.
- **Unauthorized status.** No status is observed anywhere in this file. Noncitizens include lawful permanent residents.
- **Tax compliance.** Census models liability, not payment.

## Verification commands, run and pasted

```
$ cd /Users/alien/Projects/immigration-research && uv run python3 infra/immigration-fiscal/gen_ledger_extension_2026_09_16/extend_ledger.py
EXIT=0
...
-- STEP A reproduction check --
Mexican 2nd gen minus 3rd+ NH white, taxes minus selected transfers,
equal_all_members allocation, person weights, adults 25-64: -6,066 (se 353)
Published in research/immigration-mexican-origin-by-generation-2026-09-16.md table 5: -6,066 (se 353)
Deviation from the published -6,066: +0.17
[reproduction check] PASS (within $50 of the published -6,066)

Wrote .../extended_ledger_by_generation.csv
Wrote .../extended_ledger_result.txt
```

```
$ rg -n "6,066|6066" infra/immigration-fiscal/gen_ledger_extension_2026_09_16/extended_ledger_result.txt
28:= Taxes minus selected transfers                             —      -1,313 (106)        -122 (413)      -6,066 (353)      -4,916 (456)      -8,016 (338)
36:   baseline gap (taxes minus selected transfers): -6,066
118:equal_all_members allocation, person weights, adults 25-64: -6,066 (se 353)
119:Published in research/immigration-mexican-origin-by-generation-2026-09-16.md table 5: -6,066 (se 353)
120:Deviation from the published -6,066: +0.17
RG_EXIT=0
```

Both PASS.

## Files in this lane

| File | What |
|---|---|
| `extend_ledger.py` | The run. Imports the peer generator, adds the four items, writes both outputs. |
| `stage_inputs.py` | Builds `state_parameters.csv` from the four staged source files. No network. |
| `state_parameters.csv` | 51 rows: sales tax rate, property tax effective rate, median gross rent, per-pupil spending, keyed by GESTFIPS. |
| `extended_ledger_by_generation.csv` | Long format: allocation × group × metric, estimate, SDR se, difference from third-plus NH white and its se. 300 rows, 25 metrics. |
| `extended_ledger_result.txt` | The printed tables, both allocations, plus the step-A check. |
| `taxfoundation_2024_state_sales_tax_rates.csv`, `acs2023_state_proptax_medians.json`, `acs2023_state_median_gross_rent.json`, `census_assf_fy2024_summary_tables.xlsx` | Staged source files, as downloaded. |
| `_cache/asecpub25csv.zip` | The CPS ASEC 2025 public file (147 MB, gitignored). The 2TBPNY SSD holding the original was not mounted, so the script re-downloaded from census.gov and verified the sha256 against the peer run's manifest. |

## One note on inputs

`/Volumes/2TBPNY` was **not mounted** during this run, so the paths in the peer generator's `manifest.json` were unreachable. `extend_ledger.py` resolves the CPS file through `CPS_ASEC_2025_ZIP`, then `PNY_DATA_ROOT`, then the 2TBPNY path, then a lane-local cache it will download from census.gov and sha-verify. The downloaded file is byte-identical to the one the peer run used, so this is not a degradation.
