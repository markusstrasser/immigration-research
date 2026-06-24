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

---

## Axis 5b — Innovation: the linked immigrant-inventor dataset (resolves USPTO-PATENTSVIEW's forward reference)

### USPTO-INVENTOR-LINKED — Immigrant inventors via SSN-age linkage (Bernstein, Diamond, Jiranaphawiboon, McQuade & Pousada)
**Source:** Bernstein (Harvard/NBER), Diamond (Harvard/NBER), Jiranaphawiboon (Stanford), McQuade (UC Berkeley/NBER), Pousada (CRA) — "The Contribution of High-Skilled Immigrants to Innovation in the United States" · **Access:** PUBLIC paper + working-paper drafts (free PDFs). The underlying linkage uses CONFIDENTIAL administrative data (Infutor address histories + SSA-derived age-of-SSN-assignment) — full replication MICRODATA is NOT openly redistributable; AER replication package (forthcoming) carries code + any releasable derived aggregates.
**Official:** NBER WP 30797 https://www.nber.org/papers/w30797 · DOI 10.3386/w30797 · AER-version PDF (Dec 2025) https://www.hbs.edu/ris/Publication%20Files/BDMP_2025_AER_V2%20(1)_73437f8e-0c2a-4890-ab47-55310b103df8.pdf · author copy https://web.stanford.edu/~diamondr/BDMP.pdf · non-technical summary https://www.nber.org/digest/20233/outsize-role-immigrants-us-innovation
**Format / size:** paper + appendices report the immigrant-vs-native inventor statistics; method links US inventors (1990-2016) to immigrant status by identifying individuals **assigned an SSN at age 20 or older** (a proxy for foreign birth) via large-scale administrative address data, then to USPTO/PatentsView patent records.
**Key variables (as published):** **immigrant status of inventor** (the field PatentsView lacks), patent counts, citation-weighted and market-value-weighted output, collaboration networks, technology field, county. Headline: immigrants = 16% of inventors but 23% of patents (24-25% quality/value-weighted), 36% incl. collaborations, ~32% of aggregate innovation (over half via human-capital spillovers onto US-born collaborators).
**Why it fits:** THIS is the "linked-inventor research dataset" the USPTO-PATENTSVIEW card defers to — it supplies the immigrant-status layer that turns raw patent records into an immigrant-innovation benefit estimate. The strongest single quantification of the innovation benefit channel (Azoulay / Hunt-Gauthier-Loiselle lineage), with an administrative identification strategy rather than ethnic-name imputation. Resolves the dangling USPTO-INVENTOR-LINKED reference.
**Limit / honesty:** identification is HIGH-skilled inventors only (NOT the low-skill focus of the project — this is a deliberate benefit-side counterweight, not the core). "SSN assigned at 20+" is a proxy for immigrant (misses child immigrants, naturalized-young). Microdata confidential (Infutor + SSA) — you get published aggregates and replication code, NOT a person-level file to re-run on the warehouse. Weaker ethnic-name alternatives (Kerr) exist but are inferior identification. [SOURCE: nber.org/papers/w30797] [UNVERIFIED — openness of AER replication-archive contents]
**Graph fit:** `innovation` benefit node; published aggregates by technology-field/county; no row-level join (microdata restricted) — use as a benchmark/parameter source layered on PatentsView's open inventor-country data.

---

## Axis 7 — Flows / enforcement

