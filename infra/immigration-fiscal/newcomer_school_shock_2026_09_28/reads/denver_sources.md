claude-opus-5-5

**Verdict:** Denver (CDE district 0880) has a public school × year panel for exposure, staffing and achievement over spring 2017–2026, and for spending over FY2019–FY2025 only. By school and year CDE publishes October membership; English learners (NEP + LEP + FEP monitor years 1–2) in every year and NEP/LEP alone from 2024; "Immigrant" pupils (not born in a US state, at most 3 full years in US schools); homeless pupils; grade 3–8 enrolment; teacher FTE and pupil/teacher ratio; and ESSA per-pupil spending split site/central and federal/state-local. CMAS ELA and math are published by school × grade 3–8 × language-proficiency group, including "Not EL" and a never-EL group ("PHLOTE, NA, Not Reported", 2019 on), with test records, valid scores, mean scale score, SD (2019 on) and percent met/exceeded. There was no test in 2020 and only the required grades in 2021. Four fields are not published or could not be obtained: school-level newcomer counts (DPS reports district totals only), NEP and LEP separately in membership, class size, and DPS school budget allocations. Two measurement warnings:
- Percent met/exceeded is withheld in 30–53% of school "Not EL" grade 3–8 cells that have at least 16 valid scores, and the withheld cells score lower. Use the mean scale score.
- The central share of ESSA spending is one district-wide per-pupil amount. Only site-level spending varies across schools.

# Denver Public Schools (CDE district 0880): sources for the school × year panel

Worker: Denver data-acquisition worker for lane `newcomer_school_shock_2026_09_28` (parent: lane owner).
Owned paths: `_cache/denver/`, `reads/denver_sources.md`, `build_denver.py`, `derived/denver_*.csv`,
`derived/denver_audit.json`. Retrieval: 2026-09-27 18:52–19:58 UTC (2026-09-28 JST). Every file is listed
with its URL, byte count and sha256 in the appendix and in `_cache/denver/SOURCES.tsv`.

## 1. What the build produces

Run from the repository root (openpyxl comes from the repo `.venv`; in a fresh checkout drop `--no-project`
or add `--with openpyxl`):

```
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/newcomer_school_shock_2026_09_28/build_denver.py
```

- `build_denver.py` reads 63 files from `_cache/denver/`. Each is pinned by sha256 in `INPUTS`; a missing
  or changed file raises `[BLOCKED]`. Files carrying a school-year or fiscal-year column must match the
  expected spring year, or the build raises.
- `derived/denver_schools.csv`: 2,019 rows, one per school × spring year 2017–2026. The requested columns
  come first, in the requested order; published extras follow. The extras include immigrant, migrant,
  NEP/LEP-only EL, FEP-exited, grade 3–8 enrolment, the six ESSA components, the charter flag and
  source-presence flags.
- `derived/denver_scores.csv`: 68,857 rows, one per school × year × subject × group × grade. It keeps
  `group_label` and `grade_label` as published. Each suppressed cell is blank, with the marker in a
  `*_note` column.
- `derived/denver_audit.json`: input hashes, rows in and out, suppressed-cell counts by year × field ×
  marker, skipped CMAS rows, year labels, and tallies of the consistency checks in §6.

**Double-run check (2026-09-28 JST):** two consecutive runs exited with rc=0 and produced byte-identical
outputs. Both runs followed the last edit of `build_denver.py`. [CALCULATION: `shasum -a 256`]

| output | sha256 (run 1 = run 2) |
|---|---|
| `derived/denver_schools.csv` | `3fa4859e5835b001782549a7a9faf4c737e7d50bb5a3140895feee9e25efab17` |
| `derived/denver_scores.csv` | `9aa37ad365a26e3296e9574f26d36dba6fc19061ca47a1f235bdd5affd7f9d33` |
| `derived/denver_audit.json` | `edd8310fc2575af80b9336e5a4967a17869dc9d3a1d318d220cb8e6a324066cb` |

### Coverage: Denver school rows with a published (non-blank) value

[CALCULATION: `derived/denver_audit.json` → `rows_out.denver_schools_nonblank_by_year`]

| spring year | rows | enroll_total | el_n | el_neplep_n | fep_exited_n | immigrant_n | homeless_n | teacher_fte / ratio | ppe_total |
|---|---|---|---|---|---|---|---|---|---|
| 2017 | 203 | 203 | 200 | – | – | 121 | 91 | 203 | – |
| 2018 | 208 | 208 | 196 | – | – | 56 | 14 | 207 | – |
| 2019 | 206 | 206 | 203 | – | – | 148 | 102 | 205 | 206 |
| 2020 | 207 | 207 | 188 | – | – | 67 | 23 | 206 | 207 |
| 2021 | 204 | 204 | 201 | – | – | 158 | 102 | 204 | 204 |
| 2022 | 206 | 204 | 201 | – | – | 154 | 109 | 204 | 205 |
| 2023 | 202 | 202 | 200 | – | – | 156 | 63 | 202 | 202 |
| 2024 | 196 | 196 | 192 | 191 | – | 161 | 76 | 196 | 196 |
| 2025 | 197 | 197 | 194 | 194 | 78 | 173 | 65 | 197 | 197 |
| 2026 | 190 | 190 | 186 | 186 | 74 | 172 | 78 | 190 | – |

- The count columns miss schools because of suppression (§5). The 2018 and 2020 files suppress below 16,
  not below 4, so immigrant and homeless counts are sparse in those two years.
- In 2022, two schools appear only in the ESSA file: 0040 Ridge View Academy Charter School (membership 0)
  and 9803 Gilliam School.
- Always blank: `nep_n`, `lep_n`, `newcomer_n`, `class_size_avg` (see §7).

Denver sums of the published school cells [CALCULATION, lower bounds wherever cells are suppressed]:

| year | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|
| PK-12 membership | 91,132 | 91,822 | 92,039 | 92,143 | 89,061 | 88,889 | 87,864 | 88,235 | 90,450 | 89,210 |
| EL (NEP+LEP+FEP M1/M2) | 30,646 | 30,546 | 30,173 | 28,581 | 27,454 | 25,716 | 25,853 | 26,493 | 28,345 | 27,492 |
| Immigrant | 1,800 | 2,139 | 2,889 | 2,597 | 3,001 | 2,791 | 3,283 | 5,643 | 9,265 | 8,069 |
| Teacher FTE | 5,967.7 | 6,077.1 | 6,169.1 | 6,164.2 | 6,134.6 | 6,143.4 | 5,980.9 | 5,953.8 | 6,011.3 | 6,115.4 |

### Score granularity

- Grades: rows for grades "3"…"8" and for "All Grades", which becomes `3-8`. Exceptions:
  - 2017 has no "All Grades" rows.
  - 2018 math "All Grades" includes middle-school course-test takers, so it is labelled `3-8+courses`. It
    differs from the sum of grade rows in 6 of 367 checkable cells.
  - 2021 has only ELA grades 3/5/7 and math grades 4/6/8.
- Rows skipped [DATA: audit `cmas_skipped`]:
  - 2017 ELA grade 9: 252 rows;
  - math course tests: 458 rows in 2017 and 9 in 2018;
  - Colorado Spanish Language Arts (CSLA): 55 to 177 rows per year from 2021.
- Groups (`group` code ← published label):

| years | codes |
|---|---|
| 2017–2018 | `nep` ← "NEP - Non English Proficient", `lep` ← "LEP - Limited English Proficient", `fep` ← "FEP - Fluent English Proficient", `phlote_fell_na` ← "PHLOTE/FELL/NA", `unreported` ← "Unreported" (2017, one row) |
| 2019–2022 | `el` ← "English Learner (EL)", `not_el` ← "Not English Learner (Not EL)", `nep` ← "EL: NEP (Not English Proficient)", `lep` ← "EL: LEP (Limited English Proficient)", `fep_fell` ← "Not EL: FEP (Fluent English Proficient), FELL (Former English Language Learner)", `phlote_na_nr` ← "Not EL: PHLOTE, NA, Not Reported" |
| 2023–2026 | `el` ← "English Language Proficiency: (NEP/LEP)", `not_el` ← "English Language Proficiency: (Not NEP/LEP)", `nep` ← "NEP (Not English Proficient)", `lep` ← "LEP (Limited English Proficient)", `fep_fell` ← "FEP (Fluent English Proficient), FELL (Former English Language Learner)", `phlote_na_nr` ← "PHLOTE, NA, Not Reported" |
| all years | `all` ← overall file ("All Students") |

- Rows per year (both subjects, all grades) [DATA: audit]:

| year | rows |
|---|---|
| 2017 | all 1,004, nep 635, lep 969, fep 712, phlote_fell_na 1,004 |
| 2018 | all 1,346, nep 1,101, lep 1,297, fep 1,028, phlote_fell_na 1,346 |
| 2019 | all 1,354, el 1,322, not_el 1,352, nep 1,146, lep 1,302, fep_fell 1,020, phlote_na_nr 1,352 |
| 2021 | 524 in every group, except phlote_na_nr 522 |
| 2022–2026 | 1,358 / 1,350 / 1,300 / 1,308 / 1,242 in every group |

  From 2021 every group row is published even when empty. In 2017–2019 a group with no pupils has no row;
  the partition check in §6 supports reading an absent row as zero.

## 2. Definitions quoted from the sources, and what they imply

### Membership (Student October Count)

- Pupil membership archive page (`cde_page_pm_archives.html`): "The Student October Count is based on a
  one (1) day membership count in which districts are asked to report all students who are actively
  enrolled and attending classes through their district on that date."
- Same page: "Membership is defined as enrollment and attendance for a student. Students must be enrolled
  by count date (typically October 1st) or an alternate count date if used."
- Same page, on the program flags (IP/ST): "Services provided by schools and/or districts for students
  identified as belonging to one or more of the categories below at any point during that school year:"
