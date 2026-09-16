# Crime Rates of Unauthorized Immigrants vs. Native-Born US Citizens — Research Memo

**2026-09-05 scope correction:** Arrest, conviction, incarceration and self-reported offending are different outcomes. Aggregate population comparisons are valid descriptive estimands; neither race restriction nor repeated cohort cross-sections alone identify a causal effect. See [material-inference repair](../decisions/2026-09-05-material-inference-repair.md).

**Question:** What does the empirical evidence say about observed arrest, conviction, and incarceration rates of unauthorized (illegal) immigrants compared to native-born US citizens?
**Tier:** Deep | **Date:** 2026-03-14
**Ground truth:** Multiple papers already in corpus (Light & Miller 2020, Gunadi 2019, Ousey & Kubrin 2018, Nowrasteh/Cato analyses). No prior synthesis memo on this specific topic existed.

**Instrument caveat:** Immigration and crime is a politically charged topic. The LLM instrument has known dispositions on such topics. This memo relies on sourced empirical claims from peer-reviewed studies and official data, not training-data impressions. [SOURCE: `notes/llm-bias-caveat.md`]

---

## Bottom Line

The weight of the evidence consistently finds that unauthorized immigrants have **lower observed arrest, conviction, or incarceration rates** than native-born US citizens in the best current U.S. datasets. That is the right measured estimand. It should not be silently upgraded to directly observed true offending, because reporting, detection, deportation, and denominator problems still matter. The one prominent study claiming the opposite (Lott 2018, Arizona) faces a serious unresolved immigration-status classification critique from researchers across the political spectrum, including the libertarian Cato Institute.

However, this evidence base has real limitations that an honest assessment must name:

1. **Measurement problem:** We cannot directly observe crime rates of a population that is definitionally hard to count. Every study relies on imperfect proxies (arrest records matched to immigration databases, Census-based population denominators, institutionalization rates from ACS). Each proxy introduces its own bias.
2. **Selection effects:** Unauthorized immigrants may underreport victimization and avoid police contact due to deportation fear, which could depress arrest-based crime measures without reflecting true underlying rates.
3. **Heterogeneity:** "Unauthorized immigrants" is not a monolithic group. Crime rates likely vary by country of origin, age at entry, length of residence, and local context. Aggregate comparisons obscure this variation.
4. **The ICE docket numbers** (large absolute counts of noncitizens with criminal records) are real administrative data but measure something different from per-capita crime rates. They are stock figures accumulated over decades, not rates.

