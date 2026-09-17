# IIMMLA 2004 (ICPSR 22627) by origin and generation — crime, schooling, welfare

**September 17 qualification:** the [independent audit](../../../research/immigration-new-datasets-and-conclusions-2026-09-17.md) reproduces the descriptive data but withdraws universal “at or below” parental-education wording and proof of parity/class mechanisms. Men in the some-college-plus-parent stratum have18.06% versus11.43% incarceration, with wide uncertainty. Undercounted rates do not establish lower-bound ratios, and a lifetime self-report ratio is not a bound on ACS current-stock ratios. Original evidence below retained; ladder108 governs these interpretations.

**Verdict:** IIMMLA reproduces Rumbaut's published arrest/incarceration table to within a point, and it adds what the ACS cannot: an exact third generation defined by grandparents' birthplace, and parental education. Two findings cut against the memo's current framing. (1) Self-reported lifetime arrest and incarceration among Mexican-origin men rise monotonically with generation — 1.5 gen is *below* third-plus whites, the second generation is at parity, and only the third-plus exceeds them; the "immigrant crime" gradient runs the wrong way for a nativity story. (2) Within strata of parents' education, the Mexican second generation is arrested and incarcerated at or below third-plus whites, while the bachelor's-degree gap survives the same control at roughly 13–25 points. Crime looks like class here; attainment does not.

Model self-report: environment block names **Opus 5 (1M context)**, model ID `claude-opus-5[1m]`.

[UNVERIFIED] — all figures below are this lane's own tabulations of the ICPSR 22627 public file unless tagged [SOURCE]. The Rumbaut reproduction check in §7 is the only external anchor.

---

## 0. Data, weights, and what the file will not support

`raw/ICPSR_22627/DS0001/22627-0001-Data.tsv`, 4,655 rows × 657 columns. Script: `iimmla_tab.py`. Outputs: `t1_groups_by_sex.csv`, `t2_ratios_vs_white3plus.csv`, `t3_mexican_generations.csv`, `t4_parental_education_strata.csv`, `t5_item_coverage_by_ethnos10.csv`, `t6_rumbaut_reproduction.csv`, `t7_gang_neighborhood_proxy.csv`.

**No survey weight exists in DS0001.** Every estimate here is UNWEIGHTED. This is less damaging than it sounds because IIMMLA is a quota sample: `QUOGRPS` fixed roughly 400 completes per target group, so group-internal rates are estimable but group sizes carry no population information. Nothing here can be aggregated into an LA-wide or national total.

Variables used, with their codebook labels:

