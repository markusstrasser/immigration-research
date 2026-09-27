**Verdict:** Chicago panel built; two runs are byte-identical. The panel covers CPS schools (ISBE RCDTS 15-016-2990-25) by spring year, 2017–2025.

What the panel has:

- **Enrollment and EL counts:** every year (CPS 20th day and ISBE).
- **Spending:** ISBE site-based per-pupil spending, 2019–2025.
- **Teacher FTE:**
  - from CPS quarterly rosters, every year (Sep 30 and Mar 31);
  - from ISBE, only 2024–2025.
- **Newcomers per school:** only the FY2025 budget's post-20th-day adjustment for SY2023-24. It covers 497 district-run schools; 149 have more than zero, 3,250 students in all.
- **Non-EL grade 3–8 results:**
  - 2018, 2019 and 2021–2023: ISBE all-student counts minus EL counts, school level (exact or bounded);
  - 2025: published by CPS for grades 3–8 combined, on ISBE's new scale, which ISBE says must not be compared with 2024 or earlier;
  - 2017 and 2024: none.

What is never published at school level:

- a never-EL assessment subgroup;
- a pupil-teacher ratio.

# Chicago sources for the newcomer school-shock lane

Worker model: claude-opus-5-5 (Chicago data-acquisition worker).

- Owned paths: `_cache/chicago/`, `reads/chicago_sources.md`, `build_chicago.py`, `derived/chicago_*.csv`, `derived/chicago_audit.json`.
- Retrieval: every file was fetched on 2026-09-28 JST (2026-09-27 18:45–20:50 UTC) by direct HTTP with User-Agent `Mozilla/5.0`.
- Hashes: sha256 for every cached file is in the manifest at the end. The build re-checks the hashes of the 84 files it reads.
- Tags follow the repo convention: `[DATA:]` for a local file, `[SOURCE:]` for a URL or document, `[CALCULATION:]` for a script output, `[INFERENCE]` for my reading.

## Outputs

Run from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project --with python-calamine==0.8.2 \
    python3 infra/immigration-fiscal/newcomer_school_shock_2026_09_28/build_chicago.py
```

| File | Rows | Content |
|---|---|---|
| `derived/chicago_schools.csv` | 5,873 | ISBE school × spring year 2017–2025, plus `cps_only` rows for CPS IDs with no ISBE match |
| `derived/chicago_scores.csv` | 160,952 | Grade 3–8 ELA and math results, long format, one row per school × year × subject × group × grade × source |
| `derived/chicago_staff_quarterly.csv` | 19,829 | CPS position rosters summed by school department × snapshot, 36 snapshots |
| `derived/chicago_crosswalk.csv` | 5,873 | CPS School ID to ISBE RCDTS by year, with match status |
| `derived/chicago_audit.json` | — | Input hashes, row counts by year and source, suppressed-cell counts, all checks below |

Keys and conventions:

- `school_id` is the 15-character ISBE RCDTS without dashes, e.g. `150162990252964`.
- `cps_school_id` is the six-digit CPS School ID.
- `year` is the spring of the school year: 2017 = SY2016-17.
- A blank cell means not published or suppressed. `suppressed_fields` (schools file) and `suppressed` (scores file) mark suppression. Nothing is imputed.

`chicago_scores.csv` is 19.8 MB. It is a derived file, so it can be regenerated rather than committed if size matters.

## Coverage of the schools file (non-blank cells by spring year)

[CALCULATION: `derived/chicago_schools.csv`, counted after the final build]

| Field | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| rows | 666 | 660 | 657 | 652 | 649 | 647 | 648 | 647 | 647 | |
| enroll_total | 630 | 633 | 631 | 629 | 626 | 624 | 617 | 622 | 621 | ISBE |
| el_pct | 630 | 402 | 577 | 575 | 409 | 405 | 409 | 439 | 391 | ISBE (small counts suppressed) |
| el_n | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 439 | 391 | ISBE |
| cps20_enroll_total | 664 | 660 | 657 | 652 | 649 | 647 | 648 | 647 | 647 | CPS 20th day |
| cps20_el_n | 574 | 577 | 586 | 594 | 588 | 596 | 648 | 647 | 647 | CPS 20th day |
| former_el_n, never_el_n | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 338, 568 | ISBE |
| newcomer_n | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 497 | 0 | CPS FY2025 budget |
| stls_n (ISBE homeless count) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 401 | 389 | ISBE |
| homeless_pct | 630 | 344 | 567 | 556 | 284 | 377 | 348 | 401 | 389 | ISBE |
| ppe_total (and 6 more ppe_* fields) | 0 | 0 | 628 | 627 | 624 | 622 | 621 | 620 | 619 | ISBE SBER |
| teacher_fte, teacher_headcount | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 615 | 611 | ISBE |
| pupil_teacher_ratio (elem. and HS) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | ISBE column exists, always blank for schools |
| class_size_avg | 609 | 608 | 630 | 596 | 619 | 619 | 617 | 615 | 613 | ISBE |
| class_size_g3 … g8 | ~455 | ~455 | ~436 | ~427 | ~443 | ~448 | ~450 | ~440 | ~442 | ISBE |
| cps_teacher_fte_sep30 / mar31 | 548/554 | 552/554 | 551/551 | 548/549 | 547/548 | 548/547 | 549/551 | 552/550 | 550/550 | CPS rosters |
| cps_budget_* (8 fields) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 497 | CPS FY2025 budget |
| cps_network | 664 | 660 | 657 | 652 | 649 | 647 | 648 | 647 | 647 | CPS 20th day |
| cps_governance | 0 | 0 | 0 | 0 | 0 | 0 | 648 | 647 | 647 | CPS 20th day, published from SY2022-23 |

Further notes on the schools file:

- **Spending year.** ISBE per-pupil spending labelled report-card year Y refers to the school year ending in spring Y; see Resources.
- **Newcomer placement.**
  - `newcomer_n` sits on the 2024 rows because it counts SY2023-24 arrivals.
  - The FY2025 budget fields sit on the 2025 rows because they fund SY2024-25.
- **Staffing columns.** The roster columns count CPS employees only. At charter and contract schools they are not school staffing; filter on `cps_governance` or `cps_network`. The spring-2025 teacher-FTE rows by network class: 509 district schools hold 20,736 FTE, 23 Charter/Contract-network schools hold 0, and 18 Options schools hold 137 [CALCULATION].

## Exposure

### English learners

- **ISBE.** ISBE publishes `% Student Enrollment - EL` every year and `# Student Enrollment - EL` from 2024. The 2017 file names it "L.E.P. SCHOOL %".
- **CPS 20th-day counts.** CPS publishes a 20th-day EL count for every school in every year. The school counts sum exactly to the published district totals [CALCULATION: audit `cps20_lep_<year>`]:

  | Year | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
  |---|---|---|---|---|---|---|---|---|---|
  | EL | 66,204 | 67,834 | 69,282 | 69,012 | 63,313 | 69,268 | 72,029 | 79,833 | 88,807 |
  | Total | 381,349 | 371,382 | 361,314 | 355,156 | 340,658 | 330,411 | 322,106 | 323,251 | 325,305 |

- **CPS EL label.** The label is "Bilingual" in 2017–2023 and "State English Learners" in 2024–2025. In 2017–2020 the files carry the note: "The EL data set was updated on October 10, 2020 to align with the State's definition of EL."
- **Blank EL cells in 2017–2022.** In these years no school EL cell is 0; 51–90 schools per year show blank instead. The district total equals the sum of the non-blank cells, which is consistent with the blanks being zeros [INFERENCE]. The build leaves them blank.

### Newcomers

The only per-school newcomer count published is the FY2025 budget column "Adjustment for Schools With Increased Enrollment Due to Newcomer Students" [DATA: `cps_budget/fy2025_budgetoverview_district_management-schools.xlsx`, sheet Traditional].

Coverage:

- 499 rows cover district-run traditional schools.
- 497 rows match a SY2023-24 20th-day school by exact name, and every match also passes the K-12 enrollment check (budget "Fall 2023 20th Day Enrollment" = 20th-day Total − PE − PK).
- 2 rows are unmatched: DISNEY II ES & HS and OGDEN ES & HS, both with adjustment 0.
- 149 schools have an adjustment above 0; the adjustments sum to 3,250 [CALCULATION: audit `cps_budget_fy2025`].

What the adjustment is, in CPS's words:

- Budget overview sheet: "Includes Fall 2023 20th Day Enrollment, Fall 2023 20th Day Non-Cluster Enrollment, Adjustments for Schools With Increased Enrollment Due to Newcomer Students. Also includes the Enrollment Input for Teacher allocations, which is a total of the Fall 2023 20th Day Non-Cluster Enrollment and the Adjustment for Schools With Increased Enrollment Due to Newcomer Students."
- FY2025 Appendix B, district schools: "The enrollment used is FY24 20th day minus cluster students (since special education teachers are allocated for special education cluster classrooms) plus adjustments for enrollment growth driven by newcomer students that took place during the school year."
- Schools and Networks 2025 web page: "Throughout the 2023–24 school year, the District has also seen an increase in newcomer students after the 20th day. Schools with post-20th day increased enrollment due to newcomer arrivals will see additional adjustments in their FY2025 budgets to the Core Teacher Allocation and Needs-Based Flexible Funding areas."
- FY2026 overview (no adjustment that year): "Note that there is no adjustment made in FY2026 enrollment calculations for newcomer students, as was done in FY2025."
- FY2024 Appendix B (EL-growth money, no per-school list found): "In SY22-23, the District experienced significant growth in English Learner students, most of which occurred following the fall 20th day count used for initial FY2024 SBB allocations. To support schools that have experienced growth in English learners, the District has provided 86 schools with $8 million in funding as part of their initial budget."

