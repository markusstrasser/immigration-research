# Fiscal Impact of Unauthorized Immigration — Research Memo

**Question:** What is the total lifetime fiscal cost of an unauthorized Mexican immigrant to the US? What are the categories, and how do methodological choices drive results?
**Tier:** Deep | **Date:** 2026-03-13
**Ground truth:** Prior conversation established the methodological framework (buckets, 6 binary methodological choices). This memo adds sourced empirical estimates and causal structure.

---

## Causal Structure (DAG Summary)

**Treatment:** Presence of one additional unauthorized immigrant
**Outcome:** Net fiscal balance (taxes paid − government expenditures)
**Null:** Zero net fiscal impact

### Minimal adjustment set: {Human capital at entry, Labor market conditions, Policy environment, Economic cycle}

### 14 mediator pathways from Treatment → Outcome:
| Pathway | Direction | Measurability |
|---------|-----------|---------------|
| Employment → wages → income/payroll tax | Revenue (+) | Moderate (ITIN data, SSA Suspense File) |
| Payroll tax w/o benefit claim (SSA mismatch) | Revenue (+) | Good (~$13B/yr into Suspense File) |
| Children → K-12 education costs | Cost (−) | Good (school enrollment data) |
| Healthcare → EMTALA / uncompensated care | Cost (−) | Poor (attribution crude) |
| Native wage displacement → changed native taxes | Ambiguous | Poor (Card/Borjas unresolved 30 years) |
| Enforcement costs (ICE/CBP/courts) | Cost (−) | Good (public budgets) |
| Intergenerational (children enter workforce) | Revenue (+, long-run) | Moderate (NAS projections) |
| Consumption → sales/excise tax | Revenue (+) | Poor (no direct measurement) |
| Remittances → reduced domestic multiplier | Cost (−, indirect) | Moderate (flow measurable, multiplier modeled) |

### Key colliders (DO NOT condition on):
- **Apprehension/deportation** — conditioning = survivor bias
- **Observability in admin data** — conditioning on "immigrants in our dataset" = selection on institutional engagement. **Every empirical estimate in the literature has this bias.**

### Biggest threats to causal identification (ranked):
1. Public goods attribution (marginal vs. average cost) — largest swing factor
2. Time horizon and discount rate — determines if intergenerational gains count
3. Selection on observability — datasets miss least-visible immigrants
4. Level-of-government aggregation — federal positive + state/local negative
5. SUTVA violation — per-person estimates don't scale linearly
6. Unobserved selection — who migrates is endogenous
7. Native wage displacement magnitude — empirically unresolved

**Bottom line from DAG:** The total causal effect is **not cleanly identifiable** with existing data. No valid adjustment set blocks all back-door paths (unobserved motivation/drive is unblockable). Any estimate presented without sensitivity analysis across threats 1, 2, and 4 should be treated as an advocacy number.

---

## Empirical Estimates by Source

### NAS 2017 (Gold standard)
*The Economic and Fiscal Consequences of Immigration*, National Academies Press, 2016.
Summarized in Orrenius 2017 (Dallas Fed WP 1704) — full text obtained.

**Key findings:**
- 8 scenarios run, varying public goods assumption, discount rate, time horizon
- **With marginal cost of public goods:** long-run fiscal impact is **positive**; short-run negative but very small (less negative than natives) [SOURCE: Orrenius 2017, full text]
- **With average cost of public goods:** fiscal impact **negative** in both short and long run [SOURCE: Orrenius 2017]
- Highly-educated immigrants: large positive fiscal impacts regardless of methodology [SOURCE: Orrenius 2017]
- Net costs concentrated at **state/local level**, largely due to K-12 [SOURCE: Orrenius 2017]
- Range across 8 scenarios (annual, all immigrants pooled): **−$43B to −$299B** per year [SOURCE: NumbersUSA citing NAS data]
- 2nd generation children of immigrants are "among the strongest net fiscal contributors of any demographic group" [SOURCE: NAS 2017 via Orrenius]

**Critical methodological note:** NAS pools legal and unauthorized immigrants. No separate unauthorized-only estimates in the 8 scenarios. Unauthorized-specific estimates require extrapolation.

