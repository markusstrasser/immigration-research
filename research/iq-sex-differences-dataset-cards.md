# IQ Sex Differences Dataset Cards

**Date:** 2026-03-05
**Companion config:** `sources/iq-sex-diff/stage0_config.py`

---

## ICAR / SAPA

**Local file:** `sources/iq-sex-diff/data/icar/sapaICARData18aug2010thru20may2013.csv`

**Unit:** person

**Observed rows:** `96,958`

**Key fields:**

- sex: `gender` with `1 = male`, `2 = female`
- age: `age`
- domains:
  - letter-number series
  - verbal reasoning
  - matrix reasoning
  - 3D rotation

**Scoring rule:**

- raw item matrix scored against `superKey60.tab`
- no survey weights
- treat as convenience sample only

**Primary use:**

- fast open-data decomposition
- composite-weight sensitivity checks
- invariance / DIF sandbox

**Main limitations:**

- convenience online sample
- no life-outcome linkage
- no nationally representative weighting target

## NLSY79

**Local file:** `sources/iq-sex-diff/data/nlsy/nlsy79_all_1979-2022.zip`

**Unit:** respondent

**Observed rows from local Stage 0 audit:** `12,686`

**Key identification fields:**

- respondent ID: `R0000100` / `CASEID_1979`
- household ID: `R0000149` / `HHID_1979`
- sex: `R0214800` / `SAMPLE_SEX_1979`

**Key pre-test background fields:**

- age 1979: `R0000600`
- age 1981: `R0410500`
- race / ethnicity: `R0214700`
- older siblings: `R0009300`
- mother education: `R0006500`
- father education: `R0007900`

**ASVAB score layer frozen for the primary pass:**

- arithmetic reasoning: `R0616200`
- word knowledge: `R0616400`
- paragraph comprehension: `R0616600`
- numerical operations: `R0616800`
- coding speed: `R0617000`
- auto and shop: `R0617200`
- math knowledge: `R0617400`
- mechanical comprehension: `R0617600`
- electronic information: `R0617800`

**Weight handling:**

- descriptive ASVAB summaries: `R0614700`
- general cross-sectional background summaries: `R0216101`
- sibling fixed effects: unweighted primary

**Sibling-link surface:**

- other interviewed youth IDs: `R0000150` to `R0000158`
- relationship codes: `R0000151` to `R0000159`
- sibling markers: `R0000162` to `R0000166`

**Current primary pair file:**

- `sources/iq-sex-diff/data/nlsy/nlsy79_opposite_sex_sibling_pairs.tsv`
- current locked build yields `1,461` opposite-sex pairs under the primary `<= 4` year age-gap rule

**Primary use:**

- keystone shared-family-confounding test
- clerical versus mechanical pattern inside one cohort
- later outcome relevance checks

**Main limitations:**

- public-use file does not remove within-family differential treatment
- age-at-test is proxied rather than directly timestamped
- some later XRND ability scores are incomplete at the subtest level

## NLSY97

**Local file:** `sources/iq-sex-diff/data/nlsy/nlsy97_all_1997-2023.zip`

**Unit:** respondent

**Observed rows from local Stage 0 audit:** `8,984`

**Key identification fields:**

- respondent ID: `R0000100` / `PUBID_1997`
- sex: `R0536300` / `KEY!SEX_1997`

**Audit note:**

- `R0001000` is an interview correction item and is largely missing in the local public-use extract
- `R0536300` is the usable respondent-sex field for the replication surface

**Weight handling:**

- descriptive primary weight: `R1236200`

**Frozen CAT-ASVAB score layer:**

- general science: `R9705200` + `R9706400`
- arithmetic reasoning: `R9705300` + `R9706500`
- word knowledge: `R9705400` + `R9706600`
- paragraph comprehension: `R9705500` + `R9706700`
- numerical operations: `R9705600` + `R9706800`
- coding speed: `R9705700` + `R9706900`
- auto information: `R9705800` + `R9707000`
- shop information: `R9705900` + `R9707100`
- math knowledge: `R9706000` + `R9707200`
- mechanical comprehension: `R9706100` + `R9707300`
- electronic information: `R9706200` + `R9707400`
- assembling objects: `R9706300` + `R9707500`

