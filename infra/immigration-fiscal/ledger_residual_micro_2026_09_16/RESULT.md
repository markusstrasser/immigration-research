# Person-level ledger residuals by origin-generation

Model self-report: claude-opus-5[1m] (Opus 5, 1M context)

**Verdict:** No. Not one of the five residual items moves the Mexican-second-generation gap to third-plus non-Hispanic whites by more than $500, in either direction. The largest single item is uncompensated hospital care at **−$120** (widening), and the whole CPS-side package moves the gap from **−8,286 (se 443)** to **−8,470 (se 446)**, a widening of $184 or 2.2%. Institutional care is the only item that can go either way: priced as specified it *narrows* the gap by $48 (the Mexican-origin population is young, and the expensive institutional population is the 65+ nursing-home one, which is disproportionately white), and only the most adverse pairing of two contested assumptions (generic-Hispanic prison-coding adjustment plus a 62% Medicaid-payer share on nursing facilities) pushes it to −$363 and the total move to −$547. The full span across every arm is **−8,325 to −8,833**. The sign does not change, the magnitude barely moves, and the reason is the same one the peer lane found: the gap is a tax-side gap, and none of these items is a tax. [DATA: CPS ASEC 2025 public-use file + ACS 1-year PUMS 2023 via the Census API, 160-replicate SDR] [INFERENCE for the reading]

[UNVERIFIED] marks every row priced from a published aggregate rate rather than measured in the microdata: the higher-education subsidy, the APTC dollar value, uncompensated care, and all of institutional care.

## Step A gate: PASS

```
-- STEP A gate: peer-lane extended balance --
Mexican 2nd gen minus 3rd+ NH white, EXTENDED balance, equal_all_members,
person weights, adults 25-64: -8,286 (se 443)
Published in gen_ledger_extension_2026_09_16/RESULT.md and memo §12: -8,286 (se 443)
Deviation from the published -8,286: -0.23
[Step A gate] PASS (within $50 of the published -8,286)
```

Reproduced to 23 cents because `residual_micro.py` calls `extend_ledger.build()` directly, which itself calls `prepare()`, `allocate()` and `estimate()` from `build/analyze_cps_fiscal_2025.py`. Nothing is re-implemented: the group masks, SPM resource units, employer-payroll/sales/property/K-12 additions, the composite and the 160-replicate SDR variance are the peer lane's own objects. All of the base generator's integrity gates run unchanged (federal refundable-credit identity, SPM dollar conservation, unit-field constancy, weight agreement), plus `allocate()`'s per-unit conservation assertion on every new item.

## §12 layout, `equal_all_members`, adults 25–64, $ per adult per year

Each row is the item as a difference from third-plus non-Hispanic whites; a negative number means the group's balance falls further below whites. SDR standard error in parentheses on the balances.

| | All natives | All 2nd gen | Mexican 2nd gen | Mexican 3rd+ | Mexico-born |
|---|---|---|---|---|---|
| **Extended balance (peer lane baseline)** | **−1,719 (124)** | **−327 (488)** | **−8,286 (443)** | **−6,279 (546)** | **−11,522 (402)** |
| − Government educational assistance | −13 | −45 | −25 | −8 | −12 |
| running balance | −1,732 (125) | −371 (489) | −8,312 (447) | −6,287 (547) | −11,535 (401) |
| − Public higher-education subsidy | −4 | −28 | −50 | −34 | −136 |
| running balance | −1,736 (124) | −399 (489) | −8,362 (446) | −6,320 (548) | −11,671 (401) |
| − ACA premium tax credits | −8 | −27 | **+11** | +11 | +13 |
| running balance | −1,744 (125) | −426 (490) | −8,350 (446) | −6,309 (550) | −11,658 (402) |
| − Uncompensated hospital care | −18 | −39 | **−120** | −65 | −383 |
| running balance | −1,762 (125) | −465 (490) | −8,470 (447) | −6,374 (551) | −12,040 (402) |
| − Other public transfers | −5 | −7 | −0 | −59 | +3 |
| **= Residual balance, CPS items** | **−1,767 (125)** | **−472 (490)** | **−8,470 (446)** | **−6,433 (555)** | **−12,037 (401)** |
| − Institutional care (ACS proxy, base) | −229 | −229 | **+48** | +48 | **+719** |
| **= Full residual balance** | **−1,996** | **−701** | **−8,422** | **−6,386** | **−11,318** |