| Variable | Label | Codes used |
|---|---|---|
| `gender` | Gender of respondent | 0 = Female, 1 = Male (note the unusual coding) |
| `ethnos10` | Ethnicity - 10 main groups | 1 Mexican, 2 Salvadoran/Guatemalan, 3 Other Latin American, 4 Chinese, 5 Korean, 6 Vietnamese, 7 Filipino, 8 Other Asian, 9 White non-Hispanic, 10 Black non-Hispanic |
| `ethnonat` | Ethno-national groups (detailed) | 1 Mexican, 2 Salvadoran, 3 Guatemalan, 21 Chinese, 22 Taiwanese, 25 Vietnamese, 26 Chinese-Vietnamese, 27 Filipino, 28 Korean, … |
| `paneth4` | Pan-ethnic/racial groups | 1 Latin American, 2 Asian, 3 White NH, 4 Black NH |
| `generat3` | Generational Cohort - 3 groups | 1.0 = 1.5 generation (n=1622), 2.0 = Second (n=1818), 3.0 = Third+ (n=1215) |
| `generat4` | Generational Cohort - 4 groups | 1.0 = 1.5, 2.0 = 2nd, 3.0 = 3rd (n=356), 4.0 = 4th+ (n=859) |
| `abuelofb` | If 3rd gen, N of foreign-born grandparents | 1–4, else −9 (valid n=332) |
| `q152a` | Were any of your grandparents born in a foreign country? | 1 Yes (332), 2 No (834), −9 not asked |
| `evarre` | Ever arrested (self only) | 0 No (3967), 1 Yes (688); no missing |
| `evpriso` | Ever incarcerated (self only) | 0 No (4264), 1 Yes (391); no missing |
| `educred5` | Highest educational level or degree | 0 Not HS grad, 1 HS grad, 2 Assoc/1–2 yr coll, 3 3–4 yr no degree, 4 Bachelor, 5 Advanced |
| `q177_c` / `q177_e` | Family received Medicaid/Medi-Cal / AFDC, TANF, SSI or disability in past year | 1 Yes, 2 No, −9 not asked |
| `q2_1` | Employment status - working | 1 Yes, 0 No, −9 not asked |
| `q37` | Current living arrangement | 1 Rent, 2 Own, 3 Parent's/relative's home, 4 College housing, 5 Other |
| `q171a` | Total 2003 personal income | 1 Nothing … 8 $100,000+, −9 not asked |
| `q176a` | Total 2003 household income | 1 <$12k … 7 $100k+ |
| `q72`, `q73`, `q76_1..8`, `q77_1..13` | Spouse/partner Hispanic origin, Mexican ancestry, race, Asian ancestry | used for intermarriage |
| `q133a` / `q150a` | Education level - Mother / Father | 1 Did not complete HS … 6 Graduate school |
| `q62_b` | Gang activity in neighbourhood of youth | 1 Big problem, 2 Somewhat, 3 Not a problem |

**Two skip structures I verified in the data and had to repair.**

1. **Welfare.** `q177_c` and `q177_e` were asked only of households whose 2003 income (`q176a`) fell in categories 1–4, i.e. under $50,000, plus don't-know/refused. Households at $50k+ were skipped outright (cross-tab is a clean 1.0/0.0 split). The raw "asked" rates are therefore conditional on a low-income screen whose incidence varies from 40% (Chinese) to 68% (Black) across groups, and are **not comparable between groups**. The headline `any_welfare` column codes the high-income skip as non-receipt. That is an assumption, defensible for means-tested Medi-Cal and TANF, weaker for the SSI/disability half of `q177_e`. Both versions are in `t1`; `any_welfare_asked` is the conditional one.
2. **Personal income.** `q171a` was asked only of households with two or more earners (`q175a` ≥ 2). For sole-earner households I imputed personal income from household income (`q176a`, same bracket ladder shifted by one) when the respondent was that earner (`q175b`=1), and "Nothing" when someone else was. Coverage rises from 67% to about 94%.

**No gang-membership item exists in this file.** The only gang variable is `q62_b`, gang activity as a neighbourhood problem while growing up. Reported in §6 as a context proxy, not a behaviour measure.

---

## 1 & 2. All outcomes by group, pooled and by sex (unweighted)

Pooled. Every cell n ≥ 71. "Welfare" = Medicaid or TANF/SSI, full-sample version.

| Group | n | Arrested % | Incarc. % | No HS % | BA+ % | Welfare % | Employed % | Owns home % | Median personal income | Intermarried % |
|---|---|---|---|---|---|---|---|---|---|---|
| Mexican 1.5 | 290 | 13.4 | 7.2 | 36.9 | 12.4 | 33.6 | 75.8 | 31.8 | $16k band | 8.9 |
| Mexican 2nd | 553 | 17.4 | 11.2 | 19.0 | 16.8 | 29.7 | 71.5 | 25.4 | $16k band | 17.7 |
| Mexican 3rd+ | 401 | 25.4 | 15.0 | 18.5 | 16.7 | 21.8 | 73.4 | 29.4 | $25k band | 38.9 |
| Salv/Guat 1.5+2nd | 376 | 17.3 | 8.5 | 15.7 | 16.5 | 28.3 | 72.2 | 18.6 | $16k band | 8.5 |
| Chinese 1.5+2nd | 400 | 4.8 | 1.8 | 0.5 | 64.5 | 10.3 | 72.0 | 27.6 | $25k band | 16.5 |
| Korean 1.5+2nd | 399 | 9.0 | 2.8 | 2.3 | 59.9 | 10.8 | 65.9 | 29.7 | $16k band | 12.9 |
| Vietnamese 1.5+2nd | 401 | 5.0 | 3.2 | 2.0 | 47.6 | 27.6 | 65.2 | 24.2 | $6k band | 13.5 |
| Filipino 2nd | 214 | 7.0 | 3.7 | 1.9 | 44.4 | 11.7 | 70.3 | 25.8 | $16k band | 46.5 |
| Filipino 1.5+2nd | 401 | 7.5 | 4.2 | 3.0 | 42.1 | 12.3 | 72.1 | 28.5 | $16k band | 41.1 |
| **White NH 3rd+** | 407 | 20.6 | 10.6 | 9.1 | 43.5 | 11.5 | 73.1 | 35.5 | $25k band | 22.3 |
| Black NH 3rd+ | 405 | 29.1 | 19.3 | 15.6 | 20.2 | 35.4 | 66.2 | 18.0 | $20.5k band | 22.5 |

