# Immigration — Dataset Roadmap, Batch 3 (2026-06-24)

Third batch of real datasets, supplementing `immigration-dataset-roadmap.md` (12 targets),
`immigration-dataset-roadmap-additions-2026-06-24.md` (5 more), and `immigration-dataset-register.md`
(what we hold). These are ADDITIONAL real datasets — none repeats the 17+3 already proposed/flagged.

**Gaps this batch fills (priority order):** (1) legal-status labor (NAWS, DOL OFLC), (2) health
(NHIS, AHRQ HCUP), (3) tax (IRS SOI ITIN / TIGTA, SSA Earnings Suspense File), (4) housing (AHS),
(5) innovation (USPTO PatentsView + linked-inventor research datasets), (6) international admin-linked
(StatCan IMDB, UK/Dustmann-Frattini), (7) flows/enforcement (DHS OHSS Yearbook, TRAC, MMP).

All URLs/DOIs verified live via search 2026-06-24 unless tagged `[UNVERIFIED]`.

Join-key legend for the warehouse: `state_fips`, `county_fips`, `POBP`/origin-country, `education_bucket`,
`citizenship`/`nativity`, `topic`, `FY/year`. A dataset with no nativity/status field is flagged as an
ecological/calibration layer, not a status dataset.

---

## Axis 1 — Legal-status labor (highest priority)

### NAWS-PAD — National Agricultural Workers Survey, Public Access Data
**Source:** US Dept. of Labor, ETA (Office of Policy Development & Research; survey by JBS International) · **Access:** Public — direct download, no registration, fully scriptable
**Official:** https://www.dol.gov/agencies/eta/national-agricultural-workers-survey/data · files (Excel/CSV) https://www.dol.gov/agencies/eta/national-agricultural-workers-survey/data/files-excel-csv · SAS/access guidance https://www.dol.gov/agencies/eta/national-agricultural-workers-survey/data/accessing-data-files
**Format / size:** SAS, Excel, CSV. Two primary files `NAWS_A2E1103` (~25 MB) + `NAWS_F2Y1103` (~24 MB), split alphabetically A-E / F-Y; merge on `FWID`. Plus NIOSH (2009-10) and EPA (2013-14) supplement files.
**Key variables:** 232 questionnaire + 128 created/analytic variables, 73,909 in-person interviews, 48 states, FY1989-2022. **Legal/work-authorization status of crop workers** (the created variables flag authorized/unauthorized/citizen/green-card/other) — this is THE federal survey with farmworker legal status. Also: earnings, hours, employer count, health, demographics. Composite weight `PWTYCRD` for trend analysis (combine ≥2 yrs for national estimates).
**Why it fits:** the ONLY federal survey that records work-authorization/legal status for a labor force — directly grounds the low-skill-unauthorized-labor core of the project with a status field ACS/CPS lack. Trend-capable over 34 years.
**Limit / honesty:** privacy masking — birth location and birth date are NOT in the public file; month-of-interview, primary sampling unit, and 12→6 region collapse are masked. So legal status is present but origin-country granularity and fine geography are not (restricted-data territory). Crop-worker universe only (not all immigrants). [SOURCE: dol.gov/agencies/eta/national-agricultural-workers-survey/data]
**Graph fit:** new `labor_status` layer; `legal_status` × `FY` × analysis-region (6); no clean origin-country or state join (region-level only). Pairs with our ACS education buckets for the ag-sector low-skill arm.

### OFLC-DISCLOSURE — DOL Office of Foreign Labor Certification, Disclosure Data
**Source:** US Dept. of Labor, ETA / OFLC · **Access:** Public — cumulative quarterly + FY Excel files, plus structured wage downloads. Scriptable via stable flag.dol.gov download paths.
**Official:** performance/disclosure hub https://www.dol.gov/agencies/eta/foreign-labor/performance · how-to-use PDF (field structure) https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/how_to_use_the_disclosure_data.pdf · wage-data downloads https://flag.dol.gov/wage-data/wage-data-downloads · program pages H-2A/H-2B/LCA(H-1B)/PERM under https://flag.dol.gov/programs/
**Format / size:** one cumulative Excel file per program per FY, keyed by OFLC case number (most-recent determination date); "File Structure" doc per dataset lists every field. Large (hundreds of thousands of case rows/yr).
**Key variables:** per-application case records for **H-1B (LCA), PERM, H-2A, H-2B, CW-1, Prevailing Wage**: employer name/state, `ALIEN_WORK_STATE`/worksite, SOC occupation, wage offered vs prevailing wage, `NBR_WORKERS_CERTIFIED`, case status (certified/denied/withdrawn), FY. PERM and some forms carry alien country of citizenship/birth and education.
**Why it fits:** the administrative record of the legal employment-based immigration channel — wage levels of sponsored foreign workers by occupation/state, the high-skill (H-1B) and seasonal-low-skill (H-2A/H-2B) labor-demand side. Complements our undocumented-focused stack with the documented-channel wage/occupation truth. H-2A/H-2B are the low-skill seasonal arm directly relevant to the project focus.
**Limit / honesty:** application-level, not a sample of the population; "certified" ≠ "admitted/worked"; citizenship-of-alien completeness varies by program (LCA often blank, PERM richer). Data-entry anomalies noted by OFLC itself. [SOURCE: dol.gov/agencies/eta/foreign-labor/performance]
**Graph fit:** `labor_demand` layer; join by `state_fips` (worksite) × SOC/NAICS × FY; PERM rows join origin layer by alien country of birth.

