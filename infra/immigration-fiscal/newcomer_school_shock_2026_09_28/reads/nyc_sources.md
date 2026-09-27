**Verdict:** New York City has a public school × year panel for exposure, staffing, spending, class size and
grade 3–8 results of never-ELL students for 2017-18 to 2025-26. There is no published school-level newcomer
head count for every year. The ELL count in the demographic snapshot is the full-coverage series; two allocation
memos give shelter-routed counts for July–October 2022 (SAM 65) and July 2023–February 2024 (SAM 90, weighted).
School spending has a reporting break in 2023-24.

# NYC sources for the newcomer school-shock lane

All files were retrieved on 2026-09-28 JST by direct HTTP (`curl -L -A "Mozilla/5.0"`); sha256 values are pinned
in `build_nyc.py` (`PINS`) and `extract_nysed_src.py` (`PINS`). Raw files sit in `_cache/nyc/` (git-ignored).

## 1. Demographic snapshots (exposure: ELL counts, enrollment)

- `demographic-snapshot-2021-22-to-2025-26-public.xlsx`, from
  https://infohub.nyced.org/docs/default-source/default-document-library/demographic-snapshot-2021-22-to-2025-26-public.xlsx
  (linked from https://infohub.nyced.org/reports/students-and-schools/school-quality/information-and-data-overview).
  sha256 `d7759afa…fcb69f2`.
  - NOTES tab, verbatim: "Enrollment counts are based on the October 31 Audited Register for the 2022-23, 2023-24,
    2024-25, and 2025-26 school years. To account for the delay in the start of the school year, enrollment counts
    are based on the November 12 Audited Register for 2021-22."
  - "Data on students with disabilities, English Language Learners, students' povery status, and students'
    Economic Need Value are as of the June 30 for each school year except in 2025-26. Data on SWDs, ELLs, Poverty,
    and ENI in the 2025-26 school year are as of June 4, 2026." (sic, "povery")
  - School tab columns used: `DBN`, `Year`, `Total Enrollment`, `Grade 3` … `Grade 8`, `# Students with
    Disabilities`, `# English Language Learners`, `# Poverty`, `Economic Need Index`.
- `demographic-snapshot-2017-18-to-2021-22-opendata-c7ru-d68s.csv`, NYC Open Data dataset c7ru-d68s
  ("2017-18 - 2021-22 Demographic Snapshot"), https://data.cityofnewyork.us/api/views/c7ru-d68s/rows.csv?accessType=DOWNLOAD.
  sha256 `26106be9…57975545`. Same columns. For 2021-22, which both files carry, the build keeps the newer file;
  1,716 of 1,852 schools have identical enrollment and ELL counts in both (`derived/nyc_audit.json`).

## 2. Grade 3–8 results by ELL status (achievement)

- `school-ela-results-public.xlsx` (sha256 `5a8c419e…4b02b4ce18`) and `school-math-results-public.xlsx`
  (`fc119576…f255a6a`), from https://infohub.nyced.org/reports/academics/test-results ("ELA Test Results 2018 to
  2026 … School (Excel file)"). Tabs used: "ELA - All", "ELA - ELL", "Math - All", "Math - ELL". Columns:
  `DBN, School Name, Grade, Year, Category, Number Tested, Mean Scale Score, # Level 1 … % Level 3+4`.
  Categories in the ELL tab: `Current ELL`, `Ever ELL`, `Never ELL`.
- NOTES tab, verbatim:
  - "This report includes results for the New York State ELA, Math and Science exams for the years 2018-2026 as
    of August 3, 2026."
  - "In 2023, NYSED aligned the Math and ELA tests to new standards; therefore, results from 2022 and earlier
    should not be directly compared to results from 2023 and later."
  - "Because exams were cancelled in 2020 and voluntary in 2021 (~21% of eligible students took exams in 2021),
    no data for those years is included."
  - "Prior to 2025, students enrolled in NYC PS schools outside of their district of residence were considered
    out-of-district placement (OODP) testers and attributed separately. Beginning in 2025, these students are
    attributed to the schools they were enrolled in during the testing window."
  - "District 75 students are included in city-level results but excluded in all other files."
  - "Charter schools are not included."
  - "… groups with 5 or fewer tested students are suppressed with an “s”. In addition, groups with the next
    lowest number of tested students are suppressed when they could reveal, through addition or subtraction,
    the underlying numbers that have been redacted."
- NYSED definition (glossary, https://data.nysed.gov/glossary.php?report=ell): "Never ELLs — Students who have not
  been identified as ELLs in the current or any previous school year."
- Statewide scale-score SDs used to standardize come from the NYSED technical reports; see
  `reads/scale_sd_sources.md` and `derived/scale_sd.csv`. No 2026 report exists, so SD-unit models stop at 2025.

## 3. School Allocation Memoranda (shelter-routed newcomer counts, dedicated money, register relief)

Base: https://www.nycenet.edu/offices/finance_schools/budget/DSBPO/allocationmemo/ (listings `am_fy{YY}_*.htm`).

- **SAM 65, FY2023, "Project Open Arms Allocation"**, dated October 31, 2022, "Revised November 9, 2022":
  https://www.nycenet.edu/offices/finance_schools/budget/DSBPO/allocationmemo/fy22_23/fy23_docs/fy2023_sam065.htm
  - "Schools that have enrolled six or more Students in Temporary Housing (STH), which are first time entrants
    into NYC public schools) since July 2, 2022 will receive an allocation of $2,000 per student."
  - "As this is a temporary fund source, these funds cannot be used to hire full-time staff, and this funding
    will not be allocated next year."
  - "Traditionally, a school-by-school breakdown of funds would be posted alongside a School Allocation Memo. Due
    to privacy and security concerns for the students involved, we are not posting this information at this
    time."
  - The school table `FY2023_SAM065_T01.xlsx` is 404 on the live site. The Wayback Machine captured it on the
    day of posting: https://web.archive.org/web/20221031200713id_/https://www.nycenet.edu/offices/finance_schools/budget/DSBPO/allocationmemo/fy22_23/fy23_docs/FY2023_SAM065_T01.xlsx
    (CDX: `20221031200713 … application/vnd.openxmlformats-officedocument.spreadsheetml.sheet 200`). Saved as
    `sams/FY2023_SAM065_T01_wayback20221031.xlsx`, sha256 `76f3379e…fa86112`. "Table 1: School Allocation
    Summary", columns `DSL Central Team, DSL Field Team, DBN, School Name, Allocation`; 369 school rows summing to
    the table's "Total" of 11,702,000, which is 5,851 students at $2,000. The table holds dollar totals by
    school, no student records.
  - Cross-check: the NYC Comptroller (https://comptroller.nyc.gov/reports/students-from-families-seeking-asylum/,
    2022-11-09): "According to DOE, a total of 369 schools (out of the City's total of 1,588 public schools) are
    receiving a SAM 65 allocation, representing 5,851 students."
- **SAM 90, FY2024, "Increase in Students in Temporary Housing"**, March 7, 2024, `fy2024_sam090.htm`:
  "Schools that enrolled students in temporary housing who were first time admits in NYC Public Schools from July
  2023 through February 2024 will receive an allocation of approximately $50 per student with additional
  weighting for students newly enrolled in calendar year 2024." Table `FY2024_SAM090_T01.xlsx` (sha256
  `8bac2860…6cacb`): 1,255 schools, total 1,500,000. The smallest allocation is $600 (a floor). Every
  allocation is ≡ 0 or 45 mod 50 [CALCULATION: scratch check], consistent with $50 per 2023 admit and a heavier
  weight for 2024 admits [INFERENCE]; allocation/50 is therefore a weighted count, not a head count.