Ratios to white third-plus (pooled), full set in `t2_ratios_vs_white3plus.csv`:

| Group | Arrest | Incarc. | No HS | BA+ | Welfare | Employed | Owns home | Intermarried |
|---|---|---|---|---|---|---|---|---|
| Mexican 1.5 | 0.65 | 0.68 | 4.05 | 0.29 | 2.92 | 1.04 | 0.90 | 0.40 |
| Mexican 2nd | 0.84 | 1.06 | 2.09 | 0.39 | 2.58 | 0.98 | 0.72 | 0.79 |
| Mexican 3rd+ | 1.23 | 1.42 | 2.03 | 0.38 | 1.90 | 1.00 | 0.83 | 1.74 |
| Salv/Guat | 0.84 | 0.80 | 1.73 | 0.38 | 2.46 | 0.99 | 0.52 | 0.38 |
| Chinese | 0.23 | 0.17 | 0.05 | 1.48 | 0.90 | 0.98 | 0.78 | 0.74 |
| Korean | 0.44 | 0.26 | 0.25 | 1.38 | 0.94 | 0.90 | 0.84 | 0.58 |
| Vietnamese | 0.24 | 0.30 | 0.22 | 1.09 | 2.40 | 0.89 | 0.68 | 0.61 |
| Filipino 2nd | 0.34 | 0.35 | 0.21 | 1.02 | 1.02 | 0.96 | 0.73 | 2.09 |
| Black NH 3rd+ | 1.41 | 1.82 | 1.71 | 0.46 | 3.08 | 0.91 | 0.51 | 1.01 |

**Men** (white NH 3rd+ reference: 28.9% arrested, 17.4% incarcerated, n=201):

| Group | n | Arrested % | Incarc. % | Arrest ratio | Incarc. ratio | No HS % | BA+ % | Welfare % |
|---|---|---|---|---|---|---|---|---|
| Mexican 1.5 | 143 | 23.8 | 12.6 | 0.82 | 0.72 | 39.2 | 12.6 | 28.9 |
| Mexican 2nd | 273 | 29.3 | 20.1 | 1.01 | 1.16 | 22.0 | 18.7 | 23.2 |
| Mexican 3rd+ | 192 | 39.6 | 26.6 | 1.37 | 1.53 | 21.4 | 15.1 | 15.2 |
| Salv/Guat | 187 | 29.4 | 14.4 | 1.02 | 0.83 | 16.0 | 12.3 | 25.3 |
| Chinese | 226 | 6.6 | 2.7 | 0.23 | 0.16 | 0.4 | 59.3 | 8.0 |
| Korean | 198 | 13.6 | 3.0 | 0.47 | 0.17 | 2.0 | 56.1 | 12.1 |
| Vietnamese | 201 | 7.0 | 4.5 | 0.24 | 0.26 | 2.0 | 45.8 | 27.8 |
| Filipino 2nd | 110 | 9.1 | 5.5 | 0.31 | 0.32 | 0.9 | 41.8 | 11.8 |
| White NH 3rd+ | 201 | 28.9 | 17.4 | 1.00 | 1.00 | 11.9 | 42.8 | 9.0 |
| Black NH 3rd+ | 186 | 40.9 | 28.0 | 1.42 | 1.61 | 16.1 | 19.9 | 26.1 |