Levels, same allocation, for the reference group: whites receive $56 of government educational assistance, $138 of higher-education subsidy and $208 of premium tax credits, and generate $114 of uncompensated care and $1,105 of institutional care, per adult 25–64 per year.

`equal_adults_18plus`: baseline −10,633 (587) → CPS residual −10,897 (592) → full −10,849. The same conclusion, moved $216 instead of $184, because every item is spread over fewer people.

## Item by item

**1a. Government educational assistance — measured, small.** `ED_VAL` is the *combined* amount of Pell grant plus other educational assistance; the file carries only source flags, never a per-source amount (`OED_TYP1` other government, `OED_TYP2` school scholarships, `OED_TYP3` employers/friends). The base rule counts the whole amount as public when a government source is reported or when no private source is reported at all (the Pell-only case). 2,948 unweighted recipients, 536 with a government source, 1,740 private-only. A proportional source split instead of the base rule moves the Mexican-second-generation difference from +25 to +19. Nothing here reaches $50.

**1b. Public higher-education subsidy — measured enrollment, modeled price.** `A_ENRLW = 1` and `A_HSCOL = 2` at ages 18–24, full-time weighted 1.0 and part-time 0.5 for FTE, times the NCES fall-2023 public undergraduate share (0.7726) times SHEEO's FY2024 education appropriations per FTE ($11,683). 3,961 unweighted enrollees. The Mexican second generation draws $188 against whites' $138, so this *widens* by $50; the Mexico-born draw $275, widening by $136. At the brief's 0.74 fallback share the effect is $48 rather than $50.

**2. ACA premium tax credits — measured, and the only item that helps.** `MRKS` ("Any subsidized Marketplace coverage last year") is a direct subsidy indicator, so no fallback was needed; it was computed anyway as a cross-check. 5,924 unweighted persons with any marketplace coverage, 4,089 subsidised, 1,851 unsubsidised. At CMS's full-plan-year-2024 average of $527.64 per month per APTC enrollee, the Mexican second generation receives $197 against whites' $208, **narrowing** the gap by $11. The fallback construction (any marketplace × 93.15% national subsidised share) reverses the sign to −65, because whites hold proportionally more *unsubsidised* marketplace coverage; the measured indicator is the right one and is reported as the base.

**3. Uncompensated hospital care — the largest residual, and the least like a government outlay.** Full-year-uninsured persons (`NOCOV_CYR = 3`, 11,062 unweighted) are charged the full annual amount and part-year-uninsured (`NOCOV_CYR = 2`, 4,271) half of it, at $1,524 per uninsured person-year (AHA $42.67bn in 2020 ÷ Census 28.0 million uninsured in 2020). The Mexican second generation generates $234 against whites' $114, widening by $120; the Mexico-born generate $497, widening by $383. At 2024 hospital prices (a 1.20 uplift) those become $144 and $459. **This is not a government expenditure.** It is an unpaid hospital cost, a large but unquantified share of which is recovered through Medicare and Medicaid disproportionate-share and supplemental payments, which the MEPS transport in the peer ledger already counts on the paid side. Keeping it in the running balance double counts to that extent, so treat it as an upper bound on this item.

**4. Institutional care — the only item whose sign is genuinely open.** ACS 2023 1-year PUMS, `TYPEHUGQ = 2`, PWGTP-weighted, both sexes, via the Census API tabulate endpoint. **ACS has no parental birthplace, so every US-born row pools the second and third-plus generations**; the same proxy rate is therefore applied to `mexican_second_gen` and `mexican_third_plus_selfid`, and `all_second_gen` has no proxy at all and is given the all-US-born rate, which is why its institutional row should not be read as a second-generation measurement.

Institutional share of population, 2023, percent:

| | 18–39 | 40–64 | 65+ | 25–64 |
|---|---|---|---|---|
| US-born non-Hispanic white | 0.689 | 0.792 | 2.536 | 0.814 |
| US-born Mexican-origin (self-ID) | 1.079 | 1.343 | 1.606 | 1.411 |
| … generic-Hispanic-adjusted | 1.328 | 1.628 | 1.951 | 1.712 |
| Foreign-born Mexican | 0.649 | 0.392 | 0.968 | 0.481 |
| All US-born | 1.183 | 1.184 | 2.602 | 1.291 |

