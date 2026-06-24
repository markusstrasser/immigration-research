# Public data acquisition update for lifetime fiscal modeling

Date: 2026-04-11

## Purpose

This note records which public-use datasets for a replacement lifetime-fiscal model were actually acquired, which were already present locally, and which remain gated or blocked.

## Acquired now

### Census SIPP

Downloaded to:
1. [pu2024_csv.zip](sources/immigration-fiscal/data/external/stage3/census/sipp/pu2024_csv.zip)
2. [2024_SIPP_Release_Notes.pdf](sources/immigration-fiscal/data/external/stage3/census/sipp/2024_SIPP_Release_Notes.pdf)
3. [2024_SIPP_Users_Guide.pdf](sources/immigration-fiscal/data/external/stage3/census/sipp/2024_SIPP_Users_Guide.pdf)
4. [SIPP_Data_Primer_MAY24.pdf](sources/immigration-fiscal/data/external/stage3/census/sipp/SIPP_Data_Primer_MAY24.pdf)

Official sources:
1. https://www2.census.gov/programs-surveys/sipp/data/datasets/2024/pu2024_csv.zip
2. https://www2.census.gov/programs-surveys/sipp/tech-documentation/2024/2024_SIPP_Release_Notes.pdf
3. https://www2.census.gov/programs-surveys/sipp/tech-documentation/methodology/2024_SIPP_Users_Guide.pdf
4. https://www2.census.gov/programs-surveys/sipp/SIPP_Data_Primer_MAY24.pdf

### AHRQ MEPS 2023 Full Year Consolidated File (`HC-251`)

Downloaded to:
1. [h251doc.pdf](sources/immigration-fiscal/data/external/stage3/ahrq/meps/h251doc.pdf)
2. [h251cb.pdf](sources/immigration-fiscal/data/external/stage3/ahrq/meps/h251cb.pdf)
3. [h251su.txt](sources/immigration-fiscal/data/external/stage3/ahrq/meps/h251su.txt)
4. [h251spu.txt](sources/immigration-fiscal/data/external/stage3/ahrq/meps/h251spu.txt)
5. [h251stu.txt](sources/immigration-fiscal/data/external/stage3/ahrq/meps/h251stu.txt)
6. [h251ru.txt](sources/immigration-fiscal/data/external/stage3/ahrq/meps/h251ru.txt)
7. [h251dat.zip](sources/immigration-fiscal/data/external/stage3/ahrq/meps/h251dat.zip)
8. [h251ssp.zip](sources/immigration-fiscal/data/external/stage3/ahrq/meps/h251ssp.zip)
9. [h251v9.zip](sources/immigration-fiscal/data/external/stage3/ahrq/meps/h251v9.zip)
10. [h251dta.zip](sources/immigration-fiscal/data/external/stage3/ahrq/meps/h251dta.zip)
11. [h251xlsx.zip](sources/immigration-fiscal/data/external/stage3/ahrq/meps/h251xlsx.zip)

Official source page:
1. https://meps.ahrq.gov/mepsweb/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-251

## Already present locally

### IRS SOI

Already mirrored on the SSD:
1. `/Volumes/SSK1TB/corpus/irs_soi`
2. size observed this session: about `1.1G`

The SSD copy includes county and other SOI extracts, so re-downloading generic IRS SOI content right now would be wasteful.

## Not acquired as public data file in this pass

### Synthetic SIPP underlying data

What we have:
1. [synthetic_sipp_landing.html](sources/immigration-fiscal/data/external/stage3/census/sipp/synthetic_sipp_landing.html)

Status:
1. the product definitely exists
2. the landing page and documentation are public
3. the actual synthetic data artifact was not exposed as a simple direct public ZIP in this pass
4. some documentation links referenced from the page appear stale or moved

Interpretation:
1. treat this as `exists / needs more careful acquisition` rather than `missing`

### PSID

Status:
1. direct site probe returned a Cloudflare challenge (`403`)
2. that is a site-access issue, not evidence the data do not exist
3. PSID clearly exists and is public-use with registration paths, but this was not a clean direct-download target for unattended `curl`

Official home:
1. https://psidonline.isr.umich.edu/

Interpretation:
1. likely requires browser/session-based acquisition or user registration flow

## Practical next step

The public-use stack now physically staged for us is:

1. `SIPP 2024`
2. `MEPS HC-251`
3. existing local `IRS SOI`

The next acquisition gap is:

1. `PSID`
2. better `Synthetic SIPP` artifact discovery

The next modeling gap is not acquisition but ingestion and schema design.