**Women** (white NH 3rd+ reference: 12.6% arrested, 3.9% incarcerated, n=206):

| Group | n | Arrested % | Incarc. % | No HS % | BA+ % | Welfare % | Employed % |
|---|---|---|---|---|---|---|---|
| Mexican 1.5 | 147 | 3.4 | 2.0 | 34.7 | 12.2 | 38.1 | 67.2 |
| Mexican 2nd | 280 | 5.7 | 2.5 | 16.1 | 15.0 | 36.1 | 67.4 |
| Mexican 3rd+ | 209 | 12.4 | 4.3 | 15.8 | 18.2 | 27.8 | 64.2 |
| Salv/Guat | 189 | 5.3 | 2.6 | 15.3 | 20.6 | 31.4 | 63.8 |
| Chinese | 174 | 2.3 | 0.6 | 0.6 | 71.3 | 13.5 | 70.4 |
| Korean | 201 | 4.5 | 2.5 | 2.5 | 63.7 | 9.5 | 57.3 |
| Vietnamese | 200 | 3.0 | 2.0 | 2.0 | 49.5 | 27.5 | 61.6 |
| Filipino 2nd | 104 | 4.8 | 1.9 | 2.9 | 47.1 | 11.5 | 71.3 |
| White NH 3rd+ | 206 | 12.6 | 3.9 | 6.3 | 44.2 | 14.1 | 66.5 |
| Black NH 3rd+ | 219 | 19.2 | 11.9 | 15.1 | 20.5 | 43.3 | 61.3 |

Reading. The sex gap swamps the group gap on crime: white third-plus men (28.9%) are arrested more often than Mexican third-plus women (12.4%). The incarceration ratio to whites is materially higher for Black women (3.05×) than for Black men (1.61×), because the white female base is so low.

Three results worth naming. First, **Mexican 1.5-generation men are arrested and incarcerated less often than third-plus white men** (0.82× and 0.72×), and the 1.5 generation has the highest no-high-school rate of any cell (39.2% of men), so this is not an attainment story. Second, **Korean men have an arrest rate (13.6%) four and a half times the Korean male incarceration rate (3.0%)**, the widest arrest-to-incarceration wedge of any group; Chinese, Vietnamese and Filipino men show the same pattern more weakly. Third, **Vietnamese welfare receipt (27.6% pooled, 2.40× whites) is the outlier among Asian groups** and sits at the Mexican second-generation level, consistent with refugee resettlement benefits and SSI/disability, which `q177_e` bundles together.

---

## 3. Mexican-origin: second versus third-plus, and what "third-plus" means

The brief's central question. In IIMMLA, "Mexican 3rd+" is a **self-identification** group: `QUOGRPS` category 9, "gen3 Mexican", people who identified as Mexican-origin with two US-born parents. Within it, `generat4` splits 3rd from 4th+ using `q152a`/`abuelofb`, whether any grandparent was foreign-born — the **exact** grandparent-birthplace definition. Both are available, so both are reported.

| | n | Arrested % | Incarc. % | No HS % | BA+ % | Welfare % | Employed % | Owns home % | Median income | Intermarried % (pan-ethnic) | Spouse not Mexican % |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Mexican 2nd | 553 | 17.4 | 11.2 | 19.0 | 16.8 | 29.7 | 71.5 | 25.4 | $16k | 17.7 | 28.5 |
| Mexican 3rd+ (self-ID, all) | 401 | 25.4 | 15.0 | 18.5 | 16.7 | 21.8 | 73.4 | 29.4 | $25k | 38.9 | 46.6 |
| — of whom 3rd (≥1 foreign-born grandparent) | 212 | 30.2 | 15.6 | 16.0 | 19.3 | 19.3 | 77.5 | 31.1 | $25k | 45.5 | 50.9 |
| — of whom 4th+ (no foreign-born grandparent) | 189 | 20.1 | 14.3 | 21.2 | 13.8 | 24.5 | 68.6 | 27.5 | $16k | 31.6 | 41.8 |

