claude-opus-5[1m]

**Verdict:** IN PROGRESS [UNVERIFIED]

# Literature verification — school flight, diversity & public goods, voucher outcomes
Dispatched 2026-09-18. Repo: /Users/alien/Projects/immigration-research

## Scope
1. Betts & Fairlie 2003 JPubE — native flight from public to private schools ("1 native per 4 immigrants")
2. Poterba 1997 JPAM — elderly share × racial difference → per-child education spending
3. Alesina, Baqir & Easterly 1999 QJE — ethnic fragmentation → productive public goods shares
4. Hopkins 2009 JOP — "the diversity discount"
5. DISCONFIRMATION (weighted equally)
6. Child-level outcomes of public→private switchers (vouchers, Catholic schools)

## Findings

- [PENDING] no items verified yet.

---

## 1. Betts & Fairlie 2003, JPubE 87: 987–1012 — VERIFIED, figure is (a) EXACTLY what the paper says

**Claim checked:** "about one native leaves public secondary school per four immigrant arrivals."

**Verdict: (a) exactly what the paper says** — the phrase appears in the abstract verbatim, and twice more in the text.

Abstract, p. 987 [SOURCE: Betts & Fairlie 2003, JPubE 87(5-6):987-1012, DOI 10.1016/S0047-2727(01)00164-5; PDF http://people.ucsc.edu/~rfairlie/papers/published/jpube%202003%20-%20native%20flight.pdf]:
> "The analysis uses 1980 and 1990 Census data from 132 metropolitan areas. For primary school students, no significant relation between immigration and private school enrolment is found. For secondary schools, a significant link emerges. **For every four immigrants who arrive in public high schools, it is estimated that one native student switches to a private school.** White students account for most of this flight. Natives appear to respond mainly to immigrant children who speak a language other than English at home."

p. 1001: "Each immigrant added to the public schools in an MA results in a predicted decrease of 0.26 native students in public schools ... for every four immigrants added to the public schools in an MA, just over one additional native is predicted to switch to private school."
Conclusion p. 1008: "Each immigrant added to the public high schools in a metropolitan area is predicted to result in a decrease of about 0.25 native-born children in the schools."

**Headline coefficients (Table 2, p. 1000 — secondary school; Table 3, p. 1004 — primary):**

| Spec | Secondary: immigrant-share coef (SE) | Scaled derivative | Primary: coef (SE) | Scaled derivative |
|---|---|---|---|---|
| (1) GLS (preferred) | 1.7766 (0.8514) | **0.2594** | −0.7940 (0.8375) | −0.1889 |
| (2) OLS | 1.5394 (0.9267) | 0.2248 | −1.1932 (0.8550) | −0.2838 |
| (3) IV | 3.9049 (2.3059) | 0.5702 | 1.4422 (2.8519) | 0.3431 |

Sample size = 132 MAs in every column.

**Secondary vs elementary ratio:** the elementary estimate is not a smaller positive — it is *negative and insignificant* in the preferred GLS and OLS specs. Paper, p. 1003: "We find negative, although statistically insignificant, coefficients on the immigrant share... We conclude that there is no evidence of a statistically significant link between immigration inflows and changes in native parents' decisions about whether to send their children to private schools at the primary level."

**Sample / design:** native-born children enrolled in school, not in group quarters, 1980 and 1990 Census microdata, 132 metropolitan areas. Two-stage probit of Borjas & Sueyoshi (1994): stage 1 = individual probit of private-vs-public enrolment with MA dummies and MA×1990 dummies; stage 2 = regress the MA×1990 coefficient (the 1980→1990 change in the MA fixed effect) on 1980→1990 *changes* in MA-level covariates. So the headline is a **first-differenced MA panel of two cross-sections, not an IV estimate**.

**Identification:** the preferred number is GLS on first differences, i.e. it leans on MA fixed effects plus controls (per-pupil spending, pupil/teacher ratios public and private, crime rate, native black share, log native employment, log native 5–18 population, native public-assistance rate). IV is a *robustness check only*: Altonji–Card (1991) style, using "the 1980 value of our immigration measure as an instrument for the change in its value from 1980 to 1990" (p. 1002). The authors explicitly downgrade it: "The coefficient estimate on the immigrant share is much larger (although its 95% confidence interval captures both the GLS and OLS coefficient estimates and the null hypothesis of no effect at all). **The IV model is thus not at all conclusive**" (p. 1002). [SOURCE: same PDF, p. 1002]

**Immigrants generally, or non-English-speaking?** Specifically non-English-speaking. Table 4 / p. 1003–1005: "For secondary school students, we find positive and statistically significant coefficient estimates on the non-English-speaking immigrant share, and a much smaller and statistically insignificant coefficient on the English-speaking immigrant share. The positive coefficient estimate on the non-English-speaking immigrant share is 13% larger than the original coefficient estimates reported in Table 2, suggesting that 'native flight' is almost purely from non-English-speaking immigrants."

**Who flees:** non-Hispanic white natives. Table 5 / p. 1006: "the addition of one immigrant to the public school system leads 0.28 white natives to switch from public to private schools ... the behavior of white native families is primarily responsible for our overall finding." Minority natives: "at the secondary level some very weak evidence of native minority flight emerges. However, the scaled derivative for this group is very small compared to that for white natives" (p. 1007). Sample restriction for minorities: MAs with ≥200 observations in both years, dropping 74 MAs from the secondary sample.

**IMPORTANT SCALE CAVEAT the memo must carry.** The "1 per 4" ratio is a per-immigrant derivative, not an aggregate share shift. The paper's own aggregate simulation (p. 1008): "For our sample of 132 MAs, the private secondary school rate was 10.29% in 1980. If nothing else had changed between 1980 and 1990, the percentage of secondary school natives attending private schools is predicted to have risen to 10.64% by 1990, **an increase of 0.34 percentage points or 3.3%**." Arc elasticity of the private secondary share w.r.t. the immigrant/population ratio = **0.143**. And: "Clearly, at the national level trends in the immigrant share are unlikely to have led to major swings in the enrolment shares of public high schools." Metro heterogeneity is where the action is: predicted rises of 1.34 pp (14.7%) in Los Angeles, 1.42 pp (12.7%) in San Francisco, 2.51 pp (20.0%) in Miami.

**Native black share:** the comparison regressor is positive but small and insignificant in every spec (secondary GLS 0.3900, SE 0.7068). The authors note this may be an artifact of no variation: "the native black share increased by only 0.5 percentage points from 1980 to 1990" (fn. 26, p. 1002). This is a design limitation, not evidence that Black share does not drive flight — see §5.

**Confidence: HIGH** (full text of the published article read; abstract and three in-text statements agree).

---

## 2. Poterba, "Demographic structure and the political economy of public education" — VERIFIED with an important caveat: the racial-difference result is NOT an interaction and is NOT significant in the fixed-effects specs

**Source used:** NBER WP 5677 (July 1996), the working-paper version of JPAM 16(1) 1997: 48–66. [SOURCE: https://www.nber.org/system/files/working_papers/w5677/w5677.pdf]. Cached at `_cache/poterba_w5677.pdf`. **[UNVERIFIED]** whether the published JPAM tables differ from the WP tables — I read the WP, not the JPAM typeset article. Numbers below are WP numbers.

**Sample / design:** panel of the 48 continental US states, **four years only: 1961, 1971, 1981, 1991** (Table 3 notes, p. 33). Dependent variable = log real per-child K-12 government spending (ED/CHILD), 1992 dollars. Specifications: OLS, then three columns with state and time fixed effects (adding urban share, then poverty share). All variables in logs except the racial-difference variable.

**Headline elderly effect (Table 3, p. 33):**

| Variable | OLS | FE (1) | FE + urban | FE + poverty |
|---|---|---|---|---|
| Population share aged 65+ | 0.029 (0.068) | **−0.276 (0.121)** | −0.155 (0.125) | −0.264 (0.121) |
| Population share aged 5–17 | −0.404 (0.132) | −0.998 (0.212) | −0.940 (0.208) | −0.986 (0.212) |

Text, p. 16: "These estimates suggest an elasticity of per-child spending with respect to the over-65 population share of approximately **−.25**. The results are attenuated when the fraction of the population in urban areas is included in the specification; in this case the estimated coefficient is not statistically significant at conventional significance levels."
Magnitude framing, p. 16: "a one standard deviation change in the share of elderly in the population, a shift from .108 to .130, results in almost of five percent decline in per-pupil education spending."
Note also the school-age elasticity of ≈ −1.0: a larger child cohort does not get proportionately more money.

**The race result — what it actually is.** The variable is **(nonwhite % of the age 5–17 population) − (nonwhite % of the 65+ population)**, entered as a *level* (it takes negative values), as an **additive regressor, not as an interaction with the elderly share**. Table 5, p. 35:

| | OLS | FE (1) | FE + urban | FE + poverty |
|---|---|---|---|---|
| NW% age 5–17 − NW% age 65+ | **+0.770 (0.342)** | **−0.621 (0.394)** | −0.502 (0.388) | −0.561 (≈0.39) |
| Population share aged 65+ | −0.037 (0.064) | −0.244 (0.122) | −0.136 (0.126) | −0.238 (0.122) |

Text, p. 21: "While the estimated coefficient on this variable is positive in the OLS estimates, the coefficient is negative (**although not statistically significant at standard confidence levels**) when the model includes state and time effects. Including this variable does not substantially affect the estimated coefficients for either the aged share or school-aged share of the population."
Magnitude, p. 21: "The estimate in Table 5, column 2 suggests that a one percentage point increase in the share of nonwhites in the 0-17 population, holding the share of nonwhites in the 65+ population constant, reduces the log of per-child school spending by **−.006, or approximately one half of one percent**." (This is the −0.621 coefficient × 0.01.)

Sample means for the variable, p. 18: "On average, the nonwhite share of the school aged population is 6.5 percentage points higher than the nonwhite share of the 65+ population." SD of the difference is only 0.047 (fn. 13), so the identifying variation is thin.

**So: how the abstract states it vs. what the tables show.** Abstract, p. 1: "an increase in the fraction of elderly residents in a jurisdiction is associated with a significant reduction in per child educational spending. **This reduction is particularly large when the elderly residents and the school-age population are from different racial groups.**" The tables do not contain an elderly×race-gap interaction term. The support is (i) a negative but statistically insignificant *additive* coefficient (t ≈ 1.6) in the FE specs, and (ii) the contrast with Table 6, where the same variable predicts **higher** per capita non-education spending, significantly, in all four columns — p. 21: "The coefficient estimates are positive, and in all four specifications the null hypothesis of zero effect can be rejected. These results bolster the argument that demographic heterogeneity tends to reduce spending on education, particularly in relation to spending on other programs."

The one place Poterba does run an interaction with the elderly share is Table 7 (long-term-resident share, property-tax circuit breakers). There, p. 23: "In a state in which all of the residents had been there five years ago, the percent elderly variable would have essentially no effect on school spending. In a state with only half of the population resident for five or more years, the estimated elasticity of school spending with respect to the elderly share would be −.50." But on the racial variable specifically: "the effects in this case are estimated with too little precision for further discussion."

**Poterba's own caveat:** he flags a demand-vs-technology identification problem and declines to resolve *why* the elderly spend less (fn. 11, p. 17): "A key issue for future research is *why* they spend less. This may simply reflect a lack of support among elderly voters for public programs that do not benefit the elderly, or it may reflect a higher cost of raising funds in states with more elderly."

**Confidence: HIGH on the numbers (tables read directly); MEDIUM on transfer to the published JPAM version. A memo should cite the elderly elasticity ≈ −0.25 as the solid result and must NOT present the racial-difference result as a significant interaction effect.**

---

## 6a. DC Opportunity Scholarship Program (randomized lottery) — VERIFIED, and the sign is NEGATIVE then null

All three IES/NCEE reports read in full from the primary PDFs (cached in `_cache/`).

**Design:** randomized lottery among applicants; oversubscribed DC voucher program under the SOAR Act. ITT ("scholarship offer") and TOT ("scholarship use") both reported. Outcomes = norm-referenced standardized reading and math tests (TerraNova 3rd ed.).

**Year 1** [SOURCE: Dynarski et al., NCEE 2017-4022, "Evaluation of the DC Opportunity Scholarship Program: Impacts After One Year," p. xii / p. 19]:
> "After one year, the OSP had a statistically significant negative impact on the mathematics achievement of students offered or using a scholarship. Mathematics scores were lower for these students a year after they applied to the OSP (by **5.4 percentile points** for students offered a scholarship and **7.3 percentile points** for students who used their scholarship) ... Reading scores were lower (by **3.6** and **4.9** percentile points, respectively) but the differences were not statistically significant."
Effect sizes, fn. 21: "reading and mathematics score effect sizes are **−0.09 and −0.12**."
Notably, the negative impacts were **concentrated among students NOT coming from low-performing schools**: "There were no significant achievement impacts, positive or negative, for students applying from low-performing schools (those designated as 'in need of improvement' or SINI) ... Negative impacts for both mathematics and reading scores were statistically significant for students who were not attending SINI schools when the students applied for the scholarship and also for students in grades K–5."

**Year 2** [SOURCE: Dynarski et al., NCEE 2018-4010, p. xiii / p. 19]:
> "The OSP had a statistically significant negative impact on mathematics achievement after two years. Mathematics scores were lower for students two years after they applied to the OSP (by **8.0 percentile points** for students offered a scholarship and **10.0 percentile points** for students who used their scholarship) ... Reading scores were lower (by **3.0** and **3.8** percentile points, respectively) but the differences were not statistically significant." Here the negative math impact WAS significant for the SINI priority group too.
*Caution:* the Year-2 effect-size footnote (fn. 31) prints "−0.09 and −0.12", identical to Year 1 despite larger percentile-point gaps; this looks like a footnote carried over from the Year-1 report. **[UNVERIFIED]** — use the percentile-point figures, not the Year-2 SD figures, unless the Appendix A table is checked directly.

**Year 3** [SOURCE: Webber, Rui, Garrison-Mogren, Olsen & Gutmann, NCEE 2019-4006, p. 4]:
> "There were no statistically significant impacts on either reading or mathematics achievement three years after students applied to the program. Students in the group that received a scholarship offer scored **0.1 percentile points higher** on the mathematics test, and **1.6 percentile points lower** on the reading test... Students using a scholarship scored 0.2 percentile points higher on the mathematics test, and 2.1 percentile points lower on the reading test. None of the differences were statistically significant." (n = 571 T / 366 C reading; 569 T / 365 C math.)
Synthesis across the three reports, p. 10: "The program had no effect on reading achievement in any of these years. However, for mathematics, negative impacts reported in the first two years were not found in the third year."
Scholarship use had fallen to 68% of the treatment group by year 3, but the report rules that out as the explanation (p. 11): "It seems unlikely that improved mathematics achievement for the treatment group between the second and third years and the lack of mathematics impacts in the third year were simply due to fewer students using an OSP scholarship."

**Reading for the memo:** in the one large, clean, randomized US urban voucher evaluation, moving a child from public to private school produced **significantly worse math scores for two years and no detectable benefit in reading at any horizon**, converging to zero by year 3. This is evidence *against* treating private tuition as buying a measurable academic gain for the switching child.

**Confidence: HIGH** (three primary federal evaluation reports read directly).

---

## 5a. Putnam 2007 and the Abascal & Baldassarri AJS 2015 critique — VERIFIED; the critique is stronger than usually reported

**What Putnam claimed.** [SOURCE: Putnam, "E Pluribus Unum: Diversity and Community in the Twenty-first Century," Scandinavian Political Studies 30(2) 2007: 137–174] — quoted inside Abascal & Baldassarri: residents of diverse neighborhoods "hunker down": "Trust (even of one's own race) is lower, altruism and community cooperation rarer, friends fewer" (p. 137), and "there is a tradeoff between diversity and social capital" (2007, p. 164). Data: Social Capital Community Benchmark Survey (SCCBS), 2000.

**What Abascal & Baldassarri actually found.** [SOURCE: Abascal & Baldassarri, "Love Thy Neighbor? Ethnoracial Diversity and Trust Reexamined," AJS 121(3) 2015: 722–782, DOI 10.1086/683144; OA text at https://iris.unibocconi.it/bitstream/11565/4035040/1/2.AbascalBaldassarri_HeterogeneityTrust_AJS2015.pdf — read via scrape, full sample N = 29,733]

Abstract: "It reproduces the analysis of Putnam and shows that the association between diversity and self-reported trust is **a compositional artifact attributable to residential sorting**: nonwhites report lower trust and are overrepresented in heterogeneous communities. The association between diversity and trust is better explained by differences between communities and their residents in terms of race/ethnicity, residential stability, and economic conditions; **these classic indicators of inequality, not diversity, strongly and consistently predict self-reported trust**... Only for whites does living among out-group members — not in diverse communities per se — negatively predict trust."

The decisive replication result, from the body: "First, consider the predictive power of the heterogeneity index. For the national sample, the conclusion is straightforward: as table 4 shows, **the HHI does not significantly predict any of the five indicators of social capital**. For the full sample (table 5) the HHI is not significant in four out of five models, the only exception being the model predicting trust in neighbors." Footnote 24: "the heterogeneity index does not consistently predict trust toward specific groups, such as whites, blacks, Hispanics, and Asians."

They note Putnam's own reported estimate was thin: "Albeit small, the parameter estimate for tract homogeneity turns out to be statistically significant in this linear regression model" — and that Putnam "only reports results from a multivariate model predicting trust in neighbors among the full sample," i.e. the one of five outcomes that survives.

And the asymmetry: "Among whites, the proportion of in-group members is the most consistently significant predictor of trust... Neither blacks nor Hispanics exhibit a similar in-group effect; for them, trust is not positively related to the concentration of in-group members." Their own interpretation: "the alleged effects of ethnic diversity might be more accurately attributed to bias."

**How this bears on the memo.** A "diversity lowers social capital / lowers willingness to fund public goods" premise cannot rest on Putnam 2007 without addressing that a re-analysis of his own data and measures finds the index null on 5/5 (national) and 4/5 (full) outcomes. The residual finding — whites trust less as their share of out-group neighbors rises — is itself consistent with a native-flight story but locates the mechanism in majority-group response, not in "diversity" as a community property.
**Steel-man of the other side:** Abascal & Baldassarri control for individual race, citizenship, tract white share and tract citizen share; a Putnam defender can argue this is over-controlling, since the mechanism by which diversity acts *is* composition — you cannot condition on the treatment's own components and still call the residual a null. That is a genuine specification dispute, not a settled kill. See also Dinesen, Schaeffer & Sønderskov, Annual Review of Political Science 2020, a narrative + meta-analytical review of the diversity-trust literature [SOURCE: DOI 10.1146/annurev-polisci-052918-020708] — **[UNVERIFIED]**, I did not retrieve its effect sizes.

**Confidence: HIGH on what Abascal & Baldassarri report; MEDIUM on the field's net verdict.**

---

## 5b. Kustov & Pardelli, APSR 112(4) 2018: 1096–1103 — "Ethnoracial Homogeneity and Public Outcomes: The (Non)effects of Diversity" — the identification attack on Alesina-Baqir-Easterly

[SOURCE: DOI 10.1017/S0003055418000308; abstract retrieved from Cambridge Core, IDEAS/RePEc and the APSA summary at politicalsciencenow.com. **I did not retrieve the full text**; quotes below are from the published abstract and the authors' own APSA summary.]

Abstract: "Many studies find support for the hypothesis that diversity is related to inefficient outcomes by comparing diverse and homogeneous communities. We distinguish between homogeneity of dominant and disadvantaged groups and argue that **it is often impossible to identify the effects of diversity due to its collinearity with the share of disadvantaged groups.** To disentangle the effects of these variables, we study new data from Brazilian municipalities. While it is possible to interpret the prima facie negative correlation between diversity and public goods as supportive of the prominent 'deficit' hypothesis, a closer analysis reveals that, in fact, **more homogeneous Afro-descendant communities have lower provision.** While we cannot rule out that diversity is consequential in other contexts, our results cast doubt on the reliability of previous findings related to the benefits of local ethnoracial homogeneity for public outcomes."

The US-specific point, from the authors' APSA summary: "The US, for instance, only has a small number of white-minority localities and, among them, few are racially homogeneous." That is the core problem for any US ELF-based design including ABE: in US data, high fragmentation and high minority share are nearly the same variable, so "diversity reduces public goods" and "minority share reduces public goods" are not separately identified. The Brazilian sample is chosen precisely because it breaks that collinearity — and when it is broken, the sign flips to homogeneity-of-the-disadvantaged, not diversity.

**Confidence: MEDIUM-HIGH** (published APSR abstract verified verbatim from three independent hosts; full-text tables not read).

---

## 5c. Habyarimana, Humphreys, Posner & Weinstein, APSR 101(4) 2007 — mechanism, not existence

PDF retrieved and cached (`_cache/habyarimana_apsr2007.pdf`, 18 pp.) [SOURCE: DOI 10.1017/S0003055407070499; OA copy https://escholarship.org/content/qt2km4r4dn/qt2km4r4dn.pdf]. **[PARTIAL]** — retrieved but not yet quoted here; see "What I could NOT verify."
