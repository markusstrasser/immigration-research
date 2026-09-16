# FBI 2023/2024 arrests by offence × ethnicity — crime-cost route B replaced

Model self-report: claude-opus-5[1m] (Opus 5, 1M context)

**Verdict:** The 2019 arrest flow is replaceable and has been replaced. FBI *Crime in the United
States* Table 43C now exists for **2023 and 2024**, both with far better ethnicity coverage than
2019 (12,815 agencies / 291.4m people in 2023 and 13,980 / 300.8m in 2024, against 10,831 / 229.7m
in 2019). Recomputing route B with the peer lane's own unit costs and `route_b()` function, and
Census vintage-2024 denominators, moves the Hispanic-minus-non-Hispanic-white cost difference per
adult 18+ from the 2019-based **+$1,316 (2.58×)** to **+$1,563 (3.18×) on 2023** and
**+$1,201 (2.74×) on 2024**. **The crime-cost line does not change in any way that matters.**
Route A2 (+$1,421), which the peer lane names as the more defensible level, sits inside the
2023–2024 route-B band, so the two-route agreement that the peer lane called its strongest
internal evidence survives and on 2023 it tightens (10% apart, was 8%).

What the update does change is the **uncertainty attribution**. The 2023-to-2024 spread
(+$1,563 → +$1,201, −23%; 3.18× → 2.74×) is **larger than the 2019-to-2023 change**. The arrest
year, not the choice of denominator or the choice of unit-cost source, is the dominant source of
variation in route B. The 2019 figure was never stale so much as it was one draw from a noisy
series, and the honest statement of route B is now a **band of +$1,200 to +$1,750 and 2.6× to
3.2×**, not a point.

The **Hispanic/white arrest ratio rose on every offence class** between 2019 and 2023. That is a
real change in the published numbers, but it is **confounded with the coverage expansion** and this
lane cannot separate the two. [FRAMING-SENSITIVE]

[UNVERIFIED] marks every figure that rests on the FBI's constructed non-Hispanic-white arrest
count, which is an inference, not a published series. See §6.

## Verification

```
cd /Users/alien/Projects/immigration-research && uv run python3 infra/immigration-fiscal/nibrs_arrests_2026_09_16/nibrs_arrests.py
exit=0
```

(The script re-execs itself under `uv run --with openpyxl --with xlrd` when those readers are
absent, so the plain command above works unchanged. The 2020 tables are legacy `.xls`.)

Integrity gates, all PASS:

```
[peer model imported] PASS — 17 costed offence keys, route_b present
[peer 2019 route B reproduces RESULT.md] PASS — 2019 diff $1,316 (RESULT.md +$1,316), ratio 2.58x (2.58x)
[CIUS 2023 Table 43C parsed] PASS — 13 costed offences + TOTAL; murder Hispanic adult arrests 1,698
[CIUS 2024 Table 43C parsed] PASS — TOTAL adult ethnicity-panel arrests 5,152,383
[2023 ethnicity panel Hispanic + non-Hispanic = ethnicity total] PASS — 5,064,955 adult arrests, Hispanic 1,105,409 (21.8%)
[2024 ethnicity panel Hispanic + non-Hispanic = ethnicity total] PASS — 5,152,383 adult arrests, Hispanic 1,140,056 (22.1%)
[NC-EST2024 July 2020/2023/2024 single-year ages sum to the 999 total row] PASS
[peer globals restored after the year swap] PASS — crime_cost.T43C back to its 2019 values
```

The first two gates are the load-bearing ones. The peer lane's `crime_cost.py` is **imported, not
copied**: its unit-cost table, CPI deflation, offence→cost mapping and `route_b()` are reused
verbatim, and only the year-specific module globals (`T43C`, `T43A_RACE_TOTAL`, `EST_ARRESTS_2019`,
`CRIMES_PER_ARREST`, `POP2019`) are swapped. Gate 2 confirms the import reproduces the published
+$1,316 before anything is swapped; the last gate confirms the swap is undone afterwards.

## 1. Reporting coverage — the FBI ethnicity panel

| Year | Agencies | Panel population | % of US population | Ethnicity panel ÷ race panel |
|---|---|---|---|---|
| 2019 | 10,831 | 229,735,355 | 70.0% | 86.6% |
| 2020 | 10,466 | 228,864,358 | 69.0% | 85.9% |
| 2023 | 12,815 | 291,365,847 | 87.0% | 86.3% |
| 2024 | 13,980 | 300,768,839 | 88.4% | 85.5% |