**The definition matters, and it matters in opposite directions for schooling and for crime.**

On attainment the exact split confirms the memo's §4 pooling-artefact claim in a second dataset. Pooled self-ID third-plus looks *flat* against the second generation: BA+ 16.7% vs 16.8%, no-HS 18.5% vs 19.0%, the classic "third-generation stall". Split by grandparents' birthplace, the genuine third generation gains (BA+ 19.3%, no-HS 16.0%, employment 77.5%, ownership 31.1%, median income one bracket higher) and the fourth-plus falls back (BA+ 13.8%, no-HS 21.2%, employment 68.6%). The stall is the third generation's progress averaged with a fourth-plus that has regressed — exactly what Duncan, Grogger, León & Trejo find in NLSY97 and what §4 of the memo already argues from those data.

On crime the split runs the **other** way. The exact third generation is arrested *more* than the fourth-plus (30.2% vs 20.1%), and incarceration is flat between them (15.6% vs 14.3%). So "the third generation is doing better" is true on schooling and false on arrests in the same 401 people. A single explanation covering both is not available from this file. Two candidates, neither testable here: arrest is partly exposure to policing, and the exact third generation is more concentrated in Mexican neighbourhoods (its neighbourhood-gang-problem rate is higher); or the fourth-plus cell, which is by construction people who still self-identify as Mexican after four generations, is a selected residual.

**Ethnic attrition is not solved by this design.** The `generat4`=4 cell is people with no foreign-born grandparent who *still* identify as Mexican. Everyone with Mexican-born grandparents who has stopped identifying as Mexican never entered the sampling frame at all. So the attrition bias the memo flags in §2 is present here in full; what IIMMLA adds is that *within* self-identifiers, the third/fourth-plus boundary moves attainment by 5.5 BA points and arrest by 10 points. That is a lower bound on how much generational pooling distorts a self-ID "US-born Mexican" cell.

Intermarriage rises steeply and monotonically across Mexican generations: pan-ethnic exogamy 8.9% (1.5), 17.7% (2nd), 38.9% (3rd+), and national-origin exogamy (spouse not of Mexican ancestry) 28.5% (2nd) to 46.6% (3rd+). Half of coupled third-plus Mexican-origin respondents have a non-Mexican partner, which is the engine of the attrition in the next generation.

---

## 4. Parental education: class or origin?

Parents' education = the higher of mother's and father's (`q133a`, `q150a`), collapsed to less-than-HS / HS-or-vocational / some-college-plus.

| Group | Parents' education | n | Arrested % | Incarcerated % | BA+ % | No HS % | Welfare % |
|---|---|---|---|---|---|---|---|
| Mexican 2nd | < HS | 182 | 15.9 | 12.1 | 10.4 | 25.8 | 36.8 |
| Mexican 2nd | HS/voc | 193 | 16.1 | 8.3 | 20.7 | 16.1 | 28.5 |
| Mexican 2nd | Some college+ | 130 | 15.4 | 10.0 | 25.4 | 8.5 | 19.2 |
| Mexican 3rd+ | < HS | 45 | 35.6 | 20.0 | 6.7 | 33.3 | 31.1 |
| Mexican 3rd+ | HS/voc | 177 | 23.7 | 13.6 | 11.3 | 22.0 | 21.5 |
| Mexican 3rd+ | Some college+ | 160 | 22.5 | 12.5 | 27.5 | 4.4 | 16.4 |
| White NH 3rd+ | < HS | **7** | 57.1 | 28.6 | 0.0 | 71.4 | 14.3 |
| White NH 3rd+ | HS/voc | 109 | 23.9 | 17.4 | 33.0 | 14.7 | 19.3 |
| White NH 3rd+ | Some college+ | 282 | 17.4 | 7.1 | 50.0 | 4.6 | 7.1 |