- Consequence for timing: `year` 2024 counts pupils enrolled on about 1 October 2023. Arrivals after the
  count date enter membership only in the next October.
  - DPS reported district totals only: "As of October Count 2023, there were nearly 1,500 new arrival
    students enrolled in DPS" and "Since October Count 2023, an additional 3,200 students enrolled in DPS".
    [SOURCE: DPS Strategic Regional Analysis Spring 2024, go.boarddocs.com …/D5YTHN77796D/$file/SRA_Spring
    2024_Final.pdf, read as an Exa search excerpt on 2026-09-28 and not archived.]
  - Spring 2024 CMAS records therefore likely include many pupils who are absent from October 2023
    membership. [INFERENCE]

### English learner in membership (`el_n`, `el_pct`)

The definition is the same in every year: NEP + LEP + FEP monitor years 1–2. Each year-specific CDE page
states it:
- 2016-17 (`cde_page_pm_2016-17.html`): "Note: English Learner (EL) data in the Instructional Program
  report includes NEP, LEP, FEP Monitor Year 1 and FEP Monitor Year 2".
- 2017-18, 2018-19, 2019-20, 2020-21, 2021-22 and 2022-23 pages: "English Learner counts include students
  who are NEP, LEP, and FEP Monitor Year 1 and Monitor Year 2."
- 2023-24 page: the same sentence, followed by "(unless specified)."
- 2024-25 file header: 'EL Count Including FEP Monitor Year 1 and Year 2'.
- 2025-26 header: 'Multilingual Learner: NEP, LEP, FEP Monitor Year 1 and Monitor Year 2 Count'.

Current definition page (`cde_page_pm_archives.html`): "Multilingual Learner (also known as English
Learners) Students who have been identified as Non-English Proficient (NEP), Limited English Proficient
(LEP), or Fluent English Proficient Monitor Years 1 and 2 (FEP Monitor 1, FEP Monitor 2)."

- `el_neplep_n` (NEP + LEP only) is published from 2024:
  - 2024 and 2025: 'EL Count (NEP/LEP Only)', 'EL (NEP/LEP Only) Pct';
  - 2026: 'Multilingual Learner: NEP/LEP Only Count'.
- `fep_exited_n` is published from 2025: 'EL FEP Exited Year 1 and Year 2 Count'. It is not part of EL.
- NEP and LEP are never published separately in membership.
- Percentages are fractions (0.575 = 57.5%).

### Immigrant and homeless (IPST flags)

- Immigrant: "Students are an immigrant if their age is 3 through 21, were not born in any state and have
  not been attending one or more schools in any one or more states for more than 3 full academic years."
  (`cde_page_pm_archives.html`)
- `immigrant_n` is the only published school-level count that tracks newly arrived pupils. It is a stock
  of pupils in US schools for up to about three years, not a flow of new arrivals. [INFERENCE from the
  definition]
- Homeless: "According to the McKinney Act, a “homeless individual” lacks a fixed, regular, and adequate
  nighttime residence."
- Migrant (`migrant_n`) is the federal migrant-agricultural-worker program flag, not immigration, and is
  almost always suppressed in Denver.

### CMAS language-proficiency groups (who is in "Not EL")

- 2019 on, "Not EL" / "Not NEP/LEP" contains former and monitored ELs. The 2019–2022 labels nest "FEP …,
  FELL (Former English Language Learner)" inside Not EL. In every checkable school cell of 2019–2026, Not EL
  test records = FEP/FELL + PHLOTE/NA/Not Reported, and EL = NEP + LEP (§6).
- The student data file layout for 2026 (`cde_cmas_sdf_layout_2026.pdf`, field AD LanguageProficiency) lists
  the codes: "0 = Not Applicable; 1 = NEP - Non English Proficient; 2 = LEP - Limited English Proficient; 4 =
  PHLOTE - English Proficient; 5 = FELL - Former ELL; 6 = FEP - Monitor Year 1; 7 = FEP - Monitor Year 2; 8 =
  FEP - Exited Year 1; 9 = FEP - Exited Year 2; Blank". The field definition reads: "A student's English
  language proficiency is described by his or her ability to speak, listen, read, and write in English."
- The CMAS EL group is NEP + LEP only. FEP monitor years 1–2, which membership counts as EL, sit in CMAS
  "Not EL" (inside `fep_fell`). [INFERENCE from the labels and codes]
  - So `not_el` includes recently reclassified pupils.
  - `phlote_na_nr` ("PHLOTE, NA, Not Reported" = English-proficient other-home-language pupils, English
    background, and unreported) is the closest never-EL group.
  - It is consistent from 2019 through 2026.
- In 2017–2018, "PHLOTE/FELL/NA" includes FELL, so a never-EL series cannot run back before 2019 on the same
  definition. A 2017–2018 counterpart of "Not NEP/LEP" is FEP + PHLOTE/FELL/NA + Unreported (counts add;
  means need n-weighting).
- The summary-file layout (`cde_cmas_summary_layout_2026.pdf`) lists finer groups (043–053: NEP, LEP, NEP
  and LEP, Not NEP or LEP, PHLOTE, FELL, FEP monitor 1/2, FEP exited 1/2, English Background). The public
  school files publish only the six groups above.
- The summary-file definition of the base count, group 001 "Total Number of Students": "The number of
  students who should have been assessed." It excludes "Report Suppression Codes", expelled students at
  school level, and invalidation codes "01 = Took Other Assessment OR Duplicate Registration/Attempt", "03 =
  Withdrew Before/During Testing", "07 = Medical Exemption", "08 = Part Time Public and Part Time Home
  School". I read the public 'Number of Total Records' as this base. [INFERENCE]

### CSLA and grade 3–4 ELA

- Denver grade 3–4 pupils who take Colorado Spanish Language Arts are not in the ELA records. District rows
  of `cde_cmas_overall_2024.xlsx` [CALCULATION]:
  - grade 3: ELA 5,430 + CSLA 1,041 = 6,471 total records, against math 6,458;
  - grade 4: ELA 5,536 + CSLA 799 = 6,335, against math 6,328.
- Grade 3–4 ELA "all" and "EL" cells therefore exclude many Spanish-speaking ELs. Math cells include them.
- CSLA rows are not in `denver_scores.csv`; they are in the overall files if needed.

### Teacher FTE and pupil/teacher ratio

- Staff statistics page (`cde_page_staff_statistics.html`): "The Human Resource collection contains all
  general education staff information as of December 1."
- Staff archive page: "The average number of pupil-staff ratio is the average number of pupils per staff
  FTE."
- Same archive page, under 'Staff FTE (Full Time Equivalency)': "Calculated value based upon the job class
  code, hours per day and contract days reported in the Staff Assignment data file."
- Which job codes count as "teacher":
  - 2024 file, 'Key' sheet: "Job Codes included in Teacher FTE": 201 'Teacher, Regular', 202 'Teacher,
    Special Education', 204 'Teacher, Permanent Substitute', 206 'Teacher, Title 1'.
  - 2025 title: "2024-2025 Pupil Teacher Job Codes 201-206 Ratio by School". 2026: "2025-2026 Pupil Teacher
    (Job Codes 201-206) Ratio by School".
  - 2017–2023 files name no job codes.
  - Whether 203 and 205 entered in 2025 is not stated. Denver's summed teacher FTE shows no jump
    (5,953.8 in 2024, 6,011.3 in 2025). [CALCULATION]
- Published ratio = PK-12 count / teacher FTE in every row (§6):
  - unrounded decimals in 2017–2021;
  - an integer 'N:1' string from 2022, parsed to N (`ptr_ratio_form` records which).
- `ptr_calc` is the unrounded PK-12 count / FTE for all years [CALCULATION]. Use it for trends.

### ESSA per-pupil expenditures (`ppe_*`)

Methodology (`cde_ft_methodology_2026-07-14.docx`, "ESSA-Mandated Per Student Spending Breakdown"):
- "Federal Site-Level Expenditures: Site-Level Expenditures within federal grant codes between 4000 - 9999,
  less adjustments for impact aid, less community, capital outlay, debt services and flow-through activity
  divided by the per pupil membership for the school site."
- "State/Local Site-Level Expenditures: … within state/local grant codes between 0000 - 3999, plus
  adjustments for impact aid, …, divided by the per pupil membership for the school site."
- "Federal Site-Share of Central Expenditures: District-Level Expenditures within federal grant codes …
  divided by the per pupil membership for the district excluding charter schools." The State/Local
  site-share is defined the same way.
- "District-wide (central) Learning Environment and Operations expenditures (ie school code ‘0000’) are
  included in the total per-student spending for traditional schools to approximate full allocation of
  district spending to these schools. The central spending at the charter schools is coded directly to the
  relevant schools."
- "CDE has included all current expenditures in the per-pupil calculations, including those paid for using
  private contributions."

Consequences [CALCULATION on `denver_schools.csv`]:
- The central share is one amount per year for every district-run school, and 0 for charters:

| FY (spring year) | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|
| central share per pupil ($) | 5,153 | 4,890 | 5,238 | 5,869.82 | 8,085 | 7,962 | 7,488 |

  Across schools only `ppe_site_*` varies. Use the site-level series to test whether money followed pupils.
- 'Membership' in the ESSA file equals the October PK-12 count of the same school year in all 1,415 matched
  rows. So FY2024 per-pupil values divide 2023-24 spending by October 2023 membership. Mid-year arrivals
  would then raise spending without raising the divisor. [INFERENCE]
- `ppe_federal` and `ppe_state_local` = site + central share [CALCULATION]. They equal `ppe_total` within
  $2 in all 1,417 rows.
  - FY2019–20 leave 'Site Level - Federal' blank in 72 Denver rows (28 in 2019, 44 in 2020) where the
    published site total equals the site state/local amount.
  - There the build counts the blank as 0 in `ppe_federal` only; the published column stays blank.