---

## Axis 2 — Health (nativity + insurance + utilization, and direct hospital cost)

### NHIS-PUF — National Health Interview Survey, Public-Use Files
**Source:** CDC / National Center for Health Statistics (NCHS) · **Access:** Public — direct CSV/ASCII/SAS/SPSS/Stata download, annual, no registration. Fully scriptable from stable cdc.gov paths.
**Official:** documentation gateway https://www.cdc.gov/nchs/nhis/documentation/index.html · 2024 files (public-use CSV + input statements) https://www.cdc.gov/nchs/nhis/documentation/2024-nhis.html · 2023 https://www.cdc.gov/nchs/nhis/documentation/2023-nhis.html · pre-2019 via CDC Archive
**Format / size:** Sample Adult + Sample Child files per year (~31k adult / ~6k child interviews in recent years); CSV + format-specific input statements; parent-child pair file; imputed-income file.
**Key variables:** **citizenship status and nativity (US-born vs foreign-born)** plus, on recent public files, years living in the US (often categorized); **health insurance coverage type** (uninsured/Medicaid/Medicare/private/Marketplace), **health-care utilization** (visits, ER use, delayed/forgone care, usual source of care), chronic conditions, self-rated health, income, industry/occupation supplement. The principal US source on health of the civilian noninstitutionalized population.
**Why it fits:** the cleanest public micro source linking **nativity → insurance → utilization** — lets us estimate uninsurance and care-use differentials by nativity directly, rather than inferring health cost from MEPS payer cells. Annual, long time series, large sample.
**Limit / honesty:** detailed place-of-birth (specific country) and fine geography are RESTRICTED (RDC only); public file has citizenship + foreign/native + sometimes coarse years-in-US, region + 4-level urban/rural only — no state. No legal status. [SOURCE: cdc.gov/nchs/nhis/documentation]
**Graph fit:** `health` layer; `nativity`/`citizenship` × insurance × utilization; region-level only (no state join) — descriptive incidence, pairs with MEPS cost cells.