**The white less-than-HS cell is n=7 and must not be quoted.** Its existence is the point: third-plus whites in LA essentially do not have parents without a high-school education, which is why an unconditional white/Mexican comparison is partly a comparison of two different parental-education distributions.

Within the two usable strata the answer is clean and cuts against an origin story for crime. At HS/vocational parents the Mexican second generation is arrested at 16.1% against 23.9% for whites and incarcerated at 8.3% against 17.4% — **half the white rate**. At some-college-plus parents, arrest is 15.4% vs 17.4% and incarceration 10.0% vs 7.1%, roughly at parity. The unconditional pooled near-parity (0.84× arrest, 1.06× incarceration) is therefore *worse* than the within-stratum picture, because the Mexican second generation is concentrated in the low-parental-education strata where everyone's rates are higher.

The bachelor's gap does not behave this way. At HS/vocational parents: 20.7% vs 33.0%. At some-college-plus parents: 25.4% vs 50.0%. The gap widens in absolute terms as parents' education rises — 12 points, then 25. Whatever is depressing Mexican second-generation degree completion is not parental education, and it is not shared with the crime outcome.

Mexican third-plus sits between: within strata its arrest rate is at or slightly above whites (23.7 vs 23.9; 22.5 vs 17.4) and its incarceration below or above depending on stratum (13.6 vs 17.4; 12.5 vs 7.1). So the generational deterioration in §3 survives a parental-education control only weakly, and in the HS stratum not at all.

---

## 5. Reconciliation with `research/immigration-mexican-origin-generation-incarceration-2026-09-16.md`

**§2, the 1.7–1.9× ACS institutionalisation ratio.** IIMMLA agrees on sign and disagrees on magnitude. Pooling the US-born Mexican-origin men (2nd + 3rd+, n=465) gives 22.8% ever incarcerated against 17.4% for third-plus white men: **1.31×**, against the ACS 2023–24 raw 1.7–1.9×. Two reasons the numbers should differ and one reason they should be compared anyway.

- **Lifetime versus stock.** `evpriso` is ever-incarcerated over a life to age 20–39. ACS institutional group quarters is a point-in-time count, which weights long sentences heavily. A group with more short jail spells and fewer long prison terms will show a higher lifetime rate and a lower stock rate, and vice versa. The two ratios are not the same estimand and 1.31 vs 1.8 is not a contradiction.
- **The household frame excludes the currently incarcerated.** IIMMLA is an RDD household survey. Everyone in prison on the interview date is out of frame, and self-reported arrest and incarceration under-report in every validation study. Both biases push all groups down, and push hardest on the groups with the highest true rates — Black third-plus and Mexican third-plus. So 1.31× is a **lower bound** on the true lifetime ratio, and the gap to the ACS 1.8× narrows by an unknown amount. The ACS runs the opposite way: it counts the institutionalised directly and misses nobody for being locked up.
- **What IIMMLA adds that the ACS cannot.** The ACS has no parental birthplace, so its "US-born Mexican" cell is the 2nd+3rd+ mixture the memo flags in §1. IIMMLA separates them: **1.16× for the second generation, 1.53× for the third-plus** on incarceration among men. The memo's §2 caveat that ethnic attrition biases the self-ID US-born Mexican rate upward is confirmed in direction, and the generational composition effect is now quantified: moving from a pure second generation to a pure third-plus moves the male incarceration ratio by 0.37.

**§4, the third-generation stall on test scores.** Agrees, and extends it from scores to schooling and to a dataset with actual grandparent birthplace. The flat second-to-third-plus BA rate (16.8 → 16.7) reproduces the stall; the 3rd/4th+ split (19.3 vs 13.8) reproduces the pooling artefact. This is a second, independent confirmation of the §4 reading that the genuine third generation gains and the fourth-plus falls back, and it is stronger evidence than NLSY97 alone because the outcome is completed attainment rather than a test score.

