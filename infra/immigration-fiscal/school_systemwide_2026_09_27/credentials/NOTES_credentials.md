claude-opus-5-5

**Verdict:** The ACGR (cohorts 2011-2022) and AFGR (2003-2013) state panels are parsed and match Digest Table 219.10 in every national year; the exit-exam snapshots from Digest Table 234.30 are parsed (24 states in 2013, 13 in 2019). The hand-built class-by-class exit-exam panel (`exit_exam_spells.csv`) was not finished, so `derived/exit_exams.csv` does not exist. (Verdict line written by the lane lead on 2026-09-28. The helper stalled and was stopped; its last note is timed 03:05 JST.)

PROBE IN PROGRESS: acquiring ACGR (Digest 219.46), AFGR (Digest 219.35) and a sourced exit-exam panel; findings are appended below as each part is confirmed. [UNVERIFIED] until the validation section is filled.

## Progress log

- 2026-09-28 01:50 JST. ACGR parsed from Digest Table 219.46, editions 2014-2023 (2012, 2013 and 2024
  editions return 404). Header grid expansion with rowspan/colspan; footnote-marker columns detected
  from the leaf header span. All-student series 2010-11 to 2021-22; subgroup years 2012-13 to 2021-22
  (one per edition, two in 2023). No cell differs across editions (min = max for every cell)
  [DATA: derived/acgr_state_all_editions.csv]. National all-student ACGR parsed: 79, 80, 81, 82, 83,
  84, 85, 85, 86, 87, 86, 87 for cohorts 2011-2022 [DATA: derived/acgr_state.csv]; external check
  pending. Digest 2024 Table 219.10 shows the national 2022-23 ACGR as "---" (prepared September
  2024) [SOURCE: https://nces.ed.gov/programs/digest/d24/tables/dt24_219.10.asp].
- AFGR parsed from Table 219.35 (2013-2019 and 2024 editions; annual 2002-03 to 2012-13, plus
  2018-19 and 2022-23 from the 2024 edition) and 219.40/219.41 (by sex and race: 2009-10, 2010-11,
  2011-12, 2012-13, 2022-23).
- 02:20 JST. National check passed: the parsed 219.46 national ACGR equals Digest 2024 Table 219.10's
  one-decimal national ACGR rounded half-up for all 12 cohorts 2011-2022 (79.0, 80.0, 81.4, 82.3,
  83.2, 84.1, 84.6, 85.3, 85.8, 86.5, 86.1, 86.6), and the parsed 219.35 national AFGR equals
  219.10 exactly for all 20 years it prints [DATA: derived/validation_national.csv; SOURCE:
  https://nces.ed.gov/programs/digest/d24/tables/dt24_219.10.asp]. The script exits [BLOCKED] on
  any mismatch. AFGR by race 2002-03 to 2008-09 added from the CCD web table
  (https://nces.ed.gov/ccd/tables/AFGR.asp), covering the 32-47 states that reported diplomas by race.
- Exit exams: cep-dc.org is now an unrelated site (404 with gold-IRA ads). The CEP reports are on
  ERIC: 2002 ED472055, 2007 ED503715, 2008 ED504468, 2009 ED513306, 2010 ED514155, 2011 state
  profiles ED530192-ED530223, 2012 ED535957 (files.eric.ed.gov/fulltext/<id>.pdf). The 2003-2006
  CEP reports are not in ERIC under their titles.
- 02:45 JST. Exit-exam snapshots parsed with code from Digest Table 234.30 [DATA:
  derived/exit_exam_digest_snapshots.csv]: 2013 edition (source EPE Research Center, retrieved Aug
  2013) lists 24 states "Yes" (AK AL AR AZ CA FL GA ID IN LA MA MD MN MS NJ NM NV NY OH OK SC TX VA
  WA; RI footnoted "Requirement takes effect for class of 2014"; CT "class of 2020"); 2022 edition
  (source ECS, Feb 2019) lists 13 "Yes" (FL IN LA MA MD MS NJ NM NY OH TX VA WA)
  [SOURCE: https://nces.ed.gov/programs/digest/d13/tables/dt13_234.30.asp,
  https://nces.ed.gov/programs/digest/d22/tables/dt22_234.30.asp]. These serve as code-parsed
  cross-checks on the hand-built class-year panel.
- 03:05 JST. Correction to my working notes: in the ECS May 2016 information request the footnote
  "The Class of 2016 will be the final class required to pass standardized assessments ... Class of
  2019 will be inaugural class required to pass end-of-course exams" is footnote 2 and belongs to
  Nevada, not Mississippi; Mississippi's footnote 1 says it "is transitioning away from its exit exam
  effective in the 2016-2017 school year" [SOURCE:
  https://www.ecs.org/wp-content/uploads/Info_Request_States_with_exit_exams.pdf]. ECS lists 17
  class-of-2016 exit-exam states (FL ID IN LA MD MA MS NV NJ NM NY OH OK OR TX VA WA). FairTest's May
  2019 sheet lists 11 for the class of 2020 (FL LA MD MA MS NJ NM NY OH TX VA) and its October 2025
  page 6 for the class of 2026 (FL LA OH NJ TX VA). CEP 2012 Table 1-C gives each 2011-12 exit-exam
  state's "Year diplomas first withheld"; CEP 2002 lists 18 states with exams in place and 6 phasing in.