Priced at $57,911 per person-year under 65 ($63.6bn state corrections spending 2023 ÷ 1,098,228 state prisoners) and $53,900 per resident-year at 65+ (Medicaid's 44% of $147bn institutional long-term care 2023 ÷ 1.2 million nursing facility residents), the whole adult (18+) institutional cost expressed per adult 25–64 of the group:

| Arm | 3rd+ NH white | Mexican 2nd gen | Mexico-born | Mexican 2nd gen diff |
|---|---|---|---|---|
| Base | 1,105 | 1,057 | 386 | **+48** |
| Generic-Hispanic coding adjustment | 1,105 | 1,293 | 386 | −188 |
| Prison $45k | 993 | 848 | 320 | +145 |
| Prison $70k | 1,210 | 1,253 | 448 | −44 |
| Nursing charged only to the 62% Medicaid-primary share | 876 | 1,012 | 353 | −137 |
| Both adjustments together | 876 | 1,238 | 353 | −363 |

The white group's institutional bill is 55% nursing homes ($604 of $1,105 per adult) and the Mexican-origin group's is 11% ($118 of $1,057), which is why the item's sign turns entirely on how the 65+ leg is priced. Charging every 65+ resident the Medicaid per-resident cost assumes Medicaid pays for all of them; KFF puts Medicaid as primary payer for "over 60%", and applying 62% uniformly flips the item from +48 to −137. That uniform share is itself wrong in a direction that favours whites, since private-pay residents are richer on average, but the data to split it by origin are not here. **No standard errors are available for any of this**: the Census tabulate endpoint returns point estimates, with no replicate weights.

**5. Other public transfers — negligible.** State workers' compensation (`WC_TYPE = 1`, 110 unweighted recipients) plus disability income from the three unambiguously public non-employment programmes in `DIS_SC1/2` (code 6 railroad retirement disability, 8 black-lung miners' disability, 9 state temporary sickness; 31 unweighted recipients). The Mexican-second-generation difference is $0. The Mexican third-plus difference is +59 with a standard error of 48, i.e. noise from a handful of records.

**Also found in the dictionary, and what was done with each.**

| Field | Decision |
|---|---|
| `SPM_CAPHOUSESUB` capped housing subsidy | Reported as a memo row ($41 white, $70 Mexican 2nd gen, difference +29), **not** in the running balance. It is a capped *resource value* to the household, not the programme's cost to government, and the base generator deliberately holds it outside the fiscal ledger. |
| `DIS_SC` 3 and 5 (federal, state/local government employee disability) | Excluded. Deferred compensation of public employment, not a transfer programme. |
| `CHCARE_YN`, `SPM_CHILDCAREXPNS` | Excluded. "Paid child care was needed" and a household expense. **There is no child-care subsidy field in CPS ASEC 2025.** |
| `CHSP_VAL`, `CSP_VAL` child support paid/received | Excluded. Private inter-household transfers; child-support *enforcement* spending is not in the file. |
| `WC_TYPE` 2, 3, 4 (employer, own insurance, other) | Excluded. Private workers' compensation. |
| `PHIP_VAL`, `HIPAID`, `PMED_VAL` | Excluded. Out-of-pocket premiums and medical spending, not government outlays. |
| `SUR_SC` 2/4 (federal, state/local survivor pensions) | Excluded. Public-employee survivor pensions, deferred compensation again. |

## Sources

