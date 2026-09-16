# Dataset Delta 2025-01 → 2026-09 — releases not yet used by this repo

Model self-report: claude-opus-5[1m] (Opus 5, 1M context) — researcher lane `dataset-delta`.

[DATA: HTTP probes of primary agency endpoints, 2026-09-16] [INFERENCE: USED/NOT-USED marking, priority ranking] [SOURCE: URLs inline] [UNVERIFIED: items tagged so]

**Verdict:** **11 material releases verified live in the 2025-01 → 2026-09 window; 10 of them unused by this repo.** The repo's data floor is roughly a year stale on its two load-bearing microdata files (ACS 2023 1-year, CPS ASEC 2025) and two years stale on BJS prisoner counts. The single highest-value item is the **ACS 2020–2024 5-year PUMS** (released 2026-03-05), which is the only public file that can de-noise the small-origin institutionalization cells ladder 74 flags as its stated limit. Two fiscal sources (CBO 61464, Cato) are Cloudflare-blocked and one lane (FBI NIBRS/UCR arrestee ethnicity) has **zero** citations anywhere in `research/` — an entirely unopened source, not merely a stale one.

**Top five by value to current claims**

| # | Release | Exact table / file | Ladder entry it updates |
|---|---|---|---|
| 1 | ACS 2020–2024 5-year PUMS (2026-03-05) | `csv_pus.zip`; `RELSHIPP` GQ-institutional × `ANC1P`/`POBP` × `CIT` | **74** — kills "small Asian-detail cells noisy"; also 65, 68 (state × origin cells) |
| 2 | Rockwool Study Paper 283 (2026-03) | full PDF + data appendix | **72** — that entry says verbatim "summaries read, full paper not" |
| 3 | BJS Prisoners in 2023 (2025-09-30, NCJ 310197) | Tables 5–6 (imprisonment rate by race/Hispanic origin × sex × age), 14–15 (offence × race) | **70** — series currently stops at 2021 |
| 4 | CPS ASEC 2026 + replicate weights (2026) | `asecpub26csv.zip` + `CPS_ASEC_ASCII_REPWGT_2026.ZIP` | **76, 77** — supplies a defensible variance method for the quoted `se 488`; **67** generation counts |
| 5 | BJS Jail Inmates in 2024 (2026-09-08, NCJ 311504) | "inmates held for ICE" table | **65** — the only public lever on the ICE-detention inflation of foreign-born ACS institutional rows |

## Scope
Dataset *releases* dated 2025-01 → 2026-09 bearing on (a) immigrant/second-gen fiscal position,
(b) crime & incarceration by nativity/ethnicity/generation, (c) housing & local costs, US + European
register countries. Marked against `infra/immigration-fiscal/DOWNLOAD_MANIFEST.tsv` (166 rows),
`research/immigration-INDEX.md`, ladder entries 65–78. June-2026 57-dataset roadmap NOT re-listed.

