claude-opus-5-5

# Natural experiments: group composition → trust, defensive spending/labor, time use (2026-10-21)

Status: complete 2026-10-21. [SOURCE] per entry; [UNVERIFIED] marks items read from abstracts or secondary text only. Fork of the defensive-spending lane, Plan change 1.

Bar (from RESULT.md Plan change 1): (a) policy-assigned or as-good-as-random change in a place's
group composition, (b) a stated first stage, (c) a measured outcome in {trust, defensive spending or
defensive/guard labor, time use}. Tags: [SOURCE: url] per item; [UNVERIFIED] = secondary only.

## Entries

### 1. Dinesen & Sønderskov (2015), ASR 80(3):550–573, doi:10.1177/0003122415577989
[SOURCE: preprint https://curis.ku.dk/ws/files/130251172/Dinesen_S_nderskov_Ethnic_Diversity_and_Social_Trust_Forthcoming_ASR.pdf]
- Design: Danish ESS rounds 1–5 (2002–11) linked to the national registers. Each respondent gets
  the share of immigrants within 80 m (up to 2,500 m), with individual and contextual controls.
  The variation is **observational residential exposure, not assigned**. There is no first stage;
  it rests on selection on observables.
- Outcome: social trust, 3-item 0–10 scale. Quoted: "The predicted level of trust is, ceteris
  paribus, roughly 0.30 point lower among individuals living in a micro-context with 50 percent
  immigrants or non-Western immigrants than among individuals living in a context with no
  immigrants ... a one standard deviation increase in ethnic diversity leads to a predicted
  reduction in trust of 0.06 points". The national 6-pp rise in immigrant share from 1980 to 2010
  implies "only 0.04". The effect "vanishes in larger contextual units" (past 180–250 m).
- **Clears the bar? No.** Trust is the right outcome, but composition is self-selected residence.
  The register exposure is precise but not exogenous. Parent memory: the 2020 Annual Review
  meta-analysis (Dinesen, Schaeffer & Sønderskov, doi:10.1146/annurev-polisci-052918-020708)
  pools to partial r = −0.0256 (SE 0.0044), mostly observational studies.

### 2. Dustmann, Vasiljeva & Damm (2019), REStud 86(5):2035–2091, doi:10.1093/restud/rdy047
[SOURCE: https://doi.org/10.1093/restud/rdy047, abstract and introduction via Exa]
- Design: Danish refugee dispersal 1986–98 across 275 municipalities. Quoted: "municipalities
  could not influence the allocation process. Neither could they choose the timing ... or the
  number of refugees". The variation is quasi-random in timing and number. The first stage is
  the assigned refugee share.
- Outcome: **vote shares only.** Quoted: "a one percentage point increase in the refugee share ...
  increases the vote share for anti-immigration parties by 1.34 in parliamentary and 2.32
  percentage points in municipal elections" in non-urban municipalities. In the largest 5% the
  sign is "if anything" opposite.
- **Clears the bar? Design yes, outcome no.** It measures no trust, defensive spending or time
  use. Voting is an attitude signal, not one of the three outcomes.

### 3. Couttenier, Petrencu, Rohner & Thoenig (2019), AER 109(12):4378–4425, doi:10.1257/aer.20170263
(The brief cites it as REStat 2019; it is AER.) [SOURCE: https://doi.org/10.1257/aer.20170263; online appendix https://www.aeaweb.org/content/file?id=11063]
- Design: Swiss asylum seekers (N permit) "exogenously allocated to cantons ... by a random
  allocation key based on the cantonal population". Identification comes from childhood
  conflict-exposure cohorts × nationality, using crimes by perpetrator and victim nationality,
  2009–16.
- Outcome: **crime by the migrants.** Quoted: "cohorts exposed to civil conflict/mass killing
  during childhood are 35 percent more prone to violent crime than the average cohort ...
  mostly confined to co-nationals" (114% premium toward co-nationals, 41% toward Swiss natives).
  "Offering labor market access to asylum seekers eliminates two-thirds of the effect"; the
  authors say the cantonal-policy part "cannot go much beyond correlations".
- **Clears the bar? No.** The allocation is assigned, but the paper estimates which migrants
  offend, not how natives' trust, security spending or time use respond to the composition change.

### 4. Albarosa & Elsner (2022), "Forced Migration, Social Cohesion and Conflict: The 2015 Refugee Inflow in Germany", World Bank Policy Research WP 9913, doi:10.1596/1813-9450-9913
[SOURCE: https://documents1.worldbank.org/curated/en/830181643248457941/pdf/Forced-Migration-Social-Cohesion-and-Conflict-The-2015-Refugee-Inflow-in-Germany.pdf, read in full via pdftotext; Table D.3 cells below]
- Design: SOEP natives, individual and year fixed effects. Treatment is the county's percentage
  change in asylum seekers 2014–16 × post-2015, clustered by county. Asylum seekers are assigned
  to states by the Königstein key (population and tax revenue of prior years). Within states,
  "many states deviated from their policy ... and often assigned them based on the availability
  of suitable buildings", and "asylum seekers cannot choose their initial place of residence".
  Parallel-trend checks use the 2003 and 2008 waves (a few pre-trends in "helpful" and "fair").
- First stage: none needed. The treatment is the measured inflow, and its exogeneity is argued
  from the assignment rule. It is not an IV.
- Outcome cells, effect of a doubling of a county's asylum seekers on the probability of agreeing
  (Table D.3, col. 1):
  - "People can be trusted" **.00 (.01)** (mean .67, N 18,704);
  - "People are helpful" .00 (.01);
  - "People are fair" .01 (.01);
  - "Caution towards foreigners" **.019 (.00)**, significant;
  - "Worry about crime" .01 (.01);
  - "Donations" −.01 (.00).
  - Per-capita treatment (col. 6): trust .65 (1.29), not significant.
  - Anti-immigrant violence rose for about two years, concentrated in the top 10% of inflow
    municipalities.
- **Clears the bar? Yes for trust**: policy-assigned composition change, measured generalised
  trust and worry about crime. **Finding: a precise null on trust**, a small rise in caution
  toward foreigners, no change in crime worry. Short run (to about 2018) only.

### 5. Tang, W., "Immigration and Generalised Trust: Evidence from the European Refugee Crisis in Germany", Warwick Economics student paper (wrkesp 90)
[SOURCE: https://ideas.repec.org/p/wrk/wrkesp/90.html, abstract only] [UNVERIFIED: not read; not peer-reviewed]
- Design: quasi-random allocation across federal states, TWFE and DiD. Quoted: "Across both
  models, I find no evidence of a causal effect of immigration exposure on trust."
- **Clears the bar? Design yes, weight low** (student paper, state-level variation only). It
  agrees with entry 4.

### 6. Kim, S. H. & Kim, B.-Y. (2020), "Migration and trust: Evidence from West Germany after unification", JEBO 179:425–441, doi:10.1016/j.jebo.2020.09.014
[SOURCE: https://doi.org/10.1016/j.jebo.2020.09.014, ScienceDirect abstract and method excerpt] [UNVERIFIED: coefficient table not read]
- Design: SOEP trust waves 2003, 2008 and 2013, regressed on "the average net migration rate of
  the respondent's state in 1990 to 1991". Unification is treated as exogenous, but East Germans
  chose their destination states. The variation is 10–11 West German states, with no assignment
  and no first stage.
- Finding (abstract): "West Germans' trust is negatively correlated with migration", persisting
  only for those then in the labour force.
- **Clears the bar? No.** Composition is self-selected and the variation is state-level. The
  authors themselves say "correlated".

### 7. Lange & Sommerfeld (2024), Labour Economics 86:102466, doi:10.1016/j.labeco.2023.102466; Gehrsitz & Ungerer (2022), Economica, ZEW DP 16-086 [SOURCE: https://www.zew.de/fileadmin/FTP/dp/dp16086.pdf]
- Design: German dispersal. Lange–Sommerfeld instrument actual inflows with ex-ante allocation
  quotas. Gehrsitz–Ungerer use the "scramble for accommodation" assignment to counties.
- Outcomes: **crime, employment and votes.** Lange–Sommerfeld: crime unaffected in the arrival
  year, then "approximately two cases per 100,000 residents for every three incoming refugees per
  100,000"; elasticities 0.09 (property) and 0.16 (violent); "some indication of over-reporting".
  Sommerfeld's IZA version notes that police spending "is not available on the district level".
- **Clears the bar? Design yes, outcome no.** Neither measures trust, defensive spending or time
  use. Gehrsitz–Ungerer speculate that native unemployment fell partly through "demand for
  services related to refugee housing ... such as security", but do not measure it.

### 8. Bove, Elia & Ferraresi (2021/2023), JLEO 39(1):235–280, doi:10.1093/jleo/ewab021 (also `sources_literature.md` §E)
- Design: 7,000+ Italian municipalities 2003–15. A shift-share instrument on EU-enlargement inflows,
  with a Fascist-era historical-migration instrument as a check; an IV with a first stage, not
  policy assignment.
- Outcome: **public spending on security (budget share).** Quoted: "the amount of spending
  allocated to local security increases by 0.12-0.30 percentage points for one point increase in
  the share of immigrants ... municipalities spend on average about 4.3% of their budget on
  security". The effect is larger for culturally distant origins. The mechanism runs through fear:
  "immigration is associated to fear of future crimes rather than the actual probability of being
  victim of a crime". Trust: "immigration from culturally distant societies corresponds to a
  deterioration in civic cooperation and interpersonal trust" (that trust result's design not
  verified).
- **Clears the bar? Yes, on defensive spending, as a shift-share IV.** This is weaker than random
  assignment: shift-share exogeneity rests on the shares or the shocks. **Finding: positive.**
  Scaled, a 1-pp rise in immigrant share raises security's budget share by 3–7% of its mean
  [CALCULATION: 0.12/4.3, 0.30/4.3]. Municipal budgets are small and Italian local police are a
  minor share of policing, so this does not transfer to US dollars.

### 9. Ajzenman, Dominguez & Undurraga (2023), "Immigration, Crime, and Crime (Mis)Perceptions", AEJ: Applied 15(4), doi:10.1257/app.20210156
[SOURCE: WP version Oct 2021, https://www.ajzenman.com/wp-content/uploads/2021/11/ADU_Immigration_Perceptions-1.pdf, read via pdftotext, Tables IX–X; published abstract https://doi.org/10.1257/app.20210156] [UNVERIFIED: published-version cells may differ]
- Design: Chile 2008–17, as the foreign-born share roughly tripled. A Bianchi–Buonanno–Pinotti
  shift-share instrument: origin-country push from bilateral flows to destinations other than
  Chile, × 2008 municipal settlement shares. A 2SLS long difference over **101 municipalities**
  with ENUSC victimisation survey outcomes; TWFE as a check.
- First stage: 6.81 (1.64), **F 17.35**, partial R² 0.10.
- Outcomes, Table IX, 2SLS on Δ log immigrant share (0–100 scale):
  - **investment in home security index 10.03 (4.70)**, mean 22.78;
  - **neighbours' security system index (e.g. hiring a block guard) 12.44 (4.06)**, mean 13.16;
  - owns a weapon 0.92 (1.62);
  - summary index 11.44 (4.04), mean 16.41.
  - The FWER (Holm) correction holds. The paper reads these as "doubling the share of the
    population of immigrant background" (2% → 4%).
- Victimisation, Table X, 2SLS: total 3.50 (5.21), mean 21.46; burglary 1.13 (1.83); robbery
  3.09 (2.10). All are insignificant, and the homicide effect is null. Crime concern rises
  (+19 pp on "crime first or second concern"). The effect is larger with low-education immigrants
  and in high-media municipalities.
- **Clears the bar? Yes, on defensive spending and labor**: shift-share IV with a reported first
  stage, and private precaution and block-guard hiring measured directly.
- **Finding: positive and large on precautions, with no change in measured crime.** That is
  defensive spending driven by perception. Caveats:
  - n = 101 and a shift-share design whose exogeneity rests on initial shares;
  - outcomes are binary adoption indices, with no peso amounts and no time use;
  - the inflow was Venezuelan, Haitian, Peruvian and Colombian, so transfer to the US is unclear.

### 10. Hangartner, Dinas, Marbach, Matakos & Xefteris (2019), APSR 113(2):442–455, doi:10.1017/S0003055418000813
[SOURCE: https://doi.org/10.1017/s0003055418000813, Cambridge Core text via Exa]
- Design: Aegean islands; distance to the Turkish coast instruments exposure to refugee arrivals
  (refugees passed through). 2,070 island residents surveyed.
- Outcomes: hostility and policy preferences. Quoted: "an increase of about 0.24 SD in their
  hostility toward asylum seekers (p < 0.001) ... 0.23 SD ... toward immigrants (p = 0.001), and
  0.13 SD ... toward Muslims (p = 0.041) ... increases anti-refugee political engagement by
  0.33 SD". Belief that asylum seekers commit crimes +0.14 (p = 0.102). No generalised trust, no
  security spending, no time use.
- **Clears the bar? Design yes, outcome no.** The design is as-good-as-random. The outcomes are
  out-group attitudes, not one of the three.

### 11. Mariel boatlift: Card (1990), ILRR 43(2):245–257, doi:10.2307/2523702; Billy & Packard (2022), Int. Rev. Law & Econ. 72:106094, doi:10.1016/j.irle.2022.106094
[SOURCE: abstracts and introductions via Exa]
- Design: Castro's April 1980 opening raised Miami's population by about 7%; synthetic control
  against matched metros.
- Outcomes: Card measures wages and unemployment (null). Billy–Packard measure crime: murder
  +41.2% over seven years, property crime +25–32% and robbery +70% to 1990. A demographic
  reweighting explains "only 12%–14%", and prior incarceration of the arrivals explains the rest.
  Neither measures trust, security spending or time use.
- **Clears the bar? Design yes, outcome no.** Billy–Packard warn the event is sui generis: "the
  worst observed migration event in terms of public safety in US history".

### 12. Severino & Visconti (2025), "Immigration Shocks and Unfounded Concerns About Crime: Evidence from Haitian Migration to Chile", J. Politics 87(3), doi:10.1086/732963
[SOURCE: https://www.journals.uchicago.edu/doi/epdfplus/10.1086/732963, title and abstract only] [UNVERIFIED: design and estimates not read]
- From the title, the same setting as entry 9 with crime concern as outcome. Classified only as a
  lead: **probably not clearing the bar on our outcomes** unless it measures precautions.

### 13. Beerli, Ruffner, Siegenthaler & Peri (2021), AER 111(3):976–1012, doi:10.1257/aer.20181779
[SOURCE: https://doi.org/10.1257/aer.20181779, abstract]
- Design: the 1999–2007 free-movement reform gave EU cross-border commuters free access, with
  stronger exposure close to the border. Difference-in-differences by distance to the border.
- Outcomes: foreign employment rose substantially. Wages of highly educated natives rose, and firm
  size, productivity and innovation in skill-intensive incumbents rose. **No trust, security or
  time-use outcome.** The inflow is mostly highly educated EU commuters who do not reside in
  Switzerland.
- **Clears the bar? Design yes, outcome no.** It also does not move resident group composition in
  the sense the branch asks about.

### 14. Swedish and Norwegian studies
- Wallman Lundåsen (2022), Nonprofit & Voluntary Sector Q., doi:10.1177/08997640221077143, and the
  Delmi report 2021:3 [SOURCE: https://www.delmi.se/en/publications/report-and-policy-brief-20213-community-trust-in-sweden-before-and-after-the-refugee-crisis/].
  - 33–36 Swedish municipalities with differing 2014–17 reception of asylum seekers; panel survey.
  - Delmi: "In municipalities that received many new migrants per inhabitant, community trust
    decreased slightly more"; generalised trust not moderated.
  - Reception shares are not shown to be as-good-as-random, and no first stage is reported.
  - **Does not clear** [UNVERIFIED: coefficients not read].
- Fladmoe & Steen-Johnsen (2018), Scand. Pol. Stud., doi:10.1111/1467-9477.12127: 61 Norwegian
  communities, cross-section. Diversity is associated with community trust and the lost-wallet
  item (12.1 points on 0–100, most vs least diverse), not with generalised trust. Observational:
  **does not clear**.
- Swedish 1985–94 "Sweden-wide" placement (Edin, Fredriksson & Åslund 2003 and successors) is used
  for refugees' own outcomes. No paper found uses it for natives' trust, security or time use.

### 15. Time use and avoidance
- Obminski, A. B., "Choosing Distance" (job-market paper)
  [SOURCE: https://files.arturobminski.com/papers/migrant-avoidance/migrant-avoidance-OBMINSKI.pdf, introduction via Exa] [UNVERIFIED: tables not read; not peer-reviewed]
  - Design: Poland after the 2022 Ukrainian refugee arrival, using 43,371 natives' Google Maps
    review histories. Within-individual choice among establishments as a function of the local
    (200 m grid) migrant share. The shock's timing is exogenous, but where refugees settle within
    a commuting zone is not assigned.
  - Findings: there is "no such change in visits to consumption locations" (frequency). Natives
    were "11.54 percent less likely to choose a given consumption location as the migrant share
    increased by 10 percentage points", the equivalent of 261 m of extra distance; 20.57% for
    "third places".
  - It is the closest thing to a time or attention cost found, but it measures **location
    choice, not time use**.
  - **Does not clear the bar**: the within-area migrant share is endogenous, and there is no
    first stage.
- Maggio (2021), Soc. Sci. Q., doi:10.1111/ssqu.13018: the ATUS treatment is state "show me your
  papers" laws, not composition, and the outcome is Hispanics' own socialising time. **Does not
  clear** (wrong treatment).
- Bó & Dukhovnov (2022), Pop. Space Place, doi:10.1002/psp.2561: ATUS × segregation in LA, NYC and
  Miami, correlational. **Does not clear.**
- No paper found uses a natural experiment in group composition with **natives' time use** (ATUS
  or similar) or **guard or defensive labor employment** as the outcome.

## Summary table

| # | Paper | Composition variation | First stage | Outcome in bar? | Clears | Finding |
|---|---|---|---|---|---|---|
| 1 | Dinesen & Sønderskov 2015 | residence (selected) | none | trust | no | −0.06 per SD within 80 m; vanishes past ~200 m |
| 2 | Dustmann, Vasiljeva & Damm 2019 | DK dispersal (assigned) | assigned share | votes | no | +1.34/+2.32 pp anti-immigration vote per pp refugees |
| 3 | Couttenier et al. 2019 | CH allocation key | assigned | migrants' crime | no | +35% violent crime for conflict-exposed cohorts |
| 4 | **Albarosa & Elsner 2022** | DE dispersal (Königstein + housing) | measured inflow, DiD | **trust, crime worry** | **yes** | trust .00 (.01) per doubling; caution toward foreigners +.019 |
| 5 | Tang (student WP) | DE state allocation | DiD | trust | yes, low weight | null |
| 6 | Kim & Kim 2020 | East→West German migration (selected) | none | trust | no | negative correlation |
| 7 | Lange & Sommerfeld 2024; Gehrsitz & Ungerer 2022 | DE quotas IV | yes | crime, jobs, votes | no | lagged small crime rise |
| 8 | **Bove, Elia & Ferraresi 2021** | IT shift-share IV | yes | **security spending** | **yes (shift-share)** | +0.12–0.30 pp of budget per pp immigrants, through fear |
| 9 | **Ajzenman, Dominguez & Undurraga 2023** | CL shift-share IV | F = 17.35 | **home security, block guards** | **yes (shift-share)** | +10.0 (4.7) and +12.4 (4.1) index points per log-doubling; crime null |
| 10 | Hangartner et al. 2019 | Greek islands distance IV | yes | hostility | no | +0.24 SD hostility toward asylum seekers |
| 11 | Card 1990; Billy & Packard 2022 | Mariel | synthetic control | wages; crime | no | wages null; crime up (sui generis) |
| 13 | Beerli et al. 2021 | CH cross-border opening | DiD by distance | firm outcomes | no | native high-skill wages and firm productivity up |
| 14 | Swedish and Norwegian studies | reception or observational | none | trust | no | slight community-trust fall (Delmi) |
| 15 | Obminski; Maggio; Bó & Dukhovnov | various | none or wrong treatment | location, time | no | avoidance of migrant-dense venues (Poland) |

**Verdict:** Three designs clear the bar.
- **Trust:** Albarosa & Elsner, from Germany's policy-assigned 2015–16 refugee dispersal, find a
  **precise null on natives' generalised trust** (.00, SE .01 per doubling), with no change in
  worry about crime.
- **Defensive spending:** two shift-share IVs, weaker than assignment, find **positive defensive
  spending responses driven by fear, not crime**:
  - Italian municipal security budgets rise 0.12–0.30 pp per pp of immigrants (Bove, Elia &
    Ferraresi);
  - Chilean households' home-security and block-guard adoption rises with no change in measured
    victimisation (Ajzenman, Dominguez & Undurraga).
- **Time use and defensive labor:** **no design measures natives' time use or guard or defensive
  labor employment.**

[INFERENCE] The branch's specific question, whether low friction and high trust free work time and
attention, has **no qualifying natural experiment**. On that question the branch stops. The
adjacent identified evidence is mixed: trust does not move under assigned refugee dispersal, while
perception-driven precaution spending does rise under shift-share inflows in Italy and Chile. That
spending is the channel the account already prices as fear and private security. Every
qualifying design is a refugee or Latin American and European inflow, with no US Mexican-origin
case.