### CBO (2024)
*Effects of the Immigration Surge on the Federal Budget and the Economy*

- **Federal revenues increase $1.2 trillion** over 2024-2034 from immigration surge [SOURCE: CBO pub 60569]
- Annual revenue effect reaching **$167 billion** (2.2% of total revenues) by 2034 [SOURCE: CBO pub 60569]
- Net deficit reduction **$296 billion** from 2024-2028 [SOURCE: The Hill, citing CBO]
- Discretionary spending pressure ~**$200 billion** 2024-2034 [SOURCE: Sen. Grassley, citing CBO]
- **Federal only** — excludes state/local costs [SOURCE: House Budget Committee]
- NYC alone spent **$4.3 billion** July 2022 – March 2024 on immigrant accommodation [SOURCE: CBO pub 60569]
- ~40% of surge population remains ineligible for most government financial support after 10 years [SOURCE: AEI, citing CBO]

**Critical note:** CBO estimates are federal-only and cover the recent immigration surge (2021+), not steady-state unauthorized population. These numbers cannot be directly compared to NAS lifetime estimates.

### Heritage Foundation (Rector, 2023)
Senate Budget Committee testimony, September 2023.

- Net long-term fiscal cost of illegal immigration: ~**$5 trillion** total [SOURCE: Rector testimony, congress.gov PDF]
- ~**$50,000** per household paying income taxes [SOURCE: Rector testimony]
- Current net fiscal cost: at least **$110 billion annually** [SOURCE: Heritage 2024 report]
- Each illegal immigrant household: ~**$20,000/year** net cost [SOURCE: Heritage 2024]
- FY 2004 data: low-skill immigrant household net deficit ~**$19,588/year** ($30,160 benefits − $10,573 taxes) [SOURCE: Heritage testimony to state fiscal cost hearing]