- **Title III Immigrant** (FY2023 SAM 84, FY2024 SAM 73, FY2025 SAM 81, FY2026 SAM 73), e.g. SAM 84: "immigrant
  students are defined as individuals who were not born in any U.S. state (this includes the District of Columbia
  and the Commonwealth of Puerto Rico); and have not been attending one or more schools in any one or more states
  for more than three full academic years". "Schools with sufficient numbers of immigrant students (as reported to
  NYSED) and meet a minimum threshold are eligible for this funding." Totals: $2.77m (134 schools, FY2023),
  $6.74m (597, FY2024), $4.77m (488, FY2025), $4.77m (471, FY2026) [DATA: tables, `derived/nyc_audit.json`].
  Not used as exposure (threshold-censored, formula unpublished).
- **Register relief** (FY2022 SAM 86, FY2023 SAM 85, FY2025 SAM 86, FY2026 SAM 85). FY2023 SAM 85: "this SAM
  allocates to schools with weighted register losses sufficient funding to restore 100% of the school's total
  weighted register loss. The register relief is funded by 100% of American Rescue Plan Act (ARPA) funds." …
  "Schools with weighted register increases will receive the full balance of their mid-year adjustment through
  the usual process." Totals: $323.7m to 1,210 schools (FY2022), $136.2m to 723 (FY2023), $161.3m to 828
  (FY2025), $261.7m to 1,065 (FY2026). The FY2024 listings carry no mid-year register-relief SAM; FY2024 SAM 44
  is an "ARPA Initial Allocation Hold Harmless FY 2024" (May 31, 2023).

