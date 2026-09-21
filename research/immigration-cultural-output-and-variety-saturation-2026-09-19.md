# Cultural output of the Mexican-origin population at matched SES, and whether variety saturates in group size

**Verdict:** At matched age, education and sex the Mexican-origin population supplies about three quarters as much creative labour per head as US-born non-Hispanic whites (US-born Mexican-origin 0.723, SE 0.034; Mexico-born 0.742, SE 0.059, ACS 2024 PUMS with replicate weights), and the gap survives restriction to BA+ holders (0.67–0.76) and reverse standardisation; music and the performing arts are the one genre where parity cannot be rejected. Creative earnings per capita, the only market-priced output, are $865–905 against $1,362 matched. In the canon (27 award categories, 1990–2025), Hispanic winners are 6.25% of US-citizen winner-years since 2015 against a Hispanic BA+ population share of 9.6%, up from 2.91% against 6.2% before 2015: below the credentialled benchmark throughout, rising, with a post-2015 doubling this design cannot separate from a selection-rule change; the documented-Mexican share is 0.89% against 11.1% of adults. On variety, the operator's saturation hypothesis is supported at the local margin: Mexican-cuisine restaurants per head have an elasticity of 0.18 (SE 0.03) in a metro's Mexican-origin share, 27 SE below one, three quarters of the fitted maximum density is reached by a 10% local share and the curve is flat above 20%; 95% of the lowest-decile metros (0.7% Mexican-origin) already have a Mexican restaurant. Placebos on all, Chinese and Italian restaurants load at zero or negative, an independent name classifier gives 0.14, and OSM coverage does not vary with Mexican share. The national "1/100 of them" counterfactual is not identified by cross-metro variation, and one in eight US cooks was born in Mexico (12.05%, one in five with the US-born), so the supply is not free of the group's labour. Latin music is 8.1–8.8% of US recorded-music revenue with crossover unmeasured. A fair cultural line is single-digit hundreds to low thousands of dollars per person-year, against a fiscal gap of −$7,224. [SOURCE: `infra/immigration-fiscal/cultural_output_2026_09_19/RESULT.md`, `derived/`] [FRAMING-SENSITIVE: occupation is supply not quality; awards are gated by credentials and selection rules; restaurants conflate supply with the group's own demand]

Date: 2026-09-19. Lane: `infra/immigration-fiscal/cultural_output_2026_09_19/`. Arm C (patent and copyright registrations) stopped: PatentsView bulk returns 403 and the API needs a key; the Copyright Office offers record search only (`derived/arm_c_stop_note.md`).

## 1. Creative labour (arm A)

ACS 2024 1-year PUMS, ages 25–64, SOC 27 occupations minus sports, direct standardisation to the white age × education × sex distribution, 80 successive-difference replicate weights. Creative employment per 1,000: Mexico-born 5.86 crude and 13.07 standardised; US-born Mexican-origin 11.06 and 12.72; US-born white 17.61; other foreign-born 14.29. For the Mexico-born three fifths of the raw gap is composition; for the US-born group only a quarter is, and the matched ratio is 8 SE below parity. By genre (US-born Mexican-origin): music and performing 0.80 (0.13), visual arts and design 0.70 (0.04), writers and media 0.72 (0.08), film and TV 0.77 (0.10). Creative earnings per capita standardised $905 and $865 vs $1,362; creative workers' mean earnings $67k and $61k vs $77k; BA+ share of creative workers 48% and 41% vs 70%. The ACS has no parental birthplace, so the reference is US-born rather than third-plus whites; CPS ASEC 2025 prices that substitution at 2.6% (17.21 vs 16.76 per 1,000). Age-cohort ratios rise from 0.65 at 55–64 to 0.75 at 25–34, 1.1 SE apart, so convergence is not established. [SOURCE: `derived/arm_a_creative_rates.csv`, `arm_a_cells.csv`, `arm_a_by_age_cohort.csv`, `arm_a_cps_generation_check.csv`] [CALCULATION]

## 2. Awards and canon (arm B)

Wikidata winner statements for 27 categories (Oscars, Pulitzers, National Book Awards, Grammy general fields, MacArthur, National Medal of Arts, Tonys), 1,466 winner-years; origin documented for 1.4% and otherwise surname-imputed at the 70% Hispanic threshold, 16–23% of names unmatched and counted non-Hispanic (upper bound treats them as matched). US citizens: 2.91% Hispanic 1990–2014 (upper bound 3.48%) and 6.25% 2015–2025 (7.58%), against Hispanic BA+ shares of 6.2% and 9.6%, ratios 0.47 and 0.65; against all adults 0.22 and 0.36. Non-citizen winners are Hispanic at about twice the citizen rate. The post-2015 step is real and the design cannot attribute it: a gentle age-cohort supply gradient in arm A is consistent with both a selection-rule change and a real rise among younger cohorts. [SOURCE: `derived/awards_*.csv`, ACS C15002I and B15002] [CALCULATION]

## 3. Variety saturation (arm D)

