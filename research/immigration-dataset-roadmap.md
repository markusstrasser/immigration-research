# Immigration — Dataset Acquisition Roadmap

What we **want next** and why. The flat list of what we **have** is `immigration-dataset-register.md`;
raw-byte manifest is `sources/immigration-fiscal/data/MANIFEST.md`. Status: ✅ acquired · 🚧 gated/in-progress · ⬜ wanted, not started.

**Gap analysis (2026-06-24):** the existing stack is overwhelmingly **fiscal**. The two structural
holes are (1) **crime** — the project is "fiscal *and* crime impact" but has ~zero crime datasets, and
(2) **benefit-side / second-generation mobility** — the corpus's own audit flags a cost-side evidence
skew (`immigration-evidence-base-audit.md`). The targets below are chosen to fill exactly those holes.
All URLs/DOIs verified live 2026-06-24 (Exa) unless tagged `[UNVERIFIED]`.

---

## Frontier additions (2026-06-25 pass) — full cards in the linked memos

The 5-domain frontier pass surfaced these new targets. **Urban is the priority** (the missing
housing-incidence panel). Full dataset cards (vars/quirks/what-it-settles) live in each memo; this
is the grep-able index. Status: ✅ acquired · 🚧 gated/tiered · ⬜ wanted.

**Urbanism** → `immigration-urbanism-frontier-2026-06-25.md` (+ acquire `setup-urban-housing.sh`)
- **Zillow ZORI/ZHVI metro** ✅ acquired (739 metros, monthly 2015-2026 — the Wilson-Zhou outcome var)
- **WRLURI2018** (Wharton regulation index, 2006→2018 change panel) ⬜ — one-time DL, MANUAL_ACQUIRE
- **Geocorr2022 PUMA↔CBSA crosswalk** ⬜ — on-demand generator (query spec in MANUAL); resolves the unit-mismatch
- **LODES/LEHD** workplace×residence flows ⬜ — spatial-mismatch axis

**Sociology** → `immigration-sociology-frontier-2026-06-25.md`
- **GSS trust-by-nativity** (BORN/PARBORN × TRUST/FAIR/HELPFUL) ⬜ — **public, buildable NOW** (cheapest test)
- **CILS** (ICPSR 20520) ⬜ public · **NIS** (38031/38061) 🚧 tiered · **Add Health** 🚧 tiered (networks restricted)

**Policy / enforcement instruments** → `immigration-policy-frontier-2026-06-25.md`
- **Secure-Communities activation dates** (county×month) ⬜ — the staggered-rollout instrument
- **State E-Verify mandate dates** (NCSL) ⬜ · **DHS Yearbook enforcement tables** ⬜ · **TRAC** 🚧 · **ORR/ASR** 🚧 (microdata restricted)

**Crime** → `immigration-crime-frontier-2026-06-25.md`
- **AZ ICPSR 39107** (self-report offending/victimization/gang by fine status incl. DACA) 🚧 — only US person-level non-TX status data
- **NCVS-by-citizenship** (38962/38963 + BJS API) ⬜ — victimization axis; 2017+ only, can't isolate undocumented

---

## Cluster A — Crime (the biggest gap; repo name promises it, stack omits it)

### TX-DPS-LIGHT-2020 — Texas arrest rates by immigration status ⬜ **(highest priority)**
**Source:** Light, He & Robey (PNAS 2020), via Texas Dept. of Public Safety arrest records
**Access:** Public — openICPSR, free registration · **Official:** https://www.openicpsr.org/openicpsr/project/124923/version/V1/view · DOI 10.3886/E124923V1
**Key variables:** felony/misdemeanor/conviction arrest counts × {undocumented, legal immigrant, US-born}, Texas, 2012–2018; alternative undocumented-population denominators (CMS, Pew)
**Why it fits:** the single gold-standard micro-comparison of criminality by legal status — Texas is the only state that records immigration status of *all* arrestees. Directly answers the crime half of the central question. [SOURCE: pnas.org/doi/10.1073/pnas.2014704117]
**Graph fit:** new `crime` domain; bridges to existing stock layers by status × state.

### USSC-OFFENDERS — US Sentencing Commission Individual Offender Datafiles ⬜
**Source:** US Sentencing Commission, Office of Research and Data
**Access:** Public — SPSS/SAS download, annual, FY2002→ (also ICPSR + FJSRC/Urban) · **Official:** https://www.ussc.gov/research/datafiles/commission-datafiles
**Key variables:** citizenship (US citizen / legal alien / etc.), offense of conviction, criminal-history points/category, demographics — per federal offender (~64k/yr)
**Why it fits:** federal-offender composition by citizenship; isolates immigration offenses vs other crime. National, annual, free. [SOURCE: ussc.gov public release codebook]
**Graph fit:** `crime` domain; citizenship key joins to nativity stock.