- The charter flag ('C') is blank for every school in FY2023. Central share = 0 identifies the 56 charters
  that year. [INFERENCE]
- FY2021 file: the title row says "FY2021-2022 ESS Per-Pupil Expenditures", but every row's FISCAL_YEAR is
  '2020-2021'. I use the rows; the build asserts the year label.
- FY2022 central-share cells are unrounded floats (e.g. 5869.8191); the others are whole dollars.

### CMAS comparability notes

- 2021, from the file's "Interpretation Considerations": "Fewer students tested in 2021 and participation
  varied by group".
- 2023: "Based on the Colorado Academic Standards". 2024–2026 overall files: "Based on the 2020 Colorado
  Academic Standards".
- The 2024 file prints 2024, 2023 and 2019 percent met/exceeded side by side with a 'Change 2024-2023'
  column. No scale break is flagged in the files I read. [DATA]
- Percentages (percent met/exceeded, participation) are on a 0–100 scale in every year.

## 3. Year alignment

`year` = spring year of the school year:

| source | `year` 2024 means |
|---|---|
| October membership | Oct 2023 |
| December 1 staff snapshot | Dec 2023 |
| ESSA fiscal year | July 2023–June 2024 |
| CMAS | spring 2024 |

The build asserts the year labels where a file carries them:
- IPST 2018–2020 'School Year';
- PTR 2024–2026 'School Year';
- every ESSA file's fiscal-year column.

The remaining files carry the year only in their title row or file name (§8).

## 4. Group and field mapping to the requested schema

| requested | filled from | years |
|---|---|---|
| enroll_total | IPST 'PK-12 Count' / 'Total PK-12 Pupil Membership' / 'PK-12 Pupil Membership' | 2017–2026 |
| el_n, el_pct | IPST EL count and percent (NEP+LEP+FEP M1/M2) | 2017–2026 |
| nep_n, lep_n | not published by school (NEP+LEP combined in `el_neplep_n`) | blank |
| newcomer_n | not published by school (use `immigrant_n` as the proxy) | blank |
| homeless_n | IPST 'Homeless Count' | 2017–2026 |
| ppe_total | ESSA 'Total School Expenditures' | FY2019–FY2025 |
| ppe_federal, ppe_state_local | site + central share by source [CALCULATION] | FY2019–FY2025 |
| teacher_fte | PTR 'Teacher FTE' | 2017–2026 |
| pupil_teacher_ratio | PTR ratio as published (integer from 2022) | 2017–2026 |
| class_size_avg | not published by CDE at school level | blank |

## 5. Suppression rules

**Membership.** Only the 2025-26 workbook states a rule, in its IPST footer: "*suppressed due to small
counts". The current membership page says: "Note: Student counts are suppressed for Instructional Programs
and Free/Reduced Lunch to protect student privacy." The archive page says: "The methods for student data
privacy include focused N size suppression and overall total count suppression."

Observed statewide in the IPST files [CALCULATION: `scratchpad/denver/ipst_minpos.py`, all Colorado
schools]:
- The EL, immigrant and homeless counts are never published as 0.
- The smallest published value is 4 in 2017, 2019 and 2021–2026, so a blank there means 0–3.
- In 2018 and 2020 the smallest published value is 16, so a blank means 0–15.
- Markers: '*' in 2017 and 2021–2026; 'N/A' in 2018–2020.
- Total PK-12 and grade counts are never suppressed in Denver rows.
- Suppressed Denver cells, from the audit `suppressed_membership`:
  - immigrant: 82 (2017), 152 (2018), 58 (2019), 140 (2020), 46 (2021), 50 (2022), 46 (2023), 35 (2024),
    24 (2025), 18 (2026);
  - EL: 2–19 per year.

**CMAS.** File notes:
- 2018: "*The value for this field is not displayed in order to protect student privacy."
- 2019 on: "- - The value for this cell is not displayed in order to protect student privacy."
- ESSA local report glossary: "In Colorado's ESSA State Plan, a minimum number of 16 students was
  established for all measures of student achievement."

Observed in Denver school rows [DATA: audit `suppressed_cmas`]:
- 2017–2022: when valid scores are below 16, 'Number of Valid Scores' shows '< 16' and total records,
  participation, mean, SD and percent are withheld. The counts match exactly: in 2019, 3,067 '< 16' and
  3,067 withheld record counts.
- 2023–2026: total records are withheld only below 4 ('< 4'; 1,945 cells in 2023). Valid scores below 16
  show '< 16' while total records stay published (2,296 cells in 2023).
  - So sums of `n_records` are much more complete from 2023. Do not read the jump in summed NEP records
    across 2022→2023 as all inflow.
  - Denver grade 3–8 ELA NEP records summed over published cells: 994 (2022), 1,945 (2023), 3,482 (2024),
    2,833 (2025), 2,904 (2026). [CALCULATION]

Performance-level cells are withheld when small, even with 16 or more valid scores. When they are, 'Number
Met or Exceeded' and the percent are withheld too. [DATA: raw 2024 overall rows, e.g. school 0099 math grade
5, 22 valid, levels '11', '7', '- -', '- -', '- -']
- This suppression is not random. Among rows with a published mean scale score, the rows with the percent
  withheld average 5–16 scale-score points lower than rows with it published, in every year × subject.
  [CALCULATION]
- School "Not EL" grade 3–8 cells with at least 16 valid scores, both subjects [CALCULATION]:

| year | cells | percent withheld | mean scale score missing |
|---|---|---|---|
| 2019 | 309 | 93 | 0 |
| 2022 | 302 | 134 | 2 |
| 2023 | 304 | 160 | 0 |
| 2024 | 292 | 137 | 0 |
| 2025 | 294 | 150 | 0 |
| 2026 | 280 | 149 | 0 |

**Staff and ESSA spending.** No suppressed cells in Denver rows (audit `suppressed_staff`,
`suppressed_ppe` empty).

## 6. Consistency checks in the build (all pass)

[CALCULATION: `derived/denver_audit.json` → `check_tallies`, `checks` empty]

| check | result |
|---|---|
| grade cells sum to the published PK-12 count | 2,015 of 2,015 rows equal |
| IPST PK-12 vs grade-file PK-12 | 2,014 of 2,014 equal; 3 not comparable (9803 Gilliam School, 2018–2020, absent from the grade and ratio files) |
| IPST PK-12 vs PTR-file PK-12 | 2,014 of 2,014 equal |
| published ratio vs PK-12/FTE | 2,014 of 2,014 within 0.01 (decimal years) or 0.5 (integer years) |
| ESSA membership vs October PK-12 | 1,415 of 1,415 equal |
| ESSA federal + state/local vs total | 1,417 of 1,417 within $2 |
| CMAS 'All Grades' vs sum of grade rows (n_records and n_tested, per school × subject × group) | 13,888 of 13,888 checkable `3-8` comparisons equal; 2018 `3-8+courses`: 722 equal, 12 differ (course takers) |
| CMAS all-students vs sum of the language groups (n_records, per school × subject × grade) | 6,058 of 6,058 checkable comparisons equal |
| CMAS 2019+: EL = NEP + LEP; Not EL = FEP/FELL + PHLOTE/NA/Not Reported (n_records) | 3,132 of 3,132 and 3,522 of 3,522 checkable comparisons equal |

Not checkable means a suppressed cell on either side: 13,986 of the 'All Grades' comparisons, 4,382 of
the partition comparisons, and 5,272 (EL) and 4,912 (Not EL) of the subgroup comparisons.

## 7. Not published or not obtained

- **School-level newcomer counts (`newcomer_n`).** Not published.
  - DPS reports new arrivals as district totals. The new-arrival presentations name receiving schools
    without counts.
  - Searches before this session's context reset: Exa searches for DPS board "Update: New Arrivals"
    decks, the DPS Strategic Regional Analysis (Spring 2024), Chalkbeat, CBS, Denverite, 9News, CPR and
    Westword.
  - Searches on 2026-09-28: Exa query "Denver Public Schools newcomer students enrollment by school table
    2023-24 migrant arrivals number of newcomers per school". Results:
    - the DPS SRA Spring 2024 and SRA Spring 2026 (district totals; the 2026 SRA's "New Arrivals" section
      reports "641 K-12 New Arrival students in 2025-26");
    - the DPS 2023-24 annual report (court exhibit, courtlistener);
    - Chalkbeat 2023-10-03, 2024-03-16 and 2024-10-08; 9News 2024-06-03; Denver Gazette 2024-04-23.
  - No result gave counts by school. Chalkbeat 2023-10-03 lists the schools that received the most
    (Lena Archuleta, Ashley, Bryant Webster, McMeen, Place Bridge, Denver Green School Southeast,
    Hamilton, George Washington, Thomas Jefferson, Abraham Lincoln) "according to the presentation", with
    no numbers. [SOURCE: Exa excerpts, not archived]
  - Proxy: `immigrant_n`, which rises in Denver from 3,283 (2023) to 5,643 (2024) and 9,265 (2025)
    [CALCULATION, published cells].
- **NEP and LEP separately in membership.** Not published. Membership gives NEP+LEP combined from 2024
  only. CMAS gives NEP and LEP test records and scores by school every year.
- **Class size.** CDE publishes no school-level class size.
  - The DPS SRA Spring 2026 has a "Class Sizes" section (p. 45 in its table of contents) and recommends to
    "Monitor district-run elementary class size for risk of exceeding 30 students in a classroom. This
    year, these make up 5% of DPS elementary classrooms." I read this through an Exa crawl; it is not
    archived, and I did not check whether it has school-level tables.
  - `ptr_calc` is the available school-level staffing-intensity measure.
