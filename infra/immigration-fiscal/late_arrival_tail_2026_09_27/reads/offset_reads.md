claude-opus-5-5

**Verdict:** A measured childcare/labor-supply offset exists for immigrant co-resident parents but no causal per-parent estimate does: the only US immigrant-specific estimate (Hu 2018, CPS 2006–14, correlational) puts a co-resident parent at +6 to +7.4 pp on a foreign-born mother's participation while she has a child under 6 (natives: −4.2 pp); general-population quasi-causal US estimates are +9 pp when a grandparent actually provides care (Posadas & Vidal-Fernández, FE) and 4–10 pp for proximity (Compton & Pollak), with no reliable hours effect (proximity acts on the extensive margin; co-resident single mothers work −4.1 h/week); Canada's reduced-form policy estimate (Frimpong & Compton) is −2.4 to −14 pp for immigrant mothers when parent sponsorship fell, with no per-parent first stage, and IRCC's 2024 survey (10% of sponsors 'able to return to work') is self-report. In dollars that is roughly $1,200–1,900 per year of a low-skill mother's gross earnings per co-resident parent, only in preschool years, and ×0.2–0.3 per admitted parent because only 19–26% of parent-visa holders provide any grandchild care (Australia PC Table 13.4); the public share of that (taxes on the extra earnings) is ≈ $100–400/yr, i.e. about 1–4% of a $10–20k annual per-parent public cost (gross earnings ≈ 6–19%), and it fades as the parent ages while costs rise. The offset is real in sign and small against the cost; no source found would move it to the same order of magnitude.

# Offsetting value of sponsored late-arriving parents: childcare and adult children's labor supply

Scope: measured effects of co-resident / nearby grandparents (esp. sponsored immigrant parents: US IR-5, Canada PGP, Australia parent visas) on mothers' employment/hours/earnings, plus fiscal-cost evidence on sponsored parents. Source tags per repo CLAUDE.md. Started 2026-09-27.

## Findings

- Sections below, appended in order of verification (2026-09-27).

## 1. Canada, IRCC Evaluation of the Family Reunification Program (2024 edition, covers 2014–2019 arrivals) — verified in full text

