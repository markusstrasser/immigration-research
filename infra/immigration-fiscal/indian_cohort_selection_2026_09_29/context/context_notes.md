claude-opus-5-5
**Verdict:** Items 1–3 and 5 are confirmed from archived primary files. (1) Encounters with Indian citizens rose from 19,883 (FY20) to a 96,917 peak (FY23), then fell to 90,415 (FY24) and 34,146 (FY25); southwest border USBP went 1,092 → 41,719 → 4,962 and northern border USBP peaked at 14,197 (FY24); FY19 is a [GAP] on this basis. (2) India-born unauthorized estimates: DHS 470k (2015) → 540k (2018) → 220k (2022) after the ADIS method change; Pew 680k (2023); MPI does not list India (Asia 851k). (3) India's share of H-1B approvals rose from 36.5% (FY03) to 70–76% (FY14–25); among all approvals the master's share rose from 31–37% to 54–58% and the median wage from $53k to $133k nominal; there is no cross-tab by country of birth. (4) LCA wage levels, shares of certified H-1B cases at Level I / II: the six outsourcers had 23% / 61% in FY15, 1.8% / 72% in FY19 and 0.9% / 60% in FY24, against 50% / 32%, 17% / 51% and 20% / 44% for all other employers. (5) GMAT and GRE origin pools are extracted (India's GMAT mean exceeds the US mean in every year); an older GRE snapshot is a [GAP]. (6) Flows FY2015–25 are in flows_2015_2025.csv: India-born LPRs 64k (FY15) → 127k (FY22) → 67k (FY24), with EB principals 8–44k; active SEVIS records 247k (2017) → 422k (2024); FY2024 I-94 admissions H-1B 497k and F-1 299k; FY2019 CBP encounters remain a [GAP].

# Context for Indian cohort selection lane — primary-source notes

Provenance: [DATA] primary files archived under `../_cache/context/` (sha256 recorded per item) · [SOURCE: urls per item] · [INFERENCE] only where marked · [UNVERIFIED] none yet.

Scope: origin-flow context (CBP encounters, unauthorized estimates, H-1B characteristics, LCA wage levels, origin test-taker pools). Encounters are events, not persons.

## Findings

- [PENDING] item 1 CBP encounters, citizenship India, FY2019–FY2025
- [PENDING] item 2 unauthorized India-born estimates (DHS OHSS, Pew, MPI)
- [PENDING] item 3 USCIS H-1B characteristics reports
- [PENDING] item 4 DOL OFLC LCA wage levels, IT outsourcers vs all
- [PENDING] item 5 GMAT/GRE origin test-taker pools


## Item 1 — CBP encounters, citizenship = INDIA (appended 2026-09-29, after the 22:27:31 JST `date` call) [DATA]

Encounters are events (USBP Title 8 apprehensions + Title 42 expulsions; OFO inadmissibles + expulsions), not unique persons; repeat crossers count more than once.

Sources [SOURCE: https://www.cbp.gov/newsroom/stats/nationwide-encounters]:
- `sources/immigration-fiscal/data/external/cbp/nationwide-encounters-fy22-fy25-aor.csv` (cbp.gov/sites/default/files/2025-11/…; local copy, sha256 c1a59b8a2a907fc9d254c6ad9bcbca94d2909d7a3a363cc08350dc6f9ecb098e) → FY2022–FY2025
- `_cache/context/ne-fy20-fy23-aor.csv` (https://www.cbp.gov/sites/default/files/assets/documents/2023-Nov/nationwide-encounters-fy20-fy23-aor.csv, retrieved 2026-09-29, 6,829,687 bytes = Content-Length, sha256 72247230c909cd0aa3fd24fbf1ef15635d6281d372bec65021a66856e96a7532) → FY2020–FY2021
- cross-check `sources/.../nationwide-encounters-fy21-fy24-aor.csv` (sha256 419c8b2c…1a1a): overlapping FYs match exactly across all three releases (FY2021 30,662; FY2022 63,927; FY2023 96,917).
- Script `context/cbp_india.py` → `context/cbp_india_encounters_fy2020_2025.csv` (FY × region × component) and `context/cbp_india_encounters_summary.csv`. [CALCULATION]

| FY | total | SW land border | of which USBP | Northern land border | of which USBP | Other (air/sea ports, OFO) | all USBP | all OFO |
|---|---|---|---|---|---|---|---|---|
| 2020 | 19,883 | 1,120 | 1,092 | 3,128 | 129 | 15,635 | 1,227 | 18,656 |
| 2021 | 30,662 | 2,588 | 2,555 | 2,225 | 42 | 25,849 | 2,598 | 28,064 |
| 2022 | 63,927 | 18,308 | 18,236 | 17,331 | 237 | 28,288 | 18,480 | 45,447 |
| 2023 | 96,917 | 41,770 | 41,719 | 30,010 | 1,630 | 25,137 | 43,358 | 53,559 |
| 2024 | 90,415 | 25,616 | 25,529 | 43,764 | 14,197 | 21,035 | 39,734 | 50,681 |
| 2025 | 34,146 | 5,047 | 4,962 | 14,054 | 1,580 | 15,045 | 6,551 | 27,595 |

Longer back series (different construct: USBP + ICE apprehensions, no OFO inadmissibles) — DHS OHSS Yearbook 2020 Table 34 "Noncitizens Apprehended by Region and Country of Nationality: Fiscal Years 2011 to 2020" [SOURCE: https://ohss.dhs.gov/topics/immigration/yearbook/2020/table34], archived `_cache/context/yb2020_t34.html` (retrieved 2026-09-29, sha256 75c9541c818b7e6c47e468aa96e35dc705f969ac9dcbbce59b99f5a4aa00699c). Row as parsed from the HTML table: `['India', '3,859', '1,566', '1,791', '2,106', '2,967', '4,123', '3,682', '9,953', '8,926', '1,717']` for FY2011…FY2020. Table note: "USBP data are current as of October 2020. ICE ERO data are current as of October 2020." ICE ERO counting was revised for 2016 onward (footnote). So FY2019 India apprehensions (USBP+ICE) = 8,926; FY2018 = 9,953.

[GAP] FY2019 on the CBP nationwide-encounters basis (OFO+USBP by citizenship). Tried: guessed cbp.gov paths for `nationwide-encounters-fy19-fy22-aor.csv` / `fy18-fy21` (2021-Oct/Nov, 2022-Sep/Oct/Nov/Dec: all 404); Wayback CDX wildcard (504 timeout); Wayback snapshots of the nationwide-encounters page 2021-12 and 2022-12 carry no CSV links (data portal only). Next: Wayback CDX on `cbp.gov/sites/default/files/assets/documents/2022-*` prefixes, or the USBP "Nationwide Apprehensions by Citizenship and Sector FY2007–FY2019" PDF (URL guess failed on DNS; not retried).

## Item 2 — Unauthorized India-born population estimates (appended 2026-09-29, before the 22:33:03 JST `date` call) [DATA]

All three producers use residual methods on Census survey data (foreign-born minus estimated legal residents); India is the country where the residual is most sensitive to the nonimmigrant (H-1B/F-1/H-4 and dependants) count, and the producers disagree by ~3x for the same years. [INFERENCE on the "most sensitive" point, grounded in OHSS's own caveats quoted below]

| Producer / edition | Reference date | India-born unauthorized | Method one-liner | Evidence line (pdftotext -layout) |
|---|---|---|---|---|
| DHS OIS, Baker, "Illegal Alien Population … January 2015" (Dec 2018) | 2010-01 / 2015-01 | 270,000 / 470,000 | ACS residual; nonimmigrants from I-94 | `India. . . .  470,000  4  270,000  2  76` (Table 2, cols 2015 n, %, 2010 n, %, % increase) |
| DHS OIS, Baker, "… January 2015–January 2018" (Jan 2021) | 2015-01 … 2018-01 | 450,000 / 560,000 / 490,000 / 540,000 | ACS residual | `India . . .  450,000  560,000  490,000  540,000` (Table 2, 2015–2018) |
| DHS OHSS, Baker & Warren, "… January 2018–January 2022" (Apr 2024) | 2018-01 (revised) / 2019 / 2020 / 2022 | 480,000 / 390,000 / 340,000 / 220,000 | ACS residual; legally resident nonimmigrants now from ADIS (entry-exit) records — "a methodological change from previous editions" | `India  480,000  390,000  340,000  220,000`; text: "The Indian population fell by 54 percent, or 260,000 people, from 480,000 in 2018 to 220,000 in 2022" |
| same, Table A2-1 (revised historical series, thousands) | 2000, 2005–2020, 2022 | 2000 120; 2005 280; 2006 210; 2007 220; 2008 160; 2009 200; 2010 200; 2010* 270; 2011 240; 2012 260; 2013 320; 2014 390; 2015 470; 2015** 450; 2016 560; 2017 490; 2018 540; 2018** 480; 2019 390; 2020 340; 2022 220 | * = revised to 2010 Census; ** = "Revised to show the impact of the updated methodology" | line 777 `India 120 280 210 220 160 200 200 270 240 260 320 390 470 450 560 490 540 480 390 340 220` under header line 757 |
| Pew Research, Passel & Krogstad, "U.S. Unauthorized Immigrant Population Reached a Record 14 Million in 2023" (Aug 21 2025) | 2023 | 680,000 | "Pew Research Center estimates based on augmented U.S. Census Bureau data (IPUMS)" (residual on augmented ACS/CPS) | `India (680,000)` in the top-countries sidebar; text: "El Salvador, India, China and the Philippines are the only countries to show no significant change in their U.S. unauthorized immigrant populations between 2021 and 2023 (among countries with more than 150,000 …)" |
| MPI Data Hub, "Profile of the Unauthorized Population: United States" | 2023 (pooled 2019–23 ACS) | India not shown (top 5 only: Mexico … Venezuela 486,000). Asia region total = 851,000 (6%) of 13,738,000 | ACS+SIPP status imputation weighted to Van Hook control totals | `Regions of Birth … Asia 851,000 6%` |

Caveat quoted from OHSS Jan-2015 edition (Table 3 footnote): "The estimated increases for India and China for 2014 to 2015 may overstate actual growth in these populations (see Appendix 2). India and China both exhibited rapid increases in nonimmigrant admissions during this period …; coupled with changing trends in nonimmigrant visit lengths and/or an increasing number of tourists being reported as 'resident,' these developments may have caused inflation in the estimated illegal alien …". Same edition: Asia's growth 2010–2015 "was driven primarily by an increase of about 40,000 people per year from India."

Files (all retrieved 2026-09-29 unless local):
- local `sources/immigration-fiscal/data/external/ohss/ohss_unauth_2018_2022.pdf` sha256 ae61e88ab0b5af76684c228580ae58a275335f8ef73528399b9cbf31bf810e88 [SOURCE: https://www.dhs.gov/sites/default/files/2024-05/2024_0418_ohss_estimates-of-the-unauthorized-immigrant-population-residing-in-the-united-states-january2018%E2%80%93january-2022.pdf]
- `_cache/context/ohss_unauth_2015_2018.pdf` sha256 489d46569bab42bb2561f171bbe97b6373ec0b5c0e7261b509d99d68dbf44a5d [SOURCE: https://ohss.dhs.gov/sites/default/files/2023-12/unauthorized_immigrant_population_estimates_2015_-_2018.pdf]
- `_cache/context/ohss_unauth_2015.pdf` sha256 82f929c934af908578b20d6804fbe153e408709453471ef03915c9053c3638d9 [SOURCE: https://ohss.dhs.gov/sites/default/files/2023-12/18_1214_PLCY_pops-est-report.pdf]
- local `sources/immigration-fiscal/data/pew/pew-unauthorized-immigrants-2025.pdf` sha256 dbce5b81bc65e8f4dacc98df17f5943242b107861d20e716f4ce4162efd06b2b (byte-identical to `external/pew/pew_unauth_2023.pdf`) [SOURCE: https://www.pewresearch.org/race-and-ethnicity/2025/08/21/u-s-unauthorized-immigrant-population-reached-a-record-14-million-in-2023/]
- `_cache/context/mpi_unauth_us.html` sha256 e43aa5670ff67007c2abf536da66951fe0e07060c55d6126a5453cff37ef00a1 — Wayback id_ snapshot 20260625094157 of https://www.migrationpolicy.org/data/unauthorized-immigrant-population/state/US (live site 403s curl).

[GAP] Pew country tables for India before 2023 (e.g. 2017, 2021) not fetched; Pew's interactive/appendix tables not in the local PDF. [GAP] MPI India-specific unauthorized count: not published on the US profile (top-5 only). Older OHSS editions (Jan 2005–2014, listed at https://ohss.dhs.gov/topics/immigration/illegal/population-estimates) not fetched; Table A2-1 supersedes them as the revised series.

## Item 3 — USCIS "Characteristics of H-1B Specialty Occupation Workers", FY2003–FY2025 (appended 2026-09-29 22:33:33 JST) [DATA] [CALCULATION]

Source list: https://www.uscis.gov/tools/reports-and-studies (links scraped 2026-09-29); PDFs under `_cache/context/h1b/fyNN.pdf` (URL pattern https://www.uscis.gov/sites/default/files/document/{reports,data}/…; exact paths in `context/h1b_characteristics.py` history and below), full sha256 in `context/h1b_reports_sha256.txt`. FY2006–FY2009 and FY2015–FY2016 reports are image-only → OCR with tesseract 300 dpi (`_cache/context/h1b/ocr.sh`, `fyNN.ocr.txt`); every other value is from `pdftotext -layout`. No FY2010 report on the page (h1b-fy-10-characteristics.pdf 404); FY2010 values come from the two-year tables in the FY2011 report. Script: `context/h1b_characteristics.py` → `context/h1b_characteristics_fy2003_2025.csv` (each row carries report + quoted line).

Unit: approved petitions (initial + continuing), not persons; one person can have several approvals in a year. "Initial" = new employment (cap-subject and cap-exempt). Education and median compensation are for ALL approved beneficiaries (no country-of-birth cross-tab in any report checked); India is 44–76% of approvals, so they are an India-dominated proxy, not India-specific. Compensation is nominal.

| FY | India approved n (% of all) | India initial n (%) | Bachelor / Master / Doctorate / Professional % | Median comp (nominal $) |
|---|---|---|---|---|
| 2003 | 79,166 (36.5) | 29,269 (27.8) | 50 / 31 / 12 / 6 | — |
| 2004 | 123,567 (43.0) | 60,062 (46.0) | 49 / 34 / 11 / 5 | 53,000 |
| 2005 | 118,520 (44.4) | 57,349 (49.0) | 45 / 37 / 5 / 12 (as printed; D/P likely swapped) | 55,000 |
| 2006 | 135,329 (49.9) | 59,612 (54.4) | 45 / 39 / 11 / 5 | 60,000 |
| 2007 | 147,559 (52.4) | 66,504 (55.4) | 44 / 40 / 10 / 5 | 60,000 |
| 2008 | 149,629 (54.2) | 61,739 (56.5) | 43 / 41 / 11 / 5 | 60,000 |
| 2009 | 103,059 (48.1) | 33,961 (39.4) | 41 / 40 / 13 / 6 | 64,000 |
| 2010 | 102,911 (53.3) | 34,617 (45.2) | 42 / 39 / 12 / 6 | 68,000 (derived: "$70,000 in FY 2011, $2,000 more than in FY 2010") |
| 2011 | 156,317 (58.0) | 55,972 (52.6) | 41 / 42 / 11 / 5 | 70,000 |
| 2012 | 168,367 (64.1) | 86,477 (63.2) | 46 / 41 / 8 / 4 | 70,000 |
| 2013 | 187,270 (65.3) | 81,992 (63.9) | 45 / 41 / 9 / 5 | 72,000 |
| 2014 | 220,286 (69.7) | 82,263 (66.2) | 45 / 43 / 8 / 4 | 75,000 |
| 2015 | 195,247 (70.9) | 71,263 (62.7) | 45 / 44 / 7 / 3 | 79,000 |
| 2016 | 256,226 (74.2) | 70,737 (61.8) | 44 / 45 / 7 / 3 | 82,000 |
| 2017 | 276,423 (75.6) | 67,815 (62.7) | 45 / 44 / 7 / 3 | 85,000 |
| 2018 | 243,994 (73.4) | 51,353 (54.9) | 37 / 52 / 7 / 3 | 95,000 |
| 2019 | 278,491 (71.7) | 79,423 (57.2) | 36 / 54 / 8 / 3 | 98,000 |
| 2020 | 319,494 (74.9) | 73,717 (60.0) | 35.7 / 54.2 / 7.0 / 3.0 | 101,000 |
| 2021 | 301,616 (74.1) | 75,858 (61.5) | 33.7 / 56.6 / 6.8 / 2.9 | 108,000 |
| 2022 | 320,791 (72.6) | 77,673 (58.7) | 43.1 / 42.3 / 10.3 / 4.2 among known (26% unknown) | 118,000 |
| 2023 | 279,386 (72.3) | 68,825 (57.9) | 50.1 / 32.8 / 11.8 / 5.2 among known (32% unknown) | 118,000 |
| 2024 | 283,755 (71.0) | 80,449 (57.0) | 36.5 / 50.8 / 8.9 / 3.8 among known (10% unknown) | 120,000 |
| 2025 | 284,106 (69.9) | 57,747 (50.3) | 30.5 / 57.5 / 8.1 / 3.7 (unknown <1%) | 133,000 |

Quoted lines (samples; full set in the CSV): FY2004 `India  79,166  123,567  29,269  60,062  49,897  63,505` under header `FY 2003 FY 2004 FY 2003 FY 2004 FY 2003 FY 2004` (all / initial / continuing); FY2019 report `India  278,491  243,994  79,423  51,353  199,068  192,641` under `FY 2019 FY 2018 …` (column order flips to current-first from the FY2018 report on); FY2025 `Median annual compensation for all approved H-1B beneficiaries in FY 2025 was $133,000.`; FY2022 text: "31.1 percent … master's degree, 31.7 percent … bachelor's degree, 7.6 percent … doctorate, 3.1 percent … professional degree, and 26 percent had an unknown level of education."

Reading [INFERENCE]: the master's share of H-1B approvals rose from ~31–37% (FY2002–05) to ~54–58% (FY2019–21, FY2025), bachelor's fell from ~50% to ~31–36%, while India's share of approvals rose from 37% to ~70–76%. On this proxy the dominant (India-heavy) H-1B inflow became MORE credentialed after ~2017, not less; the FY2018 jump coincides with the FY2019 cap-selection reorder / heightened scrutiny of outsourcers (policy attribution [UNVERIFIED]). The FY2022–FY2023 dips are an artefact of the unknown-education share, which falls disproportionately on master's rows (published master's % of all = 31.1 and 22 vs 54–58 in adjacent clean years).

[GAP] India-specific education / compensation: not tabulated in these reports; would need the USCIS H-1B petition microdata (I-129 microdata via FOIA [UNVERIFIED pointer]) or the H-1B Employer Data Hub joined to employer origin mix. [GAP] FY2010 report PDF not on the USCIS page.

## Item 4 — DOL OFLC LCA wage levels (appended 2026-09-29 22:38:08 JST) [GAP — partial, unverified]

dol.gov returns 403 to curl (Akamai) for both the performance page and the xlsx files. The Wayback `id_` route works: e.g. https://web.archive.org/web/20260114000148id_/https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/H-1B_Disclosure_Data_FY15_Q4.xlsx (150,875,842 bytes, fetched 2026-09-29 to `_cache/context/lca/`). Sizes (HEAD): FY2019 `H-1B_Disclosure_Data_FY2019.xlsx` 283,205,898 bytes; FY2024 `LCA_Disclosure_Data_FY2024_Q4.xlsx` 83,056,843 bytes (FY2024 is published as four separate quarterly files). A detached downloader (`_cache/context/lca/fetch.sh`, log `fetch.log`) was still fetching FY2019 and FY2024 Q1–Q4 when this epoch ended. Script `context/lca_wage_levels.py <label> <xlsx…>` (polars+fastexcel/calamine; certified H-1B LCAs; wage-level I–IV shares by cases and by worker positions; six outsourcers matched by employer-name regex: INFOSYS, TATA CONSULTANCY, COGNIZANT, WIPRO, HCL AMERICA/TECHNOLOGIES/GLOBAL, TECH MAHINDRA) was launched on FY2015 (`_cache/context/lca/run_fy15.sh`, log `run_fy15.log`); it appends to `context/lca_wage_levels.csv` and prints the columns it chose, the file sha256 and the status/visa/level value counts to the log.
[GAP] No wage-level numbers are confirmed in these notes. Before using any `lca_wage_levels.csv` row, read `run_fy15.log`: check that the column picks are right (wage-level column name differs by year), the rc is 0, and the value counts are what you expect. Then run `uv run --no-project --with polars --with fastexcel python3 context/lca_wage_levels.py FY2019 _cache/context/lca/H-1B_Disclosure_Data_FY2019.xlsx` and the FY2024 run with the four quarterly files, once `fetch.log` shows ALLDONE. Check the regex captures too: HCL's employer-name variants are not verified, and Cognizant files as "Cognizant Technology Solutions US Corp".

## Item 5 — Origin test-taker pools (NOT immigrant scores) (appended 2026-09-29 22:38:08 JST) [DATA]

These are people who hold Indian or US citizenship and took the test (for the GRE Table 3.1 volumes, people who tested in the country). They are self-selected applicant pools, not immigrants and not population samples. Score scales are not comparable across GMAT editions: the 10th Edition was used until Feb 2024 and GMAT Focus after.

GMAC "Profile of GMAT Testing: Citizenship" (testing year TY = July–June; e.g. TY2014 = 1 Jul 2013–30 Jun 2014):
| Report | Row | TY columns | India | United States |
|---|---|---|---|---|
| TY2010–TY2014 (Nov 2014) [SOURCE: https://www.gmac.com/-/media/files/gmac/research/gmat-test-taker-data/gmat-profile-citizenship-ty2010-14.pdf] sha256 b578b830…a979 | Exams taken | 2010–2014 | 26,937 · 25,394 · 30,213 · 25,268 · 28,325 | 127,061 · 116,546 · 117,511 · 90,541 · 87,110 |
| same | Mean score | 2010–2014 | 578 · 581 · 582 · 577 · 576 | 533 · 531 · 533 · 532 · 537 |
| TY2016–TY2020 (Feb 2021) [SOURCE: …/profile-of-gmat-testing-citizenship-ty2016-2020.pdf] sha256 7c604221…77b2 | Exams taken | 2016–2020 | 33,046 · 32,514 · 32,425 · 30,590 · 26,129 | 83,186 · 79,746 · 73,556 · 63,945 · 45,648 |
| same | Mean total score | 2016–2020 | 577 · 583 · 583 · 578 · 579 | 547 · 553 · 556 · 558 · 563 |
| TY2020–TY2024 (Oct 2024) [SOURCE: …/profile-of-gmat-testing-citizenship-ty2020-ty2024.pdf] sha256 70f78a23…8746 | Mean total score (10th Ed.) | 2020–2024, then TY2024 Focus | 579 · 604 · 595 · 586 · 586 · Focus 566 | 563 · 587 · 576 · 585 · 599 · Focus 558 |
Quoted lines: `India … Mean Score 578 581 582 577 576` and `United States … Mean Score 533 531 533 532 537` (TY2010–14); `Mean Total Score 577 583 583 578 579` (India, TY2016–20).

ETS, "A Snapshot of the Individuals Who Took the GRE General Test, July 2020–June 2025" [SOURCE: https://www.ets.org/pdfs/gre/snapshot.pdf], sha256 650d5b66cec023bee12ead7aba999ce408937505b90067c5613ef3deb4344a2c. Its scores cover people who tested between 1 Jul 2024 and 30 Jun 2025. Table 1.6, by country of citizenship (N, Verbal mean/SD, Quant mean/SD, AW mean/SD):
- `India 34,477 151.0 8.6 158.6 8.8 3.3 0.7`
- `United States of America 80,508 152.8 8.0 151.3 8.7 3.8 0.8`
Table 3.1 gives examinees by country where tested, 2020–21 → 2024–25. United States: 214,441 · 152,618 · 122,997 · 104,034 · 95,077. India: 66,326 · 111,476 · 110,512 · 59,133 · 31,677.
[GAP] An older GRE snapshot (for example 2013–14 or 2016–17) for the "years apart" comparison. The guessed ets.org /s/gre/pdf/snapshot_test_taker_data_{2014,2016,2018}.pdf paths all return 404, and the Wayback availability API returned 429. Next step: Wayback CDX on `ets.org/s/gre/pdf/*snapshot*`.

### Item 4 addendum — FY2015 run finished (appended 2026-09-29 22:38:31 JST) [DATA] [CALCULATION]
`run_fy15.log`, rc=0. Columns chosen: CASE_STATUS, VISA_CLASS, EMPLOYER_NAME, PW_WAGE_LEVEL, "TOTAL WORKERS". 618,804 rows. xlsx sha256 72b06426f1c22b6bd2108b4ff96431bd51b6e6bf17d826ae676cf07bf967ff90. Status counts: CERTIFIED 547,278, CERTIFIED-WITHDRAWN 41,071, WITHDRAWN 19,472, DENIED 10,983. Level values: Level I 271,921, II 211,360, III 67,087, IV 39,728, missing 28,708.

FY2015, certified H-1B LCAs, wage-level shares among cases with a level (I / II / III / IV):
- All employers: 536,693 cases, 4.2% with no level. 46.0 / 36.3 / 11.3 / 6.4
- Six outsourcers: 76,702 cases. 23.1 / 60.9 / 12.5 / 3.6
- All other employers: 459,991 cases. 50.0 / 32.0 / 11.1 / 6.9
- Tech Mahindra is 98.7% Level II; HCL is 16.7 / 49.0 / 26.3 / 8.0.

Per-employer rows and worker-weighted shares are in `context/lca_wage_levels.csv`.

[INFERENCE] The outsourcers are not concentrated at Level I. They cluster at Level II, while other employers file more Level I, which is partly new US graduates on OPT and H-1B. So the wage level alone does not show that the outsourcers hire less-skilled workers.

[GAP] FY2019 and FY2024 are not run yet; the downloads were still in progress.

## Item 6 — last-10-years flow sources, FY2015–FY2025, India (stub 2026-09-29 23:15:37 JST) [DATA]

- Sub-items (a), (b), (c), (d), (e) and the LCA FY2019/FY2024 runs are appended below; tidy rows are in `context/flows_2015_2025.csv`.

### 6(a) LPRs born in India by class, FY2015–FY2024 (appended 2026-09-29 23:18:58 JST) [DATA]

Sources: DHS Yearbook Table 10 "Persons Obtaining Lawful Permanent Resident Status by Broad Class of Admission and Region and Country of Birth", one file per FY. FY2015–2023 are the local copies in `admission_route_2026_09_21/_cache` (URL and sha256 per year in its `acquire_manifest.json`, e.g. https://ohss.dhs.gov/sites/default/files/2023-12/YRBK%25202015%2520LPR%2520Excel%2520Final_2.zip). FY2024 is `indian_ledger_2026_09_18/_cache/yearbook_lpr_fy2024.xlsx`, whose download URL is [UNVERIFIED] (not recorded locally); from FY2024 on, cells are rounded to 10. The EB principal/derivative split (*) comes from the OHSS special tabulation "LPRs by country of birth and major classes of admission", FY2005–2024 (`late_arrival_tail_2026_09_27/_cache/2026_0604_ohss_lpr_by_country_by_major_class_and_deriv_emp-based_fy2005-2024.xlsx`, sha256 cf0e8367…9769, [SOURCE: https://ohss.dhs.gov/topics/immigration/lawful-permanent-residents/lprs-country-birth-and-major-classes-admission]). Its cells are rounded to 10; derivatives = the "Restricted to Spouses and Children" sheets; principals = the EB1–5 total minus derivatives [CALCULATION]. Cross-check: special-tab EB total for FY2022 is 96,340 vs Table 10 96,335; FY2021 is 75,330 vs 75,332. Per-row file, quoted India row and sha256 are in `context/flows_2015_2025.csv` (built by `context/flows_2015_2025.py`).

| FY | LPR total | Imm. relatives | Family pref | Employment | EB principals* | EB derivatives* | Diversity | Refugee/asylee | Other |
|---|---|---|---|---|---|---|---|---|---|
| 2015 | 64116 | 20558 | 14591 | 27514 | 12130 | 15400 | 50 | 978 | 422 |
| 2016 | 64687 | 24246 | 18230 | 20747 | 9020 | 11730 | 30 | 1068 | 368 |
| 2017 | 60394 | 20549 | 14962 | 23569 | 10200 | 13370 | 40 | 795 | 479 |
| 2018 | 59821 | 20652 | 14845 | 22672 | 9750 | 12920 | 30 | 1228 | 390 |
| 2019 | 54495 | 21049 | 13387 | 18553 | 7860 | 10690 | 30 | 1007 | 474 |
| 2020 | 46363 | 12945 | 7077 | 24883 | 10660 | 14230 | 10 | 1146 | 298 |
| 2021 | 93450 | 14949 | 1896 | 75332 | 33550 | 41780 | 20 | 1009 | 242 |
| 2022 | 127012 | 20396 | 8055 | 96335 | 44420 | 51920 | 60 | 1829 | 341 |
| 2023 | 78070 | 31790 | 15140 | 28570 | 12020 | 16550 | 60 | 1740 | 790 |
| 2024 | 66800 | 34090 | 9660 | 18800 | 8390 | 10410 | 30 | 3710 | 520 |

[INFERENCE] Indian EB green cards are capped by per-country limits. The FY2021–22 spike (75k, 96k) is consistent with pandemic-unused family numbers rolling over to EB ([UNVERIFIED] mechanism, not checked against State Dept Visa Bulletin or USCIS data), i.e. backlog clearance of people already in the US, not new arrivals. Principals are only about 40–45% of EB LPRs.

### 6(b) USCIS H-1B approvals, India-born, initial vs continuing (appended 2026-09-29 23:18:58 JST) [DATA]

From `context/h1b_characteristics_fy2003_2025.csv` (item 3). Continuing = all minus initial [CALCULATION]. "Initial" includes cap-exempt and change-of-status approvals, so it is not the same as new arrivals.


| FY | H-1B approved (India) | initial | continuing |
|---|---|---|---|
| 2015 | 195247 | 71263 | 123984 |
| 2016 | 256226 | 70737 | 185489 |
| 2017 | 276423 | 67815 | 208608 |
| 2018 | 243994 | 51353 | 192641 |
| 2019 | 278491 | 79423 | 199068 |
| 2020 | 319494 | 73717 | 245777 |
| 2021 | 301616 | 75858 | 225758 |
| 2022 | 320791 | 77673 | 243118 |
| 2023 | 279386 | 68825 | 210561 |
| 2024 | 283755 | 80449 | 203306 |
| 2025 | 284106 | 57747 | 226359 |

### 6(d)(e) Cross-references (appended 2026-09-29 23:18:58 JST)

- (d) CBP encounters FY2020–FY2025: item 1 above; rows `cbp_encounters_*` are in flows_2015_2025.csv. FY2019 on the encounters basis is still a [GAP]; the DHS Yearbook 2020 Table 34 figure of 8,926 (Border Patrol + ICE apprehensions) is the fallback.
- (e) Unauthorized estimates: item 2 above (DHS 2015–2022, Pew 2023, MPI region-only).

### 6(c) Students (SEVIS) and nonimmigrant admissions (I-94), India (appended 2026-09-29 23:34:06 JST) [DATA]

**ICE SEVP "SEVIS by the Numbers"** [SOURCE: https://www.ice.gov/sevis/whats-new, the page reached from https://www.dhs.gov/hsi/sevp/sevis-by-the-numbers, listing https://www.ice.gov/doclib/sevis/btn/…]. There are 23 PDFs in `_cache/context/sevis/`; their sha256 are in `context/sevis_sha256.txt`. The script `context/sevis_india.py` appends the rows to flows_2015_2025.csv. All values are calendar years. "Active SEVIS records" means F-1 and M-1 student records active at any time in the year, which is not a stock on a given day. STEM OPT counts records with an authorization to take part during the year.

| CY | Active student records, India | STEM OPT authorized records, India | Quoted line |
|---|---|---|---|
| 2017 | 247,133 | 49,368 | `INDIA 247,133` / `INDIA 49,368` (2017 all-students-by-coc / all-coc-stem-opt) |
| 2018 | 251,290 | 70,521 | same files, 2018 |
| 2019 | 249,221 | 77,714 | same, 2019 |
| 2020 | 207,460 | 63,744 | same, 2020 |
| 2021 | 232,851 | 52,796 | same, 2021 |
| 2022 | 297,151 | 52,107 | same, 2022 |
| 2023 | 377,620 | 47,693 | same, 2023. The cy23 report text: "a total of 122,101 international students participating in … STEM OPT in 2023 … from India (39.1%)", i.e. about 47,741, consistent |
| 2024 | 422,335 | ~79,452 (derived: 48.0% × 165,524) | 2024 report: `India 422,335`; "STEM OPT extension were from India (48.0%) or China (20.4%), with 165,524 foreign students participating in STEM OPT in 2024." |

[GAP] 2015–2016 per-country SEVIS files: the earliest per-country PDFs on the ICE page are 2017; the 2017/2018 "biannual" reports are archived but were not parsed. [GAP] Pre-completion and post-completion (12-month) OPT by country: not in these per-country PDFs; the cy reports say they are in the "SEVP Data Library". [UNVERIFIED] The 2019→2023 fall in STEM OPT records (77.7k to 47.7k) while active records rose may reflect a change in definition or reporting rather than behaviour; the definitions were not reconciled.

**DHS Yearbook FY2024 nonimmigrant tables**: the local file is `indian_ledger_2026_09_18/_cache/yearbook_nonimmigrants_fy2024.xlsx`, sha256 deab954e…1087, byte-identical to `20260604_ohss_yearbook_nonimmigrants_fy2024.xlsx`; its download URL is [UNVERIFIED]. The script is `context/nonimmigrant_india.py`. I-94 admissions are entries, not persons.
- Table 27, I-94 admissions of Indian citizens, all classes, FY2015–FY2024: 1,898,330 · 1,988,420 · 2,055,480 · 2,223,160 · 2,316,030 · 1,059,770 · 540,300 · 1,793,060 · 2,599,630 · 2,944,840
- NISuppTable1, FY2024, India column: H1B 497,460; H4 215,440; L1 64,910; L2 10 (as printed, with footnote 11 on the class; it probably reflects an L-2 recoding, [UNVERIFIED]); F1 298,760; F2 6,720; J1 20,160; M1 1,760; O1 5,080; B1 247,210; B2 1,466,200.
- Table 33, FY2024 temporary workers and families, India: total 840,320; specialty occupations 497,460; intracompany transferees 64,910; spouses and children 265,400.

[GAP] Class-by-country I-94 for FY2015–FY2023: each year's yearbook nonimmigrant xlsx is needed. Not fetched; the FY2024 workbook carries only FY2024 by class.

### 6(d) FY2019 CBP retry (appended 2026-09-29 23:34:06 JST)
Wayback CDX prefix search over `cbp.gov/sites/default/files/assets/documents/{2020-Oct,2020-Nov,2021-Oct,2021-Nov,2021-Dec,2022-Oct,2022-Nov,2022-Dec}/` found `2022-Oct/nationwide-encounters-fy20-fy22.csv` (which starts at FY2020) and `2022-Oct/sbo-encounters-fy19-fy22.csv`. The latter is archived as `_cache/context/sbo-encounters-fy19-fy22.csv` (Wayback 20221231133907, sha256 eedf60aad15ef7b274350df76037dc0540807c0199cecac17cfb46509c1c5667). Its "Citizenship Grouping" only has El Salvador, Guatemala, Honduras, Mexico and Other, so India cannot be separated. The FY2019 encounters basis stays a [GAP]; use the DHS Yearbook 2020 Table 34 figure (8,926, Border Patrol + ICE apprehensions) with its construct label.

### Item 4 addendum 2 — FY2019 and FY2024 LCA runs (appended 2026-09-29 23:36:26 JST) [DATA] [CALCULATION]
Log: `_cache/context/lca/run_fy19_fy24.log`, rc19=0 and rc24=0. The first FY2019 attempt stalled on memory (the 1.74 GB sheet XML read with all columns) and was killed. The script now reads only the five needed columns.

Column checks:
- FY2019 (`H-1B_Disclosure_Data_FY2019.xlsx`, sha256 ec103bde…9ab89, 664,616 rows): the wage level is **PW_WAGE_LEVEL_1**, the first worksite's level (the file has PW_WAGE_LEVEL_1…_10, one per worksite); the positions column is TOTAL_WORKER_POSITIONS. Status counts: CERTIFIED 592,103. Level values: II 320,990, III 118,271, I 91,913, IV 69,395, missing 60,152, N/A 3,895.
- FY2024 (Q1–Q4 pooled; sha256 of the quarterly files are in the log): PW_WAGE_LEVEL and TOTAL_WORKER_POSITIONS. Status counts: Certified 514,896. Level values: II 226,704, III 107,041, I 103,566, IV 80,563, missing 40,264, N/A 2,899.

Certified H-1B LCAs, share of cases at wage levels I / II / III / IV (among cases with a level):

| FY | Group | Cases | I | II | III | IV |
|---|---|---|---|---|---|---|
| 2015 | Six outsourcers | 76,702 | 23.1 | 60.9 | 12.5 | 3.6 |
| 2015 | All other employers | 459,991 | 50.0 | 32.0 | 11.1 | 6.9 |
| 2019 | Six outsourcers | 75,657 | 1.8 | 71.7 | 20.0 | 6.6 |
| 2019 | All other employers | 502,983 | 16.8 | 51.5 | 19.7 | 12.0 |
| 2024 | Six outsourcers | 34,837 | 0.9 | 60.1 | 28.8 | 10.2 |
| 2024 | All other employers | 467,537 | 20.4 | 43.6 | 20.3 | 15.7 |

Per employer, FY2024: TCS 0.0 / 86.1 / 12.9 / 1.0; Wipro 88% Level II; Tech Mahindra 99.9% Level II; Cognizant 0.0 / 34.2 / 47.9 / 17.8. The outsourcers' share of certified H-1B LCAs fell from 14.3% (FY2015) to 6.9% (FY2024) [CALCULATION from the case counts].

[INFERENCE] Level I nearly vanished at the outsourcers after FY2015; Level II became their floor, with some shift up to Level III by FY2024. Other employers file far more Level I (new graduates). On the wage-level proxy, the outsourcer inflow therefore does not sit at the bottom. The level is set against the local occupational wage distribution, though, so it is not a skill measure. [UNVERIFIED] The FY2015→FY2019 drop in Level I across all employers (46%→15%) may partly reflect policy scrutiny of Level I filings; not checked.

[GAP] The employer-name regex has not been audited for variants such as "HCL America Inc" vs "HCL Technologies"; Cognizant matches on the word. FY2019 uses only worksite 1's level.

Rebuild order for `context/flows_2015_2025.csv`: `flows_2015_2025.py` (overwrites), then `nonimmigrant_india.py` and `sevis_india.py` (append). Run with `uv run --no-project --with openpyxl --with xlrd python3 …`.