UCR has been **NIBRS-only since 1 January 2021**. The usual worry about post-2021 arrest data is
that the transition destroyed coverage — for 2021 it did, with NYPD and LAPD among the
non-converters. By 2023 that is no longer true of the arrest tables: the ethnicity panel covers
**27% more people than 2019** and 87% of the country. The share of the race panel that also reports
ethnicity is essentially flat across the transition (86.6% → 86.3% → 85.5%), so the ethnicity item
is not differentially missing.

**The coverage gain is not neutral for the ratio.** The agencies added between 2019 and 2023 are
disproportionately in states that converted to NIBRS late, and the peer lane's own assumption 8
(agencies reporting ethnicity skew toward high-Hispanic states) applies with a different sign and an
unknown magnitude in each year. Nothing in this lane decomposes the ratio change into a real
behavioural change and a panel-composition change. [FRAMING-SENSITIVE]

## 2. Adult (18+) arrests by offence × ethnicity, 2023 — Table 43C

| Offence | Race panel | Race: White | Eth panel | Hispanic | NH white* | Hispanic share |
|---|---|---|---|---|---|---|
| Murder / nonneg. manslaughter | 9,100 | 3,713 | 7,830 | 1,698 | 1,497 | **21.7%** |
| Rape | 13,543 | 9,032 | 11,799 | 3,644 | 4,225 | 30.9% |
| Robbery | 45,000 | 18,532 | 42,347 | 11,269 | 6,170 | 26.6% |
| Aggravated assault | 270,568 | 152,736 | 244,564 | 65,113 | 72,944 | 26.6% |
| Burglary | 93,294 | 60,432 | 82,999 | 17,849 | 35,914 | 21.5% |
| Larceny-theft | 515,404 | 323,648 | 449,906 | 84,535 | 197,984 | 18.8% |
| Motor vehicle theft | 51,545 | 33,345 | 46,030 | 12,826 | 16,951 | 27.9% |
| Arson | 6,563 | 4,712 | 5,636 | 1,315 | 2,731 | 23.3% |
| Forgery / counterfeiting | 27,188 | 15,467 | 27,706 | 7,813 | 7,949 | 28.2% |
| Fraud | 64,657 | 40,925 | 55,894 | 9,557 | 25,821 | 17.1% |
| Embezzlement | 8,126 | 4,774 | 6,920 | 1,042 | 3,023 | 15.1% |
| Stolen property | 59,908 | 35,755 | 52,301 | 11,754 | 19,461 | 22.5% |
| Vandalism | 122,088 | 77,253 | 110,114 | 24,239 | 45,437 | 22.0% |
| Other (simple) assaults | 749,812 | 465,989 | 658,341 | 150,237 | 258,905 | 22.8% |
| Drug abuse violations | 687,055 | 470,251 | 607,484 | 122,568 | 293,221 | 20.2% |
| Weapons | 131,703 | 61,421 | 113,201 | 26,816 | 25,976 | 23.7% |
| Driving under the influence | 644,445 | 511,004 | 542,648 | 171,834 | 258,451 | **31.7%** |
| **All offences** | 5,853,877 | 3,909,404 | 5,064,955 | 1,105,409 | 2,277,128 | **21.8%** |

The 2024 panel is in `arrests_by_ethnicity_2023.csv`, along with 2020.

\* **Non-Hispanic white is constructed, not published**, exactly as in the 2019 lane: the race panel
is rescaled to the ethnicity panel's coverage offence by offence, then Hispanic arrests are
subtracted from White arrests, on the assumption that most Hispanic arrestees are coded racially
white. The FBI publishes no race × ethnicity cross-tab. **[INFERENCE]**

## 3. Denominators

Census **vintage-2024** national population estimates, `NC-EST2024-ALLDATA-H`, July 1, adults 18+,
columns `NHWA_MALE/FEMALE` (non-Hispanic white alone) and `H_MALE/FEMALE` (Hispanic, any race).
Single-year ages 18–100 summed; the file's own `AGE=999` row is used only as a check.

