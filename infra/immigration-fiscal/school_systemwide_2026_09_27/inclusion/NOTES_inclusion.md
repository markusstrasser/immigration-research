**Verdict:** The panel is complete and PDF-validated for all 50 states, DC and the nation (public), covering math 2000–2024 and reading 1998–2024 in grades 4 and 8 (every state from 2003), but EL exclusion as a % of all students is censored below 0.5 ("#") in 1,136 of 2,497 state-year cells, so the lane should measure EL exclusion with the published %-of-identified column or the two-decimal TDW column.

Model: claude-opus-5-5. Lane: `infra/immigration-fiscal/school_systemwide_2026_09_27/`. Built 2026-09-27/28. Counts below are [DATA: derived/validation_report.md] or [DATA: derived/naep_inclusion.csv] unless tagged otherwise.

## Outputs

Run from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/school_systemwide_2026_09_27/inclusion/acquire_inclusion.py
```

The script downloads each source to `inclusion/_cache/` only if it is absent; the lane's `.gitignore` covers `_cache/`. It parses the sources with code and rewrites `inclusion/derived/`. Two consecutive runs on 2026-09-28 exited 0 and produced byte-identical files (`shasum -a 256`). The hash of `naep_inclusion.csv` is `b9bd9e5a6039095c447e4f026cbea907736878dcf24d56c387be0f66f8e56b88`.

| file | content |
|---|---|
| `derived/naep_inclusion.csv` | Main panel, accommodations permitted: one row per subject × grade × year × jurisdiction, 2,674 rows. Math has 12 years × 2 grades × 54 jurisdictions (50 states, DC, Nation (public), DoDEA and Puerto Rico); reading has 13 × 2 × 53 (no Puerto Rico). |
| `derived/naep_inclusion_accom_not_permitted.csv` | 560 rows from samples where accommodations were not permitted: math grade 4 1992, 1996, 2000; math grade 8 1990, 1992, 1996, 2000; reading grade 4 1992, 1994, 1998; reading grade 8 1998. |
| `derived/naep_inclusion_crosscheck_summary.csv`, `derived/naep_inclusion_crosscheck_disagreements.csv` | Agreement counts per check, and all 601 disagreeing cells. |
| `derived/validation_report.md` | Per-year coverage, PDF checks, the national check, 20 seeded spot checks with the source line quoted, and the skipped row labels. |
| `derived/sources.csv` | URL, cache file, bytes and SHA-256 of all 40 sources. |
| `derived/quotes.md` | Verbatim ESSA and NAGB text, plus the NCES guideline used before 2010. |

### Main panel columns

- **Share of all students (primary source):** `{el,sd,sdel}_{identified,excluded,assessed}_pct_all`, each with a `_flag` column. Values carry 4–6 decimals, as stored in the 2024 appendix XLSX.
  - They come from the trend tables A-18/A-20 (SD and/or EL, grades 4/8), A-22/A-24 (SD) and A-26/A-28 (EL).
  - The table titles end "… when accommodations were permitted, by state/jurisdiction: Various years, 2000–24" (math) or "1998–2024" (reading) [SOURCE: https://www.nationsreportcard.gov/reports/mathematics/2024/g4_8/supporting-files/2024_technical_appendix_math_state_district.xlsx and https://www.nationsreportcard.gov/reports/reading/2024/g4_8/supporting-files/2024_technical_appendix_reading_state_district.xlsx].
  - Each row records its provenance in `pct_all_source_url` and `pct_all_source_table`.
- **Excluded as a share of identified (published):** `{el,sd,sdel}_excluded_pct_identified`, each with a `_flag` column.
  - EL and SD values for 2017 and earlier come from the 2017 state appendix trend sheets `{M,R}_G{4,8}_State_{ELL,SD}_Trend`.
  - SD and/or EL for 2017 comes from the per-year sheets `{M,R}_G{4,8}_State_Iden`.
  - 2019 comes from the 2019 appendix Tables A-29/A-30; 2022 and 2024 come from their own appendices' Tables A-29/A-30.
  - SD and/or EL exists only for 2017, 2019, 2022 and 2024; other years carry `not_in_source`.
  - Each row records its provenance in `pct_identified_source_url` and `pct_identified_source_table`.
- `{el,sd,sdel}_excluded_pct_identified_calc`: [CALCULATION] excluded ÷ identified × 100 from the share-of-all cells, to 4 decimals. It is blank when either cell is flagged.
- `{el,sd}_{identified,excluded}_pct_all_ta2022` and `_ta2019`: the same cells as printed in the 2022 and 2019 appendix XLSX files, kept raw as second sources.
  - The 2022 file stores all of them as integers.
  - The 2019 file stores integers for 1998–2005 and decimals for 2007–2019.
- **TDW columns:** `tdw_{el,sd}_excluded_pct_all` and `tdw_student_response_rate`, each with a flag, plus `tdw_{el,sd}_agrees_with_reportcard` (1/0), `tdw_row_label` and `tdw_source_url`.
  - They come from the NAEP Technical Documentation pages "Weighted student response and exclusion rates": reading 2002, and both subjects 2003–2024.
  - Values have one decimal in 2002–2003 and two from 2005 on.
  - TDW's "Total" row is mapped to Nation (public).
- **Flags:**
  - `rounds_to_zero`: the source prints "#"; the value is stored as 0.
  - `reporting_standards_not_met`: "‡"; the value is blank.
  - `not_available`: "—".
  - `not_applicable`: "†".
  - `not_in_source`: the source has no such cell.
  - `no_tdw_page`: math 2000 and reading 1998.
  - `decimal_comma_in_source`: one TDW response rate printed as "93,34".

## Coverage

The table counts states plus DC that have a value; "#" counts as a value. Each cell reads: EL identified / of which EL excluded is "#" / published EL share of identified available.

| year | math g4 | math g8 | reading g4 | reading g8 |
|---|---|---|---|---|
| 1998 | | | 41 / 11 / 14 | 38 / 14 / 8 |
| 2000 | 42 / 13 / 14 | 41 / 16 / 8 | | |
| 2002 | | | 46 / 6 / 33 | 45 / 11 / 27 |
| 2003 | 51 / 13 / 45 | 51 / 18 / 37 | 51 / 4 / 45 | 51 / 16 / 35 |
| 2005 | 51 / 17 / 42 | 51 / 25 / 33 | 51 / 8 / 42 | 51 / 15 / 33 |
| 2007 | 51 / 25 / 46 | 51 / 28 / 35 | 51 / 7 / 46 | 51 / 11 / 39 |
| 2009 | 51 / 35 / 43 | 51 / 35 / 39 | 51 / 9 / 46 | 51 / 15 / 38 |
| 2011 | 51 / 39 / 46 | 51 / 39 / 39 | 51 / 22 / 49 | 51 / 24 / 36 |
| 2013 | 51 / 44 / 48 | 51 / 43 / 36 | 51 / 30 / 47 | 51 / 34 / 39 |
| 2015 | 51 / 35 / 45 | 51 / 36 / 37 | 51 / 23 / 46 | 51 / 30 / 36 |
| 2017 | 51 / 21 / 46 | 51 / 26 / 40 | 51 / 22 / 47 | 51 / 24 / 40 |
| 2019 | 51 / 31 / 50 | 51 / 36 / 40 | 51 / 25 / 50 | 51 / 27 / 42 |
| 2022 | 51 / 28 / 48 | 51 / 31 / 43 | 51 / 28 / 48 | 51 / 28 / 43 |
| 2024 | 51 / 15 / 50 | 51 / 19 / 45 | 51 / 12 / 49 | 51 / 12 / 45 |

- **Identified and excluded as a share of all students:** complete for all 51 in every subject and grade from 2003, for EL, SD and SD and/or EL.
  - Missing earlier cells are "—". The source legend defines "—" only as "Not available" [SOURCE: 2024 math XLSX, Table A-26 (Cont-5) legend].
  - [TRAINING-DATA] State NAEP was voluntary until NCLB tied it to Title I funds from 2003, so the missing cells are states that did not take part.
  - EL identified is itself "#" in 38 state-year cells: West Virginia 15, Mississippi 7, and a few others.
- **EL excluded as a share of all students:** "#" in 1,136 of 2,497 state-year cells.
  - By subject and grade: math grade 4 316 of 603, math grade 8 352 of 602, reading grade 4 207 of 648, reading grade 8 261 of 644.
  - The smallest numeric value in the column is 0.5003 (Iowa, reading grade 8, 2003). So "#" means below 0.5 even in the decimal XLSX.
- **Published EL excluded as a share of identified:** 1,972 numeric state-year cells, 6 "#", 519 "‡" and 53 "—". The legend reads "Reporting standards not met" [SOURCE: 2024 math XLSX, Table A-29 legend].
  - "‡" covers 27–33 states in 1998 and 2000, and 6–18 states a year at grade 8 from 2002 on.
  - The 2022 per-year table prints integers; the `_calc` column gives 4 decimals for that year.
- **SD excluded as a share of identified:** available wherever the state took part.
- **TDW:** 2,335 state-year EL values. Math 2000 and reading 1998 have none.
  - The TDW sample-design index starts at 2000 [SOURCE: https://nces.ed.gov/nationsreportcard/tdw/sample_design/].
  - Its 2000 state math tables give only a combined "Weighted percentage of students identified as SD or LEP" and "Weighted percentage of students excluded" [SOURCE: https://nces.ed.gov/nationsreportcard/tdw/sample_design/2000_2001/2000_state_studsamp_participstatemathg4r3.aspx].
- **Skipped as out of scope:** urban districts (TUDA), BIE, the DDESS/DoDDS rows on the 2002–2003 TDW pages, the Virgin Islands, Guam and American Samoa, charter-school rows, and the all-schools "Nation" row of the 2017 tables. validation_report.md lists every skipped label.

## Validation

1. **2024 XLSX against the 2024 PDFs.**
   - All 39,570 parsed integer cells match. Each XLSX decimal rounds half up to the PDF integer, and "#", "—" and "‡" coincide. The PDF side is parsed independently, from `pdftotext -layout` text.
   - 540 XLSX cells have no PDF counterpart: math grade 8 SD and/or EL in 2022 and 2024. The math PDF titles that table "Various years, 2000–22", and its pages stop at 2017/2019 (PDF pp. 28–32). The XLSX carries both years in Table A-20 (Cont-5) [SOURCE: https://www.nationsreportcard.gov/reports/mathematics/2024/g4_8/supporting-files/2024_technical_appendix_math_state_district.pdf].
2. **Share-of-identified XLSX against the PDFs.** All 4,816 cells of the 2017 trend tables match [SOURCE: https://www.nationsreportcard.gov/math_2017/files/2017_Technical_Appendix_Math_State.pdf and https://www.nationsreportcard.gov/reading_2017/files/2017_Technical_Appendix_Reading_State.pdf]. All 642 cells of the 2024 Tables A-29/A-30 match too.
3. **Published share of identified against the ratio calculated from the share-of-all tables.**
   - All 1,322 EL, 2,588 SD and 847 SD and/or EL cells agree. The tolerance is 0.05 points, or 0.5 where the published cell is an integer (2022). The largest gap is 0.4992, from the integer 2022 tables.
   - The same ratio from the 2019 appendix agrees within 0.016 points (679 EL, 1,479 SD and 423 SD and/or EL cells).
   - The 2017 trend sheets and per-year sheets agree exactly (214 EL and 214 SD cells).
4. **Appendix vintages** [DATA: derived/naep_inclusion_crosscheck_disagreements.csv].
   - **2022 against 2024:** 41,898 of 41,922 overlapping cells agree within one unit of the coarser, integer cell. For EL and SD the largest gap is 0.5, so the 2022 integers are roundings of the 2024 decimals.
     - 19 of the 24 exceptions are DC 2022 SD-and/or-EL cells that the 2024 appendix revised. For example, math grade 4 identified went from 26 to 32.156141 (Table A-18 (Cont-5)).
     - The other 5 are "assessed without accommodations" cells for DC and DoDEA, reading grade 8, 2022, which the 2024 appendix prints as "—".
     - DC's EL-only and SD-only identified and excluded cells agree.
   - **2019 against 2024:** 38,520 of 38,676 cells agree. Of the 156 exceptions, 154 are in 2009 and 2 are 1994 not-permitted DoDEA reading cells.
     - In 2009, EL identified and excluded differ by at most 0.016 points (California reading grade 4 EL identified: 29.6754 vs 29.6598).
     - The large gaps are in the "assessed" columns, up to 0.91 points (Montana reading grade 8 EL assessed without accommodations: 1.5791 vs 2.4845).
     - Alabama math grade 4 EL assessed is 2.2277 in the 2024 appendix and 2.033459 in the 2019 one. Only the 2024 value fits the published 3.139% of identified: [CALCULATION] 2.3 × 3.139% = 0.072 ≈ 2.3 − 2.2277. The panel uses the 2024 appendix.
5. **National check** [SOURCE: https://www.nationsreportcard.gov/reports/mathematics/2024/g4_8/supporting-files/2024_technical_appendix_math_national.pdf p5; reading twin].
   - The task's example matches: 2024 grade 4 math EL identified is 13.478951% and excluded 0.911534% (XLSX Table A-15, all schools). The national PDF prints 13 and 1.
   - 137 of 138 year-cells match. The comparison covers EL, SD and SD and/or EL, identified and excluded, both grades, for math 2003–2024 and reading 2002–2024.
   - The mismatch is 2017 math grade 4 EL identified: 11.490565 in the XLSX, printed as 12.
   - The panel's Nation (public) row covers public schools only: 14.568742 identified and 0.98444 excluded in 2024 math grade 4. That matches the TDW "Total" row (0.98).
6. **TDW against the report card.** 2,277 of 2,427 EL cells and 2,156 of 2,427 SD cells agree. The 421 disagreements (`tdw_*_agrees_with_reportcard = 0`) fall into five groups:
   - **2003, 46 cells.** TDW attaches Colorado/Connecticut, Nebraska/New Hampshire and Nevada/New Jersey to each other's rows, in both subjects. For example, TDW "Connecticut" math grade 4 EL 0.8 and SD 1.6 are the report card's Colorado values, 0.7807 and 1.6087 [SOURCE: https://nces.ed.gov/nationsreportcard/tdw/sample_design/2002_2003/sampdsgn_2003_state_studresp_table2.aspx].
   - **2002 reading, 134 cells.** Across all 91 state cells, TDW's SD values sit a median 0.69 points below the report card (mean 0.79).
   - **2017, 194 cells.** The gaps are at most 0.32 points in either direction; the median signed gap across all 2017 state cells is about −0.01. Seven of the 194 are report-card "#" cells where TDW shows 0.51–0.64.
     - The 2017 page defines the rate "among all eligible students" [SOURCE: https://nces.ed.gov/nationsreportcard/tdw/sample_design/2017/weighted_student_response_and_exclusion_rates_for_the_2017_state_mathematics_assessment.aspx]. The 2015 page uses "all sampled students including absent, assessed, and excluded students".
     - [INFERENCE] The different definition plausibly explains the small gaps.
   - **2024 reading, 36 cells.** The alphabetical run New York–South Dakota plus Wisconsin disagrees in both grades (Ohio in grade 4 only), and no clean row permutation explains it. For example, TDW New York grade 4 EL is 0.86 against the report card's 2.216406 [SOURCE: https://nces.ed.gov/nationsreportcard/tdw/sample_design/2024/weighted_student_response_and_exclusion_rates_for_the_2024_state_reading_assessment.aspx].
   - **Other, 11 cells:**
     - 2005 math SD: North Dakota (grade 4); Alaska, North Dakota and Wyoming (grade 8).
     - 2005 reading: DC, Florida and Tennessee (grade 4); Florida (grade 8).
     - 2024 math: Puerto Rico grade 4 SD ("#" against 1.45).
   - Use the report card as the primary source, and a TDW value only where its agree flag is 1.
7. **Random spot checks.** 20 cells were drawn with seed `random.Random(20260927)`. validation_report.md quotes each raw source line; whitespace is compressed below. All 20 match.
   - Math grade 8 Delaware 2017 SD identified 16.6077 → 2024 math PDF p46, years [2017, 2019]: `Delaware 17 2 15 3 12 17 1 16 3 12`
   - Reading grade 8 Georgia 2002 SD excluded 3.0983 → 2024 reading PDF p45, years [1998, 2002]: `Georgia 10 4 6 4 2 10 3 7 4 3`
   - Reading grade 4 Colorado 2017 EL excluded 1.1942 → reading PDF p57, years [2015, 2017]: `Colorado 14 1 14 10 3 15 1 14 10 3`
   - Math grade 4 Alabama 2022 SD excluded 1.075851 → math PDF p40, years [2022, 2024]: `Alabama 13 1 12 5 8 16 1 15 4 11`
   - Math grade 4 Michigan 2005 SD identified 14.3262 → math PDF p36: `Michigan 14 4 11 3 7 13 3 10 4 7`
   - Math grade 4 Maryland 2007 SD identified 12.4583 → math PDF p36: `Maryland 13 3 10 3 7 12 4 9 3 6`
   - Reading grade 8 New Jersey 2003 SD excluded 2.2005 → reading PDF p46: `New Jersey 15 2 13 2 11 16 4 13 3 10`
   - Reading grade 4 Indiana 2022 SD identified 18.977934 → reading PDF p42: `Indiana 18 2 16 3 13 19 # 19 5 14`
   - Reading grade 4 New Mexico 2007 SD excluded 7.0652 → reading PDF p39: `New Mexico 14 7 7 3 4 13 4 8 3 5`
   - Math grade 4 Virginia 2015 SD excluded 1.0829 → math PDF p38: `Virginia 14 1 13 3 10 13 1 12 2 10`
   - Reading grade 4 South Dakota 2005 EL excluded, share of identified, 24.540579791096466 → 2017 reading PDF p20: `South Dakota — — — — 12 25 20 ‡ 13 8 17 ‡`
   - Math grade 4 Nebraska 2003 SD excluded, share of identified, 14.619740161376033 → 2017 math PDF p18: `Nebraska 32 31 15 15 12 14 13 8 9 7 7`
   - Math grade 4 Oklahoma 2024 TDW EL excluded 0.79 → TDW 2024 math row: `Oklahoma | 92.30 | 1.78 | 0.79 | 90.95 | 1.47 | 0.81`
   - The other seven are share-of-identified cells for South Carolina 2002, Michigan 2003, Mississippi 2017 and Maine 1992, and TDW rows for Iowa 2013, Minnesota 2019 and Nevada 2003. The Nevada 2003 row is one of the swapped labels; it is carried as printed and flagged 0.