OpenStreetMap restaurant and fast-food features in 32 fetched states (271,624 features, 82% cuisine-tagged) assigned to 2023 CBSAs; Mexican-origin share and income from ACS 2019–2023 5-year; Poisson QMLE with a log-population offset on the 573 CBSAs whose every state was fetched (covered metros hold 88% of the CBSA Mexican-origin population; the excluded set is the lower-share half).

| Specification | Elasticity | SE |
|---|---|---|
| Cuisine tag | 0.181 | 0.030 |
| Independent name classifier | 0.142 | 0.029 |
| Mexican share of tagged restaurants | 0.208 | 0.015 |
| Metros over 250,000, tag | 0.211 | 0.036 |
| Placebos: all / Chinese / Italian / American | −0.03 / −0.08 / −0.06 / −0.00 | |
| All 935 CBSAs, tag (disclosure only, see below) | 0.384 | 0.045 |
| … placebos on the 935: all / Chinese / Italian / Indian / American | 0.17 / 0.18 / 0.15 / 0.27 / 0.18 | |

The all-CBSA row is a disclosure and not an alternative estimate (added 2026-09-21). It adds the 362 metros that touch one of the 19 unfetched states, where a zero count is missing data: 346 of the 935 metros show no Mexican restaurant against 13 of the 573 covered ones, the excluded metros are the lower-share half, and on that sample the placebo for all restaurants loads at 0.17 where it should be zero. The 0.38 is therefore inflated by coverage that rises with Mexican share [INFERENCE from the placebo and the zero counts; the unfetched states were not fetched to confirm it]. Both samples reject proportional scaling, at 27 and 14 standard errors below one. [SOURCE: `derived/arm_d_elasticity.csv`, specs `all_cbsas` and `all_cbsas_placebo`; `scripts/11_arm_d_elasticity.py`, the `complete_states_only` comment]

Quadratic fit: predicted Mexican restaurants per 100,000 are 5.5 at a 0.5% share, 12.6 at 5%, 14.6 at 10%, 16.1 at 20% and 16.9 at 50%; the quadratic term is negative (−0.051, SE 0.014). Buffalo (0.6% Mexican-origin) carries 8.8 per 100,000 against Los Angeles (34%) at 15.5: a 53-fold difference in share and 1.8 times the density. OSM coverage against County Business Patterns establishment counts does not vary with Mexican share (t 1.4); the share of restaurants carrying any cuisine tag does rise with it (t 2.6), which biases the tag elasticity upward, so the headline is conservative. Pre-registered rejection conditions (elasticity near one, density still rising at the top) do not hold. What is identified is the local margin: within the observed range the marginal group member adds almost no further restaurant variety to the metro they live in, while the costs the repo prices scale per person. The national counterfactual is not identified, because every metro draws on a national labour market and supply chain, and 12.05% (SE 0.32) of US chefs and cooks are Mexico-born, 20.5% with the US-born Mexican-origin. [SOURCE: `derived/arm_d_elasticity.csv`, `arm_d_coverage_fit.json`, `arm_d_osm_coverage_check.csv`, `arm_d_cooks_shares.csv`] [CALCULATION]

## 4. Music (arm E)

RIAA year-end reports parsed from the PDFs: Latin music 8.1% of US recorded-music revenue in 2024 (retail basis) and 8.8% in 2025 (wholesale basis, $1.01bn). "Latin" is a language and genre category, not output of the US Mexican-origin population, and neither report gives listener composition, so crossover is unmeasured. [SOURCE: RIAA 2024 and 2025 year-end reports, `derived/arm_e_*`]

## 5. What a cultural line would be worth

Creative earnings are the only market-priced output: −$457 to −$497 per person-year against whites matched, and they are already inside the fiscal ledger as taxable income. A consumer-surplus multiple of 1–3× on the differential [INFERENCE, not derived] gives −$460 to −$1,500 per person-year relative to whites; on the group's own absolute output +$355 to +$2,200. Either way the channel is single-digit hundreds to low thousands against a fiscal gap of −$7,224 (ladder 130), and on the differential construction it does not point the other way. Restaurant variety is outside this figure and the saturation result governs how much of it can scale with population.

## 6. Limits

Occupation measures supply, not quality or influence; awards are gated by credentials, submission and selection rules that changed inside the window; surname imputation cannot separate Mexican from other Hispanic origin; OSM tagging is volunteered; restaurants per capita include the group's own demand; within-group and crossover consumption are not valued differently; 19 states are missing from the OSM sweep. Resident groups, not admission. No policy advice.

## Sources

ACS 2024 1-year PUMS (on disk); CPS ASEC March 2025; Wikidata SPARQL award statements (2026-09-19); Census 2010 surname file; ACS C15002I, B15002, B03001 and 2019–2023 5-year CBSA tables; OpenStreetMap via Overpass; TIGER 2023 CBSA boundaries; County Business Patterns 2023; RIAA year-end reports 2024 and 2025; ladder 130.

## Revisions

- 2026-09-21. §3 now discloses the all-CBSA specification (0.38) that the lane computed and the memo had not reported, with the reason the covered sample is preferred. A second agent's summary had presented 0.38 as an equally valid alternative; the placebo on that sample shows it is a coverage artefact. The local-saturation finding and its limit (national counterfactual not identified) are unchanged. Ladder 156.
