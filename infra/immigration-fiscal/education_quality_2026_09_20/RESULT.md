# Education quality and later-generation data

**Verdict:** A descriptive skill comparison is possible now and was run. Among observed 2013 BA-or-higher holders in NLSY97, Mexican/Chicano identifiers with classified third- or fourth-plus-generation histories have lower adolescent ASVAB summary percentiles than the non-Hispanic-white fourth-plus-generation comparison. This supports the narrow objection that matching credentials does not ensure matched prior skills. College tier itself remains untested here; the public ELS/HSLS files suppress Mexican-origin detail, and available degree-awarding institution measures have additional selection limits. [SOURCE: derived/nlsy/{means,contrasts,coverage}.csv; held NCES public microdata audited below]

## Completed NLSY97 comparison

The cohort was born 1980–84 and sampled while resident in the United States. ASVAB was administered in 1997–98; degree status is the 2013 interview, generally age 28–33. BA+ includes bachelor's and postgraduate credentials, excluding associate degrees. This is a comparison of adolescent preparation among later graduates, not skills produced by their universities. [SOURCE: held primary codebooks for R9829600 and T8129600; [NLS assessment documentation](https://www.nlsinfo.org/content/cohorts/nlsy97/topical-guide/education/administration-cat-asvab)]

| Observed BA+ group | Scored n | Weighted mean percentile | Difference from white G4+, 95% sampling interval |
|---|---:|---:|---:|
| Mexican self-ID, G2 | 45 | 56.09 | −20.23 [−28.36, −12.10] |
| Mexican self-ID, G3 | 20 | 54.38 | −21.94 [−33.15, −10.73] |
| Mexican self-ID, G4+ | 20 | 63.71 | −12.61 [−21.79, −3.43] |
| Mexican self-ID, G3/G4+ pooled | 40 | 59.63 | −16.69 [−24.55, −8.83] |
| Non-Hispanic white, G4+ | 682 | 76.32 | Reference |