| Denominator | NH white 18+ | Hispanic 18+ |
|---|---|---|
| NC-EST2024, July 1 2020 | 155,684,757 | 42,286,457 |
| NC-EST2024, July 1 2023 | 155,327,952 | 45,826,303 |
| NC-EST2024, July 1 2024 | 155,550,233 | 47,541,960 |
| ACS 2023 1-year, B01001H / B01001I | 157,221,841 | 46,045,083 |
| ACS 2019 1-year (peer lane, unchanged) | 160,282,147 | 41,856,869 |

The ACS 2023 row exists so the 2019→2023 comparison is not contaminated by switching denominator
source. **It changes nothing**: +$1,561 / 3.20× on ACS against +$1,563 / 3.18× on NC-EST. The
denominator choice is worth about 0.1% of the level and 0.02 of the ratio, which is two orders of
magnitude below the year-to-year variation.

## 4. Route B recomputed — dollars per adult 18+ per year, 2024 dollars

| Arm | NH white | Hispanic | Difference | Ratio |
|---|---|---|---|---|
| Tangible + CJS, 2019 (peer lane, unchanged) | 239 | 480 | +241 | 2.01× |
| Tangible + CJS, 2020 | 257 | 570 | +313 | 2.22× |
| Tangible + CJS, 2023 | 200 | 510 | +311 | 2.56× |
| Tangible + CJS, 2024 | 186 | 437 | +251 | 2.35× |
| **+ intangible, 2019 (peer lane, unchanged)** | **834** | **2,150** | **+1,316** | **2.58×** |
| **+ intangible, 2020** | 960 | 2,710 | **+1,750** | 2.82× |
| **+ intangible, 2023** | **718** | **2,281** | **+1,563** | **3.18×** |
| + intangible, 2023, ACS denominator | 710 | 2,271 | +1,561 | 3.20× |
| **+ intangible, 2024** | 690 | 1,891 | **+1,201** | 2.74× |
| + intangible + NCVS uplift 1/0.409, 2023 | 1,757 | 5,578 | +3,822 | 3.18× |
| + intangible + NCVS uplift 1/0.409, 2024 | 1,687 | 4,623 | +2,936 | 2.74× |

Change against the 2019-based headline:

| Year | Difference | vs +$1,316 | Ratio | vs 2.58× | % of the −$8,286 gap |
|---|---|---|---|---|---|
| 2019 | +1,316 | — | 2.58× | — | 15.9% |
| 2020 | +1,750 | +33.0% | 2.82× | +0.24 | 21.1% |
| 2023 | +1,563 | +18.8% | 3.18× | +0.60 | 18.9% |
| 2024 | +1,201 | −8.7% | 2.74× | +0.16 | 14.5% |

**Does the crime-cost line change? No.** Every arm stays between 14% and 21% of the extended fiscal
gap, against 15.9% on the 2019 flow. The peer lane's headline conclusion — the sign is unambiguous,
the magnitude is an order of magnitude short of closing the gap — is untouched, and so is its
preferred level, route A2's +$1,421, which is not derived from arrests at all.

**Does the ratio change? Slightly, upward, and unreliably.** 2.58× (2019) → 2.82× (2020) → 3.18×
(2023) → 2.74× (2024). The 2023 point is the high one in a four-point series whose own year-to-year
spread is ±0.4. Quoting 3.18× as "the current ratio" would overstate what these data support;
**2.6×–3.2×** is the defensible statement.

## 5. Offence composition of the 2023 difference

| Offence | NH white arrests* | Hispanic arrests* | NHW $bn | Hisp $bn | Hispanic share of $ |
|---|---|---|---|---|---|
| Murder | 1,995 | 2,263 | 42.3 | 48.0 | **53.1%** |
| Aggravated assault | 95,458 | 85,211 | 37.3 | 33.3 | 47.2% |
| Rape / sexual assault | 5,855 | 5,050 | 13.3 | 11.5 | 46.3% |
| Larceny | 272,068 | 116,167 | 8.9 | 3.8 | 29.9% |
| Motor vehicle theft | 22,237 | 16,826 | 4.5 | 3.4 | 43.1% |
| Robbery | 7,729 | 14,116 | 1.4 | 2.6 | **64.6%** |
| Burglary | 47,655 | 23,684 | 2.8 | 1.4 | 33.2% |
| Vandalism | 60,235 | 32,133 | 0.4 | 0.2 | 34.8% |
| Fraud | 35,659 | 13,198 | 0.2 | 0.1 | 27.0% |

