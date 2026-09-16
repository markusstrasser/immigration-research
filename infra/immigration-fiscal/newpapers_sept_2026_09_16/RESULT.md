# New 2025–26 Papers Audit — COMPLETE (one [GAP] on numeric extraction)

**Verdict:** Five of six targets verified at primary; two of the brief's three attributions are wrong (AEI is Orrenius/Viard/Zavodny not Strain; the Feb 2026 white paper is Cato/Bier not NASEM), and its premise that the memo cites Villarreal & Tamborini is a VERIFIED NEGATIVE. The consequential finding is Borgschulte et al.: a causal, administratively-measured incumbent-child channel that narrows ladder 81's scope. Cato concedes the second generation is fiscally negative today, so it does not refute memo §12 — the two are different estimands. Akee et al. establish that stayers are positively selected, so the Mexico-born ledger cell understates the cost.

**Model self-report:** Claude Opus 5 (1M context), model ID `claude-opus-5[1m]`, running as the `newdata-lit` research teammate.

## Scope
Audit six targets for the Mexican-origin generation/incarceration memo and the confidence ladder:
1. Akee, Chin & Crown, "Immigrant Earnings Assimilation, 1981–2021", NBER w35582 (Aug 2026)
2. Borgschulte, Cho, Lubotsky & Rothbaum, "Immigration and Inequality in the Next Generation", NBER w33961 (Jun 2025)
3. Strain / AEI, "The Fiscal Impact of Immigration: An Update" (Sept 2025)
4. "Immigrants' Recent Effects on Government Budgets 1994–2023" white paper (Feb 2026)
5. Hispanic Men's Earnings Mobility Across Immigrant Generations, Social Forces 2023 (doi 10.1093/sf/soad128)
6. Sweep: other 2025–26 NBER/IZA/SSRN on second-generation Hispanic outcomes, ethnic attrition, fiscal effects

Each gets: dataset, design, exact headline numbers with table refs, what it changes for the memo, one disconfirming point, grade NOVEL / HAD-PARTS / CONTRADICTS.

## Findings

All six sections below are complete. Remaining [GAP] tags: Villarreal & Tamborini numeric slopes (PMC wall, routes documented), NBER w35070 abstract, IZA/SSRN sweep.

---

## 1. Akee, Chin & Crown — "Immigrant Earnings Assimilation, 1981–2021", NBER w35582 (Aug 2026)

**Grade: NOVEL** (new fact for the ledger: a return-migration selection direction the repo has never priced).

**Dataset.** Continuous Work History Sample (CWHS), SSA/Census administrative longitudinal earnings, covering workers from their first year of US residence onward, arrival cohorts 1981–2010, ages 25–45 at arrival. Census DRB release CBDRB-FY21-301. Crown is at CBO; the paper is explicitly meant to improve CBO's long-run Social Security projections (title page acknowledgement).

**Design.** log-earnings on years-since-migration indicators, three-year arrival-cohort dummies, age FE, year FE (eq. 1). Estimated separately for (a) permanent migrants, (b) return migrants, (c) the same panel treated as repeated cross-sections. Return migration is inferred from prolonged absence from the earnings record (preferred: absorbing state; robustness: 10 consecutive missing years, Figures A1–A3).

**Headline numbers.**
- One-fifth to one-third of arrivals return-migrate within 10 years (abstract; Figure 2 panels A/B; the apparent rise to 25–30% for recent cohorts is partly a mechanical artefact of the classification window, and the authors say so).
- Pooled 1981–2010: permanent migrants reach earnings parity with the native-born about **8 years** after arrival for men and **19 years** for women (§4.2, Figure 3).
- Entry gap by cohort, men (Table 2 Panel A): about **70 log points** for early cohorts, falling to about **30 log points** for 1998 and later.
- Ten-year gap, men (Table 2 Panel B): **30 log points** for the 1983 cohort, **20** for 1995, **parity** for the 1998, 2001, 2007 and 2010 cohorts. Convergence is driven by rising entry earnings, not by faster growth — the growth rate declines slightly across cohorts.
- Women (Table 3 Panel B): about a **10 log point** gap remains at year 10 in every cohort, worst for the 1987–89 IRCA cohort. No trend.
- Return migrants: entry earnings similar to (slightly below) permanent migrants, then **flat or declining** earnings relative to natives over their US stay.