| Item | Source |
|---|---|
| CPS ASEC 2025 public-use microdata (income year 2024) | https://www2.census.gov/programs-surveys/cps/datasets/2025/march/asecpub25csv.zip — sha256 `318845a2b5e0034eb2973898de1738f4df0025727de38499e7669cb9c0deef0b`, the peer lane's cached copy |
| CPS ASEC 2025 data dictionary (`ED_VAL`, `OED_TYP1-3`, `A_ENRLW`, `A_HSCOL`, `A_FTPT`, `MRK/MRKS/MRKUN`, `COV`, `NOCOV_CYR`, `WC_TYPE`, `DIS_SC1/2`) | https://www2.census.gov/programs-surveys/cps/datasets/2025/march/asec2025_ddl_pub_full.pdf |
| Education appropriations $11,683 per FTE, FY2024 | SHEEO, *State Higher Education Finance FY2024*: "In 2024, education appropriations per FTE increased 0.8% beyond inflation to $11,683." https://shef.sheeo.org/wp-content/uploads/2025/05/SHEEO_SHEF_FY24_Report.pdf |
| Public undergraduate share 0.7726, fall 2023 (public 12,227,529 of 15,825,762) | NCES, *Digest of Education Statistics 2024*, Table 303.70. https://nces.ed.gov/programs/digest/d24/tables/dt24_303.70.asp |
| Average APTC $527.64/month, full plan year 2024, 19,531,827 APTC enrollees of 20,968,847 effectuated | CMS, *Effectuated Enrollment: Early 2025 Snapshot and Full Year 2024 Average*, Table 4. https://www.cms.gov/files/document/effectuated-enrollment-early-snapshot-2025-and-full-year-2024-average.pdf |
| Uncompensated hospital care $42.67bn, 2020 | AHA, *Uncompensated Hospital Care Cost Fact Sheet* (2020 update, the latest edition published). https://www.aha.org/system/files/media/file/2020/01/2020-Uncompensated-Care-Fact-Sheet.pdf |
| 28.0 million uninsured (8.6%), 2020 | U.S. Census Bureau, P60-274, *Health Insurance Coverage in the United States: 2020*. https://www.census.gov/content/dam/Census/library/publications/2021/demo/p60-274.pdf |
| $63.6bn state corrections spending 2023; median $60,989 per prisoner | USAFacts, *How much do states spend on housing prisoners?*, from the Census Annual Survey of State and Local Government Finances and BJS. https://usafacts.org/articles/how-much-do-states-spend-on-prisons/ |
| 1,254,200 prisoners at yearend 2023, of which 155,972 federal | BJS, *Prisoners in 2023 – Statistical Tables*. https://bjs.ojp.gov/document/p23st.pdf |
| Medicaid paid 44% of $147bn institutional long-term care 2023; 1.2 million nursing facility residents; "over 60%" Medicaid-primary | KFF, *5 Key Facts About Nursing Facilities and Medicaid*. https://www.kff.org/medicaid/5-key-facts-about-nursing-facilities-and-medicaid/ |
| Institutional group quarters by nativity, Hispanic origin, race and age, 2023 | ACS 1-year PUMS `TYPEHUGQ = 2` via the Census Data API tabulate endpoint. https://api.census.gov/data/2023/acs/acs1/pums |

## Assumptions, stated

1. **Every item is a scenario priced from a published aggregate, except educational assistance.** Only `ED_VAL` is a dollar amount reported by the respondent. Enrollment, subsidised-marketplace status and uninsurance are measured; their prices are national averages transported to every person regardless of state, age or plan.
2. **Uncompensated care is not a government outlay** and partly double counts the peer ledger's MEPS public-paid health transport through disproportionate-share recovery. Stated above; it is the largest CPS-side item, so this matters most.
3. **Higher education is charged only to enrolled 18–24-year-olds.** Graduate students and enrolled adults 25+ also consume state appropriations and are not charged, so every group's higher-education line is too low. The direction of the *difference* is not obviously affected.
4. **`A_ENRLW` is March-interview-week enrollment**, not enrollment during the 2024 academic year, and its universe is ages 16–54. A student enrolled in autumn 2024 but not in March 2025 is missed.
5. **Institutional care pools generations.** The ACS proxy cannot separate second from third-plus generation, and the CPS ledger groups cannot be reproduced in ACS. `all_second_gen`'s institutional row is the all-US-born rate and is not a measurement of that group.
6. **`TYPEHUGQ = 2` is all institutional group quarters**, not prisons: correctional, nursing, psychiatric and juvenile facilities together. Pricing everyone under 65 at the state-prison cost overstates the jail-held share (local jails run cheaper) and understates the psychiatric share (state hospitals run far dearer). ICE detention counts as correctional group quarters and inflates the foreign-born rate.
7. **The 65+ institutional cost is attributed per capita to the group's 25–64 adults**, as the brief directs. The numerator is the group's whole adult (18+) institutional population; the denominator is its 25–64 population. It is a cost-of-the-group-per-working-age-adult, not a cost incurred by those adults.
8. **Generic-Hispanic prison coding.** Correctional records frequently carry "Hispanic" with no origin. The adjusted arm reallocates the excess institutionalisation of `HISP = 24` above the all-native rate to named origins by population share, the same construction as the peer incarceration lane. It is a bound, not a measurement, and ethnic attrition in self-identification runs the other way.
9. **Sampling error covers CPS only.** SDR standard errors are the CPS 160-replicate estimator. They exclude error in every applied rate, in transporting national averages to individuals, in CPS income and coverage under-reporting, and all of the ACS-side estimates, for which the tabulate endpoint returns no variance at all.
10. **Uncompensated care and prison prices are 2020 and 2023 nominal**, against a 2024 income year. The uplift arm is an approximation, flagged `[INFERENCE]`.