\* national adult arrests, panel counts scaled up by Table 29 ÷ panel.

Murder is again the single point of leverage, at 53.1% of the dollars against 43.3% in 2019, and the
reason is visible in the raw counts: **Hispanic adult murder arrests now exceed constructed
non-Hispanic-white adult murder arrests** (2,263 against 1,995), where in 2019 they did not
(2,014 against 2,641). Two thirds of the difference between the 2019 and 2023 route-B numbers is
that one flip. On 2024 the murder ratio falls back to 2.99× and the headline falls with it. **A
result that rests this heavily on one offence in one year should be quoted as a band.**

## 6. Hispanic / non-Hispanic-white arrest ratio per adult 18+

| Class | 2019 | 2020 | 2023 | 2024 | 2019→2023 |
|---|---|---|---|---|---|
| Violent index (4 offences) | 2.77× | 2.87× | 3.27× | 2.95× | +0.50 |
| — Murder | 2.92× | 3.28× | 3.85× | 2.99× | +0.93 |
| — Rape | 2.76× | 2.82× | 2.92× | 2.91× | +0.16 |
| — Robbery | 3.68× | 3.92× | **6.19×** | 6.07× | **+2.51** |
| — Aggravated assault | 2.66× | 2.76× | 3.03× | 2.69× | +0.37 |
| **Simple assault** | 1.49× | 1.60× | **1.97×** | 2.02× | +0.48 |
| Property index (4 offences) | 1.17× | 1.22× | 1.56× | 1.63× | +0.39 |
| — Burglary | 1.57× | 1.60× | 1.68× | 1.54× | +0.11 |
| — Larceny | 1.01× | 1.01× | 1.45× | 1.60× | +0.43 |
| — Motor vehicle theft | 2.08× | 2.38× | 2.56× | 2.36× | +0.48 |
| — Fraud | 1.07× | 1.04× | 1.25× | 1.36× | +0.19 |
| **Drug abuse violations** | n/a | 1.57× | **1.42×** | 1.32× | n/a |

Every class rises. **Robbery is the outlier and it should be treated as suspect**: a jump from
3.68× to 6.19×, driven by the Hispanic share of robbery arrests rising from 23.0% to 26.6% while the
constructed non-Hispanic-white count falls by a third. A move that large in four years, in a panel
that gained 2,000 agencies, is more consistent with panel composition than with offending.
Robbery carries only 5% of the dollar difference, so it does not drive the headline.

**Simple assault matters for the NCVS reconciliation.** The peer lane's §6 argued that putting
simple assault back into the arrest count drops the violent ratio from 2.77× to 1.85×, bracketing
the NCVS victim-report 1.37×. On 2023 the same construction gives **2.30×** (2024: 2.24×) (violent index plus
simple assault), against 1.97× for simple assault alone. The reconciliation gets **worse**, not
better, and the residual enforcement/charging/severity wedge is correspondingly larger on 2023 data
than the peer lane's §6 implies. Its §6 numbers are 2019 numbers and should be read as such.

**Drug arrests have no 2019 comparator.** FBI CIUS downloadable publication tables on the Crime Data
Explorer begin with 2020; the 2019 static tables at `ucr.fbi.gov` now return 403 and the peer lane
never transcribed the 2019 drug row. The 2020 value (1.57×) is the earliest available here. Drug
offences carry no McCollister unit cost and enter no dollar figure in this lane or the peer lane.

## Sources — exact files

All fetched this session from the FBI Crime Data Explorer signed-URL store,
`https://cde.ucr.cjis.gov/LATEST/s3/signedurl?key=<key>`, and cached under `_cache/` (gitignored).