Citywide counts, for context only; none is by school:

- **Chicago.gov, April 12, 2024:** "Since August 2022, Chicago Public Schools in partnership with the Chicago Teachers Union has enrolled 11,692 children who meet three newcomer criteria (i.e. Students in temporary living situations, entered after August 2022, home language is not English)." [SOURCE: https://www.chicago.gov/city/en/depts/mayor/press_room/press_releases/2024/april/april-new-arrival-updates.html; archived as `pages/chicagogov_april-new-arrival-updates-2024.html`]
- **Chalkbeat Chicago, April 18, 2024**, read through Exa search highlights and not archived [SOURCE: https://www.chalkbeat.org/chicago/2024/04/18/chicago-and-illinois-count-migrant-students-differently/]:
  - "Chicago Public Schools says the district is currently serving 8,900 students who arrived since August 2022". CPS identifies them with five criteria.
  - Under ISBE's Immigrant Education Program definition, "Chicago estimates roughly 17,000 students fit this definition".
  - English learners rose "from 76,000 to 88,000 over the last year students as of April 12".

### Temporary living situations (STLS) and homeless students

- **ISBE.** `% Student Enrollment - Homeless` is published every year and `# Student Enrollment - Homeless` from 2024; the latter is `stls_n`. ISBE definition (2025 business rules): "Homeless is defined as students who lack a fixed, regular, and adequate nighttime residence."
- **CPS.** The 2025 IAR file reports "STLS Students" and "Non-STLS Students" for grades 3–8 combined.

## Resources

### ISBE site-based per-pupil expenditure (SBER), 2019–2025

Columns: "$ Total Per-Pupil Expenditures - Subtotal / - Federal / - State/Local", "$ Site-level Per-Pupil Expenditures - Subtotal / - Federal / - State/Local", "$ District Centralized Per-Pupil Expenditure - Subtotal" and "# School Enrollment". The sheet is "Financial" in 2019 and "Finance" in 2020–2025.

Definitions (2025 glossary):

- "“Per-Pupil Expenditures for each School” is defined as the is the sum of per-pupil site-level and centralized expenses funded by federal and state/ local sources of funds."
- "“Per-Pupil Expenditures for each School, disaggregated by school expenses” is defined as the sum of per-pupil site-level expenses spent by each school using federal and state/ local sources of funds."

**Fiscal year.** The business rules quote ESSA: "for each local educational agency and each school in the State for the preceding fiscal year." The data set does not label the fiscal year. I tested it in schools whose enrollment changed by more than 10% between consecutive years. The SBER enrollment in report-card year Y is closer to same-year enrollment than to prior-year enrollment in 95–141 schools per year, against 1–20 closer to the prior year (ISBE and CPS 20th-day enrollments both tested). So report-card year Y spending is the school year ending in spring Y [CALCULATION: ad hoc check on `derived/chicago_schools.csv`, 2019–2025].

**Redaction** (2025 business rules):

- "No redaction rules are applied to any Financial metrics at the State, District, or School level except for per-pupil expenditure."
- "Any SBER Enrollment less than 10 should be redacted from Report Card display".

### ISBE teacher FTE, pupil-teacher ratio, class size

| Measure | Coverage | Definition or note (quoted where the glossary defines it) |
|---|---|---|
| "Total Teacher FTE" | Schools only in 2024–2025; district only before | "Teacher Full-Time Equivalent is the measure of the number of teachers weighted for full-time/part-time status and the length of time of the year they were employed." (2025 glossary) |
| "Pupil Teacher Ratio - Elementary" / "- High School" | Blank for every CPS school in every year | "Pupil-Teacher Ratio is the student enrollment for the school year, divided by the number of full-time equivalent classroom teachers in the district. Teachers classified as special education teachers are excluded." (2025 glossary) |
| "Avg Class Size - All Grades" and grades 3–8 | Every year | 2018 glossary: "Average Class Size is the average number of students in each class in a school as of the first school day in May." 2024 and 2025 glossaries: "... as of the last day of school." |

### CPS employee position rosters (quarterly, 2016-09-30 to 2025-06-30)

The CPS Employee Position Files page [SOURCE: https://www.cps.edu/about/finance/employee-position-files/; archived as `pages/cps_employee-position-files.html`] says:

- "Chicago Public Schools has posted the district's full Employee Position File—which lists the names, job, titles, departments, and salaries of all full-time CPS employees."
- "CPS made a change to the district's full Employee Position File starting June 30, 2023. Because compensation can vary based on the experience and qualifications of the employee who is filling the position, CPS is no longer listing compensation estimates for vacant positions."

The 36 cached files cover every quarter-end from 2016-09-30 to 2025-06-30. All 36 have one sheet with the same header row: "Pos #, Dept ID, Department, FTE, ClsIndc, Annual Salary, FTE Annual Salary, Annual Benefit Cost, JobCode, Job Title, Name".

Build method:

- **Row unit and vacancies.** One row is one position line. A blank "Name" is a vacancy. A real employee is named "Vacanti", so no name matching is used.
- **Teacher rule.** A teacher is a "Job Title" containing "teacher" and none of: assist, asst, aide, "dir,", director, chief, coord, manager, mgr, pathway, recruit, eval, leadership, teaching, residency, speech, retired, analyst.
- **Titles counted.** At mapped schools across all 36 snapshots [CALCULATION: audit `staff_teacher_titles_counted`], the counted titles are:
  - Regular Teacher 465,908 rows;
  - Special Education Teacher 154,491;
  - Bilingual Teacher 75,278;
  - Program Option Teacher 11,669;
  - International Bacl Teacher 7,270;
  - Part-Time Teacher 3,475;
  - smaller titles (Head, Lead, Librarian and others).
- **Excluded titles.** Teacher Assistant variants and "Teacher-Speech Pathologist" are excluded.
- **Duplicate position numbers.** 416–833 rows per file share a "Pos #" with another row. Almost all pairs are two named incumbents at FTE 1.0 in the same department and title, with different salaries. FTE sums count both; `n_rows_shared_pos` reports them per school.
- **Salary break.** Salary and benefit sums cover filled rows only. Before the 2023-06-30 file every vacant row carries a salary; from 2023-06-30 none does [CALCULATION: audit `staff_rosters`, `vacant_rows_with_salary`].
- **Mapping to schools.** "Dept ID" is mapped to a CPS School ID through the school-profile "Finance_ID", using the profile year nearest the snapshot:
  - Finance IDs shared by several schools (including "0") are dropped. That is 311–460 rows per snapshot.
  - Departments with no school profile (central offices and networks) are dropped. That is 5,728–9,043 rows per snapshot.
- **Mapping checks.**
  - 48 of 19,829 staff rows (9 departments) have a department name sharing no word with the mapped school's profile names. All nine are renames, e.g. "Louis Agassiz Elem" to TUBMAN, "Daniel Boone Elem" to MOSAIC, "George B McClellan School" to MIÑOSO.
  - Two Finance IDs map to different schools in different years (66011 and 66012, SAFE contract schools). Neither has a row in the staff file.
- **Agreement with ISBE teacher FTE.** Ratio of roster teacher FTE to ISBE "Total Teacher FTE", school by school [CALCULATION]:

  | Year | Snapshot | Schools | Median ratio | Within ±10% | Median, filled positions only | Filled within ±10% |
  |---|---|---|---|---|---|---|
  | 2024 | Sep 30 | 536 | 1.000 | 437 | 0.962 | 444 |
  | 2024 | Mar 31 | 534 | 1.000 | 424 | 0.964 | 420 |
  | 2025 | Sep 30 | 533 | 1.039 | 379 | 1.007 | 456 |
  | 2025 | Mar 31 | 533 | 1.050 | 353 | 1.013 | 436 |

- **District trend.** Mapped-school teacher FTE on Mar 31: 18,908 (2017), 18,657, 18,969, 19,238, 19,707, 19,686, 19,777, 20,257, 20,873 (2025) [CALCULATION].

### CPS FY2025 school budget (district-run traditional schools, for SY2024-25)

Fields used (sheet "Traditional"):

- "Fall 2023 20th Day Enrollment";
- "Fall 2023 20th Day Non-Cluster Enrollment";
- the newcomer adjustment;
- "Enrollment Input for Teacher Allocations (Non-Cluster + Newcomer Adjustment)";
- "Student : Teacher Ratio for Core Classroom Teachers (Unadjusted for Floor)", e.g. "24:1", stored as 24;
- "Core Classroom";
- "Bilingual Coordinators";
- "STLS Advocates".

The FY2025 Appendix B sets the elementary teacher ratios: "For ES with an OI of 30 or less, schools will receive one teacher for every 26 students. For an ES with an OI between 31 and 41, that ratio is lowered to one teacher for every 24 students. For an ES with an OI of 42 or above, that ratio is further lowered to one teacher for every 22 students."

**Fall true-up.** The Schools and Networks 2025 page describes one: "As in previous years, schools will receive additional funding if their enrollment on the 20th day of the new school year exceeds their FY2024 budget baseline enrollment." I did not find per-school true-up amounts and ran no dedicated search for them.

## Scores

### What each source gives (`source` column)

| source | Years | Grades | Groups | Measures | Denominator |
|---|---|---|---|---|---|
| `isbe_levels` | 2017–2019, 2021–2024 | 3, 4, 5, 6, 7, 8 | all, EL ("LEP" in 2017) | % in levels 1–5; `pct_proficient` = L4+L5 (method `L4+L5`) | ISBE, with the 95% rule in 2018–2019 |
| `isbe_parcc_sat_2018` | 2018 | 3–8 each, and "Grade 3-8" | all | "% Meets", "# Tested" (put in `n_denominator`), "# Proficient" | ISBE 2018 |
| `isbe_all_tests` | 2018, 2019, 2021–2025 | `school` (every test the school gives: IAR/DLM-AA in grades 3–8, SAT or ACT in high school); 2025 also "Grade 3 to 8" | all, EL | 2018–2023: # proficient, # tested, % proficient, participation %; 2024–2025: rates only | Valid scores; 95% rule in 2018–2019 |
| `isbe_iar_3_8` | 2018–2025 | 3-8 | all, EL | 2018–2023: IAR/PARCC participation counts and rates; 2024–2025: proficiency and participation rates | — |
| `isbe_iar_grade` | 2025 | 3, 4, 5, 6, 7, 8 | "Total", "EL" | proficiency rate, participation rate | New 4-level scale |
| `isbe_rc17_acct`, `isbe_rc17_all_tests` | 2017 | school | "ALL", "LEP" / all | % proficient, % taking tests | ISBE 2017 |
| `cps_iar_1524` | 2017–2019, 2021–2024 | 3–8 each, "Combined … Grades 3-8", "Algebra I Grade 7/8" (`test_name`) | all only (the file has no student groups) | # tested, mean scale score (single grades only), % in levels 1–5, % met or exceeded | "CPS data uses the number of students tested as the denominator for all years." |
| `cps_iar_2025` | 2025 | 3–8 each (all only); "3-8" for groups | all, EL, non_el, stls, non_stls | # tested, # at or above proficient, % in 4 levels | New 4-level scale |
| `derived_all_minus_el` | 2018, 2019, 2021–2023 | school | `non_el_derived` | See below | Tested counts |

No IAR mean scale scores are published by ISBE, or by CPS for 2025. CPS publishes them for single grades in 2017–2024: "Scale scores between test types cannot be combined, so no mean scale score can be computed for combined-grade averages."

### How non-EL is defined, exactly

ISBE publishes no non-EL, former-EL or never-EL assessment result for schools in any year from 2017 to 2025. I checked every header of the 2018–2025 data sets and the rc17 layout. The 2025 data set publishes enrollment only, as "# Student Enrollment - Former EL" and "# Student Enrollment - Never EL".

ISBE's student-group definitions (2025 business rules):

- "English Learners (EL) is defined as students who have been identified through a screening process as eligible for bilingual education and/or English as a second language (ESL) services, and who have not yet reached English Proficiency, as measured by ACCESS for ELLS, 2.0."
- "Former EL is defined as students who were English Learners and met the state reclassification criteria on ACCESS through high school graduation."
- "Never English Learners is defined as students who are not “English Learner” or “Former English Learner”."
- EL group data sources: "For all metrics, this student group is based on SIS data, ISBE EL Status Table and the SIS/vendor assessment corrections data."

ISBE's EL flag on test results (2022 business rules): "Race, Gender, first year in the US, grade, IDEA, Alternate indicator, EL indicator are typically derived from assessment correction records where available, and if no assessment correction record is available, then the SIS student demographic data from the exited student enrollment is used."

EL status definition (2020 business rules): "A student is considered an EL if in the previous year the student did not achieve proficiency on the state’s assessment of English language acquisition" and "Once an EL student achieves proficiency on the state’s assessment of English language acquisition they are recategorized as non-EL."

The derived group `non_el_derived` (2018, 2019, 2021–2023) is computed from ISBE counts at school level, all tests:

- `pct_proficient` = (all proficient − EL proficient) ÷ (all tested − EL tested) × 100.
- The counts come from "# ELA Proficiency" and "# ELA Proficiency - EL", and from "# ELA Student Participation" and "# ELA Participation - EL"; math works the same way. The 2018 file uses the 2018 headers.
- By ISBE's partition this group is Former EL + Never EL [INFERENCE].
- Where ISBE left the EL cells blank, `pct_proficient_min` and `pct_proficient_max` bound the rate over 0–9 EL tested (method `bounds_el_0_9`). The bound is valid because the smallest EL participation count ISBE published is exactly 10 in every one of these years [CALCULATION: audit `min_published_el_participation_<year>`].

| Year | Exact rows | Bounds rows |
|---|---|---|
| 2018 | 660 | 592 |
| 2019 | 674 | 570 |
| 2021 | 602 | 600 |
| 2022 | 709 | 523 |
| 2023 | 718 | 510 |

- **Caveat for 2022 only.** The first-year rule then excluded any first-year-in-US student from proficiency. From 2023 the rule applies only if "EL indicator must be “yes” for First Year in U.S. School to be “yes”". So in 2022 a first-year non-EL student would be in the tested count but not the proficient count [INFERENCE; expected to be few].

CPS 2025 "Non-EL Students" (category "English Learner Status") is not defined in the file beyond its label. EL tested + Non-EL tested = All tested in 684 of 684 school × subject cells, so non-EL there means every tested student not currently EL, former EL included [CALCULATION: audit `cps2025_el_plus_non_el_equals_all_tested`].

### Comparability breaks (verbatim)

- **2018–2019, ISBE rates and levels.** 2018 business rules: "If the number of students tested is less than 95% of the testing population, then the percent proficient is calculated as the number of students proficient divided by 95% of the testing population as defined by the denominator in the participation metric." The CPS file overview adds: "Starting in 2018, the ISBE report card calculated the percent of students in each performance level as the number of students in the level divided by either by the number of students who took the test OR 95 percent of all students who ISBE believes should have tested, whichever is larger. ... CPS data uses the number of students tested as the denominator for all years."
- **2020.** No test; there are no score rows.
- **2021.** "Note for 2021: The 95% rule will not be taken into account. Therefore, the calculation will use “Number of students with valid scores excluding all students with suppressed scores” as the denominator".
- **2022–2024.** "For IAR, SAT and DLM-AA, apply the “First Year in US” indicator first." In 2023 and 2024 the EL flag must also be "yes". The 95% measure became separate: "Federal (95% Rule) Proficiency Rate ELA All Tests Formula (only published when a student group or overall participation rate is less than 95%)". The build does not use that measure.
- **2025.** "Levels 3 and 4 are proficient for IAR (grades 3 through 8)." "Proficiency data from SY2025 and forward should NOT be compared in any form (visual, tabular, etc.) to SY2024 and previous years." "Participation data and SGP data from SY2025 should be compared in any form (visual, tabular, etc.) to previous years." The 2025 exclusion also uses the Immigrant file: "If according to Immigrant file first enrolled in U.S. School date is on or after April 30, where calendar year is equal to school year minus two (e.g. SY2025 minus 2 = calendar year 2023 = April 30, 2023) AND “EL” Indicator yes in either current school year or the prior school year, then exclude the students."

### ISBE and CPS per-grade agreement

Cells where both ISBE and CPS publish all five level percentages for the same school, grade and subject [CALCULATION: audit `isbe_vs_cps_grade_levels`]:

| Year | All five equal | Largest gap ≤ 1 pt | Gap > 1 pt |
|---|---|---|---|
| 2017 | 5,230 | 32 | 128 |
| 2018 | 4,553 | 144 | 678 |
| 2019 | 3,871 | 523 | 1,036 |
| 2021 | 3,910 | 76 | 577 |
| 2022 | 4,504 | 320 | 614 |
| 2023 | 4,867 | 156 | 427 |
| 2024 | 4,903 | 139 | 418 |

The 2018–2019 gaps are expected from the 95% denominators. For 2022–2024 I averaged, school by school, ISBE L4+L5 minus CPS L4+L5. The mean is between −0.04 and 0.00 points in each newcomer group (adjustment 0, 1–19, 20 or more, no budget row); the mean absolute gap is at most 0.09 points. So the two publishers' per-grade distributions do not diverge more in newcomer-receiving schools [CALCULATION: ad hoc check on `derived/chicago_scores.csv`]. The files do not say whether ISBE's per-grade level percentages apply the first-year exclusion.

### Suppression

**ISBE, 2017–2021.** No reporting-redaction rule appears in the 2017, 2018 or 2019 glossaries or in the 2018–2021 business rules. I searched for "redact", "suppress", "fewer than", "less than 10" and "less than or equal to 9". The only hit is the summative-designation rule: "a count of at least 20 students per indicator". In practice the smallest EL participation count published in 2018–2023 is 10, and cells below that are blank.

**ISBE, 2022–2023** (business rules): "For any metric where the count is less than or equal to 9, then no data will be displayed for that metric, regardless if the data is displayed as a count or percentage."

**ISBE, 2024–2025** (business rules):

- "*" marks redaction: "For a percentage metric, display “*” (on PDS) or “Redacted” (on IIRC) (both numerator and percentage) if the numerator is less than 10 and the denominator exists."
- "For IAR, SAT, DLM, and ISA, proficiency rates are only redacted based on the denominator." (2024)
- Complementary suppression: "The second-lowest nonzero value of the subset will also be redacted to protect student privacy. ... This applies to EL status indicators: EL, Former EL and Never EL." (2025)

**CPS 2015–2024 IAR/PARCC file.** No rule is stated; small cells are blank.

**CPS 2025 file.** "Rows with <10 students in the denominator will not have data reported." The note text is "Data not reported because there are fewer than 10 students in this group."

**In the scores file.** `suppressed = 1` when any cell in the row was "*" or carried the CPS note. Counts by year and source are in audit `score_rows_flagged_suppressed`.

## Crosswalk: CPS School ID to ISBE RCDTS

- **Source.** The Chicago Data Portal progress-report files give each CPS School ID a "State_School_Report_Card_URL" containing `schoolid=<RCDTS>`.
- **Choice of mapping.** For each year the build picks the progress-report year nearest that year whose RCDTS exists in that year's ISBE file. A second pass re-points a CPS ID that shares an RCDTS to its next-nearest unclaimed RCDTS. This separates 14 CICS campuses that 2017 would otherwise put on network RCDTS …201C.
- **Result.** Attached per year: 629, 633, 631, 629, 626, 624, 623, 622, 621 (2017–2025). Every ISBE school row has a CPS ID except one in 2017. `cps_only` rows (23–36 per year) are CPS IDs with no ISBE school (Options, contract and virtual programs) [CALCULATION: audit `crosswalk_<year>`].

## Other checks in the audit

- **Totals.** CPS 20th-day EL-file totals equal the membership-file totals for every school and year.
- **2018 math EL participation column.** The 2018 header is mislabelled: there are two identical "Math Participation Total IEP Count" columns. The second one is used, and only after a check: EL proficient ÷ that column reproduces "Math Proficiency EL %" in 86.71% of 331 schools. The 2019 "% Math Participation - EL" header has the same fault and is not used.
- **Note rows.** CPS note rows are logged verbatim, for example: "NOTE: There were 449 students enrolled in the Virtual Academy, however they are all attributed to their brick and mortar schools." (SY2021-22)

## Sources

All pages linked below were retrieved on 2026-09-28 JST; file hashes are in the manifest.

### ISBE Report Card public data sets

Page: https://www.isbe.net/Pages/Illinois-State-Report-Card-Data.aspx (archived as `pages/isbe_illinois-state-report-card-data.html`). Each file is linked with the text shown.

| Link text | URL (`https://www.isbe.net` + path) | Cached as |
|---|---|---|
| "2025 Report Card Public Data Set" | `/_layouts/Download.aspx?SourceUrl=/Documents/2025-Report-Card-Public-Data-Set.xlsx` | `isbe/2025-Report-Card-Public-Data-Set.xlsx` |
| "2024 Report Card Public Data Set" | `…/Documents/24-RC-Pub-Data-Set.xlsx` | `isbe/24-RC-Pub-Data-Set.xlsx` |
| "2023 Report Card Public Data Set" | `…/Documents/23-RC-Pub-Data-Set.xlsx` | `isbe/23-RC-Pub-Data-Set.xlsx` |
| "2022 Report Card Public Data Set" | `…/Documents/2022-Report-Card-Public-Data-Set.xlsx` | `isbe/2022-Report-Card-Public-Data-Set.xlsx` |
| "2021 Report Card Public Data Set" | `…/Documents/2021-RC-Pub-Data-Set.xlsx` | `isbe/2021-RC-Pub-Data-Set.xlsx` |
| "2020 Report Card Public Data Set" | `…/Documents/2020-Report-Card-Public-Data-Set.xlsx` | `isbe/2020-Report-Card-Public-Data-Set.xlsx` |
| "2019 Report Card Public Data Set" | `…/Documents/2019-Report-Card-Public-Data-Set.xlsx` | `isbe/2019-Report-Card-Public-Data-Set.xlsx` |
| "2018 Report Card Public Data Set" | `…/Documents/Report-Card-Public-Data-Set.xlsx` | `isbe/Report-Card-Public-Data-Set.xlsx` |
| "2018 PARCC/SAT Proficiency Report" | `…/Documents/2018-PARCC-SAT-Proficient.xlsx` | `isbe/2018-PARCC-SAT-Proficient.xlsx`; its title row reads "PARCC and SAT Performance Results, 2017-2018" |
| "2016-2017 Report Card Data" | `/Documents/rc17.zip` | `isbe/rc17.zip` (member `rc17.txt`, semicolon-delimited) |
| "2016-2017 Report Card Data with Assessment Data" | `/Documents/rc17_assessment.zip` | `isbe/rc17_assessment.zip` (member `rc17_assessment.txt`) |
| "View the entire report card layout file in MS Excel format" | `…/Documents/RC17_layout.xlsx` | `isbe/RC17_layout.xlsx`; sheets "RC17" and "Assessment" give 1-based field numbers |
| "PARCC Performance Levels by District and School" | `…/Documents/rc17-parcc-performance-levels-district-school.xlsx` | cached, not used; duplicates rc17 levels |
| "2022 Report Card Additional Teacher Data Set" | `…/Documents/2022-Report-Card-Additional-Teacher-Data-Set.xlsx` | cached, not used; novice and emergency-credential teacher FTE |
| (glossaries 2017–2026) | `/Documents/<name>.pdf` | `isbe/*Glossary*.pdf` |

`PARCC_Meetexcced_subgroup.xlsx` and `rc-trend-data.xlsx` are cached but not used; they are state-level only.

Sheets and headers used:

- **2018–2025 data sets.** Sheets used: "General", "Financial"/"Finance", "ELA and Math" (2018), "ELA Math Science" (2019–2023), "ELAMathScience" (2024–2025), "PARCC" (2018) and "IAR" / "IAR (2)" (2019–2025).
- **Header text.** Exact header strings are in the build script constants `GENERAL_SPEC`, `FINANCE_COLS`, `ALLTESTS_*`, `IAR38` and `LEVEL_SPEC`. Examples:
  - "% ELA Proficiency - EL", "# ELA Participation - EL";
  - "% EL students IAR Mathematics Level 4 - Grade 7";
  - "IAR ELA Proficiency Rate Grade 5 - EL" (2025).
- **Row selection.** CPS school rows are those whose RCDTS starts `15016299025` with Type/Level "School".

### ISBE glossaries and business rules

Business rules ("Public Business Rules … Report Card Metrics") were fetched from `https://www.isbe.net/Documents/<file>`, listed on https://www.isbe.net/Pages/Report-Card-Metrics.aspx (archived as `pages/isbe_report-card-metrics.html`):

| Report year | File |
|---|---|
| 2018 | `RC-Metrics.pdf` |
| 2019 | `2019-Illinois-Report-Card-Metrics.pdf` |
| 2020 | `Public-Business-Rules-2020-Report-Card-Metrics.pdf` |
| 2021 | `Public-Bus-Rules-2021-RC-Metrics.pdf` |
| 2022 | `Public-Business-Rules-2022-Report-Card-Metrics.pdf` |
| 2023 | `Public-Business-Rules-2023-Report-Card-Metrics.pdf` |
| 2024 | `Public-Business-Rules-2024-Report-Card-Metrics.pdf` |
| 2025 | `Public-Business-Rules-2025-RC-Metrics.pdf` |

The quotes in this file were read from `pdftotext -layout` output of these PDFs. Two quotes not given above:

- 2017 glossary: "Limited-English-proficient students* are students who have been found to be eligible for bilingual education. The percentage of limited-English-proficient students is the count of limited-English-proficient students, divided by the total fall enrollment, multiplied by 100."
- 2025 business rules, revision 6.0 (August 18, 2025): "Added a note to all proficiency rate business rules regarding comparability of proficiency data, participation data, and SGP data from SY25 and forward."

### CPS 20th-day membership and EL files

The demographics page is https://www.cps.edu/about/district-data/demographics/ (archived as `pages/cps_district-data_demographics.html`). Its section title is "State English Learners, Students with IEPs, and Low Income Report". Files are fetched from `https://www.cps.edu/globalassets/cps-pages/about-cps/district-data/demographics/<file>`:

- EL files: `demographics_lepsped_{2017..2020}_10202020.xls`, `demographics_lepsped_2021_v10072020.xls`, `demographics_lepsped_2022_v10272021.xls`, `demographics_lepsped_20thday_2023.xlsx`, `demographics_lepiepfrm_20thday_sy2024_finalv2.xlsx`, `demographics_lepiepfrm_20thday_sy2025_final.xlsx`;
- membership files: `demographics_20thday_{2017,2018,2019,2020}.xls`, `demographics_20thday_2021_v10072020.xls`, `demographics_20thday_2022_v10272021.xls`, `demographics_20thday_2023.xlsx`, `demographics_20thday_sy2024_finalv2.xlsx`, `demographics_20thday_sy2025_final.xlsx`.

What the files contain:

- **Title rows.** For example, "20th Day 2016-2017 | Bilingual | SpED | Free/Reduced Lunch" and "20th Day 2024-2025 | State English Learners | Students with Disabilities | Economically Disadvantaged". The build checks that each EL file's "20th Day YYYY-YYYY" label matches its assigned year.
- **School-sheet headers (2025).** "School ID, School Name, Network, Governance, School Type, Community Area, Total, N, %, …". Before 2023 the headers are "Network, School ID, School Name, Total, N, %, …".
- **Notes (verbatim, 2017–2022 files).**
  - "Note: "Bilingual" refers to the state defintions of students who are English learners."
  - "Note: "Economically Disadvantaged Students" come from families whose income is within 185 percent of the federal poverty line. ..."

### CPS IAR/PARCC files

**2015–2024 file.** Page: https://www.cps.edu/about/district-data/metrics/assessment-reports/ (archived as `pages/cps_assessment-reports.html`). It links "IAR-PARCC Performance Levels and Sub-scores Report", "SL Report" = `https://www.cps.edu/globalassets/cps-pages/about-cps/district-data/metrics/assessment-reports/iar-parcc_2015to2024_schoollevel.xlsx` (the citywide file is cached, not used).

- Sheets: "IAR-PARCC ELA Results" and "IAR-PARCC Math Results".
- Headers: "School ID, School Name, Year, Test Name, # Students Tested, Overall ELA Mean Scale Score, % Did Not Meet, % Partially Met, % Approached, % Met, % Exceeded, % Met or Exceeded, …".
- The Overview sheet says:
  - "Data in this report from 2019 and later corresponds to the IAR assessment, and data from 2018 and earlier corresponds to the PARCC assessment."
  - "The state of Illinois has defined meeting proficiency in either subject (ELA or math) as achieving in either Level 4 (Met Expectations) or Level 5 (Exceeded Expectations)."
  - "All students with valid scores are included, including English Learners, students with IEPs, and students in charter and Options schools."

**2025 file.** The same page links "IAR Assessment Results", "CombinedSL/CW Report" to a Google Sheet titled "IAR Assessment Results - ISBE Levels Redefined 2025". It was downloaded from `https://drive.usercontent.google.com/download?id=1F05WJb2N4U4J8X9U7ha18U6wO-SFoiQD&export=download` and cached as `cps/IARProficiency_SY2025_Present.xlsx`.

- Sheet: "Data". Headers: "School Name, School Code, School Year, Test Name, Category, Student Group, %At or Above Proficient, %Above Proficient, %Proficient, %Approaching Proficient, %Below Proficient, #Tested, #At or Above Proficient, …, Notes".
- The Overview sheet says:
  - "Category … Reporting category: ALL, Economic Disadvantage, English Learner Status, Gender, IEP Status, Race/Ethnicity, Temporary Living Situation Status."
  - "%At or Above Proficient … The percent of tested students that were Above Proficient or Proficient, the two highest state performance levels."
  - "School Name … Note that Virtual Academy students test at their brick and mortar school."
- The file does not say whether first-year-in-US EL students are excluded.

### CPS budgets

Files are fetched from `https://www.cps.edu/globalassets/cps-pages/about-cps/finance/budget/budget-<FY>/docs/<file>` and linked from https://www.cps.edu/about/finance/budget/budget-2025/more-information-2025/ (archived; 2026 likewise):

- `fy2025_budgetoverview_district_management-schools.xlsx`: used; overview sheet "FY2025 School Budget Overview", "Updated 6/6/24 to reflect newly added Special Education positions at Traditional, Alternative, and Specialty Schools";
- `fy2025_budget_overview_charter_contract_alop_schools.xlsx`: not used;
- `fy2026-budget-overview-district-managed.xlsx` and `fy2026_budget_overview_charter_contract_alop_schools_.xlsx`: FY2026 = SY2025-26, outside the panel; not used;
- `fy2024_appendix_b.pdf`, `fy2025_b_appendix.pdf`, `fy2025_appendix_c.pdf` and `fy2026_appendix_b.pdf`: quoted;
- the Schools and Networks 2025 page (https://www.cps.edu/about/finance/budget/budget-2025/schools-and-networks-2025/), cached as `cps_budget/schools-and-networks-2025.html`: quoted.

FY2025 Appendix C: "For the fifth consecutive year, school budget allocations were based on the prior school year’s (SY2023–24) 20th day enrollment figures, rather than projected enrollment for the upcoming year."

### CPS employee position rosters

`https://www.cps.edu/globalassets/cps-pages/about-cps/finance/employee-position-files/<file>` for 36 files, `employeepositionroster_MMDDYYYY.xls` (some with a hyphen or a `-3` suffix, as linked). One file is xlsx content with an .xls name: `employeepositionroster_03312017.xls`. The build detects this from the content.

### Chicago Data Portal (CPS School ID links)

The build fetches `https://data.cityofchicago.org/api/views/<id>/rows.csv?accessType=DOWNLOAD`. Portal metadata JSON is archived in `pages/portal_views/`.

- **Progress reports** (School_ID to RCDTS link), by dataset ID:

  | School year | Dataset ID |
  |---|---|
  | SY1617 | cp7s-7gxg |
  | SY1718 | wkiz-8iya |
  | SY1819 | dw27-rash |
  | SY2122 | ngix-dc87 |
  | SY2223 | d7as-muwj |
  | SY2324 | 2dn2-x66j |
  | SY2425 | twrw-chuq |

  Portal description (SY2425): "2024-2025 school progress report ratings for all Chicago Public Schools, based on 2023-2024 data."
- **School profiles** (School_ID to Finance_ID), by dataset ID:

  | School year | Dataset ID |
  |---|---|
  | SY1617 | 8i6r-et8s |
  | SY1718 | w4qj-h7bg |
  | SY1819 | kh4r-387c |
  | SY2021 | 83yd-jxxw |
  | SY2122 | 2dem-8rq7 |
  | SY2223 | 9a5f-2r4p |
  | SY2324 | cu4u-b4d9 |
  | SY2425 | 3dhs-m3w4 |

  Portal description: "School profile information for all schools in the Chicago Public School district for the school year 2024-2025."
- **Not published:** no SY1920 progress-report or profile file was found. A catalog query for "SY1920" returned only school-location and attendance-boundary datasets. SY2021 has a profile file but no progress-report file.

## Not published, or not found (with the searches tried)

- **Per-school newcomer counts for 2022-23 to 2024-25 beyond the FY2025 budget adjustment.** Not found.
  - Exa searches:
    1. "Chicago Public Schools newcomer students enrollment by school data, migrant asylum-seeker children, which schools enrolled the most newcomers";
    2. `CPS "newcomer" students "11,692" three newcomer criteria`;
    3. "CPS FY2024 school budgets newcomer enrollment adjustment list of schools received additional teachers migrant students post-20th day";
    4. "Chicago Public Schools FY2025 budget enrollment adjustment for schools with increased enrollment due to newcomer students after 20th day".
  - Hits were citywide figures (Chicago.gov, Chalkbeat), a Chicago Council blog citing an internal CPS "Newcomer Support" update, a City Council hearing deck, the FY2024–FY2026 budget books, and the per-school "Staffing and School Resourcing" pages. Those pages repeat the FY2025 budget fields, e.g. https://www.cps.edu/schools/profiles/district-investments/staffing-and-school-resourcing/610191.
  - A school-level immigrant-student (ISBE Immigrant Education Program) count is not in any ISBE public data set I read.
- **FY2024 per-school budgets, including the 86 schools that received the $8 million EL-growth funding.** Not found.
  - Six guessed file names under `budget-2024/docs/` (e.g. `fy2024_budgetoverview_district_management-schools.xlsx`) return HTTP 404.
  - The FY2023 and FY2024 budget pages link only PDFs and the "Interactive Reports" portal (biportal.cps.edu, Oracle BI). A direct request to that portal returned "Request Rejected".
- **School-level non-EL or never-EL results for 2017 and 2024.** Not published.
  - No such column is in the rc17 layout or the 2024 data set, and 2024 dropped the counts that allow all-minus-EL. The CPS 2015–2024 file has no student groups.
  - Exa searches:
    1. "Chicago Public Schools IAR school-level results by student group English Learner Status "Non-EL Students" spreadsheet";
    2. "ISBE 2024 Illinois Assessment of Readiness school-level results by student group English learner data file download (number tested, number proficient)".
  - Neither returned a file.
  - The CPS assessment page offers student groups only in the 2025 file.
- **School-level pupil-teacher ratio.** The ISBE columns exist but are blank for every CPS school, 2018–2025. Use roster or ISBE teacher FTE with enrollment.
- **ISBE school teacher FTE, 2017–2023.** Blank; the rosters fill this.
- **Mean scale scores.** Published only by CPS, single grades, 2017–2024.
- **Per-school fall 20th-day budget true-ups.** Not located; no dedicated search.
- **Available but outside this panel (not built):**
  - SY2025-26 data: CPS 20th-day files (`demographics_lepiepfrm_20thday_sy2026_forweb.xlsx`), rosters through June 30, 2026, and the FY2026 budget;
  - ISBE school "ELA/Math Growth Percentile - Total" and "- EL" for 2019 and 2021–2025. ISBE says SY2025 SGP is comparable to earlier years; SGP exists for all and EL students only, not non-EL.

## Reproducibility check

On 2026-09-28 JST the final script was run twice from the repository root; both runs exited 0. The outputs are byte-identical across the runs:

- `build_chicago.py` sha256 `8af0a3acb785d9a9479d8426ab2b8513b5bd471b8c2930e7275cd94d9a7c65d9`;
- python-calamine 0.8.2;
- about 40 s per run.

| File | sha256 (both runs) |
|---|---|
| `derived/chicago_audit.json` | `1f3fe1c72e6f1afd74619b527fbd5d42008735757f78500551a346b32ecab708` |
| `derived/chicago_crosswalk.csv` | `d42035df38a4fd2ef54e985ac41019c8414d58ae82e840dde4bf5cb4e1754dfa` |
| `derived/chicago_schools.csv` | `f420889d032ddad8bac45a07d34901cb69ef860ac90e28b0c17e966ecfef4753` |
| `derived/chicago_scores.csv` | `1cae3fd1c112de62716d7001431eeac229f6769491fe3a6db057febca0d0082c` |
| `derived/chicago_staff_quarterly.csv` | `cb7c422e81c71122036471dbd76cbcacd73d068a5af8bd197a75142e0f4df0a2` |

## Appendix: cache manifest (`_cache/chicago/`, 138 files, 576.7 MB)

The largest file is `isbe/24-RC-Pub-Data-Set.xlsx` at 55.6 MB. The total is under the 10 GB stop and no file is near 2 GB.

| Path | Bytes | sha256 |
|---|---|---|
| `cps_budget/fy2024_appendix_b.pdf` | 198464 | `8770fa51ffb699c863bef94107266c709dc5f346337aa3acda9d015caeb1253b` |
| `cps_budget/fy2025_appendix_c.pdf` | 58708 | `905b64911f262d251780a5fe8c4a2c6e207b730e3d13a867ee0cc5ff5060f627` |
| `cps_budget/fy2025_b_appendix.pdf` | 180462 | `4c1a42b559b65ad65cc8c1baef01fd845da0a05d69ee5d5ce7777d6e787cf1eb` |
| `cps_budget/fy2025_budget_overview_charter_contract_alop_schools.xlsx` | 1274561 | `5d9bc2ab9cdceff726d48c5134482f447a5d231ea44ec3b076f937b279a0bab9` |
| `cps_budget/fy2025_budgetoverview_district_management-schools.xlsx` | 1574612 | `699763c4390b82263f2636cd462d6dfbd895c24b30d665daf4845fb892f5448d` |
| `cps_budget/fy2026_appendix_b.pdf` | 463522 | `ebb9d37881cb59e44e988cc343af41bfafbd6949320e0f7acc414a430ea6b2c9` |
| `cps_budget/fy2026_budget_overview_charter_contract_alop_schools_.xlsx` | 1396441 | `1c012258384c86eb85aa9c4465576129e8e2a46bb2ea8e7c5b2ebce9ba0d3c88` |
| `cps_budget/fy2026-budget-overview-district-managed.xlsx` | 1569477 | `2d4bafd9dc0d1c31fe499d0002f7f671480cff13f10e61bf552c22965deb5e82` |
| `cps_budget/schools-and-networks-2025.html` | 441191 | `191984c38647fb9690e81545d0b7a3ce2d487769be2bf8f713c64a51090d14c4` |
| `cps_positions/employeepositionroster_03312017.xls` | 2907610 | `f5b65be97369149c0bb8a95669b1aab2423a3030d0d05992cdf2f6005a384101` |
| `cps_positions/employeepositionroster_03312018.xls` | 7387648 | `991b5875e244d476a3cdc9b96c54612952ba389d77820b8ff0f5292598333521` |
| `cps_positions/employeepositionroster_03312019.xls` | 7557632 | `9475c517e98913408b020717d1729a5ce9c2fa816fe6797caf94c60424bc1a10` |
| `cps_positions/employeepositionroster_03312020.xls` | 7841280 | `58c2555c82ccb5f82518f6234ac67004a3fbebbe9f4c0ef9649f5599438fafcd` |
| `cps_positions/employeepositionroster_03312021.xls` | 8103424 | `082fe38b2602caeaccdc57652835427608dd59960b7ca3e8b1f14ea84cbe79af` |
| `cps_positions/employeepositionroster_03312023.xls` | 8688128 | `5fe536390c4682bd5895a785dcfdda94a93cb8335b14bf4063a7d7c7e47b6c59` |
| `cps_positions/employeepositionroster_03312024.xls` | 9105920 | `ebb5f7af990c07eb93e6254720d5d6d4704a850f1504a3c06842346ec2d3af47` |
| `cps_positions/employeepositionroster_03312025.xls` | 9295872 | `cec6874c03d6d5a1c4eba82eeed901cb94f9a7359af3db37d00c2ce580d8292c` |
| `cps_positions/employeepositionroster_06302017.xls` | 7393792 | `ad0a6487b32a9b907db29b454a613a40a411b5e2775675e96f7bc727789d06f3` |
| `cps_positions/employeepositionroster_06302018.xls` | 7332352 | `fd9424e6eea67a684114dce8637aba5a13f043b81c869fca6d18b075f46f52f7` |
| `cps_positions/employeepositionroster_06302019.xls` | 7524352 | `db146f785e43294ce41469a60390c903e85a3d8282d09e837aa249caed2f10f5` |
| `cps_positions/employeepositionroster_06302020.xls` | 7780864 | `947e0514057aa28efe05d68c3c4f1e49eac626bcbb00276d6a9eb59279a99913` |
| `cps_positions/employeepositionroster_06302023.xls` | 8688128 | `6bb3cf77d4a6a897c59b4f3a4fed780875152f6d52b2a968201c97491a5ec6a7` |
| `cps_positions/employeepositionroster_06302024.xls` | 9035264 | `ac3ffa67fadbe708c6187635649a59b927f12c74ed243f3c989ee24d1bdf696a` |
| `cps_positions/employeepositionroster_06302025.xls` | 9264640 | `35b20ca983aed3784df7d7b9c5313748795ed1a8247e09d59912a939e90e4aaf` |
| `cps_positions/employeepositionroster_09302016.xls` | 7484416 | `f202cd333bf5c9b8aafc56919060f7ad63634c9a1c4489268e65ed4225707b77` |
| `cps_positions/employeepositionroster_09302017.xls` | 7311872 | `7e71d3fa54e7611e52a89d37d1fa82075d4d8bb0ea8318658be30005c391ba96` |
| `cps_positions/employeepositionroster_09302018.xls` | 7479296 | `8addc9f9172fb51706fca04c89124df145e661fe48ba1f331c8ea0a59cdc7225` |
| `cps_positions/employeepositionroster_09302019.xls` | 7699456 | `941eab19b079122171d0a696ed053278fbd564da24f3d753e18ac45f7e74a834` |
| `cps_positions/employeepositionroster_09302020.xls` | 7877632 | `bba6f9454c8b24d41b417e2f18bcc82a1a37bd16f9a12eebae496f5d9ee0c2ec` |
| `cps_positions/employeepositionroster_09302022.xls` | 8618496 | `0e97afa65ad6f00550e0597366b3818d31ffb947a9c7c861a2e56a1c4c80df4d` |
| `cps_positions/employeepositionroster_09302024.xls` | 9203712 | `36c4515c418e533323d5239fb14e5012ba16c88619077aea4ec0a7b38ac53aca` |
| `cps_positions/employeepositionroster_12312016.xls` | 6846464 | `a61d70e16e2679f0a6eb38a7f20751cdbb21bcd2e14e1811c0553204f0734545` |
| `cps_positions/employeepositionroster_12312017.xls` | 7332864 | `da3f9a661fb4041fc68b6cb2bf1a454497af126b720c3541d1c2bda254ee7a7e` |
| `cps_positions/employeepositionroster_12312018.xls` | 7525376 | `d3ac7858c0d0026d92c39cb7002688663a390f8d9d726a80e9c37c7b82ddf804` |
| `cps_positions/employeepositionroster_12312019.xls` | 7773184 | `b00cc154999ef750bb79e40800db30e9b209e90fe4f12851539c4de415e3b9c4` |
| `cps_positions/employeepositionroster_12312020.xls` | 8013312 | `e9447c5caeb1ee81245226ae21295c7b4ccc7267098ddf721a54777f693d6fc8` |
| `cps_positions/employeepositionroster_12312023-3.xls` | 9030656 | `9a37b55c76dceebe7e095f2877364c96382327b59193476fd9fea1554aed8c6f` |
| `cps_positions/employeepositionroster_12312024.xls` | 9243648 | `40b1d4bef5ff07b7e51c3f6f8d81cb34156aae09bbb35583670d3d6c2c94a0c3` |
| `cps_positions/employeepositionroster-03312022.xls` | 8430592 | `31877b2ab5066098450d5eda134a09973f07ab0d9f83b723c07d90b0db36baba` |
| `cps_positions/employeepositionroster-06302021.xls` | 8071168 | `b8a44f77161aa92c71bd3db8ca94fbd32e4dade80903057be42e1a084d3c3cbc` |
| `cps_positions/employeepositionroster-06302022.xls` | 8370176 | `3998411d01ee4b6479dd88521bb57f773f3cd9d1e7da05b60a107addd69798a3` |
| `cps_positions/employeepositionroster-09302021.xls` | 8330240 | `baea346eb0a7ab6d9869e056ba511ed854f92de5f3a8b9c208b116aa6dcb69da` |
| `cps_positions/employeepositionroster-09302023.xls` | 8948224 | `cefaf7861936ac50421b7d28c8d180a00a5846b6c769d1a832ad6679aafa8504` |
| `cps_positions/employeepositionroster-12312021.xls` | 8391168 | `cbc41a3406050449f1a9ec01b5fb5d2cafdb05d7361d97ce77ec496506d2df20` |
| `cps_positions/employeepositionroster-12312022.xls` | 8659968 | `8da4fa4757ad6305a5d6f7d20e9bbc91761ecaf8e2571dada23e3464cb5dc6b9` |
| `cps/demographics_20thday_2017.xls` | 169472 | `50181007abfaff44e01ae62bf428b224ebbd868f631481ce195a5be470a17f61` |
| `cps/demographics_20thday_2018.xls` | 175104 | `16dca1ee8e02f7deacb41626824de9e8771deee73da4d74048171ca22578115a` |
| `cps/demographics_20thday_2019.xls` | 171008 | `97d3f8e82b129d6a3b9efbf50b2a990caed4488ce518b67517398f478d36cbe7` |
| `cps/demographics_20thday_2020.xls` | 170496 | `819d936700e8a715ecf657d679fd1454e609e294fdc3fd39acdca7340fe95a0d` |
| `cps/demographics_20thday_2021_v10072020.xls` | 154112 | `dffbf2f119ca6a0e994d214e385c592c19e1f6d086ee9298e69107dc35c251b4` |
| `cps/demographics_20thday_2022_v10272021.xls` | 154112 | `b8fb0656fce2f77dafb3c1d62a8885d640bf75d547ba548120c7901165b309f3` |
| `cps/demographics_20thday_2023.xlsx` | 104826 | `3b947ec63ef7eda2db8210f77cbf88b7670f5d28be46f39063efd6068dce7f5f` |
| `cps/demographics_20thday_sy2024_finalv2.xlsx` | 107138 | `5bdbc38edaf2e6c1570fa8dea072336accb4447adde09c00f7382fe0692ff487` |
| `cps/demographics_20thday_sy2025_final.xlsx` | 82500 | `32da3946bc2d850f4b53dd1fbcb0fab10c19dc5c44de2d82f5a69c729905ee44` |
| `cps/demographics_lepiepfrm_20thday_sy2024_finalv2.xlsx` | 137538 | `ac07bdae4c533fe2da65b4ba23a5f2ec389d152bfe40e921b5e156ce05009b97` |
| `cps/demographics_lepiepfrm_20thday_sy2025_final.xlsx` | 86530 | `8bd115ea4926d8c1e54d5954e945ba9fd533ab9d359740d1279b6975f9a98fb8` |
| `cps/demographics_lepsped_2017_10202020.xls` | 185856 | `71633a0c83a8b19439149fb525035de4b32932146b959c9c7675d38cd2e9b731` |
| `cps/demographics_lepsped_2018_10202020.xls` | 190976 | `57ff89643e5ec0c449f65993073e484882965e61b0a18d47394838c9029bf69d` |
| `cps/demographics_lepsped_2019_10202020.xls` | 196096 | `aba97d30f7bf98de15763eb1ffe836e657f6a6a59ed7f09c1bac303998628804` |
| `cps/demographics_lepsped_2020_10202020.xls` | 195072 | `a2b021b670b633c783046b54b2696e7d764067f519cc66a63a7b76c1e337c7bd` |
| `cps/demographics_lepsped_2021_v10072020.xls` | 178176 | `1203bc30449ef6e5cc0ca400a22af0f8de2edcc368c47a21569d2de57161c9bd` |
| `cps/demographics_lepsped_2022_v10272021.xls` | 179200 | `1fed1b93e0dd3ff52c9625a4dbb1da1c0dcd7d5c246ad2cfa8cb47f9fa818072` |
| `cps/demographics_lepsped_20thday_2023.xlsx` | 198810 | `5c868580ff1de19da1e31337dd8f2353f4c1bf81c2fbd8f87dda50f997ff2200` |
| `cps/iar-parcc_2015to2024_citywide.xlsx` | 792805 | `cbd20bdb323568a79ebc09f9092c5c133e13b065da092132e69448aafeebeef9` |
| `cps/iar-parcc_2015to2024_schoollevel.xlsx` | 9331500 | `e4de9581e60a77f2e90395854e3cea309c9cc047554a3fac165b04d27609522d` |
| `cps/IARProficiency_SY2025_Present.xlsx` | 1616137 | `08c07253f49ef766f3c2a72f9eb6f7294d54a1cd2bd26f47a119d0fed51ceca1` |
| `isbe/2017_Report_Card_Glossary.pdf` | 270312 | `7e4921b95658793f0c4c7328599521d66443b2252bb12ca4ea0c706775bbd3b8` |
| `isbe/2018-PARCC-SAT-Proficient.xlsx` | 951840 | `2f2801889cbabb6c2e5c2c255d927bceaa480b43f3a82703985d5465577b615e` |
| `isbe/2019-Illinois-Report-Card-Metrics.pdf` | 1221667 | `c946b9b56d78a0146dbb2fbfa22189db48956989eebef50b1e43807d6a4ff36f` |
| `isbe/2019-Report-Card-Glossary-Terms.pdf` | 312886 | `bcb1c51af4ac628f7567c6bf9e619062e14891b0c16c06f34e3092421ce4f473` |
| `isbe/2019-Report-Card-Public-Data-Set.xlsx` | 20052694 | `071913dbc531560f24abadc80670d0a4728a33a225f9f959c9515b11429ae436` |
| `isbe/2020-Glossary-of-Terms.pdf` | 375908 | `9daaf224197af6b887f212150b2564c166fa9400ed0676ef0fb667863b364743` |
| `isbe/2020-Report-Card-Public-Data-Set.xlsx` | 5878968 | `14a38185fa41565acd2a52662cbd87d485cbb7396d37f7f8e16bd79b8d79a99b` |
| `isbe/2021-RC-Pub-Data-Set.xlsx` | 17527653 | `b0a1a4fcfa51514e7f5e15562d395367b1c36d27dd4abe2ae9b16119e4fd8864` |
| `isbe/2021-Report-Card-Glossary-Terms.pdf` | 391104 | `51fc05e51ae8073de5e573d602ef82945604fce09d3b80ecc31c7495c3ef3172` |
| `isbe/2022-Glossary-of-Terms.pdf` | 401321 | `32b924ea4d6f9f1eee126cfec0378c9d9351c866ba3f06d4dd33e3baa6037615` |
| `isbe/2022-Report-Card-Additional-Teacher-Data-Set.xlsx` | 417334 | `653892164356140a425859ca0cc4213bbff355c99484eb043d8c06df5fdf0539` |
| `isbe/2022-Report-Card-Public-Data-Set.xlsx` | 21161046 | `6575e1b5bfbb8a133c763d4b93273cc75749b9bfc8289420b2ef226318e08a1d` |
| `isbe/2023-RC-Glossary-Terms.pdf` | 504228 | `bade493be265897ceb6326d0947364de560d84255f39cbb107ce82662c1d531e` |
| `isbe/2024-RC-Glossary-Terms.pdf` | 472517 | `cd916314e56fb761c65de161a728b0379048f4ee2519d4f58f4c94902d7add96` |
| `isbe/2025-Report-Card-Glossary-of-Terms.pdf` | 466903 | `545a675589a864637874f27c4fd062fee75429f38f02bd74b2e4df48a11436d8` |
| `isbe/2025-Report-Card-Public-Data-Set.xlsx` | 40314938 | `459ac146b52bafe7ce79fd76a95a65daa68d0472cce5205fa777cde19fb58cdf` |
| `isbe/2026-RC-Glossary.pdf` | 502066 | `b2ed3be74f7687815e836af3e643ff4e2e0656142ff5640e08f3cd2434d5e703` |
| `isbe/23-RC-Pub-Data-Set.xlsx` | 23586246 | `951536d6f81cdfdebb75e41775d0d80cde37bdd81fe256a6f31e2e571b7088ba` |
| `isbe/24-RC-Pub-Data-Set.xlsx` | 55577890 | `bab4981cd42a5355cfa8a62515b8364b981ff5e2397f4521deb0061034befa29` |
| `isbe/PARCC_Meetexcced_subgroup.xlsx` | 39718 | `b72684cd28156ff55d88bb6604e72b66611fd1e3f81fce9148b39e3364076246` |
| `isbe/Public-Bus-Rules-2021-RC-Metrics.pdf` | 2098529 | `15e64fa6014c29812aa6e94b6268fcacad213ad5f20e20792c19086ead571666` |
| `isbe/Public-Business-Rules-2020-Report-Card-Metrics.pdf` | 1677569 | `d44a5c76f996823884244e81789710bd2c2f4541efd0e43239fdcd466d51f741` |
| `isbe/Public-Business-Rules-2022-Report-Card-Metrics.pdf` | 2446304 | `b04d1389828ce0c28243806fc7d9975f61f3cb7c92c1fb81c31c0c6eac285ae5` |
| `isbe/Public-Business-Rules-2023-Report-Card-Metrics.pdf` | 2616369 | `404314605101e4ec69a2871962465007a0ce69ec1c50488425f9b0d0754f8397` |
| `isbe/Public-Business-Rules-2024-Report-Card-Metrics.pdf` | 2634220 | `e935295270448709aef7915d94aec8cce109292b1845fe08ee664c7abbe46a35` |
| `isbe/Public-Business-Rules-2025-RC-Metrics.pdf` | 2538136 | `975d53755e506e18371f1f35535d0a1ed542b8f410581578bb7b547bf1ccbcc6` |
| `isbe/RC-Metrics.pdf` | 1049818 | `899a9fe67091b97365ca87adebf3ed587e2a3a3ebbe8bfdc9f34dd2614d7a70f` |
| `isbe/rc-trend-data.xlsx` | 49397 | `ee1aa22e1f48b162d595513188ef60e0fa5c68890999713b20f4ed95ff997fb3` |
| `isbe/rc17_assessment.zip` | 14960433 | `37f495b3a89721af9ee851f2bc87b3a13b0ad676f6a7595d6a5f7596827082bf` |
| `isbe/RC17_layout.xlsx` | 935689 | `1f13f3a0940aedb2121fc539ca82cb9648eb01323c34d279d3401a72b9e82a02` |
| `isbe/rc17-parcc-performance-levels-district-school.xlsx` | 1793343 | `c38bcd048e2c4eb96a489c1fc9f5c646db88a6f42e9fcf49f714aea51221c0c6` |
| `isbe/rc17.zip` | 2350427 | `637d707b53d4d2a57bd6a2af15d0da1259417c70fc3dad7739c4ea9cf6186d8e` |
| `isbe/Report-Card-Glossary.pdf` | 127714 | `9a4166ef21fe7c2bfefeaf744612996d85dffa0676e21e3edd1ca682a3525e98` |
| `isbe/Report-Card-Public-Data-Set.xlsx` | 14313603 | `35b96aa88033591d01eb220f363ebfec4582401abb6a6684d385a2528e2243ac` |
| `pages/chicagogov_april-new-arrival-updates-2024.html` | 48634 | `930bd670efb78e55f25a6ba7431df6ebe25ba025542ec6221397387786bfb6af` |
| `pages/cps_assessment-reports.html` | 402494 | `988c6befc38b7a8a4971a3c1df0376daea8a7ca569cbdd2d2e4aef7a881a99cc` |
| `pages/cps_budget-2025_more-information.html` | 390132 | `8b5b0274e47f6d2ecc704d970409af52d7134c8cbdfe5dd51a942a45686f67f7` |
| `pages/cps_budget-2026_more-information.html` | 388038 | `b6203867982295965d183c9e5fcc68198ea3aae1b2e1c784d84fe94b24a15cce` |
| `pages/cps_district-data_demographics.html` | 412471 | `643395a132719fc988b9a19294a2a152a2945efe482c802c86187cd6103c09be` |
| `pages/cps_employee-position-files.html` | 406524 | `da785c67db177127b9912cdb5f6fc33531bbf79957190964ae48b9ff272ca153` |
| `pages/isbe_illinois-state-report-card-data.html` | 200743 | `7f7fccd0572e5264313bdf8eb7241e715255156077a2339cfb19e3b8b342868f` |
| `pages/isbe_report-card-metrics.html` | 129069 | `e293f23b5638ad0f974a9957b72f873e1c50434ebbef6406ca1385a4bb1011fe` |
| `pages/portal_views/view_2dem-8rq7.json` | 144227 | `d10f3d0f2da499e72f1a750cfca5f4bb6bdc8adc63323dd4f0b9e6f9d7067de8` |
| `pages/portal_views/view_2dn2-x66j.json` | 152383 | `c523ed49ea43a911c2fda979381f8eeec5d08a9bcfb2331807205524be191f1f` |
| `pages/portal_views/view_3dhs-m3w4.json` | 147856 | `626afb8b9f5d44c862ff24553718dbba29e1a60968cc199a5c0e1ca557ef7f4b` |
| `pages/portal_views/view_83yd-jxxw.json` | 148433 | `67515ae8d79fd4dd135f1d02caba583f3dd244ef6211f234b2d1ec246efd9960` |
| `pages/portal_views/view_8i6r-et8s.json` | 150416 | `9af7f63172b82f82990983b8b601177ef9336ee0ffa13c22c2e718163d3472e1` |
| `pages/portal_views/view_9a5f-2r4p.json` | 147527 | `3f17cec6f4a49b4ecfcf654384af302d67525d3fb5e2e38a9e5eecbcb65731c5` |
| `pages/portal_views/view_cp7s-7gxg.json` | 238728 | `2123bb24bd27ecd3eaf1ad9a1002c0a41a826dfff238686bafbc9576c0c8ad98` |
| `pages/portal_views/view_cu4u-b4d9.json` | 150547 | `8db3a6c87e016f39ad044114140c1330ea19c3ba04d185bb2d77209ce79df594` |
| `pages/portal_views/view_d7as-muwj.json` | 152193 | `f755e98c4ba4e4273534b4b776e40d1cb8ad588268ea5c150fa2f7389a7d287d` |
| `pages/portal_views/view_dw27-rash.json` | 268299 | `3992d5e3fa31a68519f6ebc2d75da2546b587254cf4ede5386b2f3b9ed375769` |
| `pages/portal_views/view_kh4r-387c.json` | 152806 | `2632ac1565480621cb3303e1bf2e1ac8df5f7f7aaa10bf97c38c007f4485ff64` |
| `pages/portal_views/view_ngix-dc87.json` | 131227 | `87f1f5417bf07d96d5d57c056da5cf13efcc7b731bf1574998585b1f2fb3ea75` |
| `pages/portal_views/view_twrw-chuq.json` | 155266 | `1873193046f362063d21f04ddebc4825eff72268256aeb0f50e6d7aada6cb124` |
| `pages/portal_views/view_w4qj-h7bg.json` | 154927 | `2c22dea6d00b3a3eaffcf3ad61cc2449f22a799b68eacf50315d2d2f0e9d53d2` |
| `pages/portal_views/view_wkiz-8iya.json` | 248741 | `612773d936e17105cc725610a3f3da85528f462c883a40b29ddd4e484f5488f1` |
| `portal/profile_SY1617_8i6r-et8s.csv` | 1182222 | `e7f935ae3a0f8b98524344eb94ec1bf52a6273188d13152bb2249c9f29cb1e61` |
| `portal/profile_SY1718_w4qj-h7bg.csv` | 1182129 | `a35acde10ffe4aff2b8690d03c1f69d7718fd6270d99a0fc36548199cb6209c2` |
| `portal/profile_SY1819_kh4r-387c.csv` | 1197346 | `ad49e9675308bb80228504e2f8ca8737824db9f33f7e5eefa16fe54a238e8e6d` |
| `portal/profile_SY2021_83yd-jxxw.csv` | 1271451 | `2d839dc07c7cb0907a8f976a7909407be21ff8f25ef9e46c9b82e6f84265554c` |
| `portal/profile_SY2122_2dem-8rq7.csv` | 1270853 | `4eba01b3dcab2bbddf0bf5142bb8081af89417d47471ea4f6ae2d9a3396f6faf` |
| `portal/profile_SY2223_9a5f-2r4p.csv` | 1266224 | `02b46c306328150eed0c7c1210ab1198aec67e0adb4d0174ce94def9d0968b44` |
| `portal/profile_SY2324_cu4u-b4d9.csv` | 1417622 | `3e4bb31144d359fe32a4342e28a1c65ef50f55e586e8bf1da054668ae2697c1c` |
| `portal/profile_SY2425_3dhs-m3w4.csv` | 1300915 | `632e742e2ea8b21f6fe3cdd0a8f4a3b28b8488b688078ca015f9154acf9d7f91` |
| `portal/progress_SY1617_cp7s-7gxg.csv` | 2033525 | `fa1ec56389d837fafc558f843c64d75f7ec5f7d3bfa8e71408cd9bdbbdf25edc` |
| `portal/progress_SY1718_wkiz-8iya.csv` | 1971865 | `d1cee91c0362ccb9aace131f51b862e938baee8d4a823e67545759fb5eb81425` |
| `portal/progress_SY1819_dw27-rash.csv` | 1827329 | `6100523805793470029036097a1ec9d0ffac263925b04deff62f323b7fb7435b` |
| `portal/progress_SY2122_ngix-dc87.csv` | 1387970 | `00f1247ba5c43b558e25baba304062b4d24d832001fdeae9196ae8c4a6700068` |
| `portal/progress_SY2223_d7as-muwj.csv` | 1415457 | `7bf4e7086269f9d74e36bb1ae360ee1298549a5853ea155c68cd5632d91cd4e2` |
| `portal/progress_SY2324_2dn2-x66j.csv` | 1413211 | `c511d8d4a896c76654684fb6ad4f51550c56ef22e708906d94b6933b796e2276` |
| `portal/progress_SY2425_twrw-chuq.csv` | 1363991 | `ce4079c2dbbb60d0aa0e269f59c03cd0e4b8ecfe021762c7b9f4e01d9bcae270` |
