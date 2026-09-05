**Verdict:** Separating race and nativity changes the wage comparison. In ACS2024, **non-Hispanic Black-alone native adults averaged $42,850 in annual wage/salary income**, versus **$51,268 for foreign-born Black-alone adults**, **$64,613 for native non-Hispanic White-alone adults**, and **$33,723 for Mexico-born adults**. These all-adult means include zeros. Employment and income-source selection matter; none of these differences is a causal effect of race, nativity or immigration policy.

2026-09-05. Population: **civilian noninstitutional adults aged25–64, resident in the 50 states/DC**, including noninstitutional group quarters. These are resident stocks, not the 2022–26 arrival cohort. All dollar amounts below are **2024 dollars** for the rolling past12months, not hourly pay or a single calendar-year payroll. [CALCULATION: actual ACS2024 national PUMS; [2024 dictionary](https://www2.census.gov/programs-surveys/acs/tech_docs/pums/data_dict/PUMS_Data_Dictionary_2024.pdf).]

| Population | Wages, all adults | Earnings, all adults | Currently employed | Wages among annual positive-wage recipients |
|---|---:|---:|---:|---:|
| All native — aggregate | $59,814 | $63,168 | 78.2% | $76,413 |
| All foreign-born — aggregate | $55,707 | $59,346 | 77.8% | $73,959 |
| Mexico-born — aggregate | $33,723 | $37,258 | 74.7% | $47,847 |
| Native: Hispanic, any race | $49,174 | $51,607 | 78.4% | $62,520 |
| Native: non-Hispanic Black alone | **$42,850** | **$44,515** | **73.4%** | **$56,657** |
| Native: non-Hispanic White alone | $64,613 | $68,501 | 79.1% | $82,145 |
| Native: non-Hispanic Asian alone | $86,127 | $89,397 | 83.4% | $102,535 |
| Native: non-Hispanic other/multiracial | $55,245 | $58,164 | 75.9% | $72,063 |
| Foreign-born: Hispanic, any race | $36,269 | $39,711 | 76.5% | $49,934 |
| Foreign-born: non-Hispanic Black alone | **$51,268** | **$53,511** | **80.7%** | **$63,011** |
| Foreign-born: non-Hispanic White alone | $79,385 | $85,296 | 77.7% | $106,286 |
| Foreign-born: non-Hispanic Asian alone | $78,476 | $81,706 | 79.4% | $99,959 |
| Foreign-born: non-Hispanic other/multiracial | $58,938 | $62,959 | 75.9% | $79,941 |

The five detailed categories are mutually exclusive **within each nativity**. Hispanic origin takes precedence regardless of race, so Hispanic Black respondents enter the Hispanic row. Aggregate rows overlap the detailed rows and must not be added to them. Native is Census `NATIVITY=1`, including citizens at birth abroad, not merely birth in the continental US. [SOURCE: dictionary `HISP`, `RAC1P`, `NATIVITY`; CALCULATION: `wage_profiles_2024.csv`.]

**Definitions:** wages are `WAGP`, wage/salary income excluding self-employment income. Earnings are `PERNP`, which includes wages and self-employment income/losses. Both are before personal taxes and deductions. All-adult means retain zero income and negative earnings. The last column conditions on **positive `WAGP` during the past12months**, including people currently unemployed; it is not an employed-at-interview mean. Current employment is `ESR=1/2`. Conditioning instead on current employment gives Black-alone native/foreign-born mean wages of **$56,640/$61,971** and earnings of **$58,830/$64,452**. That denominator can include self-employed people reporting zero wages. No hourly wage is estimated, and these means do not hold weeks/hours worked constant. Current residence/civilian status need not describe the entire income year. [SOURCE: dictionary fields `WAGP`, `PERNP`, `ESR`; [Census subject definitions](https://www2.census.gov/programs-surveys/acs/tech_docs/subject_definitions/2024_ACSSubjectDefinitions.pdf), pp.94,98; CALCULATION: profiles.]

The non-Hispanic Black-alone comparison uses **112,220 native and 18,871 foreign-born sampled adults**, representing **17.24 million and 3.15 million** adults. Foreign-born-minus-native all-adult wages are **+$8,418 (95% sampling interval +$7,196 to +$9,640)**; employment is **+7.28 percentage points (+6.53 to +8.04)**. Native Black-alone versus native White-alone wages are **−$21,763 (−$22,244 to −$21,282)**. The corresponding native Black-alone-minus-Mexico-born wage gap is **+$9,127 (+$8,483 to +$9,770)**, despite the Black-alone group's employment share being **1.33 points lower**. These are population means, not comparisons of equally situated workers. For example, bachelor's-or-higher shares are **27.5% native Black alone versus 38.7% foreign-born Black alone**; education is described, not controlled away. [CALCULATION: `wage_profiles_2024.csv`, `wage_contrasts_2024.csv`.]

Black alone versus any-race sensitivity leaves the main ordering intact:

| Definition | Native wages, all adults | Foreign-born wages, all adults |
|---|---:|---:|
| Non-Hispanic Black alone | $42,850 | $51,268 |
| Non-Hispanic Black alone or in combination | $43,635 | $52,866 |
| Black alone or in combination, including Hispanic origin | $43,851 | $51,585 |

The second definition uses `RACBLK=1` and moves qualifying multiracial people out of the other/multiracial category, producing a separate exhaustive partition. The third is an explicitly overlapping sensitivity domain, not an extra category to add to the main table. [SOURCE: dictionary `RACBLK`; CALCULATION: profiles and replicate partition-conservation checks.]

Actual ACS2019 was also processed with the same definitions. In common 2024 dollars, non-Hispanic Black-alone native wages rose **$39,500→$42,850**, a difference of **+$3,349 (+$2,811 to +$3,888)**; foreign-born Black-alone wages rose **$48,724→$51,268**, **+$2,544 (+$904 to +$4,184)**. Native Black-alone employment changed **71.17%→73.37%**; foreign-born Black-alone employment changed **81.12%→80.66%**, with that latter change's interval including zero. These are repeated cross-sections with migration, demographic and reporting changes. Census revised race questions and processing in2020, so the groups are not compositionally fixed between2019 and2024. [CALCULATION: `wage_changes_2019_2024.csv`; SOURCE: [2019 dictionary](https://www2.census.gov/programs-surveys/acs/tech_docs/pums/data_dict/PUMS_Data_Dictionary_2019.pdf), [Census race-question changes](https://www.census.gov/programs-surveys/acs/technical-documentation/user-notes/2021-03.html).]

Each year's incomes receive its record's `ADJINC/1,000,000` once. The2019 results then receive the **1.2307078233** R-CPI-U-RS factor from the previously verified Census comparison guidance;2024 receives no additional between-year conversion. Every ratio is recomputed under all80 person replicate weights, retaining negative replicate weights; variance is `4/80 × Σ(estimate_r−estimate_full)²`. Within-year contrasts preserve covariance, including nested Black-definition comparisons. Between-year change intervals assume independent samples. These sampling intervals exclude nonresponse/undercoverage, income reporting and topcoding, classification changes and choice of estimand. No age/sex/education/occupation standardization or causal race coefficient is estimated. [SOURCE: [Census comparison guidance](https://www.census.gov/programs-surveys/acs/guidance/comparing-acs-data/2024.html), [2024 PUMS accuracy](https://www2.census.gov/programs-surveys/acs/tech_docs/pums/accuracy/2024AccuracyPUMS.pdf); selected inflation vintage pinned in `wage_sources.json`.]

Reproduce with [analyze_wage_race.py](../infra/immigration-fiscal/build/analyze_wage_race.py):

```sh
uv run --with duckdb,numpy,pandas python3 infra/immigration-fiscal/build/analyze_wage_race.py \
  --acs-2024 /Volumes/2TBPNY/corpus/census_acs_2024_1yr/csv_pus.zip \
  --acs-2019 /Volumes/2TBPNY/corpus/census_acs_2019_1yr/csv_pus.zip \
  --inflation .scratch/cohort-clarity-20260905/availability/inflation.json \
  --output .scratch/clarity-next-20260905/wage-race
uv run --with duckdb,numpy,pandas python3 -m unittest discover \
  -s infra/immigration-fiscal/tests -p 'test_wage_race.py'
uv run python3 .scratch/clarity-next-20260905/wage-race/verify_outputs.py
```

**Validation:**5 targeted tests passed. Both raw passes matched official record counts (**3,422,888 in2024;3,239,553 in2019**) plus national population, males and age25–34 point/replicate-SE anchors. Independent calculations checked **648 profiles,120 within-year contrasts,324 real-dollar/yearly changes**, and **30 complete81-estimate vectors** against the earlier independent ACS pipeline. Each race partition conserves every weighted sufficient-statistic column in every replicate. No database or peer analysis was changed.

Outputs, sufficient statistics, replicate vectors, verification and manifests are in `.scratch/clarity-next-20260905/wage-race/`. Source SHA-256:2024 ZIP `afdc6d90c6e2f0bab365ed32d95ba4c4d8ac651162f46ac7861295b2dc469894`;2019 ZIP `18e4ece4cc24781c01e8046c2d5afbabeb1f15452ddec43f60fdf3b1f6e67b92`; inflation/calibration input `3564bf10a18f34cad6466b94358f28cd89df600edfc88e91c8c24a4275017518`.