## Still outside the ledger

- **Pure public goods**: defense, debt service, general government administration, courts, police, diplomacy. Still the single largest discretionary choice in any fiscal accounting and still not made.
- **Corporate income tax** and any incidence of it assigned to workers or shareholders.
- **Accrued rather than received Social Security and Medicare.** The ledger credits benefits received this year. A younger, lower-earning group accrues less future benefit, and the annual snapshot never shows it.
- **Medicare Part D and Part B premium subsidies** beyond what the MEPS public-paid transport captures.
- **Police, courts, probation, parole and victimisation costs.** Only custodial institutional care is priced here, and only at the state-prison average.
- **Child-support enforcement, child-care subsidies (CCDF), Head Start, job training, LIHEAP administration.** No field exists for any of these in CPS ASEC 2025.
- **Higher-education subsidy for students 25+ and graduate students**, and federal student-loan interest subsidies and discharges.
- **State and local government employee pension underfunding**, deliberately excluded as deferred compensation but real fiscal cost.
- **Unauthorised status.** No status is observed anywhere in the file; noncitizens include lawful permanent residents.
- **Tax compliance.** Census models liability, not payment.
- **Indirect and general-equilibrium effects**: wage and price effects on natives, capital deepening, production complementarity. Not in any accounting ledger.

## Verification commands, run and pasted

```
$ cd /Users/alien/Projects/immigration-research && uv run python3 infra/immigration-fiscal/ledger_residual_micro_2026_09_16/residual_micro.py
EXIT=0
...
-- STEP A gate: peer-lane extended balance --
Mexican 2nd gen minus 3rd+ NH white, EXTENDED balance, equal_all_members,
person weights, adults 25-64: -8,286 (se 443)
Published in gen_ledger_extension_2026_09_16/RESULT.md and memo §12: -8,286 (se 443)
Deviation from the published -8,286: -0.23
[Step A gate] PASS (within $50 of the published -8,286)

Wrote .../residual_micro_by_generation.csv
Wrote .../residual_micro_result.txt
Wrote .../acs_institutional_by_age_band.csv
```

```
$ rg -n "8,286|8286" infra/immigration-fiscal/ledger_residual_micro_2026_09_16/residual_micro_result.txt
31:EXTENDED BALANCE (peer lane)                                                 —      -1,719 (124)        -327 (488)      -8,286 (443)      -6,279 (546)     -11,522 (402)
48:Extended balance (baseline for this lane)                       -1,719 (124)        -327 (488)      -8,286 (443)      -6,279 (546)     -11,522 (402)
194:person weights, adults 25-64: -8,286 (se 443)
195:Published in gen_ledger_extension_2026_09_16/RESULT.md and memo §12: -8,286 (se 443)
196:Deviation from the published -8,286: -0.23
RG_EXIT=0
```

Both PASS.

## Files in this lane

| File | What |
|---|---|
| `residual_micro.py` | The run. Calls `extend_ledger.build()`, adds the five items, pulls ACS, writes all three outputs. No network for CPS (peer lane cache); ACS JSON tabulations are cached after the first pull. |
| `residual_micro_by_generation.csv` | Long format: allocation × group × metric, estimate, SDR se, difference from third-plus NH white and its se, plus a `source` column separating CPS from ACS rows. 288 rows. |
| `residual_micro_result.txt` | The printed tables, both allocations, the §12 layout, the ACS institutional rates, the applied rates, the source list and the Step A gate. |
| `acs_institutional_by_age_band.csv` | ACS 2023 institutional counts, populations and rates by proxy group and age band, raw and generic-Hispanic-adjusted. |
| `acs_{h,r}_{18_39,40_64,65_plus,25_64}.json` | Raw Census API tabulate responses, as returned. |
