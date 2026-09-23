# Pricing the two largest pro-side benefits: cheaper immigrant-intensive services and more high-skill native women's hours

## Current correction — September 19, 2026

**Verdict:** Retain these as extrapolation scenarios, not a bound on all benefits or a demonstrated offset to the fiscal account. The numerator removes about 3.17 million Mexico-born high-school-dropout workers; the $291bn denominator covers about 40.9 million current Mexican-origin residents across generations. Those are different population counterfactuals. The reported 7.5% and 3% ratios are scale comparisons, not an identified net benefit or deficit offset. The $21.8bn sum also combines private welfare and tax receipts. [SOURCE: tables below; INFERENCE]

The 2026 Kim–Leung–Weinberger paper finds lower consumer-packaged-goods prices through demand/search; it is not a failed replication of a services-price outcome. Barrett–Tan reports an imprecise other-services result, which does not establish zero. Neither finding supplies an upper bound on all price benefits. An implausible extrapolation is not a mathematical upper bound, and omitted sectors or equilibrium responses can move estimates either way. [SOURCE: [Kim et al., full paper](https://ryansungryongkim.github.io/papers/KLW_25Feb2026.pdf); [Barrett–Tan](https://www.imf.org/-/media/Files/Publications/WP/2025/English/wpiea2025005-print-pdf.ashx); INFERENCE]

This correction governs conflicting claims in the retained assessment below. Evidence and scope: [five-day cross-check](immigration-five-day-cross-check-2026-09-19.md).

## Retained assessment and evidence

**Verdict:** Both channels are real and both are **an order of magnitude too small to close the Mexican-origin fiscal gap**. Taking the published elasticities at face value and extrapolating them log-linearly to the removal of every Mexico-born high-school dropout from the labor force, natives lose about **$23.8bn a year** of consumer surplus on immigrant-intensive services and about **$8.7bn a year** of federal, state and payroll tax on the extra hours worked by high-wage native college-educated women. Netting the same paper's implied **$10.7bn wage gain to native high-school dropouts** leaves a defensible native total of **$21.8bn a year**, or **7.5% of the $291bn reference gap** and **8.6% of the $254bn complete-account absolute balance** [SOURCE: ladder 123 / 130, `immigration-confidence-ladder.md`]. The purely *fiscal* offset is **$8.7bn, 3.0% of the reference gap**. Under the conservative arm the totals are $10.5bn and $4.4bn. Two independent post-2008 US studies fail to reproduce the services-price channel at all.

Generator: [`infra/immigration-fiscal/consumer_price_benefit_2026_09_18/`](../infra/immigration-fiscal/consumer_price_benefit_2026_09_18/RESULT.md). Every table is in `derived/*.csv`.

## 1. Summary table

Annual flows, 2024 dollars, national, first-order. "lf_adjusted" shock throughout: the removed workers leave the labor force as well as the numerator.

| Item | Central arm | WP-elasticity arm | Conservative arm |
|---|---:|---:|---:|
| **A.** Consumer surplus on immigrant-intensive services ($bn) | 23.76 | 15.03 | 11.48 |
| A, broad scope incl. other non-traded and food away from home ($bn) | 30.04 | 21.30 | 14.61 |
| A-offset. Native high-school-dropout wage gain forgone ($bn) | −10.73 | −10.73 | −5.31 |
| **A net ($bn)** | **13.03** | **4.30** | **6.17** |
| **B.** Private earnings of top-quartile native college women ($bn) | 24.94 | 11.48 | 12.47 |
| **B-tax.** Tax on those earnings at 35% ($bn) | **8.73** | **4.02** | **4.36** |
| **Defensible native total = A net + B-tax ($bn)** | **21.76** | **8.31** | **10.54** |
| Per Mexico-born low-skill worker, total ($) | 6,873 | 2,626 | 3,328 |
| Per Mexico-born low-skill worker, fiscal only ($) | 2,757 | 1,269 | 1,378 |
| Share of the −$290.59bn gap vs third-plus NH whites | 7.5% | 2.9% | 3.6% |
| Share of the −$354.28bn complete-account gap vs whites | 6.1% | 2.4% | 3.0% |
| Share of the −$254bn complete-account absolute | 8.6% | 3.3% | 4.2% |
| **Fiscal-only share of the −$290.59bn gap** | **3.0%** | **1.4%** | **1.5%** |

[SOURCE: `derived/summary_table.csv`; fiscal denominators from ladder entries 123 and 130.]

**What this does and does not offset.** Only the B-tax line is a budget item. The consumer surplus in row A is a real-income gain to native households; it never appears in any fiscal ledger and cannot be subtracted from a deficit. The B private-earnings line is *not* additive to A in welfare terms: the extra hours are bought by giving up leisure and home production worth roughly the market wage at the margin, so the woman's own net gain is second-order (envelope theorem) while the tax she pays on them is a first-order fiscal externality. Adding row A to row B's gross earnings would double-count [INFERENCE]. Anyone who wants to claim the full $30bn broad-scope figure must also accept Cortes's own accounting that 50–80% of the price effect is a wage cut to low-skilled workers, i.e. a transfer, not new output.

## 2. Part A method: consumer prices

**The elasticity, and a published-versus-working-paper discrepancy.** The published JPE abstract states: "at current immigration levels, a 10 percent increase in the share of low-skilled immigrants in the labor force decreases the price of immigrant-intensive services, such as housekeeping and gardening, by **2 percent**" [SOURCE: https://www.journals.uchicago.edu/doi/10.1086/589756 and https://econpapers.repec.org/article/ucpjpolec/v_3a116_3ay_3a2008_3ai_3a3_3ap_3a381-422.htm, fetched 2026-09-18]. The 2005/2006 working paper of the same study states **1.3 percent**, with **0.2 percent** for "the average non-traded good" [SOURCE: https://www.economics.uci.edu/files/docs/colloqpapers/w06/Cortes.pdf, 49pp, fetched 2026-09-18, p.1 and p.44; identical text at https://cream-migration.org/files/Patricia_Cortes_Paper.pdf and in the MIT thesis, http://hdl.handle.net/1721.1/37414]. The published number is 54% larger than the working-paper number for the same study. The working paper's structural section supplies the likely reason: its preferred structural estimate θ = −0.483 implies housekeeping services (low-skilled wage-bill share 0.4) fall **1.93 percent** per 10 percent, i.e. the published 2% appears to be the structural rather than the reduced-form figure [SOURCE: same WP, Table 10 discussion]. I carry both as arms and neither as the truth.

**Definitions, taken verbatim.** The treatment variable is the log of the share of **foreign-born high-school dropouts in the labor force**, restricted to people aged 16–64 reporting labor-force participation; an immigrant is a naturalized citizen or a non-citizen [SOURCE: Cortes WP §2]. "Immigrant-intensive services" in the reduced-form price regression are exactly six CPI items: **baby-sitting, housekeeping, gardening, dry cleaning, shoe repair and barber shops** (Table 3 note, 25 cities × 6 industries = 300 observations) [SOURCE: same, Table 3]. The price data are the confidential BLS CPI research database, A-sized cities only, covering **1986–2002**, with most analysis on 1990–2000 changes. Construction is *not* in the price sample, a gap Holzer flags explicitly [SOURCE: Urban Institute, *Immigration Policy and Less-Skilled Workers in the United States*, Holzer, n.29–31].

**The shock.** ACS 2024 1-year PUMS, civilian labor force aged 16+: foreign-born high-school dropouts are **6,635,078 of 175,478,713**, a share of **3.781%**. The Mexico-born component is **3,165,994**, or **1.804% of the labor force and 47.7% of all low-skilled immigrants**. Removing them (from numerator and from the labor force) takes the share to **2.013%**, a 46.8% reduction, Δln(share) = **−0.6303** [SOURCE: `derived/lowskill_share.csv`, `derived/acs_audit.json`].

Converting the published statement to a coefficient uses Cortes's own convention. Her working paper converts a coefficient of −0.043 into "0.4 percent per 10 percent", which is −0.043 × ln(1.1); so β = ln(1 − x/100)/ln(1.1). The published 2% gives **β = −0.2120**, the working paper's 1.3% gives **−0.1373**, and the average non-traded good's 0.2% gives **−0.0210**.

Applying β to Δln(share) gives a price rise of **+14.29%** on immigrant-intensive services in the central arm, +9.04% under the working-paper elasticity, +6.91% under half the published elasticity, and +1.34% on other non-traded goods.

**Expenditure mapping.** BLS Consumer Expenditure Survey 2024, Table 1101 (income quintiles) crossed with Table 2500 (all consumer units, detailed lines). Detailed lines do not exist by quintile, so each detail line's national share of its Table 1101 parent is applied to that parent's quintile mean — an explicit constant-composition assumption [METHOD].

| CEX detail line | Mean per CU | Parent | Tier |
|---|---:|---|---|
| Babysitting, childcare, daycare, preschool | $470.46 | Personal services | immigrant-intensive |
| Personal care services (barber, beauty, nail) | $478.51 | Personal care products and services | immigrant-intensive |
| Gardening and lawn care service | $238.02 | Other household expenses | immigrant-intensive |
| Housekeeping services | $186.25 | Other household expenses | immigrant-intensive |
| Coin-operated apparel laundry and dry cleaning | $48.70 | Other apparel products and services | immigrant-intensive |
| Apparel laundry and dry cleaning, not coin-operated | $37.24 | Other apparel products and services | immigrant-intensive |
| Alteration, repair and tailoring of apparel | $6.29 | Other apparel products and services | immigrant-intensive |
| Shoe repair and other shoe services | $2.00 | Other apparel products and services | immigrant-intensive |
| Care for elderly, invalids, handicapped | $75.71 | Personal services | other non-traded |
| Services for termite/pest control | $68.04 | Other household expenses | other non-traded |
| Moving, storage and freight | $59.85 | Other household expenses | other non-traded |
| Adult day care centers | $0.95 | Personal services | other non-traded |
| Food away from home | $3,944.94 | (own aggregate) | other non-traded |

[SOURCE: `cu-all-detail-2024.xlsx` and `cu-income-quintiles-before-taxes-2024.xlsx`, BLS, published December 2025, fetched 2026-09-18; `derived/expenditure_map.csv`.]

**What does not map.** Household laundry and dry cleaning sent out (non-clothing) is published as "d/ — no data reported" and is dropped [SOURCE: `derived/compute_audit.json`, `dropped_cex_lines`]. Construction and home-repair labor is not separable into a labor component in the CEX and is outside Cortes's price sample, so it is excluded from both scopes; that omission is the single largest downward bias in this estimate, since Mexico-born workers are **11.8% of national construction employment and 26.0% in Texas, 26.9% in California** [SOURCE: `derived/industry_shares.csv`]. Coin-operated laundry is included in the narrow scope although it is capital- rather than labor-intensive, which biases slightly upward. "Personal care services" mixes barber shops and beauty salons, where Mexico-born workers are only **3.0% of national employment**, with nail salons; including it at the full immigrant-intensive elasticity is generous.

**Gate.** The fourteen major Table 1101 components sum to the published "Average annual expenditures" in every column, maximum discrepancy $2 on $150,342, i.e. rounding only [SOURCE: `derived/cex_audit.json`, `major_component_gate`].

**Native consumer units.** CEX reports 135.76m consumer units. ACS 2024 gives a native-householder share of **82.4%–84.5%** across the four CEX income cut-points ($29,932 / $57,452 / $94,511 / $155,925), remarkably flat, so the quintile-specific share is applied to each CEX quintile count [SOURCE: `derived/native_hh_by_quintile.csv`]. Household income is approximated as the sum of ADJINC-adjusted PINCP within a serial number; the housing file was not staged [METHOD, limitation].

**Result and its distribution.** The central arm gives **$23.76bn a year**, $7,506 per Mexico-born low-skilled worker. It is concentrated at the top, as Cortes herself found:

| Income quintile | Immigrant-intensive spend per CU | Loss per native CU | Aggregate loss ($bn) |
|---|---:|---:|---:|
| Lowest 20% | $625 | $89 | 2.03 |
| Second 20% | $797 | $114 | 2.60 |
| Third 20% | $1,133 | $162 | 3.68 |
| Fourth 20% | $1,572 | $225 | 5.17 |
| Highest 20% | $3,202 | $458 | 10.29 |

[SOURCE: `derived/partA_price_results.csv`.] The top quintile absorbs 43% of the total; the bottom quintile 9%.

**Industry exposure, for reference.** Mexico-born share of employment in the mapped industries, national / California / Texas: landscaping 21.2% / 53.1% / 37.2%; services to buildings and dwellings 16.0% / 40.1% / 31.6%; private households 12.6% / 26.9% / 26.9%; drycleaning and laundry 12.9% / 34.7% / 27.5%; child care services 4.3% / 16.4% / 7.4%; barber/beauty/nail 3.0% / 8.0% / 8.0%; food services 6.7% / 17.9% / 12.5%; construction 11.8% / 26.9% / 26.0%. By occupation, maids and housekeeping cleaners 19.3% / 45.3% / 38.4% and grounds maintenance 21.7% / 53.5% / 37.3% [SOURCE: `derived/industry_shares.csv`].

## 3. Part A offset: the same paper's native wage channel

Cortes's structural section reports that a 10 percent increase in the low-skilled immigrant share reduces the wages of **low-skilled natives by 0.6 percent** and of **low-skilled immigrants by 8.0 percent**, with those wage cuts accounting for 50–80 percent of the price fall [SOURCE: Cortes WP abstract and §6]. Removal therefore *raises* native low-skilled wages by the same extrapolation: Δln w = +0.0398, a **4.06% wage rise** for the 8,053,854 employed native high-school dropouts whose aggregate earnings are $264.3bn, worth **$10.73bn a year** [SOURCE: `derived/native_lowskill_wage_offset.csv`, `derived/native_lowskill_base.csv`]. This is a native gain and must be netted against the native consumer loss. Doing so cuts the central consumer-price figure from $23.76bn to **$13.03bn**. Cortes's own bottom line for the 1990s wave was the same sign structure: +0.65% purchasing power for high-skilled natives, **−2.66% for native high-school dropouts**.

## 4. Part B method: native women's hours

**What Furtado and Hock 2010 actually estimates — a verified negative.** The brief asked for its effect of a 10% increase in the low-skilled immigrant share on hours worked and on household-work time. **That estimate does not exist in the paper.** Furtado and Hock (AER Papers & Proceedings 100(2): 224–228) regress the **tetrachoric correlation between childbearing and female labor-force participation** among non-Hispanic native college graduates on the low-skilled immigrant share of the working-age population — a level, not a log. The IV coefficient is **0.845 (SE 0.307)**, and the stated magnitude is that the 1980–2000 flow "implies a 0.2 percentage point increase in the joint likelihood of fertility and work… 8.6 percent of the 2.3 percentage point rise" observed [SOURCE: full text via PMC4160832, https://pmc.ncbi.nlm.nih.gov/articles/PMC4160832/, fetched 2026-09-18, Table 1 and §III]. There is no hours outcome, no household-time outcome, and no per-10-percent conversion. It cannot be priced in the units this memo needs. [VERIFIED NEGATIVE]

**Cortes and Tessada 2011, and what I could and could not retrieve.** The published article is paywalled at AEA and JSTOR; ResearchGate, the Pontificia Universidad Católica repository and openICPSR all failed. The main-text coefficients for the **top quartile of the female wage distribution** are therefore **[UNVERIFIED]** here. What I did obtain is the AEA-hosted **Online Appendix Table 1**, which reports the same IV specification for women in occupations in the **top 25% by male median wage**, with the coefficient on the log low-skilled immigrant share [SOURCE: https://www.aeaweb.org/articles/materials/1197, 4pp, fetched 2026-09-18]:

| Outcome, top-25% occupations, IV | Basic controls | Additional controls (paper's preferred) |
|---|---:|---:|
| Usual hours per week | 1.009 (0.555) | **0.451 (0.563)** |
| Usual hours per week given hours > 0 | 2.075 (0.673) | **0.980 (0.497)** |
| P(hours ≥ 50) | 0.111 (0.033) | 0.069 (0.026) |
| P(hours ≥ 60) | 0.047 (0.015) | 0.023 (0.011) |
| Labor-force participation | −0.058 (0.017) | −0.036 (0.014) |

The unconditional-hours coefficient in the preferred column is **not statistically significant** (t = 0.80). The intensive-margin coefficient is (t = 1.97). I use 0.980 as the central arm, 0.451 as the low arm and 0.490 as the conservative arm.

**Two consistency checks on that reading.** First, the appendix's regressor is printed as "Log (Low-skilled Immigrants + Low-skilled Natives / Labor Force)", which is ambiguous; Cortes's 2023 survey states that Cortes and Tessada "uses the same empirical strategy as in Cortés (2008)", whose regressor is Ln(low-skilled immigrants / labor force) [SOURCE: NBER WP 31234, p.9, https://www.nber.org/system/files/working_papers/w31234/w31234.pdf, fetched 2026-09-18]. Second, arithmetic: the mean 1980–2000 log change in the low-skilled immigrant share across Cortes's 25 cities is **+0.370** [SOURCE: Cortes WP Table 1, transcribed and differenced in `derived/cortes_table1_cities.csv`]. A coefficient of 0.980 implies 0.363 hours a week, or **21.8 minutes**, against the published magnitude of "about 20 minutes a week" for top-quartile-wage women [SOURCE: St. Louis Fed, *Economic Synopses* 2011 no. 31, https://doi.org/10.20955/es.2011.31; World Bank Development Impact blog]. The agreement to within 10% supports both the regressor reading and the magnitude. [INFERENCE, but tightly constrained.]

**The affected population.** ACS 2024: the 75th percentile of the hourly wage among all employed women with positive hours and earnings is **$38.07**. Above it there are **12,141,678 native college-educated employed women**, mean usual hours 38.88 a week over 49.32 weeks, aggregate hourly wage **$67.41**, mean annual earnings $131,237 [SOURCE: `derived/women_top_quartile.csv`]. All native women in the top quartile number 16,635,278 and are reported as a sensitivity.

**Result.** Removal cuts hours by **0.618 a week** (1.6% of mean hours) in the central arm, **$24.94bn of annual earnings**. At a 35% combined marginal rate the tax loss is **$8.73bn**; at CBO's economywide federal rate of 27% it is $6.73bn; including the employer payroll share at 43% it is $10.72bn [SOURCE: `derived/partB_hours_results.csv`].

**The tax rate.** CBO estimates "the economywide marginal tax rate on labor income was 27 percent in 2018, consisting of 18 percent from individual income taxes and 9 percent from payroll taxes", projected to drift to about 31 percent by 2028 [SOURCE: CBO, *Marginal Federal Tax Rates on Labor Income: 1962 to 2028*, January 2019, https://www.cbo.gov/publication/54911 — text retrieved through a search index; cbo.gov returns HTTP 403 to direct fetch, consistent with prior lanes]. The 35% central arm is built up for this specific population rather than taken from CBO: a 22–24% federal statutory marginal bracket at ~$131k, 7.65% employee FICA, and roughly 4–5% state income tax. That build-up is **[INFERENCE]**, not a measured average; the CBO 27% and the 43% employer-inclusive figures bracket it.

## 5. Disconfirmation

**The extrapolation is not merely outside the identifying variation — it breaks the model.** The magnitude |Δln(share)| = 0.63 is not unusual by itself: 9 of Cortes's 25 cities moved at least that far in log terms between 1980 and 2000 (Atlanta +2.14, Dallas +1.40, Denver +1.25; 9 of 25 have |Δln| ≥ 0.63). But only **one** city moved that far *downward* (Cleveland −1.03), and none of the variation is national. The decisive problem is internal: applying Cortes's own low-skilled-immigrant wage elasticity (−8.0% per 10%) to this shock implies the wages of the *remaining* low-skilled immigrants rise **73.6 percent** [SOURCE: `derived/native_lowskill_wage_offset.csv`]. That is not credible, and because she attributes 50–80% of the price effect to exactly that wage channel, the 14.3% price rise inherits the same implausibility. The honest reading is that these figures are an **upper bound on the linear-approximation region**, and the conservative arm is closer to what the evidence can carry. [INFERENCE]

**Two recent US studies do not reproduce the services-price channel.** Barrett and Tan (IMF Working Paper 2025/005) use a shift-share design on US local inflation and find that immigration "lower[s] local goods inflation, increase[s] local housing and utilities inflation, and ha[s] **no statistically significant impact on inflation in other services**", with effects two to three times larger for working-age and low-education immigrants [SOURCE: https://ideas.repec.org/p/imf/imfwpa/2025-005.html, fetched 2026-09-18]. If services prices do not move, Part A is zero. Separately, a 2026 firm-level study using barcode data finds immigration reduces consumer-packaged-goods prices but attributes it to **consumer search**, stating "we find no evidence of negative wage effects" [SOURCE: *Prices and Immigration: Firm-Level Evidence*, https://ryansungryongkim.github.io/papers/KLW_25Feb2026.pdf, fetched 2026-09-18]. Cheremukhin et al. (2024), cited in that paper, argue on theory that the disinflationary labor-supply effect and the inflationary product-demand effect "may largely cancel each other out". Furlanetto and Robstad (2019) find small medium-run *positive* effects on general price levels.

**The international contrast runs on a different mechanism.** Lach (2007, JPE 115(4)) exploits the 1990 Former Soviet Union wave in Israel and finds that "a one-percentage-point increase in the ratio of immigrants to natives in a city decreases prices by 0.5 percentage point on average", explicitly attributing it to **immigrants as new consumers with higher price elasticities and lower search costs**, not to labor supply [SOURCE: https://www.journals.uchicago.edu/doi/10.1086/521529, fetched 2026-09-18]. His own working paper reported **1.4–1.8 percent** per percentage point — the same published-versus-working-paper shrinkage seen in Cortes [SOURCE: SSRN 776685 abstract]. Under Lach's mechanism, removing immigrants removes *consumers*, and the price response has a different sign structure entirely. Frattini (2008, UCL mimeo, never published in a journal) finds for the UK 1995–2006 that immigration reduced price growth of low-wage services such as restaurants and takeaways but **raised** the price of low-value grocery goods via demand, and calls the effects "significant but quantitatively limited" [SOURCE: http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.192.7226; corroborated in CEPR VoxEU, https://cepr.org/voxeu/columns/economic-impacts-immigration-uk].

**Does a 2008 elasticity transfer to 2024?** Weakly. The price data end in 2002 and the identifying decade is the 1990s. Since then: the low-skilled immigrant share of the national labor force is 3.78%, against double-digit shares in Los Angeles and Miami in her sample; laundry and food preparation have automated substantially; app-mediated platforms have changed the search and pricing technology in exactly the housekeeping, lawn-care and childcare markets at issue; and the Mexico-born low-skilled population is older and more settled than the 1990s inflow. All of these point toward a smaller present-day elasticity, none toward a larger one. [INFERENCE]

**What would make each number wrong.**
- *Part A too high* if Barrett–Tan is right that services prices do not respond; if the true elasticity is the working paper's 1.3% rather than the published 2%; if substitution toward home production or automation absorbs the shock (this calculation assumes zero quantity response); if "personal care services" and coin-operated laundry do not belong in the immigrant-intensive set.
- *Part A too low* because construction and repair labor is excluded entirely, and Mexico-born workers are 11.8% of national construction employment; because the CEX under-reports expenditure relative to the national accounts; and because within-parent composition may be more service-heavy at the top than the national average I imposed.
- *Part B too high* because the coefficient used is for top-25% *occupations*, not top-quartile *wages*; because the unconditional-hours coefficient in the preferred specification is insignificant; because the marginal hours are valued at the average wage; and because labor-force participation actually *falls* with immigration in the same table (−0.036), which this calculation ignores.
- *Part B too low* because it covers only college-educated native women in the top wage quartile; the all-native-top-quartile population gives $32.5bn of earnings and $11.4bn of tax.

**General-equilibrium omissions.** No capital adjustment; no pass-through of higher service prices into other sectors' costs; no housing or rent channel (covered separately by the housing lane, where removal is emphatically *not* arrival with a minus sign); no effect on the immigrants' own consumption demand, which is the entire Lach mechanism; no fiscal feedback from a higher CPI into indexed federal outlays such as the Social Security COLA and SNAP thresholds, which would push in the opposite direction to the B-tax gain; no native internal migration response; and no accounting for the low-skilled immigrants' own wage gain, which is not a native item but is most of the mechanism.

**Instrument bias.** This is a politically charged topic analyzed through an LLM with known post-training dispositions [SOURCE: `notes/llm-bias-caveat.md`]. The disposition here would push toward inflating the pro-immigration benefit; the net-of-offset framing in §3 and the conservative arm are the guards. The fiscal comparison is [FRAMING-SENSITIVE] in the same way the underlying ledger is: reference gaps are differences from a chosen comparison profile, not measured net costs.

## 6. What this settles

The pro-side's two flagship native benefits, priced at their own authors' published elasticities and extrapolated as far as the extrapolation can be pushed, come to roughly **$22bn a year**, of which **$9bn** is fiscal. Against a reference gap of $291bn to $354bn, the fiscal offset is **1.4% to 3.0%**. The consumer-price channel is further halved once the same paper's wage gain to native high-school dropouts is netted out, and it may be zero if the two most recent US studies are right. No arm of this calculation, including arms deliberately built to be generous, brings the two channels within an order of magnitude of the fiscal figures. That conclusion is robust because it does not depend on which elasticity is correct: even multiplying the central arm by three leaves the fiscal offset under 10%.

## Sources

| Source | URL | Fetched |
|---|---|---|
| Cortés 2008, JPE 116(3):381–422 (published abstract, 2% figure) | https://www.journals.uchicago.edu/doi/10.1086/589756 | 2026-09-18 |
| Cortés, working-paper version (1.3%, 0.2%, wage elasticities, Tables 1–3, 10) | https://www.economics.uci.edu/files/docs/colloqpapers/w06/Cortes.pdf | 2026-09-18 |
| Cortés, MIT PhD thesis version | http://hdl.handle.net/1721.1/37414 | 2026-09-18 |
| Cortés & Tessada 2011, AEJ: Applied 3(3):88–123 — Online Appendix Table 1 | https://www.aeaweb.org/articles/materials/1197 | 2026-09-18 |
| Cortés 2023 survey, NBER WP 31234 | https://www.nber.org/system/files/working_papers/w31234/w31234.pdf | 2026-09-18 |
| Furtado & Hock 2010, AER P&P 100(2):224–228, full text | https://pmc.ncbi.nlm.nih.gov/articles/PMC4160832/ | 2026-09-18 |
| Lach 2007, JPE 115(4) (Israel, 0.5pp, demand mechanism) | https://www.journals.uchicago.edu/doi/10.1086/521529 | 2026-09-18 |
| Lach working paper (1.4–1.8%) | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=776685 | 2026-09-18 |
| Frattini 2008, UCL mimeo (UK) | http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.192.7226 | 2026-09-18 |
| Barrett & Tan, IMF WP 2025/005, *Immigration and Local Inflation* | https://ideas.repec.org/p/imf/imfwpa/2025-005.html | 2026-09-18 |
| *Prices and Immigration: Firm-Level Evidence* (2026) | https://ryansungryongkim.github.io/papers/KLW_25Feb2026.pdf | 2026-09-18 |
| St. Louis Fed, *Economic Synopses* 2011 no. 31 (20 min/week) | https://doi.org/10.20955/es.2011.31 | 2026-09-18 |
| Holzer, *Immigration Policy and Less-Skilled Workers* (construction omission) | https://www.urban.org/sites/default/files/publication/26861/1001488-Immigration-Policy-and-Less-Skilled-Workers-in-the-United-States.PDF | 2026-09-18 |
| CBO, *Marginal Federal Tax Rates on Labor Income: 1962 to 2028* | https://www.cbo.gov/publication/54911 | 2026-09-18 (via search index; direct fetch 403) |
| BLS CEX 2024 Table 2500, all CU detail | https://www.bls.gov/cex/tables/calendar-year/mean/cu-all-detail-2024.xlsx | 2026-09-18 |
| BLS CEX 2024 Table 1101, income quintiles | https://www.bls.gov/cex/tables/calendar-year/mean-item-share-average-standard-error/cu-income-quintiles-before-taxes-2024.xlsx | 2026-09-18 |
| ACS 2024 1-year PUMS person file | https://www2.census.gov/programs-surveys/acs/data/pums/2024/1-Year/csv_pus.zip | staged 2026-09-17 |
| Repo fiscal denominators (ladder 123, 130) | [`immigration-confidence-ladder.md`](immigration-confidence-ladder.md), [`all-age findings`](immigration-all-age-and-lineage-findings-2026-09-17.md) | — |

Data-file SHA-256 hashes are recorded in `derived/cex_audit.json` and `derived/acs_audit.json`.


## Revisions — September 19, 2026

Corrected the interpretation at the point of reuse; original calculations and evidence are retained. See the [decision](../decisions/2026-09-19-bind-report-claims-to-matched-estimands.md) and linked audit for the claim-specific reason.

- 2026-09-23: The Part B hours tax is corrected from $8.7bn to $2.6bn on this memo's population. In the union frame at the account's tax rate it is $2.7bn a year ($1.8–5.8bn). Three things were wrong:
  - the regressor: Cortés–Tessada's ℒ counts no-diploma natives as well as immigrants;
  - the coefficient: 0.980 is Table 8's occupation split, and the household-service channel is Table 10's 0.479, SE 0.106;
  - the tax rate: 0.35 was used instead of the account's 0.426.

  Only the household-service part of the hours response adds to the account. The rest is a wage response, which the account's labour-supply arm already covers. Part A (cheaper services, $21.8bn gross, $11.9bn net of native low-skill wage gains) stands. It sits inside the production gain, so it is not added. Lane `care_household_services_2026_09_23`, ladder 198. Concept affected: induced native hours as a fiscal gain.