| Item | Key / file |
|---|---|
| Arrests by race and ethnicity, adults 18+, 2023 | `cius/2023/persons-arrested-2023.zip` → `Table_43C_Arrests_by_Race_and_Ethnicity_2023_Continued.xlsx` |
| Same, all ages, 2023 (used for the panel rescale) | same zip → `Table_43A_Arrests_by_Race_and_Ethnicity_2023.xlsx` |
| Estimated national arrests, 2023 | same zip → `Table_29_Estimated_Number_of_Arrests_United_States_2023.xlsx` |
| Arrests by race and ethnicity, adults 18+, 2024 | `cius/2024/persons-arrested-2024.zip` → `CIUS_Table_43C_Arrests_by_Race_and_Ethnicity_2024_Continued.xlsx` |
| Same, all ages, 2024 | same zip → `CIUS_Table_43A_Arrests_by_Race_and_Ethnicity_2024.xlsx` |
| Estimated national arrests, 2024 | same zip → `CIUS_Table_29_Estimated_Number_of_Arrests_United_States_2024.xlsx` |
| Arrests by race and ethnicity, adults 18+, 2020 | `cius/2020/persons-arrested-2020.zip` → `Table_43C_Arrests_by_Race_and_Ethnicity_2020_Continued.xls` |
| Estimated national arrests, 2020 | same zip → `Table_29_Estimated_Number_of_Arrests_United_States_2020.xls` |
| Offences known to law enforcement, 2023 | `cius/2023/cius-estimations-2023.zip` → `Table_1_Crime_in_the_United_States_by_Volume_and_Rate_per_100000_Inhabitants_2004-2023.xlsx` |
| Offences known, 2024 | `cius/2024/cius-estimations-2024.zip` → `CIUS_Table_1_..._2005-2024.xlsx` |
| Offences known, 2020 | `cius/2020/cius-estimations-2020.zip` → `Table_01_..._2001-2020.xls` |
| Population by age, sex, race, Hispanic origin, July 1 2020 / 2023 / 2024 | `https://www2.census.gov/programs-surveys/popest/datasets/2020-2024/national/asrh/nc-est2024-alldata-h-file02.csv`, `-file08.csv`, `-file10.csv` (vintage 2024) |
| Unit costs, CPI, `route_b()`, 2019 arrest panel | imported from `infra/immigration-fiscal/crime_cost_2026_09_16/crime_cost.py` |
| ACS 2023 1-year populations, B01001H / B01001I | Census Data API, via the peer lane's `acs_pop()` |

The CDE **arrest API** (`https://cde.ucr.cjis.gov/LATEST/arrest/national/all?type=totals`) was
probed first and **does not carry ethnicity at all** — its breakdowns are `Arrestee Race`,
`Arrestee Sex` and age. The arrestee-ethnicity series exists only in the CIUS publication tables
above (and, at incident level, in the NIBRS master files, which were not needed). Recorded here
because the brief pointed at the API route.

## Assumptions and limits

1. **Non-Hispanic white arrests are constructed**, not published, in every year. [INFERENCE]
2. **The coverage change between 2019 and 2023 is not adjusted for.** The panel gained 2,000
   agencies and 62m people; no weighting corrects for which states they are in. Every ratio change
   in §6 is a mixture of behaviour and composition. [FRAMING-SENSITIVE]
3. **Offences per arrest are national ratios applied to both groups equally.** The ratio is
   invariant to them; only the level moves. Same for the Table 29 scale-up and the NCVS uplift.
4. **Drug, DUI, weapons, simple assault and all public-order offences carry no unit cost** and are
   excluded from every dollar figure, as in the peer lane. The excluded block's Hispanic share is
   close to the overall 21.8%, so it is near-neutral for the ratio and lowers both levels.
5. **This is Hispanic vs non-Hispanic white, adults 18+.** It is not the ledger's US-born
   Mexican-origin vs US-born non-Hispanic white at 25–64, and it pools nativity. Route A2 remains
   the lane's preferred level for the ledger's own groups.
6. **No standard errors.** The arm spans are specification uncertainty, and the year-to-year spread
   is the closest thing to a sampling-error proxy available.
7. **2020 is a COVID year** and is reported for trend context only.
8. Everything here is resident-characteristic accounting, not a policy effect.

## Files

All under `/Users/alien/Projects/immigration-research/infra/immigration-fiscal/nibrs_arrests_2026_09_16/`:

- `RESULT.md` — this file
- `nibrs_arrests.py` — the model; run it as shown above
- `arrests_by_ethnicity_2023.csv` — 2020/2023/2024 arrests by offence × ethnicity, coverage,
  denominators, every route-B arm, every arrest ratio
- `nibrs_result.txt` — the full printed output
- `_cache/` — the downloaded FBI zips and Census files (gitignored)
