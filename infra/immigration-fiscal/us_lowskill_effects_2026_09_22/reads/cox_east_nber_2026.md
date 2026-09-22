<!-- reader extraction, opus-low agent, 2026-09-22; every numeric row carries a verbatim quote re-found in the parsed corpus text with rg -F; parent spot-checked the rows cited in the memo -->
# Cox & East (2026), "Labor Market Impacts of ICE Activity in Trump 2.0", NBER WP 35129 (April 2026, revised June 2026)

[SOURCE: /Users/alien/Projects/corpus/doi_10_3386_w35129/parsed.pymupdf4llm@0.3.4+cfg-99914b93/page.md]
[UNVERIFIED] — NBER working paper, explicitly not peer-reviewed. The main employment coefficients live in figures (images in the parsed text), so their standard errors are not recoverable here; only Tables A1–A2 print SEs.

**Verdict:** A staggered event-study / difference-in-differences comparison of US areas with sudden 2025 ICE arrest surges against areas without one, finding that employment of likely-undocumented immigrants who remain falls, US-born male employment also falls, and no group's wages rise; the design is credible (flat pre-trends, first-Trump-term placebo, Callaway–Sant'Anna and tariff-control robustness) but it is a short-horizon, within-country relative comparison that cannot recover national effects and deliberately does not measure population outflows.

## Population, period, unit

- **Unit of analysis:** 58 geographic areas — "58 areas in the final analysis; 48 states, 3 sub-state areas in California, 5 sub-state areas in Texas, and 2 sub-state areas in New York" — observed as demographic-group × area × month cells.
- **ICE arrests source:** the **Deportation Data Project**, ICE Enforcement and Removal Operations administrative arrests, **October 2023 through October 2025**. Excludes CBP and USCIS arrests, ERO criminal arrests (~4% of ERO arrests) and Homeland Security Investigations arrests (~4% of ICE arrests).
- **Labor data source:** the **basic monthly Current Population Survey** (IPUMS CPS 13.0, Flood et al. 2025), **October 2023 – November 2025**. The introduction says "January 2024 to November 2025"; the Data section and every figure note say October 2023 – November 2025, so take the figure notes as authoritative. Later CPS months are dropped because treatment measurement ends mid-October 2025.
- **Likely-undocumented sample:** foreign-born (excluding US territories), ages 20–64, high-school degree or less, not currently or recently employed by government. Robust to further restricting to non-citizens or to Hispanics.
- **US-born sample:** US-born, ages 20–64, excluding those born in US territories. All samples are restricted to people working, searching for work, or who worked within the last five years, so sector is observed; public-sector and military workers are excluded.
- **Baseline denominators:** 2023 ACS 5-year non-citizen counts; Passel–Cohn (2016) PEW undocumented sector shares.
- **Outcomes:** employed **and at work** in the previous week ("the employment rate"), average weekly earnings, hourly wage among the hourly-paid, and a "has a job but not at work last week" absence margin.

## Design and identification

Treatment is a **sudden, large jump in ICE arrests** between January and October 2025: treatment begins the month an area experiences "a 1-month change of roughly 50 arrests per 100,000 non-citizens, or an approximate doubling of arrests per 100,000 non-citizens." Control areas saw no comparable jump. Exposure is therefore a **binary event-time indicator**, not a continuous share and not a shift-share or enclave instrument.

Event study: outcome regressed on event-time dummies from τ = −14 to +6, binned into two-month groups, plus area fixed effects, calendar-month fixed effects and year fixed effects; standard errors clustered by geographic area. Data are collapsed to area-month cells using CPS final weights and the collapsed regressions are run **unweighted**, so coefficients are effects on the **average area**, not population-weighted national effects. A difference-in-differences version replaces the event-time dummies with an area-varying post indicator.

"First stage" on arrests (Figure 2) is mechanical by construction but fixes the dose: roughly **+200 daily arrests per month** in treated relative to control areas, a **114%** increase over the pre-period mean, or **+94 arrests per 100,000 non-citizens**, with **85%** of the arrest effect coming from male arrests.

Validity work: no differential pre-trends in any event study; a placebo that assigns the same areas to treatment in 2015–2017 around the first Trump inauguration produces coefficients "close to zero and insignificant"; robustness to Kolko's alternative CPS weights, baseline demographics × time, baseline economic conditions × time, the Callaway–Sant'Anna (2021) estimator, and a state tariff-exposure control.

