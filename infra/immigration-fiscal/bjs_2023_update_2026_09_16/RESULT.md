[DATA] [INFERENCE] [SOURCE: https://bjs.ojp.gov/document/p23st.zip] [SOURCE: https://bjs.ojp.gov/document/ji24st.zip] [SOURCE: https://www2.census.gov/programs-surveys/popest/datasets/2020-2024/national/asrh/]

**Model self-report:** Opus 5 (1M context) — claude-opus-5[1m]

**Verdict:** Series extended to the newest year BJS publishes, which is **2022, not 2023** — the offence-by-race table lags one year because its source is the National Corrections Reporting Program. Ladder-70's direction claim **holds through the newest year** on the four top-level offence classes. **Zero restatement** was found: Prisoners in 2023 reprints 2020, 2021 and 2022 race and Hispanic-origin counts identical to Prisoners in 2022, to the last digit. One real defect found in the predecessor script: its 2021 white denominator is the 2020 decennial count, not a population estimate.

Artifacts, all under `/Users/alien/Projects/immigration-research/infra/immigration-fiscal/bjs_2023_update_2026_09_16/`:

- `bjs_2023.py` — script, exits 0
- `bjs_offense_by_ethnicity_2023.csv` — 96 rows, wide schema extending the predecessor CSV with `n2022`, `per100k_2022`, three change legs, `share2022_pct`, and a new `pop_basis` column
- `bjs_2023_result.txt` — full console output

---

## 1. What year the newest offence table reports

`p23stt16.csv` is **Table 16. Number of sentenced prisoners under the jurisdiction of state correctional authorities, by sex, race or Hispanic origin, and most serious offense, December 31, 2022** (Prisoners in 2023 – Statistical Tables, NCJ 310197, date of version 9/30/25). Table 17 is the percent version of the same table. Table 19/20 are the federal analogue at September 30, 2023.

**Estimation basis**, stated verbatim in the table's own source line: *"Bureau of Justice Statistics, National Corrections Reporting Program, 2022; National Prisoner Statistics, 2022; and Survey of Prison Inmates, 2016."* The 2021 table in Prisoners in 2022 carries the identical construction with the reference year advanced by one (NCRP 2021 + NPS 2021 + SPI 2016). So 2021 and 2022 are on the **same** basis — race and Hispanic origin imputed from the 2016 Survey of Prison Inmates, applied to that year's administrative counts. This is the basis the 2009r restatement put the series on, so 2009r → 2021 → 2022 is one consistent chain.

There is no 2023 offence-by-race table in any BJS publication. The imprisonment-rate table for 2023 does exist (Table 13) and is carried below.

## 2. Restatement check — the trap did not recur

Sentenced prisoners by race and Hispanic origin, state plus federal, as printed in each edition:

| Year | Series | Prisoners in 2022 (Table 3) | Prisoners in 2023 (Table 3) | Delta |
|---|---|---|---|---|
| 2020 | White / Black / Hispanic | 360,100 / 390,700 / 276,100 | 360,100 / 390,700 / 276,100 | 0 / 0 / 0 |
| 2021 | White / Black / Hispanic | 356,000 / 378,000 / 273,800 | 356,000 / 378,000 / 273,800 | 0 / 0 / 0 |
| 2022 | White / Black / Hispanic | 367,800 / 384,600 / 273,900 | 367,800 / 384,600 / 273,900 | 0 / 0 / 0 |
| 2021 | Total / federal / state | 1,165,736 / 144,448 / 1,021,288 | identical | 0 |
| 2022 | Total / federal / state | 1,185,648 / 146,108 / 1,039,540 | identical | 0 |

**Discrepancies found: 0 of 18 cells.** Prisoners in 2023 Table 3 still carries the boilerplate note *"Counts for 2022 and earlier may have been revised from previous reports due to revisions in the correctional population"*, but nothing moved.

For contrast, the 2009 restatement that the brief warned about, state sentenced prisoners by race:

| Edition | White | Hispanic |
|---|---|---|
| Prisoners in 2010, Appendix Table 16b | 532,000 | 212,100 |
| Prisoners in 2011, Appendix Table 8 | 467,290 | 287,568 |
| Delta | −64,710 (−12.2%) | +75,468 (+35.6%) |

That was a one-off change of the race and Hispanic-origin estimation *source*, not a routine annual revision. The practical consequence: 2021 and 2022 may be taken from either edition without a comparability penalty. I took 2022 from the 2023 report anyway, and verified the 2021 counts in the predecessor script against Prisoners in 2022 Table 17 cell by cell — they match exactly.

## 3. Defect found in the predecessor denominators

`acs_institutional_2026_09_16/bjs_offense_by_ethnicity.py` divides 2021 non-Hispanic white prisoners by **191.7 million**. That is the 2020 *decennial census* white-alone-not-Hispanic count. The July 1, 2021 population estimate is **196.6 million** (Vintage 2024). Its Hispanic figure, 62.6 million against an estimate of 63.0 million, is close but from a different vintage. The mismatch understates the white 2009 → 2021 decline by roughly 2.5 percentage points on every offence.

The new CSV carries both. `pop_basis=orig` reproduces the published numbers; `pop_basis=pep` puts every year on July 1 resident population estimates with one definition — non-Hispanic white alone (`NHWA_MALE + NHWA_FEMALE`) and Hispanic (`H_MALE + H_FEMALE`):

| Year | NH white alone | Hispanic | Source table |
|---|---|---|---|
| 2009-07-01 | 197,274,549 | 49,327,489 | Intercensal 2000–2010, `us-est00int-alldata.csv` |
| 2021-07-01 | 196,609,140 | 63,011,125 | Vintage 2024, `nc-est2024-alldata-r-file04.csv` |
| 2022-07-01 | 195,994,987 | 64,396,719 | Vintage 2024, `nc-est2024-alldata-r-file06.csv` |

## 4. Per-capita series, 2009r → 2021 → 2022, consistent denominators

Sentenced state prisoners per 100,000 residents of the group.

| Offence | White r09 | r21 | r22 | 09→22 | Hispanic r09 | r21 | r22 | 09→22 |
|---|---|---|---|---|---|---|---|---|
| Total | 236.9 | 163.6 | 170.0 | −28.2% | 583.0 | 356.0 | 348.0 | −40.3% |
| Violent | 117.3 | 89.7 | 91.9 | −21.7% | 324.0 | 254.1 | 246.8 | −23.8% |
| Property | 56.3 | 29.3 | 29.1 | −48.2% | 87.4 | 30.2 | 29.5 | −66.2% |
| Drug | 35.1 | 24.5 | 27.2 | −22.3% | 100.1 | 35.9 | 34.5 | −65.6% |
| Public order | 26.4 | 18.7 | 20.3 | −23.0% | 68.9 | 34.8 | 36.0 | −47.7% |

The 2021 → 2022 step is the story of the newest year: **white per-capita rose on four of five classes, Hispanic fell on four of five.** White total +3.9%, drug +11.1%, public order +8.5%, violent +2.4%, property −0.6%. Hispanic total −2.2%, violent −2.9%, property −2.2%, drug −3.9%, public order +3.7%. The white drug rise is the largest single move in the table and is concentrated in possession, 15,800 → 18,200.

## 5. Does ladder-70's direction hold through the newest year?

The claim as written in entry 70 and memo section 8 covers the total and the four top-level BJS classes.

| Denominator basis | Leg | Top-level classes | Including sub-offences |
|---|---|---|---|
| pep | 2009r → 2021 | **FAILS** (violent) | FAILS |
| pep | 2009r → 2022 | **HOLDS** | FAILS |
| pep | 2021 → 2022 | **HOLDS** | FAILS |
| orig | 2009r → 2021 | **HOLDS** | FAILS |

**Direction holds through 2022.** The single failure at 2021 on corrected denominators is violent alone, white −23.5% versus Hispanic −21.6%, a 1.9-point margin created entirely by the denominator fix in section 3. On the published denominators the same leg reads −20.5% versus −22.5% and holds, which is what the memo reports. Adding 2022 restores the direction on both bases. The honest statement is that the violent leg at 2021 sat inside denominator noise, and the newest year moves it clear of that.

The claim was never made at sub-offence level and does not hold there on any leg. Hispanic rape/sexual-assault per capita is flat across the whole period (67.9 → 67.9 → 67.9) while the white rate fell 15.8%; robbery and assault also fall faster for whites. Those three are the sub-offences to watch.

## 6. Imprisonment rate by race and age, 2023

Male, state plus federal, sentence over one year, per 100,000 residents of the group. 2010 from Prisoners in 2010 Appendix Table 15; 2022 from Prisoners in 2022 Table 13; 2023 from Prisoners in 2023 Table 13 (denominator: Census postcensal estimates for January 1, 2024).

| Age | White 2022 | White 2023 | Hispanic 2022 | Hispanic 2023 | Ratio 2010 | Ratio 2022 | Ratio 2023 |
|---|---|---|---|---|---|---|---|
| 18–19 | 30 | 30 | 85 | 84 | 3.78× | 2.83× | 2.80× |
| 20–24 | 229 | 229 | 663 | 672 | 2.99× | 2.90× | 2.93× |
| 25–29 | 514 | 496 | 1,462 | 1,431 | 2.76× | 2.84× | 2.89× |
| 30–34 | 732 | 729 | 1,774 | 1,789 | 2.65× | 2.42× | 2.45× |
| 35–39 | 813 | 818 | 1,747 | 1,758 | 2.50× | 2.15× | 2.15× |
| 40–44 | 776 | 799 | 1,634 | 1,677 | — | 2.11× | 2.10× |
| All ages | 337 | 341 | 794 | 800 | 2.74× | 2.36× | 2.35× |

2023 is a flat year. Both groups tick up at the all-ages level, white +1.2% and Hispanic +0.8%, and the overall ratio is essentially unchanged at 2.35×. The long-run 2010 → 2023 convergence, 2.74× → 2.35×, is intact but stopped advancing in the newest year. Underlying male sentenced counts: white 328,400 → 330,400, Hispanic 258,500 → 266,200.

## 7. Jail inmates held for U.S. Immigration and Customs Enforcement

BJS, Jail Inmates in 2024 (NCJ 311504, date of version 9/8/2026), **Table 14, "Persons held in local jails for federal, state, and tribal correctional authorities, 2014–2024"**, column "U.S. Immigration and Customs Enforcement". Counts are the last weekday in June.

| Year | Held for ICE | Year-on-year |
|---|---|---|
| 2019 | 17,300 | +16.1% |
| 2020 | 9,300 | −46.2% |
| 2021 | 7,400 | −20.4% |
| 2022 | 6,900 | −6.8% |
| 2023 | 7,000 | +1.4% |
| 2024 | 8,000 | +14.3% |

2019 and 2024 are Census of Jails complete enumerations; the intervening years are Annual Survey of Jails estimates with standard errors of 518 to 1,040 on this column. The 2019 → 2024 fall is 53.8%; BJS prints −51.2% for 2014 → 2024. The series has not recovered its pre-2020 level.

## 8. ICE-detention inflation of the ACS foreign-born institutional count

The ladder-65 caveat is that ACS institutional group quarters since 2010 include ICE detention, biasing the foreign-born row up.

| Quantity | Value |
|---|---|
| ACS 2023 1-year PUMS, men 18–39, foreign born, institutional GQ | 65,685 |
| ICE average daily detained population, FY2023 | 28,289 |
| Arithmetic upper bound, every detainee a foreign-born man 18–39 in ACS GQ | 43.1% |
| Plausible contribution at 87% male and 55–70% aged 18–39 | 13,500–17,200, or 21–26% |

[SOURCE: ICE Annual Report FY2023, NCJ n/a, https://www.ice.gov/doclib/eoy/iceAnnualReportFY2023.pdf — "an average of 28,289 noncitizens in ICE custody"; detention statistics landing page https://www.ice.gov/detain/detention-management]

[INFERENCE] The 87% male and 55–70% age assumptions are mine and are the load-bearing uncertainty in the 21–26% band. The 43.1% upper bound is arithmetic and requires no assumption.

Two things bound this from the other side. First, BJS counts only 7,000 jail inmates held for ICE in June 2023, 25% of ICE average daily population, so most detainees are in dedicated or contract detention facilities rather than the local-jail universe. Whether the Census Bureau enumerates those as institutional group quarters determines how much of the 21–26% actually lands in the ACS cell, and I did not verify that. Second, the direction of the bias is unambiguous: netting ICE out lowers the foreign-born institutional rate and *widens* the native-versus-foreign-born gap in the pro-immigrant direction. A share of this size is large enough that the 2023 foreign-born institutional rate of 0.899% should not be quoted as a criminal-incarceration rate without the caveat attached.

## 9. Sources with table numbers

| Datum | Publication | Table |
|---|---|---|
| 2022 offence × race counts | Prisoners in 2023 – Statistical Tables, NCJ 310197, 2025-09-30 | Table 16 (`p23stt16.csv`) |
| 2022 offence × race percents | same | Table 17 |
| 2023 imprisonment rate by race and age | same | Table 13 |
| 2013–2023 sentenced by race (restatement test) | same | Table 3 |
| 2021 offence × race counts | Prisoners in 2022 – Statistical Tables, NCJ 307149 | Table 17 |
| 2022 imprisonment rate by race and age | same | Table 13 |
| 2012–2022 sentenced by race (restatement test) | same | Table 3 |
| 2009 original offence × race | Prisoners in 2010, NCJ 236096 | Appendix Table 16b |
| 2009 restated offence × race | Prisoners in 2011, NCJ 239808 | Appendix Table 8 |
| 2010 imprisonment rate by race and age | Prisoners in 2010 | Appendix Table 15 |
| Jail inmates held for ICE, 2014–2024 | Jail Inmates in 2024, NCJ 311504, 2026-09-08 | Table 14 |
| Population denominators 2021, 2022 | Census Vintage 2024, NC-EST2024 national ASRH | `nc-est2024-alldata-r-file04/06.csv`, AGE=999 |
| Population denominator 2009 | Census intercensal 2000–2010 national | `us-est00int-alldata.csv`, AGE=999, MONTH=7 |
| ICE ADP FY2023 | ICE Annual Report FY2023 | Detention section |
| ACS foreign-born institutional, men 18–39 | `acs_institutional_2026_09_16/acs_institutional_rates.csv` | rows `2023,total,All,foreign_born` |

## 10. Verification

```
cd /Users/alien/Projects/immigration-research && uv run python3 infra/immigration-fiscal/bjs_2023_update_2026_09_16/bjs_2023.py
EXIT=0
```

PASS. Full output in `bjs_2023_result.txt`.
