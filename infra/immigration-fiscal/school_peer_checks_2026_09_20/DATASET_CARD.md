# ECLS_K1998_PEERS — public student panel and teacher classroom counts

**Source:** NCES ECLS-K 1998–99 kindergarten cohort, final K–8 public file.
**Reused:** September 20, 2026, read-only from previously held public files.
**Unit:** child, 21,409 records; 15 physical ASCII lines per child.
**Lock:** [sources.json](sources.json), 1,591,930,422 raw bytes plus Stata dictionary.
**Storage:** selected Parquet and provenance in ignored `_cache/`; no raw-file copy.
**Access:** [NCES data products](https://nces.ed.gov/ecls/dataproducts.asp), subject
to the displayed public-use terms. Official links are `Childk8p.zip` plus
`Childk8p.z01`–`.z05`, and `ECLSK_Kto8_child_STATA.dct` under
`https://nces.ed.gov/ecls/data/`. These links were traced; no fresh archive
download/hash comparison is claimed. [Manual](https://files.eric.ed.gov/fulltext/ED511826.pdf).

| Fields | Definition / use | Primary verification |
|---|---|---|
| RACE=1 | Non-Hispanic white composite, with parent-report/FMS fallback | [First-grade manual](https://nces.ed.gov/pubs2002/2002135_2.pdf), pp7-11–12, Table7-14 |
| P2CHPLAC=1 | Born in 50 states/DC, not territories; does not identify parents' birth | [Spring-K parent interview](https://nces.ed.gov/ecls/pdf/kindergarten/springparent.pdf), INQ300 |
| WKLANGST=2 | English primary home language; not necessarily an English-only home or never-EL | [Base-year guide](https://nces.ed.gov/pubs2001/2001029rev_5_8.pdf), Table7-6 |
| A1OTLAN/A1LEP/A1NUMLE; A4OTLA/A4LEP/A4NUMLE | Teacher-reported other-home-language gate, LEP gate, LEP count | [Fall-K teacher](https://nces.ed.gov/ecls/pdf/kindergarten/fallteachersABC.pdf), Q13–17; [non-K round-4 teacher](https://nces.ed.gov/ecls/pdf/firstgrade/teachersABC.pdf), Q14/16/17 |
| A4KOTLA/A4KLEP/A4KNUML | Same constructs on retained-K form; negative skips become zero only through no gates | [Retained-K teacher](https://nces.ed.gov/ecls/pdf/firstgrade/kteacherABC.pdf), Q15/17/18; both no gates skip to Q22 |
| A1TOTRA/A1WHITE, A4TOTRA/A4WHITE, A4KTOTR/A4KWHIT | Classroom total and non-Hispanic-white counts, not immigrant counts | Corresponding teacher race-count tables; retained-K Q8 |
| A4CLASS | 1/2/3 K AM/PM/full-day form, 4 non-K form; not exact pupil grade | First-grade manual, pp7-29/7-74 |
| T4GLVL | Pupil grade composite; 4 first grade, 5 second, 1–3 K, 6 ungraded | Same manual, Table7-14 p7-87; retained for diagnostics, not selection |
| C1/C2/C4 R4RSCL and R4MSCL | Reading/math IRT scale scores; not theta | [Theta erratum](https://nces.ed.gov/pubs2010/2010052.pdf) explicitly says scale scores are correct |
| BYCOMW0, Y2COMW0 | Longitudinal combined child/parent/teacher weights | Final K–8 manual, chapter10, Exhibit10-4; repeated-wave complete-case restrictions remain |
| S1_ID/S4_ID, T1_ID/T4_ID | Internal school/teacher IDs available; special 999x schools excluded | Held dictionary/data. Teacher ID alone need not separate AM/PM classes |

**Known errata:** the separate [household-roster correction](https://nces.ed.gov/pubs2023/2023047.pdf)
concerns P4REL_1–19/P5REL_1–19, not the fields used here. No blanket negative-code
recode is appropriate. Both complete official errata were inspected.

**Instruction-language limitation:** current public A2ENGLS/A4IENGL fields are
populated and correspond to teacher-reported English-only instruction options.
Exact exported checkbox codes and unresolved contradictory responses require
additional checks before applying that restriction. This run does not apply it
or claim to reproduce Cho's sample. An older manuscript's suppression statement
does not establish absence from this final public release.

**Related public ECLS-K:2011 probe (executed 2026-09-21):** 18,174-child K–5 file.
`P2BTHPLC`/`P2CNTRYB` are all missing; `T1_ID` is constantly `-2`. Internal `S1_ID`
(860 schools), `X_HISP_R`, `X12LANGST`, and teacher ELL counts (`A1*NMELL`) are
populated. English-home non-Hispanic-white kindergarten school-FE association of
classroom ELL share with spring IRT theta, controlling fall theta/age/SES/sex:
reading +0.009 (se 0.013, n=2,044, 343 schools); math −0.001 (se 0.014, n=2,037).
Intervals include zero. This is not the 1998 US-born target and uses theta points,
not the 1998 scale-score SDs. [CALCULATION: `extract_2011.py`, `analyze_2011.py`,
`derived/ecls_k2011_summary.json`]

**State context:** TEA enrollment Tables2/14 and 2019/2024 TPRS staff tables;
CDE total enrollment and Title III immigrant-count/grant tables. Their period,
recent-immigrant definition, denominators and source URLs are retained in
`tabulate_growth.py` and the research note. These aggregates do not join ECLS
children or identify school-level causal arrivals.