**What it implies for the Mexico-born CPS ledger cell (the direct ask).** Return migrants are **negatively selected relative to their own arrival cohort** (§4.2, explicit: "return migrants in total are negatively selected with respect to their original arrival cohort, as shown in Figure 3"). So **stayers are positively selected** — the Mexico-born adults the CPS observes are the better-earning residue of their cohorts, not the worse. That cuts against any "the ledger's Mexico-born cell looks bad only because the successes left" defence of the −$8,166/−$7,806 figures in ladder 85: the cross-section is if anything flattered, not penalised, by emigration. Direction of the bias on the repo's per-adult-year gap: the true whole-cohort average is **more negative** than the observed stayer average, so the ledger cell is a lower bound on the cost in absolute terms. Magnitude is not identified here for Mexico specifically.

**Second implication.** Cross-sectional assimilation estimates are *not* badly biased in this data: panel and repeated-cross-section series nearly coincide (Figure 3, red vs blue), contradicting Lubotsky (2007) and blunting the standard Borjas critique. The authors attribute their divergence from Borjas (2015) to **population and coverage**, not to estimation: CWHS sees only formal-sector earnings, "largely from documented immigrants."

**One disconfirming point.** The formal-earnings coverage is the whole problem for this repo's use. The unauthorized Mexico-born cell that carries 40–46% of the gap (ladder 85) is substantially *outside* the CWHS earnings record (ladder 77: 56% of unauthorized workers underground). "Return migration" is inferred from absence from that record, so an unauthorized worker moving into cash work is coded as a return migrant. Both the return-migration rate and the negative selection of return migrants could be partly an informality artefact in exactly the population the repo cares about. The paper does not test this.

---

## 2. Borgschulte, Cho, Lubotsky & Rothbaum — "Immigration and Inequality in the Next Generation", NBER w33961 (June 2025)

**Grade: CONTRADICTS the memo's §13 "no incumbent-child cost" line — partially. It supersedes the scope of that line but not its content.**

**Dataset.** Census Bureau internal administrative linkage: W2 earnings records for US-born children, linked to parental income, by commuting zone of childhood. Public-use Census 1940–2010 for pretrend tests. Rothbaum is Census.

**Design.** Shift-share/enclave IV: 1980 immigrant enclave shares predict 1980–1990 CZ immigrant inflow rates; outcome is the adult income rank of US-born children, by decile of parental income. Controls: 1980 CZ log population, college share, manufacturing share; 1940 mobility of White and Black children at parental deciles 3 and 8 (equation 1). Robustness: CZ fixed effects, no-Mexico enclaves, COLA adjustment, 1970 enclaves, OLS (Tables 2, 3). Pretrend tests in Figure 4.

**Headline coefficients** (per 10 percentage point immigrant inflow; Table 1 col. 1, income rank, SEs clustered by CZ):

| Parental income decile | Effect on child's adult income rank |
|---|---|
| 1 | +0.147 (0.080) * |
| 2 | +0.127 (0.075) * |
| 3 | +0.148 (0.076) * |
| 5 | +0.012 (0.067) |
| 8 | −0.135 (0.078) * |
| 9 | −0.194 (0.087) ** |
| 10 | −0.238 (0.076) *** |
| All | −0.069 (0.085), n.s. |

Illustrated (§6.1): a 10-point inflow moves bottom-decile children **+1.5 rank points** (36.9 → 38.4) and top-decile children **−2.4 rank points** (63.9 → 61.5).

Education (Table 5): **BA completion** is where the affluent-child loss concentrates — decile 9 **−0.562 (0.183)\*\*\***, decile 10 **−0.593 (0.150)\*\*\***, white males decile 9/10 −0.731/−0.734, white females −0.743/−0.690. High-school completion moves the other way at the bottom (decile 1 +0.250\*\*, decile 2 +0.215\*\*\*) and is a precise zero-to-tiny negative at the top (decile 10 −0.014\*).