## Headline estimates

Units: the DiD employment coefficients appear in the running text as percentage points with the percent change in parentheses. Figure-based rows carry no printed SE in the parsed text; Table A1–A2 rows do.

| Outcome | Estimate | SE or CI | Table/figure and page | Verbatim quote (≤40 words) |
|---|---|---|---|---|
| ICE arrests, treated vs control (levels) | ≈ +200 daily arrests per month | not printed | Figure 2, §4, p. 7 | "of roughly 200 daily arrests per month in the treated areas relative to control areas" |
| ICE arrests vs pre-period mean | +114% | not printed | Figure 2, §4, p. 7 | "this is a 114% increase in arrests" |
| ICE arrests per 100k non-citizens | +94 per 100,000 | significant; SE not printed | Figure 2, §4, p. 7 | "significant increase of 94 arrests per 100,000 non-citizens in treated compared to control areas" |
| Male share of the arrest effect | 85% | female effect also significant | §4, p. 7 | "85% of the effect on total ICE arrests is driven by arrests of males" |
| Likely-undocumented employment rate, all sectors | −1.3 pp (−1.4%) | significant; SE in Figure 3 (image) | Figure 3 DD, §4, p. 8 | "employment rate of likely undocumented immigrants of 1.3 overall (1.4%) and 1.8 percentage points (2%) in the high-impact sectors" |
| Likely-undocumented employment rate, high-impact sectors | −1.8 pp (−2%) | significant; SE in Figure 3 (image) | Figure 3 DD, §4, p. 8 | "1.3 overall (1.4%) and 1.8 percentage points (2%) in the high-impact sectors" |
| Likely-undocumented **male** employment rate, all / high-impact | −2.8 pp / −3.5 pp | significant; SE in Figure 3 (image) | Figure 3 DD, §4, p. 8 | "the male employment rate of 2.8 and 3.5 percentage points, across all and high-impact sectors, respectively" |
| Likely-undocumented **female** employment rate | positive, insignificant | insignificant | Figure 3, §4, p. 8 | "The estimates for the female employment rate are positive but insignificant" |
| US-born employment rate, all workers | null; gains bounded | 95% CI rules out gains above **+0.3 pp** | Figure 5, §4, p. 10 | "employment of larger than 0.3 percentage points. And, if anything we find negative effects" |
| US-born employment rate, likely-impacted sectors | null; gains bounded | 95% CI rules out gains above **+0.3 pp** | §1, p. 2 | "we rule out increases in likely impacted sectors of more than 0.3 percentage points" |
| US-born **male** employment rate | −0.006 (0.6 pp), negative and significant | significant; SE in Figure 5 (image) | Figure 5 / Magnitudes, pp. 10–12 | "of 11,300 per area ((-0.006/0.928)*1,752,839)" |
| Likely-undocumented weekly earnings / hourly wage, both sexes | +17.414 / +0.521 (means 700.272 / 16.189) | SE 33.145 / 0.367; insignificant | Table A1a, p. 28 | "Post 17.414 0.521 -22.652* 0.059" |
| US-born weekly earnings / hourly wage, both sexes | −22.652 / +0.059 (means 1175.690 / 19.708) | SE 13.290 (p<0.10) / 0.195 | Table A1a, p. 28 | "Mean Y 700.272 16.189 1175.690 19.708" |
| Likely-undocumented **male** weekly earnings / hourly wage | −3.896 / +0.748 (means 793.719 / 17.456) | SE 49.050 / 0.541; insignificant | Table A1b, p. 28 | "Post -3.896 0.748 -24.096 0.140" |
| US-born **male** weekly earnings / hourly wage | −24.096 / +0.140 (means 1341.060 / 20.671) | SE 19.928 / 0.272; insignificant | Table A1b, p. 28 | "Mean Y 793.719 17.456 1341.060 20.671" |
| US-born **males** employed but not at work last week | +0.003 (0.3 pp) on a 0.028 mean | SE 0.001, p<0.05 | Table A2b, p. 29 | "Post 0.003**" |
| US-born, both sexes, employed but not at work | 0.000 on a 0.034 mean | SE 0.001; null | Table A2a, p. 29 | "Mean Y 0.034" |
| Implied male likely-undocumented job loss, average treated area | ≈ 8,300 fewer at work | back-of-envelope, no SE | Magnitudes, p. 11 | "This implies roughly 8,300 fewer likely undocumented males at work in all sectors in the average treated area" |
| Implied male US-born job loss, average treated area | ≈ 11,300 fewer at work | back-of-envelope, no SE | Magnitudes, p. 12 | "of 11,300 per area ((-0.006/0.928)*1,752,839)" |
| Chilling ratio per ICE arrest | 7 male likely-undocumented workers stop working (vs 2.3 under Obama I) | n/a | Magnitudes, p. 12 | "for every ICE arrest, 7 male likely undocumented workers who remain in the U.S. stop working" |
| Implied total immigrant worker loss incl. departures | ≈ 13,000 per treated area | uses Kissam (2026) departure estimate | Magnitudes, pp. 11–12 | "closer to 13,000 lost immigrant workers in the average treated area" |
| Cross-sector pattern, male likely-undocumented | largest negative effect in Construction (13% undocumented) | mostly insignificant by sector | Figure 4a, p. 9 | "significant given small sample sizes, so we focus on overall patterns in this analysis" |

