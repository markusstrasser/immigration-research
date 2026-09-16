**Verdict:** Parental selectivity does organise the second-generation ranking, and it does so strongly. Regressing second-generation BA+ share on a Feliciano-style selectivity index (first-generation BA share in the US minus origin-country BA share) across 29 parental origins gives R² = 0.91 with a coefficient of 0.81 (HC1 SE 0.046). **Mexico's residual is essentially zero** (−1.7 points in the bivariate spec, −0.4 with dummies, −2.7 in the cohort-matched spec): Mexican-American second-generation attainment of 22.0% BA+ is exactly what the least-selected large stream predicts, not an anomaly needing a separate explanation. Mexico is the only large origin with **negative** selectivity on the contemporaneous measure (first-gen BA 9.9% against Mexico's resident 17.0%); Honduras is the only other negative. Refugee origins do **not** deviate as a class on the primary spec (+5.1, p = 0.34), but they do once the first generation is cohort-matched to pre-2000 arrivals (+12.3, p = 0.03); either way the effect is carried by Vietnam, whose second generation over-performs its predicted value by 17 to 26 points while Laos and Cambodia sit at or below prediction on the primary spec. The measure's main weakness is that it cannot cleanly separate selectivity from the parents' own education level, because origin-country attainment has almost no independent predictive power on its own (R² = 0.008, p = 0.53).

[UNVERIFIED] for the interpretive claims; the CPS tabulations below are verified against three published Census benchmarks (§5).

Built 2026-09-16 from Census CPS ASEC microdata API, pooled 2019–2024, weights divided by 6.

---

## 1. Verification (all three checks PASS)

Computed from the all-ages pull, unpooled single-year weights, generation defined as Census defines it (native-born = citizenship recode 1–3; second generation = native-born with at least one foreign-born parent, where parent birthplaces in US outlying areas count as native).

| Year | 2nd gen, all ages (mine) | Census Table 1 | Diff | 2nd gen 18–64 vs Table 2 | 2nd gen Mexican vs Table 4 |
|---|---|---|---|---|---|
| 2019 | 40,349,535 | 40,260,000 | +0.22% | +0.21% | +0.12% |
| 2020 | 40,881,830 | 40,790,000 | +0.23% | +0.38% | +0.23% |
| 2021 | 40,031,171 | 40,330,000 | −0.74% | −0.64% | −0.58% |
| 2022 | 41,045,139 | 40,960,000 | +0.21% | +0.19% | +0.25% |
| 2023 | 42,153,362 | 42,110,000 | +0.10% | +0.10% | +0.02% |
| 2024 | 41,780,309 | 41,760,000 | +0.05% | +0.06% | +0.06% |

Worst deviation is 0.74%, against a 3% tolerance on Table 1 and 5% on Table 4. Total population reproduces to 324.4M–332.4M across the six years. Mexican second generation is matched on the detailed-Hispanic-origin recode, which is how Census Table 4 is built, at all ages so the age restriction is reversed as the brief required.

Pew direction check: Pew reported 21% BA+ for second-generation Hispanics in 2012. This pull gives 27.6% for 2019–2024 at ages 25–44 (27.0% at 25–34). Higher, as a decade of rising attainment implies. Direction consistent.

## 2. Second generation by parental origin, ages 25–44

Parental origin is the father's birth country when he is foreign-born, otherwise the mother's. Origins with at least 150 unweighted second-generation respondents. Earnings are weighted medians of annual personal earnings for full-time full-year workers (50+ weeks, 35+ usual hours, positive earnings). Full table in `secgen_by_origin.csv`.