**Summary sensitivity score:**

- math-verbal percentile: `R9829600`

**Score-combine rule:**

- build one signed CAT-ASVAB ability score from the paired `POS` and `NEG` fields

**Primary use:**

- cross-cohort replication against `NLSY79`
- later-schooling environment checks
- variance and tail comparisons

**Main limitations:**

- no frozen sibling-FE design yet in this tranche
- CAT-ASVAB score construction needs careful `POS/NEG` recombination

## PSID CDS / TAS

**Local path:** `sources/iq-sex-diff/data/psid/`

**Current canonical builds:**

- child panel: `sources/iq-sex-diff/data/psid/psid_cds_panel.parquet`
- transition panel: `sources/iq-sex-diff/data/psid/psid_tas_panel.parquet`

**Unit:**

- child-wave row in the current `CDS` panel
- person-wave row in the current `TAS` transition panel

**Observed rows from the first cleaned build:** `6,373`

**Observed unique children / families:**

- unique children: `3,220`
- unique `1968` families: `1,322`

**Wave coverage in the canonical child panel:**

- `1997`
- `2002`
- `2007`

**Key identification fields:**

- current core family ID: `core_fid`
- current core sequence number: `core_sn`
- stable `1968` family ID: `family_id68`
- stable `1968` person ID: `person_id68`
- child pair ID: `pair_id68`

**Key score fields in the first pass:**

- `letter_word_std`
- `passage_comp_std`
- `broad_reading_std`
- `calculation_std`
- `applied_problems_std`
- `broad_math_std`

**Weight handling:**

- descriptive summaries and family-FE pass currently use `child_weight`

**Primary use:**

- family-linked early-school replication outside the `NLSY` / `ECLS` stacks
- aligned `math versus reading` checks
- within-family reduction of the simple shared-family objection
- transition extension using normalized `HS GPA`, `college GPA`, `SAT math`, `SAT reading`, and `ACT`

**Main limitations:**

- public-file hygiene matters:
  - sentinel score values like `999` must be recoded
  - `2002/2007` age fields are already in months
  - `1997 broad_math` is not independent from `applied_problems` in the current public child file
- `2019 TAS` `cross_weight` is entirely zero in the current public file, so weighted `TAS` summaries must fall back to the positive prior longitudinal weight
- the current family-FE pass addresses shared-family confounding only; it is not a full causal identification design

## Add Health

**Local path:** `sources/iq-sex-diff/data/addhealth/`

**Current canonical build:**

- `sources/iq-sex-diff/data/addhealth/addhealth_school_surface_extract.parquet`

**Unit:** respondent

**Current public-use waves used in the canonical first pass:**

- wave I in-home parent background
- wave II in-home grades
- wave III public `PVT` file for `PVTSTD1`
- wave IV in-home attainment

**Key identification / design fields:**

- respondent ID: `AID` / `aid`
- sex: `BIO_SEX`, `bio_sex2`
- design cluster: `CLUSTER2`
- wave II weight: `GSWGT2`
- wave IV weight: `GSWGT4_2` fallback `GSWGT4`

**Key school-performance fields in the first pass:**

- English grade: `H2ED7`
- math grade: `H2ED8`
- history grade: `H2ED9`
- science grade: `H2ED10`

**Key pre-treatment background fields in the first pass:**

- wave I `PVTSTD1` recovered from the public wave III `PVT` release
- resident mother education / occupation / public assistance: `H1RM1`, `H1RM4`, `H1RM9`
- resident father education / occupation / public assistance: `H1RF1`, `H1RF4`, `H1RF9`

**Key later outcome fields in the first pass:**

- high school diploma / GED status: `H4ED1`
- highest educational attainment: `H4ED2`