### HCUP-NIS-NEDS — AHRQ Healthcare Cost and Utilization Project (NIS / NEDS / KID / SID)
**Source:** AHRQ, Federal-State-Industry partnership · **Access:** GATED — microdata via HCUP Central Distributor (online account + DUA training + purchase; ~$750/yr for recent NIS, State DBs shipped on DVD). FREE aggregate online tool: **HCUPnet**. NOT directly scriptable for microdata (per-order, all sales final); HCUPnet is interactive only.
**Official:** NIS overview https://hcup-us.ahrq.gov/nisoverview.jsp · purchase/Central Distributor https://hcup-us.ahrq.gov/tech_assist/centdist.jsp · online ordering catalog https://cdors.ahrq.gov/databases · free HCUPnet tool https://datatools.ahrq.gov/hcupnet/
**Format / size:** NIS = ~20% stratified all-payer sample of US community-hospital discharges, ~7M unweighted stays/yr → ~33M weighted; 1988-2023, 45 states + DC in 2023. NEDS = ED visits; KID = pediatric inpatient; SID/SEDD = state-level all-discharge.
**Key variables:** per-discharge diagnosis/procedure (ICD-10), **total charges and cost-to-charge-derived cost**, length of stay, **expected primary payer** (Medicare/Medicaid/private/**self-pay/uninsured/no-charge**), patient age/sex, ZIP-income quartile, hospital characteristics; ED disposition for NEDS.
**Why it fits:** the authoritative US hospital/ED **cost** database — gives real dollar magnitudes for inpatient and emergency care that our MEPS/Emergency-Medicaid cost cells only approximate. The self-pay/uninsured and Medicaid payer strata are the analytic proxy for the immigrant/unauthorized-heavy uncompensated-care channel.
**Limit / honesty:** **HCUP has NO nativity, citizenship, or immigration status — none.** Immigrant cost is reachable ONLY by proxy (payer = self-pay/uninsured/emergency-Medicaid; ZIP-income; ZIP-immigrant-share join). Treat strictly as a cost-magnitude/payer-incidence anchor, not a status dataset. Gated + paid. [SOURCE: hcup-us.ahrq.gov/nisoverview.jsp]
**Graph fit:** `health_cost` anchor; join by hospital-state and (restricted) patient ZIP; payer-strata bridge to Emergency-Medicaid/MEPS, NOT a nativity join.

---

## Axis 3 — Tax (ITIN filers; unauthorized SS contributions)

### IRS-ITIN-TAS-TIGTA — ITIN-filer tax statistics (Taxpayer Advocate + TIGTA reports)
**Source:** IRS Taxpayer Advocate Service (TAS) + Treasury Inspector General for Tax Administration (TIGTA) · **Access:** Public PDF reports (no microdata release). Scriptable only as document fetch + table parse, like the existing CBO/ITEP PDFs.
**Official:** TAS Annual Report to Congress 2024, Research Study #3 "IRS Processing of ITINs" https://www.taxpayeradvocate.irs.gov/wp-content/uploads/2024/12/ARC24_RR_Research_3.pdf · TIGTA 2020 audit (2020-40-064) https://www.tigta.gov/sites/default/files/reports/2024-11/202040064fr.pdf · TIGTA 2026 ITIN program assessment (2026-400-016) via https://www.oversight.gov/reports/audit/assessment-irss-individual-taxpayer-identification-number-program
**Format / size:** narrative + summary tables in PDF. The TAS study quantifies the ITIN filing population, taxes paid, and credits.
**Key variables (as reported aggregates):** size of ITIN tax-return filing population (millions of returns/yr); **taxes paid net of credits ≈ $2-4 billion/yr**; ITIN-filer median AGI ≈ $31,000 (predominantly low-income); credits claimed (CTC/ACTC); cumulative ITINs issued (>24M as of Dec 2019). TIGTA reports add issuance/compliance counts and trend (530k TY2001 → 1.8M TY2007).
**Why it fits:** ITIN filers are the closest administrative proxy for **tax-paying unauthorized immigrants** (no SSN, filing anyway). This is the IRS-side counterpart to our ITEP tax estimate — a federal-administrative number for the contribution side, with the low-income composition the project's low-skill focus predicts. Directly fills the "IRS SOI ITIN / TIGTA" tax gap.
**Limit / honesty:** ITIN holder ≠ unauthorized (also includes some nonresidents, dependents, certain visa holders) — a proxy, not a clean status field. Aggregate report tables only, no microdata (true SOI ITIN microdata is in the restricted SOI PUF the register already tracks). Numbers are point-in-time estimates. [SOURCE: taxpayeradvocate.irs.gov ARC24 Research Study 3]
**Graph fit:** `tax_contribution` ledger line (national); no clean state/origin join — national aggregate that cross-checks ITEP's $96.7B undocumented-tax total.

### SSA-ESF-NWALIEN — Earnings Suspense File + Nonwork Alien File (SSA OIG reports)
**Source:** Social Security Administration, Office of the Inspector General (OIG, Office of Audit) · **Access:** Public PDF audit reports with the aggregate figures; the underlying ESF/NWALIEN MICRODATA is restricted (register already flags SSA-ESF microdata as restricted). Scriptable as PDF fetch + parse.
**Official:** ESF status report A-03-15-50058 https://oig-files.ssa.gov/audits/summary/Summary%2050058.pdf · Nonwork-SSN wages A-03-18-50537 (2018) https://oig-files.ssa.gov/audits/full/A-03-18-50537.pdf · employer wage-error patterns A-08-12-13036 (2013) https://oig-files.ssa.gov/audits/full/A-08-12-13036.pdf · NWALIEN profile A-14-03-23071 (limited distribution summary) https://oig-files.ssa.gov/audits/full/A-14-03-23071.pdf · SSA OIG audit library https://oig.ssa.gov/audits-and-investigations/audit-reports/
**Format / size:** OIG report PDFs with summary tables and trend figures.
**Key variables (as reported aggregates):** **ESF cumulative ≈ $1.2 trillion uncredited wages across ~333 million W-2s (TY1937-2012)**; ~95% of recent suspensions = name/SSN mismatch; **NWALIEN file ≈ 422,000 individuals earning ≈ $50 billion in wages (TY2014-16)**; trend 607k individuals TY1996 → 343k TY2016; ~80% of employers had not used E-Verify. These are the canonical sources for unauthorized payroll-tax contributions that workers cannot later claim as benefits.
**Why it fits:** THE administrative evidence for the "unauthorized workers pay Social Security taxes they never collect" channel — a large, structural net contribution to the trust funds. Complements the SSA actuarial note already held with the suspense-file dollar magnitudes and the nonwork-SSN worker counts. Fills the "SSA Earnings Suspense File" tax gap.
**Limit / honesty:** ESF mismatches are NOT all unauthorized workers (also clerical errors, name changes, deaths) — it is an upper-bound proxy; NWALIEN is the tighter (nonwork-SSN) subset but still not the full unauthorized population (many use fraudulent/borrowed SSNs that DO match and never hit the ESF). Aggregate reports only; microdata restricted. Most recent NWALIEN figure is TY2016. [SOURCE: oig-files.ssa.gov A-03-18-50537]
**Graph fit:** `tax_contribution` ledger line (national, trust-fund); no clean state/origin join — national aggregate, pairs with the held SSA actuarial note.

---

## Axis 4 — Housing (nativity)

### AHS-PUF — American Housing Survey, Public Use File
**Source:** US Census Bureau (sponsored by HUD) · **Access:** Public — direct CSV/SAS microdata download, no registration, fully scriptable from stable census.gov paths.
**Official:** data hub https://www.census.gov/programs-surveys/ahs/data.html · 2023 National PUF https://www.census.gov/programs-surveys/ahs/data/2023/ahs-2023-public-use-file--puf-/ahs-2023-national-public-use-file--puf-.html · PUF codebook (1973+) https://www.census.gov/programs-surveys/ahs/tech-documentation/codebooks.html · getting-started guide https://www.census.gov/programs-surveys/ahs/tech-documentation/help-guides/2015-later/puf_start.html
**Format / size:** 2023 National PUF v1.1 — CSV [124 MB] / SAS [140 MB], plus a combined "flat file" (one record per housing unit) CSV [136 MB]. Biennial (odd years); national + selected metros. Value-labels package provided.
**Key variables:** housing-unit level — tenure (own/rent), housing costs, rent burden, crowding (persons-per-room), housing quality/adequacy, neighborhood, mortgage, utilities, moves; householder age/race/Hispanic origin, household income. Rich on housing-cost burden and crowding — the channels immigration is hypothesized to affect.
**Why it fits:** the deepest US housing-cost-burden and crowding microdata — directly tests the housing-market / rent-burden channel (overcrowding, cost burden) in the immigration-fiscal debate at the housing-unit level, complementing our ACS/CHAS/SAFMR housing layers.
**Limit / honesty — VERIFY BEFORE USE:** AHS's analytic strength is the housing unit, NOT person nativity. The PUF historically does **NOT** carry a clean householder foreign-born / citizenship / place-of-birth variable (it collects detailed household roster demographics but immigration nativity is sparse-to-absent on the public file). **Confirm in the 2023 PUF codebook whether any nativity/citizenship field exists before treating this as a status dataset.** If absent (likely), AHS is a housing-burden layer joined to nativity ONLY ecologically (by metro/region × ACS foreign-born share), not a person-level nativity split. [SOURCE: census.gov/programs-surveys/ahs/data] [UNVERIFIED — nativity-field presence on PUF]
**Graph fit:** `housing` layer; housing-unit level; join by metro/region; nativity only via ecological bridge unless codebook confirms a field.

---

## Axis 5 — Innovation (immigrant inventors)

### USPTO-PATENTSVIEW — PatentsView disambiguated inventor warehouse (USPTO Open Data Portal)
**Source:** USPTO (PatentsView project; American Institutes for Research et al.) · **Access:** Public API + bulk download; migrating to USPTO Open Data Portal (data.uspto.gov) — **USPTO.gov account / sign-in required as of June 18, 2026** for ODP access. Legacy PatentsView API + bulk still scriptable.
**Official:** PatentsView ODP transition guide https://data.uspto.gov/support/transition-guide/patentsview · methods/sources https://patentsview.org/methods-and-sources · disambiguation overview https://www.patentsview.org/disambiguation · API catalog https://developer.uspto.gov/api-catalog/patentsview · legacy API syntax http://www.patentsview.org/api/query-language.html
**Format / size:** relational warehouse from USPTO granted patents (1976-present) + published applications (2001-present), updated quarterly; bulk TSV downloads + JSON query API. Disambiguated **unique inventor IDs**, assignees, **geocoded inventor location** (city/state/country).
**Key variables:** per-patent inventor name, disambiguated inventor ID, **inventor location including country**, assignee (company/university), CPC/USPC technology class, grant/filing dates, citations. Inventor **foreign location** is the native field; inventor **nativity/immigration status is NOT in PatentsView** — it must be added from linked research datasets (next card).
**Why it fits:** the backbone for the immigrant-innovation benefit channel — patenting/technology output keyed to inventors, with foreign inventor-location and (via linkage) immigrant inventors. The benefit-side counterpart the project under-weights, with official microdata instead of secondary citation. The "USPTO PatentsView" half of the flagged `[UNVERIFIED]` innovation gap, now verified.
**Limit / honesty:** PatentsView has NO direct nativity/citizenship/immigration-status field — only inventor-reported location (which proxies foreign residence at filing, not foreign birth). Immigrant-inventor identification requires an external linkage (see USPTO-INVENTOR-LINKED below). Disambiguation is probabilistic (error remains). ODP sign-in now gates bulk access. [SOURCE: patentsview.org/methods-and-sources]
**Graph fit:** `innovation` layer; inventor-ID × technology-class × inventor-country × year; join origin layer by inventor country; nativity only after linkage.

---

## Axis 6 — International admin-linked (gold-standard longitudinal)

### STATCAN-IMDB — Longitudinal Immigration Database (Canada)
**Source:** Statistics Canada, on behalf of a federal-provincial consortium led by IRCC; admin immigration (IRCC) linked to tax (CRA T1) · **Access:** TWO tiers — (a) PUBLIC aggregate data tables, downloadable + scriptable via the StatCan Web Data Service (WDS) API; (b) microdata via the Research Data Centre (RDC) program (restricted, in-Canada secure-enclave only).
**Official:** program record (survey 5057) https://www.statcan.gc.ca/imdb-bmdi/5057-eng.htm · Technical Report 2024 https://www150.statcan.gc.ca/n1/en/catalogue/11-633-X2025004 · economic-outcomes interactive + table 43-10-0026-01 https://www150.statcan.gc.ca/n1/pub/71-607-x/71-607-x2019003-eng.htm · public tables searchable under "Longitudinal Immigration Database" at https://www150.statcan.gc.ca/n1/en/type/data
**Format / size:** admin records for ALL immigrants since 1952 + non-permanent residents since 1980; tax outcomes since 1982; annual. Public tables: CSV/JSON via WDS API (table IDs like 43-10-0026). Microdata: full linked file in RDC.
**Key variables:** at admission — **admission category** (economic/family/refugee, with detail), source country, official-language knowledge, pre-admission Canadian experience (work/study permit, asylum claim); outcomes — **employment income, wages/salaries, EI, investment income, self-employment, social-welfare benefits**, interprovincial mobility, citizenship acquisition (since 2004), children's outcomes, settlement-service use (since 2013). Asylum-claimant income tables too.
**Why it fits:** the **gold-standard admin-linked longitudinal immigrant fiscal database** — exactly the object the project's lifetime-NPV work approximates from ACS cross-sections. It shows, by admission category and source country over 40+ years, the earnings-and-benefit trajectory that the US lacks a public equivalent of (our SSA/IRS microdata being restricted). Provides a methodological template AND a comparison benchmark (refugee vs economic-class fiscal trajectories) the US debate cannot build domestically. The benefit/cost trajectory split by category is the structural answer to "do low-skill/humanitarian entrants converge."
**Limit / honesty:** Canada, not US — institutional/selection differences (Canada's points-system economic majority) limit direct transfer; it benchmarks METHOD and category-contrast, not US levels. Public tables are aggregates (no microdata outside Canadian RDCs; non-Canadians effectively cannot access the microdata). Tax-based, so the undocumented are out of scope (Canada's unauthorized population is small and not the IMDB universe). [SOURCE: statcan.gc.ca/imdb-bmdi/5057-eng.htm]
**Graph fit:** international benchmark node; `admission_category` × source-country × tax-year; source-country joins origin layer; cross-checks US category-specific fiscal claims.