## Repo baseline (what is actually cited today)
[DATA: grep over research/*.md + manifest]
- ACS PUMS **2023 1-year** (42 mentions) — manifest `census/acs_pums_2023_person.zip`. 2024 mentioned 9× (institutional rates, sibling lane).
- CPS ASEC **2024 and 2025** (manifest `external/cps/asec/asec_2025_*.json`). No 2026.
- BJS **Prisoners in 2010/2011/2012/2016/2021/2022**; **SPI 2016**. No Prisoners 2023, no Jail Inmates, no NCVS file.
- NIBRS / UCR: **zero mentions** anywhere in `research/`.
- SIPP 2024, MEPS HC-251, NHIS 2024, HUD SAFMR FY2025, HUD CHAS 2018–2022, NCES CCD 2023-24, OHSS FY2013–2023, ITEP 2024, CBO 60165 + 61256, Pew unauthorized 2025, Rockwool 2026 (**summary pages only — ladder 72 says "full paper not read"**).

## Findings — verified releases

### A. Census microdata (highest value)

**A1. ACS 2020–2024 5-year PUMS — LIVE, NOT USED. [TOP FIND]**
`https://www2.census.gov/programs-surveys/acs/data/pums/2024/5-Year/csv_pus.zip`
Last-Modified **2026-03-05**, 2,273,780,719 B (2.27 GB person) + 952,510,302 B (0.95 GB household).
Also on the API: `https://api.census.gov/data/2024/acs/acs5/pums` (variable `CIT` confirmed present at
`api.census.gov/data/2024/acs/acs1/pums/variables/CIT.json`).
Adds: ~5× the sample of the 1-year file the repo uses, with the same `RELSHIPP`/GQ institutional flag,
`HISPEED`/ancestry (`ANC1P`), `POBP`, `CIT`, `YOEP`. Feeds **ladder 74** directly — that entry's stated
limit is "small Asian-detail cells noisy" (Cambodian/Laotian/Hmong/Vietnamese institutionalization).
5-year PUMS is the only public file that makes those cells non-noisy. Also feeds **ladder 65/68**
(state decomposition CA/TX/other) where 1-year state × origin × institutional cells are thin.

**A2. ACS 2024 1-year PUMS — LIVE since 2025-12-04, partially used.**
`.../pums/2024/1-Year/csv_pus.zip`, 602,847,146 B, Last-Modified **2025-12-04**.
Sibling lane has pulled 2024 institutional rates; the 42 ACS-2023 citations across `research/` are not
yet refreshed. Feeds ladder 65 (ratio series 2010/2019/2023 → add 2024).

**A3. CPS ASEC 2026 (income year 2025) — LIVE, NOT USED (sibling lane active).**
`https://www2.census.gov/programs-surveys/cps/datasets/2026/march/` — confirmed files
`asecpub26csv.zip`, `asec2026_pubuse.dat.gz`, `asec2026_ddl_pub_full.pdf`, plus
`CPS_ASEC_ASCII_REPWGT_2026.ZIP` (replicate weights — the repo's ASEC work has no replicate-weight
standard errors; ladder 76 quotes `se 488` from an unstated variance method).
Feeds ladder 67 (generation counts), 76, 77.

### B. BJS (crime/incarceration)

**B1. Prisoners in 2023 – Statistical Tables — published 2025-09-30, NCJ 310197. NOT USED.**
`https://bjs.ojp.gov/library/publications/prisoners-2023-statistical-tables`
Repo's newest is **Prisoners in 2022**. Feeds **ladder 70** directly: that entry's per-capita
2009→2021 Hispanic/white decomposition stops at 2021; Prisoners 2023 Tables 5–6 (imprisonment rate by
race/Hispanic origin, sex, age) and Table 14/15 (offence by race/Hispanic origin, sentenced state
prisoners) extend it two years and re-state 2022 on the current basis. **Restatement trap applies**
(memory: BJS 2010→2011 Hispanic violent restatement) — must re-read 2021/2022 rows out of the 2023
report, not the older ones.

**B2. Jail Inmates in 2024 – Statistical Tables — published 2026-09-08, NCJ 311504. NOT USED.**
`https://bjs.ojp.gov/library/publications/jail-inmates-2024-statistical-tables`
Eight days old. Jail Inmates in 2023 also live and unused. Jails hold the ICE-detainee population that
ladder 65 flags as inflating foreign-born ACS institutional rows; the jail series carries
"held for ICE" counts, which is the only public lever on that bias.

**B3. Criminal Victimization, 2024 (NCVS) — published 2025-09-29, NCJ 310547. NOT USED.**
`https://bjs.ojp.gov/library/publications/criminal-victimization-2024`
Feeds **ladder 78**, which reconciles "NCVS 1.37× vs arrest 2.8×" using older NCVS offender-perception
tables. CV-2024 refreshes the offender race/ethnicity perception tables on the current sample.

**B4. Survey of Prison Inmates 2024 — NO landing page (404). [GAP]**
`bjs.ojp.gov/library/publications/survey-prison-inmates-2024` → 404. SPI 2016 remains the only vintage
and **SPI is the sole US source with inmate nativity**. Fielding status unverified.

**B5. Census of State and Federal Adult Correctional Facilities 2024 — 404 at the guessed slug. [GAP]**

### C. Europe

**C1. Rockwool Study Paper 283 — full PDF located, March 2026. NOT USED (summaries only).**
`https://rockwoolfonden.s3.eu-central-1.amazonaws.com/wp-content/uploads/2026/03/RF_Study-paper_283_A-Statistical-Decomposition-of-Nativity-Gaps-in-Criminal-Convictions-Using-Full-Population-Data-from-Five-Developed-Democracies_March2026.pdf`
**Ladder 72 explicitly says "summaries read, full paper not."** This closes that gap with one download.

**C2–C5 (live endpoints, vintage not yet pinned):** Statistics Denmark STRAFNA1 (statbank.dk/STRAFNA1,
200), Brå misstänkta personer (bra.se/statistik/kriminalstatistik/misstankta-personer.html, 200 — note
the repo memo's old `statistiska-undersokningar/` path now 404s), SSB Straffereaksjoner (200), Destatis
Migration-Integration (200), Eurostat `crim_off_cat` databrowser (200), BKA PKS 2025 (200, published
spring 2026 — ladder 73 reproduces **PKS 2024**). [UNVERIFIED: exact reference years of C2–C5.]

### D. Blocked / bot-walled
- **CBO 61464** (2025 state/local surge report): `cbo.gov` returns **403 Cloudflare**. Matches memory
  (`politicized-stats-lane-d-sources`: cbo.gov JS-gated). Needs `agent-browser`.
- **Cato fiscal-impact ledger**: `cato.org` **403 Cloudflare bot-management**. Memory says agent-browser
  does *not* beat Cloudflare bot-management. Route via Wayback `id_` or ask for a pasted PDF.

## Release table

| Release | Date | URL | Used? | Feeds |
|---|---|---|---|---|
| ACS 2020–2024 5-year PUMS | 2026-03-05 | www2.census.gov/…/acs/data/pums/2024/5-Year/csv_pus.zip | **NO** | ladder 74, 65, 68 |
| ACS 2024 1-year PUMS | 2025-12-04 | …/pums/2024/1-Year/csv_pus.zip | partial (sibling lane) | ladder 65 |
| CPS ASEC 2026 (IY2025) | 2026 | www2.census.gov/…/cps/datasets/2026/march/ | **NO** (sibling lane active) | ladder 67, 76, 77 |
| CPS ASEC 2026 replicate weights | 2026 | …/march/CPS_ASEC_ASCII_REPWGT_2026.ZIP | **NO** | ladder 76 SEs |
| BJS Prisoners in 2023 | 2025-09-30 | bjs.ojp.gov/library/publications/prisoners-2023-statistical-tables | **NO** | ladder 70 |
| BJS Jail Inmates in 2023 | 2025 | …/jail-inmates-2023-statistical-tables | **NO** | ladder 65 |
| BJS Jail Inmates in 2024 | 2026-09-08 | …/jail-inmates-2024-statistical-tables | **NO** | ladder 65 |
| BJS Criminal Victimization 2024 (NCVS) | 2025-09-29 | …/criminal-victimization-2024 | **NO** | ladder 78 |
| Rockwool Study Paper 283 (full) | 2026-03 | rockwoolfonden.s3…/2026/03/RF_Study-paper_283_….pdf | **NO** (summaries only) | ladder 72 |
| Statistics Denmark STRAFNA3 / STRAFNA4 | updated 2026-04-08, data thru **2025** | api.statbank.dk/v1/tableinfo/STRAFNA3 | **NO** (repo repro uses earlier years) | ladder 73 |
| BKA PKS 2025 | spring 2026 | bka.de/…/PKS2025/pks2025_node.html | **NO** (ladder 73 reproduces PKS 2024) | ladder 73 |
| DHS OHSS unauthorized-population page | live, **retitled "Illegal Aliens"** | ohss.dhs.gov/topics/immigration/unauthorized-immigrants | **NO** | ladder 77 denominators |

Verified as *not* newly released: **Survey of Prison Inmates 2024** (404 — SPI 2016 remains the only US
source with inmate nativity) and **Census of State and Federal Adult Correctional Facilities 2024** (404).

## Acquisition queue (priority order)

1. **ACS 2020–2024 5-year PUMS person file** — 2.27 GB zip (~20 GB expanded CSV). Plain HTTPS, no key.
   **Disk preflight required** (>10 GB after extraction; `df -h` the target, 1.5× rule). Or pull cells via
   the Census API (`api.census.gov/data/2024/acs/acs5/pums`, `CENSUS_API_KEY` already in `config.local.env`)
   and skip the bulk download entirely — preferred route for the ladder-74 cells.
2. **Rockwool Study Paper 283 PDF** — a few MB, direct S3, no auth. One `curl`. Closes ladder 72 outright.
3. **BJS Prisoners in 2023** — ~4 MB PDF + CSV table pack from the landing page. No auth.
4. **CPS ASEC 2026 `asecpub26csv.zip` + `CPS_ASEC_ASCII_REPWGT_2026.ZIP`** — coordinate with the
   `ledger-asec2026` lane so the replicate weights are not pulled twice.
5. **BJS Jail Inmates in 2024 + 2023** — small PDFs; extract the held-for-ICE rows only.
6. **Statistics Denmark STRAFNA3/STRAFNA4 through 2025** — free JSON via
   `api.statbank.dk/v1/data/STRAFNA3/JSONSTAT`, no key, kilobytes. Extends the ladder-73 Denmark
   reproduction by one to two reference years.

## Gaps
- [GAP] FBI CDE NIBRS 2024 arrestee-ethnicity download URL not yet resolved (the `/LATEST/webapp/` page is
  a JS shell; the guessed S3 path 404s). Repo has **zero** NIBRS/UCR citations — a whole unused lane.
- [GAP] **CJARS** `cjars.isr.umich.edu/data/` returns **403 "Just a moment…"** (Cloudflare). JOE 2024
  vintage unverified.
- [GAP] OHSS page is live and **retitled "Illegal Aliens"** (a 2025–26 rename; the old
  `unauthorized-immigrant-population` slug 404s). The estimate's reference-year vintage was not read.
- [GAP] Opportunity Insights `/data/`, IPUMS `full_count.shtml`, Add Health `/data/`, NLSY97 index all
  return 200, but their page text was not parsed (a `ugrep` Unicode-complexity error killed three
  extractions). 1950 full-count / Wave VI / round 21 status therefore **unverified, not absent**.
- [GAP] ITEP 2025 and Manhattan Institute 2025 slugs guessed and 404'd; AEI Sept 2025 not probed.
  Absence here is a failed slug guess, **not** evidence of no release.
- [GAP] Exact reference years for Brå, SSB, Destatis and Eurostat `crim_off_cat` endpoints (all 200,
  none parsed). Only Statistics Denmark was pinned (2025).
- [GAP] CILS-4 not probed.

Next queries if re-dispatched (in order): (1) FBI CDE bulk-download JSON behind
`cde.ucr.cjis.gov/LATEST/webapp/` via `agent-browser` — `api.usa.gov/crime/fbi/cde/...` returns 403
without a key, and NIBRS arrestee ethnicity is a wholly unopened lane; (2) re-parse the four 200-OK
pages (OI, IPUMS full-count, Add Health, NLSY97) with `sed`+`grep -a` rather than `ugrep` regex;
(3) `web.archive.org/web/2026/id_/cbo.gov/publication/61464` for the Cloudflare-blocked CBO surge
report; (4) site-search ITEP and Manhattan Institute rather than guessing slugs; (5) Brå/SSB/Destatis
reference years via their statistics-bank APIs, mirroring the STRAFNA3 pattern that worked.

## Audit trail
All findings above are HTTP-probe results captured 2026-09-16 (status code, `Last-Modified`,
`Content-Length`, page `<title>`, and for BJS the on-page `Publication Date`). No file was downloaded
and nothing in the repo was modified outside this directory.