| Origin | n2 | BA+ % | <HS % | Median earnings | 1st-gen BA % (25–64) | Origin BA % | Selectivity |
|---|---|---|---|---|---|---|---|
| Mexico | 10,174 | 22.0 | 10.3 | 45,000 | 9.9 | 17.0 | **−7.1** |
| Philippines | 1,431 | 55.4 | 1.1 | 60,000 | 57.5 | 18.1 | 39.5 |
| Germany | 852 | 46.6 | 3.4 | 59,500 | 53.2 | 29.6 | 23.7 |
| India | 786 | 84.9 | 1.0 | 89,000 | 87.4 | 12.1 | 75.3 |
| El Salvador | 735 | 30.9 | 5.6 | 50,000 | 10.5 | 8.4 | 2.1 |
| China | 722 | 78.4 | 3.2 | 82,000 | 64.6 | 7.7 | 56.9 |
| Vietnam | 721 | 63.1 | 2.2 | 65,000 | 31.7 | 11.5 | 20.2 |
| Canada | 716 | 51.7 | 1.5 | 70,000 | 63.9 | 32.4 | 31.5 |
| Korea | 663 | 65.5 | 2.2 | 67,000 | 69.3 | 34.5 | 34.7 |
| United Kingdom | 651 | 55.7 | 2.1 | 67,000 | 65.4 | 39.6 | 25.8 |
| Cuba | 585 | 48.2 | 3.5 | 60,000 | 32.2 | 15.3 | 16.9 |
| Dominican Republic | 572 | 37.0 | 5.7 | 55,000 | 23.3 | 14.4 | 9.0 |
| Japan | 433 | 61.5 | 0.3 | 65,000 | 69.0 | 25.5 | 43.4 |
| Guatemala | 430 | 28.2 | 8.2 | 48,000 | 9.1 | 5.7 | 3.4 |
| Colombia | 363 | 48.2 | 1.4 | 52,000 | 46.5 | 16.2 | 30.3 |
| Italy | 357 | 65.2 | 0.9 | 75,000 | 45.5 | 16.5 | 29.1 |
| Jamaica | 315 | 50.6 | 4.0 | 49,500 | 35.2 | 11.0 | 24.3 |
| Laos | 302 | 34.3 | 4.9 | 50,000 | 17.7 | 5.2 | 12.5 |
| Taiwan | 272 | 83.3 | 2.1 | 78,000 | 86.2 | 8.6 | 77.6 |
| Portugal | 243 | 59.1 | 3.0 | 70,000 | 26.6 | 23.1 | 3.4 |
| Haiti | 242 | 44.8 | 2.4 | 46,799 | 24.8 | 4.5 | 20.2 |
| Ecuador | 223 | 45.6 | 3.9 | 50,000 | 25.4 | 12.4 | 13.0 |
| Peru | 206 | 44.6 | 2.5 | 50,000 | 39.9 | 16.3 | 23.6 |
| Honduras | 178 | 38.5 | 2.9 | 50,000 | 8.9 | 9.6 | **−0.8** |
| Pakistan | 177 | 70.2 | 3.5 | 65,000 | 62.5 | 9.9 | 52.6 |
| Iran | 174 | 71.0 | 2.6 | 70,000 | 67.2 | 17.7 | 49.5 |
| Hong Kong | 172 | 83.7 | 2.3 | 91,000 | 67.8 | 14.8 | 53.0 |
| Poland | 159 | 68.8 | 0.8 | 66,000 | 48.3 | 27.7 | 20.6 |
| Cambodia | 158 | 39.0 | 7.1 | 50,000 | 18.1 | 4.6 | 13.5 |

Reference rows, same ages and pooling (`reference_groups.csv`):

| Group | n | BA+ % | <HS % | Median earnings |
|---|---|---|---|---|
| Third-plus gen non-Hispanic white | 129,093 | 47.0 | 3.6 | 60,000 |
| Third-plus gen non-Hispanic Black | 20,675 | 27.5 | 6.5 | 45,000 |
| Third-plus gen Hispanic | 16,324 | 26.9 | 8.0 | 49,000 |
| Third-plus gen, all | 174,523 | 41.8 | 4.5 | 55,000 |
| Second gen, all | 27,410 | 44.2 | 5.4 | 55,000 |
| First gen, all (25–64) | 93,957 | 37.7 | 21.0 | 50,000 |

The second generation as a whole out-attains the third-plus generation as a whole, 44.2% against 41.8%, and is close to third-plus whites at 47.0%. Third-plus Hispanics (26.9%) sit below second-generation Hispanics (27.6%), the pattern the stalled-mobility literature disputes; that comparison mixes cohorts and ethnic attrition and is not a clean generational contrast.

## 3. Regressions

Weighted least squares, weights = unweighted second-generation N, HC1 standard errors. Dependent variable is second-generation BA+ share in points. Full output in `regressions.json`, residuals in `resid_*.csv`.

