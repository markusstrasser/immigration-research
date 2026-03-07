# IQ Sex Differences - Additional Dataset Prospects

**Question:** Are there more datasets we can get that would materially improve this project?
**Tier:** Standard
**Date:** 2026-03-05

> **Historical note, 2026-03-06:** this memo predates the successful `PSID CDS/TAS` acquisition. `PSID` is now local and should be treated as a built panel, not a remaining download target. Current live access state is in `research/iq-sex-differences-access-playbook.md`. [SOURCE: `research/iq-sex-differences-access-playbook.md`; `research/iq-sex-differences-psid-cds-first-pass.md`]

## Ground Truth

Already local in this repo:

- `NLSY79`, `NLSY97`, `ICAR`, `PIAAC`
- `TIMSS 2019` Grade 4 and Grade 8
- `TIMSS Advanced 2015`
- `NLSCYA`, `ECLS-K`, `ECLS-K:2011`
- public-use respondent bundles for `HSLS:09`, `ELS:2002`, and `NELS:88`
- partial `PISA`
- metadata/support surfaces for `HS&B` and `HSTS`

Important acquisition note:

- `HS&B` remains officially public-use through `NCES DataLab / Online Codebook`,
  but the live `file/data/1` endpoint is currently returning `HTTP 500` for
  tested sessions, so it is server-blocked rather than missing from the plan

So the question is no longer “can we find any dataset at all.” The real question is which additional datasets most cleanly attack the live causal nodes:

1. early emergence versus later accumulation
2. grade-test wedge and placement contamination
3. broad school math versus advanced-track math
4. family-linked developmental trajectories
5. process / timing / interface effects

## Executive Answer

Yes. There are still several high-value datasets we can get.

The strongest additional targets are:

1. `NLSY79 Child and Young Adult (NLSCYA)` - immediate, highest value
2. `ECLS-K:2011` - immediate public-use
3. `ECLS-K` (1998-99 cohort) - immediate public-use
4. `HS&B` public-use files - important, but currently NCES-server-blocked
5. `PSID CDS/TAS` - low-friction registration, high family-design value
6. `NEPS` Scientific Use Files - free but contract-based
7. `Project Talent` - application-based, very high value for upper-tail and sibling questions
8. `NAEP` process and `HSTS` restricted microdata - high value, higher friction

The best next acquisition is **`NLSCYA`**, not because it is the biggest, but because it most directly attacks the unresolved node with family linkage, repeated child assessments, and school-linked development in the same overall data ecosystem as `NLSY79`.

## Ranked Dataset Table

| Rank | Dataset | Access status | Why it matters | Best node attacked | Official source |
| --- | --- | --- | --- | --- | --- |
| 1 | `NLSY79 Child and Young Adult (NLSCYA)` | immediate download / Investigator | Biological children of `NLSY79` mothers, repeated child assessments, family linkage, behavior and home environment | early emergence, family confounding, grade-test wedge precursors | <https://nlsinfo.org/content/access-data-investigator/accessing-data-cohorts> |
| 2 | `ECLS-K:2011` | immediate public-use download | repeated direct child assessments plus questionnaires from kindergarten to grade 5 | early emergence, teacher-rating / assessment wedge | <https://nces.ed.gov/ecls/dataproducts.asp> |
| 3 | `ECLS-K` | immediate public-use download | older cohort from kindergarten through grade 8, child / teacher / school catalogs | cohort replication of early math and school-evaluation surfaces | <https://nces.ed.gov/ecls/dataproducts.asp> |
| 4 | `HSLS:09` | staged locally via Online Codebook API | student files plus high school transcripts, postsecondary transcripts, financial aid, PEAR admin records | school-exit broad math versus transcript / track / identity | <https://nces.ed.gov/surveys/hsls09/hsls09_data.asp> |
| 5 | `ELS:2002` | staged locally via Online Codebook API | direct assessments, admissions test scores, high school transcripts, postsecondary transcripts | earlier school-exit cohort, grade-test wedge, track replication | <https://nces.ed.gov/fCSM/els2002.asp> |
| 6 | `HS&B` | public-use in principle, but current DataLab file endpoint returns `HTTP 500` | older cohort public-use microdata plus PowerStats | older-cohort school pipeline replication | <https://nces.ed.gov/surveys/hsb/accessingData.asp> |
| 7 | `PSID CDS/TAS` | registration required, otherwise low friction | nationally representative child development and transition-to-adulthood design with sibling comparisons and link to long household panel | family-linked development, standardized achievement, intergenerational pathways | <https://psidonline.isr.umich.edu/CDS/GettingStarted.aspx> |
| 8 | `NEPS` | free scientific-use files, contract required | grade 9 and other starting cohorts with competence tests and educational trajectories | cross-national schooling / track / competence replication | <https://www.lifbi.de/en-us/Start/Data-Services/Data-and-Documentation> |
| 9 | `Project Talent` | application / portal based | very large cognitive battery, siblings, twins, long follow-up | upper-tail, sibling, track, later-life outcomes | <https://www.air.org/project-talent/researchers> |
| 10 | `NAEP process data` | restricted-use license | item-level timing, visits, tools, digital process logs | process / interface / timing artifact | <https://www.nationsreportcard.gov/process_data/> |
| 11 | `HSTS` restricted microdata | public explorer plus restricted microdata | transcripts linked to NAEP achievement | transcript ladder versus tested performance | <https://www.nationsreportcard.gov/hsts_2005/hs_res_research.aspx> |
| 12 | `ABCD` | access-gated | broad adolescent neurocognitive and environmental data | lower-priority adolescent general-cognition replication | <https://abcdstudy.org/scientists/data-sharing-archive/> |