8. **Manual checks**, by grepping `pdftotext -layout` text outside the script:
   - The 2017 math PDF line `Texas 41 34 13 13 14 10 5 5 3 5 5`: its last nine values (2000–2017) are the roundings of the panel's 12.875 … 5.4418.
   - The 2024 reading PDF, 2024 columns: `California 23 1 22 19 3` = 22.856978 / 1.23306 / 21.623919, and `Nation (public) 15 1 13 9 5` = 14.605667 / 1.239622 / 13.366045.

## What the national rows show

EL exclusion as a share of identified ELs, Nation (public) [DATA: naep_inclusion.csv]:

| | 1998/2000 | 2003 | 2009 | 2011 | 2019 | 2024 |
|---|---|---|---|---|---|---|
| math g4 | 17.6 | 14.2 | 5.6 | 4.1 | 4.8 | 6.8 |
| math g8 | 21.7 | 18.1 | 8.1 | 6.9 | 6.6 | 7.6 |
| reading g4 | 37.7 | 23.9 | 16.2 | 11.0 | 5.9 | 8.5 |
| reading g8 | 29.1 | 24.4 | 17.5 | 13.6 | 8.2 | 9.2 |

The decline was gradual. In math it came mostly between 2003 and 2009, before the March 2010 policy; in reading it continued through 2019. All four series rose from 2019 to 2024, and the number of states whose EL exclusion shows as "#" fell sharply in 2024.