- **DPS school budget allocations (student-based budgeting) and mid-year newcomer adjustments.** Not
  obtained.
  - `financialservices.dpsk12.org/o/financialservices/page/financial-transparency` returns a
    "Client Challenge" page to curl (HTTP 200, 3,038 bytes).
  - Its Wayback capture 20260116133345 holds only navigation; the page content is loaded by script.
  - The BoardDocs file of the 2022-23 draft proposed budget returned HTTP 403 to curl on 2026-09-28.
  - Exa query "Denver Public Schools school-level budget by school student based budgeting FTE
    allocations spreadsheet 2023-24 new arrivals mid-year funding per school" returned district-level
    documents only.
  - One lead: a funding-formula implementation profile says DPS "publishes per-pupil expenditure data for
    each school annually" and links a "School Budgets Report Sample" on Google Drive, not followed.
  - The only school-level spending series here is CDE's ESSA file.
- **ESSA spending before FY2018-19.** Not found. The earliest CDE ESSA school file is FY2018-19
  (`ft_fy2019_essadatafile`). Before this session's context reset, a 2020 Wayback capture of the old
  Financial Transparency page listed no earlier ESSA files.
- **CMAS 2020.** Not administered. **CMAS 2021.** Only ELA grades 3, 5, 7 and math grades 4, 6, 8, with low
  participation: rates as low as 14.7% (ELA) and 12.7% (math) in some Denver cells. [DATA]
- **Available but not used:**
  - School-level free/reduced-lunch counts: CDE publishes them yearly (e.g. "2024-25 PK-12 Free and
    Reduced Lunch Eligibility by School" on the archive page). They are in the 2025-26 workbook
    (`FRL_PK12`, `FRL_K12` sheets). Not parsed.
  - ESSA local reports for Denver, 2022–2025 (cached, sha256 below). They have an EDUCATORS sheet with
    school-level inexperienced, emergency-credential and out-of-field teacher FTE from the "2021-22" to
    "2024-25 Human Resource Snapshot". Not parsed because:
    - 'Total FTE' there is not the teacher FTE of the ratio files (Abraham Lincoln: 27.4 there vs 68.4 in
      the 2022 ratio file);
    - 2025 cells are largely withheld as '< 50.0%' / '>= 50.0%' / '--';
    - it starts only in 2022.

    Their GRO sheet gives median growth percentiles for "Multilingual Learners" but no Not-EL group.

## 8. Source detail: titles, headers and URLs

Headers are quoted after collapsing internal whitespace and line breaks. Years below are spring years.

### Membership by instructional program (IPST), 2017–2025, and the 2025-26 IPST sheet

- URLs: old CDE site, fetched through Wayback `id_` captures (appendix). New-site
  (`ed.cde.state.co.us`) copies are sha256-identical to the Wayback copies for the grade files 2020–2025
  and the IPST files 2020–2022 [CALCULATION: comparison copies in the session scratchpad `cmp/`].
- Title rows:
  - 2017–2023: "2016-2017 PUPIL MEMBERSHIP INSTRUCTIONAL PROGRAMS BY SCHOOL" … "2022-2023 PUPIL MEMBERSHIP
    INSTRUCTIONAL PROGRAMS BY SCHOOL";
  - 2024–2025: "Colorado Department of Education" / "2023-2024 Pupil Membership Instructional Programs by
    School", "2024-2025 …";
  - 2026 sheet `IPST`: "Student October 2025-26: School Level PK-12th Grade Pupil Membership" / "2025-2026
    Pupil Membership Instructional Programs by School".
- Headers relied on:
  - 2017: 'Distr Code', 'Sch Code', 'School Name', 'PK-12 Count', 'EL Count', 'EL Pct', 'Homeless Count',
    'Homeless Pct', 'Immigrant Count', 'Immigrant Pct', 'Migrant Count'.
  - 2018–2020: 'School Year', 'District Code', 'School Code', 'Total PK-12 Pupil Membership', plus the same
    EL, homeless, immigrant and migrant columns.
  - 2021–2023: 'District Code', 'School Code', 'PK-12 Pupil Membership', plus the same.
  - 2024: 'Organization Code', 'School Code', 'PK-12 Count', 'EL Count (NEP/LEP Only)', 'EL (NEP/LEP Only)
    Pct', 'EL Count', 'EL Pct', …
  - 2025: … 'EL Count Including FEP Monitor Year 1 and Year 2', 'EL Including FEP Monitor Year 1 and Year 2
    Pct', 'EL FEP Exited Year 1 and Year 2 Count', …
  - 2026: 'Multilingual Learner: NEP/LEP Only Count', 'Multilingual Learner: NEP, LEP, FEP Monitor Year 1
    and Monitor Year 2 Count', 'Multilingual Learner: FEP Exited Year 1 and Exited Year 2 Count', 'Homeless
    Count', 'Homeless Percent', 'Immigrant Count', 'Immigrant Percent', 'Migrant Count'.
- Rows with school code '0000' are excluded.

### Membership by grade, 2017–2025, and the 2025-26 `Grade` sheet

- Titles: "2016-2017 PUPIL MEMBERSHIP BY SCHOOL AND GRADE" … "2024-2025 Pupil Membership by School and
  Grade"; the 2026 sheet: "Grade Level".
- Headers: 'Pre-K', 'Half-Day K' / 'Half-Day Kinder', 'Full-Day K' / 'Full-Day Kinder', '1st' … '12th',
  'PK-12 Count'.
- In the 2026 sheet '-' marks a grade with no pupils. The build reads it as 0, and the row sums confirm this
  against 'PK-12 Count' in all 190 rows.

### Pupil/teacher FTE ratio by school, 2017–2025, and the 2025-26 `Teacher by School` sheet

- Titles:
  - "2016-2017 PUPIL/TEACHER FTE RATIO BY SCHOOL";
  - "2017-2018 PUPIL TEACHER RATIO" … "2022-2023 PUPIL TEACHER RATIO";
  - "2023-2024 PUPIL TEACHER RATIO BY SCHOOL";
  - "2024-2025 Pupil Teacher Job Codes 201-206 Ratio by School";
  - "2025-2026 Pupil Teacher (Job Codes 201-206) Ratio by School".
- Headers: 'District Code' / 'Organization Code' / 'LEA' / 'LEA Code', 'School Code', 'PK-12 Count' (2025:
  'Enrollment Count'), 'Teacher FTE', and the ratio column:
  - 'Pupil/Teacher FTE Ratio' (2017, 2023–2025);
  - 'Pupil/ Teacher FTE Ratio' (2018–2022);
  - 'Pupil/Teacher Ratio' (2026).
- The other 2026 sheets (Counselor, Registered Nurse, Psychologist, Social Worker) are LEA-level only.

### ESSA per-pupil expenditures, FY2019–FY2025

- URLs: `/cdefinance/ft_fy20XX_essadatafile` on the old site through Wayback for FY2019–FY2024; the new
  site for FY2025 (appendix).
- Sheets and titles:
  - FY2019 sheet 'FY18-19_CO_ESSA_Per-Pupil' (header on row 1);
  - FY2020 'FY19-20_CO_ESSA PPE';
  - FY2021 "FY2021-2022 ESS Per-Pupil Expenditures" (typo, see §2);
  - FY2023 "Statewide ESSA Per-Pupil Expenditures" / "FY2022-2023";
  - FY2024 "ESSA Per-Pupil Expenditures" / "FY2023-24";
  - FY2025 "FY2024-25 ESSA Per-Pupil Expenditures" / "Financial Transparency for Colorado Schools".
- Headers: 'Fiscal_year' / 'Fiscal_Year' / 'FISCAL_YEAR', 'Dist_Code' / 'Dist Code', 'School Code' /
  'Sch_Code', 'School_Name' / 'Sch_Name' / 'School Name', 'Charter School' / 'Charter School?',
  'Membership', 'Site Level - Federal' (FY2019; 'Site level - Federal' later), 'Site Level - State/Local',
  'Site Level Total', 'Site Share of Central Expenditures - Federal', 'Site Share of Central Expenditures -
  State/Local', 'Site Share of Central Expenditures - Total', 'Total School Expenditures'.
- All values are dollars per pupil.

### CMAS ELA and math, overall district and school results

- Pages: https://ed.cde.state.co.us/assessment/cmas/cmas-dataandresults (2026, cached as
  `cde_page_cmas_dataandresults.html`: "2026 CMAS Math and ELA District and School Overall Results (XLS)").
  Earlier years are on the new site's archive pages `/fs/pages/2255` (2017), 2256, 2257, 2261, 2263, 2264,
  2267 and 2279 (2025).
- Titles:
  - 2017: "CMAS ELA and Math (PARCC) 2017 District and School Level Achievement Results";
  - 2018: "2018 CMAS English Language Arts/Literacy and Mathematics District and School Achievement Results";
  - 2019: "2019 CMAS District and School Achievement Results" / "English Language Arts/Literacy and
    Mathematics";
  - 2021: "2021 District and School Achievement Results" / "2021 REQUIRED TESTS";
  - 2022–2026: "Colorado Measures of Academic Success (CMAS)" / "20XX District and School Achievement
    Results".
