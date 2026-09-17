# CILS 1991–2006 (ICPSR 20520) by national origin and generation — crime, schooling, welfare

**Verdict:** The gate passes. Merging my CILS San Diego male cells with the sibling lane's IIMMLA cells reproduces Rumbaut's Table 4 Mexican men to within 0.8 points on all four target figures (1.5 gen 21.6 arrested / 12.1 incarcerated against 22.3 / 11.9; 2nd gen 29.0 / 20.3 against 29.8 / 20.4), and the all-men rows reproduce to within 0.6. But the reproduction exposes what the benchmark is made of: **the only arrest and incarceration items in the CILS public file are five-year-window items** ("During the last 5 years … I was arrested"), not lifetime ones, and they are what reproduce Rumbaut's "ever arrested" column. Three substantive results. (1) The 1.5-to-second-generation gradient is real inside CILS and is **concentrated in the Mexican-origin cell**: Mexican men go 19.7 → 28.9 on arrest and 10.6 → 20.5 on incarceration, against a pooled all-origin male move of 13.7 → 16.5 and 7.7 → 9.5, and the Cuban second generation moves *down*. (2) Panel attrition is strongly selective on exactly the covariates that predict arrest — retained cases have 0.41 higher wave-I GPA, 15 points more intact families, 0.23 SD higher parental SES, 7.4 points less 1995 dropout and 6.9 points less school fighting — so every wave-III crime rate here is a floor, and it is a lower floor for Mexican-origin (56.2% retention, the second lowest of the large origins) than for Filipino (72.4%). (3) Within parental-education strata the Mexican second generation stays above other immigrant-origin groups on arrest and incarceration, which does **not** reproduce the IIMMLA §4 result — but the comparison group is different, because CILS has no native-parentage cell at all, so the two lanes are not testing the same proposition.

Model self-report: environment block names **Opus 5 (1M context)**, model ID `claude-opus-5[1m]`.

[UNVERIFIED] — every figure below is this lane's own tabulation of the ICPSR 20520 public file unless tagged [SOURCE]. The Rumbaut Table 4 benchmark in §3 is the only external anchor.

---

## 0. Data, weights, items, and the skip structures verified in the file

`raw/ICPSR_20520/DS0001/20520-0001-Data.tsv`, 5,262 rows × 665 columns. Scripts: `cils_tab.py` (tables), `cb_scan.py` (codebook → `cb.txt`, gitignored), `supp.py` (robustness and context checks). Outputs: `t1_origin_by_generation.csv`, `t2_attrition.csv`, `t3_rumbaut_reconciliation.csv`, `t4_parental_ses_strata.csv`.

Sites: Miami 2,503, Ft. Lauderdale 339, San Diego 2,420 (`V2`). Birth years 1974–79, mean 1977 (`V20`); wave-I age mean 14.2 (`V19`). Wave III (`V400` = 1): **3,344 of 5,262, 63.5%**.

**No sampling or attrition weight exists in DS0001.** I scanned all 665 variable labels; there is no weight variable of any kind, and the ICPSR codebook front matter states the frequencies it prints "are not weighted … Please review any sampling or weighting information available with the study" [SOURCE: 20520-0001-Codebook.pdf p. 4]. Every estimate in this file is therefore **unweighted**, and nothing here aggregates to a population. This matches the sibling IIMMLA lane, which also has no weight.

### The crime items are five-year windows, not lifetime

| Variable | Codebook label and full question wording | Codes | Valid n (wave III) |
|---|---|---|---|
| `V448J` | *Respondent/arrested.* "During the last 5 years, have any of the following life change events happened to you or your family? **I was arrested.**" | 0 No, 1 Yes | 3,202 |
| `V448L` | *Respondent/detention/jail/prison.* "During the last 5 years … **I spent time in a reform school, detention center, jail, or prison.**" | 0 No, 1 Yes | 3,198 |
| `V448I` | *Respondent/family member arrested.* "… A member of my family was arrested." | 0 No, 1 Yes | 3,203 |
| `V448K` | *Respondent/family member detention/jail/prison.* | 0 No, 1 Yes | 3,202 |

A grep of every one of the 665 variable labels for `ever|arrest|jail|prison|incarcer|convict|probation|court` returns nothing else: **there is no lifetime arrest or incarceration item in the public file.** The wave-III interview was in 2001–03 at mean age ~24, so the five-year window covers roughly ages 19–24 and misses juvenile justice contact entirely. Pooled wave-III rates: 8.8% arrested, 4.8% incarcerated.