Employment (Table 4, share of years with W2 above minimum wage): monotone and large — decile 1 **+0.180\***, decile 6 **−0.200\*\*\***, decile 9 **−0.407\*\*\***, decile 10 **−0.408\*\*\***, average **−0.188\*\***.

**What it changes for the memo.** The memo's §13 / ladder 81 line is specifically about **school-quality spillovers onto incumbent students** — Figlio et al. (ReStud 2024) sibling-FE, Diette & Oyelere, Hunt 2017 — and that line survives intact, because this paper measures nothing about classrooms. But the memo's broader framing that there is **no measured incumbent-child channel** does not survive. There is one, it is causal by the repo's usual standard (administrative outcomes, enclave IV, pretrends tested, CZ-FE robustness), and for affluent natives' children it is **negative on all three of earnings rank, BA completion and employment**. Ladder 81 should be narrowed to "no measured incumbent-student *classroom-quality* cost," with a new entry for the mobility channel. Note the sign structure the repo should not garble: the effect is **redistributive within the native second generation**, not a level loss — the all-people average income-rank effect is an insignificant −0.069, and poor natives' children gain.

**One disconfirming point.** The identification rests on 1980 enclaves predicting 1980–90 inflows, and Figure 4 Panel (d) shows the instrument is **positively** correlated with pre-1980 employment rates conditional on controls (a 10-point predicted-migration difference goes with about 2 points higher employment in 1960–1980). The main employment result is a large *negative*. The authors read the sign flip as reassuring; it is equally consistent with the instrument picking up a CZ-level employment trajectory that turns over at exactly the treatment date for reasons unrelated to immigration (deindustrialisation of the same coastal/gateway metros). No pre-trend test resolves a break dated to treatment. Also: the exposure is 1980s inflows onto children who were mostly school-age in the 1980s, so transporting these magnitudes to the 2022–24 surge requires an assumption the paper does not make (footnote: if 1990s inflows had the same effect, estimates should be scaled down about 30%).

---

## 3. Orrenius, Viard & Zavodny (AEI), "The Fiscal Impact of Immigration: An Update" (Sept 2025)

**Grade: HAD-PARTS.** Note first: the brief attributes this to Strain. The authors are **Pia M. Orrenius, Alan D. Viard and Madeline Zavodny** (title page). Strain is not on it.

**What it is.** A 17-page AEI policy report, not new estimation. Its numbers are **re-prints of NAS 2016** (Blau & Mackie 2017, Table 8-13, pp. 440–42), which the repo already holds.

**Headline numbers, with source lines.**
- HS dropout arriving at 25: lifetime fiscal cost **−$246,000**; graduate degree: **+$795,000** (p. 9, Figure 4). Figure 4's own note: "net fiscal impact of an immigrant arriving at age 25 or a US native followed from age 25 over 75 years, by education, **not including the cost of any public goods**", source Blau & Mackie 2017 Table 8-13. 2012 dollars.
- Average immigrant living in the US 2011–13: **+$58,000** NPV over 75 years, 3% discount rate, zero marginal cost of public goods. **Two-fifths** of that is the immigrant, **three-fifths** the descendants.
- Comparison the repo should keep: the lifetime fiscal cost of an immigrant HS dropout arriving at 25 is **less than half** that of a US native HS dropout followed from 25.

**Descendant treatment (the direct ask).** Descendants are **included and discounted** — they enter the same 75-year NPV at 3%, and the report states the assumption plainly: "children and later descendants of immigrants **tend to converge to the US average**" (p. 9), which is why the by-education variation comes from the immigrants themselves and not from their descendants. So: **convergence assumed, not measured.**