- Headers relied on:
  - 'Level', 'District Code', 'School Code', 'School Name';
  - 'Content' (2017: 'ELA'/'Math'; 2018, 2021+: 'English Language Arts'/'Mathematics'/'Spanish Language
    Arts') or 'Subject' (2019);
  - 'Test' (2017, e.g. 'ELA Grade 03'), 'Test/Grade' (2018) or 'Grade' ('All Grades', '03'…'08');
  - 'Number of Total Records' / '# of Total Records'; 'Number of Valid Scores' / '# of Valid Scores';
  - 'Participation Rate' (2022: current year; 2023+: 'Participation Rate 2023' etc.);
  - 'Mean Scale Score'; 'Standard Deviation' (2019+);
  - 'Number Met or Exceeded Expectations' / '# Met or Exceeded Expectations' (absent in 2022 overall);
  - percent met/exceeded as '% Met or Exceeded Expectations' (2017–2018) or 'Percent Met or Exceeded
    Expectations' (2019, 2021), or a column headed by the year ('2022' … '2026') under "Percent Met or
    Exceeded Expectations".
- The 2019 file repeats 'Mean Scale Score', 'Number Met or Exceeded Expectations' and 'Percent Met or
  Exceeded Expectations' for 2018. The build takes the first occurrence, which is 2019 (super-header "2019 |
  2018").

### CMAS ELA and math by language proficiency

- Sheets and titles:
  - 2017: sheet 'Sheet1_1', "Disaggregated CMAS PARCC Spring 2016-2017 Achievement Results" / "English
    Language Arts by Language Proficiency" (math: "Math by Language Proficiency");
  - 2018: "2018 CMAS English Language Arts/Literacy Disaggregated Results" / "English Language Arts by
    Language Proficiency";
  - 2019 and 2021–2026: sheet 'Language Proficiency', e.g. "2026 District and School Achievement Results" /
    "English Language Arts Disaggregated Results" / "English Language Arts Results by Language Proficiency".
- Headers: 'Level', 'District Number' / 'District Code', 'School Number' / 'School Code', 'Test' /
  'Test/Grade' / 'Grade', 'Language Proficiency', total records, valid scores, 'Participation Rate', 'Mean
  Scale Score', 'Standard Deviation' (2019+), number and percent met or exceeded (both files use '#'/'%' in
  2017–2018).
- The disaggregated files also carry Gender, Race Ethnicity, Free Reduced Lunch, IEP, Migrant and Gifted
  sheets, which are not parsed.

### Layout documents (cached for the definitions; not read by the build)

`cde_cmas_summary_layout_2017…2026.pdf` (summary-file field definitions) and `cde_cmas_sdf_layout_2025/2026.pdf`
(student data file field definitions): quoted in §2.

## Appendix: every cached file

`fetched from` is the capture or download URL. For new-site files, the `ed.cde.state.co.us/fs/resource-manager/view/<uuid>`
link redirects to `resources.finalsite.net`; both are shown.

**Membership by instructional program (IPST), by school**

| file | fetched from | bytes | sha256 |
|---|---|---|---|
| `cde_pm_ipst_school_2017.xlsx` | https://web.archive.org/web/20250905053124id_/http://www.cde.state.co.us/datapipeline/2016-2017ipstbyschool | 259726 | `6c11f3d00b6d4ebc02a47b1363cf164787f871f363cc130c4e8c7cdd44c8f741` |
| `cde_pm_ipst_school_2018.xlsx` | https://web.archive.org/web/20250905053140id_/http://www.cde.state.co.us/cdereval/2017-18-ipst-byschool | 288408 | `05e692b41a81e80b13c5ede67d2f42371429e95e09daf5eb17bc6b4e1c25a3e2` |
| `cde_pm_ipst_school_2019.xlsx` | https://web.archive.org/web/20250905053247id_/http://www.cde.state.co.us/cdereval/2018-19pk-12instructiona-programsbyschool-0 | 325629 | `1435b646f6072404ecc6ad482933a831f81ab22a0a36c52c4bdf43fc222ffa1d` |
| `cde_pm_ipst_school_2020.xlsx` | https://web.archive.org/web/20250905053228id_/http://www.cde.state.co.us/cdereval/2019-20pk-12instructionalprogramsbyschool | 295073 | `34917745639fd2754b034fdbcc8e7802757dc30f275f0325f54d8d9372a54fb2` |
| `cde_pm_ipst_school_2021.xlsx` | https://web.archive.org/web/20260329194130id_/https://www.cde.state.co.us/cdereval/2020-21instructionalprogrambyschool | 306786 | `dd6577b214bc549c134460e4ccdc962fc7b0bdafa2e4f96cd2f5bbbde84837bd` |
| `cde_pm_ipst_school_2022.xlsx` | https://web.archive.org/web/20250905053148id_/http://www.cde.state.co.us/cdereval/2021-2022schoolipst | 285119 | `8343381b0f9079d847d09d0415ca44b4d80c588b051ae80e914e507cc5586d67` |
| `cde_pm_ipst_school_2023.xlsx` | https://web.archive.org/web/20250905053211id_/http://www.cde.state.co.us/cdereval/2022-2023schoolipst | 271015 | `ca3f1f35941af1da6fd10e589a8db27c5098133a146ec2b6e34fbaba54f1791d` |
| `cde_pm_ipst_school_2024.xlsx` | https://web.archive.org/web/20250905053238id_/http://www.cde.state.co.us/cdereval/2023-24pk-12instructionalprogramsbyschool | 289436 | `42da20c56a5c80d20786c5f324c7c11cac52b43ba9b957c52d90e75abcf95f3e` |
| `cde_pm_ipst_school_2025.xlsx` | https://web.archive.org/web/20250922190606id_/https://www.cde.state.co.us/cdereval/2024-25pk-12instructionalprogrammembershipbyschool | 309464 | `08bc958d53ed0bccde66dd374e2e8118fdade5a24323540afdd8261684bd8707` |

**Membership by grade, by school**

| file | fetched from | bytes | sha256 |
|---|---|---|---|
| `cde_pm_grade_school_2017.xlsx` | https://web.archive.org/web/20250905053121id_/http://www.cde.state.co.us/cdereval/2016-17-pm-school-grade-excel | 259168 | `812973e1bfc54b4f2212ffb9ef893108e485723b3cdc5cb432f687ac66db22bc` |
| `cde_pm_grade_school_2018.xlsx` | https://web.archive.org/web/20250905053145id_/http://www.cde.state.co.us/cdereval/2017-18-gradelevel-byschool | 241409 | `45455fccbe2c8eb3f92d0710c65aed69aa8b7fd5f79326400eb1c144652d887d` |
| `cde_pm_grade_school_2019.xlsx` | https://web.archive.org/web/20250905053244id_/http://www.cde.state.co.us/cdereval/2018-19pk-12membershipgradelevelbyschool | 242393 | `80ac51d1b2e7a9b01e5b2b5bda86cd87d87e1bf53af9bbeb6efb13e9006d5dcc` |
| `cde_pm_grade_school_2020.xlsx` | https://web.archive.org/web/20250905053222id_/http://www.cde.state.co.us/cdereval/2019-20pk-12membershipgradelevelbyschool | 243020 | `493f230cc3ca01ee1b4dc0f3d8292f2c95305fd12104a324c04c7fb8dc19eaba` |
| `cde_pm_grade_school_2021.xlsx` | https://web.archive.org/web/20250905053203id_/http://www.cde.state.co.us/cdereval/2020-21membershipgradelevelbyschool | 238325 | `590f34fbe87c11e3c7ac4a93edec0af9979c79c8626a69ec992cb8979a54f42e` |
| `cde_pm_grade_school_2022.xlsx` | https://web.archive.org/web/20250905053154id_/http://www.cde.state.co.us/cdereval/2021-2022schoolmembershipgrade | 247840 | `e42c1c6cda98bdfd9d7095c4562865985a5d3d2cdf0fe2b814ac665e42182a7f` |
| `cde_pm_grade_school_2023.xlsx` | https://web.archive.org/web/20250905053214id_/http://www.cde.state.co.us/cdereval/2022-2023schoolmembershipgrade | 245490 | `4e9bee7596ccadf07b4b4a48cfada2a0eb9fbc667f909aa099915b72faf0f4de` |
| `cde_pm_grade_school_2024.xlsx` | https://web.archive.org/web/20250905053234id_/http://www.cde.state.co.us/cdereval/2023-24pk-12membershipgradelevelbyschool | 227025 | `66ccbfd6c03c740b756fe267f978e1d1eb34cf94b1ae378ed82282eab726cc34` |
| `cde_pm_grade_school_2025.xlsx` | https://web.archive.org/web/20250830161814id_/http://www.cde.state.co.us/cdereval/2024-25pk-12membershipgradelevelbyschool | 221914 | `ce0b2fc80bb824e35c16d938ebe92803202574d21629b1e1cd02180cd17680d0` |

**2025-26 school-level membership workbook**