Over the same years, the EL share of public school students (EL identified, % of all) rose:

- Math grade 4: 7.4 (2000), 10.6 (2003), 13.0 (2019), 14.6 (2024).
- Reading grade 4: 7.1 (1998), 10.4 (2003), 13.1 (2019), 14.6 (2024).

[INFERENCE] `el_identified_pct_all` is NAEP's own weighted EL share, so it can serve as the lane's EL-growth measure alongside enrollment data.

## Caveats for the lane

- **Censoring.** "#" means below 0.5% of all students, including in the decimal XLSX. The stored 0 is censored, not a measured zero.
  - For EL exclusion, prefer `el_excluded_pct_identified`, which has its own "#" in only 6 state cells. Alternatively, use the TDW value where `tdw_el_agrees_with_reportcard=1`.
  - Where the share of identified is "‡", the only available statement is "below 0.5% of all".
- **Category definitions.**
  - The notes to the per-year Tables A-29/A-30 and national Table A-15 say: "Students identified as both SD and EL were counted only once under the combined SD and/or EL category, but were counted separately under the SD and EL categories." They also say SD includes students with an IEP or protection under Section 504 [SOURCE: 2024 math XLSX, Table A-29 and A-15 notes].
  - The trend tables' own notes do not define SD. [INFERENCE] Their 2024 cells reproduce the A-29/A-30 ratios, so they use the same counts.
  - The inclusion-rate Tables A-11/A-13 use a different SD definition, which excludes students who are protected only under Section 504 [SOURCE: 2024 math XLSX, Table A-11 note].
