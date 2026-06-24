# Immigration — Dataset Roadmap, Additions (2026-06-24)

Supplements `immigration-dataset-roadmap.md` (12 targets) and `immigration-dataset-register.md`
(what we hold). These are ADDITIONAL real datasets, scouted to fill the same two structural holes
(crime-by-status beyond Texas; admin-linked longitudinal earnings/fiscal; international comparison;
benefit-side innovation). All URLs verified live 2026-06-24 unless tagged `[UNVERIFIED]`.

Priority order requested: (1) crime w/ immigration status beyond TX, (2) admin-linked longitudinal
earnings/fiscal, (3) international fiscal comparisons, (4) benefit-side innovation/entrepreneurship.

---

## Axis 2 — Admin-linked longitudinal earnings / fiscal

### SSA-EPUF-2006 — Earnings Public-Use File (1-percent CWHS sample)
**Source:** Social Security Administration, ORES · **Access:** Public download (no registration)
**Official:** https://www.ssa.gov/policy/docs/data/index.html (file) · intro https://www.ssa.gov/policy/docs/ssb/v71n4/v71n4p33.html
**Key variables:** annual covered earnings 1951–2006 for 4.3M individuals (1% of all SSNs), birth year, sex, race, year of death; aggregate 1937–50. This is the public face of the Continuous Work History Sample (CWHS) the user asked about.
**Why it fits:** real administrative *longitudinal* earnings trajectories — the lifetime-NPV backbone the warehouse currently approximates from ACS cross-sections (flagged "do not use ACS alone for lifetime"). SSA's own "Research on Immigrant Earnings" trio (v68n1p31) documents foreign/native trajectory differences modelable on this structure.
**Limit / honesty:** EPUF has **no nativity/citizenship field** — immigrant identification is not in the public file (that requires the restricted CWHS/MEF linked to place-of-birth). So EPUF is a *native-baseline calibration* layer, not an immigrant-vs-native split by itself. The newer **BEPUF 2020** (released 2025) is fully synthetic. [SOURCE: ssa.gov/policy/docs/data/index.html]
**Graph fit:** native earnings-trajectory anchor for the lifetime warehouse; no direct nativity join — pairs with NIS / IPUMS for the immigrant arm.

### CENSUS-PSEO — Post-Secondary Employment Outcomes (LEHD)
**Source:** Census LEHD + state higher-ed + UI wage records · **Access:** Public tables + PSEO Explorer
**Official:** https://lehd.ces.census.gov/data/pseo_experimental.html · explorer https://lehd.ces.census.gov/data/pseo_explorer.html
**Key variables:** earnings (p25/p50/p75) 1/5/10 yrs after graduation by institution × degree level × field of study; flow/geography of graduates.
**Why it fits:** admin-linked (UI wage records) earnings outcomes by education — a returns-to-schooling layer that grounds the human-capital assumptions in the second-gen mobility story. **Limit:** no nativity; institution/field keyed, not person. Ecological complement to ABJP/Opportunity Atlas. [SOURCE: lehd.ces.census.gov/data/]
**Graph fit:** education × earnings; benefit-side calibration, joins by field/degree not by nativity.

### CENSUS-LED-EXTRACT (LODES/QWI raw via LED Extraction Tool)
**Source:** Census LEHD · **Access:** Public, ledextract.ces.census.gov + bulk CSV
**Official:** https://ledextract.ces.census.gov/ · LODES bulk https://lehd.ces.census.gov/data/#lodes
**Key variables:** LODES v8 (2002–2023) block-level home↔work job flows, jobs by industry/age/earnings band; QWI by demographic.
**Why it fits:** we already hold a QWI county receiver panel; LODES adds *residence↔workplace commuting* geography for receiver-shock spatial designs. **Limit: no nativity at all** (partially synthetic). Strictly ecological/exposure infrastructure, not a status dataset — include only as a geography backbone. [SOURCE: lehd.ces.census.gov/doc/help/onthemap/OnTheMapDataOverview.pdf]
**Graph fit:** block/county commuting geography; joins county context by FIPS.

---

## Axis 1 — Crime with immigration/citizenship status, BEYOND Texas (highest priority)

### ICPSR-39107-AZ — Immigration Status, Crime, Gang Affiliation & Victimization, Arizona 2007–2023
**Source:** Herrera (Cal State Fullerton), NIJ-funded; NACJD/ICPSR · **Access:** Public (ICPSR download; SDA online)
**Official:** https://www.icpsr.umich.edu/web/NACJD/studies/39107 · DOI 10.3886/ICPSR39107.v1
**Key variables:** self-report crime, gang membership, violent victimization, alcohol/drug use by immigration status (undocumented / legal immigrant / US-born); community sample + recently-booked arrestees (ADAM-style), Maricopa County AZ.
**Why it fits:** the **second** US micro-comparison of criminality by legal status after Light's Texas — and a *different* state, different method (self-report + arrestee booking, not DPS arrest universe). Directly enables a non-Texas robustness check on the crime-by-status finding, plus victimization (immigrants as victims, a frame the corpus lacks). [SOURCE: icpsr.umich.edu/web/NACJD/studies/39107]
**Graph fit:** `crime` domain; status × AZ; pairs with TX-DPS-LIGHT for cross-state generalization.

### BJS-NCRP-39234 — National Corrections Reporting Program, 1991–2021 (Selected Variables)
**Source:** Bureau of Justice Statistics (Abt collection agent) · **Access:** Public (selected-vars DS; complete ICPSR 39233 restricted)
**Official:** https://www.icpsr.umich.edu/web/NACJD/studies/39234 · DOI 10.3886/ICPSR39234.v1
**Key variables:** offender-level prison **admissions, releases, term records, year-end population** by state, 1991–2021; demographics, offense, sentence, time served; recidivism-relevant release/return linkage. The public file includes a citizenship/birthplace indicator on many state submissions (varies by state; complete file richer).
**Why it fits:** national, 30-year, offender-level corrections flow — supports incarceration **rate and recidivism** analysis by citizenship over time and across all reporting states, the longitudinal complement to the single-year BJS-SPI snapshot already on the roadmap. **Limit:** citizenship coverage is uneven across state submissions; confirm field completeness before relying. [SOURCE: icpsr.umich.edu/web/NACJD/studies/39234]
**Graph fit:** `crime`; state × year × citizenship; joins corrections-flow to the SPI stock snapshot.

---

## Axis 3 — International fiscal-impact comparison

### OECD-IMO2021-CH4 — Fiscal impact of immigration in OECD countries, 2006–18
**Source:** OECD International Migration Outlook 2021, Chapter 4 · **Access:** Public — free full-report HTML + READ (book PDF gated)
**Official:** https://www.oecd.org/en/publications/international-migration-outlook-2021_29f23e9d-en/full-report/component-8.html · annex tables in-chapter
**Key variables:** yearly **net fiscal impact** of immigrants in 25 OECD countries, 2006–18; per-item decomposition of every government revenue and expenditure line for foreign- vs native-born; socio-economic determinants of fiscal position.
**Why it fits:** puts the US net-fiscal number in internationally-comparable context using one consistent methodology — the cross-country benchmark the honorable-mentions list flagged `[UNVERIFIED]`, now verified with a free landing page and the per-line revenue/expenditure decomposition that maps onto our own ledger structure. Earlier 2013 edition also free. [SOURCE: oecd.org IMO 2021 full-report]
**Graph fit:** country-level benchmark node; the US row cross-checks the NAS/CBO domestic estimate; per-line decomposition validates ledger completeness.

[PENDING] — innovation/entrepreneurship axis + 1-2 more crime/fiscal admin sources to append.