| file | fetched from | bytes | sha256 |
|---|---|---|---|
| `cde_pm_school_workbook_2026.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/e1a21323-72ee-4c73-858b-fab252d0e75a → https://resources.finalsite.net/files/t_file_download/v1772753541/cdestatecous/nj98qjqay1rj0kwsphmg/2025-2026_PupilMembership_SchoolLevel.xlsx | 2856795 | `38162e17b78748aa75832741b390eec1ffd9fcca7158896e57b8e24212a5d387` |

**Pupil/teacher FTE ratio by school**

| file | fetched from | bytes | sha256 |
|---|---|---|---|
| `cde_ptr_school_2017.xlsx` | https://web.archive.org/web/20250905050929id_/http://www.cde.state.co.us/cdereval/student-teacher-ratios-xls | 172205 | `6d97b5b29e721a028f801f2f82c4031c2851a8a12624affeda31546d4ca053bc` |
| `cde_ptr_school_2018.xlsx` | https://web.archive.org/web/20250905050908id_/http://www.cde.state.co.us/cdereval/studentteacherratios2017-18xls | 185175 | `5af653db5c5cd9bfc5bff59173e1ff2e865038631de37fea5451cc115c776d9a` |
| `cde_ptr_school_2019.xlsx` | https://web.archive.org/web/20250905050919id_/http://www.cde.state.co.us/cdereval/2018-2019studentteacherratiosxls | 159980 | `82ea5a6ba0b1c5df1a933f839b2d01c23162e6fb9484c80184bf845455f8830c` |
| `cde_ptr_school_2020.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/5acec688-a349-4117-8117-1e6524085a9e → https://resources.finalsite.net/files/t_file_download/v1772753932/cdestatecous/z7kxxjqlwgtvgfhgxsba/Pupil-TeacherRatio.xlsx | 161775 | `aaf2e06062742bbf334672f146d65a9e12758c57052ecec9da532e683bc60f86` |
| `cde_ptr_school_2021.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/4ae60b1a-3e12-4e67-bda1-a809592d736b → https://resources.finalsite.net/files/t_file_download/v1772753911/cdestatecous/dbu0aasgh7wpvm6tbdjn/PupilTeacherRatio.xlsx | 149200 | `46758df6912a617fcc336f35668916a58691be198194ae406a9436cfa9500f84` |
| `cde_ptr_school_2022.xlsx` | https://web.archive.org/web/20260617231441id_/https://www.cde.state.co.us/cdereval/2021-22studentteacherratiosxls | 135277 | `92fae6d816a7013987d114c77a90d6574532ee046353f718cbf04fcaaf0f13b4` |
| `cde_ptr_school_2023.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/fc32f952-2545-44fe-bd98-3981d447cc83 → https://resources.finalsite.net/files/t_file_download/v1772753477/cdestatecous/qqxhvgcpnjrflrd4d7kn/20222023PupilTeacherRatiopublishedreport1.xlsx | 134043 | `306bb0cc1c382e921ae2569ce38c7c2469afc3d36a00786cc3035947383f4a26` |
| `cde_ptr_school_2024.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/95e52b1d-f4b7-4be9-9b65-199f3f9cac11 → https://resources.finalsite.net/files/t_file_download/v1772753499/cdestatecous/wgbay3ivliiawvuzcxow/2023-2024PupilTeacherRatiobySchool.xlsx | 179921 | `f9f11b2f1a2267748068d01bfc1a25903aa01efbc99c4439a06ae54f7eba788b` |
| `cde_ptr_school_2025.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/9e71cf39-e241-4258-8475-0bdd9724940e → https://resources.finalsite.net/files/t_file_download/v1772753516/cdestatecous/ybyrc5gty4ipwwym0at5/2024-2025PupilTeacherRatiobySchool.xlsx | 117535 | `4e53cd6637a6f3f3abde3e207e1b2b4782737056af0a7a9bd900b397c734fb5a` |

**2025-26 staff-to-pupil ratio workbook**

| file | fetched from | bytes | sha256 |
|---|---|---|---|
| `cde_staff_ratio_workbook_2026.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/29837afd-94d6-4b3f-a726-3febff7852e7 → https://resources.finalsite.net/files/t_file_download/v1775838201/cdestatecous/w0avpopuyd8zgjqnzsvj/2025-2026_StaffStatistics_StafftoPupilRatio.xlsx | 180502 | `966645abe119392045565bddf58811977c6f66fd6b7cf78a80dd5943913125f3` |

**ESSA per-pupil expenditures (Financial Transparency)**

| file | fetched from | bytes | sha256 |
|---|---|---|---|
| `cde_ft_essa_ppe_fy2019.xlsx` | https://web.archive.org/web/20230922140402id_/http://www.cde.state.co.us/cdefinance/ft_fy2019_essadatafile | 184497 | `6b188285bb7f8eb02b3b2013127c3bce05f6d2622e217d09b8269a0ff2c3473b` |
| `cde_ft_essa_ppe_fy2020.xlsx` | https://web.archive.org/web/20240305152054id_/https://cde.state.co.us/cdefinance/ft_fy2020_essadatafile | 187281 | `9a2aefd2575b73e9effe21254c4a65dc6aa95f17e4a7d26e7d8daada9b7ef8e9` |
| `cde_ft_essa_ppe_fy2021.xlsx` | https://web.archive.org/web/20240809162458id_/http://cde.state.co.us/cdefinance/ft_fy2021_essadatafile | 192599 | `fedc9bf454ec308c04bcc016469bee0f1084f6650abafe41908ac3515377d56d` |
| `cde_ft_essa_ppe_fy2022.xlsx` | https://web.archive.org/web/20260417214631id_/https://www.cde.state.co.us/cdefinance/ft_fy2022_essadatafile | 200090 | `44b18646563fc8f77544e8e568936cdbc8072b0af32b7bda90023016b30acd0b` |
| `cde_ft_essa_ppe_fy2023.xlsx` | https://web.archive.org/web/20250210154450id_/http://www.cde.state.co.us/cdefinance/ft_fy2023_essadatafile | 236988 | `c1ac0c850a858cd95892727f044d8ae7403e1097c87b8958419885006bb58271` |
| `cde_ft_essa_ppe_fy2024.xlsx` | https://web.archive.org/web/20260508203040id_/https://www.cde.state.co.us/cdefinance/ft_fy2024_essadatafile | 233016 | `ff5e1da67df6f0ed1b0e05b70f183586ebb8d27123e7386ea50dc4926129a9e5` |
| `cde_ft_essa_ppe_fy2025.xlsm` | https://ed.cde.state.co.us/fs/resource-manager/view/54182b20-14c9-4143-9c32-15849b7cc632 → https://resources.finalsite.net/files/t_file_download/v1781547500/cdestatecous/epfxvcnto3oqmefxw1ua/FY2024-25_ESSAPer-PupilExpenditures.xlsm | 311243 | `b99f350becbc95145d73886e0768e42b8d0d3e4566e442abb86bd37202303087` |
| `cde_ft_methodology_2026-07-14.docx` | https://ed.cde.state.co.us/fs/resource-manager/view/281a66c9-0e4b-4e00-9704-f21e0fca3d62 → https://resources.finalsite.net/files/t_file_download/v1784137481/cdestatecous/ymuplaaahfs58y0lzwwo/DataMethodology_Revised_7-14-2026.docx | 39005 | `bd3eb531ccc117c23ccd31e3fef03665481b88b470393f28367534267f61ae17` |

**CMAS ELA and math, overall district and school results**

| file | fetched from | bytes | sha256 |
|---|---|---|---|
| `cde_cmas_overall_2017.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/9bbb4ec7-ff14-4811-8cab-4354f880e069 → https://resources.finalsite.net/files/t_file_download/v1776115352/cdestatecous/amuvsfywhyxc8d50jksg/2017CMASELAMathDistrictSchoolOverallResultsFINAL_0.xlsx | 2162960 | `fc1888047e435b7e545edcb05e4475a8f6d7c7d6ffe0a1ca128e894e67b0f6fa` |
| `cde_cmas_overall_2018.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/298b1c43-b572-47ce-87b5-f24311f57e84 → https://resources.finalsite.net/files/t_file_download/v1776115350/cdestatecous/ipcb8ali5e4fbu5y40wu/2018CMASELAandMathDistrictandSchoolSummaryAchievementResults_FINAL.xlsx | 2351590 | `22e6a523d41ada5c6a9d5d958fff33a39442237d072f12b765caa04655d7e25e` |
| `cde_cmas_overall_2019.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/f211593e-4e86-4521-ac4b-edeb2dcaf2e8 → https://resources.finalsite.net/files/t_file_download/v1776115349/cdestatecous/mfkri9jqgpwmdaveyr9x/2019CMASELAMATHDistrictandSchoolAchievementResults.xlsx | 2542640 | `1f35cc5e4544fe9c842ddd76175f1b6cefe485a7765d5556b6c4bf4f0ef62c14` |
| `cde_cmas_overall_2021.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/8a7de0fa-b774-4158-b6bb-a727428e1d5c → https://resources.finalsite.net/files/t_file_download/v1776115367/cdestatecous/ckqnv9u8zgefmio8iqj0/2021CMASELAandMathDistrictandSchoolSummaryAchievementResults-RequiredTests_1.xlsx | 1003956 | `e2b09b64335cd01d5bc30fb78833b2773320adfc644cab6a9073ce41f943abd7` |
| `cde_cmas_overall_2022.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/b0b9bfba-827a-4756-ba94-a080dbaf3586 → https://resources.finalsite.net/files/t_file_download/v1776115349/cdestatecous/m0cipi2i963voucl9c99/2022CMASELAandMathDistrictandSchoolSummaryAchievementResults.xlsx | 2667327 | `e6987f4752bb6351f931d69390508f0578b61777bc1e88c1677602a15e9c0864` |
| `cde_cmas_overall_2023.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/4881a64a-4b04-4945-93b0-e9fe6c1edcb6 → https://resources.finalsite.net/files/t_file_download/v1776115348/cdestatecous/l67b72fmnf0iuhogayqj/2023CMASELAandMathDistrictandSchoolSummaryAchievementResults.xlsx | 2886179 | `d53fe2a5037d0f3268bc8eb8f130730b065c47e8ea71f736727e6ce7717fbf43` |
| `cde_cmas_overall_2024.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/2d1206ea-78b1-4a4d-9588-e540ff04080d → https://resources.finalsite.net/files/t_file_download/v1776115348/cdestatecous/axyl6lzxdo9ez4da3osq/2024CMASELAandMathDistrictandSchoolSummaryResults.xlsx | 2839049 | `b7d8ab68bc9ea3ba7451f3ac8518a4c6437d92aa989a975187f60ede3ad3c590` |
| `cde_cmas_overall_2025.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/5c130960-c90c-444a-98dc-41b35c11431b → https://resources.finalsite.net/files/t_file_download/v1776115348/cdestatecous/rrkmbmijrknlrhuvzk4e/2025CMASMathELACSLADistrictandSchoolSummaryAchievementResults.xlsx | 2854367 | `4b98b24812f867ab62910400e3e9a69dfb3a65aa9b7ebb900841b7362f1e69f9` |
| `cde_cmas_overall_2026.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/20b6751b-da99-4be8-953a-63c6047ee487 → https://resources.finalsite.net/files/t_file_download/v1787162700/cdestatecous/yjtns9iyskxbdjpexkb4/2026CMASMathELACSLADistrictandSchoolSummaryAchievementResults.xlsx | 2807128 | `3e09dc291af72efcf5566855401fa2697bac5f1cf1fede3ac386765363236197` |

**CMAS ELA by language proficiency**