- **Puerto Rico.** The notes say "In Puerto Rico, the English learner (EL) category is for the Spanish learner (SL)" [SOURCE: 2024 math XLSX, Table A-26 (Cont-5) note]. Drop it or treat it separately.
- **Mode and denominator changes.**
  - Math and reading results come from a digitally based assessment beginning in 2017 [SOURCE: 2024 math and reading appendix notes].
  - In 2022, a "full-time remote student who cannot be assessed" category was left out of the inclusion/exclusion denominator [SOURCE: 2024 math PDF p47 note; the reading PDF carries the same note once].
  - [INFERENCE] Year fixed effects absorb both changes, but not a state-specific response to them.
- **Nation and Nation (public).** Table A-15 and the national PDFs cover all schools. The panel's Nation (public) row and TDW "Total" cover public schools only.
- **Policy timing.** NCES and NAGB adopted the present inclusion policy in March 2010 [SOURCE: https://nces.ed.gov/nationsreportcard/about/inclusion.aspx]. No source read here states the first assessment run under it [UNVERIFIED]. Under the earlier NCES guidance, ELs with fewer than 3 school years of English-medium instruction could be excluded (quote c below).

## Quotes

Both quotes are verbatim in `derived/quotes.md`, generated by code from the cached pages.

- **(a) 20 U.S.C. 6311(b)(3)(A)**, ESEA §1111(b)(3)(A) as amended by ESSA [SOURCE: https://www.law.cornell.edu/uscode/text/20/6311; uscode.house.gov timed out on port 443].
  - The provision applies to "recently arrived English learners who have been enrolled in a school in one of the 50 States in the United States or the District of Columbia for less than 12 months".
  - Option (i): exclude such a learner "from one administration of the reading or language arts assessment", and exclude the learner's results from accountability for the first year.
  - Option (ii): assess and report the learner, then phase the results into accountability: excluded in year 1, growth counted in year 2, proficiency counted from year 3.
- **(b) NAGB, "NAEP Testing and Reporting on Students with Disabilities and English Language Learners"**, adopted March 6, 2010, updated August 2, 2014 [SOURCE: https://www.nagb.gov/content/dam/nagb/en/documents/policies/naep_testandreport_studentswithdisabilities.pdf].
  - ELs "who have been in United States schools for one year or more should be included", where one year means "one full academic year before the year of the assessment".
  - "Those in U.S. schools for less than one year should take the assessment if it is available in the student's primary language."
  - Reading and writing stay "in English only".
  - "The proportion of all students excluded from any NAEP sample should not exceed 5 percent", which sets the 95% inclusion goal. Among students classified as ELL or SD there is "a goal of 85 percent inclusion".
  - [INFERENCE] ELs with less than one year in U.S. schools therefore remain excludable from reading.
- **(c) Context: the earlier NCES guideline** [SOURCE: https://nces.ed.gov/nationsreportcard/about/history_inclusion.aspx, "NAEP in 1996"]. An EL student could be excluded if the student "had received reading or mathematics instruction primarily in English for less than 3 school years including the current year" and could not demonstrate knowledge even with a NAEP accommodation.

## Log

- 2026-09-27: stub created; starting source discovery.
- 00:24 source discovery: the 2024 report-card technical appendices (state_district, PDF + XLSX) carry state trend tables "Percentage of ... public school students identified as English learners [/ SD / SD and/or EL] excluded and assessed ... when accommodations were permitted, by state/jurisdiction: Various years, 2000–24" (identified, excluded, assessed as % of all students). The 2022 appendices carry the same tables through 2022 (cross-check). XLSX versions exist for 2017, 2019, 2022, 2024. 2019 technical appendix is at `.../reading/supportive_files/2019_Technical_Appendix_Reading.pdf|xlsx` and `.../mathematics/supportive_files/2019_Technical_Appendix_Math.pdf|xlsx`. TDW "Weighted student response and exclusion rates" pages exist per year (two decimals). Wayback Machine was offline (HTTP page "Temporarily Offline") during this run.
- 00:40 TDW "weighted student response and exclusion rates" pages located for every state year by crawling each year's sample-design tree (2002 reading; 2003, 2005, 2007, 2009, 2011, 2013, 2015, 2017, 2019, 2022, 2024 both subjects). URL patterns differ by year (`sampdsgn_2003_state_studresp_table{1,2}.aspx`, `2011_sampdsgn_state_studresp_{math,reading}.aspx`, `weighted_student_response_and_exclusion_rates_for_the_<year>_state_<subject>_assessment.aspx`). 2003 pages carry one decimal ("LEP" label); 2011 and later two decimals. The xlsx report-card tables carry 4–6 decimals, but print "#" for any value below 0.5, so small EL exclusion rates are censored there and only the TDW pages (and the %-of-identified tables) resolve them.
- 00:40 quotes: ESSA §1111(b)(3)(A) fetched from law.cornell.edu (uscode.house.gov refused the connection: "Failed to connect to uscode.house.gov port 443 after 75074 ms"); NAGB policy PDF fetched from nagb.gov.
- 01:05 `acquire_inclusion.py` runs end to end (rc=0): 2,674 panel rows (math 12 years x 2 grades x 54 jurisdictions; reading 13 x 2 x 53, no Puerto Rico), 560 accommodations-not-permitted rows, 7,308 TDW cells. The 2024 XLSX matches the 2024 PDF integers in all 39,570 parsed cells; the PDF lacks the math grade-8 SD-and/or-EL 2022/2024 page (540 XLSX cells, Table A-20 (Cont-5)). Findings so far: the 2024 appendix revises DC 2022 SD-and/or-EL cells versus the 2022 appendix (math g4 identified 26 -> 32.16); the 2019 appendix prints some 2009 cells differently from the 2024 appendix (up to 0.9 points, mostly "assessed"); TDW 2003 pages swap the labels of CO/CT, NE/NH and NV/NJ; TDW 2024 reading rows NY..SD and WI disagree with the report card; TDW 2002 reading runs about 0.7 points below the report card for SD.
- 2026-09-28 01:22 correction to the 00:40 entry: TDW values carry two decimals from 2005 on, not from 2011; 2002–2003 carry one decimal [DATA: naep_inclusion.csv].
- 2026-09-28 01:22 verification pass:
  - Every number in this file was recomputed from the derived CSVs with a scratch script, or read from validation_report.md.
  - Fixed two reporting defects in the TDW rows of the disagreement file. A report-card "#" was printed as 0 with abs_diff 0; it now prints "#", and abs_diff is the TDW value's distance above 0.5.
  - The coverage legend now says its counts include "#".
  - Reran twice: rc 0, byte-identical outputs, and the panel CSV unchanged.
  - Checked the TDW 2000 tables (combined SD-or-LEP only) and the NCES inclusion pages for the policy date.