| Spec | n | R² | Key coefficients (b, SE, p) |
|---|---|---|---|
| 1. Selectivity only | 29 | 0.913 | selectivity 0.810 (0.046) p<0.001 |
| 2. + first-gen BA level | 29 | 0.914 | selectivity 0.697 (0.137) p<0.001; first-gen level 0.111 (0.122) p=0.37 |
| 3. + refugee and Mexico/CentAm dummies | 29 | 0.935 | selectivity 0.602 (0.123) p<0.001; first-gen level 0.074 (0.125) p=0.55; refugee +5.10 (5.34) p=0.34; MexCentAm −7.36 (4.20) p=0.080 |
| 4. First-gen BA level only | 29 | 0.857 | 0.738 (0.061) p<0.001 |
| 5. Origin-country BA level only | 29 | **0.008** | 0.249 (0.401) p=0.53 |
| 6. Adult-arrival first gen | 28 | 0.892 | 0.785 (0.051) p<0.001 |
| 7. Barro-Lee 1990 origin vintage | 29 | 0.903 | 0.783 (0.047) p<0.001 |
| 9. Cohort-matched (pre-2000 adult arrivals vs Barro-Lee 1990) | 27 | 0.866 | 0.777 (0.062) p<0.001 |
| 10. Cohort-matched + dummies | 27 | 0.920 | selectivity 0.681 (0.071) p<0.001; refugee **+12.33 (5.72) p=0.031**; MexCentAm −5.94 (3.33) p=0.074 |

Reading. Selectivity beats the parents' education level alone (0.913 against 0.857) and survives when both enter (spec 2 and 3), while the level does not. But the gap is narrow and the two are near-collinear by construction, because the subtracted term carries almost no signal of its own (spec 5). The honest statement is that selectivity is the better of two closely related predictors, not that it is separately identified. Every vintage and cohort variant gives a coefficient between 0.68 and 0.81 and R² between 0.87 and 0.92, so the result is not an artifact of which origin-attainment series is used.

## 4. Residuals for the named origins

Points of second-generation BA+ above (+) or below (−) prediction.

| Origin | Spec 1 (bivariate) | Spec 3 (dummies) | Spec 9 (cohort-matched) |
|---|---|---|---|
| Mexico | −1.7 | −0.4 | −2.7 |
| El Salvador | −0.2 | +3.0 | +3.1 |
| Guatemala | −4.1 | −0.5 | −1.4 |
| Vietnam | **+17.2** | **+10.2** | **+26.4** |
| China | +2.8 | +6.1 | +8.2 |
| Philippines | −6.0 | −5.9 | −7.1 |
| India | −5.6 | −0.2 | −1.1 |
| Dominican Republic | +0.2 | −3.5 | +2.8 |
| Haiti | −1.1 | −2.6 | +2.5 |
| Jamaica | +1.4 | +0.1 | +2.7 |
| Cambodia | −1.4 | −8.8 | +6.0 |
| Laos | −5.3 | −13.0 | +8.9 |

Mexico is within 3 points of prediction in every spec. Vietnam is the largest positive deviation in every spec and is the single case that genuinely needs an explanation beyond selectivity. Cambodia and Laos flip sign between the primary and cohort-matched specs, which is what small cells (158 and 302 second-generation records, 86 and 105 pre-2000 first-generation records) plus a large refugee dummy will do; treat them as undetermined. The Philippines under-performs modestly and consistently, which is the known credential-downgrading pattern of a nurse-heavy stream whose US BA share overstates the transmissible advantage.

The largest positive residuals overall are Portugal (+26.8), Poland (+22.6), Vietnam (+17.2), Italy (+12.2) and Hong Kong (+11.3) in spec 1. Portugal, Poland and Italy are old European streams whose surviving first generation in a 2019–2024 survey is a small, aged, non-representative remnant. Portugal's first-generation cell has 232 records with a median entry year of 1982 and too few adult arrivals to compute a share; it drops out of the cohort-matched spec entirely. These are measurement artifacts, not substantive deviations.

## 5. Caveats

