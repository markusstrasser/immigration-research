claude-opus-5-5

**Verdict:** Statewide student-level scale-score SDs are in `derived/scale_sd.csv` (258 rows) for
New York 2018, 2019 and 2022–2025, Illinois 2023–2025 and Colorado 2017–2019 and 2021–2026. Every
listed year covers grades 3–8 in both subjects, except Colorado 2021, where only the six required tests
(ELA 3, 5, 7; math 4, 6, 8) had statewide participation. **Illinois-only SDs for 2018 (PARCC), 2019, 2021
and 2022 are not published anywhere I could find.** The only published figures for those years pool
Illinois with other PARCC/New Meridian members. They are in the CSV under pooled labels such as
`IL+BIE+NJ+NM`, never as `IL`. Illinois is 41–53% of the pooled test takers in 2018, 53–63% in 2019, 94–99% in
2021 and 54–66% in 2022. New York publishes no 2021 scale-score SD. No 2026 New York or Illinois technical
report exists yet.

# Statewide scale-score SDs, grades 3–8 ELA and math (NY, IL, CO)

Worker: data acquisition for `newcomer_school_shock_2026_09_28`, 2026-09-28. Purpose: to let the lane
convert school-level scale-score effects into student-level SD units. Every value in the CSV is quoted
below from the pinned raw file named beside it. `extract_scale_sd.py` pins each input by sha256, anchors
each value to its table title and writes the CSV. Two runs are byte-identical.

## What the CSV holds

| `state` label | Years | Source | Table | Precision |
|---|---|---|---|---|
| `NY` | 2018, 2019, 2022, 2023, 2024, 2025 | NYSED, *New York State Testing Program 20xx: ELA and Mathematics Grades 3–8* technical reports | Table 9.1/9.9 (2018, 2023) or 8.1/8.9 (other years), "… Scale Score Distribution Summary" | mean, SD 2 dp |
| `IL` | 2023 | New Meridian, *Technical Report 2022–2023, Illinois Assessment of Readiness* (Illinois only) | Tables A.12.35–A.12.46, "Full Summative Score" row | 2 dp |
| `IL` | 2024, 2025 | Pearson for ISBE, *IAR Technical Report 2023–2024* and *2024–2025* | Tables B.1–B.12, "Overall Score" row | 2 dp |
| `IL+BIE+DC+DoDEA+MD+NJ+NM` | 2018 | Pearson, *PARCC Final Technical Report for 2018 Administration* (ISBE copy) | Tables A.12.27–A.12.32, A.12.36–A.12.41 | 2 dp |
| `IL+BIE+NJ+NM` | 2019 | New Meridian, *Technical Report 2018–2019, Alternate Blueprint* (ISBE copy) | Tables A.12.48–A.12.53, A.12.57–A.12.62 | 2 dp |
| `IL+BIE+DoDEA` | 2021 | New Meridian, *Technical Report 2020–2021, Alternate Blueprint* (ISBE copy) | Tables A.12.42–A.12.47, A.12.50–A.12.55 | 2 dp |
| `IL+DC+DoDEA+NJ` | 2022 | New Meridian, *Technical Report 2021–2022, Alternate Blueprint* (ISBE copy) | Tables A.12.40–A.12.45, A.12.48–A.12.53 | 2 dp |
| `CO` | 2017, 2018 | CDE, *CMAS Math and ELA State Summary Results* PDFs | page 1, "Overall Results" | integers |
| `CO` | 2019, 2021–2026 | CDE, *CMAS … District and School Summary Achievement Results* workbooks (the Denver worker's `_cache/denver/`, read in place) | sheet "CMAS ELA and Math", `Level = STATE` rows | integers |

Columns: `state, year, subject, grade, n, mean, sd, source_file, source_table, page`. `year` is the spring
test year. `subject` is `ELA` or `math`. `n` is the table's N-count, which is the valid-score count. `mean`
and `sd` are the values as printed. `page` is the 1-based PDF page (as `pdftotext -f N` counts it) for PDF
sources. For workbooks it is the 1-based worksheet row. BIE is the Bureau of Indian Education, DC the District
of Columbia, DoDEA the Department of Defense Education Activity, MD Maryland, NJ New Jersey and NM New
Mexico.

## Gaps and cautions

1. **Illinois 2018, 2019, 2021 and 2022 are pooled, not statewide.** These consortium reports pool Illinois
   with other members in their scale-score tables. Their by-state appendices give only counts and
   demographics (Tables A.5.x in 2018, A.11.x after that). Illinois share of pooled test takers, grades 3–8
   [CALCULATION: Illinois "N of Students" ÷ pooled "N of Students", rows quoted below]:

   | Year | ELA | Math |
   |---|---|---|
   | 2018 | 41.7–42.0% | 40.8–52.5% (the upper value is grade 8) |
   | 2019 | 53.0–53.4% | 52.6–62.6% (the upper value is grade 8) |
   | 2021 | 93.7–95.2% | 93.6–99.2% |
   | 2022 | 54.6–56.1% | 54.2–65.7% (the upper value is grade 8) |

   Where Illinois-only SDs exist (2023–2025), grade 3 ELA is 40.77, 42.14 and 41.23. The pooled grade 3 ELA
   SD is 42.68 in 2018, 42.05 in 2019, 41.06 in 2021 and 44.30 in 2022. These are different years, so the
   comparison cannot show how far the pooled figures differ from Illinois alone [DATA: CSV rows].
2. **New York changed scales twice.** Scores from 2022 and 2023 cannot be compared; standardize within
   each year.
   - 2018: "… are the mean and SD of the scale scores, which equal 600 and 20, respectively" (2018 report,
     PDF p.74; this is the scaling step for the 2018 calibration population). "New scale score cuts were set this summer in 2018 and therefore, it was not
     necessary to perform any linking to the previous scale." (p.88)
   - 2023: "The scale score of 450 was chosen as the desired Level 3 cut score so that the scale-score
     ranges of the new 2023 scale would not overlap with previous Grades 3–8 tests or other NYSTP tests.
     The desired SD of scale scores was set as 23 for ELA and 27 for mathematics." (2023 report, PDF p.63)
3. **New York population.** Each year's summary says "ELA and mathematics data include examinees with
   valid scores from all public, non-public, and charter schools" (PDF p.109 in 2018, p.104 in 2019, p.100
   in 2022, p.97 in 2023, p.86 in 2024 and p.85 in 2025; capitalization varies by year).
4. **New York 2021 has no scale-score SD.** The 2021 report has no scale-score distribution section. Its
   Tables 7.1 and 7.3 give "raw-score (RS) means and raw-score standard deviations (SDs)" (PDF p.19),
   footnoted "Based on Session 1 test questions from the original administration test data." (PDF p.20).
   2021 was not requested, and the script fails loudly if a revised file changes this.