### TRAC-IMMIGRATION — Transactional Records Access Clearinghouse (Syracuse)
**Source:** TRAC, Syracuse University — case-by-case records obtained from EOIR, ICE, CBP, DOJ via FOIA + direct court feeds · **Access:** Public web data tools + Quick Facts (free); some detailed apps and bulk extracts behind a paid TRAC subscription. Tools are interactive (stable URLs) — NOT a clean bulk-CSV API for the free tier; scriptable only by scraping the tool endpoints.
**Official:** hub https://tracreports.org/immigration/index.html · data-tools index https://tracreports.org/immigration/tools/ · tools primer https://tracreports.org/immigration/tools/primer.html · ICE-detention data notes (dimensions incl. citizenship) https://tracreports.org/phptools/immigration/detention/about_data.html
**Format / size:** interactive drill-down tables + downloadable Quick Facts. Coverage: immigration-court new proceedings Oct 1991-present; court outcomes Oct 1997-present; asylum decisions by judge 1993-2025; ICE custody snapshots; removals; CBP/ICE encounters; criminal immigration prosecutions; ATD; bond decisions; MPP.
**Key variables:** immigration-court case outcomes, backlog, representation, asylum grant/deny by judge and nationality; **ICE custody by citizenship, gender, MSCC (most-serious criminal conviction) seriousness/recency**; removals; prosecution counts by charge; detention facility. Detention/court tools expose **citizenship/nationality** as a selectable dimension — a crime-and-enforcement bridge.
**Why it fits:** extends our held EOIR court layer with a maintained, longer (1991+), more granular enforcement/court series — including the criminality-of-detainees and nationality dimensions that connect the crime and enforcement halves. The "Just 2% of court filings based on criminal activity" type series is directly relevant to the immigration-crime framing.
**Limit / honesty:** FOIA-derived → subject to agency redaction/withholding (TRAC notes ICE withholding age data, ongoing disputes); court venue ≠ residence (same caveat as our EOIR file); free tier is interactive tables, not bulk microdata (full case-level extracts require paid access or scraping). Derived/secondary (TRAC's processing of agency data), not the raw agency release. [SOURCE: tracreports.org/immigration/tools]
**Graph fit:** `enforcement`/`crime` overlay; nationality × FY × outcome; nationality joins origin layer; complements EOIR + ICE-ERO.

### MMP — Mexican Migration Project (origin-side, Princeton / Guadalajara)
**Source:** Mexican Migration Project, Office of Population Research (Princeton) + University of Guadalajara; ethnosurvey since 1982 · **Access:** Public download with FREE registration (data-use agreement); fully downloadable files, scriptable once registered.
**Official:** project hub https://mmp.opr.princeton.edu/home-en.aspx · data overview https://mmp.opr.princeton.edu/databases/dataoverview-en.aspx · obtaining-files instructions https://mmp.opr.princeton.edu/databases/instructions-en.aspx · download archive https://oprdata.princeton.edu/archive/mmp/ · codebooks https://mmp.opr.princeton.edu/databases/codebooks-en.aspx
**Format / size:** core files (household-level, person-level, life-history) + community/MEXFILE/USA files in fixed-width / Stata / SPSS / CSV; 170+ Mexican communities surveyed since 1982, tens of thousands of households; companion Latin American Migration Project (LAMP) extends to other origins.
**Key variables:** complete US-migration histories of Mexican household members — **documentation status on each US trip** (undocumented / documented / citizen), trip duration, US wages, occupation, remittances, border-crossing experience, social-network ties; origin-community context. The ethnosurvey captures the unauthorized population that US household surveys miss, AT the origin.
**Why it fits:** the canonical ORIGIN-side complement — it sees the undocumented Mexican migration flow (the historical core of US unauthorized immigration) with documentation status, wages, remittances, and return migration that destination surveys cannot capture. Grounds the supply-shock and selection assumptions in the fiscal model with the migrant's own trip-level legal status and earnings. Pairs with our IPUMS supply-shock panel from the sending side.
**Limit / honesty:** NOT nationally representative of Mexico or of US-resident Mexicans (purposive community sample, over-weights high-migration communities) — excellent for mechanism/composition, NOT for population levels. Mexico-only (LAMP for other origins). Self-reported retrospective histories. Recent unauthorized flow has shifted toward Central America (out of MMP scope). [SOURCE: mmp.opr.princeton.edu/databases/instructions-en.aspx]
**Graph fit:** `origin_flow` layer; person/trip × documentation-status × sending-community; joins origin layer by Mexican state; supply-side complement to IPUMS panel.

### DHS-OHSS-YEARBOOK — Yearbook of Immigration Statistics
**Source:** DHS Office of Homeland Security Statistics (OHSS) · **Access:** Public — annual yearbook PDF + downloadable data tables (no registration). Data tables are scriptable from stable ohss.dhs.gov paths; released rolling as finalized.
**Official:** yearbook hub https://ohss.dhs.gov/topics/immigration/yearbook · 2024 https://ohss.dhs.gov/topics/immigration/yearbook/2024 · 2023 https://ohss.dhs.gov/topics/immigration/yearbook/2023 · 2022 (full PDF) https://ohss.dhs.gov/topics/immigration/yearbook/2022 · companion Annual Flow Reports (LPR / Refugees / Asylees / Naturalizations / Nonimmigrant / Enforcement) linked from the hub
**Format / size:** per-FY table sets (Excel/CSV "Download Data") + final yearbook PDF (released ~September of the following FY). Series back to 2006+ as PDFs; recent years (2023/2024) release tables rolling, full PDF "coming soon."
**Key variables:** **lawful permanent residents** (by class of admission, country of birth, state/metro of residence, age, occupation); **nonimmigrant (temporary visitor) admissions** by class (incl. H-2A/H-2B/H-1B); **refugees & asylees** by country; **naturalizations** by country/state; **enforcement actions** — apprehensions, removals, returns by country. Country-of-birth and state-of-residence are recurring keys.
**Why it fits:** the authoritative federal flow ledger — extends our held OHSS state file (2013-2023) with the full legal-admission, nonimmigrant, naturalization, and enforcement detail by country and state. Anchors the LEGAL-channel denominators (LPR/nonimmigrant inflows) that the fiscal model needs to separate authorized stock growth from unauthorized, and gives the enforcement-outcome counts (removals by country) that pair with the cost-side budget data we hold.
**Limit / honesty:** flows (events in a FY), NOT a stock or a person-panel — admissions ≠ net population change (no emigration). Legal/administrative channels are well-covered; the UNAUTHORIZED population is captured only via enforcement-action counts (apprehensions/removals), not as a measured population. Post-2017 reorganization split content into separate Annual Flow Reports — assemble across the hub. [SOURCE: ohss.dhs.gov/topics/immigration/yearbook]
**Graph fit:** `flows` layer; class-of-admission × country-of-birth × state × FY; country/state join origin + context layers; superset of the held OHSS state file.

---

## Axis 8 — International fiscal comparison (UK)

### UK-DUSTMANN-FRATTINI — Fiscal Effects of Immigration to the UK (+ Migration Observatory synthesis)
**Source:** Christian Dustmann (UCL/CReAM) & Tommaso Frattini (Univ. Milan), Economic Journal 2014; maintained synthesis by the Migration Observatory (Univ. Oxford, COMPAS) · **Access:** PUBLIC — free working-paper PDF + free Migration Observatory briefing. The estimates derive from the UK Labour Force Survey + government fiscal sources (LFS is itself a separate, accessible dataset via the UK Data Service) — the paper provides the METHOD and headline numbers, not a redistributable bespoke dataset.
**Official:** CReAM WP 22/13 free PDF https://www.cream-migration.org/publ_uploads/CDP_22_13.pdf · RePEc record (EJ 2014, vol 124(580):593-643) https://ideas.repec.org/p/crm/wpaper/1322.html · VoxEU summary https://cepr.org/voxeu/columns/fiscal-effects-immigration-uk · Migration Observatory 2024 briefing (Vargas-Silva, Sumption, Brindle) https://migrationobservatory.ox.ac.uk/resources/briefings/the-fiscal-impact-of-immigration-in-the-uk/ · briefing PDF https://migrationobservatory.ox.ac.uk/wp-content/uploads/2024/11/2024-Briefing-The-fiscal-impact-of-immigration-to-the-UK.pdf
**Format / size:** journal article + briefing (PDF/HTML) with net-fiscal-contribution tables by immigrant group and period.
**Key variables (as published):** net fiscal contribution of immigrants 1995-2011 (and recent arrivals since 2000), split **EEA vs non-EEA**; per-year revenue-minus-expenditure attribution. Headline: EEA immigrants made a **positive** net contribution even in deficit years; recent arrivals more positive than longer-resident; Migration Observatory synthesis: fiscal impact typically **<1% of GDP**, varies by route, recent > established.
**Why it fits:** the canonical UK net-fiscal estimate — the second major international benchmark (with StatCan IMDB and OECD IMO) for putting the US number in cross-country context. Its EEA/non-EEA and recent/established splits, and the "depends on age/skills/children" framing, map directly onto the project's composition-driven ledger and test whether the US low-skill-drag finding generalizes. The flagged international-comparison gap, UK leg, verified.
**Limit / honesty:** UK institutions (NHS, NRPF benefit restrictions, EEA free movement pre-Brexit) differ from US — benchmarks the METHOD and the composition-sensitivity, not US levels; the UK has no large unauthorized analog in these estimates. Static-accounting (not lifetime-NPV); results are method-sensitive (the authors and critics dispute net sign for some specifications). The paper is the artifact — to re-estimate you need the UK LFS (UK Data Service registration), not a packaged file. [SOURCE: cream-migration.org/publ_uploads/CDP_22_13.pdf]
**Graph fit:** international benchmark node; immigrant-group × period net-contribution; no row-level join — a published cross-country comparator beside StatCan IMDB and OECD IMO 2021.

---

## Summary — what this batch adds (12 cards)

| Card | Axis | Access | Scriptable? | Nativity/status field? |
|---|---|---|---|---|
| NAWS-PAD | legal-status labor | public, no reg | YES (CSV/SAS direct) | YES — legal/work-auth status (the only federal one) |
| OFLC-DISCLOSURE | legal-status labor | public | YES (Excel/flag.dol.gov) | partial — alien country/citizenship (PERM rich, LCA sparse) |
| NHIS-PUF | health | public, no reg | YES (CSV/SAS direct) | YES — citizenship/nativity (country restricted) |
| HCUP-NIS-NEDS | health cost | GATED (purchase+DUA) | NO (per-order; HCUPnet free but interactive) | NO — payer proxy only |
| IRS-ITIN-TAS-TIGTA | tax | public PDFs | parse-only | proxy — ITIN filer ≈ tax-paying unauthorized |
| SSA-ESF-NWALIEN | tax | public OIG PDFs (microdata restricted) | parse-only | proxy — nonwork-SSN/mismatch |
| AHS-PUF | housing | public, no reg | YES (CSV/SAS direct) | **likely NO on PUF — verify codebook** |
| USPTO-PATENTSVIEW | innovation | public (ODP sign-in) | YES (API+bulk) | NO — inventor country only |
| USPTO-INVENTOR-LINKED | innovation | public paper (microdata confidential) | parse-only | YES (immigrant status, high-skill only) |
| STATCAN-IMDB | intl admin-linked | public tables (microdata RDC-only) | YES (WDS API for tables) | YES — admission category, source country |
| TRAC-IMMIGRATION | flows/enforcement | public tools (bulk paid) | scrape-only (free tier) | YES — citizenship/nationality dimension |
| MMP | origin flow | public, free reg | YES (download) | YES — documentation status per US trip |
| DHS-OHSS-YEARBOOK | flows | public, no reg | YES (data tables) | YES — class of admission, country of birth |
| UK-DUSTMANN-FRATTINI | intl comparison | public paper | parse-only | n/a (EEA/non-EEA split) |

**Directly scriptable into `infra/immigration-fiscal/acquire/` now:** NAWS-PAD, OFLC-DISCLOSURE, NHIS-PUF, AHS-PUF, USPTO-PATENTSVIEW (API), STATCAN-IMDB (WDS API tables), MMP (post-registration), DHS-OHSS-YEARBOOK (data tables).
**PDF/parse like existing CBO/ITEP/EOIR:** IRS-ITIN-TAS-TIGTA, SSA-ESF-NWALIEN, USPTO-INVENTOR-LINKED, UK-DUSTMANN-FRATTINI.
**Gated/restricted:** HCUP (purchase+DUA), STATCAN-IMDB microdata (Canadian RDC), TRAC bulk (paid), SSA-ESF/IRS-SOI microdata (already-tracked restricted).

**[UNVERIFIED] flags carried forward:** (1) AHS-PUF nativity-field presence — must confirm in the 2023 PUF codebook before treating as a status dataset (most likely absent → ecological join only). (2) USPTO-INVENTOR-LINKED — openness of the forthcoming AER replication-archive contents (microdata is confidential regardless).