### BJS-SPI-2016 — Survey of Prison Inmates 2016 ⬜
**Source:** Bureau of Justice Statistics (DS1 public-use)
**Access:** Public, no ICPSR membership (DS1); DS3 restricted · **Official:** https://www.icpsr.umich.edu/web/NACJD/studies/37692
**Key variables:** citizenship/nativity of state+federal prisoners, current offense, sentence, criminal history, socioeconomic background
**Why it fits:** incarceration **rate** by citizenship (the Butcher–Piehl method) — the standard rebuttal/test surface for "immigrant incarceration" claims. [SOURCE: bjs.ojp.gov SPI]
**Graph fit:** `crime`; complements ACS institutionalized-GQ-by-nativity (derivable from IPUMS we already hold).

### FBI-NIBRS-CDE — FBI incident + county-level crime ⬜
**Source:** FBI UCR / NIBRS via Crime Data Explorer; ICPSR UCR county series (57)
**Access:** Public bulk download · **Official:** https://cde.ucr.cjis.gov · county files https://www.icpsr.umich.edu/web/NACJD/series/57
**Key variables:** incident-level offense/arrest (52 offenses); county-level arrest+offense counts + population
**Why it fits:** enables the **ecological** immigration↔crime design (county crime rate vs county foreign-born share, the Ousey–Kubrin / Wadsworth approach) using panels we already have. **Limit:** no nativity at incident level — ecological only. [SOURCE: fbi.gov NIBRS]
**Graph fit:** joins to county context warehouse by FIPS.

### DOJ-SCAAP — State Criminal Alien Assistance Program award data ⬜
**Source:** DOJ Bureau of Justice Assistance
**Access:** Public PDFs (per-FY award details) · **Official:** https://bja.ojp.gov/program/state-criminal-alien-assistance-program-scaap · e.g. https://bja.ojp.gov/funding/scaap-fy23-awards.pdf
**Key variables:** per-jurisdiction criminal-alien inmate-days, correctional-officer counts, total inmates, DOJ reimbursement $ (FY)
**Why it fits:** the only national admin series tying **incarceration burden of criminal aliens to dollars** — a direct cost-side bridge between the crime and fiscal halves. [SOURCE: ojp.gov bja-2025-172612.pdf]
**Graph fit:** state/county × year; joins state-local cost ledger.

---

## Cluster B — Enforcement & direct unauthorized-cost channels

### ICE-ERO-STATS — ICE Enforcement & Removal Operations statistics ⬜
**Source:** US ICE
**Access:** Public — annual reports FY2013→ + dashboard Excel export · **Official:** https://www.ice.gov/statistics
**Key variables:** removals by criminality (convictions / pending charges / none), country, FY; detention, ATD
**Why it fits:** criminal-removal counts + enforcement intensity (FY2024: 88,763 of 271,484 removed had criminal charges/convictions) — both a crime-composition signal and an enforcement-cost driver. [SOURCE: ice.gov/doclib/eoy/iceAnnualReportFY2024.pdf]
**Graph fit:** complements CBP/ICE budget justifications already held; adds outcome counts to the cost inputs.

### CMS-EMERGENCY-MEDICAID — Emergency Medicaid for non-citizens (CMS-64) ⬜
**Source:** CMS (CMS-64 state financial reports); CBO compilation
**Access:** Public aggregates (CBO Oct-2024 letter has the table) · **Official:** https://www.cbo.gov/system/files/2024-10/Arrington_Letter_EmergencyMedicaid_Immigration_final.pdf
**Key variables:** federal + state emergency-Medicaid spend for persons ineligible for full Medicaid by immigration status, by FY (2017–23 = **$27B** total: $18B federal + $9B state)
**Why it fits:** replaces our **inferential** MEPS-based unauthorized-health-cost proxy with a **direct administrative** number — a real cost-side ledger line. [SOURCE: cbo.gov Arrington letter 2024-10-02]
**Graph fit:** state × year; slots into the stage-5 net-negative cost layer beside Medicaid/SNAP.

### HHS-ORR-UC — Office of Refugee Resettlement: UC + Refugee program ⬜
**Source:** HHS ACF Office of Refugee Resettlement
**Access:** Public — Annual Report to Congress + UC Portal monthly data · **Official:** https://www.hhs.gov/programs/social-services/unaccompanied-children + acf.gov/orr ARC PDFs
**Key variables:** UAC program appropriation & per-child cost, counts by origin country, length of care; refugee cash/medical/support program spend
**Why it fits:** a distinct **federal** unauthorized/humanitarian fiscal channel ($1.3B UC + $0.6B refugee, FY2021) absent from the current state-local-heavy cost stack. [SOURCE: acf.gov orr-arc-fy2021.pdf]
**Graph fit:** federal cost ledger; origin-country key joins origin layer.