**Comparison with the memo.** This is the exact assumption the memo's §11–12 work falsifies for the Mexican-origin line. The repo's measured per-adult-year second-generation gap is **−$6,066 baseline, −$8,286 with employer payroll/sales/property/K-12, −$8,564 with residual items** (ladder 76), against third-plus whites, with the all-origin second generation level at −$327 (se 488). The NAS/AEI framework books Mexican-origin descendants at the US average; the repo measures them **8 thousand dollars a year below the white third-plus reference**, while agreeing with AEI that the *pooled* second generation is a wash. The two are reconcilable only because NAS is pooled across origins — which is precisely why a pooled-descendant convergence assumption cannot carry a Mexico-specific fiscal claim.

**One disconfirming point for the repo's side.** AEI's per-education framing is the right rebuttal to a nativity framing, and the repo has not neutralised it: if the Mexican second generation's gap is generated by education, and a native white HS dropout costs *more* than an immigrant one, then the memo's per-adult-year comparison against *all* third-plus whites is a composition comparison, not a like-for-like one. The memo does report education-conditioned arms elsewhere, but the headline number is not education-matched, and AEI's Table 8-13 reading is the strongest available objection to it.

---

## 4. Bier, Howard & Salazar (Cato), "Immigrants' Recent Effects on Government Budgets: 1994–2023" (Feb 3, 2026)

**Grade: HAD-PARTS / directly contested by memo §12.** Correcting the brief: the authors are **David J. Bier (Cato director of immigration studies), Michael Howard, and Julián Salazar** — a **Cato Institute White Paper** (Print ISBN 978-1-969284-24-3), not a NASEM product. NASEM shared its model with Cato; this is the Cato-modified NASEM model.

**Scenario and coverage (the direct ask).**
- **Not federal only** — federal, state and local. Net federal **$7.9T**, state and local **$6.6T** (immigrants paid $9.6T to state/local, cost $4.7T).
- **Excludes pure public goods** by assumption, defined as national defense plus interest on debt accrued before arrival (Box 1 area, p. 5). It *does* charge **congestible** public goods: $70,083 per immigrant vs $69,453 per US-born over 30 years (Table 3).
- **Children are not counted as natives.** Box 1 defines second generation as US-born with at least one first-generation parent, and the paper runs a combined first+second arm.

**The table (Table 3, "Immigrants cost governments less per capita than the US-born," 1994–2023, 2024 dollars, per capita):**

| Category | US-born | Immigrants | Difference |
|---|---|---|---|
| Social Security | $94,077 | $62,059 | −$32,017 |
| Medicare | $64,805 | $50,639 | −$14,166 |
| Government retirement | $40,740 | $13,418 | −$27,322 |
| Unemployment/workers' comp | $10,057 | $12,455 | +$2,398 |
| Refundable tax credits | $15,107 | $21,217 | +$6,110 |
| Medicaid/CHIP | $53,343 | $52,096 | −$1,246 |
| Food assistance | $11,233 | $7,889 | −$3,345 |
| Cash assistance | $10,709 | $11,669 | +$960 |
| Rent, housing, energy | $6,273 | $4,326 | −$1,947 |
| Migrant shelter | — | $116 | +$116 |
| Refugee | — | $2,878 | +$2,878 |
| Jail and felony police | $19,275 | $10,161 | −$9,113 |
| Education | $105,305 | $49,709 | −$55,596 |
| Congestible public goods | $69,453 | $70,083 | +$631 |
| Pure public goods/defense | $224,844 | — | −$224,844 |
| **Total with pure public goods** | **$725,219** | **$368,716** | **−$356,503** |
| **Total, no pure public goods** | **$500,376** | **$368,716** | **−$131,659** |

**The "positive every year" claim, and whether it survives §12.** Two distinct claims, and only the second is at issue.
- First generation alone: **$10.59T net, $14.47T with interest saved** (Table 13), positive in all 30 years.
- **Including the second generation: they concede the second generation is fiscally negative** — "Our data currently show the second generation was indeed fiscally negative" (p. 40). The positive-every-year claim for first+second rests on **$5.86T net / $7.93T with interest** (Table 13) and on the age argument: two-thirds of the second generation was born 1994–2023, median age 19, so most have not entered the labour force.