## Best Immediate Acquisitions

### 1. NLSY79 Child and Young Adult

This is the cleanest overlooked acquisition.

Why:

- the official NLS access page says downloads are available for `NLSY97`, `NLSY79`, and `NLSCYA` [SOURCE: <https://nlsinfo.org/content/access-data-investigator/accessing-data-cohorts>]
- the cohort follows the biological children of `NLSY79` women from `1986` to `2020` [SOURCE: <https://www.nlsinfo.org/content/cohorts/nlsy79-children>]
- the assessments page explicitly documents `PIAT Mathematics`, `PIAT Reading`, `PPVT-R`, `Behavior Problems Index`, `WISC Digit Span`, and `HOME`-type environment measures [SOURCE: <https://www.nlsinfo.org/content/cohorts/nlsy79-children/topical-guide/assessments/piat-mathematics>]

Why it is high value:

- same broad family ecosystem as `NLSY79`, but on children
- repeated math and reading achievement
- direct path to family-linked developmental profiles
- possible sibling and maternal fixed-effects style designs

This is the best next download if the goal is to move beyond adult batteries and fragile school-exit surfaces.

### 2. ECLS-K:2011

Why:

- NCES says the `ECLS-K:2011` public-use file contains child assessments and child questionnaires for `18,174` children across all nine rounds from kindergarten through grade 5 [SOURCE: <https://nces.ed.gov/ecls/dataproducts.asp>]
- the ECLS overview says both public-use and restricted-use files for all rounds are available [SOURCE: <https://nces.ed.gov/ecls>]

Why it matters:

- early-emergence surface
- repeated direct assessments
- school and teacher context
- lower risk of over-reading later track selection as innate ability

### 3. ECLS-K

Why:

- NCES provides public-use `ECLS-K` kindergarten-to-eighth-grade files directly from the data products page [SOURCE: <https://nces.ed.gov/ecls/dataproducts.asp>]
- that page also exposes child, teacher, and school catalogs [SOURCE: <https://nces.ed.gov/ecls/dataproducts.asp>]

Why it matters:

- older U.S. cohort
- direct replication of early-to-middle-school math surfaces
- useful bridge between `ECLS-K:2011` and `TIMSS`

## Best School-Exit / Transcript Acquisitions

### 4. HSLS:09

Why:

- NCES says student-level files are available for `2009`, `2012`, `2013`, and `2016`
- administrative records include high school transcripts, postsecondary transcripts, student financial aid, and PEAR [SOURCE: <https://nces.ed.gov/surveys/hsls09/hsls09_data.asp>]
- public-use data are available for immediate download via Online Codebook [SOURCE: <https://nces.ed.gov/surveys/hsls09/hsls09_data.asp>]

Why it matters:

- this is the best U.S. public-use school-exit surface for transcript ladder, grades, aspirations, and later outcomes
- it directly attacks the broad-math versus advanced-track wedge that `TIMSS` just surfaced
- the public-use respondent bundle is now local in this repo through the
  `Online Codebook` API path

### 5. ELS:2002

Why:

- NCES describes it as a nationally representative longitudinal study of more than `16,000` tenth-graders [SOURCE: <https://nces.ed.gov/fCSM/els2002.asp>]
- the same official page says the public-use files can be downloaded through Online Codebook and that the study includes direct assessments, admissions test scores, high school transcripts, postsecondary transcripts, and financial aid records [SOURCE: <https://nces.ed.gov/fCSM/els2002.asp>]

Why it matters:

- school-exit replication in an earlier cohort
- directly useful for grade-test wedge and transcript-path analyses
- the public-use respondent files and BRR bundle are now local in this repo

### 6. HS&B

Why:

- NCES says `HS&B` public-use microdata are available through the Online Codebook in DataLab, with PowerStats also available, while richer microdata remain restricted [SOURCE: <https://nces.ed.gov/surveys/hsb/accessingData.asp>]

Why it matters:

- older-cohort replication
- useful for checking whether newer school-pathway patterns are historically specific

Current blocker:

- the live `Online Codebook` file endpoint is returning `HTTP 500` for tested
  public-use sessions, so this is now a concrete NCES backend issue rather than
  a missing local automation path

## Best Family / Intergenerational Acquisitions

### 7. PSID CDS/TAS

Why:

- PSID says registration is required to download `CDS` or `TAS` data [SOURCE: <https://psidonline.isr.umich.edu/CDS/GettingStarted.aspx>]
- the study design page says `CDS` includes caregiver and child standardized assessments of achievement and enables sibling comparisons; `TAS` follows youth into schooling and work transitions [SOURCE: <https://psidonline.isr.umich.edu/CDS/Guide/StudyDesign.aspx>]

Why it matters:

- nationally representative
- repeated child and young-adult observations
- explicit sibling-comparison potential
- strong intergenerational linkage through core `PSID`

This is likely the second-best non-NCES addition after `NLSCYA`.

## Best International Education-Panel Acquisition

### 8. NEPS

Why:

- LIfBi says NEPS Scientific Use Files are part of its research data portfolio and are available free of charge for scientific analyses [SOURCE: <https://www.lifbi.de/en-us/Start/Data-Services/Data-and-Documentation>]
- LIfBi also says access requires a data use agreement [SOURCE: <https://www.lifbi.de/en-us/Start/Data-Services/Data-Access>]

Why it matters:

- educational trajectories with competence testing
- cross-national check outside U.S.-specific schooling institutions
- useful for track and course-path questions

Main limitation:

- not click-download; requires contract workflow

## High-Value But Higher-Friction Targets

### 9. Project Talent

Why:

- AIR’s researcher page says the base-year study includes cognitive ability, academic aptitude, and a very large school sample, plus `4,508` twins/triplets and `83,948` siblings [SOURCE: <https://www.air.org/project-talent/researchers>]

Why it matters:

- upper-tail and advanced-track questions
- sibling / twin leverage
- long-run outcomes

Main limitation:

- access is not as frictionless as NCES or NLS downloads

### 10. NAEP Process Data

Why:

- the official NAEP process page documents item-level timing, visits, tool use, and process logs for the `2017` grade 4 and grade 8 math assessments [SOURCE: <https://www.nationsreportcard.gov/process_data/>]
- the same page says access requires a restricted-use license [SOURCE: <https://www.nationsreportcard.gov/process_data/>]

Why it matters:

- strongest public-process architecture for testing timing / interface stories
- especially relevant after the `NLSY97` Stage A fragility and `PISA` process agenda

### 11. HSTS

Why:

- the official HSTS researcher guide says the transcript study links academic records to NAEP performance and offers a public explorer plus restricted-use microdata [SOURCE: <https://www.nationsreportcard.gov/hsts_2005/hs_res_research.aspx>]

Why it matters:

- transcript ladder versus test-performance link
- direct wedge surface for “grades / course-taking / placement are not pure latent ability”

## Lower-Priority Or Lower-Leverage

### 12. ABCD

Why it is not first:

- access is controlled through NIH / NDA workflows, and current release access is not purely open [SOURCE: <https://abcdstudy.org/scientists/data-sharing-archive/>]
- it is less directly aligned to school math, transcript ladders, and grade-test wedges than the education studies above

It may still matter later for broad adolescent cognitive-development replication, but it is not the best next acquisition for this repo.

## Best Remaining Acquisition Order

The immediate public-use NCES / NLS tranche is mostly local now. If the goal is
to reduce uncertainty fastest from here:

1. `HS&B`, but only if the NCES `HTTP 500` backend failure clears or a bypass is found
2. `PSID CDS/TAS`
3. `NEPS`
4. `Project Talent`
5. `NAEP process` / `HSTS` restricted files

## Claims Table

| Claim | Source | Status |
| --- | --- | --- |
| Downloads are available for `NLSY97`, `NLSY79`, and `NLSCYA`. | <https://nlsinfo.org/content/access-data-investigator/accessing-data-cohorts> | VERIFIED |
| `NLSCYA` follows biological children of `NLSY79` women and spans `1986` to `2020`. | <https://www.nlsinfo.org/content/cohorts/nlsy79-children> | VERIFIED |
| `NLSCYA` documents `PIAT Mathematics` and other assessment surfaces relevant to this project. | <https://www.nlsinfo.org/content/cohorts/nlsy79-children/topical-guide/assessments/piat-mathematics> | VERIFIED |
| `ECLS-K:2011` public-use data include child assessments and questionnaires for all nine rounds through grade 5. | <https://nces.ed.gov/ecls/dataproducts.asp> | VERIFIED |
| `ECLS-K` kindergarten-to-eighth-grade public-use files are downloadable from NCES. | <https://nces.ed.gov/ecls/dataproducts.asp> | VERIFIED |
| `HSLS:09` public-use data are immediately downloadable via Online Codebook and include transcript-linked administrative records in the study. | <https://nces.ed.gov/surveys/hsls09/hsls09_data.asp> | VERIFIED |
| `ELS:2002` public-use data are downloadable via Online Codebook and include direct assessments, test scores, and transcript records in the study. | <https://nces.ed.gov/fCSM/els2002.asp> | VERIFIED |
| `HS&B` public-use microdata are available through NCES DataLab / Online Codebook. | <https://nces.ed.gov/surveys/hsb/accessingData.asp> | VERIFIED |
| `PSID CDS/TAS` requires registration to download and includes standardized assessments of achievement plus sibling-comparison leverage. | <https://psidonline.isr.umich.edu/CDS/GettingStarted.aspx>, <https://psidonline.isr.umich.edu/CDS/Guide/StudyDesign.aspx> | VERIFIED |
| `NEPS` Scientific Use Files are free for scientific analyses but require a data use agreement. | <https://www.lifbi.de/en-us/Start/Data-Services/Data-and-Documentation>, <https://www.lifbi.de/en-us/Start/Data-Services/Data-Access> | VERIFIED |
| `Project Talent` includes large sibling and twin samples plus cognitive-ability and academic-aptitude data. | <https://www.air.org/project-talent/researchers> | VERIFIED FROM OFFICIAL PAGE SUMMARY |
| `NAEP` process files provide timing / visits / tool-use logs and require restricted-use access. | <https://www.nationsreportcard.gov/process_data/> | VERIFIED |

## Bottom Line

Yes. There are still more datasets we can get, and a few of them are genuinely high value.

The best immediate expansion was **`NLSCYA` plus `ECLS-K/ECLS-K:2011` plus `HSLS:09`**.

That combination would let this repo attack:

- family-linked developmental surfaces
- early-emergence math
- school-exit transcript and aspiration wedges

That tranche is now largely local. The best remaining additions are the
server-blocked `HS&B` path plus higher-friction targets like `PSID CDS/TAS`,
`NEPS`, `Project Talent`, and `NAEP` process / `HSTS` restricted files.

## Acquisition Update

Executed after this memo:

- `NLSCYA` direct shell download completed to `sources/iq-sex-diff/data/nlscya/nlscya_all_1979-2020.zip`
- `ECLS-K` direct shell download completed to `sources/iq-sex-diff/data/ecls_k/Childk8p.zip`
- `ECLS-K:2011` direct shell download completed to `sources/iq-sex-diff/data/ecls_k2011/ChildK5p.zip`
- `HSLS:09`, `ELS:2002`, and `NELS:88` public-use bundles were pulled through the `NCES Online Codebook` API into their local data directories

Blocker confirmed:

- `HS&B` remains officially public-use, but the live `Online Codebook`
  `file/data/1` endpoint currently returns `HTTP 500` for tested sessions