**Whose employment falls, precisely.** The US-born male employment result is for **all US-born men aged 20–64 in the area** with labor-force attachment (working, searching, or worked in the last five years), excluding public-sector and military workers. It is not restricted to low-skill men or to men competing with immigrants; the sector breakdown is a heterogeneity cut layered on that full sample. The 11,300 figure is scaled off a baseline of 1,752,839 US-born men at work in the average treated area. Likewise, the likely-undocumented male result covers all foreign-born men 20–64 with at most a high-school degree.

**Do natives fill the vacated jobs?** The authors say no, in three places. Result: "We find null effects on all U.S.-born workers' employment rate and negative effects for males' employment rate." Wages: "There is no evidence that employers increase wages to attract U.S.-born workers." Conclusion: "We find no evidence supporting this argument, and, instead document negative spillovers for U.S.-born males, suggesting that enforcement may contract, rather than reallocate, labor demand in affected areas." They add that the contrary DHS/FAIR claim of US-born workers absorbing the losses "relies on the population estimates from the CPS, which are known to have measurement issues."

## What it says about

- **Native wages by skill/education:** no education split is estimated anywhere. Wages are cut only by sex and nativity. US-born hourly wages are null (+0.059, SE 0.195); US-born weekly earnings are weakly negative (−22.652, p<0.10 for both sexes) and insignificant for men alone. Undocumented pay shows "no evidence of a significant negative or positive effect."
- **Native employment / crowd-out:** the central result. Overall US-born employment is a null with gains above +0.3 pp ruled out at 95%; US-born male employment falls significantly (≈0.6 pp implied). Across sectors, the correlation between a sector's baseline undocumented share and the US-born male employment effect is **negative**, with Agriculture the exception — the opposite sign to a crowd-out story.
- **Housing prices, rents:** not studied.
- **Fiscal: taxes, transfers, public services, schooling:** not studied. No fiscal accounting of any kind. Education enters only as a sample criterion and control; schooling outcomes appear only as a cited outside result (Figlio and Özek 2025).
- **Firms, production, investment, profits:** not measured directly. Approached only through the "employed but not at work" margin, which the authors cannot decompose: "we are unable to distinguish if the workers are choosing to stay home or whether production at their workplaces changed as a result of ICE activity."
- **Mechanism the authors claim:** three channels jointly. (1) A **chilling effect** on immigrants who remain, supported by a KFF/New York Times survey in which "40% of likely undocumented immigrants reported avoiding going to work for fear of it drawing attention to their immigration status." (2) **Production complementarity** between undocumented and US-born workers (Chassamboulli and Peri 2015), evidenced by the negative cross-sector gradient for US-born males and by the observation that undocumented workers hold less desirable jobs within the same sector. (3) **Local demand contraction**, evidenced by the largest US-born male losses landing in sectors that are both non-tradable and undocumented-intensive (Leisure/Hospitality, Other Services), following the Burstein et al. (2020) tradability split.