The reported unauthorized-versus-all-native arrest and incarceration gaps are descriptive comparisons of different populations. Cato’s separate 2023 incarceration tabulation changes from about 50% lower overall to about 30% lower after excluding Black respondents from both groups; that changes the population being compared and does not correct the Texas arrest result. [SOURCE: https://www.cato.org/sites/cato.org/files/2025-03/Policy-Analysis-994.pdf] [INFERENCE]

---

## Evidence Recitation (before synthesis)

### Study 1: Light, He, & Robey (2020) — PNAS
**"Comparing crime rates between undocumented immigrants, legal immigrants, and native-born US citizens in Texas"**
- **Data:** Texas DPS arrest records matched to DHS databases, 2012-2018. Uniquely comprehensive: Texas is the only state that systematically records immigration status at arrest via DHS cross-referencing.
- **Population denominator:** Center for Migration Studies and Pew annual state-level estimates of undocumented population.
- **Key findings:**
  - Undocumented immigrants had substantially lower felony arrest rates than native-born citizens across all offense categories. [SOURCE: PNAS 117(51), doi:10.1073/pnas.2014704117]
  - US-born citizens were **>2x** more likely to be arrested for violent crimes, **2.5x** for drug crimes, **>4x** for property crimes relative to undocumented immigrants in the aggregate native-born denominator. This does not remove race-composition confounding by itself. [SOURCE: same] [INFERENCE]
  - For specific offenses: undocumented immigrants were roughly **half** as likely to be arrested for homicide, felonious assault, and sexual assault compared to native-born citizens. [SOURCE: same]
  - Gaps for property crimes were larger: native-born citizens 3-5x more likely for robbery, burglary, theft, arson. [SOURCE: same]
  - Trend analysis: proportion of arrests involving undocumented immigrants was stable or decreasing 2012-2018. [SOURCE: same]
  - Results robust to: alternative population estimates, alternate undocumented classification, substituting convictions for arrests, substituting misdemeanors. [SOURCE: same]
- **Limitations:** Texas-specific. Relies on DHS IDENT database matching, which may miss some undocumented individuals or misclassify legal immigrants as native-born. Authors acknowledge this and run sensitivity analyses.
- **N:** ~700,000+ arrest records over 7 years.
- **Citation count:** 56 (S2). Published in PNAS (peer-reviewed, high-impact).

### Study 2: Gunadi (2019) — Journal of Economics, Race, and Policy (now Oxford Economic Papers)
**"On the association between undocumented immigration and crime in the United States"**
- **Data:** ACS institutionalization rates + state-panel crime data with IV approaches.
- **Key findings:**
  - Undocumented immigrants are **33% less likely** to be institutionalized (the study’s incarceration proxy) compared to US natives, despite possessing demographic characteristics usually associated with higher crime (young, male, low-education). [SOURCE: doi, S2 ID 0ab1f84bc263912171bb1b43ac8f3fca05c387f6]
  - No evidence that longer US residence increases institutionalization risk. [SOURCE: same]
  - Arriving at younger age is associated with higher institutionalization rate (consistent with assimilation/acculturation hypothesis). [SOURCE: same]
  - State-panel analysis: property and violent crime rates are **not statistically significantly increased** by undocumented immigration. [SOURCE: same]
Instrumental-variable estimation does not automatically correct differential reporting, outcome mismeasurement or status imputation. Those require separate assumptions or validation. [INFERENCE]
- **Limitations:** ACS institutionalization proxy conflates prisons/jails/mental health facilities (though most are correctional). IV exclusion restriction debatable. State-level panel may be too coarse.
- **Citation count:** 22 (S2).

### Study 3: Ousey & Kubrin (2018) — Annual Review of Criminology
**"Immigration and Crime: Assessing a Contentious Issue"**
- **Data:** Meta-analysis of 51 published studies, 543 effect-size estimates, covering 1994-2014 research on macrosocial (geospatial) units.
- **Key findings:**
  - **Overall weighted mean effect:** r = **-0.031** (95% CI: -0.055 to -0.003, p = 0.032). Negative but very weak — "practically zero." [SOURCE: Ousey & Kubrin 2018 via ask_papers synthesis, doi:10.1146/annurev-criminol-032317-092026]
  - The association is negative on average: higher immigration associated with slightly lower crime.
  - **Significant heterogeneity by study design:**
    - Longitudinal studies: r = **-0.147** (strongest negative effect)
    - Cross-sectional studies: r = **0.000** (null)
    - Small geographic units (tracts/neighborhoods): r = **-0.073**
    - Large geographic units (cities/MSAs): r = **0.004**
    - Traditional immigrant destinations: r = **-0.082**
    - New destinations: r = **+0.028** (slight positive, non-significant)
    - Homicide specifically: r = **-0.058**
    - Property crime: r = **0.006** (essentially null)
  - Authors conclude: the link is contingent on study characteristics. Longitudinal designs (more robust) show stronger negative association. [SOURCE: same]
- **Limitations:** Meta-analysis covers immigration broadly (not unauthorized-specific). Macrosocial units only — cannot speak to individual-level offending. Publication bias tests suggest this is not a major concern in this literature.
- **Citation count:** 303 (S2). Gold-standard venue for criminology reviews.

### Study 4: Nowrasteh / Cato Institute — Texas conviction data
**Multiple reports using Texas DPS data, 2012-2018+**
- **Key findings:**
  - Illegal immigrants in Texas had **lower conviction rates** than native-born citizens for homicide, sexual assault, and larceny. [SOURCE: https://www.cato.org/publications/immigration-research-policy-brief/criminal-immigrants-texas-illegal-immigrant, verified via Exa]
  - Homicide conviction rate for illegal immigrants approximately **26% lower** than native-born. [SOURCE: same]
  - Published detailed rebuttals of CIS counter-analyses using the same Texas data. [SOURCE: https://www.cato.org/blog/center-immigration-studies-still-wrong-about-illegal-immigrant-crime-texas]
- **Source quality:** Cato is a libertarian think tank (pro-immigration on policy grounds). However, the underlying data (Texas DPS) is the same administrative dataset used by Light & Miller's peer-reviewed PNAS study, and the findings are directionally consistent. Grade: [C2] — fairly reliable source, probably true given convergence with peer-reviewed work.

### Study 5: Butcher & Piehl (1998) — Industrial & Labor Relations Review
**"Recent Immigrants: Unexpected Implications for Crime and Incarceration"**
- Early influential study establishing that recent immigrants have lower incarceration rates than natives.
- **Citation count:** 198 (S2). Foundational paper in this literature.
- Used Census data on institutionalization.

### Study 6: Rumbaut (2008)
**"Undocumented Immigration and Rates of Crime and Imprisonment: Popular Myths and Empirical Realities"**
- Review documenting that incarceration rates for young men born in Mexico, El Salvador, and Guatemala are dramatically lower than for native-born young men, despite those groups being predominantly unauthorized.
- **Citation count:** 51 (S2).

---

## The Contrarian Case: Lott (2018)

### Lott's Arizona study
John R. Lott Jr. published "Undocumented Immigrants, U.S. Citizens, and Convicted Criminals in Arizona" (SSRN, 2018), claiming that undocumented immigrants in Arizona had higher incarceration rates than native-born citizens.

**Critical assessment:**

The study has been criticized for a **serious possible immigration-status classification problem:**

1. **Cato Institute critique (Nowrasteh):** The Arizona data Lott used does not reliably distinguish illegal immigrants from legal immigrants or naturalized citizens. The database flags were unreliable, leading to systematic misclassification. [SOURCE: https://www.cato.org/blog/fatal-flaw-john-r-lott-jrs-study-illegal-immigrant-crime-arizona]

2. **Washington Post fact-check:** Raised serious questions about the methodology, noting that the coding of immigration status in Arizona prison records was inconsistent and unreliable. [SOURCE: https://www.washingtonpost.com/news/fact-checker/wp/2018/03/21/questions-raised-about-a-study-that-links-undocumented-immigrants-to-higher-crime, verified via Exa]

3. **Latino Decisions critique:** Documented specific concerns with how the Arizona DOC data classified immigration status. [SOURCE: https://latinodecisions.com/blog/my-concerns-with-john-lotts-arizona-study, verified via Exa]

4. **Not peer-reviewed:** Published as SSRN working paper, not in a peer-reviewed journal.

5. **Author context:** Lott has a history of controversial methodological claims (the "More Guns, Less Crime" debate) and has faced criticism of his research practices in other domains.

**Assessment:** [D4] — not usually reliable source (advocacy-adjacent), doubtful information given that the specific data classification it depends on has been seriously challenged by multiple independent critics. This study is an outlier in the literature and its central data problem has not been resolved.

---

## The ICE Docket Numbers (frequently cited in political debate)

In September 2024, ICE ERO data released to Congress showed large absolute numbers of noncitizens with criminal records on ICE's national docket, split into detained and non-detained columns. The table totals include ~15,000 with homicide convictions or pending charges and ~20,000 with sexual assault convictions or charges. [SOURCE: https://homeland.house.gov/wp-content/uploads/2024/09/24-01143-ICEs-Signed-Response-to-Representative-Tony-Gonzales.pdf, verified via Exa]

**Why these numbers do not contradict the per-capita findings:**

1. **Stock vs. rate:** These are cumulative docket counts, not annual crime rates. They also describe **noncitizens on ICE's national docket**, not an unauthorized-only population. Dividing this numerator by the ~11 million unauthorized immigrant stock is therefore a denominator error; the valid conclusion is narrower: the ICE counts do not by themselves provide a per-capita native comparison or overturn the rate-based studies above. [SOURCE: same document] [INFERENCE]

2. **"Convictions or pending charges":** Convictions and pending charges are distinct outcomes. A clearly labeled sum can be an administrative count, but it cannot be described as a count of convicted offenders. [SOURCE: same ICE letter]

3. **ICE non-detained is an agency custody classification:** It does not by itself establish that everyone counted is currently free in the United States. This memo has not verified the earlier claim that this table includes deceased or already-deported people; that claim is withdrawn. The essential denominator mismatch does not depend on it. [UNVERIFIED specific composition; INFERENCE about the estimand]

4. **CNN investigation (2025):** Found that less than 10% of individuals taken into ICE custody in recent months had serious criminal convictions. [SOURCE: https://us.cnn.com/2025/06/16/us/la-ice-raids-violent-criminals-records-invs, verified via Exa]

5. **Recent reporting:** "Immigrants with no criminal record now largest group in ICE detention." [SOURCE: The Guardian, verified via Exa]

**Assessment:** The absolute numbers are real administrative data [A3], but their use to argue that unauthorized immigrants have high crime rates involves a rate-base fallacy. The numbers measure something different from what the peer-reviewed literature measures.

---

## Key Methodological Challenges (applying to ALL studies)

### 1. Denominator problem
No census perfectly counts unauthorized immigrants. Population estimates from CMS and Pew have uncertainty bands. Holding the arrest numerator and immigration-status classification fixed, a larger true unauthorized denominator mechanically lowers the calculated rate, while a smaller denominator raises it. That denominator-only sensitivity should not be confused with numerator or classification uncertainty. Light & Miller (2020) test sensitivity to alternative population estimates and find results robust. [SOURCE: PNAS 117(51)]

### 2. Reporting / detection bias
Unauthorized immigrants may avoid police contact, leading to:
- **Lower arrest rates** (fewer crimes detected, not fewer crimes committed)
- **Lower victimization reporting** (fear of deportation suppresses calls to police)

Instrumental-variable estimation does not automatically correct differential reporting, outcome mismeasurement or status imputation. Those require separate assumptions or validation. [INFERENCE]

### 3. Selection effects
People who undertake the costs and risks of unauthorized migration may be systematically different from both the sending-country population and native-born Americans. The "immigrant selectivity" hypothesis suggests migrants are positively selected on motivation, risk-aversion regarding criminal justice contact, and work orientation. This is a plausible mechanism but hard to test directly. [INFERENCE from theory in Ousey & Kubrin 2018]

### 4. Deportation as censoring
Deportation can change the observed risk set and later recorded events. Removal, re-entry, new arrivals and denominator timing determine its influence; a flat or rising series does not rule out censoring. [INFERENCE]

### 5. Population composition and the comparison being estimated

The all-native comparison describes the actual native-born population. It need not equal a comparison standardized to a common race, age, sex or geographic distribution. Choosing one of those estimands requires stating the question; a different population composition does not make the aggregate descriptive rate mathematically inflated. [INFERENCE]

**What happens when the comparison population is restricted:**

Landgrave & Nowrasteh (Cato Policy Analysis 994, April 2025) provide the race-stratified data:

| Group | Incarceration rate per 100k (2023) |
|-------|-----------------------------------|
| Native-born (all) | **1,221** |
| Native-born (excluding Black) | **891** |
| Illegal immigrants (all) | **613** |
| Illegal immigrants (excluding Black) | **626** |
| Legal immigrants | **319** |

[SOURCE: https://www.cato.org/sites/cato.org/files/2025-03/Policy-Analysis-994.pdf]

- **All-population comparison:** illegal immigrants ~50% less likely to be incarcerated than native-born
- **Excluding Black Americans from both groups:** gap narrows to ~30% less likely [SOURCE: https://www.alexnowrasteh.com/p/immigrants-have-a-lower-incarceration — Nowrasteh Apr 2025]
- **Within each racial/ethnic group:** immigrants have lower incarceration rates than their native-born counterparts. Hispanic immigrants < native-born Hispanics. Black immigrants < native-born Blacks. White immigrants < native-born whites. [SOURCE: same]

**Assessment:** Using the displayed rates, `1 − 613/1,221 = 49.8%` and `1 − 626/891 = 29.7%`. The 20.1 percentage-point change is a difference between two descriptive estimands, not a measured 20-point bias. Excluding Black respondents from both populations does not make their remaining race distributions identical, and it does not adjust age, sex, geography, detection or status classification. Within-race comparisons address that dimension only. The earlier endorsement of a “corrected” native comparator was unjustified. [SOURCE: Cato PA 994; INFERENCE; recalculated]

**Scope of Light, He & Robey (2020):** Their aggregate Texas status-group arrest comparison is not a demographic-standardized estimate or a causal effect of immigration status. The Cato national incarceration restriction above cannot supply such an adjustment to this different dataset/outcome. [SOURCE: https://doi.org/10.1073/pnas.2014704117] [INFERENCE]

### 6. Generational assimilation
The cited immigration-crime literature reports a broad generational-assimilation pattern: second-generation outcomes often move toward native-born rates rather than preserving first-generation lows. Treat this as a scope-limited caveat, not as an unauthorized-only estimate or a post-2020-surge claim. [SOURCE: Bersani, https://doi.org/10.1080/07418825.2012.659200; review context in NIJ 310356] [INFERENCE]

---

## International Context

The US finding (lower observed criminal-justice rates for first-generation / unauthorized immigrants) does **not** generalize internationally without qualification.

**European evidence is more mixed:**
- Saved but not fully analyzed: Skardhamar et al. (2014) on immigrant crime in Norway and Finland finds higher crime rates among some immigrant groups. [SOURCE: S2 ID 54b2f4ed7f408d6bb823617ec9c2d7cb82e11f6e]
- Olivier Marie & Paolo Pinotti (2024, JEP) — "Immigration and Crime: An International Perspective" documents that the relationship varies substantially by country, immigration policy regime, and immigrant composition. [SOURCE: S2 ID 1f48d32d03bf156d871a2632e516e9064b28b750]
- Key difference: European immigration includes large refugee/asylum populations with different selection mechanisms than US labor migration. The positive selection hypothesis that explains low US immigrant crime may not apply to populations selected by conflict displacement rather than labor market opportunity. [INFERENCE]

### European registry rates, pulled from the official APIs 2026-09-16

Reproducible pull (scripts, tidy CSV, validations): `infra/immigration-fiscal/registry_crime_2026_09_16/`. Raw API responses remain in the session scratch until `sources/` (SSD) is mounted. Norway publishes no open table crossing charged persons with immigration category (search of the SSB API, HTTP 200 throughout); Sweden's figures are report-only (Brå 2021:9).

**Denmark 2025, ages 15–79, persons found guilty of any offence (penal code, traffic act and special legislation together), per 100,000 of the same group.** Numerator STRAFNA9, denominator FOLK1E, both Statistics Denmark. Index is direct age standardization on the three published bands (15–29, 30–49, 50–79) with all persons of the same sex = 100; it is not DST's indirect index and the coarse bands leave within-band age differences unadjusted, which pushes the descendant index up. [SOURCE: api.statbank.dk, tables STRAFNA9 and FOLK1E; CALCULATION]

| Group | Men per 100k | Men index | Both sexes per 100k | Both index |
|---|---:|---:|---:|---:|
| Persons of Danish origin | 4,522 | 90 | 3,018 | 91 |
| Immigrants, Western | 4,767 | 88 | 3,295 | 92 |
| Immigrants, non-Western | 7,671 | 145 | 4,688 | 134 |
| Descendants, Western | 6,412 | 113 | 4,489 | 121 |
| Descendants, non-Western | 16,722 | 321 | 10,866 | 315 |
| All persons | 5,092 | 100 | 3,364 | 100 |

Men 2025 counts over population: Danish origin 88,304 / 1,952,683; non-Western immigrants 14,999 / 195,521; non-Western descendants 9,308 / 55,663. The published age total (120,166) equals the sum of the three bands. For penal-code offences only, the Danish Justice Ministry's 2023 fact sheet gives age-standardized indices of 262 for non-Western descendants and 88 for Danish origin (men), so the ordering is the same under the narrower scope. [SOURCE: as above; [Justice Ministry 2023](https://www.justitsministeriet.dk/wp-content/uploads/2025/05/Kriminalitet-og-herkomst-2023-WT.pdf)]

**Netherlands 2025 (provisional; CBS states provisional years understate the final count by a few percent), registered suspects per 10,000 residents of the group, not age-standardized.** Table 85658NED, CBS StatLine. Rates are published as integers; population is back-derived from count and rate. [SOURCE: opendata.cbs.nl/ODataApi/odata/85658NED]

| Group | Men | Both sexes |
|---|---:|---:|
| Born in NL, both parents born in NL | 83 | 50 |
| Born in NL, one parent born abroad | 178 | 108 |
| Born in NL, both parents born abroad | 453 | 265 |
| Born outside the Netherlands | 184 | 104 |
| Origin Morocco (all generations) | 473 | 265 |
| Origin Dutch Caribbean | 519 | 306 |
| Origin Türkiye | 241 | 140 |
| Origin Indonesia | 58 | 35 |
| All | 124 | 73 |

The second generation is much younger than the Dutch-origin population, so the 5.5× male ratio here is not age-adjusted; CBS's own age-restricted comparison (12–25) gives 3.4% versus 1.2%. These are descriptive registry rates: exact for their definitions, not causal, and not evidence about the United States. [INFERENCE: age caveat]

---

## Claims Table

| # | Claim | Evidence | Confidence | Source | Status |
|---|-------|----------|------------|--------|--------|
| 1 | Undocumented immigrants in Texas had substantially lower felony arrest rates than native-born citizens (2012-2018) | Administrative arrest data, PNAS peer review | HIGH | Light et al. 2020, PNAS 117(51) | VERIFIED |
| 2 | US-born citizens >2x more likely to be arrested for violent crimes than undocumented immigrants in Texas | Same dataset; aggregate native-born denominator, not standardized to a common demographic distribution | HIGH | Light et al. 2020 | DESCRIPTIVE AGGREGATE COMPARISON |
| 3 | Undocumented immigrants 33% less likely to be institutionalized than US natives nationally | ACS data + IV | MODERATE | Gunadi 2019 | VERIFIED |
| 4 | Meta-analytic average association of immigration with crime: r = -0.031 (negative, very weak) | 51 studies, 543 effect sizes | HIGH | Ousey & Kubrin 2018 | VERIFIED |
| 5 | Longitudinal studies show stronger negative association (r = -0.147) than cross-sectional (r = 0.000) | Moderator analysis within meta-analysis | HIGH | Ousey & Kubrin 2018 | VERIFIED |
| 6 | Lott's Arizona study claiming higher rates faces a serious unresolved immigration-status classification critique | Multiple independent critiques (Cato, WaPo, Latino Decisions); no independent reanalysis in this memo | MODERATE-HIGH | Nowrasteh 2022; WaPo 2018 | SUPPORTED CRITIQUE — not independent reanalysis |
| 7 | ICE national docket shows ~15K noncitizens with homicide convictions/charges | Official ICE data released to Congress | HIGH (as administrative count) | ICE ERO letter, Sept 2024 | VERIFIED — but measures stock, not rate |
| 8 | European registry data (origin-based, second generation visible) show foreign-born and especially second-generation suspect/conviction rates above native-origin: Sweden RR 2.5 and 3.2 (1.8 and 1.7 adjusted); Denmark non-Western descendants index 262 (2023, age-standardized); Netherlands 2.8% vs 0.6% suspects (2023) | National registry tables read directly | HIGH (descriptive, registry) | Brå 2021:9; Danish Justice Ministry 2023 fact sheet; CBS Integratie en samenleven 2024 | VERIFIED — see `immigration-crime-statistics-bias-mechanisms-2026-09-16.md` for exposure-denominator and events-vs-persons caveats |
| 9 | Second-generation offending is higher than adult-arrival first-generation offending and converges to, not above, native-born levels in US individual-level data; the gap is a first-generation (adult-arrival) floor | Within-family dyads (NLSY79/CYA), NLSY97 survival analysis, 1900–1930 census with parental birthplace; survey-based, single cohorts; not unauthorized-only or post-2020-surge evidence | MODERATE | Bersani & Pittman 2019, DOI 10.1177/0022427819850600; Inkpen 2024, DOI 10.1177/00111287231225125; Moehling & Piehl NBER w19083; Bersani (2014), DOI 10.1080/07418825.2012.659200 | SUPPORTED — see `immigration-generational-crime-mechanisms-2026-09-16.md`; European second-generation excess over natives is claim 8, not this row |
| 10 | Reporting bias (fear of deportation suppressing police contact) could partially explain lower observed rates | Theoretical + indirect evidence | MODERATE | Gunadi 2019; general literature | INFERENCE |

---

## What's Uncertain

1. **Magnitude precision:** We know the direction for observed justice-system rates with high confidence, but the exact ratio varies by study, crime type, time period, and geography. "2x lower" vs "50% lower" vs "33% lower" depends on the specific comparison.

2. **Causal mechanism:** Is it positive selection (migrants are unusually motivated/law-abiding), deterrence (fear of deportation), underreporting, deportation-as-censoring, or some combination? The literature has not cleanly identified the mechanism. [INFERENCE]

3. **Post-2020 surge population:** Most rigorous studies cover 2012-2018. Whether the findings generalize to the 2021-2024 immigration surge population (different composition, different entry conditions) is genuinely unknown. [UNVERIFIED]

4. **Crime type heterogeneity:** The strongest evidence is for violent crime and property crime. Evidence on immigration-specific offenses, DUI, and domestic violence is thinner.

5. **Subpopulation variation:** Aggregate "unauthorized immigrant" rates may mask important variation by nationality, age at entry, gang affiliation status, etc.

---

## Search Log

| Query/Action | Tool | Result |
|---|---|---|
| Check corpus | list_corpus | 6 immigration-related papers found |
| Read Light et al. 2020 full text | read_paper | Key findings extracted |
| Read Gunadi 2019 full text | read_paper | Key findings extracted |
| Read Ousey & Kubrin 2018 full text | read_paper | Meta-analytic effect sizes extracted |
| Synthesize meta-analysis numbers | ask_papers | Detailed moderator analysis retrieved |
| Verify claim: studies finding higher rates | verify_claim (Exa) | No peer-reviewed higher-rate study found in this pass; Lott Arizona remained the prominent non-peer-reviewed outlier |
| Search: Lott Arizona criticism | web_search_exa + verify_claim | Multiple critiques documented |
| Verify: ICE docket numbers | verify_claim (Exa) | Confirmed as administrative data |
| Verify: Cato/Nowrasteh Texas findings | verify_claim (Exa) | Confirmed, consistent with Light et al. |
| Search S2: undocumented crime incarceration | search_papers | Additional papers identified |
| Fetch Skardhamar et al. 2014 | fetch_paper | Downloaded, not fully analyzed |

---

## Sources Saved to Corpus

- Light, He, & Robey (2020) — `5928780a39cc9fea27a3427432efecf5c21c85e2` [previously saved]
- Gunadi (2019) — `0ab1f84bc263912171bb1b43ac8f3fca05c387f6` [previously saved]
- Ousey & Kubrin (2018) — `33034e4c0080fa686d177bb0e4f52afe7914c852` [previously saved]
- Skardhamar et al. (2014) — `54b2f4ed7f408d6bb823617ec9c2d7cb82e11f6e` [fetched this session]
- Marie & Pinotti (2024; earlier corpus author attribution corrected) — `1f48d32d03bf156d871a2632e516e9064b28b750` [previously saved]

## Sources Not in Corpus (web-sourced)

- Landgrave & Nowrasteh (2025) "Illegal Immigrant Incarceration Rates, 2010–2023" — Cato Policy Analysis 994. [SOURCE: https://www.cato.org/sites/cato.org/files/2025-03/Policy-Analysis-994.pdf] **Race-stratified incarceration data.**
- Nowrasteh (Apr 2025) blog post with population-restricted comparison tables. [SOURCE: https://www.alexnowrasteh.com/p/immigrants-have-a-lower-incarceration]
- Nowrasteh & Chanwong (Sep 2025), "Immigrants Have Lower Lifetime Incarceration Rates": compares a 1990 arrival cohort across subsequent ACS cross-sections, not the same individuals followed through life. Age, selective exit and changing cohort composition remain relevant; these are incarceration-prevalence snapshots, not cumulative lifetime offending probabilities. [SOURCE: https://www.cato.org/blog/immigrants-have-lower-lifetime-incarceration-rates-native-born-americans] [INFERENCE]

**Generational comparator identity [INFERENCE]:** If `a` is the second-generation share of the native-born population, `r_native = a·r_2 + (1−a)·r_3+`. Evidence that `r_2 > r_1` does not imply `r_2 > r_3+`. Thus second-generation convergence toward other natives does not establish that including the second generation inflates the native benchmark. The Ousey–Kubrin area-level meta-analysis does not itself identify an individual generational effect.

## Revisions

| Date | Change |
|------|--------|
| 2026-06-16 | Scoped race correction to incarceration magnitude, made denominator sensitivity conditional on fixed numerator/classification, and narrowed within-race comparison from "eliminates confound entirely" to removing the racial-composition confound. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Bounded the search-log wording for higher-rate studies: the Exa pass did not find a peer-reviewed higher-rate study, but that is a search-result statement, not a proof of absence across the literature. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Downgraded the European mixed-evidence table row from `VERIFIED (direction), not fully analyzed` to `PRELIMINARY`; fetched-but-unread evidence should not carry a verified status. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Reframed the Lott Arizona critique row from `HIGH/VERIFIED` fundamental flaw to a supported unresolved classification critique, because the memo cites critiques rather than running an independent data reanalysis. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Downgraded the second-generation crime row from `HIGH/VERIFIED` to a scope-limited supported literature pattern; the cited evidence is broad generational literature, not unauthorized-only or current-surge evidence. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Aligned the bottom-line and contrarian-case Lott wording with the claims table: serious unresolved classification critique, not independently verified fundamental error. Added a race-composition caveat to the aggregate Texas `>2x` violent-arrest row. |

- **2026-09-05 — Corrected comparator, observation and generational inference** See [material-inference repair](../decisions/2026-09-05-material-inference-repair.md). Historical revision entries above describe the earlier state, including conclusions superseded here.

- **2026-09-16 — European row upgraded from PRELIMINARY to VERIFIED on primary registry tables; measurement mechanisms catalogued.** Claim 8 now cites Brå 2021:9, the Danish Justice Ministry 2023 fact sheet and CBS 2024 read this session. The methodological-challenges section is extended by [crime-statistics bias mechanisms](immigration-crime-statistics-bias-mechanisms-2026-09-16.md): Texas status-identification timing deflates, European exposure denominators and federal immigration offences inflate. No causal claim changes.

- **2026-09-16 — Added Danish and Dutch registry rates pulled from the official APIs.** Exact 2025 conviction (DK, all offences) and suspect (NL, provisional) rates by origin and generation, with scope and standardization caveats; scripts and CSV under `infra/immigration-fiscal/registry_crime_2026_09_16/`. Confidence for claim 8 is unchanged (HIGH, descriptive).

- **2026-09-16 — Claim 9 restated as a first-generation floor.** Within-family (Bersani & Pittman 2019), survival (Inkpen 2024) and 1900–1930 parental-birthplace census (Moehling & Piehl) designs show the generational gap is produced by exceptionally low adult-arrival offending, with the US second generation at native-born levels rather than above them; confidence stays MODERATE (survey-based, single cohorts). Mechanism evidence and the European register picture, where the second-generation excess is partly age structure and partly a legal-status effect that jus soli countries cannot have, are in [generational crime mechanisms](immigration-generational-crime-mechanisms-2026-09-16.md).