**Weight / design handling:**

- descriptive grade surfaces: `GSWGT2`
- wave IV attainment surfaces: `GSWGT4_2` fallback `GSWGT4`
- standard errors clustered on `CLUSTER2`
- `CLUSTER2` treated as design structure, not as a primary causal control

**Primary use:**

- broad school-performance / evaluation-family replication outside the NCES transcript stack
- baseline verbal-plus-family-background check on the grade wedge
- later-attainment extension of the school-surface family

**Main limitations:**

- public-use branch is not a clean transcript/test adjudication dataset
- no same-wave standardized math surface in the current canonical pass
- parent-background block is useful but still coarser than a full household-income / parental-transcript stack
- the current local public files expose sibling/twin flags but no obvious recoverable pair identifier for a clean within-family design

## FFCWS

**Local file:** `sources/iq-sex-diff/data/ffcws/ICPSR_31622/DS0001/31622-0001-Data.dta`

**Current canonical build:**

- `sources/iq-sex-diff/data/ffcws/ffcws_achievement_extract.parquet`

**Unit:** focal child / young-adult respondent

**Key baseline fields in the first pass:**

- sex: `CM1BSEX`
- mother education: `CM1EDU`
- baseline poverty ratio: `CM1INPOV`
- mother race: `CM1ETHRACE`
- mother married to child's father: `CM1MARF`
- mother cohabiting with child's father: `CM1COHF`

**Key Year 9 child cognitive fields:**

- `CH5PPVTSS`
- `CH5WJ9SS`
- `CH5WJ10SS`
- `CH5DSSS`
- age in months: `CH5AGEM`

**Key Year 22 transition fields in the first pass:**

- college years: `K7B2`
- ever college: `K7B45`
- current GPA: `K7B55`
- highest GPA: `K7B56`
- first-college GPA numerator / denominator: `K7B76_1`, `K7B77_1`

**Weight handling:**

- Year 9 descriptive sensitivity weight: `P5NATWT`
- Year 22 descriptive sensitivity weight: `K7NATWT`
- primary transition OLS: unweighted with explicit weighted sensitivity

**Primary use:**

- external stress test of child math / verbal geometry in a disadvantaged cohort
- transition extension testing whether the female schooling-accumulation wedge survives the child battery
- observed-confounder comparison of Year 9 applied problems, verbal surfaces, and digit span for later college exposure

**Main limitations:**

- no transcript/test linkage equivalent to `HSLS` or `HSTS`
- Year 9 child assessment weights do not line up as cleanly as the child-score nonmissing counts
- Year 22 GPA fields are sparse and selected; `college_years` is the cleaner transition surface in the first pass

## PIAAC

**Local files:** `sources/iq-sex-diff/data/piaac/*.csv`

**Unit:** respondent

**Observed local main files:**

- Germany `p1/p2`
- Finland `p1/p2`
- Italy `p1/p2`
- Japan `p1/p2`
- Netherlands `p1`
- United States `p1_2012`, `p1_2017`, `p2`

**Key fields:**

- sex: `GENDER_R`
- respondent ID: `SEQID`
- age: `AGE_R` or grouped fallback `AGEG10LFS_T`
- education: `EDCAT8`, `EDCAT7`, `EDCAT6`

**Score layer:**

- literacy: `PVLIT1` to `PVLIT10`
- numeracy: `PVNUM1` to `PVNUM10`
- problem solving: `PVPSL1` to `PVPSL10`

**Weight handling:**

- full-sample weight: `SPFWT0`
- replicate weights: `SPFWT1` to `SPFWT80`
- variance metadata: `VEMETHOD`, `VEFAYFAC`, `VENREPS`, `VARSTRAT`, `VARUNIT`

**Format rule:**

- current `p1` U.S. files are pipe-delimited
- current `p1` non-U.S. files are comma-delimited
- current `p2` files are semicolon-delimited

**Primary use:**

- cross-country education-stratified heterogeneity checks
- adult-skill outcome context
- later process-data integration

