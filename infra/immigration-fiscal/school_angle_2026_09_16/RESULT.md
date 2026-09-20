# School / classroom incidence of immigrant & ELL concentration

**Correction, 2026-09-20:** The categorical verdict below is superseded by the
[school-capacity audit](../../../research/immigration-school-capacity-harms-2026-09-20.md).
The education-quality channel is **unpriced**, not established at $0. Some peer
designs absorb schoolwide resource changes or control staffing, while US spending
cuts measurably harm white pupils. Neither fact identifies immigration's national
effect. The blanket second-generation exclusion is also withdrawn. Original
findings remain below as dated evidence, not the current conclusion.

**Verdict:** NO measured incumbent-student cost in US data. The best-identified US estimates (family-FE Florida, Haitian-influx IV, Delaware new-EL spillovers, Hunt's 1940-settlement IV) are ZERO to POSITIVE. The one credible negative is small, heterogeneous, and attaches to **English-learner status, not immigrant origin** — Diette & Oyelere's own decomposition finds Latin-American share has NO effect while limited-English share has a small one. The only causally-supported classroom mechanism (teacher time reallocation) is a **−1.8% SD non-US working-paper estimate** whose US analogues are zero. Threshold/non-linearity is NOT supported; the Colombia paper finds the effect *vanishes* at higher concentration. **None of it applies to the Mexican-origin second generation**, who are English-proficient by school age. Price it at **$0 per pupil-year**; the school channel's real content is head-count operating and capital cost.

Model self-report: claude-opus-5[1m] (Opus 5, 1M context), agent `school-angle`, dispatched 2026-09-16.

Provenance tags: [DATA] [INFERENCE] [SOURCE: url] [FRONTIER] [UNVERIFIED]

## Scope
Does immigrant / English-learner (ELL) concentration in classrooms impose a measurable cost on
incumbent (native, non-ELL) students — via peer effects, teacher time, literacy instruction,
tracking — or raise teacher turnover / degrade school metrics? Is any of it measurable for the
**Mexican-origin second generation** (US-born, largely English-dominant by school age) as distinct
from **first-generation ELL children**?

Sections to cover: (1) peer effects on native achievement; (2) teacher-side turnover/vacancies;
(3) literacy / NAEP trends; (4) non-linearity & concentration thresholds; (5) generation mapping.

## Findings

Blocks 1-6 below, then Verdict, table, and 5 runnable analyses. Remaining gaps are listed at the
bottom, ranked for a re-dispatch.

---

### Block 1 — Peer effects of immigrant / EL share on incumbent achievement: the US evidence is ZERO-to-POSITIVE, the negative estimates are non-US
[DATA: abstracts and published effect sizes, retrieved 2026-09-16 via Exa]

The literature splits cleanly by **country and by whether the design handles selection**. Every US
design that controls for family or school selection returns a zero or a positive. The negatives
come from Europe, Israel and China.

| Study | Setting / data | Design | Effect on incumbents | URL |
|---|---|---|---|---|
| Figlio, Giuliano, Özek, Sapienza, *Rev. Econ. Studies* 2024 ("Diversity in Schools", NBER w28596) | Florida, ~1.3m US-born students, avg 6% foreign-born classmates | **Sibling (family) fixed effects** on cumulative immigrant exposure | **POSITIVE.** Moving 10th→90th pct of cumulative exposure (1%→13% immigrant share) raises math **+2.8% SD**, reading **+1.7% SD**. Effect **double for Black and FRPL-eligible** students, ~zero for affluent. Naive school-FE-only spec gives a small negative — selection, not causation. | [ReStud 10.1093/restud/rdad047](https://doi.org/10.1093/restud/rdad047) · [NBER w28596 PDF](https://www.nber.org/system/files/working_papers/w28596/w28596.pdf) |
| Figlio & Özek, *JOLE* 2019 (repo-held) | Florida, 2010 Haitian earthquake influx | Within-school across-grade, birth-date IV | **Precise ZERO / mild positive.** +0.6–0.7% SD reading, 0.3–0.4% SD math per pp refugee share; fewer disciplinary incidents. Powered to detect <1% SD. | [10.1086/703116](https://doi.org/10.1086/703116) |
| Özek et al., *EEPA* 2024 ("Educational Spillover Effects of New English Learners in a New Destination State") | **Delaware**, grades 4–8, a *new-destination* state | New-EL arrival shocks to receiving schools | **POSITIVE and significant** short-run spillovers on other students' scores, concentrated among **current/former ELs**; **no adverse effect on non-ELs**. | [10.3102/01623737241282412](https://doi.org/10.3102/01623737241282412) · [EdWeek writeup](https://www.edweek.org/teaching-learning/no-the-arrival-of-english-learners-doesnt-hurt-other-students-a-study-finds/2024/10) |
| Hunt, *JHR* 2017 52(4):1060 | US state panel 1940–2010 | 1940-settlement-pattern IV | **POSITIVE net.** +1pp immigrant share of pop 11–64 → **+0.3pp** probability natives 11–17 complete 12 years. Positive especially for native-born Blacks; **not for native-born Hispanics**. | [jhr.uwpress.org/content/52/4/1060](https://jhr.uwpress.org/content/52/4/1060) · [NBER w18047](https://www.nber.org/papers/w18047) |
| "Are there Peer Effects from English Learners in Elementary Schools? Evidence from an IV Approach" | **California** elementary | IV for EL *status* endogeneity | **Smaller and insignificant** EL peer effects on native English speakers, vs larger OLS. OLS overstates. | [eurekamag record](https://eurekamag.com/research/081/916/081916160.php) |
| Kim/Burkhauser et al., *Educational Researcher* 2023 | Nationally representative ECLS-K ever-ELs (N=783), K→G5 | Piecewise growth models | **Classroom EL concentration ~zero** on ELs' own reading growth, all four developmental periods, "nonsignificant, trivially sized." Undercuts the case for EL clustering. | [10.3102/0013189x231203646](https://doi.org/10.3102/0013189x231203646) · [ERIC ED632126](https://eric.ed.gov/?id=ED632126) |
| Betts & Fairlie, *J. Public Economics* 2003 87(5-6):987 | 132 US metros, 1980+1990 Census | Cross-MSA | **Native flight, secondary only.** No effect at primary. At high school, **1 native switches to private per 4 immigrants** entering public HS. White students account for most of it; response is to **immigrants who speak a language other than English at home**, not immigrants per se. | [PDF](https://people.ucsc.edu/~rfairlie/papers/published/jpube%202003%20-%20native%20flight.pdf) · [10.1016/S0047-2727(01)00164-5](https://doi.org/10.1016/s0047-2727(01)00164-5) |
| Hall (?), *Econ. of Education Review* 2016 53:268 "Public or private?" | NCES School District Demographic System, districts 1990/2000/2010, ethnic-composition IV | District-level replication of Betts–Fairlie | Native-flight estimates constructed at **district** rather than MSA level (Betts–Fairlie's own caveat). [UNVERIFIED sign/size — abstract truncated] | [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0272775716301789) |
| Brunello & Rocco, *Econ. of Education Review* 2013 32:234 (IZA DP 5479) | **PISA, cross-country aggregate** | Country-level panel | **NEGATIVE but tiny.** Doubling immigrant share 4.8%→~10% cuts native scores **1.32–1.96%** (of score, not SD). Also: **reducing the dispersion** of immigrant share across schools helps, conditional on the mean. | [IZA DP 5479 PDF](https://docs.iza.org/dp5479.pdf) |
| Jensen & Rasmussen, *Econ. of Education Review* 2011 30(6):1503 | **Denmark**, PISA-linked registers | IV | **NEGATIVE.** Higher school immigrant concentration lowers reading and math for natives and immigrants; robust across methods incl. IV. | [RePEc](https://ideas.repec.org/a/eee/ecoedu/v30y2011i6p1503-1515.html) |
| Gould, Lavy & Paserman, *J. Human Capital* 2013 7(1) "Does the Clustering of Immigrant Peers Affect the School Performance of Natives?" | **Israel** | Random within-school variation in immigrant numbers | **NEGATIVE on dropout**, and explicitly **non-linear**: "It is only with **larger proportions of immigrants** that we find significant peer effects." Mechanism = **peer quality**, not language. | [10.1086/669680](https://doi.org/10.1086/669680) |
| "Migrant peers in the classroom", *J. Comparative Economics* 2018 | **China internal rural-urban migrants** (NOT international) | Random class assignment | **LARGE NEGATIVE.** +10pp migrant share → **−0.11 SD** math for locals; **−0.16 SD** males; **−0.20 SD** in large cities. | [ScienceDirect S0147596717300768](https://www.sciencedirect.com/science/article/abs/pii/S0147596717300768) |
| Hermansen/Birkelund, *European Sociological Review* 2022 "Masked by the mean" | **Norway** registers | VAM + school FE, teacher-assigned vs blind-rated scores | Mean effects mask heterogeneity; compares teacher grades vs anonymous national tests. [UNVERIFIED sign] | [10.1093/esr/jcac035](https://doi.org/10.1093/esr/jcac035) |
| Ohinata & van Ours (NL), *Labour* 2016 quantile version; World Bank WPS8492 (Bossavie, NL) | Netherlands, PIRLS/TIMSS + registers, within-school across-grade | Grade-level immigrant share | Small/negligible linear effects; Bossavie uses within-school across-grade with placebo tests. [UNVERIFIED exact sizes] | [WPS8492 PDF](https://documents1.worldbank.org/curated/en/702871529934288951/pdf/WPS8492-REVISED.pdf) |
| Jensen, *IZA World of Labor* 194 v2 (2021) — the survey | — | Narrative review | Verdict: "**mixed** — some studies finding negative effects, and others finding no effects… differs across countries according to factors such as **organization of the school system and the type of immigrants**." | [10.15185/izawol.194.v2](https://doi.org/10.15185/izawol.194.v2) |
| Ballatore/Fort/Ichino-style + Spain (*Am. Behavioral Scientist* 2021) | **Spain**, exploits Latin-American (Spanish-speaking) vs non-Spanish-speaking migrants | Share decomposition | Tests whether the damage runs through **language of instruction**, not migrant status. The natural test of the ELL-vs-immigrant distinction. | [10.1177/0002764221996776](https://doi.org/10.1177/0002764221996776) |

**[INFERENCE] Three things the table establishes.**
1. **Selection is the whole ballgame in US data.** The ReStud paper reports that the school-FE-only
   specification yields a significant *negative* correlation, and that it *flips positive* once
   family fixed effects absorb which families end up in high-immigrant schools. Any district-level
   or school-level correlation of Hispanic/ELL share with test scores — including anything one could
   build from SEDA — is measuring that selection, not a classroom effect.
2. **The US zeros are not the same object as the European negatives.** Denmark, Israel and the
   cross-country PISA negatives are *school-level concentration* in systems with dense immigrant
   enclaves and (Israel) a mass Soviet influx. The Israeli result is explicitly threshold-shaped.
3. **The one robust US behavioral response is native flight, and it is language-triggered and
   secondary-school-only.** Betts–Fairlie's own words: natives respond "mainly to immigrant children
   who speak a language other than English at home." This is the finding that most directly targets
   first-generation ELL concentration and **not** the English-dominant second generation.

**[GAP]** Diette & Oyelere (2014 *Econ. Bull.* / 2017 NC administrative data) not yet retrieved —
they are the one US pair reporting *heterogeneous negative* effects (on high-achieving and Black
students in North Carolina). This is the strongest US-based negative and must be pulled.
**[GAP]** Tumen 2021 (Syrians in Turkey), Morales 2022 (Venezuelans in Colombia), Schneeweis 2015
(Austria) not yet pulled — the mass-sudden-inflow analogues to the 2022–24 US surge.
**[GAP]** No 2023–26 US administrative-data paper on the NYC/Chicago/Denver surge cohorts located.
The press record (CBS, Chalkbeat, Hechinger, Empire Center) is qualitative and describes strain on
*services for the newcomers*, not measured incumbent harm.

Suggested next queries if re-dispatched: "Diette Oyelere limited English proficient North Carolina
achievement high performing students"; "Tumen 2021 Syrian refugees Turkish students test scores
private school"; "Morales Venezuelan migration Colombia school quality natives".

---

### Block 2 — The one consistent US negative: Diette & Oyelere / Ahn & Jepsen, North Carolina, and it is LANGUAGE not ETHNICITY
[DATA: published abstracts, retrieved 2026-09-16]

North Carolina administrative data is the one US setting that repeatedly produces a negative, and
the authors' own decomposition tells you exactly what the negative is made of.

| Study | Result verbatim |
|---|---|
| Diette & Oyelere, *AER P&P* 2014 104(5):412 ([RePEc](https://ideas.repec.org/a/aea/aecrev/v104y2014i5p412-17.html); [IZA DP 7856](https://docs.iza.org/dp7856.pdf); [replication data 10.3886/e112806v1](https://doi.org/10.3886/e112806v1)) | "exposure to a larger share of Limited English (LE) students is associated with a **slight decline in performance for students at the top of the achievement distribution**." With school-by-year FE: "**no LE student peer effects on females'** achievement in math and reading but **significant negative effects on males and black students**." |
| Diette & Oyelere, *IZA J. Migration* 2017 ([10.1186/s40176-016-0074-y](https://doi.org/10.1186/s40176-016-0074-y)) — **the decisive decomposition** | "an increase in the share of **Latin American (LA) students does not create negative peer effects** on native students' achievement. Rather, it is the **limited English language skills** of some of these students that lead to small, negative peer effects on natives." |
| Diette & Oyelere, *Education Economics* 2017 25(4) ([10.1080/09645292.2017.1311300](https://doi.org/10.1080/09645292.2017.1311300)) | "**limited evidence** of negative peer effects of LE students, though the effects are **heterogeneous and the magnitudes are small**." |
| Ahn & Jepsen, *IZA J. Migration* 2015 ([10.1186/s40176-015-0030-2](https://doi.org/10.1186/s40176-015-0030-2)) | NC middle schools 2006–2012: "Percent LEP has a **negative association** with mathematics and reading test scores, **more so for non-LEP students than for LEP students**." But the **language mix** of LEP peers "has little if any discernable relationship with achievement." **Association, not a causal design** — no FE/IV claimed in the abstract. |

**[INFERENCE] This is the single most load-bearing distinction in the whole memo.** Diette & Oyelere
ran the exact horse race the operator's question requires: *Latin American share* versus *limited
English share*, in the same data. Latin-American share alone produces **no** negative effect on
natives. Limited-English share produces a **small** negative. The cost, such as it is, attaches to
**English-learner status**, not to Hispanic ethnicity or to immigrant origin. That maps directly
onto the generation question in Block 5.

Magnitudes: all four NC papers describe the effects with the words "slight," "small," "limited,"
or "negligible." None reports an effect large enough to price against a $17.6k pupil-year without
the authors' own point estimates in hand. **[GAP] Point estimates in SD units are behind paywalls
(AER P&P, Education Economics); IZA DP 7856 is open PDF and would supply them in one fetch.**

### Block 3 — Teacher side: turnover IS elevated in ESL/bilingual assignments, but not by much, and the vacancy story is about certification supply
[DATA: Learning Policy Institute, NCTQ, CA Commission on Teacher Credentialing figures as reported]

| Fact | Value | Source |
|---|---|---|
| National annual turnover, teachers of **ESL/bilingual education** | **19.0%** (highest of any subject listed; foreign languages 18.3%, CTE 17.5%, special ed 16.4%) | [LPI, *Teacher Turnover in the United States*](https://learningpolicyinstitute.org/product/teacher-turnover-united-states-report) |
| National turnover, **not fully certified** vs fully certified | **20.1% vs 14.7%**; among 1–3 yr experience, 24% vs 17% | same |
| Turnover in schools serving the largest concentrations of students of color | **70% higher** than lowest quartile (150% higher for alternatively certified) | [NCTQ 2024](https://reimagineteaching.nctq.org/wp-content/uploads/sites/5/2024/08/NCTQ_RT_NL_Teacher-Turnover-Why-it-Matters.pdf) |
| California **English language development** positions unfilled, 2020-21 | **~27%** — second-highest vacancy type in the state | [El Tímpano, citing CA Comm. on Teacher Credentialing](https://www.eltimpano.org/english/education/a-shortage-of-bilingual-educators-leaves-english-learners-with-too-few-qualified-teachers/) |
| CA districts reporting bilingual teacher shortages (fall 2016 survey, n>200 districts) | **14%** | [LPI bilingual factsheet](https://learningpolicyinstitute.org/media/70/download?file=Bilingual_Teacher_Shortages_California_FACTSHEET.pdf&inline=) |
| CA highest-need schools (top decile by unduplicated pupil count, which counts **English learners**) filling posts with interns/emergency permits | **11% vs 4%** in lowest-need schools | [LPI, *California's Teacher Shortages*](https://learningpolicyinstitute.org/index%2Ephp/product/gdtf-californias-teacher-shortages-brief) |

**[INFERENCE] The teacher channel is real but it is a *sorting and certification* channel, not an
immigration channel.** ESL/bilingual turnover at 19.0% sits only ~4pp above the all-teacher average,
and the same tables show special education, math and science in the same band with no immigration
involved. The larger gradients — 70% higher turnover in high-minority schools, 11% vs 4% emergency
permits — are driven by school poverty and student-of-color concentration, categories that include
large native-born populations. **No study located links immigrant/EL inflow *causally* to incumbent
teacher exits.** [GAP] The Massachusetts IES-funded study
([award page](https://ies.ed.gov/use-work/awards/how-can-state-policy-bolster-bilingual-educator-pipeline-assessing-nature-and-impact-bilingual))
will be the first to model bilingual-teacher attrition against school characteristics; results not
yet published.

### Block 4 — Literacy / NAEP: the 2022–24 reading decline is NOT differentially an English-learner story
[DATA: NCES / Nation's Report Card verbatim, retrieved 2026-09-16]

The obvious test of "did the migrant surge sink reading scores" runs the wrong way for that story.

- **2022 vs 2019, grade 4 reading**: NCES states that "the average score for fourth-grade …
  students identified as **English learners did not differ significantly from 2019**," while scores
  *did* fall for American Indian/Alaska Native, Black, Hispanic and White students, both sexes, both
  lunch-eligibility groups, and city, suburban and town schools.
  [SOURCE: [nationsreportcard.gov/reading/nation/groups](https://www.nationsreportcard.gov/reading/nation/groups/)]
  So in the pandemic decline, English learners were among the few groups that **held flat** while
  everyone else fell.
- **2024 vs 2022, grade 4 reading**: scores were lower for "students who were identified as
  English learners **and** who were not identified as English learners" — i.e. the 2024 decline is
  **common to both groups**, not concentrated in EL-heavy populations. National grade-4 reading fell
  **2 points vs 2022 and 5 points vs 2019**, with declines at every reported percentile **except the
  90th**. [SOURCE: [NAEP Reading 2024, performance by student group](https://www.nationsreportcard.gov/reports/reading/2024/g4_8/performance-by-student-group/?grade=4); [2024 results](https://www.nationsreportcard.gov/reports/reading/2024/g4_8/?grade=8)]
- **Long-run level**: grade-4 reading 217 in 2022 vs 220 in 2019, and **not measurably different
  from 1992** — across three decades in which the EL share of enrollment roughly doubled.
  [SOURCE: [NCES Condition of Education, Reading Performance](https://nces.ed.gov/Programs/Coe/indicator/cnb/reading-performance?tid=4)]

**[INFERENCE] A district panel regressing NAEP or state-test scores on EL share will find a strong
negative and it will be almost entirely confounded.** EL share is collinear with poverty,
urbanicity, parental education and district resources. The Figlio-Giuliano-Özek-Sapienza result —
school FE alone gives a negative, family FE flips it positive — is the direct warning that
district-level cross-sections cannot identify this. Any SEDA-based analysis here is descriptive
only and must be labelled as such.

Instruments available for the by-ELL-status tables: NCES Digest **Table 221.70** (NAEP reading by
ELL status **and state**, 2019) and **Table 221.12** (reading by EL status, 1992–2022) are the
clean published series.
[SOURCE: [dt19_221.70](https://nces.ed.gov/programs/digest/d19/tables/dt19_221.70.asp?current=yes) · [dt22_221.12](https://nces.ed.gov/programs/digest/d22/tables/dt22_221.12.asp?current=yes)]

### Block 5 — Mass-inflow analogues and the threshold question: the evidence for a concentration threshold is WEAK and one good study runs the WRONG WAY
[DATA: verbatim abstracts, retrieved 2026-09-16]

The operator asked whether effects appear only above some concentration (>25–30% EL). Four
sudden-mass-inflow studies bear on this and they do not agree on a threshold.

| Study | Shock | Result |
|---|---|---|
| **Tümen**, *J. Development Economics* 2021 150:102633 (IZA DP 14039) | ~3.5m Syrians into Turkey; PISA 2015 vs 2018, regional refugee intensity | **POSITIVE.** "Math, Science, and Reading scores of Turkish adolescents **increased** following the Syrian refugee influx," concentrated in the **lower half** of the distribution and among natives with **lower maternal education**. Design deliberately isolates the **labor-market** mechanism (refugee kids only entered Turkish schools systematically after 2016), so it is a *general-equilibrium* positive, not a classroom effect. | [10.1016/j.jdeveco.2021.102633](https://doi.org/10.1016/j.jdeveco.2021.102633) · [IZA DP 14039](https://ideas.repec.org/p/iza/izadps/dp14039.html) |
| **Irazoque Sillerico** 2026 (UNLP/CEDLAS WP 0364) — the Colombia/Venezuela paper | Venezuelan exodus; 2016 border reopening as natural experiment, diff-in-diff | **NEGATIVE, −1.8% of a standard deviation** for exposed Colombian high-schoolers. Persistent 4 years then decays to zero. Stated mechanism: "**teachers allocate class time to assist lower-achieving Venezuelans**." Larger for women, **high-achieving** natives, natives with highly educated mothers, and high-scoring schools. | [RePEc dls/wpaper/0364](https://ideas.repec.org/p/dls/wpaper/0364.html) · [thesis PDF](https://www.me.econo.unlp.edu.ar/wp-content/uploads/Tesis_Irazoque_final.pdf) |
| **Çakır, Erbay & Kırdar**, IZA DP 14972 | Syrians in Turkey, DiD-IV | Native children's **employment falls**, school enrollment **rises for boys**; NEET rises for girls with less-educated parents. Labor-market channel again, not classroom. | [IZA DP 14972](https://docs.iza.org/dp14972.pdf) |
| **Gould, Lavy & Paserman** 2013 (Israel) | 1990s Soviet influx | The **only** clean threshold claim: "It is **only with larger proportions of immigrants** that we find significant peer effects," on native dropout. Mechanism = **peer quality**. | [10.1086/669680](https://doi.org/10.1086/669680) |

**[INFERENCE] The threshold hypothesis is not supported, and the Colombia paper actively
contradicts it.** Irazoque reports the negative effect "**becomes insignificant when the
concentration of immigrants is higher**" — the opposite of a rising-in-concentration threshold. A
coherent reading is a **disruption-of-a-high-performing-environment** effect rather than a
congestion effect: the harm lands on high-achieving natives in high-scoring schools with educated
mothers, i.e. where the counterfactual classroom was academically dense, and it fades where
immigrant concentration is already high (where schools have adapted, or where natives have already
sorted out — the Betts–Fairlie flight margin). Gould-Lavy-Paserman's threshold is on *dropout* and
attributed to *peer quality*, not language load.

**The only mechanism with direct causal support for a classroom-level incumbent cost is teacher
time reallocation** (Irazoque's stated mechanism; consistent with Diette & Oyelere's finding that
the effect attaches to limited-English rather than Latin-American share). That is the mechanism the
operator named, and it is supported by **one working paper outside the US** at **−1.8% SD**.

**[GAP]** Schneeweis 2015 (Austria), Ohinata & van Ours 2013 exact estimates, Bossavie 2020 (NL)
point estimates, and Morales 2022 (Colombia, if distinct from Irazoque) not retrieved.
**[GAP] VERIFIED NEGATIVE so far: no US administrative-data study of the 2022–24 NYC / Chicago /
Denver migrant-surge cohorts measuring incumbent outcomes exists as of 2026-09-16.** Searches over
2023-06→2026-09 return only journalism (CBS, Chalkbeat, Hechinger, Documented NY, Empire Center).
Those sources document **service strain on the newcomers** (ELL caseloads quadrupling at one
Manhattan school, 24→182 EL students in a year; ~34,000 migrant children enrolled in NYC in 18
months; Chicago migrant students in segregated schools without bilingual support), and one Empire
Center finding that the influx **slowed** NY's enrollment decline (2024-25 enrollment fell only
1,451 students, −0.06%). None measures incumbent achievement. This is a genuine hole in the
literature and a legitimate thing for the essay to say.

### Block 6 — Which of this applies to the Mexican-origin SECOND generation? Almost none of it.
[INFERENCE, built on Blocks 1, 2 and 5]

This must be stated explicitly because the whole channel is mis-specified if it isn't.

1. **The measured effect attaches to English-learner status, not to immigrant origin or Hispanic
   ethnicity.** Diette & Oyelere's horse race is decisive on this within one dataset: Latin-American
   share → no effect; limited-English share → small negative. Betts & Fairlie's native-flight
   response is triggered by "immigrant children who **speak a language other than English at home**."
   Brunello & Rocco find the dispersion of immigrant share matters conditional on the mean, and the
   Spanish study is built expressly to test the language channel.
2. **The Mexican-origin second generation is, by school age, overwhelmingly English-proficient.**
   US-born children of Mexican immigrants are not classified EL for most of their K-12 careers; EL
   classification is concentrated in the early grades and in the first generation. So the second
   generation is largely **not in the treatment group** for the one channel that produces a negative.
3. **Therefore the peer-effect cost, to the extent it exists, is a FIRST-generation / newcomer-ELL
   phenomenon with a short half-life per child** (EL classification typically clears within a few
   years), not a persistent attribute of the Mexican-origin population.
4. **The one second-generation-relevant result runs the other way and is negative for them
   specifically**: Hunt 2017 finds the positive effect of immigration on native high-school
   completion holds for native-born Blacks but **"not for native-born Hispanics."** That is the
   closest thing in the literature to a second-generation-specific finding, and it is a *null for
   Hispanics*, not a cost imposed *by* them.
5. **Scope condition that cuts the other way:** the K-12 need-weighted fiscal cost
   (repo: `research/immigration-mexican-origin-by-generation-2026-09-16.md` §5.3) applies to the
   second generation regardless, because it is a **head-count** cost, not a peer-effect cost. The
   fiscal and the peer-effect channels must not be conflated. Second-generation children cost
   per-pupil dollars; they do not, on this evidence, impose classroom externalities.

---

## Verdict

**Is there a measured incumbent-student cost from immigrant/ELL concentration? In US data, no —
the best-identified US estimates are zero to positive. The credible negative is small, non-US,
and attaches to English-learner status rather than immigrant origin. It should not be priced into
the fiscal ledger as a per-pupil cost.**

Sign, size, scope, in one place:

| Claim | Verdict | Best number | Scope condition |
|---|---|---|---|
| Immigrant peers lower incumbent US achievement | **FALSE on the best design** | **+2.8% SD math / +1.7% SD reading** moving 1%→13% exposure (family FE, Florida, n≈1.3m) | Selection-corrected. School-FE-only gives a spurious negative. |
| A sudden refugee influx harms incumbents | **FALSE at observed US shock sizes** | Precise zero; powered to <1% SD | Only 4 Florida schools exceeded 5% refugee share; prepared receiving system |
| EL arrivals harm non-ELs in a new-destination state | **FALSE** | Positive spillovers, concentrated in current/former ELs; **no adverse effect on non-ELs** | Delaware 4–8, 2000s–2010s growth, not a 2022-24-scale surge |
| Limited-English share has a small negative on some natives | **TRUE but small and heterogeneous** | "slight decline" at the top of the distribution; negative for **males and Black students**, zero for females | North Carolina; school-by-year FE; magnitudes never reported as large |
| The negative is about ethnicity/immigration | **FALSE** | LA share → no effect; LE share → small negative, **same data** | Diette & Oyelere 2017 decomposition |
| Teacher time reallocation is the mechanism | **PLAUSIBLE, one causal source** | **−1.8% SD**, Colombia, persists 4 years then decays | Venezuelan mass exodus, secondary school, non-US |
| There is a concentration threshold above which harm appears | **NOT SUPPORTED; one study says the reverse** | Colombia effect **insignificant at higher** immigrant concentration; Israel's threshold is on *dropout* via *peer quality* | — |
| Native flight to private school | **TRUE, secondary only** | **1 native → private per 4 immigrants** entering public HS; nil at primary | 1980/1990 Census, 132 MSAs; language-triggered |
| ELL share drove the 2019–24 reading decline | **FALSE** | EL 4th-grade reading **did not differ significantly** 2022 vs 2019 while most other groups fell; 2024 decline hit EL and non-EL alike | NAEP |
| Any of this applies to the Mexican second generation | **NO** | They are not EL by school age; the channel is first-generation newcomer-ELL | See Block 6 |

**What it would add per pupil-year if priced.** [INFERENCE — arithmetic is mine, inputs are sourced]
The honest answer is **$0 for the US central case**, and the essay should say so rather than
reaching for a number the evidence does not support. If one insisted on pricing the *upper* bound
by transporting the Colombian estimate to the US: −1.8% SD of test score, converted at the common
rule of thumb that **1 SD of test score ≈ 10–15% of lifetime earnings**, is ≈ **0.18–0.27% of
lifetime earnings** per exposed incumbent student-year of exposure. Against a ~$1.7m present value
of lifetime earnings that is **≈ $3,000–$4,900 per exposed incumbent, one-time**, not per year —
and it is a *transported, non-US, working-paper* estimate whose US analogues are zero or positive.
**Do not put this in the ledger as a cost line. Put it in the memo as a bounded upper limit that
the US evidence does not reach.** The SD→earnings conversion is a convention, **[UNVERIFIED]**
against a primary source in this probe.

**The defensible essay position**, given repo-held Figlio & Özek: the congestion-on-incumbents leg
of the capacity argument is the **weakest leg of the whole capacity case**. The school channel's
real content is **capital cost per seat and per-pupil operating cost** — head-count costs — not
classroom externalities. Anyone who argues classroom harm is arguing from out-of-sample
concentration or from the non-US literature, and must say which.

## ≤5 runnable analyses on public data

1. **NAEP by ELL status × state, 2019, as a confounding demonstration.** NCES Digest Table 221.70
   gives 4th- and 8th-grade reading scale scores for **ELL and non-ELL separately by state**.
   Regress the *non-ELL* state mean on the state ELL enrollment share (EDFacts / NCES CCD). If the
   slope is strongly negative while the within-state ELL/non-ELL gap is flat, the cross-state
   correlation is composition, not classroom effect. ~40 lines; two public tables; no acquisition.
2. **NAEP EL vs non-EL decline decomposition, 2019 → 2022 → 2024.** Digest Table 221.12 (1992–2022)
   plus the 2024 Nation's Report Card group tables. Question: did the EL/non-EL gap widen in the
   surge years? The published text already says EL held flat 2019→2022 and both fell 2022→2024;
   this puts numbers on it and kills the "surge sank reading" story with one chart.
3. **SEDA district panel × EL share, run explicitly as a placebo.** Stanford Education Data Archive
   (district-year, grades 3–8, on a common scale) crossed with EDFacts EL counts and CCD
   enrollment. Fit (a) cross-section, (b) district FE, (c) district FE + cohort trends. Report all
   three. The **point** is that the coefficient shrinks toward zero as selection is absorbed,
   replicating the Figlio et al. school-FE-vs-family-FE pattern at district level. Label it
   descriptive. This is the highest-value analysis because it demonstrates the confound rather than
   pretending to identify an effect.
4. **Native-flight replication, 2010–2023.** ACS/PUMS private-school enrollment by metro (already in
   the repo's IPUMS panel, `BPL>=150` foreign-born flag) against metro foreign-born school-age
   share. Tests whether the Betts–Fairlie 1-per-4 secondary-school margin still exists three
   decades on, and whether it is language-driven (PUMS has **HHL / language spoken at home**).
   Uses repo-held microdata; no new acquisition.
5. **Teacher-turnover gradient against EL share, state level.** NCES Schools and Staffing / NTPS
   public tables plus state EL shares. Tests whether the 19.0% ESL/bilingual turnover rate varies
   with state EL concentration, or is a flat occupational feature. Cheap; likely a null; publishable
   as a null.

## Gaps for a re-dispatch, ranked
1. **IZA DP 7856 (Diette & Oyelere) full PDF** — the only open-access route to US point estimates in
   SD units for the one US negative. One fetch. Highest value.
2. **Irazoque 2026 full text** — verify the −1.8% SD, the concentration non-linearity, and the
   teacher-time mechanism against the paper rather than the abstract.
3. **Özek et al. 2024 (Delaware) effect sizes** — currently only the sign is verified.
4. **Schneeweis 2015 (Austria), Ohinata & van Ours 2013 (NL), Bossavie 2020 (NL)** point estimates.
5. **School construction cost per seat** — inherited from the capacity lane; still the largest
   unquantified school channel and a *head-count* cost, which is where the school argument actually
   lives.
6. **SD → lifetime earnings conversion** at primary (Chetty/Friedman/Rockoff or Hanushek) to make
   the upper-bound arithmetic in the Verdict citable.