These are **percentile points**, not IQ points or standardized latent-ability differences. The intervals are exploratory and account for the public sampling design, not all selection or classification uncertainty. Estimates use 2013 interview weights and retain all 117 strata / 234 pseudo-PSUs for domain variance. The direct contrast includes covariance. Kish effective n is 33.07 for the pooled Mexican group and 676.67 for white G4+. [SOURCE: derived/nlsy/means.csv, contrasts.csv, audit.json; [NLS weights and design](https://www.nlsinfo.org/content/cohorts/nlsy97/using-and-understanding-the-data/sample-weights-design-effects)]

Checks against alternative constructions:

- Restricting both sides to **BA as highest degree**, excluding postgraduate holders, leaves Mexican G3/G4+ n32 and white G4+ n478: gap −17.72 points [−25.80, −9.64]. Thus this recorded contrast is not explained by the mixing of BA and postgraduate credentials. [SOURCE: derived/nlsy/contrasts.csv]
- Replacing 2013 weights with baseline weights among the same retained sample gives a pooled BA+ gap −16.79 [−24.74, −8.85]. Neither weight choice repairs every joint test/degree/family-history selection process. [SOURCE: same]
- There are 759 observed white G4+ BA+ holders, including 77 without scores. Their missing scores carry 10.51% of the group weight. Assigning those scores the extreme percentiles 0 and 100 bounds this realized group's mean at 68.30–78.81, still above the observed Mexican pooled mean of 59.63. These are fixed-sample missing-score bounds, not confidence intervals or ancestry bounds. [SOURCE: derived/nlsy/missing_score_bounds.csv]
- All 897 recorded Mexican identifiers have scores because the origin/descent questions were administered with ASVAB. Zero missing scores among the identified Mexican graduates **does not mean that all Mexican descendants were tested or identified**. The white missing-score exercise cannot repair that asymmetric ascertainment. [SOURCE: primary R97023–R97025 definitions; independent source reconstruction in verify_nlsy.py]

G3 requires US-born respondent, both biological parents US-born, and at least one foreign-born grandparent. G4+ requires all four grandparents reported US-born. The foreign-born forebear need not be Mexican. Mexican origin here is self-identification, not independent complete genealogy. Unknown family histories remain outside those exact groups. Degree holders with unresolved grandparents are not silently reassigned; the corresponding Mexican BA+ cell has n7 and a mean of 71.60 with a wide interval. [SOURCE: audited family linkage and derived/nlsy/coverage.csv, means.csv]

The contrast is not standardized by sex, major, institution, exact graduation age or family background. No school-value-added, genetic, fiscal or causal claim follows from it. A comparable result in a larger ancestry-ascertained sample, with joint test/degree observation and institution records, could change either the magnitude or the interpretation. [INFERENCE]

## Which other datasets help

All files below were already held locally. This turn inspected actual public data and codebooks; it did not obtain restricted files or submit applications. Counts are unweighted support counts, not substantive group estimates. [SOURCE: local primary files and bounded field probes]

### ELS:2002 — school achievement and selected college-tier comparisons

Local source: `/Users/alien/Projects/iq-sex-differences/data/els/els_02_12_byf3pststu_v1_0.sav`, 16,197 rows, SHA256 `4648297d46e4ed074f3d8be98ecd2afdd631de78c465f83fff6c855e9f1b34f4`. [SOURCE: [NCES student public archive](https://nces.ed.gov/datalab/files/zip/OnlineCodebook/ELS_2002-12_PETS_v1_0_Student_SPSS_Datasets.zip), [public codebook](https://nces.ed.gov/datalab/files/zip/OnlineCodebook/ELS_2002-12_v1_0_CodeBook_RecordFileLayout.zip)]

The public file includes standardized high-school math/reading composites and `F3TZDEG1SLC`, selectivity of the institution awarding the **first known certificate or degree**. That is more informative than first college attended, but is not automatically the school awarding a later BA. No latest-BA-awarding selectivity variable was established. The separate institution file's `F3ISELC` is suppressed on all 20,951 rows, so the attempted institution-level repair fails. [SOURCE: actual public files, embedded value labels, NCES codebook]

A conservative first-BA support probe, excluding known certificates/associate degrees and later graduate degrees, finds 266 Hispanic and 2,315 non-Hispanic-white records with institution-tier values; positive panel weights exist for 257 and 2,194. Requiring US-born respondent and both biological parents leaves 88 Hispanic records before the weight restriction. This subset **excludes AA-to-BA transfer paths**. Four selected white cases have a two-year institution classification that needs adjudication before estimation. No weighted selectivity gap was estimated. [SOURCE: raw support probe; conditions F3TZBACH1DT valid, F3TZHIGHDEG=3, F3TZCERT1DT=F3TZASOC1DT=−3; the relevant temporary probe artifacts are /private/tmp/education-quality-els/]

Mexican-origin fields `BYHISPAN`, `BYS16`, `BYP14` are suppressed as −5 on **every** public row. Public own/parent US-birth flags cannot recover Mexico or separate G3/G4; grandparent education is not grandparent birthplace. Hence this is a broad Hispanic education route, not an exact Mexican-lineage correction. [SOURCE: raw values and codebook]

### PIAAC — adult skills behind the credential

Held official national 2012/14 pooled source: `/Users/alien/Projects/iq-sex-differences/data/docs/2016667REV_HHPUF.zip`, SAS member `SAS/prgushp1_puf.sas7bdat`, 8,670 respondents. Separate 2017 national file: `/Users/alien/Projects/iq-sex-differences/data/piaac/prgusap1_2017.csv`, 3,660 respondents. Both provide literacy and numeracy plausible values and US race/ethnicity fields. [SOURCE: held primary files and 2016667REV_codebook.pdf; [NCES access description](https://nces.ed.gov/surveys/piaac/datafiles.asp)]

For respondents aged 25–65 who and whose mother/female guardian and father/male guardian were US-born, BA+ samples are:

| Release | Hispanic BA+ | NH-white BA+ | Hispanic BA-only |
|---|---:|---:|---:|
| Official 2012/14 pool | 32 | 1,100 | 21 |
| Separate 2017 | 28 | 640 | 22 |

These cases have all ten literacy and ten numeracy plausible values. The definitions use `RACETHN_5CAT` 1/2, `EDCAT8` 6–8 (BA-only 6), `J_Q04A=J_Q06A=J_Q07A=1`, and `AGEG5LFSEXT` 3–10. The last age band includes 65; this is not age 25–64. Inferences require pooling plausible-value uncertainty with 45 JK2 replicate-weight variances; simply treating the mean plausible value as an ordinary observed score understates uncertainty. No PIAAC outcome gap was estimated in this audit. [SOURCE: raw records; official codebook; existing sibling implementation analysis/piaac_p1_stratified.py]

Mexican subtype and grandparent history are unavailable in these public files. Even the underlying Mexican-origin question is asked after Hispanic identification, so it cannot recover ancestry nonidentifiers. Tests measure adult English literacy/numeracy, not college tier or the causal contribution of a particular school. The official access table lists the combined 2012/14/17 release as restricted-only; no informal overlapping-file concatenation was used. The site's stale 2023-release timetable is not evidence of present availability. [SOURCE: [US questionnaire](https://nces.ed.gov/surveys/piaac/2014-en-household-bq.html), [technical report](https://nces.ed.gov/pubs2020/2020224.pdf), raw public headers and NCES access table]

### HSLS:09 — useful school outcomes, held BA release too early

The held public 2017 student release has 23,503 records and useful grade-9/11 math and high-school GPA categories. Hispanic-origin detail and `X4IMMIGEN` are suppressed on all records. `X5HIGHSEC` measures the degree-awarding institution's sector, not selectivity. Only 17 Hispanic BA+ cases exist by the June 2016 transcript cutoff; that early-graduating subset cannot represent eventual BA holders. NCES lists a later 2021 administrative collection, but this audit did not establish its public awarded-BA selectivity variables. [SOURCE: actual HSLS_2017_PETS_SR_v1_0 student public file; [NCES available-data page](https://nces.ed.gov/surveys/hsls09/hsls09_data.asp)]

## Reproduction and validation

From the repository root:

```sh
UV_CACHE_DIR=/private/tmp/codex-uv-cache uv run --offline --no-project --with pandas --with scipy python3 infra/immigration-fiscal/education_quality_2026_09_20/analyze_nlsy.py
UV_CACHE_DIR=/private/tmp/codex-uv-cache uv run --offline --no-project --with pandas --with scipy python3 infra/immigration-fiscal/education_quality_2026_09_20/verify_nlsy.py
```

The commands use the already cached local Python dependencies; a fresh environment must first provision pandas and scipy with network access. The inputs come from the existing audited family/NLSY acquisition lanes; `derived/nlsy/audit.json` pins their hashes. The independent verifier imports no analyzer functions, reconstructs identity and generic generation from source fields plus previously audited parent linkage, and checks all 48 means, 72 contrasts, eight coverage rows and eight missing-score bounds. It reproduces 843 numeric checks and the official mean/SE benchmark 50.410/0.638. It does not independently rebuild the entire original parent-roster linkage. [SOURCE: derived/nlsy/verification.json]

Instrument check: this is LLM-assisted research. Raw variable definitions, independent arithmetic, alternative credential/weight constructions and explicit missing-score bounds constrain interpretation; they do not make the selected cohort equivalent to a complete ancestry sample. [INFERENCE]

## Revisions

2026-09-20: The final PIAAC adult-skills calculation is now [executed](PIAAC_RESULT.md). Its lower Hispanic point estimates have wide approximate intervals including zero in both releases; BA-only and age/sex checks remain inconclusive. This updates the earlier availability-only paragraphs above, retained as the discovery record. The [stopping decision](../../../decisions/2026-09-20-close-degree-quality-avenue.md) closes further modeling on the current public samples without changing the NLSY statistics or claiming adult skill equivalence.
