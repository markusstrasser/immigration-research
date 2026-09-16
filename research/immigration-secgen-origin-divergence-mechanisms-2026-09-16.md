claude-opus-5[1m]

# Second-Generation Divergence by National Origin — Mechanism Evaluation

**Verdict:** The divergence is not one mechanism. The two with real identification are parental
unauthorized status (1.24 years of schooling, IRCA-instrumented, structurally near-zero for
refugee-origin Asians) and parental English (an A-grade IV that explains levels for every
non-English origin and therefore cannot explain why Vietnamese children beat Mexican ones).
Selectivity relative to origin is the organizing fact but a small individual coefficient, about
0.3-0.5 child-years for a 40-percentile gap. Part of the measured Asian-Latino gap is instrument
error: ethnic attrition is positively selected for Hispanics and negatively selected for Asians, so
it widens the observed gap from both ends, and "third-generation stagnation" is partly a
third-versus-fourth-plus pooling artifact. Family structure runs the wrong way; ethnic capital and
refugee resettlement have no identified estimate at all. [INFERENCE on the ranking]

**Question:** Why do children of low-skill immigrant origins diverge so sharply in education,
earnings and incarceration — Vietnamese, Chinese and (partly) Central American second generations
outperforming Mexican, Dominican and Cambodian/Laotian/Hmong — and which mechanisms carry
well-identified evidence? Ranking and prior sources: §5 of
[the incarceration memo](immigration-mexican-origin-generation-incarceration-2026-09-16.md).

### Verified block 1 — parental selectivity and parental legal status

**Feliciano & Lanuza 2017, ASR 82(1):211–241, DOI 10.1177/0003122416684777** [SOURCE: full
text fetched to corpus this session]. Add Health Wave 1 (1994–95) → Wave 4 (2008–09) linked to
Barro-Lee country education distributions; analytic N = 9,285 (subsample with parents ≤12 years
of schooling, N = 3,509). "Contextual attainment" = Ichou's (2014) percentile: share of
same-age, same-sex peers in the origin country with lower education + 0.5 × share with the same
education; the higher-scoring parent is used. OLS on child's completed years of schooling:

| Model | Absolute parental years | Relative (contextual) percentile |
|---|---|---|
| Absolute only | 0.274 (0.016) | — |
| Relative only | — | 0.023 (0.001) |
| Both | 0.192 (0.030) | 0.008 (0.003) |
| Both + aspirations | 0.165 (0.027) | 0.006 (0.003) |
| Both + aspirations + HS GPA | 0.107 (0.023) | 0.004 (0.002)† |
| Both, parents ≤12 yrs schooling (N=3,509) | 0.150 (0.063) | 0.012 (0.006) |

Reading: relative position survives conditioning on absolute education, and survives *better* in
the low-parental-education subsample (0.012 vs 0.008) — the Vietnamese/Chinese/Mexican comparison
of interest. The magnitude is small: 0.008 × 40 percentiles ≈ 0.3 child-years, ≈ 0.5 in the
low-education subsample, and most of it runs through aspirations and GPA (a mediation claim, not
an exclusion restriction). Grade **B+** (nationally representative panel, sharp construct,
observational, Barro-Lee cell error, no origin-side instrument). [SOURCE: Tables 3, 4, A2]

**Bean, Leach, Brown, Bachmeier & Hipp 2011, IMR 45(2):348–385, DOI
10.1111/j.1747-7379.2011.00851.x** [SOURCE: full text fetched this session]. IIMMLA 2004,
five-county Los Angeles, adults 20–40; analytic N = 2,526 (935 Mexican-origin, 1,591 Asian-origin:
399 Chinese, 400 Korean, 400 Vietnamese, 392 Filipino). Parental unauthorized status is
*reconstructed* from adult children's retrospective reports, with an imputation rule: a parent who
entered on a temporary visa or border-crossing card, later became LPR, has less than high school
and 5+ years here is coded unauthorized-at-entry. Child's schooling penalty from a mother who
stayed unauthorized versus one who entered legally or legalized:

| Estimator | Effect on child's years of schooling |
|---|---|
| Raw difference | 2.04 |
| OLS with parental selectivity + covariates | 1.51 |
| 2SLS, IRCA amnesty eligibility as instrument | 1.24 |

Mixed-status class premiums vs both-parents-unauthorized (Table 6, Model 5, IPTW) run +1.10 to
+1.53 years, all p<.01, except mother-unauthorized/father-legalized at −0.36 (n.s.).

The design detail that matters: **the legal-status analysis is Mexican-only by construction** —
unauthorized status is near-absent among the IIMMLA Asian samples, so no legal-status penalty is
estimated for Chinese, Korean, Vietnamese or Filipino origin. Grade **B** (the IV is IRCA
eligibility, a function of arrival date and so correlated with cohort quality and the child's birth
cohort; status imputed, not observed; one metro). [SOURCE: Tables 1, 6, Appendix A]

### Verified block 2 — ethnic attrition, and the Chetty mobility benchmark

**The single most important measurement fact for this memo: attrition biases run in OPPOSITE
directions for Hispanics and Asians, so they inflate the observed Asian–Latino second-generation
gap from both ends.** Duncan & Trejo 2016, NBER w21982, "The Complexity of Immigrant Generations",
2003–2013 CPS: second-generation Hispanics who do *not* identify as Hispanic average **0.76 years
more** education than those who do; second-generation Asians who do not identify as Asian average
about **0.6 years less** (a deficit). Attrition rates: second generation 7% Hispanic / 21% Asian;
third-generation children 18% Hispanic / 42% Asian, with Mexican third-generation children at 12%
and Salvadorans and Japanese above 50%, Indians above 60%. Per-origin attrition coefficients
(second-generation adults, SE): Mexico +0.76 (.11), Puerto Rico +0.63 (.13), Dominican Republic
+0.40 (.27), El Salvador +0.30 (.20), Cuba +0.15 (.18). Attrition concentrates in mixed origins:
third-generation children with the ethnicity on both sides attrit at 2% (Hispanic) / 7% (Asian),
one side only at 35% / 55%. [SOURCE: https://doi.org/10.3386/w21982, Tables 1, 2, 6, 7]
Grade **A** for the description (large CPS samples, objective vs subjective definitions side by
side), **C** for any causal correction (the authors themselves say the results "shed more light on
the direction rather than the ultimate magnitude" and that it is "unknown whether correcting for
selective ethnic attrition would produce a small or large improvement").

**How much of the Mexican third-generation deficit is attrition?** Two answers from the same
authors, disagreeing in size:
- Duncan & Trejo 2011, JOLE 29(2), DOI 10.1086/658088: ~30% of third-generation Mexican children in
  CPS are not identified as Mexican; their dropout rate is 25% higher in the self-ID sample (3.4%
  vs 2.7%), and on the objective definition dropout (2.7%) equals third+-generation non-Hispanic
  whites. But their own Table 10 reconstruction raises third-generation fathers' schooling only
  0.25 years and mothers' 0.19; at a transmission rate below 0.5 that is **"hidden" progress on the
  order of 0.1 years**, which they call a lower bound since intermarried families' advantage is
  mostly unobserved.
- Duncan, Grogger, León & Trejo 2019, *Labour Economics* 60:101771 (NBER w24067): NLSY97 records
  grandparents' birthplaces, so the third generation is objective. Attrition is negligible for the
  1.5 and second generations (100%, 95% identify) and 21% for the objective third generation;
  third-generation non-identifiers average ~2/3 year more schooling and 29% vs 23% BA — **on 11
  people**, as the authors say. The substantive result: "substantial educational progress between
  second- and third-generation Mexicans that is largely hidden when we instead ... aggregate the
  third and higher generations into a 'third+' generation", with third-generation high-school
  graduation "only slightly below" fourth+-generation whites. Geographic roots (Texas vs
  California), parental schooling and family structure shrink the fourth+ deficit "by up to 40
  percent" without eliminating it. Grade **B+** (right fix for generation coding; the
  attrition-selectivity cell is N=11 and cannot carry a magnitude).

Net reading: attrition is a **large classification problem** (12–21% of third-generation Mexicans,
42% of third-generation Asian children) with a **small and poorly bounded effect on measured
attainment** (0.1 years by the one explicit calculation). The better-documented error is the
third-vs-fourth+ pooling artifact, which is a different thing. "Mexican third-generation
stagnation is a measurement artifact" overreads both papers. [INFERENCE]

**Chetty, Hendren, Jones & Porter 2020, QJE 135(2):711–783, DOI 10.1093/qje/qjz042** [SOURCE: full
text fetched this session]. Population-wide tax and census records, 1989–2015 cohorts. Child mean
income rank at parent rank 25: whites 45, Hispanics 43, Blacks 32.6. The Hispanic–white gap is
projected to fall from 22 percentiles (parents) to 10 (children) to **5.7 in steady state**
(Hispanic 48.7 vs white 54.4); Hispanic *natives* alone reach 47.3. The paper does **not** discuss
ethnic attrition, a live threat to exactly this projection, since the higher-attaining descendants
are the ones who exit the label. Grade **A** for the mobility estimates, **B−** for the steady-state
projection (a Markov extrapolation at fixed transition rates, no attrition adjustment). No origin
breakdown in the text; the authors point to online data tables by parental country of birth —
**[GAP]** worth pulling, since that is the origin-specific series this memo lacks.

### Verified block 3 — parental English (best-identified here) and refugee status

**Bleakley & Chin 2008, JHR 43(2):267–298, DOI 10.1353/jhr.2008.0028** [SOURCE: full text
fetched this session]. 2000 Census 1%+5% PUMS; N = 164,559 US-born children under 18 living with a
parent aged 25–55 who immigrated before age 18 (148,039 non-English-origin, 16,520
English-origin). Identification: the critical-period drop in language acquisition by age at
arrival, differenced against immigrants from English-speaking countries so that non-language
age-at-arrival effects are netted out (2SLS-DD); 2SLS-D drops the control group and assumes zero
non-language age-at-arrival effect. Effects of a one-unit increase in parental English (0–3 scale):

| Outcome | 2SLS-DD | 2SLS-D |
|---|---|---|
| Child English proficiency (5–17) | 0.169 (0.021) just-ID; 0.161 (0.020) over-ID | — |
| Attends school, age 3 | 0.131 (0.075) | 0.044 (0.018) |
| Attends school, age 4 | 0.053 (0.028) | 0.056 (0.010) |
| Dropped out of HS, 15–17 | −0.0177 (0.0058) | −0.0072 (0.0033) |
| Below age-appropriate grade, 15–17 | −0.0432 (0.0159) | −0.0239 (0.0058) |

Scale: −1.77 points on dropout is about **80% of the mean dropout rate** of children of
non-English-speaking immigrants; −4.32 on grade retardation is about **60%**. Hispanic-restricted
estimates are nearly identical (−0.0154, −0.0410); effects concentrate in below-median-GDP origins.
Mediation says **parental education is the main channel**, which weakens a pure-language reading.
Grade **A−** (real exclusion restriction, differenced control, huge N; residual worry is that age
at arrival also shifts parental schooling and networks). It is the strongest causal estimate here
and it is **origin-blind** — Vietnamese and Chinese parents have worse English than Mexican parents
on average and their children still out-attain. A level mechanism, not a divergence one.
[INFERENCE]

**Evans & Fitzgerald 2017, NBER w23498** [SOURCE:
https://www.nber.org/system/files/working_papers/w23498/w23498.pdf, abstract and results verified].
ACS 2010–2014, refugees separated from other immigrants by the Capps et al. (2015) country-year
procedure, ~20,000 refugees entering 1990–2014. Refugees entering **before age 14 graduate high
school and enter college at the same rate as natives**; older-teen entrants lag, attributed to
language and unaccompanied arrival. Controlling for education there is "no difference in economic
outcomes between refugees who arrived as children and U.S.-born survey respondents." Adult
refugees (18–45 at entry) start 23.7 and 13.2 points below natives on high-school and college
completion, cross the native employment rate at year 7, never converge on earnings.

The **[GAP] that matters**: this is the 1.5 generation, not the second, and the comparison group is
US natives throughout, never non-refugee immigrants with the same education. So it cannot separate
"resettlement support" from "arrived young." Grade **B** for the refugee-child result, **C** as
evidence for mechanism 3 as dispatched. Nothing found this session estimates a resettlement effect
on the US-born children of refugees. [GAP]

### Verified block 4 — remaining mechanisms

**Selectivity, the group-level version.** Feliciano 2005, IMR 39(4):841–871, DOI
10.1111/j.1747-7379.2005.tb00291.x: 32 immigrant groups, origin-country education distributions
against US Census/CPS. Nearly all US streams are *positively* selected, Asians most strongly, and
"the more positive selection of Asian immigrants helps explain their second generations' higher
college attendance rates as compared to Europeans, Afro-Caribbeans, and Latinos." The design is
**ecological — unit = group, N = 32** — so it cannot separate selectivity from anything else
varying at origin-group level (visa channel, settlement geography, co-ethnic institutions, race).
Grade **C+** as causal evidence, **A** as the framing fact; Feliciano & Lanuza 2017 is the
individual-level upgrade and its coefficient is small. [SOURCE: abstract verified at DOI]

**Ethnic capital.** Borjas 1992, QJE 107(1), DOI 10.2307/2118325, and Borjas 1993, JOLE 11(1):
next-generation skills depend on parental inputs *and* on mean ethnic-group skill, so groups
regress to their own ethnic mean, not the national one. **Not identified** — the ethnic mean is a
group-level regressor collinear with selectivity and everything else group-level, and Borjas
treats it as an externality assumption. Zhou & Bankston's Vietnamese New Orleans work and Lee &
Zhou's "success frame" are ethnographies with no effect size. Grade **C**. The one
quasi-experimental co-ethnic result in the repo (Martén, Hainmueller & Hangartner 2019, PNAS,
Swiss refugee assignment) is first-generation labour-market entry, not children.

**Family structure and early fertility — this one reverses.** Darney et al. 2022, *J Adolescent
Health*, DOI 10.1016/j.jadohealth.2022.06.021: adjusted probability of an adolescent birth is 30.1%
for foreign-born Mexican-origin Latinas, 29.9% for women in Mexico, **26.2% for US-born
Mexican-Americans**, 11.6% for US-born non-Latina whites, the gap running through contraceptive
use, not age at first sex. Goldberg 2018 (Add Health Waves 1–4, N = 8,777 women), DOI
10.1111/jomf.12478: foreign-born and **second-generation** women initiate sex and childbearing
*later* than those with US-born parents. Early childbearing is a Mexican-vs-white gap that narrows
with generation, not a second-generation penalty, and cannot drive origin divergence in the claimed
direction. Where it does bite: Levine & Painter 2003, *ReStat* 85(4):884–900, within-school
propensity matching, find teen out-of-wedlock childbearing cuts education "substantially, although
far less than the cross-sectional comparisons of means suggest." Grade **B**. A
**disconfirmation** of mechanism 5 as dispatched. [INFERENCE on direction]

**Discrimination and phenotype.** Murguía & Telles 1996, *Sociology of Education*, DOI
10.2307/2112715, 1979 National Chicano Survey: the lightest, most European-looking quarter of
Mexican Americans had about **1.5 more years of schooling** than the darker majority, surviving
controls (7.0% vs 19.2% and 18.0% in the lowest education category; 10.2% vs 4.2% and 5.3% college
completion). The effect is **place- and cohort-contingent**: strong in Texas, "virtually no
effects in California"; ~2 years for pre-1935 cohorts, closing for 1935–44, reappearing for
1945–54. Telles & Ortiz 2008 *Generations of Exclusion* (1965 UCLA survey re-interviewed 2000; 684
respondents, 758 children, Los Angeles and San Antonio) is the four-generation companion:
attainment peaks in the second generation and declines after, attributed to school underfunding and
racialization. Grade **B** for Murguía–Telles (interviewer-rated phenotype; the coefficient falls
once parental education enters, itself downstream of parental phenotype), **C+** for Telles–Ortiz
(two metros, 35-year attrition, and its third/fourth-generation decline is exactly the pattern
Duncan–Grogger–León–Trejo show is contaminated by pooling and attrition). A discrimination effect
strong in Texas and absent in California predicts an origin-by-place interaction, largely untested
on modern data. [GAP]

**Direct decompositions.** Sakamoto & Woo 2007, *Sociological Inquiry* 77(1), DOI
10.1111/j.1475-682X.2007.00177.x, and Sakamoto, Iceland & Siskar 2021, *PRPR* 41 (ACS 2012–2016)
are the best origin-disaggregated series for the Southeast Asian refugee origins. **No paper
reachable this session decomposes the Asian–Latino second-generation gap into selectivity + legal
status + language + place on one dataset.** [GAP — the highest-value thing the repo could build.]

## Ranked mechanism table

Ranked by (identification grade × plausible share of the origin gap). "Applies to" names the
origins where the mechanism can operate at all.

| # | Mechanism | Best evidence | Effect size | ID grade | Applies to |
|---|---|---|---|---|---|
| 1 | Parental unauthorized status | Bean et al. 2011, IIMMLA, IRCA-eligibility 2SLS | 1.24 yr (2SLS), 1.51 (OLS), 2.04 raw | B | Mexican, Central American; ~0 for refugee-origin Vietnamese/Cambodian/Hmong and for Chinese/Korean/Filipino in this sample |
| 2 | Parental English proficiency | Bleakley & Chin 2008, critical-period IV, N=164,559 | −1.8 pt dropout (≈80% of the mean), −4.3 pt grade retardation (≈60%) per unit English | A− | All non-English origins — so it explains *levels*, not the Asian–Latino divergence |
| 3 | Measurement: attrition + 3rd/4th+ pooling | Duncan & Trejo 2016; Duncan, Grogger, León & Trejo 2019 | +0.76 yr for Hispanic attriters, −0.6 for Asian; 12–21% of 3rd-gen Mexicans, 42% of 3rd-gen Asian children; explicit correction only ≈0.1 yr | A (description), C (magnitude) | Mexican and Asian, opposite directions — inflates the measured gap from both ends |
| 4 | Parental selectivity relative to origin | Feliciano & Lanuza 2017 (individual); Feliciano 2005 (group) | 0.008 yr per percentile (0.012 for low-educated parents) → ≈0.3–0.5 yr for a 40-point selectivity gap | B+ / C+ | All; largest Asian–Mexican contrast, but small once absolute education is held |
| 5 | Age at arrival (1.5 gen), incl. refugee children | Evans & Fitzgerald 2017 | Arrival before 14 → native-equal HS and college entry; older teens lag | B | Refugee origins (Vietnamese, Cambodian, Laotian, Hmong, Cuban) and any child migrant |
| 6 | Discrimination / phenotype | Murguía & Telles 1996 | 1.5 yr light vs dark; ~2 yr pre-1935 cohorts; Texas strong, California ~0 | B | Mexican (indigenous-phenotype gradient); no comparable estimate for Asian origins |
| 7 | Neighbourhood / school context | Chetty et al. 2020 QJE | Hispanic child rank 43 vs white 45 at parent rank 25; gap projected 22 → 10 → 5.7 percentiles | A (mobility), B− (projection) | All Hispanics pooled; no origin breakdown in the text |
| 8 | Ethnic capital / co-ethnic institutions | Borjas 1992/1993; Zhou & Bankston; Lee & Zhou | No identified estimate | C | Asserted for Vietnamese and Chinese |
| 9 | Refugee resettlement support per se | — | No second-generation estimate found | — [GAP] | Vietnamese, Cambodian, Laotian, Hmong, Cuban |
| 10 | Family structure / early childbearing | Darney 2022; Goldberg 2018; Levine & Painter 2003 | Second-generation fertility is *later*, not earlier; adolescent-birth probability falls 30.1% → 26.2% from first to later US-born generations | B | Mexican-origin vs white, but the sign is wrong for a second-generation divergence story |


## Disconfirmation search

- **Against selectivity as the answer:** Feliciano & Lanuza's own individual coefficient (0.008
  years per percentile) is an order of magnitude below what the group-level story implies, and van
  de Werfhorst & Heath 2018 (EJP, ten destinations) plus Ferrara & Luthra 2024 (*SSR* 103016) find
  its explanatory power partial and destination-contingent.
- **Against family structure (mechanism 5):** found the opposite sign. Second-generation women
  delay sex and childbearing relative to third-plus, and Mexican-American adolescent-birth
  probability (26.2%) is *below* the foreign-born figure (30.1%). Mechanism 5 is demoted.
- **Against "the third-generation deficit is a measurement artifact":** Duncan & Trejo's own
  reconstruction yields ~0.1 hidden years and the NLSY97 selectivity cell is N=11 — directionally
  supported, quantitatively unsupported.
- **Against a pure discrimination reading:** the phenotype effect is ~0 in California, large in
  Texas, largest in pre-WWII cohorts. A constant-discrimination model does not fit its own best
  evidence.
- **Against legal status as *the* Mexican factor:** the estimate exists only for Mexicans because
  unauthorized status is near-absent in the IIMMLA Asian samples. What is established is the
  largest factor that is Mexican-specific *by construction of the available data*.
- **Against culture (steel-manned first):** the strongest version is Lee & Zhou's success frame —
  hyperselected parents import origin-country elite norms plus co-ethnic supplementary-education
  institutions, so low-income Chinese and Vietnamese children still out-attain. Every measured
  input in it is group-level and collinear with selectivity, so the ethnography cannot separate the
  norm from the selection that produced it. Plausible, unmeasured, unranked.

## Five testable claims for CPS/ACS in this repo

1. **Attrition asymmetry inflates the measured Asian–Latino gap.** CPS ASEC (`PEFNTVTY`,
   `PEMNTVTY`, `PRDTHSP`, `PTDTRACE`, `PEEDUCA`): compute second-generation attainment by origin
   twice, by parental birthplace alone and again requiring Hispanic/Asian self-ID. Predicted: the
   Mexican mean rises, the Chinese/Vietnamese mean falls, gap narrows 0.5–1.0 years.
2. **The legal-status penalty as a within-origin cohort break.** ACS PUMS (`YRIMMIG`, `CITIZEN`,
   `BPL`, `EDUC`, `AGE`): compare second-generation Mexican attainment for children of 1977–1981
   arrivals (IRCA-eligible) against 1987–1991 arrivals (ineligible), holding parental education.
   Bean's 1.24 years predicts a break; no break falsifies IIMMLA out of sample.
3. **English is a level, not a divergence, mechanism.** ACS PUMS (`SPEAKENG`, `LANGUAGE`, `BPL`):
   regress second-generation attainment on parental English by origin. Predicted: parental English
   enters strongly and *uniformly* and the Vietnam and China dummies stay positive after it —
   falsifying mechanism 2 as an origin-gap explanation while keeping it as a level effect.
4. **Discrimination as an origin × state interaction.** ACS PUMS by state, Mexican second
   generation, Texas versus California, `EDUC` and `INCEARN`. Murguía & Telles predicts a residual
   Texas penalty; Duncan et al. 2019 predicts the same from geographic roots. A *null* kills both.
5. **Third-generation identification, done properly.** CPS ASEC pooled 2003–2025, children living
   with parents (grandparent birthplace recoverable through the parents' `PEFNTVTY`/`PEMNTVTY`):
   build the objective third generation and compare its attainment path with the self-ID
   "third-plus" series the repo uses now. Predicted: the Mexican plateau shrinks, not vanishes.

## Coverage and gaps

**[GAP]** no identified estimate exists for ethnic capital or for refugee-resettlement effects on
the *second* generation; Chetty's online data tables with second-generation mobility by parental
birth country were not pulled and are the highest-value external addition; and no paper decomposes
the Asian–Latino second-generation gap into selectivity, legal status, language and place on one
dataset — claims 1 and 3 above are the cheapest route to building it here.