**Main limitations:**

- no local process / log files yet
- construct match to `ASVAB` and `ICAR` is partial, not automatic
- country comparisons remain scaling-sensitive
- current local `p2` files do not expose `EDCAT6`, `EDCAT7`, or `EDCAT8`, so primary education-stratified analyses should start on `p1`

## PISA 2018 / 2022

**Local path:** `sources/iq-sex-diff/data/pisa/`

**Snapshot status on 2026-03-05:**

- local now: `SPSS_STU_COG.zip`, `SPSS_STU_QQQ.zip`, `index.html`
- additional `2018` timing / visits and `2022` cognitive / questionnaire files were being staged in the same acquisition tranche

**Unit:** student, nominal age 15

**Construct surface:**

- international large-scale school math / reading / science assessment
- questionnaire layers for confidence, anxiety, school climate, and other
  school-linked attitudes
- public cognitive timing / visits surface is strongest in `PISA 2018`

**Primary use:**

- item-format and timing decomposition close to school exit
- cross-country checks on confidence / anxiety / school-system narratives
- public international test of whether score gaps move materially once the
  response-process layer is used

**Main limitations:**

- not the same construct as `ASVAB` quantitative or `PIAAC` numeracy
- country and cycle comparisons need scaling discipline
- local acquisition is not yet a fully complete `PISA` bundle in this snapshot

**Official source:** <https://webfs.oecd.org/pisa2022/index.html>

## TIMSS 2019

**Local paths:**

- grade 8: `sources/iq-sex-diff/data/timss/`
- grade 4: `sources/iq-sex-diff/data/timss_grade4/`

**Snapshot status on 2026-03-05:**

- grade 8 local: `SPSS Data`, `Codebooks`, `Item Information`, and `User Guide`
- grade 4 local: `SPSS Data`, `Codebooks`, and `Item Information`

**Unit:** student in grade 4 or grade 8

**Construct surface:**

- international school mathematics and science
- item-information and IRT-parameter support files
- linked official `eTIMSS` process-data ecosystem for digital assessments

**Primary use:**

- emergence check: grade 4 versus grade 8
- content-domain and item-information decomposition
- cross-country heterogeneity before labor-market accumulation enters

**Main limitations:**

- not a direct near-adult outcome surface
- public process-data workflow still needs additional staging and handling

**Official source:** <https://timss2019.org/international-database/>

## TIMSS Advanced 2015

**Local path:** `sources/iq-sex-diff/data/timss_advanced/`

**Snapshot status on 2026-03-05:**

- local: `TA15_SPSSData.zip`, `TA15_Codebooks.zip`, `TA15_UserGuide.pdf`,
  `TA15_ItemInformation.zip`

**Unit:** student in advanced-track mathematics or physics in participating
countries

**Construct surface:**

- advanced mathematics and physics achievement
- student, teacher, school, and curriculum background data

**Primary use:**

- upper-track / upper-tail adjudication
- test whether disagreement lives in advanced academic selection rather than in
  broad-population numeracy

**Main limitations:**

- selected advanced-track population, not general population
- not a clean measure of general ability

**Official source:** <https://timssandpirls.bc.edu/timss2015/advanced-international-database/>

## HSLS:09 Public-Use Surface

**Local files:**

- `sources/iq-sex-diff/data/hsls/HSLS09_VariableList_rev01-24.xlsx`
- `sources/iq-sex-diff/data/hsls/HSLS_2017_PETS_SR_v1_0_SPSS_Datasets.zip`
- `sources/iq-sex-diff/data/hsls/HSLS_2017_PETS_SR_v1_0_CodeBook_RecordFileLayout.zip`
- `sources/iq-sex-diff/data/hsls/hsls_onlinecodebook_manifest.json`

**Unit:** student and school public-use files

**Current local status:** complete

**Primary use:**

- best U.S. school-exit replication target for the grade-test wedge,
  evaluation / placement, curriculum exposure, and identity-sorting branches