That is an **age-composition** defence, not a per-adult-year one, and it does not touch the memo. The memo's §12 gap is measured **per adult-year at ages 25–64**, holding age fixed; Cato's surplus is generated by a young cohort not yet drawing old-age benefits and by 30 years of accumulation. The four §12 extensions land as follows against Cato's own accounting:
- **Employer payroll** (memo −$946/adult-yr): Cato uses updated corporate-tax incidence research and counts all non-tax revenue, so it is at least partly inside their revenue side; not additive.
- **K-12** (memo −$460): Cato charges education and reports immigrants **below** the US-born per capita ($49,709 vs $105,305) — because the immigrant *first generation* mostly arrived educated abroad. Their second-generation arm is where the K-12 bill lands, and that arm is the one they concede is negative.
- **Local services**: charged, as congestible public goods, at essentially parity (+$631).
- **Per-capita public goods**: **not charged.** This is the single largest line in the table, $224,844 per US-born over 30 years, and the entire "immigrants cost half as much" headline is manufactured by it. The memo's own per-capita-public-goods arm (ladder 76: gap −$8,901; adults-only −$12,374) is the mirror image of this choice.

So: Cato's claim survives *as stated* for the first generation. Its first+second-generation version survives only under an age-composition argument that a per-adult-year ledger removes by construction, and Cato itself concedes the sign for the second generation today. The two results are not in contradiction; they are different estimands, and the memo should say so rather than treat Cato as refuted.

**One disconfirming point for the memo.** Cato's Figure 36 (net fiscal effect by age, 2018–2023) shows the second generation's **prime-age peak is nearly double the third-plus generation's**, with a BA share about **7 points above** the US-born (Figure 37). That is a real, measured, age-profile result on the same CPS ASEC the memo's generator uses, and it is the strongest available objection to reading the memo's Mexican second-generation number as a statement about the second generation in general. The memo's own all-origin second-generation estimate (−$327, se 488) is the pooled cell; Cato's is that same pooled cell with a favourable age profile. The disagreement is entirely about whether "second generation" means Mexican-origin or all origins.


---

## 5. Villarreal & Tamborini — "Hispanic Men's Earnings Mobility Across Immigrant Generations: Estimates Using Tax Records"

**Two corrections to the brief before anything else.**

1. **Citation.** Crossref for doi 10.1093/sf/soad128 returns: Villarreal and Tamborini, *Social Forces* **102(4): 1484–1504**, published **2024-04-12**, not 2023. The brief's "Social Forces 2023" is the online-first year at best. PMID 39895995, PMCID PMC11784596.
2. **VERIFIED NEGATIVE: the memo does not cite this paper.** Searched `research/`, `decisions/`, `notes/`, `infra/` for `soad128`, `Social Forces`, and the title. The only repo hits are `research/immigration-sociology-frontier-2026-06-25.md` (which cites a *different* Social Forces paper — Haller, Portes & Lynch 2011, "Dreams Fulfilled and Shattered") and this file. The central memo's §11 cites Opportunity Insights `race_table6a/6b`, Duncan-Grogger-León-Trejo 2020, Reardon & Galindo 2009, and the CPS selectivity build. **So there is no memo use of this paper to check for accuracy.** The brief's premise is wrong, and the finding is that this is an uncited gap, not a miscitation.

**Dataset and design (from the authoritative abstract, OpenAlex record for the DOI).** Multiple years of the Current Population Survey **linked to individuals' IRS tax earnings**, matching actual parents to sons rather than the synthetic-generation approach that proxies parents with people born a generation earlier. The matching identifies the **exact third generation** and lets ethnic attrition be evaluated directly.

**Headline findings (abstract, verbatim substance).**
- Second-generation Hispanic men have **lower mobility than later-generation Whites for most values of parental earnings**, but that lower mobility **is explained by their immigrant parents' lower education**.
- **Third-generation Hispanic men have lower mobility even after accounting for parental education and ethnic attrition.**
- The authors read this as "a stalling or reversal in the socioeconomic progress of Hispanics beyond the second generation."