**Cohort mismatch is the main defect.** The first generation measured in 2019–2024 is not the parent cohort of the second generation measured at ages 25–44, who were born 1975–1999 to parents who arrived mostly 1970–1995. Median first-generation entry year in this sample runs from 1982 (Portugal) to 2008 (India). For India, China, Cuba, Honduras and Guatemala the measured first generation is a much later and differently selected wave than the actual parents, which inflates measured selectivity for the high-skill Asian streams in particular. Spec 9 addresses this by restricting to pre-2000 adult arrivals and pairing them with Barro-Lee 1990 origin attainment; the coefficient barely moves, which is the strongest evidence that the result is real.

**Origin-country attainment vintages differ.** Primary measure is World Bank SE.TER.CUAT.BA.ZS, latest value in 2000–2022, which ranges from 2017 (Haiti) to 2022 across countries. Taiwan, Hong Kong and Peru are absent from the World Bank series and use Barro-Lee 2010 tertiary-completed instead. Contemporaneous origin attainment understates selectivity for countries whose education expanded fast after the migration, Vietnam and China most of all: Vietnam's 2022 figure is 11.5% against 1.8% in 1990, when the refugee parents left. The Barro-Lee 1990 specs correct for this and are the more faithful implementation of Feliciano's design.

**Barro-Lee has bad cells.** Guatemala's 2010 tertiary-completed figure is 0.01%, against the World Bank's 5.7%, and Taiwan's 8.61% is implausibly low. Neither is load-bearing here because the primary spec uses World Bank values where available.

**CPS-specific limits.** Parental birthplace is self-reported by the respondent, not verified. The 2.5 generation, one foreign-born and one native-born parent, is assigned to the foreign parent's origin and is pooled with the pure second generation. Naturalized parents are indistinguishable from non-citizen parents in the origin assignment. The 2020 ASEC has known pandemic nonresponse and its weights were adjusted by Census; it is included and its verification deviation (+0.23% to +0.38%) is no worse than other years, but the composition effects inside cells are not testable here. Return migration means the measured first generation is the stayers, not the arrivals. Ethnic attrition does not affect this design, which uses parental birthplace rather than self-identification, and that is the main advantage of CPS over ACS for this question.

**Small cells.** Nine origins have between 150 and 250 second-generation records. Median earnings for those cells rest on 60 to 150 full-time full-year workers and should be read as ordinal, not as point estimates. No standard errors are attached to the cell-level shares; the regression SEs treat cell means as measured without error, which understates uncertainty for the smallest origins.

**The outcome is one outcome.** This tests attainment, not the incarceration ranking that §5 of the memo also presents. Nothing here bears on whether selectivity organises the crime ranking.

## 6. Files

All under `/Users/alien/Projects/immigration-research/infra/immigration-fiscal/secgen_selectivity_2026_09_16/`.

- `secgen_by_origin.csv` — the tidy table requested, one row per origin
- `reference_groups.csv` — third-plus-generation and pooled reference rows
- `regressions.json` — all ten specifications with HC1 SEs
- `resid_*.csv` — fitted values and residuals per specification
- `verification.csv` — the three Census benchmark comparisons by year
- `country_crosswalk.csv` — CPS 3-digit code to ISO3, World Bank and Barro-Lee attainment, refugee and Mexico/Central America dummies
- `cps_country_codes.json` — the CPS birth-country code list as pulled from the API
- `pull_cps.py`, `build_crosswalk.py`, `analyze.py` — the pipeline
- `cps_asec_2564_{2019..2024}.csv`, `cps_asec_allages_{2019..2024}.csv` — raw record-level pulls
- `urls.log` — every API request, key redacted
- `wb_ter_ba.json`, `barrolee_MF2599.csv`, `cps2024_gen_table{1,2,4}.xlsx` — external sources
- `analysis_output.txt` — the full console run

Sources: Census CPS ASEC microdata API, `https://api.census.gov/data/{2019..2024}/cps/asec/mar`. Census foreign-born generation tables, `https://www2.census.gov/programs-surveys/demo/tables/foreign-born/2024/cps2024/2024_asec_generation_table{1,2,4}.xlsx`. World Bank `SE.TER.CUAT.BA.ZS`, last updated 2026-07-13. Barro-Lee 2013 v2.2, MF 25+, `https://raw.githubusercontent.com/barrolee/BarroLeeDataSet/master/BLData/BL2013_MF2599_v2.2.csv`.