### Skip structures I checked in the data

1. **The `V448` block is wave-III only and otherwise universal.** Cross-tab of `V400` against `V448J` non-missing is clean: 3,202 of the 3,344 wave-III cases valid, **0 of the 1,918 non-wave-III cases**. The 142 missing are item non-response, not a skip. Same for `V448L` (3,198), `V424` welfare (3,272) and `V407` education (3,296). There is no income screen on welfare of the kind the IIMMLA lane had to repair.
2. **The `V408` degree series is unusable and I did not use it.** `V408A` (GED), `V408C` (HS diploma) and `V408H` (bachelor's) carry only 1,814 valid cases, and the pattern is *not* a function of `V407`: roughly half of every single `V407` category has them (e.g. 378 of 671 among "Graduated 4/5-yr college"). Whatever gates that block is not documented in the codebook and is not the respondent's attainment. All education below comes from `V407`.
3. **`V407` has a floor at 10 years of schooling.** Its lowest category is "Some High School (Grades 9-12, No Diploma)"; there is no below-9th-grade category (`V407A` recodes the minimum to 10 years). "No HS" here is therefore a floor and is **not** comparable to IIMMLA's `educred5` = 0. It is also depressed by the wave-I frame, which sampled students enrolled in 8th/9th grade in 1992 and so never contained anyone who left school earlier.
4. **The parental (`P`) interview is a 46% subsample and it is site-skewed.** `P1` = 1 for 2,442 of 5,262. By site: San Diego 54.5%, Miami 41.8%, Ft. Lauderdale 22.4%. `P56` family income valid for 2,322; `P31` parent education for 2,433. Because that skew is correlated with national origin (Mexican is almost entirely San Diego, Cuban almost entirely Miami), the P-variable columns carry a site-selection component that the child-reported columns do not. The strata in §4 therefore use **child-reported parental education** (`V36`/`V41`, max of mother and father, valid 4,791) as the primary stratifier, with `P56` income as the secondary one.
5. **Half the wave-III sample is still enrolled.** `V409` = 1 for 51.2% of wave-III respondents at mean age 24. Bachelor's-degree rates below are censored by age and are **not** comparable to IIMMLA's completed attainment at ages 20–39.

### Generation and origin

`V21A` (respondent birth country): 0 = United States → **second generation** (n = 2,630); any foreign country → **1.5 generation** (n = 2,628); 4 missing. By design **CILS has no third generation and no native-parentage comparison group** — every respondent has at least one foreign-born parent. Among the foreign-born, `V22` (US stay length at wave I) is: all my life 0 / ten years or more 1,217 / five to nine years 1,017 / **less than five years 309**. So about 12% of the 1.5 generation arrived after roughly age 9, slightly looser than Rumbaut's "arrived before teen years"; §3 reports the robustness check.

National origin uses `C3` ("National Origin. Constructed from `V9`, `V15`, and `V21a`. If father and mother are from different countries, mother's national origin is assigned"), which is a parental-birthplace construction rather than self-identification. Two combined rows are added: Lao/Hmong/Cambodian (`C3` 32, 33, 34) and Jamaican + West Indian (`C3` 22, 23).

---

## 1. Origin × generation × sex

Full table in `t1_origin_by_generation.csv` (every origin with wave-I n ≥ 60, each by 1.5 / 2nd / both and men / women / pooled, with wave-I and wave-III n, arrest, incarceration, no-HS, BA+, currently enrolled, employed, welfare, wave-I family income median and wave-I parental education). Pooled-sex headline rows:

| Origin | Gen | n W1 | n W3 | Arrested % | Incarc. % | No HS % | BA+ % | Enrolled % | Employed % | Welfare % | W1 family income median | Parents < HS % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Cuban | 1.5 | 355 | 222 | 9.4 | 5.2 | 5.0 | 21.0 | 46.3 | 85.5 | 3.2 | $22.5k | 29.3 |
| Cuban | 2nd | 870 | 588 | 9.0 | 3.6 | 3.8 | 32.0 | 54.7 | 83.1 | 2.1 | $42.5k | 13.8 |
| Mexican | 1.5 | 299 | 148 | 11.1 | 6.3 | 12.7 | 11.3 | 38.3 | 83.3 | 4.2 | $17.5k | 64.2 |
| Mexican | 2nd | 456 | 276 | 16.3 | 10.9 | 6.9 | 9.2 | 42.0 | 84.3 | 5.3 | $22.5k | 46.4 |
| Nicaraguan | 1.5 | 318 | 211 | 6.5 | 3.6 | 5.3 | 22.1 | 50.2 | 87.1 | 2.4 | $30k | 11.9 |
| Colombian | 1.5+2nd | 227 | 155 | 10.9 | 5.4 | 2.6 | 27.9 | 50.7 | 87.7 | 1.3 | $30k | 18.9 |
| Haitian | 1.5+2nd | 178 | 97 | 8.0 | 4.5 | 3.1 | 21.6 | 58.3 | 71.9 | 5.3 | $12.5k | 33.1 |
| Jamaican + West Indian | 1.5+2nd | 272 | 159 | 10.7 | 5.4 | 5.1 | 33.8 | 55.1 | 79.1 | 6.4 | $30k | 7.5 |
| Filipino | 1.5 | 370 | 245 | 5.5 | 3.8 | 2.5 | 24.1 | 54.5 | 79.3 | 2.1 | $42.5k | 4.0 |
| Filipino | 2nd | 449 | 348 | 5.6 | 3.8 | 1.5 | 29.2 | 58.9 | 82.6 | 5.5 | $52.5k | 3.1 |
| Vietnamese | 1.5 | 312 | 158 | 7.3 | 6.0 | 5.8 | 40.9 | 51.3 | 74.5 | 2.0 | $17.5k | 43.4 |
| Lao/Hmong/Cambodian | 1.5 | 293 | 180 | 4.0 | 3.4 | 6.4 | 13.9 | 41.8 | 81.5 | 3.5 | $17.5k | 56.5 |
| **Pooled** | 1.5 | 2,628 | 1,563 | 7.6 | 4.2 | 5.3 | 23.8 | 48.9 | 81.5 | 3.0 | $22.5k | 28.2 |
| **Pooled** | 2nd | 2,630 | 1,777 | 10.0 | 5.4 | 3.7 | 29.3 | 53.4 | 82.1 | 3.6 | $42.5k | 17.8 |

Men (the cells the crime items can actually support; n is the arrest-item denominator):

| Origin | Gen | n | Arrested % | Incarc. % | BA+ % | Enrolled % | Employed % | Welfare % |
|---|---|---|---|---|---|---|---|---|
| Mexican | 1.5 | 66 | 19.7 | 10.6 | 16.7 | 31.8 | 94.0 | 1.5 |
| Mexican | 2nd | 121 | **28.9** | **20.5** | 11.6 | 38.1 | 91.9 | 2.5 |
| Cuban | 1.5 | 86 | 17.4 | 8.3 | 13.6 | 39.3 | 91.2 | 1.1 |
| Cuban | 2nd | 302 | **14.2** | **6.0** | 34.8 | 50.5 | 83.3 | 2.6 |
| Colombian | 2nd | 31 | 25.8 | 18.8 | 31.2 | 65.6 | 87.9 | 3.0 |
| Nicaraguan | 1.5 | 88 | 12.5 | 8.0 | 22.3 | 44.7 | 84.4 | 2.1 |
| Jamaican + W. Indian | 1.5 | 19 | 21.1 | 10.5 | 21.1 | 50.0 | 75.0 | 5.0 |
| Jamaican + W. Indian | 2nd | 25 | 32.0 | 20.8 | 40.0 | 44.0 | 72.0 | 4.0 |
| Filipino | 1.5 | 111 | 8.1 | 5.4 | 14.0 | 57.5 | 79.1 | 0.0 |
| Filipino | 2nd | 165 | 8.5 | 6.1 | 21.0 | 61.5 | 89.7 | 2.4 |
| Vietnamese | 1.5 | 79 | 13.9 | 11.2 | 27.5 | 42.9 | 75.9 | 2.5 |
| Lao/Hmong/Cambodian | 1.5 | 78 | 7.7 | 7.7 | 7.9 | 41.1 | 83.3 | 2.7 |
| **Pooled** | 1.5 | 659 | 13.7 | 7.7 | 18.9 | 45.7 | 82.9 | 2.0 |
| **Pooled** | 2nd | 802 | 16.5 | 9.5 | 28.6 | 51.2 | 86.1 | 2.2 |

Women pooled: 1.5 gen 2.7% arrested / 1.4% incarcerated (n = 837), second 4.2% / 1.7% (n = 900). Mexican women 3.8 / 2.6 then 5.6 / 2.8. As in IIMMLA, the sex gap dominates: pooled second-generation men are arrested four times as often as second-generation women, which is a wider male-female ratio than any origin gap in the table.

**Three things the table says.** First, the generational rise in arrest is not general — it is Mexican and Caribbean. Mexican men move +9.2 points on arrest and +9.9 on incarceration, Jamaican/West Indian men +10.9 and +10.3 (small n), Colombian men +9.1; **Cuban men move down** (−3.2 and −2.3 on n = 302, the largest male second-generation cell in the file) and Filipino men are flat. The pooled +2.8 / +1.8 is a weighted average of those opposite movements. Second, the Mexican cell is the one that loses ground on schooling as well: it is the only origin whose second generation has a *lower* BA+ rate than its 1.5 generation (9.2 vs 11.3 pooled; 11.6 vs 16.7 among men), and it does so while parental education improves (parents below high school 64.2% → 46.4%). Third, welfare receipt (`V424`, TANF or SSI in the past 12 months, respondent's own) is tiny everywhere — 3.3% pooled, 5.3% at the Mexican second-generation maximum — because these are 24-year-olds reporting their own receipt, not their households'. It does no work in any comparison and should not be quoted against household-level measures.

---

## 2. Attrition

`t2_attrition.csv`. Wave-III retention overall 63.5%, and it ranges from 52.4% (Dominican) and 54.1% (Vietnamese) to 72.4% (Filipino). **Mexican retention is 56.2%, the second lowest of the large origins.**

Retained versus lost, on wave-I and wave-II covariates measured before the attrition happened (z is a two-sample z on the difference of means):

| Covariate | Retained | Lost | Diff | z |
|---|---|---|---|---|
| Wave-I GPA (`V139`, school records) | 2.67 | 2.26 | **+0.41** | 15.8 |
| Intact two-parent household (`V28` = father and mother) % | 69.3 | 54.3 | **+15.0** | 10.8 |
| Parent SES index (`V148`) | +0.02 | −0.21 | **+0.23 SD** | 10.7 |
| Dropped out by 1995 (`V337`, school records) % | 4.6 | 12.0 | **−7.4** | −8.5 |
| In a physical fight at school, wave II (`V220` = once or more) % | 13.5 | 20.4 | **−6.9** | −5.3 |

All five run the same way and they are large: the panel retained the higher-GPA, higher-SES, intact-family, non-dropout, non-fighting cases. Every one of those predicts lower arrest. **Wave-III arrest and incarceration rates in this file are therefore biased down, and the bias is differential** — it is worst where retention is worst. Mexican retention (56.2%) is 16 points below Filipino (72.4%), and the Mexican retained-lost GPA gap (+0.26) is smaller than Filipino's (+0.30) only because the Mexican wave-I GPA distribution is compressed lower to begin with (retained 2.36 vs Filipino 3.01). Every origin except Chinese (n = 72, z = −0.4) shows the same sign on GPA.

The behavioural covariate is the one to watch, because it is the closest thing in the file to a pre-treatment measure of the outcome. Cases lost between wave II and wave III were **20.4% likely to have been in a physical fight at school that year against 13.5% of the retained**, a 6.9-point gap at z = −5.3, and the gap is negative for every large origin (Cuban −9.2, Mexican −7.0, Filipino −6.5, Jamaican+West Indian −10.8). The panel shed the fighters. That is a direct, same-domain reason to treat the wave-III arrest rates as floors rather than an inference from SES. The one caveat on this item is that it is measured at wave II, so it is already conditioned on surviving the first attrition step and its denominator excludes the wave-I-only losses entirely; the wave-I GPA, SES and family-structure comparisons are not so conditioned and point the same way.

**There is no suspension or expulsion item in the file.** I checked all 665 labels; the closest behavioural measures are `V220` (in a fight at school, wave II) and `V337` (dropped out by 1995, school records). The brief's "suspensions" covariate does not exist in CILS and I have substituted the dropout record.

---

## 3. Rumbaut Table 4 reconciliation — the gate

`t3_rumbaut_reconciliation.csv`. Benchmark: Table 4, "Arrest and incarceration among young men in Southern California, by ethnicity and generation (merged IIMMLA and CILS-III surveys: N = 2,971 males, ages 20–39; mean age 27.5)" [SOURCE: Rumbaut, "Undocumented Immigration and Rates of Crime and Imprisonment: Popular Myths and Empirical Realities", Appendix D in *The Role of Local Police*, Police Foundation 2009, p. 132, text cached at `_cache/rumbaut_appendix_d.txt`].

**Scope decision, made from the benchmark text rather than assumed.** The article describes the merge as IIMMLA plus "the third wave of the Children of Immigrants Longitudinal Study (CILS) **in San Diego**", surveyed "in the same metropolitan region (the six contiguous Southern California counties)". The Miami and Ft. Lauderdale CILS cases are therefore out of Rumbaut's frame. I report both scopes; the gate is judged on San Diego.

IIMMLA male cells are taken from `../iimmla_2026_09_17/t6_rumbaut_reproduction.csv` (ages 20–39). CILS-III respondents were 22–29 at interview, so no age filter applies on my side. Merge is `(n_I·p_I + n_C·p_C) / (n_I + n_C)`.

| Cell | CILS SD n | CILS % | IIMMLA n | IIMMLA % | Merged | Rumbaut Table 4 | Δ | Gate |
|---|---|---|---|---|---|---|---|---|
| **Mexican men 1.5, arrested** | 61 | 19.7 | 138 | 22.5 | **21.6** | **22.3** | −0.7 | PASS |
| **Mexican men 1.5, incarcerated** | 61 | 11.5 | 138 | 12.3 | **12.1** | **11.9** | +0.2 | PASS |
| **Mexican men 2nd, arrested** | 114 | 29.8 | 265 | 28.7 | **29.0** | **29.8** | −0.8 | PASS |
| **Mexican men 2nd, incarcerated** | 115 | 20.9 | 265 | 20.0 | **20.3** | **20.4** | −0.1 | PASS |
| All men 1.5, arrested | 352 | 11.1 | 787 | 13.7 | 12.9 | 13.2 | −0.3 | PASS |
| All men 1.5, incarcerated | 352 | 7.9 | 787 | 7.5 | 7.6 | 7.8 | −0.2 | PASS |
| All men 2nd, arrested | 323 | 17.3 | 871 | 21.1 | 20.1 | 20.7 | −0.6 | PASS |
| All men 2nd, incarcerated | 323 | 12.3 | 871 | 11.8 | 11.9 | 12.1 | −0.2 | PASS |
| Salv./Guat. men 1.5, arrested (both sites; SD cell empty) | 8 | 25.0 | 87 | 21.8 | 22.1 | 21.3 | +0.8 | PASS |
| Salv./Guat. men 2nd, arrested (both sites) | 10 | 30.0 | 96 | 35.4 | 34.9 | 36.7 | −1.8 | PASS |

**All four Mexican gate cells land within 0.8 points of the benchmark, well inside the 2-point band.** The all-men rows and the Salvadoran/Guatemalan rows also pass. Sample-size arithmetic corroborates the San Diego reading: Rumbaut's merged total is 2,971 males against the IIMMLA lane's 2,196, implying a CILS-III male contribution of 775; my San Diego wave-III males number 710 (675 with a valid arrest item), while both sites give 1,533. San Diego is the right frame and the residual 65 is a wave-III-flag or age-edge difference I cannot resolve from the public file.

**What the pass tells us about the benchmark.** Rumbaut's column headings say "ever arrested" and "ever incarcerated", and the accompanying text says the men were asked "whether they had ever been arrested or incarcerated". For the CILS half of the merge that cannot be literally true of the public file, which contains only the five-year items. Two readings survive: either Rumbaut used `V448J`/`V448L` and the "ever" heading is loose for the CILS half, or a restricted CILS-III lifetime item exists that happens to yield near-identical rates at age 24. The arithmetic cannot separate them — backing out the CILS cell Rumbaut must have had (given his merged figure and the IIMMLA lane's cell) gives 21.9% for Mexican 1.5 arrest against my measured 19.7% on n = 61, a 1.3-case difference. [INFERENCE] The first reading is the more economical one, and either way the practical consequence is the same: **the CILS half of Rumbaut's famous table is a five-year window ending at age 24, not a life history**, and any use of Table 4 as a lifetime measure inherits that.

**Robustness on the 1.5-generation definition.** Rumbaut defines 1.5 as foreign-born and arrived before the teen years; `V21A` alone does not impose an arrival age. Restricting Mexican San Diego 1.5-generation men to those in the US five years or more at wave I (`V22` ≤ 3, i.e. arrived by roughly age 9) *raises* the cell from 19.7 / 11.5 (n = 61) to **26.1 / 15.2** (n = 46), moving the merged Mexican 1.5 figures to 23.7 / 13.3 and the arrest cell 1.4 points above the published 22.3. So the looser definition is the one that matches Rumbaut, and the recent arrivals I include are the low-arrest cases. This is a real caution for the whole 1.5-generation literature: the shorter the US exposure, the lower the measured rate, within the foreign-born.

**Cells that do not reconcile, reported rather than adjusted.** Vietnamese CILS San Diego men run 14.1 / 11.4 (1.5) and 14.3 / 14.3 (2nd) against Table 4's merged 8.1 / 5.8 and 12.7 / 9.9, well above what the merge with IIMMLA's low Vietnamese male rates (7.0 / 4.5 pooled) would produce. Laotian/Cambodian 1.5 men reproduce almost exactly (7.7 / 7.7 against 8.4 / 8.4, and the identical arrest and incarceration figures in the published row are themselves the signature of a small CILS-only cell). Korean, Chinese and Other Latin American San Diego cells have n between 1 and 12 and carry no information; Rumbaut's figures for those groups are IIMMLA-dominated.

---

## 4. Parental SES strata

`t4_parental_ses_strata.csv`. Stratifier: child-reported parental education, max of `V36` (father) and `V41` (mother) on the codebook's 1–6 scale, collapsed to < HS (1–3), HS grad (4), some college+ (5–6). Secondary stratifier: `P56` wave-I parental family income, bracket midpoints, collapsed at $15k and $35k. Second generation, pooled sex; n is the arrest-item denominator at wave III.

| Stratum | Group | n | Arrested % | Incarc. % | BA+ % | No HS % |
|---|---|---|---|---|---|---|
| Parents < HS | Mexican | 109 | 14.7 | 8.3 | 5.6 | 8.4 |
| Parents < HS | All other origins | 163 | 13.5 | 6.2 | 16.0 | 6.7 |
| Parents HS grad | Mexican | 64 | 21.9 | 18.8 | 3.2 | 6.3 |
| Parents HS grad | All other origins | 262 | 8.8 | 4.6 | 18.9 | 4.7 |
| Parents some college+ | Mexican | 69 | 14.5 | 7.0 | 20.3 | 4.3 |
| Parents some college+ | All other origins | 966 | 8.0 | 3.6 | 40.5 | 2.1 |
| Unstratified | Mexican | 264 | 16.3 | 10.9 | 9.2 | 6.9 |
| Unstratified | All other origins | 1,438 | 8.8 | 4.3 | 32.9 | 3.1 |

Named comparison groups within the same strata (all in the CSV): Cuban second generation runs 15.4 / 10.0 / 7.2 on arrest across the three strata, Filipino 22.2 (n = 9, **flagged**) / 7.0 / 4.8, Haitian+West Indian 0.0 (n = 14, **flagged**) / 11.1 / 15.8. **Cells flagged `YES(<40)` in the CSV must not be quoted**: every Vietnamese, Lao/Hmong/Cambodian and Nicaraguan second-generation stratum cell is under 40, as are the Filipino < HS cell (9), the Haitian+West Indian < HS cell (14) and the Mexican $35k+ income cell (31).

By wave-I family income (P56, with the 46% parental-interview coverage caveat from §0): Mexican second generation 15.2 / 13.8 / 22.6 on arrest across < $15k, $15–35k, $35k+ against other origins 11.9 / 11.2 / 5.9. The Mexican $35k+ cell is n = 31 and flagged.

Men only (`supp.py`), because arrest is overwhelmingly male:

| Stratum | Mexican 2nd men | Other-origin 2nd men |
|---|---|---|
| Parents < HS | n=44, 22.7 arrested / 13.6 incarcerated | n=70, 20.0 / 11.4 |
| Parents HS grad | n=28, 46.4 / 39.3 | n=118, 15.3 / 7.8 |
| Parents some college+ | n=37, 24.3 / 13.2 | n=465, 12.9 / 6.3 |

**Reading, and it is not the IIMMLA reading.** Controlling for parental education does not close the Mexican gap here; it closes only in the lowest stratum, where Mexican and other-origin second-generation rates are within 1.2 points on arrest and 2.1 on incarceration, and the Mexican disadvantage is largest in the middle stratum. The bachelor's gap behaves as it does in IIMMLA — it is large in every stratum and widens in absolute terms as parental education rises (10.4, 15.7, then 20.2 points) — so the schooling and crime outcomes separate in CILS too, just at different levels.

The middle stratum is where I would put the least weight and the most suspicion. Mexican second-generation men whose parents finished high school and no more show 46.4% arrested and 39.3% incarcerated on n = 28 — more than double the adjacent strata in the same group. On 28 cases a swing of three respondents moves that cell 10 points. I am reporting it because the brief asks for the strata, not because it supports a claim.

---

## 5. Reconciliation with IIMMLA and with the memo

### With `../iimmla_2026_09_17/RESULT.md` §3–§5

**The gradient agrees in direction and CILS localises it.** IIMMLA finds Mexican-origin male arrest rising 23.8 → 29.3 → 39.6 and incarceration 12.6 → 20.1 → 26.6 across 1.5, second and third-plus. CILS reproduces the first leg on an independent San Diego sample with a different instrument and a different cohort: 19.7 → 28.9 and 10.6 → 20.5. Two surveys, two metros, same first leg. What CILS adds is that **this is not a general immigrant-cohort pattern**: in the same file the Cuban second generation is *below* its 1.5 generation on both outcomes (men 14.2 vs 17.4, 6.0 vs 8.3) on the largest male cell in the study, and Filipino men are flat. IIMMLA could not see this because its non-Mexican Latin American and Asian groups are reported pooled across generations.

**The parental-education result does not transfer, and the reason is structural.** IIMMLA finds the Mexican second generation *at or below* third-plus non-Hispanic whites within parental-education strata (16.1% vs 23.9% arrested at HS-educated parents). CILS finds the Mexican second generation *above* other immigrant-origin groups within the same strata. These are not contradictory findings, because they use different comparison groups: **CILS has no native-parentage cell at all.** The IIMMLA comparison asks whether a Mexican second-generation man is arrested more than a white man whose grandparents were born here, at the same parental education. The CILS comparison asks whether he is arrested more than a Cuban or Filipino second-generation man, at the same parental education. The first answer is no; the second is yes. Anyone quoting "crime looks like class" from IIMMLA §4 should carry the qualifier that it is class *relative to third-plus whites*, and that against other children of immigrants at the same parental education the Mexican gap is still there. [FRAMING-SENSITIVE]

**Ethnic attrition.** IIMMLA's §3 result — that the third/fourth-plus boundary moves arrest by 10 points and BA+ by 5.5 among self-identified Mexicans — has no CILS analogue, because CILS is a school-roster panel with parental birthplace recorded at age 14 and no self-identification filter on entry. That is CILS's one clean advantage over both IIMMLA and the ACS on this question: within CILS, national origin cannot be lost to intermarriage or re-identification, because it was fixed from the parents' birth countries before any of it happened.

### With memo §5 (origin cells against ACS 2020–24)

The ordering **does not reproduce** outside the Mexican cell, and I am not going to force it.

| Origin | ACS 2020–24, US-born men 18–39, institutionalised, ratio to NH white [SOURCE: memo §5] | CILS men, incarcerated (5-year, age ~24) |
|---|---|---|
| Mexican | 1.68 | 2nd gen 20.5% (n = 121) — highest male cell with n > 100 |
| Cuban | 1.03 | 2nd gen 6.0% (n = 302) |
| Colombian | 0.27 | 2nd gen 18.8% (n = 31, unusable) |
| Vietnamese | 0.30 (1-year) | 1.5 gen 11.2% (n = 79), 2nd gen 18.8% (n = 16, unusable) |
| Cambodia / Laos / Hmong | 1.35 / 1.60 / 0.84 (1-year) | 1.5 gen 7.7% (n = 78) |
| Salvadoran / Guatemalan | 0.67 / 0.83 | n = 18 across both generations, unusable |

Mexican-highest and Cuban-well-below-Mexican reproduce. The Asian cells invert: the ACS says Vietnamese are low and Cambodian/Laotian high among the US-born, CILS says the opposite among the foreign-born. Four reasons, none of which I can rank from this file. The CILS Southeast Asian groups are almost entirely 1.5 generation (Vietnamese second generation n = 58 at wave I, Lao/Hmong/Cambodian n = 8), so there is no CILS analogue of the ACS US-born cell for them at all. The estimands differ — a five-year self-report at 24 versus a point-in-time institutional count at 18–39. San Diego's Vietnamese and Cambodian samples are refugee-resettlement populations that need not resemble the national US-born cell. And the CILS n are 16–79. The honest statement is that **CILS confirms the Mexican position in the origin ordering and cannot test the rest.**

### With memo §18 (IIMMLA)

§18's four results are unaffected in substance; CILS adds three qualifications. **(a)** Its headline gate framing — "the lane reproduces Rumbaut's published Table 4 within about a point" — is now reproduced from the other side of the merge as well, and the merged Mexican cells pass at 21.6 / 12.1 and 29.0 / 20.3. **(b)** §18 describes Table 4 as carrying "self-reported lifetime arrest and incarceration". That is accurate for the IIMMLA half only; the CILS half is a five-year window ending at age 24, which means the published merged column is a **mixed-estimand** figure, weighted roughly 74% IIMMLA lifetime and 26% CILS five-year among Mexican men. That does not change the sign of anything in §18 but it does mean Table 4's absolute levels are not a clean lifetime rate. **(c)** §18's "crime looks like class in this file; degree completion does not" needs the comparison-group qualifier in §5 above.

---

## 6. Disconfirmation and instrument caveats

**Attrition is the dominant threat and it is not estimable away.** §2 quantifies it: the panel kept the higher-GPA, higher-SES, intact-family, non-dropout, non-fighting cases, on z-statistics of 5 to 16. The wave-III crime rates are floors, differentially so by origin, and the worst-retained large origin is Mexican. If the lost cases had been retained at their wave-I risk profile, the Mexican second-generation male rates would be higher, not lower — which means the gate's agreement with Rumbaut is agreement between two floors, not between two estimates of the truth.

**Self-report, plus a frame that excludes the incarcerated.** A respondent serving a sentence in 2002 could not be interviewed by a panel that traced people to households and phone numbers, and socially undesirable behaviour is under-reported. Both push all rates down and push hardest on the highest-rate cells. The family-member items are the internal check and they run much higher than the self items: among wave-III Mexican second-generation respondents, 35.6% report a family member arrested and 33.5% report a family member in detention, jail or prison in the last five years, against 16.3% and 10.9% for themselves; the corresponding pooled figures are 19.6% / 16.8% against 10.0% / 5.4%. A family of four or five adults should produce roughly three to four times the individual rate if reporting were symmetric, and the Mexican second-generation ratio (2.2× and 3.1×) is inside that band, so this is a weak consistency check rather than evidence of under-reporting. It does confirm that the Mexican-origin second generation's *exposure* to the justice system is far wider than its own-arrest rate suggests.

**The five-year window truncates in both directions.** Ages 19–24 is after the juvenile peak for many and before the peak age of imprisonment for others. An adolescent arrest at 16 is invisible here and would show up in a lifetime measure. Nothing in this file speaks to the full life course, and the §3 merged figures inherit that for their CILS quarter.

**Two sites that are not interchangeable.** Miami/Ft. Lauderdale supplies almost all of the Cuban, Nicaraguan, Colombian, Haitian and West Indian cases; San Diego supplies almost all Mexican, Filipino, Vietnamese and Lao/Cambodian cases (Mexican: 727 of 755 in San Diego). **Origin and site are nearly collinear**, so every origin comparison in §1 is also a metro comparison, with different policing, labour markets and school systems. The gate in §3 is restricted to San Diego for exactly this reason.

**One cohort, born 1974–79.** These people were 19–24 in 1996–2003. Their teenage years span the peak and the first half of the great crime decline. A rate measured on this cohort is not a rate for people turning 24 in 2026, and the memo's ACS comparisons are 2020–24 stock counts on a much wider age range.

**Neighbourhood exposure does not explain the generational gradient here either.** `P112` (parent report at wave I, "In your neighborhood, how much of a problem is … delinquent gangs or drug gangs?", recoded so that 2 or 3 = a problem): Mexican-origin 1.5 generation 54.2%, second generation 53.4% — flat, against an arrest rate that rises from 11.1% to 16.3%. The pooled all-origin figure is 23.1% and 23.8%, also flat. `V214` ("There are many gangs in school", wave II, agree a lot or a little): Mexican 37.6% and 37.5%, again flat. This mirrors the IIMMLA §6 disconfirmation from the other direction — there, measured gang exposure *fell* across generations while arrest rose; here it is flat while arrest rises. In neither file does measured childhood gang exposure track the generational crime gradient. Whatever produces that gradient is not this variable. There is no gang-membership item in CILS.

**Instrument bias.** This analysis is produced by an LLM on a politically charged question (`notes/llm-bias-caveat.md`). The specific risk visible in this lane is the pull toward reporting the gate as a clean success and moving on. The gate does pass; the finding that matters more is that passing it required discovering the benchmark's CILS half is a five-year window, and that the IIMMLA lane's parental-education result does not survive a change of comparison group. Both of those cut against the tidier story.

**No population aggregation.** CILS wave I is a census of eligible 8th and 9th graders in selected San Diego and Miami-area schools in 1992, not a probability sample of any defined population, and it carries no weight. Every number here is a within-cell rate among panel survivors. Nothing in this file may be scaled to San Diego, to Miami, to the children of immigrants, or to anything else.