---

## Cluster C — Benefit-side / second-generation mobility (corrects the flagged cost-side skew)

### ABJP-MOBILITY-120490 — Intergenerational mobility of immigrants over two centuries ⬜ **(high priority)**
**Source:** Abramitzky, Boustan, Jácome & Pérez (AER 2021)
**Access:** Public · **Official:** https://www.openicpsr.org/openicpsr/project/120490/version/V1/view · DOI 10.3886/E120490V1
**Key variables:** father–son rank-rank mobility by origin country, 1880–2015 (linked Census + CPS/Opportunity-Insights modern cohorts)
**Why it fits:** the headline **benefit-side** finding the corpus under-weights — children of immigrants from nearly every origin out-rise children of the US-born. Directly counters the "low-skill parent ⇒ permanent fiscal drag" frame in the welfare-ledger map. [SOURCE: aeaweb.org/articles?id=10.1257/aer.20191586]
**Graph fit:** second-generation node; origin-country key.

### OI-OPP-ATLAS-2NDGEN — Opportunity Atlas, 2nd-gen immigrant ranks ⬜
**Source:** Opportunity Insights + Census CES
**Access:** Public · **Official:** https://opportunityinsights.org/data + https://www.census.gov/programs-surveys/ces/data/public-use-data/opportunity-atlas-data-tables.html
**Key variables:** "Income Ranks for Second-Generation Immigrant Children by Parent Income, Country of Origin, Gender"; tract/county adult earnings **and incarceration** by parental income/race/sex
**Why it fits:** dual-purpose — second-gen earnings (benefit) **and** tract-level incarceration outcomes (crime), both by origin. Bridges Clusters A and C. [SOURCE: opportunityinsights.org/data]
**Graph fit:** tract/county × origin; joins county context + the new crime domain.

### CENSUS-ABS-CBO — Annual Business Survey, Characteristics of Business Owners ⬜
**Source:** US Census Bureau
**Access:** Public API · **Official:** https://www.census.gov/data/developers/data-sets/abs.html · api.census.gov/data/2023/abscbo
**Key variables:** business ownership by **USBORN** + **USCITIZEN** × NAICS industry × geography (US/state/metro/county), 2023 reference year
**Why it fits:** quantifies immigrant **entrepreneurship/job-creation** (the Azoulay-et-al benefit channel, cluster T07) with official microdata instead of secondary citation. [SOURCE: census.gov ABS CBO API tech doc]
**Graph fit:** owner-nativity × industry; benefit-side counterpart to the cost ledger.

### NIS — New Immigrant Survey ⬜
**Source:** Jasso, Massey, Rosenzweig, Smith (Princeton OPR / NYU / RAND)
**Access:** Public-use added 2024 (ICPSR 38031 R1 / 38061 R2); some restricted · **Official:** https://nis.princeton.edu + https://www.icpsr.umich.edu/web/DSDR/studies/38031
**Key variables:** longitudinal new-LPR + children: earnings trajectory, program use, health, schooling, skin-color/assimilation, origin
**Why it fits:** the only nationally-representative **longitudinal** immigrant panel — supports lifetime-NPV and program-use modeling on **both** ledger sides without the ACS cross-section limits flagged in "do not use" rules. [SOURCE: icpsr 38031/38061]
**Graph fit:** longitudinal individual layer; feeds the lifetime-evidence warehouse.

---

## Honorable mentions (real, not yet URL-verified this pass — `[UNVERIFIED]`)

- **OECD International Migration Outlook — fiscal chapter** — cross-country fiscal-impact benchmark (puts the US number in international context). `[UNVERIFIED]`
- **USPTO PatentsView + immigrant inventors** — patenting/innovation by inventor nativity (benefit channel). `[UNVERIFIED]`
- **DHS OHSS Yearbook of Immigration Statistics** — broader flows (we hold the OHSS state file; the Yearbook adds naturalization/nonimmigrant/enforcement). `[UNVERIFIED]`
- **TRAC Immigration (Syracuse)** — court/detention/enforcement FOIA series (extends our EOIR layer). `[UNVERIFIED]`

## Acquisition notes

- Crime cluster needs a new `crime` schema in the warehouse (or a `crime` namespace in the unified DB) — none exists today.
- TX-DPS-LIGHT, ABJP-MOBILITY, USSC, NIS, BJS-SPI are openICPSR/ICPSR direct downloads → scriptable into `infra/immigration-fiscal/acquire/`.
- CMS Emergency Medicaid + SCAAP + ICE-ERO + ORR are PDF/Excel admin releases → parse like the existing CBO/EOIR PDFs.
- Census ABS is an API pull (like the existing ACS/QWI pulls).