5. **Grade 8 math sometimes excludes accelerated students.** Where it does, the grade 8 math SD describes
   a truncated population [DATA: CSV `n` column].
   - New York, all years: grade 8 math N is 94,063–116,534, against 147,257–156,304 in ELA. The 2024
     report gives the reason: "The number of students “Not Tested” was larger here than for other
     mathematics grades due to some students taking a Regents exam instead of the NYSTP Grade 8
     mathematics test." (PDF p.37)
   - Colorado 2017 and 2018: grade 8 math N is 43,158 and 49,189, against 56,211 and 58,684 in ELA. High-school
     math tests appear as separate rows (2018 PDF p.1: Algebra I 8,097, Geometry 1,661, Integrated I 672,
     Integrated II 89). From 2019, grade 8 math N roughly equals ELA N (58,862 against 58,807 in 2019).
   - Pooled Illinois years: grade 8 math N is 263,809 (2018), 225,726 (2019) and 211,563 (2022), against
     339,283, 266,251 and 249,387 in ELA. The state-count rows below put almost all of the shortfall
     outside Illinois. Illinois's own grade 8 gap is 3,735 in 2018, 845 in 2019 and 909 in 2022
     [CALCULATION: Illinois ELA grade 8 minus math grade 8 N].
   - Illinois-only years (2023–2025): grade 8 math N roughly equals ELA N (for example 138,558 against
     138,908 in 2023).
6. **Colorado 2021: only the required tests are statewide.** The cached workbook covers "2021 REQUIRED
   TESTS": ELA 3, 5, 7 and math 4, 6, 8. Participation was 57.9–76.2% (workbook column "Participation
   Rate"). CDE's separate non-required-tests file (`_cache/sd/cde_cmas_state_summary_2021_nonrequired.xlsx`)
   says: "Fewer than ten percent of students participated in these optional assessments. As a result,
   interpretations from statewide results on these assessments should be completely avoided." Its rows are
   quoted below and **left out of the CSV**.
7. **Colorado precision.** CDE prints means and SDs as integers, so each SD carries up to ±0.5 points of
   rounding, about ±1.5% of a 33-point SD.
8. **Colorado 2017 and 2018 cross-check.** The state-summary PDFs give the SD. For every grade-subject
   cell, the script asserts that the PDF's valid-score count and mean equal the `STATE` row of the Denver
   worker's district/school workbook, which has no SD column in those years. All 24 cells match.
9. **Illinois 2025 kept the 650–850 scale.** Only the performance levels changed. "The IAR student results
   are reported as total scale scores ranging from 650 to 850 for all tests" (2024–2025 report, PDF p.39).
   "The performance level cut scores were established in 2025 during a standard setting to unify the
   performance levels across the ACT, IAR, and Illinois Science Assessment (ISA)." (p.10). "All assessments
   were pre-equated, meaning the scoring was based on item parameters estimated using data from earlier
   administrations." (p.51). No new scale was introduced in 2025.
10. **Illinois 2021 is a partial spring cohort.** "Only Bureau of Indian Education, Department of Defense
    Education Activity, and Illinois administered forms in spring 2021. Illinois provided the option for
    students to test in fall 2021 instead of spring 2021." (2020–2021 report, PDF p.26). The Illinois spring
    grade 3 ELA count was 90,774, against 137,092 in 2019.
11. **Illinois 2024–2025 N.** The "Overall Score" N equals the valid-case count in Table 8.1, for example
    129,997 for 2024 ELA grade 3. "Students missing information on one or more of the demographic
    variables were omitted from the subgroup analyses" (2023–2024 report, PDF p.36). That applies to the
    subgroup rows, not the overall row.
12. **No 2026 NY or IL reports.** The NYSED listing
    (https://www.nysed.gov/state-assessment/grades-3-8-technical-information-and-reports, fetched
    2026-09-28) ends at 2025. `…/ei-ela-math-technical-report-2026.pdf` returns 404. ISBE's IAR page lists
    the 2023–2024 and 2024–2025 reports, and `https://www.isbe.net/Documents/IAR-Tech-Report-2025-2026.pdf`
    returns 404. Colorado 2026 is published and is in the CSV.

## Searches for Illinois-only 2018, 2019, 2021 and 2022 SDs (none found)