**§5, origin cells versus ACS 2020–24.** Ordering agrees; magnitudes are mixed.

| Origin | ACS 2020–24, US-born men 18–39, ratio to NH white | IIMMLA men, ever incarcerated, ratio to white 3rd+ |
|---|---|---|
| Salvadoran / Guatemalan | 0.67 (Salv) / 0.83 (Guat) | 0.83 |
| Vietnamese | 0.30 | 0.26 |
| Chinese | — (0.12 rate in §5 table) | 0.16 |
| Mexican (US-born) | 1.68 | 1.31 |

Vietnamese and Chinese reproduce almost exactly. Salvadoran/Guatemalan reproduces at the Guatemalan end of the ACS range, with the caveat that IIMMLA's Central Americans are 1.5 and second generation while the ACS cell is US-born only, so IIMMLA's is the more favourable composition and still lands at 0.83. The Mexican cell is the one that shrinks, for the lifetime-versus-stock reason above.

**Where IIMMLA disagrees outright.** The memo's framing throughout treats the ACS "US-born Mexican" rate as the quantity of interest. IIMMLA says that quantity is dominated by generation-three-and-beyond and that the *second* generation — the actual children of immigrants, the group an immigration-policy counterfactual acts on — is at 1.16× white men on incarceration and 1.01× on arrest, and at or below whites once parental education is held constant. That is a materially different policy object from 1.68×, and no ACS-based number can separate them.

**Scope limits that bound all of the above.** Greater Los Angeles only, five counties. 2004 fieldwork, so the cohort is people born 1964–1984, a cohort whose young adulthood spans the 1990s crime peak; a 2004 lifetime arrest rate is not a 2024 one. Ages 20–39, so late-onset incarceration is censored out. And the quota design means these are within-group rates, never population aggregates.

---

## 6. Disconfirming evidence and instrument caveats

**Response rates** [SOURCE: 22627-0001-Codebook.pdf, "Cooperation Rate and Response Rate Calculations", Field Research Corporation methodology section]. Screening-instrument cooperation (AAPOR COOP1) 76.2%; main-questionnaire cooperation 82.1%; **overall cooperation 63%**. Screening RR3 50.2%, main-questionnaire RR3 55.6%, **overall response rate approximately 28%**. RR3 assumes 20% of the 45,097 unresolved numbers were usable residential lines. A 28% response rate on a crime self-report means the non-response bias is plausibly larger than several of the group differences above, and it is not estimable from the public file.

**Self-report under-reporting is the dominant threat and it is differential.** Three mechanisms, all pushing measured rates down and all pushing hardest on the highest-rate groups: (a) the household frame excludes the currently incarcerated; (b) socially undesirable behaviour is under-reported on the telephone, more so in a second language (3.5% of interviews were in Spanish, `intlang`); (c) people with active justice-system contact are harder to reach by RDD and likelier to refuse. Any comparison of IIMMLA rates to administrative or census-GQ rates should treat IIMMLA as a floor.

**Rumbaut's own caveat, from the multivariate result.** In the merged-sample logistic regression of ever-convicted-and-jailed, "ethnicity washed out of the logistic regression once the other predictor variables were controlled — that is, none of the ethnic group variables was significantly linked to incarceration, despite the fact that non-Hispanic blacks and Mexicans had the highest rates of arrest and incarceration". The surviving predictors were adolescent educational attainment, generational status, two-parent upbringing and having grown up in a dangerous neighbourhood [SOURCE: Rumbaut, "Undocumented Immigration and Rates of Crime and Imprisonment: Popular Myths and Empirical Realities", Appendix D in *The Role of Local Police*, Police Foundation 2009, pp. 132–133, https://www.policinginstitute.org/wp-content/uploads/2015/06/Appendix-D_0.pdf]. My §4 stratification is consistent with that on the crime side and inconsistent with it on the attainment side.

**Neighbourhood gang exposure** (`q62_b`, "big problem" while growing up), the only gang variable in the file:

| Group | % big problem |
|---|---|
| Mexican 1.5 | 37.7 |
| Mexican 2nd | 27.5 |
| Mexican 3rd+ | 18.3 |
| Salv/Guat | 34.0 |
| Vietnamese | 11.5 |
| Filipino 2nd | 11.2 |
| Chinese | 5.0 |
| Korean | 4.8 |
| White NH 3rd+ | 5.4 |
| Black NH 3rd+ | 23.6 |

This is the sharpest disconfirmation of a simple neighbourhood-exposure account of the generational arrest gradient: gang exposure falls monotonically across Mexican generations (37.7 → 27.5 → 18.3) while arrest rises monotonically (13.4 → 17.4 → 25.4). Whatever drives the generational crime gradient in these data, it is not measured childhood neighbourhood gang exposure.

**Welfare comparisons are the weakest numbers here** for the income-screen reason in §0, and because `q177_c`/`q177_e` ask about "you or anyone in your immediate family", not the respondent. A young adult living in a parent's home (32.6% of the sample, `q37`=3) reports the parents' receipt. Group differences in co-residence therefore contaminate the welfare column directly.

---

## 7. Reproduction check against Rumbaut's published table

`t6_rumbaut_reproduction.csv`. Benchmark: Table 4, "Arrest and incarceration among young men in Southern California, by ethnicity and generation (merged IIMMLA and CILS-III surveys: N=2,971 males, ages 20–39; mean age 27.5)", adapted from Rumbaut 2008 [SOURCE: Police Foundation Appendix D, pp. 132–133, text and table transcribed this session from the PDF]. The benchmark is a **merged** IIMMLA + CILS-III sample, so the 1.5 and second-generation cells include CILS-III cases my IIMMLA-only tabulation does not have; the third-plus cells are IIMMLA-only in both, because CILS-III sampled only foreign-parentage youth.

| Cell | Rumbaut Table 4 | This lane (IIMMLA only) |
|---|---|---|
| All men, 1.5 gen | 13.2 arrested / 8 incarcerated | 13.7 / 7.5 |
| All men, 2nd gen | 20.7 / 12 | 21.1 / 11.8 |
| All men, 3rd+ gen | 36.3 / 24 | 35.7 / 23.4 |
| Mexican men, 1.5 | 22.3 / 12 | 22.5 / 12.3 |
| Mexican men, 2nd | 29.8 / 20 | 28.7 / 20.0 |
| Mexican men, 3rd+ | 39.6 / 27 | 39.0 / 26.4 (39.6 / 26.6 unrestricted by age) |
| Latino men, all gen | 29 / 18 | 29.4 / 18.4 |
| Asian men, all gen | 10 / 6 | 10.2 / 4.6 |
| White NH men, 3rd+ | 29 / 18 | 26.9 / 16.1 (28.9 / 17.4 unrestricted by age) |
| Black NH men, 3rd+ | 40 / 27 | 42.3 / 28.6 (40.9 / 28.0 unrestricted by age) |

Every cell reproduces within about 1 point except Asian incarceration (4.6 vs 6, where CILS-III adds Cambodian and Laotian cases IIMMLA samples only as "Other Asian"). The third-plus rows match the published figures more closely when I do **not** impose the 20–39 age filter, which suggests Rumbaut used all IIMMLA completes; the study targeted 20–39 but a minority aged past 39 during fieldwork. My §1–§4 tables use all completes, consistent with that.

The published table therefore validates both the variable construction (`evarre`, `evpriso`, `generat3`, `ethnos10`) and the direction of the headline result: **"the patterns are linear, but with the outcomes worsening over time and generation — and acculturation — in the United States"**, and "the rates for all of the immigrants and U.S.-born children of immigrants in this sample are lower than the rates for native-stock majority-group whites." Rumbaut's own sample says the second generation is below third-plus whites on arrest; my 1.01× male arrest ratio for the Mexican second generation specifically is the one place I would qualify that sentence, since it holds for the pooled second generation but not for the Mexican second generation on its own.