**Main limitations:**

- public-use file is not the full restricted school-level surface
- acquisition depended on the `NCES Online Codebook` API rather than an obvious
  static study-page link

**Official source:** <https://nces.ed.gov/surveys/hsls09/>

## ELS:2002 Public-Use Surface

**Local files:**

- `sources/iq-sex-diff/data/els/ELS2002_Variable_List_throughF3-PETS.zip`
- `sources/iq-sex-diff/data/els/ELS_2002-12_PETS_v1_0_Student_SPSS_Datasets.zip`
- `sources/iq-sex-diff/data/els/ELS_2002-12_PETS_v1_0_Student_BRR_SPSS_Datasets.zip`
- `sources/iq-sex-diff/data/els/ELS_2002-12_PETS_v1_0_Other_SPSS_Datasets.zip`
- `sources/iq-sex-diff/data/els/ELS_2002-12_v1_0_CodeBook_RecordFileLayout.zip`
- `sources/iq-sex-diff/data/els/els_onlinecodebook_manifest.json`
- supporting transcript doc: `sources/iq-sex-diff/data/docs/ELS_03_transcript.pdf`

**Unit:** student public-use files

**Current local status:** complete

**Primary use:**

- transcript-rich earlier-cohort replication of the `HSLS` style analyses

**Main limitations:**

- public-use file still suppresses some school-identifying information
- replicate-weight handling is required for correct variance estimation
- first raw pass suggests some candidate transcript-summary variables may be
  suppressed or non-varying in the public-use file, so wedge replication needs
  a viability audit before it is treated as execution-ready

**Official source:** <https://nces.ed.gov/surveys/els2002/availdataproducts.asp>

## NELS:88 Public-Use Surface

**Local files:**

- `sources/iq-sex-diff/data/nels/NELS_Variable_List.zip`
- `sources/iq-sex-diff/data/nels/NELS_1988-00_v1_0_SPSS_Datasets.zip`
- `sources/iq-sex-diff/data/nels/NELS_1988-00_v1_0_CodeBook_RecordFileLayout.zip`
- `sources/iq-sex-diff/data/nels/nels_onlinecodebook_manifest.json`

**Unit:** student and postsecondary-linked public-use files

**Current local status:** complete

**Primary use:**

- older-cohort school pipeline and transcript-linked replication

**Main limitations:**

- older cohort and older file structure mean more cleaning overhead
- public-use file still needs construct alignment before comparisons to newer
  school-exit batteries

**Official source:** <https://nces.ed.gov/surveys/nels88/data_products.asp>

## HS&B Metadata Surface

**Local file:** `sources/iq-sex-diff/data/hsb/HSB_STUDY_VARIABLE_LIST.xlsx`
**Probe artifact:** `sources/iq-sex-diff/data/hsb/hsb_onlinecodebook_probe.txt`

**Unit once raw data are accessed:** student

**Current local status:** metadata-only

**Primary use:**

- older-cohort cognitive-growth and transcript-linked replication
- background check on whether later narratives are specific to recent school
  environments or already visible in older cohorts

**Main limitations:**

- current local surface is only a variable manifest
- live `Online Codebook` `file/data/1` requests currently return `HTTP 500` for
  tested public-use sessions, so respondent-level download is blocked by NCES
  infrastructure rather than by repo setup

**Official source:** <https://nces.ed.gov/surveys/hsb/data.asp>

## HSTS / NAEP Transcript Support Surface

**Local file:** `sources/iq-sex-diff/data/naep_hsts/cssc_list.xls`

**Unit:** course-code taxonomy / support material, not respondent-level records

**Primary use:**

- harmonizing transcript course ladders across NCES transcript studies
- making grade / course / ladder comparisons less ad hoc

**Main limitations:**

- no respondent-level `HSTS` records are staged locally here
- useful as infrastructure, not as a standalone adjudicator

**Official source:** <https://nces.ed.gov/use-work/elementarysecondary/hst-high-school-transcript-studies>