**Methodological issues (from DAG analysis):**
- Uses **average cost** attribution (assigns pro-rata share of defense, interest on debt, etc.)
- Attributes US-born children's costs to "immigration" column
- Short time horizon (doesn't credit intergenerational fiscal gains)
- Does not use marginal cost framework preferred by most economists

### CIS / Camarota (2024 congressional testimony)
*The Cost of Illegal Immigration to Taxpayers*, prepared testimony for the House Judiciary immigration subcommittee.

- Claims a lifetime fiscal drain of **`-$68,390`** per illegal immigrant in 2023 dollars [SOURCE: https://www.congress.gov/118/meeting/house/116727/witnesses/HHRG-118-JU01-Wstate-CamarotaS-20240111.pdf]
- Claims **`59.4%`** of illegal-immigrant-headed households use one or more welfare programs and that those programs cost roughly **`$42B`** [SOURCE: same testimony]
- Claims roughly **`$68.1B`** in K-12 costs from children of illegal immigrants in public school, mostly U.S.-born [SOURCE: same testimony]

**Assessment:**
- The testimony is **not a neutral baseline estimate**. It is congressional advocacy from CIS, which openly describes itself as pursuing a `pro-immigrant, low-immigration vision`. [SOURCE: https://cis.org/Center-For-Immigration-Studies-Background]
- The core mechanism tying lower education to lower tax payments is mainstream and consistent with NAS/Orrenius. [SOURCE: https://doi.org/10.24149/wp1704] [SOURCE: https://www.nap.edu/catalog/23550/the-economic-and-fiscal-consequences-of-immigration]
- The scalar estimates are **model outputs**, not direct measurements. The `-$68,390` figure is Camarota's construction from averaged NAS scenarios plus CIS legality adjustments; it is not a National Academies estimate for unauthorized immigrants. [SOURCE: https://www.congress.gov/118/meeting/house/116727/witnesses/HHRG-118-JU01-Wstate-CamarotaS-20240111.pdf] [SOURCE: https://www.nap.edu/catalog/23550/the-economic-and-fiscal-consequences-of-immigration]
- The welfare and population estimates depend on inferred unauthorized status in survey data, exactly the kind of fragile residual/imputation problem highlighted in recent methods work. [SOURCE: https://www.ssa.gov/policy/docs/ssb/v85n2/v85n2p1.html] [SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC9107075/] [SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC12439705/]
- The school-cost estimate is fair only within a **current local-budget incidence** frame that assigns U.S.-born children's K-12 costs to immigration; it is incomplete as a total lifetime fiscal estimate unless those children's later tax contributions are also counted. [SOURCE: https://www.urban.org/sites/default/files/publication/90796/state_and_local_fiscal_effects_of_immigration.pdf] [SOURCE: https://doi.org/10.24149/wp1704]

**Repo classification:** Use Camarota as an adversarial source and a generator of categories/claims to verify, not as the repo's baseline estimator. See [immigration-fiscal-camarota-cis-testimony-audit.md](/Users/alien/Projects/research/research/immigration-fiscal-camarota-cis-testimony-audit.md).

### Cato Institute (Bier, Feb 2026) [CONTESTED]
*Immigrants' Recent Effects on Government Budgets: 1994–2023*

- Claims immigrants **reduced deficits by $14.5 trillion** (real 2024 $) from 1994-2023, including $3.9T in interest savings [SOURCE: Cato white paper, Feb 2026]
- Without immigrants, public debt would be **205% of GDP** (vs ~100% actual) [SOURCE: Cato white paper]
- Updates NAS methodology with newer corporate tax incidence research, property value effects, improved mixed-status household attribution [SOURCE: Cato white paper]

**Published criticisms:**
- **Camarota (CIS):** Cato "exclude[s] all the costs the U.S.-born dependent child of immigrants create for the welfare system and education" — allows a population with "relatively heavy welfare use and relatively lower tax payment" to appear fiscally positive [SOURCE: Newsweek, Feb 2026]
- **Beck (NumbersUSA):** Points to NAS data showing "all eight scenarios resulted in an annual fiscal drain of between $43 billion and $299 billion" as contradicting Cato's $14.5T surplus [SOURCE: Newsweek, Feb 2026]
- **Di Martino (Manhattan Institute):** Published critique claiming "our math doesn't add up." Cato responded with two-part rebuttal claiming MI's criticisms were about presentation, not methodology [SOURCE: Nowrasteh blog, Mar 2026]

**User note:** User flagged this study as "destroyed on Twitter — very unprofessional and bad research... very dishonest." The core dispute is the attribution of US-born children's costs — the single largest swing factor identified in both the DAG analysis and the NAS methodology.

### Manhattan Institute (Di Martino, Oct 2025)
*Lifetime Fiscal Impact of Immigrants*

- Average immigrant: modest positive **$10,000** in present value over lifetime (federal only) [SOURCE: Cato WP 82 reviewing MI report]
- Immigrants without bachelor's degree: "extremely fiscally negative" [SOURCE: Cato WP 82]
- Recent migration surge: projected cost of **$1.1 trillion** over a century (federal) [SOURCE: Cato WP 82]

---

## Labor Market Effects (2nd Order)

### The Borjas-Peri Debate

| Researcher | Finding | Method | Source |
|------------|---------|--------|--------|
| **Peri** (Berkeley) | Immigration 1990-2006: **−0.7%** wage effect on native low-skill (short run), **+0.3%** (long run) | Task-based framework, immigrants as complements | [SOURCE: Exa search result, papers.economics.ubc.ca/legacypapers/peri.pdf] |
| **Borjas** (Harvard) | **3-4%** wage decline for native high-school dropouts from immigration | Education-experience cells, immigrants as substitutes | [SOURCE: Exa search result, Card-Peri JEL review of Borjas 2014] |
| **Meta-analysis** (88 studies, 1985-2023) | Mixed results, vary by methodology and assumptions | Survey of literature | [SOURCE: Exa search result, halshs-05052498] |

**Key insight from DAG:** Native wage displacement (M3) is a mediator, not a control. Studies that condition on employment status or income level are estimating conditional effects, not total effects. Most existing estimates commit this error.

---

## Specific Cost Categories

### Taxes paid (revenue side)
| Category | Estimate | Source |
|----------|----------|--------|
| Payroll taxes (FICA) | 50-75% of unauthorized workers pay via ITIN or mismatched SSN | [TRAINING-DATA — widely cited, needs verification] |
| SSA Earnings Suspense File | ~$13B/year in wages with no-match SSNs | [TRAINING-DATA — SSA actuary reports] |
| Effective state/local tax rate | ~8% for unauthorized immigrants | [TRAINING-DATA — ITEP estimates] |
| ITIN filing (income tax) | ~4.4M individual tax returns filed with ITINs (2015) | [TRAINING-DATA — IRS data] |

### Costs (expenditure side)
| Category | Estimate | Source |
|----------|----------|--------|
| K-12 education | ~$15K/year avg per pupil × children in household | [TRAINING-DATA — NCES per-pupil data] |
| Emergency healthcare (EMTALA) | Mandated regardless of status | Statutory — no clean aggregate estimate found |
| Medicaid for citizen children | Citizen children of unauthorized parents eligible | Statutory |
| SNAP/WIC for citizen children | Citizen children eligible | Statutory |
| Immigration enforcement (total) | CBP + ICE + EOIR budgets are public | To be quantified from DHS data |
| Incarceration | Lower crime rates than natives — see [immigration-crime-rates-unauthorized-vs-native-born.md](immigration-crime-rates-unauthorized-vs-native-born.md) for full evidence review (Light et al. 2020 PNAS, Ousey & Kubrin 2018 meta-analysis, Gunadi 2019 IV) | [SOURCE: PNAS 117(51); Cato/Nowrasteh Texas DPS data] |

### Remittances
| Year | Amount to Mexico | Source |
|------|-----------------|--------|
| ~2023 | ~$63B (total, all immigrants) | [TRAINING-DATA — World Bank Remittance data] |

**Note:** Not all remittances to Mexico come from unauthorized immigrants. Legal immigrants and naturalized citizens also remit. No clean decomposition by status exists.

---

## The Cato Study Controversy — Detailed

The core methodological dispute centers on **one question**: When an unauthorized immigrant has a US-born child, and that child costs $15K/year in K-12 education, whose fiscal column does that go in?

- **Cato/NAS (some scenarios):** The child is a US citizen. Their costs go in the "native" column. The immigrant's fiscal ledger only includes their own taxes and their own direct benefit consumption.
- **Heritage/CIS:** The child would not exist in the US absent the immigration. The child's costs are causally attributable to immigration and belong in the "immigrant" column.

**From the DAG analysis:** Children (M4) are a **mediator** on the causal path X → M4 → Y. The child's fiscal costs are part of the causal effect of immigration. However, the child's own lifetime fiscal trajectory (M11) is also part of the causal effect — and NAS shows this is typically net positive. You cannot count children's costs without also counting children's eventual contributions.

Heritage counts the costs but uses a short horizon that excludes the contributions. Cato excludes both from the immigrant column. Neither approach captures the full causal effect correctly.

**The honest specification:** Include children's K-12 costs AND children's lifetime fiscal trajectory, with explicit discount rate sensitivity analysis. NAS 2017 did this — and the sign depends on the discount rate.

---

## Methodological Choices That Drive Results

| Choice | Heritage answer | Cato answer | Effect on estimate |
|--------|----------------|-------------|-------------------|
| Public goods cost attribution | Average cost (pro-rata) | Marginal cost (~zero) | **Largest swing** — $100K+ per household lifetime |
| Attribution of US-born children | Include as immigration cost | Exclude (they're citizens) | **Second largest** — flips sign |
| Time horizon | 10-20 years | 75+ years with descendants | Long horizon → more positive |
| Discount rate | 3%+ | 0% (or low) | High discount → intergenerational gains vanish |
| Level of government | All levels | Federal emphasized | Federal-only → more positive |
| Marginal vs average benefit cost | Average | Marginal | Marginal → more positive |

---

## What's Uncertain

1. **No unauthorized-specific NAS estimates exist.** NAS pools all immigrants. Heritage and Cato attempt unauthorized-specific estimates but with opposite methodological choices.
2. **SSA Earnings Suspense File data** — the ~$13B/year figure is [TRAINING-DATA] and needs verification against current SSA actuarial reports.
3. **ITEP state/local tax estimates** — the 8% effective rate is [TRAINING-DATA] and needs verification.
4. **Healthcare costs** — no clean aggregate estimate of EMTALA costs attributable to unauthorized immigrants was found in this search.
5. **Remittance decomposition** — total to Mexico is ~$63B but share from unauthorized immigrants specifically is unknown.
6. **The Borjas-Peri debate remains empirically unresolved** after 30+ years. A meta-analysis of 88 studies found results vary by methodology.

---

## Sources Saved to Corpus

- Orrenius 2017 "New Findings on the Fiscal Impact of Immigration in the United States" (Dallas Fed WP 1704) — **full text obtained**

## Sources Identified but Not Yet in Corpus

- NAS 2017 full report (book-length, $85)
- CBO pub 60569 (403 on WebFetch)
- Rector 2023 Senate testimony (PDF)
- Di Martino 2025 Manhattan Institute report
- Cato 2026 white paper
- Card-Peri JEL review of Borjas (2014)
- Meta-analysis of 88 wage effect studies (2023)

---

## Dataset Catalog

**Fundamental constraint:** No US dataset directly identifies unauthorized status. All analyses use the **residual method** (subtract legal immigrants from total foreign-born) or imputation filters. Error margins ~10-15%.

### Priority 1: Core Fiscal Data

| # | Dataset | What it gives you | Access | Immigration ID | Used by |
|---|---------|------------------|--------|----------------|---------|
| 1 | **CPS ASEC** | ~100K HH. Income, benefit receipt (SNAP, Medicaid, SSI, TANF), employment, nativity, citizenship | [census.gov](https://www.census.gov/data/datasets/time-series/demo/cps/cps-asec.html) or [IPUMS](https://cps.ipums.org) — free | Residual method required | NAS 2017, CBO, Pew |
| 2 | **SIPP** | ~50K HH longitudinal panel. Most detailed public benefit receipt data | [census.gov](https://www.census.gov/programs-surveys/sipp/data/datasets.html) — free | Residual method | NAS 2017 |
| 3 | **ACS PUMS** | ~3.5M persons/yr. Best for state/local due to large N. Income, housing, education, citizenship, year of entry | [census.gov](https://www.census.gov/programs-surveys/acs/microdata.html) or [IPUMS-USA](https://usa.ipums.org/usa/) — free | Residual method. CMS publishes ACS-derived unauthorized estimates by state | State-level analyses |
| 4 | **SSA Earnings Suspense File** | Payroll taxes paid with mismatched SSNs (proxy for unauthorized contributions) | **NOT public** (PII). Aggregate stats in [SSA Actuarial Note 151](https://www.ssa.gov/oact/NOTES/pdf_notes/note151.pdf) and [OIG audits](https://oig.ssa.gov/) | Direct proxy | SSA actuarial estimates (~$12B/yr OASDI contribution) |

### Priority 2: Cost-Side Data

| # | Dataset | Fiscal component | Access |
|---|---------|-----------------|--------|
| 5 | **NCES Education Finance** | K-12 per-pupil expenditure by state/district (largest state/local cost) | [nces.ed.gov](https://nces.ed.gov/ccd/elsi/) — free |
| 6 | **MEPS** | Individual healthcare utilization & expenditure (~40K persons/yr) | [meps.ahrq.gov](https://meps.ahrq.gov/) — free |
| 7 | **DOJ/BOP + SCAAP** | Incarceration costs. Federal: [$44,090/yr per prisoner (FY2023)](https://www.federalregister.gov/documents/2025/12/15/2025-22777/annual-determination-of-average-cost-of-incarceration-fee-coif). SCAAP reimburses states for incarcerating undocumented aliens | [bjs.ojp.gov](https://bjs.ojp.gov/document/fpscufsa24.pdf), [bja.ojp.gov](https://bja.ojp.gov/program/state-criminal-alien-assistance-program-scaap/overview) |
| 8 | **DHS Budget (CBP/ICE/EOIR)** | Enforcement line items | [dhs.gov](https://www.dhs.gov/dhs-budget) — Congressional Budget Justifications (PDF) |
| 9 | **USDA/FNS (SNAP/WIC)** | Benefit participation & costs. Unauthorized ineligible; their US-citizen children eligible | [fns.usda.gov/snap](https://www.fns.usda.gov/pd/supplemental-nutrition-assistance-program-snap), [fns.usda.gov/wic](https://www.fns.usda.gov/pd/wic-program) — free |

### Priority 3: Tax Revenue Data

| # | Dataset | What it gives you | Access |
|---|---------|------------------|--------|
| 10 | **IRS ITIN filing data** | Returns filed & taxes paid by ITIN holders (predominantly unauthorized) | [IRS Data Book](https://www.irs.gov/statistics/soi-tax-stats-irs-data-book) — aggregate only |
| 11 | **ITEP estimates** | Microsimulation of state/local taxes paid by unauthorized immigrants. Headline: ~$96.7B total taxes (2022) | [itep.org](https://itep.org/undocumented-immigrants-taxes-2024/) — free. Note: advocacy-adjacent org, cross-check |
| 12 | **State comptroller reports** | Texas 2006 (positive state, negative local). CBO state/local: [$9.2B cost in 2023](https://www.cbo.gov/publication/61464) | Various PDFs |

### Priority 4: Labor Market Data

| # | Dataset | Access | Note |
|---|---------|--------|------|
| 13 | **LEHD / QWI** | [QWI](https://ledextract.ces.census.gov/static/data.html) free; microdata restricted (FSRDC only) | No immigration status. Useful for wage/industry analysis |
| 14 | **QCEW** | [bls.gov](https://www.bls.gov/cew/downloadable-data-files.htm) — free CSV | Aggregate employer-level. Cross-reference with ACS industry × nativity |

### Priority 5: Integration/Outcomes

| # | Dataset | Access | Limitation |
|---|---------|--------|-----------|
| 15 | **NIS** | [nis.princeton.edu](https://nis.princeton.edu/data.html) — free | Legal immigrants only (2003 cohort). Comparator group, not direct |
| 16 | **CILS** | [ICPSR](https://www.icpsr.umich.edu/web/DSDR/studies/20520) — free with registration | 2nd-gen outcomes, 1991-2006, two metros only. Dated. |

### Key Derived/Population Sources

| Source | URL | Provides |
|--------|-----|----------|
| Pew unauthorized estimates | [pewresearch.org](https://www.pewresearch.org/unauthorized-immigrant-estimates) | State-level counts by year (residual method on CPS) |
| CMS estimates | [cmsny.org](https://data.cmsny.org) | ACS-derived counts by state, year, country of origin |
| DHS estimates | [ohss.dhs.gov](https://ohss.dhs.gov/topics/immigration/illegal/population-estimates) | Official DHS estimates |
| SSA Actuarial Note 151 | [ssa.gov](https://www.ssa.gov/oact/NOTES/pdf_notes/note151.pdf) | Unauthorized worker effects on Social Security trust funds |
| NAS 2017 full report | [nap.nationalacademies.org](https://nap.nationalacademies.org/read/23550) | Canonical methodology and estimates |

### Dataset Gaps

1. **No dataset directly identifies unauthorized status.** Everything depends on residual method (+/- 10-15%).
2. **SSA Earnings Suspense File microdata is a black box.** Best proxy for payroll tax contributions, but only aggregate OIG/actuarial figures available.
3. **Tax compliance rates are assumed, not measured.** ITEP assumes 50-75% income tax compliance. True rate unknown.
4. **Emergency Medicaid costs** have no clean aggregate attributable to unauthorized immigrants.
5. **Dynamic/long-run effects are model-dependent** — not a data gap, but a framing choice.

## Revisions

- **2026-03-13:** Added a source audit for the January 2024 Camarota/CIS testimony and downgraded it from "another estimate" to "adversarial briefing with reusable subclaims only". Trigger: [2026-03-13-treat-cis-camarota-as-advocacy-not-baseline](/Users/alien/Projects/research/decisions/2026-03-13-treat-cis-camarota-as-advocacy-not-baseline.md).