| file | fetched from | bytes | sha256 |
|---|---|---|---|
| `cde_cmas_ela_disagg_2019.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/ca8d1384-aa67-4327-90a5-3524d8d22f3c → https://resources.finalsite.net/files/t_file_download/v1776115327/cdestatecous/wbyzqtqdbqmtjylm2aus/2019CMASELADisaggregatedDistrictandSchoolAchievementResults.xlsx | 15981930 | `7ef4f0f267221db2b943ac0c00540d7039a8f87de8f09c37694161b69f466b23` |
| `cde_cmas_ela_disagg_2021.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/8fff34f4-5fe9-4504-82ba-9ab450bb7cd5 → https://resources.finalsite.net/files/t_file_download/v1776115333/cdestatecous/bs20emjobbdeyjr8sxa8/2021CMASELADistrictandSchoolAchievementResultsDisaggregatedbySubgroups-RequiredTests_2.xlsx | 8299625 | `c3cd8393df98616787c183d760a9b6def79a56e6016577accdb9b58230c278f5` |
| `cde_cmas_ela_disagg_2022.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/8a39c269-016b-4246-9d8e-210112479fb8 → https://resources.finalsite.net/files/t_file_download/v1776115325/cdestatecous/n2bwvwj6vpgzmqtokjg0/2022CMASELASchoolandDistrictAchievementResults-DisaggregatedbyGroup.xlsx | 20447080 | `470acb93784fed2dca9b7f346e0fb544cbdce27642afa525be88f0173da6dffb` |
| `cde_cmas_ela_disagg_2023.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/8ffcb4d2-dffa-4d78-82a1-49b13dd8ed8b → https://resources.finalsite.net/files/t_file_download/v1776115321/cdestatecous/bsp0zue5dinmqehvn0aq/2023CMASELADistrictandSchoolDisaggregatedAchievementResults.xlsx | 20679598 | `c8046592408aa05440818b9953a063096e2a00f983bc80cecff55f2b56b741e3` |
| `cde_cmas_ela_disagg_2024.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/5e448f67-c371-4cb5-8fd5-4e22f710670e → https://resources.finalsite.net/files/t_file_download/v1776115321/cdestatecous/l6jtivcwus2bqteltuas/2024CMASELADistrictandSchoolDisaggregatedResults.xlsx | 20563445 | `37a85363b5e7daba162ca6951a78666b77a8a37f56f97d05095046d816542ec4` |
| `cde_cmas_ela_disagg_2025.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/ce57648f-fc3c-4dd9-a3ae-bf27c90848ad → https://resources.finalsite.net/files/t_file_download/v1776115324/cdestatecous/te0gf5usj8jou7wswzcu/2025CMASELADisaggregatedDistrictandSchoolAchievementResults.xlsx | 20466135 | `2fc233480639e63d94a2755f6b1702c96914d4679cc6d342bf32bb90efe52753` |
| `cde_cmas_ela_disagg_2026.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/35b6cde6-0cd3-4538-b5ff-19576f5be2a5 → https://resources.finalsite.net/files/t_file_download/v1787162714/cdestatecous/gbvlsqflvbskoburxfwg/2026CMASELADisaggregatedDistrictandSchoolAchievementResults.xlsx | 20297100 | `2f9be78842116d7674fd5b1b77000183a3136f4816b7d310242d510cc60ec575` |
| `cde_cmas_ela_langprof_2017.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/7b49d56d-4c08-4c60-9b34-129afb2cd063 → https://resources.finalsite.net/files/t_file_download/v1776115354/cdestatecous/owyv6myebezakw8kephd/DisaggregatedReportELA-LangProficiency_1.xlsx | 1890816 | `ca79c8d3bca47359811666873d2366f35f6eff109806807618061371b1d2e023` |
| `cde_cmas_ela_langprof_2018.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/77970976-ede2-408f-89b6-f722c5609438 → https://resources.finalsite.net/files/t_file_download/v1776115353/cdestatecous/tnwkymhhdbomvtlgmirg/2018CMASELAStateAchievementResultsDisaggregatedbyLanguageProficiency_FINAL.xlsx | 2150394 | `6ef92ccc2d7871f650e74ca2ed1034e538530421591dc7ecae0bad3f33249bf1` |

**CMAS math by language proficiency**

| file | fetched from | bytes | sha256 |
|---|---|---|---|
| `cde_cmas_math_disagg_2019.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/e11da2c5-648c-4b26-a065-91f7610f1647 → https://resources.finalsite.net/files/t_file_download/v1776115327/cdestatecous/rxiqvycjah8dvbqyokft/2019CMASMathDisaggregatedDistrictandSchoolAchievementResults.xlsx | 15910080 | `57d580076004faa60428be6be80ad26d1286e0cfcb16f351a6dc30c6904d70cf` |
| `cde_cmas_math_disagg_2021.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/d9878e45-2f03-4f95-8c3e-ab2276018081 → https://resources.finalsite.net/files/t_file_download/v1776115335/cdestatecous/mfihtbdscmjgibcjvtdx/2021CMASMathDistrictandSchoolAchievementResultsDisaggregatedbySubgroups-RequiredTests_1.xlsx | 7307619 | `598037b751704244b1dbb8ebb958550fd66fdb69bfb8999f94446ddb06977f94` |
| `cde_cmas_math_disagg_2022.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/f26955c6-66c3-4881-9cf2-c3b0b7214a3b → https://resources.finalsite.net/files/t_file_download/v1776115325/cdestatecous/h3f60rd7gclbwp7gzukt/2022CMASMathSchoolandDistrictAchievementResults-DisaggregatedbyGroup.xlsx | 20364151 | `b1f1f2cf0e30f507b649a0a995f997773ca0be16b4af90075c3d2c282c0b3483` |
| `cde_cmas_math_disagg_2023.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/8cfba38a-dfb0-4896-b4a5-893094d5d0ec → https://resources.finalsite.net/files/t_file_download/v1776115321/cdestatecous/avn43f8gscccecbqxbzi/2023CMASMathDistrictandSchoolDisaggregatedAchievementResults.xlsx | 20600577 | `e828a56de7435a0844e49a3fbfa44dccd08f72beb17d247dd6ca4789946e2203` |
| `cde_cmas_math_disagg_2024.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/fc4f710b-d64a-442f-ad73-ec81a15bb0ed → https://resources.finalsite.net/files/t_file_download/v1776115324/cdestatecous/eewhpgpbpobjgncj7167/2024CMASMathDistrictandSchoolDisaggregatedResults.xlsx | 20497164 | `505945024d23c90a219bc082b31dadff707848b32ab5271d7fa266731080bc24` |
| `cde_cmas_math_disagg_2025.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/405e216a-a1ba-4d67-913e-b61b92f3cb5c → https://resources.finalsite.net/files/t_file_download/v1776115325/cdestatecous/rgjs9xqaiquootvnczar/2025CMASMathDisaggregatedDistrictandSchoolAchievementResults.xlsx | 20459237 | `0c95e05b0557ef76b1279ac73e6add10f4185be0e93773bf3012315e91826ec8` |
| `cde_cmas_math_disagg_2026.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/c7cac613-7286-47c7-a725-ca1ca9a69826 → https://resources.finalsite.net/files/t_file_download/v1787162708/cdestatecous/jp9bcm9zhr0gkmxr6c3e/2026CMASMathDisaggregatedDistrictandSchoolAchievementResults.xlsx | 20334280 | `1117cd6540513408103c5288a24e50868ab282280ed8d3652dca0d081fbab112` |
| `cde_cmas_math_langprof_2017.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/a5c1d03c-d57c-4c07-b55f-e84477201a31 → https://resources.finalsite.net/files/t_file_download/v1776115357/cdestatecous/bw9hqsh622gqxipgteev/DisaggregatedReportMath-LangProficiency.xlsx | 1543557 | `22ab4f7dfb22bd23fff24bcbd2586789b43b74aab0f28e629c553c590492aa84` |
| `cde_cmas_math_langprof_2018.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/b6fa1a0c-9200-40aa-a4d8-5e8a238b9184 → https://resources.finalsite.net/files/t_file_download/v1776115351/cdestatecous/ljgpfppijfm8uoqpnhtn/2018CMASMathStateAchievementResultsDisaggregatedbyLanguageProficiency_FINAL.xlsx | 2283967 | `a3f0661aceca091b639c7d07f44ed15ed499aa91270226c87aeba1f9e6423842` |

**CMAS summary-file field definitions**