## 4. NYSED report-card databases (spending, teachers)

- `SRC2019.zip`, `SRC2021.zip` … `SRC2025.zip` from https://data.nysed.gov/downloads.php
  (`/files/essa/{18-19,20-21,21-22,22-23,23-24,24-25}/SRC{Y}.zip`), 140–390 MB each; sha256 in
  `extract_nysed_src.py`. Read with mdbtools 1.0.1 (`mdb-export`).
- Tables: "Expenditures per Pupil" and "Inexperienced Teachers and Principals" ("Staff Qualifications" in
  SRC2019). ReadMe (SRC2024): "YEAR School Year (2023 for 2022-23; 2024 for 2023-24)"; "FEDERAL_EXP Federal
  expenditures"; "STATE_LOCAL_EXP State and local expenditures"; "FED_STATE_LOCAL_EXP Total federal and
  state/local expenditures"; "NUM_TEACH … Number of teachers as reported in the Student Information Repository
  System". Each release carries two school years; the build takes each year from the latest release. The 2019
  release has expenditures for 2018-19 only, so spending runs 2018-19 to 2024-25 and teachers 2017-18 to 2024-25.
- ENTITY_CD → DBN: `CC DD 0001 T SSS` → `DD` + borough(`CC`: 31 M, 32 X, 33 K, 34 Q, 35 R) + `SSS`; charters
  (`0086`) are dropped. 1,546 of 1,579 mapped DBNs are in the demographic snapshot; each mapped DBN has one entity
  code per year (the build raises otherwise).
- **Reporting break in 2023-24.** Citywide ("NYC CHANCELLOR'S OFFICE", 300000010000) spending per pupil is
  $30,185 (2022-23), $33,864 (2023-24), $35,496 (2024-25), up 12% into 2023-24. School-level spending rose 56% at
  the median school over the same year (ratio 2024/2023: p25 1.48, median 1.57, p75 1.65) [CALCULATION: scratch
  check on `derived/nyc_schools.csv`]. More citywide cost was attributed to schools from 2023-24; the ReadMe does
  not describe the change. Estimates use logs with year effects and a variant that lets the break load on
  2021-22 spending per pupil.

## 5. Class size and pupil-teacher ratio

- https://infohub.nyced.org/reports/government-reports/class-size-reports: school files for November 2018,
  February 2019, November 2019, February 2020, "prelim2022" (the page: "unaudited enrollment information … as of
  10/31/22"), February 2023 ("updated2023"), and November/February/June for 2023-24, 2024-25 and 2025-26. The
  2023-24 page: "beginning with the 2023-24 school year, NYCPS now reports on class sizes as of 6/15".
- NYC Open Data: "2017-2018 SCHOOL LEVEL CLASS SIZE REPORT" (2ic6-4hrf) and "2021 - 2022 Average Class Size by
  School" (sgr7-hhwp), the only public school files for those years. 2020-21 has none.
- Used: K-5 grade-level rows (`Grade Level` K–5; '01'–'05' in files from 2024-25), programs Gen Ed, ICT, G&T,
  ICT & G&T; average = students / classes. Self-contained special-education classes and multi-grade "Bridge"
  classes are excluded.

## Reproducibility

`extract_nysed_src.py` then `build_nyc.py`, then `analyze.py`. The double-run check is recorded in RESULT.md.
