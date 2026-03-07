# Dataset Roadmap and Methodology — Pedagogical Research

**Date:** 2026-03-06

## Dataset Acquisition Status

### Acquired (local, ready for analysis)

| Dataset | Location | Size | Format | Notes |
|---------|----------|------|--------|-------|
| PSID CDS/TAS | `data/psid/` | 20 files | various | All CDS + TAS public bundles. Child panel + transition panel built. |
| Add Health public-use | `data/addhealth/` | 169 MB | .tab, .sas7bdat, .xpt | Waves 1-6 from UNC Dataverse. Public subset of variables. |
| NLSY79 | `data/nlsy79/` | — | — | ASVAB + schooling extracts built |
| NLSY97 | `data/nlsy97/` | — | — | PIAT, transcript, behavior, course, stage-A passes built |
| ECLS-K / ECLS-K:2011 | `data/ecls*/` | — | — | Early school extracts built |
| NELS | `data/nels/` | — | — | Wedge first pass built |
| ELS | `data/els/` | — | — | Wedge first pass built |
| HSLS | `data/hsls/` | — | — | Wedge first pass + refinement built |
| PISA 2018 | `data/pisa/` | — | — | DIF, framework proxy, item split passes built |
| TIMSS | `data/timss/` | — | — | Cognitive split, grade decomposition built |
| PIAAC | `data/piaac/` | — | — | Age-stratified, occupation proxy passes built |
| ICAR | local | — | — | Decomposition pass built |

### Codebooks only (ICPSR institutional membership required for data)

| Dataset | Location | Status |
|---------|----------|--------|
| HSB (7896, 8297, 8443, 8896) | `data/hsb/codebooks/` | 4 codebook zips. Data files require ICPSR institutional membership. |
| SECCYD Phase I (21940) | `data/seccyd/codebooks/` | Codebook zip. Data files require ICPSR institutional membership. |

### Blocked — requires decision

| Dataset | Blocker | Value | Priority |
|---------|---------|-------|----------|
| HSTS transcript microdata | NCES restricted-use license | Cleanest transcript/test linkage | High if pursuing transcript quantity channel |
| NAEP process data | NCES restricted-use license | Cleanest U.S. process-log data | High if pursuing timing/navigation channel |
| Add Health restricted-use + AHAA | Contract application via UNC | School-based design, sibling sample, transcript ancillary | Medium-high |
| Fragile Families | Princeton OPR archive registration | Urban disadvantage stress-test cohort | Medium |
| ABCD | NDA registration | Neurocognition at ages 9-10 | Medium |
| Project Talent | AIR (currently on hold) | Upper-tail / sibling / twin | Low (access frozen) |
| WLS | Prohibited — terms bar LLM/AI use | Longitudinal Wisconsin | Do not use |

## Best Remaining Datasets (ranked)

1. **Add Health restricted + AHAA** — Nationally representative, school-based, genetically informed sibling sample, long follow-up, official transcript ancillary. Best non-NCES target. Source: [Add Health data access](https://addhealth.cpc.unc.edu/data/)

2. **HSTS restricted microdata** — Cleanest transcript/test linkage. Separates transcript quantity, transcript grades, and tested math without public-use suppression. Source: [NCES transcripts](https://nces.ed.gov/surveys/slsp/transcripts.asp)

3. **NAEP process data** — Cleanest U.S. process-log dataset. Direct test of timing/navigation effects instead of proxies. Source: [NAEP process data](https://www.nationsreportcard.gov/process_data/)

4. **SECCYD** — Public at ICPSR. Repeated child development / achievement structure for stress-testing the early-school node. Source: [ICPSR 21940](https://www.icpsr.umich.edu/web/DSDR/studies/21940)

5. **Fragile Families** — Stress-test cohort for family structure, behavior, urban disadvantage. Public waves via Princeton with replicate weights. Tests "does the wedge survive in a very different family/social environment?" Source: [Princeton FFCWS](https://fragilefamilies.princeton.edu/)

6. **ABCD** — School records + neurocognition (picture vocabulary, processing speed, matrix reasoning, visuospatial). Good for construct-family work at ages 9-10. Source: [ABCD](https://abcdstudy.org/scientists/data-sharing-archive/)

7. **Project Talent** — Best upper-tail / sibling / twin branch if access normalizes. Currently frozen at AIR. Source: [AIR](https://www.air.org/project-talent/researchers)

## Methodology Roadmap

### Core Insight: Separate Surface Families

Stop treating "the gap" as one thing. Formalize into separate measurement surface families:

1. **Applied/reasoning** — problem-solving, novel contexts, spatial
2. **School-knowledge** — curriculum-aligned, taught content, recall
3. **Evaluation/GPA** — teacher assessment, grades, behavioral compliance
4. **Track/quantity** — course-taking, credit accumulation, curriculum intensity
5. **Process/timing** — response time, navigation patterns, item-level behavior

### Mediator Design (DAG-consistent)

Run a real mediation, not more descendant-heavy regression blocks. Stages:

```
Pre-treatment background
    → Measured engagement/compliance
        → School evaluation (GPA, teacher ratings)
            → Transcript exposure (courses, credits)
                → Tested outcomes (standardized tests)
```

Each stage is a separate node in one DAG-consistent design. No conditioning on descendants.

### High-Payoff Experimental Designs

1. **Released-item experiment** — Manipulate: time limit, school framing vs neutral framing, response format, diagram/context burden. If the sex gap moves sharply under those manipulations, that is direct causal leverage on MeasurementSurface.

2. **Blinded grading experiment** — Same student work, randomized male/female names, teacher or evaluator sample. Directly tests the evaluation node instead of inferring it from GPA wedges.

3. **Predictive-validity-by-sex** — Does Math Knowledge predict later STEM/earnings the same way as PIAT or SAT math? Does GPA carry more or less signal than tested math within each sex? Gets to "who cares?" rather than just "who scored higher?"

### Negative Controls

Build deliberately:
- Reading / language (non-math)
- Non-STEM grades
- Teacher recognition unrelated to math

Tests whether the wedge is math-specific or a broader evaluation/compliance phenomenon.

## HS&B Access Notes

- NCES Online Codebook endpoint is broken (HTTP 500, surveyId=25 removed from catalog)
- ICPSR has the data freely available but requires: (1) account, (2) terms acceptance, (3) authenticated download
- Terms acceptance button is React-rendered and does not appear reliably — but direct navigation to download URLs works when logged in
- Study-level download (`/download/spss`) returns the full study bundle (codebooks + data when authenticated)
- Previous unauthenticated downloads returned codebook-only zips

## ICPSR Download Pattern (for future use)

```
https://www.icpsr.umich.edu/web/{archive}/studies/{id}/versions/{version}/download/spss?path=/pcms/studies/{path}/{id_padded}/{version}
```

Where `{path}` is derived from study ID digits: `0/0/7/8` for study 7896.

The download page returns HTML with `<meta http-equiv="refresh" content="...url=https://pcms.icpsr.umich.edu/pcms/performDownload/{uuid}">`. The browser auto-follows this to get the actual zip.