| file | fetched from | bytes | sha256 |
|---|---|---|---|
| `cde_cmas_summary_layout_2017.pdf` | https://ed.cde.state.co.us/fs/resource-manager/view/933b146b-e4e9-47b5-9237-9dfa4a5b40f4 → https://resources.finalsite.net/images/v1776115409/cdestatecous/bobrvcnbxyrcfnllvc4j/CO_CMAS_Spring_2017_ELA_and_Math_Summary_File_Field_Definitions_V11web.pdf | 177686 | `28c1cbdfad88e70ee28ac116c3f30a16e6a6d570937450a967950513615af6ce` |
| `cde_cmas_summary_layout_2018.pdf` | https://ed.cde.state.co.us/fs/resource-manager/view/3dfa46b8-c7e7-4f73-8dcd-e793d37dde52 → https://resources.finalsite.net/images/v1776115392/cdestatecous/uqobqnqtkwj2ybxpcled/2018CMASandCoAltSummaryDataFileLayout_V02_FOR_WEB.pdf | 374734 | `66088af2c1b8c2d53021da9518d47b146e1b8a115eab8b5ce95432838c956984` |
| `cde_cmas_summary_layout_2019.pdf` | https://ed.cde.state.co.us/fs/resource-manager/view/0174dd86-e853-442f-9ac6-6afe361347a0 → https://resources.finalsite.net/images/v1776115401/cdestatecous/m71npbjrxbx28fz5kbgu/2019_CMAS_CoAlt_Summary_File_Field_Definitions_03_Final.pdf | 267264 | `07234a37a973fdde34b3e33b0584be88d65b68775a2e9c047ac9cf091e8c6a87` |
| `cde_cmas_summary_layout_2021.pdf` | https://ed.cde.state.co.us/fs/resource-manager/view/5824d78a-68f3-4a31-95ec-446be747c76e → https://resources.finalsite.net/images/v1776115384/cdestatecous/nekzmblq29zyw8jlrupk/2021_CO_Summary_File_Field_Definitions_10.pdf | 514789 | `64b13e3ec471a1d1911749026ce9a3c4b282a995c6a411b0932e4f8b7e108d28` |
| `cde_cmas_summary_layout_2022.pdf` | https://ed.cde.state.co.us/fs/resource-manager/view/dfc59a81-a1fe-4776-b235-995ec69af636 → https://resources.finalsite.net/images/v1776115378/cdestatecous/qtgdegexfeq9qb1qippn/2022_CO_Summary_File_Field_Definitions_21_1.pdf | 587271 | `d03f8a1575a448e7a143a57d6801586a59f58bf30a7eb468239c527881de6940` |
| `cde_cmas_summary_layout_2023.pdf` | https://ed.cde.state.co.us/fs/resource-manager/view/929086fb-b673-4718-8faa-dcea4800d445 → https://resources.finalsite.net/images/v1776115382/cdestatecous/yjhiw7jo7qtabck7tjsl/2023_CO_Summary_File_Field_Definitions_30_Final_1.pdf | 539209 | `36c9147120f9f52a69c6f615f19518e15f922e933801ffa4c6e0c9b4d8994401` |
| `cde_cmas_summary_layout_2024.pdf` | https://ed.cde.state.co.us/fs/resource-manager/view/5809dcba-4d13-462d-98f1-0027789e934a → https://resources.finalsite.net/images/v1776115387/cdestatecous/phbxd8o4v0g9iawxwlof/2024_CO_Summary_File_Field_Definitions_31_0.pdf | 459722 | `5c12c1c7ccbf561d1fee7821c30a02ed4c1fbe734e9152a557e1e78acc51511f` |
| `cde_cmas_summary_layout_2025.pdf` | https://ed.cde.state.co.us/fs/resource-manager/view/f6b76141-39d7-4787-b7e9-5a5777952cb7 → https://resources.finalsite.net/images/v1776115383/cdestatecous/ibvj9yzuqoazxu5yon4i/2025_CO_Summary_File_Field_Definitions_32_1.pdf | 515699 | `ee55683c20c99d81a9ab763286c790665e8db977445c3c4c39c3ab61c735ddee` |
| `cde_cmas_summary_layout_2026.pdf` | https://ed.cde.state.co.us/fs/resource-manager/view/536b2eb6-011a-4ebb-9c82-3d6e26f8f939 → https://resources.finalsite.net/images/v1780351059/cdestatecous/olbevfuctuxygtaatvrc/2026_CMAS_CoAlt_Summary_Data_File_Field_Definitions.pdf | 588098 | `18814576f783126d3091b99d79ac39f95a14cb71aa1b574e7d3f9f3298566b36` |

**CMAS student-data-file field definitions**

| file | fetched from | bytes | sha256 |
|---|---|---|---|
| `cde_cmas_sdf_layout_2025.pdf` | https://ed.cde.state.co.us/fs/resource-manager/view/da6b7c4b-7c9f-46df-8540-7e27207095bb → https://resources.finalsite.net/images/v1787171722/cdestatecous/qjxoneguuz6xegj4mdlf/2025_CMAS_SDF_Field_Definitions_34.pdf | 514346 | `ae5f4adedc369fb77892373f3d7e8feda41cfa76f8ebd3886b3fd73f92df9726` |
| `cde_cmas_sdf_layout_2026.pdf` | https://ed.cde.state.co.us/fs/resource-manager/view/472c00b5-3451-4100-b649-e9ab05cd8611 → https://resources.finalsite.net/images/v1779891035/cdestatecous/gkhtdm8sjvwutvxddn6b/2026_CMAS_SDF_Field_Definitions.pdf | 644160 | `7d90b57c72540516969c57341502f27b10504abc8db6075805c565bc01c4ea78` |

**ESSA local report, Denver (cached, not read by the build)**

| file | fetched from | bytes | sha256 |
|---|---|---|---|
| `cde_essa_local_report_0880_2022.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/ff05167b-7020-4bd8-95d8-6c1735d31313 → https://resources.finalsite.net/files/t_file_download/v1773686285/cdestatecous/zakcheef7kvwzsfnsadf/0880DenverCounty1_21-22ESSAStateReport.xlsx | 2311568 | `713f473d3b07e1be97decfc666eead1e661d35911d116db15ce44a880b693c09` |
| `cde_essa_local_report_0880_2023.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/15988e8b-1b12-4464-bdfe-99ba23f40851 → https://resources.finalsite.net/files/t_file_download/v1773442136/cdestatecous/sy84exjgnx4rwdtzujvb/0880DenverCounty1_22-23ESSALocalReport.xlsx | 14880245 | `8f99ce30dfa3273c6a5dea1377c5c2a34c2f14d74406ad1f20e8fa66db26d035` |
| `cde_essa_local_report_0880_2024.xlsx` | https://web.archive.org/web/20251112041329id_/https://www.cde.state.co.us/fedprograms/2023-24-essa-local-report-0880-denver-county-1 | 2367552 | `cddfd9fcda871cb8b7e67ebb48e5a21f3884c5caad17d45306487082d83e2ae3` |
| `cde_essa_local_report_0880_2025.xlsx` | https://ed.cde.state.co.us/fs/resource-manager/view/953a3192-3af4-4edc-bf51-c6f0e4ada48d → https://resources.finalsite.net/files/t_file_download/v1771955072/cdestatecous/urgxfjpimani1tvzfjbs/0880_LocalReportData.xlsx | 3321225 | `e3adffc2ce6ac63743843a097d102b1410d1f229c484e8350c0a2471496427a9` |

**HTML pages quoted for definitions**

| file | fetched from | bytes | sha256 |
|---|---|---|---|
| `cde_page_cmas_dataandresults.html` | https://ed.cde.state.co.us/assessment/cmas/cmas-dataandresults | 55637 | `36237d5292fff52ac29a3897e8153ed0b6397cdf5289c3f2c719f1caf711a858` |
| `cde_page_pm_2016-17.html` | https://web.archive.org/web/20250901031352id_/http://www.cde.state.co.us/cdereval/2016-2017pupilmembership | 27674 | `ab1296bd7f5aa1f9851b394347759d4939e37f274e1c7ef963f462be624c1f42` |
| `cde_page_pm_2017-18.html` | https://web.archive.org/web/20250901031353id_/http://www.cde.state.co.us/cdereval/2017-18pupilmembership | 27907 | `35c4d4ba5250aa7652f949993bed313cfa6120af9724d9ba34e0c8840619c34c` |
| `cde_page_pm_2018-19.html` | https://web.archive.org/web/20250901031355id_/http://www.cde.state.co.us/cdereval/2017-2018pupilmembership | 27327 | `d0e1ecb0abea778048675b4ce169160cdc10db90c04c92fc5cac4d57259649e4` |
| `cde_page_pm_2019-20.html` | https://web.archive.org/web/20250901031354id_/http://www.cde.state.co.us/cdereval/2019-2020pupilmembership | 27606 | `57483e0de0ab08dc27fc5550d6ed9e7e54fdab005c1028dda7ba91f6129dc6a5` |
| `cde_page_pm_2020-21.html` | https://web.archive.org/web/20250922190558id_/https://www.cde.state.co.us/cdereval/2020-2021pupilmembership | 26986 | `ac570fd8da1c09e1613e4bda85f09d39cf4ce44cbf82c2ccdf5f52cad91aa047` |
| `cde_page_pm_2021-22.html` | https://web.archive.org/web/20250922190557id_/https://www.cde.state.co.us/cdereval/2021-2022pupilmembership | 26897 | `9300c8da9ba0c571ffc2ada74e5c1a72c133522ce1fa2006763e64f5a28a70dc` |
| `cde_page_pm_2022-23.html` | https://web.archive.org/web/20250922190557id_/https://www.cde.state.co.us/cdereval/2022-2023pupilmembership | 26704 | `5d553f9bd2bc5a723a58290d8dca6a11bbfb39543939e878daaf18685960f23b` |
| `cde_page_pm_2023-24.html` | https://web.archive.org/web/20250901031355id_/http://www.cde.state.co.us/cdereval/2023-2024pupilmembership | 26936 | `9b5ae85753cf5d1bca8712668a0d2f4f6025369b32a9679b485990245516de0a` |
| `cde_page_pm_archives.html` | https://ed.cde.state.co.us/cdereval/pupilmembership-statistics/data-insights-resources-archives | 112430 | `c18d5002c0505a6a98d0a7cf4f505ba51057b1272116c2c483fdadc8d233d8c5` |
| `cde_page_pm_statistics.html` | https://ed.cde.state.co.us/cdereval/pupilmembership-statistics | 56980 | `8ab92773e6ed5f3e96fa08d393f001ff37ab56077f15b35d0573474a585fd77a` |
| `cde_page_staff_archives.html` | https://ed.cde.state.co.us/cdereval/staffstatistics/data-insights-resources-archives | 83022 | `a97758aa517b634f5e9c1abfe19de98bf7ae364df5bd1373e11e2221987e2e1f` |
| `cde_page_staff_statistics.html` | https://ed.cde.state.co.us/cdereval/staffstatistics | 52282 | `c3373ddf2aabdec46c875387da463af4594bb4cac58bf00e66db54e844cd9c6d` |

<!-- 92 files; every sha256 re-verified against the file on disk -->