- ISBE IAR page (https://www.isbe.net/iar, fetched 2026-09-28), "Technical Reports" section. For 2019–2022
  it links only the New Meridian consortium reports above; `New-Meridian-Tech-Rpt-2019.pdf` and
  `New-Meridian-Tech-Report-2020-21.pdf` have the same byte lengths as the cached copies (7,501,936 and
  6,861,328).
- PARCC 2018 final technical report (https://www.isbe.net/Documents/PARCC-Tech-Report-2017-2018.pdf). Its
  scale-score tables are consortium-wide. Its state appendix (Tables A.5.1–A.5.27) holds counts and
  demographics only. Its only other state-level table is "Table 13.9 State-specific SGP Progressions"
  (growth, not SDs).
- New Meridian 2019, 2021 and 2022 reports: the same pattern. "Table 15.9 State-specific SGP Progressions"
  in 2021 and 2022 is the only other state-level table.
- Illinois Report Card public data sets for 2019 and 2022 (the Chicago worker's `_cache/chicago/isbe/`,
  read in place). No column on any sheet, including "IAR", has "scale", "deviation", "SD" or "mean" in its
  header rows.
- ISBE explainer PDFs `IAR-Score-Interpretation.pdf`, `IAR-Demystified.pdf` and
  `Deep-Dive-Assessments-2019.pdf`: no standard deviations. The first mentions only average scale scores.
- WebSearch queries, none of which returned an Illinois-only SD table:
  - "Illinois Assessment of Readiness IAR technical report scale score mean standard deviation by grade"
  - "Illinois IAR 2019 statewide "standard deviation" scale score grade 3 ELA mathematics Illinois students"
  - "PARCC 2018 technical report Illinois scale score mean standard deviation by state grade"
  - "isbe.net IAR statewide results scale score distribution 2019 2021 2022 Illinois "mean scale score""
  - "Illinois IAR 2022 "standard deviation" statewide grade 3-8 scale score pandemic learning loss Illinois report IWERC"
  - ""Illinois Assessment of Readiness" "standard deviation" scale score 2019 statewide grade IWERC OR "Discovery Partners Institute" learning loss technical appendix"
  - "site:isbe.net PARCC technical report 2018 Illinois"
  - ""Illinois" IAR 2021 OR 2022 statewide "mean scale score" "standard deviation" grade 3 4 5 6 7 8 ELA math table"
  - "New Meridian technical report Illinois state-specific scale score statistics addendum IAR fall 2021"
- Not tried: a request to ISBE, which is outside a worker's remit.

## Population statements that fix the `state` labels

- 2018 PARCC (PDF p.19): "Section 5 – Test Taker Characteristics: Participation included students from
  Bureau of Indian Education, District of Columbia, Department of Defense Education Activity, Illinois,
  Maryland, New Jersey, and New Mexico."
- 2019 (PDF p.108): "Approximately two million students from the Bureau of Indian Education, Illinois, New
  Jersey, and New Mexico participated in the operational administration of the summative assessments
  during the 2018–2019 school year." Table 11.1 note (p.109): "This information is provided for all
  participating states combined."
- 2021 (PDF p.92): "Over a million forms were administered in the Bureau of Indian Education, the
  Department of Defense Education Activity, and Illinois during the 2020–2021 school year."
- 2022 (PDF p.85): "Over a million forms were administered in the Department of Defense Education
  Activity, the District of Columbia, Illinois, and New Jersey during the 2021–2022 school year."
- 2023 (PDF p.65): "Almost 800,000 forms were administered in Illinois during the 2022–2023 school year."
- 2024 and 2025 (PDF p.1): "Prepared by Pearson for the Illinois State Board of Education (ISBE)".

### Pooled versus Illinois test-taker rows, verbatim

In the 2019, 2021 and 2022 reports, the state label is printed on the line next to the row. The 2021
tables also split "N of / Students" across lines. PDF pages:

```
2018 PARCC p.247  PARCC N of Students 2,475,049 338,927 345,483 348,524 344,520 338,731 339,283 128,229 188,597 102,755
2018 PARCC p.248  IL N of Students 859,725 141,226 144,266 146,243 143,620 142,125 142,245 n/a n/a n/a
2018 PARCC p.249  PARCC N of Students 2,468,267 348,117 354,080 355,854 345,712 323,440 263,809 221,242 130,412 123,787 750 873 191
2018 PARCC p.249  IL N of Students 862,339 141,946 144,832 146,506 144,009 141,727 138,510 4,344 335 111 17 2 n/a
2019 p.224 (All States, ELA)  N of Students 1,879,282 256,870 265,169 271,778 275,277 269,386 266,251 121,619 118,322 34,610
2019 p.224 (IL, ELA)          N of Students 855,200 137,092 140,534 144,713 146,878 143,739 142,244 n/a n/a n/a
2019 p.226 (All States, math) N of Students 1,871,889 258,807 266,629 272,714 275,732 264,960 225,726 134,107 105,010 66,789 673 541 201
2019 p.226 (IL, math)         N of Students 852,627 136,938 140,253 144,476 146,399 143,162 141,399 n/a n/a n/a n/a n/a n/a
2021 p.200 (All States, ELA)  590,314 96,928 99,006 99,632 98,590 96,950 96,028 2,767 413
2021 p.201 (IL, ELA)          554,553 90,774 92,980 94,084 93,199 92,127 91,389 n/a n/a
2021 p.202 (All States, math) 582,332 96,011 97,740 98,306 96,924 91,315 92,946 3,424 2,922 2,726 17 1
2021 p.203 (IL, math)         546,315 89,899 91,756 92,831 91,707 90,539 89,583 n/a n/a n/a n/a n/a
2022 p.194 (All States, ELA)  N of Students 1,542,916 229,185 232,317 237,847 238,260 245,106 249,388 103,744 7,069
2022 p.195 (IL, ELA)          N of Students 792,057 125,191 127,131 131,381 132,030 136,346 139,978 n/a n/a
2022 p.196 (All States, math) N of Students 1,556,982 230,054 232,955 238,545 238,630 235,692 211,563 115,174 40,404 13,965
2022 p.197 (IL, math)         N of Students 788,132 124,674 126,558 130,894 131,359 135,578 139,069 n/a n/a n/a
```

Columns are Total, then grades 3–8, then high-school grades or courses.

## Colorado 2021 non-required tests (not in the CSV)

`_cache/sd/cde_cmas_state_summary_2021_nonrequired.xlsx`, sheet "Overall ELA and Math", selected rows
(row 19, "Grade 04 - Spanish", N 53, is omitted; columns: Report Category, Number of Valid Scores, Participation Rate, Mean Scale Score, Standard
Deviation, Percent Met or Exceeded Expectations):

```
row 18: Grade 04 - English | 5725 | 9.4 | 743 | 35 | 45.9
row 20: Grade 06 | 5437 | 8.3 | 738 | 30 | 36.5
row 21: Grade 08 | 4463 | 6.6 | 743 | 38 | 45.0
row 23: Grade 03 (math) | 5942 | 9.8 | 741 | 38 | 42.6
row 24: Grade 05 (math) | 5932 | 9.4 | 739 | 34 | 38.7
row 25: Grade 07 (math) | 5510 | 8.2 | 733 | 27 | 27.3
```

Row 9 of the same sheet: "To address health and safety considerations and maximize instructional time
in spring 2021, some English language arts and math assessments were not required in spring 2021 as
established by state law and federal assessment waiver.* Fewer than ten percent of students participated
in these optional assessments. As a result, interpretations from statewide results on these assessments
should be completely avoided."

## Quoted tables

### New York

`_cache/sd/nysed_3-8_techreport_2018.pdf`, PDF page 109:

```
Table 9.1. ELA Scale Score Distribution Summary
                     Scale Score            Percentile Ranks
 Grade N-Count Mean          SD      10th   25th   50th   75th   90th
   3   182,885 599.79       20.22    573    586    602    614    626
   4   184,266 599.77       20.17    572    586    601    614    624
   5     177,609 599.88     20.27    573    587    602    614    625
   6     173,183 599.74     20.30    574    587    601    614    623
   7     161,958 599.74     20.26    574    587    601    613    623
   8     154,663 599.59     20.50    574    588    601    614    624
```

`_cache/sd/nysed_3-8_techreport_2018.pdf`, PDF page 117:

```
Table 9.9. Mathematics Scale Score Distribution Summary
                    Scale Score            Percentile Ranks
 Grade N-Count Mean         SD      10th   25th   50th   75th     90th
   3   184,970 599.48      20.19    574    587    601    613      623
   4   186,331 599.38      20.23    573    587    600    612      624
   5     178,875 599.09    20.39    574    587    600    613      625
   6     173,731 599.36    20.36    575    586    600    613      624
   7     160,487 599.16    20.42    572    587    601    613      623
   8     116,534 598.98    20.47    568    586    601    612      623
```

`_cache/sd/nysed_3-8_techreport_2019.pdf`, PDF page 104:

```
Table 8.1. ELA Scale Score Distribution Summary
                    Scale Score            Percentile Ranks
 Grade N-Count Mean         SD      10th   25th   50th   75th   90th
   3   182,559 599.39      19.46    574    586    602    612    624
   4   186,205 598.42      19.56    573    587    599    612    622
   5     180,679 599.14    21.44    572    587    601    612    625
   6     179,908 598.04    22.49    570    585    600    615    626
   7     170,595 599.61    21.05    572    587    600    613    626
   8     156,304 599.58    20.14    574    587    601    613    624
```

`_cache/sd/nysed_3-8_techreport_2019.pdf`, PDF page 112:

```
Table 8.9. Mathematics Scale Score Distribution Summary
               Scale Score                 Percentile Ranks
Grade N-Count Mean     SD           10th   25th 50th 75th       90th
  3   184,576 599.81 19.69          574    588 601 613          622
  4   188,143 600.01 20.38          574    588 601 614          624
  5   181,771 599.74 20.80          572    586 601 613          624
  6   179,611 600.24 20.17          573    588 602 614          625
  7   168,909 600.78 20.68          575    588 602 615          626
   8     115,886 599.39    21.67    569    588    602    614    624
```

`_cache/sd/nysed_3-8_techreport_2022.pdf`, PDF page 100:

```
Table 8.1. ELA Scale Score Distribution Summary
                          Scale Score
    Grade N-Count       Mean      SD
      3   165,209       598.21 19.31
      4   168,725       595.76 20.87
      5   165,024       600.87 19.65
      6   163,509        602.5 20.59
      7   159,762       604.09 19.18
      8   150,130       599.96 21.50
```

`_cache/sd/nysed_3-8_techreport_2022.pdf`, PDF page 107–108:

```
Table 8.9. Mathematics Scale Score Distribution Summary
                         Scale Score
    Grade N-Count       Mean     SD
      3   166,446       596.21 20.54
      4   169,535       595.48 22.21
   5   163,950      595.20 21.65
   6   160,087      596.99 20.18
   7   154,425      597.51 20.07
   8    97,284      595.72 20.66
```

`_cache/sd/nysed_3-8_techreport_2023.pdf`, PDF page 98:

```
Table 9.1. ELA Scale Score Distribution Summary
                         Scale Score
 Grade     N-Count     Mean      SD
    3      166,155     444.41   23.06
    4      166,173     447.39   23.06
    5      165,259     445.53   23.07
    6      165,051     444.95   22.93
    7      160,467     447.56   23.05
    8      152,212     450.78   23.00
```

`_cache/sd/nysed_3-8_techreport_2023.pdf`, PDF page 105:

```
Table 9.9. Mathematics Scale Score Distribution Summary
                              Scale Score
 Grade         N-Count     Mean         SD
    3          169,444      451.61      27.06
    4          169,293      451.69      27.39
    5          167,238       449.7       27.1
    6          164,792       449.8      27.02
    7          158,339      452.57      27.17
    8          102,560      444.63      26.97
```

`_cache/sd/nysed_3-8_techreport_2024.pdf`, PDF page 86:

```
Table 8.1. ELA Scale Score Distribution Summary
                         Scale Score
 Grade     N-Count     Mean      SD
    3       164,461    443.27   22.17
    4       168,811    444.42   22.95
    5       158,765    444.11   22.99
    6       164,913    443.16   22.65
    7       159,902    447.62   22.82
    8       147,257    449.25   24.63
```

`_cache/sd/nysed_3-8_techreport_2024.pdf`, PDF page 94:

```
Table 8.9. Mathematics Scale Score Distribution Summary
                          Scale Score
 Grade     N-Count      Mean       SD
   3       167,123      451.21     26.34
   4       167,995      456.15     29.27
   5       155,787      451.58     27.52
   6       164,601      451.37     26.87
   7       157,751      457.06     29.01
   8        94,063      447.18     27.79
```

`_cache/sd/nysed_3-8_techreport_2025.pdf`, PDF page 85:

```
Table 8.1. ELA Scale Score Distribution Summary
                        Scale Score
 Grade     N-Count    Mean      SD
   3       168,225    450.16   22.58
   4       163,567    451.18   22.32
   5       163,017    450.79   22.78
   6       162,321    447.93   22.75
   7       163,708    448.62   22.66
   8       151,464    450.09   22.58
```

`_cache/sd/nysed_3-8_techreport_2025.pdf`, PDF page 93:

```
Table 8.9. Mathematics Scale Score Distribution Summary
                         Scale Score
 Grade     N-Count     Mean       SD
   3       167,949     455.70    28.46
   4       161,749     457.98    27.73
   5       160,121     454.65    27.06
   6       158,220     452.72    26.92
   7       157,998     456.56    28.14
   8        95,233     448.75    27.15
```

### Illinois (PDF page, table title, then the overall row as printed)

`_cache/sd/isbe_parcc_techreport_2018.pdf` (IL+BIE+DC+DoDEA+MD+NJ+NM):

```
p359 Table A.12.27 Subgroup Performance for ELA/L Scale Scores: Grade 3
      Full Summative Score 338,927 738.80 42.68 650 850
p361 Table A.12.28 Subgroup Performance for ELA/L Scale Scores: Grade 4
      Full Summative Score 345,483 743.92 37.34 650 850
p363 Table A.12.29 Subgroup Performance for ELA/L Scale Scores: Grade 5
      Full Summative Score 348,524 742.50 35.32 650 850
p365 Table A.12.30 Subgroup Performance for ELA/L Scale Scores: Grade 6
      Full Summative Score 344,520 741.96 33.38 650 850
p367 Table A.12.31 Subgroup Performance for ELA/L Scale Scores: Grade 7
      Full Summative Score 338,731 745.09 40.18 650 850
p369 Table A.12.32 Subgroup Performance for ELA/L Scale Scores: Grade 8
      Full Summative Score 339,283 743.30 40.42 650 850
p377 Table A.12.36 Subgroup Performance for Mathematics Scale Scores: Grade 3
      Full Summative Score 348,117 742.56 37.24 650 850
p378 Table A.12.37 Subgroup Performance for Mathematics Scale Scores: Grade 4
      Full Summative Score 354,080 738.12 33.85 650 850
p379 Table A.12.38 Subgroup Performance for Mathematics Scale Scores: Grade 5
      Full Summative Score 355,854 738.22 33.85 650 850
p380 Table A.12.39 Subgroup Performance for Mathematics Scale Scores: Grade 6
      Full Summative Score 345,712 734.45 31.92 650 850
p381 Table A.12.40 Subgroup Performance for Mathematics Scale Scores: Grade 7
      Full Summative Score 323,440 735.75 29.36 650 850
p382 Table A.12.41 Subgroup Performance for Mathematics Scale Scores: Grade 8
      Full Summative Score 263,809 725.69 37.06 650 850
```

`_cache/sd/isbe_iar_techreport_2019.pdf` (IL+BIE+NJ+NM):

```
p318 Table A.12.48 Subgroup Performance for ELA/L Scale Scores: Grade 3
      Full Summative Score 256,870 738.54 42.05 650 850
p320 Table A.12.49 Subgroup Performance for ELA/L Scale Scores: Grade 4
      Full Summative Score 265,169 742.91 38.37 650 850
p322 Table A.12.50 Subgroup Performance for ELA/L Scale Scores: Grade 5
      Full Summative Score 271,778 744.04 36.42 650 850
p324 Table A.12.51 Subgroup Performance for ELA/L Scale Scores: Grade 6
      Full Summative Score 275,277 743.02 34.47 650 850
p326 Table A.12.52 Subgroup Performance for ELA/L Scale Scores: Grade 7
      Full Summative Score 269,386 746.87 41.47 650 850
p328 Table A.12.53 Subgroup Performance for ELA/L Scale Scores: Grade 8
      Full Summative Score 266,251 746.55 42.10 650 850
p336 Table A.12.57 Subgroup Performance for Mathematics Scale Scores: Grade 3
      258,807 743.16 36.43 650 850   [row label: Full Summative Score]
p337 Table A.12.58 Subgroup Performance for Mathematics Scale Scores: Grade 4
      Full Summative Score 266,629 739.36 34.87 650 850
p338 Table A.12.59 Subgroup Performance for Mathematics Scale Scores: Grade 5
      272,714 737.90 33.04 650 850   [row label: Full Summative Score]
p339 Table A.12.60 Subgroup Performance for Mathematics Scale Scores: Grade 6
      275,732 732.71 32.62 650 850   [row label: Full Summative Score]
p340 Table A.12.61 Subgroup Performance for Mathematics Scale Scores: Grade 7
      264,960 737.26 30.54 650 850   [row label: Full Summative Score]
p341 Table A.12.62 Subgroup Performance for Mathematics Scale Scores: Grade 8
      225,726 728.24 38.46 650 850   [row label: Full Summative Score]
```

`_cache/sd/isbe_iar_techreport_2021.pdf` (IL+BIE+DoDEA):

```
p278 Table A.12.42 Subgroup Performance for ELA/L Scale Scores: Grade 3
      Full summative score 96928 724.36 41.06 650 850
p280 Table A.12.43 Subgroup Performance for ELA/L Scale Scores: Grade 4
      Full summative score 99006 728.57 35.38 650 850
p282 Table A.12.44 Subgroup Performance for ELA/L Scale Scores: Grade 5
      Full summative score 99632 731.20 34.06 650 850
p284 Table A.12.45 Subgroup Performance for ELA/L Scale Scores: Grade 6
      Full summative score 98590 733.68 31.38 650 850
p286 Table A.12.46 Subgroup Performance for ELA/L Scale Scores: Grade 7
      Full summative score 96950 733.47 37.42 650 850
p288 Table A.12.47 Subgroup Performance for ELA/L Scale Scores: Grade 8
      Full summative score 96028 734.91 37.11 650 850
p294 Table A.12.50 Subgroup Performance for Mathematics Scale Scores: Grade 3
      Full Summative 96011 730.93 38.66 650 850
p295 Table A.12.51 Subgroup Performance for Mathematics Scale Scores: Grade 4
      97740 726.00 34.73 650 850   [row label: Full Summative Score]
p296 Table A.12.52 Subgroup Performance for Mathematics Scale Scores: Grade 5
      Full Summative 98306 726.90 33.87 650 850
p297 Table A.12.53 Subgroup Performance for Mathematics Scale Scores: Grade 6
      Full Summative 96924 724.92 32.04 650 850
p298 Table A.12.54 Subgroup Performance for Mathematics Scale Scores: Grade 7
      Full Summative 91315 732.06 28.12 650 850
p299 Table A.12.55 Subgroup Performance for Mathematics Scale Scores: Grade 8
      Full Summative 92946 723.42 39.41 650 850
```

`_cache/sd/isbe_iar_techreport_2022.pdf` (IL+DC+DoDEA+NJ):

```
p264 Table A.12.40 Subgroup Performance for ELA/L Scale Scores: Grade 3
      Full Summative Score 229,184 730.45 44.30 650 850
p266 Table A.12.41 Subgroup Performance for ELA/L Scale Scores: Grade 4
      Full Summative Score 232,317 737.26 38.96 650 850
p268 Table A.12.42 Subgroup Performance for ELA/L Scale Scores: Grade 5
      Full Summative Score 237,847 738.17 37.48 650 850
p270 Table A.12.43 Subgroup Performance for ELA/L Scale Scores: Grade 6
      Full Summative Score 238,260 737.27 33.89 650 850
p272 Table A.12.44 Subgroup Performance for ELA/L Scale Scores: Grade 7
      Full Summative Score 245,105 739.51 40.53 650 850
p274 Table A.12.45 Subgroup Performance for ELA/L Scale Scores: Grade 8
      Full Summative Score 249,387 737.91 41.92 650 850
p280 Table A.12.48 Subgroup Performance for Mathematics Scale Scores: Grade 3
      Full Summative Score 230,053 737.99 39.38 650 850
p281 Table A.12.49 Subgroup Performance for Mathematics Scale Scores: Grade 4
      Full Summative Score 232,955 732.80 35.41 650 850
p282 Table A.12.50 Subgroup Performance for Mathematics Scale Scores: Grade 5
      Full Summative Score 238,545 730.00 35.36 650 850
p283 Table A.12.51 Subgroup Performance for Mathematics Scale Scores: Grade 6
      Full Summative Score 238,630 727.54 32.92 650 850
p284 Table A.12.52 Subgroup Performance for Mathematics Scale Scores: Grade 7
      Full Summative Score 235,692 733.63 29.03 650 850
p285 Table A.12.53 Subgroup Performance for Mathematics Scale Scores: Grade 8
      Full Summative Score 211,563 720.42 37.50 650 850
```

`_cache/sd/isbe_iar_techreport_2023.pdf` (IL):

```
p177 Table A.12.35 Subgroup Performance for ELA/L Scale Scores: Grade 3
      Full Summative Score 128,356 723.35 40.77 650 850
p179 Table A.12.36 Subgroup Performance for ELA/L Scale Scores: Grade 4
      Full Summative Score 127,980 734.11 37.78 650 850
p181 Table A.12.37 Subgroup Performance for ELA/L Scale Scores: Grade 5
      Full Summative Score 129,738 734.37 35.29 650 850
p183 Table A.12.38 Subgroup Performance for ELA/L Scale Scores: Grade 6
      Full Summative Score 133,179 733.46 33.18 650 850
p185 Table A.12.39 Subgroup Performance for ELA/L Scale Scores: Grade 7
      Full Summative Score 134,267 735.41 38.12 650 850
p187 Table A.12.40 Subgroup Performance for ELA/L Scale Scores: Grade 8
      Full Summative Score 138,908 738.26 37.97 650 850
p189 Table A.12.41 Subgroup Performance for Mathematics Scale Scores: Grade 3
      Full Summative Score 128,109 731.72 37.74 650 850
p190 Table A.12.42 Subgroup Performance for Mathematics Scale Scores: Grade 4
      Full Summative Score 127,833 728.98 34.50 650 850
p191 Table A.12.43 Subgroup Performance for Mathematics Scale Scores: Grade 5
      Full Summative Score 129,562 727.88 33.19 650 850
p192 Table A.12.44 Subgroup Performance for Mathematics Scale Scores: Grade 6
      Full Summative Score 132,858 725.16 32.56 650 850
p193 Table A.12.45 Subgroup Performance for Mathematics Scale Scores: Grade 7
      Full Summative Score 133,956 731.18 30.21 650 850
p194 Table A.12.46 Subgroup Performance for Mathematics Scale Scores: Grade 8
      Full Summative Score 138,558 723.86 41.04 650 850
```

`_cache/sd/isbe_iar_techreport_2024.pdf` (IL):

```
p102 Table B.1. Scale Score Performance by Demographic Subgroup—ELA/L Grade 3
      Overall Score 129,997 727.19 42.14 650 850
p103 Table B.2. Scale Score Performance by Demographic Subgroup—ELA/L Grade 4
      Overall Score 129,858 734.73 38.11 650 850
p104 Table B.3. Scale Score Performance by Demographic Subgroup—ELA/L Grade 5
      Overall Score 129,335 736.77 36.27 650 850
p105 Table B.4. Scale Score Performance by Demographic Subgroup—ELA/L Grade 6
      Overall Score 130,763 742.56 33.87 650 850
p107 Table B.5. Scale Score Performance by Demographic Subgroup—ELA/L Grade 7
      Overall Score 133,542 742.09 34.11 650 850
p108 Table B.6. Scale Score Performance by Demographic Subgroup—ELA/L Grade 8
      Overall Score 134,873 744.60 38.91 650 850
p109 Table B.7. Scale Score Performance by Demographic Subgroup—Mathematics Grade 3
      Overall Score 130,057 733.52 37.02 650 850
p110 Table B.8. Scale Score Performance by Demographic Subgroup—Mathematics Grade 4
      Overall Score 129,924 730.82 33.94 650 850
p110 Table B.9. Scale Score Performance by Demographic Subgroup—Mathematics Grade 5
      Overall Score 129,432 729.66 33.77 650 850
p111 Table B.10. Scale Score Performance by Demographic Subgroup—Mathematics Grade 6
      Overall Score 130,694 728.37 31.76 650 850
p111 Table B.11. Scale Score Performance by Demographic Subgroup—Mathematics Grade 7
      Overall Score 133,394 733.81 28.81 650 850
p112 Table B.12. Scale Score Performance by Demographic Subgroup—Mathematics Grade 8
      Overall Score 134,715 727.00 40.16 650 850
```

`_cache/sd/isbe_iar_techreport_2025.pdf` (IL):

```
p115 Table B.1. Scale Score Performance by Demographic Subgroup—ELA/L Grade 3
      Overall Score 132,063 100.0% 729.69 41.23 650 850
p116 Table B.2. Scale Score Performance by Demographic Subgroup—ELA/L Grade 4
      Overall Score 130,742 100.0% 736.19 36.84 650 850
p118 Table B.3. Scale Score Performance by Demographic Subgroup—ELA/L Grade 5
      Overall Score 130,422 100.0% 739.26 35.95 650 850
p119 Table B.4. Scale Score Performance by Demographic Subgroup—ELA/L Grade 6
      Overall Score 129,426 100.0% 741.26 33.77 650 850
p121 Table B.5. Scale Score Performance by Demographic Subgroup—ELA/L Grade 7
      Overall Score 130,924 100.0% 744.41 34.04 650 850
p122 Table B.6. Scale Score Performance by Demographic Subgroup—ELA/L Grade 8
      Overall Score 134,023 100.0% 747.32 38.98 650 850
p124 Table B.7. Scale Score Performance by Demographic Subgroup—Mathematics Grade 3
      Overall Score 131,915 100.0% 731.74 36.35 650 850
p124 Table B.8. Scale Score Performance by Demographic Subgroup—Mathematics Grade 4
      Overall Score 130,600 100.0% 731.68 33.25 650 850
p125 Table B.9. Scale Score Performance by Demographic Subgroup—Mathematics Grade 5
      Overall Score 130,283 100.0% 728.07 33.46 650 850
p125 Table B.10. Scale Score Performance by Demographic Subgroup—Mathematics Grade 6
      Overall Score 129,232 100.0% 726.67 32.57 650 850
p126 Table B.11. Scale Score Performance by Demographic Subgroup—Mathematics Grade 7
      Overall Score 130,683 100.0% 735.38 29.24 650 850
p126 Table B.12. Scale Score Performance by Demographic Subgroup—Mathematics Grade 8
      Overall Score 133,755 100.0% 728.24 41.18 650 850
```

### Colorado

`_cache/sd/cde_cmas_state_summary_2017.pdf`, PDF page 1 (CMAS ELA and Math (PARCC) 2016-2017 Achievement Results: Overall Results); header lines and grade 3–8 rows:

```
  Report Category                      # of         Mean        Standard        % Did Not
                                       Valid        Scale       Deviation
 ELA Grade 03                         63,608         738            40              18.6          17.5            23.8          36.8           3.3            40.1           37.4          2.7       96.4
 ELA Grade 04                         64,116         743            35              12.0          17.7            26.2          35.1           9.0            44.1           43.9          0.2       95.7
 ELA Grade 05                         63,391         745            34              10.5          17.0            26.2          40.9           5.3            46.3           41.2          5.1       94.3
 ELA Grade 06                         60,841         741            31              10.1          20.3            29.0          34.4           6.1            40.6           38.3          2.3       92.3
 ELA Grade 07                         58,778         743            38              14.0          16.8            25.0          30.8           13.5           44.2              41         3.2       89.1
 ELA Grade 08                         56,211         742            38              14.8          17.6            24.3          34.2           9.1            43.4           41.6          1.8       85.2
 Math Grade 03                        65,422          739            37             14.8         19.1             26.1        31.2           8.7           40.0           38.9           1.1         96.7
 Math Grade 04                        65,009          735            33             14.7         23.1             28.1        30.7           3.3           34.0           33.3           0.7         95.8
 Math Grade 05                        63,446          736            32             13.4         23.5             29.5        28.9           4.7           33.6           34.3           -0.7        94.4
 Math Grade 06                        60,950          733            32             15.5         24.6             29.0        26.3           4.5           30.9            31            -0.1        92.5
 Math Grade 07                        56,210          732            27             11.9         27.4             34.9        23.6           2.2           25.8           26.2           -0.4        89.2
 Math Grade 08                        43,158          722            35             29.5         23.8             25.6        19.6           1.4           21.0           20.4           0.6         85.7
```

`_cache/sd/cde_cmas_state_summary_2018.pdf`, PDF page 1 (2018 CMAS English Language Arts/Literacy and Mathematics State Achievement Results: Overall Results); header lines and grade 3–8 rows:

```
                         # of  Mean Standard % Did Not       % Partially      %        % Met     % Exceeded 2018 % Met or 2017 % Met or      %         2018
    Report               Valid Scale Deviation   Yet Meet       Met      Approached Expectations Expectations  Exceeded      Exceeded     Change** Participation
ELA Grade 03             63,016    739        40           17.8            18.1        23.8      36.7           3.7            40.4            40.1            0.3        97.2
ELA Grade 04             64,789    745        35           10.6            17.2        26.1      35.6          10.4            46.1            44.1            2.0        96.7
ELA Grade 05             65,359    746        34           9.9             16.1        26.7      41.9           5.5            47.4            46.3            1.1        95.9
ELA Grade 06             63,647    743        34           10.5            18.9        27.8      35.1           7.7            42.8            40.6            2.2        94.2
ELA Grade 07             60,907    744        40           14.4            15.7        23.3      31.5          15.1            46.6            44.2            2.4        92.0
ELA Grade 08             58,684    743        40           14.7            17.1        24.4      33.4          10.4            43.8            43.4            0.4        88.7
Mathematics Grade 03     64,714    739       37           14.3             19.8        26.9      31.0           8.1            39.1            40.0           -0.9        97.3
Mathematics Grade 04     65,995    734       33           15.4             23.5        27.2      31.1           2.7            33.9            34.0           -0.1        96.9
Mathematics Grade 05     65,516    737       34           13.7             23.1        27.7      29.3           6.2            35.5            33.6           1.9         96.2
Mathematics Grade 06     63,765    733       31           14.1             27.2        28.4      26.2           4.2            30.4            30.9           -0.5        94.3
Mathematics Grade 07     59,983    733       29           12.3             24.7        34.2      26.0           2.8            28.8            25.8           3.0         92.1
Mathematics Grade 08     49,189    728       37           22.9             23.6        25.4      25.4           2.7            28.2            21.0           7.2         89.0
```

`_cache/denver/cde_cmas_overall_2019.xlsx`, sheet 'CMAS ELA and Math', header columns [5] 'Subject', [6] 'Grade', [8] 'Number of Valid Scores', [11] 'Mean Scale Score', [12] 'Standard Deviation'; STATE rows (worksheet row: subject, grade, valid scores, mean, SD):

```
row 14: English Language Arts | 03 | 60,795 | 740 | 41
row 15: English Language Arts | 04 | 63,257 | 745 | 36
row 16: English Language Arts | 05 | 65,757 | 747 | 34
row 17: English Language Arts | 06 | 64,493 | 743 | 33
row 18: English Language Arts | 07 | 62,642 | 745 | 39
row 19: English Language Arts | 08 | 58,807 | 745 | 40
row 21: Mathematics | 03 | 62,560 | 740 | 36
row 22: Mathematics | 04 | 64,473 | 735 | 32
row 23: Mathematics | 05 | 65,917 | 738 | 34
row 24: Mathematics | 06 | 64,650 | 732 | 31
row 25: Mathematics | 07 | 62,787 | 735 | 29
row 26: Mathematics | 08 | 58,862 | 736 | 41
```

`_cache/denver/cde_cmas_overall_2021.xlsx`, sheet 'CMAS ELA and Math', header columns [5] 'Content', [6] 'Grade', [8] 'Number of Valid Scores', [11] 'Mean Scale Score', [12] 'Standard Deviation'; STATE rows (worksheet row: subject, grade, valid scores, mean, SD):

```
row 29: English Language Arts | 03 | 45,187 | 736 | 43
row 31: English Language Arts | 05 | 46,909 | 746 | 32
row 32: English Language Arts | 07 | 42,928 | 742 | 37
row 33: Mathematics | 04 | 46,781 | 729 | 33
row 34: Mathematics | 06 | 44,813 | 727 | 32
row 35: Mathematics | 08 | 39,202 | 730 | 39
```

`_cache/denver/cde_cmas_overall_2022.xlsx`, sheet 'CMAS ELA and Math', header columns [5] 'Content', [6] 'Grade', [8] 'Number of Valid Scores', [13] 'Mean Scale Score', [14] 'Standard Deviation'; STATE rows (worksheet row: subject, grade, valid scores, mean, SD):

```
row 15: English Language Arts | 03 | 55,078 | 737 | 44
row 16: English Language Arts | 04 | 55,741 | 740 | 36
row 17: English Language Arts | 05 | 57,360 | 745 | 33
row 18: English Language Arts | 06 | 55,956 | 742 | 34
row 19: English Language Arts | 07 | 55,263 | 741 | 37
row 20: English Language Arts | 08 | 52,725 | 742 | 41
row 25: Mathematics | 03 | 56,479 | 737 | 39
row 26: Mathematics | 04 | 56,881 | 732 | 33
row 27: Mathematics | 05 | 57,420 | 736 | 35
row 28: Mathematics | 06 | 55,932 | 728 | 33
row 29: Mathematics | 07 | 55,281 | 730 | 28
row 30: Mathematics | 08 | 52,802 | 731 | 40
```

`_cache/denver/cde_cmas_overall_2023.xlsx`, sheet 'CMAS ELA and Math', header columns [5] 'Content', [6] 'Grade', [8] 'Number of Valid Scores', [13] 'Mean Scale Score', [14] 'Standard Deviation'; STATE rows (worksheet row: subject, grade, valid scores, mean, SD):

```
row 15: English Language Arts | 03 | 55,737 | 737 | 44
row 16: English Language Arts | 04 | 55,517 | 742 | 37
row 17: English Language Arts | 05 | 56,656 | 747 | 34
row 18: English Language Arts | 06 | 55,600 | 743 | 33
row 19: English Language Arts | 07 | 53,885 | 744 | 38
row 20: English Language Arts | 08 | 51,755 | 741 | 41
row 25: Mathematics | 03 | 57,382 | 738 | 39
row 26: Mathematics | 04 | 56,787 | 733 | 33
row 27: Mathematics | 05 | 56,895 | 737 | 35
row 28: Mathematics | 06 | 55,911 | 730 | 33
row 29: Mathematics | 07 | 54,138 | 731 | 28
row 30: Mathematics | 08 | 52,032 | 732 | 41
```

`_cache/denver/cde_cmas_overall_2024.xlsx`, sheet 'CMAS ELA and Math', header columns [5] 'Content', [6] 'Grade', [8] 'Number of Valid Scores', [13] 'Mean Scale Score', [14] 'Standard Deviation'; STATE rows (worksheet row: subject, grade, valid scores, mean, SD):

```
row 15: English Language Arts | 03 | 54,572 | 738 | 44
row 16: English Language Arts | 04 | 55,710 | 741 | 37
row 17: English Language Arts | 05 | 55,950 | 747 | 34
row 18: English Language Arts | 06 | 54,560 | 743 | 33
row 19: English Language Arts | 07 | 53,327 | 746 | 39
row 20: English Language Arts | 08 | 50,334 | 740 | 41
row 25: Mathematics | 03 | 56,724 | 740 | 38
row 26: Mathematics | 04 | 57,395 | 735 | 35
row 27: Mathematics | 05 | 56,598 | 739 | 34
row 28: Mathematics | 06 | 55,120 | 732 | 32
row 29: Mathematics | 07 | 53,895 | 733 | 29
row 30: Mathematics | 08 | 50,798 | 732 | 41
```

`_cache/denver/cde_cmas_overall_2025.xlsx`, sheet 'CMAS ELA and Math', header columns [5] 'Content', [6] 'Grade', [8] 'Number of Valid Scores', [13] 'Mean Scale Score', [14] 'Standard Deviation'; STATE rows (worksheet row: subject, grade, valid scores, mean, SD):

```
row 20: English Language Arts | 03 | 56,598 | 737 | 44
row 21: English Language Arts | 04 | 55,071 | 741 | 37
row 22: English Language Arts | 05 | 56,595 | 746 | 35
row 23: English Language Arts | 06 | 54,607 | 743 | 34
row 24: English Language Arts | 07 | 53,148 | 747 | 39
row 25: English Language Arts | 08 | 50,297 | 741 | 41
row 30: Mathematics | 03 | 58,763 | 739 | 39
row 31: Mathematics | 04 | 56,789 | 736 | 34
row 32: Mathematics | 05 | 57,000 | 739 | 34
row 33: Mathematics | 06 | 55,127 | 732 | 34
row 34: Mathematics | 07 | 53,581 | 735 | 30
row 35: Mathematics | 08 | 50,929 | 734 | 42
```

`_cache/denver/cde_cmas_overall_2026.xlsx`, sheet 'CMAS ELA and Math', header columns [5] 'Content', [6] 'Grade', [8] 'Number of Valid Scores', [13] 'Mean Scale Score', [14] 'Standard Deviation'; STATE rows (worksheet row: subject, grade, valid scores, mean, SD):

```
row 20: English Language Arts | 03 | 54,154 | 738 | 46
row 21: English Language Arts | 04 | 56,808 | 744 | 39
row 22: English Language Arts | 05 | 55,942 | 748 | 34
row 23: English Language Arts | 06 | 54,941 | 742 | 33
row 24: English Language Arts | 07 | 52,766 | 745 | 38
row 25: English Language Arts | 08 | 49,977 | 741 | 40
row 30: Mathematics | 03 | 55,928 | 740 | 39
row 31: Mathematics | 04 | 58,268 | 738 | 35
row 32: Mathematics | 05 | 55,955 | 740 | 34
row 33: Mathematics | 06 | 55,081 | 734 | 33
row 34: Mathematics | 07 | 52,864 | 737 | 30
row 35: Mathematics | 08 | 50,110 | 736 | 43
```

## Reproduction

```sh
# from the repository root
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
    infra/immigration-fiscal/newcomer_school_shock_2026_09_28/extract_scale_sd.py
```

- Two consecutive runs on 2026-09-28 wrote byte-identical `derived/scale_sd.csv`: 258 rows plus the header,
  LF line endings, sha256 `79b40966843a9042672503049f5f71ea36ae00a3cb195f8afbdbe192367a68f2`. Both runs
  exited 0.
- PDF text comes from `pdftotext -layout -enc UTF-8` (poppler 26.09.0). Page numbers are PDF page indices.
- The raw pulls, with original URL, bytes, sha256 and retrieval time, are listed in `_cache/sd/SOURCES.tsv`.
  The Denver workbooks are read in place; their sha256 values match `_cache/denver/SOURCES.tsv`.
- The script stops with `[BLOCKED]` in these cases:
  - an input's sha256 differs from its pin;
  - a table title is not found exactly once as a standalone line;
  - a table yields other than grades 3–8, or the Illinois row under a title is not the overall row
    (label "Full Summative"/"Overall Score", min 650, max 850);
  - a report's population statement is missing, or a Colorado 2017/2018 PDF cell disagrees with the
    workbook;
  - the row count is not 258, a state-year-subject-grade key repeats, or a value falls outside a
    plausibility band (NY 2018–2022 mean 580–620 and SD 15–30; NY 2023+ mean 430–470 and SD 18–35;
    IL/CO mean 650–850 and SD 20–60; N at least 30,000).
- Positive controls (scratch test, not kept): a corrupted pin and a missing title each raised
  `[BLOCKED]`. The New York row pattern accepted a data row and rejected a subscore row. The Illinois row
  pattern parsed the wrapped-label 2019 layout and the 2025 layout with a percent column.

## Log

### 2026-09-28 06:40 — progress note (appended while working)

- NY: NYSED grades 3–8 technical reports for 2018, 2019, 2021, 2022, 2023, 2024, 2025 downloaded to
  `_cache/sd/`. Each (except 2021) has "Table x.1 ELA Scale Score Distribution Summary" and
  "Table x.9 Mathematics Scale Score Distribution Summary" with N-Count, Mean, SD by grade. The 2021
  report has no scale-score summary (its Tables 7.1/7.3 are raw-score statistics "Based on Session 1
  test questions from the original administration test data"). No 2026 report is listed on
  https://www.nysed.gov/state-assessment/grades-3-8-technical-information-and-reports (checked
  2026-09-28; latest is 2025).
- CO: the Denver worker's CDE "District and School Summary Achievement Results" files carry STATE rows
  with a "Standard Deviation" column for 2019 and 2021–2026 (not 2017, 2018). For 2017 and 2018 the
  CDE "CMAS Math and ELA State Summary Results" PDFs (downloaded to `_cache/sd/`) carry "Mean Scale
  Score" and "Standard Deviation" by grade.
- IL: the ISBE-hosted IAR technical reports for 2019, 2021 and 2022 are New Meridian consortium
  reports whose scale-score tables pool several states (2019: BIE, IL, NJ, NM; 2021: BIE, DoDEA, IL;
  2022: DC, DoDEA, IL, NJ). The 2023 (New Meridian), 2024 and 2025 (Pearson for ISBE) reports are
  Illinois-only. Search for Illinois-only 2018, 2019, 2021, 2022 figures is in progress.

### 2026-09-28 06:55 — final note

- The Illinois-only search closed without a find (see "Searches for Illinois-only …"). The pooled
  2018/2019/2021/2022 tables went into the CSV under population labels, and the verdict above replaces
  `pending`.
- `extract_scale_sd.py` ran three times after its last edit, and each run wrote the same
  `derived/scale_sd.csv` (sha256 `79b40966…a68f2`, 258 rows). `_cache/sd/SOURCES.tsv` lists all 17 raw
  pulls. The Denver and Chicago caches were only read, never written.