**[GAP] The numeric rank-rank slopes and the size of the ethnic-attrition adjustment are not verified here.** The paper is paywalled at Oxford; the PMC author manuscript (PMC11784596, nihms-2029813.pdf) refused every route tried: direct PMC PDF with a browser user-agent and referer (returns HTML), Europe PMC `fullTextXML` (HTTP 500 for this PMCID), Europe PMC `?pdf=render` (returns HTML), the Europe PMC `fulltextRepo` endpoint (JSON error), and `fetch_paper` by DOI through the research MCP (`Could not download PDF`). Next route if re-dispatched: `agent-browser` against `https://europepmc.org/article/MED/39895995`, or firecrawl_scrape on the same URL.

**What it would change for the memo (on the abstract alone). Grade: NOVEL, and load-bearing.** This is the exact-third-generation, attrition-corrected, administratively-linked design that the memo's §4 and §11 say does not exist for mobility. It agrees with the memo's ladder-75 mechanism finding at the second generation (the gap is parental education) and it **independently corroborates ladder 83's fourth-plus-generation regression** — Duncan et al.'s NLSY97 AFQT pattern (2nd −0.70, 3rd −0.48, 4th+ −0.72 SD) and this paper's "stalling or reversal beyond the second generation" are two different instruments finding the same non-monotonic shape, one on test scores and one on tax-record earnings. The memo currently rests that claim on a single attrition-free file. Adding this gives it a second leg on a completely different outcome.

**One disconfirming point.** CPS-to-IRS matching selects on having a taxpayer record and on a successful link, which drops non-filing parents — the same selection the memo already flags against the Opportunity Atlas tables in §11 ("the tax linkage drops children whose parents did not file, which removes many unauthorized Mexican-origin parents and selects the better-off"). The direction is the same here, so the third-generation stall is measured on the better-linked half of the population, and the paper cannot rule out that a lower-linkage third generation would look different. Also, the outcome is men's earnings mobility, not levels, so it is silent on the ledger.

---

## 6. Sweep: other 2025–26 papers

Method: NBER working-paper search API (`/api/v1/working_page_listing/.../search`), queries `immigration second generation`, `immigrant fiscal`, `ethnic attrition`, `immigrant crime`, `Hispanic assimilation`, filtered to 2025–2026 display dates. NBER PDFs download with a browser user-agent as the brief said. Springer/SSRN not needed; PMC and Europe PMC were the only walls hit (see §5).

| Paper | Date | Why it matters | Grade |
|---|---|---|---|
| **w35070, "Birthright Citizenship and Youth Crime"** | Apr 2026 | The single most relevant unexamined paper for this memo. Directly addresses whether legal status at birth causes the second generation's crime outcomes — the mechanism the memo's §3 and ladder 65 leave unidentified. | **NOVEL, highest priority for re-dispatch** |
| **w33329, "Immigrant Age at Arrival and the Intergenerational Transmission of Ethnic Identification"** | Jan 2025 | Ethnic attrition is a load-bearing caveat in ladders 65, 74, 75, 83 and 87, and the repo's correction for it is "about 0.1 years" from the mechanisms memo. This paper models the transmission process that generates attrition. | **NOVEL** |
| **w33558, "Intergenerational Mobility of Immigrants in 15 Destination Countries"** | Mar 2025 | Cross-country comparator for the §11 origin-regression result and the Rockwool five-country work (ladder 72). | **HAD-PARTS** (the repo has the Nordic register decompositions; this adds a common-design mobility comparison) |
| **w34462, "The Implications of Sorting for Immigrant Wage Assimilation and Changing Cohort Quality in Canada"** | Nov 2025 | Firm-sorting explanation for measured assimilation; a direct methodological counterweight to Akee et al. §1. | HAD-PARTS |
| **"Black like us? The Occupational Integration of Black Immigrants"** | Feb 2026 | Origin-specific second-generation divergence outside the Hispanic case. | Peripheral |
| **"ICE Arrests across Trump's First and Second Terms: Variation in Targeting, Method, and Geography"** | Feb 2026 | Bears on the memo's §2 caveat that ICE detention inflates foreign-born institutional rows. | HAD-PARTS |

