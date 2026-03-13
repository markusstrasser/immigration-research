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
| Incarceration | Lower crime rates than natives (multiple studies) but nonzero | [SOURCE: Cato/Nowrasteh, Texas TDCJ data] |

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

*(Dataset discovery agent still running — will be appended)*