Source: IRCC Evaluation Division, *Evaluation of the Family Reunification Program*, Ci4-125/2024E-PDF, 41 pp. [SOURCE: https://www.canada.ca/content/dam/ircc/documents/pdf/english/corporate/reports-statistics/evaluations/family-reunification_en.pdf; local copy in scratchpad `frp2024.pdf`, pages cited by PDF page number]

Design: **self-report survey, no counterfactual** (not causal). PGP Sponsor Survey sent to 47,382 sponsors of PGPs arriving 2014–2019, "8,441 responses received (response rate of 17.8%)"; PGP Client Survey 5,613 responses, "response rate of 9.8%" (p. 14). Sample: all origins, Canada.

Key numbers (p. 29, verbatim): "33% of PGP sponsors reported that having their PGP in Canada allowed them to work full-time, 20% reported being able to work more hours, 11% reported being able to go to school/study, and 10% were able to return to work. More women (12%) than men (8%) reported that having their PGP in Canada helped them return to work."

p. 28: "unpaid contributions of PGPs or the costs that families would incur if PGPs were absent from their households are substantial but subjective in nature and thus difficult to measure." Most common household task "meal preparation (85%), followed by child care, and house cleaning" (Figure 15; the child-care % is only in the figure, not in extractable text) [GAP: Figure 15 child-care % not read].

The quantitative-evidence citation behind the labor-supply claim is internal: footnote 20 "IRCC (2020). Quantitative studies on the impact of grandparent care and proximity on labour force participation of their adult children especially daughters" and footnote 21 "IRCC (2019). Diagnostic: Measuring the contributions of Parents and Grandparents" — neither is public [GAP]. Footnote 19: Avila-Yipton (2017), uOttawa thesis [UNVERIFIED, not read].

Conversion: "10% able to return to work" is an upper-bound extensive-margin figure among responding sponsors (both sexes, selected responders, no counterfactual, and "allowed them to work full-time" is not a measured change). Treat as **at most ~10 pp extensive margin per sponsoring household, self-reported, likely inflated by response selection (17.8%) and by the survey's purpose**. Not usable as a causal effect.

Cost side, same report (IMDB 2021, PGP principal applicants arriving 2009–2020 who filed taxes):
- p. 24 (via p. 3 summary): "19% to 28% having employment income within their first ten years in Canada. The median employment income ranged from $11,600 to $16,400."
- p. 25: OAS "starting with 1% in YSA 1 and increasing to 10% in YSA 9, and 41% in YSA 10" (OAS residence test is 10 years since age 18; the jump at YSA 10 is the residence rule, not an undertaking break).
- p. 26: social welfare "2% in YSA 1 and increasing to 10% by YSA 9 and 26% in YSA 10"; "the 65+ age category had the highest incidence of Social Welfare benefits usage by YSA 10 (29%)".
- p. 27: EI "average of 7% ... over the first ten YSAs".
These are incidence rates, not dollars. Health-care use by PGPs is not measured in this report [GAP].

## 2. Hu (2018), "Filling the Niche: The Role of the Parents of Immigrants in the United States" — immigrant-specific US estimate, verified in full text

Source: Xiaochu Hu, *RSF: The Russell Sage Foundation Journal of the Social Sciences* 4(1): 96–116 (2018). [SOURCE: https://www.rsfjournal.org/content/rsfjss/4/1/96.full.pdf; printed page numbers below]

Sample: CPS monthly 2006–2014 (IPUMS), mothers 18+ of ≥1 child under 6, household heads or spouses; foreign-born n = 178,206 person-months (Table 3), native n = 752,120. Share with a co-resident parent: foreign-born 5.8%, native 3.0% (Table 1, p. 102). Foreign-born mothers' LFP mean 0.479 (Table 1).

Estimates (LPM coefficients, i.e. **percentage points**, although the author writes "percent"):
- Table 3 col. 2 (p. 105), "Parent present in the same household": **foreign-born +0.074*** (0.004)**; col. 1 **native-born −0.042*** (0.003)**. Text (p. 104): "having a coresiding parent significantly increases the probability of participating in the labor force for a foreign-born female with a preschooler by about 7 percent (0.074)."
- Table 3 col. 6 (p. 106): parent main effect 0.062*** (applies to the omitted high-school-or-less group), "HE_parent interaction 0.024**" → college-educated +8.6 pp. The author's text (p. 107) says the benefit "is significant only when the mother is college-educated", which misreads the table: the low-education main effect 0.062 is itself significant. For low-skill Mexican-origin families the relevant figure is **≈ +6 pp**.
- Table 3 col. 4 (p. 105, unclustered): "Latin_parent interaction −0.013 (0.024)" on a main effect of 0.064 → Latin America ≈ +5 pp (relative to omitted region; n.s. difference). With clustered SEs (col. 5) every regional interaction is uninformative (SEs ~50–140).
- IV (col. 3, retirement age of source country): coefficient 4.728, "implausibly large, denoting a weak instrument" (p. 104). **No credible IV result.**
- Difference-in-differences around a birth (Table 6, p. 108, foreign-born, n = 148,981): post-childbirth −0.067, coresiding parent 0.051, "Child-parent interaction 0.033 (2.040)**". Raw (Table 5, p. 107): LFP with no parent 58.21% → 53.51% after birth; with parent 65.31% → 65.08%.
- Hours: "logged hours worked last week ... similar. (Results are not shown here ...)" (p. 107) — **no usable hours estimate**.

Design grade: **correlational**. The "fixed effects" have "Group number 120" (Table 3), not individual fixed effects, so the 0.074 is essentially a cross-sectional association with controls; co-residence is endogenous (grandparents move in where the mother works, or a working couple sponsors a parent). The native estimate is negative (−4.2 pp), consistent with co-residence reflecting care *for* the elderly parent in native households. Positive selection of internationally mobile grandparents is the author's own explanation for the sign difference (p. 104).

Conversion: +6 to +7.4 pp LFP for a foreign-born mother of a preschooler per co-resident parent (not per grandparent; a household can hold two). Applies only while a child under 6 is present.

## 3. Compton & Pollak, "Family proximity, childcare, and women's labor force attachment" — general US population, verified in full text (NBER WP version)

Source: Janice Compton & Robert A. Pollak, NBER Working Paper 17678 (Dec 2011); published *Journal of Urban Economics* 79 (2014): 72–90, doi:10.1016/j.jue.2013.03.007. Pages below are the WP's printed pages. [SOURCE: https://www.nber.org/system/files/working_papers/w17678/w17678.pdf]

Sample: NSFH waves I–II (1987–94), married women 25–60 with mother and mother-in-law "ALUS" (alive, living in US); plus 2000 Census PUMS birth-state proxy and military wives. **Excludes grandparents living abroad**: "By excluding those whose mothers are not ALUS, our sample under-represents migrants to the U.S." (fn. 19, p. 16). Not immigrant-specific.

Key numbers:
- Abstract (p. 1): "the predicted probability of employment and labor force participation is 4-10 percentage points higher for married women with young children living in close proximity to their mothers or their mothers-in-law compared with those living further away."
- IV on received childcare (p. 15): "Marginal effects are significant, ranging from 5.1 to 6.2 percentage points."
- Table 5 (p. 17 text): with children ≤12, "close proximity to mother-in-law or to both mother and mother-in-law increases the predicted probability of employment by 10 percentage points. The coefficient on close proximity to only her mother is positive, but insignificant."
- Table 4 (p. 34), NSFH wave II, married women: near both mothers probit marginal 0.073; Tobit usual weekly hours +3.429* (fitted mean 19.29 h). Unmarried women: **"Coreside with Mother" probit −0.228* (marginal −0.073), Tobit −4.103* weekly hours** — co-residence *lowers* work for single mothers.
- Intensive margin (p. 17): "the effect of proximity is primarily on the extensive margin ... rather than on the intensive margin". No effect where the grandmother is in poor health (Table 5 cols 5–6).

Design grade: **proximity treated as exogenous (reduced form) plus an IV with proximity instruments; correlational-to-weakly-identified**. Relevance to IR-5 parents: effect is of *proximity* (within 25 miles), with co-residence folded into "close" for married women; own-mother-only proximity (the sponsored-mother analogue for a daughter) is insignificant in NSFH (Table 4 col 2: 0.008). Conversion: **~0–10 pp extensive margin; ≈+3.4 h/week unconditional (Tobit latent, not a marginal effect) only when near both mothers**.

## 4. Posadas & Vidal-Fernández (2013), "Grandparents' Childcare and Female Labor Force Participation" — general US population, verified in full text (tables are images; numbers from text)

Source: *IZA Journal of Labor Policy* 2:14 (2013), doi:10.1186/2193-9004-2-14 (open access) [SOURCE: https://link.springer.com/article/10.1186/2193-9004-2-14]; earlier IZA DP 6398 (2012) [SOURCE: https://docs.iza.org/dp6398.pdf].

Sample: NLSY79 + Children of NLSY79, mothers 18–49 interviewed 1979–2006, child aged 0–3; treatment GPC = a grandparent is the primary/secondary/tertiary childcare arrangement. Not immigrant-specific (NLSY79 is a US-resident youth cohort).

Key numbers (Section 5, Table 3):
- "OLS estimates suggest that when grandparents take care of grandchildren, young mothers are almost 16 percentage points more likely to participate in the labor force."
- Preferred FE: "young mothers' likelihood of participating in the labor force significantly increases by 9 percentage points on average". Drops "from 0.09 to 0.08" when the year before the maternal grandfather's death is controlled (Section 6.1).
- IV (maternal grandmother's death): "IV produces imprecise estimates and they are very similar in magnitude to OLS" (the 2012 DP: "The IV point estimate of the effect of grandparents is 0.3 points larger than OLS", F > 312).
- Heterogeneity (Table 4): effect larger "for Black, Hispanic, and single or never married mothers".

Design grade: **quasi-causal (women's FE; IV imprecise)**. Estimand is the effect of *using* grandparent care, conditional on a child 0–3 — an upper bound on the effect of a grandparent's *presence*, since not every present grandparent provides care and the effect lasts only while a child is 0–3 (or up to school age). Conversion: **+9 pp maternal LFP per household with grandparent care of a 0–3 child**. No hours estimate.

## 5. Frimpong & Compton, "Family Immigration Policy and Women's Employment" — Canada, immigrant-specific, quasi-experimental (triple difference); verified in thesis full text

Source: NanaAma (Jennifer) Frimpong, *Three Essays on the Labour Market Integration of Immigrants in Canada*, PhD thesis, University of Manitoba (2023/24), ch. 1 (co-authored with Janice Compton); SSRN 4397876 (2023). Printed page numbers. [SOURCE: https://mspace.lib.umanitoba.ca/server/api/core/bitstreams/68fe4abf-1ec4-4f64-aa0e-045c96755358/content]

Design: StatCan LAD 1983–2005 linked to IMDB; triple difference (immigrant × young children × post-1995), dropping 1992–1995; treatment is the mid-1990s policy shift away from family class, which cut the PGP share of arrivals (Figure 1.2, p. 12). Outcome: positive employment income (extensive margin) and high/low income (multinomial). Immigrant-specific, all origins, Canada.

Key numbers (p. 20, Table 1.3 col. A): "the policy lowered the probability of employment for economic class and family class immigrants with young children by 4.8 and 2.4 percentage points respectively. The impact of the policy is even larger for women refugees and those in other immigrant classes, with an estimated reduction of 14 and 12 percentage points respectively." Abstract: "participation rates for immigrant mothers with young children that were 2.4 to 14.8 percentage points lower than expected." Intensive margin (p. 21): economic- and family-class mothers shifted from high-income (≥ full-year-full-time average) to low-income employment; refugee mothers "49 percent less likely to earn a relatively high income".

Design grade: **quasi-causal reduced form, but not a per-grandparent effect**. There is no first stage: the paper never measures how many fewer grandparents each mother had nearby, so the coefficient is an intention-to-treat effect of a program-wide policy on all resident immigrant mothers. The 1995 package also changed selection of the mothers themselves (points system) and coincided with provincial welfare cuts (Ontario 1995) — the triple difference nets out changes common to all mothers but not immigrant-mother-specific shocks [INFERENCE]. The largest effects fall on refugees, the group least likely to have been sponsoring parents anyway, which weakens the childcare-channel reading [INFERENCE]. It is nonetheless the only quasi-experimental estimate found that ties *parent-sponsorship policy* to immigrant mothers' employment, and its sign supports an offset.

## 6. Australia, Productivity Commission (2016), *Migrant Intake into Australia*, Inquiry Report No. 77 — both sides, verified in full text

Source: [SOURCE: https://assets.pc.gov.au/inquiries/completed/migrant-intake/report/migrant-intake-report.pdf; printed page numbers]

**Share of parent-visa holders who provide childcare at all** (Table 13.4, p. 473; ABS Australian Census and Migrants Integrated Dataset 2011, arrivals 2009–Aug 2011): "Providing childcare, but not for own children", both applicants: **Parent (103) 18.7%; Contributory Parent (143) 26.1%**; skilled 1.7%. Text (p. 472): "between 75 and 80 per cent of such parents do not provide any such childcare." This is census-measured (any unpaid childcare in the reference fortnight), not a labor-supply effect.

The KPMG figure the PC rejects (p. 472): "Boucher (sub. DR128) cited 2009 evidence from KPMG that aged parents could save their sponsors ... $13 800 per year in childcare costs for a family with two children, as well as allowing that household to generate an additional $55 066 in income." PC's verdict (p. 473): "such estimates ... are estimates of what 'could' apply, rather than estimates of what typically applies" and "the actual savings to the Australian community from the child-caring role of people on permanent parent visas is a small fraction of the value cited in the KPMG report." Reasons listed (pp. 472–473): applies only to the minority who provide care; "the need for childcare is greatest for infants, and so often not enduring. In contrast, the responsibilities of taxpayers for supporting the parent visa stream apply throughout the rest of their lives"; much of the benefit is private; grandparents can do this on temporary visitor visas. [UNVERIFIED: the KPMG 2009 report itself, not read.]

**Cost side** (p. 478): "In 2008, the AGA estimated that in present value terms, the cumulated lifetime fiscal costs of a parent visa holder was between $230 000 and $285 000 per adult (AGA 2008). Using the AGA's annually updated cost indexes ... the estimated cost in 2015 is between around $335 000 and $410 000 per person (with the 'best' estimate being just over $370 000). The actual charge applied is roughly one tenth of this cost for contributory visa holders and about 1 per cent for non-contributory visa holders." Overview (p. 27): the liability for "these 8700 parents over their lifetime ranges between $2.6 and $3.2 billion in present value terms." Currency AUD 2015–16. Footnote 1, p. 534: the estimate "does not incorporate some possible fiscal savings, such as childcare subsidies where grandparents look after children".

Conversion [CALCULATION: 370,000 AUD PV; at ~0.75 USD/AUD 2015 ≈ US$280k PV per adult; spread over ~20 remaining years ≈ US$14k/yr undiscounted-equivalent, order-of-magnitude only]. This is age-related Commonwealth spending (pension, health, aged care), net of taxes.

Design grade for the offset: **measured prevalence of care (19–26%), no labor-supply estimate**. Useful as the take-up multiplier: any per-caregiver labor-supply effect must be scaled by ~0.2–0.3 to be per-admitted-parent.

## 7. Bansak, Dziadula & Zavodny (2026), "The role of coresident grandparents in the Asian-white maternal employment gap in the US" — US, correlational, abstract and text read; coefficient tables not extracted

Source: *Journal of Population Economics* 39: 26 (2026), doi:10.1007/s00148-026-01170-2, open access [SOURCE: https://link.springer.com/article/10.1007/s00148-026-01170-2]. Data: 2000 Census + 2001–2019 ACS (IPUMS), SIPP for caregiving. Authors call their approach "descriptive" (Section 2 end). Quotes: "living in an intergenerational household tends to be positively related to employment for Asian women, especially if they are foreign-born or have young children, but negatively related to employment for white women"; "grandparent coresidence is more strongly related to maternal employment among foreign-born women than among US natives, suggesting that immigrants may be more likely to bring over their parents if they need childcare" (abstract). "The maternal employment gap is about 10 percentage points smaller among Asian women than among white women" (Introduction). Hispanic/Mexican women are not analysed. [GAP: regression coefficients sit in table images; not extracted.] Corroborates Hu's sign pattern (positive for immigrants, negative for natives); the authors' own reading is reverse causation (parents brought over *because* childcare is needed), which cuts both ways for a causal offset.

## 8. US cost side: sponsor deeming and affidavit-of-support enforcement — GAO-09-375, verified on GAO's product page

Source: GAO, *Sponsored Noncitizens and Public Benefits: More Clarity in Federal Guidance and Better Access to Federal Information Could Improve Implementation of Income Eligibility Rules*, GAO-09-375 (May 2009) [SOURCE: https://www.gao.gov/products/gao-09-375 ; https://www.gao.gov/assets/gao-09-375.pdf]. Page numbers as quoted by House Ways and Means (2009-05-29) [SOURCE: https://waysandmeans.house.gov/2009/05/29/gao-almost-no-state-ensures-taxpayers-paid-back-if-sponsored-noncitizens-collect-welfare-benefits/]; wording checked against the GAO highlights text.

- Repayment: "In total, only two states have pursued sponsor repayment" (Highlights); "SSA officials told us that neither its regional nor field offices have pursued sponsor repayment of SSI benefits" (p. 24).
- Deeming: "69 percent indicated that cases involving sponsor deeming had seldom or never occurred in their states during the past 2 years" (p. 11). SSI: SSA officials in "all 10 SSA regional offices reported that deeming has occurred either rarely or never since PRWORA became effective", because deeming does not apply once 40 quarters are credited and most sponsored noncitizens qualify for SSI only via that route (GAO text).
- Consequence: "certain sponsored noncitizens may receive means-tested public benefits based on their income and assets alone, even though they have sponsors who signed legally enforceable affidavits" (p. 27).
- Statutory context [SOURCE: same]: sponsor income must be ≥125% of poverty; the affidavit runs until naturalization or 40 quarters. A sponsored parent who naturalizes (eligible after 5 years of LPR status) leaves deeming entirely and qualifies for SSI/Medicaid on own income [INFERENCE from the statute GAO describes; the naturalization termination is the standard 8 U.S.C. 1183a rule — not re-read here, [UNVERIFIED] at primary].
- Status: GAO's recommendation to CMS was closed after CHIPRA 2009 let states waive deeming for some Medicaid applicants; HHS 2011 found "approximately half of states have opted to adopt the CHIPRA waiver" (GAO recommendation table).
[GAP: no SSA/CRS table read giving SSI take-up by elderly naturalized former IR-5 parents; suggested next query: SSA Research and Statistics Note on SSI noncitizen recipients by age and citizenship, and CRS RL33809.]
The Canadian parallel (IRCC 2014 evaluation, key findings, archived HTML read through §3.2): "the undertaking that is signed by PGP sponsors was shown to have an important containment effect on the use of social assistance by PGPs, with reliance on social assistance spiking following the termination of the undertaking" [SOURCE: https://www.canada.ca/en/immigration-refugees-citizenship/corporate/reports-statistics/evaluations/family-reunification-program.html, Executive summary]. [GAP: §3.3–3.4 of the 2014 evaluation (childcare %, SA rates by age at landing) not read: canada.ca DNS failed locally and Firecrawl credits exhausted.]

## 9. Comparison table

Effects are on the adult daughter's (mother's) labor supply. "Per co-resident parent" conversions assume one parent in the household; $ uses an assumed annual earnings of a low-skill immigrant mother who works of $20–25k [ASSUMPTION, not sourced here; check against the lane's ACS earnings for Mexico-born mothers] and apply only in years with a preschool child.

| Study | Sample, country, years | Treatment | Design | Employment effect | Hours/week | $/yr per co-resident parent (gross earnings) | Cite |
|---|---|---|---|---|---|---|---|
| Hu 2018 | Foreign-born mothers of child <6, US CPS 2006–14 | Co-resident parent | Correlational (120-group FE; IV weak) | +7.4 pp all; +6.2 pp HS-or-less; natives −4.2 pp | not reported | ≈ $1,200–1,900 (6.2–7.4 pp × $20–25k) | Table 3 cols 1, 2, 6, pp. 105–106 |
| Hu 2018 DiD | Foreign-born women 18–45 around a birth | Co-resident parent × birth | Weak DiD (16-month CPS panel) | +3.3 pp (cushions a −6.7 pp birth drop) | n.r. | ≈ $700–800 | Table 6, p. 108 |
| Bansak–Dziadula–Zavodny 2026 | Asian vs NH-white mothers, US Census/ACS 2000–19 | Intergenerational household | Descriptive | Positive for foreign-born Asian, negative for whites (coefficients not extracted) | — | — | Abstract, Introduction |
| Frimpong & Compton 2023 | Immigrant mothers of young children, Canada LAD 1983–2005 | 1995 shift away from family class (fewer PGPs) | Triple difference, reduced form, no first stage | −2.4 (family class) to −14 pp (refugees); −4.8 pp economic class | shift to low-income employment | not per parent (no first stage) | Table 1.3, p. 20–21 |
| IRCC 2024 evaluation | PGP sponsors, Canada, arrivals 2014–19 (n = 8,441, 17.8% response) | Having PGP in Canada | Self-report, no counterfactual | 10% "able to return to work"; 33% "allowed them to work full-time"; 20% "work more hours" | — | upper bound only | p. 29 |
| Posadas & Vidal-Fernández 2013 | US mothers of child 0–3, NLSY79 1979–2006, not immigrant-specific | Grandparent provides childcare | Women's FE (IV imprecise) | +9 pp (FE), +16 pp (OLS) | n.r. | ≈ $1,800–2,300 if care is provided; × 0.2–0.3 take-up (PC) ≈ $400–700 per parent | §5, Table 3 |
| Compton & Pollak 2014 | US married women, NSFH 1987–94 + Census, not immigrant-specific; excludes grandmothers abroad | Living within 25 miles | Reduced form + IV | 4–10 pp; own mother only: n.s. (0.008); single women co-residing: −7.3 pp | +3.4 (near both mothers, Tobit); −4.1 for co-residing single mothers | ≈ $0–2,500 | Abstract p. 1; Table 4 p. 34; p. 17 |
| Productivity Commission 2016 | Parent-visa holders, Australia Census-migrants 2011 | — | Measured prevalence | Only 18.7% (103) / 26.1% (143) of parent-visa holders provide care to others' children | — | KPMG "could" figure A$13,800 childcare + A$55,066 income, rejected by PC | Table 13.4, pp. 472–473 |

Cost comparators: Australia AGA lifetime net fiscal cost of a parent visa holder A$335–410k PV, best ≈ A$370k (p. 478); Canada PGP social welfare incidence 26% and OAS 41% at year 10 (IRCC 2024 pp. 25–26); US deeming/repayment essentially unenforced (GAO-09-375).

[CALCULATION] Fiscal value of the offset: the public account gains only the taxes on the extra earnings (plus any avoided childcare subsidy), not the earnings. At a combined federal+state+payroll rate of roughly 10–20% on a low-wage second earner, $1,200–1,900/yr of extra earnings is ≈ $120–380/yr of revenue; for a low-income mother in the EITC phase-in range the net fiscal effect can be near zero or negative [INFERENCE]. The effect lasts only the years a grandchild is under ~6 (roughly 5–10 of the parent's remaining ~20–25 years), while age-related costs rise over time.

## 10. Coverage, gaps, next queries

Read in full text: IRCC 2024 evaluation (pp. 3, 14, 24–29); Hu 2018 (pp. 102–108); Compton & Pollak NBER WP (pp. 1, 15–17, 34); Posadas & Vidal-Fernández 2013 (text; tables are images); Frimpong thesis ch. 1 (pp. 10–12, 20–21); PC 2016 (pp. 27, 472–473, 478, 534); GAO-09-375 (highlights and quoted pages). Partly read: IRCC 2014 evaluation (through §3.2); Bansak–Dziadula–Zavodny 2026 (text, not tables).
Not read: Chen 2023 (Wellesley undergraduate thesis; reduced-form +2 pp per one-child fall in origin fertility, not per grandparent) [UNVERIFIED beyond search excerpt]; Arpino, Pronzato & Tavares 2014; García-Morán & Kuehn 2017; Zamarro; Ramos & Yoshida 2012 (LSIC, Canadian Ethnic Studies); Avila-Yipton 2017; IRCC internal 2019/2020 diagnostics (not public); KPMG 2009.
[GAP] No Mexico- or Hispanic-specific estimate. [GAP] No hours or earnings estimate for immigrant mothers. [GAP] SSI/Medicaid take-up of naturalized former IR-5 parents not sourced (next: SSA ORES SSI noncitizen tables; CRS RL33809).
Next queries if re-dispatched: "Arpino Pronzato Tavares 2014 instrumental variable grandparental support mothers' labour market"; "Garcia-Moran Kuehn with strings attached Review of Economic Dynamics"; IRCC 2014 evaluation §3.3 via publications.gc.ca Ci4-125/2014E-PDF; ACS replication of Hu restricted to Mexico-born mothers with an IR-5-age co-resident parent.