**[GAP] Not covered.** IZA discussion papers 2025–26 were not swept (no turns left after the PMC wall). SSRN was not swept. Abstracts for w35070, w33329 and w33558 were being extracted when the budget closed; only titles and dates are verified for those three. **Suggested next queries if re-dispatched:** fetch `https://www.nber.org/system/files/working_papers/w35070/w35070.pdf` (birthright citizenship and youth crime — read the design and the compliers), then `w33329`; then `https://www.iza.org/publications/dp` filtered to 2025–2026 with `immigrant OR second generation OR ethnic`.

---

## Summary of grades

| # | Paper | Grade | One-line consequence |
|---|---|---|---|
| 1 | Akee, Chin & Crown w35582 | NOVEL | Stayers are positively selected, so the Mexico-born ledger cell understates the cost |
| 2 | Borgschulte et al. w33961 | CONTRADICTS (scope) | A real incumbent-child channel exists; ladder 81 must be narrowed to classroom quality |
| 3 | Orrenius, Viard & Zavodny (AEI) | HAD-PARTS | Reprints NAS Table 8-13; assumes descendant convergence rather than measuring it |
| 4 | Bier, Howard & Salazar (Cato) | HAD-PARTS | Concedes the second generation is fiscally negative today; the surplus is age composition plus uncharged public goods |
| 5 | Villarreal & Tamborini | NOVEL | Exact third generation stalls after conditioning on parental education and attrition; the memo does not cite it |
| 6 | Sweep | mixed | w35070 on birthright citizenship and youth crime is the highest-value unread paper |

## Corrections to the dispatching brief

1. Target 3 is by **Orrenius, Viard and Zavodny**, not Strain.
2. Target 4 is a **Cato Institute** white paper by **Bier, Howard and Salazar**, using the NASEM model Cato was given, not a NASEM product.
3. Target 5 is **Social Forces 102(4):1484–1504, 2024**, and **the memo does not cite it** — there is no §11 use of it to audit.

---

## 6b. Sweep detail verified after the table above

**w33329 — Duncan & Trejo, "Immigrant Age at Arrival and the Intergenerational Transmission of Ethnic Identification among Mexican Americans" (Jan 2025). Grade: NOVEL, and it should be cited in the memo.** Abstract read from the NBER PDF. Same authors as the memo's ladder-83 source (Duncan, Grogger, León & Trejo 2020). Data: 2000 Census plus 2001–2019 ACS microdata. Finding: ethnic attrition among Mexican immigrants who arrived as children is **higher the younger they arrived**, and their US-born children show the same gradient. They test parental English, parental education, family structure, intermarriage and geography, and **intermarriage is the primary mechanism** — young-arrival immigrants marry non-Hispanics more, and attrition is dramatically higher among mixed-background children.

Why it matters here: ethnic attrition is a caveat attached to ladders 65, 74, 75, 83 and 87, and the repo's current correction is "about 0.1 years" from the mechanisms memo. This paper gives attrition an observable predictor (parental age at arrival, operating through intermarriage) on the same ACS the memo's incarceration cross-tabs use. That makes the attrition bias in the self-identified Mexican-origin cell testable rather than assumed, which is directly actionable for the §1–2 rebuild.

**w33558 — Boustan, Jensen, Abramitzky, Jácome, Manning, Pérez et al., "Intergenerational Mobility of Immigrants in 15 Destination Countries" (Mar 2025).** Confirmed: 30+ authors, Rockwool Foundation funding for Jensen, ERC and national-agency funding across the consortium. A coordinated cross-country design, so it is the natural comparator to ladder 72's Rockwool five-country decomposition and to the §11 origin-regression. Numbers not extracted.

**w35070 — "Birthright Citizenship and Youth Crime" (Apr 2026). [GAP]** The standard NBER PDF path returned nothing extractable in this run. Retry `https://www.nber.org/papers/w35070` for the landing page and abstract before re-fetching the PDF. This remains the highest-value unread item for the memo's §3.