## Elasticities or parameters a model could transport

The paper reports **no structural elasticities**: no CES nest, no elasticity of substitution between natives and immigrants, no labor-demand elasticity. What transports is a set of reduced-form quantities estimated on the 2025 CPS at area level.

1. **Chilling response of employment to an arrest surge.** An approximate doubling of arrests (+94 per 100,000 non-citizens, +114%) lowers the likely-undocumented employment rate by 1.3 pp (−1.4%) overall, 1.8 pp in undocumented-intensive sectors, and 2.8 pp among men. Population: foreign-born, ages 20–64, at most a high-school degree, in 58 US areas, 2025.
2. **Displaced-worker multiplier per arrest:** 7 male likely-undocumented workers stop working per ICE arrest, versus 2.3 per detention under Obama's first term (East et al. 2023). This is a policy-regime parameter reflecting how indiscriminate enforcement is, not a labor-market primitive.
3. **Immigrant-to-US-born employment-loss ratio:** 8,300 immigrant men versus 11,300 US-born men out of work per average treated area, i.e. roughly **1.4 US-born men displaced per immigrant man displaced**. The authors instead benchmark against a literature range of "0.61 to 4.3" (Zipperer 2025). Any production-term model has to reproduce this sign; a pure substitution nest cannot.
4. **Upper bound on native employment gains:** +0.3 pp at 95%, both overall and in the most exposed sectors. Usable as a falsification band for any model predicting native job gains from enforcement.

Transport caution for a fiscal or native-surplus application: these are **area-relative** effects over a horizon of at most nine post-treatment months, estimated unweighted so they describe the average area rather than the nation, with immigrant population outflow deliberately excluded from the outcome. They bound the short-run sign of the native-surplus channel; they do not identify a long-run elasticity of substitution, and the authors explicitly warn that inflow and enforcement-driven outflow effects "are unlikely to be symmetric."

## Authors' stated limitations and external-validity notes

- **National effects are not identified:** "we will miss any national effects, and we do not extrapolate our findings to national totals."
- **Control-area contamination attenuates:** immigrants in control areas may respond to media and social networks; "If anything, this would attenuate our estimates towards zero."
- **Only the chilling channel is measured, not removals.** The outcomes "will only capture part of the total effect on immigrant labor supply, since we miss the direct effects of removals." Population counts are avoided because of CPS non-response and immigrant population-estimate problems (Kolko 2025b; Bick and Bloodworth II 2025; Edelberg and Watson 2024).
- **Survey non-response biases toward zero:** the most-affected people are the most likely to stop responding, so "our estimates will, if anything, be an underestimate of the overall economic impacts."
- **Removal composition could bias upward** if those removed had higher labor supply; the authors argue this is unlikely given Trump 2.0 arrest patterns (mostly people already in law-enforcement custody or encountered somewhat randomly).
- **Documentation status is a proxy**, never observed; the CPS has no such variable.
- **Sample is labor-force-attached**, skewed toward those with work history, which the authors defend as the policy-relevant sample.
- **Sector-level estimates are imprecise:** "significant given small sample sizes, so we focus on overall patterns in this analysis."
- **Chilling effects are larger than in the Obama era**, which the authors attribute to more indiscriminate enforcement — so the magnitudes are regime-specific and should not be transported to a different enforcement style.
- **Not peer-reviewed:** NBER working papers "have not been peer-reviewed or been subject to the review by the NBER Board of Directors."

## Data availability

No replication package is mentioned anywhere in the paper. All inputs are public or licensed-public: Deportation Data Project ICE data (deportationdata.org), IPUMS CPS 13.0, ACS 2023 5-year estimates, ICE ERO Area-of-Responsibility boundaries, Passel–Cohn (2016) PEW sector shares, and Jed Kolko's alternative CPS weights. Funding from the Russell Sage Foundation. No restricted-access data is used.

## Verification

**22 of 22 numeric rows verified.** Every row's quote fragment was re-found with `rg -F` against the paper path; fragments were shortened where the parsed Markdown breaks a sentence across lines. No row was dropped. Figure-based coefficients (Figures 2, 3, 5) have no printed standard errors in the parsed text because the figures are images; the point estimates quoted for them come from the running text, not from reading the figures.
